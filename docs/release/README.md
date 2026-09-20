# Release preparation tools

These checks are a fast, read-only overlay on frozen evidence, not a replacement
for the full circuit-reconstruction verifier or human review.

From the repository root, use the existing pinned environment:

```powershell
.context/week15_env_v1/Scripts/python.exe -m research.release_checks.audit --require-environment --output NEW_AUDIT.json
.context/week15_env_v1/Scripts/python.exe -m research.release_checks.tables NEW_TABLE.csv
```

Outputs must not already exist. Neither command installs dependencies, changes
archives or runs hardware. An environment mismatch gives audit exit2 when
required; artifact errors produce a nonzero exit. A successful audit leaves
scientific admission false. The CSV includes all12 configurations, including
infeasible plans, with exact integer counts and explicit logical-projection labels.

The scope pins four archive-completion manifests; their hashes cover the recorded
source/input inventories. Editing scope or claims changes the reviewed release
candidate and requires review. No signature or external trust is inferred.
Version equality is not a complete wheel/ABI/platform reproducibility guarantee.

The generated table refers to the fixed $1, at-least95%-confidence development
study. Do not relabel its projected counts as runtime, measured prices, new
experiments or quantum advantage. Test receipts describe historical executions;
overlapping runs are not additive.

Full reconstruction remains available through
`research.journal_sprint.verify_matched_arithmetic`; see the
[reviewed study](../journal_sprint/MATCHED_ARITHMETIC_REVIEW_20260917.md).
