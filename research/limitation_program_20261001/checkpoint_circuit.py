"""Paid reversible checkpoint circuits using unchanged financial leaf arrays.

The hierarchy is an emitted logical circuit: explicit copies, native leaf gates,
literal leaf inverses, physical allocation spans and output XOR copies. Each
invocation has a serial barrier; ASAP scheduling is used only inside its leaf.
No dynamic allocation or recomputation is free in the resource ledger.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import json

import numpy as np

from research.controlled_priority_completion.parallel_source import entries
from research.controlled_source_completion.compact_parallel_v7 import _storage
from research.controlled_source_completion.compiler import mapped_gates, resolve_library
from research.controlled_source_completion.primitives import gate_resources


FORMAT = "paid-reversible-checkpoint-circuit-v1"
COUNT_FIELDS = ("source_gates", "x", "cx", "ccx", "t_count", "clifford_cx", "clifford_h")


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode("utf-8")).hexdigest()


def _groups(scope):
    result = {g["id"]: g for g in scope["groups"]}
    if len(result) != len(scope["groups"]):
        raise ValueError("duplicate producer group")
    return result


def _spans(spans, width, floor, cap):
    """Validate and expand explicit physical spans independently of allocator."""
    wires = []
    for span in spans:
        offset, size = span["offset"], span["width"]
        if type(offset) is not int or type(size) is not int or size <= 0:
            raise ValueError("invalid physical allocation span")
        if offset < floor or offset + size > cap:
            raise ValueError("physical allocation exceeds declared workspace cap")
        wires.extend(range(offset, offset + size))
    if len(wires) != width or len(wires) != len(set(wires)):
        raise ValueError("physical span width or overlap mismatch")
    return np.asarray(wires, dtype=np.int64)


def validate_allocations(scope, plan):
    """Reject illegal moves without trusting scheduler live-state bookkeeping."""
    groups = _groups(scope)
    floor, cap = scope["fixed_floor"], plan["cap"]
    if type(cap) is not int or cap < floor:
        raise ValueError("workspace cap cannot fit fixed input/output floor")
    input_ids = {n["id"] for n in scope["inputs"]}
    output_specs = {o["name"]: o for o in scope["outputs"]}
    if len(output_specs) != len(scope["outputs"]):
        raise ValueError("duplicate named output")
    fixed = set()
    for node in scope["inputs"]:
        interval = set(range(node["offset"], node["offset"] + node["width"]))
        if fixed & interval or min(interval, default=-1) < 0 or max(interval, default=0) >= floor:
            raise ValueError("input floor register collision")
        fixed |= interval
    for output in scope["outputs"]:
        interval = set(range(output["offset"], output["offset"] + scope["word_width"]))
        if fixed & interval or min(interval, default=-1) < 0 or max(interval, default=0) >= floor:
            raise ValueError("named output floor register collision")
        fixed |= interval
    if fixed != set(range(floor)):
        raise ValueError("fixed floor contains unaccounted wires")
    producer = {}
    for group in groups.values():
        if group["width"] != sum(group["out_widths"]):
            raise ValueError("atomic producer output width mismatch")
        if len(group["out"]) != len(group["out_widths"]):
            raise ValueError("atomic producer output arity mismatch")
        for value in group["out"]:
            if value in producer or value in input_ids:
                raise ValueError("duplicate SSA producer")
            producer[value] = group["id"]
    live, occupied, copied = {}, set(), Counter()
    peak, highwater, maximum_private = floor, floor, 0
    for index, move in enumerate(plan["moves"]):
        kind = move["kind"]
        if kind == "copy_output":
            name = move.get("outputname", move.get("name"))
            if name not in output_specs or move["value"] != output_specs[name]["value"]:
                raise ValueError("output copy does not bind declared SSA value")
            value = move["value"]
            if value not in input_ids and producer.get(value) not in live:
                raise ValueError("output copy requires live producer")
            if copied[name]:
                raise ValueError("named output copied more than once")
            copied[name] += 1
            continue
        if kind not in ("compute", "erase") or move["group"] not in groups:
            raise ValueError("unsupported checkpoint move")
        group = groups[move["group"]]
        actual_preds = {producer[a] for a in group["args"] if a not in input_ids}
        if set(group["preds"]) != actual_preds or any(p not in live for p in actual_preds):
            raise ValueError("compute/erase requires every predecessor producer live")
        storage = _spans(move["storage"], group["width"], floor, cap)
        private = _spans(move["private_storage"], group["private"], floor, cap)
        storage_set, private_set = set(map(int, storage)), set(map(int, private))
        if kind == "compute":
            if group["id"] in live or occupied & storage_set:
                raise ValueError("dirty destination overwrite or double compute")
            if private_set & (occupied | storage_set):
                raise ValueError("native private workspace aliases live SSA")
            live[group["id"]] = move["storage"]
            occupied |= storage_set
        else:
            if group["id"] not in live or live[group["id"]] != move["storage"]:
                raise ValueError("erase requires its original live allocation")
            if private_set & occupied:
                raise ValueError("native private workspace aliases live SSA")
        peak = max(peak, floor + len(occupied) + len(private_set))
        highwater = max(highwater, max(storage_set | private_set, default=floor - 1) + 1)
        maximum_private = max(maximum_private, len(private_set))
        if kind == "erase":
            occupied -= storage_set
            del live[group["id"]]
        if floor + len(occupied) > cap:
            raise ValueError("observed live storage exceeds cap")
    if live or occupied:
        raise ValueError("checkpoint schedule leaves producer registers dirty")
    if set(copied) != set(output_specs):
        raise ValueError("checkpoint schedule omits named/boundary output copy")
    return {
        "peak_live_qubits": peak,
        "logical_qubits": highwater,
        "max_reused_scratch_qubits": maximum_private,
        "complete_checkpoint_cleanup": True,
        "named_output_copy_count": dict(copied),
    }


def _native_cost(gates, qubits, inverse):
    counted, td, ctd = gate_resources(gates[::-1] if inverse else gates, qubits)
    x, cx, ccx = map(int, counted)
    return {
        "source_gates": len(gates),
        "x": x,
        "cx": cx,
        "ccx": ccx,
        "t_count": 7 * ccx,
        "clifford_cx": cx + 6 * ccx,
        "clifford_h": 2 * ccx,
        "t_depth": int(td),
        "clifford_t_depth": int(ctd),
    }


def _checked_context(target, source, scope):
    if scope["word_width"] != source["word_width"]:
        raise ValueError("checkpoint native word width changed")
    if scope["source_fingerprint"] != fingerprint(source) or scope[
        "target_fingerprint"
    ] != fingerprint(target):
        raise ValueError("checkpoint scope does not match original financial target/source")
    metadata = entries(source)
    storage = _storage(target, source, metadata)
    widths = storage["widths"]
    if scope["widths"] != widths:
        raise ValueError("checkpoint active masks or widths differ from original proof")
    if "proof_masks" in scope and scope["proof_masks"] != storage["proof_masks"]:
        raise ValueError("checkpoint active-bit masks differ from original proof")
    original_inputs = {n["out"][0]: n for n in source["inputs"]}
    if {n["id"] for n in scope["inputs"]} != set(original_inputs):
        raise ValueError("checkpoint scope must retain all original random input registers")
    for node in scope["inputs"]:
        original = original_inputs[node["id"]]
        if (node["name"], node["bits"], node["width"]) != (
            original["params"]["name"],
            original["params"]["bits"],
            widths[node["id"]],
        ):
            raise ValueError("checkpoint external input promise changed")
    for group in scope["groups"]:
        call = source["forward_calls"][group["call_index"]]
        entry = metadata[call["leaf"]]
        if (
            group["args"] != call["args"]
            or group["out"] != call["out"]
            or group["leaf"] != call["leaf"]
        ):
            raise ValueError("checkpoint producer does not bind original native leaf")
        if group["out_widths"] != [widths[v] for v in call["out"]]:
            raise ValueError("checkpoint producer compact widths changed")
        if group["private"] != entry["resources"]["qubits"] - group["width"]:
            raise ValueError("checkpoint private native/high-output scratch not fully charged")
    return metadata, storage


def emit_checkpoint_schedule(target, source, scope, plan):
    """Freeze actual leaf costs and all copy/allocation events into the circuit."""
    metadata, _ = _checked_context(target, source, scope)
    observed = validate_allocations(scope, plan)
    groups, library = _groups(scope), resolve_library(source)
    costs, gate_hashes = {}, {}
    for key in sorted({g["leaf"] for g in groups.values()}):
        entry = metadata[key]
        path = library / entry["gate_file"]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != entry["sha256"]:
            raise ValueError("checkpoint native gate array hash mismatch")
        gates = np.load(path, mmap_mode="r")
        if gates.ndim != 2 or gates.shape[1] != 4:
            raise ValueError("invalid emitted native gate array")
        q = entry["resources"]["qubits"]
        forward = _native_cost(gates, q, False)
        inverse = _native_cost(gates, q, True)
        if any(forward[field] != entry["resources"][field] for field in forward):
            raise ValueError("actual native leaf cost does not match frozen metadata")
        costs[key] = {"compute": forward, "erase": inverse}
        gate_hashes[key] = digest
    totals = Counter()
    events, argument_cx, output_cx, copy_depth = [], 0, 0, 0
    widths = scope["widths"]
    for index, move in enumerate(plan["moves"]):
        event = dict(move, index=index)
        if move["kind"] == "copy_output":
            value = move["value"]
            cx = widths[value]
            output_cx += cx
            for field in ("source_gates", "cx", "clifford_cx"):
                totals[field] += cx
            totals["clifford_t_depth"] += 1
            event.update(copy_cx=cx, copy_depth=1)
        else:
            group = groups[move["group"]]
            cost = costs[group["leaf"]][move["kind"]]
            for field, count in cost.items():
                totals[field] += count
            cx = 2 * sum(widths[v] for v in group["args"])
            depth = 2 * max(Counter(group["args"]).values(), default=0)
            for field in ("source_gates", "cx", "clifford_cx"):
                totals[field] += cx
            totals["clifford_t_depth"] += depth
            argument_cx += cx
            copy_depth += depth
            event.update(
                leaf=group["leaf"],
                call_index=group["call_index"],
                args=group["args"],
                out=group["out"],
                argument_copy_cx=cx,
                argument_copy_depth=depth,
                native_cost=cost,
                literal_inverse=move["kind"] == "erase",
            )
        events.append(event)
    resources = dict(totals)
    resources.update(observed)
    resources["random_hadamards"] = sum(n["bits"] for n in scope["inputs"])
    resources["fixed_floor_qubits"] = scope["fixed_floor"]
    return {
        "format": FORMAT,
        "source_fingerprint": fingerprint(source),
        "target_fingerprint": fingerprint(target),
        "scope_fingerprint": fingerprint(scope),
        "plan_fingerprint": fingerprint(plan),
        "cap": plan["cap"],
        "heuristic": plan["heuristic"],
        "events": events,
        "resources": resources,
        "native_leaf_costs": costs,
        "native_gate_sha256": gate_hashes,
        "argument_and_output_copy_cx": argument_cx + output_cx,
        "argument_copy_cx": argument_cx,
        "output_copy_cx": output_cx,
        "argument_copy_depth": copy_depth,
        "depth_convention": (
            "Serial invocation barriers; exact seven-T Toffoli expansion and all-to-all ASAP "
            "within each native forward/literal-inverse leaf; every interface copy and output "
            "copy charged"
        ),
        "inverse": (
            "Literal gate-array reverse on erase; same predecessor bindings and clean native "
            "private workspace"
        ),
        "routing": "All-to-all logical schedule; physical placement/routing/factory costs unproved",
    }


def _split_value_wires(group, wires):
    result, cursor = {}, 0
    for value, width in zip(group["out"], group["out_widths"], strict=True):
        result[value] = wires[cursor : cursor + width]
        cursor += width
    return result


def replay_checkpoint(
    target, source, scope, schedule, inputs, initial_outputs=None, expected_trace=None
):
    """Execute actual frozen gates, including dirty native-width output XOR."""
    if schedule.get("format") != FORMAT:
        raise ValueError("checkpoint circuit format does not match reader")
    if (
        schedule["source_fingerprint"],
        schedule["target_fingerprint"],
        schedule["scope_fingerprint"],
    ) != (fingerprint(source), fingerprint(target), fingerprint(scope)):
        raise ValueError("checkpoint circuit original binding changed")
    metadata, _ = _checked_context(target, source, scope)
    plan = {"cap": schedule["cap"], "moves": schedule["events"]}
    observed = validate_allocations(scope, plan)
    if any(schedule["resources"][key] != value for key, value in observed.items()):
        raise ValueError("checkpoint observed allocation ledger differs from circuit")
    q, w = observed["logical_qubits"], scope["word_width"]
    state = np.zeros(q, dtype=np.uint8)
    value_wires = {}
    for node in scope["inputs"]:
        raw = int(inputs[node["name"]])
        if not 0 <= raw < 1 << node["bits"]:
            raise ValueError("external input violates original word declaration")
        wires = np.arange(node["offset"], node["offset"] + node["width"], dtype=np.int64)
        state[wires] = [(raw >> bit) & 1 for bit in range(node["width"])]
        value_wires[node["id"]] = wires
    output_specs = {o["name"]: o for o in scope["outputs"]}
    for output in output_specs.values():
        raw = int((initial_outputs or {}).get(output["name"], 0))
        if not 0 <= raw < 1 << w:
            raise ValueError("initial output does not fit full native word")
        state[output["offset"] : output["offset"] + w] = [(raw >> bit) & 1 for bit in range(w)]
    before, groups, cache = state.copy(), _groups(scope), {}
    library = resolve_library(source)
    computed = erased = checked_values = 0
    for event in schedule["events"]:
        if event["kind"] == "copy_output":
            name = event.get("outputname", event.get("name"))
            output, value = output_specs[name], event["value"]
            wires = value_wires[value]
            state[output["offset"] : output["offset"] + len(wires)] ^= state[wires]
            continue
        group = groups[event["group"]]
        entry = metadata[group["leaf"]]
        if group["leaf"] not in cache:
            path = library / entry["gate_file"]
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest != entry["sha256"] or digest != schedule["native_gate_sha256"][group["leaf"]]:
                raise ValueError("checkpoint frozen gate hash mismatch during replay")
            cache[group["leaf"]] = np.load(path, mmap_mode="r")
        physical = _spans(event["storage"], group["width"], scope["fixed_floor"], schedule["cap"])
        private = _spans(
            event["private_storage"], group["private"], scope["fixed_floor"], schedule["cap"]
        )
        produced = _split_value_wires(group, physical)
        inverse = event["kind"] == "erase"
        if not inverse and np.any(state[physical]):
            raise AssertionError("compute destination is dirty before native invocation")
        if np.any(state[private]):
            raise AssertionError("native private workspace is dirty before invocation")
        mapping = np.full(entry["resources"]["qubits"], -1, dtype=np.int64)
        for value, register in zip(group["out"], entry["outs"], strict=True):
            mapping[register[: len(produced[value])]] = produced[value]
        remaining = np.flatnonzero(mapping < 0)
        if len(remaining) != len(private):
            raise ValueError("native unused output/input scratch omitted")
        mapping[remaining] = private
        if len(set(map(int, mapping))) != len(mapping):
            raise ValueError("native leaf mapping aliases wires")
        for value, register in zip(group["args"], entry["args"], strict=True):
            wires = value_wires[value]
            state[mapping[register[: len(wires)]]] ^= state[wires]
        mapped_gates(cache[group["leaf"]], state, mapping, inverse)
        for value, register in zip(group["args"], entry["args"], strict=True):
            wires = value_wires[value]
            state[mapping[register[: len(wires)]]] ^= state[wires]
        if np.any(state[private]):
            raise AssertionError("native scratch/interface copies/high outputs did not restore")
        if inverse:
            if np.any(state[physical]):
                raise AssertionError("actual erase left checkpoint output dirty")
            for value in group["out"]:
                del value_wires[value]
            erased += 1
        else:
            value_wires.update(produced)
            if expected_trace is not None:
                for value, wires in produced.items():
                    actual = sum(int(state[wire]) << bit for bit, wire in enumerate(wires))
                    if actual != int(expected_trace[value]):
                        raise AssertionError(
                            "checkpoint value differs from original exact financial trace"
                        )
                    checked_values += 1
            computed += 1
    values = {
        name: sum(int(state[output["offset"] + bit]) << bit for bit in range(w))
        for name, output in output_specs.items()
    }
    for output in output_specs.values():
        state[output["offset"] : output["offset"] + w] = before[
            output["offset"] : output["offset"] + w
        ]
    return {
        "values": values,
        "all_input_and_workspace_bits_restored": bool(np.array_equal(state, before)),
        "compute_invocations": computed,
        "erase_invocations": erased,
        "original_trace_values_checked": checked_values,
        "full_native_output_xor_width": w,
        "observed_peak_live_qubits": observed["peak_live_qubits"],
        "observed_physical_qubits": observed["logical_qubits"],
    }
