"""Classical integer semantics of the unchanged native logarithm/root arithmetic."""

from fractions import Fraction
from math import isqrt


F = 40
W = 72
SCALE = 1 << F
SHIFT = Fraction(8, 5)


def nearest_integer(value):
    lower = value.numerator // value.denominator
    residual = value - lower
    return lower + int(residual > Fraction(1, 2) or (residual == Fraction(1, 2) and lower % 2))


SHIFT_RAW = nearest_integer(SHIFT * SCALE)


def signed72(value):
    value %= 1 << W
    return value - (1 << W) if value >= 1 << (W - 1) else value


def native_log_raw(p_raw, table, ln2_raw):
    """Match Graph.log normalization, clipped table/Horner and exponent product."""
    if type(p_raw) is not int or not 0 < p_raw < SCALE:
        raise ValueError("Positive native f40 input below one required")
    guarded = max(p_raw, 1)
    exponent = guarded.bit_length() - 1 - F
    mantissa = guarded << (-exponent)
    clipped = min(max(mantissa, SCALE), 2 * SCALE - 1)
    index = (clipped - SCALE) >> (F - 5)
    center = SCALE + ((2 * index + 1) << (F - 6))
    local = signed72(clipped - center)
    polynomial = signed72(table[index][-1])
    for coefficient in reversed(table[index][:-1]):
        product = signed72((polynomial * local) >> F)
        polynomial = signed72(product + coefficient)
    # exponent*2^40 is exactly scaled, so signed floor cancels the scale.
    exponent_product = signed72(exponent * ln2_raw)
    result = signed72(polynomial + exponent_product)
    return {
        "exponent": exponent,
        "mantissa_raw": mantissa,
        "table_index": index,
        "local_raw": local,
        "log_raw": result,
        "input_guard_changed": guarded != p_raw,
        "mantissa_clip_changed": clipped != mantissa,
    }


def mathematical_transform_word(raw, table, ln2_raw):
    """A supplied q32 ordinary-tail word; no compiled coherent leaf is executed."""
    if type(raw) is not int or not 0 <= raw < 1 << 32:
        raise ValueError("Unsigned q32 input required")
    uniform_raw = (2 * raw + 1) << 7
    p_raw = min(uniform_raw, SCALE - uniform_raw)
    if Fraction(p_raw, SCALE) >= Fraction(3, 40):
        raise ValueError("Ordinary tail only")
    log = native_log_raw(p_raw, table, ln2_raw)
    # Negation of the ALREADY floored signed log is exact two's complement;
    # it is not a new downward-rounded approximation to -ln(p).
    negative_log = signed72(-log["log_raw"])
    argument = max(negative_log, 0)
    root = isqrt(argument << F)
    transformed = signed72(root - SHIFT_RAW)
    return {
        **log,
        "uniform_raw": uniform_raw,
        "tail_probability_raw": p_raw,
        "negative_log_raw": negative_log,
        "sqrt_argument_raw": argument,
        "sqrt_guard_changed": argument != negative_log,
        "sqrt_raw": root,
        "nearest_shift_raw": SHIFT_RAW,
        "transform_r_raw": transformed,
        "output_sign_negative": raw < 1 << 31,
    }
