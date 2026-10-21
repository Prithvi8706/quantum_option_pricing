"""Independent original-pair polar CDF/BV audit; no producer/helper imports.

Only a future root invocation may execute this module. Its kernel independently
reads the immutable SSA, proves exact driver incidence and recomputes outward
log/radius and hybrid inequalities at 130 digits. It has zero fixture credit;
native financial bias, cosine arithmetic, costs and adoption remain open.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter
import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
from importlib import metadata
from importlib.util import cache_from_source
import json
import os
from pathlib import Path
import re
import site
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
PROGRAM = ROOT / "results/limitation_program_20261001"
SOURCE = PROGRAM / "A02_polar_cdf_bv_run002"
OUTPUT = PROGRAM / "A02_polar_cdf_bv_audit_run002"
AUTHOR = RESEARCH / "audit_box_muller_polar_cdf_bv_v2.py"
PRODUCER_AUTHOR = RESEARCH / "experiment_box_muller_polar_cdf_bv_v2.py"
METHOD = RESEARCH / "box_muller_polar_cdf_bv_preflight.json"
METHOD_DOC = RESEARCH / "BOX_MULLER_POLAR_CDF_BV_PREFLIGHT.md"
IMPLEMENTATION = RESEARCH / "box_muller_polar_cdf_bv_implementation_preflight_v2.json"
IMPLEMENTATION_DOC = RESEARCH / "BOX_MULLER_POLAR_CDF_BV_IMPLEMENTATION_PREFLIGHT_V2.md"
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
METHOD_SHA = "6305d69109fd8d73c6d0da1e32880ebfd292e975a66f40ee6fa395c630f7e37d"
METHOD_DOC_SHA = "4bf87dbd3ebd526cd5317faab8c54b01c639ea9d8a5bff907f1f8eb5debf888a"
CPU, ADMISSION, WALL, DIGITS = 180, 150, 600, 130
Q, N, W = 1 << 40, 1 << 32, 72
EPS = Fraction(1, Q)
CASES = {"B4x12": (4, 12, 30), "B8x52": (8, 52, 234)}
SHA_PATTERN = re.compile(r"[0-9a-f]{64}\Z")
PATH_CACHE, ACTUAL_HASH_CACHE, OBSERVED_HASHES = {}, {}, {}
BASE_TREES, BASE_FILES = (), ()
BASE_PREFIX = None
BASE_SITE_LEXICAL = BASE_SITE = None
MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = 24_000, 2 * 1024**3
ROOT_LEAF = "160a18dba2e09b8e1ad2"
ROOT_OWNERS = {
    (
        "results/limitation_program_20261001/A10_coefficient_run001/manifest.json"
    ): "0a732d7f487bca1efd298e7eca4feb2f2d2e83d1958ebb9a14ee9b32a0d78a40",
    (
        "results/limitation_program_20261001/A01_run011/manifest.json"
    ): "6dca072a99497bf4172adba0a6631ecdea9540c56300e3f03f4673667215ef03",
}
ROOT_PINS = {
    (
        "results/limitation_program_20261001/A10_coefficient_run001/B4x12/"
        "min-depth/leaves/160a18dba2e09b8e1ad2.json"
    ): "7d5b9840c1ddd5e6c12bb02cfde591a6be8bdeb18b1de75b93f527d3fde7d5d2",
    (
        "results/limitation_program_20261001/A10_coefficient_run001/B4x12/"
        "min-depth/leaves/160a18dba2e09b8e1ad2.npy"
    ): "bea31e5f32e249a2104885e9eacbd6595788d86dccc222d9384bbede2bd21971",
    (
        "results/limitation_program_20261001/A10_coefficient_run001/B8x52/"
        "min-depth/leaves/160a18dba2e09b8e1ad2.json"
    ): "7d5b9840c1ddd5e6c12bb02cfde591a6be8bdeb18b1de75b93f527d3fde7d5d2",
    (
        "results/limitation_program_20261001/A10_coefficient_run001/B8x52/"
        "min-depth/leaves/160a18dba2e09b8e1ad2.npy"
    ): "bea31e5f32e249a2104885e9eacbd6595788d86dccc222d9384bbede2bd21971",
    (
        "results/limitation_program_20261001/A10_coefficient_run001/"
        "executed_code/nonrestoring_sqrt.py"
    ): "69d97fad09c450a065c025a3ad40904e36e5e30e7d28fa9a2677830704e84fb6",
    (
        "results/limitation_program_20261001/A10_coefficient_run001/"
        "executed_code/prove_nonrestoring_input.py"
    ): "1048339d6ba1fb741a547074da3c730b4680570b3f8eaf88d6d07a79b18cbccf",
    (
        "results/limitation_program_20261001/A10_coefficient_run001/"
        "executed_code/reversible_fixed_point.py"
    ): "52584dee87c84541b9f9e2f070114d7276de3d49d306d33c471214795b729b8b",
    (
        "results/limitation_program_20261001/A10_coefficient_run001/executed_code/reversible.py"
    ): "5105a9cb7eac541843f1a7540e9826543dfd9c5e5617d25614e435040ba8000a",
    (
        "results/limitation_program_20261001/A01_run011/nonrestoring_arithmetic_certificate.json"
    ): "e5958b206fc5c03ae3c9df8792db41a88b557f9ac5210d32308701f07909224b",
    (
        "results/limitation_program_20261001/A01_run011/leaf_audit.json"
    ): "8772b8f48286857fcdd3e17647daeeb18793e6e89db7f5f870635479eab58601",
    (
        "results/limitation_program_20261001/A01_run011/executed_code/reconcile_nonrestoring_v2.py"
    ): "6d0249e66efbf42883d04179aa7181842ccd416f9dc9863e4048edc84c40747e",
    (
        "results/limitation_program_20261001/A11_nonrestoring_leaf_run001/02b69bbccf8176e3b72d.json"
    ): "420dce31acccfcf887141668e14b6c83f2b6edc70447ec35b30a7b0a2e6d0224",
    (
        "results/limitation_program_20261001/A11_nonrestoring_leaf_run001/02b69bbccf8176e3b72d.npy"
    ): "bea31e5f32e249a2104885e9eacbd6595788d86dccc222d9384bbede2bd21971",
}
ORIGINAL_AUTHORS = {
    "experiment_box_muller_polar_cdf_bv.py": (
        "39927c8688b7e990ea64ba7747fda0fada183a5d156f73c3eb36f798a3643dd3"
    ),
    "audit_box_muller_polar_cdf_bv.py": (
        "0cf54f42c37b0044e6543e49ff82e02880c8d2dcda7d2264f3562b48e7225ce7"
    ),
    "BOX_MULLER_POLAR_CDF_BV_IMPLEMENTATION_PREFLIGHT.md": (
        "0ac4452a357bfb21e93acb2abefd0c1c22bcb377515ecef8b2d05b822fed90f5"
    ),
    "box_muller_polar_cdf_bv_implementation_preflight.json": (
        "b07f0344b7688f02a2686ee91985cab45124febb4337fe2bee87e3c20b970b1d"
    ),
}
ORIGINAL_FAILURE = PROGRAM / "A02_polar_cdf_bv_admission_failure_run001"
ORIGINAL_REVIEW = PROGRAM / "A02_polar_cdf_bv_root_review_run001"
ORIGINAL_FAILURE_SHA = "ae3333bd578a4725a542df0c6d80039623bc675fda3f972f15df4124dab9b7a5"
ORIGINAL_REVIEW_SHA = "778b42a5abe95176a19b7d1ffc788a970cdd8e1903c41f33f572ba762cb6f49e"


class BudgetCensoredError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check(started, *, admission=False):
    cpu, wall = time.process_time(), time.monotonic() - started
    if cpu >= (ADMISSION if admission else CPU) or wall >= WALL:
        raise BudgetCensoredError("Fixed independent polar CPU/wall censor")
    return cpu, wall


def start_clock():
    """Charge Windows process startup, including standard-library imports."""
    require(os.name == "nt", "Pinned local Windows runtime")
    require(ctypes.sizeof(ctypes.c_void_p) == 8, "Pinned Win64 runtime")
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.GetCurrentProcess.argtypes = []
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
    kernel.GetProcessTimes.restype = wintypes.BOOL
    fields = [wintypes.FILETIME() for _ in range(4)]
    require(
        kernel.GetProcessTimes(kernel.GetCurrentProcess(), *(ctypes.byref(v) for v in fields)),
        "Actual process creation time unavailable",
    )
    ticks = (fields[0].dwHighDateTime << 32) | fields[0].dwLowDateTime
    age_ns = time.time_ns() - (ticks - 116_444_736_000_000_000) * 100
    require(age_ns >= 0, "Observed actual creation precedes clock observation")
    return time.monotonic() - age_ns / 1_000_000_000


def encode(value):
    value = Fraction(value)
    return [value.numerator, value.denominator]


def rational(value):
    require(
        type(value) is list and len(value) == 2 and all(type(v) is int for v in value),
        "Typed exact rational pair",
    )
    require(value[1] > 0, "Positive rational denominator")
    result = Fraction(*value)
    require(encode(result) == value, "Canonical reduced rational")
    return result


def same(left, right, message):
    require(
        json.dumps(left, sort_keys=True, separators=(",", ":"), allow_nan=False)
        == json.dumps(right, sort_keys=True, separators=(",", ":"), allow_nan=False),
        message,
    )


def unsigned_word(value):
    require(type(value) is int and 0 <= value < 1 << W, "Canonical unsigned72 constant word")
    return value - (1 << W) if value >= 1 << (W - 1) else value


def signed_coefficient(value):
    require(
        type(value) is int and -(1 << 71) <= value < 1 << 71,
        "Canonical signed72 coefficient integer",
    )
    return value


def nearest_fraction(value):
    value = Fraction(value)
    quotient, remainder = divmod(value.numerator, value.denominator)
    return quotient + int(
        2 * remainder > value.denominator
        or (2 * remainder == value.denominator and quotient % 2 != 0)
    )


class GraphAudit:
    """Own backward traversal on actual SSA; never constructs or evaluates it."""

    def __init__(self, target, started):
        self.target, self.started, self.nodes, self.ancestor_cache = target, started, {}, {}
        require((target["width"], target["fraction_bits"]) == (72, 40), "Native W72/F40")
        arities = {
            "input": 0,
            "const": 0,
            "add": 2,
            "sub": 2,
            "mul": 2,
            "cmul": 1,
            "lt": 2,
            "select": 3,
            "positive": 1,
            "msb": 1,
            "bits": 1,
            "shift": 2,
            "sqrt": 1,
            "lookup": 1,
        }
        next_value = 0
        for row in target["nodes"]:
            check(started)
            op, args, out, params = (row[k] for k in ("op", "args", "out", "params"))
            require(
                op in arities and type(args) is list and len(args) == arities[op], "Typed arity"
            )
            require(type(out) is list and type(params) is dict and out, "Typed node shape")
            require(all(type(v) is int and v in self.nodes for v in args), "Topological dependency")
            require(
                out == list(range(next_value, next_value + len(out))),
                "Exact contiguous output slots",
            )
            require(all(type(v) is int for v in out), "Typed SSA identities")
            next_value += len(out)
            require(op == "lookup" or len(out) == 1, "Single output native primitive")
            if op == "const":
                require(set(params) == {"value"}, "Exact constant fields")
                unsigned_word(params["value"])
            elif op == "cmul":
                require(set(params) == {"c"}, "Exact coefficient fields")
                signed_coefficient(params["c"])
            elif op == "bits":
                require(
                    set(params) == {"shift", "width", "signed"}
                    and type(params["shift"]) is int
                    and type(params["width"]) is int
                    and 1 <= params["width"] <= 72
                    and type(params["signed"]) is bool,
                    "Exact bit-extraction fields",
                )
            elif op == "lookup":
                require(
                    set(params) == {"table", "bits"} and type(params["bits"]) is int,
                    "Exact lookup fields",
                )
                table = target["tables"][params["table"]]
                require(
                    len(table) == 1 << params["bits"]
                    and all(len(entry) == len(out) for entry in table),
                    "Complete table shape",
                )
                for entry in table:
                    for coefficient in entry:
                        signed_coefficient(coefficient)
            elif op == "input":
                require(set(params) == {"name", "bits", "preparation"}, "Exact input fields")
            else:
                require(params == {}, "No undeclared arithmetic parameters")
            for value in out:
                self.nodes[value] = row

    def node(self, value, kind=None, params=None):
        check(self.started)
        require(type(value) is int and value in self.nodes, "Actual SSA identity")
        row = self.nodes[value]
        require(kind is None or row["op"] == kind, "Expected native operation")
        if params is not None:
            same(row["params"], params, "Exact native operation parameters")
        return row

    def constant(self, value, expected=None):
        result = unsigned_word(self.node(value, "const")["params"]["value"])
        require(expected is None or result == expected, "Actual decoded constant")
        return result

    def ancestors(self, value):
        if value not in self.ancestor_cache:
            pending, values = [value], set()
            while pending:
                check(self.started)
                current = pending.pop()
                if current not in values:
                    values.add(current)
                    pending.extend(self.node(current)["args"])
            self.ancestor_cache[value] = values
        return self.ancestor_cache[value]

    def clamp(self, value, low=None, high=None):
        topflag, middle, upper = self.node(value, "select")["args"]
        require(self.node(topflag, "lt")["args"] == [middle, upper], "Exact upper clamp")
        bottomflag, lower, original = self.node(middle, "select")["args"]
        require(self.node(bottomflag, "lt")["args"] == [original, lower], "Exact lower clamp")
        require(self.constant(lower, low) < self.constant(upper, high), "Ordered clamp literals")
        return original

    def midpoint(self, value, input_value):
        args = self.node(value, "add")["args"]
        shifted = [v for v in args if self.node(v)["op"] == "bits"]
        require(len(shifted) == 1, "One midpoint conversion")
        require(
            self.node(shifted[0], "bits", {"shift": -8, "width": 72, "signed": False})["args"]
            == [input_value],
            "Exact q32 to f40 conversion",
        )
        self.constant(next(v for v in args if v != shifted[0]), 128)

    def interpolation(self, result, table_name, input_value):
        bins, degree, lower, bits = (32, 8, Q, 5) if table_name == "log" else (64, 7, 0, 6)
        candidates = {
            tuple(self.node(v)["out"])
            for v in self.ancestors(result)
            if self.node(v)["op"] == "lookup" and self.node(v)["params"]["table"] == table_name
        }
        require(len(candidates) == 1, "One table supplies every Horner coefficient")
        coefficients = next(iter(candidates))
        require(len(coefficients) == degree + 1, "All actual polynomial coefficients")
        address = self.node(coefficients[0], "lookup", {"table": table_name, "bits": bits})["args"][
            0
        ]
        bounded = self.node(address, "bits", {"shift": 40 - bits, "width": bits, "signed": False})[
            "args"
        ][0]
        if lower:
            bounded, literal = self.node(bounded, "sub")["args"]
            self.constant(literal, lower)
        require(
            self.clamp(bounded, lower, lower + Q - 1) == input_value, "Interpolation input binding"
        )
        current, local = result, None
        for coefficient in coefficients[:-1]:
            args = self.node(current, "add")["args"]
            require(coefficient in args, "Horner coefficient order")
            factors = self.node(next(v for v in args if v != coefficient), "mul")["args"]
            if local is None:
                possible = [v for v in factors if self.node(v)["op"] == "sub"]
                require(len(possible) == 1, "One local variable in Horner")
                local = possible[0]
            require(local in factors, "Every Horner product uses same local variable")
            current = next(v for v in factors if v != local)
        require(current == coefficients[-1], "Horner terminal coefficient")
        actual, center = self.node(local, "sub")["args"]
        require(actual == bounded, "Local variable uses bounded argument")
        args = self.node(center, "add")["args"]
        shifted = [v for v in args if self.node(v)["op"] == "bits"]
        require(len(shifted) == 1, "Exact local center shift")
        require(
            self.node(shifted[0], "bits", {"shift": bits - 40, "width": 72, "signed": False})[
                "args"
            ]
            == [address],
            "Local center derives from same address",
        )
        self.constant(next(v for v in args if v != shifted[0]), lower + Q // (2 * bins))
        return dict(
            output=result,
            input=input_value,
            address=address,
            local=local,
            lookup_outputs=list(coefficients),
            floors=degree,
        )

    def joint_pair(self, first, second, input_u, input_v, ln2):
        products = [self.node(v, "mul")["args"] for v in (first, second)]
        shared = set(products[0]) & set(products[1])
        require(len(shared) == 1, "Actual pair shares one radius")
        radius = next(iter(shared))
        positive = self.node(radius, "sqrt")["args"][0]
        product = self.node(positive, "positive")["args"][0]
        logarithm = self.node(product, "cmul", {"c": -2 * Q})["args"][0]
        addends = self.node(logarithm, "add")["args"]
        exponent_terms = [v for v in addends if self.node(v)["op"] == "cmul"]
        require(len(exponent_terms) == 1, "Unique integer exponent literal product")
        term = exponent_terms[0]
        scaled = self.node(term, "cmul", {"c": ln2})["args"][0]
        exponent = self.node(scaled, "bits", {"shift": -40, "width": 72, "signed": False})["args"][
            0
        ]
        top, f = self.node(exponent, "sub")["args"]
        self.constant(f, 40)
        safe = self.node(top, "msb")["args"][0]
        flag, tiny, midpoint_u = self.node(safe, "select")["args"]
        self.constant(tiny, 1)
        require(self.node(flag, "lt")["args"] == [midpoint_u, tiny], "Actual positive-input guard")
        self.midpoint(midpoint_u, input_u)
        polynomial = next(v for v in addends if v != term)
        lookups = {
            tuple(self.node(v)["out"])
            for v in self.ancestors(polynomial)
            if self.node(v)["op"] == "lookup"
        }
        require(len(lookups) == 1, "Unique original log lookup")
        address = self.node(next(iter(lookups))[0])["args"][0]
        shifted = self.node(address)["args"][0]
        bounded = self.node(shifted, "sub")["args"][0]
        mantissa = self.clamp(bounded, Q, 2 * Q - 1)
        u, negated = self.node(mantissa, "shift")["args"]
        require(u == safe, "Same positive midpoint is normalized")
        zero, same_exponent = self.node(negated, "sub")["args"]
        self.constant(zero, 0)
        require(same_exponent == exponent, "Exact normalization exponent")
        log_scope = self.interpolation(polynomial, "log", mantissa)
        cosines = [next(v for v in args if v != radius) for args in products]
        turns = []
        for cosine in cosines:
            lookups = {
                tuple(self.node(v)["out"])
                for v in self.ancestors(cosine)
                if self.node(v)["op"] == "lookup"
            }
            require(len(lookups) == 1, "Unique original cosine lookup")
            address = self.node(next(iter(lookups))[0])["args"][0]
            bounded = self.node(address)["args"][0]
            turns.append(self.clamp(bounded, 0, Q - 1))
        midpoint_v, wrapped = turns
        self.midpoint(midpoint_v, input_v)
        total = self.node(wrapped, "bits", {"shift": 0, "width": 40, "signed": False})["args"][0]
        args = self.node(total, "add")["args"]
        require(midpoint_v in args, "Both angles derive from same midpoint")
        self.constant(next(v for v in args if v != midpoint_v), 3 * Q // 4)
        scopes = [self.interpolation(v, "cos", a) for v, a in zip(cosines, turns, strict=True)]
        dependencies = {
            v
            for root in (first, second)
            for v in self.ancestors(root)
            if self.node(v)["op"] == "input"
        }
        require(dependencies == {input_u, input_v}, "Exactly two independent pair input words")
        return dict(
            normal_values=[first, second],
            raw_uniform_values=[input_u, input_v],
            radius=radius,
            log=log_scope,
            cosines=scopes,
            original_shared_pair_preserved=True,
        )

    def sum_terms(self, value, stops):
        pending, result = [value], Counter()
        while pending:
            check(self.started)
            current = pending.pop()
            if current in stops:
                result[current] += 1
            else:
                pending.extend(self.node(current, "add")["args"])
        return result


def financial_incidence(graph, normals, assets, dates, pair_count):
    """Recover linear atoms first, then infer every stock's date and asset."""
    indices = {value: index for index, value in enumerate(normals)}
    require(len(indices) == dates * (assets + 1), "Distinct complete original normals")
    require(set(graph.target["outputs"]) == {"Y"}, "Original one financial output")
    alive, payoff, zero = graph.node(graph.target["outputs"]["Y"], "select")["args"]
    graph.constant(zero, 0)
    discount = graph.node(payoff, "cmul")
    require(discount["params"]["c"] > 0, "Positive actual discount")
    difference = graph.node(discount["args"][0], "positive")["args"][0]
    average, strike = graph.node(difference, "sub")["args"]
    graph.constant(strike, 100 * Q)
    average_node = graph.node(average, "cmul", {"c": nearest_fraction(Fraction(Q, assets * dates))})
    pending, stocks = [average_node["args"][0]], set()
    while pending:
        value = pending.pop()
        if graph.node(value)["op"] == "shift":
            stocks.add(value)
        else:
            pending.extend(graph.node(value, "add")["args"])
    require(
        len(stocks) == assets * dates
        and graph.sum_terms(average_node["args"][0], stocks) == Counter({v: 1 for v in stocks}),
        "Every original stock appears once in arithmetic average",
    )
    memo = {}

    def atoms(value):
        check(graph.started)
        if value not in memo:
            row = graph.node(value)
            if row["op"] == "add":
                result = Counter()
                for child in row["args"]:
                    result.update(atoms(child))
            elif row["op"] == "const":
                result = Counter({("constant", graph.constant(value)): 1})
            else:
                row = graph.node(value, "cmul")
                require(
                    row["args"][0] in indices and row["params"]["c"] > 0,
                    "Raw prefix is positive literal-scaled original driver",
                )
                result = Counter({("normal", indices[row["args"][0]], row["params"]["c"]): 1})
            memo[value] = result
        return memo[value]

    matrix, witnesses, constants_sets = {}, [], [set() for _ in range(5)]
    common, idio, initial, drift, clamps = constants_sets
    for stock in sorted(stocks):
        polynomial, exponent = graph.node(stock, "shift")["args"]
        graph.node(polynomial, "add")
        scaled = graph.node(exponent, "bits", {"shift": 40, "width": 72, "signed": True})["args"][0]
        clipped = graph.node(scaled, "cmul")["args"][0]
        original = graph.clamp(clipped)
        upper = graph.node(clipped)["args"][2]
        lower = graph.node(graph.node(clipped)["args"][1])["args"][1]
        clamps.add((graph.constant(lower), graph.constant(upper)))
        linear, literal_counts = Counter(), Counter()
        for token, count in atoms(original).items():
            if token[0] == "constant":
                literal_counts[token[1]] += count
            else:
                linear[token[1]] += count
                (common if token[1] % (assets + 1) == 0 else idio).add(token[2])
        require(
            linear and all(v == 1 for v in linear.values()), "No driver duplication in raw prefix"
        )
        asset_roles = {v % (assets + 1) for v in linear if v % (assets + 1)}
        require(len(asset_roles) == 1, "One asset role in each stock")
        asset, date = next(iter(asset_roles)) - 1, max(v // (assets + 1) for v in linear)
        wanted = Counter(
            {t * (assets + 1) + role: 1 for t in range(date + 1) for role in (0, asset + 1)}
        )
        require(
            0 <= date < dates and linear == wanted and (asset, date) not in matrix,
            "Complete exact unreset cumulative prefix",
        )
        matrix[asset, date] = stock
        positive = [v for v in literal_counts if v > 0]
        negative = [v for v in literal_counts if v < 0]
        require(
            len(positive) == len(negative) == 1
            and len(literal_counts) == 2
            and literal_counts[positive[0]] == 1
            and literal_counts[negative[0]] == date + 1,
            "One initial log and one fixed drift per increment",
        )
        initial.add(positive[0])
        drift.add(negative[0])
        witnesses.append(
            dict(
                stock=stock,
                raw_log=original,
                asset=asset,
                date=date,
                original_normal_indices=sorted(linear),
                every_driver_multiplicity=1,
                constants=[[v, n] for v, n in sorted(literal_counts.items())],
            )
        )
    require(
        set(matrix) == {(i, j) for i in range(assets) for j in range(dates)}
        and all(len(values) == 1 for values in constants_sets),
        "Complete role matrix and literal inventories",
    )
    maximum, barrier = graph.node(alive, "lt")["args"]
    graph.constant(barrier, 140 * Q)
    pending, baskets = [maximum], Counter()
    while pending:
        check(graph.started)
        value = pending.pop()
        if graph.node(value)["op"] == "cmul":
            baskets[value] += 1
        else:
            flag, high, low = graph.node(value, "select")["args"]
            require(graph.node(flag, "lt")["args"] == [low, high], "Actual maximum selection")
            pending.extend((low, high))
    require(
        len(baskets) == dates and all(v == 1 for v in baskets.values()),
        "All monitored baskets once",
    )
    basket_witnesses, covered_dates = [], set()
    for basket in sorted(baskets):
        row = graph.node(basket, "cmul", {"c": Q // assets})
        terms = graph.sum_terms(row["args"][0], stocks)
        matching = [
            date
            for date in range(dates)
            if terms == Counter({matrix[asset, date]: 1 for asset in range(assets)})
        ]
        require(
            len(matching) == 1 and matching[0] not in covered_dates,
            "Whole same-date arithmetic basket",
        )
        covered_dates.add(matching[0])
        basket_witnesses.append(dict(basket=basket, date=matching[0], stocks=sorted(terms)))
    roles = []
    for pair in range(pair_count):
        check(graph.started)
        scalar = [2 * pair, 2 * pair + 1]
        locations = [dict(date=v // (assets + 1), role=v % (assets + 1)) for v in scalar]
        a, b = locations
        if a["role"] == 0:
            require(b == {"date": a["date"], "role": 1}, "Common-first-idio pair")
            kind = "same_date_common_first_idio"
        elif b["role"] == 0:
            require(a["role"] == assets and b["date"] == a["date"] + 1, "Cross-date pair")
            kind = "cross_date_last_idio_common"
        else:
            require(
                a["date"] == b["date"] and b["role"] == a["role"] + 1, "Distinct same-date idios"
            )
            kind = "same_date_distinct_idios"
        incidence = []
        for asset in range(assets):
            for date in range(dates):
                check(graph.started)
                active = [v["date"] <= date and v["role"] in (0, asset + 1) for v in locations]
                require(
                    not all(active) or any(v["role"] == 0 for v in locations),
                    "Only common+idio can both affect stock",
                )
                square = Fraction(9, 100 * dates) * sum(
                    (
                        Fraction(2, 5) if v["role"] == 0 else Fraction(3, 5)
                        for v, used in zip(locations, active, strict=True)
                        if used
                    ),
                    Fraction(0),
                )
                require(square <= Fraction(9, 100 * dates), "Ideal reference pair coefficient norm")
                incidence.append(
                    dict(asset=asset, date=date, active=active, ideal_squared_norm=encode(square))
                )
        roles.append(
            dict(
                pair=pair,
                scalar_indices=scalar,
                roles=locations,
                kind=kind,
                stock_prefix_incidence=incidence,
            )
        )
    return dict(
        assets=assets,
        dates=dates,
        pairs=pair_count,
        prefix_witnesses=witnesses,
        baskets=basket_witnesses,
        actual_common_literal=next(iter(common)),
        actual_idio_literal=next(iter(idio)),
        actual_initial_literal=next(iter(initial)),
        actual_drift_literal=next(iter(drift)),
        actual_clamps=list(next(iter(clamps))),
        native_discount_literal=discount["params"]["c"],
        actual_pair_roles=roles,
        ideal_maximum_squared_norm=encode(Fraction(9, 100 * dates)),
        native_literal_coefficients_equal_ideal_claimed=False,
    )


def outward(mp, value):
    value = Fraction(value)
    return mp.iv.mpf(value.numerator) / value.denominator


def endpoints(value):
    result = []
    for sign, mantissa, exponent, bitcount in value._mpi_:
        require(
            type(mantissa) is int and type(exponent) is int and bitcount >= 0,
            "Finite outward mpmath endpoint",
        )
        result.append(Fraction((-1) ** sign * mantissa) * Fraction(2) ** exponent)
    require(len(result) == 2 and result[0] <= result[1], "Ordered exact outward endpoints")
    return tuple(result)


def log_certificate(mp, rows, ln2, started):
    radius = Fraction(1, 64)
    records, row_errors, maximum = [], [], Fraction(0)
    for index, row in enumerate(rows):
        center = Fraction(64 + 2 * index + 1, 64)
        errors = []
        for degree, raw in enumerate(row):
            check(started)
            signed_coefficient(raw)
            truth = (
                endpoints(mp.iv.log(outward(mp, center)))
                if degree == 0
                else (Fraction((-1) ** (degree - 1), degree) / center**degree,) * 2
            )
            error = max(abs(Fraction(raw, Q) - v) for v in truth)
            require(error <= EPS / 2, "Actual log literal meets nearest allowance")
            errors.append(error)
            records.append(
                dict(
                    row=index,
                    degree=degree,
                    raw=raw,
                    exact_coefficient_enclosure=[encode(v) for v in truth],
                    literal_error_upper=encode(error),
                )
            )
        row_errors.append(sum((e * radius**j for j, e in enumerate(errors)), Fraction(0)))
        bound = abs(Fraction(row[-1], Q))
        maximum = max(maximum, bound)
        for raw in reversed(row[:-1]):
            product = bound * radius + EPS
            require(bound * radius * Q * Q < 1 << 143, "Full signed144 Horner product")
            bound = abs(Fraction(raw, Q)) + product
            maximum = max(maximum, product, bound)
    require(len(records) == 288 and maximum < 1 << 31, "All288 actual literals and stored72 bounds")
    remainder = radius**9 / 9
    coefficients = max(row_errors)
    floors = sum((EPS * radius**j for j in range(8)), Fraction(0))
    table_error = remainder + coefficients + floors
    true_ln2 = endpoints(mp.iv.log(outward(mp, 2)))
    ln_error = max(abs(Fraction(ln2, Q) - v) for v in true_ln2)
    require(ln_error <= EPS / 2, "Actual ln2 nearest allowance")
    total_log_error = table_error + 33 * ln_error
    root_argument = 66 * true_ln2[1] + 2 * total_log_error
    B = endpoints(mp.iv.sqrt(outward(mp, root_argument)))[1]
    require(
        root_argument * Q < 1 << 46
        and B < 1 << 31
        and 2 * (33 * Fraction(abs(ln2), Q) + maximum) < 1 << 31,
        "Actual unsigned46 root and all signed72 arithmetic guards",
    )
    exponent_rows, covered = [], []
    for exponent in range(-33, 0):
        check(started)
        lower = max(0, -(-(2 ** (40 + exponent) - 128) // 256))
        upper = min(N - 1, (2 ** (41 + exponent) - 1 - 128) // 256)
        require(0 <= lower <= upper < N, "Every occupied exact midpoint exponent class")
        first, last = (2 * lower + 1) * 128, (2 * upper + 1) * 128
        require(
            first.bit_length() - 1 - 40 == exponent and last.bit_length() - 1 - 40 == exponent,
            "Exact exponent classification",
        )
        mlo, mhi = first << (-exponent), last << (-exponent)
        require(
            Q <= mlo <= mhi < 2 * Q and 33 * ln2 < 1 << 71,
            "Exact normalization and integer-ln2 word bounds",
        )
        exponent_rows.append(
            dict(
                exponent=exponent,
                uniform_integer_bounds=[lower, upper],
                mantissa_raw_bounds=[mlo, mhi],
                left_shift=-exponent,
            )
        )
        covered.append((lower, upper))
    require(
        covered[0][0] == 0
        and covered[-1][1] == N - 1
        and all(a[1] + 1 == b[0] for a, b in zip(covered, covered[1:])),
        "Complete q32 exponent union",
    )
    bins = []
    for index in range(32):
        left, right = Q + index * (Q // 32), Q + (index + 1) * (Q // 32) - 1
        center = Q + (2 * index + 1) * (Q // 64)
        require(
            (left - Q) >> 35 == index == (right - Q) >> 35
            and (left - center, right - center) == (-Q // 64, Q // 64 - 1),
            "Exact32 address/center/local intervals",
        )
        bins.append(
            dict(
                row=index,
                mantissa_raw_bounds=[left, right],
                center_raw=center,
                local_raw_bounds=[left - center, right - center],
            )
        )
    eta = 2 * total_log_error + 2 * EPS * B + EPS**2
    D = min(Fraction(1), Fraction(1, 2 * N) + eta / 2)
    return (
        dict(
            coefficient_checks=records,
            coefficient_count=288,
            log_table_remainder_upper=encode(remainder),
            log_table_literal_rounding_upper=encode(coefficients),
            log_table_floor_upper=encode(floors),
            log_table_error_upper=encode(table_error),
            log_Horner_maximum_magnitude=encode(maximum),
            ln2_literal=ln2,
            ln2_true_enclosure=[encode(v) for v in true_ln2],
            ln2_literal_error_upper=encode(ln_error),
            log_error_all_midpoints_upper=encode(total_log_error),
            root_argument_upper=encode(root_argument),
            internal_radius_upper=encode(B),
            square_error_eta_upper=encode(eta),
            squared_radius_KS_upper=encode(D),
            exponent_class_count=33,
            exact_exponent_classes=exponent_rows,
            normalization_bin_count=32,
            exact_normalization_bins=bins,
            native_map_monotonicity_used=False,
            radial_Holder_or_cutoff_used=False,
            internal_radius_not_final_normal_norm=True,
        ),
        B,
        D,
    )


def source_convention(started):
    paths = {
        "contract": ROOT / "research/advantage_frontier_20260923/barrier_oracle_depth.py",
        "sampler": ROOT / "research/controlled_source_completion/finance.py",
        "semantics": ROOT / "research/controlled_source_completion/ir.py",
    }
    trees = {
        name: ast.parse(read_bytes(path, started).decode("utf-8"), filename=str(path))
        for name, path in paths.items()
    }
    parameters = [
        node
        for node in trees["contract"].body
        if isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and isinstance(node.targets[0], ast.Tuple)
        and [getattr(v, "id", None) for v in node.targets[0].elts]
        == ["SIGMA", "CORR", "S0", "RATE", "T", "K", "H"]
    ]
    require(
        len(parameters) == 1 and all(isinstance(v, ast.Constant) for v in parameters[0].value.elts),
        "One literal original contract declaration",
    )
    values = [Fraction(str(v.value)) for v in parameters[0].value.elts]
    expected = [[3, 10], [2, 5], [100, 1], [3, 100], [1, 1], [100, 1], [140, 1]]
    same([encode(v) for v in values], expected, "Exact ideal reference economics")
    functions = {
        node.name: node for node in trees["contract"].body if isinstance(node, ast.FunctionDef)
    }
    nodes = {ast.dump(node, include_attributes=False) for node in ast.walk(functions["build"])}
    expressions = (
        "nt * (na + 1)",
        "T / nt",
        "zs[j * (na + 1)]",
        "zs[j * (na + 1) + 1 + i]",
        "SIGMA * math.sqrt(dt * CORR)",
        "SIGMA * math.sqrt(dt * (1 - CORR))",
        "g.lt(tree(g, baskets, g.maximum), g.c(H))",
        "g.cmul(tree(g, [s for row in stocks for s in row], g.add), 1 / (na * nt))",
        "g.cmul(g.pos(g.sub(average, g.c(K))), math.exp(-RATE * T))",
        "g.select(alive, payoff, g.c(0))",
    )
    witnesses = []
    for expression in expressions:
        check(started)
        parsed = ast.dump(ast.parse(expression, mode="eval").body, include_attributes=False)
        require(parsed in nodes, "Original source financial role/formula witness")
        witnesses.append(dict(expression=expression, actual_AST=parsed))
    samplers = [
        node
        for node in trees["sampler"].body
        if isinstance(node, ast.FunctionDef) and node.name == "normals_graph"
    ]
    require(len(samplers) == 1, "One original sampler function")
    nodes = {ast.dump(node, include_attributes=False) for node in ast.walk(samplers[0])}
    for expression in (
        "g.input('uniform_%d' % (2*j), q)",
        "g.input('uniform_%d' % (2*j+1), q)",
        "g.sqrt(g.cmul(g.log(u), -2))",
        "g.mul(radius, g.cos_unit(v))",
        "g.mul(radius, g.cos_unit(angle2))",
    ):
        parsed = ast.dump(ast.parse(expression, mode="eval").body, include_attributes=False)
        require(parsed in nodes, "Original sampler source formula witness")
        witnesses.append(dict(expression=expression, actual_AST=parsed))
    root_expression = "math.isqrt(raw[0] << f)"
    root_node = ast.dump(ast.parse(root_expression, mode="eval").body, include_attributes=False)
    require(
        root_node
        in {ast.dump(node, include_attributes=False) for node in ast.walk(trees["semantics"])},
        "Original integer floor-root evaluator semantics",
    )
    return dict(
        priors=expected,
        AST_witnesses=witnesses,
        actual_root_expression=root_expression,
        ideal_reference_is_exact_unclipped=True,
        native_floor_and_clamp_finance_equivalence_claimed=False,
    )


def source_inventory(started):
    original = read_json(PROGRAM / "C06_pair_run001/certificate.json", started)
    archived = read_json(PROGRAM / "C06_pair_audit_run001/actual_pair_scope_audit.json", started)
    report, table, ln2 = {}, None, None
    roots = independent_root_semantics(started)
    for case, (assets, dates, pairs) in CASES.items():
        check(started, admission=True)
        route = PROGRAM / "A10_coefficient_run001" / case / "min-depth"
        target, native = (
            read_json(route / "target.json", started),
            read_json(route / "source.json", started),
        )
        graph = GraphAudit(target, started)
        saved = original["source_bindings"][case]
        require(ROOT / saved["target"] == route / "target.json", "Frozen original target route")
        inputs = [node for node in target["nodes"] if node["op"] == "input"]
        require(
            len(inputs) == 2 * pairs == dates * (assets + 1), "Complete q32 pair input inventory"
        )
        for index, node in enumerate(inputs):
            same(
                node["params"],
                {"name": "uniform_" + str(index), "bits": 32, "preparation": "uniform"},
                "Every independent q32 input role",
            )
        same(native["inputs"], inputs, "Native source input binding")
        same(native["outputs"], target["outputs"], "Native source output binding")
        require((native["word_width"], native["fraction_bits"]) == (72, 40), "Native source ABI")
        operations = [node for node in target["nodes"] if node["op"] != "input"]
        require(
            len(operations) == len(native["forward_calls"]), "Complete actual native call count"
        )
        for operation, call in zip(operations, native["forward_calls"], strict=True):
            check(started)
            same(
                [operation["args"], operation["out"]],
                [call["args"], call["out"]],
                "Every native call maps actual SSA arguments and outputs",
            )
            require(
                call["argument_copy_cx"] == 2 * len(operation["args"]) * W,
                "All full72 argument copies remain paid",
            )
        current_table = target["tables"]["log"]
        require(
            len(current_table) == 32 and all(len(row) == 9 for row in current_table),
            "Frozen log32 degree8",
        )
        current_ln2 = signed_coefficient(saved["literal_ln2"])
        require(0 < current_ln2 < Q, "Actual positive ln2 coefficient")
        if table is None:
            table, ln2 = current_table, current_ln2
        same(current_table, table, "Both original targets have same log literals")
        require(current_ln2 == ln2, "Both original targets share actual ln2")
        normals = saved["normal_values"]
        require(
            len(normals) == 2 * pairs and len(set(normals)) == len(normals),
            "All distinct pair normal roots",
        )
        scopes = [
            graph.joint_pair(
                normals[2 * p],
                normals[2 * p + 1],
                inputs[2 * p]["out"][0],
                inputs[2 * p + 1]["out"][0],
                ln2,
            )
            for p in range(pairs)
        ]
        same(
            scopes,
            archived[case]["independently_walked_pair_scopes"],
            "Own walk agrees with independent original scopes",
        )
        calls_by_output = {tuple(call["out"]): call for call in native["forward_calls"]}
        root_calls = []
        for scope in scopes:
            check(started)
            call = calls_by_output[(scope["radius"],)]
            require(
                call["leaf"] == ROOT_LEAF
                and call["args"] == graph.node(scope["radius"], "sqrt")["args"]
                and call["argument_copy_cx"] == 144,
                "Actual root full72 mapping and both argument copies",
            )
            root_calls.append(call)
        report[case] = dict(
            joint_pair_scopes=scopes,
            source_call_count=len(operations),
            financial_roles=financial_incidence(graph, normals, assets, dates, pairs),
            actual_root_descriptor=roots["actual_descriptors"][case],
            actual_root_calls=root_calls,
        )
    return (
        dict(convention=source_convention(started), native_root_prior=roots, cases=report),
        table,
        ln2,
    )


def compare_log_record(saved, own, started):
    """Validate primary90-digit enclosures with own130-digit computations."""
    require(
        saved["coefficient_count"] == 288 and len(saved["coefficient_checks"]) == 288,
        "Exactly288 primary log checks",
    )
    primary_row_errors = [[] for _ in range(32)]
    for actual, replay in zip(saved["coefficient_checks"], own["coefficient_checks"], strict=True):
        check(started)
        same(
            [actual[k] for k in ("row", "degree", "raw")],
            [replay[k] for k in ("row", "degree", "raw")],
            "Every original literal identity",
        )
        lower, upper = [rational(v) for v in actual["exact_coefficient_enclosure"]]
        own_lower, own_upper = [rational(v) for v in replay["exact_coefficient_enclosure"]]
        require(
            lower <= own_lower <= own_upper <= upper,
            "Primary coefficient enclosure contains own interval",
        )
        error = max(
            abs(Fraction(actual["raw"], Q) - lower), abs(Fraction(actual["raw"], Q) - upper)
        )
        require(
            rational(actual["literal_error_upper"]) == error and error <= EPS / 2,
            "Primary per-literal nearest allowance correctly reconstructed",
        )
        primary_row_errors[actual["row"]].append(error)
    remainder = Fraction(1, 64) ** 9 / 9
    coefficients = max(
        sum((v * Fraction(1, 64) ** j for j, v in enumerate(row)), Fraction(0))
        for row in primary_row_errors
    )
    floors = EPS * sum((Fraction(1, 64) ** j for j in range(8)), Fraction(0))
    for name, value in (
        ("log_table_remainder_upper", remainder),
        ("log_table_literal_rounding_upper", coefficients),
        ("log_table_floor_upper", floors),
        ("log_table_error_upper", remainder + coefficients + floors),
    ):
        require(rational(saved[name]) == value, "Exact primary table error composition")
    require(saved["ln2_literal"] == own["ln2_literal"], "Actual primary ln2 identity")
    lo, hi = [rational(v) for v in saved["ln2_true_enclosure"]]
    a, b = [rational(v) for v in own["ln2_true_enclosure"]]
    require(lo <= a <= b <= hi, "Primary ln2 interval contains independent130-digit interval")
    ln_error = max(
        abs(Fraction(saved["ln2_literal"], Q) - lo), abs(Fraction(saved["ln2_literal"], Q) - hi)
    )
    require(
        rational(saved["ln2_literal_error_upper"]) == ln_error and ln_error <= EPS / 2,
        "Primary ln2 literal discrepancy reconstruction",
    )
    E = remainder + coefficients + floors + 33 * ln_error
    A = 66 * hi + 2 * E
    B, eta, D = [
        rational(saved[k])
        for k in ("internal_radius_upper", "square_error_eta_upper", "squared_radius_KS_upper")
    ]
    require(
        rational(saved["log_error_all_midpoints_upper"]) == E
        and rational(saved["root_argument_upper"]) == A
        and B >= 0
        and B**2 >= A,
        "Primary source-bound log and radius composition",
    )
    require(
        B >= rational(own["internal_radius_upper"]) and A * Q < 1 << 46,
        "Primary radius outward and unsigned46 source contract",
    )
    require(
        eta == 2 * E + 2 * EPS * B + EPS**2 and D == min(Fraction(1), Fraction(1, 2 * N) + eta / 2),
        "Primary squared-radius CDF composition",
    )
    require(
        saved["root_input_unsigned_bit_contract"] == 46
        and rational(saved["root_input_raw_upper"]) == A * Q,
        "Primary actual root-input guard",
    )
    require(
        rational(saved["log_Horner_maximum_magnitude"])
        == rational(own["log_Horner_maximum_magnitude"]),
        "Independent full72/144 Horner range guard",
    )
    require(
        saved["internal_radius_not_final_normal_norm"] is True
        and saved["native_map_monotonicity_used"] is False
        and saved["radial_Holder_or_cutoff_used"] is False
        and saved["all_midpoints_covered_without_sweep"] is True
        and saved["midpoint_exponents"] == [-33, -1],
        "Source/formulation scope retained",
    )
    rows = saved["exact_exponent_class_partition"]
    require(len(rows) == 33, "All33 exact midpoint exponent classes")
    for primary, independent in zip(rows, own["exact_exponent_classes"], strict=True):
        lower, upper = independent["uniform_integer_bounds"]
        expected = dict(
            exponent=independent["exponent"],
            first_raw_uniform=lower,
            last_raw_uniform=upper,
            count=upper - lower + 1,
            midpoint_raw_bounds=[256 * lower + 128, 256 * upper + 128],
            normalized_raw_bounds=independent["mantissa_raw_bounds"],
        )
        same(primary, expected, "Independent complete q32 exponent partition")
    return B, D


def audit_symbolic_identity(saved, started):
    """Decode the primary monomials into a different fixed exponent-vector ring."""
    names = ("A", "B", "s", "c", "k", "U", "V")

    def decode(rows):
        result = {}
        for variables, coefficient in rows:
            require(
                type(variables) is list
                and variables == sorted(variables)
                and all(v in names for v in variables)
                and len(variables) <= 4,
                "Finite canonical formal monomial",
            )
            key = tuple(variables.count(v) for v in names)
            require(key not in result, "Unique formal coefficient")
            result[key] = rational(coefficient)
        return {k: v for k, v in result.items() if v}

    zero = (0,) * 7

    def scalar(value):
        return {zero: Fraction(value)} if value else {}

    def variable(name):
        powers = tuple(int(v == name) for v in names)
        return {powers: Fraction(1)}

    def add(*polynomials):
        result = Counter()
        for polynomial in polynomials:
            for key, value in polynomial.items():
                result[key] += value
        return {k: v for k, v in result.items() if v}

    def negative(value):
        return {k: -v for k, v in value.items()}

    def multiply(*polynomials):
        result = scalar(1)
        for polynomial in polynomials:
            following = Counter()
            for a, av in result.items():
                for b, bv in polynomial.items():
                    following[tuple(x + y for x, y in zip(a, b, strict=True))] += av * bv
            result = {k: v for k, v in following.items() if v}
        return result

    A, B, s, c, k, U, V = [variable(v) for v in names]
    s2, c2 = multiply(s, s), multiply(c, c)
    y = add(negative(multiply(A, s)), multiply(B, c))
    X = add(multiply(c, U), multiply(s, V))
    formulas = {
        "pointwise_nonnegative_remainder": (
            add(multiply(k, add(multiply(s2, A), multiply(c2, B))), negative(multiply(y, y))),
            add(
                multiply(s2, A, add(k, negative(A))),
                multiply(c2, B, add(k, negative(B))),
                multiply(scalar(2), s, c, A, B),
            ),
        ),
        "stationary_U_circle_remainder": (
            add(
                U,
                negative(multiply(c, X)),
                negative(multiply(s, add(multiply(s, U), negative(multiply(c, V))))),
            ),
            multiply(U, add(scalar(1), negative(c2), negative(s2))),
        ),
        "stationary_V_circle_remainder": (
            add(
                V,
                negative(multiply(s, X)),
                negative(multiply(c, add(multiply(c, V), negative(multiply(s, U))))),
            ),
            multiply(V, add(scalar(1), negative(c2), negative(s2))),
        ),
        "circle_sum_bound": (
            multiply(add(s, c), add(s, c)),
            add(scalar(1), multiply(scalar(2), s, c), s2, c2, scalar(-1)),
        ),
        "circle_product_bound": (
            multiply(add(s, negative(c)), add(s, negative(c))),
            add(s2, c2, negative(multiply(scalar(2), s, c))),
        ),
    }
    records = saved["exact_formal_identity_witnesses"]
    require(
        len(records) == 5 and {row["name"] for row in records} == set(formulas),
        "Exactly five frozen angular identities",
    )
    for row in records:
        check(started)
        left, right = formulas[row["name"]]
        require(
            left == right == decode(row["left"]) == decode(row["right"])
            and row["zero_difference"] == [],
            "Own exponent-vector formal identity verification",
        )
    require(
        saved["analytical_premises_are_not_native_finance_equivalence"] is True
        and saved["strict_threshold_TV"] == 2
        and saved["closed_finite_band_TV"] == 4
        and saved["radial_payoff_TV_multiplier"] == 4
        and saved["native_cosine_or_clipped_unimodality_certified"] is False,
        "Frozen conditional analytic scope",
    )
    for name in (
        "radial_CDF",
        "radial_BV",
        "angular_BV",
        "midpoint_circle",
        "hybrid_order",
        "actual_point_value_BV_convention",
    ):
        require(
            type(saved[name]) is list
            and saved[name]
            and all(type(v) is str and v for v in saved[name]),
            "Explicit analytic proof and endpoint obligations retained",
        )
    return dict(
        independent_formal_identities=5,
        exponent_vector_ring=True,
        exact_source_roles_positive=True,
        radial_convexity_unclipped_only=True,
        strict_threshold_TV=2,
        closed_band_TV=4,
        radial_payoff_TV_multiplier=4,
        angular_payoff_TV="2*C*(nt+1)",
        axis_zero_radius_constant_and_strict_ties_retained=True,
        current_radius_replaced_before_current_angle=True,
        native_financial_bridge_open=True,
    )


def audit_guard_and_prices(mp, binding, B, D, own_B, own_D, started):
    saved = read_json(SOURCE / "angular_guards.json", started)
    require(
        set(saved["cases"]) == set(CASES)
        and saved["rejection_blocks_angular_and_dollar_certificates"] is True,
        "Both fixed angular guard scopes",
    )
    all_passed, own_guards = True, {}
    for case, (assets, dates, pairs) in CASES.items():
        check(started)
        norm = rational(binding["cases"][case]["financial_roles"]["ideal_maximum_squared_norm"])
        require(norm == Fraction(9, 100 * dates), "Actual ideal source-role norm bound")
        square = B**2 * norm
        passed = square < 2
        row = dict(
            assets=assets,
            dates=dates,
            joint_pairs=pairs,
            ideal_squared_norm_upper=encode(norm),
            radius_upper=encode(B),
            kappa_squared_upper=encode(square),
            strict_threshold=2,
            passed=passed,
            actual_native_finance_literals_used=False,
        )
        same(saved["cases"][case], row, "Strict actual primary angular guard composition")
        all_passed = all_passed and passed
        own_guards[case] = row
    require(saved["all_strict_guards_passed"] is all_passed, "Complete primary guard conjunction")
    if not all_passed:
        require(
            not (SOURCE / "ideal_hybrid_bounds.json").exists(),
            "Failed guard prohibits dollar certificate",
        )
        return False, dict(cases=own_guards), None
    price = read_json(SOURCE / "ideal_hybrid_bounds.json", started)
    require(
        price["interval_digits"] == 90
        and price["outward_exact_rational_endpoints"] is True
        and set(price["cases"]) == set(CASES),
        "Primary bound precision and scopes",
    )
    discount = endpoints(mp.iv.exp(outward(mp, -Fraction(3, 100))))
    lower, upper = [rational(v) for v in price["exact_discount_enclosure"]]
    require(
        0 < lower <= discount[0] <= discount[1] <= upper < 1, "Exact discounted ideal survival cap"
    )
    independent = {}
    for case, (_, dates, pairs) in CASES.items():
        check(started)
        row = price["cases"][case]
        radial, angular = 4 * (40 * upper) * D, 40 * upper * Fraction(dates + 1, N)
        total = pairs * (radial + angular)
        expected = dict(
            joint_pairs=pairs,
            squared_radius_KS_upper=encode(D),
            exact_cap_enclosure=[encode(40 * lower), encode(40 * upper)],
            one_pair_radial_dollars_upper=encode(radial),
            one_pair_angular_dollars_upper=encode(angular),
            hybrid_dollars_upper=encode(total),
            unchanged_residual_dollars=[11, 2000],
            partial_bound_below_context_residual=total < Fraction(11, 2000),
            residual_spent_or_reallocated=False,
            full_native_G2_acceptance=False,
            adoption=False,
        )
        same(row, expected, "Every primary whole-pair dollar formula and scope")
        independent[case] = dict(
            cap_enclosure=[encode(40 * v) for v in discount],
            audited_primary_hybrid_upper=encode(total),
            whole_joint_pairs=pairs,
            independent130_kappa_squared_upper=encode(own_B**2 * Fraction(9, 100 * dates)),
            independent130_squared_radius_KS_upper=encode(own_D),
            independent130_hybrid_upper=encode(
                pairs * (4 * 40 * discount[1] * own_D + 40 * discount[1] * Fraction(dates + 1, N))
            ),
            residual_spent_or_reallocated=False,
            full_G2=False,
        )
    for name in (
        "joint_digital_normals_asserted_independent",
        "native_cosine_envelope_computed",
        "full_G2",
        "cost_transfer",
        "adoption",
    ):
        require(price[name] is False, "No native-law, financial or cost transfer")
    require(
        price["test_credit"] == 0
        and price["native_financial_bridge_open"] is True
        and price["no_old_Holder_or_grid_term_added_again"] is True
        and price["pair_order"] == "each current radius FIRST then current ideal angle",
        "Hybrid pay-once order",
    )
    return (
        True,
        dict(cases=own_guards),
        dict(cases=independent, own_discount_enclosure=[encode(v) for v in discount]),
    )


def initialize(started):
    """Independent admission of the actual local interpreter; stdlib only."""
    global BASE_PREFIX, BASE_TREES, BASE_FILES, BASE_SITE_LEXICAL, BASE_SITE
    PATH_CACHE.clear()
    ACTUAL_HASH_CACHE.clear()
    OBSERVED_HASHES.clear()
    require(sys.dont_write_bytecode is True, "Interpreter startup -B is mandatory")
    require(
        Path.cwd().resolve() == ROOT and Path(__file__).resolve() == AUTHOR,
        "Exact auditor module and working directory",
    )
    require(Path(sys.executable).resolve() == LAUNCHER, "Pinned isolated launcher")
    require(
        Path(sys.prefix).resolve() == ROOT / ".context/frontier_t0_env",
        "Exact isolated interpreter prefix",
    )
    require(site.ENABLE_USER_SITE is False, "User site must be disabled")
    for name in ("PYTHONPATH", "PYTHONHOME", "SAGE_ROOT", "MPMATH_SAGE"):
        require(not os.environ.get(name), "Unexpected runtime override: " + name)
    os.environ["MPMATH_NOGMPY"] = os.environ["MPMATH_NOSAGE"] = "1"
    BASE_PREFIX = Path(sys.base_prefix).resolve(strict=True)
    BASE_SITE_LEXICAL = BASE_PREFIX / "Lib/site-packages"
    BASE_SITE = BASE_SITE_LEXICAL.resolve()
    base = Path(getattr(sys, "_base_executable", sys.executable)).resolve(strict=True)
    require(base.parent == BASE_PREFIX, "Actual adjacent base interpreter")
    BASE_TREES = tuple(
        (BASE_PREFIX / name).resolve(strict=True)
        for name in ("Lib", "DLLs")
        if (BASE_PREFIX / name).is_dir()
    )
    BASE_FILES = tuple(
        path.resolve(strict=True) for path in BASE_PREFIX.iterdir() if path.is_file()
    )
    require(base in BASE_FILES, "Actual base executable is captured")
    forbidden_imports()
    check(started)


def forbidden_imports():
    banned = ("numpy", "scipy", "numba", "llvmlite", "qiskit", "gmpy", "gmpy2", "sage")
    for name in sys.modules:
        require(
            not any(name == prefix or name.startswith(prefix + ".") for prefix in banned),
            "Forbidden numerical or SDK import: " + name,
        )
        if name.startswith("research."):
            require(
                name
                in (
                    "research.limitation_program_20261001",
                    "research.limitation_program_20261001.audit_box_muller_polar_cdf_bv_v2",
                ),
                "Auditor must not import producer or other research helpers",
            )


def permitted(path):
    if BASE_SITE is not None and path.is_relative_to(BASE_SITE):
        return False
    return (
        path.is_relative_to(ROOT)
        or path == BASE_PREFIX
        or path in BASE_FILES
        or any(path.is_relative_to(root) for root in BASE_TREES)
    )


def reject_unreachable_origin(path, started):
    """Deny excluded lexical/physical origins even when their files disappeared."""
    check(started)
    candidate = Path(path)
    require(not candidate.drive or candidate.is_absolute(), "Ambiguous runtime origin drive")
    require(
        BASE_SITE_LEXICAL is None or not candidate.absolute().is_relative_to(BASE_SITE_LEXICAL),
        "Unreachable base site-packages lexical origin forbidden",
    )
    actual = candidate.resolve(strict=False)
    require(
        BASE_SITE is None or not actual.is_relative_to(BASE_SITE),
        "Unreachable base site-packages physical origin forbidden",
    )
    check(started)


def canonical_path(path, started, *, fresh=False):
    check(started)
    value = Path(path)
    require(not value.drive or value.is_absolute(), "Ambiguous drive-relative path forbidden")
    require(
        BASE_SITE_LEXICAL is None or not value.absolute().is_relative_to(BASE_SITE_LEXICAL),
        "Unreachable base site-packages lexical paths forbidden",
    )
    lexical = str(value.absolute())
    if not fresh and lexical in PATH_CACHE:
        check(started)
        return PATH_CACHE[lexical]
    actual = value.resolve(strict=True)
    require(permitted(actual), "Outside ROOT or exact observed base-runtime scopes")
    require(
        lexical not in PATH_CACHE or PATH_CACHE[lexical] == actual,
        "Previously confined lexical path redirected",
    )
    PATH_CACHE[lexical] = actual
    PATH_CACHE.setdefault(str(actual), actual)
    check(started)
    return actual


def fingerprint(path):
    data = path.stat()
    return (
        data.st_dev,
        data.st_ino,
        data.st_size,
        data.st_mtime_ns,
        data.st_ctime_ns,
        getattr(data, "st_file_attributes", None),
        getattr(data, "st_reparse_tag", None),
    )


def actual_digest(path, started, *, fresh=False):
    check(started)
    require(permitted(path), "Pre-read confinement of actual hash path")
    identity, key = fingerprint(path), str(path)
    require(path.is_file(), "Actual regular byte input")
    if not fresh and key in ACTUAL_HASH_CACHE and ACTUAL_HASH_CACHE[key][0] == identity:
        check(started)
        return ACTUAL_HASH_CACHE[key][1]
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            check(started)
            state.update(block)
            check(started)
    require(fingerprint(path) == identity, "Actual bytes changed during SHA observation")
    result = state.hexdigest()
    require(
        key not in OBSERVED_HASHES or OBSERVED_HASHES[key] == result,
        "First independently observed actual SHA changed",
    )
    OBSERVED_HASHES.setdefault(key, result)
    ACTUAL_HASH_CACHE[key] = (identity, result)
    check(started)
    return result


def sha(path, started, *, fresh=False):
    return actual_digest(canonical_path(path, started, fresh=fresh), started, fresh=fresh)


def root_key(path, started):
    actual = canonical_path(path, started)
    require(actual.is_relative_to(ROOT), "ROOT-relative field confinement")
    return actual.relative_to(ROOT).as_posix()


def bind(frozen, external, path, expected, started):
    check(started)
    require(type(expected) is str and SHA_PATTERN.fullmatch(expected), "Canonical SHA256")
    actual = canonical_path(path, started)
    mapping = frozen if actual.is_relative_to(ROOT) else external
    key = actual.relative_to(ROOT).as_posix() if actual.is_relative_to(ROOT) else str(actual)
    require(key not in mapping or mapping[key] == expected, "Conflicting expected SHA binding")
    require(actual_digest(actual, started) == expected, "Actual byte SHA differs: " + key)
    mapping[key] = expected
    check(started)
    return actual


def read_bytes(path, started):
    actual = canonical_path(path, started)
    identity = fingerprint(actual)
    require(
        actual.is_file() and identity[2] <= 128 * 1024**2, "Bounded regular source/artifact input"
    )
    chunks, state, total = [], hashlib.sha256(), 0
    with actual.open("rb") as stream:
        while block := stream.read(1 << 20):
            check(started)
            total += len(block)
            require(total <= identity[2], "Text input grew while reading")
            state.update(block)
            check(started)
            chunks.append(block)
    require(
        total == identity[2] and fingerprint(actual) == identity,
        "Exact text bytes stable during read",
    )
    data = b"".join(chunks)
    observed = state.hexdigest()
    check(started)
    key = str(actual)
    require(
        key not in OBSERVED_HASHES or OBSERVED_HASHES[key] == observed,
        "JSON/source read contradicts original actual SHA",
    )
    OBSERVED_HASHES.setdefault(key, observed)
    ACTUAL_HASH_CACHE[key] = (identity, observed)
    return data


def read_json(path, started):
    value = json.loads(read_bytes(path, started))
    check(started)
    return value


def write_json(path, value, started):
    check(started)
    data = (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()
    check(started)
    require(len(data) <= 128 * 1024**2, "Bounded JSON output")
    with Path(path).open("xb") as stream:
        for offset in range(0, len(data), 1 << 20):
            check(started)
            stream.write(data[offset : offset + (1 << 20)])
            check(started)


def verify_maps(frozen, external, started):
    for mapping, parent in ((frozen, ROOT), (external, None)):
        for key, expected in mapping.items():
            check(started)
            path = parent / key if parent is not None else Path(key)
            require(sha(path, started) == expected, "Immutable map byte mismatch: " + key)


def final_fresh(frozen, external, started):
    """Fresh confinement for all aliases and fresh full bytes for every actual path."""
    for lexical, expected_path in tuple(PATH_CACHE.items()):
        check(started)
        require(
            canonical_path(lexical, started, fresh=True) == expected_path,
            "Final independent lexical alias mismatch",
        )
    expected = {}
    for mapping, parent in ((frozen, ROOT), (external, None)):
        for key, value in mapping.items():
            check(started)
            actual = canonical_path(parent / key if parent is not None else key, started)
            require(actual not in expected or expected[actual] == value, "Equal-SHA final merge")
            expected[actual] = value
    observed = {Path(key): value for key, value in OBSERVED_HASHES.items()}
    union = set(expected) | set(observed)
    for path in sorted(union):
        check(started)
        actual = canonical_path(path, started, fresh=True)
        value = actual_digest(actual, started, fresh=True)
        require(path not in expected or expected[path] == value, "Final expected SHA differs")
        require(path not in observed or observed[path] == value, "Final observed SHA differs")
    return len(union)


def original_owner_entries(path, data, started):
    """Independently normalize exact historical map conventions, without LIVE waiver."""
    if "files" in data:
        require(
            data.get("manifest_self_hash_excluded") is True,
            "Original nested owner self-hash convention",
        )
        mappings = [(field, data.get(field, {})) for field in ("files", "frozen_inputs")]
    else:
        require(
            path == PROGRAM / "A10_coefficient_run001/manifest.json",
            "Only pinned historical A10 flat map is recognized",
        )
        mappings = [("flat_owned_files", data)]
    result = []
    for field, mapping in mappings:
        require(type(mapping) is dict, "Recognized original expected byte map")
        for literal, expected in mapping.items():
            check(started)
            require(
                type(literal) is str and type(expected) is str and SHA_PATTERN.fullmatch(expected),
                "Typed original map record",
            )
            normalized = literal.replace("\\", "/")
            route = (
                ROOT / normalized
                if normalized.startswith(
                    ("results/", "research/", "docs/", "manuscript/", ".context/")
                )
                else path.parent / normalized
            )
            # Membership is structural; no claim that every original current source remains LIVE.
            actual = route.resolve()
            require(actual.is_relative_to(ROOT), "Original membership confined to ROOT")
            result.append((field, actual, literal, expected))
            check(started)
    return result


def independent_origins(pins, owners, frozen, external, started, *, selected):
    inventories = []
    for key, expected in owners.items():
        path = bind(frozen, external, ROOT / key, expected, started)
        inventories.append((key, original_owner_entries(path, read_json(path, started), started)))
    records = []
    for key, expected in pins.items():
        check(started)
        actual = bind(frozen, external, ROOT / key, expected, started)
        if selected and key.endswith("/manifest.json"):
            continue
        matches = []
        for owner, inventory in inventories:
            for field, candidate, original, value in inventory:
                check(started)
                if candidate == actual and value == expected:
                    matches.append(
                        dict(
                            owner_manifest=owner,
                            source_map=field,
                            original_key=original,
                            expected_sha256=value,
                        )
                    )
        require(matches, "Original equal-SHA owner membership required: " + key)
        row = dict(
            path=key, sha256=expected, original_memberships=matches, expected_hash_waived=False
        )
        if selected:
            row["archived_route"] = False
        records.append(row)
    return records


def implementation_policy(started):
    data = read_json(IMPLEMENTATION, started)
    require(
        data["schema"] == "box-muller-polar-cdf-bv-implementation-preflight-v2",
        "Exact implementation policy schema",
    )
    for name in (
        "producer_CPU_admission_wall_seconds",
        "independent_auditor_CPU_admission_wall_seconds",
    ):
        same(data[name], [CPU, ADMISSION, WALL], "Fixed complete process budgets")
    require(
        data["primary_interval_decimal_digits"] == 90
        and data["independent_interval_decimal_digits"] == DIGITS
        and data["numerical_threads"] == 1
        and data["new_fixture_credit"] == 0,
        "Fixed interval precision, threads and zero fixtures",
    )
    require(
        data["runtime_backend"] == "python"
        and data["mpmath_version"] == "1.3.0"
        and data["MPMATH_NOGMPY"] == data["MPMATH_NOSAGE"] == "1"
        and data["startup_B_required"] is True
        and data["cosine_512_coefficient_envelope_in_scope"] is False
        and data["native_financial_bridge_open"] is True,
        "Held pure-Python and incomplete native bridge scope",
    )
    same(
        data["runtime_inventory_cap_files_bytes"],
        [MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES],
        "Complete runtime inventory fixed caps",
    )
    scope = data["runtime_scope"]
    require(
        scope["base_Lib_site_packages"] == "EXCLUDED_UNREACHABLE_AND_REJECTED"
        and scope["full_remaining_standard_Lib"] is True
        and scope["actual_venv_pth_customize_and_loaded_bootstrap_bytes"] is True
        and scope["full_mpmath_existing_cache_and_distribution_metadata"] is True
        and scope["full_base_DLL_and_adjacent_files"] is True
        and scope["no_blanket_other_venv_package_admission"] is True
        and scope["excluded_lexical_resolved_alias_and_vanished_module_origins_rejected"] is True
        and scope["selected_source_and_old_provenance_hash_waivers"] is False,
        "Exact reachable-runtime scope correction without expected hash waiver",
    )
    same(
        data["method_document_SHA256"],
        {METHOD.name: METHOD_SHA, METHOD_DOC.name: METHOD_DOC_SHA},
        "Exact immutable held method documents",
    )
    same(data["original_root_owner_manifest_SHA256"], ROOT_OWNERS, "Pinned root proof owners")
    same(
        data["additional_native_root_provenance_SHA256"],
        ROOT_PINS,
        "All13 exact actual root inputs",
    )
    require(
        data["producer_receipt"] == SOURCE.relative_to(ROOT).as_posix()
        and data["independent_auditor_receipt"] == OUTPUT.relative_to(ROOT).as_posix(),
        "Fresh exact source and audit receipt labels",
    )
    hashes = data["author_sha256"]
    require(
        set(hashes) == {AUTHOR.name, PRODUCER_AUTHOR.name}, "Both executable author pins required"
    )
    for name, expected in hashes.items():
        require(
            type(expected) is str and SHA_PATTERN.fullmatch(expected),
            "Null author SHA blocks prepare",
        )
        require(sha(RESEARCH / name, started) == expected, "Exact frozen executable bytes")
    return data


def prior_failed_admission(data, frozen, external, started):
    same(data["original_polar_author_SHA256"], ORIGINAL_AUTHORS, "Exact immutable original quartet")
    require(
        data["original_admission_failure_manifest_SHA256"] == ORIGINAL_FAILURE_SHA
        and data["original_root_review_manifest_SHA256"] == ORIGINAL_REVIEW_SHA,
        "Exact actual pre-mkdir failure and original root review pins",
    )
    require(
        not (PROGRAM / "A02_polar_cdf_bv_run001").exists()
        and not (PROGRAM / "A02_polar_cdf_bv_audit_run001").exists(),
        "Original failed admission created no execution or audit receipt",
    )
    for name, expected in ORIGINAL_AUTHORS.items():
        check(started)
        bind(frozen, external, RESEARCH / name, expected, started)
    for path, expected in ((METHOD, METHOD_SHA), (METHOD_DOC, METHOD_DOC_SHA)):
        bind(frozen, external, path, expected, started)
    for receipt, expected, own_count, input_count in (
        (ORIGINAL_FAILURE, ORIGINAL_FAILURE_SHA, 3, 8),
        (ORIGINAL_REVIEW, ORIGINAL_REVIEW_SHA, 1, 6),
    ):
        manifest = bind(frozen, external, receipt / "manifest.json", expected, started)
        packet = read_json(manifest, started)
        require(
            packet.get("manifest_self_hash_excluded") is True, "Pinned original manifest convention"
        )
        require(
            packet["new_fixture_credit"] == 0
            and len(packet["files"]) == own_count
            and len(packet["frozen_inputs"]) == input_count,
            "Exact complete prior owner/input map counts and zero credit",
        )
        owned = set()
        for field, path, original, expected in original_owner_entries(manifest, packet, started):
            check(started)
            actual = bind(frozen, external, path, expected, started)
            require(
                actual.relative_to(ROOT).as_posix() == original,
                "Original canonical ROOT-relative path without alias",
            )
            if field == "files":
                require(actual.is_relative_to(receipt), "Original owned file confinement")
                owned.add(actual.relative_to(receipt).as_posix())
        current = set()
        for path in receipt.rglob("*"):
            check(started)
            if path.is_file():
                actual = canonical_path(path, started)
                require(actual.is_relative_to(receipt), "Original directory file confinement")
                key = actual.relative_to(receipt).as_posix()
                require(key not in current, "Original receipt has no aliased owned file")
                current.add(key)
        same(
            sorted(current),
            sorted(owned | {"manifest.json"}),
            "Complete original owned directory membership",
        )
    failure = read_json(ORIGINAL_FAILURE / "summary.json", started)
    require(
        failure["schema"] == "root-polar-pre-mkdir-admission-failure-v1"
        and failure["diagnostic_passed"] is True
        and failure["original_prepare_passed"] is False
        and failure["original_execution_receipt_created"] is False
        and failure["new_fixture_or_scientific_credit"] == 0
        and failure["runtime_inventory_cap_rejected"] is True
        and failure["process_budget_censor_claim"] is False
        and failure["old_sources_and_review_immutable"] is True,
        "Actual source-bound pre-mkdir file-cap failure, zero credit",
    )
    review = read_json(ORIGINAL_REVIEW / "summary.json", started)
    require(
        review["static_root_review_passed"] is True
        and review["independent_peer_review_passed"] is True
        and review["author_sources_frozen"] is True
        and review["new_fixture_credit"] == 0
        and review["scientific_kernel_or_prepare_or_sourcewalker_executed_by_review"] is False,
        "Original source static review is not a scientific result",
    )
    for record in (failure, review):
        require(
            record["full_G2"] is record["cost_transfer"] is record["adoption"] is False,
            "No failure/review numerical or adoption credit",
        )


def method_origins(implementation, frozen, external, started):
    prior_failed_admission(implementation, frozen, external, started)
    bind(frozen, external, METHOD, METHOD_SHA, started)
    bind(frozen, external, METHOD_DOC, METHOD_DOC_SHA, started)
    plan = read_json(METHOD, started)
    require(
        plan["status"] == "HELD_AUTHOR_ONLY_NO_EXECUTOR_OR_EXECUTION", "Immutable held method state"
    )
    pins = plan["source_bindings_SHA256"]
    require(type(pins) is dict and len(pins) == 17, "All17 original selected pins")
    owners = {key: value for key, value in pins.items() if key.endswith("/manifest.json")}
    require(len(owners) == 3, "All3 selected original owners")
    selected = independent_origins(pins, owners, frozen, external, started, selected=True)
    require(len(selected) == 14, "All14 selected nonmanifest memberships")
    roots = independent_origins(ROOT_PINS, ROOT_OWNERS, frozen, external, started, selected=False)
    for path in (AUTHOR, PRODUCER_AUTHOR, IMPLEMENTATION, IMPLEMENTATION_DOC):
        bind(frozen, external, path, sha(path, started), started)
    same(
        implementation["author_sha256"],
        {
            name: frozen[(RESEARCH / name).relative_to(ROOT).as_posix()]
            for name in (AUTHOR.name, PRODUCER_AUTHOR.name)
        },
        "Actual pinned authors",
    )
    return plan, selected, roots


def independent_root_semantics(started):
    """No array load: exact bytes tie prior universal induction to its actual realization."""
    prior = PROGRAM / "A01_run011"
    proof = read_json(prior / "nonrestoring_arithmetic_certificate.json", started)
    structural = read_json(prior / "leaf_audit.json", started)
    old = read_json(PROGRAM / "A11_nonrestoring_leaf_run001/02b69bbccf8176e3b72d.json", started)
    require(
        proof["passed"] is True
        and proof["algebraic_all_guarded_input_identity"] is True
        and proof["input_formula"] == "isqrt(unsigned_x << fraction_bits)"
        and proof["invariant"] == "Q=isqrt(N); R=N-Q\u00b2 if nonnegative, else N-(Q+1)\u00b2",
        "Previously executed all-input nonrestoring induction, not finite fixtures",
    )
    parser = structural["structural_parser"]
    require(
        structural["passed"] is True
        and parser["passed"] is True
        and parser["all_stages"] == 43
        and parser["full_native_argument_bits"] == parser["full_native_output_bits"] == 72
        and parser["signed_remainder_bits"] == 45
        and parser["retained_remainder_history_count"] == 44,
        "Prior actual full-stage structural realization",
    )
    for key in (
        "arbitrary_output_xor",
        "literal_forward_reverse_cleanup",
        "input_high_bits_untouched",
        "output_high_bits_unchanged",
    ):
        require(parser[key] is True, "Prior actual arbitrary output and cleanup guard")
    original = read_json(prior / "manifest.json", started)
    routes = []
    for old_key, basename in (
        ("research/controlled_source_completion/nonrestoring_sqrt.py", "nonrestoring_sqrt.py"),
        ("research/journal_sprint/reversible_fixed_point.py", "reversible_fixed_point.py"),
        ("research/antithetic_feasibility/reversible.py", "reversible.py"),
    ):
        check(started)
        archive = PROGRAM / "A10_coefficient_run001/executed_code" / basename
        expected = original["frozen_inputs"][old_key]
        require(
            sha(archive, started) == expected, "Prior universal proof source archived byte identity"
        )
        routes.append(
            dict(
                original_owner="A01_run011",
                original_map="frozen_inputs",
                original_key=old_key,
                expected_sha256=expected,
                verified_archived_path=archive.relative_to(ROOT).as_posix(),
                current_original_path_integrity_asserted=False,
                expected_hash_waived=False,
            )
        )
    result = {}
    for case in CASES:
        check(started)
        path = (
            PROGRAM / "A10_coefficient_run001" / case / "min-depth/leaves" / (ROOT_LEAF + ".json")
        )
        descriptor = read_json(path, started)
        require(
            descriptor["key"] == ROOT_LEAF
            and descriptor["op"] == "sqrt"
            and descriptor["params"] == {},
            "Exact integrated original native root",
        )
        same(
            descriptor["input_contract"],
            {"unsigned_input_bits": 46},
            "Unsigned46 root input contract",
        )
        same(descriptor["args"], [list(range(72))], "Full72 actual input bank")
        same(descriptor["outs"], [list(range(72, 144))], "Full72 arbitrary output XOR bank")
        spec = descriptor["spec"]
        for key, expected in {
            "width": 72,
            "fraction_bits": 40,
            "active_input_bits": 46,
            "radicand_bits": 86,
            "result_bits": 43,
            "remainder_bits": 45,
            "remainder_history_count": 44,
            "operand_bits": 45,
            "adder_helper_bits": 1,
        }.items():
            require(type(spec[key]) is int and spec[key] == expected, "Original native root widths")
        require(
            spec["algorithm"] == "signed-remainder-single-cuccaro-add"
            and spec["lowering"] == "unsigned-nonrestoring-sqrt-signed-remainder-v1"
            and spec["integration_lowering"] == "same-target-nonrestoring-unsigned-sqrt-library-v1",
            "Exact original root method",
        )
        same(spec["input_contract"], descriptor["input_contract"], "Exact nested contract")
        canonical = json.dumps(spec, sort_keys=True, separators=(",", ":"))
        require(
            hashlib.sha256(canonical.encode()).hexdigest()[:20] == ROOT_LEAF,
            "Original exact specification key",
        )
        base_spec = {key: value for key, value in spec.items() if key != "integration_lowering"}
        same(base_spec, old["spec"], "Same universal-audited leaf specification")
        same(descriptor["args"], old["args"], "Prior actual full input bank identity")
        same(descriptor["outs"], old["outs"], "Prior actual arbitrary output bank identity")
        gate = canonical_path(path.parent / descriptor["gate_file"], started)
        require(
            gate.parent == path.parent
            and gate.name == ROOT_LEAF + ".npy"
            and descriptor["sha256"] == old["sha256"] == sha(gate, started),
            "Actual integrated array identical to prior all-input realization bytes",
        )
        result[case] = dict(
            path=path.relative_to(ROOT).as_posix(),
            spec=spec,
            gate_path=gate.relative_to(ROOT).as_posix(),
            gate_sha256=descriptor["sha256"],
        )
    return dict(
        actual_descriptors=result,
        prior_universal_induction=proof,
        prior_actual_gate_structure=parser,
        prior_proof_source_archived_equal_SHA_routes=routes,
        source_array_identity_not_fixture_inference=True,
        root_semantics="out XOR isqrt(unsigned argument <<40), high argument bits46..71 zero",
        no_new_gate_scan_replay_or_synthesis=True,
    )


def runtime_candidates(root, started):
    """Prune the unreachable base site directory before traversing its entries."""
    root = canonical_path(root, started)
    if root.is_file():
        yield root
        return
    require(root.is_dir(), "Finite actual runtime directory")
    for current, directory_names, filenames in os.walk(root, topdown=True, followlinks=False):
        check(started)
        directory = canonical_path(current, started)
        require(
            directory == root or directory.is_relative_to(root),
            "Runtime walk directory confinement",
        )
        retained = []
        for name in directory_names:
            check(started)
            candidate = directory / name
            if candidate.absolute() == BASE_SITE_LEXICAL:
                continue
            actual = canonical_path(candidate, started)
            require(actual.is_relative_to(root), "Runtime directory alias escape")
            require(
                not candidate.is_symlink() and not candidate.is_junction(),
                "Untraversed runtime directory links forbidden",
            )
            retained.append(name)
        directory_names[:] = retained
        for name in filenames:
            check(started)
            candidate = directory / name
            if candidate.is_file():
                actual = canonical_path(candidate, started)
                require(actual.is_relative_to(root), "Runtime file alias escape")
                yield actual


def bootstrap_runtime_paths(site_root, started):
    """Exact actual hook roots and preexisting loaded venv files, without package expansion."""
    paths = set()
    for candidate in site_root.iterdir():
        check(started)
        hook_name = candidate.name.split(".", 1)[0]
        customize_names = ("sitecustomize", "usercustomize")
        hook_file = candidate.is_file() and (
            candidate.suffix.lower() == ".pth"
            or hook_name in customize_names
            and candidate.suffix.lower() in (".py", ".pyc", ".pyd")
        )
        hook_package = candidate.is_dir() and candidate.name in customize_names
        if not (hook_file or hook_package):
            continue
        reject_unreachable_origin(candidate, started)
        require(candidate.absolute().is_relative_to(site_root), "Lexical isolated startup hook")
        actual = canonical_path(candidate, started)
        require(actual.is_relative_to(site_root), "Physical isolated startup hook")
        require(actual.is_file() or actual.is_dir(), "Actual startup hook file or package")
        paths.add(actual)
        if candidate.suffix == ".py":
            cached = Path(cache_from_source(str(candidate)))
            reject_unreachable_origin(cached, started)
            if cached.is_file():
                require(
                    cached.absolute().is_relative_to(site_root), "Lexical startup cache confinement"
                )
                cache_actual = canonical_path(cached, started)
                require(
                    cache_actual.is_relative_to(site_root), "Physical startup cache confinement"
                )
                paths.add(cache_actual)
    for module in tuple(sys.modules.values()):
        check(started)
        if module is None:
            continue
        for origin in (getattr(module, "__file__", None), getattr(module, "__cached__", None)):
            if not origin:
                continue
            reject_unreachable_origin(origin, started)
            lexical = Path(origin).absolute()
            if Path(origin).is_file():
                actual = canonical_path(origin, started)
                if lexical.is_relative_to(site_root):
                    require(
                        actual.is_relative_to(site_root), "Loaded venv bootstrap alias confinement"
                    )
                if actual.is_relative_to(site_root) and not actual.is_relative_to(
                    site_root / "mpmath"
                ):
                    paths.add(actual)
    return sorted(paths)


def runtime_inventory(frozen, external, started):
    prefix = canonical_path(sys.prefix, started)
    config = prefix / "pyvenv.cfg"
    require(
        "include-system-site-packages = false" in read_bytes(config, started).decode().lower(),
        "Isolated actual venv config",
    )
    site_root = canonical_path(prefix / "Lib/site-packages", started)
    distribution = metadata.distribution("mpmath")
    require(
        distribution.version == "1.3.0" and distribution.files,
        "Fixed installed mpmath RECORD inventory",
    )
    metadata_roots = set()
    for member in distribution.files:
        check(started)
        path = canonical_path(distribution.locate_file(member), started)
        for parent in (path, *path.parents):
            if parent.name.endswith(".dist-info"):
                metadata_roots.add(parent)
                break
    require(len(metadata_roots) == 1, "Exactly one actual mpmath metadata root")
    metadata_root = metadata_roots.pop()
    require(metadata_root.parent == site_root, "Distribution metadata confined to pinned site")
    roots = [
        config,
        prefix / "Scripts",
        site_root / "mpmath",
        metadata_root,
        *BASE_TREES,
        *BASE_FILES,
    ]
    bootstrap_paths = bootstrap_runtime_paths(site_root, started)
    roots.extend(bootstrap_paths)
    for path in (ROOT / "research/__init__.py", RESEARCH / "__init__.py"):
        if path.is_file():
            roots.append(path)
    for path in (AUTHOR, PRODUCER_AUTHOR):
        cached = Path(cache_from_source(str(path)))
        if cached.is_file():
            roots.append(cached)
    paths, total = set(), 0
    actual_roots = []
    for route in roots:
        root = canonical_path(route, started)
        actual_roots.append(str(root))
        for candidate in runtime_candidates(root, started):
            check(started)
            if not candidate.is_file():
                continue
            path = canonical_path(candidate, started)
            require(path == root or path.is_relative_to(root), "Actual runtime tree confinement")
            if path in paths:
                continue
            total += path.stat().st_size
            paths.add(path)
            require(
                len(paths) <= MAX_RUNTIME_FILES and total <= MAX_RUNTIME_BYTES,
                "Fixed entire runtime inventory cap",
            )
            bind(frozen, external, path, sha(path, started), started)
    absent = []
    allowed_roots = {ROOT, site_root, BASE_PREFIX, *BASE_TREES}
    for entry in sys.path:
        check(started)
        path = Path(entry or ROOT)
        reject_unreachable_origin(path, started)
        if path.exists():
            require(
                canonical_path(path, started) in allowed_roots
                or canonical_path(path, started) in BASE_FILES,
                "Unexpected actual module search path",
            )
        else:
            actual = path.resolve()
            require(
                actual
                == BASE_PREFIX
                / ("python" + str(sys.version_info.major) + str(sys.version_info.minor) + ".zip"),
                "Only standard absent interpreter zip",
            )
            absent.append(str(actual))
    return dict(
        python_version=sys.version,
        executable=str(canonical_path(sys.executable, started)),
        base_executable=str(canonical_path(sys._base_executable, started)),
        base_prefix=str(BASE_PREFIX),
        venv_prefix=str(prefix),
        mpmath_version="1.3.0",
        backend="python",
        MPMATH_NOGMPY="1",
        MPMATH_NOSAGE="1",
        startup_bytecode_disabled=True,
        user_site_disabled=True,
        runtime_inventory=dict(
            roots=actual_roots,
            actual_file_paths=sorted(str(p) for p in paths),
            files=len(paths),
            bytes=total,
        ),
        sys_path=list(sys.path),
        external_runtime_trees=[str(p) for p in BASE_TREES],
        external_adjacent_files=[str(p) for p in BASE_FILES],
        absent_standard_runtime_paths=absent,
        excluded_base_site_packages=str(BASE_SITE),
        excluded_base_site_packages_lexical=str(BASE_SITE_LEXICAL),
        base_site_packages_import_rejected=True,
        bootstrap_hook_and_loaded_venv_paths=[str(path) for path in bootstrap_paths],
        standard_Lib_excludes_only_unreachable_base_site_packages=True,
        other_installed_venv_packages_not_blanket_admitted=True,
    )


def verify_runtime(record, frozen, external, started):
    check(started)
    require(
        record["python_version"] == sys.version
        and record["executable"] == str(canonical_path(sys.executable, started))
        and record["base_executable"] == str(canonical_path(sys._base_executable, started))
        and record["base_prefix"] == str(BASE_PREFIX)
        and record["venv_prefix"] == str(canonical_path(sys.prefix, started))
        and record["mpmath_version"] == metadata.version("mpmath") == "1.3.0",
        "Actual interpreter and dependency version provenance",
    )
    same(record["sys_path"], list(sys.path), "Exact interpreter search path snapshot")
    same(
        record["external_runtime_trees"],
        [str(p) for p in BASE_TREES],
        "Exact observed base tree scopes",
    )
    same(
        record["external_adjacent_files"],
        [str(p) for p in BASE_FILES],
        "Exact observed adjacent runtime files",
    )
    require(
        record["backend"] == "python"
        and record["startup_bytecode_disabled"] is True
        and record["user_site_disabled"] is True
        and sys.dont_write_bytecode is True
        and site.ENABLE_USER_SITE is False
        and os.environ.get("MPMATH_NOGMPY") == os.environ.get("MPMATH_NOSAGE") == "1",
        "Exact isolated pure Python import policy",
    )
    require(
        record["excluded_base_site_packages"] == str(BASE_SITE)
        and record["excluded_base_site_packages_lexical"] == str(BASE_SITE_LEXICAL)
        and record["base_site_packages_import_rejected"] is True,
        "Exact unreachable base site-packages exclusion and import rejection",
    )
    require(
        record["standard_Lib_excludes_only_unreachable_base_site_packages"] is True
        and record["other_installed_venv_packages_not_blanket_admitted"] is True,
        "Full remaining runtime and selected venv package policy",
    )
    site_root = canonical_path(Path(sys.prefix) / "Lib/site-packages", started)
    same(
        [str(path) for path in bootstrap_runtime_paths(site_root, started)],
        record["bootstrap_hook_and_loaded_venv_paths"],
        "Actual complete startup hook membership",
    )
    allowed_sys_roots = {ROOT, site_root, BASE_PREFIX, *BASE_TREES}
    for entry in sys.path:
        check(started)
        candidate = Path(entry or ROOT)
        reject_unreachable_origin(candidate, started)
        if candidate.exists():
            actual = canonical_path(candidate, started)
            require(
                actual in allowed_sys_roots or actual in BASE_FILES,
                "Unexpected current sys.path root",
            )
    paths = set()
    for route in record["runtime_inventory"]["roots"]:
        root = canonical_path(route, started)
        for candidate in runtime_candidates(root, started):
            check(started)
            if candidate.is_file():
                path = canonical_path(candidate, started)
                require(
                    path == root or path.is_relative_to(root),
                    "Fresh runtime membership confinement",
                )
                paths.add(path)
    same(
        sorted(str(p) for p in paths),
        record["runtime_inventory"]["actual_file_paths"],
        "Complete existing source/cache/metadata/runtime file membership",
    )
    total = 0
    for path in paths:
        check(started)
        total += path.stat().st_size
        require(
            len(paths) <= MAX_RUNTIME_FILES and total <= MAX_RUNTIME_BYTES,
            "Actual complete runtime cap",
        )
        key = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)
        mapping = frozen if path.is_relative_to(ROOT) else external
        require(
            key in mapping and sha(path, started) == mapping[key],
            "Entire runtime byte origin is frozen",
        )
    require(
        record["runtime_inventory"]["files"] == len(paths)
        and record["runtime_inventory"]["bytes"] == total,
        "Exact recorded runtime count and bytes",
    )
    for path in record["absent_standard_runtime_paths"]:
        check(started)
        require(not Path(path).exists(), "Recorded absent interpreter zip appeared")
    forbidden_imports()


def loaded_origins(frozen, external, started):
    forbidden_imports()
    result = []
    for name, module in tuple(sys.modules.items()):
        check(started)
        if module is None:
            continue
        for kind, origin in (
            ("source", getattr(module, "__file__", None)),
            ("cache", getattr(module, "__cached__", None)),
        ):
            if origin:
                reject_unreachable_origin(origin, started)
            if origin and Path(origin).is_file():
                path = canonical_path(origin, started)
                key = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)
                mapping = frozen if path.is_relative_to(ROOT) else external
                require(
                    key in mapping and sha(path, started) == mapping[key],
                    "Actual loaded module source/existing cache not frozen: " + name,
                )
                result.append(dict(module=name, kind=kind, path=key, sha256=mapping[key]))
    return result


def map_inputs(record, frozen, external, started):
    for field, is_external in (("frozen_inputs", False), ("external_runtime_inputs", True)):
        mapping = record[field]
        require(type(mapping) is dict, "Complete recognized source/protocol byte map")
        for key, expected in mapping.items():
            check(started)
            require(type(key) is str, "Typed input map path")
            route = Path(key) if is_external else ROOT / key
            require(
                route.is_absolute() if is_external else not Path(key).is_absolute(),
                "Exact external-absolute / ROOT-relative map convention",
            )
            actual = bind(frozen, external, route, expected, started)
            canonical = str(actual) if is_external else actual.relative_to(ROOT).as_posix()
            require(
                canonical == key and (not is_external or not actual.is_relative_to(ROOT)),
                "Canonical source-map path; no aliases or ROOT path in external map",
            )


def protocol_policy(protocol, implementation, plan, started):
    check(started)
    require(
        protocol["schema"] == "box-muller-polar-cdf-bv-protocol-v1"
        and protocol["output"] == SOURCE.relative_to(ROOT).as_posix()
        and protocol["producer_module"]
        == "research.limitation_program_20261001.experiment_box_muller_polar_cdf_bv_v2",
        "Exact original-pair source protocol",
    )
    require(
        protocol["operational_runtime_scope_version"] == 2
        and protocol["original_admission_failure_manifest_SHA256"] == ORIGINAL_FAILURE_SHA
        and protocol["original_root_review_manifest_SHA256"] == ORIGINAL_REVIEW_SHA
        and protocol["previous_failed_preparation_scientific_or_fixture_credit"] == 0,
        "Exact source operational release and zero-credit original admission",
    )
    same(
        [
            protocol[k]
            for k in ("process_CPU_seconds", "admission_process_CPU_seconds", "wall_seconds")
        ],
        [CPU, ADMISSION, WALL],
        "Complete primary fixed budget",
    )
    require(
        protocol["primary_interval_decimal_digits"] == 90
        and protocol["independent_interval_decimal_digits"] == DIGITS
        and protocol["numerical_threads"] == 1
        and protocol["fixture_credit"] == 0,
        "Exact distinct interval precisions, threads and zero fixtures",
    )
    for name in (
        "startup_B_required",
        "pure_Python_mpmath_backend_required",
        "runtime_and_source_frozen_before_kernel_import",
        "full_native_financial_bridge_open",
        "no_numerical_kernel_source_walk_or_bound_executed_in_prepare",
    ):
        require(protocol[name] is True, "Source prospective/runtime scope flag: " + name)
    require(protocol["cosine_512_envelope_computed"] is False, "Native cosine bridge remains open")
    same(
        protocol["immutable_author_sha256"],
        implementation["author_sha256"],
        "Prepared exact author bytes",
    )
    same(
        protocol["method_document_SHA256"],
        implementation["method_document_SHA256"],
        "Held method pins",
    )
    same(
        protocol["selected_source_SHA256"],
        plan["source_bindings_SHA256"],
        "All17 exact source pins",
    )
    same(
        protocol["additional_native_root_provenance_SHA256"],
        ROOT_PINS,
        "Full actual root provenance",
    )
    same(protocol["original_root_owner_manifest_SHA256"], ROOT_OWNERS, "Original root proof owners")
    clock = protocol["clock_policy"]
    require(
        clock["CPU_includes_actual_process_bootstrap"] is True
        and clock["wall_includes_actual_GetProcessTimes_creation"] is True
        and clock["monotonic_origin_derived_from_creation_UTC_observation"] is True
        and type(clock["actual_process_creation_FILETIME_ticks"]) is int,
        "Primary all-inclusive actual process clock",
    )


def source_packet(implementation, frozen, external, started):
    """Verify actual terminal producer bytes without importing or running its code."""
    require(SOURCE.is_dir(), "Actual producer receipt must already exist")
    for marker in ("FAILED_UNSEALED.json", "failure.json"):
        require(not (SOURCE / marker).exists(), "Source failed/partial terminal cannot be audited")
    manifest_path = SOURCE / "manifest.json"
    manifest = read_json(manifest_path, started)
    require(
        manifest["schema"] == "box-muller-polar-cdf-bv-terminal-manifest-v1"
        and manifest["manifest_self_hash_excluded"] is True
        and manifest["terminal_outcome_file"] == "completion_outcome.json"
        and manifest["completed"] is True
        and manifest["budget_censored"] is False
        and type(manifest["passed"]) is bool
        and manifest["original_expected_hashes_waived"] is False
        and manifest["verification_and_output_hashing_before_terminal"] is True,
        "Actual uncensored single source terminal manifest",
    )
    same(
        manifest["historical_global_LIVE_integrity"],
        dict(passed=False, mismatch_references=36, distinct_paths=9, expected_hashes_waived=False),
        "Historical LIVE defects separately retained; no waiver",
    )
    require(
        manifest["archived_selected_receipt_validity_separate"] is True,
        "Selected immutable receipt validity separate from global LIVE",
    )
    files = manifest["files"]
    require(type(files) is dict and 0 < len(files) <= 64, "Finite complete source owned map")
    actual_files, total = set(), 0
    for path in SOURCE.rglob("*"):
        check(started)
        if path.is_file():
            actual = canonical_path(path, started)
            require(actual.is_relative_to(SOURCE), "Source owned byte confinement")
            key = actual.relative_to(SOURCE).as_posix()
            require(key not in actual_files, "No aliased source-owned file")
            actual_files.add(key)
            total += actual.stat().st_size
    require(
        actual_files == set(files) | {"manifest.json"} and total <= 128 * 1024**2,
        "Exact source directory file membership",
    )
    for key, expected in files.items():
        check(started)
        require(
            type(key) is str and key != "manifest.json" and not Path(key).is_absolute(),
            "Receipt-relative source owned map convention",
        )
        path = bind(frozen, external, SOURCE / key, expected, started)
        require(
            path.is_relative_to(SOURCE) and path.relative_to(SOURCE).as_posix() == key,
            "Canonical source-owned path; no traversal or alias",
        )
    bind(frozen, external, manifest_path, sha(manifest_path, started), started)
    map_inputs(manifest, frozen, external, started)
    plan, selected, roots = method_origins(implementation, frozen, external, started)
    same(
        selected,
        read_json(SOURCE / "selected_source_origins.json", started),
        "Independent selected source original-owner membership",
    )
    same(
        roots,
        read_json(SOURCE / "native_root_provenance.json", started),
        "Independent actual root original-owner membership",
    )
    protocol = read_json(SOURCE / "protocol.json", started)
    protocol_policy(protocol, implementation, plan, started)
    for field in ("frozen_inputs", "external_runtime_inputs"):
        require(type(protocol[field]) is dict, "Original complete preparation byte map")
        for key, expected in protocol[field].items():
            check(started)
            require(
                manifest[field].get(key) == expected,
                "Source terminal preserves every prepared expected byte",
            )
    prepared = read_json(SOURCE / "PREPARED_RECEIPT.json", started)
    require(
        prepared["prepared"] is True
        and prepared["terminal"] is False
        and prepared["no_numeric_result_claim"] is True
        and prepared["protocol_sha256"] == sha(SOURCE / "protocol.json", started),
        "Actual immutable source preparation receipt",
    )
    for path in (AUTHOR, PRODUCER_AUTHOR, IMPLEMENTATION, IMPLEMENTATION_DOC, METHOD, METHOD_DOC):
        require(
            sha(SOURCE / "executed_code" / path.name, started) == sha(path, started),
            "Actual source copies retain exact frozen author/method bytes",
        )
    interpreter = read_json(SOURCE / "interpreter.json", started)
    same(interpreter, protocol["interpreter"], "Original prepared interpreter record")
    verify_runtime(interpreter, frozen, external, started)
    summary = read_json(SOURCE / "summary.json", started)
    outcome = read_json(SOURCE / "completion_outcome.json", started)
    passed = manifest["passed"]
    for value in (summary, outcome):
        require(
            value["completed"] is True
            and value["passed"] is passed
            and value["rejection"] is (not passed)
            and value["budget_censored"] is False,
            "Complete uncensored accepted-or-rejected hybrid source outcome",
        )
        require(
            value["new_test_credit"] == 0
            and value["full_G2"] is False
            and value["cost_transfer"] is False
            and value["adoption"] is False,
            "No fixtures/native financial/cost/adoption credit",
        )
    require(
        summary["schema"] == "box-muller-polar-cdf-bv-summary-v1"
        and summary["status"]
        == outcome["status"]
        == ("ideal_hybrid_component_passed" if passed else "rejected_angular_guard")
        and outcome["summary_file"] == "summary.json"
        and outcome["phase"] == "run",
        "Actual source outcome authority and status",
    )
    same(
        summary["complete_actual_pair_counts"],
        {case: count for case, (_, _, count) in CASES.items()},
        "Actual complete30/234 whole-pair inventory",
    )
    require(
        summary["log_coefficients_recomputed"] == 288
        and summary["log_segments"] == 32
        and summary["midpoint_exponent_classes"] == 33
        and summary["all_fixture_credit"] == 0
        and summary["squared_radius_CDF_retained"] is True
        and summary["angular_dollar_certificate_retained"] is passed
        and summary["native_financial_bridge_open"] is True
        and summary["residual_spent_or_reallocated"] is False
        and summary["native_cosine_envelope_computed"] is False
        and summary["basis_or_circuit_or_price_estimator_replays"] == 0
        and summary["source_expected_hashes_waived"] is False,
        "Fixed hybrid-only method and native obligations",
    )
    same(
        outcome["limits_CPU_admission_wall"],
        [CPU, ADMISSION, WALL],
        "Actual source final budget policy",
    )
    for value in (manifest["terminal_budget_observation"], outcome["budget"], summary["budget"]):
        require(
            0 <= value["process_CPU_seconds"] < CPU and 0 <= value["wall_seconds"] < WALL,
            "Actual source terminal observations within hard caps",
        )
    loaded = read_json(SOURCE / "loaded_module_origins.json", started)
    require(type(loaded) is list and loaded, "Actual producer loaded origins retained")
    for record in loaded:
        check(started)
        require(record["kind"] in ("source", "cache"), "Source/cache origin type")
        key, expected = record["path"], record["sha256"]
        mapping = (
            manifest["external_runtime_inputs"]
            if Path(key).is_absolute()
            else manifest["frozen_inputs"]
        )
        require(mapping.get(key) == expected, "Every actual producer loaded origin frozen")
    return plan, summary, protocol


def independent_analytic_derivation():
    """Paper obligations expressed independently of the primary proof prose."""
    return {
        "actual_point_value_BV_convention": [
            (
                "Variation includes the actual value at every point: at a crossing or "
                "atom, both |f(a)-f(a-)| and |f(a+)-f(a)| are charged. Strict-tie "
                "singleton defects therefore have two jumps; no right-continuous "
                "representative replaces the priced value."
            ),
            (
                "For these piecewise smooth conditional functions, write the "
                "left-to-point jump as a closed threshold 1{x>=a} and the "
                "point-to-right jump as an open threshold 1{x>a}. Both threshold "
                "expectation differences are bounded by the same CDF discrepancy D "
                "because the comparison radial/angle law is continuous and one-sided "
                "CDF limits are bounded by D."
            ),
            (
                "The continuous variation and both actual jump variations give the "
                "CDF/BV error <=D*TV with the actual priced point values. The same "
                "finite-jump argument applies on the circle after a cut, and uniform "
                "midpoint D=1/(2N) yields TV/(2N), including extrema ties at midpoint "
                "atoms."
            ),
        ],
        "squared_radius_CDF": [
            (
                "For every original midpoint U, Lhat differs from log(U) by at most "
                "E_L; therefore max(-2Lhat,0) differs from -2log(U) by at most 2E_L, "
                "since positive-part is 1-Lipschitz and -2log(U)>=0."
            ),
            (
                "The raw isqrt divides by Q and rounds the nonnegative square root "
                "down by less than EPS. With true/root upper bound B, squared radius "
                "discrepancy is at most eta=2E_L+2EPS*B+EPS^2."
            ),
            (
                "Uniform midpoint CDF has discrepancy <=1/(2N) from uniform[0,1]. "
                "Exact -2log(U) is Exp(rate1/2), whose interval probability is <= "
                "interval_length/2."
            ),
            (
                "Event inclusions S<=t-eta implies Shat<=t implies S<=t+eta yield "
                "KS(Shat,Exp)<=1/(2N)+eta/2. No order of Shat(U) is needed; sqrt maps "
                "this to a Rayleigh radius CDF bound."
            ),
        ],
        "radial_BV": [
            (
                "Condition on every other variable and the current angle. Every ideal "
                "stock is c_i exp(d_i*r), c_i>0, with unrestricted signed d_i; each "
                "date basket is positive and convex on r>=0."
            ),
            (
                "A strict convex sublevel is one interval, possibly empty or "
                "unbounded. All-date strict survival is the intersection of these "
                "intervals and hence also one interval."
            ),
            (
                "The time/stock average is convex; its positive part above K, scaled "
                "by positive discount, is convex and nonnegative. Cap it at "
                "C=(H-K)*discount, which equals the ideal surviving payoff because "
                "every date basket is <H."
            ),
            (
                "A nonnegative capped convex function on the half-line decreases then "
                "increases, with total variation <=2C. Restricting it to one survival "
                "interval adds at most two endpoint jumps of size C, so payoff "
                "TV<=4C, including strict endpoint ties."
            ),
            (
                "The CDF/BV inequality on [0,infinity) thus costs <=4C*D_S per whole "
                "pair's radius replacement."
            ),
        ],
        "angular_BV": [
            (
                "Condition on other variables after this pair's radius is finite and "
                "replaced. Positive ideal role coefficients give every stock c_i "
                "exp(A_i*cos(theta)+B_i*sin(theta)), c_i>0,A_i>=0,B_i>=0, with "
                "A_i^2+B_i^2<=kappa^2<2."
            ),
            (
                "Put x_i=A_i*c+B_i*s,y_i=-A_i*s+B_i*c,w_i=c_i*exp(x_i). For "
                "first-quadrant s,c>0, y_i^2<=kappa*(s^2*A_i+c^2*B_i) by the "
                "independently checked nonnegative polynomial remainder and "
                "A_i,B_i<=kappa."
            ),
            (
                "At a stationary point, U=sum(w_i*A_i),V=sum(w_i*B_i) satisfy "
                "-s*U+c*V=0. X=sum(w_i*x_i)=c*U+s*V then yields U=c*X,V=s*X, so "
                "sum(w_i*y_i^2)<=kappa*s*c*(s+c)*X<=kappa*X/sqrt(2)<X when X>0."
            ),
            (
                "Consequently every first-quadrant stationary point is a strict "
                "maximum. In quadrantIII x_i<=0 makes basket second "
                "derivative=sum(w_i*(y_i^2-x_i))>0 unless all directions vanish; "
                "quadrantsII andIV have fixed derivative signs."
            ),
            (
                "Derivative continuity plus quadrant endpoint signs gives one "
                "circular maximum and one minimum. If an axis derivative vanishes all "
                "positive-weight directions have that coordinate zero; the one-axis "
                "semicircle case, all-zero directions, zero radius and constant "
                "functions are handled directly."
            ),
            (
                "Every strict threshold indicator has circular TV<=2, including a "
                "strict tie removing an extremal point. A closed finite band can be "
                "two arcs and has TV<=4. The average basket has the same positive "
                "form, so its nonnegative payoff capped at C has circular TV<=2C."
            ),
            (
                "Product variation with nt survival indicators is <=2C+sum_j "
                "C*2=2C*(nt+1). Each current whole-pair angle midpoint replacement "
                "costs <=TV/(2N)=C*(nt+1)/N."
            ),
        ],
        "whole_pair_order_and_open_native_bridge": [
            (
                "Replace a current pair radius first while its current angle may "
                "remain continuous, then replace that pair's ideal angle. Other pair "
                "values only change positive weights; no independence of the pair's "
                "two output coordinates is claimed."
            ),
            (
                "The source supplies exactly30/234 complete pairs, possibly spanning "
                "dates. Uniform positive source-role norm guards apply to every stock "
                "prefix and all fixed pair conditionings; sum per-pair radial and "
                "angular costs once."
            ),
            (
                "These lemmas certify exact unclipped ideal GBM with internal native "
                "Rhat and exact ideal angle. They do not certify rounded native "
                "cosine/product, log-domain clamps, exp/financial floors, barrier "
                "bands or native dollar bias; no AS scalar2C, old Holder, cutoff or "
                "old grid term is transferred."
            ),
        ],
        "full_G2": False,
        "native_financial_bridge_open": True,
        "fixture_credit": 0,
    }


def elapsed(started):
    return dict(process_CPU_seconds=time.process_time(), wall_seconds=time.monotonic() - started)


def copy_exact(source, destination, frozen, external, started):
    source = canonical_path(source, started)
    expected, identity = sha(source, started), fingerprint(source)
    with source.open("rb") as incoming, Path(destination).open("xb") as outgoing:
        while block := incoming.read(1 << 20):
            check(started)
            outgoing.write(block)
            check(started)
    require(fingerprint(source) == identity, "Copy source remains immutable")
    bind(frozen, external, destination, expected, started)


def owned_artifacts(output, started):
    result, total = {}, 0
    for candidate in output.rglob("*"):
        check(started)
        if candidate.is_file():
            path = canonical_path(candidate, started)
            require(
                path.is_relative_to(output) and path.name != "manifest.json",
                "Owned output confinement and no manifest reuse",
            )
            key = path.relative_to(output).as_posix()
            require(key not in result, "No aliased owned output")
            total += path.stat().st_size
            require(len(result) < 64 and total <= 128 * 1024**2, "Finite owned artifact caps")
            result[key] = sha(path, started)
    return result


def seal(output, frozen, external, started, outcome):
    require(
        not (output / "manifest.json").exists()
        and not (output / "FAILED_UNSEALED.json").exists()
        and not (output / "completion_outcome.json").exists(),
        "One exclusive terminal, no retry",
    )
    count = final_fresh(frozen, external, started)
    outcome = dict(
        outcome,
        verification_unique_paths=count,
        budget=elapsed(started),
        limits_CPU_admission_wall=[CPU, ADMISSION, WALL],
        new_test_credit=0,
        all_fixture_credit=0,
        full_G2=False,
        native_financial_bridge_open=True,
        cost_transfer=False,
        adoption=False,
    )
    write_json(output / "completion_outcome.json", outcome, started)
    files = owned_artifacts(output, started)
    check(started)
    write_json(
        output / "manifest.json",
        dict(
            schema="box-muller-polar-cdf-bv-independent-audit-manifest-v1",
            files=files,
            frozen_inputs=frozen,
            external_runtime_inputs=external,
            manifest_self_hash_excluded=True,
            terminal_outcome_file="completion_outcome.json",
            completed=outcome["completed"],
            passed=outcome["passed"],
            budget_censored=outcome["budget_censored"],
            terminal_budget_observation=elapsed(started),
            verification_and_output_hashing_before_terminal=True,
            original_expected_hashes_waived=False,
            historical_global_LIVE_integrity=dict(
                passed=False, mismatch_references=36, distinct_paths=9, expected_hashes_waived=False
            ),
            archived_selected_receipt_validity_separate=True,
        ),
        started,
    )


def retain_failure(output, frozen, external, started, error, phase):
    if not output.exists():
        return  # Root records the real pre-mkdir failure; no fabricated protocol.
    try:
        require(
            not (output / "manifest.json").exists()
            and not (output / "completion_outcome.json").exists(),
            "Partial/existing terminal blocks failure reseal",
        )
        check(started)
        write_json(
            output / "failure.json",
            dict(
                failed=True,
                completed=False,
                passed=False,
                phase=phase,
                error_type=type(error).__name__,
                error=str(error),
                traceback=traceback.format_exc(),
                budget_censored=isinstance(error, BudgetCensoredError),
                new_test_credit=0,
                all_fixture_credit=0,
                budget=elapsed(started),
            ),
            started,
        )
        seal(
            output,
            frozen,
            external,
            started,
            dict(
                completed=False,
                passed=False,
                failed=True,
                rejection=False,
                independent_audit_passed=False,
                ideal_hybrid_component_passed=False,
                budget_censored=isinstance(error, BudgetCensoredError),
                phase=phase,
                failure_file="failure.json",
            ),
        )
    except BaseException:
        # Authoritative constant marker; no scans/hashes after hard exhaustion.
        try:
            with (output / "FAILED_UNSEALED.json").open("xb") as stream:
                stream.write(
                    b'{"failed":true,"completed":false,"passed":false,"budget_censored":true,'
                    b'"new_test_credit":0,"all_fixture_credit":0,"independent_audit_passed":false,'
                    b'"partial_summary_or_manifest_is_not_terminal_success":true,'
                    b'"requires_fresh_version_and_receipt":true}\n'
                )
        except FileExistsError:
            pass


def prepare(output):
    started = start_clock()
    frozen, external, created = {}, {}, False
    try:
        initialize(started)
        require(output == OUTPUT and not output.exists(), "Fresh exact independent receipt")
        require("mpmath" not in sys.modules, "Stdlib-only preparation")
        implementation = implementation_policy(started)
        plan, source_summary, _ = source_packet(implementation, frozen, external, started)
        runtime_record = runtime_inventory(frozen, external, started)
        verify_runtime(runtime_record, frozen, external, started)
        loaded_origins(frozen, external, started)
        verify_maps(frozen, external, started)
        check(started, admission=True)
        output.mkdir()
        created = True
        (output / "executed_code").mkdir()
        for path in (
            AUTHOR,
            PRODUCER_AUTHOR,
            IMPLEMENTATION,
            IMPLEMENTATION_DOC,
            METHOD,
            METHOD_DOC,
        ):
            copy_exact(path, output / "executed_code" / path.name, frozen, external, started)
        write_json(output / "interpreter.json", runtime_record, started)
        count = final_fresh(frozen, external, started)
        check(started, admission=True)
        protocol = dict(
            schema="box-muller-polar-cdf-bv-independent-audit-protocol-v1",
            output=output.relative_to(ROOT).as_posix(),
            source=SOURCE.relative_to(ROOT).as_posix(),
            source_manifest_sha256=sha(SOURCE / "manifest.json", started),
            prepared_UTC=datetime.now(timezone.utc).isoformat(),
            independent_auditor_module="research.limitation_program_20261001.audit_box_muller_polar_cdf_bv_v2",
            frozen_inputs=frozen,
            external_runtime_inputs=external,
            interpreter=runtime_record,
            immutable_author_sha256=implementation["author_sha256"],
            method_document_SHA256=implementation["method_document_SHA256"],
            selected_source_SHA256=plan["source_bindings_SHA256"],
            additional_native_root_provenance_SHA256=ROOT_PINS,
            original_root_owner_manifest_SHA256=ROOT_OWNERS,
            process_CPU_seconds=CPU,
            admission_process_CPU_seconds=ADMISSION,
            wall_seconds=WALL,
            independent_interval_decimal_digits=DIGITS,
            primary_interval_decimal_digits=90,
            numerical_threads=1,
            fixture_credit=0,
            startup_B_required=True,
            pure_Python_mpmath_backend_required=True,
            runtime_and_source_frozen_before_kernel_import=True,
            native_financial_bridge_open=True,
            native_cosine_envelope_computed=False,
            scientific_producer_or_helper_imports=False,
            source_hybrid_guard_passed=source_summary["passed"],
            final_fresh_preparation_verified_paths=count,
            preparation_budget=elapsed(started),
            clock_policy=dict(
                CPU_includes_actual_process_bootstrap=True,
                wall_includes_actual_GetProcessTimes_creation=True,
            ),
            no_source_kernel_proof_interval_or_bound_executed_in_prepare=True,
        )
        write_json(output / "protocol.json", protocol, started)
        write_json(
            output / "PREPARED_RECEIPT.json",
            dict(
                prepared=True,
                terminal=False,
                protocol_sha256=sha(output / "protocol.json", started),
                preparation_budget=elapsed(started),
                no_numeric_result_claim=True,
            ),
            started,
        )
        return {"prepared": True, "terminal": False, "new_test_credit": 0}
    except BaseException as error:
        if created:
            retain_failure(output, frozen, external, started, error, "prepare")
        raise


def audit_protocol_policy(protocol, implementation, plan, source_summary, started):
    check(started)
    require(
        protocol["schema"] == "box-muller-polar-cdf-bv-independent-audit-protocol-v1"
        and protocol["output"] == OUTPUT.relative_to(ROOT).as_posix()
        and protocol["source"] == SOURCE.relative_to(ROOT).as_posix()
        and protocol["independent_auditor_module"]
        == "research.limitation_program_20261001.audit_box_muller_polar_cdf_bv_v2",
        "Exact prepared independent scope",
    )
    same(
        [
            protocol[k]
            for k in ("process_CPU_seconds", "admission_process_CPU_seconds", "wall_seconds")
        ],
        [CPU, ADMISSION, WALL],
        "Fixed all-inclusive independent budget",
    )
    require(
        protocol["independent_interval_decimal_digits"] == DIGITS
        and protocol["primary_interval_decimal_digits"] == 90
        and protocol["numerical_threads"] == 1
        and protocol["fixture_credit"] == 0
        and protocol["source_hybrid_guard_passed"] is source_summary["passed"]
        and protocol["scientific_producer_or_helper_imports"] is False
        and protocol["native_cosine_envelope_computed"] is False,
        "Prepared independent numerical and incomplete bridge scope",
    )
    for name in (
        "startup_B_required",
        "pure_Python_mpmath_backend_required",
        "runtime_and_source_frozen_before_kernel_import",
        "native_financial_bridge_open",
        "no_source_kernel_proof_interval_or_bound_executed_in_prepare",
    ):
        require(protocol[name] is True, "Prepared scope/policy flag")
    same(
        protocol["immutable_author_sha256"],
        implementation["author_sha256"],
        "Frozen executable authors",
    )
    same(
        protocol["method_document_SHA256"],
        implementation["method_document_SHA256"],
        "Held frozen method",
    )
    same(
        protocol["selected_source_SHA256"],
        plan["source_bindings_SHA256"],
        "All17 original selected pins",
    )
    same(
        protocol["additional_native_root_provenance_SHA256"],
        ROOT_PINS,
        "All13 exact native root inputs",
    )
    same(protocol["original_root_owner_manifest_SHA256"], ROOT_OWNERS, "Both root owners")
    require(
        protocol["source_manifest_sha256"] == sha(SOURCE / "manifest.json", started),
        "Prepared source terminal manifest unchanged",
    )
    require(
        protocol["clock_policy"]["CPU_includes_actual_process_bootstrap"] is True
        and protocol["clock_policy"]["wall_includes_actual_GetProcessTimes_creation"] is True,
        "All-inclusive independent process clocks",
    )


def run(output):
    started = start_clock()
    frozen, external, admitted = {}, {}, False
    try:
        initialize(started)
        require(output == OUTPUT and output.is_dir(), "Exact prepared independent output")
        require(
            not any(
                (output / name).exists()
                for name in (
                    "run_started.json",
                    "manifest.json",
                    "FAILED_UNSEALED.json",
                    "failure.json",
                    "completion_outcome.json",
                )
            ),
            "No reused/failed independent run",
        )
        admitted = True
        protocol = read_json(output / "protocol.json", started)
        prepared = read_json(output / "PREPARED_RECEIPT.json", started)
        require(
            prepared["prepared"] is True
            and prepared["terminal"] is False
            and prepared["no_numeric_result_claim"] is True
            and prepared["protocol_sha256"] == sha(output / "protocol.json", started),
            "Actual independent preparation immutable",
        )
        map_inputs(protocol, frozen, external, started)
        for path in (
            output / "protocol.json",
            output / "PREPARED_RECEIPT.json",
            output / "interpreter.json",
        ):
            bind(frozen, external, path, sha(path, started), started)
        implementation = implementation_policy(started)
        plan, source_summary, _ = source_packet(implementation, frozen, external, started)
        audit_protocol_policy(protocol, implementation, plan, source_summary, started)
        runtime_record = read_json(output / "interpreter.json", started)
        same(runtime_record, protocol["interpreter"], "Actual prepared independent runtime")
        verify_runtime(runtime_record, frozen, external, started)
        for path in (
            AUTHOR,
            PRODUCER_AUTHOR,
            IMPLEMENTATION,
            IMPLEMENTATION_DOC,
            METHOD,
            METHOD_DOC,
        ):
            require(
                sha(output / "executed_code" / path.name, started) == sha(path, started),
                "Independent prepared author copies unchanged",
            )
        loaded_origins(frozen, external, started)
        verify_maps(frozen, external, started)
        check(started, admission=True)
        write_json(
            output / "run_started.json",
            dict(
                UTC=datetime.now(timezone.utc).isoformat(),
                process_id=os.getpid(),
                limits_CPU_admission_wall=[CPU, ADMISSION, WALL],
                fixture_credit=0,
            ),
            started,
        )
        require("mpmath" not in sys.modules, "Fresh lazy pure-Python interval import")
        import mpmath as mp

        require(
            mp.__version__ == "1.3.0" and sys.modules["mpmath.libmp.backend"].BACKEND == "python",
            "Actual frozen pure-Python interval backend",
        )
        mp.iv.dps = mp.mp.dps = DIGITS
        loaded_origins(frozen, external, started)
        check(started, admission=True)
        binding, rows, ln2 = source_inventory(started)
        same(
            binding,
            read_json(SOURCE / "source_binding.json", started),
            "Independent actual whole-source and full native root binding",
        )
        write_json(output / "independent_source_binding.json", binding, started)
        check(started, admission=True)
        envelope, own_B, own_D = log_certificate(mp, rows, ln2, started)
        primary_B, primary_D = compare_log_record(
            read_json(SOURCE / "log_radius_envelope.json", started), envelope, started
        )
        write_json(output / "independent130_log_radius_envelope.json", envelope, started)
        check(started, admission=True)
        identities = audit_symbolic_identity(
            read_json(SOURCE / "method_obligations.json", started), started
        )
        write_json(
            output / "independent_method_derivation.json",
            dict(
                exact_formal_identity_audit=identities,
                analytic_derivation=independent_analytic_derivation(),
            ),
            started,
        )
        check(started, admission=True)
        component_passed, guards, prices = audit_guard_and_prices(
            mp, binding, primary_B, primary_D, own_B, own_D, started
        )
        require(
            component_passed is source_summary["passed"],
            "Actual source guard outcome independently reproduced",
        )
        write_json(output / "independent_angular_guards.json", guards, started)
        if component_passed:
            write_json(output / "independent130_ideal_hybrid_bounds.json", prices, started)
        verify_runtime(runtime_record, frozen, external, started)
        write_json(
            output / "loaded_module_origins.json",
            loaded_origins(frozen, external, started),
            started,
        )
        summary = dict(
            schema="box-muller-polar-cdf-bv-independent-audit-summary-v1",
            completed=True,
            passed=True,
            independent_audit_passed=True,
            ideal_hybrid_component_passed=component_passed,
            source_passed=component_passed,
            source_rejection_retained=not component_passed,
            budget_censored=False,
            independently_recomputed_log_coefficients=288,
            log_segments=32,
            exact_midpoint_exponent_classes=33,
            complete_actual_pair_counts={case: count for case, (_, _, count) in CASES.items()},
            independent_interval_decimal_digits=DIGITS,
            producer_or_helper_imported=False,
            exact_formal_identities_independently_checked=5,
            squared_radius_CDF_retained=True,
            angular_dollar_certificate_retained=component_passed,
            new_test_credit=0,
            all_fixture_credit=0,
            basis_or_circuit_or_price_estimator_replays=0,
            full_G2=False,
            native_financial_bridge_open=True,
            native_cosine_envelope_computed=False,
            residual_spent_or_reallocated=False,
            cost_transfer=False,
            adoption=False,
            source_expected_hashes_waived=False,
            budget=elapsed(started),
        )
        write_json(output / "summary.json", summary, started)
        seal(
            output,
            frozen,
            external,
            started,
            dict(
                completed=True,
                passed=True,
                independent_audit_passed=True,
                ideal_hybrid_component_passed=component_passed,
                source_rejection_retained=not component_passed,
                budget_censored=False,
                phase="run",
                summary_file="summary.json",
            ),
        )
        return {
            "independent_audit_passed": True,
            "ideal_hybrid_component_passed": component_passed,
            "new_test_credit": 0,
            "full_G2": False,
            "native_financial_bridge_open": True,
        }
    except BaseException as error:
        if admitted:
            retain_failure(output, frozen, external, started, error, "run")
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("prepare", "run"))
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = (ROOT / args.output).resolve()
    require(output == OUTPUT, "Only exact fresh independent receipt")
    result = prepare(output) if args.operation == "prepare" else run(output)
    print(json.dumps(result, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    main()
