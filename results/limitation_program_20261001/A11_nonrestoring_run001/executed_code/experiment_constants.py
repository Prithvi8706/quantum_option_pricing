"""Finite exact constant-library screens and complete capped gate replays."""

import argparse
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import random
import shutil
import sys
import time

from research.controlled_priority_completion.parallel_source import entries
from research.controlled_source_completion.compact_parallel import (
    execute_compact_parallel,
    make_compact_schedule,
)
from research.controlled_source_completion.compiler import compile_graph, resolve_library
from research.controlled_source_completion.constant_multiplier import STRATEGIES
from research.controlled_source_completion.ir import evaluate
from research.limitation_program_20261001.progress import ROOT, update_progress


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def changed_calls(old, new):
    if len(old["forward_calls"]) != len(new["forward_calls"]):
        raise ValueError("replacement changed the financial call count")
    old_entries, new_entries = entries(old), entries(new)
    changes, unchanged = [], set()
    old_path, new_path = resolve_library(old), resolve_library(new)
    for index, (before, after) in enumerate(zip(old["forward_calls"], new["forward_calls"])):
        if before["args"] != after["args"] or before["out"] != after["out"]:
            raise ValueError("replacement changed a financial SSA binding")
        left, right = old_entries[before["leaf"]], new_entries[after["leaf"]]
        if left["op"] != right["op"] or left["params"] != right["params"]:
            raise ValueError("replacement changed a financial operation")
        if before["leaf"] == after["leaf"]:
            key = before["leaf"]
            if key in unchanged:
                continue
            if digest(old_path / (key + ".json")) != digest(new_path / (key + ".json")):
                raise ValueError("fallback leaf metadata changed")
            if digest(old_path / left["gate_file"]) != digest(new_path / right["gate_file"]):
                raise ValueError("fallback leaf gates changed")
            unchanged.add(key)
        else:
            changes.append(
                dict(
                    call_index=index,
                    args=before["args"],
                    out=before["out"],
                    old_key=before["leaf"],
                    new_key=after["leaf"],
                    op=left["op"],
                    params=left["params"],
                    old_resources=left["resources"],
                    new_resources=right["resources"],
                    input_contract=right.get("input_contract", {}),
                )
            )
    return dict(changes=changes, unchanged_leaf_keys=sorted(unchanged))


def run(source_root, output, mode):
    from research.limitation_program_20261001.constant_library import (
        ConstantIntegrationLibrary,
    )

    source_root, output = source_root.resolve(), output.resolve()
    baseline_summary = read(source_root / "summary.json")
    if not baseline_summary["passed"] or not baseline_summary["accepted"]:
        raise ValueError("source root is not an accepted exact baseline")
    output.mkdir(parents=True, exist_ok=False)
    dependencies = [
        Path(__file__),
        ROOT / "research/limitation_program_20261001/constant_library.py",
        ROOT / "research/controlled_source_completion/compact_parallel.py",
        ROOT / "research/controlled_source_completion/constant_multiplier.py",
        ROOT / "research/controlled_source_completion/log_constant_multiplier.py",
        ROOT / "research/limitation_program_20261001/prove_log_exponent.py",
        ROOT / "research/controlled_source_completion/compiler.py",
        ROOT / "research/controlled_source_completion/primitives.py",
        ROOT / "research/controlled_source_completion/compact_storage.py",
        ROOT / "research/controlled_source_completion/ir.py",
        ROOT / "research/controlled_priority_completion/parallel_source.py",
        ROOT / "research/journal_sprint/reversible_fixed_point.py",
        ROOT / "research/limitation_program_20261001/test_constant_integration.py",
        ROOT / "research/limitation_program_20261001/test_log_constant_multiplier.py",
        ROOT / "research/limitation_program_20261001/test_inverse_ln2_multiplier.py",
    ]
    snapshots = output / "executed_code"
    snapshots.mkdir()
    frozen = []
    for dependency in dependencies:
        snapshot = snapshots / dependency.name
        shutil.copy2(dependency, snapshot)
        frozen.append(
            dict(
                source=str(dependency.relative_to(ROOT)),
                snapshot=str(snapshot.relative_to(output)),
                sha256=digest(snapshot),
            )
        )
    coefficient = 1586259972792 if mode == "inverse" else 762123384786
    # Fixed, bounded test-vector generation, not a sampled price estimate.
    b4_target = read(source_root / "B4x12/target.json")
    generator = random.Random(20261001)
    positive_sample = None
    for attempt in range(64):
        sample = {
            node["params"]["name"]: generator.getrandbits(node["params"]["bits"])
            for node in b4_target["nodes"]
            if node["op"] == "input"
        }
        if evaluate(b4_target, sample)["Y"] > 0:
            positive_sample = dict(inputs=sample, attempt=attempt)
            break
    if positive_sample is None:
        raise ValueError("bounded B4 positive-payoff test-vector screen found no case")
    baseline_hashes = {"summary.json": digest(source_root / "summary.json")}
    for name in ("B4x12", "B8x52"):
        for filename in ("target.json", "source.json", "schedule_capped.json"):
            baseline_hashes[name + "/" + filename] = digest(source_root / name / filename)
        original = read(source_root / name / "source.json")
        library_path = resolve_library(original)
        for key, entry in entries(original).items():
            if digest(library_path / entry["gate_file"]) != entry["sha256"]:
                raise ValueError("baseline leaf hash mismatch")
            baseline_hashes[name + "/leaves/" + key + ".json"] = digest(
                library_path / (key + ".json")
            )
            baseline_hashes[name + "/leaves/" + entry["gate_file"]] = entry["sha256"]
    save(
        output / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            local_only=True,
            items=["A10", "A07"] if mode == "log" else ["A10"],
            mode=mode,
            coefficient=coefficient,
            source_root=str(source_root.relative_to(ROOT)),
            changed="Only guarded signed7 log leaves"
            if mode == "log"
            else "Only general signed72 inverse-ln2 constant leaves, no input promise",
            unchanged="Financial target bytes, precision, law, all other gate/metadata bytes",
            candidates=list(STRATEGIES),
            cap="Actual accepted baseline logical qubits, separately for each case",
            selection="Eligible complete-source Pareto improvement; minimum T-depth, "
            "then T count, Clifford+T depth and logical qubits",
            acceptance="Both complete cases have no increase in T-depth, T count or "
            "Clifford+T depth at the existing cap, with at least one strict decrease; "
            "exact arbitrary-output XOR and full cleanup in every emitted replay",
            replays="Chosen B4 previous random, all-zero and fixed positive-payoff input; "
            "chosen B8 previous random (already positive payoff)",
            positive_test_vector=dict(seed=20261001, maximum_draws=64, **positive_sample),
            exclusions="No continuous-price certificate, physical runtime or advantage claim",
            executed_dependencies=frozen,
            baseline_hashes=baseline_hashes,
            environment=dict(
                python=sys.version,
                executable=sys.executable,
                executable_sha256=digest(Path(sys.executable)),
                packages={
                    name: version(name) for name in ("numpy", "scipy", "numba", "qiskit", "pytest")
                },
            ),
        ),
    )
    update_progress(
        ["A10"],
        mode + " constant full-source resource screen",
        next_action="Screen all four strategies at fixed caps, replay only "
        "the best eligible source and retain only a verified improvement",
    )
    cases = []
    for name in ("B4x12", "B8x52"):
        base_dir = source_root / name
        target, original = read(base_dir / "target.json"), read(base_dir / "source.json")
        old_schedule = read(base_dir / "schedule_capped.json")
        old_resources = old_schedule["resources"]
        cap = old_resources["logical_qubits"]
        directory = output / name
        directory.mkdir()
        trials = []
        for strategy in STRATEGIES:
            trial_dir = directory / strategy
            library = ConstantIntegrationLibrary(
                trial_dir / "leaves",
                target,
                original,
                log_strategy=strategy if mode == "log" else None,
                general_replacements={coefficient: strategy} if mode == "inverse" else None,
            )
            source, _ = compile_graph(target, trial_dir, library)
            if read(trial_dir / "target.json") != target:
                raise ValueError("target semantics changed")
            shutil.copy2(base_dir / "target.json", trial_dir / "target.json")
            attribution = changed_calls(original, source)
            if not attribution["changes"]:
                raise ValueError("candidate changed no intended calls")
            save(trial_dir / "changed_calls.json", attribution)
            save(trial_dir / "site_decisions.json", library.decisions)
            try:
                schedule = make_compact_schedule(target, source, cap)
            except ValueError as error:
                row = dict(strategy=strategy, eligible=False, reason=str(error))
            else:
                save(trial_dir / "schedule_capped.json", schedule)
                resources = schedule["resources"]
                fields = ("t_depth", "t_count", "clifford_t_depth")
                eligible = (
                    resources["logical_qubits"] <= cap
                    and all(resources[field] <= old_resources[field] for field in fields)
                    and any(resources[field] < old_resources[field] for field in fields)
                )
                row = dict(
                    strategy=strategy,
                    resources=resources,
                    eligible=eligible,
                    batches=len(schedule["groups"]),
                    changed_calls=len(attribution["changes"]),
                )
                print(
                    name,
                    strategy,
                    "T-depth",
                    resources["t_depth"],
                    "T count",
                    resources["t_count"],
                    "qubits",
                    resources["logical_qubits"],
                    "eligible",
                    eligible,
                    flush=True,
                )
            trials.append(row)
            save(directory / "screen.json", trials)
        eligible = [row for row in trials if row["eligible"]]
        result = dict(
            case=name,
            baseline=old_resources,
            trials=trials,
            target_sha256=digest(base_dir / "target.json"),
            accepted=False,
            replay_passed=False,
            replays=[],
        )
        if not eligible:
            result.update(decision="No complete-source Pareto improvement; baseline retained")
            save(directory / "comparison.json", result)
            cases.append(result)
            continue
        selected = min(
            eligible,
            key=lambda row: tuple(
                row["resources"][field]
                for field in ("t_depth", "t_count", "clifford_t_depth", "logical_qubits")
            ),
        )
        selected_dir = directory / selected["strategy"]
        source = read(selected_dir / "source.json")
        schedule = read(selected_dir / "schedule_capped.json")
        for filename in ("source.json", "target.json", "schedule_capped.json"):
            shutil.copy2(selected_dir / filename, directory / filename)
        result.update(selected=selected, candidate=selected["resources"])
        previous = next(row for row in baseline_summary["cases"] if row["case"] == name)
        inputs = previous["replays"][0]["inputs"]
        samples = [("previous_random", inputs)]
        if name == "B4x12":
            samples.append(("all_zero", {n["params"]["name"]: 0 for n in source["inputs"]}))
            samples.append(("positive_payoff", positive_sample["inputs"]))
        initial = {key: int("a5" * 9, 16) for key in source["outputs"]}
        for label, sample in samples:
            started = time.perf_counter()
            _, trace = evaluate(target, sample, True)
            expected = {
                key: trace[value] ^ initial[key] for key, value in source["outputs"].items()
            }
            actual = execute_compact_parallel(target, source, schedule, sample, initial)
            if actual["values"] != expected or not actual["all_input_and_workspace_bits_restored"]:
                raise AssertionError("full gate replay failed")
            result["replays"].append(
                dict(
                    label=label,
                    inputs=sample,
                    initial=initial,
                    expected=expected,
                    actual=actual,
                    passed=True,
                    seconds=time.perf_counter() - started,
                )
            )
            save(directory / "comparison.json", result)
            print(name, mode, label, "complete compact gate replay PASS", flush=True)
            update_progress(
                ["A10"],
                name + " " + mode + " replay " + label,
                next_action="Finish preregistered replays and verify saved receipts",
            )
        result.update(accepted=True, replay_passed=True)
        save(directory / "comparison.json", result)
        cases.append(result)
    accepted = all(row["accepted"] for row in cases)
    save(
        output / "summary.json",
        dict(
            cases=cases,
            accepted=accepted,
            passed=all(
                row["replay_passed"] or not any(t["eligible"] for t in row["trials"])
                for row in cases
            ),
            decision="Accepted exact constant integration" if accepted else "Baseline retained",
            mode=mode,
            complete_source_gain_is_measured=True,
        ),
    )
    update_progress(
        ["A10"],
        "complete " + mode + " integration",
        decision="accepted exact component; broader arithmetic family remains open"
        if accepted
        else "screened candidate; prior baseline retained",
        receipts=[str((output / "summary.json").relative_to(ROOT))],
        baseline=str(output.relative_to(ROOT)) if accepted else None,
        next_action="Reconcile accepted source costs and screen the next dominant arithmetic leaf",
        gates={
            "G1": "passed for current exact B4/B8 source; financial error "
            "certification and physical mapping remain open"
        },
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--mode", required=True, choices=("log", "inverse"))
    args = parser.parse_args()
    run(args.source_root, args.output, args.mode)
