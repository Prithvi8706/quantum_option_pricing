"""Independent signed arithmetic and emitted-wire tests for compact capped waves."""

import hashlib
import json
from collections import Counter
from itertools import product

import numpy as np
import pytest

from research.controlled_source_completion import compact_parallel
from research.controlled_source_completion.carry_save_multiplier import build_multiplier
from research.controlled_source_completion.compact_parallel import (
    execute_compact_parallel,
    make_compact_schedule,
)
from research.controlled_source_completion.compact_storage import narrow_comparison
from research.controlled_source_completion.compiler import compile_graph
from research.controlled_source_completion.constant_multiplier import build_constant_multiplier
from research.controlled_source_completion.ir import Graph
from research.controlled_source_completion.primitives import Library, array_gates, resources
from research.journal_sprint.reversible_fixed_point import Program, constant


class AdversarialLibrary(Library):
    """Fresh real gates, including nonuniform output-register metadata."""

    def __init__(self, path, width, fraction, tables, *,
                 narrow_flags=False, revive_constants=False,
                 csa=False, zero_low=False):
        super().__init__(path, width, fraction, tables)
        self.narrow_flags = narrow_flags
        self.revive_constants = revive_constants
        self.csa = csa
        self.zero_low = zero_low

    def get(self, node):
        op = node["op"]
        contract = None
        if op == "lt" and self.narrow_flags:
            program, args, outs = narrow_comparison(self.w)
            lowering = "one-bit-flag"
        elif op == "const" and self.revive_constants:
            program = Program(compact=True)
            args, outs = [], [program.register(self.w)]
            high, other = outs[0][-1], outs[0][-2]
            # An exact identity on arbitrary output words. High output wires
            # temporarily become nonzero and must have distinct private slots.
            program.gate(high)
            program.gate(high, other)
            program.gate(high)
            program.gate(high, other)
            program.gate(other)
            constant(program, outs[0], node["params"]["value"])
            lowering = "revive-proved-zero-output-bits"
        elif op == "mul" and self.csa:
            program, args, outs = build_multiplier(self.w, self.f)
            lowering = "actual-carry-save"
        elif op == "cmul" and self.zero_low:
            program, args, outs = build_constant_multiplier(
                self.w, self.f, node["params"]["c"], self.f,
            )
            contract = {"zero_low_bits": self.f}
            lowering = "actual-promised-constant"
        else:
            return super().get(node)
        spec = {"op": op, "params": node["params"], "lowering": lowering,
                "width": self.w, "fraction": self.f}
        key = hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest()[:20]
        if key not in self.entries:
            binary = self.path / (key + ".npy")
            np.save(binary, array_gates(program))
            entry = {
                "key": key, "op": op, "params": node["params"],
                "args": list(map(list, args)), "outs": list(map(list, outs)),
                "resources": resources(program), "gate_file": binary.name,
                "sha256": hashlib.sha256(binary.read_bytes()).hexdigest(),
                "table_bits": 0,
            }
            if contract is not None:
                entry["input_contract"] = contract
            (self.path / (key + ".json")).write_text(json.dumps(entry), encoding="utf-8")
            self.entries[key] = entry
        return key, self.entries[key]


def compile_case(graph, directory, **alternatives):
    target = graph.as_dict()
    library = AdversarialLibrary(
        directory / "leaves", graph.w, graph.f, target["tables"], **alternatives,
    )
    source, _ = compile_graph(target, directory / "source", library)
    return target, source, library


def signed(raw, width):
    return raw - (1 << width) if raw & (1 << (width - 1)) else raw


def xor_expected(raw_values, initial, width):
    mask = (1 << width) - 1
    return {name: (raw ^ initial.get(name, 0)) & mask
            for name, raw in raw_values.items()}


def assert_clean_result(target, source, schedule, inputs, expected, initial):
    got = execute_compact_parallel(target, source, schedule, inputs, initial)
    assert got["values"] == xor_expected(expected, initial, source["word_width"])
    assert got["all_input_and_workspace_bits_restored"]
    return got


def audit_schedule(source, schedule, library):
    """Check actual leaf resources and DAG constraints."""
    width = source["word_width"]
    calls = source["forward_calls"]
    groups = schedule["groups"]
    scheduled = [i for group in groups for i in group["call_indices"]]
    assert sorted(scheduled) == list(range(len(calls)))
    assert len(scheduled) == len(set(scheduled))
    occupied = set()
    for offset, bits in zip(schedule["offsets"], schedule["widths"]):
        register = set(range(offset, offset + bits))
        assert not occupied & register
        occupied |= register
    assert occupied == set(range(schedule["retained_ssa_qubits"]))
    producers = {value: index for index, call in enumerate(calls) for value in call["out"]}
    positions = {index: group_index for group_index, group in enumerate(groups)
                 for index in group["call_indices"]}
    for index, call in enumerate(calls):
        for argument in call["args"]:
            if argument in producers:
                assert positions[producers[argument]] < positions[index]
    entries = library.entries
    private_max = 0
    for group in groups:
        private = 0
        shared = Counter()
        for index in group["call_indices"]:
            call = calls[index]
            entry = entries[call["leaf"]]
            retained = sum(schedule["widths"][v] for v in call["out"])
            private += entry["resources"]["qubits"] - retained
            shared.update(call["args"])
        assert group["private_scratch_qubits"] == private
        assert group["copy_rounds"] == max(shared.values(), default=0)
        assert group["t_depth"] == max(
            (entries[calls[i]["leaf"]]["resources"]["t_depth"]
             for i in group["call_indices"]), default=0,
        )
        private_max = max(private_max, private)
    retained = schedule["retained_ssa_qubits"] + width * len(source["outputs"])
    assert schedule["resources"]["logical_qubits"] == retained + private_max
    assert schedule["resources"]["logical_qubits"] <= schedule["qubit_cap"]
    argument_copies = 4 * sum(
        schedule["widths"][v] for call in calls for v in call["args"]
    )
    output_copies = sum(schedule["widths"][v] for v in source["outputs"].values())
    assert schedule["argument_and_output_copy_cx"] == argument_copies + output_copies
    assert schedule["baseline_argument_and_output_copy_cx"] == (
        4 * sum(len(call["args"]) * width for call in calls) + len(source["outputs"]) * width
    )
    leaf_totals = Counter()
    for call in calls:
        for field, value in entries[call["leaf"]]["resources"].items():
            if isinstance(value, int):
                leaf_totals[field] += value
    counts = schedule["resources"]
    assert counts["t_count"] == source["resources"]["t_count"]
    assert counts["t_depth"] == 2 * sum(group["t_depth"] for group in groups)
    for name in ("source_gates", "cx", "clifford_cx"):
        assert counts[name] == 2 * leaf_totals[name] + argument_copies + output_copies
    for name in ("ccx", "x", "clifford_h"):
        assert counts[name] == 2 * leaf_totals[name]


@pytest.mark.parametrize("fraction", [0, 1, 2])
def test_exhaustive_signed_graph_aliases_and_nonzero_outputs(tmp_path, fraction):
    graph = Graph(fraction, 4 - fraction)
    a, b = graph.input("a", 4), graph.input("b", 4)
    square, multiplication, addition = graph.mul(a, a), graph.mul(a, b), graph.add(a, b)
    mixed = graph.add(graph.sub(square, multiplication), addition)
    flag = graph.lt(a, b)
    positive = graph.pos(a)
    value = graph.select(flag, mixed, positive)
    right = graph.bits(a, 7, 4, signed=True)
    graph.outputs = {"value": value, "alias": value, "flag": flag,
                     "positive": positive, "sign": right}
    target, source, library = compile_case(graph, tmp_path, narrow_flags=True)
    generous = make_compact_schedule(target, source, source["resources"]["logical_qubits"] * 8)
    minimum = generous["retained_ssa_qubits"] + len(source["outputs"]) * graph.w
    minimum += max(
        entry["resources"]["qubits"] - sum(generous["widths"][v] for v in call["out"])
        for call in source["forward_calls"] for entry in [library.entries[call["leaf"]]]
    )
    capped = make_compact_schedule(target, source, minimum)
    for schedule in (generous, capped):
        audit_schedule(source, schedule, library)
        assert schedule["widths"][flag] == 1
        initial = {"value": 11, "alias": 6, "flag": 13, "positive": 7, "sign": 5}
        for raw_a, raw_b in product(range(16), repeat=2):
            sa, sb = signed(raw_a, 4), signed(raw_b, 4)
            expected_flag = int(sa < sb)
            expected_mixed = ((sa * sa >> fraction) - (sa * sb >> fraction)
                              + sa + sb) & 15
            expected = {
                "value": expected_mixed if expected_flag else max(sa, 0),
                "alias": expected_mixed if expected_flag else max(sa, 0),
                "flag": expected_flag, "positive": max(sa, 0),
                "sign": 15 if sa < 0 else 0,
            }
            assert_clean_result(target, source, schedule,
                                {"a": raw_a, "b": raw_b}, expected, initial)
    with pytest.raises(ValueError, match="cap"):
        make_compact_schedule(target, source, minimum - 1)


def test_lookup_flags_zero_columns_and_private_zero_revival(tmp_path, monkeypatch):
    graph = Graph(0, 5)
    address = graph.input("address", 2)
    one = graph.const_int(1)
    index = graph.bits(address, 0, 2)
    table = [[0, 1, 0], [1, 5, 0], [3, 0, 0], [2, 7, 0]]
    graph.tables["literal"] = table
    loaded = graph.node("lookup", (index,), {"bits": 2, "table": "literal"}, 3)
    flag = graph.lt(loaded[0], loaded[1])
    graph.outputs = {"small": loaded[0], "larger": loaded[1], "zero": loaded[2],
                     "flag": flag, "one": one, "input": address}
    target, source, library = compile_case(
        graph, tmp_path, narrow_flags=True, revive_constants=True,
    )
    schedule = make_compact_schedule(target, source, source["resources"]["logical_qubits"] * 8)
    audit_schedule(source, schedule, library)
    assert [schedule["widths"][v] for v in loaded] == [2, 3, 1]
    assert schedule["widths"][flag] == schedule["widths"][one] == 1
    assert (schedule["argument_and_output_copy_cx"]
            < schedule["baseline_argument_and_output_copy_cx"])
    original = compact_parallel.mapped_gates
    captured = []

    def capture(gates, state, mapping, inverse):
        assert len(mapping) == len(set(map(int, mapping)))
        assert int(np.max(mapping, initial=0)) < schedule["resources"]["logical_qubits"]
        captured.append(mapping.copy())
        return original(gates, state, mapping, inverse)

    monkeypatch.setattr(compact_parallel, "mapped_gates", capture)
    initial = {name: (17 + i) & 31 for i, name in enumerate(graph.outputs)}
    for raw in range(4):
        expected = {"small": table[raw][0], "larger": table[raw][1], "zero": 0,
                    "flag": int(table[raw][0] < table[raw][1]), "one": 1, "input": raw}
        assert_clean_result(target, source, schedule, {"address": raw}, expected, initial)
    scratch_base = schedule["retained_ssa_qubits"] + len(graph.outputs) * graph.w
    cursor = 0
    for group in schedule["groups"]:
        previous = set()
        for _ in group["call_indices"]:
            mapping = captured[cursor]
            cursor += 1
            private = {int(wire) for wire in mapping if wire >= scratch_base}
            assert not private & previous
            previous |= private
        assert len(previous) == group["private_scratch_qubits"]


def test_actual_csa_and_zero_low_constant_leaves(tmp_path):
    graph = Graph(2, 4)
    a, b = graph.input("a", 6), graph.input("b", 2)
    shifted = graph.bits(a, -2, 6)
    constant_value = graph.node("cmul", (shifted,), {"c": 3})
    square, product_value = graph.mul(a, a), graph.mul(a, b)
    graph.outputs = {"constant": constant_value, "square": square,
                     "product": product_value, "constant_alias": constant_value}
    target, source, library = compile_case(graph, tmp_path, csa=True, zero_low=True)
    schedule = make_compact_schedule(target, source, source["resources"]["logical_qubits"] * 8)
    audit_schedule(source, schedule, library)
    initial = {"constant": 37, "square": 21, "product": 55, "constant_alias": 14}
    for raw_a, raw_b in product(range(64), range(4)):
        sa = signed(raw_a, 6)
        shifted_signed = signed((raw_a << 2) & 63, 6)
        expected = {"constant": (shifted_signed * 3 >> 2) & 63,
                    "square": (sa * sa >> 2) & 63,
                    "product": (sa * raw_b >> 2) & 63}
        expected["constant_alias"] = expected["constant"]
        assert_clean_result(target, source, schedule,
                            {"a": raw_a, "b": raw_b}, expected, initial)


@pytest.mark.parametrize("bad_input", [-1, 4, 17])
def test_bit_preparation_promise_rejected(tmp_path, bad_input):
    graph = Graph(0, 4)
    value = graph.input("small", 2)
    graph.outputs = {"value": graph.pos(value)}
    target, source, _ = compile_case(graph, tmp_path)
    schedule = make_compact_schedule(target, source, source["resources"]["logical_qubits"])
    with pytest.raises(ValueError, match="promise"):
        execute_compact_parallel(target, source, schedule, {"small": bad_input})


def test_unproved_specialized_leaf_input_contract_rejected(tmp_path):
    graph = Graph(2, 4)
    value = graph.input("unproved", 6)
    graph.outputs = {"constant": graph.node("cmul", (value,), {"c": 3})}
    target, source, _ = compile_case(graph, tmp_path, zero_low=True)
    with pytest.raises(ValueError, match="contract|promise|zero|proof"):
        make_compact_schedule(target, source, source["resources"]["logical_qubits"] * 8)


def test_corrupt_leaf_cannot_be_replayed(tmp_path):
    graph = Graph(0, 4)
    value = graph.input("x", 2)
    graph.outputs = {"value": graph.pos(value)}
    target, source, library = compile_case(graph, tmp_path)
    schedule = make_compact_schedule(target, source, source["resources"]["logical_qubits"])
    entry = library.entries[source["forward_calls"][0]["leaf"]]
    binary = library.path / entry["gate_file"]
    binary.write_bytes(binary.read_bytes() + b"deliberate test corruption")
    with pytest.raises(ValueError, match="hash"):
        execute_compact_parallel(target, source, schedule, {"x": 1})


def test_same_bindings_with_different_leaf_semantics_are_rejected(tmp_path):
    graph = Graph(0, 4)
    one = graph.const_int(1)
    graph.outputs = {"value": one}
    target, source, _ = compile_case(graph, tmp_path)
    # Bindings are identical, but the leaf still writes 1 while the new target
    # claims 0. The mask proof alone cannot authenticate leaf semantics.
    target["nodes"][0]["params"]["value"] = 0
    with pytest.raises(ValueError, match="mismatch|semantic|parameter|leaf"):
        make_compact_schedule(target, source, source["resources"]["logical_qubits"])


def test_same_lookup_bindings_with_changed_literals_are_rejected(tmp_path):
    graph = Graph(0, 4)
    address = graph.input("address", 2)
    graph.tables["literal"] = [[1], [1], [1], [1]]
    value = graph.node("lookup", (address,), {"bits": 2, "table": "literal"})
    graph.outputs = {"value": value}
    target, source, _ = compile_case(graph, tmp_path)
    # The target's possible-one mask remains 1, but address zero now means 0;
    # the original gate bytes still return 1. A table-name/mask check misses it.
    target["tables"]["literal"][0][0] = 0
    with pytest.raises(ValueError, match="lookup|table|semantic|identity|leaf"):
        make_compact_schedule(target, source, source["resources"]["logical_qubits"] * 2)


def test_input_only_named_aliases_and_full_word_output_xor(tmp_path):
    graph = Graph(0, 4)
    value = graph.input("x", 2)
    graph.outputs = {"value": value, "alias": value}
    target, source, library = compile_case(graph, tmp_path)
    cap = 2 + 2 * 4
    schedule = make_compact_schedule(target, source, cap)
    audit_schedule(source, schedule, library)
    assert schedule["groups"] == []
    assert schedule["resources"]["logical_qubits"] == cap
    assert schedule["resources"]["t_count"] == schedule["resources"]["t_depth"] == 0
    for raw in range(4):
        assert_clean_result(target, source, schedule, {"x": raw},
                            {"value": raw, "alias": raw}, {"value": 15, "alias": 11})


def test_constant_zero_and_zero_bit_input_are_clean(tmp_path):
    graph = Graph(0, 4)
    empty = graph.input("empty", 0)
    zero = graph.const_int(0)
    graph.outputs = {"zero": zero, "input": empty}
    target, source, library = compile_case(graph, tmp_path, revive_constants=True)
    schedule = make_compact_schedule(target, source, source["resources"]["logical_qubits"] * 8)
    audit_schedule(source, schedule, library)
    assert schedule["proof_masks"][zero] == schedule["proof_masks"][empty] == 0
    assert_clean_result(target, source, schedule, {"empty": 0},
                        {"zero": 0, "input": 0}, {"zero": 13, "input": 7})
    with pytest.raises(ValueError, match="promise"):
        execute_compact_parallel(target, source, schedule, {"empty": 1})


def test_production_named_outputs_keep_all_72_bits(tmp_path):
    graph = Graph(40, 32)
    value = graph.input("x", 2)
    zero = graph.const_int(0)
    small = graph.bits(value, 0, 2)
    graph.outputs = {"value": small, "alias": small, "zero": zero}
    target, source, library = compile_case(graph, tmp_path, revive_constants=True)
    schedule = make_compact_schedule(target, source, source["resources"]["logical_qubits"])
    audit_schedule(source, schedule, library)
    assert schedule["retained_ssa_qubits"] == 5
    assert schedule["resources"]["logical_qubits"] >= 3 * 72 + 5
    initial = {"value": int("a5" * 9, 16), "alias": (1 << 72) - 1,
               "zero": (1 << 71) | 13}
    for raw in range(4):
        assert_clean_result(target, source, schedule, {"x": raw},
                            {"value": raw, "alias": raw, "zero": 0}, initial)


def test_unknown_leaf_promise_cannot_be_silently_ignored(tmp_path):
    graph = Graph(0, 4)
    value = graph.input("x", 2)
    graph.outputs = {"value": graph.pos(value)}
    target, source, library = compile_case(graph, tmp_path)
    key = source["forward_calls"][0]["leaf"]
    metadata = library.path / (key + ".json")
    entry = json.loads(metadata.read_text(encoding="utf-8"))
    entry["input_contract"] = {"undocumented_domain": True}
    metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="unsupported.*contract"):
        make_compact_schedule(target, source, source["resources"]["logical_qubits"])
