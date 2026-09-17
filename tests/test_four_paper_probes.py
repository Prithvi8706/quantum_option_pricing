import copy
import numpy as np
import pytest
from qiskit import transpile
from qiskit.quantum_info import Operator, Statevector
from research.journal_sprint.normal_loader_budget import loader_plan, circuit
from research.journal_sprint.four_paper_probes import (
    folded_loader, folded_rounding_bound, geometric, geometric_product,
    walsh_branch, branch_metrics, normal_probabilities, multiplexer)


@pytest.mark.parametrize('q', [1,2,3,4])
def test_entire_controlled_unitary_and_inverse(q):
    plan = loader_plan(q)
    a, b = circuit(plan), folded_loader(plan)
    assert np.max(abs(Operator(a).data-Operator(b).data)) < 2e-13
    assert np.max(abs(Operator(a.to_gate().control()).data-
                         Operator(b.to_gate().control()).data)) < 3e-13
    identity = b.compose(b.inverse())
    assert np.max(abs(Operator(identity).data-np.eye(1<<q))) < 2e-13
    assert folded_rounding_bound(plan)['operator_error_upper'] < 1e-13


@pytest.mark.parametrize('q', [1,2,3,4,5,6])
def test_state_and_gate_bound(q):
    plan = loader_plan(q)
    qc = folded_loader(plan)
    assert np.max(abs(Statevector(qc).data-np.sqrt(normal_probabilities(q)))) < 2e-13
    native = transpile(qc,basis_gates=['ry','cx'],optimization_level=0)
    assert native.count_ops().get('cx',0) <= (1<<q)-2


@pytest.mark.parametrize('a', [-3,-.1,0,.1,3])
def test_geometric_and_inclusive_endpoint(a):
    p = geometric(5,a)
    assert np.max(abs(p-geometric_product(5,a))) < 2e-14
    lo, hi = 3, 10
    sub = p[lo:hi+1]/p[lo:hi+1].sum()
    assert len(sub) == 8  # Cardinality, not hi-lo, is the power of two.
    for x in range(lo,hi+1):
        if a == 0:
            closed = (x-lo+1)/(hi-lo+1)
        else:
            closed = np.expm1(a*(x-lo+1))/np.expm1(a*(hi-lo+1))
        assert abs(sub[:x-lo+1].sum()-closed) < 2e-14


def test_walsh_mean_cannot_be_dropped():
    f = np.array([.8,1.1,1.3,.9])
    assert branch_metrics(walsh_branch(f,.001),f)['fidelity'] > .99999
    assert branch_metrics(walsh_branch(f,.001,True),f)['fidelity'] < .1
    assert branch_metrics(walsh_branch(np.ones(4),.1,True),np.ones(4))['success_probability'] == 0


def test_one_round_amplification_threshold():
    # Standard one-step Grover is sin(3 asin(sqrt(p)))**2; exact phases
    # can achieve one only if p>=1/4 (phase-matched construction).
    p = .01
    assert np.sin(3*np.arcsin(np.sqrt(p)))**2 < .1
    assert abs(np.sin(3*np.arcsin(.5))**2-1) < 1e-14


def test_phase_not_only_fidelity():
    a = np.array([1,1])/np.sqrt(2)
    assert abs(np.vdot(a,1j*a))**2 == pytest.approx(1)
    assert np.linalg.norm(a-1j*a) > 1


def test_arithmetic_basket_is_not_geometric():
    spots = np.array([50.,200.])
    assert max(spots.mean()-100,0) == 25
    assert max(np.exp(np.log(spots).mean())-100,0) < 1e-12


def test_bad_plan_rejected():
    plan = loader_plan(2)
    broken = copy.deepcopy(plan)
    broken['nodes'].append(broken['nodes'][0])
    with pytest.raises(ValueError):
        folded_loader(broken)


def test_tiny_angles_not_pruned():
    angles = [1e-12,2e-12,-3e-12,4e-12]
    op = Operator(multiplexer(angles)).data
    for k, a in enumerate(angles):
        expected = np.array([[np.cos(a/2),-np.sin(a/2)],
                             [np.sin(a/2),np.cos(a/2)]])
        assert np.max(abs(op[2*k:2*k+2,2*k:2*k+2]-expected)) < 1e-26
