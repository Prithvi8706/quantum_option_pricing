"""Freeze one actual financial ancestor closure for paid reversible checkpointing.

The complete accepted graph is validated before extracting a sparse subgraph.
All random-input registers remain retained, including the unused coordinates.
Every selected value consumed outside the closure is a named, full-native-width
boundary output. Atomic producer groups retain every output of a lookup leaf.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path

from research.controlled_priority_completion.parallel_source import entries
from research.controlled_source_completion.compact_parallel_v7 import _storage, fingerprint
from research.controlled_source_completion.compiler import resolve_library
from research.limitation_program_20261001.baseline import fingerprints


ROOT = Path(__file__).resolve().parents[2]
FORMAT = "paid-checkpoint-financial-scope-v1"


def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def select_financial_root(target):
    """Capture the builder's first stock and require complete optimized equality."""
    from research.advantage_frontier_20260923 import barrier_oracle_depth as builder
    from research.controlled_source_completion.optimize import optimize

    captured_exponentials, captured_normals = [], []
    original_exp, original_normals = builder.exp_estrin, builder.normals_graph

    def capture_exp(graph, argument):
        result = original_exp(graph, argument)
        captured_exponentials.append((argument, result))
        return result

    def capture_normals(graph, count, precision):
        result = original_normals(graph, count, precision)
        captured_normals.extend(result)
        return result

    builder.exp_estrin, builder.normals_graph = capture_exp, capture_normals
    try:
        original = json.loads(json.dumps(builder.build(4, 12, q=32).as_dict()))
    finally:
        builder.exp_estrin, builder.normals_graph = original_exp, original_normals
    if optimize(original) != target:
        raise ValueError("Financial builder/optimizer differs from the accepted B4 target")
    before, after = fingerprints(original), fingerprints(target)
    reverse = {token: value for value, token in after.items()}
    if len(reverse) != len(after):
        raise ValueError("Ambiguous optimized structural fingerprints")
    if len(captured_exponentials) != 4 * 12 or len(captured_normals) != 12 * 5:
        raise ValueError("Unexpected financial builder exponential or normal order")
    clipped_log, stock = captured_exponentials[0]
    return {
        "builder": "research.advantage_frontier_20260923.barrier_oracle_depth.build",
        "assets": 4,
        "dates": 12,
        "asset_index": 0,
        "date_index": 0,
        "rule": "first exp_estrin invocation in verified asset-major/date-major builder",
        "original_stock_value": stock,
        "stock_value": reverse[before[stock]],
        "clipped_log_value": reverse[before[clipped_log]],
        "common_normal_value": reverse[before[captured_normals[0]]],
        "idiosyncratic_normal_value": reverse[before[captured_normals[1]]],
        "stock_structural_fingerprint": before[stock],
        "clipped_log_structural_fingerprint": before[clipped_log],
        "full_original_graph_fingerprint": fingerprint(original),
        "full_optimized_graph_fingerprint": fingerprint(target),
        "complete_optimized_graph_equality": True,
        "builder_files": {
            str(path): file_sha(ROOT / path)
            for path in (
                "research/advantage_frontier_20260923/barrier_oracle_depth.py",
                "research/controlled_source_completion/finance.py",
                "research/controlled_source_completion/ir.py",
                "research/controlled_source_completion/optimize.py",
                "research/limitation_program_20261001/baseline.py",
            )
        },
    }


def extract_scope(target, source, storage, metadata, selection):
    """Pure atomic extraction after whole-target validation; useful for fixtures."""
    root = selection["stock_value"]
    nodes, calls = target["nodes"], source["forward_calls"]
    producers = {v: index for index, node in enumerate(nodes) for v in node["out"]}
    if len(producers) != source["values"] or root not in producers:
        raise ValueError("Missing or duplicate SSA producer")
    widths = storage["widths"]
    noninput_nodes = [i for i, node in enumerate(nodes) if node["op"] != "input"]
    call_for_node = dict(zip(noninput_nodes, range(len(calls))))
    selected, stack = set(), [root]
    while stack:
        node_index = producers[stack.pop()]
        node = nodes[node_index]
        if node["op"] == "input" or node_index in selected:
            continue
        selected.add(node_index)
        stack.extend(node["args"])
    selected_values = {v for i in selected for v in nodes[i]["out"]}
    input_values = {v for node in source["inputs"] for v in node["out"]}
    needed_inputs = sorted({v for i in selected for v in nodes[i]["args"] if v in input_values})
    outgoing_edges = []
    for node_index, node in enumerate(nodes):
        for value in sorted(set(node["args"]) & selected_values):
            outgoing_edges.append(
                {
                    "value": value,
                    "consumer_node_index": node_index,
                    "consumer_call_index": call_for_node[node_index],
                    "consumer_op": node["op"],
                    "consumer_outputs": list(node["out"]),
                    "argument_positions": [
                        i for i, argument in enumerate(node["args"]) if argument == value
                    ],
                    "external": node_index not in selected,
                }
            )
    boundary_values = {edge["value"] for edge in outgoing_edges if edge["external"]}
    boundary_values.add(root)
    # Preserve named output aliases as distinct external native destinations.
    named_inside = {
        name: value for name, value in source["outputs"].items() if value in selected_values
    }
    boundary_values.update(named_inside.values())
    groups = []
    for node_index in sorted(selected):
        node = nodes[node_index]
        call_index = call_for_node[node_index]
        call = calls[call_index]
        if (node["args"], node["out"]) != (call["args"], call["out"]):
            raise ValueError("Target/source invocation mismatch")
        entry = metadata[call["leaf"]]
        out_widths = [widths[v] for v in node["out"]]
        output_width = sum(out_widths)
        pred_ids = sorted(
            {call_for_node[producers[v]] for v in node["args"] if v not in input_values}
        )
        if any(producers[v] not in selected for v in node["args"] if v not in input_values):
            raise ValueError("Ancestor closure lost a predecessor group")
        groups.append(
            {
                "id": call_index,
                "call_index": call_index,
                "node_index": node_index,
                "op": node["op"],
                "params": node["params"],
                "args": list(node["args"]),
                "out": list(node["out"]),
                "outputs": list(node["out"]),
                "out_widths": out_widths,
                "width": output_width,
                "private": entry["resources"]["qubits"] - output_width,
                "preds": pred_ids,
                "input_values": [v for v in node["args"] if v in input_values],
                "leaf": call["leaf"],
                "gate_sha256": entry["sha256"],
                "resources": entry["resources"],
                "cost": entry["resources"]["t_count"],
                "argument_copy_cx_per_invocation": 2 * sum(widths[v] for v in node["args"]),
                "argument_copy_rounds_per_direction": max(
                    Counter(node["args"]).values(), default=0
                ),
            }
        )
    input_bindings, cursor = [], 0
    for node in source["inputs"]:
        if len(node["out"]) != 1:
            raise ValueError("Unexpected multi-register external input")
        value = node["out"][0]
        input_bindings.append(
            {
                "id": value,
                "value": value,
                "name": node["params"]["name"],
                "bits": node["params"]["bits"],
                "width": widths[value],
                "offset": cursor,
                "needed_by_selected_closure": value in needed_inputs,
            }
        )
        cursor += widths[value]
    random_floor = cursor
    outputs = []
    for value in sorted(boundary_values):
        name = "first_date_first_asset_stock" if value == root else f"boundary_ssa_{value}"
        outputs.append(
            {
                "name": name,
                "outputname": name,
                "value": value,
                "group": call_for_node[producers[value]],
                "offset": cursor,
                "width": source["word_width"],
                "protected_external_uses": sum(
                    edge["external"] for edge in outgoing_edges if edge["value"] == value
                ),
            }
        )
        cursor += source["word_width"]
    for name, value in sorted(named_inside.items()):
        outputs.append(
            {
                "name": name,
                "outputname": name,
                "value": value,
                "group": call_for_node[producers[value]],
                "offset": cursor,
                "width": source["word_width"],
                "named_financial_output_alias": True,
            }
        )
        cursor += source["word_width"]
    group_for_id = {group["id"]: group for group in groups}
    retained = sum(group["width"] for group in groups)
    private = max((group["private"] for group in groups), default=0)
    workspace = retained + private
    leaf_bounds = [
        {
            "group": group["id"],
            "op": group["op"],
            "total_qubits": cursor
            + group["width"]
            + group["private"]
            + sum(group_for_id[pred]["width"] for pred in group["preds"]),
            "predecessor_group_width": sum(group_for_id[pred]["width"] for pred in group["preds"]),
            "destination_width": group["width"],
            "private_width": group["private"],
        }
        for group in groups
    ]
    minimum = max(leaf_bounds, key=lambda row: (row["total_qubits"], -row["group"]))
    tables = {
        node["params"]["table"]: target["tables"][node["params"]["table"]]
        for i in sorted(selected)
        if (node := nodes[i])["op"] == "lookup"
    }
    return {
        "format": FORMAT,
        "word_width": source["word_width"],
        "fraction_bits": source["fraction_bits"],
        "selection": selection,
        "groups": groups,
        "inputs": input_bindings,
        "outputs": outputs,
        "output_bindings": outputs,
        "required_input_values": needed_inputs,
        "widths": widths,
        "proof_masks": storage["proof_masks"],
        "proof_reasons": storage["proof_reasons"],
        "selected_node_indices": sorted(selected),
        "selected_value_ids": sorted(selected_values),
        "selected_call_indices": [group["id"] for group in groups],
        "outgoing_edges": outgoing_edges,
        "protected_boundary_values": sorted(boundary_values),
        "literal_tables": tables,
        "original_named_outputs": source["outputs"],
        "fixed_floor": cursor,
        "floor": cursor,
        "fixed_floor_components": {
            "all_original_random_input_qubits": random_floor,
            "named_full_native_boundary_output_qubits": cursor - random_floor,
            "unused_random_coordinates_remain_retained": True,
        },
        "retained_group_width": retained,
        "maximum_private_leaf_workspace": private,
        "retain_all_transient_workspace": workspace,
        "baseline_workspace": workspace,
        "caps": {str(percent): cursor + workspace * percent // 100 for percent in (75, 50)},
        "retain_all_total_qubits": cursor + workspace,
        "retain_all_definition": (
            "All compact selected producer output slots simultaneously allocated, "
            "plus maximum private native leaf workspace; "
            "all argument copies and high output bits included."
        ),
        "workspace_caps": [
            {
                "percent": percent,
                "cap": cursor + workspace * percent // 100,
                "transient_cap": workspace * percent // 100,
                "formula": f"F + floor({percent}/100 * W0)",
                "infeasible_by_required_local_leaf": cursor + workspace * percent // 100
                < minimum["total_qubits"],
            }
            for percent in (75, 50)
        ],
        "minimum_required_local_move": minimum,
        "minimum_move_qubits": minimum["total_qubits"],
        "minimum_local_move_scope": (
            "Necessary lower bound only: fixed floor plus clean destination, "
            "full charged leaf private scratch and each distinct atomic "
            "predecessor group's active outputs. Additional ancestors, "
            "fragmentation and cleanup may require more workspace."
        ),
        "operation_counts": dict(Counter(group["op"] for group in groups)),
        "complete_financial_replay": False,
        "quantum_advantage": "unproved",
    }


def build_scope(target, source=None, accepted_schedule=None, source_root=None):
    """Validate frozen accepted storage, arrays and builder, then extract scope."""
    if source is None:
        directory = Path(target)
        target = json.loads((directory / "target.json").read_text(encoding="utf-8"))
        source = json.loads((directory / "source.json").read_text(encoding="utf-8"))
        accepted_schedule = json.loads(
            (directory / "schedule_capped.json").read_text(encoding="utf-8")
        )
        source_root = directory
    metadata = entries(source)
    storage = _storage(target, source, metadata)
    for field, value in storage.items():
        if accepted_schedule.get(field) != value:
            raise ValueError("Accepted compact schedule storage differs: " + field)
    if accepted_schedule.get("source_fingerprint") != fingerprint(source):
        raise ValueError("Accepted source fingerprint differs")
    if accepted_schedule.get("target_fingerprint") != fingerprint(target):
        raise ValueError("Accepted target fingerprint differs")
    library = resolve_library(source)
    checked_arrays = {}
    for key, entry in sorted(metadata.items()):
        path = library / entry["gate_file"]
        actual = file_sha(path)
        if actual != entry["sha256"]:
            raise ValueError("Frozen leaf array hash mismatch: " + key)
        checked_arrays[key] = actual
    selection = select_financial_root(target)
    scope = extract_scope(target, source, storage, metadata, selection)
    scope["source_fingerprint"] = fingerprint(source)
    scope["target_fingerprint"] = fingerprint(target)
    scope["accepted_schedule_fingerprint"] = fingerprint(accepted_schedule)
    scope["whole_original_typed_storage_validated_before_extraction"] = True
    scope["whole_original_library_array_sha256"] = checked_arrays
    if source_root is not None:
        scope["source_root"] = str(Path(source_root).resolve().relative_to(ROOT)).replace("\\", "/")
    return scope
