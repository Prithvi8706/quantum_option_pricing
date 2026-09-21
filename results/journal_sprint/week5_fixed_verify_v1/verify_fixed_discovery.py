"""Reconstruct week-5 fixed-design records, diagnostic targets and cost ledgers."""

import argparse
from collections import Counter, defaultdict
from dataclasses import asdict
import json
from pathlib import Path
import shutil

import numpy as np

from .calibrated_readout import invert_calibrated
from .intervals import price_decision, response
from .run_fixed_discovery import (
    BUDGETS,
    CONDITIONS,
    COST_FIELDS,
    DESIGNS,
    checked_inputs,
    designs_for,
    summarize_cell,
)
from .storage import finish_run, rng_for, sha256, start_run, write_json
from .tighter_grid import tighter_bounds_for
from research.paper_a.benchmark import C6, by_id
from research.paper_a.payoff import a_calc
from research.paper_a.references import black_scholes_call, grid_points, grid_probabilities


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source", type=Path, default=Path("results/journal_sprint/week5_fixed_discovery_v1")
    )
    parser.add_argument("--output", default="results/journal_sprint/week5_fixed_verify_v1")
    args = parser.parse_args()
    source = args.source
    manifest = json.loads((source / "complete.json").read_text())
    for name, expected in manifest["sha256"].items():
        require(sha256(source / name) == expected, f"hash mismatch {name}")
    ledger, profiles, manifests = checked_inputs()
    planned = json.loads((source / "planned.json").read_text())["config"]
    require(planned["input_manifests"] == manifests, "input lineage")
    decisions = json.loads((source / "decisions.json").read_text())
    truths = json.loads((source / "diagnostic_truths.json").read_text())
    require(set(decisions) == set(C6), "decision contract set")
    for cid in C6:
        c = by_id(cid)
        bound, _ = tighter_bounds_for(c, 6, 0.125)
        d = decisions[cid]
        require(d["bounds"] == asdict(bound) and d["bound_total"] == bound.total, "bounds")
        require(d["refused"] == (bound.total >= 1), "refusal")
        if d["refused"]:
            require(d["designs"] == {} and cid not in truths, "refused target acquisition")
            continue
        a = a_calc(
            grid_probabilities(c, bound.lower, bound.upper, 6),
            grid_points(bound.lower, bound.upper, 6),
            c.K,
            bound.upper,
            0.125,
        )
        price = float(black_scholes_call(c.S0, c.K, c.r, c.sigma, c.T))
        require(truths[cid] == {"amplitude": a, "price": price}, "diagnostic target")
        require(
            d["designs"] == {str(b): designs_for(cid, b, ledger, profiles[cid]) for b in BUDGETS},
            "design decisions",
        )
    require(set(truths) == {cid for cid in C6 if not decisions[cid]["refused"]}, "truth keys")
    seen = set()
    totals = Counter()
    groups = defaultdict(list)
    for line in (source / "records.jsonl").read_text().splitlines():
        row = json.loads(line)
        cid, budget, condition, design, rep = (
            row[k] for k in ("contract", "budget", "condition", "design", "rep")
        )
        key = (cid, budget, condition, design, rep)
        require(key not in seen, "duplicate trial")
        seen.add(key)
        seed_key = ["week5_fixed", *key]
        require(row["seed_key"] == seed_key, "seed key")
        d = decisions[cid]
        if d["refused"]:
            require(row["status"] == "pre_refusal", "refusal state")
            require("counts" not in row and "calibration_errors" not in row, "refused observations")
            require(row["cost"] == {k: 0 for k in COST_FIELDS}, "refusal cost")
            totals["refused"] += 1
        else:
            totals["executed"] += 1
            fixed = d["designs"][str(budget)][design]
            depths, shots = fixed["depths"], fixed["shots"]
            require(row["depths"] == depths and row["shots"] == shots, "executed schedule")
            require(row["cost"] == fixed["cost"], "executed costs")
            target = truths[cid]
            f, g = (0.02, 0.07) if condition == "stationary" else (0.05, 0.04)
            errors = rng_for(*seed_key, "calibration").binomial(4096, [0.02, 0.07])
            counts = rng_for(*seed_key, "validation").binomial(
                shots, f + (1 - f - g) * response(target["amplitude"], depths)
            )
            require(np.array_equal(errors, row["calibration_errors"]), "calibration replay")
            require(np.array_equal(counts, row["counts"]), "validation replay")
            confidence, calibration = invert_calibrated(
                counts, shots, depths, errors, [4096] * 2, transfer_bounds=(0.03, 0.03)
            )
            require([list(c) for c in confidence.components] == row["components"], "components")
            require(calibration == row["calibration"], "calibration rectangle")
            b = d["bounds"]
            price_result = price_decision(
                confidence, b["sensitivity"], b["offset"], d["bound_total"], 1.0
            )
            require(
                json.loads(json.dumps(price_result)) == {k: row[k] for k in price_result},
                "price decision",
            )
            interval = price_result["interval"]
            contained = interval is not None and interval[0] <= target["price"] <= interval[1]
            false = (
                price_result["status"] == "precision_met"
                and abs(sum(interval) / 2 - target["price"]) > 1
            )
            require(
                row["amplitude_contains"] == confidence.contains(target["amplitude"]),
                "amplitude flag",
            )
            require(
                row["price_contains"] == contained and row["false_declaration"] == false,
                "price flags",
            )
        for field, value in row["cost"].items():
            if not field.startswith("max_"):
                totals[field] += value
        groups[(cid, budget, condition, design)].append(row)
    expected_keys = {
        (cid, b, c, s, r)
        for cid in C6
        for b in BUDGETS
        for c in CONDITIONS
        for s in DESIGNS
        for r in range(100)
    }
    require(seen == expected_keys, "full matrix")
    summary = json.loads((source / "summary.json").read_text())
    require(summary["attempts"] == 7200 and len(summary["cells"]) == 72, "summary dimensions")
    summary_keys = {
        (r["contract"], r["budget"], r["condition"], r["design"]) for r in summary["cells"]
    }
    require(summary_keys == set(groups), "summary uniqueness")
    for cell in summary["cells"]:
        k = tuple(cell[f] for f in ("contract", "budget", "condition", "design"))
        recomputed = summarize_cell(groups[k])
        require(recomputed == {f: cell[f] for f in recomputed}, "summary mismatch")
    output = start_run(args.output, {"source_manifest_sha256": sha256(source / "complete.json")})
    shutil.copy2(__file__, output / "verify_fixed_discovery.py")
    write_json(
        output / "verification.json",
        {
            "hashes": len(manifest["sha256"]),
            "attempts": len(seen),
            "cells": len(groups),
            "totals": dict(totals),
            "scope": "reconstruction with producing numerical helpers, not independent proof",
        },
    )
    finish_run(output)
    print(json.dumps(dict(totals)))


if __name__ == "__main__":
    main()
