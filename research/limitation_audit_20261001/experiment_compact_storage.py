"""Measure and replay exact storage packing on both full Stage A graphs."""

import argparse
import json
from pathlib import Path

import numpy as np

from research.controlled_source_completion.compact_storage import (
    compact_plan, execute_compact, narrow_comparison,
)
from research.controlled_source_completion.ir import evaluate
from research.controlled_source_completion.primitives import build, resources
from research.limitation_audit_20261001.experiment_lookup import dump


def run(source_root, output):
    output.mkdir(parents=True, exist_ok=False)
    rows = []
    for case in ("B4x12", "B8x52"):
        target = json.loads((source_root / case / "target.json").read_text())
        source = json.loads((source_root / case / "source.json").read_text())
        plan = compact_plan(target, source)
        dump(output / case / "plan.json", plan)
        rng = np.random.default_rng(20261002)
        inputs = {n["params"]["name"]: int(rng.integers(0, 2**n["params"]["bits"]))
                  for n in source["inputs"]}
        initial = {name: int("a5" * 9, 16) for name in source["outputs"]}
        _, values = evaluate(target, inputs, True)
        assert all(value & ~mask == 0 for value, mask in zip(values, plan["proof_masks"]))
        actual = execute_compact(target, source, plan, inputs, initial)
        assert actual["inputs_and_workspace_restored"]
        assert actual["values"] == {name: values[v] ^ initial[name]
                                    for name, v in source["outputs"].items()}
        row = dict(case=case, baseline_serial_qubits=source["resources"]["logical_qubits"],
                   compact_serial_qubits=plan["logical_qubits"],
                   retained_before=source["values"] * source["word_width"],
                   retained_after=plan["retained_ssa_qubits"],
                   t_count_unchanged=plan["t_count"], widths=plan["width_histogram"],
                   copies_before=plan["baseline_argument_and_output_copy_cx"],
                   copies_after=plan["argument_and_output_copy_cx"],
                   replay=dict(inputs=inputs, initial=initial, actual=actual, passed=True))
        dump(output / case / "comparison.json", row)
        rows.append(row)
        print(case, row["baseline_serial_qubits"], "->", row["compact_serial_qubits"],
              "full gate replay PASS", flush=True)
    dump(output / "summary.json", dict(cases=rows, passed=True,
         standalone_comparison=dict(baseline=resources(build("lt", 72, 40)[0]),
                                    candidate=resources(narrow_comparison(72)[0])),
         scope="Exact serial storage and argument-copy reduction; no parallel-depth or "
         "physical-routing claim. All arithmetic values retain their original precision."))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.source_root, args.output)
