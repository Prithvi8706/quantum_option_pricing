"""Exact interval/tie and finite Bernoulli confidence-inversion checks."""

from fractions import Fraction
from itertools import product

import pytest

from research.limitation_program_20261001.conservative_coverage import (
    binary64,
    binomial_cdf,
    classify,
    clopper_pearson_outward,
    conditional_joint_confidence,
)


@pytest.mark.parametrize(
    "center,half,radius,expected",
    (
        (0, 1, 1, (True, True, True)),
        (1, 1, 1, (False, True, True)),
        (2, 1, 1, (False, False, True)),
        (3, 1, 1, (False, False, False)),
        (0, 0, 0, (True, True, True)),
    ),
)
def test_closed_interval_edges_and_three_count_nesting(center, half, radius, expected):
    result = classify(center, half, 0, radius)
    assert (result.guaranteed, result.reference_point, result.possible) == expected


@pytest.mark.parametrize("n", range(1, 7))
def test_binomial_cdf_against_individual_bernoulli_history_enumeration(n):
    for probability in (Fraction(0), Fraction(1), Fraction(1, 2), Fraction(1, 7), Fraction(6, 7)):
        for cutoff in range(-1, n + 1):
            expected = Fraction(0)
            for history in product((0, 1), repeat=n):
                if sum(history) <= cutoff:
                    expected += probability ** sum(history) * (1 - probability) ** (
                        n - sum(history)
                    )
            assert binomial_cdf(n, cutoff, probability) == expected


@pytest.mark.parametrize("successes", range(5))
def test_cp_endpoints_outwardly_bracket_exact_tail_equations(successes):
    n, failure, bits = 4, Fraction(1, 20), 12
    lower, upper = clopper_pearson_outward(successes, n, failure, bits)
    step, target = Fraction(1, 1 << bits), failure / 2
    if successes:
        assert binomial_cdf(n, n - successes, 1 - lower) <= target
        assert binomial_cdf(n, n - successes, 1 - lower - step) >= target
    else:
        assert lower == 0
    if successes < n:
        assert binomial_cdf(n, successes, upper) <= target
        assert binomial_cdf(n, successes, upper - step) >= target
    else:
        assert upper == 1


def test_exact_cp_coverage_under_a_complete_finite_bernoulli_model():
    n, failure = 5, Fraction(1, 4)
    intervals = [clopper_pearson_outward(k, n, failure, 12) for k in range(n + 1)]
    for probability in (Fraction(0), Fraction(1, 8), Fraction(1, 2), Fraction(9, 10), Fraction(1)):
        uncovered = Fraction(0)
        for history in product((0, 1), repeat=n):
            lo, hi = intervals[sum(history)]
            if not lo <= probability <= hi:
                uncovered += probability ** sum(history) * (1 - probability) ** (n - sum(history))
        assert uncovered <= failure


def test_one_trial_root_direction_has_closed_form_and_no_float_quantile():
    step = Fraction(1, 1 << 16)
    lower, upper = clopper_pearson_outward(1, 1, Fraction(1, 20), 16)
    assert lower <= Fraction(1, 40) < lower + step and upper == 1
    lower, upper = clopper_pearson_outward(0, 1, Fraction(1, 20), 16)
    assert lower == 0 and upper - step < Fraction(39, 40) <= upper


def test_sure_contains_and_possible_contains_bound_every_reference_endpoint():
    intervals = ((0, 2), (1, 0), (3, 1), (-2, 1))
    for center, half in intervals:
        membership = classify(center, half, 0, 1)
        for true_value in (Fraction(-1), Fraction(-1, 3), Fraction(0), Fraction(2, 3), Fraction(1)):
            actual = abs(true_value - center) <= half
            assert membership.guaranteed <= actual <= membership.possible


def test_binary64_comparison_rounding_cannot_make_a_false_guarantee():
    center, half, reference = 1.0, 1.0, -(2.0**-53)
    assert abs(center - reference) <= half  # Rounded binary64 subtraction.
    actual = classify(binary64(center), binary64(half), binary64(reference), 0)
    assert not actual.reference_point and not actual.guaranteed and not actual.possible


def test_model_confidence_composition_and_invalid_premises_are_explicit():
    assert conditional_joint_confidence(Fraction(1, 20), (Fraction(1, 100),) * 2) == Fraction(
        93, 100
    )
    assert conditional_joint_confidence(Fraction(4, 5), (Fraction(1, 2),)) == 0
    for value in (True, float("nan"), float("inf"), 1):
        with pytest.raises(ValueError, match="binary64"):
            binary64(value)
    with pytest.raises(ValueError, match="Nonnegative"):
        classify(0, -1, 0, 0)
    for args in ((0, 0), (1, 1001), (2, 1), (True, 1)):
        with pytest.raises(ValueError):
            clopper_pearson_outward(*args)
    with pytest.raises(ValueError):
        clopper_pearson_outward(1, 2, Fraction(0))
    # Python bool/float keys compare equal to some exact integer/Fraction keys.
    # Public validation must happen before memoization can return a prior result.
    clopper_pearson_outward(1, 1)
    clopper_pearson_outward(1, 2, Fraction(1, 2), 1)
    for args in ((True, 1), (1, True), (1, 2, 0.5, 1), (1, 2, Fraction(1, 2), True)):
        with pytest.raises(ValueError):
            clopper_pearson_outward(*args)
