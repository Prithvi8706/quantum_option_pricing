import pytest
from research.release_checks.budgets import verify_budget
from .test_targets import evidence


def test_budget_terms_and_totals():
    rows = [r for c in evidence()['comparisons'] for r in c['alternatives']]
    assert all(verify_budget(r) for r in rows)
    rows[-1]['budget']['components'].pop('preparation')
    with pytest.raises(ValueError, match='components'):
        verify_budget(rows[-1])


def test_understatement_and_false_physical_admission():
    row = evidence()['comparisons'][0]['alternatives'][-1]
    row['budget']['deterministic_upper'] = '0'
    with pytest.raises(ValueError, match='understates'):
        verify_budget(row)
