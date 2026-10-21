"""Guard complete-price decisions against hidden budgets and missing bounds."""

from copy import deepcopy
from fractions import Fraction

import pytest

from research.limitation_program_20261001.complete_price_ledger import (
    adaptive_failure_allocation,
    assess,
    make_b4_ledger,
    rational,
)


def fixture():
    return make_b4_ledger(
        dict(
            statistical_error_dollars_exact=[9, 2000],
            ideal_failure_upper_exact=[1, 500],
            certificate="finite exact median certificate",
        ),
        dict(fixed_contract_certificate="original source/target hash binding"),
        dict(certificate="independent all-input support audit"),
    )


def test_digital_confidence_does_not_close_continuous_price():
    ledger = fixture()
    result = ledger["assessment"]
    assert not result["complete_price_certified"]
    assert result["known_dollar_bound_sum"] == [9, 2000]
    assert result["remaining_dollar_headroom"] == [11, 2000]
    assert result["allocated_failure_sum"] == [1, 100]
    assert len(result["open_obligations"]) == 5
    assert ledger["further_discount_factor_applied"] == [1, 1]


def test_all_certificates_and_exact_boundary_are_required():
    ledger = fixture()
    for term in ledger["dollar_terms"] + ledger["failure_terms"]:
        if term["bound"] is None:
            term.update(bound=[0, 1], certificate="hypothetical test certificate")
    ledger["dollar_terms"][0]["bound"] = [11, 2000]
    assert assess(ledger)["complete_price_certified"]
    ledger["dollar_terms"][0]["bound"] = [5500001, 1000000000]
    assert not assess(ledger)["complete_price_certified"]


@pytest.mark.parametrize(
    "damage",
    ("float", "negative", "unproven-zero", "duplicate", "overallocation", "own-allocation"),
)
def test_invalid_budget_or_unproved_term_is_rejected(damage):
    ledger = deepcopy(fixture())
    if damage == "float":
        ledger["epsilon_dollars"] = 0.01
    elif damage == "negative":
        ledger["dollar_terms"][0]["bound"] = [-1, 100]
    elif damage == "unproven-zero":
        ledger["dollar_terms"][0]["bound"] = [0, 1]
    elif damage == "duplicate":
        ledger["dollar_terms"].append(deepcopy(ledger["dollar_terms"][0]))
    elif damage == "overallocation":
        ledger["failure_terms"][2]["allowance"] = [4, 1000]
    else:
        ledger["failure_terms"][0]["allowance"] = [1, 1000]
    with pytest.raises(ValueError):
        assess(ledger)


def test_adaptive_union_bound_uses_exact_fractions():
    stages = [
        dict(name="first", failure_upper=[1, 1000]),
        dict(name="second", failure_upper=[1, 500]),
    ]
    assert adaptive_failure_allocation(stages, Fraction(3, 1000)) == [3, 1000]
    stages[1]["failure_upper"] = [2000001, 1000000000]
    with pytest.raises(ValueError, match="exceed"):
        adaptive_failure_allocation(stages, Fraction(3, 1000))


def test_missing_adaptive_certificate_cannot_be_zero():
    with pytest.raises(ValueError, match="every adaptive"):
        adaptive_failure_allocation([dict(name="stage", failure_upper=None)], Fraction(3, 1000))


@pytest.mark.parametrize("error,failure", (([1, 100], [1, 500]), ([9, 2000], [1, 100])))
def test_estimator_must_match_exact_dollar_and_confidence_contract(error, failure):
    with pytest.raises(ValueError):
        make_b4_ledger(
            dict(
                statistical_error_dollars_exact=error,
                ideal_failure_upper_exact=failure,
                certificate="test",
            ),
            dict(fixed_contract_certificate="test"),
            dict(certificate="test"),
        )


def test_rational_decimals_are_exact_text():
    assert rational("0.003") == Fraction(3, 1000)
