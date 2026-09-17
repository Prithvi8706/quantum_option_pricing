import math
import numpy as np
import pytest
from qiskit.quantum_info import Operator, Statevector
from research.journal_sprint.week2_pipeline import (
    ae_schedule, choose, controlled_zero, loader, walk, readout, phase_error)
from research.journal_sprint.reflection_centered_signal import ReflectionSignal, signal_circuit
from research.journal_sprint.factorized_signal import projected_phase
from research.journal_sprint.combined_qsp import response
from research.journal_sprint.four_paper_probes import normal_probabilities


@pytest.mark.parametrize('mode',['original','reflection'])
@pytest.mark.parametrize('q',[1,2])
def test_integrated_expectation(mode,q):
    p = ReflectionSignal([.1,-.2],[[.3,-.15],[-.2,.25]],.8,q,4,mode)
    signal,_ = signal_circuit(p)
    phases = [.3,-.2,.4]
    unitary,error = walk(p,signal,phases)
    marginal,loader_error = loader(q)
    assert float(error.hi)<1e-12
    assert float(loader_error.hi)<1e-12
    state = Statevector.from_instruction(readout(p,unitary,marginal))
    probability = state.probabilities([p.num_qubits])[1]
    weights = normal_probabilities(q)
    values,probabilities = [],[]
    for word in range(1 << p.path_qubits):
        digits = [(word >> (j*q)) & ((1<<q)-1) for j in range(2)]
        z = [p.nodes[j,digits[j]] for j in range(2)]
        values.append((np.exp(p.means+p.factor@z).mean()-.8)/p.B)
        probabilities.append(np.prod(weights[digits]))
    expected = (1-np.dot(probabilities,response(values,phases).real))/2
    assert abs(probability-expected)<2e-12


@pytest.mark.parametrize('phi',[-6.,-.3,0.,.7,6.])
def test_wrapped_phase_bound(phi):
    qc = projected_phase(2,[0,1],phi)
    error = phase_error(qc,phi)
    target = np.diag([np.exp(1j*phi)]+[np.exp(-1j*phi)]*3)
    assert float(error.hi)<1e-13
    np.testing.assert_allclose(Operator(qc).data,target,atol=2e-14)


@pytest.mark.parametrize('n',[2,3,4])
def test_controlled_zero_clean_workspace(n):
    qc = controlled_zero(n)
    for word in range(1 << (n+1)):
        actual = Statevector.from_int(word,1 << qc.num_qubits).evolve(qc).data
        target = np.zeros_like(actual)
        target[word] = -1 if word==(1 << n) else 1
        np.testing.assert_allclose(actual,target,atol=2e-13)


def test_schedule_and_inverse_accounting():
    s = ae_schedule(20,.6)
    assert s['status']=='ideal_plan'
    assert s['statistical_dollar_bound']<=.4
    assert s['a_calls']==s['repetitions']*(2*s['M']-1)
    assert s['grover_calls']==s['repetitions']*(s['M']-1)
    assert s['repetitions']%2==1
    assert math.exp(-.18*s['repetitions'])<=.05
    assert ae_schedule(20,1)['status']=='deterministic_budget_exhausted'
    assert ae_schedule(20,.6,cap=1)['status']=='query_cap'


@pytest.mark.parametrize('args',[(0,.2),(1,-.1),(math.inf,.1)])
def test_bad_schedule(args):
    with pytest.raises(ValueError):
        ae_schedule(*args)


def test_selector_never_promotes_hardware():
    rows = [dict(mode='reflection',budget=dict(degree=128,schedule=dict(status='ideal_plan')),
                 resources=dict(total_cx_projection=123))]
    result = choose(rows)
    assert result['ideal_choice']==dict(mode='reflection',degree=128)
    assert result['production_choice'] is None
    assert not result['confirmation_admitted']
    assert choose([])['ideal_choice'] is None
