"""Fresh synthetic check of a fixed calibration-first decision rule."""

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import shutil

from .encoding_decision import Encoding, calibration_menu, fixed_price_interval, plan_menu
from .storage import ROOT, finish_run, rng_for, sha256, start_run, write_json
from research.paper_a.benchmark import C6, by_id
from research.paper_a.references import black_scholes_call


PROTOCOL = ROOT / "docs/journal_sprint/PROTOCOL_ENCODING_DECISION_V1.md"
SOURCE = ROOT / "results/journal_sprint/rescue_encoding_v2"


def load_profiles(source):
    manifest = json.loads((source / "complete.json").read_text(encoding="utf-8"))["sha256"]
    profiles = {}
    for name in C6:
        path = source / f"profile_{name}.json"
        if sha256(path) != manifest[path.name]:
            raise ValueError("profile hash mismatch")
        profiles[name] = json.loads(path.read_text(encoding="utf-8"))
    return profiles


def trial(name, profiles, guard, axis, rep):
    key = ("encoding_decision_v1", name, str(guard), axis, rep)
    encodings, errors, caps = [], {}, {}
    old_cx = profiles["linearized"]["profiles"]["0"]["gates"]["cx"]
    for encoding in ("linearized", "exact_table"):
        p = profiles[encoding]
        b = p["bounds"]
        cx = p["profiles"]["0"]["gates"]["cx"]
        encodings.append(Encoding(
            encoding, b["sensitivity"], b["offset"],
            b["support"] + b["grid"] + b["encoding"], 1 if axis == "shots" else cx,
        ))
        errors[encoding] = rng_for(*key, encoding, "calibration").binomial(
            16384, [0.02, 0.07]
        ).tolist()
        caps[encoding] = 32768 if axis == "shots" else (32768 * old_cx) // cx
    rectangles = calibration_menu(errors, 16384, guard)
    plan = plan_menu(encodings, rectangles, 1.0, caps, 16384, 1 if axis == "shots" else 0)
    row = dict(
        contract=name, guard=guard, axis=axis, rep=rep, plan=plan,
        calibration_errors=errors, rectangles={k: asdict(v) for k, v in rectangles.items()},
        status="not_certified", successes=None, interval=None, contains=None,
        erroneous=False, midpoint_error=None, pricing_cx=0,
    )
    if plan["selected"] is not None:
        chosen = plan["selected"]
        e = next(e for e in encodings if e.name == chosen)
        # Truth/amplitude cross the evaluator boundary only AFTER plan creation.
        q = 0.02 + 0.91 * profiles[chosen]["amplitude"]
        count = int(rng_for(*key, chosen, "validation").binomial(plan["shots"], q))
        interval = fixed_price_interval(e, rectangles[chosen], count, plan["shots"])
        c = by_id(name)
        truth = black_scholes_call(c.S0, c.K, c.r, c.sigma, c.T)
        error = abs(sum(interval) / 2 - truth)
        row.update(
            status="precision_met", successes=count, interval=list(interval),
            contains=bool(interval[0] <= truth <= interval[1]),
            erroneous=bool(error > 1), midpoint_error=error,
            pricing_cx=plan["shots"] * profiles[chosen]["profiles"]["0"]["gates"]["cx"],
        )
    return row


def records(profiles):
    return [
        trial(name, profiles[name], guard, axis, rep)
        for name in C6 for guard in (0.0, 0.003, 0.03)
        for axis in ("shots", "cx") for rep in range(30)
    ]


def summarize(rows):
    cells = []
    for name in C6:
        for guard in (0.0, 0.003, 0.03):
            for axis in ("shots", "cx"):
                group = [r for r in rows if (r["contract"], r["guard"], r["axis"])
                         == (name, guard, axis)]
                cells.append(dict(
                    contract=name, guard=guard, axis=axis, attempts=len(group),
                    delivered=sum(r["status"] == "precision_met" for r in group),
                    mean_pricing_shots=sum(r["plan"]["shots"] for r in group) / len(group),
                    mean_total_shots=sum(r["plan"]["total_shots"] for r in group) / len(group),
                ))
    reasons = {}
    selected = {}
    for row in rows:
        key = row["plan"]["selected"] or "none"
        selected[key] = selected.get(key, 0) + 1
        for score in row["plan"]["scores"]:
            key = score["encoding"] + ":" + score["status"]
            reasons[key] = reasons.get(key, 0) + 1
    return dict(
        rows=len(rows), selected=selected, candidate_statuses=reasons,
        declared=sum(r["status"] == "precision_met" for r in rows),
        interval_misses=sum(r["contains"] is False for r in rows),
        erroneous_declarations=sum(r["erroneous"] for r in rows), cells=cells,
        scope="fresh synthetic draws, known contracts, k=0; no advantage claim",
    )


def verify_inventory(output):
    complete = json.loads((output / "complete.json").read_text(encoding="utf-8"))["sha256"]
    actual = {str(p.relative_to(output)) for p in output.rglob("*")
              if p.is_file() and p != output / "complete.json"}
    if actual != set(complete):
        raise ValueError("archive inventory mismatch")
    for relative, digest in complete.items():
        path = (output / relative).resolve()
        if output.resolve() not in path.parents or sha256(path) != digest:
            raise ValueError("archive hash/path mismatch")
    return len(complete)


def verify(output):
    files = verify_inventory(output)
    planned = json.loads((output / "planned.json").read_text(encoding="utf-8"))
    for relative, digest in planned["config"]["replay_sources"].items():
        if sha256(ROOT / relative) != digest:
            raise ValueError("live replay source differs from frozen source")
    profiles = load_profiles(output / "input")
    rows = records(profiles)
    saved = json.loads((output / "records.json").read_text(encoding="utf-8"))
    summary = json.loads((output / "summary.json").read_text(encoding="utf-8"))
    if rows != saved or summarize(rows) != summary or len(rows) != 1080:
        raise ValueError("deterministic replay mismatch")
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
    output = start_run(args.output, dict(protocol=str(PROTOCOL.relative_to(ROOT)),
                                       replay_sources=hashes, namespace="encoding_decision_v1"))
    try:
        for p in sources:
            target = output / "source_snapshot" / p.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target)
            if sha256(target) != hashes[str(p.relative_to(ROOT))]:
                raise ValueError("source changed during snapshot")
        (output / "input").mkdir()
        for p in [SOURCE / "complete.json"] + [SOURCE / f"profile_{c}.json" for c in C6]:
            shutil.copy2(p, output / "input" / p.name)
        if load_profiles(output / "input") != profiles:
            raise ValueError("input changed during snapshot")
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
