# Journal feasibility sprint: prospective protocol v1

Recorded 9 September 2026 before this sprint's stochastic outputs are inspected.
Authorized scope: the author's request to execute weeks 1–2 of the journal
reengineering plan. Neither paper has been submitted or published.

This is an exploratory feasibility study, isolated in `research/journal_sprint/`.
It does not alter the frozen July `paper-a/main/v1` protocol or reinterpret its
results. All simulations here are finite-shot response-model simulations,
unless explicitly marked circuit validation. No hardware submission is planned.

## Questions and limits

Can exact simultaneous binomial inversion preserve all feasible amplitudes,
propagate a declared noise envelope, and return useful conditional price
intervals? How much conservatism or abstention does this cost? Can we reproduce
a recent comparator's published/reference benchmark in its original convention?

The prototype is a conservative baseline, not a claim of a novel QAE algorithm.
The intended later contribution is joint representation/resource selection with
reliable application accuracy. BAE/BIQAE remain required later comparators;
this sprint selects the open, compact September 2026 geometric-ladder MLE
implementation for the first independently rerunnable reproduction.

## Frozen comparator experiment

Source: https://github.com/unitaryfoundation/csAE, revision
`202ffb8a462828d04dab13eef5005e295270d0e3`, `mlqae/core.py`.
Apache-2.0 source retained unchanged, with license and attribution.
Reference: https://arxiv.org/html/2609.02715v1, Table I and source golden test.

- Golden test: plain and flagship ladder at requested cap 125, 30,000 trials,
  seed 880125, amplitudes uniform on (0.1,0.9), original source conventions.
- Source target windows: plain C95 2.82 ± 0.04; flagship C95 2.85 ± 0.05,
  C99 5.23 ± 0.30, parallel C95 0.209 ± 0.008.
- Independent reduced replication of Table I: caps 60 and 125, 30,000 trials,
  seeds 2026090960 and 20260909125; reference C95 values 2.776 and 2.886.
  Report a 95% order-statistic interval for C95 and deviation from the published
  point. Reduced trials/different NumPy and Python are explicitly disclosed;
  this is not the original million-trial reproduction.
- Noise extension: cap 182, eta=0.001, 20,000 trials, seed 20260909182;
  matched eta and zero-eta likelihood on identically sampled observations.
  This is a qualitative replication of the noise comparison, not exact Table IV.
- Preserve per-trial truth, counts, estimates and errors in compressed NPZ.
- The source estimates `b=sin(theta)` using cos-squared response; our circuit
  objective probability is `a=sin(theta)^2`, measured with sine-squared response.
  Do not compare raw percentile constants across these conventions.
- Preserve source `Ntot=sum(shots*k)+shots_at_zero`; also report
  `sum(shots)`, `sum(shots*k)`, and `sum(shots*(2*k+1))` separately.

## Frozen prototype experiment

Response: `q_k=.5+(1-eta)^(2*k+1)*(sin((2*k+1)*theta)^2-.5)`;
`theta=asin(sqrt(a))`, `a` is the objective probability.

- Amplitudes: 0.01, 0.10, 0.30, 0.50, 0.70, 0.90, 0.99.
- Validation schedule: k=(0,1,2,4,8). Shots per depth: 128 and 512.
- Independent trial repetitions per amplitude/condition/shot setting: 200.
- Conditions: ideal eta=0; matched eta=0.01; true eta=0.01 inside a declared
  [0.005,0.015] envelope; misspecified eta=0.03 with assumed eta=0; and an
  intentionally inconsistent depth-response vector (0.05,0.95,0.05,0.95,0.05).
- Family-wise interval failure budget: 0.05, split equally across depths.
- Invert exact two-sided Clopper–Pearson intervals analytically through all
  sine-squared branches. Noise bounds are relaxed per depth; this is an outer
  enclosure of the shared-eta feasible set and may be conservative.
- Precision decisions: report half-width thresholds 0.01 and 0.025 in probability
  units and illustrative affine price maps with sensitivities 1 and 100.
  Dollar tolerance 1; deterministic bound 0.1. These maps are controlled
  illustrations, not actual option-pricing or speedup experiments.
- Report target containment, components, half-width, incompatible-set frequency,
  declared-precision rate, unconditional/conditional erroneous declarations,
  RMSE of the interval-hull midpoint, and all resource counts.
- Baselines on the same counts: known-model grid MLE point estimate (no claimed
  calibrated interval); direct k=0 sampling at equal A-equivalent cost.
- Separate split-sample pilot: same amplitudes, eta=0.01, known model, 200 trials;
  64 pilot shots at each depth choose a single fresh validation shot count
  from (128,512) by projected pilot interval width versus probability tolerance
  0.01. Truth is never an input to selection. Every candidate validation batch
  is independent of pilot observations, and pilot cost is included.
- Seed keys are SHA-256 based and contain experiment, amplitude, condition,
  shots, replicate and purpose. Pilot and validation purposes are distinct.
- A nonempty conservative set is not evidence that an arbitrary noise model is
  correct. Guarantees are conditional on the declared envelope, independent
  stationary binomial shots, and valid deterministic bounds.
- Numerical rounding allowance is explicit. We test exact endpoint behavior and
  preimage containment; no claim of formally verified floating-point arithmetic.

## Validation, storage, and decision gates

Before the exploratory experiment, pass analytic preimage/alias tests, zero/all
count endpoint tests, noise-envelope containment checks, exact enumeration of
small-sample simultaneous coverage, invalid-input tests, and a small Qiskit
statevector check of the ideal sine-squared response. Existing E0 results were
verified in the preceding review; this isolated response prototype additionally
has its own tests and does not launch the original E1–E7 run matrices.

Preserve an evidence manifest containing historical file hashes and last known
Git revisions. Historical inputs are read-only. New output directories are
exclusive-create; a run cannot overwrite an existing directory. Persist the
planned run and final config/source hashes, records, aggregates, and completion
marker. Retain failures and do not silently retry or omit cells.

Use no more than 60 minutes for the initial response experiment; a longer run
needs an explicitly recorded compute-only amendment before continuing. A slow
case stays a documented partial run. Do not select parameters after observing
results merely to improve the headline. Any new experiment gets a new version.

Pass/fail distinction: software and source-reproduction tests have numerical
gates; usefulness is exploratory. The sprint never declares publishability or
quantum advantage. It concludes with observed trade-offs and a concrete next
decision. Human contributor availability and independent scholarly review stay
pending until actually supplied.
