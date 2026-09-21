"""Week-7 exact replay, paired nesting checks and predeclared descriptive analysis."""

import argparse
from collections import Counter, defaultdict
from itertools import combinations
import json
from pathlib import Path
import shutil

from .run_ablation import (
    BUDGETS,
    CALIBRATIONS,
    CONDITIONS,
    DESIGNS,
    KEY_FIELDS,
    cells,
    configuration,
    diagnostic_truths,
    prepare,
    summarize,
    trial,
    valid_guards,
)
from .run_fixed_discovery import checked_inputs
from .storage import ROOT, finish_run, sha256, start_run, write_json


def require(value, message):
    if not value:
        raise ValueError(message)


def enclosed(narrow, wide):
    return all(any(wl - 1e-12 <= lo and hi <= wu + 1e-12 for wl, wu in wide) for lo, hi in narrow)


def analyze(summaries):
    index = {tuple(r[k] for k in KEY_FIELDS): r for r in summaries}
    require(len(summaries) == len(index) == 216 and set(index) == set(cells()), "analysis matrix")

    def arm(key, g):
        return index[key]["arms"][str(g)]

    def delta(a, b):
        return (
            a["declared"] / a["executed"] - b["declared"] / b["executed"]
            if a["executed"] and b["executed"]
            else None
        )

    contrasts = []
    for key, row in index.items():
        cid, b, n, c, d = key
        for g in valid_guards(c):
            here = arm(key, g)
            for axis, low, other in (
                ("pricing", b == BUDGETS[0], (cid, BUDGETS[1], n, c, d)),
                ("calibration", n == CALIBRATIONS[0], (cid, b, CALIBRATIONS[1], c, d)),
            ):
                if low:
                    contrasts.append(
                        dict(
                            axis=axis,
                            key=list(key),
                            guard=g,
                            paired=False,
                            delivery_difference=delta(arm(other, g), here),
                            added_acquisition_costs={
                                field: index[other]["acquisition_totals"][field] - value
                                for field, value in row["acquisition_totals"].items()
                            },
                        )
                    )
            if d == "direct":
                for name in DESIGNS[1:]:
                    contrasts.append(
                        dict(
                            axis="design",
                            key=list(key),
                            guard=g,
                            paired=False,
                            comparator=name,
                            delivery_difference=delta(arm((cid, b, n, c, name), g), here),
                        )
                    )
        for small, large in combinations(valid_guards(c), 2):
            contrasts.append(
                dict(
                    axis="guard",
                    key=list(key),
                    narrow=small,
                    wide=large,
                    paired=True,
                    delivery_difference=delta(arm(key, large), arm(key, small)),
                    added_acquisition_cost=0,
                )
            )
    feasible = [
        cid
        for cid in dict.fromkeys(k[0] for k in index)
        if index[cid, BUDGETS[0], CALIBRATIONS[0], "stationary", "direct"]["acquired"]
    ]
    screens = []
    for b in BUDGETS:
        for n in CALIBRATIONS:
            checks = []
            for cid in feasible:
                for c in CONDITIONS:
                    cx = arm((cid, b, n, c, "CX_capped"), 0.03)
                    direct = arm((cid, b, n, c, "direct"), 0.03)
                    checks.append(
                        dict(
                            contract=cid,
                            condition=c,
                            cx_declared=cx["declared"],
                            direct_declared=direct["declared"],
                            executed=cx["executed"],
                            passes=cx["declared"] >= 90
                            and cx["declared"] - direct["declared"] >= 10,
                        )
                    )
            screens.append(
                dict(
                    budget=b,
                    calibration_n=n,
                    checks=checks,
                    passes=bool(checks) and all(r["passes"] for r in checks),
                )
            )
    return dict(
        contrasts=contrasts,
        readiness=screens,
        interpretation="descriptive discovery; screen is not confirmation or a risk guarantee",
    )


def validate_config(config, manifests):
    require(
        config == configuration(manifests, config["dependency_sha256"]), "declared config mismatch"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source", type=Path, default=Path("results/journal_sprint/week7_ablation_v1")
    )
    parser.add_argument("--output", default="results/journal_sprint/week7_closeout_v1")
    args = parser.parse_args()
    source = args.source
    manifest = json.loads((source / "complete.json").read_text())
    for name, digest in manifest["sha256"].items():
        require(sha256(source / name) == digest, f"archive hash: {name}")
    config = json.loads((source / "planned.json").read_text())["config"]
    ledger, profiles, manifests = checked_inputs()
    validate_config(config, manifests)
    snapshot = source / "source_snapshot"
    inventory = {str(p.relative_to(snapshot)) for p in snapshot.rglob("*") if p.is_file()}
    require(inventory == set(config["dependency_sha256"]), "dependency inventory")
    for name, digest in config["dependency_sha256"].items():
        require(
            sha256(snapshot / name) == digest and sha256(ROOT / name) == digest,
            f"source drift: {name}",
        )
    required = {
        "research/journal_sprint/run_ablation.py",
        "research/journal_sprint/calibrated_readout.py",
        "docs/journal_sprint/PROTOCOL_W7_ABLATION.md",
    }
    require(required <= {Path(p).as_posix() for p in inventory}, "required sources")
    prepared = prepare(ledger, profiles)
    require(prepared == json.loads((source / "decisions.json").read_text()), "bound/design replay")
    truths = diagnostic_truths(prepared)
    require(truths == json.loads((source / "diagnostic_truths.json").read_text()), "truth replay")
    seen, groups, totals, arm_totals, misses = set(), defaultdict(list), Counter(), Counter(), []
    nesting_checks = 0
    expected = {(*k, r) for k in cells() for r in range(100)}
    with (source / "records.jsonl").open() as stream:
        for line in stream:
            row = json.loads(line)
            key = tuple(row[k] for k in KEY_FIELDS)
            identity = (*key, row["rep"])
            require(identity in expected and identity not in seen, "identity")
            seen.add(identity)
            replay = trial(key, row["rep"], prepared[key[0]], truths.get(key[0]))
            require(row == json.loads(json.dumps(replay)), f"record replay: {identity}")
            groups[key].append(row)
            totals[row["status"]] += 1
            for k, value in row["cost"].items():
                if not k.startswith("max_"):
                    totals[k] += value
            for guard, arm in row["arms"].items():
                arm_totals[arm["status"]] += 1
                arm_totals["price_contained"] += int(arm.get("price_contains", False))
                arm_totals["false_declarations"] += int(arm.get("false_declaration", False))
                if row["status"] == "acquired" and not arm["price_contains"]:
                    misses.append(dict(identity=identity, guard=guard, **arm))
            if row["status"] == "acquired":
                for small, large in combinations(valid_guards(key[3]), 2):
                    require(
                        enclosed(
                            row["arms"][str(small)]["components"],
                            row["arms"][str(large)]["components"],
                        ),
                        "guard enclosure",
                    )
                    nesting_checks += 1
    require(seen == expected, "complete matrix")
    summary = json.loads((source / "summary.json").read_text())
    require(summary["attempts"] == 21600, "attempt count")
    for row in summary["cells"]:
        key = tuple(row[k] for k in KEY_FIELDS)
        require(row == summarize(groups[key]), "cell reconstruction")
    analysis = analyze(summary["cells"])
    output = start_run(args.output, dict(source_manifest_sha256=sha256(source / "complete.json")))
    shutil.copy2(__file__, output / "closeout_ablation.py")
    write_json(
        output / "verification.json",
        dict(
            attempts=len(seen),
            cells=len(groups),
            archive_hashes=len(manifest["sha256"]),
            dependency_hashes=len(inventory),
            nesting_checks=nesting_checks,
            acquisition_totals=dict(totals),
            arm_totals=dict(arm_totals),
            scope="replay uses producing trial/numerical helpers; not independent proof",
        ),
    )
    write_json(output / "analysis.json", analysis)
    write_json(output / "containment_misses.json", misses)
    finish_run(output)
    print(json.dumps(dict(acquisition_totals=dict(totals), arm_totals=dict(arm_totals))))


if __name__ == "__main__":
    main()
