"""Fixed 48/24 signed control design, integer reference and outward certificate.

This module emits no gates. Its overflow proof covers the stated straight-line
map, including products before coefficient addition. Circuit/resource admission
remains separate. All archived floats mean their exact binary values.
"""

from decimal import ROUND_CEILING, ROUND_FLOOR
from fractions import Fraction as F  # noqa: N817
from itertools import product
import json
import math

from research.journal_sprint.control_offset_enclosure import (
    control_enclosure,
    moment_enclosure,
)
from research.journal_sprint.decimal_enclosure import Interval as I, pi_interval  # noqa: N817
from .budget import reduced_plan

FRACTION_BITS = 24
WIDTH = 48
Q = 1 << FRACTION_BITS


def menu():
    """Fixed nine configurations per case; no outcome-dependent selection."""
    return [
        dict(fraction_bits=24, width=48, degree=n, reductions=s)
        for n, s in product((8, 12, 16), (1, 2, 3))
    ]


def _fraction(value):
    if isinstance(value, bool):
        raise ValueError("boolean is not an archived number")
    if isinstance(value, F):
        return value
    result = I(value)
    return F(result.lo)


def _interval(value):
    value = F(value)
    return I(value.numerator) / value.denominator


def _floor(value):
    return value.numerator // value.denominator


def _integer_bound(value, rounding):
    return int(value.to_integral_value(rounding=rounding))


def _canonical_json(value):
    """Normalize tuple/list archives while preserving JSON scalar types.

    In particular true != 1 and false != 0, unlike Python container equality.
    Reject NaN/Infinity and non-JSON objects rather than coercing them.
    """
    try:
        return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    except (TypeError, ValueError) as error:
        raise ValueError("certificate must contain finite JSON values") from error


def _binding(means, factor, q, strike, radius, low):
    return dict(
        means=[str(_fraction(v)) for v in means],
        factor=[[str(_fraction(v)) for v in row] for row in factor],
        q=q,
        cutoff=4,
        strike=str(_fraction(strike)),
        radius=str(_fraction(radius)),
        low=[str(_fraction(v)) for v in low],
    )


def low_polynomial(low_coefficients):
    """Exact monomial g=(x+p4)/2 and analytic residual bound on [-1,1]."""
    if len(low_coefficients) != 5:
        raise ValueError("five archived Chebyshev coefficients required")
    c = list(map(_fraction, low_coefficients))
    g = ((c[0] - c[2] + c[4]) / 2, (1 + c[1] - 3 * c[3]) / 2, c[2] - 4 * c[4], 2 * c[3], 4 * c[4])
    pi = pi_interval()
    exact = (2 / pi, I(0), 4 / (3 * pi), I(0), -4 / (15 * pi))
    bridge = sum(((_interval(a) - b).absolute() for a, b in zip(c, exact)), I(0))
    rho = 1 / (5 * pi) + bridge / 2
    return dict(
        monomial_rationals=[str(v) for v in g],
        residual_normalized_upper=str(rho.hi),
        coefficient_bridge_upper=str(bridge.hi),
        residual_at_zero=str(-g[0]),
        residual_at_one=str(1 - sum(g)),
    )


def control_offset_certificate(
    means, factor, *, q, strike, radius, low_coefficients, offset, discount
):
    """Re-certify an archived reflection offset against matching finite moments.

    discount is the archived binary64 discount used for that offset. This can
    be computed once per case and reused for all nine exponential designs.
    """
    values = [
        *means,
        *(v for row in factor for v in row),
        strike,
        radius,
        discount,
        *low_coefficients,
    ]
    if any(_fraction(v) != F(float(v)) for v in values):
        raise ValueError("offset enclosure requires exact archived binary64 inputs")
    moments = moment_enclosure(means, factor, q, 4)
    enclosure = control_enclosure(moments["moments"], strike, radius, discount, low_coefficients)[
        "value"
    ]
    chosen = float(offset)
    error = (I(chosen) - enclosure).absolute()
    return dict(
        schema="residual_offset_v1",
        binding=_binding(means, factor, q, strike, radius, low_coefficients),
        discount=str(_fraction(discount)),
        offset=chosen,
        expectation=enclosure.record(),
        error_upper=str(error.hi),
        work=moments["work"],
        scope="ideal_finite_midpoint_model",
    )


def evaluate_control_integer(sum_integer, certificate):
    """Unbounded reference; circuit must preserve this exact operation order.

    All variables have scale Q, except integer products before // Q. No wrap.
    The input is the parent sum of spot integers, NOT an averaged basket.
    """
    if type(sum_integer) is not int:
        raise ValueError("integer basket sum required")
    t = sum_integer - certificate["strike_sum"]
    x = t * certificate["reciprocal_integer"] // Q
    coefficients = certificate["control_coefficients"]
    y = coefficients[-1]
    for c in reversed(coefficients[:-1]):
        y = x * y // Q + c
    control = y * certificate["control_scale_integer"] // Q
    payoff = max(t, 0)
    residual = payoff - control
    return dict(
        poststrike_integer=t,
        normalized_integer=x,
        polynomial_integer=y,
        control_integer=control,
        payoff_integer=payoff,
        residual_integer=residual,
        threshold_integer=residual + certificate["shift_integer"],
    )


def decode_probability(amplitude, certificate):
    """The two binary64 operations covered by decoding_error_upper.

    The supplied amplitude is a binary64 number in [0,1]; any AE statistical
    error or prior conversion to binary64 is accounted for by the caller.
    """
    if type(amplitude) is not float or not 0 <= amplitude <= 1:
        raise ValueError("binary64 amplitude in [0,1] required")
    return certificate["decoder_intercept"] + certificate["decoder_scale"] * amplitude


def residual_plan(parent, means, factor, *, radius, low_coefficients, offset_certificate):
    """Certify a full 48/24 reduced parent plus the fixed signed control map.

    The supplied offset certificate is trusted evidence from
    control_offset_certificate; its complete financial binding is checked.
    No representation/loading/AE error is silently assumed zero here.

    With E bounding parent per-price error, k/Q the reciprocal, and v the
    normalization input, |v-x| <= E/B+d(B+E)|k/Q-1/(dB)|+1/Q.
    Horner uses that expanded domain. The control error is bounded by
    dB*(Lip(g)*dx+Horner_error)+|scale_hat-dB|*|g_hat|+1/Q.
    Positive part contributes dE; subtraction/shift are exact if word ranges
    pass. Residual normalization uses the Chebyshev tail, not sampled maxima.
    """
    if parent["fraction_bits"] != 24 or parent["width"] != 48:
        raise ValueError("residual route requires parent and control both 48/24")
    d = len(means)
    strike = F(parent["strike_sum"], d * Q)
    if strike.denominator != 1:
        raise ValueError("integer strike required")
    discount = I(parent["discount_lower"], parent["discount_upper"])
    rebuilt = reduced_plan(
        means,
        factor,
        cutoff=4,
        normal_bits=parent["normal_bits"],
        fraction_bits=24,
        width=48,
        degree=parent["degree"],
        reductions=parent["reductions"],
        spot=parent["spot"],
        strike=int(strike),
        discount=discount,
    )
    archived_fields = {k: parent.get(k) for k in rebuilt}
    if _canonical_json(archived_fields) != _canonical_json(rebuilt):
        raise ValueError("parent certificate does not match supplied model")
    binding = _binding(means, factor, parent["normal_bits"], strike, radius, low_coefficients)
    if _canonical_json(offset_certificate.get("binding")) != _canonical_json(binding):
        raise ValueError("offset model/q/strike/radius/coefficients mismatch")
    B = _fraction(radius)
    if B <= 0:
        raise ValueError("positive radius required")
    b, scale = _interval(B), _interval(d * B)
    basket_lower, basket_upper = I(0), I(0)
    for mu, row in zip(means, factor):
        spread = 4 * sum((I(v).absolute() for v in row), I(0))
        basket_lower += (I(mu) - spread).exp() / d
        basket_upper += (I(mu) + spread).exp() / d
    support = I(basket_lower.lo, basket_upper.hi)
    if (support - int(strike)).absolute().hi > b.lo:
        raise ValueError("radius does not enclose the entire cutoff cube")
    polynomial = low_polynomial(low_coefficients)
    g = tuple(F(v) for v in polynomial["monomial_rationals"])
    cs = tuple(_floor(Q * v) for v in g)
    reciprocal = _floor(F(Q) / (d * B))
    scale_integer = _floor(Q * d * B)
    unit = I(1) / Q
    ea = I(parent["exp_budget"]["total_error_upper"])
    reciprocal_error = (_interval(F(reciprocal, Q)) - 1 / scale).absolute()
    # |T/Q| <= d(B+ea), and |Ahat-A| <= ea.
    dx = ea / b + d * (b + ea) * reciprocal_error + unit
    r = 1 + dx
    horner_error = (_interval(g[-1]) - I(cs[-1]) / Q).absolute()
    for k in reversed(range(4)):
        horner_error = r * horner_error + unit + (_interval(g[k]) - I(cs[k]) / Q).absolute()
    derivative = sum((k * _interval(abs(g[k])) * r ** (k - 1) for k in range(1, 5)), I(0))
    g_magnitude = sum((_interval(abs(v)) * r**k for k, v in enumerate(g)), I(0))
    scale_error = (scale - I(scale_integer) / Q).absolute()
    # Scale rounding multiplies the implemented polynomial, not just g(x).
    control_error = scale * (derivative * dx + horner_error)
    control_error += scale_error * (g_magnitude + horner_error) + unit
    residual_error = d * ea + control_error  # positive part is 1-Lipschitz

    records, failures = [], []
    if not parent["overflow_safe"]:
        failures.append("parent_overflow_certificate_failed")

    def check(label, bounds, width=WIDTH):
        lo, hi = bounds
        if not -(1 << (width - 1)) <= lo <= hi < 1 << (width - 1):
            failures.append(label)
        records.append(dict(operation=label, integer_bounds=[lo, hi], width=width))
        return lo, hi

    def mul(label, a, b):
        values = [x * y for x in a for y in b]
        raw = check(label + "_product", (min(values), max(values)), 2 * WIDTH)
        return check(label, (raw[0] // Q, raw[1] // Q))

    check("sum", tuple(parent["sum_integer_bounds"]))
    check("strike", (parent["strike_sum"], parent["strike_sum"]))
    t = check("poststrike", tuple(parent["poststrike_integer_bounds"]))
    # Intersect with independent true-support plus parent-error enclosure.
    real_t = d * (support - int(strike) + I(ea.hi.copy_negate(), ea.hi)) * Q
    t = (
        max(t[0], _integer_bound(real_t.lo, ROUND_CEILING)),
        min(t[1], _integer_bound(real_t.hi, ROUND_FLOOR)),
    )
    check("poststrike_tight", t)
    check("reciprocal_constant", (reciprocal, reciprocal))
    check("scale_constant", (scale_integer, scale_integer))
    for k, c in enumerate(cs):
        check("coefficient_" + str(k), (c, c))
    x = mul("normalize", t, (reciprocal, reciprocal))
    y = (cs[-1], cs[-1])
    for k in reversed(range(4)):
        y = mul("horner_" + str(k), x, y)
        y = check("add_" + str(k), (y[0] + cs[k], y[1] + cs[k]))
    c_range = mul("control_scale", y, (scale_integer, scale_integer))
    p_range = check("positive_part", (max(0, t[0]), max(0, t[1])))
    direct = (p_range[0] - c_range[1], p_range[1] - c_range[0])
    bound = (scale * I(polynomial["residual_normalized_upper"]) + residual_error) * Q
    bound_integer = _integer_bound(bound.hi, ROUND_FLOOR)
    residual_range = check(
        "residual_subtract", (max(direct[0], -bound_integer), min(direct[1], bound_integer))
    )
    # Strictly greater even when the upper bound is an exact power of two.
    shift = 1 << bound_integer.bit_length()
    selector_bits = shift.bit_length()
    check("shift_constant", (shift, shift))
    threshold = check("shift_add", (residual_range[0] + shift, residual_range[1] + shift))
    if not 0 <= threshold[0] <= threshold[1] < 1 << selector_bits or selector_bits >= WIDTH:
        failures.append("selector_range")

    # O_arch approximates D_arch E[C]. Bridge to the parent's exact D.
    offset = float(offset_certificate["offset"])
    offset_error = I(offset_certificate["error_upper"])
    if offset_error.lo < 0:
        raise ValueError("nonnegative offset error required")
    control_abs = b * sum((_interval(abs(v)) for v in g), I(0))
    offset_bridge = (
        discount - _interval(F(offset_certificate["discount"]))
    ).absolute() * control_abs
    slope = discount * (1 << selector_bits) / (d * Q)
    intercept = I(offset) - discount * shift / (d * Q)
    slope_float = float(slope.hi)
    intercept_float = float(intercept.lo)
    if not math.isfinite(slope_float) or not math.isfinite(intercept_float):
        raise ValueError("nonfinite binary64 decoder")
    constant_error = (I(slope_float) - slope).absolute() + (
        I(intercept_float) - intercept
    ).absolute()
    # Specified decoder: intercept_float + slope_float * amplitude, two ops.
    decoding = (
        constant_error
        + I(8) * I(2.0**-52) * (I(slope_float).absolute() + I(intercept_float).absolute())
        + I(2.0**-1022)
    )
    arithmetic = discount * residual_error / d
    deterministic = arithmetic + offset_error + offset_bridge + decoding
    return dict(
        schema="signed_residual_plan_v1",
        fraction_bits=24,
        width=48,
        dimension=d,
        binding=binding,
        parent_plan=parent,
        strike_sum=parent["strike_sum"],
        reciprocal_integer=reciprocal,
        control_coefficients=cs,
        control_scale_integer=scale_integer,
        shift_integer=shift,
        selector_bits=selector_bits,
        polynomial=polynomial,
        integer_stages=records,
        residual_integer_bounds=residual_range,
        threshold_integer_bounds=threshold,
        normalization_error_upper=str(dx.hi),
        horner_error_upper=str(horner_error.hi),
        scale_error_upper=str(scale_error.hi),
        control_sum_error_upper=str(control_error.hi),
        residual_sum_error_upper=str(residual_error.hi),
        arithmetic_price_error_upper=str(arithmetic.hi),
        offset_certificate=offset_certificate,
        offset_bridge_upper=str(offset_bridge.hi),
        sensitivity_upper=str(slope.hi),
        decoder_scale=slope_float,
        decoder_intercept=intercept_float,
        decoding_error_upper=str(decoding.hi),
        deterministic_partial_upper=str(deterministic.hi),
        overflow_safe=not failures,
        overflow_failures=failures,
        application_admitted=False,
        circuit_admitted=False,
        missing=[
            "continuous representation allowance",
            "loader allowance",
            "AE schedule",
            "emitted control circuit and resources",
        ],
    )
