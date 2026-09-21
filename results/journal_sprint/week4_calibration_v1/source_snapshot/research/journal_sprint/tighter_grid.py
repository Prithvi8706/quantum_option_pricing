"""Cancellation-aware nearest-cell bound; no exact price references consulted."""

from dataclasses import replace
import math

import numpy as np
from scipy.stats import lognorm

from .pricing_bounds import bounds_for
from research.paper_a.references import grid_points


def density_derivative(x, mu, s):
    x = np.asarray(x)
    return -lognorm.pdf(x, s=s, scale=math.exp(mu)) / x * (1 + (np.log(x) - mu) / s**2)


def derivative_suprema(left, right, mu, s):
    """Max |f'| occurs at endpoints or roots of f'' for positive lognormal x."""
    left, right = np.asarray(left), np.asarray(right)
    maxima = np.maximum(abs(density_derivative(left, mu, s)), abs(density_derivative(right, mu, s)))
    for v in ((-3 - math.sqrt(1 + 4 / s**2)) / 2, (-3 + math.sqrt(1 + 4 / s**2)) / 2):
        root = math.exp(mu + s**2 * v)
        inside = (left <= root) & (root <= right)
        maxima = np.where(inside, np.maximum(maxima, abs(density_derivative(root, mu, s))), maxima)
    return maxima


def tighter_bounds_for(contract, n, scale, q_total=1e-5):
    old = bounds_for(contract, n, scale, q_total)
    c = contract
    s = c.sigma * math.sqrt(c.T)
    mu = math.log(c.S0) + (c.r - c.sigma**2 / 2) * c.T
    distribution = lognorm(s=s, scale=math.exp(mu))
    x = grid_points(old.lower, old.upper, n)
    edges = np.concatenate(([old.lower], (x[:-1] + x[1:]) / 2, [old.upper]))
    left, right = edges[:-1], edges[1:]
    retained = 1 - float(distribution.cdf(old.lower) + distribution.sf(old.upper))
    payoff = np.maximum(x - c.K, 0)
    # Integral of the payoff against constant density on a cell. This is NOT
    # integration against the true density and does not calculate a target price.
    integral_difference = (right - left) * payoff - (
        np.maximum(right - c.K, 0) ** 2 - np.maximum(left - c.K, 0) ** 2
    ) / 2
    constant_signed = float(np.dot(distribution.pdf(x), integral_difference))
    derivative = derivative_suprema(left, right, mu, s)
    remainder = float(np.dot(derivative, ((x - left) ** 3 + (right - x) ** 3) / 3))
    new_quantization = (abs(constant_signed) + remainder) / retained
    old_quantization = (old.upper - old.lower) / (2**n - 1) / 2
    quantization = min(old_quantization, new_quantization)
    grid = math.exp(-c.r * c.T) * (quantization + (old.upper - c.K) * old.total_variation)
    details = {
        "old_quantization": old_quantization,
        "new_quantization": new_quantization,
        "constant_signed": constant_signed,
        "derivative_remainder": remainder,
        "retained_mass": retained,
        "old_grid_bound": old.grid,
    }
    return replace(old, grid=grid), details
