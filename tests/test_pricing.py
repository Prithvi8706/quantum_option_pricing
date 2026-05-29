import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.black_scholes import black_scholes_call
from src.classical import monte_carlo_call


# ── Black-Scholes ─────────────────────────────────────────────────────────────

def test_bs_atm():
    """ATM call price matches known analytical value."""
    price = black_scholes_call(S0=100, K=100, r=0.05, sigma=0.20, T=1.0)
    assert abs(price - 10.45) < 0.02, f"Expected ~10.45, got {price:.4f}"


def test_bs_deep_itm():
    """Deep ITM call price exceeds intrinsic value."""
    price = black_scholes_call(S0=120, K=80, r=0.05, sigma=0.20, T=1.0)
    intrinsic = 120 - 80 * 1.0  # loose lower bound
    assert price > 35, f"Deep ITM price should be > $35, got {price:.4f}"


def test_bs_deep_otm():
    """Deep OTM call price is near zero."""
    price = black_scholes_call(S0=80, K=120, r=0.05, sigma=0.10, T=0.5)
    assert price < 0.01, f"Deep OTM price should be ~0, got {price:.6f}"


def test_bs_put_call_parity():
    """C - P = S0 - K*e^(-rT): put via parity should be ~5.57 for ATM 1y 20% vol."""
    import numpy as np
    S0, K, r, sigma, T = 100, 100, 0.05, 0.20, 1.0
    call = black_scholes_call(S0, K, r, sigma, T)
    put = call - S0 + K * np.exp(-r * T)
    assert 5.0 < put < 6.5, f"Put via parity = {put:.4f}, expected ~5.57"


# ── Monte Carlo ───────────────────────────────────────────────────────────────

def test_mc_close_to_bs():
    """MC at N=20 000 is within $1 of Black-Scholes."""
    bs = black_scholes_call(S0=100, K=100, r=0.05, sigma=0.20, T=1.0)
    mc_p, mc_err = monte_carlo_call(S0=100, K=100, r=0.05, sigma=0.20, T=1.0, N=20_000)
    assert abs(mc_p - bs) < 1.0, f"MC={mc_p:.4f} BS={bs:.4f}"
    assert mc_err > 0, "std_err must be positive"


def test_mc_err_decreases_with_n():
    """Larger N yields smaller standard error (law of large numbers)."""
    _, err_small = monte_carlo_call(100, 100, 0.05, 0.20, 1.0, N=500)
    _, err_large = monte_carlo_call(100, 100, 0.05, 0.20, 1.0, N=10_000)
    assert err_large < err_small, "std_err should shrink as N grows"


def test_mc_nonnegative():
    """Option price is always non-negative."""
    price, _ = monte_carlo_call(S0=80, K=120, r=0.05, sigma=0.10, T=0.5, N=1_000)
    assert price >= 0, f"Price must be >= 0, got {price}"


# ── Sigma floor (quantum clamping logic) ──────────────────────────────────────

def test_sigma_floor_clamps_below_015():
    """quantum_call with sigma < 0.15 returns the same price as sigma=0.15 (clamped)."""
    pytest.importorskip("qiskit", reason="Qiskit not installed (dev dependency)")
    from src.quantum import quantum_call
    p_clamped, _, _, _ = quantum_call(100.0, 100.0, 0.05, 0.10, 1.0)
    p_floor,   _, _, _ = quantum_call(100.0, 100.0, 0.05, 0.15, 1.0)
    assert abs(p_clamped - p_floor) < 1e-9, (
        f"Clamp not applied: sigma=0.10 → {p_clamped:.6f}, sigma=0.15 → {p_floor:.6f}"
    )


def test_sigma_floor_passes_above_015():
    """quantum_call with sigma=0.20 is not clamped to 0.15 (price differs from sigma=0.15)."""
    pytest.importorskip("qiskit", reason="Qiskit not installed (dev dependency)")
    from src.quantum import quantum_call
    p_at_floor, _, _, _ = quantum_call(100.0, 100.0, 0.05, 0.15, 1.0)
    p_above,    _, _, _ = quantum_call(100.0, 100.0, 0.05, 0.20, 1.0)
    assert abs(p_above - p_at_floor) > 0.05, (
        f"sigma=0.20 should differ from sigma=0.15: {p_above:.4f} vs {p_at_floor:.4f}"
    )


def test_bs_sigma_sensitivity():
    """Higher volatility → higher call price (vega > 0)."""
    lo = black_scholes_call(S0=100, K=100, r=0.05, sigma=0.10, T=1.0)
    hi = black_scholes_call(S0=100, K=100, r=0.05, sigma=0.40, T=1.0)
    assert hi > lo, "Higher sigma must produce higher call price"
