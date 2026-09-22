# Committed-checkout verification receipt

22 September 2026. Computational candidate:
`fcd4b1fa1d087d07c020e6f93ce9f9f423ae0a01`.
This receipt and subsequent PR/merge metadata do not change its numerical work.

A separate detached checkout of that commit was created under
`.context/controlled_priority_checkout`. The isolated pinned interpreter ran
with user-site loading disabled. All five checks passed:

| Check | Result |
|---|---|
| Environment isolation | Passed; Qiskit loads from the isolated environment |
| Final estimator/wrapper/decoder tests | 20 passed; pytest reports 14.44 seconds |
| Artifact audit before replay | 503 current artifacts, 196 leaf hashes, 895 historical artifacts and 25 snapshots verified |
| Composed emitted-gate replay | C4/H8 financial+selector and financial+phase passes and inverses passed, using selected initial targets and normalizers |
| Artifact audit after replay | Same complete inventory verifies; detached checkout remains clean |

The machine-readable receipt is
`results/controlled_priority_completion/release_validation/receipt.json`.
It records the exact commit, interpreter, commands, return codes, elapsed
verification times and hashes of all five logs, with `all_passed: true` and an
empty final Git status. Log hashes are checked again before publishing the PR.

The earlier full research-suite run passed 161 tests; the final 20 overlap that
scope and are not 20 additional unique tests. Targeted Ruff and Git whitespace
checks pass. Main application sources and the original manuscript have no diff
against the previous merged main commit `15c2e1c8`. Historical global-lint and
unavailable-mypy limitations remain documented in VALIDATION.md.

Scientific decision: no established significant quantum advantage. Numerical
component certificates and implementation checks pass; the complete financial
baseline/regret and physical execution gates remain unmet. This receipt does
not attest to human author approval, journal submission or held-out confirmation.

Repository review: [PR #11](https://github.com/Prithvi8706/quantum_option_pricing/pull/11).
GitHub's Macroscope correctness check completed with **SKIPPED** and the message
"Credit balance exhausted." It supplied no automated review or approval.
Independent subagent reviews and local verification are the actual review
evidence. Main has no required branch protection; no failed required check or
protection was bypassed. The original instruction authorized PR creation and
merge after review; it did not authorize inventing journal author declarations.
