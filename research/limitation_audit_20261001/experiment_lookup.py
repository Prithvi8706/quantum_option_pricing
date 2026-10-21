"""Measure exact QROM replacement, preserving every other archived leaf.

Run with the pinned environment, from the repository root:
    python -m research.limitation_audit_20261001.experiment_lookup --output <new-dir>
"""

import argparse
import hashlib
import json
import shutil
import time
from pathlib import Path

import numpy as np

from research.controlled_priority_completion.parallel_source import make_schedule
from research.controlled_priority_completion.parallel_source import execute as wave_execute
from research.controlled_source_completion.compiler import compile_graph, resolve_library
from research.controlled_source_completion.ir import coefficients, evaluate
from research.controlled_source_completion.primitives import Library, basis_run, build, resources


ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "results/frontier_completion_20260927/stage_a"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def signature(node):
    return json.dumps([node["op"], node["params"]], sort_keys=True)


class LookupOnlyLibrary(Library):
    """Replace lookup; copy and hash-check the precise other archived leaves."""

    def __init__(self, path, target, source):
        super().__init__(path, target["width"], target["fraction_bits"], target["tables"])
        self.archive = resolve_library(source)
        self.original = {}
        nodes = [n for n in target["nodes"] if n["op"] != "input"]
        assert len(nodes) == len(source["forward_calls"])
        for node, call in zip(nodes, source["forward_calls"]):
            assert (node["args"], node["out"]) == (call["args"], call["out"])
            if node["op"] == "lookup":
                continue
            sig = signature(node)
            if sig in self.original:
                assert self.original[sig] == call["leaf"]
            self.original[sig] = call["leaf"]

    def get(self, node):
        if node["op"] == "lookup":
            return super().get(node)
        key = self.original[signature(node)]
        if key not in self.entries:
            entry = json.loads((self.archive / (key + ".json")).read_text())
            binary = self.archive / entry["gate_file"]
            assert digest(binary) == entry["sha256"]
            for name in (key + ".json", entry["gate_file"]):
                destination = self.path / name
                if destination.exists():
                    assert digest(destination) == digest(self.archive / name)
                else:
                    shutil.copy2(self.archive / name, destination)
            self.entries[key] = entry
        return key, self.entries[key]


def leaf_experiments():
    rows = []
    for name, size, degree in (("log", 32, 8), ("atan", 32, 8),
                               ("cos", 64, 7), ("cdf", 256, 7)):
        table = coefficients(name, size, degree, 40)
        bits = size.bit_length() - 1
        new, args, outs = build("lookup", 72, 40, {"bits": bits}, table)
        old, _, _ = build("lookup", 72, 40,
                          {"bits": bits, "lookup_strategy": "equality"}, table)
        initial = [int("a5" * 9, 16) ^ i for i in range(degree + 1)]
        mask = (1 << 72) - 1
        for index in range(size):
            expected = [(value & mask) ^ x for value, x in zip(table[index], initial)]
            actual, clean, preserved, _ = basis_run(new, args, outs, [index], initial)
            assert (actual, clean, preserved) == (expected, True, True)
            restored, clean, preserved, _ = basis_run(new, args, outs, [index], actual, True)
            assert (restored, clean, preserved) == (initial, True, True)
        baseline, candidate = resources(old), resources(new)
        assert candidate["qubits"] <= baseline["qubits"]
        assert candidate["t_count"] < baseline["t_count"]
        rows.append(dict(name=name, rows=size, columns=degree + 1, width=72,
                         every_address_and_inverse_passed=True,
                         baseline=baseline, candidate=candidate))
        print(name, baseline["t_count"], "->", candidate["t_count"], flush=True)
    return rows


def source_experiment(case, output):
    original_path = ARCHIVE / case
    original = json.loads((original_path / "source.json").read_text())
    target = json.loads((original_path / "target.json").read_text())
    library = LookupOnlyLibrary(output / "leaves", target, original)
    source, _ = compile_graph(target, output / case, library)
    schedules, comparisons = {}, {}
    for label, limit in (("all", None), ("128", 128), ("32", 32)):
        baseline = json.loads((original_path / ("schedule_" + label + ".json")).read_text())
        schedule = make_schedule(source, limit)
        schedules[label] = schedule
        comparisons[label] = {"baseline": baseline["resources"],
                              "candidate": schedule["resources"]}
        dump(output / case / ("schedule_" + label + ".json"), schedule)
    result = dict(case=case, source_sha256=digest(original_path / "source.json"),
                  target_sha256=digest(original_path / "target.json"),
                  serial={"baseline": original["resources"], "candidate": source["resources"]},
                  schedules=comparisons, replays=[])
    dump(output / case / "comparison.json", result)
    # Replay the actual emitted complete wave circuit, not only its IR.
    rng = np.random.default_rng(20261001)
    names = [n["params"]["name"] for n in source["inputs"]]
    samples = [dict(zip(names, map(int, rng.integers(0, 2**32, len(names)))))]
    if case == "B4x12":
        samples += [dict.fromkeys(names, 0), dict.fromkeys(names, 2**32 - 1)]
    initial = {"Y": int("a5" * 9, 16)}
    for index, inputs in enumerate(samples):
        started = time.perf_counter()
        _, trace = evaluate(target, inputs, True)
        expected = {name: trace[value] ^ initial[name] for name, value in target["outputs"].items()}
        actual = wave_execute(source, schedules["all"], inputs, initial)
        assert actual["values"] == expected and actual["all_input_and_workspace_bits_restored"]
        result["replays"].append(dict(inputs=inputs, initial=initial, expected=expected,
                                      actual=actual, seconds=time.perf_counter() - started))
        dump(output / case / "comparison.json", result)
        print(case, "gate replay", index, "PASS", flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    protocol = dict(unchanged="72-bit words, 40 fraction bits, every financial IR node, "
                    "all non-lookup gate bytes, exact 7T CCX decomposition",
                    baseline="Archived Stage A equality scan",
                    acceptance="Exact XOR and clean workspace on all leaf addresses; "
                    "complex-state unit test; lower T cost without extra leaf workspace",
                    source_scope="Arithmetic source only; no estimator or hardware speed claim",
                    source_code_sha256=digest(Path(__file__)))
    dump(args.output / "protocol.json", protocol)
    leaves = leaf_experiments()
    dump(args.output / "leaves.json", leaves)
    cases = [source_experiment(case, args.output) for case in ("B4x12", "B8x52")]
    dump(args.output / "summary.json", dict(leaves=leaves, cases=cases, passed=True))


if __name__ == "__main__":
    main()
