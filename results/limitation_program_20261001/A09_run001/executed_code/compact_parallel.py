"""Exact compact SSA bindings with capped parallel clean-leaf schedules.

Only proved-zero high SSA bits are omitted. Every omitted leaf output bit has
a distinct private wire; the original arithmetic leaves are used unchanged.
"""

from collections import Counter, defaultdict
import hashlib
import json

import numpy as np

from research.controlled_priority_completion.parallel_source import entries
from research.controlled_source_completion.compact_storage import active_masks
from research.controlled_source_completion.compiler import mapped_gates, resolve_library
from research.controlled_source_completion.primitives import LOOKUP_LOWERING


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def _storage(target, source, metadata):
    w = source["word_width"]
    if target["width"] != w or target["fraction_bits"] != source["fraction_bits"]:
        raise ValueError("target/source precision mismatch")
    nodes = [n for n in target["nodes"] if n["op"] != "input"]
    calls = source["forward_calls"]
    if len(nodes) != len(calls) or any(
        (n["args"], n["out"]) != (c["args"], c["out"]) for n, c in zip(nodes, calls)
    ):
        raise ValueError("target/source call binding mismatch")
    if source["inputs"] != [n for n in target["nodes"] if n["op"] == "input"]:
        raise ValueError("target/source input mismatch")
    if source["outputs"] != target["outputs"]:
        raise ValueError("target/source output mismatch")
    masks, reasons = active_masks(target)
    signed_context = None
    if any("signed_upper_bits" in entry.get("input_contract", {}) for entry in metadata.values()):
        from research.limitation_program_20261001.prove_log_exponent import SSAContext

        signed_context = SSAContext(target)
    if set(masks) != set(range(source["values"])):
        raise ValueError("target/source SSA allocation mismatch")
    widths = [max(1, masks[v].bit_length()) for v in range(source["values"])]
    offsets, retained = [], 0
    for width in widths:
        offsets.append(retained)
        retained += width
    for node, call in zip(nodes, calls):
        entry = metadata[call["leaf"]]
        if entry["op"] != node["op"] or entry["params"] != node["params"]:
            raise ValueError("target/source leaf semantics mismatch")
        if node["op"] == "lookup":
            spec = dict(
                op="lookup",
                width=w,
                fraction_bits=source["fraction_bits"],
                params=node["params"],
                table=target["tables"][node["params"]["table"]],
            )
            keys = set()
            for candidate in (spec, dict(spec, lowering=LOOKUP_LOWERING)):
                encoded = json.dumps(candidate, sort_keys=True, separators=(",", ":")).encode()
                keys.add(hashlib.sha256(encoded).hexdigest()[:20])
            if call["leaf"] not in keys:
                raise ValueError("lookup table does not match the compiled leaf")
        if len(entry["args"]) != len(call["args"]) or len(entry["outs"]) != len(call["out"]):
            raise ValueError("leaf register arity mismatch")
        registers = entry["args"] + entry["outs"]
        wires = [q for reg in registers for q in reg]
        if len(wires) != len(set(wires)) or any(
            not 0 <= q < entry["resources"]["qubits"] for q in wires
        ):
            raise ValueError("leaf register wire collision or invalid wire")
        for value, register in zip(call["args"] + call["out"], registers):
            if not widths[value] <= len(register) <= w:
                raise ValueError("leaf register omits an active bit")
        contract = entry.get("input_contract", {})
        if set(contract) - {"zero_low_bits", "signed_upper_bits"}:
            raise ValueError("unsupported leaf input contract")
        if "zero_low_bits" in contract:
            zero = contract["zero_low_bits"]
            if type(zero) is not int or not 0 <= zero <= w or len(call["args"]) != 1:
                raise ValueError("invalid zero-low leaf contract")
            if masks[call["args"][0]] & ((1 << zero) - 1):
                raise ValueError("leaf zero-low contract is not proved by this graph")
        if "signed_upper_bits" in contract:
            from research.limitation_program_20261001.prove_log_exponent import prove_log_site

            if contract != {"zero_low_bits": 40, "signed_upper_bits": 7}:
                raise ValueError("unsupported signed upper-word contract")
            index = signed_context.locations[node["out"][0]]
            if prove_log_site(signed_context, index) is None:
                raise ValueError("signed upper-word contract is not proved by this graph")
    return dict(
        widths=widths,
        offsets=offsets,
        retained_ssa_qubits=retained,
        proof_masks=[masks[v] for v in range(source["values"])],
        proof_reasons=[reasons[v] for v in range(source["values"])],
    )


def make_compact_schedule(target, source, qubit_cap):
    """First-fit packing at each dependency wave using actual compact bindings."""
    if type(qubit_cap) is not int or qubit_cap < 0:
        raise ValueError("qubit cap must be a nonnegative integer")
    metadata = entries(source)
    storage = _storage(target, source, metadata)
    widths, w = storage["widths"], source["word_width"]
    retained = storage["retained_ssa_qubits"] + len(source["outputs"]) * w
    capacity = qubit_cap - retained
    if capacity < 0:
        raise ValueError("qubit cap cannot fit retained SSA and named outputs")
    levels = {v: 0 for n in source["inputs"] for v in n["out"]}
    arrivals, waves = dict(levels), defaultdict(list)
    calls = source["forward_calls"]
    for index, call in enumerate(calls):
        level = 1 + max((levels[v] for v in call["args"]), default=0)
        end = metadata[call["leaf"]]["resources"]["t_depth"] + max(
            (arrivals[v] for v in call["args"]),
            default=0,
        )
        for v in call["out"]:
            if v in levels:
                raise ValueError("SSA output allocated twice")
            levels[v], arrivals[v] = level, end
        waves[level].append(index)
    groups = []
    for wave, indices in sorted(waves.items()):
        indices.sort(key=lambda i: (-metadata[calls[i]["leaf"]]["resources"]["t_depth"], i))
        batches = []
        for index in indices:
            call = calls[index]
            scratch = metadata[call["leaf"]]["resources"]["qubits"] - sum(
                widths[v] for v in call["out"]
            )
            if scratch > capacity:
                raise ValueError("qubit cap cannot fit a single required leaf")
            batch = next((b for b in batches if b["scratch"] + scratch <= capacity), None)
            if batch is None:
                batch = dict(indices=[], scratch=0)
                batches.append(batch)
            batch["indices"].append(index)
            batch["scratch"] += scratch
        for batch in batches:
            selected = [calls[i] for i in batch["indices"]]
            rs = [metadata[c["leaf"]]["resources"] for c in selected]
            copies = max(Counter(v for c in selected for v in c["args"]).values(), default=0)
            groups.append(
                dict(
                    wave=wave,
                    call_indices=batch["indices"],
                    private_scratch_qubits=batch["scratch"],
                    copy_rounds=copies,
                    t_depth=max(r["t_depth"] for r in rs),
                    clifford_t_depth=max(r["clifford_t_depth"] for r in rs) + 2 * copies,
                )
            )
    compact_copies = 4 * sum(sum(widths[v] for v in c["args"]) for c in calls)
    compact_copies += sum(widths[v] for v in source["outputs"].values())
    baseline_copies = 4 * sum(len(c["args"]) * w for c in calls) + len(source["outputs"]) * w
    resources = dict(source["resources"])
    for field in ("source_gates", "cx", "clifford_cx"):
        resources[field] += compact_copies - baseline_copies
    scratch = max((g["private_scratch_qubits"] for g in groups), default=0)
    output_depth = max(Counter(source["outputs"].values()).values(), default=0)
    resources.update(
        logical_qubits=retained + scratch,
        max_reused_scratch_qubits=scratch,
        t_depth=2 * sum(g["t_depth"] for g in groups),
        clifford_t_depth=2 * sum(g["clifford_t_depth"] for g in groups) + output_depth,
        t_depth_schedule="Compact exact SSA; memory-capped independent leaf batches",
    )
    return dict(
        format="compact-clean-xor-capped-wave-schedule-v1",
        **storage,
        source_fingerprint=fingerprint(source),
        target_fingerprint=fingerprint(target),
        qubit_cap=qubit_cap,
        groups=groups,
        resources=resources,
        argument_and_output_copy_cx=compact_copies,
        baseline_argument_and_output_copy_cx=baseline_copies,
        dependency_only_forward_t_depth=max(
            (arrivals[v] for v in source["outputs"].values()), default=0
        ),
        packing="First-fit decreasing leaf T-depth within each dependency wave",
        inverse="Reverse batches; repeat clean XOR leaves with identical bindings",
        routing="All-to-all logical schedule; physical layout and routing unproved",
        input_contract="Nonnegative raw bit patterns within each declared input bit width",
    )


def execute_compact_parallel(target, source, schedule, inputs, initial_outputs=None):
    """Replay original emitted gates with disjoint private wires in every batch."""
    if schedule["source_fingerprint"] != fingerprint(source) or schedule[
        "target_fingerprint"
    ] != fingerprint(target):
        raise ValueError("schedule does not match target/source fingerprints")
    metadata = entries(source)
    storage = _storage(target, source, metadata)
    if any(schedule[k] != v for k, v in storage.items()):
        raise ValueError("schedule storage proof mismatch")
    widths, offsets, w = storage["widths"], storage["offsets"], source["word_width"]
    output_base = storage["retained_ssa_qubits"]
    scratch_base = output_base + len(source["outputs"]) * w
    state = np.zeros(schedule["resources"]["logical_qubits"], np.uint8)
    for node in source["inputs"]:
        value = int(inputs[node["params"]["name"]])
        if not 0 <= value < (1 << node["params"]["bits"]):
            raise ValueError("input violates bit-width promise")
        v = node["out"][0]
        for bit in range(widths[v]):
            state[offsets[v] + bit] = (value >> bit) & 1
    for index, name in enumerate(source["outputs"]):
        value = (initial_outputs or {}).get(name, 0)
        for bit in range(w):
            state[output_base + index * w + bit] = (value >> bit) & 1
    before, library, cache = state.copy(), resolve_library(source), {}

    def apply(groups):
        for group in groups:
            cursor, bindings = scratch_base, []
            for index in group["call_indices"]:
                call = source["forward_calls"][index]
                entry = metadata[call["leaf"]]
                if call["leaf"] not in cache:
                    file = library / entry["gate_file"]
                    if hashlib.sha256(file.read_bytes()).hexdigest() != entry["sha256"]:
                        raise ValueError("leaf gate hash mismatch")
                    cache[call["leaf"]] = np.load(file, mmap_mode="r")
                mapping = np.full(entry["resources"]["qubits"], -1, np.int64)
                for v, register in zip(call["out"], entry["outs"]):
                    mapping[register[: widths[v]]] = np.arange(offsets[v], offsets[v] + widths[v])
                private = np.flatnonzero(mapping < 0)
                mapping[private] = np.arange(cursor, cursor + len(private))
                bindings.append((call, entry, cache[call["leaf"]], mapping))
                cursor += len(private)
            if cursor - scratch_base != group["private_scratch_qubits"] or cursor > len(state):
                raise ValueError("batch scratch or capacity mismatch")
            for call, entry, _, mapping in bindings:
                for v, register in zip(call["args"], entry["args"]):
                    state[mapping[register[: widths[v]]]] ^= state[
                        offsets[v] : offsets[v] + widths[v]
                    ]
            for _, _, gates, mapping in bindings:
                mapped_gates(gates, state, mapping, False)
            for call, entry, _, mapping in bindings:
                for v, register in zip(call["args"], entry["args"]):
                    state[mapping[register[: widths[v]]]] ^= state[
                        offsets[v] : offsets[v] + widths[v]
                    ]
            if np.any(state[scratch_base:]):
                raise AssertionError("storage proof or leaf violated clean private workspace")

    apply(schedule["groups"])
    for index, v in enumerate(source["outputs"].values()):
        state[output_base + index * w : output_base + index * w + widths[v]] ^= state[
            offsets[v] : offsets[v] + widths[v]
        ]
    apply(reversed(schedule["groups"]))
    values = {
        name: sum(int(state[output_base + index * w + bit]) << bit for bit in range(w))
        for index, name in enumerate(source["outputs"])
    }
    state[output_base:scratch_base] = before[output_base:scratch_base]
    return dict(
        values=values, all_input_and_workspace_bits_restored=bool(np.array_equal(state, before))
    )
