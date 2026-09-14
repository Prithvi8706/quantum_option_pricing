# PR #1 reconciliation and merge gate

14 September 2026. User explicitly requested inspection of neutral checks,
resolution of blockers, reconciliation of local edits, verification and merge.
Neutral/skipped GitHub conclusions were not treated as approval. Their attached
Macroscope report said “Not approved” and reported additional findings.

## Additional review findings

| Finding | Verified disposition |
| --- | --- |
| Schema integer overflow (4004480007) | Overflowing integer conversion returns a violation; covered for estimates, prices, clipping and interval elements. |
| Materializer vendor directory (4004480010) | Directory exists in the distributed original snapshot, so the stated failure did not reproduce. Parent directories are now explicitly created defensively. Original archive is unchanged. |
| Smoke support rule (4004480016) | Reconciled the user's benchmark-selected support rule, producing q_total=1e-5, with the journaled runner; records retain support and acquisition parameters. |
| Multi-suite XML acceptance (4004480017) | Check all suites; reject failures/errors in later suites, empty reports and zero tests. |
| RQMC JSON serialization (4004480019) | Not reproduced: estimates is already a list of Python floats; only the separate samples variable is an ndarray. New strict JSON serialization regression passes without changing the estimator. |
| Failed smoke attempt loses resources (4004480022) | Persist the failed record and original invocation ledger before re-raising. Unknown powers/query costs remain null, not reconstructed. Reruns cannot silently replace a failed attempt. |
| Changed shots reuse results (4004480031) | Shot-specific attempt keys plus a persisted acquisition configuration. Changed configurations require a new output directory and cannot receive a stale success marker. |
| Restarted integer RNG seed (4004480032) | Reconciled the user's persistent Generator derived from the recorded stream key; per-round calls advance it. |
| Incomplete handoff dependencies (4005052042) | Include Paper A Python sources, its configuration JSON and the research package initializer in future verification snapshots. |
| Rescaling above one (4005052047) | Enforce finite 0<c<=1 at payoff and circuit boundaries; tests cover invalid finite and nonfinite values. |
| Missing raw archives/default CLI (4005052050) | Clearly label local-only evidence and its actual owner-workspace location. Added archive-root/source arguments and actionable preflight failures; replayed using the full local input root. See [archive inputs](ARCHIVE_INPUTS.md). |
| Stream-coordinate collisions (4005052056) | Reject separators in free-form coordinates and invalid integer coordinates, preserving the existing valid-key format. |
| Git metadata depends on caller cwd (4005052060) | Reconciled source-root lookup and dirty-state reporting. Source distributions without Git report unavailable/null, never invented clean provenance. |
| Unknown experiment labels (4005052068) | Enforce exact total count, per-label counts and label set before publishing analysis; unknown records fail the integrity gate. |

Additional cross-file findings were addressed: the BAE wrapper now rejects dirty
checkouts; manifest names and dependency inventories use the same safe portable
path normalization throughout the affected consumers. Historical commands/status
and local-only evidence links have explicit current-scope notices. Archived
source snapshots retain their original bugs as historical evidence and are not
silently repaired or described as newly approved executables.

## Reconciliation of six tracked local edits

Before editing, all six were preserved in the named Git stash
`Preserved six user edits before PR1 reconciliation 2026-09-14`.
The stash is retained as a recovery copy; it is not reapplied over the reconciled
code because that would reintroduce superseded implementations.

- Plan correction to the selected support budget: retained.
- e0.json duplicate unused tolerance table removal: retained; validation constants
  remain the actual gate authority and were not loosened.
- Source-root environment capture and git_dirty field/test: retained and extended
  to handle unavailable metadata explicitly.
- Smoke support selection, recorded parameters and advancing Generator: integrated
  with the newer recovery/failure and acquisition-identity safeguards.
- Schema call to the production clipping helper: deliberately not adopted. The
  independent max(0,price) check avoids validating a helper against itself, while
  the newer finite/type guards remain intact. Original edit is in the stash.
- Filtering unknown shot entries out of total costs: not used to imply complete
  costs. Successful sampler metadata is required; failed attempts preserve the
  actual partial ledger and explicitly unknown totals.

Unrelated untracked `.claude`, manuscript outputs, downloaded papers, environment
caches, the June plan and large raw archives remain local and are not bulk-added.
No historical result was deleted or overwritten. The only completion-marker
invalidation is in new runner behavior/tests, not a deletion of historical runs.

## Verification evidence

- Focused reconciliation/regression run: 73 passed, 9 upstream warnings,
  110.25 seconds. Final full suite: **410 passed**, 11 upstream warnings,
  **336.99 seconds**, including all 20 new second-pass regressions. Report:
  `results/journal_sprint/tests_merge_integrated_v1.xml` in the main workspace.
- Week-1/2 reconstruction: 43,200 rows and 216 cells verified; 74 input hashes
  across three original archives. Output `merge_closeout_v1` under the main
  workspace's results/journal_sprint directory. No new pricing draws.
- Week-3 summary replay: 926 hashes across ten archives verified, with the
  existing circuit/reference checks. Output `merge_week3_summary_v1`.
- Updated finite numerical diagnostic: output `merge_numerical_v1`; all 312 cases
  passed, with records byte-identical to week 9. Eighteen reference sets were empty,
  78 full and none finally multicomponent. This is not formal certification.
- Ruff passed on both research packages. Whitespace checks passed. Test bytecode
  cache changes are excluded from commits.

## Merge policy

The user authorized merge after this verification. No required branch-protection
policy was reported for main; merge will use the normal GitHub path and exact-head
guard, not an admin bypass. Macroscope's automatic-approval eligibility setting
and the previous “Not approved” report are not relabeled as an approval of this
new revision. No billing limits or paid retry settings are changed.

This closes a code-review/integration milestone, not publication readiness.
Week-10 scientific work, confirmation, authorship approval and journal decisions
remain separate. The final merge result is recorded in the PR conversation.
