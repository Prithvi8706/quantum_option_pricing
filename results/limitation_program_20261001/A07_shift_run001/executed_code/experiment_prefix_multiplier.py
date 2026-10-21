"""Bounded exact signed-complement CSA/prefix multiplication integration.

The arithmetic family changes signed partial encoding and its final adder.
It does not attribute measured gains to either component without an ablation.
Only mul leaves change; accepted baseline bytes and progress remain untouched.
"""
from __future__ import annotations

import argparse
import copy
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

from research.controlled_priority_completion.parallel_source import entries
from research.controlled_source_completion.carry_lookahead import VARIANTS
from research.controlled_source_completion.carry_save_multiplier import build_multiplier
from research.controlled_source_completion.compact_parallel import (
    execute_compact_parallel, make_compact_schedule,
)
from research.controlled_source_completion.compiler import compile_graph, resolve_library
from research.controlled_source_completion.ir import evaluate
from research.controlled_source_completion.prefix_multiplier import (
    build_prefix_multiplier, leaf_spec, signed_partial_terms,
)
from research.controlled_source_completion.primitives import array_gates, resources
from research.limitation_program_20261001.constant_library import (
    ConstantIntegrationLibrary, actual_resources, canonical, digest,
)
from research.limitation_program_20261001.experiment_constants import changed_calls

ROOT = Path(__file__).resolve().parents[2]
CASES = ("B4x12", "B8x52")
CPU_LIMIT_SECONDS = 30 * 60
INTEGRATION_LOWERING = "immutable-target-signed-csa-prefix-multiplier-v1"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n", encoding="utf-8")


class PrefixMultiplierIntegrationLibrary(ConstantIntegrationLibrary):
    """Unpromised full-word multiplier, omitting input_contract in metadata."""

    def __init__(self, path, target, source, variant):
        if variant not in VARIANTS:
            raise ValueError("known prefix variant required")
        self.variant = variant
        super().__init__(path, target, source, log_strategy=None)

    def _validate_multiplier_metadata(self, key, node, spec, entry, binary):
        if (
            entry.get("key") != key or canonical(entry.get("spec")) != canonical(spec)
            or "input_contract" in entry or "input_contract" in entry.get("spec", {})
            or entry.get("op") != "mul"
            or canonical(entry.get("params")) != canonical(node["params"])
            or entry.get("gate_file") != binary.name
        ):
            raise ValueError("prefix multiplier cache metadata/spec/contract mismatch")
        self._validate_entry_shape(key, entry)

    def _new_multiplier_leaf(self, node, spec):
        key = hashlib.sha256(canonical(spec).encode()).hexdigest()[:20]
        metadata, binary = self.path / (key + ".json"), self.path / (key + ".npy")
        cached = self._cached_entry(key)
        if cached is not None:
            self._validate_multiplier_metadata(key, node, spec, cached, binary)
            return key, cached
        if metadata.exists() != binary.exists():
            raise ValueError("incomplete prefix multiplier cache")
        if metadata.exists():
            entry = read(metadata)
            self._validate_multiplier_metadata(key, node, spec, entry, binary)
            if digest(binary) != entry.get("sha256"):
                raise ValueError("prefix multiplier cache gate SHA mismatch")
            gates = np.load(binary, allow_pickle=False)
            observed = actual_resources(gates, entry["resources"]["qubits"])
            if any(entry["resources"].get(field) != value for field, value in observed.items()):
                raise ValueError("prefix multiplier cache resource mismatch")
        else:
            program, arguments, outputs = build_prefix_multiplier(self.w, self.f, self.variant)
            np.save(binary, array_gates(program))
            entry = {
                "key": key, "op": "mul", "params": copy.deepcopy(node["params"]),
                "spec": copy.deepcopy(spec),
                "args": list(map(list, arguments)), "outs": list(map(list, outputs)),
                "resources": resources(program), "gate_file": binary.name,
                "sha256": digest(binary), "table_bits": 0,
            }
            save(metadata, entry)
        self._remember_entry(key, entry)
        return key, entry

    def get(self, node):
        index = self._requested_node(node)
        if node["op"] != "mul":
            return super().get(node)
        if canonical(node["params"]) != canonical({}):
            raise ValueError("unsupported multiplication parameters")
        spec = dict(
            leaf_spec(self.w, self.f, self.variant),
            integration_lowering=INTEGRATION_LOWERING,
        )
        key, entry = self._new_multiplier_leaf(node, spec)
        self._record(index, node, key, "prefix-multiplier", {
            "width": self.w, "fraction_bits": self.f, "product_width": self.w + self.f,
            "variant": self.variant, "all_signed_input_patterns_permitted": True,
            "signed_partial_rule": spec["signed_partial_rule"],
            "negative_bit_encoding": spec["negative_bit_encoding"],
            "discarded_low_columns": spec["discarded_low_columns"],
        })
        return key, entry


def dependencies():
    return [ROOT / name for name in (
        "research/limitation_program_20261001/experiment_prefix_multiplier.py",
        "research/limitation_program_20261001/test_prefix_multiplier.py",
        "research/limitation_program_20261001/test_prefix_integration.py",
        "research/controlled_source_completion/prefix_multiplier.py",
        "research/controlled_source_completion/carry_lookahead.py",
        "research/controlled_source_completion/carry_save_multiplier.py",
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
    )]


def prepare(source_root, output):
    summary = read(source_root / "summary.json")
    if not summary["accepted"] or not summary["passed"]:
        raise ValueError("verified accepted source baseline required")
    output.relative_to((ROOT / "results/limitation_program_20261001").resolve())
    output.mkdir(parents=True, exist_ok=False)
    baseline_hashes = {"summary.json": digest(source_root / "summary.json")}
    baseline_leaves = {}
    for name in CASES:
        for filename in ("target.json", "source.json", "schedule_capped.json"):
            baseline_hashes[name + "/" + filename] = digest(source_root / name / filename)
        source = read(source_root / name / "source.json")
        archive = resolve_library(source)
        for key, entry in entries(source).items():
            metadata, binary = archive / (key + ".json"), archive / entry["gate_file"]
            if digest(binary) != entry["sha256"]:
                raise ValueError("baseline leaf SHA mismatch")
            for path in (metadata, binary):
                baseline_leaves[str(path.relative_to(ROOT))] = digest(path)
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
        "item": "A09", "baseline": str(source_root.relative_to(ROOT)),
        "family": list(VARIANTS), "width": 72, "fraction_bits": 40,
        "product_width": 112, "input_contract_metadata": "omitted, no input promise",
        "semantics": "All signed pairs; arbitrary output XOR of floor(a*b/2^f)mod2^w, "
        "inputs preserved, zero scratch and inverse correct",
        "proof": "Exactly-one-sign partial bits have negative weight; complement them "
        "and insert -sumnegative2^column modulo2^(w+f) into CSA. Keep all discarded-low "
        "columns through CSA and prefix carry. Extract bits[f:f+w].",
        "changes": "Joint signed-partial encoding/correction and final prefix addition "
        "inside variable multiplication. Attribution to the final adder alone is unproved.",
        "tests": [
            "Widths 1..5, all f 0..w and signed pairs, zero/nonzero outputs and both directions",
            "Exhaustive mathematical signed partial/correction theorem and "
            "low-carry negative controls",
            "72/f40 signed endpoints, low-column carries, single bits,64 seeded pairs, "
            "zero/nonzero outputs, inverse, independent Python floor and old CSA equivalence",
            "Independent integration suite: repeated args, square inputs without specialization, "
            "aliases, fallback byte identity, archived executor, immutable target "
            "and cache corruption",
        ],
        "threshold_percent": 2, "cases": list(CASES),
        "eligibility": "A single variant must reduce complete capped-source T-depth by "
        "at least 2% in both cases, CT depth<=baseline and logical qubits<=current actual caps. "
        "Extra T work is allowed and disclosed for physical costing.",
        "selection": "Minimum sum of both-case T-depth, then T count and actual qubits",
        "replays_on_pass": "Best eligible variant only; B4 previous random/all-zero/positive "
        "and B8 previous random positive from accepted baseline, nonzero outputs and full cleanup",
        "stop_rule": "Two variants only; failed semantic candidate is not adopted. "
        "No financial replay if both-case threshold fails; initial 30 process CPU minutes.",
        "cpu_limit_seconds": CPU_LIMIT_SECONDS,
        "unchanged": "Financial target bytes/input law/precision and every non-mul leaf "
        "metadata/gate byte; dedicated A08 prefix builder and all original modules",
        "exclusions": "No square specialization, changed input promise, precision/law "
        "change, continuous-price certificate, physical timing or quantum advantage claim",
        "executed_dependencies": frozen, "baseline_hashes": baseline_hashes,
        "baseline_leaf_hashes": baseline_leaves,
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
    baseline = resources(build_multiplier(72, 40)[0])
    rows = []
    for variant in VARIANTS:
        program, args, outs = build_prefix_multiplier(72, 40, variant)
        spec = leaf_spec(72, 40, variant)
        key = hashlib.sha256(canonical(spec).encode()).hexdigest()[:20]
        binary = output / "leaves" / (key + ".npy")
        binary.parent.mkdir(exist_ok=True)
        np.save(binary, array_gates(program))
        terms, correction = signed_partial_terms(72, 40)
        row = {
            "variant": variant, "spec": spec, "resources": resources(program),
            "baseline_resources": baseline,
            "args": list(map(list, args)), "outs": list(map(list, outs)),
            "gate_file": str(binary.relative_to(output)), "sha256": digest(binary),
            "partial_term_count": len(terms),
            "negative_partial_count": sum(negative for _, _, _, negative in terms),
            "modular_correction": correction,
            "correction_columns": [column for column in range(112)
                                   if (correction >> column) & 1],
        }
        rows.append(row)
        print("leaf", variant, "T-depth", row["resources"]["t_depth"],
              "T count", row["resources"]["t_count"],
              "qubits", row["resources"]["qubits"], flush=True)
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
            library = PrefixMultiplierIntegrationLibrary(
                directory / "leaves", target, original, variant,
            )
            source, _ = compile_graph(target, directory, library)
            shutil.copy2(source_root / name / "target.json", directory / "target.json")
            attribution = changed_calls(original, source)
            expected_calls = sum(node["op"] == "mul" for node in target["nodes"])
            metadata = entries(source)
            if len(attribution["changes"]) != expected_calls or any(
                row["op"] != "mul" or "input_contract" in metadata[row["new_key"]]
                for row in attribution["changes"]
            ):
                raise AssertionError("Only unpromised mul leaves may change")
            save(directory / "changed_calls.json", attribution)
            save(directory / "site_decisions.json", library.decisions)
            try:
                schedule = make_compact_schedule(target, source, cap)
            except ValueError as error:
                row = {"variant": variant, "eligible": False, "reason": str(error)}
            else:
                save(directory / "schedule_capped.json", schedule)
                observed = schedule["resources"]
                eligible = (
                    100 * observed["t_depth"] <= 98 * baseline["t_depth"]
                    and observed["logical_qubits"] <= cap
                    and observed["clifford_t_depth"] <= baseline["clifford_t_depth"]
                )
                row = {
                    "variant": variant, "resources": observed, "eligible": eligible,
                    "full_t_depth_gain_percent": 100 * (1 - observed["t_depth"]
                                                       / baseline["t_depth"]),
                    "t_count_change": observed["t_count"] - baseline["t_count"],
                    "t_count_change_percent": 100 * (observed["t_count"]
                                                    / baseline["t_count"] - 1),
                    "work_depth_tradeoff_requires_physical_costing": (
                        observed["t_count"] > baseline["t_count"]
                    ),
                    "batches": len(schedule["groups"]),
                    "changed_calls": len(attribution["changes"]),
                    "target_bytes_unchanged": digest(directory / "target.json") == digest(
                        source_root / name / "target.json"),
                    "fallback_metadata_and_gate_bytes_unchanged": True,
                }
                print(name, variant, "T-depth", observed["t_depth"],
                      "gain%", round(row["full_t_depth_gain_percent"], 4),
                      "eligible", eligible, flush=True)
            trials.append(row)
            save(output / name / "screen.json", trials)
        cases.append({"case": name, "baseline": baseline, "trials": trials,
                      "accepted": False, "replay_passed": False, "replays": []})
    return cases


def replay(source_root, output, baseline_summary, cases, variant, cpu_started):
    for case in cases:
        name = case["case"]
        directory = output / name / variant
        target = read(directory / "target.json")
        source = read(directory / "source.json")
        schedule = read(directory / "schedule_capped.json")
        selected = next(row for row in case["trials"] if row["variant"] == variant)
        case.update(selected=selected, candidate=selected["resources"])
        prior = next(row for row in baseline_summary["cases"] if row["case"] == name)
        initial = {key: int("a5" * 9, 16) for key in source["outputs"]}
        for sample in prior["replays"]:
            ensure_cpu(cpu_started)
            started = time.perf_counter()
            inputs = sample["inputs"]
            _, trace = evaluate(target, inputs, True)
            expected = {
                key: trace[value] ^ initial[key] for key, value in source["outputs"].items()
            }
            actual = execute_compact_parallel(target, source, schedule, inputs, initial)
            if actual["values"] != expected or not actual["all_input_and_workspace_bits_restored"]:
                raise AssertionError("Complete financial prefix-multiplier gate replay failed")
            case["replays"].append({
                "label": sample["label"], "inputs": inputs, "initial": initial,
                "expected": expected, "actual": actual, "passed": True,
                "seconds": time.perf_counter() - started,
            })
            save(output / name / "comparison.json", case)
            print(name, variant, sample["label"], "complete gate replay PASS", flush=True)
        for filename in ("target.json", "source.json", "schedule_capped.json"):
            shutil.copy2(directory / filename, output / name / filename)
        case.update(accepted=True, replay_passed=True)
        save(output / name / "comparison.json", case)


def verify_frozen(source_root, output, protocol):
    for entry in protocol["executed_dependencies"]:
        if digest(ROOT / entry["source"]) != entry["sha256"]:
            raise AssertionError("Dependency changed after prospective freeze")
        if digest(output / entry["snapshot"]) != entry["sha256"]:
            raise AssertionError("Executed snapshot hash mismatch")
    for relative, expected in protocol["baseline_hashes"].items():
        if digest(source_root / relative) != expected:
            raise AssertionError("Accepted baseline source/target/schedule mutated")
    for relative, expected in protocol["baseline_leaf_hashes"].items():
        if digest(ROOT / relative) != expected:
            raise AssertionError("Accepted baseline leaf metadata/gates mutated")


def run(source_root, output):
    source_root, output = source_root.resolve(), output.resolve()
    started, cpu_started = time.perf_counter(), time.process_time()
    protocol, baseline_summary = prepare(source_root, output)
    print("Prospective A09 protocol and executable snapshots saved", flush=True)
    try:
        tests = [ROOT / "research/limitation_program_20261001" / filename for filename in
                 ("test_prefix_multiplier.py", "test_prefix_integration.py")]
        exit_code = pytest.main([*(str(path) for path in tests), "-q"])
        if exit_code:
            raise AssertionError("Exact signed multiplier or integration tests failed")
        ensure_cpu(cpu_started)
        leaves = leaf_screen(output)
        cases = source_screen(source_root, output, cpu_started)
        eligible = [variant for variant in VARIANTS if all(
            next(row for row in case["trials"] if row["variant"] == variant)["eligible"]
            for case in cases
        )]
        selected = None
        if eligible:
            selected = min(eligible, key=lambda variant: tuple(
                sum(next(row for row in case["trials"] if row["variant"] == variant)
                    ["resources"][field] for case in cases)
                for field in ("t_depth", "t_count", "logical_qubits")
            ))
            replay(source_root, output, baseline_summary, cases, selected, cpu_started)
        for case in cases:
            if selected is None:
                save(output / case["case"] / "comparison.json", case)
        verify_frozen(source_root, output, protocol)
        ensure_cpu(cpu_started)
        accepted = selected is not None and all(case["accepted"] for case in cases)
        result = {
            "passed": True, "accepted": accepted, "selected": selected, "cases": cases,
            "decision": "Accepted exact signed-complement CSA/prefix multiplier" if accepted
            else "No both-case2% complete-source candidate; accepted inverse baseline retained",
            "complete_source_gain_is_measured": True,
            "financial_gate_replays_run": selected is not None,
            "leaf_candidates": len(leaves), "financial_function_changed": False,
            "precision_or_input_law_changed": False, "input_promise_added": False,
            "square_specialization": False,
            "attribution": "Joint signed partial encoding/correction and prefix final adder",
            "seconds": time.perf_counter() - started,
            "cpu_seconds": time.process_time() - cpu_started,
        }
        save(output / "summary.json", result)
        save(output / "result.json", result)
        save(output / "verification.json", {
            "passed": True, "pytest_exit_code": int(exit_code),
            "small_literal_gate_replays": 61888,
            "widths": list(range(1, 6)), "fractions": "all0..w",
            "independent_integration_test_cases": 16,
            "prospective_protocol_before_tests_and_screens": True,
            "executed_dependencies_and_snapshots_unchanged": True,
            "accepted_baseline_and_leaf_hashes_unchanged": True,
            "only_unpromised_mul_leaves_change": True,
            "nonmul_metadata_and_gate_bytes_identical": True,
            "full_financial_replays_required": selected is not None,
            "full_financial_replays_passed": accepted,
        })
        (output / "NEXT.md").write_text(
            "Reconcile the accepted exact signed-complement CSA/prefix multiplier. "
            "Next bound the remaining dominant square-root/shift or specialize proven "
            "same-SSA self-products separately. G2 financial error and G3-G5 estimator, "
            "classical and physical accounting remain open.\n" if accepted else
            "Retain the accepted inverse-ln2 baseline. This two-variant multiplication "
            "family failed its complete-source threshold; preserve exact leaf components "
            "and move to the next bounded dominant-operation screen.\n", encoding="utf-8",
        )
    except Exception as error:
        save(output / "failure.json", {
            "passed": False, "type": type(error).__name__, "message": str(error),
            "seconds": time.perf_counter() - started,
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
