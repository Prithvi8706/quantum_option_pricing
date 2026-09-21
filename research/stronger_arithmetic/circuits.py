"""Development X/CX/CCX kernels with explicit zero-workspace reuse.

Words are little endian, signed two's complement at scale 2**f. Arithmetic
wraps at word width after every operation; callers must certify all ranges
and approximation errors separately. These kernels do not certify pricing.
All newly allocated workspace must start zero and is returned zero, including
on coherent inputs. Outputs use XOR except for clean_row_sum's modular ADD.
"""

from research.journal_sprint.reversible_fixed_point import (
    Program,
    add,
    affine,
    constant,
    copy,
    fixed_multiply,
    horner,
    less_than,
    positive_part,
    subtract,
)


def _registers(p, *registers):
    if not isinstance(p, Program):
        raise ValueError("Program required")
    try:
        words = tuple(tuple(r) for r in registers)
    except TypeError as error:
        raise ValueError("register sequences required") from error
    wires = [b for r in words for b in r]
    if (
        not all(words)
        or any(type(b) is not int or not 0 <= b < p.qubits for b in wires)
        or len(wires) != len(set(wires))
    ):
        raise ValueError("nonempty, allocated, disjoint registers required")
    return words


def _parameters(width, coefficients, f, reductions, spot):
    if type(width) is not int or width < 1:
        raise ValueError("positive integer width required")
    if type(f) is not int or not 0 <= f < width:
        raise ValueError("fraction bits must satisfy 0 <= f < width")
    if type(reductions) is not int or reductions < 0:
        raise ValueError("nonnegative integer reductions required")
    if type(spot) is not int or spot < 0:
        raise ValueError("nonnegative integer spot required")
    try:
        coefficients = tuple(coefficients)
    except TypeError as error:
        raise ValueError("integer coefficient sequence required") from error
    if not coefficients or any(
        type(c) is not int or not -(1 << (width - 1)) <= c < (1 << (width - 1))
        for c in coefficients
    ):
        raise ValueError("nonempty representable signed integer coefficients required")
    while len(coefficients) > 1 and coefficients[-1] == 0:
        coefficients = coefficients[:-1]
    return coefficients


def clean_exp(p, x, out, coefficients, f, reductions, spot):
    """Emit out XOR= spot * square_f**reductions(Horner_f(x >> reductions)).

    Coefficients are ascending-power integers, already quantized at scale
    2**f for exp with spot=1 (no implicit Taylor generation or rescaling).
    The shift is signed floor, including shifts >= width. Every multiplication
    floors before wrapping. Final integer spot scaling has no fixed-point
    shift. Spot is any nonnegative integer; reductions=0, spot=1 preserves
    the parent Horner integer map, including intermediate modular overflow.

    One full product/partial/carry workspace is shared by every Horner and
    squaring step. Stored stage words permit complete Bennett uncomputation;
    the duplicate squaring operand is cleared immediately after each use.
    The inverse is the reversed emitted gate segment (Program.undo).
    """
    x, out = _registers(p, x, out)
    w = len(x)
    if len(out) != w:
        raise ValueError("equal input/output widths required")
    coefficients = _parameters(w, coefficients, f, reductions, spot)
    if reductions == 0 and spot == 1:
        horner(p, x, out, coefficients, f)
        return
    reduced = p.register(w)
    stages = [p.register(w) for _ in range(len(coefficients) + reductions)]
    product, partial = p.register(2 * w), p.register(2 * w)
    cword, duplicate, scaled = p.register(w), p.register(w), p.register(w)
    helper = p.register(1)[0]
    start = len(p.gates)
    for i, target in enumerate(reduced):
        p.gate(x[min(i + reductions, w - 1)], target)
    constant(p, stages[0], coefficients[-1])
    for i, c in enumerate(reversed(coefficients[:-1])):
        fixed_multiply(p, reduced, stages[i], stages[i + 1], f, product, partial, helper)
        constant(p, cword, c)
        add(p, cword, stages[i + 1], helper)
        constant(p, cword, c)
    for i in range(len(coefficients) - 1, len(stages) - 1):
        copy(p, stages[i], duplicate)
        fixed_multiply(p, stages[i], duplicate, stages[i + 1], f, product, partial, helper)
        copy(p, stages[i], duplicate)
    # Multiplication by an integer is a modular shift/add, with no rounding.
    for i in range(w):
        if (spot >> i) & 1:
            add(p, stages[-1][: w - i], scaled[i:], helper)
    end = len(p.gates)
    copy(p, scaled, out)
    p.undo(start, end)


def conversion_program(n, w, affine_row, coefficients, f, reductions=0, spot=1):
    """Return (compact Program, inputs, log, out) for one retained conversion.

    Inputs comprise n individual bits; log/out are w-bit words initially zero.
    All remaining wires are scratch, initially and finally zero, and may be
    remapped to the same physical scratch region across independent rows while
    retaining each row's log/out. No inverse conversion is needed for scratch
    reuse. Reverse the whole block to erase log/out when no longer needed.
    """
    if type(n) is not int or n < 1:
        raise ValueError("positive integer input bit count required")
    coefficients = _parameters(w, coefficients, f, reductions, spot)
    rows = _rows(tuple(range(n)), w, (affine_row,))
    p = Program(compact=True)
    inputs, log, out = p.register(n), p.register(w), p.register(w)
    intercept, cs = rows[0]
    affine(p, inputs, log, intercept, cs)
    clean_exp(p, log, out, coefficients, f, reductions, spot)
    return p, inputs, log, out


def _rows(inputs, width, affine_rows):
    try:
        rows = tuple((a, tuple(cs)) for a, cs in affine_rows)
    except (TypeError, ValueError) as error:
        raise ValueError("rows must be (intercept, bit coefficient sequence)") from error
    if not rows:
        raise ValueError("nonempty affine rows required")
    for a, cs in rows:
        if type(a) is not int or len(cs) != len(inputs) or any(type(c) is not int for c in cs):
            raise ValueError("one integer coefficient per input bit required")
    return rows


def clean_row_sum(p, inputs, out, affine_rows, coefficients, f, reductions=0, spot=1):
    """Emit out += sum_i clean_exp(affine_i(inputs)), modulo output width.

    Rows are (integer intercept, integer coefficients per input BIT), matching
    the frozen affine interface. A single physical conversion allocation is
    reused across rows. Each row emits compute / add / inverse-compute before
    the next row uses those wires. Qubit allocation is independent of row count;
    the emitted gate ledger includes every recomputation. No truth tables.
    """
    inputs, out = _registers(p, inputs, out)
    w = len(out)
    coefficients = _parameters(w, coefficients, f, reductions, spot)
    rows = _rows(inputs, w, affine_rows)
    shared = ()
    helper = p.register(1)[0]
    for intercept, cs in rows:
        template = Program(compact=True)
        local_inputs = template.register(len(inputs))
        log, value = template.register(w), template.register(w)
        affine(template, local_inputs, log, intercept, cs)
        clean_exp(template, log, value, coefficients, f, reductions, spot)
        needed = template.qubits - len(inputs)
        if not shared:
            shared = p.register(needed)
        if len(shared) != needed:
            raise AssertionError("row conversion workspace changed width")
        mapping = inputs + shared
        start = len(p.gates)
        for gate in template.gates:
            p.gate(*(mapping[b] for b in gate))
        end = len(p.gates)
        add(p, tuple(mapping[b] for b in value), out, helper)
        p.undo(start, end)


def raw_payoff_flag(
    p,
    inputs,
    selector,
    flag,
    width,
    fraction_bits,
    affine_rows,
    exp_coefficients,
    strike_sum,
    reductions=0,
    spot=1,
):
    """Clean flag XOR= selector < max(sum(row values)-strike_sum, 0).

    The caller must certify signed intermediates and payoff < 2**len(selector).
    As in the parent interface, strike_sum is already at the fixed-point scale;
    no averaging or selector normalization is silently inserted.
    """
    inputs, selector, _ = _registers(p, inputs, selector, (flag,))
    coefficients = _parameters(width, exp_coefficients, fraction_bits, reductions, spot)
    rows = _rows(inputs, width, affine_rows)
    if not 1 <= len(selector) < width:
        raise ValueError("selector must fit positive signed word")
    if type(strike_sum) is not int or not 0 <= strike_sum < 1 << (width - 1):
        raise ValueError("representable nonnegative integer strike required")
    total, strike, payoff = p.register(width), p.register(width), p.register(width)
    helper = p.register(1)[0]
    difference, extended = p.register(len(selector) + 1), p.register(len(selector) + 1)
    start = len(p.gates)
    clean_row_sum(p, inputs, total, rows, coefficients, fraction_bits, reductions, spot)
    constant(p, strike, strike_sum)
    subtract(p, strike, total, helper)
    positive_part(p, total, payoff)
    end = len(p.gates)
    less_than(p, selector, payoff[: len(selector)], flag, difference, extended, helper)
    p.undo(start, end)
