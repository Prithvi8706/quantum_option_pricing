"""Reference price ladder, layers 1-2: continuous and support-conditioned.

Nothing in this module touches Qiskit. These are the independent references
that circuit output is checked against.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np
from scipy import integrate
from scipy.stats import lognorm, norm

from research.paper_a.benchmark import Contract


def black_scholes_call(S0: float, K: float, r: float, sigma: float,
                       T: float) -> float:
    """P_BS: continuous, untruncated Black-Scholes call price."""
    d1 = (math.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return S0 * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)


def _lognormal(c: Contract):
    """Risk-neutral terminal-price distribution as a frozen scipy object."""
    mu_ln = (c.r - 0.5 * c.sigma ** 2) * c.T + math.log(c.S0)
    s_ln = c.sigma * math.sqrt(c.T)
    return lognorm(s=s_ln, scale=math.exp(mu_ln))


@dataclass(frozen=True)
class SupportAudit:
    L: float
    U: float
    m: float
    omitted_mass: float
    C_tail: float
    normalization: float
    P_support: float
    support_bias: float


def support_bounds(c: Contract, q_total: float) -> tuple[float, float]:
    """L = min(F^-1(q/2), 0.98K), U = max(F^-1(1-q/2), 1.02K)."""
    dist = _lognormal(c)
    L = min(float(dist.ppf(q_total / 2.0)), 0.98 * c.K)
    U = max(float(dist.ppf(1.0 - q_total / 2.0)), 1.02 * c.K)
    return L, U


def support_audit(c: Contract, q_total: float) -> SupportAudit:
    """Store retained mass, omitted mass, omitted payoff, and bias separately."""
    dist = _lognormal(c)
    L, U = support_bounds(c, q_total)
    D = math.exp(-c.r * c.T)
    m = float(dist.cdf(U) - dist.cdf(L))

    def payoff_density(s: float) -> float:
        return max(0.0, s - c.K) * dist.pdf(s)

    inside, _ = integrate.quad(payoff_density, L, U, limit=400)
    below, _ = integrate.quad(payoff_density, 0.0, L, limit=400)
    above, _ = integrate.quad(payoff_density, U, np.inf, limit=400)

    P_support = (D / m) * inside
    C_tail = D * (below + above)
    P_bs = black_scholes_call(c.S0, c.K, c.r, c.sigma, c.T)
    return SupportAudit(L=L, U=U, m=m, omitted_mass=1.0 - m, C_tail=C_tail,
                        normalization=1.0 / m, P_support=P_support,
                        support_bias=P_support - P_bs)


def select_support_rule(contracts: Iterable[Contract],
                        candidates: Sequence[float]) -> float:
    """Freeze the least-wide q_total passing all three gates on every contract.

    Least-wide support = largest q_total, so candidates are tried from
    largest to smallest and the first that passes everywhere wins.
    """
    rows = list(contracts)
    for q in sorted(candidates, reverse=True):
        if all(
            (a := support_audit(c, q)).omitted_mass <= 1e-4
            and a.C_tail <= 1e-4 * c.S0
            and abs(a.support_bias) <= 1e-4 * c.S0
            for c in rows
        ):
            return q
    raise ValueError("no candidate q_total passes all support gates")


def grid_points(L: float, U: float, n: int) -> np.ndarray:
    """x_i = L + i(U-L)/(2^n - 1), the frozen finite point grid."""
    count = 2 ** n
    return L + np.arange(count) * (U - L) / (count - 1)


def grid_probabilities(c: Contract, L: float, U: float, n: int) -> np.ndarray:
    """pi_i = f(x_i) / sum_l f(x_l): normalized POINTWISE densities.

    This matches Qiskit's LogNormalDistribution semantics. Integrated bin
    masses are a different quantity and are never substituted here.
    """
    density = _lognormal(c).pdf(grid_points(L, U, n))
    return density / density.sum()


def p_grid(c: Contract, L: float, U: float, n: int) -> float:
    """P_grid: exact expectation on the frozen grid, exact payoff, classical."""
    x = grid_points(L, U, n)
    pi = grid_probabilities(c, L, U, n)
    payoff = np.maximum(0.0, x - c.K)
    return math.exp(-c.r * c.T) * float((pi * payoff).sum())
