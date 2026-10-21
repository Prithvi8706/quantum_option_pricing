"""Exact full-domain signed constant multiplication with a prefix final sum.

The native input and XOR-output words retain their complete width. Binary or
nonadjacent signed digits generate a complemented signed bit plane modulo
2**(width+fraction_bits). Every low carry column survives through the fresh
CSA history and the frozen clean Brent-Kung final adder. No narrowed-input or
zero-low promise is used; all compute gates are literally reversed after the
full-width output copy.
"""

from research.controlled_source_completion.constant_multiplier import signed_digits
from research.controlled_source_completion.prefix_multiplier import embed_clean_prefix
from research.journal_sprint.reversible_fixed_point import Program

LOWERING = "signed-constant-complement-csa-prefix-final-v1"
ALGORITHM = "full-domain-signed-constant-planes-brent-kung"
VARIANT = "brent-kung"
STRATEGIES = ("binary-prefix-carry-save", "signed-digit-prefix-carry-save")


def _validate(width, fraction_bits, coefficient, strategy):
    if any(type(value) is not int for value in (width, fraction_bits, coefficient)):
        raise ValueError("integer native width, fractional width and coefficient required")
    if width < 1 or not 0 <= fraction_bits <= width or strategy not in STRATEGIES:
        raise ValueError("valid native/fractional widths and known prefix strategy required")


def signed_constant_partial_terms(width, fraction_bits, coefficient, strategy):
    """Return (input-index,column,negative) and a full-product modular correction."""
    _validate(width, fraction_bits, coefficient, strategy)
    form = "binary" if strategy.startswith("binary-") else "signed-digit"
    n = width + fraction_bits
    terms, correction = [], 0
    for position, digit in signed_digits(coefficient, form):
        for index in range(min(width, max(0, n - position))):
            column = position + index
            # Native two's-complement input has one negative sign-bit weight.
            negative = (-digit if index == width - 1 else digit) < 0
            terms.append((index, column, negative))
            if negative:
                correction -= 1 << column
    return terms, correction & ((1 << n) - 1)


def leaf_spec(width, fraction_bits, coefficient, strategy):
    """Canonical full-domain leaf description; booleans never encode widths/c."""
    _validate(width, fraction_bits, coefficient, strategy)
    return {
        "op": "cmul",
        "width": width,
        "fraction_bits": fraction_bits,
        "params": {"c": coefficient},
        "strategy": strategy,
        "variant": VARIANT,
        "lowering": LOWERING,
        "algorithm": ALGORITHM,
        "zero_bits": 0,
        "product_width": width + fraction_bits,
        "digit_form": "binary" if strategy.startswith("binary-") else "signed-digit",
        "domain": "all native signed input words; no narrowed or zero-low promise",
        "signed_partial_rule": "digit polarity times native two's-complement bit weight",
        "negative_bit_encoding": "complement plus fixed negative weight correction",
        "correction_modulus": "full native width plus fractional width",
        "discarded_low_columns": "retained through CSA and final prefix carry",
        "cleanup": "native output XOR; literal inverse of complete compute",
        "input_contract": {"zero_low_bits": 0},
    }


def build_prefix_constant_multiplier(
    width, fraction_bits, coefficient, strategy="signed-digit-prefix-carry-save"
):
    """XOR floor(signed(x)*coefficient/2**f) mod2**w into an arbitrary output."""
    terms, correction = signed_constant_partial_terms(width, fraction_bits, coefficient, strategy)
    n = width + fraction_bits
    program = Program(compact=True)
    x, out = program.register(width), program.register(width)
    if coefficient == 0:
        return program, [x], [out]
    columns = [[] for _ in range(n)]
    start = len(program.gates)
    # For t in {0,1}, -t*2**k = (1-t)*2**k - 2**k modulo2**n.
    for index, column, negative in terms:
        value = program.register(1)[0]
        if negative:
            program.gate(value)
        program.gate(x[index], value)
        columns[column].append(value)
    for column in range(n):
        if (correction >> column) & 1:
            value = program.register(1)[0]
            program.gate(value)
            columns[column].append(value)
    # Retaining each old source/sum/carry wire permits exact literal cleanup.
    while max(map(len, columns)) > 2:
        following = [[] for _ in range(n)]
        for column, values in enumerate(columns):
            consumed = 0
            for offset in range(0, len(values) - 2, 3):
                a, b, c = values[offset : offset + 3]
                summed = program.register(1)[0]
                program.gate(a, summed)
                program.gate(b, summed)
                if column + 1 < n:
                    carry = program.register(1)[0]
                    program.gate(a, b, carry)
                    program.gate(summed, c, carry)
                    following[column + 1].append(carry)
                program.gate(c, summed)
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
    return program, [x], [out]
