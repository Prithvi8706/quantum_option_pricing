"""Certified classical canonical-AE label conversion for the residual decoder.

This opt-in adapter closes the exact-label to binary64-input interface only.
It does not certify native quantum gates, noise, or archived acquisitions.
"""

from decimal import Decimal

from research.journal_sprint.decimal_enclosure import Interval
from research.journal_sprint.week2_decoding import amplitude_interval


def label_amplitude(label, size):
    """Return a binary64 probability and an outward bound from the exact AE label."""
    enclosure = amplitude_interval(label, size)
    # Conversion accuracy need not be assumed: enclose its actual binary value.
    value = min(1.0, max(0.0, float(enclosure.lo)))
    error = (Interval(value) - enclosure).absolute().hi
    return {
        "value": value,
        "exact_label_enclosure": enclosure.record(),
        "conversion_error_upper": str(error),
    }


def median_amplitude(labels, size):
    """Enclose the median exact probability; bound the returned float median.

Coordinatewise order statistics are monotone, so sorted lower and upper
endpoints enclose the exact median even when intervals overlap. An odd sample
requires no additional floating-point averaging operation.
"""
    labels = list(labels)
    if not labels or len(labels) % 2 == 0:
        raise ValueError("nonempty odd number of canonical labels required")
    rows = [label_amplitude(label, size) for label in labels]
    middle = len(rows) // 2
    lower = sorted(Decimal(row["exact_label_enclosure"]["lower"]) for row in rows)[middle]
    upper = sorted(Decimal(row["exact_label_enclosure"]["upper"]) for row in rows)[middle]
    enclosure = Interval(lower, upper)
    value = sorted(row["value"] for row in rows)[middle]
    return {
        "value": value,
        "exact_median_enclosure": enclosure.record(),
        "conversion_error_upper": str((Interval(value) - enclosure).absolute().hi),
    }


def price_allowance(sensitivity_upper, conversion_error_upper):
    """Additional allowance, to be added to the existing deterministic budget."""
    scale, error = Interval(sensitivity_upper), Interval(conversion_error_upper)
    if scale.lo <= 0 or error.lo < 0:
        raise ValueError("positive sensitivity and nonnegative conversion bound required")
    return str((scale * error).hi)
