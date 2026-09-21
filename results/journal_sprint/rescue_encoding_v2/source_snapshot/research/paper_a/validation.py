"""E0 gate battery.

No stochastic experiment starts until every gate here passes. Tolerances are
frozen; changing one requires a versioned amendment before E1 outputs are
inspected.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np
from qiskit.quantum_info import Statevector

from research.paper_a.benchmark import Contract
from research.paper_a.errors import deterministic_ladder
from research.paper_a.european.circuits import build_european, statevector_amplitude
from research.paper_a.payoff import (
    a_calc,
    h_inverse,
    presentation_clipped,
    to_price,
)
from research.paper_a.references import (
    grid_points,
    grid_probabilities,
    support_audit,
)

TOL_NORMALIZATION = 1e-12
TOL_PMF_MAX = 1e-12
TOL_PMF_L1 = 1e-10
TOL_OBJECTIVE = 1e-10
TOL_RELATIVE = 1e-10


@dataclass(frozen=True)
class GateResult:
    name: str
    passed: bool
    worst: float
    tolerance: float
    detail: str


def _gate(name: str, worst: float, tolerance: float, detail: str) -> GateResult:
    return GateResult(name, worst <= tolerance, worst, tolerance, detail)


def run_e0_gates(
    contracts: Sequence[Contract], q_total: float, qubit_counts: Sequence[int], rescaling: float
) -> list[GateResult]:
    worst = {
        k: (0.0, "")
        for k in (
            "probability_normalization",
            "pmf_max_elementwise",
            "pmf_l1",
            "objective_probability",
            "dollar_round_trip",
            "error_identity",
            "discount_applied_once",
            "raw_and_clipped_separate",
        )
    }

    def bump(key: str, value: float, detail: str) -> None:
        if value > worst[key][0]:
            worst[key] = (value, detail)

    for c in contracts:
        audit = support_audit(c, q_total)
        scale = max(1.0, c.S0)
        for n in qubit_counts:
            tag = f"{c.id} n={n}"
            x = grid_points(audit.L, audit.U, n)
            pi = grid_probabilities(c, audit.L, audit.U, n)
            bump("probability_normalization", abs(pi.sum() - 1.0), tag)

            ec = build_european(c, audit.L, audit.U, n, rescaling)
            circuit_pmf = Statevector(ec.circuit).probabilities(range(n))
            bump("pmf_max_elementwise", float(np.abs(circuit_pmf - pi).max()), tag)
            bump("pmf_l1", float(np.abs(circuit_pmf - pi).sum()), tag)

            expected_a = a_calc(pi, x, c.K, audit.U, rescaling)
            a_sv = statevector_amplitude(ec)
            bump("objective_probability", abs(a_sv - expected_a), tag)

            # Independent encoded payoff expectation. Do not compare to the
            # linear grid payoff: its encoding error is deliberately nonzero.
            price = to_price(a_sv, c.K, audit.U, rescaling, c.r, c.T)
            undiscounted = h_inverse(a_sv, c.K, audit.U, rescaling)
            normalized_payoff = np.maximum(x - c.K, 0.0) / (audit.U - c.K)
            angles = np.pi / 4 + np.pi * rescaling / 2 * (normalized_payoff - 0.5)
            encoded_payoff = (audit.U - c.K) * (
                0.5 + (2 * np.sin(angles) ** 2 - 1) / (np.pi * rescaling)
            )
            reference_payoff = float(np.dot(pi, encoded_payoff))
            expected_price = math.exp(-c.r * c.T) * reference_payoff
            bump(
                "dollar_round_trip",
                max(abs(price - expected_price), abs(undiscounted - reference_payoff)) / scale,
                tag,
            )

            # Discount applied EXACTLY once: the price must match a single
            # discount and must be measurably far from a doubled one.
            once = expected_price
            twice = math.exp(-2.0 * c.r * c.T) * reference_payoff
            single_gap = abs(price - once) / scale
            double_gap = abs(price - twice) / scale
            bump("discount_applied_once", single_gap if double_gap > TOL_RELATIVE else 1.0, tag)

            # Raw and clipped must be genuinely separate quantities. Drive the
            # amplitude below the zero-price point so the raw value is negative
            # and the clipped value provably differs from it.
            negative_raw = to_price(0.0, c.K, audit.U, rescaling, c.r, c.T)
            clipped = presentation_clipped(negative_raw)
            separated = negative_raw < 0.0 and clipped == 0.0 and clipped != negative_raw
            bump("raw_and_clipped_separate", 0.0 if separated else 1.0, tag)

            ladder = deterministic_ladder(c, q_total, n, rescaling)
            telescoped = ladder.e_support + ladder.e_grid + ladder.e_encode
            bump("error_identity", abs(telescoped - (ladder.P_circuit - ladder.P_BS)) / scale, tag)

    tolerances = {
        "probability_normalization": TOL_NORMALIZATION,
        "pmf_max_elementwise": TOL_PMF_MAX,
        "pmf_l1": TOL_PMF_L1,
        "objective_probability": TOL_OBJECTIVE,
        "dollar_round_trip": TOL_RELATIVE,
        "error_identity": TOL_RELATIVE,
        "discount_applied_once": TOL_RELATIVE,
        "raw_and_clipped_separate": 0.0,
    }
    return [_gate(name, value, tolerances[name], detail) for name, (value, detail) in worst.items()]


def all_passed(results: Sequence[GateResult]) -> bool:
    return all(r.passed for r in results)
