"""All-q32 native ordinary-tail transform proof, with a fresh rational error ledger."""

from fractions import Fraction
from pathlib import Path
import json
import time

import mpmath as mp

from research.limitation_program_20261001.quantile_transform_native import (
    F,
    W,
    SCALE,
    SHIFT,
    SHIFT_RAW,
    nearest_integer,
)


ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
PAIR = PROGRAM / "C06_pair_run001"
TAIL = PROGRAM / "A02_quantile_tail_run001"
CENTRAL = PROGRAM / "A02_quantile_central_run002"
INTERVAL_DIGITS = 90
EPSILON = Fraction(1, SCALE)
RMAX = Fraction(321, 100)
TARGET = Fraction(1, 100000000)
EXPONENTS = tuple(range(-33, -3))


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def pair(value):
    return [value.numerator, value.denominator]


def iv(value):
    value = Fraction(value)
    return mp.iv.mpf(value.numerator) / value.denominator


def enclosure(value):
    def endpoint(part):
        sign, mantissa, exponent, _ = part
        return Fraction((-1) ** sign * mantissa) * Fraction(2) ** exponent

    return tuple(endpoint(part) for part in value._mpi_)


def source_inputs():
    """Use original archived literals; never regenerate or fit a table."""
    binding = read(PAIR / "certificate.json")["source_bindings"]
    targets = {name: read(ROOT / entry["target"]) for name, entry in binding.items()}
    if any(target["width"] != W or target["fraction_bits"] != F for target in targets.values()):
        raise ValueError("Original72/f40 logarithm target interface required")
    if targets["B4x12"]["tables"]["log"] != targets["B8x52"]["tables"]["log"]:
        raise ValueError("Original B4/B8 logarithm table differs")
    ln2 = binding["B4x12"]["literal_ln2"]
    if ln2 != binding["B8x52"]["literal_ln2"] or ln2 != 762123384786:
        raise ValueError("Original logarithm ln2 literal changed")
    table = targets["B4x12"]["tables"]["log"]
    if len(table) != 32 or any(len(row) != 9 for row in table):
        raise ValueError("Original32-cell degree8 logarithm interface required")
    return table, ln2, binding


def log_table_proof(table):
    radius = Fraction(1, 64)
    remainder = radius**9 / 9
    floors = EPSILON * sum((radius**k for k in range(8)), Fraction(0))
    rows, maximum_value, maximum_product = [], Fraction(0), Fraction(0)
    for index, row in enumerate(table):
        center = 1 + Fraction(2 * index + 1, 64)
        checks, errors = [], []
        for degree, raw in enumerate(row):
            if type(raw) is not int:
                raise ValueError("Original literal logarithm coefficient required")
            exact = (
                enclosure(mp.iv.log(iv(center)))
                if degree == 0
                else (Fraction((-1) ** (degree - 1), degree) / center**degree,) * 2
            )
            error = max(abs(Fraction(raw, SCALE) - endpoint) for endpoint in exact)
            if error > EPSILON / 2:
                raise ArithmeticError("Original logarithm coefficient nearest-rounding unproved")
            errors.append(error)
            checks.append(
                {
                    "degree": degree,
                    "literal_raw": raw,
                    "true_coefficient_interval_exact": [pair(value) for value in exact],
                    "coefficient_error_upper_exact": pair(error),
                }
            )
        coefficient_error = sum((error * radius**k for k, error in enumerate(errors)), Fraction(0))
        value = abs(Fraction(row[-1], SCALE))
        maximum_value = max(maximum_value, value)
        for raw in reversed(row[:-1]):
            maximum_product = max(maximum_product, value * radius)
            product_after_floor = value * radius + EPSILON
            value = product_after_floor + abs(Fraction(raw, SCALE))
            maximum_value = max(maximum_value, value, product_after_floor)
        rows.append(
            {
                "table_cell": index,
                "center_exact": pair(center),
                "radius_exact": pair(radius),
                "coefficient_checks": checks,
                "coefficient_error_upper_exact": pair(coefficient_error),
                "Taylor_remainder_upper_exact": pair(remainder),
                "Horner_floor_error_upper_exact": pair(floors),
                "table_error_upper_exact": pair(remainder + coefficient_error + floors),
            }
        )
    return rows, maximum_value, maximum_product


def normalization_proof():
    # Every native midpoint, or its complement, has form odd*128.
    if not Fraction(3, 40) * SCALE < 1 << 37:
        raise ArithmeticError("Tail upper input index bound failed")
    return {
        "midpoint_native_raw": "(2*k+1)*128; complement2^40-u_raw has the same odd*128 form",
        "minimum_tail_probability_raw": 128,
        "maximum_tail_probability_raw_exclusive_exact": pair(Fraction(3, 40) * SCALE),
        "native_input_guard_raw_one_inactive": True,
        "msb_index_range": [7, 36],
        "log_exponent_range": [-33, -4],
        "normalization_only_left_shifts": True,
        "normalization_roundoff_exact": [0, 1],
        "minimum_mantissa_zero_low_bits": 11,
        "mantissa_raw_bounds": [SCALE, 2 * SCALE - (1 << 11)],
        "interpolation_clips_inactive": True,
        "table_index_range": [0, 31],
        "local_argument_radius_exact": [1, 64],
        "local_argument_center_and_subtraction_exact": True,
        "exponent_times_ln2_floor_error_exact": [0, 1],
        "negative_log_negation_error_exact": [0, 1],
        "signed_floor_negation_explanation": (
            "The logarithm polynomial is already floored. Native subtraction from zero "
            "negates that signed integer exactly; it is not a new floor of -ln(p). "
            "Exponent raw=e*2^40 makes cmul by literal ln2 exactly e*ln2_raw, even for e<0."
        ),
        "all_q32_tail_words_covered": True,
        "enumerated_q32_words_as_completeness_proof": 0,
    }


def transform_error_proof(table, ln2_raw):
    rows, max_poly, max_product = log_table_proof(table)
    ln2_interval = enclosure(mp.iv.log(iv(2)))
    ln2_error = max(abs(Fraction(ln2_raw, SCALE) - value) for value in ln2_interval)
    if ln2_error > EPSILON / 2:
        raise ArithmeticError("Original ln2 nearest-f40 enclosure unproved")
    if not 33 * ln2_interval[1] < Fraction(231, 10):
        raise ArithmeticError("Exact q32 negative-log upper bound unproved")
    combinations = [
        {
            "table_cell": row["table_cell"],
            "exponent": exponent,
            "native_log_error_upper_exact": pair(
                Fraction(*row["table_error_upper_exact"]) + abs(exponent) * ln2_error
            ),
        }
        for row in rows
        for exponent in EXPONENTS
    ]
    error = max(Fraction(*row["native_log_error_upper_exact"]) for row in combinations)
    x_interval = enclosure(-mp.iv.log(iv(Fraction(3, 40))))
    if not (x_interval[0] > Fraction(259, 100) and error < Fraction(1, 1000)):
        raise ArithmeticError("Strict away-from-zero sqrt margins unproved")
    native_lower = Fraction(259, 100) - error
    native_upper = Fraction(231, 10) + error
    if not (
        native_lower > Fraction(1609, 1000) ** 2
        and native_lower > SHIFT**2
        and native_upper < Fraction(4807, 1000) ** 2
        and native_upper < 24
    ):
        raise ArithmeticError("Native sqrt/rational-input range guards unproved")
    shift_error = abs(Fraction(SHIFT_RAW, SCALE) - SHIFT)
    root_sensitivity_error = Fraction(5, 16) * error
    rho = root_sensitivity_error + EPSILON + shift_error
    r_native_lower = Fraction(9, 1000) - EPSILON - shift_error
    r_native_upper = Fraction(3207, 1000) + shift_error
    if not 0 < r_native_lower < r_native_upper < RMAX:
        raise ArithmeticError("Actual native transform lies outside certified rational domain")
    stored = max(
        max_poly + 33 * abs(Fraction(ln2_raw, SCALE)),
        Fraction(33),
        Fraction(24),
        Fraction(4807, 1000),
    )
    full_product = max(max_product, 33 * abs(Fraction(ln2_raw, SCALE))) * (1 << (2 * F))
    if stored * SCALE >= 1 << (W - 1) or full_product >= 1 << (2 * W - 1):
        raise ArithmeticError("Native logarithm full-width overflow guard failed")
    return {
        "normalization": normalization_proof(),
        "log_table_cells": rows,
        "exponent_classes": list(EXPONENTS),
        "cell_exponent_cover": combinations,
        "conservative_cover_includes_unreachable_combinations": True,
        "original_ln2_raw": ln2_raw,
        "ln2_interval_exact": [pair(value) for value in ln2_interval],
        "ln2_literal_error_upper_exact": pair(ln2_error),
        "true_negative_log_upper_exact": [231, 10],
        "q32_log_upper_bound_from_ln2_enclosure": True,
        "native_log_error_upper_exact": pair(error),
        "continuous_uniform_midpoint_coupling_error_included": False,
        "radial_cutoff_or_bad_event_used": False,
        "true_negative_log_lower_interval_exact": [pair(value) for value in x_interval],
        "native_negative_log_lower_exact": pair(native_lower),
        "native_negative_log_upper_exact": pair(native_upper),
        "sqrt_positive_guard_inactive": True,
        "sqrt_argument_unsigned45_bits": True,
        "accepted_unsigned46_sqrt_semantics_applicable_mathematically": True,
        "sqrt_radicand_shifted_bits": 86,
        "actual_shifted_sqrt_radicand_bits": 85,
        "accepted_sqrt_semantic_radicand_bits": 86,
        "sqrt_output_upper_exclusive_exact": [4807, 1000],
        "sqrt_output43_bits": True,
        "sqrt_floor_error_upper_exact": pair(EPSILON),
        "sqrt_sensitivity_error_upper_exact": pair(root_sensitivity_error),
        "sqrt_sensitivity_proof": (
            "Both exact and native radicands exceed (8/5)^2; "
            "|sqrt(a)-sqrt(x)|=|a-x|/(sqrt(a)+sqrt(x))<=5*Elog/16. "
            "Native isqrt(a_raw<<40) contributes one f40 floor ULP."
        ),
        "nearest_shift_raw": SHIFT_RAW,
        "nearest_shift_error_exact": pair(shift_error),
        "native_transform_error_upper_exact": pair(rho),
        "actual_native_r_range_exact": [pair(r_native_lower), pair(r_native_upper)],
        "maximum_stored_value_upper_exact": pair(stored),
        "maximum_full_product_raw_upper_exact": pair(full_product),
        "signed72_log_transform_storage_no_overflow": True,
        "signed144_log_products_no_overflow": True,
        "new_same_SSA_sqrt_dispatch_or_leaf_validation": False,
        "actual_compiled_transform_leaf": None,
        "actual_quantum_gate_cost": None,
    }


def _horner_error(coefficients, raw_coefficients, upper):
    error = abs(Fraction(raw_coefficients[-1], SCALE) - coefficients[-1])
    for coefficient, raw in reversed(
        list(zip(coefficients[:-1], raw_coefficients[:-1], strict=True))
    ):
        error = error * upper + EPSILON + abs(Fraction(raw, SCALE) - coefficient)
    return error


def _derivative_bound(coefficients, upper):
    return sum(
        (
            degree * coefficient * upper ** (degree - 1)
            for degree, coefficient in enumerate(coefficients)
            if degree
        ),
        Fraction(0),
    )


def _native_horner(raw_coefficients, r_raw):
    value = raw_coefficients[-1]
    for coefficient in reversed(raw_coefficients[:-1]):
        value = ((value * r_raw) >> F) + coefficient
    return value


def fresh_tail_ledger(tail, cells, rho):
    if not isinstance(rho, Fraction) or rho < 0:
        raise ValueError("Nonnegative exact rational transform perturbation required")
    a = tuple(map(Fraction, tail["source_coefficients"]["A_decimals_ascending"]))
    b = tuple(map(Fraction, tail["source_coefficients"]["B_decimals_ascending"]))
    raw_a = tuple(nearest_integer(value * SCALE) for value in a)
    raw_b = tuple(nearest_integer(value * SCALE) for value in b)
    if (
        list(raw_a) != tail["native_interface"]["native_A_raw_ascending"]
        or list(raw_b) != tail["native_interface"]["native_B_raw_ascending"]
    ):
        raise ValueError("Frozen published rational coefficient rounding differs")
    ledger = []
    for cell in cells:
        lower, upper = map(lambda value: Fraction(*value), cell["r_domain_exact"])
        extended_lower = max(Fraction(0), lower - rho)
        # This cap uses the separately proved ACTUAL q32 native transform range.
        extended_upper = min(RMAX, upper + rho)
        lower_raw = (extended_lower * SCALE).numerator // (extended_lower * SCALE).denominator
        denominator = Fraction(_native_horner(raw_b, lower_raw), SCALE)
        numerator_error = _horner_error(a, raw_a, extended_upper) + rho * _derivative_bound(
            a, extended_upper
        )
        denominator_error = _horner_error(b, raw_b, extended_upper) + rho * _derivative_bound(
            b, extended_upper
        )
        if denominator < 1:
            raise ArithmeticError("Fresh perturbed-input rational denominator guard failed")
        fresh_native = (
            numerator_error + Fraction(13, 2) * denominator_error
        ) / denominator + EPSILON
        real = Fraction(*cell["real_quantile_error_upper_exact"])
        ledger.append(
            {
                "cell_index": cell["cell_index"],
                "extended_r_domain_exact": [pair(extended_lower), pair(extended_upper)],
                "argument_perturbation_upper_exact": pair(rho),
                "native_denominator_lower_exact": pair(denominator),
                "numerator_coefficient_Horner_and_input_error_upper_exact": pair(numerator_error),
                "denominator_coefficient_Horner_and_input_error_upper_exact": pair(
                    denominator_error
                ),
                "fresh_native_rational_error_upper_exact": pair(fresh_native),
                "saved_real_approximation_error_upper_exact": pair(real),
                "actual_native_tail_quantile_error_upper_exact": pair(real + fresh_native),
                "previous_conditional_floor_arithmetic_error_added": False,
                "actual_sqrt_floor_and_shift_error_only_in_rho": True,
            }
        )
    return ledger


def central_denominator64_proof(central):
    native = central["native_arithmetic"]
    upper = Fraction(*native["r_native_upper_exact"])
    raw_b = native["native_B_raw_ascending"]
    value = Fraction(raw_b[-1], SCALE)
    for coefficient in reversed(raw_b[:-1]):
        value = value * upper + Fraction(coefficient, SCALE)
    raw_upper = value * SCALE
    if raw_upper >= 1 << 64 or min(raw_b) <= 0 or raw_b[0] != SCALE:
        raise ArithmeticError("Central divisor64 compatibility guard unproved")
    return {
        "central_native_argument_upper_exact": pair(upper),
        "maximum_central_denominator_raw_upper_exact": pair(raw_upper),
        "unsigned64_denominator_no_truncation": True,
        "native_denominator_floor_at_one_guard_inactive": True,
        "actual_IR_division_guard_raw_one_inactive": True,
        "actual_divisor64_leaf_or_backend_adopted": False,
    }


def certify(cpu_limit=120):
    started = time.process_time()
    mp.iv.dps = INTERVAL_DIGITS
    table, ln2, binding = source_inputs()
    transform = transform_error_proof(table, ln2)
    if time.process_time() - started >= cpu_limit:
        return {
            "certified": False,
            "budget_censored": True,
            "reason": "fixed_CPU_limit",
            "transform": transform,
            "fresh_tail_rows": [],
        }
    tail = read(TAIL / "tail_certificate.json")
    cells = read(TAIL / "cell_bounds.json")["cells"]
    if (
        not tail["certified"]
        or len(cells) != 1024
        or [row["cell_index"] for row in cells] != list(range(1024))
    ):
        raise ValueError("Completed frozen1024-cell tail certificate required")
    rho = Fraction(*transform["native_transform_error_upper_exact"])
    fresh = fresh_tail_ledger(tail, cells, rho)
    central = read(CENTRAL / "central_certificate.json")
    if central.get("certified") is not True:
        raise ValueError("Successful frozen central certificate required")
    denominator = central_denominator64_proof(central)
    maximum = max(Fraction(*row["actual_native_tail_quantile_error_upper_exact"]) for row in fresh)
    central_error = Fraction(*central["total_central_quantile_error_upper_exact"])
    elapsed = time.process_time() - started
    return {
        "certified": maximum <= TARGET and central_error <= TARGET and elapsed <= cpu_limit,
        "budget_censored": elapsed > cpu_limit,
        "reason": "fixed_CPU_limit"
        if elapsed > cpu_limit
        else None
        if maximum <= TARGET and central_error <= TARGET
        else "fixed_native_error_bound_exceeds_target",
        "source_bindings": binding,
        "transform": transform,
        "fresh_tail_rows": fresh,
        "actual_native_tail_quantile_error_upper_exact": pair(maximum),
        "central_quantile_error_upper_exact": pair(central_error),
        "combined_mathematical_native_quantile_error_upper_exact": pair(
            max(maximum, central_error)
        ),
        "required_uniform_quantile_error_exact": pair(TARGET),
        "central_denominator64": denominator,
        "actual_q32_native_transform_error_included": True,
        "exact_transform_hypothesis_replaced_by_mathematical_native_arithmetic": True,
        "actual_coherent_leaf_or_quantum_gate_cost": None,
        "native_financial_path_arithmetic_certified": False,
        "coherent_loader_implemented_or_adopted": False,
        "accepted_Box_Muller_baseline_changed": False,
        "full_G2_closed": False,
        "elapsed_CPU_seconds": elapsed,
    }
