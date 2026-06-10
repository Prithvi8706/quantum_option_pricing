# Project Update — 2026-06-10

## What was accomplished

**Paper B hardened and completed:**
- Table IV rebuilt with bootstrap 95% CIs (2000 resamples, 10 trials, 30 RQMC
  replications — budget parity with Table III). The d≈16–32 crossover is now
  demonstrated by overlapping confidence bands, not asserted by a point estimate.
- New Section VII (Robustness to Payoff Discontinuity): RQMC retains −0.98
  [−1.06, −0.90] on the European digital (cash-or-nothing) call, consistent with
  He and Wang (2015, SIAM J. Numer. Anal. 53(5):2488–2503) who proved the
  scrambled-net RMSE rate is O(n^{-1/2-1/(2d)}) for indicator functions; at d=1
  this predicts −1.0, which the measured CI contains.
- QAE grid-bias finding: at n=5 qubits, IQAE is discretization-limited to a fixed
  2.2e-2 error floor vs the continuous price, independent of epsilon. This overhead
  is not captured by the asymptotic O(1/M) argument.
- Figure 4 (digital convergence) embedded. Abstract, conclusion, ref [7] (P. Raghu,
  working title, in preparation 2026), and ref [11] (He & Wang 2015) all updated.

**New code committed:**
- `src/digital_option.py` — digital_mc, digital_antithetic_mc, digital_rqmc
- `src/black_scholes.py` — added digital_bs_price
- `src/quantum.py` — added _build_digital_circuit, quantum_digital_call
- `src/plot_digital_convergence.py` — full convergence experiment script
- `tests/test_digital.py` — TDD test suite (15 tests, all passing)
- `figures/fig_digital_convergence.png` — Figure 4
- `src/plot_dimension_sweep.py` — updated to 5-point N window, bootstrap CIs
- `figures/fig_rqmc_dimension_decay.png` — updated Figure 2

**Arithmetic Asian experiment (null result, kept for reproducibility):**
- `src/asian_option.py` — added arithmetic_asian_cv_ref (geometric CV reference)
- `src/plot_arithmetic_asian_decay.py` — arithmetic dimension-decay sweep
- `tests/test_asian_cv_ref.py` — 3 tests

## Problems hit and how we resolved them

**1. Reference-floor contamination in the arithmetic sweep.**
At low dimensions (d=2,4,8), RQMC at N=65536 was accurate enough that the
reference SE (~1.7e-4) exceeded 10% of the measured error — meaning the reference
noise contaminated the slope fit. Fix: truncated the N range to [1024, 16384]
(5 points) for both arithmetic and geometric sweeps so they use identical windows.
Also bumped N_REF from 2^22 to 2^23 to clear the last marginal case. Geometric
Table IV was re-run on the same 5-point window for direct comparability.

**2. Arithmetic null result — couldn't resolve the smoothness question.**
The arithmetic Asian experiment was designed to test whether RQMC degrades on a
non-smooth payoff. Result: arithmetic and geometric RQMC slopes were statistically
indistinguishable within bootstrap CIs at every dimension. Root cause: arithmetic
averaging over d≥8 dates smooths the payoff enough that the payoff-type difference
is smaller than the statistical noise of a 10-trial fit. The non-smoothness effect
is real but confined to genuinely discontinuous payoffs, not averaged ones.
Decision: do not feature the arithmetic table in the paper; pivot to the digital
option which has a real discontinuity.

**3. QAE M=2 statevector collapse.**
Discovered that Sampler() in exact/statevector mode returns the true amplitude
with zero variance. IQAE's stopping criterion (CI width < 2ε) is satisfied
immediately at round 0. M=2 (the minimum) is returned for every epsilon — this
is not a convergence measurement. This affects the entire QAE stack (both
quantum_call and quantum_digital_call), not just the digital.
Fix: replaced IQAE runs with theoretical oracle cost M = ceil(π/ε), matching
the formula in plot_break_even_shift.py (M = π√N/1.96, VRF=1 → M = π/ε).
The QAE series is explicitly labeled "theoretical cost line, not measured
convergence" in the figure, caption, y-axis label, and printed output.

**4. LinearAmplitudeFunction post_processing bug.**
LinearAmplitudeFunction.post_processing uses the Woerner Taylor-approximation
inverse, designed for linear payoffs. For the step-function digital oracle, this
formula is wrong: pp(sqrt(0.537)) = 0.648 ≠ 0.537 at n=5.
Root cause: the digital circuit encodes P(obj=|1⟩) = grid_p exactly (not via
Taylor approx), so IQAE returns the probability directly, not the amplitude.
Fix: post_processing = lambda a: a (identity). Confirmed by statevector check:
sv P(obj=1) = grid_p to 1e-6. The D2 assertion in the script is the load-bearing
guard for this.

**5. QAE grid-bias floor.**
At n=5 qubits, the digital price on the 32-point grid is 0.5107 vs the continuous
0.5323 — a fixed 2.16e-2 offset. As epsilon shrinks, QAE error vs the continuous
price floors at this value, falsely appearing to "stop converging."
Fix: QAE epsilon sweep measures error vs grid_true_price (computed classically
from LogNormalDistribution._values/_probabilities), not the continuous BS price.
Grid bias reported separately. Section D3 in the script computes grid_true_price
before the sweep and it is used as the QAE convergence reference throughout.

## Current Paper B status

Complete pending:
- Final read-through (author task)
- Ref [7] title to be finalized when Paper A is named

## Open items for next sessions

- Paper A: IBM hardware run (highest-leverage item in the program)
- Ref [7]: update with Paper A's final title once known
- The unanswered question: "where does QAE actually win in option pricing?"
  (Digital showed it doesn't win there either; the genuine quantum-advantage
  regime remains unlocalized experimentally)
- Paper C: awaiting Papers A and B completion
