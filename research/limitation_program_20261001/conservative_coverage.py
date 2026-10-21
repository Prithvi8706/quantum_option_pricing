"""Exact interval geometry and outward binomial confidence brackets.

These are conditional statistical tools. A shared estimated reference and
pseudorandom replication design do not automatically prove true-price coverage.
No source intervals or probabilities are evaluated on import.
"""

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from math import isfinite

MAX_REPLICATIONS = 1000
ROOT_BITS = 64
CLASSIFICATIONS = 3
METHOD_CELLS = 18
COUNT_INTERVALS = CLASSIFICATIONS * METHOD_CELLS
COUNT_FAILURE = Fraction(1, 20)
PER_INTERVAL_FAILURE = COUNT_FAILURE / COUNT_INTERVALS


def rational(value):
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise ValueError("Exact integer or Fraction required")
    return Fraction(value)


def binary64(value):
    if isinstance(value, bool) or not isinstance(value, float) or not isfinite(value):
        raise ValueError("Finite binary64 float required")
    return Fraction.from_float(value)


@dataclass(frozen=True)
class Membership:
    guaranteed: bool
    reference_point: bool
    possible: bool


def classify(center, half_width, reference, reference_radius):
    center, half_width, reference, reference_radius = map(
        rational, (center, half_width, reference, reference_radius)
    )
    if half_width < 0 or reference_radius < 0:
        raise ValueError("Nonnegative interval half-widths required")
    distance = abs(center - reference)
    result = Membership(
        distance + reference_radius <= half_width,
        distance <= half_width,
        distance <= half_width + reference_radius,
    )
    assert result.guaranteed <= result.reference_point <= result.possible
    return result


def _lower_sum(n, k, numerator, denominator):
    """One exact common-denominator binomial sum, with no floating tail."""
    if k < 0:
        return 0, 1
    if k >= n:
        return 1, 1
    if numerator == 0:
        return 1, 1
    if numerator == denominator:
        return 0, 1
    complement = denominator - numerator
    total_denominator = denominator**n
    term = complement**n
    total = term
    for i in range(k):
        top = term * (n - i) * numerator
        divisor = (i + 1) * complement
        term, remainder = divmod(top, divisor)
        assert remainder == 0
        total += term
    return total, total_denominator


def _cdf(n, k, probability):
    if k < 0:
        return 0, 1
    if k >= n:
        return 1, 1
    a, b = probability.numerator, probability.denominator
    if k < n // 2:
        return _lower_sum(n, k, a, b)
    # Sum the shorter failure tail, which is especially important near99%.
    numerator, denominator = _lower_sum(n, n - k - 1, b - a, b)
    return denominator - numerator, denominator


def binomial_cdf(n, k, probability):
    probability = rational(probability)
    if type(n) is not int or not 1 <= n <= MAX_REPLICATIONS or type(k) is not int:
        raise ValueError("Bounded positive integer replication count and integer cutoff required")
    if not 0 <= probability <= 1:
        raise ValueError("Probability must be in[0,1]")
    return Fraction(*_cdf(n, k, probability))


def clopper_pearson_outward(successes, n, failure=PER_INTERVAL_FAILURE, bits=ROOT_BITS):
    """Conservative dyadic endpoints enclosing the exact two-sided CP interval.

    Lower solves P_p(X>=successes)=failure/2; upper solves
    P_p(X<=successes)=failure/2. Integer comparisons decide every bisection.
    The returned lower rounds down and upper rounds up. Bonferroni needs no
    independence between different cells, but each count needs its own valid
    IID Bernoulli replication model conditional on the shared reference.
    """
    failure = rational(failure)
    if type(n) is not int or not 1 <= n <= MAX_REPLICATIONS:
        raise ValueError("Bounded positive integer replication count required")
    if type(successes) is not int or not 0 <= successes <= n:
        raise ValueError("Integer success count must be inside the replication count")
    if not 0 < failure < 1 or type(bits) is not int or not 1 <= bits <= ROOT_BITS:
        raise ValueError("Strict failure probability and bounded integer root bits required")
    return _clopper_pearson_outward(successes, n, failure, bits)


@lru_cache(maxsize=256)
def _clopper_pearson_outward(successes, n, failure, bits):
    """Cache only arguments that have already passed exact public guards."""
    target = failure / 2
    lower, upper = Fraction(0), Fraction(1)
    if successes:
        lo, hi = Fraction(0), Fraction(1)
        for _ in range(bits):
            midpoint = (lo + hi) / 2
            numerator, denominator = _cdf(n, n - successes, 1 - midpoint)
            if numerator * target.denominator >= target.numerator * denominator:
                hi = midpoint
            else:
                lo = midpoint
        lower = lo
    if successes < n:
        lo, hi = Fraction(0), Fraction(1)
        for _ in range(bits):
            midpoint = (lo + hi) / 2
            numerator, denominator = _cdf(n, successes, midpoint)
            if numerator * target.denominator >= target.numerator * denominator:
                lo = midpoint
            else:
                hi = midpoint
        upper = hi
    assert 0 <= lower <= upper <= 1
    return lower, upper


def conditional_joint_confidence(count_failure, reference_failures):
    """Union bound ONLY if the reference and conditional-count premises hold."""
    count_failure = rational(count_failure)
    reference_failures = tuple(map(rational, reference_failures))
    if not 0 <= count_failure <= 1 or any(not 0 <= value <= 1 for value in reference_failures):
        raise ValueError("Failure probabilities must be inside[0,1]")
    return max(Fraction(0), 1 - count_failure - sum(reference_failures, Fraction(0)))
