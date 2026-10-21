"""Two prospective exact streaming placements on the original B2x4 harness."""

from __future__ import annotations

# Frozen protocol prose is retained as exact readable literals.
# ruff: noqa: E501

import argparse
from datetime import datetime, timezone
from itertools import product
from pathlib import Path
import random
import shutil
import sys
import time

import pytest

from research.controlled_source_completion.compact_parallel_v7 import (
    execute_compact_parallel,
    make_compact_schedule,
)
from research.controlled_source_completion.ir import evaluate
from research.limitation_program_20261001.constant_library import digest
from research.limitation_program_20261001.experiment_checkpoint import (
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
from research.limitation_program_20261001.streaming_scope import (
    streaming_statistics_from_original_trace,
)

REFERENCE = PROGRAM / "A19_reference_run001"
PLACEMENTS = ("date-boundaries", "two-date-blocks")
TESTS = (
    "test_streaming_updates.py",
    "test_streaming_stage_schedule.py",
    "test_streaming_circuit.py",
)
CPU_LIMIT = 3600


def ensure_cpu(start):
    if time.process_time() - start > CPU_LIMIT:
        raise TimeoutError("Prospective A19 process CPU limit")


def prepare(output):
    output.relative_to(PROGRAM.resolve())
    assert not output.exists()
    assert read(REFERENCE / "summary.json")["passed"]
    source = read(REFERENCE / "source.json")
    old = read(REFERENCE / "protocol.json")
    verify(old)
    frozen = dict(old["frozen_inputs"])
    frozen.update(read(REFERENCE / "manifest.json")["files"])
    frozen[relative(REFERENCE / "manifest.json")] = digest(REFERENCE / "manifest.json")
    output.mkdir()
    dependencies = []
    for name in (
        "experiment_streaming.py",
        "streaming_updates.py",
        "streaming_stage_schedule.py",
        "streaming_circuit.py",
        *TESTS,
    ):
        path = ROOT / "research/limitation_program_20261001" / name
        frozen[relative(path)] = digest(path)
        copy = output / "executed_code" / name
        copy.parent.mkdir(exist_ok=True)
        shutil.copy2(path, copy)
        dependencies.append(
            dict(
                source=relative(path),
                snapshot=copy.relative_to(output).as_posix(),
                sha256=digest(path),
            )
        )
    protocol = dict(
        local_only=True,
        created_utc=datetime.now(timezone.utc).isoformat(),
        item="A19 exact B2x4 streaming",
        before_tests_candidate_emission_and_grid_execution=True,
        reference=relative(REFERENCE),
        placements=list(PLACEMENTS),
        financial_max_lanes={"date-boundaries": 2, "two-date-blocks": 4},
        serial_stages=["Gaussian pairs", "increments", "final payoff"],
        qubit_cap=source["resources"]["logical_qubits"],
        counter_bits=3,
        monitoring_dates=4,
        classical_tiny_draw_grid=dict(
            each_uniform_word=[0, (1 << 32) - 1], coordinates=12, combinations=4096
        ),
        vectors=dict(
            families=[
                "all_zero",
                "all_max",
                "all_midpoint",
                "seeded_random",
                "first_positive_payoff",
            ],
            seed=202610019,
            positive_search_limit=256,
            maximum_gate_replays_per_placement=5,
        ),
        dirty_output=int("a5" * 9, 16),
        selection_dimensions=list(DIMENSIONS),
        acceptance="Exact original raw log/prefix, stock-word Asian sum, strict barrier and finite final rounding; complete inputs/workspace/counter/checkpoint cleanup; actual peak <=cap and reduced versus original compact SSA; retain nondominated points with complete extra work/depth charges",
        cleanup="Two-date point snapshots each date raw logs, reverses increments to clear earlier snapshots with correct controls and redoes paid increments to retain block-end state; reverse complete updates after final output. Date point erases local arithmetic before advancing.",
        stop_rule="Exactly one B2x4 harness and two fixed placements, no packing search. Full B4/B8 scaling deferred unless independently verified point and physical-cap frontier support it; this harness cannot replace B8.",
        process_cpu_limit_seconds=CPU_LIMIT,
        full_B4_gate_replays=0,
        B8_attempts=0,
        preferred_latency_source_unchanged=True,
        G2_to_G5="open",
        frozen_inputs=frozen,
        executed_dependencies=dependencies,
        python=sys.version,
        executable=sys.executable,
    )
    save(output / "protocol.json", protocol)
    verify(protocol)
    print("A19 two-placement protocol frozen, cap", protocol["qubit_cap"], flush=True)


def run(output):
    from research.limitation_program_20261001.streaming_updates import emit_updates
    from research.limitation_program_20261001.streaming_circuit import (
        make_streaming_schedule,
        replay_streaming,
    )

    protocol = read(output / "protocol.json")
    assert not (output / "summary.json").exists()
    verify(protocol)
    started = time.process_time()
    rc = pytest.main(
        [
            *(str(ROOT / "research/limitation_program_20261001" / name) for name in TESTS),
            "-q",
            "-p",
            "no:cacheprovider",
            "--junitxml=" + str(output / "tests.xml"),
        ]
    )
    if rc:
        save(output / "failed_tests.json", dict(passed=False, return_code=int(rc)))
        manifest(output, protocol)
        raise AssertionError("Frozen streaming emitted fixtures failed")
    target, source, scope = (
        read(REFERENCE / name) for name in ("target.json", "source.json", "scope.json")
    )
    control = make_compact_schedule(target, source, protocol["qubit_cap"])
    save(output / "control_schedule.json", control)
    update_directory = output / "updates"
    updates = emit_updates(update_directory, width=72, counter_bits=3)
    attempts = []
    for placement in PLACEMENTS:
        ensure_cpu(started)
        schedule = make_streaming_schedule(
            target, source, scope, placement, updates, update_directory
        )
        save(output / (placement + "_schedule.json"), schedule)
        row = dict(placement=placement, resources=schedule["resources"], replays=[])
        row["fits_cap"] = row["resources"]["logical_qubits"] <= protocol["qubit_cap"]
        row["width_saving"] = (
            row["resources"]["logical_qubits"] < control["resources"]["logical_qubits"]
        )
        attempts.append(row)
        print(placement, "actual resources", row["resources"], flush=True)
    alternatives = [control["resources"]] + [r["resources"] for r in attempts if r["fits_cap"]]
    for row in attempts:
        row["nondominated"] = row["fits_cap"] and not dominated(row["resources"], alternatives)
    # Exhaust the declared grid against independent original-SSA raw traces.
    # This checks statistic identities; it is not 4096 emitted gate replays.
    names = [n["params"]["name"] for n in source["inputs"]]
    grid_count = positive_count = 0
    outputs = set()
    for words in product(protocol["classical_tiny_draw_grid"]["each_uniform_word"], repeat=12):
        ensure_cpu(started)
        values = dict(zip(names, words, strict=True))
        _, trace = evaluate(target, values, True)
        comparison = streaming_statistics_from_original_trace(scope, trace)
        outputs.add(comparison["raw_output"])
        positive_count += int(comparison["raw_output"] > 0)
        grid_count += 1
    assert grid_count == 4096
    save(
        output / "tiny_grid.json",
        dict(
            passed=True,
            original_integer_trace_comparisons=grid_count,
            positive_payoff_inputs=positive_count,
            distinct_raw_outputs=len(outputs),
            coverage="Declared endpoint grid only; modular identities and source binding supply the general semantic argument",
            emitted_gate_replays=0,
        ),
    )
    rng = random.Random(protocol["vectors"]["seed"])
    vectors = [
        dict(label=label, inputs={name: word for name in names})
        for label, word in (("all_zero", 0), ("all_max", (1 << 32) - 1), ("all_midpoint", 1 << 31))
    ]
    vectors.append(
        dict(label="seeded_random", inputs={name: rng.randrange(1 << 32) for name in names})
    )
    positive_search = 0
    for i in range(protocol["vectors"]["positive_search_limit"]):
        ensure_cpu(started)
        values = {name: rng.randrange(1 << 32) for name in names}
        _, trace = evaluate(target, values, True)
        positive_search = i + 1
        if trace[target["outputs"]["Y"]] > 0:
            vectors.append(dict(label="first_positive_payoff", inputs=values))
            break
    save(
        output / "replay_vectors.json",
        dict(vectors=vectors, positive_search_evaluations=positive_search),
    )
    initial = {name: protocol["dirty_output"] for name in source["outputs"]}
    sample = vectors[-1]
    _, trace = evaluate(target, sample["inputs"], True)
    expected = {name: trace[value] ^ initial[name] for name, value in source["outputs"].items()}
    actual = execute_compact_parallel(target, source, control, sample["inputs"], initial)
    assert actual["values"] == expected and actual["all_input_and_workspace_bits_restored"]
    save(
        output / "control_replay.json",
        dict(
            passed=True,
            label=sample["label"],
            inputs=sample["inputs"],
            initial=initial,
            expected=expected,
            actual=actual,
            harness_only=True,
        ),
    )
    for row in attempts:
        if not (row["fits_cap"] and row["width_saving"] and row["nondominated"]):
            continue
        schedule = read(output / (row["placement"] + "_schedule.json"))
        for sample in vectors:
            ensure_cpu(started)
            _, trace = evaluate(target, sample["inputs"], True)
            expected = {
                name: trace[value] ^ initial[name] for name, value in source["outputs"].items()
            }
            actual = replay_streaming(
                target, source, scope, schedule, sample["inputs"], initial, expected_trace=trace
            )
            assert actual["values"] == expected and actual["all_input_and_workspace_bits_restored"]
            row["replays"].append(
                dict(
                    passed=True,
                    label=sample["label"],
                    inputs=sample["inputs"],
                    initial=initial,
                    expected=expected,
                    actual=actual,
                )
            )
            save(output / (row["placement"] + "_comparison.json"), row)
            print(row["placement"], sample["label"], "exact harness gate replay PASS", flush=True)
    frontier = [
        r["placement"]
        for r in attempts
        if r["nondominated"] and r["width_saving"] and len(r["replays"]) == len(vectors)
    ]
    result = dict(
        passed=True,
        local_only=True,
        harness="B2x4",
        control_resources=control["resources"],
        attempts=attempts,
        retained_harness_frontier=frontier,
        classical_grid_comparisons=4096,
        new_harness_gate_replays=1 + sum(len(r["replays"]) for r in attempts),
        new_complete_B4_B8_financial_gate_replays=0,
        full_B4_scaling_executed=False,
        preferred_latency_source_unchanged=True,
        G2_to_G5="open",
        process_cpu_seconds=time.process_time() - started,
    )
    save(output / "summary.json", result)
    manifest(output, protocol)
    print("A19 bounded harness done", frontier, flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    (prepare if args.phase == "prepare" else run)(args.output.resolve())
