"""Independent exact root, full output-XOR and complete cleanup checks."""

from functools import lru_cache
from math import isqrt
import random

from numba import njit
import numpy as np
import pytest

from research.controlled_source_completion.narrow_sqrt import build_narrow_sqrt
from research.controlled_source_completion.nonrestoring_sqrt import (
    ALGORITHM, LOWERING, build_nonrestoring_sqrt, contract_holds, input_contract,
    leaf_spec,
)
from research.controlled_source_completion.primitives import (
    array_gates, basis_run, run_gates,
)


@njit(cache=True)
def exhaustive_words(gates, qubits, width, expected_roots):
    """Python isqrt supplies roots; enumerate every dirty word in both directions."""
    visited = 0
    for value in range(len(expected_roots)):
        expected = expected_roots[value]
        for initial in range(1 << width):
            for inverse in (False, True):
                state = np.zeros(qubits, np.uint8)
                for bit in range(width):
                    state[bit] = (value >> bit) & 1
                    state[width + bit] = (initial >> bit) & 1
                run_gates(gates, state, inverse)
                for bit in range(width):
                    if state[bit] != (value >> bit) & 1:
                        return False, visited, value, initial, inverse, 1
                    if state[width + bit] != ((initial ^ expected) >> bit) & 1:
                        return False, visited, value, initial, inverse, 2
                for wire in range(2 * width, qubits):
                    if state[wire]:
                        return False, visited, value, initial, inverse, 3
                visited += 1
    return True, visited, 0, 0, False, 0


@pytest.mark.parametrize("width", range(1, 7))
def test_all_small_active_widths_fractions_input_output_words_and_inverse(width):
    for fraction_bits in range(width + 1):
        for active_bits in range(1, width + 1):
            program, _, _ = build_nonrestoring_sqrt(width, fraction_bits, active_bits)
            expected = np.asarray(
                [isqrt(value << fraction_bits) for value in range(1 << active_bits)],
                dtype=np.int64,
            )
            report = exhaustive_words(array_gates(program), program.qubits, width, expected)
            assert report[0], (width, fraction_bits, active_bits, report)
            assert report[1] == 2 * (1 << (width + active_bits))


def check_integer_trace(value, fraction_bits, active_bits):
    """Integer theorem check, including each prefix and signed remainder bound."""
    k = (active_bits + fraction_bits + 1) // 2
    root, remainder, prefix = 0, 0, 0
    radicand = value << fraction_bits
    saw_negative, saw_positive, shifted_overflow = False, False, False
    for position in reversed(range(k)):
        digit = (radicand >> (2 * position)) & 3
        prefix = 4 * prefix + digit
        old_sign = int(remainder < 0)
        operand = (4 * root + 3) if old_sign else -(4 * root + 1)
        encoded = 3
        for bit in range(2, k + 2):
            encoded |= (((root >> (bit - 2)) & 1) ^ (1 - old_sign)) << bit
        assert encoded == operand & ((1 << (k + 2)) - 1)
        shifted = 4 * remainder + digit
        shifted_overflow |= not -(1 << (k + 1)) <= shifted < 1 << (k + 1)
        remainder = shifted + operand
        root = 2 * root + int(remainder >= 0)
        assert root == isqrt(prefix)
        expected_remainder = prefix - (root if remainder >= 0 else root + 1) ** 2
        assert remainder == expected_remainder
        assert -(2 * root + 1) <= remainder <= 2 * root
        assert -(1 << (k + 1)) <= remainder < 1 << (k + 1)
        saw_negative |= remainder < 0
        saw_positive |= remainder >= 0
    assert root == isqrt(radicand)
    return saw_negative, saw_positive, shifted_overflow


def test_standard_integer_recurrence_operand_identity_prefix_invariant_and_bounds():
    branches = [False, False, False]
    for active_bits in range(1, 9):
        for fraction_bits in range(9):
            for value in range(1 << active_bits):
                trace = check_integer_trace(value, fraction_bits, active_bits)
                branches = [old or new for old, new in zip(branches, trace)]
    assert all(branches), "Both signed branches and modular overflow must be exercised"


def production_values(active_bits=46, fraction_bits=40, random_count=128):
    maximum = (1 << active_bits) - 1
    values = {0, 1, 2, 3, maximum, maximum - 1, 1 << (active_bits - 1)}
    for bit in range(active_bits):
        values.update(
            value for value in ((1 << bit) - 1, 1 << bit, (1 << bit) + 1)
            if 0 <= value <= maximum
        )
    # For odd f, x=2*s*s also makes x<<f a perfect integer square.
    factor = 2 if fraction_bits % 2 else 1
    largest = isqrt(maximum // factor)
    for root in (0, 1, 2, 3, 7, 31, largest // 2, largest - 1, largest):
        square = factor * root * root
        values.update(value for value in (square - 1, square, square + 1)
                      if 0 <= value <= maximum)
    rng = random.Random(20261031 + active_bits + fraction_bits)
    values.update(rng.getrandbits(active_bits) for _ in range(random_count))
    return sorted(values)


@lru_cache
def production_leaf():
    return build_nonrestoring_sqrt(72, 40, 46)


@lru_cache
def accepted_leaf():
    return build_narrow_sqrt(72, 40, 46, "tight-digit-by-digit", "fused-child-copy")


def test_production_unsigned46_topbit_square_neighbors_128_randoms_accepted_equivalence():
    program, args, outs = production_leaf()
    old, old_args, old_outs = accepted_leaf()
    rng, mask = random.Random(20261101), (1 << 72) - 1
    for value in production_values():
        assert contract_holds(value)
        for initial in (0, mask, rng.getrandbits(72) | (1 << 71)):
            expected = ([initial ^ isqrt(value << 40)], True, True)
            for inverse in (False, True):
                assert basis_run(program, args, outs, [value], [initial], inverse)[:3] == expected
            assert basis_run(old, old_args, old_outs, [value], [initial])[:3] == expected
    assert isqrt((1 << 45) << 40) > 0


@pytest.mark.parametrize("width,fraction_bits,active_bits", [
    (24, 12, 20), (40, 23, 32), (72, 40, 46),
])
def test_native24_40_72_fixtures_scale_parity_dirty_high_output_and_cleanup(
    width, fraction_bits, active_bits,
):
    program, args, outs = build_nonrestoring_sqrt(width, fraction_bits, active_bits)
    old, old_args, old_outs = build_narrow_sqrt(width, fraction_bits, active_bits)
    rng = random.Random(20261102 + width)
    for value in production_values(active_bits, fraction_bits, 32):
        initial = rng.getrandbits(width) | (1 << (width - 1))
        expected = ([initial ^ isqrt(value << fraction_bits)], True, True)
        for inverse in (False, True):
            assert basis_run(program, args, outs, [value], [initial], inverse)[:3] == expected
        assert basis_run(old, old_args, old_outs, [value], [initial])[:3] == expected


@pytest.mark.parametrize("width,fraction_bits,active_bits", [
    (1, 0, 1), (6, 5, 4), (72, 40, 46),
])
def test_native_layout_all_history_charged_and_literal_compute_copy_inverse(
    width, fraction_bits, active_bits,
):
    program, args, outs = build_nonrestoring_sqrt(width, fraction_bits, active_bits)
    spec = leaf_spec(width, fraction_bits, active_bits)
    k, r = spec["result_bits"], spec["remainder_bits"]
    assert args == [tuple(range(width))]
    assert outs == [tuple(range(width, 2 * width))]
    assert program.qubits == 2 * width + k + (k + 2) * r + 1
    assert all(gate[-1] not in set(args[0]) for gate in program.gates)
    assert all(not set(gate) & set(args[0][active_bits:]) for gate in program.gates)
    assert all(not set(gate) & set(outs[0][k:]) for gate in program.gates)
    assert all(not set(gate[:-1]) & set(outs[0]) for gate in program.gates)
    assert (len(program.gates) - k) % 2 == 0
    boundary = (len(program.gates) - k) // 2
    forward = program.gates[:boundary]
    middle = program.gates[boundary:boundary + k]
    assert program.gates[boundary + k:] == list(reversed(forward))
    assert middle == [(2 * width + bit, width + bit) for bit in range(k)]
    assert all(not set(gate) & set(outs[0]) for gate in forward)


@pytest.mark.parametrize("parameters", [
    (0, 0, 1), (72, -1, 46), (72, 73, 46), (72, 40, 0),
    (72, 40, 73), (True, 0, 1), (72, True, 46), (72, 40, True),
    (72.0, 40, 46), (72, 40, 46.0),
])
def test_invalid_widths_and_boolean_parameters(parameters):
    with pytest.raises(ValueError):
        build_nonrestoring_sqrt(*parameters)
    with pytest.raises(ValueError):
        leaf_spec(*parameters)


def test_versioned_one_family_spec_unsigned_domain_and_signed_remainder_history():
    spec = leaf_spec()
    assert spec["lowering"] == LOWERING
    assert spec["algorithm"] == ALGORITHM
    assert spec["input_contract"] == input_contract() == {"unsigned_input_bits": 46}
    assert spec["radicand_bits"] == 86
    assert spec["result_bits"] == 43
    assert spec["remainder_bits"] == 45
    assert spec["remainder_history_count"] == 44
    assert spec["width"] == 72 and spec["fraction_bits"] == 40
    for invalid in (True, 0, -1, 46.0):
        with pytest.raises(ValueError):
            input_contract(invalid)


def test_unsigned_boundary_rejects_high_inputs_and_demonstrates_promised_domain_mismatch():
    for invalid in (True, -1, 1 << 46, 1 << 71, 1 << 72, 1.0):
        assert not contract_holds(invalid)
    assert contract_holds(1 << 45) and contract_holds((1 << 46) - 1)
    assert not contract_holds(0, True, 1)
    assert not contract_holds(0, 72, True)
    assert not contract_holds(0, 72, 73)
    program, args, outs = production_leaf()
    for value in (1 << 46, (1 << 46) + 1, 1 << 71):
        actual = basis_run(program, args, outs, [value], [0])
        assert actual[1:3] == (True, True)
        assert actual[0][0] != isqrt(value << 40)


def test_negative_control_unsigned_remainder_interpretation_breaks_zero_input():
    # First root step for digit00 produces R=-1. Treating its word as an
    # unsigned nonnegative integer would emit1 instead of the correct0.
    remainder_word = (-1) & ((1 << 3) - 1)
    assert remainder_word >= 0
    assert int(remainder_word >= 0) != isqrt(0)


def test_negative_control_missing_plus_three_negative_branch_breaks_exact_root():
    # prefix0 makes R=-1; next digit01 must use +(4Q+3), giving R=0,Q=1.
    assert 4 * (-1) + 1 + (4 * 0 + 3) == 0
    wrong_remainder = 4 * (-1) + 1 + (4 * 0 + 1)
    wrong_root = int(wrong_remainder >= 0)
    assert wrong_root != isqrt(1)
