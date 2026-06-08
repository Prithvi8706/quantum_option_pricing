import numpy as np
from scipy.stats import qmc, norm
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from black_scholes import black_scholes_call


def antithetic_mc(S0, K, r, sigma, T, N, seed=None):
    """Antithetic variates estimator using N/2 antithetic pairs (N total draws)."""
    rng = np.random.default_rng(seed)
    half = N // 2
    Z = rng.standard_normal(half)
    discount = np.exp(-r * T)
    drift = (r - 0.5 * sigma**2) * T
    vol = sigma * np.sqrt(T)

    S_pos = S0 * np.exp(drift + vol * Z)
    S_neg = S0 * np.exp(drift - vol * Z)

    paired_avg = 0.5 * (np.maximum(S_pos - K, 0.0) + np.maximum(S_neg - K, 0.0))
    price = discount * paired_avg.mean()
    std_err = discount * paired_avg.std(ddof=1) / np.sqrt(half)
    return price, std_err


def control_variate_mc(S0, K, r, sigma, T, N, seed=None):
    """Control variate estimator using terminal stock price S_T as control."""
    rng = np.random.default_rng(seed)
    Z = rng.standard_normal(N)
    discount = np.exp(-r * T)
    drift = (r - 0.5 * sigma**2) * T
    vol = sigma * np.sqrt(T)

    S_T = S0 * np.exp(drift + vol * Z)
    payoffs = np.maximum(S_T - K, 0.0)

    E_ST = S0 * np.exp(r * T)
    cov_matrix = np.cov(payoffs, S_T, ddof=1)
    c = -cov_matrix[0, 1] / cov_matrix[1, 1]

    corrected = payoffs + c * (S_T - E_ST)
    price = discount * corrected.mean()
    std_err = discount * corrected.std(ddof=1) / np.sqrt(N)
    return price, std_err


def quasi_mc(S0, K, r, sigma, T, N, seed=None):
    """Quasi-Monte Carlo estimator using a scrambled Sobol sequence."""
    N_pow2 = 2 ** int(np.ceil(np.log2(N)))
    if N_pow2 != N:
        print(f"[quasi_mc] N={N} rounded up to {N_pow2} (nearest power of 2 for Sobol)")

    sampler = qmc.Sobol(d=1, scramble=True, seed=seed)
    u = sampler.random(N_pow2).flatten()
    Z = norm.ppf(u)

    discount = np.exp(-r * T)
    drift = (r - 0.5 * sigma**2) * T
    vol = sigma * np.sqrt(T)

    S_T = S0 * np.exp(drift + vol * Z)
    payoffs = np.maximum(S_T - K, 0.0)

    price = discount * payoffs.mean()
    std_err = discount * payoffs.std(ddof=1) / np.sqrt(N_pow2)
    return price, std_err


def quasi_mc_rqmc(S0, K, r, sigma, T, N, n_replications=30, seed=42):
    """RQMC estimator: mean and statistically valid std_err from independent scrambled Sobol replications."""
    N_pow2 = 2 ** int(np.ceil(np.log2(N)))
    if N_pow2 != N:
        print(f"[quasi_mc_rqmc] N={N} rounded up to {N_pow2} (nearest power of 2 for Sobol)")

    discount = np.exp(-r * T)
    drift = (r - 0.5 * sigma**2) * T
    vol = sigma * np.sqrt(T)

    rep_prices = np.empty(n_replications)
    for i in range(n_replications):
        sampler = qmc.Sobol(d=1, scramble=True, seed=seed + i)
        u = sampler.random(N_pow2).flatten()
        Z = norm.ppf(u)
        S_T = S0 * np.exp(drift + vol * Z)
        payoffs = np.maximum(S_T - K, 0.0)
        rep_prices[i] = discount * payoffs.mean()

    price = rep_prices.mean()
    std_err = rep_prices.std(ddof=1) / np.sqrt(n_replications)
    return price, std_err


def compute_vrf(naive_var, reduced_var):
    """Variance reduction factor: naive_var / reduced_var."""
    return naive_var / reduced_var


def compare_all(S0=100, K=100, r=0.05, sigma=0.2, T=1.0, N=100_000, seed=42):
    from classical import monte_carlo_call

    bs_price = black_scholes_call(S0, K, r, sigma, T)
    print(f"Black-Scholes analytical price: {bs_price:.6f}\n")

    naive_price, naive_se = monte_carlo_call(S0, K, r, sigma, T, N)
    naive_var = naive_se**2 * N

    anti_price, anti_se = antithetic_mc(S0, K, r, sigma, T, N, seed=seed)
    anti_var = anti_se**2 * N

    cv_price, cv_se = control_variate_mc(S0, K, r, sigma, T, N, seed=seed)
    cv_var = cv_se**2 * N

    qmc_price, qmc_se = quasi_mc_rqmc(S0, K, r, sigma, T, N, seed=seed)
    qmc_var = qmc_se**2 * N  # use same N as naive for a fair VRF comparison (ratio of estimator variances)

    results = [
        ("Naive MC",          naive_price, naive_se, naive_var, 1.0),
        ("Antithetic MC",     anti_price,  anti_se,  anti_var,  compute_vrf(naive_var, anti_var)),
        ("Control Variate",   cv_price,    cv_se,    cv_var,    compute_vrf(naive_var, cv_var)),
        ("RQMC (Sobol)",      qmc_price,   qmc_se,   qmc_var,   compute_vrf(naive_var, qmc_var)),
    ]

    hdr = f"{'Method':<22} {'Price':>10} {'Std Err':>10} {'Variance':>12} {'VRF':>8} {'Err vs BS':>12}"
    print(hdr)
    print("-" * len(hdr))
    for method, price, se, var, vrf in results:
        print(
            f"{method:<22} {price:>10.6f} {se:>10.6f} {var:>12.4e} {vrf:>8.2f} {price - bs_price:>+12.6f}"
        )


if __name__ == "__main__":
    compare_all()
