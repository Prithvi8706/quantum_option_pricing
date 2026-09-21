"""Reconstruct week-9 diagnostic and hash-check the main discovery claim sources."""

import argparse
import json
from pathlib import Path
import shutil

import mpmath as mp

from .checks import archive_path, relative_archive_path
from .numerical_reference import PRECISION, STEPS, case_table
from .run_numerical_check import compare
from .storage import ROOT, finish_run, sha256, start_run, write_json


def require(value, message):
    if not value:
        raise ValueError(message)


def checked_archive(folder):
    manifest = json.loads((folder / "complete.json").read_text())
    for name, digest in manifest["sha256"].items():
        require(sha256(archive_path(folder, name)) == digest, f"hash mismatch: {name}")
    return manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source", type=Path, default=Path("results/journal_sprint/week9_numerical_v1")
    )
    parser.add_argument("--output", default="results/journal_sprint/week9_verify_v1")
    args = parser.parse_args()
    source = args.source
    manifest = checked_archive(source)
    config = json.loads((source / "planned.json").read_text())["config"]
    require(
        {k: v for k, v in config.items() if k != "dependency_sha256"}
        == dict(
            protocol="PROTOCOL_W9_NUMERICAL",
            precision=PRECISION,
            bisections=STEPS,
            mpmath=mp.__version__,
            case_count=312,
        ),
        "configuration",
    )
    snap = source / "source_snapshot"
    require(
        {p.relative_to(snap).as_posix() for p in snap.rglob("*") if p.is_file()}
        == {relative_archive_path(n).as_posix() for n in config["dependency_sha256"]},
        "source inventory",
    )
    producing = {
        "research/journal_sprint/run_numerical_check.py",
        "research/journal_sprint/numerical_reference.py",
        "research/journal_sprint/calibrated_readout.py",
        "research/journal_sprint/intervals.py",
        "research/journal_sprint/storage.py",
        "docs/journal_sprint/PROTOCOL_W9_NUMERICAL.md",
    }
    inventory = {relative_archive_path(name).as_posix() for name in config["dependency_sha256"]}
    require(len(inventory) == len(config["dependency_sha256"]), "aliased source names")
    require(producing <= inventory, "missing producing dependency")
    for name, digest in config["dependency_sha256"].items():
        require(sha256(archive_path(snap, name)) == digest, f"snapshot drift: {name}")
        if relative_archive_path(name).as_posix() in producing:
            require(sha256(archive_path(ROOT, name)) == digest, f"producing source drift: {name}")
    cases = case_table()
    require(cases == json.loads((source / "cases.json").read_text()), "case matrix")
    rows = [json.loads(line) for line in (source / "records.jsonl").read_text().splitlines()]
    require(len(rows) == len(cases) == 312, "case count")
    for row, case in zip(rows, cases):
        require(row == json.loads(json.dumps(compare(case))), f"reference replay {case['case_id']}")
    summary = json.loads((source / "summary.json").read_text())
    expected = dict(
        cases=312,
        failed=sum(not r["encloses"] for r in rows),
        empty_reference=sum(not r["reference_components"] for r in rows),
        full_reference=sum(r["reference_components"] == [["0.0", "1.0"]] for r in rows),
        multicomponent_reference=sum(len(r["reference_components"]) > 1 for r in rows),
        max_endpoint_slack=max(r["max_endpoint_slack"] for r in rows),
    )
    require(expected == {k: summary[k] for k in expected}, "numerical summary")
    evidence = []
    for name, attempts in (
        ("week5_fixed_discovery_v1", 7200),
        ("week6_transfer_grid_v1", 32400),
        ("week7_ablation_v1", 21600),
        ("week8_representation_v2", 5400),
    ):
        folder = ROOT / "results/journal_sprint" / name
        old = checked_archive(folder)
        s = json.loads((folder / "summary.json").read_text())
        require(s["attempts"] == attempts, "historical attempt total")
        arm_level = name == "week7_ablation_v1"
        units = [a for c in s["cells"] for a in c["arms"].values()] if arm_level else s["cells"]
        evidence.append(
            dict(
                archive=name,
                manifest_sha256=sha256(folder / "complete.json"),
                hashes=len(old["sha256"]),
                attempts=s["attempts"],
                cells=len(s["cells"]),
                declaration_unit="inference arm" if arm_level else "procedure",
                declarations=sum(c["declared"] for c in units),
                scope="archive hashes and summary aggregation; not pricing replay",
            )
        )
    output = start_run(args.output, dict(source_manifest_sha256=sha256(source / "complete.json")))
    shutil.copy2(__file__, output / "verify_numerical_check.py")
    write_json(
        output / "verification.json",
        dict(
            archive_hashes=len(manifest["sha256"]),
            dependency_hashes=len(config["dependency_sha256"]),
            live_producing_dependencies=len(producing),
            **expected,
            scope="high-precision reference replay; not formal certification",
        ),
    )
    write_json(output / "claim_sources.json", evidence)
    finish_run(output)
    print(json.dumps(expected))


if __name__ == "__main__":
    main()
