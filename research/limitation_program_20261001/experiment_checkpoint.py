"""Prospective local A18 real-financial checkpointing experiment.

Prepare freezes the actual subgraph, two caps, algorithms and complete original
leaf library before any candidate schedule or correctness tests are executed.
"""

from __future__ import annotations

# Prospective protocol prose is stored as exact readable literals.
# ruff: noqa: E501

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import sys
import time

import pytest

from research.controlled_priority_completion.parallel_source import entries
from research.controlled_source_completion.compiler import resolve_library
from research.controlled_source_completion.ir import evaluate
from research.limitation_program_20261001.constant_library import digest
from research.limitation_program_20261001.progress import ROOT

PROGRAM = ROOT / "results/limitation_program_20261001"
BASELINE = PROGRAM / "A10_coefficient_run001"
CASE = BASELINE / "B4x12/min-depth"
HEURISTICS = ("block-checkpointing", "cost-aware")
FRACTIONS = (75, 50)
DIMENSIONS = ("logical_qubits", "t_count", "t_depth", "clifford_t_depth")
TEST_NAMES = (
    "test_checkpoint_scope.py",
    "test_checkpoint_scheduler.py",
    "test_checkpoint_circuit.py",
)


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def relative(path):
    return path.resolve().relative_to(ROOT).as_posix()


def verify(protocol):
    for name, expected in protocol["frozen_inputs"].items():
        if digest(ROOT / name) != expected:
            raise AssertionError("A18 frozen input changed: " + name)


def manifest(output, protocol):
    verify(protocol)
    save(
        output / "manifest.json",
        {
            "files": {
                relative(p): digest(p)
                for p in sorted(output.rglob("*"))
                if p.is_file() and p.name != "manifest.json"
            },
            "frozen_inputs": protocol["frozen_inputs"],
            "manifest_self_hash_excluded": True,
        },
    )


def prepare(output):
    from research.limitation_program_20261001.checkpoint_scope import build_scope

    output.relative_to(PROGRAM.resolve())
    if output.exists():
        raise FileExistsError("A18 receipt must be new")
    accepted = read(PROGRAM / "progress.json")["accepted_baseline"]
    if accepted != relative(BASELINE):
        raise AssertionError("A18 baseline must match the accepted live source")
    prior = read(BASELINE / "summary.json")
    if not prior["passed"] or not prior["accepted"] or prior["selected"] != "min-depth":
        raise AssertionError("Verified coefficient baseline required")
    # This is extraction and a required-leaf lower bound, not a candidate run.
    scope = build_scope(CASE)
    source = read(CASE / "source.json")
    archive = resolve_library(source)
    frozen = {}
    for p in ROOT.joinpath("research").rglob("*.py"):
        # Optional fullB4 work has its own later prospective protocol.
        if "checkpoint_b4" in p.name.lower():
            continue
        frozen[relative(p)] = digest(p)
    for p in (
        BASELINE / "manifest.json",
        BASELINE / "summary.json",
        PROGRAM / "A01_run014/manifest.json",
        PROGRAM / "WAVE07_run001/manifest.json",
        *(CASE / name for name in ("source.json", "target.json", "schedule_capped.json")),
    ):
        frozen[relative(p)] = digest(p)
    for key, entry in entries(source).items():
        for p in (archive / (key + ".json"), archive / entry["gate_file"]):
            frozen[relative(p)] = digest(p)
        if frozen[relative(archive / entry["gate_file"])] != entry["sha256"]:
            raise AssertionError("Actual baseline leaf hash mismatch")
    output.mkdir()
    save(output / "subgraph.json", scope)
    dependencies = []
    for p in sorted(ROOT.joinpath("research/limitation_program_20261001").glob("*checkpoint*.py")):
        if "checkpoint_b4" in p.name.lower():
            continue
        snapshot = output / "executed_code" / p.name
        snapshot.parent.mkdir(exist_ok=True)
        shutil.copy2(p, snapshot)
        dependencies.append(
            {
                "source": relative(p),
                "snapshot": snapshot.relative_to(output).as_posix(),
                "sha256": digest(p),
            }
        )
    samples = next(c["replays"] for c in prior["cases"] if c["case"] == "B4x12")
    protocol = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "local_only": True,
        "item": "A18 paid reversible checkpointing",
        "baseline": relative(CASE),
        "scope_sha256": digest(output / "subgraph.json"),
        "before_tests_and_candidate_schedule_generation": True,
        "heuristics": list(HEURISTICS),
        "workspace_percentages": list(FRACTIONS),
        "caps": scope["caps"],
        "floor": scope["fixed_floor"],
        "workspace_baseline": scope["baseline_workspace"],
        "denominator": "Retain-all active intermediate storage plus the maximum actual native private leaf workspace; all 60 B4 random input registers and full72 boundary output destinations remain in fixed floor.",
        "limits_per_attempt": {
            "recursive_events": 100000,
            "paid_moves": 20000,
            "process_cpu_seconds": 900,
        },
        "tie_breaking": "Frozen algorithms use original group/call IDs; no parameter grid or adaptive extra attempts.",
        "selection": "Nondominated actual qubits/T-count/T-depth/Clifford+T-depth versus retain-all and legal candidates. At most one fullB4 point, minimum qubits then T-count,T-depth,CT-depth,declared attempt order.",
        "replay_vectors": samples,
        "dirty_output": int("a5" * 9, 16),
        "full_B4_integration_limit": 1,
        "B8_experiments": 0,
        "acceptance": "Legal actual erasures and clean slot reuse; all copies, native scratch, inverse and recomputation charged; observed peak <=cap; exact original raw integer boundary trace and dirty full72 output XOR, all input/workspace bits restored.",
        "stop_rule": "Exactly two heuristic families by two caps on one fixed real closure; no fullsource scaling without a verified nondominated extracted point.",
        "G2_to_G5": "open",
        "preferred_latency_source_unchanged": True,
        "executed_dependencies": dependencies,
        "frozen_inputs": frozen,
        "python": sys.version,
        "executable": sys.executable,
    }
    save(output / "protocol.json", protocol)
    verify(protocol)
    print("A18 protocol frozen", len(scope["groups"]), "groups", scope["caps"], flush=True)


def dominated(resource, alternatives):
    return any(
        all(other[d] <= resource[d] for d in DIMENSIONS)
        and any(other[d] < resource[d] for d in DIMENSIONS)
        for other in alternatives
    )


def run(output):
    from research.limitation_program_20261001.checkpoint_scheduler import (
        plan_checkpoint,
        retain_all_plan,
    )
    from research.limitation_program_20261001.checkpoint_circuit import (
        emit_checkpoint_schedule,
        replay_checkpoint,
    )

    protocol = read(output / "protocol.json")
    if (output / "summary.json").exists():
        raise FileExistsError("Executed A18 receipt cannot be rerun")
    verify(protocol)
    scope = read(output / "subgraph.json")
    if digest(output / "subgraph.json") != protocol["scope_sha256"]:
        raise AssertionError("Frozen subgraph changed")
    target, source = (read(CASE / name) for name in ("target.json", "source.json"))
    started = time.perf_counter()
    tests = [ROOT / "research/limitation_program_20261001" / name for name in TEST_NAMES]
    if not tests:
        raise AssertionError("Meaningful checkpoint fixtures required")
    rc = pytest.main(
        [
            *(str(p) for p in tests),
            "-q",
            "-p",
            "no:cacheprovider",
            "--junitxml=" + str(output / "tests.xml"),
        ]
    )
    if rc != 0:
        save(output / "failed_tests.json", {"return_code": int(rc), "passed": False})
        manifest(output, protocol)
        raise AssertionError("Frozen checkpoint tests failed")
    baseline_plan = retain_all_plan(scope)
    baseline = emit_checkpoint_schedule(target, source, scope, baseline_plan)
    save(output / "retain_all_schedule.json", baseline)
    rows = []
    for heuristic in HEURISTICS:
        for percentage in FRACTIONS:
            name = f"{heuristic}-{percentage}"
            directory = output / name
            directory.mkdir()
            cap = scope["caps"][str(percentage)]
            plan = plan_checkpoint(scope, cap, heuristic)
            save(directory / "plan.json", plan)
            row = {
                "name": name,
                "heuristic": heuristic,
                "workspace_percent": percentage,
                "cap": cap,
                "feasible": plan["feasible"],
                "replays": [],
            }
            if plan["feasible"]:
                schedule = emit_checkpoint_schedule(target, source, scope, plan)
                save(directory / "schedule.json", schedule)
                row["resources"] = schedule["resources"]
                if schedule["resources"]["logical_qubits"] > cap:
                    raise AssertionError("Actual emitted schedule exceeded declared cap")
            else:
                row["failure"] = plan.get("failure", plan.get("reason"))
            rows.append(row)
            save(output / "attempts.json", rows)
            print(
                name,
                "feasible",
                row["feasible"],
                row.get("resources", row.get("failure")),
                flush=True,
            )
    alternatives = [baseline["resources"]] + [r["resources"] for r in rows if r["feasible"]]
    for row in rows:
        row["nondominated"] = row["feasible"] and not dominated(row["resources"], alternatives)
        row["width_saving"] = (
            row["feasible"]
            and row["resources"]["logical_qubits"] < baseline["resources"]["logical_qubits"]
        )
        if not row["nondominated"] or not row["width_saving"]:
            continue
        schedule = read(output / row["name"] / "schedule.json")
        initial = {o["name"]: protocol["dirty_output"] for o in scope["outputs"]}
        for sample in protocol["replay_vectors"]:
            _, trace = evaluate(target, sample["inputs"], True)
            expected = {o["name"]: trace[o["value"]] ^ initial[o["name"]] for o in scope["outputs"]}
            actual = replay_checkpoint(
                target, source, scope, schedule, sample["inputs"], initial, expected_trace=trace
            )
            if actual["values"] != expected or not actual["all_input_and_workspace_bits_restored"]:
                raise AssertionError("Real extracted financial checkpoint replay failed")
            row["replays"].append(
                {
                    "label": sample["label"],
                    "inputs": sample["inputs"],
                    "initial": initial,
                    "expected": expected,
                    "actual": actual,
                    "passed": True,
                }
            )
            save(output / row["name"] / "comparison.json", row)
            print(row["name"], sample["label"], "real subgraph replay PASS", flush=True)
    survivors = [
        r for r in rows if r["nondominated"] and r["width_saving"] and len(r["replays"]) == 3
    ]
    selected = (
        min(
            survivors, key=lambda r: tuple(r["resources"][d] for d in DIMENSIONS) + (rows.index(r),)
        )
        if survivors
        else None
    )
    summary = {
        "passed": True,
        "local_only": True,
        "baseline_resources": baseline["resources"],
        "attempts": rows,
        "retained_workspace_frontier": [r["name"] for r in survivors],
        "selected_for_one_B4_integration": selected["name"] if selected else None,
        "new_extracted_subgraph_gate_replays": sum(len(r["replays"]) for r in rows),
        "new_complete_financial_gate_replays": 0,
        "preferred_latency_source_unchanged": True,
        "G2_to_G5": "open",
        "A18_entire_limitation_closed": False,
        "wall_seconds": time.perf_counter() - started,
    }
    save(output / "summary.json", summary)
    save(output / "result.json", summary)
    manifest(output, protocol)
    print(
        "A18 bounded extracted experiment complete",
        summary["retained_workspace_frontier"],
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    (prepare if args.phase == "prepare" else run)(args.output.resolve())
