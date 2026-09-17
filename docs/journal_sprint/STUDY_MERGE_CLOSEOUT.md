# Bounded-development and minimal-pivot study handoff

This integration brings the completed confirmation-gate development, four-paper
audit, and two-week minimal-pivot study onto the default branch. Merging software
and evidence does **not** admit the confirmation campaign or promote a scientific
claim. The reflection-centered candidate remains on standby.

## Reading order

1. [Running project record](PROJECT_LOG.md): chronology, checks and limitations.
2. [Confirmation gate results](CONFIRMATION_GATE_BOUNDS_RESULTS.md): unresolved
   prerequisites and why confirmation remains blocked.
3. [Four-paper audit](FOUR_PAPER_AUDIT.md): literature assessment and scope.
4. [Week 1 results](MINIMAL_PIVOT_WEEK1_RESULTS.md): signal construction and
   equally optimized baseline comparison.
5. [Week 2 results](MINIMAL_PIVOT_WEEK2_RESULTS.md): integration, fixed-menu
   validation, classical comparisons and negative results.

The favorable Week 2 ratios are projected logical CX reductions between two
quantum constructions, not hardware speedups or quantum-over-classical advantage.
The difficult E2 case fails the fixed accuracy menu. Physical execution error
remains unbounded. The tiny simulation is not a production-resolution run.

## Cleanup policy

Remove the accidentally tracked Python bytecode cache from version control;
existing ignore rules already prevent its re-addition. Keep the local copy.
Preserve failed/interrupted runs and superseded analysis receipts: these explain
the audit trail. Leave unrelated untracked research outputs, manuscripts and
local configuration untouched. Do not use a blanket clean or broad ignore rule
to conceal potentially useful research material.

## Verification

Final integration receipts are recorded alongside the study evidence in
`results/journal_sprint/merge_study_*`. Source and artifact hash verification
checks recorded experiments; it does not rerun the expensive acquisitions and
does not constitute independent scientific peer review. Regression tests must
run against frozen source files because provenance checks detect concurrent
source edits.

The initial fresh Windows checkout exposed a real packaging defect: 16 captured
sources were converted from LF to CRLF by Git, so W1/W2 archive verification
correctly refused them (`acquire_four_paper_code.py` was the first reported
mismatch). Commit `42731ad1` adds explicit `-text` attributes for those files.
Their source bytes and all existing experiment manifests remain unchanged.
The corrected fresh checkout passes both verifiers, and regenerated Week 2
analysis has the same SHA-256 as `minimal_pivot_week2_analysis_v2.json`.

Macroscope's PR check was skipped with **Credit balance exhausted**. This is not
a successful external review. The repository has no required branch checks;
local regression and clean-checkout verification are the integration evidence.

Final corrected checkout `42731ad1`: **1,143 tests passed**, 12 legacy warnings
(`merge_study_clean_full_tests_v2.xml`). The working-tree and initial checkout
regression runs also passed 1,143 tests each. The existing separate pinned
environment passed 51 focused W1/W2 tests. Earlier development and four-paper
archive verification passed as well. All 81 changed Python files passed Ruff F
checks; this is not a full legacy-style lint claim. Final changes after these
checks contain only documentation and verification receipts.

## Contribution workflow

Preserve the existing substantive commit history with a normal merge, rather
than reconstructing it for activity counts. Future commits should represent
completed, reviewable changes: an implementation, a regression fix, a verified
experiment, or a useful methods/evidence update. Open PRs around coherent work
packages, include negative results, and attribute only genuine contributions.
Do not create empty commits, backdate activity, or assign honorary authorship.

GitHub profile credit requires eligible commits on the default branch with an
author email associated with the account. Contribution dates reflect real commit
dates, not an invented daily streak; updates may take up to 24 hours. See
[GitHub's contribution criteria](https://docs.github.com/en/account-and-profile/reference/profile-contributions-reference)
and [missing-contribution troubleshooting](https://docs.github.com/en/account-and-profile/how-tos/contribution-settings/troubleshooting-missing-contributions).
