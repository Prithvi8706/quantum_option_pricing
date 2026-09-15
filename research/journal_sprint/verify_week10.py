"""Replay and integrity gate for the week-10 extension archive."""

import argparse
import json
from pathlib import Path

from .checks import archive_path, archive_names, require
from .storage import ROOT, sha256, write_json
from .week10_stress import cases, compare


def verify(folder):
    folder = Path(folder)
    complete = json.loads((folder / "complete.json").read_text())["sha256"]
    archive_names(complete)
    actual = {
        p.relative_to(folder).as_posix()
        for p in folder.rglob("*")
        if p.is_file() and p != folder / "complete.json"
    }
    require(actual == archive_names(complete), "file inventory mismatch")
    for name, digest in complete.items():
        require(sha256(archive_path(folder, name)) == digest, "output hash mismatch")
    config = json.loads((folder / "planned.json").read_text())["config"]
    require(config.get("extension") is True, "extension archive required")
    required_sources = {
        "research/journal_sprint/" + name
        for name in (
            "week10_stress.py",
            "numerical_reference.py",
            "calibrated_readout.py",
            "intervals.py",
            "storage.py",
        )
    }
    required_sources.update(
        {
            "docs/journal_sprint/PROTOCOL_W10_STRESS.md",
            "docs/journal_sprint/PROTOCOL_W10_EXTENSION.md",
        }
    )
    require(archive_names(config["sources"]) == required_sources, "source inventory mismatch")
    archive_names(config["sources"])
    for name, digest in config["sources"].items():
        require(sha256(archive_path(ROOT, name)) == digest, "live source drift")
        require(sha256(archive_path(folder / "source_snapshot", name)) == digest, "snapshot drift")
    declared = json.loads((folder / "cases.json").read_text())
    require(declared == cases(True), "case matrix mismatch")
    rows = [json.loads(line) for line in (folder / "records.jsonl").read_text().splitlines()]
    require(len(rows) == 83, "missing records")
    for row, case in zip(rows, declared):
        expected = json.loads(json.dumps(compare(case)))
        require(row == expected, "replay mismatch")
        require(row["stable"] and row["encloses"], "numerical gate failed")
    summary = json.loads((folder / "summary.json").read_text())
    expected = dict(
        cases=len(rows),
        failed=0,
        unstable=0,
        disconnected=sum(len(r["reference"]) > 1 for r in rows),
        disconnected_intersections=sum(
            r["depths"] == [1, 2] and len(r["reference"]) > 1 for r in rows
        ),
        empty=sum(not r["reference"] for r in rows),
    )
    require(all(summary[k] == v for k, v in expected.items()), "summary mismatch")
    require(expected["disconnected_intersections"] > 0, "topology gate failed")
    return dict(
        verified=True,
        replayed=len(rows),
        checked_files=len(complete),
        scope="integrity and deterministic replay, not external peer review",
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    result = verify(args.source)
    write_json(args.report, result)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
