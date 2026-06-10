"""
Dimension-decay sweep for Paper B, Section VI-B / Table V / Fig. 3.

Arithmetic-average Asian call, geometric control-variate reference.

Direct mirror of plot_dimension_sweep.py (geometric). Same harness, same config
(10 trials / 30 reps / 2000 bootstrap resamples), same figure style. Differences:
  - payoff: arithmetic average (non-smooth, no closed form)
  - reference: geometric_asian_closed_form + MC[arith - geo] at N=2^22
  - output: Table V, fig_arithmetic_asian_decay.png

Scientific question (Section VI-B): does RQMC's O(1/N)-ish edge survive on
the non-smooth arithmetic payoff, or degrade relative to the geometric case?
"""
import os
import sys
import warnings

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
from black_scholes import black_scholes_call
from asian_option import (
    simulate_paths,
    geometric_asian_closed_form,
    arithmetic_asian_cv_ref,
    asian_geometric_rqmc,
    asian_naive_mc,
    asian_antithetic_mc,
    asian_rqmc,
)

warnings.filterwarnings("ignore", category=UserWarning)

S0, K, r, sigma, T = 100.0, 100.0, 0.05, 0.2, 1.0

# ── Config (parity with plot_dimension_sweep.py) ───────────────────────────────
N_REF    = 8_388_608            # 2^23 — reference MC budget; 2^22 left ratio=0.12 at d=2/N=16384
REF_SEED = 999                  # fixed → reproducible reference
DIMS     = [1, 2, 4, 8, 16, 32, 64]
# N capped at 2^14 = 16,384 (5 points) because above this threshold the
# arithmetic CV reference SE (~1.8e-4) exceeds 10% of the RQMC error at
# low d (d=2,4,8), corrupting the slope fit.  plot_dimension_sweep.py uses
# the identical window so Tables IV and V remain directly comparable.
N_VALUES = [2 ** i for i in range(10, 15)]   # 1024 → 16384
N_TRIALS = 10
N_REP    = 30
N_BOOT   = 2000
CI       = (2.5, 97.5)
log_N    = np.log10(N_VALUES)
boot_rng = np.random.default_rng(0)

# 5-point-window Table IV bootstrap CIs for the RQMC geometric slope (spot-check).
# Updated from the 7-point original after truncating N_VALUES to [2^10..2^14].
GEO_RQMC_CI = {1: (-1.13, -0.77), 64: (-0.89, -0.47)}

# ── Section A: Geometric sanity check ─────────────────────────────────────────
print("=== Section A: Geometric sanity check ===\n")

# A1: geometric mean equivalence
Z_chk          = np.random.default_rng(42).standard_normal((1000, 4))
S_chk          = simulate_paths(S0, r, sigma, T, Z_chk)
dt             = T / 4
cumlog_chk     = np.cumsum((r - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*Z_chk, axis=1)
geo_via_log    = np.exp(np.log(S_chk).mean(axis=1))
geo_via_cumlog = S0 * np.exp(cumlog_chk.mean(axis=1))
max_diff       = np.max(np.abs(geo_via_log - geo_via_cumlog))
assert max_diff < 1e-10, (
    f"Geometric mean methods disagree: max diff = {max_diff:.2e}"
)
print(f"  A1 geometric mean equivalence: max diff = {max_diff:.2e}  OK\n")

# A2: RQMC slope spot-check
print("  A2 geometric RQMC slope spot-check:")
for d_chk in [1, 64]:
    ref_geo  = geometric_asian_closed_form(S0, K, r, sigma, T, d_chk)
    errs_chk = np.zeros((N_TRIALS, len(N_VALUES)))
    for j, N in enumerate(N_VALUES):
        for t in range(N_TRIALS):
            p, _ = asian_geometric_rqmc(
                S0, K, r, sigma, T, N, d_chk, n_replications=N_REP, seed=t * 1000
            )
            errs_chk[t, j] = abs(p - ref_geo)
    slope_chk = np.polyfit(log_N, np.log10(errs_chk.mean(axis=0)), 1)[0]
    lo, hi    = GEO_RQMC_CI[d_chk]
    status    = "PASS" if lo <= slope_chk <= hi else "FAIL"
    print(f"    d={d_chk}: RQMC slope = {slope_chk:.3f}  CI=[{lo}, {hi}]  [{status}]")
    assert status == "PASS", (
        f"Harness bug: d={d_chk} RQMC slope {slope_chk:.3f} outside "
        f"published CI [{lo}, {hi}] — stop and investigate"
    )

print("\n  All Section A checks passed.\n")

# ── Section B: Build arithmetic CV references ──────────────────────────────────
print("=== Section B: Arithmetic CV references ===\n")
refs    = {}
ref_ses = {}
for d in DIMS:
    price, se  = arithmetic_asian_cv_ref(
        S0, K, r, sigma, T, d, N_ref=N_REF, seed=REF_SEED
    )
    refs[d]    = price
    ref_ses[d] = se

print("\n  Section B complete.\n")

# ── Section C: Arithmetic sweep ────────────────────────────────────────────────
methods = ["Naive MC", "Antithetic MC", "RQMC"]
colors  = {"Naive MC": "#1f77b4", "Antithetic MC": "#2ca02c", "RQMC": "#9467bd"}
markers = {"Naive MC": "o", "Antithetic MC": "s", "RQMC": "D"}

central          = {m: [] for m in methods}
ci_lo            = {m: [] for m in methods}
ci_hi            = {m: [] for m in methods}
rqmc_errs_by_dim = {}

print(f"=== Section C: Arithmetic sweep "
      f"({N_TRIALS} trials, {N_REP} reps, {N_BOOT} bootstrap) ===\n")
print(f"{'d':>4} | {'Naive MC':>20} | {'Antithetic MC':>20} | {'RQMC':>20}")
print("-" * 74)

for d in DIMS:
    errs = {m: np.zeros((N_TRIALS, len(N_VALUES))) for m in methods}
    for j, N in enumerate(N_VALUES):
        for t in range(N_TRIALS):
            p_naive, _ = asian_naive_mc(S0, K, r, sigma, T, N, d, seed=t)
            p_anti,  _ = asian_antithetic_mc(S0, K, r, sigma, T, N, d, seed=t)
            p_rqmc,  _ = asian_rqmc(
                S0, K, r, sigma, T, N, d, n_replications=N_REP, seed=t * 1000
            )
            errs["Naive MC"][t, j]      = abs(p_naive - refs[d])
            errs["Antithetic MC"][t, j] = abs(p_anti  - refs[d])
            errs["RQMC"][t, j]          = abs(p_rqmc  - refs[d])

    rqmc_errs_by_dim[d] = errs["RQMC"]   # saved for Section D noise-floor check

    row = []
    for m in methods:
        mean_curve = errs[m].mean(axis=0)
        c = np.polyfit(log_N, np.log10(mean_curve), 1)[0]
        boot = np.empty(N_BOOT)
        for b in range(N_BOOT):
            idx     = boot_rng.integers(0, N_TRIALS, N_TRIALS)
            mc      = errs[m][idx].mean(axis=0)
            boot[b] = np.polyfit(log_N, np.log10(mc), 1)[0]
        lo, hi = np.percentile(boot, CI)
        central[m].append(c)
        ci_lo[m].append(lo)
        ci_hi[m].append(hi)
        row.append(f"{c:>6.3f} [{lo:>5.2f},{hi:>5.2f}]")

    print(f"{d:>4} | {row[0]:>20} | {row[1]:>20} | {row[2]:>20}")

# ── Section D: Noise floor check ───────────────────────────────────────────────
print("\n=== Section D: Noise floor check ===\n")
print(f"{'d':>4}  {'ref_SE':>10}  {'rqmc_err':>14}  {'ratio':>8}  N       flag")
print("-" * 62)
for d in DIMS:
    se          = ref_ses[d]
    err_small   = rqmc_errs_by_dim[d].mean(axis=0)[0]     # N=N_VALUES[0]
    err_large   = rqmc_errs_by_dim[d].mean(axis=0)[-1]   # N=N_VALUES[-1]
    ratio_small = se / err_small
    ratio_large = se / err_large
    flag_small  = "  WARN: increase N_REF" if ratio_small >= 0.1 else "  ok"
    flag_large  = "  WARN: increase N_REF" if ratio_large >= 0.1 else "  ok"
    print(f"  {d:>4}  {se:>10.2e}  {err_small:>14.2e}  {ratio_small:>8.4f}  "
          f"N={N_VALUES[0]:<6}  {flag_small}")
    print(f"  {' ':>4}  {' ':>10}  {err_large:>14.2e}  {ratio_large:>8.4f}  "
          f"N={N_VALUES[-1]:<6}  {flag_large}")

# ── Table V ────────────────────────────────────────────────────────────────────
print("\n--- Table V (paste into DOCX) ---")
print("| d | Naive MC | Antithetic | RQMC |")
print("|---|---|---|---|")
for i, d in enumerate(DIMS):
    def cell(m, i=i):
        return f"{central[m][i]:.2f} [{ci_lo[m][i]:.2f}, {ci_hi[m][i]:.2f}]"
    print(f"| {d} | {cell('Naive MC')} | {cell('Antithetic MC')} | {cell('RQMC')} |")

# ── Figure ─────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))

for m in methods:
    c  = np.array(central[m])
    lo = np.array(ci_lo[m])
    hi = np.array(ci_hi[m])
    ax.plot(DIMS, c, color=colors[m], marker=markers[m],
            linewidth=2.0, markersize=6, label=m, zorder=3)
    ax.fill_between(DIMS, lo, hi, color=colors[m], alpha=0.18, zorder=1)

ax.axhline(-1.0, color="#555555", linestyle="--", linewidth=1.0,
           label=r"$O(1/N)$ — quantum-parity scaling")
ax.axhline(-0.5, color="#555555", linestyle=":", linewidth=1.0,
           label=r"$O(1/\sqrt{N})$ — classical limit")

ax.set_xscale("log", base=2)
ax.set_xticks(DIMS)
ax.set_xticklabels([str(d) for d in DIMS])
ax.set_xlabel("Problem dimension  d  (monitoring dates)", fontsize=12)
ax.set_ylabel("Fitted convergence slope (95% CI band)", fontsize=12)
ax.set_title(
    "RQMC Advantage Decays with Dimension  "
    "[arithmetic Asian, geometric CV reference]",
    fontsize=12, pad=12)
ax.legend(fontsize=9, loc="lower right", framealpha=0.9)
ax.grid(True, which="both", alpha=0.3)
ax.set_ylim(-1.3, -0.1)

plt.tight_layout()
out_path = os.path.join(os.path.dirname(__file__), "..", "figures",
                        "fig_arithmetic_asian_decay.png")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
fig.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"\nSaved: {os.path.normpath(out_path)}")
plt.close(fig)
