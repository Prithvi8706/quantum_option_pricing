# Week 4 transfer stress and delivered dollar precision

Discovery results from [the prospectively declared protocol](PROTOCOL_W4_TRANSFER_PRICE.md).
No hardware, paid jobs, confirmation cases or comparative advantage claim.

## Matrix and verification

Six existing discovery contracts, n=6/scale=.125, five readout/preparation
conditions and 200 attempts per cell: **6000 attempted datasets**. The sufficient
deterministic bound rejects E030/E038 before acquisition, leaving **4000 executed
datasets and 2000 pre-refusals**. Each executed dataset supplies the same counts
to unexpanded and guarded analyses, giving 8000 executed inferences plus 4000
refusal records across both methods. Inference reuse is not extra acquisition.

The guarded analysis expands calibration-rate intervals by supplied .03 bounds
per rate. The stationary, constant/depth-dependent .03 transfer and .02 imperfect
preparation conditions lie within those synthetic bounds. The .08 false-positive
shift deliberately does not. The bounds were declared, not inferred from data.

All 61 run-artifact hashes verified. Reconstruction checked 6000 unique attempts,
all acquired counts and seed namespaces, 8000 interval/decision records, all
summary denominators and all cost totals. This reconstruction reuses the
implementation and does not substitute for independent mathematical review.

## What the experiment establishes within its scope

Within the supplied transfer bounds, every guarded executed cell contains the
true amplitude and continuous price in 200/200 trials. This finite observation
does not prove zero error or certify coverage universally. Its analytical
interpretation remains conditional on the specified sampling/rate assumptions
and conservative numerical inversion.

Useful dollar delivery is much more limited:

| Guarded condition | E001 $1 deliveries / 200 | E014/E025/E049 deliveries / 200 each |
|---|---:|---:|
| Stationary | 200 | 0 |
| Constant transfer | 200 | 0 |
| Depth-dependent transfer | 200 | 0 |
| Imperfect calibration preparation | 31 | 0 |

Thus containing the true price does not mean the interval is useful at the
requested tolerance. More validation shots cannot automatically eliminate a
supplied transfer allowance; calibration and model assumptions must be part of
the resource-selection question. This experiment does not prove an absolute
precision floor for all representations or estimators.

Without guard expansion, constant transfer makes all executed trials
incompatible. Depth transfer makes all but one incompatible. With imperfect
preparation, all intervals remain nonempty but amplitude containment is only
25/48/63/102 out of 200 for E001/E014/E025/E049 respectively. These outcomes
illustrate failures of calibration transfer, not a theorem about arbitrary
device noise.

## Deliberately exceeded assumptions

Under the .08 shift, every guarded executed interval misses the true amplitude
and price, including cases that nonetheless declare $1 precision:

| Contract | Declarations / 200 | Erroneous declarations | Errors among declarations |
|---|---:|---:|---:|
| E001 | 108 | 0 | 0 / 108 |
| E014 | 67 | 67 | 67 / 67 |
| E025 | 102 | 102 | 102 / 102 |
| E049 | 13 | 13 | 13 / 13 |

E001 is not contradictory: an interval can miss the target while its midpoint
is still within the larger requested $1 tolerance. Containment of the reported
interval and midpoint accuracy at tolerance are distinct outcomes. For E025,
the erroneous-declaration rate per executed/attempted trial is 102/200=51%,
while conditional error among declarations is 102/102=100%. Do not exchange
these denominators. This table counts midpoint errors only when precision was
declared, not errors among all returned unresolved intervals. No nominal
guarantee applies to this out-of-bound condition.

The guard is not a detector of arbitrary misspecification. In particular, a
nonempty narrow interval cannot establish validity of its own transfer bound.

## Cost and handoff

Across actual acquisitions: 393,216,000 synthetic validation shots and
32,768,000 synthetic calibration shots, totaling **425,984,000 shots** represented
by binomial draws. Pricing validation uses **1,179,648,000 A-equivalent calls**.
These are simulated resource counts, not circuits physically executed or a
runtime forecast. Each accepted task uses 106,496 total shots; refused tasks
use none, while their classical bound setup times are retained.

Sprint regression: 107 tests passed, 11 legacy warnings, 13.28 seconds; Ruff
passes. Final integrated regression: **271 passed**, zero failures/errors/skips,
11 legacy warnings, 240.17 seconds; XML is `tests_week4_integrated_v1.xml`.
The bounded Astra review found
no P0/P1 issue or demonstrated enclosure/truth-leakage bug. Its table-heading
and artifact-reference corrections are applied here. It did not duplicate
every reconstruction or test, and its inspection is not formal certification.
Macroscope remains unconnected and the PR remains held.

The [week-5/6 draft contract](WEEK_5_6_VALIDATION_CONTRACT_DRAFT.md) retains
model-conditional readout-only scope and prohibits oracle leakage, repeated
fixed-alpha validation and uncounted calibration/pilot costs. It does not freeze
confirmation. The next substantive question is useful fixed-design delivery
versus full cost before attempting adaptive resource selection.

Artifacts: `results/journal_sprint/week4_transfer_price_v1` and
`results/journal_sprint/week4_transfer_verify_v2`.
