# Week-12 separate-agent review record

2026-09-16. Requested explicitly by the user. These are separate AI-agent code/
statistical reviews, not human peer review, collaborator sign-off or Macroscope.

## Pre-acquisition reviews

Statistical reviewer Dalton (`01a0a988-b31b-7c42-bd79-ef95ed39dc7a`) found no policy
validity blocker. Caveats: runner must enforce fresh samples; the historical CP
selection forecast differs from the shared delta diagnostic; unequal-full is not
a symmetry-only ablation; independently test positive-guard unequal endpoints.
Changes: separate selection forecast field, explicit attribution limits, and
independent binomial endpoint tests at guards 0/.003/.03. Actual runner behavior
receives the separate review below.

Software reviewer Carver (`01a0a98b-4260-7690-88e2-7e2f913a5da0`) blocked the first
runner draft before any observations. Findings and changes:

| Finding | Pre-acquisition correction |
|---|---|
| Failed attempts not reconciled | Read-only recovery audit, known consumed/in-flight resource accounting and failure-penalized started outcomes |
| Runtime projection trusted without semantic validation | Finite nonnegative times, aggregate consistency and exact projection recomputation |
| Incomplete source/config provenance accepted | Exact source-set identity, snapshot hashes, stage/cap/thread/config checks; always replay events/results |
| Unknown candidate bias aborts | Explicit candidate exclusion; remaining candidate considered, or zero-acquisition refusal |
| Historical forecast hidden | Original CP selection radius retained separately from delta diagnostic |
| Missing analysis denominators/uncertainty | Conditional/unconditional misses, success-conditioned cost and difference/ratio uncertainty summaries |
| Runtime reservation not enforced | Overall 7200-second main deadline covers gate/setup/acquisition/automatic replay; main retains intact pilot evidence |

Injected failures occur only inside temporary test fixtures. No actual campaign
has been launched at this review checkpoint. Follow-up review dispositions and
final evidence assessment will be appended after they occur.

## Follow-up findings before production acquisition

Dalton found an inclusive floating-point threshold defect: 380/400 minus 388/400
could compare below -.02. Fixed using integer counts and cost sums, with a boundary
regression. Dalton confirmed no remaining statistical blockers in a subsequent
read-only pass.

Carver found test isolation and persistence-boundary defects. Initial archive
fixtures sampled the first five pilot-v1 identities on actual C6 profiles; the
earlier blanket statement of no observations was too broad. No production archive,
primary or secondary acquisitions existed. Corrected all tests to fixture inputs
and TEST_ONLY namespaces, declared fresh production pilot-v2 before acquisition,
and documented this amendment without changing policy/thresholds.

Recovery now handles torn final events/raw rows with explicit incomplete-resource
flags, validates draw/plan/arm/count/budget invariants, and never appends diagnostics
to a potentially damaged event log. Separate best-effort failure artifacts retain
the original exception even if storage remains unavailable. Added end-to-end torn
append, raw-before-completion, interrupted-draw and invalid-contract fixtures.
Pilot/main input identity and final deadline checks were strengthened. The full
main+preserved-pilot path now has an isolated fixture replay test.

The pre-correction full suite (676 passing tests) ran while review revisions were
being developed and is retained as an iteration report, not the final frozen-source
gate. One earlier focused test failed because its injected pilot event used a fixed
arm; corrected the fixture to the intended paid arm, preserving strict validation.
Final focused/frozen-source full-suite results are recorded in the closeout.

Both reviewers completed follow-up static passes before production acquisition:
Dalton confirmed the statistical blocker resolved; Carver confirmed no remaining
acquisition blockers after the torn-tail exception-handler correction, conditional
on passing tests and the pilot runtime gate. Final focused suite: 104 passed in
27.17 seconds. A fresh full suite is required for the corrected source, separate
from the retained 676-test iteration report.
That corrected-source suite subsequently passed **684 tests**, with 11 legacy
Qiskit warnings, in 321.87 seconds. No production acquisition ran alongside it.
