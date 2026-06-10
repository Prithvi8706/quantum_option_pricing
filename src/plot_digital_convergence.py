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

# ── Section E: Classical convergence sweep ─────────────────────────────────────
methods  = ["Naive MC", "Antithetic MC", "RQMC"]
colors   = {"Naive MC": "#1f77b4", "Antithetic MC": "#2ca02c", "RQMC": "#9467bd"}
markers  = {"Naive MC": "o", "Antithetic MC": "s", "RQMC": "D"}

log_N    = np.log10(N_VALUES)
boot_rng = np.random.default_rng(0)   # fixed -> reproducible CIs

central = {m: None for m in methods}
ci_lo   = {m: None for m in methods}
ci_hi   = {m: None for m in methods}

errs = {m: np.zeros((N_TRIALS, len(N_VALUES))) for m in methods}

print(f"=== Section E: Classical sweep ({N_TRIALS} trials, {N_REP} reps, {N_BOOT} bootstrap) ===\n")

for j, N in enumerate(N_VALUES):
    for t in range(N_TRIALS):
        p_naive, _ = digital_mc(
            S0, K, r, sigma, T, N, seed=t)
        p_anti,  _ = digital_antithetic_mc(
            S0, K, r, sigma, T, N, seed=t)
        p_rqmc,  _ = digital_rqmc(
            S0, K, r, sigma, T, N, n_replications=N_REP, seed=t * 1000)
        errs["Naive MC"][t, j]      = abs(p_naive - ref)
        errs["Antithetic MC"][t, j] = abs(p_anti  - ref)
        errs["RQMC"][t, j]          = abs(p_rqmc  - ref)

for m in methods:
    mean_curve = errs[m].mean(axis=0)
    c = np.polyfit(log_N, np.log10(mean_curve), 1)[0]
    boot = np.empty(N_BOOT)
    for b in range(N_BOOT):
        idx     = boot_rng.integers(0, N_TRIALS, N_TRIALS)
        mc_b    = errs[m][idx].mean(axis=0)
        boot[b] = np.polyfit(log_N, np.log10(mc_b), 1)[0]
    lo, hi        = np.percentile(boot, CI_PERCENTILE)
    central[m]    = c
    ci_lo[m]      = lo
    ci_hi[m]      = hi
    atm_note      = "  * ATM symmetry watch-item" if m == "Antithetic MC" else ""
    print(f"  {m:<18}: slope = {c:+.3f}  95% CI [{lo:+.3f}, {hi:+.3f}]{atm_note}")

print()

# ── Section F: QAE epsilon sweep ───────────────────────────────────────────────
print(f"=== Section F: QAE epsilon sweep (n={QAE_N_QUBITS}) ===\n")
print(f"  (grid_true_price = {grid_true_price:.6f}  grid_bias = {grid_bias_n5:.2e})\n")

qae_results = []
for eps in QAE_EPSILONS:
    price_q, ci_q, elapsed_q, M = quantum_digital_call(
        S0, K, r, sigma, T, QAE_N_QUBITS, epsilon=eps, alpha=QAE_ALPHA
    )
    err_grid  = abs(price_q - grid_true_price)
    err_exact = abs(price_q - ref)
    qae_results.append((M, err_grid))
    print(f"  eps={eps:.3f}  M={M:>5}  qae={price_q:.6f}  "
          f"err_grid={err_grid:.2e}  err_exact={err_exact:.2e}  ({elapsed_q:.1f}s)")

qae_M, qae_err = zip(*sorted(qae_results))
print()

# ── Section G: Printed table ───────────────────────────────────────────────────
print("--- Digital Convergence Slopes (paste into paper) ---")
print(f"Note: N in [256, 65536]; NOT cross-comparable to Tables IV/V (Asian, N in [1024, 16384])")
print(f"Note: Antithetic MC slope may be inflated by ATM symmetry -- see text.\n")
print(f"{'Method':<20} | {'Slope (95% CI)':<24}")
print("-" * 48)
for m in methods:
    atm = "  *" if m == "Antithetic MC" else ""
    print(f"  {m:<18}  {central[m]:+.3f} [{ci_lo[m]:+.3f}, {ci_hi[m]:+.3f}]{atm}")

print(f"\nQAE (IQAE, n={QAE_N_QUBITS}) oracle queries M vs |err vs grid_true_price|:")
for M, err in zip(qae_M, qae_err):
    print(f"  M={M:>5}  err={err:.2e}")
print(f"\nQAE grid bias (n={QAE_N_QUBITS}): {grid_bias_n5:.2e}  (systematic offset vs continuous exact)")

# ── Figure ─────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))

for m in methods:
    mean_curve = errs[m].mean(axis=0)
    label = f"{m}  (slope {central[m]:+.2f} [{ci_lo[m]:+.2f},{ci_hi[m]:+.2f}])"
    ax.loglog(N_VALUES, mean_curve, color=colors[m], marker=markers[m],
              linewidth=2.0, markersize=6, label=label, zorder=3)

ax.scatter(qae_M, qae_err, color="#ff7f0e", marker="D", s=60, zorder=4,
           label=f"QAE IQAE n={QAE_N_QUBITS} (vs grid exact)")

# Reference lines anchored at naive MC first point
anchor_y = errs["Naive MC"].mean(axis=0)[0]
anchor_N = N_VALUES[0]
ref_N    = np.array([N_VALUES[0], N_VALUES[-1]], dtype=float)
ax.loglog(ref_N, anchor_y * (anchor_N / ref_N)**0.5, "k--", linewidth=1.2,
          alpha=0.55, label=r"$O(1/\sqrt{N})$ -- classical limit")
ax.loglog(ref_N, anchor_y * (anchor_N / ref_N)**1.0, "k:",  linewidth=1.2,
          alpha=0.55, label=r"$O(1/N)$ -- quantum-parity scaling")

ax.set_xlabel("Budget  (paths N for MC/RQMC;  oracle queries M for QAE)", fontsize=11)
ax.set_ylabel("Mean absolute error  |price - reference|", fontsize=11)
ax.set_title(
    "Digital Option Convergence: MC vs RQMC vs QAE  [cash-or-nothing call]\n"
    r"$\it{N\ range\ differs\ from\ Tables\ IV/V\ --\ slopes\ not\ cross-comparable}$",
    fontsize=11, pad=10)
ax.legend(fontsize=8.5, framealpha=0.9)
ax.grid(True, which="both", alpha=0.3)

plt.tight_layout()
out_path = os.path.join(os.path.dirname(__file__), "..", "figures",
                        "fig_digital_convergence.png")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
fig.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"\nSaved: {os.path.normpath(out_path)}")
plt.close(fig)
