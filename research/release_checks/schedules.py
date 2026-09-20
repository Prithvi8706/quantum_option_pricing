"""Check the fixed 95%-confidence AE schedule using rational pi enclosures."""
from fractions import Fraction as F
from research.journal_sprint.claim_assessment import PI_LOWER, PI_UPPER
from .ledger import count


def verify_schedule(row):
    budget = row['budget']
    remaining = F(1)-F(budget['deterministic_upper'])
    beta = F(budget['beta'] if row['mode'] == 'reflection' else budget['beta_upper'])
    if beta <= 0 or F(budget['deterministic_upper']) < 0:
        raise ValueError('invalid budget scale')
    s = budget['schedule']
    if remaining <= 0:
        if s != {'status': 'deterministic_budget_exhausted', 'M': None, 'a_calls': None}:
            raise ValueError('exhausted budget received a schedule')
        return True
    m, runs = count(s['M']), count(s['repetitions'])
    if m < 2 or m & (m-1) or runs != 17 or s['phase_qubits'] != m.bit_length()-1:
        raise ValueError('invalid fixed-confidence schedule')
    calls = 17*(2*m-1)
    bound = 2*beta*(PI_UPPER/m+PI_UPPER**2/m**2)
    previous = 2*beta*(PI_LOWER/(m//2)+PI_LOWER**2/(m//2)**2)
    expected_status = 'ideal_plan' if calls <= 10_000_000 else 'query_cap'
    if s['a_calls'] != calls or s['status'] != expected_status or bound > remaining:
        raise ValueError('call count, status or precision mismatch')
    if m > 2 and previous <= remaining:
        raise ValueError('M is not certified minimal')
    if F(s['statistical_upper_rational']) != bound:
        raise ValueError('statistical bound differs')
    return True
