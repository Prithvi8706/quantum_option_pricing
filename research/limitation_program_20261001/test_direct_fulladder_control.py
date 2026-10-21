"""Phase, dirty-output, scratch, adjoint and honest-cost comparator fixtures."""

import numpy as np
import pytest

from research.limitation_program_20261001.direct_fulladder_control import (
    direct_schedule,
    exact_direct_contract,
    literal_adjoint_array,
)
from research.limitation_program_20261001.temporary_and_fulladder import (
    decode,
    encode,
    expected_logical_permutation,
    resources,
    run_columns,
)


def test_actual_direct_control_is_full_unitary_on_all128_columns_including_dirty_scratch():
    operations = direct_schedule()
    actual = run_columns(operations, np.eye(128, dtype=np.complex128))
    target = np.kron(np.eye(4), expected_logical_permutation())
    assert np.max(np.abs(actual - target)) < 1e-12


def test_exact_cyclotomic_proof_covers_full_dirty_target_and_boolean_contract():
    proof = exact_direct_contract(encode(direct_schedule()))
    assert len(proof["exact_dirty_target_CCX_columns"]) == 8
    assert len(proof["exact_dirty_sum_carry_permutation"]) == 32
    assert proof["forward_unitary_preserves_relative_phases_exactly"]
    assert proof["arbitrary_unused_scratch_preserved"]


def test_literal_adjoint_cancels_full_unitary_on_nonuniform_complex_entangled_columns():
    array = encode(direct_schedule())
    state = np.asarray(
        [[complex(i + j + 1, (i * 5 - j) % 7) for j in range(3)] for i in range(128)]
    )
    state /= np.linalg.norm(state)
    forward = run_columns(decode(array), state)
    inverse = run_columns(decode(literal_adjoint_array(array)), forward)
    assert np.max(np.abs(inverse - state)) < 1e-12


def test_cost_has_two_actual_seven_t_ccx_and_no_measurement_or_fresh_scratch_use():
    operations = direct_schedule()
    paid = resources(operations)
    assert paid["T_count"] == 14 and paid["fixed_serial_operation_slots"] == 34
    assert paid["X_basis_measurements"] == 0
    assert paid["conditional_CZ_scheduled_slots"] == 0
    assert paid["conditional_X_reset_scheduled_slots"] == 0
    assert set(wire for op in operations for wire in op.wires) == set(range(5))


def test_adjoint_refuses_measurement_and_exact_contract_refuses_phase_forgery():
    forged = encode(direct_schedule())
    forged[0, 0] = 7
    with pytest.raises(ValueError):
        literal_adjoint_array(forged)
    forged = encode(direct_schedule())
    forged[2, 0] = 2
    with pytest.raises(AssertionError):
        exact_direct_contract(forged)
