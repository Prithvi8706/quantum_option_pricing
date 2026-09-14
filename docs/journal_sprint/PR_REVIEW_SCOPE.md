# Journal reengineering PR: weeks 1–9

Requested by the user on 14 September 2026 so Macroscope review can follow.
This supersedes earlier operational instructions to hold PR creation pending
Macroscope. It does not imply Macroscope approval, merge approval or submission.

## Included

- The 19 existing Paper A foundation commits required by the sprint, plus sprint
  Python source/tests, the licensed comparator extract and its license/notice.
- Research plans, protocols, historical claim corrections, week-1–9 logs and
  closeouts, current manuscript and proposed week-10 evidence gate.
- Selected small week-5–9 summaries, original completion manifests and week-9
  numerical records/replay summaries. These are deliberately partial evidence
  exports, not complete replay archives. Completion-manifest entries can refer
  to omitted files; the manifests preserve original provenance, not a claim
  that this checkout contains every hashed artifact.
  Git attributes disable newline conversion for these evidence files so their
  original bytes, rather than just their parsed JSON values, are retained.

## Excluded and preserved locally

Raw large pricing archives and source snapshots, downloaded papers, external
comparator clones, virtual environments, historical manuscript binaries,
`.claude`, unrelated plan files, and uncommitted Paper A user edits. Earlier
documents refer to local evidence paths that are not all distributed in this PR.
Full archive-verification commands require those complete local archives;
do not interpret a missing archive as a numerical result.

## Review focus

Start with [claim boundaries](WEEK_9_CLAIM_EVIDENCE.md), the
[current manuscript](MANUSCRIPT_RELIABILITY_DRAFT.md), and
[week-9 closeout](WEEK_9_CLOSEOUT.md). Review calibrated inversion and failure
allocation, deterministic price bounds, all-branch intersection, refusal and
declaration semantics, pilot/final separation, cost accounting and provenance.
Check that no discovery result is described as confirmation or advantage.

Known limits: delivery concentrated on E001; paid representation selection did
not improve delivery; finite numerical diagnostics are not certification;
matched end-to-end native/classical comparison and journal novelty remain open.
Week-7 inference arms share observations. Week-8 v2 is not an independent replicate.

The local working-tree integrated run passed 337 tests before a verifier-only
change, followed by a successful replay. Some unrelated Paper A changes existed
in that tree; a separate PR-tree check is therefore needed before attributing
that exact full-suite result to this PR. Astra-requested review was bounded;
Macroscope review is pending and will be initiated by the user.

After PR creation, the automatic Macroscope check was skipped: estimated cost
39.12 USD exceeded the workspace's 10 USD per-review limit. No paid retry or
billing-limit change was requested by the agent. These are the check's estimates,
not a fee guarantee for a later updated diff.
