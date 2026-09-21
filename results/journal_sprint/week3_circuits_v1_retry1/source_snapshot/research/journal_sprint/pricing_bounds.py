"""Exact-arithmetic bounds evaluated numerically; no target-price oracle inputs."""

from dataclasses import dataclass
import math

import numpy as np
from scipy.stats import lognorm, norm

from research.paper_a.references import grid_points, grid_probabilities, support_bounds


@dataclass(frozen=True)
class PriceBounds:
    lower: float
    upper: float
    sensitivity: float
    offset: float
    support: float
    grid: float
    encoding: float
    total_variation: float

    @property
    def total(self):
        return self.support + self.grid + self.encoding

    def probability_budget(self, dollars):
        if not math.isfinite(dollars) or dollars <= 0:
            raise ValueError("dollar tolerance must be positive and finite")
        return max(0.0, (dollars - self.total) / self.sensitivity)


def bounds_for(contract, n, scale, q_total=1e-5):
    """No Black-Scholes, exact grid payoff or encoded target is consulted."""
    if not isinstance(n, int) or isinstance(n, bool) or not 1 <= n <= 20:
        raise ValueError("n must be an integer in [1,20]")
    if not 0 < scale <= 1 or not 0 < q_total < 1:
        raise ValueError("scale and q_total out of range")
    c = contract
    if not all(math.isfinite(v) for v in (c.S0, c.K, c.r, c.T, c.sigma)):
        raise ValueError("contract parameters must be finite")
    if min(c.S0, c.K, c.T, c.sigma) <= 0:
        raise ValueError("spot, strike, maturity and volatility must be positive")
    lower, upper = support_bounds(c, q_total)
    discount = math.exp(-c.r * c.T)
    s = c.sigma * math.sqrt(c.T)
    mu = math.log(c.S0) + (c.r - c.sigma**2 / 2) * c.T
    distribution = lognorm(s=s, scale=math.exp(mu))
    omitted = float(distribution.cdf(lower) + distribution.sf(upper))
    retained = 1 - omitted
    # lower < K < upper by the support rule, so omitted lower payoff is zero.
    z = (math.log(upper) - mu) / s
    upper_payoff = math.exp(mu + s * s / 2) * norm.sf(z - s) - c.K * norm.sf(z)
    support = discount * (max(0.0, float(upper_payoff)) + omitted * (upper - c.K))
    x = grid_points(lower, upper, n)
    edges = np.concatenate(([lower], (x[:-1] + x[1:]) / 2, [upper]))
    # Survival differences avoid cancellation in upper-tail bins.
    cdf = distribution.cdf(edges)
    sf = distribution.sf(edges)
    masses = np.where(cdf[:-1] > 0.5, sf[:-1] - sf[1:], np.diff(cdf)) / retained
    point_weights = grid_probabilities(c, lower, upper, n)
    tv = float(np.sum(abs(masses - point_weights)) / 2)
    spacing = (upper - lower) / (2**n - 1)
    grid = discount * (spacing / 2 + (upper - c.K) * tv)
    encoding = discount * (upper - c.K) * math.pi**2 * scale**2 / 48
    sensitivity = discount * (upper - c.K) * 2 / (math.pi * scale)
    offset = sensitivity * (-0.5 + math.pi * scale / 4)
    return PriceBounds(lower, upper, sensitivity, offset, support, grid, encoding, tv)
