"""Exact canonical bounded-AE schedule for the original discounted digital Y.

Machin's identity and alternating rational series enclose pi. Every schedule
decision and median confidence calculation uses fractions, with no fitted
moments, observed outcomes or floating point thresholds.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb


def atan_interval(inverse, terms):
    if type(inverse) is not int or inverse <= 1 or type(terms) is not int or terms < 1:
        raise ValueError("positive alternating-series domain required")
    total = sum(
        (Fraction((-1) ** k, (2 * k + 1) * inverse ** (2 * k + 1)) for k in range(terms)),
        Fraction(0),
    )
    following = total + Fraction((-1) ** terms, (2 * terms + 1) * inverse ** (2 * terms + 1))
    return min(total, following), max(total, following)


def pi_interval(terms=80):
    a, b = atan_interval(5, terms), atan_interval(239, terms)
    return 16 * a[0] - 4 * b[1], 16 * a[1] - 4 * b[0]


def rational_pair(value):
    value = Fraction(value)
    return [value.numerator, value.denominator]


def binomial_majority_tail(repetitions, probability):
    if type(repetitions) is not int or repetitions < 1 or repetitions % 2 == 0:
        raise ValueError("odd positive median repetition count required")
    probability = Fraction(probability)
    if not 0 <= probability < Fraction(1, 2):
        raise ValueError("elementary failure must be below one half")
    return sum(
        (
            comb(repetitions, k) * probability**k * (1 - probability) ** (repetitions - k)
            for k in range(repetitions // 2 + 1, repetitions + 1)
        ),
        Fraction(0),
    )


def certified_schedule(error=Fraction(9, 2000), failure=Fraction(3, 1000), span=64):
    if isinstance(error, float) or isinstance(failure, float):
        raise ValueError("exact rational error and failure required")
    error, failure = Fraction(error), Fraction(failure)
    if error <= 0 or not 0 < failure < 1 or type(span) is not int or span < 1:
        raise ValueError("positive dollar error, span and probability required")
    lo, hi = pi_interval()
    M = 1
    while span * (hi / M + hi**2 / M**2) > error:
        M *= 2
    if M > 1 and span * (lo / (M // 2) + lo**2 / (M // 2) ** 2) <= error:
        raise ArithmeticError("pi enclosure cannot distinguish adjacent QPE schedules")
    elementary = 1 - 8 / hi**2
    denominator = 1 << 40
    numerator = (
        elementary.numerator * denominator + elementary.denominator - 1
    ) // elementary.denominator
    bad = Fraction(numerator, denominator)
    assert bad >= elementary and bad < Fraction(1, 2)
    repetitions = 1
    while binomial_majority_tail(repetitions, bad) > failure:
        repetitions += 2
    return dict(
        format="exact-rational-canonical-bounded-AE-schedule-v1",
        statistical_error_dollars_exact=rational_pair(error),
        requested_failure_exact=rational_pair(failure),
        normalization_span_dollars=span,
        amplitude_tolerance_exact=rational_pair(error / span),
        pi_enclosure_exact=[rational_pair(lo), rational_pair(hi)],
        elementary_failure_upper_exact=rational_pair(bad),
        ideal_failure_upper_exact=rational_pair(binomial_majority_tail(repetitions, bad)),
        ideal_error_upper_exact=rational_pair(span * (hi / M + hi**2 / M**2)),
        M=M,
        qpe_bits=M.bit_length() - 1,
        repetitions=repetitions,
        controlled_grover_calls=repetitions * (M - 1),
        longest_single_shot_grover_chain=M - 1,
        fresh_preparations=repetitions,
        adaptive_quantum_rounds=0,
        median_classical_comparisons_upper=repetitions * (repetitions - 1) // 2,
        finite_error_formula="span*(pi/M + pi**2/M**2), success >= 8/pi**2",
        certificate_method=(
            "Machin rational enclosure; rounded-up elementary probability; "
            "exact binomial majority tail"
        ),
        output_already_discounted=True,
        further_discount_factor=[1, 1],
        synthesis_and_physical_failure_included=False,
    )
