# Checkpoint publication validation — 6 October 2026

Validation was performed in an isolated checkout based on `origin/main` at
`34e0877d`, using the retained local Python 3.12.4 research environment.
These are code regression checks; they add no scientific fixture credit.

| Check | Result |
|---|---|
| `pytest -q tests/test_exact_coefficient_lookup.py` | 12 passed, 14.18 seconds |
| `pytest -q research/controlled_source_completion/test_completion.py` | 32 passed, 41.51 seconds |
| `ruff check research/controlled_source_completion/exact_lookup.py tests/test_exact_coefficient_lookup.py` | Passed |
| Compact evidence index | All 14 original hashes matched; eight published receipts also matched the Git index byte for byte |
| Ledger reconciliation | 110 entries: 6 complete, 53 partial, 25 ready, 18 conditional, 8 audit; no active research items |
| Publication selection | Plans, reports, compact receipts and lookup source/tests; environments, raw arrays, downloaded paper and unexecuted handoff helper excluded |
| Credential patterns | No matches in the selected files for the bounded private-key/token patterns checked |

The existing compiler suite reported three pending QFT deprecation warnings.
The selected lookup implementation and its test are byte-identical to the
locally verified source and original test. The `.gitattributes` additions
preserve receipt bytes and historical reports' existing line endings and final
blank lines.

The independent overall-progress audit is published in `checkpoint_evidence/`.
A separate independent review must approve the final PR commit before merging.
The original workspace retains the detailed selection-validation receipt at
`.context/ROOT_CHECKPOINT_PR_SELECTED_VALIDATION_run001.json`. No raw campaign
rerun, full application test suite, or physical quantum execution was performed
for this publication.
