"""Prospective finite exact signed7 shift leaf experiment, entirely local."""

import argparse
from datetime import datetime, timezone
from importlib.metadata import version
import hashlib
from pathlib import Path
import shutil
import sys
import time

import numpy as np
import pytest

from research.controlled_source_completion.narrow_shift import (
    build_narrow_shift,
    input_contract,
    leaf_spec,
)
from research.controlled_source_completion.primitives import array_gates, build, resources
from research.limitation_program_20261001.constant_library import canonical, digest
from research.limitation_program_20261001.experiment_prefix_multiplier import ROOT, read, save


def run(output):
    output = output.resolve()
    output.relative_to((ROOT / "results/limitation_program_20261001").resolve())
    output.mkdir(exist_ok=False)
    dependencies = [
        ROOT / name
        for name in (
            "research/limitation_program_20261001/experiment_shift_leaf.py",
            "research/controlled_source_completion/narrow_shift.py",
            "research/limitation_program_20261001/test_narrow_shift.py",
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
    protocol = dict(
        created_utc=datetime.now(timezone.utc).isoformat(),
        local_only=True,
        item="A07 signed7 shift leaf",
        before_tests_and_resource_measurement=True,
        candidates=["signed7-barrel"],
        width=72,
        fraction_bits=40,
        input_contract=input_contract(7),
        semantics="Full72 data; count is unscaled signed integer. Positive counts left "
        "shift modulo2**72; negative counts arithmetic right shift. Full72 arbitrary "
        "output XOR; two native input registers and all workspace restored.",
        architecture="Conditional bit reversal, unsigned narrow magnitude, one exact "
        "left barrel with signed fill, reverse permutation, copy and exact inverse",
        boundary="The magnitude of signed7 count -64 is unsigned64; no signed reinterpretation",
        required_checks="Independent exhaustive small signed data/count/output patterns, "
        "inverse and cleanup; all128 production counts, endpoints and seeded inputs; "
        "native interfaces and full output XOR",
        acceptance="Exact tests pass and unchanged producer/dependencies; no source "
        "adoption or full-source resource saving can be credited by this leaf receipt",
        stop_rule="One declared finite leaf, any semantic failure stops; 30 process CPU minutes",
        resource_model="Actual X/CX/CCX arrays, exact seven-T Toffoli, logical all-to-all ASAP",
        exclusions="Full financial replay, error certification, matched classical or "
        "physical advantage not established; G2-G5 remain open",
        executed_dependencies=snapshots,
        dependencies=frozen,
        environment=dict(
            python=sys.version,
            executable=sys.executable,
            executable_sha256=digest(Path(sys.executable)),
            packages={name: version(name) for name in ("numpy", "numba", "pytest")},
        ),
    )
    save(output / "protocol.json", protocol)
    print("Prospective shift leaf protocol saved", flush=True)
    wall, cpu = time.perf_counter(), time.process_time()
    try:
        test_exit = pytest.main(
            [
                str(ROOT / "research/limitation_program_20261001/test_narrow_shift.py"),
                "-q",
                "--junitxml=" + str(output / "regression.xml"),
            ]
        )
        if test_exit:
            raise AssertionError("Exact signed7 shift leaf tests failed")
        if time.process_time() - cpu > 1800:
            raise TimeoutError("Declared leaf CPU ceiling exceeded")
        program, args, outs = build_narrow_shift(72, 40, 7)
        spec = leaf_spec(72, 40, 7)
        key = hashlib.sha256(canonical(spec).encode()).hexdigest()[:20]
        binary = output / (key + ".npy")
        np.save(binary, array_gates(program))
        metadata = dict(
            key=key,
            op="shift",
            params={},
            spec=spec,
            input_contract=input_contract(7),
            args=[list(argument) for argument in args],
            outs=[list(out) for out in outs],
            resources=resources(program),
            gate_file=binary.name,
            sha256=digest(binary),
        )
        save(output / (key + ".json"), metadata)
        old = resources(build("shift", 72, 40)[0])
        result = dict(
            passed=True,
            decision="Exact signed7 leaf verified; source dispatch, cost and replay still required",
            best=metadata,
            historical_shift72=old,
            all_128_signed7_counts_tested=True,
            positive_left_negative_arithmetic_right=True,
            same_financial_function_under_proved_dispatch=True,
            full_source_gain_claimed=False,
            elapsed_seconds=time.perf_counter() - wall,
            cpu_seconds=time.process_time() - cpu,
        )
        save(output / "summary.json", result)
        assert all(digest(ROOT / name) == expected for name, expected in frozen.items())
        assert read(output / "protocol.json") == protocol
        save(
            output / "verification.json",
            dict(passed=True, pytest_exit_code=int(test_exit), dependencies_unchanged=True),
        )
        (output / "NEXT.md").write_text(
            "Require a validated actual SSA count interval proof. Keep full native "
            "argument copies and generic archived fallback. Screen both complete capped "
            "sources, then financial replay and independent audit before adoption.\n",
            encoding="utf-8",
        )
        print(dict(passed=True, resources=metadata["resources"], baseline=old), flush=True)
    except Exception as error:
        save(
            output / "failure.json",
            dict(passed=False, type=type(error).__name__, error=str(error)),
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
