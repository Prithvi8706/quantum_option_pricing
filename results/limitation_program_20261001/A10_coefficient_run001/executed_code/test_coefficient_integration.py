"""Full signed coefficient dispatch, canonical admission and frozen fallbacks."""

import copy
import json
from pathlib import Path
import shutil

import pytest

from research.controlled_source_completion.compact_parallel_v7 import (
    execute_compact_parallel,
    make_compact_schedule,
)
from research.controlled_source_completion.compiler import compile_graph, resolve_library
from research.controlled_source_completion.ir import Graph, evaluate
from research.limitation_program_20261001.coefficient_library import (
    CoefficientIntegrationLibrary,
    compile_coefficient_graph,
)
from research.limitation_program_20261001.nonrestoring_library import NonRestoringIntegrationLibrary
from research.limitation_program_20261001.prove_coefficient_input import (
    FRONTIER,
    INTEGRATION_LOWERING,
    STRATEGIES,
    coefficient_leaf_spec,
    frontier_leaf_spec,
    validate_coefficient_entry,
)
from research.limitation_program_20261001.range_library import (
    RangeIntegrationLibrary,
    compile_range_graph,
)
from research.limitation_program_20261001.shift_library import ShiftIntegrationLibrary

ROOT = Path(__file__).resolve().parents[2]
PREFIX_STRATEGY = "signed-digit-prefix-carry-save"
TOP_COEFFICIENTS = (1067016148260, 60222732077, 22906492245)


def coefficient_graph(width=6, fraction=2, *, accepted=False):
    graph = Graph(fraction, width - fraction)
    mask = (1 << width) - 1
    raw = graph.input("raw", width, "provided")
    index = graph.input("index", 5, "uniform")
    graph.tables["coefficients"] = [[((i % 8) - 4) & mask, ((i % 3) - 1) & mask] for i in range(32)]
    left, right = graph.node("lookup", (index,), {"table": "coefficients", "bits": 5}, 2)
    ranged = graph.mul(left, right)
    coefficients = TOP_COEFFICIENTS if accepted else (11, -9, 0)
    products = [graph.node("cmul", (raw,), {"c": c}) for c in coefficients]
    fallback = graph.node("cmul", (raw,), {"c": 17})
    graph.outputs = {
        "Y": products[0],
        "alias": products[0],
        "second": products[1],
        "third": products[2],
        "ranged": ranged,
        "fallback": fallback,
        "raw": raw,
    }
    root = shifted = None
    if accepted:
        radicand = graph.input("radicand", 46, "uniform")
        root = graph.node("sqrt", (radicand,))
        shift_index = graph.input("shift_index", 1, "uniform")
        graph.tables["counts"] = [[(-1) & mask], [1]]
        count = graph.node("lookup", (shift_index,), {"table": "counts", "bits": 1})
        shifted = graph.shift(raw, count)
        graph.outputs.update(root=root, shifted=shifted)
    return graph, {
        "raw": raw,
        "products": products,
        "coefficients": coefficients,
        "ranged": ranged,
        "fallback": fallback,
        "root": root,
        "shifted": shifted,
    }


def call_for(source, value):
    return next(call for call in source["forward_calls"] if call["out"] == [value])


def node_for(target, value):
    return next(node for node in target["nodes"] if node["out"] == [value])


def cap_for(*sources):
    return 4 * max(source["resources"]["logical_qubits"] for source in sources)


def assert_result(target, source, schedule, inputs):
    width = source["word_width"]
    mask = (1 << width) - 1
    initial = {
        name: ((1 << (width - 1)) | (17 * (i + 1))) & mask
        for i, name in enumerate(source["outputs"])
    }
    _, trace = evaluate(target, inputs, trace=True)
    expected = {name: trace[value] ^ initial[name] for name, value in target["outputs"].items()}
    got = execute_compact_parallel(target, source, schedule, inputs, initial)
    assert got["values"] == expected
    assert got["all_input_and_workspace_bits_restored"]


@pytest.fixture(scope="module")
def templates(tmp_path_factory):
    result = {}
    for strategy in STRATEGIES:
        directory = tmp_path_factory.mktemp("coefficient_" + strategy)
        graph, ids = coefficient_graph()
        target = graph.as_dict()
        original, _ = compile_graph(target, directory / "generic_source")
        ranges = RangeIntegrationLibrary(
            directory / "range_leaves", target, original, allowed_bits=(3, 5, 6)
        )
        original, _ = compile_range_graph(target, directory / "range_source", ranges)
        replacements = dict.fromkeys(ids["coefficients"], strategy)
        library = CoefficientIntegrationLibrary(
            directory / "new_leaves", target, original, replacements
        )
        source, _ = compile_coefficient_graph(target, directory / "candidate", library)
        result[strategy] = dict(
            target=target,
            original=original,
            source=source,
            library=library,
            ids=ids,
            replacements=replacements,
        )
    return result


@pytest.fixture(scope="module")
def accepted(tmp_path_factory):
    directory = tmp_path_factory.mktemp("coefficient_accepted")
    graph, ids = coefficient_graph(72, 40, accepted=True)
    target = graph.as_dict()
    original, _ = compile_graph(target, directory / "generic")
    for name, cls in (
        ("shift", ShiftIntegrationLibrary),
        ("root", NonRestoringIntegrationLibrary),
        ("range", RangeIntegrationLibrary),
    ):
        library = cls(directory / (name + "_leaves"), target, original)
        original, _ = compile_graph(target, directory / (name + "_source"), library)
    replacements = dict.fromkeys(TOP_COEFFICIENTS, PREFIX_STRATEGY)
    library = CoefficientIntegrationLibrary(
        directory / "new_leaves", target, original, replacements
    )
    source, _ = compile_coefficient_graph(target, directory / "candidate", library)
    return dict(
        target=target,
        original=original,
        source=source,
        library=library,
        ids=ids,
        replacements=replacements,
    )


def mutable_candidate(template, tmp_path):
    target, original, source = [
        copy.deepcopy(template[name]) for name in ("target", "original", "source")
    ]
    path = tmp_path / "mutable_leaves"
    shutil.copytree(resolve_library(source), path)
    source["library"] = source["library_workspace_relative"] = str(path.resolve())
    return target, original, source, path


@pytest.mark.parametrize("strategy", STRATEGIES)
def test_all_native_signed_patterns_full_source_dirty_xor_alias_and_cleanup(templates, strategy):
    item = templates[strategy]
    target, original, source, library = [
        item[name] for name in ("target", "original", "source", "library")
    ]
    for value, coefficient in zip(item["ids"]["products"], item["ids"]["coefficients"]):
        key = call_for(source, value)["leaf"]
        assert key != call_for(original, value)["leaf"]
        entry = library.entries[key]
        assert entry["input_contract"] == {"zero_low_bits": 0}
        assert entry["coefficient_frontier"] == FRONTIER
        assert entry["spec"] == coefficient_leaf_spec(6, 2, coefficient, strategy)
        assert entry["args"] == [list(range(6))]
        assert entry["outs"] == [list(range(6, 12))]
        assert entry["spec"]["integration_lowering"] == INTEGRATION_LOWERING
        base = frontier_leaf_spec(6, 2, coefficient, strategy)
        assert entry["spec"] == dict(base, integration_lowering=INTEGRATION_LOWERING)
    assert library.counts == {"fallback": 3, "coefficient-full-domain": 3}
    schedule = make_compact_schedule(target, source, cap_for(original, source))
    previous = make_compact_schedule(target, original, cap_for(original, source))
    assert schedule["format"] == "compact-clean-xor-capped-wave-schedule-v7"
    for field in (
        "widths",
        "offsets",
        "retained_ssa_qubits",
        "proof_masks",
        "proof_reasons",
        "argument_and_output_copy_cx",
        "baseline_argument_and_output_copy_cx",
    ):
        assert schedule[field] == previous[field]
    for raw in range(64):
        assert_result(target, source, schedule, {"raw": raw, "index": raw & 31})


def test_default_empty_replacements_preserves_every_original_byte(templates, tmp_path):
    item = templates[PREFIX_STRATEGY]
    library = CoefficientIntegrationLibrary(tmp_path / "leaves", item["target"], item["original"])
    source, _ = compile_coefficient_graph(item["target"], tmp_path / "source", library)
    assert library.counts == {"fallback": len(source["forward_calls"])}
    for old, new in zip(item["original"]["forward_calls"], source["forward_calls"]):
        assert old == new
        entry = library.entries[new["leaf"]]
        for name in (new["leaf"] + ".json", entry["gate_file"]):
            assert (library.archive / name).read_bytes() == (library.path / name).read_bytes()


@pytest.mark.parametrize(
    "replacements",
    [
        [],
        "not a map",
        {True: PREFIX_STRATEGY},
        {False: PREFIX_STRATEGY},
        {1.0: PREFIX_STRATEGY},
        {"11": PREFIX_STRATEGY},
        {999: PREFIX_STRATEGY},
        {11: "unknown"},
        {11: True},
        {11: []},
        {11: PREFIX_STRATEGY, -9: PREFIX_STRATEGY, 0: PREFIX_STRATEGY, 17: PREFIX_STRATEGY},
    ],
)
def test_replacement_map_is_typed_actual_and_bounded(templates, tmp_path, replacements):
    item = templates[PREFIX_STRATEGY]
    with pytest.raises(ValueError, match="integer|coefficient|strategy|three"):
        CoefficientIntegrationLibrary(
            tmp_path / "leaves", item["target"], item["original"], replacements
        )


@pytest.mark.parametrize(
    "contract",
    [
        None,
        {},
        [],
        {"zero_low_bits": False},
        {"zero_low_bits": True},
        {"zero_low_bits": 1},
        {"zero_low_bits": -1},
        {"zero_low_bits": 0, "signed_upper_bits": 7},
    ],
)
def test_missing_malformed_or_narrowed_contract_rejected_before_storage(
    templates, tmp_path, contract
):
    item = templates[PREFIX_STRATEGY]
    target, original, source, path = mutable_candidate(item, tmp_path)
    key = call_for(source, item["ids"]["products"][0])["leaf"]
    metadata = path / (key + ".json")
    entry = json.loads(metadata.read_text(encoding="utf-8"))
    if contract is None:
        entry.pop("input_contract")
    else:
        entry["input_contract"] = contract
    metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="coefficient|contract"):
        make_compact_schedule(target, source, cap_for(original, source))
    with pytest.raises(ValueError, match="coefficient|contract"):
        CoefficientIntegrationLibrary(tmp_path / "reload", target, source)


@pytest.mark.parametrize("spec", [None, [], "not a specification", {}])
def test_outer_family_marker_prevents_malformed_spec_from_hiding(templates, tmp_path, spec):
    item = templates[PREFIX_STRATEGY]
    target, original, source, path = mutable_candidate(item, tmp_path)
    key = call_for(source, item["ids"]["products"][0])["leaf"]
    metadata = path / (key + ".json")
    entry = json.loads(metadata.read_text(encoding="utf-8"))
    entry["spec"] = spec
    metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="specification|coefficient|strategy"):
        make_compact_schedule(target, source, cap_for(original, source))
    with pytest.raises(ValueError, match="specification|coefficient|strategy"):
        CoefficientIntegrationLibrary(tmp_path / "reload", target, source)


@pytest.mark.parametrize(
    "remaining",
    ["coefficient_frontier", "integration_lowering", "lowering", "algorithm", "strategy"],
)
def test_remaining_spec_marker_prevents_removed_outer_marker_from_hiding(
    templates, tmp_path, remaining
):
    item = templates[PREFIX_STRATEGY]
    target, original, source, path = mutable_candidate(item, tmp_path)
    key = call_for(source, item["ids"]["products"][0])["leaf"]
    metadata = path / (key + ".json")
    entry = json.loads(metadata.read_text(encoding="utf-8"))
    entry.pop("coefficient_frontier")
    entry["spec"] = {remaining: entry["spec"][remaining]}
    metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="coefficient|marker"):
        make_compact_schedule(target, source, cap_for(original, source))
    with pytest.raises(ValueError, match="coefficient|marker"):
        CoefficientIntegrationLibrary(tmp_path / "reload", target, source)


@pytest.mark.parametrize(
    "corruption",
    [
        "key",
        "coefficient",
        "precision",
        "op",
        "params",
        "input_register",
        "output_register",
        "marker",
    ],
)
def test_scheduler_requires_exact_coefficient_key_spec_and_native_interface(
    templates, tmp_path, corruption
):
    item = templates[PREFIX_STRATEGY]
    target, original, source, path = mutable_candidate(item, tmp_path)
    key = call_for(source, item["ids"]["products"][0])["leaf"]
    metadata = path / (key + ".json")
    entry = json.loads(metadata.read_text(encoding="utf-8"))
    if corruption == "key":
        entry["key"] = "forged"
    elif corruption == "coefficient":
        entry["spec"]["params"]["c"] += 1
    elif corruption == "precision":
        entry["spec"]["fraction_bits"] += 1
    elif corruption == "op":
        entry["op"] = "add"
    elif corruption == "params":
        entry["params"]["c"] += 1
    elif corruption == "input_register":
        entry["args"][0] = entry["args"][0][:-1]
    elif corruption == "output_register":
        entry["outs"][0] = entry["outs"][0][:-1]
    else:
        entry["coefficient_frontier"] = False
    metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="coefficient|specification|key|interface|marker"):
        make_compact_schedule(target, source, cap_for(original, source))


@pytest.mark.parametrize(
    "corruption",
    ["contract", "spec", "gate", "resources", "key", "input_register", "output_register", "marker"],
)
def test_cached_leaf_is_revalidated_on_fresh_get(templates, tmp_path, corruption):
    item = templates[PREFIX_STRATEGY]
    target, original, source, path = mutable_candidate(item, tmp_path)
    key = call_for(source, item["ids"]["products"][0])["leaf"]
    metadata = path / (key + ".json")
    entry = json.loads(metadata.read_text(encoding="utf-8"))
    if corruption == "gate":
        binary = path / entry["gate_file"]
        binary.write_bytes(binary.read_bytes() + b"deliberate corruption")
    elif corruption == "resources":
        entry["resources"]["t_count"] += 7
    elif corruption == "key":
        entry["key"] = "forged"
    elif corruption == "input_register":
        entry["args"][0] = entry["args"][0][:-1]
    elif corruption == "output_register":
        entry["outs"][0] = entry["outs"][0][:-1]
    elif corruption == "contract":
        entry["input_contract"]["zero_low_bits"] = 1
    elif corruption == "marker":
        entry.pop("coefficient_frontier")
    else:
        entry["spec"]["params"]["c"] += 1
    metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(
        ValueError,
        match="cache|SHA|metadata|spec|resource|register|layout|interface|coefficient|marker|contract",
    ):
        library = CoefficientIntegrationLibrary(path, target, original, item["replacements"])
        library.get(node_for(target, item["ids"]["products"][0]))


def test_in_memory_cached_marker_mutation_is_rejected(templates, tmp_path):
    item = templates[PREFIX_STRATEGY]
    library = CoefficientIntegrationLibrary(
        tmp_path / "leaves", item["target"], item["original"], item["replacements"]
    )
    node = node_for(item["target"], item["ids"]["products"][0])
    _, entry = library.get(node)
    entry["coefficient_frontier"] = False
    with pytest.raises(ValueError, match="in-memory|cache|metadata"):
        library.get(node)


def test_already_specialized_source_reload_is_byte_exact(templates, tmp_path):
    item = templates[PREFIX_STRATEGY]
    library = CoefficientIntegrationLibrary(
        tmp_path / "leaves", item["target"], item["source"], item["replacements"]
    )
    source, _ = compile_coefficient_graph(item["target"], tmp_path / "source", library)
    assert [call["leaf"] for call in source["forward_calls"]] == [
        call["leaf"] for call in item["source"]["forward_calls"]
    ]
    schedule = make_compact_schedule(item["target"], source, cap_for(item["source"], source))
    for raw in (0, 1, 31, 32, 63):
        assert_result(item["target"], source, schedule, {"raw": raw, "index": raw & 31})


@pytest.mark.parametrize(
    "mutation", ["input_width", "preparation", "output", "table", "coefficient"]
)
def test_whole_target_mutation_rejected_by_bound_compiler(templates, tmp_path, mutation):
    item = templates[PREFIX_STRATEGY]
    target = copy.deepcopy(item["target"])
    library = CoefficientIntegrationLibrary(tmp_path / "leaves", target, item["original"])
    if mutation == "input_width":
        target["nodes"][0]["params"]["bits"] -= 1
    elif mutation == "preparation":
        target["nodes"][0]["params"]["preparation"] = "uniform"
    elif mutation == "output":
        target["outputs"]["Y"] = item["ids"]["ranged"]
    elif mutation == "table":
        target["tables"]["coefficients"][0][0] = 1
    else:
        node_for(target, item["ids"]["products"][0])["params"]["c"] += 1
    with pytest.raises(ValueError, match="target|immutable|snapshot"):
        compile_coefficient_graph(target, tmp_path / "source", library)


def test_mutated_compiler_table_and_detached_node_are_rejected(templates, tmp_path):
    item = templates[PREFIX_STRATEGY]
    library = CoefficientIntegrationLibrary(tmp_path / "leaves", item["target"], item["original"])
    node = copy.deepcopy(node_for(item["target"], item["ids"]["products"][0]))
    node["params"]["c"] += 1
    with pytest.raises(ValueError, match="immutable|target"):
        library.get(node)
    library.tables["coefficients"][0][0] = 1
    with pytest.raises(ValueError, match="table|target|frozen"):
        library.get(node_for(item["target"], item["ids"]["products"][0]))


def test_detached_external_invocation_cannot_use_forged_location(templates):
    item = templates[PREFIX_STRATEGY]
    value = item["ids"]["products"][0]
    entry = item["library"].entries[call_for(item["source"], value)["leaf"]]
    node = copy.deepcopy(node_for(item["target"], value))
    node["out"] = [10_000]
    for locations in (None, {10_000: item["library"].context.locations[value]}):
        with pytest.raises(ValueError, match="bound|validated|target"):
            validate_coefficient_entry(item["target"], node, entry, locations=locations)


@pytest.mark.parametrize("mutation", ["target", "source", "storage", "format"])
def test_replay_requires_matching_fingerprints_storage_and_v7_format(templates, mutation):
    item = templates[PREFIX_STRATEGY]
    target, source = copy.deepcopy(item["target"]), copy.deepcopy(item["source"])
    schedule = make_compact_schedule(target, source, cap_for(item["original"], source))
    if mutation == "target":
        target["tables"]["coefficients"][0][0] ^= 1
    elif mutation == "source":
        source["forward_calls"][0]["argument_copy_cx"] += 1
    elif mutation == "storage":
        schedule["widths"][item["ids"]["products"][0]] -= 1
    else:
        schedule["format"] = "compact-clean-xor-capped-wave-schedule-v6"
    with pytest.raises(ValueError, match="fingerprint|storage|format|match"):
        execute_compact_parallel(target, source, schedule, {"raw": 1, "index": 0})


def test_gate_sha_checked_during_full_source_replay(templates, tmp_path):
    item = templates[PREFIX_STRATEGY]
    target, original, source, path = mutable_candidate(item, tmp_path)
    schedule = make_compact_schedule(target, source, cap_for(original, source))
    key = call_for(source, item["ids"]["products"][0])["leaf"]
    entry = json.loads((path / (key + ".json")).read_text(encoding="utf-8"))
    binary = path / entry["gate_file"]
    binary.write_bytes(binary.read_bytes() + b"deliberate corruption")
    with pytest.raises(ValueError, match="SHA|hash"):
        execute_compact_parallel(target, source, schedule, {"raw": 1, "index": 0})


def test_native_top_coefficients_preserve_roots_shifts_range_and_32_row_lookup(accepted):
    item = accepted
    library = item["library"]
    for old, new, node in zip(
        item["original"]["forward_calls"],
        item["source"]["forward_calls"],
        [node for node in item["target"]["nodes"] if node["op"] != "input"],
    ):
        if node["op"] == "cmul" and node["params"]["c"] in TOP_COEFFICIENTS:
            continue
        assert old == new
        entry = library.entries[new["leaf"]]
        for name in (new["leaf"] + ".json", entry["gate_file"]):
            assert (library.archive / name).read_bytes() == (library.path / name).read_bytes()
    for name, field, expected in (
        ("root", "unsigned_input_bits", 46),
        ("shifted", "signed_shift_count_bits", 7),
        ("ranged", "signed_operand_bits", [24, 24]),
    ):
        entry = library.entries[call_for(item["source"], item["ids"][name])["leaf"]]
        assert entry["input_contract"] == {field: expected}
    schedule = make_compact_schedule(
        item["target"], item["source"], cap_for(item["original"], item["source"])
    )
    for index, raw in enumerate((0, 1, (1 << 71) - 1, 1 << 71, (1 << 72) - 1)):
        assert_result(
            item["target"],
            item["source"],
            schedule,
            {
                "raw": raw,
                "index": index,
                "radicand": (1 << 45) + index,
                "shift_index": index & 1,
            },
        )


@pytest.mark.parametrize("name", ["root", "shifted", "ranged"])
def test_new_reader_revalidates_all_preserved_typed_guards(accepted, tmp_path, name):
    item = accepted
    target, original, source, path = mutable_candidate(item, tmp_path)
    key = call_for(source, item["ids"][name])["leaf"]
    metadata = path / (key + ".json")
    entry = json.loads(metadata.read_text(encoding="utf-8"))
    field = next(iter(entry["input_contract"]))
    entry["input_contract"][field] = False
    metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="unsigned|signed|shift|operand|width|contract"):
        make_compact_schedule(target, source, cap_for(original, source))
    with pytest.raises(ValueError, match="unsigned|signed|shift|operand|width|contract"):
        CoefficientIntegrationLibrary(tmp_path / "reload", target, source)


@pytest.mark.parametrize("mutation", ["boolean_ssa", "duplicate_output", "forward_reference"])
def test_external_reader_validates_ordered_typed_ssa_before_coefficient_masks(
    templates, tmp_path, mutation
):
    item = templates[PREFIX_STRATEGY]
    target, original, source, _ = mutable_candidate(item, tmp_path)
    value = item["ids"]["products"][0]
    node, call = node_for(target, value), call_for(source, value)
    if mutation == "boolean_ssa":
        node["args"][0] = call["args"][0] = True
    elif mutation == "duplicate_output":
        node_for(target, item["ids"]["products"][1])["out"] = [value]
        call_for(source, item["ids"]["products"][1])["out"] = [value]
    else:
        node["args"][0] = call["args"][0] = item["ids"]["fallback"]
    with pytest.raises(ValueError, match="SSA|producer|duplicate|identifier|integer|boolean"):
        make_compact_schedule(target, source, cap_for(original, source))
