"""Both signed operand guards, complete native XOR interfaces and fixed fallbacks."""

import copy
import json
import math
from pathlib import Path
import shutil

import pytest

from research.controlled_source_completion.compact_parallel_v6 import (
    execute_compact_parallel,
    make_compact_schedule,
)
from research.controlled_source_completion.compiler import compile_graph, resolve_library
from research.controlled_source_completion.ir import Graph, evaluate
from research.limitation_program_20261001.interval_bounds import bound_graph
from research.limitation_program_20261001.nonrestoring_library import NonRestoringIntegrationLibrary
from research.limitation_program_20261001.prove_range_input import (
    INTEGRATION_LOWERING,
    prove_range_site,
    select_range_site,
    signed_interval_bits,
)
from research.limitation_program_20261001.range_library import (
    RangeIntegrationLibrary,
    compile_range_graph,
)
from research.limitation_program_20261001.shift_library import ShiftIntegrationLibrary

ROOT = Path(__file__).resolve().parents[2]


def range_graph(*, width=7, fraction=2, preparation="uniform", lookup=True, accepted=False):
    graph = Graph(fraction, width - fraction)
    mask = (1 << width) - 1
    if lookup:
        index = graph.input("index", 3, preparation)
        left_values = (-4, -3, -1, 0, 1, 2, 3, 4)
        right_values = (-1, 0, 1, -1, 1, 0, -1, 1)
        graph.tables["operands"] = [[a & mask, b & mask] for a, b in zip(left_values, right_values)]
        left, right = graph.node("lookup", (index,), {"table": "operands", "bits": 3}, 2)
    else:
        left = graph.input("left", 3, preparation)
        right = graph.input("right", 1, preparation)
    product = graph.mul(left, right)
    reverse = graph.mul(right, left)
    square = graph.mul(left, left)
    total = graph.add(product, square)
    graph.outputs = {
        "Y": product,
        "reverse": reverse,
        "square": square,
        "alias": product,
        "total": total,
        "left": left,
        "right": right,
    }
    root = shifted = None
    if accepted:
        raw = graph.input("radicand", 46, "uniform")
        root = graph.node("sqrt", (raw,))
        data = graph.input("data", width, "provided")
        shift_index = graph.input("shift_index", 1, "uniform")
        graph.tables["counts"] = [[(-1) & mask], [1]]
        count = graph.node("lookup", (shift_index,), {"table": "counts", "bits": 1})
        shifted = graph.shift(data, count)
        graph.outputs.update(root=root, shifted=shifted)
    return graph, {
        "left": left,
        "right": right,
        "product": product,
        "reverse": reverse,
        "square": square,
        "total": total,
        "root": root,
        "shifted": shifted,
    }


def call_for(source, value):
    return next(call for call in source["forward_calls"] if call["out"] == [value])


def node_for(target, value):
    return next(node for node in target["nodes"] if node["out"] == [value])


def cap_for(original, source):
    return max(original["resources"]["logical_qubits"], source["resources"]["logical_qubits"])


def initial_words(source):
    mask = (1 << source["word_width"]) - 1
    return {
        name: ((1 << (source["word_width"] - 1)) | (17 * (i + 1))) & mask
        for i, name in enumerate(source["outputs"])
    }


def assert_result(target, source, schedule, inputs):
    initial = initial_words(source)
    _, trace = evaluate(target, inputs, trace=True)
    expected = {name: trace[value] ^ initial[name] for name, value in target["outputs"].items()}
    got = execute_compact_parallel(target, source, schedule, inputs, initial)
    assert got["values"] == expected
    assert got["all_input_and_workspace_bits_restored"]


@pytest.fixture(scope="module")
def templates(tmp_path_factory):
    result = {}
    for name, kwargs in (
        ("lookup", {}),
        ("uniform", {"lookup": False}),
        ("provided", {"lookup": False, "preparation": "provided"}),
        ("accepted", {"width": 72, "fraction": 40, "accepted": True}),
    ):
        directory = tmp_path_factory.mktemp("range_" + name)
        graph, ids = range_graph(**kwargs)
        target = graph.as_dict()
        original, _ = compile_graph(target, directory / "original")
        if name == "accepted":
            shifts = ShiftIntegrationLibrary(directory / "shift_leaves", target, original)
            original, _ = compile_graph(target, directory / "shift_source", shifts)
            roots = NonRestoringIntegrationLibrary(directory / "root_leaves", target, original)
            original, _ = compile_graph(target, directory / "root_source", roots)
        bins = (24, 40, 72) if name == "accepted" else (3, 5, 7)
        library = RangeIntegrationLibrary(
            directory / "range_leaves", target, original, allowed_bits=bins
        )
        source, _ = compile_range_graph(target, directory / "candidate", library)
        result[name] = dict(
            target=target, original=original, source=source, library=library, ids=ids, bins=bins
        )
    return result


def mutable_candidate(template, tmp_path):
    target, original, source = [
        copy.deepcopy(template[name]) for name in ("target", "original", "source")
    ]
    path = tmp_path / "mutable_leaves"
    shutil.copytree(resolve_library(source), path)
    source["library"] = source["library_workspace_relative"] = str(path.resolve())
    return target, original, source, path


def test_ordered_lookup_pairs_keep_native_interfaces_dirty_outputs_aliases_and_inverse(templates):
    item = templates["lookup"]
    target, original, source, library = [
        item[name] for name in ("target", "original", "source", "library")
    ]
    for output, pair in (("product", [5, 3]), ("reverse", [3, 5]), ("square", [5, 5])):
        key = call_for(source, item["ids"][output])["leaf"]
        assert key != call_for(original, item["ids"][output])["leaf"]
        entry = library.entries[key]
        assert entry["input_contract"] == {"signed_operand_bits": pair}
        assert entry["spec"]["integration_lowering"] == INTEGRATION_LOWERING
        assert entry["args"] == [list(range(7)), list(range(7, 14))]
        assert entry["outs"] == [list(range(14, 21))]
    schedule = make_compact_schedule(target, source, cap_for(original, source))
    assert schedule["format"] == "compact-clean-xor-capped-wave-schedule-v6"
    previous = make_compact_schedule(target, original, cap_for(original, source))
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
    for index in range(8):
        assert_result(target, source, schedule, {"index": index})


def test_unsigned_positive_input_requires_extra_signed_bit_and_both_operands_are_proved(templates):
    item = templates["uniform"]
    key = call_for(item["source"], item["ids"]["product"])["leaf"]
    assert item["library"].entries[key]["input_contract"] == {"signed_operand_bits": [5, 3]}
    schedule = make_compact_schedule(
        item["target"], item["source"], cap_for(item["original"], item["source"])
    )
    for left in range(8):
        for right in range(2):
            assert_result(item["target"], item["source"], schedule, {"left": left, "right": right})


def test_provided_input_law_falls_back_and_preserves_all_original_bytes(templates):
    item = templates["provided"]
    assert item["library"].counts == {"fallback": len(item["source"]["forward_calls"])}
    for old, new in zip(item["original"]["forward_calls"], item["source"]["forward_calls"]):
        assert old == new
        entry = item["library"].entries[new["leaf"]]
        for filename in (new["leaf"] + ".json", entry["gate_file"]):
            assert (item["library"].archive / filename).read_bytes() == (
                item["library"].path / filename
            ).read_bytes()


def test_eligible_pair_filter_keeps_exact_generic_bytes_for_excluded_pair(templates, tmp_path):
    item = templates["lookup"]
    library = RangeIntegrationLibrary(
        tmp_path / "filtered",
        item["target"],
        item["original"],
        allowed_bits=item["bins"],
        eligible_pairs=[(5, 3)],
    )
    source, _ = compile_range_graph(item["target"], tmp_path / "filtered_source", library)
    assert (
        call_for(source, item["ids"]["product"])["leaf"]
        != call_for(item["original"], item["ids"]["product"])["leaf"]
    )
    for value in (item["ids"]["reverse"], item["ids"]["square"]):
        old = call_for(item["original"], value)["leaf"]
        assert call_for(source, value)["leaf"] == old
        assert (library.path / (old + ".npy")).read_bytes() == (
            library.archive / (old + ".npy")
        ).read_bytes()
    schedule = make_compact_schedule(item["target"], source, cap_for(item["original"], source))
    for index in range(8):
        assert_result(item["target"], source, schedule, {"index": index})


def test_forged_range_contract_cannot_specialize_provided_full_signed_inputs(templates, tmp_path):
    item = templates["provided"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    key = call_for(source, item["ids"]["product"])["leaf"]
    metadata = path / (key + ".json")
    entry = json.loads(metadata.read_text(encoding="utf-8"))
    entry["input_contract"] = {"signed_operand_bits": [5, 3]}
    metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="operand|contract|proved"):
        make_compact_schedule(target, source, cap_for(original, source))
    with pytest.raises(ValueError, match="operand|contract|proved"):
        RangeIntegrationLibrary(tmp_path / "reload", target, source, allowed_bits=item["bins"])


@pytest.mark.parametrize(
    "contract",
    [
        None,
        {},
        [],
        {"signed_operand_bits": False},
        {"signed_operand_bits": [True, 3]},
        {"signed_operand_bits": [5, False]},
        {"signed_operand_bits": [0, 3]},
        {"signed_operand_bits": [8, 3]},
        {"signed_operand_bits": [3, 3]},
        {"signed_operand_bits": [5, 1]},
        {"signed_operand_bits": [5]},
        {"signed_operand_bits": [5, 3, 7]},
        {"signed_operand_bits": [5, 3], "unsigned_input_bits": 3},
    ],
)
def test_missing_malformed_or_one_unproved_operand_contract_is_rejected(
    templates, tmp_path, contract
):
    item = templates["lookup"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    key = call_for(source, item["ids"]["product"])["leaf"]
    metadata = path / (key + ".json")
    entry = json.loads(metadata.read_text(encoding="utf-8"))
    if contract is None:
        entry.pop("input_contract")
    else:
        entry["input_contract"] = contract
    metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="signed|operand|contract|width|proved"):
        make_compact_schedule(target, source, cap_for(original, source))
    with pytest.raises(ValueError, match="signed|operand|contract|width|proved"):
        RangeIntegrationLibrary(tmp_path / "reload", target, source, allowed_bits=item["bins"])


@pytest.mark.parametrize("spec", [None, [], "not a specification", {}])
def test_outer_range_promise_cannot_hide_in_malformed_spec(templates, tmp_path, spec):
    item = templates["lookup"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    key = call_for(source, item["ids"]["product"])["leaf"]
    metadata = path / (key + ".json")
    entry = json.loads(metadata.read_text(encoding="utf-8"))
    entry["spec"] = spec
    metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="signed|multiplier|specification"):
        make_compact_schedule(target, source, cap_for(original, source))
    with pytest.raises(ValueError, match="signed|multiplier|specification"):
        RangeIntegrationLibrary(tmp_path / "reload", target, source, allowed_bits=item["bins"])


@pytest.mark.parametrize(
    "remaining",
    ["algorithm", "active_operand_bits", "lowering", "integration_lowering", "input_contract"],
)
def test_any_remaining_specialized_marker_prevents_hiding_a_removed_outer_promise(
    templates, tmp_path, remaining
):
    item = templates["lookup"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    key = call_for(source, item["ids"]["product"])["leaf"]
    metadata = path / (key + ".json")
    entry = json.loads(metadata.read_text(encoding="utf-8"))
    entry.pop("input_contract")
    entry["spec"] = {remaining: entry["spec"][remaining]}
    metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="signed|operand|contract"):
        make_compact_schedule(target, source, cap_for(original, source))
    with pytest.raises(ValueError, match="signed|operand|contract"):
        RangeIntegrationLibrary(tmp_path / "reload", target, source, allowed_bits=item["bins"])


@pytest.mark.parametrize("corruption", ["key", "params", "op", "input_register", "output_register"])
def test_schedule_requires_canonical_range_spec_key_operation_and_native_interface(
    templates, tmp_path, corruption
):
    item = templates["lookup"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    key = call_for(source, item["ids"]["product"])["leaf"]
    metadata = path / (key + ".json")
    entry = json.loads(metadata.read_text(encoding="utf-8"))
    if corruption == "key":
        entry["key"] = "forged"
    elif corruption == "params":
        entry["spec"]["fraction_bits"] += 1
    elif corruption == "op":
        entry["op"] = "add"
    elif corruption == "input_register":
        entry["args"][1] = entry["args"][1][:-1]
    else:
        entry["outs"][0] = entry["outs"][0][:-1]
    metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="multiplier|specification|key|interface"):
        make_compact_schedule(target, source, cap_for(original, source))


@pytest.mark.parametrize(
    "corruption",
    ["contract", "spec", "gate", "resources", "key", "input_register", "output_register"],
)
def test_cached_specialized_leaf_is_fully_revalidated_on_fresh_get(templates, tmp_path, corruption):
    item = templates["lookup"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    key = call_for(source, item["ids"]["product"])["leaf"]
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
        entry["input_contract"]["signed_operand_bits"][0] = 3
    else:
        entry["spec"]["active_operand_bits"][0] = 3
    metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(
        ValueError, match="cache|SHA|metadata|spec|resource|register|layout|interface"
    ):
        library = RangeIntegrationLibrary(path, target, original, allowed_bits=item["bins"])
        library.get(node_for(target, item["ids"]["product"]))


def test_in_memory_cached_promise_mutation_is_rejected(templates, tmp_path):
    item = templates["lookup"]
    library = RangeIntegrationLibrary(
        tmp_path / "cache", item["target"], item["original"], allowed_bits=item["bins"]
    )
    node = node_for(item["target"], item["ids"]["product"])
    _, entry = library.get(node)
    entry["input_contract"]["signed_operand_bits"][1] = 1
    with pytest.raises(ValueError, match="in-memory|cache|metadata"):
        library.get(node)


def test_generated_specialization_reload_and_already_specialized_source_are_exact(
    templates, tmp_path
):
    item = templates["lookup"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    library = RangeIntegrationLibrary(path, target, original, allowed_bits=item["bins"])
    for name in ("product", "reverse", "square"):
        assert (
            library.get(node_for(target, item["ids"][name]))[0]
            == call_for(source, item["ids"][name])["leaf"]
        )
    library = RangeIntegrationLibrary(
        tmp_path / "second", target, source, allowed_bits=item["bins"]
    )
    second, _ = compile_range_graph(target, tmp_path / "second_source", library)
    assert [c["leaf"] for c in second["forward_calls"]] == [
        c["leaf"] for c in source["forward_calls"]
    ]
    schedule = make_compact_schedule(target, second, cap_for(original, second))
    for index in range(8):
        assert_result(target, second, schedule, {"index": index})


@pytest.mark.parametrize("mutation", ["input_width", "preparation", "output", "table"])
def test_whole_target_mutation_is_rejected_by_bound_compiler(templates, tmp_path, mutation):
    item = templates["lookup"]
    target = copy.deepcopy(item["target"])
    library = RangeIntegrationLibrary(
        tmp_path / "bound", target, item["original"], allowed_bits=item["bins"]
    )
    if mutation == "input_width":
        target["nodes"][0]["params"]["bits"] = 4
    elif mutation == "preparation":
        target["nodes"][0]["params"]["preparation"] = "provided"
    elif mutation == "output":
        target["outputs"]["Y"] = item["ids"]["square"]
    else:
        target["tables"]["operands"][0][0] = 63
    with pytest.raises(ValueError, match="target|immutable|snapshot"):
        compile_range_graph(target, tmp_path / "mutated", library)


def test_mutated_compiler_table_and_detached_requested_node_are_rejected(templates, tmp_path):
    item = templates["lookup"]
    library = RangeIntegrationLibrary(
        tmp_path / "bound", item["target"], item["original"], allowed_bits=item["bins"]
    )
    node = copy.deepcopy(node_for(item["target"], item["ids"]["product"]))
    node["args"].reverse()
    with pytest.raises(ValueError, match="immutable|target"):
        library.get(node)
    library.tables["operands"][0][0] = 63
    with pytest.raises(ValueError, match="table|target|frozen"):
        library.get(node_for(item["target"], item["ids"]["product"]))


def test_detached_node_cannot_be_proved_even_with_forged_constant_time_location(templates):
    item = templates["lookup"]
    node = copy.deepcopy(node_for(item["target"], item["ids"]["product"]))
    node["out"] = [10_000]
    for locations in (None, {10_000: item["library"].context.locations[item["ids"]["product"]]}):
        with pytest.raises(ValueError, match="bound|validated|target"):
            prove_range_site(
                item["target"], node, item["library"].bounds, 5, 3, locations=locations
            )


@pytest.mark.parametrize("mutation", ["boolean_ssa", "duplicate_output", "forward_reference"])
def test_external_reader_validates_ordered_typed_ssa_before_multiplier_storage_masks(
    templates, tmp_path, mutation
):
    item = templates["lookup"]
    target, original, source, _ = mutable_candidate(item, tmp_path)
    node, call = node_for(target, item["ids"]["product"]), call_for(source, item["ids"]["product"])
    if mutation == "boolean_ssa":
        node["args"][0] = call["args"][0] = True
    elif mutation == "duplicate_output":
        node_for(target, item["ids"]["total"])["out"] = [item["ids"]["product"]]
        call_for(source, item["ids"]["total"])["out"] = [item["ids"]["product"]]
    else:
        node["args"][0] = call["args"][0] = item["ids"]["total"]
    with pytest.raises(ValueError, match="SSA|producer|duplicate|identifier|integer|boolean"):
        make_compact_schedule(target, source, cap_for(original, source))


@pytest.mark.parametrize("mutation", ["target", "source", "storage", "format"])
def test_replay_requires_matching_fingerprints_storage_and_v6_format(templates, mutation):
    item = templates["lookup"]
    target, source = copy.deepcopy(item["target"]), copy.deepcopy(item["source"])
    schedule = make_compact_schedule(target, source, cap_for(item["original"], source))
    if mutation == "target":
        target["tables"]["operands"][0][0] ^= 1
    elif mutation == "source":
        source["forward_calls"][0]["argument_copy_cx"] += 1
    elif mutation == "storage":
        schedule["widths"][item["ids"]["product"]] -= 1
    else:
        schedule["format"] = "unknown"
    with pytest.raises(ValueError, match="fingerprint|storage|format|match"):
        execute_compact_parallel(target, source, schedule, {"index": 0})


def test_gate_sha_is_checked_when_replaying_compiled_full_source(templates, tmp_path):
    item = templates["lookup"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    schedule = make_compact_schedule(target, source, cap_for(original, source))
    key = call_for(source, item["ids"]["product"])["leaf"]
    entry = json.loads((path / (key + ".json")).read_text(encoding="utf-8"))
    binary = path / entry["gate_file"]
    binary.write_bytes(binary.read_bytes() + b"deliberate corruption")
    with pytest.raises(ValueError, match="SHA|hash"):
        execute_compact_parallel(target, source, schedule, {"index": 0})


def test_adopted_nonrestoring_roots_signed7_shifts_and_lookup_bytes_are_preserved(templates):
    item = templates["accepted"]
    library = item["library"]
    for old, new, node in zip(
        item["original"]["forward_calls"],
        item["source"]["forward_calls"],
        [n for n in item["target"]["nodes"] if n["op"] != "input"],
    ):
        if node["op"] == "mul":
            continue
        assert old == new
        entry = library.entries[new["leaf"]]
        for filename in (new["leaf"] + ".json", entry["gate_file"]):
            assert (library.archive / filename).read_bytes() == (
                library.path / filename
            ).read_bytes()
    root = library.entries[call_for(item["source"], item["ids"]["root"])["leaf"]]
    shift = library.entries[call_for(item["source"], item["ids"]["shifted"])["leaf"]]
    assert root["input_contract"] == {"unsigned_input_bits": 46}
    assert shift["input_contract"] == {"signed_shift_count_bits": 7}
    schedule = make_compact_schedule(
        item["target"], item["source"], cap_for(item["original"], item["source"])
    )
    for index in (0, 2, 7):
        inputs = {
            "index": index,
            "radicand": (1 << 45) + index,
            "data": (1 << 71) | 13,
            "shift_index": index & 1,
        }
        assert_result(item["target"], item["source"], schedule, inputs)
        assert math.isqrt(inputs["radicand"] << 40) > 0


@pytest.mark.parametrize("contract_name", ["root", "shifted"])
def test_new_reader_revalidates_preserved_root_and_shift_promises(
    templates, tmp_path, contract_name
):
    item = templates["accepted"]
    target, original, source, path = mutable_candidate(item, tmp_path)
    key = call_for(source, item["ids"][contract_name])["leaf"]
    metadata = path / (key + ".json")
    entry = json.loads(metadata.read_text(encoding="utf-8"))
    field = next(iter(entry["input_contract"]))
    entry["input_contract"][field] = False
    metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="unsigned|signed|shift|width|contract"):
        make_compact_schedule(target, source, cap_for(original, source))
    with pytest.raises(ValueError, match="unsigned|signed|shift|width|contract"):
        RangeIntegrationLibrary(tmp_path / "reload", target, source)


@pytest.mark.parametrize("power", [0, 1, 23, 24, 38, 39, 40, 70])
def test_positive_signed_boundaries_cannot_be_classified_as_unsigned_width(power):
    assert signed_interval_bits(1 << power, 1 << power, 72) == power + 2
    assert signed_interval_bits(-(1 << power), -(1 << power), 72) == power + 1


@pytest.mark.parametrize("case", ["B4x12", "B8x52"])
def test_actual_accepted_sources_prove_only_complete_minimum_bin_operand_pairs(case):
    directory = ROOT / "results/limitation_program_20261001/A11_nonrestoring_run001" / case
    target = json.loads((directory / "target.json").read_text(encoding="utf-8"))
    bounds, _ = bound_graph(target)
    locations = {
        value: index for index, node in enumerate(target["nodes"]) for value in node["out"]
    }
    counts = {}
    total = 0
    for node in target["nodes"]:
        proof = select_range_site(target, node, bounds, (24, 40, 72), locations=locations)
        if proof is not None:
            total += 1
            pair = tuple(proof["signed_operand_bits"])
            counts[pair] = counts.get(pair, 0) + 1
            assert proof["both_operand_guards_proved"]
            for (low, high), bits in zip(proof["input_bounds"], pair):
                assert -(1 << (bits - 1)) <= low <= high < 1 << (bits - 1)
    assert total == (527 if case == "B4x12" else 4451)
    assert counts[(40, 40)] == 7
    assert counts[(24, 72)] == (190 if case == "B4x12" else 1662)
    assert counts[(72, 24)] == 2
    assert counts[(40, 72)] == (238 if case == "B4x12" else 2078)
    assert counts[(72, 40)] == (90 if case == "B4x12" else 702)
