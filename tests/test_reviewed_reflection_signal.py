"""Regression for an interval that touches zero from the negative side."""

import numpy as np
import pytest
from qiskit.quantum_info import Operator

from research.journal_sprint.reflection_centered_signal import ReflectionSignal, signal_circuit
from research.journal_sprint.reviewed_reflection_signal import ReviewedReflectionSignal


def test_negative_constant_endpoint_reproducer():
    original = ReflectionSignal([-1e-80], [[0.]], .5, 1, 1)
    corrected = ReviewedReflectionSignal([-1e-80], [[0.]], .5, 1, 1)
    assert original.constant.lo < 0 and original.constant.hi == 0
    assert not original.negative_constant
    assert corrected.negative_constant
    assert corrected.B_interval.record() == original.B_interval.record()


@pytest.mark.parametrize("mu,strike,negative", [(0., .5, False), (0., .75, True),
                                               (0., .25, False), (-1e-80, .5, True)])
def test_reviewed_signal_projection_and_involution(mu, strike, negative):
    plan = ReviewedReflectionSignal([mu], [[0.]], strike, 1, 1)
    assert plan.negative_constant is negative
    circuit, _ = signal_circuit(plan)
    matrix = Operator(circuit).data
    target = (np.exp(mu)-strike)/plan.B
    np.testing.assert_allclose(matrix[:2, :2], np.eye(2)*target, atol=2e-13)
    np.testing.assert_allclose(matrix, matrix.conj().T, atol=2e-13)
    np.testing.assert_allclose(matrix@matrix, np.eye(len(matrix)), atol=3e-13)
