# Controlled compound follow-up

Start with [results](../../docs/controlled_completion_followup/RESULTS.md) and the
[current checklist](../../docs/controlled_completion_followup/CHECKLIST.md).
This package records a failed advantage screen, a circuit improvement and
partial financial/physical certification. It does not demonstrate advantage.

Use a fresh Python 3.9 environment with system/user site packages disabled:

```powershell
python -m venv .context/controlled_closeout_repro
.context/controlled_closeout_repro/Scripts/python.exe -m pip install -r research/controlled_completion_followup/requirements-lock.txt
```

On POSIX, replace `Scripts/python.exe` by `bin/python`. Run from the repository
root. The lock file records the tested isolated Python 3.9 environment;
`requirements.txt` also lists the direct research dependencies. The gate-library
resolver accepts both archived Windows paths and portable
workspace-relative paths, independent of the old user's directory.

Read-only verification of committed evidence:

```text
python -m pytest research/antithetic_feasibility research/compound_feasibility research/controlled_residual_feasibility research/controlled_source_completion/test_completion.py research/controlled_completion_followup -q
python -m research.controlled_completion_followup.synthesis_rotations --verify-only
python -m research.controlled_completion_followup.audit_artifacts
```

`audit_artifacts` writes only its new `arithmetic_v1/audit.json` receipt. It verifies
895 historical artifact hashes, 25 preserved source/docs snapshots, all five
unchanged digital targets and 324 new library files. The test suite includes
the independent compiler regressions, multiplier checks, financial inequalities
and signed controlled-phase/factory checks. Neither runs full pricing QPE.

To regenerate the development artifacts, use an isolated checkout; the commands
below overwrite the corresponding *new* follow-up outputs in that checkout:

```text
python -m research.controlled_completion_followup.arithmetic_run
python -m research.controlled_completion_followup.financial_bridge
python -m research.controlled_completion_followup.financial_arithmetic_audit
python -m research.controlled_completion_followup.review_baseline
python -m research.controlled_completion_followup.synthesis_rotations
python -m research.controlled_completion_followup.ft_model --ledger results/controlled_completion_followup/arithmetic_v1/cost_v3_phase64/ledger.json
```

The arithmetic run compiles four financial sources and one phase source,
executes all their emitted gates on the saved diagnostic inputs, recosts all
eight schedules and executes four fused cleanup checks. The full graphs are
hierarchical, not opaque billions-of-gates estimates. The repeated definitions
are shared through actual X/CX/CCX arrays and per-leaf hashes.

Fresh synthesis may choose different accurate sequences. Verification binds the
committed sequences to exact targets and certified errors; matrix products are
stored left to right and execute right to left. All inverse/sign conventions
are explicit. No free QRAM, unpaid Gaussian oracle or hardware service is used.

The predecessor directories are included as the provenance/dependency chain:
initial source search and screen, antithetic feasibility, compound feasibility,
controlled residuals, then complete-source compilation. Their historical
recommendations are dated; the current follow-up result is authoritative.
Downloaded third-party papers remain local and untracked; their primary links
and hashes are published in the reading-cache provenance file. The original
manuscript and its release evidence are not rewritten.
