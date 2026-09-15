"""Matched total-shot check; all observations synthetic, no quantum speedup claim."""

import argparse
import json
from pathlib import Path
import shutil

from .allocation_rule import allocate, cp_decision, preselect
from .encoding_decision import Encoding, calibration_menu, fixed_price_interval, plan_menu
from .run_encoding_decision import SOURCE, load_profiles, verify_inventory
from .storage import ROOT, finish_run, rng_for, sha256, start_run, write_json
from research.paper_a.benchmark import C6, by_id
from research.paper_a.references import black_scholes_call


PROTOCOL = ROOT / "docs/journal_sprint/PROTOCOL_ALLOCATION_V1.md"
ARMS = ("fixed_cp", "pilot_cp", "single_hoeffding")
SCENARIOS = {"design_match": (0.02, 0.07), "swapped": (0.07, 0.02)}


def trial(name, profiles, guard, scenario, arm, rep):
    encodings = []
    for label in ("linearized", "exact_table"):
        b = profiles[label]["bounds"]
        encodings.append(Encoding(label, b["sensitivity"], b["offset"],
                                  b["support"] + b["grid"] + b["encoding"], 1))
    choice = preselect(encodings)
    row = dict(contract=name, guard=guard, scenario=scenario, arm=arm, rep=rep,
               choice=choice, status="not_certified", interval=None, radius=None,
               pilot_shots=0, pilot_successes=None, calibration_shots=0,
               calibration_errors=None, pricing_shots=0, successes=None,
               total_shots=0, pricing_cx=0, total_cx=0,
               contains=None, erroneous=False, midpoint_error=None, allocation=None)
    if choice["selected"] is None:
        return row
    label = choice["selected"]
    e = next(e for e in encodings if e.name == label)
    p = profiles[label]
    f, g = SCENARIOS[scenario]
    # Evaluator-only truth; never passed into preselect/allocate.
    q = f + (1 - f - g) * p["amplitude"]
    key = ("allocation_v1", name, str(guard), scenario, arm, rep, label)
    m, n = 16384, 32768
    if arm == "pilot_cp":
        s_p = int(rng_for(*key, "pilot").binomial(1024, q))
        allocation = allocate(e, s_p, guard=guard)
        m, n = allocation["calibration_per_state"], allocation["pricing_shots"]
        row.update(pilot_shots=1024, pilot_successes=s_p, allocation=allocation)
    cal = rng_for(*key, "calibration").binomial(m, [f, g]).tolist()
    row.update(calibration_errors=cal, calibration_shots=2 * m,
               total_shots=row["pilot_shots"] + 2 * m)
    if arm == "single_hoeffding":
        rect = calibration_menu({label: cal}, m, guard)
        plan = plan_menu([e], rect, 1, {label: n}, m, 1)
        row["allocation"] = plan
        if plan["selected"] is None:
            return row
        n = plan["shots"]
    s = int(rng_for(*key, "validation").binomial(n, q))
    if arm == "single_hoeffding":
        interval = list(fixed_price_interval(e, rect[label], s, n))
        decision = dict(status="precision_met", interval=interval,
                        radius=(interval[1] - interval[0]) / 2)
    else:
        decision = cp_decision(e, s, n, cal, m, guard)
    interval = decision["interval"]
    c = by_id(name)
    truth = black_scholes_call(c.S0, c.K, c.r, c.sigma, c.T)
    error = None if interval is None else abs(sum(interval) / 2 - truth)
    cx = p["profiles"]["0"]["gates"]["cx"]
    row.update(**decision, pricing_shots=n, successes=s,
               total_shots=row["total_shots"] + n,
               pricing_cx=n * cx, total_cx=(row["pilot_shots"] + n) * cx,
               contains=None if interval is None else bool(interval[0] <= truth <= interval[1]),
               erroneous=bool(decision["status"] == "precision_met" and error > 1),
               midpoint_error=error)
    return row


def records(profiles):
    return [trial(name, profiles[name], guard, scenario, arm, rep)
            for name in C6 for guard in (0.0, 0.003, 0.03)
            for scenario in SCENARIOS for arm in ARMS for rep in range(30)]


def summarize(rows):
    cells, allocations = [], {}
    for row in rows:
        if row["arm"] == "pilot_cp":
            key = str(row["calibration_shots"] // 2)
            allocations[key] = allocations.get(key, 0) + 1
    for name in C6:
        for guard in (0.0, 0.003, 0.03):
            for scenario in SCENARIOS:
                for arm in ARMS:
                    group = [r for r in rows if (r["contract"], r["guard"],
                             r["scenario"], r["arm"]) == (name, guard, scenario, arm)]
                    cells.append(dict(contract=name, guard=guard, scenario=scenario, arm=arm,
                                      delivered=sum(r["status"] == "precision_met" for r in group),
                                      mean_total_shots=sum(r["total_shots"] for r in group) / 30))
    return dict(rows=len(rows), cells=cells, pilot_allocations=allocations,
                declarations={a: sum(r["status"] == "precision_met" for r in rows
                                     if r["arm"] == a) for a in ARMS},
                interval_misses=sum(r["contains"] is False for r in rows),
                erroneous_declarations=sum(r["erroneous"] for r in rows))


def verify(output):
    files = verify_inventory(output)
    plan = json.loads((output / "planned.json").read_text(encoding="utf-8"))
    for relative, digest in plan["config"]["replay_sources"].items():
        if sha256(ROOT / relative) != digest:
            raise ValueError("live replay source differs")
    rows = records(load_profiles(output / "input"))
    saved = json.loads((output / "records.json").read_text(encoding="utf-8"))
    if len(rows) != 3240 or saved != rows:
        raise ValueError("replay mismatch")
    if summarize(rows) != json.loads((output / "summary.json").read_text(encoding="utf-8")):
        raise ValueError("summary mismatch")
    for row in rows:
        if row["total_shots"] != sum(row[k] for k in
                                     ("pilot_shots", "calibration_shots", "pricing_shots")):
            raise ValueError("cost mismatch")
        if row["total_shots"] > 65536:
            raise ValueError("budget exceeded")
    return dict(verified=True, rows=len(rows), files=files)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.verify:
        print(json.dumps(verify(args.output)))
        return
    profiles = load_profiles(SOURCE)
    sources = list((ROOT / "research/journal_sprint").glob("*.py"))
    sources += list((ROOT / "research/paper_a").rglob("*.py")) + [PROTOCOL]
    hashes = {str(p.relative_to(ROOT)): sha256(p) for p in sources}
    output = start_run(args.output, dict(replay_sources=hashes, namespace="allocation_v1"))
    try:
        for p in sources:
            target = output / "source_snapshot" / p.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target)
            if sha256(target) != hashes[str(p.relative_to(ROOT))]:
                raise ValueError("source drift")
        (output / "input").mkdir()
        for p in [SOURCE / "complete.json"] + [SOURCE / f"profile_{c}.json" for c in C6]:
            shutil.copy2(p, output / "input" / p.name)
        if load_profiles(output / "input") != profiles:
            raise ValueError("input drift")
        rows = records(profiles)
        write_json(output / "records.json", rows)
        summary = summarize(rows)
        write_json(output / "summary.json", summary)
        finish_run(output)
        print(json.dumps({k: v for k, v in summary.items() if k != "cells"}))
    except Exception as error:
        write_json(output / "failure.json", dict(error=str(error)))
        raise


if __name__ == "__main__":
    main()
