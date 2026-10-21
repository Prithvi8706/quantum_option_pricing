"""Independent exact-array, proof and cost audit of the local A11 sqrt screen.

The general A01 accounting body is versioned here to recognize the new
unsigned input promise. Historical producers, readers and evidence are intact.
No financial or gate replay is run by this auditor.
"""

from __future__ import annotations

# Complete receipt prose intentionally remains readable.
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
    Auditor as BaseAuditor,
    ORIGINAL,
    graph_log_proof,
    library_path,
    relative,
)

BASELINE = ROOT / "results/limitation_program_20261001/A09_run001"
CASES = ("B4x12", "B8x52")
ALGORITHMS = ("padded-historical", "tight-digit-by-digit")
EMBEDDINGS = ("clean-child-twice", "fused-child-copy")
VARIANTS = tuple(a + "__" + e for a in ALGORITHMS for e in EMBEDDINGS)
CAPS = {"B4x12": 550141, "B8x52": 4460481}
LOWERING = "unsigned-narrow-sqrt-v1"
INTEGRATION_LOWERING = "same-target-unsigned-sqrt-range-v1"


class Auditor(BaseAuditor):
    """Unchanged array scanner plus independently recomputed unsigned guards."""

    def unsigned_proof(self, target, node_index, contract):
        assert contract == {"unsigned_input_bits": 46}
        assert target["width"] == 72 and target["fraction_bits"] == 40
        node = target["nodes"][node_index]
        assert node["op"] == "sqrt" and node["params"] == {}
        assert len(node["args"]) == len(node["out"]) == 1
        key = id(target)
        if not hasattr(self, "interval_cache"):
            self.interval_cache = {}
        if key not in self.interval_cache:
            self.interval_cache[key] = (target, bound_graph(target))
        # Hold the target object in the cache to prevent Python object-ID reuse.
        # Audit targets are private JSON loads and their frozen bytes are checked.
        cached_target, (intervals, rules) = self.interval_cache[key]
        assert cached_target is target
        operand, result = node["args"][0], node["out"][0]
        low, high = intervals[operand]
        assert 0 <= low <= high < 1 << 46, ("Unproved same-SSA unsigned46 promise", node_index, low, high)
        return dict(
            node_index=node_index,
            input_value=operand,
            output_value=result,
            input_bounds=[low, high],
            output_bounds=list(intervals[result]),
            unsigned_input_bits=46,
            all_declared_input_bit_patterns=True,
            finite_samples_used_as_proof=False,
            input_rule=rules[operand],
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
        labels, op_names, proofs, unsigned_proofs = [], [], [], []
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
            assert set(contract) <= {"zero_low_bits", "signed_upper_bits", "unsigned_input_bits"}
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
            interpretation="Exact repeated SSA operands only. These are candidates for a squaring replacement; no squaring arithmetic, attainable capped saving or equivalence is assumed.",
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


def input_files(directory):
    files = [directory / name for name in ("target.json", "source.json", "schedule_capped.json")]
    source = load(directory / "source.json")
    archive = library_path(source)
    for key in source["library_keys"]:
        meta = archive / (key + ".json")
        files.extend((meta, archive / load(meta)["gate_file"]))
    return files


def check_manifest(directory):
    manifest = load(directory / "manifest.json")
    records = manifest.get("files", manifest)
    for name, expected in records.items():
        assert isinstance(expected, str) and len(expected) == 64
        path = directory / name
        if not path.exists():
            path = ROOT / name
        assert sha(path) == expected, ("Producer manifest mismatch", name)
    for name, expected in manifest.get("external_files", {}).items():
        assert sha(ROOT / name) == expected, ("Producer external manifest mismatch", name)


def freeze(source_root):
    summary, protocol = (load(source_root / name) for name in ("summary.json", "protocol.json"))
    assert summary["passed"] and len(summary["cases"]) == 2
    assert (ROOT / protocol["baseline"].replace("\\", "/")).resolve() == BASELINE.resolve()
    assert load(BASELINE / "summary.json")["accepted"]
    check_manifest(source_root)
    frozen = {relative(path): sha(path) for path in source_root.rglob("*") if path.is_file()}
    leaf_root = ROOT / protocol["leaf_receipt"].replace("\\", "/")
    assert sha(leaf_root / "manifest.json") == protocol["leaf_receipt_manifest_sha256"]
    assert load(leaf_root / "summary.json")["passed"]
    check_manifest(leaf_root)
    for path in leaf_root.rglob("*"):
        if path.is_file():
            frozen[relative(path)] = sha(path)
    for name, expected in load(leaf_root / "manifest.json").get("external_files", {}).items():
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
    for module in (
        sys.modules[BaseAuditor.__module__],
        sys.modules["research.limitation_program_20261001.baseline"],
        sys.modules["research.limitation_program_20261001.compact_ledger"],
        sys.modules["research.limitation_program_20261001.interval_bounds"],
        sys.modules["research.controlled_source_completion.primitives"],
    ):
        path = Path(module.__file__)
        frozen[relative(path)] = sha(path)
    frozen[relative(Path(__file__))] = sha(Path(__file__))
    return frozen, protocol


def recurrence_certificate():
    """Integer inductive recurrence and exact bounds, independent of gate replay."""
    # Exhaust all digit truth cases for bounded q/r; the algebra below covers
    # larger q and does not infer a production promise from these finite cases.
    checked = 0
    for q in range(64):
        for remainder in range(2 * q + 1):
            for digit in range(4):
                candidate = 4 * remainder + digit
                take = int(candidate >= 4 * q + 1)
                new_q = 2 * q + take
                new_remainder = candidate - take * (4 * q + 1)
                assert 4 * (q * q + remainder) + digit == new_q * new_q + new_remainder
                assert 0 <= new_remainder < 2 * new_q + 1
                checked += 1
    k = (46 + 40 + 1) // 2
    # Before stage s, q<2**s and r<2*q+1. Hence r<=2*q and
    # 4*r+d <=8*q+3 <2**(s+3); the largest s=k-1 needs k+2 bits.
    stages = []
    for s in range(k):
        maximum_q = (1 << s) - 1
        maximum_candidate = 8 * maximum_q + 3
        maximum_trial = 4 * maximum_q + 1
        assert maximum_candidate < 1 << (k + 2)
        assert maximum_trial < 1 << (k + 2)
        stages.append(dict(stage=s, maximum_root_prefix=maximum_q, maximum_candidate_remainder=maximum_candidate, maximum_trial=maximum_trial))
    return dict(
        passed=True,
        active_input_bits=46,
        fraction_bits=40,
        radicand_bits=86,
        result_bits=k,
        tight_remainder_bits=k + 2,
        recurrence="q' = 2*q + t; r' = 4*r+d-t*(4*q+1), t=[4*r+d >= 4*q+1]",
        invariant="Processed radicand prefix = q*q+r, 0<=r<2*q+1",
        algebraic_induction="t=0 gives r'<4*q+1=2*q'+1; t=1 gives 0<=r'<=4*q+2<2*q'+1. Both preserve the displayed polynomial identity. Final invariant uniquely gives q=floor(sqrt(N)).",
        unsigned_highest_active_bit_permitted=True,
        high_input_zero_required=True,
        arithmetic_no_overflow=True,
        stages=stages,
        finite_recurrence_checks=checked,
        proof_scope="Exact integer recurrence and width bound hold for all promised inputs. Actual comparison/subtraction realization is covered by unchanged primitive semantics, physical structure and saved finite leaf tests; no exhaustive72 input claim.",
    )


def clean_child_structure(gates, output):
    count = len(output)
    assert len(gates) >= count and (len(gates) - count) % 2 == 0
    split = (len(gates) - count) // 2
    before, middle, after = gates[:split], gates[split : split + count], gates[split + count :]
    assert np.array_equal(before, after[::-1])
    assert not np.isin(before[:, 1:], output).any()
    assert np.all(middle[:, 0] == 2) and np.array_equal(middle[:, 2], output)
    assert not np.isin(middle[:, 1], output).any()
    assert len(set(map(int, middle[:, 1]))) == count
    return dict(copy_bits=count, literal_reverse=True, output_never_controls=True, distinct_copy_sources=True)


def structure(entry, path):
    assert sha(path) == entry["sha256"]
    spec = entry["spec"]
    assert entry["op"] == spec["op"] == "sqrt" and entry["params"] == {}
    assert spec["width"] == 72 and spec["fraction_bits"] == 40
    assert spec["active_input_bits"] == 46 and spec["radicand_bits"] == 86
    assert spec["result_bits"] == 43
    assert spec["lowering"] == LOWERING
    assert spec["integration_lowering"] == INTEGRATION_LOWERING
    assert entry["input_contract"] == spec["input_contract"] == {"unsigned_input_bits": 46}
    assert spec["algorithm"] in ALGORITHMS and spec["embedding"] in EMBEDDINGS
    assert entry["args"] == [list(range(72))]
    assert entry["outs"] == [list(range(72, 144))]
    expected_key = hashlib.sha256(json.dumps(spec, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()[:20]
    assert entry["key"] == expected_key
    child_in, child_out, remainder = ((46, 46, 48) if spec["algorithm"] == "padded-historical" else (46, 43, 45))
    assert (spec["child_input_bits"], spec["child_output_bits"], spec["remainder_bits"]) == (child_in, child_out, remainder)
    roots = child_in if spec["algorithm"] == "padded-historical" else child_out
    child_scratch = roots + 44 * remainder + 2 * remainder + 2 * (remainder + 1) + 1
    expected_qubits = 144 + child_scratch + (child_out if spec["embedding"] == "clean-child-twice" else 0)
    assert entry["resources"]["qubits"] == expected_qubits
    gates = np.load(path, mmap_mode="r")
    assert not np.isin(gates[:, 1:], np.arange(46, 72)).any()
    output = np.arange(72, 72 + child_out)
    assert not np.isin(gates[:, 1:], np.arange(72 + child_out, 144)).any()
    if spec["embedding"] == "fused-child-copy":
        outer = clean_child_structure(gates, output)
        cleanup = "Literal surrounding compute/reverse segments"
    else:
        locations = np.flatnonzero(np.isin(gates[:, 1:], output).any(axis=1))
        assert len(locations) == child_out
        assert np.array_equal(locations, np.arange(locations[0], locations[0] + child_out))
        middle = gates[locations]
        assert np.all(middle[:, 0] == 2) and np.array_equal(middle[:, 2], output)
        before, after = gates[: locations[0]], gates[locations[-1] + 1 :]
        assert np.array_equal(before, after)
        product = middle[:, 1]
        assert len(set(map(int, product))) == child_out and not np.isin(product, np.arange(144)).any()
        outer = clean_child_structure(before, product)
        assert not np.isin(before[:, 1:], output).any()
        cleanup = "Repeated self-inverse clean XOR child; its distinct copy CX gates commute"
    return dict(
        algorithm=spec["algorithm"], embedding=spec["embedding"],
        full_width_archival_input_output=True, unsigned_input_bits=46,
        highest_active_bit_kept=True, external_high_output_bits_unchanged=True,
        private_remainders_counted_and_restored=True, output_xor_and_cleanup_structure=outer,
        cleanup_identity=cleanup, qubits=expected_qubits,
        arithmetic_certificate_scope="All-input recurrence induction plus saved finite emitted leaf tests",
    )


def independently_pack(source, entries, schedule):
    """Rebuild predeclared first-fit packing independently of scheduler module."""
    widths, word = schedule["widths"], source["word_width"]
    retained = sum(widths) + len(source["outputs"]) * word
    capacity = schedule["qubit_cap"] - retained
    levels = {v: 0 for node in source["inputs"] for v in node["out"]}
    waves = defaultdict(list)
    for index, call in enumerate(source["forward_calls"]):
        level = 1 + max((levels[v] for v in call["args"]), default=0)
        for value in call["out"]:
            levels[value] = level
        waves[level].append(index)
    groups = []
    calls = source["forward_calls"]
    for level, indices in sorted(waves.items()):
        batches = []
        for index in sorted(indices, key=lambda i: (-entries[calls[i]["leaf"]]["resources"]["t_depth"], i)):
            call = calls[index]
            scratch = entries[call["leaf"]]["resources"]["qubits"] - sum(widths[v] for v in call["out"])
            assert scratch <= capacity
            batch = next((b for b in batches if b["scratch"] + scratch <= capacity), None)
            if batch is None:
                batch = dict(indices=[], scratch=0)
                batches.append(batch)
            batch["indices"].append(index)
            batch["scratch"] += scratch
        for batch in batches:
            selected = [calls[i] for i in batch["indices"]]
            resources = [entries[call["leaf"]]["resources"] for call in selected]
            copies = max(Counter(v for call in selected for v in call["args"]).values(), default=0)
            groups.append(dict(wave=level, call_indices=batch["indices"], private_scratch_qubits=batch["scratch"], copy_rounds=copies, t_depth=max(r["t_depth"] for r in resources), clifford_t_depth=max(r["clifford_t_depth"] for r in resources) + 2 * copies))
    assert groups == schedule["groups"]


def changes(auditor, source_root, case, variant):
    directory = source_root / case / variant
    before, after = (load(path / "source.json") for path in (BASELINE / case, directory))
    target = load(directory / "target.json")
    assert sha(directory / "target.json") == sha(BASELINE / case / "target.json")
    for field in ("format", "word_width", "fraction_bits", "values", "inputs", "outputs", "clean_schedule", "invocation_semantics", "inverse_semantics", "exact_clifford_t", "arbitrary_rotations"):
        assert before[field] == after[field]
    left, right = auditor.leafs(before), auditor.leafs(after)
    old_archive, new_archive = library_path(before), library_path(after)
    noninputs = [i for i, node in enumerate(target["nodes"]) if node["op"] != "input"]
    changed, unchanged, structures, proofs = [], set(), {}, []
    for call_index, (old, new) in enumerate(zip(before["forward_calls"], after["forward_calls"], strict=True)):
        assert {k: v for k, v in old.items() if k != "leaf"} == {k: v for k, v in new.items() if k != "leaf"}
        old_entry, new_entry = left[old["leaf"]], right[new["leaf"]]
        node_index = noninputs[call_index]
        intended = target["nodes"][node_index]["op"] == "sqrt"
        assert (old["leaf"] != new["leaf"]) == intended
        if not intended:
            key = old["leaf"]
            if key not in unchanged:
                assert sha(old_archive / (key + ".json")) == sha(new_archive / (key + ".json"))
                assert sha(old_archive / old_entry["gate_file"]) == sha(new_archive / new_entry["gate_file"])
                unchanged.add(key)
            continue
        assert new_entry["spec"]["algorithm"] + "__" + new_entry["spec"]["embedding"] == variant
        proof = auditor.unsigned_proof(target, node_index, new_entry["input_contract"])
        proofs.append(proof)
        if new["leaf"] not in structures:
            structures[new["leaf"]] = structure(new_entry, new_archive / new_entry["gate_file"])
        changed.append(dict(call_index=call_index, args=new["args"], out=new["out"], old_key=old["leaf"], new_key=new["leaf"], op="sqrt", params={}, old_resources=old_entry["resources"], new_resources=new_entry["resources"], input_contract=new_entry["input_contract"]))
    assert len(proofs) == (30 if case == "B4x12" else 234)
    assert load(directory / "changed_calls.json") == dict(changes=changed, unchanged_leaf_keys=sorted(unchanged))
    decisions = load(directory / "site_decisions.json")
    assert len(decisions) == len(after["forward_calls"])
    assert {d["forward_call_index"] for d in decisions} == set(range(len(after["forward_calls"])))
    for row in decisions:
        index = row["forward_call_index"]
        assert row["node_index"] == noninputs[index]
        assert row["old_key"] == before["forward_calls"][index]["leaf"]
        assert row["new_key"] == after["forward_calls"][index]["leaf"]
        if row["old_key"] != row["new_key"]:
            assert "sqrt" in row["type"]
        else:
            assert row["type"] == "fallback"
    schedule, old_schedule = (load(path / "schedule_capped.json") for path in (directory, BASELINE / case))
    assert schedule["format"] == "compact-clean-xor-capped-wave-schedule-v2"
    for field in ("widths", "offsets", "retained_ssa_qubits", "proof_masks", "proof_reasons", "argument_and_output_copy_cx", "baseline_argument_and_output_copy_cx"):
        assert schedule[field] == old_schedule[field], ("Unreviewed storage/copy change", case, variant, field)
    independently_pack(after, right, schedule)
    return dict(changed_calls=len(changed), unchanged_leaf_keys=len(unchanged), structural_leaf_proofs=structures, unsigned46_same_ssa_proofs=proofs, storage_and_copy_allocation_unchanged=True, exact_first_fit_groups_recomputed=True)


def run(source_root, output):
    source_root, output = source_root.resolve(), output.resolve()
    frozen, producer_protocol = freeze(source_root)
    output.mkdir(parents=True, exist_ok=False)
    report = ROOT / "docs/limitation_program_20261001/SQRT_SOURCE_COSTS.md"
    assert not report.exists()
    started = time.perf_counter()
    dump(output / "protocol.json", dict(
        created_utc=datetime.now(timezone.utc).isoformat(), before_analysis=True,
        local_only=True, source_root=relative(source_root), baseline=relative(BASELINE),
        frozen_inputs=frozen, producer_sha256=sha(Path(__file__)),
        scope="Independent read-only exact-array, structure, range and resource audit; no new pricing or gate replay",
        family=list(VARIANTS),
        checks="All gate array counts/depths and full72 interfaces; unsigned recurrence/remainder width; fused and repeated-child clean XOR structure; actual same-SSA guards with all literal lookup rows; target/fallback bytes; unchanged compact masks/storage/copies; full counts/DAG/groups/first-fit caps/categories; shared predeclared both-case selection; saved finite pytest/full-source replay receipts",
        selection="At least2% complete capped T-depth reduction separately in both cases, no Clifford+T depth increase, current actual caps; minimum summed T-depth, then T work, then logical qubits",
        stop_rule="Exactly four preregistered variants in two cases; abort first mismatch, preserve historical bytes and report no quantum advantage",
        proof_scope="Input ranges and recurrence bounds are structural integer guarantees. Actual emitted functional correctness is supported by frozen finite leaf tests/replays and unchanged comparison/subtraction semantics. No exhaustive72 enumeration, continuous-price or physical-speedup certification.",
    ))
    dump(output / "environment.json", environment())
    certificate = recurrence_certificate()
    dump(output / "sqrt_arithmetic_certificate.json", certificate)
    auditor = Auditor(frozen)
    summary = load(source_root / "summary.json")
    trials = {}
    for case in CASES:
        comparison = next(row for row in summary["cases"] if row["case"] == case)
        if (source_root / case / "comparison.json").exists():
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
            assert row["resources"] == ledger["resources"]
            assert ledger["qubit_cap"] == CAPS[case]
            eligible = (100 * ledger["resources"]["t_depth"] <= 98 * baseline["t_depth"] and ledger["resources"]["clifford_t_depth"] <= baseline["clifford_t_depth"] and ledger["resources"]["logical_qubits"] <= CAPS[case])
            delta_t = ledger["resources"]["t_count"] - baseline["t_count"]
            assert row["eligible"] == eligible
            assert row["changed_calls"] == attribution["changed_calls"]
            assert row["batches"] == ledger["batch_count"] and row["t_count_change"] == delta_t
            assert abs(row["full_t_depth_gain_percent"] - 100 * (1 - ledger["resources"]["t_depth"] / baseline["t_depth"])) < 1e-9
            ledger.update(variant=variant, eligible=eligible, changes=attribution, t_count_change=delta_t, baseline_resources=baseline, t_depth_change=ledger["resources"]["t_depth"] - baseline["t_depth"], clifford_t_depth_change=ledger["resources"]["clifford_t_depth"] - baseline["clifford_t_depth"])
            trials[case, variant] = ledger
            dump(output / (case + "_" + variant + "_ledger.json"), ledger)
    eligible_variants = [v for v in VARIANTS if all(trials[case, v]["eligible"] for case in CASES)]
    selected = min(eligible_variants, key=lambda v: tuple(sum(trials[case, v]["resources"][field] for case in CASES) for field in ("t_depth", "t_count", "logical_qubits"))) if eligible_variants else None
    assert summary["selected"] == selected and summary["accepted"] == (selected is not None)
    baseline_summary = load(BASELINE / "summary.json")
    final_cases = []
    for case in CASES:
        comparison = next(row for row in summary["cases"] if row["case"] == case)
        if selected is not None:
            chosen = next(row for row in comparison["trials"] if row["variant"] == selected)
            assert comparison["selected"] == chosen and comparison["candidate"] == chosen["resources"]
            assert comparison["accepted"] and comparison["replay_passed"]
            replays = comparison["replays"]
            prior = next(row for row in baseline_summary["cases"] if row["case"] == case)["replays"]
            assert len(replays) == len(prior)
            if (source_root / case / "replays.json").exists():
                assert replays == load(source_root / case / "replays.json")
            for replay, old in zip(replays, prior, strict=True):
                for key in ("label", "inputs", "initial", "expected"):
                    assert replay[key] == old[key]
                assert replay["passed"] and replay["actual"]["values"] == replay["expected"]
                assert replay["actual"]["all_input_and_workspace_bits_restored"]
                assert any(replay["initial"].values())
                assert all(0 <= value < (1 << 72) for value in replay["initial"].values())
            for filename in ("source.json", "target.json", "schedule_capped.json"):
                assert sha(source_root / case / filename) == sha(source_root / case / selected / filename)
            final, effective_source = trials[case, selected], source_root / case
        else:
            assert not comparison.get("accepted", False) and not comparison.get("replay_passed", False)
            final, effective_source = auditor.costs(case, BASELINE / case), BASELINE / case
        final = dict(final, effective_source=relative(effective_source), selected_variant=selected, prior_full_source_replays=len(comparison.get("replays", [])))
        final_cases.append(final)
        dump(output / (case + "_accepted_ledger.json"), final)
        print(case, "PASS", selected or "baseline-retained", final["resources"]["t_depth"], flush=True)
    xml_receipts = []
    for path in source_root.rglob("*.xml"):
        document = ET.parse(path).getroot()
        suites = [document] if document.tag == "testsuite" else document.findall("testsuite")
        assert suites and all(int(s.get("failures", "0")) == 0 and int(s.get("errors", "0")) == 0 for s in suites)
        xml_receipts.append(dict(path=relative(path), tests=sum(int(s.get("tests", "0")) for s in suites)))
    verification = load(source_root / "verification.json")
    assert verification["passed"] and verification["pytest_exit_code"] == 0
    next_action = "Use the newly recomputed complete-source owner ranking for the next bounded local screen. An exact same-SSA squaring replacement for remaining variable products is a candidate; cmul/shift alternatives need their own leaf proof and full-source cap/replay check. Carry exact T work and width into G5 before asserting physical runtime improvement."
    result = dict(passed=True, decision="independent_unsigned_sqrt_source_audit", accepted=selected is not None, selected=selected, source_root=relative(source_root), baseline=relative(BASELINE), cases=final_cases, actual_unique_gate_arrays_scanned=len(auditor.array_scans), metadata_locations_checked=len(auditor.leaf_cache), frozen_input_count=len(frozen), exact_arithmetic_certificate=True, pytest_xml_receipts=xml_receipts, new_gate_replays=0, G2_G5="unresolved", next_action=next_action, seconds=time.perf_counter() - started)
    dump(output / "summary.json", result)
    dump(output / "verification.json", dict(passed=True, producer_sha256=sha(Path(__file__)), command=[str(Path(sys.executable).resolve()), "-m", "research.limitation_program_20261001.reconcile_sqrt", "--source-root", relative(source_root), "--output", relative(output)], checks=["Frozen inputs/code/producer manifests", "Actual array gate counts and ASAP depths", "Unsigned recurrence and counted clean remainder structure", "Same-SSA unsigned46 interval promise for every changed call", "Full72 native interfaces, fallback/target bytes and unchanged storage/copies", "Full counts/DAG/first-fit batches/width caps/categories", "Both-case shared selection and finite saved test/replay receipts"], new_replays=0))
    with (output / "NEXT.md").open("x", encoding="utf-8") as handle:
        handle.write("# Next local action\n\n" + next_action + "\n")
    lines = ["# Independent unsigned square-root source audit\n\n", "The local A11 screen was independently checked against actual emitted arrays, the accepted A09 baseline and the unchanged target. All four preregistered variants were reconciled in both cases; this audit adds no financial or gate replay.\n\n", "| Case | Selected variant | T gates | T change | Compact T-depth | Clifford+T depth | Logical qubits / cap |\n|---|---|---:|---:|---:|---:|---:|\n"]
    for row in final_cases:
        resources = row["resources"]
        old = load(BASELINE / row["case"] / "schedule_capped.json")["resources"]
        lines.append(f"| {row['case']} | {selected or 'baseline retained'} | {resources['t_count']:,} | {resources['t_count']-old['t_count']:+,} | {resources['t_depth']:,} | {resources['clifford_t_depth']:,} | {resources['logical_qubits']:,} / {row['qubit_cap']:,} |\n")
    lines.append(f"\nThe predeclared complete-source rule requires at least 2% T-depth reduction in each case, no Clifford+T depth increase and the current accepted logical qubit caps. A common variant is selected by summed T-depth, T work and qubits. Actual scans covered {len(auditor.array_scans)} unique gate arrays and {len(auditor.leaf_cache)} metadata locations.\n\n")
    lines.append("All 30 B4x12 and 234 B8x52 square-root calls have their actual same-SSA input range recomputed against all literal lookup rows and declared input widths: nonnegative unsigned raw inputs below 2^46. Bit45 remains active and may be one; no signed46 reinterpretation is accepted. The external input/output registers remain72 bits, and existing SSA masks, storage, argument copies and output copies are identical to A09. Every fallback metadata and gate file and the target file match their baseline bytes.\n\n")
    lines.append("For N=x*2^40, the integer restoring recurrence maintains prefix=q^2+r and 0<=r<2q+1. Processing the next base-four digit d gives candidate 4r+d, trial 4q+1 and q'=2q+t. Conditional subtraction yields the same invariant and uniquely selects floor(sqrt(N)). With86 radicand bits there are43 stages; all intermediate candidates fit45 unsigned remainder bits. Every remainder is allocated, counted and restored. Structural checks independently verify the fused compute/copy/reverse case and the repeated self-inverse child case, arbitrary-output XOR, unchanged high output bits and restored private workspace. Saved finite emitted tests and full-source replays support circuit realization; this is not exhaustive72 input enumeration.\n\n")
    for row in final_cases:
        lines.append(f"## Final {row['case']} ledger\n\nIndependent forward DAG T-depth: {row['independent_forward_dependency_t_depth']:,}; compact argument/output copy CX: {row['compact_total_copy_cx']:,}. Retained SSA qubits: {row['retained_ssa_qubits']:,}; full external output: {row['named_output_qubits']}; peak private scratch: {row['peak_private_scratch_qubits']:,}. Exact same-SSA self-products: {row['same_ssa_self_products']['count']:,}.\n\n| Category | T gates | Overlapping capped T-depth diagnostic |\n|---|---:|---:|\n")
        for name, category in row["category_costs"].items():
            lines.append(f"| {name} | {category.get('t_count',0):,} | {category.get('overlapping_capped_t_depth_diagnostic',0):,} |\n")
        lines.append("\nTop three deterministic depth-owner leaves:\n\n")
        for leaf in row["top_three_depth_owner_leaves"]:
            lines.append(f"- `{leaf['leaf']}`: {leaf['op']}, {leaf['params']}, {leaf['exclusive_batch_t_depth']:,} attributed layers; hypothetical fixed-batch zero-cost saving {leaf['optimistic_fixed_batch_zero_cost_saving']:,}.\n")
    lines.append("\nCategory depth diagnostics overlap and cannot be summed. Owner/zero-cost diagnostics identify candidate work; they do not claim attainable independent gains. Canonical serial and actual compact executed resources were separately reconciled.\n\n" + next_action + "\n\nG2 continuous-dollar certification, G3 compatible99% estimator scheduling, G4 matched classical timing and G5 physical10x runtime accounting remain unresolved. This circuit improvement does not establish quantum advantage. Everything remained local.\n\n")
    lines.append(f"Receipts: [summary](../../{relative(output)}/summary.json), [complete audit](../../{relative(output)}/), [auditor](../../research/limitation_program_20261001/reconcile_sqrt.py).\n")
    with report.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write("".join(lines))
    assert all(sha(ROOT / name) == digest for name, digest in frozen.items())
    files = {relative(path): sha(path) for path in output.rglob("*") if path.is_file()}
    files[relative(report)] = sha(report)
    dump(output / "manifest.json", dict(files=files, frozen_inputs=frozen, manifest_self_hash_excluded=True))
    print("PASS independent unsigned sqrt source audit", len(auditor.array_scans), "actual arrays", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.source_root, args.output)
