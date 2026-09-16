# Week14 closeout and handoff

The allowed **finite-target development** is complete. The conditional original
continuous end-to-end comparison is not: week13 admitted no application encoding.
No new quantum algorithm, continuous-price certificate or quantum advantage is
claimed. Week15 confirmation remains NO-GO; see the explicit
[claim matrix and gate](WEEK_14_CLAIMS_GATE.md).

## Implementation checklist

- [x] Freeze finite-target scope, methods, budgets, seeds and analysis before run.
- [x] Implement actual k=0..4 raw/residual circuits and independent density checks.
- [x] Integrate pinned native finite-shot IQAE, preserving native stopping/counts.
- [x] Run source-faithful csAE with applicable known-noise response model;
  distinguish point estimates from interval-based precision delivery.
- [x] Compare fixed direct/depth-limited sampling, all five week12 policy arms,
  calibration/pilot/transfer/noise ablations and finite classical/direct-sum baselines.
- [x] Record paid/projected costs, source identities, raw checkpoints, failures
  and caps without discarding negative outcomes; no hardware timing claim.
- [x] Complete93tasks/912trial outcomes and20response checks; archive2022files.
- [x] Strict numerical replay,58cell analysis, claims/resource report.
- [x] Clean checkout72focused tests and93task/2022file strict replay; same environment.
- [x] Independent scientific evidence review ACCEPT after wording corrections.
- [x] Independent software/provenance evidence review ACCEPT; final half-width
  terminology correction applied to claim matrix.
- [x] Prepare bounded collaborator-review packet; explicitly leave signatures pending.
- [ ] Continuous application admission, defensible prior-work distinction and
  signed confirmation protocol. These remain scientific gates, not completed tasks.

## Reproduction

Use the existing pinned Python3.9.13/NumPy2.0.2/SciPy1.13.1/Terra0.46.3
environment; default system Python is not equivalent. No package upgrade made.
The strict verifier enforces native IQAE/Sampler hashes and20project/protocol
source hashes, not every transitive installed package file.

```powershell
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$env:PYTHONDONTWRITEBYTECODE='1'
venv/Scripts/python.exe -m pytest -q
venv/Scripts/python.exe -m research.journal_sprint.run_w14 verify results/journal_sprint/w14_finite_v1
venv/Scripts/python.exe -m research.journal_sprint.w14_analysis results/journal_sprint/w14_finite_v1 results/journal_sprint/w14_analysis_new.json
```

Analysis outputs require absent paths. Do not write receipts into the immutable
archive. A new `run` requires an exclusive new output directory and is another
development run, not automatically fresh confirmation. A clean source checkout
with the same existing environment is not fresh-environment reproduction.

Producing freeze76914458; evidence/review commits are recorded in Git. Branch
`research/week14-comparisons` includes preceding local week13 work. No push,
PR or merge was requested for this turn and none was performed. Unrelated
untracked archives, user files, stash and existing worktrees are preserved.

Verification:807repository tests passed in two disjoint invocations
(609journal tests,198tests/paper_a tests); clean checkout1fbea8b6 passed72new
tests and the full strict replay. Producing code is unchanged since76914458;
the clean checkout used the same existing environment, not a fresh installation.
Scientific and software evidence reviews accepted; four documented wording
corrections applied. No remaining implementation/archive/review blocker within
the declared finite-target development scope. Scientific application and
confirmation gates remain unresolved as listed above.

Two planned blocks remain (weeks15-16), subject to the unresolved gate. Safe
next work is explicit gate-resolution research/replanning, not an automatic
week15 confirmation run. See [results](WEEK_14_RESULTS.md),
[independent review](WEEK_14_REVIEW.md), and [gate](WEEK_14_CLAIMS_GATE.md).
