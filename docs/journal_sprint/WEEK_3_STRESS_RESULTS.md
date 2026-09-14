# Readout and dependence stress results

Completed under [PROTOCOL_W3_STRESS.md](PROTOCOL_W3_STRESS.md). This is a
response-sampling experiment using saved actual ideal pricing-circuit targets,
not a new device or gate-noise simulation. Outputs are in
`results/journal_sprint/week3_stress_v1/`.

## Results

Four contract/scale groups each use 500 independent repetitions per condition,
with 1024 observations at each of k=0,1,2. The readout case is analyzed twice
using exactly the same counts. There are 8000 distinct synthetic datasets and
10000 inference records, not 10000 independent acquisitions.

| Condition / analysis | Amplitude containment range across four groups |
|---|---:|
| Ideal independent binomial | 93.4–96.4% |
| Asymmetric readout, ignored | 0–9.0% |
| Asymmetric readout, known correction | 94.4–96.8% |
| Ordered-batch drift, ignored | 0–12.2% |
| Beta-binomial dependence, ignored | 12.6–16.6% |

These are descriptive ranges over four fixed discovery groups, not confidence
intervals or population-wide guarantees. The lowest ideal result, 467/500, has
a marginal exact 95% binomial interval approximately [90.86%,95.41%]; its observed
93.4% does not alone contradict a nominal 95% coverage statement. No multiplicity-
adjusted inference or coverage-based retuning was performed.

The readout correction assumes the stipulated error rates are known exactly:
`q_report=.02+.91*q_ideal`. It first constructs the simultaneous binomial
intervals for reported outcomes, inverts this affine map, then retains all
sinusoidal branches. It does not merely correct a point estimate. Uncertainty
in estimated readout rates would require a further calibrated envelope and
failure budget; these results do not establish that extension.

The drift condition uses a common random sign on ordered-depth offsets
.03*(-1,0,1). The dependence condition draws a latent probability per depth from
a beta distribution with the correct ideal mean and concentration 100, then
conditionally samples a binomial count. The resulting unconditional shot law
is overdispersed. These models stress stationarity and independence; they do
not characterize real hardware drift.

## Precision-selection warning

The secondary amplitude-radius target is .005, not a dollar target. With known
readout correction, erroneous declarations occur in 1.2–1.6% of all attempts,
but 15.0–44.4% of declarations. In the E030/c=.25 group, only 18/500 trials
declare this radius and 8 of those 18 are erroneous.

This distinction matters: a fixed-sample confidence construction controls
unconditional noncoverage, not error conditional on a data-selected narrow
interval. A procedure can declare precision rarely and still have poor reliability
among those declarations. The result cannot be described as “95% correct whenever
precision is declared.” A stronger selective guarantee or a redesigned validation
rule would need its own proof and prospective test.

Ignoring readout at c=.25 produces incompatible sets in all 500 trials for each
contract. Zero erroneous declarations there reflects no delivery, not useful
reliability. Conversely, nonempty intervals under drift can be systematically
wrong; nonemptiness does not validate the model.

## Integrity and cost

All 50 archived artifact hashes verified. The 10000 records correspond to 8000
unique dataset IDs: 6000 analyzed once and 2000 readout datasets analyzed twice.
Counts are in range, and paired analyses use identical observations.

Each distinct dataset represents 3072 shots, 9216 A-equivalent calls and 3072
Grover calls under its stipulated schedule. Totals are 24,576,000 synthetic shots
and 73,728,000 A-equivalent calls. Reanalysis does not double these acquisition
costs. These are response-study accounting quantities, not executed hardware calls.

Updated sprint suite: **73 passed, 11 legacy warnings, 18.38 seconds**; XML is
`results/journal_sprint/tests_week3_stress.xml`. Ruff passes. The full repository
suite was not rerun for this change. Existing experiment outputs and manuscripts
were preserved.

## Decision

The readout/dependence stress milestone is complete at the response-model tier.
Do not transfer the independent stationary-binomial guarantee to drift or
correlated shots. Known affine readout inversion is a working baseline, not a
complete hardware calibration solution. Retain conditional-declaration error as
an explicit outcome in the main study.

Next implement the costed classical MC/RQMC baseline harness, then return to
the stronger comparator and validation-design questions before confirmation.
