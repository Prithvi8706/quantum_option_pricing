# Week 4 progress: finite-shot readout calibration

Latest: [transfer stress and dollar-precision results](WEEK_4_TRANSFER_RESULTS.md)
and the [week-5/6 validation draft](WEEK_5_6_VALIDATION_CONTRACT_DRAFT.md).
The local week-4 research milestones have now been executed/drafted; independent
Astra review is complete, with its documentation corrections applied. Final
integrated verification passed all 271 tests. See the [closeout](WEEK_4_CLOSEOUT.md).
The text below
records the first milestone, not the current total of completed work.

First milestone complete; week 4 is still in progress. Governed by the
[prospective protocol](PROTOCOL_W4_CALIBRATION.md), with remaining work in the
[week-4 plan](WEEK_4_PLAN.md). This does not alter completed week-3 artifacts.

## Executed discovery result

1200 distinct synthetic datasets, each analyzed three ways, produced 3600
inferences. The uncertainty-aware method accounts for both calibration and
validation error budgets. A plug-in comparator ignores calibration uncertainty;
the known-rate oracle is diagnostic, not deployable.

| Calibration shots per state | Plug-in containment across 3 cells | Finite-calibration containment across 3 cells |
|---|---:|---:|
| 256 | 121–164 / 200 (60.5–82%) | 200 / 200 in each cell |
| 4096 | 183–192 / 200 (91.5–96%) | 199–200 / 200 (99.5–100%) |

The conservative intervals are wider. For example, at a=.4 their median radii
are .021625 (256/state) and .012131 (4096/state), versus approximately .00875
for the oracle. Increasing calibration cost narrows the uncertainty-aware
interval, but does not establish an optimal calibration allocation. No cell
with 200 trials establishes zero risk or certifies a universal coverage rate.
Median radii in the archive use nonempty intervals; incompatibility counts
are retained separately rather than silently discarded.

Every dataset uses 3072 validation shots and 9216 validation A-equivalent calls.
Calibration adds 512 or 8192 shots, yielding 3584 or 11264 total shots per
dataset. Entire experiment: 8,908,800 shots, with 11,059,200 pricing-validation
A-equivalents. These are different units. Calibration preparations are not
silently counted as free, or charged as complete pricing-A operations.

## Checks and limitations

- Sprint regression: 95 passed, 11 legacy warnings, 11.35 seconds. Full-repository
  tests were not rerun for this milestone; week 3's 253-test report is historical.
- Ruff passes. All 46 archive hashes verified.
- All 1200 seed-separated calibration and validation datasets reconstructed;
  all finite-calibration components/containment flags and shot totals checked.
- Verification reuses the numerical inversion implementation: it is an artifact
  reconstruction check, not an independent proof or independent agent review.
- Exact conservative containment is conditional on stationary shared rates,
  independent shots, perfect calibration-state preparations, and valid numerical
  inversion. Floating-point padding is not formal numerical certification.

Next: calibration-transfer/drift stress, then dollar-precision propagation and
the fixed-validation contract. Gate noise, imperfect calibration preparation,
conditional correctness among declarations and held-out confirmation remain
unresolved. No hardware or submission work was performed. The week-3 Astra
audit does not cover these new files; Macroscope and the PR remain pending.

Run: `python -m research.journal_sprint.run_calibrated_readout --output <new-directory>`.
Archive: `results/journal_sprint/week4_calibration_v1`.
