"""Ordinary AS241 tail rational proof, conditional on an exact rounded transform."""

from fractions import Fraction
from math import factorial
import time

from research.limitation_program_20261001.quantile_tail_interval import (
    DOMAIN,
    Interval,
    exp_negative,
    gaussian_prefactors,
    jet_inverse,
    jet_mul,
    jet_polynomial,
    normal_cdf,
    normal_density,
    point,
    square,
    variable_jet,
)


# Exact published decimal literals, ascending in the ordinary-tail argument.
A_DECIMALS = (
    "1.42343711074968357734",
    "4.6303378461565452959",
    "5.7694972214606914055",
    "3.64784832476320460504",
    "1.27045825245236838258",
    ".24178072517745061177",
    ".0227238449892691845833",
    "7.7454501427834140764e-4",
)
B_DECIMALS = (
    "1",
    "2.05319162663775882187",
    "1.6763848301838038494",
    ".68976733498510000455",
    ".14810397642748007459",
    ".0151986665636164571966",
    "5.475938084995344946e-4",
    "1.05075007164441684324e-9",
)
A = tuple(map(Fraction, A_DECIMALS))
B = tuple(map(Fraction, B_DECIMALS))
SHIFT = Fraction(8, 5)
RMAX = Fraction(321, 100)
TMAX = SHIFT + RMAX
CELLS = 1024
F = 40
W = 72
EPSILON = Fraction(1, 1 << F)
TARGET = Fraction(1, 100000000)


def pair(value):
    return [value.numerator, value.denominator]


def nearest_integer(value):
    lower = value.numerator // value.denominator
    residual = value - lower
    return lower + int(residual > Fraction(1, 2) or (residual == Fraction(1, 2) and lower % 2))


def rounded_coefficients(coefficients):
    return tuple(nearest_integer(coefficient * (1 << F)) for coefficient in coefficients)


def rational_jet(r):
    argument = variable_jet(r)
    return jet_mul(jet_polynomial(A, argument), jet_inverse(jet_polynomial(B, argument)))


def residual_derivatives(r, z=None, include_residual=True):
    """Derivatives of Phi(-z(r))-exp(-(r+8/5)^2), through order four."""
    z = rational_jet(r) if z is None else z
    t = point(r) + SHIFT
    density = normal_density(z[0])
    probability = exp_negative(square(t))
    z1, z2, z3, z4 = z[1], 2 * z[2], 6 * z[3], 24 * z[4]
    t2 = square(t)
    g = normal_cdf(-z[0]) - probability if include_residual else None
    g1 = -density * z1 + 2 * t * probability
    g2 = -density * (z2 - z[0] * z1 * z1) - (4 * t2 - 2) * probability
    g3 = (
        -density * (z3 - 3 * z[0] * z1 * z2 + (square(z[0]) - 1) * z1 * z1 * z1)
        - (12 * t - 8 * t * t2) * probability
    )
    g4 = (
        -density
        * (
            z4
            - 4 * z[0] * z1 * z3
            - 3 * z[0] * z2 * z2
            + 6 * (square(z[0]) - 1) * z1 * z1 * z2
            + (3 * z[0] - z[0] * square(z[0])) * z1 * z1 * z1 * z1
        )
        - (16 * square(t2) - 48 * t2 + 12) * probability
    )
    return z[0], g, g1, g2, g3, g4


def tighten_jet(value, center, radius):
    result = list(value)
    for degree in (3, 2, 1, 0):
        excursion = (degree + 1) * result[degree + 1].bound() * radius
        lo = max(result[degree].lo, center[degree].lo - excursion)
        hi = min(result[degree].hi, center[degree].hi + excursion)
        if lo > hi:
            raise ArithmeticError("Derivative mean-value interval intersection failed")
        result[degree] = Interval(lo, hi)
    return result


def _horner_error(coefficients, raw_coefficients, r_upper):
    error = abs(Fraction(raw_coefficients[-1], 1 << F) - coefficients[-1])
    for coefficient, raw in reversed(
        list(zip(coefficients[:-1], raw_coefficients[:-1], strict=True))
    ):
        error = error * r_upper + EPSILON + abs(Fraction(raw, 1 << F) - coefficient)
    return error


def _derivative_bound(coefficients, r_upper):
    return sum(
        (
            degree * coefficient * r_upper ** (degree - 1)
            for degree, coefficient in enumerate(coefficients)
            if degree
        ),
        Fraction(0),
    )


def _native_horner(raw_coefficients, r_raw):
    value = raw_coefficients[-1]
    for raw in reversed(raw_coefficients[:-1]):
        value = ((value * r_raw) >> F) + raw
    return value


def native_cell_error(lower, upper):
    """Arithmetic conditional on r_raw=FLOOR(2^40*r), not on a log/sqrt leaf."""
    if not 0 <= lower <= upper <= RMAX:
        raise ValueError("Ordered ordinary-tail rational domain required")
    raw_a, raw_b = rounded_coefficients(A), rounded_coefficients(B)
    lower_raw = (lower * (1 << F)).numerator // (lower * (1 << F)).denominator
    native_denominator = Fraction(_native_horner(raw_b, lower_raw), 1 << F)
    a_error = _horner_error(A, raw_a, upper) + EPSILON * _derivative_bound(A, upper)
    b_error = _horner_error(B, raw_b, upper) + EPSILON * _derivative_bound(B, upper)
    if native_denominator < 1:
        raise ArithmeticError("Native denominator positivity or floor-at-one guard failed")
    quotient_error = (a_error + DOMAIN * b_error) / native_denominator + EPSILON
    return {
        "hypothetical_exact_transform_floor_error_upper_exact": pair(EPSILON),
        "native_denominator_lower_exact": pair(native_denominator),
        "numerator_polynomial_error_upper_exact": pair(a_error),
        "denominator_polynomial_error_upper_exact": pair(b_error),
        "native_rational_arithmetic_error_upper_exact": pair(quotient_error),
    }


def native_width_certificate():
    raw_a, raw_b = rounded_coefficients(A), rounded_coefficients(B)
    if min(raw_a + raw_b) <= 0 or raw_b[0] != 1 << F:
        raise ArithmeticError("Positive native coefficient or denominator constant changed")

    def value_bounds(coefficients):
        value = Fraction(coefficients[-1], 1 << F)
        values, products = [value], []
        for coefficient in reversed(coefficients[:-1]):
            products.append(value * RMAX)
            value = value * RMAX + Fraction(coefficient, 1 << F)
            values.append(value)
        return values, products

    a_values, a_products = value_bounds(raw_a)
    b_values, b_products = value_bounds(raw_b)
    stored = max(*a_values, *b_values, RMAX, Fraction(1))
    full_product = max(*a_products, *b_products) * (1 << (2 * F))
    dividend = a_values[-1] * (1 << (2 * F))
    denominator = b_values[-1] * (1 << F)
    if (
        stored * (1 << F) >= 1 << (W - 1)
        or full_product >= 1 << (2 * W - 1)
        or dividend >= 1 << (W + F)
        or denominator >= 1 << 64
    ):
        raise ArithmeticError("Declared storage/product/dividend/divisor width exceeded")
    return {
        "coefficient_rounding": "nearest-even f40, exact published decimals, no fit/tuning",
        "native_A_raw_ascending": list(raw_a),
        "native_B_raw_ascending": list(raw_b),
        "hypothetical_transform": "FLOOR_f40(sqrt(-ln(min(u,1-u)))-8/5)",
        "hypothetical_transform_implemented": False,
        "rounding_ties": "nearest-even coefficients; floor transform/division inclusive at ties",
        "division_semantics": "unsigned floor((A_raw<<40)/B_raw), positive magnitudes only",
        "signed_restoration": "negate magnitude when u<1/2; exact inverse-CDF floor not claimed",
        "maximum_stored_fixed_point_value_upper_exact": pair(stored),
        "maximum_full_product_raw_upper_exact": pair(full_product),
        "maximum_shifted_division_numerator_raw_upper_exact": pair(dividend),
        "maximum_denominator_raw_upper_exact": pair(denominator),
        "signed72_stored_values_no_overflow": True,
        "signed144_full_products_no_overflow": True,
        "unsigned112_dividend_no_truncation": True,
        "unsigned64_denominator_no_truncation": True,
        "native_denominator_floor_at_one_guard_inactive": True,
        "native_quotient_output72_no_truncation": True,
        "actual_coherent_log_sqrt_transform_error_bound": None,
        "actual_coherent_transform_leaf": None,
        "actual_reversible_divider_emitted_or_replayed": False,
        "actual_quantum_gate_cost": None,
    }


def mathematical_native_rational_word(r_raw, negative=False):
    """Classical integer interface fixture, with supplied hypothetical r_raw."""
    max_raw = (RMAX * (1 << F)).numerator // (RMAX * (1 << F)).denominator
    if type(r_raw) is not int or not 0 <= r_raw <= max_raw or type(negative) is not bool:
        raise ValueError("Unsigned f40 ordinary-tail rational input and boolean sign required")
    numerator = _native_horner(rounded_coefficients(A), r_raw)
    denominator = _native_horner(rounded_coefficients(B), r_raw)
    quotient = (numerator << F) // denominator
    return -quotient if negative else quotient


def domain_certificate():
    lower_probability = exp_negative(TMAX**2)
    upper_probability = exp_negative(SHIFT**2)
    lower_cdf = normal_cdf(-DOMAIN)
    degree4 = sum((Fraction(7, 10) ** k / factorial(k) for k in range(5)), Fraction(0))
    if not (
        degree4 > 2
        and Fraction(33 * 7, 10) < TMAX**2
        and TMAX < 5
        and upper_probability.lo > Fraction(3, 40)
        and upper_probability.hi < Fraction(1, 2)
        and lower_cdf.hi < lower_probability.lo
        and lower_cdf.hi < Fraction(1, 1 << 33)
    ):
        raise ArithmeticError("Expanded q32 ordinary-tail domain or quantile bracket unproved")
    return {
        "q32_midpoint_minimum_tail_probability_exact": [1, 1 << 33],
        "ordinary_tail_probability_upper_exclusive_exact": [3, 40],
        "expanded_r_domain_exact": [[0, 1], pair(RMAX)],
        "expanded_t_domain_exact": [pair(SHIFT), pair(TMAX)],
        "positive_degree4_exp_7_over_10_lower_exact": pair(degree4),
        "ln2_upper_exclusive_exact": [7, 10],
        "33_ln2_upper_exclusive_exact": [231, 10],
        "actual_q32_extreme_tail_branch_absent": True,
        "central_tail_branch_tie_not_a_q32_midpoint": (
            "3/40 has denominator factor5; q32 midpoint denominators are powers of2"
        ),
        "expanded_minimum_probability_interval_exact": [
            pair(lower_probability.lo),
            pair(lower_probability.hi),
        ],
        "expanded_maximum_probability_interval_exact": [
            pair(upper_probability.lo),
            pair(upper_probability.hi),
        ],
        "Phi_minus_6_point_5_interval_exact": [pair(lower_cdf.lo), pair(lower_cdf.hi)],
        "expanded_true_quantile_magnitude_upper_exact": pair(DOMAIN),
        "Gaussian_Chernoff_proof": (
            "Completing the square gives E[exp(-sZ)]=exp(s^2/2); Markov with s=x "
            "gives Phi(-x)<=exp(-x^2/2). For p=exp(-t^2), the positive true "
            "quantile magnitude is therefore <=sqrt(2)*t."
        ),
    }


def cell_certificate(index):
    if type(index) is not int or not 0 <= index < CELLS:
        raise ValueError("Fixed equal ordinary-tail cell index required")
    width = RMAX / CELLS
    lower, upper = index * width, (index + 1) * width
    center, radius = (lower + upper) / 2, width / 2
    center_jet = rational_jet(center)
    z0, g0, g1, g2, g3, _ = residual_derivatives(center, center_jet)
    whole_jet = tighten_jet(rational_jet(Interval(lower, upper)), center_jet, radius)
    zall, _, _, _, _, g4all = residual_derivatives(Interval(lower, upper), whole_jet, False)
    if zall.lo < 0 or zall.hi > DOMAIN or zall.hi**2 > 2 * (lower + SHIFT) ** 2:
        raise ArithmeticError("Cell rational magnitude/density conversion range unproved")
    density_lower = gaussian_prefactors()[0].lo * exp_negative((upper + SHIFT) ** 2).lo
    residual = (
        g0.bound()
        + radius * g1.bound()
        + radius**2 * g2.bound() / 2
        + radius**3 * g3.bound() / 6
        + radius**4 * g4all.bound() / 24
    )
    real_error = residual / density_lower
    native = native_cell_error(lower, upper)
    native_error = Fraction(*native["native_rational_arithmetic_error_upper_exact"])
    return {
        "cell_index": index,
        "r_domain_exact": [pair(lower), pair(upper)],
        "center_r_exact": pair(center),
        "radius_exact": pair(radius),
        "rational_z_range_exact": [pair(zall.lo), pair(zall.hi)],
        "rational_z_squared_upper_exact": pair(zall.hi**2),
        "twice_minimum_t_squared_exact": pair(2 * (lower + SHIFT) ** 2),
        "center_rational_z_interval_exact": [pair(z0.lo), pair(z0.hi)],
        "center_residual_interval_exact": [pair(g0.lo), pair(g0.hi)],
        "center_first_residual_derivative_interval_exact": [pair(g1.lo), pair(g1.hi)],
        "center_second_residual_derivative_interval_exact": [pair(g2.lo), pair(g2.hi)],
        "center_third_residual_derivative_interval_exact": [pair(g3.lo), pair(g3.hi)],
        "fourth_residual_derivative_absolute_upper_exact": pair(g4all.bound()),
        "CDF_residual_absolute_upper_exact": pair(residual),
        "inverse_density_lower_exact": pair(density_lower),
        "real_quantile_error_upper_exact": pair(real_error),
        "native_arithmetic": native,
        "total_conditioned_tail_quantile_error_upper_exact": pair(real_error + native_error),
    }


def run_fixed_cells(cpu_limit=300):
    started = time.process_time()
    domain = domain_certificate()
    native = native_width_certificate()
    cells = []
    try:
        for index in range(CELLS):
            if time.process_time() - started >= cpu_limit:
                return {
                    "certified": False,
                    "budget_censored": True,
                    "reason": "fixed_CPU_limit",
                    "cells_completed": cells,
                    "domain_proof": domain,
                    "native_interface": native,
                    "elapsed_CPU_seconds": time.process_time() - started,
                }
            cells.append(cell_certificate(index))
    except (ValueError, ArithmeticError) as error:
        return {
            "certified": False,
            "budget_censored": False,
            "reason": str(error),
            "cells_completed": cells,
            "domain_proof": domain,
            "native_interface": native,
            "elapsed_CPU_seconds": time.process_time() - started,
        }
    maximum = max(
        Fraction(*cell["total_conditioned_tail_quantile_error_upper_exact"]) for cell in cells
    )
    return {
        "certified": maximum <= TARGET,
        "budget_censored": False,
        "reason": None if maximum <= TARGET else "fixed_method_error_bound_exceeds_target",
        "cells_completed": cells,
        "domain_proof": domain,
        "native_interface": native,
        "real_approximation_error_upper_exact": pair(
            max(Fraction(*cell["real_quantile_error_upper_exact"]) for cell in cells)
        ),
        "native_rational_arithmetic_error_upper_exact": pair(
            max(
                Fraction(*cell["native_arithmetic"]["native_rational_arithmetic_error_upper_exact"])
                for cell in cells
            )
        ),
        "total_conditioned_tail_quantile_error_upper_exact": pair(maximum),
        "required_uniform_quantile_error_exact": pair(TARGET),
        "actual_coherent_log_sqrt_error_included": False,
        "elapsed_CPU_seconds": time.process_time() - started,
    }
