import math
import numpy as np
import pytest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from research.journal_sprint.week2_explicit_ae import canonical_circuit


@pytest.mark.parametrize('probability',[0.,.03,.2,.5,.81,1.])
def test_canonical_distribution(probability):
    prep = QuantumCircuit(1)
    prep.ry(2*math.asin(math.sqrt(probability)),0)
    qc,meta = canonical_circuit(prep,0,3)
    actual = Statevector.from_instruction(qc).probabilities([0,1,2])
    theta = math.asin(math.sqrt(probability))/math.pi
    y = np.arange(8)
    expected = np.zeros(8)
    for sign in (-1,1):
        delta = sign*theta-y/8
        expected += abs(np.exp(2j*np.pi*np.outer(delta,np.arange(8))).sum(axis=1)/8)**2/2
    np.testing.assert_allclose(actual,expected,atol=1e-12)
    labels = np.sin(np.pi*y/8)**2
    assert actual[abs(labels-probability)<=meta['amplitude_error']].sum()>=8/math.pi**2-1e-12
    assert meta['a_calls']==15


def test_canonical_rejects_unbounded_register():
    with pytest.raises(ValueError):
        canonical_circuit(QuantumCircuit(1),0,0)
