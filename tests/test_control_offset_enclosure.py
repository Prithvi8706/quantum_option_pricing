"""Independent finite-grid references; these checks are not the interval proof."""

from decimal import Decimal, localcontext
from itertools import product
from math import comb

import mpmath as mp
import numpy as np
import pytest
from scipy.special import ndtr

from research.journal_sprint.combined_qsp import abs_polynomial
from research.journal_sprint.control_offset_enclosure import (
    control_enclosure, control_offset_enclosure, moment_enclosure,
)
from research.journal_sprint.decimal_enclosure import Interval
from research.journal_sprint.polynomial_residual import basket_moments, polynomial_control


def parameters(d=2, q=2):
    return dict(
        means=[0.1, -0.2][:d], factor=[[0.1, -0.03], [0.07, 0.2]][:d],
        q=q, strike=0.9, radius=2.3, discount=0.97,
        low_coefficients=[0.6, -0.03, 0.4, 0.02, -0.08],
    ) | ({"factor": [[0.1]]} if d == 1 else {})


def exact_float(value):
    return mp.mpf(str(Decimal.from_float(float(value))))


def reference(p):
    """Enumerate the independent grid and evaluate Chebyshev functions directly."""
    d, n = len(p["means"]), 2**p["q"]
    edges = [mp.mpf(-4) + mp.mpf(8) * j / n for j in range(n + 1)]
    def cdf(x):
        return (1 + mp.erf(x / mp.sqrt(2))) / 2
    mass = cdf(4) - cdf(-4)
    weights = [(cdf(b) - cdf(a)) / mass for a, b in zip(edges, edges[1:])]
    nodes = [(a + b) / 2 for a, b in zip(edges, edges[1:])]
    moments, expectation = [mp.mpf(0) for _ in range(5)], mp.mpf(0)
    for indices in product(range(n), repeat=d):
        weight = mp.fprod(weights[j] for j in indices)
        basket = mp.fsum(
            mp.exp(exact_float(p["means"][i]) + mp.fsum(
                exact_float(p["factor"][i][k]) * nodes[j] for k, j in enumerate(indices)
            )) for i in range(d)
        ) / d
        for k in range(5):
            moments[k] += weight * basket**k
        x = (basket - exact_float(p["strike"])) / exact_float(p["radius"])
        low = mp.fsum(exact_float(c) * mp.chebyt(k, x)
                      for k, c in enumerate(p["low_coefficients"]))
        expectation += weight * exact_float(p["discount"]) * exact_float(p["radius"]) / 2 * (
            x + low
        )
    # Normalization gives E[1]=1 exactly; numerical grid summation need not.
    assert abs(moments[0] - 1) < mp.mpf("1e-95")
    moments[0] = mp.mpf(1)
    return moments, expectation


def contains(interval, value):
    assert mp.mpf(str(interval.lo)) <= value <= mp.mpf(str(interval.hi))


@pytest.mark.parametrize("d", [1, 2])
@pytest.mark.parametrize("q", [1, 2])
def test_direct_high_precision_grid(d, q):
    p = parameters(d, q)
    result = control_offset_enclosure(**p)
    # 100 digits keeps reference rounding below the 80-digit interval arithmetic.
    with mp.workdps(100):
        moments, value = reference(p)
        for interval, expected in zip(result["moments"], moments):
            contains(interval, expected)
        contains(result["value"], value)
    assert result["terms"] == comb(d + 4, 4)
    assert result["scope"] == "ideal_finite_midpoint_model"


def test_old_control_offset_error_includes_float_conversion():
    p = parameters()
    coefficients, tail = abs_polynomial(4)
    p["low_coefficients"] = coefficients * (1 + tail)
    edges = np.linspace(-4, 4, 5)
    nodes = (edges[:-1] + edges[1:]) / 2
    weights = np.diff(ndtr(edges)) / (ndtr(4) - ndtr(-4))
    moments, terms = basket_moments(p["means"], p["factor"], nodes, weights, 4)
    _, offset = polynomial_control(np.array([1.]), p["strike"], p["radius"],
                                   p["discount"], moments)
    result = control_offset_enclosure(**p, actual_float_offset=offset)
    assert result["terms"] == terms
    assert result["actual_float_offset_error_upper"] == (
        Interval(float(offset)) - result["value"]
    ).absolute().hi
    with mp.workdps(100):
        _, expected = reference(p)
        contains(result["value"], expected)
        assert abs(exact_float(offset) - expected) <= mp.mpf(
            str(result["actual_float_offset_error_upper"])
        )
    assert result["actual_float_offset_error_upper"] < Decimal("1e-12")


def test_exact_loading_and_ambient_context():
    p = parameters()
    p["factor"] = [[0.1, -0.1], [0.2, 0.1]]
    baseline = control_offset_enclosure(**p)
    with localcontext() as context:
        context.prec = 3
        assert control_offset_enclosure(**p) == baseline
    with mp.workdps(100):
        moments, expected = reference(p)
        contains(baseline["value"], expected)
        for interval, value in zip(baseline["moments"], moments):
            contains(interval, value)


def test_q10_dimension4_work_bound_and_cache(monkeypatch):
    calls = 0
    original = Interval.exp

    def counted(value):
        nonlocal calls
        calls += 1
        return original(value)

    monkeypatch.setattr(Interval, "exp", counted)
    result = control_offset_enclosure(
        [0.1] * 4, [[0.1] * 4 for _ in range(4)], 10, 1., 2., 0.97,
        [0.6, 0., 0.4, 0., -0.08],
    )
    work = result["work"]
    assert result["terms"] == 70
    assert work["cdf_boundaries"] == 1025
    assert calls == work["exp_calls"] == 69 + 2 * 4
    assert work["cell_visits"] == 4 * 1024
    assert work["cell_visits"] <= work["cell_visits_bound"] == 282624
    assert calls <= work["exp_calls_bound"] == 621


@pytest.mark.parametrize("key,value", [
    ("q", True), ("q", 0), ("q", 11), ("q", 1.5), ("cutoff", 3),
    ("means", []), ("means", [0.] * 5), ("factor", [[0.1]]),
    ("means", [float("nan"), 0.]), ("factor", [[0., 0.], [0., float("inf")]]),
    ("means", [251., 0.]), ("factor", [[63., 0.], [0., 0.]]),
    ("strike", -1.), ("discount", -0.1), ("radius", 0.), ("radius", -1.),
    ("discount", float("inf")), ("radius", True),
    ("low_coefficients", [0.] * 4), ("low_coefficients", [float("nan")] * 5),
    ("actual_float_offset", float("nan")),
])
def test_invalid_inputs(key, value):
    p = parameters()
    p[key] = value
    with pytest.raises(ValueError):
        control_offset_enclosure(**p)


def test_zero_discount_and_zero_loadings():
    p = parameters()
    p.update(discount=0., strike=0., means=[0., 0.], factor=[[0., 0.], [0., 0.]])
    result = control_offset_enclosure(**p, actual_float_offset=0.)
    assert result["value"] == Interval(0)
    assert result["actual_float_offset_error_upper"] == 0
    assert result["work"]["cell_visits"] == 0
    for moment in result["moments"]:
        assert moment.lo <= 1 <= moment.hi


def test_split_api_reuses_moments_and_archives_all_five(monkeypatch):
    p = parameters()
    result = moment_enclosure(p["means"], p["factor"], p["q"], L=4, degree=4)
    archived = [moment.record() for moment in result["moments"]]
    restored = tuple(Interval(item["lower"], item["upper"]) for item in archived)
    assert len(restored) == 5
    assert restored == result["moments"]

    def forbidden(*args):
        pytest.fail("control evaluation must reuse moments without transcendental work")

    monkeypatch.setattr(Interval, "exp", forbidden)
    for radius in (1.1, 2.3, 5.7):
        control = control_enclosure(restored, p["strike"], radius, p["discount"],
                                    p["low_coefficients"])
        with mp.workdps(100):
            _, expected = reference(p | {"radius": radius})
            contains(control["value"], expected)
        with localcontext() as context:
            context.prec = 100
            offset = float((control["value"].lo + control["value"].hi) / 2)
        error = (Interval(offset) - control["value"]).absolute().hi
        assert error.is_finite() and error >= 0


def test_original_four_dimensional_model_q10():
    from research.journal_sprint.asian_basket import Basket, setup

    model = setup(Basket(2, 2, 100))
    result = moment_enclosure(model["means"], model["factor"], 10)
    assert result["terms"] == 70
    assert len(result["moments"]) == 5
    for moment in result["moments"]:
        assert moment.lo > 0 and moment.hi.is_finite()
        assert (moment.hi - moment.lo) / moment.lo < Decimal("1e-50")
    assert result["work"]["exp_calls"] <= 621
    assert result["work"]["cell_visits"] <= 282624


@pytest.mark.parametrize("degree", [True, 3, 5, 4.0])
def test_invalid_degree(degree):
    with pytest.raises(ValueError):
        moment_enclosure([0.], [[0.]], 1, degree=degree)


@pytest.mark.parametrize("moments", [
    [Interval(1)] * 4, [1.] * 5, [Interval(2)] * 5,
    [Interval(1), Interval(-1), Interval(1), Interval(1), Interval(1)],
])
def test_invalid_precomputed_moments(moments):
    with pytest.raises(ValueError):
        control_enclosure(moments, 1., 2., 1., [0.] * 5)
