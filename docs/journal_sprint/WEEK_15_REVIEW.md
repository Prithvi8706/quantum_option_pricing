# Week15 independent reproduction review record

Review scope: fresh-environment reproduction only; confirmation is blocked.
Reviewers are Bacon (software/provenance) and Darwin (scientific claims), read-only
and independent of main's installation/reproduction orchestration. This is not
human collaborator sign-off or journal peer review.

## Before execution

Both independently reviewed the merged weeks13-14 scope and accepted the gate
interpretation: reproduce existing evidence, do not silently replace the
application or call development seeds held-out confirmation. Original producer
commits remain e59782a7/week13 and76914458/week14. PR#4 merge d5e1c3f2.

Reproduction protocol initially e9c673ef; before runtime installation, bootstrap
tooling amendment958a7a9c pinned pip23.2.1 for its artifact report. Clean detached
checkout fast-forwarded to958a7a9c. No algorithm, seed, tolerance, original archive
or source-manifest edit. New venv created without system-site packages using
Python3.9.13. Cached wheel downloads are allowed; installed environments are not
copied or shared. Subsequent results and final review dispositions follow below.

## Final reproduction results

New environment123tests passed,17upstream warnings,44.37s; zero failures/errors/
skips. Both strict replays passed104+2022files,6cases/24circuits and93tasks.
Scalar-formula audit6cases and exact58cell analysis equality passed. Module
locations,22pins, bootstrap setuptools58.1.0 and pip-check0 recorded. No producing
code, old evidence or tolerance changes. Evidence commit7ce21101.

Main additionally created a separate tracked-only checkout7ce21101 and checked
all11artifact files/10manifest hashes and both ZIP-member hashes. Receipt
results/journal_sprint/w15_artifact_checkout_v1.json. Original reproduction
checkout958a7a9c is preserved. Two local raw logs are not silently missing from
the tracked archive: they are explicitly excluded and losslessly ZIP archived.

## Darwin: independent scientific/claims ACCEPT

At7ce21101, no scientific/claims merge blockers. Independently reconstructed all
96ideal fixed-method intervals from raw counts; reconciled the main comparison
table's delivery/shots/Aeq/CX including native ledgers, and all six rate
numerators/denominators across50confidence cells. Checked all10committed evidence
blobs against manifest, archive integrity, fresh-environment identities,123test
receipt, replay receipts and exact58cell equality. Confirmed unchanged scientific
producer code and appropriate narrower claims. No edits/Git writes/acquisition.

## Bacon: independent software/provenance ACCEPT

At7ce21101, no remaining software/provenance or reporting blockers for bounded
reproduction. No redundant full-test rerun claimed; acceptance of reviewed
evidence is separate from main's fresh123tests and tracked-only packaging check.
Confirmation/scientific gates remain blocked. Actual read-only checks:

- Fresh venv isolation, executable/prefix, disabled system/user site packages,
  all21runtime module locations,22pins/inventory and pip check.
- Approved native IQAE/Sampler hashes, project producer hashes, clean detached
  checkout958a7a9c and actual checked-out requirements hash.
- Pip report's21runtime packages/artifact hashes and installer-amendment chronology.
- Exact local inventory,10payload hashes, both ZIP-member/raw-log hashes, and
  both original and reproduction-checkout archive inventories.
- 123test and104/2022file replay receipts; independently recomputed six-case
  scalar audit and exact58cell analysis in the fresh environment.
- Closeout/protocol/review/planning wording and blocked-confirmation distinction.

The additional tracked-only packaging check was main's, not independently rerun
by Bacon. No human reviewer approval is implied.

## Remote review and merge

PR#5: https://github.com/Prithvi8706/quantum_option_pricing/pull/5.
Macroscope check104894407876 skipped: "Credit balance exhausted." No hosted
workflow or human review acceptance is claimed. Both independent subagent
dispositions ACCEPT; ordinary merge awaits final-head remote check. This is
approval to merge the reproduction record, not to run confirmation.
