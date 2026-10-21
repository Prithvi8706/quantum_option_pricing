"""Exact non-restoring unsigned root with native clean-XOR interface.

Only the proved unsigned active-input domain is promised. All signed remainder
history is retained until a literal inverse erases it. The temporary shifted
remainder can overflow its word: each recurrence is performed modulo 2**r,
and its FINAL exact integer remainder lies in the signed r-bit range.
"""

from math import isqrt

from research.journal_sprint.reversible_fixed_point import Program, add, copy

LOWERING = "unsigned-nonrestoring-sqrt-signed-remainder-v1"
ALGORITHM = "signed-remainder-single-cuccaro-add"


def input_contract(active_bits=46):
    if type(active_bits) is not int or active_bits < 1:
        raise ValueError("positive integer active input width required")
    return {"unsigned_input_bits": active_bits}


def contract_holds(value, width=72, active_bits=46):
    return (
        type(width) is int
        and type(active_bits) is int
        and 1 <= active_bits <= width
        and type(value) is int
        and 0 <= value < 1 << active_bits
    )


def leaf_spec(width=72, fraction_bits=40, active_bits=46):
    if (
        type(width) is not int
        or type(fraction_bits) is not int
        or type(active_bits) is not int
        or width < 1
        or not 0 <= fraction_bits <= width
        or not 1 <= active_bits <= width
    ):
        raise ValueError("valid native, fractional and active widths required")
    k = (active_bits + fraction_bits + 1) // 2
    result_bits = isqrt(((1 << active_bits) - 1) << fraction_bits).bit_length()
    if result_bits != k:
        raise ValueError("unexpected exact root width")
    return {
        "op": "sqrt",
        "params": {},
        "width": width,
        "fraction_bits": fraction_bits,
        "active_input_bits": active_bits,
        "domain": "unsigned high bits zero; highest active bit may be one",
        "radicand_bits": active_bits + fraction_bits,
        "result_bits": k,
        "remainder_bits": k + 2,
        "remainder_history_count": k + 1,
        "operand_bits": k + 2,
        "adder_helper_bits": 1,
        "arithmetic": "modulo 2**(k+2); final remainder exact signed integer",
        "recurrence": {
            "initial": "Q=0,R=0",
            "nonnegative_old_R": "R'=4*R+digit-(4*Q+1)",
            "negative_old_R": "R'=4*R+digit+(4*Q+3)",
            "new_root": "Q'=2*Q+int(R'>=0)",
            "operand": "bits0,1=1; higher bits=Q_bit XOR NOT(old_R_sign)",
            "invariant": "R=N-Q**2 if nonnegative else N-(Q+1)**2; Q=isqrt(N)",
            "signed_bound": "-(2*Q+1)<=R<=2*Q; Q<2**stage<=2**k",
        },
        "cleanup": "native output XOR; literal inverse of complete compute",
        "input_contract": input_contract(active_bits),
        "algorithm": ALGORITHM,
        "lowering": LOWERING,
    }


def build_nonrestoring_sqrt(width=72, fraction_bits=40, active_bits=46):
    """Emit out XOR isqrt(unsigned(argument) << f), with private bits erased.

    The argument and output retain their native width. The highest active
    input bit is legal data. Domain validity belongs to a same-SSA graph proof;
    this leaf intentionally ignores the argument's promised-zero high bits.
    """
    spec = leaf_spec(width, fraction_bits, active_bits)
    k, r = spec["result_bits"], spec["remainder_bits"]
    p = Program(compact=True)
    argument, output = p.register(width), p.register(width)
    roots = p.register(k)
    remainders = [p.register(r) for _ in range(k + 1)]
    operand, helper = p.register(r), p.register(1)[0]
    start = len(p.gates)
    for stage in range(k):
        position = k - 1 - stage
        previous, next_remainder = remainders[stage : stage + 2]
        # Exact modulo-word multiplication by four, followed by radicand pair.
        for bit in range(r - 2):
            p.gate(previous[bit], next_remainder[bit + 2])
        for bit in (0, 1):
            source = 2 * position + bit - fraction_bits
            if 0 <= source < active_bits:
                p.gate(argument[source], next_remainder[bit])
        # -(4Q+1) or +(4Q+3). Both have low pair11; higher bits are
        # Q XOR NOT(old sign). Every high complement/sign control is charged.
        operand_start = len(p.gates)
        p.gate(operand[0])
        p.gate(operand[1])
        for bit in range(2, r):
            p.gate(operand[bit])
            p.gate(previous[-1], operand[bit])
            root_bit = position + bit - 1
            if root_bit < k:
                p.gate(roots[root_bit], operand[bit])
        operand_stop = len(p.gates)
        add(p, operand, next_remainder, helper)
        p.undo(operand_start, operand_stop)
        # FINAL recurrence lies in signed r-bit range, so its sign is exact.
        p.gate(roots[position])
        p.gate(next_remainder[-1], roots[position])
    stop = len(p.gates)
    copy(p, roots, output[:k])
    p.undo(start, stop)
    return p, [argument], [output]
