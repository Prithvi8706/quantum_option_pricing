# Claim assessment: frozen secondary-analysis protocol

Date: 2026-09-17. Base implementation: b8b8c7e2. Scope: user's four
claim-assessment tasks. This is retrospective analysis of the completed W2
evidence; neither new acquisition nor fresh confirmation. Candidate stays standby
until the assessment records an explicit disposition.

## Questions and fixed analysis

1. Classify primitive identities, application construction, correctness results,
   resource projections and empirical findings against nearest primary sources.
2. Prove a restricted normalization result over independent row probabilities
   t_i in [0,1], c_i >= 0, C=sum c_i, K>=0. Treat the zero function separately.
   Do not infer optimality on correlated basket support or gate optimality.
3. Prove the conditional continuous cost-proxy optimum for
   W(n)=g*beta*n^2/(e*n-a), n>a/e, with positive g,beta,e,a; identify assumptions
   that prevent transferring it to a general quantum advantage theorem.
4. Independently recompute the 32 existing production schedules and corrected
   integer composition costs. Use exact rational arithmetic and a Machin-formula
   enclosure for pi, without calling the production schedule/cost helpers.
5. Freeze the secondary sensitivity grid: dollar tolerances {0.5,1,2}, extra
   deterministic allowances {0,0.01,0.025,0.05,0.1,0.2}, all four cases, both
   encodings and degrees {16,32,64,128}. This produces 576 plan evaluations and
   72 case/tolerance/allowance comparisons. Confidence remains 95%, median
   repetitions17, M a power of two starting at2, A-call cap10,000,000.
6. An extra allowance is hypothetical additive price bias. It is not a native
   gate/noise bound and cannot stand in for accumulated execution error.
7. For each cell retain both families' best feasible plans, refusal reasons,
   corrected projected costs, exact baseline fixed-schedule margins and ties.
   Report all cases, including failures. No discovery-based grid expansion.

Inputs: production_v1/results.json, authoritative analysis_v2.json and tiny_v2/
results.json under results/journal_sprint/minimal_pivot_week2_*. Record hashes
before reading and use exclusive output directories. Archive new code/protocol
identities; preserve old producers and receipts. Reproduce the derived results in
the existing separate pinned environment. Tests must include failures at the
deterministic boundary, query caps, false cost-win inference and interval bounds.

## Decision and review

Advance the candidate to focused manuscript development only if its core claim
survives the assessment. Scientific confirmation and production admission stay
closed unless their separate requirements are met. A supported resource study
may warrant a narrow claim; publication-level novelty must not be inferred from
our implementation tests or from a restricted corollary of established theory.

Separate AI mathematical and literature reviews are requested. Neither counts
as human expert assessment. Do not contact external researchers without user
instructions. Prepare a concrete review brief for subsequent expert feedback.
