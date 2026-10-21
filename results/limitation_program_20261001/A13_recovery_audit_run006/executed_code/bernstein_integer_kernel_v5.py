"""Author-only exact rational Bernstein transform with integer intermediates.

No evaluation occurs on import. A separately reviewed controller must supply a
mandatory budget checkpoint. This changes verifier arithmetic, not quantum
circuits, witnesses, polynomial coefficients, or rounding rules.
"""

from fractions import Fraction
from math import comb, lcm


def integer_bernstein(coefficients, left, right, degree, checkpoint):
    """Return the identical degree-elevated Bernstein vector on [left, right]."""
    checkpoint()
    if left > right or len(coefficients) > degree + 1:
        raise ValueError("Whole closed Bernstein domain")
    # The original permissive guard also admits degree=-1 with an empty vector.
    if degree < 0:
        return []
    coefficients = tuple(Fraction(value) for value in coefficients)
    left, right = Fraction(left), Fraction(right)
    maximum_power = max(0, len(coefficients) - 1)
    coefficient_denominator = 1
    for value in coefficients:
        checkpoint()
        coefficient_denominator = lcm(coefficient_denominator, value.denominator)
    scaled_coefficients = tuple(
        value.numerator * (coefficient_denominator // value.denominator) for value in coefficients
    )
    width = right - left
    domain_denominator = lcm(left.denominator, width.denominator)
    left_integer = left.numerator * (domain_denominator // left.denominator)
    width_integer = width.numerator * (domain_denominator // width.denominator)
    left_powers, width_powers, denominator_powers = [1], [1], [1]
    for _ in range(maximum_power):
        checkpoint()
        left_powers.append(left_powers[-1] * left_integer)
        width_powers.append(width_powers[-1] * width_integer)
        denominator_powers.append(denominator_powers[-1] * domain_denominator)
    transformed = []
    for order in range(degree + 1):
        checkpoint()
        if order >= len(coefficients):
            transformed.append(0)
            continue
        subtotal = 0
        for power in range(order, len(coefficients)):
            checkpoint()
            subtotal += (
                scaled_coefficients[power]
                * comb(power, order)
                * left_powers[power - order]
                * denominator_powers[maximum_power - power]
            )
        transformed.append(subtotal * width_powers[order])
    active_orders = min(degree, maximum_power)
    binomials = [comb(degree, order) for order in range(active_orders + 1)]
    binomial_denominator = 1
    for value in binomials:
        checkpoint()
        binomial_denominator = lcm(binomial_denominator, value)
    weights = [binomial_denominator // value for value in binomials]
    denominator = coefficient_denominator * denominator_powers[maximum_power] * binomial_denominator
    rows = []
    for index in range(degree + 1):
        checkpoint()
        numerator = 0
        for order in range(min(index, active_orders) + 1):
            checkpoint()
            numerator += transformed[order] * comb(index, order) * weights[order]
        rows.append(Fraction(numerator, denominator))
    return rows
