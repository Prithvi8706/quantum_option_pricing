"""Exact static QROM with shared address prefixes and a factored constant row.

Only X/CX/CCX gates are emitted. Outputs are XOR targets and need not start zero.
Clean prefix ancillas return to zero. No relative-phase or measurement shortcut
is used, so the verified permutation acts identically on coherent inputs.
"""


LOOKUP_LOWERING = "shared-prefix-xor-v2"


def lookup_shared(p, address, outs, table, bits):
    """Apply out[j] ^= table[address mod 2**bits][j], modulo output widths.

    Unlisted rows are zero, matching the historical equality-scan circuit.
    A prefix P splits into P*x and P*(1-x) using one clean target, two
    Toffolis and two CNOTs for compute, sibling switch, and cleanup.
    """
    if type(bits) is not int or not 0 <= bits <= len(address):
        raise ValueError("lookup bits must fit the address register")
    if not outs or any(not out for out in outs):
        raise ValueError("lookup requires nonempty output registers")
    wires = list(address) + [wire for out in outs for wire in out]
    if len(set(wires)) != len(wires):
        raise ValueError("lookup address and outputs must be disjoint")
    if not table or len(table) > 1 << bits or any(len(row) != len(outs) for row in table):
        raise ValueError("lookup table shape does not match the interface")

    masks = [(1 << len(out)) - 1 for out in outs]
    rows = [tuple(int(value) & mask for value, mask in zip(row, masks)) for row in table]
    # Missing rows must stay implicit: a sparse wide address is a valid input.
    # A zero base lets every wholly absent subtree prune without materializing
    # 2**bits rows. Full tables retain the factored constant-row optimization.
    base = rows[0] if len(rows) == 1 << bits else tuple(0 for _ in outs)
    for out, value in zip(outs, base):
        for bit, wire in enumerate(out):
            if (value >> bit) & 1:
                p.gate(wire)
    residual = [tuple(a ^ b for a, b in zip(row, base)) for row in rows]
    if bits == 0 or not any(any(row) for row in residual):
        return

    # Allocate only a reusable stack, rather than one flag for each table row.
    scratch = p.register(bits - 1) if bits > 1 else ()

    def emit_row(index, control):
        for out, value in zip(outs, residual[index]):
            for bit, wire in enumerate(out):
                if (value >> bit) & 1:
                    p.gate(control, wire)

    def visit(level, prefix, start):
        # Explicit depth-first frames preserve compute/high/switch/low/cleanup
        # gate order without imposing Python's recursion limit on address size.
        pending = [(level, prefix, start, 0)]
        while pending:
            level, prefix, start, phase = pending.pop()
            if phase:
                p.gate(prefix, scratch[level])
                if phase == 2:
                    p.gate(prefix, address[level], scratch[level])
                continue
            if not any(any(row) for row in residual[start:start + (1 << (level + 1))]):
                continue
            if level < 0:
                emit_row(start, prefix)
                continue
            flag = scratch[level]
            p.gate(prefix, address[level], flag)
            pending.extend([
                (level, prefix, start, 2),
                (level - 1, flag, start, 0),
                (level, prefix, start, 1),
                (level - 1, flag, start + (1 << level), 0),
            ])

    high = address[bits - 1]
    visit(bits - 2, high, 1 << (bits - 1))
    p.gate(high)
    visit(bits - 2, high, 0)
    p.gate(high)
