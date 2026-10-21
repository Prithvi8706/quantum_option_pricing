"""Explicit wave schedules of immutable clean-XOR leaves with private scratch.

Independent leaves never share their private input/scratch/output wires. Shared
SSA controls are copied in distinct rounds. Inverse waves apply the same clean
XOR leaves again, in reverse dependency order; that implements the inverse on
the clean-workspace subspace without assuming a reversed gate-depth formula.
"""

from collections import Counter, defaultdict
import hashlib
import json

import numpy as np

from research.controlled_source_completion.compiler import mapped_gates, resolve_library


def entries(source):
    library = resolve_library(source)
    return {
        key: json.loads((library / (key + ".json")).read_text()) for key in source["library_keys"]
    }


def make_schedule(source, parallel_limit=None):
    if parallel_limit is not None and parallel_limit < 1:
        raise ValueError("parallel_limit must be positive or None")
    metadata = entries(source)
    w = source["word_width"]
    levels = {value: 0 for node in source["inputs"] for value in node["out"]}
    arrival = dict(levels)
    waves = defaultdict(list)
    for index, call in enumerate(source["forward_calls"]):
        level = 1 + max((levels[arg] for arg in call["args"]), default=0)
        cost = metadata[call["leaf"]]["resources"]["t_depth"]
        end = cost + max((arrival[arg] for arg in call["args"]), default=0)
        for value in call["out"]:
            if value in levels:
                raise ValueError("SSA output allocated twice")
            levels[value], arrival[value] = level, end
        waves[level].append(index)
    groups = []
    for wave, indices in sorted(waves.items()):
        indices.sort(
            key=lambda i: (-metadata[source["forward_calls"][i]["leaf"]]["resources"]["t_depth"], i)
        )
        limit = parallel_limit or len(indices)
        for offset in range(0, len(indices), limit):
            batch = indices[offset : offset + limit]
            calls = [source["forward_calls"][i] for i in batch]
            copy_depth = max(Counter(a for call in calls for a in call["args"]).values(), default=0)
            scratch, td, depth = 0, 0, 0
            for call in calls:
                r = metadata[call["leaf"]]["resources"]
                scratch += r["qubits"] - len(call["out"]) * w
                td = max(td, r["t_depth"])
                depth = max(depth, r["clifford_t_depth"])
            groups.append(
                dict(
                    wave=wave,
                    call_indices=batch,
                    private_scratch_qubits=scratch,
                    copy_rounds=copy_depth,
                    t_depth=td,
                    clifford_t_depth=depth + 2 * copy_depth,
                )
            )
    result = dict(source["resources"])
    scratch = max(g["private_scratch_qubits"] for g in groups)
    output_copy_depth = max(Counter(source["outputs"].values()).values(), default=0)
    result.update(
        logical_qubits=(source["values"] + len(source["outputs"])) * w + scratch,
        max_reused_scratch_qubits=scratch,
        t_depth=2 * sum(g["t_depth"] for g in groups),
        clifford_t_depth=2 * sum(g["clifford_t_depth"] for g in groups) + output_copy_depth,
        t_depth_schedule="Serial wave batches, disjoint private leaf workspaces; "
        "ASAP inside leaves, shared-control copies in separate rounds.",
    )
    return dict(
        format="clean-xor-parallel-wave-schedule-v1",
        parallel_limit=parallel_limit,
        groups=groups,
        resources=result,
        dependency_only_forward_t_depth=max(arrival[v] for v in source["outputs"].values()),
        dependency_bound_scope="Weighted clean-leaf DAG bound for this fixed leaf "
        "decomposition; omits resource constraints and is not "
        "a lower bound on arbitrary implementations.",
        inverse="Reverse wave groups, repeat the clean XOR leaves with unchanged "
        "argument binding. Leaf scratch starts/ends zero in each batch.",
        routing="All-to-all logical scheduling; physical layout/routing unproved.",
    )


def apply_half(source, schedule, state, base=0, inverse=False, cache=None):
    cache = {} if cache is None else cache
    library = resolve_library(source)
    w = source["word_width"]
    scratch_base = base + (source["values"] + len(source["outputs"])) * w
    groups = reversed(schedule["groups"]) if inverse else schedule["groups"]
    for group in groups:
        bindings = []
        cursor = scratch_base
        for index in group["call_indices"]:
            call = source["forward_calls"][index]
            key = (library, call["leaf"])
            if key not in cache:
                entry = json.loads((library / (call["leaf"] + ".json")).read_text())
                file = library / entry["gate_file"]
                if hashlib.sha256(file.read_bytes()).hexdigest() != entry["sha256"]:
                    raise ValueError("Leaf hash mismatch")
                cache[key] = (entry, np.load(file, mmap_mode="r"))
            entry, gates = cache[key]
            arity, nout = len(call["args"]), len(call["out"])
            mapping = np.empty(entry["resources"]["qubits"], np.int64)
            for i in range(len(mapping)):
                if arity * w <= i < (arity + nout) * w:
                    mapping[i] = base + call["out"][(i - arity * w) // w] * w + i % w
                else:
                    mapping[i] = cursor + i - (nout * w if i >= (arity + nout) * w else 0)
            bindings.append((call, gates, mapping, cursor))
            cursor += entry["resources"]["qubits"] - nout * w
        assert cursor - scratch_base == group["private_scratch_qubits"]
        # The CPU executor serializes these copies; the recipe permits exactly
        # copy_rounds disjoint-wire layers, paying every shared-control occurrence.
        for call, _, _, cursor in bindings:
            for a, value in enumerate(call["args"]):
                state[cursor + a * w : cursor + (a + 1) * w] ^= state[
                    base + value * w : base + (value + 1) * w
                ]
        for _, gates, mapping, _ in bindings:
            mapped_gates(gates, state, mapping, False)
        for call, _, _, cursor in bindings:
            for a, value in enumerate(call["args"]):
                state[cursor + a * w : cursor + (a + 1) * w] ^= state[
                    base + value * w : base + (value + 1) * w
                ]


def execute(source, schedule, inputs, initial_outputs=None):
    w = source["word_width"]
    output_base = source["values"] * w
    state = np.zeros(schedule["resources"]["logical_qubits"], np.uint8)
    for node in source["inputs"]:
        raw = inputs[node["params"]["name"]]
        for bit in range(w):
            state[node["out"][0] * w + bit] = (raw >> bit) & 1
    for i, name in enumerate(source["outputs"]):
        raw = (initial_outputs or {}).get(name, 0)
        for bit in range(w):
            state[output_base + i * w + bit] = (raw >> bit) & 1
    before, cache = state.copy(), {}
    apply_half(source, schedule, state, cache=cache)
    for i, value in enumerate(source["outputs"].values()):
        state[output_base + i * w : output_base + (i + 1) * w] ^= state[value * w : (value + 1) * w]
    apply_half(source, schedule, state, inverse=True, cache=cache)
    observed = {
        name: sum(int(state[output_base + i * w + bit]) << bit for bit in range(w))
        for i, name in enumerate(source["outputs"])
    }
    state[output_base : output_base + len(source["outputs"]) * w] = before[
        output_base : output_base + len(source["outputs"]) * w
    ]
    return dict(
        values=observed, all_input_and_workspace_bits_restored=bool(np.array_equal(state, before))
    )
