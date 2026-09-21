"""Reconstruct transfer/pricing records and costs; not an independent math proof."""

from .checks import archive_path

import argparse
from collections import Counter
import json
from pathlib import Path

import numpy as np

from .calibrated_readout import invert_calibrated
from .intervals import price_decision, response
from .run_transfer_price import CONDITIONS, rates
from .storage import finish_run, rng_for, sha256, start_run, write_json
from research.paper_a.benchmark import C6


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source", type=Path, default=Path("results/journal_sprint/week4_transfer_price_v1")
    )
    parser.add_argument("--output", default="results/journal_sprint/week4_transfer_verify_v1")
    args = parser.parse_args()
    source = args.source
    manifest = json.loads((source / "complete.json").read_text())
    for name, expected in manifest["sha256"].items():
        require(sha256(archive_path(source, name)) == expected, f"hash: {name}")
    decisions = json.loads((source / "decisions.json").read_text())
    truths = json.loads((source / "diagnostic_truths.json").read_text())
    seen = set()
    totals = Counter()
    grouped = {}
    for line in (source / "records.jsonl").read_text().splitlines():
        row = json.loads(line)
        key = (row["contract"], row["condition"], row["rep"])
        require(key not in seen, "duplicate dataset")
        seen.add(key)
        cid, condition, _ = key
        decision = decisions[cid]
        require(decision["refused"] == (decision["bound_total"] >= 1), "bound refusal")
        require(set(row["analyses"]) == {"unexpanded", "guarded"}, "analysis arms")
        if decision["refused"]:
            require(
                all(r == {"status": "pre_refusal"} for r in row["analyses"].values()),
                "refusal analyses",
            )
            require("counts" not in row and "calibration_errors" not in row, "refused data")
            costs = (0, 0, 0, 0)
            totals["refused"] += 1
        else:
            totals["executed"] += 1
            a = truths[cid]["amplitude"]
            calrates, f, g = rates(condition)
            key_rng = row["seed_key"]
            require(key_rng == ["week4_transfer_price", cid, condition, row["rep"]], "seed key")
            errors = rng_for(*key_rng, "calibration").binomial(4096, calrates)
            counts = rng_for(*key_rng, "validation").binomial(
                32768, f + (1 - f - g) * response(a, [0, 1, 2])
            )
            require(np.array_equal(errors, row["calibration_errors"]), "calibration replay")
            require(np.array_equal(counts, row["counts"]), "validation replay")
            b = decision["bounds"]
            for method, transfer in (("unexpanded", (0, 0)), ("guarded", (0.03, 0.03))):
                confidence, calibration = invert_calibrated(
                    counts, [32768] * 3, [0, 1, 2], errors, [4096] * 2, transfer_bounds=transfer
                )
                actual = row["analyses"][method]
                expected = price_decision(
                    confidence, b["sensitivity"], b["offset"], decision["bound_total"], 1
                )
                require(
                    [list(c) for c in confidence.components] == actual["components"], "components"
                )
                require(calibration == actual["calibration"], "calibration rectangle")
                require(confidence.contains(a) == actual["amplitude_contains"], "amplitude flag")
                for field in ("status", "radius"):
                    require(expected[field] == actual[field], f"decision {field}")
                interval = expected["interval"]
                require(
                    (list(interval) if interval is not None else None) == actual["interval"],
                    "price interval",
                )
                target = truths[cid]["price"]
                contained = interval is not None and interval[0] <= target <= interval[1]
                false = (
                    expected["status"] == "precision_met" and abs(sum(interval) / 2 - target) > 1
                )
                require(contained == actual["price_contains"], "price flag")
                require(false == actual["false_declaration"], "false declaration flag")
            costs = (98304, 294912, 8192, 106496)
        for field, value in zip(
            ("validation_shots", "validation_A_equivalents", "calibration_shots", "total_shots"),
            costs,
        ):
            require(row[field] == value, f"cost {field}")
            totals[field] += value
        for method, actual in row["analyses"].items():
            group = grouped.setdefault((cid, condition, method), Counter())
            group["attempts"] += 1
            group["executed"] += actual["status"] != "pre_refusal"
            group["declared"] += actual["status"] == "precision_met"
            group["incompatible"] += actual["status"] == "incompatible"
            group["amplitude_contained"] += actual.get("amplitude_contains", False)
            group["price_contained"] += actual.get("price_contains", False)
            group["false_declarations"] += actual.get("false_declaration", False)
    require(seen == {(c, s, r) for c in C6 for s in CONDITIONS for r in range(200)}, "matrix")
    summary = json.loads((source / "summary.json").read_text())
    require(summary["attempts"] == 6000 and len(summary["cells"]) == 60, "summary dimensions")
    summary_keys = {(r["contract"], r["condition"], r["method"]) for r in summary["cells"]}
    require(summary_keys == set(grouped), "missing or duplicated summary cells")
    for cell in summary["cells"]:
        recomputed = grouped[(cell["contract"], cell["condition"], cell["method"])]
        require(all(cell[k] == v for k, v in recomputed.items()), "summary counts")
        for field, denominator in (
            ("false_per_attempt", "attempts"),
            ("false_per_executed", "executed"),
            ("false_given_declaration", "declared"),
        ):
            expected = (
                recomputed["false_declarations"] / recomputed[denominator]
                if recomputed[denominator]
                else None
            )
            require(cell[field] == expected, "summary denominator")
    output = start_run(args.output, {"source_manifest_sha256": sha256(source / "complete.json")})
    write_json(
        output / "verification.json",
        {
            "hashes": len(manifest["sha256"]),
            "datasets": len(seen),
            "cost_totals": dict(totals),
            "inferences_reconstructed": totals["executed"] * 2,
            "scope": "numerical reconstruction, not independent proof or hardware validation",
        },
    )
    finish_run(output)
    print(json.dumps(dict(totals)))


if __name__ == "__main__":
    main()
