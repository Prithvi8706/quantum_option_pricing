# PR #2 verification and remaining-work checklist

2026-09-16. Integration scope: weeks 10-11 and prospective forward planning.
This checklist distinguishes a software integration gate from a publication gate.

## Integration sweep

Verification source: `0796cb744375fac614c565a8f64fa8420c05b60d`, checked out in a
separate Windows worktree. Subsequent PR changes are documentation and verification
reports only. Existing Python 3.9 environment reused; fresh installation untested.

- [x] Read PR review/comment/check state: no review comments; Macroscope SKIPPED,
  not an approval. No hosted test workflow; local results must not be called CI.
- [x] Review changed implementation, inference interfaces, cost accounting,
  benchmark schedules, tests and evidence-extraction safeguards.
- [x] Verify/extract all 3708 bundled files without changing producer manifests.
- [x] Check all 12 complete archive inventories and hashes; preserve the incomplete
  rescue first attempt and all superseded evidence.
- [x] Bounded credential-pattern review of all 83 original PR files and ZIP members;
  no flagged matches. Not an exhaustive security guarantee.
- [x] Ruff on all changed Python files and Git whitespace checks pass.
- [x] Independently reconcile week-11 schedules, row counts and exactly two events
  per completed attempt: 132 pilot, 384 reference and 2308 main/warmup rows.
- [x] Independently recompute 144 RMSE cells and evaluation/training totals;
  maximum RMSE difference `3.47e-18` dollars.
- [x] Check all 299 local links in the original 101 sprint Markdown documents.
- [x] Correct the stale roadmap instruction: week 11 is development-complete;
  the next implementation block is week 12.
- [x] Preserve original archives, unrelated untracked files and six-edit user stash.

- [x] Full suite: **580 passed, 11 legacy Qiskit warnings, 381.48 seconds**;
  `results/journal_sprint/tests_pr2_merge_v1.xml`. Only pre-existing tracked
  pytest bytecode was regenerated in the disposable checkout; source unchanged.
- [x] Week-10 extension: 83 cases; rescue: 4320 rows; encoding v2: 1080 rows;
  allocation: 3240 rows; shortlist: 768 estimates, 192 references, 72 Heston
  diagnostics and 40 nested rows across eight levels; pilot: 132 rows.
  Report: `results/journal_sprint/pr2_merge_replays_v1.json`.
- [x] Pilot confidence-sequence reanalysis: 2160 rows, with 4320 input rows
  verified; `results/journal_sprint/pr2_merge_pilot_cs_v1.json`.
- [x] Week-11 reference numerical replay: all 384 rows / 490 files, complete.

- [x] Week-11 main numerical replay: all 2308 rows / 2415 files, complete;
  saved numerical results reproduced, not timings.
- [x] Final working-document link audit: 306 local links across 102 sprint documents,
  no missing targets (before adding the PR-state link below).

Integration decision: **GO for the user-authorized merge**, with no new unresolved
implementation blocker found in this bounded sweep. This is not an independent
human review or a guarantee of defect-free software. The actual merge event and
commit are recorded by [PR #2](https://github.com/Prithvi8706/quantum_option_pricing/pull/2).

## Historical replay disposition

`encoding_decision_v1` is preserved historical evidence, not the preferred runner.
The current strict verifier rejects its old producing source; its frozen verifier
also contains the already documented nested-`complete.json` inventory bug.
Neither rejection was hidden or corrected inside the immutable archive.
A supplemental audit verified all 96 files, frozen source hashes, 1080 original
producer rows and their summary using a separate frozen-source reconstruction.
The corrected v2 archive is the current replay target. See
[original defect disposition](ENCODING_DECISION_RULE.md).

Parallel verification reruns test numbers, not runtime performance; no new timing
claim, confirmation sample, quantum experiment or paid job was produced.

## Completed development

- [x] Weeks 1-9 foundation and earlier review fixes (PR #1).
- [x] Week-10 development evidence gate, with confirmation/submission NO-GO retained.
- [x] Finite-grid payoff rescue, encoding-aware planner and equal-calibration
  allocation experiment; negative/tied outcomes retained.
- [x] Hard-pricing survey and bounded follow-through diagnostics.
- [x] Week-11 error/resource interface, stronger classical Asian/basket references,
  benchmark, novelty matrix and week-12 development manifest.

## Remaining work: five planned blocks

- [ ] Week 12: unequal-calibration/target-delivery policy, cost-aware fixed comparator,
  fresh-sample validity argument, bounded runtime pilot, then gated development study.
- [ ] Week 13: small harder-payoff quantum encoding, structured state-preparation
  feasibility, componentwise error and full resource accounting.
- [ ] Week 14: matched end-to-end classical/quantum comparisons, nonzero-depth AE,
  ablations and an explicit novelty/confirmation decision.
- [ ] Week 15: fresh held-out confirmation only after its gate; independent
  reproduction in a fresh environment and uncertainty analysis.
- [ ] Week 16: manuscript/artifact audit, current venue/fee assessment, actual
  external critique, contribution records and human submission approvals.

## Still-open scientific and publication gates

- [ ] Establish a defensible quantum contribution; no novel quantum algorithm or
  quantum advantage is currently demonstrated.
- [ ] Justify encoding/loading/arithmetic error bounds and matched total costs;
  the contract schema does not prove caller-supplied bounds.
- [ ] Establish a useful method distinction against strong prior-work comparators;
  equal-calibration delivery tied fixed CP, and matched-N error is not matched-cost advantage.
- [ ] Validate portability/fresh dependency installation and resolve legacy-stack
  maintenance risks before claiming broad reproducibility.
- [ ] Obtain real collaborator/human review and final author approval; no honorary
  authorship or review credit is implied by this merge.
- [ ] Pass confirmation and submission-readiness gates. Merging code does not pass them.

See [active roadmap](WEEKS_11_16_IMPLEMENTATION_PLAN.md) and
[publication checklist](../JOURNAL_REENGINEERING_CHECKLIST_2026-09-09.md).
