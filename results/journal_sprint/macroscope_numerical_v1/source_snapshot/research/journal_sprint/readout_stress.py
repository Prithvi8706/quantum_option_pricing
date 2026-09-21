"""Declared response-level readout/dependence stress, using saved circuit targets."""

from .checks import require

import argparse
import json
import os
import shutil
from collections import defaultdict

import numpy as np

from .intervals import ConfidenceSet, ROUNDING, clopper_pearson, intersect, invert, sine_preimage
from .storage import ROOT, finish_run, rng_for, sha256, start_run, write_json


def readout_probability(probability, false_positive, false_negative):
    if not 0 <= false_positive < 1 or not 0 <= false_negative < 1:
        raise ValueError("invalid readout errors")
    if false_positive + false_negative >= 1:
        raise ValueError("this correction requires positive readout contrast")
    return false_positive + (1 - false_positive - false_negative) * np.asarray(probability)


def invert_readout(counts, shots, depths, false_positive, false_negative, alpha=0.05):
    readout_probability(0, false_positive, false_negative)
    if len(counts) != len(depths) or not len(depths):
        raise ValueError("depths must match counts")
    if not 0 < alpha < 1:
        raise ValueError("invalid alpha")
    lo, hi = clopper_pearson(counts, shots, alpha / len(depths))
    contrast = 1 - false_positive - false_negative
    result = [(0, np.pi / 2)]
    for lower, upper, depth in zip(lo, hi, depths):
        lower = max(0, (lower - ROUNDING - false_positive) / contrast)
        upper = min(1, (upper + ROUNDING - false_positive) / contrast)
        if lower > upper:
            return ConfidenceSet((), alpha)
        result = intersect(result, sine_preimage(lower, upper, depth))
    return ConfidenceSet(
        tuple(
            (max(0, float(np.sin(a) ** 2) - ROUNDING), min(1, float(np.sin(b) ** 2) + ROUNDING))
            for a, b in result
        ),
        alpha,
    )


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/journal_sprint/week3_stress_v1")
    parser.add_argument("--baseline", default="results/journal_sprint/week3_circuits_v1_retry1")
    args = parser.parse_args(argv)
    baseline = ROOT / args.baseline
    manifest = json.loads((baseline / "complete.json").read_text())
    require(all(sha256(baseline / name) == value for name, value in manifest["sha256"].items()))
    groups = defaultdict(list)
    for row in json.loads((baseline / "summary.json").read_text())["rows"]:
        if row["n"] == 3:
            groups[(row["contract"], row["scale"])].append(row)
    path = start_run(
        args.output,
        {
            "protocol": "PROTOCOL_W3_STRESS",
            "repetitions": 500,
            "shots_per_depth": 1024,
            "baseline_sha256": sha256(baseline / "complete.json"),
        },
    )
    sources = list((ROOT / "research/journal_sprint").rglob("*.py"))
    sources.append(ROOT / "docs/journal_sprint/PROTOCOL_W3_STRESS.md")
    for source in sources:
        target = path / "source_snapshot" / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    aggregated = defaultdict(list)
    with (path / "records.jsonl").open("x", encoding="utf-8") as stream:
        for (cid, scale), group in sorted(groups.items()):
            group = sorted(group, key=lambda r: r["k"])
            q = np.array([r["ideal"] for r in group])
            truth = group[0]["base_probability"]
            for condition in ("ideal", "readout", "drift", "overdispersed"):
                write_json(
                    path / f"planned_{cid}_{scale}_{condition}.json",
                    {"contract": cid, "scale": scale, "condition": condition, "reps": 500},
                )
                for rep in range(500):
                    rng = rng_for("week3_stress", cid, scale, condition, rep)
                    latent = q.copy()
                    if condition == "readout":
                        latent = readout_probability(q, 0.02, 0.07)
                    elif condition == "drift":
                        latent = np.clip(
                            q + rng.choice([-1, 1]) * 0.03 * np.array([-1, 0, 1]), 0, 1
                        )
                    elif condition == "overdispersed":
                        latent = rng.beta(100 * q, 100 * (1 - q))
                    counts = rng.binomial(1024, latent).tolist()
                    policies = ["ignored"] + (["known_readout"] if condition == "readout" else [])
                    for policy in policies:
                        confidence = (
                            invert_readout(counts, [1024] * 3, [0, 1, 2], 0.02, 0.07)
                            if policy == "known_readout"
                            else invert(counts, [1024] * 3, [0, 1, 2])
                        )
                        declared = confidence.radius is not None and confidence.radius <= 0.005
                        record = {
                            "contract": cid,
                            "scale": scale,
                            "condition": condition,
                            "rep": rep,
                            "policy": policy,
                            "counts": counts,
                            "latent": latent.tolist(),
                            "components": confidence.components,
                            "contains": confidence.contains(truth),
                            "nonempty": bool(confidence.components),
                            "radius": confidence.radius,
                            "declared": declared,
                            "false": bool(declared and abs(confidence.midpoint - truth) > 0.005),
                            "dataset_id": f"{cid}_{scale}_{condition}_{rep}",
                            "dataset_shots": 3072,
                            "dataset_a_queries": 9216,
                            "dataset_grover_queries": 3072,
                        }
                        stream.write(json.dumps(record, allow_nan=False) + "\n")
                        aggregated[(cid, scale, condition, policy)].append(record)
                stream.flush()
                os.fsync(stream.fileno())
    summaries = []
    for key, records in aggregated.items():
        nonempty = sum(r["nonempty"] for r in records)
        contains = sum(r["contains"] for r in records)
        declared = sum(r["declared"] for r in records)
        false = sum(r["false"] for r in records)
        summaries.append(
            {
                "contract": key[0],
                "scale": key[1],
                "condition": key[2],
                "policy": key[3],
                "trials": len(records),
                "contains": contains,
                "coverage": contains / len(records),
                "nonempty": nonempty,
                "coverage_nonempty": contains / nonempty if nonempty else None,
                "declared": declared,
                "false": false,
                "false_unconditional": false / len(records),
                "false_given_declaration": false / declared if declared else None,
            }
        )
    write_json(path / "summary.json", summaries)
    finish_run(path)
    print(json.dumps(summaries))


if __name__ == "__main__":
    main()
