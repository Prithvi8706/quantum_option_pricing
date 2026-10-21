"""Prospective exact B4/B8 digital support certificate, before estimator emission."""

# Prospective proof and normalization descriptions are exact receipt literals.
# ruff: noqa: E501

import argparse
from datetime import datetime, timezone
import shutil
from pathlib import Path
import sys

import pytest

from research.limitation_program_20261001.constant_library import digest
from research.limitation_program_20261001.experiment_checkpoint import (
    read,
    save,
    relative,
    manifest,
    verify,
    PROGRAM,
    BASELINE,
)
from research.limitation_program_20261001.progress import ROOT
from research.limitation_program_20261001.prove_native_payoff_support import certify


def run(output):
    output.relative_to(PROGRAM.resolve())
    assert not output.exists()
    output.mkdir()
    frozen = {}
    dependencies = []
    names = (
        "prove_native_payoff_support.py",
        "test_native_payoff_support.py",
        "experiment_native_support.py",
        "baseline.py",
        "interval_bounds.py",
        "prove_log_exponent.py",
    )
    for name in names:
        path = ROOT / "research/limitation_program_20261001" / name
        snapshot = output / "executed_code" / name
        snapshot.parent.mkdir(exist_ok=True)
        shutil.copy2(path, snapshot)
        frozen[relative(path)] = digest(path)
        dependencies.append(
            dict(
                source=relative(path),
                snapshot=snapshot.relative_to(output).as_posix(),
                sha256=digest(path),
            )
        )
    for name in (
        "research/advantage_frontier_20260923/barrier_oracle_depth.py",
        "research/controlled_source_completion/ir.py",
        "research/controlled_source_completion/finance.py",
        "research/controlled_source_completion/optimize.py",
    ):
        frozen[name] = digest(ROOT / name)
    for case in ("B4x12", "B8x52"):
        for name in ("target.json", "source.json", "schedule_capped.json"):
            path = BASELINE / case / "min-depth" / name
            frozen[relative(path)] = digest(path)
    protocol = dict(
        local_only=True,
        created_utc=datetime.now(timezone.utc).isoformat(),
        item="E03 exact native payoff support prerequisite",
        before_tests_and_certificate_execution=True,
        cases=["B4x12", "B8x52"],
        method="Exact integer range-reduction cells, outward integer Estrin intervals with same-operand squaring, positivity/no-overflow, strict barrier conditioning, actual rounded average/discount",
        acceptance="Complete original builder/optimized target equality, all clipped integer cells covered, every native intermediate bounded without overflow, maskedY support<40 dollars; finite test traces never replace all-input proof",
        stop_rule="One proof per original source, one independent tiny SSA exhaustion; no approximation or pricing input-law changes",
        complete_price_error_certified=False,
        estimator_yet_emitted=False,
        frozen_inputs=frozen,
        executed_dependencies=dependencies,
        python=sys.version,
    )
    save(output / "protocol.json", protocol)
    verify(protocol)
    rc = pytest.main(
        [
            str(ROOT / "research/limitation_program_20261001/test_native_payoff_support.py"),
            "-q",
            "-p",
            "no:cacheprovider",
            "--junitxml=" + str(output / "tests.xml"),
        ]
    )
    if rc:
        save(output / "failed_tests.json", dict(passed=False, return_code=int(rc)))
        manifest(output, protocol)
        raise AssertionError("Frozen native support proof tests failed")
    cases = []
    for assets, dates, case in ((4, 12, "B4x12"), (8, 52, "B8x52")):
        target = read(BASELINE / case / "min-depth/target.json")
        proof = certify(target, assets, dates)
        save(output / (case + "_certificate.json"), proof)
        cases.append(
            dict(
                case=case,
                payoff_raw_bounds=proof["payoff_raw_bounds"],
                selector_random_bits=proof["selector_random_bits"],
                selector_span_dollars_rational=proof["selector_span_dollars_rational"],
            )
        )
    save(
        output / "summary.json",
        dict(
            passed=True,
            local_only=True,
            cases=cases,
            all_input_native_output_support_certified=True,
            finite_samples_used_as_support_proof=False,
            complete_financial_gate_replays=0,
            G2_to_G5="open",
            next="Emit exact positive support selector and source-bound estimator ledger; independently audit support before using its normalization.",
        ),
    )
    manifest(output, protocol)
    print("Exact native payoff support certificates frozen", cases, flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.output.resolve())
