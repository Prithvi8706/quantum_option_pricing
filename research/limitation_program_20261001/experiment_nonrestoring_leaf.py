"""Finite prospective exact non-restoring root leaf and matched-domain cost screen."""

import argparse
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
from pathlib import Path
import shutil
import sys
import time

import numpy as np
import pytest

from research.controlled_priority_completion.parallel_source import entries
from research.controlled_source_completion.compiler import resolve_library
from research.controlled_source_completion.nonrestoring_sqrt import (
    build_nonrestoring_sqrt,
    input_contract,
    leaf_spec,
)
from research.controlled_source_completion.primitives import array_gates, resources
from research.limitation_program_20261001.constant_library import (
    actual_resources,
    canonical,
    digest,
)
from research.limitation_program_20261001.experiment_prefix_multiplier import ROOT, read, save

BASELINE = ROOT / "results/limitation_program_20261001/A07_shift_run001"
DIMENSIONS = ("t_count", "t_depth", "clifford_t_depth", "qubits")


def baseline_leaf():
    matched = []
    for case in ("B4x12", "B8x52"):
        source = read(BASELINE / case / "source.json")
        archive = resolve_library(source)
        roots = [
            entry
            for entry in entries(source).values()
            if entry["op"] == "sqrt" and entry.get("input_contract") == input_contract(46)
        ]
        if len(roots) != 1:
            raise ValueError("one accepted unsigned46 root leaf per case required")
        entry = roots[0]
        matched.append((entry, archive / (entry["key"] + ".json"), archive / entry["gate_file"]))
    assert matched[0][0]["sha256"] == matched[1][0]["sha256"]
    assert matched[0][0]["resources"] == matched[1][0]["resources"]
    return matched


def run(output):
    output = output.resolve()
    output.relative_to((ROOT / "results/limitation_program_20261001").resolve())
    assert read(BASELINE / "summary.json")["accepted"]
    matched = baseline_leaf()
    output.mkdir(exist_ok=False)
    dependencies = [
        ROOT / name
        for name in (
            "research/limitation_program_20261001/experiment_nonrestoring_leaf.py",
            "research/controlled_source_completion/nonrestoring_sqrt.py",
            "research/limitation_program_20261001/test_nonrestoring_sqrt.py",
            "research/controlled_source_completion/narrow_sqrt.py",
            "research/controlled_source_completion/primitives.py",
            "research/controlled_source_completion/exact_lookup.py",
            "research/journal_sprint/reversible_fixed_point.py",
            "research/antithetic_feasibility/reversible.py",
            "research/limitation_program_20261001/constant_library.py",
            "research/limitation_program_20261001/experiment_prefix_multiplier.py",
        )
    ]
    frozen, snapshots = {}, []
    for path in dependencies:
        snapshot = output / "executed_code" / path.name
        snapshot.parent.mkdir(exist_ok=True)
        shutil.copy2(path, snapshot)
        frozen[str(path.relative_to(ROOT))] = digest(path)
        snapshots.append(
            dict(
                source=str(path.relative_to(ROOT)),
                snapshot=str(snapshot.relative_to(output)),
                sha256=digest(snapshot),
            )
        )
    for _, metadata, binary in matched:
        for path in (metadata, binary):
            frozen[str(path.relative_to(ROOT))] = digest(path)
    for case in ("B4x12", "B8x52"):
        for name in ("target.json", "source.json", "schedule_capped.json"):
            path = BASELINE / case / name
            frozen[str(path.relative_to(ROOT))] = digest(path)
    frozen[str((BASELINE / "manifest.json").relative_to(ROOT))] = digest(BASELINE / "manifest.json")
    protocol = dict(
        created_utc=datetime.now(timezone.utc).isoformat(),
        local_only=True,
        item="A11 exact non-restoring root leaf",
        before_recorded_tests_and_cost=True,
        candidates=["nonrestoring-signed-remainder"],
        width=72,
        fraction_bits=40,
        active_input_bits=46,
        promise=input_contract(46),
        baseline=str(BASELINE.relative_to(ROOT)),
        baseline_leaf=matched[0][0],
        semantics="Native72 input and arbitrary output XOR isqrt(unsigned(input)<<40). "
        "Input fits unsigned46; top active bit is legal; restore every input/scratch bit.",
        recurrence="For old R>=0: Rnext=4R+digit-(4Q+1); else: "
        "Rnext=4R+digit+(4Q+3); Qnext=2Q+[Rnext>=0].",
        storage="All signed remainder snapshots, root bits, arithmetic work and exact "
        "copy/inverse cleanup counted; only final signed remainders supply sign decisions.",
        required_checks="Exhaust small input/active/fraction widths with dirty output "
        "and inverse; production perfect-square boundaries, zero/max/topbit/seeded values; "
        "native24/40/72 fixtures; exact Python isqrt and archived root equivalence.",
        resource_dimensions=list(DIMENSIONS),
        dominance="Old dominates if all four old dimensions <=candidate and one strictly "
        "less. Equal leaves give no improvement. Source screen additionally requires "
        "Twork or qubits strictly improve, matching the existing clean-leaf source gate.",
        stop_rule="One exact family; no full source if dominated, equal or incapable of "
        "the clean-leaf work/space gate; any semantic failure stops; 30 process CPU minutes.",
        exclusions="No source gain/adoption/financial replay here. Newton approximation, "
        "separate Heston validation and G2-G5 remain open.",
        executed_dependencies=snapshots,
        dependencies=frozen,
        environment=dict(
            python=sys.version,
            executable=sys.executable,
            executable_sha256=digest(Path(sys.executable)),
            packages={n: version(n) for n in ("numpy", "numba", "pytest")},
        ),
    )
    save(output / "protocol.json", protocol)
    print("Prospective non-restoring leaf protocol saved", flush=True)
    wall, cpu = time.perf_counter(), time.process_time()
    try:
        test_exit = pytest.main(
            [
                str(ROOT / "research/limitation_program_20261001/test_nonrestoring_sqrt.py"),
                "-q",
                "--junitxml=" + str(output / "regression.xml"),
            ]
        )
        if test_exit:
            raise AssertionError("Exact non-restoring root tests failed")
        if time.process_time() - cpu > 1800:
            raise TimeoutError("Declared leaf CPU ceiling exceeded")
        program, args, outs = build_nonrestoring_sqrt(72, 40, 46)
        spec = leaf_spec(72, 40, 46)
        key = hashlib.sha256(canonical(spec).encode()).hexdigest()[:20]
        binary = output / (key + ".npy")
        np.save(binary, array_gates(program))
        metadata = dict(
            key=key,
            op="sqrt",
            params={},
            spec=spec,
            input_contract=input_contract(46),
            args=[list(a) for a in args],
            outs=[list(o) for o in outs],
            resources=resources(program),
            gate_file=binary.name,
            sha256=digest(binary),
        )
        save(output / (key + ".json"), metadata)
        old_entry, _, old_binary = matched[0]
        assert digest(old_binary) == old_entry["sha256"]
        actual_old = actual_resources(
            np.load(old_binary, allow_pickle=False), old_entry["resources"]["qubits"]
        )
        assert all(old_entry["resources"][n] == value for n, value in actual_old.items())
        old, new = old_entry["resources"], metadata["resources"]
        dominated = all(old[n] <= new[n] for n in DIMENSIONS) and any(
            old[n] < new[n] for n in DIMENSIONS
        )
        improves = any(new[n] < old[n] for n in DIMENSIONS)
        work_or_space = new["t_count"] < old["t_count"] or new["qubits"] < old["qubits"]
        allowed = not dominated and improves and work_or_space
        result = dict(
            passed=True,
            best=metadata,
            baseline_root=old,
            leaf_nondominated=not dominated,
            any_resource_improvement=improves,
            clean_leaf_work_or_scratch_improved=work_or_space,
            source_screen_allowed=allowed,
            decision="Exact nondominated leaf; proof-dispatched source screen required"
            if allowed
            else "Exact leaf fails matched cost gate; accepted shift source retained",
            same_integer_function_under_unsigned_guard=True,
            source_gain_claimed=False,
            financial_gate_replays_run=False,
            elapsed_seconds=time.perf_counter() - wall,
            cpu_seconds=time.process_time() - cpu,
        )
        save(output / "summary.json", result)
        assert all(digest(ROOT / name) == value for name, value in frozen.items())
        assert read(output / "protocol.json") == protocol
        save(
            output / "verification.json",
            dict(passed=True, pytest_exit_code=int(test_exit), dependencies_unchanged=True),
        )
        (output / "NEXT.md").write_text(
            "Run a fresh proof-dispatched full-source screen only when source_screen_allowed. "
            "Preserve accepted shifts, native copies and unsigned guards. "
            "Reconcile complete cleanup and costs independently; G2-G5 remain open.\n",
            encoding="utf-8",
        )
        print(
            dict(passed=True, source_screen_allowed=allowed, candidate=new, baseline=old),
            flush=True,
        )
    except Exception as error:
        save(
            output / "failure.json", dict(passed=False, type=type(error).__name__, error=str(error))
        )
        raise
    finally:
        files = {
            str(path.relative_to(ROOT)): digest(path)
            for path in output.rglob("*")
            if path.is_file() and path.name != "manifest.json"
        }
        save(output / "manifest.json", dict(files=files, frozen_inputs=frozen))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output)
