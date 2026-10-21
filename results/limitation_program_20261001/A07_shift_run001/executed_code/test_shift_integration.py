"""Actual-SSA shift-count guards, native copies, XOR and corruption controls."""

import copy
import json
import shutil
from pathlib import Path

import pytest

from research.controlled_source_completion.compact_parallel_v4 import (
    execute_compact_parallel,
    make_compact_schedule,
)
from research.controlled_source_completion.compiler import compile_graph, resolve_library
from research.controlled_source_completion.ir import Graph, evaluate
from research.limitation_program_20261001.shift_library import (
    ShiftIntegrationLibrary,
    compile_shift_graph,
)
from research.limitation_program_20261001.sqrt_library import NarrowSqrtIntegrationLibrary

ROOT = Path(__file__).resolve().parents[2]


def shift_graph(width=8, fraction=3, count_bits=7, mode="lookup", sqrt_site=False):
    graph = Graph(fraction, width - fraction)
    x = graph.input("x", 2 if mode == "alias" else width,
                    "uniform" if mode == "alias" else "provided")
    if mode == "lookup":
        index_bits = min(count_bits, 3) if width == 72 else count_bits
        index = graph.input("index", index_bits, "uniform")
        counts = ([-64, -63, -16, -1, 0, 1, 33, 63] if width == 72
                  else range(-(1 << (count_bits - 1)), 1 << (count_bits - 1)))
        graph.tables["counts"] = [[count & ((1 << width) - 1)] for count in counts]
        count = graph.node("lookup", (index,), {"table": "counts", "bits": index_bits})
    elif mode == "alias":
        count = x
    else:
        count = graph.input("count", 7 if mode == "uniform_overflow" else width,
                            "uniform" if mode == "uniform_overflow" else "provided")
    shifted = graph.shift(x, count)
    doubled = graph.add(shifted, shifted)
    graph.outputs = {"Y": shifted, "alias": shifted, "doubled": doubled,
                     "data": x, "count": count}
    root = None
    if sqrt_site:
        radicand = graph.input("radicand", 46, "uniform")
        root = graph.node("sqrt", (radicand,))
        graph.outputs["root"] = root
    return graph, {"data": x, "count": count, "shifted": shifted,
                   "doubled": doubled, "root": root}


def call_for(source, value):
    return next(call for call in source["forward_calls"] if call["out"] == [value])


def node_for(target, value):
    return next(node for node in target["nodes"] if node["out"] == [value])


def compile_integration(graph, directory, count_bits=7, sqrt_baseline=False):
    target = graph.as_dict()
    original, _ = compile_graph(target, directory / "original")
    if sqrt_baseline:
        narrowed = NarrowSqrtIntegrationLibrary(directory / "sqrt_leaves", target, original)
        original, _ = compile_graph(target, directory / "sqrt_source", narrowed)
    library = ShiftIntegrationLibrary(directory / "shift_leaves", target, original, count_bits)
    source, _ = compile_shift_graph(target, directory / "candidate", library)
    return target, original, source, library


def cap_for(original, candidate):
    return max(original["resources"]["logical_qubits"],
               candidate["resources"]["logical_qubits"])


def assert_result(target, source, schedule, inputs):
    _, trace = evaluate(target, inputs, trace=True)
    width = source["word_width"]
    patterns = (int("a5" * 9, 16), (1 << width) - 1,
                (1 << (width - 1)) | 13, int("39" * 9, 16), int("e1" * 9, 16))
    initial = {name: patterns[index % len(patterns)] & ((1 << width) - 1)
               for index, name in enumerate(source["outputs"])}
    expected = {name: trace[value] ^ initial[name] for name, value in target["outputs"].items()}
    got = execute_compact_parallel(target, source, schedule, inputs, initial)
    assert got["values"] == expected
    assert got["all_input_and_workspace_bits_restored"]


@pytest.fixture(scope="module")
def templates(tmp_path_factory):
    result = {}
    for name, kwargs in (
        ("small", {"width": 5, "fraction": 2, "count_bits": 3}),
        ("guarded", {}), ("unguarded", {"mode": "provided"}),
        ("uniform_overflow", {"mode": "uniform_overflow"}),
        ("alias", {"mode": "alias"}),
        ("production", {"width": 72, "fraction": 40, "sqrt_site": True}),
    ):
        graph, ids = shift_graph(**kwargs)
        target, original, source, library = compile_integration(
            graph, tmp_path_factory.mktemp("shift_" + name),
            count_bits=kwargs.get("count_bits", 7), sqrt_baseline=name == "production",
        )
        result[name] = {"target": target, "original": original, "source": source,
                        "library": library, "ids": ids}
    return result


def mutable_candidate(template, tmp_path):
    target, original, source = [copy.deepcopy(template[name])
                                for name in ("target", "original", "source")]
    path = tmp_path / "candidate_leaves"
    shutil.copytree(resolve_library(source), path)
    source["library"] = source["library_workspace_relative"] = str(path.resolve())
    return target, original, source, path


def metadata_for(source, path, value):
    key = call_for(source, value)["leaf"]
    metadata = path / (key + ".json")
    return key, metadata, json.loads(metadata.read_text(encoding="utf-8"))


def test_small_signed_counts_exhaustive_data_and_all_dirty_named_outputs(templates):
    item = templates["small"]
    target, original, source = [item[name] for name in ("target", "original", "source")]
    schedule = make_compact_schedule(target, source, cap_for(original, source))
    for data in range(32):
        for index in range(8):
            assert_result(target, source, schedule, {"x": data, "index": index})


def test_signed7_small_width_oversized_counts_saturate_in_the_correct_direction(templates):
    item = templates["guarded"]
    target, original, source = [item[name] for name in ("target", "original", "source")]
    schedule = make_compact_schedule(target, source, cap_for(original, source))
    # Includes negative -64, both signed endpoints, zero and shifts >= data width.
    for index in range(128):
        for data in (0, 1, 127, 128, 255):
            assert_result(target, source, schedule, {"x": data, "index": index})


def test_production_count_minimum_is_unsigned_magnitude64_and_sqrt_bytes_are_retained(
        templates):
    item = templates["production"]
    target, original, source, library = [item[name] for name in
                                       ("target", "original", "source", "library")]
    entry = library.entries[call_for(source, item["ids"]["shifted"])["leaf"]]
    assert entry["input_contract"] == {"signed_shift_count_bits": 7}
    assert entry["args"] == [list(range(72)), list(range(72, 144))]
    assert entry["outs"] == [list(range(144, 216))]
    root = item["ids"]["root"]
    key = call_for(source, root)["leaf"]
    assert key == call_for(original, root)["leaf"]
    sqrt_entry = library.entries[key]
    assert sqrt_entry["input_contract"] == {"unsigned_input_bits": 46}
    for name in (key + ".json", sqrt_entry["gate_file"]):
        assert (resolve_library(original) / name).read_bytes() == (library.path / name).read_bytes()
    schedule = make_compact_schedule(target, source, cap_for(original, source))
    values = (0, 1, (1 << 71) - 1, 1 << 71, (1 << 71) + 1, (1 << 72) - 1)
    for index in range(8):
        for raw in values:
            assert_result(target, source, schedule,
                          {"x": raw, "index": index, "radicand": (1 << 45) + index})


@pytest.mark.parametrize("template_name", ["unguarded", "uniform_overflow"])
def test_unproved_count_domains_keep_exact_fallback_even_when_sample_values_fit(
        templates, template_name):
    item = templates[template_name]
    target, original, source, library = [item[name] for name in
                                       ("target", "original", "source", "library")]
    key = call_for(source, item["ids"]["shifted"])["leaf"]
    assert key == call_for(original, item["ids"]["shifted"])["leaf"]
    entry = library.entries[key]
    for name in (key + ".json", entry["gate_file"]):
        assert (resolve_library(original) / name).read_bytes() == (library.path / name).read_bytes()
    schedule = make_compact_schedule(target, source, cap_for(original, source))
    counts = (0, 1, 7, 8, 63, 64, 127)
    if template_name == "unguarded":
        counts += (128, 191, 192, 248, 249, 255)
    for count in counts:
        for data in (1, 128, 255):
            assert_result(target, source, schedule, {"x": data, "count": count})


def test_repeated_actual_ssa_keeps_both_native_copies_and_storage_masks(templates):
    item = templates["alias"]
    target, original, source = [item[name] for name in ("target", "original", "source")]
    call = call_for(source, item["ids"]["shifted"])
    assert call["args"] == [item["ids"]["data"], item["ids"]["data"]]
    assert call["argument_copy_cx"] == 4 * 8
    cap = cap_for(original, source)
    schedule = make_compact_schedule(target, source, cap)
    original_schedule = make_compact_schedule(target, original, cap)
    assert schedule["widths"] == original_schedule["widths"]
    assert schedule["proof_masks"] == original_schedule["proof_masks"]
    expected = 4 * sum(sum(schedule["widths"][v] for v in c["args"])
                       for c in source["forward_calls"])
    expected += sum(schedule["widths"][v] for v in source["outputs"].values())
    assert schedule["argument_and_output_copy_cx"] == expected
    group = next(g for g in schedule["groups"]
                 if source["forward_calls"].index(call) in g["call_indices"])
    assert group["copy_rounds"] == 2
    for data in range(4):
        assert_result(target, source, schedule, {"x": data})


def test_fresh_cache_reload_preserves_validated_key_and_gate_bytes(templates, tmp_path):
    item = templates["guarded"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    key, _, entry = metadata_for(source, path, item["ids"]["shifted"])
    before = {name: (path / name).read_bytes() for name in (key + ".json", entry["gate_file"])}
    library = ShiftIntegrationLibrary(path, target, original)
    got_key, _ = library.get(node_for(target, item["ids"]["shifted"]))
    assert got_key == key
    for name, data in before.items():
        assert (path / name).read_bytes() == data


@pytest.mark.parametrize("template_name", ["guarded", "production"])
def test_specialized_archive_reload_revalidates_count_promises(templates, tmp_path, template_name):
    item = templates[template_name]
    target, _, source, _ = mutable_candidate(item, tmp_path)
    library = ShiftIntegrationLibrary(tmp_path / "second_generation", target, source)
    compiled, _ = compile_shift_graph(target, tmp_path / "second_source", library)
    value = item["ids"]["shifted"]
    assert call_for(compiled, value)["leaf"] == call_for(source, value)["leaf"]
    schedule = make_compact_schedule(target, compiled, cap_for(item["original"], source))
    inputs = {"x": 1 << (target["width"] - 1), "index": 0}
    if template_name == "production":
        inputs["radicand"] = (1 << 46) - 1
    assert_result(target, compiled, schedule, inputs)


@pytest.mark.parametrize("contract", [
    None, {}, [], {"signed_shift_count_bits": False}, {"signed_shift_count_bits": True},
    {"signed_shift_count_bits": "7"}, {"signed_shift_count_bits": 0},
    {"signed_shift_count_bits": 9}, {"signed_shift_count_bits": 7, "zero_low_bits": 0},
])
def test_missing_empty_false_and_forged_count_promises_rejected(templates, tmp_path, contract):
    item = templates["guarded"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    _, metadata, entry = metadata_for(source, path, item["ids"]["shifted"])
    if contract is None:
        entry.pop("input_contract")
    else:
        entry["input_contract"] = contract
    metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="shift|count|contract|spec"):
        make_compact_schedule(target, source, cap_for(original, source))
    with pytest.raises(ValueError, match="shift|count|contract|spec"):
        ShiftIntegrationLibrary(tmp_path / "reload", target, source)


@pytest.mark.parametrize("malformed_spec", [None, [], "not a specification"])
def test_typed_shift_promise_cannot_hide_in_non_mapping_spec(
        templates, tmp_path, malformed_spec):
    item = templates["guarded"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    _, metadata, entry = metadata_for(source, path, item["ids"]["shifted"])
    entry["spec"] = malformed_spec
    metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="shift|contract|spec"):
        make_compact_schedule(target, source, cap_for(original, source))
    with pytest.raises(ValueError, match="shift|contract|spec"):
        ShiftIntegrationLibrary(tmp_path / "reload", target, source)


def test_authentic_specialized_archive_cannot_attach_to_unproved_count_ssa(templates, tmp_path):
    item = templates["unguarded"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    guarded = templates["guarded"]
    key = call_for(guarded["source"], guarded["ids"]["shifted"])["leaf"]
    entry = guarded["library"].entries[key]
    for name in (key + ".json", entry["gate_file"]):
        shutil.copy2(guarded["library"].path / name, path / name)
    call_for(source, item["ids"]["shifted"])["leaf"] = key
    source["library_keys"] = sorted({call["leaf"] for call in source["forward_calls"]})
    with pytest.raises(ValueError, match="shift|count|contract|proof|proved"):
        make_compact_schedule(target, source, cap_for(original, source))
    with pytest.raises(ValueError, match="shift|count|contract|proof|proved"):
        ShiftIntegrationLibrary(tmp_path / "reload", target, source)


@pytest.mark.parametrize("corruption", ["outer_contract", "spec_contract", "spec_width",
                                         "key", "input_register", "output_register",
                                         "resource", "gate"])
def test_generated_cache_checks_specs_interfaces_resources_and_sha(
        templates, tmp_path, corruption):
    item = templates["guarded"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    _, metadata, entry = metadata_for(source, path, item["ids"]["shifted"])
    if corruption == "gate":
        gate = path / entry["gate_file"]
        gate.write_bytes(gate.read_bytes() + b"deliberate corruption")
    else:
        if corruption == "outer_contract":
            entry["input_contract"]["signed_shift_count_bits"] = False
        elif corruption == "spec_contract":
            entry["spec"]["input_contract"]["signed_shift_count_bits"] = False
        elif corruption == "spec_width":
            entry["spec"]["width"] = 7
        elif corruption == "key":
            entry["key"] = "forged"
        elif corruption == "input_register":
            entry["args"][1] = entry["args"][0]
        elif corruption == "output_register":
            entry["outs"][0] = entry["outs"][0][:-1]
        else:
            entry["resources"]["t_count"] += 7
        metadata.write_text(json.dumps(entry), encoding="utf-8")
    error = "cache|hash|SHA|metadata|contract|spec|resource|interface|layout"
    with pytest.raises(ValueError, match=error):
        library = ShiftIntegrationLibrary(path, target, original)
        library.get(node_for(target, item["ids"]["shifted"]))


@pytest.mark.parametrize("corruption", ["spec", "input_register", "output_register", "key"])
def test_scheduling_rechecks_count_spec_key_and_full_native_interface(
        templates, tmp_path, corruption):
    item = templates["guarded"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    _, metadata, entry = metadata_for(source, path, item["ids"]["shifted"])
    if corruption == "spec":
        entry["spec"]["width"] = 7
    elif corruption == "key":
        entry["key"] = "forged"
    elif corruption == "input_register":
        entry["args"][1] = entry["args"][0]
    else:
        entry["outs"][0] = entry["outs"][0][:-1]
    metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="shift|spec|register|wire|interface|key"):
        make_compact_schedule(target, source, cap_for(original, source))


def test_in_memory_metadata_mutation_rejected(templates, tmp_path):
    item = templates["guarded"]
    target, original, _, path = mutable_candidate(item, tmp_path)
    library = ShiftIntegrationLibrary(path, target, original)
    node = node_for(target, item["ids"]["shifted"])
    _, entry = library.get(node)
    entry["input_contract"]["signed_shift_count_bits"] = False
    with pytest.raises(ValueError, match="metadata|cache|validation"):
        library.get(node)


def test_replay_checks_emitted_gate_sha(templates, tmp_path):
    item = templates["guarded"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    schedule = make_compact_schedule(target, source, cap_for(original, source))
    _, _, entry = metadata_for(source, path, item["ids"]["shifted"])
    gate = path / entry["gate_file"]
    gate.write_bytes(gate.read_bytes() + b"deliberate corruption")
    with pytest.raises(ValueError, match="hash|SHA"):
        execute_compact_parallel(target, source, schedule, {"x": 128, "index": 0})


@pytest.mark.parametrize("mutation", ["input_width", "preparation", "output", "unused_table",
                                     "shift_binding", "node_params"])
def test_bound_compiler_rejects_whole_target_and_requested_node_mutations(
        templates, tmp_path, mutation):
    item = templates["guarded"]
    target, original, _, path = mutable_candidate(item, tmp_path)
    library = ShiftIntegrationLibrary(path, target, original)
    if mutation == "input_width":
        target["nodes"][0]["params"]["bits"] -= 1
    elif mutation == "preparation":
        target["nodes"][0]["params"]["preparation"] = "uniform"
    elif mutation == "output":
        target["outputs"]["Y"] = item["ids"]["doubled"]
    elif mutation == "unused_table":
        target["tables"]["unused"] = [[0], [1]]
    elif mutation == "shift_binding":
        node_for(target, item["ids"]["shifted"])["args"][1] = item["ids"]["doubled"]
    else:
        node_for(target, item["ids"]["shifted"])["params"]["unexpected"] = True
    with pytest.raises(ValueError, match="target|snapshot|frozen|semantic|binding|defined"):
        compile_shift_graph(target, tmp_path / "mutated_source", library)


def test_compiler_lookup_snapshot_mutation_rejected(templates, tmp_path):
    item = templates["guarded"]
    target, original, _, path = mutable_candidate(item, tmp_path)
    library = ShiftIntegrationLibrary(path, target, original)
    library.tables["counts"][0][0] = 1
    with pytest.raises(ValueError, match="table|target|snapshot|frozen"):
        library.get(node_for(target, item["ids"]["shifted"]))


@pytest.mark.parametrize("corruption", ["boolean_ssa", "duplicate_output", "forward_reference"])
def test_external_reader_requires_valid_typed_ordered_ssa_before_masks(
        templates, tmp_path, corruption):
    item = templates["guarded"]
    target, original, source, _ = mutable_candidate(item, tmp_path)
    shifted = node_for(target, item["ids"]["shifted"])
    call = call_for(source, item["ids"]["shifted"])
    if corruption == "boolean_ssa":
        target["nodes"][0]["out"] = [False]
        target["inputs"][0] = False
        shifted["args"][0] = call["args"][0] = False
        source["inputs"][0] = copy.deepcopy(target["nodes"][0])
    elif corruption == "duplicate_output":
        node_for(target, item["ids"]["doubled"])["out"] = [item["ids"]["shifted"]]
        call_for(source, item["ids"]["doubled"])["out"] = [item["ids"]["shifted"]]
    else:
        shifted["args"][1] = call["args"][1] = item["ids"]["doubled"]
    with pytest.raises(ValueError, match="SSA|producer|duplicate|identifier|integer|boolean"):
        make_compact_schedule(target, source, cap_for(original, source))


@pytest.mark.parametrize("mutation", ["target", "source", "call", "storage"])
def test_replay_requires_fingerprints_and_matching_storage(templates, mutation):
    item = templates["guarded"]
    target, source = copy.deepcopy(item["target"]), copy.deepcopy(item["source"])
    schedule = make_compact_schedule(target, source, cap_for(item["original"], source))
    if mutation == "target":
        target["nodes"][0]["params"]["bits"] -= 1
    elif mutation == "source":
        source["forward_calls"][0]["argument_copy_cx"] += 1
    elif mutation == "call":
        call_for(source, item["ids"]["shifted"])["args"][1] = item["ids"]["doubled"]
    else:
        schedule["widths"][item["ids"]["shifted"]] -= 1
    with pytest.raises(ValueError, match="fingerprint|storage|match"):
        execute_compact_parallel(target, source, schedule, {"x": 1, "index": 0})


@pytest.mark.parametrize("case", ["B4x12", "B8x52"])
def test_accepted_a11_preserves_sqrt_log_and_all_nonspecialized_fallback_bytes(tmp_path, case):
    directory = ROOT / "results" / "limitation_program_20261001" / "A11_run001" / case
    target = json.loads((directory / "target.json").read_text(encoding="utf-8"))
    original = json.loads((directory / "source.json").read_text(encoding="utf-8"))
    library = ShiftIntegrationLibrary(tmp_path / "financial_leaves", target, original)
    sqrt_nodes = [node for node in target["nodes"] if node["op"] == "sqrt"]
    assert len(sqrt_nodes) == (30 if case == "B4x12" else 234)
    for node in sqrt_nodes:
        key, entry = library.get(node)
        assert key == call_for(original, node["out"][0])["leaf"]
        assert entry["input_contract"] == {"unsigned_input_bits": 46}
        for name in (key + ".json", entry["gate_file"]):
            assert (library.archive / name).read_bytes() == (library.path / name).read_bytes()
    assert any(entry.get("input_contract") == {"zero_low_bits": 40, "signed_upper_bits": 7}
               for entry in library.original_entries.values())
    shifts = [node for node in target["nodes"] if node["op"] == "shift"]
    assert len(shifts) == (78 if case == "B4x12" else 650)
    for node in shifts:
        key, entry = library.get(node)
        assert key != call_for(original, node["out"][0])["leaf"]
        assert entry["input_contract"] == {"signed_shift_count_bits": 7}
