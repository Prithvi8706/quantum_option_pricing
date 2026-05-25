import numpy as np


def monte_carlo_call(S0: float, K: float, r: float, sigma: float, T: float, N: int):
    """
    Price a European call option via Monte Carlo simulation using geometric Brownian motion.

    Parameters
    ----------
    S0    : Initial stock price
    K     : Strike price
    r     : Risk-free interest rate (annualised)
    sigma : Volatility (annualised)
    T     : Time to expiry (years)
    N     : Number of simulation paths

    Returns
    -------
    price : float  — discounted expected payoff
    std_err : float — standard error of the estimate
    """
    rng = np.random.default_rng()
    Z = rng.standard_normal(N)
    S_T = S0 * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * Z)
    payoffs = np.maximum(S_T - K, 0.0)
    discount = np.exp(-r * T)
    price = discount * payoffs.mean()
    std_err = discount * payoffs.std() / np.sqrt(N)
    return price, std_err
