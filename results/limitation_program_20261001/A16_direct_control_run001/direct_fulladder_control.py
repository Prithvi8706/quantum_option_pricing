"""Direct dirty-carry unitary comparator for the isolated A16 fulladder.

Two complete seven-T Toffolis target the arbitrary carry output directly.
Five logical wires are active. The prior two scratch ABI wires are preserved
and unused; no freshness, measurement, reset or feedforward is needed here.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np

from research.limitation_program_20261001.experiment_temporary_and_fulladder import (
    cyclotomic_add,
    cyclotomic_multiply,
)
from research.limitation_program_20261001.temporary_and_fulladder import (
    ccx_seven_t,
    encode,
    gate,
)


def direct_schedule():
    operations = ccx_seven_t(0, 1, 4)
    operations.append(gate("CX", 0, 1))
    operations.extend(ccx_seven_t(1, 2, 4))
    operations.extend([gate("CX", 1, 3), gate("CX", 2, 3), gate("CX", 0, 1)])
    return operations


def literal_adjoint_array(array):
    if array.dtype != np.dtype(np.int16) or array.ndim != 2 or array.shape[1] != 5:
        raise ValueError("Original int16 five-column primitive array required")
    if set(array[:, 0].tolist()) - {1, 2, 3, 5}:
        raise ValueError("Direct control contains only H/T/Tdag/CX")
    if np.any(array[:, 3:] != -1):
        raise ValueError("Unitary comparator has no measurement or feedforward")
    result = array[::-1].copy()
    for row in result:
        if row[0] in (2, 3):
            row[0] = 5 - row[0]
    return result


def exact_ccx_proof():
    """Verify the dirty-target full CCX in Q(omega), not with floating matrices."""
    zero = (Fraction(0),) * 4
    one = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
    hscale = (Fraction(0), Fraction(1, 2), Fraction(0), Fraction(-1, 2))
    omega = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
    inverse = (Fraction(0), Fraction(0), Fraction(0), Fraction(-1))
    operations = encode(ccx_seven_t(0, 1, 2))
    rows = []
    for source in range(8):
        amplitudes = [zero] * 8
        amplitudes[source] = one
        for code, first, second, condition, result in operations.tolist():
            assert condition == result == -1
            if code == 1:
                following = list(amplitudes)
                for lower in range(8):
                    if (lower >> first) & 1:
                        continue
                    upper = lower | (1 << first)
                    a, b = amplitudes[lower], amplitudes[upper]
                    following[lower] = cyclotomic_multiply(hscale, cyclotomic_add(a, b))
                    following[upper] = cyclotomic_multiply(
                        hscale, cyclotomic_add(a, tuple(-value for value in b))
                    )
                amplitudes = following
            elif code in (2, 3):
                phase = omega if code == 2 else inverse
                amplitudes = [
                    cyclotomic_multiply(value, phase) if (word >> first) & 1 else value
                    for word, value in enumerate(amplitudes)
                ]
            elif code == 5:
                amplitudes = [
                    amplitudes[word ^ ((1 << second) if (word >> first) & 1 else 0)]
                    for word in range(8)
                ]
            else:
                raise AssertionError("Unexpected exact CCX primitive")
        destination = source ^ (((source & 1) & ((source >> 1) & 1)) << 2)
        assert amplitudes[destination] == one
        assert all(value == zero for word, value in enumerate(amplitudes) if word != destination)
        rows.append(
            dict(
                input_word=source,
                output_word=destination,
                exact_nonzero_phase_coefficients=[[1, 1], [0, 1], [0, 1], [0, 1]],
            )
        )
    return rows


def exact_direct_contract(array):
    virtual = encode(ccx_seven_t(0, 1, 2))

    def mapped(mapping):
        rows = virtual.copy()
        for row in rows:
            row[1] = mapping[int(row[1])]
            if row[2] >= 0:
                row[2] = mapping[int(row[2])]
        return rows

    assert array.shape == (34, 5)
    assert np.array_equal(array[:15], mapped({0: 0, 1: 1, 2: 4}))
    assert array[15].tolist() == [5, 0, 1, -1, -1]
    assert np.array_equal(array[16:31], mapped({0: 1, 1: 2, 2: 4}))
    assert array[31:].tolist() == [[5, 1, 3, -1, -1], [5, 2, 3, -1, -1], [5, 0, 1, -1, -1]]
    columns = []
    for source in range(32):
        a, b, c, total, carry = ((source >> bit) & 1 for bit in range(5))
        first = a & b
        temporary_b = a ^ b
        carry ^= first ^ (temporary_b & c)
        total ^= temporary_b ^ c
        restored_b = a ^ temporary_b
        assert restored_b == b
        assert (first ^ (temporary_b & c)) == (a + b + c) // 2
        assert (temporary_b ^ c) == (a + b + c) % 2
        destination = a + 2 * b + 4 * c + 8 * total + 16 * carry
        columns.append(dict(input_word=source, output_word=destination))
    return dict(
        exact_dirty_target_CCX_columns=exact_ccx_proof(),
        exact_dirty_sum_carry_permutation=columns,
        exact_cyclotomic_field="Q(omega), omega^4=-1; H coefficient=(omega-omega^3)/2",
        forward_unitary_preserves_relative_phases_exactly=True,
        arbitrary_unused_scratch_preserved=True,
        logical_fulladder_self_inverse=True,
        inverse_implementation=(
            "Explicit literal adjoint reverses the gate array and exchanges T with Tdag; "
            "the logical XOR channel is also self-inverse."
        ),
        floating_tolerance_is_not_the_formal_proof=True,
        best_possible_unitary_frontier_claim=False,
    )
