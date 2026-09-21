# Promotion plan for main

Date: 2026-09-21. **Plan only: no promotion is performed in this task.**
The stable remote base is `da3080d19a8f746cab31bbee157a5d591c6b56fb`.
Local main is intentionally unchanged at `103ddfd1`; synchronize it to the
remote stable base only when a future main-integration task is authorized.
All proposed existing snapshots are ancestors of dev and retain the original
source/acquisition commits. Readiness here concerns scoped integration, not
submission, human novelty approval, hardware delivery or confirmation.

## Batches from the actual ancestry

| Batch / snapshot | Exact scope and dependencies | Validation and scientific claim | Current readiness / blocker |
| --- | --- | --- | --- |
| 1. Stronger arithmetic source; through `23f8d948` | Original commits `9511bc0c`, `23f8d948` above PR #8. `research/stronger_arithmetic/`, eleven `tests/test_stronger_arithmetic_*.py` files, directed-certificate/primary/signed methods and acquisition protocols, scoped attributes. No new results archive in this snapshot. | Prior independent source reviews; 315 overlapping pinned tests and the later 1,645-case integrated receipt cover this unchanged source. Arithmetic, cleanup, signed floors, overflow and logical planner claims only. Evidence receipts are review attachments from dev until batch 2. Frozen decoder accepts binary64 probabilities; do not present it as a complete exact-label adapter. | **Ready for a scoped integration review.** Requires the normal merge review/checks on the proposed snapshot, not a new research acquisition. The separate label adapter belongs to batch 3; disclose its interface condition now. |
| 2. Frozen study and closeout; through `49b8f0a5` | `60e735e1`, `add768dc`, `49b8f0a5`, after batch 1. Primary 148-row and residual 18-row archives, combined analysis/CSV, pinned/full test and replay receipts, release review/results, updated README/checklist/log. | Source and input binding, all certificates/finite diagnostics, both ledgers, selected complete gate reconstruction; current independent rational/resource checks corroborate them. D1/D2 local ordering and width tradeoff only. | **Ready for evidence integration review.** Attach the current assessment as review context so historical closeout is not read as novelty or executable-label clearance. No additional all-menu gate re-emission or full-suite rerun is justified unless new failures arise. |
| 3. Preservation and reviewed numerical interface; through `601ebcdc` | Chronological commits `5f96b9ec`, `b90c2e30`, `601ebcdc`, after batch 2. New opt-in `research/assessment_20260921/`, tests/protocol/receipts; previously untracked historical artifacts and manifest; narrow ignore/attribute rules and archival manuscript notice. | 384 exact-label possibilities, all 18 schedules unchanged, 19 passing targeted tests (15 new plus four existing decoder tests), Ruff, independent math review. Every one of the 13,783 preserved original artifacts matches its recorded SHA-256. Preservation is not new scientific validation. | **Ready for artifact/interface review as one snapshot.** Do not promote v1 alone as the final minimality verification. Review artifact size, provenance and the historical-draft notice; retain source hashes and the original v1 record. |
| 4. Scientific assessment and consolidation record | The completed assessment commit and its delivery receipt on dev, after batch 3. `docs/novelty_assessment/2026-09-21/`, root README/checklist/log pointers. Exact payload commit is recorded by the delivery receipt rather than guessed in advance. | Twenty-five substantive primary sources, eight closest-source formula comparisons, A–H claim assessment, sixteen objections, three independent AI scopes plus a separate narrative pass, link/hash/claim consistency checks. No new pricing acquisition. | **Ready for documentation/scientific-framing review after recorded delivery checks.** Conditional go for the narrow case-study draft. Common-policy compilation and human significance assessment remain open, not blockers to documenting their absence. |
| 5. Bounded common-policy comparison | A future separately committed protocol/producer and exclusive archive under the [follow-up plan](BOUNDED_FOLLOWUP_PLAN.md), after batch 4. Selected D1/D2 reflection/raw-parent/residual only; no financial pivot. | Same decomposition/optimization rules, controlled/uncompute work, width/depth, both ledgers, bounded compute and independent review. Outcome may narrow or reverse the current implementation ranking. | **Not ready: not executed.** No imaginary commit or successful result assigned. |
| 6. Manuscript and publication package | Future integrated manuscript, generated tables/figures, dependency/data/license review, author contributions and disclosures, current venue policy/fee review after choosing a venue. | Human scientific judgment and actual author approval; claims limited by all preceding evidence. Submission requires separate authorization. | **Not ready.** No completed manuscript, human approval, submission or publication is claimed. |

The source/acquisition boundaries are dictated by existing commits. In
particular, the adapter's first commit precedes artifact preservation and its
reviewed fix follows it. Rearranging or squashing those commits just to fit a
tidier conceptual grouping would damage provenance. Batch 3 therefore uses
the complete reviewed snapshot instead of an artificial reordered history.

## Practical workflow with two permanent branches

For each authorized batch, review the diff from the then-current main to its
exact snapshot, verify ancestry/source bindings, and use an ordinary merge
that preserves the original commits. A fast-forward is suitable when main
is an ancestor; a merge commit is suitable when integration commits create
divergence. Never reset or force-push main/dev. Avoid cherry-picking, rebasing
or squash-merging provenance-critical producer/acquisition commits.

A temporary PR head such as `promote/arithmetic-source` can point to the
exact batch snapshot, target main and be deleted locally/remotely immediately
after merge. It is a temporary review vehicle, not a third permanent branch.
If even temporary branch names are undesirable, an authorized maintainer can
review the exact snapshot externally and perform an ordinary local merge and
non-force push; this must comply with protections in force at that time.
A PR from the full dev head would include all later work and therefore is
unsuitable for promoting only the first snapshot.

After each main merge, reconcile main back into dev by an ordinary merge when
needed so future batches share the integration ancestry. Check current PRs
and protections again at integration time. Delete temporary heads only after
their tips are reachable from main/dev. Existing evidence freezes remain at
their original hashes regardless of later integration commits.

The first concrete review can begin at `23f8d948`. Its reviewed scope is
implementation/certificates and tests; it does not require deciding whether
the proposed paper will be accepted. The original research evidence and the
new candid assessment remain fully available on dev during that review.
