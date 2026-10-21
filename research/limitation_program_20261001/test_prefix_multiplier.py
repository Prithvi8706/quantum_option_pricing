"""Exact signed product proof checks and literal clean-leaf verification."""
from __future__ import annotations

from functools import lru_cache
import random

import numpy as np
from numba import njit
import pytest

from research.controlled_source_completion.carry_lookahead import VARIANTS
from research.controlled_source_completion.carry_save_multiplier import build_multiplier
from research.controlled_source_completion.prefix_multiplier import (
    build_prefix_multiplier, leaf_spec, signed_partial_terms,
)
from research.controlled_source_completion.primitives import (
    array_gates, basis_run, run_gates,
)


@njit(cache=True)
def exhaust_signed(gates, qubits, width, fraction):
    limit, count = 1 << width, 0
    for a in range(limit):
        signed_a = a - limit if a & (limit >> 1) else a
        for b in range(limit):
            signed_b = b - limit if b & (limit >> 1) else b
            expected = (signed_a * signed_b >> fraction) & (limit - 1)
            for initial in (0, limit - 1):
                for inverse in (False, True):
                    state = np.zeros(qubits, np.uint8)
                    for bit in range(width):
                        state[bit] = (a >> bit) & 1
                        state[width + bit] = (b >> bit) & 1
                        state[2 * width + bit] = (initial >> bit) & 1
                    run_gates(gates, state, inverse)
                    observed = 0
                    for bit in range(width):
                        if state[bit] != (a >> bit) & 1:
                            return False, count, a, b, initial, inverse, 1
                        if state[width + bit] != (b >> bit) & 1:
                            return False, count, a, b, initial, inverse, 2
                        observed |= int(state[2 * width + bit]) << bit
                    if observed != expected ^ initial:
                        return False, count, a, b, initial, inverse, 3
                    for wire in range(3 * width, qubits):
                        if state[wire]:
                            return False, count, a, b, initial, inverse, 4
                    count += 1
    return True, count, 0, 0, 0, False, 0


@pytest.mark.parametrize("variant", VARIANTS)
def test_every_small_signed_pair_fraction_boundary_nonzero_output_inverse(variant):
    for width in range(1, 6):
        for fraction in range(width + 1):
            program, args, outs = build_prefix_multiplier(width, fraction, variant)
            report = exhaust_signed(array_gates(program), program.qubits, width, fraction)
            assert report[0], (variant, width, fraction, report)
            assert report[1] == 4 * (1 << (2 * width))
            output_wires = set(outs[0])
            input_wires = set(args[0] + args[1])
            assert all(not (set(gate[:-1]) & output_wires) for gate in program.gates)
            assert all(gate[-1] not in input_wires for gate in program.gates)


def test_signed_partial_complement_correction_and_truncation_theorem_exhaustively():
    for width in range(1, 6):
        limit = 1 << width
        for fraction in range(width + 1):
            terms, correction = signed_partial_terms(width, fraction)
            n, mask = width + fraction, (1 << (width + fraction)) - 1
            expected_indices = {(j, i) for i in range(width) for j in range(width)
                                if i + j < n}
            assert {(j, i) for j, i, _, _ in terms} == expected_indices
            assert len(terms) == len(expected_indices)
            for a in range(limit):
                signed_a = a - limit if a & (limit >> 1) else a
                for b in range(limit):
                    signed_b = b - limit if b & (limit >> 1) else b
                    represented = correction
                    for j, i, column, negative in terms:
                        bit = ((a >> j) & 1) & ((b >> i) & 1)
                        assert negative == ((i == width - 1) != (j == width - 1))
                        represented += ((1 - bit) if negative else bit) << column
                    residue = represented & mask
                    product = signed_a * signed_b
                    assert residue == product & mask
                    assert residue >> fraction == (product >> fraction) & (limit - 1)


def test_negative_controls_for_correction_and_discarded_low_carries():
    terms, correction = signed_partial_terms(3, 2)
    no_correction_zero_product = sum(negative << column for _, _, column, negative in terms)
    assert correction != 0
    assert ((no_correction_zero_product & 31) >> 2) != 0
    assert ((no_correction_zero_product + correction) & 31) >> 2 == 0
    # 3*3 has two low-column carries into retained column2. Dropping low
    # partials before accumulation would produce1 instead of the exact2.
    retained_terms_only = sum(
        (((3 >> j) & 1) & ((3 >> i) & 1)) << (i + j)
        for i in range(4) for j in range(4) if 2 <= i + j < 6
    )
    assert retained_terms_only >> 2 == 1
    assert (3 * 3) >> 2 == 2


def test_csa_majority_xor_and_modular_top_carry():
    for x in (0, 1):
        for y in (0, 1):
            for z in (0, 1):
                carry = (x & y) ^ ((x ^ y) & z)
                assert not ((x & y) and ((x ^ y) & z))
                assert (x ^ y ^ z) + 2 * carry == x + y + z


def production_vectors(width=72):
    mask, sign = (1 << width) - 1, 1 << (width - 1)
    edges = (0, 1, 2, 3, mask, mask - 1, sign, sign - 1, sign + 1,
             1 << 40, (1 << 40) - 1, (1 << 40) + 1)
    values = {(a, b) for a in edges for b in edges}
    for bit in range(width):
        single = 1 << bit
        values.update(((single, single), (single, mask), (mask, single),
                       (single - 1, single - 1), (single - 1, 3)))
    rng = random.Random(20261001)
    values.update((rng.getrandbits(width), rng.getrandbits(width)) for _ in range(64))
    return sorted(values)


@lru_cache
def historical_leaf():
    return build_multiplier(72, 40)


@pytest.mark.parametrize("variant", VARIANTS)
def test_production72_signed_floor_historical_equivalence_nonzero_and_inverse(variant):
    program, args, outs = build_prefix_multiplier(72, 40, variant)
    old, old_args, old_outs = historical_leaf()
    mask = (1 << 72) - 1
    rng = random.Random(20261010)
    for a, b in production_vectors():
        signed_a = a - (1 << 72) if a >> 71 else a
        signed_b = b - (1 << 72) if b >> 71 else b
        expected = (signed_a * signed_b >> 40) & mask
        for initial in (0, rng.getrandbits(72)):
            for inverse in (False, True):
                actual = basis_run(program, args, outs, [a, b], [initial], inverse)[:3]
                assert actual == ([initial ^ expected], True, True), (variant, a, b)
            previous = basis_run(old, old_args, old_outs, [a, b], [initial])[:3]
            assert previous == ([initial ^ expected], True, True)
def test_versioned_unpromised_spec_and_invalid_parameters():
    for variant in VARIANTS:
        spec = leaf_spec(72, 40, variant)
        assert spec["product_width"] == 112 and spec["op"] == "mul"
        assert "input_contract" not in spec
    for args in ((True, 0, "brent-kung"), (0, 0, "brent-kung"),
                 (3, -1, "brent-kung"), (3, 4, "brent-kung"), (3, 2, "unknown")):
        with pytest.raises(ValueError):
            build_prefix_multiplier(*args)
