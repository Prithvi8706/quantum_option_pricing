# PR #1: Macroscope findings and fixes

14 September 2026. Reviewed all 15 inline findings from Macroscope reviews of
21c032bb and 8009d41e. The earlier cost-limit notice is historical: the user
triggered a completed review. A bot's “no longer relevant” label was not treated
as evidence that the underlying code was fixed.

Fixes are made in the separate PR checkout, excluding the main workspace's
uncommitted Paper A edits. No original experiment archive or completion manifest
is rewritten. These corrections do not retrospectively certify past runs.

| Finding (GitHub discussion ID) | Disposition |
| --- | --- |
| 4002229082: nonfinite spot/strike | Reject nonfinite values for all six numeric contract inputs before domain comparisons; 18 parameterized regressions. |
| 4002229083: assertions removed by optimization | Replace runtime assertions throughout sprint production modules with explicit exception gates, including the additional comparator/classical/verification instances. An AST regression prevents reintroduction; an optimized subprocess rejects a tampered archive before creating verification output. |
| 4002229085: malformed confidence intervals | Validate sequence shape, finite numeric elements and ordering before indexing; malformed data returns violations. Also guard estimation/price numeric types. |
| 4002229086: invalid smoke outputs marked complete | Invalidate stale COMPLETE before recovery, persist validation output, reject violations and mismatched attempt inventories before atomically publishing a new marker. |
| 4002229090: dropped sampler batch members | Transpile, submit and record the entire batch; validate metadata cardinality and per-circuit effective shots. Failures retain each member's in-memory ledger entry. The ledger itself is not falsely called disk-durable. |
| 4002229093: dirty pinned BIQAE checkout | Reject tracked or untracked checkout changes before source import; targeted test ensures modified source is not executed. |
| 4002229094: Windows manifest names on POSIX | Normalize source/manifest names consistently with PureWindowsPath before native joins and inventory comparison. Reject absolute, traversal and aliased dependency paths. Tests cover Windows separators and tampering; a native Linux run was not performed. |
| 4002229095: unbounded sine inversion | Maximum supported depth 4096, enforced before branch generation and at public depth-vector validation. Reject out-of-int64 inputs before casting. Existing discovery depths are unchanged. |
| 4002229105: missing environment recipe in handoff | Include requirements-legacy-circuit.txt in future verification snapshots. It is a candidate environment recipe, not proof of exact historical equivalence. |
| 4002229106: flush without fsync | Append-only records flush and fsync before returning; regression spies on the fsync request. Filesystem/power-loss durability is not unconditional. |
| 4002229108: tautological dollar gate | Compute an independent encoded-payoff expectation from PMF and payoff angles, and compare both inverse conversion and discounted price against it. Do not incorrectly compare the nonlinear encoded value to the linear grid payoff. Mutation tests detect broken inverse and price conversion. |
| 4002229110: pilot phase misses time limit | Check after each persisted pilot trial and before final completion; a simulated timeout retains the trial and prevents COMPLETE. |
| 4002229111: arbitrary HTTP 200 accepted as reading | Require expected primary URL, paper-title prefix, article structure and abstract before saving content. Non-article responses and request failures are explicit unsuccessful retrieval records. No new paper downloads were needed for tests. |
| 4002229113: interrupted raw/resource pair | Persist a durable journal containing both original payloads before either append; recover missing records without resampling or inventing resources. Legacy partial pairs without a journal fail closed and remain available for audit. Conflicts/duplicates prevent completion. |
| 4002237697: missing V1 protocol in historical snapshot | Preserve snapshot immutability. Supply the original V1 protocol separately, matching the hash already in planned.json, and a verified materialization helper. See [archive reconstruction](ARCHIVE_REPLAY.md). No archived comparator code is silently edited. |

## Validation and remaining scope

Initial focused regression run: 52 passed, 9 upstream warnings, 24.61 seconds.
An additional materialization regression was then added. The full PR-checkout
suite passed **390 tests**, with 11 upstream warnings, in **142.10 seconds**.
This includes all 53 new regressions. Report:
`results/journal_sprint/tests_macroscope_fixes_v1.xml` in the main workspace.
Ruff passed on the sprint and all changed Paper A Python files; whitespace
checks passed. No test was skipped or weakened to obtain these results.

The updated numerical diagnostic reran 312 cases: zero failures, 18 empty,
78 full, zero final multicomponent references; maximum slack
1.1003482766924545e-13. All saved numerical record bytes equal the original
week-9 diagnostic. Archive: `results/journal_sprint/macroscope_numerical_v1`
in the main workspace, not included as a duplicate evidence export in this PR.
This is unchanged finite diagnostic evidence, not certification or new pricing
replicates. Historical strict live-source checks should reject today's changed
producer files against old snapshots; do not weaken that provenance gate.

No merge, submission, new authorship or manual paid review retry was requested.
Macroscope's re-review/approval of these fixes is a separate outcome; the original
review must not be relabeled as approval of subsequent changes. Attempting to
reuse the earlier Astra reviewer returned “agent not found”; no new Astra
approval is claimed for this fix set.
