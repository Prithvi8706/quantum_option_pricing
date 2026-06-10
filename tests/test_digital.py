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


# ── QAE digital oracle ────────────────────────────────────────────────────────

def test_build_digital_circuit_qubit_count():
    """_build_digital_circuit: obj_q == n; circuit has at least n+1 qubits (LinearAmplitudeFunction adds ancillae)."""
    pytest.importorskip("qiskit", reason="Qiskit not installed")
    from src.quantum import _build_digital_circuit
    n = 3
    circ, obj_q = _build_digital_circuit(100, 100, 0.05, 0.2, 1.0, num_uncertainty_qubits=n)
    assert obj_q == n, f"Expected objective_qubit={n}, got {obj_q}"
    assert circ.num_qubits >= n + 1, f"Expected at least {n+1} qubits, got {circ.num_qubits}"


def test_digital_circuit_step_encoding():
    """sv P(obj=|1>) equals classical grid P(S>K) at n=3 — Section D2 check."""
    pytest.importorskip("qiskit", reason="Qiskit not installed")
    import numpy as np
    from qiskit.quantum_info import Statevector
    from qiskit_finance.circuit.library import LogNormalDistribution
    from src.quantum import _build_digital_circuit

    S0, K, r, sigma, T = 100.0, 100.0, 0.05, 0.2, 1.0
    n = 3
    sigma_c = max(sigma, 0.15)
    mu_ln = (r - 0.5 * sigma_c**2) * T + np.log(S0)
    sigma_var = (sigma_c * np.sqrt(T))**2
    mean_s = np.exp(mu_ln + 0.5 * sigma_var)
    var_s  = (np.exp(sigma_var) - 1) * np.exp(2 * mu_ln + sigma_var)
    std_s  = np.sqrt(var_s)
    low    = max(0.0, min(mean_s - 3 * std_s, K * 0.98))
    high   = max(mean_s + 3 * std_s, K * 1.02)

    full_circ, _ = _build_digital_circuit(S0, K, r, sigma, T, n)
    sv_probs = np.abs(np.array(Statevector(full_circ)))**2
    prob_obj1 = sum(sv_probs[i] for i in range(len(sv_probs)) if (i >> n) & 1)

    lnd = LogNormalDistribution(n, mu=mu_ln, sigma=sigma_var, bounds=(low, high))
    grid_p = np.dot(lnd._probabilities, (np.array(lnd._values) > K).astype(float))

    assert abs(prob_obj1 - grid_p) < 1e-6, (
        f"Step encoding mismatch: sv P(obj=1)={prob_obj1:.6f}  grid_p={grid_p:.6f}"
    )


def test_quantum_digital_call_converges_to_grid_price():
    """quantum_digital_call at n=5, eps=0.01 is within 0.02 of grid_true_price."""
    pytest.importorskip("qiskit", reason="Qiskit not installed")
    import numpy as np
    from qiskit_finance.circuit.library import LogNormalDistribution
    from src.quantum import quantum_digital_call

    S0, K, r, sigma, T = 100.0, 100.0, 0.05, 0.2, 1.0
    n = 5
    sigma_c = max(sigma, 0.15)
    mu_ln = (r - 0.5 * sigma_c**2) * T + np.log(S0)
    sigma_var = (sigma_c * np.sqrt(T))**2
    mean_s = np.exp(mu_ln + 0.5 * sigma_var)
    var_s  = (np.exp(sigma_var) - 1) * np.exp(2 * mu_ln + sigma_var)
    std_s  = np.sqrt(var_s)
    low    = max(0.0, min(mean_s - 3 * std_s, K * 0.98))
    high   = max(mean_s + 3 * std_s, K * 1.02)

    lnd = LogNormalDistribution(n, mu=mu_ln, sigma=sigma_var, bounds=(low, high))
    grid_p = np.dot(lnd._probabilities, (np.array(lnd._values) > K).astype(float))
    grid_true_price = np.exp(-r * T) * grid_p

    price, ci, elapsed, M = quantum_digital_call(S0, K, r, sigma, T, n, epsilon=0.01)
    assert abs(price - grid_true_price) < 0.02, (
        f"QAE price={price:.4f}  grid_true={grid_true_price:.4f}  diff={abs(price-grid_true_price):.4f}"
    )
    assert M > 0, "oracle_queries must be positive"
    assert ci[0] <= price <= ci[1], f"price {price:.4f} not in CI ({ci[0]:.4f}, {ci[1]:.4f})"


def test_quantum_digital_sigma_clamp():
    """sigma < 0.15 is clamped: same result as sigma=0.15."""
    pytest.importorskip("qiskit", reason="Qiskit not installed")
    from src.quantum import quantum_digital_call
    p_clamped, _, _, _ = quantum_digital_call(100, 100, 0.05, 0.10, 1.0, num_uncertainty_qubits=3)
    p_floor,   _, _, _ = quantum_digital_call(100, 100, 0.05, 0.15, 1.0, num_uncertainty_qubits=3)
    assert abs(p_clamped - p_floor) < 1e-9, (
        f"Clamp not applied: sigma=0.10 → {p_clamped:.6f}, sigma=0.15 → {p_floor:.6f}"
    )
