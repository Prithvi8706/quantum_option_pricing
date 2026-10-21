"""All-input exact support of the actual masked B4/B8 fixed-point payoff.

The proof bounds integer Estrin range reduction cell by cell, establishes
positivity and absence of overflow, and then uses the strict barrier condition.
It certifies the implemented digital output, not continuous-price error.
"""

from __future__ import annotations

# The exact proof statement is a readable receipt field.
# ruff: noqa: E501

import json
import math

from research.advantage_frontier_20260923 import barrier_oracle_depth as builder
from research.controlled_source_completion.optimize import optimize
from research.limitation_program_20261001.baseline import fingerprints


def ceildiv(a, b):
    return -(-a // b)


def product_bounds(left, right, fraction, square=False):
    a, b = left
    c, d = right
    values = (a * c, a * d, b * c, b * d)
    low, high = min(values), max(values)
    if square:
        if left != right:
            raise ValueError("square refinement requires the same exact operand")
        low = 0 if a <= 0 <= b else min(a * a, b * b)
        high = max(a * a, b * b)
    return low >> fraction, high >> fraction


def estrin_intervals(coefficients, remainder, fraction, width):
    """The identical integer expression with correlated power squaring."""
    limit = 1 << (width - 1)
    level = [(c, c) for c in coefficients]
    power = remainder
    stages = []

    def check(pair):
        if not -limit <= pair[0] <= pair[1] < limit:
            raise ArithmeticError("A native arithmetic output may overflow")
        return pair

    check(power)
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level) - 1, 2):
            term = check(product_bounds(level[i + 1], power, fraction))
            result = check((level[i][0] + term[0], level[i][1] + term[1]))
            nxt.append(result)
        if len(level) % 2:
            nxt.append(level[-1])
        level = nxt
        stages.append(dict(level=list(level), power=power))
        if len(level) > 1:
            power = check(product_bounds(power, power, fraction, square=True))
    return level[0], stages


def stock_support(width, fraction, lower_log, upper_log, inverse_ln2, ln2, coefficients):
    """Every clipped native integer input belongs to one exact reduction cell."""
    limit, Q = 1 << (width - 1), 1 << fraction
    if not (width > fraction >= 2 and lower_log <= upper_log and inverse_ln2 > 0 and ln2 > 0):
        raise ValueError("Valid native range-reduction parameters required")
    if not all(type(c) is int and 0 <= c < limit for c in coefficients):
        raise ValueError("Positive native Taylor coefficient words required")
    cmul_lo, cmul_hi = lower_log * inverse_ln2 // Q, upper_log * inverse_ln2 // Q
    if not -limit <= cmul_lo <= cmul_hi < limit:
        raise ArithmeticError("Inverse-ln2 multiplication may overflow")
    first, last = cmul_lo // Q, cmul_hi // Q
    if not -width < first <= last < width:
        raise ArithmeticError("Shift counts outside the native normal range")
    rows = []
    for k in range(first, last + 1):
        lo = max(lower_log, ceildiv(k * Q * Q, inverse_ln2))
        hi = min(upper_log, ceildiv((k + 1) * Q * Q, inverse_ln2) - 1)
        if lo > hi:
            continue
        if not -limit <= k * Q < limit or not -limit <= k * ln2 < limit:
            raise ArithmeticError("Native exponent scaling may overflow")
        remainder = lo - k * ln2, hi - k * ln2
        poly, stages = estrin_intervals(coefficients, remainder, fraction, width)
        if poly[0] < 0:
            raise ArithmeticError("The stock polynomial is not proved nonnegative")
        shifted = (poly[0] << k, poly[1] << k) if k >= 0 else (poly[0] >> -k, poly[1] >> -k)
        if not 0 <= shifted[0] <= shifted[1] < limit:
            raise ArithmeticError("Stock shift may overflow or become negative")
        rows.append(
            dict(
                k=k,
                clipped_log_interval=[lo, hi],
                remainder_interval=list(remainder),
                polynomial_interval=list(poly),
                stock_interval=list(shifted),
                stages=stages,
            )
        )
    if (
        not rows
        or rows[0]["clipped_log_interval"][0] != lower_log
        or rows[-1]["clipped_log_interval"][1] != upper_log
    ):
        raise AssertionError("Range-reduction cells do not cover the declared input")
    if any(
        a["clipped_log_interval"][1] + 1 != b["clipped_log_interval"][0]
        for a, b in zip(rows, rows[1:])
    ):
        raise AssertionError("Range-reduction partition has a gap or overlap")
    return dict(
        lower=min(r["stock_interval"][0] for r in rows),
        upper=max(r["stock_interval"][1] for r in rows),
        cells=rows,
        all_clipped_integer_inputs=True,
        positive_and_no_native_overflow=True,
    )


def certify(target, assets, dates):
    """Bind the proof to complete builder equality and actual output words."""
    stocks = []
    original_exp = builder.exp_estrin

    def capture(graph, value):
        out = original_exp(graph, value)
        stocks.append((value, out))
        return out

    builder.exp_estrin = capture
    try:
        original = json.loads(json.dumps(builder.build(assets, dates, q=32).as_dict()))
    finally:
        builder.exp_estrin = original_exp
    if optimize(original) != target:
        raise ValueError("The support theorem does not bind the actual financial target")
    if (target["width"], target["fraction_bits"]) != (72, 40):
        raise ValueError("This financial contract requires native72/f40")
    before, after = fingerprints(original), fingerprints(target)
    reverse = {token: value for value, token in after.items()}
    if len(reverse) != len(after) or len(stocks) != assets * dates:
        raise ValueError("Ambiguous financial expression binding")
    w, f = target["width"], target["fraction_bits"]
    Q, limit = 1 << f, 1 << (w - 1)
    lower, upper = round(math.log(2**-16) * Q), round(math.log(4096) * Q)
    cinv, cln = round(Q / math.log(2)), round(math.log(2) * Q)
    coeffs = [round(Q / math.factorial(j)) for j in range(13)]
    support = stock_support(w, f, lower, upper, cinv, cln, coeffs)
    if assets * dates * support["upper"] >= limit:
        raise ArithmeticError("Tree sums are not proved free from native overflow")
    basket_c = round(Q / assets)
    if basket_c * assets != Q:
        raise ValueError("This exact barrier proof requires binary basket weights")
    H, K, discount = (
        round(builder.H * Q),
        round(builder.K * Q),
        round(math.exp(-builder.RATE * builder.T) * Q),
    )
    avg_c = round(Q / (assets * dates))
    if not 0 < discount <= Q or not 0 <= K < H:
        raise ValueError("Positive discounted call contract required")
    # floor(S_j/assets)<H gives S_j<=assets*H-1 exactly.
    surviving_sum = dates * (assets * H - 1)
    average_upper = surviving_sum * avg_c // Q
    undiscounted = max(0, average_upper - K)
    payoff_upper = undiscounted * discount // Q
    if not 0 <= payoff_upper < limit:
        raise ArithmeticError("Masked payoff cannot be represented safely")
    producers = {v: n for n in target["nodes"] for v in n["out"]}
    output = producers[target["outputs"]["Y"]]
    if output["op"] != "select":
        raise ValueError("Actual output is not the preserved alive/payoff selector")
    alive, payoff, zero = (producers[v] for v in output["args"])
    if (alive["op"], payoff["op"], zero["op"]) != ("lt", "cmul", "const"):
        raise ValueError("Actual output marking structure differs from the theorem")
    if payoff["params"]["c"] != discount or zero["params"]["value"] != 0:
        raise ValueError("Actual discount/zero branch differs from the theorem")
    span_bits = max(1, payoff_upper.bit_length())
    return dict(
        assets=assets,
        dates=dates,
        width=w,
        fraction_bits=f,
        target_output=target["outputs"],
        complete_builder_equality=True,
        stock_ids=[reverse[before[y]] for _, y in stocks],
        clipped_log_ids=[reverse[before[x]] for x, _ in stocks],
        literal_inverse_ln2=cinv,
        literal_ln2=cln,
        literal_exp_coefficients=coeffs,
        clipped_log_integer_bounds=[lower, upper],
        stock_support=support,
        all_stock_tree_sums_no_overflow=True,
        stock_total_upper=assets * dates * support["upper"],
        strict_barrier_raw=H,
        strike_raw=K,
        basket_coefficient=basket_c,
        average_coefficient=avg_c,
        discount_coefficient=discount,
        surviving_stock_sum_upper=surviving_sum,
        surviving_average_upper=average_upper,
        payoff_raw_bounds=[0, payoff_upper],
        dollar_bounds_rational=[[0, 1], [payoff_upper, Q]],
        selector_random_bits=span_bits,
        selector_span_raw=1 << span_bits,
        selector_span_dollars_rational=[1 << span_bits, Q],
        conditional_proof="alive=1 iff every signed positive date basket<H; no-overflow gives exact basket=floor(date stock sum/assets), hence each sum<=assets*H-1. The modular tree is then the ordinary integer sum. Original rounded total-average and discount coefficients bound the masked payoff. alive=0 returns exactly zero.",
        all_original_uniform_word_patterns=True,
        sampled_price_maximum_used=False,
        continuous_dollar_error_certified=False,
        physical_runtime_certified=False,
    )
