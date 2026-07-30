"""Signed deterministic error ladder.

The five-term decomposition telescopes by construction, so the identity
check is a float-arithmetic guard on the bookkeeping, not evidence about
the physics. Report it as such.
"""
from __future__ import annotations

from dataclasses import dataclass

from research.paper_a.benchmark import Contract
from research.paper_a.european.circuits import build_european, p_circuit
from research.paper_a.references import (
    black_scholes_call, p_grid, support_audit,
)


@dataclass(frozen=True)
class ErrorLadder:
    P_BS: float
    P_support: float
    P_grid: float
    P_circuit: float
    e_support: float
    e_grid: float
    e_encode: float


def deterministic_ladder(c: Contract, q_total: float, n: int,
                         rescaling: float) -> ErrorLadder:
    audit = support_audit(c, q_total)
    bs = black_scholes_call(c.S0, c.K, c.r, c.sigma, c.T)
    grid = p_grid(c, audit.L, audit.U, n)
    ec = build_european(c, audit.L, audit.U, n, rescaling)
    circuit = p_circuit(c, ec, rescaling)
    return ErrorLadder(
        P_BS=bs, P_support=audit.P_support, P_grid=grid, P_circuit=circuit,
        e_support=audit.P_support - bs,
        e_grid=grid - audit.P_support,
        e_encode=circuit - grid,
    )


def total_mean_error(ladder: ErrorLadder, e_est_mean: float,
                     delta_noise: float) -> float:
    """e_total_mean = e_support + e_grid + e_encode + e_est_mean + Delta_noise."""
    return (ladder.e_support + ladder.e_grid + ladder.e_encode
            + e_est_mean + delta_noise)


def identity_residual(ladder: ErrorLadder, e_est_mean: float,
                      delta_noise: float, e_total_mean: float) -> float:
    return total_mean_error(ladder, e_est_mean, delta_noise) - e_total_mean
