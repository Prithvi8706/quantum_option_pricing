"""Independent controller and finite-unitary checks for the explicit schedule."""

from fractions import Fraction

import numpy as np
import pytest

from research.controlled_priority_completion.estimator_hadamard import (
    candidate,
    controller,
    exact_tail,
    hadamard_plus_probability,
    probability_bounds,
)


@pytest.fixture(scope="module")
def allocation():
    return candidate(
        0.19448064336973883, 0.002030226129231438, 0.003, 32, Fraction(1, 8), 5, certify=True
    )


def test_exact_confidence_union_and_radius(allocation):
    assert allocation["certificates_complete"]
    assert allocation["normalizer"] >= 16
    assert allocation["final_radius"] <= allocation["error"]
    total = Fraction(0)
    for row in allocation["stages"]:
        a = Fraction(*row["p_plus_small_lower_exact"])
        b = Fraction(*row["p_plus_large_upper_exact"])
        r, k = row["repetitions"], row["small_if_plus_count_at_least"]
        small = exact_tail(r, a, upper=k - 1)
        large = exact_tail(r, b, lower=k)
        total += max(small, large)
    assert total <= Fraction(allocation["ideal_test_failure"])


@pytest.mark.parametrize("c", [Fraction(1, 10), Fraction(1, 8), Fraction(1, 4), Fraction(1, 2)])
def test_balanced_interval_geometry(c):
    width = Fraction(7, 3)
    epsilon = width / (1 + 3 * c)
    target = c * epsilon
    q = (1 + c) / (1 + 3 * c)
    assert target - c * epsilon == 0
    assert target + epsilon == q * width
    assert width - (target + c * epsilon) == q * width
    # Small is compulsory below this point; large is compulsory above it.
    assert target + c * epsilon <= target + epsilon


def test_controller_all_legal_ambiguity_choices(allocation):
    radius = Fraction(*allocation["initial_radius_exact"])
    c = Fraction(*allocation["c_exact"])
    q = Fraction(*allocation["contraction_exact"])
    for mu in (radius * Fraction(j, 10) for j in range(-10, 11)):
        for choose_small_in_gap in (True, False):
            left, width = -radius, 2 * radius

            def measure(stage, target_raw):
                nonlocal left, width
                eps = width / (1 + 3 * c)
                target = left + c * eps
                assert target_raw == round(target * 2**64)
                distance = abs(mu - target)
                small = (distance <= c * eps) or (distance < eps and choose_small_in_gap)
                if not small:
                    left += 2 * c * eps
                width *= q
                assert left <= mu <= left + width
                return [small] * stage["repetitions"]

            result = controller(allocation, measure)
            assert abs(result["estimate"] - float(mu)) <= result["radius"] + 1e-15


def test_spectral_hadamard_probabilities(allocation):
    rng = np.random.default_rng(2026092801)
    rms = Fraction(*allocation["normalized_RMS_upper_exact"])
    c = Fraction(*allocation["c_exact"])
    rows = allocation["stages"]
    for stage in (rows[0], rows[len(rows) // 2], rows[-1]):
        eps = Fraction(*stage["test_epsilon_exact"])
        a, b = probability_bounds(rms, eps, c, allocation["C"], stage["T"], certify=True)
        for regime, means in (
            ("small", [0.0, float(c * eps) / 2, float(c * eps)]),
            ("large", [float(eps), float((1 + 2 * c) * eps)]),
        ):
            for mean in means:
                for sign in (-1, 1):
                    for skew in (0.5, 0.001, 0.999, 0.000001):
                        p = np.array([skew, 1 - skew])
                        centered = rng.normal(size=2)
                        centered -= p @ centered
                        centered *= np.sqrt(max(0.0, float(rms) ** 2 - mean**2) / (p @ centered**2))
                        values = sign * mean + centered
                        actual = hadamard_plus_probability(values, p, stage["T"])
                        if regime == "small":
                            assert actual >= float(a) - 1e-8
                        else:
                            assert actual <= float(b) + 1e-8


def test_invalid_measurement_rejected(allocation):
    with pytest.raises(ValueError):
        controller(allocation, lambda stage, target: [1] * stage["repetitions"])
