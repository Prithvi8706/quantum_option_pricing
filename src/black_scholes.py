import numpy as np
from scipy.stats import norm


def black_scholes_call(S0: float, K: float, r: float, sigma: float, T: float) -> float:
    """
    Exact Black-Scholes price for a European call option.

    Parameters
    ----------
    S0    : Initial stock price
    K     : Strike price
    r     : Risk-free interest rate (annualised)
    sigma : Volatility (annualised)
    T     : Time to expiry (years)

    Returns
    -------
    price : float — Black-Scholes call price
    """
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    price = S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return price
