"""Independent exact/Decimal references for the specified signed control map."""

from copy import deepcopy
from decimal import Decimal as D, ROUND_FLOOR, localcontext  # noqa: N817
from fractions import Fraction as F  # noqa: N817
from itertools import product
import json
from pathlib import Path

import pytest

from research.journal_sprint.decimal_enclosure import Interval as I  # noqa: N817
from research.stronger_arithmetic.budget import reduced_plan, evaluate_reduced_integer
from research.stronger_arithmetic.residual import (
    Q,
    control_offset_certificate,
    decode_probability,
    evaluate_control_integer,
    low_polynomial,
    menu,
    residual_plan,
)

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "results/journal_sprint/normalization_approximation_v1/model.json"


@pytest.fixture(scope="module")
def low():
    return json.loads(ARCHIVE.read_text())["low_coefficients"]


@pytest.fixture(scope="module")
def evidence(low):
    means, factor = [4.6], [[0.1]]
    offset = control_offset_certificate(
        means, factor, q=2, strike=100, radius=100, low_coefficients=low, offset=0, discount=1
    )
    # Choose a decoder offset inside its proven enclosure without repeating
    # moment computation. The certificate schema records the chosen float.
    enclosure = offset["expectation"]
    chosen = float(enclosure["lower"])
    offset["offset"] = chosen
    offset["error_upper"] = str(
        (I(chosen) - I(enclosure["lower"], enclosure["upper"])).absolute().hi
    )
    return means, factor, offset


def make(evidence, low, degree=12, reductions=2):
    means, factor, offset = evidence
    parent = reduced_plan(
        means,
        factor,
        normal_bits=2,
        strike=100,
        degree=degree,
        reductions=reductions,
        fraction_bits=24,
        width=48,
    )
    return residual_plan(
        parent, means, factor, radius=100, low_coefficients=low, offset_certificate=offset
    )


def test_archived_exact_witness_and_analytic_bound(low):
    p = low_polynomial(low)
    assert F(p["residual_at_zero"]) == -F(4587328911378127, 72057594037927936)
    assert F(p["residual_at_one"]) > 0
    assert D(p["residual_normalized_upper"]) < D("0.063662")
    cs = [F(v) for v in p["monomial_rationals"]]
    c0 = (Q * cs[0]).numerator // (Q * cs[0]).denominator
    assert c0 == 1068070
    assert (-c0) % Q == 15709146
    for i in range(-256, 257):
        x = F(i, 256)
        r = max(x, 0) - sum(c * x**k for k, c in enumerate(cs))
        assert abs(r) <= F(p["residual_normalized_upper"])


@pytest.mark.parametrize("degree,reductions", product((8, 12, 16), (1, 2, 3)))
def test_full_financial_error_and_every_integer_stage(evidence, low, degree, reductions):
    c = make(evidence, low, degree, reductions)
    assert c["overflow_safe"], c["overflow_failures"]
    stages = {r["operation"]: r for r in c["integer_stages"]}

    def within(name, value):
        lo, hi = stages[name]["integer_bounds"]
        assert lo <= value <= hi, (name, value, lo, hi)

    with localcontext() as ctx:
        ctx.prec = 120
        means, factor, _ = evidence
        parent = c["parent_plan"]
        a, cs = parent["affine_rows"][0]
        g = [D(F(v).numerator) / D(F(v).denominator) for v in c["polynomial"]["monomial_rationals"]]
        for packed in range(4):
            log = a + sum(((packed >> k) & 1) * v for k, v in enumerate(cs))
            price = evaluate_reduced_integer(
                log, parent["exp_budget"]["coefficients"], 24, reductions, 100
            )
            actual = evaluate_control_integer(price, c)
            t = price - c["strike_sum"]
            within("poststrike_tight", t)
            raw = t * c["reciprocal_integer"]
            within("normalize_product", raw)
            x = raw // Q
            within("normalize", x)
            y = c["control_coefficients"][-1]
            for k in reversed(range(4)):
                raw = x * y
                within("horner_" + str(k) + "_product", raw)
                y = raw // Q
                within("horner_" + str(k), y)
                y += c["control_coefficients"][k]
                within("add_" + str(k), y)
            raw = y * c["control_scale_integer"]
            within("control_scale_product", raw)
            within("control_scale", raw // Q)
            within("residual_subtract", actual["residual_integer"])
            within("shift_add", actual["threshold_integer"])

            # Independent Decimal floor reference, including negative products.
            def floor(v):
                return v.to_integral_value(rounding=ROUND_FLOOR)

            xd = floor(D(t) * c["reciprocal_integer"] / Q)
            yd = D(c["control_coefficients"][-1])
            for v in reversed(c["control_coefficients"][:-1]):
                yd = floor(xd * yd / Q) + v
            cd = floor(yd * c["control_scale_integer"] / Q)
            assert actual["control_integer"] == int(cd)
            A = (D.from_float(means[0]) + D.from_float(factor[0][0]) * (-3 + 2 * packed)).exp()
            truth_x = (A - 100) / 100
            control = 100 * sum(v * truth_x**k for k, v in enumerate(g))
            residual = max(A - 100, 0) - control
            assert abs(D(actual["control_integer"]) / Q - control) <= D(
                c["control_sum_error_upper"]
            )
            assert abs(D(actual["residual_integer"]) / Q - residual) <= D(
                c["residual_sum_error_upper"]
            )
            assert 0 <= actual["threshold_integer"] < 1 << c["selector_bits"]


def test_strict_shift_and_decoder_rounding(evidence, low):
    c = make(evidence, low)
    h = c["shift_integer"]
    assert h & (h - 1) == 0 and (1 << c["selector_bits"]) == 2 * h
    lo, hi = c["residual_integer_bounds"]
    assert -h < lo <= hi < h
    with localcontext() as ctx:
        ctx.prec = 120
        for a in [0.0, 2.0**-52, 0.13, 0.5, 1.0]:
            actual = decode_probability(a, c)
            exact = (
                D.from_float(c["offset_certificate"]["offset"])
                - D(h) / Q
                + D(1 << c["selector_bits"]) / Q * D.from_float(a)
            )
            assert abs(D.from_float(actual) - exact) <= D(c["decoding_error_upper"])


def test_metadata_binding_and_fixed_route(evidence, low):
    means, factor, offset = evidence
    c = make(evidence, low)
    for key, value in [("q", 10), ("radius", "101"), ("low", ["0"] * 5)]:
        bad = deepcopy(offset)
        bad["binding"][key] = value
        with pytest.raises(ValueError, match="mismatch"):
            residual_plan(
                c["parent_plan"],
                means,
                factor,
                radius=100,
                low_coefficients=low,
                offset_certificate=bad,
            )
    bad = deepcopy(c["parent_plan"])
    bad["fraction_bits"] = 20
    with pytest.raises(ValueError, match="48/24"):
        residual_plan(
            bad, means, factor, radius=100, low_coefficients=low, offset_certificate=offset
        )
    bad = deepcopy(c["parent_plan"])
    bad["exp_budget"]["total_error_upper"] = "0"
    with pytest.raises(ValueError, match="parent certificate"):
        residual_plan(
            bad, means, factor, radius=100, low_coefficients=low, offset_certificate=offset
        )


def test_parent_archive_json_round_trip(evidence, low):
    means, factor, offset = evidence
    original = make(evidence, low)
    archived = json.loads(json.dumps(original["parent_plan"]))
    assert isinstance(archived["affine_rows"][0], list)
    assert isinstance(archived["exp_budget"]["coefficients"], list)
    actual = residual_plan(
        archived,
        means,
        factor,
        radius=100,
        low_coefficients=low,
        offset_certificate=json.loads(json.dumps(offset)),
    )
    assert json.loads(json.dumps(actual)) == json.loads(json.dumps(original))


@pytest.mark.parametrize(
    "path,value",
    [
        (("overflow_safe",), 1),
        (("application_admitted",), 0),
        (("exp_budget", "overflow_safe"), 1),
        (("exp_budget", "coefficients", -1), False),
        (("exp_budget", "product_width"), 96.0),
    ],
)
def test_parent_json_comparison_preserves_scalar_types(evidence, low, path, value):
    means, factor, offset = evidence
    archived = json.loads(json.dumps(make(evidence, low)["parent_plan"]))
    node = archived
    for key in path[:-1]:
        node = node[key]
    # These replacements compare equal in ordinary Python container equality.
    assert node[path[-1]] == value
    node[path[-1]] = value
    with pytest.raises(ValueError, match="parent certificate"):
        residual_plan(
            archived, means, factor, radius=100, low_coefficients=low, offset_certificate=offset
        )


def test_discount_bridge_is_not_omitted(evidence, low):
    means, factor, offset = evidence
    parent = reduced_plan(
        means,
        factor,
        normal_bits=2,
        fraction_bits=24,
        width=48,
        degree=12,
        reductions=2,
        discount="0.97",
    )
    c = residual_plan(
        parent, means, factor, radius=100, low_coefficients=low, offset_certificate=offset
    )
    assert D(c["offset_bridge_upper"]) > 0
    assert D(c["deterministic_partial_upper"]) > D(c["arithmetic_price_error_upper"])


def test_directed_certificate_independent_of_ambient_precision(evidence, low):
    with localcontext() as ctx:
        ctx.prec = 6
        a = make(evidence, low)
    with localcontext() as ctx:
        ctx.prec = 120
        b = make(evidence, low)
    assert a == b
    assert len(menu()) == 9
    assert not a["circuit_admitted"] and not a["application_admitted"]
    json.dumps(a)


def test_radius_and_overflow_failures(evidence, low):
    means, factor, offset = evidence
    parent = make(evidence, low)["parent_plan"]
    bad = deepcopy(offset)
    bad["binding"]["radius"] = "1"
    with pytest.raises(ValueError, match="cutoff cube"):
        residual_plan(parent, means, factor, radius=1, low_coefficients=low, offset_certificate=bad)
    # Huge low-polynomial coefficients must yield an explicit infeasible
    # certificate, even though normalization itself still fits.
    huge = [1e12, 0.0, 0.0, 0.0, 0.0]
    bad["binding"] = deepcopy(offset["binding"])
    bad["binding"]["low"] = [str(F(v)) for v in huge]
    c = residual_plan(
        parent, means, factor, radius=100, low_coefficients=huge, offset_certificate=bad
    )
    assert not c["overflow_safe"]
    assert "coefficient_0" in c["overflow_failures"]
    assert "selector_range" in c["overflow_failures"]


@pytest.mark.parametrize("case_id", ["D1", "D2"])
def test_archived_q10_offsets_and_entire_fixed_menu(low, case_id):
    import math
    from research.journal_sprint.asian_basket import Basket, setup
    from research.journal_sprint.arithmetic_plan import raw_plan
    from research.journal_sprint.claim_assessment import schedule

    archived = json.loads(
        (
            ROOT
            / "results/journal_sprint/minimal_pivot_week2_production_v1"
            / ("case_" + case_id + ".json")
        ).read_text()
    )
    reflection = next(row for row in archived if row["mode"] == "reflection")
    case = reflection["case"]
    contract = Basket(**{k: v for k, v in case.items() if k not in ("id", "split")})
    model = setup(contract)
    means, factor = model["means"].tolist(), model["factor"].tolist()
    discount = (-I(str(contract.rate)) * I(str(contract.maturity))).exp()
    matched = json.loads(
        (
            ROOT / "results/journal_sprint/matched_arithmetic_v1" / ("case_" + case_id + ".json")
        ).read_text()
    )
    # Reject a numerical environment which regenerates a different parent map.
    old = raw_plan(
        means,
        factor,
        fraction_bits=20,
        width=40,
        degree=24,
        strike=int(contract.strike),
        discount=discount,
    )
    assert json.loads(json.dumps(old["affine_rows"])) == matched["arithmetic_plan"]["affine_rows"]
    B = reflection["plan"]["radius"]
    offset = control_offset_certificate(
        means,
        factor,
        q=10,
        strike=int(contract.strike),
        radius=B,
        low_coefficients=low,
        offset=reflection["budget"]["offset"],
        discount=math.exp(-contract.rate * contract.maturity),
    )
    assert D(offset["error_upper"]) < D("1e-10")
    statuses = []
    for spec in menu():
        parent = reduced_plan(means, factor, strike=int(contract.strike), discount=discount, **spec)
        c = residual_plan(
            parent, means, factor, radius=B, low_coefficients=low, offset_certificate=offset
        )
        # These are checks, not an assertion that all declared designs must win.
        assert c["overflow_safe"], c["overflow_failures"]
        for packed in (0, (1 << parent["normal_qubits"]) - 1):
            total = 0
            for a, cs in parent["affine_rows"]:
                x = a + sum(((packed >> k) & 1) * v for k, v in enumerate(cs))
                total += evaluate_reduced_integer(
                    x, parent["exp_budget"]["coefficients"], 24, parent["reductions"], 100
                )
            actual = evaluate_control_integer(total, c)
            assert (
                c["threshold_integer_bounds"][0]
                <= actual["threshold_integer"]
                <= c["threshold_integer_bounds"][1]
            )
        representation = I(str(reflection["budget"]["components"]["representation"]))
        # Inherit the archived raw loader dollar allowance conservatively:
        # the new sensitivity is checked no larger than the original scale.
        raw = next(row["budget"] for row in matched["alternatives"] if row["mode"] == "ripple")
        assert I(c["sensitivity_upper"]).hi <= I(raw["sensitivity_upper"]).lo
        deterministic = (
            I(c["deterministic_partial_upper"])
            + representation
            + I(raw["components"]["preparation"])
        )
        ae = schedule(F(c["sensitivity_upper"]) / 2, F(deterministic.hi))
        statuses.append(ae["status"])
    assert len(statuses) == 9
    assert "ideal_plan" in statuses
