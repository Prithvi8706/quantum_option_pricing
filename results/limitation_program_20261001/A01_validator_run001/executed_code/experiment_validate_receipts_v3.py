"""Freeze V3 validator and tiny adversarial receipts before fixture execution."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

from research.limitation_program_20261001 import validate_receipts_v3 as validator


ROOT = validator.ROOT
RESEARCH = ROOT / "research/limitation_program_20261001"
RESULTS = ROOT / "results/limitation_program_20261001"
DECLARED_TESTS = 18


def relative(path):
    return path.relative_to(ROOT).as_posix()


def create(path, value):
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def run(directory):
    directory = directory.resolve()
    if not directory.is_relative_to(RESULTS):
        raise ValueError("Local limitation-program receipt required")
    directory.mkdir(parents=True, exist_ok=False)
    snapshot_dir = directory / "executed_code"
    snapshot_dir.mkdir()
    code = [
        Path(__file__).resolve(),
        RESEARCH / "validate_receipts_v3.py",
        RESEARCH / "test_validate_receipts_v3.py",
    ]
    archive_manifest = RESULTS / "A01_drift_run001/manifest.json"
    archive_inputs = [archive_manifest] + [
        ROOT / name for name in validator.read(archive_manifest)["files"]
    ]
    inputs = code + [RESEARCH / "validate_receipts_v2.py"] + archive_inputs
    frozen = {relative(path): validator.digest(path) for path in sorted(set(inputs))}
    snapshots = []
    for path in code:
        snapshot = snapshot_dir / path.name
        snapshot.write_bytes(path.read_bytes())
        snapshots.append(
            dict(
                original=relative(path),
                snapshot=snapshot.relative_to(directory).as_posix(),
                sha256=validator.digest(snapshot),
            )
        )
    create(
        directory / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            local_only=True,
            before_meaningful_fixture_tests=True,
            executed_dependencies=snapshots,
            declared_tests=DECLARED_TESTS,
            fixture_inputs="Temporary synthetic receipts only",
            strict_passed_definition="No live expected-hash mismatch",
            archival_definition=(
                "Separately validated exact old snapshots inside the explicitly supplied "
                "receipt, matching all affected-manifest membership and hash references"
            ),
            allowed_archival_paths=sorted(validator.DRIFT_PATHS),
            allowed_affected_receipts=sorted(validator.AFFECTED_RECEIPTS),
            known_archive_receipt=validator.ARCHIVE_RECEIPT,
            immutable_v2_map_resolution_preserved=True,
            legitimate_expected_hashes_waived=False,
            live_mismatches_removed_or_overridden=False,
            hash_reads="Streaming one MiB chunks, per invocation memoization only",
            permanent_hash_cache=False,
            runtime_nonexecution_claim=False,
            full_program_scan_executed=False,
            finance_or_quantum_executions=0,
        ),
    )
    create(directory / "frozen_inputs.json", frozen)
    completed = subprocess.run(
        [
            str(ROOT / ".context/frontier_t0_env/Scripts/python.exe"),
            "-m",
            "pytest",
            "-q",
            str(RESEARCH / "test_validate_receipts_v3.py"),
            "--junitxml=" + str(directory / "tests.xml"),
            "-p",
            "no:cacheprovider",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    (directory / "pytest_stdout.txt").write_text(completed.stdout, encoding="utf-8")
    (directory / "pytest_stderr.txt").write_text(completed.stderr, encoding="utf-8")
    suites = list(ET.parse(directory / "tests.xml").getroot().iter("testsuite"))
    counts = {
        field: sum(int(suite.attrib.get(field, 0)) for suite in suites)
        for field in ("tests", "failures", "errors", "skipped")
    }
    unchanged = all(validator.digest(ROOT / name) == digest for name, digest in frozen.items())
    passed = (
        completed.returncode == 0
        and counts == dict(tests=DECLARED_TESTS, failures=0, errors=0, skipped=0)
        and unchanged
    )
    create(
        directory / "summary.json",
        dict(
            passed=passed,
            tests=counts,
            frozen_inputs_unchanged=unchanged,
            strict_live_failure_preserved_when_archive_valid=True,
            archive_snapshot_escape_corruption_or_unlisted_membership_rejected=True,
            v2_map_and_snapshot_resolution_fixture_checked=True,
            full_program_scan_executed=False,
            actual_program_archival_or_live_outcome_evaluated=False,
            legitimate_expected_hashes_waived=False,
            local_only=True,
            finance_or_quantum_executions=0,
        ),
    )
    create(
        directory / "manifest.json",
        dict(
            files={
                relative(path): validator.digest(path)
                for path in sorted(directory.rglob("*"))
                if path.is_file()
            },
            frozen_inputs=frozen,
            manifest_self_hash_excluded=True,
        ),
    )
    print(json.dumps(dict(passed=passed, tests=counts, full_program_scan_executed=False)))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=RESULTS / "A01_validator_run001")
    run(parser.parse_args().output)
