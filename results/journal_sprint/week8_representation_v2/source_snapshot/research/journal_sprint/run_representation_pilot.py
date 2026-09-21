"""Paid representation pilot followed by one fresh fixed validation batch."""

import argparse
from dataclasses import asdict
from itertools import product
import json
import math
import os
import shutil
import time

from .calibrated_readout import invert_calibrated
from .fixed_costs import schedule_cost
from .intervals import price_decision, response
from .run_fixed_discovery import COST_FIELDS, checked_inputs
from .storage import ROOT, finish_run, rng_for, sha256, start_run, write_json
from .tighter_grid import tighter_bounds_for
from research.paper_a.benchmark import C6, by_id
from research.paper_a.payoff import a_calc
from research.paper_a.references import black_scholes_call, grid_points, grid_probabilities

NS = (5, 6)
POLICIES = ("fixed_n5", "fixed_n6", "pilot_select")
CONDITIONS = {
    "stationary": (0.02, 0.07),
    "small_transfer": (0.03, 0.06),
    "boundary_transfer": (0.05, 0.04),
}
CX_CAP = 330301440
KEY_FIELDS = ("contract", "condition", "policy")


def cells():
    return product(C6, CONDITIONS, POLICIES)


def configuration(manifests, hashes):
    return dict(
        protocol="PROTOCOL_W8_REPRESENTATION",
        contracts=list(C6),
        ns=list(NS),
        scale=0.125,
        policies=list(POLICIES),
        conditions={k: list(v) for k, v in CONDITIONS.items()},
        repetitions=100,
        cx_cap=CX_CAP,
        pilot_shots_per_depth=1024,
        pilot_calibration_per_state=4096,
        validation_calibration_per_state=16384,
        guard=0.03,
        tolerance=1.0,
        alpha_calibration=0.025,
        alpha_validation=0.025,
        max_seconds=900,
        max_bytes=250_000_000,
        readiness_delivery=0.9,
        readiness_mean_gain=0.1,
        input_manifests=manifests,
        dependency_sha256=hashes,
    )


def inputs():
    _, _, manifests = checked_inputs()
    profiles = {}
    for name in ("week3_resources_v1", "week5_resources_v1"):
        rows = json.loads((ROOT / f"results/journal_sprint/{name}/summary.json").read_text())[
            "rows"
        ]
        for r in rows:
            if r["n"] in NS and r["scale"] == 0.125:
                group = profiles.setdefault((r["contract"], r["n"]), {})
                if r["k"] in group:
                    raise ValueError("duplicate profile")
                group[r["k"]] = r
    return profiles, manifests


def prepare(profiles):
    menu = {}
    for cid in C6:
        menu[cid] = {}
        for n in NS:
            b, _ = tighter_bounds_for(by_id(cid), n, 0.125)
            entry = dict(n=n, bounds=asdict(b), bound_total=b.total, eligible=b.total < 1)
            if entry["eligible"]:
                p = profiles[cid, n]
                if set(p) != {0, 1, 2}:
                    raise ValueError("missing compiled profile")
                entry["profiles"] = {str(k): v for k, v in p.items()}
                entry["ladder_cx"] = sum(v["gates"]["cx"] for v in p.values())
            menu[cid][str(n)] = entry
    return menu


def truths_for(menu):
    truths = {}
    for cid, entries in menu.items():
        truths[cid] = {}
        for n, e in entries.items():
            if not e["eligible"]:
                continue
            c, b = by_id(cid), e["bounds"]
            a = a_calc(
                grid_probabilities(c, b["lower"], b["upper"], int(n)),
                grid_points(b["lower"], b["upper"], int(n)),
                c.K,
                b["upper"],
                0.125,
            )
            p = float(black_scholes_call(c.S0, c.K, c.r, c.sigma, c.T))
            if abs(b["offset"] + b["sensitivity"] * a - p) > e["bound_total"] + 1e-9:
                raise ValueError("diagnostic bound failure")
            truths[cid][n] = dict(amplitude=a, price=p)
    return truths


def select_candidate(scores):
    """Strict target-free boundary: only observable pilot radii and candidate IDs."""
    if not scores:
        raise ValueError("no candidates")
    seen = set()
    for s in scores:
        if (
            set(s) != {"n", "radius"}
            or type(s["n"]) is not int
            or s["n"] not in NS
            or s["n"] in seen
        ):
            raise ValueError("invalid selector fields or candidate")
        seen.add(s["n"])
        if s["radius"] is not None and (not math.isfinite(s["radius"]) or s["radius"] < 0):
            raise ValueError("invalid pilot radius")
    return min(scores, key=lambda s: (math.inf if s["radius"] is None else s["radius"], s["n"]))[
        "n"
    ]


def cost(entry, shots, ncal):
    return schedule_cost(
        {int(k): v for k, v in entry["profiles"].items()}, [0, 1, 2], [shots] * 3, 2 * ncal
    )


def add_costs(parts):
    return {
        k: (
            max((p[k] for p in parts), default=0)
            if k.startswith("max_")
            else sum(p[k] for p in parts)
        )
        for k in COST_FIELDS
    }


def batch(seed, phase, entry, shots, ncal, condition, truth):
    errors = rng_for(*seed, phase, entry["n"], "calibration").binomial(ncal, [0.02, 0.07])
    f, g = CONDITIONS[condition]
    counts = rng_for(*seed, phase, entry["n"], "validation").binomial(
        [shots] * 3, f + (1 - f - g) * response(truth["amplitude"], [0, 1, 2])
    )
    conf, cal = invert_calibrated(
        counts,
        [shots] * 3,
        [0, 1, 2],
        errors,
        [ncal] * 2,
        alpha_calibration=0.025,
        alpha_validation=0.025,
        transfer_bounds=(0.03, 0.03),
    )
    b = entry["bounds"]
    decision = price_decision(conf, b["sensitivity"], b["offset"], entry["bound_total"], 1.0)
    return dict(
        n=entry["n"],
        shots=[shots] * 3,
        calibration_shots_per_state=ncal,
        counts=counts.tolist(),
        calibration_errors=errors.tolist(),
        calibration=cal,
        components=conf.components,
        cost=cost(entry, shots, ncal),
        **decision,
    )


def trial(key, rep, menu, truths, on_selection=None):
    cid, condition, policy = key
    if policy not in POLICIES or condition not in CONDITIONS:
        raise ValueError("unknown procedure condition or policy")
    seed = ("week8_representation", *key, rep)
    row = dict(zip(KEY_FIELDS, key), rep=rep, seed_key=seed, pilots=[])
    eligible = [n for n in NS if menu[str(n)]["eligible"]]
    desired = 5 if policy == "fixed_n5" else 6 if policy == "fixed_n6" else None
    candidates = eligible if desired is None else [desired] if desired in eligible else []
    if not candidates:
        event = dict(**row, selected_n=None, reason="pre_refusal", scores=[], validation_shots=None)
        if on_selection:
            on_selection(event)
        return dict(event, status="pre_refusal", cost=add_costs([]))
    scores = []
    if policy == "pilot_select" and len(candidates) > 1:
        for n in candidates:
            pilot = batch(seed, "pilot", menu[str(n)], 1024, 4096, condition, truths[str(n)])
            row["pilots"].append(pilot)
            scores.append(dict(n=n, radius=pilot["radius"]))
        selected = select_candidate(scores)
        reason = "pilot_rank"
    else:
        selected = candidates[0]
        reason = "sole_candidate" if policy == "pilot_select" else "fixed"
    spent = add_costs([p["cost"] for p in row["pilots"]])
    entry = menu[str(selected)]
    shots = (CX_CAP - spent["pricing_logical_cx"]) // entry["ladder_cx"]
    if shots < 1:
        raise ValueError("pilot exhausted budget")
    event = dict(**row, selected_n=selected, reason=reason, scores=scores, validation_shots=shots)
    if on_selection:
        on_selection(event)
    final = batch(seed, "final", entry, shots, 16384, condition, truths[str(selected)])
    interval = final["interval"]
    truth = truths[str(selected)]
    final.update(
        price_contains=bool(interval is not None and interval[0] <= truth["price"] <= interval[1]),
        false_declaration=bool(
            final["status"] == "precision_met" and abs(sum(interval) / 2 - truth["price"]) > 1
        ),
        amplitude_contains=any(lo <= truth["amplitude"] <= hi for lo, hi in final["components"]),
        deterministic_radius=entry["bound_total"],
        statistical_radius=None
        if final["radius"] is None
        else final["radius"] - entry["bound_total"],
        component_count=len(final["components"]),
    )
    total = add_costs([p["cost"] for p in row["pilots"]] + [final["cost"]])
    if total["pricing_logical_cx"] > CX_CAP or total["calibration_shots"] > 49152:
        raise ValueError("procedure cost cap")
    return dict(event, status=final["status"], final=final, cost=total)


def summarize(rows):
    from .run_fixed_discovery import summarize_cell

    expanded = [dict(r.get("final", {}), status=r["status"], cost=r["cost"]) for r in rows]
    result = summarize_cell(expanded)
    result.update(
        pilot_acquisitions=sum(len(r["pilots"]) for r in rows),
        selected_counts={str(n): sum(r["selected_n"] == n for r in rows) for n in NS},
        nonempty_intervals=sum(r.get("interval") is not None for r in expanded),
        multicomponent_intervals=sum(r.get("component_count", 0) > 1 for r in expanded),
    )
    return dict(**{k: rows[0][k] for k in KEY_FIELDS}, **result)


def check_limits(elapsed, record_bytes):
    if elapsed > 900 or record_bytes > 250_000_000:
        raise RuntimeError("execution limit; incomplete")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/journal_sprint/week8_representation_v1")
    args = parser.parse_args()
    if shutil.disk_usage(ROOT).free < 1_000_000_000:
        raise RuntimeError("need 1 GB free")
    profiles, manifests = inputs()
    sources = sorted((ROOT / "research/journal_sprint").rglob("*.py"))
    sources += sorted((ROOT / "research/paper_a").glob("*.py"))
    sources += [ROOT / "docs/journal_sprint/PROTOCOL_W8_REPRESENTATION.md"]
    config = configuration(manifests, {str(p.relative_to(ROOT)): sha256(p) for p in sources})
    path = start_run(args.output, config)
    tick, attempts = time.perf_counter(), 0
    try:
        for p in sources:
            target = path / "source_snapshot" / p.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target)
            if sha256(target) != config["dependency_sha256"][str(p.relative_to(ROOT))]:
                raise ValueError("snapshot drift")
        start = time.perf_counter()
        menu = prepare(profiles)
        write_json(path / "menu.json", menu)
        write_json(path / "setup.json", dict(bound_menu_seconds=time.perf_counter() - start))
        truths = truths_for(menu)
        write_json(path / "diagnostic_truths.json", truths)
        summaries = []
        with (
            (path / "events.jsonl").open("x", encoding="utf-8") as events,
            (path / "records.jsonl").open("x", encoding="utf-8") as records,
        ):

            def persist(event):
                events.write(json.dumps(event, allow_nan=False) + "\n")
                events.flush()
                os.fsync(events.fileno())

            for key in cells():
                check_limits(time.perf_counter() - tick, events.tell() + records.tell())
                rows = []
                for rep in range(100):
                    row = trial(key, rep, menu[key[0]], truths[key[0]], persist)
                    records.write(json.dumps(row, allow_nan=False) + "\n")
                    rows.append(row)
                    attempts += 1
                records.flush()
                os.fsync(records.fileno())
                summaries.append(summarize(rows))
                check_limits(time.perf_counter() - tick, events.tell() + records.tell())
        write_json(
            path / "summary.json",
            dict(attempts=attempts, cells=summaries, elapsed_seconds=time.perf_counter() - tick),
        )
        finish_run(path)
        print(path)
    except Exception as e:
        write_json(path / "failure.json", dict(attempts=attempts, error=str(e)))
        raise


if __name__ == "__main__":
    main()
