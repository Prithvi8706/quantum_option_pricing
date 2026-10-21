"""Compare exact ln(2) leaves and full memory-capped arithmetic sources locally."""

import argparse
import hashlib
import json
import shutil
import time
from pathlib import Path

import numpy as np

from research.controlled_priority_completion.parallel_source import execute
from research.controlled_source_completion.budget_schedule import make_budget_schedule
from research.controlled_source_completion.compiler import compile_graph, resolve_library
from research.controlled_source_completion.constant_multiplier import (
    LOWERING, STRATEGIES, build_constant_multiplier, has_zero_low_proof,
)
from research.controlled_source_completion.ir import evaluate
from research.controlled_source_completion.primitives import Library, array_gates, resources
from research.limitation_audit_20261001.experiment_lookup import digest, dump, signature


COEFFICIENT = 762123384786


class ConstantLibrary(Library):
    """Copy all other leaves unchanged; specialize only statically proved calls."""

    def __init__(self, path, target, source, strategy, coefficient=COEFFICIENT):
        super().__init__(path, target["width"], target["fraction_bits"], target["tables"])
        self.archive = resolve_library(source)
        self.strategy, self.coefficient = strategy, coefficient
        self.producers = {v: node for node in target["nodes"] for v in node["out"]}
        self.original, self.proofs = {}, []
        nodes = [node for node in target["nodes"] if node["op"] != "input"]
        assert len(nodes) == len(source["forward_calls"])
        for node, call in zip(nodes, source["forward_calls"]):
            assert (node["args"], node["out"]) == (call["args"], call["out"])
            sig = signature(node)
            if sig in self.original:
                assert self.original[sig] == call["leaf"]
            self.original[sig] = call["leaf"]

    def get(self, node):
        eligible = (node["params"].get("c") == self.coefficient and self.f < self.w
                    and has_zero_low_proof(node, self.producers, self.f))
        if not eligible:
            key = self.original[signature(node)]
            if key not in self.entries:
                entry = json.loads((self.archive / (key + ".json")).read_text())
                assert digest(self.archive / entry["gate_file"]) == entry["sha256"]
                for name in (key + ".json", entry["gate_file"]):
                    destination = self.path / name
                    if destination.exists():
                        assert digest(destination) == digest(self.archive / name)
                    else:
                        shutil.copy2(self.archive / name, destination)
                self.entries[key] = entry
            return key, self.entries[key]
        producer = self.producers[node["args"][0]]
        self.proofs.append(dict(output=node["out"], argument=node["args"][0],
                                producer_output=producer["out"], producer_params=producer["params"],
                                theorem="Left-shifted bit extraction has zero low fraction bits",
                                zero_low_bits=self.f))
        spec = dict(op="cmul", width=self.w, fraction_bits=self.f, coefficient=self.coefficient,
                    zero_bits=self.f, strategy=self.strategy, lowering=LOWERING)
        key = hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest()[:20]
        if key not in self.entries:
            meta, binary = self.path / (key + ".json"), self.path / (key + ".npy")
            if meta.exists() and binary.exists():
                entry = json.loads(meta.read_text())
                if digest(binary) != entry["sha256"] or entry["spec"] != spec:
                    raise ValueError("constant leaf cache mismatch")
            else:
                p, args, outs = build_constant_multiplier(
                    self.w, self.f, self.coefficient, self.f, self.strategy,
                )
                np.save(binary, array_gates(p))
                entry = dict(key=key, op="cmul", params={"c": self.coefficient}, spec=spec,
                             input_contract={"zero_low_bits": self.f},
                             args=list(map(list, args)), outs=list(map(list, outs)),
                             resources=resources(p), gate_file=binary.name,
                             sha256=digest(binary), table_bits=0)
                dump(meta, entry)
            self.entries[key] = entry
        return key, self.entries[key]


def leaf_rows():
    rows = []
    from research.controlled_source_completion.primitives import build
    old = build("cmul", 72, 40, {"c": COEFFICIENT})[0]
    for strategy in STRATEGIES:
        new = build_constant_multiplier(72, 40, COEFFICIENT, 40, strategy)[0]
        rows.append(dict(strategy=strategy, baseline=resources(old), candidate=resources(new)))
        print(strategy, resources(new), flush=True)
    return rows


def run(source_root, output):
    output.mkdir(parents=True, exist_ok=False)
    dump(output / "protocol.json", dict(
        source_root=str(source_root), changed="Only proved ln(2) cmul leaf calls",
        coefficient=COEFFICIENT, width=72, fraction_bits=40,
        domain="Input low40 bits are zero, proved by the same SSA graph",
        unchanged="Every financial IR node/table/input and all other leaf gate bytes",
        comparison="Four arithmetic candidates and a fixed-batch control, followed by "
        "repacking at exactly the previous logical-qubit caps",
        selection="Lowest whole-source capped T-depth, then T count, then logical qubits",
        acceptance="Independent signed integer tests; proof guard and cache tests; "
        "full emitted source forward/output XOR/inverse with nonzero outputs",
        exclusions="No estimator, physical runtime, continuous-price or advantage claim",
        producer_sha256=digest(Path(__file__)),
    ))
    leaves = leaf_rows()
    dump(output / "leaves.json", leaves)
    cases = []
    for case in ("B4x12", "B8x52"):
        original = source_root / case
        target = json.loads((original / "target.json").read_text())
        old_source = json.loads((original / "source.json").read_text())
        baseline = json.loads((original / "schedule_capped.json").read_text())
        cap = baseline["resources"]["logical_qubits"]
        trials = []
        for strategy in STRATEGIES:
            library = ConstantLibrary(output / "leaves", target, old_source, strategy)
            source, _ = compile_graph(target, output / case / strategy, library)
            assert library.proofs
            dump(output / case / strategy / "input_proofs.json", library.proofs)
            schedule = make_budget_schedule(source, cap)
            assert schedule["resources"]["logical_qubits"] <= cap
            dump(output / case / strategy / "schedule_capped.json", schedule)
            # Matched fixed batches isolate arithmetic from scheduling effects.
            fixed = sum(2 * max(library.entries[source["forward_calls"][i]["leaf"]]
                                ["resources"]["t_depth"] for i in group["call_indices"])
                        for group in baseline["groups"])
            row = dict(strategy=strategy, candidate=schedule["resources"],
                       proved_calls=len(library.proofs), fixed_batch_t_depth=fixed,
                       repacked_t_depth=schedule["resources"]["t_depth"], qubit_cap=cap)
            trials.append(row)
            print(case, strategy, "depth", row["repacked_t_depth"], "qubits",
                  row["candidate"]["logical_qubits"], flush=True)
        best = min(trials, key=lambda r: (r["repacked_t_depth"], r["candidate"]["t_count"],
                                          r["candidate"]["logical_qubits"]))
        path = output / case / best["strategy"]
        source = json.loads((path / "source.json").read_text())
        schedule = json.loads((path / "schedule_capped.json").read_text())
        result = dict(case=case, baseline=baseline["resources"], best=best, all_candidates=trials,
                      original_target_sha256=digest(original / "target.json"),
                      original_source_sha256=digest(original / "source.json"), replays=[])
        dump(output / case / "comparison.json", result)
        assert best["repacked_t_depth"] < baseline["resources"]["t_depth"]
        # Reuse previous random financial input to isolate the changed source,
        # plus the two uniform-register endpoints for the smaller case.
        previous = json.loads((original / "comparison.json").read_text())["gate_replay"]
        samples = [("previous_random", previous["inputs"])]
        names = [n["params"]["name"] for n in source["inputs"]]
        if case == "B4x12":
            samples += [("all_zero", dict.fromkeys(names, 0)),
                        ("all_maximum", dict.fromkeys(names, 2**32 - 1))]
        initial = {name: int("a5" * 9, 16) for name in source["outputs"]}
        proved_args = [proof["argument"] for proof in json.loads((path / "input_proofs.json").read_text())]
        for label, inputs in samples:
            started = time.perf_counter()
            _, trace = evaluate(target, inputs, True)
            assert all(trace[arg] & ((1 << 40) - 1) == 0 for arg in proved_args)
            negative = sum(bool(trace[arg] & (1 << 71)) for arg in proved_args)
            expected = {name: trace[v] ^ initial[name] for name, v in source["outputs"].items()}
            actual = execute(source, schedule, inputs, initial)
            assert actual["values"] == expected and actual["all_input_and_workspace_bits_restored"]
            result["replays"].append(dict(label=label, inputs=inputs, initial=initial,
                                          expected=expected, actual=actual, negative_operands=negative,
                                          seconds=time.perf_counter() - started, passed=True))
            dump(output / case / "comparison.json", result)
            print(case, label, "complete gate replay PASS", "negative operands", negative, flush=True)
        cases.append(result)
    dump(output / "summary.json", dict(leaves=leaves, cases=cases, passed=True,
        disposition="Retain the chosen exact specialized leaves and guarded local library. "
        "The general multiplier is retained for inputs lacking the zero-low proof."))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    run(args.source_root, args.output)
