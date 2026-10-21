"""Matched full-source embedding, protected edges and global-peak fixtures."""

from copy import deepcopy

import pytest

from research.controlled_source_completion.compiler import compile_graph
from research.controlled_source_completion.ir import Graph, evaluate
from research.limitation_program_20261001.checkpoint_B4 import make_b4_schedule, replay_b4
from research.limitation_program_20261001.checkpoint_circuit import emit_checkpoint_schedule
from research.limitation_program_20261001.test_checkpoint_circuit import (
    _fixture_scope,
    _retain_all,
)


def _partial_scope(target, source, selected):
    scope = _fixture_scope(target, source)
    scope["groups"] = [g for g in scope["groups"] if g["id"] in selected]
    cursor = sum(n["width"] for n in scope["inputs"])
    scope["outputs"] = []
    for group in scope["groups"]:
        for value in group["out"]:
            scope["outputs"].append(
                {
                    "name": f"boundary_{value}",
                    "value": value,
                    "group": group["id"],
                    "offset": cursor,
                }
            )
            cursor += source["word_width"]
    scope["fixed_floor"] = cursor
    return scope


def _early_copy_plan(scope):
    """Independent producers copied and genuinely erased before reusing slots."""
    moves, floor, peak = [], scope["fixed_floor"], scope["fixed_floor"]
    for group in scope["groups"]:
        assert not group["preds"]
        storage = [{"offset": floor, "width": group["width"]}]
        private = [{"offset": floor + group["width"], "width": group["private"]}]
        peak = max(peak, floor + group["width"] + group["private"])
        invocation = {"group": group["id"], "storage": storage, "private_storage": private}
        moves.append(dict(invocation, kind="compute"))
        for output in scope["outputs"]:
            if output["group"] == group["id"]:
                moves.append(
                    {"kind": "copy_output", "value": output["value"], "outputname": output["name"]}
                )
        moves.append(dict(invocation, kind="erase"))
    return {"heuristic": "early-copy-fixture", "moves": moves, "cap": peak}


def _squared_fixture(tmp_path):
    graph = Graph(f=2, integer_bits=2)
    raw = graph.input("raw", 2)
    square = graph.mul(raw, raw)
    constant = graph.const_int(3)
    final = graph.add(square, constant)
    graph.outputs = {"Y": final, "alias": final}
    target = graph.as_dict()
    source, _ = compile_graph(target, tmp_path / "source")
    scope = _partial_scope(target, source, {0, 1})
    return target, source, scope


def test_full_exact_target_all_dirty_output_patterns_and_boundary_cleanup(tmp_path):
    target, source, scope = _squared_fixture(tmp_path)
    sub = emit_checkpoint_schedule(target, source, scope, _early_copy_plan(scope))
    full = make_b4_schedule(target, source, scope, sub)
    assert full["subroutine_invocations"] == 2
    assert full["external_forward_calls"] == 1
    assert full["resources"]["t_count"] == 7 * full["resources"]["ccx"]
    for raw in range(4):
        _, trace = evaluate(target, {"raw": raw}, trace=True)
        for dirty in range(16):
            initial = {"Y": dirty, "alias": dirty ^ 15}
            result = replay_b4(
                target, source, scope, sub, full, {"raw": raw}, initial, expected_trace=trace
            )
            assert result["values"] == {
                name: initial[name] ^ trace[value] for name, value in source["outputs"].items()
            }
            assert result["all_input_and_workspace_bits_restored"]
            assert result["boundary_registers_restored"]
            assert result["native_gate_invocations"] == 10


def test_matched_global_peak_saves_only_actual_private_bank_difference(tmp_path):
    target, source, scope = _squared_fixture(tmp_path)
    old_sub = emit_checkpoint_schedule(target, source, scope, _retain_all(scope))
    new_sub = emit_checkpoint_schedule(target, source, scope, _early_copy_plan(scope))
    old = make_b4_schedule(target, source, scope, old_sub)
    new = make_b4_schedule(target, source, scope, new_sub)
    assert old["outside_allocations"] == new["outside_allocations"]
    assert old_sub["resources"]["logical_qubits"] - new_sub["resources"]["logical_qubits"] == 2
    assert old["resources"]["logical_qubits"] - new["resources"]["logical_qubits"] == 2
    assert old["resources"]["t_count"] == new["resources"]["t_count"]


def test_outside_leaf_can_hide_extracted_workspace_saving(tmp_path):
    graph = Graph(f=2, integer_bits=2)
    raw = graph.input("raw", 2)
    constant_a, constant_b = graph.const_int(3), graph.const_int(1)
    final = graph.mul(graph.add(raw, constant_a), constant_b)
    graph.outputs = {"Y": final}
    target = graph.as_dict()
    source, _ = compile_graph(target, tmp_path / "source")
    scope = _partial_scope(target, source, {0, 1})
    old_sub = emit_checkpoint_schedule(target, source, scope, _retain_all(scope))
    new_sub = emit_checkpoint_schedule(target, source, scope, _early_copy_plan(scope))
    old, new = (make_b4_schedule(target, source, scope, sub) for sub in (old_sub, new_sub))
    assert old_sub["resources"]["logical_qubits"] > new_sub["resources"]["logical_qubits"]
    assert old["resources"]["logical_qubits"] == new["resources"]["logical_qubits"]
    assert (
        new["resources"]["outside_private_leaf_workspace_qubits"]
        > (old["resources"]["extracted_transient_workspace_qubits"])
    )


def test_full_embedding_rejects_omitted_protected_outgoing_edge(tmp_path):
    target, source, scope = _squared_fixture(tmp_path)
    # Square and the constant both feed the outside add; neither can be omitted.
    scope["outputs"] = scope["outputs"][:1]
    scope["fixed_floor"] -= source["word_width"]
    sub = emit_checkpoint_schedule(target, source, scope, _retain_all(scope))
    with pytest.raises(ValueError, match="outgoing financial edge"):
        make_b4_schedule(target, source, scope, sub)


@pytest.mark.parametrize(
    "field",
    ["target_fingerprint", "source_fingerprint", "scope_fingerprint", "subroutine_fingerprint"],
)
def test_full_replay_rechecks_all_original_and_subroutine_bindings(tmp_path, field):
    target, source, scope = _squared_fixture(tmp_path)
    sub = emit_checkpoint_schedule(target, source, scope, _early_copy_plan(scope))
    full = make_b4_schedule(target, source, scope, sub)
    altered = deepcopy(full)
    altered[field] = "0" * 64
    with pytest.raises(ValueError, match="binding changed"):
        replay_b4(target, source, scope, sub, altered, {"raw": 0})


@pytest.mark.parametrize("tamper", ["output_offset", "call_leaf", "ssa_width", "private_peak"])
def test_full_replay_reconstructs_unchanged_outside_allocation(tmp_path, tamper):
    target, source, scope = _squared_fixture(tmp_path)
    sub = emit_checkpoint_schedule(target, source, scope, _early_copy_plan(scope))
    full = make_b4_schedule(target, source, scope, sub)
    altered = deepcopy(full)
    if tamper == "output_offset":
        altered["named_outputs"][0]["offset"] -= 1
    elif tamper == "call_leaf":
        altered["outside_allocations"][0]["leaf"] = scope["groups"][0]["leaf"]
    elif tamper == "ssa_width":
        altered["outside_allocations"][0]["output_bindings"][0]["width"] -= 1
    else:
        altered["private_width"] -= 1
    with pytest.raises(ValueError, match="changed"):
        replay_b4(target, source, scope, sub, altered, {"raw": 0})
