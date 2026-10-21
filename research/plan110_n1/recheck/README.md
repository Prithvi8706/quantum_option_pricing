# N2 re-check workspace (plan110 branch N)

- **`recheck_draft.py`** checks the numbers in `FRONTIER_NEGATIVE_RESULT_DRAFT_v2.md` programmatically.
  - It is adapted from `../review/check_draft.py`.
  - It re-derives every number that v2 adds from the primary N1 and W0 files, and keeps the fixer's value as a second column.
  - It also runs probes for new defects.
  - It is stdlib only. Run it from the repository root:

    `.context/frontier_t0_env/Scripts/python.exe -I -S -B research/plan110_n1/recheck/recheck_draft.py`

    Add `--dry` to print results without writing any files.
  - It writes `results/plan110_n1/recheck/number_recheck.json` (exclusive create) and appends rows to `results/plan110_n1/recheck/rows.jsonl`.
- **The report** is `results/plan110_n1/recheck/RECHECK.md`.
