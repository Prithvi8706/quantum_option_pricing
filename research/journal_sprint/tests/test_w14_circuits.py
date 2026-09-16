"""Small fixture-only nonzero Grover/noise semantics."""

import math

import numpy as np
import pytest

from research.journal_sprint.asian_basket import Basket
from research.journal_sprint.asian_encoding import grid
from research.journal_sprint.w14_circuits import response, fixed_interval


@pytest.mark.parametrize("rep", ["raw", "residual"])
@pytest.mark.parametrize("k", [0, 1, 2, 4])
def test_actual_unitary_and_density_response(rep, k):
    data = grid(Basket(1, 2, 71, spot=73, sigma=0.22), 1, 3.0)
    result = response(data, 1, rep, k, 0.037)
    a = result["amplitude"]
    theta = math.asin(math.sqrt(a))
    expected = 0.5 + (1 - 0.037) ** (2 * k + 1) * (math.sin((2 * k + 1) * theta) ** 2 - 0.5)
    assert result["density_probability"] == pytest.approx(expected, abs=1e-12)
    assert max(result["errors"].values()) < 1e-12
    assert result["minimum_eigenvalue"] > -1e-12
    assert result["A_calls"] == 2 * k + 1
    assert result["circuit"]["cx"] >= (2 * k + 1) * result["preparation"]["cx"]


@pytest.mark.parametrize("k,eta", [(True, 0), (-1, 0), (5, 0), (1, 1), (1, float("nan"))])
def test_invalid_controls(k, eta):
    with pytest.raises(ValueError):
        response({}, 1, "raw", k, eta)


def test_fixed_interval_known_noise_and_all_branches():
    a, eta = 0.173, 0.037
    depths = [0, 1, 2, 3, 4]
    probabilities = [
        0.5
        + (1 - eta) ** (2 * k + 1) * (math.sin((2 * k + 1) * math.asin(math.sqrt(a))) ** 2 - 0.5)
        for k in depths
    ]
    counts = [round(100000 * p) for p in probabilities]
    ci = fixed_interval(counts, [100000] * 5, depths, eta)
    assert ci.contains(a)
    assert ci.radius < 0.01
    assert np.isfinite(ci.radius)
