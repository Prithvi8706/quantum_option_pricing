"""Emitted component ledger for the raw-plan fixed-point payoff flag.

No loader or aggregation circuit is fabricated here. The caller must add its
aggregation compute AND inverse, and any extra aggregation ancillas. Registers
are retained without scratch reuse; this is deliberately not space optimal.
Basis checks establish integer semantics at selected inputs, not a continuous
price certificate or an exhaustive proof of the supplied overflow certificate.
"""

from decimal import ROUND_CEILING

from .decimal_enclosure import Interval
from .fixed_exp_budget import evaluate_integer
from .reversible_fixed_point import (
    Program, affine, basis, constant, horner, less_than, positive_part, subtract,
)


def compiler_counts(counts):
    """Conservative exact logical U/CX decomposition, not hardware synthesis.

    X -> one U; CCX -> six CX and nine U. Controlled counts use conservative
    bounds of two CX and six U per U, and six CX and nine U per CX, plus
    one U allowance for a controlled global phase.
    """
    values = [counts[k] for k in ("x", "cx", "ccx")]
    if any(type(v) is not int or v < 0 for v in values):
        raise ValueError("nonnegative integer gate counts required")
    x, cx, ccx = values
    u, cx = x + 9*ccx, cx + 6*ccx
    return dict(u=u, cx=cx, controlled_u=6*u+9*cx+1,
                controlled_cx=2*u+6*cx)


def _sum_counts(resources, multiplier=1):
    return {k: multiplier*sum(r[k] for r in resources)
            for k in ("x", "cx", "ccx")}


def _check(actual, expected, label):
    if actual != expected:
        raise ArithmeticError(label + ": integer semantics or clean workspace failed")


def arithmetic_components(plan, checks=None):
    """Return JSON-safe emitted counts and deterministic packed-input checks.

    ``plan`` is a certified ``raw_plan`` dictionary. ``checks`` is a nonempty
    bounded iterable of packed Gaussian-input integers; default: zero and max.
    Each row is checked separately; the payoff and clean threshold comparator
    are then checked against unbounded Python integers. Aggregation correctness
    must be verified separately by its provider. No statevector is allocated.
    """
    if plan.get("overflow_safe") is not True:
        raise ArithmeticError("overflow_safe certificate required before construction")
    n, s, w, f = (plan[k] for k in
                  ("normal_qubits", "selector_bits", "width", "fraction_bits"))
    if any(type(v) is not int for v in (n, s, w, f)) or not (
            n > 0 and 0 < s < w and 0 <= f < w):
        raise ValueError("invalid register widths")
    rows = plan["affine_rows"]
    coefficients = plan["exp_budget"]["coefficients"]
    strike = plan["strike_sum"]
    if not rows or type(strike) is not int or not 0 <= strike < 1 << (w-1):
        raise ValueError("nonempty rows and representable strike required")
    # raw_plan's separate sum/strike tests do not suffice if polynomial prices
    # can be negative. Bound both signs using its directed Horner magnitude.
    if "intermediate_magnitude_upper" not in plan["exp_budget"]:
        raise ArithmeticError("directed intermediate magnitude bound required")
    magnitude = Interval(plan["exp_budget"]["intermediate_magnitude_upper"])
    if magnitude.lo < 0 or not magnitude.hi.is_finite():
        raise ArithmeticError("finite nonnegative magnitude bound required")
    price_bound = int((magnitude*(1 << f)).hi.to_integral_value(rounding=ROUND_CEILING))
    sum_bound = len(rows)*price_bound
    lower, upper = -sum_bound-strike, sum_bound-strike
    if sum_bound >= 1 << (w-1) or lower < -(1 << (w-1)) or upper >= 1 << (w-1):
        raise ArithmeticError("universal poststrike signed range failed")
    packed_inputs = list((0, (1 << n)-1) if checks is None else checks)
    if not packed_inputs or len(packed_inputs) > 256 or any(
            type(v) is not int or not 0 <= v < 1 << n for v in packed_inputs):
        raise ValueError("checks must contain 1..256 valid packed inputs")
    packed_inputs = list(dict.fromkeys(packed_inputs))
    totals = [0]*len(packed_inputs)
    conversion, row_checks = [], []
    for row_index, (intercept, bit_coefficients) in enumerate(rows):
        if len(bit_coefficients) != n:
            raise ValueError("affine row does not match input width")
        p = Program(compact=True)
        inputs, log, spot = p.register(n), p.register(w), p.register(w)
        affine(p, inputs, log, intercept, bit_coefficients)
        horner(p, log, spot, coefficients, f)
        conversion.append(p.resources())
        for j, packed in enumerate(packed_inputs):
            log_value = intercept + sum(((packed >> i) & 1)*c
                                        for i, c in enumerate(bit_coefficients))
            price = evaluate_integer(log_value, coefficients, f)
            if not (-(1 << (w-1)) <= log_value < 1 << (w-1)
                    and 0 <= price < 1 << (w-1)):
                raise ArithmeticError("checked log/price violates signed range")
            expected = basis(inputs, packed) | basis(log, log_value) | basis(spot, price)
            _check(p.run(basis(inputs, packed)), expected, "conversion")
            totals[j] += price
            row_checks.append(dict(row=row_index, packed_input=packed,
                                   log_integer=log_value, price_integer=price,
                                   clean_workspace=True))
        # Only one row program is retained at a time, including Horner scratch.
        del p

    p = Program(compact=True)
    total, strike_word, payoff = p.register(w), p.register(w), p.register(w)
    helper = p.register(1)[0]
    constant(p, strike_word, strike)
    subtract(p, strike_word, total, helper)
    positive_part(p, total, payoff)
    post = p.resources()

    comparator = Program(compact=True)
    selector, payoff_low = comparator.register(s), comparator.register(s)
    flag = comparator.register(1)
    difference, extended = comparator.register(s+1), comparator.register(s+1)
    carry = comparator.register(1)[0]
    less_than(comparator, selector, payoff_low, flag[0], difference, extended, carry)
    comparison = comparator.resources()
    semantic_checks = []
    for packed, value in zip(packed_inputs, totals):
        delta = value-strike
        positive = max(delta, 0)
        if not (0 <= value < 1 << (w-1) and -(1 << (w-1)) <= delta < 1 << (w-1)
                and positive < 1 << s):
            raise ArithmeticError("checked sum/payoff violates certified range")
        expected = basis(total, delta) | basis(strike_word, strike) | basis(payoff, positive)
        _check(p.run(basis(total, value)), expected, "postaggregation payoff")
        selectors = sorted({0, (1 << s)-1, max(0, positive-1), positive})
        for u in selectors:
            for initial_flag in (0, 1):
                initial = (basis(selector, u) | basis(payoff_low, positive)
                           | basis(flag, initial_flag))
                _check(comparator.run(initial), initial ^ basis(flag, int(u < positive)),
                       "threshold comparator")
        semantic_checks.append(dict(packed_input=packed, sum_integer=value,
                                    payoff_integer=positive, selectors=selectors,
                                    both_initial_flags_checked=True, clean_workspace=True))
    forward = _sum_counts(conversion)
    full = {k: 2*forward[k]+2*post[k]+comparison[k] for k in forward}
    # Shared: inputs, selector, flag; row logs/spots/scratch; total/strike/payoff
    # plus post carry; comparator scratch plus its own (unreused) carry.
    qubits = n+s+1+sum(r["qubits"]-n for r in conversion)+3*w+1+2*(s+1)+1
    return dict(schema="matched_arithmetic_components_v1",
                conversion_rows=conversion, conversion_forward=forward,
                postaggregation_payoff=post, comparator=comparison,
                total_excluding_aggregation=full, compiler_counts=compiler_counts(full),
                native_excluding_aggregation={k: compiler_counts(full)[k] for k in ("u", "cx")},
                A_num_qubits_excluding_loader_ancillas=qubits,
                a_qubits_excluding_aggregation_helper=qubits,
                poststrike_bounds=dict(price_absolute_integer_upper=price_bound,
                    sum_integer_lower=-sum_bound, sum_integer_upper=sum_bound,
                    difference_integer_lower=lower, difference_integer_upper=upper,
                    signed_word_lower=-(1 << (w-1)), signed_word_upper=(1 << (w-1))-1,
                    proof="Directed Horner intermediate magnitude times scale, "
                    "rounded upward; triangle inequality over all rows; subtract exact strike.",
                    universal_signed_range_safe=True),
                wire_layout=dict(shared_input=n, selector=s, flag=1,
                    conversion_private=sum(r["qubits"]-n for r in conversion),
                    total_strike_payoff=3*w, post_carry=1,
                    comparator_scratch=2*(s+1)+1),
                row_checks=row_checks, semantic_checks=semantic_checks,
                aggregation_included=False, loading_included=False,
                additional_aggregation_ancillas_included=False,
                aggregation_interface=dict(spot_registers=len(rows), width=w,
                                           total_initial_value=0,
                                           preserve_spots=True, clean_scratch_required=True),
                qualification="Counts include conversion and payoff inverses; "
                "comparator is already clean. Add aggregation and its inverse, "
                "loader/selector preparation, and any extra ancillas. Disjoint retained "
                "workspaces are not space optimal. No physical synthesis or AE included.")
