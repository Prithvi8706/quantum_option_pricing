# Journal reengineering: running record

## 2026-09-14: Macroscope review remediation

User reported the completed review and requested necessary fixes. Read all 15
inline findings, including those the bot subsequently labeled no longer relevant.
Implemented safety/integrity, batch handling, record validation, smoke recovery,
independent dollar-gate and archive portability fixes in the separate PR checkout.
Preserved unrelated user edits and all immutable original experiment evidence.
See the [finding-by-finding response](MACROSCOPE_REVIEW_RESPONSE.md) for changes,
tests and limitations; [archive reconstruction](ARCHIVE_REPLAY.md) documents the
historical protocol supplement instead of rewriting the original snapshot.

Initial 52 new regression tests passed; a 53rd materialization test was then added.
Reran all 312 numerical cases with zero failures and byte-identical records to
week 9. Full suite: 390 passed, 11 upstream warnings, 142.10 seconds. Ruff and
whitespace checks passed. Fixes are pushed to PR #1 from the separate review
checkout; the main workspace's uncommitted edits remain untouched.
The prior Macroscope cost skip is superseded by the completed user-triggered
review, not by a claim of approval. No billing settings or author list changed.

## 2026-09-14: review PR opened at user request

User explicitly requested publication of the work as a PR so they can initiate
Macroscope review. Opened [PR #1](https://github.com/Prithvi8706/quantum_option_pricing/pull/1)
from `journal-reengineering-weeks-1-9` against `main`. This supersedes earlier
PR-hold status; Macroscope approval itself remains pending.

Included 19 pre-existing foundation commits and the sprint source/tests,
documents, licensed comparator extract and selected small evidence exports.
[Scope and exclusions](PR_REVIEW_SCOPE.md) explains why original manifests are
not complete replay archives in this checkout. Unrelated uncommitted Paper A
edits, local environments, downloaded papers and large archives remain local.
Sprint Ruff passed. A separate clean PR-tree full-suite check was started;
its disposition is recorded in the review-scope document and PR description.
The clean run produced 325 passes and 12 missing-fixture failures. Included the
small required baseline/configuration fixtures; all 27 tests in affected modules
then passed, including every prior failure. No tests were skipped or weakened.
Preserved original evidence bytes using Git attributes. Macroscope automatically
skipped the first review because its 39.12 USD estimate exceeded the 10 USD
per-review limit; no paid retry or billing change was initiated by the agent.
No merge, submission or authorship change was made.

## 2026-09-14: week 9 started and completed locally

User requested week 9 start to end, then resumed after network interruption.
[Plan](WEEK_9_PLAN.md), [step-by-step closeout](WEEK_9_CLOSEOUT.md),
[results](WEEK_9_RESULTS.md), [new manuscript](MANUSCRIPT_RELIABILITY_DRAFT.md).

- Reconciled weeks 5–8 into a claim/evidence audit and synchronized manuscript;
  corrected stale calibration/bound language while preserving historical drafts.
- Refreshed focused primary records, adding an explicitly abstract-only basket
  pricing overlap screen. No exhaustive-search or certified-novelty claim.
- Predeclared independent 80-digit numerical reference: 312 cases, zero missing
  components, 18 empty, 78 full, zero disconnected final reference sets. Maximum
  endpoint slack 1.1003482766924545e-13; finite diagnostic, not certification.
- Replayed all cases; checked 71 archive hashes, 67 snapshot hashes and six live
  producing dependencies. Historical week-5–8 manifest/summary checks retained
  distinct procedure and inference-arm denominators, not new pricing replays.
- Integrated suite: 337 passed, 11 warnings, 192.80 seconds. Nine new focused
  tests passed. Subsequent verifier-only provenance clarification passed replay
  and lint; not falsely included in the earlier full-suite run.
- Separate Astra-requested reviewer independently replayed 312 cases, ran nine
  tests and inspected test XML. Corrected “paired” to descriptive unpaired for
  week-8 contrasts and completed the linked results document.
- No new pricing trials, target-driven retuning or restored withdrawn claims.
  Paid selector remains negative; journal sufficiency remains unestablished.
  Macroscope/PR, submission and authorship gates remain open. No external write.
- Next: [week-10 proposal](WEEK_10_GATE_DRAFT.md), not an executed protocol.

This record captures milestone decisions, evidence and corrections, not every
terminal command. Prior week-1–8 entries remain below.

## Week 8 started

User requested start to end. [Plan](WEEK_8_PLAN.md) and
[prospective representation-pilot protocol](PROTOCOL_W8_REPRESENTATION.md)
freeze a paid, target-free pilot choice with fresh validation versus both fixed
representations. Bound-only menu audit completed before new draws; all outcomes
and costs will be logged, including negative selection results.

## 2026-09-13: week 8 complete locally

All five [planned items](WEEK_8_PLAN.md) completed. See the
[step-by-step closeout](WEEK_8_CLOSEOUT.md), [results](WEEK_8_RESULTS.md), and
[selection scope](WEEK_8_SELECTION_SCOPE.md).

- Audited n5/n6 bounds and existing compiled profiles before new draws. Fixed
  both baselines and an observable pilot-radius ranking heuristic; target-field
  injection is rejected at the selector interface. No representation/guard
  retuning after observing outcomes.
- Executed 5400 procedures: 3300 final acquisitions, 2100 pre-refusals, plus
  1800 paid pilot acquisitions. Persisted pilot observations, choice and fixed
  final schedule before generating fresh calibration/validation observations.
- Reconstructed all 5400 events/records and 54 summaries; checked 81 archive
  hashes and 74 planned dependencies. Preserved all pilot/final costs and
  36 selector-minus-fixed contrasts.
- Observed 900 declarations (all E001), 2400 unresolved final intervals, no
  incompatibilities, 3300/3300 price containment and zero erroneous declarations.
  These are frequencies, not zero risk or coverage conditional on delivery.
- Paid choices: 350 n5 / 550 n6; another 300 n6 bypasses for E049. All delivery
  contrasts were zero; only 3/12 cells met the >=90% threshold and both mean
  gains were zero. Selector fails and is retained as a negative ablation.
- Full regression: **325 passed**, 11 legacy warnings, 328.17 s. Separate
  Astra-requested source/data/claim review passed, identifying two minor issues.
  Clarified claim wording and added after-cell resource checks including the
  last cell. **14 focused tests** passed afterward, including three new boundary
  cases; no post-fix full-suite rerun claimed. Ruff and links checked.
- Preserved v1 and executed corrected-source v2 plus full replay. Records,
  selection events, menu and targets match byte-for-byte; outcomes unchanged.
  V2 is same-key replay, not another independent experiment to pool with v1.
  Reviewer accepted both fixes in final mechanical recheck.
- Decision: no adaptive promotion/main confirmation. Narrow candidate scope to
  model-conditional interval coverage and empirical precision delivery with
  explicit costs; novelty remains unestablished. [Week 9 gate](WEEK_9_GATE_DRAFT.md)
  is future claim/evidence work, not a completed experiment.

Archives under `results/journal_sprint`: `week8_representation_v1`,
`week8_closeout_v1`, `week8_representation_v2`, `week8_closeout_v2`.
Tests: `tests_week8_integrated_v1.xml`, `tests_week8_review_fix.xml`.
No original evidence overwritten, unrelated user work changed, author additions,
commit/push/PR, paid hardware or submission. Macroscope remains unconnected.
Eight scheduled weeks (9–16) plus reserve remain readiness-gated, not acceptance.

## Week 7 started

User requested start-to-end completion. [Week-7 plan](WEEK_7_PLAN.md) and
[prospective ablation](PROTOCOL_W7_ABLATION.md) separate pricing shots,
calibration shots and guard width at fixed actual transfer. Pinned comparator
semantics will be audited in parallel with local implementation. No main matrix
or adaptive claim is assumed. Completion and evidence will be appended here.

## 2026-09-13: week 7 complete locally

All five [planned items](WEEK_7_PLAN.md) completed start to end. The
[step-by-step closeout](WEEK_7_CLOSEOUT.md), [results](WEEK_7_RESULTS.md), and
[native-comparator audit](WEEK_7_COMPARATOR_SCOPE.md) record the evidence.

- Prospectively separated pricing budget, calibration budget and valid guard
  width while holding actual transfer fixed for paired guard comparisons.
- Executed 21600 acquisition attempts: 14400 acquired, 7200 refused. Shared
  guard arms produced 43200 arm attempts / 28800 executed inferences. Costs
  charged once per acquisition, not once per arm; represented shots 5089003200.
- Replayed every record and all 216 summaries; 77 archive and 71 planned
  dependency hashes checked, 19200 guard-enclosure comparisons passed.
- Archived 1008 descriptive contrasts and all four predeclared readiness
  screens. All failed: 1/12,1/12,3/12,3/12 cells passed, respectively. E001
  improves with more pricing shots; broad four-contract usefulness is not shown.
- Preserved 5042 arm declarations, 23758 unresolved outcomes and nine interval
  misses. Three misses were precise E001 intervals but midpoint errors remained
  <=$1; zero erroneous $1 declarations observed. No risk/coverage overclaim.
- Pinned BAE/BIQAE source audit confirms that their current native adapters do
  not supply the finite-calibrated asymmetric-readout/transfer guarantee. No
  mismatched native head-to-head win or modified baseline was invented.
- Ten new targeted tests passed before run; full regression **314 passed**,
  11 legacy warnings, 190.03 s. Ruff and local Markdown links checked.
- Separate Astra-requested final numerical/claim review passed. Closeout link
  completed. Mathematical/numerical certification remains separate.
  Reviewer executed full existing replay into `week7_sidecar_review_v1`, with
  separate aggregation; parent verified its three result JSON files match.
  Reviewer inspected test XML rather than personally rerunning pytest.
- Decision: no adaptive promotion or confirmatory main matrix. The
  [week-8 gate draft](WEEK_8_GATE_DRAFT.md) is a future design task, not an
  executed experiment. Nine scheduled weeks (8–16) plus reserve remain gated.

Evidence: `results/journal_sprint/week7_ablation_v1`,
`results/journal_sprint/week7_closeout_v1`,
`results/journal_sprint/tests_week7_integrated_v1.xml`. No archives overwritten,
unrelated user edits changed, author additions, commits, pushes or submissions.
Macroscope remains unconnected and the PR is held.

This is the central index and ongoing milestone log, not a verbatim transcript
of every command. Protocols, result notes, code, test outputs and hashed run
archives hold the detailed evidence. Negative results and unresolved gates
must remain visible; completion of a week does not mean publication readiness.

## Work completed before week 6

- [Weeks 1–2](WEEK_1_2_CLOSEOUT.md): evidence audit, pricing bounds and prototypes.
- [Week 3](WEEK_3_PROGRESS.md): circuit/stress/classical checks;
  [review and PR gate](WEEK_3_PR_GATE.md).
- [Week 4](WEEK_4_CLOSEOUT.md): finite calibration and guarded transfer discovery.
- [Week 5](WEEK_5_CLOSEOUT.md): compiled fixed-design cost comparison,
  7200 attempts, reconstruction and bounded automated review.

## 2026-09-13: week 6 started

User requested a clear ongoing Markdown record and week-6 execution.
The [week-6 protocol](PROTOCOL_W6_TRANSFER_GRID.md) develops the prior
[pilot draft](WEEK_6_PILOT_DRAFT.md). Retain all six contracts, nine stipulated
transfer positions, two calibration budgets and three fixed designs.
No adaptive tuning, held-out confirmation or real-device claims are authorized
by these discovery results. Status and evidence: [week-6 progress](WEEK_6_PROGRESS.md).

First execution completed: 32400 attempts in 29.43 seconds; 16 targeted tests
passed before acquisition. Raw archive: `results/journal_sprint/week6_transfer_grid_v1`.
This initial status is superseded by the completed closeout below.

Macroscope remains unconnected; PR, author approvals and submission remain held.

## 2026-09-13: week 6 completed locally

User requested completion without stopping at milestones. Continued through
reconstruction, predefined analysis, regression, bounded separate review and
next-stage decision. [Full step-by-step closeout](WEEK_6_CLOSEOUT.md) and
[results](WEEK_6_RESULTS.md) are the current state.

- Reconstructed all 32400 attempts / 324 cells, including 21600 acquisitions
  and 10800 refusals; checked 71 archive hashes and 66 planned dependency hashes.
- Recorded 2729 precision declarations and 18871 unresolved acquisitions.
  Three price-containment misses were unresolved; zero erroneous declarations
  observed. These outcomes do not imply zero risk or conditional coverage.
- Published all 162 calibration contrasts, 216 design contrasts and 36 range
  summaries. E001 CX-capped delivery ranged 0–99% at low calibration and 2–99%
  at high; rare E014/E025 declarations retained rather than suppressed.
- Full regression: 304 passed, 11 legacy warnings, 189.06 seconds. Ruff passes.
- Astra-requested review resumed after usage-limit interruption; no blocking
  scientific-reporting issue. Corrected per-contract depth wording and recorded
  the fail-closed live-source replay limitation; no mathematical proof claimed.
  Reviewer replayed all records using existing helpers with writes intercepted,
  separately calculated contrast checks, and ran 12 overlapping targeted tests.
- Scientific decision: no adaptive promotion or confirmatory main matrix.
  [Week-7 gate draft](WEEK_7_GATE_DRAFT.md) calls for separately declared
  ablation and fair-comparator work. No unexecuted future experiment is counted
  as completed. Ten scheduled weeks (7–16) remain, subject to readiness gates.

Archives: `results/journal_sprint/week6_transfer_grid_v1`,
`results/journal_sprint/week6_closeout_v1`; integrated test XML:
`results/journal_sprint/tests_week6_integrated_v1.xml`. Original archives and
unrelated user edits preserved. No PR/push/submission/author-list changes.

## Retrospective week-by-week log: weeks 1–5

Added 2026-09-13 from the linked existing evidence. Weeks 1–2 were closed out
jointly: the thematic split below is for navigation, not a claim that exact
work dates or a separate week-1/week-2 sign-off were recorded. Test counts from
overlapping suites are not added together. Failed and superseded artifacts
remain preserved; these summaries do not replace their provenance.

### Week 1 — evidence audit and research direction (joint sprint)

- Work: preserved historical manuscripts/data; distinguished encoded-reference
  deviation from continuous Black–Scholes error; removed unsupported floor
  claims from the replacement narrative. Excluded both disputed Paper B slope
  sets for lack of adequate producing-run evidence.
- Research: six assigned primary papers read in full; two additional 2026
  papers only abstract-screened. Separated established estimation tools from
  the proposed application contribution. Proposed small genuine collaborator
  packages without claiming acceptance, completed work or authorship.
- Outputs: [reading ledger](READING_LEDGER.md),
  [literature supplement](LITERATURE_SUPPLEMENT.md),
  [claim ledger](CLAIM_LEDGER.md),
  [Paper B disposition](PAPER_B_EVIDENCE_DISPOSITION.md),
  [working manuscript](MANUSCRIPT_WORKING_DRAFT.md),
  [team packages](TEAM_WORK_PACKAGES.md).
- Decision: pursue contract-aware delivered precision with auditable bounds
  and costs, not an unsupported generic new estimator or hardware advantage.
- Open: genuine contributor agreement, availability/budgets, and the later
  scientific/publication gates. Historical evidence was not fabricated.

### Week 2 — feasibility and dollar-precision prototypes (joint sprint)

- Work: pinned comparator with golden checks; conservative all-branch
  inversion, independent pilot/validation streams, mismatch/refusal outcomes.
  Generic prototype retained 26600 records; comparator work retained 160000
  estimations over 140000 distinct generated datasets.
- Application: examined 72 bound configurations; tighter grid bound increased
  positive $1 statistical allowances from 4 to 14, across four of six contracts.
  V2C recorded 43200 attempts: 36000 executed, 7200 pre-refused.
- Findings: largest-budget ideal fixed multidepth delivered in 51.08% of all
  attempts versus 33.33% for equal-A direct sampling. Not a best-classical or
  modern-estimator advantage. Bound-only selection mainly saved refusal costs,
  not demonstrated adaptive scheduling benefit.
- Checks: full suite 225 passed before three additional closeout tests;
  updated sprint suite 64 passed. All 43200 V2C records reconstructed.
- Evidence: [joint closeout](WEEK_1_2_CLOSEOUT.md),
  [V2C results](PRICE_INTERVALS_V2C_RESULTS.md),
  [next-stage amendment](PROSPECTIVE_AMENDMENT_DRAFT.md);
  archive `results/journal_sprint/week12_closeout_v1`.
- Decision: feasibility foundation complete, administrative sign-off pending;
  proceed to circuit checks and stronger baselines, not submission.

### Week 3 — circuit, noise, classical and reproducibility checks

- Work: actual-circuit/noise checks, readout/dependence stress, 480-row
  classical European/Asian matrix, pinned BAE/BIQAE source smokes, 20 larger
  logical profiles, and a fresh-environment circuit replay.
- Findings: response-model failures and matched-cost/conditional-risk questions
  prevented confirmation. No adaptive superiority or practical advantage.
- Checks: final integrated 253 passed; fresh-environment sprint 89 passed
  (overlapping scopes). Bounded automated review requested with `gpt-6-astra`;
  findings addressed and corrected artifacts checked, not human peer review.
- Evidence: [progress](WEEK_3_PROGRESS.md),
  [stress results](WEEK_3_STRESS_RESULTS.md),
  [baselines and review](WEEK_3_BASELINES_AND_REVIEW.md),
  [PR gate](WEEK_3_PR_GATE.md).
- Decision: hold confirmation. Macroscope unavailable/unconnected, PR held.
  Existing branch history and unrelated user edits prevent treating a broad
  staged tree as an isolated weekly PR; no bulk staging of result caches.

### Week 4 — finite calibration and transfer validity

- Work: 1200 calibration datasets / 3600 analyses; transfer/dollar experiment
  with 6000 attempts, 4000 acquisitions, 2000 pre-refusals and 8000 inferences.
  Charged calibration and distinguished wrong declarations from noncontainment.
- Findings: guarded intervals contained targets in all tested within-bound
  cells, but useful $1 delivery was largely E001. Exceeding supplied bounds
  could produce narrow wrong intervals; precision cannot validate assumptions.
- Checks: 271 integrated tests passed; 107 sprint tests overlap. Reconstructed
  all 6000 trial identities and 8000 inferences; 61 transfer hashes checked.
  Separate calibration checks covered 46 hashes and 1200 observations.
  Bounded Astra-requested review led to heading/reference corrections.
- Evidence: [closeout](WEEK_4_CLOSEOUT.md),
  [calibration progress](WEEK_4_PROGRESS.md),
  [transfer results](WEEK_4_TRANSFER_RESULTS.md),
  [validation contract draft](WEEK_5_6_VALIDATION_CONTRACT_DRAFT.md);
  archive `results/journal_sprint/week4_transfer_verify_v2`.
- Decision: local discovery milestones complete; develop fixed cost baselines
  before adaptive control. Real transfer justification, numerical certification,
  fair comparisons, confirmation and Macroscope/PR remain open.

### Week 5 — fixed-design pricing costs and delivery

- Work: ten missing k=2 profiles, 30 combined profiles and 40 fixed-cost
  comparisons. Recorded 7200 attempts: 4800 acquisitions, 2400 refusals,
  516 precision declarations and 4284 unresolved acquisitions.
- Findings: only E001 delivered $1 precision. Larger-budget CX-capped delivery
  was 6/100 stationary and 95/100 transfer versus direct's zero. Equal-A
  multidepth used about 15.6 times direct's pricing CX count. Neither result
  establishes broad advantage, continuous-region robustness or zero error risk.
- Checks: 287 integrated tests passed before verifier-only strengthening;
  11 targeted tests passed afterward, including five configuration mutations.
  v2 replay validated exact configuration and live/archive Python identity.
  Separate Astra-requested source/hash review accepted fixes; not independent
  numerical proof. Qualified local predeclaration versus timestamped registration.
- Evidence: [plan](WEEK_5_PLAN.md), [results](WEEK_5_FIXED_RESULTS.md),
  [closeout](WEEK_5_CLOSEOUT.md); archives
  `results/journal_sprint/week5_fixed_discovery_v1` and
  `results/journal_sprint/week5_fixed_verify_v2`.
- Decision: local week complete; choose transfer-position/calibration-size
  discovery for week 6. Keep adaptive promotion, confirmation and PR held.
