"""Two immutable native loaders, full-word copies and exact packed basis replay.

Import performs no research-module imports, graph construction or numerical work.
The only numerical imports are lazy, after a prospective protocol is frozen.
"""

from __future__ import annotations

import ast
from collections import Counter
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
from math import isqrt
from pathlib import Path
import time

W, F, S = 72, 40, 1 << 40
MASK = (1 << W) - 1
CAP, CPU, ADMISSION, WALL = 45000, 300, 240, 600
CHUNK = 65536
LABELS = ("AS241_two_actual_scalar_invocations", "BoxMuller_one_actual_shared_pair")
PAIRS = (
    (0, 0),
    (0, 4294967295),
    (4294967295, 0),
    (4294967295, 4294967295),
    (322122546, 322122547),
    (3972844749, 3972844748),
    (2147483647, 2147483648),
    (1073741824, 3221225472),
)
DIRTY = (0, MASK)
LANES, LANE_MASK = 16, (1 << 16) - 1
FIELDS = ("x", "cx", "ccx", "source_gates", "t_count", "t_depth", "clifford_t_depth")
MACRO = (
    ("H", "target"),
    ("CX", "b", "target"),
    ("Tdg", "target"),
    ("CX", "a", "target"),
    ("T", "target"),
    ("CX", "b", "target"),
    ("Tdg", "target"),
    ("CX", "a", "target"),
    ("T", "b"),
    ("T", "target"),
    ("H", "target"),
    ("CX", "a", "b"),
    ("T", "a"),
    ("Tdg", "b"),
    ("CX", "a", "b"),
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def fingerprint(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


class BudgetCensoredError(RuntimeError):
    """Hard terminal censor; no retry, additional row or method switch."""


class Budget:
    def __init__(self, cpu=CPU, admission=ADMISSION, wall=WALL):
        self.started_cpu, self.started_wall = time.process_time(), time.monotonic()
        self.cpu, self.admission, self.wall = cpu, admission, wall

    def check(self, admission=False):
        elapsed_cpu = time.process_time() - self.started_cpu
        elapsed_wall = time.monotonic() - self.started_wall
        if elapsed_cpu > (self.admission if admission else self.cpu) or elapsed_wall > self.wall:
            raise BudgetCensoredError("Fixed paired-loader process CPU/admission/wall budget")
        return elapsed_cpu, elapsed_wall


def phase_premise(root):
    """Read applicable frozen phase proof and its literal macro; never evaluate it."""
    program = root / "results/limitation_program_20261001"
    proof = read(program / "A17_quantile_divider_run001/exact_CCX_phase_proof.json")
    require(
        canonical(proof)
        == canonical(
            [
                dict(input=k, output=k ^ (((k & 1) & ((k >> 1) & 1)) << 2), exact_nonzero_phase=1)
                for k in range(8)
            ]
        ),
        "Eight prior exact phase-one CCX columns",
    )
    path = root / "research/limitation_program_20261001/temporary_and_fulladder.py"
    definitions = [
        node
        for node in ast.parse(path.read_text(encoding="utf-8")).body
        if isinstance(node, ast.FunctionDef) and node.name == "ccx_seven_t"
    ]
    require(len(definitions) == 1, "One preserved exact CCX definition")
    returns = [node for node in definitions[0].body if isinstance(node, ast.Return)]
    require(len(returns) == 1 and isinstance(returns[0].value, ast.List), "Literal paid macro")
    rows = []
    for item in returns[0].value.elts:
        require(
            isinstance(item, ast.Call)
            and isinstance(item.func, ast.Name)
            and item.func.id == "gate"
            and not item.keywords
            and isinstance(item.args[0], ast.Constant)
            and all(isinstance(arg, ast.Name) for arg in item.args[1:]),
            "Literal macro row",
        )
        rows.append((item.args[0].value, *(arg.id for arg in item.args[1:])))
    require(canonical(rows) == canonical(MACRO), "Both paid control-wire phases and chronology")
    return dict(
        exact_macro=[list(row) for row in MACRO],
        proof_columns=8,
        exact_native_phase_one=True,
        basis_fixtures_are_not_phase_proof=True,
    )


def _closure(target, outputs, input_values):
    require((target["width"], target["fraction_bits"]) == (W, F), "Immutable native72/f40")
    producer, sequence, live = {}, [], set(input_values)
    for node in target["nodes"]:
        require(
            type(node["args"]) is list
            and type(node["out"]) is list
            and all(type(v) is int and v >= 0 for v in node["args"] + node["out"]),
            "Canonical SSA identifiers, not booleans",
        )
        require(all(v not in producer for v in node["out"]), "Unique native SSA outputs")
        require(
            node["op"] == "input" or all(v in producer for v in node["args"]),
            "Original topological SSA order",
        )
        for value in node["out"]:
            producer[value] = node
        sequence.append(node)
    wanted, pending = set(), list(outputs)
    while pending:
        value = pending.pop()
        if value in wanted:
            continue
        require(value in producer, "Named original output has a producer")
        node = producer[value]
        wanted.update(node["out"])
        pending.extend(arg for arg in node["args"] if arg not in wanted)
    selected = [node for node in sequence if any(value in wanted for value in node["out"])]
    require(
        {node["out"][0] for node in selected if node["op"] == "input"} == live,
        "Exactly original external q32 inputs",
    )
    return selected, wanted


def derive_wrappers(plan, root, checkpoint):
    """Select original nodes/calls only; no graph builder, lowering or leaf emission."""
    program = root / "results/limitation_program_20261001"
    scalar = program / "A02_quantile_scalar_run001/candidate64"
    bm = program / "A10_coefficient_run001/B4x12/min-depth"
    scalar_source, scalar_target = (
        read(scalar / "source.json"),
        read(scalar.parent / "scalar_target.json"),
    )
    bm_source, bm_target = read(bm / "source.json"), read(bm / "target.json")
    pair_scope = read(program / "C06_pair_audit_run001/actual_pair_scope_audit.json")
    walked = pair_scope["B4x12"]["independently_walked_pair_scopes"][0]
    require(
        (
            walked["normal_values"],
            walked["raw_uniform_values"],
            walked["radius"],
            walked["log"]["output"],
            [v["output"] for v in walked["cosines"]],
        )
        == ([94, 125], [0, 1], 58, 52, [93, 124]),
        "Original shared pair provenance",
    )
    source_binding = read(program / "C06_pair_run001/certificate.json")["source_bindings"]["B4x12"]
    expected_target = next(
        row["author_readonly_sha256"]
        for row in plan["author_readonly_input_bindings"]
        if row["path"].endswith("A10_coefficient_run001/B4x12/min-depth/target.json")
    )
    require(
        source_binding["target_sha256"] == expected_target
        and source_binding["normal_values"][:2] == [94, 125],
        "Original accepted target binding",
    )
    wrappers, targets = {}, {}
    for index, (source, target, directory, outputs, inputs, total, count, inventory) in enumerate(
        (
            (
                scalar_source,
                scalar_target,
                scalar,
                [170],
                [0],
                171,
                162,
                plan["AS241_wrapper"]["actual_leaf_inventory"],
            ),
            (
                bm_source,
                bm_target,
                bm,
                [94, 125],
                [0, 1],
                126,
                102,
                plan["BoxMuller_wrapper"]["actual_leaf_inventory"],
            ),
        )
    ):
        checkpoint()
        require(
            source["format"] == "hierarchical-clean-xor-source-v1"
            and (source["word_width"], source["fraction_bits"]) == (W, F)
            and source["exact_clifford_t"] is True
            and source["arbitrary_rotations"] == 0,
            "Accepted exact native clean source",
        )
        nodes, values = _closure(target, outputs, inputs)
        require(
            values == set(range(total)) and len(nodes) == count + len(inputs),
            "Exact accepted closure, retaining every native SSA bank",
        )
        if index == 0:
            require(
                source["values"] == total and source["outputs"] == {"Z": 170}, "Scalar source ABI"
            )
        selected = [node for node in nodes if node["op"] != "input"]
        calls = deepcopy(source["forward_calls"][:count])
        require(len(calls) == len(selected) == count, "Exact archived call count")
        leaves = {row["key"]: deepcopy(row) for row in inventory}
        require(
            len(leaves) == (59 if index == 0 else 32)
            and set(leaves) == {call["leaf"] for call in calls},
            "Exact selected leaf inventory",
        )
        private = 0
        for node, call in zip(selected, calls, strict=True):
            require(
                canonical((node["args"], node["out"])) == canonical((call["args"], call["out"]))
                and call["argument_copy_cx"] == 2 * W * len(node["args"]),
                "Unchanged original call/argument occurrence/full72 copy",
            )
            entry = read(root / leaves[call["leaf"]]["metadata"])
            require(
                entry["op"] == node["op"]
                and canonical(entry["params"]) == canonical(node["params"]),
                "Unchanged original native operation and literal parameters",
            )
            arity, nout = len(node["args"]), len(node["out"])
            require(
                canonical(entry["args"])
                == canonical([list(range(i * W, (i + 1) * W)) for i in range(arity)])
                and canonical(entry["outs"])
                == canonical(
                    [list(range((arity + i) * W, (arity + i + 1) * W)) for i in range(nout)]
                ),
                "Every native input/output is contiguous full72",
            )
            qubits = entry["resources"]["qubits"]
            require(
                type(qubits) is int and qubits >= (arity + nout) * W,
                "Explicit full native private/high-wire allocation",
            )
            require(
                entry["key"] == call["leaf"]
                and entry["sha256"]
                == leaves[call["leaf"]]["native_gate_sha256_from_archived_metadata"]
                and qubits == leaves[call["leaf"]]["native_qubits_declared_in_metadata"],
                "Pinned metadata identity and declared native high-water mark",
            )
            private = max(private, qubits - nout * W)
        noninputs = total - len(inputs)
        ssa_base, private_base = 4 * W, (4 + noninputs) * W
        invocations = []
        for invocation in range(2 if index == 0 else 1):
            external_inputs = [invocation] if index == 0 else [0, 1]
            external_outputs = [invocation] if index == 0 else [0, 1]
            banks = [external_inputs[i] * W for i in range(len(inputs))]
            banks.extend(
                ssa_base + (value - len(inputs)) * W for value in range(len(inputs), total)
            )
            invocations.append(
                dict(
                    value_banks=banks,
                    external_input_words=external_inputs,
                    external_output_words=external_outputs,
                    outputs=outputs,
                    forward_calls=deepcopy(calls),
                )
            )
        wrapper = dict(
            schema="two-draw-actual-native-wrapper-v1",
            label=LABELS[index],
            word_width=W,
            fraction_bits=F,
            native_input_offsets=[0, W],
            dirty_output_offsets=[2 * W, 3 * W],
            internal_SSA_words=noninputs,
            SSA_base=ssa_base,
            private_base=private_base,
            private_qubits=private,
            logical_qubits=private_base + private,
            initial_H_separate=64,
            original_source=directory.relative_to(root).as_posix() + "/source.json",
            original_target=(
                scalar.parent / "scalar_target.json" if index == 0 else bm / "target.json"
            )
            .relative_to(root)
            .as_posix(),
            invocations=invocations,
            leaves=leaves,
            clean_schedule="F, full72 output XORs, literal F inverse; serial complete invocations",
            literal_wrapper_inverse="reverse invocation order; same F/CX/literal F^-1 blocks",
            scratch_reuse_only_after_complete_cleanup=True,
            original_nodes_retained=len(nodes),
        )
        require(wrapper["logical_qubits"] <= CAP, "Both actual loaders fit fixed45000 cap")
        wrappers[LABELS[index]] = wrapper
        targets[LABELS[index]] = dict(
            width=W, fraction_bits=F, nodes=nodes, tables=target["tables"], outputs=outputs
        )
    return wrappers, targets


def make_engine():
    """JIT our fixed scanner and packed native gate traversal; disk cache forbidden."""
    import numpy as np
    from numba import njit

    @njit(cache=False)
    def scan(gates, start, stop, reverse, levels, depths, counts):
        qubits = len(levels)
        for position in range(start, stop):
            row = len(gates) - 1 - position if reverse else position
            kind, a, b, c = gates[row]
            if kind < 1 or kind > 3 or a < 0 or a >= qubits:
                raise ValueError("Actual native opcode/first wire")
            if kind < 2 and b != 0 or kind < 3 and c != 0:
                raise ValueError("Canonical zero unused native operands")
            if kind >= 2 and (b < 0 or b >= qubits or a == b):
                raise ValueError("Actual allocated distinct second wire")
            if kind == 3 and (c < 0 or c >= qubits or a == c or b == c):
                raise ValueError("Actual allocated distinct third wire")
            counts[kind - 1] += 1
            if kind == 1:
                depths[a] += 1
            elif kind == 2:
                t, d = max(levels[a], levels[b]), max(depths[a], depths[b]) + 1
                levels[a] = levels[b] = t
                depths[a] = depths[b] = d
            else:
                wires = (
                    (c, c),
                    (b, c),
                    (c, c),
                    (a, c),
                    (c, c),
                    (b, c),
                    (c, c),
                    (a, c),
                    (b, b),
                    (c, c),
                    (c, c),
                    (a, b),
                    (a, a),
                    (b, b),
                    (a, b),
                )
                for step in range(15):
                    first, second = wires[step]
                    t = max(levels[first], levels[second]) + int(step in (2, 4, 6, 8, 9, 12, 13))
                    d = max(depths[first], depths[second]) + 1
                    levels[first] = levels[second] = t
                    depths[first] = depths[second] = d

    @njit(cache=False)
    def gates_packed(gates, state, mapping, start, stop, reverse):
        for position in range(start, stop):
            row = len(gates) - 1 - position if reverse else position
            kind, a, b, c = gates[row]
            if kind == 1:
                state[mapping[a]] ^= np.uint64(LANE_MASK)
            elif kind == 2:
                state[mapping[b]] ^= state[mapping[a]]
            elif kind == 3:
                state[mapping[c]] ^= state[mapping[a]] & state[mapping[b]]
            else:
                raise ValueError("Only previously scanned exact native X/CX/CCX")

    return np, scan, gates_packed


def scan_leaves(wrapper, root, engine, checkpoint):
    np, scan, _ = engine
    ledger, loaded = {}, {}
    for key, origin in sorted(wrapper["leaves"].items()):
        checkpoint()
        entry = read(root / origin["metadata"])
        array = np.load(root / origin["native_gate_file"], mmap_mode="r", allow_pickle=False)
        require(
            array.dtype == np.dtype("int32") and array.ndim == 2 and array.shape[1] == 4,
            "Actual saved int32(N,4) native array",
        )
        qubits, directions = entry["resources"]["qubits"], []
        for reverse in (False, True):
            levels, depths, counts = (
                np.zeros(qubits, np.int64),
                np.zeros(qubits, np.int64),
                np.zeros(3, np.int64),
            )
            for start in range(0, len(array), CHUNK):
                checkpoint()
                scan(array, start, min(start + CHUNK, len(array)), reverse, levels, depths, counts)
                checkpoint()
            x, cx, ccx = map(int, counts)
            directions.append(
                dict(
                    x=x,
                    cx=cx,
                    ccx=ccx,
                    source_gates=len(array),
                    t_count=7 * ccx,
                    t_depth=int(levels.max()),
                    clifford_t_depth=int(depths.max()),
                )
            )
        require(
            all(entry["resources"][field] == directions[0][field] for field in FIELDS),
            "Actual forward rows reconcile immutable metadata, never inherited totals",
        )
        ledger[key] = dict(
            qubits=qubits,
            native_args=entry["args"],
            native_outputs=entry["outs"],
            native_gate_file=origin["native_gate_file"],
            gate_sha256=entry["sha256"],
            forward=directions[0],
            literal_inverse=directions[1],
        )
        loaded[key] = (entry, array)
    return ledger, loaded


def resource_row(wrapper, leaves):
    forward, backward = Counter(), Counter()
    copy_CX, copy_rounds, output_CX, output_rounds = 0, 0, 0, 0
    for invocation in wrapper["invocations"]:
        for call in invocation["forward_calls"]:
            for field in FIELDS:
                forward[field] += leaves[call["leaf"]]["forward"][field]
                backward[field] += leaves[call["leaf"]]["literal_inverse"][field]
            copy_CX += 2 * W * len(call["args"])
            copy_rounds += max(Counter(call["args"]).values(), default=0)
        output_CX += W * len(invocation["outputs"])
        output_rounds += max(Counter(invocation["outputs"]).values(), default=0)
    clean = {field: forward[field] + backward[field] for field in FIELDS}
    clean["cx"] += 2 * copy_CX + output_CX
    clean["source_gates"] += 2 * copy_CX + output_CX
    clean["clifford_t_depth"] += 4 * copy_rounds + output_rounds
    clean.update(
        clifford_cx=clean["cx"] + 6 * clean["ccx"],
        clifford_h=2 * clean["ccx"],
        logical_qubits=wrapper["logical_qubits"],
        max_reused_scratch_qubits=wrapper["private_qubits"],
        internal_full72_SSA_words=wrapper["internal_SSA_words"],
        native_input_words=2,
        dirty_output_words=2,
        initial_Hadamards_separate=64,
        t_depth_schedule="serial complete actual leaves; exact7T ASAP each direction",
        ccx_expansion="phase-correct sevenT/sixCX/twoH with both control-wire phases",
    )
    return dict(
        label=wrapper["label"],
        clean_resources=clean,
        native_leaves=leaves,
        forward_native_resources=dict(forward),
        literal_inverse_native_resources=dict(backward),
        argument_copy_CX_forward=copy_CX,
        argument_copy_CX_inverse=copy_CX,
        argument_copy_depth_sum_forward=copy_rounds,
        full72_output_copy_CX=output_CX,
        full72_output_copy_depth=output_rounds,
        immutable_source_invocations=len(wrapper["invocations"]),
        native_high_wires_full_banks_literal_uncompute_all_charged=True,
        financial_source_cost_divided_by_coordinate_count=False,
    )


def integer_quantile(raw, literals):
    """Independent literal signed integer formula, outside the SSA/gate traversal."""
    require(type(raw) is int and 0 <= raw < 1 << 32, "Canonical q32 input")
    midpoint = (2 * raw + 1) << 7
    negative = midpoint < S // 2
    absolute, probability = abs(midpoint - S // 2), min(midpoint, S - midpoint)

    def horner(coefficients, argument):
        value = coefficients[-1]
        for coefficient in coefficients[-2::-1]:
            value = value * argument // S + coefficient
        return value

    if probability < Fraction(3 * S, 40):
        exponent = probability.bit_length() - 1 - F
        mantissa = probability << -exponent
        index = (mantissa - S) >> (F - 5)
        local = mantissa - (S + (index << (F - 5)) + (1 << (F - 6)))
        logarithm = horner(literals["log_table"][index], local) + exponent * literals["ln2_raw"]
        argument = isqrt((-logarithm) << F) - literals["tail_shift_raw"]
        numerator, denominator = (
            horner(literals[name], argument) for name in ("tail_A_raw", "tail_B_raw")
        )
    else:
        argument = literals["central_rconstant_raw"] - absolute * absolute // S
        numerator = absolute * horner(literals["central_A_raw"], argument) // S
        denominator = horner(literals["central_B_raw"], argument)
    require(
        0 <= numerator < 1 << W and S <= denominator < 1 << 64,
        "Native numerator/denominator contract",
    )
    value = (numerator << F) // denominator
    return (-value if negative else value) & MASK


def integer_pair(target, inputs):
    """Interpret only the unchanged original native pair, with every literal floor."""
    values = {}
    for node in target["nodes"]:
        operation, parameters = node["op"], node["params"]
        raw = [values[key] for key in node["args"]]
        signed = [value - (1 << W) if value & (1 << (W - 1)) else value for value in raw]
        if operation == "input":
            result = [inputs[node["out"][0]]]
        elif operation == "const":
            result = [parameters["value"]]
        elif operation == "add":
            result = [signed[0] + signed[1]]
        elif operation == "sub":
            result = [signed[0] - signed[1]]
        elif operation == "mul":
            result = [(signed[0] * signed[1]) >> F]
        elif operation == "cmul":
            result = [(signed[0] * parameters["c"]) >> F]
        elif operation == "lt":
            result = [int(signed[0] < signed[1])]
        elif operation == "select":
            result = [raw[1] if raw[0] & 1 else raw[2]]
        elif operation == "positive":
            result = [max(signed[0], 0)]
        elif operation == "sqrt":
            result = [isqrt(raw[0] << F)]
        elif operation == "msb":
            result = [max(0, raw[0].bit_length() - 1)]
        elif operation == "shift":
            shift = signed[1]
            result = [
                0
                if shift >= W
                else (-1 if signed[0] < 0 else 0)
                if shift <= -W
                else signed[0] << shift
                if shift >= 0
                else signed[0] >> -shift
            ]
        elif operation == "bits":
            value = signed[0] if parameters.get("signed") else raw[0]
            shift = parameters["shift"]
            result = [
                (value >> shift if shift >= 0 else value << -shift)
                & ((1 << parameters["width"]) - 1)
            ]
        elif operation == "lookup":
            result = target["tables"][parameters["table"]][raw[0] & ((1 << parameters["bits"]) - 1)]
        else:
            raise ValueError("Unexpected original pair operation: " + operation)
        require(len(result) == len(node["out"]), "Original native operation arity")
        for identifier, value in zip(node["out"], result, strict=True):
            values[identifier] = int(value) & MASK
    return [values[key] for key in target["outputs"]]


def initial_state(wrapper, np):
    state = np.zeros(wrapper["logical_qubits"], np.uint64)
    for pair_index, words in enumerate(PAIRS):
        for dirty_index, dirty in enumerate(DIRTY):
            lane = 2 * pair_index + dirty_index
            for bank, word in enumerate((*words, dirty, dirty)):
                for bit in range(W):
                    state[bank * W + bit] |= np.uint64(((word >> bit) & 1) << lane)
    return state


def apply_wrapper(wrapper, state, loaded, engine, checkpoint, inverse=False):
    np, _, execute = engine
    require(
        state.dtype == np.dtype("uint64")
        and state.shape == (wrapper["logical_qubits"],)
        and not np.any(state & np.uint64(~LANE_MASK & ((1 << 64) - 1))),
        "All packed lane masks and allocated wires",
    )

    def call_native(call, banks, reverse):
        entry, array = loaded[call["leaf"]]
        arity, nout = len(call["args"]), len(call["out"])
        private = wrapper["private_base"]
        mapping = np.empty(entry["resources"]["qubits"], np.int64)
        for wire in range(len(mapping)):
            if arity * W <= wire < (arity + nout) * W:
                mapping[wire] = banks[call["out"][(wire - arity * W) // W]] + wire % W
            else:
                mapping[wire] = private + wire - (nout * W if wire >= (arity + nout) * W else 0)
        require(
            int(mapping.min()) >= 0
            and int(mapping.max()) < len(state)
            and len(set(map(int, mapping))) == len(mapping),
            "Complete injective native high-wire bank map",
        )
        argument_order = tuple(reversed(range(arity))) if reverse else tuple(range(arity))
        for argument in argument_order:
            value = call["args"][argument]
            state[private + argument * W : private + (argument + 1) * W] ^= state[
                banks[value] : banks[value] + W
            ]
        for start in range(0, len(array), CHUNK):
            checkpoint()
            execute(array, state, mapping, start, min(start + CHUNK, len(array)), reverse)
            checkpoint()
        for argument in argument_order:
            value = call["args"][argument]
            state[private + argument * W : private + (argument + 1) * W] ^= state[
                banks[value] : banks[value] + W
            ]
        require(
            not np.any(state[private:]),
            "Every copied argument/native private bit clean after actual call",
        )

    invocations = reversed(wrapper["invocations"]) if inverse else wrapper["invocations"]
    for invocation in invocations:
        checkpoint()
        require(
            not np.any(state[wrapper["SSA_base"] :]), "Complete work bank zero before serial reuse"
        )
        banks = invocation["value_banks"]
        for call in invocation["forward_calls"]:
            call_native(call, banks, False)
        output_pairs = list(
            zip(invocation["outputs"], invocation["external_output_words"], strict=True)
        )
        for value, external in reversed(output_pairs) if inverse else output_pairs:
            state[(2 + external) * W : (3 + external) * W] ^= state[banks[value] : banks[value] + W]
        for call in reversed(invocation["forward_calls"]):
            call_native(call, banks, True)
        require(
            not np.any(state[wrapper["SSA_base"] :]),
            "All full72 SSA/native private bits clean before next invocation",
        )
    require(
        not np.any(state & np.uint64(~LANE_MASK & ((1 << 64) - 1))),
        "Native traversal preserves exact fixed lane mask",
    )


def word_from_state(state, offset, lane):
    return sum(((int(state[offset + bit]) >> lane) & 1) << bit for bit in range(W))


def fixture_row(wrapper, target, literals, before, after, restored, pair_index, dirty_index):
    """Check every allocated bit in one actual lane, including complete native inputs."""
    lane = pair_index * 2 + dirty_index
    words, dirty = PAIRS[pair_index], DIRTY[dirty_index]
    expected = (
        [integer_quantile(word, literals) for word in words]
        if wrapper["label"] == LABELS[0]
        else integer_pair(target, {0: words[0], 1: words[1]})
    )
    expected = [value ^ dirty for value in expected]
    require(
        len(before) == len(after) == len(restored) == wrapper["logical_qubits"],
        "Every allocated wire retained",
    )
    for wire in range(len(before)):
        bank, bit = divmod(wire, W)
        initial_word = (*words, dirty, dirty)[bank] if bank < 4 else 0
        final_word = (*words, *expected)[bank] if bank < 4 else 0
        require(
            all(
                type(int(state[wire])) is int and 0 <= int(state[wire]) <= LANE_MASK
                for state in (before, after, restored)
            ),
            "Canonical packed state/lane mask",
        )
        require(
            ((int(before[wire]) >> lane) & 1) == ((initial_word >> bit) & 1),
            "Exact initial complete lane state",
        )
        require(
            ((int(after[wire]) >> lane) & 1) == ((final_word >> bit) & 1),
            "Actual full dirty XOR/input/zero scratch state",
        )
        require(
            ((int(restored[wire]) >> lane) & 1) == ((initial_word >> bit) & 1),
            "Literal inverse restores every bit",
        )
    return dict(
        loader=wrapper["label"],
        pair_index=pair_index,
        dirty_index=dirty_index,
        lane=lane,
        q32_raw=list(words),
        initial_outputs72=[dirty, dirty],
        expected_outputs72=expected,
        observed_outputs72=[
            word_from_state(after, 2 * W, lane),
            word_from_state(after, 3 * W, lane),
        ],
        full_native_inputs72_preserved=True,
        all_full_SSA_and_native_private_bits_clean=True,
        literal_inverse_restores_complete_state=True,
        all_allocated_bits_checked=True,
        allocated_state_qubits=len(after),
        actual_immutable_gate_replay=True,
        basis_diagnostic_is_not_all_input_or_phase_proof=True,
    )
