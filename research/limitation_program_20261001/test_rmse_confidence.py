"""Exact tail minimality, Markov counterexample and input/censor guards."""

from fractions import Fraction
from math import comb

import pytest

from research.limitation_program_20261001.rmse_confidence import conversions


def independent_tail(r):
    return sum(
        (Fraction(comb(r, k) * 3 ** (r - k), 4**r) for k in range(r // 2 + 1, r + 1)), Fraction(0)
    )


def test_minimal_median_and_safe_one_run_target():
    result = conversions()
    median = result["independent_median"]
    r = median["repetitions"]
    assert independent_tail(r) == Fraction(*median["certified_failure_upper_exact"])
    assert independent_tail(r) <= Fraction(3, 1000) < independent_tail(r - 2)
    safe = Fraction(*result["one_run"]["safe_rational_RMSE_target_dollars_exact"])
    assert safe**2 <= Fraction(9, 2000) ** 2 * Fraction(3, 1000)
    assert not result["cheaper_complete_conversion_selected"]
    assert median["source_inverse_preparation_readout_reset_multiplicity"] == r


def test_rmse_equal_to_allowance_can_fail_with_probability_one_quarter():
    error = Fraction(9, 2000)
    # Z-mu=2e withprobability1/4, otherwise0. Its RMSE=e but failure=1/4.
    squared_error = Fraction(1, 4) * (2 * error) ** 2
    assert squared_error == error**2
    assert Fraction(1, 4) > Fraction(3, 1000)


@pytest.mark.parametrize(
    "error,failure",
    [
        (0, Fraction(3, 1000)),
        (-1, Fraction(3, 1000)),
        (Fraction(9, 2000), 0),
        (Fraction(9, 2000), Fraction(1, 2)),
        (0.0045, Fraction(3, 1000)),
    ],
)
def test_bad_or_nonexact_allowances_rejected(error, failure):
    with pytest.raises(ValueError):
        conversions(error, failure)


def test_censored_repetition_cap_remains_null():
    result = conversions(max_repetitions=1)
    assert result["independent_median"]["repetitions"] is None
    assert result["independent_median"]["certified_failure_upper_exact"] is None
    assert result["independent_median"]["complete_quantum_cost"] is None
