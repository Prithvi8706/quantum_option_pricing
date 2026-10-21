"""Freeze local B4/B8 task provenance and independently reconcile source costs.

Read-only with respect to accepted archives. Writes prospective protocols before
rebuilding graphs or deriving counts. Does not execute a pricing or gate replay.
"""

# Receipt and Markdown prose strings deliberately retain their full text.
# ruff: noqa: E501

from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
import hashlib
from importlib import metadata
import json
import math
from pathlib import Path
import platform
import subprocess
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "results/limitation_audit_20261001/constant_multiplier_v1"
CATEGORIES = ("uniform_preparation", "scalar_normals", "correlation", "path_payoff", "shared")
COUNT_FIELDS = ("source_gates", "x", "cx", "ccx", "t_count", "clifford_cx", "clifford_h")
CODE_PATHS = (
    "research/limitation_program_20261001/baseline.py",
    "research/advantage_frontier_20260923/barrier_oracle_depth.py",
    "research/controlled_source_completion/finance.py",
    "research/controlled_source_completion/ir.py",
    "research/controlled_source_completion/optimize.py",
    "research/controlled_source_completion/compiler.py",
    "research/controlled_source_completion/budget_schedule.py",
    "research/controlled_priority_completion/parallel_source.py",
    "research/controlled_source_completion/constant_multiplier.py",
    "research/controlled_source_completion/carry_save_multiplier.py",
    "research/controlled_source_completion/exact_lookup.py",
)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical_hash(data):
    raw = json.dumps(data, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    return hashlib.sha256(raw).hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def dump(path, data):
    with Path(path).open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(data, indent=2, sort_keys=True, allow_nan=False) + "\n")


def environment():
    return {
        "python": sys.version,
        "executable": str(Path(sys.executable).resolve()),
        "interpreter_sha256": sha(sys.executable),
        "platform": platform.platform(),
        "packages": sorted(
            [{"name": d.metadata["Name"], "version": d.version} for d in metadata.distributions()],
            key=lambda d: (str(d["name"]).casefold(), d["version"]),
        ),
        "git_head": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "code_sha256": {p: sha(ROOT / p) for p in CODE_PATHS},
        "meaning": "Existing local environment snapshot, not a fresh hash-pinned installation.",
    }


def fingerprints(data):
    """Semantic structural IDs survive commutative ordering and exact CSE.

    The rebuilt current financial graph is also compared in full after applying
    the archived optimizer. These IDs only transfer boundary labels, not prices.
    """
    result, constants = {}, {}
    mask = (1 << data["width"]) - 1
    for node in data["nodes"]:
        raw_args = node["args"]
        alias = None
        if node["op"] == "add":
            if constants.get(raw_args[0]) == 0:
                alias = raw_args[1]
            elif constants.get(raw_args[1]) == 0:
                alias = raw_args[0]
        elif node["op"] == "sub" and constants.get(raw_args[1]) == 0:
            alias = raw_args[0]
        elif node["op"] == "select" and raw_args[1] == raw_args[2]:
            alias = raw_args[1]
        elif node["op"] == "cmul" and node["params"]["c"] == 2 ** data["fraction_bits"]:
            alias = raw_args[0]
        elif (
            node["op"] == "bits"
            and node["params"]["shift"] == 0
            and node["params"]["width"] == data["width"]
        ):
            alias = raw_args[0]
        if alias is not None:
            assert len(node["out"]) == 1
            result[node["out"][0]] = result[alias]
            if alias in constants:
                constants[node["out"][0]] = constants[alias]
            continue
        args = [result[a] for a in node["args"]]
        if node["op"] in ("add", "mul"):
            args.sort()
        params = dict(node["params"])
        if node["op"] == "const":
            params["value"] &= mask
            constants[node["out"][0]] = params["value"]
        for index, value in enumerate(node["out"]):
            result[value] = canonical_hash([node["op"], args, params, index, len(node["out"])])
    return result


def graph_boundaries(assets, dates, target):
    from research.advantage_frontier_20260923 import barrier_oracle_depth as builder
    from research.controlled_source_completion.optimize import optimize

    original_normals = builder.normals_graph
    normal_roots = []

    def capture(graph, count, precision):
        roots = original_normals(graph, count, precision)
        normal_roots.extend(roots)
        return roots

    builder.normals_graph = capture
    try:
        # JSON archives encode coefficient tuples as lists. Normalize only the
        # container representation before testing complete graph equality.
        original = json.loads(json.dumps(builder.build(assets, dates).as_dict()))
    finally:
        builder.normals_graph = original_normals
    rebuilt = optimize(original)
    assert rebuilt == target, "Current financial builder/optimizer differs from accepted target"
    assert rebuilt["optimization"]["constant_folded_nodes"] == 0
    before, after = fingerprints(original), fingerprints(target)
    reverse = {token: value for value, token in after.items()}
    assert len(reverse) == len(after), "Optimized graph has ambiguous structural IDs"
    normals = [reverse[before[v]] for v in normal_roots]
    normal_set = set(normals)
    assert len(normals) == dates * (assets + 1)
    dt = builder.T / dates
    common_c = round(builder.SIGMA * math.sqrt(dt * builder.CORR) * 2 ** target["fraction_bits"])
    idio_c = round(
        builder.SIGMA * math.sqrt(dt * (1 - builder.CORR)) * 2 ** target["fraction_bits"]
    )
    drift = round((builder.RATE - 0.5 * builder.SIGMA**2) * dt * 2 ** target["fraction_bits"])
    producers = {v: node for node in target["nodes"] for v in node["out"]}
    increments = []
    for node in target["nodes"]:
        if node["op"] != "add":
            continue
        noise, fixed = sorted((producers[v] for v in node["args"]), key=lambda n: n["op"])
        if noise["op"] != "add" or fixed["op"] != "const":
            continue
        if fixed["params"]["value"] != drift % (1 << target["width"]):
            continue
        operands = [producers[v] for v in noise["args"]]
        if not all(n["op"] == "cmul" and n["args"][0] in normal_set for n in operands):
            continue
        if sorted(n["params"]["c"] for n in operands) != sorted((common_c, idio_c)):
            continue
        increments.append(node["out"][0])
    assert len(increments) == assets * dates, "Correlation/increment boundary mismatch"
    financial = {
        "model": "correlated geometric Brownian motion at contractual dates",
        "assets": assets,
        "dates": dates,
        "observation_times": [(j + 1) * builder.T / dates for j in range(dates)],
        "spot_each_asset_dollars": builder.S0,
        "strike_dollars": builder.K,
        "barrier_dollars": builder.H,
        "annual_rate": builder.RATE,
        "annual_volatility_each_asset": builder.SIGMA,
        "maturity_years": builder.T,
        "equicorrelation": builder.CORR,
        "equity_covariance_matrix": [
            [1.0 if i == j else builder.CORR for j in range(assets)] for i in range(assets)
        ],
        "payoff": "exp(-r*T) * max(mean over all asset/date spots - K, 0) * indicator(max over monitored dates of equal-weight spot basket < H)",
        "barrier_equality": "basket >= H is knocked out; alive uses strict < H",
        "notional_semantics": {
            "initial_equal_weight_basket_dollars": builder.S0,
            "participation": 1,
            "separate_notional_multiplier": None,
            "interpretation": "One unit of the equal-weight basket/Asian call. Initial basket is $100; payoff is already in dollars. No extra factor of 100 or 0.01 is introduced.",
            "recovered_from": "barrier_oracle_depth.build constants, 1/assets and 1/(assets*dates) averages, strike and discount; matches Stage A original_target and optimized target",
        },
        "discount": math.exp(-builder.RATE * builder.T),
        "continuous_sampling": "Independent common/idiosyncratic standard normals give exact GBM log increments at each contractual date before numerical representation.",
        "digital_source": {
            "word_width": target["width"],
            "fraction_bits": target["fraction_bits"],
            "uniform_bits_each": 32,
            "uniform_midpoint": "u=(integer+1/2)/2^32",
            "law": "Independent uniform 32-bit integers, paired Box-Muller with existing log/cos polynomial tables and integer square root",
            "normal_count": len(normals),
            "spot_guard": [2**-16, 4096.0],
            "guard_semantics": "Each accumulated log spot is clipped before its Estrin exponential; the digital guard's continuous-price bias remains unproved.",
            "exponential": "ln(2) range reduction and degree-12 Taylor polynomial evaluated by Estrin",
            "integer_semantics": target["semantics"],
            "output": target["outputs"],
            "output_dollar_conversion": "Interpret output Y as signed two's-complement integer divided by 2^40; discount is already applied.",
        },
        "output_contract": {
            "delivered_output": "one classical discounted dollar price",
            "absolute_error_dollars": [0.10, 0.03, 0.01, 0.001],
            "final_strict_target_scope": "0.001 is the historical B4/B8 knock-out final test, not silently extended to every source family",
            "per_price_success_probability_at_least": 0.99,
            "complete_advantage": "T_Q <= fastest eligible complete measured T_C / 10",
            "statistical_share_reference": "e=0.45*epsilon retained as a historical/planning allocation, not an implemented estimator",
        },
    }
    return original, financial, normals, increments


def classify(target, normals, increments):
    producers = {v: i for i, n in enumerate(target["nodes"]) for v in n["out"]}
    input_nodes = {i for i, n in enumerate(target["nodes"]) if n["op"] == "input"}

    def closure(roots, boundaries=()):
        stop = set(boundaries)
        seen, stack = set(), list(roots)
        while stack:
            value = stack.pop()
            if value in stop:
                continue
            index = producers[value]
            if index in seen or index in input_nodes:
                continue
            seen.add(index)
            stack.extend(target["nodes"][index]["args"])
        return seen

    sets = {
        "scalar_normals": closure(normals),
        "correlation": closure(increments, normals),
        "path_payoff": closure(target["outputs"].values(), [*normals, *increments]),
    }
    labels, shared = {}, []
    for i, node in enumerate(target["nodes"]):
        if i in input_nodes:
            labels[i] = "uniform_preparation"
            continue
        members = [name for name, nodes in sets.items() if i in nodes]
        assert members, ("Unattributed non-input node", i, node)
        labels[i] = members[0] if len(members) == 1 else "shared"
        if len(members) > 1:
            shared.append({"node_index": i, "memberships": members, "node": node})
    assert len(labels) == len(target["nodes"])
    return labels, shared


def independent_dag(source, leafs):
    """Kahn traversal, independent of the compiler's ordered arrival loop."""
    calls = source["forward_calls"]
    producer = {}
    for i, call in enumerate(calls):
        for value in call["out"]:
            assert value not in producer
            producer[value] = i
    inputs = {v for n in source["inputs"] for v in n["out"]}
    parents, children = {}, defaultdict(set)
    for i, call in enumerate(calls):
        assert all(v in producer or v in inputs for v in call["args"])
        parents[i] = {producer[v] for v in call["args"] if v in producer}
        for p in parents[i]:
            children[p].add(i)
    pending = {i: len(p) for i, p in parents.items()}
    queue = deque(i for i, count in pending.items() if not count)
    arrival, level, predecessor = {}, {}, {}
    while queue:
        i = queue.popleft()
        p = min(parents[i], key=lambda j: (-arrival[j], j)) if parents[i] else None
        predecessor[i] = p
        arrival[i] = (arrival[p] if p is not None else 0) + leafs[calls[i]["leaf"]]["resources"][
            "t_depth"
        ]
        level[i] = 1 + max((level[j] for j in parents[i]), default=0)
        for child in sorted(children[i]):
            pending[child] -= 1
            if not pending[child]:
                queue.append(child)
    assert len(arrival) == len(calls), "DAG is cyclic or has omitted producers"
    endpoint = min(
        (producer[v] for v in source["outputs"].values()), key=lambda j: (-arrival[j], j)
    )
    critical = []
    cursor = endpoint
    while cursor is not None:
        critical.append(cursor)
        cursor = predecessor[cursor]
    return arrival[endpoint], level, list(reversed(critical))


def leaf_audit(source, cache, file_hashes):
    library = ROOT / source["library_workspace_relative"].replace("\\", "/")
    result = {}
    for key in source["library_keys"]:
        if key not in cache:
            meta_path = library / (key + ".json")
            entry = load(meta_path)
            gate_path = library / entry["gate_file"]
            actual_hash = sha(gate_path)
            assert actual_hash == entry["sha256"], ("Leaf hash mismatch", key)
            gates = np.load(gate_path, mmap_mode="r")
            counts = Counter(map(int, gates[:, 0]))
            assert set(counts) <= {1, 2, 3}
            raw = {"x": counts[1], "cx": counts[2], "ccx": counts[3], "source_gates": len(gates)}
            raw.update(
                t_count=7 * raw["ccx"],
                clifford_cx=raw["cx"] + 6 * raw["ccx"],
                clifford_h=2 * raw["ccx"],
            )
            assert all(raw[k] == entry["resources"][k] for k in COUNT_FIELDS), key
            file_hashes[str(meta_path.relative_to(ROOT)).replace("\\", "/")] = sha(meta_path)
            file_hashes[str(gate_path.relative_to(ROOT)).replace("\\", "/")] = actual_hash
            cache[key] = entry
        result[key] = cache[key]
    return result


def analyze_case(case, assets, dates, cache, file_hashes):
    folder = ARCHIVE / case / "signed-digit-carry-save"
    target, source, schedule = (
        load(folder / name) for name in ("target.json", "source.json", "schedule_capped.json")
    )
    original, task, normals, increments = graph_boundaries(assets, dates, target)
    original_archive = load(
        ROOT / "results/frontier_completion_20260927/stage_a" / case / "original_target.json"
    )
    assert original == original_archive, "Original financial graph changed since Stage A"
    labels, shared = classify(target, normals, increments)
    leafs = leaf_audit(source, cache, file_hashes)
    node_indices = [i for i, n in enumerate(target["nodes"]) if n["op"] != "input"]
    assert len(node_indices) == len(source["forward_calls"])
    forward = Counter()
    categories = {name: Counter() for name in CATEGORIES}
    operations = defaultdict(Counter)
    call_labels = []
    copy_rounds = 0
    assignments = []
    w = source["word_width"]
    for call_index, (node_index, call) in enumerate(
        zip(node_indices, source["forward_calls"], strict=True)
    ):
        node = target["nodes"][node_index]
        entry = leafs[call["leaf"]]
        assert node["args"] == call["args"] and node["out"] == call["out"]
        assert node["op"] == entry["op"] and node["params"] == entry["params"]
        assert call["argument_copy_cx"] == 2 * len(call["args"]) * w
        category = labels[node_index]
        call_labels.append(category)
        rs = entry["resources"]
        copies = call["argument_copy_cx"]
        copy_rounds += max(Counter(call["args"]).values(), default=0)
        for field in COUNT_FIELDS:
            forward[field] += rs[field]
            categories[category][field] += 2 * rs[field]
        for field in ("source_gates", "cx", "clifford_cx"):
            categories[category][field] += 2 * copies
        categories[category]["argument_copy_cx_clean"] += 2 * copies
        categories[category]["forward_calls"] += 1
        categories[category]["clean_leaf_invocations"] += 2
        categories[category]["serial_leaf_t_depth_diagnostic"] += 2 * rs["t_depth"]
        operations[node["op"]]["clean_t_count"] += 2 * rs["t_count"]
        operations[node["op"]]["clean_leaf_t_depth_diagnostic"] += 2 * rs["t_depth"]
        operations[node["op"]]["forward_calls"] += 1
        forward["t_depth"] += rs["t_depth"]
        forward["clifford_t_depth"] += rs["clifford_t_depth"]
        assignments.append(
            {
                "node_index": node_index,
                "call_index": call_index,
                "category": category,
                "op": node["op"],
                "leaf": call["leaf"],
                "out": call["out"],
            }
        )
    input_count = 0
    for i, node in enumerate(target["nodes"]):
        categories[labels[i]]["target_nodes"] += 1
        if node["op"] == "input":
            input_count += 1
            assert node["params"]["bits"] == 32 and node["params"]["preparation"] == "uniform"
            categories["uniform_preparation"]["initial_hadamards_separate"] += node["params"][
                "bits"
            ]
    clean_copies = sum(2 * call["argument_copy_cx"] for call in source["forward_calls"])
    output_copies = len(source["outputs"]) * w
    for field in ("source_gates", "cx", "clifford_cx"):
        categories["path_payoff"][field] += output_copies
    categories["path_payoff"]["output_copy_cx"] = output_copies
    totals = {
        field: 2 * forward[field]
        + (clean_copies + output_copies if field in ("source_gates", "cx", "clifford_cx") else 0)
        for field in COUNT_FIELDS
    }
    output_depth = max(Counter(source["outputs"].values()).values(), default=0)
    serial_depths = {
        "t_depth": 2 * forward["t_depth"],
        "clifford_t_depth": 2 * forward["clifford_t_depth"] + 4 * copy_rounds + output_depth,
    }
    for field, value in {**totals, **serial_depths}.items():
        assert source["resources"][field] == value, (case, "serial", field)
    for field in COUNT_FIELDS:
        assert sum(c[field] for c in categories.values()) == totals[field], (
            case,
            "category",
            field,
        )
        assert schedule["resources"][field] == totals[field], (case, "schedule count", field)
    random_h = sum(n["params"]["bits"] for n in source["inputs"])
    assert (
        random_h
        == source["resources"]["random_hadamards"]
        == categories["uniform_preparation"]["initial_hadamards_separate"]
    )
    words = sum(len(n["out"]) for n in target["nodes"])
    assert words == source["values"] == source["resources"]["ssa_words"]
    retained = (words + len(source["outputs"])) * w
    serial_scratch = max(
        leafs[c["leaf"]]["resources"]["qubits"] - len(c["out"]) * w for c in source["forward_calls"]
    )
    assert source["resources"]["logical_qubits"] == retained + serial_scratch
    dag_depth, levels, critical = independent_dag(source, leafs)
    assert dag_depth == schedule["dependency_only_forward_t_depth"]
    for i in critical:
        categories[call_labels[i]]["one_critical_path_t_depth_contribution"] += leafs[
            source["forward_calls"][i]["leaf"]
        ]["resources"]["t_depth"]
    assert (
        sum(c["one_critical_path_t_depth_contribution"] for c in categories.values()) == dag_depth
    )
    invoked = []
    scheduled_t, scheduled_ct, peak_scratch = 0, 0, 0
    group_checks = []
    previous_wave = 0
    for group_index, group in enumerate(schedule["groups"]):
        indices = group["call_indices"]
        invoked.extend(indices)
        assert group["wave"] >= previous_wave
        previous_wave = group["wave"]
        assert all(levels[i] == group["wave"] for i in indices)
        calls = [source["forward_calls"][i] for i in indices]
        rs = [leafs[c["leaf"]]["resources"] for c in calls]
        scratch = sum(r["qubits"] - len(c["out"]) * w for c, r in zip(calls, rs, strict=True))
        copies = max(Counter(a for c in calls for a in c["args"]).values(), default=0)
        td = max(r["t_depth"] for r in rs)
        ctd = max(r["clifford_t_depth"] for r in rs) + 2 * copies
        assert scratch == group["private_scratch_qubits"] and copies == group["copy_rounds"]
        assert td == group["t_depth"] and ctd == group["clifford_t_depth"]
        assert retained + scratch <= schedule["qubit_cap"]
        scheduled_t += 2 * td
        scheduled_ct += 2 * ctd
        peak_scratch = max(peak_scratch, scratch)
        owner = min(
            indices,
            key=lambda i: (-leafs[source["forward_calls"][i]["leaf"]]["resources"]["t_depth"], i),
        )
        categories[call_labels[owner]]["exclusive_batch_owner_t_depth_diagnostic"] += 2 * td
        operations[target["nodes"][node_indices[owner]]["op"]][
            "exclusive_batch_owner_t_depth_diagnostic"
        ] += 2 * td
        for category in CATEGORIES:
            categories[category]["overlapping_capped_t_depth_diagnostic"] += 2 * max(
                (
                    r["t_depth"]
                    for i, r in zip(indices, rs, strict=True)
                    if call_labels[i] == category
                ),
                default=0,
            )
        group_checks.append(
            {
                "group_index": group_index,
                "wave": group["wave"],
                "calls": len(indices),
                "t_depth": td,
                "scratch_qubits": scratch,
                "dominant_call": owner,
                "dominant_category": call_labels[owner],
            }
        )
    assert sorted(invoked) == list(range(len(source["forward_calls"])))
    assert len(invoked) == len(set(invoked))
    scheduled_ct += output_depth
    assert scheduled_t == schedule["resources"]["t_depth"]
    assert scheduled_ct == schedule["resources"]["clifford_t_depth"]
    assert retained + peak_scratch == schedule["resources"]["logical_qubits"]
    assert peak_scratch == schedule["resources"]["max_reused_scratch_qubits"]
    assert 2 * dag_depth <= scheduled_t
    assert (
        sum(c["exclusive_batch_owner_t_depth_diagnostic"] for c in categories.values())
        == scheduled_t
    )
    comparison = load(ARCHIVE / case / "comparison.json")
    prior_replays = comparison.get("replays", comparison.get("full_replays", []))
    result = {
        "case": case,
        "passed": True,
        "target_nodes": len(target["nodes"]),
        "input_nodes": input_count,
        "non_input_nodes_and_forward_calls": len(node_indices),
        "clean_leaf_invocations": 2 * len(node_indices),
        "normal_roots": normals,
        "correlated_increment_roots": increments,
        "shared_nodes": shared,
        "assignments": assignments,
        "category_costs": {name: dict(categories[name]) for name in CATEGORIES},
        "operation_costs": {op: dict(value) for op, value in sorted(operations.items())},
        "reconciled_counts": totals,
        "copy_ledger": {
            "forward_bind_and_unbind_cx": clean_copies // 2,
            "inverse_bind_and_unbind_cx": clean_copies // 2,
            "clean_argument_cx": clean_copies,
            "output_xor_cx": output_copies,
        },
        "serial_resources_reconciled": {
            **totals,
            **serial_depths,
            "logical_qubits": retained + serial_scratch,
        },
        "capped_resources_reconciled": {
            **totals,
            "t_depth": scheduled_t,
            "clifford_t_depth": scheduled_ct,
            "logical_qubits": retained + peak_scratch,
            "retained_ssa_and_output_qubits": retained,
            "peak_private_scratch_qubits": peak_scratch,
            "qubit_cap": schedule["qubit_cap"],
        },
        "independent_forward_dependency_t_depth": dag_depth,
        "one_critical_path_calls": critical,
        "groups_checked": len(group_checks),
        "group_checks": group_checks,
        "shared_policy": "Cross-category nodes are assigned once to shared; within-category common-subexpression reuse is charged once. Initial uniform H is separate. Output XOR is assigned once to path_payoff.",
        "depth_interpretation": "Overlapping category depths are diagnostics and must not be serially summed. Exclusive batch ownership uses one deterministic maximum-depth call per batch; it is additive bookkeeping, not causal savings. One-DAG-path attribution sums only along that selected path and omits memory/routing constraints.",
        "builder_target_identical": True,
        "stage_a_original_identical": True,
        "prior_replay_field_count": len(prior_replays),
        "new_replays_executed": 0,
    }
    return task, result


def error_ledger(task):
    return {
        "case": f"B{task['assets']}x{task['dates']}",
        "allocations": [
            {
                "epsilon_dollars": e,
                "statistical_reference_allowance_dollars": 0.45 * e,
                "remaining_nonstatistical_dollars": 0.55 * e,
                "certified_total_dollars": None,
                "allocation_is_certificate": False,
            }
            for e in task["output_contract"]["absolute_error_dollars"]
        ],
        "deterministic_terms": [
            {
                "term": term,
                "dollar_bound": None,
                "status": "unresolved",
                "failure_probability": None,
            }
            for term in (
                "finite_uniform_to_continuous_normal_law",
                "Gaussian_log_cos_sqrt_function_and_rounding_error",
                "spot_guard_and_tail_bias",
                "fixed_point_GBM_path_and_Estrin_exponential_error",
                "barrier_boundary_misclassification",
                "rotation_or_phase_synthesis_if_added",
                "estimator_finite_resolution",
            )
        ],
        "failure_terms": [
            {"term": term, "allocated_probability": None, "status": "unresolved"}
            for term in (
                "estimator_statistics_and_stopping",
                "probabilistic_moment_or_reference_certification_if_used",
                "state_preparation_or_synthesis_certification_if_probabilistic",
                "hardware_execution_and_decoding",
            )
        ],
        "allocation_policy": "Before outcome-sensitive work, fix nonnegative dollar allowances with sum <= epsilon and failure shares with sum <= 0.01. Retain 0.45*epsilon as reference statistical share until a valid cost/error grid justifies a prospective replacement. Unknown bounds/shares remain null; none is assumed free. Deterministic proofs consume no stochastic failure share once established. Quantum/classical reference checks retain their own explicit ledgers.",
        "contractual_dates": "Discrete monitoring is part of the payoff. Ideal GBM log transitions are exact at those dates; no deletion or continuous-monitoring substitution is authorized.",
        "non_applicable_terms": "Compound baseline, surrogate and exercise-policy regret terms do not belong to this plain knock-out source family.",
        "gates": {
            "G2": "unresolved",
            "G3": "unresolved",
            "G4": "unresolved_actual_target_time_to_accuracy",
            "G5": "unresolved_physical_mapping_and_complete_latency",
        },
    }


def receipt_manifest(folder, external):
    data = {
        str(p.relative_to(ROOT)).replace("\\", "/"): sha(p)
        for p in sorted(folder.rglob("*"))
        if p.is_file() and p.name != "manifest.json"
    }
    dump(
        folder / "manifest.json",
        {"files": data, "frozen_inputs": external, "manifest_self_hash_excluded": True},
    )


def run(program_root, g0_name="G0_run001", a01_name="A01_run001"):
    g0, a01 = program_root / g0_name, program_root / a01_name
    assert not g0.exists() and not a01.exists(), "Fresh run roots required"
    doc = ROOT / "docs/limitation_program_20261001/BASELINE.md"
    assert not doc.exists(), "Refuse to overwrite the baseline report"
    program_root.mkdir(parents=True, exist_ok=True)
    g0.mkdir()
    a01.mkdir()
    inputs = {}
    for case in ("B4x12", "B8x52"):
        for name in ("target.json", "source.json", "schedule_capped.json", "input_proofs.json"):
            path = ARCHIVE / case / "signed-digit-carry-save" / name
            inputs[str(path.relative_to(ROOT)).replace("\\", "/")] = sha(path)
    for name in ("verification.json", "summary.json", "protocol.json"):
        path = ARCHIVE / name
        inputs[str(path.relative_to(ROOT)).replace("\\", "/")] = sha(path)
    created = datetime.now(timezone.utc).isoformat()
    protocol = {
        "created_utc": created,
        "scope": "G0/C01-C03/C13 for current B4/B8 arithmetic, plus A01 accounting only",
        "source_family": "B4x12 and B8x52 plain discretely monitored GBM arithmetic-Asian equal-weight basket knock-out Y; not C4/H8 residual, Heston or compound estimators",
        "accepted_strategy": "signed-digit-carry-save ln(2), exact variable carry-save and exact shared-prefix lookup",
        "fixed_inputs": inputs,
        "producer_sha256": sha(Path(__file__)),
        "local_only": True,
        "preparation_reads": "Repository task/specification and accepted archives were inspected to design this analysis. Protocols are saved before the new graph reconstruction, categorization and independent count derivation; this is not retrospective preregistration of earlier experiments.",
        "exclusions": "No new gate replay, pricing acquisition, Stage C edit, estimator fit, package installation, push, external service or physical-time claim.",
        "success": "Recover the exact task from the archived builder/targets; verify immutable hashes; create nonzero-filled error/failure ledgers; exactly reconcile every node, call, gate/copy count, DAG depth and capped batch resource.",
        "stop": "One analysis per case. Any identity/hash/count/binding mismatch aborts acceptance and leaves the prior accepted source unchanged.",
    }
    dump(g0 / "protocol.json", protocol)
    dump(
        a01 / "protocol.json",
        {
            **protocol,
            "classification": "Uniform inputs separately; scalar-normal ancestor closures, correlation-to-GBM-increment closures stopping at normal roots, path/payoff closure stopping at correlation/normal roots; intersections assigned once to shared.",
            "independent_checks": "Scan X/CX/CCX gate arrays and seven-T expansion; reconstruct source copy counts, serial costs, Kahn DAG and every capped batch from leaf weights.",
        },
    )
    env = environment()
    dump(g0 / "environment.json", env)
    cache, tasks, results = {}, [], []
    for case, assets, dates in (("B4x12", 4, 12), ("B8x52", 8, 52)):
        task, result = analyze_case(case, assets, dates, cache, inputs)
        tasks.append(task)
        results.append(result)
        dump(g0 / (case + "_task.json"), task)
        dump(g0 / (case + "_error_ledger.json"), error_ledger(task))
        dump(a01 / (case + "_accounting.json"), result)
        print(
            case,
            "PASS",
            result["non_input_nodes_and_forward_calls"],
            "calls; T-depth",
            result["capped_resources_reconciled"]["t_depth"],
            flush=True,
        )
    prior = load(ARCHIVE / "verification.json")
    assert prior["artifact_checks_passed"]
    assert [c["case"] for c in prior["cases"]] == ["B4x12", "B8x52"]
    assert all(inputs[p] == sha(ROOT / p) for p in inputs)
    baseline = [
        {
            "case": r["case"],
            "source_directory": str(
                (ARCHIVE / r["case"] / "signed-digit-carry-save").relative_to(ROOT)
            ).replace("\\", "/"),
            "resources": r["capped_resources_reconciled"],
            "category_costs": r["category_costs"],
            "task_sha256": sha(g0 / (r["case"] + "_task.json")),
        }
        for r in results
    ]
    summary = {
        "passed": True,
        "decision": "completed_audit",
        "cases": baseline,
        "G0": "passed_for_current_B4_B8_arithmetic",
        "G1": "prior_accepted_exact_arithmetic_receipts_plus_new_accounting_only",
        "G2": "unresolved",
        "G3": "unresolved",
        "G4": "unresolved",
        "G5": "unresolved",
        "unique_leaves_scanned_and_hash_checked": len(cache),
        "new_scientific_or_gate_replays": 0,
        "scope": "One consistent arithmetic baseline; no quantum runtime or advantage claim",
    }
    dump(g0 / "summary.json", summary)
    dump(g0 / "result.json", summary)
    dump(a01 / "summary.json", summary)
    dump(
        a01 / "result.json",
        {
            "passed": True,
            "decision": "completed_audit",
            "cases": [
                {
                    k: r[k]
                    for k in (
                        "case",
                        "target_nodes",
                        "input_nodes",
                        "non_input_nodes_and_forward_calls",
                        "clean_leaf_invocations",
                        "reconciled_counts",
                        "copy_ledger",
                        "independent_forward_dependency_t_depth",
                        "groups_checked",
                    )
                }
                for r in results
            ],
        },
    )
    command = (
        ".context/frontier_t0_env/Scripts/python.exe -m "
        "research.limitation_program_20261001.baseline --output "
        f"results/limitation_program_20261001 --g0-run {g0_name} --a01-run {a01_name}"
    )
    verification = {
        "passed": True,
        "command": command,
        "producer_sha256": sha(Path(__file__)),
        "environment_sha256": sha(g0 / "environment.json"),
        "checks": [
            "Current optimized builder equals each accepted target",
            "Current original builder equals each Stage A original target",
            "Every used leaf gate hash and actual X/CX/CCX expansion matches metadata",
            "Every non-input node and call assigned once",
            "All count totals and copy costs reconcile",
            "Independent Kahn DAG matches archived dependency depth",
            "Every capped group/copy/scratch/depth checked",
            "Input, code and leaf hashes unchanged after analysis",
        ],
        "prior_replays": {"B4x12": 3, "B8x52": 1},
        "new_replays": 0,
        "prior_replay_source": "results/limitation_audit_20261001/constant_multiplier_v1/verification.json",
        "qualification": "Existing sampled full-source replays are reused, not claimed newly run or exhaustive. G2-G5 remain open.",
    }
    dump(g0 / "verification.json", verification)
    dump(a01 / "verification.json", verification)
    next_text = "# Next local action\n\nThe task and reconciled B4/B8 arithmetic baseline are frozen. Combine compact SSA allocation with the accepted carry-save/ln(2) leaves and capped parallel schedule (A06/H15/C13), preserving target hashes and using the original caps. Validate bindings, signed values, arbitrary output XOR and cleanup before adoption. A01 category and operation ledgers then rank subsequent leaf trials. Do not use C4/H8 estimator counts for these B4/B8 sources. G2 price error, G3 estimator, G4 actual matched time-to-accuracy and G5 physical mapping remain unresolved. Failed exact candidates retain this accepted baseline. All work remains local.\n"
    for folder in (g0, a01):
        with (folder / "NEXT.md").open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(next_text)
    doc.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Frozen B4/B8 task and reconciled arithmetic baseline\n\n",
        "Local execution, 1 October 2026. G0/C01-C03/C13 and A01 are completed for the current knock-out arithmetic sources. Their gate/price/error scopes remain separate; no new scientific pricing or gate replay was performed. Every current target was rebuilt from the original financial builder and exact optimizer and matched both the accepted target and Stage A original graph.\n\n",
        "The payoff is one unit of the equal-weight basket Asian call: exp(-0.03)*max(mean of all asset/date spots-100,0), paid only when every monitored equal-weight basket is strictly below 140. Each asset starts at 100, volatility is 0.30, equity correlation is 0.40, maturity is one year and observations are equally spaced. Barrier equality knocks out. The initial basket is $100; output is already discounted dollars, with no extra notional multiplier. B4 uses 4 assets/12 dates; B8 uses 8 assets/52 dates.\n\n",
        "The digital source uses 32-bit midpoint uniforms, the existing paired Box-Muller arithmetic, f=40/72-bit words, clipped log spots in [log(2^-16),log(4096)], degree-12 Estrin exponentials and signed modular integer semantics. These choices define the accepted digital function; their continuous-price effects remain unproved. Output Y is interpreted as signed integer/2^40.\n\n",
        "The unchanged tolerance grid is $0.10, $0.03, $0.01 and the B4/B8 final $0.001 test, with at least 99% per-price confidence and complete latency at most one tenth the fastest eligible complete classical time. The historical 0.45*epsilon statistical share is a planning reference. Every missing error bound and failure allocation is null, not zero; G2-G5 remain unresolved.\n\n",
        "| Case | Nodes / forward calls | T gates | Capped T-depth | Clifford+T depth | Logical qubits | Separate uniform H |\n|---|---:|---:|---:|---:|---:|---:|\n",
    ]
    for r in results:
        q = r["capped_resources_reconciled"]
        lines.append(
            f"| {r['case']} | {r['target_nodes']:,} / {r['non_input_nodes_and_forward_calls']:,} | {q['t_count']:,} | {q['t_depth']:,} | {q['clifford_t_depth']:,} | {q['logical_qubits']:,} | {r['category_costs']['uniform_preparation']['initial_hadamards_separate']:,} |\n"
        )
    lines.append(
        "\nEach target node and forward invocation is attributed exactly once. Uniform inputs have no arithmetic leaf. Scalar-normal ancestors stop at inputs; correlation includes the scaled common/idiosyncratic combination and deterministic log-increment drift; path/payoff begins after those increments. Cross-stage shared constants/nodes have an explicit shared bucket. Output XOR is charged once to path/payoff.\n\n"
    )
    for r in results:
        lines.append(
            f"## {r['case']} attribution\n\n| Category | Nodes | Forward calls | Clean T gates | Argument-copy CX | Overlapping capped T-depth diagnostic |\n|---|---:|---:|---:|---:|---:|\n"
        )
        for category in CATEGORIES:
            c = r["category_costs"][category]
            lines.append(
                f"| {category} | {c.get('target_nodes', 0):,} | {c.get('forward_calls', 0):,} | {c.get('t_count', 0):,} | {c.get('argument_copy_cx_clean', 0):,} | {c.get('overlapping_capped_t_depth_diagnostic', 0):,} |\n"
            )
        work = sorted(
            r["operation_costs"].items(), key=lambda item: (-item[1]["clean_t_count"], item[0])
        )[:3]
        depth = sorted(
            r["operation_costs"].items(),
            key=lambda item: (-item[1].get("exclusive_batch_owner_t_depth_diagnostic", 0), item[0]),
        )[:3]
        lines.append(
            "\nTop three work operations: "
            + ", ".join(f"{op} ({c['clean_t_count']:,} T)" for op, c in work)
            + ". Top three deterministic batch-owner depth operations: "
            + ", ".join(
                f"{op} ({c.get('exclusive_batch_owner_t_depth_diagnostic', 0):,} layers attributed)"
                for op, c in depth
            )
            + ".\n\n"
        )
        lines.append(
            f"Independent forward weighted-DAG T-depth is {r['independent_forward_dependency_t_depth']:,}; all {r['groups_checked']:,} capped batches and their scratch/copy costs reconcile. Clean argument-copy CX count is {r['copy_ledger']['clean_argument_cx']:,}; output XOR adds {r['copy_ledger']['output_xor_cx']} CX.\n\n"
        )
    lines.append(
        "Category depths overlap within parallel batches and must not be summed as serial elapsed time or multiplied into separate speedup factors. Deterministic batch ownership sums to the complete scheduled depth but is attribution only: tied or hidden leaf costs can become dominant after a change. The independent DAG bound concerns this fixed leaf decomposition, with no routing/factory model; it is not a lower bound on all implementations.\n\n"
    )
    lines.append(
        f"Actual immutable gate arrays for {len(cache)} unique leaves were scanned for X/CX/CCX counts and hashed. Reconstructed counts reproduce all seven source count fields, exact seven-T/six-CX/two-H CCX expansion, serial depths, both capped depths, qubits and copy costs. Prior evidence contains three B4 and one B8 sampled full-source replays; none was repeated here. The environment is the existing pinned local Python, not a new installation.\n\n"
    )
    lines.append(
        f"Receipts: [G0 summary](../../results/limitation_program_20261001/{g0_name}/summary.json), [frozen tasks/error ledgers](../../results/limitation_program_20261001/{g0_name}/), [A01 accounting](../../results/limitation_program_20261001/{a01_name}/), and [producer](../../research/limitation_program_20261001/baseline.py). Each run has a prospective protocol, verification, next action and manifest.\n\n"
    )
    lines.append(
        "Next: combine exact compact SSA storage with the accepted parallel leaf library under the unchanged caps. Recompute these ledgers after any adoption and then screen the dominant remaining arithmetic. Price certification, an estimator for this source, matched actual classical target timings and a compatible physical mapping are separate unfinished gates. Nothing was pushed, uploaded or published.\n"
    )
    with doc.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write("".join(lines))
    frozen = {
        **inputs,
        **env["code_sha256"],
        str(doc.relative_to(ROOT)).replace("\\", "/"): sha(doc),
    }
    receipt_manifest(g0, frozen)
    receipt_manifest(a01, frozen)
    for folder in (g0, a01):
        manifest = load(folder / "manifest.json")
        assert all(sha(ROOT / p) == value for p, value in manifest["files"].items())
        assert all(sha(ROOT / p) == value for p, value in manifest["frozen_inputs"].items())
    print("G0 and A01 completed audits; manifests verified; G2-G5 unresolved.", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--g0-run", default="G0_run001")
    parser.add_argument("--a01-run", default="A01_run001")
    args = parser.parse_args()
    run(args.output.resolve(), args.g0_run, args.a01_run)
