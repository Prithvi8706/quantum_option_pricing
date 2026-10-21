"""Exact finite-law fixtures for a conditional AS241 Gaussian-law transfer."""

from copy import deepcopy
from fractions import Fraction
from itertools import product

import pytest

from research.limitation_program_20261001.quantile_as241_law_certificate import (
    CASES,
    TERMS,
    TARGET,
    gaussian_density_proof,
    law_bound,
    pair,
    validate_native_error,
)


def model(case="B4x12"):
    assets, dates = CASES[case]
    return {
        "case": case,
        "assets": assets,
        "dates": dates,
        **{name: pair(value) for name, value in TERMS.items()},
        "equal_asset_volatility": True,
        "basket": "positive equal-weight arithmetic spot basket",
        "continuous_driver_law": "independent common and idiosyncratic Brownian drivers",
        "digital_paired_outputs_claimed_independent_gaussian": False,
    }


def native_fixture():
    rho, real, arithmetic, central = map(Fraction, ("1e-11", "2e-10", "3e-10", "7e-9"))
    certificate = {
        "certified": True,
        "budget_censored": False,
        "actual_q32_native_transform_error_included": True,
        "exact_transform_hypothesis_replaced_by_mathematical_native_arithmetic": True,
        "native_financial_path_arithmetic_certified": False,
        "coherent_loader_implemented_or_adopted": False,
        "accepted_Box_Muller_baseline_changed": False,
        "full_G2_closed": False,
        "actual_coherent_leaf_or_quantum_gate_cost": None,
        "transform": {
            "normalization": {
                "all_q32_tail_words_covered": True,
                "enumerated_q32_words_as_completeness_proof": 0,
            },
            "continuous_uniform_midpoint_coupling_error_included": False,
            "radial_cutoff_or_bad_event_used": False,
            "cell_exponent_cover": [
                {"table_cell": cell, "exponent": exponent}
                for cell in range(32)
                for exponent in range(-33, -3)
            ],
            "native_transform_error_upper_exact": pair(rho),
        },
        "actual_native_tail_quantile_error_upper_exact": pair(real + arithmetic),
        "central_quantile_error_upper_exact": pair(central),
        "combined_mathematical_native_quantile_error_upper_exact": pair(central),
        "required_uniform_quantile_error_exact": pair(TARGET),
    }
    rows = [
        {
            "cell_index": index,
            "saved_real_approximation_error_upper_exact": pair(real),
            "fresh_native_rational_error_upper_exact": pair(arithmetic),
            "actual_native_tail_quantile_error_upper_exact": pair(real + arithmetic),
            "argument_perturbation_upper_exact": pair(rho),
            "previous_conditional_floor_arithmetic_error_added": False,
            "actual_sqrt_floor_and_shift_error_only_in_rho": True,
        }
        for index in range(1024)
    ]
    return certificate, {"fixed_rows": 1024, "completed_rows": 1024, "rows": rows}


def cdf(values, threshold, strict=False):
    return Fraction(
        sum(value < threshold if strict else value <= threshold for value in values), len(values)
    )


def ks(left, right):
    return max(
        abs(cdf(left, threshold, strict) - cdf(right, threshold, strict))
        for threshold in set(left + right)
        for strict in (False, True)
    )


@pytest.mark.parametrize("case,dimension", [("B4x12", 60), ("B8x52", 468)])
def test_exact_uniform_error_to_dollars_and_separate_allowance(case, dimension):
    error = Fraction(7, 10**9)
    row = law_bound(model(case), error)
    expected_ks = Fraction(1, 2**33) + Fraction(2, 5) * error
    assert Fraction(*row["scalar_Gaussian_KS_error_upper_exact"]) == expected_ks
    assert Fraction(*row["ideal_GBM_new_law_price_bias_upper_dollars_exact"]) == (
        80 * dimension * expected_ks
    )
    assert row["new_law_bias_fits_separate_exploratory_allowance"]
    assert Fraction(*row["separate_exploratory_law_allowance_dollars_exact"]) == Fraction(1, 1000)
    assert not row["new_law_monotonicity_required"]
    assert not row["previous_exact_floor_quantile_law_ULP_added"]
    for field in (
        "accepted_Box_Muller_law_certified",
        "accepted_Box_Muller_baseline_changed",
        "native_financial_exp_clipping_or_path_certified",
        "coherent_divider_or_loader_adopted",
        "complete_original_price_certified",
        "full_G2_closed",
        "quantum_advantage_established",
        "second_discount_applied",
    ):
        assert row[field] is False
    assert row["actual_quantum_gate_cost"] is None
    assert row["native_financial_price_error_bound"] is None


def test_zero_approximation_error_recovers_exact_midpoint_law_bound():
    row = law_bound(model(), Fraction(0))
    assert Fraction(*row["ideal_GBM_new_law_price_bias_upper_dollars_exact"]) == Fraction(
        60 * 40, 2**32
    )


def test_worst_allowed_quantile_error_still_fits_fixed_exploratory_allowance():
    row = law_bound(model("B8x52"), TARGET)
    assert Fraction(*row["ideal_GBM_new_law_price_bias_upper_dollars_exact"]) < Fraction(1, 1000)
    assert Fraction(*row["quantile_displacement_KS_error_upper_exact"]) == Fraction(1, 250000000)


def test_nonmonotone_outputs_cdf_sandwich_including_atoms_and_left_limits():
    original = tuple(map(Fraction, (-1, 0, 1, 2)))
    new = (Fraction(-1), Fraction(1, 2), Fraction(1, 4), Fraction(2))
    error = Fraction(3, 4)
    assert new[1] > new[2]
    assert max(abs(a - b) for a, b in zip(original, new, strict=True)) == error
    thresholds = sorted(set(original + new + tuple(x - error for x in original)))
    thresholds += [Fraction(7, 8), Fraction(-2), Fraction(3)]
    for threshold in thresholds:
        for strict in (False, True):
            assert cdf(original, threshold - error, strict) <= cdf(new, threshold, strict)
            assert cdf(new, threshold, strict) <= cdf(original, threshold + error, strict)


@pytest.mark.parametrize("strict", [False, True])
def test_halfline_indicator_difference_is_paid_at_discrete_equality(strict):
    left = (Fraction(0), Fraction(1), Fraction(2))
    right = (Fraction(0), Fraction(3, 2), Fraction(2))
    distance = ks(left, right)
    assert distance == Fraction(1, 3)
    for threshold in set(left + right):
        assert abs(cdf(left, threshold, strict) - cdf(right, threshold, strict)) <= distance


def test_exact_two_coordinate_product_telescope_with_strict_knockout():
    left = (Fraction(0), Fraction(1), Fraction(2))
    right = (Fraction(0), Fraction(3, 2), Fraction(2))

    def payoff(x, y):
        # Abstract bounded-variation fixture, not a financial path observation.
        return min(max(x + y - 1, Fraction(0)), Fraction(1)) if max(x, y) < 2 else Fraction(0)

    def expectation(first, second):
        return sum((payoff(x, y) for x, y in product(first, second)), Fraction(0)) / (
            len(first) * len(second)
        )

    initial, mixed, final = (
        expectation(left, left),
        expectation(right, left),
        expectation(right, right),
    )
    per_coordinate = 2 * ks(left, right)
    assert abs(initial - mixed) <= per_coordinate
    assert abs(mixed - final) <= per_coordinate
    assert abs(initial - final) <= 2 * per_coordinate


@pytest.mark.parametrize("bad", [-1, 0.0, True, Fraction(1, 10**7)])
def test_nonexact_negative_or_failed_error_premise_rejected(bad):
    with pytest.raises(ValueError):
        law_bound(model(), bad)


@pytest.mark.parametrize("field", ["barrier_dollars_exact", "correlation_exact", "rate_exact"])
def test_original_economic_parameter_mutation_rejected(field):
    changed = model()
    changed[field] = pair(TERMS[field] + 1)
    with pytest.raises(ValueError):
        law_bound(changed, TARGET)


@pytest.mark.parametrize(
    "field,value",
    [
        ("equal_asset_volatility", False),
        ("basket", "negative-weight spread"),
        ("continuous_driver_law", "dependent finite Box-Muller pairs"),
        ("digital_paired_outputs_claimed_independent_gaussian", True),
    ],
)
def test_independence_and_positive_coordinate_template_mutations_rejected(field, value):
    changed = model()
    changed[field] = value
    with pytest.raises(ValueError):
        law_bound(changed, TARGET)


def test_successful_all_input_transform_and_fresh_row_maxima_reconcile():
    certificate, rows = native_fixture()
    assert validate_native_error(certificate, rows) == Fraction(7, 10**9)


@pytest.mark.parametrize(
    "field,value",
    [
        ("certified", False),
        ("budget_censored", True),
        ("actual_q32_native_transform_error_included", False),
        ("exact_transform_hypothesis_replaced_by_mathematical_native_arithmetic", False),
        ("native_financial_path_arithmetic_certified", True),
        ("actual_coherent_leaf_or_quantum_gate_cost", 0),
    ],
)
def test_failed_transform_or_scope_promotion_rejected(field, value):
    certificate, rows = native_fixture()
    certificate[field] = value
    with pytest.raises(ValueError):
        validate_native_error(certificate, rows)


@pytest.mark.parametrize("kind", ["missing", "duplicate"])
def test_incomplete_or_duplicate_exponent_cover_rejected(kind):
    certificate, rows = native_fixture()
    cover = certificate["transform"]["cell_exponent_cover"]
    if kind == "missing":
        cover.pop()
    else:
        cover[-1] = deepcopy(cover[0])
    with pytest.raises(ValueError):
        validate_native_error(certificate, rows)


@pytest.mark.parametrize("kind", ["missing", "sum", "rho", "double_count", "floor_scope"])
def test_fresh_rational_sensitivity_ledger_mutation_rejected(kind):
    certificate, fresh = native_fixture()
    row = fresh["rows"][0]
    if kind == "missing":
        fresh["rows"].pop()
    elif kind == "sum":
        row["actual_native_tail_quantile_error_upper_exact"] = [1, 10**9]
    elif kind == "rho":
        row["argument_perturbation_upper_exact"] = [0, 1]
    elif kind == "double_count":
        row["previous_conditional_floor_arithmetic_error_added"] = True
    else:
        row["actual_sqrt_floor_and_shift_error_only_in_rho"] = False
    with pytest.raises(ValueError):
        validate_native_error(certificate, fresh)


@pytest.mark.parametrize(
    "field",
    [
        "actual_native_tail_quantile_error_upper_exact",
        "combined_mathematical_native_quantile_error_upper_exact",
    ],
)
def test_forged_saved_maximum_rejected(field):
    certificate, rows = native_fixture()
    certificate[field] = [0, 1]
    with pytest.raises(ValueError):
        validate_native_error(certificate, rows)


def test_exact_machin_lower_bound_proves_gaussian_density_constant():
    proof = gaussian_density_proof()
    lower = Fraction(*proof["Machin_alternating_lower_bound_exact"])
    assert lower > Fraction(25, 8)
    assert 2 * lower > 1 / Fraction(2, 5) ** 2
    assert proof["numerical_Gaussian_evaluations"] == 0
