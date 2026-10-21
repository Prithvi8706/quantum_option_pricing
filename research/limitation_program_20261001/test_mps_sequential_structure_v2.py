"""Sixteen fixed structural fixtures, one toy SDK emission, no Gaussian runs."""

from fractions import Fraction
import json
import math
import os
from pathlib import Path

import numpy as np
import pytest

from research.limitation_program_20261001.mps_sequential_structure_v2 import (
    Primitive,
    apply_local_matrix,
    apply_operations,
    apply_structure,
    complete_isometry,
    contract_mps,
    decompose_plan,
    inverse_operations,
    make_structure_plan,
    right_canonicalize,
    structure_diagnostics,
    transition_from_core,
    validate_cores,
)


def fixed_toy_cores():
    # Fixed exact dyadic Fourier columns with a genuine global i phase, then
    # one fixed sqrt(2)-scaled two-dimensional unitary. No random observations.
    fourier = np.array(
        [[1, 1, 1, 1], [1, 1j, -1, -1j], [1, -1, 1, -1], [1, -1j, -1, 1j]],
        dtype=complex,
    ) / 2
    final = np.array([[1, 1j], [1j, 1]], dtype=complex) / math.sqrt(2)
    return (
        (1j * fourier[:, :1]).T.reshape(1, 2, 2),
        fourier[:, :2].T.reshape(2, 2, 2),
        final.T.reshape(2, 2, 1),
    )


def literal_matrix(matrix):
    return [
        [[float(value.real).hex(), float(value.imag).hex()] for value in row]
        for row in np.asarray(matrix)
    ]


def literal_operation(operation):
    return {
        "gate": operation.gate,
        "wires": list(operation.wires),
        "angle_exact": None if operation.angle is None else [
            operation.angle.numerator, operation.angle.denominator,
        ],
    }


@pytest.fixture(scope="module")
def emitted_toy():
    cores = fixed_toy_cores()
    canonical = right_canonicalize(cores)
    plan = make_structure_plan(canonical)
    operations, local_records = decompose_plan(
        plan, maximum_local_calls=3, maximum_operations=4096,
    )
    destination = os.environ.get("A04_MPS_STRUCTURE_EVIDENCE_PATH")
    if destination:
        evidence = {
            "one_fixed_nonfinancial_toy": True,
            "physical_outputs": 3,
            "bond_path": [1, 2, 2, 1],
            "actual_local_SDK_calls": 3,
            "original_cores_binary64_hex": [
                {"shape": list(core.shape),
                 "entries": literal_matrix(core.reshape(core.shape[0], -1))}
                for core in cores
            ],
            "canonical_cores_binary64_hex": [
                {"shape": list(core.shape),
                 "entries": literal_matrix(core.reshape(core.shape[0], -1))}
                for core in canonical.cores
            ],
            "initial_normalizer_binary64_hex": canonical.initial_normalizer.hex(),
            "final_gauge_scalar_binary64_hex": [
                canonical.final_gauge_scalar.real.hex(), canonical.final_gauge_scalar.imag.hex(),
            ],
            "canonical_reconstruction_residual_numeric": canonical.reconstruction_residual_numeric,
            "row_isometry_defect_numeric": canonical.maximum_row_isometry_defect_numeric,
            "transitions": [
                {
                    "site": item.site, "output_wire": item.output_wire,
                    "left_rank": item.left_rank, "right_rank": item.right_rank,
                    "local_wires": list(item.local_wires),
                    "swap_before": item.swap_before,
                    "newly_cleared_wire": item.newly_cleared_wire,
                    "matrix_binary64_hex": literal_matrix(item.matrix),
                    "isometry_columns_binary64_hex": literal_matrix(item.isometry_columns),
                    "completion_change_numeric": item.completion_change_numeric,
                    "unitary_defect_numeric": item.unitary_defect_numeric,
                }
                for item in plan.transitions
            ],
            "forward_operations": list(map(literal_operation, operations)),
            "literal_inverse_operations": list(
                map(literal_operation, inverse_operations(operations))
            ),
            "local_SDK_records": local_records,
            "diagnostics": structure_diagnostics(plan, operations),
            "numerical_diagnostics_are_rigorous_error_bounds": False,
            "Gaussian_target_error_or_synthesis_error_certificate": None,
        }
        with Path(destination).open("x", encoding="utf-8") as handle:
            json.dump(evidence, handle, indent=2, allow_nan=False)
            handle.write("\n")
    return canonical, plan, operations


def independent_dense_gate(operation, n):
    # Separate basis-action construction; no production replay or local helper.
    if operation.gate == "phase":
        return np.exp(1j * float(operation.angle)) * np.eye(1 << n, dtype=complex)
    matrix = np.zeros((1 << n, 1 << n), dtype=complex)
    if operation.gate in ("ry", "rz"):
        theta = float(operation.angle)
        local = (
            np.array([[np.cos(theta / 2), -np.sin(theta / 2)],
                      [np.sin(theta / 2), np.cos(theta / 2)]], dtype=complex)
            if operation.gate == "ry"
            else np.diag([np.exp(-1j * theta / 2), np.exp(1j * theta / 2)])
        )
        wire = operation.wires[0]
        for column in range(1 << n):
            source_bit = (column >> wire) & 1
            for destination_bit in (0, 1):
                row = (column & ~(1 << wire)) | (destination_bit << wire)
                matrix[row, column] = local[destination_bit, source_bit]
    else:
        a, b = operation.wires
        for column in range(1 << n):
            row = column
            if operation.gate == "cx" and column & (1 << a):
                row ^= 1 << b
            elif operation.gate == "swap" and ((column >> a) & 1) != ((column >> b) & 1):
                row ^= (1 << a) | (1 << b)
            matrix[row, column] = 1
    return matrix


def test_contraction_uses_most_significant_site_first():
    first = np.array([[[0], [1j]]], dtype=complex)
    second = np.array([[[1], [0]]], dtype=complex)
    assert np.array_equal(contract_mps((first, second)), [0, 0, 1j, 0])


def test_boundary_bond_dimension_must_be_one():
    with pytest.raises(ValueError, match="Consecutive"):
        validate_cores((np.ones((2, 2, 1)),))
    with pytest.raises(ValueError, match="final bond"):
        validate_cores((np.ones((1, 2, 2)),))


def test_nonpower_rank_and_rank_jumps_are_rejected_without_adaptation():
    with pytest.raises(ValueError, match="power-of-two"):
        validate_cores((np.ones((1, 2, 3)), np.ones((3, 2, 1))))
    with pytest.raises(ValueError, match="factor of two"):
        validate_cores((np.ones((1, 2, 4)), np.ones((4, 2, 1))))


def test_nonfinite_core_literals_are_rejected():
    for value in (np.nan, np.inf, complex(0, np.inf)):
        with pytest.raises(ValueError, match="finite"):
            validate_cores((np.full((1, 2, 1), value),))


def test_right_canonical_rows_and_one_fixed_normalization():
    cores = list(fixed_toy_cores())
    cores[0] = 3 * cores[0]
    canonical = right_canonicalize(cores)
    assert abs(canonical.initial_normalizer - 3) < 1e-14
    assert canonical.maximum_row_isometry_defect_numeric < 1e-13
    assert canonical.reconstruction_residual_numeric < 1e-13
    assert abs(canonical.final_gauge_scalar - 1) < 1e-13


def test_complex_preparation_phase_is_preserved_in_right_canonical_cores():
    original = contract_mps(fixed_toy_cores())
    canonical = right_canonicalize(fixed_toy_cores())
    assert np.linalg.norm(contract_mps(canonical.cores) - original) < 1e-13
    assert np.linalg.norm(contract_mps(canonical.cores) - original / 1j) > 1


def test_expand_transition_columns_use_low_bond_bits_then_output():
    # One matrix-only 2->4 expansion; no extra SDK call or candidate.
    columns = np.eye(8, dtype=complex)[:, [5, 2]]
    core = columns.T.reshape(2, 2, 4)
    transition = transition_from_core(core, 0, 0, (1, 2))
    assert transition.local_wires == (1, 2, 0) and transition.swap_before is None
    assert np.linalg.norm(transition.matrix[:, :2] - columns) < 1e-13
    for alpha, expected_local in enumerate((5, 2)):
        initial = np.zeros(8, dtype=complex)
        initial[alpha << 1] = 1
        actual = apply_local_matrix(initial, transition.matrix, transition.local_wires, 3)
        physical = ((expected_local & 1) << 1) | (((expected_local >> 1) & 1) << 2)
        physical |= (expected_local >> 2) & 1
        assert abs(actual[physical] - 1) < 1e-13


def test_equal_rank_transition_has_no_swap_or_extra_memory_lane():
    core = fixed_toy_cores()[1]
    transition = transition_from_core(core, 1, 0, (1, 2))
    assert transition.local_wires == (1, 0)
    assert transition.swap_before is None and transition.newly_cleared_wire is None
    assert np.linalg.norm(transition.matrix[:, :2] - core.reshape(2, 4).T) < 1e-13


def test_shrink_swap_clears_retired_bond_even_when_entangled_with_reference():
    columns = np.eye(4, dtype=complex)[:, [2, 0, 3, 1]]
    transition = transition_from_core(columns.T.reshape(4, 2, 2), 0, 0, (1, 2))
    assert transition.swap_before == (2, 0)
    assert transition.local_wires == (1, 0) and transition.newly_cleared_wire == 2
    initial = np.zeros(16, dtype=complex)
    initial[0] = initial[(1 << 2) | (1 << 3)] = 1 / math.sqrt(2)
    swapped = apply_operations(initial, (Primitive("swap", transition.swap_before),), 4)
    final = apply_local_matrix(swapped, transition.matrix, transition.local_wires, 4)
    assert np.array_equal(final[np.arange(16) & (1 << 2) != 0], np.zeros(8))
    assert abs(np.linalg.norm(final) - 1) < 1e-13


def test_fresh_output_cannot_alias_any_bond_wire():
    with pytest.raises(ValueError, match="distinct"):
        transition_from_core(fixed_toy_cores()[1], 1, 1, (1,))


def test_zero_state_and_dependent_isometry_are_rejected():
    with pytest.raises(ValueError, match="normalization"):
        right_canonicalize((np.zeros((1, 2, 1)),))
    with pytest.raises(ValueError, match="dependent"):
        complete_isometry(np.ones((4, 2), dtype=complex))


def test_full_toy_emission_prepares_state_with_exact_structural_scratch_zero(emitted_toy):
    canonical, plan, operations = emitted_toy
    initial = np.zeros(1 << plan.num_wires, dtype=complex)
    initial[0] = 1
    actual = apply_operations(initial, operations, plan.num_wires)
    count = 1 << len(plan.output_wires_msb_first)
    assert np.array_equal(actual[count:], np.zeros(len(actual) - count))
    assert np.linalg.norm(actual[:count] - contract_mps(canonical.cores)) < 1e-11
    assert np.linalg.norm(actual - apply_structure(initial, plan)) < 1e-11


def test_independent_dense_full_operator_matches_all_emitted_local_columns(emitted_toy):
    _, plan, operations = emitted_toy
    size = 1 << plan.num_wires
    native = np.eye(size, dtype=complex)
    for operation in operations:
        native = independent_dense_gate(operation, plan.num_wires) @ native
    direct = np.column_stack([
        apply_structure(np.eye(size, dtype=complex)[:, column], plan)
        for column in range(size)
    ])
    assert np.linalg.norm(native - direct) < 1e-10


def test_literal_inverse_restores_dirty_register_entangled_with_reference(emitted_toy):
    _, plan, operations = emitted_toy
    # Arbitrary deterministic complex coefficients over all dirty wire states
    # and an additional untouched reference; this is not a financial sample.
    size = 1 << (plan.num_wires + 1)
    initial = np.array([complex(index + 1, (7 * index + 3) % 19) for index in range(size)])
    initial /= np.linalg.norm(initial)
    forward = apply_operations(initial, operations, plan.num_wires + 1)
    restored = apply_operations(forward, inverse_operations(operations), plan.num_wires + 1)
    assert np.linalg.norm(restored - initial) < 1e-11
    assert len(inverse_operations(operations)) == len(operations)


def test_tracked_global_phase_is_paid_in_the_operator_comparison():
    operations = (Primitive("phase", (), Fraction(1, 3)), Primitive("ry", (0,), Fraction(1, 5)))
    initial = np.array([1, 0], dtype=complex)
    full = apply_operations(initial, operations, 1)
    omitted = apply_operations(initial, operations[1:], 1)
    assert np.linalg.norm(full - omitted) > 0.3
    restored = apply_operations(full, inverse_operations(operations), 1)
    assert np.linalg.norm(restored - initial) < 1e-14


def test_fixed_local_call_cap_rejects_before_any_additional_sdk_call(emitted_toy):
    _, plan, _ = emitted_toy
    with pytest.raises(ValueError, match="call cap"):
        decompose_plan(plan, maximum_local_calls=2, maximum_operations=4096)
    report = structure_diagnostics(plan, ())
    assert report["Gaussian_target_or_q10_price_law_adopted"] is False
    assert report["rounded_core_or_completion_operator_error_certificate"] is None
    assert report["Clifford_T_synthesis_error_or_cost"] is None
