import numpy as np
import pytest

from research.journal_sprint.classical_baselines import brownian_pca, geometric_price, estimate
from research.paper_a.references import black_scholes_call


@pytest.mark.parametrize("d", [1, 8, 32])
def test_pca_covariance(d):
    dates, matrix = brownian_pca(d, 1.5)
    assert np.allclose(matrix @ matrix.T, np.minimum.outer(dates, dates), atol=1e-12)


def test_geometric_one_date_is_european():
    assert geometric_price(100, 100, 0.05, 0.2, 1, 1) == pytest.approx(
        black_scholes_call(100, 100, 0.05, 0.2, 1)
    )


def test_cost_and_reproducibility():
    spec = {
        "kind": "asian",
        "d": 8,
        "S0": 100.0,
        "K": 100.0,
        "rate": 0.05,
        "sigma": 0.2,
        "maturity": 1.0,
    }
    one = estimate(spec, "rqmc", 128, ("test",))
    two = estimate(spec, "rqmc", 128, ("test",))
    assert one["price"] == two["price"]
    assert one["total_paths"] == 1152
    assert len(one["scramble_means"]) == 32


@pytest.mark.parametrize("d", [8, 32])
def test_multidate_geometric_against_independent_quadrature(d):
    from scipy.integrate import quad
    from scipy.stats import norm

    # Closed sums for equally spaced Brownian covariances, not the PCA code.
    mu = np.log(100) + (0.05 - 0.2**2 / 2) * (d + 1) / (2 * d)
    variance = 0.2**2 * (d + 1) * (2 * d + 1) / (6 * d * d)
    cutoff = (np.log(100) - mu) / np.sqrt(variance)
    value, _ = quad(
        lambda z: np.exp(-0.05) * (np.exp(mu + np.sqrt(variance) * z) - 100) * norm.pdf(z),
        cutoff,
        12,
        epsabs=1e-11,
    )
    assert geometric_price(100, 100, 0.05, 0.2, 1, d) == pytest.approx(value, abs=1e-10)
