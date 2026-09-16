# Week15 bounded reproduction protocol (not confirmation)

## Entry decision

PR#4 merged weeks13-14 atd5e1c3f290906e4c9bad53845da477791002dcb7 on
2026-09-16T16:53:14Z after new independent Bacon/Darwin reviews,807fresh full
tests and both archive replays. Macroscope skipped due exhausted credits; no
human approval or hosted workflow test pass is implied.

The scientific confirmation gate remains NO-GO. The active plan's week15 step3
allows independent reproduction, and its fallback requires recording blocked
confirmation. This protocol executes that bounded milestone only. It does not
replace the primary application, create new held-out regimes/seeds, retune a
method or claim a signed confirmation protocol. Both new reviewers accepted
this distinction before execution.

## Prespecified procedure

1. Commit this protocol and minimal pinned replay requirements. Create a detached
   clean source checkout of that commit. Preserve original source and archives.
2. Create a new Python3.9.13 venv in absent .context/week15_env_v1, with no system
   site packages. Install requirements-week15-replay.txt from packages, not by
   copying the old venv. The base interpreter/OS may be the same; that is not a
   new machine, independent implementation or cross-platform reproduction.
3. Retain installer report, installed version inventory, pyvenv configuration,
   executable/prefix/module locations, commands and pip-check outcome in separate
   results/journal_sprint/w15_reproduction_v1. Record failures/discrepancies; do
   not quietly relax requirements or the strict verifier.
4. With OPENBLAS_NUM_THREADS, OMP_NUM_THREADS and MKL_NUM_THREADS set to1 and
   PYTHONDONTWRITEBYTECODE=1, run all123new week13/14 tests, then the unchanged
   strict verifiers on both original archives. Recompute all58week14 analysis
   cells and compare exactly with saved derived JSON. Run the existing stdlib
   week13 formula audit (all6cases, including week14's16path input table).
5. Retain receipts outside the original archives. Hash/inventory-check the
   originals before/after. Record any failure before a versioned repair/retry;
   do not alter original snapshots, manifests or tolerances to obtain a pass.
6. Have independent subagents review the reproduction evidence and blocked
   confirmation disposition. If no implementation/report blockers remain, merge
   this reproduction record separately. Code merge does not clear science gates.

## Coverage and limits

The minimal environment is for these replay modules/tests, not the full web app
or historical Aer/Finance suites. The complete807test suite has already been run
in the original environment at premerge. Report the123fresh-environment tests
separately, not as all807. Original frozen RNG streams are intentionally reused
for deterministic replay; this is not new confirmation data or912new independent
acquisitions. Simulator timing is not hardware timing. Native source hashes and
environment checks remain enforced unchanged.

Installation artifact hashes will be captured by pip's report, not invented as
preinstallation supply-chain attestations. These version pins cover the intended
runtime; record any resolver-added packages and their actual versions. The
existing Windows platform has no installed symengine requirement under Terra's
case-sensitive machine marker; the new environment must still pass pip check.

## Confirmation prerequisites remain open

Continuous bias/error enclosure; a non-enumerative oracle or visibly replanned
defensible finite application; useful prior-work distinction; same-target strong
classical comparisons/paid noise learning where claimed; justified native
coverage wording; actual collaborator review; and a signed primary-outcome,
held-out-regime/sample-size/multiplicity protocol. No new confirmation campaign
will be run under this reproduction protocol. Completion means reproduction
completed with confirmation blocked, not week15 confirmation completed.
