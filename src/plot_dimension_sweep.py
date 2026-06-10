"""
Dimension-decay sweep for Paper B, Table IV / Fig. 2.

Upgraded from the original (5 trials / 20 reps, single slope-of-mean) to:
  - 10 trials / 30 replications  (budget parity with Table III)
  - bootstrap 95% CI on the slope-of-mean  (honest uncertainty, referee-proof)
  - shaded confidence bands on the figure
  - white background (journal-standard, not dark/slide style)

Every number printed here is produced by the real estimators in asian_option.py.
Nothing is synthetic. Re-run and the numbers reproduce (seeds are fixed).
"""
import os
import sys
import warnings

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
from black_scholes import black_scholes_call
from asian_option import (
    geometric_asian_closed_form,
    asian_geometric_naive_mc,
    asian_geometric_antithetic_mc,
    asian_geometric_rqmc,
)

# Sobol at non-power-of-2 sample counts emits a balance warning; the estimator
# is still valid (we draw exact powers of 2 internally), so silence the noise.
warnings.filterwarnings("ignore", category=UserWarning)

S0, K, r, sigma, T = 100.0, 100.0, 0.05, 0.2, 1.0

# ── Validation: geometric closed form must match Black-Scholes at d=1 ──────
bs_price = black_scholes_call(S0, K, r, sigma, T)
geo_d1 = geometric_asian_closed_form(S0, K, r, sigma, T, d=1)
print("Validation: geometric_asian_closed_form(d=1) vs black_scholes_call()")
print(f"  Black-Scholes  : {bs_price:.6f}")
print(f"  Geometric (d=1): {geo_d1:.6f}")
print(f"  Difference     : {abs(geo_d1 - bs_price):.2e}")
assert abs(geo_d1 - bs_price) < 1e-10, "Closed-form / BS mismatch - check sigma_G formula"
print("  OK - match to machine precision\n")

# ── Sweep configuration ────────────────────────────────────────────────────
DIMS = [1, 2, 4, 8, 16, 32, 64]
# N capped at 2^14 = 16,384 (5 points) to match the arithmetic sweep window.
# At N=65536 the arithmetic CV reference SE (~1.8e-4) exceeds 10% of the RQMC
# error at low d (d=2,4,8), corrupting the slope fit there.  Both sweeps must
# use the same N-range for Table IV / Table V to be directly comparable.
N_VALUES = [2 ** i for i in range(10, 15)]   # 1024 -> 16384
N_TRIALS = 10        # was 5  -> parity with Table III (10 trials)
N_REP = 30           # was 20 -> matches main RQMC config (quasi_mc_rqmc)
N_BOOT = 2000        # bootstrap resamples for the slope CI
CI = (2.5, 97.5)     # 95% percentile interval

methods = ["Naive MC", "Antithetic MC", "RQMC"]
colors = {"Naive MC": "#1f77b4", "Antithetic MC": "#2ca02c", "RQMC": "#9467bd"}
markers = {"Naive MC": "o", "Antithetic MC": "s", "RQMC": "D"}

log_N = np.log10(N_VALUES)
boot_rng = np.random.default_rng(0)   # fixed -> reproducible CIs

# central slope + bootstrap CI, per method per dimension
central = {m: [] for m in methods}
ci_lo = {m: [] for m in methods}
ci_hi = {m: [] for m in methods}

print(f"Sweep: {N_TRIALS} trials, {N_REP} reps, {N_BOOT} bootstrap resamples")
print(f"{'d':>4} | {'Naive MC':>20} | {'Antithetic MC':>20} | {'RQMC':>20}")
print("-" * 74)

for d in DIMS:
    ref_price = geometric_asian_closed_form(S0, K, r, sigma, T, d)

    # per-trial absolute-error curves: errs[m] has shape (N_TRIALS, len(N_VALUES))
    errs = {m: np.zeros((N_TRIALS, len(N_VALUES))) for m in methods}
    for j, N in enumerate(N_VALUES):
        for t in range(N_TRIALS):
            p_naive, _ = asian_geometric_naive_mc(S0, K, r, sigma, T, N, d, seed=t)
            p_anti, _ = asian_geometric_antithetic_mc(S0, K, r, sigma, T, N, d, seed=t)
            p_rqmc, _ = asian_geometric_rqmc(
                S0, K, r, sigma, T, N, d, n_replications=N_REP, seed=t * 1000)
            errs["Naive MC"][t, j] = abs(p_naive - ref_price)
            errs["Antithetic MC"][t, j] = abs(p_anti - ref_price)
            errs["RQMC"][t, j] = abs(p_rqmc - ref_price)

    row = []
    for m in methods:
        mean_curve = errs[m].mean(axis=0)
        c = np.polyfit(log_N, np.log10(mean_curve), 1)[0]

        # bootstrap over trials: resample trial indices, refit slope of mean curve
        boot = np.empty(N_BOOT)
        for b in range(N_BOOT):
            idx = boot_rng.integers(0, N_TRIALS, N_TRIALS)
            mc = errs[m][idx].mean(axis=0)
            boot[b] = np.polyfit(log_N, np.log10(mc), 1)[0]
        lo, hi = np.percentile(boot, CI)

        central[m].append(c)
        ci_lo[m].append(lo)
        ci_hi[m].append(hi)
        row.append(f"{c:>6.3f} [{lo:>5.2f},{hi:>5.2f}]")

    print(f"{d:>4} | {row[0]:>20} | {row[1]:>20} | {row[2]:>20}")

# ── Markdown table for the paper (paste-ready) ─────────────────────────────
print("\n--- Table IV (paste into DOCX) ---")
print("| d | Naive MC | Antithetic | RQMC |")
print("|---|---|---|---|")
for i, d in enumerate(DIMS):
    def cell(m):
        return f"{central[m][i]:.2f} [{ci_lo[m][i]:.2f}, {ci_hi[m][i]:.2f}]"
    print(f"| {d} | {cell('Naive MC')} | {cell('Antithetic MC')} | {cell('RQMC')} |")

# ── Plot: central slope line + shaded 95% CI band, white background ────────
fig, ax = plt.subplots(figsize=(10, 6))

for m in methods:
    c = np.array(central[m])
    lo = np.array(ci_lo[m])
    hi = np.array(ci_hi[m])
    ax.plot(DIMS, c, color=colors[m], marker=markers[m],
            linewidth=2.0, markersize=6, label=m, zorder=3)
    ax.fill_between(DIMS, lo, hi, color=colors[m], alpha=0.18, zorder=1)

ax.axhline(-1.0, color="#555555", linestyle="--", linewidth=1.0,
           label=r"$O(1/N)$ - quantum-parity scaling")
ax.axhline(-0.5, color="#555555", linestyle=":", linewidth=1.0,
           label=r"$O(1/\sqrt{N})$ - classical limit")

ax.set_xscale("log", base=2)
ax.set_xticks(DIMS)
ax.set_xticklabels([str(d) for d in DIMS])
ax.set_xlabel("Problem dimension  d  (monitoring dates)", fontsize=12)
ax.set_ylabel("Fitted convergence slope (95% CI band)", fontsize=12)
ax.set_title(
    "RQMC Advantage Decays with Dimension  [geometric Asian, zero-noise reference]",
    fontsize=12, pad=12)
ax.legend(fontsize=9, loc="lower right", framealpha=0.9)
ax.grid(True, which="both", alpha=0.3)
ax.set_ylim(-1.3, -0.1)

plt.tight_layout()
out_path = os.path.join(os.path.dirname(__file__), "..", "figures",
                        "fig_rqmc_dimension_decay.png")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
fig.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"\nSaved: {os.path.normpath(out_path)}")
plt.close(fig)