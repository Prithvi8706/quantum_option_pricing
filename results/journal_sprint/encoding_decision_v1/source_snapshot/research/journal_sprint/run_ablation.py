"""Week-7 fixed factorial discovery with paired, valid guard inference arms."""

import argparse
from dataclasses import asdict
from itertools import product
import json
import os
import shutil
import time

from .calibrated_readout import invert_calibrated
from .fixed_costs import fixed_allocation, schedule_cost
from .intervals import price_decision, response
from .run_fixed_discovery import COST_FIELDS, DESIGNS, checked_inputs, designs_for, summarize_cell
from .storage import ROOT, finish_run, rng_for, sha256, start_run, write_json
from .tighter_grid import tighter_bounds_for
from research.paper_a.benchmark import C6, by_id
from research.paper_a.payoff import a_calc
from research.paper_a.references import black_scholes_call, grid_points, grid_probabilities

BUDGETS = (294912, 1179648)
CALIBRATIONS = (4096, 16384)
CONDITIONS = {
    "stationary": (0.02, 0.07, 0.0),
    "small_transfer": (0.03, 0.06, 0.01),
    "boundary_transfer": (0.05, 0.04, 0.03),
}
GUARDS = (0.0, 0.01, 0.03)
KEY_FIELDS = ("contract", "budget", "calibration_n", "condition", "design")


def cells():
    return product(C6, BUDGETS, CALIBRATIONS, CONDITIONS, DESIGNS)


def valid_guards(condition):
    return tuple(g for g in GUARDS if g >= CONDITIONS[condition][2])


def configuration(manifests, hashes):
    return dict(
        protocol="PROTOCOL_W7_ABLATION",
        contracts=list(C6),
        budgets=list(BUDGETS),
        calibration_sizes=list(CALIBRATIONS),
        conditions={k: list(v) for k, v in CONDITIONS.items()},
        guards=list(GUARDS),
        designs=list(DESIGNS),
        repetitions=100,
        n=6,
        scale=0.125,
        tolerance=1.0,
        alpha_calibration=0.025,
        alpha_validation=0.025,
        calibration_rates=[0.02, 0.07],
        max_seconds=900,
        max_record_bytes=500_000_000,
        readiness_delivery=0.9,
        readiness_gain=0.1,
        input_manifests=manifests,
        dependency_sha256=hashes,
    )


def prepare(ledger, profiles):
    result = {}
    for cid in C6:
        bound, _ = tighter_bounds_for(by_id(cid), 6, 0.125)
        p = dict(
            bounds=asdict(bound), bound_total=bound.total, refused=bound.total >= 1, designs={}
        )
        if not p["refused"]:
            baseline = designs_for(cid, BUDGETS[0], ledger, profiles[cid])
            for budget in BUDGETS:
                direct, a = fixed_allocation(profiles[cid], budget, "A_equivalents")
                _, cx = fixed_allocation(profiles[cid], budget, "logical_cx")
                p["designs"][str(budget)] = {
                    name: dict(
                        depths=depths, shots=shots, cost=schedule_cost(profiles[cid], depths, shots)
                    )
                    for name, depths, shots in (
                        ("direct", [0], direct),
                        ("A_matched", [0, 1, 2], a),
                        ("CX_capped", [0, 1, 2], cx),
                    )
                }
            if p["designs"][str(BUDGETS[0])] != baseline:
                raise ValueError("baseline ledger mismatch")
        result[cid] = p
    return result


def diagnostic_truths(prepared):
    result = {}
    for cid, p in prepared.items():
        if p["refused"]:
            continue
        c, b = by_id(cid), p["bounds"]
        a = a_calc(
            grid_probabilities(c, b["lower"], b["upper"], 6),
            grid_points(b["lower"], b["upper"], 6),
            c.K,
            b["upper"],
            0.125,
        )
        price = float(black_scholes_call(c.S0, c.K, c.r, c.sigma, c.T))
        if abs(b["offset"] + b["sensitivity"] * a - price) > p["bound_total"] + 1e-9:
            raise ValueError("diagnostic representation mismatch")
        result[cid] = dict(amplitude=a, price=price)
    return result


def trial(key, rep, prepared, truth):
    cid, budget, ncal, condition, design = key
    seed = ("week7_ablation", *key, rep)
    row = dict(zip(KEY_FIELDS, key), rep=rep, seed_key=seed)
    if prepared["refused"]:
        row.update(
            status="pre_refusal",
            cost={k: 0 for k in COST_FIELDS},
            arms={str(g): dict(status="pre_refusal") for g in valid_guards(condition)},
        )
        return row
    fixed = prepared["designs"][str(budget)][design]
    depths, shots = fixed["depths"], fixed["shots"]
    f, g, _ = CONDITIONS[condition]
    errors = rng_for(*seed, "calibration").binomial(ncal, [0.02, 0.07])
    counts = rng_for(*seed, "validation").binomial(
        shots, f + (1 - f - g) * response(truth["amplitude"], depths)
    )
    cost = dict(fixed["cost"], calibration_shots=2 * ncal, total_shots=sum(shots) + 2 * ncal)
    arms = {}
    for guard in valid_guards(condition):
        conf, cal = invert_calibrated(
            counts,
            shots,
            depths,
            errors,
            [ncal] * 2,
            alpha_calibration=0.025,
            alpha_validation=0.025,
            transfer_bounds=(guard, guard),
        )
        b = prepared["bounds"]
        decision = price_decision(conf, b["sensitivity"], b["offset"], prepared["bound_total"], 1.0)
        interval = decision["interval"]
        arms[str(guard)] = dict(
            **decision,
            components=conf.components,
            calibration=cal,
            amplitude_contains=conf.contains(truth["amplitude"]),
            price_contains=bool(
                interval is not None and interval[0] <= truth["price"] <= interval[1]
            ),
            false_declaration=bool(
                decision["status"] == "precision_met"
                and abs(sum(interval) / 2 - truth["price"]) > 1
            ),
        )
    row.update(
        status="acquired",
        depths=depths,
        shots=shots,
        cost=cost,
        counts=counts.tolist(),
        calibration_errors=errors.tolist(),
        arms=arms,
    )
    return row


def summarize(rows):
    base = {k: rows[0][k] for k in KEY_FIELDS}
    acquired = sum(r["status"] == "acquired" for r in rows)
    arms = {}
    for guard in rows[0]["arms"]:
        arm_rows = [dict(r["arms"][guard], cost=r["cost"]) for r in rows]
        summary = summarize_cell(arm_rows)
        summary.pop("acquisition_totals")
        summary["nonempty_intervals"] = sum(r.get("interval") is not None for r in arm_rows)
        arms[guard] = summary
    return dict(
        **base,
        attempts=len(rows),
        acquired=acquired,
        refused=len(rows) - acquired,
        acquisition_totals={
            k: sum(r["cost"][k] for r in rows) for k in COST_FIELDS if not k.startswith("max_")
        },
        arms=arms,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/journal_sprint/week7_ablation_v1")
    args = parser.parse_args()
    if shutil.disk_usage(ROOT).free < 1_000_000_000:
        raise RuntimeError("need 1 GB free disk")
    ledger, profiles, manifests = checked_inputs()
    sources = sorted((ROOT / "research/journal_sprint").rglob("*.py"))
    sources += sorted((ROOT / "research/paper_a").glob("*.py"))
    sources += [ROOT / "docs/journal_sprint/PROTOCOL_W7_ABLATION.md"]
    config = configuration(manifests, {str(p.relative_to(ROOT)): sha256(p) for p in sources})
    path = start_run(args.output, config)
    tick, attempts = time.perf_counter(), 0
    try:
        for source in sources:
            target = path / "source_snapshot" / source.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            if sha256(target) != config["dependency_sha256"][str(source.relative_to(ROOT))]:
                raise ValueError("snapshot changed")
        setup = time.perf_counter()
        prepared = prepare(ledger, profiles)
        write_json(path / "decisions.json", prepared)
        write_json(path / "setup.json", dict(bound_design_seconds=time.perf_counter() - setup))
        truths = diagnostic_truths(prepared)
        write_json(path / "diagnostic_truths.json", truths)
        summaries = []
        with (path / "records.jsonl").open("x", encoding="utf-8") as stream:
            for key in cells():
                if time.perf_counter() - tick > 900 or stream.tell() > 500_000_000:
                    raise RuntimeError("between-cell execution limit; incomplete run")
                rows = [trial(key, rep, prepared[key[0]], truths.get(key[0])) for rep in range(100)]
                for row in rows:
                    stream.write(json.dumps(row, allow_nan=False) + "\n")
                    attempts += 1
                stream.flush()
                os.fsync(stream.fileno())
                summaries.append(summarize(rows))
        write_json(
            path / "summary.json",
            dict(attempts=attempts, cells=summaries, elapsed_seconds=time.perf_counter() - tick),
        )
        finish_run(path)
        print(path)
    except Exception as error:
        write_json(path / "failure.json", dict(attempts=attempts, error=str(error)))
        raise


if __name__ == "__main__":
    main()
