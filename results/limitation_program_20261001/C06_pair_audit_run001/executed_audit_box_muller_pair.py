"""Independent audit of the frozen joint-pair and B4 first-date coupling.

No certificate generator or financial evaluator is imported. Actual SSA nodes
are matched to the native midpoint, normalization, table Horner and stock
polynomial operations. Independent interval enclosures use a rational pi
identity different from the producer's interval constant.
"""

from __future__ import annotations

# Long receipt explanations are deliberate.
# ruff: noqa: E501

import argparse
import ast
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import shutil
import sys
import traceback
import xml.etree.ElementTree as ET

import mpmath as mp

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
Q = 1 << 40
EPSILON = Fraction(1, Q)
LIMIT = 1 << 31
CASES = {"B4x12": (4, 12, 30), "B8x52": (8, 52, 234)}


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    with Path(path).open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def relative(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def encoded(value):
    value = Fraction(value)
    return [value.numerator, value.denominator]


def decoded(value):
    assert len(value) == 2 and all(type(v) is int for v in value) and value[1] > 0
    result = Fraction(*value)
    assert encoded(result) == value
    return result


def signed(value):
    value %= 1 << 72
    return value - (1 << 72) if value >= 1 << 71 else value


def verify(files):
    for name, expected in files.items():
        assert sha(ROOT / name) == expected, ("immutable file changed", name)


def exact(record, name, expected):
    assert decoded(record[name]) == expected, (name, decoded(record[name]), expected)


def iv(value):
    value = Fraction(value)
    return mp.iv.mpf(value.numerator) / value.denominator


def endpoint(value):
    sign, mantissa, exponent, _ = value
    return Fraction((-1) ** sign * mantissa) * Fraction(2) ** exponent


def enclosure(value):
    return tuple(endpoint(part) for part in value._mpi_)


def upper(value):
    return enclosure(value)[1]


def error(value, bounds):
    return max(abs(value - bounds[0]), abs(value - bounds[1]))


def validate_transcendental(record, name, calculation):
    """The charged90-digit endpoint must enclose a fresh130-digit result."""
    charged, computed = decoded(record[name]), upper(calculation)
    assert charged >= computed, ("transcendental bound too small", name)
    assert charged - computed <= Fraction(1, 1 << 260) * max(1, abs(charged)), (
        "unexplained transcendental allowance",
        name,
    )
    return charged


def independent_pi():
    # atan(1/2)+atan(1/3) is in (0,pi/2), and tangent addition equals1.
    assert (Fraction(1, 2) + Fraction(1, 3)) / (1 - Fraction(1, 6)) == 1
    bounds = []
    for denominator in (2, 3):
        term, partial = Fraction(1, denominator), Fraction(0)
        for j in range(240):
            partial += (-1 if j % 2 else 1) * term / (2 * j + 1)
            term /= denominator**2
        bounds.append((partial, partial + term / 481))
    lo = 4 * sum(row[0] for row in bounds)
    hi = 4 * sum(row[1] for row in bounds)
    assert hi - lo < Fraction(1, 10**140)
    return mp.iv.mpf([iv(lo).a, iv(hi).b])


class ActualGraph:
    """Strict operation matching on the actual accepted target, not a builder."""

    def __init__(self, target):
        assert target["width"] == 72 and target["fraction_bits"] == 40
        self.target = target
        self.nodes = {value: node for node in target["nodes"] for value in node["out"]}
        assert len(self.nodes) == sum(len(node["out"]) for node in target["nodes"])

    def node(self, value, op=None, params=None):
        node = self.nodes[value]
        assert op is None or node["op"] == op, (value, op, node)
        assert params is None or node["params"] == params, (value, params, node)
        return node

    def const(self, value, raw):
        node = self.node(value, "const")
        assert signed(node["params"]["value"]) == raw, (value, raw)
        return value

    def unordered(self, value, op, args):
        assert sorted(self.node(value, op)["args"]) == sorted(args), (value, op, args)

    def clip(self, value, low, high):
        flag, middle, hi = self.node(value, "select")["args"]
        self.const(hi, high)
        assert self.node(flag, "lt")["args"] == [middle, hi]
        lo_flag, lo, raw = self.node(middle, "select")["args"]
        self.const(lo, low)
        assert self.node(lo_flag, "lt")["args"] == [raw, lo]
        return raw

    def midpoint(self, value, input_id):
        args = self.node(value, "add")["args"]
        shifts = [arg for arg in args if self.node(arg)["op"] == "bits"]
        assert len(shifts) == 1
        shift = shifts[0]
        assert self.node(shift, "bits", dict(shift=-8, width=72, signed=False))["args"] == [
            input_id
        ]
        self.const(next(arg for arg in args if arg != shift), 128)

    def ancestors(self, value):
        found, pending = set(), [value]
        while pending:
            current = pending.pop()
            if current not in found:
                found.add(current)
                pending.extend(self.node(current)["args"])
        return found

    def interpolation(self, value, name, argument):
        segments, degree, lo = (32, 8, Q) if name == "log" else (64, 7, 0)
        index_bits = int(math.log2(segments))
        candidates = {
            tuple(self.node(v)["out"])
            for v in self.ancestors(value)
            if self.node(v)["op"] == "lookup" and self.node(v)["params"]["table"] == name
        }
        assert len(candidates) == 1
        outputs = next(iter(candidates))
        lookup = self.node(outputs[0], "lookup", dict(table=name, bits=index_bits))
        assert len(outputs) == degree + 1
        index = lookup["args"][0]
        address = self.node(
            index, "bits", dict(shift=40 - index_bits, width=index_bits, signed=False)
        )["args"][0]
        if lo:
            address_args = self.node(address, "sub")["args"]
            address, lower_guard = address_args
            self.const(lower_guard, lo)
        bounded = address
        assert self.clip(bounded, lo, lo + Q - 1) == argument
        current, local = value, None
        for j in range(degree):
            args = self.node(current, "add")["args"]
            assert outputs[j] in args and len(args) == 2
            product = next(arg for arg in args if arg != outputs[j])
            factors = self.node(product, "mul")["args"]
            if local is None:
                possible = [v for v in factors if self.node(v)["op"] == "sub"]
                assert len(possible) == 1
                local = possible[0]
            assert local in factors
            current = next(arg for arg in factors if arg != local)
        assert current == outputs[-1]
        actual_x, center = self.node(local, "sub")["args"]
        assert actual_x == bounded
        center_args = self.node(center, "add")["args"]
        center_shifts = [v for v in center_args if self.node(v)["op"] == "bits"]
        assert len(center_shifts) == 1
        center_shift = center_shifts[0]
        assert self.node(center_shift, "bits", dict(shift=index_bits - 40, width=72, signed=False))[
            "args"
        ] == [index]
        self.const(next(v for v in center_args if v != center_shift), lo + Q // (2 * segments))
        return dict(
            output=value,
            input=argument,
            address=index,
            local=local,
            lookup_outputs=list(outputs),
            floors=degree,
        )

    def pair(self, roots, raw_u, raw_v, literal_ln2):
        first, second = roots
        assert len(roots) == 2
        output_factors = [self.node(v, "mul")["args"] for v in roots]
        common = set(output_factors[0]).intersection(output_factors[1])
        assert len(common) == 1
        radius = next(iter(common))
        radius_input = self.node(radius, "sqrt")["args"][0]
        negative_two = self.node(radius_input, "positive")["args"][0]
        log_value = self.node(negative_two, "cmul", dict(c=-2 * Q))["args"][0]
        log_args = self.node(log_value, "add")["args"]
        exponent_terms = [v for v in log_args if self.node(v)["op"] == "cmul"]
        assert len(exponent_terms) == 1
        exponent_term = exponent_terms[0]
        exponent_scaled = self.node(exponent_term, "cmul", dict(c=literal_ln2))["args"][0]
        exponent = self.node(exponent_scaled, "bits", dict(shift=-40, width=72, signed=False))[
            "args"
        ][0]
        top, fraction = self.node(exponent, "sub")["args"]
        self.const(fraction, 40)
        safe_u = self.node(top, "msb")["args"][0]
        lowflag, tiny, midpoint_u = self.node(safe_u, "select")["args"]
        self.const(tiny, 1)
        assert self.node(lowflag, "lt")["args"] == [midpoint_u, tiny]
        self.midpoint(midpoint_u, raw_u)
        log_poly = next(v for v in log_args if v != exponent_term)
        # Recover the normalized argument from the log interpolation clip.
        lookups = [self.node(v) for v in self.ancestors(log_poly) if self.node(v)["op"] == "lookup"]
        assert len({tuple(n["out"]) for n in lookups}) == 1
        index = lookups[0]["args"][0]
        address = self.node(index)["args"][0]
        clipped = self.node(address, "sub")["args"][0]
        mantissa = self.clip(clipped, Q, 2 * Q - 1)
        mantissa_u, negative_exponent = self.node(mantissa, "shift")["args"]
        assert mantissa_u == safe_u
        zero, negated = self.node(negative_exponent, "sub")["args"]
        self.const(zero, 0)
        assert negated == exponent
        log_scope = self.interpolation(log_poly, "log", mantissa)
        cos_values = [next(v for v in factors if v != radius) for factors in output_factors]
        cos_arguments = []
        for cosine in cos_values:
            lookup_nodes = [
                self.node(v) for v in self.ancestors(cosine) if self.node(v)["op"] == "lookup"
            ]
            assert len({tuple(n["out"]) for n in lookup_nodes}) == 1
            cos_index = lookup_nodes[0]["args"][0]
            cos_clip = self.node(cos_index)["args"][0]
            cos_arguments.append(self.clip(cos_clip, 0, Q - 1))
        midpoint_v, quarter = cos_arguments
        self.midpoint(midpoint_v, raw_v)
        quarter_sum = self.node(quarter, "bits", dict(shift=0, width=40, signed=False))["args"][0]
        angular_args = self.node(quarter_sum, "add")["args"]
        assert midpoint_v in angular_args
        self.const(next(v for v in angular_args if v != midpoint_v), 3 * Q // 4)
        cosine_scopes = [
            self.interpolation(v, "cos", a) for v, a in zip(cos_values, cos_arguments, strict=True)
        ]
        assert {
            v
            for v in self.ancestors(first) | self.ancestors(second)
            if self.node(v)["op"] == "input"
        } == {raw_u, raw_v}
        return dict(
            normal_values=list(roots),
            raw_uniform_values=[raw_u, raw_v],
            radius=radius,
            log=log_scope,
            cosines=cosine_scopes,
            original_shared_pair_preserved=True,
        )


def audit_sources(certificate):
    targets, supports, reports = {}, {}, {}
    for case, (assets, dates, count) in CASES.items():
        binding = certificate["source_bindings"][case]
        target_path = ROOT / binding["target"]
        assert target_path == PROGRAM / "A10_coefficient_run001" / case / "min-depth/target.json"
        assert sha(target_path) == binding["target_sha256"]
        target, support = (
            read(target_path),
            read(PROGRAM / "E03_support_run001" / (case + "_certificate.json")),
        )
        graph = ActualGraph(target)
        assert binding["pair_count"] == count and binding["scalar_count"] == 2 * count == dates * (
            assets + 1
        )
        roots = binding["normal_values"]
        assert len(roots) == len(set(roots)) == 2 * count
        inputs = [node for node in target["nodes"] if node["op"] == "input"]
        assert [n["out"][0] for n in inputs] == target["inputs"]
        assert len(inputs) == 2 * count
        for j, node in enumerate(inputs):
            assert node["params"] == dict(name="uniform_%d" % j, bits=32, preparation="uniform")
        scopes = [
            graph.pair(
                roots[2 * j : 2 * j + 2],
                inputs[2 * j]["out"][0],
                inputs[2 * j + 1]["out"][0],
                binding["literal_ln2"],
            )
            for j in range(count)
        ]
        assert support["assets"] == assets and support["dates"] == dates
        support_binding = certificate["payoff_support_bindings"][case]
        support_path, support_audit_path = (
            ROOT / support_binding["certificate"],
            ROOT / support_binding["independent_audit"],
        )
        assert (
            sha(support_path) == support_binding["certificate_sha256"]
            and sha(support_audit_path) == support_binding["independent_audit_sha256"]
        )
        assert support_path == PROGRAM / "E03_support_run001" / (case + "_certificate.json")
        support_audit = read(support_audit_path)
        assert (
            support_audit["passed"]
            and support_audit["payoff_raw_bounds"] == support["payoff_raw_bounds"]
        )
        assert 0 == support["payoff_raw_bounds"][0] <= support["payoff_raw_bounds"][1] < 40 * Q
        exact(support_binding, "payoff_difference_on_bad_event_upper_dollars_exact", Fraction(40))
        targets[case], supports[case] = target, support
        reports[case] = dict(
            passed=True,
            joint_pairs=count,
            scalar_normal_outputs=2 * count,
            original_input_law=True,
            independently_walked_pair_scopes=scopes,
            digital_discounted_support_raw=support["payoff_raw_bounds"],
            tail_absolute_difference_dollars_exact=[40, 1],
        )
        print(case, count, "actual joint pair graphs and digital support PASS", flush=True)
    assert targets["B4x12"]["tables"] == targets["B8x52"]["tables"]
    assert (
        certificate["source_bindings"]["B4x12"]["literal_ln2"]
        == certificate["source_bindings"]["B8x52"]["literal_ln2"]
    )
    return targets, supports, reports


def audit_table(name, rows, saved, pi):
    segments, degree = (32, 8) if name == "log" else (64, 7)
    assert saved["name"] == name and saved["segments"] == segments and saved["degree"] == degree
    assert len(rows) == segments and all(len(row) == degree + 1 for row in rows)
    assert len(saved["coefficient_checks"]) == segments * (degree + 1)
    radius, weighted_errors, magnitude = Fraction(1, 2 * segments), [], Fraction(0)
    checks = []
    for index, row in enumerate(rows):
        center = Fraction(name == "log") + Fraction(2 * index + 1, 2 * segments)
        errors = []
        for j, raw in enumerate(row):
            record = saved["coefficient_checks"][index * (degree + 1) + j]
            assert record["row"] == index and record["degree"] == j and record["literal"] == raw
            if name == "log":
                true = (
                    enclosure(mp.iv.log(iv(center)))
                    if j == 0
                    else (Fraction((-1) ** (j - 1), j) / center**j,) * 2
                )
            else:
                true = enclosure(
                    (2 * pi) ** j * mp.iv.cos(2 * pi * iv(center) + j * pi / 2) / math.factorial(j)
                )
            original = tuple(decoded(part) for part in record["true_coefficient_enclosure"])
            assert original[0] <= true[0] <= true[1] <= original[1], (
                name,
                index,
                j,
                "true interval containment",
            )
            literal_error = error(Fraction(raw, Q), original)
            assert literal_error <= EPSILON / 2
            exact(record, "rounding_error_upper_exact", literal_error)
            errors.append(literal_error)
            checks.append(
                dict(
                    row=index,
                    degree=j,
                    literal=raw,
                    independent_true_coefficient_enclosure=[encoded(part) for part in true],
                    original_enclosure_contains_independent_enclosure=True,
                    nearest_rounding_proved=True,
                )
            )
        weighted_errors.append(sum((e * radius**j for j, e in enumerate(errors)), Fraction(0)))
        bound = abs(Fraction(row[-1], Q))
        magnitude = max(magnitude, bound)
        for raw in row[-2::-1]:
            product_bound = radius * bound + EPSILON
            bound = abs(Fraction(raw, Q)) + product_bound
            magnitude = max(magnitude, bound, product_bound)
    remainder = (
        radius ** (degree + 1) / (degree + 1)
        if name == "log"
        else validate_transcendental(
            saved,
            "Taylor_remainder_upper_exact",
            (2 * pi * iv(radius)) ** (degree + 1) / math.factorial(degree + 1),
        )
    )
    exact(saved, "Taylor_remainder_upper_exact", remainder)
    exact(saved, "coefficient_rounding_upper_exact", max(weighted_errors))
    floors = EPSILON * sum((radius**j for j in range(degree)), Fraction(0))
    exact(saved, "Horner_floor_upper_exact", floors)
    exact(saved, "total_error_upper_exact", remainder + max(weighted_errors) + floors)
    exact(saved, "maximum_native_intermediate_magnitude_exact", magnitude)
    assert magnitude < LIMIT and saved["signed_overflow_excluded"]
    return dict(
        passed=True,
        coefficients_verified=len(checks),
        checks=checks,
        signed_floor_geometric_charge_exact=encoded(floors),
        total_error_upper_exact=saved["total_error_upper_exact"],
        maximum_intermediate_magnitude_exact=encoded(magnitude),
        every_signed_Horner_product_charged=True,
        native_signed_overflow_excluded=True,
    )


def audit_pair(candidate, certificate, pi):
    cutoff = candidate["cutoff_bits"]
    assert cutoff in (20, 24)
    delta, h = Fraction(1, 1 << cutoff), Fraction(1, 1 << 33)
    assert delta * (1 << 32) == int(delta * (1 << 32))
    exact(candidate, "delta_exact", delta)
    grid = candidate["radial_grid"]
    r = mp.iv.sqrt(-2 * mp.iv.log(iv(delta)))
    assert enclosure(-2 * mp.iv.log(iv(Fraction(1, 2) + h)))[0] > 1
    low = validate_transcendental(grid, "low_u_derivative_bound_exact", iv(h) / (iv(delta) * r))
    high = validate_transcendental(
        grid, "high_u_Holder_bound_exact", mp.iv.sqrt(iv(2 * h / (Fraction(1, 2) - h)))
    )
    radial_max = validate_transcendental(grid, "radial_maximum_upper_exact", r)
    radial_grid = max(low, high)
    exact(grid, "radial_grid_error_upper_exact", radial_grid)
    assert grid["midpoint_remains_above_cutoff"]
    ln2_literal = Fraction(certificate["source_bindings"]["B4x12"]["literal_ln2"], Q)
    ln2_error = decoded(candidate["log_ln2_literal_error_per_exponent_exact"])
    true_error = error(ln2_literal, enclosure(mp.iv.log(iv(2))))
    assert true_error <= ln2_error <= true_error + Fraction(1, 1 << 260)
    log_error = (
        decoded(certificate["log_table_certificate"]["total_error_upper_exact"])
        + cutoff * ln2_error
    )
    exact(candidate, "log_error_upper_exact", log_error)
    exact(candidate, "sqrt_argument_approximation_error_upper_exact", 2 * log_error)
    holder = validate_transcendental(
        candidate, "radius_Holder_error_upper_exact", mp.iv.sqrt(iv(2 * log_error))
    )
    radius_error = holder + EPSILON
    cosine_error = decoded(certificate["cos_table_certificate"]["total_error_upper_exact"])
    arithmetic = radius_error + (radial_max + radius_error) * cosine_error + EPSILON
    exact(candidate, "normal_arithmetic_error_upper_exact", arithmetic)
    angular = validate_transcendental(
        candidate, "angular_grid_error_upper_exact", 2 * pi * iv(h) * iv(radial_max)
    )
    exact(candidate, "normal_grid_error_upper_exact", radial_grid + angular)
    coordinate = arithmetic + radial_grid + angular
    exact(candidate, "coordinate_discrepancy_upper_exact", coordinate)
    exact(candidate, "joint_pair_Linf_discrepancy_upper_exact", coordinate)
    validate_transcendental(
        candidate, "joint_pair_L2_discrepancy_upper_exact", mp.iv.sqrt(2) * iv(coordinate)
    )
    for name in (
        "log_normalization_shift_error_exact",
        "log_exponent_times_ln2_floor_error_exact",
        "negative_two_log_floor_error_exact",
        "angular_quarter_turn_and_wrap_error_exact",
    ):
        exact(candidate, name, Fraction(0))
    for name in ("sqrt_floor_error_upper_exact", "final_multiply_floor_error_upper_exact"):
        exact(candidate, name, EPSILON)
    assert candidate["good_event"] == "Shared radial U>=delta"
    return dict(
        passed=True,
        cutoff_bits=cutoff,
        coordinate_discrepancy_upper_exact=encoded(coordinate),
        joint_pair_Linf_discrepancy_upper_exact=encoded(coordinate),
        original_joint_shared_input_law=True,
        signed_native_floor_charges_reconciled=True,
        exact_normalization_and_integer_ln2_products=True,
        high_U_radial_Holder_bound_verified=True,
        conditional_normal_independence_used=False,
    )


def polynomial(graph, root, variable, radius):
    # Walk topological SSA order independently of the producer's recursive proof.
    needed = set()
    pending = [root]
    while pending:
        v = pending.pop()
        if v != variable and v not in needed:
            needed.add(v)
            pending.extend(graph.node(v)["args"])
    cache = {variable: ({1: Fraction(1)}, Fraction(0))}
    steps = {}

    def magnitude(poly):
        return sum((abs(c) * radius**degree for degree, c in poly.items()), Fraction(0))

    for node in graph.target["nodes"]:
        v = node["out"][0]
        if v not in needed:
            continue
        assert len(node["out"]) == 1
        if node["op"] == "const":
            coefficients, floor = {0: Fraction(signed(node["params"]["value"]), Q)}, Fraction(0)
        else:
            assert node["op"] in ("mul", "add") and len(node["args"]) == 2
            (a, ea), (b, eb) = (cache[arg] for arg in node["args"])
            coefficients = Counter()
            if node["op"] == "add":
                for degree, c in list(a.items()) + list(b.items()):
                    coefficients[degree] += c
                floor = ea + eb
            else:
                for ja, ca in a.items():
                    for jb, cb in b.items():
                        coefficients[ja + jb] += ca * cb
                floor = magnitude(a) * eb + magnitude(b) * ea + ea * eb + EPSILON
            coefficients = dict(coefficients)
        bound = magnitude(coefficients) + floor
        assert bound < LIMIT
        cache[v] = coefficients, floor
        steps[v] = dict(
            value=v,
            op=node["op"],
            magnitude_upper_exact=encoded(bound),
            floor_error_upper_exact=encoded(floor),
        )
    coefficients, floor = cache[root]
    return coefficients, floor, steps


def flatten_sum(graph, value):
    result, pending = [], [value]
    while pending:
        current = pending.pop()
        node = graph.node(current)
        if node["op"] == "add":
            pending.extend(node["args"])
        else:
            result.append(current)
    return result


def date_structure(target, normal_values, support, saved):
    graph, scopes = ActualGraph(target), []
    alpha_literal, common_literal, idio_literal, constants, guard_bounds = (
        None,
        None,
        None,
        None,
        None,
    )
    for asset in range(4):
        stock = support["stock_ids"][12 * asset]
        polynomial_root, k = graph.node(stock, "shift")["args"]
        k_mult = graph.node(k, "bits", dict(shift=40, width=72, signed=True))["args"][0]
        alpha_node = graph.node(k_mult, "cmul")
        clipped = alpha_node["args"][0]
        assert clipped == support["clipped_log_ids"][12 * asset]
        _, middle, hi = graph.node(clipped, "select")["args"]
        _, lo, raw = graph.node(middle, "select")["args"]
        bounds = (
            signed(graph.node(lo, "const")["params"]["value"]),
            signed(graph.node(hi, "const")["params"]["value"]),
        )
        assert graph.clip(clipped, *bounds) == raw
        leaves = flatten_sum(graph, raw)
        products = {
            graph.node(v)["args"][0]: graph.node(v)["params"]["c"]
            for v in leaves
            if graph.node(v)["op"] == "cmul"
        }
        current_constants = sorted(
            signed(graph.node(v)["params"]["value"])
            for v in leaves
            if graph.node(v)["op"] == "const"
        )
        assert len(leaves) == 4 and len(products) == len(current_constants) == 2
        assert set(products) == {normal_values[0], normal_values[asset + 1]}
        if asset == 0:
            alpha_literal = alpha_node["params"]["c"]
            common_literal, idio_literal = products[normal_values[0]], products[normal_values[1]]
            constants, guard_bounds = current_constants, bounds
        assert products == {
            normal_values[0]: common_literal,
            normal_values[asset + 1]: idio_literal,
        }
        assert (
            current_constants == constants
            and bounds == guard_bounds
            and alpha_node["params"]["c"] == alpha_literal
        )
        remainder_nodes = [
            n
            for n in target["nodes"]
            if n["op"] == "sub"
            and n["args"][0] == clipped
            and graph.node(n["args"][1])["op"] == "cmul"
            and graph.node(n["args"][1])["params"]["c"] == support["literal_ln2"]
        ]
        assert len(remainder_nodes) == 1
        remainder_node = remainder_nodes[0]
        exponent_scaled = graph.node(
            remainder_node["args"][1], "cmul", dict(c=support["literal_ln2"])
        )["args"][0]
        assert graph.node(exponent_scaled, "bits", dict(shift=-40, width=72, signed=False))[
            "args"
        ] == [k]
        scopes.append(
            dict(
                asset=asset,
                stock=stock,
                clipped_log=clipped,
                normal_values=[normal_values[0], normal_values[asset + 1]],
                polynomial_root=polynomial_root,
                remainder=remainder_node["out"][0],
            )
        )
    assert [
        {k: s[k] for k in ("asset", "stock", "clipped_log", "normal_values")} for s in scopes
    ] == saved["all_four_asset_date1_scopes"]
    assert len({j // 2 for j in range(5)}) == saved["Gaussian_pairs_used"] == 3
    return graph, scopes, alpha_literal, common_literal, idio_literal, constants, guard_bounds


def audit_date(target, pair, support, normal_values):
    date = pair["B4_date1"]
    graph, scopes, alpha_raw, common_raw, idio_raw, constants, guards = date_structure(
        target, normal_values, support, date
    )
    assert support["basket_coefficient"] == Q // 4 and date["date"] == 1 and date["assets"] == 4
    assert date["observation_time_exact"] == [1, 12]
    common, idio = Fraction(common_raw, Q), Fraction(idio_raw, Q)
    drift, spot = (Fraction(v, Q) for v in constants)
    exact(date, "common_coefficient_literal_exact", common)
    exact(date, "idiosyncratic_coefficient_literal_exact", idio)
    common_error = decoded(date["common_coefficient_error_upper_exact"])
    idio_error = decoded(date["idiosyncratic_coefficient_error_upper_exact"])
    spot_error = decoded(date["log_spot_literal_error_upper_exact"])
    for literal, calculation, charge in (
        (common, mp.iv.sqrt(iv(Fraction(3, 1000))), common_error),
        (idio, mp.iv.sqrt(iv(Fraction(9, 2000))), idio_error),
        (spot, mp.iv.log(iv(100)), spot_error),
    ):
        computed = error(literal, enclosure(calculation))
        assert computed <= charge <= computed + Fraction(1, 1 << 260)
    drift_error = abs(drift + Fraction(1, 800))
    exact(date, "drift_literal_error_upper_exact", drift_error)
    exact(date, "two_increment_floor_error_upper_exact", 2 * EPSILON)
    radius = decoded(pair["radial_grid"]["radial_maximum_upper_exact"])
    beta = decoded(pair["coordinate_discrepancy_upper_exact"])
    coefficient_sum = abs(common) + abs(idio)
    log_error = (
        coefficient_sum * beta
        + (common_error + idio_error) * radius
        + drift_error
        + spot_error
        + 2 * EPSILON
    )
    exact(date, "log_discrepancy_exact", log_error)
    native_normal_maximum = radius + decoded(pair["normal_arithmetic_error_upper_exact"])
    digital_lo, digital_hi = (
        spot + drift - coefficient_sum * native_normal_maximum - 2 * EPSILON,
        spot + drift + coefficient_sum * native_normal_maximum,
    )
    assert [encoded(digital_lo), encoded(digital_hi)] == date[
        "digital_unclipped_log_enclosure_exact"
    ]
    assert Fraction(guards[0], Q) < digital_lo < digital_hi < Fraction(guards[1], Q)
    assert date["clipping_inactive_on_good_event"]
    assert (
        max(
            abs(digital_lo),
            abs(digital_hi),
            abs(common) * native_normal_maximum + EPSILON,
            abs(idio) * native_normal_maximum + EPSILON,
        )
        < LIMIT
    )
    alpha, ln2 = Fraction(alpha_raw, Q), Fraction(support["literal_ln2"], Q)
    low_k, high_k = math.floor(alpha * digital_lo), math.floor(alpha * digital_hi)
    assert [low_k, high_k] == date["exp_range_exponents"] and 0 <= low_k <= high_k <= 30
    remainder_radius = max(
        abs(Fraction(j + edge) / alpha - j * ln2)
        for j in range(low_k, high_k + 1)
        for edge in (0, 1)
    )
    exact(date, "exp_remainder_magnitude_upper_exact", remainder_radius)
    all_polynomials = []
    for scope in scopes:
        coefficients, evaluation_error, steps = polynomial(
            graph, scope["polynomial_root"], scope["remainder"], remainder_radius
        )
        assert set(coefficients) == set(range(13))
        assert all(
            coefficients[j] == Fraction(round(Fraction(Q, math.factorial(j))), Q) for j in range(13)
        )
        all_polynomials.append((coefficients, evaluation_error, steps))
    coefficients, evaluation_error, steps = all_polynomials[0]
    assert all(c == coefficients and e == evaluation_error for c, e, _ in all_polynomials)
    saved_polynomial = date["exp_polynomial_certificate"]
    assert {str(j): encoded(c) for j, c in sorted(coefficients.items())} == saved_polynomial[
        "coefficients"
    ]
    assert {step["value"]: step for step in saved_polynomial["steps"]} == steps
    assert (
        len(saved_polynomial["steps"]) == len(steps)
        and saved_polynomial["signed_overflow_excluded"]
    )
    exact(saved_polynomial, "evaluation_floor_error_upper_exact", evaluation_error)
    coefficient_error = sum(
        (
            abs(coefficients[j] - Fraction(1, math.factorial(j))) * remainder_radius**j
            for j in range(13)
        ),
        Fraction(0),
    )
    exact(date, "exp_coefficient_error_upper_exact", coefficient_error)
    exact(date, "exp_Estrin_floor_error_upper_exact", evaluation_error)
    remainder_error = validate_transcendental(
        date,
        "exp_Taylor_remainder_upper_exact",
        mp.iv.exp(iv(remainder_radius)) * iv(remainder_radius) ** 13 / math.factorial(13),
    )
    # Reconstruct using the producer's valid ln2 enclosure allowance, not a
    # narrower fresh one: the charged downstream expression must be exact.
    ln2_error = decoded(pair["log_ln2_literal_error_per_exponent_exact"])
    reconstruction = validate_transcendental(
        date,
        "exp_ln2_reconstruction_error_upper_exact",
        mp.iv.exp(iv(digital_hi)) * (mp.iv.exp(iv(high_k * ln2_error)) - 1),
    )
    exp_error = (1 << high_k) * (
        coefficient_error + remainder_error + evaluation_error
    ) + reconstruction
    exact(date, "native_exp_discrepancy_dollars_exact", exp_error)
    continuous_high_interval = (
        mp.iv.log(iv(100))
        + iv(Fraction(-1, 800))
        + (mp.iv.sqrt(iv(Fraction(3, 1000))) + mp.iv.sqrt(iv(Fraction(9, 2000)))) * iv(radius)
    )
    # The producer rounds continuous_high once before the outer exp. A fresh
    # 130-digit calculation is enclosed by that90-digit construction.
    coupled = validate_transcendental(
        date,
        "coupled_log_to_spot_discrepancy_dollars_exact",
        mp.iv.exp(continuous_high_interval) * (mp.iv.exp(iv(log_error)) - 1),
    )
    stock_error = coupled + exp_error
    exact(date, "spot_discrepancy_dollars_exact", stock_error)
    exact(date, "basket_discrepancy_dollars_exact", stock_error + EPSILON)
    exact(date, "basket_native_averaging_floor_upper_exact", EPSILON)
    shifted_bound = (1 << high_k) * (
        sum((abs(c) * remainder_radius**j for j, c in coefficients.items()), Fraction(0))
        + evaluation_error
    )
    assert shifted_bound < LIMIT and date["exp_final_shift_signed_overflow_excluded"]
    assert 4 * shifted_bound < LIMIT  # Actual basket addition intermediates also fit.
    for name in ("exp_integer_k_times_ln2_floor_error_exact", "exp_final_left_shift_error_exact"):
        exact(date, name, Fraction(0))
    below = stock_error <= Fraction(11, 2000)
    assert date["one_date_component_below_unallocated_headroom"] == below
    assert (
        date["component_comparison_is_not_full_price_certification"]
        and date["first_asset_template_bound_applies_to_all_four_assets"]
    )
    assert date["barrier_boundary_mass"] is date["complete_price_bias_dollars"] is None
    return dict(
        passed=True,
        cutoff_bits=pair["cutoff_bits"],
        date=1,
        assets=4,
        jointly_used_pairs=3,
        independent_scalar_seed_assumption=False,
        all_four_actual_polynomials_reconstructed=True,
        first_asset_SSA_steps_reconciled=len(steps),
        all_asset_SSA_steps_reconciled=sum(len(s) for _, _, s in all_polynomials),
        log_discrepancy_upper_exact=encoded(log_error),
        stock_discrepancy_upper_dollars_exact=encoded(stock_error),
        basket_discrepancy_upper_dollars_exact=encoded(stock_error + EPSILON),
        clipping_inactive_on_good_event=True,
        native_intermediates_and_final_shifts_no_overflow=True,
        one_date_component_below_headroom=below,
        full_price_claim=False,
    )


def audit_tail_and_claims(candidate, certificate):
    delta, cutoff = decoded(candidate["delta_exact"]), candidate["cutoff_bits"]
    probability = {
        "one_pair": 1,
        "B4_date1_three_pairs": 3,
        "B4_all30_pairs": 30,
        "B8_all234_pairs": 234,
    }
    assert candidate["tail_probability_union_upper_exact"] == {
        k: encoded(v * delta) for k, v in probability.items()
    }
    costs = {
        "B4_date1_bad_pair_event_only": 3,
        "B4_all30_pairs_bad_event_only": 30,
        "B8_all234_pairs_bad_event_only": 234,
    }
    assert candidate["tail_payoff_difference_dollars_upper_exact"] == {
        k: encoded(40 * v * delta) for k, v in costs.items()
    }
    identity = "C06_q32_f40_shared_uniform_delta2minus%d" % cutoff
    assert candidate["coupling_id"] == identity
    basket, bad = candidate["claims"]
    assert basket == certificate["claims"]["delta2minus%d_B4_date1_basket" % cutoff]
    assert bad == certificate["claims"]["delta2minus%d_B4_date1_bad_event" % cutoff]
    for claim in (basket, bad):
        assert claim["proved"] and claim["scope"] == dict(case="B4x12", date=1)
        assert (
            claim["coupling_id"] == identity
            and claim["measure"] == "continuous-underlying-uniform-coupling"
        )
    assert basket["kind"] == "basket-absolute-error" and basket["native_exp_and_clipping_included"]
    assert basket["event"] == "First three radial uniforms are at least delta"
    assert basket["upper_exact"] == candidate["B4_date1"]["basket_discrepancy_dollars_exact"]
    assert bad["kind"] == "bad-event-probability" and decoded(bad["upper_exact"]) == 3 * delta
    return dict(
        passed=True,
        cutoff_bits=cutoff,
        shared_radial_uniform_events_only=True,
        probabilities=candidate["tail_probability_union_upper_exact"],
        tail_difference_dollars=candidate["tail_payoff_difference_dollars_upper_exact"],
        difference_support_40_not_80=True,
        claims_hash=hashlib.sha256(
            json.dumps(candidate["claims"], sort_keys=True).encode()
        ).hexdigest(),
        full_path_G2_closed=False,
    )


def audit_global_nooverflow(certificate):
    record = certificate["native_pair_no_overflow_certificate"]
    assert record["all_q32_midpoints"] and record["log_exponent_integer_bounds"] == [-33, -1]
    assert record["normalized_mantissa_raw_bounds"] == [Q, 2 * Q - 1]
    # Every exact midpoint integer lies between128 andQ-128; its msb lies
    # between7 and39. Its normalization shifts left by33..1, so no bit is lost.
    assert (128).bit_length() - 1 == 7 and (Q - 128).bit_length() - 1 == 39
    assert (128 << 33) == Q and ((Q - 128) << 1) < 2 * Q
    for exponent in range(-33, 0):
        low_raw, high_raw = 1 << (40 + exponent), (1 << (41 + exponent)) - 1
        assert Q <= low_raw << (-exponent) <= high_raw << (-exponent) <= 2 * Q - 1
    ln2 = abs(Fraction(certificate["source_bindings"]["B4x12"]["literal_ln2"], Q))
    log_bound = (
        decoded(certificate["log_table_certificate"]["maximum_native_intermediate_magnitude_exact"])
        + 33 * ln2
    )
    exact(record, "logarithm_magnitude_upper_exact", log_bound)
    radius = validate_transcendental(
        record, "radius_magnitude_upper_exact", mp.iv.sqrt(iv(2 * log_bound)) + iv(EPSILON)
    )
    normal = (
        radius * (1 + decoded(certificate["cos_table_certificate"]["total_error_upper_exact"]))
        + EPSILON
    )
    exact(record, "final_normal_magnitude_upper_exact", normal)
    exact(record, "signed_native_real_magnitude_limit_exact", Fraction(LIMIT))
    assert max(normal, radius, 2 * log_bound, 33 * ln2, Fraction(33), Fraction(2)) < LIMIT
    assert record["all_Horner_intermediates_checked"] and record["native_output_overflow_excluded"]
    return dict(
        passed=True,
        all_2pow32_midpoints_covered_analytically=True,
        exact_midpoint_raw_bounds=[128, Q - 128],
        normalized_mantissa_raw_bounds=[Q, 2 * Q - 1],
        exact_normalization_left_shift_amounts=[1, 33],
        all_table_centers_and_addresses_exact=True,
        quarter_turn_and_wrap_exact=True,
        negative_signed_integer_ln2_products_exact=True,
        maximum_normal_magnitude_exact=encoded(normal),
        signed_native_magnitude_limit=LIMIT,
    )


def continuous_contract():
    path = ROOT / "research/advantage_frontier_20260923/barrier_oracle_depth.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    constants = {}
    for node in tree.body:
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
        ):
            try:
                constants[node.targets[0].id] = Fraction(str(ast.literal_eval(node.value)))
            except (ValueError, TypeError, SyntaxError):
                pass
        elif (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Tuple)
        ):
            names = node.targets[0].elts
            if all(isinstance(name, ast.Name) for name in names):
                try:
                    values = ast.literal_eval(node.value)
                    constants.update(
                        (name.id, Fraction(str(value)))
                        for name, value in zip(names, values, strict=True)
                    )
                except (ValueError, TypeError, SyntaxError):
                    pass
    for key, value in dict(
        S0=100, K=100, H=140, T=1, RATE=Fraction(3, 100), SIGMA=Fraction(3, 10), CORR=Fraction(2, 5)
    ).items():
        assert constants[key] == value
    build = next(
        node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "build"
    )
    assignments = {
        node.targets[0].id: ast.unparse(node.value)
        for node in build.body
        if isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and isinstance(node.targets[0], ast.Name)
    }
    assert assignments["alive"] == "g.lt(tree(g, baskets, g.maximum), g.c(H))"
    assert (
        assignments["average"]
        == "g.cmul(tree(g, [s for row in stocks for s in row], g.add), 1 / (na * nt))"
    )
    assert assignments["payoff"] == "g.cmul(g.pos(g.sub(average, g.c(K))), math.exp(-RATE * T))"
    # Strict survival implies every positive basket<140. Their arithmetic
    # average is<140; the strike100 call is<40; positive discount<=1.
    assert constants["H"] - constants["K"] == 40 and constants["RATE"] * constants["T"] >= 0
    assert constants["SIGMA"] ** 2 * Fraction(1, 12) * constants["CORR"] == Fraction(3, 1000)
    assert constants["SIGMA"] ** 2 * Fraction(1, 12) * (1 - constants["CORR"]) == Fraction(9, 2000)
    assert (constants["RATE"] - constants["SIGMA"] ** 2 / 2) * Fraction(1, 12) == Fraction(-1, 800)
    return dict(
        passed=True,
        strict_monitored_barrier=140,
        strike=100,
        discounted_payoff_nonnegative=True,
        discounted_payoff_upper_dollars_exact=[40, 1],
        pathwise_difference_upper_40=True,
        contract_source_sha256=sha(path),
    )


def audit_one_date_bridge(certificate, producer, pi):
    """Reconcile the restricted disagreement contribution, never full price."""
    directory = PROGRAM / "C07_bound_date1_run001"
    bound, summary, prospective = (
        read(directory / name) for name in ("certificate.json", "summary.json", "protocol.json")
    )
    assert (
        summary["passed"]
        and summary["frozen_inputs_unchanged"]
        and summary["historical_receipts_unchanged"]
    )
    assert xml_count(directory / "tests.xml") == prospective["declared_tests"] == 12
    assert prospective["selected_eta_values"] == 1 and prospective["cutoff_bits"] == 20
    assert (
        prospective["bound_forms"] == ["density", "centered_interval_maximum"]
        and not prospective["eta_grid_or_adaptive_search"]
    )
    assert prospective["C06_independent_audit_required_before_adoption"]
    for dependency in prospective["executed_dependencies"]:
        assert (
            sha(ROOT / dependency["original"])
            == sha(directory / dependency["snapshot"])
            == dependency["sha256"]
        )
    expected_paths = {
        "C06_certificate": producer / "certificate.json",
        "eta_claim": producer / "certificate.json",
        "bad_event_claim": producer / "certificate.json",
        "C07_certificate": PROGRAM / "C07_barrier_run002/B4_date1_certificate.json",
        "C07_independent_audit": PROGRAM / "C07_barrier_audit_run001/audit.json",
        "original_builder": ROOT / "research/advantage_frontier_20260923/barrier_oracle_depth.py",
        "accepted_target": ROOT / certificate["source_bindings"]["B4x12"]["target"],
        "digital_support_certificate": ROOT
        / certificate["payoff_support_bindings"]["B4x12"]["certificate"],
        "digital_support_independent_audit": ROOT
        / certificate["payoff_support_bindings"]["B4x12"]["independent_audit"],
    }
    assert set(bound["bindings"]) == set(expected_paths)
    for name, expected_path in expected_paths.items():
        pointer = bound["bindings"][name]
        assert Path(pointer["path"]).resolve() == expected_path.resolve()
        assert pointer["sha256"] == sha(expected_path)
    eta_key, bad_key = "delta2minus20_B4_date1_basket", "delta2minus20_B4_date1_bad_event"
    assert bound["bindings"]["eta_claim"]["claim"] == prospective["eta_claim"] == eta_key
    assert (
        bound["bindings"]["bad_event_claim"]["claim"] == prospective["bad_event_claim"] == bad_key
    )
    eta = decoded(certificate["claims"][eta_key]["upper_exact"])
    bad = decoded(certificate["claims"][bad_key]["upper_exact"])
    exact(bound, "eta_basket_dollars_exact", eta)
    exact(bound, "date1_bad_event_probability_upper_exact", bad)
    exact(bound, "whole_B4_all30_pairs_bad_event_probability_upper_exact", 10 * bad)
    exact(bound, "date1_bad_event_tail_dollars_upper_exact", 40 * bad)
    exact(bound, "whole_B4_all30_pairs_bad_event_tail_dollars_upper_exact", 400 * bad)
    exact(bound, "payoff_difference_cap_dollars_exact", Fraction(40))
    assert bound["date1_and_whole_B4_tails_are_separate_alternatives_not_added"]
    assert bound["scope"] == dict(case="B4x12", date=1, observation_time_exact=[1, 12])
    assert bound["selected_eta_values"] == 1 and bound["selected_cutoff_bits"] == 20
    assert bound["coupling_id"] == certificate["candidates"][0]["coupling_id"]
    assert bound["measure"] == certificate["claims"][eta_key]["measure"]
    domain = bound["domain"]
    assert domain["good_event"] == certificate["claims"][eta_key]["event"]
    assert domain["delta_exact"] == [1, 1 << 20]
    assert domain["used_joint_pairs"] == 3 and domain["used_normal_scalars"] == 5
    assert (
        not domain["finite_normal_outputs_assumed_independent"]
        and domain["native_exp_and_clipping_included"]
    )
    api = bound["barrier_api_certificate"]
    model = api["model"]
    assert model["case"] == "B4x12" and model["assets"] == 4 and model["dates"] == 12
    for key, expected in dict(
        volatility_exact=Fraction(3, 10),
        correlation_exact=Fraction(2, 5),
        spot_dollars_exact=Fraction(100),
        rate_exact=Fraction(3, 100),
        maturity_years_exact=Fraction(1),
        strike_dollars_exact=Fraction(100),
        barrier_dollars_exact=Fraction(140),
    ).items():
        exact(model, key, expected)
    assert model["builder_sha256"] == sha(expected_paths["original_builder"])
    assert Path(model["builder_path"]).resolve() == expected_paths["original_builder"].resolve()
    prior = read(expected_paths["C07_independent_audit"])
    assert prior["passed"] and prior["source_contract"]["builder_sha256"] == model["builder_sha256"]
    assert prior["source_contract"]["common_log_variance_exact"] == [3, 1000]
    target_name = relative(expected_paths["accepted_target"])
    assert read(PROGRAM / "C07_barrier_run002/protocol.json")["frozen_inputs"][target_name] == sha(
        expected_paths["accepted_target"]
    )
    assert api["date"] == 1 and api["observation_time_exact"] == [1, 12]
    exact(api, "common_log_variance_exact", Fraction(3, 1000))
    for name, claim_key, pointer_key in (
        ("eta", eta_key, "eta_claim"),
        ("bad_event_probability", bad_key, "bad_event_claim"),
    ):
        interface = api[name]
        assert interface["artifact"] == bound["bindings"][pointer_key]
        assert interface["upper_exact"] == certificate["claims"][claim_key]["upper_exact"]
        assert (
            interface["coupling_id"] == bound["coupling_id"]
            and interface["theorem_externally_proved"]
        )
        assert not interface["external_theorem_reproved_here"]
    bounds = api["proved_discrepancy_band_bounds"]
    assert bounds["eta_dollars_exact"] == encoded(eta) and bounds["barrier_dollars_exact"] == [
        140,
        1,
    ]
    L = mp.iv.log((iv(140) + iv(eta)) / (iv(140) - iv(eta)))
    sc = mp.iv.sqrt(iv(Fraction(3, 1000)))
    density = L / mp.iv.sqrt(2 * pi * iv(Fraction(3, 1000)))
    d = L / (2 * sc)
    assert 0 < upper(d) < Fraction(1, 1000)
    integral = mp.iv.mpf(0)
    for j in range(32):
        integral += (-1) ** j * d ** (2 * j + 1) / (2**j * math.factorial(j) * (2 * j + 1))
    remainder = d**65 / (2**32 * math.factorial(32) * 65)
    factor = mp.iv.sqrt(2 / pi)
    centered = (integral + mp.iv.mpf([-remainder.b, remainder.b])) * factor
    independent = dict(
        log_length=enclosure(L),
        density=enclosure(density),
        centered_interval_maximum=enclosure(centered),
    )
    charged_L = tuple(decoded(v) for v in bounds["log_length_interval_exact"])
    assert (
        charged_L[0] <= independent["log_length"][0] <= independent["log_length"][1] <= charged_L[1]
    )
    probabilities = {}
    for kind in ("density", "centered_interval_maximum"):
        lo, hi = (decoded(v) for v in bounds[kind]["interval_exact"])
        assert lo <= independent[kind][0] <= independent[kind][1] <= hi
        assert decoded(bounds[kind]["probability_upper_exact"]) == hi
        reference = tuple(decoded(v) for v in bound["independent_numeric_validation"][kind])
        assert reference[0] <= independent[kind][0] <= independent[kind][1] <= reference[1]
        contribution = bound["one_date_barrier_contributions"][kind]
        exact(contribution, "one_date_good_event_band_probability_upper_exact", hi)
        exact(
            contribution,
            "one_date_good_event_payoff_difference_contribution_dollars_upper_exact",
            40 * hi,
        )
        exact(
            contribution,
            "one_date_decision_disagreement_probability_upper_exact",
            min(Fraction(1), hi + bad),
        )
        exact(
            contribution,
            "one_date_disagreement_event_only_payoff_difference_dollars_upper_exact",
            40 * min(Fraction(1), hi + bad),
        )
        assert not contribution["is_full_price_error_bound"]
        probabilities[kind] = hi
        for key, value in contribution.items():
            if key != "is_full_price_error_bound":
                assert summary["one_date_event_contribution_displays"][kind][key] == math.nextafter(
                    float(decoded(value)), math.inf
                )
    assert probabilities["centered_interval_maximum"] <= probabilities["density"]
    exact(
        api,
        "one_date_decision_disagreement_upper_exact",
        min(Fraction(1), probabilities["centered_interval_maximum"] + bad),
    )
    assert (
        not api["gaussian_law_conditioned_on_coupling_good_event"]
        and not api["digital_paired_outputs_claimed_independent_gaussian"]
    )
    for key in (
        "discounted_smooth_payoff_zeta",
        "discounted_tail_dollars",
        "any_contractual_date_band_probability",
        "dollar_bias_upper_exact",
    ):
        assert api[key] is None
    for key in (
        "discounted_smooth_full_Asian_payoff_zeta",
        "any_contractual_date_band_probability",
        "full_path_native_exp_and_clipping_discrepancy",
        "complete_price_error_dollars_upper_exact",
    ):
        assert bound[key] is None
    assert (
        not api["full_G2_certificate"]
        and not api["all_contractual_dates_covered"]
        and not api["second_discount_applied"]
    )
    assert not bound["full_G2_closed"] and not bound["second_discount_applied"]
    assert (
        not bound["adopted_as_complete_financial_error_certificate"]
        and not bound["eta_grid_or_adaptive_radius_search"]
    )
    assert bound["new_financial_price_samples"] == bound["new_financial_gate_replays"] == 0
    assert bound["C06_independent_audit_adoption"] == dict(
        status="required_before_adoption", pointer=None
    )
    return dict(
        passed=True,
        restricted_to_original_date1_decision_disagreement=True,
        independent_pytest_cases_reconciled=12,
        claim_pointers_and_actual_target_model_support_hashes_verified=True,
        eta_basket_dollars_exact=encoded(eta),
        unconditional_band_probability_upper_exact={
            kind: encoded(p) for kind, p in probabilities.items()
        },
        centered_restricted_event_contribution_dollars_upper_exact=encoded(
            40 * (probabilities["centered_interval_maximum"] + bad)
        ),
        date1_bad_event_probability_exact=encoded(bad),
        whole_B4_bad_event_probability_exact=encoded(10 * bad),
        tails_separate_and_not_added=True,
        no_second_discount=True,
        Gaussian_law_not_conditioned_on_good_event=True,
        full_price_error_dollars=None,
        full_G2_closed=False,
        independently_enclosed_numeric_bounds={
            kind: [encoded(v) for v in interval] for kind, interval in independent.items()
        },
    )


def xml_count(path):
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root)
    cases = [
        (case.get("classname"), case.get("name"))
        for suite in suites
        for case in suite.findall("testcase")
    ]
    assert len(cases) == len(set(cases)) == sum(int(suite.get("tests", 0)) for suite in suites)
    assert all(
        int(suite.get(field, 0)) == 0
        for suite in suites
        for field in ("failures", "errors", "skipped")
    )
    return len(cases)


def receipt_inputs(directory):
    manifest_path = Path(directory) / "manifest.json"
    manifest = read(manifest_path)
    files = {relative(manifest_path): sha(manifest_path)}
    for key in ("files", "frozen_inputs"):
        for name, digest in manifest.get(key, {}).items():
            files[name.replace("\\", "/")] = digest
    verify(files)
    return files


def prepare(producer, output):
    producer, output = Path(producer).resolve(), Path(output).resolve()
    producer.relative_to(PROGRAM)
    output.relative_to(PROGRAM)
    assert read(producer / "summary.json")["passed"] and not output.exists()
    frozen = {}
    for directory in (
        producer,
        PROGRAM / "E03_support_run001",
        PROGRAM / "E03_support_audit_run002",
        PROGRAM / "C07_barrier_run002",
        PROGRAM / "C07_barrier_audit_run001",
        PROGRAM / "C07_bound_date1_run001",
    ):
        frozen.update(receipt_inputs(directory))
    own = Path(__file__).resolve()
    frozen[relative(own)] = sha(own)
    verify(frozen)
    output.mkdir()
    shutil.copy2(own, output / "executed_audit_box_muller_pair.py")
    save(
        output / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            local_only=True,
            before_independent_audit=True,
            producer=relative(producer),
            frozen_inputs=frozen,
            interpreter_sha256=sha(sys.executable),
            mpmath_version=mp.__version__,
            interval_decimal_precision=130,
            independent_pi="4*(atan(1/2)+atan(1/3)),240 alternating-series terms per angle",
            cutoff_bits=[20, 24],
            pair_counts=dict(B4x12=30, B8x52=234),
            actual_coefficient_count=800,
            one_date_scope=dict(case="B4x12", date=1, assets=4, joint_pairs=3),
            C07_adoption_interface="C07_bound_date1_run001, delta20 basket and3delta date1 bad-event claims; independent centered/density intervals and restricted disagreement-event dollars; full30delta B4 tail kept separate",
            proof_generator_imported=False,
            actual_gate_or_financial_replays=0,
            new_candidates=0,
            new_pytest_cases=0,
            scope="All actual shared-input pair DAGs;800 literal Taylor coefficients; native signedHornerfloors, exact midpoint normalization/exponent products/quarter turns; radial andangular coupling andHolderbound; allfour original first-datepolynomials/clipping with native range reconstruction andfloors; exact tail/claim interfaces and independentlyaudited nonnegativepayoffs. No fullpath/barriercomposition or fullG2 certification.",
            freeze_rule="Preserve any failure; corrections require versioned code and a fresh receipt",
        ),
    )
    print("Independent C06 joint-pair audit protocol frozen", flush=True)


def run(output):
    output = Path(output).resolve()
    assert not (output / "summary.json").exists()
    protocol = read(output / "protocol.json")
    verify(protocol["frozen_inputs"])
    assert (
        sha(sys.executable) == protocol["interpreter_sha256"]
        and mp.__version__ == protocol["mpmath_version"]
    )
    mp.iv.dps = 130
    pi = independent_pi()
    producer = ROOT / protocol["producer"]
    certificate, summary, prospective = (
        read(producer / name) for name in ("certificate.json", "summary.json", "protocol.json")
    )
    assert summary["passed"] and summary["returncode"] == 0 and summary["frozen_inputs_unchanged"]
    assert xml_count(producer / "pytest.xml") == prospective["declared_tests"] == 26
    assert summary["tests"] == dict(tests=26, failures=0, errors=0, skipped=0)
    assert prospective["before_meaningful_tests_and_certification"] and prospective[
        "cutoff_bits"
    ] == [20, 24]
    assert prospective["pair_counts"] == dict(B4x12=30, B8x52=234) and prospective[
        "scalar_counts"
    ] == dict(B4x12=60, B8x52=468)
    for binding in prospective["executed_dependencies"]:
        assert (
            sha(ROOT / binding["original"])
            == sha(producer / binding["snapshot"])
            == binding["sha256"]
        )
    assert (
        read(producer / "frozen_inputs.json") == read(producer / "manifest.json")["frozen_inputs"]
    )
    assert (
        certificate["uniform_bits"] == 32
        and certificate["fraction_bits"] == 40
        and certificate["native_width"] == 72
    )
    assert (
        certificate["interval_decimal_precision"] == 90
        and certificate["outward_exact_rational_endpoints"]
    )
    assert certificate["unallocated_dollar_headroom_exact"] == [11, 2000]
    assert read(PROGRAM / "E07_schedule_run001/summary.json")["complete_price_assessment"][
        "remaining_dollar_headroom"
    ] == [11, 2000]
    assert [c["cutoff_bits"] for c in certificate["candidates"]] == [20, 24]
    assert set(certificate["claims"]) == {
        "delta2minus%d_B4_date1_%s" % (d, s) for d in (20, 24) for s in ("basket", "bad_event")
    }
    assert not certificate["full_G2_closed"] and not certificate["complete_price_certified"]
    assert (
        certificate["new_financial_gate_replays"]
        == summary["new_financial_gate_replays"]
        == summary["new_quantum_unitary_tests"]
        == 0
    )
    assert all(value is None for value in certificate["unresolved"].values())
    assert set(certificate["unresolved"]) == {
        "full_path_clipping_dollar_bias",
        "full_path_stock_error",
        "barrier_boundary_probability",
        "complete_price_bias_dollars",
        "physical_runtime",
    }
    targets, supports, sources = audit_sources(certificate)
    save(output / "actual_pair_scope_audit.json", sources)
    tables = {}
    for name in ("log", "cos"):
        tables[name] = audit_table(
            name, targets["B4x12"]["tables"][name], certificate[name + "_table_certificate"], pi
        )
        print(
            name,
            tables[name]["coefficients_verified"],
            "independent coefficient intervals PASS",
            flush=True,
        )
    assert sum(table["coefficients_verified"] for table in tables.values()) == 800
    save(output / "independent_table_audit.json", tables)
    contract = continuous_contract()
    save(output / "continuous_support_contract_audit.json", contract)
    global_overflow = audit_global_nooverflow(certificate)
    save(output / "all_Q32_native_nooverflow_audit.json", global_overflow)
    candidates = []
    for candidate, display in zip(certificate["candidates"], summary["candidates"], strict=True):
        pair_report = audit_pair(candidate, certificate, pi)
        date_report = audit_date(
            targets["B4x12"],
            candidate,
            supports["B4x12"],
            certificate["source_bindings"]["B4x12"]["normal_values"],
        )
        tail_report = audit_tail_and_claims(candidate, certificate)
        assert display["cutoff_bits"] == candidate["cutoff_bits"]
        for name, exact_value in (
            (
                "coordinate_discrepancy_display_upper",
                decoded(candidate["coordinate_discrepancy_upper_exact"]),
            ),
            (
                "date1_log_discrepancy_display_upper",
                decoded(candidate["B4_date1"]["log_discrepancy_exact"]),
            ),
            (
                "date1_stock_discrepancy_display_upper_dollars",
                decoded(candidate["B4_date1"]["spot_discrepancy_dollars_exact"]),
            ),
            (
                "date1_basket_discrepancy_display_upper_dollars",
                decoded(candidate["B4_date1"]["basket_discrepancy_dollars_exact"]),
            ),
            (
                "B4_full_bad_pair_tail_display_upper_dollars",
                decoded(
                    candidate["tail_payoff_difference_dollars_upper_exact"][
                        "B4_all30_pairs_bad_event_only"
                    ]
                ),
            ),
        ):
            assert (
                display[name] == math.nextafter(float(exact_value), math.inf)
                and Fraction(display[name]) >= exact_value
            )
        assert (
            display["date1_component_below_headroom"]
            == date_report["one_date_component_below_headroom"]
        )
        report = dict(pair=pair_report, first_date=date_report, tails_and_claims=tail_report)
        save(output / ("delta2minus%d_audit.json" % candidate["cutoff_bits"]), report)
        candidates.append(report)
        print(
            "delta2minus%d" % candidate["cutoff_bits"],
            "joint-pair,allfourfirst-date stocks, tail/claims PASS",
            flush=True,
        )
    assert [c["first_date"]["one_date_component_below_headroom"] for c in candidates] == [
        True,
        False,
    ]
    bridge = audit_one_date_bridge(certificate, producer, pi)
    save(output / "C07_bound_date1_adoption_audit.json", bridge)
    print("C07 actual date1 coupling bridge/adoption interface PASS", flush=True)
    verify(protocol["frozen_inputs"])
    save(
        output / "summary.json",
        dict(
            passed=True,
            local_only=True,
            producer_distinct_pytest_cases_reconciled=26,
            independently_walked_joint_pairs=264,
            actual_coefficient_literals_verified=800,
            candidate_cutoffs=[20, 24],
            candidate_reports=candidates,
            C07_actual_date1_adoption_audit_passed=bridge["passed"],
            C07_bound_date1_distinct_pytest_cases_reconciled=12,
            all_Q32_native_pair_nooverflow=True,
            first_date_actual_stock_graphs_verified=4,
            digital_and_continuous_nonnegative_price_support_below40=True,
            shared_pair_conditioning_preserved=True,
            independent_scalar_seed_assumption=False,
            new_financial_gate_replays=0,
            new_quantum_unitary_tests=0,
            new_candidates=0,
            new_pytest_cases=0,
            full_G2_closed=False,
            complete_price_certified=False,
            physical_runtime_seconds=None,
            remaining=[
                "full-path stock/clipping dollar discrepancy",
                "barrier boundary mass",
                "full smooth payoff and date composition",
            ],
        ),
    )
    finish_manifest(output)
    print("Independent C06 joint-pair and first-date audit PASS", flush=True)


def finish_manifest(output):
    save(
        output / "manifest.json",
        dict(
            files={relative(path): sha(path) for path in output.rglob("*") if path.is_file()},
            frozen_inputs=read(output / "protocol.json")["frozen_inputs"],
            manifest_self_hash_excluded=True,
        ),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "run"))
    parser.add_argument("--producer", type=Path, default=PROGRAM / "C06_pair_run001")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.phase == "prepare":
        prepare(args.producer, args.output)
    else:
        try:
            run(args.output)
        except Exception as failure:
            output = args.output.resolve()
            (output / "failure.txt").write_text(traceback.format_exc(), encoding="utf-8")
            save(
                output / "summary.json",
                dict(
                    passed=False,
                    local_only=True,
                    failure_type=type(failure).__name__,
                    message=str(failure),
                    new_financial_gate_replays=0,
                    new_candidates=0,
                ),
            )
            finish_manifest(output)
            raise
