"""Rigorous local scalar-quantile words and a conditional rounded-law theorem.

The all-input law is mathematically defined by an exact inverse CDF and floor.
Certifying sixteen words is not a complete inverse-CDF algorithm or loader.
"""

from fractions import Fraction
import time

from research.limitation_program_20261001.barrier_band_certificate import (
    PRECISION,
    TAYLOR_TERMS,
    _centered_normal_interval,
    exact,
    pair,
)
from research.limitation_program_20261001.financial_bounded_schedule import pi_interval


Q = 32
F = 40
W = 72
MAX_STEPS = 80
RAW_WORDS = (
    0x00000000,
    0x00000001,
    0xFFFFFFFE,
    0xFFFFFFFF,
    0x7FFFFFFE,
    0x7FFFFFFF,
    0x80000000,
    0x80000001,
    0x3FFFFFFF,
    0x40000000,
    0xBFFFFFFF,
    0xC0000000,
    0x12345678,
    0x9ABCDEF0,
    0x31415926,
    0xDEADBEEF,
)
MODEL_DIMENSIONS = {"B4x12": 60, "B8x52": 468}
PROOF = {
    "rounding": (
        "For every raw q32 word k, u=(2k+1)/2^33 lies strictly inside(0,1). "
        "Define z=Phi_inverse(u) and a=floor(2^40*z)/2^40. Then a<=z<a+2^-40. "
        "The local interval solver emits a word only after proving this floor "
        "bin; sixteen selected words do not establish solver completeness."
    ),
    "midpoint_KS": (
        "The exact independent scalar quantile midpoint law has distribution "
        "function within2^-33 of Phi, including either side of each atom. "
        "This follows by counting midpoint uniforms below any Phi(x)."
    ),
    "rounded_KS": (
        "Since a<=z<a+epsilon, G_z(x)<=G_a(x)<=G_z(x+epsilon). "
        "The standard normal density is everywhere<=1/sqrt(2*pi)<2/5; "
        "pi>25/8 is certified by the existing exact rational enclosure. "
        "Consequently sup_x abs(G_a(x)-Phi(x))<=2^-33+(2/5)*2^-40."
    ),
    "bounded_variation_product": (
        "For a scalar function of bounded variation V, expectation difference "
        "under two laws is<=V times their Kolmogorov distance, by the "
        "Stieltjes integration-by-parts bound, including one-sided jump values. "
        "The independently audited original continuous GBM/payoff has "
        "coordinate variation<=80 discounted dollars. Replace independent "
        "coordinates one at a time and integrate over the other coordinates: "
        "price-law bias<=dimension*80*(2^-33+(2/5)*2^-40)."
    ),
    "scope": (
        "This all-input result concerns the mathematically DEFINED floor-rounded "
        "independent scalar quantile law and exact continuous financial arithmetic. "
        "It does not infer certification of all2^32 words from16 tests, does not "
        "certify finite Box-Muller or a coherent loader, and does not bound "
        "native path arithmetic/clipping or physical runtime."
    ),
}


def midpoint(raw):
    if type(raw) is not int or not 0 <= raw < 1 << Q:
        raise ValueError("Unsigned q32 raw word required")
    return Fraction(2 * raw + 1, 1 << (Q + 1))


def normal_cdf_interval(argument):
    """One fixed audited integrated-Taylor method, with exact Gaussian symmetry."""
    argument = exact(argument)
    if not -8 <= argument <= 8:
        raise ValueError("Fixed Gaussian enclosure domain[-8,8] required")
    lower, upper = _centered_normal_interval((abs(argument),) * 2)
    if argument < 0:
        return (1 - upper) / 2, (1 - lower) / 2
    return (1 + lower) / 2, (1 + upper) / 2


def floor_bin(lower, upper):
    """Prove one floor bin for an open quantile bracket, including negative words."""
    lower, upper = exact(lower), exact(upper)
    if lower >= upper:
        raise ValueError("Ordered nonempty open quantile bracket required")
    scale = 1 << F
    raw_signed = (lower * scale).numerator // (lower * scale).denominator
    if upper <= Fraction(raw_signed + 1, scale):
        if not -(1 << (W - 1)) <= raw_signed < 1 << (W - 1):
            raise ValueError("Certified word leaves native signed72 domain")
        return raw_signed
    return None


def solve_quantile_word(raw, cdf=normal_cdf_interval, max_steps=MAX_STEPS):
    """At most80 bisections; unresolved comparisons and bins remain censored."""
    probability = midpoint(raw)
    if type(max_steps) is not int or not 0 <= max_steps <= MAX_STEPS:
        raise ValueError("Declared bisection limit between0 and80 required")
    started = time.process_time()
    lower, upper = Fraction(-8), Fraction(8)
    left, right = cdf(lower), cdf(upper)
    evaluations, steps = 2, 0
    reason = None
    if not left[1] < probability < right[0]:
        reason = "endpoint_root_bracket_unproved"
    signed = None
    history = []
    while reason is None:
        signed = floor_bin(lower, upper)
        if signed is not None:
            break
        if steps == max_steps:
            reason = "bisection_limit_floor_bin_unproved"
            break
        middle = (lower + upper) / 2
        cdf_lower, cdf_upper = cdf(middle)
        if not 0 <= cdf_lower <= cdf_upper <= 1:
            raise ValueError("Ordered probability enclosure required")
        evaluations += 1
        steps += 1
        history.append(
            {
                "argument_exact": pair(middle),
                "CDF_interval_exact": [pair(cdf_lower), pair(cdf_upper)],
            }
        )
        if cdf_upper < probability:
            lower = middle
        elif cdf_lower > probability:
            upper = middle
        else:
            reason = "CDF_comparison_unresolved_at_fixed_precision"
    return {
        "raw_uniform_word": raw,
        "midpoint_probability_exact": pair(probability),
        "certified": signed is not None,
        "censored": signed is None,
        "censor_reason": reason,
        "open_quantile_bracket_exact": [pair(lower), pair(upper)],
        "initial_endpoint_CDF_intervals_exact": [
            [pair(bound) for bound in left],
            [pair(bound) for bound in right],
        ],
        "native_signed72_f40_word": signed,
        "native_two_complement_word": signed % (1 << W) if signed is not None else None,
        "rounded_normal_exact": pair(Fraction(signed, 1 << F)) if signed is not None else None,
        "downward_rounding_error_upper_exact": [1, 1 << F] if signed is not None else None,
        "bisection_steps": steps,
        "CDF_enclosure_evaluations": evaluations,
        "CDF_comparison_history": history,
        "classical_solver_CPU_seconds": time.process_time() - started,
        "quantum_gate_count_inferred": False,
        "all_input_solver_completeness_inferred": False,
    }


def defined_law_certificate(case):
    """Conditional all-input law theorem, separate from finite solver outcomes."""
    if case not in MODEL_DIMENSIONS:
        raise ValueError("Original supported contract required")
    pi_lower, _ = pi_interval()
    if pi_lower <= Fraction(25, 8):
        raise ArithmeticError("Normal density bound proof failed")
    midpoint_error = Fraction(1, 1 << (Q + 1))
    rounding_error = Fraction(2, 5) / (1 << F)
    ks = midpoint_error + rounding_error
    dimension = MODEL_DIMENSIONS[case]
    price_bias = dimension * 80 * ks
    return {
        "case": case,
        "uniform_bits": Q,
        "fraction_bits": F,
        "word_width": W,
        "defined_law": (
            "floor(2^40*Phi_inverse((raw+1/2)/2^32))/2^40, independent scalar coordinates"
        ),
        "quantile_rounding": "downward FLOOR, including negative quantiles",
        "pointwise_defined_quantile_error_upper_exact": [1, 1 << F],
        "midpoint_law_KS_upper_exact": pair(midpoint_error),
        "rounding_KS_increment_upper_exact": pair(rounding_error),
        "defined_rounded_law_KS_upper_exact": pair(ks),
        "normal_density_upper_exact": [2, 5],
        "pi_lower_exact": pair(pi_lower),
        "normal_coordinates": dimension,
        "coordinate_total_variation_upper_dollars_exact": [80, 1],
        "all_date_defined_rounded_law_price_bias_upper_exact": pair(price_bias),
        "headroom_exact": [11, 2000],
        "defined_rounded_law_term_fits_headroom": price_bias <= Fraction(11, 2000),
        "conditional_all_input_defined_law_certificate": True,
        "all_input_solver_completeness_certified": False,
        "accepted_Box_Muller_law_certified": False,
        "native_financial_path_arithmetic_certified": False,
        "coherent_loader_implemented": False,
        "complete_original_price_certified": False,
        "second_discount_applied": False,
        "quantum_resources_or_runtime_extrapolated_from_classical_solver": False,
        "proof": PROOF,
        "enclosure_method": {
            "method": "audited integrated Gaussian Taylor plus symmetry",
            "terms": TAYLOR_TERMS,
            "outward_precision_bits": PRECISION,
            "domain": [-8, 8],
            "maximum_bisection_steps_per_word": MAX_STEPS,
        },
    }
