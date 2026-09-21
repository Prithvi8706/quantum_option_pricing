"""Verify and summarize archived classical and resource discovery results."""

import argparse
from collections import defaultdict
import json

import numpy as np

from .storage import ROOT, finish_run, sha256, start_run, write_json
from .run_comparator import validate_golden


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/journal_sprint/week3_summary_v1")
    args = parser.parse_args()
    base = ROOT / "results/journal_sprint"
    runs = [
        "week3_classical_v1",
        "week3_resources_v1",
        "week3_stress_v1",
        "week3_circuits_v1_retry1",
        "comparator_v1",
    ]
    verified = {}
    for name in runs:
        manifest = json.loads((base / name / "complete.json").read_text())
        for relative, expected in manifest["sha256"].items():
            if sha256(base / name / relative) != expected:
                raise RuntimeError(f"hash mismatch {name}/{relative}")
        verified[name] = len(manifest["sha256"])
    validate_golden(json.loads((base / "comparator_v1/summary.json").read_text()))
    rows = json.loads((base / "week3_classical_v1/rows.json").read_text())
    keys = {(r["contract"], r["method"], r["paths"], r["rep"]) for r in rows}
    if len(rows) != 480 or len(keys) != 480:
        raise RuntimeError("classical matrix incomplete or duplicated")
    grouped = defaultdict(list)
    for r in rows:
        if r["total_paths"] != r["paths"] + r["pilot_paths"]:
            raise RuntimeError("path cost mismatch")
        if r["scramble_means"] is not None:
            se = np.std(r["scramble_means"], ddof=1) / np.sqrt(32)
            if not np.isclose(se, r["se"], rtol=1e-12, atol=1e-15):
                raise RuntimeError("scramble standard error mismatch")
        grouped[(r["contract"], r["method"], r["paths"])].append(r)
    summaries = []
    for (cid, method, paths), group in sorted(grouped.items()):
        summaries.append(
            {
                "contract": cid,
                "method": method,
                "evaluation_paths": paths,
                "total_paths_per_trial": group[0]["total_paths"],
                "rms_reference_deviation": float(
                    np.sqrt(np.mean([r["reference_deviation"] ** 2 for r in group]))
                ),
                "mean_seconds": float(np.mean([r["seconds"] for r in group])),
            }
        )
    resource = json.loads((base / "week3_resources_v1/summary.json").read_text())
    path = start_run(args.output, {"purpose": "descriptive post-run summary", "runs": runs})
    write_json(
        path / "summary.json",
        {
            "verified_hashes": verified,
            "classical": summaries,
            "total_trial_paths": sum(r["total_paths"] for r in rows),
            "resource_cases": len(resource["rows"]),
            "max_ideal_difference": max(r["absolute_difference"] for r in resource["rows"]),
            "resource_seconds": resource["seconds"],
            "decision": "hold confirmation: model, selective-risk and review gates remain open",
        },
    )
    finish_run(path)
    print(
        json.dumps(
            {
                "verified": verified,
                "classical_larger_budget": [r for r in summaries if r["evaluation_paths"] == 16384],
                "resource_seconds": resource["seconds"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
