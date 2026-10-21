"""Independent allocation, original graph and actual-array audit for A18."""

from __future__ import annotations

# Exact audit scope text is a receipt field.
# ruff: noqa: E501

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET

import numpy as np
from numba import njit

from research.controlled_priority_completion.parallel_source import entries
from research.controlled_source_completion.compiler import resolve_library
from research.controlled_source_completion.ir import evaluate
from research.limitation_program_20261001.compact_ledger import active_bit_certificate
from research.limitation_program_20261001.constant_library import digest
from research.limitation_program_20261001.progress import ROOT


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path, data):
    path.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n", encoding="utf-8")


@njit(cache=True)
def scan(gates, qubits, inverse):
    """Fresh gate parse and literal seven-T expansion, independent of emitter."""
    t = np.zeros(qubits, np.int64)
    d = np.zeros(qubits, np.int64)
    counts = np.zeros(3, np.int64)
    for index in range(len(gates)):
        kind, a, b, c = gates[len(gates) - 1 - index if inverse else index]
        assert 1 <= kind <= 3 and 0 <= a < qubits
        counts[kind - 1] += 1
        if kind == 1:
            d[a] += 1
        elif kind == 2:
            assert 0 <= b < qubits and a != b
            level = max(t[a], t[b])
            depth = max(d[a], d[b]) + 1
            t[a] = t[b] = level
            d[a] = d[b] = depth
        else:
            assert 0 <= b < qubits and 0 <= c < qubits
            assert a != b and a != c and b != c
            # H,CX,Tdag,CX,T,CX,Tdag,CX,T,T,H,CX,T,Tdag,CX.
            operations = (
                (c, c, 0),
                (b, c, 0),
                (c, c, 1),
                (a, c, 0),
                (c, c, 1),
                (b, c, 0),
                (c, c, 1),
                (a, c, 0),
                (b, b, 1),
                (c, c, 1),
                (c, c, 0),
                (a, b, 0),
                (a, a, 1),
                (b, b, 1),
                (a, b, 0),
            )
            for x, y, is_t in operations:
                level = max(t[x], t[y]) + is_t
                depth = max(d[x], d[y]) + 1
                t[x] = t[y] = level
                d[x] = d[y] = depth
    return counts, t.max(), d.max()


def costs(gates, q, inverse):
    counts, td, depth = scan(gates, q, inverse)
    x, cx, ccx = map(int, counts)
    return dict(
        source_gates=len(gates),
        x=x,
        cx=cx,
        ccx=ccx,
        t_count=7 * ccx,
        clifford_cx=cx + 6 * ccx,
        clifford_h=2 * ccx,
        t_depth=int(td),
        clifford_t_depth=int(depth),
    )


def audit_schedule(scope, circuit, library_costs):
    fingerprint = hashlib.sha256(json.dumps(scope, sort_keys=True).encode("utf-8")).hexdigest()
    assert circuit["scope_fingerprint"] == fingerprint
    assert circuit["source_fingerprint"] == scope["source_fingerprint"]
    assert circuit["target_fingerprint"] == scope["target_fingerprint"]
    groups = {g["id"]: g for g in scope["groups"]}
    outputs = {o["name"]: o for o in scope["outputs"]}
    floor, cap = scope["fixed_floor"], circuit["cap"]
    live, copied, total = {}, Counter(), Counter()
    maximum, high, peak_private, argument_cx, output_cx, copy_depth = floor, floor, 0, 0, 0, 0

    def intervals(spans, expected):
        assert sum(s["width"] for s in spans) == expected
        result = []
        for s in spans:
            assert type(s["offset"]) is int and type(s["width"]) is int
            low, size = s["offset"], s["width"]
            assert size > 0 and floor <= low < low + size <= cap
            result.append((low, low + size))
        return result

    for event in circuit["events"]:
        kind = event["kind"]
        if kind == "copy_output":
            name, value = event["outputname"], event["value"]
            assert name in outputs and outputs[name]["value"] == value
            assert outputs[name]["group"] in live and copied[name] == 0
            copied[name] += 1
            width = scope["widths"][value]
            assert event["copy_cx"] == width and event["copy_depth"] == 1
            output_cx += width
            for field in ("source_gates", "cx", "clifford_cx"):
                total[field] += width
            total["clifford_t_depth"] += 1
            continue
        assert kind in ("compute", "erase")
        g = groups[event["group"]]
        assert set(g["preds"]) <= set(live)
        allocation = intervals(event["storage"], g["width"])
        private = intervals(event["private_storage"], g["private"])
        if kind == "compute":
            assert g["id"] not in live
            live[g["id"]] = allocation
        else:
            assert g["id"] in live and allocation == live[g["id"]]
        all_intervals = [interval for spans in live.values() for interval in spans] + private
        ordered = sorted(all_intervals)
        assert all(left[1] <= right[0] for left, right in zip(ordered, ordered[1:]))
        maximum = max(maximum, floor + sum(b - a for a, b in ordered))
        high = max(high, *(b for _, b in ordered))
        peak_private = max(peak_private, g["private"])
        cost = library_costs[g["leaf"]][kind]
        assert event["native_cost"] == cost and event["literal_inverse"] == (kind == "erase")
        total.update(cost)
        copied_cx = 2 * sum(scope["widths"][v] for v in g["args"])
        depth = 2 * max(Counter(g["args"]).values(), default=0)
        assert event["argument_copy_cx"] == copied_cx and event["argument_copy_depth"] == depth
        for field in ("source_gates", "cx", "clifford_cx"):
            total[field] += copied_cx
        total["clifford_t_depth"] += depth
        argument_cx += copied_cx
        copy_depth += depth
        if kind == "erase":
            del live[g["id"]]
    assert not live and set(copied) == set(outputs)
    r = circuit["resources"]
    assert all(r[k] == v for k, v in total.items())
    assert r["peak_live_qubits"] == maximum and r["logical_qubits"] == high <= cap
    assert r["max_reused_scratch_qubits"] == peak_private
    assert circuit["argument_copy_cx"] == argument_cx and circuit["output_copy_cx"] == output_cx
    assert circuit["argument_copy_depth"] == copy_depth
    assert circuit["argument_and_output_copy_cx"] == argument_cx + output_cx
    assert circuit["native_leaf_costs"] == library_costs
    return dict(
        resources=r, emitted_leaf_calls=sum(e["kind"] != "copy_output" for e in circuit["events"])
    )


def run(producer, output):
    assert not output.exists()
    summary, scope, protocol = (
        read(producer / name) for name in ("summary.json", "subgraph.json", "protocol.json")
    )
    assert summary["passed"]
    frozen = {}
    for path, expected in read(producer / "manifest.json")["files"].items():
        assert digest(ROOT / path) == expected
        frozen[path] = expected
    for path, expected in protocol["frozen_inputs"].items():
        assert digest(ROOT / path) == expected
        frozen[path] = expected
    frozen[(producer / "manifest.json").relative_to(ROOT).as_posix()] = digest(
        producer / "manifest.json"
    )
    own = Path(__file__)
    frozen[own.relative_to(ROOT).as_posix()] = digest(own)
    output.mkdir()
    shutil.copy2(own, output / "executed_reconcile_checkpoint_v2.py")
    save(
        output / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            local_only=True,
            before_analysis=True,
            independent_of_emitter_and_scheduler=True,
            frozen_inputs=frozen,
            scope="Original closure, outside edges, atomic groups, fresh actual-gate forward/inverse scan, physical allocations, all copy and cost charges, nondominance, saved real trace replays",
        ),
    )
    baseline = ROOT / protocol["baseline"]
    source, target = (read(baseline / name) for name in ("source.json", "target.json"))
    metadata, archive = entries(source), resolve_library(source)
    masks = active_bit_certificate(target)
    widths = [max(1, masks[v].bit_length()) for v in range(source["values"])]
    assert scope["widths"] == widths
    root = scope["selection"]["stock_value"]
    nodes = target["nodes"]
    owners = {v: i for i, n in enumerate(nodes) for v in n["out"]}
    closure, stack = set(), [root]
    while stack:
        i = owners[stack.pop()]
        if nodes[i]["op"] == "input" or i in closure:
            continue
        closure.add(i)
        stack.extend(nodes[i]["args"])
    assert sorted(closure) == scope["selected_node_indices"]
    selected_values = {v for i in closure for v in nodes[i]["out"]}
    boundary = {
        v
        for i, n in enumerate(nodes)
        if i not in closure
        for v in n["args"]
        if v in selected_values
    } | {root}
    boundary |= set(source["outputs"].values()) & selected_values
    assert sorted(boundary) == scope["protected_boundary_values"]
    assert len(scope["inputs"]) == len(source["inputs"]) == 60
    assert sum(n["width"] for n in scope["inputs"]) == 1920
    assert scope["fixed_floor"] == 1920 + 72 * len(scope["outputs"])
    noninputs = [i for i, n in enumerate(nodes) if n["op"] != "input"]
    group_for_value = {v: g["id"] for g in scope["groups"] for v in g["out"]}
    for g in scope["groups"]:
        call = source["forward_calls"][g["call_index"]]
        assert noninputs[g["call_index"]] == g["node_index"] in closure
        assert all(g[f] == call[f] for f in ("leaf", "args", "out"))
        assert g["out_widths"] == [widths[v] for v in call["out"]]
        assert g["width"] == sum(g["out_widths"])
        assert g["private"] + g["width"] == metadata[g["leaf"]]["resources"]["qubits"]
        assert set(g["preds"]) == {group_for_value[a] for a in g["args"] if a in group_for_value}
    costs_by_leaf = {}
    actual_gate_hashes = {}
    for key in sorted({g["leaf"] for g in scope["groups"]}):
        entry = metadata[key]
        path = archive / entry["gate_file"]
        assert digest(path) == entry["sha256"]
        actual_gate_hashes[key] = digest(path)
        gates = np.load(path, mmap_mode="r")
        c = {
            kind: costs(gates, entry["resources"]["qubits"], kind == "erase")
            for kind in ("compute", "erase")
        }
        assert all(entry["resources"][k] == v for k, v in c["compute"].items())
        costs_by_leaf[key] = c
        print("A18 audit actual array", key, flush=True)
    control = read(producer / "retain_all_schedule.json")
    assert control["native_gate_sha256"] == actual_gate_hashes
    audited = {"retain-all": audit_schedule(scope, control, costs_by_leaf)}
    minimum = max(
        scope["fixed_floor"]
        + g["private"]
        + g["width"]
        + sum(next(p["width"] for p in scope["groups"] if p["id"] == pred) for pred in g["preds"])
        for g in scope["groups"]
    )
    assert minimum == scope["minimum_move_qubits"]
    assert scope["baseline_workspace"] == sum(g["width"] for g in scope["groups"]) + max(
        g["private"] for g in scope["groups"]
    )
    for percent in (75, 50):
        assert (
            scope["caps"][str(percent)]
            == scope["fixed_floor"] + percent * scope["baseline_workspace"] // 100
        )
    replay_count = 0
    for row in summary["attempts"]:
        assert row["cap"] == scope["caps"][str(row["workspace_percent"])]
        plan = read(producer / row["name"] / "plan.json")
        assert plan["cap"] == row["cap"]
        if not row["feasible"]:
            assert not plan["moves"]
            if plan.get("infeasible_proved"):
                assert row["cap"] < minimum
            continue
        circuit = read(producer / row["name"] / "schedule.json")
        assert circuit["cap"] == row["cap"]
        assert circuit["native_gate_sha256"] == actual_gate_hashes
        assert row["resources"] == circuit["resources"]
        audited[row["name"]] = audit_schedule(scope, circuit, costs_by_leaf)
        for replay, sample in zip(row["replays"], protocol["replay_vectors"]):
            assert replay["inputs"] == sample["inputs"] and replay["label"] == sample["label"]
            _, trace = evaluate(target, sample["inputs"], True)
            expected = {
                o["name"]: trace[o["value"]] ^ protocol["dirty_output"] for o in scope["outputs"]
            }
            assert replay["expected"] == replay["actual"]["values"] == expected and replay["passed"]
            assert replay["actual"]["all_input_and_workspace_bits_restored"]
            assert replay["actual"]["original_trace_values_checked"] > 0
            replay_count += 1
    dimensions = ("logical_qubits", "t_count", "t_depth", "clifford_t_depth")
    alternatives = [control["resources"]] + [
        r["resources"] for r in summary["attempts"] if r["feasible"]
    ]
    frontier = []
    for row in summary["attempts"]:
        if row["feasible"]:
            r = row["resources"]
            nondominated = not any(
                all(a[d] <= r[d] for d in dimensions) and any(a[d] < r[d] for d in dimensions)
                for a in alternatives
            )
            assert row["nondominated"] == nondominated
            if nondominated and r["logical_qubits"] < control["resources"]["logical_qubits"]:
                assert len(row["replays"]) == 3
                frontier.append(row["name"])
    assert frontier == summary["retained_workspace_frontier"]
    assert replay_count == summary["new_extracted_subgraph_gate_replays"]
    xml = ET.parse(producer / "tests.xml").getroot()
    suites = list(xml) if xml.tag != "testsuite" else [xml]
    assert all(
        int(s.get(field, 0)) == 0 for s in suites for field in ("failures", "errors", "skipped")
    )
    names = {(c.get("classname"), c.get("name")) for s in suites for c in s.findall("testcase")}
    assert len(names) == sum(int(s.get("tests", 0)) for s in suites)
    result = dict(
        passed=True,
        local_only=True,
        actual_unique_gate_arrays_scanned=len(costs_by_leaf),
        original_atomic_groups=len(scope["groups"]),
        protected_outputs=len(scope["outputs"]),
        minimum_move_qubits=minimum,
        new_distinct_pytest_cases=len(names),
        producer_extracted_gate_replays=replay_count,
        new_audit_gate_replays=0,
        retained_workspace_frontier=frontier,
        audited_schedules=audited,
        G2_to_G5="open",
    )
    save(output / "summary.json", result)
    assert all(digest(ROOT / p) == expected for p, expected in frozen.items())
    save(
        output / "manifest.json",
        dict(
            files={
                p.relative_to(ROOT).as_posix(): digest(p) for p in output.rglob("*") if p.is_file()
            },
            frozen_inputs=frozen,
        ),
    )
    print("A18 independent audit PASS", len(costs_by_leaf), "arrays", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--producer", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.producer.resolve(), args.output.resolve())
