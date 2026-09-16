# Week 14 independent review record

This records AI-agent review, not human collaborator approval or journal peer
review. All initial corrections below preceded production acquisition.

## Pre-freeze work and corrections

Kant audited native Terra IQAE, vendored csAE, alternatives, conventions,
prior-work boundaries and the human-review packet. Copernicus implemented the
two comparator adapters in a disjoint source/test pair; its own unit tests are
implementation checks, not independent review of its code.

Main-agent tests found an incorrect positional GroverOperator construction;
the positional argument is the oracle, not state preparation. Fixed to explicit
flag-Z oracle and state_preparation keyword. All14 circuit fixtures then passed,
including nonzero powers and independently evolved noisy density matrices.
No production observations existed when this bug was corrected.

Hegel's independent mathematical review confirmed the finite offset identity,
global depolarization derivation, fixed CP/transfer assumptions and cost formulas.
Requested corrections:

1. Label ignored-noise CP results outside-model, even when width meets tolerance.
2. Freeze hull-containment, empty-set, cap and erroneous-declaration denominators;
   do not infer5% conditional-on-declaration error from an unconditional bound.
3. Distinguish unitary-only and measurement-inclusive circuit depth and preserve
   native oracle decomposition overhead. Synthetic acquisition costs are projected
   from measured circuit inventories, not actual device gate counts.

These are now explicit in code, analysis tests and protocol. Initial scientific
review independently ran49 circuit/comparator fixtures; final evidence review
will be recorded separately.

Heisenberg's independent software review found:

1. Nested files named complete.json escaped inventory because every basename
   was excluded. Only the root manifest is now excluded in input/run/analysis.
2. Recording the current library version did not enforce the protocol pin.
   Acquisition/replay now require Terra0.46.3 and the approved IQAE/Sampler
   source hashes. This is not a hash of every transitive site-package file.
3. csAE counts were available before project processing but not checkpointed.
   Native output is now immediately persisted before price/resource processing.

Source/input identities and copied producer bytes are rechecked before completion.
The explicit20-file runtime/protocol closure avoids treating unrelated historical
tests as producing dependencies. New producers have byte-preserving attributes.

Main integration additionally required checkpoint-error propagation, unknown
expense for failed native sampler jobs, enforced query-count reconciliation,
unique per-batch checkpoint filenames, deterministic transpilation, explicit
timings and actual native cap status. Worker implemented those changes and tests.

The first integrated focused pass:72tests passed,17upstream warnings,19.08s.
This is an iteration report, not yet the final frozen source receipt.

The final full-fixture analysis also caught a reporting-category collision:
policy names fixed_cp/fixed_target matched a substring intended for the fixed
comparison family. Exact category parsing fixed it before production. The final
prefreeze focused run passed72tests/17upstream warnings in21.94s; Ruff passed
after formatting. Producer/protocol frozen at76914458. No study output was used
to select a fix, method or threshold.

## Final evidence review

Production completed93tasks without failure; strict replay passed2022files and
all tasks. Full repository regression807passed in two disjoint invocations:
609journal tests/20warnings in165.62s and198other tests/9warnings in240.44s.
Receipts: tests_week14_full.xml (journal subset despite filename) and
tests_week14_other.xml. Clean source checkout1fbea8b6 passed72focused tests,
17warnings,23.06s and strict replay93tasks/2022files with the same existing
environment. Receipts: tests_week14_clean.xml and w14_clean_replay_v1.json.
No producer changes since freeze; Ruff and git whitespace checks pass.
Independent final reviewers
are Hegel (scientific) and Heisenberg (software/provenance), neither an author
of the producing implementation. Their initial scientific/software blockers
were cleared before acquisition. Human collaborator review remains pending.

### Hegel: final scientific evidence review ACCEPT

Independently checked task/file/byte/time totals, all resource-table entries,
point-estimator errors, allocation ties, native stopping observations, finite/
continuous offsets, noise-failure counts and uncertainty qualifications. No
numerical discrepancy. Three wording changes requested and applied:

1. Hull membership is weaker than membership in the original union of confidence
   components, not membership in every disconnected component.
2. Oracle construction enumerates payoffs; that makes direct finite summation
   available with minimal extra work, not a mandatory summation construction step.
   The finite numerical target is not a certified real-arithmetic enclosure.
3. Smaller tested delivery budgets are observed; minimum required effort is not
   established by the tested budget grid.

Reviewer rechecked all three corrections and returned ACCEPT for the declared
finite-target development scope, no remaining scientific reporting blocker.
Week15 NO-GO, lack of continuous certification/novelty/advantage and pending
human approval were explicitly retained. Reviewer did not edit files.

### Heisenberg: final software evidence review

ACCEPTED with no remaining implementation/archive blockers. Independently
verified producer hashes, archive inventory and receipts for807regression tests,
72clean-checkout tests and93task/2022file clean replay, zero failures/errors/skips.
No long tests rerun at this final receipt stage. Requested one final wording
correction: delivery is interval **half-width <=$1**, not full width <=$1.
Applied in the claim matrix; observed native full widths may exceed$1.
Acceptance covers bounded finite-target development only, not continuous-price
certification, confirmation, novelty or advantage. No producing code/evidence
changed during final reviews.
