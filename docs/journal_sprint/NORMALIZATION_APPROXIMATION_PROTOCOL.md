# Normalization and approximation development — 2026-09-17

New bounded adaptive development after barrier_v1; not confirmation. Preserve
previous producers and evidence. No hardware submission or remote writes.

## Fixed acquisition scope

- Original two-asset/two-date basket, strike100, cutoff4. Finite q2 diagnostic
  and q10 non-enumerative error/resource plans; no q10 joint enumeration.
- Degrees16/32/64/128. Compare archived-style truncated Chebyshev approximation
  with an even polynomial fit by discrete minimax LP (8193 fitting nodes,
  HiGHS maxiter10000). Retain failure/status; no continuous optimality claim.
- Independent uniform certificate: explicit binary64 Chebyshev evaluation
  rounding bound on a dyadic grid N>=8*degree^2, followed by Markov's inequality
  on p(x)-x in [0,1]. Even parity covers [-1,1]. No mesh-only certificate.
- Both original separable signal and centered product expansion. Center each
  exp(b*z) into cosh(|b|L)+sinh(|b|L)*r(z); expand subsets and combine constant
  terms with strike. The centered expansion grows exponentially in dimension
  and is capped at four dimensions. Never describe it as asymptotically scalable.
- Compile matched tiny d2/q1 signal circuits for both constructions. Original
  d4/q2 and d4/q10 are structural plans only in this study. Signal-only gate
  counts are not full controlled-QSP runtime; no extrapolated hardware speedup.
- Same degree4 archived-coefficient classical control on both sides. Fit raw
  and residual polynomial identities separately from phase accuracy. Scale the
  phase allowance by dollars, fixing frozen barrier_v1's conservative rejection
  mismatch in this NEW producer. Four continuation stages,150 evaluations each.
- Enclose q10 finite-model control moments/offset using directed interval
  arithmetic, not enumerated joint paths. Pay and archive the product-loader
  error and rotation counts. Signal/execution errors remain unknown unless
  separately established; no automatic confirmation admission.
- Archive exact model means/factors, polynomial constants, configuration and
  environment before acquisition. Make configuration operative. Exclusive output
  directories, before/after source hashes, checkpointed artifacts, failure marker.

## Research basis

[Dong et al., constrained minimax QSP, August2026](https://arxiv.org/abs/2608.30937)
identifies finite-grid feasibility as insufficient for full-domain constraints.
Our discrete LP plus independent Markov enclosure is not their Fourier
retraction algorithm, and is not claimed to improve it.
[QSPPACK](https://github.com/qsppack/QSPPACK) provides established polynomial and
phase-design methods. Minimax fitting, control variates, LCU composition and
Markov bounds are established tools; this study does not establish novelty.

## Acceptance and reporting

Uniform ideal phase bound <1e-8; approximation error reported in dollars with
each actual ideal normalization. Keep all degree/family outcomes, including
negative cost tradeoffs. Classical controls receive identical offsets and
setup information. Finite-grid exact call versus quantum polynomial estimands
differ; variance alone is not an equal-total-error performance comparison.
Run focused/full tests, separate-environment replay, independent agent review,
and log results, limitations and remaining blockers.
