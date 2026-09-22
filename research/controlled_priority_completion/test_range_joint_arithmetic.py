"""Independent numerical and algebraic checks of the joint-bound components."""

import math

import mpmath as mp
import numpy as np
import pytest

from research.compound_feasibility.model import MODELS
from research.controlled_priority_completion.range_joint_arithmetic import (
    Q,
    cdf_interval,
    checked_constants,
    coefficient_certificate,
    certificate,
    control_arithmetic,
)
from research.controlled_source_completion.finance import lognormal
from research.controlled_source_completion.ir import Graph, evaluate


@pytest.fixture(scope="module")
def elementary():
    return coefficient_certificate()


def test_erf_series_interval_contains_independent_high_precision_reference():
    mp.mp.dps = 100
    mp.iv.dps = 80
    for x in (-8, -7.96875, -4, -0.03125, 0, 0.03125, 4, 7.96875, 8):
        interval = cdf_interval(mp.iv.mpf(x))
        reference = (1 + mp.erf(mp.mpf(x) / mp.sqrt(2))) / 2
        assert mp.mpf(interval._mpi_[0]) <= reference <= mp.mpf(interval._mpi_[1])


@pytest.mark.parametrize("bits", [4, 8, 12, 16])
def test_discrete_reciprocal_radius_inequality(bits):
    h = 2.0**-bits
    u = (np.arange(1 << bits, dtype=float) + 0.5) * h
    actual = float(np.mean(1 / np.sqrt(-2 * np.log(u))))
    assert actual <= math.sqrt(math.pi / 2) + math.sqrt(h)


@pytest.mark.parametrize("model", [MODELS[0], MODELS[-1]], ids=["C4", "H8"])
def test_lognormal_arithmetic_uniform_bound_at_difficult_inputs(model, elementary):
    mp.mp.dps = 100
    _, controls, _, _, _ = checked_constants(model)
    for _, vfloat, variance in (controls[0], controls[1], controls[-1]):
        bound, _ = control_arithmetic(vfloat, variance, elementary)
        vr = mp.mpf(variance._mpi_[0])
        for mu in (-11.0, math.log(100), math.log(4096)):
            for strike in (-3896.0, 0.0, 1 / Q, 1.0e-6, 100.0, 200.0):
                g = Graph(40)
                call, put = lognormal(g, g.c(mu), g.c(vfloat), g.c(strike))
                g.outputs = {"call": call, "put": put}
                result = evaluate(g.as_dict(), {})
                mr = mp.mpf(round(mu * Q)) / Q
                kr = mp.mpf(round(strike * Q)) / Q
                mean = mp.exp(mr + vr / 2)
                if kr <= 0:
                    real_call, real_put = mean - kr, mp.mpf(0)
                else:
                    d2 = (mr - mp.log(kr)) / mp.sqrt(vr)
                    d1 = d2 + mp.sqrt(vr)
                    def cdf(x):
                        return (1 + mp.erf(x / mp.sqrt(2))) / 2
                    real_call = mean * cdf(d1) - kr * cdf(d2)
                    real_put = kr * cdf(-d2) - mean * cdf(-d1)
                assert abs(mp.mpf(result["call"]) - real_call) <= mp.mpf(bound._mpi_[1])
                assert abs(mp.mpf(result["put"]) - real_put) <= mp.mpf(bound._mpi_[1])


def test_all_models_leave_numeric_budget_for_existing_financial_bridge(elementary):
    for model in MODELS:
        result = certificate(model, elementary)
        assert result["expectation_terms"]["joint_arithmetic_dollars"] + 0.000029 < 0.002
        assert max(c["error"] for c in result["constants"]) < 1 / Q
