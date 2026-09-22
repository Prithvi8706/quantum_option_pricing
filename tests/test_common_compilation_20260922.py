"""Meaningful small-unitary and independent composition tests for common policy."""

import numpy as np
import pytest
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Operator

from research.common_compilation_20260922.compiler import (
    Profile,
    ae_profile,
    arithmetic_profile,
    compile_block,
    controlled,
    explicit_control,
)
from research.journal_sprint.week2_pipeline import controlled_zero


@pytest.mark.parametrize(
    "angles,phase",
    [
        ((0.0, 0.0, 0.0), 0.0),
        ((0.71, -0.93, 2.31), 0.37),
        ((-1.9, 0.2, -0.8), -1.17),
        ((np.pi, np.pi / 2, -np.pi / 3), np.pi),
    ],
)
def test_controlled_policy_preserves_full_unitary_and_phase(angles, phase):
    circuit = QuantumCircuit(2)
    circuit.global_phase = phase
    circuit.u(*angles, 0)
    circuit.cx(0, 1)
    circuit.u(0.11, -0.37, 0.29, 1)
    native = transpile(circuit, basis_gates=["u", "cx"], optimization_level=0)
    for block in (native, native.inverse()):
        block = transpile(block, basis_gates=["u", "cx"], optimization_level=0)
        actual = explicit_control(block)
        expected = QuantumCircuit(3)
        expected.append(block.to_gate().control(), [0, 1, 2])
        assert np.max(np.abs(Operator(actual).data - Operator(expected).data)) < 2e-14
        assert compile_block(actual) == controlled(compile_block(block))


def test_arithmetic_decomposition_and_inverse():
    circuit = QuantumCircuit(3)
    circuit.x(0)
    circuit.cx(0, 1)
    circuit.ccx(0, 1, 2)
    expected = arithmetic_profile(dict(x=1, cx=1, ccx=1))
    assert expected == Profile(10, 7)
    assert compile_block(circuit) == compile_block(circuit.inverse()) == expected


def test_controlled_zero_has_right_phase_and_clean_workspace():
    circuit = controlled_zero(3)
    matrix = Operator(circuit).data
    # targets bits 0..2, control bit 3, clean helper bit 4.
    for word in range(16):
        expected = -1 if word == 8 else 1
        assert abs(matrix[word, word] - expected) < 1e-12
        assert np.linalg.norm(np.delete(matrix[:, word], word)) < 1e-12


def test_ae_composition_includes_swaps_global_sign_and_hadamards():
    a, zero = Profile(13, 7), Profile(19, 11)
    # M=8, m=3: initial phase H=3U, IQFT=12U+9CX.
    # Each cancelled iterate:2A + zero + CZ(2U,1CX)+global sign(1U).
    assert ae_profile(a, zero, 8, 3, True) == Profile(
        3 * (13 + 3 + 7 * (26 + 19 + 3) + 12), 3 * (7 + 7 * (14 + 11 + 1) + 9)
    )
    ca = controlled(a)
    assert ae_profile(a, zero, 8, 3, False).cx == 3 * (7 + 7 * (2 * ca.cx + 12) + 9)


@pytest.mark.parametrize("size", [0, 1, 3, 6, True])
def test_invalid_ae_size(size):
    with pytest.raises(ValueError):
        ae_profile(Profile(), Profile(), size, 17, True)


def test_inverse_and_control_cancellation_unitaries():
    a = QuantumCircuit(2)
    a.global_phase = 0.39
    a.u(0.7, -0.2, 1.3, 0)
    a.cx(0, 1)
    ordinary = QuantumCircuit(3)
    ordinary.append(a.to_gate().control(), [0, 1, 2])
    ordinary.cz(0, 2)
    ordinary.append(a.inverse().to_gate().control(), [0, 1, 2])
    cancelled = QuantumCircuit(3)
    cancelled.compose(a, [1, 2], inplace=True)
    cancelled.cz(0, 2)
    cancelled.compose(a.inverse(), [1, 2], inplace=True)
    assert np.max(np.abs(Operator(ordinary).data - Operator(cancelled).data)) < 2e-14
