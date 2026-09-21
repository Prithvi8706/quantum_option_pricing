# Arithmetic Asian RQMC Dimension-Decay Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `arithmetic_asian_cv_ref()` to `asian_option.py` and create `plot_arithmetic_asian_decay.py` — the arithmetic counterpart to the geometric sweep in Table IV — using a geometric control-variate reference so the noise floor is far below RQMC accuracy.

**Architecture:** One new function in `asian_option.py` (uses `simulate_paths` + `geometric_asian_closed_form`, both already present); one new script that is a direct mirror of `plot_dimension_sweep.py` with arithmetic pricers, the CV reference, a geometric sanity check gate (Sections A–B), and a noise-floor audit (Section D). No shared harness module; duplication is intentional for experiment provenance.

**Tech Stack:** Python 3, NumPy, SciPy (`qmc`, `norm`), Matplotlib, pytest (venv-pinned, scipy==1.13.1)

---

## File Map

| Path | Action | Responsibility |
|---|---|---|
| `src/asian_option.py` | Modify (append) | Add `arithmetic_asian_cv_ref()` after existing geometric helpers, before `if __name__` block |
| `tests/test_asian_cv_ref.py` | Create | Unit tests for the new reference function |
| `src/plot_arithmetic_asian_decay.py` | Create | Full sweep script: sanity check → references → sweep → noise-floor → table → figure |
| `figures/fig_arithmetic_asian_decay.png` | Create (output) | Written by the script on execution |

---

## Task 1: Write failing tests for `arithmetic_asian_cv_ref`

**Files:**
- Create: `tests/test_asian_cv_ref.py`

- [ ] **Step 1: Create the test file**

```python
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
```

- [ ] **Step 2: Run tests — verify all three FAIL with ImportError**

```
venv\Scripts\pytest.exe tests\test_asian_cv_ref.py -v
```

Expected output (all three FAIL):
```
FAILED tests/test_asian_cv_ref.py::test_cv_ref_price_between_geo_and_european
FAILED tests/test_asian_cv_ref.py::test_cv_ref_se_much_smaller_than_naive
FAILED tests/test_asian_cv_ref.py::test_cv_ref_reproducible_with_seed
ImportError: cannot import name 'arithmetic_asian_cv_ref'
```

---

## Task 2: Implement `arithmetic_asian_cv_ref`, run tests

**Files:**
- Modify: `src/asian_option.py` — append new function before the `if __name__ == "__main__":` block (currently line 163)

- [ ] **Step 3: Add the function to `asian_option.py`**

Insert the following block immediately before `if __name__ == "__main__":` (i.e., after the `asian_geometric_rqmc` function body, which ends around line 161):

```python
def arithmetic_asian_cv_ref(S0, K, r, sigma, T, d, N_ref=4_194_304, seed=None):
    """
    Control-variate reference price for the arithmetic-average Asian call.

    Estimate = MC[ arith_payoff(Z) - geo_payoff(Z) ] * discount
               + geometric_asian_closed_form(S0, K, r, sigma, T, d)

    Both payoffs are computed from the same Z matrix; because arithmetic and
    geometric averages are highly correlated on identical paths, the difference
    has far lower variance than either payoff alone.

    With N_ref = 2^22 = 4,194,304 the residual SE is typically < 1e-4, far
    below any RQMC error in the dimension-decay sweep.

    Prints reference price and SE on every call so callers can verify the
    noise floor before trusting measured convergence slopes.

    Parameters
    ----------
    N_ref : int
        MC budget for the difference estimator. Use >= 4_000_000 to keep
        residual SE below the sweep noise floor; default is 2^22 = 4_194_304.
    seed : int or None
        RNG seed. Fix to reproduce the reference across runs.

    Returns
    -------
    price : float
        Estimated arithmetic Asian call price.
    se : float
        Standard error of the difference estimator — the residual noise in
        the reference value, not the SE of any sweep estimator.
    """
    rng     = np.random.default_rng(seed)
    Z       = rng.standard_normal((N_ref, d))
    S_paths = simulate_paths(S0, r, sigma, T, Z)
    discount = np.exp(-r * T)

    arith  = np.maximum(S_paths.mean(axis=1) - K, 0.0)
    G      = np.exp(np.log(S_paths).mean(axis=1))   # geometric mean of price levels
    geo    = np.maximum(G - K, 0.0)

    diff   = arith - geo
    se     = discount * diff.std(ddof=1) / np.sqrt(N_ref)
    geo_cf = geometric_asian_closed_form(S0, K, r, sigma, T, d)
    price  = discount * diff.mean() + geo_cf

    print(f"  [ref d={d:>2}]  price={price:.6f}  SE={se:.2e}  geo_exact={geo_cf:.6f}")
    return price, se
```

- [ ] **Step 4: Run the tests — verify all three PASS**

```
venv\Scripts\pytest.exe tests\test_asian_cv_ref.py -v
```

Expected:
```
PASSED tests/test_asian_cv_ref.py::test_cv_ref_price_between_geo_and_european
PASSED tests/test_asian_cv_ref.py::test_cv_ref_se_much_smaller_than_naive
PASSED tests/test_asian_cv_ref.py::test_cv_ref_reproducible_with_seed
3 passed
```

- [ ] **Step 5: Run existing tests — confirm no regressions**

```
venv\Scripts\pytest.exe tests\test_pricing.py -v
```

Expected: all tests that were passing before still pass (Qiskit tests may skip — that's fine).

- [ ] **Step 6: Commit**

```
git add src\asian_option.py tests\test_asian_cv_ref.py
git commit -m "feat: add arithmetic_asian_cv_ref control-variate reference to asian_option.py"
```

---

## Task 3: Create `plot_arithmetic_asian_decay.py` — Sections A and B only

Build and gate-check the script incrementally. In this task, write only Sections A (geometric sanity) and B (reference building), then run to confirm both pass before adding the slow sweep.

**Files:**
- Create: `src/plot_arithmetic_asian_decay.py`

- [ ] **Step 7: Create the script with Sections A and B**

```python
"""
Dimension-decay sweep for Paper B, Section VI-B / Table V / Fig. 3.

Arithmetic-average Asian call, geometric control-variate reference.

Direct mirror of plot_dimension_sweep.py (geometric). Same harness, same config
(10 trials / 30 reps / 2000 bootstrap resamples), same figure style. Differences:
  - payoff: arithmetic average (non-smooth, no closed form)
  - reference: geometric_asian_closed_form + MC[arith - geo] at N=2^22
  - output: Table V, fig_arithmetic_asian_decay.png

Scientific question (Section VI-B): does RQMC's O(1/N)-ish edge survive on
the non-smooth arithmetic payoff, or degrade relative to the geometric case?
"""
import os
import sys
import warnings

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
from black_scholes import black_scholes_call
from asian_option import (
    simulate_paths,
    geometric_asian_closed_form,
    arithmetic_asian_cv_ref,
    asian_geometric_rqmc,
    asian_naive_mc,
    asian_antithetic_mc,
    asian_rqmc,
)

warnings.filterwarnings("ignore", category=UserWarning)

S0, K, r, sigma, T = 100.0, 100.0, 0.05, 0.2, 1.0

# ── Config (parity with plot_dimension_sweep.py) ───────────────────────────────
N_REF    = 4_194_304            # 2^22 — reference MC budget
REF_SEED = 999                  # fixed → reproducible reference
DIMS     = [1, 2, 4, 8, 16, 32, 64]
N_VALUES = [2 ** i for i in range(10, 17)]   # 1024 → 65536
N_TRIALS = 10
N_REP    = 30
N_BOOT   = 2000
CI       = (2.5, 97.5)
log_N    = np.log10(N_VALUES)
boot_rng = np.random.default_rng(0)

# Published Table IV 95% bootstrap CIs for the RQMC geometric slope (spot-check)
GEO_RQMC_CI = {1: (-1.10, -0.80), 64: (-0.83, -0.60)}

# ── Section A: Geometric sanity check ─────────────────────────────────────────
print("=== Section A: Geometric sanity check ===\n")

# A1: geometric mean equivalence
Z_chk          = np.random.default_rng(42).standard_normal((1000, 4))
S_chk          = simulate_paths(S0, r, sigma, T, Z_chk)
dt             = T / 4
cumlog_chk     = np.cumsum((r - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*Z_chk, axis=1)
geo_via_log    = np.exp(np.log(S_chk).mean(axis=1))
geo_via_cumlog = S0 * np.exp(cumlog_chk.mean(axis=1))
max_diff       = np.max(np.abs(geo_via_log - geo_via_cumlog))
assert max_diff < 1e-10, (
    f"Geometric mean methods disagree: max diff = {max_diff:.2e}"
)
print(f"  A1 geometric mean equivalence: max diff = {max_diff:.2e}  OK\n")

# A2: RQMC slope spot-check
print("  A2 geometric RQMC slope spot-check:")
for d_chk in [1, 64]:
    ref_geo  = geometric_asian_closed_form(S0, K, r, sigma, T, d_chk)
    errs_chk = np.zeros((N_TRIALS, len(N_VALUES)))
    for j, N in enumerate(N_VALUES):
        for t in range(N_TRIALS):
            p, _ = asian_geometric_rqmc(
                S0, K, r, sigma, T, N, d_chk, n_replications=N_REP, seed=t * 1000
            )
            errs_chk[t, j] = abs(p - ref_geo)
    slope_chk = np.polyfit(log_N, np.log10(errs_chk.mean(axis=0)), 1)[0]
    lo, hi    = GEO_RQMC_CI[d_chk]
    status    = "PASS" if lo <= slope_chk <= hi else "FAIL"
    print(f"    d={d_chk}: RQMC slope = {slope_chk:.3f}  CI=[{lo}, {hi}]  [{status}]")
    assert status == "PASS", (
        f"Harness bug: d={d_chk} RQMC slope {slope_chk:.3f} outside "
        f"published CI [{lo}, {hi}] — stop and investigate"
    )

print("\n  All Section A checks passed.\n")

# ── Section B: Build arithmetic CV references ──────────────────────────────────
print("=== Section B: Arithmetic CV references ===\n")
refs    = {}
ref_ses = {}
for d in DIMS:
    price, se  = arithmetic_asian_cv_ref(
        S0, K, r, sigma, T, d, N_ref=N_REF, seed=REF_SEED
    )
    refs[d]    = price
    ref_ses[d] = se

print("\n  Section B complete.\n")

# ── Sections C-F: added in Task 4 ─────────────────────────────────────────────
print("Sections C-F not yet implemented.")
```

- [ ] **Step 8: Confirm scipy version, then run Sections A and B**

```
venv\Scripts\python.exe -c "import scipy; print(scipy.__version__)"
```

Expected: `1.13.1`

```
venv\Scripts\python.exe src\plot_arithmetic_asian_decay.py
```

Expected output (abridged):
```
=== Section A: Geometric sanity check ===

  A1 geometric mean equivalence: max diff = 0.00e+00  OK

  A2 geometric RQMC slope spot-check:
    d=1:  RQMC slope = -0.9xx  CI=[-1.10, -0.80]  [PASS]
    d=64: RQMC slope = -0.7xx  CI=[-0.83, -0.60]  [PASS]

  All Section A checks passed.

=== Section B: Arithmetic CV references ===

  [ref d= 1]  price=...  SE=...  geo_exact=...
  [ref d= 2]  price=...  SE=...  geo_exact=...
  ...
  [ref d=64]  price=...  SE=...  geo_exact=...

  Section B complete.

Sections C-F not yet implemented.
```

If Section A fails with AssertionError — **stop and paste the full traceback**. Do not proceed to Task 4.

- [ ] **Step 9: Commit the partial script**

```
git add src\plot_arithmetic_asian_decay.py
git commit -m "wip: add arithmetic Asian sweep script Sections A+B (sanity check + CV references)"
```

---

## Task 4: Add Sections C, D, E, F — sweep, noise floor, table, figure

**Files:**
- Modify: `src/plot_arithmetic_asian_decay.py` — replace the stub `print("Sections C-F not yet implemented.")` with the full sweep

- [ ] **Step 10: Replace the stub with Sections C–F**

Replace the final two lines of the file (`# ── Sections C-F ...` through `print("Sections C-F not yet implemented.")`) with:

```python
# ── Section C: Arithmetic sweep ────────────────────────────────────────────────
methods = ["Naive MC", "Antithetic MC", "RQMC"]
colors  = {"Naive MC": "#1f77b4", "Antithetic MC": "#2ca02c", "RQMC": "#9467bd"}
markers = {"Naive MC": "o", "Antithetic MC": "s", "RQMC": "D"}

central          = {m: [] for m in methods}
ci_lo            = {m: [] for m in methods}
ci_hi            = {m: [] for m in methods}
rqmc_errs_by_dim = {}

print(f"=== Section C: Arithmetic sweep "
      f"({N_TRIALS} trials, {N_REP} reps, {N_BOOT} bootstrap) ===\n")
print(f"{'d':>4} | {'Naive MC':>20} | {'Antithetic MC':>20} | {'RQMC':>20}")
print("-" * 74)

for d in DIMS:
    errs = {m: np.zeros((N_TRIALS, len(N_VALUES))) for m in methods}
    for j, N in enumerate(N_VALUES):
        for t in range(N_TRIALS):
            p_naive, _ = asian_naive_mc(S0, K, r, sigma, T, N, d, seed=t)
            p_anti,  _ = asian_antithetic_mc(S0, K, r, sigma, T, N, d, seed=t)
            p_rqmc,  _ = asian_rqmc(
                S0, K, r, sigma, T, N, d, n_replications=N_REP, seed=t * 1000
            )
            errs["Naive MC"][t, j]      = abs(p_naive - refs[d])
            errs["Antithetic MC"][t, j] = abs(p_anti  - refs[d])
            errs["RQMC"][t, j]          = abs(p_rqmc  - refs[d])

    rqmc_errs_by_dim[d] = errs["RQMC"]   # saved for Section D noise-floor check

    row = []
    for m in methods:
        mean_curve = errs[m].mean(axis=0)
        c = np.polyfit(log_N, np.log10(mean_curve), 1)[0]
        boot = np.empty(N_BOOT)
        for b in range(N_BOOT):
            idx     = boot_rng.integers(0, N_TRIALS, N_TRIALS)
            mc      = errs[m][idx].mean(axis=0)
            boot[b] = np.polyfit(log_N, np.log10(mc), 1)[0]
        lo, hi = np.percentile(boot, CI)
        central[m].append(c)
        ci_lo[m].append(lo)
        ci_hi[m].append(hi)
        row.append(f"{c:>6.3f} [{lo:>5.2f},{hi:>5.2f}]")

    print(f"{d:>4} | {row[0]:>20} | {row[1]:>20} | {row[2]:>20}")

# ── Section D: Noise floor check ───────────────────────────────────────────────
print("\n=== Section D: Noise floor check ===\n")
print(f"{'d':>4}  {'ref_SE':>10}  {'rqmc_err':>14}  {'ratio':>8}  {'N'}  {'flag'}")
print("-" * 62)
for d in DIMS:
    se           = ref_ses[d]
    err_small    = rqmc_errs_by_dim[d].mean(axis=0)[0]    # N=1024
    err_large    = rqmc_errs_by_dim[d].mean(axis=0)[-1]   # N=65536
    ratio_small  = se / err_small
    ratio_large  = se / err_large
    flag_small   = "  WARN: increase N_REF" if ratio_small >= 0.1 else "  ok"
    flag_large   = "  WARN: increase N_REF" if ratio_large >= 0.1 else "  ok"
    print(f"  {d:>4}  {se:>10.2e}  {err_small:>14.2e}  {ratio_small:>8.4f}  "
          f"N=1024  {flag_small}")
    print(f"  {' ':>4}  {' ':>10}  {err_large:>14.2e}  {ratio_large:>8.4f}  "
          f"N=65536 {flag_large}")

# ── Table V ────────────────────────────────────────────────────────────────────
print("\n--- Table V (paste into DOCX) ---")
print("| d | Naive MC | Antithetic | RQMC |")
print("|---|---|---|---|")
for i, d in enumerate(DIMS):
    def cell(m, i=i):
        return f"{central[m][i]:.2f} [{ci_lo[m][i]:.2f}, {ci_hi[m][i]:.2f}]"
    print(f"| {d} | {cell('Naive MC')} | {cell('Antithetic MC')} | {cell('RQMC')} |")

# ── Figure ─────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))

for m in methods:
    c  = np.array(central[m])
    lo = np.array(ci_lo[m])
    hi = np.array(ci_hi[m])
    ax.plot(DIMS, c, color=colors[m], marker=markers[m],
            linewidth=2.0, markersize=6, label=m, zorder=3)
    ax.fill_between(DIMS, lo, hi, color=colors[m], alpha=0.18, zorder=1)

ax.axhline(-1.0, color="#555555", linestyle="--", linewidth=1.0,
           label=r"$O(1/N)$ — quantum-parity scaling")
ax.axhline(-0.5, color="#555555", linestyle=":", linewidth=1.0,
           label=r"$O(1/\sqrt{N})$ — classical limit")

ax.set_xscale("log", base=2)
ax.set_xticks(DIMS)
ax.set_xticklabels([str(d) for d in DIMS])
ax.set_xlabel("Problem dimension  d  (monitoring dates)", fontsize=12)
ax.set_ylabel("Fitted convergence slope (95% CI band)", fontsize=12)
ax.set_title(
    "RQMC Advantage Decays with Dimension  "
    "[arithmetic Asian, geometric CV reference]",
    fontsize=12, pad=12)
ax.legend(fontsize=9, loc="lower right", framealpha=0.9)
ax.grid(True, which="both", alpha=0.3)
ax.set_ylim(-1.3, -0.1)

plt.tight_layout()
out_path = os.path.join(os.path.dirname(__file__), "..", "figures",
                        "fig_arithmetic_asian_decay.png")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
fig.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"\nSaved: {os.path.normpath(out_path)}")
plt.close(fig)
```

Note on the `cell()` closure: the `i=i` default-argument capture prevents the
loop-variable capture bug that would make all cells print the last `i`. The
geometric sweep has this same pattern; match it exactly.

- [ ] **Step 11: Run the full script (allow 10–15 min)**

Confirm scipy first:
```
venv\Scripts\python.exe -c "import scipy; print(scipy.__version__)"
```
Must print `1.13.1` — stop if it doesn't.

```
venv\Scripts\python.exe src\plot_arithmetic_asian_decay.py
```

Let it run to completion. Do not kill it — the d=64 RQMC case is slow (30 reps × 10 trials × 7 N-values).

- [ ] **Step 12: Verify all six criteria from the spec**

After the script finishes, check each criterion in order:

**1. Section A PASSes** — output must show:
```
  A1 geometric mean equivalence: max diff = 0.00e+00  OK
  A2 geometric RQMC slope spot-check:
    d=1:  ... [PASS]
    d=64: ... [PASS]
  All Section A checks passed.
```
If either `[FAIL]` appears or an AssertionError is raised — stop, paste the traceback.

**2. Section D — no WARN flags** — all eight rows (7 dims × {N=1024, N=65536}) must show `ok`, not `WARN`. If any WARN appears — stop; N_REF must be increased before the results are trusted.

**3. Table V is printed** — 7 rows with numeric slopes and CIs.

**4. Figure saved** — check the timestamp:
```
(Get-Item figures\fig_arithmetic_asian_decay.png).LastWriteTime
```
Must be within the last few minutes.

**5. Reproducibility spot-check** — re-run once:
```
venv\Scripts\python.exe src\plot_arithmetic_asian_decay.py
```
Table V slopes must be bit-identical to the first run (all seeds fixed).

**6. No changes to existing pricers** — confirm:
```
git diff HEAD~1 src\asian_option.py
```
Only the new `arithmetic_asian_cv_ref` function should appear; no diffs to existing functions.

- [ ] **Step 13: Run full test suite — no regressions**

```
venv\Scripts\pytest.exe tests\ -v
```

Expected: all previously-passing tests still pass; the three new `test_asian_cv_ref.py` tests pass.

- [ ] **Step 14: Final commit**

```
git add src\plot_arithmetic_asian_decay.py figures\fig_arithmetic_asian_decay.png
git commit -m "feat: add arithmetic Asian RQMC dimension-decay sweep (Paper B Section VI-B, Table V)"
```

---

## Self-Review

**Spec coverage:**

| Spec requirement | Task covering it |
|---|---|
| `arithmetic_asian_cv_ref` new function with docstring | Task 2, Step 3 |
| Docstring states CV design, N_ref param, prints SE, SE meaning | Task 2, Step 3 |
| No existing pricer modified | Task 2 Steps 3+6 enforce this via git diff check |
| Section A1: geometric mean equivalence assert | Task 3, Step 7 |
| Section A2: slope spot-check d=1,64 with published CI assertion | Task 3, Step 7 |
| Section B: 7 CV references printed before sweep | Task 3, Step 7 |
| Section C: arithmetic pricers, same seeds as geometric sweep | Task 4, Step 10 |
| Section C: `rqmc_errs_by_dim` saved per dim for Section D | Task 4, Step 10 |
| Section D: ratio at N=1024 and N=65536 both printed | Task 4, Step 10 |
| Section D: WARN flag at ratio ≥ 0.1 | Task 4, Step 10 |
| Table V: same Markdown format as Table IV | Task 4, Step 10 |
| Figure: white background, shaded CI, correct title, correct filename | Task 4, Step 10 |
| All seeds fixed → reproducible | Verified in Step 12 |
| scipy==1.13.1 confirmed before each run | Steps 8, 11 |

**Placeholder scan:** No TBD/TODO in any code block. All commands have expected outputs.

**Type consistency:**
- `arithmetic_asian_cv_ref` returns `(float, float)` — used as `price, se = ...` in Section B ✓
- `refs[d]` is `float`, used in `abs(p - refs[d])` ✓
- `rqmc_errs_by_dim[d]` is `ndarray (N_TRIALS, len(N_VALUES))`, indexed `.mean(axis=0)[0]` and `[-1]` ✓
- `central[m]`, `ci_lo[m]`, `ci_hi[m]` are lists of floats; converted to `np.array` for plotting ✓
- `cell(m, i=i)` closure capture: `i=i` default prevents loop-variable bug ✓
