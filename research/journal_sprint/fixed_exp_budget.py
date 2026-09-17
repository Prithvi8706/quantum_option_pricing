"""Directed Taylor/Horner certificate for a development fixed-point exponential.

Domain, input quantization and overflow are explicit. This is not a price
contract: Gaussian loading and integration with a payoff circuit are separate.
"""

from math import factorial
from .decimal_enclosure import Interval


def exp_budget(radius, input_error, degree, fraction_bits, width, spot=100):
    for value in (degree, fraction_bits, width):
        if type(value) is not int or value < 1:
            raise ValueError("positive integer precision parameters required")
    h, dx, s = Interval(radius), Interval(input_error), Interval(spot)
    if h.lo < 0 or dx.lo < 0 or s.lo <= 0 or fraction_bits >= width:
        raise ValueError("invalid domain/scale")
    unit = Interval(1) / (1 << fraction_bits)
    domain = h + dx
    # Use exact integer spot only, keeping coefficient construction rational.
    if s.lo != s.hi or s.lo != int(s.lo):
        raise ValueError("integer spot required by this development kernel")
    coefficients = tuple(int(s.lo) * (1 << fraction_bits) // factorial(k)
                         for k in range(degree+1))
    error = s / factorial(degree) - Interval(coefficients[-1]) * unit
    magnitude = Interval(coefficients[-1]) * unit
    maximum = magnitude.hi
    for k in reversed(range(degree)):
        rounding = unit if magnitude.hi else Interval(0)
        coefficient_error = s / factorial(k) - Interval(coefficients[k]) * unit
        error = domain * error + rounding + coefficient_error
        magnitude = domain * magnitude + rounding + Interval(coefficients[k]) * unit
        maximum = max(maximum, magnitude.hi)
    remainder = s * domain.exp() * domain**(degree+1) / factorial(degree+1)
    input_term = s * domain.exp() * dx
    total = error + remainder + input_term
    limit = Interval((1 << (width-1))-1) * unit
    return dict(coefficients=coefficients, domain_upper=str(domain.hi),
                horner_error_upper=str(error.hi), remainder_upper=str(remainder.hi),
                input_error_upper=str(input_term.hi), total_error_upper=str(total.hi),
                intermediate_magnitude_upper=str(maximum),
                overflow_safe=maximum <= limit.lo and domain.hi <= limit.lo,
                scope="scalar exponential only; not application admission")


def evaluate_integer(x, coefficients, fraction_bits):
    """Unbounded integer reference, no modular wrapping."""
    y = coefficients[-1]
    for c in reversed(coefficients[:-1]):
        y = (x*y // (1 << fraction_bits)) + c
    return y
