# Confirmation unblock attempt: reversible arithmetic

Date: 2026-09-17. Development only. Confirmation remains blocked.

## What is now implemented

Table-free signed fixed-point affine log mapping, exact reversible modular
addition, signed full-product/floor multiplication, Taylor/Horner exponential,
raw arithmetic-call payoff, uniform-selector comparator and clean uncomputation.
The construction emits actual X/CX/CCX gates rather than assigning an abstract
oracle query a unit cost. A separate product-normal binary-tree loader encloses
its stored-angle error in an explicitly ideal controlled-RY model.

The original two-asset/two-date case uses L=4, q=10 per normal, f=24, 40-bit
arithmetic words and degree32 before removing exact zero high coefficients.
No 2^40 payoff table is constructed. Register/circuit resource use remains large.

| Quantity | Development result |
|---|---:|
| Normal-input qubits | 40 |
| Selector qubits | 35 |
| Total allocated logical payoff-program qubits | 3,637 |
| X / CX / CCX | 3,214 / 5,080,501 / 5,019,262 |
| Total logical payoff gates, including clean uncompute | 10,102,977 |
| Logical payoff depth | 1,597,792 |
| Additional controlled-RY loader nodes | 4,092 |
| Arithmetic price-error upper bound | $0.001514075 |
| Ideal loader price-error upper bound | $1.022e-10 |
| Prospective combined representation-bias upper bound | $0.203585334 |
| Actual comparator price scale | $496.868114 |

Rounded bounds in this table are upwards. Exact decimal endpoints are archived.
The combined bound includes the earlier tail/midpoint/model bridge. It is an
analytic logical-design bound, not a validated six-component PriceContract,
physical implementation certificate or delivered-price confidence interval.
Hardware synthesis error remains unknown. Full A, A-inverse and Grover
reflections have not been hardware-transpiled/costed together. These logical
gate counts cannot be compared numerically with classical seconds as a speedup.

## Same continuous target: classical development check

Existing MC/control, PCA randomized-QMC/control and conditional randomized-QMC/
control producers were used for the same business contract. Each method paid
one independent1024path control-fitting pilot; setup/pilot timing is stored
separately. Sixteen independent repetitions at each of1024and4096paths were
generated with purpose-separated development streams. The fitted control is
fixed across repetitions; uncertainty is conditional on this paid pilot.

At4096paths per repetition:

| Method | Mean price | Replicate SD | Standard error of mean |
|---|---:|---:|---:|
| Antithetic MC + control | 9.205911 | 0.016263 | 0.004066 |
| PCA RQMC + control | 9.199887 | 0.001434 | 0.0003584 |
| Conditional RQMC + control | 9.199371 | 0.00031465 | 0.000078663 |

These are observed floating-point development diagnostics, not certified error
bounds, independent-point binomial intervals or confirmation results. There is
no exact continuous truth in this audit and no claim that SD equals RMSE.
Still, the strong baseline combined with expensive reversible arithmetic gives
no empirical support for quantum superiority on this candidate.

## Verification and provenance

- Focused primitive/loader suite:40tests passed before the large audit; final
  isolated-environment suite41passed in10.74s, including runner failure and
  exclusive-output preservation. Existing week15 environment reused, not newly
  created for this increment.
- Small signed addition/multiplication/comparison domains were exhaustively
  checked, including negative floor semantics and ancilla return. Small composed
  raw-payoff truth checks cover128input/selector/flag combinations.
- An actual full-register comparator statevector matched the nonzero Grover
  response; Gaussian loaders q1..4 matched statevector sanity checks and inverse.
  This is not a full large-payoff statevector execution.
- The original large audit checks two computational basis states, both with a
  false output flag. A separate regeneration verifier adds a nonzero-payoff,
  true-flag test to avoid treating those two checks as sufficient flag coverage.
- Source/input hashes, exact plans/angles, gate hash/counts and all development
  records are retained. Separate-environment regeneration reproduced plans,
  loader and all10,102,977gates exactly; the additional positive-flag/workspace
  check passed. All96classical prices, pilots, identities and summaries replayed
  exactly excluding timing. Fresh-process reproduction is not independent
  scientific review. Full-regression completion is recorded in the running log.
- Full regression886passed/20legacywarnings in426.78s. Only three unused test
  imports were removed during that run; the final isolated41test pass covers
  the resulting test files. Producer code was unchanged throughout acquisition,
  regeneration and verification.
- Initial test failures (overly loose zero-stage magnitude accounting and an
  interval coercion mismatch) were fixed before the successful large acquisition.
  No failed research trial was dropped; these were development unit-test failures.

Artifacts: `results/journal_sprint/arithmetic_development_v1`,
`arithmetic_classical_v1`; source/proof scope:
[protocol](REVERSIBLE_ARITHMETIC_PROTOCOL.md).

## Decision and actual remaining gate

The exponential path-table requirement has a concrete replacement for the raw
call. This is meaningful implementation progress, not a new quantum algorithm.
The basic clean implementation has high workspace/gate cost; tighter register
reuse, constant-specific arithmetic, alternative exponential circuits and a
residual kernel are possible optimization tasks, not demonstrated solutions.

Do not open a quantum-superiority confirmation campaign on this evidence.
The existing encoding-aware decision-rule/limitations contribution can still be
evaluated, but changing the primary claim to that contribution must be explicit.
Before launching any held-out confirmation, obtain actual scientific agreement
on the claim, ideal-versus-physical scope, full cost accounting and statistical
protocol; then run the relevant fixed-design study. No code change can provide
those human endorsements or make a costly route advantageous by declaration.

### Review packet for Aasa and the statistical reviewer

Aasa: review the affine/overflow/Horner/comparator derivations and loader model;
identify any valid cheaper circuit and its error/cost proof; distinguish known
arithmetic from the paper's intended contribution. State objections and actual
work performed. Do not attest to experiments or a hardware advantage not shown.

Statistical reviewer: select the precise primary claim with the authors; verify
total error allocation, stopping/interval guarantees for the chosen adapter,
paid setup/calibration and strong-baseline fairness, multiplicity, declaration
denominators, repetitions/power and held-out regimes. Existing sixteen-replicate
development observations cannot be relabeled confirmation. Record real names,
dates, decisions and contributions; agent review is not their signature.
