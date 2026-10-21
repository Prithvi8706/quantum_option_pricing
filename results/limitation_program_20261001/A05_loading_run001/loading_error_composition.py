"""Independent preparation errors and a bounded-payoff loading allowance."""

from fractions import Fraction
from math import isqrt


def probability(value):
    if type(value) is int or isinstance(value, Fraction):
        value = Fraction(value)
    else:
        raise ValueError("Exact rational error required")
    if not 0 <= value <= 1:
        raise ValueError("Trace distance lies in [0,1]")
    return value


def product_trace_squared(errors, *, independent_pure_product):
    if independent_pure_product is not True:
        raise ValueError("Pure product-state structure must be proved")
    errors = tuple(map(probability, errors))
    if not errors:
        raise ValueError("At least one factor required")
    fidelity = Fraction(1)
    for error in errors:
        fidelity *= 1 - error**2
    return 1 - fidelity


def general_trace_upper(errors):
    errors = tuple(map(probability, errors))
    if not errors:
        raise ValueError("At least one factor required")
    return min(Fraction(1), sum(errors, Fraction(0)))


def sqrt_lower(value, bits=128):
    if not isinstance(value, Fraction) or value < 0:
        raise ValueError("Nonnegative exact square required")
    if type(bits) is not int or not 1 <= bits <= 256:
        raise ValueError("Bounded integer precision required")
    scale = 1 << bits
    root = isqrt((value.numerator * scale * scale) // value.denominator)
    result = Fraction(root, scale)
    assert result**2 <= value < (result + Fraction(1, scale)) ** 2
    return result


def allowances(draws, loading_dollars=Fraction(1, 1000), payoff_span=Fraction(40)):
    if type(draws) is not int or draws < 1:
        raise ValueError("Positive integer draw count required")
    if not isinstance(loading_dollars, Fraction) or not 0 < loading_dollars < payoff_span:
        raise ValueError("Exact loading allowance smaller than payoff span required")
    if not isinstance(payoff_span, Fraction) or payoff_span <= 0:
        raise ValueError("Positive exact payoff span required")
    total = loading_dollars / payoff_span
    conservative = total / draws
    pure = sqrt_lower(total**2 / draws)
    assert general_trace_upper([conservative] * draws) * payoff_span <= loading_dollars
    exact_product_squared = product_trace_squared([pure] * draws, independent_pure_product=True)
    assert exact_product_squared <= draws * pure**2 <= total**2
    return dict(
        loading_dollars=loading_dollars,
        payoff_span=payoff_span,
        draws=draws,
        total_trace_allowance=total,
        conservative_scalar_trace_allowance=conservative,
        pure_product_scalar_trace_allowance_lower=pure,
        pure_product_scalar_allowance_square_upper=total**2 / draws,
        exact_pure_product_trace_squared_upper=exact_product_squared,
        pure_product_structure_required=True,
    )
