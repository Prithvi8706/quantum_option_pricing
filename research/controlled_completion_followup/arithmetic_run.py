"""Compile, execute and recost the exact multiplier redesign; preserve old evidence."""

import json
import time
from pathlib import Path

from research.controlled_completion_followup.truncated_multiplier import TruncatedLibrary
from research.controlled_source_completion.compiler import compile_graph, execute, resolve_library
from research.controlled_source_completion.ir import evaluate
from research.controlled_source_completion.run import dump

OLD = Path("results/controlled_source_completion")
ROOT = Path("results/controlled_completion_followup/arithmetic_v1")


def main():
    rows = []
    basis = json.loads((OLD / "validation_v2/full_source_basis.json").read_text())
    for f, names in ((24, ("C4", "H8")), (40, ("C4", "H8")), (64, ("phase",))):
        # Phase64 was emitted into compile_v2's separate library.
        example = json.loads(
            (OLD / "compile_v2" / ("%s_f%d" % (names[0], f)) / "source.json").read_text()
        )
        base = resolve_library(example)
        lib = TruncatedLibrary(ROOT / ("leaves_f%d" % f), f + 32, f, {}, base)
        for name in names:
            tag = "%s_f%d" % (name, f)
            data = json.loads((OLD / "compile_v2" / tag / "target.json").read_text())
            tic = time.perf_counter()
            manifest, lib = compile_graph(data, ROOT / "compile_v2" / tag, lib)
            if name == "phase":
                inputs = dict(Y=-17 << f, left=-1 << f, scale_exponent=4)
            else:
                inputs = next(
                    c["inputs"] for c in basis if c["model"] == name and c["fraction_bits"] == f
                )
            _, trace = evaluate(data, inputs, True)
            initial = {key: 0xA5 for key in data["outputs"]}
            got = execute(manifest, inputs, initial)
            expected = {key: trace[value] ^ initial[key] for key, value in data["outputs"].items()}
            assert got["values"] == expected and got["workspace_clean"] and got["inputs_preserved"]
            old = json.loads((OLD / "compile_v2" / tag / "source.json").read_text())["resources"]
            row = dict(
                model=name,
                fraction_bits=f,
                resources=manifest["resources"],
                previous_resources=old,
                basis_inputs=inputs,
                basis_validation=got,
                t_count_reduction=old["t_count"] / manifest["resources"]["t_count"],
                t_depth_reduction=old["t_depth"] / manifest["resources"]["t_depth"],
                seconds=time.perf_counter() - tic,
                interpretation=(
                    "Same digital target and estimator; executed emitted gates, nonzero XOR "
                    "output and complete cleanup. This is a quantum circuit improvement only."
                ),
            )
            rows.append(row)
            dump(ROOT / "summary.json", rows)
            print(
                json.dumps(
                    {
                        k: row[k]
                        for k in (
                            "model",
                            "fraction_bits",
                            "t_count_reduction",
                            "t_depth_reduction",
                            "seconds",
                        )
                    }
                ),
                flush=True,
            )
    from research.controlled_source_completion import cost, fusion_validation

    cost.ROOT = ROOT
    cost.main("v2", 64, True)
    dump(ROOT / "validation_v2/full_source_basis.json", basis)
    fusion_validation.ROOT = ROOT
    fusion_validation.main()


if __name__ == "__main__":
    main()
