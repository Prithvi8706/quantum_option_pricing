# Comparator case-study manuscript

[Read the manuscript](main.md). This is a complete research draft for human
scientific and authorship review, not a submitted or accepted paper. Its
contribution is a reproducible, restricted comparator finding. It does not
claim a new quantum primitive or quantum-over-classical advantage.

## Evidence and figures

- `artifacts/historical_v1/` contains the historical 166-row table, selected
  comparisons, width/CX plots, and matched-parent mechanism plots.
- `artifacts/common_v1/` contains the separately acquired six-oracle common-policy
  comparison, error allowances, claim/evidence mapping, and cost plots.
- Each figure is supplied as PNG, SVG and PDF. Tables are CSV and Markdown.
- Each artifact directory has a manifest binding producer, source evidence,
  software versions and output bytes. The manuscript separates historical
  ledgers from the new compiler policy.

## Reproduce

Run from the repository root. Use a new output directory for each command;
the producers deliberately refuse to overwrite an existing directory.

```powershell
# Historical figures: Python 3.9.13 and matplotlib 3.9.4 in the recorded run.
venv/Scripts/python.exe -m research.manuscript_20260922.artifacts .context/historical_replay_new

# Common-policy figures consume the completed archive; no circuit reacquisition.
venv/Scripts/python.exe -m research.manuscript_20260922.common_artifacts results/journal_sprint/common_compilation_20260922_v2 .context/common_figures_replay_new

# Small correctness checks in the pinned Terra 0.46.3 environment.
.context/week15_env_v1/Scripts/python.exe -m pytest tests/test_common_compilation_20260922.py tests/test_assessment_label_bridge.py tests/test_week2_decoding.py -q
```

The local environment paths are examples, not committed dependencies. Consult
the acquisition's `planned.json` for exact Python/library versions and source
hashes. Reacquiring circuits is optional and bounded by the
[frozen protocol](../../docs/release/COMMON_COMPILATION_PROTOCOL_20260922.md).
It requires a checkout matching the recorded producer hashes and the pinned
Terra version. Do not overwrite either retained attempt. The first attempt
failed a JSON representation guard before producing any six-oracle results;
the corrected attempt has a distinct source commit and output directory.

The rendered Markdown manuscript links its evidence directly. No journal
template, author list or submission package is implied. Rotation synthesis,
fault-tolerant scheduling and human significance review remain separate work.
