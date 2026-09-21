"""Replay durable selection events and independent final validation; descriptive screen."""

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import shutil

from .run_representation_pilot import (
    CONDITIONS,
    CX_CAP,
    KEY_FIELDS,
    POLICIES,
    cells,
    configuration,
    inputs,
    prepare,
    summarize,
    trial,
    truths_for,
)
from .storage import ROOT, finish_run, sha256, start_run, write_json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_config(config, manifests):
    require(
        config == configuration(manifests, config["dependency_sha256"]), "configuration mismatch"
    )


def analyze(rows):
    index = {tuple(r[k] for k in KEY_FIELDS): r for r in rows}
    require(len(index) == len(rows) == 54 and set(index) == set(cells()), "analysis matrix")
    comparisons = []
    feasible = []
    for cid in dict.fromkeys(k[0] for k in index):
        if index[cid, "stationary", "pilot_select"]["executed"]:
            feasible.append(cid)
        for condition in CONDITIONS:
            selected = index[cid, condition, "pilot_select"]
            for policy in POLICIES[:2]:
                fixed = index[cid, condition, policy]
                comparisons.append(
                    dict(
                        contract=cid,
                        condition=condition,
                        baseline=policy,
                        difference_per_attempt=(selected["declared"] - fixed["declared"]) / 100,
                        added_costs={
                            k: v - fixed["acquisition_totals"][k]
                            for k, v in selected["acquisition_totals"].items()
                        },
                    )
                )
    checks = [
        dict(
            contract=cid,
            condition=condition,
            declarations=index[cid, condition, "pilot_select"]["declared"],
            passes=index[cid, condition, "pilot_select"]["declared"] >= 90,
        )
        for cid in feasible
        for condition in CONDITIONS
    ]
    differences = (
        {
            p: sum(
                r["difference_per_attempt"]
                for r in comparisons
                if r["baseline"] == p and r["contract"] in feasible
            )
            / len(checks)
            for p in POLICIES[:2]
        }
        if checks
        else {}
    )
    false = sum(r["false_declarations"] for r in rows)
    return dict(
        comparisons=comparisons,
        readiness=dict(
            cells=checks,
            mean_gains=differences,
            passes=bool(checks)
            and all(c["passes"] for c in checks)
            and all(g >= 0.1 - 1e-12 for g in differences.values()),
            false_declarations_to_investigate=false,
        ),
        scope="descriptive discovery; not conditional coverage or confirmation",
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source", type=Path, default=Path("results/journal_sprint/week8_representation_v1")
    )
    parser.add_argument("--output", default="results/journal_sprint/week8_closeout_v1")
    args = parser.parse_args()
    source = args.source
    manifest = json.loads((source / "complete.json").read_text())
    for name, digest in manifest["sha256"].items():
        require(sha256(source / name) == digest, f"archive hash: {name}")
    config = json.loads((source / "planned.json").read_text())["config"]
    profiles, manifests = inputs()
    validate_config(config, manifests)
    snap = source / "source_snapshot"
    names = {str(p.relative_to(snap)) for p in snap.rglob("*") if p.is_file()}
    require(names == set(config["dependency_sha256"]), "source inventory")
    required = {
        "research/journal_sprint/run_representation_pilot.py",
        "research/journal_sprint/calibrated_readout.py",
        "docs/journal_sprint/PROTOCOL_W8_REPRESENTATION.md",
    }
    require(required <= {Path(p).as_posix() for p in names}, "required dependencies")
    for name, digest in config["dependency_sha256"].items():
        require(
            sha256(snap / name) == digest and sha256(ROOT / name) == digest,
            f"dependency drift: {name}",
        )
    menu = prepare(profiles)
    require(menu == json.loads((source / "menu.json").read_text()), "menu replay")
    truths = truths_for(menu)
    require(
        truths == json.loads((source / "diagnostic_truths.json").read_text()), "diagnostic replay"
    )
    events = {}
    for line in (source / "events.jsonl").read_text().splitlines():
        e = json.loads(line)
        identity = tuple(e[k] for k in (*KEY_FIELDS, "rep"))
        require(identity not in events, "duplicate event")
        events[identity] = e
    seen, groups, totals, phases, misses = (
        set(),
        defaultdict(list),
        Counter(),
        defaultdict(Counter),
        [],
    )
    expected = {(*key, r) for key in cells() for r in range(100)}
    for line in (source / "records.jsonl").read_text().splitlines():
        row = json.loads(line)
        key = tuple(row[k] for k in KEY_FIELDS)
        identity = (*key, row["rep"])
        require(identity in expected and identity not in seen, "record identity")
        seen.add(identity)
        generated = []
        replay = trial(key, row["rep"], menu[key[0]], truths[key[0]], generated.append)
        require(row == json.loads(json.dumps(replay)), "procedure replay")
        require(
            len(generated) == 1 and events[identity] == json.loads(json.dumps(generated[0])),
            "selection event replay",
        )
        groups[key].append(row)
        totals[row["status"]] += 1
        totals["pilot_acquisitions"] += len(row["pilots"])
        if row["selected_n"] is not None:
            totals["final_acquisitions"] += 1
            final = row["final"]
            totals["price_contained"] += int(final["price_contains"])
            totals["false_declarations"] += int(final["false_declaration"])
            totals["multicomponent_intervals"] += int(final["component_count"] > 1)
            if not final["price_contains"]:
                misses.append(dict(identity=identity, selected_n=row["selected_n"], **final))
            for phase, parts in (("pilot", row["pilots"]), ("final", [final])):
                for part in parts:
                    for field, value in part["cost"].items():
                        if not field.startswith("max_"):
                            phases[phase][field] += value
        require(
            row["cost"]["pricing_logical_cx"] <= CX_CAP
            and row["cost"]["calibration_shots"] <= 49152,
            "cost cap",
        )
        for field, value in row["cost"].items():
            if not field.startswith("max_"):
                totals[field] += value
    require(seen == set(events) == expected, "complete event/record matrix")
    summary = json.loads((source / "summary.json").read_text())
    require(summary["attempts"] == 5400, "attempt total")
    for row in summary["cells"]:
        require(row == summarize(groups[tuple(row[k] for k in KEY_FIELDS)]), "summary replay")
    analysis = analyze(summary["cells"])
    output = start_run(args.output, dict(source_manifest_sha256=sha256(source / "complete.json")))
    shutil.copy2(__file__, output / "closeout_representation_pilot.py")
    write_json(
        output / "verification.json",
        dict(
            attempts=len(seen),
            events=len(events),
            cells=len(groups),
            archive_hashes=len(manifest["sha256"]),
            dependency_hashes=len(names),
            totals=dict(totals),
            phase_costs={k: dict(v) for k, v in phases.items()},
            scope="producing-helper replay and event-order inspection; not mathematical proof",
        ),
    )
    write_json(output / "analysis.json", analysis)
    write_json(output / "containment_misses.json", misses)
    finish_run(output)
    print(json.dumps(dict(totals)))


if __name__ == "__main__":
    main()
