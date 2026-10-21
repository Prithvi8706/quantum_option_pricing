"""Freeze conservative exact normal-radius ranges without changing a circuit."""

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import random
import shutil
import subprocess
import sys
import time

from research.controlled_source_completion.ir import evaluate
from research.limitation_program_20261001.interval_bounds import bound_graph
from research.limitation_program_20261001.progress import ROOT


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def run(source_root, output):
    source_root, output = source_root.resolve(), output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    dependencies = [
        Path(__file__),
        ROOT / "research/limitation_program_20261001/interval_bounds.py",
        ROOT / "research/limitation_program_20261001/test_interval_bounds.py",
        ROOT / "research/limitation_program_20261001/prove_log_exponent.py",
        ROOT / "research/controlled_source_completion/ir.py",
    ]
    snapshots = output / "executed_code"
    snapshots.mkdir()
    frozen = []
    for path in dependencies:
        destination = snapshots / path.name
        shutil.copy2(path, destination)
        frozen.append(
            dict(
                source=str(path.relative_to(ROOT)),
                snapshot=str(destination.relative_to(output)),
                sha256=sha(destination),
            )
        )
    targets = {case: sha(source_root / case / "target.json") for case in ("B4x12", "B8x52")}
    protocol = dict(
        created_utc=datetime.now(timezone.utc).isoformat(),
        local_only=True,
        items=["A07", "A11"],
        source_root=str(source_root.relative_to(ROOT)),
        target_sha256=targets,
        executed_dependencies=frozen,
        environment=dict(
            python=sys.version,
            executable=sys.executable,
            executable_sha256=sha(Path(sys.executable)),
        ),
        method="Conservative exact signed-integer interval propagation, "
        "overflow fallback, same-SSA MSB normalization and bin-local refinement",
        test_vectors="Exhaustive small signed words/fractions and refinement "
        "negative controls; prior financial vectors, zero/max and 8 seeded "
        "uniform patterns per case, integer trace only",
        acceptance="All tested traces enclosed at every SSA value; each current "
        "radius input/output has a nonnegative strict subword bound",
        exclusions="No leaf emission, SSA packing change, gate replay, "
        "circuit gain or continuous-price certificate",
    )
    save(output / "protocol.json", protocol)
    started = time.perf_counter()
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            str(dependencies[2]),
            "-q",
            "--junitxml=" + str(output / "regression.xml"),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    (output / "test_output.txt").write_text(completed.stdout + completed.stderr, encoding="utf-8")
    if completed.returncode:
        save(
            output / "summary.json",
            dict(passed=False, stage="interval validation", test_returncode=completed.returncode),
        )
        print(completed.stdout + completed.stderr, flush=True)
        raise RuntimeError("interval tests failed; preparation retained")
    summary = read(source_root / "summary.json")
    cases = []
    for case in ("B4x12", "B8x52"):
        target = read(source_root / case / "target.json")
        bounds, rules = bound_graph(target)
        radii = []
        for index, node in enumerate(target["nodes"]):
            if node["op"] != "sqrt":
                continue
            operand, result = node["args"][0], node["out"][0]
            in_bounds, out_bounds = bounds[operand], bounds[result]
            if min(in_bounds + out_bounds) < 0:
                raise AssertionError("radius bound remained signed/unknown")
            radii.append(
                dict(
                    node_index=index,
                    input_value=operand,
                    output_value=result,
                    input_bounds=in_bounds,
                    output_bounds=out_bounds,
                    input_unsigned_bits=max(1, in_bounds[1].bit_length()),
                    output_unsigned_bits=max(1, out_bounds[1].bit_length()),
                )
            )
        previous = next(row for row in summary["cases"] if row["case"] == case)
        samples = [row["inputs"] for row in previous["replays"]]
        inputs = [node for node in target["nodes"] if node["op"] == "input"]
        samples += [
            {node["params"]["name"]: value for node in inputs} for value in (0, (1 << 32) - 1)
        ]
        generator = random.Random(20261002)
        samples += [
            {
                node["params"]["name"]: generator.getrandbits(node["params"]["bits"])
                for node in inputs
            }
            for _ in range(8)
        ]
        width, checked = target["width"], 0
        for sample in samples:
            _, trace = evaluate(target, sample, True)
            for value, raw in enumerate(trace):
                value_signed = raw - (1 << width) if raw & (1 << (width - 1)) else raw
                lo, hi = bounds[value]
                if not lo <= value_signed <= hi:
                    raise AssertionError((case, value, value_signed, bounds[value], rules[value]))
                checked += 1
        save(
            output / (case + "_bounds.json"),
            dict(
                target_sha256=targets[case],
                intervals={str(v): list(pair) for v, pair in bounds.items()},
                rules={str(v): rule for v, rule in rules.items()},
                sqrt_sites=radii,
            ),
        )
        result = dict(
            case=case,
            sqrt_sites=len(radii),
            maximum_input_unsigned_bits=max(row["input_unsigned_bits"] for row in radii),
            maximum_output_unsigned_bits=max(row["output_unsigned_bits"] for row in radii),
            rule_counts=dict(Counter(rules.values())),
            sampled_trace_values_checked=checked,
            samples=len(samples),
            passed=True,
        )
        cases.append(result)
        print(
            case,
            "radius input/output active bits",
            result["maximum_input_unsigned_bits"],
            result["maximum_output_unsigned_bits"],
            "sites",
            len(radii),
            flush=True,
        )
    save(
        output / "summary.json",
        dict(
            passed=True,
            cases=cases,
            integrated=False,
            seconds=time.perf_counter() - started,
            decision="Exact interval proof component; no resource improvement adopted",
        ),
    )
    (output / "NEXT.md").write_text(
        "# Next bounded action\n\nIndependently review these static integer bounds. "
        "If sound, emit a narrowed square-root leaf under a versioned same-target "
        "unsigned-range contract, retain a generic fallback and screen full source "
        "costs. The bounds do not measure an unbuilt circuit or continuous-law error.\n",
        encoding="utf-8",
    )
    files = {
        str(path.relative_to(ROOT)): sha(path)
        for path in sorted(output.rglob("*"))
        if path.is_file()
    }
    save(
        output / "manifest.json",
        dict(
            files=files,
            frozen_inputs={
                str((source_root / case / "target.json").relative_to(ROOT)): value
                for case, value in targets.items()
            },
            manifest_self_hash_excluded=True,
        ),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    run(args.source_root, args.output)
