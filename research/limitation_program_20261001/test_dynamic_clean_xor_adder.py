"""Fixed w2 dirty-output, phase, reset, entanglement and lifetime fixtures."""

import numpy as np
import pytest

from research.limitation_program_20261001.dynamic_clean_xor_adder import (
    arbitrary_width_lemma,
    direct_schedule,
    exact_fixed_contract,
    expected_permutation,
    logical_injection,
    measured_schedule,
    resources,
    run_columns,
    validate_array,
)


@pytest.mark.parametrize("outcome", (0, 1))
def test_all64_dirty_output_columns_have_exact_phase_contract_and_clean_scratch(outcome):
    actual = run_columns(measured_schedule(), logical_injection(), outcome)
    assert np.max(np.abs(actual[:64] - expected_permutation() / np.sqrt(2))) < 1e-12
    assert np.max(np.abs(actual[64:])) < 1e-12
    assert np.max(np.abs(actual.conj().T @ actual - np.eye(64) / 2)) < 1e-12


def test_nonuniform_entangled_reference_is_preserved_by_each_unnormalized_branch():
    state = np.asarray(
        [[complex(i + j + 1, (i * 3 - j) % 11) for j in range(5)] for i in range(64)]
    )
    state /= np.linalg.norm(state)
    injection = logical_injection() @ state
    target = expected_permutation() @ state
    for outcome in (0, 1):
        actual = run_columns(measured_schedule(), injection, outcome)
        assert np.max(np.abs(actual[:64] - target / np.sqrt(2))) < 1e-12
        assert np.max(np.abs(actual[64:])) < 1e-12
        assert abs(np.linalg.norm(actual) ** 2 - 0.5) < 1e-12


def test_actual_direct7_t_control_has_same_clean_xor_contract_without_fresh_scratch_use():
    actual = run_columns(direct_schedule(), np.eye(1024, dtype=np.complex128))
    assert np.max(np.abs(actual - np.kron(np.eye(16), expected_permutation()))) < 1e-12
    assert set(int(wire) for row in direct_schedule() for wire in row[1:3] if wire >= 0) == set(
        range(6)
    )


def test_exact_proof_and_fixed_resource_counts_do_not_credit_native72():
    proof = exact_fixed_contract(measured_schedule(), direct_schedule())
    assert len(proof["exact_all64_dirty_output_columns"]) == 64
    assert not proof["formal_proof_uses_floating_tolerance"]
    paid, control = (
        resources(measured_schedule(), measured=True),
        resources(direct_schedule(), measured=False),
    )
    assert (
        paid["T_count"],
        paid["fixed_serial_operation_slots"],
        paid["X_basis_measurements"],
    ) == (4, 27, 1)
    assert (
        control["T_count"],
        control["fixed_serial_operation_slots"],
        control["fresh_scratch_required"],
    ) == (7, 19, 0)
    assert arbitrary_width_lemma()["no_native72_resources_credited"]


def test_forward_channel_realizes_adjoint_with_fresh_scratch_without_reversing_measurements():
    target = expected_permutation()
    assert np.array_equal(target @ target, np.eye(64))
    branches = [run_columns(measured_schedule(), logical_injection(), bit)[:64] for bit in (0, 1)]
    for left in branches:
        for right in branches:
            assert np.max(np.abs(left @ right - np.eye(64) / 2)) < 1e-12


def test_early_p_erasure_is_not_a_valid_cleanup_lifetime_reordering():
    array = measured_schedule()
    # Erase p0 before its copied sum bit: this changes the full output contract.
    forged = np.concatenate((array[:15], array[25:], array[15:25]))
    actual = run_columns(forged, logical_injection(), 1)
    assert np.max(np.abs(actual[:64] - expected_permutation() / np.sqrt(2))) > 0.1
    with pytest.raises(AssertionError):
        exact_fixed_contract(forged, direct_schedule())


def test_generic_emission_and_feedback_before_measurement_are_rejected():
    with pytest.raises(ValueError):
        measured_schedule(72)
    forged = measured_schedule()
    forged[[19, 21]] = forged[[21, 19]]
    with pytest.raises(ValueError):
        validate_array(forged)
