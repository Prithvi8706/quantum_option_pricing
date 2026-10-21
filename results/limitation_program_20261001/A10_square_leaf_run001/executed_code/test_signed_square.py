"""Exact same-SSA square checks and prospective finite local leaf experiment."""

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
from pathlib import Path

import numpy as np
from numba import njit
import pytest

from research.controlled_source_completion.prefix_multiplier import build_prefix_multiplier
from research.controlled_source_completion.primitives import (
    array_gates, basis_run, resources, run_gates,
)
from research.controlled_source_completion.signed_square import (
    LOWERING, VARIANTS, build_signed_square, input_contract, leaf_spec,
    signed_square_terms, validate_same_ssa_arguments,
)

ROOT = Path(__file__).resolve().parents[2]


@njit(cache=True)
def exhaustive_equal_arguments(gates, qubits, width, fraction_bits):
    """Independent signed integer oracle, every input/output word and inverse."""
    limit, count = 1 << width, 0
    for value in range(limit):
        signed = value - limit if value & (limit >> 1) else value
        expected = (signed * signed // (1 << fraction_bits)) & (limit - 1)
        for initial in range(limit):
            for inverse in (False, True):
                state = np.zeros(qubits, np.uint8)
                for bit in range(width):
                    state[bit] = (value >> bit) & 1
                    state[width + bit] = (value >> bit) & 1
                    state[2 * width + bit] = (initial >> bit) & 1
                run_gates(gates, state, inverse)
                observed = 0
                for bit in range(width):
                    if state[bit] != (value >> bit) & 1:
                        return False, count, value, initial, inverse, 1
                    if state[width + bit] != (value >> bit) & 1:
                        return False, count, value, initial, inverse, 2
                    observed |= int(state[2 * width + bit]) << bit
                if observed != (expected ^ initial):
                    return False, count, value, initial, inverse, 3
                for wire in range(3 * width, qubits):
                    if state[wire]:
                        return False, count, value, initial, inverse, 4
                count += 1
    return True, count, 0, 0, False, 0


@pytest.mark.parametrize("width", range(1, 7))
def test_every_small_signed_input_all_fraction_output_words_and_inverse(width):
    for fraction_bits in range(width + 1):
        program, _, _ = build_signed_square(width, fraction_bits)
        report = exhaustive_equal_arguments(
            array_gates(program), program.qubits, width, fraction_bits
        )
        assert report[0], (width, fraction_bits, report)
        assert report[1] == 2 * (1 << (2 * width))


def test_signed_symmetric_expansion_complement_correction_and_retained_slice_theorem():
    for width in range(1, 7):
        limit = 1 << width
        for fraction_bits in range(width + 1):
            n = width + fraction_bits
            mask = (1 << n) - 1
            terms, correction = signed_square_terms(width, fraction_bits)
            expected_indices = {
                (i, j) for i in range(width) for j in range(i, width)
                if (2 * i if i == j else i + j + 1) < n
            }
            assert {(i, j) for i, j, _, _ in terms} == expected_indices
            assert len(terms) == len(expected_indices)
            for raw in range(limit):
                signed = raw - limit if raw & (limit >> 1) else raw
                represented = correction
                for i, j, column, negative in terms:
                    assert column == (2 * i if i == j else i + j + 1)
                    assert negative == (i != j and ((i == width - 1) != (j == width - 1)))
                    bit = ((raw >> i) & 1) & ((raw >> j) & 1)
                    represented += ((1 - bit) if negative else bit) << column
                residue = represented & mask
                assert residue == (signed * signed) & mask
                assert residue >> fraction_bits == (
                    signed * signed // (1 << fraction_bits)
                ) & (limit - 1)


def test_negative_controls_for_sign_correction_and_discarded_low_column_carry():
    terms, correction = signed_square_terms(3, 2)
    uncorrected_zero = sum(int(negative) << column for _, _, column, negative in terms)
    assert correction != 0
    assert (uncorrected_zero & 31) >> 2 != 0
    assert ((uncorrected_zero + correction) & 31) >> 2 == 0
    # At f=3 the diagonal bit0 and two symmetric contributions at column2
    # jointly produce a carry into column3: 3**2//8=1, not zero.
    terms, _ = signed_square_terms(4, 3)
    retained_only = sum(
        (((3 >> i) & 1) & ((3 >> j) & 1)) << column
        for i, j, column, _ in terms if column >= 3
    )
    assert retained_only >> 3 == 0
    assert 3 * 3 // 8 == 1


def test_csa_majority_xor_has_disjoint_terms_and_exact_sum():
    for x in (0, 1):
        for y in (0, 1):
            for z in (0, 1):
                first, second = x & y, (x ^ y) & z
                assert not (first and second)
                assert (x ^ y ^ z) + 2 * (first ^ second) == x + y + z


def production_values():
    width = 72
    mask, sign = (1 << width) - 1, 1 << (width - 1)
    values = {0, 1, 2, 3, mask, mask - 1, sign, sign - 1, sign + 1,
              1 << 40, (1 << 40) - 1, (1 << 40) + 1}
    for bit in range(width):
        single = 1 << bit
        values.update((single, single - 1, (single + 1) & mask, (-single) & mask))
    rng = random.Random(20261012)
    values.update(rng.getrandbits(width) for _ in range(128))
    return sorted(values)


@lru_cache
def production_leaf():
    return build_signed_square(72, 40)


@lru_cache
def historical_leaf():
    return build_prefix_multiplier(72, 40, "brent-kung")


def test_production72_signed_endpoints_128_randoms_historical_equivalence_and_inverse():
    program, args, outs = production_leaf()
    old, old_args, old_outs = historical_leaf()
    mask = (1 << 72) - 1
    rng = random.Random(20261013)
    for raw in production_values():
        assert validate_same_ssa_arguments(72, [raw, raw])
        signed = raw - (1 << 72) if raw >> 71 else raw
        expected = (signed * signed // (1 << 40)) & mask
        for initial in (0, rng.getrandbits(72)):
            for inverse in (False, True):
                assert basis_run(program, args, outs, [raw, raw], [initial], inverse)[:3] == (
                    [initial ^ expected], True, True
                )
            assert basis_run(old, old_args, old_outs, [raw, raw], [initial])[:3] == (
                [initial ^ expected], True, True
            )


def test_native_two_argument_layout_diagonal_cx_offdiagonal_ccx_and_exact_cleanup():
    program, args, outs = production_leaf()
    assert args[0] == tuple(range(72))
    assert args[1] == tuple(range(72, 144))
    assert outs[0] == tuple(range(144, 216))
    input_wires, second_wires = set(args[0] + args[1]), set(args[1])
    output_wires = set(outs[0])
    assert all(not set(gate) & second_wires for gate in program.gates)
    assert all(not set(gate[:-1]) & output_wires for gate in program.gates)
    assert all(gate[-1] not in input_wires for gate in program.gates)
    terms, correction = signed_square_terms(72, 40)
    assert correction == 1 << 72
    assert sum(negative for _, _, _, negative in terms) == 40
    cursor, wire = 0, 216
    for i, j, _, negative in terms:
        if negative:
            assert program.gates[cursor] == (wire,)
            cursor += 1
        assert program.gates[cursor] == (
            (args[0][i], wire) if i == j else (args[0][i], args[0][j], wire)
        )
        cursor += 1
        wire += 1
    assert program.gates[cursor] == (wire,)
    assert (len(program.gates) - 72) % 2 == 0
    boundary = (len(program.gates) - 72) // 2
    copies = [program.gates[boundary + index] for index in range(72)]
    assert all(len(gate) == 2 and gate[-1] == outs[0][index]
               for index, gate in enumerate(copies))
    assert len({gate[0] for gate in copies}) == 72
    assert all(program.gates[index] == program.gates[-1 - index]
               for index in range(boundary))


def test_explicit_equality_boundary_rejects_invalid_invocations_and_shows_mismatch():
    for invalid in ([1, 2], [True, True], [-1, -1], [1 << 72, 1 << 72],
                    [1.0, 1.0], [0], [0, 0, 0], None):
        with pytest.raises(ValueError):
            validate_same_ssa_arguments(72, invalid)
    assert validate_same_ssa_arguments(72, (1, 1))
    candidate, args, outs = build_signed_square(4, 0)
    old, old_args, old_outs = build_prefix_multiplier(4, 0)
    assert basis_run(candidate, args, outs, [1, 2], [0])[0] == [1]
    assert basis_run(old, old_args, old_outs, [1, 2], [0])[0] == [2]


@pytest.mark.parametrize("arguments", [
    (True, 0, "brent-kung"), (0, 0, "brent-kung"),
    (3, True, "brent-kung"), (3, -1, "brent-kung"),
    (3, 4, "brent-kung"), (3, 2, "kogge-stone"),
    (3, 2, "unknown"), (3.0, 2, "brent-kung"),
])
def test_invalid_parameters(arguments):
    with pytest.raises(ValueError):
        build_signed_square(*arguments)
    with pytest.raises(ValueError):
        leaf_spec(*arguments)


def test_versioned_spec_full_interface_and_one_declared_variant():
    spec = leaf_spec(72, 40)
    assert spec["op"] == "mul" and spec["params"] == {}
    assert spec["width"] == 72 and spec["fraction_bits"] == 40
    assert spec["product_width"] == 112
    assert spec["lowering"] == LOWERING
    assert spec["input_contract"] == input_contract() == {"same_ssa_arguments": True}
    assert VARIANTS == ("brent-kung",)
    assert leaf_spec(3, 3)["product_width"] == 6


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def run(output):
    output = output.resolve()
    output.relative_to((ROOT / "results/limitation_program_20261001").resolve())
    output.mkdir(parents=True, exist_ok=False)
    producer = Path(__file__).resolve()
    implementation = ROOT / "research/controlled_source_completion/signed_square.py"
    dependencies = [ROOT / relative for relative in (
        "research/controlled_source_completion/prefix_multiplier.py",
        "research/controlled_source_completion/carry_lookahead.py",
        "research/controlled_source_completion/primitives.py",
        "research/journal_sprint/reversible_fixed_point.py",
    )]
    snapshot = output / "executed_code"
    snapshot.mkdir()
    for path in [producer, implementation, *dependencies]:
        (snapshot / path.name).write_bytes(path.read_bytes())
    protocol = {
        "task": "A10 exact same-SSA signed square finite leaf experiment",
        "frozen_before_tests_and_counts": True,
        "width": 72, "fraction_bits": 40, "product_width": 112,
        "input_contract": input_contract(), "native_input_registers": 2,
        "function": "Under equal arguments, output XOR floor(signed(a)**2/2**40) mod2**72",
        "variant": "brent-kung", "lowering": LOWERING,
        "producer_sha256": digest(producer), "implementation_sha256": digest(implementation),
        "dependencies": {str(path.relative_to(ROOT)): digest(path) for path in dependencies},
        "environment": {
            "python": platform.python_version(), "executable": sys.executable,
            "executable_sha256": digest(Path(sys.executable)),
            **{name: importlib.metadata.version(name) for name in ("numpy", "numba", "pytest")},
        },
        "acceptance": [
            "Exhaust widths1..6, f0..w, every signed raw input and output word, forward/inverse; "
            "independent integer square/floor and complete input/scratch restoration.",
            "Production72/f40 signed endpoints, all single-bit/adjacent/negated powers and "
            "128 seeded random words equal independent floor and frozen general prefix multiply.",
            "Inspect literal diagonal CX/offdiagonal CCX, no output controls and no use of b; "
            "complete outer compute/copy/exact-reverse structure.",
            "Reject unequal or malformed invocations at explicit API boundary; show deliberate "
            "inequality mismatch. Whole-source same SSA proof is separate work.",
            "Negative controls demonstrate missing sign correction and low-column carry fail.",
        ],
        "selection": "One declared exact variant; no adaptive search or precision change.",
        "stop_rule": "One finite candidate; at most 30 CPU minutes. Stop on any semantic failure.",
        "resource_model": "Actual X/CX/CCX arrays; seven-T exact CCX; "
        "all-to-all logical scheduling.",
        "exclusions": "No source adoption/full-source gain, physical runtime "
        "or quantum advantage claim.",
    }
    save(output / "protocol.json", protocol)
    started, cpu_started = time.perf_counter(), time.process_time()
    try:
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            test_exit = pytest.main([
                str(producer), "-q", "--junitxml=" + str(output / "regression.xml")
            ])
        (output / "test_output.txt").write_text(captured.getvalue(), encoding="utf-8")
        print(captured.getvalue(), end="")
        if test_exit != 0:
            raise AssertionError("Same-SSA square exact semantic/contract checks failed")
        if time.process_time() - cpu_started > 1800:
            raise TimeoutError("Declared 30 CPU minute leaf ceiling exceeded")
        program, args, outs = production_leaf()
        spec = leaf_spec(72, 40)
        key = hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest()[:20]
        binary = output / (key + ".npy")
        np.save(binary, array_gates(program))
        metadata = {
            "key": key, "op": "mul", "params": {}, "spec": spec,
            "input_contract": input_contract(),
            "args": [list(argument) for argument in args],
            "outs": [list(out) for out in outs], "resources": resources(program),
            "gate_file": binary.name, "sha256": digest(binary),
        }
        save(output / (key + ".json"), metadata)
        old = resources(historical_leaf()[0])
        terms, correction = signed_square_terms(72, 40)
        result = {
            "passed": True,
            "decision": "Exact leaf verified; same-SSA source dispatch/cost/replay still required",
            "best": metadata, "historical_prefix_multiply72": old,
            "production_pattern_count": len(production_values()), "seeded_random_count": 128,
            "symmetric_term_count": len(terms),
            "diagonal_count": sum(i == j for i, j, _, _ in terms),
            "off_diagonal_count": sum(i != j for i, j, _, _ in terms),
            "negative_term_count": sum(negative for _, _, _, negative in terms),
            "correction_raw": correction,
            "dominates_historical_leaf": all(
                metadata["resources"][name] < old[name]
                for name in ("t_depth", "t_count", "qubits")
            ),
            "same_financial_integer_function_under_proved_dispatch": True,
            "full_source_gain_claimed": False,
            "elapsed_seconds": time.perf_counter() - started,
            "cpu_seconds": time.process_time() - cpu_started,
        }
        save(output / "summary.json", result)
        assert digest(producer) == protocol["producer_sha256"]
        assert digest(implementation) == protocol["implementation_sha256"]
        assert all(digest(path) == protocol["dependencies"][str(path.relative_to(ROOT))]
                   for path in dependencies)
        save(output / "verification.json", {
            "passed": True, "test_exit": int(test_exit),
            "code_unchanged_since_prospective_protocol": True,
            "all_declared_candidates_emitted": True, "full_source_gain_claimed": False,
        })
        (output / "NEXT.md").write_text(
            "Require identical SSA identifiers for both multiplication operands; retain generic "
            "fallback otherwise. Cost and replay both full sources under existing caps before "
            "adoption. The native second argument still counts in copies/interface.\n",
            encoding="utf-8",
        )
        print(json.dumps({"passed": True, "key": key, "resources": metadata["resources"]}))
    except Exception as error:
        save(output / "failure.json", {
            "passed": False, "type": type(error).__name__, "error": str(error)
        })
        raise
    finally:
        save(output / "manifest.json", {
            "files": {
                str(path.relative_to(output)): digest(path)
                for path in sorted(output.rglob("*"))
                if path.is_file() and path.name != "manifest.json"
            }
        })


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output)
