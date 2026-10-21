"""Independent130 original Box-Muller native financial bridge, author-only.

No producer/helper imports, AS theorem or cost transfer. Preparation requires
actual passed polar packets pinned by root; null pins block admission. Every
future source/interval/proof operation and terminal byte check stays within the
fixed180/150/600 clocks. No code kernel has executed during authoring.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter
import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
from fractions import Fraction
from math import factorial
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
SOURCE = PROGRAM / "A02_BM_native_financial_bridge_run001"
OUTPUT = PROGRAM / "A02_BM_native_financial_bridge_audit_run001"
AUTHOR = RESEARCH / "audit_box_muller_native_financial_bridge.py"
PRODUCER_AUTHOR = RESEARCH / "experiment_box_muller_native_financial_bridge.py"
OLD_METHOD = RESEARCH / "box_muller_native_financial_bridge_preflight.json"
OLD_METHOD_DOC = RESEARCH / "BOX_MULLER_NATIVE_FINANCIAL_BRIDGE_PREFLIGHT.md"
METHOD = RESEARCH / "box_muller_native_financial_bridge_preflight_v2.json"
METHOD_DOC = RESEARCH / "BOX_MULLER_NATIVE_FINANCIAL_BRIDGE_PREFLIGHT_V2.md"
IMPLEMENTATION = RESEARCH / "box_muller_native_financial_bridge_implementation_preflight.json"
IMPLEMENTATION_DOC = RESEARCH / "BOX_MULLER_NATIVE_FINANCIAL_BRIDGE_IMPLEMENTATION_PREFLIGHT.md"
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
OLD_METHOD_SHA = "32010ceaf2990583e4f27b8be833e8c1cf698fff59afa2ef3bdcab65c4dac9be"
OLD_METHOD_DOC_SHA = "9619262b469a2f40a30807e2bd0b12d80f8732b72a0af4098b32f01d1f28ec16"
METHOD_SHA = "263dbcd26beea4d4337e67f648e667663a0b666ee4a4986b69914c44645c2ce8"
METHOD_DOC_SHA = "b999f56da7eeb68ddee96e14260d96dd99a69cadf3157b2524908a3960b53c74"
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

POLAR = PROGRAM / "A02_polar_cdf_bv_run003"
POLAR_AUDIT = PROGRAM / "A02_polar_cdf_bv_audit_run003"
POLAR_MANIFESTS = {
    "results/limitation_program_20261001/A02_polar_cdf_bv_run003/manifest.json": (
        "86dcd6b400233b58f62d4197127e38c6d2598c05e1903d207b0947168b326a05"
    ),
    "results/limitation_program_20261001/A02_polar_cdf_bv_audit_run003/manifest.json": (
        "75ed7d7d6d5b929571d64d8fa54d53f6bf146c283d18133a5d191ac612724eb9"
    ),
}
ALLOWANCE = Fraction(11, 2000)
EXPONENTS = tuple(range(-17, 13))


class BudgetCensoredError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check(started, *, admission=False):
    cpu, wall = time.process_time(), time.monotonic() - started
    if cpu >= (ADMISSION if admission else CPU) or wall >= WALL:
        raise BudgetCensoredError("Fixed independent native-financial CPU/wall censor")
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
                    "research.limitation_program_20261001.audit_box_muller_native_financial_bridge",
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


def venv_adjacent_runtime(prefix, started):
    """Exact admitted prefix entries; capture adjacent files, caches and real packages."""
    paths, membership = set(), []
    for candidate in sorted(prefix.iterdir()):
        check(started)
        actual = canonical_path(candidate, started)
        require(
            actual == candidate.absolute() and actual.parent == prefix,
            "Adjacent actual venv entry is direct and has no redirected alias",
        )
        if candidate.is_file():
            kind = "file"
            require(actual.parent == prefix, "Actual adjacent venv regular file")
            paths.add(actual)
        else:
            require(candidate.is_dir(), "Actual adjacent venv file or directory")
            kind = "directory"
            importable_package = any(
                (candidate / name).is_file() for name in ("__init__.py", "__init__.pyc")
            )
            if candidate.name == "__pycache__" or importable_package:
                require(candidate.name not in ("Lib", "Scripts"), "No ambiguous venv package root")
                paths.add(actual)
        membership.append([candidate.name, kind])
    return sorted(paths), sorted(membership)


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
    adjacent_paths, adjacent_membership = venv_adjacent_runtime(prefix, started)
    roots.extend(adjacent_paths)
    for path in (ROOT / "research/__init__.py", RESEARCH / "__init__.py"):
        if path.is_file():
            roots.append(path)
    for path in (ROOT / "research/__init__.py", RESEARCH / "__init__.py", AUTHOR, PRODUCER_AUTHOR):
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
    allowed_roots = {ROOT, prefix, site_root, BASE_PREFIX, *BASE_TREES}
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
        exact_sys_prefix_search_path_admitted=True,
        venv_adjacent_runtime_paths=[str(path) for path in adjacent_paths],
        venv_root_directory_membership=adjacent_membership,
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
    prefix = canonical_path(sys.prefix, started)
    require(
        record["exact_sys_prefix_search_path_admitted"] is True,
        "Only exact isolated venv-prefix search root additionally admitted",
    )
    adjacent_paths, adjacent_membership = venv_adjacent_runtime(prefix, started)
    same(
        [str(path) for path in adjacent_paths],
        record["venv_adjacent_runtime_paths"],
        "Exact adjacent venv runtime roots",
    )
    same(
        adjacent_membership,
        record["venv_root_directory_membership"],
        "Exact finite venv-root directory membership",
    )
    same(
        [str(path) for path in bootstrap_runtime_paths(site_root, started)],
        record["bootstrap_hook_and_loaded_venv_paths"],
        "Actual complete startup hook membership",
    )
    allowed_sys_roots = {ROOT, prefix, site_root, BASE_PREFIX, *BASE_TREES}
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


def word72(bounds):
    require(
        type(bounds) in (tuple, list)
        and len(bounds) == 2
        and all(type(v) is int for v in bounds)
        and -(1 << 71) <= bounds[0] <= bounds[1] < 1 << 71,
        "Every actual stored signed72 intermediate safe",
    )
    return tuple(bounds)


def multiply72(a, b, *, square=False):
    products = [x * y for x in a for y in b]
    if square:
        products = [x * x for x in a]
        if a[0] <= 0 <= a[1]:
            products.append(0)
    lo, hi = min(products), max(products)
    require(-(1 << 143) <= lo <= hi < 1 << 143, "Actual full signed144 product safe")
    return word72((lo // Q, hi // Q))


def ceiling(value):
    value = Fraction(value)
    return -((-value.numerator) // value.denominator)


def cosine_certificate(mp, table, B, started):
    require(
        len(table) == 64 and all(len(row) == 8 for row in table), "All512 original cos literals"
    )
    radius, pi = Fraction(1, 128), mp.iv.pi
    checks, row_errors, largest = [], [], Fraction(0)
    for row_index, row in enumerate(table):
        check(started)
        center = Fraction(2 * row_index + 1, 128)
        errors = []
        for degree, raw in enumerate(row):
            check(started)
            signed_coefficient(raw)
            truth = endpoints(
                (2 * pi) ** degree
                / factorial(degree)
                * mp.iv.cos(2 * pi * outward(mp, center) + degree * pi / 2)
            )
            error = max(abs(Fraction(raw, Q) - value) for value in truth)
            # Actual float-built coefficients can cross an exact rounding boundary.
            # The whole actual discrepancy is paid; no half-ULP predicate is assumed.
            errors.append(error)
            checks.append(
                dict(
                    row=row_index,
                    degree=degree,
                    raw=raw,
                    exact_coefficient_enclosure=[encode(v) for v in truth],
                    literal_error_upper=encode(error),
                )
            )
        row_errors.append(
            sum((error * radius**degree for degree, error in enumerate(errors)), Fraction(0))
        )
        bound = abs(Fraction(row[-1], Q))
        largest = max(largest, bound)
        for raw in reversed(row[:-1]):
            product = bound * radius
            require(product * Q**2 < 1 << 143, "Native cosine full signed144 Horner product")
            bound = product + EPS + abs(Fraction(raw, Q))
            largest = max(largest, product + EPS, bound)
            require(bound * Q < 1 << 71, "Every native cosine stored72 Horner intermediate")
    remainder = endpoints((2 * pi * outward(mp, radius)) ** 8 / factorial(8))[1]
    coefficients = max(row_errors)
    floors = EPS * sum((radius**degree for degree in range(7)), Fraction(0))
    error = remainder + coefficients + floors
    delta = B * error + EPS
    native_z = B * (1 + error) + EPS
    radius_raw, cosine_raw = ceiling(B * Q), ceiling((1 + error) * Q)
    require(
        radius_raw * cosine_raw < 1 << 143 and ceiling(native_z * Q) < 1 << 71,
        "Actual final radius product144 and normal stored72 safe",
    )
    return (
        dict(
            interval_digits=DIGITS,
            coefficient_count=512,
            coefficient_checks=checks,
            cosine_table_remainder_upper=encode(remainder),
            cosine_table_literal_rounding_upper=encode(coefficients),
            cosine_table_floor_upper=encode(floors),
            cosine_table_error_upper=encode(error),
            cosine_Horner_maximum_magnitude=encode(largest),
            internal_radius_upper=encode(B),
            normal_coordinate_error_upper=encode(delta),
            native_normal_absolute_upper=encode(native_z),
            coefficient_half_ULP_assumed=False,
            actual_all512_discrepancies_paid=True,
            final_signed_radius_product_floor_paid=True,
            direct_cos_2pi_unit_turns=True,
            exact_positive_sine_three_quarter_turn_wrap=True,
            old_radius_Holder_or_grid_term_added=False,
        ),
        delta,
        native_z,
    )


def stock_templates(binding, case, started):
    target = read_json(PROGRAM / "A10_coefficient_run001" / case / "min-depth/target.json", started)
    graph = GraphAudit(target, started)
    roles = binding["cases"][case]["financial_roles"]
    scopes = []
    for witness in roles["prefix_witnesses"]:
        check(started)
        stock = witness["stock"]
        p, k = graph.node(stock, "shift")["args"]
        scaled = graph.node(k, "bits", {"shift": 40, "width": 72, "signed": True})["args"][0]
        reducer = graph.node(scaled, "cmul")
        clipped, inverse = reducer["args"][0], reducer["params"]["c"]
        require(
            inverse > 0 and graph.clamp(clipped) == witness["raw_log"],
            "Actual positive reduction and raw prefix",
        )
        pending, visited, candidates = [p], set(), set()
        while pending:
            value = pending.pop()
            if value in visited:
                continue
            visited.add(value)
            node = graph.node(value)
            if node["op"] == "sub":
                candidates.add(value)
            else:
                require(
                    node["op"] in ("const", "add", "mul"),
                    "Exact native Estrin-only polynomial closure",
                )
                pending.extend(node["args"])
        require(len(candidates) == 1, "One stock remainder variable")
        remainder = next(iter(candidates))
        left, right = graph.node(remainder, "sub")["args"]
        ln2_node = graph.node(right, "cmul")
        ln2 = ln2_node["params"]["c"]
        require(left == clipped and ln2 > 0, "Actual remainder and positive ln2 coefficient")
        expanded = graph.node(
            ln2_node["args"][0], "bits", {"shift": -40, "width": 72, "signed": False}
        )["args"][0]
        require(expanded == k, "Same signed integer k is converted exactly to f40")
        ordered_values = {clipped: ["clipped-native-word"]}
        closure, pending_ordered = set(), [stock]
        while pending_ordered:
            check(started)
            value = pending_ordered.pop()
            if value == clipped or value in closure:
                continue
            closure.add(value)
            pending_ordered.extend(graph.node(value)["args"])
        for value in sorted(closure):
            check(started)
            native = graph.node(value)
            ordered_values[value] = [
                native["op"],
                native["params"],
                [ordered_values[arg] for arg in native["args"]],
            ]
        support_signature = hashlib.sha256(
            json.dumps(ordered_values[stock], sort_keys=True).encode()
        ).hexdigest()
        values, labels = {}, {remainder: "remainder"}
        for value in sorted(visited - {remainder}):
            check(started)
            node = graph.node(value)
            children = sorted(labels[child] for child in node["args"])
            signature = (node["op"], graph.constant(value) if node["op"] == "const" else children)
            labels[value] = hashlib.sha256(
                json.dumps(signature, separators=(",", ":")).encode()
            ).hexdigest()
            values[value] = node
        scopes.append(
            dict(
                stock=stock,
                raw_log=witness["raw_log"],
                asset=witness["asset"],
                date=witness["date"],
                clipped=clipped,
                k=k,
                scaled_reduction=scaled,
                polynomial=p,
                remainder=remainder,
                ln2_scaled=right,
                k_f40=ln2_node["args"][0],
                inverse_ln2_raw=inverse,
                ln2_raw=ln2,
                polynomial_signature=labels[p],
                actual_original_support_signature=support_signature,
                full_stock_node_ids=sorted(closure),
                polynomial_node_ids=sorted(values),
                polynomial_node_labels={str(v): labels[v] for v in values},
            )
        )
    require(
        len(scopes) == CASES[case][0] * CASES[case][1]
        and len({row["polynomial_signature"] for row in scopes}) == 1
        and len({(row["inverse_ln2_raw"], row["ln2_raw"]) for row in scopes}) == 1,
        "Every original stock binds the same commutative actual arithmetic template",
    )
    return graph, roles, scopes


def native_polynomial(graph, scope, raw_range, started):
    variable = scope["remainder"]
    values = {variable: word72(raw_range)}
    dense = {variable: [Fraction(0), Fraction(1)]}
    errors = {variable: Fraction(0)}
    rho = Fraction(max(abs(v) for v in raw_range), Q)
    records = []
    for value in scope["polynomial_node_ids"]:
        check(started)
        node = graph.node(value)
        if node["op"] == "const":
            constant = graph.constant(value)
            values[value] = word72((constant, constant))
            coefficients, error = [Fraction(constant, Q)], Fraction(0)
        else:
            a, b = node["args"]
            left, right = dense[a], dense[b]
            ea, eb = errors[a], errors[b]
            if node["op"] == "add":
                coefficients = [Fraction(0)] * max(len(left), len(right))
                for degree, coefficient in enumerate(left):
                    coefficients[degree] += coefficient
                for degree, coefficient in enumerate(right):
                    coefficients[degree] += coefficient
                error = ea + eb
                values[value] = word72((values[a][0] + values[b][0], values[a][1] + values[b][1]))
            else:
                require(node["op"] == "mul", "Exact polynomial multiplication")
                coefficients = [Fraction(0)] * (len(left) + len(right) - 1)
                for i, ca in enumerate(left):
                    for j, cb in enumerate(right):
                        coefficients[i + j] += ca * cb
                ma = sum(
                    (abs(coefficient) * rho**degree for degree, coefficient in enumerate(left)),
                    Fraction(0),
                )
                mb = sum(
                    (abs(coefficient) * rho**degree for degree, coefficient in enumerate(right)),
                    Fraction(0),
                )
                error = ea * mb + eb * ma + ea * eb + EPS
                require(
                    (ma + ea) * (mb + eb) * Q**2 < 1 << 143,
                    "Every actual polynomial magnitude product144",
                )
                values[value] = multiply72(values[a], values[b], square=a == b)
        require(len(coefficients) <= 13, "Bounded original degree12 polynomial")
        magnitude = (
            sum(
                (abs(coefficient) * rho**degree for degree, coefficient in enumerate(coefficients)),
                Fraction(0),
            )
            + error
        )
        require(magnitude * Q < 1 << 71, "All eager polynomial magnitude stored72")
        dense[value], errors[value] = coefficients, error
        records.append(
            dict(
                value=value,
                signature=scope["polynomial_node_labels"][str(value)],
                primitive=node["op"],
                raw_bounds=list(values[value]),
                magnitude_upper=encode(magnitude),
                floor_error_upper=encode(error),
            )
        )
    coefficients = dense[scope["polynomial"]]
    require(
        len(coefficients) == 13
        and all(
            coefficient > 0 and (coefficient * Q).denominator == 1 for coefficient in coefficients
        ),
        "All13 actual positive literal coefficients",
    )
    literal_error = sum(
        (
            abs(coefficient - Fraction(1, factorial(degree))) * rho**degree
            for degree, coefficient in enumerate(coefficients)
        ),
        Fraction(0),
    )
    return dict(
        raw_bounds=list(values[scope["polynomial"]]),
        radius=encode(rho),
        floor_error_upper=encode(errors[scope["polynomial"]]),
        literal_error_upper=encode(literal_error),
        actual_coefficients_raw=[int(coefficient * Q) for coefficient in coefficients],
        steps=records,
    )


def stock_certificate(mp, graph, roles, scopes, started):
    low, high = roles["actual_clamps"]
    reference = scopes[0]
    inverse, ln2 = reference["inverse_ln2_raw"], reference["ln2_raw"]
    domain = (low * inverse // Q**2, high * inverse // Q**2)
    require(
        EXPONENTS[0] <= domain[0] <= domain[1] <= EXPONENTS[-1],
        "Actual exponent domain in unchanged30 superset",
    )
    require(
        abs(low * inverse) < 1 << 143 and abs(high * inverse) < 1 << 143,
        "Both actual clipped-input reduction product144 extremes",
    )
    word72((low * inverse // Q, high * inverse // Q))
    true_ln2 = endpoints(mp.iv.log(outward(mp, 2)))
    ln_error = max(abs(Fraction(ln2, Q) - value) for value in true_ln2)
    rows, next_raw, maximum_alpha, stock_lo, stock_hi = [], low, Fraction(0), None, None
    token_union = {}
    for k in EXPONENTS:
        check(started)
        first = max(low, ceiling(Fraction(k * Q**2, inverse)))
        last = min(high, ceiling(Fraction((k + 1) * Q**2, inverse)) - 1)
        if first > last:
            rows.append(dict(k=k, empty=True))
            continue
        require(
            first == next_raw and first * inverse // Q**2 == last * inverse // Q**2 == k,
            "Every occupied clipped integer class without a gap or overlap",
        )
        next_raw = last + 1
        word72((k * Q, k * Q))
        require(abs(k * Q * ln2) < 1 << 143, "Exact integer k*ln2 native product144")
        remainder = word72((first - k * ln2, last - k * ln2))
        model = native_polynomial(graph, reference, remainder, started)
        radius = rational(model["radius"])
        taylor = endpoints(
            mp.iv.exp(outward(mp, radius)) * outward(mp, radius**13 / factorial(13))
        )[1]
        E = rational(model["floor_error_upper"]) + rational(model["literal_error_upper"]) + taylor
        exp_minus = endpoints(mp.iv.exp(outward(mp, -Fraction(remainder[0], Q))))[1]
        alpha = endpoints(
            mp.iv.exp(outward(mp, abs(k) * ln_error)) * outward(mp, 1 + E * exp_minus) - 1
        )[1]
        require(0 <= alpha < 1, "Uniform actual stock relative envelope guard")
        maximum_alpha = max(maximum_alpha, alpha)
        pmin, pmax = model["raw_bounds"]
        require(pmin > 0, "Every original native stock polynomial positive")
        stock_range = word72((pmin << k, pmax << k) if k >= 0 else (pmin >> -k, pmax >> -k))
        stock_lo = stock_range[0] if stock_lo is None else min(stock_lo, stock_range[0])
        stock_hi = stock_range[1] if stock_hi is None else max(stock_hi, stock_range[1])
        for step in model["steps"]:
            token, bounds = step["signature"], step["raw_bounds"]
            old = token_union.get(token, bounds)
            token_union[token] = [min(old[0], bounds[0]), max(old[1], bounds[1])]
        rows.append(
            dict(
                k=k,
                empty=False,
                clipped_raw_bounds=[first, last],
                remainder_raw_bounds=list(remainder),
                native_polynomial=model,
                degree12_Taylor_remainder_upper=encode(taylor),
                total_polynomial_error_upper=encode(E),
                relative_alpha_upper=encode(alpha),
                stock_raw_bounds=list(stock_range),
            )
        )
    require(
        next_raw == high + 1 and len(rows) == 30,
        "Entire clipped integer union across fixed30 classes",
    )
    high_k = high * inverse // Q**2
    point = native_polynomial(graph, reference, (high - high_k * ln2,) * 2, started)
    require(
        point["raw_bounds"][0] == point["raw_bounds"][1],
        "Exact native upper-clamp stock integer evaluation",
    )
    p = point["raw_bounds"][0]
    native_upper = p << high_k if high_k >= 0 else p >> -high_k
    word72((native_upper, native_upper))
    return dict(
        clamp_raw_bounds=[low, high],
        inverse_ln2_raw=inverse,
        ln2_raw=ln2,
        ln2_true_enclosure=[encode(v) for v in true_ln2],
        ln2_literal_error_upper=encode(ln_error),
        fixed_exponent_classes=list(EXPONENTS),
        actual_exponent_domain=list(domain),
        class_count=30,
        classes=rows,
        alpha_upper=encode(maximum_alpha),
        beta_upper=encode(EPS),
        native_stock_raw_bounds=[stock_lo, stock_hi],
        native_upper_clamp_stock_raw=native_upper,
        polynomial_template_signature=reference["polynomial_signature"],
        all_actual_stock_bindings=scopes,
        polynomial_token_raw_union=token_union,
        original_degree12_Estrin_no_AS_certificate_transfer=True,
    )


def raw_log_certificate(mp, graph, roles, normals, native_z, delta, B, started):
    assets, dates = roles["assets"], roles["dates"]
    true_a = endpoints(mp.iv.sqrt(outward(mp, Fraction(9, 100 * dates) * Fraction(2, 5))))
    true_b = endpoints(mp.iv.sqrt(outward(mp, Fraction(9, 100 * dates) * Fraction(3, 5))))
    true_initial = endpoints(mp.iv.log(outward(mp, 100)))
    a, b = [Fraction(roles[name], Q) for name in ("actual_common_literal", "actual_idio_literal")]
    mu = Fraction(roles["actual_drift_literal"], Q)
    initial = Fraction(roles["actual_initial_literal"], Q)
    ea, eb = max(abs(a - v) for v in true_a), max(abs(b - v) for v in true_b)
    emu = abs(mu - Fraction(-3, 200 * dates))
    e0 = max(abs(initial - v) for v in true_initial)
    increment = (abs(a) + abs(b)) * delta + (ea + eb) * B + emu + 2 * EPS
    require(
        len(normals) == dates * (assets + 1) and len(set(normals)) == len(normals),
        "Complete distinct actual native normal roots from pair binder",
    )
    nbound = ceiling(native_z * Q)
    values = {value: word72((-nbound, nbound)) for value in normals}
    work, requested = [], set()
    for witness in roles["prefix_witnesses"]:
        work.append(witness["raw_log"])
    while work:
        value = work.pop()
        if value in values or value in requested:
            continue
        requested.add(value)
        node = graph.node(value)
        require(node["op"] in ("const", "add", "cmul"), "All eager raw-prefix arithmetic only")
        work.extend(node["args"])
    records = []
    for value in sorted(requested):
        check(started)
        node = graph.node(value)
        if node["op"] == "const":
            v = graph.constant(value)
            bounds = word72((v, v))
        elif node["op"] == "add":
            left, right = (values[child] for child in node["args"])
            bounds = word72((left[0] + right[0], left[1] + right[1]))
        else:
            c = signed_coefficient(node["params"]["c"])
            bounds = multiply72(values[node["args"][0]], (c, c))
        values[value] = bounds
        records.append(dict(value=value, primitive=node["op"], raw_bounds=list(bounds)))
    return dict(
        assets=assets,
        dates=dates,
        actual_common_raw=roles["actual_common_literal"],
        actual_idio_raw=roles["actual_idio_literal"],
        actual_drift_raw=roles["actual_drift_literal"],
        actual_initial_raw=roles["actual_initial_literal"],
        true_common_enclosure=[encode(v) for v in true_a],
        true_idio_enclosure=[encode(v) for v in true_b],
        true_initial_enclosure=[encode(v) for v in true_initial],
        common_literal_error_upper=encode(ea),
        idio_literal_error_upper=encode(eb),
        drift_literal_error=encode(emu),
        initial_literal_error_upper=encode(e0),
        paid_increment_error_upper=encode(increment),
        date_log_error_upper=[encode(e0 + j * increment) for j in range(1, dates + 1)],
        actual_raw_prefix_word_guards=records,
        native_normal_absolute_upper=encode(native_z),
        every_original_driver_once=True,
        every_stored_partial_sum_and_product_safe=True,
        additive_rounding_zero_only_after_no_wrap=True,
        source_reset_or_AS_endpoint_used=False,
    ), values


def original_support(graph, roles, scopes, case, started):
    """Independently bind existing universal support to the exact current source."""
    assets, dates, _ = CASES[case]
    original = read_json(PROGRAM / "E03_support_run001" / (case + "_certificate.json"), started)
    audit = read_json(PROGRAM / "E03_support_audit_run002" / (case + "_audit.json"), started)
    stocks = sorted(row["stock"] for row in scopes)
    same(sorted(original["stock_ids"]), stocks, "Original support stock inventory")
    same(original["target_output"], graph.target["outputs"], "Source-identical financial output")
    require(
        original["complete_builder_equality"] is True
        and original["all_original_uniform_word_patterns"] is True
        and original["stock_support"]["all_clipped_integer_inputs"] is True
        and original["stock_support"]["positive_and_no_native_overflow"] is True
        and original["all_stock_tree_sums_no_overflow"] is True
        and audit["passed"] is True
        and audit["assets"] == assets
        and audit["dates"] == dates
        and audit["actual_stock_templates_checked"] == len(stocks)
        and audit["all_stock_native_intermediates_no_overflow"] is True
        and audit["all_actual_sum_max_average_subtract_discount_nodes_safe"] is True
        and audit["finite_samples_used"] is False
        and audit["new_financial_gate_replays"] == 0,
        "Exact original universal stock support and independent structural arithmetic proof",
    )
    require(
        all(
            row["actual_original_support_signature"] == audit["actual_stock_template_signature"]
            for row in scopes
        ),
        "Every actual ordered stock template matches original independent support",
    )
    same(
        original["clipped_log_integer_bounds"],
        roles["actual_clamps"],
        "Original signed clamp literals",
    )
    same(
        [original["literal_inverse_ln2"], original["literal_ln2"]],
        [scopes[0]["inverse_ln2_raw"], scopes[0]["ln2_raw"]],
        "Exact original stock reduction literals",
    )
    alive, payoff, zero = graph.node(graph.target["outputs"]["Y"], "select")["args"]
    graph.constant(zero, 0)
    discount = graph.node(payoff, "cmul")
    positive = graph.node(discount["args"][0], "positive")
    average, strike = graph.node(positive["args"][0], "sub")["args"]
    graph.constant(strike, 100 * Q)
    average_node = graph.node(average, "cmul")
    c_average, c_discount = average_node["params"]["c"], discount["params"]["c"]
    graph.constant(graph.node(alive, "lt")["args"][1], 140 * Q)
    require(
        0 < c_discount <= Q and c_average == nearest_fraction(Fraction(Q, assets * dates)),
        "Actual rounded whole-stock average and nonexpansive positive discount",
    )
    for basket in roles["baskets"]:
        graph.node(basket["basket"], "cmul", {"c": Q // assets})
    same(
        [
            original[key]
            for key in (
                "basket_coefficient",
                "average_coefficient",
                "discount_coefficient",
                "strict_barrier_raw",
                "strike_raw",
            )
        ],
        [Q // assets, c_average, c_discount, 140 * Q, 100 * Q],
        "Exact native financial literal inventory",
    )
    # floor(S/na)<Hraw, with integral Hraw, implies S<=na*Hraw-1.
    # Sum across dates BEFORE rounding the Asian average, exactly as actual SSA.
    total = dates * (assets * 140 * Q - 1)
    upper_average = total * c_average // Q
    cap_raw = max(0, upper_average - 100 * Q) * c_discount // Q
    same(
        original["payoff_raw_bounds"],
        [0, cap_raw],
        "Fresh native support from strict integer survival",
    )
    same(audit["payoff_raw_bounds"], [0, cap_raw], "Independent original native support agrees")
    require(0 <= cap_raw < 40 * Q, "Original native financial output below40 dollars")
    return dict(
        certificate=original,
        independent_support_audit=audit,
        stock_raw_support_bounds=[
            original["stock_support"]["lower"],
            original["stock_support"]["upper"],
        ],
        native_cap_upper=encode(Fraction(cap_raw, Q)),
        actual_average_literal=c_average,
        actual_discount_literal=c_discount,
        strict_surviving_unrounded_stock_sum_raw_upper=total,
        strict_integer_survival_sum_proved=True,
        original_universal_support_source_identical=True,
        historical_builder_or_AS241_certificate_imported=False,
    )


def eager_financial_safety(graph, roles, scopes, stock, raw_values, normals, started):
    """Check all eagerly emitted financial values, including dead Estrin powers."""
    values = dict(raw_values)
    sampler = set()
    for value in normals:
        sampler.update(graph.ancestors(value))
    low, high = roles["actual_clamps"]
    inverse, ln2 = scopes[0]["inverse_ln2_raw"], scopes[0]["ln2_raw"]
    k_min, k_max = stock["actual_exponent_domain"]
    occupied = [row for row in stock["classes"] if not row["empty"]]
    r_min = min(row["remainder_raw_bounds"][0] for row in occupied)
    r_max = max(row["remainder_raw_bounds"][1] for row in occupied)
    for scope in scopes:
        check(started)
        values[scope["clipped"]] = word72((low, high))
        values[scope["scaled_reduction"]] = multiply72((low, high), (inverse, inverse))
        values[scope["k"]] = word72((k_min, k_max))
        values[scope["k_f40"]] = word72((k_min * Q, k_max * Q))
        values[scope["ln2_scaled"]] = word72((k_min * ln2, k_max * ln2))
        values[scope["remainder"]] = word72((r_min, r_max))
        values[scope["stock"]] = word72(stock["native_stock_raw_bounds"])
        for value in scope["polynomial_node_ids"]:
            signature = scope["polynomial_node_labels"][str(value)]
            values[value] = word72(stock["polynomial_token_raw_union"][signature])
    records = []
    for value in sorted(graph.nodes):
        check(started)
        node = graph.node(value)
        op = node["op"]
        if op == "const":
            constant = graph.constant(value)
            values.setdefault(value, word72((constant, constant)))
        if value in values:
            records.append(
                dict(
                    value=value,
                    primitive=op,
                    raw_bounds=list(values[value]),
                    boundary_or_preproved=True,
                )
            )
            continue
        if value in sampler:
            continue
        require(
            len(node["out"]) == 1 and all(child in values for child in node["args"]),
            "Every non-sampler eager financial dependency is explicitly bounded",
        )
        args = [values[child] for child in node["args"]]
        if op == "add":
            bound = (args[0][0] + args[1][0], args[0][1] + args[1][1])
        elif op == "sub":
            bound = (args[0][0] - args[1][1], args[0][1] - args[1][0])
        elif op == "mul":
            bound = multiply72(args[0], args[1], square=node["args"][0] == node["args"][1])
        elif op == "cmul":
            literal = signed_coefficient(node["params"]["c"])
            bound = multiply72(args[0], (literal, literal))
        elif op == "lt":
            bound = (int(args[0][1] < args[1][0]), int(args[0][0] < args[1][1]))
        elif op == "select":
            require(0 <= args[0][0] <= args[0][1] <= 1, "Actual unscaled Boolean flag")
            bound = (min(args[1][0], args[2][0]), max(args[1][1], args[2][1]))
        elif op == "positive":
            bound = (max(0, args[0][0]), max(0, args[0][1]))
        else:
            require(False, "Uncertified eager operation outside exact bounded stock/sampler scopes")
        values[value] = word72(bound)
        records.append(
            dict(
                value=value,
                primitive=op,
                raw_bounds=list(values[value]),
                boundary_or_preproved=False,
            )
        )
    require(graph.target["outputs"]["Y"] in values, "Full actual financial output word safety")
    return dict(
        all_eager_financial_values_signed72_safe=True,
        all_eager_signed144_products_safe=True,
        eager_dead_Estrin_power_paths_included=True,
        no_finite_samples_or_native_replays_used=True,
        independently_checked_values=records,
        sampler_universal_scope_reused_only_through_exact_original_pair_binding=True,
    )


def contains_enclosure(primary, independent, message):
    lo, hi = [rational(value) for value in primary]
    own_lo, own_hi = [rational(value) for value in independent]
    require(lo <= own_lo <= own_hi <= hi, message)


def claimed_upper(primary, independent, message):
    value, own = rational(primary), rational(independent)
    require(0 <= own <= value, message)
    return value


def integer_stock_values(graph, scope, first, last, k, started):
    """Independent full72 integer range induction for one exact clipped class."""
    values, products = {scope["clipped"]: word72((first, last))}, []
    for value in scope["full_stock_node_ids"]:
        check(started)
        node = graph.node(value)
        args, op = [values[child] for child in node["args"]], node["op"]
        if op == "const":
            result = (graph.constant(value),) * 2
        elif op in ("mul", "cmul"):
            left = args[0]
            right = args[1] if op == "mul" else (signed_coefficient(node["params"]["c"]),) * 2
            endpoints_raw = [a * b for a in left for b in right]
            square = op == "mul" and node["args"][0] == node["args"][1]
            minimum = 0 if square and left[0] <= 0 <= left[1] else min(endpoints_raw)
            product = (minimum, max(endpoints_raw))
            require(
                -(1 << 143) <= product[0] <= product[1] < 1 << 143,
                "Exact class signed144 product bounds",
            )
            products.append(dict(value=value, product_raw_bounds=list(product)))
            result = (product[0] // Q, product[1] // Q)
        elif op == "add":
            result = (args[0][0] + args[1][0], args[0][1] + args[1][1])
        elif op == "sub":
            result = (args[0][0] - args[1][1], args[0][1] - args[1][0])
        elif op == "bits":
            shift = node["params"]["shift"]
            require(node["params"]["width"] == W, "Actual stock full72 extraction")
            if shift >= 0:
                require(
                    node["params"]["signed"] is True, "Native signed arithmetic exponent extraction"
                )
                result = (args[0][0] >> shift, args[0][1] >> shift)
            else:
                require(node["params"]["signed"] is False, "Native modular full72 k scaling")
                result = (args[0][0] << -shift, args[0][1] << -shift)
        else:
            require(
                op == "shift" and args[1] == (k, k) and -72 < k < 72 and args[0][0] > 0,
                "Native positive stock and exact class shift",
            )
            result = tuple(v << k if k >= 0 else v >> -k for v in args[0])
        values[value] = word72(result)
    require(
        values[scope["k"]] == (k, k)
        and values[scope["remainder"]]
        == (first - k * scope["ln2_raw"], last - k * scope["ln2_raw"])
        and values[scope["stock"]][0] > 0,
        "Exact class reduction, remainder and strictly positive native stock",
    )
    return values, products


def compare_cosine(primary, own, B, table, started):
    require(
        primary["schema"] == "original-BM-cosine-arithmetic-envelope-v1"
        and primary["interval_digits"] == 90
        and primary["coefficient_count"] == 512,
        "Primary original cosine scope and precision",
    )
    require(len(primary["coefficient_checks"]) == 512, "Every primary literal discrepancy retained")
    for declared, independent in zip(
        primary["coefficient_checks"], own["coefficient_checks"], strict=True
    ):
        check(started)
        same(
            [declared[k] for k in ("row", "degree", "raw")],
            [independent[k] for k in ("row", "degree", "raw")],
            "All512 actual cosine identities",
        )
        contains_enclosure(
            declared["exact_coefficient_enclosure"],
            independent["exact_coefficient_enclosure"],
            "Primary cosine true coefficient includes independent130 enclosure",
        )
        claimed_upper(
            declared["actual_literal_error_upper"],
            independent["literal_error_upper"],
            "All512 primary literal discrepancy bounds independently justified",
        )
    radius = Fraction(1, 128)
    same(primary["local_absolute_radius"], encode(radius), "Exact actual dyadic cosine bin radius")
    same(
        primary["Horner_floor_upper"],
        own["cosine_table_floor_upper"],
        "All seven signed Horner floors",
    )
    require(len(primary["native_Horner_steps"]) == 64, "Every original cosine row native safety")
    for index, row in enumerate(table):
        check(started)
        report = primary["native_Horner_steps"][index]
        require(report["row"] == index and len(report["steps"]) == 7, "Exact original Horner steps")
        magnitude = abs(Fraction(row[-1], Q))
        for degree, declared in zip(range(6, -1, -1), report["steps"], strict=True):
            require(magnitude * radius * Q**2 < 1 << 143, "Primary cosine step signed144 safety")
            magnitude = magnitude * radius + EPS + abs(Fraction(row[degree], Q))
            require(magnitude * Q < 1 << 71, "Primary cosine step stored72 safety")
            require(declared["degree"] == degree, "Native Horner order")
            same(
                declared["magnitude_upper"],
                encode(magnitude),
                "Exact native Horner rational safety bound",
            )
    remainder = claimed_upper(
        primary["Taylor_degree7_remainder_upper"],
        own["cosine_table_remainder_upper"],
        "Primary degree7 analytic cosine remainder justified",
    )
    literals = claimed_upper(
        primary["literal_rounding_upper"],
        own["cosine_table_literal_rounding_upper"],
        "Primary weighted actual coefficient error justified",
    )
    floors = rational(primary["Horner_floor_upper"])
    E = remainder + literals + floors
    same(
        primary["cosine_error_upper"],
        encode(E),
        "Cosine error has exactly its three paid components",
    )
    same(
        primary["pinned_native_radius_upper"],
        encode(B),
        "Same actual independently approved internal radius",
    )
    delta, native = B * E + EPS, B * (1 + E) + EPS
    same(
        primary["remaining_coordinate_error_upper"],
        encode(delta),
        "Only remaining coordinate error paid",
    )
    same(primary["native_normal_absolute_upper"], encode(native), "Native absolute normal envelope")
    same(
        primary["final_signed_product_floor_upper"],
        encode(EPS),
        "Actual final signed product floor paid once",
    )
    require(
        ceiling(native * Q) < 1 << 71 and ceiling(B * Q) * ceiling((1 + E) * Q) < 1 << 143,
        "Full actual stored72 and signed144 final product safe",
    )
    require(
        primary["exact_midpoint_and_positive_sine_quarter_wrap"] is True
        and primary["absent_rounded_two_pi_multiply_not_charged"] is True
        and primary["old_radius_Holder_log_root_or_grid_terms_added_again"] is False
        and primary["all_actual_coefficients_paid_without_half_ULP_assumption"] is True
        and primary["all_product144_and_stored72_guards_passed"] is True,
        "Original direct cosine convention and pay-once arithmetic scope",
    )
    return delta, native


def compare_stock_record(mp, declared, own, graph, scopes, support, started):
    require(
        declared["actual_stock_sites"] == len(scopes)
        and declared["retained_classes"] == 30
        and declared["whole_clipped_integer_domain_covered"] is True,
        "Every actual original stock and all fixed30 classes retained",
    )
    same(declared["fixed_exponent_superset"], [-17, 12], "Unchanged exponent superset")
    same(
        [declared["lower_clamp_raw"], declared["upper_clamp_raw"]],
        own["clamp_raw_bounds"],
        "Actual signed72 clamp interpretation",
    )
    require(len(declared["actual_sites"]) == len(scopes), "Full primary original stock inventory")
    for source, scope in zip(declared["actual_sites"], scopes, strict=True):
        check(started)
        same(
            [source[k] for k in ("stock", "clipped", "raw_log", "polynomial", "remainder")],
            [scope[k] for k in ("stock", "clipped", "raw_log", "polynomial", "remainder")],
            "Every actual source stock identity",
        )
        same(
            [source[k] for k in ("exponent", "low", "high", "inverse_ln2", "ln2")],
            [scope["k"], *own["clamp_raw_bounds"], scope["inverse_ln2_raw"], scope["ln2_raw"]],
            "Exact original extraction and native stock literals",
        )
        require(
            source["actual_original_support_signature"]
            == scope["actual_original_support_signature"],
            "Primary stock original-support source hash independently recovered",
        )
    require(len(declared["classes"]) == 30, "Every primary fixed class including empties")
    primary_alphas = []
    for source, row in zip(declared["classes"], own["classes"], strict=True):
        check(started)
        require(
            source["k"] == row["k"] and source["empty"] is row["empty"], "Exact class occupancy"
        )
        if row["empty"]:
            k = row["k"]
            low, high = own["clamp_raw_bounds"]
            inverse = own["inverse_ln2_raw"]
            same(
                source["clipped_log_raw_bounds"],
                [
                    max(low, ceiling(Fraction(k * Q**2, inverse))),
                    min(high, ceiling(Fraction((k + 1) * Q**2, inverse)) - 1),
                ],
                "Exact empty endpoint class, no asserted occupied extreme",
            )
            continue
        same(
            source["clipped_log_raw_bounds"],
            row["clipped_raw_bounds"],
            "Exact whole integer class endpoints",
        )
        same(
            source["remainder_raw_bounds"],
            row["remainder_raw_bounds"],
            "Exact original cell remainder",
        )
        model = row["native_polynomial"]
        same(
            source["actual_polynomial_coefficients"],
            [encode(Fraction(word, Q)) for word in model["actual_coefficients_raw"]],
            "All13 actual original Estrin coefficients",
        )
        same(
            model["actual_coefficients_raw"],
            support["certificate"]["literal_exp_coefficients"],
            "Original support polynomial literals are source-identical",
        )
        same(
            source["polynomial_literal_error_upper"],
            model["literal_error_upper"],
            "Exact polynomial literal errors",
        )
        same(
            source["polynomial_native_floor_error_upper"],
            model["floor_error_upper"],
            "Every actual Estrin floor",
        )
        taylor = claimed_upper(
            source["Taylor_degree12_remainder_upper"],
            row["degree12_Taylor_remainder_upper"],
            "Original polynomial analytic remainder independently justified",
        )
        E = rational(model["literal_error_upper"]) + rational(model["floor_error_upper"]) + taylor
        same(source["polynomial_error_upper"], encode(E), "Complete actual cell polynomial error")
        ln_error = claimed_upper(
            source["ln2_literal_error_upper"],
            own["ln2_literal_error_upper"],
            "Original ln2 literal error independently justified",
        )
        independent_relative = endpoints(
            mp.iv.exp(outward(mp, abs(row["k"]) * ln_error))
            * (
                1
                + outward(mp, E)
                * mp.iv.exp(outward(mp, -Fraction(row["remainder_raw_bounds"][0], Q)))
            )
            - 1
        )[1]
        alpha = claimed_upper(
            source["relative_stock_error_upper"],
            encode(independent_relative),
            "Primary original relative stock envelope independently justified",
        )
        primary_alphas.append(alpha)
        integer_values, product_values = integer_stock_values(
            graph, scopes[0], *row["clipped_raw_bounds"], row["k"], started
        )
        same(
            source["polynomial_raw_bounds"],
            list(integer_values[scopes[0]["polynomial"]]),
            "Exact native class polynomial range",
        )
        same(
            source["stock_raw_bounds"],
            list(integer_values[scopes[0]["stock"]]),
            "Exact class stock shift range",
        )
        same(
            source["signed144_products"],
            product_values,
            "Every original stock full144 product range",
        )
        require(
            source["all_actual_native_intermediates_signed72_safe"] is True
            and source["k_times_ln2_extra_rounding"] == 0,
            "Original cell native safety and exact integer ln2 product",
        )
        own_steps = {step["value"]: step for step in model["steps"]}
        require(
            {step["value"] for step in source["polynomial_floor_and_range_steps"]}
            == set(own_steps),
            "All primary Estrin error-induction steps retained",
        )
        for step in source["polynomial_floor_and_range_steps"]:
            independent = own_steps[step["value"]]
            require(step["op"] == independent["primitive"], "Actual Estrin operation identity")
            same(
                step["magnitude_upper"],
                independent["magnitude_upper"],
                "Exact polynomial magnitude induction",
            )
            same(
                step["native_floor_error_upper"],
                independent["floor_error_upper"],
                "Exact polynomial floor induction",
            )
    alpha = max(primary_alphas)
    same(
        declared["alpha_upper"], encode(alpha), "Primary alpha is maximum over every occupied class"
    )
    same(declared["beta_upper"], encode(EPS), "Only final negative shift floor additive beta")
    require(
        0 <= alpha < 1
        and declared["actual_native_upper_clamp_stock_raw"] == own["native_upper_clamp_stock_raw"],
        "Strict relative envelope and actual upper-clamp integer",
    )
    require(
        declared["all_positive_stock_stored72_product144_shift_guards_passed"] is True
        and declared["final_negative_shift_floor_charged_once"] is True
        and declared["AS241_financial_theorem_transferred"] is False,
        "Original arithmetic and no AS transfer",
    )
    return alpha


def compare_raw_record(declared, own, graph, roles, raw_values, delta, native, B, started):
    same(
        [
            declared[k]
            for k in (
                "actual_common_literal",
                "actual_idio_literal",
                "actual_drift_literal",
                "actual_initial_literal",
            )
        ],
        [
            roles[k]
            for k in (
                "actual_common_literal",
                "actual_idio_literal",
                "actual_drift_literal",
                "actual_initial_literal",
            )
        ],
        "Every actual raw-prefix literal",
    )
    contains_enclosure(
        declared["exact_common_coefficient_enclosure"],
        own["true_common_enclosure"],
        "Primary common coefficient true interval justified",
    )
    contains_enclosure(
        declared["exact_idio_coefficient_enclosure"],
        own["true_idio_enclosure"],
        "Primary idiosyncratic coefficient true interval justified",
    )
    dates, assets = roles["dates"], roles["assets"]
    same(
        declared["exact_drift"], encode(Fraction(-3, 200 * dates)), "Exact unchanged contract drift"
    )
    ea = claimed_upper(
        declared["common_literal_error_upper"],
        own["common_literal_error_upper"],
        "Common coefficient error",
    )
    eb = claimed_upper(
        declared["idio_literal_error_upper"],
        own["idio_literal_error_upper"],
        "Idio coefficient error",
    )
    same(
        declared["drift_literal_error_upper"],
        own["drift_literal_error"],
        "Exact drift-literal discrepancy",
    )
    e0 = claimed_upper(
        declared["initial_log_spot_error_upper"],
        own["initial_literal_error_upper"],
        "Initial log-spot error",
    )
    a, b = [Fraction(roles[k], Q) for k in ("actual_common_literal", "actual_idio_literal")]
    increment = (
        (abs(a) + abs(b)) * delta + (ea + eb) * B + rational(own["drift_literal_error"]) + 2 * EPS
    )
    same(
        declared["per_increment_error_upper"],
        encode(increment),
        "Each original increment exactly itemized",
    )
    require(
        declared["normal_raw_absolute_upper"] == ceiling(native * Q),
        "Actual symmetric native normal word bound",
    )
    require(len(declared["prefixes"]) == dates, "All original date-prefix rows")
    lambdas = []
    for date, row in enumerate(declared["prefixes"]):
        check(started)
        witnesses = sorted(
            (v for v in roles["prefix_witnesses"] if v["date"] == date), key=lambda v: v["asset"]
        )
        require(
            row["date"] == date and row["elapsed_dates"] == date + 1 and len(witnesses) == assets,
            "Exact primary date index and complete assets",
        )
        same(
            row["actual_raw_log_sites"],
            [v["raw_log"] for v in witnesses],
            "Every actual raw-prefix output",
        )
        same(
            row["actual_raw_log_bounds"],
            [list(raw_values[v["raw_log"]]) for v in witnesses],
            "Every unrounded actual raw-prefix integer range",
        )
        lam = e0 + (date + 1) * increment
        same(
            row["lambda_upper"], encode(lam), "Full prefix error with no reset or duplicate charge"
        )
        require(
            row["original_driver_count_per_stock"] == 2 * (date + 1)
            and row["original_driver_multiplicity"] == 1
            and row["original_drift_multiplicity"] == date + 1,
            "Every original driver exactly once",
        )
        lambdas.append(lam)
    steps = own["actual_raw_prefix_word_guards"]
    same(
        declared["native_partial_sum_inventory"],
        [dict(value=v["value"], op=v["primitive"], raw_bounds=v["raw_bounds"]) for v in steps],
        "All actual raw partial additions and outputs independently bounded",
    )
    products = []
    for step in steps:
        check(started)
        node = graph.node(step["value"])
        if node["op"] == "cmul":
            source = raw_values[node["args"][0]]
            coefficient = signed_coefficient(node["params"]["c"])
            endpoints_raw = [word * coefficient for word in source]
            product = [min(endpoints_raw), max(endpoints_raw)]
            require(
                -(1 << 143) <= product[0] <= product[1] < 1 << 143,
                "Actual raw scaled-normal signed144 safe",
            )
            products.append(dict(value=step["value"], product_raw_bounds=product))
    same(
        declared["native_full144_product_inventory"],
        products,
        "Every actual scaled-normal full product",
    )
    require(
        declared["every_stored72_raw_partial_sum_safe"] is True
        and declared["every_signed144_scaled_normal_product_safe"] is True
        and declared["raw_prefix_proof_before_clips_and_survival"] is True
        and declared["addition_rounding_paid"] == 0
        and declared["signed_scaled_normal_floors_per_increment"] == 2
        and declared["normal_radius_or_grid_error_paid_again"] is False,
        "Native no-wrap premises precede all clipping and survivor claims",
    )
    return lambdas


def audit_closed_bands(mp, declared, stock, alpha, lambdas, roles, raw_values, DS, polar, started):
    assets, dates, pairs = roles["assets"], roles["dates"], roles["pairs"]
    low, high = [Fraction(v, Q) for v in stock["clamp_raw_bounds"]]
    same(declared["alpha_upper"], encode(alpha), "Same validated primary stock alpha")
    same(declared["beta_upper"], encode(EPS), "Same paid final stock shift floor")
    same(
        [declared["decoded_lower_clamp"], declared["decoded_upper_clamp"]],
        [encode(low), encode(high)],
        "Actual signed clamps",
    )
    ell_true_upper = endpoints(outward(mp, 1 + alpha) * mp.iv.exp(outward(mp, low)))[1] + EPS
    ell = claimed_upper(
        declared["ell_upper"], encode(ell_true_upper), "Lower-clamp leakage at independent130"
    )
    require(
        ell < 140 and stock["native_upper_clamp_stock_raw"] >= assets * 140 * Q,
        "Native upper-clamp knockout and bounded lower leakage",
    )
    require(
        polar["angular"]["all_strict_guards_passed"] is True
        and polar["angular"]["cases"][
            next(k for k, v in CASES.items() if v[:2] == (assets, dates))
        ]["passed"]
        is True,
        "Actual audited bounded-radius strict angular guard",
    )
    require(len(declared["dates"]) == dates, "Each strict source date barrier covered")
    rows, probabilities = [], []
    for j, (row, lam) in enumerate(zip(declared["dates"], lambdas, strict=True), start=1):
        check(started)
        require(row["date"] == j - 1 and row["elapsed_dates"] == j, "Exact barrier date")
        same(row["lambda_upper"], encode(lam), "Same complete primary raw-log error")
        a_true = endpoints(outward(mp, 1 - alpha) * mp.iv.exp(outward(mp, -lam)))[0]
        b_true = endpoints(outward(mp, 1 + alpha) * mp.iv.exp(outward(mp, lam)))[1]
        a, b = rational(row["a_lower"]), rational(row["b_upper"])
        require(
            0 < a <= a_true <= 1 <= b_true <= b,
            "Independent primary multiplicative clip-band bounds",
        )
        same(row["ell_upper"], encode(ell), "Same validated lower-clamp leakage")
        ideal_upper_lower = endpoints(mp.iv.exp(outward(mp, high - lam)))[0]
        declared_upper_lower = rational(row["ideal_upper_clip_stock_lower"])
        require(
            assets * 140 < declared_upper_lower <= ideal_upper_lower,
            "Primary upper-clip guard independently checked at its OWN full lambda",
        )
        require(
            row["native_upper_clip_stock_raw"] == stock["native_upper_clamp_stock_raw"],
            "Actual native upper stock integer",
        )
        lower, upper = Fraction(140 - ell, b), Fraction(140 + EPS + EPS, a)
        require(
            0 < lower <= upper, "Positive ordered closed barrier band including native equality"
        )
        same(
            [row["closed_band_lower"], row["closed_band_upper"]],
            [encode(lower), encode(upper)],
            "Exact closed band endpoints",
        )
        variance = Fraction(9 * j, 250 * dates)
        same(
            row["exact_continuous_common_variance"],
            encode(variance),
            "Continuous common-driver variance only",
        )
        pg = min(
            Fraction(1),
            endpoints(
                mp.iv.log(outward(mp, upper / lower))
                / mp.iv.sqrt(outward(mp, 2 * variance) * mp.iv.pi)
            )[1],
        )
        source_pg = claimed_upper(
            row["gaussian_closed_band_probability_upper"],
            encode(pg),
            "Unconditional Gaussian band bound independently derived",
        )
        require(source_pg <= 1, "Primary Gaussian probability capped by one")
        m = ((assets + 1) * j + 1) // 2
        require(
            0 < m <= pairs and row["relevant_whole_pairs"] == m,
            "Whole relevant pair blocks including unused partner",
        )
        law = m * (4 * DS + Fraction(2, N))
        same(
            row["pair_law_allowance"],
            encode(law),
            "Separate radialTV4 and circularTV4 band transport",
        )
        hybrid = min(Fraction(1), source_pg + law)
        same(
            row["hybrid_closed_band_probability_upper"],
            encode(hybrid),
            "Hybrid closed-band probability with atoms and ties",
        )
        require(
            row["radial_band_pointwise_TV_upper"] == row["circular_band_pointwise_TV_upper"] == 4
            and row["strict_threshold_TV2_not_substituted"] is True
            and row["unused_future_pair_partner_retained"] is True,
            "Actual-point band variation and whole-pair law",
        )
        probabilities.append(hybrid)
        rows.append(
            dict(
                date=j - 1,
                independent_a_lower=encode(a_true),
                independent_b_upper=encode(b_true),
                independent_ideal_upper_clip_stock_lower=encode(ideal_upper_lower),
                independent_gaussian_probability_upper=encode(pg),
                source_conservative_row=row,
            )
        )
    switch = min(Fraction(1), sum(probabilities, Fraction(0)))
    same(
        declared["hybrid_any_switch_probability_upper"],
        encode(switch),
        "One union bound for every strict date switch",
    )
    require(
        len(declared["actual_eager_clamp_inventory"]) == assets * dates,
        "Each actual source clamp inspected",
    )
    for witness, row in zip(
        roles["prefix_witnesses"], declared["actual_eager_clamp_inventory"], strict=True
    ):
        check(started)
        same(
            [row["stock"], row["raw_log"], row["raw_log_bounds"]],
            [witness["stock"], witness["raw_log"], list(raw_values[witness["raw_log"]])],
            "Actual eager clamp source and raw bounds",
        )
        same(
            row["decoded_lower_upper_raw"],
            stock["clamp_raw_bounds"],
            "Signed native clamp literals",
        )
        same(row["eager_lt_flag_bounds"], [0, 1], "Native unscaled Boolean comparison flags")
    require(
        declared["two_direction_upper_clip_knockout_guards_passed"] is True
        and declared["all_strict_comparison_and_closed_endpoint_ties_retained"] is True
        and declared["no_survival_clipping_or_good_radius_conditioning_in_Gaussian_bound"] is True,
        "Closed unconditional barrier proof scope",
    )
    return dict(
        dates=rows,
        independent_ell_upper=encode(ell_true_upper),
        verified_primary_any_switch_upper=encode(switch),
        primary_closed_bands=declared,
    ), switch


def audit_smooth(mp, declared, bands, support, assets, dates, started):
    c_average, c_discount = support["actual_average_literal"], support["actual_discount_literal"]
    require(
        declared["actual_average_literal"] == c_average
        and declared["actual_discount_literal"] == c_discount,
        "Actual source whole-stock average and discount coefficients",
    )
    average_error_literal = abs(Fraction(c_average, Q) - Fraction(1, assets * dates))
    same(
        declared["exact_average_literal_error"],
        encode(average_error_literal),
        "Exact whole-stock mean coefficient error",
    )
    true_discount = endpoints(mp.iv.exp(outward(mp, Fraction(-3, 100))))
    contains_enclosure(
        declared["exact_discount_enclosure"],
        [encode(v) for v in true_discount],
        "Primary discount true enclosure independently130",
    )
    discount_error = max(abs(Fraction(c_discount, Q) - v) for v in true_discount)
    source_discount_error = claimed_upper(
        declared["discount_literal_error_upper"],
        encode(discount_error),
        "Actual discount-literal error",
    )
    ell = rational(bands["ell_upper"])
    require(
        len(declared["date_mean_stock_errors"]) == dates,
        "Each unrounded survivor stock mean covered",
    )
    date_errors = []
    for source, row in zip(declared["date_mean_stock_errors"], bands["dates"], strict=True):
        check(started)
        a, b = rational(row["a_lower"]), rational(row["b_upper"])
        error = 140 * max(1 - a, b - 1) + max(EPS, ell)
        require(source["date"] == row["date"], "Source mean-stock error date")
        same(
            source["unrounded_mean_stock_error_upper"],
            encode(error),
            "Safe both-survivor unrounded mean envelope",
        )
        date_errors.append(error)
    average = (
        sum(date_errors, Fraction(0)) / dates + assets * dates * 140 * average_error_literal + EPS
    )
    zeta = Fraction(c_discount, Q) * average + 40 * source_discount_error + EPS
    same(
        declared["average_error_upper"],
        encode(average),
        "One average floor and actual mean coefficient paid",
    )
    same(
        declared["smooth_discounted_payoff_error_upper"],
        encode(zeta),
        "One final discount floor and true discount error paid",
    )
    same(
        declared["fixed_both_payoffs_safe_cap"],
        encode(40),
        "Both nonnegative payoff supports bound by40",
    )
    same(
        declared["native_cap_upper"],
        support["native_cap_upper"],
        "Exact original source native payoff cap",
    )
    same(declared["average_floor_upper"], encode(EPS), "Actual average floor exactly once")
    same(
        declared["final_discount_floor_upper"],
        encode(EPS),
        "Final signed discount floor exactly once",
    )
    require(
        0 < c_discount <= Q
        and rational(support["native_cap_upper"]) < 40
        and declared["averaging_ALL_native_stock_words"] is True
        and declared["rounded_baskets_not_averaged"] is True
        and declared["basket_floor_charged_only_in_barrier_band"] is True
        and declared["strict_survival_unrounded_mean_proof"] is True
        and declared["positive_part_is_1_Lipschitz_and_same_exact_strike"] is True,
        "Native integer survival, original mean and discounted pay-once supports",
    )
    return dict(
        independent_true_discount_enclosure=[encode(v) for v in true_discount],
        independent_discount_literal_error_upper=encode(discount_error),
        verified_primary_average_error_upper=encode(average),
        verified_primary_smooth_discounted_error_upper=encode(zeta),
    ), zeta


def audit_complete(declared, polar, bridges, started):
    require(
        declared["schema"] == "original-BM-complete-native-financial-bounds-v1"
        and set(declared["cases"]) == set(CASES),
        "Both original financial contracts retained",
    )
    reports, fits = {}, []
    for case, (_, dates, pairs) in CASES.items():
        check(started)
        row = declared["cases"][case]
        premise = polar["price"]["cases"][case]
        price = rational(premise["hybrid_dollars_upper"])
        cap_lo, cap_hi = [rational(v) for v in premise["exact_cap_enclosure"]]
        DS = rational(polar["radius"]["squared_radius_KS_upper"])
        require(
            0 <= cap_lo <= cap_hi <= 40 and 0 <= DS <= 1,
            "Actual approved primary ideal support and squared-radius distribution bound",
        )
        require(
            price == pairs * (4 * cap_hi * DS + cap_hi * Fraction(dates + 1, N)),
            "One existing primary polar whole-pair price-law term",
        )
        zeta, switch = bridges[case]
        bridge, total = zeta + 40 * switch, price + zeta + 40 * switch
        fit = total <= ALLOWANCE
        same(
            row["pinned_primary_hybrid_price_upper"],
            encode(price),
            "Existing primary hybrid term preserved exactly",
        )
        same(
            row["pinned_primary_exact_cap_enclosure"],
            premise["exact_cap_enclosure"],
            "Both original ideal support endpoints",
        )
        same(
            row["pinned_primary_squared_radius_KS_upper"],
            encode(DS),
            "Pinned radial-law premise paid once",
        )
        same(
            row["smooth_discounted_payoff_error_upper"],
            encode(zeta),
            "Verified complete native smooth error",
        )
        same(
            row["hybrid_any_switch_probability_upper"],
            encode(switch),
            "Verified closed-band union bound",
        )
        same(row["fixed_safe_switch_cap"], encode(40), "One shared nonnegative payoff support cap")
        same(
            row["native_bridge_dollars_upper"], encode(bridge), "Only new bridge components summed"
        )
        same(
            row["continuous_to_native_dollars_upper"],
            encode(total),
            "Complete original bias ledger has exactly two terms",
        )
        same(
            row["unchanged_financial_residual"],
            encode(ALLOWANCE),
            "Unchanged financial residual allowance",
        )
        require(
            row["financial_residual_fit"] is fit
            and row["native_financial_bias_certificate_valid"] is True
            and row["actual_joint_pairs"] == pairs
            and row["independent_audit_still_required"] is True,
            "Exact fit decision is separate from proof validity and audit requirement",
        )
        reports[case] = dict(
            verified_primary_total_upper=encode(total),
            financial_residual_fit=fit,
            verified_primary_hybrid_upper=encode(price),
            verified_primary_native_bridge_upper=encode(bridge),
        )
        fits.append(fit)
    require(
        declared["all_financial_residuals_fit"] is all(fits)
        and declared["native_financial_bias_certificate_valid"] is True
        and declared["full_G2"] is declared["adoption"] is declared["cost_transfer"] is False
        and declared["estimator_99percent_delivery_certified"] is False
        and declared["matched_classical_or_quantum_advantage_claimed"] is False
        and declared["new_fixture_credit"] == 0,
        "No estimator, cost, G2, advantage or fixture transfer",
    )
    return dict(
        cases=reports,
        all_financial_residuals_fit=all(fits),
        native_financial_bias_certificate_valid=True,
    ), all(fits)


def independent_bridge_derivation():
    """Written proof of the transport premises, independently retained in the audit."""
    return dict(
        actual_point_values=(
            "Variation counts left-limit -> actual value -> right-limit, and the circular seam. "
            "An isolated contact therefore pays two jumps. CDF differences use F(t-) and F(t); "
            "an atomic hybrid point is not removed by replacing the function almost everywhere."
        ),
        radial_band=(
            "Condition on every other pair and the current ideal angle. Each unclipped exact stock "
            "is c_i exp(v_i r), c_i>0, so its basket has nonnegative second derivative on r>=0. "
            "A convex basket's closed finite band is its closed upper sublevel minus its "
            "open lower "
            "sublevel: at most two intervals, including singleton contacts and the endpoint zero. "
            "The radial domain is the full [0,infinity); extend only below zero, with no upper "
            "radius cutoff or good-radius conditioning. There are at most four pointwise jumps. "
            "Composition with sqrt(s) preserves that "
            "variation, so its squared-radius distribution difference is at most4*DS."
        ),
        angular_band=(
            "The actual audited polar certificate supplies positive ideal pair directions and "
            "strict B^2*maximum_squared_norm<2 for each original contract. With current radius "
            "bounded by B, write x_i=r(a_i cos(theta)+b_i sin(theta)), y_i=x_i'. At a quadrant-I "
            "stationary point positive and negative weighted derivative masses both equal M. "
            "Their respective |y_i| bounds are kappa*cos(theta), kappa*sin(theta), and their x_i "
            "lower bounds give sum(w_i x_i)>=M/(sin(theta)cos(theta)). Thus sum(w_i y_i^2) "
            "<=kappa*(sin(theta)+cos(theta))*M<=kappa/sqrt(2)*sum(w_i x_i), so B''<0. "
            "Quadrant III is convex; II and IV have fixed derivative signs. Constant, axis and "
            "zero-radius cases retain endpoint values. There is one max/min or a constant basket; "
            "a closed band has at most two arcs with circular pointwise TV<=4. The midpoint grid "
            "therefore costs at most4/(2N), including a sampled singleton."
        ),
        replacement_order=(
            "Start from the fully continuous ideal joint Gaussian law. Replace the CURRENT whole "
            "pair radius first by the certified native internal radius, then its ideal angle by "
            "the uniform midpoint angle. The angular step now has bounded radius. Other pairs only "
            "alter positive weights. Date j uses ceil((na+1)j/2) whole independent blocks, "
            "including "
            "a straddling pair's unused future coordinate; band allowance is m_j*(4DS+2/N)."
        ),
        gaussian_band=(
            "Only in the fully continuous law, common and idiosyncratic coordinates are "
            "independent "
            "Gaussian drivers. Factor the date basket as exp(s_j Z)*W, W>0 independent of Z, "
            "s_j^2=(9/100)*(2/5)*j/nt. Conditional band log width is log(U_j/L_j)/s_j; normal "
            "density is at most1/sqrt(2pi). Integrating W yields the unconditional closed-band "
            "bound, capped by one. No survivor, clip or good-radius conditioning is introduced. "
            "Add the separately paid whole-pair allowance and then a single date union bound."
        ),
        clip_discharge=(
            "The fresh actual stock arithmetic gives (1-alpha)exp(clip(xhat))-beta<=S_N "
            "<=(1+alpha)exp(clip(xhat))+beta. Actual S_N(U)>=na*H and exp(U-lambda_j)>na*H, "
            "together with positive stocks, exclude every upper-clip event from either survivor. "
            "A lower clip leaks at most ell. Summing and paying the exact binary basket floor "
            "gives a_j B_H-beta-eps<=B_N<=b_j B_H+ell. Opposite strict decisions imply the CLOSED "
            "band [(H-ell)/b_j,(H+beta+eps)/a_j], with native equality and extrema ties included."
        ),
        survivor_mean=(
            "The actual native integer date sum S_raw obeys floor(S_raw/na)<140Q. Since 140Q "
            "is integral, S_raw<=na*140Q-1. Thus each unrounded survivor mean<H, and the total "
            "surviving stock sum is at most nt*(na*140Q-1), before averaging. The source averages "
            "all stock words. On both-path survival the unrounded mean error is bounded by "
            "H*max(1-a_j,b_j-1)+max(beta,ell); pay actual average-literal error, "
            "one average floor, "
            "the 1-Lipschitz positive part at the same strike, true discount-literal error and "
            "one discount floor. Both already-discounted nonnegative payoffs lie in[0,40]."
        ),
        ledger=(
            "Pinned primary polar price-law error already pays the radius log/root and midpoint "
            "angle law. Remaining coordinate error is ONLY B*Ecos+eps. The sole added bridge is "
            "zeta+40*P_H(any switch), then Total=H_price+Bridge. Do not add a second augmented "
            "envelope, old radial Holder/grid/cutoff, scalar AS theorem or extra generic "
            "dimension/N. Only continuous-to-native original financial bias is certified; "
            "full G2 and adoption stay open."
        ),
        native_rounded_finance_convexity_assumed=False,
        AS241_theorem_or_native_cost_transferred=False,
    )


def implementation_policy(started):
    data = read_json(IMPLEMENTATION, started)
    require(
        data["schema"] == "box-muller-native-financial-bridge-implementation-preflight-v1",
        "Exact new bridge implementation contract",
    )
    for field in (
        "producer_CPU_admission_wall_seconds",
        "independent_auditor_CPU_admission_wall_seconds",
    ):
        same(data[field], [CPU, ADMISSION, WALL], "Unchanged all-inclusive budgets")
    same(
        data["runtime_inventory_cap_files_bytes"],
        [MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES],
        "Unchanged finite runtime inventory caps",
    )
    require(
        data["primary_interval_decimal_digits"] == 90
        and data["independent_interval_decimal_digits"] == DIGITS
        and data["numerical_threads"] == 1
        and data["new_fixture_credit"] == data["new_gate_replays"] == 0
        and data["runtime_backend"] == "python"
        and data["mpmath_version"] == "1.3.0",
        "Fixed independent precision and scope",
    )
    same(
        data["method_document_SHA256"],
        {METHOD.name: METHOD_SHA, METHOD_DOC.name: METHOD_DOC_SHA},
        "Exact held mathematical and operational method",
    )
    same(data["required_polar_manifest_SHA256"], POLAR_MANIFESTS, "Actual root-supplied PASS pins")
    same(
        data["required_polar_receipts"],
        [p.relative_to(ROOT).as_posix() for p in (POLAR, POLAR_AUDIT)],
        "Actual polar release003 routes",
    )
    same(
        data["required_polar_author_SHA256"],
        {
            "experiment_box_muller_polar_cdf_bv_v3.py": (
                "e1e59867be43a8a66b8a7b5b9df88e41a23d2eaa211f7fe4fb101967312015a3"
            ),
            "audit_box_muller_polar_cdf_bv_v3.py": (
                "b9b57daaa56dbceb28672165b7d7f7d544dc0360bc4bc3e100c8e3cae972961a"
            ),
        },
        "Actual polar executable bytes independently pinned",
    )
    same(data["original_root_owner_manifest_SHA256"], ROOT_OWNERS, "Both original root owners")
    same(data["additional_native_root_provenance_SHA256"], ROOT_PINS, "All13 original root inputs")
    same(data["native_financial_residual"], encode(ALLOWANCE), "Unchanged financial allowance")
    require(
        data["producer_receipt"] == SOURCE.relative_to(ROOT).as_posix()
        and data["independent_auditor_receipt"] == OUTPUT.relative_to(ROOT).as_posix(),
        "Exact fresh original native-financial source and audit receipts",
    )
    for flag in (
        "startup_B_required",
        "package_init_source_and_existing_exact_cache_included",
        "cosine_512_coefficient_envelope_in_scope",
        "cosine_actual_literal_errors_paid_without_nearest_half_ULP_assumption",
        "all_actual_17_polar_and_25_bridge_selected_owner_memberships_strict",
        "actual_polar_packets_complete_owned_frozen_external_maps_required",
        "all_emitted_native_dead_paths_including_unused_polynomial_powers_range_checked",
        "pinned_primary_polar_B_DS_cap_and_hybrid_upper_paid_once",
        "valid_certificate_and_residual_fit_are_separate",
    ):
        require(data[flag] is True, "Fixed explicit implementation premise: " + flag)
    for flag in (
        "full_G2",
        "adoption",
        "cost_transfer",
        "estimator_99percent_delivery_certified",
        "matched_classical_or_quantum_advantage_claimed",
    ):
        require(data[flag] is False, "No broader delivery or adoption claim: " + flag)
    scope = data["runtime_scope"]
    require(
        scope["base_Lib_site_packages"] == "EXCLUDED_UNREACHABLE_AND_REJECTED"
        and scope["full_remaining_standard_Lib"] is True
        and scope["actual_venv_pth_customize_and_loaded_bootstrap_bytes"] is True
        and scope["full_mpmath_existing_cache_and_distribution_metadata"] is True
        and scope["full_base_DLL_and_adjacent_files"] is True
        and scope["no_blanket_other_venv_package_admission"] is True
        and scope["exact_sys_prefix_search_path_admitted"] is True
        and scope["actual_venv_adjacent_bytes_and_directory_membership_frozen"] is True
        and scope["selected_source_and_old_provenance_hash_waivers"] is False,
        "Accepted reachable-runtime policy, no historical SHA waiver",
    )
    hashes = data["author_sha256"]
    require(set(hashes) == {AUTHOR.name, PRODUCER_AUTHOR.name}, "Both new executable pins required")
    for name, expected in hashes.items():
        check(started)
        require(
            type(expected) is str and SHA_PATTERN.fullmatch(expected),
            "Null code pins block preparation",
        )
        require(
            sha(RESEARCH / name, started) == expected,
            "Exact independently reviewed executable bytes",
        )
    return data


def metadata_history(plan, frozen, external, started):
    policy = plan["operational_v2_provenance"]
    require(
        policy["route_only_change_mathematical_contract_unchanged"] is True
        and policy["no_expected_hash_override_or_old_failure_reclassification"] is True,
        "Earlier failures remain explicit zero-credit admission evidence",
    )
    same(
        policy["original_method_SHA256"],
        {
            OLD_METHOD.relative_to(ROOT).as_posix(): OLD_METHOD_SHA,
            OLD_METHOD_DOC.relative_to(ROOT).as_posix(): OLD_METHOD_DOC_SHA,
        },
        "Both original held method bytes remain strict inputs",
    )
    for field in (
        "original_method_SHA256",
        "original_polar_author_SHA256",
        "original_polar_v2_author_SHA256",
    ):
        require(type(policy[field]) is dict, "Complete original author map")
        for key, expected in policy[field].items():
            check(started)
            actual = bind(frozen, external, ROOT / key, expected, started)
            require(
                actual.relative_to(ROOT).as_posix() == key, "Strict canonical original author route"
            )
    for suffix in ("run001", "audit_run001", "run002", "audit_run002"):
        require(
            not (PROGRAM / ("A02_polar_cdf_bv_" + suffix)).exists(),
            "Original rejected admissions have no mathematical receipt",
        )
    exact_prior = {
        "A02_polar_cdf_bv_admission_failure_run001": (
            "ae3333bd578a4725a542df0c6d80039623bc675fda3f972f15df4124dab9b7a5",
            [3, 8],
        ),
        "A02_polar_cdf_bv_root_review_run001": (
            "778b42a5abe95176a19b7d1ffc788a970cdd8e1903c41f33f572ba762cb6f49e",
            [1, 6],
        ),
        "A02_polar_cdf_bv_root_review_run002": (
            "0ff23db10caef553061bc687d677cd33f17bdebd33ab0bb54b68d09effadd333",
            [1, 7],
        ),
        "A02_polar_cdf_bv_admission_failure_run002": (
            "39a15e24c93b79a39f6e97930fff1f922d7d3ff4362347ee47077073dc3277b6",
            [3, 9],
        ),
        "A02_polar_cdf_bv_admission_observation_correction_run001": (
            "6d133c5e3f848d7af17be1e796b65b1851a6f6c4d8cdb669c201520065125eea",
            [1, 13],
        ),
        "A02_polar_cdf_bv_root_review_run003": (
            "296bb3a68d743dfe3c92a86839b1dfea30f57c67170c8ba37d8ca4197b8b5538",
            [1, 8],
        ),
    }
    rows = policy["prior_metadata_packets"]
    require(len(rows) == len(exact_prior), "All six actual diagnostic/review packets retained")
    reports, labels = [], set()
    for row in rows:
        check(started)
        receipt = canonical_path(ROOT / row["receipt"], started)
        require(
            receipt.parent == PROGRAM
            and receipt.name not in labels
            and receipt.name in exact_prior,
            "Finite exact metadata packet route",
        )
        labels.add(receipt.name)
        pin, counts = exact_prior[receipt.name]
        require(
            row["manifest_SHA256"] == pin
            and row["owned_frozen_counts"] == counts
            and row["scientific_or_fixture_credit"] == 0,
            "Exact prior pins/counts and zero credit",
        )
        manifest_path = bind(frozen, external, receipt / "manifest.json", pin, started)
        manifest = read_json(manifest_path, started)
        require(
            manifest["manifest_self_hash_excluded"] is True
            and [len(manifest["files"]), len(manifest["frozen_inputs"])] == counts,
            "Complete real prior maps, no fabricated failed-runtime inventory",
        )
        owned = set()
        for field in ("files", "frozen_inputs"):
            require(type(manifest[field]) is dict, "Recognized original ROOT-map schema")
            for key, expected in manifest[field].items():
                check(started)
                require(
                    type(key) is str and not Path(key).is_absolute(), "Original canonical ROOT key"
                )
                path = bind(frozen, external, ROOT / key, expected, started)
                require(
                    path.relative_to(ROOT).as_posix() == key,
                    "No original map alias or SHA replacement",
                )
                if field == "files":
                    require(path.is_relative_to(receipt), "Original owner confinement")
                    owned.add(path.relative_to(receipt).as_posix())
        actual_files(receipt, owned, started)
        reports.append(
            dict(
                receipt=row["receipt"],
                manifest_sha256=pin,
                owned_frozen_counts=counts,
                scientific_or_fixture_credit=0,
            )
        )
    require(labels == set(exact_prior), "All original metadata owners retained once")
    return reports


def method_origins(implementation, frozen, external, started):
    bind(frozen, external, METHOD, METHOD_SHA, started)
    bind(frozen, external, METHOD_DOC, METHOD_DOC_SHA, started)
    plan = read_json(METHOD, started)
    require(
        plan["schema"] == "original-box-muller-native-financial-bridge-author-preflight-v2"
        and plan["status"] == "HELD_AUTHOR_ONLY_ROUTE_CORRECTION_NO_EXECUTION",
        "Frozen route-only mathematical method",
    )
    pins = plan["original_selected_source_pins_from_existing_manifest_metadata"]
    require(type(pins) is dict and len(pins) == 25, "All25 actual original selected pins")
    owners = {key: value for key, value in pins.items() if key.endswith("/manifest.json")}
    require(len(owners) == 5, "Five original owners, not invented self-membership")
    selected = independent_origins(pins, owners, frozen, external, started, selected=True)
    require(len(selected) == 20, "All20 nonmanifest equal-SHA original memberships")
    roots = independent_origins(ROOT_PINS, ROOT_OWNERS, frozen, external, started, selected=False)
    history = metadata_history(plan, frozen, external, started)
    original = read_json(OLD_METHOD, started)
    same(
        original["original_selected_source_pins_from_existing_manifest_metadata"],
        pins,
        "Original mathematical source inventory preserved",
    )
    for field in (
        "remaining_normal_error",
        "raw_log_obligations",
        "stock_exponential_obligations",
        "clip_and_predicate_obligations",
        "closed_band_law_transfer",
    ):
        same(original[field], plan[field], "Original mathematical contract retained: " + field)
    for path in (AUTHOR, PRODUCER_AUTHOR, IMPLEMENTATION, IMPLEMENTATION_DOC):
        bind(frozen, external, path, sha(path, started), started)
    return plan, selected, roots, history


def actual_files(receipt, expected, started):
    found, total = set(), 0
    for candidate in receipt.rglob("*"):
        check(started)
        if candidate.is_file():
            actual = canonical_path(candidate, started)
            require(actual.is_relative_to(receipt), "Actual receipt directory confinement")
            key = actual.relative_to(receipt).as_posix()
            require(key not in found, "No aliased actual owned file")
            found.add(key)
            total += actual.stat().st_size
            require(len(found) <= 65 and total <= 128 * 1024**2, "Finite actual receipt cap")
    require(
        found == set(expected) | {"manifest.json"},
        "Exact complete actual owned directory inventory",
    )


def terminal_packet(receipt, schema, pin, frozen, external, started):
    require(
        receipt.is_dir()
        and not any((receipt / name).exists() for name in ("FAILED_UNSEALED.json", "failure.json")),
        "Failed/unsealed markers override every partial summary or manifest",
    )
    path = bind(frozen, external, receipt / "manifest.json", pin, started)
    manifest = read_json(path, started)
    require(
        manifest["schema"] == schema
        and manifest["manifest_self_hash_excluded"] is True
        and manifest["terminal_outcome_file"] == "completion_outcome.json"
        and manifest["completed"] is True
        and manifest["budget_censored"] is False
        and manifest["original_expected_hashes_waived"] is False
        and manifest["verification_and_output_hashing_before_terminal"] is True,
        "Complete uncensored terminal packet with exact original expected hashes",
    )
    same(
        manifest["historical_global_LIVE_integrity"],
        dict(passed=False, mismatch_references=36, distinct_paths=9, expected_hashes_waived=False),
        "Historical global LIVE failures remain separate",
    )
    files = manifest["files"]
    require(type(files) is dict and 0 < len(files) <= 64, "Complete finite receipt-local owned map")
    actual_files(receipt, files, started)
    for key, expected in files.items():
        check(started)
        require(
            type(key) is str and not Path(key).is_absolute() and key != "manifest.json",
            "Recognized receipt-local owner convention",
        )
        actual = bind(frozen, external, receipt / key, expected, started)
        require(
            actual.is_relative_to(receipt) and actual.relative_to(receipt).as_posix() == key,
            "Strict rebase and confinement of every owned byte",
        )
    map_inputs(manifest, frozen, external, started)
    protocol = read_json(receipt / "protocol.json", started)
    for field in ("frozen_inputs", "external_runtime_inputs"):
        require(type(protocol[field]) is dict, "Complete prepared map")
        for key, expected in protocol[field].items():
            check(started)
            require(manifest[field].get(key) == expected, "No prepared input dropped or overridden")
    outcome = read_json(receipt / "completion_outcome.json", started)
    summary = read_json(receipt / "summary.json", started)
    for record in (summary, outcome):
        require(
            record["completed"] is True
            and record["budget_censored"] is False
            and record["new_test_credit"] == 0
            and record["full_G2"] is record["adoption"] is record["cost_transfer"] is False,
            "Complete component-only terminal evidence, zero fixture credit",
        )
        require(record["passed"] is manifest["passed"], "Terminal decision agreement")
    for observation in (
        summary["budget"],
        outcome["budget"],
        manifest["terminal_budget_observation"],
    ):
        require(
            0 <= observation["process_CPU_seconds"] < CPU
            and 0 <= observation["wall_seconds"] < WALL,
            "Actual recorded hard terminal limits",
        )
    same(
        [
            protocol[key]
            for key in ("process_CPU_seconds", "admission_process_CPU_seconds", "wall_seconds")
        ],
        [CPU, ADMISSION, WALL],
        "Unchanged prerequisite and source process budgets",
    )
    return dict(manifest=manifest, protocol=protocol, outcome=outcome, summary=summary)


def polar_prerequisites(implementation, frozen, external, started):
    packets = {}
    for receipt, schema in (
        (POLAR, "box-muller-polar-cdf-bv-terminal-manifest-v1"),
        (POLAR_AUDIT, "box-muller-polar-cdf-bv-independent-audit-manifest-v1"),
    ):
        check(started)
        key = (receipt / "manifest.json").relative_to(ROOT).as_posix()
        packet = terminal_packet(receipt, schema, POLAR_MANIFESTS[key], frozen, external, started)
        require(
            packet["manifest"]["passed"] is True and packet["summary"]["passed"] is True,
            "Both actual root-pinned polar source and independent packets PASS",
        )
        if receipt == POLAR:
            require(
                packet["summary"]["rejection"] is False
                and packet["summary"]["angular_dollar_certificate_retained"] is True,
                "Actual ideal hybrid guard and dollar certificate retained",
            )
        else:
            summary = packet["summary"]
            require(
                summary["independent_audit_passed"] is True
                and summary["ideal_hybrid_component_passed"] is True
                and summary["source_passed"] is True
                and summary["source_rejection_retained"] is False,
                "Actual independent polar approval of the same ideal hybrid component",
            )
        for name, expected in implementation["required_polar_author_SHA256"].items():
            check(started)
            require(
                sha(receipt / "executed_code" / name, started) == expected,
                "Both actual polar executable copies match frozen v3 bytes",
            )
        packets[receipt.name] = dict(
            manifest_sha256=POLAR_MANIFESTS[key],
            protocol=packet["protocol"],
            summary=packet["summary"],
            outcome=packet["outcome"],
        )
    source = {
        name: read_json(POLAR / name, started)
        for name in (
            "source_binding.json",
            "log_radius_envelope.json",
            "angular_guards.json",
            "ideal_hybrid_bounds.json",
        )
    }
    independent = {
        name: read_json(POLAR_AUDIT / name, started)
        for name in (
            "independent_source_binding.json",
            "independent130_log_radius_envelope.json",
            "independent_angular_guards.json",
            "independent130_ideal_hybrid_bounds.json",
        )
    }
    same(
        source["source_binding.json"],
        independent["independent_source_binding.json"],
        "Actual independent complete source/role/root binding",
    )
    return dict(
        packets=packets,
        source=source,
        independent=independent,
        binding=source["source_binding.json"],
        radius=source["log_radius_envelope.json"],
        angular=source["angular_guards.json"],
        price=source["ideal_hybrid_bounds.json"],
    )


def independent_range_step(node, arguments, graph, products):
    op, value = node["op"], node["out"][0]
    if op == "const":
        return (graph.constant(value),) * 2
    if op == "add":
        return (arguments[0][0] + arguments[1][0], arguments[0][1] + arguments[1][1])
    if op == "sub":
        return (arguments[0][0] - arguments[1][1], arguments[0][1] - arguments[1][0])
    if op in ("mul", "cmul"):
        left = arguments[0]
        right = arguments[1] if op == "mul" else (signed_coefficient(node["params"]["c"]),) * 2
        corners = [first * second for first in left for second in right]
        low = (
            0
            if op == "mul" and node["args"][0] == node["args"][1] and left[0] <= 0 <= left[1]
            else min(corners)
        )
        product = (low, max(corners))
        require(
            -(1 << 143) <= product[0] <= product[1] < 1 << 143,
            "Every independently walked eager product is signed144 safe",
        )
        products.append(dict(value=value, product_raw_bounds=list(product)))
        return (product[0] // Q, product[1] // Q)
    if op == "lt":
        return (0, 1)
    if op == "select":
        require(0 <= arguments[0][0] <= arguments[0][1] <= 1, "Actual unscaled native selector")
        return (min(arguments[1][0], arguments[2][0]), max(arguments[1][1], arguments[2][1]))
    if op == "positive":
        return (max(0, arguments[0][0]), max(0, arguments[0][1]))
    if op == "bits":
        params = node["params"]
        require(params["width"] == 72, "Actual complete72 extraction")
        shift, bounds = params["shift"], arguments[0]
        if shift < 0:
            require(params["signed"] is False, "Exact modular left shift only after no-wrap")
            return (bounds[0] << -shift, bounds[1] << -shift)
        require(
            params["signed"] is True or bounds[0] >= 0,
            "Unsigned right extraction source nonnegative",
        )
        return (bounds[0] >> shift, bounds[1] >> shift)
    require(op == "shift", "No uncertified eager primitive outside the original sampler")
    base, exponent = arguments
    require(
        base[0] > 0 and -72 < exponent[0] <= exponent[1] < 72,
        "Positive shift source and bounded full72 exponent",
    )
    return (
        base[0] << exponent[0] if exponent[0] >= 0 else base[0] >> -exponent[0],
        base[1] << exponent[1] if exponent[1] >= 0 else base[1] >> -exponent[1],
    )


def all_emitted_safety(declared, graphs, binding, stocks, native_z, started):
    require(
        declared["schema"] == "original-BM-all-emitted-financial-safety-v1"
        and set(declared["cases"]) == set(CASES),
        "Full two-case emitted safety artifact",
    )
    result = {}
    normal_limit = ceiling(native_z * Q)
    for case in CASES:
        check(started, admission=True)
        graph = graphs[case]
        normals = [
            value
            for row in binding["cases"][case]["joint_pair_scopes"]
            for value in row["normal_values"]
        ]
        sampler = set()
        for value in normals:
            check(started)
            sampler.update(graph.ancestors(value))
        output_scope = graph.ancestors(graph.target["outputs"]["Y"])
        values = {value: word72((-normal_limit, normal_limit)) for value in normals}
        occupied = [row for row in stocks[case]["classes"] if not row["empty"]]
        remainder = (
            min(row["remainder_raw_bounds"][0] for row in occupied),
            max(row["remainder_raw_bounds"][1] for row in occupied),
        )
        scopes = stocks[case]["actual_sites"]
        remainder_ids = {row["remainder"] for row in scopes}
        clips = {row["clipped"]: (row["low"], row["high"]) for row in scopes}
        rows, products, dead = [], [], []
        for node in graph.target["nodes"]:
            check(started)
            if node["op"] != "const" and all(value in sampler for value in node["out"]):
                continue
            require(len(node["out"]) == 1, "Every remaining emitted operation has one output")
            value = node["out"][0]
            require(
                all(arg in values for arg in node["args"]),
                "Finance uses only independently bounded sampler outputs and constants",
            )
            bound = independent_range_step(
                node, [values[arg] for arg in node["args"]], graph, products
            )
            if value in remainder_ids:
                require(node["op"] == "sub", "Only exact original correlated reduction reused")
                bound = remainder
            if value in clips:
                require(node["op"] == "select", "Only actual signed clamp domain reused")
                bound = clips[value]
            values[value] = word72(bound)
            rows.append(
                dict(
                    value=value,
                    op=node["op"],
                    raw_bounds=list(bound),
                    exact_cell_correlation_reused=value in remainder_ids,
                    exact_clamp_domain_reused=value in clips,
                )
            )
            if value not in sampler and value not in output_scope:
                dead.append(value)
        require(
            set(graph.nodes) == sampler | set(values),
            "Every emitted value, including dead powers, has exactly applicable safety",
        )
        own = dict(
            actual_nonsampler_emitted_ranges=rows,
            actual_nonsampler_signed144_products=products,
            actual_dead_emitted_nonsampler_values=dead,
            full_emitted_value_count=len(graph.nodes),
            sampler_closure_value_count=len(sampler),
            all_emitted_dead_paths_and_polynomial_powers_retained=True,
            no_safety_obligation_dropped_as_unreachable_or_knocked_out=True,
            all_product144_and_stored72_guards_passed=True,
        )
        same(
            declared["cases"][case],
            own,
            "Independently traversed full emitted range and product inventory",
        )
        result[case] = own
    return dict(schema="independent130-original-BM-all-emitted-financial-safety-v1", cases=result)


def financial_tail_safety(declared, graph, roles, support, started):
    stock = support["certificate"]["stock_support"]
    bound = word72((stock["lower"], stock["upper"]))
    require(bound[0] > 0, "Actual source-identical universal positive stock support")
    values = {row["stock"]: bound for row in roles["prefix_witnesses"]}
    closure, pending = set(), [graph.target["outputs"]["Y"]]
    while pending:
        check(started)
        value = pending.pop()
        if value in values or value in closure:
            continue
        node = graph.node(value)
        require(
            node["op"] in ("const", "add", "sub", "cmul", "positive", "lt", "select"),
            "Original actual financial-tail primitive set",
        )
        closure.add(value)
        pending.extend(node["args"])
    rows, products = [], []
    for value in sorted(closure):
        check(started)
        node = graph.node(value)
        bound = word72(
            independent_range_step(node, [values[arg] for arg in node["args"]], graph, products)
        )
        values[value] = bound
        rows.append(dict(value=value, op=node["op"], raw_bounds=list(bound)))
    require(
        values[graph.target["outputs"]["Y"]][0] >= 0, "Both eager payoff branches are nonnegative"
    )
    own = dict(
        stock_raw_bounds=[stock["lower"], stock["upper"]],
        actual_eager_tail_nodes=rows,
        actual_full144_products=products,
        all_stored72_and_product144_safe=True,
        both_select_branches_bound=True,
        no_knockout_path_removed=True,
    )
    same(declared, own, "Independent complete eager financial-tail words and products")
    return own


def source_protocol_policy(protocol, implementation, plan, started):
    check(started)
    require(
        protocol["schema"] == "box-muller-native-financial-bridge-protocol-v1"
        and protocol["output"] == SOURCE.relative_to(ROOT).as_posix()
        and protocol["producer_module"]
        == "research.limitation_program_20261001.experiment_box_muller_native_financial_bridge",
        "Exact original native-financial prepared source",
    )
    for field in (
        "immutable_author_sha256",
        "method_document_SHA256",
        "required_polar_manifest_SHA256",
        "required_polar_author_SHA256",
        "additional_native_root_provenance_SHA256",
        "original_root_owner_manifest_SHA256",
    ):
        key = "author_sha256" if field == "immutable_author_sha256" else field
        same(protocol[field], implementation[key], "Exact prepared source prerequisite: " + field)
    same(
        protocol["selected_source_SHA256"],
        plan["original_selected_source_pins_from_existing_manifest_metadata"],
        "Every fixed original selected source pin",
    )
    require(
        protocol["primary_interval_decimal_digits"] == 90
        and protocol["independent_interval_decimal_digits"] == DIGITS
        and protocol["numerical_threads"] == 1
        and protocol["fixture_credit"] == 0
        and protocol["cosine_512_envelope_in_scope"] is True
        and protocol["cosine_512_envelope_computed_in_prepare"] is False,
        "Fixed complete native bridge and deferred numerical execution",
    )
    for field in (
        "startup_B_required",
        "pure_Python_mpmath_backend_required",
        "runtime_and_source_frozen_before_kernel_import",
        "no_numerical_kernel_source_walk_or_bound_executed_in_prepare",
    ):
        require(protocol[field] is True, "Prepared source runtime/kernel scope: " + field)
    require(
        protocol["clock_policy"]["CPU_includes_actual_process_bootstrap"] is True
        and protocol["clock_policy"]["wall_includes_actual_GetProcessTimes_creation"] is True,
        "Original whole-process CPU and creation-derived wall clocks",
    )


def source_packet(implementation, frozen, external, started):
    plan, origins, roots, history = method_origins(implementation, frozen, external, started)
    polar = polar_prerequisites(implementation, frozen, external, started)
    pin = sha(SOURCE / "manifest.json", started)
    packet = terminal_packet(
        SOURCE,
        "box-muller-native-financial-bridge-terminal-manifest-v1",
        pin,
        frozen,
        external,
        started,
    )
    source_protocol_policy(packet["protocol"], implementation, plan, started)
    summary, outcome = packet["summary"], packet["outcome"]
    fit = summary["financial_residual_fit"]
    require(
        type(fit) is bool
        and summary["native_financial_bias_certificate_valid"] is True
        and summary["passed"] is fit
        and summary["rejection"] is (not fit)
        and summary["status"]
        == (
            "native_financial_bias_component_passed"
            if fit
            else "certificate_method_rejected_residual"
        )
        and summary["independent_audit_still_required"] is True,
        "Source proof validity is separate from the exact residual-fit decision",
    )
    require(
        outcome["native_financial_bias_certificate_valid"] is True
        and outcome["financial_residual_fit"] is fit
        and outcome["rejection"] is (not fit),
        "Complete source decision includes useful mathematical cost-budget rejection",
    )
    require(
        summary["actual_stock_sites"] == 464
        and summary["fresh_cosine_coefficients_checked"] == 512
        and summary["retained_stock_exponent_classes"] == 60
        and summary["all_fixture_credit"] == summary["new_gate_replays"] == 0
        and summary["basis_or_circuit_or_price_estimator_replays"] == 0
        and summary["source_expected_hashes_waived"] is False
        and summary["estimator_99percent_delivery_certified"] is False
        and summary["matched_classical_or_quantum_advantage_claimed"] is False
        and summary["residual_spent_or_reallocated"] is False,
        "Actual complete scope, zero numerical-test or adoption credit",
    )
    same(
        summary["unchanged_financial_residual"],
        encode(ALLOWANCE),
        "Unchanged source dollar allowance",
    )
    same(
        summary["actual_joint_pair_counts"],
        {case: values[2] for case, values in CASES.items()},
        "Every original shared pair retained",
    )
    for path in (AUTHOR, PRODUCER_AUTHOR, IMPLEMENTATION, IMPLEMENTATION_DOC, METHOD, METHOD_DOC):
        require(
            sha(SOURCE / "executed_code" / path.name, started) == sha(path, started),
            "Actual immutable executed source copies equal reviewed current bytes",
        )
    same(
        read_json(SOURCE / "selected_source_origins.json", started),
        origins,
        "All original selected origins",
    )
    same(
        read_json(SOURCE / "native_root_provenance.json", started),
        roots,
        "All actual original root origins",
    )
    same(
        read_json(SOURCE / "operational_provenance.json", started),
        history,
        "Complete original zero-credit history",
    )
    # Compare the producer's declared packet shape, without local convenience keys.
    same(
        read_json(SOURCE / "polar_prerequisites.json", started),
        {key: polar[key] for key in ("packets", "source", "independent")},
        "Actual passed polar packets and all preserved primary/independent artifacts",
    )
    verify_runtime(packet["protocol"]["interpreter"], frozen, external, started)
    prepared = read_json(SOURCE / "PREPARED_RECEIPT.json", started)
    require(
        prepared["prepared"] is True
        and prepared["terminal"] is False
        and prepared["protocol_sha256"] == sha(SOURCE / "protocol.json", started),
        "Actual immutable original source preparation",
    )
    return plan, packet, polar


def seal(output, frozen, external, started, outcome):
    require(
        not any(
            (output / name).exists()
            for name in ("manifest.json", "completion_outcome.json", "FAILED_UNSEALED.json")
        ),
        "One exclusive terminal outcome, no retry or partial-success reseal",
    )
    verified = final_fresh(frozen, external, started)
    outcome = dict(
        outcome,
        verification_unique_paths=verified,
        budget=elapsed(started),
        limits_CPU_admission_wall=[CPU, ADMISSION, WALL],
        new_test_credit=0,
        all_fixture_credit=0,
        full_G2=False,
        cost_transfer=False,
        adoption=False,
    )
    write_json(output / "completion_outcome.json", outcome, started)
    files = owned_artifacts(output, started)
    check(started)
    write_json(
        output / "manifest.json",
        dict(
            schema="box-muller-native-financial-bridge-independent-audit-manifest-v1",
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
        return  # Root preserves the real pre-mkdir exception; no fabricated preparation.
    try:
        require(
            not any(
                (output / name).exists() for name in ("manifest.json", "completion_outcome.json")
            ),
            "Existing or partial terminal blocks failure resealing",
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
                independent_audit_passed=False,
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
                native_financial_bias_certificate_valid=False,
                financial_residual_fit=False,
                budget_censored=isinstance(error, BudgetCensoredError),
                phase=phase,
                failure_file="failure.json",
            ),
        )
    except BaseException:
        # No scans, hashes or dynamic JSON after exhaustion; this overrides partial success.
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
        require(output == OUTPUT and not output.exists(), "Fresh exact independent bridge receipt")
        require("mpmath" not in sys.modules, "Standard-library-only preparation")
        implementation = implementation_policy(started)
        plan, source, _ = source_packet(implementation, frozen, external, started)
        interpreter = runtime_inventory(frozen, external, started)
        verify_runtime(interpreter, frozen, external, started)
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
        write_json(output / "interpreter.json", interpreter, started)
        verified = final_fresh(frozen, external, started)
        check(started, admission=True)
        protocol = dict(
            schema="box-muller-native-financial-bridge-independent-audit-protocol-v1",
            output=output.relative_to(ROOT).as_posix(),
            source=SOURCE.relative_to(ROOT).as_posix(),
            source_manifest_sha256=sha(SOURCE / "manifest.json", started),
            independent_auditor_module="research.limitation_program_20261001.audit_box_muller_native_financial_bridge",
            prepared_UTC=datetime.now(timezone.utc).isoformat(),
            frozen_inputs=frozen,
            external_runtime_inputs=external,
            interpreter=interpreter,
            immutable_author_sha256=implementation["author_sha256"],
            method_document_SHA256=implementation["method_document_SHA256"],
            required_polar_manifest_SHA256=POLAR_MANIFESTS,
            required_polar_author_SHA256=implementation["required_polar_author_SHA256"],
            selected_source_SHA256=plan[
                "original_selected_source_pins_from_existing_manifest_metadata"
            ],
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
            scientific_producer_or_helper_imports=False,
            cosine_512_envelope_in_scope=True,
            cosine_512_envelope_computed_in_prepare=False,
            source_financial_residual_fit=source["summary"]["financial_residual_fit"],
            source_native_financial_bias_certificate_valid=True,
            final_fresh_preparation_verified_paths=verified,
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
        check(started)
        return dict(prepared=True, terminal=False, new_test_credit=0)
    except BaseException as error:
        if created:
            retain_failure(output, frozen, external, started, error, "prepare")
        raise


def audit_protocol_policy(protocol, implementation, plan, source, started):
    check(started)
    require(
        protocol["schema"] == "box-muller-native-financial-bridge-independent-audit-protocol-v1"
        and protocol["output"] == OUTPUT.relative_to(ROOT).as_posix()
        and protocol["source"] == SOURCE.relative_to(ROOT).as_posix()
        and protocol["independent_auditor_module"]
        == "research.limitation_program_20261001.audit_box_muller_native_financial_bridge",
        "Exact prepared independent bridge scope",
    )
    same(
        [
            protocol[key]
            for key in ("process_CPU_seconds", "admission_process_CPU_seconds", "wall_seconds")
        ],
        [CPU, ADMISSION, WALL],
        "Same all-inclusive independent clock budget",
    )
    require(
        protocol["independent_interval_decimal_digits"] == DIGITS
        and protocol["primary_interval_decimal_digits"] == 90
        and protocol["numerical_threads"] == 1
        and protocol["fixture_credit"] == 0
        and protocol["scientific_producer_or_helper_imports"] is False
        and protocol["cosine_512_envelope_computed_in_prepare"] is False
        and protocol["source_financial_residual_fit"]
        is source["summary"]["financial_residual_fit"],
        "Fixed independent130 and exact residual source decision",
    )
    for key in (
        "startup_B_required",
        "pure_Python_mpmath_backend_required",
        "runtime_and_source_frozen_before_kernel_import",
        "cosine_512_envelope_in_scope",
        "source_native_financial_bias_certificate_valid",
        "no_source_kernel_proof_interval_or_bound_executed_in_prepare",
    ):
        require(protocol[key] is True, "Prepared independent premise: " + key)
    for field, expected in (
        ("immutable_author_sha256", implementation["author_sha256"]),
        ("method_document_SHA256", implementation["method_document_SHA256"]),
        ("required_polar_manifest_SHA256", POLAR_MANIFESTS),
        ("required_polar_author_SHA256", implementation["required_polar_author_SHA256"]),
        (
            "selected_source_SHA256",
            plan["original_selected_source_pins_from_existing_manifest_metadata"],
        ),
        ("additional_native_root_provenance_SHA256", ROOT_PINS),
        ("original_root_owner_manifest_SHA256", ROOT_OWNERS),
    ):
        same(protocol[field], expected, "Exact immutable audit prerequisite: " + field)
    require(
        protocol["source_manifest_sha256"] == sha(SOURCE / "manifest.json", started),
        "Prepared complete source packet cannot change",
    )
    require(
        protocol["clock_policy"]["CPU_includes_actual_process_bootstrap"] is True
        and protocol["clock_policy"]["wall_includes_actual_GetProcessTimes_creation"] is True,
        "Independent CPU/wall charge actual startup",
    )


def run(output):
    started = start_clock()
    frozen, external, admitted = {}, {}, False
    try:
        initialize(started)
        require(output == OUTPUT and output.is_dir(), "Exact prepared independent bridge receipt")
        require(
            not any(
                (output / name).exists()
                for name in (
                    "manifest.json",
                    "run_started.json",
                    "completion_outcome.json",
                    "FAILED_UNSEALED.json",
                    "failure.json",
                )
            ),
            "No reused run, failed preparation or partial terminal",
        )
        admitted = True
        protocol = read_json(output / "protocol.json", started)
        prepared = read_json(output / "PREPARED_RECEIPT.json", started)
        require(
            prepared["prepared"] is True
            and prepared["terminal"] is False
            and prepared["protocol_sha256"] == sha(output / "protocol.json", started),
            "Immutable actual independent preparation",
        )
        map_inputs(protocol, frozen, external, started)
        for name in ("protocol.json", "PREPARED_RECEIPT.json", "interpreter.json"):
            bind(frozen, external, output / name, sha(output / name, started), started)
        implementation = implementation_policy(started)
        plan, source, polar = source_packet(implementation, frozen, external, started)
        audit_protocol_policy(protocol, implementation, plan, source, started)
        interpreter = read_json(output / "interpreter.json", started)
        same(interpreter, protocol["interpreter"], "Exact prepared independent runtime record")
        verify_runtime(interpreter, frozen, external, started)
        loaded_origins(frozen, external, started)
        verify_maps(frozen, external, started)
        check(started, admission=True)
        write_json(
            output / "run_started.json",
            dict(
                UTC=datetime.now(timezone.utc).isoformat(),
                process_id=os.getpid(),
                limits=[CPU, ADMISSION, WALL],
            ),
            started,
        )
        require(
            "mpmath" not in sys.modules,
            "Lazy pure-Python interval import after full byte admission",
        )
        import mpmath as mp

        require(
            mp.__version__ == "1.3.0" and sys.modules["mpmath.libmp.backend"].BACKEND == "python",
            "Actual fixed pure-Python mpmath backend, no optional backend",
        )
        mp.iv.dps, mp.mp.dps = DIGITS, DIGITS
        loaded_origins(frozen, external, started)
        check(started, admission=True)
        binding, _, _ = source_inventory(started)
        same(
            binding,
            polar["binding"],
            "Fresh independent full typed source, pair, role and root binding",
        )
        same(
            binding,
            read_json(SOURCE / "native_source_binding.json", started),
            "Actual original primary financial source",
        )
        write_json(output / "independent_native_source_binding.json", binding, started)
        graphs, roles, scopes, supports = {}, {}, {}, {}
        for case in CASES:
            check(started, admission=True)
            graphs[case], roles[case], scopes[case] = stock_templates(binding, case, started)
            supports[case] = original_support(
                graphs[case], roles[case], scopes[case], case, started
            )
        same(
            supports,
            read_json(SOURCE / "original_support_evidence.json", started),
            "Every original E03 support literal/template and fresh strict native support cap",
        )
        write_json(output / "independent_original_support_evidence.json", supports, started)
        B, DS = (
            rational(polar["radius"][key])
            for key in ("internal_radius_upper", "squared_radius_KS_upper")
        )
        require(0 < B and 0 <= DS <= 1, "Actual audited polar radius/law premises")
        table = graphs["B4x12"].target["tables"]["cos"]
        same(
            table,
            graphs["B8x52"].target["tables"]["cos"],
            "Same512 original actual cosine literals",
        )
        check(started, admission=True)
        own_cos, _, _ = cosine_certificate(mp, table, B, started)
        declared_cos = read_json(SOURCE / "cosine_envelope.json", started)
        delta, native_z = compare_cosine(declared_cos, own_cos, B, table, started)
        write_json(output / "independent130_cosine_envelope.json", own_cos, started)
        prefixes = read_json(SOURCE / "raw_log_prefix_envelopes.json", started)
        stocks = read_json(SOURCE / "stock_exponential_envelopes.json", started)
        bands = read_json(SOURCE / "closed_barrier_bands.json", started)
        smooth = read_json(SOURCE / "smooth_payoff_bounds.json", started)
        complete = read_json(SOURCE / "complete_financial_bounds.json", started)
        require(
            prefixes["schema"] == "original-BM-raw-log-prefix-envelopes-v1"
            and stocks["schema"] == "original-BM-stock-exponential-envelopes-v1"
            and bands["schema"] == "original-BM-closed-barrier-band-envelopes-v1"
            and smooth["schema"] == "original-BM-smooth-payoff-envelopes-v1",
            "Actual fixed complete primary financial artifact schemas",
        )
        for record in (prefixes, stocks, bands, smooth):
            require(
                record["interval_digits"] == 90 and set(record["cases"]) == set(CASES),
                "Fixed primary90 and both full original contracts",
            )
        same(
            prefixes["pinned_internal_radius_upper"], encode(B), "Same actual polar radius premise"
        )
        same(
            prefixes["remaining_coordinate_error_upper"],
            encode(delta),
            "Only fresh original coordinate remainder",
        )
        same(
            bands["pinned_squared_radius_KS_upper"],
            encode(DS),
            "Same actual polar radial law premise",
        )
        require(
            bands["pair_transport_order"] == "CURRENT_RADIUS_THEN_CURRENT_ANGLE"
            and bands["actual_point_value_BV_convention"] is True,
            "Whole-pair radius-first proof and actual values at all atoms",
        )
        own_stocks, own_prefixes, own_bands, own_smooth, bridges = {}, {}, {}, {}, {}
        for case, (assets, dates, _) in CASES.items():
            check(started, admission=True)
            normal_ids = [
                value
                for row in binding["cases"][case]["joint_pair_scopes"]
                for value in row["normal_values"]
            ]
            own_stock = stock_certificate(mp, graphs[case], roles[case], scopes[case], started)
            alpha = compare_stock_record(
                mp,
                stocks["cases"][case],
                own_stock,
                graphs[case],
                scopes[case],
                supports[case],
                started,
            )
            own_raw, raw_values = raw_log_certificate(
                mp, graphs[case], roles[case], normal_ids, native_z, delta, B, started
            )
            lambdas = compare_raw_record(
                prefixes["cases"][case],
                own_raw,
                graphs[case],
                roles[case],
                raw_values,
                delta,
                native_z,
                B,
                started,
            )
            own_band, switch = audit_closed_bands(
                mp,
                bands["cases"][case],
                own_stock,
                alpha,
                lambdas,
                roles[case],
                raw_values,
                DS,
                polar,
                started,
            )
            financial_tail_safety(
                bands["cases"][case]["eager_financial_tail_safety"],
                graphs[case],
                roles[case],
                supports[case],
                started,
            )
            own_mean, zeta = audit_smooth(
                mp,
                smooth["cases"][case],
                bands["cases"][case],
                supports[case],
                assets,
                dates,
                started,
            )
            own_stocks[case], own_prefixes[case], own_bands[case], own_smooth[case] = (
                own_stock,
                own_raw,
                own_band,
                own_mean,
            )
            bridges[case] = (zeta, switch)
        safety = all_emitted_safety(
            read_json(SOURCE / "all_emitted_financial_safety.json", started),
            graphs,
            binding,
            stocks["cases"],
            native_z,
            started,
        )
        verified_complete, fit = audit_complete(complete, polar, bridges, started)
        require(
            source["summary"]["financial_residual_fit"] is fit
            and source["summary"]["passed"] is fit
            and source["summary"]["rejection"] is (not fit),
            "Independent final fit decision equals recorded source outcome",
        )
        same(
            source["summary"]["case_dollars_upper"],
            {
                case: row["verified_primary_total_upper"]
                for case, row in verified_complete["cases"].items()
            },
            "Source summary reproduces independently authorized exact complete bounds",
        )
        obligations = read_json(SOURCE / "method_obligations.json", started)
        for key in (
            "actual_point_value_BV_convention",
            "radial_closed_band",
            "angular_closed_band",
            "whole_pair_transport",
            "continuous_anti_concentration",
            "clipping_and_band",
            "survival_and_smooth",
            "pay_once",
        ):
            require(
                type(obligations[key]) is str and obligations[key],
                "Explicit primary proof obligation retained",
            )
        require(
            obligations["native_convexity_or_unimodality_claimed"] is False
            and obligations["AS241_theorem_imported"] is False,
            "No native rounded convexity or unrelated scalar theorem assumed",
        )
        for name, value in (
            ("independent130_stock_exponential_envelopes.json", own_stocks),
            ("independent130_raw_log_prefix_envelopes.json", own_prefixes),
            ("independent130_closed_barrier_bands.json", own_bands),
            ("independent130_smooth_payoff_bounds.json", own_smooth),
            ("independent_all_emitted_financial_safety.json", safety),
            ("independent_complete_financial_bounds.json", verified_complete),
            ("independent_transport_derivation.json", independent_bridge_derivation()),
        ):
            write_json(output / name, value, started)
        verify_runtime(interpreter, frozen, external, started)
        write_json(
            output / "loaded_module_origins.json",
            loaded_origins(frozen, external, started),
            started,
        )
        summary = dict(
            schema="original-BM-native-financial-bridge-independent-audit-summary-v1",
            completed=True,
            passed=True,
            independent_audit_passed=True,
            budget_censored=False,
            native_financial_bias_certificate_valid=True,
            financial_residual_fit=fit,
            native_financial_bias_component_passed=fit,
            source_passed=fit,
            source_rejection_retained=not fit,
            source_manifest_sha256=sha(SOURCE / "manifest.json", started),
            unchanged_financial_residual=encode(ALLOWANCE),
            actual_joint_pair_counts={case: values[2] for case, values in CASES.items()},
            actual_stock_sites=464,
            independently_checked_cosine_coefficients=512,
            independent_retained_stock_exponent_classes=60,
            independently_verified_case_dollars_upper={
                case: row["verified_primary_total_upper"]
                for case, row in verified_complete["cases"].items()
            },
            complete_primary_bound_authorized_by_independent130=True,
            all_actual_native_emitted_dead_paths_product144_and_stored72_safe=True,
            primary_own_error_inputs_used_for_independent_clip_guards=True,
            actual_point_values_and_all_closed_endpoint_ties_retained=True,
            no_old_radius_Holder_log_root_grid_or_cutoff_term_added_again=True,
            source_expected_hashes_waived=False,
            new_test_credit=0,
            all_fixture_credit=0,
            new_gate_replays=0,
            scientific_producer_or_helper_imports=False,
            full_G2=False,
            adoption=False,
            cost_transfer=False,
            estimator_99percent_delivery_certified=False,
            matched_classical_or_quantum_advantage_claimed=False,
            residual_spent_or_reallocated=False,
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
                native_financial_bias_certificate_valid=True,
                financial_residual_fit=fit,
                native_financial_bias_component_passed=fit,
                source_passed=fit,
                source_rejection_retained=not fit,
                rejection=False,
                budget_censored=False,
                phase="run",
                summary_file="summary.json",
            ),
        )
        return summary
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
    require(output == OUTPUT, "Only the exact new independent bridge receipt")
    result = prepare(output) if args.operation == "prepare" else run(output)
    print(
        json.dumps(
            dict(
                operation=args.operation,
                output=output.relative_to(ROOT).as_posix(),
                prepared=args.operation == "prepare",
                passed=result.get("passed"),
                new_test_credit=0,
            )
        )
    )


if __name__ == "__main__":
    main()
