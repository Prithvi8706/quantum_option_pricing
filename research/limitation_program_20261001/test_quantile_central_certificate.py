"""Analytical jet/enclosure and mathematical integer-interface fixtures."""

from fractions import Fraction

import mpmath as mp
import pytest

from research.limitation_program_20261001.quantile_central_certificate import (
    A,
    B,
    CELLS,
    F,
    QMAX,
    RMAX,
    mathematical_native_central_word,
    native_rounding_certificate,
    nearest_integer,
    rational_jet,
    rconstant_raw,
    rounded_coefficients,
    tighten_jet,
)
from research.limitation_program_20261001.quantile_central_interval import (
    Interval,
    jet_inverse,
    jet_mul,
    normal_cdf,
    normal_density,
    point,
    square,
    variable_jet,
)


def test_cubic_jet_matches_exact_derivatives_at_a_rational_point():
    q = Fraction(1, 8)
    jet = variable_jet(q)
    cubic = jet_mul(jet_mul(jet, jet), jet)
    expected = (q**3, 3 * q**2, 3 * q, Fraction(1))
    assert all(
        interval.lo <= value <= interval.hi for interval, value in zip(cubic, expected, strict=True)
    )


def test_inverse_jet_known_rational_function_at_zero():
    inverse = jet_inverse([point(1), point(0), point(1), point(0)])
    expected = (1, 0, -1, 0)
    assert all(
        interval.lo <= value <= interval.hi
        for interval, value in zip(inverse, expected, strict=True)
    )


def test_inverse_jet_rejects_zero_denominator():
    with pytest.raises(ValueError):
        jet_inverse([Interval(Fraction(-1), Fraction(1)), point(0), point(0), point(0)])


def test_square_crossing_zero_has_nonnegative_lower_bound():
    enclosed = square(Interval(Fraction(-1, 2), Fraction(1, 3)))
    assert enclosed.lo == 0 and enclosed.hi >= Fraction(1, 4)


@pytest.mark.parametrize(
    "argument", [Fraction(-3, 2), Fraction(-1, 2), Fraction(0), Fraction(1, 2), Fraction(3, 2)]
)
def test_fixed_gaussian_enclosures_against_high_precision_numerical_fixture(argument):
    # Sanity fixture; the certificate uses explicit Taylor remainders.
    mp.mp.dps = 100
    z = mp.mpf(argument.numerator) / argument.denominator
    cdf = normal_cdf(argument)
    density = normal_density(argument)
    values = (
        (cdf, (1 + mp.erf(z / mp.sqrt(2))) / 2),
        (density, mp.exp(-z * z / 2) / mp.sqrt(2 * mp.pi)),
    )
    for interval, value in values:
        assert mp.mpf(interval.lo.numerator) / interval.lo.denominator <= value
        assert value <= mp.mpf(interval.hi.numerator) / interval.hi.denominator


def test_true_central_quantile_bracket_and_inverse_density_constant():
    assert normal_cdf(Fraction(-3, 2)).hi < Fraction(3, 40)
    assert normal_cdf(Fraction(3, 2)).lo > Fraction(37, 40)
    assert normal_density(Fraction(3, 2)).lo > Fraction(1, 8)


def test_mean_value_jet_intersection_preserves_linear_function_range():
    center = variable_jet(Fraction(0))
    whole = variable_jet(Interval(Fraction(-1), Fraction(1)))
    restricted = tighten_jet(whole, center, Fraction(1, 8))
    assert restricted[0].lo == Fraction(-1, 8) and restricted[0].hi == Fraction(1, 8)


def test_fixed_domain_cells_and_public_coefficients_are_positive():
    assert CELLS == 2048 and QMAX == Fraction(17, 40) and RMAX == Fraction(289, 1600)
    assert len(A) == len(B) == 8 and min(A + B) > 0 and B[0] == 1


def test_nearest_even_coefficients_and_ceiling_rconstant_are_exact():
    assert nearest_integer(Fraction(1, 2)) == 0
    assert nearest_integer(Fraction(3, 2)) == 2
    assert nearest_integer(Fraction(5, 2)) == 2
    assert RMAX <= Fraction(rconstant_raw(), 2**F) < RMAX + Fraction(1, 2**F)
    assert all(
        abs(Fraction(raw, 2**F) - coefficient) <= Fraction(1, 2 ** (F + 1))
        for raw, coefficient in zip(rounded_coefficients(A), A, strict=True)
    )


def test_mathematical_native_contract_preserves_denominator_and_full_product_widths():
    native = native_rounding_certificate()
    assert native["native_denominator_lower_exact"] == [1, 1]
    assert native["signed72_stored_values_no_overflow"]
    assert native["signed144_full_multiply_products_no_overflow"]
    assert native["unsigned112_division_numerator_no_truncation"]
    assert native["new_central_approximation_law_not_prior_exact_floor_quantile_law"]
    assert not native["actual_reversible_leaf_emitted_or_replayed"]


@pytest.mark.parametrize(
    "raw",
    [
        0x7FFFFFFE,
        0x7FFFFFFF,
        0x80000000,
        0x80000001,
        0x3FFFFFFF,
        0x40000000,
        0xBFFFFFFF,
        0xC0000000,
    ],
)
def test_signed_magnitude_integer_rule_is_symmetric_and_stays_in_native72(raw):
    value = mathematical_native_central_word(raw)
    assert value == -mathematical_native_central_word(2**32 - 1 - raw)
    assert -(2**71) < value < 2**71


@pytest.mark.parametrize("raw", [0, 2**32 - 1, True, 1.0])
def test_integer_rule_refuses_noncentral_or_inexact_input(raw):
    with pytest.raises(ValueError):
        mathematical_native_central_word(raw)


def test_real_rational_jet_has_zero_even_derivatives_at_center():
    jet = rational_jet(Fraction(0))
    assert jet[0].lo == jet[0].hi == 0
    assert jet[2].lo <= 0 <= jet[2].hi
