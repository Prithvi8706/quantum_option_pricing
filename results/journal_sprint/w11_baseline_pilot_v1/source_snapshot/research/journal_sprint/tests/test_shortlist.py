"""Analytic and independent quadrature checks for new classical baselines."""

import math

import numpy as np
import pytest
from scipy.integrate import quad
from scipy.stats import norm

from research.journal_sprint.asian_basket import (
    Basket, conditional_call, evaluate, estimate, lognormal_call, setup,
)
from research.journal_sprint.shortlist_diagnostics import (
    antithetic_correction, heston_conditions, heston_grid, normal_positive_mean,
)


@pytest.mark.parametrize("d,steps", [(1, 1), (2, 3), (4, 12)])
def test_covariance_reconstruction(d, steps):
    b = Basket(d, steps, 100)
    m = setup(b)
    assert m["factor"] @ m["factor"].T == pytest.approx(m["covariance"], abs=1e-12)
    assert m["residual"] @ m["residual"].T + np.outer(m["load"], m["load"]) == pytest.approx(
        m["covariance"], abs=1e-12)


def test_geometric_formula_one_asset_one_date():
    c = Basket(1, 1, 100)
    model = setup(c)
    d1 = (.03 + .3**2 / 2) / .3
    expected = 100 * norm.cdf(d1) - 100 * math.exp(-.03) * norm.cdf(d1 - .3)
    assert model["expected_control"] == pytest.approx(expected, abs=1e-12)
    z = np.random.default_rng(42).normal(size=(256, 1))
    for conditional in (False, True):
        a, g, _ = evaluate(c, model, z, conditional)
        assert a == pytest.approx(g, abs=1e-10)
    value, _ = estimate(c, model, 10, 123, "rqmc_cv", beta=1)
    assert value == pytest.approx(expected, abs=1e-12)


@pytest.mark.parametrize("strike", [80, 100, 120])
def test_conditional_against_direct_quadrature(strike):
    coeff = np.array([20., 30., 50.])
    slopes = np.array([.1, .4, .8])
    actual, residual = conditional_call(np.log(coeff)[None, :], slopes, strike)
    reference = quad(lambda z: max(float((coeff * np.exp(slopes*z)).sum()) - strike, 0)
                     * norm.pdf(z), -12, 12, epsabs=1e-8)[0]
    assert actual[0] == pytest.approx(reference, abs=2e-7)
    assert residual < 1e-8


def test_conditional_controls_expectation_by_quadrature():
    c = Basket(1, 1, 100)
    m = setup(c)
    value = quad(lambda z: float(evaluate(c, m, [[z]], True)[1][0]) * norm.pdf(z),
                 -10, 10, epsabs=1e-8)[0]
    assert value == pytest.approx(m["expected_control"], abs=1e-8)


@pytest.mark.parametrize("params", [(0, 12, 100), (2, 0, 100), (True, 2, 100),
                                     (2, 12, -1)])
def test_invalid_contract(params):
    with pytest.raises(ValueError):
        Basket(*params)


def test_invalid_conditional():
    with pytest.raises(ValueError):
        conditional_call([[0, 1]], [.1, -.1], 100)
    with pytest.raises(ValueError):
        conditional_call([[float("nan")]], [.1], 100)
    assert lognormal_call(0., 0., .5) == .5


def test_heston_screen_not_theorem_proof():
    rows = heston_grid()
    assert len(rows) == 72
    for r in rows:
        assert r["full_theorem_applicability"] == "not_established"
        if r["rho"] < 0:
            assert not r["tests"]["middle_nonnegative"]
        if r["delta"] < 1:
            assert not r["tests"]["delta_at_least_one"]
    assert heston_conditions(2, .5, .2, .3, 3)["displayed_scalar_screen"]


def test_gaussian_nested_bias_and_jensen_correction():
    exact = normal_positive_mean(.2, 1)
    direct = quad(lambda z: max(z, 0) * norm.pdf(z, .2, 1), -12, 12)[0]
    assert exact == pytest.approx(direct, abs=1e-10)
    errors = [normal_positive_mean(.2, 1 + 4 / m) - exact for m in (1, 4, 16, 64, 256)]
    assert errors == sorted(errors, reverse=True)
    assert min(errors) > 0
    x = np.random.default_rng(2).normal(size=(1000, 16))
    assert np.max(antithetic_correction(x)) < 1e-14
    # Exact finite-sample telescoping identity for a recursively halved row.
    x = x[:1]
    total = float(np.maximum(x, 0).mean())
    for width in (2, 4, 8, 16):
        total += float(antithetic_correction(x.reshape(-1, width)).mean())
    assert total == pytest.approx(max(float(x.mean()), 0), abs=1e-14)
