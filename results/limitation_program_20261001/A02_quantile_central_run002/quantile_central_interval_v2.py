"""One fixed dyadic interval and order-four normalized Taylor-jet method."""

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from math import factorial

from research.limitation_program_20261001.barrier_band_certificate import sqrt_interval
from research.limitation_program_20261001.financial_bounded_schedule import pi_interval


PRECISION = 128
CDF_TERMS = 32
EXP_TERMS = 40
DOMAIN = Fraction(3, 2)


def exact(value):
    if type(value) is int or isinstance(value, Fraction):
        return Fraction(value)
    raise ValueError("Exact rational interval input required")


@dataclass(frozen=True)
class Interval:
    lo: Fraction
    hi: Fraction

    def __post_init__(self):
        object.__setattr__(self, "lo", exact(self.lo))
        object.__setattr__(self, "hi", exact(self.hi))
        if self.lo > self.hi:
            raise ValueError("Ordered rational interval required")

    def __add__(self, other):
        other = point(other)
        return outward(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-point(other))

    def __rsub__(self, other):
        return point(other) - self

    def __mul__(self, other):
        other = point(other)
        products = [left * right for left in (self.lo, self.hi) for right in (other.lo, other.hi)]
        return outward(min(products), max(products))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = point(other)
        if other.lo <= 0 <= other.hi:
            raise ValueError("Interval denominator contains zero")
        return self * outward(1 / other.hi, 1 / other.lo)

    def bound(self):
        return max(abs(self.lo), abs(self.hi))


def point(value):
    return value if isinstance(value, Interval) else Interval(exact(value), exact(value))


def outward(lower, upper):
    scale = 1 << PRECISION
    lo = lower.numerator * scale // lower.denominator
    hi = -((-upper.numerator * scale) // upper.denominator)
    return Interval(Fraction(lo, scale), Fraction(hi, scale))


def square(value):
    value = point(value)
    lower = 0 if value.lo <= 0 <= value.hi else min(value.lo**2, value.hi**2)
    return outward(Fraction(lower), max(value.lo**2, value.hi**2))


def constant_jet(value):
    return [point(value), point(0), point(0), point(0), point(0)]


def variable_jet(value):
    return [point(value), point(1), point(0), point(0), point(0)]


def jet_add(left, right):
    return [a + b for a, b in zip(left, right, strict=True)]


def jet_neg(value):
    return [-coefficient for coefficient in value]


def jet_mul(left, right):
    return [sum((left[j] * right[k - j] for j in range(k + 1)), point(0)) for k in range(5)]


def jet_inverse(value):
    result = [point(1) / value[0]]
    for degree in range(1, 5):
        result.append(
            -sum((value[k] * result[degree - k] for k in range(1, degree + 1)), point(0)) / value[0]
        )
    return result


def jet_polynomial(coefficients, argument):
    result = constant_jet(coefficients[-1])
    for coefficient in reversed(coefficients[:-1]):
        result = jet_add(jet_mul(result, argument), constant_jet(coefficient))
    return result


@lru_cache(None)
def gaussian_prefactors():
    pi_lo, pi_hi = pi_interval()
    density = Interval(
        sqrt_interval(1 / (2 * pi_hi), PRECISION)[0],
        sqrt_interval(1 / (2 * pi_lo), PRECISION)[1],
    )
    integrated = Interval(
        sqrt_interval(2 / pi_hi, PRECISION)[0],
        sqrt_interval(2 / pi_lo, PRECISION)[1],
    )
    return density, integrated


def _polynomial(coefficients, argument):
    result = point(coefficients[-1])
    for coefficient in reversed(coefficients[:-1]):
        result = result * argument + coefficient
    return result


def normal_density(value):
    value = point(value)
    if value.bound() > DOMAIN:
        raise ValueError("Fixed central Gaussian domain exceeded")
    argument = square(value) / 2
    coefficients = [Fraction((-1) ** k, factorial(k)) for k in range(EXP_TERMS + 1)]
    remainder = (DOMAIN**2 / 2) ** (EXP_TERMS + 1) / factorial(EXP_TERMS + 1)
    exponential = _polynomial(coefficients, argument) + Interval(-remainder, remainder)
    return exponential * gaussian_prefactors()[0]


def normal_cdf(value):
    value = point(value)
    if value.bound() > DOMAIN:
        raise ValueError("Fixed central Gaussian domain exceeded")
    argument = square(value) / 2
    coefficients = [Fraction((-1) ** k, factorial(k) * (2 * k + 1)) for k in range(CDF_TERMS + 1)]
    remainder = DOMAIN ** (2 * CDF_TERMS + 3) / (
        2 ** (CDF_TERMS + 1) * factorial(CDF_TERMS + 1) * (2 * CDF_TERMS + 3)
    )
    integral = value * _polynomial(coefficients, argument) + Interval(-remainder, remainder)
    return (1 + integral * gaussian_prefactors()[1]) / 2
