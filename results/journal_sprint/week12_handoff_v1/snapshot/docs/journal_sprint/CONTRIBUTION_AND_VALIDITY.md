# Contribution candidate and validity boundary

9 September 2026. Working research decision, not a novelty certification.

## The paper we should try to build

**Reliability-aware resource selection for quantum option pricing under explicit
representation and noise uncertainty.** One coherent unpublished journal paper,
with the essential strong classical baselines from Paper B integrated into its
evaluation. The separate A/B packaging is not a scientific constraint.

The research question is whether a controller can deliver a declared *price*
tolerance at lower honestly counted cost, or correctly decline it, by selecting
representation and quantum resources without consulting exact test answers.
Merely applying QAE to European calls, or observing noisy degradation, is not
enough. Closed-form European pricing remains a validation task, not a commercial
quantum-advantage target.

## Prior-work matrix

| Prior work | Already established / must not claim as ours | Candidate distinction requiring evidence |
|---|---|---|
| [Quantum option pricing, 2020](https://quantum-journal.org/papers/q-2020-07-06-291/) | Quantum financial payoff estimation and hardware demonstrations | End-to-end delivered-price reliability and representation/resource selection, not another payoff circuit |
| [Noisy likelihood AE](https://link.springer.com/article/10.1007/s11128-021-03215-9) | Noise-aware likelihood estimation and depth/noise effects | Explicit envelope uncertainty, all feasible components, refusal rules and application bias accounting |
| [IQAE bias, 2024](https://link.springer.com/article/10.1140/epjqt/s40507-024-00253-x) | Stopping-induced bias and treatment of the last round | Independent pilot/validation integrated with resource selection; splitting itself is standard |
| [BAE, 2025](https://quantum-journal.org/papers/q-2025-09-11-1856/) | Bayesian adaptive AE, uncertainty and noise-aware decisions | Compare frequentist delivered-price coverage and costs against the actual Bayesian method; do not claim adaptive AE is new |
| [BIQAE, 2026](https://quantum-journal.org/papers/q-2026-01-14-1962/) | Bayesian iterative AE | Same: required later executable comparator; credible and confidence intervals are not interchangeable |
| [Non-power-of-two schedules, September 2026 preprint](https://arxiv.org/html/2609.02715v1) | Geometric ladders, likelihood estimation and noise comparisons | Cost-aware application controller with independently validated precision; source benchmark reproduced in this sprint |
| [Quantum QMC, September 2026 preprint](https://arxiv.org/html/2609.03625v1) | A competing route involving QMC and quantum resources | Compare encoding/setup/arithmetic costs and strong RQMC, rather than claiming an MC-only speedup |

These distinctions are hypotheses. The earlier research report contains a broader
source search. Full independent reading of all six designated methodological
papers, including appendices, remains an unchecked human/research task; this
sprint does not relabel focused source inspection as complete reading.

## What the prototype guarantees in exact arithmetic

Fix a schedule of m depths and validation shot counts. At each depth, observations
are stationary independent Bernoulli trials with probability q_k(a,eta), and the
true eta belongs to the declared envelope. Compute a two-sided exact binomial
interval I_k with failure probability at most alpha/m. Invert every sine-squared
branch and allow any eta within the envelope at each depth. Intersect these
preimages to form C.

With probability at least 1-alpha, every I_k contains its true response
probability (union bound). On that event, the true a lies in every preimage and
therefore in C. Allowing a different eta at each depth only enlarges C relative
to inversion constrained to one common eta. It sacrifices tightness, not this
containment argument. Independence between depths is not needed for the union
bound; stationary binomial marginal observations at each depth are needed.

If the schedule/shots are selected using an independent pilot, condition on the
pilot. The fixed-schedule argument applies to fresh validation data for every
selected configuration. Averaging over pilot outcomes preserves the same bound.
Do not repeatedly inspect validation batches and reuse the fixed-sample claim.

If the desired price P satisfies |P-(offset+L*a)| <= B for a *valid deterministic
bound* B and L>0, expanding the mapped hull by B gives a price interval with the
same containment statement. Its midpoint has absolute error at most the declared
tolerance whenever its radius meets that tolerance and containment occurs.
Thus the unconditional probability of an erroneous precision declaration is at
most alpha. The error rate **conditional on making a declaration** need not be
at most alpha; report it separately. Empty sets mean incompatibility, not a price.

If an envelope is itself estimated with failure budget beta, a separately justified
calibration guarantee is required and total failure is at most alpha+beta. This
sprint supplies no such calibration guarantee. A nonempty set never validates an
arbitrary noise model. Drift, correlated shots, and missing noise channels are
outside the theorem.

Implementation widens boundaries by 2e-14 and is numerically tested; it is not
formally verified interval arithmetic. The theorem is exact-arithmetic reasoning.
The affine maps in this sprint use *illustrative* L and B, not proved bounds for
the project's actual option contracts.

## Next prospective protocol (before larger runs)

Keep July E0 and historical outputs unchanged. Version a separate v2 only after
the following are specified: candidate qubit counts and payoff scales; admissible
support/grid/encoding bounds; independent calibration and selection streams;
candidate depth/shot schedules; fixed IQAE, modern AE, direct sampling, quadrature,
control-variate MC and scrambled Sobol baselines; setup/calibration/pilot costs;
held-out contracts; primary false-declaration and completion outcomes; and limits
for simulator time and hardware spend (currently zero hardware spend).

Primary controller success must be measured against the strongest *cheap fixed*
configuration as well as an expensive fixed configuration. The first pilot's
overhead already makes that distinction important. Do not choose v2 thresholds
to improve a v1 headline, or reuse v1 as held-out confirmation.
