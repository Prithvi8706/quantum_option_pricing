"""Freeze two fixed-cutoff optimistic all-date budget screens for B4x12."""

import argparse
from datetime import datetime, timezone
from pathlib import Path
import shutil

import pytest

from research.limitation_program_20261001.constant_library import digest
from research.limitation_program_20261001.experiment_checkpoint import (
    PROGRAM,
    manifest,
    read,
    relative,
    save,
    verify,
)
from research.limitation_program_20261001.progress import ROOT
from research.limitation_program_20261001.uniform_composition_screen import optimistic_terms


RECEIPTS = (
    "C06_pair_run001",
    "C06_pair_audit_run001",
    "C07_barrier_run002",
    "C07_barrier_audit_run001",
    "C07_bound_date1_run001",
)
CODE = (
    "experiment_uniform_composition_screen.py",
    "uniform_composition_screen.py",
    "test_uniform_composition_screen.py",
)


def run(output):
    output.relative_to(PROGRAM.resolve())
    assert not output.exists()
    for name in RECEIPTS:
        assert read(PROGRAM / name / "summary.json")["passed"]
    output.mkdir()
    frozen = {}
    for name in RECEIPTS:
        path = PROGRAM / name
        receipt = read(path / "manifest.json")
        frozen.update(receipt["files"])
        frozen.update(receipt["frozen_inputs"])
        frozen[relative(path / "manifest.json")] = digest(path / "manifest.json")
    for name in CODE:
        path = ROOT / "research/limitation_program_20261001" / name
        shutil.copy2(path, output / name)
        frozen[relative(path)] = digest(path)
    protocol = dict(
        created_utc=datetime.now(timezone.utc).isoformat(),
        local_only=True,
        case="B4x12",
        before_tests_and_two_fixed_cutoff_screens=True,
        candidates=[20, 24],
        dates=list(range(1, 13)),
        methods=["density", "centered_interval_maximum"],
        allowance_dollars_exact=[11, 2000],
        financial_samples_or_gate_replays=0,
        acceptance=(
            "Enclose optimistic certificate formulas and compare with remaining "
            "headroom; never label their lower endpoints actual price-bias lower bounds"
        ),
        stop_rule=(
            "Two previously fixed cutoffs and two previously audited methods only. "
            "If the optimistic formulas exceed headroom, retain the one-date "
            "certificate and move to a different bound without precision changes."
        ),
        full_native_path_proof_attempted=False,
        omitted_native_terms_certified_zero=False,
        frozen_inputs=frozen,
    )
    save(output / "protocol.json", protocol)
    verify(protocol)
    rc = pytest.main(
        [
            str(ROOT / "research/limitation_program_20261001/test_uniform_composition_screen.py"),
            "-q",
            "-p",
            "no:cacheprovider",
            "--junitxml=" + str(output / "tests.xml"),
        ]
    )
    if rc:
        save(output / "summary.json", dict(passed=False, return_code=int(rc)))
        manifest(output, protocol)
        raise AssertionError("Frozen optimistic composition fixtures failed")
    certificate = read(PROGRAM / "C06_pair_run001/certificate.json")
    assert [row["cutoff_bits"] for row in certificate["candidates"]] == protocol["candidates"]
    assert certificate["source_bindings"]["B4x12"]["pair_count"] == 30
    results = []
    for candidate in certificate["candidates"]:
        date1 = candidate["B4_date1"]
        row = optimistic_terms(
            candidate["coordinate_discrepancy_upper_exact"],
            date1["common_coefficient_literal_exact"],
            date1["idiosyncratic_coefficient_literal_exact"],
            candidate["delta_exact"],
        )
        row["cutoff_bits"] = candidate["cutoff_bits"]
        row["source_candidate_pointer"] = "/candidates/" + str(len(results))
        save(output / ("cutoff" + str(candidate["cutoff_bits"]) + "_screen.json"), row)
        results.append(
            dict(
                cutoff_bits=candidate["cutoff_bits"],
                methods=row["methods"],
                all_fixed_methods_rejected=all(
                    method["formula_floor_exceeds_remaining_headroom"]
                    for method in row["methods"].values()
                ),
            )
        )
    save(
        output / "summary.json",
        dict(
            passed=True,
            local_only=True,
            results=results,
            optimistic_uniform_composition_can_fit=any(
                not row["all_fixed_methods_rejected"] for row in results
            ),
            actual_price_bias_lower_bound_claimed=False,
            full_native_path_error_proved=False,
            full_G2_closed=False,
            current_precision_and_law_preserved=True,
            financial_samples_or_gate_replays=0,
            next_bound_required=(
                "Expected/distribution-sensitive coupling or a validated sharper "
                "barrier comparison; the current uniform-error union screen is insufficient"
            ),
        ),
    )
    manifest(output, protocol)
    print("Fixed uniform-composition screens retained; full G2 remains open", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output.resolve())
