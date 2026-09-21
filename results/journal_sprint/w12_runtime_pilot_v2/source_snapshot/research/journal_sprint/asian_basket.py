"""Classical Gaussian/PCA and conditional Asian-basket baselines, not quantum."""

from dataclasses import dataclass
import math

import numpy as np
from scipy.special import ndtr, ndtri
from scipy.stats import qmc


@dataclass(frozen=True)
class Basket:
    assets: int
    dates: int
    strike: float
    spot: float = 100.0
    sigma: float = 0.3
    rate: float = 0.03
    maturity: float = 1.0
    correlation: float = 0.5

    def __post_init__(self):
        for n in (self.assets, self.dates):
            if isinstance(n, bool) or not isinstance(n, int) or n < 1:
                raise ValueError("positive integer dimensions required")
        vals = (self.strike, self.spot, self.sigma, self.rate,
                self.maturity, self.correlation)
        if not all(math.isfinite(x) for x in vals):
            raise ValueError("nonfinite parameters")
        if min(self.strike, self.spot, self.sigma, self.maturity) <= 0:
            raise ValueError("positive scale parameters required")
        if not 0 < self.correlation < 1:
            raise ValueError("prototype requires positive, nonunit equicorrelation")


def pca_factor(covariance):
    values, vectors = np.linalg.eigh(covariance)
    if values.min() < -1e-10:
        raise ValueError("non-PSD covariance")
    order = np.argsort(values)[::-1]
    factor = vectors[:, order] * np.sqrt(np.maximum(values[order], 0))
    # Resolve eigenvector signs for reproducibility; repeated eigenspaces may
    # still rotate across LAPACK versions. Numeric replay is environment scoped.
    for j in range(factor.shape[1]):
        if factor[np.argmax(np.abs(factor[:, j])), j] < 0:
            factor[:, j] *= -1
    return factor


def setup(contract):
    d, steps = contract.assets, contract.dates
    times = np.linspace(contract.maturity / steps, contract.maturity, steps)
    temporal = np.minimum.outer(times, times)
    asset_cov = (1 - contract.correlation) * np.eye(d) + contract.correlation
    covariance = contract.sigma**2 * np.kron(asset_cov, temporal)
    factor = pca_factor(covariance)
    load = contract.sigma * math.sqrt(contract.correlation) * np.tile(
        times / math.sqrt(contract.maturity), d
    )
    # Condition on the common terminal factor. The residual covariance is
    # positive definite for rho<1: use d*steps residual normals, plus one
    # analytically integrated normal. No path table is enumerated.
    residual = pca_factor(covariance - np.outer(load, load))
    means = np.tile(math.log(contract.spot)
                    + (contract.rate - contract.sigma**2 / 2) * times, d)
    mu_g = float(means.mean())
    var_g = float(covariance.mean())
    expected_control = lognormal_call(mu_g, var_g, contract.strike) * math.exp(
        -contract.rate * contract.maturity
    )
    return dict(factor=factor, residual=residual, load=load, means=means,
                covariance=covariance, expected_control=expected_control)


def lognormal_call(mu, variance, strike):
    mu = np.asarray(mu)
    if variance < 0 or strike <= 0:
        raise ValueError("invalid lognormal call parameters")
    if variance == 0:
        return np.maximum(np.exp(mu) - strike, 0)
    std = math.sqrt(variance)
    d2 = (mu - math.log(strike)) / std
    return np.exp(mu + variance / 2) * ndtr(d2 + std) - strike * ndtr(d2)


def conditional_call(log_coefficients, slopes, strike):
    """Integrate (sum c_i exp(b_i Z)-K)+ over one Gaussian, b_i,c_i>0.

    Returns conditional payoff and maximum relative root residual. Finite
    bisection/numerical errors are checked, not proved by directed rounding.
    """
    lc = np.asarray(log_coefficients, dtype=float)
    b = np.asarray(slopes, dtype=float)
    if (lc.ndim != 2 or b.shape != (lc.shape[1],) or not np.all(np.isfinite(lc))
            or not np.all(np.isfinite(b)) or np.any(b <= 0)
            or not math.isfinite(strike) or strike <= 0):
        raise ValueError("invalid conditional payoff inputs")
    # Analytic bracket: at lower, every term <=K/p; at upper every term >=K/p.
    roots = (math.log(strike / len(b)) - lc) / b
    lo, hi = roots.min(axis=1), roots.max(axis=1)
    for _ in range(44):
        mid = (lo + hi) / 2
        with np.errstate(over="raise", invalid="raise"):
            value = np.exp(lc + mid[:, None] * b).sum(axis=1)
        low = value < strike
        lo = np.where(low, mid, lo)
        hi = np.where(low, hi, mid)
    root = (lo + hi) / 2
    residual = float(np.max(np.abs(np.exp(lc + root[:, None] * b).sum(axis=1) - strike)
                            / strike))
    if residual > 1e-8:
        raise ArithmeticError("conditional root failed tolerance")
    value = (np.exp(lc + b * b / 2) * ndtr(b - root[:, None])).sum(axis=1)
    value -= strike * ndtr(-root)
    if np.any(value < -1e-10) or not np.all(np.isfinite(value)):
        raise ArithmeticError("invalid conditional expectation")
    return np.maximum(value, 0), residual


def evaluate(contract, model, normals, conditional=False):
    z = np.asarray(normals)
    dim = contract.assets * contract.dates
    if z.ndim != 2 or z.shape[1] != dim or not np.all(np.isfinite(z)):
        raise ValueError("invalid normal sample matrix")
    logs = model["means"] + z @ (model["residual"] if conditional else model["factor"]).T
    discount = math.exp(-contract.rate * contract.maturity)
    if conditional:
        value, residual = conditional_call(logs - math.log(dim), model["load"], contract.strike)
        control = lognormal_call(logs.mean(axis=1), float(model["load"].mean()**2),
                                 contract.strike)
    else:
        value = np.maximum(np.exp(logs).mean(axis=1) - contract.strike, 0)
        control = np.maximum(np.exp(logs.mean(axis=1)) - contract.strike, 0)
        residual = 0.0
    return value * discount, control * discount, residual


def normal_points(dim, power, seed, method):
    if method == "mc_cv":
        z = np.random.default_rng(seed).normal(size=(2**(power - 1), dim))
        return np.concatenate([z, -z])
    engine = qmc.Sobol(dim, scramble=True, seed=seed)
    u = engine.random_base2(power)
    return ndtri(np.clip(u, np.nextafter(0.0, 1.0), np.nextafter(1.0, 0.0)))


def fit_control(contract, model, rng, conditional=False, count=1024):
    a, g, residual = evaluate(contract, model, rng.normal(size=(count, len(model["means"]))),
                              conditional)
    variance = float(np.var(g, ddof=1))
    beta = 0.0 if variance <= 1e-20 else float(np.cov(a, g, ddof=1)[0, 1] / variance)
    return beta, residual


def estimate(contract, model, power, seed, method, beta=0.0):
    z = normal_points(len(model["means"]), power, seed, method)
    values, controls, residuals = [], [], []
    for start in range(0, len(z), 512):
        a, g, residual = evaluate(contract, model, z[start:start + 512],
                                  conditional=method == "conditional_cv")
        values.append(a)
        controls.append(g)
        residuals.append(residual)
    adjusted = np.concatenate(values) - beta * (
        np.concatenate(controls) - model["expected_control"]
    )
    return float(adjusted.mean()), max(residuals)
