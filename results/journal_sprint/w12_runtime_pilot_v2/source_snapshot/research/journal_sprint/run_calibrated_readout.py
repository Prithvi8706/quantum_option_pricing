"""Week-4 finite-calibration discovery; raw observations shared across analyses."""

import argparse
from collections import defaultdict
import json
import os
import shutil

import numpy as np

from .calibrated_readout import invert_calibrated
from .intervals import response
from .readout_stress import invert_readout, readout_probability
from .storage import ROOT, finish_run, rng_for, start_run, write_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/journal_sprint/week4_calibration_v1")
    args = parser.parse_args()
    config = {
        "amplitudes": [0.1, 0.4, 0.8],
        "calibration_shots_per_state": [256, 4096],
        "validation_shots_per_depth": 1024,
        "depths": [0, 1, 2],
        "repetitions": 200,
        "false_positive": 0.02,
        "false_negative": 0.07,
        "protocol": "PROTOCOL_W4_CALIBRATION",
        "alpha_calibration": 0.025,
        "alpha_validation": 0.025,
    }
    path = start_run(args.output, config)
    sources = list((ROOT / "research/journal_sprint").rglob("*.py"))
    sources.append(ROOT / "docs/journal_sprint/PROTOCOL_W4_CALIBRATION.md")
    for source in sources:
        target = path / "source_snapshot" / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    groups = defaultdict(list)
    datasets = 0
    try:
        with (path / "records.jsonl").open("x", encoding="utf-8") as stream:
            for a in config["amplitudes"]:
                reported = readout_probability(response(a, config["depths"]), 0.02, 0.07)
                for ncal in config["calibration_shots_per_state"]:
                    for rep in range(config["repetitions"]):
                        key = ("week4_calibration", a, ncal, rep)
                        errors = rng_for(*key, "calibration").binomial(ncal, [0.02, 0.07])
                        counts = rng_for(*key, "validation").binomial(1024, reported)
                        uncertain, calibration = invert_calibrated(
                            counts, [1024] * 3, [0, 1, 2], errors, [ncal] * 2
                        )
                        fhat, ghat = errors / ncal
                        # The declared matrix has low rates; preserve unexpected
                        # unusable plug-in contrast rather than silently skipping.
                        plugin = (
                            invert_readout(counts, [1024] * 3, [0, 1, 2], fhat, ghat)
                            if fhat + ghat < 1
                            else None
                        )
                        known = invert_readout(counts, [1024] * 3, [0, 1, 2], 0.02, 0.07)
                        analyses = {}
                        for method, result in (
                            ("known_oracle", known),
                            ("plugin", plugin),
                            ("finite_calibration", uncertain),
                        ):
                            analyses[method] = {
                                "components": result.components if result else None,
                                "contains": result.contains(a) if result else False,
                                "radius": result.radius if result else None,
                                "unavailable": result is None,
                            }
                            groups[(a, ncal, method)].append(analyses[method])
                        row = {
                            "seed_key": key,
                            "amplitude": a,
                            "calibration_n": ncal,
                            "rep": rep,
                            "calibration_errors": errors.tolist(),
                            "counts": counts.tolist(),
                            "calibration": calibration,
                            "analyses": analyses,
                            "validation_shots": 3072,
                            "validation_A_equivalents": 9216,
                            "calibration_shots": 2 * ncal,
                            "total_shots": 3072 + 2 * ncal,
                        }
                        stream.write(json.dumps(row, allow_nan=False) + "\n")
                        datasets += 1
                    stream.flush()
                    os.fsync(stream.fileno())
                    print(f"a={a}, calibration/state={ncal}: completed", flush=True)
        summary = []
        for (a, ncal, method), rows in sorted(groups.items()):
            radii = [r["radius"] for r in rows if r["radius"] is not None]
            summary.append(
                {
                    "amplitude": a,
                    "calibration_n": ncal,
                    "method": method,
                    "trials": len(rows),
                    "contained": sum(r["contains"] for r in rows),
                    "incompatible": sum(r["components"] == () for r in rows),
                    "unavailable": sum(r["unavailable"] for r in rows),
                    "median_radius_nonempty": float(np.median(radii)) if radii else None,
                }
            )
        write_json(
            path / "summary.json",
            {
                "datasets": datasets,
                "inferences": datasets * 3,
                "cells": summary,
                "scope": "stationary, perfect calibration preparations",
            },
        )
        finish_run(path)
    except Exception as error:
        write_json(path / "failure.json", {"completed_datasets": datasets, "error": str(error)})
        raise


if __name__ == "__main__":
    main()
