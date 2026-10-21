"""Prospective exact signed operand range multiplier leaf screen, entirely local."""

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
from research.controlled_source_completion.range_multiplier import (
    build_range_multiplier,
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

BASELINE = ROOT / "results/limitation_program_20261001/A11_nonrestoring_run001"
ACTIVE_WIDTHS = (24, 40, 72)
PAIRS = tuple((a, b) for a in ACTIVE_WIDTHS for b in ACTIVE_WIDTHS if (a, b) != (72, 72))
DIMENSIONS = ("t_count", "t_depth", "clifford_t_depth", "qubits")


def baseline_leaf():
    matched = []
    for case in ("B4x12", "B8x52"):
        source = read(BASELINE / case / "source.json")
        archive = resolve_library(source)
        leaves = [entry for entry in entries(source).values() if entry["op"] == "mul"]
        if len(leaves) != 1 or leaves[0].get("input_contract"):
            raise ValueError("one accepted unrestricted signed multiplier required")
        entry = leaves[0]
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
    names = (
        "research/limitation_program_20261001/experiment_range_leaf.py",
        "research/controlled_source_completion/range_multiplier.py",
        "research/limitation_program_20261001/test_range_multiplier.py",
        "research/controlled_source_completion/prefix_multiplier.py",
        "research/controlled_source_completion/carry_lookahead.py",
        "research/controlled_source_completion/primitives.py",
        "research/controlled_source_completion/exact_lookup.py",
        "research/journal_sprint/reversible_fixed_point.py",
        "research/antithetic_feasibility/reversible.py",
        "research/limitation_program_20261001/constant_library.py",
        "research/limitation_program_20261001/experiment_prefix_multiplier.py",
    )
    frozen, snapshots = {}, []
    for name in names:
        path = ROOT / name
        snapshot = output / "executed_code" / path.name
        snapshot.parent.mkdir(exist_ok=True)
        shutil.copy2(path, snapshot)
        frozen[name] = digest(path)
        snapshots.append(
            dict(source=name, snapshot=str(snapshot.relative_to(output)), sha256=digest(snapshot))
        )
    for _, metadata, binary in matched:
        for path in (metadata, binary):
            frozen[str(path.relative_to(ROOT))] = digest(path)
    for case in ("B4x12", "B8x52"):
        for name in ("target.json", "source.json", "schedule_capped.json"):
            path = BASELINE / case / name
            frozen[str(path.relative_to(ROOT))] = digest(path)
    for path in (
        BASELINE / "manifest.json",
        ROOT / "results/limitation_program_20261001/A09_range_scope_run001/manifest.json",
    ):
        frozen[str(path.relative_to(ROOT))] = digest(path)
    protocol = dict(
        created_utc=datetime.now(timezone.utc).isoformat(),
        local_only=True,
        item="A09 proved signed operand widths",
        before_recorded_tests_and_cost=True,
        family="signed-range-complement-csa-prefix-final-v1",
        active_widths=list(ACTIVE_WIDTHS),
        candidates=[list(pair) for pair in PAIRS],
        width=72,
        fraction_bits=40,
        source_portfolios=["mixed40", "mixed24-40"],
        baseline=str(BASELINE.relative_to(ROOT)),
        baseline_leaf=matched[0][0],
        semantics="Native two72 inputs, arbitrary72 output XOR floor(signed(a)*signed(b)/2^40) mod2^72; both native inputs are exact sign extensions of their declared active signed widths. Every input and helper is restored.",
        storage="All partials, low carry columns, full112-bit modular sign correction, CSA snapshots, Brent-Kung sum, native output copy and literal inverse counted.",
        required_checks="Exhaust unequal small signed pairs/fractions, dirty output/inverse; production extrema, negative tiny products, seeded values, native24/40/72 and invalid promises.",
        resource_dimensions=list(DIMENSIONS),
        dominance="Old dominates if all four old dimensions<=candidate and one strictly less. Source may use only nondominated leaves with Twork or qubits strictly improved; equal/dominated leaves fall back to archived generic.",
        stop_rule="One exact circuit family, exactly three active production widths, at most two source portfolios; no Karatsuba prototype or additional width search; any semantic failure stops;30 process CPU minutes.",
        exclusions="No financial/source gain or advantage claim at leaf stage; G2-G5 remain open.",
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
    print("Prospective signed range leaf protocol saved", flush=True)
    wall, cpu = time.perf_counter(), time.process_time()
    try:
        test_exit = pytest.main(
            [
                str(ROOT / "research/limitation_program_20261001/test_range_multiplier.py"),
                "-q",
                "--junitxml=" + str(output / "regression.xml"),
            ]
        )
        if test_exit:
            raise AssertionError("Exact signed range multiplier tests failed")
        old_entry, _, old_binary = matched[0]
        actual_old = actual_resources(
            np.load(old_binary, allow_pickle=False), old_entry["resources"]["qubits"]
        )
        assert all(old_entry["resources"][n] == value for n, value in actual_old.items())
        old, candidates = old_entry["resources"], []
        for a_bits, b_bits in PAIRS:
            if time.process_time() - cpu > 1800:
                raise TimeoutError("Declared leaf CPU ceiling exceeded")
            program, args, outs = build_range_multiplier(72, 40, a_bits, b_bits)
            spec = leaf_spec(72, 40, a_bits, b_bits)
            key = hashlib.sha256(canonical(spec).encode()).hexdigest()[:20]
            binary = output / (key + ".npy")
            np.save(binary, array_gates(program))
            metadata = dict(
                key=key,
                op="mul",
                params={},
                spec=spec,
                input_contract=input_contract(a_bits, b_bits),
                args=[list(a) for a in args],
                outs=[list(o) for o in outs],
                resources=resources(program),
                gate_file=binary.name,
                sha256=digest(binary),
            )
            save(output / (key + ".json"), metadata)
            new = metadata["resources"]
            dominated = all(old[n] <= new[n] for n in DIMENSIONS) and any(
                old[n] < new[n] for n in DIMENSIONS
            )
            improves = any(new[n] < old[n] for n in DIMENSIONS)
            work_or_space = new["t_count"] < old["t_count"] or new["qubits"] < old["qubits"]
            candidates.append(
                dict(
                    active_bits=[a_bits, b_bits],
                    metadata=metadata,
                    leaf_nondominated=not dominated,
                    any_resource_improvement=improves,
                    clean_leaf_work_or_scratch_improved=work_or_space,
                    source_screen_allowed=not dominated and improves and work_or_space,
                )
            )
            print("signed range", a_bits, b_bits, new, flush=True)
        result = dict(
            passed=True,
            candidates=candidates,
            baseline_multiplier=old,
            source_screen_allowed=any(c["source_screen_allowed"] for c in candidates),
            same_integer_function_under_signed_guards=True,
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
