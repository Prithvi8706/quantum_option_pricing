"""Compile range-certified multipliers, then execute the emitted wave schedule."""

import hashlib
import json
from pathlib import Path
import time

from research.compound_feasibility.model import MODELS
from research.controlled_priority_completion.parallel_source import execute, make_schedule
from research.controlled_priority_completion.range_audit import ranges_for_compiled
from research.controlled_priority_completion.ranged_multiplier import RangedLibrary
from research.controlled_source_completion.compiler import compile_graph, resolve_library
from research.controlled_source_completion.ir import evaluate
from research.controlled_source_completion.run import dump


BASE = Path("results/controlled_completion_followup/arithmetic_v1/compile_v2")
ROOT = Path("results/controlled_priority_completion")


def main():
    basis = json.loads(
        Path(
            "results/controlled_source_completion/validation_v2/full_source_basis.json"
        ).read_text()
    )
    rows = []
    for model in (MODELS[0], MODELS[3]):
        tag = model.name + "_f40"
        old = json.loads((BASE / tag / "source.json").read_text())
        data = json.loads((BASE / tag / "target.json").read_text())
        certificate = ranges_for_compiled(data, model)
        assert certificate["guaranteed"] and not certificate["signed_overflow_sites"]
        directory = ROOT / "range_compile_v1" / tag
        dump(directory / "range_certificate.json", certificate)
        library = RangedLibrary(
            ROOT / "range_compile_v1/leaves_f40",
            72,
            40,
            data["tables"],
            resolve_library(old),
            certificate["bounds"],
        )
        started = time.perf_counter()
        source, _ = compile_graph(data, directory, library)
        inputs = next(
            c["inputs"] for c in basis if c["model"] == model.name and c["fraction_bits"] == 40
        )
        initial = {key: 0xA5 for key in data["outputs"]}
        _, values = evaluate(data, inputs, True)
        expected = {key: values[value] ^ initial[key] for key, value in data["outputs"].items()}
        schedules = []
        for limit in (1, 8, 32, 128, None):
            schedule = make_schedule(source, limit)
            schedule.update(
                source_manifest=(directory / "source.json").as_posix(),
                source_sha256=hashlib.sha256((directory / "source.json").read_bytes()).hexdigest(),
                range_certificate=(directory / "range_certificate.json").as_posix(),
                range_certificate_sha256=hashlib.sha256(
                    (directory / "range_certificate.json").read_bytes()
                ).hexdigest(),
            )
            dump(ROOT / "range_parallel_v1" / (tag + "_limit_%s.json" % (limit or "all")), schedule)
            row = dict(
                model=model.name,
                parallel_limit=limit,
                resources=schedule["resources"],
                groups=len(schedule["groups"]),
                t_reduction=old["resources"]["t_count"] / schedule["resources"]["t_count"],
                depth_reduction=old["resources"]["t_depth"] / schedule["resources"]["t_depth"],
                logical_qubit_ratio=schedule["resources"]["logical_qubits"]
                / old["resources"]["logical_qubits"],
            )
            if limit is None:
                got = execute(source, schedule, inputs, initial)
                assert got["values"] == expected and got["all_input_and_workspace_bits_restored"]
                row["basis_execution"] = dict(**got, inputs=inputs, expected=expected)
            schedules.append(row)
            print(
                json.dumps(
                    {
                        k: row[k]
                        for k in (
                            "model",
                            "parallel_limit",
                            "groups",
                            "t_reduction",
                            "depth_reduction",
                            "logical_qubit_ratio",
                        )
                    }
                ),
                flush=True,
            )
        rows.append(
            dict(
                model=model.name,
                compile_and_check_cpu_seconds=time.perf_counter() - started,
                schedules=schedules,
                original_resources=old["resources"],
                source_resources=source["resources"],
            )
        )
        dump(ROOT / "range_parallel_v1/summary.json", rows)


if __name__ == "__main__":
    main()
