# Prospective analysis specification, Stage B — 1 October 2026

Stage B covers plan items **T0** (pinned environment) and **Q0** (provenance replay).
This file is committed before the environment is built and before any replay runs.
It is a separate file so the Stage A specification, whose hash Stage A verification
checks, stays byte-identical. It does not preregister C1–C8, Q4 or X1; those need
their own extension before they run (ANALYSIS_SPEC.md, "Deferred work").

## Author decisions recorded on Day 1 (1 October 2026)

- CUDA wheels may be downloaded into the pinned environment for the GPU comparator (C6).
- The draft may be sent to a model from a different provider for internal review rounds.

## T0: pinned environment

- Interpreter: CPython 3.12.4 (`py -3.12`), a fresh `venv` at `.context/frontier_t0_env`
  with no system site-packages. `.context/` is gitignored; the lock and receipt are tracked.
- Top-level pins are in `research/frontier_replay_20261001/t0_requirements.in`. The full
  closure was downloaded from PyPI as binary wheels into `.context/frontier_t0_wheelhouse`.
  `t0_requirements.lock` lists every wheel as `name==version` with its SHA-256.
- One numpy, 2.0.2: the newest version numba 0.60 supports, and the version the
  original P1, P2, decision and frontier runs used. P3 and Q1 originally ran with numpy
  1.26.4 in other interpreters, so any P3/Q1 difference in Q0 is attributed to that change
  and recorded, not tuned away.
- Qiskit 1.4.6 (latest 1.x resolved). None of the six Q0 scripts imports Qiskit; it is
  present for the existing compiler tests. The 0.45 series used earlier was not tested
  against numpy 2 and is not used.
- CUDA: numba-cuda 0.30.4 with the CUDA 12.9 wheels (`cu12` extra), for C6 only.
- Install: `pip install --no-index --find-links <wheelhouse> --require-hashes --no-deps
  -r t0_requirements.lock`.

**T0 passes when** the hash-checked install succeeds, `pip check` reports no broken
requirements, the installed distributions (excluding pip) equal the lock exactly, and
each top-level package imports. The receipt `results/frontier_replay_20261001/t0_environment.json`
records the interpreter, lock hash, installed versions, CPU, GPU, driver, power plan and
the MiKTeX/latexmk versions. A CUDA smoke kernel (elementwise add, checked against
numpy) runs on the GPU; its result is recorded. A failed smoke test does not fail T0,
but blocks C6 until fixed, and the fix is recorded.

## Q0: provenance replay

- Checkout: a detached git worktree of the commit containing this file, at
  `.context/frontier_q0_replay_20261001`. Its commit SHA is recorded.
- Scripts, in the 24 September order, all with the T0 interpreter, from the checkout root:
  P3 `barrier_fast_classical.py`, P1 `classical_exponent_pilot.py`, P2 `barrier_oss_pilot.py`,
  Q1 `barrier_oracle_depth.py`, `barrier_decision.py`, `frontier.py`
  (all in `research/advantage_frontier_20260923/`). No script is edited.
- Comparison: the archived JSON in the main repository against the checkout's regenerated
  JSON, using `walk` and `timing_key` imported unchanged from
  `provenance_replay_diff.py`. Its timing classification is not revised. The report goes
  to a new file, `results/frontier_replay_20261001/q0_provenance_replay.json`. The
  24 September report `provenance_replay_20260924.json` is never overwritten.
- Recorded per script: exit code, wall time and log. Recorded per archived file: exact
  fields compared, exact mismatches with archived and replayed values, and the number of
  timing-derived fields that changed.

**Q0 passes when** all six scripts exit 0 and there are **zero exact-field mismatches**,
with the exact-field count per file equal to the 24 September counts (1,611; 108; 57;
209; 2,112; 270; total 4,367). A changed count means the output structure changed and
is itself a failure.

**If Q0 fails:** the mismatch paths and values are reported and added to ERRATA as a new
entry. The archived values are not changed. Nothing is re-run in a different environment
to make it pass. An attribution run (for example P3 under the 24 September anaconda
interpreter) is allowed only as a separately labelled diagnostic, and it does not replace
the Q0 outcome.

Timing fields are re-measured on the same laptop and are not judged. They are not the C2
timing study. The replayed stop/continue decision is reported for information, next to
the archived decision.
