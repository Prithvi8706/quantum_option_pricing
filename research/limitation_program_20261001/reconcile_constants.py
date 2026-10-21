"""Read-only independent ledger for completed exact constant source screens.

No pricing or gate replay is run. The four recorded strategies are audited,
including rejected candidates, against actual leaf arrays and compact bindings.
"""

from __future__ import annotations

# Full human-readable receipt strings intentionally remain unwrapped.
# ruff: noqa: E501

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import time

import numpy as np

from research.controlled_source_completion.primitives import gate_resources
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


ORIGINAL = ROOT / "results/limitation_program_20261001/A01_run003"
COEFFICIENT = {"log": 762123384786, "inverse": 1586259972792}
STRATEGIES = (
    "binary-shift-add",
    "signed-digit-shift-add",
    "binary-carry-save",
    "signed-digit-carry-save",
)


def relative(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def library_path(source):
    return ROOT / source["library_workspace_relative"].replace("\\", "/")


def graph_log_proof(target, index, context=None):
    """Independently recognize the exact guarded exponent chain, no range samples."""
    if (target["width"], target["fraction_bits"]) != (72, 40):
        return None
    nodes = target["nodes"]

    def form(node, op, arity, params):
        return (
            node["op"] == op
            and len(node["args"]) == arity
            and len(node["out"]) == 1
            and node["params"] == params
        )

    product = nodes[index]
    if not form(product, "cmul", 1, {"c": COEFFICIENT["log"]}):
        return None
    if context is None:
        context = (
            {v: n for n in nodes for v in n["out"]},
            {v: i for i, n in enumerate(nodes) for v in n["out"]},
        )
    producers, locations = context
    shifted = producers[product["args"][0]]
    if not form(shifted, "bits", 1, {"shift": -40, "width": 72, "signed": False}):
        return None
    exponent = producers[shifted["args"][0]]
    if not form(exponent, "sub", 2, {}):
        return None
    top, fraction = [producers[a] for a in exponent["args"]]
    if not form(top, "msb", 1, {}) or not form(fraction, "const", 0, {"value": 40}):
        return None
    guarded = producers[top["args"][0]]
    if not form(guarded, "select", 3, {}):
        return None
    comparison, unit, raw = [producers[a] for a in guarded["args"]]
    if not form(comparison, "lt", 2, {}) or not form(unit, "const", 0, {"value": 1}):
        return None
    if comparison["args"] != [guarded["args"][2], guarded["args"][1]]:
        return None
    chain = [product, shifted, exponent, top, fraction, guarded, comparison, unit, raw]
    # Whatever the raw input, a 72-bit MSB is in 0..71. Subtracting40 gives
    # -40..31, hence signed7. Left shift40 yields zero bits0..39 and sign
    # extension from bit46 through bit71. These are all possible MSB outcomes.
    for msb in range(72):
        k = msb - 40
        raw_value = (k << 40) & ((1 << 72) - 1)
        upper = (raw_value >> 40) & 127
        interpreted = upper - 128 if upper & 64 else upper
        assert interpreted == k
        assert raw_value & ((1 << 40) - 1) == 0
        assert raw_value >> 47 == (((1 << 25) - 1) if k < 0 else 0)
    return {
        "node_index": index,
        "chain_indices": [locations[n["out"][0]] for n in chain],
        "conservative_range": [-40, 31],
        "structural_all_input_proof": True,
        "msb_outcomes_checked": 72,
    }


class Auditor:
    def __init__(self, frozen):
        self.frozen = frozen
        self.leaf_cache = {}
        self.array_scans = {}

    def record(self, path):
        key, digest = relative(path), sha(path)
        assert self.frozen[key] == digest, ("Input changed during audit", key)
        return digest

    def leafs(self, source):
        library = library_path(source)
        result = {}
        for key in source["library_keys"]:
            meta = library / (key + ".json")
            digest = self.record(meta)
            cache_key = (relative(meta), digest)
            if cache_key not in self.leaf_cache:
                entry = load(meta)
                path = library / entry["gate_file"]
                gate_hash = self.record(path)
                assert gate_hash == entry["sha256"]
                scan_key = (gate_hash, entry["resources"]["qubits"])
                if scan_key not in self.array_scans:
                    gates = np.load(path, mmap_mode="r")
                    assert gates.ndim == 2 and gates.shape[1] == 4
                    counts = Counter(map(int, gates[:, 0]))
                    assert set(counts) <= {1, 2, 3}
                    # Inspect every participating wire rather than sentinel columns.
                    for op in (1, 2, 3):
                        rows = gates[gates[:, 0] == op, 1 : 1 + op]
                        assert not rows.size or (
                            rows.min() >= 0 and rows.max() < entry["resources"]["qubits"]
                        )
                        if op > 1:
                            assert not np.any(rows[:, 0] == rows[:, 1])
                            if op == 3:
                                assert not np.any(rows[:, 0] == rows[:, 2]) and not np.any(
                                    rows[:, 1] == rows[:, 2]
                                )
                    observed, td, ctd = gate_resources(gates, entry["resources"]["qubits"])
                    assert list(map(int, observed)) == [counts[1], counts[2], counts[3]]
                    raw = dict(
                        source_gates=len(gates),
                        x=counts[1],
                        cx=counts[2],
                        ccx=counts[3],
                        t_count=7 * counts[3],
                        clifford_cx=counts[2] + 6 * counts[3],
                        clifford_h=2 * counts[3],
                        t_depth=int(td),
                        clifford_t_depth=int(ctd),
                    )
                    self.array_scans[scan_key] = raw
                assert all(
                    entry["resources"][field] == value
                    for field, value in self.array_scans[scan_key].items()
                ), key
                registers = entry["args"] + entry["outs"]
                wires = [wire for register in registers for wire in register]
                assert len(wires) == len(set(wires))
                assert all(type(q) is int and 0 <= q < entry["resources"]["qubits"] for q in wires)
                self.leaf_cache[cache_key] = entry
            result[key] = self.leaf_cache[cache_key]
        assert set(result) == {call["leaf"] for call in source["forward_calls"]}
        return result

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
        labels, op_names, proofs = [], [], []
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
            assert set(contract) <= {"zero_low_bits", "signed_upper_bits"}
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

    def changed(self, target, before, after, directory, mode, strategy):
        left, right = self.leafs(before), self.leafs(after)
        base_library, new_library = library_path(before), library_path(after)
        nodes = [i for i, n in enumerate(target["nodes"]) if n["op"] != "input"]
        context = (
            {v: n for n in target["nodes"] for v in n["out"]},
            {v: i for i, n in enumerate(target["nodes"]) for v in n["out"]},
        )
        changes, unchanged = [], set()
        for index, (a, b) in enumerate(
            zip(before["forward_calls"], after["forward_calls"], strict=True)
        ):
            assert a["args"] == b["args"] and a["out"] == b["out"]
            old, new = left[a["leaf"]], right[b["leaf"]]
            assert old["op"] == new["op"] and old["params"] == new["params"]
            proof = graph_log_proof(target, nodes[index], context)
            intended = (
                proof is not None
                if mode == "log"
                else old["op"] == "cmul" and old["params"].get("c") == COEFFICIENT[mode]
            )
            assert (a["leaf"] != b["leaf"]) == intended
            if not intended:
                key = a["leaf"]
                if key not in unchanged:
                    assert sha(base_library / (key + ".json")) == sha(new_library / (key + ".json"))
                    assert sha(base_library / old["gate_file"]) == sha(new_library / new["gate_file"])
                unchanged.add(key)
                continue
            contract = (
                {"zero_low_bits": 40, "signed_upper_bits": 7}
                if mode == "log"
                else {"zero_low_bits": 0}
            )
            assert new["input_contract"] == contract and new["spec"]["strategy"] == strategy
            changes.append(
                dict(
                    call_index=index,
                    args=a["args"],
                    out=a["out"],
                    old_key=a["leaf"],
                    new_key=b["leaf"],
                    op=old["op"],
                    params=old["params"],
                    old_resources=old["resources"],
                    new_resources=new["resources"],
                    input_contract=contract,
                )
            )
        observed = load(directory / "changed_calls.json")
        assert observed == dict(changes=changes, unchanged_leaf_keys=sorted(unchanged))
        self.record(directory / "changed_calls.json")
        decisions = load(directory / "site_decisions.json")
        self.record(directory / "site_decisions.json")
        assert len(decisions) == len(after["forward_calls"])
        changed_indices = {c["call_index"] for c in changes}
        for decision in decisions:
            index = decision["forward_call_index"]
            assert decision["node_index"] == nodes[index]
            assert (
                decision["old_key"] == before["forward_calls"][index]["leaf"]
                and decision["new_key"] == after["forward_calls"][index]["leaf"]
            )
            kind = (
                ("log-signed7" if mode == "log" else "general-constant")
                if index in changed_indices
                else "fallback"
            )
            assert decision["type"] == kind
            if kind == "log-signed7":
                assert decision["proof"]["cmul_node_index"] == nodes[index]
                assert decision["proof"]["conservative_exponent_range"] == [-40, 31]
            elif kind == "general-constant":
                assert decision["proof"]["no_narrowed_input_promise"] is True
        assert {d["forward_call_index"] for d in decisions} == set(
            range(len(after["forward_calls"]))
        )
        return dict(
            changed_calls=len(changes),
            unchanged_leaf_keys=len(unchanged),
            exponential_same_coefficient_fallbacks=sum(
                old["op"] == "cmul"
                and old["params"].get("c") == COEFFICIENT["log"]
                and graph_log_proof(target, nodes[i], context) is None
                for i, call in enumerate(before["forward_calls"])
                for old in [left[call["leaf"]]]
            ),
        )


def collect_inputs(source_roots):
    """Freeze every complete screen and its baseline before deriving costs."""
    frozen = {}

    def add(path):
        frozen[relative(path)] = sha(path)

    def source_files(directory):
        for filename in (
            "target.json",
            "source.json",
            "schedule_capped.json",
            "changed_calls.json",
            "site_decisions.json",
        ):
            path = directory / filename
            if path.exists():
                add(path)
        source = load(directory / "source.json")
        library = library_path(source)
        for key in source["library_keys"]:
            meta = library / (key + ".json")
            add(meta)
            add(library / load(meta)["gate_file"])

    add(ORIGINAL / "manifest.json")
    for source_root in source_roots:
        summary = load(source_root / "summary.json")
        assert summary["passed"] and len(summary["cases"]) == 2
        protocol = load(source_root / "protocol.json")
        assert protocol["mode"] in COEFFICIENT
        baseline = ROOT / protocol["source_root"].replace("\\", "/")
        for filename in ("summary.json", "protocol.json"):
            add(source_root / filename)
        add(baseline / "summary.json")
        for dependency in protocol["executed_dependencies"]:
            path = source_root / dependency["snapshot"]
            assert sha(path) == dependency["sha256"]
            add(path)
        for case in ("B4x12", "B8x52"):
            source_files(baseline / case)
            for filename in ("screen.json", "comparison.json"):
                add(source_root / case / filename)
            for strategy in STRATEGIES:
                source_files(source_root / case / strategy)
            if (source_root / case / "source.json").exists():
                source_files(source_root / case)
            add(ORIGINAL / (case + "_accounting.json"))
        for key, expected in protocol["baseline_hashes"].items():
            parts = key.split("/")
            if len(parts) == 3 and parts[1] == "leaves":
                path = library_path(load(baseline / parts[0] / "source.json")) / parts[2]
            else:
                path = baseline / key
            assert sha(path) == expected, ("Baseline producer receipt mismatch", key)
    for path in (
        Path(__file__),
        Path(
            __import__(
                "research.limitation_program_20261001.baseline", fromlist=["__file__"]
            ).__file__
        ),
        Path(
            __import__(
                "research.limitation_program_20261001.compact_ledger", fromlist=["__file__"]
            ).__file__
        ),
        Path(
            __import__(
                "research.controlled_source_completion.primitives", fromlist=["__file__"]
            ).__file__
        ),
    ):
        add(path)
    return frozen


def audit_root(auditor, root, output):
    protocol, producer_summary = load(root / "protocol.json"), load(root / "summary.json")
    mode = protocol["mode"]
    assert (
        protocol["coefficient"] == COEFFICIENT[mode] and tuple(protocol["candidates"]) == STRATEGIES
    )
    baseline = ROOT / protocol["source_root"].replace("\\", "/")
    assert load(baseline / "summary.json")["accepted"]
    cases = []
    for case in ("B4x12", "B8x52"):
        before = load(baseline / case / "source.json")
        target = load(baseline / case / "target.json")
        old = load(baseline / case / "schedule_capped.json")["resources"]
        cap = old["logical_qubits"]
        comparison = load(root / case / "comparison.json")
        screens = load(root / case / "screen.json")
        assert comparison["trials"] == screens and comparison["baseline"] == old
        assert comparison["target_sha256"] == sha(baseline / case / "target.json")
        assert [row["strategy"] for row in screens] == list(STRATEGIES)
        trials = []
        for row in screens:
            directory = root / case / row["strategy"]
            assert sha(directory / "target.json") == sha(baseline / case / "target.json")
            after = load(directory / "source.json")
            attribution = auditor.changed(target, before, after, directory, mode, row["strategy"])
            result = auditor.costs(case, directory)
            result.update(strategy=row["strategy"], changes=attribution)
            if result["schedule_available"]:
                assert row["resources"] == result["resources"]
                assert cap == result["qubit_cap"] and row["batches"] == result["batch_count"]
                eligible = (
                    result["resources"]["logical_qubits"] <= cap
                    and all(
                        result["resources"][f] <= old[f]
                        for f in ("t_depth", "t_count", "clifford_t_depth")
                    )
                    and any(
                        result["resources"][f] < old[f]
                        for f in ("t_depth", "t_count", "clifford_t_depth")
                    )
                )
                assert (
                    row["eligible"] == eligible
                    and row["changed_calls"] == attribution["changed_calls"]
                )
            else:
                assert not row["eligible"] and "reason" in row
                assert result["minimum_retained_and_one_leaf_qubits"] > cap, (
                    "Unsupported schedule rejection must be examined"
                )
            trials.append(result)
            dump(output / (mode + "_" + case + "_" + row["strategy"] + "_ledger.json"), result)
        eligible = [row for row in screens if row["eligible"]]
        if eligible:
            selected = min(
                eligible,
                key=lambda row: tuple(
                    row["resources"][f]
                    for f in ("t_depth", "t_count", "clifford_t_depth", "logical_qubits")
                ),
            )
            assert (
                comparison["selected"] == selected
                and comparison["candidate"] == selected["resources"]
            )
            assert comparison["accepted"] and comparison["replay_passed"] and comparison["replays"]
            for replay in comparison["replays"]:
                assert (
                    replay["passed"] and replay["actual"]["all_input_and_workspace_bits_restored"]
                )
                # Runner stores its XOR-adjusted expected output, not raw Y.
                assert replay["actual"]["values"] == replay["expected"]
            for filename in ("target.json", "source.json", "schedule_capped.json"):
                assert sha(root / case / filename) == sha(
                    root / case / selected["strategy"] / filename
                )
            final = next(trial for trial in trials if trial["strategy"] == selected["strategy"])
            final_directory = root / case
            selected_strategy = selected["strategy"]
        else:
            assert not comparison["accepted"] and not comparison["replay_passed"]
            assert not (root / case / "source.json").exists()
            final = auditor.costs(case, baseline / case)
            final_directory, selected_strategy = baseline / case, "baseline-retained"
        final = dict(
            final,
            selected_strategy=selected_strategy,
            effective_source=relative(final_directory),
            prior_full_source_replay_records=len(comparison["replays"]),
            baseline_resources=old,
        )
        cases.append(final)
        dump(output / (mode + "_" + case + "_accepted_ledger.json"), final)
        print(mode, case, "PASS", selected_strategy, final["resources"]["t_depth"], flush=True)
    assert producer_summary["cases"] == [
        load(root / case / "comparison.json") for case in ("B4x12", "B8x52")
    ]
    assert producer_summary["accepted"] == all(
        load(root / case / "comparison.json")["accepted"] for case in ("B4x12", "B8x52")
    )
    return dict(
        mode=mode,
        root=relative(root),
        baseline=relative(baseline),
        passed=True,
        accepted=producer_summary["accepted"],
        cases=cases,
    )


def run(source_roots, output):
    start = time.perf_counter()
    source_roots = [path.resolve() for path in source_roots]
    frozen = collect_inputs(source_roots)
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    report = ROOT / "docs/limitation_program_20261001/CONSTANT_SOURCE_COSTS.md"
    assert not report.exists()
    dump(
        output / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            before_analysis=True,
            source_roots=[relative(path) for path in source_roots],
            frozen_inputs=frozen,
            producer_sha256=sha(Path(__file__)),
            local_only=True,
            checks="Actual gate arrays and exact resources; independent guarded signed7 chain; unchanged fallback bytes; all source totals, compact widths/copies/registers, Kahn DAG/batches/peak qubits; every four-way eligibility and selection.",
            stop_rule="One audit of the completed recorded roots; abort on first mismatch; no new source/gate/pricing replay or source modification.",
            proof_scope="Structural signed7 provenance plus all72 MSB outcomes proves its operand promise for this canonical graph. Existing finite gate replays remain finite validation, not exhaustive signed72 circuit equivalence or continuous-dollar certification.",
            category_scope="Frozen A01_run003 call labels reused with each call counted once; category depths overlap and are not serially summed; zero-cost fixed-batch diagnostics do not count as measured gain.",
            unresolved="G2-G5 remain unresolved; this is arithmetic resource accounting.",
        ),
    )
    dump(output / "environment.json", environment())
    auditor = Auditor(frozen)
    results = [audit_root(auditor, root, output) for root in source_roots]
    final = results[-1]["cases"]
    next_action = "Use the actual same-SSA self-product ledger to test an exact signed72 fixed-point squaring leaf with floor-after40-bit semantics, arbitrary-output XOR and cleanup. Compare it with the unchanged variable multiplication leaf first; if valid and worthwhile, replace only proved self-products and measure the complete compact source at the current accepted caps. General variable multiplication and sqrt remain separate alternatives; their hypothetical zero-cost screens do not count as measured gains."
    summary = dict(
        passed=True,
        decision="independent_completed_constant_source_audit",
        roots=results,
        actual_unique_gate_arrays_scanned=len(auditor.array_scans),
        metadata_locations_checked=len(auditor.leaf_cache),
        frozen_input_count=len(frozen),
        final_cases=[
            {
                key: row[key]
                for key in (
                    "case",
                    "effective_source",
                    "selected_strategy",
                    "resources",
                    "top_three_depth_owner_leaves",
                    "operation_ranking",
                    "same_ssa_self_products",
                )
            }
            for row in final
        ],
        new_gate_replays=0,
        G2_G5="unresolved",
        next_action=next_action,
        seconds=time.perf_counter() - start,
    )
    dump(output / "summary.json", summary)
    dump(
        output / "verification.json",
        dict(
            passed=True,
            command=[
                str(Path(sys.executable).resolve()),
                "-m",
                "research.limitation_program_20261001.reconcile_constants",
                "--source-roots",
                *[relative(p) for p in source_roots],
                "--output",
                relative(output),
            ],
            producer_sha256=sha(Path(__file__)),
            checks=[
                "All recorded four-way screens and exact selected ordering",
                "All used actual leaf arrays, wires, gate/depth resources and immutable fallback bytes",
                "Every signed7 binding independently proved from same canonical target",
                "Generic inverse remains full signed72 with zero-low promise0",
                "Canonical manifest and actual compact scope reconciled separately",
                "All counts, copy CX, categories, dependency waves, batch depths and cap/peak allocation",
            ],
            new_replays=0,
        ),
    )
    with (output / "NEXT.md").open("x", encoding="utf-8") as handle:
        handle.write(
            "# Next local action\n\n"
            + next_action
            + "\n\nCurrent depth attribution is below; hypothetical zero-cost savings are only prioritization diagnostics. Source improvement does not resolve G2-G5.\n\n"
        )
        for row in final:
            handle.write(
                row["case"]
                + ": "
                + ", ".join(
                    item["op"] + " " + item["leaf"] for item in row["top_three_depth_owner_leaves"]
                )
                + ".\n"
            )
    lines = [
        "# Independent constant-source cost reconciliation\n\n",
        "The completed local logarithm and inverse-ln2 screens were independently audited against every actual leaf array, the frozen original call categories, same target bytes, unchanged fallback metadata/gates and compact schedules. This audit runs no new gate or pricing replay. The source manifest's full-width serial accounting and the actual compact schedule remain separate scopes.\n\n",
        "| Screen | Case | Selected strategy | T gates | Compact T-depth | Clifford+T depth | Actual logical qubits / cap |\n|---|---|---|---:|---:|---:|---:|\n",
    ]
    for root_result in results:
        for row in root_result["cases"]:
            r = row["resources"]
            lines.append(
                f"| {root_result['mode']} | {row['case']} | {row['selected_strategy']} | {r['t_count']:,} | {r['t_depth']:,} | {r['clifford_t_depth']:,} | {r['logical_qubits']:,} / {row['qubit_cap']:,} |\n"
            )
    lines.append(
        f"\nAll four candidates per case were checked, including rejection reasons, complete-source Pareto eligibility and the predeclared ordering. Actual gate-resource scans covered {len(auditor.array_scans)} unique arrays and {len(auditor.leaf_cache)} metadata locations. Exact argument/output register mapping includes retained one-bit SSA values, full-width external outputs and omitted-output wires counted as private scratch. Count identities include seven T/six CX/two H per CCX. All forward call totals, compact copies, every batch and the independent weighted DAG reconcile.\n\n"
    )
    lines.append(
        "The signed7 promise is proved independently from the same guarded-log SSA chain: MSB is in0..71, its exponent after subtracting40 is in-40..31, and shift40 gives low40 zeros and the required sign extension. All72 MSB outcomes verify that interface. This proof applies to the operand promise; archived finite arbitrary-output gate replays and leaf tests remain finite correctness checks. The exponential calls sharing ln2 retain their original signed32 fallback. Generic inverse-ln2 replacements retain the complete signed72 domain and floor/shift semantics with no nonzero low-bit or narrow-range promise.\n\n"
    )
    for row in final:
        lines.append(
            f"## Final {row['case']} ledger\n\n| Category | Clean T gates | Argument-copy CX | Overlapping capped T-depth diagnostic |\n|---|---:|---:|---:|\n"
        )
        for name in CATEGORIES:
            c = row["category_costs"][name]
            lines.append(
                f"| {name} | {c.get('t_count', 0):,} | {c.get('clean_argument_copy_cx', 0):,} | {c.get('overlapping_capped_t_depth_diagnostic', 0):,} |\n"
            )
        lines.append(
            f"\nIndependent forward DAG T-depth: {row['independent_forward_dependency_t_depth']:,}. Compact argument/output copy CX: {row['compact_total_copy_cx']:,}. Retained SSA qubits: {row['retained_ssa_qubits']:,}; named output: {row['named_output_qubits']}; peak private scratch: {row['peak_private_scratch_qubits']:,}.\n\n"
        )
        lines.append(
            f"There are {row['same_ssa_self_products']['count']} actual same-SSA self-products. Their complete producer signatures, occurrence indices and current leaf resources are saved in the final ledger. Exact repeated operands establish a squaring opportunity, not an accepted squaring circuit or a capped-source saving.\n\n"
        )
        lines.append("Top three deterministic depth-owner leaves:\n\n")
        for leaf in row["top_three_depth_owner_leaves"]:
            lines.append(
                f"- `{leaf['leaf']}`: {leaf['op']}, {leaf['params']}, {leaf['exclusive_batch_t_depth']:,} attributed layers; optimistic frozen-batch zero-cost saving {leaf['optimistic_fixed_batch_zero_cost_saving']:,}.\n"
            )
    lines.append(
        "\nCategory depths overlap and cannot be serially summed. Batch ownership is deterministic attribution with tie effects; frozen-batch zero-cost savings are hypothetical, not measured improvements. The table records complete-source resources only, with no multiplication of independent leaf speedups.\n\n"
        + next_action
        + "\n\nArithmetic improvement leaves G2 continuous-dollar error certification, G3 an explicit compatible99% estimator schedule, G4 matched actual classical timing and G5 physical10× runtime inequality unresolved. All receipts and code stayed local; no historical evidence or progress ledger was edited.\n\n"
    )
    lines.append(
        f"Receipts: [summary](../../{relative(output)}/summary.json), [full audit](../../{relative(output)}/), [producer](../../research/limitation_program_20261001/reconcile_constants.py).\n"
    )
    with report.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write("".join(lines))
    assert all(sha(ROOT / path) == digest for path, digest in frozen.items())
    files = {relative(p): sha(p) for p in sorted(output.rglob("*")) if p.is_file()}
    files[relative(report)] = sha(report)
    dump(
        output / "manifest.json",
        dict(files=files, frozen_inputs=frozen, manifest_self_hash_excluded=True),
    )
    assert all(sha(ROOT / path) == digest for path, digest in files.items())
    print(
        "PASS independent constant-source accounting",
        len(auditor.array_scans),
        "actual arrays",
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-roots", nargs="+", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.source_roots, args.output)
