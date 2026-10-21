"""Freeze local provenance inputs before searching nine historical Stage C SHAs."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

from research.limitation_program_20261001 import historical_drift_reconciliation as audit


ROOT = audit.ROOT
RESEARCH = ROOT / "research/limitation_program_20261001"
DECLARED_TESTS = 9


def create(path, value):
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def run(directory):
    directory = directory.resolve()
    if not directory.is_relative_to(ROOT):
        raise ValueError("Local workspace receipt required")
    directory.mkdir(parents=True, exist_ok=False)
    executed = directory / "executed_code"
    executed.mkdir()
    code = [
        Path(__file__).resolve(),
        RESEARCH / "historical_drift_reconciliation.py",
        RESEARCH / "test_historical_drift_reconciliation.py",
    ]
    metadata = audit.metadata(ROOT)
    inputs = [ROOT / name for name in audit.PATHS] + [
        ROOT / name for name in metadata["archive_file_candidates"]
    ]
    execution_roots = []
    for name in audit.RECEIPTS:
        historical = audit.RESULTS / name
        inputs += [p for p in historical.rglob("*") if p.is_file()]
        for row in audit.roots_for(historical):
            row["snapshot_workspace_path"] = audit.relative(historical / row["snapshot"])
            execution_roots.append(row)
    closure, _ = audit.project_import_closure(ROOT, execution_roots)
    inputs += list(closure.values())
    frozen = {audit.relative(p): audit.sha(p) for p in sorted(set(code + inputs))}
    snapshots = []
    for path in code:
        snapshot = executed / path.name
        snapshot.write_bytes(path.read_bytes())
        snapshots.append(
            dict(
                original=audit.relative(path),
                snapshot=snapshot.relative_to(directory).as_posix(),
                sha256=audit.sha(snapshot),
            )
        )
    create(directory / "prepared_search_inventory.json", metadata)
    create(
        directory / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            local_only=True,
            before_old_blob_payload_search_tests_and_reconciliation=True,
            executed_dependencies=snapshots,
            declared_tests=DECLARED_TESTS,
            affected_receipts=list(audit.RECEIPTS),
            declared_drift_paths=list(audit.PATHS),
            transformations=list(audit.TRANSFORMS),
            commits=metadata["commits"],
            git_object_format=metadata["object_format"],
            git_blob_candidate_count=len(metadata["git_blob_candidates"]),
            local_archive_filename_candidate_count=len(metadata["archive_file_candidates"]),
            max_commit_candidates=audit.MAX_COMMITS,
            max_archive_candidates=audit.MAX_ARCHIVE_CANDIDATES,
            original_expected_hashes_are_never_waived=True,
            global_live_integrity_false_until_original_live_expectations_match=True,
            restore_live_sources_or_edit_historical_receipts=False,
            runtime_import_nonexecution_claim=False,
            actor_attribution=False,
            finance_or_quantum_executions=0,
            acceptance=(
                "Recover and hash exact original byte strings; distinguish raw Git bytes "
                "from explicit line-ending materialization; report legitimate live "
                "mismatches unchanged"
            ),
            full_program_quantum_array_scan_repeated=False,
        ),
    )
    create(directory / "frozen_inputs.json", frozen)
    completed = subprocess.run(
        [
            str(ROOT / ".context/frontier_t0_env/Scripts/python.exe"),
            "-m",
            "pytest",
            "-q",
            str(RESEARCH / "test_historical_drift_reconciliation.py"),
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
    tests = {
        field: sum(int(x.attrib.get(field, 0)) for x in suites)
        for field in ("tests", "failures", "errors", "skipped")
    }
    result, error = None, None
    if completed.returncode == 0:
        try:
            result = audit.reconcile(ROOT, directory, metadata)
            create(directory / "reconciliation.json", result)
        except Exception as exception:
            error = dict(type=type(exception).__name__, message=str(exception))
            create(directory / "reconciliation_error.json", error)
    unchanged = all(audit.sha(ROOT / name) == digest for name, digest in frozen.items())
    passed = (
        completed.returncode == 0
        and tests == dict(tests=DECLARED_TESTS, failures=0, errors=0, skipped=0)
        and result is not None
        and result["passed"]
        and unchanged
    )
    create(
        directory / "summary.json",
        dict(
            passed=passed,
            tests=tests,
            reconciliation_error=error,
            frozen_inputs_unchanged=unchanged,
            old_receipts_and_live_sources_unchanged=unchanged,
            historical_snapshot_integrity=result["historical_snapshot_integrity"]
            if result
            else None,
            global_live_integrity=False,
            expected_hashes_waived=False,
            local_only=True,
            recovered_old_source_paths=sum(
                x["historical_old_bytes_recovered"] for x in result["rows"]
            )
            if result
            else 0,
            live_expected_mismatches=sum(not x["expected_live_matches"] for x in result["rows"])
            if result
            else None,
            historical_snapshot_scope=(
                "Nine old inventory byte strings plus receipt-owned files and declared "
                "snapshots/literal project import sources"
            ),
            finance_or_quantum_executions=0,
        ),
    )
    create(
        directory / "manifest.json",
        dict(
            files={
                audit.relative(p): audit.sha(p) for p in sorted(directory.rglob("*")) if p.is_file()
            },
            frozen_inputs=frozen,
            manifest_self_hash_excluded=True,
        ),
    )
    print(
        json.dumps(
            dict(
                passed=passed,
                tests=tests,
                error=error,
                historical_snapshot_integrity=result["historical_snapshot_integrity"]
                if result
                else None,
                global_live_integrity=False,
                recovered=result["distinct_drift_paths"] if result else 0,
            )
        )
    )
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=audit.RESULTS / "A01_drift_run001")
    run(parser.parse_args().output)
