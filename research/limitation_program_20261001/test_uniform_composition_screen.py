"""Independent numerical checks and misuse guards for the fixed budget screen."""

from fractions import Fraction

import mpmath as mp
import pytest

from research.limitation_program_20261001.uniform_composition_screen import optimistic_terms


@pytest.mark.parametrize("bad", [0, -1, 0.00001, True])
def test_rejects_nonexact_or_nonpositive_beta(bad):
    with pytest.raises(ValueError):
        optimistic_terms(bad, Fraction(1, 20), Fraction(1, 15), Fraction(1, 2**20))


@pytest.mark.parametrize("dates,pairs", [(1, 30), (52, 234), (12, 3)])
def test_rejects_unmatched_contract(dates, pairs):
    with pytest.raises(ValueError):
        optimistic_terms(
            Fraction(1, 40000),
            Fraction(1, 20),
            Fraction(1, 15),
            Fraction(1, 2**20),
            dates=dates,
            pairs=pairs,
        )


def test_formula_enclosures_and_dollar_units_against_independent_erf():
    result = optimistic_terms(
        Fraction(1, 40000), Fraction(1, 20), Fraction(1, 15), Fraction(1, 2**20)
    )
    mp.mp.dps = 120
    centered, density = mp.mpf(0), mp.mpf(0)
    for row in result["dates"]:
        date = row["date"]
        error = mp.mpf(date) * mp.mpf(7) / 60 / 40000
        variance = mp.mpf(3) * date / 1000
        centered += mp.erf(error / mp.sqrt(2 * variance))
        density += 2 * error / mp.sqrt(2 * mp.pi * variance)
    tail = mp.mpf(40 * 30) / 2**20
    for name, total in (("density", density), ("centered_interval_maximum", centered)):
        interval = result["methods"][name]["barrier_and_tail_formula_dollars_interval_exact"]
        lo, hi = (mp.mpf(n) / d for n, d in interval)
        assert lo <= 40 * total + tail <= hi


def test_rejection_does_not_claim_bias_or_ignore_unproved_terms():
    result = optimistic_terms(
        Fraction(1, 40000), Fraction(1, 20), Fraction(1, 15), Fraction(1, 2**20)
    )
    assert all(
        row["formula_floor_exceeds_remaining_headroom"] for row in result["methods"].values()
    )
    assert not result["complete_continuous_price_certificate"]
    assert not result["omitted_terms_credited_as_certified_zero"]
    assert not result["full_path_stock_or_basket_discrepancy_certified"]
    assert all(
        not row["actual_price_bias_lower_bound_claimed"]
        and not row["actual_probability_lower_bound_claimed"]
        for row in result["methods"].values()
    )


def test_budget_guard_can_be_false_for_a_hypothetically_tighter_bound():
    result = optimistic_terms(
        Fraction(1, 10**12), Fraction(1, 20), Fraction(1, 15), Fraction(1, 2**40)
    )
    assert not any(
        row["formula_floor_exceeds_remaining_headroom"] for row in result["methods"].values()
    )
    assert not result["complete_continuous_price_certificate"]
