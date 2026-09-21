# Branch consolidation and preservation

Date: 2026-09-21. **Completed: local and remote development branches are now
exactly `main` and `dev`.** Main was not advanced, rewritten or force-pushed.
The [machine-readable cleanup receipt](provenance/branch_cleanup.json) records
the actual operation output, before/after references and worktree preservation checks.

## Verified starting state

Fetch confirmed remote main at `da3080d19a8f746cab31bbee157a5d591c6b56fb`
(PR #8). Local main was already 26 commits behind at
`103ddfd1391e3e9800a0cf73b552be10fe3aa01f`. Both remain at those exact commits.
Keeping main unchanged means the stale local pointer was not silently updated.
Future integration must start from the current remote stable state, not from
the stale local pointer.

The five reported research commits were present, unpublished, and consecutive
above remote main. No dev branch existed. Dev was created at `49b8f0a5`, then
pushed and verified there before subsequent assessment/preservation commits.
All original branch tips were ancestors of this development state. No branch
had unique commits requiring a merge or a conflicting experiment disposition.
No history was rebased, squashed, cherry-picked or discarded.

GitHub's default branch is main. Open PR inventory was empty both initially
and immediately before deletion. The main protection endpoint reported 404,
"Branch not protected"; the repository ruleset list was empty. Cleanup did
not encounter or bypass a protection. No PR depended on a removed branch.

## Preserved branch inventory

Full object IDs and initial reachability checks are in
[initial_refs.json](provenance/initial_refs.json). The abbreviated inventory
below is for reading; all useful work remains reachable through dev.

| Former branch | Local tip | Remote tip if present | Disposition |
| --- | --- | --- | --- |
| journal-reengineering-weeks-1-9 | `8009d41e` | `3ba9925b` | Both ancestors retained; redundant names deleted |
| maintenance/release-readiness-20260920 | `6b978949` | same | Retained in main/dev ancestry; names deleted |
| paper-a-foundation-e0 | `0bc163ca` | absent | Ancestor retained; local name deleted |
| research/claim-assessment-20260917 | `62324151` | same | Ancestor retained; names deleted |
| research/confirmation-gate-bounds | `df355120` | same | Ancestor retained; names deleted |
| research/stronger-arithmetic-20260921 | `49b8f0a5` | absent | Five original commits retained with authorship in dev; local name deleted |
| research/week10-evidence-gate | `ba59c35e` | same | Ancestor retained; names deleted |
| research/week12-unequal-calibration | `c0055ff2` | same | Ancestor retained; names deleted |
| research/week13-quantum-encoding | `42537ff0` | absent | Ancestor retained; local name deleted |
| research/week14-comparisons | `4ffe5732` | same | Ancestor retained; names deleted |
| research/week15-reproduction | `efa08acc` | same | Ancestor retained; names deleted |
| review/macroscope-fixes | `3ba9925b` | absent | Review worktree detached at same commit; local branch name deleted |

Before cleanup, dev was pushed again through preservation commit
`b90c2e30a3e59a96d641619808eae99e668a9a48` and verified with `ls-remote`.
Every deletion candidate was rechecked as an ancestor of that **pushed** SHA.
Eight redundant remote branches were deleted by ordinary push deletions;
twelve redundant local branches were deleted with `git branch -d`. No force
deletion was needed. The receipt confirms only the two requested heads remain.

## Work outside branch heads

The linked review worktree at `C:/Users/prith/quantum_option_pricing_pr_review`
had one modified tracked Python bytecode file. Detaching at the same commit
preserved its HEAD, status and SHA-256 exactly. No worktree or file was removed.
Other historical validation worktrees were already detached and were retained.
Detached worktrees are not additional development branches.

The existing stash `d20fdc626c8bf823505281402f1004071f9ed38f` is retained.
Its six source edits had already received explicit reconciliation in
`3ba9925b`, documented in
[MERGE_VERIFICATION.md](../../journal_sprint/MERGE_VERIFICATION.md).
Reapplying the stash would reintroduce superseded decisions; preservation
does not mean silently replacing the current source with those old edits.

The pre-existing archival reference `refs/original/refs/heads/main` at
`145dafc40a1c2ad1909d7adcb473cc750b87c314` is retained locally. Its two old
digital-pricing commits have corresponding active-history work at `91b51fdf`
and `d9261ca9`; `src/digital_option.py` and `src/black_scholes.py` match the
archived versions byte-for-byte, and current tests add coverage. The old
commit identities remain recoverable without pretending they were merged.
Stash, archival and tooling references are not `refs/heads` development branches.

A complete pre-cleanup Git bundle was created and verified at
`.context/assessment-20260921/pre-consolidation.bundle`. It includes the old
branch tips, stash, archival reference and detached worktree heads. This is a
**local recovery artifact**, not a file pushed to GitHub; it also contains
local tooling references. Published branch tips are independently recoverable
as dev ancestors using the committed inventory. `git show <full-tip>` or a
detached worktree can inspect them without restoring permanent branch names.

## Legitimate previously untracked project information

The initial active checkout had no tracked edits. Untracked material was
classified explicitly before staging. Commit `b90c2e30` preserves 13,783
historical project files (254,488,741 original bytes): earlier research
archives, source snapshots, QPY circuits, failed/excluded runs, receipts,
project-authored Paper A outputs and the June arithmetic/RQMC plan.
It adds an archival-status notice to the old manuscript outputs; their old
readiness/novelty language is not endorsed by the new assessment.

The [inventory](provenance/preservation_inventory.json),
[per-file SHA-256 manifest](provenance/consolidated_files.jsonl),
[verifier](provenance/verify_preservation.py) and
[byte-preservation receipt](provenance/preservation_verification.json)
record classification and verify every selected Git blob against its original
bytes. This establishes preservation, not scientific revalidation of every
historical experiment. A limited high-confidence secret-pattern scan found
no suspect paths; it was not a comprehensive secrets audit.

18,450 environment/external-checkout entries, 24 downloaded third-party
reading copies and one personal settings file were retained locally and
excluded. Narrow ignore rules prevent accidentally staging those locations.
Environments, caches, downloaded dependencies and arbitrary local files were
not added. Explicit path lists were used; there was no indiscriminate staging
or deletion. Frozen tracked producers and archives were not edited.

## Assessment delivery and future integration

Assessment implementation commits are `5f96b9ec` (label adapter/protocol/v1)
and `601ebcdc` (reviewed lower-pi minimality check, v2 receipt and 19-test
receipt). They preserve the v1 source and evidence rather than overwriting
history. The complete assessment and independent reports were committed at
`ece17aed4b179cf863a628fd0ea13bef67b7a15c` and pushed to origin/dev.

The [post-push delivery receipt](provenance/delivery_verification.json) verifies
that payload's remote SHA equals local HEAD, both main pointers remain
unchanged, all former branch tips remain reachable, 297 local link targets
resolve, and 143 receipt/source/input hash bindings match. It records the
19-test receipt and absence of modifications/deletions to frozen tracked
source, tests, release methods and evidence. The 14 required assessment
documents are present. These checks add no pricing data or external-link
availability guarantee.

The receipt and this factual delivery note are committed afterward as a
closeout record. Its document hashes refer to the verified `ece17aed` payload;
they do not purport to hash the subsequent self-referential closeout text.
The final response reports the separately verified remote SHA after this
closeout record is pushed.

Main remains the stable integration branch, dev the complete ongoing project.
[MAIN_BATCH_PLAN.md](MAIN_BATCH_PLAN.md) specifies reviewable future snapshots.
No batch has been merged into main by this task. No remote protection, unique
branch work or unresolved PR prevents the requested two-branch organization.
