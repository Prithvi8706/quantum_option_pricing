"""Independent signed7 barrel-shift, array and full-source audit of local A07.

The resource body is versioned to support the signed7 count promise while
keeping historical auditors and receipts immutable. This auditor runs no
financial or emitted gate replay; it checks their saved receipts when present.
"""

from __future__ import annotations

# Human-readable receipt prose deliberately remains unwrapped.
# ruff: noqa: E501

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import time
import xml.etree.ElementTree as ET

import numpy as np

from research.limitation_program_20261001.baseline import (
    CATEGORIES, COUNT_FIELDS, ROOT, dump, environment, independent_dag, load, sha,
)
from research.limitation_program_20261001.compact_ledger import active_bit_certificate
from research.limitation_program_20261001.interval_bounds import bound_graph
from research.limitation_program_20261001.reconcile_constants import (
    ORIGINAL, graph_log_proof, library_path, relative,
)
from research.limitation_program_20261001.reconcile_sqrt import (
    Auditor as SqrtAuditor, check_manifest as check_basic_manifest, input_files, independently_pack,
)

BASELINE = ROOT / "results/limitation_program_20261001/A11_run001"
CASES = ("B4x12", "B8x52")
CAPS = {"B4x12": 550141, "B8x52": 4460481}
VARIANTS = ("signed7-barrel",)


class Auditor(SqrtAuditor):
    """Actual scanner with independently recomputed count interval promises."""

    def shift_proof(self, target, node_index, contract):
        assert contract == {"signed_shift_count_bits": 7}
        assert type(contract["signed_shift_count_bits"]) is int
        assert (target["width"], target["fraction_bits"]) == (72, 40)
        node = target["nodes"][node_index]
        assert node["op"] == "shift" and node["params"] == {}
        assert len(node["args"]) == 2 and len(node["out"]) == 1
        key = id(target)
        if not hasattr(self, "interval_cache"):
            self.interval_cache = {}
        if key not in self.interval_cache:
            self.interval_cache[key] = (target, bound_graph(target))
        cached_target, (intervals, rules) = self.interval_cache[key]
        assert cached_target is target
        data, count = node["args"]
        output = node["out"][0]
        low, high = intervals[count]
        assert -64 <= low <= high <= 63, ("Unproved signed7 count", node_index, low, high)
        return dict(
            node_index=node_index, data_value=data, shift_value=count,
            output_value=output, shift_bounds=[low, high],
            signed_control_bits=7, signed7_guard_proved=True,
            input_rule=rules[count], all_declared_input_bit_patterns=True,
            finite_samples_used_as_proof=False,
            two_full_native_arguments_preserved=True,
        )

    def costs(self, case, directory):
        target, source = (load(directory / name) for name in ("target.json", "source.json"))
        for name in ("target.json", "source.json"):
            self.record(directory / name)
        original_manifest = load(ORIGINAL / "manifest.json")
        original_target_key = (
            "results/limitation_audit_20261001/constant_multiplier_v1/"
            + case
            + "/signed-digit-carry-save/target.json"
        )
        assert (
            sha(directory / "target.json")
            == original_manifest["frozen_inputs"][original_target_key]
        )
        accounting_path = ORIGINAL / (case + "_accounting.json")
        assert sha(accounting_path) == original_manifest["files"][relative(accounting_path)]
        entries = self.leafs(source)
        original = load(ORIGINAL / (case + "_accounting.json"))
        calls = source["forward_calls"]
        assert len(calls) == len(original["assignments"])
        masks = active_bit_certificate(target)
        assert set(masks) == set(range(source["values"]))
        widths = [max(1, masks[value].bit_length()) for value in range(source["values"])]
        w = source["word_width"]
        assert (
            w == target["width"] == 72 and source["fraction_bits"] == target["fraction_bits"] == 40
        )
        noninputs = [i for i, node in enumerate(target["nodes"]) if node["op"] != "input"]
        assert noninputs == [a["node_index"] for a in original["assignments"]]
        categories = {name: Counter() for name in CATEGORIES}
        operations, owners = defaultdict(Counter), defaultdict(Counter)
        forward, serial_op = Counter(), defaultdict(Counter)
        active_copies = serial_copies = serial_copy_depth = 0
        labels, op_names, proofs, unsigned_proofs, shift_proofs = [], [], [], [], []
        context = (
            {v: n for n in target["nodes"] for v in n["out"]},
            {v: i for i, n in enumerate(target["nodes"]) for v in n["out"]},
        )
        self_products, self_signatures = [], defaultdict(list)
        for index, (call, assignment) in enumerate(
            zip(calls, original["assignments"], strict=True)
        ):
            node_index = assignment["node_index"]
            node, entry = target["nodes"][node_index], entries[call["leaf"]]
            assert assignment["call_index"] == index and assignment["out"] == call["out"]
            assert node["args"] == call["args"] and node["out"] == call["out"]
            assert node["op"] == entry["op"] and node["params"] == entry["params"]
            assert len(entry["args"]) == len(call["args"]) and len(entry["outs"]) == len(
                call["out"]
            )
            for value, register in zip(
                call["args"] + call["out"], entry["args"] + entry["outs"], strict=True
            ):
                assert widths[value] <= len(register) <= w
            contract = entry.get("input_contract", {})
            assert set(contract) <= {"zero_low_bits", "signed_upper_bits", "unsigned_input_bits", "signed_shift_count_bits"}
            if "signed_shift_count_bits" in contract:
                shift_proofs.append(self.shift_proof(target, node_index, contract))
                assert entry["args"] == [list(range(72)), list(range(72, 144))]
                assert entry["outs"] == [list(range(144, 216))]
            if "unsigned_input_bits" in contract:
                unsigned_proofs.append(self.unsigned_proof(target, node_index, contract))
            if "zero_low_bits" in contract:
                low = contract["zero_low_bits"]
                assert len(call["args"]) == 1 and type(low) is int and 0 <= low <= w
                assert not masks[call["args"][0]] & ((1 << low) - 1)
            if "signed_upper_bits" in contract:
                assert contract == {"zero_low_bits": 40, "signed_upper_bits": 7}
                proof = graph_log_proof(target, node_index, context)
                assert proof is not None, ("Unproved signed7 promise", case, index)
                proofs.append(proof)
            assert call["argument_copy_cx"] == 2 * len(call["args"]) * w
            copied = 4 * sum(widths[v] for v in call["args"])
            active_copies += copied
            serial_copies += 4 * len(call["args"]) * w
            serial_copy_depth += max(Counter(call["args"]).values(), default=0)
            label = assignment["category"]
            labels.append(label)
            op_names.append(node["op"])
            categories[label]["forward_calls"] += 1
            categories[label]["clean_argument_copy_cx"] += copied
            for field in COUNT_FIELDS + ("t_depth", "clifford_t_depth"):
                forward[field] += entry["resources"][field]
            for field in COUNT_FIELDS:
                categories[label][field] += 2 * entry["resources"][field]
            for field in ("source_gates", "cx", "clifford_cx"):
                categories[label][field] += copied
            serial_op[node["op"]].update(
                calls=1,
                t_count=entry["resources"]["t_count"],
                t_depth=entry["resources"]["t_depth"],
            )
            operations[node["op"]]["clean_t_count"] += 2 * entry["resources"]["t_count"]
            if node["op"] == "mul" and node["args"][0] == node["args"][1]:
                operand = context[0][node["args"][0]]
                signature = dict(
                    producer_op=operand["op"],
                    producer_params=operand["params"],
                    producer_arity=len(operand["args"]),
                    width=w,
                    fraction_bits=source["fraction_bits"],
                )
                self_signatures[json.dumps(signature, sort_keys=True)].append(index)
                self_products.append(
                    dict(
                        call_index=index,
                        node_index=node_index,
                        operand_value=node["args"][0],
                        operand_producer_index=context[1][node["args"][0]],
                        operand_producer=operand,
                        category=label,
                        leaf=call["leaf"],
                        outputs=call["out"],
                        resources=entry["resources"],
                    )
                )
        serial_copies += len(source["outputs"]) * w
        out_copies = sum(widths[v] for v in source["outputs"].values())
        active_copies += out_copies
        output_depth = max(Counter(source["outputs"].values()).values(), default=0)
        for field in ("source_gates", "cx", "clifford_cx"):
            categories["path_payoff"][field] += out_copies
        categories["path_payoff"]["output_copy_cx"] = out_copies
        serial_counts = {
            field: 2 * forward[field]
            + (serial_copies if field in ("source_gates", "cx", "clifford_cx") else 0)
            for field in COUNT_FIELDS
        }
        serial_counts.update(
            t_depth=2 * forward["t_depth"],
            clifford_t_depth=2 * forward["clifford_t_depth"] + 4 * serial_copy_depth + output_depth,
        )
        serial_scratch = max(
            entries[c["leaf"]]["resources"]["qubits"] - len(c["out"]) * w for c in calls
        )
        serial_counts.update(
            logical_qubits=(source["values"] + len(source["outputs"])) * w + serial_scratch,
            max_reused_scratch_qubits=serial_scratch,
        )
        assert all(source["resources"][field] == value for field, value in serial_counts.items())
        assert {op: dict(value) for op, value in serial_op.items()} == source[
            "forward_operation_costs"
        ]
        counts = {
            field: 2 * forward[field]
            + (active_copies if field in ("source_gates", "cx", "clifford_cx") else 0)
            for field in COUNT_FIELDS
        }
        assert all(
            sum(c[field] for c in categories.values()) == counts[field] for field in COUNT_FIELDS
        )
        assert (
            counts["t_count"] == 7 * counts["ccx"]
            and counts["clifford_cx"] == counts["cx"] + 6 * counts["ccx"]
        )
        dag, levels, critical = independent_dag(source, entries)
        result = dict(
            case=case,
            passed=True,
            counts=counts,
            canonical_serial_manifest_resources=serial_counts,
            forward_calls=len(calls),
            signed7_structural_proofs=proofs,
            unsigned46_same_ssa_proofs=unsigned_proofs,
            signed7_shift_count_proofs=shift_proofs,
            independent_forward_dependency_t_depth=dag,
            serial_full_width_copy_cx=serial_copies,
            compact_argument_copy_cx=active_copies - out_copies,
            output_copy_cx=out_copies,
            compact_total_copy_cx=active_copies,
        )
        result["same_ssa_self_products"] = dict(
            count=len(self_products),
            cases=self_products,
            signatures=[
                dict(signature=json.loads(key), count=len(indices), call_indices=indices)
                for key, indices in sorted(self_signatures.items())
            ],
            interpretation="Existing exact repeated SSA multiplication sites are inventoried without changes in this shift experiment. No independent attainable capped saving is inferred from site counts.",
        )
        schedule_path = directory / "schedule_capped.json"
        if not schedule_path.exists():
            result.update(
                schedule_available=False,
                minimum_retained_and_one_leaf_qubits=sum(widths)
                + len(source["outputs"]) * w
                + max(
                    entries[c["leaf"]]["resources"]["qubits"] - sum(widths[v] for v in c["out"])
                    for c in calls
                ),
            )
            return result
        self.record(schedule_path)
        schedule = load(schedule_path)

        def fingerprint(obj):
            return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()

        assert schedule["source_fingerprint"] == fingerprint(source) and schedule[
            "target_fingerprint"
        ] == fingerprint(target)
        assert schedule["widths"] == widths and schedule["proof_masks"] == [
            masks[v] for v in range(source["values"])
        ]
        cursor, offsets = 0, []
        for width in widths:
            offsets.append(cursor)
            cursor += width
        assert offsets == schedule["offsets"] and cursor == schedule["retained_ssa_qubits"]
        assert (
            active_copies == schedule["argument_and_output_copy_cx"]
            and serial_copies == schedule["baseline_argument_and_output_copy_cx"]
        )
        assert all(schedule["resources"][field] == value for field, value in counts.items())
        assert dag == schedule["dependency_only_forward_t_depth"]
        for index in critical:
            categories[labels[index]]["one_critical_path_t_depth_contribution"] += entries[
                calls[index]["leaf"]
            ]["resources"]["t_depth"]
        retained = cursor + len(source["outputs"]) * w
        indices_seen, batches = [], []
        td_total = ct_total = peak = 0
        for batch_index, batch in enumerate(schedule["groups"]):
            indices = batch["call_indices"]
            assert indices and len(indices) == len(set(indices))
            indices_seen.extend(indices)
            assert all(levels[i] == batch["wave"] for i in indices)
            assert batch_index == 0 or batch["wave"] >= schedule["groups"][batch_index - 1]["wave"]
            scratch = sum(
                entries[calls[i]["leaf"]]["resources"]["qubits"]
                - sum(widths[v] for v in calls[i]["out"])
                for i in indices
            )
            copies = max(Counter(v for i in indices for v in calls[i]["args"]).values(), default=0)
            td = max(entries[calls[i]["leaf"]]["resources"]["t_depth"] for i in indices)
            ct = (
                max(entries[calls[i]["leaf"]]["resources"]["clifford_t_depth"] for i in indices)
                + 2 * copies
            )
            assert (scratch, copies, td, ct) == (
                batch["private_scratch_qubits"],
                batch["copy_rounds"],
                batch["t_depth"],
                batch["clifford_t_depth"],
            )
            assert retained + scratch <= schedule["qubit_cap"]
            td_total += 2 * td
            ct_total += 2 * ct
            peak = max(peak, scratch)
            owner = min(
                indices, key=lambda i: (-entries[calls[i]["leaf"]]["resources"]["t_depth"], i)
            )
            key = calls[owner]["leaf"]
            owners[key]["exclusive_batch_t_depth"] += 2 * td
            owners[key]["owned_batches"] += 1
            operations[op_names[owner]]["exclusive_batch_t_depth"] += 2 * td
            categories[labels[owner]]["exclusive_batch_owner_t_depth_diagnostic"] += 2 * td
            for name in CATEGORIES:
                categories[name]["overlapping_capped_t_depth_diagnostic"] += 2 * max(
                    (
                        entries[calls[i]["leaf"]]["resources"]["t_depth"]
                        for i in indices
                        if labels[i] == name
                    ),
                    default=0,
                )
            batches.append(
                dict(
                    batch=batch_index,
                    dominant_call=owner,
                    dominant_leaf=key,
                    dominant_op=op_names[owner],
                    t_depth=td,
                    private_scratch_qubits=scratch,
                )
            )
        ct_total += output_depth
        assert sorted(indices_seen) == list(range(len(calls))) and len(set(indices_seen)) == len(
            indices_seen
        )
        assert (td_total, ct_total, retained + peak, peak) == tuple(
            schedule["resources"][field]
            for field in (
                "t_depth",
                "clifford_t_depth",
                "logical_qubits",
                "max_reused_scratch_qubits",
            )
        )
        assert (
            sum(c["exclusive_batch_owner_t_depth_diagnostic"] for c in categories.values())
            == td_total
        )
        assert sum(c["one_critical_path_t_depth_contribution"] for c in categories.values()) == dag
        random_h = sum(n["params"]["bits"] for n in source["inputs"])
        assert (
            random_h
            == schedule["resources"]["random_hadamards"]
            == source["resources"]["random_hadamards"]
        )
        categories["uniform_preparation"]["initial_hadamards_separate"] = random_h
        top = []
        for key, owner in sorted(
            owners.items(), key=lambda pair: (-pair[1]["exclusive_batch_t_depth"], pair[0])
        )[:3]:
            zero_depth = 2 * sum(
                max(
                    (
                        entries[calls[i]["leaf"]]["resources"]["t_depth"]
                        for i in group["call_indices"]
                        if calls[i]["leaf"] != key
                    ),
                    default=0,
                )
                for group in schedule["groups"]
            )
            top.append(
                dict(
                    leaf=key,
                    op=entries[key]["op"],
                    params=entries[key]["params"],
                    **dict(owner),
                    optimistic_fixed_batch_zero_cost_saving=td_total - zero_depth,
                )
            )
        result.update(
            schedule_available=True,
            resources=schedule["resources"],
            qubit_cap=schedule["qubit_cap"],
            retained_ssa_qubits=cursor,
            named_output_qubits=len(source["outputs"]) * w,
            peak_private_scratch_qubits=peak,
            batch_count=len(batches),
            category_costs={name: dict(value) for name, value in categories.items()},
            operation_ranking=sorted(
                (dict(op=op, **dict(value)) for op, value in operations.items()),
                key=lambda v: (-v.get("exclusive_batch_t_depth", 0), v["op"]),
            ),
            top_three_depth_owner_leaves=top,
            batches=batches,
        )
        return result


def arithmetic_certificate():
    """Unsigned magnitude and serial-mux shift identities, independently checked."""
    checks = 0
    for count in range(-64, 64):
        raw = count & 127
        negative = bool(raw & 64)
        negated = (-raw) & 127
        magnitude = negated if negative else raw
        assert negative == (count < 0) and magnitude == abs(count)
        assert 0 <= magnitude <= 64
        assert magnitude == sum(((magnitude >> j) & 1) << j for j in range(7))
        for width in (1, 2, 3, 4, 8, 72):
            mask, sign = (1 << width) - 1, 1 << (width - 1)
            patterns = range(1 << width) if width <= 8 else (0, 1, mask, sign, sign-1, sign+1, 1 << 63, mask ^ (1 << 32))
            for data in patterns:
                signed = data - (1 << width) if data & sign else data
                negative_data = int(bool(data & sign))

                def reverse(value):
                    return sum(((value >> i) & 1) << (width - 1 - i) for i in range(width))

                work = reverse(data) if negative else data
                fill = int(negative) & negative_data
                for j in range(7):
                    if magnitude >> j & 1:
                        distance = 1 << j
                        work = ((work << distance) & mask) | (fill * ((1 << min(distance, width)) - 1))
                chosen = reverse(work) if negative else work
                expected = (signed >> -count if count < 0 else data << count) & mask
                assert chosen == expected
                checks += 1
    assert ((-((-64) & 127)) & 127) == 64
    return dict(
        passed=True, signed_count_bits=7, admissible_count_interval=[-64, 63],
        full_native_width=72, unsigned_magnitude_interval=[0, 64],
        minimum_count_magnitude=64,
        direction="nonnegative count: left modulo2**72; negative count: arithmetic right",
        magnitude="Select negative7=(~k_low7+1)mod128 when k6=1, else low7; interpret selected7 as unsigned, including -64->64",
        stages="Conditional reversal R for negative count; fill=negative_count AND negative_data; for j=0..6, mux maps each bit z to old[z-2**j] if in range, else fill, when unsigned magnitude bit j is set; conditional final R gives arithmetic right for negative counts and modular left otherwise",
        oversized_branch="Maximum magnitude64<width72, so no oversized comparison/saturation branch is needed under the guard; generic fallback retains all fullword counts",
        all_word_identity=True, finite_bookkeeping_checks=checks,
        proof_scope="Two's-complement magnitude and modular left/arithmetic-right mux composition are algebraic all-data identities on the signed7 guard. Finite enumeration checks bookkeeping; saved emitted tests and structural parser check realization, without exhaustive72 data enumeration.",
    )


def structure(entry, path):
    """Parse unsigned magnitude, Fredkin reversal and every actual barrel mux."""
    assert sha(path) == entry["sha256"]
    spec = entry["spec"]
    assert entry["op"] == spec["op"] == "shift" and entry["params"] == spec["params"] == {}
    assert (spec["width"], spec["fraction_bits"], spec["count_bits"]) == (72, 40, 7)
    assert spec["lowering"] == "signed-count-narrow-barrel-shift-v1"
    assert spec == dict(
        op="shift", width=72, fraction_bits=40, params={}, count_bits=7,
        input_contract={"signed_shift_count_bits": 7},
        lowering="signed-count-narrow-barrel-shift-v1",
        integration_lowering="same-target-signed-count-shift-library-v1",
        domain="second native word is sign-extended signed count_bits integer",
        count_scale="unscaled integer; fraction_bits does not scale the count",
        direction="nonnegative modular left; negative arithmetic right",
        algorithm="conditional reversal; unsigned magnitude; one left barrel",
        embedding="native compute/output-XOR/literal reverse",
        oversized="left zero; arithmetic right all original data sign bits",
    )
    assert entry["input_contract"] == spec["input_contract"] == {"signed_shift_count_bits": 7}
    assert type(spec["input_contract"]["signed_shift_count_bits"]) is int
    assert entry["args"] == [list(range(72)), list(range(72, 144))]
    assert entry["outs"] == [list(range(144, 216))]
    expected_key = hashlib.sha256(json.dumps(spec, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()[:20]
    assert entry["key"] == expected_key
    gates = np.load(path, mmap_mode="r")
    assert (len(gates) - 72) % 2 == 0
    half = (len(gates) - 72) // 2
    before, copied, after = gates[:half], gates[half:half + 72], gates[half + 72:]
    assert np.array_equal(before, after[::-1])
    assert not np.isin(before[:, 1:], np.arange(79, 216)).any()
    assert np.all(copied[:, 0] == 2) and np.array_equal(copied[:, 2], np.arange(144, 216))
    assert not np.isin(copied[:, 1], np.arange(216)).any()
    position, wire_cursor = 0, 216

    def allocate(size):
        nonlocal wire_cursor
        result = list(range(wire_cursor, wire_cursor + size))
        wire_cursor += size
        return result

    def expect(wires):
        nonlocal position
        row = before[position]
        assert int(row[0]) == len(wires) and tuple(map(int, row[1:1 + len(wires)])) == tuple(wires), ("Unexpected shift gate", position, row.tolist(), wires)
        assert wires[-1] >= 216, ("Input modified by shift body", position, wires)
        position += 1

    work, magnitude, carries = allocate(72), allocate(7), allocate(6)
    fill, difference = allocate(1)[0], allocate(1)[0]
    data, count, sign = list(range(72)), list(range(72, 79)), 78
    for source, destination in zip(data, work, strict=True):
        expect((source, destination))

    def reverse_conditional(register):
        for z in range(36):
            left, right = register[z], register[71 - z]
            expect((left, right))
            expect((sign, right, left))
            expect((left, right))

    reverse_conditional(work)
    expect((count[0], magnitude[0]))
    for i in range(1, 7):
        previous = sign if i == 1 else carries[i - 2]
        carry = carries[i - 1]
        # carry_i = sign AND all lower count bits zero. This encodes -k
        # modulo128; the selected magnitude is interpreted as unsigned.
        expect((previous, carry))
        expect((previous, count[i - 1], carry))
        expect((count[i], magnitude[i]))
        expect((sign, magnitude[i]))
        expect((carry, magnitude[i]))
    expect((sign, data[-1], fill))
    muxes, fill_muxes = 0, 0
    previous = work
    for j in range(7):
        following = allocate(72)
        distance = 1 << j
        for z in range(72):
            source = previous[z - distance] if z >= distance else fill
            old, destination = previous[z], following[z]
            expect((old, destination))
            expect((old, difference))
            expect((source, difference))
            expect((magnitude[j], difference, destination))
            expect((source, difference))
            expect((old, difference))
            muxes += 1
            fill_muxes += z < distance
        previous = following
    reverse_conditional(previous)
    assert position == len(before), (position, len(before))
    assert np.array_equal(copied[:, 1], previous)
    assert entry["resources"]["qubits"] == wire_cursor == 807
    return dict(
        native_argument_bits=[72, 72], output_bits=72,
        count_low_control_bits=7, native_high_count_bits_preserved=True,
        native_arguments_never_modified=True, conditional_reversal_pairs=72,
        clean_reused_difference_wire=True, barrel_stages=7,
        conditional_muxes=muxes, signed_fill_muxes=fill_muxes,
        magnitude_carry_wires=6, minimum_signed_count_unsigned_magnitude=64,
        largest_shift_magnitude_less_than72=True,
        direction="nonnegative leftmodular, negative arithmeticright",
        arbitrary_output_xor=True, literal_forward_reverse_cleanup=True,
        private_workspace_counted_and_restored=True, qubits=wire_cursor,
    )


def changes(auditor, source_root, case, variant):
    directory = source_root / case / variant
    before, after = (load(path / "source.json") for path in (BASELINE / case, directory))
    target = load(directory / "target.json")
    assert sha(directory / "target.json") == sha(BASELINE / case / "target.json")
    for field in ("format", "word_width", "fraction_bits", "values", "inputs", "outputs", "clean_schedule", "invocation_semantics", "inverse_semantics", "exact_clifford_t", "arbitrary_rotations"):
        assert before[field] == after[field]
    left, right = auditor.leafs(before), auditor.leafs(after)
    producer_protocol = load(source_root / "protocol.json")
    leaf_root = ROOT / producer_protocol["leaf_receipt"].replace("\\", "/")
    leaf_best = load(leaf_root / "summary.json")["best"]
    old_archive, new_archive = library_path(before), library_path(after)
    noninputs = [i for i, node in enumerate(target["nodes"]) if node["op"] != "input"]
    changed, unchanged, structures, proofs = [], set(), {}, []
    for call_index, (old, new) in enumerate(zip(before["forward_calls"], after["forward_calls"], strict=True)):
        assert {k: v for k, v in old.items() if k != "leaf"} == {k: v for k, v in new.items() if k != "leaf"}
        old_entry, new_entry = left[old["leaf"]], right[new["leaf"]]
        node_index = noninputs[call_index]
        node = target["nodes"][node_index]
        intended = node["op"] == "shift" and len(node["args"]) == 2 and node["params"] == {}
        assert (old["leaf"] != new["leaf"]) == intended
        if not intended:
            key = old["leaf"]
            if key not in unchanged:
                assert sha(old_archive / (key + ".json")) == sha(new_archive / (key + ".json"))
                assert sha(old_archive / old_entry["gate_file"]) == sha(new_archive / new_entry["gate_file"])
                unchanged.add(key)
            continue
        assert variant == "signed7-barrel"
        assert new_entry["sha256"] == leaf_best["sha256"]
        assert new_entry["resources"] == leaf_best["resources"]
        assert {k: v for k, v in new_entry["spec"].items() if k != "integration_lowering"} == leaf_best["spec"]
        proofs.append(auditor.shift_proof(target, node_index, new_entry["input_contract"]))
        if new["leaf"] not in structures:
            structures[new["leaf"]] = structure(new_entry, new_archive / new_entry["gate_file"])
        changed.append(dict(call_index=call_index, args=new["args"], out=new["out"], old_key=old["leaf"], new_key=new["leaf"], op="shift", params={}, old_resources=old_entry["resources"], new_resources=new_entry["resources"], input_contract=new_entry["input_contract"]))
    assert len(proofs) == (78 if case == "B4x12" else 650)
    assert load(directory / "changed_calls.json") == dict(changes=changed, unchanged_leaf_keys=sorted(unchanged))
    decisions = load(directory / "site_decisions.json")
    assert len(decisions) == len(after["forward_calls"])
    assert {d["forward_call_index"] for d in decisions} == set(range(len(after["forward_calls"])))
    proofs_by_index = {proof["node_index"]: proof for proof in proofs}
    for row in decisions:
        index = row["forward_call_index"]
        assert row["node_index"] == noninputs[index]
        node = target["nodes"][row["node_index"]]
        assert row["outputs"] == node["out"] and row["op"] == node["op"]
        assert row["old_key"] == before["forward_calls"][index]["leaf"]
        assert row["new_key"] == after["forward_calls"][index]["leaf"]
        if row["old_key"] != row["new_key"]:
            assert row["type"] == "shift-narrow"
            proof = proofs_by_index[row["node_index"]]
            assert row["proof"] == dict(
                data_value=proof["data_value"], count_value=proof["shift_value"],
                output_value=proof["output_value"], count_bounds=proof["shift_bounds"],
                signed_shift_count_bits=7, all_declared_input_patterns=True,
                maximum_count_magnitude=64, data_width=72,
                proof="Inductive exact integer intervals in the same validated SSA graph",
                directions="Nonnegative count: modular left; negative: arithmetic right",
            )
        else:
            assert row["type"] == "fallback"
    schedule, old_schedule = (load(path / "schedule_capped.json") for path in (directory, BASELINE / case))
    assert schedule["format"] == "compact-clean-xor-capped-wave-schedule-v4"
    for field in ("widths", "offsets", "retained_ssa_qubits", "proof_masks", "proof_reasons", "argument_and_output_copy_cx", "baseline_argument_and_output_copy_cx"):
        assert schedule[field] == old_schedule[field], ("Unreviewed storage/copy change", case, variant, field)
    independently_pack(after, right, schedule)
    leaf_improved = bool(changed) and all(row["new_resources"]["t_count"] < row["old_resources"]["t_count"] or row["new_resources"]["qubits"] < row["old_resources"]["qubits"] for row in changed)
    return dict(changed_calls=len(changed), unchanged_leaf_keys=len(unchanged), structural_leaf_proofs=structures, actual_same_ssa_shift_proofs=proofs, storage_and_copy_allocation_unchanged=True, exact_first_fit_groups_recomputed=True, clean_leaf_work_or_scratch_improved=leaf_improved)


def check_manifest(directory):
    check_basic_manifest(directory)
    for name, expected in load(directory / "manifest.json").get("frozen_inputs", {}).items():
        assert sha(ROOT / name.replace("\\", "/")) == expected, ("Frozen producer dependency changed", name)


def freeze(source_root):
    summary, protocol = (load(source_root / name) for name in ("summary.json", "protocol.json"))
    assert summary["passed"] and len(summary["cases"]) == 2
    assert (ROOT / protocol["baseline"].replace("\\", "/")).resolve() == BASELINE.resolve()
    assert protocol["family"] == list(VARIANTS)
    assert protocol["threshold_percent"] == 2 and protocol["promise"] == {"signed_shift_count_bits": 7}
    assert (protocol["width"], protocol["fraction_bits"]) == (72, 40)
    assert protocol["cases"] == list(CASES) and protocol["local_only"] is True
    assert protocol["cpu_limit_seconds"] == 1800
    assert load(BASELINE / "summary.json")["accepted"]
    assert protocol["replay_inputs"] == {row["case"]: row["replays"] for row in load(BASELINE / "summary.json")["cases"]}
    check_manifest(source_root)
    frozen = {relative(path): sha(path) for path in source_root.rglob("*") if path.is_file()}
    leaf_root = ROOT / protocol["leaf_receipt"].replace("\\", "/")
    assert sha(leaf_root / "manifest.json") == protocol["leaf_receipt_manifest_sha256"]
    assert load(leaf_root / "summary.json")["passed"]
    check_manifest(leaf_root)
    for path in leaf_root.rglob("*"):
        if path.is_file():
            frozen[relative(path)] = sha(path)
    for field in ("external_files", "frozen_inputs"):
        for name, expected in load(leaf_root / "manifest.json").get(field, {}).items():
            assert sha(ROOT / name) == expected
            frozen[name.replace("\\", "/")] = expected
    for case in CASES:
        for path in input_files(BASELINE / case):
            frozen[relative(path)] = sha(path)
        for variant in VARIANTS:
            for path in input_files(source_root / case / variant):
                frozen[relative(path)] = sha(path)
    for path in (BASELINE / "summary.json", ORIGINAL / "manifest.json"):
        frozen[relative(path)] = sha(path)
    for case in CASES:
        path = ORIGINAL / (case + "_accounting.json")
        frozen[relative(path)] = sha(path)
    for name, expected in protocol["baseline_hashes"].items():
        assert sha(BASELINE / name) == expected
    for name, expected in protocol["baseline_leaf_hashes"].items():
        assert sha(ROOT / name) == expected
    for dependency in protocol["executed_dependencies"]:
        snapshot = source_root / dependency["snapshot"]
        assert sha(snapshot) == dependency["sha256"]
        assert sha(ROOT / dependency["source"]) == dependency["sha256"]
        frozen[dependency["source"].replace("\\", "/")] = dependency["sha256"]
    for name in (
        "research.limitation_program_20261001.reconcile_sqrt",
        "research.limitation_program_20261001.reconcile_constants",
        "research.limitation_program_20261001.baseline",
        "research.limitation_program_20261001.compact_ledger",
        "research.limitation_program_20261001.interval_bounds",
        "research.controlled_source_completion.primitives",
    ):
        path = Path(sys.modules[name].__file__)
        frozen[relative(path)] = sha(path)
    path = ROOT / "research/controlled_source_completion/carry_lookahead.py"
    frozen[relative(path)] = sha(path)
    frozen[relative(Path(__file__))] = sha(Path(__file__))
    return frozen, protocol


def eligibility(resources, baseline, cap, leaf_improved):
    return (
        100 * resources["t_depth"] <= 98 * baseline["t_depth"]
        and resources["clifford_t_depth"] <= baseline["clifford_t_depth"]
        and resources["logical_qubits"] <= cap
        and leaf_improved
    )


def run(source_root, output):
    source_root, output = source_root.resolve(), output.resolve()
    frozen, producer_protocol = freeze(source_root)
    output.mkdir(parents=True, exist_ok=False)
    report = ROOT / "docs/limitation_program_20261001/SHIFT_SOURCE_COSTS.md"
    assert not report.exists()
    started = time.perf_counter()
    dump(output / "protocol.json", dict(
        created_utc=datetime.now(timezone.utc).isoformat(), before_analysis=True,
        local_only=True, source_root=relative(source_root), baseline=relative(BASELINE),
        frozen_inputs=frozen, producer_sha256=sha(Path(__file__)),
        scope="Independent read-only actual-array, unsigned-magnitude, barrel, cleanup and resource audit; no new pricing or gate replay",
        family=list(VARIANTS),
        checks="All gate array counts/depths and native two72 arguments; independent signed7 unsigned-magnitude arithmetic; two conditional reversals and every conditional left mux, signed fill, clean reused difference wire, minimum-count magnitude64, output copy and reverse; actual same-SSA interval guards; target/fallback bytes including sqrt and lookup; unchanged compact masks/storage/copies; full counts/DAG/first-fit caps/categories; predeclared both-case eligibility and stop rule; saved finite tests/full-source replay receipts",
        selection="At least2% complete capped T-depth reduction in each case, CT-depth<=baseline, current actual caps, clean leaf T work or scratch improvement at every changed call; sole preregistered signed7-count barrel-shift variant",
        stop_rule="One preregistered candidate in two cases; if either full-depth threshold fails, retain A11, run no new financial replay and stop this branch",
        proof_scope="The actual count intervals and signed7 shift identity cover all declared inputs under the guard. Emitted realization is checked structurally against exact primitives and finite saved tests; no exhaustive72 enumeration, continuous-price or physical speedup certification.",
    ))
    dump(output / "environment.json", environment())
    certificate = arithmetic_certificate()
    dump(output / "shift_arithmetic_certificate.json", certificate)
    auditor = Auditor(frozen)
    summary = load(source_root / "summary.json")
    trials = {}
    for case in CASES:
        comparison = next(row for row in summary["cases"] if row["case"] == case)
        assert comparison == load(source_root / case / "comparison.json")
        screens = load(source_root / case / "screen.json")
        assert screens == comparison["trials"]
        assert [row["variant"] for row in screens] == list(VARIANTS)
        baseline = load(BASELINE / case / "schedule_capped.json")["resources"]
        assert comparison["baseline"] == baseline and baseline["logical_qubits"] == CAPS[case]
        for row in screens:
            variant = row["variant"]
            directory = source_root / case / variant
            attribution = changes(auditor, source_root, case, variant)
            ledger = auditor.costs(case, directory)
            assert row["resources"] == ledger["resources"] and ledger["qubit_cap"] == CAPS[case]
            eligible = eligibility(ledger["resources"], baseline, CAPS[case], attribution["clean_leaf_work_or_scratch_improved"])
            delta_t = ledger["resources"]["t_count"] - baseline["t_count"]
            assert row["eligible"] == eligible
            assert row["clean_leaf_work_or_scratch_improved"] == attribution["clean_leaf_work_or_scratch_improved"]
            assert row["changed_calls"] == attribution["changed_calls"]
            assert row["batches"] == ledger["batch_count"] and row["t_count_change"] == delta_t
            assert abs(row["full_t_depth_gain_percent"] - 100 * (1 - ledger["resources"]["t_depth"] / baseline["t_depth"])) < 1e-9
            assert abs(row["t_count_change_percent"] - 100 * (ledger["resources"]["t_count"] / baseline["t_count"] - 1)) < 1e-9
            ledger.update(variant=variant, eligible=eligible, changes=attribution, t_count_change=delta_t, baseline_resources=baseline, t_depth_change=ledger["resources"]["t_depth"] - baseline["t_depth"], clifford_t_depth_change=ledger["resources"]["clifford_t_depth"] - baseline["clifford_t_depth"])
            trials[case, variant] = ledger
            dump(output / (case + "_" + variant + "_ledger.json"), ledger)
    eligible_variants = [v for v in VARIANTS if all(trials[case, v]["eligible"] for case in CASES)]
    selected = eligible_variants[0] if eligible_variants else None
    assert summary["selected"] == selected and summary["accepted"] == (selected is not None)
    baseline_summary = load(BASELINE / "summary.json")
    final_cases = []
    for case in CASES:
        comparison = next(row for row in summary["cases"] if row["case"] == case)
        if selected is not None:
            chosen = next(row for row in comparison["trials"] if row["variant"] == selected)
            assert comparison["selected"] == chosen and comparison["candidate"] == chosen["resources"]
            assert comparison["accepted"] and comparison["replay_passed"]
            prior = next(row for row in baseline_summary["cases"] if row["case"] == case)["replays"]
            assert len(comparison["replays"]) == len(prior)
            for replay, old in zip(comparison["replays"], prior, strict=True):
                for key in ("label", "inputs", "initial", "expected"):
                    assert replay[key] == old[key]
                assert replay["passed"] and replay["actual"]["values"] == replay["expected"]
                assert replay["actual"]["all_input_and_workspace_bits_restored"]
                assert any(replay["initial"].values())
                assert all(0 <= value < 1 << 72 for value in replay["initial"].values())
            for filename in ("source.json", "target.json", "schedule_capped.json"):
                assert sha(source_root / case / filename) == sha(source_root / case / selected / filename)
            final, effective_source = trials[case, selected], source_root / case
        else:
            assert not comparison.get("accepted", False) and not comparison.get("replay_passed", False)
            assert comparison.get("replays", []) == []
            assert not (source_root / case / "source.json").exists()
            final, effective_source = auditor.costs(case, BASELINE / case), BASELINE / case
        final = dict(final, effective_source=relative(effective_source), selected_variant=selected, new_full_source_replays=len(comparison.get("replays", [])))
        final_cases.append(final)
        dump(output / (case + "_accepted_ledger.json"), final)
        print(case, "PASS", selected or "A11-retained", final["resources"]["t_depth"], flush=True)
    xml_receipts = []
    leaf_root = ROOT / producer_protocol["leaf_receipt"].replace("\\", "/")
    for path in list(source_root.rglob("*.xml")) + list(leaf_root.rglob("*.xml")):
        document = ET.parse(path).getroot()
        suites = [document] if document.tag == "testsuite" else document.findall("testsuite")
        assert suites and all(int(s.get("failures", "0")) == 0 and int(s.get("errors", "0")) == 0 and int(s.get("skipped", "0")) == 0 for s in suites)
        xml_receipts.append(dict(path=relative(path), tests=sum(int(s.get("tests", "0")) for s in suites)))
    verification = load(source_root / "verification.json")
    assert verification["passed"] and verification["pytest_exit_code"] == 0
    assert sum(len(c["replays"]) for c in summary["cases"]) == (4 if selected else 0)
    next_action = (
        "Use the accepted full-source owner ranking for the next bounded local screen. Remaining generic multiplication, square-root and shift leaves require separate exact guarded replacements and full-cap screening. Keep G2-G5 open and carry measured T work and qubit use into physical accounting."
        if selected else
        "Stop this shift-only source branch under its predeclared >=2% both-case threshold; retain A11 unchanged. Keep the exact leaf as a separately proved reusable component. Choose the next dominant generic multiplication or shift limitation from the current accepted owner ranking; any future combined experiment requires a fresh protocol."
    )
    result = dict(passed=True, decision="independent_same_ssa_shift_source_audit", accepted=selected is not None, selected=selected, source_root=relative(source_root), baseline=relative(BASELINE), cases=final_cases, actual_unique_gate_arrays_scanned=len(auditor.array_scans), metadata_locations_checked=len(auditor.leaf_cache), frozen_input_count=len(frozen), exact_arithmetic_certificate=True, pytest_xml_receipts=xml_receipts, new_gate_replays=0, new_producer_full_source_replays=sum(len(c["replays"]) for c in summary["cases"]), G2_G5="unresolved", next_action=next_action, seconds=time.perf_counter() - started)
    dump(output / "summary.json", result)
    dump(output / "verification.json", dict(passed=True, producer_sha256=sha(Path(__file__)), command=[str(Path(sys.executable).resolve()), "-m", "research.limitation_program_20261001.reconcile_shift", "--source-root", relative(source_root), "--output", relative(output)], checks=["Frozen inputs/code/producer manifests", "Actual array gate counts and ASAP depths", "Signed7 unsigned-magnitude, direction and every barrel mux stage", "Actual same-SSA signed7 interval at every changed site and two72 native arguments", "Literal output-copy/reverse cleanup", "Target/fallback bytes and unchanged masks/storage/copies", "Full counts/DAG/first-fit batches/width caps/categories", "Both-case eligibility, acceptance or stop, saved finite tests/replays"], new_replays=0))
    with (output / "NEXT.md").open("x", encoding="utf-8") as handle:
        handle.write("# Next local action\n\n" + next_action + "\n")
    write_report(report, output, selected, trials, final_cases, auditor, next_action)
    assert all(sha(ROOT / name) == digest for name, digest in frozen.items())
    files = {relative(path): sha(path) for path in output.rglob("*") if path.is_file()}
    files[relative(report)] = sha(report)
    dump(output / "manifest.json", dict(files=files, frozen_inputs=frozen, manifest_self_hash_excluded=True))
    print("PASS independent signed7 shift source audit", len(auditor.array_scans), "actual arrays", flush=True)


def write_report(report, output, selected, trials, final_cases, auditor, next_action):
    lines = ["# Independent signed7-count shift source audit\n\n", "The sole local signed7-count barrel-shift candidate was reconciled against actual emitted arrays, the accepted A11 circuits and unchanged financial targets. This audit runs no new financial or gate replay.\n\n", "| Case | Candidate T gates | T change | Candidate T-depth | T-depth gain | Candidate CT-depth | Qubits / cap | Eligible |\n|---|---:|---:|---:|---:|---:|---:|---|\n"]
    for case in CASES:
        row = trials[case, "signed7-barrel"]
        r, baseline = row["resources"], row["baseline_resources"]
        lines.append(f"| {case} | {r['t_count']:,} | {row['t_count_change']:+,} | {r['t_depth']:,} | {100*(1-r['t_depth']/baseline['t_depth']):.4f}% | {r['clifford_t_depth']:,} | {r['logical_qubits']:,} / {row['qubit_cap']:,} | {row['eligible']} |\n")
    lines.append("\nThe predeclared rule requires at least 2% complete capped T-depth reduction separately in both cases, no Clifford+T-depth increase, the current actual qubit caps and T work or scratch improvement for every changed clean leaf. ")
    lines.append("The candidate passed and all four saved full-source replays were reconciled.\n\n" if selected else "The candidate failed the adoption gate; A11 remains accepted. No new financial replay was run under the declared stop rule.\n\n")
    lines.append(f"The scanner checked {len(auditor.array_scans)} unique gate arrays and {len(auditor.leaf_cache)} metadata locations. All 78 B4x12 and 650 B8x52 shift-count arguments have actual validated SSA intervals within [-64,63], without sampling. The native interface keeps two distinct full 72-bit arguments and one full 72-bit arbitrary-XOR output. Compact masks, retained storage and argument/output copy counts are unchanged. Every nonspecialized metadata and gate file matches A11 bytes, including narrowed sqrt, generic prefix multiplication and all 32 literal lookup rows.\n\n")
    lines.append("Magnitude arithmetic uses unsigned 7-bit words: the signed minimum -64 becomes unsigned 64. Direction follows the financial IR: nonnegative counts shift left modulo 2^72; negative counts shift right arithmetically. Conditional bit reversal before and after one left-shift barrel gives the negative direction, with fill equal to count-sign AND original data-sign. Each conditional stage shifts by 2^j with exact fill and a difference ancilla restored immediately for reuse. Their composition yields the declared digital shift for all 72-bit data under the guard. Actual forward gate parsing checks magnitude construction, both reversals, every mux stage, signed fill, 72 output CX gates and the literal reverse cleanup. The largest magnitude 64 is smaller than 72, which justifies removing the oversized-count branch only under this proved contract.\n\n")
    for row in final_cases:
        r=row["resources"]
        lines.append(f"## Effective {row['case']} ledger\n\nSource: `{row['effective_source']}`. T gates:{r['t_count']:,}; T-depth:{r['t_depth']:,}; Clifford+T-depth:{r['clifford_t_depth']:,}; qubits:{r['logical_qubits']:,}. Independently recomputed forward DAG depth:{row['independent_forward_dependency_t_depth']:,}; compact argument/output copyCX:{row['compact_total_copy_cx']:,}. Retained SSA storage:{row['retained_ssa_qubits']:,}; named output:{row['named_output_qubits']}; peak private scratch:{row['peak_private_scratch_qubits']:,}.\n\n| Category | T gates | Overlapping capped T-depth diagnostic |\n|---|---:|---:|\n")
        for name, category in row["category_costs"].items():
            lines.append(f"| {name} | {category.get('t_count',0):,} | {category.get('overlapping_capped_t_depth_diagnostic',0):,} |\n")
        lines.append("\nTop deterministic depth-owner leaves:\n\n")
        for leaf in row["top_three_depth_owner_leaves"]:
            lines.append(f"- `{leaf['leaf']}`:{leaf['op']},{leaf['params']},{leaf['exclusive_batch_t_depth']:,} attributed layers; hypothetical fixed-batch zero-cost saving{leaf['optimistic_fixed_batch_zero_cost_saving']:,}.\n")
    lines.append("\nCategory depth diagnostics overlap and cannot be added. Zero-cost owner diagnostics do not establish attainable speedup. Serial and actual compact resource counts were reconciled separately.\n\n"+next_action+"\n\nG2 continuous-dollar certification, G3 compatible99% estimator scheduling, G4 matched classical timing and G5 physical10x runtime accounting remain unresolved. This screen establishes no quantum advantage. Everything remained local.\n\n")
    lines.append(f"Receipts:[summary](../../{relative(output)}/summary.json),[complete audit](../../{relative(output)}/),[auditor](../../research/limitation_program_20261001/reconcile_shift.py).\n")
    with report.open("x",encoding="utf-8",newline="\n") as handle:
        handle.write("".join(lines))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.source_root, args.output)
