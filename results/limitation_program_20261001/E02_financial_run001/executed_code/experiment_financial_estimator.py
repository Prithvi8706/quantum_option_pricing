"""Freeze two matching native payoff wrappers and one exact bounded-AE row each."""

# Prospective protocol descriptions are preserved as readable exact literals.
# ruff: noqa: E501

import argparse
from datetime import datetime, timezone
from pathlib import Path
import shutil
import sys
import time

import pytest

from research.controlled_source_completion.ir import evaluate
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
from research.limitation_program_20261001.financial_estimator_ledger import assemble_estimator_row
from research.limitation_program_20261001.progress import ROOT


SUPPORT = PROGRAM / "E03_support_run001"
AUDIT = PROGRAM / "E03_support_audit_run002"
SCHEDULE = PROGRAM / "E07_schedule_run001"
CODE = (
    "experiment_financial_estimator.py",
    "native_payoff_estimator.py",
    "test_native_payoff_estimator.py",
    "financial_estimator_ledger.py",
    "test_financial_estimator_ledger.py",
    "bounded_price_readout.py",
    "test_bounded_price_readout.py",
)


def prepare(output):
    output.relative_to(PROGRAM.resolve())
    assert not output.exists()
    output.mkdir()
    frozen = {}
    for directory in (BASELINE, SUPPORT, AUDIT, SCHEDULE):
        receipt = read(directory / "manifest.json")
        if "files" in receipt:
            frozen.update(receipt["files"])
            frozen.update(receipt["frozen_inputs"])
        else:
            assert receipt and all(isinstance(value, str) for value in receipt.values())
            frozen.update(
                {
                    relative(directory / name.replace("\\", "/")): value
                    for name, value in receipt.items()
                }
            )
            legacy = read(directory / "protocol.json")
            frozen.update(legacy.get("frozen_inputs", {}))
            frozen.update(legacy.get("leaf_receipt_frozen_inputs", {}))
            frozen.update(
                {
                    item["source"].replace("\\", "/"): item["sha256"]
                    for item in legacy["executed_dependencies"]
                }
            )
        frozen[relative(directory / "manifest.json")] = digest(directory / "manifest.json")
    for name in ("checkpoint_circuit.py", "experiment_checkpoint.py", "progress.py"):
        path = ROOT / "research/limitation_program_20261001" / name
        frozen[relative(path)] = digest(path)
    for name in (
        "research/controlled_priority_completion/estimator_bounded.py",
        "research/controlled_priority_completion/estimator_hadamard.py",
        "research/antithetic_feasibility/estimator.py",
    ):
        frozen[name] = digest(ROOT / name)
    for name in CODE:
        path = ROOT / "research/limitation_program_20261001" / name
        snapshot = output / "executed_code" / name
        snapshot.parent.mkdir(exist_ok=True)
        shutil.copy2(path, snapshot)
        frozen[relative(path)] = digest(path)
    protocol = dict(
        local_only=True,
        created_utc=datetime.now(timezone.utc).isoformat(),
        item="E02/E03 source-compatible bounded digital payoff estimator",
        before_tests_wrapper_emission_and_source_marking_replays=True,
        cases=["B4x12", "B8x52"],
        current_source="A10_coefficient_run001/min-depth per original case",
        target_precision=dict(word_width=72, fraction_bits=40, original_uniform_bits=32),
        normalization=dict(
            selector_bits=46,
            dollar_span=64,
            probability="E[already discounted nativeY]/64",
            second_discount=False,
        ),
        schedule=relative(SCHEDULE / "schedule.json"),
        epsilon_dollars_exact=[1, 100],
        statistical_allowance_exact=[9, 2000],
        ideal_failure_allowance_exact=[3, 1000],
        qpe=dict(M=65536, bits=16, serial_fresh_shots=15),
        readout=dict(
            method="Rational Machin/Taylor interval sin-square, native40 fractional dollar rounding",
            error_dollars_exact=[2, 1 << 40],
        ),
        actual_marking_replays=dict(
            B4x12=dict(
                original_saved_label="positive_payoff",
                selector_boundary_offsets=[-1, 0],
                controls=[0, 1],
                count=4,
            ),
            B8x52=dict(
                original_saved_label="previous_random",
                selector_boundary_offsets=[-1, 0],
                controls=[1],
                count=2,
            ),
        ),
        large_QPE_statevector_or_price_runs=0,
        tiny_complete_iterates=3,
        acceptance="Exact all-input positiveY proof; original source/target/storage/group/native gate bindings; actual selector+literal source inverses; superposed control-off identity and signed reflection on tiny actual circuits; six original-financial marking replays restore all inputs/selector/control/workspace; exact expanded count/readout/rotation ledger with missing synthesis/physical costs null",
        stop_rule="One exactpositive selector46 and one original capped wrapper per B4/B8; one epsilon/failure row. Incompatible source/count/bound fails before an advantage claim; no extra arithmetic portfolios or estimator optimization in this receipt",
        preferred_latency_source_unchanged=True,
        old_full_clean_XOR_financial_replay_total_unchanged=41,
        G2_to_G5="open",
        process_cpu_limit_seconds=1800,
        frozen_inputs=frozen,
        python=sys.version,
        executable=sys.executable,
    )
    save(output / "protocol.json", protocol)
    verify(protocol)
    print("Source-compatible bounded estimator protocol frozen", flush=True)


def run(output):
    from research.limitation_program_20261001.native_payoff_estimator import (
        bind_source_estimator,
        emit_iterate,
        emit_toy_iterates,
        replay_marking,
    )

    protocol = read(output / "protocol.json")
    assert not (output / "summary.json").exists()
    verify(protocol)
    started = time.process_time()
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
        raise AssertionError("Frozen native estimator fixtures failed")
    schedule = read(SCHEDULE / "schedule.json")
    assert (schedule["M"], schedule["qpe_bits"], schedule["repetitions"]) == (65536, 16, 15)
    emit_toy_iterates(output / "toys")
    rows = []
    for case in protocol["cases"]:
        if time.process_time() - started > protocol["process_cpu_limit_seconds"]:
            raise TimeoutError("Prospective native estimator CPU limit")
        binding = bind_source_estimator(
            BASELINE / case / "min-depth", SUPPORT / (case + "_certificate.json"), AUDIT
        )
        wrapper = emit_iterate(binding, output / case)
        row = assemble_estimator_row(wrapper, schedule)
        row["wrapper"] = relative(output / case / "iterate.json")
        row["wrapper_sha256"] = digest(output / case / "iterate.json")
        spec = protocol["actual_marking_replays"][case]
        original = read(BASELINE / case / "comparison.json")
        sample = next(x for x in original["replays"] if x["label"] == spec["original_saved_label"])
        target = read(BASELINE / case / "min-depth/target.json")
        _, trace = evaluate(target, sample["inputs"], True)
        expected_y = trace[target["outputs"]["Y"]]
        assert 0 < expected_y < 1 << 46
        replays = []
        for offset in spec["selector_boundary_offsets"]:
            for control in spec["controls"]:
                actual = replay_marking(wrapper, sample["inputs"], expected_y + offset, control)
                assert actual["y_raw"] == expected_y
                assert actual["marked"] == (offset < 0)
                assert actual["controlled_phase"] == (-1 if control and offset < 0 else 1)
                assert actual["all_input_selector_control_and_workspace_restored"]
                replays.append(
                    dict(
                        passed=True,
                        original_label=sample["label"],
                        inputs=sample["inputs"],
                        expected_y_raw=expected_y,
                        actual=actual,
                    )
                )
                save(output / case / "marking_replays.json", replays)
                print(
                    case,
                    "selector offset",
                    offset,
                    "control",
                    control,
                    "actual financial marking cleanup PASS",
                    flush=True,
                )
        assert len(replays) == spec["count"]
        row["actual_marking_replays"] = len(replays)
        save(output / case / "estimator_ledger.json", row)
        rows.append(row)
    result = dict(
        passed=True,
        local_only=True,
        controlled_grover_calls=schedule["controlled_grover_calls"],
        case_rows=[
            dict(
                case=row["case"],
                source_graph_directions=row["source_graph_directions"],
                source_iterate_resources=row["source_iterate_resources"],
                logical_qubits=row["logical_qubits"],
                fixed_T_count=row["complete_known_T_count_excluding_arbitrary_rotation_synthesis"],
                serial_known_T_depth=row[
                    "serial_known_T_depth_excluding_arbitrary_rotation_synthesis"
                ],
                iqft_arbitrary_Rz_rotations=row["iqft_arbitrary_Rz_rotations"],
                marking_replays=row["actual_marking_replays"],
            )
            for row in rows
        ],
        new_source_marking_gate_replays=sum(row["actual_marking_replays"] for row in rows),
        new_complete_clean_XOR_financial_replays=0,
        historical_complete_clean_XOR_financial_replays=41,
        quantum_price_estimates_run=0,
        full_QPE_statevector_runs=0,
        ideal_digital_mean_certificate=True,
        full_continuous_price_certificate=False,
        full_synthesis_or_physical_cost_certificate=False,
        no_C4_residual_counts_transferred_to_B4_B8=True,
        preferred_latency_source_unchanged=True,
        G2_to_G5="open",
        process_cpu_seconds=time.process_time() - started,
    )
    save(output / "summary.json", result)
    manifest(output, protocol)
    print("Both original financial source-compatible estimator rows PASS", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    (prepare if args.phase == "prepare" else run)(args.output.resolve())
