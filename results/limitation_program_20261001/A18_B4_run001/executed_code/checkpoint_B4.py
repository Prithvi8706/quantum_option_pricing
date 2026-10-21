"""One paid clean-boundary subroutine embedded in the unchanged full source.

Retain-all external SSA values and serial external leaves provide a matched
control. The same private bank is reused by the extracted subroutine and the
outside leaves, so only a saving at the real global peak saves global qubits.
"""

from __future__ import annotations

from collections import Counter
import hashlib

import numpy as np

from research.controlled_source_completion.compiler import mapped_gates, resolve_library
from research.limitation_program_20261001.checkpoint_circuit import (
    FORMAT as SUBROUTINE_FORMAT,
    COUNT_FIELDS,
    _checked_context,
    _groups,
    _native_cost,
    _spans,
    _split_value_wires,
    fingerprint,
    validate_allocations,
)


FORMAT = "paid-reversible-full-financial-integration-v1"


def _binding(target, source, scope, subroutine):
    metadata, storage = _checked_context(target, source, scope)
    if subroutine.get("format") != SUBROUTINE_FORMAT:
        raise ValueError("full-source integration requires the frozen checkpoint circuit")
    if (
        subroutine["source_fingerprint"],
        subroutine["target_fingerprint"],
        subroutine["scope_fingerprint"],
    ) != (fingerprint(source), fingerprint(target), fingerprint(scope)):
        raise ValueError("full-source integration subroutine binding changed")
    observed = validate_allocations(
        scope,
        {
            "cap": subroutine["cap"],
            "moves": subroutine["events"],
        },
    )
    if observed["logical_qubits"] != subroutine["resources"]["logical_qubits"]:
        raise ValueError("subroutine memory ledger does not match emitted lifetimes")
    chosen = {g["call_index"] for g in scope["groups"]}
    outside = [(i, c) for i, c in enumerate(source["forward_calls"]) if i not in chosen]
    selected_values = {v for g in scope["groups"] for v in g["out"]}
    boundary_values = {o["value"] for o in scope["outputs"]}
    for _, call in outside:
        for value in call["args"]:
            if value in selected_values and value not in boundary_values:
                raise ValueError("full-source subroutine omits an outgoing financial edge")
    for value in source["outputs"].values():
        if value in selected_values and value not in boundary_values:
            raise ValueError("full-source subroutine omits a named financial output")
    return metadata, storage, outside


def make_b4_schedule(target, source, scope, subroutine):
    """Measure one fixed full-source embedding without adding extra portfolios."""
    metadata, storage, outside = _binding(target, source, scope, subroutine)
    widths, w = storage["widths"], source["word_width"]
    cursor = scope["fixed_floor"]
    outputs = []
    for name, value in source["outputs"].items():
        outputs.append({"name": name, "value": value, "offset": cursor, "width": w})
        cursor += w
    floor = cursor
    allocations = []
    for index, call in outside:
        output_bindings = []
        for value in call["out"]:
            output_bindings.append({"value": value, "offset": cursor, "width": widths[value]})
            cursor += widths[value]
        entry = metadata[call["leaf"]]
        private = entry["resources"]["qubits"] - sum(widths[v] for v in call["out"])
        allocations.append(
            {
                "call_index": index,
                "leaf": call["leaf"],
                "args": call["args"],
                "out": call["out"],
                "output_bindings": output_bindings,
                "private": private,
            }
        )
    private_base = cursor
    sub_private = subroutine["resources"]["logical_qubits"] - scope["fixed_floor"]
    outside_private = max((a["private"] for a in allocations), default=0)
    private_width = max(sub_private, outside_private)
    library, costs, hashes = resolve_library(source), {}, {}
    for key in sorted({c["leaf"] for _, c in outside}):
        entry = metadata[key]
        path = library / entry["gate_file"]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != entry["sha256"]:
            raise ValueError("full-source unchanged native leaf hash mismatch")
        gates = np.load(path, mmap_mode="r")
        forward = _native_cost(gates, entry["resources"]["qubits"], False)
        reverse = _native_cost(gates, entry["resources"]["qubits"], True)
        if any(forward[k] != entry["resources"][k] for k in forward):
            raise ValueError("full-source unchanged native leaf actual cost differs")
        costs[key] = {"compute": forward, "erase": reverse}
        hashes[key] = digest
    counts = Counter(
        {
            field: 2 * subroutine["resources"].get(field, 0)
            for field in (*COUNT_FIELDS, "t_depth", "clifford_t_depth")
        }
    )
    external_argument_copy_cx, external_argument_copy_depth = 0, 0
    for _, call in outside:
        for direction in ("compute", "erase"):
            for field, count in costs[call["leaf"]][direction].items():
                counts[field] += count
        copies = 4 * sum(widths[v] for v in call["args"])
        copy_depth = 4 * max(Counter(call["args"]).values(), default=0)
        for field in ("source_gates", "cx", "clifford_cx"):
            counts[field] += copies
        counts["clifford_t_depth"] += copy_depth
        external_argument_copy_cx += copies
        external_argument_copy_depth += copy_depth
    output_copies = sum(widths[v] for v in source["outputs"].values())
    for field in ("source_gates", "cx", "clifford_cx"):
        counts[field] += output_copies
    # Named copies are explicit serial layers, including aliases.
    counts["clifford_t_depth"] += len(outputs)
    resources = dict(counts)
    resources.update(
        logical_qubits=private_base + private_width,
        peak_live_qubits=private_base + private_width,
        fixed_floor_qubits=floor,
        retained_outside_ssa_qubits=private_base - floor,
        max_reused_scratch_qubits=private_width,
        extracted_transient_workspace_qubits=sub_private,
        outside_private_leaf_workspace_qubits=outside_private,
        random_hadamards=sum(n["params"]["bits"] for n in source["inputs"]),
    )
    return {
        "format": FORMAT,
        "target_fingerprint": fingerprint(target),
        "source_fingerprint": fingerprint(source),
        "scope_fingerprint": fingerprint(scope),
        "subroutine_fingerprint": fingerprint(subroutine),
        "outside_allocations": allocations,
        "named_outputs": outputs,
        "private_base": private_base,
        "private_width": private_width,
        "subroutine_dynamic_base": private_base,
        "sequence": [
            "clean extracted boundary subroutine",
            "outside forward calls",
            "copy named financial output to dirty full-native destination",
            "literal inverse outside calls",
            "repeat clean boundary subroutine",
        ],
        "resources": resources,
        "native_leaf_costs": costs,
        "native_gate_sha256": hashes,
        "subroutine_invocations": 2,
        "external_forward_calls": len(outside),
        "copy_ledger": {
            "subroutine_all_copies_cx": 2 * subroutine["argument_and_output_copy_cx"],
            "outside_argument_copies_cx": external_argument_copy_cx,
            "outside_argument_copy_depth": external_argument_copy_depth,
            "full_named_output_copy_cx": output_copies,
        },
        "allocation": (
            "All original random inputs and full-native boundary/named output registers retained; "
            "outside SSA retained with original compact widths; extracted dynamic workspace and "
            "outside native private workspace reuse one physical bank"
        ),
        "depth_convention": (
            "Serial invocation barriers, exact seven-T Toffoli; forward/literal-inverse leaf ASAP "
            "depths measured separately; every recomputation and copy charged"
        ),
        "physical_runtime_claim": False,
    }


def replay_b4(
    target, source, scope, subroutine, schedule, inputs, initial_outputs=None, expected_trace=None
):
    """Replay one full original financial target with clean boundary restoration."""
    metadata, storage, outside = _binding(target, source, scope, subroutine)
    if schedule.get("format") != FORMAT or (
        schedule["target_fingerprint"],
        schedule["source_fingerprint"],
        schedule["scope_fingerprint"],
        schedule["subroutine_fingerprint"],
    ) != (fingerprint(target), fingerprint(source), fingerprint(scope), fingerprint(subroutine)):
        raise ValueError("full financial checkpoint circuit binding changed")
    w, widths = source["word_width"], storage["widths"]
    # Reconstruct the fixed outside allocation instead of trusting serialized
    # register offsets, leaf names or compact output widths during execution.
    cursor, expected_outputs = scope["fixed_floor"], []
    for name, value in source["outputs"].items():
        expected_outputs.append({"name": name, "value": value, "offset": cursor, "width": w})
        cursor += w
    if schedule["named_outputs"] != expected_outputs:
        raise ValueError("full-source named output allocation changed")
    expected_allocations = []
    for index, call in outside:
        bindings = []
        for value in call["out"]:
            bindings.append({"value": value, "offset": cursor, "width": widths[value]})
            cursor += widths[value]
        private = metadata[call["leaf"]]["resources"]["qubits"] - sum(
            widths[v] for v in call["out"]
        )
        expected_allocations.append(
            {
                "call_index": index,
                "leaf": call["leaf"],
                "args": call["args"],
                "out": call["out"],
                "output_bindings": bindings,
                "private": private,
            }
        )
    expected_private = max(
        subroutine["resources"]["logical_qubits"] - scope["fixed_floor"],
        max((a["private"] for a in expected_allocations), default=0),
    )
    if schedule["outside_allocations"] != expected_allocations:
        raise ValueError("full-source original call or retained SSA allocation changed")
    if (
        schedule["private_base"],
        schedule["private_width"],
        schedule["resources"]["logical_qubits"],
    ) != (cursor, expected_private, cursor + expected_private):
        raise ValueError("full-source physical peak or private bank changed")
    state = np.zeros(schedule["resources"]["logical_qubits"], dtype=np.uint8)
    fixed_input_wires = {}
    for node in scope["inputs"]:
        raw = int(inputs[node["name"]])
        if not 0 <= raw < 1 << node["bits"]:
            raise ValueError("input violates original external declaration")
        wires = np.arange(node["offset"], node["offset"] + node["width"], dtype=np.int64)
        state[wires] = [(raw >> bit) & 1 for bit in range(node["width"])]
        fixed_input_wires[node["id"]] = wires
    for output in schedule["named_outputs"]:
        raw = int((initial_outputs or {}).get(output["name"], 0))
        if not 0 <= raw < 1 << w:
            raise ValueError("dirty financial output must fit the full native word")
        state[output["offset"] : output["offset"] + w] = [(raw >> bit) & 1 for bit in range(w)]
    before, library, cache = state.copy(), resolve_library(source), {}
    groups = _groups(scope)
    base = schedule["private_base"]
    trace_values_checked = 0
    native_invocations = 0

    def gates_for(key):
        if key not in cache:
            entry = metadata[key]
            path = library / entry["gate_file"]
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            expected = subroutine["native_gate_sha256"].get(
                key, schedule["native_gate_sha256"].get(key)
            )
            if digest != entry["sha256"] or digest != expected:
                raise ValueError("actual full-source gate array changed before replay")
            cache[key] = np.load(path, mmap_mode="r")
        return cache[key]

    def invoke(key, args, out, produced, value_wires, private, inverse):
        nonlocal native_invocations, trace_values_checked
        entry = metadata[key]
        mapping = np.full(entry["resources"]["qubits"], -1, dtype=np.int64)
        for value, register in zip(out, entry["outs"], strict=True):
            mapping[register[: len(produced[value])]] = produced[value]
            if not inverse and np.any(state[produced[value]]):
                raise AssertionError("full-source compute destination is dirty")
        remaining = np.flatnonzero(mapping < 0)
        if len(remaining) != len(private) or np.any(state[private]):
            raise AssertionError("full-source native private bank invalid or dirty")
        mapping[remaining] = private
        if len(set(map(int, mapping))) != len(mapping) or max(mapping, default=-1) >= len(state):
            raise ValueError("full-source native mapping aliases or exceeds real allocation")
        for value, register in zip(args, entry["args"], strict=True):
            wires = value_wires[value]
            state[mapping[register[: len(wires)]]] ^= state[wires]
        mapped_gates(gates_for(key), state, mapping, inverse)
        for value, register in zip(args, entry["args"], strict=True):
            wires = value_wires[value]
            state[mapping[register[: len(wires)]]] ^= state[wires]
        if np.any(state[private]):
            raise AssertionError("full-source native inputs/scratch/high outputs did not clean")
        for value, wires in produced.items():
            actual = sum(int(state[wire]) << bit for bit, wire in enumerate(wires))
            if inverse and actual:
                raise AssertionError("full-source actual erase left output dirty")
            if not inverse and expected_trace is not None:
                if actual != int(expected_trace[value]):
                    raise AssertionError("full-source financial intermediate changed")
                trace_values_checked += 1
        native_invocations += 1

    def apply_subroutine():
        value_wires = dict(fixed_input_wires)
        output_bindings = {o["name"]: o for o in scope["outputs"]}

        def translate(wires):
            return np.where(
                wires < scope["fixed_floor"], wires, base + wires - scope["fixed_floor"]
            )

        for event in subroutine["events"]:
            if event["kind"] == "copy_output":
                name = event.get("outputname", event.get("name"))
                output = output_bindings[name]
                wires = value_wires[event["value"]]
                state[output["offset"] : output["offset"] + len(wires)] ^= state[wires]
                continue
            group = groups[event["group"]]
            physical = translate(
                _spans(event["storage"], group["width"], scope["fixed_floor"], subroutine["cap"])
            )
            private = translate(
                _spans(
                    event["private_storage"],
                    group["private"],
                    scope["fixed_floor"],
                    subroutine["cap"],
                )
            )
            produced = _split_value_wires(group, physical)
            inverse = event["kind"] == "erase"
            invoke(
                group["leaf"], group["args"], group["out"], produced, value_wires, private, inverse
            )
            if inverse:
                for value in group["out"]:
                    del value_wires[value]
            else:
                value_wires.update(produced)
        if np.any(state[base:]):
            raise AssertionError("extracted subroutine did not clean global private bank")

    value_wires = dict(fixed_input_wires)
    for output in scope["outputs"]:
        value_wires.setdefault(
            output["value"],
            np.arange(output["offset"], output["offset"] + widths[output["value"]], dtype=np.int64),
        )
    allocations = schedule["outside_allocations"]
    if [a["call_index"] for a in allocations] != [i for i, _ in outside]:
        raise ValueError("full-source external invocation set changed")
    for allocation in allocations:
        for output in allocation["output_bindings"]:
            value_wires[output["value"]] = np.arange(
                output["offset"], output["offset"] + output["width"], dtype=np.int64
            )
    apply_subroutine()
    for inverse, sequence in ((False, allocations), (True, list(reversed(allocations)))):
        if inverse:
            for output in schedule["named_outputs"]:
                wires = value_wires[output["value"]]
                state[output["offset"] : output["offset"] + len(wires)] ^= state[wires]
        for allocation in sequence:
            produced = {v: value_wires[v] for v in allocation["out"]}
            private = np.arange(base, base + allocation["private"], dtype=np.int64)
            invoke(
                allocation["leaf"],
                allocation["args"],
                allocation["out"],
                produced,
                value_wires,
                private,
                inverse,
            )
    apply_subroutine()
    values = {
        output["name"]: sum(int(state[output["offset"] + bit]) << bit for bit in range(w))
        for output in schedule["named_outputs"]
    }
    for output in schedule["named_outputs"]:
        state[output["offset"] : output["offset"] + w] = before[
            output["offset"] : output["offset"] + w
        ]
    return {
        "values": values,
        "all_input_and_workspace_bits_restored": bool(np.array_equal(state, before)),
        "boundary_registers_restored": not bool(
            np.any(state[sum(n["width"] for n in scope["inputs"]) : scope["fixed_floor"]])
        ),
        "original_trace_values_checked": trace_values_checked,
        "native_gate_invocations": native_invocations,
        "full_native_output_xor_width": w,
        "observed_physical_qubits": len(state),
    }
