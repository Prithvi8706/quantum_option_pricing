"""
European digital option convergence experiment — Paper B, Section VII.

MC / Antithetic MC / RQMC (Sobol) / QAE (IQAE) on a cash-or-nothing call.
Tests whether QAE's quadratic advantage survives a discontinuous payoff.

Sections:
  A  — Exact reference + MC sanity check
  D  — QAE discretization validation gate (mandatory; must pass before sweep)
  E  — Classical convergence sweep  [added in Task 5]
  F  — QAE epsilon sweep            [added in Task 5]
  G  — Printed table + figure       [added in Task 5]

Scientific question: does RQMC's empirical slope degrade from ~-1.0 toward
-0.5 on the discontinuous digital payoff? Three possible outcomes are tested
with equal weight — see spec for details.

Cross-comparability note: N ∈ [256, 65536] here. Slopes are NOT cross-
comparable to Tables IV/V (Asian, N ∈ [1024, 16384]).
"""
import os
import sys
import warnings

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm as _scipy_norm

sys.path.insert(0, os.path.dirname(__file__))
from black_scholes import digital_bs_price
from digital_option import digital_mc, digital_antithetic_mc, digital_rqmc
from quantum import _build_digital_circuit, quantum_digital_call

warnings.filterwarnings("ignore", category=UserWarning)

# ── Parameters ─────────────────────────────────────────────────────────────────
S0, K, r, sigma, T = 100.0, 100.0, 0.05, 0.2, 1.0

N_VALUES      = [2**i for i in range(8, 17)]    # 256 → 65536 (9 points)
N_TRIALS      = 10
N_REP         = 30
N_BOOT        = 2000
CI_PERCENTILE = (2.5, 97.5)
N_SANITY      = 1_000_000

QAE_N_QUBITS  = 5
QAE_EPSILONS  = [0.001, 0.002, 0.004, 0.007, 0.010, 0.015, 0.020]
QAE_ALPHA     = 0.05

# Bounds (same logic as _build_digital_circuit, sigma ≥ 0.15 guaranteed here)
sigma_c   = max(sigma, 0.15)
mu_ln     = (r - 0.5 * sigma_c**2) * T + np.log(S0)
sigma_var = (sigma_c * np.sqrt(T))**2
mean_s    = np.exp(mu_ln + 0.5 * sigma_var)
var_s     = (np.exp(sigma_var) - 1) * np.exp(2 * mu_ln + sigma_var)
std_s     = np.sqrt(var_s)
low       = max(0.0, min(mean_s - 3 * std_s, K * 0.98))
high      = max(mean_s + 3 * std_s, K * 1.02)

# ── Section A: Exact reference + MC sanity check ───────────────────────────────
print("=== Section A: Reference and MC sanity check ===\n")

ref = digital_bs_price(S0, K, r, sigma, T)
print(f"Exact digital BS price: {ref:.6f}  (e^{{-rT}}*N(d2))\n")

mc_price, mc_se = digital_mc(S0, K, r, sigma, T, N_SANITY, seed=0)
err_mc = abs(mc_price - ref)
assert err_mc < 5 * mc_se, (
    f"MC sanity FAILED: |mc - exact| = {err_mc:.2e} >= 5*se = {5*mc_se:.2e}"
)
print(f"MC sanity (N={N_SANITY:,}): |mc - exact| = {err_mc:.2e}   5*se = {5*mc_se:.2e}   PASS\n")

# ── Section D: QAE discretization validation gate (mandatory) ─────────────────
print("=== Section D: QAE discretization validation ===\n")

from qiskit_finance.circuit.library import LogNormalDistribution
from qiskit.quantum_info import Statevector

# D1 — Grid bias shrinks with n + normalization guard
print("  D1: Grid bias vs number of uncertainty qubits")
biases = {}
for n in [3, 4, 5]:
    lnd = LogNormalDistribution(n, mu=mu_ln, sigma=sigma_var, bounds=(low, high))
    x_grid     = np.array(lnd._values)
    grid_probs = np.array(lnd._probabilities)
    assert np.isclose(grid_probs.sum(), 1.0), (
        f"n={n}: lnd._probabilities sums to {grid_probs.sum():.8f}, not 1.0 — "
        "LogNormalDistribution internals may have changed"
    )
    grid_p     = np.dot(grid_probs, (x_grid > K).astype(float))
    grid_price = np.exp(-r * T) * grid_p
    bias       = abs(grid_price - ref)
    biases[n]  = bias
    print(f"    n={n}: grid_price={grid_price:.6f}  exact={ref:.6f}  bias={bias:.2e}")

assert biases[4] < biases[3], "ABORT — bias(n=4) >= bias(n=3); check bounds/LogNormal params"
assert biases[5] < biases[4], "ABORT — bias(n=5) >= bias(n=4); check bounds/LogNormal params"
print("  D1 PASS: grid bias monotone-decreasing with n\n")

# D2 — Step encoding correctness (load-bearing)
print("  D2: Step encoding -- sv P(obj=|1>) vs classical grid_p at n=3")
n_check = 3
full_circ_chk, _ = _build_digital_circuit(S0, K, r, sigma, T, n_check)
sv_probs_chk = np.abs(np.array(Statevector(full_circ_chk)))**2
prob_obj1_chk = sum(sv_probs_chk[i] for i in range(len(sv_probs_chk)) if (i >> n_check) & 1)

lnd_chk   = LogNormalDistribution(n_check, mu=mu_ln, sigma=sigma_var, bounds=(low, high))
grid_p_chk = np.dot(lnd_chk._probabilities, (np.array(lnd_chk._values) > K).astype(float))

assert abs(prob_obj1_chk - grid_p_chk) < 1e-6, (
    f"Step encoding MISMATCH: sv P(obj=1)={prob_obj1_chk:.6f}  grid_p={grid_p_chk:.6f}\n"
    "  LinearAmplitudeFunction image=(0,1) may be silently renormalized — stop."
)
print(f"  D2 PASS: sv P(obj=1) = {prob_obj1_chk:.6f}  grid_p = {grid_p_chk:.6f}  diff < 1e-6\n")

# D3 — Compute grid_true_price for n=5 (used as QAE convergence reference in Section F)
lnd5       = LogNormalDistribution(QAE_N_QUBITS, mu=mu_ln, sigma=sigma_var, bounds=(low, high))
grid_probs5 = np.array(lnd5._probabilities)
assert np.isclose(grid_probs5.sum(), 1.0), "n=5 normalization assert failed"
grid_p5    = np.dot(grid_probs5, (np.array(lnd5._values) > K).astype(float))
grid_true_price = np.exp(-r * T) * grid_p5
grid_bias_n5 = abs(grid_true_price - ref)
print(f"  D3: n=5 grid_true_price = {grid_true_price:.6f}")
print(f"       exact BS price      = {ref:.6f}")
print(f"       grid bias (n=5)     = {grid_bias_n5:.2e}  (fixed systematic offset)")
print(f"\n  All Section D checks passed.\n")

# ── Sections E, F, G: added in Task 5 ─────────────────────────────────────────
print("Sections E, F, G not yet implemented.")
