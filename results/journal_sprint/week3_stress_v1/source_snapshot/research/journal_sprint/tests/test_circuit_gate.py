import numpy as np
import pytest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from research.journal_sprint.circuit_gate import amplified_circuit, positive_controls


@pytest.mark.parametrize("depth", [0, 1, 2])
def test_amplification_with_work_qubit(depth):
    circuit = QuantumCircuit(2)
    circuit.ry(0.37, 0)
    circuit.cx(0, 1)
    amplified = amplified_circuit(circuit, 1, depth)
    probability = Statevector(amplified).probabilities([1])[1]
    assert probability == pytest.approx(np.sin((2 * depth + 1) * 0.37 / 2) ** 2)


def test_channels_positive_controls():
    assert positive_controls()["full_cx_depolarization"] == pytest.approx(0.5)


def test_invalid_depth():
    with pytest.raises(ValueError):
        amplified_circuit(QuantumCircuit(2), 1, -1)
