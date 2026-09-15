# Archive availability and verification inputs

Update: the week-10-through-week-11 integration includes the complete new
archives enumerated in [the PR handoff](PR_WEEKS_10_11_HANDOFF.md), including
failed/superseded attempts and their provenance. The older partial-export
limitations below still apply to the week-1-9 historical inputs, not those
explicitly bundled new archives.

The repository deliberately includes partial evidence exports. Most historical
`results/journal_sprint/...` paths in week reports refer to the originating local
workspace, not files available in a fresh GitHub checkout. This includes the
full week-1–8 raw/replay archives, test XML and downloaded primary papers.
The complete V2A baseline used by regression tests is the documented exception.
No public download location for omitted raw archives is currently provided.

For this project's owner, the preserved input root is:
`C:/Users/prith/quantum_option_pricing/results/journal_sprint`.
Other reviewers need a copy of the complete relevant archives from the owner;
do not mistake a summary plus completion manifest for a complete input archive.
Downloaded papers are not redistributed through this PR.

Read-only reconstruction can consume an explicit input root and write to a new
output directory without overwriting historical evidence:

```text
python -m research.journal_sprint.closeout --archive-root PATH_TO_FULL_ARCHIVES --output PATH_TO_NEW_CLOSEOUT
python -m research.journal_sprint.week3_summary --archive-root PATH_TO_FULL_ARCHIVES --output PATH_TO_NEW_SUMMARY
```

For new V2C acquisitions, the input is the complete V2B archive:

```text
python -m research.journal_sprint.run_price_intervals --source PATH_TO_FULL_V2B --output PATH_TO_NEW_RUN
```

Alternatively regenerate V2B with `python -m research.journal_sprint.run_tighter_gate`
from the bundled V2A baseline. This is a new artifact, not replacement evidence
for a historical run. Missing required archives fail before completion with an
actionable input-location message. Strict verifiers can still reject current
source files that differ from historical producer snapshots; path portability
does not waive that identity requirement. See [historical reconstruction](ARCHIVE_REPLAY.md).
