# Week 6 closeout

13 September 2026. **All planned local week-6 discovery work is complete**:
execution, reconstruction, predefined analysis, bounded separate review,
regression checks and next-stage decision. This is not paper completion,
held-out confirmation or completion of the external Macroscope/PR gate.

## Step-by-step record

1. Finalized [transfer-grid protocol](PROTOCOL_W6_TRANSFER_GRID.md), based on
   the prior draft, before drawing observations. Recorded all C6, nine rate
   positions, two calibration budgets, three fixed designs, 100 repetitions,
   confidence allocation and between-cell runtime/storage limits. Protocol and
   dependency hashes entered the local planned record; not external registration.
2. Implemented fixed-design runner with distinct calibration/validation seed
   namespaces and explicit extra calibration costs. Bounds/refusals/designs
   precede diagnostic target access. Sixteen targeted tests passed before run.
3. Completed 32400 attempts in 29.43 seconds: 21600 acquisitions and 10800
   pre-refusals. Saved raw observations, all confidence-set components, statuses,
   costs, 324 summaries and original producing-source snapshots.
4. Reconstructed 32400 unique trial identities and all summaries, bounds,
   targets, schedules and costs. Checked 71 archive and 66 planned dependency
   hashes. Shared producing helpers make this consistency replay, not independent
   mathematical/numerical certification. Future source drift fails closed.
5. Calculated all 162 calibration contrasts, 216 multidepth/direct contrasts
   and 36 nine-position ranges. [Results](WEEK_6_RESULTS.md) retain rare successes,
   misses and undefined denominators rather than reporting only favorable cells.
6. Full regression passed **304 tests**, with 11 legacy dependency warnings in
   189.06 seconds. Ruff and tracked whitespace checks passed. No producing code
   changes were needed after this test run; later changes clarify documentation.
7. Separate review requested with `gpt-6-astra` initially hit a usage limit;
   resumed after the user's refresh. Final claim check found no blocking
   scientific-reporting issue. Corrected compiled-depth wording to distinguish
   cross-contract maxima/E001 from the other contracts. Explicitly documented
   the current verifier's live-source replay limitation. This is bounded
   automated review, not a human referee report or independent full proof.
   The reviewer executed the closeout with output creation intercepted: all
   32400 records, 324 summaries and 71/66 hash checks passed through the existing
   implementation. Separate audit calculations checked saved-summary contrasts,
   raw containment misses, table values and costs. It personally ran 12 targeted
   tests (all passed), but did not rerun the 304-test integrated suite. No
   truth leakage, uncharged acquisitions or configuration mismatch was found.
   Those targeted tests overlap the integrated suite and are not extra unique tests.
8. Recorded **no-go for adaptive promotion or a confirmatory main matrix**.
   [Week-7 entry gate](WEEK_7_GATE_DRAFT.md) calls for separately declared
   pricing/calibration/guard ablations and fair-comparator design first. That
   future ablation was not silently added to or claimed as a week-6 result.

## Outcome

2729 precision declarations, 18871 unresolved acquisitions, no incompatibilities.
Price containment was 21597/21600: three misses, all unresolved. No erroneous
$1 declaration was observed; this does not prove zero risk or conditional coverage.
E001 accounts for 2724 declarations; E014 one, E025 four, E049 zero.
E030/E038 remained pre-refused, not removed from the attempt denominator.

E001 CX-capped delivery spans 0–99% across positions at lower calibration and
2–99% at higher calibration. Fourfold calibration does not make cheap-gate
delivery uniformly high. A-matched's strong E001 delivery costs about 15.62
times direct's pricing CX. Neither is a general quantum/classical advantage.

## Evidence and reproduction

- Raw archive: `results/journal_sprint/week6_transfer_grid_v1`.
- Reconstruction/contrasts: `results/journal_sprint/week6_closeout_v1`.
- Tests: `results/journal_sprint/tests_week6_integrated_v1.xml`.
- Source: `research/journal_sprint/run_transfer_grid.py` and
  `research/journal_sprint/closeout_transfer_grid.py`.
- Ongoing chronological/retrospective record: [PROJECT_LOG.md](PROJECT_LOG.md).

From the repository root, with matching archived dependencies, run
`venv\Scripts\python.exe -m research.journal_sprint.closeout_transfer_grid --output results/journal_sprint/week6_closeout_replay_02`.
Choose a fresh unused output directory. Same keys reconstruct the same draws;
this is not a new independent stochastic replication. Never overwrite archives.

## Still open beyond this week

Macroscope is unconnected; no PR, commit, push or submission was created.
Unrelated user modifications and earlier failed/superseded evidence remain intact.
Contributor approval/authorship, realistic transfer bounds, numerical guarantees,
modern/classical comparison fairness, novelty, and confirmation remain open.
Ten scheduled weeks remain (7–16), plus the original reserve; the main-experiment
calendar is readiness-gated and is not a journal acceptance forecast.
