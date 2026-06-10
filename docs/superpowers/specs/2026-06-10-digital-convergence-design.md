---
title: European Digital Option Convergence Experiment — MC vs RQMC vs QAE
date: 2026-06-10
status: approved
---

# European Digital Option Convergence Experiment

## Scientific Question

Does QAE's quadratic convergence advantage survive on a **discontinuous payoff**?
The European cash-or-nothing call pays 1 if S_T > K, else 0 — a jump discontinuity
at the strike. RQMC's scrambled-net theory (Owen 1997, Koksma-Hlawka) assumes
bounded variation; a step discontinuity formally violates this.

The experiment measures empirical convergence slopes for Naive MC, Antithetic MC,
RQMC (Sobol), and QAE (IQAE) on identical parameters, placing all four on the
break-even framing from Paper B Section III.

**Three possible outcomes — weighted equally:**

- **(a)** RQMC empirical slope ≈ −0.5 — discontinuity fully degrades scrambling to
  MC rate; QAE's quadratic advantage re-emerges relative to RQMC.
- **(b)** RQMC slope stays steep (≈ −1.0 or steeper) — Owen scrambling is more
  robust than theory guarantees for the 1D case; QAE still loses scaling parity.
- **(c)** High binary-payoff variance (Bernoulli) makes the slope fit underpowered
  — all three classical methods produce wide bootstrap CIs, result inconclusive.

**Cross-comparability note**: N ∈ [256, 65536] here; Tables IV/V use
N ∈ [1024, 16384] on Asian payoffs. Slopes measured here are **not
cross-comparable** to Tables IV/V. The paper must not imply otherwise.

---

## Files Changed

| File | Change |
|---|---|
| `src/black_scholes.py` | Add `digital_bs_price()` — one function, ~6 lines |
| `src/digital_option.py` | New: `digital_mc()`, `digital_antithetic_mc()`, `digital_rqmc()` |
| `src/quantum.py` | Add `_build_digital_circuit()`, `quantum_digital_call()` — no existing code touched |
| `src/plot_digital_convergence.py` | New experiment script |
| `figures/fig_digital_convergence.png` | New output figure |

---

## Reference Value

```python
def digital_bs_price(S0, K, r, sigma, T) -> float:
    d2 = (np.log(S0/K) + (r - 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    return np.exp(-r*T) * norm.cdf(d2)
```

Exact Black-Scholes digital call price — no control variate needed.
Added to `src/black_scholes.py` alongside `black_scholes_call()`.

At standard params (S0=K=100, r=0.05, σ=0.2, T=1.0):
`digital_bs_price = 0.532325`, `N(d₂) = P(S_T > K) = 0.559618`.

---

## `src/digital_option.py` — Function Signatures

```python
def digital_mc(S0, K, r, sigma, T, N, seed=None) -> tuple[float, float]:
    """Naive MC digital call. Payoff = (S_T > K).astype(float).
    Returns (price, std_err)."""

def digital_antithetic_mc(S0, K, r, sigma, T, N, seed=None) -> tuple[float, float]:
    """Antithetic pairs on binary payoff. N/2 antithetic pairs.
    std_err from paired-average std dev / sqrt(N/2). Returns (price, std_err).

    ATM watch-item: at S0=K=100 (our standard params), Z and −Z straddle the
    threshold symmetrically. paired_avg = 0.5*(1(Z>t) + 1(−Z>t)) concentrates
    near 0.5 for |Z| > |t|, suppressing variance by ~3× vs naive MC. This
    may produce an artificially steep slope specific to ATM symmetry rather
    than genuine convergence improvement. Antithetic slope should be
    interpreted cautiously and not generalized to non-ATM strikes."""

def digital_rqmc(S0, K, r, sigma, T, N, n_replications=30, seed=None) -> tuple[float, float]:
    """RQMC digital call. Scrambled Sobol d=1.
    std_err estimated from replication variance. Returns (price, std_err)."""
```

All three are structurally identical to their call counterparts in
`variance_reduced_mc.py`, with `np.maximum(S_T - K, 0)` replaced by
`(S_T > K).astype(float)`. Seed conventions match exactly (`seed=t` for
naive/antithetic, `seed=t*1000` for RQMC) so draws are directly comparable
across payoff types.

---

## `src/quantum.py` Additions

### `_build_digital_circuit`

```python
def _build_digital_circuit(
    S0: float, K: float, r: float, sigma: float, T: float,
    num_uncertainty_qubits: int = 5,
) -> tuple[QuantumCircuit, int]:
```

Returns `(full_circuit, objective_qubit_index)`. The `objective_qubit_index`
is always `num_uncertainty_qubits`.

**Preamble** (identical to `_build_circuit`):
- Same `sigma` clamp: `sigma = max(sigma, 0.15)`
- Same `mu_ln`, `sigma_var`, `bounds` computation
- Same `LogNormalDistribution` construction

**Oracle** (replaces `EuropeanCallPricingObjective`):

```python
from qiskit.circuit.library import LinearAmplitudeFunction
digital_obj = LinearAmplitudeFunction(
    num_state_qubits=num_uncertainty_qubits,
    slope=[0, 0],        # constant in both intervals
    offset=[0, 1],       # 0 below K, 1 at/above K
    domain=(low, high),
    image=(0, 1),
    breakpoints=[low, K],  # K on the ≥ side → pays 1 at S_T = K
    rescaling_factor=1.0,
)
```

**Why `rescaling_factor=1.0` is correct and exact:**
For the binary payoff f ∈ {0, 1}, the circuit applies `Ry(2·arcsin(sqrt(c·f)))`:
- f=0: `Ry(0)` → P(obj=|1⟩) = 0
- f=1, c=1: `Ry(π)` → P(obj=|1⟩) = 1

Therefore `P(obj=|1⟩) = E[f(x)] = grid_p` — exact, no Woerner approximation.
Empirically confirmed: `Statevector(full_circuit).probabilities()` marginalized
over the objective qubit equals `grid_p` to numerical precision (see Section D).

### Critical: custom `post_processing`

`LinearAmplitudeFunction.post_processing` is NOT appropriate for this circuit.
Its formula `(a − 0.5 + π·c/4) · 2/(π·c)` is designed for a Taylor approximation
inverse and does not recover P(S>K) from the IQAE estimate.

**How IQAE reports values in Qiskit 0.3.1 (empirically confirmed):**
`result.estimation` = `P(obj=|1⟩)` **directly** (the probability, not the amplitude
`sqrt(P(obj=|1⟩))`). Verified: at n=5, `result.estimation = 0.536897 = grid_p`
exactly. This means `post_processing = lambda a: a**2` would return `grid_p²
≈ 0.288`, which is wrong. `LinearAmplitudeFunction.post_processing(grid_p)
= 0.524 ≠ grid_p`, also wrong.

**Correct post_processing** is identity:

```python
# In quantum_digital_call, NOT in _build_digital_circuit:
post_processing = lambda a: a   # IQAE returns P(obj=1) = grid_p directly
```

**CI behavior confirmed** (Qiskit 0.3.1): `IterativeAmplitudeEstimation.estimate`
applies `post_processing` elementwise to both CI bounds automatically:
`confidence_interval_processed = (pp(ci_lo), pp(ci_hi))`. With identity
post_processing, CI bounds are already in probability space; multiply by discount
to get price CI. Verified by inspecting `IterativeAmplitudeEstimation.estimate`
source: `confidence_interval = tuple(estimation_problem.post_processing(x) for x in
confidence_interval)`.

Price and CI in `quantum_digital_call`:
```python
price    = result.estimation_processed * discount         # grid_p * discount
conf_int = (result.confidence_interval_processed[0] * discount,
            result.confidence_interval_processed[1] * discount)
```

### `quantum_digital_call`

```python
def quantum_digital_call(
    S0: float, K: float, r: float, sigma: float, T: float,
    num_uncertainty_qubits: int = 5,
    epsilon: float = 0.01,
    alpha: float = 0.05,
) -> tuple[float, tuple[float, float], float, int]:
    """
    Price a European digital (cash-or-nothing) call via IQAE.

    Returns
    -------
    price          : float — discounted P(S_T > K on n-qubit grid)
    conf_int       : (float, float) — (1-alpha) CI on the price
    elapsed        : float — wall-clock seconds
    oracle_queries : int — sum(2k+1 for k in result.powers)

    Note: price converges to grid_true_price (the discretized price at
    num_uncertainty_qubits), NOT to the continuous digital_bs_price.
    Grid bias = |grid_true_price − digital_bs_price| is a systematic
    offset that does NOT shrink with epsilon. Compute grid_true_price
    separately via LogNormalDistribution._values / ._probabilities
    and use it as the convergence reference in the epsilon sweep.
    """
```

Uses `EstimationProblem(post_processing=lambda a: a)`. Price is
`result.estimation_processed * discount` = `grid_p * discount`.

---

## `src/plot_digital_convergence.py` — Script Structure

### Constants

```python
S0, K, r, sigma, T = 100.0, 100.0, 0.05, 0.2, 1.0

N_VALUES      = [2**i for i in range(8, 17)]   # 256 → 65536  (9 points, d=1)
N_TRIALS      = 10
N_REP         = 30
N_BOOT        = 2000
CI            = (2.5, 97.5)
N_SANITY      = 1_000_000

QAE_N_QUBITS  = 5                              # validated in Section D
QAE_EPSILONS  = [0.001, 0.002, 0.004, 0.007, 0.010, 0.015, 0.020]
QAE_ALPHA     = 0.05
```

---

### Section A — Exact reference and MC sanity check

```python
ref = digital_bs_price(S0, K, r, sigma, T)
print(f"Exact digital BS price: {ref:.6f}")

mc_price, mc_se = digital_mc(S0, K, r, sigma, T, N_SANITY, seed=0)
assert abs(mc_price - ref) < 5 * mc_se, "MC sanity failed"
print(f"MC sanity: |mc − exact| = {abs(mc_price - ref):.2e},  5σ = {5*mc_se:.2e}")
```

---

### Section D — QAE Discretization Validation (Mandatory Gate)

If any assert fails, the script aborts with a diagnostic message. This section
runs before any convergence sweep.

**D1 — Grid bias shrinks with n**

For `n ∈ {3, 4, 5}` using only `LogNormalDistribution._values` and `._probabilities`
(no quantum circuit or IQAE required):

```python
from qiskit_finance.circuit.library import LogNormalDistribution
# (same bounds logic as _build_digital_circuit)

for n in [3, 4, 5]:
    lnd = LogNormalDistribution(n, mu=mu_ln, sigma=sigma_var, bounds=(low, high))
    x_grid = np.array(lnd._values)        # 2^n evenly spaced points, linspace(low, high, 2^n)
    grid_probs = np.array(lnd._probabilities)  # normalized log-normal mass at each point
    # Normalization guard: grid_true_price is computed from these private attributes.
    # A silent renormalization change in a Qiskit update would corrupt the reference.
    assert np.isclose(grid_probs.sum(), 1.0), \
        f"n={n}: lnd._probabilities sums to {grid_probs.sum():.8f}, not 1.0"
    grid_p = np.dot(grid_probs, (x_grid > K).astype(float))
    grid_price = np.exp(-r*T) * grid_p
    bias = abs(grid_price - ref)
    print(f"  n={n}: grid_price={grid_price:.6f}  exact={ref:.6f}  bias={bias:.2e}")
```

Expected (standard params, empirically confirmed):
- n=3: bias ≈ 1.00e-01
- n=4: bias ≈ 6.18e-02
- n=5: bias ≈ 2.16e-02

Assert `bias(n=4) < bias(n=3)` and `bias(n=5) < bias(n=4)`. If either fails:
"ABORT — grid bias not monotone-decreasing with n; check bounds / LogNormal params."

**D2 — Step encoding correctness (load-bearing)**

Build the n=3 digital circuit and extract the statevector. This is the only check
that validates `LinearAmplitudeFunction` with `slope=[0,0]`, `offset=[0,1]`,
`image=(0,1)`, `rescaling_factor=1.0` correctly encodes the step function. If
`image=(0,1)` is silently renormalized by the slope/offset/domain combination,
this assert is the only thing that catches it.

```python
from qiskit.quantum_info import Statevector
n = 3
full_circ, _ = _build_digital_circuit(S0, K, r, sigma, T, n)
sv_probs = np.abs(np.array(Statevector(full_circ)))**2
prob_obj1 = sum(sv_probs[i] for i in range(len(sv_probs)) if (i >> n) & 1)
# Compare against grid P(S > K) at n=3
lnd3 = LogNormalDistribution(3, mu=mu_ln, sigma=sigma_var, bounds=(low, high))
grid_p_n3 = np.dot(lnd3._probabilities, (np.array(lnd3._values) > K).astype(float))
assert abs(prob_obj1 - grid_p_n3) < 1e-6, \
    f"Step encoding mismatch: sv P(obj=1)={prob_obj1:.6f} vs grid_p={grid_p_n3:.6f}"
print(f"  D2 PASS: sv P(obj=1) = {prob_obj1:.6f}  grid_p = {grid_p_n3:.6f}")
```

**D3 — Compute `grid_true_price` for n=5 (used in Section F)**

```python
lnd5 = LogNormalDistribution(QAE_N_QUBITS, mu=mu_ln, sigma=sigma_var, bounds=(low, high))
grid_p_n5 = np.dot(lnd5._probabilities, (np.array(lnd5._values) > K).astype(float))
grid_true_price = np.exp(-r*T) * grid_p_n5
grid_bias_n5 = abs(grid_true_price - ref)
print(f"  n=5 grid_true_price={grid_true_price:.6f}  exact={ref:.6f}  grid_bias={grid_bias_n5:.2e}")
```

`grid_true_price` is the value QAE (at n=5) converges to as epsilon → 0.
It is computed classically and stored for use in Section F.

---

### Section E — Classical Convergence Sweep

```python
methods = ["Naive MC", "Antithetic MC", "RQMC"]
errs = {m: np.zeros((N_TRIALS, len(N_VALUES))) for m in methods}

for j, N in enumerate(N_VALUES):
    for t in range(N_TRIALS):
        p_naive, _ = digital_mc(S0, K, r, sigma, T, N, seed=t)
        p_anti,  _ = digital_antithetic_mc(S0, K, r, sigma, T, N, seed=t)
        p_rqmc,  _ = digital_rqmc(S0, K, r, sigma, T, N, n_replications=N_REP, seed=t*1000)
        errs["Naive MC"][t, j]      = abs(p_naive - ref)
        errs["Antithetic MC"][t, j] = abs(p_anti  - ref)
        errs["RQMC"][t, j]          = abs(p_rqmc  - ref)
```

Classical methods compare against `ref` (continuous `digital_bs_price`).

Bootstrap CI: identical to `plot_dimension_sweep.py` — resample 10 trial indices
2000 times, refit slope-of-mean each resample, 2.5th/97.5th percentile.
`boot_rng = np.random.default_rng(0)` (fixed → reproducible CIs).

---

### Section F — QAE Epsilon Sweep

```python
qae_results = []
for eps in QAE_EPSILONS:
    price, ci, elapsed, M = quantum_digital_call(
        S0, K, r, sigma, T, QAE_N_QUBITS, epsilon=eps, alpha=QAE_ALPHA
    )
    qae_err = abs(price - grid_true_price)   # error vs grid value, NOT continuous exact
    qae_results.append((M, qae_err))
    print(f"  eps={eps:.3f}  M={M:>5}  qae={price:.6f}  err_grid={qae_err:.2e}  err_exact={abs(price-ref):.2e}")

qae_M, qae_err = zip(*sorted(qae_results))
```

**Why error is measured against `grid_true_price`, not `ref`:**
As epsilon shrinks, IQAE converges to `grid_true_price` (the exact value on the
n=5 grid), not to `ref` (the continuous closed form). If `ref` is used as the
target, QAE error floors at `grid_bias_n5 ≈ 2.16e-02` even at epsilon=0.001,
creating a false impression that QAE "stops converging." Using `grid_true_price`
isolates QAE's estimation convergence from the fixed grid bias.

The grid bias is a known systematic offset, reported separately:
`print(f"QAE grid bias (n={QAE_N_QUBITS}): {grid_bias_n5:.2e}")`.

QAE is deterministic in statevector mode — no bootstrap CI needed or applicable.

---

### Section G — Printed Table

```
--- Digital Convergence Slopes (paste into paper) ---
Note: N ∈ [256, 65536], NOT cross-comparable to Tables IV/V (Asian, N ∈ [1024, 16384]).
Note: Antithetic MC slope may be inflated by ATM symmetry — see text.

Method          | Slope (95% CI)
Naive MC        | -X.XX [-X.XX, -X.XX]
Antithetic MC   | -X.XX [-X.XX, -X.XX]  * ATM symmetry watch-item
RQMC            | -X.XX [-X.XX, -X.XX]

QAE (IQAE, n=5) — oracle queries M vs |error vs grid_true_price|:
  M=XXXX  err=X.XXe-XX  (epsilon=0.020)
  ...
QAE grid bias (n=5): X.XXe-02  (systematic offset vs continuous exact)
```

---

## Figure Design

Single panel, white background (journal-standard, matching
`fig_rqmc_dimension_decay.png`).

- **X-axis**: "Budget (paths N for MC/RQMC; oracle queries M for QAE)"
- **Y-axis**: Mean absolute error |price − reference|
- **3 classical series**: Naive MC, Antithetic MC, RQMC — error vs `ref`
  (continuous exact), fitted slopes in legend labels
- **1 QAE series**: orange diamonds, error vs `grid_true_price`, scatter only
  (no slope fit — 7 deterministic points; note in legend: "vs grid exact")
- **Reference lines**: dashed `O(1/√N)`, dotted `O(1/N)`
- **Annotation** on RQMC: if CI straddles −0.75, note "ambiguous; see outcomes
  (a)/(b) in text"
- **File**: `figures/fig_digital_convergence.png`, dpi=150

---

## Verification Criteria

1. **MC sanity check passes**: `|digital_mc(N=10^6) − ref| < 5 × mc_se`
2. **Grid bias monotone-decreasing**: `bias(n=4) < bias(n=3)` and `bias(n=5) < bias(n=4)`
3. **Step encoding exact**: `|sv P(obj=1) − grid_p_n3| < 1e-6` (D2 assert)
4. **Reproducibility**: all seeds fixed (`seed=t`, `seed=t*1000`,
   `boot_rng=np.random.default_rng(0)`, QAE statevector is deterministic)
5. **No changes to existing pricers**: `quantum_call`, `monte_carlo_call`,
   `black_scholes_call`, all `asian_option.py` functions unchanged
6. **Figure saved**: `figures/fig_digital_convergence.png` timestamp updated
7. **Cross-comparability note present** in printed table header and figure caption

---

## Parameters

```python
S0, K, r, sigma, T = 100.0, 100.0, 0.05, 0.2, 1.0
```

Matches the rest of Paper B. ATM chosen deliberately to activate the antithetic
watch-item (see `digital_antithetic_mc` docstring).

---

## Key Technical Findings (from pre-spec validation)

**Finding 1 — IQAE reports probability, not amplitude.**
In Qiskit 0.3.1 (statevector Sampler), `result.estimation = P(obj=|1⟩)` directly.
Empirically confirmed at n=5: `result.estimation = 0.536897 = grid_p`. The correct
`post_processing` is therefore `lambda a: a` (identity); `lambda a: a**2` would
return `grid_p² ≈ 0.288`, silently wrong.

**Finding 2 — `LinearAmplitudeFunction.post_processing` is wrong for this oracle.**
The library function applies `(a − 0.5 + π/4) · (2/π)` — appropriate for its
internal Taylor approximation but incorrect for the digital step encoding:

| n | `digital_obj.post_processing(grid_p)` | actual `grid_p` |
|---|---|---|
| 3 | 0.471 | 0.454 |
| 5 | 0.523 | 0.537 |

Both off by ~3–4%. Using the library default would introduce a systematic
pricing error comparable to the grid bias itself.

**Finding 3 — Step encoding is exact.**
`sv P(obj=1) = grid_p` to numerical precision (< 1e-6). The circuit correctly
encodes the digital payoff with `rescaling_factor=1.0`.

**Finding 4 — CI bounds auto-squashed by Qiskit.**
Qiskit 0.3.1 applies `post_processing` elementwise to CI bounds automatically
(confirmed in source). With identity post_processing, CI is already in
probability space; multiply by discount to get the price CI.

---

## Runtime Estimate

- Section A (MC sanity, N=10^6): ~2 s
- Section D (validation, statevector n=3): ~10–30 s
- Section E (classical sweep, 9 N-values × 10 trials × 30 reps): ~2–5 min
- Section F (QAE sweep, 7 epsilons at n=5, statevector IQAE): ~10–20 min
- Total: ~15–25 min
