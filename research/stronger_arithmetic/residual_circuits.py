"""Emitted signed degree-four control and shifted-residual threshold kernels.

All words are little endian at scale Q=2**f. The supplied constants are already
quantized integers; this module neither chooses nor certifies them. Every
arithmetic stage wraps at word width. A separate certificate must exclude
overflow, bound quantization error, and prove 0 <= residual+shift < 2**width.
The shifted encoding requires its own normalization/decoder and AE budget.
No continuous-price, residual-error, or statistical claim is made here.
"""

from research.journal_sprint.reversible_fixed_point import (
    Program,
    add,
    constant,
    copy,
    fixed_multiply,
    horner,
    less_than,
    positive_part,
    subtract,
)
from .circuits import _registers


def _constants(width, coefficients, f, reciprocal, scale, shift=0):
    if type(width) is not int or width < 1:
        raise ValueError("positive integer width required")
    if type(f) is not int or not 0 <= f < width:
        raise ValueError("fraction bits must satisfy 0 <= f < width")
    try:
        coefficients = tuple(coefficients)
    except TypeError as error:
        raise ValueError("five integer control coefficients required") from error
    limit = 1 << (width - 1)
    if len(coefficients) != 5 or any(
        type(c) is not int or not -limit <= c < limit for c in coefficients
    ):
        raise ValueError("five representable signed control coefficients required")
    if any(type(c) is not int or not 0 < c < limit for c in (reciprocal, scale)):
        raise ValueError("positive representable signed reciprocal and scale required")
    if type(shift) is not int or not 0 <= shift < 1 << width:
        raise ValueError("representable nonnegative unsigned shift required")
    return coefficients


def _control_compute(p, delta, coefficients, f, reciprocal, scale):
    """Leave intermediate words live; caller must reverse this entire segment."""
    w = len(delta)
    normalized, polynomial, control = (p.register(w) for _ in range(3))
    cword, product, partial = p.register(w), p.register(2 * w), p.register(2 * w)
    helper = p.register(1)[0]
    constant(p, cword, reciprocal)
    fixed_multiply(p, delta, cword, normalized, f, product, partial, helper)
    constant(p, cword, reciprocal)
    horner(p, normalized, polynomial, coefficients, f)
    constant(p, cword, scale)
    fixed_multiply(p, polynomial, cword, control, f, product, partial, helper)
    constant(p, cword, scale)
    return control


def _numerator_compute(p, delta, coefficients, f, reciprocal, scale, shift):
    control = _control_compute(p, delta, coefficients, f, reciprocal, scale)
    w = len(delta)
    numerator, cword, helper = p.register(w), p.register(w), p.register(1)[0]
    positive_part(p, delta, numerator)
    subtract(p, control, numerator, helper)
    constant(p, cword, shift)
    add(p, cword, numerator, helper)
    constant(p, cword, shift)
    return numerator


def clean_control(p, delta, out, coefficients, f, reciprocal, scale):
    """XOR control into out; preserve delta and clean every allocated scratch.

    x = floor(delta*reciprocal/Q)
    y = fixed-point Horner g(x), five ascending-power coefficients
    control = floor(y*scale/Q)

    coefficients = certificate["control_coefficients"] already describes the
    complete monomial g=(x+p4(x))/2. No additional x addition or halving occurs.
    reciprocal = certificate["reciprocal_integer"] approximates Q/(d*B);
    scale = certificate["control_scale_integer"] approximates Q*d*B.
    This matches residual.evaluate_control_integer(sum_integer, certificate)
    when delta = sum_integer - certificate["strike_sum"] and f=24, without
    signed overflow. All fixed products use signed floor rounding.
    out may be nonzero; new scratch must start zero. Program.undo(start) emits
    the full inverse, including outside the clean-workspace subspace.
    """
    delta, out = _registers(p, delta, out)
    if len(out) != len(delta):
        raise ValueError("equal delta/output widths required")
    coefficients = _constants(len(delta), coefficients, f, reciprocal, scale)
    start = len(p.gates)
    control = _control_compute(p, delta, coefficients, f, reciprocal, scale)
    end = len(p.gates)
    copy(p, control, out)
    p.undo(start, end)


def clean_shifted_residual(p, delta, out, coefficients, f, reciprocal, scale, shift):
    """out XOR= max(signed(delta),0) - control(delta) + shift, modulo 2**w.

    shift is an integer at the same Q scale. Its representation and the final
    numerator are unsigned, so values >= 2**(w-1) are supported. The residual
    before shifting is signed. All scratch starts/ends zero; out is arbitrary.
    No redundant outer clean_control invocation: retain its intermediates and
    reverse them once after copying the numerator.
    """
    delta, out = _registers(p, delta, out)
    if len(out) != len(delta):
        raise ValueError("equal delta/output widths required")
    coefficients = _constants(len(delta), coefficients, f, reciprocal, scale, shift)
    start = len(p.gates)
    numerator = _numerator_compute(p, delta, coefficients, f, reciprocal, scale, shift)
    end = len(p.gates)
    copy(p, numerator, out)
    p.undo(start, end)


def residual_payoff_flag(p, delta, selector, flag, coefficients, f, reciprocal, scale, shift):
    """flag XOR= unsigned(selector) < unsigned(shifted residual).

    selector may have 1..width bits and is zero-extended before comparison;
    the numerator is NEVER truncated. For a probability proportional to the
    numerator, separately certify numerator <= 2**len(selector) (strictly <
    2**width for representation). A narrower selector otherwise saturates.
    delta/selector and every scratch wire are preserved, for either flag state.
    Counts include control evaluation, numerator arithmetic, comparator and
    every inverse. This consumes an already computed delta, not row conversion
    or aggregation; those costs must be included by the assembling caller.
    """
    delta, selector, _ = _registers(p, delta, selector, (flag,))
    w = len(delta)
    coefficients = _constants(w, coefficients, f, reciprocal, scale, shift)
    if len(selector) > w:
        raise ValueError("selector width must not exceed delta width")
    extended_selector = p.register(w)
    difference, extended_b, helper = p.register(w + 1), p.register(w + 1), p.register(1)[0]
    start = len(p.gates)
    numerator = _numerator_compute(p, delta, coefficients, f, reciprocal, scale, shift)
    copy(p, selector, extended_selector[: len(selector)])
    end = len(p.gates)
    less_than(p, extended_selector, numerator, flag, difference, extended_b, helper)
    p.undo(start, end)


def residual_program(width, f, coefficients, reciprocal, scale, shift, selector_bits=None):
    """Return (compact Program, delta, selector, flag_wire) for actual costing.

    Only delta, selector, and flag are external wires; all remaining wires are
    clean scratch. Default selector width equals delta width. No loader, delta
    construction, selector Hadamards, AE, offset expectation or decoder costs.
    Pass control_coefficients, reciprocal_integer, control_scale_integer and
    shift_integer directly from the residual certificate, in that order.
    """
    coefficients = _constants(width, coefficients, f, reciprocal, scale, shift)
    if selector_bits is None:
        selector_bits = width
    if type(selector_bits) is not int or not 1 <= selector_bits <= width:
        raise ValueError("selector bits must satisfy 1 <= selector_bits <= width")
    p = Program(compact=True)
    delta, selector, flag = p.register(width), p.register(selector_bits), p.register(1)[0]
    residual_payoff_flag(p, delta, selector, flag, coefficients, f, reciprocal, scale, shift)
    return p, delta, selector, flag
