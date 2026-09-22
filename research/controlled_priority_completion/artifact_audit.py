"""Freeze/verify this continuation and audit historical byte preservation."""

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIRECTORY = ROOT / "results/controlled_priority_completion"
MANIFEST = DIRECTORY / "artifact_manifest.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def old_audit():
    old = ROOT / "results/controlled_source_completion/validation_v2"
    archive = json.loads((old / "artifact_manifest.json").read_text())
    for item in archive["artifacts"]:
        path = ROOT / item["path"].replace("\\", "/")
        assert path.stat().st_size == item["bytes"] and sha(path) == item["sha256"]
    for item in archive["source_snapshot"]:
        assert sha(old / "snapshot" / item["path"].replace("\\", "/")) == item["sha256"]
    return dict(
        unchanged_artifacts=len(archive["artifacts"]),
        unchanged_source_snapshots=len(archive["source_snapshot"]),
    )


def paths():
    for directory in (
        "research/controlled_priority_completion",
        "results/controlled_priority_completion",
        "docs/controlled_priority_completion",
        "manuscript/controlled-compound-2026-09-22",
    ):
        for path in sorted((ROOT / directory).rglob("*")):
            if (
                path.is_file()
                and path != MANIFEST
                and "__pycache__" not in path.parts
                and "release_validation" not in path.parts
                and path.name != "RELEASE_RECEIPT.md"
            ):
                yield path


def bindings():
    # Every emitted leaf byte file is bound to its independently counted metadata.
    leaf_count = 0
    for path in (DIRECTORY / "range_compile_v1/leaves_f40").glob("*.json"):
        record = json.loads(path.read_text())
        assert sha(path.parent / record["gate_file"]) == record["sha256"]
        leaf_count += 1
    for name in ("capacity_revised.json", "capacity_range.json", "capacity_estimator_review.json"):
        record = json.loads((DIRECTORY / name).read_text())
        for relative, expected in record["input_sha256"].items():
            assert sha(DIRECTORY / relative) == expected, (name, relative)
    record = json.loads((DIRECTORY / "capacity_integration_review.json").read_text())
    for relative, expected in record["input_sha256"].items():
        assert sha(ROOT / relative) == expected, relative
    for directory in ("parallel_v1", "range_parallel_v1"):
        for path in (DIRECTORY / directory).glob("*_limit_*.json"):
            record = json.loads(path.read_text())
            assert sha(ROOT / record["source_manifest"]) == record["source_sha256"]
            if "range_certificate" in record:
                assert sha(ROOT / record["range_certificate"]) == record["range_certificate_sha256"]
    return dict(leaf_hashes=leaf_count, cross_artifact_bindings_passed=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze", action="store_true")
    args = parser.parse_args()
    historical, cross = old_audit(), bindings()
    if args.freeze:
        data = dict(
            format="controlled-priority-artifact-manifest-v1",
            historical=historical,
            cross_artifact_checks=cross,
            artifacts=[
                dict(path=p.relative_to(ROOT).as_posix(), bytes=p.stat().st_size, sha256=sha(p))
                for p in paths()
            ],
        )
        MANIFEST.write_text(json.dumps(data, indent=2) + "\n")
    data = json.loads(MANIFEST.read_text())
    for record in data["artifacts"]:
        path = ROOT / record["path"]
        assert path.stat().st_size == record["bytes"] and sha(path) == record["sha256"], path
    assert {p.relative_to(ROOT).as_posix() for p in paths()} == {
        r["path"] for r in data["artifacts"]
    }
    print(
        json.dumps(dict(**historical, **cross, verified_current_artifacts=len(data["artifacts"])))
    )


if __name__ == "__main__":
    main()
