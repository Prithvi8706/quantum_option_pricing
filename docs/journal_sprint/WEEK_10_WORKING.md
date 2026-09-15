# Week 10: evidence gate in progress

Started 2026-09-14 on `research/week10-evidence-gate`, from merged main
`77fd5ec14035094e74f941319560f8a5ab7cc4c0`. Historical archives remain unchanged.
This preserves the starting assessment. The subsequent
[week-10 closeout](WEEK_10_CLOSEOUT.md) supersedes its pending-work status;
neither document is a frozen confirmation protocol.

## Methods comparison completed for the screened basket paper

Read the primary HTML methods (III-A through III-F) and results/conclusion
(IV-V), not just the abstract, of
[Kashif et al., arXiv:2509.09432v1](https://arxiv.org/html/2509.09432v1).
No source-code reproduction or figure-image audit has been performed.

Source observations: III-B uses independent asset distributions and basket
binning. III-C describes state preparation and approximate payoff encoding.
III-E includes binned summation and Monte Carlo. These overlap with our
representation and accuracy/resource questions. IV explicitly switches to final
basket values rather than option payoffs. III-B's independence footnote and
V's correlated-model wording also require clarification before reproduction.
The inspected methods do not specify our finite readout-calibration rectangle,
transfer allowance, all-branch set intersection and dollar-declaration audit.
This bounded comparison does not establish priority over the wider literature.

Our mathematical check, independent of their implementation: for a basket
equal to 80 or 120 with equal probability and strike 100, the expected call
payoff is 10, whereas applying the payoff to its expected basket value gives
0 (before discounting). Thus expected basket agreement cannot by itself verify
option-price agreement. This is a target-matching requirement, not evidence
that our estimator outperforms theirs.

## Matched-comparison design direction (not frozen)

Use a fixed, already studied single-asset representation first, without
claiming a multi-asset extension. All arms must estimate the same discounted
expected payoff under the same probability measure, support and encoding.
Record the encoded target separately from the continuous price and its
deterministic allowance B. Exact summation is an evaluation reference and a
reported classical competitor, not information available to a controller.

Candidate arms are native IQAE and direct classical sampling of the same
bounded encoded payoff. Fix a $1 continuous-price tolerance and total failure
allowance 0.05 before running; map remaining tolerance through S and B.
Refuse when B alone precludes delivery. A fixed-sample bounded-variable
confidence bound can give the classical arm an explicit frequentist allowance;
do not substitute an unvalidated normal interval. Native stopping guarantees
must be checked against its implementation and noise assumptions first.
Start noiseless: this does not validate the readout-transfer model. Bayesian
arms require a separate interpretation of posterior uncertainty.

Report setup, distribution construction, classical payoff evaluations, exact
summation cost, quantum shots, A-equivalent calls, logical CX, calibration,
pilot, failures and elapsed simulation time separately. Do not equate a
classical sample to a CX gate or simulator runtime to hardware runtime.
Contract list, seeds, budgets and replication count remain to be frozen;
this document does not authorize a confirmation campaign.

## Numerical gate as planned at the start

Before stress execution, save an exact case table covering disconnected final
sets, branch critical points, extreme counts and large shot counts. Validate
the independent beta-tail strategy against analytic boundaries, small-count
reference results and higher precision. Preserve timeout/convergence failures;
never silently drop difficult cases or alter the original week-9 protocol.
Compare whole reference components with production components, without extra
comparison tolerance. Even a passing finite matrix is not formal certification.

## Provisional scientific decision at the start

Continue as a reliability-methods candidate, not an advantage or successful
controller paper. The comparison sharpens the target audit but is not a new
estimator or sufficient novelty evidence. Week 10 remains open until numerical
stress implementation/execution, comparator feasibility checks and an explicit
go/no-go decision are logged. No new experimental result, reviewer approval,
submission readiness or authorship approval is claimed here.
