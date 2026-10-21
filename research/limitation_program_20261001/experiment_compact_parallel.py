"""Integrate exact compact bindings with the latest capped arithmetic sources."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import time

from research.controlled_source_completion.compact_parallel import (
    execute_compact_parallel,
    make_compact_schedule,
)
from research.controlled_source_completion.compiler import resolve_library
from research.controlled_priority_completion.parallel_source import entries
from research.controlled_source_completion.ir import evaluate
from research.limitation_program_20261001.progress import ROOT, update_progress


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def case_paths(source_root, case):
    summary = read(source_root / "summary.json")
    previous = next(row for row in summary["cases"] if row["case"] == case)
    return source_root / case / previous["best"]["strategy"], previous


def run(source_root, output):
    source_root, output = source_root.resolve(), output.resolve()
    baseline_receipt = ROOT / "results/limitation_program_20261001/G0_run003/summary.json"
    accounting_receipt = ROOT / "results/limitation_program_20261001/A01_run003/summary.json"
    assert read(baseline_receipt)["passed"] and read(accounting_receipt)["passed"]
    output.mkdir(parents=True, exist_ok=False)
    save(
        output / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            items=["A06", "H15", "C13"],
            source_root=str(source_root),
            changed="Exact compact SSA bindings and memory-capped batch packing",
            unchanged="Financial IR, precision, tables, input law and "
            "all arithmetic leaf gate bytes",
            candidates="Four fixed cap points: original, half retained saving, full retained "
            "saving, 1.5 times retained saving (bounded by one-leaf minimum)",
            selection="Minimum T-depth, then Clifford+T depth, then actual logical qubits "
            "under the original cap",
            acceptance="Exact output XOR and full cleanup in emitted replays; T count "
            "unchanged; complete depth or memory Pareto improvement",
            replays="Chosen B4 previous random/zero/max, chosen B8 previous random; "
            "one additional memory Pareto point per case when distinct",
            exclusions="No changed financial law, estimator, routing, physical runtime "
            "or advantage claim",
            producer_sha256=digest(Path(__file__)),
            implementation_sha256=digest(
                ROOT / "research/controlled_source_completion/compact_parallel.py"
            ),
        ),
    )
    update_progress(
        ["C01", "C02", "C03", "A01"],
        "baseline freeze and cost reconciliation",
        decision="completed scoped baseline audit; financial certificates remain open",
        receipts=[str(p.relative_to(ROOT)) for p in (baseline_receipt, accounting_receipt)],
        gates={
            "G0": "passed for current B4/B8 task and provenance",
            "G1": "prior verified exact baseline; new integrations require replay",
        },
    )
    update_progress(
        ["A07"],
        "logarithm exponent structural proof",
        decision="verified signed-seven-bit interface; broader range investigation remains open",
        receipts=["results/limitation_program_20261001/A07_run001/result.json"],
    )
    update_progress(
        ["A06", "H15", "C13"],
        "compact schedule generation",
        next_action="Verify compact bindings, select finite Pareto screen, "
        "replay both complete sources",
    )
    cases = []
    for name in ("B4x12", "B8x52"):
        original, previous = case_paths(source_root, name)
        target, source = read(original / "target.json"), read(original / "source.json")
        baseline = read(original / "schedule_capped.json")
        cap = baseline["resources"]["logical_qubits"]
        directory = output / name
        directory.mkdir()
        for file in ("target.json", "source.json"):
            shutil.copy2(original / file, directory / file)
            assert digest(original / file) == digest(directory / file)
        library = resolve_library(source)
        leaves = entries(source)
        leaf_hashes = {}
        for key, entry in leaves.items():
            assert digest(library / entry["gate_file"]) == entry["sha256"]
            leaf_hashes[key] = dict(
                metadata_sha256=digest(library / (key + ".json")), gate_sha256=entry["sha256"]
            )
        save(directory / "unchanged_leaves.json", leaf_hashes)
        full = make_compact_schedule(target, source, cap)
        saving = source["values"] * source["word_width"] - full["retained_ssa_qubits"]
        floor = (
            full["retained_ssa_qubits"]
            + len(source["outputs"]) * source["word_width"]
            + max(
                (
                    leaves[c["leaf"]]["resources"]["qubits"]
                    - sum(full["widths"][v] for v in c["out"])
                    for c in source["forward_calls"]
                ),
                default=0,
            )
        )
        caps = list(
            dict.fromkeys(
                [
                    cap,
                    max(floor, cap - saving // 2),
                    max(floor, cap - saving),
                    max(floor, cap - 3 * saving // 2),
                ]
            )
        )
        trials = []
        schedules = {}
        for index, point in enumerate(caps):
            schedule = full if point == cap else make_compact_schedule(target, source, point)
            assert schedule["resources"]["logical_qubits"] <= point
            assert schedule["resources"]["t_count"] == baseline["resources"]["t_count"]
            file = f"schedule_trial_{index}.json"
            save(directory / file, schedule)
            row = dict(
                cap=point,
                resources=schedule["resources"],
                schedule=file,
                batches=len(schedule["groups"]),
                retained_ssa_qubits=schedule["retained_ssa_qubits"],
                argument_and_output_copy_cx=schedule["argument_and_output_copy_cx"],
                baseline_argument_and_output_copy_cx=schedule[
                    "baseline_argument_and_output_copy_cx"
                ],
            )
            trials.append(row)
            schedules[file] = schedule
            print(
                name,
                "cap",
                point,
                "actual",
                row["resources"]["logical_qubits"],
                "T-depth",
                row["resources"]["t_depth"],
                flush=True,
            )
        best = min(
            trials,
            key=lambda row: (
                row["resources"]["t_depth"],
                row["resources"]["clifford_t_depth"],
                row["resources"]["logical_qubits"],
            ),
        )
        valid_memory = [
            row for row in trials if row["resources"]["t_depth"] <= baseline["resources"]["t_depth"]
        ]
        memory = (
            min(valid_memory, key=lambda row: row["resources"]["logical_qubits"])
            if valid_memory
            else None
        )
        candidate = schedules[best["schedule"]]
        accepted = (
            best["resources"]["t_depth"] <= baseline["resources"]["t_depth"]
            and best["resources"]["logical_qubits"] <= cap
            and (
                best["resources"]["t_depth"] < baseline["resources"]["t_depth"]
                or best["resources"]["logical_qubits"] < cap
            )
        )
        save(directory / "schedule_capped.json", candidate)
        result = dict(
            case=name,
            baseline=baseline["resources"],
            candidate=best["resources"],
            selected=best,
            memory_pareto=memory,
            trials=trials,
            original_target_sha256=digest(original / "target.json"),
            original_source_sha256=digest(original / "source.json"),
            arithmetic_leaf_bytes_unchanged=True,
            accepted=False,
            replay_passed=False,
            replays=[],
        )
        save(directory / "comparison.json", result)
        samples = [("previous_random", previous["replays"][0]["inputs"])]
        if name == "B4x12":
            names = [node["params"]["name"] for node in source["inputs"]]
            samples += [
                ("all_zero", dict.fromkeys(names, 0)),
                ("all_maximum", dict.fromkeys(names, 2**32 - 1)),
            ]
        runs = [(label, inputs, best) for label, inputs in samples]
        if memory and memory["schedule"] != best["schedule"]:
            runs.append(("memory_pareto_random", samples[0][1], memory))
        initial = {name: int("a5" * 9, 16) for name in source["outputs"]}
        for label, inputs, trial in runs:
            started = time.perf_counter()
            schedule = schedules[trial["schedule"]]
            _, trace = evaluate(target, inputs, True)
            assert all(not (trace[v] & ~mask) for v, mask in enumerate(schedule["proof_masks"]))
            expected = {name: trace[v] ^ initial[name] for name, v in source["outputs"].items()}
            actual = execute_compact_parallel(target, source, schedule, inputs, initial)
            assert actual["values"] == expected
            assert actual["all_input_and_workspace_bits_restored"]
            result["replays"].append(
                dict(
                    label=label,
                    schedule=trial["schedule"],
                    inputs=inputs,
                    initial=initial,
                    expected=expected,
                    actual=actual,
                    passed=True,
                    seconds=time.perf_counter() - started,
                )
            )
            save(directory / "comparison.json", result)
            print(name, label, "complete compact gate replay PASS", flush=True)
            update_progress(
                ["A06", "H15", "C13"],
                name + " replay " + label,
                next_action="Finish the preregistered compact replays and "
                "record the accepted Pareto result",
            )
        result.update(accepted=accepted, replay_passed=True)
        save(directory / "comparison.json", result)
        cases.append(result)
    passed = all(case["replay_passed"] for case in cases)
    accepted = all(case["accepted"] for case in cases)
    save(
        output / "summary.json",
        dict(
            cases=cases,
            passed=passed,
            accepted=accepted,
            decision="Accepted exact integration"
            if accepted
            else "Correct candidate; retain prior accepted baseline",
            scope="Exact compact memory and logical-depth tradeoffs for "
            "the unchanged arithmetic source",
        ),
    )
    update_progress(
        ["A06", "H15", "C13"],
        "complete compact integration",
        decision="accepted exact component"
        if accepted
        else "tested candidate; prior baseline retained",
        receipts=[str((output / "summary.json").relative_to(ROOT))],
        baseline=str(output.relative_to(ROOT)) if accepted else None,
        next_action="Use A07 log-exponent proof to screen an exact "
        "signed-seven-bit constant multiplier",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    run(args.source_root, args.output)
