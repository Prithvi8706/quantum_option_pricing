"""Independent actual-gate and complete-source audit of signed-range multiplication.

No emitted gates or financial paths are replayed here. Saved tests and pricing
replays are reconciled after independent algebra, actual-array parsing and cost
accounting. All historical producers and receipts remain immutable.
"""

from __future__ import annotations

# ruff: noqa: E501

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import random
import shutil
import sys
import time

import numpy as np

from research.limitation_program_20261001.baseline import (
    CATEGORIES,
    COUNT_FIELDS,
    ROOT,
    dump,
    environment,
    independent_dag,
    load,
    sha,
)
from research.limitation_program_20261001.compact_ledger import active_bit_certificate
from research.limitation_program_20261001.interval_bounds import bound_graph
from research.limitation_program_20261001.reconcile_constants import (
    ORIGINAL,
    graph_log_proof,
    library_path,
    relative,
)
from research.limitation_program_20261001.reconcile_nonrestoring_v2 import (
    leaf_eligibility,
    scan,
    xml_receipts,
)
from research.limitation_program_20261001.reconcile_shift import (
    Auditor as ShiftAuditor,
    eligibility,
)
from research.limitation_program_20261001.reconcile_sqrt import (
    check_manifest,
    independently_pack,
    input_files,
)

BASELINE = ROOT / "results/limitation_program_20261001/A11_nonrestoring_run001"
CASES = ("B4x12", "B8x52")
CAPS = {"B4x12": 550141, "B8x52": 4460481}
PORTFOLIOS = ("mixed40", "mixed24-40")
BINS = (24, 40, 72)
LOWERING = "signed-range-complement-csa-prefix-final-v1"
ALGORITHM = "ordered-signed-active-planes-brent-kung"
INTEGRATION = "same-target-signed-range-multiplier-library-v1"
DIMENSIONS = ("t_count", "t_depth", "clifford_t_depth", "qubits")


class Auditor(ShiftAuditor):
    """Versioned resource body; independently prove both actual signed intervals."""

    def range_proof(self, target, node_index, contract):
        assert set(contract) == {"signed_operand_bits"}
        bits = contract["signed_operand_bits"]
        assert type(bits) is list and len(bits) == 2
        assert all(type(b) is int and b in BINS for b in bits)
        assert bits != [72, 72]
        assert (target["width"], target["fraction_bits"]) == (72, 40)
        node = target["nodes"][node_index]
        assert node["op"] == "mul" and node["params"] == {}
        assert len(node["args"]) == 2 and len(node["out"]) == 1
        assert node["out"][0] not in node["args"]
        key = id(target)
        if not hasattr(self, "interval_cache"):
            self.interval_cache = {}
        if key not in self.interval_cache:
            self.interval_cache[key] = (target, bound_graph(target))
        cached, (intervals, rules) = self.interval_cache[key]
        assert cached is target
        proofs = []
        for value, active in zip(node["args"], bits, strict=True):
            low, high = intervals[value]
            assert -(1 << (active - 1)) <= low <= high < 1 << (active - 1)
            proofs.append(
                dict(value=value, bounds=[low, high], signed_bits=active, rule=rules[value])
            )
        return dict(
            node_index=node_index,
            input_values=node["args"],
            output_value=node["out"][0],
            operands=proofs,
            both_signed_guards_proved=True,
            all_declared_input_bit_patterns=True,
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
        labels, op_names, proofs, unsigned_proofs, shift_proofs, range_proofs = (
            [],
            [],
            [],
            [],
            [],
            [],
        )
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
            assert set(contract) <= {
                "zero_low_bits",
                "signed_upper_bits",
                "unsigned_input_bits",
                "signed_shift_count_bits",
                "signed_operand_bits",
            }
            if "signed_operand_bits" in contract:
                range_proofs.append(self.range_proof(target, node_index, contract))
                assert entry["args"] == [list(range(72)), list(range(72, 144))]
                assert entry["outs"] == [list(range(144, 216))]
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
            signed_operand_range_proofs=range_proofs,
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
    """Independent signed polynomial and full-modulus complement identity."""
    checks = negative_products = tiny_negative = 0

    def check(width, fraction, left_bits, right_bits, left, right):
        nonlocal checks, negative_products, tiny_negative
        n, modulus = width + fraction, 1 << (width + fraction)
        a, b = left % (1 << left_bits), right % (1 << right_bits)
        correction = encoded = 0
        for i in range(right_bits):
            for j in range(left_bits):
                if i + j >= n:
                    continue
                bit = ((a >> j) & 1) & ((b >> i) & 1)
                negative = (i == right_bits - 1) != (j == left_bits - 1)
                correction -= (1 << (i + j)) if negative else 0
                encoded += ((1 - bit) if negative else bit) << (i + j)
        product = (encoded + correction % modulus) % modulus
        assert product == (left * right) % modulus
        actual = (product >> fraction) % (1 << width)
        assert actual == (left * right // (1 << fraction)) % (1 << width)
        negative_products += left * right < 0
        tiny_negative += -(1 << fraction) < left * right < 0
        checks += 1

    for left_bits in range(1, 5):
        for right_bits in range(1, 5):
            for fraction in range(7):
                width = max(left_bits, right_bits, fraction, 1)
                for left in range(-(1 << (left_bits - 1)), 1 << (left_bits - 1)):
                    for right in range(-(1 << (right_bits - 1)), 1 << (right_bits - 1)):
                        check(width, fraction, left_bits, right_bits, left, right)
    rng = random.Random(0xA09C057)
    for left_bits in BINS:
        for right_bits in BINS:
            if (left_bits, right_bits) == (72, 72):
                continue
            a_edges = (
                -(1 << (left_bits - 1)),
                -(1 << (left_bits - 1)) + 1,
                -1,
                0,
                1,
                (1 << (left_bits - 1)) - 1,
            )
            b_edges = (
                -(1 << (right_bits - 1)),
                -(1 << (right_bits - 1)) + 1,
                -1,
                0,
                1,
                (1 << (right_bits - 1)) - 1,
            )
            for left in a_edges:
                for right in b_edges:
                    check(72, 40, left_bits, right_bits, left, right)
            for _ in range(32):
                left = rng.randrange(-(1 << (left_bits - 1)), 1 << (left_bits - 1))
                right = rng.randrange(-(1 << (right_bits - 1)), 1 << (right_bits - 1))
                check(72, 40, left_bits, right_bits, left, right)
    assert negative_products and tiny_negative
    return dict(
        passed=True,
        finite_bookkeeping_inputs=checks,
        negative_products=negative_products,
        tiny_negative_products=tiny_negative,
        signed_identity="a=sum(low ai*2**i)-a_sign*2**(abits-1), likewise b; distributivity makes a term negative iff exactly one factor is its active sign bit",
        complement_identity="For t in {0,1}, -t*2**column=(1-t)*2**column-2**column. Sum fixed corrections modulo the FULL 2**(native_width+fraction_bits), including high sign extension",
        carry_identity="Fresh sum=x XOR y XOR z; carry=(x AND y) XOR ((x XOR y) AND z). The two carry terms are disjoint, so sum+2*carry=x+y+z. No low column is discarded",
        prefix_identity="A prefix pair is G (carry generated) and P (all propagate); G*P=0. Composition (Gh XOR Ph*Gl, Ph*Pl) exactly represents the concatenated interval. Addition output bit=propagate XOR preceding prefix G",
        slice_identity="For any integer p, ((p mod 2**(w+f)) >> f) equals floor(p/2**f) mod 2**w, including negative products smaller in magnitude than 2**f",
        sign_extension_policy="Active signed intervals prove every high native input bit equals its active sign bit. Native inputs/output remain full width; compute does not target inputs or externally supplied output",
        cleanup="All partial, correction, CSA and prefix scratch wires are retained and charged; native output XOR followed by literal reverse restores every workspace bit",
        all_guarded_input_algebraic_identity=True,
        proof_scope="All guarded signed inputs follow from these identities. Finite arithmetic and saved emitted tests check realization; no exhaustive72-bit, continuous-dollar or physical advantage certification",
    )


def expected_spec(width, fraction, left_bits, right_bits):
    """Canonical independent specification; producer does not supply this object."""
    return dict(
        op="mul",
        width=width,
        fraction_bits=fraction,
        params={},
        variant="brent-kung",
        lowering=LOWERING,
        product_width=width + fraction,
        active_operand_bits=[left_bits, right_bits],
        input_contract={"signed_operand_bits": [left_bits, right_bits]},
        algorithm=ALGORITHM,
        domain="each native operand is the sign extension of its active low word",
        signed_partial_rule="negative iff exactly one operand bit is its active sign bit",
        negative_bit_encoding="complement plus fixed negative weight correction",
        correction_modulus="full native width plus fractional width",
        discarded_low_columns="retained through CSA and final prefix carry",
        cleanup="native output XOR; literal inverse of complete compute",
    )


def structure(entry, path):
    """Parse actual partial, correction, CSA, prefix, copy and inverse gates."""
    assert sha(path) == entry["sha256"]
    spec = entry["spec"]
    width, fraction = spec["width"], spec["fraction_bits"]
    left_bits, right_bits = spec["active_operand_bits"]
    assert (width, fraction) == (72, 40)
    assert left_bits in BINS and right_bits in BINS and (left_bits, right_bits) != (72, 72)
    canonical = expected_spec(width, fraction, left_bits, right_bits)
    if "integration_lowering" in spec:
        canonical["integration_lowering"] = INTEGRATION
    assert spec == canonical, (spec, canonical)
    assert (
        entry["key"]
        == hashlib.sha256(
            json.dumps(canonical, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
        ).hexdigest()[:20]
    )
    assert entry["op"] == "mul" and entry["params"] == {}
    assert entry["input_contract"] == {"signed_operand_bits": [left_bits, right_bits]}
    assert entry["args"] == [list(range(width)), list(range(width, 2 * width))]
    assert entry["outs"] == [list(range(2 * width, 3 * width))]
    gates = np.load(path, mmap_mode="r")
    assert (len(gates) - width) % 2 == 0
    half = (len(gates) - width) // 2
    before, copied, after = gates[:half], gates[half : half + width], gates[half + width :]
    assert np.array_equal(before, after[::-1])
    assert not np.isin(before[:, 1:], np.arange(2 * width, 3 * width)).any()
    cursor, position, n = 3 * width, 0, width + fraction

    def allocate(size):
        nonlocal cursor
        wires = list(range(cursor, cursor + size))
        cursor += size
        return wires

    def expect(wires):
        nonlocal position
        row = before[position]
        assert int(row[0]) == len(wires)
        assert tuple(map(int, row[1 : 1 + len(wires)])) == tuple(wires), (
            position,
            row.tolist(),
            wires,
        )
        assert wires[-1] >= 3 * width, ("Native input/output targeted by compute", position)
        position += 1

    columns = [[] for _ in range(n)]
    correction = partials = negatives = 0
    for i in range(right_bits):
        for j in range(left_bits):
            if i + j >= n:
                continue
            wire = allocate(1)[0]
            negative = (i == right_bits - 1) != (j == left_bits - 1)
            if negative:
                expect((wire,))
                correction -= 1 << (i + j)
                negatives += 1
            expect((j, width + i, wire))
            columns[i + j].append(wire)
            partials += 1
    correction %= 1 << n
    correction_wires = 0
    for column in range(n):
        if correction & (1 << column):
            wire = allocate(1)[0]
            expect((wire,))
            columns[column].append(wire)
            correction_wires += 1
    layers = compressors = 0
    while max(map(len, columns)) > 2:
        following = [[] for _ in range(n)]
        for column, values in enumerate(columns):
            consumed = 0
            for offset in range(0, len(values) - 2, 3):
                x, y, z = values[offset : offset + 3]
                summed = allocate(1)[0]
                expect((x, summed))
                expect((y, summed))
                if column + 1 < n:
                    carry = allocate(1)[0]
                    expect((x, y, carry))
                    expect((summed, z, carry))
                    following[column + 1].append(carry)
                expect((z, summed))
                following[column].append(summed)
                consumed = offset + 3
                compressors += 1
            following[column].extend(values[consumed:])
        columns = following
        layers += 1
    left, right, product = (allocate(n) for _ in range(3))
    for column, values in enumerate(columns):
        if values:
            expect((values[0], left[column]))
        if len(values) == 2:
            expect((values[1], right[column]))
    # Independently parse the exact mapped child prefix adder, including its
    # own clean-XOR copy and inverse; no circuit builder is imported or called.
    propagate, generate = allocate(n), allocate(n - 1)
    prefix_start = position
    for bit in range(n):
        expect((left[bit], propagate[bit]))
        expect((right[bit], propagate[bit]))
        if bit < n - 1:
            expect((left[bit], right[bit], generate[bit]))
    pairs = list(zip(generate, propagate[: n - 1]))
    prefix_nodes = 0

    def compose(high, low):
        nonlocal prefix_nodes
        g, p = allocate(2)
        gh, ph = high
        gl, pl = low
        expect((gh, g))
        expect((ph, gl, g))
        expect((ph, pl, p))
        prefix_nodes += 1
        return g, p

    distance = 1
    while distance < len(pairs):
        previous, updated = pairs, pairs.copy()
        for bit in range(2 * distance - 1, len(pairs), 2 * distance):
            updated[bit] = compose(previous[bit], previous[bit - distance])
        pairs = updated
        distance *= 2
    distance //= 4
    while distance >= 1:
        previous, updated = pairs, pairs.copy()
        for bit in range(3 * distance - 1, len(pairs), 2 * distance):
            updated[bit] = compose(previous[bit], previous[bit - distance])
        pairs = updated
        distance //= 2
    prefix_end = position
    for bit, target in enumerate(product):
        expect((propagate[bit], target))
        if bit:
            expect((pairs[bit - 1][0], target))
    reversed_count = prefix_end - prefix_start
    assert np.array_equal(
        before[position : position + reversed_count], before[prefix_start:prefix_end][::-1]
    )
    position += reversed_count
    assert position == half
    assert np.array_equal(copied[:, 0], np.full(width, 2))
    assert np.array_equal(copied[:, 1], product[fraction : fraction + width])
    assert np.array_equal(copied[:, 2], np.arange(2 * width, 3 * width))
    assert cursor == entry["resources"]["qubits"]
    return dict(
        passed=True,
        parsed_forward_gates=half,
        active_operand_bits=[left_bits, right_bits],
        full_modular_product_bits=n,
        signed_partial_terms=partials,
        complemented_negative_terms=negatives,
        fixed_full_modulus_correction=correction,
        charged_correction_wires=correction_wires,
        csa_layers=layers,
        compressors=compressors,
        prefix_nodes=prefix_nodes,
        every_low_column_and_carry_retained=True,
        full_native_argument_bits=[width, width],
        full_native_output_bits=width,
        native_inputs_untouched=True,
        arbitrary_output_xor=True,
        literal_forward_reverse_cleanup=True,
        qubits=cursor,
        algorithm="independent actual-gate signed-plane, CSA and Brent-Kung parser",
    )


def minimum_signed_bits(low, high, width=72):
    assert type(low) is int and type(high) is int and low <= high
    for active in range(1, width + 1):
        if -(1 << (active - 1)) <= low <= high < 1 << (active - 1):
            return active
    raise AssertionError("Interval outside native signed word")


def selected_pair(node, bounds, portfolio, eligible_pairs):
    if node["op"] != "mul" or node["params"] != {}:
        return None
    assert len(node["args"]) == 2 and len(node["out"]) == 1
    bins = (40, 72) if portfolio == "mixed40" else BINS
    pair = tuple(
        next(b for b in bins if minimum_signed_bits(*bounds[value]) <= b) for value in node["args"]
    )
    return pair if pair != (72, 72) and pair in eligible_pairs else None


def source_changes(auditor, source_root, leaf_entries, case, portfolio):
    directory = source_root / case / portfolio
    before, after = (load(path / "source.json") for path in (BASELINE / case, directory))
    target = load(directory / "target.json")
    assert sha(directory / "target.json") == sha(BASELINE / case / "target.json")
    for field in (
        "format",
        "word_width",
        "fraction_bits",
        "values",
        "inputs",
        "outputs",
        "clean_schedule",
        "invocation_semantics",
        "inverse_semantics",
        "exact_clifford_t",
        "arbitrary_rotations",
    ):
        assert before[field] == after[field], field
    old_entries, new_entries = auditor.leafs(before), auditor.leafs(after)
    old_archive, new_archive = library_path(before), library_path(after)
    bounds, _ = bound_graph(target)
    noninputs = [i for i, node in enumerate(target["nodes"]) if node["op"] != "input"]
    eligible_pairs = set(leaf_entries)
    changed, unchanged, structures, proofs, pairs = [], set(), {}, [], Counter()
    for call_index, (old, new) in enumerate(
        zip(before["forward_calls"], after["forward_calls"], strict=True)
    ):
        assert {k: v for k, v in old.items() if k != "leaf"} == {
            k: v for k, v in new.items() if k != "leaf"
        }
        old_entry, new_entry = old_entries[old["leaf"]], new_entries[new["leaf"]]
        node_index = noninputs[call_index]
        node = target["nodes"][node_index]
        pair = selected_pair(node, bounds, portfolio, eligible_pairs)
        assert (old["leaf"] != new["leaf"]) == (pair is not None), (
            case,
            portfolio,
            call_index,
            pair,
        )
        if pair is None:
            key = old["leaf"]
            if key not in unchanged:
                assert sha(old_archive / (key + ".json")) == sha(new_archive / (key + ".json"))
                assert sha(old_archive / old_entry["gate_file"]) == sha(
                    new_archive / new_entry["gate_file"]
                )
                unchanged.add(key)
            continue
        leaf_entry = leaf_entries[pair]
        assert new_entry["resources"] == leaf_entry["resources"]
        assert new_entry["sha256"] == leaf_entry["sha256"]
        assert {
            k: v for k, v in new_entry["spec"].items() if k != "integration_lowering"
        } == leaf_entry["spec"]
        proofs.append(auditor.range_proof(target, node_index, new_entry["input_contract"]))
        if new["leaf"] not in structures:
            structures[new["leaf"]] = structure(new_entry, new_archive / new_entry["gate_file"])
        pairs[pair] += 1
        changed.append(
            dict(
                call_index=call_index,
                args=new["args"],
                out=new["out"],
                old_key=old["leaf"],
                new_key=new["leaf"],
                op="mul",
                params={},
                old_resources=old_entry["resources"],
                new_resources=new_entry["resources"],
                input_contract=new_entry["input_contract"],
            )
        )
    assert load(directory / "changed_calls.json") == dict(
        changes=changed, unchanged_leaf_keys=sorted(unchanged)
    )
    decisions = load(directory / "site_decisions.json")
    assert len(decisions) == len(after["forward_calls"])
    assert {d["forward_call_index"] for d in decisions} == set(range(len(after["forward_calls"])))
    for row in decisions:
        index = row["forward_call_index"]
        assert row["node_index"] == noninputs[index]
        node = target["nodes"][row["node_index"]]
        assert row["outputs"] == node["out"] and row["op"] == node["op"]
        assert row["old_key"] == before["forward_calls"][index]["leaf"]
        assert row["new_key"] == after["forward_calls"][index]["leaf"]
        if row["old_key"] != row["new_key"]:
            proof = row["proof"]
            assert proof["input_values"] == node["args"] and proof["output_value"] == node["out"][0]
            assert proof["input_bounds"] == [list(bounds[value]) for value in node["args"]]
            assert proof["minimum_signed_operand_bits"] == [
                minimum_signed_bits(*bounds[value]) for value in node["args"]
            ]
            assert (
                proof["signed_operand_bits"]
                == new_entries[row["new_key"]]["input_contract"]["signed_operand_bits"]
            )
            assert (
                proof["both_operand_guards_proved"] is True
                and proof["all_declared_input_patterns"] is True
            )
        else:
            assert row["type"] == "fallback"
    schedule, old_schedule = (
        load(path / "schedule_capped.json") for path in (directory, BASELINE / case)
    )
    assert schedule["format"] == "compact-clean-xor-capped-wave-schedule-v6"
    for field in (
        "widths",
        "offsets",
        "retained_ssa_qubits",
        "proof_masks",
        "proof_reasons",
        "argument_and_output_copy_cx",
        "baseline_argument_and_output_copy_cx",
    ):
        assert schedule[field] == old_schedule[field], (case, portfolio, field)
    independently_pack(after, new_entries, schedule)
    improved = all(
        row["new_resources"]["t_count"] < row["old_resources"]["t_count"]
        or row["new_resources"]["qubits"] < row["old_resources"]["qubits"]
        for row in changed
    )
    return dict(
        changed_calls=len(changed),
        changed_pair_counts=[
            dict(active_bits=list(pair), calls=count) for pair, count in sorted(pairs.items())
        ],
        unchanged_leaf_keys=len(unchanged),
        actual_both_operand_signed_proofs=proofs,
        structural_leaf_proofs=structures,
        storage_and_copy_allocation_unchanged=True,
        exact_first_fit_groups_recomputed=True,
        clean_leaf_work_or_scratch_improved=bool(changed) and improved,
    )


def freeze(leaf_root, source_root):
    frozen = {}
    roots = [BASELINE, leaf_root] + ([source_root] if source_root else [])
    for directory in roots:
        check_manifest(directory)
        for path in directory.rglob("*"):
            if path.is_file():
                frozen[relative(path)] = sha(path)
        manifest = load(directory / "manifest.json")
        for field in ("external_files", "frozen_inputs", "dependency_sha256"):
            for name, expected in manifest.get(field, {}).items():
                assert sha(ROOT / name) == expected
                frozen[name.replace("\\", "/")] = expected
        for row in load(directory / "protocol.json").get("executed_dependencies", []):
            assert sha(directory / row["snapshot"]) == row["sha256"]
            assert sha(ROOT / row["source"]) == row["sha256"]
            frozen[row["source"].replace("\\", "/")] = row["sha256"]
    for case in CASES:
        for path in input_files(BASELINE / case):
            frozen[relative(path)] = sha(path)
        if source_root:
            for portfolio in PORTFOLIOS:
                for path in input_files(source_root / case / portfolio):
                    frozen[relative(path)] = sha(path)
        path = ORIGINAL / (case + "_accounting.json")
        frozen[relative(path)] = sha(path)
    frozen[relative(ORIGINAL / "manifest.json")] = sha(ORIGINAL / "manifest.json")
    for name in (
        "research.controlled_source_completion.primitives",
        "research.limitation_program_20261001.baseline",
        "research.limitation_program_20261001.interval_bounds",
        "research.limitation_program_20261001.reconcile_constants",
        "research.limitation_program_20261001.reconcile_sqrt",
        "research.limitation_program_20261001.reconcile_shift",
        "research.limitation_program_20261001.reconcile_nonrestoring_v2",
        "research.limitation_program_20261001.compact_ledger",
    ):
        path = Path(sys.modules[name].__file__)
        frozen[relative(path)] = sha(path)
    frozen[relative(Path(__file__))] = sha(Path(__file__))
    return frozen


def run(leaf_root, source_root, output):
    leaf_root, output = leaf_root.resolve(), output.resolve()
    source_root = source_root.resolve() if source_root else None
    frozen = freeze(leaf_root, source_root)
    output.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    dump(
        output / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            before_analysis=True,
            local_only=True,
            leaf_root=relative(leaf_root),
            source_root=relative(source_root) if source_root else None,
            baseline=relative(BASELINE),
            frozen_inputs=frozen,
            producer_sha256=sha(Path(__file__)),
            family=list(PORTFOLIOS),
            active_widths=list(BINS),
            width=72,
            fraction_bits=40,
            scope="Independent read-only actual-array signed polynomial, full correction/carry, cleanup and complete-source resource audit; no emitted gate or financial replay",
            selection="Nondominated leaf with strict improvement and T-work or scratch improvement; full source >=2% capped T-depth in each case, CT-depth<=baseline, actual caps, no whole-source domination. Minimize sum(T-depth), then sum(T-count), then sum(qubits), then declared portfolio order",
            no_new_emitted_replays=True,
            G2_G5="unresolved",
        ),
    )
    dump(output / "environment.json", environment())
    executed = output / "executed_code"
    executed.mkdir()
    shutil.copyfile(Path(__file__), executed / "reconcile_range.py")
    certificate = arithmetic_certificate()
    dump(output / "range_arithmetic_certificate.json", certificate)
    leaf_summary, leaf_protocol = (
        load(leaf_root / name) for name in ("summary.json", "protocol.json")
    )
    assert leaf_summary["passed"] and leaf_protocol["local_only"] is True
    assert (leaf_protocol["width"], leaf_protocol["fraction_bits"]) == (72, 40)
    assert leaf_protocol["active_widths"] == list(BINS)
    assert leaf_protocol["resource_dimensions"] == list(DIMENSIONS)
    verification = load(leaf_root / "verification.json")
    assert verification["passed"] and verification["pytest_exit_code"] == 0
    auditor = Auditor(frozen)
    baseline_ledgers = {case: auditor.costs(case, BASELINE / case) for case in CASES}
    accepted_entries = []
    for case in CASES:
        entries = auditor.leafs(load(BASELINE / case / "source.json"))
        generic = [entry for entry in entries.values() if entry["op"] == "mul"]
        assert len(generic) == 1
        accepted_entries.append(generic[0])
    assert accepted_entries[0] == accepted_entries[1]
    baseline_resources = accepted_entries[0]["resources"]
    assert leaf_summary["baseline_multiplier"] == baseline_resources
    all_entries, eligible_entries, leaf_rows = {}, {}, []
    for row in leaf_summary["candidates"]:
        entry = row["metadata"]
        pair = tuple(row["active_bits"])
        assert pair not in all_entries and list(pair) == entry["spec"]["active_operand_bits"]
        matches = [p for p in leaf_root.rglob(entry["key"] + ".json") if load(p) == entry]
        assert len(matches) == 1
        path = matches[0].parent / entry["gate_file"]
        scanned, parsed = scan(entry, path), structure(entry, path)
        auditor.array_scans[entry["sha256"], entry["resources"]["qubits"]] = scanned
        decision = leaf_eligibility(entry["resources"], baseline_resources)
        for key, independent_key in (
            ("leaf_nondominated", "leaf_nondominated"),
            ("any_resource_improvement", "strict_any_metric_improvement"),
            ("clean_leaf_work_or_scratch_improved", "clean_leaf_work_or_scratch_improved"),
            ("source_screen_allowed", "source_screen_allowed"),
        ):
            assert row[key] == decision[independent_key]
        all_entries[pair] = entry
        if decision["source_screen_allowed"]:
            eligible_entries[pair] = entry
        leaf_rows.append(
            dict(
                active_bits=list(pair),
                actual_gate_scan=scanned,
                structural_parser=parsed,
                decision=decision,
            )
        )
    assert set(all_entries) == {(a, b) for a in BINS for b in BINS if (a, b) != (72, 72)}
    assert leaf_summary["source_screen_allowed"] == bool(eligible_entries)
    assert (
        not leaf_summary["financial_gate_replays_run"] and not leaf_summary["source_gain_claimed"]
    )
    assert bool(source_root) == bool(eligible_entries)
    dump(
        output / "leaf_audit.json",
        dict(
            passed=True,
            baseline_resources=baseline_resources,
            candidates=leaf_rows,
            eligible_pairs=[list(pair) for pair in sorted(eligible_entries)],
        ),
    )
    selected, final_cases, trials = None, [], {}
    if source_root:
        summary, protocol = (load(source_root / name) for name in ("summary.json", "protocol.json"))
        assert summary["passed"] and protocol["family"] == list(PORTFOLIOS)
        assert (ROOT / protocol["baseline"]).resolve() == BASELINE.resolve()
        assert protocol["threshold_percent"] == 2 and protocol["active_widths"] == list(BINS)
        assert {tuple(pair) for pair in protocol["allowed_pairs"]} == set(eligible_entries)
        assert protocol["cases"] == list(CASES) and protocol["cpu_limit_seconds"] == 1800
        assert protocol["local_only"] is True and summary["cpu_seconds"] <= 1800
        for name, digest in protocol["baseline_hashes"].items():
            assert sha(BASELINE / name) == digest
        for name, digest in protocol["baseline_leaf_hashes"].items():
            assert sha(ROOT / name) == digest
        baseline_summary = load(BASELINE / "summary.json")
        assert protocol["replay_inputs"] == {
            row["case"]: row["replays"] for row in baseline_summary["cases"]
        }
        assert sha(leaf_root / "manifest.json") == protocol["leaf_receipt_manifest_sha256"]
        for case in CASES:
            comparison = next(row for row in summary["cases"] if row["case"] == case)
            assert comparison == load(source_root / case / "comparison.json")
            screens = load(source_root / case / "screen.json")
            assert screens == comparison["trials"] and [row["variant"] for row in screens] == list(
                PORTFOLIOS
            )
            baseline = baseline_ledgers[case]["resources"]
            assert baseline["logical_qubits"] == CAPS[case] and comparison["baseline"] == baseline
            for row in screens:
                portfolio = row["variant"]
                attribution = source_changes(
                    auditor, source_root, eligible_entries, case, portfolio
                )
                ledger = auditor.costs(case, source_root / case / portfolio)
                assert row["resources"] == ledger["resources"] and ledger["qubit_cap"] == CAPS[case]
                eligible = eligibility(
                    ledger["resources"],
                    baseline,
                    CAPS[case],
                    attribution["clean_leaf_work_or_scratch_improved"],
                )
                assert (
                    row["eligible"] == eligible
                    and row["changed_calls"] == attribution["changed_calls"]
                )
                assert (
                    row["clean_leaf_work_or_scratch_improved"]
                    == attribution["clean_leaf_work_or_scratch_improved"]
                )
                assert row["batches"] == ledger["batch_count"]
                assert row["t_count_change"] == ledger["resources"]["t_count"] - baseline["t_count"]
                assert (
                    abs(
                        row["t_count_change_percent"]
                        - 100 * (ledger["resources"]["t_count"] / baseline["t_count"] - 1)
                    )
                    < 1e-9
                )
                assert (
                    abs(
                        row["full_t_depth_gain_percent"]
                        - 100 * (1 - ledger["resources"]["t_depth"] / baseline["t_depth"])
                    )
                    < 1e-9
                )
                assert all(
                    row[field] is True
                    for field in (
                        "target_bytes_unchanged",
                        "ssa_storage_and_copy_accounting_unchanged",
                        "fallback_metadata_and_gate_bytes_unchanged",
                    )
                )
                ledger.update(
                    variant=portfolio,
                    eligible=eligible,
                    changes=attribution,
                    baseline_resources=baseline,
                )
                trials[case, portfolio] = ledger
                dump(output / (case + "_" + portfolio + "_trial_ledger.json"), ledger)

        def dominated(portfolio):
            dims = ("t_count", "t_depth", "clifford_t_depth", "logical_qubits")
            return any(
                other != portfolio
                and all(
                    trials[case, other]["resources"][d] <= trials[case, portfolio]["resources"][d]
                    for case in CASES
                    for d in dims
                )
                and any(
                    trials[case, other]["resources"][d] < trials[case, portfolio]["resources"][d]
                    for case in CASES
                    for d in dims
                )
                for other in PORTFOLIOS
            )

        independent_nondominated = [p for p in PORTFOLIOS if not dominated(p)]
        for comparison in summary["cases"]:
            for row in comparison["trials"]:
                assert row["source_nondominated"] == (row["variant"] in independent_nondominated)
        frontier = load(source_root / "range_frontier.json")
        assert frontier["nondominated"] == independent_nondominated
        assert frontier["variants"] == list(PORTFOLIOS)
        candidates = [
            p
            for p in PORTFOLIOS
            if all(trials[case, p]["eligible"] for case in CASES) and not dominated(p)
        ]
        selected = (
            min(
                candidates,
                key=lambda p: (
                    tuple(
                        sum(trials[case, p]["resources"][d] for case in CASES)
                        for d in ("t_depth", "t_count", "logical_qubits")
                    )
                    + (PORTFOLIOS.index(p),)
                ),
            )
            if candidates
            else None
        )
        assert summary["selected"] == selected and summary["accepted"] == bool(selected)
        assert summary["financial_gate_replays_run"] == bool(selected)
        for case in CASES:
            comparison = next(row for row in summary["cases"] if row["case"] == case)
            if selected:
                trial = trials[case, selected]
                chosen = next(row for row in comparison["trials"] if row["variant"] == selected)
                assert (
                    comparison["selected"] == chosen
                    and comparison["candidate"] == trial["resources"]
                )
                assert comparison["replay_passed"] and comparison["accepted"]
                prior = next(row for row in baseline_summary["cases"] if row["case"] == case)[
                    "replays"
                ]
                assert len(comparison["replays"]) == len(prior)
                for replay, old in zip(comparison["replays"], prior, strict=True):
                    for field in ("label", "inputs", "initial", "expected"):
                        assert replay[field] == old[field]
                    assert replay["passed"] and replay["actual"]["values"] == replay["expected"]
                    assert replay["actual"]["all_input_and_workspace_bits_restored"]
                    assert any(replay["initial"].values())
                for name in ("source.json", "target.json", "schedule_capped.json"):
                    assert sha(source_root / case / name) == sha(
                        source_root / case / selected / name
                    )
                final, effective = trial, source_root / case
            else:
                assert comparison.get("replays", []) == [] and not comparison.get("accepted", False)
                assert not comparison.get("replay_passed", False)
                assert not (source_root / case / "source.json").exists()
                final, effective = baseline_ledgers[case], BASELINE / case
            final_cases.append(
                dict(final, effective_source=relative(effective), selected_variant=selected)
            )
        source_verification = load(source_root / "verification.json")
        assert source_verification["passed"] and source_verification["pytest_exit_code"] == 0
        replay_count = sum(len(row["replays"]) for row in baseline_summary["cases"])
        assert replay_count == 4
        assert sum(len(row["replays"]) for row in summary["cases"]) == (
            replay_count if selected else 0
        )
    else:
        final_cases = [
            dict(
                baseline_ledgers[case],
                effective_source=relative(BASELINE / case),
                selected_variant=None,
            )
            for case in CASES
        ]
    for row in final_cases:
        dump(output / (row["case"] + "_accepted_ledger.json"), row)
    receipts = xml_receipts([leaf_root] + ([source_root] if source_root else []))
    next_action = (
        "Use the accepted complete-source owner ranking for the next bounded local limitation. Keep G2-G5 open and everything local."
        if selected
        else "Retain A11_nonrestoring_run001. Preserve exact range leaves and their measured stop, then move to the next bounded limitation under a fresh protocol. Keep G2-G5 open."
    )
    result = dict(
        passed=True,
        decision="independent_signed_range_multiplier_audit",
        accepted=bool(selected),
        selected=selected,
        source_root=relative(source_root) if source_root else None,
        leaf_root=relative(leaf_root),
        baseline=relative(BASELINE),
        source_screen_run=bool(source_root),
        eligible_pairs=[list(pair) for pair in sorted(eligible_entries)],
        cases=final_cases,
        trials=list(trials.values()),
        actual_unique_gate_arrays_scanned=len(auditor.array_scans),
        metadata_locations_checked=len(auditor.leaf_cache) + len(all_entries),
        frozen_input_count=len(frozen),
        exact_arithmetic_certificate=True,
        pytest_xml_receipts=receipts,
        new_gate_replays=0,
        new_producer_full_source_replays=4 if selected else 0,
        G2_G5="unresolved",
        next_action=next_action,
        seconds=time.perf_counter() - started,
    )
    dump(output / "summary.json", result)
    command = [
        str(Path(sys.executable).resolve()),
        "-m",
        "research.limitation_program_20261001.reconcile_range",
        "--leaf-root",
        relative(leaf_root),
        "--output",
        relative(output),
    ] + (["--source-root", relative(source_root)] if source_root else [])
    dump(
        output / "verification.json",
        dict(
            passed=True,
            producer_sha256=sha(Path(__file__)),
            command=command,
            checks=[
                "Frozen receipts and executed code",
                "Independent signed polynomial/full-modulus complement/carry/slice identities",
                "Every actual partial, correction, CSA and Brent-Kung gate, native copy and literal inverse",
                "Both actual operand intervals and strict typed contract",
                "Unchanged fallback metadata/gates, root/shift/lookup, SSA masks/native copies",
                "Complete serial/parallel counts, DAG, first-fit packing and caps",
                "Both-case eligibility/Pareto/tie-break selection and baseline-derived saved replay cardinality",
            ],
            new_replays=0,
        ),
    )
    with (output / "NEXT.md").open("x", encoding="utf-8") as handle:
        handle.write("# Next local action\n\n" + next_action + "\n")
    report = ROOT / "docs/limitation_program_20261001/RANGE_SOURCE_COSTS.md"
    lines = [
        "# Independent signed-range multiplication audit\n\n",
        "Both complete native arguments remain 72 bits. The narrowed signed plane is allowed only when both actual SSA intervals fit their selected signed widths. The complement correction is reduced modulo the full 112-bit product width; every low carry is retained. The audit parsed every actual partial, correction, compressor, prefix gate, output copy and literal inverse, and ran no new gate or pricing replay.\n\n",
        "| Portfolio | Case | T gates | T-depth | T-depth gain | CT-depth | Qubits / cap | Eligible |\n|---|---|---:|---:|---:|---:|---:|---|\n",
    ]
    for row in trials.values():
        r, b = row["resources"], row["baseline_resources"]
        lines.append(
            f"| {row['variant']} | {row['case']} | {r['t_count']:,} | {r['t_depth']:,} | {100 * (1 - r['t_depth'] / b['t_depth']):.4f}% | {r['clifford_t_depth']:,} | {r['logical_qubits']:,} / {row['qubit_cap']:,} | {row['eligible']} |\n"
        )
    lines.append(
        "\n"
        + (
            f"Adopted `{selected}` after both-case eligibility and four saved complete-source replays.\n\n"
            if selected
            else "The accepted non-restoring baseline is retained. No new complete-source financial replay was run.\n\n"
        )
    )
    lines.append(
        next_action
        + "\n\nG2 continuous-dollar certification, G3 compatible 99% estimator schedule, G4 matched classical timing and G5 physical runtime accounting remain unresolved. This audit establishes no quantum advantage. Everything stayed local.\n\n"
    )
    lines.append(
        f"Receipts: [summary](../../{relative(output)}/summary.json), [complete audit](../../{relative(output)}/), [auditor](../../research/limitation_program_20261001/reconcile_range.py).\n"
    )
    with report.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write("".join(lines))
    assert all(sha(ROOT / name) == digest for name, digest in frozen.items())
    files = {relative(path): sha(path) for path in output.rglob("*") if path.is_file()}
    files[relative(report)] = sha(report)
    dump(
        output / "manifest.json",
        dict(files=files, frozen_inputs=frozen, manifest_self_hash_excluded=True),
    )
    print(
        "PASS independent signed-range audit",
        selected or "nonrestoring-retained",
        len(auditor.array_scans),
        "actual arrays",
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--leaf-root", type=Path, required=True)
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.leaf_root, args.source_root, args.output)
