"""Checks of the exact-label interface, including ordering and decimal context."""

from decimal import Decimal, localcontext
from fractions import Fraction

import pytest

from research.assessment_20260921.label_bridge import (
    label_amplitude,
    median_amplitude,
    price_allowance,
)


@pytest.mark.parametrize("label,exact", [(0, 0), (2, Fraction(1, 2)), (4, 1), (6, Fraction(1, 2))])
def test_exact_special_labels(label, exact):
    row = label_amplitude(label, 8)
    bounds = row["exact_label_enclosure"]
    assert Fraction(bounds["lower"]) <= exact <= Fraction(bounds["upper"])
    assert abs(Fraction(row["value"]) - exact) <= Fraction(row["conversion_error_upper"])


def test_folded_labels_and_nontrivial_order_statistic():
    # Integer label order differs from probability order after M/2.
    row = median_amplitude([7, 4, 0, 2, 6], 8)
    assert abs(Fraction(row["value"]) - Fraction(1, 2)) <= Fraction(
        row["conversion_error_upper"]
    )
    assert label_amplitude(1, 8) == label_amplitude(7, 8)


def test_ambient_decimal_precision_does_not_weaken_bound():
    reference = median_amplitude([3, 31, 8], 32)
    with localcontext() as context:
        context.prec = 6
        assert median_amplitude([3, 31, 8], 32) == reference
        charged = price_allowance("62.108514147104523", reference["conversion_error_upper"])
    assert Fraction(charged) >= Fraction("62.108514147104523") * Fraction(
        reference["conversion_error_upper"]
    )
    assert Decimal(charged) < Decimal("1e-13")


@pytest.mark.parametrize("labels,size", [([], 8), ([1, 2], 8), ([True], 8), ([8], 8), ([1], 3)])
def test_invalid_canonical_inputs(labels, size):
    with pytest.raises(ValueError):
        median_amplitude(labels, size)


@pytest.mark.parametrize("scale,error", [(0, 0), (-1, 1), (1, -1), (float("inf"), 0)])
def test_invalid_price_bridge(scale, error):
    with pytest.raises(ValueError):
        price_allowance(scale, error)
