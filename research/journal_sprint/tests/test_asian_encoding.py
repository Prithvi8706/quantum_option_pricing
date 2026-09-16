"""Fixture-only semantics and bounds: no production configurations or RNGs."""

import math

import numpy as np
import pytest
from scipy.special import ndtr

from research.journal_sprint.asian_basket import Basket
from research.journal_sprint.asian_encoding import (
    grid, analytic_bounds, price_contract, measure,
)
from research.journal_sprint import asian_encoding


@pytest.fixture
def fixture():
    contract = Basket(2, 2, 71, spot=73, sigma=.22, correlation=.37)
    return contract, grid(contract, 1, 2.5)


def test_independent_path_and_endian_semantics(fixture):
    contract, data = fixture
    factor, means = data["model"]["factor"], data["model"]["means"]
    for index, normals in enumerate(data["normals"]):
        assert list(normals) == [(-1.25 if (index >> j) & 1 == 0 else 1.25)
                                 for j in range(4)]
        logs = [means[i] + math.fsum(factor[i, j] * normals[j] for j in range(4))
                for i in range(4)]
        raw = math.exp(-contract.rate) * max(math.fsum(math.exp(x) for x in logs) / 4 - 71, 0)
        control = math.exp(-contract.rate) * max(math.exp(math.fsum(logs) / 4) - 71, 0)
        assert data["raw"][index] == pytest.approx(raw, abs=1e-12)
        assert data["control"][index] == pytest.approx(control, abs=1e-12)
        assert data["residual"][index] >= 0
    assert data["weights"].sum() == pytest.approx(1)


@pytest.mark.parametrize("representation", ["raw", "residual"])
@pytest.mark.parametrize("loader", ["product", "dense"])
def test_compiled_joint_semantics_and_inverse(fixture, representation, loader):
    _, data = fixture
    result = measure(data, 1, representation, loader)
    assert result["max_joint_probability_error"] < 1e-12
    assert result["inverse_return_error"] < 1e-12
    assert result["state_fidelity_error"] < 1e-12
    assert result["shots"] == 0
    assert result["acquisition"]["cx"] >= result["payoff"]["cx"]


def test_nonuniform_marginal_and_contract_refuses_unknown_bias():
    c = Basket(1, 2, 71, spot=73, sigma=.22, correlation=.37)
    data = grid(c, 3, 2.5)
    edges = np.linspace(-2.5, 2.5, 9)
    assert data["marginal"] == pytest.approx(np.diff(ndtr(edges)) / (ndtr(2.5)-ndtr(-2.5)))
    assert not np.allclose(data["marginal"], np.ones(8)/8)
    for representation in ("raw", "residual"):
        for loader in ("product", "dense"):
            assert measure(data, 3, representation, loader)["max_joint_probability_error"] < 1e-12
        pc = price_contract(c, 3, 2.5, data, representation)
        assert pc.readiness(1) == "unknown_bias"
        with pytest.raises(ValueError, match="unknown bias"):
            pc.to_encoding(100)


def test_finite_and_analytic_offset_distinguished(fixture):
    c, d = fixture
    raw = float(d["weights"] @ d["raw"])
    residual = float(d["weights"] @ d["residual"])
    finite_control = float(d["weights"] @ d["control"])
    assert raw == pytest.approx(residual + finite_control)
    pc = price_contract(c, 1, 2.5, d, "residual")
    assert abs(pc.offset - finite_control) > 1e-4


def test_bound_monotonicity_and_finite_refinement(fixture):
    c, d = fixture
    for representation in ("raw", "residual"):
        b1 = analytic_bounds(c, 1, 2.5, d["model"], representation)
        b2 = analytic_bounds(c, 2, 2.5, d["model"], representation)
        assert b2["discretization"] == pytest.approx(b1["discretization"] / 2)
        assert 0 < b1["cube_probability"] < 1
        assert b1["tail_and_renormalization"] > 0
        fine = grid(c, 2, 2.5)
        diff = abs(float(d["weights"] @ d[representation])
                   - float(fine["weights"] @ fine[representation]))
        assert diff < b1["discretization"] + b2["discretization"]


@pytest.mark.parametrize("precision", [True, 0, -1, 2.0, 9])
def test_precision_rejected(fixture, precision):
    with pytest.raises(ValueError):
        grid(fixture[0], precision, 3)


@pytest.mark.parametrize("cutoff", [True, float("nan"), float("inf"), 0, 7])
def test_cutoff_rejected(fixture, cutoff):
    with pytest.raises(ValueError):
        grid(fixture[0], 1, cutoff)


def test_relative_phase_error_rejected(fixture, monkeypatch):
    original = asian_encoding.resources
    def phase_error(circuit):
        compiled, counts = original(circuit)
        compiled.z(0)
        return compiled, counts
    monkeypatch.setattr(asian_encoding, "resources", phase_error)
    with pytest.raises(ArithmeticError, match="semantics"):
        measure(fixture[1], 1, "raw", "product")
