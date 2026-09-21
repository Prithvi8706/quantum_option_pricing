"""Bounded, emitted arithmetic-only ledger; no loader, selector H, or AE.

Both layouts retain row logs/spots. Only scratch proven clean by the kernel
construction is shared. Endpoint checks are diagnostics, not universal proofs:
the supplied plan certificate is required before any gates are acquired.
"""

from copy import deepcopy
from decimal import ROUND_CEILING
from functools import lru_cache

import numpy as np

from research.journal_sprint.decimal_enclosure import Interval
from research.journal_sprint.fixed_exp_budget import evaluate_integer
from research.journal_sprint.matched_aggregation import _modular_add
from research.journal_sprint.matched_arithmetic import compiler_counts
from research.journal_sprint.reversible_fixed_point import (
    CompactGates,
    Program,
    affine,
    basis,
    constant,
    horner,
    less_than,
    positive_part,
    subtract,
)
from .circuits import clean_exp

MAX_CONVERSION_GATES = 8_000_000
MAX_CONVERSION_QUBITS = 4096
MAX_COMPONENT_GATES = 100_000_000


class ResourceLimitError(ValueError):
    """A protocol cap was exceeded; no resource result is valid."""


ComponentLimitError = ResourceLimitError


class _CappedGates(CompactGates):
    def append(self, gate):
        if len(self) >= MAX_CONVERSION_GATES:
            raise ComponentLimitError("conversion exceeds 8,000,000 gates")
        super().append(gate)


class _BoundedProgram(Program):
    def __init__(self):
        super().__init__(compact=True)
        self.gates = _CappedGates()

    def register(self, width):
        if self.qubits + width > MAX_CONVERSION_QUBITS:
            raise ComponentLimitError("conversion exceeds 4096 wires")
        return super().register(width)


class _Ledger:
    """Dependency depth of actual remapped gates, without a full gate list."""

    def __init__(self, qubits):
        self.depths = [0] * qubits
        self.counts = dict(x=0, cx=0, ccx=0)

    def emit(self, gate):
        self.counts[("x", "cx", "ccx")[len(gate) - 1]] += 1
        level = 1 + max(self.depths[b] for b in gate)
        for b in gate:
            self.depths[b] = level

    def extend(self, p, mapping, inverse=False):
        # Traverse compact records directly: no millions of temporary tuples
        # or generator/max calls. This is the same per-wire gate recurrence.
        data, depths = p.gates.data, self.depths
        indices = range(len(data) - 4, -1, -4) if inverse else range(0, len(data), 4)
        x = cx = ccx = 0
        for i in indices:
            arity = data[i]
            a = mapping[data[i + 1]]
            if arity == 1:
                depths[a] += 1
                x += 1
            else:
                b = mapping[data[i + 2]]
                level = max(depths[a], depths[b])
                if arity == 3:
                    c = mapping[data[i + 3]]
                    level = max(level, depths[c]) + 1
                    depths[c] = level
                    ccx += 1
                else:
                    level += 1
                    cx += 1
                depths[a] = depths[b] = level
        self.counts["x"] += x
        self.counts["cx"] += cx
        self.counts["ccx"] += ccx

    def resources(self):
        return dict(self.counts, qubits=len(self.depths), logical_depth=max(self.depths, default=0))


def _check(actual, expected, label):
    if actual != expected:
        raise ArithmeticError(label + ": integer map or clean scratch failed")


def _run(p, state, inverse=False):
    data = p.gates.data
    indices = range(len(data) - 4, -1, -4) if inverse else range(0, len(data), 4)
    for i in indices:
        arity = data[i]
        if arity == 1:
            state ^= 1 << data[i + 1]
        elif arity == 2:
            if (state >> data[i + 1]) & 1:
                state ^= 1 << data[i + 2]
        elif (state >> data[i + 1]) & (state >> data[i + 2]) & 1:
            state ^= 1 << data[i + 3]
    return state


def _inverse_run(p, state):
    return _run(p, state, inverse=True)


def _certificate(plan, reduced):
    if plan.get("overflow_safe") is not True:
        raise ArithmeticError("overflow_safe plan certificate required")
    n, s, w, f = (plan[k] for k in ("normal_qubits", "selector_bits", "width", "fraction_bits"))
    if any(type(v) is not int for v in (n, s, w, f)) or not (n > 0 and 0 < s < w and 0 <= f < w):
        raise ValueError("invalid register widths")
    rows = tuple((a, tuple(cs)) for a, cs in plan["affine_rows"])
    strike = plan["strike_sum"]
    if not rows or type(strike) is not int or not 0 <= strike < 1 << (w - 1):
        raise ValueError("nonempty rows and representable strike required")
    for a, cs in rows:
        if type(a) is not int or len(cs) != n or any(type(c) is not int for c in cs):
            raise ValueError("invalid affine row")
        # Prefix sums of signed additions must also fit the certified word.
        lo, hi = a + sum(min(c, 0) for c in cs), a + sum(max(c, 0) for c in cs)
        if not -(1 << (w - 1)) <= lo <= hi < 1 << (w - 1):
            raise ArithmeticError("universal affine signed range failed")
    budget = plan["exp_budget"]
    coefficients = tuple(budget["coefficients"])
    if not coefficients or any(type(c) is not int for c in coefficients):
        raise ValueError("integer exponential coefficients required")
    while len(coefficients) > 1 and coefficients[-1] == 0:
        coefficients = coefficients[:-1]
    reductions, spot = 0, 1
    if reduced:
        reductions = budget.get("reductions", plan.get("reductions"))
        spot = budget.get("spot", plan.get("spot"))
        if (
            "reductions" in plan
            and plan["reductions"] != reductions
            or "spot" in plan
            and plan["spot"] != spot
        ):
            raise ValueError("plan and exponential kernel parameters disagree")
        if type(reductions) is not int or reductions < 0 or type(spot) is not int or spot < 1:
            raise ValueError("reduced plan requires integer reductions and spot")
        if budget.get("overflow_safe") is not True:
            raise ArithmeticError("reduced exponential overflow certificate required")
        lo, hi = budget["output_integer_bounds"]
        if any(type(v) is not int for v in (lo, hi)) or lo > hi:
            raise ArithmeticError("invalid output integer bounds")
    else:
        if "intermediate_magnitude_upper" not in budget:
            raise ArithmeticError("directed magnitude bound required")
        magnitude = Interval(budget["intermediate_magnitude_upper"])
        if magnitude.lo < 0 or not magnitude.hi.is_finite():
            raise ArithmeticError("finite nonnegative magnitude bound required")
        hi = int((magnitude * (1 << f)).hi.to_integral_value(rounding=ROUND_CEILING))
        lo = -hi
    lower, upper = len(rows) * lo, len(rows) * hi
    dlower, dupper = lower - strike, upper - strike
    limit = 1 << (w - 1)
    if not (
        -limit <= min(0, lower) <= max(0, upper) < limit and -limit <= dlower <= dupper < limit
    ):
        raise ArithmeticError("universal sum/poststrike signed range failed")
    # Plan may provide a tighter true-price-plus-certified-error bound.
    payoff_bound = max(0, dupper)
    if "payoff_upper_integer" in plan:
        bound = plan["payoff_upper_integer"]
        if type(bound) is not int:
            raise ArithmeticError("integer payoff certificate required")
        payoff_bound = min(payoff_bound, max(0, bound))
    if payoff_bound >= 1 << s:
        raise ArithmeticError("universal selector range failed")
    proof = dict(
        sum_integer_bounds=[lower, upper],
        poststrike_integer_bounds=[dlower, dupper],
        payoff_upper_integer=payoff_bound,
        universal_signed_range_safe=True,
        universal_selector_safe=True,
    )
    return (n, s, w, f, rows, coefficients, strike, reduced, reductions, spot), proof


@lru_cache(maxsize=1)
def _kernel(w, f, coefficients, reduced, reductions, spot, gate_cap, wire_cap):
    p = _BoundedProgram()
    x, out = p.register(w), p.register(w)
    if reduced:
        clean_exp(p, x, out, coefficients, f, reductions, spot)
    else:
        horner(p, x, out, coefficients, f)
    return p


def _conversion(n, w, row, kernel):
    p = _BoundedProgram()
    inputs, log, spot = p.register(n), p.register(w), p.register(w)
    affine(p, inputs, log, row[0], row[1])
    scratch = p.register(kernel.qubits - 2 * w)
    mapping = log + spot + scratch
    if len(p.gates) + len(kernel.gates) > MAX_CONVERSION_GATES:
        raise ComponentLimitError("conversion exceeds 8,000,000 gates")
    # Remap the emitted compact records in bulk, preserving every gate and its
    # order. Padding fields are immaterial. The caps were checked before this
    # bounded allocation; no count or depth is inferred from a size formula.
    records = np.frombuffer(kernel.gates.data, dtype=np.intc).reshape(-1, 4).copy()
    records[:, 1:] = np.asarray(mapping, dtype=np.intc)[records[:, 1:]]
    p.gates.data.frombytes(records.tobytes())
    return p, inputs, log, spot


@lru_cache(maxsize=8)
def _acquire(key, gate_cap, wire_cap, component_cap):
    n, s, w, f, rows, coefficients, strike, reduced, reductions, spot_scale = key
    kernel = _kernel(w, f, coefficients, reduced, reductions, spot_scale, gate_cap, wire_cap)
    if 2 * len(rows) * len(kernel.gates) > component_cap:
        raise ResourceLimitError("component exceeds 100,000,000 gate applications")
    # Affine scratch is w+1; exponential scratch follows it in each row.
    scratch_width = w + 1 + kernel.qubits - 2 * w
    shared_width = n + s + 1
    permanent = shared_width + 2 * w * len(rows)
    post_width = 3 * w + 1 + 2 * (s + 1)
    layouts = {}
    for reuse in (False, True):
        scratch_total = scratch_width * (1 if reuse else len(rows))
        post_start = permanent + scratch_total
        layouts[reuse] = (_Ledger(post_start + post_width), post_start)
    applications = 0

    def stream(p, maps, inverse=False):
        nonlocal applications
        applications += len(p.gates)
        if applications > component_cap:
            raise ComponentLimitError("component exceeds 100,000,000 gate applications")
        for reuse, (ledger, _) in layouts.items():
            ledger.extend(p, maps[reuse], inverse)

    def row_maps(i):
        result = {}
        for reuse in layouts:
            start = permanent + (0 if reuse else i * scratch_width)
            result[reuse] = (
                tuple(range(n))
                + tuple(range(shared_width + 2 * w * i, shared_width + 2 * w * (i + 1)))
                + tuple(range(start, start + scratch_width))
            )
        return result

    packed_inputs = (0, (1 << n) - 1)
    totals = [0, 0]
    prices = [[], []]
    row_checks = []
    conversion_counts = dict(x=0, cx=0, ccx=0)
    for i, row in enumerate(rows):
        p, inputs, log, spot = _conversion(n, w, row, kernel)
        for j, packed in enumerate(packed_inputs):
            value = row[0] + sum(((packed >> k) & 1) * c for k, c in enumerate(row[1]))
            price = evaluate_integer(value >> reductions, coefficients, f)
            for _ in range(reductions):
                price = price * price // (1 << f)
            price *= spot_scale
            if not -(1 << (w - 1)) <= price < 1 << (w - 1):
                raise ArithmeticError("checked price violates signed word")
            initial = basis(inputs, packed)
            expected = initial | basis(log, value) | basis(spot, price)
            _check(_run(p, initial), expected, "conversion")
            _check(_inverse_run(p, expected), initial, "conversion inverse")
            totals[j] += price
            prices[j].append(price)
            row_checks.append(
                dict(
                    row=i,
                    packed_input=packed,
                    log_integer=value,
                    price_integer=price,
                    clean_workspace=True,
                    inverse_checked=True,
                )
            )
        # Counts are already traversed by stream, so take differences.
        before = dict(layouts[False][0].counts)
        stream(p, row_maps(i))
        for k in conversion_counts:
            conversion_counts[k] += layouts[False][0].counts[k] - before[k]
        del p

    agg = Program(compact=True)
    operands = [agg.register(w) for _ in rows]
    total, helper = agg.register(w), agg.register(1)[0]
    for a, b in zip(operands[0], total):
        agg.gate(a, b)
    for operand in operands[1:]:
        _modular_add(agg, operand, total, helper)
    agg_maps = {}
    for reuse, (_, start) in layouts.items():
        agg_maps[reuse] = (
            tuple(
                b
                for i in range(len(rows))
                for b in range(shared_width + (2 * i + 1) * w, shared_width + (2 * i + 2) * w)
            )
            + tuple(range(start, start + w))
            + (start + 3 * w,)
        )
    stream(agg, agg_maps)

    post = Program(compact=True)
    pt, strike_word, payoff = post.register(w), post.register(w), post.register(w)
    carry = post.register(1)[0]
    constant(post, strike_word, strike)
    subtract(post, strike_word, pt, carry)
    positive_part(post, pt, payoff)
    post_maps = {r: tuple(range(start, start + post.qubits)) for r, (_, start) in layouts.items()}
    stream(post, post_maps)

    cmp = Program(compact=True)
    selector, low, flag = cmp.register(s), cmp.register(s), cmp.register(1)
    difference, extended, carry = cmp.register(s + 1), cmp.register(s + 1), cmp.register(1)[0]
    less_than(cmp, selector, low, flag[0], difference, extended, carry)
    cmp_maps = {
        r: (
            tuple(range(n, n + s))
            + tuple(range(start + 2 * w, start + 2 * w + s))
            + (n + s,)
            + tuple(range(start + 3 * w + 1, start + post_width))
            + (start + 3 * w,)
        )
        for r, (_, start) in layouts.items()
    }
    stream(cmp, cmp_maps)
    stream(post, post_maps, inverse=True)
    stream(agg, agg_maps, inverse=True)
    for i in reversed(range(len(rows))):
        p, _, _, _ = _conversion(n, w, rows[i], kernel)
        stream(p, row_maps(i), inverse=True)
        del p

    checks = []
    for j, (packed, value) in enumerate(zip(packed_inputs, totals)):
        positive = max(value - strike, 0)
        if not (
            -(1 << (w - 1)) <= value < 1 << (w - 1)
            and -(1 << (w - 1)) <= value - strike < 1 << (w - 1)
            and positive < 1 << s
        ):
            raise ArithmeticError("checked sum/payoff violates certificate")
        initial = sum(basis(word, price) for word, price in zip(operands, prices[j]))
        expected = initial | basis(total, value)
        _check(agg.run(initial), expected, "aggregation")
        _check(_inverse_run(agg, expected), initial, "aggregation inverse")
        initial = basis(pt, value)
        expected = basis(pt, value - strike) | basis(strike_word, strike) | basis(payoff, positive)
        _check(post.run(initial), expected, "poststrike")
        _check(_inverse_run(post, expected), initial, "poststrike inverse")
        selectors = sorted({0, (1 << s) - 1, max(0, positive - 1), positive})
        for u in selectors:
            for b in (0, 1):
                initial = basis(selector, u) | basis(low, positive) | basis(flag, b)
                _check(cmp.run(initial), initial ^ basis(flag, int(u < positive)), "comparator")
        checks.append(
            dict(
                packed_input=packed,
                sum_integer=value,
                payoff_integer=positive,
                selectors=selectors,
                both_initial_flags_checked=True,
                clean_workspace=True,
            )
        )
    result = {}
    for reuse, (ledger, _) in layouts.items():
        resources = ledger.resources()
        native = compiler_counts(ledger.counts)
        result["reused" if reuse else "retained"] = dict(
            schema="stronger_arithmetic_components_v1",
            reuse=reuse,
            reduced=reduced,
            **resources,
            total=dict(ledger.counts),
            native={k: native[k] for k in ("u", "cx")},
            compiler_counts=native,
            A_num_qubits_excluding_loader_ancillas=resources["qubits"],
            workspace_qubits=resources["qubits"] - shared_width,
            retained_workspace_qubits=len(layouts[False][0].depths) - shared_width,
            reused_workspace_qubits=len(layouts[True][0].depths) - shared_width,
            conversion_scratch_per_row=scratch_width,
            conversion_forward=conversion_counts,
            aggregation=agg.resources(),
            postaggregation_payoff=post.resources(),
            comparator=cmp.resources(),
            emitted_gate_applications=applications,
            row_checks=row_checks,
            semantic_checks=checks,
            aggregation_included=True,
            aggregation_zero_initialized=True,
            loading_included=False,
            ae_included=False,
            native_basis=["u", "cx"],
            qualification="Actual emitted/remapped X/CX/CCX dependency depth; exact standard "
            "X/CCX decomposition to U/CX, no global optimizer, connectivity or physical synthesis. "
            "Includes all arithmetic inverses; excludes loader and selector preparation.",
        )
    return result


def components_both(plan, reduced=False):
    """Return {'retained': result, 'reused': result} from one acquisition.

    Certificate validation runs even on cache hits. Exact effective circuit
    configurations share cached acquisitions (e.g. degrees with trailing zero
    coefficients). Returned dictionaries are independent of the bounded cache.
    """
    if type(reduced) is not bool:
        raise ValueError("reduced must be boolean")
    key, proof = _certificate(plan, reduced)
    result = deepcopy(
        _acquire(key, MAX_CONVERSION_GATES, MAX_CONVERSION_QUBITS, MAX_COMPONENT_GATES)
    )
    for item in result.values():
        item["poststrike_bounds"] = dict(proof)
        if any(
            row["payoff_integer"] > proof["payoff_upper_integer"] for row in item["semantic_checks"]
        ):
            raise ArithmeticError("checked payoff exceeds universal plan certificate")
    return result


def components(plan, reuse=None, reduced=False):
    """Both layouts by default; explicit reuse=True/False selects one layout."""
    if reuse is not None and type(reuse) is not bool:
        raise ValueError("reuse must be boolean or None")
    result = components_both(plan, reduced)
    return result if reuse is None else result["reused" if reuse else "retained"]
