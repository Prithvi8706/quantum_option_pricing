"""Boundaries and matched control/resource conventions; no market acquisition."""

from fractions import Fraction as F

import pytest

from research.journal_sprint.claim_assessment import projected_cost, schedule
from research.journal_sprint.run_matched_arithmetic import (
    arithmetic_budget, cancelled_cost, full_resources, integer_payoffs, plan_for,
)


def test_control_cancellation_ledger_counts_initial_A_and_all_inverses():
    ae = schedule(F(2), F(0))
    resource = full_resources({'cx': 20, 'u': 13}, 4, ae)
    m, repeats, bits = ae['M'], ae['repetitions'], ae['phase_qubits']
    expected = repeats*(20+(m-1)*(40+resource['zero_reflection_cx_projection']+1)
                        +bits*(bits-1)+3*(bits//2))
    assert resource['control_cancelled_total_cx_projection'] == expected
    assert resource['total_cx_projection'] == projected_cost(resource, m, repeats)
    assert resource['total_cx_projection'] > expected
    assert resource['total_qubits'] == 6+bits


def test_exhausted_schedule_does_not_get_a_price_or_physical_promotion():
    ae = schedule(F(2), F(1))
    resources = full_resources({'cx': 20, 'u': 13}, 4, ae)
    assert resources['total_cx_projection'] is None
    assert resources['control_cancelled_total_cx_projection'] is None
    assert resources['physical_execution_error'] is None
    assert cancelled_cost(resources, ae) is None


def test_integer_target_uses_floored_horner_and_positive_part():
    plan = dict(fraction_bits=1, affine_rows=[(0, [2])],
                exp_budget={'coefficients': [2, 2]}, strike_sum=3, selector_bits=2)
    assert integer_payoffs(plan, [0, 1]).tolist() == [0, .5]


def test_selector_truncation_is_rejected():
    plan = dict(fraction_bits=1, affine_rows=[(0, [2])],
                exp_budget={'coefficients': [2, 2]}, strike_sum=0, selector_bits=1)
    with pytest.raises(ArithmeticError, match='selector'):
        integer_payoffs(plan, [0, 1])


def test_control_cancellation_preserves_relative_phase_not_only_probabilities():
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Operator
    a = QuantumCircuit(2)
    a.ry(.31, 0)
    a.cx(0, 1)
    a.p(.71, 1)
    a.global_phase = .23
    reflection = QuantumCircuit(2)
    reflection.x([0, 1])
    reflection.cz(0, 1)
    reflection.x([0, 1])
    block = QuantumCircuit(2)
    block.append(a.inverse().to_gate(), [0, 1])
    block.append(reflection.to_gate(), [0, 1])
    block.append(a.to_gate(), [0, 1])
    direct = QuantumCircuit(3)
    direct.append(block.to_gate().control(), [0, 1, 2])
    cancelled = QuantumCircuit(3)
    cancelled.append(a.inverse().to_gate(), [1, 2])
    cancelled.append(reflection.to_gate().control(), [0, 1, 2])
    cancelled.append(a.to_gate(), [1, 2])
    np.testing.assert_allclose(Operator(direct).data, Operator(cancelled).data, atol=1e-13)


@pytest.mark.parametrize('case_index', [0, 1])
def test_declared_market_decoder_scale_fits_existing_allowance(case_index):
    from research.journal_sprint.run_minimal_pivot_week2 import CASES, contract_of
    from research.journal_sprint.asian_basket import setup
    contract = contract_of(CASES[case_index])
    model = setup(contract)
    plan = plan_for(contract, model, 10)
    budget = arithmetic_budget(contract, model, plan, 0, '0')
    assert budget['decoder_scale'] == 2*budget['beta_upper']
    assert F(budget['decoder_bridge_upper']) <= F(budget['components']['decoding'])
