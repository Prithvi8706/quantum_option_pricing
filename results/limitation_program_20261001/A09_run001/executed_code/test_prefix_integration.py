"""Independent integer and archived-interface checks for prefix multiplication."""

import copy
import hashlib
import json
import random

import pytest

from research.controlled_source_completion.compact_parallel import (
    execute_compact_parallel,
    make_compact_schedule,
)
from research.controlled_source_completion.compiler import compile_graph, execute, resolve_library
from research.controlled_source_completion.ir import Graph
from research.controlled_source_completion.prefix_multiplier import (
    build_prefix_multiplier,
    leaf_spec,
)
from research.controlled_source_completion.primitives import basis_run
from research.limitation_program_20261001.constant_library import canonical
from research.limitation_program_20261001.experiment_prefix_multiplier import (
    PrefixMultiplierIntegrationLibrary,
)

WIDTH, FRACTION = 72, 40
MODULUS, SIGN = 1 << WIDTH, 1 << (WIDTH - 1)
MASK = MODULUS - 1
VARIANTS = ("brent-kung", "kogge-stone")
TABLE = [(0, 1), (3, -2), (MASK, 1 << FRACTION), (SIGN, -7)]


def signed(raw):
    raw &= MASK
    return raw - MODULUS if raw & SIGN else raw


def product(a, b):
    # Python integer // is floor, including a negative nonintegral quotient.
    return (signed(a) * signed(b) // (1 << FRACTION)) & MASK


def graph_fixture():
    graph = Graph(FRACTION, WIDTH - FRACTION)
    x = graph.input("x", WIDTH, "provided")
    y = graph.input("y", WIDTH, "provided")
    address = graph.input("address", 2, "provided")
    distinct = graph.mul(x, y)
    square = graph.mul(x, x)
    nested = graph.mul(distinct, y)
    total = graph.add(distinct, square)
    low = graph.bits(y, 0, 12)
    graph.tables["literal"] = copy.deepcopy(TABLE)
    coefficients = graph.node("lookup", (address,), {"table": "literal", "bits": 2}, 2)
    graph.outputs = {
        "distinct": distinct, "alias": distinct, "square": square,
        "nested": nested, "sum": total, "low": low,
        "table_a": coefficients[0], "table_b": coefficients[1],
    }
    return graph, {"distinct": distinct, "square": square, "nested": nested,
                   "total": total, "lookup": coefficients}


def compile_fixture(directory, variant):
    graph, ids = graph_fixture()
    target = graph.as_dict()
    original, _ = compile_graph(target, directory / "original")
    library = PrefixMultiplierIntegrationLibrary(
        directory / "new/leaves", target, original, variant,
    )
    source, _ = compile_graph(target, directory / "new", library)
    schedule = make_compact_schedule(target, source, source["resources"]["logical_qubits"] * 4)
    return target, original, source, library, schedule, ids


def call_for(source, value):
    return next(call for call in source["forward_calls"] if value in call["out"])


def node_for(target, value):
    return next(node for node in target["nodes"] if value in node["out"])


def initial_words(source):
    values = [int("a5" * 9, 16), MASK, SIGN | 13, int("39" * 9, 16)]
    return {name: values[index % len(values)] for index, name in enumerate(source["outputs"])}


def independent_outputs(x, y, address):
    first, square = product(x, y), product(x, x)
    return {
        "distinct": first, "alias": first, "square": square,
        "nested": product(first, y), "sum": (first + square) & MASK,
        "low": y & ((1 << 12) - 1),
        "table_a": TABLE[address][0] & MASK, "table_b": TABLE[address][1] & MASK,
    }


def production_vectors():
    low = (1 << FRACTION) - 1
    vectors = {
        (0, 0), (1, 1), (1, MASK), (MASK, MASK),
        (SIGN, SIGN), (SIGN, SIGN - 1), (SIGN, 1), (SIGN, MASK),
        (SIGN - 1, SIGN - 1), (low, low), (low + 2, low),
        ((1 << 20) - 1, (1 << 20) - 1), (1 << 20, 1 << 20),
        ((-low) & MASK, (1 << FRACTION) + 3),
    }
    generator = random.Random(20261009)
    vectors.update((generator.getrandbits(WIDTH), generator.getrandbits(WIDTH))
                   for _ in range(8))
    return sorted(vectors)


@pytest.mark.parametrize("variant", VARIANTS)
def test_full_word_pipeline_independent_floor_aliases_and_cleanup(tmp_path, variant):
    target, original, source, library, schedule, ids = compile_fixture(tmp_path, variant)
    same = call_for(source, ids["square"])
    assert same["args"][0] == same["args"][1]
    for value in (ids["distinct"], ids["square"], ids["nested"]):
        call = call_for(source, value)
        assert call["leaf"] != call_for(original, value)["leaf"]
        entry = library.entries[call["leaf"]]
        assert "input_contract" not in entry and "input_contract" not in entry["spec"]
        assert [len(register) for register in entry["args"]] == [WIDTH, WIDTH]
        assert [len(register) for register in entry["outs"]] == [WIDTH]
    initial = initial_words(source)
    for index, (x, y) in enumerate(production_vectors()):
        address = index % len(TABLE)
        expected = independent_outputs(x, y, address)
        actual = execute_compact_parallel(
            target, source, schedule, {"x": x, "y": y, "address": address}, initial,
        )
        assert actual["values"] == {name: initial[name] ^ raw for name, raw in expected.items()}
        assert actual["all_input_and_workspace_bits_restored"]
    # Carry from discarded columns can change the retained result; retaining
    # only above-cutoff individual partial products would fail this vector.
    low = (1 << FRACTION) - 1
    assert product(low, low) == (1 << FRACTION) - 2
    assert product(1, MASK) == MASK  # floor(-2**-40) is -1, not zero.


@pytest.mark.parametrize("variant", VARIANTS)
def test_production_leaf_inverse_nonzero_output_and_no_output_controls(variant):
    program, arguments, outputs = build_prefix_multiplier(WIDTH, FRACTION, variant)
    occupied_inputs, output = set(arguments[0] + arguments[1]), set(outputs[0])
    assert all(gate[-1] not in occupied_inputs for gate in program.gates)
    assert all(not set(gate[:-1]) & output for gate in program.gates)
    initial = int("a5" * 9, 16)
    for x, y in ((1, MASK), (SIGN, MASK), (SIGN, SIGN - 1),
                 ((1 << FRACTION) - 1, (1 << FRACTION) - 1),
                 ((1 << FRACTION) + 1, (1 << FRACTION) + 3)):
        for inverse in (False, True):
            assert basis_run(program, arguments, outputs, [x, y], [initial], inverse)[:3] == (
                [initial ^ product(x, y)], True, True,
            )


@pytest.mark.parametrize("variant", VARIANTS)
def test_archive_reader_loads_omitted_contract_and_fallback_bytes(tmp_path, variant):
    target, original, source, library, _, ids = compile_fixture(tmp_path, variant)
    old_archive = resolve_library(original)
    for node in target["nodes"]:
        if node["op"] in ("input", "mul"):
            continue
        old, new = call_for(original, node["out"][0]), call_for(source, node["out"][0])
        assert old["leaf"] == new["leaf"]
        key = old["leaf"]
        entry = json.loads((old_archive / (key + ".json")).read_text(encoding="utf-8"))
        for name in (key + ".json", entry["gate_file"]):
            assert (old_archive / name).read_bytes() == (library.path / name).read_bytes()
    key = call_for(source, ids["distinct"])["leaf"]
    saved = json.loads((library.path / (key + ".json")).read_text(encoding="utf-8"))
    assert "input_contract" not in saved and "input_contract" not in saved["spec"]
    assert key == hashlib.sha256(canonical(saved["spec"]).encode()).hexdigest()[:20]
    assert saved["spec"]["lowering"]
    # This is the current archived full-word executor, without a new adapter.
    sample = {"x": MASK, "y": (1 << FRACTION) + 3, "address": 3}
    initial = initial_words(source)
    actual = execute(source, sample, initial)
    expected = independent_outputs(sample["x"], sample["y"], sample["address"])
    assert actual["values"] == {name: initial[name] ^ raw for name, raw in expected.items()}
    assert actual["workspace_clean"] and actual["inputs_preserved"]


def test_saved_node_and_source_parameter_mutation_rejected(tmp_path):
    target, original, _, library, _, ids = compile_fixture(tmp_path, VARIANTS[0])
    node = node_for(target, ids["distinct"])
    mutant = copy.deepcopy(node)
    mutant["params"] = {"rounding": "nearest"}
    with pytest.raises(ValueError, match="immutable|semantic|parameter|match"):
        library.get(mutant)
    different = copy.deepcopy(target)
    node_for(different, ids["distinct"])["params"] = {"rounding": "nearest"}
    with pytest.raises(ValueError, match="source|target|semantic|param|match"):
        PrefixMultiplierIntegrationLibrary(tmp_path / "different", different, original, VARIANTS[0])
    foreign = copy.deepcopy(node)
    foreign["args"].reverse()
    foreign["out"] = [123456]
    with pytest.raises(ValueError, match="immutable|semantic|output|match"):
        library.get(foreign)


def test_archived_source_leaf_parameter_mutation_rejected(tmp_path):
    graph, ids = graph_fixture()
    target = graph.as_dict()
    original, _ = compile_graph(target, tmp_path / "original")
    key = call_for(original, ids["distinct"])["leaf"]
    path = resolve_library(original) / (key + ".json")
    entry = json.loads(path.read_text(encoding="utf-8"))
    entry["params"] = {"rounding": "nearest"}
    path.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="source|target|param|semantic"):
        PrefixMultiplierIntegrationLibrary(tmp_path / "new", target, original, VARIANTS[0])


@pytest.mark.parametrize("when", ("before-constructor", "after-constructor"))
def test_lookup_table_mutation_rejected_even_with_same_mask_and_key(tmp_path, when):
    graph, _ = graph_fixture()
    target = graph.as_dict()
    original, _ = compile_graph(target, tmp_path / "original")
    if when == "after-constructor":
        library = PrefixMultiplierIntegrationLibrary(
            tmp_path / "new/leaves", target, original, VARIANTS[0],
        )
        # Union of possible set bits and all SSA bindings stay identical.
        target["tables"]["literal"][0] = (1, 1)
        with pytest.raises(ValueError, match="table|frozen|snapshot|immutable"):
            compile_graph(target, tmp_path / "changed", library)
    else:
        target["tables"]["literal"][0] = (1, 1)
        with pytest.raises(ValueError, match="lookup|table|bound|key"):
            PrefixMultiplierIntegrationLibrary(
                tmp_path / "new/leaves", target, original, VARIANTS[0],
            )


@pytest.mark.parametrize("corruption", ("gate", "version", "contract"))
def test_versioned_prefix_cache_rejects_corruption(tmp_path, corruption):
    target, original, source, library, _, ids = compile_fixture(tmp_path, VARIANTS[0])
    node = node_for(target, ids["distinct"])
    key = call_for(source, ids["distinct"])["leaf"]
    metadata = library.path / (key + ".json")
    entry = json.loads(metadata.read_text(encoding="utf-8"))
    if corruption == "gate":
        binary = library.path / entry["gate_file"]
        binary.write_bytes(binary.read_bytes() + b"prefix cache negative control")
    else:
        if corruption == "version":
            entry["spec"]["lowering"] += "-changed"
        else:
            entry["input_contract"] = {}
        metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="cache|SHA|spec|contract|metadata"):
        cached = PrefixMultiplierIntegrationLibrary(library.path, target, original, VARIANTS[0])
        cached.get(node)


def test_repeated_dispatch_deduplicates_decisions_and_checks_memory_cache(tmp_path):
    target, _, source, library, _, ids = compile_fixture(tmp_path, VARIANTS[0])
    node = node_for(target, ids["distinct"])
    count = len(library.decisions)
    for _ in range(3):
        library.get(node)
    assert len(library.decisions) == count == len(source["forward_calls"])
    key = call_for(source, ids["distinct"])["leaf"]
    library.entries[key]["resources"]["t_count"] += 7
    with pytest.raises(ValueError, match="memory|metadata|validation|cache"):
        library.get(node)


def test_clean_cache_reload_keeps_key_resources_and_contract_omission(tmp_path):
    target, original, source, library, _, ids = compile_fixture(tmp_path, VARIANTS[0])
    key = call_for(source, ids["distinct"])["leaf"]
    before = json.loads((library.path / (key + ".json")).read_text(encoding="utf-8"))
    cached = PrefixMultiplierIntegrationLibrary(library.path, target, original, VARIANTS[0])
    actual_key, actual = cached.get(node_for(target, ids["distinct"]))
    assert actual_key == key and actual == before
    assert "input_contract" not in actual and "input_contract" not in actual["spec"]


def test_spec_is_full_width_and_variant_keys_are_distinct():
    specs = [leaf_spec(WIDTH, FRACTION, variant) for variant in VARIANTS]
    assert all(spec["op"] == "mul" and "input_contract" not in spec for spec in specs)
    assert len({hashlib.sha256(canonical(spec).encode()).hexdigest() for spec in specs}) == 2
