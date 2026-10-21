"""Sixteen small error-ledger fixtures; no SVD, SDK or synthesis calls."""

from dataclasses import replace
from fractions import Fraction

import numpy as np
import pytest

from research.limitation_program_20261001.mps_loader_components import (
    SYNTHESIS_RESERVE,
    TARGETS,
    assessment_rows,
    cdf,
    certify_emission,
    certify_rounded_target,
    completion_error_upper,
    exact_contract,
    gauge_distance,
    gram_norm_upper,
    literal,
    literal_vector,
    local_operation_blocks,
    native_local_matrix,
    norm_squared,
    normalized_trace_distance,
    pair,
    save_literals,
    sdk_operator_error_upper,
    sqrt_upper,
    validate_plan_binding,
)
from research.limitation_program_20261001.mps_sequential_structure_v2 import (
    CanonicalMPS,
    Primitive,
    StructurePlan,
    Transition,
)


def one_zero_site():
    core = np.array([[[1.0], [0.0]]], dtype=complex)
    canonical = CanonicalMPS((core,), 1.0, 1 + 0j, 0.0, 0.0)
    columns = core.reshape(1, 2).T
    transition = Transition(0, 0, 1, 1, (0,), None, None, columns, np.eye(2), 0.0, 0.0)
    plan = StructurePlan((transition,), (0,), (), 1, (0,), 1)
    return core, canonical, plan


def records(phase=Fraction(0), slots=0):
    return ({"site": 0, "native_slots": slots, "recorded_global_phase_exact": pair(phase)},)


def test_binary64_literals_are_exact_and_nonfinite_values_rejected():
    value = complex(float.fromhex("0x1.0000000000001p-3"), -0.5)
    assert literal(value) == (Fraction((1 << 52) + 1, 1 << 55), Fraction(-1, 2))
    assert save_literals([value])["binary64_complex_rationals"] == [
        [pair(Fraction((1 << 52) + 1, 1 << 55)), [-1, 2]]
    ]
    for bad in (float("nan"), float("inf"), complex(0, float("inf"))):
        with pytest.raises(ValueError, match="Finite"):
            literal(bad)


def test_exact_tensor_contraction_preserves_msb_order_and_complex_phase():
    first = np.array([[[0, 1j], [1, 0]]], dtype=complex)
    second = np.array([[[1], [0]], [[0], [0.5]]], dtype=complex)
    assert exact_contract((first, second)) == ((0, 0), (0, Fraction(1, 2)), (1, 0), (0, 0))


def test_exact_norm_overlap_and_directed_square_root_guard():
    vector = literal_vector([0.5, 0.5j])
    assert norm_squared(vector) == Fraction(1, 2)
    assert normalized_trace_distance(vector, vector) == (0, 0)
    for value in (Fraction(2), Fraction(1, 7), Fraction(1, 16)):
        bound = sqrt_upper(value)
        assert bound**2 >= value and (bound - Fraction(1, 1 << 256)) ** 2 < value
    with pytest.raises(ValueError, match="Nonnegative"):
        sqrt_upper(-1)


def test_compression_trace_is_scale_phase_invariant_but_gauge_distance_is_not():
    first, phased = literal_vector([1, 0]), literal_vector([2j, 0])
    assert normalized_trace_distance(first, phased) == (0, 0)
    assert gauge_distance(literal_vector([1j, 0]), first) > 1


def test_orthogonal_compression_and_zero_vector_contract():
    assert normalized_trace_distance(literal_vector([1, 0]), literal_vector([0, 1])) == (1, 1)
    with pytest.raises(ValueError, match="Positive"):
        normalized_trace_distance(literal_vector([0, 0]), literal_vector([1, 0]))


def test_probability_and_amplitude_normalization_contracts_are_guarded():
    with pytest.raises(ValueError, match="Matching"):
        certify_rounded_target([(Fraction(1), Fraction(1))], [])
    with pytest.raises(ValueError, match="normalized law"):
        certify_rounded_target([(Fraction(3, 4),) * 2] * 2, [1.0, 1.0])
    with pytest.raises(ValueError, match="Nonnegative"):
        certify_rounded_target([(Fraction(1),) * 2], [-1.0])


def test_cdf_zero_is_exact_and_fixed_domain_is_guarded():
    assert cdf(0) == (Fraction(1, 2),) * 2
    with pytest.raises(ValueError, match="domain"):
        cdf(Fraction(7))


def test_cdf_symmetry_uses_the_same_q10_grid_boundary():
    positive = cdf(Fraction(3, 2))
    assert cdf(Fraction(-3, 2)) == (1 - positive[1], 1 - positive[0])
    assert Fraction(9, 10) < positive[0] <= positive[1] < Fraction(19, 20)


def test_target_literal_normalization_rounding_is_paid():
    result = certify_rounded_target([(Fraction(1, 2),) * 2] * 2, [1.0, 1.0])
    assert result["rounded_target_norm_squared_exact"] == [2, 1]
    assert Fraction(*result["ideal_CDF_to_normalized_literal_target_trace_upper_exact"]) < Fraction(
        1, 10**70
    )
    asymmetric = certify_rounded_target([(Fraction(1, 2),) * 2] * 2, [1.0, 0.5])
    assert Fraction(
        *asymmetric["ideal_CDF_to_normalized_literal_target_trace_upper_exact"]
    ) > Fraction(1, 10)


def test_local_gram_bound_charges_nonorthogonality_without_unitary_predicate():
    epsilon = Fraction(1, 1 << 20)
    columns = np.array([[1, complex(0, float(epsilon))], [0, 1]], dtype=complex)
    bound = gram_norm_upper(columns)
    assert bound**2 >= 1 + epsilon + epsilon**2
    assert gram_norm_upper(np.eye(2)) == 1


def test_completion_active_column_changes_are_exactly_charged():
    columns = np.array([[1], [0]], dtype=complex)
    completed = np.eye(2)
    completed[0, 0] += 2**-20
    assert completion_error_upper(columns, completed) == Fraction(1, 1 << 20)
    with pytest.raises(ValueError, match="Matching"):
        completion_error_upper(columns, np.eye(3))


def test_full_local_identity_and_fresh_emission_have_outward_zero_bounds():
    core, canonical, plan = one_zero_site()
    inverse_pair = (Primitive("ry", (0,), Fraction(1, 7)), Primitive("ry", (0,), Fraction(-1, 7)))
    assert sdk_operator_error_upper(inverse_pair, (0,), np.eye(2)) < Fraction(1, 10**70)
    result = certify_emission((core,), canonical, plan, (), records())
    assert Fraction(*result["compressed_to_exact_native_preparation_trace_upper_exact"]) < Fraction(
        1, 10**70
    )
    assert result["full_SDK_operator_error_is_not_a_single_column_check"]


def test_recorded_sdk_global_phase_is_bound_and_charged_in_full_operator():
    _, _, plan = one_zero_site()
    phase = Fraction(1, 7)
    operation = Primitive("phase", (), phase)
    block = local_operation_blocks(plan, (operation,), records(phase))[0]
    assert sdk_operator_error_upper(block, (0,), np.eye(2)) > Fraction(1, 10)
    with pytest.raises(ValueError, match="global phase"):
        local_operation_blocks(plan, (), records(phase))


def test_native_rotation_wire_arity_and_unknown_gate_are_guarded():
    for operation in (
        Primitive("ry", (), Fraction(0)),
        Primitive("cx", (0, 0)),
        Primitive("ry", (2,), Fraction(0)),
        Primitive("h", (0,)),
    ):
        with pytest.raises(ValueError):
            native_local_matrix((operation,), (0,))


def test_exact_structure_and_saved_core_binding_reject_wire_and_column_forgery():
    _, canonical, plan = one_zero_site()
    assert validate_plan_binding(canonical, plan)
    with pytest.raises(ValueError, match="structure"):
        validate_plan_binding(canonical, replace(plan, output_wires_msb_first=(1,)))
    columns = plan.transitions[0].isometry_columns.copy()
    columns[0, 0] += 2**-20
    forged = replace(plan.transitions[0], isometry_columns=columns)
    with pytest.raises(ValueError, match="transition"):
        validate_plan_binding(canonical, replace(plan, transitions=(forged,)))


def test_fixed_targets_pay_synthesis_reserve_and_keep_complete_costs_null():
    rows = assessment_rows(8, Fraction(0), Fraction(0), Fraction(0), 4096)
    assert len(rows) == 3 and all(
        row["component_ledger_eligible_for_one_future_registry"] for row in rows
    )
    assert [row["scalar_target_exact"] for row in rows] == list(map(pair, TARGETS))
    assert all(
        row["paid_reserved_synthesis_operator_upper_exact"] == pair(SYNTHESIS_RESERVE)
        for row in rows
    )
    assert rows[0]["conditional_disjoint_factor_budget_rows"][1][
        "prospective_preparation_dollars_with_synthesis_reserve_exact"
    ] == pair(40 * 468 * SYNTHESIS_RESERVE)
    assert all(
        row["complete_preparation_trace_certificate"] is None
        and row["complete_Clifford_T_cost"] is None
        and row["q10_continuous_price_law_certificate_passed"] is False
        for row in rows
    )
    assert not any(
        row["component_ledger_eligible_for_one_future_registry"]
        for row in assessment_rows(8, Fraction(0), Fraction(0), Fraction(0), 4097)
    )
