import os
import sys
import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# ── digital_bs_price ──────────────────────────────────────────────────────────

def test_digital_bs_atm_value():
    """ATM digital price matches known BS closed-form value."""
    # digital_bs_price not yet defined — this test must FAIL
    from src.black_scholes import digital_bs_price
    price = digital_bs_price(S0=100, K=100, r=0.05, sigma=0.20, T=1.0)
    # d2 = (ln(1) + 0.03) / 0.2 = 0.15; N(0.15)=0.5596; e^{-0.05}*0.5596=0.5323
    assert abs(price - 0.5323) < 0.001, f"Expected ~0.5323, got {price:.6f}"


def test_digital_bs_deep_itm():
    """Deep ITM digital → near e^{-rT} (certain payment)."""
    from src.black_scholes import digital_bs_price
    price = digital_bs_price(S0=200, K=50, r=0.05, sigma=0.01, T=1.0)
    expected = np.exp(-0.05 * 1.0)   # d2 → +∞, N(d2) → 1
    assert abs(price - expected) < 0.01, f"Expected ~{expected:.4f}, got {price:.4f}"


def test_digital_bs_deep_otm():
    """Deep OTM digital → near zero."""
    from src.black_scholes import digital_bs_price
    price = digital_bs_price(S0=50, K=200, r=0.05, sigma=0.01, T=1.0)
    assert price < 0.001, f"Deep OTM digital should be ~0, got {price:.6f}"


def test_digital_bs_sigma_sensitivity():
    """Higher sigma → more probability mass above K → higher digital price (OTM).

    Note: S0=80 < K=100 (deep OTM). For a digital call, higher vol increases
    price when OTM because fat tails push more mass above K. For ITM options
    the relationship reverses (higher vol decreases d2 faster than it raises
    tail probability), so this test intentionally uses OTM parameters.
    """
    from src.black_scholes import digital_bs_price
    lo = digital_bs_price(S0=80, K=100, r=0.05, sigma=0.10, T=1.0)
    hi = digital_bs_price(S0=80, K=100, r=0.05, sigma=0.40, T=1.0)
    assert hi > lo, f"Higher vol should raise digital price when OTM: lo={lo:.4f} hi={hi:.4f}"
