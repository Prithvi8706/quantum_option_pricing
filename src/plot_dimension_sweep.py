import numpy as np
import matplotlib.pyplot as plt
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from black_scholes import black_scholes_call
from asian_option import (
    geometric_asian_closed_form,
    asian_geometric_naive_mc,
    asian_geometric_antithetic_mc,
    asian_geometric_rqmc,
)

S0, K, r, sigma, T = 100.0, 100.0, 0.05, 0.2, 1.0

# ── Validation: geometric closed form must match Black-Scholes at d=1 ──────
bs_price  = black_scholes_call(S0, K, r, sigma, T)
geo_d1    = geometric_asian_closed_form(S0, K, r, sigma, T, d=1)
print("Validation: geometric_asian_closed_form(d=1) vs black_scholes_call()")
print(f"  Black-Scholes  : {bs_price:.6f}")
print(f"  Geometric (d=1): {geo_d1:.6f}")
print(f"  Difference     : {abs(geo_d1 - bs_price):.2e}")
assert abs(geo_d1 - bs_price) < 1e-10, "Closed-form / BS mismatch — check sigma_G formula"
print("  OK — match to machine precision\n")

# ── Sweep configuration ────────────────────────────────────────────────────
DIMS     = [1, 2, 4, 8, 16, 32, 64]
N_VALUES = [2**i for i in range(10, 17)]   # 1024 → 65536
N_TRIALS = 5
N_REP    = 20

methods = ["Naive MC", "Antithetic MC", "RQMC"]
colors  = {"Naive MC": "#4fc3f7", "Antithetic MC": "#81c784", "RQMC": "#ce93d8"}
markers = {"Naive MC": "o",       "Antithetic MC": "s",       "RQMC": "D"}

slopes_all = {m: [] for m in methods}

print(f"{'d':>4} | {'Naive slope':>12} | {'Antithetic slope':>16} | {'RQMC slope':>11}")
print("-" * 52)

for d in DIMS:
    # Zero-noise-floor reference: exact closed form for every d
    ref_price = geometric_asian_closed_form(S0, K, r, sigma, T, d)

    d_mean_errors = {m: [] for m in methods}

    for N in N_VALUES:
        trial_errs = {m: [] for m in methods}
        for t in range(N_TRIALS):
            p_naive, _ = asian_geometric_naive_mc(
                S0, K, r, sigma, T, N, d, seed=t)
            p_anti,  _ = asian_geometric_antithetic_mc(
                S0, K, r, sigma, T, N, d, seed=t)
            p_rqmc,  _ = asian_geometric_rqmc(
                S0, K, r, sigma, T, N, d, n_replications=N_REP, seed=t * 1000)

            trial_errs["Naive MC"].append(abs(p_naive - ref_price))
            trial_errs["Antithetic MC"].append(abs(p_anti  - ref_price))
            trial_errs["RQMC"].append(abs(p_rqmc  - ref_price))

        for m in methods:
            d_mean_errors[m].append(np.mean(trial_errs[m]))

    # Fit log-log slope
    log_N   = np.log10(N_VALUES)
    d_slopes = {}
    for m in methods:
        log_err      = np.log10(np.array(d_mean_errors[m]))
        d_slopes[m]  = np.polyfit(log_N, log_err, 1)[0]
        slopes_all[m].append(d_slopes[m])

    print(f"{d:>4} | {d_slopes['Naive MC']:>12.3f} | "
          f"{d_slopes['Antithetic MC']:>16.3f} | {d_slopes['RQMC']:>11.3f}")

# ── Plot ───────────────────────────────────────────────────────────────────
plt.style.use("dark_background")
fig, ax = plt.subplots(figsize=(12, 7))

for m in methods:
    ax.plot(DIMS, slopes_all[m], color=colors[m], marker=markers[m],
            linewidth=2.2, markersize=7, label=m)

ax.axhline(-1.0, color="white", linestyle="--", linewidth=1.0, alpha=0.5,
           label=r"$O(1/N)$ — quantum-parity scaling")
ax.axhline(-0.5, color="white", linestyle=":",  linewidth=1.0, alpha=0.5,
           label=r"$O(1/\sqrt{N})$ — classical limit")
ax.axhline(-0.75, color="gold", linestyle="-.", linewidth=0.8, alpha=0.35)

# Find where RQMC slope first crosses below −0.75 (interpolate on log2 scale)
rqmc_slopes  = slopes_all["RQMC"]
crossover_d  = DIMS[-1]
crossover_s  = rqmc_slopes[-1]
for i in range(len(DIMS) - 1):
    if rqmc_slopes[i] >= -0.75 > rqmc_slopes[i + 1]:
        ld0, ld1 = np.log2(DIMS[i]), np.log2(DIMS[i + 1])
        s0,  s1  = rqmc_slopes[i],   rqmc_slopes[i + 1]
        log_cross = ld0 + (ld1 - ld0) * (-0.75 - s0) / (s1 - s0)
        crossover_d = 2 ** log_cross
        crossover_s = -0.75
        break

text_d = min(crossover_d * 2.0, DIMS[-2])
text_s = crossover_s + 0.16
ax.annotate(
    "Above this dimension, classical RQMC\n"
    "loses its quantum-parity edge —\n"
    "the regime where QAE may still win",
    xy=(crossover_d, -0.75),
    xytext=(text_d, text_s),
    fontsize=9, color="gold", alpha=0.9,
    arrowprops=dict(arrowstyle="->", color="gold", alpha=0.6),
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#1a1a1a", alpha=0.85),
)

ax.set_xscale("log", base=2)
ax.set_xticks(DIMS)
ax.set_xticklabels([str(d) for d in DIMS])
ax.set_xlabel("Problem dimension  d  (monitoring dates)", fontsize=12)
ax.set_ylabel("Fitted convergence slope", fontsize=12)
ax.set_title("RQMC Advantage Decays with Dimension  [geometric Asian, zero-noise reference]",
             fontsize=12, pad=12)
ax.legend(fontsize=10, framealpha=0.3, loc="lower right")
ax.grid(True, which="both", alpha=0.2)
ax.set_ylim(-1.3, -0.2)

plt.tight_layout()
out_path = os.path.join(os.path.dirname(__file__), "..", "figures",
                        "fig_rqmc_dimension_decay.png")
fig.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"\nSaved: {os.path.normpath(out_path)}")
plt.close(fig)
