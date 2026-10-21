"""Independent guards and full-word XOR checks for proved unsigned sqrt sites."""

import copy
import json
import math
import shutil

import pytest

from research.controlled_source_completion.compact_parallel_v2 import (
    execute_compact_parallel,
    make_compact_schedule,
)
from research.controlled_source_completion.compiler import compile_graph, resolve_library
from research.controlled_source_completion.ir import Graph
from research.limitation_program_20261001.sqrt_library import (
    NarrowSqrtIntegrationLibrary,
    compile_sqrt_graph,
)

WIDTH, FRACTION, ACTIVE = 72, 40, 46
MASK = (1 << WIDTH) - 1


def sqrt_graph(*, bits=ACTIVE, preparation="uniform", lookup=False):
    """Raw sqrt deliberately avoids Graph.sqrt's optional signed clamp."""
    graph = Graph(FRACTION, WIDTH - FRACTION)
    raw = graph.input("x", 1 if lookup else bits, preparation)
    operand = raw
    if lookup:
        graph.tables["radicands"] = [[0], [1 << (ACTIVE - 1)]]
        operand = graph.node("lookup", (raw,), {"table": "radicands", "bits": 1})
    root = graph.node("sqrt", (operand,))
    doubled = graph.add(root, root)
    graph.outputs = {"Y": root, "alias": root, "doubled": doubled, "operand": operand}
    return graph, {"raw": raw, "operand": operand, "root": root, "doubled": doubled}


def compile_integration(graph, directory):
    target = graph.as_dict()
    original, _ = compile_graph(target, directory / "original")
    library = NarrowSqrtIntegrationLibrary(directory / "new_leaves", target, original)
    source, _ = compile_graph(target, directory / "candidate", library)
    return target, original, source, library


def call_for(source, value):
    return next(call for call in source["forward_calls"] if call["out"] == [value])


def node_for(target, value):
    return next(node for node in target["nodes"] if node["out"] == [value])


def initial_words(source):
    # High bits must remain present even though a correct result needs 43 bits.
    values = [int("a5" * 9, 16), MASK, (1 << 71) | 13, int("39" * 9, 16)]
    return {name: values[index] for index, name in enumerate(source["outputs"])}


def assert_result(target, source, schedule, raw, operand=None):
    operand = raw if operand is None else operand
    root = math.isqrt(operand << FRACTION)
    expected = {"Y": root, "alias": root, "doubled": (2 * root) & MASK, "operand": operand}
    initial = initial_words(source)
    got = execute_compact_parallel(target, source, schedule, {"x": raw}, initial)
    assert got["values"] == {name: initial[name] ^ value for name, value in expected.items()}
    assert got["all_input_and_workspace_bits_restored"]


@pytest.fixture(scope="module")
def templates(tmp_path_factory):
    result = {}
    for name, kwargs in (
        ("proved", {}),
        ("generic", {"bits": WIDTH}),
        ("provided", {"preparation": "provided"}),
        ("lookup", {"lookup": True}),
    ):
        graph, ids = sqrt_graph(**kwargs)
        directory = tmp_path_factory.mktemp("sqrt_" + name)
        target, original, source, library = compile_integration(graph, directory)
        result[name] = {
            "target": target, "original": original, "source": source,
            "library": library, "ids": ids,
        }
    return result


def mutable_candidate(template, tmp_path):
    target, original, source = [copy.deepcopy(template[name])
                                for name in ("target", "original", "source")]
    path = tmp_path / "candidate_leaves"
    shutil.copytree(resolve_library(source), path)
    source["library"] = source["library_workspace_relative"] = str(path.resolve())
    return target, original, source, path


def test_proved_sqrt_unsigned_bit45_full_output_xor_repeated_arguments_and_cleanup(templates):
    item = templates["proved"]
    target, original, source, library = [item[name] for name in
                                       ("target", "original", "source", "library")]
    key = call_for(source, item["ids"]["root"])["leaf"]
    assert key != call_for(original, item["ids"]["root"])["leaf"]
    entry = library.entries[key]
    assert entry["input_contract"] == {"unsigned_input_bits": ACTIVE}
    assert entry["args"] == [list(range(WIDTH))]
    assert entry["outs"] == [list(range(WIDTH, 2 * WIDTH))]
    assert entry["resources"]["t_count"] < library.original_entries[
        call_for(original, item["ids"]["root"])["leaf"]
    ]["resources"]["t_count"]
    schedule = make_compact_schedule(target, source, original["resources"]["logical_qubits"])
    values = {0, 1, 2, 3, (1 << 45) - 1, 1 << 45, (1 << 45) + 1, (1 << ACTIVE) - 1}
    for base in (1, 3, 7, (1 << 22) - 1, 1 << 22):
        square = base * base
        values.update(value for value in (square - 1, square, square + 1)
                      if 0 <= value < 1 << ACTIVE)
    for value in sorted(values):
        assert_result(target, source, schedule, value)


@pytest.mark.parametrize("template_name", ["generic", "provided"])
def test_unproved_sqrt_keeps_original_leaf_bytes(templates, template_name):
    item = templates[template_name]
    original, source, library = [item[name] for name in ("original", "source", "library")]
    value = item["ids"]["root"]
    old_key, new_key = call_for(original, value)["leaf"], call_for(source, value)["leaf"]
    assert old_key == new_key
    entry = library.entries[new_key]
    for name in (new_key + ".json", entry["gate_file"]):
        assert (resolve_library(original) / name).read_bytes() == (library.path / name).read_bytes()
    schedule = make_compact_schedule(item["target"], source,
                                     original["resources"]["logical_qubits"])
    values = (0, 1, (1 << 45), (1 << ACTIVE) - 1)
    if template_name == "generic":
        values += (1 << 71, MASK)
    for raw in values:
        assert_result(item["target"], source, schedule, raw)


def test_lookup_interval_uses_every_literal_row_and_unsigned_operand(templates):
    item = templates["lookup"]
    key = call_for(item["source"], item["ids"]["root"])["leaf"]
    assert key != call_for(item["original"], item["ids"]["root"])["leaf"]
    assert item["library"].entries[key]["input_contract"] == {"unsigned_input_bits": ACTIVE}
    schedule = make_compact_schedule(item["target"], item["source"],
                                     item["original"]["resources"]["logical_qubits"])
    for raw in (0, 1):
        assert_result(item["target"], item["source"], schedule, raw,
                      item["target"]["tables"]["radicands"][raw][0])


def test_fresh_library_reload_preserves_generated_key_and_bytes(templates, tmp_path):
    item = templates["proved"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    node = node_for(target, item["ids"]["root"])
    key = call_for(source, item["ids"]["root"])["leaf"]
    before = {name: (path / name).read_bytes() for name in
              (key + ".json", item["library"].entries[key]["gate_file"])}
    reloaded = NarrowSqrtIntegrationLibrary(path, target, original)
    got_key, got_entry = reloaded.get(node)
    assert got_key == key
    assert got_entry["input_contract"] == {"unsigned_input_bits": ACTIVE}
    for name, value in before.items():
        assert (path / name).read_bytes() == value
    compiled, _ = compile_graph(target, tmp_path / "recompiled", reloaded)
    schedule = make_compact_schedule(target, compiled, original["resources"]["logical_qubits"])
    assert_result(target, compiled, schedule, 1 << 45)


def test_already_specialized_source_can_be_reloaded_with_proof_at_actual_site(templates, tmp_path):
    item = templates["proved"]
    target, _, source, _ = mutable_candidate(item, tmp_path)
    library = NarrowSqrtIntegrationLibrary(tmp_path / "second_generation", target, source)
    compiled, _ = compile_sqrt_graph(target, tmp_path / "second_source", library)
    value = item["ids"]["root"]
    assert call_for(compiled, value)["leaf"] == call_for(source, value)["leaf"]
    schedule = make_compact_schedule(target, compiled,
                                     item["original"]["resources"]["logical_qubits"])
    assert_result(target, compiled, schedule, (1 << ACTIVE) - 1)


@pytest.mark.parametrize("contract", [
    {"unsigned_input_bits": 45},
    {"unsigned_input_bits": True},
    {"unsigned_input_bits": 0},
    {"unsigned_input_bits": 73},
    {"unsigned_input_bits": 46, "signed_upper_bits": 7},
])
def test_malformed_or_too_narrow_promises_are_rejected(templates, tmp_path, contract):
    item = templates["proved"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    key = call_for(source, item["ids"]["root"])["leaf"]
    metadata = path / (key + ".json")
    entry = json.loads(metadata.read_text(encoding="utf-8"))
    entry["input_contract"] = contract
    metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="unsigned|contract|promise|proof|narrow|spec"):
        make_compact_schedule(target, source, original["resources"]["logical_qubits"])


@pytest.mark.parametrize("template_name", ["generic", "provided"])
def test_forged_promise_cannot_specialize_an_unproved_source(templates, tmp_path, template_name):
    item = templates[template_name]
    target, original, source, path = mutable_candidate(item, tmp_path)
    key = call_for(source, item["ids"]["root"])["leaf"]
    metadata = path / (key + ".json")
    entry = json.loads(metadata.read_text(encoding="utf-8"))
    entry["input_contract"] = {"unsigned_input_bits": ACTIVE}
    metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="unsigned|contract|promise|proof|narrow"):
        make_compact_schedule(target, source, original["resources"]["logical_qubits"])
    with pytest.raises(ValueError, match="unsigned|contract|promise|proof|narrow"):
        NarrowSqrtIntegrationLibrary(tmp_path / "reload", target, source)


@pytest.mark.parametrize("corruption", ["missing", "empty", "different", "interface"])
def test_narrow_spec_cannot_hide_or_mismatch_its_outer_promise(templates, tmp_path, corruption):
    item = templates["proved"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    key = call_for(source, item["ids"]["root"])["leaf"]
    metadata = path / (key + ".json")
    entry = json.loads(metadata.read_text(encoding="utf-8"))
    if corruption == "missing":
        entry.pop("input_contract")
    elif corruption == "empty":
        entry["input_contract"] = {}
    elif corruption == "different":
        entry["input_contract"] = {"zero_low_bits": 0}
    else:
        entry["outs"][0] = entry["outs"][0][:56]
    metadata.write_text(json.dumps(entry), encoding="utf-8")
    error = "unsigned|contract|promise|proof|interface|layout|register"
    with pytest.raises(ValueError, match=error):
        make_compact_schedule(target, source, original["resources"]["logical_qubits"])
    with pytest.raises(ValueError, match=error):
        NarrowSqrtIntegrationLibrary(tmp_path / "reload", target, source)


@pytest.mark.parametrize("corruption", ["contract", "spec", "gate", "resources"])
def test_specialized_cache_corruption_fails_on_fresh_get(templates, tmp_path, corruption):
    item = templates["proved"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    key = call_for(source, item["ids"]["root"])["leaf"]
    metadata = path / (key + ".json")
    entry = json.loads(metadata.read_text(encoding="utf-8"))
    if corruption == "gate":
        gate = path / entry["gate_file"]
        gate.write_bytes(gate.read_bytes() + b"deliberate corruption")
    elif corruption == "resources":
        entry["resources"]["t_count"] += 7
        metadata.write_text(json.dumps(entry), encoding="utf-8")
    else:
        entry["input_contract" if corruption == "contract" else "spec"]["unsigned_input_bits"] = 45
        metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="cache|hash|SHA|metadata|contract|spec|resource"):
        reloaded = NarrowSqrtIntegrationLibrary(path, target, original)
        reloaded.get(node_for(target, item["ids"]["root"]))


def test_in_memory_metadata_corruption_is_rejected(templates, tmp_path):
    item = templates["proved"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    library = NarrowSqrtIntegrationLibrary(path, target, original)
    node = node_for(target, item["ids"]["root"])
    key, entry = library.get(node)
    entry["input_contract"]["unsigned_input_bits"] = 45
    with pytest.raises(ValueError, match="metadata|cache|validation"):
        library.get(node)


def test_gate_sha_is_checked_at_full_source_replay(templates, tmp_path):
    item = templates["proved"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    schedule = make_compact_schedule(target, source, original["resources"]["logical_qubits"])
    key = call_for(source, item["ids"]["root"])["leaf"]
    entry = json.loads((path / (key + ".json")).read_text(encoding="utf-8"))
    gate = path / entry["gate_file"]
    gate.write_bytes(gate.read_bytes() + b"deliberate corruption")
    with pytest.raises(ValueError, match="hash|SHA"):
        execute_compact_parallel(target, source, schedule, {"x": 1})


@pytest.mark.parametrize("mutation", ["input_width", "sqrt_binding", "target_table"])
def test_source_target_binding_and_table_mutations_are_rejected(templates, tmp_path, mutation):
    item = templates["lookup"] if mutation == "target_table" else templates["proved"]
    target, original, _, path = mutable_candidate(item, tmp_path)
    if mutation == "input_width":
        target["nodes"][0]["params"]["bits"] = WIDTH
    elif mutation == "sqrt_binding":
        node_for(target, item["ids"]["root"])["args"] = [item["ids"]["doubled"]]
    else:
        target["tables"]["radicands"][1][0] = 1 << 70
    with pytest.raises(ValueError,
                       match="target|source|input|SSA|binding|table|graph|match|defined"):
        NarrowSqrtIntegrationLibrary(path, target, original)


def test_mutating_compiler_table_snapshot_is_rejected(templates, tmp_path):
    item = templates["lookup"]
    target, original, _, path = mutable_candidate(item, tmp_path)
    library = NarrowSqrtIntegrationLibrary(path, target, original)
    library.tables["radicands"][1][0] = 1 << 70
    with pytest.raises(ValueError, match="table|target|snapshot|frozen"):
        library.get(node_for(target, item["ids"]["root"]))


@pytest.mark.parametrize("mutation", ["input_width", "preparation", "output", "unused_table"])
def test_bound_compiler_rejects_any_whole_target_mutation(templates, tmp_path, mutation):
    item = templates["proved"]
    target, original, _, path = mutable_candidate(item, tmp_path)
    library = NarrowSqrtIntegrationLibrary(path, target, original)
    if mutation == "input_width":
        target["nodes"][0]["params"]["bits"] = WIDTH
    elif mutation == "preparation":
        target["nodes"][0]["params"]["preparation"] = "provided"
    elif mutation == "output":
        target["outputs"]["Y"] = item["ids"]["doubled"]
    else:
        target["tables"]["unused"] = [[0], [1]]
    with pytest.raises(ValueError, match="target|snapshot|same|frozen|semantic"):
        compile_sqrt_graph(target, tmp_path / "mutated_source", library)


def test_raw_compiler_upstream_mutation_is_rejected_at_scheduling_boundary(templates, tmp_path):
    item = templates["proved"]
    target, original, _, path = mutable_candidate(item, tmp_path)
    library = NarrowSqrtIntegrationLibrary(path, target, original)
    target["nodes"][0]["params"]["bits"] = WIDTH
    # The old generic compiler has no whole-target handshake. The new reader
    # must independently recompute the actual invocation's range nonetheless.
    source, _ = compile_graph(target, tmp_path / "raw_source", library)
    with pytest.raises(ValueError, match="unsigned|contract|promise|proof"):
        make_compact_schedule(target, source, original["resources"]["logical_qubits"])


@pytest.mark.parametrize("mutation", ["target", "source", "storage"])
def test_replay_requires_matching_schedule_fingerprints_and_storage(templates, mutation):
    item = templates["proved"]
    target, source = copy.deepcopy(item["target"]), copy.deepcopy(item["source"])
    schedule = make_compact_schedule(target, source,
                                     item["original"]["resources"]["logical_qubits"])
    if mutation == "target":
        target["nodes"][0]["params"]["bits"] -= 1
    elif mutation == "source":
        source["forward_calls"][0]["argument_copy_cx"] += 1
    else:
        schedule["widths"][item["ids"]["root"]] -= 1
    with pytest.raises(ValueError, match="fingerprint|storage|match"):
        execute_compact_parallel(target, source, schedule, {"x": 1})


def test_replay_rejects_raw_input_outside_proved_domain(templates):
    item = templates["proved"]
    schedule = make_compact_schedule(item["target"], item["source"],
                                     item["original"]["resources"]["logical_qubits"])
    for raw in (-1, 1 << ACTIVE):
        with pytest.raises(ValueError, match="input|bit-width|promise"):
            execute_compact_parallel(item["target"], item["source"], schedule, {"x": raw})
