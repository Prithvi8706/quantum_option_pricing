# Independent AI review and verification record

Scope: bounded matched arithmetic study, 2026-09-17. AI reviews are not human
expert novelty assessment or external peer review. No collaborator is credited
with work performed by an agent. The implementation workers and final reviewers
are separate agents.

## Design and mathematical review: Huygens

Agent `01a0aeba-332a-7a00-844f-15ed921a091b` independently inspected the existing
arithmetic and relevant primary-paper passages. Recommended fixes implemented
before the frozen acquisition:

- Use the same integer payoff in both arithmetic routes; connect reflection
  to the same real financial target through its distinct error bound.
- Use a zero-start copy plus efficient modular ripple addition, and a
  Hadamard-initialized Fourier sum. Uncompute the actual shortened circuit.
- Add a universal signed post-strike bound; separate operand bounds alone
  do not guarantee that subtraction cannot wrap.
- Report standard control cancellation for every route as a secondary ledger.
- Declare the arithmetic decoder scale and check that its interval bridge and
  multiplication rounding fit the decoding allowance. Both market cases pass
  the new regression test; no favorable budget adjustment was needed.

Reviewer independently verified the archived reflection producer's eight
artifacts and175 sources, its linked inputs, the scope of the decoder bridge,
and the full-pricing accounting. Conditional mathematical approval to acquire
was given before the frozen run; final evidence review is recorded below when
complete.

## Implementation/evidence review: Locke

Agent `01a0aec3-6912-70d3-90a0-70e7f77a0e50` independently read the new modules
and ran88 focused tests. Found no concrete circuit/composition defect but raised
two evidence blockers: the initial verifier accepted a rehashed archive with
duplicate reflection rows and missing arithmetic, and it accepted empty source
and input manifests.

Before acquisition, the verifier was strengthened to require the exact frozen
commit's source inventory, separate mandatory input inventory, exact file/menu
structure, finite diagnostic recomputation, fresh emission/checking of arithmetic
components, compiled aggregation, reconstructed budgets/resources/qubits, and
the actual minimizing choices. The source archive hash is byte-exact. Its
separate comparison to the Git commit allows only historical CRLF/LF conversion;
old hashed producers were not rewritten. New producer bytes are Git-preserved.

Mutation regressions cover duplicate routes, missing budget/components, a
fabricated winner, false width, production promotion, absent finite diagnostics,
empty provenance, artifact tampering and extra/unsafe manifest entries.

## Reproducibility boundaries

The protocol is bounded development, not blinded preregistration. Historical
reflection results, scalar-precision preflight and implementation-worker endpoint
checks were known before the final acquisition. The fixed q/width/degree/menu
were not tuned after matched pricing-cost outcomes. All acquisition code and
protocol were committed at `68e78e3f` before the two recorded runs.

The normal environment and isolated pinned research environment acquire separate
exclusive directories. Verification re-emits the components rather than trusting
supplied cost fields. Reconstruction is cached only within one verifier process
to avoid rerunning identical first/replay components. It shares tested producer
primitives: this is deterministic reconstruction, not a separately invented
arithmetic implementation or a proof assistant certificate.

## Completed verification receipts

- [Acquisition/replay verifier](../../results/journal_sprint/matched_arithmetic_verification_v1.json):
  passed both archives;12 rows and188 source hashes each, mandatory inventories,
  fresh gate/component reconstruction, budgets/choices and exact replay.
- [Isolated focused suite](../../results/journal_sprint/matched_arithmetic_isolated_tests_v1.xml):
 103 tests passed,17 legacy dependency warnings. Includes the mutation regressions.
- [Prior claim-assessment replay](../../results/journal_sprint/matched_prior_claim_verification_v1.json):
  passed; earlier source/evidence unchanged.
- [Prior W2 integrity/replay](../../results/journal_sprint/matched_prior_w2_verification_v1.json):
  passed all final source/archive hashes, exact replays and32 decisions.
- Ruff F checks passed for all14 changed/new Python files across both the claim
  assessment and comparator work. Git whitespace checks passed.

Final result-review dispositions, integrated-suite total, clean-checkout checks
and merge status will be appended after they finish. No final approval is
implied by this interim receipt list.
