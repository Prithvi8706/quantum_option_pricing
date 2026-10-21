"""Exact finite schedule thresholds and median confidence checks."""

from fractions import Fraction
from math import comb

import pytest

from research.limitation_program_20261001.financial_bounded_schedule import (
    atan_interval,
    binomial_majority_tail,
    certified_schedule,
    pi_interval,
)


def test_machin_intervals_nest_and_enclose_independent_classical_bounds():
    old = pi_interval(8)
    lo, hi = pi_interval(80)
    assert old[0] <= lo < hi <= old[1]
    assert Fraction(314159265358979323846264338327950288419716939937510, 10**50) < lo
    assert hi < Fraction(314159265358979323846264338327950288419716939937511, 10**50)
    assert Fraction(333, 106) < lo < hi < Fraction(355, 113)


@pytest.mark.parametrize("terms", (1, 2, 3, 4))
def test_alternating_arctangent_interval_contains_later_enclosure(terms):
    lo, hi = atan_interval(5, terms)
    later = atan_interval(5, 30)
    assert lo <= later[0] < later[1] <= hi


def test_median_tail_matches_enumeration_of_independent_finite_coin_words():
    bad = Fraction(1, 4)
    for repetitions in (1, 3, 5, 7):
        failing = sum(
            comb(repetitions, k) * 3 ** (repetitions - k)
            for k in range(repetitions // 2 + 1, repetitions + 1)
        )
        assert binomial_majority_tail(repetitions, bad) == Fraction(failing, 4**repetitions)


def test_one_b4_price_has_minimal_power_and_odd_repetition_certificate():
    row = certified_schedule()
    assert row["M"] == 65536
    assert row["controlled_grover_calls"] == row["repetitions"] * 65535
    assert row["qpe_bits"] == 16 and row["adaptive_quantum_rounds"] == 0
    assert Fraction(*row["ideal_error_upper_exact"]) <= Fraction(9, 2000)
    assert Fraction(*row["ideal_failure_upper_exact"]) <= Fraction(3, 1000)
    assert binomial_majority_tail(
        row["repetitions"] - 2, Fraction(*row["elementary_failure_upper_exact"])
    ) > Fraction(3, 1000)


@pytest.mark.parametrize(
    "error,failure,span",
    (
        (0, Fraction(3, 1000), 64),
        (Fraction(1, 100), 0, 64),
        (0.01, Fraction(3, 1000), 64),
        (Fraction(1, 100), Fraction(3, 1000), 0),
    ),
)
def test_invalid_or_floating_budgets_rejected(error, failure, span):
    with pytest.raises(ValueError):
        certified_schedule(error, failure, span)
