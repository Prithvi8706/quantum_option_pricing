import math
import numpy as np
import pytest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
from research.journal_sprint.reflection_centered_signal import (
    ReflectionSignal, signal_circuit, phased_circuit, mux_rounding, prep_tree)
from research.journal_sprint.decimal_enclosure import Interval as I
from research.journal_sprint.combined_qsp import response


def exact_block(plan):
    values = []
    for word in range(1 << plan.path_qubits):
        z = [plan.nodes[j,(word >> (j*plan.q)) & ((1 << plan.q)-1)] for j in range(plan.d)]
        values.append((np.exp(plan.means+plan.factor@z).mean()-plan.strike)/plan.B)
    return np.array(values)


@pytest.mark.parametrize('mode',['reflection','original'])
@pytest.mark.parametrize('d,q',[(1,1),(1,2),(2,1),(2,2)])
def test_full_operator(mode,d,q):
    p = ReflectionSignal([.1,-.2][:d],np.array([[.3,-.15],[-.2,.25]])[:d,:d],.8,q,1.5,mode)
    qc,cert = signal_circuit(p)
    u = Operator(qc).data
    n = 1 << p.path_qubits
    assert float(cert['operator_error_upper']) < 1e-12
    np.testing.assert_allclose(u.conj().T,u,atol=2e-13)
    np.testing.assert_allclose(u@u,np.eye(len(u)),atol=3e-13)
    np.testing.assert_allclose(u[:n,:n],np.diag(exact_block(p)),atol=2e-13)
    phases = [.3,-.2,.4]
    phased = Operator(phased_circuit(p,qc,phases)).data[:n,:n]
    np.testing.assert_allclose(phased,np.diag(response(exact_block(p),phases)),atol=5e-13)


@pytest.mark.parametrize('strike',[0.,.1,1.,10.])
def test_positive_negative_constant_and_controls(strike):
    p = ReflectionSignal([.1],[[.3]],strike,1,1.5)
    qc,_ = signal_circuit(p)
    u = Operator(qc).data
    test = QuantumCircuit(p.num_qubits+1)
    test.append(qc.to_gate().control(),[p.num_qubits]+list(range(p.num_qubits)))
    actual = Operator(test).data
    expected = np.zeros_like(actual)
    n = len(u)
    expected[:n,:n] = np.eye(n)
    expected[n:,n:] = u
    np.testing.assert_allclose(actual,expected,atol=1e-12)
    np.testing.assert_allclose(u[:2,:2],np.diag(exact_block(p)),atol=1e-13)


def test_zero_factors_endpoints_and_exact_zero_constant():
    p = ReflectionSignal([0.],[[0.]],.5,1,2,nodes=[-2,2])
    qc,_ = signal_circuit(p)
    np.testing.assert_allclose(Operator(qc).data[:2,:2],np.eye(2),atol=1e-13)


def test_scale_algebra_and_dimension_growth():
    for d in (1,2,4,8,16):
        p = ReflectionSignal(np.zeros(d),np.eye(d)*.2,.7,10,4)
        C = math.exp(.8)
        assert p.B == pytest.approx(max(.7,C-.7))
        assert p.metadata()['coefficient_slots'] == d+1
        assert p.metadata()['padded_mux_entries'] < 2*d*(d+1)*1024
        assert not p.metadata()['joint_path_table']


def test_mux_certificate_and_zero_mass():
    err = mux_rounding([.1,.2,.3,.4])
    assert 0 <= float(err.hi) < 1e-15
    qc,error,_ = prep_tree([I(1),I(0),I(0),I(0)])
    assert float(error.hi) < 1e-12
    np.testing.assert_allclose(Operator(qc).data[:,0],[1,0,0,0],atol=1e-13)


@pytest.mark.parametrize('q,d,mode',[(0,1,'reflection'),(11,1,'reflection'),
                                  (1,17,'reflection'),(1,1,'wrong')])
def test_invalid(q,d,mode):
    with pytest.raises(ValueError):
        ReflectionSignal(np.zeros(d),np.eye(d),1,q,4,mode)
