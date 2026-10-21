"""Exact signed-count shift checks against independent integer semantics."""

from functools import lru_cache
import random

from numba import njit
import numpy as np
import pytest

from research.controlled_source_completion.narrow_shift import (
    LOWERING, build_narrow_shift, contract_holds, input_contract, leaf_spec,
)
from research.controlled_source_completion.primitives import (
    array_gates, basis_run, build, resources, run_gates,
)


def integer_shift(raw_data, signed_count, width):
    """Independent Python oracle, including oversized modular/signed shifts."""
    limit = 1 << width
    signed_data = raw_data - limit if raw_data & (limit >> 1) else raw_data
    if signed_count >= width:
        return 0
    if signed_count <= -width:
        return (limit - 1) if signed_data < 0 else 0
    shifted = signed_data << signed_count if signed_count >= 0 else signed_data >> -signed_count
    return shifted & (limit - 1)


@njit(cache=True)
def exhaustive_words(gates, qubits, width, count_bits):
    """Every small signed data/count and dirty output, forward and inverse."""
    limit, count_limit = 1 << width, 1 << count_bits
    visited = 0
    for raw_data in range(limit):
        signed_data = raw_data - limit if raw_data & (limit >> 1) else raw_data
        for narrow_count in range(count_limit):
            signed_count = (
                narrow_count - count_limit
                if narrow_count & (count_limit >> 1) else narrow_count
            )
            raw_count = signed_count & (limit - 1)
            if signed_count >= width:
                expected = 0
            elif signed_count <= -width:
                expected = limit - 1 if signed_data < 0 else 0
            elif signed_count >= 0:
                expected = (signed_data << signed_count) & (limit - 1)
            else:
                expected = (signed_data >> -signed_count) & (limit - 1)
            for initial in range(limit):
                for inverse in (False, True):
                    state = np.zeros(qubits, np.uint8)
                    for bit in range(width):
                        state[bit] = (raw_data >> bit) & 1
                        state[width + bit] = (raw_count >> bit) & 1
                        state[2 * width + bit] = (initial >> bit) & 1
                    run_gates(gates, state, inverse)
                    for bit in range(width):
                        if state[bit] != (raw_data >> bit) & 1:
                            return False, visited, raw_data, signed_count, initial, 1
                        if state[width + bit] != (raw_count >> bit) & 1:
                            return False, visited, raw_data, signed_count, initial, 2
                        if state[2 * width + bit] != ((expected ^ initial) >> bit) & 1:
                            return False, visited, raw_data, signed_count, initial, 3
                    for wire in range(3 * width, qubits):
                        if state[wire]:
                            return False, visited, raw_data, signed_count, initial, 4
                    visited += 1
    return True, visited, 0, 0, 0, 0


@pytest.mark.parametrize("width", range(1, 7))
def test_all_small_data_counts_dirty_outputs_and_inverse(width):
    for count_bits in range(1, width + 1):
        program, _, _ = build_narrow_shift(width, width // 2, count_bits)
        report = exhaustive_words(array_gates(program), program.qubits, width, count_bits)
        assert report[0], (width, count_bits, report)
        assert report[1] == 2 * (1 << (2 * width + count_bits))


@njit(cache=True)
def check_batch(gates, qubits, inputs, initial_outputs, expected_outputs):
    """Replay both directions; inputs/expected values supplied by Python oracle."""
    width = initial_outputs.shape[1]
    for case in range(inputs.shape[0]):
        for inverse in (False, True):
            state = np.zeros(qubits, np.uint8)
            state[:2 * width] = inputs[case]
            state[2 * width:3 * width] = initial_outputs[case]
            run_gates(gates, state, inverse)
            for wire in range(2 * width):
                if state[wire] != inputs[case, wire]:
                    return False, case, inverse, 1
            for wire in range(width):
                if state[2 * width + wire] != expected_outputs[case, wire]:
                    return False, case, inverse, 2
            for wire in range(3 * width, qubits):
                if state[wire]:
                    return False, case, inverse, 3
    return True, inputs.shape[0], False, 0


def bit_array(values, width):
    return np.asarray([[(int(value) >> bit) & 1 for bit in range(width)]
                       for value in values], dtype=np.uint8)


@lru_cache
def production_leaf():
    return build_narrow_shift()


def production_values():
    width, sign, mask = 72, 1 << 71, (1 << 72) - 1
    values = {0, 1, 2, 3, sign - 1, sign, sign + 1, mask, mask - 1,
              1 << 40, (1 << 40) - 1, (1 << 40) + 1}
    for bit in range(width):
        values.update((1 << bit, (-(1 << bit)) & mask))
    rng = random.Random(20261021)
    values.update(rng.getrandbits(width) for _ in range(128))
    return sorted(values)


def test_production72_all128_counts_endpoints_single_bits_128_randoms_and_inverse():
    program, _, _ = production_leaf()
    width, mask = 72, (1 << 72) - 1
    rng = random.Random(20261022)
    data_values, count_values, initial_values, expected_values = [], [], [], []
    for signed_count in range(-64, 64):
        raw_count = signed_count & mask
        assert contract_holds(raw_count)
        for raw_data in production_values():
            initial = rng.getrandbits(width) | 1 | (1 << 71)
            data_values.append(raw_data)
            count_values.append(raw_count)
            initial_values.append(initial)
            expected_values.append(initial ^ integer_shift(raw_data, signed_count, width))
    inputs = np.concatenate((bit_array(data_values, width), bit_array(count_values, width)),
                            axis=1)
    initial = bit_array(initial_values, width)
    expected = bit_array(expected_values, width)
    report = check_batch(array_gates(program), program.qubits, inputs, initial, expected)
    assert report[0], report
    assert report[1] == 128 * len(production_values())


def test_archived_full_count_shift_equivalence_each_production_count_with_dirty_output():
    program, args, outs = production_leaf()
    historical, historical_args, historical_outs = build("shift", 72, 40)
    mask, rng = (1 << 72) - 1, random.Random(20261023)
    for signed_count in range(-64, 64):
        for raw_data in (0, 1, 1 << 71, (1 << 71) - 1, mask, rng.getrandbits(72)):
            raw_count, initial = signed_count & mask, rng.getrandbits(72)
            expected = ([initial ^ integer_shift(raw_data, signed_count, 72)], True, True)
            assert basis_run(program, args, outs, [raw_data, raw_count], [initial])[:3] == (
                expected
            )
            assert basis_run(historical, historical_args, historical_outs,
                             [raw_data, raw_count], [initial])[:3] == expected


@pytest.mark.parametrize("width,count_bits", [(1, 1), (5, 5), (8, 7), (72, 7)])
def test_native_interface_and_literal_compute_copy_reverse_boundary(width, count_bits):
    program, args, outs = build_narrow_shift(width, width // 2, count_bits)
    assert args == [tuple(range(width)), tuple(range(width, 2 * width))]
    assert outs == [tuple(range(2 * width, 3 * width))]
    assert program.qubits == (count_bits + 4) * width + 2 * count_bits + 1
    native_inputs, native_outputs = set(args[0] + args[1]), set(outs[0])
    assert all(gate[-1] not in native_inputs for gate in program.gates)
    assert all(not set(gate[:-1]) & native_outputs for gate in program.gates)
    assert all(not set(gate) & set(args[1][count_bits:]) for gate in program.gates)
    assert (len(program.gates) - width) % 2 == 0
    boundary = (len(program.gates) - width) // 2
    forward = program.gates[:boundary]
    middle = program.gates[boundary:boundary + width]
    reverse = program.gates[boundary + width:]
    assert reverse == list(reversed(forward))
    assert all(not set(gate) & native_outputs for gate in forward)
    assert all(len(gate) == 2 and gate[1] == target
               for gate, target in zip(middle, outs[0]))
    assert len({gate[0] for gate in middle}) == width


def test_minimum_signed_count_magnitude64_and_historical_direction_negative_control():
    program, args, outs = production_leaf()
    mask, initial = (1 << 72) - 1, (1 << 71) | 123
    for raw_data in ((1 << 71), (1 << 71) - 1, mask, 1, (1 << 64) | 7):
        expected = integer_shift(raw_data, -64, 72)
        observed = basis_run(program, args, outs, [raw_data, (-64) & mask], [initial])
        assert observed[:3] == ([initial ^ expected], True, True)
    # Both signs distinguish the archived direction from the reversed convention.
    assert integer_shift(3, 1, 72) == 6
    assert integer_shift(3, -1, 72) == 1
    assert integer_shift(mask - 2, -1, 72) == mask - 1
    # Reading the abs(-64) unsigned magnitude as signed -64 would be wrong.
    assert abs(-64) == 64 and (64 - 128) == -64


def test_small_native_oversized_counts_saturate_right_and_zero_left():
    program, args, outs = build_narrow_shift(8, 3, 7)
    for count in (-64, -63, -9, -8, 8, 9, 62, 63):
        for data in (0, 1, 127, 128, 129, 255):
            for initial in (0, 1, 127, 128, 255):
                for inverse in (False, True):
                    expected = integer_shift(data, count, 8)
                    assert basis_run(program, args, outs, [data, count & 255],
                                     [initial], inverse)[:3] == (
                        [initial ^ expected], True, True
                    )


def test_narrow_unsigned_magnitude_zero_prefix_carry_identity_exhaustively():
    for count_bits in range(1, 10):
        limit = 1 << count_bits
        for raw in range(limit):
            sign, carry = raw >> (count_bits - 1), raw >> (count_bits - 1)
            magnitude = raw & 1
            for bit in range(1, count_bits):
                carry = carry & (1 - ((raw >> (bit - 1)) & 1))
                magnitude |= (((raw >> bit) & 1) ^ sign ^ carry) << bit
            signed = raw - limit if sign else raw
            assert magnitude == abs(signed)


def test_fredkin_and_difference_mux_truth_tables():
    for sign in (0, 1):
        for low in (0, 1):
            for high in (0, 1):
                a, b = low, high
                b ^= a
                a ^= sign & b
                b ^= a
                assert (a, b) == ((high, low) if sign else (low, high))
                target, difference = low, low ^ high
                target ^= sign & difference
                difference ^= high
                difference ^= low
                assert target == (high if sign else low) and difference == 0


def test_contract_rejects_missing_sign_extension_and_signed_overflow():
    mask = (1 << 72) - 1
    for value in range(-64, 64):
        assert contract_holds(value & mask)
    for invalid in (64, 127, 128, (-65) & mask, (-128) & mask, -1, 1 << 72,
                    True, 1.0, None):
        assert not contract_holds(invalid)
    assert not contract_holds(127)  # low signed7=-1, native signed72=+127
    assert not contract_holds(0, True, 1)
    assert not contract_holds(0, 1, 2)


@pytest.mark.parametrize("width,fraction_bits,count_bits", [
    (0, 0, 1), (True, 0, 1), (4, -1, 2), (4, 5, 2), (4, True, 2),
    (4, 0, 0), (4, 0, 5), (4, 0, True), (4, 0, 2.0),
])
def test_invalid_width_and_contract_parameters_rejected(width, fraction_bits, count_bits):
    with pytest.raises(ValueError):
        leaf_spec(width, fraction_bits, count_bits)
    with pytest.raises(ValueError):
        build_narrow_shift(width, fraction_bits, count_bits)


def test_spec_fraction_independence_and_measured_production_resources():
    spec = leaf_spec()
    assert spec["lowering"] == LOWERING
    assert spec["input_contract"] == input_contract() == {"signed_shift_count_bits": 7}
    assert spec["op"] == "shift" and spec["params"] == {}
    zero_fraction, _, _ = build_narrow_shift(8, 0, 7)
    full_fraction, _, _ = build_narrow_shift(8, 8, 7)
    assert np.array_equal(array_gates(zero_fraction), array_gates(full_fraction))
    new, _, _ = production_leaf()
    old, _, _ = build("shift", 72, 40)
    candidate, baseline = resources(new), resources(old)
    assert candidate["qubits"] < baseline["qubits"]
    assert candidate["t_count"] < baseline["t_count"]
    assert candidate["t_depth"] < baseline["t_depth"]
    assert candidate["clifford_t_depth"] < baseline["clifford_t_depth"]
    assert candidate["x"] == 0
    assert candidate["ccx"] == 2 * (72 * 7 + 72 + 6 + 1)
