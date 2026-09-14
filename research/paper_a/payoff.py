"""Annex C: objective probability and dollar post-processing.

h() is the exact inverse of the LINEARIZED sin^2 map, matching Qiskit's
LinearAmplitudeFunction.post_processing. The gap between the true sin^2 and
its linearization is precisely the encoding error e_encode, and it is a
direct function of the rescaling factor c.
"""
from __future__ import annotations

import math

import numpy as np

C_RESCALING = 0.25


def _check_c(c: float) -> None:
    if not math.isfinite(c) or not 0 < c <= 1:
        raise ValueError(f"rescaling factor must be in (0,1], got {c}")


def objective_amplitudes(x: np.ndarray, K: float, U: float,
                         c: float) -> np.ndarray:
    """a_i = sin^2(theta_i) with theta_i = (pi/4)(1-c) + (pi c/2) y_i."""
    _check_c(c)
    y = np.maximum(0.0, x - K) / (U - K)
    theta = (math.pi / 4.0) * (1.0 - c) + (math.pi * c / 2.0) * y
    return np.sin(theta) ** 2


def a_calc(pi: np.ndarray, x: np.ndarray, K: float, U: float,
           c: float) -> float:
    """Independently calculated objective probability sum_i pi_i a_i."""
    return float((pi * objective_amplitudes(x, K, U, c)).sum())


def h_inverse(a: float, K: float, U: float, c: float) -> float:
    """h(a) = (U-K)(2/pi c)(a - 1/2 + pi c/4). Applied exactly once."""
    _check_c(c)
    return (U - K) * (2.0 / (math.pi * c)) * (a - 0.5 + math.pi * c / 4.0)


def to_price(a: float, K: float, U: float, c: float, r: float,
             T: float) -> float:
    """Discounted dollar price. Discount applied exactly once."""
    return math.exp(-r * T) * h_inverse(a, K, U, c)


def presentation_clipped(price: float) -> float:
    """Display-only. Never used for error, interval, or failure accounting."""
    return max(0.0, price)
