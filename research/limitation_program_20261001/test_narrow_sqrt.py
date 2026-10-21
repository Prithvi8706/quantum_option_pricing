"""Exact narrowed unsigned sqrt tests and prospective local leaf experiment."""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.metadata
import io
import json
import platform
import random
import sys
import time
from functools import lru_cache
from math import isqrt
from pathlib import Path

import numpy as np
import pytest

import research.controlled_source_completion.narrow_sqrt as implementation
from research.controlled_source_completion.narrow_sqrt import (
    ALGORITHMS,
    EMBEDDINGS,
    build_narrow_sqrt,
    contract_holds,
    leaf_spec,
    split_clean_child,
)
from research.controlled_source_completion.primitives import (
    array_gates,
    basis_run,
    build,
    resources,
)

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("width", range(1, 7))
@pytest.mark.parametrize("algorithm", ALGORITHMS)
@pytest.mark.parametrize("embedding", EMBEDDINGS)
def test_small_exhaustive_unsigned_input_all_scales_and_active_widths(width, algorithm, embedding):
    rng = random.Random(20261101 + width)
    mask = (1 << width) - 1
    for fraction_bits in range(width + 1):
        for active_bits in range(1, width + 1):
            candidate, arguments, outputs = build_narrow_sqrt(
                width, fraction_bits, active_bits, algorithm, embedding
            )
            for value in range(1 << active_bits):
                initials = range(1 << width) if width <= 3 else (0, mask, rng.getrandbits(width))
                expected_root = isqrt(value << fraction_bits)
                for initial in initials:
                    for inverse in (False, True):
                        actual = basis_run(
                            candidate, arguments, outputs, [value], [initial], inverse
                        )[:3]
                        assert actual == ([initial ^ expected_root], True, True)


def production_values():
    maximum = (1 << 46) - 1
    values = {0, 1, 2, 3, maximum, maximum - 1, 1 << 45, (1 << 45) - 1}
    for index in range(46):
        values.update(
            value
            for value in ((1 << index) - 1, 1 << index, (1 << index) + 1)
            if 0 <= value <= maximum
        )
    # x=s*s gives a perfect scaled square because the fixed scale is 2**40.
    for root in (0, 1, 2, 3, 7, 31, 1 << 11, (1 << 22) - 1, isqrt(maximum)):
        square = root * root
        values.update(value for value in (square - 1, square, square + 1) if 0 <= value <= maximum)
    rng = random.Random(20261102)
    values.update(rng.getrandbits(46) for _ in range(64))
    return sorted(values)


@lru_cache
def historical_leaf():
    return build("sqrt", 72, 40)


@pytest.mark.parametrize("algorithm", ALGORITHMS)
@pytest.mark.parametrize("embedding", EMBEDDINGS)
def test_production_exact_scaled_squares_unsigned_sign_bit_and_historical_equivalence(
    algorithm, embedding
):
    candidate, arguments, outputs = build_narrow_sqrt(algorithm=algorithm, embedding=embedding)
    old, old_arguments, old_outputs = historical_leaf()
    rng = random.Random(20261103)
    for value in production_values():
        assert contract_holds(value)
        for initial in (0, rng.getrandbits(72)):
            expected = [initial ^ isqrt(value << 40)]
            for inverse in (False, True):
                assert basis_run(candidate, arguments, outputs, [value], [initial], inverse)[
                    :3
                ] == (expected, True, True)
            assert basis_run(old, old_arguments, old_outputs, [value], [initial])[:3] == (
                expected,
                True,
                True,
            )
    # The highest active input bit is data, not a sign bit for a signed46 clamp.
    assert isqrt((1 << 45) << 40) > 0
    ignored_inputs = set(arguments[0][46:])
    all_outputs = set(outputs[0])
    high_outputs = set(outputs[0][43:])
    assert all(not set(gate) & ignored_inputs for gate in candidate.gates)
    assert all(not set(gate[:-1]) & all_outputs for gate in candidate.gates)
    # Padded child copies known-zero root bits43..45; these also remain XOR-zero.
    if algorithm == "tight-digit-by-digit":
        assert all(not set(gate) & high_outputs for gate in candidate.gates)


@pytest.mark.parametrize("algorithm", ALGORITHMS)
@pytest.mark.parametrize("embedding", EMBEDDINGS)
def test_invalid_high_input_promise_is_detected_and_semantically_distinct(algorithm, embedding):
    candidate, arguments, outputs = build_narrow_sqrt(algorithm=algorithm, embedding=embedding)
    old, old_arguments, old_outputs = historical_leaf()
    for value in (1 << 46, (1 << 46) + 1, 1 << 71):
        assert not contract_holds(value)
        actual = basis_run(candidate, arguments, outputs, [value], [0])[0][0]
        historical = basis_run(old, old_arguments, old_outputs, [value], [0])[0][0]
        assert actual != historical
    for invalid in (True, -1, 1 << 72, 1.0):
        assert not contract_holds(invalid)


@pytest.mark.parametrize(
    "values",
    [
        (0, 0, 1),
        (72, -1, 46),
        (72, 73, 46),
        (72, 40, 0),
        (72, 40, 73),
        (True, 0, 1),
        (72, True, 46),
        (72, 40, True),
    ],
)
def test_invalid_widths(values):
    with pytest.raises(ValueError):
        build_narrow_sqrt(*values)


def test_versioned_specs_unsigned_domain_and_distinct_candidates():
    specs = [
        leaf_spec(algorithm=algorithm, embedding=embedding)
        for algorithm in ALGORITHMS
        for embedding in EMBEDDINGS
    ]
    keys = {hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest() for spec in specs}
    assert len(keys) == 4
    for spec in specs:
        assert spec["input_contract"] == {"unsigned_input_bits": 46}
        assert spec["radicand_bits"] == 86
        assert spec["result_bits"] == 43
        assert spec["width"] == 72 and spec["fraction_bits"] == 40
    assert leaf_spec()["remainder_bits"] == 45
    with pytest.raises(ValueError):
        leaf_spec(algorithm="Newton approximate")
    with pytest.raises(ValueError):
        leaf_spec(embedding="unknown")


def test_copy_fusion_rejects_output_control_and_damaged_inverse(monkeypatch):
    original = implementation.tight_child

    def damaged(*args):
        child, arguments, outputs = original(*args)
        gate = child.gates[0]
        child.gates[0:1] = [(outputs[0][0], gate[-1])]
        return child, arguments, outputs

    monkeypatch.setattr(implementation, "tight_child", damaged)
    with pytest.raises(ValueError, match="child"):
        build_narrow_sqrt()
    child, _, outputs = original(3, 2)
    count = len(outputs[0])
    boundary = (len(child.gates) - count) // 2
    child.gates[boundary : boundary + 1] = [(outputs[0][0], child.gates[0][-1])]
    with pytest.raises(ValueError, match="copy"):
        split_clean_child(child, outputs[0])


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def run(output):
    output = output.resolve()
    output.relative_to((ROOT / "results/limitation_program_20261001").resolve())
    output.mkdir(parents=True, exist_ok=False)
    producer = Path(__file__).resolve()
    module = ROOT / "research/controlled_source_completion/narrow_sqrt.py"
    proof_root = ROOT / "results/limitation_program_20261001/A07_run003"
    dependencies = [
        ROOT / "research/controlled_source_completion/primitives.py",
        ROOT / "research/antithetic_feasibility/reversible.py",
        ROOT / "research/journal_sprint/reversible_fixed_point.py",
    ]
    snapshot = output / "executed_code"
    snapshot.mkdir()
    for path in [producer, module, *dependencies]:
        (snapshot / path.name).write_bytes(path.read_bytes())
    protocol = {
        "task": "A11 narrowed unsigned exact square-root leaf screen",
        "frozen_before_tests": True,
        "width": 72,
        "fraction_bits": 40,
        "active_input_bits": 46,
        "input_contract": {"unsigned_input_bits": 46},
        "function": "output XOR isqrt(unsigned raw argument << 40)",
        "range_proof": str((proof_root / "summary.json").relative_to(ROOT)),
        "range_proof_sha256": digest(proof_root / "summary.json"),
        "producer_sha256": digest(producer),
        "implementation_sha256": digest(module),
        "dependencies": {str(path.relative_to(ROOT)): digest(path) for path in dependencies},
        "environment": {
            "python": platform.python_version(),
            "executable": sys.executable,
            **{name: importlib.metadata.version(name) for name in ("numpy", "numba", "pytest")},
        },
        "algorithms": list(ALGORITHMS),
        "embeddings": list(EMBEDDINGS),
        "selection": "Minimum exact seven-T/all-to-all leaf T-depth, then T count and qubits",
        "acceptance": [
            "Small external widths1..6: exhaustive promised unsigned inputs, all f0..w, "
            "all active input widths, output XOR and inverse with full cleanup.",
            "Production signed-bit trap, scaled perfect-square neighbors, powers and "
            "seeded randoms equal independent isqrt and historical full72 clean leaf.",
            "Invalid high-input promises are rejected by a separate predicate and "
            "exhibit a deliberate historical mismatch; no graph dispatch proof here.",
            "Fused child must match literal compute/copy/exact-reverse structure.",
            "All stored remainder and arithmetic workspace wires are included in costs.",
        ],
        "stop_rule": "At most four declared exact variants, one finite leaf screen; "
        "30 CPU minute ceiling per candidate. No approximation or precision changes.",
        "exclusions": "No full-source integration/replay, total source resource gain, "
        "physical hardware timing or quantum advantage claim.",
    }
    save(output / "protocol.json", protocol)
    started = time.perf_counter()
    try:
        proof = json.loads((proof_root / "summary.json").read_text())
        assert proof["passed"]
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            test_exit = pytest.main(
                [str(producer), "-q", "--junitxml=" + str(output / "regression.xml")]
            )
        (output / "test_output.txt").write_text(captured.getvalue(), encoding="utf-8")
        print(captured.getvalue(), end="")
        if test_exit != 0:
            raise AssertionError("Narrowed sqrt semantic/domain tests failed")
        candidates = []
        for algorithm in ALGORITHMS:
            for embedding in EMBEDDINGS:
                leaf, arguments, outputs = build_narrow_sqrt(
                    algorithm=algorithm, embedding=embedding
                )
                spec = leaf_spec(algorithm=algorithm, embedding=embedding)
                key = hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest()[:20]
                binary = output / (key + ".npy")
                np.save(binary, array_gates(leaf))
                metadata = {
                    "key": key,
                    "op": "sqrt",
                    "params": {},
                    "spec": spec,
                    "input_contract": spec["input_contract"],
                    "args": [list(argument) for argument in arguments],
                    "outs": [list(out) for out in outputs],
                    "resources": resources(leaf),
                    "gate_file": binary.name,
                    "sha256": digest(binary),
                }
                save(output / (key + ".json"), metadata)
                candidates.append(metadata)
        old = resources(historical_leaf()[0])
        best = min(
            candidates,
            key=lambda row: (
                row["resources"]["t_depth"],
                row["resources"]["t_count"],
                row["resources"]["qubits"],
            ),
        )
        result = {
            "passed": True,
            "decision": "exact leaf accepted; graph dispatch and full-source replay still required",
            "historical72": old,
            "best": best,
            "candidates": [
                {key: row[key] for key in ("key", "spec", "resources")} for row in candidates
            ],
            "dominates_historical72": all(
                best["resources"][name] < old[name] for name in ("t_depth", "t_count", "qubits")
            ),
            "production_pattern_count": len(production_values()),
            "financial_function_changed": False,
            "full_source_gain_claimed": False,
            "elapsed_seconds": time.perf_counter() - started,
        }
        save(output / "summary.json", result)
        assert digest(producer) == protocol["producer_sha256"]
        assert digest(module) == protocol["implementation_sha256"]
        save(
            output / "verification.json",
            {
                "passed": True,
                "code_unchanged_since_prospective_protocol": True,
                "test_exit": test_exit,
                "all_four_candidates_emitted": len(candidates) == 4,
            },
        )
        (output / "NEXT.md").write_text(
            "Use a validated same-SSA unsigned46 range guard, preserve the full72 output, "
            "and cost/schedule/replay the full source before adopting this leaf.\n",
            encoding="utf-8",
        )
        print(json.dumps({"passed": True, "best": best["key"], "resources": best["resources"]}))
    except Exception as error:
        save(
            output / "failure.json",
            {"passed": False, "type": type(error).__name__, "error": str(error)},
        )
        raise
    finally:
        save(
            output / "manifest.json",
            {
                "files": {
                    str(path.relative_to(output)): digest(path)
                    for path in sorted(output.rglob("*"))
                    if path.is_file() and path.name != "manifest.json"
                },
            },
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output)
