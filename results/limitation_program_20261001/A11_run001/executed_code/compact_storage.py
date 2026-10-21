"""Exact variable-width SSA storage for the existing clean XOR leaves.

High output bits proved zero use private temporary wires, never aliased wires.
Leaves keep their exact 72-bit arithmetic. This reduces retained storage and
argument copies, not arithmetic precision or T counts. Input promises are
explicitly enforced by the executor.
"""

import json
import hashlib
from collections import Counter

import numpy as np

from research.controlled_source_completion.compiler import mapped_gates, resolve_library
from research.controlled_priority_completion.parallel_source import entries
from research.controlled_source_completion.primitives import compare
from research.journal_sprint.reversible_fixed_point import Program


def narrow_comparison(width):
    """Signed full-width comparison with an actual one-qubit XOR output."""
    p = Program(compact=True)
    a, b, flag = p.register(width), p.register(width), p.register(1)
    for operand in (a, b):
        p.gate(operand[-1])
    compare(p, a, b, flag[0])
    for operand in (a, b):
        p.gate(operand[-1])
    return p, [a, b], [flag]


def active_masks(target):
    """Conservative possible-one masks, proved compositionally, without sampling."""
    w = target["width"]
    full = (1 << w) - 1
    masks, reasons = {}, {}
    for node in target["nodes"]:
        op, params = node["op"], node["params"]
        args = [masks[a] for a in node["args"]]
        if op == "input":
            bits = params["bits"]
            if not 0 <= bits <= w:
                raise ValueError("input bit promise exceeds word width")
            values, reason = [(1 << bits) - 1], "input preparation promise"
        elif op == "const":
            values, reason = [params["value"] & full], "exact constant"
        elif op == "lt":
            values, reason = [1], "comparison is exactly 0 or 1"
        elif op == "msb":
            values, reason = [(1 << (w - 1).bit_length()) - 1], "index is in [0,width-1]"
        elif op == "positive":
            values, reason = [args[0] & (full >> 1)], "negative branch is zero"
        elif op == "select":
            values = [args[1] | args[2] if args[0] & 1 else args[2]]
            reason = "union of possible selected bit patterns"
        elif op == "bits":
            shift = params["shift"]
            value = args[0] >> shift if shift >= 0 else args[0] << -shift
            if shift > 0 and params.get("signed") and args[0] & (1 << (w - 1)):
                value |= full ^ ((1 << max(0, w - shift)) - 1)
            values = [value & ((1 << params["width"]) - 1) & full]
            reason = "exact bit extraction and possible sign extension"
        elif op == "lookup":
            values = [0] * len(node["out"])
            for row in target["tables"][params["table"]]:
                for j, value in enumerate(row):
                    values[j] |= value & full
            reason = "union of all literal table rows"
        elif op == "add" and sum(args) <= full:
            values = [(1 << sum(args).bit_length()) - 1]
            reason = "unsigned upper bound; modular addition has no overflow here"
        else:
            values, reason = [full] * len(node["out"]), "no narrowing proof used"
        for value_id, mask in zip(node["out"], values):
            masks[value_id], reasons[value_id] = mask, reason
    return masks, reasons


def compact_plan(target, source):
    """Plan a serial clean source; retain the original named full-width outputs."""
    masks, reasons = active_masks(target)
    w = source["word_width"]
    metadata = entries(source)
    widths = [max(1, masks[v].bit_length()) for v in range(source["values"])]
    offsets, cursor = [], 0
    for width in widths:
        offsets.append(cursor)
        cursor += width
    scratch = max(metadata[c["leaf"]]["resources"]["qubits"]
                  - sum(widths[v] for v in c["out"]) for c in source["forward_calls"])
    copies = 4 * sum(sum(widths[v] for v in c["args"]) for c in source["forward_calls"])
    copies += sum(widths[v] for v in source["outputs"].values())
    baseline_copies = 4 * sum(len(c["args"]) * w for c in source["forward_calls"])
    baseline_copies += len(source["outputs"]) * w
    return dict(format="compact-proved-ssa-storage-v1", widths=widths, offsets=offsets,
                proof_masks=[masks[v] for v in range(source["values"])],
                proof_reasons=[reasons[v] for v in range(source["values"])],
                retained_ssa_qubits=cursor, scratch_qubits=scratch,
                logical_qubits=cursor + len(source["outputs"]) * w + scratch,
                width_histogram=dict(Counter(widths)),
                argument_and_output_copy_cx=copies,
                baseline_argument_and_output_copy_cx=baseline_copies,
                t_count=source["resources"]["t_count"],
                t_depth=source["resources"]["t_depth"],
                schedule="Original serial leaf order; original within-leaf schedules",
                input_contract="Every input must be nonnegative and fit its declared bits")


def execute_compact(target, source, plan, inputs, initial_outputs=None):
    w = source["word_width"]
    widths, offsets = plan["widths"], plan["offsets"]
    output_base = plan["retained_ssa_qubits"]
    scratch_base = output_base + len(source["outputs"]) * w
    state = np.zeros(plan["logical_qubits"], np.uint8)
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
    before = state.copy()
    library, cache = resolve_library(source), {}

    def invoke(call, inverse):
        key = call["leaf"]
        if key not in cache:
            entry = json.loads((library / (key + ".json")).read_text())
            actual_hash = hashlib.sha256((library / entry["gate_file"]).read_bytes()).hexdigest()
            if actual_hash != entry["sha256"]:
                raise ValueError("leaf gate hash mismatch")
            cache[key] = entry, np.load(library / entry["gate_file"], mmap_mode="r")
        entry, gates = cache[key]
        arity = len(call["args"])
        mapping = np.full(entry["resources"]["qubits"], -1, np.int64)
        for index, v in enumerate(call["out"]):
            mapping[(arity + index) * w:(arity + index) * w + widths[v]] = np.arange(
                offsets[v], offsets[v] + widths[v],
            )
        private = np.flatnonzero(mapping < 0)
        mapping[private] = np.arange(scratch_base, scratch_base + len(private))
        for index, v in enumerate(call["args"]):
            state[mapping[index * w:index * w + widths[v]]] ^= state[
                offsets[v]:offsets[v] + widths[v]]
        mapped_gates(gates, state, mapping, inverse)
        for index, v in enumerate(call["args"]):
            state[mapping[index * w:index * w + widths[v]]] ^= state[
                offsets[v]:offsets[v] + widths[v]]
        if np.any(state[scratch_base:]):
            raise AssertionError("proof or leaf violated clean private workspace")

    for call in source["forward_calls"]:
        invoke(call, False)
    for index, v in enumerate(source["outputs"].values()):
        state[output_base + index * w:output_base + index * w + widths[v]] ^= state[
            offsets[v]:offsets[v] + widths[v]]
    for call in reversed(source["forward_calls"]):
        invoke(call, True)
    values = {name: sum(int(state[output_base + index * w + bit]) << bit for bit in range(w))
              for index, name in enumerate(source["outputs"])}
    restored = np.array_equal(state[:output_base], before[:output_base])
    return dict(values=values, inputs_and_workspace_restored=bool(restored and
                not np.any(state[scratch_base:])))
