"""Prospective template and arithmetic-identity checks for exact streaming."""

from copy import deepcopy
from itertools import product

import pytest

from research.controlled_source_completion.ir import evaluate
from research.controlled_source_completion.optimize import optimize
from research.limitation_program_20261001.streaming_reference import build_reference
from research.limitation_program_20261001.streaming_scope import (
    producer_closure,
    streaming_statistics_from_original_trace,
)


@pytest.fixture(scope="module")
def actual_reference():
    return build_reference()


def test_actual_builder_reference_labels_both_assets_and_all_dates(actual_reference):
    original, target, labels = actual_reference
    assert optimize(deepcopy(original)) == target
    assert (target["width"], target["fraction_bits"]) == (72, 40)
    assert len(target["inputs"]) == 12
    assert len(labels["normal_values"]) == 12
    assert len(labels["date_bindings"]) == 4
    assert labels["count_width"] == 3
    producers = {v: n for n in target["nodes"] for v in n["out"]}
    for date, binding in enumerate(labels["date_bindings"]):
        assert binding["date"] == date
        assert len(binding["raw_log_values"]) == len(binding["stock_values"]) == 2
        assert producers[binding["basket_value"]]["op"] == "cmul"
        assert producers[binding["basket_value"]]["params"]["c"] == 1 << 39
        assert binding["common_normal_value"] == labels["normal_values"][date * 3]
        assert (
            binding["idiosyncratic_normal_values"]
            == labels["normal_values"][date * 3 + 1 : date * 3 + 3]
        )


def test_gaussian_pairs_preserve_lookup_siblings_and_original_uniforms(actual_reference):
    _, target, labels = actual_reference
    nodes = target["nodes"]
    constants = set(labels["global_constant_values"])
    for pair in range(6):
        closure = producer_closure(
            target, labels["normal_values"][2 * pair : 2 * pair + 2], constants
        )
        values = {value for index in closure for value in nodes[index]["out"]}
        assert not values & constants
        assert set(labels["normal_values"][2 * pair : 2 * pair + 2]) <= values
        assert len([index for index in closure if nodes[index]["op"] == "lookup"]) == 3
        inputs = {
            value
            for index in closure
            for value in nodes[index]["args"]
            if value in set(target["inputs"])
        }
        assert len(inputs) == 2
        for index in closure:
            if nodes[index]["op"] == "lookup":
                assert set(nodes[index]["out"]) <= values


def test_stock_stage_stops_at_original_raw_logs_and_global_constants(actual_reference):
    _, target, labels = actual_reference
    constants = set(labels["global_constant_values"])
    nodes = target["nodes"]
    for binding in labels["date_bindings"]:
        boundary = constants | set(binding["raw_log_values"])
        closure = producer_closure(target, [binding["basket_value"]], boundary)
        values = {value for index in closure for value in nodes[index]["out"]}
        assert set(binding["stock_values"]) <= values
        assert not values & boundary
        external = {
            value for index in closure for value in nodes[index]["args"] if value not in values
        }
        assert external - constants == set(binding["raw_log_values"])
        assert not set(labels["normal_values"]) & values


@pytest.mark.parametrize("width", [2, 3])
def test_modular_running_raw_state_matches_hillis_steele_for_every_small_word(width):
    modulus = 1 << width
    for words in product(range(modulus), repeat=5):
        initial, increments = words[0], list(words[1:])
        prefix = list(increments)
        prefix[0] = (prefix[0] + initial) % modulus
        distance = 1
        while distance < len(prefix):
            prefix = [
                value if j < distance else (value + prefix[j - distance]) % modulus
                for j, value in enumerate(prefix)
            ]
            distance *= 2
        sequential, current = [], initial
        for increment in increments:
            current = (current + increment) % modulus
            sequential.append(current)
        assert sequential == prefix


def test_violation_count_matches_strict_maximum_at_every_small_signed_boundary():
    domain = range(-4, 4)
    for threshold, first, second, third in product(domain, repeat=4):
        baskets = [first, second, third]
        count = sum(value >= threshold for value in baskets)
        assert (count == 0) == (max(baskets) < threshold)
    assert sum(value >= 2 for value in [1, 2, 3]) == 2


def test_rounding_date_baskets_before_asian_sum_changes_the_exact_function():
    stocks = [(1, 0), (3, 0), (1, 0), (3, 0)]
    original_asian = sum(sum(date) for date in stocks) // 8
    prematurely_rounded = sum(sum(date) // 2 for date in stocks) // 4
    assert original_asian == 1
    assert prematurely_rounded == 0


def test_feeding_clipped_log_back_changes_future_raw_state():
    raw, low, high = 6, 0, 4
    increment = -3
    original_next = raw + increment
    changed_next = min(max(raw, low), high) + increment
    assert original_next == 3 and changed_next == 1


@pytest.mark.parametrize("raw", [0, 2**31, 2**32 - 1])
def test_actual_integer_running_statistics_equal_original_source(actual_reference, raw):
    _, target, labels = actual_reference
    inputs = {node["params"]["name"]: raw for node in target["nodes"] if node["op"] == "input"}
    _, trace = evaluate(target, inputs, trace=True)
    scope = {
        "word_width": target["width"],
        "fraction_bits": target["fraction_bits"],
        "semantics": labels,
        "date_bindings": labels["date_bindings"],
    }
    result = streaming_statistics_from_original_trace(scope, trace)
    assert result["identity_checks_passed"]
    assert result["raw_output"] == trace[target["outputs"]["Y"]]
    assert len(result["history"]) == 4
    assert not result["gate_replay_executed"]


def test_atomic_closure_rejects_missing_original_producer():
    target = {
        "nodes": [
            {"op": "input", "args": [], "out": [0]},
            {"op": "lookup", "args": [0], "out": [1, 2]},
            {"op": "add", "args": [1, 9], "out": [3]},
        ]
    }
    with pytest.raises(ValueError):
        producer_closure(target, [3])
