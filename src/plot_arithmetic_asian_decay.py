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
