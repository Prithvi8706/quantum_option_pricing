"""Unsigned restoring divider with a proved denominator-width interface.

The emitted X/CX/CCX leaf preserves both full input words, XORs the low output
word into an arbitrary dirty word, and cleans every scratch wire. Actual
quantile dispatch, nonzero/range proof and source adoption are separate.
This file is authored only until the Stage C timing slot is clear.
"""

from __future__ import annotations

from research.journal_sprint.reversible_fixed_point import (
    Program,
    copy,
    less_than,
    subtract,
)

LOWERING = "unsigned-restoring-denominator-width-clean-xor-v1"


def validate_parameters(width, fraction_bits, denominator_bits):
    if type(width) is not int or width < 1:
        raise ValueError("Positive integer full native width required")
    if type(fraction_bits) is not int or not 0 <= fraction_bits <= width:
        raise ValueError("Integer fractional width within the native word required")
    if type(denominator_bits) is not int or not 1 <= denominator_bits <= width:
        raise ValueError("Positive integer denominator width within the native word required")


def contract_holds(numerator, denominator, width, denominator_bits):
    """Guard the full unsigned inputs; zero retains the old all-ones behavior."""
    return (
        type(numerator) is int
        and type(denominator) is int
        and type(width) is int
        and type(denominator_bits) is int
        and 1 <= denominator_bits <= width
        and 0 <= numerator < 1 << width
        and 0 <= denominator < 1 << denominator_bits
    )


def expected_quotient(numerator, denominator, width, fraction_bits, denominator_bits):
    validate_parameters(width, fraction_bits, denominator_bits)
    if not contract_holds(numerator, denominator, width, denominator_bits):
        raise ValueError("Unsigned denominator-width input guard failed")
    mask = (1 << width) - 1
    return mask if denominator == 0 else ((numerator << fraction_bits) // denominator) & mask


def leaf_spec(width, fraction_bits, denominator_bits):
    validate_parameters(width, fraction_bits, denominator_bits)
    return dict(
        op="divide",
        width=width,
        fraction_bits=fraction_bits,
        denominator_bits=denominator_bits,
        lowering=LOWERING,
        unsigned_inputs=True,
        input_contract={"unsigned_denominator_bits": denominator_bits},
        zero_divisor_behavior="Full output mask, matching original unsigned divider",
        division_output="Low width bits of floor((unsigned_a << fraction_bits)/unsigned_b)",
        dirty_output_XOR=True,
        input_words_preserved=True,
        literal_gate_inverse=True,
        scratch_initial_and_final_zero=True,
        unpriced_quantile_sign_restore_and_path_interface=True,
        current_Box_Muller_source_dispatch=False,
    )


def build_bounded_divider(width, fraction_bits, denominator_bits, *, compact=True):
    """Emit every trial compare/subtract and its literal cleanup.

    For positive b<2**d and each processed numerator prefix P, maintain
    P=q*b+r,0<=r<b. Trial t=2*r+next_bit<2*b fits d+1 bits. The comparator
    supplies bit1 exactly when t>=b; subtracting that bit*b returns r'<b.
    Thus the stored remainder's top bit is zero before every subsequent
    shift, including the high-bit denominator boundary. For b=0 every
    comparison gives bit1; every subtraction is zero, so output is all ones.
    Full high denominator wires remain untouched under the declared guard.
    """
    validate_parameters(width, fraction_bits, denominator_bits)
    program = Program(compact=compact)
    numerator = program.register(width)
    denominator = program.register(width)
    output = program.register(width)
    remainder_width = denominator_bits + 1
    steps = width + fraction_bits
    remainders = [program.register(remainder_width) for _ in range(steps + 1)]
    divisor = program.register(remainder_width)
    conditional = program.register(remainder_width)
    quotient = program.register(steps)
    difference = program.register(remainder_width + 1)
    extended = program.register(remainder_width + 1)
    helper = program.register(1)[0]
    start = len(program.gates)
    copy(program, denominator[:denominator_bits], divisor[:denominator_bits])
    for stage, position in enumerate(reversed(range(steps))):
        previous, current = remainders[stage:stage + 2]
        for bit in range(denominator_bits):
            program.gate(previous[bit], current[bit + 1])
        if fraction_bits <= position < fraction_bits + width:
            program.gate(numerator[position - fraction_bits], current[0])
        less_than(program, current, divisor, quotient[position], difference, extended, helper)
        program.gate(quotient[position])
        for bit in range(remainder_width):
            program.gate(quotient[position], divisor[bit], conditional[bit])
        subtract(program, conditional, current, helper)
        for bit in range(remainder_width):
            program.gate(quotient[position], divisor[bit], conditional[bit])
    end = len(program.gates)
    copy(program, quotient[:width], output)
    program.undo(start, end)
    registers = dict(numerator=numerator, denominator=denominator, output=output,
                     scratch=tuple(range(3 * width, program.qubits)))
    return program, registers, leaf_spec(width, fraction_bits, denominator_bits)


def classical_restoring_trace(numerator, denominator, width, fraction_bits, denominator_bits):
    """Independent integer invariants; not a gate-level replay or quantum cost."""
    expected = expected_quotient(
        numerator, denominator, width, fraction_bits, denominator_bits
    )
    prefix, quotient, remainder = 0, 0, 0
    rows = []
    dividend = numerator << fraction_bits
    for position in reversed(range(width + fraction_bits)):
        bit = (dividend >> position) & 1
        prefix = 2 * prefix + bit
        trial = 2 * remainder + bit
        decision = int(trial >= denominator)
        quotient = 2 * quotient + decision
        remainder = trial - decision * denominator
        if denominator:
            assert trial < 2 * denominator
            assert 0 <= remainder < denominator < 1 << denominator_bits
            assert prefix == quotient * denominator + remainder
        else:
            # The gate circuit truncates remainder shifts for b=0; the
            # output mask identity depends only on decision=1 in every step.
            assert decision == 1
        rows.append(dict(position=position, input_bit=bit, quotient_bit=decision,
                         prefix=prefix, quotient_prefix=quotient, remainder=remainder))
    assert quotient & ((1 << width) - 1) == expected
    return rows
