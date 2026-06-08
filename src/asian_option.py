import numpy as np
from scipy.stats import qmc, norm


def simulate_paths(S0, r, sigma, T, Z):
    """GBM price paths over d equal time steps given standard-normal shocks Z (n_paths, d)."""
    n_paths, d = Z.shape
    dt = T / d
    drift = (r - 0.5 * sigma**2) * dt
    diffusion = sigma * np.sqrt(dt)
    log_increments = drift + diffusion * Z          # (n_paths, d)
    log_paths = np.cumsum(log_increments, axis=1)   # cumulative log-return
    S_paths = S0 * np.exp(log_paths)                # (n_paths, d) price at each date
    return S_paths


def _asian_payoff(S_paths, K, r, T):
    """Discounted arithmetic-average Asian call payoff."""
    discount = np.exp(-r * T)
    payoffs = np.maximum(S_paths.mean(axis=1) - K, 0.0)
    return discount, payoffs


def asian_naive_mc(S0, K, r, sigma, T, N, d, seed=None):
    rng = np.random.default_rng(seed)
    Z = rng.standard_normal((N, d))
    S_paths = simulate_paths(S0, r, sigma, T, Z)
    discount, payoffs = _asian_payoff(S_paths, K, r, T)
    price = discount * payoffs.mean()
    std_err = discount * payoffs.std(ddof=1) / np.sqrt(N)
    return price, std_err


def asian_antithetic_mc(S0, K, r, sigma, T, N, d, seed=None):
    rng = np.random.default_rng(seed)
    half = N // 2
    Z = rng.standard_normal((half, d))
    S_pos = simulate_paths(S0, r, sigma, T,  Z)
    S_neg = simulate_paths(S0, r, sigma, T, -Z)
    discount = np.exp(-r * T)
    pay_pos = np.maximum(S_pos.mean(axis=1) - K, 0.0)
    pay_neg = np.maximum(S_neg.mean(axis=1) - K, 0.0)
    paired_avg = 0.5 * (pay_pos + pay_neg)
    price = discount * paired_avg.mean()
    std_err = discount * paired_avg.std(ddof=1) / np.sqrt(half)
    return price, std_err


def asian_rqmc(S0, K, r, sigma, T, N, d, n_replications=20, seed=None):
    """
    RQMC estimator using independent scrambled Sobol replications.
    Each replication draws m = ceil_pow2(N / n_replications) points in d dimensions.
    std_err is estimated across replication means (statistically valid for QMC).
    """
    m = 2 ** int(np.ceil(np.log2(max(2, N / n_replications))))
    discount = np.exp(-r * T)
    base = seed if seed is not None else 0
    rep_prices = np.empty(n_replications)
    for i in range(n_replications):
        sampler = qmc.Sobol(d=d, scramble=True, seed=base + i)
        u = sampler.random(m)           # (m, d) uniform in [0, 1)
        Z = norm.ppf(u)                 # (m, d) standard normals
        S_paths = simulate_paths(S0, r, sigma, T, Z)
        payoffs = np.maximum(S_paths.mean(axis=1) - K, 0.0)
        rep_prices[i] = discount * payoffs.mean()
    price = rep_prices.mean()
    std_err = rep_prices.std(ddof=1) / np.sqrt(n_replications)
    return price, std_err


def asian_control_variate(S0, K, r, sigma, T, N, d, seed=None):
    """
    Control variate: terminal stock price S_T = S_paths[:, -1].
    E[S_T] = S0 * exp(r * T) under the risk-neutral measure (exact).
    Chosen over geometric-average closed form for simplicity; works for any d.
    """
    rng = np.random.default_rng(seed)
    Z = rng.standard_normal((N, d))
    S_paths = simulate_paths(S0, r, sigma, T, Z)
    discount, payoffs = _asian_payoff(S_paths, K, r, T)
    S_T = S_paths[:, -1]
    E_ST = S0 * np.exp(r * T)
    cov_matrix = np.cov(payoffs, S_T, ddof=1)
    c = -cov_matrix[0, 1] / cov_matrix[1, 1]
    corrected = payoffs + c * (S_T - E_ST)
    price = discount * corrected.mean()
    std_err = discount * corrected.std(ddof=1) / np.sqrt(N)
    return price, std_err


# ── Geometric Asian helpers ────────────────────────────────────────────────

def _cumlog(r, sigma, T, Z):
    """Cumulative log-returns relative to S0 (no S0 factor): S = S0 * exp(result)."""
    dt = T / Z.shape[1]
    return np.cumsum((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z, axis=1)


def geometric_asian_closed_form(S0, K, r, sigma, T, d):
    """
    Exact price for a geometric-average Asian call with d equal monitoring dates.

    Uses the correct sigma_G = sigma*sqrt((d+1)(2d+1)/(6d^2)), which reduces to
    sigma at d=1 so the formula matches Black-Scholes exactly for a European call.

    Reference: Kemna & Vorst (1990), corrected for discrete monitoring.
    """
    sigma_G = sigma * np.sqrt((d + 1) * (2 * d + 1) / (6 * d**2))
    mu_G    = (r - 0.5 * sigma**2) * (d + 1) / (2 * d) + 0.5 * sigma_G**2
    vol_T   = sigma_G * np.sqrt(T)
    d1 = (np.log(S0 / K) + (mu_G + 0.5 * sigma_G**2) * T) / vol_T
    d2 = d1 - vol_T
    return S0 * np.exp((mu_G - r) * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)


def asian_geometric_naive_mc(S0, K, r, sigma, T, N, d, seed=None):
    rng = np.random.default_rng(seed)
    Z   = rng.standard_normal((N, d))
    lp  = _cumlog(r, sigma, T, Z)
    discount = np.exp(-r * T)
    G        = S0 * np.exp(lp.mean(axis=1))
    payoffs  = np.maximum(G - K, 0.0)
    price    = discount * payoffs.mean()
    std_err  = discount * payoffs.std(ddof=1) / np.sqrt(N)
    return price, std_err


def asian_geometric_antithetic_mc(S0, K, r, sigma, T, N, d, seed=None):
    rng  = np.random.default_rng(seed)
    half = N // 2
    Z    = rng.standard_normal((half, d))
    discount = np.exp(-r * T)
    for sign in (1, -1):
        lp = _cumlog(r, sigma, T, sign * Z)
        G  = S0 * np.exp(lp.mean(axis=1))
        pay = np.maximum(G - K, 0.0)
        if sign == 1:
            pay_pos = pay
        else:
            pay_neg = pay
    paired_avg = 0.5 * (pay_pos + pay_neg)
    price   = discount * paired_avg.mean()
    std_err = discount * paired_avg.std(ddof=1) / np.sqrt(half)
    return price, std_err


def asian_geometric_rqmc(S0, K, r, sigma, T, N, d, n_replications=20, seed=None):
    """RQMC geometric Asian: scrambled Sobol replications, std_err from replication variance."""
    m        = 2 ** int(np.ceil(np.log2(max(2, N / n_replications))))
    discount = np.exp(-r * T)
    base     = seed if seed is not None else 0
    rep_prices = np.empty(n_replications)
    for i in range(n_replications):
        sampler = qmc.Sobol(d=d, scramble=True, seed=base + i)
        u  = sampler.random(m)
        Z  = norm.ppf(u)
        lp = _cumlog(r, sigma, T, Z)
        G  = S0 * np.exp(lp.mean(axis=1))
        rep_prices[i] = discount * np.maximum(G - K, 0.0).mean()
    return rep_prices.mean(), rep_prices.std(ddof=1) / np.sqrt(n_replications)


if __name__ == "__main__":
    S0, K, r, sigma, T = 100.0, 100.0, 0.05, 0.2, 1.0
    d, N = 4, 100_000
    print(f"Sanity check: d={d}, N={N:,}, S0={S0}, K={K}, r={r}, sigma={sigma}, T={T}\n")
    runs = [
        ("Naive MC",       asian_naive_mc,        {}),
        ("Antithetic MC",  asian_antithetic_mc,   {}),
        ("RQMC",           asian_rqmc,            {"n_replications": 20}),
        ("Control Variate",asian_control_variate, {}),
    ]
    for name, fn, kw in runs:
        price, se = fn(S0, K, r, sigma, T, N, d, seed=42, **kw)
        print(f"  {name:<18}  price={price:.5f}   std_err={se:.6f}")
