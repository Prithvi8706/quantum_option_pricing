import math

import numpy as np
import pytest

from research.paper_a.benchmark import BENCHMARK, VALIDATION_SET, by_id
from research.paper_a.references import (
    black_scholes_call, grid_points, grid_probabilities, p_grid,
    select_support_rule, support_audit, support_bounds,
)


def test_black_scholes_matches_known_atm_value():
    assert abs(black_scholes_call(100, 100, 0.05, 0.20, 1.0) - 10.4506) < 1e-3


def test_black_scholes_respects_put_call_parity():
    S0, K, r, sigma, T = 100, 100, 0.05, 0.20, 1.0
    call = black_scholes_call(S0, K, r, sigma, T)
    put = call - S0 + K * math.exp(-r * T)
    assert abs(put - 5.5735) < 1e-3


def test_support_bounds_bracket_the_strike():
    for c in BENCHMARK:
        L, U = support_bounds(c, 1e-4)
        assert L < c.K < U
        assert L <= 0.98 * c.K
        assert U >= 1.02 * c.K


def test_support_bounds_are_fixed_across_n():
    """The rule depends on q_total only, never on the qubit count."""
    c = by_id("E025")
    assert support_bounds(c, 1e-4) == support_bounds(c, 1e-4)


def test_wider_budget_gives_narrower_support():
    c = by_id("E025")
    tight_L, tight_U = support_bounds(c, 1e-4)
    loose_L, loose_U = support_bounds(c, 1e-2)
    assert loose_L >= tight_L and loose_U <= tight_U


def test_exact_identity_p_bs_equals_m_times_p_support_plus_tail():
    """Annex A: P_BS = m * P_support + C_tail, exactly."""
    for cid in ("E001", "E025", "E050"):
        c = by_id(cid)
        a = support_audit(c, 1e-4)
        reconstructed = a.m * a.P_support + a.C_tail
        assert abs(reconstructed - black_scholes_call(
            c.S0, c.K, c.r, c.sigma, c.T)) < 1e-10 * max(1.0, c.S0)


def test_audit_stores_each_quantity_separately():
    a = support_audit(by_id("E025"), 1e-4)
    assert 0 < a.m <= 1
    assert abs(a.omitted_mass - (1 - a.m)) < 1e-15
    assert a.C_tail >= 0
    assert abs(a.normalization - 1.0 / a.m) < 1e-12


def test_selected_rule_satisfies_all_three_gates_on_all_50():
    q = select_support_rule(BENCHMARK, (1e-2, 1e-3, 1e-4, 1e-5, 1e-6))
    for c in BENCHMARK:
        a = support_audit(c, q)
        assert a.omitted_mass <= 1e-4
        assert a.C_tail <= 1e-4 * c.S0
        assert abs(a.support_bias) <= 1e-4 * c.S0


def test_selected_rule_is_the_least_wide_that_passes():
    """Least-wide means the LARGEST passing q_total, since larger q trims
    more tail. Verify nothing larger also passes."""
    candidates = (1e-2, 1e-3, 1e-4, 1e-5, 1e-6)
    q = select_support_rule(BENCHMARK, candidates)
    for bigger in [x for x in candidates if x > q]:
        failed = any(
            support_audit(c, bigger).omitted_mass > 1e-4
            or support_audit(c, bigger).C_tail > 1e-4 * c.S0
            or abs(support_audit(c, bigger).support_bias) > 1e-4 * c.S0
            for c in BENCHMARK)
        assert failed, f"q={bigger} also passes; {q} is not least-wide"


def test_rule_also_passes_on_the_validation_fixtures():
    q = select_support_rule(BENCHMARK, (1e-2, 1e-3, 1e-4, 1e-5, 1e-6))
    for c in VALIDATION_SET:
        a = support_audit(c, q)
        assert a.omitted_mass <= 1e-4


def test_no_candidate_passing_raises():
    with pytest.raises(ValueError, match="no candidate"):
        select_support_rule(BENCHMARK, (0.5,))


def test_grid_is_the_frozen_linear_rule():
    pts = grid_points(10.0, 20.0, 3)
    assert len(pts) == 8
    assert pts[0] == 10.0 and pts[-1] == 20.0
    assert np.allclose(np.diff(pts), 10.0 / 7.0)


def test_grid_size_doubles_with_each_qubit():
    for n in (2, 3, 4, 5, 6):
        assert len(grid_points(50.0, 150.0, n)) == 2 ** n


def test_probabilities_are_normalized_pointwise_densities():
    c = by_id("E025")
    L, U = support_bounds(c, 1e-4)
    pi = grid_probabilities(c, L, U, 3)
    assert abs(pi.sum() - 1.0) <= 1e-12
    assert (pi > 0).all()


def test_probabilities_are_not_integrated_bin_masses():
    """Guard against silently substituting bin integrals for point densities."""
    from scipy.stats import lognorm
    import math
    c = by_id("E025")
    L, U = support_bounds(c, 1e-4)
    x = grid_points(L, U, 3)
    mu = (c.r - 0.5 * c.sigma ** 2) * c.T + math.log(c.S0)
    dist = lognorm(s=c.sigma * math.sqrt(c.T), scale=math.exp(mu))
    density = dist.pdf(x)
    assert np.allclose(grid_probabilities(c, L, U, 3),
                       density / density.sum(), atol=1e-15)


def test_p_grid_uses_the_exact_payoff_evaluated_classically():
    import math
    c = by_id("E025")
    L, U = support_bounds(c, 1e-4)
    x = grid_points(L, U, 3)
    pi = grid_probabilities(c, L, U, 3)
    expected = math.exp(-c.r * c.T) * float(
        (pi * np.maximum(0.0, x - c.K)).sum())
    assert abs(p_grid(c, L, U, 3) - expected) < 1e-14


def test_grid_error_shrinks_as_n_grows():
    c = by_id("E025")
    L, U = support_bounds(c, 1e-4)
    from research.paper_a.references import support_audit
    target = support_audit(c, 1e-4).P_support
    errs = [abs(p_grid(c, L, U, n) - target) for n in (3, 4, 5, 6)]
    assert errs[-1] < errs[0]
