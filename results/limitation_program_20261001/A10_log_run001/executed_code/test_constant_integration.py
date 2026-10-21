"""Guarded constant integration checked against independent signed integers."""

import copy
import json

import pytest

from research.controlled_source_completion.compact_parallel import (
    execute_compact_parallel,
    make_compact_schedule,
)
from research.controlled_source_completion.compiler import compile_graph, resolve_library
from research.controlled_source_completion.ir import Graph
from research.limitation_program_20261001.constant_library import ConstantIntegrationLibrary

COEFFICIENT = 762123384786
INVERSE_LN2 = 1586259972792
WIDTH, FRACTION = 72, 40
MASK = (1 << WIDTH) - 1


def signed_word(raw, width=WIDTH):
    raw &= (1 << width) - 1
    return raw - (1 << width) if raw & (1 << (width - 1)) else raw


def canonical_log_graph(*, offset=FRACTION, coefficient=COEFFICIENT, reverse_guard=False):
    """Construct the formula independently of the site-proof fixture helper."""
    graph = Graph(FRACTION, WIDTH - FRACTION)
    raw = graph.input("x", WIDTH)
    one = graph.const_int(1)
    flag = graph.lt(raw, one)
    guarded = graph.select(flag, raw, one) if reverse_guard else graph.select(flag, one, raw)
    top = graph.node("msb", (guarded,))
    exponent = graph.sub(top, graph.const_int(offset))
    shifted = graph.bits(exponent, -FRACTION, WIDTH, signed=False)
    value = graph.node("cmul", (shifted,), {"c": coefficient})
    graph.outputs = {"Y": value, "alias": value, "exponent": exponent, "guarded": guarded}
    return graph, {"raw": raw, "guarded": guarded, "exponent": exponent,
                   "shifted": shifted, "product": value}


def compile_integration(graph, directory, **options):
    target = graph.as_dict()
    original, _ = compile_graph(target, directory / "original")
    library = ConstantIntegrationLibrary(directory / "new_leaves", target, original, **options)
    source, _ = compile_graph(target, directory / "candidate", library)
    return target, original, source, library


def call_for(source, value):
    return next(call for call in source["forward_calls"] if call["out"] == [value])


def node_for(target, value):
    return next(node for node in target["nodes"] if node["out"] == [value])


def initial_words(source):
    words = [int("a5" * 9, 16), MASK, (1 << 71) | 13, int("39" * 9, 16)]
    return {name: words[index % len(words)] for index, name in enumerate(source["outputs"])}


def assert_graph_result(target, source, schedule, raw, expected):
    initial = initial_words(source)
    got = execute_compact_parallel(target, source, schedule, {"x": raw}, initial)
    assert got["values"] == {
        name: initial[name] ^ (value & MASK) for name, value in expected.items()
    }
    assert got["all_input_and_workspace_bits_restored"]
    return got


def assert_fallback_bytes(original, candidate, library, value):
    old_call, new_call = call_for(original, value), call_for(candidate, value)
    assert old_call["leaf"] == new_call["leaf"]
    key = old_call["leaf"]
    old_library = resolve_library(original)
    entry = json.loads((old_library / (key + ".json")).read_text(encoding="utf-8"))
    for name in (key + ".json", entry["gate_file"]):
        assert (old_library / name).read_bytes() == (library.path / name).read_bytes()


def test_canonical_log_full_graph_every_exponent_boundary_and_cleanup(tmp_path):
    graph, ids = canonical_log_graph()
    target, original, source, library = compile_integration(graph, tmp_path)
    specialized = call_for(source, ids["product"])["leaf"]
    assert specialized != call_for(original, ids["product"])["leaf"]
    entry = library.entries[specialized]
    assert entry["input_contract"] == {"zero_low_bits": 40, "signed_upper_bits": 7}
    assert len(entry["args"][0]) == len(entry["outs"][0]) == WIDTH
    assert len(library.proofs) == 1
    schedule = make_compact_schedule(target, source, original["resources"]["logical_qubits"] * 4)
    patterns = {0, 1, 2, MASK, 1 << 71, (1 << 71) - 1}
    for index in range(71):
        patterns.update({(1 << index) - 1, 1 << index})
    observed_exponents = set()
    for raw in sorted(patterns):
        # Signed comparison clamps zero and every negative word to literal one.
        guarded = max(signed_word(raw), 1)
        exponent = guarded.bit_length() - 1 - FRACTION
        observed_exponents.add(exponent)
        assert -40 <= exponent <= 30
        assert_graph_result(target, source, schedule, raw,
                            {"Y": exponent * COEFFICIENT,
                             "alias": exponent * COEFFICIENT,
                             "exponent": exponent, "guarded": guarded})
    assert observed_exponents == set(range(-40, 31))


@pytest.mark.parametrize("variant", ["offset", "coefficient", "guard"])
def test_nearby_unproved_log_chain_keeps_original_leaf(tmp_path, variant):
    kwargs = {"offset": 41} if variant == "offset" else (
        {"coefficient": COEFFICIENT + 1} if variant == "coefficient"
        else {"reverse_guard": True}
    )
    graph, ids = canonical_log_graph(**kwargs)
    target, original, source, library = compile_integration(graph, tmp_path)
    assert library.proofs == []
    assert_fallback_bytes(original, source, library, ids["product"])
    schedule = make_compact_schedule(target, source, original["resources"]["logical_qubits"] * 4)
    for raw in (0, 1, 1 << 40, (1 << 71) - 1, 1 << 71, MASK):
        guarded = min(signed_word(raw), 1) if variant == "guard" else max(signed_word(raw), 1)
        guarded_raw = guarded & MASK
        exponent = max(0, guarded_raw.bit_length() - 1) - kwargs.get("offset", FRACTION)
        # Left-shift/truncation makes a signed32 upper word, even for an
        # unproved graph. This is the fallback's actual arithmetic contract.
        upper = signed_word(exponent, WIDTH - FRACTION)
        coefficient = kwargs.get("coefficient", COEFFICIENT)
        assert_graph_result(target, source, schedule, raw,
                            {"Y": upper * coefficient, "alias": upper * coefficient,
                             "exponent": exponent, "guarded": guarded})


def exp_graph():
    graph = Graph(FRACTION, WIDTH - FRACTION)
    raw = graph.input("x", WIDTH)
    scaled = graph.node("cmul", (raw,), {"c": INVERSE_LN2})
    quotient = graph.bits(scaled, FRACTION, WIDTH, signed=True)
    shifted = graph.bits(quotient, -FRACTION, WIDTH, signed=False)
    value = graph.node("cmul", (shifted,), {"c": COEFFICIENT})
    graph.outputs = {"Y": value, "quotient": quotient, "scaled": scaled}
    return graph, {"scaled": scaled, "quotient": quotient, "product": value}


def test_exp_same_ln2_coefficient_remains_a_byte_identical_fallback(tmp_path):
    graph, ids = exp_graph()
    target, original, source, library = compile_integration(graph, tmp_path)
    assert library.proofs == []
    assert_fallback_bytes(original, source, library, ids["product"])
    schedule = make_compact_schedule(target, source, original["resources"]["logical_qubits"] * 4)
    for raw in (0, 1, 128 << 40, (1 << 71) - 1, 1 << 71, MASK):
        scaled = (signed_word(raw) * INVERSE_LN2 >> FRACTION) & MASK
        quotient = signed_word(scaled) >> FRACTION
        assert_graph_result(target, source, schedule, raw,
                            {"Y": quotient * COEFFICIENT,
                             "quotient": quotient, "scaled": scaled})


def test_general_ln2_input_is_not_dispatched_by_coefficient_alone(tmp_path):
    graph = Graph(FRACTION, WIDTH - FRACTION)
    raw = graph.input("x", WIDTH)
    value = graph.node("cmul", (raw,), {"c": COEFFICIENT})
    graph.outputs = {"Y": value}
    target, original, source, library = compile_integration(graph, tmp_path)
    assert library.proofs == []
    assert_fallback_bytes(original, source, library, value)
    schedule = make_compact_schedule(target, source, original["resources"]["logical_qubits"] * 4)
    for raw in (0, 2, 1 << 40, 64 << 40, (1 << 71) - 1, 1 << 71, MASK):
        assert_graph_result(target, source, schedule, raw,
                            {"Y": signed_word(raw) * COEFFICIENT >> FRACTION})


def test_general_constant_replacement_handles_unpromised_low_bits_and_sign(tmp_path):
    graph = Graph(FRACTION, WIDTH - FRACTION)
    raw = graph.input("x", WIDTH)
    value = graph.node("cmul", (raw,), {"c": INVERSE_LN2})
    graph.outputs = {"Y": value, "alias": value}
    target, original, source, library = compile_integration(
        graph, tmp_path, general_replacements={INVERSE_LN2: "signed-digit-carry-save"},
    )
    key = call_for(source, value)["leaf"]
    assert key != call_for(original, value)["leaf"]
    assert library.entries[key]["input_contract"] == {"zero_low_bits": 0}
    assert library.proofs == [] and len(library.general_sites) == 1
    schedule = make_compact_schedule(target, source, original["resources"]["logical_qubits"] * 8)
    for raw in (0, 1, 2, (1 << 40) + 3, (1 << 71) - 1, 1 << 71, MASK):
        expected = signed_word(raw) * INVERSE_LN2 >> FRACTION
        assert_graph_result(target, source, schedule, raw, {"Y": expected, "alias": expected})


def test_ln2_cannot_be_forced_through_general_replacement_map(tmp_path):
    graph, _ = canonical_log_graph()
    target = graph.as_dict()
    original, _ = compile_graph(target, tmp_path / "original")
    with pytest.raises(ValueError, match="reserved|ln|special|coefficient"):
        ConstantIntegrationLibrary(
            tmp_path / "new", target, original,
            general_replacements={COEFFICIENT: "signed-digit-carry-save"},
        )


def test_saved_target_mutation_is_rejected_during_compilation(tmp_path):
    graph, _ = canonical_log_graph()
    target = graph.as_dict()
    original, _ = compile_graph(target, tmp_path / "original")
    library = ConstantIntegrationLibrary(tmp_path / "new", target, original)
    constant_one = next(node for node in target["nodes"]
                        if node["op"] == "const" and node["params"]["value"] == 1)
    constant_one["params"]["value"] = 2
    with pytest.raises(ValueError, match="snapshot|same|node|semantic|target|match"):
        compile_graph(target, tmp_path / "mutated", library)


def test_constructor_rejects_a_different_target_with_the_same_bindings(tmp_path):
    graph, _ = canonical_log_graph()
    target = graph.as_dict()
    original, _ = compile_graph(target, tmp_path / "original")
    different_target = copy.deepcopy(target)
    fraction = next(node for node in different_target["nodes"]
                    if node["op"] == "const" and node["params"]["value"] == FRACTION)
    fraction["params"]["value"] = FRACTION + 1
    with pytest.raises(ValueError, match="source|target|semantic|match|parameter"):
        ConstantIntegrationLibrary(tmp_path / "new", different_target, original)


def test_foreign_output_id_and_mutated_coefficient_are_rejected(tmp_path):
    graph, ids = canonical_log_graph()
    target = graph.as_dict()
    original, _ = compile_graph(target, tmp_path / "original")
    library = ConstantIntegrationLibrary(tmp_path / "new", target, original)
    node = node_for(target, ids["product"])
    foreign = copy.deepcopy(node)
    foreign["out"] = [123456]
    with pytest.raises(ValueError, match="node|graph|snapshot|match|output"):
        library.get(foreign)
    changed = copy.deepcopy(node)
    changed["params"]["c"] += 1
    with pytest.raises(ValueError, match="node|graph|snapshot|match|semantic"):
        library.get(changed)


@pytest.mark.parametrize("contract", [
    {"zero_low_bits": 40, "signed_upper_bits": 7},
    {"zero_low_bits": 40, "signed_upper_bits": 8},
    {"signed_upper_bits": 7},
])
def test_exp_leaf_cannot_claim_the_log_signed7_contract(tmp_path, contract):
    graph, ids = exp_graph()
    target, original, source, library = compile_integration(graph, tmp_path)
    key = call_for(source, ids["product"])["leaf"]
    metadata = library.path / (key + ".json")
    entry = json.loads(metadata.read_text(encoding="utf-8"))
    entry["input_contract"] = contract
    metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="signed|contract|proof"):
        make_compact_schedule(target, source, original["resources"]["logical_qubits"] * 4)


@pytest.mark.parametrize("corruption", ["gate", "contract"])
def test_specialized_cache_corruption_is_rejected(tmp_path, corruption):
    graph, ids = canonical_log_graph()
    target, original, source, library = compile_integration(graph, tmp_path)
    node = node_for(target, ids["product"])
    key = call_for(source, ids["product"])["leaf"]
    metadata = library.path / (key + ".json")
    entry = json.loads(metadata.read_text(encoding="utf-8"))
    if corruption == "gate":
        binary = library.path / entry["gate_file"]
        binary.write_bytes(binary.read_bytes() + b"deliberate cache corruption")
    else:
        entry["input_contract"] = {"zero_low_bits": 40, "signed_upper_bits": 8}
        metadata.write_text(json.dumps(entry), encoding="utf-8")
    with pytest.raises(ValueError, match="cache|hash|metadata|contract|spec"):
        cached = ConstantIntegrationLibrary(library.path, target, original)
        cached.get(node)
