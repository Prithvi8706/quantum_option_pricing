"""Check the grid theorem against exact one-date knockout expectations."""

from fractions import Fraction

import mpmath as mp
import pytest

from research.limitation_program_20261001.barrier_band_certificate import original_model
from research.limitation_program_20261001.quantile_grid_certificate import law_bound


@pytest.mark.parametrize("case,dimension", [("B4x12", 60), ("B8x52", 468)])
def test_contract_dimension_exact_dollars_and_transfer_guards(case, dimension):
    row = law_bound(original_model(case))
    assert Fraction(*row["all_date_continuous_payoff_grid_law_error_upper_dollars_exact"]) == (
        Fraction(dimension * 40, 2**32)
    )
    assert row["ideal_grid_law_term_fits_headroom"]
    assert not row["accepted_Box_Muller_law_certified"]
    assert not row["native_rounded_inverse_CDF_or_path_certified"]
    assert not row["coherent_loader_implemented"]
    assert not row["complete_original_price_certified"]


@pytest.mark.parametrize("bits", [0, 65, True, 32.0])
def test_precision_guard(bits):
    with pytest.raises(ValueError):
        law_bound(original_model(), bits)


def test_changed_model_rejected():
    model = original_model()
    model["barrier_dollars_exact"] = [141, 1]
    with pytest.raises(ValueError):
        law_bound(model)


@pytest.mark.parametrize(
    "field,value",
    [
        ("basket", "negative weighted spread"),
        ("equal_asset_volatility", False),
        ("continuous_driver_law", "dependent paired finite normals"),
    ],
)
def test_proof_assumption_mutations_rejected(field, value):
    model = original_model()
    model[field] = value
    with pytest.raises(ValueError):
        law_bound(model)


def test_coarse_grid_can_fail_the_same_allowance():
    assert not law_bound(original_model(), 16)["ideal_grid_law_term_fits_headroom"]


@pytest.mark.parametrize("bits", [4, 8])
def test_numerical_gaussian_toy_closed_price_within_analytic_variation_bound(bits):
    # Approximate high-precision fixture; the analytic theorem supplies the proof.
    # This is not a B4/B8 price observation or native circuit replay.
    mp.mp.dps = 90
    sigma, rate, spot, strike, barrier = map(mp.mpf, (".3", ".03", "100", "100", "140"))
    drift = rate - sigma**2 / 2
    lower = -drift / sigma
    upper = (mp.log(barrier / spot) - drift) / sigma

    def cdf(z):
        return (1 + mp.erf(z / mp.sqrt(2))) / 2

    continuous = mp.exp(-rate) * (
        spot * mp.exp(rate) * (cdf(upper - sigma) - cdf(lower - sigma))
        - strike * (cdf(upper) - cdf(lower))
    )
    total = mp.mpf(0)
    for raw in range(1 << bits):
        u = (mp.mpf(raw) + mp.mpf(".5")) / (1 << bits)
        z = mp.sqrt(2) * mp.erfinv(2 * u - 1)
        stock = spot * mp.exp(drift + sigma * z)
        if stock < barrier:
            total += mp.exp(-rate) * max(mp.mpf(0), stock - strike)
    discrete = total / (1 << bits)
    assert abs(discrete - continuous) <= mp.mpf(40) / (1 << bits)


def test_midpoint_jump_is_paid_by_variation_bound():
    # A jump located exactly at the midpoint attains w*TV/2, with strict survival.
    width = Fraction(1, 16)
    cap = Fraction(40)
    integral = width * cap / 2
    midpoint_estimate = Fraction(0)
    assert abs(integral - midpoint_estimate) == width * cap / 2
