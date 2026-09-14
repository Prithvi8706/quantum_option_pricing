"""V2C fixed and bound-selected finite-shot dollar intervals."""

from .checks import require

import argparse
import json
import os
import shutil
import time

import numpy as np

from .intervals import invert, price_decision, response
from .storage import ROOT, finish_run, rng_for, sha256, start_run, write_json
from research.paper_a.benchmark import C6

CONDITIONS = {
    "ideal": (0.0, (0.0, 0.0)),
    "matched": (0.01, (0.01, 0.01)),
    "envelope": (0.01, (0.005, 0.015)),
}
DEPTHS = [0, 1, 2, 4, 8]


def select_representation(candidates):
    """Only these four numeric fields are accepted; no diagnostic/truth fields."""
    choices = []
    for row in candidates:
        if set(row) != {"n", "scale", "bias_bound", "sensitivity"}:
            raise ValueError("Selector accepts only representation and bound inputs")
        budget = (1 - row["bias_bound"]) / row["sensitivity"]
        if budget > 0:
            choices.append((budget, -row["n"], -row["scale"], row))
    return max(choices, key=lambda item: item[:3])[3] if choices else None


def summarize(rows):
    n = len(rows)
    declarations = [r for r in rows if r["declared"]]
    return {
        "trials": n,
        "declared_rate": sum(r["declared"] for r in rows) / n,
        "refused_rate": sum(r["state"] == "pre_refusal" for r in rows) / n,
        "incompatible_rate": sum(r["state"] == "incompatible" for r in rows) / n,
        "price_containment_rate": sum(r["price_contains"] for r in rows) / n,
        "probability_containment_rate": sum(r["probability_contains"] for r in rows) / n,
        "false_declaration_rate": sum(r["false_declaration"] for r in rows) / n,
        "false_given_declaration": (
            sum(r["false_declaration"] for r in declarations) / len(declarations)
            if declarations
            else None
        ),
        "mean_a_equivalent_queries": float(np.mean([r["a_queries"] for r in rows])),
        "median_price_radius_nonempty": float(
            np.median([r["radius"] for r in rows if r["radius"] is not None])
        )
        if any(r["radius"] is not None for r in rows)
        else None,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/journal_sprint/price_intervals_v2c")
    args = parser.parse_args()
    baseline = ROOT / "results/journal_sprint/pricing_gate_v2b"
    original = json.loads((baseline / "rows.json").read_text())
    manifest = json.loads((baseline / "complete.json").read_text())
    require(all(sha256(baseline / name) == value for name, value in manifest["sha256"].items()))
    started = time.perf_counter()
    choices = {}
    for cid in C6:
        group = [r for r in original if r["contract"] == cid]
        allowed = [
            {
                "n": r["n"],
                "scale": r["scale"],
                "bias_bound": r["total_bound"],
                "sensitivity": r["bounds"]["sensitivity"],
            }
            for r in group
        ]
        chosen = select_representation(allowed)
        choices[cid] = {
            "fixed": (6, 0.125),
            "selected": (chosen["n"], chosen["scale"]) if chosen else None,
        }
    selection_seconds = time.perf_counter() - started
    lookup = {(r["contract"], r["n"], r["scale"]): r for r in original}
    path = start_run(
        args.output,
        {
            "protocol": "PROTOCOL_V2C",
            "contracts": C6,
            "shots": [512, 8192, 32768],
            "reps": 200,
            "conditions": CONDITIONS,
            "choices": choices,
            "baseline_sha256": sha256(baseline / "rows.json"),
            "cached_bound_selection_seconds": selection_seconds,
        },
    )
    sources = list((ROOT / "research/journal_sprint").rglob("*.py"))
    sources += [
        ROOT / "docs/journal_sprint/PROTOCOL_V2C.md",
        ROOT / "research/paper_a/benchmark.py",
    ]
    for source in sources:
        destination = path / "source_snapshot" / source.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    summaries = []
    simulation_start = time.perf_counter()
    with (path / "records.jsonl").open("x", encoding="utf-8") as stream:
        for arm in ("fixed", "selected"):
            for condition, (eta, envelope) in CONDITIONS.items():
                for shots in (512, 8192, 32768):
                    pooled = {"multidepth": [], "direct": []}
                    for cid in C6:
                        choice = choices[cid][arm]
                        model = lookup[(cid,) + tuple(choice)] if choice else None
                        cell = {"multidepth": [], "direct": []}
                        for rep in range(200):
                            for method in ("multidepth", "direct"):
                                row = {
                                    "arm": arm,
                                    "condition": condition,
                                    "shots": shots,
                                    "contract": cid,
                                    "rep": rep,
                                    "method": method,
                                    "representation": choice,
                                }
                                if model is None:
                                    row.update(
                                        state="pre_refusal",
                                        counts=[],
                                        declared=False,
                                        price_contains=False,
                                        probability_contains=False,
                                        false_declaration=False,
                                        radius=None,
                                        a_queries=0,
                                        grover_queries=0,
                                        total_shots=0,
                                    )
                                else:
                                    truth = model["diagnostic"]
                                    depths = DEPTHS if method == "multidepth" else [0]
                                    shot_vector = (
                                        [shots] * 5 if method == "multidepth" else [35 * shots]
                                    )
                                    counts = rng_for(
                                        "v2c", cid, arm, condition, shots, rep, method
                                    ).binomial(
                                        shot_vector, response(truth["probability"], depths, eta)
                                    )
                                    confidence = invert(counts, shot_vector, depths, envelope)
                                    decision = price_decision(
                                        confidence,
                                        model["bounds"]["sensitivity"],
                                        offset=model["bounds"]["offset"],
                                        bias_bound=model["total_bound"],
                                        tolerance=1.0,
                                    )
                                    interval = decision["interval"]
                                    declared = decision["status"] == "precision_met"
                                    error = (
                                        abs(sum(interval) / 2 - truth["black_scholes"])
                                        if interval
                                        else None
                                    )
                                    row.update(
                                        state=decision["status"],
                                        counts=counts.tolist(),
                                        declared=declared,
                                        price_interval=interval,
                                        probability_components=confidence.components,
                                        price_contains=bool(
                                            interval
                                            and interval[0] <= truth["black_scholes"] <= interval[1]
                                        ),
                                        probability_contains=confidence.contains(
                                            truth["probability"]
                                        ),
                                        false_declaration=bool(declared and error > 1),
                                        radius=decision["radius"],
                                        absolute_price_error=error,
                                        a_queries=35 * shots,
                                        grover_queries=15 * shots if method == "multidepth" else 0,
                                        total_shots=sum(shot_vector),
                                    )
                                stream.write(json.dumps(row, allow_nan=False) + "\n")
                                cell[method].append(row)
                        for method, records in cell.items():
                            summaries.append(
                                {
                                    "arm": arm,
                                    "condition": condition,
                                    "shots": shots,
                                    "contract": cid,
                                    "method": method,
                                    **summarize(records),
                                }
                            )
                            pooled[method].extend(records)
                        stream.flush()
                        os.fsync(stream.fileno())
                    for method, records in pooled.items():
                        summary = {
                            "arm": arm,
                            "condition": condition,
                            "shots": shots,
                            "contract": "pooled_C6",
                            "method": method,
                            **summarize(records),
                        }
                        summaries.append(summary)
                        print(summary, flush=True)
                    if time.perf_counter() - simulation_start > 3600:
                        raise TimeoutError("Prospective simulation time limit")
    write_json(path / "summary.json", summaries)
    write_json(
        path / "timing.json",
        {
            "simulation_seconds": time.perf_counter() - simulation_start,
            "selection_seconds": selection_seconds,
            "warning": "Selection uses cached bounds; bound construction not free",
        },
    )
    finish_run(path)


if __name__ == "__main__":
    main()
