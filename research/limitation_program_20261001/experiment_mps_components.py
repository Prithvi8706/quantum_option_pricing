"""Prospective q10 target plus three native MPS component ledgers, no synthesis."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import os
from pathlib import Path
import shutil
import sys
import time
import traceback
import xml.etree.ElementTree as ET

os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import numpy as np  # noqa: E402
import pytest  # noqa: E402

from research.limitation_program_20261001.experiment_mps_structure_v2 import (  # noqa: E402
    PROGRAM,
    RESEARCH,
    bind_frozen,
    create,
    finish_manifest,
    pinned_interpreter,
    read,
    relative,
    receipt_files,
    sha,
    verify,
)
from research.limitation_program_20261001.mps_loader_components import (  # noqa: E402
    BONDS,
    DPS,
    TARGETS,
    SYNTHESIS_RESERVE,
    assessment_rows,
    build_target,
    certify_emission,
    compress_once,
    exact_contract,
    literal_vector,
    normalized_trace_distance,
    operation_data,
    pair,
    save_literals,
)
from research.limitation_program_20261001.mps_sequential_structure_v2 import (  # noqa: E402
    apply_operations,
    decompose_plan,
    inverse_operations,
    make_structure_plan,
    right_canonicalize,
    structure_diagnostics,
)

CODE = (
    "mps_loader_components.py",
    "test_mps_loader_components.py",
    "experiment_mps_components.py",
    "mps_component_preflight.json",
)
DEPENDENCIES = (
    "experiment_mps_structure_v2.py",
    "mps_sequential_structure_v2.py",
    "financial_bounded_schedule.py",
)
PREREQUISITES = (
    "A04_structure_run002",
    "A05_loading_run001",
    "A05_loading_audit_run001",
    "A03_law_screen_run001",
    "A03_law_screen_audit_run001",
)
TESTS = 16
CPU_LIMIT = 900
ADMISSION_CPU = 840
WALL_LIMIT = 1800


class BudgetCensoredError(RuntimeError):
    """A global budget exit; never an ordinary unsupported candidate exception."""


def prepare(output):
    pinned_interpreter()
    output = Path(output).resolve()
    output.relative_to(PROGRAM)
    if output.exists():
        raise FileExistsError("A fresh q10 component receipt is required")
    frozen = {}

    def bind(name, expected):
        bind_frozen(frozen, name, expected)

    for name in PREREQUISITES:
        directory = PROGRAM / name
        summary = read(directory / "summary.json")
        if summary.get("passed") is not True or summary.get("budget_censored", False) is not False:
            raise ValueError("The successful structural/loading/law-audit prerequisite is missing")
        manifest = read(directory / "manifest.json")
        for field in ("files", "frozen_inputs"):
            for path, expected in manifest[field].items():
                bind(path, expected)
        bind(relative(directory / "manifest.json"), sha(directory / "manifest.json"))
    if (
        read(PROGRAM / "A03_law_screen_run001/summary.json")[
            "q10_uniform_certificate_meets_fixed_law_budget"
        ]
        is not False
    ):
        raise ValueError("The separate failed q10 law screen must remain accurately bound")
    loading = read(PROGRAM / "A05_loading_run001/certificate.json")
    b8 = next(row for row in loading["rows"] if row["case"] == "B8x52")
    if b8["conservative_scalar_trace_allowance_exact"] != pair(TARGETS[0]):
        raise ValueError(
            "The conservative468-factor target does not match the audited loading budget"
        )
    for name in CODE + DEPENDENCIES:
        bind(relative(RESEARCH / name), sha(RESEARCH / name))
    preflight = read(RESEARCH / "mps_component_preflight.json")
    if not (
        preflight["fixed_bond_limits"] == list(BONDS)
        and preflight["fixed_scalar_trace_targets_exact"] == list(map(pair, TARGETS))
        and preflight["prospective_unique_new_fixtures"] == TESTS
        and preflight["process_CPU_limit_seconds_including_fixtures_and_all_candidates"]
        == CPU_LIMIT
        and preflight["new_work_admission_CPU_seconds"] == ADMISSION_CPU
        and preflight["wall_limit_seconds"] == WALL_LIMIT
    ):
        raise ValueError("The fixed component preflight and producer inventory disagree")
    verify(frozen)
    output.mkdir()
    try:
        prepare_receipt(output, frozen)
    except BaseException as failure:
        create(
            output / "preparation_failure.json",
            {
                "failure_type": type(failure).__name__,
                "message": str(failure),
                "traceback": traceback.format_exc(),
                "partial_files_preserved": True,
                "fixed_receipt_terminal_no_retry": True,
            },
        )
        create(
            output / "summary.json",
            {
                "passed": False,
                "local_only": True,
                "preparation_failed": True,
                "budget_censored": isinstance(failure, (BudgetCensoredError, TimeoutError)),
                "partial_files_preserved": True,
                "fixed_receipt_terminal_no_retry": True,
                "new_synthesis_calls": 0,
                "full_preparation_Clifford_T_error_or_cost": None,
                "source_law_or_financial_ledger_adopted": False,
            },
        )
        finish_manifest(output, {"frozen_inputs": frozen})
        raise


def prepare_receipt(output, frozen):
    for name in CODE:
        shutil.copy2(RESEARCH / name, output / name)
        if sha(output / name) != frozen[relative(RESEARCH / name)]:
            raise ValueError("Frozen component code snapshot differs: " + name)
    verify(frozen)
    create(
        output / "protocol.json",
        {
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "local_only": True,
            "before_tests_CDF_SVD_SDK_or_native_costs": True,
            "requires_root_Stage_C_supervisor_and_exclusive_children_terminal_clearance": True,
            "frozen_inputs": frozen,
            "all_frozen_insertions_resolve_aliases_and_preserve_previous_SHA_expectations": True,
            "partial_preparation_failures_are_terminal_and_preserved": True,
            "current_candidate_attempt_preserved_on_global_failure_or_censor": True,
            "SDK_imports_and_calls_occur_only_in_the_frozen_run": True,
            "executed_dependencies": [
                {
                    "original": relative(RESEARCH / name),
                    "snapshot": name,
                    "sha256": frozen[relative(RESEARCH / name)],
                }
                for name in CODE
            ],
            "target": "q10 Gaussian bins on[-6,6], conditional and midpoint-labelled",
            "fixed_bonds": list(BONDS),
            "fixed_scalar_targets_exact": list(map(pair, TARGETS)),
            "CDF_nonnegative_boundaries_maximum": 513,
            "CDF_fixture_point_already_in_target": [3, 2],
            "interval_decimal_precision": DPS,
            "root_ceiling_bits": 256,
            "CDF_degree": 256,
            "pi_arctangent_terms": 240,
            "exact_binary64_literal_coefficients_inputs_matrices_angles_and_phases": True,
            "compressions_maximum": 3,
            "native_circuits_maximum": 3,
            "local_SDK_calls_maximum": 30,
            "native_slots_maximum_per_candidate": 20000,
            "SDK_optimization_level": 0,
            "SDK_seed_transpiler": 0,
            "SDK_basis": ["ry", "rz", "cx"],
            "SDK_check_input": True,
            "no_rank_adaptation_precision_retry_or_repeat_emission": True,
            "declared_unique_tests": TESTS,
            "new_fixture_SVD_SDK_calls": 0,
            "structural_tests_recredited": 0,
            "native_full_matrix_interval_error_includes_SDK_global_phase": True,
            "exact_literal_inverse_is_separate_from_fresh_input_error": True,
            "fixed_dirty_reference_statevectors_per_emitted_candidate": 1,
            "fixed_dirty_reference_statevectors_maximum": 3,
            "dirty_reference_wires_maximum": 14,
            "dirty_reference_amplitudes_maximum": 16384,
            "dirty_reference_inverse_max_amplitude_difference_threshold": "1e-9",
            "native_dense_full_operators": 0,
            "future_synthesis_reserve_exact": pair(SYNTHESIS_RESERVE),
            "new_synthesis_calls": 0,
            "complete_preparation_Clifford_T_error_or_cost": None,
            "conditional_disjoint_scalar_factor_count": 468,
            "pure_product_refinement": False,
            "q10_uniform_price_law_certificate_failed_separately": True,
            "new_financial_source_prices_or_replays": 0,
            "source_law_and_current_price_ledger_changed": False,
            "process_CPU_limit_seconds": CPU_LIMIT,
            "new_work_admission_CPU_seconds": ADMISSION_CPU,
            "elapsed_wall_limit_seconds": WALL_LIMIT,
            "numerical_threads_per_process": 1,
            "python": sys.version,
        },
    )
    print("One q10 target and exactly three fixed bond candidates prospectively frozen", flush=True)


def _test_credit(path):
    cases = list(ET.parse(path).getroot().iter("testcase"))
    identities = {(case.attrib.get("classname"), case.attrib["name"]) for case in cases}
    if (
        len(cases) != len(identities)
        or len(cases) != TESTS
        or any(
            case.find(tag) is not None for case in cases for tag in ("failure", "error", "skipped")
        )
    ):
        raise ValueError("The16 new component fixtures did not all pass distinctly")
    return {
        "new_unique_fixtures_passed": TESTS,
        "structural_fixtures_recredited": 0,
        "test_identities": [list(item) for item in sorted(identities)],
    }


def _plan_data(plan):
    return {
        "num_wires": plan.num_wires,
        "output_wires_msb_first": list(plan.output_wires_msb_first),
        "bond_wires_low_bit_first": list(plan.bond_wires_low_bit_first),
        "required_initial_zero_wires": list(plan.required_initial_zero_wires),
        "final_bond_rank": plan.final_bond_rank,
        "transitions": [
            {
                "site": item.site,
                "output_wire": item.output_wire,
                "left_rank": item.left_rank,
                "right_rank": item.right_rank,
                "local_wires": list(item.local_wires),
                "swap_before": list(item.swap_before) if item.swap_before is not None else None,
                "newly_cleared_wire": item.newly_cleared_wire,
                "isometry_columns": save_literals(item.isometry_columns),
                "completed_local_matrix": save_literals(item.matrix),
                "completion_change_numeric_not_a_certificate": item.completion_change_numeric,
                "unitary_defect_numeric_not_a_certificate": item.unitary_defect_numeric,
            }
            for item in plan.transitions
        ],
    }


def _dirty_reference_diagnostic(directory, plan, operations, inverse, checkpoint):
    """One deterministic dirty entangled vector, with no dense full operator."""
    checkpoint()
    total_wires = plan.num_wires + 1
    size = 1 << total_wires
    if total_wires > 14 or size > 16384:
        raise ValueError("The fixed dirty/reference vector allocation bound was exceeded")
    indices = np.arange(size, dtype=np.int64)
    state = (indices % 17 - 8) + 1j * ((3 * indices + 5) % 19 - 9)
    state /= np.linalg.norm(state)
    np.save(directory / "dirty_reference_initial.npy", state, allow_pickle=False)
    create(
        directory / "dirty_reference_protocol.json",
        {
            "fixed_vectors": 1,
            "actual_wires_including_reference": total_wires,
            "actual_amplitudes": size,
            "reference_wire": plan.num_wires,
            "all_output_and_bond_wires_may_be_dirty": True,
            "deterministic_coefficients": "(i mod17-8)+I*((3i+5)mod19-9), once normalized",
            "maximum_inverse_amplitude_difference": "1e-9",
            "numerical_diagnostic_is_not_a_loader_or_full_operator_certificate": True,
        },
    )
    forward = state
    for operation in operations:
        checkpoint()
        forward = apply_operations(forward, (operation,), total_wires)
    np.save(directory / "dirty_reference_forward.npy", forward, allow_pickle=False)
    restored = forward
    for operation in inverse:
        checkpoint()
        restored = apply_operations(restored, (operation,), total_wires)
    np.save(directory / "dirty_reference_restored.npy", restored, allow_pickle=False)
    difference = float(np.max(np.abs(restored - state)))
    norm_difference = float(abs(np.linalg.norm(forward) - np.linalg.norm(state)))
    if not np.isfinite(difference) or difference >= 1e-9:
        raise AssertionError("The fixed actual native dirty/reference inverse diagnostic failed")
    return {
        "passed": True,
        "fixed_vectors": 1,
        "actual_wires_including_reference": total_wires,
        "actual_amplitudes": size,
        "max_inverse_amplitude_difference_numeric": difference,
        "forward_norm_difference_numeric": norm_difference,
        "all_saved_scalar_global_phases_replayed": True,
        "dense_full_global_operator_constructed": False,
        "numerical_diagnostic_is_a_rigorous_preparation_bound": False,
    }


def run(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM)
    if (output / "summary.json").exists():
        raise FileExistsError("The q10 component receipt is already terminal")
    protocol = read(output / "protocol.json")
    started_cpu, started_wall = time.process_time(), time.monotonic()

    def admit():
        if time.process_time() - started_cpu >= ADMISSION_CPU or (
            time.monotonic() - started_wall >= WALL_LIMIT
        ):
            raise BudgetCensoredError(
                "The fixed global component-work admission budget was exhausted"
            )

    points, assessments = [], []
    checked_files = None
    try:
        verify(protocol["frozen_inputs"])
        pinned_interpreter()
        # The inherited structural receipt freezes this exact installed SDK.
        # Import its exception class only after the new protocol verifies.
        from qiskit.exceptions import QiskitError

        rc = pytest.main(
            [
                str(RESEARCH / "test_mps_loader_components.py"),
                "-q",
                "-p",
                "no:cacheprovider",
                "--junitxml=" + str(output / "tests.xml"),
            ]
        )
        if rc:
            raise AssertionError("The fixed component fixtures failed")
        create(output / "test_credit_reconciliation.json", _test_credit(output / "tests.xml"))
        admit()
        amplitudes, target = build_target(admit)
        create(output / "q10_target_certificate.json", target)
        table_error = Fraction(*target["ideal_CDF_to_normalized_literal_target_trace_upper_exact"])
        target_literals = literal_vector(amplitudes)
        for bond in BONDS:
            admit()
            directory = output / ("bond" + str(bond))
            directory.mkdir()
            point = {
                "bond": bond,
                "attempted_once": True,
                "supported": False,
                "native_emission_completed": False,
                "actual_SDK_calls": None,
                "dirty_reference_inverse_diagnostic_completed": False,
                "terminal_status": "incomplete",
                "stage": "compression",
            }
            points.append(point)
            compression_error = None
            try:
                cores, numeric = compress_once(amplitudes, bond)
                create(
                    directory / "compressed_cores.json",
                    {
                        "cores": [save_literals(core) for core in cores],
                        "numeric_diagnostic": numeric,
                    },
                )
                compressed = exact_contract(cores, admit)
                point["stage"] = "compression_certificate"
                compression_error, deficit = normalized_trace_distance(target_literals, compressed)
                create(
                    directory / "compression_certificate.json",
                    {
                        "literal_target_to_literal_tensor_trace_upper_exact": pair(
                            compression_error
                        ),
                        "exact_normalized_overlap_deficit": pair(deficit),
                        "no_SVD_discarded_error_theorem_assumed": True,
                    },
                )
                admit()
                point["stage"] = "canonicalization"
                canonical = right_canonicalize(cores)
                create(
                    directory / "canonical_cores.json",
                    {
                        "cores": [save_literals(core) for core in canonical.cores],
                        "numeric_normalizer_literal": save_literals([canonical.initial_normalizer]),
                        "numeric_final_gauge_literal": save_literals(
                            [canonical.final_gauge_scalar]
                        ),
                        "numeric_residual_not_a_certificate": (
                            canonical.reconstruction_residual_numeric
                        ),
                        "numeric_row_defect_not_a_certificate": (
                            canonical.maximum_row_isometry_defect_numeric
                        ),
                    },
                )
                plan = make_structure_plan(canonical)
                create(directory / "structure_plan.json", _plan_data(plan))
                admit()
                point["stage"] = "SDK_decomposition"
                operations, records = decompose_plan(
                    plan, maximum_local_calls=10, maximum_operations=20000
                )
                inverse = inverse_operations(operations)
                create(
                    directory / "native_operations.json",
                    {
                        "forward": [operation_data(item) for item in operations],
                        "literal_inverse": [operation_data(item) for item in inverse],
                        "local_SDK_records": list(records),
                        "diagnostics": structure_diagnostics(plan, operations),
                    },
                )
                point.update(native_emission_completed=True, actual_SDK_calls=len(records))
                admit()
                point["stage"] = "native_emission_certificate"
                emission = certify_emission(cores, canonical, plan, operations, records, admit)
                create(directory / "native_emission_certificate.json", emission)
                emission_error = Fraction(
                    *emission["compressed_to_exact_native_preparation_trace_upper_exact"]
                )
                point["stage"] = "dirty_reference_inverse_diagnostic"
                diagnostic = _dirty_reference_diagnostic(
                    directory, plan, operations, inverse, admit
                )
                create(directory / "dirty_reference_diagnostic.json", diagnostic)
                point["dirty_reference_inverse_diagnostic_completed"] = True
                point["stage"] = "fixed_target_assessments"
                rotations = sum(op.gate in ("ry", "rz") for op in operations)
                rows = assessment_rows(
                    bond, table_error, compression_error, emission_error, rotations
                )
                create(directory / "fixed_target_assessments.json", rows)
                assessments.extend(rows)
                point.update(
                    supported=True,
                    terminal_status="supported",
                    native_rotations=rotations,
                    synthesis_eligible=any(
                        row["component_ledger_eligible_for_one_future_registry"] for row in rows
                    ),
                )
            except (ValueError, np.linalg.LinAlgError, QiskitError) as failure:
                # Ordinary fixed-method domain/SDK failures do not change the
                # global budget and do not introduce another rank or circuit.
                if point["stage"] not in (
                    "compression",
                    "compression_certificate",
                    "canonicalization",
                    "SDK_decomposition",
                ):
                    point.update(
                        terminal_status="failed",
                        failure_type=type(failure).__name__,
                        failure_message=str(failure),
                    )
                    raise
                point.update(terminal_status="unsupported", unsupported_reason=str(failure))
                create(
                    directory / "unsupported.json",
                    {
                        "failure_type": type(failure).__name__,
                        "message": str(failure),
                        "traceback": traceback.format_exc(),
                    },
                )
                for target_allowance in TARGETS:
                    assessments.append(
                        {
                            "bond": bond,
                            "scalar_target_exact": pair(target_allowance),
                            "table_trace_upper_exact": pair(table_error),
                            "compression_trace_upper_exact": (
                                pair(compression_error) if compression_error is not None else None
                            ),
                            "native_emission_trace_upper_exact": None,
                            "paid_reserved_synthesis_operator_upper_exact": pair(SYNTHESIS_RESERVE),
                            "prospective_component_sum_with_synthesis_reserve_exact": None,
                            "component_ledger_eligible_for_one_future_registry": False,
                            "missing_component_certificate": str(failure),
                            "complete_preparation_trace_certificate": None,
                            "complete_Clifford_T_cost": None,
                        }
                    )
            except BaseException as failure:
                point.update(
                    terminal_status=(
                        "censored" if isinstance(failure, BudgetCensoredError) else "failed"
                    ),
                    failure_type=type(failure).__name__,
                    failure_message=str(failure),
                )
                raise
            finally:
                create(directory / "attempt.json", point)
        admit()
        create(output / "fixed_nine_assessments.json", assessments)
        if len(points) != 3 or len(assessments) != 9:
            raise AssertionError("The fixed three-bond/three-target inventory differs")
        verify(protocol["frozen_inputs"])
        checked_files = receipt_files(output)
        cpu, wall = time.process_time() - started_cpu, time.monotonic() - started_wall
        if cpu >= CPU_LIMIT or wall >= WALL_LIMIT:
            raise BudgetCensoredError("The fixed terminal component receipt budget was exceeded")
        create(
            output / "summary.json",
            {
                "passed": True,
                "budget_censored": False,
                "local_only": True,
                "new_unique_pytest_cases": TESTS,
                "prior_structural_fixture_counts_added_again": 0,
                "fixed_q10_target_tables": 1,
                "fixed_bond_attempts": points,
                "fixed_bond_target_assessments": len(assessments),
                "native_circuits_completed": sum(
                    point["native_emission_completed"] for point in points
                ),
                "component_rows_eligible_for_future_registry": sum(
                    row["component_ledger_eligible_for_one_future_registry"] for row in assessments
                ),
                "new_synthesis_calls": 0,
                "full_preparation_Clifford_T_error_or_cost": None,
                "actual_dirty_reference_statevectors": sum(
                    point["dirty_reference_inverse_diagnostic_completed"] for point in points
                ),
                "native_dense_full_operators_or_financial_replays": 0,
                "q10_uniform_price_law_certificate_failed_separately": True,
                "source_law_or_financial_ledger_adopted": False,
                "G2_or_G5_or_quantum_advantage_established": False,
                "CPU_seconds": cpu,
                "wall_seconds": wall,
            },
        )
    except BaseException as failure:
        create(
            output / "failure.json",
            {
                "failure_type": type(failure).__name__,
                "message": str(failure),
                "traceback": traceback.format_exc(),
                "completed_fixed_bond_points": points,
            },
        )
        if not (output / "summary.json").exists():
            create(
                output / "summary.json",
                {
                    "passed": False,
                    "local_only": True,
                    "budget_censored": isinstance(failure, BudgetCensoredError),
                    "failure_type": type(failure).__name__,
                    "message": str(failure),
                    "new_synthesis_calls": 0,
                    "full_preparation_Clifford_T_error_or_cost": None,
                    "source_law_or_financial_ledger_adopted": False,
                },
            )
        raise
    finally:
        finish_manifest(output, protocol, checked_files)
    print(
        "Three fixed q10 MPS component attempts retained; "
        "synthesis and price adoption remain separate",
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, default=PROGRAM / "A04_mps_run001")
    args = parser.parse_args()
    (prepare if args.mode == "prepare" else run)(args.output)
