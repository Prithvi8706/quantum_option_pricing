"""Contract/method guards for the three-family finite theorem screen."""

from fractions import Fraction

import pytest

from research.limitation_program_20261001 import finite_estimator_theorem_screen as screen


@pytest.mark.parametrize("error", [0.0045, True, Fraction(1, 500)])
def test_changed_or_inexact_error_rejected(error):
    with pytest.raises(ValueError):
        screen.formula_intervals(error=error)


@pytest.mark.parametrize("failure", [0.003, False, Fraction(1, 100)])
def test_changed_or_inexact_failure_rejected(failure):
    with pytest.raises(ValueError):
        screen.formula_intervals(failure=failure)


@pytest.mark.parametrize("span", [256, 64.0, 40])
def test_old_residual_or_unmatched_normalization_rejected(span):
    with pytest.raises(ValueError):
        screen.formula_intervals(span=span)


def test_dollar_tolerance_becomes_current_exact_amplitude_tolerance():
    assert screen.AMPLITUDE_ERROR == Fraction(9, 128000)
    assert screen.FAILURE == Fraction(3, 1000)


def test_papers_query_formula_units_do_not_include_preparation_or_readout():
    assert "Grover" in screen.PRIMARY_SOURCES["original-IQAE"]["query_unit"]
    assert "Grover" in screen.PRIMARY_SOURCES["modified-IQAE"]["query_unit"]
    assert screen.PRIMARY_SOURCES["modified-IQAE"]["printed_query_wording_ambiguous"]
