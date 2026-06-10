import numpy as np
from scipy.stats import qmc, norm


def digital_mc(S0, K, r, sigma, T, N, seed=None):
    """Naive MC digital call. Payoff = (S_T > K).astype(float). Returns (price, std_err)."""
    rng = np.random.default_rng(seed)
    Z = rng.standard_normal(N)
    discount = np.exp(-r * T)
    S_T = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
    payoffs = (S_T > K).astype(float)
    price = discount * payoffs.mean()
    std_err = discount * payoffs.std(ddof=1) / np.sqrt(N)
    return price, std_err


def digital_antithetic_mc(S0, K, r, sigma, T, N, seed=None):
    """
    Antithetic pairs on binary payoff. N/2 antithetic pairs.
    std_err from paired-average std dev / sqrt(N/2). Returns (price, std_err).

    ATM watch-item: at S0=K, Z and -Z straddle the threshold symmetrically,
    suppressing variance by ~3x vs naive MC. This may produce an artificially
    steep slope specific to ATM symmetry rather than genuine convergence
    improvement. Antithetic slope should be interpreted cautiously and not
    generalised to non-ATM strikes.
    """
    rng = np.random.default_rng(seed)
    half = N // 2
    Z = rng.standard_normal(half)
    discount = np.exp(-r * T)
    drift = (r - 0.5 * sigma**2) * T
    vol = sigma * np.sqrt(T)
    S_pos = S0 * np.exp(drift + vol * Z)
    S_neg = S0 * np.exp(drift - vol * Z)
    paired_avg = 0.5 * ((S_pos > K).astype(float) + (S_neg > K).astype(float))
    price = discount * paired_avg.mean()
    std_err = discount * paired_avg.std(ddof=1) / np.sqrt(half)
    return price, std_err


def digital_rqmc(S0, K, r, sigma, T, N, n_replications=30, seed=None):
    """RQMC digital call. Scrambled Sobol d=1.
    std_err estimated from replication variance. Returns (price, std_err)."""
    m = 2 ** int(np.ceil(np.log2(max(2, N / n_replications))))
    discount = np.exp(-r * T)
    drift = (r - 0.5 * sigma**2) * T
    vol = sigma * np.sqrt(T)
    base = seed if seed is not None else 0
    rep_prices = np.empty(n_replications)
    for i in range(n_replications):
        sampler = qmc.Sobol(d=1, scramble=True, seed=base + i)
        u = sampler.random(m).flatten()
        Z = norm.ppf(u)
        S_T = S0 * np.exp(drift + vol * Z)
        rep_prices[i] = discount * (S_T > K).astype(float).mean()
    price = rep_prices.mean()
    std_err = rep_prices.std(ddof=1) / np.sqrt(n_replications)
    return price, std_err
