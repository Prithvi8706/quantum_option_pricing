"""Exact signed truncated CSA multiplication with a clean prefix final adder.

Negative-weight signed partial bits are complemented with a fixed modular
correction in the CSA columns. No low columns are discarded before carrying.
This leaf has no narrowed-input promise and preserves arbitrary output XOR.
"""
from __future__ import annotations

from research.controlled_source_completion.carry_lookahead import (
    VARIANTS, build_carry_lookahead,
)
from research.journal_sprint.reversible_fixed_point import Program

LOWERING = "signed-complement-csa-prefix-final-v1"


def signed_partial_terms(width, fraction):
    """Return (a-index,b-index,column,negative) and fixed correction mod2**n."""
    if type(width) is not int or width < 1 or type(fraction) is not int:
        raise ValueError("integer width and fraction required")
    if not 0 <= fraction <= width:
        raise ValueError("fraction must lie in [0,width]")
    n = width + fraction
    terms, correction = [], 0
    for i in range(width):
        for j in range(min(width, n - i)):
            negative = (i == width - 1) != (j == width - 1)
            terms.append((j, i, i + j, negative))
            if negative:
                correction -= 1 << (i + j)
    return terms, correction & ((1 << n) - 1)


def embed_clean_prefix(program, left, right, product, variant):
    """Embed the frozen clean-XOR child, preserving both final CSA rows."""
    width = len(left)
    if len(right) != width or len(product) != width:
        raise ValueError("matching final row widths required")
    registers = left + right + product
    if len(set(registers)) != len(registers):
        raise ValueError("final prefix registers must be disjoint")
    child, args, outs = build_carry_lookahead("add", width, variant)
    expected = tuple(range(3 * width))
    if args[0] + args[1] + outs[0] != expected:
        raise ValueError("unexpected child register layout")
    scratch = program.register(child.qubits - 3 * width)
    mapping = registers + scratch
    for gate in child.gates:
        program.gate(*(mapping[wire] for wire in gate))


def build_prefix_multiplier(width, fraction_bits, variant="brent-kung"):
    """XOR floor(signed(a)*signed(b)/2**f) mod2**w into a full-width output."""
    terms, correction = signed_partial_terms(width, fraction_bits)
    if variant not in VARIANTS:
        raise ValueError("unknown prefix variant")
    n = width + fraction_bits
    program = Program(compact=True)
    a, b, out = (program.register(width) for _ in range(3))
    columns = [[] for _ in range(n)]
    start = len(program.gates)
    # The two sign coefficients multiply: only exactly-one-sign terms are
    # negative. For t in {0,1}, -t*2**k = (1-t)*2**k - 2**k.
    for j, i, column, negative in terms:
        value = program.register(1)[0]
        if negative:
            program.gate(value)
        program.gate(a[j], b[i], value)
        columns[column].append(value)
    for column in range(n):
        if (correction >> column) & 1:
            value = program.register(1)[0]
            program.gate(value)
            columns[column].append(value)
    # Fresh sum/carry wires at each layer preserve all source bits for exact
    # reversal. A carry leaving column n-1 vanishes modulo2**n.
    while max(map(len, columns)) > 2:
        following = [[] for _ in range(n)]
        for column, values in enumerate(columns):
            consumed = 0
            for offset in range(0, len(values) - 2, 3):
                x, y, z = values[offset:offset + 3]
                summed = program.register(1)[0]
                program.gate(x, summed)
                program.gate(y, summed)
                if column + 1 < n:
                    carry = program.register(1)[0]
                    # xy and (x XOR y)z are disjoint, so XOR is majority.
                    program.gate(x, y, carry)
                    program.gate(summed, z, carry)
                    following[column + 1].append(carry)
                program.gate(z, summed)
                following[column].append(summed)
                consumed = offset + 3
            following[column].extend(values[consumed:])
        columns = following
    left, right, product = (program.register(n) for _ in range(3))
    for column, values in enumerate(columns):
        if values:
            program.gate(values[0], left[column])
        if len(values) == 2:
            program.gate(values[1], right[column])
    embed_clean_prefix(program, left, right, product, variant)
    end = len(program.gates)
    for source, target in zip(product[fraction_bits:fraction_bits + width], out):
        program.gate(source, target)
    program.undo(start, end)
    return program, [a, b], [out]


def leaf_spec(width, fraction_bits, variant):
    signed_partial_terms(width, fraction_bits)  # exact validation, including f=w
    if variant not in VARIANTS:
        raise ValueError("unknown prefix variant")
    return {
        "op": "mul", "width": width, "fraction_bits": fraction_bits,
        "params": {}, "variant": variant, "lowering": LOWERING,
        "product_width": width + fraction_bits,
        "signed_partial_rule": "negative iff exactly one operand bit is its sign bit",
        "negative_bit_encoding": "complement plus fixed negative weight correction",
        "discarded_low_columns": "retained through CSA and final prefix carry",
    }
