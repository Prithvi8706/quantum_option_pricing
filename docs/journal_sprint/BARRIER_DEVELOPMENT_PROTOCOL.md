# Bounded barrier development, 2026-09-17

Adaptive development after the combined experiments; not confirmation. Preserve
all prior producers/evidence. No hardware jobs, remote writes or advantage claim.

## Fixed scope before acquisition

- Original two-asset/two-date contract, strike 100, cutoff 4. Degrees
  8/16/32/64/128 with degree-4 analytical control. Phase fits use a palindromic
  parameterization, analytic Jacobian and continuation at .25/.5/.75/1, each
  capped at 150 least-squares evaluations. Retain every attempt, including caps.
- Certify the ideal phase response by outward 70-digit interval Laurent
  coefficient arithmetic, not mesh acceptance alone. Accept only uniform error
  below 1e-8. Separately bound exact analytical vs archived coefficients.
- Replace joint signal lookup by a separable product-exp block encoding:
  d squared marginal functions of q bits, LCU over d rows plus negative strike.
  Pay B=sum_i exp(mu_i+L*sum_j|b_ij|)/d+K rather than observed grid radius.
  This scales as O(d squared * 2^q) input angles, NOT polynomial in precision.
  Gaussian state preparation remains a separate O(d*2^q) product loader.
- Exhaustive tiny block/Hermiticity/walk tests; emit/compile bounded small
  circuits only. Original d=4, q=2 circuit resources and q=6/10 construction
  plans are separate evidence. Do not statevector-simulate production size.
- Finite q=2 enumeration is a diagnostic/comparator, never an oracle input.
  Compare old observed radius and new paid B on the same finite target. Both
  quantum and classical estimators receive identical polynomial controls.
- Compose existing outward continuous tail/midpoint/model-bridge bounds with
  polynomial and phase bounds at q=2/6/10. Signal implementation, control-offset
  rounding and execution errors remain UNKNOWN unless separately enclosed.
  A partial sum is not a complete bound or admission. No confidence campaign.

## Sources and distinction

Symmetric QSP is established prior work, not our new algorithm:
[Dong et al., robust iterative symmetric QSP](https://arxiv.org/abs/2307.12468),
[QSPPACK](https://github.com/qsppack/QSPPACK), and
[pyqsp implementation](https://github.com/ichuang/pyqsp).
Our bounded solver independently implements the symmetric parameterization with
SciPy least squares; do not label it their Newton method. Separable LCU and
projected walks use standard block-encoding constructions, not a novelty claim.

## Evidence controls

Exclusive output directory, configuration/source hashes before and after,
checkpointed phase records, failure marker and artifact checksum manifest.
Run focused and full regressions and independent code review where available.
Development checks/fixes before acquisition are not confirmation observations.
