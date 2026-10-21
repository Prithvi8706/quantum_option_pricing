"""Coverage arithmetic, exact toy response and prospective admission guards."""

from fractions import Fraction
import math

import mpmath as mp
import pytest

from research.limitation_program_20261001 import finite_iqae_controller as controller


@pytest.mark.parametrize(
    "amplitude,power,expected",
    [
        (Fraction(1, 8), 0, Fraction(1, 8)),
        (Fraction(1, 8), 1, Fraction(25, 32)),
        (Fraction(1, 8), 2, Fraction(121, 128)),
        (Fraction(1, 4), 1, Fraction(1)),
        (Fraction(1, 2), 123, Fraction(1, 2)),
        (Fraction(0), 100, Fraction(0)),
        (Fraction(1), 100, Fraction(1)),
    ],
)
def test_exact_chebyshev_response_matches_known_rotation(amplitude, power, expected):
    assert controller.exact_grover_probability(amplitude, power) == expected


@pytest.mark.parametrize(
    "probability", [Fraction(0), Fraction(1, 8), Fraction(1, 4), Fraction(1, 2), Fraction(1)]
)
def test_outward_monotone_inverse_contains_high_precision_reference(probability):
    lower, upper = controller.inverse_probability(probability)
    if lower == upper:
        lo, hi = controller.angle_probability(lower)
        assert lo <= probability <= hi
        return
    with mp.workdps(130):
        actual = mp.asin(mp.sqrt(mp.mpf(probability.numerator) / probability.denominator)) / mp.pi
        assert (
            mp.mpf(lower.numerator) / lower.denominator
            <= actual
            <= mp.mpf(upper.numerator) / upper.denominator
        )


def test_hoeffding_radius_rounds_up_and_charges_two_sided_failure():
    _, _, radius = controller.hoeffding_interval(5, 16, Fraction(3, 20000))
    with mp.workdps(100):
        value = mp.mpf(radius.numerator) / radius.denominator
        assert 2 * mp.exp(-32 * value**2) <= mp.mpf(3) / 20000


def test_original_round_and_all_look_allocations_are_simultaneous():
    total = sum((Fraction(1, j * (j + 1)) for j in range(1, 9)), Fraction(0))
    assert total < 1
    assert 20 * controller.ALPHA / 20 * total < controller.ALPHA


def test_modified_cost_weight_allocations_sum_below_budget():
    cap = controller.power_cap()
    powers = [1]
    while 3 * powers[-1] <= cap:
        powers.append(3 * powers[-1])
    assert (
        sum((Fraction(2, 3) * controller.ALPHA * K / cap for K in powers), Fraction(0))
        <= controller.ALPHA
    )


def test_admission_budget_checks_before_observation(monkeypatch):
    monkeypatch.setattr(controller, "MAX_PAID_SOURCE_PAIRS", 15)
    calls = []
    result = controller.controller(lambda *args: calls.append(args), controller.SETTINGS[0])
    assert result["status"] == "censored" and result["paid_source_pairs"] == 0 and not calls
    assert result["amplitude_interval_exact"] is None


def test_exact_observer_endpoint_probabilities_need_no_approximation():
    assert controller.ExactToyObserver(Fraction(1, 4), 1)(1, 17) == 17
    assert controller.ExactToyObserver(0, 1)(100, 17) == 0


def test_controller_configuration_set_is_finite_before_observations():
    assert len(controller.SETTINGS) == 8 and len(controller.TOY_LAWS) == 2
    assert controller.MAX_PAID_SOURCE_PAIRS < 15 * (2**16 - 1)
    assert math.isfinite(controller.MAX_POWER_SEARCH_EVENTS)
