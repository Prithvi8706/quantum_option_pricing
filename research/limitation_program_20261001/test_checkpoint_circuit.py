"""Adversarial allocations and exhaustive dirty-output emitted-gate fixtures."""

from copy import deepcopy

import pytest

from research.controlled_priority_completion.parallel_source import entries
from research.controlled_source_completion.compact_parallel_v7 import _storage
from research.controlled_source_completion.compiler import compile_graph
from research.controlled_source_completion.ir import Graph, evaluate
from research.limitation_program_20261001.checkpoint_circuit import (
    emit_checkpoint_schedule,
    fingerprint,
    replay_checkpoint,
    validate_allocations,
)


def _fixture_scope(target, source):
    metadata = entries(source)
    storage = _storage(target, source, metadata)
    widths = storage["widths"]
    scope = {
        "word_width": source["word_width"],
        "widths": widths,
        "proof_masks": storage["proof_masks"],
        "source_fingerprint": fingerprint(source),
        "target_fingerprint": fingerprint(target),
        "groups": [],
        "inputs": [],
        "outputs": [],
    }
    cursor, producers = 0, {}
    for node in source["inputs"]:
        value = node["out"][0]
        scope["inputs"].append(
            {
                "id": value,
                "name": node["params"]["name"],
                "bits": node["params"]["bits"],
                "width": widths[value],
                "offset": cursor,
            }
        )
        cursor += widths[value]
    for name, value in source["outputs"].items():
        scope["outputs"].append({"name": name, "value": value, "offset": cursor})
        cursor += source["word_width"]
    scope["fixed_floor"] = cursor
    for index, call in enumerate(source["forward_calls"]):
        out_widths = [widths[v] for v in call["out"]]
        entry = metadata[call["leaf"]]
        scope["groups"].append(
            {
                "id": index,
                "call_index": index,
                "args": call["args"],
                "out": call["out"],
                "out_widths": out_widths,
                "width": sum(out_widths),
                "private": entry["resources"]["qubits"] - sum(out_widths),
                "preds": sorted({producers[a] for a in call["args"] if a in producers}),
                "leaf": call["leaf"],
            }
        )
        producers.update({v: index for v in call["out"]})
    return scope


def _retain_all(scope):
    cursor, stored, moves = scope["fixed_floor"], {}, []
    for group in scope["groups"]:
        stored[group["id"]] = [{"offset": cursor, "width": group["width"]}]
        cursor += group["width"]
    cap = cursor + max((g["private"] for g in scope["groups"]), default=0)
    for group in scope["groups"]:
        moves.append(
            {
                "kind": "compute",
                "group": group["id"],
                "storage": stored[group["id"]],
                "private_storage": [{"offset": cursor, "width": group["private"]}]
                if group["private"]
                else [],
            }
        )
    for output in scope["outputs"]:
        moves.append(
            {"kind": "copy_output", "value": output["value"], "outputname": output["name"]}
        )
    for group in reversed(scope["groups"]):
        moves.append(
            {
                "kind": "erase",
                "group": group["id"],
                "storage": stored[group["id"]],
                "private_storage": [{"offset": cursor, "width": group["private"]}]
                if group["private"]
                else [],
            }
        )
    return {"cap": cap, "heuristic": "retain-all-fixture", "moves": moves}


def _small_graph():
    graph = Graph(f=2, integer_bits=2)
    raw = graph.input("raw", 2)
    square = graph.mul(raw, raw)
    value = graph.add(square, graph.const_int(3))
    graph.outputs = {"value": value, "alias": value}
    return graph.as_dict()


@pytest.fixture
def synthetic():
    # One atomic two-output producer and its repeated-argument child.
    scope = {
        "word_width": 4,
        "fixed_floor": 10,
        "widths": [2, 3, 3, 4],
        "inputs": [{"id": 0, "name": "u", "bits": 2, "width": 2, "offset": 0}],
        "outputs": [
            {"name": "left", "value": 1, "offset": 2},
            {"name": "right", "value": 3, "offset": 6},
        ],
        "groups": [
            {
                "id": 0,
                "args": [0],
                "out": [1, 2],
                "out_widths": [3, 3],
                "width": 6,
                "private": 2,
                "preds": [],
            },
            {
                "id": 1,
                "args": [1, 1],
                "out": [3],
                "out_widths": [4],
                "width": 4,
                "private": 3,
                "preds": [0],
            },
        ],
    }
    return scope, _retain_all(scope)


def test_independent_live_accounting_and_atomic_lookup(synthetic):
    scope, plan = synthetic
    observed = validate_allocations(scope, plan)
    assert observed["complete_checkpoint_cleanup"]
    assert observed["peak_live_qubits"] == 23
    assert observed["logical_qubits"] == 23


@pytest.mark.parametrize(
    "mutation",
    [
        "missing_predecessor",
        "dirty_overwrite",
        "private_alias",
        "lost_atomic_output",
        "erase_wrong_span",
        "output_wrong_value",
        "duplicate_output_copy",
        "missing_output_copy",
        "unclean_finish",
        "infeasible_cap",
        "overlapping_span",
        "missing_private",
        "wrong_pred_declaration",
        "duplicate_producer",
        "fixed_floor_collision",
    ],
)
def test_adversarial_allocation_rejected(synthetic, mutation):
    scope, plan = deepcopy(synthetic)
    moves = plan["moves"]
    if mutation == "missing_predecessor":
        moves[0], moves[1] = moves[1], moves[0]
    elif mutation == "dirty_overwrite":
        moves.insert(1, deepcopy(moves[0]))
    elif mutation == "private_alias":
        moves[1]["private_storage"] = [{"offset": 10, "width": 3}]
    elif mutation == "lost_atomic_output":
        scope["groups"][0]["out_widths"] = [3]
    elif mutation == "erase_wrong_span":
        moves[-2]["storage"] = [{"offset": 15, "width": 4}]
    elif mutation == "output_wrong_value":
        moves[2]["value"] = 2
    elif mutation == "duplicate_output_copy":
        moves.insert(3, deepcopy(moves[2]))
    elif mutation == "missing_output_copy":
        del moves[2]
    elif mutation == "unclean_finish":
        del moves[-1]
    elif mutation == "infeasible_cap":
        plan["cap"] -= 1
    elif mutation == "overlapping_span":
        moves[0]["storage"] = [{"offset": 10, "width": 3}, {"offset": 10, "width": 3}]
    elif mutation == "missing_private":
        moves[0]["private_storage"] = []
    elif mutation == "wrong_pred_declaration":
        scope["groups"][1]["preds"] = []
    elif mutation == "duplicate_producer":
        scope["groups"][1]["out"] = [1]
    elif mutation == "fixed_floor_collision":
        scope["outputs"][0]["offset"] = 0
    with pytest.raises((ValueError, KeyError)):
        validate_allocations(scope, plan)


def test_fragmented_native_private_and_producer_allocation(synthetic):
    scope, plan = deepcopy(synthetic)
    for move in plan["moves"]:
        if move["kind"] != "copy_output" and move["group"] == 0:
            move["storage"] = [{"offset": 10, "width": 2}, {"offset": 12, "width": 4}]
    assert validate_allocations(scope, plan)["complete_checkpoint_cleanup"]


def test_actual_repeated_args_aliases_and_all_dirty_output_patterns(tmp_path):
    target = _small_graph()
    source, _ = compile_graph(target, tmp_path / "source")
    scope = _fixture_scope(target, source)
    plan = _retain_all(scope)
    emitted = emit_checkpoint_schedule(target, source, scope, plan)
    assert emitted["resources"]["t_count"] == 7 * emitted["resources"]["ccx"]
    assert emitted["argument_copy_depth"] >= 8  # repeated source controls in both directions
    for raw in range(4):
        _, trace = evaluate(target, {"raw": raw}, trace=True)
        for dirty in range(16):
            initial = {"value": dirty, "alias": dirty ^ 15}
            result = replay_checkpoint(
                target, source, scope, emitted, {"raw": raw}, initial, expected_trace=trace
            )
            assert result["all_input_and_workspace_bits_restored"]
            assert result["values"] == {
                name: initial[name] ^ trace[value] for name, value in source["outputs"].items()
            }


def test_actual_atomic_multioutput_lookup_with_high_output_scratch(tmp_path):
    graph = Graph(f=2, integer_bits=2)
    address = graph.input("address", 1)
    graph.tables["tiny"] = [[1, 3], [2, 5]]
    left, right = graph.node("lookup", (address,), {"table": "tiny", "bits": 1}, nout=2)
    graph.outputs = {"left": left, "right": right}
    target = graph.as_dict()
    source, _ = compile_graph(target, tmp_path / "source")
    scope = _fixture_scope(target, source)
    plan = _retain_all(scope)
    emitted = emit_checkpoint_schedule(target, source, scope, plan)
    entry = next(iter(entries(source).values()))
    assert scope["groups"][0]["private"] == entry["resources"]["qubits"] - 5
    for address_raw in range(2):
        _, trace = evaluate(target, {"address": address_raw}, trace=True)
        result = replay_checkpoint(
            target,
            source,
            scope,
            emitted,
            {"address": address_raw},
            {"left": 15, "right": 10},
            expected_trace=trace,
        )
        assert result["values"] == {"left": 15 ^ trace[left], "right": 10 ^ trace[right]}
        assert result["all_input_and_workspace_bits_restored"]


@pytest.mark.parametrize("tamper", ["precision", "source", "target", "output_width"])
def test_original_financial_binding_rechecked(tmp_path, tamper):
    target = _small_graph()
    source, _ = compile_graph(target, tmp_path / "source")
    scope = _fixture_scope(target, source)
    plan = _retain_all(scope)
    if tamper == "precision":
        scope["word_width"] += 1
    elif tamper == "source":
        scope["source_fingerprint"] = "0" * 64
    elif tamper == "target":
        scope["target_fingerprint"] = "0" * 64
    else:
        scope["groups"][0]["out_widths"][0] -= 1
    with pytest.raises(ValueError):
        emit_checkpoint_schedule(target, source, scope, plan)
