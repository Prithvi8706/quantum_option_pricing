"""Prospective A19 prerequisite: exact B2 reference and native leaf bindings."""

# Exact prospective protocol descriptions remain readable receipt literals.
# ruff: noqa: E501

import argparse
from datetime import datetime, timezone
from pathlib import Path
import shutil
import sys

import pytest

from research.controlled_priority_completion.parallel_source import entries
from research.controlled_source_completion.compiler import resolve_library
from research.limitation_program_20261001.constant_library import digest
from research.limitation_program_20261001.experiment_checkpoint import (
    CASE,
    PROGRAM,
    manifest,
    read,
    relative,
    save,
    verify,
)
from research.limitation_program_20261001.progress import ROOT
from research.limitation_program_20261001.streaming_reference import (
    build_reference,
    compile_reference,
)
from research.limitation_program_20261001.streaming_scope import build_streaming_scope


def run(output):
    output.relative_to(PROGRAM.resolve())
    assert not output.exists()
    output.mkdir()
    frozen, dependencies = {}, []
    for name in (
        "streaming_reference.py",
        "streaming_scope.py",
        "test_streaming_scope.py",
        "experiment_streaming_reference.py",
    ):
        p = ROOT / "research/limitation_program_20261001" / name
        frozen[relative(p)] = digest(p)
        snapshot = output / "executed_code" / name
        snapshot.parent.mkdir(exist_ok=True)
        shutil.copy2(p, snapshot)
        dependencies.append(
            dict(
                source=relative(p),
                snapshot=snapshot.relative_to(output).as_posix(),
                sha256=digest(p),
            )
        )
    # Frozen previous portfolio dependencies remain unchanged; include their map.
    old = read(PROGRAM / "A10_coefficient_run001/protocol.json")
    frozen.update(
        {str(Path(k)).replace("\\", "/"): v for k, v in old["baseline_leaf_hashes"].items()}
    )
    for name in ("source.json", "target.json", "schedule_capped.json"):
        frozen[relative(CASE / name)] = digest(CASE / name)
    for row in old["executed_dependencies"]:
        frozen[str(Path(row["source"])).replace("\\", "/")] = row["sha256"]
    for name in ("experiment_checkpoint.py", "progress.py"):
        p = ROOT / "research/limitation_program_20261001" / name
        frozen[relative(p)] = digest(p)
    for name in (
        "research/advantage_frontier_20260923/barrier_oracle_depth.py",
        "research/controlled_source_completion/ir.py",
        "research/controlled_source_completion/finance.py",
        "research/controlled_source_completion/optimize.py",
        "research/controlled_source_completion/compiler.py",
        "research/controlled_source_completion/primitives.py",
        "research/controlled_source_completion/compact_parallel_v7.py",
    ):
        frozen[name] = digest(ROOT / name)
    source = read(CASE / "source.json")
    library = resolve_library(source)
    for key, entry in entries(source).items():
        for p in (library / (key + ".json"), library / entry["gate_file"]):
            frozen[relative(p)] = digest(p)
    protocol = dict(
        local_only=True,
        created_utc=datetime.now(timezone.utc).isoformat(),
        item="A19 exact B2x4 reference prerequisite",
        before_reference_emission_and_tests=True,
        assets=2,
        dates=4,
        word_width=72,
        fraction_bits=40,
        uniform_bits=32,
        source_selection="Use only previously accepted native kernels after whole original target binding and actual B2-site guard validation; minimum frozen T-depth/T-count/qubits/key, otherwise full native generic fallback",
        checkpoint_candidates_executed=0,
        full_financial_gate_replays=0,
        scope="One original financial template, six clean Gaussian pair boundaries, four date increment/stock/basket boundaries and unchanged final rounding chain",
        frozen_inputs=frozen,
        executed_dependencies=dependencies,
        python=sys.version,
    )
    save(output / "protocol.json", protocol)
    verify(protocol)
    rc = pytest.main(
        [
            str(ROOT / "research/limitation_program_20261001/test_streaming_scope.py"),
            "-q",
            "-p",
            "no:cacheprovider",
            "--junitxml=" + str(output / "tests.xml"),
        ]
    )
    if rc:
        save(output / "failed_tests.json", dict(passed=False, return_code=int(rc)))
        manifest(output, protocol)
        raise AssertionError("Frozen exact streaming reference tests failed")
    original, target, semantics = build_reference()
    save(output / "original_target.json", original)
    save(output / "target.json", target)
    save(output / "semantics.json", semantics)
    source, report = compile_reference(target, output / "compiled")
    save(output / "source.json", source)
    save(output / "reference_compilation.json", report)
    scope = build_streaming_scope(target, source, semantics)
    save(output / "scope.json", scope)
    save(
        output / "summary.json",
        dict(
            passed=True,
            local_only=True,
            harness="B2x4",
            nodes=len(target["nodes"]),
            values=source["values"],
            uniform_registers=len(source["inputs"]),
            gaussian_pairs=len(scope["gaussian_pairs"]),
            dates=len(scope["date_bindings"]),
            native_reuse_counts=report["reuse_counts"],
            checkpoint_candidates_executed=0,
            full_financial_gate_replays=0,
            whole_original_target_guards_preserved=True,
            G2_to_G5="open",
        ),
    )
    manifest(output, protocol)
    print(
        "Exact B2x4 reference source and stage boundaries frozen",
        report["reuse_counts"],
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.output.resolve())
