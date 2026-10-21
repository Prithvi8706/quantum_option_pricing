"""AS241 central-only real-approximation and native rounding certificate."""

from fractions import Fraction
import time

from research.limitation_program_20261001.quantile_central_interval import (
    DOMAIN,
    Interval,
    constant_jet,
    jet_add,
    jet_inverse,
    jet_mul,
    jet_neg,
    jet_polynomial,
    normal_cdf,
    normal_density,
    point,
    square,
    variable_jet,
)


# Published decimal constants, in ascending degree, unchanged from AS241.
A_DECIMALS = (
    "3.387132872796366608",
    "133.14166789178437745",
    "1971.5909503065514427",
    "13731.693765509461125",
    "45921.953931549871457",
    "67265.770927008700853",
    "33430.575583588128105",
    "2509.0809287301226727",
)
B_DECIMALS = (
    "1",
    "42.313330701600911252",
    "687.1870074920579083",
    "5394.1960214247511077",
    "21213.794301586595867",
    "39307.89580009271061",
    "28729.085735721942674",
    "5226.495278852854561",
)
A = tuple(map(Fraction, A_DECIMALS))
B = tuple(map(Fraction, B_DECIMALS))
QMAX = Fraction(17, 40)
RMAX = QMAX**2
CELLS = 2048
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


def rconstant_raw():
    scaled = RMAX * (1 << F)
    return -((-scaled.numerator) // scaled.denominator)


def rational_jet(q):
    q = variable_jet(q)
    r = jet_add(constant_jet(RMAX), jet_neg(jet_mul(q, q)))
    numerator = jet_mul(q, jet_polynomial(A, r))
    denominator = jet_polynomial(B, r)
    return jet_mul(numerator, jet_inverse(denominator))


def residual_derivatives(q, z=None):
    z = rational_jet(q) if z is None else z
    density = normal_density(z[0])
    z1, z2, z3 = z[1], 2 * z[2], 6 * z[3]
    g = normal_cdf(z[0]) - point(q) - Fraction(1, 2)
    g1 = density * z1 - 1
    g2 = density * (z2 - z[0] * z1 * z1)
    g3 = density * (z3 - 3 * z[0] * z1 * z2 + (square(z[0]) - 1) * z1 * z1 * z1)
    return z[0], g, g1, g2, g3


def tighten_jet(value, center, radius):
    """Mean-value intersections of lower derivatives, using the same jets."""
    result = list(value)
    for degree in (2, 1, 0):
        excursion = (degree + 1) * result[degree + 1].bound() * radius
        lo = max(result[degree].lo, center[degree].lo - excursion)
        hi = min(result[degree].hi, center[degree].hi + excursion)
        if lo > hi:
            raise ArithmeticError("Derivative mean-value interval intersection failed")
        result[degree] = Interval(lo, hi)
    return result


def cell_certificate(index):
    if type(index) is not int or not 0 <= index < CELLS:
        raise ValueError("Fixed equal-cell index required")
    width = 2 * QMAX / CELLS
    lower, upper = -QMAX + index * width, -QMAX + (index + 1) * width
    center, radius = (lower + upper) / 2, width / 2
    center_jet = rational_jet(center)
    z0, g0, g1, g2, _ = residual_derivatives(center, center_jet)
    domain = Interval(lower, upper)
    cell_jet = tighten_jet(rational_jet(domain), center_jet, radius)
    zall, _, _, _, g3all = residual_derivatives(domain, cell_jet)
    bound = (
        g0.bound()
        + radius * g1.bound()
        + radius**2 * g2.bound() / 2
        + radius**3 * g3all.bound() / 6
    )
    return {
        "cell_index": index,
        "q_domain_exact": [pair(lower), pair(upper)],
        "center_q_exact": pair(center),
        "radius_exact": pair(radius),
        "rational_z_range_exact": [pair(zall.lo), pair(zall.hi)],
        "center_rational_z_interval_exact": [pair(z0.lo), pair(z0.hi)],
        "center_residual_interval_exact": [pair(g0.lo), pair(g0.hi)],
        "center_first_residual_derivative_interval_exact": [pair(g1.lo), pair(g1.hi)],
        "center_second_residual_derivative_interval_exact": [pair(g2.lo), pair(g2.hi)],
        "third_residual_derivative_absolute_upper_exact": pair(g3all.bound()),
        "CDF_residual_absolute_upper_exact": pair(bound),
        "real_quantile_error_upper_exact": pair(8 * bound),
    }


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


def _horner_value_bounds(raw_coefficients, r_upper):
    value = Fraction(raw_coefficients[-1], 1 << F)
    bounds = [value]
    products = []
    for raw in reversed(raw_coefficients[:-1]):
        products.append(value * r_upper)
        value = value * r_upper + Fraction(raw, 1 << F)
        bounds.append(value)
    return bounds, products


def native_rounding_certificate():
    raw_a, raw_b = rounded_coefficients(A), rounded_coefficients(B)
    if any(coefficient <= 0 for coefficient in raw_a + raw_b) or raw_b[0] != 1 << F:
        raise ArithmeticError("Native positive coefficients/denominator constant changed")
    constant_error = Fraction(rconstant_raw(), 1 << F) - RMAX
    argument_error = constant_error + EPSILON
    r_upper = RMAX + argument_error
    a_error = _horner_error(A, raw_a, r_upper) + argument_error * _derivative_bound(A, r_upper)
    b_error = _horner_error(B, raw_b, r_upper) + argument_error * _derivative_bound(B, r_upper)
    numerator_error = QMAX * a_error + EPSILON
    total = numerator_error + DOMAIN * b_error + EPSILON
    a_values, a_products = _horner_value_bounds(raw_a, r_upper)
    b_values, b_products = _horner_value_bounds(raw_b, r_upper)
    # All output-register quantities are fixed-point values; each native
    # multiply uses the original full144-bit product before floor conversion.
    stored = max(*a_values, *b_values, QMAX * a_values[-1], QMAX, r_upper, Fraction(1))
    product = max(*a_products, *b_products, QMAX**2, QMAX * a_values[-1]) * (1 << (2 * F))
    division_numerator = QMAX * a_values[-1] * (1 << (2 * F))
    if (
        stored * (1 << F) >= 1 << (W - 1)
        or product >= 1 << (2 * W - 1)
        or division_numerator >= 1 << (W + F)
    ):
        raise ArithmeticError("Original native storage/product/division width exceeded")
    return {
        "coefficient_rounding": "exact nearest-even to f40, no fit/tuning",
        "native_A_raw_ascending": list(raw_a),
        "native_B_raw_ascending": list(raw_b),
        "rconstant_raw": rconstant_raw(),
        "rconstant_rounding": "ceil_f40(289/1600), fixed to preserve r_native>=0",
        "q32_midpoint_and_q_exactly_representable_f40": True,
        "r_argument_error_upper_exact": pair(argument_error),
        "r_native_lower_exact": [0, 1],
        "r_native_upper_exact": pair(r_upper),
        "numerator_polynomial_error_upper_exact": pair(a_error),
        "denominator_polynomial_error_upper_exact": pair(b_error),
        "native_denominator_lower_exact": [1, 1],
        "division_semantics": (
            "unsigned floor((a_raw<<40)/b_raw); positive magnitudes only; nonzero denominator"
        ),
        "signed_restoration": (
            "negate the magnitude quotient when q<0; absolute error retained; "
            "exact Gaussian floor not claimed"
        ),
        "new_central_approximation_law_not_prior_exact_floor_quantile_law": True,
        "native_arithmetic_error_upper_exact": pair(total),
        "maximum_stored_fixed_point_value_upper_exact": pair(stored),
        "maximum_full_product_raw_upper_exact": pair(product),
        "maximum_shifted_division_numerator_raw_upper_exact": pair(division_numerator),
        "signed72_stored_values_no_overflow": True,
        "signed144_full_multiply_products_no_overflow": True,
        "unsigned112_division_numerator_no_truncation": True,
        "native_divider_clamp_inactive": True,
        "actual_reversible_leaf_emitted_or_replayed": False,
        "division_gate_cost_charged": False,
        "quantile_quantum_cost": None,
    }


def mathematical_native_central_word(raw):
    """Specified f40 integer arithmetic only; no reversible leaf executed."""
    if type(raw) is not int or not 0 <= raw < 1 << 32:
        raise ValueError("Unsigned q32 word required")
    q_raw = ((2 * raw + 1) << 7) - (1 << 39)
    if abs(Fraction(q_raw, 1 << F)) > QMAX:
        raise ValueError("Central domain only")
    r_raw = rconstant_raw() - ((q_raw * q_raw) >> F)

    def horner(coefficients):
        value = coefficients[-1]
        for coefficient in reversed(coefficients[:-1]):
            value = ((value * r_raw) >> F) + coefficient
        return value

    numerator = (abs(q_raw) * horner(rounded_coefficients(A))) >> F
    denominator = horner(rounded_coefficients(B))
    quotient = (numerator << F) // denominator
    return -quotient if q_raw < 0 else quotient


def run_fixed_cells(cpu_limit=180):
    started = time.process_time()
    left, right = normal_cdf(-DOMAIN), normal_cdf(DOMAIN)
    density_lower = normal_density(DOMAIN).lo
    if (
        not left.hi < Fraction(3, 40)
        or not right.lo > Fraction(37, 40)
        or density_lower < Fraction(1, 8)
    ):
        raise ArithmeticError("Central quantile bracket/density inverse bound unproved")
    cells = []
    try:
        for index in range(CELLS):
            if time.process_time() - started >= cpu_limit:
                return {
                    "certified": False,
                    "budget_censored": True,
                    "reason": "fixed_CPU_limit",
                    "cells_completed": cells,
                    "elapsed_CPU_seconds": time.process_time() - started,
                }
            cells.append(cell_certificate(index))
    except (ValueError, ArithmeticError) as error:
        return {
            "certified": False,
            "budget_censored": False,
            "reason": str(error),
            "cells_completed": cells,
            "elapsed_CPU_seconds": time.process_time() - started,
        }
    native = native_rounding_certificate()
    maximum = max(Fraction(*cell["real_quantile_error_upper_exact"]) for cell in cells)
    native_error = Fraction(*native["native_arithmetic_error_upper_exact"])
    return {
        "certified": maximum + native_error <= TARGET,
        "budget_censored": False,
        "reason": None
        if maximum + native_error <= TARGET
        else "fixed_method_error_bound_exceeds_target",
        "cells_completed": cells,
        "real_approximation_error_upper_exact": pair(maximum),
        "native_arithmetic": native,
        "total_central_quantile_error_upper_exact": pair(maximum + native_error),
        "required_uniform_quantile_error_exact": pair(TARGET),
        "central_true_quantile_and_rational_approximation_domain": [-1.5, 1.5],
        "normal_density_lower_exact": [1, 8],
        "proved_endpoint_CDF_intervals_exact": [
            [pair(left.lo), pair(left.hi)],
            [pair(right.lo), pair(right.hi)],
        ],
        "elapsed_CPU_seconds": time.process_time() - started,
    }
