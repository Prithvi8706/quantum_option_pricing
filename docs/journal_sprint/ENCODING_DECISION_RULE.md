# Encoding-aware dollar decision rule: implementation and evidence

Date: 2026-09-15. Status: implemented conservative fixed-time planner, not a new
quantum algorithm, quantum advantage, or journal-ready novelty claim.

## What question it answers

For a finite menu of encodings of the SAME price, which has the lowest declared
acquisition cost among those for which a sufficient uniform dollar-error bound
fits the pricing budget? The planner sees no exact price, expected payoff,
statevector amplitude or pricing observations. It can decline to certify.

This answers a different question from whether a quantum computer is faster
than a classical one. All experiments here use k=0 direct sampling, whose
statistical scaling is the usual inverse-square precision scaling. There is
no amplitude-estimation query speedup in this planner.

Implementation: `research/journal_sprint/encoding_decision.py`.
Runner/replay: `research/journal_sprint/run_encoding_decision.py`.
Frozen local protocol: [PROTOCOL_ENCODING_DECISION_V1.md](PROTOCOL_ENCODING_DECISION_V1.md).

## 1. Assumptions and notation

Fix K encodings before calibration. For each encoding e assume an externally
justified bound |P - (O_e + S_e a_e)| <= B_e with a_e in [0,1] and S_e>0.
The bound must include every relevant support, grid, payoff approximation,
rotation synthesis and preparation error. Our synthetic check reuses the
existing ideal-grid bounds; it does not establish physical error allowances.

Direct pricing outcomes are independent Bernoulli with fixed response
q_e = f_e + (1-f_e-g_e) a_e. Independent here includes fresh pricing samples
conditional on calibration and the resulting encoder/sample-size selection.
This is not arbitrary gate noise, correlated errors or uncontrolled drift.

Acquire m fixed calibration shots for each of two states for EACH encoding.
Use a CP interval with noncoverage alpha_cal/(2K) for each of the 2K rates.
Expand endpoints by the supplied transfer guard, clipped to [0,1]. By a union
bound, all rectangles simultaneously cover the pricing rates with probability
at least 1-alpha_cal, provided the transfer assumption holds. Separate rates
per encoder are allowed. Independence between different calibration datasets
is not needed for this union bound, but each coordinate's binomial assumption is.

For one rectangle define

    f_mid = (f_L + f_U)/2,  g_mid = (g_L + g_U)/2
    c = 1 - f_mid - g_mid
    d = max(f_U-f_L, g_U-g_L)/2.

The implemented sufficient screen requires f_U+g_U<1. A weaker contrast test
might also support the algebra below, but is not used in this protocol.

## 2. Uniform error bound

On the calibration event,

    |q - [f_mid + c*a]|
      = |(1-a)(f-f_mid) - a(g-g_mid)| <= d.

For n fresh pricing outcomes, let q_hat be their mean and
a_hat=clip((q_hat-f_mid)/c, 0, 1). Hoeffding gives

    h(n) = sqrt(log(2/alpha_val)/(2*n)),
    Pr(|q_hat-q| > h(n)) <= alpha_val.

Clipping onto [0,1] cannot increase distance to the true a. On both events,

    |a_hat-a| <= [h(n)+d]/c,
    |O+S*a_hat-P| <= R(n) = B + S*[h(n)+d]/c.

The emitted price interval is [O+S*a_hat-R(n), O+S*a_hat+R(n)]. No no-arbitrage
clipping is used to hide interval width. A trivial full-amplitude interval and
outcome-dependent narrower intervals are possible alternatives, but are not
optimized by this first planner. Floating-point padding in the calibration
intervals is engineering protection, not a directed-rounding proof.

## 3. Pricing budget and representation selection

For desired dollar tolerance tau, define

    margin_e = c_e*(tau-B_e)/S_e - d_e.

If margin_e>0, a sufficient number of pricing shots is

    N_e = ceil[log(2/alpha_val)/(2*margin_e^2)].

The implementation uses monotone integer binary search under each supplied cap
to avoid numerical overflow near a zero margin. It directly rechecks R(N)<=tau.
It ranks eligible encodings by

    acquisition_score_e = 2*K*m*calibration_cost_per_shot
                          + N_e*encoding_cost_per_shot.

The result minimizes THIS sufficient-bound score in THIS fixed menu. It is not
an optimal sample complexity, optimal calibration allocation or lower bound.
Units must match: a logical-CX cost cannot be added to seconds. In the CX check,
single-qubit calibration has zero CX but all its shots remain in total-shot
accounting. Circuit construction, compilation, routing and error correction
are not included, so the score is not end-to-end runtime.

Every refusal names the failed sufficient condition:

- Bias bound consumes the tolerance.
- Positive contrast cannot be established by the chosen screen.
- The calibration component consumes the tolerance under this radius bound.
- The pricing cap cannot satisfy the bound.

The limiting quantity B+S*d/c is a floor of THIS certificate, not a universal
identifiability lower bound. In particular, refusal does not prove the task
impossible; narrower calibration inversion or outcome-dependent CP intervals
can succeed where this uniform Hoeffding certificate does not.

## 4. Selection-validity argument

Condition on all calibration observations. The selected encoding and its
sample size are then fixed before any pricing outcomes. Hoeffding's bound
holds for the single selected fresh stream conditional on that calibration.
Unconditioning still bounds the validation failure probability by alpha_val.
Combine with the simultaneous calibration event using a union bound:

    Pr(any erroneous declaration in one invocation) <= alpha_cal + alpha_val.

No factor K is needed for validation because only one preselected fresh stream
is used. Calibration DOES pay the across-menu correction. Trying several
pricing streams and picking the nicest result is a different procedure and
would invalidate this argument. Repeated peeking at this fixed-time interval
is also unsupported: the earlier confidence-sequence module is separate.

At alpha_cal=alpha_val=.025 the statement is per-invocation unconditional
wrong-declaration control, not 95% coverage conditional on declaration or
simultaneous coverage over 1080 invocations. Every selected invocation has a
planned radius at most tau, but a confidence failure can still cause error.
Zero errors in this experiment does not make that risk zero.

This derivation specializes established CP, union-bound and Hoeffding ideas.
It is not by itself proof of publication novelty. See the contextual attribution
in [RESCUE_THEORY.md](RESCUE_THEORY.md) and the
[research report](QUANTUM_RESCUE_RESEARCH.md).

## 5. Fresh synthetic check: all outcomes

Archive: `results/journal_sprint/encoding_decision_v2`. The protocol used six
known contracts, three guards, two cost axes and 30 repetitions: 1080 trials.
Calibration and pricing RNG streams are new relative to rescue and pilot runs.
Reusing known contracts means this is not external validation or a clean test
of a previously unexamined application family.

| Outcome | Count |
|---|---:|
| Selected exact-table encoding and declared | 180 |
| Selected linearized encoding | 0 |
| No certificate within budget | 900 |
| Observed interval misses among declarations | 0 |
| Observed erroneous dollar declarations | 0 |

All 180 declarations are E001: 30/30 in each guard/axis cell. E014, E025,
E030, E038 and E049 have zero declarations in every cell. Detailed candidate
scores and all observations are retained, including rejected encoders.

For E001 with zero guard and the shots objective, mean pricing consumption is
376.43 shots. However, calibrating BOTH encodings costs 65536 shots, making the
mean total **65912.43**. At guards .003 and .03 these become 65942.87 and
66580.13 total shots respectively. Reporting only the small pricing count
would conceal the dominant cost. This is not an end-to-end shot saving over
the earlier fixed exact-encoding procedure, which used 65536 total shots at
its cap. Different calibration protocols also preclude a matched head-to-head
performance conclusion from these separate experiments.

Across all 2160 candidate assessments:

| Candidate status | Linearized | Exact table |
|---|---:|---:|
| Certified | 60 | 180 |
| Pricing budget not certified | 60 | 180 |
| Calibration bound exhausts tolerance | 600 | 720 |
| Bias bound exhausts tolerance | 360 | 0 |

The rule is therefore a tested conservative screening tool, NOT an improvement
over the previous successful E014/E025 fixed-interval results. Its false-negative
screening behavior and calibration overhead are the main development targets.

## 6. Verification and retained defect

Twenty-four focused tests passed: known-readout closed-form budget identity;
integer minimality; encoding tradeoff selection; nuisance-corner propagation;
exact enumeration of binomial noncoverage at six amplitudes; calibration
coordinate coverage; invalid inputs; refusals; tie behavior; and archive checks.

The v1 experiment completed all 1080 rows, but its replay inventory check
mistakenly excluded ALL files called complete.json, including the copied input
manifest. Fixed the exclusion to apply only to the output's root manifest and
added a nested-manifest regression. Preserved v1 and reran into v2 with the same
protocol and RNG namespace. Records are byte-identical, SHA256
`FAFCC1CCD2F257C7577B1A55976A2169BDB86E00A2793912EEDD42F7F924FFB8`.
This rerun is NOT another independent sample. Corrected replay verified all
1080 rows and 96 archived files; it also checks frozen input profiles and live
source hashes. Replay uses the same implementation; the algebra/coverage tests
provide separate reference checks, not independent human peer review.

Initial integrated regression passed 469 tests with 11 upstream warnings in
273.02 seconds (`tests_encoding_decision_v1.xml`). It collected before the two
additional archive/calibration tests; the post-fix focused suite passed all 24.
These are overlapping counts, not 493 distinct tests. Ruff passed all three new
Python/test files; local links and whitespace checks passed. See the
[project log](PROJECT_LOG.md). No historical inference module, manuscript claim
or original archive was changed.

## 7. Next research gates

1. Compare with a one-encoding calibration baseline at identical TOTAL budget.
   Prune candidates using deterministic dominance before acquiring calibration;
   the present protocol intentionally calibrates the entire fixed menu.
2. Derive a sharper prospective planner using exact calibration inversion or
   a paid pilot followed by independent validation. Do not tune using validation
   counts or label this worst-case bound a necessary sample size.
3. Optimize calibration allocation before acquisition, including guard floors.
   Adaptive calibration requires valid sequential calibration sets rather than
   repeated fixed-size CP checking.
4. Only then extend to amplified depths with explicit all-branch ambiguity,
   depth-dependent response assumptions and faithful modern AE baselines.
5. Test on a harder, explicitly approved pricing family against strong classical
   methods, with state loading and oracle construction charged. A certifier alone
   cannot create a quantum advantage.

Reproduce into a NEW directory (existing archives are immutable):

```powershell
venv\Scripts\python.exe -m research.journal_sprint.run_encoding_decision --output results/journal_sprint/encoding_decision_NEW
venv\Scripts\python.exe -m research.journal_sprint.run_encoding_decision --output results/journal_sprint/encoding_decision_NEW --verify
venv\Scripts\python.exe -m pytest research/journal_sprint/tests/test_encoding_decision.py -q
```
