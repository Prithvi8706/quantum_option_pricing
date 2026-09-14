# Week 8 closeout

13 September 2026. **All five planned local week-8 work items are complete**:
experiment, reconstruction, analysis, regression, bounded review, fixes and final
recheck. External Macroscope/PR and confirmation gates remain open.

## Step-by-step record

1. Audited the existing two-representation bound and compiled-cost menu without
   exact targets. Declared the [week-8 plan](WEEK_8_PLAN.md) and
   [protocol](PROTOCOL_W8_REPRESENTATION.md), keeping all C6 and fixed guard=.03.
   Both representations are eligible for E001/E014/E025, only n6 for E049,
   neither for E030/E038. No larger circuit or unprofiled cost was invented.
2. Implemented a strict observable-score selector and both fixed baselines.
   Two candidate pilots consume pricing-CX allowance before final allocation;
   a sole candidate bypasses pilots. Every selection event durably contains
   pilot observations and the chosen schedule before fresh final counts.
   Eleven targeted tests passed before execution, including oracle-field
   rejection, cost/bypass checks and event-before-final ordering.
3. Completed 5400 procedure attempts in 19.06 seconds: 3300 final acquisitions,
   2100 pre-refusals and an additional 1800 pilot candidate acquisitions.
   Bound/menu setup took .13381 seconds. Pilot and final cost totals are separate.
4. Reconstructed all 5400 events and records and all 54 summaries. Verified
   81 archive hashes and 74 planned dependency hashes, recalculated the menu,
   targets, pilots, choices, final schedules, intervals and phase costs.
   Replayed data reuse producing helpers; matching hashes are not independent
   mathematical proof or an external chronological-registration certificate.
5. Archived all 36 baseline contrasts and the readiness screen, and wrote
   [results](WEEK_8_RESULTS.md) and [selection-scope argument](WEEK_8_SELECTION_SCOPE.md).
   All delivery contrasts were zero; only three of 12 feasible-contract/condition
   cells met >=90% delivery. Mean gains against both baselines were zero.
6. Decision: **do not promote the selector or launch main confirmation**. Retain
   it as a negative, fully costed ablation. [Week 9](WEEK_9_GATE_DRAFT.md) is a
   future claim/evidence design gate, not an already executed experiment.

## Outcomes and limits

900 final precision declarations, all E001; 2400 unresolved; zero incompatibilities.
All 3300 final intervals contained price, with zero observed erroneous declarations.
This does not imply zero risk, simultaneous coverage, real-device validity or 95%
correctness conditional on delivery. All final confidence sets were connected;
disconnected-branch gaps did not cause broad hulls in these observed final sets.

Of 900 paid choices, n5 was chosen 350 times and n6 550 times; E049 bypassed
pilots to n6 in another 300 procedures. Actual adaptive choice is not evidence
of useful adaptation. Additional pilot calibration cost produced no delivery gain.

Total represented shots: 284589600 (20275200 pilot phase, 264314400 final phase).
Pricing CX total: 1089951639000, individually capped at 330301440 per procedure.
This is equal pricing-CX allowance, not equal total shots/calibration/runtime.
There is no native BAE/BIQAE or classical-pricing advantage claim.

## Checks and review

Full repository regression passed **325 tests**, 11 legacy dependency warnings,
328.17 seconds. This includes the 11 new targeted tests that passed before run.
Ruff and tracked whitespace checks pass. The full suite was not rerun after the
limit-only fix below: **14 focused tests** then passed, including three new
limit/boundary cases. These counts overlap and must not be added as unique tests.

Separate bounded review requested with `gpt-6-astra` passed with no substantive
code/data/claim correction. The reviewer personally checked 81 raw-run hashes,
five closeout hashes, 74 live/snapshot dependencies, configuration/menu, 5400
event/record correspondences, and independently aggregated phase costs, outcomes,
rankings, choices, median radii, component counts, contrasts and the failed screen.
It inspected source/test code and the conditional-on-pilot-history argument;
it did not personally run pytest, Ruff or the full numerical replay in that audit.

Two minor findings were addressed: ambiguous wording became "model-conditional
interval coverage and empirical precision delivery"; resource limits are now
checked after every cell, including the final cell, as well as before cells.
The original run was within limits and preserved. A versioned same-key v2 run
and full replay passed; records, events, menu and target files match v1 byte-for-
byte. V2 is a corrected-source replay of the same data, not fresh independent
evidence. No statistical/inference/selection algorithm changed. The resource
checks detect excess at cell boundaries, not by preemptively interrupting a batch.

The scope is bounded automated review, not a human referee or independent
mathematical certificate. Macroscope remains unconnected and the PR stays held.
The final mechanical recheck passed: the reviewer confirmed before/after-cell
limit checks, corrected wording and accurate pre/post-fix test scope. No new
tests or numerical replay were claimed for that recheck. Its unsupported initial
model-unavailability assertion was retracted; attribution remains review requested
with `gpt-6-astra`, not a claim based on the reviewer's self-identification.

## Evidence and reproduction

- Raw data and durable events: `results/journal_sprint/week8_representation_v1`.
- Reconstruction, 36 contrasts, screen and misses: `results/journal_sprint/week8_closeout_v1`.
- Corrected-source repeat/replay: `week8_representation_v2` / `week8_closeout_v2`
  under `results/journal_sprint`, with unchanged scientific records.
- Integrated test output: `results/journal_sprint/tests_week8_integrated_v1.xml`.
- Source: `research/journal_sprint/run_representation_pilot.py` and
  `research/journal_sprint/closeout_representation_pilot.py`.
- Ongoing record: [PROJECT_LOG.md](PROJECT_LOG.md).

With matching archived source/dependencies, from repository root:
`venv\Scripts\python.exe -m research.journal_sprint.closeout_representation_pilot --source results/journal_sprint/week8_representation_v2 --output results/journal_sprint/week8_closeout_replay_03`.
Choose a fresh unused directory. The same keys replay the same draws, not an
independent stochastic replication. Live-source drift is rejected; old archives
must be replayed with compatible archived code rather than silently edited.

No commit, push, PR, submission, paid hardware or author-list change was made.
Original archives and unrelated user edits remain intact. Eight scheduled weeks
(9–16), plus reserve, remain readiness-gated, not an acceptance forecast. Main
confirmation, numerical certification, real transfer justification, novelty and
actual contributor work/approval remain open beyond this local week.
