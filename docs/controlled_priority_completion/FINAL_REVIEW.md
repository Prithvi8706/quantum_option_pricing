# Independent technical review and resolution

22 September 2026. Three separate subagents reviewed components they did not
author. These are internal AI-agent reviews, not external human referees or
journal acceptance. No reviewer was used to independently approve its own
estimator, financial certificate or capacity calculation.

| Reviewed work | Author | Independent reviewer | Evidence |
|---|---|---|---|
| Wave scheduler and range-specialized multipliers | Root | Estimator agent | REVIEW_COMPILER.md; exhaustive primitive ranges and explicit wire/copy coloring |
| Structural ranges and joint arithmetic proof | Range agent | Estimator agent | REVIEW_COMPILER.md; coefficient, domain, clipping and policy-cancellation review |
| Hadamard and bounded-QAE guarantees | Estimator agent | Physical/capacity agent | REVIEW_ESTIMATORS.md; exact tails, interval phases, direct finite-unitary checks |
| Fixed-work/factory capacity and noise assumptions | Physical/capacity agent | Range agent | REVIEW_CAPACITY.md; independent 360-coordinate and six-row reconciliation |
| Combined resource ledger, composed replay and paper claims | Root | Physical/capacity agent | REVIEW_INTEGRATION.md; independent counts and preserved 95-rotation certificate replay |
| New composed wrapper bindings | Estimator agent, after review request | Root | Address ranges, source/phase offsets, three-phase synthesis convention, controller/allocation and IQFT correspondence inspected; focused tests |

## Findings resolved

- The arithmetic reviewer requested executable assertions for exponential
  domains, range-reduction constants, digital normal first moments, and forward
  and policy caps. The financial author added them and regenerated the bound.
- The capacity author had retained obsolete QPE workspace in Hadamard rows.
  It was replaced with the single-control allocation, removing 21/23 redundant
  logical bits. This was an overcount; the result did not change the gate.
- The initial estimator test run used pytest from the user site. The whole
  research suite was rerun in the isolated pinned environment with user-site
  loading disabled. No claim of isolation is based on the older run.
- A resource composition alone did not bind the new schedules to estimator
  wires. New Hadamard/bounded wrappers now reference the actual range sources,
  wave schedules, classical controls, powers and synthesized rotation library.
- The composed replay originally exercised normalizer 16 for both models. It
  now uses the selected first-stage target and normalizers 16/64 for C4/H8.
  Both new complete financial/phase and selector inverse checks passed.
- The paper's temporary bibliography placeholder and indirect arithmetic
  status were replaced with the verified title and the actual reviewed bounds.
- Prose in the combined JSON was regenerated to agree with its generator;
  numerical resources were unchanged. The integration receipt was refreshed
  after replay changes.
- The final classical decoder now encloses each amplitude and the median with
  interval arithmetic, pays binary64 output rounding, and verifies the total
  still fits its allocated error. Hadamard decoding also includes center
  rounding in its reported radius. Endpoint and asymmetric-median tests pass.
- Estimator generation no longer requires the ignored local paper cache; it
  records a reading hash when available. The PDF renderer preserves literal
  multiplication symbols in formulas rather than parsing them as emphasis.

No correctness blocker remains for the claims as scoped in CLAIM_LEDGER.md.
This does not close the same-policy baseline/regret or physical-price obligations.
The reviews explicitly reject promoting a digital certificate, query theorem,
bare capacity pass or circuit improvement to a significant advantage result.

## Scientific and publication decision

The studied implementation has not achieved the original acceptance criterion.
The general impossibility of quantum advantage is also not established. The
new bare Hadamard capacity pass must remain visible alongside the failed
constructed schedules and restricted encoded/factory scenarios.

The companion paper is a concrete benchmark/feasibility draft. It is not an
advantage paper, a certified novel algorithm or a guaranteed journal acceptance.
Submission remains dependent on missing author facts, truthful attestations and
human approval. The original manuscript and historical evidence are preserved.
