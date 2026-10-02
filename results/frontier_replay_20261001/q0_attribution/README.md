# Q0 attribution diagnostics (1 October 2026)

Separately labelled diagnostics for the Stage B Q0 mismatch (see
`manuscript/advantage-frontier-2026-09-23/STAGE_B_RESULTS.md`). They do not replace Q0.
The scripts are kept exactly as they ran, so they are excluded from lint
(`pyproject.toml`), and known blemishes are listed here instead of being edited.

## Inputs that are not tracked

- `dump_conda_1264.npz`, `dump_t0_202.npz` and `dump_t0_202_eigh1264.npz` (41 MB each,
  written by `boundary_dump.py`) live untracked in `.context/frontier_q0_attribution_dumps/`.
  `attribution_diagnostic_L.py` and `scramble_inprocess.py` read the first one from this
  folder, where it stood when they ran; `summarize.py` reads all three from `.context`. On a
  clean clone, regenerate them with `boundary_dump.py` (numpy 1.26.4 interpreter for
  `conda_1264`, the T0 interpreter for the other two) and place them accordingly. Their
  factor hashes are recorded in `attribution_summary.json`.
- `order_8x52_numpy1.26.4.npy` was written by an inline command, not a committed script,
  under the anaconda interpreter (numpy 1.26.4):
  `np.save("order_8x52_numpy1.26.4.npy", np.argsort(np.load("eigh_8x52_numpy1.26.4.npz")["vals"])[::-1])`.
  Note: `eigh_8x52_numpy1.26.4.npz` was computed with multithreaded MKL (diagnostic 1).

## Known blemishes (not edited)

- `attribution_diagnostic.py` imports `os` without using it.
- `attribution_diagnostic_L_single_thread.py` (diagnostic 2b) has a garbled docstring from
  a scripted edit: it names itself "diagnostic 2", and a sentence about diagnostic 2a is
  spliced mid-clause. Because the script stores `purpose=__doc__`, the garbled text is also
  in `attribution_result_L_single_thread.json`. The meaning is in STAGE_B_RESULTS.md.
- `summarize.py` sets `pooled_run_repeatable_in_T0` twice; the second assignment (a
  field-by-field comparison) is the recorded value.
