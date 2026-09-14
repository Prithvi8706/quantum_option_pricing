# Week 7 closeout

13 September 2026. **All five planned local week-7 work items are complete**:
experiment, reconstruction, comparator-scope audit, analysis, regression,
bounded separate review and logged closeout. No confirmation or PR.

## Work completed in order

1. Wrote the [week-7 plan](WEEK_7_PLAN.md) and prospective
   [ablation protocol](PROTOCOL_W7_ABLATION.md). Fixed two pricing budgets, two
   calibration sizes, three actual transfer conditions, three designs, all C6
   and 100 repetitions. Declared only valid guard arms, shared-arm accounting,
   contrasts and a four-contract readiness screen before acquiring observations.
2. Implemented new runner/replay modules without modifying prior producing
   sources. Tested complete matrix, refusals, one-charge shared arms, guard
   nesting, configuration mutations, contrast counts and readiness logic.
   Ten new targeted tests passed before execution.
3. Executed 21600 acquisition attempts: 14400 acquired and 7200 pre-refused.
   Valid guard reuse produced 43200 arm attempts, 28800 executed inferences,
   14400 refused arms. Acquisition cost was charged once. Run took 34.48 s;
   measured bound/design setup was .04466 s.
4. Reconstructed every record and 216 summaries; checked 77 archive and 71
   planned dependency hashes and all 19200 guard-component enclosure comparisons.
   Saved all 1008 descriptive contrasts, four readiness outcomes and all nine
   containment misses. Replay uses producing numerical helpers, not independent
   mathematical or floating-point proof; live-source drift fails closed.
5. Completed [pinned native comparator audit](WEEK_7_COMPARATOR_SCOPE.md).
   Existing BAE/BIQAE adapters are not equivalent native baselines for the
   finite-calibrated asymmetric-readout/transfer claim. No fabricated native
   coverage guarantee, modified algorithm or head-to-head victory was added.
6. Full repository regression: **314 passed**, 11 legacy warnings, 190.03 s.
   Ruff and tracked whitespace checks pass. Tests overlap the targeted suite;
   do not add the counts. Final independent review disposition follows below.
7. Recorded [all results](WEEK_7_RESULTS.md) and the **no-go** decision: none
   of four candidates met the full predeclared screen. Wrote a
   [week-8 entry-gate draft](WEEK_8_GATE_DRAFT.md), not an executed experiment.

## Scientific result

5042 arm-level declarations, 23758 unresolved inferences, no incompatibilities.
Price containment was 28791/28800 executed arms. Three of nine misses were
precise E001 intervals whose midpoint error still lay within the requested $1;
the other six were unresolved. Zero erroneous $1 declarations were observed,
not zero interval error or a conditional coverage guarantee.

Fourfold pricing budget improved broad-guard E001 CX-capped delivery to
96–100/100 across the three conditions, but the full four-contract screen
failed. E001 accounts for 5034 arm declarations, E025 eight, E014/E049 zero.
Changing a valid guard on the same stationary data can strongly change delivery;
that does not justify shrinking an unverified real-device drift allowance.

## Review disposition

A separate reviewer was requested with `gpt-6-astra`, continuing the user's
explicit review request. Its pinned-source comparator audit checked checkout
HEADs and inspected file hashes, interval/stopping models, randomness and costs.
Final bounded numerical/claim review passed with no substantive corrections.
Both report tables, contract/cost totals, nesting and screen outcomes matched
the evidence. The three precise E001 containment misses had midpoint errors
approximately $.473, $.237 and $.461, consistent with zero erroneous $1 claims.
The reviewer checked the regression XML (314 tests; no failures/errors/skips).
Its initially missing closeout-link finding is resolved by this file; local
Markdown links were checked. Review does not constitute mathematical proof.
The reviewer personally executed the existing full replay into
`results/journal_sprint/week7_sidecar_review_v1`, including all records and
nesting checks. Separate read-only aggregation checked arm/acquisition costs,
valid guards, contrasts and screens. Its verification, analysis and containment-
miss JSON match the parent outputs exactly; the parent also checked those file
hashes. The reviewer did not run pytest, but inspected the integrated XML.
The numerical replay still reuses producing helpers; separate aggregation does
not turn that into independent numerical certification. No source fix was needed.
Macroscope remains unconnected; the external dual-provider gate and PR are held.

## Reproduction and evidence

- Raw run: `results/journal_sprint/week7_ablation_v1`.
- Replay, contrasts, readiness, misses: `results/journal_sprint/week7_closeout_v1`.
- Tests: `results/journal_sprint/tests_week7_integrated_v1.xml`.
- Source: `research/journal_sprint/run_ablation.py` and `closeout_ablation.py`.
- Running record: [PROJECT_LOG.md](PROJECT_LOG.md).

With matching archived source/dependencies, from the repository root:
`venv\Scripts\python.exe -m research.journal_sprint.closeout_ablation --output results/journal_sprint/week7_closeout_replay_02`.
Use a fresh unused directory. Same seed keys reproduce the same observations;
this is not a new independent stochastic replication. No archives were overwritten.

No commit, push, PR, hardware job, paid service, submission or author-list change
was made. Unrelated user changes and prior evidence remain preserved. Numerical
certification, realistic transfer assumptions, matched comparators, novelty,
confirmation and human contributor/author approvals remain separate open gates.
Nine scheduled weeks (8–16), plus reserve, remain readiness-gated; not an
acceptance forecast or a promise that the current candidate merits a journal.
