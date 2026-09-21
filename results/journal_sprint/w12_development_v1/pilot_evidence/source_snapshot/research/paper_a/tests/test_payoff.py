import math

import numpy as np
import pytest

from research.paper_a.payoff import (
    C_RESCALING, a_calc, h_inverse, objective_amplitudes,
    presentation_clipped, to_price,
)

K, U, C = 100.0, 177.24074841962909, C_RESCALING


def test_rescaling_factor_is_frozen():
    assert C_RESCALING == 0.25


def test_amplitudes_follow_the_frozen_angle_formula():
    x = np.array([90.0, 100.0, 140.0, U])
    y = np.maximum(0.0, x - K) / (U - K)
    theta = (math.pi / 4) * (1 - C) + (math.pi * C / 2) * y
    assert np.allclose(objective_amplitudes(x, K, U, C), np.sin(theta) ** 2)


def test_amplitudes_stay_in_the_unit_interval():
    x = np.linspace(0.0, U, 500)
    a = objective_amplitudes(x, K, U, C)
    assert (a >= 0).all() and (a <= 1).all()


def test_y_is_bounded_by_one_at_the_upper_support():
    """max x_i is U, so y = g/(U-K) never exceeds 1."""
    assert objective_amplitudes(np.array([U]), K, U, C)[0] <= 1.0


def test_zero_payoff_region_is_the_constant_baseline():
    baseline = math.sin((math.pi / 4) * (1 - C)) ** 2
    a = objective_amplitudes(np.array([10.0, 50.0, K]), K, U, C)
    assert np.allclose(a, baseline)


def test_h_inverse_round_trips_the_linearization():
    """h is the exact inverse of the LINEARIZED map, so it round-trips y."""
    for y in (0.0, 0.25, 0.5, 1.0):
        a_lin = 0.5 + (math.pi * C / 2) * y - math.pi * C / 4
        assert abs(h_inverse(a_lin, K, U, C) - y * (U - K)) < 1e-10


def test_h_matches_qiskit_post_processing_exactly():
    from qiskit.circuit.library import LinearAmplitudeFunction
    laf = LinearAmplitudeFunction(
        3, slope=[0.0, 1.0], offset=[0.0, 0.0], domain=(55.165149432260606, U),
        image=(0.0, U - K), rescaling_factor=C,
        breakpoints=[55.165149432260606, K])
    for a in (0.2, 0.339439213658, 0.5, 0.7):
        assert abs(h_inverse(a, K, U, C) - laf.post_processing(a)) < 1e-12


def test_discount_is_applied_exactly_once():
    r, T, a = 0.05, 0.25, 0.339439213658
    assert abs(to_price(a, K, U, C, r, T)
               - math.exp(-r * T) * h_inverse(a, K, U, C)) < 1e-14


def test_negative_prices_are_retained_not_clipped():
    price = to_price(0.0, K, U, C, 0.05, 1.0)
    assert price < 0
    assert presentation_clipped(price) == 0.0
    assert price != presentation_clipped(price)


def test_a_calc_is_the_probability_weighted_mean_amplitude():
    x = np.array([80.0, 100.0, 120.0, 160.0])
    pi = np.array([0.4, 0.3, 0.2, 0.1])
    expected = float((pi * objective_amplitudes(x, K, U, C)).sum())
    assert abs(a_calc(pi, x, K, U, C) - expected) < 1e-15


def test_smaller_c_shrinks_the_amplitude_span():
    """The E1 c-sweep tradeoff: smaller c means a more accurate
    linearization but a smaller signal to estimate."""
    x = np.linspace(K, U, 64)
    spans = [np.ptp(objective_amplitudes(x, K, U, cc))
             for cc in (0.05, 0.25, 0.5)]
    assert spans[0] < spans[1] < spans[2]


@pytest.mark.parametrize("bad_c", [0.0, -0.1])
def test_nonpositive_rescaling_is_rejected(bad_c):
    with pytest.raises(ValueError):
        h_inverse(0.5, K, U, bad_c)
