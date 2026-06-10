# European Digital Option Convergence Experiment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a European digital (cash-or-nothing) call convergence experiment comparing Naive MC, Antithetic MC, RQMC (Sobol), and QAE (IQAE) — testing whether QAE's quadratic advantage re-emerges on a discontinuous payoff where RQMC's smoothness assumption formally breaks down.

**Architecture:** Four new source units (`digital_bs_price` in `black_scholes.py`, new `digital_option.py`, two new functions in `quantum.py`, and `plot_digital_convergence.py`) follow the pattern established by Paper B's Asian experiment. TDD: failing tests precede every implementation. Script is gated: Sections A+D (validation) must pass before the slow classical sweep (Section E) or QAE sweep (Section F) runs.

**Tech Stack:** Python 3, NumPy, SciPy (`qmc`, `norm`, `stats`), Qiskit / qiskit-algorithms 0.3.1 / qiskit-finance, Matplotlib, pytest (scipy==1.13.1 venv)

---

## File Map

| Path | Action | Responsibility |
|---|---|---|
| `src/black_scholes.py` | Modify (append) | Add `digital_bs_price()` after `black_scholes_call` |
| `src/digital_option.py` | Create | `digital_mc()`, `digital_antithetic_mc()`, `digital_rqmc()` |
| `src/quantum.py` | Modify (append) | Add `LinearAmplitudeFunction` import, `_build_digital_circuit()`, `quantum_digital_call()` |
| `src/plot_digital_convergence.py` | Create | Experiment script: validation gate → classical sweep → QAE sweep → table → figure |
| `tests/test_digital.py` | Create | Unit tests for all new functions |
| `figures/fig_digital_convergence.png` | Create (output) | Written by script on execution |

---

## Task 1: Write failing tests for `digital_bs_price`, then implement

**Files:**
- Create: `tests/test_digital.py`
- Modify: `src/black_scholes.py`

- [ ] **Step 1: Create test file with failing tests for `digital_bs_price`**

```python
# tests/test_digital.py
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
    """Higher sigma → more probability mass above K → higher digital price (near ATM)."""
    from src.black_scholes import digital_bs_price
    lo = digital_bs_price(S0=110, K=100, r=0.05, sigma=0.10, T=1.0)
    hi = digital_bs_price(S0=110, K=100, r=0.05, sigma=0.40, T=1.0)
    assert hi > lo, "Higher vol should raise digital price when ITM"
```

- [ ] **Step 2: Run — verify all four FAIL with ImportError**

```
venv\Scripts\pytest.exe tests\test_digital.py::test_digital_bs_atm_value tests\test_digital.py::test_digital_bs_deep_itm tests\test_digital.py::test_digital_bs_deep_otm tests\test_digital.py::test_digital_bs_sigma_sensitivity -v
```

Expected: all four FAIL with `ImportError: cannot import name 'digital_bs_price'`

- [ ] **Step 3: Append `digital_bs_price` to `src/black_scholes.py`**

Add after `black_scholes_call` (after the closing `return price` on line 23):

```python
def digital_bs_price(S0: float, K: float, r: float, sigma: float, T: float) -> float:
    """
    Exact Black-Scholes price for a European cash-or-nothing (digital) call.

    Parameters
    ----------
    S0    : Initial stock price
    K     : Strike price
    r     : Risk-free interest rate (annualised)
    sigma : Volatility (annualised)
    T     : Time to expiry (years)

    Returns
    -------
    price : float — e^{-rT} * N(d2)
    """
    d2 = (np.log(S0 / K) + (r - 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return np.exp(-r * T) * norm.cdf(d2)
```

- [ ] **Step 4: Run tests — verify all four PASS**

```
venv\Scripts\pytest.exe tests\test_digital.py::test_digital_bs_atm_value tests\test_digital.py::test_digital_bs_deep_itm tests\test_digital.py::test_digital_bs_deep_otm tests\test_digital.py::test_digital_bs_sigma_sensitivity -v
```

Expected: 4 passed

- [ ] **Step 5: Run existing tests — no regressions**

```
venv\Scripts\pytest.exe tests\test_pricing.py -v
```

Expected: same pass/skip counts as before.

- [ ] **Step 6: Commit**

```
git add src\black_scholes.py tests\test_digital.py
git commit -m "feat: add digital_bs_price to black_scholes.py with tests"
```

---

## Task 2: Create `src/digital_option.py` with TDD

**Files:**
- Modify: `tests/test_digital.py` — append tests for the three pricers
- Create: `src/digital_option.py`

- [ ] **Step 7: Append digital pricer tests to `tests/test_digital.py`**

```python
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
```

- [ ] **Step 8: Run new tests — verify all seven FAIL with ImportError**

```
venv\Scripts\pytest.exe tests\test_digital.py -k "mc or rqmc" -v
```

Expected: 7 FAIL with `ImportError: cannot import name 'digital_mc'` (or similar)

- [ ] **Step 9: Create `src/digital_option.py`**

```python
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
```

- [ ] **Step 10: Run all digital tests — verify all eleven PASS**

```
venv\Scripts\pytest.exe tests\test_digital.py -v
```

Expected: 11 passed (4 BS + 7 digital pricers)

- [ ] **Step 11: Run full test suite — no regressions**

```
venv\Scripts\pytest.exe tests\ -v
```

Expected: all previously-passing tests still pass.

- [ ] **Step 12: Commit**

```
git add src\digital_option.py tests\test_digital.py
git commit -m "feat: add digital_option.py with MC, antithetic, RQMC pricers and tests"
```

---

## Task 3: Add `_build_digital_circuit` and `quantum_digital_call` to `quantum.py`

**Files:**
- Modify: `tests/test_digital.py` — append QAE tests
- Modify: `src/quantum.py` — append import + two new functions

- [ ] **Step 13: Append QAE tests to `tests/test_digital.py`**

```python
# ── QAE digital oracle ────────────────────────────────────────────────────────

def test_build_digital_circuit_qubit_count():
    """_build_digital_circuit returns a circuit with n+1 qubits, obj qubit = n."""
    pytest.importorskip("qiskit", reason="Qiskit not installed")
    from src.quantum import _build_digital_circuit
    circ, obj_q = _build_digital_circuit(100, 100, 0.05, 0.2, 1.0, num_uncertainty_qubits=3)
    assert obj_q == 3, f"Expected objective_qubit=3, got {obj_q}"
    assert circ.num_qubits == 4, f"Expected 4 qubits (n=3 + 1 obj), got {circ.num_qubits}"


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
```

- [ ] **Step 14: Run new QAE tests — verify all four FAIL**

```
venv\Scripts\pytest.exe tests\test_digital.py -k "digital_circuit or quantum_digital" -v
```

Expected: 4 FAIL with `ImportError: cannot import name '_build_digital_circuit'`

- [ ] **Step 15: Add `LinearAmplitudeFunction` import and append two functions to `src/quantum.py`**

First, add the import to the existing import block at the top of `src/quantum.py` (after line 6, the `qiskit_finance` import):

```python
from qiskit.circuit.library import LinearAmplitudeFunction
```

Then append both functions after `quantum_call` (at the end of the file):

```python
def _build_digital_circuit(
    S0: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    num_uncertainty_qubits: int = 5,
) -> tuple[QuantumCircuit, int]:
    # Same sigma clamp as _build_circuit: very low sigma causes Qiskit domain errors.
    sigma = max(sigma, 0.15)

    mu_ln = (r - 0.5 * sigma**2) * T + np.log(S0)
    sigma_ln = sigma * np.sqrt(T)
    sigma_var = sigma_ln**2

    mean_stock = np.exp(mu_ln + 0.5 * sigma_var)
    var_stock = (np.exp(sigma_var) - 1) * np.exp(2 * mu_ln + sigma_var)
    std_stock = np.sqrt(var_stock)
    low = max(0.0, min(mean_stock - 3 * std_stock, K * 0.98))
    high = max(mean_stock + 3 * std_stock, K * 1.02)

    uncertainty_model = LogNormalDistribution(
        num_uncertainty_qubits,
        mu=mu_ln,
        sigma=sigma_var,
        bounds=(low, high),
    )

    # Step function: f(x) = 0 for x < K, f(x) = 1 for x >= K.
    # rescaling_factor=1.0 is exact for binary payoff (no Woerner approximation).
    # breakpoints=[low, K] puts K on the >= side (pays 1 at S_T = K).
    digital_obj = LinearAmplitudeFunction(
        num_state_qubits=num_uncertainty_qubits,
        slope=[0, 0],
        offset=[0, 1],
        domain=(low, high),
        image=(0, 1),
        breakpoints=[low, K],
        rescaling_factor=1.0,
    )

    full_circuit = QuantumCircuit(digital_obj.num_qubits)
    full_circuit.append(uncertainty_model, range(num_uncertainty_qubits))
    full_circuit.append(digital_obj, range(digital_obj.num_qubits))

    return full_circuit, num_uncertainty_qubits


def quantum_digital_call(
    S0: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    num_uncertainty_qubits: int = 5,
    epsilon: float = 0.01,
    alpha: float = 0.05,
) -> tuple[float, tuple[float, float], float, int]:
    """
    Price a European digital (cash-or-nothing) call via IQAE.

    Parameters
    ----------
    S0    : Initial stock price
    K     : Strike price
    r     : Risk-free interest rate (annualised)
    sigma : Volatility (annualised)
    T     : Time to expiry (years)
    num_uncertainty_qubits : Qubits to discretise the log-normal distribution.
    epsilon : IQAE target half-width precision.
    alpha   : Significance level for the confidence interval.

    Returns
    -------
    price          : float — discounted P(S_T > K on n-qubit grid) = grid_true_price
    conf_int       : (float, float) — (1-alpha) CI on the price
    elapsed        : float — wall-clock seconds
    oracle_queries : int — sum(2k+1 for k in result.powers)

    Note: price converges to grid_true_price (exact probability on the n-qubit
    grid), NOT to the continuous digital_bs_price. Grid bias at n=5 ≈ 2.16e-02
    at standard params (S0=K=100, r=0.05, sigma=0.2, T=1.0) — a fixed
    systematic offset independent of epsilon.

    Implementation note: post_processing=lambda a: a (identity). In Qiskit
    0.3.1, IQAE reports result.estimation = P(obj=|1>) directly (the probability,
    not the amplitude sqrt(P)). Confirmed empirically: result.estimation=grid_p.
    LinearAmplitudeFunction.post_processing is NOT used here.
    """
    t0 = time.perf_counter()

    full_circuit, objective_qubit = _build_digital_circuit(
        S0, K, r, sigma, T, num_uncertainty_qubits
    )

    problem = EstimationProblem(
        state_preparation=full_circuit,
        objective_qubits=[objective_qubit],
        post_processing=lambda a: a,  # identity: IQAE returns P(obj=1) = grid_p
    )

    iae = IterativeAmplitudeEstimation(
        epsilon_target=epsilon,
        alpha=alpha,
        sampler=Sampler(),
    )
    result = iae.estimate(problem)

    discount = np.exp(-r * T)
    price = result.estimation_processed * discount
    ci_raw = result.confidence_interval_processed
    conf_int = (max(0.0, ci_raw[0]) * discount, min(1.0, ci_raw[1]) * discount)

    elapsed = time.perf_counter() - t0
    oracle_queries = sum(2 * k + 1 for k in result.powers)
    return price, conf_int, elapsed, oracle_queries
```

- [ ] **Step 16: Run QAE tests — verify all four PASS**

```
venv\Scripts\pytest.exe tests\test_digital.py -k "digital_circuit or quantum_digital" -v
```

Expected: 4 passed. `test_quantum_digital_call_converges_to_grid_price` may take ~2 min (statevector IQAE at n=5).

- [ ] **Step 17: Run full test suite — no regressions**

```
venv\Scripts\pytest.exe tests\ -v
```

Expected: all previously-passing tests still pass. New digital tests all pass.

- [ ] **Step 18: Commit**

```
git add src\quantum.py tests\test_digital.py
git commit -m "feat: add _build_digital_circuit and quantum_digital_call to quantum.py"
```

---

## Task 4: `plot_digital_convergence.py` — Sections A+D (validation gate only)

Build and gate-check the script incrementally. This task writes only the reference, MC sanity check, and the full Section D QAE validation. The slow sweep (Sections E–F) is added in Task 5 only after this gate passes.

**Files:**
- Create: `src/plot_digital_convergence.py`

- [ ] **Step 19: Create the script with Sections A and D only**

```python
"""
European digital option convergence experiment — Paper B, Section VII.

MC / Antithetic MC / RQMC (Sobol) / QAE (IQAE) on a cash-or-nothing call.
Tests whether QAE's quadratic advantage survives a discontinuous payoff.

Sections:
  A  — Exact reference + MC sanity check
  D  — QAE discretization validation gate (mandatory; must pass before sweep)
  E  — Classical convergence sweep  [added in Task 5]
  F  — QAE epsilon sweep            [added in Task 5]
  G  — Printed table + figure       [added in Task 5]

Scientific question: does RQMC's empirical slope degrade from ~-1.0 toward
-0.5 on the discontinuous digital payoff? Three possible outcomes are tested
with equal weight — see spec for details.

Cross-comparability note: N ∈ [256, 65536] here. Slopes are NOT cross-
comparable to Tables IV/V (Asian, N ∈ [1024, 16384]).
"""
import os
import sys
import warnings

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm as _scipy_norm

sys.path.insert(0, os.path.dirname(__file__))
from black_scholes import digital_bs_price
from digital_option import digital_mc, digital_antithetic_mc, digital_rqmc
from quantum import _build_digital_circuit, quantum_digital_call

warnings.filterwarnings("ignore", category=UserWarning)

# ── Parameters ─────────────────────────────────────────────────────────────────
S0, K, r, sigma, T = 100.0, 100.0, 0.05, 0.2, 1.0

N_VALUES      = [2**i for i in range(8, 17)]    # 256 → 65536 (9 points)
N_TRIALS      = 10
N_REP         = 30
N_BOOT        = 2000
CI_PERCENTILE = (2.5, 97.5)
N_SANITY      = 1_000_000

QAE_N_QUBITS  = 5
QAE_EPSILONS  = [0.001, 0.002, 0.004, 0.007, 0.010, 0.015, 0.020]
QAE_ALPHA     = 0.05

# Bounds (same logic as _build_digital_circuit, sigma ≥ 0.15 guaranteed here)
sigma_c   = max(sigma, 0.15)
mu_ln     = (r - 0.5 * sigma_c**2) * T + np.log(S0)
sigma_var = (sigma_c * np.sqrt(T))**2
mean_s    = np.exp(mu_ln + 0.5 * sigma_var)
var_s     = (np.exp(sigma_var) - 1) * np.exp(2 * mu_ln + sigma_var)
std_s     = np.sqrt(var_s)
low       = max(0.0, min(mean_s - 3 * std_s, K * 0.98))
high      = max(mean_s + 3 * std_s, K * 1.02)

# ── Section A: Exact reference + MC sanity check ───────────────────────────────
print("=== Section A: Reference and MC sanity check ===\n")

ref = digital_bs_price(S0, K, r, sigma, T)
print(f"Exact digital BS price: {ref:.6f}  (e^{{-rT}}*N(d2))\n")

mc_price, mc_se = digital_mc(S0, K, r, sigma, T, N_SANITY, seed=0)
err_mc = abs(mc_price - ref)
assert err_mc < 5 * mc_se, (
    f"MC sanity FAILED: |mc - exact| = {err_mc:.2e} >= 5*se = {5*mc_se:.2e}"
)
print(f"MC sanity (N={N_SANITY:,}): |mc - exact| = {err_mc:.2e}   5σ = {5*mc_se:.2e}   PASS\n")

# ── Section D: QAE discretization validation gate (mandatory) ─────────────────
print("=== Section D: QAE discretization validation ===\n")

from qiskit_finance.circuit.library import LogNormalDistribution
from qiskit.quantum_info import Statevector

# D1 — Grid bias shrinks with n + normalization guard
print("  D1: Grid bias vs number of uncertainty qubits")
biases = {}
for n in [3, 4, 5]:
    lnd = LogNormalDistribution(n, mu=mu_ln, sigma=sigma_var, bounds=(low, high))
    x_grid     = np.array(lnd._values)
    grid_probs = np.array(lnd._probabilities)
    assert np.isclose(grid_probs.sum(), 1.0), (
        f"n={n}: lnd._probabilities sums to {grid_probs.sum():.8f}, not 1.0 — "
        "LogNormalDistribution internals may have changed"
    )
    grid_p     = np.dot(grid_probs, (x_grid > K).astype(float))
    grid_price = np.exp(-r * T) * grid_p
    bias       = abs(grid_price - ref)
    biases[n]  = bias
    print(f"    n={n}: grid_price={grid_price:.6f}  exact={ref:.6f}  bias={bias:.2e}")

assert biases[4] < biases[3], "ABORT — bias(n=4) >= bias(n=3); check bounds/LogNormal params"
assert biases[5] < biases[4], "ABORT — bias(n=5) >= bias(n=4); check bounds/LogNormal params"
print("  D1 PASS: grid bias monotone-decreasing with n\n")

# D2 — Step encoding correctness (load-bearing)
print("  D2: Step encoding — sv P(obj=|1>) vs classical grid_p at n=3")
n_check = 3
full_circ_chk, _ = _build_digital_circuit(S0, K, r, sigma, T, n_check)
sv_probs_chk = np.abs(np.array(Statevector(full_circ_chk)))**2
prob_obj1_chk = sum(sv_probs_chk[i] for i in range(len(sv_probs_chk)) if (i >> n_check) & 1)

lnd_chk   = LogNormalDistribution(n_check, mu=mu_ln, sigma=sigma_var, bounds=(low, high))
grid_p_chk = np.dot(lnd_chk._probabilities, (np.array(lnd_chk._values) > K).astype(float))

assert abs(prob_obj1_chk - grid_p_chk) < 1e-6, (
    f"Step encoding MISMATCH: sv P(obj=1)={prob_obj1_chk:.6f}  grid_p={grid_p_chk:.6f}\n"
    "  LinearAmplitudeFunction image=(0,1) may be silently renormalized — stop."
)
print(f"  D2 PASS: sv P(obj=1) = {prob_obj1_chk:.6f}  grid_p = {grid_p_chk:.6f}  diff < 1e-6\n")

# D3 — Compute grid_true_price for n=5 (used as QAE convergence reference in Section F)
lnd5       = LogNormalDistribution(QAE_N_QUBITS, mu=mu_ln, sigma=sigma_var, bounds=(low, high))
grid_probs5 = np.array(lnd5._probabilities)
assert np.isclose(grid_probs5.sum(), 1.0), "n=5 normalization assert failed"
grid_p5    = np.dot(grid_probs5, (np.array(lnd5._values) > K).astype(float))
grid_true_price = np.exp(-r * T) * grid_p5
grid_bias_n5 = abs(grid_true_price - ref)
print(f"  D3: n=5 grid_true_price = {grid_true_price:.6f}")
print(f"       exact BS price      = {ref:.6f}")
print(f"       grid bias (n=5)     = {grid_bias_n5:.2e}  (fixed systematic offset)")
print(f"\n  All Section D checks passed.\n")

# ── Sections E, F, G: added in Task 5 ─────────────────────────────────────────
print("Sections E, F, G not yet implemented.")
```

- [ ] **Step 20: Confirm scipy version, then run Sections A+D**

```
venv\Scripts\python.exe -c "import scipy; print(scipy.__version__)"
```

Expected: `1.13.1`

```
venv\Scripts\python.exe src\plot_digital_convergence.py
```

Expected output (full — paste this for review):

```
=== Section A: Reference and MC sanity check ===

Exact digital BS price: 0.532325  (e^{-rT}*N(d2))

MC sanity (N=1,000,000): |mc - exact| = X.XXe-XX   5σ = X.XXe-XX   PASS

=== Section D: QAE discretization validation ===

  D1: Grid bias vs number of uncertainty qubits
    n=3: grid_price=0.432301  exact=0.532325  bias=1.00e-01
    n=4: grid_price=0.594159  exact=0.532325  bias=6.18e-02
    n=5: grid_price=0.510712  exact=0.532325  bias=2.16e-02
  D1 PASS: grid bias monotone-decreasing with n

  D2: Step encoding — sv P(obj=|1>) vs classical grid_p at n=3
  D2 PASS: sv P(obj=1) = 0.454466  grid_p = 0.454466  diff < 1e-6

  D3: n=5 grid_true_price = 0.510712
       exact BS price      = 0.532325
       grid bias (n=5)     = 2.16e-02  (fixed systematic offset)

  All Section D checks passed.

Sections E, F, G not yet implemented.
```

**CHECKPOINT — stop here and paste the Section D output for review before continuing to Task 5.**

If any assert fails (D1 bias not monotone, D2 mismatch, normalization error): **stop, paste the full traceback**. Do not proceed to Task 5.

- [ ] **Step 21: Commit the partial script**

```
git add src\plot_digital_convergence.py
git commit -m "wip: add digital convergence script Sections A+D (validation gate)"
```

---

## Task 5: Add Sections E, F, G — classical sweep, QAE sweep, table, figure

**Prerequisite:** Task 4 checkpoint passed (Section D output reviewed and approved).

**Files:**
- Modify: `src/plot_digital_convergence.py` — replace the stub line with Sections E–G

- [ ] **Step 22: Replace the stub with Sections E, F, G**

Replace the final two lines of `plot_digital_convergence.py` (`# ── Sections E, F, G ...` through `print("Sections E, F, G not yet implemented.")`) with:

```python
# ── Section E: Classical convergence sweep ─────────────────────────────────────
methods  = ["Naive MC", "Antithetic MC", "RQMC"]
colors   = {"Naive MC": "#1f77b4", "Antithetic MC": "#2ca02c", "RQMC": "#9467bd"}
markers  = {"Naive MC": "o", "Antithetic MC": "s", "RQMC": "D"}

log_N    = np.log10(N_VALUES)
boot_rng = np.random.default_rng(0)   # fixed → reproducible CIs

central = {m: None for m in methods}
ci_lo   = {m: None for m in methods}
ci_hi   = {m: None for m in methods}

errs = {m: np.zeros((N_TRIALS, len(N_VALUES))) for m in methods}

print(f"=== Section E: Classical sweep ({N_TRIALS} trials, {N_REP} reps, {N_BOOT} bootstrap) ===\n")

for j, N in enumerate(N_VALUES):
    for t in range(N_TRIALS):
        p_naive, _ = digital_mc(
            S0, K, r, sigma, T, N, seed=t)
        p_anti,  _ = digital_antithetic_mc(
            S0, K, r, sigma, T, N, seed=t)
        p_rqmc,  _ = digital_rqmc(
            S0, K, r, sigma, T, N, n_replications=N_REP, seed=t * 1000)
        errs["Naive MC"][t, j]      = abs(p_naive - ref)
        errs["Antithetic MC"][t, j] = abs(p_anti  - ref)
        errs["RQMC"][t, j]          = abs(p_rqmc  - ref)

for m in methods:
    mean_curve = errs[m].mean(axis=0)
    c = np.polyfit(log_N, np.log10(mean_curve), 1)[0]
    boot = np.empty(N_BOOT)
    for b in range(N_BOOT):
        idx     = boot_rng.integers(0, N_TRIALS, N_TRIALS)
        mc_b    = errs[m][idx].mean(axis=0)
        boot[b] = np.polyfit(log_N, np.log10(mc_b), 1)[0]
    lo, hi        = np.percentile(boot, CI_PERCENTILE)
    central[m]    = c
    ci_lo[m]      = lo
    ci_hi[m]      = hi
    atm_note      = "  * ATM symmetry watch-item" if m == "Antithetic MC" else ""
    print(f"  {m:<18}: slope = {c:+.3f}  95% CI [{lo:+.3f}, {hi:+.3f}]{atm_note}")

print()

# ── Section F: QAE epsilon sweep ───────────────────────────────────────────────
print(f"=== Section F: QAE epsilon sweep (n={QAE_N_QUBITS}) ===\n")
print(f"  (grid_true_price = {grid_true_price:.6f}  grid_bias = {grid_bias_n5:.2e})\n")

qae_results = []
for eps in QAE_EPSILONS:
    price_q, ci_q, elapsed_q, M = quantum_digital_call(
        S0, K, r, sigma, T, QAE_N_QUBITS, epsilon=eps, alpha=QAE_ALPHA
    )
    err_grid  = abs(price_q - grid_true_price)
    err_exact = abs(price_q - ref)
    qae_results.append((M, err_grid))
    print(f"  eps={eps:.3f}  M={M:>5}  qae={price_q:.6f}  "
          f"err_grid={err_grid:.2e}  err_exact={err_exact:.2e}  ({elapsed_q:.1f}s)")

qae_M, qae_err = zip(*sorted(qae_results))
print()

# ── Section G: Printed table ───────────────────────────────────────────────────
print("--- Digital Convergence Slopes (paste into paper) ---")
print(f"Note: N ∈ [256, 65536]; NOT cross-comparable to Tables IV/V (Asian, N ∈ [1024, 16384])")
print(f"Note: Antithetic MC slope may be inflated by ATM symmetry — see text.\n")
print(f"{'Method':<20} | {'Slope (95% CI)':<24}")
print("-" * 48)
for m in methods:
    atm = "  *" if m == "Antithetic MC" else ""
    print(f"  {m:<18}  {central[m]:+.3f} [{ci_lo[m]:+.3f}, {ci_hi[m]:+.3f}]{atm}")

print(f"\nQAE (IQAE, n={QAE_N_QUBITS}) oracle queries M vs |err vs grid_true_price|:")
for M, err in zip(qae_M, qae_err):
    print(f"  M={M:>5}  err={err:.2e}")
print(f"\nQAE grid bias (n={QAE_N_QUBITS}): {grid_bias_n5:.2e}  (systematic offset vs continuous exact)")

# ── Figure ─────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))

for m in methods:
    mean_curve = errs[m].mean(axis=0)
    label = f"{m}  (slope {central[m]:+.2f} [{ci_lo[m]:+.2f},{ci_hi[m]:+.2f}])"
    ax.loglog(N_VALUES, mean_curve, color=colors[m], marker=markers[m],
              linewidth=2.0, markersize=6, label=label, zorder=3)

ax.scatter(qae_M, qae_err, color="#ff7f0e", marker="D", s=60, zorder=4,
           label=f"QAE IQAE n={QAE_N_QUBITS} (vs grid exact)")

# Reference lines anchored at naive MC first point
anchor_y = errs["Naive MC"].mean(axis=0)[0]
anchor_N = N_VALUES[0]
ref_N    = np.array([N_VALUES[0], N_VALUES[-1]], dtype=float)
ax.loglog(ref_N, anchor_y * (anchor_N / ref_N)**0.5, "k--", linewidth=1.2,
          alpha=0.55, label=r"$O(1/\sqrt{N})$ — classical limit")
ax.loglog(ref_N, anchor_y * (anchor_N / ref_N)**1.0, "k:",  linewidth=1.2,
          alpha=0.55, label=r"$O(1/N)$ — quantum-parity scaling")

ax.set_xlabel("Budget  (paths N for MC/RQMC;  oracle queries M for QAE)", fontsize=11)
ax.set_ylabel("Mean absolute error  |price − reference|", fontsize=11)
ax.set_title(
    "Digital Option Convergence: MC vs RQMC vs QAE  [cash-or-nothing call]\n"
    r"$\it{N\ range\ differs\ from\ Tables\ IV/V\ —\ slopes\ not\ cross-comparable}$",
    fontsize=11, pad=10)
ax.legend(fontsize=8.5, framealpha=0.9)
ax.grid(True, which="both", alpha=0.3)

plt.tight_layout()
out_path = os.path.join(os.path.dirname(__file__), "..", "figures",
                        "fig_digital_convergence.png")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
fig.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"\nSaved: {os.path.normpath(out_path)}")
plt.close(fig)
```

- [ ] **Step 23: Run the full script (allow 20–35 min)**

Confirm scipy first:
```
venv\Scripts\python.exe -c "import scipy; print(scipy.__version__)"
```
Must print `1.13.1` — stop if it doesn't.

```
venv\Scripts\python.exe src\plot_digital_convergence.py
```

Section E runs in ~2–5 min. Section F (7 QAE points at n=5) runs in ~15–25 min. Do not kill the process.

- [ ] **Step 24: Verify all seven criteria from the spec**

After the script completes, check each criterion in order:

**1. MC sanity passes** — Section A output must show `PASS`, not `AssertionError`.

**2. D1 normalization asserts pass** — no `AssertionError` about `grid_probs.sum()`. Printed sums should be `1.0000000000`.

**3. D1 bias monotone** — `bias(n=4) < bias(n=3)` and `bias(n=5) < bias(n=4)`. Expected: `1.00e-01 → 6.18e-02 → 2.16e-02`.

**4. D2 step encoding** — `PASS` line must appear with `diff < 1e-6`.

**5. Slopes printed in Section G** — 3 rows with numeric `slope [lo, hi]` for all methods.

**6. Figure saved** — check timestamp:
```
(Get-Item figures\fig_digital_convergence.png).LastWriteTime
```
Must be within the last few minutes.

**7. Reproducibility** — re-run once:
```
venv\Scripts\python.exe src\plot_digital_convergence.py
```
Classical slopes (Section G) must be bit-identical. QAE M values must match (deterministic statevector).

- [ ] **Step 25: Run full test suite — no regressions**

```
venv\Scripts\pytest.exe tests\ -v
```

Expected: all tests pass (Qiskit tests may skip with `pytest.importorskip` if not installed — that is fine).

- [ ] **Step 26: Final commit**

```
git add src\plot_digital_convergence.py figures\fig_digital_convergence.png
git commit -m "feat: add European digital option convergence experiment (Paper B, MC vs RQMC vs QAE)"
```

---

## Self-Review

**Spec coverage:**

| Spec requirement | Task |
|---|---|
| `digital_bs_price` added to `black_scholes.py` | Task 1 Step 3 |
| `digital_mc`, `digital_antithetic_mc`, `digital_rqmc` in new module | Task 2 Step 9 |
| ATM watch-item docstring in `digital_antithetic_mc` | Task 2 Step 9 |
| `_build_digital_circuit` with `LinearAmplitudeFunction` step function | Task 3 Step 15 |
| `post_processing = lambda a: a` (identity, not a**2) | Task 3 Step 15 |
| `quantum_digital_call` docstring notes grid bias / post_processing reasoning | Task 3 Step 15 |
| sigma clamp inherited in `_build_digital_circuit` | Task 3 Step 15 |
| Section D1: normalization assert + bias monotone | Task 4 Step 19 |
| Section D2: statevector step encoding assert (load-bearing) | Task 4 Step 19 |
| Section D3: `grid_true_price` computed classically from `._probabilities` | Task 4 Step 19 |
| Checkpoint after D — stop for review before sweep | Task 4 Step 20 |
| Section E: classical sweep with exact seeds `seed=t`, `seed=t*1000` | Task 5 Step 22 |
| Bootstrap CI: 2000 resamples, `boot_rng=np.random.default_rng(0)` | Task 5 Step 22 |
| Section F: QAE error vs `grid_true_price`, NOT continuous exact | Task 5 Step 22 |
| Grid bias reported separately in Section F and Section G | Task 5 Step 22 |
| Section G table: cross-comparability note, ATM watch-item flag | Task 5 Step 22 |
| Figure: white background, 4 series, reference lines, correct title | Task 5 Step 22 |
| Reproducibility verified with re-run | Task 5 Step 24 |
| No changes to existing pricers (`quantum_call`, `monte_carlo_call`, etc.) | Enforced throughout |

**Placeholder scan:** No TBD/TODO in any code block. All commands have expected outputs. All function bodies are complete.

**Type consistency:**
- `digital_bs_price` returns `float` — used as `ref = digital_bs_price(...)` ✓
- `digital_mc`, `digital_antithetic_mc`, `digital_rqmc` return `(float, float)` — destructured as `price, se = ...` ✓
- `_build_digital_circuit` returns `(QuantumCircuit, int)` — destructured as `full_circuit, objective_qubit = ...` ✓
- `quantum_digital_call` returns `(float, tuple[float,float], float, int)` — destructured as `price_q, ci_q, elapsed_q, M = ...` ✓
- `errs[m]` shape `(N_TRIALS, len(N_VALUES))` — `.mean(axis=0)` gives `(len(N_VALUES),)` for polyfit ✓
- `grid_true_price` computed in Section D3, used in Section F: both in same script scope ✓
- `qae_M`, `qae_err` from `zip(*sorted(qae_results))`: types are tuples of `(int, float)` — plotted as scatter ✓
