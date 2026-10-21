"""Exact signed symmetric square under a same-SSA-argument promise.

The native clean-XOR interface has two full-width inputs and one full-width
output. Only the first input is read: the caller must prove both arguments
denote the same SSA value, rather than relying on accidental runtime equality.
All low product columns are retained until the final carry propagation.
"""

from __future__ import annotations

from research.controlled_source_completion.prefix_multiplier import embed_clean_prefix
from research.journal_sprint.reversible_fixed_point import Program

VARIANTS = ("brent-kung",)
LOWERING = "same-ssa-signed-square-csa-prefix-v1"


def signed_square_terms(width, fraction_bits):
    """Return (i,j,column,negative) terms, i<=j, and modular correction.

    With s_i=+1 except s_(w-1)=-1, x*x is the sum of diagonal
    x_i*2**(2*i) and off-diagonal s_i*s_j*x_i*x_j*2**(i+j+1).
    A negative bit -t*2**k is represented by (1-t)*2**k-2**k.
    Columns >=w+f vanish modulo2**(w+f); no low columns are dropped.
    """
    if type(width) is not int or width < 1 or type(fraction_bits) is not int:
        raise ValueError("integer width and fraction required")
    if not 0 <= fraction_bits <= width:
        raise ValueError("fraction must lie in [0,width]")
    n = width + fraction_bits
    terms, correction = [], 0
    for i in range(width):
        for j in range(i, width):
            column = 2 * i if i == j else i + j + 1
            if column >= n:
                continue
            negative = i != j and ((i == width - 1) != (j == width - 1))
            terms.append((i, j, column, negative))
            if negative:
                correction -= 1 << column
    return terms, correction & ((1 << n) - 1)


def input_contract():
    """The proof required for dispatch; register equality is not inferred."""
    return {"same_ssa_arguments": True}


def validate_same_ssa_arguments(width, values):
    """Reject malformed or unequal raw words at an explicit contract boundary.

    This predicate verifies a concrete invocation. A source compiler must also
    establish identical SSA argument identifiers for the whole input domain.
    The reversible circuit itself does not measure or check equality.
    """
    signed_square_terms(width, 0)
    if not isinstance(values, (list, tuple)) or len(values) != 2:
        raise ValueError("two raw argument values required")
    if any(type(value) is not int or not 0 <= value < (1 << width) for value in values):
        raise ValueError("raw arguments must fit the word")
    if values[0] != values[1]:
        raise ValueError("same-SSA square requires equal raw arguments")
    return True


def build_signed_square(width, fraction_bits, variant="brent-kung"):
    """Under a=b, XOR floor(signed(a)**2/2**f) mod2**w; restore scratch.

    For unrestricted a,b this permutation computes the square of a and leaves
    b alone. Therefore it may replace multiplication only with the explicit
    same-SSA proof. Arbitrary output words never control a gate.
    """
    terms, correction = signed_square_terms(width, fraction_bits)
    if variant not in VARIANTS:
        raise ValueError("unknown square prefix variant")
    n = width + fraction_bits
    program = Program(compact=True)
    a, b, out = (program.register(width) for _ in range(3))
    columns = [[] for _ in range(n)]
    start = len(program.gates)
    for i, j, column, negative in terms:
        value = program.register(1)[0]
        if negative:
            program.gate(value)
        if i == j:
            # The two equal bit factors are one bit, including the sign square.
            program.gate(a[i], value)
        else:
            program.gate(a[i], a[j], value)
        columns[column].append(value)
    for column in range(n):
        if (correction >> column) & 1:
            value = program.register(1)[0]
            program.gate(value)
            columns[column].append(value)
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
                    # xy and (x XOR y)z are disjoint; their XOR is majority.
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


def leaf_spec(width, fraction_bits, variant="brent-kung"):
    signed_square_terms(width, fraction_bits)
    if variant not in VARIANTS:
        raise ValueError("unknown square prefix variant")
    return {
        "op": "mul", "width": width, "fraction_bits": fraction_bits,
        "params": {}, "variant": variant, "lowering": LOWERING,
        "input_contract": input_contract(), "product_width": width + fraction_bits,
        "signed_partial_rule": "diagonal positive; off-diagonal negative iff sign cross",
        "diagonal_encoding": "single first-argument bit via CX at column2i",
        "off_diagonal_encoding": "first-argument bit pair via CCX at column i+j+1",
        "negative_bit_encoding": "complement plus fixed negative weight correction",
        "discarded_low_columns": "retained through CSA and final prefix carry",
        "second_argument": "native full-width interface; never read or modified",
    }
