"""Independent cost reconciliation of the accepted compact capped sources."""

from __future__ import annotations

# Human-readable receipt/report strings deliberately retain their complete text.
# ruff: noqa: E501

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

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


ORIGINAL = ROOT / "results/limitation_program_20261001/A01_run003"
COMPACT = ROOT / "results/limitation_program_20261001/A06_run001"


def active_bit_certificate(target):
    """Reconstruct the possible-one bound without calling compact allocator code."""
    word = target["width"]
    full = (1 << word) - 1
    bounds = {}
    for node in target["nodes"]:
        operation, p = node["op"], node["params"]
        operands = [bounds[a] for a in node["args"]]
        if operation == "input":
            assert 0 <= p["bits"] <= word
            out = [(1 << p["bits"]) - 1]
        elif operation == "const":
            out = [p["value"] & full]
        elif operation == "lt":
            out = [1]
        elif operation == "msb":
            out = [(1 << (word - 1).bit_length()) - 1]
        elif operation == "positive":
            out = [operands[0] & (full >> 1)]
        elif operation == "select":
            out = [operands[1] | operands[2] if operands[0] & 1 else operands[2]]
        elif operation == "bits":
            shift = p["shift"]
            mask = operands[0] >> shift if shift >= 0 else operands[0] << -shift
            if shift > 0 and p["signed"] and operands[0] & (1 << (word - 1)):
                mask |= full ^ ((1 << max(0, word - shift)) - 1)
            out = [mask & full & ((1 << p["width"]) - 1)]
        elif operation == "lookup":
            out = [0] * len(node["out"])
            for row in target["tables"][p["table"]]:
                for i, value in enumerate(row):
                    out[i] |= value & full
        elif operation == "add" and sum(operands) <= full:
            out = [(1 << sum(operands).bit_length()) - 1]
        else:
            out = [full] * len(node["out"])
        assert len(out) == len(node["out"])
        for value, mask in zip(node["out"], out, strict=True):
            assert value not in bounds
            bounds[value] = mask
    return bounds


def frozen_leafs(source, frozen_hashes, tracked):
    library = ROOT / source["library_workspace_relative"].replace("\\", "/")
    result = {}
    for key in source["library_keys"]:
        meta_path = library / (key + ".json")
        entry = load(meta_path)
        gate_path = library / entry["gate_file"]
        for file in (meta_path, gate_path):
            relative = file.relative_to(ROOT).as_posix()
            digest = sha(file)
            assert digest == frozen_hashes[relative], ("Frozen leaf changed", relative)
            tracked[relative] = digest
        assert sha(gate_path) == entry["sha256"]
        result[key] = entry
    return result


def analyze(case, frozen_hashes, tracked):
    baseline = load(ORIGINAL / (case + "_accounting.json"))
    directory = COMPACT / case
    target, source, schedule = (
        load(directory / name) for name in ("target.json", "source.json", "schedule_capped.json")
    )
    old_directory = (
        ROOT
        / "results/limitation_audit_20261001/constant_multiplier_v1"
        / case
        / "signed-digit-carry-save"
    )
    assert sha(directory / "target.json") == sha(old_directory / "target.json")
    assert sha(directory / "source.json") == sha(old_directory / "source.json")
    def expected_fp(obj):
        return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()
    assert schedule["source_fingerprint"] == expected_fp(source)
    assert schedule["target_fingerprint"] == expected_fp(target)
    entries = frozen_leafs(source, frozen_hashes, tracked)
    masks = active_bit_certificate(target)
    values = source["values"]
    assert set(masks) == set(range(values))
    widths = [max(1, masks[value].bit_length()) for value in range(values)]
    assert widths == schedule["widths"]
    assert [masks[value] for value in range(values)] == schedule["proof_masks"]
    cursor, offsets = 0, []
    for width in widths:
        assert 1 <= width <= source["word_width"]
        offsets.append(cursor)
        cursor += width
    assert offsets == schedule["offsets"] and cursor == schedule["retained_ssa_qubits"]
    calls = source["forward_calls"]
    assert len(calls) == len(baseline["assignments"])
    labels, op_names = [], []
    category = {name: Counter() for name in CATEGORIES}
    work, owners = defaultdict(Counter), defaultdict(Counter)
    forward_totals = Counter()
    active_copies, baseline_copies = 0, 0
    word = source["word_width"]
    for index, (call, assignment) in enumerate(zip(calls, baseline["assignments"], strict=True)):
        assert assignment["call_index"] == index and assignment["leaf"] == call["leaf"]
        node = target["nodes"][assignment["node_index"]]
        assert node["args"] == call["args"] and node["out"] == call["out"]
        entry = entries[call["leaf"]]
        assert entry["op"] == node["op"] and entry["params"] == node["params"]
        label = assignment["category"]
        labels.append(label)
        op_names.append(node["op"])
        assert len(entry["args"]) == len(call["args"])
        assert len(entry["outs"]) == len(call["out"])
        registers = entry["args"] + entry["outs"]
        wires = [wire for register in registers for wire in register]
        assert len(wires) == len(set(wires))
        assert all(0 <= q < entry["resources"]["qubits"] for q in wires)
        for value, register in zip(call["args"] + call["out"], registers, strict=True):
            assert widths[value] <= len(register) <= word
        low = entry.get("input_contract", {}).get("zero_low_bits")
        if low is not None:
            assert len(call["args"]) == 1 and not masks[call["args"][0]] & ((1 << low) - 1)
        copies = 4 * sum(widths[v] for v in call["args"])
        original_copies = 4 * len(call["args"]) * word
        active_copies += copies
        baseline_copies += original_copies
        category[label]["clean_argument_copy_cx"] += copies
        category[label]["saved_argument_copy_cx"] += original_copies - copies
        category[label]["forward_calls"] += 1
        for field in COUNT_FIELDS:
            cost = entry["resources"][field]
            forward_totals[field] += cost
            category[label][field] += 2 * cost
        for field in ("source_gates", "cx", "clifford_cx"):
            category[label][field] += copies
        work[node["op"]]["clean_t_count"] += 2 * entry["resources"]["t_count"]
    output_copies = sum(widths[v] for v in source["outputs"].values())
    active_copies += output_copies
    baseline_copies += len(source["outputs"]) * word
    for field in ("source_gates", "cx", "clifford_cx"):
        category["path_payoff"][field] += output_copies
    category["path_payoff"]["output_copy_cx"] = output_copies
    category["path_payoff"]["saved_output_copy_cx"] = len(source["outputs"]) * word - output_copies
    assert active_copies == schedule["argument_and_output_copy_cx"]
    assert baseline_copies == schedule["baseline_argument_and_output_copy_cx"]
    totals = {
        field: 2 * forward_totals[field]
        + (active_copies if field in ("source_gates", "cx", "clifford_cx") else 0)
        for field in COUNT_FIELDS
    }
    for field in COUNT_FIELDS:
        assert totals[field] == schedule["resources"][field]
        assert sum(c[field] for c in category.values()) == totals[field]
        expected_delta = (
            active_copies - baseline_copies if field in ("source_gates", "cx", "clifford_cx") else 0
        )
        assert totals[field] == source["resources"][field] + expected_delta
    assert totals["t_count"] == 7 * totals["ccx"]
    assert totals["clifford_cx"] == totals["cx"] + 6 * totals["ccx"]
    assert totals["clifford_h"] == 2 * totals["ccx"]
    dag_depth, levels, critical = independent_dag(source, entries)
    assert (
        dag_depth
        == baseline["independent_forward_dependency_t_depth"]
        == schedule["dependency_only_forward_t_depth"]
    )
    for index in critical:
        category[labels[index]]["one_critical_path_t_depth_contribution"] += entries[
            calls[index]["leaf"]
        ]["resources"]["t_depth"]
    assert sum(c["one_critical_path_t_depth_contribution"] for c in category.values()) == dag_depth
    retained = cursor + len(source["outputs"]) * word
    all_indices, batch_rows = [], []
    tdepth = ctdepth = peak_scratch = copy_depth = 0
    for batch_index, batch in enumerate(schedule["groups"]):
        indices = batch["call_indices"]
        all_indices.extend(indices)
        assert all(levels[index] == batch["wave"] for index in indices)
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
        assert scratch == batch["private_scratch_qubits"] and copies == batch["copy_rounds"]
        assert td == batch["t_depth"] and ct == batch["clifford_t_depth"]
        assert retained + scratch <= schedule["qubit_cap"]
        tdepth += 2 * td
        ctdepth += 2 * ct
        copy_depth += 4 * copies
        peak_scratch = max(peak_scratch, scratch)
        owner = min(indices, key=lambda i: (-entries[calls[i]["leaf"]]["resources"]["t_depth"], i))
        owners[calls[owner]["leaf"]]["exclusive_batch_t_depth"] += 2 * td
        owners[calls[owner]["leaf"]]["owned_batches"] += 1
        work[op_names[owner]]["exclusive_batch_t_depth"] += 2 * td
        category[labels[owner]]["exclusive_batch_owner_t_depth_diagnostic"] += 2 * td
        for name in CATEGORIES:
            category[name]["overlapping_capped_t_depth_diagnostic"] += 2 * max(
                (
                    entries[calls[i]["leaf"]]["resources"]["t_depth"]
                    for i in indices
                    if labels[i] == name
                ),
                default=0,
            )
        batch_rows.append(
            {
                "batch": batch_index,
                "wave": batch["wave"],
                "calls": len(indices),
                "scratch_qubits": scratch,
                "dominant_call": owner,
                "dominant_leaf": calls[owner]["leaf"],
                "dominant_operation": op_names[owner],
                "t_depth": td,
            }
        )
    output_depth = max(Counter(source["outputs"].values()).values(), default=0)
    ctdepth += output_depth
    assert sorted(all_indices) == list(range(len(calls))) and len(all_indices) == len(
        set(all_indices)
    )
    assert tdepth == schedule["resources"]["t_depth"]
    assert ctdepth == schedule["resources"]["clifford_t_depth"]
    assert retained + peak_scratch == schedule["resources"]["logical_qubits"]
    assert peak_scratch == schedule["resources"]["max_reused_scratch_qubits"]
    assert sum(c["exclusive_batch_owner_t_depth_diagnostic"] for c in category.values()) == tdepth
    for name in CATEGORIES:
        assert category[name]["t_count"] == baseline["category_costs"][name].get("t_count", 0)
    random_h = sum(n["params"]["bits"] for n in source["inputs"])
    assert random_h == schedule["resources"]["random_hadamards"]
    category["uniform_preparation"]["initial_hadamards_separate"] = random_h
    ranked = sorted(
        owners.items(), key=lambda pair: (-pair[1]["exclusive_batch_t_depth"], pair[0])
    )[:3]
    top_leafs = []
    for key, owner in ranked:
        zero_cost_depth = 2 * sum(
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
        top_leafs.append(
            {
                "leaf": key,
                "op": entries[key]["op"],
                "params": entries[key]["params"],
                **dict(owner),
                "fixed_batch_zero_cost_depth_diagnostic": zero_cost_depth,
                "optimistic_fixed_batch_depth_saving": tdepth - zero_cost_depth,
            }
        )
    comparison = load(directory / "comparison.json")
    assert comparison["accepted"] and comparison["replay_passed"]
    result = {
        "case": case,
        "passed": True,
        "decision": "completed_scoped_cost_audit",
        "source_manifest_scope": "Unchanged canonical full-width serial manifest; compact executed resources are schedule_capped.json, not source.json's serial fields.",
        "counts": totals,
        "source_values": values,
        "forward_calls": len(calls),
        "retained_ssa_qubits": cursor,
        "named_output_qubits": len(source["outputs"]) * word,
        "peak_private_scratch_qubits": peak_scratch,
        "logical_qubits": retained + peak_scratch,
        "qubit_cap": schedule["qubit_cap"],
        "t_depth": tdepth,
        "clifford_t_depth": ctdepth,
        "independent_forward_dependency_t_depth": dag_depth,
        "batch_count": len(batch_rows),
        "copy_ledger": {
            "clean_argument_copy_cx": active_copies - output_copies,
            "output_copy_cx": output_copies,
            "total_copy_cx": active_copies,
            "full_width_total_copy_cx": baseline_copies,
            "saved_copy_cx": baseline_copies - active_copies,
            "clean_shared_control_copy_depth": copy_depth,
            "output_copy_depth": output_depth,
        },
        "width_histogram": dict(Counter(widths)),
        "one_bit_retained_values": widths.count(1),
        "leaf_register_validation": "Every argument/output uses its actual metadata register wires; active SSA width must fit it. Private scratch includes omitted output wires. Full-width external outputs remain separately allocated, including when a retained SSA result is one bit.",
        "category_costs": {name: dict(value) for name, value in category.items()},
        "operation_ranking": sorted(
            ({"op": op, **dict(value)} for op, value in work.items()),
            key=lambda value: (-value.get("exclusive_batch_t_depth", 0), value["op"]),
        ),
        "top_three_depth_owner_leaves": top_leafs,
        "batches": batch_rows,
        "new_gate_replays": 0,
        "prior_compact_replays": len(comparison["replays"]),
        "interpretation": "Category depths overlap and must not be summed. Deterministic batch owners are attribution, not attainable marginal savings. Zero-cost depth rows freeze current batches and are optimistic diagnostics only; no source replacement or physical speedup is claimed.",
    }
    return result


def run(output):
    output.mkdir(parents=True, exist_ok=False)
    report = ROOT / "docs/limitation_program_20261001/COMPACT_COST_LEDGER.md"
    assert not report.exists()
    tracked = {}
    for case in ("B4x12", "B8x52"):
        for name in (
            "target.json",
            "source.json",
            "schedule_capped.json",
            "comparison.json",
            "unchanged_leaves.json",
        ):
            path = COMPACT / case / name
            tracked[path.relative_to(ROOT).as_posix()] = sha(path)
        path = ORIGINAL / (case + "_accounting.json")
        tracked[path.relative_to(ROOT).as_posix()] = sha(path)
    frozen_manifest = load(ORIGINAL / "manifest.json")
    tracked[(ORIGINAL / "manifest.json").relative_to(ROOT).as_posix()] = sha(
        ORIGINAL / "manifest.json"
    )
    dump(
        output / "protocol.json",
        {
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "item": "A01",
            "scope": "Independent accounting update after accepted A06 compact integration",
            "producer_sha256": sha(Path(__file__)),
            "frozen_inputs": tracked,
            "before_analysis": True,
            "classification": "Reuse frozen A01_run003 attribution; assign every call once and recompute compact argument/output CX costs from proved widths.",
            "checks": "Exact unchanged target/source hashes and immutable leaf hashes, independent possible-one masks, real register-wire metadata, Kahn DAG, every compact capped batch, counts and resource fields",
            "stop_rule": "Two existing cases, one pass each; abort on mismatch. No new full gate or financial replay, no old manifests or progress edit.",
            "depth_interpretation": "Overlap diagnostics are not serial sums. One deterministic maximum owner per batch gives attribution; frozen-batch zero-cost estimates are not achievable improvements.",
            "local_only": True,
        },
    )
    dump(output / "environment.json", environment())
    results = []
    for case in ("B4x12", "B8x52"):
        result = analyze(case, frozen_manifest["frozen_inputs"], tracked)
        results.append(result)
        dump(output / (case + "_ledger.json"), result)
        print(case, "PASS", result["t_depth"], result["batch_count"], "batches", flush=True)
    summary = {
        "passed": True,
        "decision": "completed_scoped_cost_audit",
        "cases": [
            {
                key: r[key]
                for key in (
                    "case",
                    "counts",
                    "retained_ssa_qubits",
                    "peak_private_scratch_qubits",
                    "logical_qubits",
                    "qubit_cap",
                    "t_depth",
                    "clifford_t_depth",
                    "batch_count",
                    "copy_ledger",
                    "top_three_depth_owner_leaves",
                )
            }
            for r in results
        ],
        "G2_G5": "unresolved",
        "next": "Complete the proved seven-bit logarithm-exponent integration already underway, then re-rank. Further exact trials should target the actual mul/cmul/sqrt owner leaves with capped source-wide validation.",
        "new_gate_replays": 0,
    }
    dump(output / "summary.json", summary)
    dump(output / "result.json", summary)
    dump(
        output / "verification.json",
        {
            "passed": True,
            "producer_sha256": sha(Path(__file__)),
            "command": ".context/frontier_t0_env/Scripts/python.exe -m research.limitation_program_20261001.compact_ledger --output results/limitation_program_20261001/A01_run004",
            "checks": [
                "All old target/source/category and used leaf hashes unchanged",
                "Independent active-bit masks equal accepted widths/masks",
                "All actual register wires/widths and zero-low input promises valid",
                "All seven gate count fields and exact seven-T expansion reconcile",
                "All calls occur once in valid dependency waves",
                "Independent DAG and every batch scratch/T/Clifford/copy depth reconcile",
                "Peak qubits and both original caps checked",
                "Category T work unchanged and CX copying savings assigned once",
            ],
            "new_replays": 0,
            "prior_replays": {r["case"]: r["prior_compact_replays"] for r in results},
        },
    )
    with (output / "NEXT.md").open("x", encoding="utf-8") as handle:
        handle.write(
            "# Next local action\n\nFinish the seven-bit logarithm-exponent integration already supplied by A07/A10, revalidate its full compact schedule, then rerank the ledger. Multiplication, remaining constant multiplication and square root dominate current batch attribution. Fixed-batch zero-cost screens only prioritize proof/implementation; they are not achievable gains. Keep the current accepted compact sources when a candidate fails. G2-G5 remain unresolved.\n"
        )
    lines = [
        "# Reconciled compact-source cost ledger\n\n",
        "Local A01 follow-up, 1 October 2026. The accepted A06 compact sources were independently checked against frozen original tasks, node categories and immutable leaf hashes. No gate replay was repeated. The same exact financial IR, precision and arithmetic leaves remain; lower argument-copy CX and different memory packing account for the resource change. The untouched source.json still describes its canonical full-width serial implementation; schedule_capped.json describes the accepted compact execution.\n\n",
        "| Case | T gates | Compact T-depth | Clifford+T depth | Actual logical qubits / cap | Retained SSA qubits | Saved copy CX | Batches |\n|---|---:|---:|---:|---:|---:|---:|---:|\n",
    ]
    for r in results:
        lines.append(
            f"| {r['case']} | {r['counts']['t_count']:,} | {r['t_depth']:,} | {r['clifford_t_depth']:,} | {r['logical_qubits']:,} / {r['qubit_cap']:,} | {r['retained_ssa_qubits']:,} | {r['copy_ledger']['saved_copy_cx']:,} | {r['batch_count']} |\n"
        )
    lines.append(
        "\nAll X/CCX/T counts remain unchanged. source_gates, CX and expanded Clifford CX each decrease by exactly the saved copy count. Every active-bit width/offset/mask, actual leaf argument/output register, omitted-output scratch wire, zero-low input promise, call occurrence, dependency wave, batch depth and peak allocation reconciles. External named outputs remain full width; one-bit SSA flags do not cause accidental one-bit external-output allocation.\n\n"
    )
    for r in results:
        lines.append(
            f"## {r['case']} attribution\n\n| Category | Clean T gates | Clean argument-copy CX | Copy CX saved | Overlapping capped T-depth diagnostic |\n|---|---:|---:|---:|---:|\n"
        )
        for name in CATEGORIES:
            c = r["category_costs"][name]
            lines.append(
                f"| {name} | {c.get('t_count', 0):,} | {c.get('clean_argument_copy_cx', 0):,} | {c.get('saved_argument_copy_cx', 0):,} | {c.get('overlapping_capped_t_depth_diagnostic', 0):,} |\n"
            )
        lines.append(
            "\nTop three deterministic depth-owner operations: "
            + ", ".join(
                f"{item['op']} ({item.get('exclusive_batch_t_depth', 0):,} attributed layers)"
                for item in r["operation_ranking"][:3]
            )
            + ".\n\n"
        )
        lines.append("Top three individual depth-owner leaves:\n\n")
        for leaf in r["top_three_depth_owner_leaves"]:
            lines.append(
                f"- `{leaf['leaf']}`: {leaf['op']}, params `{json.dumps(leaf['params'], sort_keys=True)}`, {leaf['exclusive_batch_t_depth']:,} attributed layers; its optimistic frozen-batch zero-cost saving is {leaf['optimistic_fixed_batch_depth_saving']:,} layers.\n"
            )
        lines.append(
            f"\nIndependent forward DAG depth remains {r['independent_forward_dependency_t_depth']:,}. The ledger checks {r['one_bit_retained_values']:,} retained one-bit values, {r['named_output_qubits']} named-output qubits and peak private scratch of {r['peak_private_scratch_qubits']:,}. Existing A06 evidence contains {r['prior_compact_replays']} complete replay records for this case; this audit reuses them.\n\n"
        )
    lines.append(
        "Category depths overlap within batches and are not serial elapsed-time sums. Deterministic batch ownership is additive bookkeeping only, with tie effects; frozen-batch zero-cost rows are optimistic prioritization diagnostics. Repacking or a different leaf can change the remaining maxima. No independent speedup factors are multiplied.\n\n"
    )
    lines.append(
        "Next: finish the already proved seven-bit logarithm-exponent integration, verify the resulting complete compact schedules, and rerank. The current operation ranking prioritizes multiplication, other expensive constants and square root. Source validity is an arithmetic result; G2 continuous-dollar certification, G3 an explicit compatible estimator, G4 actual matched classical target timing and G5 physical resources remain unresolved. All work stayed local.\n\n"
    )
    lines.append(
        "Receipts: [summary](../../results/limitation_program_20261001/A01_run004/summary.json), [complete accounting](../../results/limitation_program_20261001/A01_run004/), [producer](../../research/limitation_program_20261001/compact_ledger.py). The frozen original [baseline](BASELINE.md) and its manifests remain unchanged.\n"
    )
    with report.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write("".join(lines))
    tracked[Path(__file__).relative_to(ROOT).as_posix()] = sha(Path(__file__))
    tracked[report.relative_to(ROOT).as_posix()] = sha(report)
    assert all(sha(ROOT / path) == digest for path, digest in tracked.items())
    files = {
        p.relative_to(ROOT).as_posix(): sha(p) for p in sorted(output.rglob("*")) if p.is_file()
    }
    dump(
        output / "manifest.json",
        {"files": files, "frozen_inputs": tracked, "manifest_self_hash_excluded": True},
    )
    assert all(sha(ROOT / path) == digest for path, digest in files.items())
    print("Independent compact cost ledger completed; original receipts unchanged.", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output.resolve())
