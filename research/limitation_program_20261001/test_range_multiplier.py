"""Independent signed-domain, exact floor, carry and clean-XOR leaf checks."""

from functools import lru_cache
import random

from numba import njit
import numpy as np
import pytest

from research.controlled_source_completion.prefix_multiplier import (
    build_prefix_multiplier,
    signed_partial_terms,
)
from research.controlled_source_completion.primitives import array_gates, basis_run, run_gates
from research.controlled_source_completion.range_multiplier import (
    ALGORITHM,
    LOWERING,
    VARIANT,
    build_range_multiplier,
    contract_holds,
    input_contract,
    leaf_spec,
    signed_range_partial_terms,
)


@njit(cache=True)
def exhaustive_signed_words(gates, qubits, width, fraction_bits, left_bits, right_bits):
    """Signed integers supply expected values, independently of the partial plane."""
    native_limit, count = 1 << width, 0
    for left_low in range(1 << left_bits):
        left = left_low - (1 << left_bits) if left_low >> (left_bits - 1) else left_low
        left_word = left & (native_limit - 1)
        for right_low in range(1 << right_bits):
            right = right_low - (1 << right_bits) if right_low >> (right_bits - 1) else right_low
            right_word = right & (native_limit - 1)
            expected = (left * right >> fraction_bits) & (native_limit - 1)
            for initial_index in range(native_limit if width <= 3 else 3):
                initial = (
                    initial_index
                    if width <= 3
                    else (
                        0
                        if initial_index == 0
                        else native_limit - 1
                        if initial_index == 1
                        else native_limit >> 1
                    )
                )
                for inverse in (False, True):
                    state = np.zeros(qubits, np.uint8)
                    for bit in range(width):
                        state[bit] = (left_word >> bit) & 1
                        state[width + bit] = (right_word >> bit) & 1
                        state[2 * width + bit] = (initial >> bit) & 1
                    run_gates(gates, state, inverse)
                    for bit in range(width):
                        if state[bit] != (left_word >> bit) & 1:
                            return False, count, left, right, initial, inverse, 1
                        if state[width + bit] != (right_word >> bit) & 1:
                            return False, count, left, right, initial, inverse, 2
                        if state[2 * width + bit] != ((expected ^ initial) >> bit) & 1:
                            return False, count, left, right, initial, inverse, 3
                    for wire in range(3 * width, qubits):
                        if state[wire]:
                            return False, count, left, right, initial, inverse, 4
                    count += 1
    return True, count, 0, 0, 0, False, 0


@pytest.mark.parametrize("width", range(1, 6))
def test_every_small_active_pair_fraction_native_dirty_word_and_inverse(width):
    for fraction_bits in range(width + 1):
        for left_bits in range(1, width + 1):
            for right_bits in range(1, width + 1):
                program, _, _ = build_range_multiplier(width, fraction_bits, left_bits, right_bits)
                report = exhaustive_signed_words(
                    array_gates(program),
                    program.qubits,
                    width,
                    fraction_bits,
                    left_bits,
                    right_bits,
                )
                assert report[0], (width, fraction_bits, left_bits, right_bits, report)
                outputs = (1 << width) if width <= 3 else 3
                assert report[1] == 2 * outputs * (1 << (left_bits + right_bits))


def test_full_modulus_signed_partial_identity_exhaustively_including_short_products():
    for width in range(1, 6):
        native_mask = (1 << width) - 1
        for fraction_bits in range(width + 1):
            full_mask = (1 << (width + fraction_bits)) - 1
            for left_bits in range(1, width + 1):
                for right_bits in range(1, width + 1):
                    terms, correction = signed_range_partial_terms(
                        width,
                        fraction_bits,
                        left_bits,
                        right_bits,
                    )
                    expected_indices = {
                        (j, i)
                        for i in range(right_bits)
                        for j in range(left_bits)
                        if i + j < width + fraction_bits
                    }
                    assert {(j, i) for j, i, _, _ in terms} == expected_indices
                    assert len(terms) == len(expected_indices)
                    for left in range(-(1 << (left_bits - 1)), 1 << (left_bits - 1)):
                        for right in range(-(1 << (right_bits - 1)), 1 << (right_bits - 1)):
                            represented = correction
                            for j, i, column, negative in terms:
                                bit = ((left >> j) & 1) & ((right >> i) & 1)
                                assert negative == ((j == left_bits - 1) != (i == right_bits - 1))
                                represented += ((1 - bit) if negative else bit) << column
                            residue = represented & full_mask
                            assert residue == (left * right) & full_mask
                            assert (
                                residue >> fraction_bits
                                == (left * right >> fraction_bits) & native_mask
                            )


def test_negative_control_short_modulus_loses_negative_floor_and_high_ones():
    width, fraction_bits, left_bits, right_bits = 8, 6, 2, 2
    terms, correction = signed_range_partial_terms(width, fraction_bits, left_bits, right_bits)
    left, right = -1, 1
    complemented = sum(
        (
            (1 - (((left >> j) & 1) & ((right >> i) & 1)))
            if negative
            else (((left >> j) & 1) & ((right >> i) & 1))
        )
        << column
        for j, i, column, negative in terms
    )
    assert correction >> (left_bits + right_bits) != 0
    full = (complemented + correction) & ((1 << (width + fraction_bits)) - 1)
    assert full >> fraction_bits == 255 == (left * right >> fraction_bits) & 255
    wrong = (complemented + correction) & ((1 << (left_bits + right_bits)) - 1)
    assert wrong >> fraction_bits != 255


def test_negative_control_low_partial_carries_are_required_for_exact_rounding():
    # The positive 3*3 product has two carries from discarded low columns.
    terms, _ = signed_range_partial_terms(8, 2, 3, 4)
    retained_only = sum(
        (((3 >> j) & 1) & ((3 >> i) & 1)) << column
        for j, i, column, negative in terms
        if column >= 2 and not negative
    )
    assert retained_only >> 2 == 1
    assert (3 * 3) >> 2 == 2


def signed_vectors(left_bits, right_bits, fraction_bits, random_count=32):
    def edges(bits):
        low, high = -(1 << (bits - 1)), (1 << (bits - 1)) - 1
        return sorted(
            value
            for value in {low, low + 1, -2, -1, 0, 1, 2, 3, high - 1, high}
            if low <= value <= high
        )

    values = {(left, right) for left in edges(left_bits) for right in edges(right_bits)}
    for bits, on_left in ((left_bits, True), (right_bits, False)):
        for bit in range(bits - 1):
            for value in ((1 << bit) - 1, 1 << bit, -(1 << bit)):
                values.add((value, -1) if on_left else (-1, value))
    for left, right in ((-1, 1), (1, -1), (-1, -1), (3, 3)):
        if -(1 << (left_bits - 1)) <= left < 1 << (left_bits - 1):
            if -(1 << (right_bits - 1)) <= right < 1 << (right_bits - 1):
                values.add((left, right))
    # Fractional-scale neighbors stay in the actual active signed domains.
    for bit in (fraction_bits - 1, fraction_bits, fraction_bits + 1):
        if 0 <= bit < left_bits - 1:
            values.update((((1 << bit) - 1, 3), (1 << bit, -3)))
        if 0 <= bit < right_bits - 1:
            values.update(((3, (1 << bit) - 1), (-3, 1 << bit)))
    rng = random.Random(20261002 + 100 * left_bits + right_bits + fraction_bits)
    values.update(
        (
            rng.randrange(-(1 << (left_bits - 1)), 1 << (left_bits - 1)),
            rng.randrange(-(1 << (right_bits - 1)), 1 << (right_bits - 1)),
        )
        for _ in range(random_count)
    )
    return sorted(values)


@lru_cache
def generic_leaf(width, fraction_bits):
    return build_prefix_multiplier(width, fraction_bits, VARIANT)


@pytest.mark.parametrize(
    "width,fraction_bits,left_bits,right_bits",
    [
        (24, 12, 7, 24),
        (40, 23, 24, 40),
        (72, 40, 24, 24),
        (72, 40, 24, 40),
        (72, 40, 24, 72),
        (72, 40, 40, 24),
        (72, 40, 40, 40),
        (72, 40, 40, 72),
        (72, 40, 72, 24),
        (72, 40, 72, 40),
    ],
)
def test_native24_40_72_signed_extrema_power_neighbors_randoms_generic_equivalence(
    width,
    fraction_bits,
    left_bits,
    right_bits,
):
    program, args, outs = build_range_multiplier(width, fraction_bits, left_bits, right_bits)
    old, old_args, old_outs = generic_leaf(width, fraction_bits)
    mask, rng = (1 << width) - 1, random.Random(20261003 + left_bits + right_bits)
    for index, (left, right) in enumerate(signed_vectors(left_bits, right_bits, fraction_bits)):
        left_word, right_word = left & mask, right & mask
        assert contract_holds(left_word, right_word, width, left_bits, right_bits)
        expected = (left * right >> fraction_bits) & mask
        for initial in (0, rng.getrandbits(width) | (1 << (width - 1))):
            answer = ([initial ^ expected], True, True)
            for inverse in (False, True):
                assert (
                    basis_run(program, args, outs, [left_word, right_word], [initial], inverse)[:3]
                    == answer
                )
            if index < 32 or index % 17 == 0:
                assert (
                    basis_run(old, old_args, old_outs, [left_word, right_word], [initial])[:3]
                    == answer
                )


@pytest.mark.parametrize(
    "width,fraction_bits,left_bits,right_bits",
    [
        (1, 0, 1, 1),
        (8, 8, 2, 3),
        (24, 12, 7, 24),
        (72, 40, 24, 72),
        (72, 40, 40, 40),
        (72, 40, 72, 24),
    ],
)
def test_native_registers_promised_high_bits_unused_and_literal_compute_copy_inverse(
    width,
    fraction_bits,
    left_bits,
    right_bits,
):
    program, args, outs = build_range_multiplier(width, fraction_bits, left_bits, right_bits)
    assert args == [tuple(range(width)), tuple(range(width, 2 * width))]
    assert outs == [tuple(range(2 * width, 3 * width))]
    input_wires, output_wires = set(args[0] + args[1]), set(outs[0])
    unused = set(args[0][left_bits:] + args[1][right_bits:])
    assert all(gate[-1] not in input_wires for gate in program.gates)
    assert all(not set(gate) & unused for gate in program.gates)
    assert all(not set(gate[:-1]) & output_wires for gate in program.gates)
    assert (len(program.gates) - width) % 2 == 0
    boundary = (len(program.gates) - width) // 2
    forward = program.gates[:boundary]
    middle = program.gates[boundary : boundary + width]
    assert program.gates[boundary + width :] == list(reversed(forward))
    assert all(not set(gate) & output_wires for gate in forward)
    assert len(middle) == width and all(len(gate) == 2 for gate in middle)
    product_base = middle[0][0] - fraction_bits
    assert middle == [(product_base + fraction_bits + bit, 2 * width + bit) for bit in range(width)]


def test_unrestricted_pair_matches_original_partial_terms_and_gate_bytes():
    for width, fraction_bits in ((1, 0), (5, 3), (24, 12)):
        assert signed_range_partial_terms(
            width, fraction_bits, width, width
        ) == signed_partial_terms(width, fraction_bits)
        program, args, outs = build_range_multiplier(width, fraction_bits, width, width)
        old, old_args, old_outs = generic_leaf(width, fraction_bits)
        assert args == old_args and outs == old_outs and program.qubits == old.qubits
        assert np.array_equal(array_gates(program), array_gates(old))


@pytest.mark.parametrize(
    "parameters",
    [
        (0, 0, 1, 1),
        (72, -1, 24, 72),
        (72, 73, 24, 72),
        (72, 40, 0, 72),
        (72, 40, 24, 0),
        (72, 40, 73, 72),
        (72, 40, 24, 73),
        (True, 0, 1, 1),
        (72, True, 24, 72),
        (72, 40, True, 72),
        (72, 40, 24, True),
        (72.0, 40, 24, 72),
        (72, 40.0, 24, 72),
        (72, 40, 24.0, 72),
        (72, 40, 24, 72.0),
    ],
)
def test_invalid_native_fractional_and_ordered_active_widths(parameters):
    for function in (build_range_multiplier, leaf_spec, signed_range_partial_terms):
        with pytest.raises(ValueError):
            function(*parameters)


def test_versioned_ordered_contract_exact_domain_and_boolean_rejection():
    spec = leaf_spec(72, 40, 24, 72)
    assert spec["lowering"] == LOWERING and spec["algorithm"] == ALGORITHM
    assert spec["variant"] == "brent-kung" and spec["product_width"] == 112
    assert spec["active_operand_bits"] == [24, 72]
    assert spec["input_contract"] == input_contract(24, 72) == {"signed_operand_bits": [24, 72]}
    assert input_contract(72, 24) != input_contract(24, 72)
    for invalid in ((True, 72), (24, True), (0, 72), (24, -1), (24.0, 72), (24, 72.0)):
        with pytest.raises(ValueError):
            input_contract(*invalid)
    mask = (1 << 72) - 1
    assert contract_holds((-(1 << 23)) & mask, 1 << 71, 72, 24, 72)
    assert contract_holds((1 << 23) - 1, mask, 72, 24, 72)
    for left, right, width, left_bits, right_bits in (
        (1 << 23, 1, 72, 24, 72),
        (1 << 24, 1, 72, 24, 72),
        (1 << 71, 1, 72, 24, 72),
        (-1, 1, 72, 24, 72),
        (1 << 72, 1, 72, 24, 72),
        (True, 1, 72, 24, 72),
        (0, True, 72, 24, 72),
        (0, 0, True, 24, 72),
        (0, 0, 72, True, 72),
        (0, 0, 72, 24, True),
    ):
        assert not contract_holds(left, right, width, left_bits, right_bits)


@pytest.mark.parametrize(
    "left_bits,right_bits,left_word,right_word",
    [
        (24, 72, 1 << 24, 1 << 40),
        (72, 24, 1 << 40, 1 << 24),
        (24, 72, 1 << 23, 1 << 40),
        (72, 24, 1 << 40, 1 << 23),
    ],
)
def test_invalid_sign_extension_demonstrates_required_both_operand_proofs(
    left_bits,
    right_bits,
    left_word,
    right_word,
):
    width, fraction_bits = 72, 40
    assert not contract_holds(left_word, right_word, width, left_bits, right_bits)
    program, args, outs = build_range_multiplier(width, fraction_bits, left_bits, right_bits)
    result = basis_run(program, args, outs, [left_word, right_word], [0])
    assert result[1:3] == (True, True)
    assert result[0][0] != (left_word * right_word >> fraction_bits) & ((1 << width) - 1)
