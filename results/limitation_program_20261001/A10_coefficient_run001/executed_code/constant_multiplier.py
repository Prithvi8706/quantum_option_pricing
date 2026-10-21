"""Exact constant multiplication with an explicit zero-low-bit input contract.

Input/output words retain the original width and clean XOR interface. The
contract is a static promise proved by the caller; this circuit does not check
it dynamically. General callers must use zero_bits=0.
"""

from research.journal_sprint.reversible_fixed_point import Program, add, copy, subtract


LOWERING = "signed-constant-zero-low-v1"
STRATEGIES = (
    "binary-shift-add", "signed-digit-shift-add",
    "binary-carry-save", "signed-digit-carry-save",
)


def signed_digits(coefficient, form="signed-digit"):
    """Exact binary or nonadjacent signed-digit expansion of an integer."""
    if type(coefficient) is not int or form not in ("binary", "signed-digit"):
        raise ValueError("integer coefficient and known digit form required")
    value, position, result = abs(coefficient), 0, []
    polarity = -1 if coefficient < 0 else 1
    while value:
        if value & 1:
            digit = 1 if form == "binary" else 2 - (value & 3)
            result.append((position, polarity * digit))
            value -= digit
        value //= 2
        position += 1
    return result


def has_zero_low_proof(node, producers, fraction):
    """Accept a syntactic zero-low proof in this same SSA graph, never c alone."""
    if node["op"] != "cmul" or len(node["args"]) != 1:
        return False
    producer = producers.get(node["args"][0])
    if not producer or producer["op"] != "bits":
        return False
    params = producer["params"]
    return type(params.get("shift")) is int and params["shift"] <= -fraction


def build_constant_multiplier(width, fraction, coefficient, zero_bits=0,
                              strategy="signed-digit-carry-save"):
    """XOR floor(signed(x)*coefficient/2**fraction) into a full-width output.

    Requires x mod 2**zero_bits = 0. Then signed(x) equals the signed upper
    (width-zero_bits) bits times 2**zero_bits, so only fraction-zero_bits
    product bits need be discarded. No input sign or coefficient rounding is
    changed. All emitted gates are exact X/CX/CCX.
    """
    if any(type(value) is not int for value in (width, fraction, coefficient, zero_bits)):
        raise ValueError("integer parameters required")
    if width < 1 or not 0 <= fraction <= width or not 0 <= zero_bits < width:
        raise ValueError("invalid widths or zero-bit contract")
    if zero_bits > fraction or strategy not in STRATEGIES:
        raise ValueError("invalid fraction or strategy")
    p = Program(compact=True)
    x, out = p.register(width), p.register(width)
    if coefficient == 0:
        return p, [x], [out]
    form = "binary" if strategy.startswith("binary-") else "signed-digit"
    digits = signed_digits(coefficient, form)
    effective = x[zero_bits:]
    discarded = fraction - zero_bits
    n = width + discarded
    start = len(p.gates)

    if strategy.endswith("shift-add"):
        product, extended = p.register(n), p.register(n)
        helper = p.register(1)[0]
        for index, wire in enumerate(extended):
            p.gate(effective[min(index, len(effective) - 1)], wire)
        for position, digit in digits:
            if position < n:
                operation = add if digit > 0 else subtract
                operation(p, extended[:n - position], product[position:], helper)
    else:
        columns = [[] for _ in range(n)]
        correction = 0
        # Each signed input bit has a known weight: +2**i except the sign bit,
        # whose weight is -2**(m-1). A negative-weight bit can be represented
        # by its complement with a -2**i constant correction, modulo 2**n.
        for position, digit in digits:
            for index, source in enumerate(effective[:max(0, n - position)]):
                column = position + index
                value = p.register(1)[0]
                weight_sign = -digit if index == len(effective) - 1 else digit
                if weight_sign < 0:
                    p.gate(value)
                    correction -= 1 << column
                p.gate(source, value)
                columns[column].append(value)
        correction &= (1 << n) - 1
        for column in range(n):
            if (correction >> column) & 1:
                value = p.register(1)[0]
                p.gate(value)
                columns[column].append(value)
        while max(map(len, columns)) > 2:
            following = [[] for _ in range(n)]
            for column, values in enumerate(columns):
                consumed = 0
                for offset in range(0, len(values) - 2, 3):
                    a, b, c = values[offset:offset + 3]
                    summed = p.register(1)[0]
                    p.gate(a, summed)
                    p.gate(b, summed)
                    if column + 1 < n:
                        carry = p.register(1)[0]
                        p.gate(a, b, carry)
                        p.gate(summed, c, carry)
                        following[column + 1].append(carry)
                    p.gate(c, summed)
                    following[column].append(summed)
                    consumed = offset + 3
                following[column].extend(values[consumed:])
            columns = following
        left, product = p.register(n), p.register(n)
        helper = p.register(1)[0]
        for column, values in enumerate(columns):
            if values:
                p.gate(values[0], left[column])
            if len(values) == 2:
                p.gate(values[1], product[column])
        add(p, left, product, helper)
    stop = len(p.gates)
    copy(p, product[discarded:discarded + width], out)
    p.undo(start, stop)
    return p, [x], [out]
