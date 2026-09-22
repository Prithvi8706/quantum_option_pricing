"""Emit wave schedules and execute production financial/phase gate programs."""

import hashlib
import json
from pathlib import Path
import time

from research.controlled_priority_completion.parallel_source import execute, make_schedule
from research.controlled_source_completion.ir import evaluate
from research.controlled_source_completion.run import dump

SOURCE = Path("results/controlled_completion_followup/arithmetic_v1/compile_v2")
OUTPUT = Path("results/controlled_priority_completion/parallel_v1")


def main():
    basis = json.loads(
        Path(
            "results/controlled_source_completion/validation_v2/full_source_basis.json"
        ).read_text()
    )
    rows = []
    for tag in ("C4_f40", "H8_f40", "phase_f64"):
        root = SOURCE / tag
        file = root / "source.json"
        source = json.loads(file.read_text())
        data = json.loads((root / "target.json").read_text())
        for limit in (1, 8, 32, 128, None):
            schedule = make_schedule(source, limit)
            schedule.update(
                source_manifest=file.as_posix(),
                source_sha256=hashlib.sha256(file.read_bytes()).hexdigest(),
            )
            name = "%s_limit_%s" % (tag, limit or "all")
            dump(OUTPUT / (name + ".json"), schedule)
            row = dict(
                tag=tag,
                parallel_limit=limit,
                resources=schedule["resources"],
                groups=len(schedule["groups"]),
                depth_improvement=source["resources"]["t_depth"] / schedule["resources"]["t_depth"],
                qubit_ratio=schedule["resources"]["logical_qubits"]
                / source["resources"]["logical_qubits"],
                dependency_only_forward_t_depth=schedule["dependency_only_forward_t_depth"],
            )
            if limit is None:
                if tag == "phase_f64":
                    inputs = dict(Y=-17 << 64, left=-1 << 64, scale_exponent=4)
                else:
                    inputs = next(
                        c["inputs"]
                        for c in basis
                        if c["model"] == tag.split("_")[0] and c["fraction_bits"] == 40
                    )
                initial = {key: 0xA5 for key in data["outputs"]}
                start = time.perf_counter()
                got = execute(source, schedule, inputs, initial)
                _, values = evaluate(data, inputs, True)
                expected = {
                    key: values[value] ^ initial[key] for key, value in data["outputs"].items()
                }
                assert got["values"] == expected and got["all_input_and_workspace_bits_restored"]
                row["execution"] = dict(
                    **got, seconds=time.perf_counter() - start, inputs=inputs, expected=expected
                )
            rows.append(row)
            dump(OUTPUT / "summary.json", rows)
            print(
                json.dumps(
                    {
                        k: row[k]
                        for k in (
                            "tag",
                            "parallel_limit",
                            "groups",
                            "depth_improvement",
                            "qubit_ratio",
                        )
                    }
                ),
                flush=True,
            )


if __name__ == "__main__":
    main()
