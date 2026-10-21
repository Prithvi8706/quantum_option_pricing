"""Recompile full graphs with carry-save multiplication under archived qubit caps."""

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from research.controlled_source_completion.carry_save_multiplier import LOWERING, build_multiplier
from research.controlled_source_completion.budget_schedule import make_budget_schedule
from research.controlled_source_completion.compiler import compile_graph
from research.controlled_source_completion.ir import evaluate
from research.controlled_source_completion.primitives import array_gates, resources
from research.controlled_priority_completion.parallel_source import make_schedule, execute
from research.limitation_audit_20261001.experiment_lookup import (
    ARCHIVE, LookupOnlyLibrary, digest, dump,
)


class CarrySaveLibrary(LookupOnlyLibrary):
    """Explicit alternative backend; default compact multiplier is still available."""

    def get(self, node):
        if node["op"] != "mul":
            return super().get(node)
        spec = dict(op="mul", width=self.w, fraction=self.f, lowering=LOWERING)
        key = hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest()[:20]
        if key not in self.entries:
            p, args, outs = build_multiplier(self.w, self.f)
            binary = self.path / (key + ".npy")
            np.save(binary, array_gates(p))
            entry = dict(key=key, op="mul", params={}, lowering=LOWERING,
                         args=list(map(list, args)), outs=list(map(list, outs)),
                         resources=resources(p), gate_file=binary.name,
                         sha256=digest(binary), table_bits=0)
            dump(self.path / (key + ".json"), entry)
            self.entries[key] = entry
        return key, self.entries[key]


def run(source_root, output):
    output.mkdir(parents=True, exist_ok=False)
    dump(output / "protocol.json", dict(
        input_source=str(source_root), changed="Multiplier only; exact signed fixed-point law",
        budget="Each original Stage A unlimited-wave logical-qubit count is a hard cap",
        selection="Minimum emitted wave T-depth among parallel limits 1..64,128,256,None "
        "and memory-capped first-fit batches",
        acceptance="Signed leaf correctness, clean full-source replay, lower scheduled "
        "depth without exceeding the declared logical-qubit cap",
        excluded="No factory, routing, measurement, rotation or price-estimator latency claim",
    ))
    rows = []
    for case in ("B4x12", "B8x52"):
        target = json.loads((source_root / case / "target.json").read_text())
        old_source = json.loads((source_root / case / "source.json").read_text())
        library = CarrySaveLibrary(output / "leaves", target, old_source)
        source, _ = compile_graph(target, output / case, library)
        archived = json.loads((ARCHIVE / case / "schedule_all.json").read_text())["resources"]
        previous = json.loads((source_root / case / "schedule_all.json").read_text())["resources"]
        cap = archived["logical_qubits"]
        tested, best = [], None
        for limit in [*range(1, 65), 128, 256, None]:
            schedule = make_schedule(source, limit)
            r = schedule["resources"]
            tested.append(dict(limit=limit, qubits=r["logical_qubits"], t_depth=r["t_depth"],
                               t_count=r["t_count"], within_cap=r["logical_qubits"] <= cap))
            if r["logical_qubits"] <= cap and (
                    best is None or r["t_depth"] < best["resources"]["t_depth"]):
                best = schedule
            if limit is None:
                dump(output / case / "schedule_all.json", schedule)
        uniform_best_depth = best["resources"]["t_depth"] if best else None
        packed = make_budget_schedule(source, cap)
        if best is None or packed["resources"]["t_depth"] < best["resources"]["t_depth"]:
            best = packed
        assert best is not None
        dump(output / case / "schedule_capped.json", best)
        row = dict(case=case, archived_baseline=archived, lookup_only_baseline=previous,
                   candidate=best["resources"], chosen_parallel_limit=best["parallel_limit"],
                   chosen_packing=best.get("packing"), uniform_limit_best_depth=uniform_best_depth,
                   faster_at_same_cap=best["resources"]["t_depth"] < previous["t_depth"],
                   tested_schedules=tested, qubit_cap=cap,
                   source_target_sha256=digest(source_root / case / "target.json"))
        dump(output / case / "comparison.json", row)
        print(case, "capped T-depth", previous["t_depth"], "->",
              best["resources"]["t_depth"], "qubits", best["resources"]["logical_qubits"],
              "limit", best["parallel_limit"], flush=True)
        rng = np.random.default_rng(20261004)
        inputs = {n["params"]["name"]: int(rng.integers(0, 2**32)) for n in source["inputs"]}
        initial = {name: int("a5" * 9, 16) for name in source["outputs"]}
        _, trace = evaluate(target, inputs, True)
        expected = {name: trace[v] ^ initial[name] for name, v in source["outputs"].items()}
        actual = execute(source, best, inputs, initial)
        assert actual["values"] == expected and actual["all_input_and_workspace_bits_restored"]
        row["gate_replay"] = dict(inputs=inputs, initial=initial, expected=expected,
                                  actual=actual, passed=True)
        dump(output / case / "comparison.json", row)
        rows.append(row)
        print(case, "complete capped circuit replay PASS", flush=True)
    dump(output / "summary.json", dict(cases=rows, passed=True,
         disposition="Keep explicit carry-save backend and capped schedules. The leaf "
         "uses more workspace, so it is not an unconditional replacement at all budgets."))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.source_root, args.output)
