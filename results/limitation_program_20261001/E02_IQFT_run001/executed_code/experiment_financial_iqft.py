"""Freeze14 archived rotations and retarget them to both actual financial IQFTs."""

# Frozen protocol descriptions retain exact readable literals.
# ruff: noqa: E501

import argparse
from datetime import datetime, timezone
from pathlib import Path
import shutil
import sys

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
from research.limitation_program_20261001.financial_iqft import (
    synthesized_row,
    verify_rotation_library,
)
from research.limitation_program_20261001.progress import ROOT


SOURCE = PROGRAM / "E02_financial_run002"
AUDIT = PROGRAM / "E02_financial_audit_run001"
LIBRARY = ROOT / "results/controlled_completion_followup/synthesis_rotations.json"
CODE = ("experiment_financial_iqft.py", "financial_iqft.py", "test_financial_iqft.py")


def run(output):
    output.relative_to(PROGRAM.resolve())
    assert not output.exists()
    assert read(SOURCE / "summary.json")["passed"]
    assert read(AUDIT / "summary.json")["passed"]
    output.mkdir()
    frozen = {}
    for directory in (SOURCE, AUDIT):
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
    frozen[relative(LIBRARY)] = digest(LIBRARY)
    method = ROOT / "research/controlled_completion_followup/synthesis_rotations.py"
    frozen[relative(method)] = digest(method)
    protocol = dict(
        local_only=True,
        created_utc=datetime.now(timezone.utc).isoformat(),
        item="E02/E07 current source-compatible IQFT synthesis obligation",
        before_tests_and_interval_rotation_verification=True,
        cases=["B4x12", "B8x52"],
        qpe_bits=16,
        serial_shots=15,
        reused_library=relative(LIBRARY),
        target_keys=["pi_1_%d" % (1 << (gap + 1)) for gap in range(2, 16)],
        rotation_strategy="One immutable existing string per exact target; inverse by adjoint; no new gridsynth generation or cost selection",
        interval_matrix_decimal_precision=120,
        synthesis_observation_failure_allowance_exact=[1, 1000],
        usage=4725,
        global_phase_rule="Only scalar W in unconditional terminal IQFT single-qubit gates may be omitted; source external-control Z signs remain explicit",
        tiny_validation_qpe_bits=[2, 3, 4],
        acceptance="Every exact Rz target, signed adjoint, CP decomposition and full little-endian IQFT agrees; interval operator bounds compose into the declared observation budget; complete logical counts derived from actual gate strings and original source-bound row",
        stop_rule="Exactly14 frozen rotation strings, both already audited source rows, no financial circuit or huge QPE replay; failed matrix/count/usage stops this binding",
        original_source_or_estimator_rows_edited=False,
        new_financial_gate_replays=0,
        physical_routing_factories_readout_durations=None,
        frozen_inputs=frozen,
        python=sys.version,
    )
    save(output / "protocol.json", protocol)
    verify(protocol)
    rc = pytest.main(
        [
            str(ROOT / "research/limitation_program_20261001/test_financial_iqft.py"),
            "-q",
            "-p",
            "no:cacheprovider",
            "--junitxml=" + str(output / "tests.xml"),
        ]
    )
    if rc:
        save(output / "failed_tests.json", dict(passed=False, return_code=int(rc)))
        manifest(output, protocol)
        raise AssertionError("Frozen IQFT signed/Fourier tests failed")
    rotations = verify_rotation_library(LIBRARY)
    assert len(rotations) == 14
    save(output / "rotations.json", rotations)
    rows = []
    for case in protocol["cases"]:
        row = read(SOURCE / case / "estimator_ledger.json")
        recipe_path = output / case / "iqft_operations.json"
        operations, result = synthesized_row(row, rotations, relative(recipe_path))
        save(recipe_path, operations)
        result["original_source_estimator_ledger"] = relative(
            SOURCE / case / "estimator_ledger.json"
        )
        result["original_source_estimator_ledger_sha256"] = digest(
            SOURCE / case / "estimator_ledger.json"
        )
        save(output / case / "synthesized_estimator_ledger.json", result)
        rows.append(
            dict(
                case=case,
                logical_qubits=result["logical_qubits"],
                full_T_count=result["full_T_count"],
                full_logical_serial_T_depth=result["full_T_depth"],
                full_known_clifford_t_depth_upper=result["full_known_clifford_t_depth_upper"],
                iqft_synthesis_T_count=result["synthesized_single_qubit_T_count"],
                synthesis_observation_perturbation_upper=result[
                    "synthesis_total_observation_perturbation_upper_exact"
                ],
                physical_runtime_seconds=None,
            )
        )
    save(
        output / "summary.json",
        dict(
            passed=True,
            local_only=True,
            cases=rows,
            reused_distinct_rotations=14,
            total_arbitrary_rotation_applications_per_price=4725,
            complete_logical_estimator_recipe=True,
            physical_runtime_certified=False,
            continuous_price_error_certified=False,
            new_financial_gate_replays=0,
            huge_QPE_statevector_runs=0,
            G2_to_G5="open",
        ),
    )
    manifest(output, protocol)
    print("Both complete logical source-compatible IQFT synthesis rows PASS", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output.resolve())
