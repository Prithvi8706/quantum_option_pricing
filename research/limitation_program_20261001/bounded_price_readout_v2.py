"""Rational interval decoding of canonical QPE readout into discounted dollars."""

from fractions import Fraction
from math import factorial

from research.limitation_program_20261001.financial_bounded_schedule import pi_interval


def dyadic_pi_interval(bits=160):
    if type(bits) is not int or bits < 64:
        raise ValueError("at least64 bits for an outward pi enclosure")
    lo, hi = pi_interval()
    scale = 1 << bits
    lower = lo.numerator * scale // lo.denominator
    upper = (hi.numerator * scale + hi.denominator - 1) // hi.denominator
    return Fraction(lower, scale), Fraction(upper, scale)


def price_interval(outcome, M, span=64, terms=60):
    if type(M) is not int or M < 2 or M & (M - 1):
        raise ValueError("power-of-two QPE modulus required")
    if type(outcome) is not int or not 0 <= outcome < M:
        raise ValueError("QPE outcome outside its register")
    if type(span) is not int or span < 1 or type(terms) is not int or terms < 1:
        raise ValueError("positive span and Taylor order required")
    if outcome == 0:
        return Fraction(0), Fraction(0)
    if outcome == M // 2:
        return Fraction(span), Fraction(span)
    folded = min(outcome, M - outcome)
    lo, hi = dyadic_pi_interval()
    x = (2 * lo * folded / M, 2 * hi * folded / M)
    z = (x[0] ** 2, x[1] ** 2)
    polynomial = (Fraction((-1) ** terms, factorial(2 * terms)),) * 2
    for j in range(terms - 1, -1, -1):
        products = [p * zz for p in polynomial for zz in z]
        coefficient = Fraction((-1) ** j, factorial(2 * j))
        polynomial = (min(products) + coefficient, max(products) + coefficient)
    # Derivatives of cosine are bounded by one on the whole real line.
    remainder = x[1] ** (2 * terms + 2) / factorial(2 * terms + 2)
    cos_lo, cos_hi = polynomial[0] - remainder, polynomial[1] + remainder
    return max(Fraction(0), span * (1 - cos_hi) / 2), min(Fraction(span), span * (1 - cos_lo) / 2)


def rounded_price(outcome, M, span=64, fraction_bits=40):
    if type(fraction_bits) is not int or fraction_bits < 1:
        raise ValueError("positive readout precision required")
    lo, hi = price_interval(outcome, M, span)
    scale = 1 << fraction_bits
    if hi - lo > Fraction(1, scale):
        raise ArithmeticError("readout enclosure exceeds the declared rounding error")
    midpoint = (lo + hi) / 2
    # Deterministic downward rounding; one exact raw dollar quantum bounds
    # midpoint rounding plus enclosure error under the above interval check.
    raw = midpoint.numerator * scale // midpoint.denominator
    value = Fraction(raw, scale)
    error = max(abs(value - lo), abs(value - hi))
    if error > Fraction(2, scale):
        raise ArithmeticError("readout rounding cannot meet its explicit dollar bound")
    return dict(
        raw_price=raw,
        fraction_bits=fraction_bits,
        exact_price=[value.numerator, value.denominator],
        deterministic_error_upper=[2, scale],
        certified_uniform_error_allowance=[2, scale],
        already_discounted=True,
    )
