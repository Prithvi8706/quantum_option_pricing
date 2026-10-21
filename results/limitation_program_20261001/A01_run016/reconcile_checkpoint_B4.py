"""Independent complete B4 allocation and actual-array reconciliation for A18."""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET

import numpy as np

from research.controlled_priority_completion.parallel_source import entries
from research.controlled_source_completion.compiler import resolve_library
from research.controlled_source_completion.ir import evaluate
from research.limitation_program_20261001.constant_library import digest
from research.limitation_program_20261001.experiment_checkpoint import (
    CASE,
    DIMENSIONS,
    PROGRAM,
    dominated,
    read,
    relative,
    save,
)
from research.limitation_program_20261001.progress import ROOT
from research.limitation_program_20261001.reconcile_checkpoint_v2 import costs


def fingerprint(data):
    import json

    return hashlib.sha256(json.dumps(data, sort_keys=True).encode("utf-8")).hexdigest()


def analyze(target, source, scope, subroutine, full, actual_costs, actual_hashes):
    assert full["source_fingerprint"] == fingerprint(source)
    assert full["target_fingerprint"] == fingerprint(target)
    assert full["scope_fingerprint"] == fingerprint(scope)
    assert full["subroutine_fingerprint"] == fingerprint(subroutine)
    widths, w = scope["widths"], source["word_width"]
    chosen = set(scope["selected_call_indices"])
    outside = [(i, c) for i, c in enumerate(source["forward_calls"]) if i not in chosen]
    total = Counter(
        {
            k: 2 * subroutine["resources"][k]
            for k in (
                "source_gates",
                "x",
                "cx",
                "ccx",
                "t_count",
                "clifford_cx",
                "clifford_h",
                "t_depth",
                "clifford_t_depth",
            )
        }
    )
    cursor = scope["fixed_floor"]
    expected_outputs = []
    for name, value in source["outputs"].items():
        expected_outputs.append(dict(name=name, value=value, offset=cursor, width=w))
        cursor += w
    assert full["named_outputs"] == expected_outputs
    fixed = cursor
    expected_allocations, maximum_private, argcopies, argdepth = [], 0, 0, 0
    selected_values = set(scope["selected_value_ids"])
    boundary_values = {o["value"] for o in scope["outputs"]}
    live = {i["id"] for i in scope["inputs"]} | boundary_values
    for index, call in outside:
        assert set(call["args"]) <= live
        assert not set(call["out"]) & live
        assert not (set(call["args"]) & selected_values) - boundary_values
        bindings = []
        for value in call["out"]:
            bindings.append(dict(value=value, offset=cursor, width=widths[value]))
            cursor += widths[value]
        nativeq = actual_costs[call["leaf"]]["qubits"]
        private = nativeq - sum(widths[v] for v in call["out"])
        maximum_private = max(maximum_private, private)
        expected_allocations.append(
            dict(
                call_index=index,
                leaf=call["leaf"],
                args=call["args"],
                out=call["out"],
                output_bindings=bindings,
                private=private,
            )
        )
        for kind in ("compute", "erase"):
            total.update(actual_costs[call["leaf"]][kind])
        cx = 4 * sum(widths[v] for v in call["args"])
        depth = 4 * max(Counter(call["args"]).values(), default=0)
        for field in ("source_gates", "cx", "clifford_cx"):
            total[field] += cx
        total["clifford_t_depth"] += depth
        argcopies += cx
        argdepth += depth
        live.update(call["out"])
    assert full["outside_allocations"] == expected_allocations
    assert set(source["outputs"].values()) <= live
    output_cx = sum(widths[v] for v in source["outputs"].values())
    for field in ("source_gates", "cx", "clifford_cx"):
        total[field] += output_cx
    total["clifford_t_depth"] += len(source["outputs"])
    dynamic = subroutine["resources"]["logical_qubits"] - scope["fixed_floor"]
    bank = max(dynamic, maximum_private)
    resources = full["resources"]
    assert all(resources[k] == v for k, v in total.items())
    assert full["private_base"] == cursor and full["private_width"] == bank
    assert full["subroutine_dynamic_base"] == cursor
    assert resources["logical_qubits"] == resources["peak_live_qubits"] == cursor + bank
    assert resources["fixed_floor_qubits"] == fixed
    assert resources["retained_outside_ssa_qubits"] == cursor - fixed
    assert resources["max_reused_scratch_qubits"] == bank
    assert resources["extracted_transient_workspace_qubits"] == dynamic
    assert resources["outside_private_leaf_workspace_qubits"] == maximum_private
    assert resources["random_hadamards"] == 1920
    outside_keys = {c["leaf"] for _, c in outside}
    expected_costs = {
        key: {kind: actual_costs[key][kind] for kind in ("compute", "erase")}
        for key in outside_keys
    }
    assert full["native_leaf_costs"] == expected_costs
    assert full["native_gate_sha256"] == {k: actual_hashes[k] for k in outside_keys}
    assert full["external_forward_calls"] == len(outside)
    assert full["subroutine_invocations"] == 2
    assert full["copy_ledger"] == dict(
        subroutine_all_copies_cx=2 * subroutine["argument_and_output_copy_cx"],
        outside_argument_copies_cx=argcopies,
        outside_argument_copy_depth=argdepth,
        full_named_output_copy_cx=output_cx,
    )
    return resources


def run(producer, output):
    assert not output.exists()
    result, protocol = read(producer / "summary.json"), read(producer / "protocol.json")
    assert result["passed"]
    frozen = dict(protocol["frozen_inputs"])
    frozen.update(read(producer / "manifest.json")["files"])
    frozen[relative(producer / "manifest.json")] = digest(producer / "manifest.json")
    own = Path(__file__)
    frozen[relative(own)] = digest(own)
    assert all(digest(ROOT / path) == expected for path, expected in frozen.items())
    output.mkdir()
    shutil.copy2(own, output / own.name)
    save(
        output / "protocol.json",
        dict(
            local_only=True,
            created_utc=datetime.now(timezone.utc).isoformat(),
            before_analysis=True,
            frozen_inputs=frozen,
            independent_of_B4_generator=True,
        ),
    )
    target, source = (read(CASE / name) for name in ("target.json", "source.json"))
    subroot = PROGRAM / "A18_run001"
    scope = read(subroot / "subgraph.json")
    sub = read(subroot / protocol["selected"] / "schedule.json")
    controlsub = read(subroot / "retain_all_schedule.json")
    library = resolve_library(source)
    actual, hashes = {}, {}
    for key, entry in entries(source).items():
        path = library / entry["gate_file"]
        assert digest(path) == entry["sha256"]
        hashes[key] = digest(path)
        gates = np.load(path, mmap_mode="r")
        actual[key] = dict(qubits=entry["resources"]["qubits"])
        for direction in ("compute", "erase"):
            actual[key][direction] = costs(gates, actual[key]["qubits"], direction == "erase")
        assert all(entry["resources"][k] == v for k, v in actual[key]["compute"].items())
    candidate = read(producer / "schedule.json")
    control = read(producer / "matched_retain_all_schedule.json")
    cr = analyze(target, source, scope, sub, candidate, actual, hashes)
    br = analyze(target, source, scope, controlsub, control, actual, hashes)
    original = read(CASE / "schedule_capped.json")["resources"]
    assert cr == result["candidate_resources"] and br == result["matched_retain_all_resources"]
    assert result["preferred_latency_resources"] == original
    assert result["width_saving_versus_matched_control"] == (
        cr["logical_qubits"] < br["logical_qubits"]
    )
    assert result["nondominated"] == (not dominated(cr, [br, original]))
    assert result["retained_workspace_point"] == (
        cr["logical_qubits"] < br["logical_qubits"] and not dominated(cr, [br, original])
    )
    assert result["checkpoint_global_qubits_saved"] == br["logical_qubits"] - cr["logical_qubits"]
    assert len(result["replays"]) == (3 if result["retained_workspace_point"] else 0)
    for replay, sample in zip(result["replays"], protocol["replay_vectors"]):
        assert replay["label"] == sample["label"] and replay["inputs"] == sample["inputs"]
        _, trace = evaluate(target, sample["inputs"], True)
        expected = {
            name: trace[value] ^ protocol["dirty_output"]
            for name, value in source["outputs"].items()
        }
        assert replay["actual"]["values"] == replay["expected"] == expected
        assert replay["passed"] and replay["actual"]["all_input_and_workspace_bits_restored"]
        assert replay["actual"]["original_trace_values_checked"] > source["values"] - len(
            source["inputs"]
        )
    xml = ET.parse(producer / "tests.xml").getroot()
    suites = list(xml) if xml.tag != "testsuite" else [xml]
    assert all(
        int(s.get(field, 0)) == 0 for s in suites for field in ("failures", "errors", "skipped")
    )
    names = {(c.get("classname"), c.get("name")) for s in suites for c in s.findall("testcase")}
    assert len(names) == sum(int(s.get("tests", 0)) for s in suites)
    summary = dict(
        passed=True,
        local_only=True,
        actual_unique_gate_arrays_scanned=len(actual),
        original_outside_calls=len(candidate["outside_allocations"]),
        candidate_resources=cr,
        matched_control_resources=br,
        checkpoint_qubits_saved=br["logical_qubits"] - cr["logical_qubits"],
        retained_workspace_point=result["retained_workspace_point"],
        new_distinct_tests=len(names),
        producer_financial_replays=len(result["replays"]),
        new_audit_gate_replays=0,
        preferred_latency_source_unchanged=True,
        G2_to_G5="open",
        selection_dimensions=list(DIMENSIONS),
    )
    save(output / "summary.json", summary)
    assert all(digest(ROOT / path) == expected for path, expected in frozen.items())
    save(
        output / "manifest.json",
        dict(
            files={relative(p): digest(p) for p in output.rglob("*") if p.is_file()},
            frozen_inputs=frozen,
        ),
    )
    print("Full B4 checkpoint independent audit PASS", len(actual), "arrays", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--producer", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.producer.resolve(), args.output.resolve())
