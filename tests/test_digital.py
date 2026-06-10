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


# ── digital_mc ────────────────────────────────────────────────────────────────

def test_digital_mc_close_to_bs():
    """Naive MC at N=50 000 is within 5σ of the exact digital BS price."""
    from src.digital_option import digital_mc
    from src.black_scholes import digital_bs_price
    ref = digital_bs_price(100, 100, 0.05, 0.2, 1.0)
    price, se = digital_mc(100, 100, 0.05, 0.2, 1.0, N=50_000, seed=42)
    assert abs(price - ref) < 5 * se, f"MC={price:.4f} ref={ref:.4f} 5se={5*se:.4f}"


def test_digital_mc_std_err_decreases():
    """Larger N → smaller std_err (law of large numbers)."""
    from src.digital_option import digital_mc
    _, se_small = digital_mc(100, 100, 0.05, 0.2, 1.0, N=500,    seed=0)
    _, se_large = digital_mc(100, 100, 0.05, 0.2, 1.0, N=10_000, seed=0)
    assert se_large < se_small, "std_err must shrink as N grows"


def test_digital_mc_deep_itm():
    """Deep ITM: digital MC price close to e^{-rT}."""
    from src.digital_option import digital_mc
    price, se = digital_mc(200, 50, 0.05, 0.01, 1.0, N=10_000, seed=0)
    expected = np.exp(-0.05)
    assert abs(price - expected) < 0.02, f"Deep ITM: {price:.4f} vs {expected:.4f}"


# ── digital_antithetic_mc ─────────────────────────────────────────────────────

def test_digital_antithetic_close_to_bs():
    """Antithetic MC at N=50 000 is within 5σ of the exact digital BS price."""
    from src.digital_option import digital_antithetic_mc
    from src.black_scholes import digital_bs_price
    ref = digital_bs_price(100, 100, 0.05, 0.2, 1.0)
    price, se = digital_antithetic_mc(100, 100, 0.05, 0.2, 1.0, N=50_000, seed=42)
    assert abs(price - ref) < 5 * se, f"Antithetic={price:.4f} ref={ref:.4f}"


def test_digital_antithetic_reproducible():
    """Same seed → bit-identical result."""
    from src.digital_option import digital_antithetic_mc
    p1, se1 = digital_antithetic_mc(100, 100, 0.05, 0.2, 1.0, N=1_000, seed=99)
    p2, se2 = digital_antithetic_mc(100, 100, 0.05, 0.2, 1.0, N=1_000, seed=99)
    assert p1 == p2 and se1 == se2, "Same seed must produce bit-identical results"


# ── digital_rqmc ──────────────────────────────────────────────────────────────

def test_digital_rqmc_close_to_bs():
    """RQMC at N=1024 is within 5σ of the exact digital BS price."""
    from src.digital_option import digital_rqmc
    from src.black_scholes import digital_bs_price
    ref = digital_bs_price(100, 100, 0.05, 0.2, 1.0)
    price, se = digital_rqmc(100, 100, 0.05, 0.2, 1.0, N=1_024, n_replications=30, seed=0)
    assert abs(price - ref) < 5 * se, f"RQMC={price:.4f} ref={ref:.4f} 5se={5*se:.4f}"


def test_digital_rqmc_reproducible():
    """Same seed → bit-identical result."""
    from src.digital_option import digital_rqmc
    p1, _ = digital_rqmc(100, 100, 0.05, 0.2, 1.0, N=512, n_replications=10, seed=5)
    p2, _ = digital_rqmc(100, 100, 0.05, 0.2, 1.0, N=512, n_replications=10, seed=5)
    assert p1 == p2, "Same seed must produce bit-identical result"
