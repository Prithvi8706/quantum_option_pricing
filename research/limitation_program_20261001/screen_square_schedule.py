"""Bounded schedule-only relaxation for same-SSA squares on accepted A11.

No gates are emitted or replayed. A zero-work/zero-scratch square is an
unrealizable optimistic relaxation. Weighted capacity lower bounds apply only
to the unchanged dependency waves, non-square leaves and retained storage.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
from importlib import metadata
import json
from pathlib import Path
import platform
import random
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
A11 = ROOT / "results/limitation_program_20261001/A11_run001"
SCOPE = ROOT / "results/limitation_program_20261001/A09_square_scope_run001"
CASES = ("B4x12", "B8x52")
THRESHOLDS = (0.1, 2.0)


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def dump(path, value):
    with Path(path).open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def relative(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def library_path(source):
    for field in ("library_workspace_relative", "library"):
        raw = source.get(field)
        if not raw:
            continue
        path = Path(str(raw).replace("\\", "/"))
        if ".." in path.parts:
            raise ValueError("parent traversal in local library path")
        if not path.is_absolute():
            path = ROOT / path
        if path.is_dir():
            return path.resolve()
    raise ValueError("accepted local leaf library cannot be resolved")


def ceil_div(value, denominator):
    return (value + denominator - 1) // denominator


def pack(items, capacity):
    """Same deterministic first-fit decreasing depth policy as accepted A11."""
    batches = []
    for item in sorted(items, key=lambda item: (-item["depth"], item["index"])):
        if not 0 <= item["scratch"] <= capacity:
            raise ValueError("item does not fit capacity")
        batch = next((b for b in batches if b["scratch"] + item["scratch"] <= capacity),
                     None)
        if batch is None:
            batch = {"indices": [], "scratch": 0, "depth": 0}
            batches.append(batch)
        batch["indices"].append(item["index"])
        batch["scratch"] += item["scratch"]
        batch["depth"] = max(batch["depth"], item["depth"])
    return batches


def memory_lower_bound(items, capacity):
    """Valid bin-count bounds; no claim to solve general bin packing."""
    if not items:
        return 0
    result = max(1, ceil_div(sum(item["scratch"] for item in items), capacity))
    sizes = Counter(item["scratch"] for item in items if item["scratch"])
    for size, count in sizes.items():
        result = max(result, ceil_div(count, capacity // size))
    # A bin can hold at most m items individually greater than C/(m+1).
    for m in range(1, min(64, len(items)) + 1):
        count = sum(item["scratch"] * (m + 1) > capacity for item in items)
        result = max(result, ceil_div(count, m))
    return result


def wave_lower_bound(items, capacity):
    """Integrate mandatory bin counts for every positive depth threshold.

    For any packing, sum(batch maximum depth) equals the integral of the
    number of batches containing a leaf with depth >= threshold. Restricting
    to those leaves cannot increase their needed capacity, giving a valid
    lower bound on this sum for every packing of these same-wave items.
    """
    threshold_rows, total, previous = [], 0, 0
    for depth in sorted({item["depth"] for item in items if item["depth"] > 0}):
        active = [item for item in items if item["depth"] >= depth]
        bins = memory_lower_bound(active, capacity)
        contribution = (depth - previous) * bins
        threshold_rows.append({"threshold": depth, "width": depth - previous,
                               "mandatory_batches": bins, "contribution": contribution})
        total += contribution
        previous = depth
    return {"minimum_non_square_batches": memory_lower_bound(items, capacity),
            "maximum_leaf_depth_lower_bound": max((item["depth"] for item in items), default=0),
            "weighted_capacity_sum_maxima_lower_bound": total,
            "depth_thresholds": threshold_rows}


def exact_small_packing_cost(items, capacity):
    """Independent subset-partition oracle, used only on n <= 6 synthetic items."""
    @lru_cache(None)
    def solve(remaining):
        if not remaining:
            return 0
        anchor = remaining & -remaining
        subset, best = remaining, None
        while subset:
            if subset & anchor:
                selected = [item for i, item in enumerate(items) if subset & (1 << i)]
                if sum(item["scratch"] for item in selected) <= capacity:
                    value = max(item["depth"] for item in selected) + solve(remaining ^ subset)
                    best = value if best is None else min(best, value)
            subset = (subset - 1) & remaining
        if best is None:
            raise ValueError("synthetic item exceeds capacity")
        return best
    return solve((1 << len(items)) - 1)


def validate_synthetic():
    original = [{"index": 0, "scratch": 6, "depth": 10, "square": True},
                {"index": 1, "scratch": 4, "depth": 10, "square": False},
                {"index": 2, "scratch": 4, "depth": 10, "square": False}]
    groups = pack(original, 10)
    fixed = sum(max((original[i]["depth"] for i in g["indices"]
                     if not original[i]["square"]), default=0) for g in groups)
    nonsquares = [item for item in original if not item["square"]]
    repacked = sum(g["depth"] for g in pack(nonsquares, 10))
    assert sum(g["depth"] for g in groups) == fixed == 20
    assert repacked == wave_lower_bound(nonsquares, 10)[
        "weighted_capacity_sum_maxima_lower_bound"] == 10
    rng = random.Random(20261001)
    for index in range(64):
        items = [{"index": i, "scratch": rng.randrange(11), "depth": rng.randrange(13)}
                 for i in range(index % 7)]
        lower = wave_lower_bound(items, 10)["weighted_capacity_sum_maxima_lower_bound"]
        exact = exact_small_packing_cost(items, 10)
        first_fit = sum(g["depth"] for g in pack(items, 10))
        assert lower <= exact <= first_fit
        assert memory_lower_bound(items, 10) <= len(pack(items, 10))
    return {"passed": True, "random_subset_partition_oracle_cases": 64,
            "fixed_group_counterexample": {"actual_depth": 20,
                                            "fixed_groups_squares_zero_work_depth": fixed,
                                            "zero_square_scratch_repacked_depth": repacked},
            "meaning": "Fixed-group zeroing is not a global bound; capacity relaxation validated"}


def screen_case(case):
    target = load(A11 / case / "target.json")
    source = load(A11 / case / "source.json")
    schedule = load(A11 / case / "schedule_capped.json")
    inventory = load(SCOPE / (case + "_inventory.json"))
    assert target["width"] == source["word_width"] == 72
    assert target["fraction_bits"] == source["fraction_bits"] == 40
    path = library_path(source)
    entries = {key: load(path / (key + ".json")) for key in source["library_keys"]}
    nodes = [(i, node) for i, node in enumerate(target["nodes"]) if node["op"] != "input"]
    assert len(nodes) == len(source["forward_calls"])
    expected_sites = {index for index, (_, node) in enumerate(nodes)
                      if node["op"] == "mul" and len(node["args"]) == 2
                      and node["args"][0] == node["args"][1]}
    square_sites = {site["call_index"]: site for site in inventory["square_sites"]}
    assert set(square_sites) == expected_sites
    levels = {value: 0 for node in source["inputs"] for value in node["out"]}
    waves = defaultdict(list)
    widths = schedule["widths"]
    paired = zip(nodes, source["forward_calls"], strict=True)
    for index, ((node_index, node), call) in enumerate(paired):
        entry = entries[call["leaf"]]
        assert (node["args"], node["out"]) == (call["args"], call["out"])
        assert (node["op"], node["params"]) == (entry["op"], entry["params"])
        level = 1 + max((levels[value] for value in call["args"]), default=0)
        for value in call["out"]:
            assert value not in levels
            levels[value] = level
        if index in square_sites:
            site = square_sites[index]
            assert site["node_index"] == node_index
            assert site["input_value"] == node["args"][0]
            assert site["output_value"] == node["out"][0]
            assert site["actual_same_ssa_alias"] == node["args"]
            assert site["leaf"] == call["leaf"]
        waves[level].append({"index": index, "depth": entry["resources"]["t_depth"],
                             "scratch": entry["resources"]["qubits"] - sum(
                                 widths[value] for value in call["out"]),
                             "square": index in square_sites})
    retained = schedule["retained_ssa_qubits"] + len(source["outputs"]) * source["word_width"]
    assert retained == sum(widths) + 72 * len(source["outputs"])
    capacity = schedule["qubit_cap"] - retained
    assert capacity > 0
    actual_groups = defaultdict(list)
    for group in schedule["groups"]:
        actual_groups[group["wave"]].append(group)
    assert set(actual_groups) == set(waves)
    records, actual_forward, fixed_forward, repack_forward, lower_forward = [], 0, 0, 0, 0
    for wave, items in sorted(waves.items()):
        rebuilt = pack(items, capacity)
        groups = actual_groups[wave]
        assert len(rebuilt) == len(groups)
        assert all(g["indices"] == old["call_indices"]
                   and g["scratch"] == old["private_scratch_qubits"]
                   and g["depth"] == old["t_depth"]
                   for g, old in zip(rebuilt, groups, strict=True))
        by_index = {item["index"]: item for item in items}
        actual_depth = sum(g["depth"] for g in rebuilt)
        fixed_depth = sum(max((by_index[i]["depth"] for i in g["indices"]
                               if not by_index[i]["square"]), default=0) for g in rebuilt)
        nonsquares = [item for item in items if not item["square"]]
        hypothetical = pack(nonsquares, capacity)
        repack_depth = sum(g["depth"] for g in hypothetical)
        lower = wave_lower_bound(nonsquares, capacity)
        assert lower["weighted_capacity_sum_maxima_lower_bound"] <= repack_depth
        actual_forward += actual_depth
        fixed_forward += fixed_depth
        repack_forward += repack_depth
        lower_forward += lower["weighted_capacity_sum_maxima_lower_bound"]
        records.append({"wave": wave, "square_calls": len(items) - len(nonsquares),
                        "non_square_calls": len(nonsquares), "actual_batches": len(groups),
                        "hypothetical_repacked_batches": len(hypothetical),
                        "actual_forward_depth": actual_depth,
                        "fixed_group_zero_square_forward_depth": fixed_depth,
                        "hypothetical_repacked_forward_depth": repack_depth,
                        **lower, "hypothetical_groups": hypothetical})
    actual = 2 * actual_forward
    assert actual == schedule["resources"]["t_depth"]
    rigorous_lower = 2 * lower_forward
    maximum_gain = 100 * (actual - rigorous_lower) / actual
    return {"case": case, "passed": True, "same_ssa_square_calls": len(square_sites),
            "actual_t_depth": actual, "actual_batches": len(schedule["groups"]),
            "retained_storage_qubits": retained, "qubit_cap": schedule["qubit_cap"],
            "available_private_scratch_qubits": capacity,
            "fixed_group_zero_square_work_t_depth": 2 * fixed_forward,
            "fixed_group_diagnostic_gain_percent": 100 * (actual - 2 * fixed_forward) / actual,
            "hypothetical_zero_square_work_and_scratch_repacked_t_depth": 2 * repack_forward,
            "hypothetical_repacked_gain_percent": 100 * (actual - 2 * repack_forward) / actual,
            "rigorous_same_wave_relaxation_t_depth_lower_bound": rigorous_lower,
            "rigorous_gain_upper_bound_percent_within_stated_class": maximum_gain,
            "thresholds_ruled_out_within_stated_class": {
                str(threshold): maximum_gain < threshold for threshold in THRESHOLDS},
            "hypothetical_total_non_square_batches": sum(
                row["hypothetical_repacked_batches"] for row in records),
            "memory_lower_bound_total_non_square_batches": sum(
                row["minimum_non_square_batches"] for row in records),
            "per_wave": records,
            "new_gates_or_realized_resource_improvement": False,
            "bound_class": "Same waves; unchanged non-square leaves and retained storage",
            "outside_bound_class": "Cross-wave scheduling, changed leaves, reduced SSA storage"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    destination = (ROOT / args.output).resolve()
    destination.relative_to(ROOT)
    if destination.exists():
        raise ValueError("fresh local receipt directory required")
    destination.mkdir(parents=True)
    started = time.perf_counter()
    files = [A11 / name for name in ("summary.json", "protocol.json", "manifest.json")]
    files += [SCOPE / name for name in ("summary.json", "protocol.json", "manifest.json")]
    files += [Path(__file__).resolve()]
    for case in CASES:
        files += [A11 / case / name for name in
                  ("target.json", "source.json", "schedule_capped.json")]
        files.append(SCOPE / (case + "_inventory.json"))
        source = load(A11 / case / "source.json")
        path = library_path(source)
        for key in source["library_keys"]:
            leaf = path / (key + ".json")
            files += [leaf, path / load(leaf)["gate_file"]]
    frozen = {relative(path): sha(path) for path in sorted(set(files))}
    executed = destination / "executed_screen_square_schedule.py"
    shutil.copy2(Path(__file__), executed)
    protocol = {
        "format": "prospective-same-wave-square-schedule-relaxation-v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {"python": sys.version, "executable": str(Path(sys.executable).resolve()),
                        "interpreter_sha256": sha(sys.executable), "platform": platform.platform(),
                        "packages": sorted((d.metadata["Name"], d.version)
                                           for d in metadata.distributions()),
                        "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"],
                                                            cwd=ROOT, text=True).strip()},
        "frozen_inputs": frozen, "executed_code_sha256": sha(executed),
        "eligibility": "Full72/f40 mul with identical actual SSA argument IDs",
        "models": ["Actual accepted batches", "Fixed-group zero square work diagnostic",
                   "Zero square work/scratch; re-pack non-square leaves by original FFD rule",
                   "Threshold capacity lower bound for every packing within original waves"],
        "thresholds_percent": list(THRESHOLDS),
        "validation": "Tied-max counterexample and 64 seeded <=6-item exact partition oracles",
        "preserved": "All dependency waves, retained SSA/output storage and original copy contract",
        "interpretation": "No hypothetical output is an emitted circuit or an achieved gain",
        "outside_lower_bound_scope": "Cross-wave scheduling, changed leaves or SSA storage",
        "stopping": "One bounded screen; no gates/replays/new financial or physical conclusions",
    }
    dump(destination / "protocol.json", protocol)
    assert load(A11 / "summary.json")["accepted"]
    validation = validate_synthetic()
    dump(destination / "synthetic_validation.json", validation)
    cases = []
    for case in CASES:
        result = screen_case(case)
        dump(destination / (case + "_screen.json"), result)
        cases.append({key: value for key, value in result.items() if key != "per_wave"})
    both_rule_out = {str(threshold): all(case["thresholds_ruled_out_within_stated_class"][
        str(threshold)] for case in cases) for threshold in THRESHOLDS}
    summary = {"passed": True, "cases": cases, "thresholds_ruled_out_in_both_cases": both_rule_out,
               "realized_circuit_gain_claimed": False,
               "financial_or_physical_gate_closed": False,
               "interpretation": "Hypothetical FFD is diagnostic; bounds have stated scope",
               "seconds": time.perf_counter() - started}
    dump(destination / "summary.json", summary)
    mismatches = {name: (expected, sha(ROOT / name)) for name, expected in frozen.items()
                  if sha(ROOT / name) != expected}
    assert not mismatches
    dump(destination / "verification.json", {"passed": True, "frozen_inputs": len(frozen),
                                              "input_mismatches": mismatches,
                                              "executed_code_matches":
                                              sha(executed) == sha(__file__)})
    receipt_files = {relative(path): sha(path) for path in destination.rglob("*") if path.is_file()}
    dump(destination / "manifest.json", {"format": "local-square-schedule-screen-receipt-v1",
                                          "files": receipt_files, "frozen_inputs": frozen})
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
