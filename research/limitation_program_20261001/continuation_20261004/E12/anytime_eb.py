"""Dyadic iid empirical-Bernstein CS; exact rational inputs, outward endpoints."""
from dataclasses import dataclass
from decimal import Context, Decimal, ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_EVEN
from fractions import Fraction

PRECISION = 80


def rational(value):
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError("Exact int/Fraction input required; floats are not certificates")
    return Fraction(value)


def context(rounding=ROUND_HALF_EVEN, precision=PRECISION):
    return Context(prec=precision, rounding=rounding)


def fraction_interval(value, precision=PRECISION):
    value = rational(value)
    a, b = Decimal(value.numerator), Decimal(value.denominator)
    return (context(ROUND_FLOOR, precision).divide(a, b),
            context(ROUND_CEILING, precision).divide(a, b))


def log_interval(value, precision=PRECISION):
    lo, hi = fraction_interval(value, precision)
    if lo <= 0:
        raise ValueError("Log argument must be positive")
    ctx = context(precision=precision)
    return ctx.next_minus(ctx.ln(lo)), ctx.next_plus(ctx.ln(hi))


def exp_interval(value, precision=PRECISION):
    lo, hi = fraction_interval(value, precision)
    ctx = context(precision=precision)
    return ctx.next_minus(ctx.exp(lo)), ctx.next_plus(ctx.exp(hi))


def look_failure(alpha, exponent):
    alpha = rational(alpha)
    if not 0 < alpha < 1 or isinstance(exponent, bool) or not isinstance(exponent, int) or exponent < 1:
        raise ValueError("Require 0<alpha<1 and positive integer exponent")
    return alpha / (exponent * (exponent + 1))


def empirical_bernstein_radius(variance, n, width, failure, precision=PRECISION):
    variance, width, failure = map(rational, (variance, width, failure))
    if isinstance(n, bool) or not isinstance(n, int) or n < 2:
        raise ValueError("n must be an integer >=2")
    if variance < 0 or width <= 0 or not 0 < failure < 1:
        raise ValueError("Invalid variance, width or failure")
    floor_ctx = context(ROUND_FLOOR, precision)
    ceil_ctx = context(ROUND_CEILING, precision)
    nearest = context(precision=precision)
    log_lo, log_hi = log_interval(4 / failure, precision)
    coefficient_lo, coefficient_hi = fraction_interval(2 * variance / n, precision)
    radicand_lo = floor_ctx.multiply(coefficient_lo, log_lo)
    radicand_hi = ceil_ctx.multiply(coefficient_hi, log_hi)
    sqrt_lo = max(Decimal(0), nearest.next_minus(nearest.sqrt(radicand_lo))) if radicand_lo else Decimal(0)
    sqrt_hi = nearest.next_plus(nearest.sqrt(radicand_hi)) if radicand_hi else Decimal(0)
    tail_coefficient_lo, tail_coefficient_hi = fraction_interval(7 * width / (3 * (n - 1)), precision)
    tail_lo = floor_ctx.multiply(tail_coefficient_lo, log_lo)
    tail_hi = ceil_ctx.multiply(tail_coefficient_hi, log_hi)
    return (floor_ctx.add(sqrt_lo, tail_lo), ceil_ctx.add(sqrt_hi, tail_hi))


@dataclass(frozen=True)
class Statistics:
    n: int
    total: Fraction
    squares: Fraction
    lower: Fraction = Fraction(0)
    upper: Fraction = Fraction(1)

    def __post_init__(self):
        for name in ("total", "squares", "lower", "upper"):
            object.__setattr__(self, name, rational(getattr(self, name)))
        if isinstance(self.n, bool) or not isinstance(self.n, int) or self.n < 2 or self.lower >= self.upper:
            raise ValueError("Invalid n or support")
        if not self.n * self.lower <= self.total <= self.n * self.upper:
            raise ValueError("Mean outside proved support")
        if self.squares < self.total * self.total / self.n:
            raise ValueError("Negative variance")
        # (x-a)(x-b)<=0 gives an independent aggregate support constraint.
        if self.squares > (self.lower + self.upper) * self.total - self.n * self.lower * self.upper:
            raise ValueError("Squared sum incompatible with proved support")

    @property
    def mean(self):
        return self.total / self.n

    @property
    def variance(self):
        return (self.squares - self.total * self.total / self.n) / (self.n - 1)

    @classmethod
    def bernoulli(cls, n, successes):
        if isinstance(successes, bool) or not isinstance(successes, int) or not 0 <= successes <= n:
            raise ValueError("Invalid Bernoulli success count")
        return cls(n, Fraction(successes), Fraction(successes))

    @classmethod
    def observations(cls, values, lower=Fraction(0), upper=Fraction(1)):
        values = [rational(x) for x in values]
        lower, upper = rational(lower), rational(upper)
        if any(x < lower or x > upper for x in values):
            raise ValueError("Observation outside proved support")
        return cls(len(values), sum(values, Fraction(0)), sum((x*x for x in values), Fraction(0)), lower, upper)


def interval(stats, failure, precision=PRECISION):
    radius = empirical_bernstein_radius(stats.variance, stats.n, stats.upper - stats.lower, failure, precision)
    mean_lo, mean_hi = fraction_interval(stats.mean, precision)
    support_lo = fraction_interval(stats.lower, precision)[0]
    support_hi = fraction_interval(stats.upper, precision)[1]
    lo = max(support_lo, context(ROUND_FLOOR, precision).subtract(mean_lo, radius[1]))
    hi = min(support_hi, context(ROUND_CEILING, precision).add(mean_hi, radius[1]))
    return lo, hi, radius


class DyadicCS:
    def __init__(self, alpha=Fraction(1, 2000), cap_exponent=16):
        look_failure(alpha, cap_exponent)
        self.alpha = rational(alpha)
        self.cap_exponent = cap_exponent
        self.exponent = 0
        self.lower = Decimal(0)
        self.upper = Decimal(1)
        self.empty = False
        self.looks = []
        self.previous_stats = None

    def update(self, stats):
        exponent = self.exponent + 1
        if exponent > self.cap_exponent or stats.n != 2 ** exponent:
            raise ValueError("Only the next frozen dyadic look is permitted")
        if (stats.lower, stats.upper) != (Fraction(0), Fraction(1)):
            raise ValueError("CS requires normalized [0,1] group statistics")
        if self.previous_stats is not None:
            previous = self.previous_stats
            Statistics(stats.n - previous.n, stats.total - previous.total,
                       stats.squares - previous.squares)
        delta = look_failure(self.alpha, exponent)
        lo, hi, radius = interval(stats, delta)
        self.lower = max(self.lower, lo)
        self.upper = min(self.upper, hi)
        self.empty = self.empty or self.lower > self.upper
        self.exponent = exponent
        self.previous_stats = stats
        record = dict(exponent=exponent, n=stats.n, failure=str(delta),
                      mean=str(stats.mean), sample_variance=str(stats.variance),
                      radius_lower=str(radius[0]), radius_upper=str(radius[1]),
                      retained_lower=str(self.lower), retained_upper=str(self.upper),
                      empty=self.empty)
        self.looks.append(record)
        return record

    def reaches(self, target):
        target = rational(target)
        target_lo = fraction_interval(target)[0]
        return not self.empty and self.exponent > 0 and self.upper <= target_lo

    def result(self, target):
        ready = self.reaches(target)
        return dict(status="TARGET_CERTIFIED" if ready else "SUPPORT_FALLBACK",
                    certificate_upper=str(self.upper) if ready else "1",
                    observations=2 ** self.exponent if self.exponent else 0,
                    empty=self.empty, allocated_failure=str(self.alpha))
