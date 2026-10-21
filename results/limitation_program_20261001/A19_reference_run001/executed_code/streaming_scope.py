"""Original-site subroutine boundaries for exact B2x4 streaming arithmetic."""

from __future__ import annotations

from collections import Counter

from research.controlled_priority_completion.parallel_source import entries
from research.controlled_source_completion.compact_parallel_v7 import _storage, fingerprint


def producer_closure(target, roots, boundaries=()):
    """Atomic node ancestor closure, preserving complete multi-output producers."""
    producers = {value: i for i, node in enumerate(target["nodes"]) for value in node["out"]}
    stop, selected, stack = set(boundaries), set(), list(roots)
    while stack:
        value = stack.pop()
        if value in stop:
            continue
        if value not in producers:
            raise ValueError("Subroutine root/predecessor lacks an original SSA producer")
        index = producers[value]
        node = target["nodes"][index]
        if index in selected or node["op"] == "input":
            continue
        selected.add(index)
        stack.extend(node["args"])
    return sorted(selected)


def build_streaming_scope(target, source, semantics):
    """Validate original target, then freeze Gaussian/date/payoff subroutines."""
    if semantics["target_fingerprint"] != fingerprint(target):
        raise ValueError("Financial template labels do not bind original B2 target")
    metadata = entries(source)
    storage = _storage(target, source, metadata)
    nodes = target["nodes"]
    noninputs = [i for i, node in enumerate(nodes) if node["op"] != "input"]
    call_for_node = dict(zip(noninputs, range(len(source["forward_calls"]))))
    producer = {value: i for i, node in enumerate(nodes) for value in node["out"]}
    constants = set(semantics["global_constant_values"])
    normals = set(semantics["normal_values"])
    widths = storage["widths"]

    def groups_for(indices):
        selected_ids = {call_for_node[index] for index in indices}
        groups = []
        for index in indices:
            call_index = call_for_node[index]
            call = source["forward_calls"][call_index]
            entry = metadata[call["leaf"]]
            out_widths = [widths[value] for value in call["out"]]
            args = list(call["args"])
            pred_ids = {
                call_for_node[producer[value]]
                for value in args
                if nodes[producer[value]]["op"] != "input"
            }
            external_values = [
                value
                for value in args
                if nodes[producer[value]]["op"] == "input"
                or call_for_node[producer[value]] not in selected_ids
            ]
            groups.append(
                {
                    "id": call_index,
                    "call_index": call_index,
                    "node_index": index,
                    "op": nodes[index]["op"],
                    "params": nodes[index]["params"],
                    "args": args,
                    "out": list(call["out"]),
                    "outputs": list(call["out"]),
                    "out_widths": out_widths,
                    "width": sum(out_widths),
                    "private": entry["resources"]["qubits"] - sum(out_widths),
                    "preds": sorted(pred_ids & selected_ids),
                    "external_values": sorted(set(external_values)),
                    "leaf": call["leaf"],
                    "gate_sha256": entry["sha256"],
                    "resources": entry["resources"],
                    "cost": entry["resources"]["t_count"],
                }
            )
        return groups

    def subroutine(roots, boundaries):
        indices = producer_closure(target, roots, boundaries)
        groups = groups_for(indices)
        selected_values = {value for group in groups for value in group["out"]}
        external = sorted(
            {value for group in groups for value in group["args"] if value not in selected_values}
        )
        if any(
            value not in set(boundaries) and nodes[producer[value]]["op"] != "input"
            for value in external
        ):
            raise ValueError("Original-site subroutine lost a required boundary")
        return {
            "root_values": list(roots),
            "boundary_values": external,
            "selected_node_indices": indices,
            "call_indices": [group["id"] for group in groups],
            "groups": groups,
            "atomic_lookup_producers": [group["id"] for group in groups if group["op"] == "lookup"],
            "retained_internal_width": sum(group["width"] for group in groups),
            "maximum_private_width": max((group["private"] for group in groups), default=0),
            "whole_original_typed_sites_preserved": True,
        }

    gaussian_pairs = []
    for pair in range(6):
        roots = semantics["normal_values"][pair * 2 : pair * 2 + 2]
        descriptor = subroutine(roots, constants)
        input_values = [
            value
            for value in descriptor["boundary_values"]
            if nodes[producer[value]]["op"] == "input"
        ]
        if len(input_values) != 2:
            raise ValueError("Gaussian pair does not bind exactly two original uniform words")
        descriptor.update(pair=pair, normal_values=list(roots), input_values=input_values)
        gaussian_pairs.append(descriptor)
    date_bindings = []
    for binding in semantics["date_bindings"]:
        increments = subroutine(binding["increment_values"], constants | normals)
        local = subroutine([binding["basket_value"]], constants | set(binding["raw_log_values"]))
        selected_values = {value for group in local["groups"] for value in group["out"]}
        if not set(binding["stock_values"]) <= selected_values:
            raise ValueError("Date basket stage lost an actual stock exponential")
        if set(local["boundary_values"]) - constants != set(binding["raw_log_values"]):
            raise ValueError("Date stock stage consumes an unexpected nonconstant boundary")
        date_bindings.append(
            dict(
                binding,
                increment_subroutine=increments,
                increment_groups=increments["groups"],
                local_subroutine=local,
                local_groups=local["groups"],
                local_call_indices=local["call_indices"],
            )
        )
    # The existing average/strike/discount leaf chain is preserved. Alive and
    # Asian sum are supplied by proved running-statistic identities.
    payoff = subroutine(
        [semantics["output_value"]],
        constants | {semantics["asian_sum_value"], semantics["alive_value"]},
    )
    constant_groups = groups_for(sorted(producer[value] for value in constants))
    full_groups = groups_for(noninputs)
    source_inputs = [
        {
            "id": node["out"][0],
            "name": node["params"]["name"],
            "bits": node["params"]["bits"],
            "width": widths[node["out"][0]],
        }
        for node in source["inputs"]
    ]
    return {
        "format": "exact-original-site-B2x4-streaming-scope-v1",
        "word_width": source["word_width"],
        "fraction_bits": source["fraction_bits"],
        "target_fingerprint": fingerprint(target),
        "source_fingerprint": fingerprint(source),
        "semantics": semantics,
        "inputs": source_inputs,
        "original_outputs": source["outputs"],
        "widths": widths,
        "proof_masks": storage["proof_masks"],
        "proof_reasons": storage["proof_reasons"],
        "constant_groups": constant_groups,
        "global_constant_values": sorted(constants),
        "normal_values": list(semantics["normal_values"]),
        "gaussian_pairs": gaussian_pairs,
        "date_bindings": date_bindings,
        "payoff_subroutine": payoff,
        "payoff_groups": payoff["groups"],
        "final_groups": payoff["groups"],
        "final_call_indices": payoff["call_indices"],
        "final_total_stock_sum_value": semantics["asian_sum_value"],
        "original_alive_value": semantics["alive_value"],
        "final_output_value": semantics["output_value"],
        "initial_log_raw": nodes[producer[semantics["initial_log_value"]]]["params"]["value"],
        "threshold_value": semantics["barrier_value"],
        "all_original_groups": full_groups,
        "original_operation_counts": dict(Counter(group["op"] for group in full_groups)),
        "whole_original_storage_validated_before_subroutine_extraction": True,
        "mutable_state_binding_requirement": (
            "At date j each current raw-log word equals the original parallel-prefix "
            "raw_log_values[j] exactly modulo 2^72; the sum equals original native "
            "stock-word accumulation before averaging; count==0 equals original alive "
            "predicate. No independent boundary-input law replaces these identities."
        ),
        "checkpoint_placements": [
            {"name": "date-boundaries", "block_dates": [[0], [1], [2], [3]]},
            {"name": "two-date-blocks", "block_dates": [[0, 1], [2, 3]]},
        ],
        "harness_only": True,
        "full_B4_scaling_executed": False,
        "G2_to_G5": "open",
    }


def streaming_statistics_from_original_trace(scope, trace):
    """Independent integer identities for current raw logs, total and violations.

    This helper uses original exponential outputs and makes no circuit or runtime
    claim. Actual emitted stages must separately replay their leaf gate arrays.
    """
    semantics = scope["semantics"]
    w, f = scope["word_width"], scope["fraction_bits"]
    modulus, sign = 1 << w, 1 << (w - 1)

    def signed(value):
        return value - modulus if value & sign else value

    raw = [int(trace[semantics["initial_log_value"]])] * 2
    total = violations = 0
    history = []
    for binding in scope["date_bindings"]:
        raw = [
            (value + int(trace[increment])) % modulus
            for value, increment in zip(raw, binding["increment_values"], strict=True)
        ]
        original_raw = [int(trace[value]) for value in binding["raw_log_values"]]
        if raw != original_raw:
            raise AssertionError("Sequential raw log differs from original prefix arithmetic")
        stocks = [int(trace[value]) for value in binding["stock_values"]]
        total = (total + sum(stocks)) % modulus
        basket_sum = sum(stocks) % modulus
        basket = (signed(basket_sum) * ((1 << f) // 2) >> f) % modulus
        if basket != int(trace[binding["basket_value"]]):
            raise AssertionError("Date arithmetic basket differs from original rounding")
        violations += int(signed(basket) >= signed(int(trace[semantics["barrier_value"]])))
        history.append(
            {
                "date": binding["date"],
                "raw_logs": list(raw),
                "asian_sum": total,
                "basket": basket,
                "violations": violations,
            }
        )
    if total != int(trace[semantics["asian_sum_value"]]):
        raise AssertionError("Running native-stock sum differs from original balanced tree")
    alive = int(violations == 0)
    if alive != int(trace[semantics["alive_value"]]):
        raise AssertionError("Violation count zero differs from original strict barrier")
    average = (signed(total) * semantics["average_coefficient"] >> f) % modulus
    positive = max(signed((average - int(trace[semantics["strike_value"]])) % modulus), 0)
    payoff = (positive * semantics["discount_coefficient"] >> f) % modulus
    output = payoff if alive else 0
    if output != int(trace[semantics["output_value"]]):
        raise AssertionError("Running sufficient-statistic payoff differs from original source")
    return {
        "history": history,
        "asian_sum": total,
        "violations": violations,
        "alive": alive,
        "raw_output": output,
        "identity_checks_passed": True,
        "gate_replay_executed": False,
    }
