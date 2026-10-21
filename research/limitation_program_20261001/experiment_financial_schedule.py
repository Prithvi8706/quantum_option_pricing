"""Freeze one B4 exact bounded-AE schedule and complete-price obligation ledger."""

import argparse
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
import shutil
import sys

import pytest

from research.limitation_program_20261001.complete_price_ledger import make_b4_ledger
from research.limitation_program_20261001.constant_library import digest
from research.limitation_program_20261001.experiment_checkpoint import (
    BASELINE,
    PROGRAM,
    manifest,
    read,
    relative,
    save,
    verify,
)
from research.limitation_program_20261001.financial_bounded_schedule import certified_schedule
from research.limitation_program_20261001.progress import ROOT


SUPPORT = PROGRAM / "E03_support_run001"
AUDIT = PROGRAM / "E03_support_audit_run002"
CODE = (
    "experiment_financial_schedule.py",
    "complete_price_ledger.py",
    "financial_bounded_schedule.py",
    "test_complete_price_ledger.py",
    "test_financial_bounded_schedule.py",
)


def run(output):
    output.relative_to(PROGRAM.resolve())
    assert not output.exists()
    assert read(SUPPORT / "summary.json")["passed"]
    assert read(AUDIT / "summary.json")["passed"]
    output.mkdir()
    frozen = {}
    for directory in (SUPPORT, AUDIT):
        receipt = read(directory / "manifest.json")
        frozen.update(receipt["files"])
        frozen.update(receipt["frozen_inputs"])
        frozen[relative(directory / "manifest.json")] = digest(directory / "manifest.json")
    for name in CODE:
        path = ROOT / "research/limitation_program_20261001" / name
        snapshot = output / "executed_code" / name
        snapshot.parent.mkdir(exist_ok=True)
        shutil.copy2(path, snapshot)
        frozen[relative(path)] = digest(path)
    protocol = dict(
        local_only=True,
        created_utc=datetime.now(timezone.utc).isoformat(),
        item="E02/E07 exact schedule prerequisite and one B4 complete-price ledger",
        before_tests_and_schedule_execution=True,
        case="B4x12",
        epsilon_dollars_exact=[1, 100],
        statistical_error_dollars_exact=[9, 2000],
        estimator_failure_allowance_exact=[3, 1000],
        native_support_span_dollars=64,
        candidate_schedules=1,
        pi_enclosure="Machin identity, 80 alternating rational terms for each arctangent",
        acceptance=(
            "Exact dollar/error conversion, minimal certified power-of-two M and odd median "
            "repetitions, exact union allocations, missing financial bounds never zero"
        ),
        stop_rule=(
            "One declared financial epsilon/failure row; missing bridges become named "
            "prerequisites rather than repeated estimator runs"
        ),
        source_circuit_replays=0,
        financial_price_estimates=0,
        primary_theorem=dict(
            title="Quantum Amplitude Amplification and Estimation",
            url="https://arxiv.org/pdf/quant-ph/0005055",
            theorem="Theorem12, k=1; section4 uniform-state quantum counting interface",
            verified_date="2026-10-02",
            routine_counts=(
                "Derived from new emitted wrapper; theorem query terminology not transferred"
            ),
        ),
        frozen_inputs=frozen,
        python=sys.version,
        executable=sys.executable,
    )
    save(output / "protocol.json", protocol)
    verify(protocol)
    rc = pytest.main(
        [
            *(
                str(ROOT / "research/limitation_program_20261001" / name)
                for name in CODE
                if name.startswith("test_")
            ),
            "-q",
            "-p",
            "no:cacheprovider",
            "--junitxml=" + str(output / "tests.xml"),
        ]
    )
    if rc:
        save(output / "failed_tests.json", dict(passed=False, return_code=int(rc)))
        manifest(output, protocol)
        raise AssertionError("Frozen rational financial schedule/ledger fixtures failed")
    schedule = certified_schedule(Fraction(9, 2000), Fraction(3, 1000), 64)
    schedule["certificate"] = relative(output / "schedule.json")
    save(output / "schedule.json", schedule)
    directory = BASELINE / "B4x12/min-depth"
    ledger = make_b4_ledger(
        schedule,
        dict(
            target=relative(directory / "target.json"),
            target_sha256=digest(directory / "target.json"),
            source=relative(directory / "source.json"),
            source_sha256=digest(directory / "source.json"),
            capped_schedule=relative(directory / "schedule_capped.json"),
            capped_schedule_sha256=digest(directory / "schedule_capped.json"),
            fixed_contract_certificate=relative(AUDIT / "summary.json"),
        ),
        dict(
            certificate=relative(SUPPORT / "B4x12_certificate.json"),
            independent_audit=relative(AUDIT / "summary.json"),
            normalization_span_dollars=64,
            selector_bits=46,
            native_payoff_lower=0,
            native_payoff_upper=42680645928225,
        ),
    )
    assert not ledger["assessment"]["complete_price_certified"]
    save(output / "complete_price_ledger.json", ledger)
    result = dict(
        passed=True,
        local_only=True,
        case="B4x12",
        epsilon_dollars_exact=[1, 100],
        statistical_error_dollars_exact=[9, 2000],
        M=schedule["M"],
        qpe_bits=schedule["qpe_bits"],
        repetitions=schedule["repetitions"],
        controlled_grover_calls=schedule["controlled_grover_calls"],
        longest_single_shot_grover_chain=schedule["longest_single_shot_grover_chain"],
        ideal_error_upper_dollars=float(Fraction(*schedule["ideal_error_upper_exact"])),
        ideal_failure_upper=float(Fraction(*schedule["ideal_failure_upper_exact"])),
        complete_price_assessment=ledger["assessment"],
        financial_price_estimates=0,
        new_complete_financial_gate_replays=0,
        complete_physical_cost_included=False,
        compatible_financial_wrapper_pending=True,
        G2_to_G5="open",
    )
    save(output / "summary.json", result)
    manifest(output, protocol)
    print(
        "Exact bounded schedule and rational ledger PASS",
        schedule["M"],
        schedule["repetitions"],
        schedule["controlled_grover_calls"],
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output.resolve())
