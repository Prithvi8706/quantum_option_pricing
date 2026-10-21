"""Tail-domain, rigorous enclosure, derivative and conditional integer fixtures."""

from fractions import Fraction

import mpmath as mp
import pytest

from research.limitation_program_20261001.quantile_tail_certificate import (
    A,
    B,
    CELLS,
    EPSILON,
    F,
    RMAX,
    SHIFT,
    TMAX,
    domain_certificate,
    mathematical_native_rational_word,
    native_cell_error,
    native_width_certificate,
    nearest_integer,
    rational_jet,
    residual_derivatives,
    rounded_coefficients,
)
from research.limitation_program_20261001.quantile_tail_interval import (
    CDF_TERMS,
    DOMAIN,
    EXP_TERMS,
    Interval,
    exp_negative,
    jet_inverse,
    jet_polynomial,
    normal_cdf,
    normal_density,
    point,
    variable_jet,
)


def _contains_numerical(interval, value):
    assert mp.mpf(interval.lo.numerator) / interval.lo.denominator <= value
    assert value <= mp.mpf(interval.hi.numerator) / interval.hi.denominator


def test_fixed_published_tail_domain_and_coefficients():
    assert len(A) == len(B) == 8 and min(A + B) > 0 and B[0] == 1
    assert SHIFT == Fraction(8, 5) and RMAX == Fraction(321, 100)
    assert TMAX == Fraction(481, 100) and CELLS == 1024
    assert CDF_TERMS == EXP_TERMS == 128 and DOMAIN == Fraction(13, 2)


def test_exact_q32_endpoint_domain_and_absent_extreme_branch():
    proof = domain_certificate()
    assert (
        proof["positive_degree4_exp_7_over_10_lower_exact"][0]
        > 2 * proof["positive_degree4_exp_7_over_10_lower_exact"][1]
    )
    assert proof["actual_q32_extreme_tail_branch_absent"]
    assert Fraction(33 * 7, 10) < TMAX**2 < 25
    assert Fraction(*proof["Phi_minus_6_point_5_interval_exact"][1]) < Fraction(1, 1 << 33)


@pytest.mark.parametrize(
    "raw,ordinary", [(0, True), (322122546, True), (322122547, False), (2**32 - 1, True)]
)
def test_central_tail_boundary_is_exactly_classified(raw, ordinary):
    u = Fraction(2 * raw + 1, 1 << 33)
    p = min(u, 1 - u)
    assert (p < Fraction(3, 40)) == ordinary
    assert p != Fraction(3, 40)


@pytest.mark.parametrize(
    "argument", [Fraction(0), Fraction(1, 2), Fraction(169, 8), TMAX**2, Fraction(25)]
)
def test_positive_taylor_reciprocal_encloses_negative_exponential(argument):
    # Numerical fixture only; the certificate uses an exact geometric tail.
    mp.mp.dps = 120
    value = mp.mpf(argument.numerator) / argument.denominator
    _contains_numerical(exp_negative(argument), mp.exp(-value))


@pytest.mark.parametrize(
    "argument", [Fraction(-13, 2), Fraction(-3, 2), Fraction(0), Fraction(3, 2), Fraction(13, 2)]
)
def test_tail_gaussian_enclosures_at_fixed_extreme_endpoints(argument):
    mp.mp.dps = 120
    value = mp.mpf(argument.numerator) / argument.denominator
    _contains_numerical(normal_cdf(argument), (1 + mp.erf(value / mp.sqrt(2))) / 2)
    _contains_numerical(normal_density(argument), mp.exp(-(value**2) / 2) / mp.sqrt(2 * mp.pi))
    assert normal_cdf(argument).hi - normal_cdf(argument).lo < Fraction(1, 10**20)


@pytest.mark.parametrize("argument", [Fraction(-1), Fraction(25) + EPSILON])
def test_exponential_refuses_argument_outside_frozen_domain(argument):
    with pytest.raises(ValueError):
        exp_negative(argument)


def test_gaussian_refuses_argument_outside_frozen_domain():
    with pytest.raises(ValueError):
        normal_cdf(DOMAIN + EPSILON)


def test_inverse_jet_fourth_coefficient_is_factorial_normalized():
    inverse = jet_inverse([point(1), point(0), point(1), point(0), point(0)])
    assert all(
        interval.lo <= value <= interval.hi
        for interval, value in zip(inverse, (1, 0, -1, 0, 1), strict=True)
    )


def test_residual_fourth_derivative_matches_independent_composed_function():
    mp.mp.dps = 120
    r = Fraction(1, 8)
    z = jet_polynomial((1, 1, 1, 1, 1), variable_jet(r))
    derivatives = residual_derivatives(r, z)

    def residual(argument):
        magnitude = 1 + argument + argument**2 + argument**3 + argument**4
        return mp.erfc(magnitude / mp.sqrt(2)) / 2 - mp.exp(-((argument + mp.mpf(8) / 5) ** 2))

    for order in range(5):
        _contains_numerical(derivatives[order + 1], mp.diff(residual, mp.mpf(1) / 8, order))


def test_actual_published_rational_fourth_derivative_matches_independent_fixture():
    mp.mp.dps = 120
    a = [mp.mpf(value.numerator) / value.denominator for value in A]
    b = [mp.mpf(value.numerator) / value.denominator for value in B]

    def rational(argument):
        return mp.polyval(list(reversed(a)), argument) / mp.polyval(list(reversed(b)), argument)

    fourth = 24 * rational_jet(Fraction(1, 8))[4]
    _contains_numerical(fourth, mp.diff(rational, mp.mpf(1) / 8, 4))


def test_native_conditional_widths_include_unsigned64_denominator():
    native = native_width_certificate()
    assert native["signed72_stored_values_no_overflow"]
    assert native["signed144_full_products_no_overflow"]
    assert native["unsigned112_dividend_no_truncation"]
    assert native["unsigned64_denominator_no_truncation"]
    assert Fraction(*native["maximum_denominator_raw_upper_exact"]) < 1 << 64
    assert native["native_denominator_floor_at_one_guard_inactive"]
    assert native["native_quotient_output72_no_truncation"]
    assert native["actual_coherent_transform_leaf"] is None
    assert native["actual_coherent_log_sqrt_transform_error_bound"] is None
    assert not native["actual_reversible_divider_emitted_or_replayed"]


def test_nearest_even_coefficients_and_floor_transform_ties_are_declared():
    assert nearest_integer(Fraction(1, 2)) == 0
    assert nearest_integer(Fraction(3, 2)) == 2
    assert nearest_integer(Fraction(5, 2)) == 2
    assert min(rounded_coefficients(A) + rounded_coefficients(B)) > 0
    assert rounded_coefficients(B)[0] == 1 << F
    assert "floor" in native_width_certificate()["rounding_ties"]


@pytest.mark.parametrize("raw", [0, 1, 2**39, 2**40, 2**41, 3 * 2**40, (321 * 2**40) // 100])
def test_hypothetical_rational_input_integer_law_has_paid_sign_rule_and_safe_width(raw):
    positive = mathematical_native_rational_word(raw)
    assert positive == -mathematical_native_rational_word(raw, True)
    assert 0 < positive < 1 << 71


@pytest.mark.parametrize("raw", [-1, True, 1.0, (321 * 2**40) // 100 + 1])
def test_integer_law_rejects_invalid_conditional_input(raw):
    with pytest.raises(ValueError):
        mathematical_native_rational_word(raw)


@pytest.mark.parametrize(
    "lower,upper",
    [(Fraction(0), Fraction(1, 100)), (Fraction(1), Fraction(101, 100)), (Fraction(3), RMAX)],
)
def test_native_error_uses_actual_positive_local_denominator(lower, upper):
    certificate = native_cell_error(lower, upper)
    assert Fraction(*certificate["native_denominator_lower_exact"]) >= 1
    assert Fraction(*certificate["native_rational_arithmetic_error_upper_exact"]) > 0
    assert certificate["hypothetical_exact_transform_floor_error_upper_exact"] == [1, 1 << 40]


def test_native_error_rejects_outside_rational_domain():
    with pytest.raises(ValueError):
        native_cell_error(Fraction(-1), RMAX)
    with pytest.raises(ValueError):
        native_cell_error(Fraction(0), RMAX + EPSILON)


def test_negative_exponential_interval_enclosure_preserves_monotonicity():
    interval = exp_negative(Interval(Fraction(1), Fraction(2)))
    assert interval.lo <= exp_negative(Fraction(2)).lo
    assert interval.hi >= exp_negative(Fraction(1)).hi
