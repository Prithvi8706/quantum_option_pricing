"""Small outward decimal intervals; no binary-float transcendental evaluation.

Arithmetic uses directed rounding. Correctly-rounded decimal exp/ln/sqrt are
enlarged by one representable neighbor on each endpoint. Normal CDF uses an
alternating integral series with a bounded remainder, not scipy's CDF.
"""

from dataclasses import dataclass
from decimal import Context, Decimal, ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_EVEN
from functools import lru_cache


PRECISION = 80
DOWN = Context(prec=PRECISION, rounding=ROUND_FLOOR)
UP = Context(prec=PRECISION, rounding=ROUND_CEILING)
NEAR = Context(prec=PRECISION, rounding=ROUND_HALF_EVEN)


def exact(value):
    if isinstance(value, bool):
        raise ValueError("boolean is not an interval endpoint")
    result = Decimal.from_float(value) if isinstance(value, float) else Decimal(value)
    if not result.is_finite():
        raise ValueError("finite endpoint required")
    return result


@dataclass(frozen=True)
class Interval:
    lo: Decimal
    hi: Decimal

    def __init__(self, lo, hi=None):
        lo, hi = exact(lo), exact(lo if hi is None else hi)
        if lo > hi:
            raise ValueError("reversed interval")
        object.__setattr__(self, "lo", lo)
        object.__setattr__(self, "hi", hi)

    @staticmethod
    def coerce(value):
        return value if isinstance(value, Interval) else Interval(value)

    def __add__(self, other):
        other = self.coerce(other)
        return Interval(DOWN.add(self.lo, other.lo), UP.add(self.hi, other.hi))

    __radd__ = __add__

    def __neg__(self):
        # Decimal unary minus can round in the ambient context; copy_negate cannot.
        return Interval(self.hi.copy_negate(), self.lo.copy_negate())

    def __sub__(self, other):
        return self + -self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other) + -self

    def __mul__(self, other):
        other = self.coerce(other)
        pairs = [(a, b) for a in (self.lo, self.hi) for b in (other.lo, other.hi)]
        return Interval(
            min(DOWN.multiply(a, b) for a, b in pairs), max(UP.multiply(a, b) for a, b in pairs)
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.coerce(other)
        if other.lo <= 0 <= other.hi:
            raise ValueError("division interval contains zero")
        inverse = Interval(DOWN.divide(Decimal(1), other.hi), UP.divide(Decimal(1), other.lo))
        return self * inverse

    def __rtruediv__(self, other):
        return self.coerce(other) / self

    def __pow__(self, n):
        if isinstance(n, bool) or not isinstance(n, int) or n < 0:
            raise ValueError("nonnegative integer power required")
        result, base = Interval(1), self
        while n:
            if n % 2:
                result = result * base
            base, n = base * base, n // 2
        return result

    def absolute(self):
        if self.lo >= 0:
            return self
        if self.hi <= 0:
            return -self
        return Interval(0, max(self.lo.copy_abs(), self.hi.copy_abs()))

    def _monotone(self, name):
        operation = getattr(NEAR, name)
        return Interval(NEAR.next_minus(operation(self.lo)), NEAR.next_plus(operation(self.hi)))

    def exp(self):
        if self.lo < -1000 or self.hi > 1000:
            raise ValueError("exponential outside supported domain")
        return self._monotone("exp")

    def ln(self):
        if self.lo <= 0:
            raise ValueError("positive logarithm interval required")
        return self._monotone("ln")

    def sqrt(self):
        if self.lo < 0:
            raise ValueError("negative square-root interval")
        result = self._monotone("sqrt")
        return Interval(max(Decimal(0), result.lo), result.hi)

    def record(self):
        return dict(lower=str(self.lo), upper=str(self.hi))


def product(values):
    result = Interval(1)
    for value in values:
        result *= value
    return result


@lru_cache(maxsize=1)
def pi_interval():
    def arctan_inverse(n):
        x = Interval(1) / n
        term, total = x, Interval(0)
        for k in range(120):
            total += term / (2 * k + 1) if k % 2 == 0 else -term / (2 * k + 1)
            term *= x * x
        remainder = (term / 241).hi
        return total + Interval(remainder.copy_negate(), remainder)

    return 16 * arctan_inverse(5) - 4 * arctan_inverse(239)


@lru_cache(maxsize=4096)
def _cdf_point(x):
    if x.copy_abs() > 10:
        raise ValueError("normal CDF enclosure supports [-10,10]")
    if x < 0:
        return 1 - _cdf_point(x.copy_negate())
    if x == 0:
        return Interval("0.5")
    value = Interval(x)
    term, total = value, Interval(0)
    for n in range(1000):
        total += term if n % 2 == 0 else -term
        next_term = term * value * value * (2 * n + 1) / (2 * (n + 1) * (2 * n + 3))
        if n >= 50 and next_term.hi < Decimal("1e-65"):
            # x<=10 and n>=50 imply all subsequent terms decrease in magnitude.
            remainder = next_term.hi
            integral = total + Interval(remainder.copy_negate(), remainder)
            result = Interval("0.5") + integral / (2 * pi_interval()).sqrt()
            return Interval(max(Decimal(0), result.lo), min(Decimal(1), result.hi))
        term = next_term
    raise ArithmeticError("normal integral series did not converge")


def normal_cdf(value):
    value = Interval.coerce(value)
    return Interval(_cdf_point(value.lo).lo, _cdf_point(value.hi).hi)
