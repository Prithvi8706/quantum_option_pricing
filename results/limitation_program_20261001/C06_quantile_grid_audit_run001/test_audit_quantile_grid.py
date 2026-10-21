"""Independent exact algebra fixtures; no financial path or quantum simulation."""

from copy import deepcopy
from fractions import Fraction
from itertools import combinations_with_replacement, product

import pytest

from research.limitation_program_20261001.audit_quantile_grid import (
    BUILDER,
    CASES,
    PROGRAM,
    audit_builder_contract,
    audit_grid_certificate,
    knockout_variation,
    pair,
    rational,
    read,
    step_midpoint_profile,
)


@pytest.mark.parametrize("cells", [2, 4])
def test_midpoint_bv_lemma_exhausts_small_rational_step_functions(cells):
    # All 3**4 and 3**8 right-continuous step functions, including jumps
    # precisely at every midpoint. This is an algebraic quadrature fixture.
    for values in product((0, 1, 2), repeat=2 * cells):
        profile = step_midpoint_profile(values)
        assert profile["absolute_error"] <= profile["midpoint_BV_upper"]


def test_strict_midpoint_knockout_attains_the_half_cell_variation_bound():
    profile = step_midpoint_profile([40, 0])
    assert profile["integral"] == 20
    assert profile["midpoint"] == 0
    assert profile["absolute_error"] == profile["midpoint_BV_upper"] == 20


def test_monotone_survival_then_knockout_variation_exhausts_small_prefixes():
    for length in range(1, 9):
        for prefix in combinations_with_replacement((0, 20, 40), length):
            assert knockout_variation(prefix, 40) <= 80
    assert knockout_variation([0, 40], 40) == 80


@pytest.mark.parametrize("prefix,cap", [([], 40), ([0, 41], 40), ([20, 0], 40), ([0], -1)])
def test_variation_requires_monotone_bounded_surviving_payoff(prefix, cap):
    with pytest.raises(ValueError):
        knockout_variation(prefix, cap)


def test_original_builder_positive_averages_and_strict_barrier_bind_independently():
    checked = audit_builder_contract(BUILDER)
    assert checked["positive_increment_coefficients_and_average_template_checked"]
    assert checked["strict_less_than_survival_template_checked"]
    assert not checked["native_clipping_exp_and_rounding_accuracy_audited"]


@pytest.mark.parametrize(
    "before,after",
    [
        ("SIGMA * math.sqrt(dt * CORR)", "-SIGMA * math.sqrt(dt * CORR)"),
        ("1 / (na * nt)", "-1 / (na * nt)"),
        ("g.lt(tree(g, baskets, g.maximum), g.c(H))", "g.lt(g.c(H), tree(g, baskets, g.maximum))"),
        ("math.exp(-RATE * T)", "math.exp(RATE * T)"),
    ],
)
def test_changed_economic_template_fails_independent_ast_check(tmp_path, before, after):
    path = tmp_path / "changed_builder.py"
    text = BUILDER.read_text(encoding="utf-8")
    assert before in text
    path.write_text(text.replace(before, after), encoding="utf-8")
    with pytest.raises(ValueError):
        audit_builder_contract(path)


@pytest.mark.parametrize("case", list(CASES))
def test_frozen_certificates_match_independently_derived_exact_product_bound(case):
    # Merely reconcile the saved theorem; no producer theorem function called.
    result = audit_grid_certificate(
        read(PROGRAM / "C06_quantile_grid_run001" / (case + "_certificate.json")),
        read(PROGRAM / "G0_run003" / (case + "_task.json")),
    )
    assets, dates = CASES[case]
    assert result["independently_derived_midpoint_grid_bias_upper_exact"] == pair(
        Fraction(40 * (assets + 1) * dates, 2**32)
    )
    assert not result["complete_continuous_price_certified"]


@pytest.mark.parametrize(
    "fault",
    ["dimension", "bound", "cap", "model", "law", "bits", "native", "strict", "economic"],
)
def test_changed_bound_law_model_or_transfer_claim_is_rejected(fault):
    case = "B4x12"
    certificate = deepcopy(
        read(PROGRAM / "C06_quantile_grid_run001" / (case + "_certificate.json"))
    )
    task = deepcopy(read(PROGRAM / "G0_run003" / (case + "_task.json")))
    if fault == "dimension":
        certificate["normal_coordinates"] -= 1
    elif fault == "bound":
        certificate["all_date_continuous_payoff_grid_law_error_upper_dollars_exact"] = [0, 1]
    elif fault == "cap":
        certificate["coordinate_total_variation_upper_dollars_exact"] = [40, 1]
    elif fault == "model":
        certificate["original_model_binding"]["basket"] = "signed basket weights"
    elif fault == "law":
        certificate["ideal_law"] = "paired finite Box-Muller"
    elif fault == "bits":
        certificate["uniform_bits"] = 33
    elif fault == "native":
        certificate["native_rounded_inverse_CDF_or_path_certified"] = True
    elif fault == "strict":
        task["barrier_equality"] = "ties survive"
    else:
        task["annual_rate"] = 0.04
    with pytest.raises(ValueError):
        audit_grid_certificate(certificate, task)


@pytest.mark.parametrize("value", [True, 0.1, [1, 0], [1.0, 2]])
def test_audit_rationals_reject_inexact_inputs(value):
    with pytest.raises(ValueError):
        rational(value)
