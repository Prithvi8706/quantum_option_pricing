"""Numerical cross-checks are regression tests, not the interval proof itself."""

from decimal import Decimal, localcontext
from fractions import Fraction
import math

import mpmath as mp
import pytest

from research.journal_sprint.asian_basket import Basket, setup, lognormal_call
from research.journal_sprint.asian_encoding import analytic_bounds, grid, price_contract
from research.journal_sprint.decimal_enclosure import Interval, normal_cdf, pi_interval
from research.journal_sprint.encoding_enclosure import (
    at_precision,
    base_enclosure,
    screened_contract,
    upward_float,
)


def contains(interval, value):
    assert mp.mpf(str(interval.lo)) <= value <= mp.mpf(str(interval.hi))


@pytest.mark.parametrize("x", [-10, -8, -6, -3, -0.1, 0, 0.1, 3, 6, 8, 10])
def test_cdf_against_high_precision_reference(x):
    with mp.workdps(130):
        exact = mp.mpf(str(Decimal.from_float(x))) if isinstance(x, float) else mp.mpf(x)
        contains(normal_cdf(x), (1 + mp.erf(exact / mp.sqrt(2))) / 2)


def test_pi_and_transcendentals():
    with mp.workdps(130):
        contains(pi_interval(), mp.pi)
        for x in ("0.001", "2", "100"):
            contains(Interval(x).sqrt(), mp.sqrt(mp.mpf(x)))
            contains(Interval(x).ln(), mp.log(mp.mpf(x)))
            contains(Interval(x).exp(), mp.exp(mp.mpf(x)))


def test_independent_of_ambient_context_and_negation():
    baseline = base_enclosure(Basket(1, 2, 100), setup(Basket(1, 2, 100)), 4, "residual")
    with localcontext() as context:
        context.prec = 3
        precise = Interval("1.123456789012345678901234567890123456789")
        assert (-precise).lo == precise.hi.copy_negate()
        changed = base_enclosure(Basket(1, 2, 100), setup(Basket(1, 2, 100)), 4, "residual")
        assert at_precision(changed, 8) == at_precision(baseline, 8)


@pytest.mark.parametrize("a,b", [("-0.3", "0.7"), ("1e-40", "2.9"), ("-7", "-2")])
def test_basic_arithmetic(a, b):
    # Exact rational references handle zero-width decimal results without
    # confusing mpmath's own rounding with an enclosure failure.
    x, y = Fraction(a), Fraction(b)
    for interval, exact in (
        (Interval(a) + Interval(b), x + y),
        (Interval(a) - Interval(b), x - y),
        (Interval(a) * Interval(b), x * y),
        (Interval(a) / Interval(b), x / y),
    ):
        assert Fraction(interval.lo) <= exact <= Fraction(interval.hi)


@pytest.mark.parametrize("bad", [True, float("inf"), float("nan")])
def test_invalid_endpoints(bad):
    with pytest.raises(ValueError):
        Interval(bad)


def test_domain_errors():
    for operation in (
        lambda: Interval(2, 1),
        lambda: Interval(1) / Interval(-1, 1),
        lambda: Interval(-1).sqrt(),
        lambda: Interval(0).ln(),
        lambda: normal_cdf(11),
        lambda: Interval(1001).exp(),
        lambda: Interval(2) ** -1,
    ):
        with pytest.raises(ValueError):
            operation()


@pytest.mark.parametrize("rep", ["raw", "residual"])
def test_improves_existing_bound_and_keeps_unknowns(rep):
    contract = Basket(2, 2, 100)
    data = grid(contract, 1, 3)
    base = base_enclosure(contract, data["model"], 3, rep)
    record = at_precision(base, 1)
    old = analytic_bounds(contract, 1, 3, data["model"], rep)
    assert float(record["tail"]["upper"]) < old["tail_and_renormalization"]
    assert float(record["discretization"]["upper"]) < old["discretization"]
    assert float(record["bridge"]["upper"]) < 1e-9
    original = price_contract(contract, 1, 3, data, rep)
    amended = screened_contract(original, record)
    assert amended.readiness(1) == "unknown_bias"
    assert original.readiness(1) == "unknown_bias"
    with pytest.raises(ValueError):
        amended.to_encoding(16)
    assert not record["application_admitted"]
    assert record["payoff_table_entries"] == "16"
    assert Decimal.from_float(float(data[rep].max())) < Decimal(record["safe_cube_scale"]["upper"])


def test_precision_without_exponential_enumeration():
    contract = Basket(2, 12, 100)
    base = base_enclosure(contract, setup(contract), 4, "raw")
    low, high = at_precision(base, 8), at_precision(base, 12)
    assert Decimal(high["discretization"]["upper"]) < Decimal(low["discretization"]["upper"])
    assert high["normal_qubits"] == 288
    assert high["payoff_table_entries"] == str(2**288)


def test_rounding_bridge_covers_perturbed_one_date_model():
    contract = Basket(1, 1, 100)
    model = setup(contract)
    model["factor"] *= 1.01
    model["means"] += 0.001
    bound = base_enclosure(contract, model, 4, "raw")["bridge"].hi
    target = lognormal_call(math.log(100) + (0.03 - 0.3**2 / 2), 0.3**2, 100)
    approximate = lognormal_call(model["means"][0], model["factor"][0, 0] ** 2, 100)
    assert abs(target - approximate) * math.exp(-0.03) < float(bound)


@pytest.mark.parametrize("q", [True, 0, 33, 1.5])
def test_invalid_precision(q):
    with pytest.raises(ValueError):
        at_precision({}, q)


def test_upward_float_is_not_downward():
    exact = Decimal("0.1")
    assert Decimal.from_float(upward_float(exact)) >= exact
    assert Decimal.from_float(upward_float(Decimal("1e-400"))) >= Decimal("1e-400")
    with pytest.raises(ValueError):
        upward_float(Decimal("1e400"))


def test_invalid_model():
    contract = Basket(1, 2, 100)
    for key, value in (("means", [1]), ("factor", [[1], [2]])):
        model = setup(contract)
        model[key] = value
        with pytest.raises(ValueError):
            base_enclosure(contract, model, 3, "raw")
