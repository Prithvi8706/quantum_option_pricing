"""Independent actual-SSA audit of the E03 native payoff support certificates.

This reader never imports the support-proof generator. It discovers every stock
from the actual financial sum/max DAG, partitions its clipped integer input by
binary search, and propagates each original SSA operation with fixed reduction
integer. No financial gate replay, candidate search or price-error claim occurs.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
PRODUCER = PROGRAM / "E03_support_run001"
BASELINE = PROGRAM / "A10_coefficient_run001"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, data):
    Path(path).write_text(json.dumps(data, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def relative(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def verify(frozen):
    for name, expected in frozen.items():
        if sha(ROOT / name) != expected:
            raise AssertionError("Support audit frozen input changed: " + name)


def prepare(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM)
    if output.exists():
        raise FileExistsError("Independent support audit receipt must be fresh")
    manifest = read(PRODUCER / "manifest.json")
    frozen = {}
    for field in ("files", "frozen_inputs"):
        for name, expected in manifest[field].items():
            if sha(ROOT / name) != expected:
                raise AssertionError("Producer receipt changed: " + name)
            frozen[name] = expected
    for path in (Path(__file__), PRODUCER / "manifest.json", Path(sys.executable)):
        # The interpreter is separately recorded; input files use workspace paths.
        if path == Path(sys.executable):
            continue
        frozen[relative(path)] = sha(path)
    output.mkdir()
    shutil.copy2(Path(__file__), output / "executed_audit_native_payoff_support.py")
    protocol = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "local_only": True,
        "before_audit_execution": True,
        "independent_of_support_proof_generator": True,
        "method": "Discover financial stock leaves through actual sum/max/output DAG; "
        "canonicalize actual stock SSA templates; binary-search integer reduction-cell "
        "boundaries; propagate actual SSA operations with the cell's fixed integer; "
        "prove positivity/no overflow, then apply actual strict barrier and coefficients.",
        "cases": ["B4x12", "B8x52"],
        "stop_rule": "One exact actual-SSA audit per frozen target and one producer XML "
        "reconciliation; no new financial execution or candidate search",
        "frozen_inputs": frozen,
        "executable": sys.executable,
        "interpreter_sha256": sha(sys.executable),
        "new_test_cases": 0,
        "new_financial_gate_replays": 0,
    }
    save(output / "protocol.json", protocol)
    verify(frozen)
    print("Independent E03 support audit protocol frozen", flush=True)


class ActualGraph:
    def __init__(self, target):
        self.target = target
        self.width, self.fraction = target["width"], target["fraction_bits"]
        self.quantum = 1 << self.fraction
        self.limit = 1 << (self.width - 1)
        self.modulus = 1 << self.width
        self.producer = {v: n for n in target["nodes"] for v in n["out"]}
        assert len(self.producer) == sum(len(n["out"]) for n in target["nodes"])
        self.index = {v: i for i, n in enumerate(target["nodes"]) for v in n["out"]}

    def node(self, value, operation):
        node = self.producer[value]
        assert node["op"] == operation, (value, node["op"], operation)
        return node

    def literal(self, value):
        raw = int(self.node(value, "const")["params"]["value"])
        raw %= self.modulus
        return raw - self.modulus if raw >= self.limit else raw

    def safe(self, pair):
        assert -self.limit <= pair[0] <= pair[1] < self.limit, pair
        return pair

    def sum_leaves(self, value):
        node = self.producer[value]
        if node["op"] != "add":
            return [value]
        return [leaf for arg in node["args"] for leaf in self.sum_leaves(arg)]

    def max_leaves(self, value):
        node = self.producer[value]
        if node["op"] != "select":
            return [value]
        flag, right, left = node["args"]
        compare = self.node(flag, "lt")
        assert compare["args"] == [left, right], "Maximum loses original signed ordering"
        return self.max_leaves(left) + self.max_leaves(right)

    def clipping(self, clipped):
        flag, maximum, high = self.node(clipped, "select")["args"]
        assert self.node(flag, "lt")["args"] == [maximum, high]
        lower_flag, low, raw = self.node(maximum, "select")["args"]
        assert self.node(lower_flag, "lt")["args"] == [raw, low]
        lo, hi = self.literal(low), self.literal(high)
        assert lo < hi
        return lo, hi

    def stock_template(self, stock):
        polynomial, exponent = self.node(stock, "shift")["args"]
        bits = self.node(exponent, "bits")
        assert bits["params"] == {"shift": self.fraction, "width": self.width, "signed": True}
        inverse = self.node(bits["args"][0], "cmul")
        clipped = inverse["args"][0]
        low, high = self.clipping(clipped)
        coefficient = inverse["params"]["c"]
        assert coefficient > 0
        self.safe((low * coefficient // self.quantum, high * coefficient // self.quantum))
        selected, todo = set(), [stock]
        while todo:
            value = todo.pop()
            if value == clipped or value in selected:
                continue
            selected.add(value)
            node = self.producer[value]
            assert len(node["out"]) == 1
            assert node["op"] in {"const", "cmul", "bits", "sub", "mul", "add", "shift"}
            todo.extend(node["args"])
        ordered = sorted(selected, key=self.index.__getitem__)
        reduced = [
            self.producer[value]
            for value in selected
            if self.producer[value]["op"] == "sub" and self.producer[value]["args"][0] == clipped
        ]
        assert len(reduced) == 1
        logarithm_product = self.node(reduced[0]["args"][1], "cmul")
        scaled = self.node(logarithm_product["args"][0], "bits")
        assert scaled["args"] == [exponent]
        assert scaled["params"] == {"shift": -self.fraction, "width": self.width, "signed": False}
        ln2 = logarithm_product["params"]["c"]
        assert ln2 > 0
        signatures = {clipped: ["clipped-native-word"]}
        for value in ordered:
            node = self.producer[value]
            signatures[value] = [
                node["op"],
                node["params"],
                [signatures[arg] for arg in node["args"]],
            ]
        signature = hashlib.sha256(
            json.dumps(signatures[stock], sort_keys=True).encode()
        ).hexdigest()
        return {
            "stock": stock,
            "clipped": clipped,
            "polynomial": polynomial,
            "exponent": exponent,
            "low": low,
            "high": high,
            "inverse_ln2": coefficient,
            "ln2": ln2,
            "values": ordered,
            "signature": signature,
            "literal_coefficients": sorted(
                {self.literal(value) for value in selected if self.producer[value]["op"] == "const"}
            ),
        }

    def stock_cells(self, template):
        low, high = template["low"], template["high"]
        coefficient = template["inverse_ln2"]

        def exponent_at(value):
            return (value * coefficient // self.quantum) // self.quantum

        def first_at_least(exponent):
            left, right = low, high + 1
            while left < right:
                middle = (left + right) // 2
                if exponent_at(middle) >= exponent:
                    right = middle
                else:
                    left = middle + 1
            return left

        rows = []
        for k in range(exponent_at(low), exponent_at(high) + 1):
            lo, hi = first_at_least(k), first_at_least(k + 1) - 1
            assert lo <= hi and exponent_at(lo) == exponent_at(hi) == k
            bounds = {template["clipped"]: (lo, hi)}
            for value in template["values"]:
                node, operation = self.producer[value], self.producer[value]["op"]
                args = [bounds[arg] for arg in node["args"]]
                params = node["params"]
                if operation == "const":
                    pair = (self.literal(value),) * 2
                elif operation == "cmul":
                    products = [endpoint * params["c"] for endpoint in args[0]]
                    pair = (min(products) // self.quantum, max(products) // self.quantum)
                elif operation == "bits":
                    shift = params["shift"]
                    assert params["width"] == self.width
                    if shift >= 0:
                        assert params["signed"]
                        pair = (args[0][0] >> shift, args[0][1] >> shift)
                    else:
                        # A negative signed word is first interpreted unsigned.
                        # Full-width modular left shift cancels that modulus;
                        # the following native-range check recovers signed value.
                        pair = (args[0][0] << -shift, args[0][1] << -shift)
                elif operation == "sub":
                    pair = (args[0][0] - args[1][1], args[0][1] - args[1][0])
                elif operation == "add":
                    pair = (args[0][0] + args[1][0], args[0][1] + args[1][1])
                elif operation == "mul":
                    if node["args"][0] == node["args"][1]:
                        a, b = args[0]
                        products = (a * a, b * b)
                        lower = 0 if a <= 0 <= b else min(products)
                        pair = (lower // self.quantum, max(products) // self.quantum)
                    else:
                        products = [a * b for a in args[0] for b in args[1]]
                        pair = (min(products) // self.quantum, max(products) // self.quantum)
                else:
                    assert operation == "shift" and args[1] == (k, k)
                    assert -self.width < k < self.width and args[0][0] >= 0
                    pair = tuple(
                        endpoint << k if k >= 0 else endpoint >> -k for endpoint in args[0]
                    )
                bounds[value] = self.safe(pair)
            assert bounds[template["exponent"]] == (k, k)
            polynomial = bounds[template["polynomial"]]
            stock = bounds[template["stock"]]
            assert 0 < stock[0] <= stock[1]
            rows.append(
                {
                    "k": k,
                    "clipped_log_interval": [lo, hi],
                    "polynomial_interval": list(polynomial),
                    "stock_interval": list(stock),
                    "native_intermediates_checked": len(template["values"]),
                    "maximum_absolute_native_intermediate": max(
                        abs(endpoint) for pair in bounds.values() for endpoint in pair
                    ),
                }
            )
        assert rows[0]["clipped_log_interval"][0] == low
        assert rows[-1]["clipped_log_interval"][1] == high
        assert all(
            a["clipped_log_interval"][1] + 1 == b["clipped_log_interval"][0]
            for a, b in zip(rows, rows[1:])
        )
        return rows


def audit_case(target, certificate, assets, dates):
    graph = ActualGraph(target)
    assert (graph.width, graph.fraction) == (72, 40)
    output = graph.node(target["outputs"]["Y"], "select")
    alive, discounted, zero = output["args"]
    assert graph.literal(zero) == 0
    alive_node = graph.node(alive, "lt")
    maximum, barrier_value = alive_node["args"]
    barrier = graph.literal(barrier_value)
    basket_values = graph.max_leaves(maximum)
    assert len(basket_values) == dates and len(set(basket_values)) == dates
    stocks_by_date = []
    for basket_value in basket_values:
        basket = graph.node(basket_value, "cmul")
        assert basket["params"]["c"] * assets == graph.quantum
        stocks = graph.sum_leaves(basket["args"][0])
        assert len(stocks) == assets
        stocks_by_date.append(stocks)
    stocks = [value for row in stocks_by_date for value in row]
    assert len(set(stocks)) == assets * dates
    assert set(stocks) == set(certificate["stock_ids"])
    templates = [graph.stock_template(value) for value in stocks]
    assert len({template["signature"] for template in templates}) == 1
    assert set(t["clipped"] for t in templates) == set(certificate["clipped_log_ids"])
    for template in templates:
        assert [template["low"], template["high"]] == certificate["clipped_log_integer_bounds"]
        assert template["inverse_ln2"] == certificate["literal_inverse_ln2"]
        assert template["ln2"] == certificate["literal_ln2"]
        assert template["literal_coefficients"] == sorted(
            set(certificate["literal_exp_coefficients"])
        )
    cells = graph.stock_cells(templates[0])
    for actual, saved in zip(cells, certificate["stock_support"]["cells"], strict=True):
        for field in ("k", "clipped_log_interval", "polynomial_interval", "stock_interval"):
            assert actual[field] == saved[field], (field, actual[field], saved[field])
    stock_min = min(row["stock_interval"][0] for row in cells)
    stock_max = max(row["stock_interval"][1] for row in cells)
    assert (stock_min, stock_max) == (
        certificate["stock_support"]["lower"],
        certificate["stock_support"]["upper"],
    )
    total_max = assets * dates * stock_max
    graph.safe((0, total_max))
    graph.safe((0, assets * stock_max))
    discount_node = graph.node(discounted, "cmul")
    discount = discount_node["params"]["c"]
    positive_node = graph.node(discount_node["args"][0], "positive")
    subtract = graph.node(positive_node["args"][0], "sub")
    average, strike_value = subtract["args"]
    strike = graph.literal(strike_value)
    average_node = graph.node(average, "cmul")
    average_coefficient = average_node["params"]["c"]
    assert Counter(graph.sum_leaves(average_node["args"][0])) == Counter(stocks)
    assert 0 < average_coefficient <= graph.quantum and 0 < discount <= graph.quantum
    assert 0 <= strike < barrier < graph.limit
    unconditional_average_max = total_max * average_coefficient // graph.quantum
    graph.safe((0, unconditional_average_max))
    graph.safe((-strike, unconditional_average_max - strike))
    graph.safe((0, max(0, unconditional_average_max - strike)))
    graph.safe((0, max(0, unconditional_average_max - strike) * discount // graph.quantum))
    # Positive stocks make every sum ordinary; the max DAG is actual signed max.
    # floor(S/assets)<H is equivalent to S<assets*H for integer S,H.
    surviving_total = dates * (assets * barrier - 1)
    surviving_average = surviving_total * average_coefficient // graph.quantum
    upper = max(0, surviving_average - strike) * discount // graph.quantum
    graph.safe((0, upper))
    assert certificate["surviving_stock_sum_upper"] == surviving_total
    assert certificate["surviving_average_upper"] == surviving_average
    assert certificate["payoff_raw_bounds"] == [0, upper]
    assert certificate["basket_coefficient"] == graph.quantum // assets
    assert certificate["strict_barrier_raw"] == barrier and certificate["strike_raw"] == strike
    assert certificate["average_coefficient"] == average_coefficient
    assert certificate["discount_coefficient"] == discount
    span_bits = upper.bit_length()
    assert certificate["selector_random_bits"] == span_bits == 46
    assert certificate["selector_span_raw"] == 1 << span_bits
    assert certificate["selector_span_dollars_rational"] == [1 << span_bits, graph.quantum]
    assert certificate["dollar_bounds_rational"] == [[0, 1], [upper, graph.quantum]]
    return {
        "passed": True,
        "assets": assets,
        "dates": dates,
        "actual_stock_templates_checked": len(templates),
        "actual_stock_template_signature": templates[0]["signature"],
        "range_reduction_cells": cells,
        "stock_raw_bounds": [stock_min, stock_max],
        "all_stock_native_intermediates_no_overflow": True,
        "all_actual_sum_max_average_subtract_discount_nodes_safe": True,
        "unconditional_average_upper": unconditional_average_max,
        "strict_survival_total_upper": surviving_total,
        "payoff_raw_bounds": [0, upper],
        "selector_bits": span_bits,
        "selector_dollar_span": (1 << span_bits) // graph.quantum,
        "finite_samples_used": False,
        "new_financial_gate_replays": 0,
    }


def run(output):
    output = Path(output).resolve()
    protocol = read(output / "protocol.json")
    if (output / "summary.json").exists():
        raise FileExistsError("Executed audit cannot be rerun")
    verify(protocol["frozen_inputs"])
    assert sha(sys.executable) == protocol["interpreter_sha256"]
    cases = []
    for assets, dates, case in ((4, 12, "B4x12"), (8, 52, "B8x52")):
        target = read(BASELINE / case / "min-depth/target.json")
        certificate = read(PRODUCER / (case + "_certificate.json"))
        report = audit_case(target, certificate, assets, dates)
        report["case"] = case
        save(output / (case + "_audit.json"), report)
        cases.append(report)
        print(case, "actual-SSA support audit PASS", report["payoff_raw_bounds"], flush=True)
    xml = ET.parse(PRODUCER / "tests.xml").getroot()
    suites = [xml] if xml.tag == "testsuite" else list(xml)
    assert all(
        int(s.get(field, 0)) == 0 for s in suites for field in ("failures", "errors", "skipped")
    )
    tests = {
        (test.get("classname"), test.get("name"))
        for suite in suites
        for test in suite.findall("testcase")
    }
    assert len(tests) == sum(int(s.get("tests", 0)) for s in suites) == 11
    summary = {
        "passed": True,
        "local_only": True,
        "independent_actual_SSA_support_audit": True,
        "cases": [
            {key: value for key, value in case.items() if key != "range_reduction_cells"}
            for case in cases
        ],
        "producer_distinct_tests_reconciled": len(tests),
        "new_distinct_tests": 0,
        "all_input_native_output_support_certified": True,
        "new_financial_gate_replays": 0,
        "G2_to_G5": "open",
    }
    save(output / "summary.json", summary)
    verify(protocol["frozen_inputs"])
    save(
        output / "manifest.json",
        {
            "files": {relative(path): sha(path) for path in output.rglob("*") if path.is_file()},
            "frozen_inputs": protocol["frozen_inputs"],
            "manifest_self_hash_excluded": True,
        },
    )
    print(
        "Independent E03 support audit complete: 464 stock templates, 11 producer tests", flush=True
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    (prepare if args.phase == "prepare" else run)(args.output)
