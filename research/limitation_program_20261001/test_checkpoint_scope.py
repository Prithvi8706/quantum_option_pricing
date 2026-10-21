"""Extraction checks for shared producers, atomic outputs and financial scope."""

from copy import deepcopy
from pathlib import Path

import pytest

from research.limitation_program_20261001.checkpoint_scope import build_scope, extract_scope


def fixture():
    nodes = [
        {"op": "input", "args": [], "params": {"name": "u0", "bits": 2}, "out": [0]},
        {"op": "input", "args": [], "params": {"name": "unused", "bits": 2}, "out": [1]},
        {"op": "const", "args": [], "params": {"value": 1}, "out": [2]},
        {"op": "lookup", "args": [0], "params": {"table": "fixture"}, "out": [3, 4]},
        {"op": "add", "args": [3, 2], "params": {}, "out": [5]},
        {"op": "mul", "args": [4, 1], "params": {}, "out": [6]},
        {"op": "add", "args": [3, 3], "params": {}, "out": [7]},
    ]
    calls = [{"leaf": str(i), "args": n["args"], "out": n["out"]} for i, n in enumerate(nodes[2:])]
    target = {"nodes": nodes, "tables": {"fixture": [[0, 1], [2, 3]]}}
    source = {
        "values": 8,
        "inputs": nodes[:2],
        "outputs": {"Y": 6},
        "forward_calls": calls,
        "word_width": 5,
        "fraction_bits": 2,
    }
    widths = [2, 2, 1, 5, 5, 5, 5, 5]
    storage = {
        "widths": widths,
        "proof_masks": [(1 << w) - 1 for w in widths],
        "proof_reasons": ["fixture"] * 8,
    }
    metadata = {
        str(i): {"sha256": "0" * 64, "resources": {"qubits": q, "t_count": i}}
        for i, q in enumerate([5, 20, 20, 30, 20])
    }
    return target, source, storage, metadata, {"stock_value": 5}


def test_lookup_sibling_unused_by_root_is_protected_when_used_outside():
    plan = extract_scope(*fixture())
    lookup = next(g for g in plan["groups"] if g["op"] == "lookup")
    assert lookup["out"] == [3, 4]
    assert lookup["width"] == 10
    assert plan["protected_boundary_values"] == [3, 4, 5]
    assert plan["literal_tables"] == {"fixture": [[0, 1], [2, 3]]}
    assert set(plan["selected_call_indices"]) == {0, 1, 2}


def test_repeated_outside_arguments_preserve_both_edge_positions():
    plan = extract_scope(*fixture())
    edge = next(e for e in plan["outgoing_edges"] if e["consumer_node_index"] == 6)
    assert edge["value"] == 3
    assert edge["argument_positions"] == [0, 1]
    assert edge["external"]
    assert len([e for e in plan["outgoing_edges"] if e["value"] == 3]) == 2


def test_unused_random_register_stays_in_floor_and_leaf_private_is_charged():
    plan = extract_scope(*fixture())
    assert len(plan["inputs"]) == 2
    assert plan["required_input_values"] == [0]
    assert not plan["inputs"][1]["needed_by_selected_closure"]
    assert plan["fixed_floor"] == 4 + 3 * 5
    assert plan["baseline_workspace"] == 16 + 15
    assert plan["caps"] == {"75": 42, "50": 34}
    assert plan["minimum_move_qubits"] == 19 + 20 + 11
    assert all(c["infeasible_by_required_local_leaf"] for c in plan["workspace_caps"])


def test_named_output_aliases_have_separate_native_destinations():
    args = list(fixture())
    args[1]["outputs"] = {"root": 5, "alias": 5, "outside": 6}
    plan = extract_scope(*args)
    aliases = [out for out in plan["outputs"] if out["value"] == 5]
    assert {out["name"] for out in aliases} == {"first_date_first_asset_stock", "root", "alias"}
    assert len({out["offset"] for out in aliases}) == 3
    assert plan["fixed_floor"] == 4 + 5 * 5


@pytest.mark.parametrize("damage", ["call-binding", "duplicate-producer", "missing-root"])
def test_invalid_extraction_binding_rejected(damage):
    args = deepcopy(list(fixture()))
    if damage == "call-binding":
        args[1]["forward_calls"][2]["args"] = [0, 2]
    elif damage == "duplicate-producer":
        args[0]["nodes"][-1]["out"] = [6]
    else:
        args[4]["stock_value"] = 100
    with pytest.raises(ValueError):
        extract_scope(*args)


def test_actual_gaussian_estrin_scope_has_complete_external_edge_protection():
    root = Path(__file__).resolve().parents[2]
    baseline = root / "results/limitation_program_20261001/A10_coefficient_run001/B4x12/min-depth"
    plan = build_scope(baseline)
    assert plan["selection"]["complete_optimized_graph_equality"]
    assert plan["selection"]["stock_value"] == 4021
    assert plan["selection"]["clipped_log_value"] == 3579
    assert len(plan["groups"]) == 159
    assert len(plan["inputs"]) == 60
    assert all(inp["bits"] == 32 for inp in plan["inputs"])
    assert plan["required_input_values"] == [0, 1]
    assert len(plan["outputs"]) == 28
    assert {e["value"] for e in plan["outgoing_edges"] if e["external"]} <= set(
        plan["protected_boundary_values"]
    )
    assert plan["selection"]["common_normal_value"] in plan["selected_value_ids"]
    assert plan["selection"]["idiosyncratic_normal_value"] in plan["selected_value_ids"]
    assert plan["operation_counts"]["lookup"] == 3
    assert plan["operation_counts"]["sqrt"] == 1
    assert plan["fixed_floor"] == 3936
    assert plan["baseline_workspace"] == 25194
    assert plan["minimum_move_qubits"] == 19445
    assert plan["caps"] == {"75": 22831, "50": 16533}
