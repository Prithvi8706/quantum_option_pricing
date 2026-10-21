"""Validate exact QPE dollar decoding and register-domain rejection."""

from fractions import Fraction

import mpmath as mp
import pytest

from research.limitation_program_20261001.bounded_price_readout_v2 import (
    price_interval,
    rounded_price,
)


def test_every_small_qpe_outcome_against_independent_high_precision_sine():
    mp.mp.dps = 130
    for M in (4, 8, 16, 32):
        for y in range(M):
            lo, hi = price_interval(y, M)
            reference = 64 * mp.sin(mp.pi * y / M) ** 2
            lower = mp.mpf(lo.numerator) / lo.denominator
            upper = mp.mpf(hi.numerator) / hi.denominator
            assert lower - mp.mpf("1e-120") <= reference <= upper + mp.mpf("1e-120")
            decoded = rounded_price(y, M)
            assert Fraction(*decoded["deterministic_error_upper"]) <= Fraction(2, 1 << 40)
            assert price_interval(M - y if y else 0, M) == (lo, hi)


def test_exact_empty_and_full_success_endpoints():
    assert rounded_price(0, 65536)["raw_price"] == 0
    assert rounded_price(32768, 65536)["raw_price"] == 64 << 40
    assert rounded_price(16384, 65536)["raw_price"] in ((32 << 40) - 1, 32 << 40)


@pytest.mark.parametrize("outcome,M", ((-1, 8), (8, 8), (1, 7), (0, 1)))
def test_invalid_qpe_outcomes_rejected(outcome, M):
    with pytest.raises(ValueError):
        price_interval(outcome, M)


def test_outward_dyadic_pi_contains_original_rational_proof():
    from research.limitation_program_20261001.bounded_price_readout_v2 import dyadic_pi_interval
    from research.limitation_program_20261001.financial_bounded_schedule import pi_interval

    lo, hi = pi_interval()
    outer_lo, outer_hi = dyadic_pi_interval()
    assert outer_lo <= lo < hi <= outer_hi
    assert outer_hi - outer_lo <= Fraction(2, 1 << 160)
