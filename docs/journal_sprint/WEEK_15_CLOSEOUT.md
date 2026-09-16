# Week15: reproduction completed; confirmation blocked

## Outcome

Completed the permitted fresh-environment reproduction milestone and explicit
gate assessment. **The planned confirmation campaign is not completed.** No
held-out regimes, new confirmation seeds, tuned methods, scientific promotion
or human sign-offs were invented to bypass the week14 NO-GO decision.

Weeks13-14 merged in [PR#4](https://github.com/Prithvi8706/quantum_option_pricing/pull/4),
commitd5e1c3f290906e4c9bad53845da477791002dcb7 on2026-09-16T16:53:14Z.
Both new independent reviewers accepted that bounded merge; the fresh full
807test run and both replays passed. Macroscope skipped with exhausted credits.
The user separately authorized this week15 work, independent review and merge.

## Fresh-environment evidence

Protocol e9c673ef, installer amendment958a7a9c, detached clean checkout
`.context/week15_reproduction` at958a7a9c01133b9e2606edfc1a72e03ccac1573b.
Created `.context/week15_env_v1` from Python3.9.13 without system-site packages.
Installed pinned runtime/test packages into it, not copied from the old venv.
Package-manager wheel cache was reused; this is a fresh installed environment,
not a new machine, new operating system or independent algorithm implementation.

| Check | Observed result |
|---|---|
| Environment isolation | NumPy/SciPy/Qiskit imports resolve inside the new prefix; system-site packages false |
| Version pins | All22requirements match, including pip23.2.1; bootstrap setuptools58.1.0 additionally recorded |
| Dependency consistency | pip check exit0, no broken requirements |
| Fresh tests | 123passed,17upstream warnings,44.37s; zero failures/errors/skips |
| Strict week13 replay | 104files,6cases,24circuits PASS |
| Strict week14 replay | 2022files,93tasks PASS |
| Independent scalar formulas | All6week13 cases, including week14's16path input, PASS |
| Derived analysis | All58week14 cells exactly equal saved JSON |
| Original preservation | Both original and clean-checkout archive inventories/hashes unchanged |

The123tests are the week13/14 test files, not the entire807test repository suite.
The807premerge tests ran separately in the original environment. The minimal
replay environment deliberately does not install historical Aer/Finance or web
app dependencies. No claim those unrelated suites were tested in the new venv.
The strict environment and native-source checks were not relaxed. No discrepancy,
failed replay or runtime-package installation failure was observed. Bootstrap
pip22.0.4 lacked --report; pip23.2.1 was explicitly pinned in the new venv before
runtime installation. The old venv was not upgraded.

## Artifact map and reproducibility limits

Archive: `results/journal_sprint/w15_reproduction_v1`.
`complete.json` hashes all10other tracked files and explicitly excludes the two
local raw installer logs, preserved losslessly in `installation_logs.zip` with
separate member hashes. No original log was deleted. `install_report.json`
contains runtime wheel URLs/hashes; bootstrap activity is retained in its log,
not claimed as a preinstallation hash-locked supply-chain verification.
`environment.json` records pins/inventory, executable/prefix, pyvenv config,
import locations, platform/thread settings, native/producer identities and Git
checkout. Requirements hashes describe the actual checked-out Windows bytes;
normal Git text newline conversion is not a scientific source amendment.

`tests_fresh.xml`, `week13_replay.json`, `week14_replay.json`,
`scalar_formula_audit.json`, `analysis_reproduced.json`,
`analysis_comparison.json` and `original_integrity.json` record the checks.
The replay intentionally reuses frozen RNG streams and evidence; it is not
912new independent observations, fresh statistical confirmation or hardware
execution. All earlier model, finite-target, CI/stopping and cost caveats remain.

The scalar auditor uses a separate standard-library formulation but existed
before this week. Exact58cell reproduction uses the project analysis implementation;
that equality check alone is not an independently derived statistical proof.
Independent subagent count/formula/table review is recorded separately in
[WEEK_15_REVIEW.md](WEEK_15_REVIEW.md), not labeled human peer review.

## Commands

From the repository root, creation required absent environment/output paths:

```powershell
venv/Scripts/python.exe -m venv .context/week15_env_v1
.context/week15_env_v1/Scripts/python.exe -m pip install pip==23.2.1 --log results/journal_sprint/w15_reproduction_v1/pip_bootstrap.log
.context/week15_env_v1/Scripts/python.exe -m pip install -r .context/week15_reproduction/research/journal_sprint/requirements-week15-replay.txt --report results/journal_sprint/w15_reproduction_v1/install_report.json --log results/journal_sprint/w15_reproduction_v1/install.log
```

For replay, work from the detached checkout and invoke the new interpreter by
its absolute path (or `../week15_env_v1/Scripts/python.exe` relative to checkout):

```powershell
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$env:PYTHONDONTWRITEBYTECODE='1'
../week15_env_v1/Scripts/python.exe -m pip check
../week15_env_v1/Scripts/python.exe -m pytest research/journal_sprint/tests/test_asian_encoding.py research/journal_sprint/tests/test_run_w13.py research/journal_sprint/tests/test_w14_circuits.py research/journal_sprint/tests/test_w14_comparators.py research/journal_sprint/tests/test_run_w14.py research/journal_sprint/tests/test_w14_analysis.py -q
../week15_env_v1/Scripts/python.exe -m research.journal_sprint.run_w13 verify results/journal_sprint/w13_encoding_v1
../week15_env_v1/Scripts/python.exe -m research.journal_sprint.run_w14 verify results/journal_sprint/w14_finite_v1
../week15_env_v1/Scripts/python.exe scripts/verify_week13_independent.py results/journal_sprint/w13_encoding_v1
```

Receipts additionally call `w14_analysis.analyze` and compare its complete result
to the saved JSON, using exclusive `storage.write_json` outside the originals.
Choose fresh output paths for another reproduction; do not overwrite this record.

## Week15 disposition checklist

- [x] Assess entry gate; retain NO-GO.
- [x] Freeze bounded reproduction protocol and pinned environment recipe.
- [x] Fresh installation, module provenance and dependency consistency checks.
- [x] 123focused tests, both strict replays, scalar formulas and58cell comparison.
- [x] Preserve all original sources/evidence and record limits/failures honestly.
- [ ] Final independent software/scientific reproduction review and merge.
- [ ] Continuous-price error enclosure/admitted application.
- [ ] Useful defensible prior-work distinction and same-target comparisons.
- [ ] Actual collaborator sign-off and frozen confirmation sample/multiplicity plan.
- [ ] Fresh held-out confirmation campaign; **not run because prerequisites fail**.

Next step requires explicit scientific gate-resolution work or a visible route
replan, not automatic promotion to a completed confirmation/manuscript claim.
Week16 remains planned; the scientific week15 confirmation block is still open.
