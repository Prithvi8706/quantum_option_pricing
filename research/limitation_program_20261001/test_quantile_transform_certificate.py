"""Native transform semantics, finite classes and nonduplicated sensitivity fixtures."""

from fractions import Fraction
import math

import mpmath as mp
import pytest

from research.limitation_program_20261001.quantile_transform_certificate import (
    CENTRAL,
    PAIR,
    EPSILON,
    EXPONENTS,
    RMAX,
    central_denominator64_proof,
    fresh_tail_ledger,
    log_table_proof,
    normalization_proof,
    read,
    source_inputs,
)
from research.limitation_program_20261001.quantile_transform_native import (
    F,
    SCALE,
    SHIFT,
    SHIFT_RAW,
    mathematical_transform_word,
    native_log_raw,
    signed72,
)


@pytest.fixture(scope="module")
def archived():
    table, ln2, _ = source_inputs()
    return table, ln2


def test_exact_normalization_covers_all_thirty_exponent_classes(archived):
    table, ln2 = archived
    seen = []
    for bit in range(7, 37):
        p_raw = 128 if bit == 7 else (1 << bit) + 128
        result = native_log_raw(p_raw, table, ln2)
        assert result["exponent"] == bit - F
        assert result["mantissa_raw"] == p_raw << (F - bit)
        assert SCALE <= result["mantissa_raw"] <= 2 * SCALE - (1 << 11)
        assert result["mantissa_raw"] % (1 << 11) == 0
        assert not result["input_guard_changed"] and not result["mantissa_clip_changed"]
        assert abs(result["local_raw"]) <= SCALE // 64
        seen.append(result["exponent"])
    assert seen == list(EXPONENTS)
    assert normalization_proof()["enumerated_q32_words_as_completeness_proof"] == 0


def test_native_negative_product_floor_and_exact_negation_are_distinct():
    a, b = -((1 << 40) + 1), 3
    native_product = signed72((a * b) >> F)
    exact = Fraction(a * b, SCALE)
    assert Fraction(native_product) <= exact < Fraction(native_product + 1)
    assert signed72(-native_product) == -native_product
    # Negating the already floored value gives the upward-rounded opposite.
    assert Fraction(-native_product) >= -exact


@pytest.mark.parametrize("raw", [0, 1, (1 << 17) - 1, (1 << 28) - 1, 322122546, 2**32 - 1])
def test_fixed_native_tail_transform_fixture_has_exact_symmetry_and_inactive_guards(raw, archived):
    table, ln2 = archived
    result = mathematical_transform_word(raw, table, ln2)
    mirror = mathematical_transform_word((1 << 32) - 1 - raw, table, ln2)
    assert result["tail_probability_raw"] == mirror["tail_probability_raw"]
    assert result["transform_r_raw"] == mirror["transform_r_raw"]
    assert result["output_sign_negative"] != mirror["output_sign_negative"]
    assert not result["input_guard_changed"] and not result["mantissa_clip_changed"]
    assert not result["sqrt_guard_changed"]
    assert 0 < result["sqrt_argument_raw"] < 1 << 45
    assert result["sqrt_raw"] < 1 << 43
    assert 0 < result["transform_r_raw"] < RMAX * SCALE


@pytest.mark.parametrize("raw", [0, 1, (1 << 28) - 1, 322122546])
def test_native_log_fixture_against_independent_high_precision_and_prior_table_bound(raw, archived):
    table, ln2 = archived
    result = mathematical_transform_word(raw, table, ln2)
    mp.mp.dps = 120
    p = mp.mpf(result["tail_probability_raw"]) / SCALE
    error = abs(mp.mpf(result["log_raw"]) / SCALE - mp.log(p))
    old = read(PAIR / "certificate.json")
    # The old certificate's native table bound is separate from its coupling.
    table_error = Fraction(*old["log_table_certificate"]["total_error_upper_exact"])
    pair = old["candidates"][0]
    ln2_error = Fraction(*pair["log_ln2_literal_error_per_exponent_exact"])
    bound = table_error + 33 * ln2_error
    assert error <= mp.mpf(bound.numerator) / bound.denominator


def test_native_sqrt_floor_has_at_most_one_f40_ulp_for_declared_integer_arguments():
    for raw in (1, 2, 3, 259 * SCALE // 100, 23 * SCALE, (24 * SCALE) - 1):
        root = math.isqrt(raw << F)
        assert root * root <= raw << F < (root + 1) ** 2
        assert Fraction(root, SCALE) ** 2 <= Fraction(raw, SCALE)
        assert Fraction(raw, SCALE) < Fraction(root + 1, SCALE) ** 2


def test_shift_constant_nearest_rounding_and_exact_signed_subtraction():
    assert SHIFT_RAW == 1759218604442
    assert Fraction(SHIFT_RAW, SCALE) - SHIFT == Fraction(2, 5) * EPSILON
    assert abs(Fraction(SHIFT_RAW, SCALE) - SHIFT) <= EPSILON / 2


def test_original_coefficient_mutation_is_rejected_by_rigorous_table_check(archived):
    table, _ = archived
    forged = [list(row) for row in table]
    forged[0][0] += 2
    mp.iv.dps = 90
    with pytest.raises(ArithmeticError, match="nearest-rounding"):
        log_table_proof(forged)


def toy_tail():
    return {
        "source_coefficients": {"A_decimals_ascending": ["1", "1"], "B_decimals_ascending": ["1"]},
        "native_interface": {
            "native_A_raw_ascending": [SCALE, SCALE],
            "native_B_raw_ascending": [SCALE],
        },
    }


def test_fresh_sensitivity_replaces_old_floor_allowance_without_double_counting():
    rho = Fraction(1, 1 << 20)
    cells = [
        {
            "cell_index": 0,
            "r_domain_exact": [[0, 1], [1, 1]],
            "real_quantile_error_upper_exact": [0, 1],
            "native_arithmetic": {"native_rational_arithmetic_error_upper_exact": [999, 1]},
        }
    ]
    result = fresh_tail_ledger(toy_tail(), cells, rho)[0]
    assert Fraction(*result["fresh_native_rational_error_upper_exact"]) == rho + 2 * EPSILON
    assert not result["previous_conditional_floor_arithmetic_error_added"]
    assert result["argument_perturbation_upper_exact"] == [rho.numerator, rho.denominator]


def test_fresh_native_denominator_lower_uses_shifted_cell_lower_endpoint():
    rho = Fraction(1, 1 << 20)
    tail = toy_tail()
    tail["source_coefficients"]["B_decimals_ascending"] = ["1", "1"]
    tail["native_interface"]["native_B_raw_ascending"] = [SCALE, SCALE]
    cells = [
        {
            "cell_index": 0,
            "r_domain_exact": [[1, 1], [2, 1]],
            "real_quantile_error_upper_exact": [0, 1],
        }
    ]
    result = fresh_tail_ledger(tail, cells, rho)[0]
    assert Fraction(*result["native_denominator_lower_exact"]) == 2 - rho


def test_fresh_native_coefficient_forgery_is_rejected():
    tail = toy_tail()
    tail["native_interface"]["native_A_raw_ascending"][0] += 1
    with pytest.raises(ValueError, match="rounding differs"):
        fresh_tail_ledger(tail, [], EPSILON)


def test_negative_or_inexact_sensitivity_bound_is_rejected():
    for rho in (Fraction(-1), 1.0):
        with pytest.raises(ValueError, match="Nonnegative exact"):
            fresh_tail_ledger(toy_tail(), [], rho)


def test_actual_central_divisor64_bound_is_a_mathematical_interface_only():
    result = central_denominator64_proof(read(CENTRAL / "central_certificate.json"))
    assert Fraction(*result["maximum_central_denominator_raw_upper_exact"]) < 1 << 64
    assert result["unsigned64_denominator_no_truncation"]
    assert not result["actual_divisor64_leaf_or_backend_adopted"]


def test_central_divisor64_overflow_is_rejected():
    forged = {
        "native_arithmetic": {
            "r_native_upper_exact": [1, 1],
            "native_B_raw_ascending": [SCALE, 1 << 64],
        }
    }
    with pytest.raises(ArithmeticError, match="divisor64"):
        central_denominator64_proof(forged)


@pytest.mark.parametrize("raw", [True, 1.0, -1, 1 << 32, 1 << 31])
def test_nonordinary_or_invalid_transform_input_is_rejected(raw, archived):
    table, ln2 = archived
    with pytest.raises(ValueError):
        mathematical_transform_word(raw, table, ln2)
