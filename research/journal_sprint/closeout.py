"""Read-only verification and separately versioned week-1/2 analysis."""

import argparse
from collections import Counter, defaultdict
import csv
import json
import math
import shutil
import subprocess
import time

import numpy as np
from scipy.stats import beta

from .intervals import invert
from .storage import ROOT, finish_run, sha256, start_run, write_json
from .tighter_grid import tighter_bounds_for
from research.paper_a.benchmark import C6, by_id


def rate_interval(successes, trials):
    """Marginal exact binomial interval; never pool heterogeneous contracts."""
    if not trials:
        return None
    return [
        float(beta.ppf(0.025, successes, trials - successes + 1)) if successes else 0.0,
        float(beta.ppf(0.975, successes + 1, trials - successes)) if successes < trials else 1.0,
    ]


def summarize_cell(rows):
    executed = [r for r in rows if r["state"] != "pre_refusal"]
    nonempty = [r for r in executed if r["price_interval"] is not None]
    declarations = sum(r["declared"] for r in rows)
    false = sum(r["false_declaration"] for r in rows)
    contains = sum(r["price_contains"] for r in rows)
    return {
        "attempts": len(rows),
        "executed": len(executed),
        "nonempty": len(nonempty),
        "declarations": declarations,
        "false_declarations": false,
        "delivery_rate": declarations / len(rows),
        "price_contains_count": contains,
        "price_containment_among_executed": contains / len(executed) if executed else None,
        "price_containment_among_nonempty": contains / len(nonempty) if nonempty else None,
        "false_unconditional": false / len(rows),
        "false_among_declarations": false / declarations if declarations else None,
        "total_a_queries": sum(r["a_queries"] for r in rows),
        "total_shots": sum(r["total_shots"] for r in rows),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/journal_sprint/week12_closeout_v1")
    args = parser.parse_args()
    path = start_run(args.output, {"purpose": "post-experiment verification, not new trials"})
    shutil.copy2(__file__, path / "closeout.py")
    hashes = {}
    for name in ("price_intervals_v2c", "pricing_gate_v2b", "pricing_gate_v2a_retry1"):
        folder = ROOT / "results/journal_sprint" / name
        complete = json.loads((folder / "complete.json").read_text())
        for relative, expected in complete["sha256"].items():
            assert sha256(folder / relative) == expected, (name, relative)
        hashes[name] = {
            "artifacts_verified": len(complete["sha256"]),
            "manifest_sha256": sha256(folder / "complete.json"),
        }
    baseline = ROOT / "results/journal_sprint/pricing_gate_v2b/rows.json"
    models = json.loads(baseline.read_text())
    lookup = {(r["contract"], r["n"], r["scale"]): r for r in models}
    raw = ROOT / "results/journal_sprint/price_intervals_v2c/records.jsonl"
    rows = [json.loads(line) for line in raw.read_text().splitlines()]
    assert len(rows) == 43200
    keys = ("arm", "condition", "shots", "contract", "method")
    cells = defaultdict(list)
    identities = set()
    envelopes = {"ideal": (0, 0), "matched": (0.01, 0.01), "envelope": (0.005, 0.015)}
    start = time.perf_counter()
    for row in rows:
        key = tuple(row[k] for k in keys)
        identity = key + (row["rep"],)
        assert identity not in identities
        identities.add(identity)
        cells[key].append(row)
        if row["state"] == "pre_refusal":
            assert row["arm"] == "selected" and row["contract"] in ("E030", "E038")
            assert not row["counts"] and row["a_queries"] == row["total_shots"] == 0
            assert not row["declared"] and not row["false_declaration"]
            continue
        model = lookup[(row["contract"],) + tuple(row["representation"])]
        multi = row["method"] == "multidepth"
        depths = [0, 1, 2, 4, 8] if multi else [0]
        shots = [row["shots"]] * 5 if multi else [35 * row["shots"]]
        assert len(shots) == len(row["counts"])
        assert all(isinstance(c, int) and 0 <= c <= n for c, n in zip(row["counts"], shots))
        assert row["a_queries"] == sum(n * (2 * k + 1) for n, k in zip(shots, depths))
        assert row["grover_queries"] == sum(n * k for n, k in zip(shots, depths))
        assert row["total_shots"] == sum(shots)
        conf = invert(row["counts"], shots, depths, envelopes[row["condition"]])
        assert [list(c) for c in conf.components] == row["probability_components"]
        assert conf.contains(model["diagnostic"]["probability"]) == row["probability_contains"]
        if not conf.components:
            assert row["state"] == "incompatible" and not row["declared"]
            assert row["price_interval"] is None
            continue
        bound = model["total_bound"]
        L = model["bounds"]["sensitivity"]
        offset = model["bounds"]["offset"]
        expected = [L * conf.hull[0] + offset - bound, L * conf.hull[1] + offset + bound]
        assert np.allclose(row["price_interval"], expected, rtol=0, atol=1e-10)
        radius = (expected[1] - expected[0]) / 2
        assert math.isclose(row["radius"], radius, abs_tol=1e-10)
        assert row["declared"] == (radius <= 1)
        price = model["diagnostic"]["black_scholes"]
        assert row["price_contains"] == (expected[0] <= price <= expected[1])
        assert row["false_declaration"] == (row["declared"] and abs(sum(expected) / 2 - price) > 1)
    assert len(cells) == 216 and all(len(c) == 200 for c in cells.values())
    output = []
    pooled = defaultdict(list)
    for key, records in sorted(cells.items()):
        summary = dict(zip(keys, key))
        summary.update(summarize_cell(records))
        summary["delivery_marginal_cp95"] = rate_interval(summary["declarations"], 200)
        summary["false_marginal_cp95"] = rate_interval(summary["false_declarations"], 200)
        summary["false_given_declaration_marginal_cp95"] = rate_interval(
            summary["false_declarations"], summary["declarations"]
        )
        output.append(summary)
        pooled[(key[0], key[1], key[2], key[4])].extend(records)
    write_json(path / "cells.json", output)
    pooled_rows = []
    for key, records in sorted(pooled.items()):
        item = dict(zip(("arm", "condition", "shots", "method"), key))
        item.update(summarize_cell(records))
        pooled_rows.append(item)
    write_json(path / "pooled.json", pooled_rows)
    with (path / "pooled.csv").open("x", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(pooled_rows[0]))
        writer.writeheader()
        writer.writerows(pooled_rows)
    construction = []
    for repetition in range(5):
        tick = time.perf_counter()
        for model in models:
            bounds, _ = tighter_bounds_for(by_id(model["contract"]), model["n"], model["scale"])
            assert math.isclose(bounds.total, model["total_bound"], rel_tol=1e-12)
        construction.append(time.perf_counter() - tick)
    write_json(
        path / "verification.json",
        {
            "input_hashes": hashes,
            "raw_sha256": sha256(raw),
            "rows": len(rows),
            "cells": len(cells),
            "states": dict(Counter(r["state"] for r in rows)),
            "reinversion_and_analysis_seconds": time.perf_counter() - start,
            "bound_construction_72_candidates_seconds": construction,
            "timing_note": "Post-run CPU only; excludes circuit setup and quantum runtime",
            "all_checks_pass": True,
        },
    )
    commands = [
        ["git", "log", "--all", "--oneline", "--", "src/plot_dimension_sweep.py"],
        [
            "git",
            "log",
            "--all",
            "--name-only",
            "--format=",
            "--",
            "data",
            "results",
            "outputs",
            "figures",
            "src",
            "research",
        ],
    ]
    evidence = []
    for command in commands:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=True)
        lines = sorted(set(result.stdout.splitlines()))
        if "--name-only" in command:
            lines = [
                line
                for line in lines
                if any(
                    s in line.lower()
                    for s in ("dimension", "sweep", "trial", "rqmc", ".npz", ".csv")
                )
            ]
        evidence.append({"command": command, "output": lines})
    write_json(path / "paper_b_git_search.json", evidence)
    finish_run(path)
    print(json.dumps({"verified": len(rows), "path": str(path), "contracts": list(C6)}))


if __name__ == "__main__":
    main()
