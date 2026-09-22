# Reproduction

Run from the repository root. Scientific dependencies remain the pinned lock
in `research/controlled_completion_followup/requirements-lock.txt`. Use Python
3.9.13 (the recorded interpreter), create an isolated virtual environment and
install that file. The executed continuation used the already-created isolated
`.context/controlled_closeout_repro`, with system/user packages disabled.

```powershell
$env:PYTHONNOUSERSITE='1'
.context/controlled_closeout_repro/Scripts/python.exe -m pytest research/antithetic_feasibility research/compound_feasibility research/controlled_residual_feasibility research/controlled_source_completion/test_completion.py research/controlled_completion_followup research/controlled_priority_completion -q
.context/controlled_closeout_repro/Scripts/python.exe -m research.controlled_priority_completion.artifact_audit
```

The audit is read-only unless `--freeze` is explicitly supplied. A fresh freeze
is for a new authorized evidence release, not for making changed results appear
to match an old manifest. The audit also verifies 895 historical artifacts and
25 preserved source snapshots against their original hashes.

Development reproduction, in dependency order (writes only the continuation's
new generated artifacts):

```text
python -m research.controlled_priority_completion.estimator_hadamard
python -m research.controlled_priority_completion.estimator_bounded --replay
python -m research.controlled_priority_completion.range_audit
python -m research.controlled_priority_completion.range_joint_arithmetic
python -m research.controlled_priority_completion.parallel_run
python -m research.controlled_priority_completion.ranged_run
python -m research.controlled_priority_completion.combined_cost
python -m research.controlled_priority_completion.combined_replay
python -m research.controlled_priority_completion.combined_wrappers
python -m research.controlled_priority_completion.capacity_screen
python -m research.controlled_priority_completion.capacity_revised
python -m research.controlled_priority_completion.capacity_revised --source-root results/controlled_priority_completion/range_compile_v1 --output results/controlled_priority_completion/capacity_range.json
python -m research.controlled_priority_completion.range_sampling_screen
python -m research.controlled_priority_completion.review_compiler
python -m research.controlled_priority_completion.capacity_estimator_review
python -m research.controlled_priority_completion.capacity_integration_review
```

The deterministic numeric counts/bounds can be compared directly. Local paths,
CPU diagnostic timings and environment provenance can differ after regeneration;
they are not quantum execution times. Do not overwrite the archived reference
package and then claim its old byte manifest verifies the regenerated copy.
Use a separate checkout for full regeneration. Local downloaded primary papers
are not redistributed; the relevant links and reading depth remain in the
reports. Numerical estimator generation does not require the local paper cache.

The document renderer is separate from the scientific environment. The executed
build used Markdown 3.7 in `.context/controlled_document_tools` and installed
headless Microsoft Edge. Install Markdown into that directory, then run:

```text
python -m research.controlled_priority_completion.build_draft
```

`--browser` can supply a compatible installed Chromium/Edge executable. The
build writes Markdown-derived HTML/PDF and a byte-hash receipt. PDF metadata can
change between builds; it is the frozen PDF hash, not assumed deterministic
browser output, that identifies the reviewed draft. PyMuPDF 1.24.14 was used only
to inspect the generated seven-page PDF, not for any pricing computation.

No command above submits a paper, runs the full multi-million-qubit QAE on a
simulator, confirms advantage on held-out cases or provides hardware timing.
