# tests/test_asian_cv_ref.py
import os
import sys
import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.asian_option import geometric_asian_closed_form, simulate_paths
from src.black_scholes import black_scholes_call


def test_cv_ref_price_between_geo_and_european():
    """Arithmetic Asian price > geometric (Jensen's inequality) and
    < European call (averaging reduces terminal exposure)."""
    # arithmetic_asian_cv_ref not yet defined — this test must FAIL
    from src.asian_option import arithmetic_asian_cv_ref
    S0, K, r, sigma, T = 100.0, 100.0, 0.05, 0.2, 1.0
    price, _ = arithmetic_asian_cv_ref(S0, K, r, sigma, T, d=4, N_ref=50_000, seed=42)
    geo_cf   = geometric_asian_closed_form(S0, K, r, sigma, T, d=4)
    bs_price = black_scholes_call(S0, K, r, sigma, T)
    assert geo_cf < price < bs_price, (
        f"Expected geo={geo_cf:.4f} < arith={price:.4f} < BS={bs_price:.4f}"
    )


def test_cv_ref_se_much_smaller_than_naive():
    """CV SE at N=10,000 must be less than half of naive MC SE at same N,
    confirming the arith-geo correlation reduces variance substantially."""
    from src.asian_option import arithmetic_asian_cv_ref
    S0, K, r, sigma, T = 100.0, 100.0, 0.05, 0.2, 1.0
    d, N = 4, 10_000
    _, cv_se = arithmetic_asian_cv_ref(S0, K, r, sigma, T, d=d, N_ref=N, seed=42)
    # Naive MC SE for comparison (no variance reduction)
    rng = np.random.default_rng(42)
    Z = rng.standard_normal((N, d))
    S_paths = simulate_paths(S0, r, sigma, T, Z)
    discount = np.exp(-r * T)
    payoffs = np.maximum(S_paths.mean(axis=1) - K, 0.0)
    naive_se = discount * payoffs.std(ddof=1) / np.sqrt(N)
    assert cv_se < naive_se * 0.5, (
        f"CV SE={cv_se:.6f} should be < half of naive SE={naive_se:.6f}"
    )


def test_cv_ref_reproducible_with_seed():
    """Identical seed → identical (price, se). Confirms determinism."""
    from src.asian_option import arithmetic_asian_cv_ref
    S0, K, r, sigma, T = 100.0, 100.0, 0.05, 0.2, 1.0
    p1, se1 = arithmetic_asian_cv_ref(S0, K, r, sigma, T, d=8, N_ref=10_000, seed=7)
    p2, se2 = arithmetic_asian_cv_ref(S0, K, r, sigma, T, d=8, N_ref=10_000, seed=7)
    assert p1 == p2 and se1 == se2, "Same seed must produce bit-identical results"
