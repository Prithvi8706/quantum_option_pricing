"""Exact signed truncated multiplication using a clean carry-save tree.

Trades additional clean workspace for less sequential arithmetic. Never silently
replaces the compact multiplier: callers must choose a workspace budget.
"""

from research.journal_sprint.reversible_fixed_point import Program, add, copy, subtract


LOWERING = "carry-save-signed-truncated-v1"


def build_multiplier(width, fraction):
    if type(width) is not int or width < 1 or type(fraction) is not int:
        raise ValueError("integer width and fraction required")
    if not 0 <= fraction <= width:
        raise ValueError("fraction must lie in [0,width]")
    p = Program(compact=True)
    a, b, out = (p.register(width) for _ in range(3))
    n = width + fraction
    columns = [[] for _ in range(n)]
    start = len(p.gates)
    for i in range(width):
        for j in range(min(width, n - i)):
            product = p.register(1)[0]
            p.gate(a[j], b[i], product)
            columns[i + j].append(product)
    while max(map(len, columns)) > 2:
        following = [[] for _ in range(n)]
        for index, bits in enumerate(columns):
            consumed = 0
            for offset in range(0, len(bits) - 2, 3):
                x, y, z = bits[offset:offset + 3]
                summed = p.register(1)[0]
                p.gate(x, summed)
                p.gate(y, summed)
                if index + 1 < n:
                    carry = p.register(1)[0]
                    # Majority(x,y,z) = x*y XOR (x XOR y)*z.
                    p.gate(x, y, carry)
                    p.gate(summed, z, carry)
                    following[index + 1].append(carry)
                p.gate(z, summed)
                following[index].append(summed)
                consumed = offset + 3
            following[index].extend(bits[consumed:])
        columns = following
    left, product = p.register(n), p.register(n)
    helper = p.register(1)[0]
    for index, bits in enumerate(columns):
        if bits:
            p.gate(bits[0], left[index])
        if len(bits) == 2:
            p.gate(bits[1], product[index])
    add(p, left, product, helper)
    # signed(A)*signed(B) = A*B - sign(A)*B*2**w - sign(B)*A*2**w
    # modulo 2**(w+f). The double-sign term vanishes because f <= w.
    if fraction:
        correction = p.register(fraction)
        for sign, operand in ((a[-1], b), (b[-1], a)):
            first = len(p.gates)
            for j in range(fraction):
                p.gate(sign, operand[j], correction[j])
            last = len(p.gates)
            subtract(p, correction, product[width:], helper)
            p.undo(first, last)
    stop = len(p.gates)
    copy(p, product[fraction:fraction + width], out)
    p.undo(start, stop)
    return p, [a, b], [out]
