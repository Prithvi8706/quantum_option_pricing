"""Prospectively freeze and audit three existing residual-estimator recipes."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

from research.limitation_program_20261001.estimator_ledger_export_v2 import (
    SELECTED_ROWS,
    discover_archive_inputs,
    export_archive,
)


ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
RESULTS = ROOT / "results/limitation_program_20261001"
DECLARED_TESTS = 35


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def create(path, data):
    with path.open("x", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, allow_nan=False)
        handle.write("\n")


def run(directory):
    directory = directory.resolve()
    if not directory.is_relative_to(ROOT):
        raise ValueError("Receipt must stay in the local workspace")
    directory.mkdir(parents=True, exist_ok=False)
    snapshots = directory / "executed"
    snapshots.mkdir()
    code = [
        Path(__file__).resolve(),
        RESEARCH / "estimator_ledger_export_v2.py",
        RESEARCH / "test_estimator_ledger_export_v2.py",
    ]
    inputs = discover_archive_inputs(ROOT)
    # These existing sources explain archived semantics; they are not imported
    # or reexecuted by the independent exporter.
    inputs += [
        ROOT / "research/controlled_priority_completion/combined_wrappers.py",
        ROOT / "research/controlled_priority_completion/combined_cost.py",
        ROOT / "research/controlled_priority_completion/parallel_source.py",
        ROOT / "research/controlled_priority_completion/estimator_hadamard.py",
        ROOT / "research/controlled_priority_completion/estimator_bounded.py",
        ROOT / "research/controlled_source_completion/compiler.py",
        ROOT / "research/controlled_source_completion/envelope.py",
        ROOT / "research/controlled_priority_completion/range_audit.py",
        RESULTS / "E02_archive_run001/manifest.json",
        RESULTS / "E02_archive_run001/summary.json",
    ]
    dependencies = sorted(set(code + inputs))
    frozen = {path.relative_to(ROOT).as_posix(): sha(path) for path in dependencies}
    executed = []
    for path in code:
        target = snapshots / path.name
        target.write_bytes(path.read_bytes())
        executed.append(
            dict(
                original=path.relative_to(ROOT).as_posix(),
                snapshot=target.relative_to(directory).as_posix(),
                sha256=sha(target),
            )
        )
    create(
        directory / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            item="E02 archived estimator invocation ledger v2",
            previous_receipt="E02_archive_run001",
            previous_failure=(
                "Exporter v1 assumed a byte hash for the range target; historical range_audit "
                "defines sorted-JSON semantic SHA256. Historical artifacts unchanged."
            ),
            local_only=True,
            before_meaningful_test_execution=True,
            before_meaningful_archive_expansion=True,
            executed_dependencies=executed,
            frozen_input_count=len(frozen),
            declared_tests=DECLARED_TESTS,
            selected_rows=[
                dict(model=model, method=method, mode=mode) for model, method, mode in SELECTED_ROWS
            ],
            expected_controlled_calls=[1203320, 2967610, 7864305],
            maximum_rows=3,
            parameter_scans=0,
            new_financial_candidate_attempts=0,
            complete_financial_replays=0,
            new_quantum_unitary_tests=0,
            contract=(
                "Only original C4/H8, Kc=6, one-strike residual mean error .002/discount "
                "and ideal estimator failure .003."
            ),
            audit=(
                "Expand actual integer Hadamard stages or QPE powers; validate wrapper "
                "compute/inverse, literal selector inverse, phase synthesis, signed reflection, "
                "native schedule and leaf metadata; independently reconcile saved T resources."
            ),
            gate_arrays=(
                "The unchanged archived gate arrays are SHA-addressed in native metadata "
                "but not replayed or rehashed by this count audit."
            ),
            unknowns=(
                "Readout, reset, feedback, Clifford time, routing, factories and full-price "
                "obligations stay explicitly unknown, never free zero."
            ),
            financial_transfer=(
                "No archived call count multiplied by current B4 depth. A fresh dollar selector, "
                "proved support and bound wrapper are separate pending work."
            ),
            freeze_semantics=(
                "Any failed first execution keeps this receipt; executed code changes "
                "require a new version and receipt."
            ),
        ),
    )
    # Preserve the prospective input inventory even if a later audit fails.
    create(directory / "frozen_inputs.json", frozen)
    xml_path = directory / "pytest.xml"
    completed = subprocess.run(
        [
            str(ROOT / ".context/frontier_t0_env/Scripts/python.exe"),
            "-m",
            "pytest",
            "-q",
            str(RESEARCH / "test_estimator_ledger_export_v2.py"),
            f"--junitxml={xml_path}",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    (directory / "pytest_stdout.txt").write_text(completed.stdout, encoding="utf-8")
    (directory / "pytest_stderr.txt").write_text(completed.stderr, encoding="utf-8")
    suites = list(ET.parse(xml_path).getroot().iter("testsuite"))
    counts = {
        field: sum(int(s.attrib.get(field, 0)) for s in suites)
        for field in ("tests", "failures", "errors", "skipped")
    }
    ledger, error = None, None
    try:
        ledger = export_archive(ROOT)
        create(directory / "ledger.json", ledger)
    except Exception as exception:
        error = dict(type=type(exception).__name__, message=str(exception))
        create(directory / "export_error.json", error)
    unchanged = all(sha(ROOT / path) == expected for path, expected in frozen.items())
    passed = (
        completed.returncode == 0
        and counts["tests"] == DECLARED_TESTS
        and not any(counts[k] for k in ("failures", "errors", "skipped"))
        and ledger is not None
        and unchanged
    )
    create(
        directory / "summary.json",
        dict(
            passed=passed,
            local_only=True,
            tests=counts,
            returncode=completed.returncode,
            frozen_inputs_unchanged=unchanged,
            export_error=error,
            archived_rows_exported=len(ledger["rows"]) if ledger else 0,
            new_financial_candidate_attempts=0,
            complete_financial_replays=0,
            new_quantum_unitary_tests=0,
            original_residual_contract_only=True,
            current_B4_estimator_pending=True,
            controlled_calls=[
                r["schedule_expansion"]["controlled_wrapper_calls"] for r in ledger["rows"]
            ]
            if ledger
            else None,
            advantage_demonstrated=False,
        ),
    )
    files = {
        path.relative_to(ROOT).as_posix(): sha(path)
        for path in sorted(directory.rglob("*"))
        if path.is_file()
    }
    create(
        directory / "manifest.json",
        dict(
            files=files,
            frozen_inputs=frozen,
            manifest_self_hash_excluded=True,
            historical_receipts_unchanged=unchanged,
        ),
    )
    print(
        json.dumps(
            dict(
                passed=passed,
                tests=counts,
                directory=directory.relative_to(ROOT).as_posix(),
                export_error=error,
            ),
            indent=2,
        )
    )
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=RESULTS / "E02_archive_run002")
    run(parser.parse_args().output)
