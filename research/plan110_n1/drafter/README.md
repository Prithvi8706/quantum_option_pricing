# N2-drafter (plan110 branch N, wave 2)

This workstream wrote the draft
`manuscript/advantage-frontier-2026-09-23/FRONTIER_NEGATIVE_RESULT_DRAFT.md`, on 12 October
2026.
- The file was created new and does not overwrite anything.
- No existing manuscript file was edited.

## Resume note

The run began after the logout. Neither `research/plan110_n1/drafter/` nor
`results/plan110_n1/drafter/` existed, and the draft file did not exist, so there was
nothing to reuse.

## Scripts

Both scripts run under `.context/frontier_t0_env/Scripts/python.exe -I -S -B` (3.12.4,
stdlib only). Both create their outputs with exclusive create, and both append rows to
`results/plan110_n1/drafter/rows.jsonl`.

- **`draft_numbers.py`** writes `results/plan110_n1/drafter/draft_numbers.json`.
  - It copies every quoted value from the N1 headline, estimator and hwclassical JSONs.
  - It checks 10 arithmetic identities; the largest relative error is 1.8e-16. The
    identities include M = k / k_10x, the split 232 = 74.8 × 3.10, and distribution-free
    M = M_practice / factor.
  - **Known defect, left unfixed (no overwrite).** The field `certified_k_range_0.45eps`
    reads [532.5, 1066.7], because it mixes in the non-dyadic conditional-credit rows.
    The correct certified range is 585.8-1066.7. That value is recorded in a correction
    row in `rows.jsonl`, and it is the one the draft uses.
- **`draft_addendum.py`** writes `results/plan110_n1/drafter/addendum.json`.
  - It multiplies the N1-estimator direction-select ratios into the N1-headline pairs and
    the N1-hwclassical distribution-free M values. No single N1 file contains these
    combinations.
  - Result: the explicit class with all-free + 1 lane vs 1 core gives M = 0.97, and
    all-free + distribution-free gives 0.27.
