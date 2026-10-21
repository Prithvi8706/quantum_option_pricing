"""Exact signed multiplication on proved, ordered active operand widths.

The native input and XOR-output registers retain their complete width. Each
input's high bits must be its active sign bit, as proved at the actual SSA call.
The product is formed modulo 2**(width+fraction_bits), including every low
column and the full-width correction needed by negative short products.
"""

from research.controlled_source_completion.prefix_multiplier import embed_clean_prefix
from research.journal_sprint.reversible_fixed_point import Program

LOWERING = "signed-range-complement-csa-prefix-final-v1"
ALGORITHM = "ordered-signed-active-planes-brent-kung"
VARIANT = "brent-kung"


def input_contract(left_bits, right_bits):
    """Return an ordered signed-width promise; booleans are not widths."""
    if type(left_bits) is not int or type(right_bits) is not int or left_bits < 1 or right_bits < 1:
        raise ValueError("positive integer active operand widths required")
    return {"signed_operand_bits": [left_bits, right_bits]}


def _validate(width, fraction_bits, left_bits, right_bits):
    input_contract(left_bits, right_bits)
    if (
        type(width) is not int
        or type(fraction_bits) is not int
        or width < 1
        or not 0 <= fraction_bits <= width
        or not 1 <= left_bits <= width
        or not 1 <= right_bits <= width
    ):
        raise ValueError("valid native, fractional and active operand widths required")


def contract_holds(left_word, right_word, width, left_bits, right_bits):
    """Check native words have the promised signed high-bit extension."""
    try:
        _validate(width, 0, left_bits, right_bits)
    except ValueError:
        return False
    mask = (1 << width) - 1
    for word, active in ((left_word, left_bits), (right_word, right_bits)):
        if type(word) is not int or not 0 <= word <= mask:
            return False
        low = word & ((1 << active) - 1)
        signed_low = low - (1 << active) if low >> (active - 1) else low
        if word != signed_low & mask:
            return False
    return True


def signed_range_partial_terms(width, fraction_bits, left_bits, right_bits):
    """Return (a-index,b-index,column,negative), correction modulo full product."""
    _validate(width, fraction_bits, left_bits, right_bits)
    n = width + fraction_bits
    terms, correction = [], 0
    for i in range(right_bits):
        for j in range(min(left_bits, n - i)):
            negative = (i == right_bits - 1) != (j == left_bits - 1)
            terms.append((j, i, i + j, negative))
            if negative:
                correction -= 1 << (i + j)
    # A short negative product still needs ones through native product bit n-1.
    # Masking at left_bits+right_bits would destroy its arithmetic right shift.
    return terms, correction & ((1 << n) - 1)


def leaf_spec(width, fraction_bits, left_bits, right_bits):
    _validate(width, fraction_bits, left_bits, right_bits)
    return {
        "op": "mul",
        "width": width,
        "fraction_bits": fraction_bits,
        "params": {},
        "variant": VARIANT,
        "lowering": LOWERING,
        "algorithm": ALGORITHM,
        "active_operand_bits": [left_bits, right_bits],
        "product_width": width + fraction_bits,
        "domain": "each native operand is the sign extension of its active low word",
        "signed_partial_rule": "negative iff exactly one operand bit is its active sign bit",
        "negative_bit_encoding": "complement plus fixed negative weight correction",
        "correction_modulus": "full native width plus fractional width",
        "discarded_low_columns": "retained through CSA and final prefix carry",
        "cleanup": "native output XOR; literal inverse of complete compute",
        "input_contract": input_contract(left_bits, right_bits),
    }


def build_range_multiplier(width, fraction_bits, left_bits, right_bits):
    """XOR floor(signed(a)*signed(b)/2**f) mod2**w, under both width promises."""
    terms, correction = signed_range_partial_terms(
        width,
        fraction_bits,
        left_bits,
        right_bits,
    )
    n = width + fraction_bits
    program = Program(compact=True)
    a, b, out = (program.register(width) for _ in range(3))
    columns = [[] for _ in range(n)]
    start = len(program.gates)
    # Exactly-one-sign partials have negative weight. Complementing a bit and
    # subtracting its fixed weight represents that contribution modulo2**n.
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
    # Retain all old wires until the final inverse. Carries leaving column n-1
    # are discarded only because the complete product is modular at bit n.
    while max(map(len, columns)) > 2:
        following = [[] for _ in range(n)]
        for column, values in enumerate(columns):
            consumed = 0
            for offset in range(0, len(values) - 2, 3):
                x, y, z = values[offset : offset + 3]
                summed = program.register(1)[0]
                program.gate(x, summed)
                program.gate(y, summed)
                if column + 1 < n:
                    carry = program.register(1)[0]
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
    embed_clean_prefix(program, left, right, product, VARIANT)
    end = len(program.gates)
    for source, target in zip(product[fraction_bits : fraction_bits + width], out):
        program.gate(source, target)
    program.undo(start, end)
    return program, [a, b], [out]
