"""Freeze current financial estimator contract, then evaluate three theorem rows."""

import argparse
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import subprocess

from research.limitation_program_20261001 import finite_estimator_theorem_screen as screen


ROOT = screen.ROOT
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
    directory.mkdir(parents=True, exist_ok=False)
    executed = directory / "executed_code"
    executed.mkdir()
    code = [
        Path(__file__).resolve(),
        RESEARCH / "finite_estimator_theorem_screen.py",
        RESEARCH / "test_finite_estimator_theorem_screen.py",
        RESEARCH / "audit_barrier_band.py",
    ]
    inputs = [
        ROOT / "docs/limitation_audit_20261001/implementation_plan/ESTIMATION.md",
        ROOT / "docs/limitation_audit_20261001/ESTIMATION_AND_CERTIFICATION.md",
    ]
    for name in (
        "E07_schedule_run001",
        "E02_financial_run002",
        "E02_IQFT_run001",
        "E02_IQFT_audit_run001",
    ):
        historical = screen.RESULTS / name
        inputs += [p for p in historical.rglob("*") if p.is_file()]
        inputs += [
            ROOT / name for name in screen.audit.read(historical / "manifest.json")["frozen_inputs"]
        ]
    frozen = {
        p.relative_to(ROOT).as_posix(): screen.audit.sha(p) for p in sorted(set(code + inputs))
    }
    snapshots = []
    for path in code:
        snapshot = executed / path.name
        snapshot.write_bytes(path.read_bytes())
        snapshots.append(
            dict(
                original=path.relative_to(ROOT).as_posix(),
                snapshot=snapshot.relative_to(directory).as_posix(),
                sha256=screen.audit.sha(snapshot),
            )
        )
    create(
        directory / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            local_only=True,
            before_meaningful_tests_and_formula_evaluation=True,
            item="E04 three-family theorem upper-bound screen",
            executed_dependencies=snapshots,
            declared_tests=DECLARED_TESTS,
            families=list(screen.FAMILIES),
            family_count=3,
            span_dollars=64,
            error_dollars_exact=[9, 2000],
            amplitude_error_exact=[9, 128000],
            failure_exact=[3, 1000],
            retained_canonical_Q_calls=983025,
            primary_sources=screen.PRIMARY_SOURCES,
            rigorous_numeric_method=(
                "mp.iv110 digits; exact-rational financial tolerances and binary rational endpoints"
            ),
            bound_comparison_is_not_actual_cost_lower_bound=True,
            unknown_controller_shot_counts_not_zero=True,
            controller_simulations=0,
            financial_samples_or_gate_replays=0,
            next_controller_scope=(
                "Atmost8 preregistered settings and2 exact tiny-source laws; "
                "separate prospective receipt before observations"
            ),
            full_price_and_physical_certificates=False,
        ),
    )
    create(directory / "frozen_inputs.json", frozen)
    completed = subprocess.run(
        [
            str(ROOT / ".context/frontier_t0_env/Scripts/python.exe"),
            "-m",
            "pytest",
            "-q",
            str(RESEARCH / "test_finite_estimator_theorem_screen.py"),
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
    tests = screen.audit.xml_counts(directory / "tests.xml")
    result, error = None, None
    if completed.returncode == 0:
        try:
            result = screen.screen(ROOT)
            create(directory / "screen.json", result)
        except Exception as exception:
            error = dict(type=type(exception).__name__, message=str(exception))
            create(directory / "screen_error.json", error)
    unchanged = all(screen.audit.sha(ROOT / name) == digest for name, digest in frozen.items())
    passed = (
        completed.returncode == 0
        and tests == dict(tests=DECLARED_TESTS, failures=0, errors=0, skipped=0)
        and result is not None
        and unchanged
    )
    displays = (
        [
            {
                "family": row["family"],
                "general_Q_upper_formula_display": math.nextafter(
                    float(screen.audit.exact(row["general_Q_bound_formula_interval_exact"][1])),
                    math.inf,
                ),
                "rigorous_Q_bound_formula_ceiling": row["rigorous_Q_bound_formula_ceiling"],
            }
            for row in result["families"][1:]
        ]
        if result
        else []
    )
    create(
        directory / "summary.json",
        dict(
            passed=passed,
            tests=tests,
            screen_error=error,
            frozen_inputs_unchanged=unchanged,
            historical_receipts_unchanged=unchanged,
            local_only=True,
            family_count=3,
            canonical_Q_calls=983025,
            displays=displays,
            general_bound_screen_is_not_controller_impossibility=True,
            complete_IQAE_work_or_latency_known=False,
            financial_samples_or_replays=0,
            full_G2_closed=False,
            actual_price_bias_or_cost_lower_bound_claimed=False,
        ),
    )
    create(
        directory / "manifest.json",
        dict(
            files={
                p.relative_to(ROOT).as_posix(): screen.audit.sha(p)
                for p in sorted(directory.rglob("*"))
                if p.is_file()
            },
            frozen_inputs=frozen,
            manifest_self_hash_excluded=True,
        ),
    )
    print(json.dumps(dict(passed=passed, tests=tests, error=error, displays=displays), indent=2))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=screen.RESULTS / "E04_theorem_run001")
    run(parser.parse_args().output)
