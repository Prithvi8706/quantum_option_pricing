"""Prospective single B4 embedding of the verified paid checkpoint frontier."""

from __future__ import annotations

# Frozen prospective protocol descriptions remain single exact literals.
# ruff: noqa: E501

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import sys

import pytest

from research.controlled_source_completion.ir import evaluate
from research.limitation_program_20261001.checkpoint_B4 import make_b4_schedule, replay_b4
from research.limitation_program_20261001.constant_library import digest
from research.limitation_program_20261001.experiment_checkpoint import (
    CASE,
    DIMENSIONS,
    PROGRAM,
    dominated,
    manifest,
    read,
    relative,
    save,
    verify,
)
from research.limitation_program_20261001.progress import ROOT

PRODUCER = PROGRAM / "A18_run001"
AUDIT = PROGRAM / "A01_run015"


def prepare(output):
    output.relative_to(PROGRAM.resolve())
    assert not output.exists()
    summary, audit = read(PRODUCER / "summary.json"), read(AUDIT / "summary.json")
    assert summary["passed"] and audit["passed"]
    selected = summary["selected_for_one_B4_integration"]
    assert selected in audit["retained_workspace_frontier"]
    prior = read(PRODUCER / "protocol.json")
    verify(prior)
    frozen = dict(prior["frozen_inputs"])
    for directory in (PRODUCER, AUDIT):
        data = read(directory / "manifest.json")
        frozen.update(data["files"])
        frozen[relative(directory / "manifest.json")] = digest(directory / "manifest.json")
    output.mkdir()
    snapshots = []
    for filename in ("checkpoint_B4.py", "test_checkpoint_B4.py", "experiment_checkpoint_B4.py"):
        path = ROOT / "research/limitation_program_20261001" / filename
        frozen[relative(path)] = digest(path)
        copy = output / "executed_code" / filename
        copy.parent.mkdir(exist_ok=True)
        shutil.copy2(path, copy)
        snapshots.append(
            dict(
                source=relative(path),
                snapshot=copy.relative_to(output).as_posix(),
                sha256=digest(path),
            )
        )
    protocol = dict(
        created_utc=datetime.now(timezone.utc).isoformat(),
        local_only=True,
        before_tests_and_complete_source_cost_measurement=True,
        baseline=relative(CASE),
        extracted_producer=relative(PRODUCER),
        independent_audit=relative(AUDIT),
        selected=selected,
        candidate_limit=1,
        B8_limit=0,
        full_replays_limit=3,
        comparison="Matched retain-all extracted subroutine with identical outside allocations/serial leaf execution, plus accepted parallel latency source. Keep only nondominated width-saving point; no latency threshold.",
        selection_dimensions=list(DIMENSIONS),
        replay_vectors=prior["replay_vectors"],
        dirty_output=prior["dirty_output"],
        stop_rule="One B4 candidate and one matched retain-all control. No gate replay if dominated or no global memory saving; no alternate points or B8 scaling.",
        preferred_latency_source_unchanged=True,
        G2_to_G5="open",
        frozen_inputs=frozen,
        executed_dependencies=snapshots,
        executable=sys.executable,
    )
    save(output / "protocol.json", protocol)
    verify(protocol)
    print("Single B4 integration protocol frozen", selected, flush=True)


def run(output):
    protocol = read(output / "protocol.json")
    assert not (output / "summary.json").exists()
    verify(protocol)
    rc = pytest.main(
        [
            str(ROOT / "research/limitation_program_20261001/test_checkpoint_B4.py"),
            "-q",
            "-p",
            "no:cacheprovider",
            "--junitxml=" + str(output / "tests.xml"),
        ]
    )
    if rc != 0:
        save(output / "failed_tests.json", dict(passed=False, return_code=int(rc)))
        manifest(output, protocol)
        raise AssertionError("Prospective B4 embedding fixtures failed")
    target, source = (read(CASE / name) for name in ("target.json", "source.json"))
    scope = read(PRODUCER / "subgraph.json")
    chosen_sub = read(PRODUCER / protocol["selected"] / "schedule.json")
    control_sub = read(PRODUCER / "retain_all_schedule.json")
    control = make_b4_schedule(target, source, scope, control_sub)
    candidate = make_b4_schedule(target, source, scope, chosen_sub)
    assert candidate["outside_allocations"] == control["outside_allocations"]
    assert candidate["private_base"] == control["private_base"]
    save(output / "matched_retain_all_schedule.json", control)
    save(output / "schedule.json", candidate)
    latency = read(CASE / "schedule_capped.json")["resources"]
    width_saving = candidate["resources"]["logical_qubits"] < control["resources"]["logical_qubits"]
    nondominated = not dominated(candidate["resources"], [control["resources"], latency])
    accepted = width_saving and nondominated
    replays = []
    if accepted:
        initial = {name: protocol["dirty_output"] for name in source["outputs"]}
        for sample in protocol["replay_vectors"]:
            _, trace = evaluate(target, sample["inputs"], True)
            expected = {
                name: trace[value] ^ initial[name] for name, value in source["outputs"].items()
            }
            actual = replay_b4(
                target,
                source,
                scope,
                chosen_sub,
                candidate,
                sample["inputs"],
                initial,
                expected_trace=trace,
            )
            assert actual["values"] == expected and actual["all_input_and_workspace_bits_restored"]
            replays.append(
                dict(
                    label=sample["label"],
                    inputs=sample["inputs"],
                    initial=initial,
                    expected=expected,
                    actual=actual,
                    passed=True,
                )
            )
            save(output / "comparison.json", dict(replays=replays))
            print("Full B4 checkpoint financial replay PASS", sample["label"], flush=True)
    result = dict(
        passed=True,
        local_only=True,
        retained_workspace_point=accepted,
        width_saving_versus_matched_control=width_saving,
        nondominated=nondominated,
        matched_retain_all_resources=control["resources"],
        candidate_resources=candidate["resources"],
        preferred_latency_resources=latency,
        preferred_latency_source_unchanged=True,
        replays=replays,
        new_complete_financial_gate_replays=len(replays),
        checkpoint_global_qubits_saved=control["resources"]["logical_qubits"]
        - candidate["resources"]["logical_qubits"],
        serial_packing_savings_are_separate_from_checkpoint_savings=True,
        target_precision_input_law_and_frozen_leaf_bytes_unchanged=True,
        G2_to_G5="open",
    )
    save(output / "summary.json", result)
    save(output / "result.json", result)
    manifest(output, protocol)
    print(json.dumps({k: v for k, v in result.items() if k not in ("replays",)}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    (prepare if args.phase == "prepare" else run)(args.output.resolve())
