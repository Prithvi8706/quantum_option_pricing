"""Freeze then independently audit C07 run002, preserving the failed run001."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess

from research.limitation_program_20261001 import audit_barrier_band as audit


ROOT = audit.ROOT
RESEARCH = ROOT / "research/limitation_program_20261001"
DECLARED_TESTS = 14


def create(path, value):
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def run(directory):
    directory = directory.resolve()
    if not directory.is_relative_to(ROOT):
        raise ValueError("Workspace receipt required")
    directory.mkdir(parents=True, exist_ok=False)
    executed = directory / "executed_code"
    executed.mkdir()
    code = [
        Path(__file__).resolve(),
        RESEARCH / "audit_barrier_band.py",
        RESEARCH / "test_audit_barrier_band.py",
    ]
    inputs = [ROOT / "research/advantage_frontier_20260923/barrier_oracle_depth.py"]
    for name in ("C07_barrier_run001", "C07_barrier_run002"):
        historical = audit.RESULTS / name
        inputs += [path for path in historical.rglob("*") if path.is_file()]
        manifest = audit.read(historical / "manifest.json")
        inputs += [ROOT / name for name in manifest["frozen_inputs"]]
    frozen = {p.relative_to(ROOT).as_posix(): audit.sha(p) for p in sorted(set(code + inputs))}
    snapshots = []
    for path in code:
        snapshot = executed / path.name
        snapshot.write_bytes(path.read_bytes())
        snapshots.append(
            dict(
                original=path.relative_to(ROOT).as_posix(),
                snapshot=snapshot.relative_to(directory).as_posix(),
                sha256=audit.sha(snapshot),
            )
        )
    create(
        directory / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            local_only=True,
            before_meaningful_tests_and_audit=True,
            item="C07 independent analytic and receipt audit",
            target="C07_barrier_run002",
            preserved_first_failure="C07_barrier_run001",
            executed_dependencies=snapshots,
            declared_tests=DECLARED_TESTS,
            fixed_exploratory_eta_exact=[1, 10000],
            new_production_eta_values=0,
            independent_method=(
                "mp.iv110 digits; independent64-term Gaussian integral with exact remainder"
            ),
            relative_radius_check="mp.iv1000 digits; exact80-term positive series geometric upper",
            independent_proof=audit.PROOF,
            finite_financial_samples=0,
            financial_replays=0,
            full_price_error_remains_null=True,
            historical_sources_are_read_only=True,
        ),
    )
    create(directory / "frozen_inputs.json", frozen)
    completed = subprocess.run(
        [
            str(ROOT / ".context/frontier_t0_env/Scripts/python.exe"),
            "-m",
            "pytest",
            "-q",
            str(RESEARCH / "test_audit_barrier_band.py"),
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
    tests = audit.xml_counts(directory / "tests.xml")
    result, error = None, None
    if completed.returncode == 0:
        try:
            result = audit.audit(ROOT)
            create(directory / "audit.json", result)
        except Exception as exception:
            error = dict(type=type(exception).__name__, message=str(exception))
            create(directory / "audit_error.json", error)
    unchanged = all(audit.sha(ROOT / name) == digest for name, digest in frozen.items())
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
            financial_samples=0,
            financial_replays=0,
            new_production_eta_values=0,
            full_G2_closed=False,
            complete_price_error_dollars=None,
        ),
    )
    create(
        directory / "manifest.json",
        dict(
            files={
                p.relative_to(ROOT).as_posix(): audit.sha(p)
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
    parser.add_argument("--output", type=Path, default=audit.RESULTS / "C07_barrier_audit_run001")
    run(parser.parse_args().output)
