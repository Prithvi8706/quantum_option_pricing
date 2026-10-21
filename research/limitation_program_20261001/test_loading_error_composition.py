"""Meaningful structure, observable and scalar-allocation fixtures."""

from fractions import Fraction

import numpy as np
import pytest

from research.limitation_program_20261001.loading_error_composition import (
    allowances,
    general_trace_upper,
    product_trace_squared,
    sqrt_lower,
)


def test_two_factor_exact_fidelity_identity_and_telescoping_bound():
    a, b = Fraction(1, 3), Fraction(2, 5)
    product = product_trace_squared([a, b], independent_pure_product=True)
    assert product == a**2 + b**2 - a**2 * b**2
    assert product <= a**2 + b**2
    assert product <= general_trace_upper([a, b]) ** 2


def test_two_qubit_density_matrix_matches_independent_product_formula():
    a, b = 0.25, 0.4
    state = np.kron([np.sqrt(1 - a * a), a], [np.sqrt(1 - b * b), b])
    ideal = np.array([1.0, 0.0, 0.0, 0.0])
    delta = np.outer(state, state) - np.outer(ideal, ideal)
    distance = np.abs(np.linalg.eigvalsh(delta)).sum() / 2
    expected = float(
        product_trace_squared([Fraction(1, 4), Fraction(2, 5)], independent_pure_product=True)
    )
    assert abs(distance**2 - expected) < 1e-14
    # A projector onto the positive eigenspace saturates the [0,M] bound.
    values, vectors = np.linalg.eigh(delta)
    positive = vectors[:, values > 1e-12]
    observable = 40 * positive @ positive.T
    assert abs(np.trace(observable @ delta) - 40 * distance) < 1e-12


def test_correlated_joint_states_cannot_use_equal_marginals_as_zero_product_error():
    rho = np.diag([0.5, 0, 0, 0.5])
    sigma = np.diag([0, 0.5, 0.5, 0])
    assert np.abs(np.linalg.eigvalsh(rho - sigma)).sum() / 2 == 1
    # Both individual reduced states are I/2; product structure is essential.
    assert np.array_equal(
        rho.diagonal().reshape(2, 2).sum(axis=0), sigma.diagonal().reshape(2, 2).sum(axis=0)
    )
    with pytest.raises(ValueError):
        product_trace_squared([Fraction(0), Fraction(0)], independent_pure_product=False)


@pytest.mark.parametrize("draws", [60, 468])
def test_actual_driver_scalar_allowances_fit_exact_reserved_dollars(draws):
    row = allowances(draws)
    assert row["conservative_scalar_trace_allowance"] == Fraction(1, 40000 * draws)
    assert (
        row["pure_product_scalar_trace_allowance_lower"]
        > row["conservative_scalar_trace_allowance"]
    )
    assert row["exact_pure_product_trace_squared_upper"] <= Fraction(1, 40000) ** 2


def test_general_mixed_state_telescoping_bound_saturates_at_one():
    assert general_trace_upper([Fraction(3, 4), Fraction(3, 4)]) == 1
    assert product_trace_squared([Fraction(1), Fraction(0)], independent_pure_product=True) == 1


def test_dyadic_sqrt_lower_is_conservative_even_with_finite_truncation():
    value = Fraction(2, 3)
    bound = sqrt_lower(value, bits=17)
    assert bound**2 <= value < (bound + Fraction(1, 2**17)) ** 2


@pytest.mark.parametrize("errors", [[], [Fraction(-1, 2)], [Fraction(3, 2)], [0.1], [True]])
def test_invalid_or_inexact_trace_errors_are_rejected(errors):
    with pytest.raises(ValueError):
        general_trace_upper(errors)
