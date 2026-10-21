"""Freeze one actual C06 delta20 radius and two existing C07 date1 bound forms."""

import argparse
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import subprocess
import time

from research.limitation_program_20261001 import audit_barrier_band as audit
from research.limitation_program_20261001 import bind_one_date_error as bridge


ROOT = bridge.ROOT
RESEARCH = ROOT / "research/limitation_program_20261001"
DECLARED_TESTS = 12


def create(path, value):
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def upper_display(value):
    return math.nextafter(float(audit.exact(value)), math.inf)


def run(directory):
    directory = directory.resolve()
    if not directory.is_relative_to(ROOT):
        raise ValueError("Workspace receipt required")
    directory.mkdir(parents=True, exist_ok=False)
    executed = directory / "executed_code"
    executed.mkdir()
    code = [
        Path(__file__).resolve(),
        RESEARCH / "bind_one_date_error.py",
        RESEARCH / "test_bind_one_date_error.py",
    ]
    inputs = [
        RESEARCH / "audit_barrier_band.py",
        RESEARCH / "barrier_band_certificate.py",
        RESEARCH / "financial_bounded_schedule.py",
        ROOT / "research/advantage_frontier_20260923/barrier_oracle_depth.py",
    ]
    for name in ("C06_pair_run001", "C07_barrier_run002", "C07_barrier_audit_run001"):
        historical = bridge.RESULTS / name
        inputs += [p for p in historical.rglob("*") if p.is_file()]
        inputs += [
            ROOT / name for name in audit.read(historical / "manifest.json")["frozen_inputs"]
        ]
    for name in ("E03_support_run001", "E03_support_audit_run002"):
        historical = bridge.RESULTS / name
        inputs += [p for p in historical.rglob("*") if p.is_file()]
    frozen = {p.relative_to(ROOT).as_posix(): audit.sha(p) for p in sorted(set(code + inputs))}
    snapshots = []
    for path in code + inputs[:4]:
        snapshot = (
            executed / path.name
            if path.parent == RESEARCH
            else executed / path.parent.name / path.name
        )
        snapshot.parent.mkdir(parents=True, exist_ok=True)
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
            before_meaningful_tests_and_binding=True,
            item="C07 one actual C06 date1 error bridge",
            executed_dependencies=snapshots,
            declared_tests=DECLARED_TESTS,
            case="B4x12",
            date=1,
            cutoff_bits=20,
            selected_eta_values=1,
            eta_claim=bridge.ETA_CLAIM,
            bad_event_claim=bridge.BAD_CLAIM,
            bound_forms=["density", "centered_interval_maximum"],
            bound_form_count=2,
            eta_grid_or_adaptive_search=False,
            independent_validation="mp.iv110 + separate64-term integral",
            event_contribution_proof=bridge.EVENT_PROOF,
            date1_bad_event_probability="3*2^-20",
            whole_B4_bad_event_probability="30*2^-20",
            payoff_difference_cap_dollars_exact=[40, 1],
            tail_scopes_are_separate=True,
            C06_independent_audit_required_before_adoption=True,
            full_price_unknowns_remain_null=True,
            new_financial_price_samples=0,
            new_financial_gate_replays=0,
            maximum_process_cpu_seconds=300,
        ),
    )
    create(directory / "frozen_inputs.json", frozen)
    completed = subprocess.run(
        [
            str(ROOT / ".context/frontier_t0_env/Scripts/python.exe"),
            "-m",
            "pytest",
            "-q",
            str(RESEARCH / "test_bind_one_date_error.py"),
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
    started = time.process_time()
    if completed.returncode == 0:
        try:
            result = bridge.bind(ROOT)
            create(directory / "certificate.json", result)
        except Exception as exception:
            error = dict(type=type(exception).__name__, message=str(exception))
            create(directory / "binding_error.json", error)
    cpu = time.process_time() - started
    unchanged = all(audit.sha(ROOT / name) == digest for name, digest in frozen.items())
    passed = (
        completed.returncode == 0
        and tests == dict(tests=DECLARED_TESTS, failures=0, errors=0, skipped=0)
        and result is not None
        and unchanged
        and cpu <= 300
    )
    displays = {}
    if result:
        for kind, contribution in result["one_date_barrier_contributions"].items():
            displays[kind] = {
                name: upper_display(value)
                for name, value in contribution.items()
                if name.endswith("_exact")
            }
    create(
        directory / "summary.json",
        dict(
            passed=passed,
            tests=tests,
            binding_error=error,
            frozen_inputs_unchanged=unchanged,
            historical_receipts_unchanged=unchanged,
            elapsed_binding_cpu_seconds=cpu,
            local_only=True,
            cutoff_bits=20,
            case="B4x12",
            date=1,
            selected_eta_values=1,
            bound_forms=2,
            display_floats_rounded_upward=True,
            eta_basket_display_dollars_upper=upper_display(result["eta_basket_dollars_exact"])
            if result
            else None,
            one_date_event_contribution_displays=displays,
            C06_independent_audit_required_before_adoption=True,
            full_G2_closed=False,
            complete_price_error_dollars=None,
            new_financial_price_samples=0,
            new_financial_gate_replays=0,
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
    print(
        json.dumps(
            dict(passed=passed, tests=tests, error=error, cpu=cpu, displays=displays), indent=2
        )
    )
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=bridge.RESULTS / "C07_bound_date1_run001")
    run(parser.parse_args().output)
