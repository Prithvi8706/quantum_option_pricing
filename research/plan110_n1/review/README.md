# N2-reviewer (plan110 branch N, wave 2)

This is an adversarial review of `manuscript/advantage-frontier-2026-09-23/FRONTIER_NEGATIVE_RESULT_DRAFT.md` (sha256 `3d8e5900…c62b1c`). It was written on 12 October 2026 by an agent that did not write the draft.

## Resume note

Neither `research/plan110_n1/review/` nor `results/plan110_n1/review/` existed when this run started, so nothing was reused.

## Scripts

Both scripts are stdlib only and run under `.context/frontier_t0_env/Scripts/python.exe -I -S -B`. Each creates its output with exclusive create and appends rows to `results/plan110_n1/review/rows.jsonl`.

| Script | Output | What it does |
|---|---|---|
| `check_draft.py` | `results/plan110_n1/review/number_check.json` | Runs 78 checks of quoted draft numbers against the N1 and W0 files. 74 pass; 4 are flagged. It also computes the derived thresholds the review uses. |
| `confirm_dirsel.py` | `results/plan110_n1/review/dirsel_confirm.json` | Confirms the drafter's direction-select cross-products cell by cell. It also computes two alternative readings: the symmetric-rigour reading without U1, and the zero-bias-consistent reading. |

## Writes and limits

- Nothing outside `research/plan110_n1/review/` and `results/plan110_n1/review/` was written.
- No manuscript file was edited.
- No git commands, controllers, launchers or verifiers were run.

## Results

The review itself is `results/plan110_n1/review/REVIEW.md`.
