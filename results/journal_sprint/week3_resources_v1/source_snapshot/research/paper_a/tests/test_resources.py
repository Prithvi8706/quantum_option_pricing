import pytest

from research.paper_a.recording import Invocation
from research.paper_a.resources import (
    executed_powers, m_a_executed, m_a_logical, m_q_executed,
    max_executed_depth, shot_weighted_gates,
)


def _inv(ordinal, shots, depth, ops):
    return Invocation(ordinal=ordinal, requested_shots=shots,
                      logical_qpy_sha256="0" * 64, isa_qpy_sha256="1" * 64,
                      isa_depth=depth, isa_ops=ops, effective_shots=shots,
                      status="complete")


def test_leading_sentinel_zero_is_excluded():
    """Qiskit initializes powers=[0] before the loop; that entry was never
    submitted unless an invocation proves it."""
    invocations = [_inv(0, 512, 10, {"cx": 4}), _inv(1, 512, 20, {"cx": 8})]
    assert executed_powers([0, 0, 1], invocations) == [0, 1]


def test_sentinel_kept_when_an_invocation_proves_k_zero_was_submitted():
    invocations = [_inv(i, 512, 10, {"cx": 4}) for i in range(3)]
    assert executed_powers([0, 0, 1], invocations) == [0, 0, 1]


def test_repeated_powers_remain_separate():
    invocations = [_inv(i, 512, 10, {"cx": 4}) for i in range(3)]
    assert executed_powers([0, 2, 2, 2], invocations) == [2, 2, 2]


def test_m_a_logical_is_an_invocation_count_not_a_depth():
    assert m_a_logical([0, 1, 2]) == (2 * 0 + 1) + (2 * 1 + 1) + (2 * 2 + 1)
    assert m_a_logical([0, 1, 2]) == 9


def test_m_a_executed_is_shot_weighted():
    assert m_a_executed([0, 1], [512, 2048]) == 512 * 1 + 2048 * 3


def test_m_q_executed_matches_qiskit_oracle_query_convention():
    """Qiskit accumulates num_oracle_queries += shots * k."""
    assert m_q_executed([0, 1, 3], [512, 512, 1024]) == (
        512 * 0 + 512 * 1 + 1024 * 3)


def test_unweighted_and_weighted_metrics_are_different_quantities():
    powers, shots = [0, 1, 2], [512, 512, 8192]
    assert m_a_logical(powers) != m_a_executed(powers, shots)
    assert m_a_executed(powers, shots) != m_q_executed(powers, shots)


def test_mismatched_lengths_are_rejected():
    with pytest.raises(ValueError):
        m_a_executed([0, 1], [512])


def test_shot_weighted_gate_burden_sums_per_operation():
    invocations = [_inv(0, 512, 10, {"cx": 4, "sx": 6}),
                   _inv(1, 2048, 20, {"cx": 8, "sx": 2})]
    assert shot_weighted_gates(invocations) == {
        "cx": 512 * 4 + 2048 * 8, "sx": 512 * 6 + 2048 * 2}


def test_max_executed_depth_is_the_maximum_not_the_sum():
    invocations = [_inv(0, 512, 10, {}), _inv(1, 512, 37, {}),
                   _inv(2, 512, 22, {})]
    assert max_executed_depth(invocations) == 37


def test_failed_invocations_retain_their_consumed_resources():
    failed = Invocation(ordinal=0, requested_shots=512,
                        logical_qpy_sha256="0" * 64, isa_qpy_sha256="1" * 64,
                        isa_depth=44, isa_ops={"cx": 3}, effective_shots=None,
                        status="failed", exception="boom")
    assert max_executed_depth([failed]) == 44
    assert shot_weighted_gates([failed]) == {}
