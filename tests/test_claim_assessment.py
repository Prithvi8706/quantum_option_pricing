"""Independent boundary, resource and exact-arithmetic checks for claim audit."""

from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

import pytest

from research.journal_sprint.claim_assessment import (
    analyze, atan_bounds, compare, pi_bounds, projected_cost, proxy_optimum,
    schedule, universal_radius,
)


@pytest.mark.parametrize("coefficients,strike", [
    ([1], 0), ([1], F(1, 2)), ([1, 2], 4), ([0, 0], 2),
    ([1, F(3, 2), 4], F(5, 4)), ([0, 0], 0),
])
def test_cube_norm_matches_all_vertices_and_reflection_lcu(coefficients, strike):
    c, k = list(map(F, coefficients)), F(strike)
    radius = universal_radius(c, k)
    assert radius == max(abs(sum((a*t for a, t in zip(c, ts)), F(0))-k)
                         for ts in product((0, 1), repeat=len(c)))
    assert radius == sum(c)/2+abs(sum(c)/2-k)
    for ts in product((F(0), F(1, 3), F(1)), repeat=len(c)):
        assert sum(a*(2*t-1)/2 for a, t in zip(c, ts))+sum(c)/2-k == sum(a*t for a, t in zip(c, ts))-k


def test_cube_optimality_does_not_imply_instance_optimality():
    assert universal_radius([1], F(3, 4)) == F(3, 4)
    # Actual domain restricted to t=1: |t-K| is only 1/4.
    assert abs(1-F(3, 4)) < universal_radius([1], F(3, 4))


def test_signed_coefficients_are_outside_theorem():
    with pytest.raises(ValueError):
        universal_radius([1, -1], 0)


def test_proxy_global_minimum_exact_difference_identity():
    g, beta, a, e = map(F, (3, 5, 7, 2))
    degree, optimum = proxy_optimum(g, beta, a, e)
    assert degree == 7
    for n in (F(15, 4), F(4), F(7), F(10), F(100)):
        cost = g*beta*n*n/(e*n-a)
        assert cost-optimum == g*beta*(e*n-2*a)**2/(e*e*(e*n-a))
        assert cost >= optimum
    with pytest.raises(ValueError):
        proxy_optimum(0, beta, a, e)


def test_rational_pi_enclosure_against_independent_directed_implementation():
    from research.journal_sprint.decimal_enclosure import pi_interval
    lo, hi = pi_bounds()
    ref = pi_interval()
    assert lo <= F(ref.lo) <= F(ref.hi) <= hi
    assert hi-lo < F(1, 10**55)
    for n in (1, 2, 9, 10):
        a, b = atan_bounds(5, n)
        c, d = atan_bounds(5, n+1)
        assert a <= c <= d <= b


def test_median_17_has_95_percent_hoeffding_guarantee():
    # exp(.18*17) >= truncated positive Taylor series > 20.
    term = F(1)
    total = term
    for k in range(1, 15):
        term *= F(306, 100)/k
        total += term
    assert total > 20


def test_schedule_boundary_cap_and_minimal_power():
    assert schedule(1, 1)["status"] == "deterministic_budget_exhausted"
    assert schedule(1, F(9, 10), extra="0.1")["status"] == "deterministic_budget_exhausted"
    assert schedule(1, 0, cap=1)["status"] == "query_cap"
    result = schedule(1, F(1, 2))
    m = result["M"]
    lo, _ = pi_bounds()
    assert 2*(lo/(m//2)+lo**2/(m//2)**2) > F(1, 2)
    assert F(result["fixed_schedule_margin_rational"]) >= 0
    with pytest.raises(ValueError):
        schedule(1, 0, extra="-0.1")


def test_full_composition_includes_inverse_and_iqft_swaps():
    resources = {"a_cx_projection": 2, "controlled_a_cx_projection": 5,
                 "zero_reflection_cx_projection": 7}
    # M=4: initial2 + three*(two*5+7+1) + two QFT rotations + three swap CX.
    assert projected_cost(resources, 4, 1) == 61
    with pytest.raises(ValueError):
        projected_cost(resources, 3)


def test_comparison_retains_refusal_and_tie():
    def row(mode, cost):
        return {"mode": mode, "degree": 16, "projected_cx": cost}
    assert compare([row("original", None), row("reflection", None)])["outcome"] == "neither_feasible"
    assert compare([row("original", 2), row("reflection", 2)])["outcome"] == "tie"
    assert compare([row("original", 1), row("reflection", 2)])["outcome"] == "original_lower_projection"


def test_upper_bound_ratio_is_not_actual_cost_ratio():
    upper_original, upper_reflection = 200, 100
    actual_original, actual_reflection = 10, 90
    assert actual_original <= upper_original and actual_reflection <= upper_reflection
    assert F(upper_original, upper_reflection) > 1
    assert F(actual_original, actual_reflection) < 1


def test_frozen_archive_complete_grid_and_fail_closed():
    base = Path(__file__).resolve().parents[1]/"results/journal_sprint"
    def read(name):
        return json.loads((base/name).read_text(encoding="utf-8"))
    production = read("minimal_pivot_week2_production_v1/results.json")
    analysis = read("minimal_pivot_week2_analysis_v2.json")
    tiny = read("minimal_pivot_week2_tiny_v2/results.json")
    report = analyze(production, analysis, tiny)
    assert len(report["cells"]) == 72
    assert sum(len(c["all_plans"]) for c in report["cells"]) == 576
    assert not report["confirmation_admitted"]
    assert not report["quantum_over_classical_advantage_established"]
    production["rows"].pop()
    with pytest.raises(ValueError, match="grid"):
        analyze(production, analysis, tiny)
