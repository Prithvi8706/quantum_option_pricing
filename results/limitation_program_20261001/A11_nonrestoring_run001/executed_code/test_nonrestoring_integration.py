"""Non-restoring actual-SSA guards, clean XOR and adopted shift preservation."""

import copy
import json
import math
import shutil
from pathlib import Path

import pytest

from research.controlled_source_completion.compact_parallel_v5 import (
    execute_compact_parallel,
    make_compact_schedule,
)
from research.controlled_source_completion.compiler import compile_graph, resolve_library
from research.controlled_source_completion.ir import Graph
from research.limitation_program_20261001.nonrestoring_library import (
    NonRestoringIntegrationLibrary,
    compile_nonrestoring_graph,
)
from research.limitation_program_20261001.prove_nonrestoring_input import (
    INTEGRATION_LOWERING,
    prove_nonrestoring_site,
)
from research.limitation_program_20261001.shift_library import ShiftIntegrationLibrary
from research.limitation_program_20261001.sqrt_library import NarrowSqrtIntegrationLibrary

WIDTH, FRACTION, ACTIVE = 72, 40, 46
MASK = (1 << WIDTH) - 1
ROOT = Path(__file__).resolve().parents[2]


def sqrt_graph(*, bits=ACTIVE, preparation="uniform", lookup=False,
               width=WIDTH, fraction=FRACTION, shift=False):
    """Raw sqrt deliberately avoids Graph.sqrt's optional signed clamp."""
    graph = Graph(fraction, width - fraction)
    raw = graph.input("x", 1 if lookup else bits, preparation)
    operand = raw
    if lookup:
        graph.tables["radicands"] = [[0], [1 << (bits - 1)]]
        operand = graph.node("lookup", (raw,), {"table": "radicands", "bits": 1})
    root = graph.node("sqrt", (operand,))
    doubled = graph.add(root, root)
    graph.outputs = {"Y": root, "alias": root, "doubled": doubled, "operand": operand}
    shifted = None
    if shift:
        data = graph.input("data", width, "provided")
        index = graph.input("index", 3, "uniform")
        mask = (1 << width) - 1
        graph.tables["counts"] = [[v & mask] for v in (-64, -1, 0, 1, 33, 63, -63, -16)]
        count = graph.node("lookup", (index,), {"table": "counts", "bits": 3})
        shifted = graph.shift(data, count)
        graph.outputs["shifted"] = shifted
    return graph, {"raw": raw, "operand": operand, "root": root,
                   "doubled": doubled, "shifted": shifted}


def compile_integration(graph, directory, active_bits=ACTIVE, accepted_baseline=False):
    target = graph.as_dict()
    original, _ = compile_graph(target, directory / "original")
    if accepted_baseline:
        restoring = NarrowSqrtIntegrationLibrary(directory / "restoring_leaves", target, original)
        original, _ = compile_graph(target, directory / "restoring_source", restoring)
        shift = ShiftIntegrationLibrary(directory / "shift_leaves", target, original)
        original, _ = compile_graph(target, directory / "shift_source", shift)
    library = NonRestoringIntegrationLibrary(
        directory / "new_leaves", target, original, active_bits=active_bits
    )
    source, _ = compile_nonrestoring_graph(target, directory / "candidate", library)
    return target, original, source, library


def call_for(source, value):
    return next(call for call in source["forward_calls"] if call["out"] == [value])


def node_for(target, value):
    return next(node for node in target["nodes"] if node["out"] == [value])


def cap_for(original, candidate):
    return max(original["resources"]["logical_qubits"],
               candidate["resources"]["logical_qubits"])


def initial_words(source):
    # High bits must remain present even though a correct result needs 43 bits.
    values = [int("a5" * 9, 16), MASK, (1 << 71) | 13, int("39" * 9, 16)]
    mask = (1 << source["word_width"]) - 1
    return {name: values[index % len(values)] & mask
            for index, name in enumerate(source["outputs"])}


def assert_result(target, source, schedule, raw, operand=None):
    operand = raw if operand is None else operand
    root = math.isqrt(operand << target["fraction_bits"])
    mask = (1 << target["width"]) - 1
    expected = {"Y": root, "alias": root, "doubled": (2 * root) & mask, "operand": operand}
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
        ("small", {"width": 5, "fraction": 2, "bits": 3}),
        ("accepted", {"shift": True}),
    ):
        graph, ids = sqrt_graph(**kwargs)
        directory = tmp_path_factory.mktemp("sqrt_" + name)
        target, original, source, library = compile_integration(
            graph, directory, active_bits=3 if name == "small" else ACTIVE,
            accepted_baseline=name == "accepted",
        )
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
    assert entry["spec"]["integration_lowering"] == INTEGRATION_LOWERING
    schedule = make_compact_schedule(target, source, cap_for(original, source))
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
                                     cap_for(original, source))
    values = (0, 1, (1 << 45), (1 << ACTIVE) - 1)
    if template_name == "generic":
        values += (1 << 71, MASK)
    for raw in values:
        assert_result(item["target"], source, schedule, raw)


def test_lookup_interval_uses_every_literal_row_and_unsigned_operand(templates):
    item = templates["lookup"]
    source = item["source"]
    key = call_for(item["source"], item["ids"]["root"])["leaf"]
    assert key != call_for(item["original"], item["ids"]["root"])["leaf"]
    assert item["library"].entries[key]["input_contract"] == {"unsigned_input_bits": ACTIVE}
    schedule = make_compact_schedule(item["target"], item["source"],
                                     cap_for(item["original"], source))
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
    reloaded = NonRestoringIntegrationLibrary(path, target, original)
    got_key, got_entry = reloaded.get(node)
    assert got_key == key
    assert got_entry["input_contract"] == {"unsigned_input_bits": ACTIVE}
    for name, value in before.items():
        assert (path / name).read_bytes() == value
    compiled, _ = compile_graph(target, tmp_path / "recompiled", reloaded)
    schedule = make_compact_schedule(target, compiled, cap_for(original, source))
    assert_result(target, compiled, schedule, 1 << 45)


def test_already_specialized_source_can_be_reloaded_with_proof_at_actual_site(templates, tmp_path):
    item = templates["proved"]
    target, _, source, _ = mutable_candidate(item, tmp_path)
    library = NonRestoringIntegrationLibrary(tmp_path / "second_generation", target, source)
    compiled, _ = compile_nonrestoring_graph(target, tmp_path / "second_source", library)
    value = item["ids"]["root"]
    assert call_for(compiled, value)["leaf"] == call_for(source, value)["leaf"]
    schedule = make_compact_schedule(target, compiled,
                                     cap_for(item["original"], source))
    assert_result(target, compiled, schedule, (1 << ACTIVE) - 1)


@pytest.mark.parametrize("contract", [
    None, {}, [],
    {"unsigned_input_bits": False},
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
    if contract is None:
        entry.pop("input_contract")
    else:
        entry["input_contract"] = contract
    metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="unsigned|contract|promise|proof|narrow|spec"):
        make_compact_schedule(target, source, cap_for(original, source))
    with pytest.raises(ValueError, match="unsigned|contract|promise|proof|narrow|spec"):
        NonRestoringIntegrationLibrary(tmp_path / "reload", target, source)


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
        make_compact_schedule(target, source, cap_for(original, source))
    with pytest.raises(ValueError, match="unsigned|contract|promise|proof|narrow"):
        NonRestoringIntegrationLibrary(tmp_path / "reload", target, source)


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
        make_compact_schedule(target, source, cap_for(original, source))
    with pytest.raises(ValueError, match=error):
        NonRestoringIntegrationLibrary(tmp_path / "reload", target, source)


@pytest.mark.parametrize("corruption", ["contract", "spec", "gate", "resources", "key",
                                      "input_register", "output_register"])
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
    elif corruption in ("key", "input_register", "output_register"):
        if corruption == "key":
            entry["key"] = "forged"
        elif corruption == "input_register":
            entry["args"][0] = entry["args"][0][:-1]
        else:
            entry["outs"][0] = entry["outs"][0][:-1]
        metadata.write_text(json.dumps(entry), encoding="utf-8")
    else:
        entry["input_contract" if corruption == "contract" else "spec"]["unsigned_input_bits"] = 45
        metadata.write_text(json.dumps(entry), encoding="utf-8")
    error = "cache|hash|SHA|metadata|contract|spec|resource|register|layout|interface"
    with pytest.raises(ValueError, match=error):
        reloaded = NonRestoringIntegrationLibrary(path, target, original)
        reloaded.get(node_for(target, item["ids"]["root"]))


def test_in_memory_metadata_corruption_is_rejected(templates, tmp_path):
    item = templates["proved"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    library = NonRestoringIntegrationLibrary(path, target, original)
    node = node_for(target, item["ids"]["root"])
    key, entry = library.get(node)
    entry["input_contract"]["unsigned_input_bits"] = 45
    with pytest.raises(ValueError, match="metadata|cache|validation"):
        library.get(node)


def test_gate_sha_is_checked_at_full_source_replay(templates, tmp_path):
    item = templates["proved"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    schedule = make_compact_schedule(target, source, cap_for(original, source))
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
        NonRestoringIntegrationLibrary(path, target, original)


def test_mutating_compiler_table_snapshot_is_rejected(templates, tmp_path):
    item = templates["lookup"]
    target, original, _, path = mutable_candidate(item, tmp_path)
    library = NonRestoringIntegrationLibrary(path, target, original)
    library.tables["radicands"][1][0] = 1 << 70
    with pytest.raises(ValueError, match="table|target|snapshot|frozen"):
        library.get(node_for(target, item["ids"]["root"]))


@pytest.mark.parametrize("mutation", ["input_width", "preparation", "output", "unused_table"])
def test_bound_compiler_rejects_any_whole_target_mutation(templates, tmp_path, mutation):
    item = templates["proved"]
    target, original, _, path = mutable_candidate(item, tmp_path)
    library = NonRestoringIntegrationLibrary(path, target, original)
    if mutation == "input_width":
        target["nodes"][0]["params"]["bits"] = WIDTH
    elif mutation == "preparation":
        target["nodes"][0]["params"]["preparation"] = "provided"
    elif mutation == "output":
        target["outputs"]["Y"] = item["ids"]["doubled"]
    else:
        target["tables"]["unused"] = [[0], [1]]
    with pytest.raises(ValueError, match="target|snapshot|same|frozen|semantic"):
        compile_nonrestoring_graph(target, tmp_path / "mutated_source", library)


def test_raw_compiler_upstream_mutation_is_rejected_at_scheduling_boundary(templates, tmp_path):
    item = templates["proved"]
    target, original, _, path = mutable_candidate(item, tmp_path)
    library = NonRestoringIntegrationLibrary(path, target, original)
    target["nodes"][0]["params"]["bits"] = WIDTH
    # The old generic compiler has no whole-target handshake. The new reader
    # must independently recompute the actual invocation's range nonetheless.
    source, _ = compile_graph(target, tmp_path / "raw_source", library)
    with pytest.raises(ValueError, match="unsigned|contract|promise|proof"):
        make_compact_schedule(target, source, cap_for(original, source))


@pytest.mark.parametrize("mutation", ["target", "source", "storage"])
def test_replay_requires_matching_schedule_fingerprints_and_storage(templates, mutation):
    item = templates["proved"]
    target, source = copy.deepcopy(item["target"]), copy.deepcopy(item["source"])
    schedule = make_compact_schedule(target, source,
                                     cap_for(item["original"], source))
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
    source = item["source"]
    schedule = make_compact_schedule(item["target"], item["source"],
                                     cap_for(item["original"], source))
    for raw in (-1, 1 << ACTIVE):
        with pytest.raises(ValueError, match="input|bit-width|promise"):
            execute_compact_parallel(item["target"], item["source"], schedule, {"x": raw})


def test_small_root_exhaustive_forward_reverse_and_dirty_output_aliases(templates):
    item = templates["small"]
    target, source = item["target"], item["source"]
    schedule = make_compact_schedule(target, source, cap_for(item["original"], source))
    for raw in range(8):
        assert_result(target, source, schedule, raw)


def test_nonrestoring_dispatch_preserves_adopted_signed7_shift_bytes(templates):
    item = templates["accepted"]
    target, original, source, library = [item[name] for name in
                                       ("target", "original", "source", "library")]
    root = item["ids"]["root"]
    assert call_for(source, root)["leaf"] != call_for(original, root)["leaf"]
    for old, new in zip(original["forward_calls"], source["forward_calls"]):
        if old["out"] == [root]:
            continue
        assert old == new
        key = new["leaf"]
        entry = library.entries[key]
        for name in (key + ".json", entry["gate_file"]):
            assert (library.archive / name).read_bytes() == (library.path / name).read_bytes()
    shift = library.entries[call_for(source, item["ids"]["shifted"])["leaf"]]
    assert shift["input_contract"] == {"signed_shift_count_bits": 7}
    schedule = make_compact_schedule(target, source, cap_for(original, source))
    initial = initial_words(source)
    mask = (1 << 72) - 1
    data = (1 << 71) + 13
    counts = (-64, -1, 0, 1, 33, 63, -63, -16)
    for index, count in enumerate(counts):
        raw = (1 << 45) + index
        root_value = math.isqrt(raw << 40)
        shifted = ((data << count) if count >= 0 else
                   ((data - (1 << 72)) >> -count)) & mask
        expected = {"Y": root_value, "alias": root_value,
                    "doubled": (2 * root_value) & mask,
                    "operand": raw, "shifted": shifted}
        got = execute_compact_parallel(target, source, schedule,
                                       {"x": raw, "data": data, "index": index}, initial)
        assert got["values"] == {name: initial[name] ^ v for name, v in expected.items()}
        assert got["all_input_and_workspace_bits_restored"]


def test_new_root_reader_revalidates_adopted_shift_count_contract(templates, tmp_path):
    item = templates["accepted"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    key = call_for(source, item["ids"]["shifted"])["leaf"]
    metadata = path / (key + ".json")
    entry = json.loads(metadata.read_text(encoding="utf-8"))
    entry["input_contract"]["signed_shift_count_bits"] = False
    metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="shift|count|contract|spec"):
        make_compact_schedule(target, source, cap_for(original, source))
    with pytest.raises(ValueError, match="shift|count|contract|spec"):
        NonRestoringIntegrationLibrary(tmp_path / "reload", target, source)


def test_algorithm_marker_cannot_hide_removed_lowering_and_outer_promise(templates, tmp_path):
    item = templates["proved"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    key = call_for(source, item["ids"]["root"])["leaf"]
    metadata = path / (key + ".json")
    entry = json.loads(metadata.read_text(encoding="utf-8"))
    entry.pop("input_contract")
    entry["spec"].pop("lowering")
    entry["spec"].pop("integration_lowering")
    metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="unsigned|contract|root|sqrt|spec"):
        make_compact_schedule(target, source, cap_for(original, source))
    with pytest.raises(ValueError, match="unsigned|contract|root|sqrt|spec"):
        NonRestoringIntegrationLibrary(tmp_path / "reload", target, source)


@pytest.mark.parametrize("malformed_spec", [None, [], "not a specification"])
def test_unsigned_promise_cannot_hide_in_malformed_spec(templates, tmp_path, malformed_spec):
    item = templates["proved"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    key = call_for(source, item["ids"]["root"])["leaf"]
    metadata = path / (key + ".json")
    entry = json.loads(metadata.read_text(encoding="utf-8"))
    entry["spec"] = malformed_spec
    metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="unsigned|sqrt|contract|spec"):
        make_compact_schedule(target, source, cap_for(original, source))
    with pytest.raises(ValueError, match="unsigned|sqrt|contract|spec"):
        NonRestoringIntegrationLibrary(tmp_path / "reload", target, source)


@pytest.mark.parametrize("corruption", ["key", "input_register", "output_register", "op"])
def test_schedule_requires_canonical_key_operation_and_native_interface(
        templates, tmp_path, corruption):
    item = templates["proved"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    key = call_for(source, item["ids"]["root"])["leaf"]
    metadata = path / (key + ".json")
    entry = json.loads(metadata.read_text(encoding="utf-8"))
    if corruption == "key":
        entry["key"] = "forged"
    elif corruption == "input_register":
        entry["args"][0] = entry["args"][0][:-1]
    elif corruption == "output_register":
        entry["outs"][0] = entry["outs"][0][:-1]
    else:
        entry["op"] = "add"
    metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="root|sqrt|spec|key|interface|register|semantics"):
        make_compact_schedule(target, source, cap_for(original, source))


@pytest.mark.parametrize("corruption", ["boolean_ssa", "duplicate_output", "forward_reference"])
def test_external_reader_validates_typed_ordered_ssa_before_root_masks(
        templates, tmp_path, corruption):
    item = templates["proved"]
    target, original, source, _ = mutable_candidate(item, tmp_path)
    root = node_for(target, item["ids"]["root"])
    call = call_for(source, item["ids"]["root"])
    if corruption == "boolean_ssa":
        target["nodes"][0]["out"] = [False]
        target["inputs"][0] = False
        root["args"][0] = call["args"][0] = False
        source["inputs"][0] = copy.deepcopy(target["nodes"][0])
    elif corruption == "duplicate_output":
        node_for(target, item["ids"]["doubled"])["out"] = [item["ids"]["root"]]
        call_for(source, item["ids"]["doubled"])["out"] = [item["ids"]["root"]]
    else:
        root["args"][0] = call["args"][0] = item["ids"]["doubled"]
    with pytest.raises(ValueError, match="SSA|producer|duplicate|identifier|integer|boolean"):
        make_compact_schedule(target, source, cap_for(original, source))


def test_proof_rejects_detached_root_with_foreign_output(templates):
    item = templates["proved"]
    node = copy.deepcopy(node_for(item["target"], item["ids"]["root"]))
    node["out"] = [10_000]
    with pytest.raises(ValueError, match="bound|target"):
        prove_nonrestoring_site(item["target"], node, item["library"].bounds)


@pytest.mark.parametrize("case", ["B4x12", "B8x52"])
def test_actual_accepted_shift_sources_prove_every_root_and_keep_nonsqrt_bytes(tmp_path, case):
    directory = ROOT / "results" / "limitation_program_20261001" / "A07_shift_run001" / case
    target = json.loads((directory / "target.json").read_text(encoding="utf-8"))
    original = json.loads((directory / "source.json").read_text(encoding="utf-8"))
    library = NonRestoringIntegrationLibrary(tmp_path / "financial_leaves", target, original)
    nodes = [n for n in target["nodes"] if n["op"] != "input"]
    roots = shifts = lookups = 0
    checked = set()
    for node, old_call in zip(nodes, original["forward_calls"]):
        key, entry = library.get(node)
        if node["op"] == "sqrt":
            roots += 1
            assert key != old_call["leaf"]
            proof = prove_nonrestoring_site(target, node, library.bounds)
            assert proof["all_declared_input_patterns"]
            assert 0 <= proof["input_bounds"][0] <= proof["input_bounds"][1] < 1 << 46
            assert entry["input_contract"] == {"unsigned_input_bits": 46}
            continue
        assert key == old_call["leaf"]
        if key not in checked:
            for name in (key + ".json", entry["gate_file"]):
                assert (library.archive / name).read_bytes() == (library.path / name).read_bytes()
            checked.add(key)
        if node["op"] == "shift":
            shifts += 1
            assert entry["input_contract"] == {"signed_shift_count_bits": 7}
        if node["op"] == "lookup" and len(target["tables"][node["params"]["table"]]) == 32:
            lookups += 1
    assert roots == (30 if case == "B4x12" else 234)
    assert shifts == (78 if case == "B4x12" else 650)
    assert lookups >= roots
    assert any(entry.get("input_contract") == {"zero_low_bits": 40, "signed_upper_bits": 7}
               for entry in library.original_entries.values())
