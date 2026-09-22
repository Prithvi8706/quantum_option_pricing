"""Independent numerical checks of analytic inequalities and witness premises."""

import math

import mpmath as mp
import pytest

from research.compound_feasibility.model import MODELS
from research.controlled_completion_followup.financial_bridge import (
    certificate,
    clipping_bounds,
    control_identity_counterexample,
    normal_l1_bound,
    upper,
)
from research.controlled_completion_followup.financial_arithmetic_audit import (
    certified_low_precision_witness,
)


@pytest.mark.parametrize("bits", [2, 3, 5, 8])
def test_box_muller_radial_bound_against_exact_cell_integrals(bits):
    mp.mp.dps = 50
    mp.iv.dps = 60
    h = mp.mpf(2) ** -bits

    def integral(x):
        if x == 0:
            return mp.mpf(0)
        r = mp.sqrt(-2 * mp.log(x))
        return x * r + mp.sqrt(mp.pi / 2) * mp.erfc(r / mp.sqrt(2))

    radial = sum(
        2 * integral((j + mp.mpf(".5")) * h) - integral(j * h) - integral((j + 1) * h)
        for j in range(2**bits)
    )
    rm = sum(mp.sqrt(-2 * mp.log((j + mp.mpf(".5")) * h)) * h for j in range(2**bits))
    # The actual radial error plus the same angular Lipschitz bound must fit.
    assert radial + mp.pi * h * rm < upper(normal_l1_bound(bits))


@pytest.mark.parametrize("model", MODELS, ids=lambda m: m.name)
def test_clipping_inequalities_against_exact_lognormal_formulas(model):
    mp.mp.dps = 100
    mp.iv.dps = 70
    def phi(x):
        return mp.exp(-x * x / 2) / mp.sqrt(2 * mp.pi)

    def survival(x):
        return mp.erfc(x / mp.sqrt(2)) / 2
    for j in range(1, model.dates + 1):
        t = mp.mpf(str(model.maturity)) * j / model.dates
        v = mp.mpf(str(model.sigma)) ** 2 * t
        sd = mp.sqrt(v)
        mu = mp.log(model.spot) + (mp.mpf(str(model.rate)) - mp.mpf(str(model.sigma)) ** 2 / 2) * t
        lo, hi = mp.mpf(2) ** -16, mp.mpf(4096)
        zl, zh = (mu - mp.log(lo)) / sd, (mp.log(hi) - mu) / sd
        stock_exact = lo * survival(zl) - mp.exp(mu + v / 2) * survival(zl + sd)
        stock_exact += mp.exp(mu + v / 2) * survival(zh - sd) - hi * survival(zh)
        log_exact = sd * (phi(zl) - zl * survival(zl) + phi(zh) - zh * survival(zh))
        stock_bound, log_bound = clipping_bounds(model, str(t))
        assert 0 <= stock_exact <= upper(stock_bound)
        assert 0 <= log_exact <= upper(log_bound)


@pytest.mark.parametrize("model", MODELS, ids=lambda m: m.name)
def test_high_precision_law_budget_and_even_normal_pair_split(model):
    assert (model.dates // 2 * (model.assets + 1)) % 2 == 0
    fine, coarse = certificate(model, 32), certificate(model, 16)
    assert fine["law_and_controls_total_upper"] < 0.00003
    assert fine["remaining_for_arithmetic"] > 0.00197
    assert coarse["law_and_controls_total_upper"] > 0.002


@pytest.mark.parametrize("model", MODELS[1:], ids=lambda m: m.name)
def test_exact_finite_control_identity_is_false(model):
    witness = control_identity_counterexample(model)
    assert witness["tau_log_lower"] > witness["guard_log_upper"]
    assert witness["accrued_lower"] > model.strike
    assert witness["conditional_control_bias_lower_before_outer_discount"] > 17


def test_reachable_f24_error_exceeds_uniform_arithmetic_budget():
    witness = certified_low_precision_witness()
    assert witness["absolute_arithmetic_error_lower"] > 0.005
    assert witness["digital_Y_6"] == 0
    assert math.isfinite(witness["digital_base_6"])
