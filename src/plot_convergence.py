import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import qmc, norm

sys.path.insert(0, os.path.dirname(__file__))
from black_scholes import black_scholes_call
from variance_reduced_mc import antithetic_mc, control_variate_mc

S0, K, r, sigma, T = 100.0, 100.0, 0.05, 0.2, 1.0
BS_PRICE = black_scholes_call(S0, K, r, sigma, T)

N_VALUES = [2**i for i in range(8, 18)]
N_TRIALS = 10
N_REP = 20


def _gbm_price(S0, K, r, sigma, T, Z):
    discount = np.exp(-r * T)
    S_T = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
    return discount * np.maximum(S_T - K, 0.0).mean()


def naive_price(S0, K, r, sigma, T, N, seed):
    rng = np.random.default_rng(seed)
    return _gbm_price(S0, K, r, sigma, T, rng.standard_normal(N))


def rqmc_price(S0, K, r, sigma, T, N, n_rep, trial_seed):
    n_per_rep = 2 ** int(np.ceil(np.log2(max(2, N / n_rep))))
    rep_prices = np.empty(n_rep)
    for i in range(n_rep):
        sampler = qmc.Sobol(d=1, scramble=True, seed=trial_seed * 100 + i)
        u = sampler.random(n_per_rep).flatten()
        rep_prices[i] = _gbm_price(S0, K, r, sigma, T, norm.ppf(u))
    return rep_prices.mean()


# --- collect errors ----------------------------------------------------------
methods = ["Naive MC", "Antithetic MC", "Control Variate", "RQMC (Sobol)"]
all_errors = {m: [] for m in methods}

for N in N_VALUES:
    trial_errs = {m: [] for m in methods}
    for t in range(N_TRIALS):
        p_naive = naive_price(S0, K, r, sigma, T, N, seed=t)
        p_anti, _ = antithetic_mc(S0, K, r, sigma, T, N, seed=t)
        p_cv, _ = control_variate_mc(S0, K, r, sigma, T, N, seed=t)
        p_rqmc = rqmc_price(S0, K, r, sigma, T, N, N_REP, trial_seed=t)
        for m, p in zip(methods, [p_naive, p_anti, p_cv, p_rqmc]):
            trial_errs[m].append(abs(p - BS_PRICE))
    for m in methods:
        all_errors[m].append(np.mean(trial_errs[m]))

N_arr = np.array(N_VALUES, dtype=float)

# --- fit slopes --------------------------------------------------------------
slopes = {}
for m in methods:
    err = np.array(all_errors[m])
    coeffs = np.polyfit(np.log10(N_arr), np.log10(err), 1)
    slopes[m] = coeffs[0]
    print(f"{m:<22}  empirical slope: {coeffs[0]:+.3f}")

# --- plot --------------------------------------------------------------------
plt.style.use("dark_background")
fig, ax = plt.subplots(figsize=(9, 6))

colors = ["#4fc3f7", "#81c784", "#ffb74d", "#ce93d8"]
markers = ["o", "s", "^", "D"]

for m, color, marker in zip(methods, colors, markers):
    err = np.array(all_errors[m])
    label = f"{m}  (slope {slopes[m]:+.2f})"
    ax.loglog(N_arr, err, color=color, marker=marker, linewidth=1.8,
              markersize=6, label=label)

# Reference lines anchored at naive MC first point
anchor_y = all_errors["Naive MC"][0]
anchor_N = N_VALUES[0]
ref_N = np.array([N_VALUES[0], N_VALUES[-1]], dtype=float)

y_half = anchor_y * (anchor_N / ref_N) ** 0.5
y_one = anchor_y * (anchor_N / ref_N) ** 1.0

ax.loglog(ref_N, y_half, "w--", linewidth=1.2, alpha=0.55,
          label=r"$O(1/\sqrt{N})$ — classical limit")
ax.loglog(ref_N, y_one,  "w:",  linewidth=1.2, alpha=0.55,
          label=r"$O(1/N)$ — QAE / RQMC scaling")

ax.set_xlabel("N  (paths per estimate)", fontsize=12)
ax.set_ylabel("Mean Absolute Error  |price − BS|", fontsize=12)
ax.set_title("Monte Carlo Convergence: Classical vs Quasi-Random", fontsize=13, pad=12)
ax.legend(fontsize=9, framealpha=0.3)
ax.grid(True, which="both", alpha=0.2)

out_path = os.path.join(os.path.dirname(__file__), "..", "figures", "fig_mc_convergence.png")
fig.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"\nSaved: {os.path.normpath(out_path)}")
plt.close(fig)
