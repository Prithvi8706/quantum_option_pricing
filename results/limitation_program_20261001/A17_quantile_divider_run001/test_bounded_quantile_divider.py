"""Independent division arithmetic, dirty outputs, guards and exact gate phases.

This file is authored but must not execute during Stage C exclusive timing.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import product
import json
from pathlib import Path

from numba import njit
import numpy as np
import pytest

from research.controlled_source_completion.primitives import (
    array_gates,
    basis_run,
    build,
    run_gates,
)
from research.limitation_program_20261001.bounded_quantile_divider import (
    build_bounded_divider,
    contract_holds,
    expected_quotient,
    validate_parameters,
)
from research.limitation_program_20261001.temporary_and_fulladder import ccx_seven_t

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"


@njit(cache=True)
def exhaustive_clean_xor(gates, qubits, width, fraction_bits, denominator_bits):
    visits = 0
    for numerator in range(1 << width):
        for denominator in range(1 << denominator_bits):
            answer = ((numerator << fraction_bits) // denominator) if denominator else -1
            answer &= (1 << width) - 1
            for dirty in range(1 << width):
                for inverse in (False, True):
                    state = np.zeros(qubits, np.uint8)
                    for bit in range(width):
                        state[bit] = (numerator >> bit) & 1
                        state[width + bit] = (denominator >> bit) & 1
                        state[2 * width + bit] = (dirty >> bit) & 1
                    run_gates(gates, state, inverse)
                    for bit in range(width):
                        if state[bit] != ((numerator >> bit) & 1):
                            return False, visits, numerator, denominator, dirty, inverse, 1
                        if state[width + bit] != ((denominator >> bit) & 1):
                            return False, visits, numerator, denominator, dirty, inverse, 2
                        if state[2 * width + bit] != (((dirty ^ answer) >> bit) & 1):
                            return False, visits, numerator, denominator, dirty, inverse, 3
                    for wire in range(3 * width, qubits):
                        if state[wire]:
                            return False, visits, numerator, denominator, dirty, inverse, 4
                    visits += 1
    return True, visits, 0, 0, 0, False, 0


@pytest.mark.parametrize("width,fraction_bits,denominator_bits", [(3, 1, 2), (4, 2, 3)])
def test_complete_tiny_domain_dirty_outputs_and_literal_inverse(
    width, fraction_bits, denominator_bits
):
    program, _, _ = build_bounded_divider(width, fraction_bits, denominator_bits)
    report = exhaustive_clean_xor(
        array_gates(program), program.qubits, width, fraction_bits, denominator_bits
    )
    assert report[0], report
    assert report[1] == 2 * (1 << (2 * width + denominator_bits))


@pytest.mark.parametrize("params", [
    (True, 1, 1), (0, 0, 1), (3, 1, 0), (3, 1, 4), (3, 4, 2), (3, 1, True)
])
def test_invalid_width_or_scale_is_rejected(params):
    with pytest.raises(ValueError):
        validate_parameters(*params)


@pytest.mark.parametrize("numerator,denominator", [
    (-1, 1), (1, -1), (1, 1 << 64), (1 << 72, 1), (True, 1), (1, False)
])
def test_invalid_unsigned_or_high_denominator_bits_are_rejected(numerator, denominator):
    assert not contract_holds(numerator, denominator, 72, 64)
    with pytest.raises(ValueError):
        expected_quotient(numerator, denominator, 72, 40, 64)


def test_zero_divisor_mask_and_low_word_overflow_semantics_are_explicit():
    assert expected_quotient(0, 0, 4, 2, 3) == 15
    assert expected_quotient(15, 1, 4, 2, 3) == 12
    assert expected_quotient(15, 7, 4, 2, 3) == 8


def cyclotomic_multiply(left, right):
    result = [Fraction(0)] * 4
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[(i + j) % 4] += a * b * (-1 if i + j >= 4 else 1)
    return tuple(result)


def exact_ccx_phase_columns():
    """Exact Q(omega) check of the paid primitive, including every input phase."""
    zero = (Fraction(0),) * 4
    one = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
    half_root = (Fraction(0), Fraction(1, 2), Fraction(0), Fraction(-1, 2))
    phase = {
        "T": (Fraction(0), Fraction(1), Fraction(0), Fraction(0)),
        "Tdg": (Fraction(0), Fraction(0), Fraction(0), Fraction(-1)),
    }
    operation_list = ccx_seven_t(0, 1, 2)
    assert sum(op.gate in phase for op in operation_list) == 7
    rows = []
    for source in range(8):
        amplitudes = [zero] * 8
        amplitudes[source] = one
        for op in operation_list:
            if op.gate == "CX":
                control, target = op.wires
                new = [zero] * 8
                for index, value in enumerate(amplitudes):
                    out = index ^ (1 << target) if (index >> control) & 1 else index
                    new[out] = value
                amplitudes = new
            elif op.gate in phase:
                target = op.wires[0]
                amplitudes = [cyclotomic_multiply(value, phase[op.gate])
                              if (index >> target) & 1 else value
                              for index, value in enumerate(amplitudes)]
            elif op.gate == "H":
                target = op.wires[0]
                new = [zero] * 8
                for index in range(8):
                    if (index >> target) & 1:
                        continue
                    other = index | (1 << target)
                    a, b = amplitudes[index], amplitudes[other]
                    new[index] = cyclotomic_multiply(
                        half_root, tuple(x + y for x, y in zip(a, b, strict=True))
                    )
                    new[other] = cyclotomic_multiply(
                        half_root, tuple(x - y for x, y in zip(a, b, strict=True))
                    )
                amplitudes = new
            else:
                raise AssertionError("Unexpected primitive phase operation")
        expected = source ^ (((source & 1) & ((source >> 1) & 1)) << 2)
        assert amplitudes == [one if index == expected else zero for index in range(8)]
        rows.append(dict(input=source, output=expected, exact_nonzero_phase=1))
    return rows


def test_actual_seven_t_primitive_has_exact_phase_one_on_all_columns():
    assert len(exact_ccx_phase_columns()) == 8


def native_horner(raw_coefficients, argument):
    result = raw_coefficients[-1]
    for coefficient in reversed(raw_coefficients[:-1]):
        result = (result * argument >> 40) + coefficient
    return result


def production_fixtures():
    central = json.loads((PROGRAM / "A02_quantile_central_run002/central_certificate.json")
                         .read_text(encoding="utf-8"))["native_arithmetic"]
    tail = json.loads((PROGRAM / "A02_quantile_tail_run001/tail_certificate.json")
                      .read_text(encoding="utf-8"))["native_interface"]
    central_upper = Fraction(*central["r_native_upper_exact"]) * (1 << 40)
    arguments = [
        ("central_lower", central, 0),
        ("central_upper", central, central_upper.numerator // central_upper.denominator),
        ("tail_lower", tail, 0),
        ("tail_upper", tail, (321 * (1 << 40)) // 100),
    ]
    fixtures = [dict(label=label,
                     numerator=native_horner(data["native_A_raw_ascending"], argument),
                     denominator=native_horner(data["native_B_raw_ascending"], argument),
                     actual_q32_input_reachability_required=False)
                for label, data, argument in arguments]
    fixtures += [
        dict(label="top_denominator_bit", numerator=(1 << 71) - 1, denominator=1 << 63),
        dict(label="upper_unsigned_boundary", numerator=(1 << 72) - 1,
             denominator=(1 << 64) - 1),
        dict(label="minimum_native_denominator", numerator=(1 << 48) + 123,
             denominator=1 << 40),
        dict(label="zero_divisor_contract", numerator=(1 << 72) - 1, denominator=0),
    ]
    assert len(fixtures) == 8
    assert all(contract_holds(row["numerator"], row["denominator"], 72, 64)
               for row in fixtures)
    return fixtures


@lru_cache(maxsize=1)
def production_pair():
    candidate, registers, _ = build_bounded_divider(72, 40, 64)
    control, arguments, outputs = build("divide", 72, 40)
    return candidate, registers, control, arguments, outputs


def test_fixed_native_candidate_and_original_control_all_dirty_words_both_directions():
    candidate, registers, control, arguments, outputs = production_pair()
    programs = [(candidate, [registers["numerator"], registers["denominator"]],
                 [registers["output"]]), (control, arguments, outputs)]
    dirties = [0, (1 << 72) - 1, int("55" * 9, 16), 1 << 71]
    visits = 0
    for row, dirty, inverse, (program, inputs, targets) in product(
        production_fixtures(), dirties, (False, True), programs
    ):
        a, b = row["numerator"], row["denominator"]
        expected = (((a << 40) // b) if b else -1) & ((1 << 72) - 1)
        observed, clean, preserved, _ = basis_run(
            program, inputs, targets, [a, b], [dirty], inverse=inverse
        )
        assert observed == [dirty ^ expected] and clean and preserved, row["label"]
        visits += 1
    assert visits == 128
