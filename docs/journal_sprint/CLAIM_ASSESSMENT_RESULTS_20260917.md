# Claim assessment and next-stage decision

Date: 2026-09-17. This work addresses checklist section5A. Scope and analysis
were fixed in [the secondary-analysis protocol](CLAIM_ASSESSMENT_PROTOCOL_20260917.md).

## Supported claim

For a specified separable lognormal basket, we implement a shared-reflection
signal with sharp normalization on the enclosing independent probability cube,
directed logical-error accounting, and encoding/degree selection over a finite
menu. Reproducible component counts and composition projections demonstrate
normalization-versus-circuit-cost tradeoffs, including a reversal of the selected
encoding as the statistical schedule changes.

This is the current defensible *technical statement*. Its originality and
sufficiency for publication remain to be established. The reflection/LCU
identities, normalization lower bound and continuous cost-proxy optimization
are standard tools/corollaries; packaging them as theorems does not create a new
quantum primitive. See [proofs and limitations](CLAIM_THEOREMS_20260917.md).

## New completed analysis

The new analyzer uses exact rational arithmetic, an alternating-series Machin
enclosure of pi, and its own schedule/cost formulas. It reproduces all32
production schedule decisions and the authoritative corrected selected costs.
It shares the archived inputs and AE theorem, but does not call the old
schedule/selection/cost helpers. This is independent implementation of the
secondary calculation, not independent experiment acquisition.
Archived deterministic budgets and component costs remain inputs; this analysis
does not independently recertify their derivation. Tiny fixed-schedule counts
are copied from the hashed original archive rather than newly compiled here.

Frozen sensitivity grid: tolerances $0.50/$1/$2, six hypothetical additional
price-bias allowances from $0 to $0.20, four existing cases, two encodings and
four degrees. All576 plan evaluations and72 comparisons are retained:

| Outcome | Cells |
| --- | ---: |
| Both feasible; reflection has lower composition projection | 38 |
| Reflection feasible; original refused | 9 |
| Both feasible; original has lower composition projection | 1 |
| Neither feasible | 24 |

These are correlated, retrospective grid cells over four existing contracts.
They are not independent trials, success probabilities, confidence intervals or
evidence of generalized performance. The extra allowance is hypothetical price
bias; it does not certify any native execution/noise model.

### A concrete reversal, and why selection is necessary

For E2 at $2 tolerance, both degree128 plans are feasible:

| Extra bias allowance | Original M | Reflection M | Original projected CX | Reflection projected CX |
| --- | ---: | ---: | ---: | ---: |
| $0 | 1024 | 512 | 10,620,373,592,188 | 10,555,082,898,967 |
| $0.05 | 1024 | 1024 | 10,620,373,592,188 | 21,129,742,845,308 |
| $0.10 | 2048 | 1024 | 21,250,586,670,544 | 21,129,742,845,308 |

At $0.05, the reflection schedule doubles its M before the original schedule
does. Its higher per-call composition cost then makes the original almost
twice as cheap under this model. At $0.10 the original schedule also doubles,
reversing the ranking again. Smaller normalization alone is therefore an
insufficient selection rule. The common $1/no-extra-allowance results remain
unchanged: ratios4.0318/2.0139/4.0195 in D1/D2/E1, E2 refused.

At $0.50/no-extra-allowance, only D1 reflection meets the menu. At
$2/no-extra-allowance, D2/E1/E2 reflection savings shrink to around1%, rather
than the headline2–4x seen at $1 in other cases. The result supports retaining
both encodings and the discrete cost-to-accuracy decision; it does not establish
the best algorithm outside this menu.
Feasibility/refusal here is limited to the fixed menu, conservative bounds and
caps; it is not a proof of possibility or impossibility for an entire family.

## Independent AI review and implementation issue

Two separate AI reviewers assessed mathematics and primary-literature overlap.
Their assessment is recorded in [the review note](CLAIM_ASSESSMENT_REVIEW_20260917.md).
This is not independent human expert signoff.

The mathematical review found a constant-sign endpoint defect in the frozen
constructor: a negative interval touching zero could be assigned a positive
sign. A versioned corrected class and regression tests were added. Its correction
is available for new experiments; the old experiment producers are preserved.
The four production contracts have strictly positive centered constants
(approximately25.84,123.15,139.77,392.86), so this endpoint case does not explain
or alter the archived comparisons. No exceeded total operator bound was shown.

## Novelty gap that matters next

The [updated prior-art assessment](CLAIM_PRIOR_ART_20260917.md) identifies a
July2026 author-uploaded Fourier-arithmetic payoff-oracle preprint and a related
Asian-payoff arithmetic construction by Wang/Kan as missing external comparisons.
The KL Asian-pricing paper also has a running-average alternative beyond its
nested-estimation construction. Internal original/subset-centered baselines
alone do not establish competitiveness with these routes.

## Decision

**GO for one bounded external arithmetic-comparator study.** Keep the candidate
on standby for confirmation, production and manuscript promotion. Retain an
ideal-logical resource/error contribution as the working claim to evaluate.
This explicitly chooses the bounded-experiment branch of checklist5A; it does
not approve a new financial target or automatically abandon the user's desired
quantum-over-classical advantage. That advantage remains unestablished.

The next study must compare the same factor distribution and payoff under a
common error/resource model, charging conversion to price registers, efficient
conventional versus Fourier aggregation, payoff loading, uncomputation and AE.
The concrete comparison scope is in the prior-art note. If this yields no
distinct useful result and expert review finds no novelty, record that outcome
and reconsider the paper scope rather than label the current package ready.

## Status of the four requested items

- Human expert novelty assessment: **open**. Targeted primary-source audit,
  separate AI assessment and an unsent expert review brief are complete.
- Defensible technical result: **documented and tested** in the restricted scope
  above. Publication-level originality remains provisional.
- Advance/experiment/scope decision: **complete**. Choose the bounded external
  comparator study; candidate remains standby.
- Matched quantum-over-classical advantage: **not established**. Existing
  classical intervals are approximate and physical execution costs unknown.

Evidence directories: `results/journal_sprint/claim_assessment_v1` and
`claim_assessment_replay_v1`; verification receipt
`claim_assessment_verification_v1.json`. Both environments produce byte-identical
results and input records. Original W1/W2 integrity verifiers continue to pass.
No new confirmation observations or hardware executions were acquired.
