"""Proof/solver fixtures, separate from the sixteen actual quantile words."""

from fractions import Fraction

import mpmath as mp
import pytest

from research.limitation_program_20261001.quantile_rounding_certificate import (
    F,
    MAX_STEPS,
    Q,
    RAW_WORDS,
    defined_law_certificate,
    floor_bin,
    midpoint,
    normal_cdf_interval,
    solve_quantile_word,
)


def test_fixed_preregistered_word_budget_and_precision():
    assert (Q, F, MAX_STEPS) == (32, 40, 80)
    assert len(RAW_WORDS) == len(set(RAW_WORDS)) == 16
    assert RAW_WORDS[:4] == (0, 1, 2**32 - 2, 2**32 - 1)


@pytest.mark.parametrize("raw", [-1, 2**32, True, 1.0])
def test_raw_word_must_be_exact_unsigned_q32(raw):
    with pytest.raises(ValueError):
        midpoint(raw)


def test_midpoints_are_interior_and_symmetric():
    assert midpoint(0) == Fraction(1, 2**33)
    assert midpoint(2**32 - 1) == 1 - Fraction(1, 2**33)
    assert all(midpoint(raw) + midpoint(2**32 - 1 - raw) == 1 for raw in RAW_WORDS)


@pytest.mark.parametrize("argument", [0, Fraction(1, 2), 1, 2, 8])
def test_audited_cdf_enclosure_against_high_precision_numerical_fixture(argument):
    # Numerical sanity fixture only; the enclosure proof is inherited from
    # the independently audited integrated Taylor/remainder arithmetic.
    lower, upper = normal_cdf_interval(argument)
    mp.mp.dps = 120
    x = mp.mpf(argument.numerator) / argument.denominator
    reference = (1 + mp.erf(x / mp.sqrt(2))) / 2
    assert mp.mpf(lower.numerator) / lower.denominator <= reference
    assert reference <= mp.mpf(upper.numerator) / upper.denominator
    negative = normal_cdf_interval(-argument)
    assert negative == (1 - upper, 1 - lower)
    assert 0 <= lower <= upper <= 1


@pytest.mark.parametrize("argument", [-9, 9, True, 0.1])
def test_fixed_exact_cdf_domain_guard(argument):
    with pytest.raises(ValueError):
        normal_cdf_interval(argument)


@pytest.mark.parametrize("signed", [-17, -1, 0, 1, 2047])
def test_floor_bin_certificate_handles_negative_words_and_open_upper_boundary(signed):
    scale = 2**F
    assert floor_bin(Fraction(3 * signed + 1, 3 * scale), Fraction(signed + 1, scale)) == signed
    assert floor_bin(Fraction(signed, scale), Fraction(signed + 2, scale)) is None


def test_synthetic_solver_certifies_floor_instead_of_nearest_rounding():
    # A shifted uniform CDF is an algebraic solver fixture, not an actual
    # Gaussian quantile evaluation or an extra raw-word candidate.
    epsilon = Fraction(1, 2**F)

    def synthetic_cdf(argument):
        value = min(Fraction(1), max(Fraction(0), Fraction(1, 2) + (argument + epsilon / 3) / 16))
        return value, value

    row = solve_quantile_word(0x80000000, cdf=synthetic_cdf)
    assert row["certified"] and not row["censored"]
    assert row["native_signed72_f40_word"] == 2047
    assert row["bisection_steps"] <= MAX_STEPS
    assert not row["all_input_solver_completeness_inferred"]


def test_synthetic_solver_censors_a_midpoint_comparison_it_cannot_decide():
    def synthetic_cdf(argument):
        if argument == -8:
            return Fraction(0), Fraction(0)
        if argument == 8:
            return Fraction(1), Fraction(1)
        return Fraction(0), Fraction(1)

    row = solve_quantile_word(0x7FFFFFFF, cdf=synthetic_cdf)
    assert row["censored"] and row["native_signed72_f40_word"] is None
    assert row["censor_reason"] == "CDF_comparison_unresolved_at_fixed_precision"
    assert row["bisection_steps"] == 1


def test_synthetic_solver_preserves_unproved_initial_bracket():
    row = solve_quantile_word(0, cdf=lambda argument: (Fraction(0), Fraction(1)))
    assert row["censored"] and row["bisection_steps"] == 0
    assert row["censor_reason"] == "endpoint_root_bracket_unproved"


def test_synthetic_solver_stops_at_declared_bisection_budget():
    def synthetic_cdf(argument):
        value = (argument + 8) / 16
        return value, value

    row = solve_quantile_word(1, cdf=synthetic_cdf, max_steps=2)
    assert row["censored"] and row["bisection_steps"] == 2
    assert row["censor_reason"] == "bisection_limit_floor_bin_unproved"


@pytest.mark.parametrize("limit", [-1, 81, True, 80.0])
def test_solver_rejects_work_budget_extension(limit):
    with pytest.raises(ValueError):
        solve_quantile_word(0, max_steps=limit)


@pytest.mark.parametrize("case,dimension", [("B4x12", 60), ("B8x52", 468)])
def test_defined_all_input_law_ks_bv_product_bound_and_nontransfer_guards(case, dimension):
    row = defined_law_certificate(case)
    ks = Fraction(1, 2**33) + Fraction(2, 5 * 2**40)
    assert Fraction(*row["defined_rounded_law_KS_upper_exact"]) == ks
    assert (
        Fraction(*row["all_date_defined_rounded_law_price_bias_upper_exact"]) == dimension * 80 * ks
    )
    assert row["defined_rounded_law_term_fits_headroom"]
    assert row["conditional_all_input_defined_law_certificate"]
    for field in (
        "all_input_solver_completeness_certified",
        "accepted_Box_Muller_law_certified",
        "native_financial_path_arithmetic_certified",
        "coherent_loader_implemented",
        "complete_original_price_certified",
        "quantum_resources_or_runtime_extrapolated_from_classical_solver",
    ):
        assert row[field] is False


def test_unsupported_contract_rejected():
    with pytest.raises(ValueError):
        defined_law_certificate("B2x4")
