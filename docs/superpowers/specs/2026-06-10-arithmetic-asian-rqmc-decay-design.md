---
title: Arithmetic Asian RQMC Convergence Decay — Section VI-B
date: 2026-06-10
status: approved
---

# Arithmetic Asian RQMC Dimension-Decay Experiment (Paper B, Section VI-B)

## Scientific question

Does RQMC's O(1/N)-ish convergence advantage survive on the arithmetic-average
Asian call (non-smooth, no closed form), or does the non-smoothness degrade it
relative to the geometric case in Table IV? This is the direct counterpart to the
geometric sweep; results go into Table V and Fig. 3.

---

## Files changed

| File | Change |
|---|---|
| `src/asian_option.py` | Add `arithmetic_asian_cv_ref()` — new function, no existing pricer touched |
| `src/plot_arithmetic_asian_decay.py` | New script — direct mirror of `plot_dimension_sweep.py` |
| `figures/fig_arithmetic_asian_decay.png` | New output figure |

---

## Reference value design (critical)

Arithmetic Asian has no closed form. The reference is built as:

```
ref_price(d) = MC[ arith_payoff(Z) - geo_payoff(Z) ] * discount
               + geometric_asian_closed_form(S0, K, r, sigma, T, d)
```

**Why this works:** arithmetic and geometric payoffs are highly correlated when
computed from the same Z matrix, so `arith - geo` has far lower variance than
either payoff alone. At N_ref = 2^22 = 4,194,304, the residual SE is typically
< 1e-4 — well below any RQMC error in the sweep.

**Why not plain high-N naive MC:** a naive-MC anchor has its own O(1/√N) floor
(~0.003 at N=4M) that can exceed RQMC's accuracy at large N in the sweep,
corrupting measured slopes. This mistake was made in a prior version of this
project and must not be repeated.

### `arithmetic_asian_cv_ref` function spec

Added to `src/asian_option.py` after the existing geometric helpers.

```python
def arithmetic_asian_cv_ref(S0, K, r, sigma, T, d, N_ref=4_194_304, seed=None):
```

**Algorithm:**
1. Draw `Z ~ N(0,I)` of shape `(N_ref, d)` with `np.random.default_rng(seed)`.
2. Call `simulate_paths(S0, r, sigma, T, Z)` → `S_paths (N_ref, d)`.
3. `arith = max(mean(S_paths, axis=1) - K, 0)` — arithmetic payoff.
4. `G = exp(mean(log(S_paths), axis=1))` — geometric mean of price levels.
5. `geo = max(G - K, 0)` — geometric payoff from same paths.
6. `diff = arith - geo`; `se = discount * std(diff, ddof=1) / sqrt(N_ref)`.
7. `geo_cf = geometric_asian_closed_form(S0, K, r, sigma, T, d)`.
8. `price = discount * mean(diff) + geo_cf`.
9. Print: `[ref d= ]  price=  SE=  geo_exact=`.
10. Return `(price, se)`.

**Docstring must state:**
- This is a control-variate reference (arithmetic minus geometric, plus exact CF).
- `N_ref` parameter: MC budget; must be >= 4,000,000 to keep SE below sweep noise floor.
- Function prints SE so callers can verify noise floor.
- SE returned is residual noise in the reference, not the SE of any sweep estimator.

**No changes to existing functions** in `asian_option.py`.

---

## Script: `src/plot_arithmetic_asian_decay.py`

Direct mirror of `plot_dimension_sweep.py`. Identical structure, variable names,
bootstrap logic, and figure style. Differences are payoff type, reference source,
output names, and added sections A/D.

### Constants

```python
N_REF     = 4_194_304   # 2^22
REF_SEED  = 999         # fixed seed for the reference MC
DIMS      = [1, 2, 4, 8, 16, 32, 64]
N_VALUES  = [2**i for i in range(10, 17)]   # 1024 → 65536
N_TRIALS  = 10
N_REP     = 30
N_BOOT    = 2000
CI        = (2.5, 97.5)
```

### Section A — Geometric sanity check

Runs **before** any arithmetic work. If either assert fails, the script aborts
with a diagnostic message — this signals a harness bug, not a result.

**Step A1 — Geometric mean equivalence assert** (run once, not per-d):
```python
Z_chk = np.random.default_rng(42).standard_normal((1000, 4))
S_chk = simulate_paths(S0, r, sigma, T, Z_chk)
dt = T / 4
cumlog_chk = np.cumsum((r - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*Z_chk, axis=1)
geo_via_log    = np.exp(np.log(S_chk).mean(axis=1))
geo_via_cumlog = S0 * np.exp(cumlog_chk.mean(axis=1))
assert np.max(np.abs(geo_via_log - geo_via_cumlog)) < 1e-10
```
Confirms `exp(mean(log(S_paths))) == S0 * exp(mean(cumlog))` to machine precision.
Uses the log-increment formula inline — no import of private `_cumlog`.

**Step A2 — Slope spot check** for `d ∈ {1, 64}`:
- Run geometric RQMC sweep: 10 trials × 30 reps, same seed scheme as Table IV.
- Compute slope-of-mean via `polyfit(log_N, log10(mean_errs), 1)`.
- Assert slope falls within published Table IV bootstrap CIs:
  - d=1:  slope ∈ [−1.10, −0.80]
  - d=64: slope ∈ [−0.83, −0.60]
- Print `PASS` / `FAIL` per dimension.

### Section B — Build arithmetic CV references

```python
for d in DIMS:
    price, se = arithmetic_asian_cv_ref(S0, K, r, sigma, T, d,
                                        N_ref=N_REF, seed=REF_SEED)
    refs[d], ref_ses[d] = price, se
```

The function prints each reference line. Section B produces 7 lines before the
sweep starts so the reference SE values are visible in the output.

### Section C — Arithmetic sweep

Identical loop structure to `plot_dimension_sweep.py`:

```python
for d in DIMS:
    for j, N in enumerate(N_VALUES):
        for t in range(N_TRIALS):
            asian_naive_mc(…, seed=t)
            asian_antithetic_mc(…, seed=t)
            asian_rqmc(…, n_replications=N_REP, seed=t*1000)
        errs[method][t, j] = abs(price - refs[d])
    # Store RQMC error array for Section D noise floor check
    rqmc_errs_by_dim[d] = errs["RQMC"]   # shape (N_TRIALS, len(N_VALUES))
```

`rqmc_errs_by_dim` is initialised as `{}` before the outer loop so Section D
can access per-dim arrays after the sweep completes.

Seeds match the geometric sweep exactly (`seed=t` for naive/antithetic,
`seed=t*1000` for RQMC) — same random draws, directly comparable experiments.

Bootstrap CI computed identically to `plot_dimension_sweep.py`:
resample trial indices 2000 times, refit slope-of-mean each resample,
take 2.5th/97.5th percentiles.

### Section D — Noise floor check

Printed after the sweep, before the table. For each `d ∈ DIMS`:

| Column | Value |
|---|---|
| `ref_se` | `ref_ses[d]` from Section B |
| `rqmc_err_small_N` | `rqmc_errs_by_dim[d].mean(axis=0)[0]`  — mean over trials at N=1024 |
| `rqmc_err_large_N` | `rqmc_errs_by_dim[d].mean(axis=0)[-1]` — mean over trials at N=65536 |
| `ratio_small` | `ref_se / rqmc_err_small_N` |
| `ratio_large` | `ref_se / rqmc_err_large_N` |

Flag `WARN` if either ratio ≥ 0.1. The binding constraint is typically at small N
(largest RQMC errors), so both ratios are printed. No hard assert — a `WARN`
means "stop and increase N_REF before trusting the slopes."

### Section E — Printed table

```
--- Table V (paste into DOCX) ---
| d | Naive MC | Antithetic | RQMC |
|---|---|---|---|
| 1 | slope [lo, hi] | ... | ... |
...
```

Same format as Table IV in `plot_dimension_sweep.py`.

### Section F — Figure

- File: `figures/fig_arithmetic_asian_decay.png`
- Style: white background, shaded CI bands — identical to `fig_rqmc_dimension_decay.png`
- Title: `"RQMC Advantage Decays with Dimension  [arithmetic Asian, geometric CV reference]"`
- Axes, legend, grid, `ylim`, reference lines (O(1/N) and O(1/√N)) unchanged.

---

## Verification criteria (before declaring done)

1. **Reference SE < noise floor**: all `ratio_large < 0.1` and all `ratio_small < 0.1`
   (no WARN flags). If any WARN appears, stop and increase `N_REF`.

2. **Geometric sanity check PASSes**: both d=1 and d=64 RQMC slopes fall within
   published Table IV CIs. If either FAILs, stop — harness bug.

3. **Geometric mean equivalence assert passes** with max diff < 1e-10.

4. **Reproducibility**: re-running the script produces identical numbers (all
   seeds are fixed: `seed=t`, `seed=t*1000`, `seed=REF_SEED=999`, `boot_rng=np.random.default_rng(0)`).

5. **Figure saved**: `figures/fig_arithmetic_asian_decay.png` timestamp updated.

6. **No changes to existing pricers** in `asian_option.py`.

---

## Parameters (fixed across both experiments)

```python
S0, K, r, sigma, T = 100.0, 100.0, 0.05, 0.2, 1.0
```

---

## Runtime estimate

- Section A (sanity check, 2 dims): ~1–2 min
- Section B (7 references at N=4M, d up to 64): ~1–2 min
- Section C (arithmetic sweep, same budget as Table IV): ~5–10 min
- Total: ~10–15 min
