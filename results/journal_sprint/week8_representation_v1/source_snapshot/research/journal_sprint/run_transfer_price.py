"""Fixed-design discovery of calibration transfer and delivered dollar precision."""

import argparse
from collections import defaultdict
from dataclasses import asdict
import json
import os
import shutil
import time

import numpy as np

from .calibrated_readout import invert_calibrated
from .intervals import price_decision, response
from .storage import ROOT, finish_run, rng_for, start_run, write_json
from .tighter_grid import tighter_bounds_for
from research.paper_a.benchmark import C6, by_id
from research.paper_a.payoff import a_calc
from research.paper_a.references import black_scholes_call, grid_points, grid_probabilities


CONDITIONS = (
    "stationary",
    "constant_transfer",
    "depth_transfer",
    "imperfect_preparation",
    "outside_bound",
)


def rates(condition):
    calibration = np.array([0.02, 0.07])
    f, g = np.full(3, 0.02), np.full(3, 0.07)
    if condition == "constant_transfer":
        f += 0.03
        g -= 0.03
    elif condition == "depth_transfer":
        f += [0, 0.015, 0.03]
        g -= [0, 0.015, 0.03]
    elif condition == "imperfect_preparation":
        calibration += 0.02 * (1 - 0.02 - 0.07)
    elif condition == "outside_bound":
        f += 0.08
    elif condition != "stationary":
        raise ValueError("unknown transfer condition")
    return calibration, f, g


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/journal_sprint/week4_transfer_price_v1")
    args = parser.parse_args()
    config = {
        "protocol": "PROTOCOL_W4_TRANSFER_PRICE",
        "contracts": list(C6),
        "n": 6,
        "scale": 0.125,
        "tolerance": 1.0,
        "depths": [0, 1, 2],
        "validation_shots": 32768,
        "calibration_shots": 4096,
        "repetitions": 200,
        "conditions": CONDITIONS,
        "alpha_calibration": 0.025,
        "alpha_validation": 0.025,
        "transfer_bounds": {"unexpanded": [0.0, 0.0], "guarded": [0.03, 0.03]},
    }
    path = start_run(args.output, config)
    sources = list((ROOT / "research/journal_sprint").rglob("*.py"))
    sources += list((ROOT / "research/paper_a").glob("*.py"))
    sources.append(ROOT / "docs/journal_sprint/PROTOCOL_W4_TRANSFER_PRICE.md")
    for source in sources:
        destination = path / "source_snapshot" / source.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    prepared = {}
    attempts = 0
    groups = defaultdict(list)
    try:
        for cid in C6:
            tick = time.perf_counter()
            bound, _ = tighter_bounds_for(by_id(cid), 6, 0.125)
            prepared[cid] = {
                "bounds": {k: float(v) for k, v in asdict(bound).items()},
                "bound_total": float(bound.total),
                "refused": bound.total >= 1,
                "setup_seconds": time.perf_counter() - tick,
            }
        write_json(path / "decisions.json", prepared)
        # Fixed bound decisions are recorded before truth evaluation or acquisition.
        truths = {}
        for cid in C6:
            if prepared[cid]["refused"]:
                continue
            c = by_id(cid)
            b = prepared[cid]["bounds"]
            amplitude = a_calc(
                grid_probabilities(c, b["lower"], b["upper"], 6),
                grid_points(b["lower"], b["upper"], 6),
                c.K,
                b["upper"],
                0.125,
            )
            truths[cid] = {
                "amplitude": amplitude,
                "price": float(black_scholes_call(c.S0, c.K, c.r, c.sigma, c.T)),
            }
        write_json(path / "diagnostic_truths.json", truths)
        with (path / "records.jsonl").open("x", encoding="utf-8") as stream:
            for cid in C6:
                for condition in CONDITIONS:
                    calrates, f, g = rates(condition)
                    for rep in range(200):
                        key = ("week4_transfer_price", cid, condition, rep)
                        row = {
                            "seed_key": key,
                            "contract": cid,
                            "condition": condition,
                            "rep": rep,
                            "analyses": {},
                            "validation_shots": 0,
                            "validation_A_equivalents": 0,
                            "calibration_shots": 0,
                            "total_shots": 0,
                        }
                        if prepared[cid]["refused"]:
                            for method in config["transfer_bounds"]:
                                row["analyses"][method] = {"status": "pre_refusal"}
                        else:
                            truth = truths[cid]
                            p = response(truth["amplitude"], [0, 1, 2])
                            errors = rng_for(*key, "calibration").binomial(4096, calrates)
                            counts = rng_for(*key, "validation").binomial(
                                32768, f + (1 - f - g) * p
                            )
                            row.update(
                                calibration_errors=errors.tolist(),
                                counts=counts.tolist(),
                                validation_shots=98304,
                                validation_A_equivalents=294912,
                                calibration_shots=8192,
                                total_shots=106496,
                            )
                            b = prepared[cid]["bounds"]
                            for method, transfer in config["transfer_bounds"].items():
                                confidence, calibration = invert_calibrated(
                                    counts,
                                    [32768] * 3,
                                    [0, 1, 2],
                                    errors,
                                    [4096] * 2,
                                    transfer_bounds=transfer,
                                )
                                decision = price_decision(
                                    confidence,
                                    b["sensitivity"],
                                    b["offset"],
                                    prepared[cid]["bound_total"],
                                    1.0,
                                )
                                interval = decision["interval"]
                                declared = decision["status"] == "precision_met"
                                row["analyses"][method] = {
                                    **decision,
                                    "components": confidence.components,
                                    "calibration": calibration,
                                    "amplitude_contains": confidence.contains(truth["amplitude"]),
                                    "price_contains": bool(
                                        interval is not None
                                        and interval[0] <= truth["price"] <= interval[1]
                                    ),
                                    "false_declaration": bool(
                                        declared and abs(sum(interval) / 2 - truth["price"]) > 1
                                    ),
                                }
                        stream.write(json.dumps(row, allow_nan=False) + "\n")
                        attempts += 1
                        for method, analysis in row["analyses"].items():
                            groups[(cid, condition, method)].append(analysis)
                    stream.flush()
                    os.fsync(stream.fileno())
                print(cid, "completed", flush=True)
        summary = []
        for (cid, condition, method), rows in sorted(groups.items()):
            executed = sum(r["status"] != "pre_refusal" for r in rows)
            declared = sum(r["status"] == "precision_met" for r in rows)
            false = sum(r.get("false_declaration", False) for r in rows)
            summary.append(
                {
                    "contract": cid,
                    "condition": condition,
                    "method": method,
                    "attempts": len(rows),
                    "executed": executed,
                    "declared": declared,
                    "incompatible": sum(r["status"] == "incompatible" for r in rows),
                    "amplitude_contained": sum(r.get("amplitude_contains", False) for r in rows),
                    "price_contained": sum(r.get("price_contains", False) for r in rows),
                    "false_declarations": false,
                    "false_per_attempt": false / len(rows),
                    "false_per_executed": false / executed if executed else None,
                    "false_given_declaration": false / declared if declared else None,
                }
            )
        write_json(path / "summary.json", {"attempts": attempts, "cells": summary})
        finish_run(path)
    except Exception as error:
        write_json(path / "failure.json", {"completed_attempts": attempts, "error": str(error)})
        raise


if __name__ == "__main__":
    main()
