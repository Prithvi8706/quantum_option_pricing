"""Freeze and independently audit the fixed two-cutoff composition receipt."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess

from research.limitation_program_20261001 import audit_uniform_composition as audit


ROOT = audit.ROOT
RESEARCH = ROOT / "research/limitation_program_20261001"
DECLARED_TESTS = 11


def create(path, value):
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def run(directory):
    directory = directory.resolve()
    if not directory.is_relative_to(ROOT):
        raise ValueError("Workspace receipt required")
    prerequisites = (
        "C06_pair_run001",
        "C06_pair_audit_run001",
        "C07_bound_date1_run001",
        "C07_composition_screen_run001",
    )
    for name in prerequisites:
        if audit.receipt.read(audit.RESULTS / name / "summary.json")["passed"] is not True:
            raise ValueError("Passed prerequisite required")
    directory.mkdir(parents=True, exist_ok=False)
    executed = directory / "executed_code"
    executed.mkdir()
    code = [
        Path(__file__).resolve(),
        RESEARCH / "audit_uniform_composition.py",
        RESEARCH / "test_audit_uniform_composition.py",
        RESEARCH / "audit_barrier_band.py",
    ]
    inputs = []
    for name in prerequisites:
        historical = audit.RESULTS / name
        inputs += [p for p in historical.rglob("*") if p.is_file()]
        inputs += [
            ROOT / name
            for name in audit.receipt.read(historical / "manifest.json")["frozen_inputs"]
        ]
    frozen = {
        p.relative_to(ROOT).as_posix(): audit.receipt.sha(p) for p in sorted(set(code + inputs))
    }
    snapshots = []
    for path in code:
        snapshot = executed / path.name
        snapshot.write_bytes(path.read_bytes())
        snapshots.append(
            dict(
                original=path.relative_to(ROOT).as_posix(),
                snapshot=snapshot.relative_to(directory).as_posix(),
                sha256=audit.receipt.sha(snapshot),
            )
        )
    create(
        directory / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            local_only=True,
            before_meaningful_tests_and_audit=True,
            item="C07 independent fixed formula-budget screen audit",
            executed_dependencies=snapshots,
            declared_tests=DECLARED_TESTS,
            source_cutoffs=[20, 24],
            dates=list(range(1, 13)),
            formula_forms=list(audit.METHODS),
            additional_cutoff_candidates=0,
            independent_method=(
                "mp.iv110; independent64-term integrated exp with exact Taylor remainder"
            ),
            actual_target_coefficients_reconciled=True,
            forbidden_interpretation="No lower bound on actual probability or financial bias",
            full_price_unknowns_remain_null=True,
            financial_samples_or_replays=0,
        ),
    )
    create(directory / "frozen_inputs.json", frozen)
    completed = subprocess.run(
        [
            str(ROOT / ".context/frontier_t0_env/Scripts/python.exe"),
            "-m",
            "pytest",
            "-q",
            str(RESEARCH / "test_audit_uniform_composition.py"),
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
    tests = audit.receipt.xml_counts(directory / "tests.xml")
    result, error = None, None
    if completed.returncode == 0:
        try:
            result = audit.audit(ROOT)
            create(directory / "audit.json", result)
        except Exception as exception:
            error = dict(type=type(exception).__name__, message=str(exception))
            create(directory / "audit_error.json", error)
    unchanged = all(audit.receipt.sha(ROOT / name) == digest for name, digest in frozen.items())
    passed = (
        completed.returncode == 0
        and tests == dict(tests=DECLARED_TESTS, failures=0, errors=0, skipped=0)
        and result is not None
        and unchanged
    )
    create(
        directory / "summary.json",
        dict(
            passed=passed,
            tests=tests,
            audit_error=error,
            frozen_inputs_unchanged=unchanged,
            historical_receipts_unchanged=unchanged,
            local_only=True,
            source_cutoffs=[20, 24],
            new_cutoff_candidates=0,
            actual_probability_or_bias_lower_bound_claimed=False,
            full_G2_closed=False,
            complete_price_error_dollars=None,
            financial_samples_or_replays=0,
        ),
    )
    create(
        directory / "manifest.json",
        dict(
            files={
                p.relative_to(ROOT).as_posix(): audit.receipt.sha(p)
                for p in sorted(directory.rglob("*"))
                if p.is_file()
            },
            frozen_inputs=frozen,
            manifest_self_hash_excluded=True,
        ),
    )
    print(json.dumps(dict(passed=passed, tests=tests, error=error)))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=audit.RESULTS / "C07_composition_audit_run001"
    )
    run(parser.parse_args().output)
