"""Integrity and shared-path replay of the separately declared pilot follow-up."""

import argparse
import json
from pathlib import Path

from .checks import archive_names, archive_path, require
from .pilot_cs import reanalyze
from .storage import ROOT, sha256, write_json
from .verify_rescue import verify


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--pilot", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    verify(args.source)
    source, pilot = Path(args.source), Path(args.pilot)
    manifest = json.loads((pilot / "complete.json").read_text())["sha256"]
    require(
        archive_names(manifest)
        == {
            p.relative_to(pilot).as_posix()
            for p in pilot.rglob("*")
            if p.is_file() and p != pilot / "complete.json"
        },
        "inventory mismatch",
    )
    for name, digest in manifest.items():
        require(sha256(archive_path(pilot, name)) == digest, "hash mismatch")
    config = json.loads((pilot / "planned.json").read_text())["config"]
    require(config["source_manifest"] == sha256(source / "complete.json"), "input archive drift")
    require(
        archive_names(config["sources"])
        == {"research/journal_sprint/pilot_cs.py", "docs/journal_sprint/PROTOCOL_PILOT_CS_V1.md"},
        "source inventory mismatch",
    )
    for name, digest in config["sources"].items():
        require(sha256(archive_path(ROOT, name)) == digest, "live source drift")
        require(sha256(archive_path(pilot / "source_snapshot", name)) == digest, "snapshot drift")
    original = [json.loads(line) for line in (source / "records.jsonl").read_text().splitlines()]
    expected = []
    for row in original:
        if row["inference"] == "fixed_cp":
            profile = json.loads((source / f"profile_{row['contract']}.json").read_text())[
                row["encoding"]
            ]
            expected.append(reanalyze(row, profile))
    actual = json.loads((pilot / "records.json").read_text())
    require(actual == json.loads(json.dumps(expected)), "replay mismatch")
    require(len(actual) == 2160, "incomplete identities")
    summary = json.loads((pilot / "summary.json").read_text())
    require(
        summary["declared"] == sum(r["status"] == "precision_met" for r in actual), "count mismatch"
    )
    require(summary["misses"] == sum(r["contains"] is False for r in actual), "miss count mismatch")
    require(summary["erroneous"] == sum(r["erroneous"] for r in actual), "error count mismatch")
    result = dict(
        verified=True,
        replayed=2160,
        input_rows_verified=4320,
        scope="post-result reanalysis, not independent experimental replication",
    )
    write_json(args.report, result)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
