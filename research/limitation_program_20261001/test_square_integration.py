"""Independent same-SSA guards and full-word XOR checks for signed squaring.

Small graphs exercise dispatch and corruption checks; a 72/f40 graph also
reloads the already accepted unsigned 46-bit square-root promise.  Neither
equal sampled values nor narrower retained SSA storage proves an equality.
"""

import copy
import json
import shutil
from pathlib import Path

import pytest

from research.controlled_source_completion.compact_parallel_v3 import (
    execute_compact_parallel,
    make_compact_schedule,
)
from research.controlled_source_completion.compiler import compile_graph, resolve_library
from research.controlled_source_completion.ir import Graph, evaluate
from research.limitation_program_20261001.square_library import (
    SquareIntegrationLibrary,
    compile_square_graph,
)
from research.limitation_program_20261001.sqrt_library import NarrowSqrtIntegrationLibrary

ROOT = Path(__file__).resolve().parents[2]


def square_graph(*, width=6, fraction=2, distinct=False, lookup=False, sqrt_site=False):
    graph = Graph(fraction, width - fraction)
    x = graph.input("x", 2 if lookup else width, "uniform" if lookup else "provided")
    operand = x
    if lookup:
        graph.tables["signed_operands"] = [[0], [1 << (width - 1)], [(1 << width) - 1],
                                          [(1 << (width - 1)) - 1]]
        operand = graph.node("lookup", (x,), {"table": "signed_operands", "bits": 2})
    y = graph.input("y", width, "provided") if distinct else operand
    product = graph.mul(operand, y)
    doubled = graph.add(product, product)
    graph.outputs = {"Y": product, "alias": product, "doubled": doubled, "operand": operand}
    root = None
    if sqrt_site:
        radicand = graph.input("radicand", 46, "uniform")
        root = graph.node("sqrt", (radicand,))
        graph.outputs["root"] = root
    return graph, {"x": x, "operand": operand, "y": y,
                   "product": product, "doubled": doubled, "root": root}


def call_for(source, value):
    return next(call for call in source["forward_calls"] if call["out"] == [value])


def node_for(target, value):
    return next(node for node in target["nodes"] if node["out"] == [value])


def compile_integration(graph, directory, sqrt_baseline=False):
    target = graph.as_dict()
    original, _ = compile_graph(target, directory / "original")
    if sqrt_baseline:
        narrowed = NarrowSqrtIntegrationLibrary(directory / "sqrt_leaves", target, original)
        original, _ = compile_graph(target, directory / "sqrt_source", narrowed)
    library = SquareIntegrationLibrary(directory / "square_leaves", target, original)
    source, _ = compile_square_graph(target, directory / "candidate", library)
    return target, original, source, library


def initial_words(source):
    width = source["word_width"]
    mask = (1 << width) - 1
    patterns = (int("a5" * 9, 16), mask, (1 << (width - 1)) | 13,
                int("39" * 9, 16), int("e1" * 9, 16))
    return {name: patterns[index % len(patterns)] & mask
            for index, name in enumerate(source["outputs"])}


def assert_result(target, source, schedule, inputs):
    _, trace = evaluate(target, inputs, trace=True)
    initial = initial_words(source)
    expected = {name: trace[value] ^ initial[name] for name, value in target["outputs"].items()}
    got = execute_compact_parallel(target, source, schedule, inputs, initial)
    assert got["values"] == expected
    assert got["all_input_and_workspace_bits_restored"]


@pytest.fixture(scope="module")
def templates(tmp_path_factory):
    result = {}
    for name, kwargs in (("square", {}), ("distinct", {"distinct": True}),
                         ("lookup", {"lookup": True}),
                         ("production", {"width": 72, "fraction": 40, "sqrt_site": True})):
        graph, ids = square_graph(**kwargs)
        target, original, source, library = compile_integration(
            graph, tmp_path_factory.mktemp("square_" + name), sqrt_baseline=name == "production"
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


def cap_for(original, candidate):
    # Guard tests use enough private workspace for either leaf family.  The
    # production experiment separately checks the actual accepted B4/B8 caps.
    return max(original["resources"]["logical_qubits"],
               candidate["resources"]["logical_qubits"])


def test_same_ssa_signed_square_exhaustive_small_graph_and_full_output_xor(templates):
    item = templates["square"]
    target, original, source, library = [item[name] for name in
                                       ("target", "original", "source", "library")]
    product = item["ids"]["product"]
    old_key, key = call_for(original, product)["leaf"], call_for(source, product)["leaf"]
    assert key != old_key
    entry = library.entries[key]
    assert entry["input_contract"] == {"same_ssa_arguments": True}
    assert entry["args"] == [list(range(6)), list(range(6, 12))]
    assert entry["outs"] == [list(range(12, 18))]
    schedule = make_compact_schedule(target, source, cap_for(original, source))
    for x in range(1 << 6):
        assert_result(target, source, schedule, {"x": x})


def test_production_signed_endpoints_high_output_bits_and_accepted_sqrt_compatibility(templates):
    item = templates["production"]
    target, original, source, library = [item[name] for name in
                                       ("target", "original", "source", "library")]
    product, root = item["ids"]["product"], item["ids"]["root"]
    entry = library.entries[call_for(source, product)["leaf"]]
    assert entry["args"] == [list(range(72)), list(range(72, 144))]
    assert entry["outs"] == [list(range(144, 216))]
    assert entry["input_contract"] == {"same_ssa_arguments": True}
    assert call_for(original, root)["leaf"] == call_for(source, root)["leaf"]
    sqrt_entry = library.entries[call_for(source, root)["leaf"]]
    assert sqrt_entry["input_contract"] == {"unsigned_input_bits": 46}
    for name in (call_for(source, root)["leaf"] + ".json", sqrt_entry["gate_file"]):
        assert (resolve_library(original) / name).read_bytes() == (library.path / name).read_bytes()
    schedule = make_compact_schedule(target, source, cap_for(original, source))
    mask = (1 << 72) - 1
    values = (0, 1, (1 << 40) - 1, 1 << 40, (1 << 71) - 1,
              1 << 71, (1 << 71) + 1, mask, mask - (1 << 40))
    for index, raw in enumerate(values):
        assert_result(target, source, schedule,
                      {"x": raw, "radicand": (1 << 45) + index})


def test_repeated_ssa_retains_both_argument_copies_and_original_storage_masks(templates):
    item = templates["square"]
    target, original, source = [item[name] for name in ("target", "original", "source")]
    call = call_for(source, item["ids"]["product"])
    assert call["args"] == [item["ids"]["operand"], item["ids"]["operand"]]
    assert call["argument_copy_cx"] == 4 * 6
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


def test_distinct_ssa_equal_sample_values_keep_fallback_metadata_and_gate_bytes(templates):
    item = templates["distinct"]
    target, original, source, library = [item[name] for name in
                                       ("target", "original", "source", "library")]
    value = item["ids"]["product"]
    old_key, key = call_for(original, value)["leaf"], call_for(source, value)["leaf"]
    assert old_key == key
    entry = library.entries[key]
    for name in (key + ".json", entry["gate_file"]):
        assert (resolve_library(original) / name).read_bytes() == (library.path / name).read_bytes()
    schedule = make_compact_schedule(target, source, cap_for(original, source))
    for x, y in ((0, 0), (31, 31), (32, 32), (63, 63), (1, 2), (32, 63), (31, 32)):
        assert_result(target, source, schedule, {"x": x, "y": y})


def test_lookup_signed_literal_rows_can_be_squared_from_same_actual_ssa(templates):
    item = templates["lookup"]
    source, original, target = [item[name] for name in ("source", "original", "target")]
    assert call_for(source, item["ids"]["product"])["leaf"] != call_for(
        original, item["ids"]["product"]
    )["leaf"]
    schedule = make_compact_schedule(target, source, cap_for(original, source))
    for x in range(4):
        assert_result(target, source, schedule, {"x": x})


def test_fresh_generated_cache_reload_preserves_key_and_bytes(templates, tmp_path):
    item = templates["square"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    key, _, entry = metadata_for(source, path, item["ids"]["product"])
    before = {name: (path / name).read_bytes() for name in (key + ".json", entry["gate_file"])}
    library = SquareIntegrationLibrary(path, target, original)
    got_key, _ = library.get(node_for(target, item["ids"]["product"]))
    assert got_key == key
    for name, value in before.items():
        assert (path / name).read_bytes() == value
    compiled, _ = compile_square_graph(target, tmp_path / "recompiled", library)
    schedule = make_compact_schedule(target, compiled, cap_for(original, source))
    assert_result(target, compiled, schedule, {"x": 32})


@pytest.mark.parametrize("template_name", ["square", "production"])
def test_specialized_archive_reload_revalidates_actual_ssa_promises(
        templates, tmp_path, template_name):
    item = templates[template_name]
    target, _, source, _ = mutable_candidate(item, tmp_path)
    library = SquareIntegrationLibrary(tmp_path / "second_generation", target, source)
    compiled, _ = compile_square_graph(target, tmp_path / "second_source", library)
    value = item["ids"]["product"]
    assert call_for(compiled, value)["leaf"] == call_for(source, value)["leaf"]
    schedule = make_compact_schedule(target, compiled,
                                     cap_for(item["original"], source))
    inputs = {"x": 1 << (target["width"] - 1)}
    if template_name == "production":
        inputs["radicand"] = (1 << 46) - 1
    assert_result(target, compiled, schedule, inputs)


@pytest.mark.parametrize("contract", [
    None, {}, {"same_ssa_arguments": False}, {"same_ssa_arguments": 1},
    {"same_ssa_arguments": "true"}, {"same_ssa_arguments": True, "zero_low_bits": 0},
])
def test_missing_empty_false_or_malformed_square_promises_cannot_hide_specialization(
        templates, tmp_path, contract):
    item = templates["square"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    _, metadata, entry = metadata_for(source, path, item["ids"]["product"])
    if contract is None:
        entry.pop("input_contract")
    else:
        entry["input_contract"] = contract
    metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="same|square|contract|promise|spec"):
        make_compact_schedule(target, source, cap_for(original, source))
    with pytest.raises(ValueError, match="same|square|contract|promise|spec"):
        SquareIntegrationLibrary(tmp_path / "reload", target, source)


def test_authentic_square_gate_archive_cannot_be_attached_to_distinct_ssa(templates, tmp_path):
    item = templates["distinct"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    square = templates["square"]
    specialized = call_for(square["source"], square["ids"]["product"])["leaf"]
    entry = square["library"].entries[specialized]
    for name in (specialized + ".json", entry["gate_file"]):
        shutil.copy2(square["library"].path / name, path / name)
    call_for(source, item["ids"]["product"])["leaf"] = specialized
    source["library_keys"] = sorted({call["leaf"] for call in source["forward_calls"]})
    with pytest.raises(ValueError, match="same|square|contract|promise|proof|distinct"):
        make_compact_schedule(target, source, cap_for(original, source))
    with pytest.raises(ValueError, match="same|square|contract|promise|proof|distinct"):
        SquareIntegrationLibrary(tmp_path / "reload", target, source)


@pytest.mark.parametrize("malformed_spec", [None, [], "not a specification"])
def test_outer_square_promise_cannot_be_hidden_by_non_mapping_spec(
        templates, tmp_path, malformed_spec):
    item = templates["square"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    _, metadata, entry = metadata_for(source, path, item["ids"]["product"])
    entry["spec"] = malformed_spec
    metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="square|contract|spec"):
        make_compact_schedule(target, source, cap_for(original, source))
    with pytest.raises(ValueError, match="square|contract|spec"):
        SquareIntegrationLibrary(tmp_path / "reload", target, source)


@pytest.mark.parametrize("malformed_spec", [None, [], "not a specification"])
def test_accepted_sqrt_promise_cannot_be_hidden_by_non_mapping_spec(
        templates, tmp_path, malformed_spec):
    item = templates["production"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    _, metadata, entry = metadata_for(source, path, item["ids"]["root"])
    entry["spec"] = malformed_spec
    metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="sqrt|contract|spec"):
        make_compact_schedule(target, source, cap_for(original, source))
    with pytest.raises(ValueError, match="sqrt|contract|spec"):
        SquareIntegrationLibrary(tmp_path / "reload", target, source)


@pytest.mark.parametrize("corruption", ["outer_contract", "spec_contract", "spec_width",
                                         "input_register", "output_register", "resource", "gate"])
def test_generated_cache_spec_interface_resources_and_sha_are_checked(
        templates, tmp_path, corruption):
    item = templates["square"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    _, metadata, entry = metadata_for(source, path, item["ids"]["product"])
    if corruption == "gate":
        gate = path / entry["gate_file"]
        gate.write_bytes(gate.read_bytes() + b"deliberate corruption")
    else:
        if corruption == "outer_contract":
            entry["input_contract"]["same_ssa_arguments"] = False
        elif corruption == "spec_contract":
            entry["spec"]["input_contract"]["same_ssa_arguments"] = False
        elif corruption == "spec_width":
            entry["spec"]["width"] = 5
        elif corruption == "input_register":
            entry["args"][1] = entry["args"][0]
        elif corruption == "output_register":
            entry["outs"][0] = entry["outs"][0][:-1]
        else:
            entry["resources"]["t_count"] += 7
        metadata.write_text(json.dumps(entry), encoding="utf-8")
    error = "cache|hash|SHA|metadata|contract|spec|resource|interface|layout"
    with pytest.raises(ValueError, match=error):
        library = SquareIntegrationLibrary(path, target, original)
        library.get(node_for(target, item["ids"]["product"]))


@pytest.mark.parametrize("corruption", ["spec", "input_register", "output_register"])
def test_scheduling_rechecks_square_spec_and_full_native_register_interface(
        templates, tmp_path, corruption):
    item = templates["square"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    _, metadata, entry = metadata_for(source, path, item["ids"]["product"])
    if corruption == "spec":
        entry["spec"]["width"] = 5
    elif corruption == "input_register":
        entry["args"][1] = entry["args"][0]
    else:
        entry["outs"][0] = entry["outs"][0][:-1]
    metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="square|spec|register|wire|interface|layout"):
        make_compact_schedule(target, source, cap_for(original, source))


def test_in_memory_specialized_metadata_mutation_is_rejected(templates, tmp_path):
    item = templates["square"]
    target, original, _, path = mutable_candidate(item, tmp_path)
    library = SquareIntegrationLibrary(path, target, original)
    node = node_for(target, item["ids"]["product"])
    _, entry = library.get(node)
    entry["input_contract"]["same_ssa_arguments"] = False
    with pytest.raises(ValueError, match="metadata|cache|validation"):
        library.get(node)


def test_gate_sha_is_checked_at_emitted_full_source_replay(templates, tmp_path):
    item = templates["square"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    schedule = make_compact_schedule(target, source, cap_for(original, source))
    _, _, entry = metadata_for(source, path, item["ids"]["product"])
    gate = path / entry["gate_file"]
    gate.write_bytes(gate.read_bytes() + b"deliberate corruption")
    with pytest.raises(ValueError, match="hash|SHA"):
        execute_compact_parallel(target, source, schedule, {"x": 32})


@pytest.mark.parametrize("mutation", ["input_width", "preparation", "output", "unused_table",
                                     "mul_binding", "node_params"])
def test_bound_compiler_rejects_whole_target_and_requested_node_mutations(
        templates, tmp_path, mutation):
    item = templates["square"]
    target, original, _, path = mutable_candidate(item, tmp_path)
    library = SquareIntegrationLibrary(path, target, original)
    if mutation == "input_width":
        target["nodes"][0]["params"]["bits"] -= 1
    elif mutation == "preparation":
        target["nodes"][0]["params"]["preparation"] = "uniform"
    elif mutation == "output":
        target["outputs"]["Y"] = item["ids"]["doubled"]
    elif mutation == "unused_table":
        target["tables"]["unused"] = [[0], [1]]
    elif mutation == "mul_binding":
        node_for(target, item["ids"]["product"])["args"][1] = item["ids"]["doubled"]
    else:
        node_for(target, item["ids"]["product"])["params"]["unexpected"] = True
    with pytest.raises(ValueError, match="target|snapshot|same|frozen|semantic|binding|defined"):
        compile_square_graph(target, tmp_path / "mutated_source", library)


def test_compiler_lookup_snapshot_mutation_is_rejected(templates, tmp_path):
    item = templates["lookup"]
    target, original, _, path = mutable_candidate(item, tmp_path)
    library = SquareIntegrationLibrary(path, target, original)
    library.tables["signed_operands"][1][0] = 1
    with pytest.raises(ValueError, match="table|target|snapshot|frozen"):
        library.get(node_for(target, item["ids"]["product"]))


@pytest.mark.parametrize("corruption", ["boolean_ssa", "duplicate_output", "forward_reference"])
def test_square_only_external_reader_requires_valid_typed_ordered_ssa(
        templates, tmp_path, corruption):
    item = templates["square"]
    target, original, source, _ = mutable_candidate(item, tmp_path)
    product = node_for(target, item["ids"]["product"])
    call = call_for(source, item["ids"]["product"])
    if corruption == "boolean_ssa":
        target["nodes"][0]["out"] = [False]
        target["inputs"] = [False]
        product["args"] = call["args"] = [False, False]
        source["inputs"] = [copy.deepcopy(target["nodes"][0])]
    elif corruption == "duplicate_output":
        node_for(target, item["ids"]["doubled"])["out"] = [item["ids"]["product"]]
        call_for(source, item["ids"]["doubled"])["out"] = [item["ids"]["product"]]
    else:
        product["args"] = call["args"] = [item["ids"]["doubled"], item["ids"]["doubled"]]
    with pytest.raises(ValueError, match="SSA|producer|duplicate|identifier|integer|boolean"):
        make_compact_schedule(target, source, cap_for(original, source))


@pytest.mark.parametrize("mutation", ["target", "source", "call", "storage"])
def test_replay_requires_fingerprinted_source_target_and_matching_storage(templates, mutation):
    item = templates["square"]
    target, source = copy.deepcopy(item["target"]), copy.deepcopy(item["source"])
    schedule = make_compact_schedule(
        target, source, cap_for(item["original"], source)
    )
    if mutation == "target":
        target["nodes"][0]["params"]["bits"] -= 1
    elif mutation == "source":
        source["forward_calls"][0]["argument_copy_cx"] += 1
    elif mutation == "call":
        call_for(source, item["ids"]["product"])["args"][1] = item["ids"]["doubled"]
    else:
        schedule["widths"][item["ids"]["product"]] -= 1
    with pytest.raises(ValueError, match="fingerprint|storage|match"):
        execute_compact_parallel(target, source, schedule, {"x": 1})


@pytest.mark.parametrize("case", ["B4x12", "B8x52"])
def test_real_accepted_a11_archive_preserves_all_unsigned_sqrt_and_signed_log_contracts(
        tmp_path, case):
    directory = ROOT / "results" / "limitation_program_20261001" / "A11_run001" / case
    target = json.loads((directory / "target.json").read_text(encoding="utf-8"))
    original = json.loads((directory / "source.json").read_text(encoding="utf-8"))
    library = SquareIntegrationLibrary(tmp_path / "financial_leaves", target, original)
    sqrt_nodes = [node for node in target["nodes"] if node["op"] == "sqrt"]
    assert len(sqrt_nodes) == (30 if case == "B4x12" else 234)
    for node in sqrt_nodes:
        key, entry = library.get(node)
        assert key == call_for(original, node["out"][0])["leaf"]
        assert entry["input_contract"] == {"unsigned_input_bits": 46}
    assert any(entry.get("input_contract") == {"zero_low_bits": 40, "signed_upper_bits": 7}
               for entry in library.original_entries.values())
