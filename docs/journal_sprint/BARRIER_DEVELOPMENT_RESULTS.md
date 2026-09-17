# Barrier development results — 2026-09-17

## Outcome

Two concrete engineering advances: the previously failing degree-32 residual
now synthesizes reliably in this bounded study, including degrees 64 and 128;
and a separable signal circuit removes the joint payoff lookup. Neither proves
an application advantage. Full continuous-price certification remains blocked.

This is adaptive development, not confirmation or a new asymptotic algorithm.
The [protocol](BARRIER_DEVELOPMENT_PROTOCOL.md) was frozen before acquisition.
Original producer/evidence files remain unchanged.

## Phase synthesis and uniform certification

Implemented a palindromic phase parameterization with an analytic Jacobian and
four continuation stages, using SciPy least squares. Symmetric QSP is existing
work: [Dong et al.](https://arxiv.org/abs/2307.12468). This implementation is not
their Newton solver and is not a comparison against QSPPACK's performance.

| Degree | Uniform ideal phase-response error upper bound |
|---|---:|
| 8 | 4.22e-16 |
| 16 | 6.32e-16 |
| 32 | 1.41e-15 |
| 64 | 1.98e-15 |
| 128 | 5.51e-15 |

All five passed the fixed 1e-8 uniform gate. Every continuation attempt is
recorded. No random restart selection was needed in this run; robustness beyond
these five targets is untested. The earlier failed degree-32 fits remain archived.

The certificate uses 70-digit outward interval Laurent arithmetic: write
x=(z+z^-1)/2, propagate the exact archived binary phases, and sum outward bounds
on coefficients of Re(response)-target on the unit circle. It therefore bounds
the whole interval [-1,1], unlike a mesh maximum. A double-precision sampled
response can differ by additional floating evaluation error and need not lie
below a ~1e-15 bound on the exact mathematical response. The bound does NOT
include hardware rotations or implementation error. Exact analytical versus
stored residual coefficients are bounded separately.

## Signal construction without joint lookup

For each basket row, factor exp(mu_i + sum_j b_ij*z_j) into d bounded marginal
functions exp(b_ij*z_j-|b_ij|L). Tensor products of Hermitian reflections encode
their products. A signed linear combination over rows and strike encodes
(A-K)/B. PREP/SELECT/PREP-inverse is an involution; projected reflections give
the invariant two-dimensional walk required by the phase sequence.

These use established [qubitization](https://arxiv.org/abs/1610.06546) and
[block-encoding composition](https://arxiv.org/abs/1806.01838), not a new
primitive. Garbage amplitudes remain and are part of the block encoding.
The construction never substitutes a raw-payoff flag for a QSP signal.

| Four-dimensional model | Marginal signal entries | Avoided joint entries | Signal circuit qubits |
|---|---:|---:|---:|
| q=2 | 64 | 256 | 15 |
| q=6 | 1,024 | 16,777,216 | 31 |
| q=10 | 16,384 | 1,099,511,627,776 | 47 |

q=6/10 are construction plans, not compiled production circuits. These counts
exclude a Hadamard test qubit and are not fault-tolerant physical qubits.
Marginal tables still scale as O(d^2*2^q), not polynomially in precision.
Separate product-normal preparation needs d*(2^q-1) controlled rotations
before decomposition: 4,092 at q=10, with its own cost/error budget.

The actual original-model q=2 signal alone compiled to 3,828 CX, 3,669 u gates,
depth 6,294. This is NOT a full controlled QSP/Hadamard cost. A complete tiny
one-asset/two-date q=1 degree-8 circuit, including product-normal loading and a
Hadamard test, used 7 qubits/16,488 CX and matched its independently enumerated
finite expectation within 1.32e-14. It is a smoke test, not the original target.
Tests also check full complex blocks, Hermiticity, involution, global phases,
endpoint inputs and nonzero garbage on small instances.

## Normalization cost and pricing outcome

The earlier observed finite-grid radius was 109.1852. A non-enumerative safe
ideal radius is 698.5702. This substantially worsens low-degree approximation:

| Degree | Observed finite-price bias with new radius | Ideal variance reduction vs raw QSP at same radius |
|---|---:|---:|
| 8 | +$14.17384 | 5,886.95x |
| 16 | +$3.95658 | 1,248.88x |
| 32 | -$0.39455 | 491.35x |
| 64 | -$1.01322 | 261.34x |
| 128 | +$0.04089 | 177.70x |

The biases need not decrease monotonically; the uniform truncation bound does.
All rows use the original two-asset/two-date contract but its q=2 finite model,
whose exact price is $12.76820533. They are not observations of continuous-price
accuracy. The raw comparator receives the analytic linear offset; both quantum
representations target the same polynomial and have equal approximation bias.
The raw high-degree comparator uses its ideal polynomial response, not a newly
synthesized raw circuit. Reported variance ratios are ideal analytical ratios,
not measured hardware or compiled-cost speedups.

Do not promote the large ratios alone: at degree128, controlled quantum
per-shot price variance is **652.2604**, whereas classical sampling with the
same degree-4 control has variance **18.2575**. Exact classical summation also
solves this 256-path diagnostic. There is no demonstrated quantum superiority.
The classical estimator targets the exact finite payoff; the quantum one targets
its polynomial approximation. This variance comparison is not an equal-total-
error runtime benchmark, and neither direction of end-to-end superiority follows.

## Continuous-price budget remains partial

For q=10/degree128, the outward sum of known representation, polynomial and
phase terms is approximately **$1.874862**. This is a partial bound, not the
actual error, a lower bound on actual error, or a complete price certificate.
Four implementation terms remain unknown:

- signal construction/normalization/rotation implementation error;
- state-preparation error for the integrated representation;
- numerical error in the classical control offset;
- execution/synthesis error of the complete implemented unitary.

The ledger refuses to replace unknown terms with zero. It includes degree-fold
signal operator error and twice the state-vector error, multiplied by the
appropriate residual price scale, when such bounds are supplied. The small
floating circuit discrepancy is not used as an error certificate. Floating
signal coefficients differ slightly from the outward ideal radius, so the
implementation bridge is explicitly unresolved. Hardware noise is not studied.

## Verification and next decision

Focused implementation tests passed before acquisition. Both acquisitions
reproduced all eight numeric payloads exactly in the existing isolated week15
environment; 52 source/artifact hash entries checked. This is same-producer
replay, distinct from independent agent code review and not human review.
Full regression: **964 passed**, 12 legacy warnings, 423.32s. Five supplemental
tests were added after that suite's collection; the final isolated focused run
covered all 63 new tests, passing in 14.58s. No full-suite rerun after those five
test additions is implied. F-only Ruff and whitespace checks passed.

Clean checkout of commit `6529472a`, using the existing isolated week15 env:
63 focused tests passed in 15.88s; both stored archives again passed the eight-
payload/52-hash replay check. This clean check did not rerun full acquisition or
the full regression. Receipts: `barrier_clean_tests_v1.xml` and
`barrier_clean_replay_check_v1.json`.

Independent read-only agent review found no blocking circuit/phase defect for
the stated partial scope. The signal author separately reviewed the phase/error
integration; a third agent audited the interval/dollar calculations. Review
confirmed that the floating signal scale differs from the directed ideal scale
and must remain within the unresolved implementation bridge.

Review follow-up: the q1 smoke test had uniform Gaussian weights. A supplemental
q3 nonuniform product-loader/Hadamard check now agrees within 3.89e-15; reversing
the register bits changes the probability vector by 1.2799 in l1, making this
test sensitive to that error. Loader probabilities agree with independent CDF
weights within 5.56e-17. This remains a small diagnostic, not production proof.

Two reproducibility limitations are retained explicitly: v1 is frozen at
low4/cutoff4/q2 (not every CONFIG field is operative), and its original model
arrays were not contemporaneously archived. The supplemental verifier enforces
the fixed configuration and stores reconstructed means/PCA factors as exact
binary hex values, labeled as post-acquisition reconstruction. Future producers
must archive inputs at acquisition and make every configuration field operative.
See `barrier_integration_check_v1.json`; it does not retroactively repair original
input provenance. All eight numeric payloads did reproduce in the separate env.

One future-run robustness issue was found by synthetic review: the dimensionless
phase gate is 1e-8, but the runner's equal-price diagnostic is a fixed $1e-7.
A candidate with certified phase error 8e-9 can therefore pass the first and
fail the second after dollar scaling. This is conservative false rejection,
not false acceptance. None of this acquisition's <6e-15 fits is affected.
Keep frozen v1 unchanged; the next producer must separate the polynomial
identity check from the certified, dollar-scaled phase-response allowance.

The q3 supplemental check covers within-register bit order for one coordinate;
it is not an independent nonuniform multi-register integration test.

Next substantive target: reduce the normalization/approximation cost (e.g.
sharper certified approximants or a cheaper centered signal), and enclose the
signal/control-offset numerical bridge. Increasing phase-solver effort alone
is no longer the main issue in the tested degree range. Larger-degree circuits
must pay all controlled signal/reflection/preparation costs. Keep classical
controls and randomized QMC competitive in every eventual same-target study.

Evidence: `results/journal_sprint/barrier_development_v1`, corresponding replay
archive and `barrier_replay_check_v1.json`. No hardware jobs, remote push, PR,
merge, confirmation promotion or paper-advantage claim was made in this step.
