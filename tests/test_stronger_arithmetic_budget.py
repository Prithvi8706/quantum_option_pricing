"""Independent high-precision checks of the directed range-reduction ledger."""

from decimal import Decimal as D, ROUND_FLOOR, localcontext  # noqa: N817
from itertools import product
from math import factorial

import pytest

from research.stronger_arithmetic.budget import (
    evaluate_reduced_integer,
    reduced_exp_budget,
    reduced_plan,
)


def decimal_map(x, coefficients, bits, reductions, spot):
    """Decimal arithmetic with explicit floor at every integer operation."""
    scale = D(2) ** bits

    def floor(v):
        return v.to_integral_value(rounding=ROUND_FLOOR)

    z = floor(D(x) / (D(2) ** reductions))
    y = D(coefficients[-1])
    for c in reversed(coefficients[:-1]):
        y = floor(z * y / scale) + D(c)
    for _ in range(reductions):
        y = floor(y * y / scale)
    return int(spot * y)


@pytest.mark.parametrize("reductions", [0, 1, 2, 3])
@pytest.mark.parametrize("degree,bits,spot", [(1, 3, 1), (4, 5, 7), (8, 8, 100)])
def test_exhaustive_signed_integer_map_and_exp_certificate(reductions, degree, bits, spot):
    scale = 1 << bits
    certificate = reduced_exp_budget(2, "0.03125", degree, bits, 32, reductions, spot)
    cs = certificate["coefficients"]
    assert cs == tuple(scale // factorial(k) for k in range(degree + 1))
    assert certificate["overflow_safe"]
    with localcontext() as ctx:
        ctx.prec = 120
        for x in range(-2 * scale, 2 * scale + 1):
            actual = evaluate_reduced_integer(x, cs, bits, reductions, spot)
            assert actual == decimal_map(x, cs, bits, reductions, spot)
            lo, hi = certificate["output_integer_bounds"]
            assert lo <= actual <= hi
            for delta in (D("-0.03125"), D(0), D("0.03125")):
                truth_x = D(x) / scale + delta
                if abs(truth_x) <= 2:
                    assert abs(D(actual) / scale - spot * truth_x.exp()) <= D(
                        certificate["total_error_upper"]
                    )


def test_negative_shift_and_exact_spot_semantics():
    # -1 // 4 == -1, while truncation toward zero would give 0.
    assert evaluate_reduced_integer(-1, (16, 16), 4, 2, 7) == 84
    budget = reduced_exp_budget(1, 0, 4, 4, 16, 2, 7)
    assert D(budget["shift_rounding_upper"]) >= D(3) / 64
    assert budget["spot_rounding_error_upper"] == "0"
    assert D(reduced_exp_budget(1, 0, 4, 4, 16, 0)["shift_rounding_upper"]) == 0


def test_all_intermediate_ranges_and_stage_errors():
    bits, reductions, spot = 6, 3, 9
    scale = 1 << bits
    b = reduced_exp_budget(3, 0, 6, bits, 24, reductions, spot)
    with localcontext() as ctx:
        ctx.prec = 120
        for x in range(-3 * scale, 3 * scale + 1):
            z, y = x // (1 << reductions), b["coefficients"][-1]
            for c, stage in zip(reversed(b["coefficients"][:-1]), b["horner_stages"]):
                raw = z * y
                assert (
                    stage["product_integer_bounds"][0] <= raw <= stage["product_integer_bounds"][1]
                )
                y = raw // scale
                assert (
                    stage["multiplied_integer_bounds"][0]
                    <= y
                    <= stage["multiplied_integer_bounds"][1]
                )
                y += c
                assert stage["output_integer_bounds"][0] <= y <= stage["output_integer_bounds"][1]
            for j, stage in enumerate(b["squaring_stages"], 1):
                raw = y * y
                assert (
                    stage["product_integer_bounds"][0] <= raw <= stage["product_integer_bounds"][1]
                )
                y = raw // scale
                target = (D(x) / scale / (1 << (reductions - j))).exp()
                assert target <= D(stage["exact_magnitude_upper"])
                assert abs(D(y) / scale - target) <= D(stage["error_upper"])
                assert abs(D(y) / scale) <= D(stage["approximate_magnitude_upper"])


@pytest.mark.parametrize("spot", [1, 7, 100])
@pytest.mark.parametrize("reductions", [0, 2])
def test_spot_shift_add_prefixes_for_both_signs(spot, reductions):
    b = reduced_exp_budget(3, 0, 1, 4, 24, reductions, spot)
    assert b["overflow_safe"]
    lower, upper = b["spot_prefix_integer_bounds"]
    shifts = [k for k in range(spot.bit_length()) if (spot >> k) & 1]
    for x in range(-48, 49):
        y = decimal_map(x, b["coefficients"], 4, reductions, 1)
        # Every subset is a possible prefix of some ordering of the set bits.
        for selected in product((False, True), repeat=len(shifts)):
            prefix = sum((y << k) for k, use in zip(shifts, selected) if use)
            assert lower <= prefix <= upper
            assert -(1 << 23) <= prefix < 1 << 23
        assert lower <= spot * y <= upper
    assert b["output_nonnegative"] == (reductions > 0)


@pytest.mark.parametrize("reductions", [0, 1, 3])
def test_full_plan_independent_decimal_payoffs(reductions):
    means, factors = [4.6, 4.59], [[0.2, -0.1], [0.1, 0.2]]
    p = reduced_plan(
        means,
        factors,
        normal_bits=2,
        fraction_bits=24,
        width=48,
        degree=12,
        reductions=reductions,
        discount="0.97",
    )
    assert p["overflow_safe"] and not p["application_admitted"]
    with localcontext() as ctx:
        ctx.prec = 120
        scale = 1 << p["fraction_bits"]
        for indices in product(range(4), repeat=2):
            bits = [(v >> k) & 1 for v in indices for k in range(2)]
            prices, truth = [], D(0)
            for mean, row, (a, cs) in zip(means, factors, p["affine_rows"]):
                x = a + sum(b * c for b, c in zip(bits, cs))
                log = (
                    D.from_float(mean)
                    - D(100).ln()
                    + sum(D.from_float(c) * (-3 + 2 * v) for c, v in zip(row, indices))
                )
                assert abs(D(x) / scale - log) <= D(p["log_quantization_error_upper"])
                prices.append(decimal_map(x, p["exp_budget"]["coefficients"], 24, reductions, 100))
                truth += 100 * log.exp()
            total = sum(prices)
            assert p["sum_integer_bounds"][0] <= total <= p["sum_integer_bounds"][1]
            poststrike = total - p["strike_sum"]
            assert (
                p["poststrike_integer_bounds"][0] <= poststrike <= p["poststrike_integer_bounds"][1]
            )
            payoff = max(poststrike, 0)
            assert payoff <= p["payoff_upper_integer"] < 1 << p["selector_bits"]
            observed = D("0.97") * abs(D(payoff) / scale / 2 - max(truth / 2 - 100, 0))
            assert observed <= D(p["arithmetic_price_error_upper"])
        exact_sensitivity = D("0.97") * (1 << p["selector_bits"]) / scale / 2
        assert D(p["sensitivity_upper"]) >= exact_sensitivity


def test_overflow_coefficients_input_products_and_spot():
    # c_0=scale itself cannot fit, even if a selected input gives zero.
    assert not reduced_exp_budget(0, 0, 1, 7, 8, 0, 1)["overflow_safe"]
    assert not reduced_exp_budget(16, 0, 2, 4, 8, 4, 1)["overflow_safe"]
    # The multiply before coefficient addition underflows: -9*16=-144.
    b = reduced_exp_budget(9, 0, 1, 4, 8, 0, 1)
    assert not b["overflow_safe"]
    assert b["horner_stages"][0]["multiplied_integer_bounds"][0] < -128
    assert not reduced_exp_budget(0, 0, 2, 4, 8, 1, 8)["overflow_safe"]
    # Unscaled full product can exceed a word and still fit double-width scratch.
    b = reduced_exp_budget(1, 0, 4, 4, 8, 1, 1)
    assert b["overflow_safe"]
    assert 127 < b["product_integer_magnitude_upper"] < 1 << 15


def test_sum_and_negative_poststrike_overflow_and_zero_payoff():
    p = reduced_plan(
        [0],
        [[1]],
        cutoff=2,
        normal_bits=1,
        fraction_bits=4,
        width=8,
        degree=1,
        reductions=0,
        spot=1,
        strike=7,
    )
    assert p["exp_budget"]["overflow_safe"]
    assert p["strike_sum"] <= 127
    assert p["poststrike_integer_bounds"][0] < -128
    assert not p["overflow_safe"]
    p = reduced_plan(
        [2, 2], [[0, 0], [0, 0]], fraction_bits=4, width=8, degree=4, reductions=2, spot=1, strike=1
    )
    assert p["exp_budget"]["overflow_safe"]
    assert p["sum_integer_bounds"][1] > 127
    assert not p["overflow_safe"]
    p = reduced_plan([0], [[0]], fraction_bits=12, width=24, spot=1, strike=100)
    assert p["overflow_safe"]
    assert p["payoff_upper_integer"] == 0 and p["selector_bits"] == 1


def test_selector_strictly_exceeds_power_of_two_bound():
    p = reduced_plan(
        ["0.9375"], [[0]], fraction_bits=4, width=16, degree=1, reductions=0, spot=1, strike=1
    )
    assert p["payoff_upper_integer"] == 16
    assert p["selector_bits"] == 5


@pytest.mark.parametrize("case_index", [0, 1])
def test_existing_arithmetic_budget_accepts_metadata(case_index):
    from fractions import Fraction
    from research.journal_sprint.asian_basket import setup
    from research.journal_sprint.decimal_enclosure import Interval
    from research.journal_sprint.run_matched_arithmetic import arithmetic_budget
    from research.journal_sprint.run_minimal_pivot_week2 import CASES, contract_of

    contract = contract_of(CASES[case_index])
    model = setup(contract)
    discount = (-Interval(str(contract.rate)) * Interval(str(contract.maturity))).exp()
    p = reduced_plan(
        model["means"],
        model["factor"],
        fraction_bits=24,
        width=48,
        degree=12,
        reductions=2,
        discount=discount,
    )
    assert p["overflow_safe"]
    b = arithmetic_budget(contract, model, p, 0, "0")
    assert b["components"]["arithmetic"] == p["arithmetic_price_error_upper"]
    assert Fraction(b["decoder_bridge_upper"]) <= Fraction(b["components"]["decoding"])
    assert b["physical_execution_error"] is None


@pytest.mark.parametrize(
    "changes",
    [
        dict(radius=-1),
        dict(input_error=-1),
        dict(radius="NaN"),
        dict(input_error="Infinity"),
        dict(degree=True),
        dict(fraction_bits=0),
        dict(width=8, fraction_bits=8),
        dict(reductions=-1),
        dict(reductions=True),
        dict(reductions=1.5),
        dict(spot=1.5),
        dict(spot=0),
    ],
)
def test_invalid_certificate_arguments(changes):
    kwargs = dict(radius=1, input_error=0, degree=4, fraction_bits=8, width=24, reductions=1)
    kwargs.update(changes)
    with pytest.raises(ValueError):
        reduced_exp_budget(**kwargs)


@pytest.mark.parametrize(
    "kwargs",
    [
        dict(normal_bits=True),
        dict(strike=0),
        dict(discount=0),
        dict(cutoff=-1),
        dict(reductions=True),
    ],
)
def test_invalid_plan_arguments(kwargs):
    with pytest.raises(ValueError):
        reduced_plan([0], [[0]], **kwargs)


def test_directed_results_do_not_depend_on_ambient_decimal_precision():
    with localcontext() as ctx:
        ctx.prec = 6
        low = reduced_plan([4.6], [[0.2]], fraction_bits=24, width=48, reductions=3)
    with localcontext() as ctx:
        ctx.prec = 120
        high = reduced_plan([4.6], [[0.2]], fraction_bits=24, width=48, reductions=3)
    assert low == high
