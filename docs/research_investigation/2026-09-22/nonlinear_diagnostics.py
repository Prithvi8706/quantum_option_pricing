"""Cheap falsification diagnostics; classical CPU arithmetic, no quantum execution.

Run with: python docs/research_investigation/2026-09-22/nonlinear_diagnostics.py
The timings are single-process observations, not optimized comparative benchmarks.
"""
import json
import math
import time
from pathlib import Path

import scipy
from scipy.integrate import quad
from scipy.special import ndtr


def call(s, strike, r, sigma, maturity):
    vol = sigma * math.sqrt(maturity)
    d1 = (math.log(s / strike) + (r + sigma * sigma / 2) * maturity) / vol
    return s * ndtr(d1) - strike * math.exp(-r * maturity) * ndtr(d1 - vol)


def compound(k_outer, sigma):
    s0, k_inner, r, t1, t2, cutoff = 100.0, 100.0, 0.03, 0.5, 1.0, 9.0
    evaluations = 0

    def f(z):
        nonlocal evaluations
        evaluations += 1
        s1 = s0 * math.exp((r - sigma * sigma / 2) * t1 + sigma * math.sqrt(t1) * z)
        continuation = call(s1, k_inner, r, sigma, t2 - t1)
        return (math.exp(-r * t1) * max(continuation - k_outer, 0.0)
                * math.exp(-z * z / 2) / math.sqrt(2 * math.pi))

    started = time.perf_counter()
    value, quadrature_error = quad(f, -cutoff, cutoff, epsabs=1e-9, epsrel=1e-10, limit=200)
    seconds = time.perf_counter() - started
    # Outer payoff <= continuation <= S(t1); analytic lognormal first-moment tail.
    tail_bound = s0 * (ndtr(sigma * math.sqrt(t1) - cutoff)
                       + ndtr(-cutoff - sigma * math.sqrt(t1)))
    return dict(k_outer=k_outer, sigma=sigma, price=value,
                quadrature_error_estimate=quadrature_error,
                analytic_omitted_tail_bound=tail_bound,
                function_evaluations=evaluations, seconds=seconds)


def main():
    # Literal Algorithm 6, arXiv:2602.08120v1, p10: no special base level printed.
    # Exact terminal mean = 1 and g(z)=z. Every displayed difference is 1-1.
    literal = sum(1.0 - 1.0 for _ in range(17))
    corrected = 1.0 + sum(1.0 - 1.0 for _ in range(16))
    eta = 1e-4  # Illustrative $0.01 / $100 payoff normalization.
    result = {
        "scope": "Classical simplification and literal-pseudocode diagnostics; no advantage benchmark",
        "scipy_version": scipy.__version__,
        "compound_black_scholes": [compound(k, s) for k in [2.0, 5.0, 10.0] for s in [0.15, 0.3, 0.6]],
        "repeated_v1_literal_base_diagnostic": {
            "exact_target": 1.0, "literal_displayed_telescoping_sum": literal,
            "with_explicit_base_term": corrected,
            "interpretation": "Apparent missing base-level convention in accessible v1; not a disproof of intended theorem; final ICML PDF inaccessible"
        },
        "illustrative_quantum_oracle_budget_seconds": {
            str(classical_seconds): classical_seconds * eta / 10
            for classical_seconds in [0.01, 1.0, 100.0]
        },
        "crossover_assumptions": "Hypothetical Q=1/eta calls, zero setup, 10x speedup; ignores nonlinear logarithms, confidence amplification, and variance constants; sensitivity calculation, not measured quantum cost."
    }
    out = Path(__file__).with_name("nonlinear_diagnostics.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
