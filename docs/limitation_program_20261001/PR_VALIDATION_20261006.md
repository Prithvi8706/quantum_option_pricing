# Checkpoint publication validation — 6 October 2026

Validation was performed in an isolated checkout based on `origin/main` at
`34e0877d`, using the retained local Python 3.12.4 research environment.
These are code regression checks; they add no scientific fixture credit.

| Check | Result |
|---|---|
| `pytest -q tests/test_exact_coefficient_lookup.py` | 12 passed, 14.18 seconds |
| `pytest -q research/controlled_source_completion/test_completion.py` | 32 passed, 41.51 seconds |
| Both suites after the independent review correction | 46 passed, 35.62 seconds (14 lookup tests and 32 existing regressions) |
| `ruff check research/controlled_source_completion/exact_lookup.py tests/test_exact_coefficient_lookup.py` | Passed |
| Compact evidence index | All 14 original hashes matched; eight published receipts also matched the Git index byte for byte |
| Ledger reconciliation | 110 entries: 6 complete, 53 partial, 25 ready, 18 conditional, 8 audit; no active research items |
| Publication selection | Plans, reports, compact receipts and lookup source/tests; environments, raw arrays, downloaded paper and unexecuted handoff helper excluded |
| Credential patterns | No matches in the selected files for the bounded private-key/token patterns checked |

The existing compiler suite reported three pending QFT deprecation warnings.
Independent PR review found that padding an implicitly zero sparse lookup to
`2**bits` rows could exhaust memory for a wide address. The publication fix
keeps missing rows implicit, retains the constant-row optimization for full
tables, and advances the cache lowering tag to `shared-prefix-xor-v2`. Two
32-bit sparse-address regression cases cover nonzero and zero rows. These
source/test changes are isolated from the frozen local campaign, whose old
source bytes and accepted result costs are preserved.

The `.gitattributes` additions preserve receipt bytes and historical reports'
existing line endings and final blank lines.

The independent overall-progress audit is published in `checkpoint_evidence/`.
A separate independent review must approve the final PR commit before merging.
The original workspace retains the initial selection-validation receipt at
`.context/ROOT_CHECKPOINT_PR_SELECTED_VALIDATION_run001.json` and the final
corrected snapshot validation at
`.context/ROOT_CHECKPOINT_PR_SELECTED_VALIDATION_run002.json`. No raw campaign
rerun, full application test suite, or physical quantum execution was performed
for this publication.
