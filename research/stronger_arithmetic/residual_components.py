"""Residual arithmetic costing from bound primary evidence and a new oracle.

No conversion is rebuilt. The runner must attach ``parent_plan`` to its reused
primary component record after verifying the archive's case/spec binding.
Counts are emitted logical costs; depth_upper is a conservative projection,
not the dependency depth of a fully remapped residual circuit.
"""

from copy import deepcopy
import hashlib
import json

from research.journal_sprint.matched_arithmetic import compiler_counts
from research.journal_sprint.reversible_fixed_point import basis, constant, subtract
from .budget import evaluate_reduced_integer
from .components import ResourceLimitError, _BoundedProgram, _certificate
from .residual_circuits import residual_payoff_flag

MAX_ORACLE_GATES = 8_000_000
MAX_ORACLE_QUBITS = 4096
MAX_COMPONENT_GATES = 100_000_000
_GATES = ("x", "cx", "ccx")


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _digest(value):
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _counts(record):
    values = {k: record[k] for k in _GATES}
    if any(type(v) is not int or v < 0 for v in values.values()):
        raise ValueError("nonnegative emitted gate counts required")
    return values


def _positive_integer(value, label):
    if type(value) is not int or value < 1:
        raise ValueError(label + " must be a positive integer")
    return value


def _validate(parent, certificate, base):
    _certificate(parent, True)
    encoded = _canonical(parent)
    if _canonical(certificate.get("parent_plan")) != encoded:
        raise ValueError("residual certificate parent_plan mismatch")
    if _canonical(base.get("parent_plan")) != encoded:
        raise ValueError("base component requires matching runner-bound parent_plan")
    if certificate.get("overflow_safe") is not True or certificate.get("overflow_failures"):
        raise ArithmeticError("residual overflow certificate required")
    if certificate.get("schema") != "signed_residual_plan_v1":
        raise ValueError("signed residual certificate schema required")
    for field in ("width", "fraction_bits", "strike_sum"):
        if certificate[field] != parent[field]:
            raise ValueError("residual/parent mismatch: " + field)
    if certificate["dimension"] != len(parent["affine_rows"]):
        raise ValueError("residual dimension mismatch")
    w = parent["width"]
    s = _positive_integer(certificate["selector_bits"], "selector_bits")
    if s >= w:
        raise ArithmeticError("residual selector must fit signed word")
    shift = certificate["shift_integer"]
    lo, hi = certificate["residual_integer_bounds"]
    tl, th = certificate["threshold_integer_bounds"]
    if any(type(v) is not int for v in (shift, lo, hi, tl, th)) or not (
        0 <= shift < 1 << (w - 1)
        and -(1 << (w - 1)) <= lo <= hi < 1 << (w - 1)
        and tl == lo + shift
        and th == hi + shift
        and 0 <= tl <= th < 1 << s
    ):
        raise ArithmeticError("universal residual/shift/selector bounds failed")
    if (
        base.get("schema") != "stronger_arithmetic_components_v1"
        or base.get("reuse") is not True
        or base.get("reduced") is not True
        or base.get("aggregation_included") is not True
        or base.get("aggregation_zero_initialized") is not True
    ):
        raise ValueError("reused reduced primary component with zero-start aggregation required")
    conv, agg, post, cmp = (
        _counts(base[k])
        for k in ("conversion_forward", "aggregation", "postaggregation_payoff", "comparator")
    )
    total = _counts(base["total"])
    if total != {k: 2 * conv[k] + 2 * agg[k] + 2 * post[k] + cmp[k] for k in _GATES}:
        raise ValueError("base component count identity failed")
    native = compiler_counts(total)
    if base["native"] != {k: native[k] for k in ("u", "cx")}:
        raise ValueError("base native counts disagree with emitted counts")
    if base["emitted_gate_applications"] != sum(total.values()):
        raise ValueError("base emitted gate applications mismatch")
    n, sold = parent["normal_qubits"], parent["selector_bits"]
    scratch = _positive_integer(base["conversion_scratch_per_row"], "conversion scratch")
    expected_qubits = (
        n + sold + 1 + 2 * w * len(parent["affine_rows"]) + scratch + 3 * w + 1 + 2 * (sold + 1)
    )
    if base["qubits"] != expected_qubits:
        raise ValueError("base allocation identity failed")
    _positive_integer(base["logical_depth"], "base logical depth")
    _positive_integer(base["aggregation"]["logical_depth"], "aggregation logical depth")
    # Independently check that the recorded endpoints are from this integer map.
    endpoints = (0, (1 << n) - 1)
    row_evidence = {(r["row"], r["packed_input"]): r for r in base["row_checks"]}
    if len(row_evidence) != 2 * len(parent["affine_rows"]):
        raise ValueError("base endpoint conversion evidence missing")
    totals = []
    budget = parent["exp_budget"]
    for packed in endpoints:
        total_value = 0
        for i, (a, cs) in enumerate(parent["affine_rows"]):
            log = a + sum(((packed >> k) & 1) * c for k, c in enumerate(cs))
            price = evaluate_reduced_integer(
                log,
                budget["coefficients"],
                parent["fraction_bits"],
                parent["reductions"],
                parent["spot"],
            )
            record = row_evidence.get((i, packed), {})
            if (
                record.get("log_integer") != log
                or record.get("price_integer") != price
                or record.get("clean_workspace") is not True
                or record.get("inverse_checked") is not True
            ):
                raise ValueError("base endpoint conversion evidence mismatch")
            total_value += price
        totals.append((packed, total_value))
    return conv, agg, totals


def _reference(total, certificate):
    """Unbounded integer reference at certificate scale (also usable in tiny tests)."""
    unit = 1 << certificate["fraction_bits"]
    delta = total - certificate["strike_sum"]
    x = delta * certificate["reciprocal_integer"] // unit
    cs = certificate["control_coefficients"]
    y = cs[-1]
    for c in reversed(cs[:-1]):
        y = x * y // unit + c
    control = y * certificate["control_scale_integer"] // unit
    residual = max(delta, 0) - control
    return dict(
        sum_integer=total,
        poststrike_integer=delta,
        normalized_integer=x,
        polynomial_integer=y,
        control_integer=control,
        residual_integer=residual,
        threshold_integer=residual + certificate["shift_integer"],
    )


def _oracle(certificate):
    # Use the same emitter as residual_program, with allocation-time caps and
    # the missing sum->delta->sum wrapper. The strike is restored to zero.
    p = _BoundedProgram()
    w, s = certificate["width"], certificate["selector_bits"]
    total, selector, flag = p.register(w), p.register(s), p.register(1)[0]
    strike, helper = p.register(w), p.register(1)[0]
    start = len(p.gates)
    constant(p, strike, certificate["strike_sum"])
    subtract(p, strike, total, helper)
    stop = len(p.gates)
    residual_payoff_flag(
        p,
        total,
        selector,
        flag,
        certificate["control_coefficients"],
        certificate["fraction_bits"],
        certificate["reciprocal_integer"],
        certificate["control_scale_integer"],
        certificate["shift_integer"],
    )
    p.undo(start, stop)
    if len(p.gates) > MAX_ORACLE_GATES or p.qubits > MAX_ORACLE_QUBITS:
        raise ResourceLimitError("residual oracle exceeds 8M gates or 4096 wires")
    return p, total, selector, flag


def _packed_checks(p, cases):
    """Simulate all endpoint/selector/flag cases in parallel bits per wire."""
    mask = (1 << len(cases)) - 1
    initial = [
        sum(((state >> b) & 1) << j for j, (state, _) in enumerate(cases)) for b in range(p.qubits)
    ]
    expected = [
        sum(((state >> b) & 1) << j for j, (_, state) in enumerate(cases)) for b in range(p.qubits)
    ]
    wires = list(initial)
    data = p.gates.data
    for inverse in (False, True):
        indices = range(len(data) - 4, -1, -4) if inverse else range(0, len(data), 4)
        for i in indices:
            arity, a = data[i], data[i + 1]
            if arity == 1:
                wires[a] ^= mask
            elif arity == 2:
                wires[data[i + 2]] ^= wires[a]
            else:
                wires[data[i + 3]] ^= wires[a] & wires[data[i + 2]]
        if wires != (initial if inverse else expected):
            raise ArithmeticError("residual oracle endpoint map or clean workspace failed")


def residual_components(parent_plan, residual_certificate, base_component_reused):
    """Compose bound primary evidence with an actually emitted complete oracle.

    ``base_component_reused['parent_plan']`` must be attached by the archive
    consumer; an unbound component record is deliberately rejected. Existing
    certificates are trusted evidence, not regenerated financial proofs here.
    """
    parent, cert, base = parent_plan, residual_certificate, base_component_reused
    conv, agg, totals = _validate(parent, cert, base)
    inherited = {k: 2 * conv[k] + 2 * agg[k] for k in _GATES}
    if sum(inherited.values()) >= MAX_COMPONENT_GATES:
        raise ResourceLimitError("residual component exceeds 100M gate applications")
    p, total, selector, flag = _oracle(cert)
    oracle = p.resources()
    counts = {k: inherited[k] + oracle[k] for k in _GATES}
    applications = sum(counts.values())
    if applications > MAX_COMPONENT_GATES:
        raise ResourceLimitError("residual component exceeds 100M gate applications")
    evidence, cases = [], []
    for packed, value in totals:
        reference = _reference(value, cert)
        numerator = reference["threshold_integer"]
        lo, hi = cert["threshold_integer_bounds"]
        if not lo <= numerator <= hi:
            raise ArithmeticError("endpoint exceeds universal residual threshold certificate")
        choices = sorted({0, (1 << len(selector)) - 1, max(0, numerator - 1), numerator})
        for u in choices:
            for b in (0, 1):
                initial = basis(total, value) | basis(selector, u) | (b << flag)
                cases.append((initial, initial ^ (int(u < numerator) << flag)))
        evidence.append(
            dict(
                reference,
                packed_input=packed,
                selectors=choices,
                both_initial_flags_checked=True,
                clean_workspace=True,
                inverse_checked=True,
            )
        )
    _packed_checks(p, cases)
    n, s, w, d = (
        parent["normal_qubits"],
        cert["selector_bits"],
        parent["width"],
        len(parent["affine_rows"]),
    )
    # Includes total and every oracle-private wire. Reuse its zero helper for
    # ripple aggregation before/after the oracle; no extra hidden ancilla.
    oracle_private = p.qubits - s - 1
    qubits = n + s + 1 + 2 * w * d + base["conversion_scratch_per_row"] + oracle_private
    native = compiler_counts(counts)
    # Each inherited prefix/suffix is a subsequence of the primary circuit,
    # hence individually bounded by its depth. Separately, gate count bounds
    # the sum of conversion depths. Neither bound claims full remapped depth.
    inherited_depth_upper = min(
        2 * base["logical_depth"], 2 * sum(conv.values()) + 2 * base["aggregation"]["logical_depth"]
    )
    return dict(
        schema="signed_residual_components_v1",
        native={k: native[k] for k in ("u", "cx")},
        qubits=qubits,
        depth_upper=inherited_depth_upper + oracle["logical_depth"],
        depth_kind="conservative_composition_upper_bound",
        actual_remapped_depth=False,
        depth_bound_derivation="min(2*primary_full_depth, 2*conversion_forward_gate_count "
        "+ 2*aggregation_depth) + complete_oracle_depth",
        total=counts,
        compiler_counts=native,
        emitted_gate_applications=applications,
        inherited_conversion_forward=deepcopy(conv),
        inherited_aggregation_forward=deepcopy(agg),
        complete_postoracle=oracle,
        oracle_private_qubits=oracle_private,
        wire_layout=dict(
            inputs=n,
            selector=s,
            flag=1,
            retained_logs_spots=2 * w * d,
            shared_conversion_scratch=base["conversion_scratch_per_row"],
            total_and_oracle_private=oracle_private,
        ),
        aggregation_helper="oracle strike-subtraction helper; zero before and after oracle",
        parent_plan_sha256=_digest(parent),
        base_component_sha256=_digest(base),
        residual_certificate_sha256=_digest(cert),
        semantic_checks=evidence,
        aggregation_included=True,
        all_inverses_included=True,
        loading_included=False,
        selector_preparation_included=False,
        ae_included=False,
        qualification="Inherited emitted conversion/aggregation counts plus new emitted "
        "sum-to-delta, signed control, shift, comparator and all inverses. "
        "Qubits use shared clean conversion scratch and separate oracle scratch. "
        "Depth is a conservative projection, not an actually remapped full-circuit depth.",
    )
