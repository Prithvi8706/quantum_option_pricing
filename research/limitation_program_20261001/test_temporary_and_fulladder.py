"""Phase-sensitive channel, measurement, dirty-output and control fixtures."""

from dataclasses import replace

import numpy as np
import pytest

from research.limitation_program_20261001.temporary_and_fulladder import (
    and_compute,
    ccx_seven_t,
    channel_certificate,
    decode,
    encode,
    expected_logical_permutation,
    fulladder_schedule,
    logical_injection,
    resources,
    run_columns,
)


@pytest.mark.parametrize("a,b", [(0, 0), (0, 1), (1, 0), (1, 1)])
def test_temporary_and_has_exact_fresh_target_isometry_phase(a, b):
    column = np.zeros((128, 1), dtype=np.complex128)
    column[a | (b << 1)] = 1
    actual = run_columns(and_compute(0, 1, 5), column)
    expected = np.zeros_like(column)
    expected[a | (b << 1) | ((a & b) << 5)] = 1
    assert np.max(np.abs(actual - expected)) < 1e-12


def test_paid_seven_t_ccx_is_full_unitary_on_all_eight_columns():
    initial = np.zeros((128, 8), dtype=np.complex128)
    initial[:8] = np.eye(8)
    expected = np.zeros_like(initial)
    for word in range(8):
        expected[word ^ (((word & 1) & ((word >> 1) & 1)) << 2), word] = 1
    actual = run_columns(ccx_seven_t(0, 1, 2), initial)
    assert np.max(np.abs(actual - expected)) < 1e-12


@pytest.mark.parametrize("outcomes", [(0, 0), (0, 1), (1, 0), (1, 1)])
def test_every_branch_preserves_all_dirty_outputs_and_relative_input_phases(outcomes):
    actual = run_columns(fulladder_schedule(measured=True), logical_injection(), outcomes)
    target = logical_injection() @ expected_logical_permutation() / 2
    assert np.max(np.abs(actual - target)) < 1e-12
    assert np.max(np.abs(actual.conj().T @ actual - np.eye(32) / 4)) < 1e-12
    assert np.max(np.abs(actual[32:])) < 1e-12


def test_full_channel_including_reference_entanglement_and_arbitrary_superposition():
    operations = fulladder_schedule(measured=True)
    certificate, kraus = channel_certificate(operations)
    assert certificate[
        "arbitrary_superposition_and_entangled_reference_follows_from_Kraus_identity"
    ]
    # Deterministic nonuniform complex state entangled with a three-state reference.
    state = np.asarray(
        [[complex(i + j + 1, (i * 5 - j * 3) % 7) for j in range(3)] for i in range(32)]
    )
    state /= np.linalg.norm(state)
    expected = expected_logical_permutation() @ state
    for branch in kraus:
        actual = branch @ state
        assert np.max(np.abs(actual - expected / 2)) < 1e-12
        assert abs(np.linalg.norm(actual) ** 2 - 0.25) < 1e-12


def test_actual_unitary_control_has_same_full_dirty_output_channel():
    actual = run_columns(fulladder_schedule(measured=False), logical_injection())
    expected = logical_injection() @ expected_logical_permutation()
    assert np.max(np.abs(actual - expected)) < 1e-12


def test_basis_truth_table_does_not_hide_missing_control_phase_correction():
    operations = [op for op in fulladder_schedule(measured=True) if op.gate != "CZ"]
    actual = run_columns(operations, logical_injection(), (1, 1))
    expected = logical_injection() @ expected_logical_permutation() / 2
    assert np.max(np.abs(np.abs(actual) - np.abs(expected))) < 1e-12
    with pytest.raises(AssertionError):
        channel_certificate(operations)


def test_fresh_target_phase_correction_is_required_despite_correct_classical_and():
    operations = [op for op in fulladder_schedule(measured=True) if op.gate != "Sdg"]
    actual = run_columns(operations, logical_injection(), (0, 0))
    expected = logical_injection() @ expected_logical_permutation() / 2
    assert np.max(np.abs(np.abs(actual) - np.abs(expected))) < 1e-12
    with pytest.raises(AssertionError):
        channel_certificate(operations)


def test_schedule_roundtrip_charges_all_measurement_feedback_and_reset_slots():
    operations = fulladder_schedule(measured=True)
    assert decode(encode(operations)) == operations
    cost = resources(operations)
    assert cost["T_count"] == 8 and cost["T_depth"] == 8
    assert cost["X_basis_measurements"] == 2
    assert cost["conditional_CZ_scheduled_slots"] == 2
    assert cost["conditional_X_reset_scheduled_slots"] == 2
    assert cost["fresh_scratch_qubits"] == 2
    assert cost["physical_measurement_feedback_reset_seconds"] is None
    assert resources(fulladder_schedule(measured=False))["T_count"] == 28


def test_forward_feedback_is_rejected_before_corresponding_measurement():
    operations = fulladder_schedule(measured=True)
    conditional = next(op for op in operations if op.gate == "CZ")
    with pytest.raises(ValueError, match="earlier actual measurement"):
        run_columns([conditional] + operations, logical_injection())
    with pytest.raises(ValueError, match="outcome-one"):
        replace(conditional, condition_value=0)
