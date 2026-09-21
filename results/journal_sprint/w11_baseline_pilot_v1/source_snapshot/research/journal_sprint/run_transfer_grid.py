"""Fixed week-6 discovery; no observed outcome changes any allocation."""

import argparse
from dataclasses import asdict
from itertools import product
import json
import os
import shutil
import time

from .calibrated_readout import invert_calibrated
from .intervals import price_decision, response
from .run_fixed_discovery import COST_FIELDS, DESIGNS, checked_inputs, designs_for, summarize_cell
from .storage import ROOT, finish_run, rng_for, sha256, start_run, write_json
from .tighter_grid import tighter_bounds_for
from research.paper_a.benchmark import C6, by_id
from research.paper_a.payoff import a_calc
from research.paper_a.references import black_scholes_call, grid_points, grid_probabilities

CALIBRATIONS = (4096, 16384)
SHIFTS = tuple(product((-0.02, 0.0, 0.03), (-0.03, 0.0, 0.03)))


def cells():
    return product(C6, CALIBRATIONS, range(9), DESIGNS)


def trial(cid, calibration_n, position, design, rep, prepared, truth):
    key = ("week6_grid", cid, calibration_n, position, design, rep)
    row = dict(
        contract=cid,
        calibration_n=calibration_n,
        position=position,
        design=design,
        rep=rep,
        seed_key=key,
    )
    if prepared["refused"]:
        row.update(status="pre_refusal", cost={k: 0 for k in COST_FIELDS})
        return row
    fixed = prepared["designs"][design]
    depths, shots = fixed["depths"], fixed["shots"]
    df, dg = SHIFTS[position]
    f, g = 0.02 + df, 0.07 + dg
    errors = rng_for(*key, "calibration").binomial(calibration_n, [0.02, 0.07])
    counts = rng_for(*key, "validation").binomial(
        shots, f + (1 - f - g) * response(truth["amplitude"], depths)
    )
    confidence, calibration = invert_calibrated(
        counts,
        shots,
        depths,
        errors,
        [calibration_n] * 2,
        alpha_calibration=0.025,
        alpha_validation=0.025,
        transfer_bounds=(0.03, 0.03),
    )
    b = prepared["bounds"]
    decision = price_decision(
        confidence, b["sensitivity"], b["offset"], prepared["bound_total"], 1.0
    )
    interval = decision["interval"]
    cost = dict(fixed["cost"])
    cost.update(calibration_shots=2 * calibration_n, total_shots=sum(shots) + 2 * calibration_n)
    row.update(
        **decision,
        counts=counts.tolist(),
        calibration_errors=errors.tolist(),
        calibration=calibration,
        depths=depths,
        shots=shots,
        cost=cost,
        components=confidence.components,
        amplitude_contains=confidence.contains(truth["amplitude"]),
        price_contains=bool(interval is not None and interval[0] <= truth["price"] <= interval[1]),
        false_declaration=bool(
            decision["status"] == "precision_met" and abs(sum(interval) / 2 - truth["price"]) > 1
        ),
    )
    return row


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/journal_sprint/week6_transfer_grid_v1")
    args = parser.parse_args()
    if shutil.disk_usage(ROOT).free < 1_000_000_000:
        raise RuntimeError("need 1 GB free before launch")
    ledger, profiles, manifests = checked_inputs()
    sources = sorted((ROOT / "research/journal_sprint").rglob("*.py"))
    sources += sorted((ROOT / "research/paper_a").glob("*.py"))
    sources += [ROOT / "docs/journal_sprint/PROTOCOL_W6_TRANSFER_GRID.md"]
    config = dict(
        protocol="PROTOCOL_W6_TRANSFER_GRID",
        contracts=list(C6),
        calibration_sizes=CALIBRATIONS,
        shifts=SHIFTS,
        designs=DESIGNS,
        repetitions=100,
        budget=294912,
        n=6,
        scale=0.125,
        tolerance=1.0,
        alpha_calibration=0.025,
        alpha_validation=0.025,
        transfer_bounds=[0.03, 0.03],
        calibration_rates=[0.02, 0.07],
        max_seconds=900,
        max_record_bytes=250_000_000,
        input_manifests=manifests,
        dependency_sha256={str(p.relative_to(ROOT)): sha256(p) for p in sources},
    )
    path = start_run(args.output, config)
    tick = time.perf_counter()
    attempts = 0
    try:
        for source in sources:
            target = path / "source_snapshot" / source.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            if sha256(target) != config["dependency_sha256"][str(source.relative_to(ROOT))]:
                raise ValueError("source changed during snapshot")
        prepared = {}
        for cid in C6:
            bound, _ = tighter_bounds_for(by_id(cid), 6, 0.125)
            refused = bound.total >= 1
            prepared[cid] = dict(
                bounds=asdict(bound),
                bound_total=bound.total,
                refused=refused,
                designs={} if refused else designs_for(cid, 294912, ledger, profiles[cid]),
            )
        write_json(path / "decisions.json", prepared)
        truths = {}
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
                raise ValueError("diagnostic bound mismatch")
            truths[cid] = dict(amplitude=a, price=price)
        write_json(path / "diagnostic_truths.json", truths)
        summaries = []
        with (path / "records.jsonl").open("x", encoding="utf-8") as stream:
            for cid, ncal, position, design in cells():
                if time.perf_counter() - tick > 900 or stream.tell() > 250_000_000:
                    raise RuntimeError("between-cell execution limit; incomplete run")
                rows = [
                    trial(cid, ncal, position, design, rep, prepared[cid], truths.get(cid))
                    for rep in range(100)
                ]
                for row in rows:
                    stream.write(json.dumps(row, allow_nan=False) + "\n")
                    attempts += 1
                stream.flush()
                os.fsync(stream.fileno())
                summaries.append(
                    dict(
                        contract=cid,
                        calibration_n=ncal,
                        position=position,
                        design=design,
                        **summarize_cell(rows),
                    )
                )
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
