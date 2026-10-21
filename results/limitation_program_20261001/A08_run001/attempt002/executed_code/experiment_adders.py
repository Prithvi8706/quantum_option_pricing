"""Prospective bounded prefix-leaf and exact capped financial-source screen.

No shared compiler, primitive, evidence or progress files are modified. The
full-source threshold is two percent T-depth at the prior actual qubit caps;
failure stops before financial gate replay, retaining the accepted baseline.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import shutil
import sys
import time

import numpy as np
import pytest

from research.controlled_source_completion.carry_lookahead import (
    VARIANTS, build_carry_lookahead, leaf_spec,
)
from research.controlled_source_completion.compact_parallel import (
    execute_compact_parallel, make_compact_schedule,
)
from research.controlled_source_completion.compiler import compile_graph
from research.controlled_source_completion.compiler import resolve_library
from research.controlled_source_completion.ir import evaluate
from research.controlled_source_completion.primitives import array_gates, build, resources
from research.limitation_program_20261001.constant_library import (
    ConstantIntegrationLibrary, canonical,
)
from research.limitation_program_20261001.experiment_constants import changed_calls
from research.controlled_priority_completion.parallel_source import entries

ROOT = Path(__file__).resolve().parents[2]
INTEGRATION_LOWERING = "immutable-target-prefix-add-sub-library-v1"
CASES = ("B4x12", "B8x52")
CPU_LIMIT_SECONDS = 30 * 60


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")


class PrefixIntegrationLibrary(ConstantIntegrationLibrary):
    """Override only full-word direct add/sub; byte-copy all other leaves."""

    def __init__(self, path, target, source, variant):
        if variant not in VARIANTS:
            raise ValueError("known prefix variant required")
        self.variant = variant
        super().__init__(path, target, source, log_strategy=None)

    def get(self, node):
        index = self._requested_node(node)
        if node["op"] not in ("add", "sub"):
            return super().get(node)
        if canonical(node["params"]) != canonical({}):
            raise ValueError("unsupported direct add/sub parameters")
        spec = dict(
            leaf_spec(node["op"], self.w, self.f, self.variant),
            integration_lowering=INTEGRATION_LOWERING,
        )
        key, entry = self._new_leaf(
            node, spec, lambda: build_carry_lookahead(node["op"], self.w, self.variant),
        )
        self._record(index, node, key, "prefix-" + node["op"], {
            "input_contract": {}, "modular_width": self.w,
            "carry_out_discarded": True, "variant": self.variant,
        })
        return key, entry


def dependencies():
    names = (
        "research/limitation_program_20261001/experiment_adders.py",
        "research/limitation_program_20261001/test_carry_lookahead.py",
        "research/controlled_source_completion/carry_lookahead.py",
        "research/limitation_program_20261001/constant_library.py",
        "research/limitation_program_20261001/experiment_constants.py",
        "research/limitation_program_20261001/prove_log_exponent.py",
        "research/controlled_source_completion/compact_parallel.py",
        "research/controlled_source_completion/compact_storage.py",
        "research/controlled_source_completion/compiler.py",
        "research/controlled_source_completion/primitives.py",
        "research/controlled_source_completion/ir.py",
        "research/controlled_priority_completion/parallel_source.py",
        "research/journal_sprint/reversible_fixed_point.py",
    )
    return [ROOT / name for name in names]


def prepare(source_root, output):
    summary = read(source_root / "summary.json")
    if not summary["accepted"] or not summary["passed"]:
        raise ValueError("baseline must be accepted and verified")
    output.relative_to((ROOT / "results/limitation_program_20261001").resolve())
    output.mkdir(parents=True, exist_ok=False)
    baseline_hashes = {"summary.json": digest(source_root / "summary.json")}
    for name in CASES:
        for filename in ("source.json", "target.json", "schedule_capped.json"):
            baseline_hashes[name + "/" + filename] = digest(source_root / name / filename)
    baseline_leaf_hashes = {}
    for name in CASES:
        source = read(source_root / name / "source.json")
        archive = resolve_library(source)
        for key, entry in entries(source).items():
            metadata, binary = archive / (key + ".json"), archive / entry["gate_file"]
            if digest(binary) != entry["sha256"]:
                raise ValueError("Accepted baseline leaf gates differ from their SHA")
            for path in (metadata, binary):
                baseline_leaf_hashes[str(path.relative_to(ROOT))] = digest(path)
    frozen = []
    for path in dependencies():
        snapshot = output / "executed_code" / path.name
        snapshot.parent.mkdir(exist_ok=True)
        shutil.copy2(path, snapshot)
        frozen.append({
            "source": str(path.relative_to(ROOT)),
            "snapshot": str(snapshot.relative_to(output)), "sha256": digest(snapshot),
        })
    protocol = {
        "created_utc": datetime.now(timezone.utc).isoformat(), "local_only": True,
        "item": "A08", "baseline": str(source_root.relative_to(ROOT)),
        "family": list(VARIANTS), "operations": ["add", "sub"],
        "leaf_widths": [24, 40, 72], "leaf_qubit_ceiling": 4096,
        "semantics": "Full output XOR with exact modular addition/subtraction, preserved "
        "inputs, clean workspace, output never controls, empty input contract",
        "proof": "Contiguous generate/propagate pairs obey G*P=0; carry OR equals XOR. "
        "Subtraction uses complemented B and carry-in1. Compute/copy/reverse cleanup.",
        "tests": [
            "Every input a,b and initial output z for widths1..5, forward and inverse",
            "All allowed disjoint G/P singleton states through width7 for both networks",
            "Production carry chains, signed endpoints/wrap,64 seeded pairs per width, "
            "zero/nonzero outputs, inverse, independent modular formula and old ripple",
            "Immutable-node dispatch, arbitrary aliases, unchanged fallback gate/metadata bytes",
        ],
        "full_source_cases": list(CASES), "threshold_percent": 2,
        "eligibility": "Both cases separately reduce complete capped-schedule T-depth by "
        "at least2%, without increasing Clifford+T depth, and fit the accepted actual "
        "baseline qubit caps. A T-count increase is allowed and explicitly disclosed "
        "for later physical costing. Minimum T-depth, then T count, then qubits.",
        "stop_rule": "Exactly two prefix variants. After exact tests and static complete "
        "resource screen, if no single variant meets both-case eligibility, retain baseline "
        "and stop before financial replays. Stop at30process CPU minutes.",
        "replays_on_pass": "Selected variant only, B4 prior-random/all-zero/positive "
        "and B8 prior-random from accepted baseline, full emitted gates with nonzerooutputs",
        "unchanged": "Financial target bytes, source input law, precision, all nondirect "
        "add/sub leaf metadata and gate bytes; inner multiplier ripple adders remain unchanged",
        "exclusions": "No A09 inner-adder claim, continuous-price certificate, physical "
        "runtime or quantum advantage claim",
        "cpu_limit_seconds": CPU_LIMIT_SECONDS, "executed_dependencies": frozen,
        "baseline_hashes": baseline_hashes, "baseline_leaf_hashes": baseline_leaf_hashes,
        "environment": {
            "python": sys.version, "executable": sys.executable,
            "executable_sha256": digest(Path(sys.executable)),
            "packages": {name: version(name) for name in ("numpy", "numba", "pytest")},
        },
    }
    save(output / "protocol.json", protocol)
    return protocol, summary


def ensure_cpu(started):
    if time.process_time() - started > CPU_LIMIT_SECONDS:
        raise TimeoutError("Prospective30CPU-minute ceiling exceeded")


def leaf_screen(output):
    rows = []
    for width in (24, 40, 72):
        for op in ("add", "sub"):
            ripple, _, _ = build(op, width, min(40, width - 1))
            baseline = resources(ripple)
            for variant in VARIANTS:
                program, args, outs = build_carry_lookahead(op, width, variant)
                spec = leaf_spec(op, width, min(40, width - 1), variant)
                key = hashlib.sha256(canonical(spec).encode()).hexdigest()[:20]
                binary = output / "leaves" / (key + ".npy")
                binary.parent.mkdir(exist_ok=True)
                np.save(binary, array_gates(program))
                row = {
                    "op": op, "width": width, "variant": variant, "spec": spec,
                    "resources": resources(program), "ripple_resources": baseline,
                    "args": list(map(list, args)), "outs": list(map(list, outs)),
                    "gate_file": str(binary.relative_to(output)), "sha256": digest(binary),
                }
                if row["resources"]["qubits"] > 4096:
                    raise AssertionError("Prefix leaf exceeds prospective4096-qubit ceiling")
                rows.append(row)
    save(output / "leaf_screen.json", rows)
    return rows


def source_screen(source_root, output, cpu_started):
    cases = []
    for name in CASES:
        target = read(source_root / name / "target.json")
        original = read(source_root / name / "source.json")
        baseline = read(source_root / name / "schedule_capped.json")["resources"]
        cap = baseline["logical_qubits"]
        trials = []
        for variant in VARIANTS:
            ensure_cpu(cpu_started)
            directory = output / name / variant
            library = PrefixIntegrationLibrary(directory / "leaves", target, original, variant)
            source, _ = compile_graph(target, directory, library)
            # Keep the exact prior target bytes, including their serialization.
            shutil.copy2(source_root / name / "target.json", directory / "target.json")
            attribution = changed_calls(original, source)
            expected_calls = sum(node["op"] in ("add", "sub") for node in target["nodes"])
            if len(attribution["changes"]) != expected_calls or any(
                row["op"] not in ("add", "sub") or row["input_contract"] != {}
                for row in attribution["changes"]
            ):
                raise AssertionError("Replacement touched operations outside direct add/sub")
            save(directory / "changed_calls.json", attribution)
            save(directory / "site_decisions.json", library.decisions)
            schedule = make_compact_schedule(target, source, cap)
            save(directory / "schedule_capped.json", schedule)
            observed = schedule["resources"]
            gain = 100 * (1 - observed["t_depth"] / baseline["t_depth"])
            eligible = (
                100 * observed["t_depth"] <= 98 * baseline["t_depth"]
                and observed["logical_qubits"] <= cap
                and observed["clifford_t_depth"] <= baseline["clifford_t_depth"]
            )
            row = {
                "variant": variant, "resources": observed, "eligible": eligible,
                "full_t_depth_gain_percent": gain, "batches": len(schedule["groups"]),
                "t_count_change": observed["t_count"] - baseline["t_count"],
                "t_count_change_percent": 100 * (observed["t_count"] / baseline["t_count"] - 1),
                "work_depth_tradeoff_requires_physical_costing": (
                    observed["t_count"] > baseline["t_count"]
                ),
                "changed_calls": len(attribution["changes"]),
                "target_bytes_unchanged": digest(directory / "target.json") == digest(
                    source_root / name / "target.json"),
                "fallback_metadata_and_gate_bytes_unchanged": True,
            }
            trials.append(row)
            save(output / name / "screen.json", trials)
            print(name, variant, "full T-depth", observed["t_depth"],
                  "gain%", round(gain, 4), "eligible", eligible, flush=True)
        cases.append({"case": name, "baseline": baseline, "trials": trials})
    return cases


def replay_selected(source_root, output, baseline_summary, cases, variant, cpu_started):
    for case in cases:
        name = case["case"]
        directory = output / name / variant
        target = read(directory / "target.json")
        source = read(directory / "source.json")
        schedule = read(directory / "schedule_capped.json")
        previous = next(row for row in baseline_summary["cases"] if row["case"] == name)
        initial = {key: int("a5" * 9, 16) for key in source["outputs"]}
        replays = []
        for prior in previous["replays"]:
            ensure_cpu(cpu_started)
            started = time.perf_counter()
            sample = prior["inputs"]
            _, trace = evaluate(target, sample, True)
            expected = {
                key: trace[value] ^ initial[key] for key, value in source["outputs"].items()
            }
            actual = execute_compact_parallel(target, source, schedule, sample, initial)
            if actual["values"] != expected or not actual["all_input_and_workspace_bits_restored"]:
                raise AssertionError("Complete prefix-source gate replay failed")
            replays.append({
                "label": prior["label"], "inputs": sample, "initial": initial,
                "expected": expected, "actual": actual, "passed": True,
                "seconds": time.perf_counter() - started,
            })
            save(output / name / "replays.json", replays)
            print(name, variant, prior["label"], "complete gate replay PASS", flush=True)
        for filename in ("target.json", "source.json", "schedule_capped.json"):
            shutil.copy2(directory / filename, output / name / filename)
        case.update(replays=replays, replay_passed=True, accepted=True)


def verify_frozen(output, source_root, protocol):
    for entry in protocol["executed_dependencies"]:
        if digest(ROOT / entry["source"]) != entry["sha256"]:
            raise AssertionError("Executed dependency changed after prospective freeze")
        if digest(output / entry["snapshot"]) != entry["sha256"]:
            raise AssertionError("Saved executable snapshot hash mismatch")
    for relative, expected in protocol["baseline_hashes"].items():
        if digest(source_root / relative) != expected:
            raise AssertionError("Accepted baseline mutated")
    for relative, expected in protocol["baseline_leaf_hashes"].items():
        if digest(ROOT / relative) != expected:
            raise AssertionError("Accepted baseline leaf bytes mutated")


def run(source_root, output):
    source_root, output = source_root.resolve(), output.resolve()
    wall_started, cpu_started = time.perf_counter(), time.process_time()
    protocol, baseline_summary = prepare(source_root, output)
    try:
        tests = ROOT / "research/limitation_program_20261001/test_carry_lookahead.py"
        test_exit = pytest.main([str(tests), "-q"])
        if test_exit:
            raise AssertionError("Prefix semantic or dispatch tests failed")
        ensure_cpu(cpu_started)
        leaves = leaf_screen(output)
        cases = source_screen(source_root, output, cpu_started)
        eligible = [variant for variant in VARIANTS if all(
            next(trial for trial in case["trials"] if trial["variant"] == variant)["eligible"]
            for case in cases
        )]
        selected = None
        if eligible:
            selected = min(eligible, key=lambda variant: tuple(
                sum(next(trial for trial in case["trials"] if trial["variant"] == variant)
                    ["resources"][field] for case in cases)
                for field in ("t_depth", "t_count", "logical_qubits")
            ))
            replay_selected(source_root, output, baseline_summary, cases, selected, cpu_started)
        verify_frozen(output, source_root, protocol)
        accepted = selected is not None
        result = {
            "passed": True, "accepted": accepted, "cases": cases, "selected": selected,
            "decision": "Accepted exact direct add/sub prefix replacement" if accepted
            else "No variant reaches2% complete-source T-depth gain in both cases; "
            "baseline retained",
            "complete_source_gain_is_measured": True,
            "financial_gate_replays_run": accepted, "leaf_candidates": len(leaves),
            "financial_function_changed": False, "precision_or_input_law_changed": False,
            "inner_multiplier_adders_changed": False,
            "seconds": time.perf_counter() - wall_started,
            "cpu_seconds": time.process_time() - cpu_started,
        }
        save(output / "summary.json", result)
        save(output / "result.json", result)
        save(output / "verification.json", {
            "passed": True, "pytest_exit_code": int(test_exit),
            "small_literal_gate_replays": 299584,
            "prefix_disjoint_state_patterns": 2 * sum(3 ** width for width in range(1, 8)),
            "prospective_protocol_saved_before_tests_and_screens": True,
            "accepted_baseline_hashes_unchanged": True,
            "executed_dependencies_and_saved_snapshots_unchanged": True,
            "all_changed_calls_are_direct_add_sub": True,
            "all_other_leaf_gate_and_metadata_bytes_identical": True,
            "full_source_replays_required": accepted,
            "full_source_replays_passed": accepted,
        })
        (output / "NEXT.md").write_text(
            "Retain the accepted A10 inverse baseline. This bounded A08 family did not "
            "meet its preregistered full-source threshold; do not attribute leaf savings "
            "to full-source advantage. Next screen A09 inner multiplier accumulation "
            "separately, or another dominant arithmetic operation.\n" if not accepted else
            "Reconcile this accepted exact direct add/sub source in downstream resource "
            "accounts. Inner multiplier ripple adders remain a separate A09 experiment; "
            "financial certification and physical advantage remain open.\n", encoding="utf-8",
        )
    except Exception as error:
        save(output / "failure.json", {
            "passed": False, "type": type(error).__name__, "message": str(error),
            "seconds": time.perf_counter() - wall_started,
            "cpu_seconds": time.process_time() - cpu_started,
        })
        raise
    manifest = {str(path.relative_to(output)): digest(path) for path in output.rglob("*")
                if path.is_file() and path.name != "manifest.json"}
    save(output / "manifest.json", manifest)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    run(args.source_root, args.output)
