# Normalization and approximation results — 2026-09-17

## Decision

The discrete-minimax candidate improves the uniform payoff bound at fixed
degree. Centering further reduces the normalization, but its subset expansion
increases circuit cost substantially. Keep minimax as a promising approximation
option, and centered LCU as a cost-qualified alternative, not an automatic
replacement. There is still no demonstrated quantum advantage or confirmation.

This is bounded adaptive development under the
[frozen protocol](NORMALIZATION_APPROXIMATION_PROTOCOL.md), not a new algorithm
or a confirmation sample. Earlier producers/evidence are unchanged.

## Measured and enclosed outcomes

Original two-asset/two-date contract; cutoff4; q10 budget and q2 finite diagnostic.
All eight polynomial/phase candidates (two approximations, four degrees) passed
the fixed ideal uniform phase gate. All sixteen family/approximation/degree
rows are retained. Degree128 comparison:

| Signal / approximation | Ideal radius B | Uniform payoff-error bound | Sum of known dollar bounds |
|---|---:|---:|---:|
| Original / truncated | 698.5702 | $1.672791 | $1.874862 |
| Centered / truncated | 498.5702 | $1.193872 | $1.395944 |
| Original / minimax candidate | 698.5702 | $0.848004 | $1.050076 |
| Centered / minimax candidate | 498.5702 | $0.605222 | $0.807293 |

The last column is a **partial bound**, not actual error, a complete price
certificate, or a lower bound on actual error. `total_bound` remains null and
`application_admitted` remains false. Two terms remain unknown: signal
implementation and execution/synthesis error. Hardware noise is not studied.

The minimax candidate's degree128 uniform approximation bound is 0.002501767
versus 0.004935037 for the truncated polynomial: about a 49.3% reduction before
dollar scaling. Its ideal uniform phase-response error bound is 8.44e-15.

## Why the approximation certificate is stronger than a sampled fit

HiGHS solves a finite-grid even-Chebyshev approximation LP. The returned
polynomial is only a candidate; continuous minimax optimality is not claimed.
An independent certificate evaluates p(x)-x on an exact dyadic grid in [0,1],
pays a directed bound for each binary64 recurrence/product/sum/subtraction,
then uses Markov's inequality:

M = max_[0,1]|p(x)-x| <= (grid_max + evaluation_error)/(1-degree^2/N).

N>=8*degree^2 limits the multiplicative grid-to-domain factor to 8/7. Evenness
covers [-1,1]. The certificate assumes IEEE binary64 round-to-nearest, gradual
underflow and the explicitly implemented separate arithmetic operations. It
does not trust LP feasibility, floating root finding or a mesh alone.

The recent [Dong et al. constrained-minimax QSP paper](https://arxiv.org/abs/2608.30937)
motivated treating full-domain feasibility separately from discrete fitting.
Our LP-plus-Markov method is not their Fourier-retraction algorithm, nor a
claimed improvement over it. QSP minimax design and LCU are established methods.

## Centering: normalization improvement, circuit penalty

Expand exp(b*z)=cosh(|b|L)+sinh(|b|L)*r(z), |r|<=1, over subsets. Combining
the constant terms with strike gives B=U-C+|C-K|, where U bounds the basket
and C is the summed constant. Here C>K, so B=U-K instead of U+K: reduction
698.5702 to 498.5702. Directed ideal-radius enclosures are recorded; floating
implemented coefficients still need an operator-error bridge.

| Original four-dimensional construction | Original LCU | Centered LCU |
|---|---:|---:|
| Selected terms | 5 | 61 |
| Local reflections | 16 | 128 |
| Signal qubits at q10 | 47 | 50 |
| Unique marginal entries at q10 | 16,384 | 16,384 |
| SELECT marginal-angle uses at q10 | 16,384 | 131,072 |

Centering grows exponentially with dimension and is capped at d<=4. The marginal
tables still grow exponentially in precision q. No joint path table is used.
The q10 numbers are structural plans, not compiled production resources.

Actual matched **tiny d2/q1 signal-only** compilation: original206CX versus
centered1020CX (4.95x), and 6 versus7 qubits. These are neither full controlled
QSP/Hadamard costs nor original-target wall-clock times. They rule out claiming
centering is unconditionally cheaper merely because B is smaller. Actual small
operators were checked for Hermiticity, involution, strike sign, unused index
branches, retained garbage and complex projected-walk response.

## Two previously unknown ideal-model terms now bounded

1. Product-state preparation: reuse the directed ideal controlled-RY loader
   construction and telescope four independent normal registers. The normalized
   state-vector error is <=2.05632e-13; each residual expectation pays twice this
   value times its price scale. This is not a hardware preparation guarantee.
2. Control offset: outward finite-model moments through degree4 use70multinomial
   terms, not joint enumeration. q10 used579exponentials,261120cell visits and
   1025CDF boundaries. Exponentials along a coordinate use a directed geometric
   recurrence. Moments are computed once per precision and shared across both
   families. The actual selected binary offset is compared with the full
   interval, paying rounding and Chebyshev-to-monomial arithmetic.

q10 original/centered offset-error bounds are 9.06e-16 and3.20e-15 dollars.
The exact business discount versus archived binary discount difference is paid
separately (<=1.335e-14 dollars). The same controls and moments are available
classically. Representation tail/discretization/model-bridge bounds are retained.

## Finite diagnostic is not confirmation or performance superiority

The q2 exact finite price is $12.76820533, not the continuous target price.
At degree128:

| Signal / approximation | Observed finite-price bias | Quantum ideal per-shot variance | Classical controlled variance |
|---|---:|---:|---:|
| Original / truncated | +$0.04089 | 652.2604 | 18.2575 |
| Centered / truncated | +$0.12386 | 455.0015 | 14.7188 |
| Original / minimax candidate | +$0.55215 | 763.7400 | 18.2575 |
| Centered / minimax candidate | -$0.03019 | 488.5011 | 14.7188 |

A tighter worst-case bound does not guarantee smaller error under this specific
finite distribution: original/minimax has worse observed bias than truncated.
Do not hide that outcome or promote the favorable centered point as confirmation.
Classical sampling targets the exact finite call; quantum estimates a polynomial
approximation. Variances are therefore not an equal-total-error/equal-cost
runtime comparison. Exact classical summation also solves this diagnostic.

## Reproducibility and handoff

Model means/factors, binary hex inputs, low coefficients, numerical backend and
source hashes were archived before fits/acquisition. Configuration is operative,
with explicit rejection outside supported low4/cutoff4. The prior producer's
fixed-dollar phase check is replaced by separate polynomial identity and
dollar-scaled certified phase-response checks. Failures/no-overwrite behavior
and replay tamper rejection have regression tests.

Independent agent review covered the uniform certificate, centered construction,
offset enclosure and budget integration. The separate-environment replay matched
all15numeric payloads exactly except explicitly named timings;74source/artifact
hash entries checked. Full-suite and clean-checkout receipts are recorded in the
project log. Same-producer replay is not independent scientific review.

Post-acquisition read-only agent audit recomputed all eight candidate/phase
certificates, residual coefficient bridges, offsets from archived moments, and
all sixteen budgets, and recompiled both tiny signals. No blocking finding for
the stated scope. It checked all21producer hashes and16artifact hashes in the
original acquisition. This is agent review, not collaborator/human sign-off.

Clean checkout `e6894c82`, using the existing isolated week15 environment:
102new tests passed (8legacywarnings,22.36s), plus the fifteen-payload/74-hash
replay check. The clean checkout did not repeat the complete acquisitions or
the full regression. Receipts are `normalization_clean_tests_v1.xml` and
`normalization_clean_replay_check_v1.json`.

Full regression on the main tree completed: **1071passed**,12legacywarnings,
488.91s. All102new tests were included; no producer changes during acquisition,
replay or regression. F-only Ruff and whitespace checks passed. Full receipt:
`normalization_full_tests_v1.xml`.

Next: certify the implemented signal block (stored marginal rotations plus LCU
preparation and normalization), then the execution model. Explore cheaper
normalization only with full controlled-circuit costs; do not expand the
exponential subset construction without a cost justification. A complete bias
budget and a same-target classical comparison remain necessary before confirmation.

Artifacts: `results/journal_sprint/normalization_approximation_v1`, corresponding
replay and `normalization_replay_check_v1.json`. No hardware job, remote push,
PR, merge, or confirmation promotion in this step.
