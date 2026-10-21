"""Exact native-width shift with a proved narrow, sign-extended count.

The archived operation is signed(data) << count for nonnegative counts and
arithmetic signed(data) >> -count for negative counts, reduced modulo 2**width.
Only the count is narrow. Both arguments and the arbitrary XOR output retain
their full native width, and all private scratch is restored.
"""

from research.journal_sprint.reversible_fixed_point import Program, copy

LOWERING = "signed-count-narrow-barrel-shift-v1"


def input_contract(count_bits=7):
    """A compiler must prove the actual count SSA value fits signed count_bits."""
    if type(count_bits) is not int or count_bits < 1:
        raise ValueError("positive integer signed count width required")
    return {"signed_shift_count_bits": count_bits}


def contract_holds(value, width=72, count_bits=7):
    """Check a raw native count word is the sign extension of its low bits."""
    if (
        type(width) is not int
        or type(count_bits) is not int
        or not 1 <= count_bits <= width
        or type(value) is not int
        or not 0 <= value < 1 << width
    ):
        return False
    signed = value - (1 << width) if value & (1 << (width - 1)) else value
    return -(1 << (count_bits - 1)) <= signed < 1 << (count_bits - 1)


def leaf_spec(width=72, fraction_bits=40, count_bits=7):
    if (
        type(width) is not int
        or type(fraction_bits) is not int
        or type(count_bits) is not int
        or width < 1
        or not 0 <= fraction_bits <= width
        or not 1 <= count_bits <= width
    ):
        raise ValueError("valid native, fraction and signed-count widths required")
    return {
        "op": "shift",
        "width": width,
        "fraction_bits": fraction_bits,
        "params": {},
        "count_bits": count_bits,
        "input_contract": input_contract(count_bits),
        "lowering": LOWERING,
        "domain": "second native word is sign-extended signed count_bits integer",
        "count_scale": "unscaled integer; fraction_bits does not scale the count",
        "direction": "nonnegative modular left; negative arithmetic right",
        "algorithm": "conditional reversal; unsigned magnitude; one left barrel",
        "embedding": "native compute/output-XOR/literal reverse",
        "oversized": "left zero; arithmetic right all original data sign bits",
    }


def _conditional_reverse(program, word, sign):
    """Fredkin on each disjoint bit pair: two CX and one CCX."""
    for bit in range(len(word) // 2):
        low, high = word[bit], word[-1 - bit]
        program.gate(low, high)
        program.gate(sign, high, low)
        program.gate(low, high)


def build_narrow_shift(width=72, fraction_bits=40, count_bits=7):
    """Emit clean out XOR shift(data,count), under the explicit count promise.

    Conditional reversal converts arithmetic right shifts into a left barrel
    whose incoming bits are the original data sign. The unsigned count_bits
    magnitude represents the minimum signed count exactly (e.g. -64 -> 64).
    Stages whose distance reaches the word width fill the entire word, so this
    construction also handles oversized counts in smaller native words.
    """
    leaf_spec(width, fraction_bits, count_bits)
    program = Program(compact=True)
    data, count, output = (program.register(width) for _ in range(3))
    work = program.register(width)
    magnitude = program.register(count_bits)
    carries = program.register(count_bits - 1) if count_bits > 1 else ()
    fill, difference = program.register(1)[0], program.register(1)[0]
    sign = count[count_bits - 1]
    start = len(program.gates)
    copy(program, data, work)
    _conditional_reverse(program, work, sign)

    # Conditional two's-complement negation. carry_i equals
    # sign AND (all count bits below i are zero), and needs no wide adder.
    program.gate(count[0], magnitude[0])
    for bit in range(1, count_bits):
        previous = sign if bit == 1 else carries[bit - 2]
        carry = carries[bit - 1]
        program.gate(previous, carry)
        program.gate(previous, count[bit - 1], carry)
        program.gate(count[bit], magnitude[bit])
        program.gate(sign, magnitude[bit])
        program.gate(carry, magnitude[bit])
    program.gate(sign, data[-1], fill)

    for bit in range(count_bits):
        distance = 1 << bit
        following = program.register(width)
        for position in range(width):
            old = work[position]
            shifted = work[position - distance] if position >= distance else fill
            target = following[position]
            program.gate(old, target)
            program.gate(old, difference)
            program.gate(shifted, difference)
            program.gate(magnitude[bit], difference, target)
            program.gate(shifted, difference)
            program.gate(old, difference)
        work = following
    _conditional_reverse(program, work, sign)
    end = len(program.gates)
    copy(program, work, output)
    program.undo(start, end)
    return program, [data, count], [output]
