# Week 4 closeout

13 September 2026. The four planned local research milestones are complete at
discovery/draft scope. This is not completion of the paper, confirmation, or the
requested dual-provider review gate. No PR or submission has been created.

## Delivered

1. Finite-shot readout calibration: conservative uncertainty propagation and
   1200 synthetic datasets / 3600 analyses, with calibration costs retained.
2. Calibration transfer and preparation stress: 6000 attempted datasets,
   4000 acquisitions and 2000 pre-refusals; two inference methods share data.
3. Dollar-precision propagation: 8000 executed inferences with unchanged
   analytical representation bounds, per-cell denominators and erroneous
   declarations separated from interval noncontainment.
4. [Week-5/6 fixed-validation contract](WEEK_5_6_VALIDATION_CONTRACT_DRAFT.md):
   model-conditional readout-only scope, fixed validation, no target-answer
   leakage or uncounted acquisition, and explicit prerequisites for confirmation.

Results: [calibration milestone](WEEK_4_PROGRESS.md) and
[transfer/dollar experiment](WEEK_4_TRANSFER_RESULTS.md).

## Verification and independent check

- Final repository regression: **271 passed**, zero failures/errors/skips,
  11 legacy warnings; `results/journal_sprint/tests_week4_integrated_v1.xml`.
- Sprint run: 107 passed. These tests overlap the full run; do not add totals.
- Ruff and tracked whitespace checks passed.
- All 61 transfer-run artifact hashes and all 6000 trial identities checked;
  all 8000 executed inferences, raw observations and summary/cost arithmetic
  reconstructed in `results/journal_sprint/week4_transfer_verify_v2`.
- Bounded review requested with `gpt-6-astra` found no P0/P1 issue or
  demonstrated enclosure/truth-leakage defect. The ambiguous erroneous-
  declaration table heading and stale verification reference were corrected.
  It did not independently re-execute every test or reconstruct every trial.
- Macroscope remains unconnected. Its review, and therefore the PR, remain held.

The previous calibration milestone's 46 hashes and 1200 observations were
checked separately. Reconstruction reuses numerical inference code and stored
bounds/truths; it is not independent mathematical or floating-point certification.

## Scientific decision and next work

Within stipulated transfer bounds, guarded intervals contain the target in all
tested executed cells, but useful $1 delivery is largely restricted to E001.
When those bounds are exceeded, narrow wrong intervals can still be returned.
Neither a nonempty result nor a precise result validates its own assumptions.
The experiments do not establish quantum advantage, hardware reliability,
universal coverage, or correctness conditional on delivery.

Start week 5 with strong fixed-design resource/precision comparisons and the
remaining compiled schedule profiles before developing an adaptive controller.
Justification of real transfer allowances, comparator fairness, numerical scope
and a frozen prospective analysis remain necessary before held-out confirmation.

The original schedule now has **12 planned working weeks remaining (5–16)**,
plus its 4–8 week reserve. This is an estimate to submission readiness, not
acceptance. Contribution approvals and publication spending remain unconfirmed.
