# Week 11 closeout: contracts, classical baselines and quantum contribution gate

2026-09-15. Week-11 development work completed and locally verified. This means
the planned foundation/benchmark/design tasks have a recorded disposition, NOT
that a quantum advantage, new quantum algorithm or submission-ready paper exists.

## Deliverables and disposition

| Week-11 task | Completed work / scope |
|---|---|
| Evidence reconciliation | Existing weeks/rescue/allocation/shortlist results classified as development or diagnostics; no relabeling as confirmation; prior ties preserved |
| Error/resource interface | Opt-in `price_contract.py`; explicit target/currency/bias components, unknown-bound refusal, separate resource units and measured/projected evidence; 34 contract tests |
| Tolerances/confidence/held-out design | Cent-to-dollar research ladder, explicit approximate RQMC uncertainty, eight reserved candidate cases; no held-out acquisitions |
| Timing/memory pilot | 128 observations + four warmups; 132 rows/234 files replayed |
| Refined classical references | 384 independent estimates; all twelve SE diagnostics pass; 384 rows/490 files replayed |
| Full baseline comparison | 2304 observations + four warmups; 2308 rows/2415 files replayed; 144 summary cells independently checked |
| Prior-work distinction | Focused primary-source refresh and [quantum novelty checkpoint](WEEK_11_NOVELTY_MATRIX.md); novelty/advantage remain unestablished |
| Next-stage design/budget | [Week-12 development manifest](WEEK_12_DESIGN_MANIFEST.md): five arms including cost-aware fixed design, bounded runtime pilot and explicit criteria; no asymmetric trial run |
| Regression and artifact checks | 569 tests pass; Ruff passes; source/hash/event/denominator replay and local documentation checks |

Complete measurements and limitations: [WEEK_11_RESULTS.md](WEEK_11_RESULTS.md).
Historical first increment: [WEEK_11_WORKING.md](WEEK_11_WORKING.md).
Active forward scope: [weeks 11-16](WEEKS_11_16_IMPLEMENTATION_PLAN.md).

## Scientific outcome

Classical RQMC with control variates is already strong on these twelve Asian
baskets: at N=1024, observed single-deployment RMSE relative to refined numerical
references is .002082-.004084 dollars. Conditional integration lowers empirical
RMSE in all 36 matched contract/N cells but costs 5.29-9.01 times more standalone
time at the same N. This is not a matched-accuracy speedup or universal ranking.
Some high-resolution errors approach reference uncertainty. No measured quantum
experiment is part of these new results.

Decision: GO for bounded week-12 supporting-method development. NO-GO for
quantum-advantage, new-quantum-algorithm or submission claims. The user's intended
paper remains quantum-centered: a concrete encoding/preparation/AE resource result
must be established; a reliability-only alternative is not silently substituted.
The week-13/14 quantum feasibility and novelty gates remain necessary.

## Items deliberately carried forward

- Caller-supplied error bounds/composition assumptions still need actual proofs
  for each encoding. The contract schema cannot certify an unproved loader bound.
- Current Asian timing results use one machine and sampled, uncontrolled external
  load. No test/benchmark ran alongside acquisition, but there was light read-only
  inspection/document work. Larger performance claims require further validation.
- The eight held-out candidates remain reserved. A structured `assets=3` search
  over journal-sprint JSON/JSONL artifacts (excluding snapshots/environments)
  found no matches, and executed schedules/tests exclude those dimensions.
  This is not a universal audit of every historical schema/alias. Repeat the
  full exposure audit before the week-14 confirmation freeze; replace any
  contaminated case prospectively.
- The focused literature refresh does not establish priority. Faithful modern
  quantum comparators, state preparation, nonzero-depth AE and end-to-end quantum
  costs remain development work; no automatic novelty credit for known methods.
- The week-12 manifest's exact forecasting objective/fixed-design assumptions
  and implementation must be frozen and checked before new observations. Its
  pilot can trigger a disclosed prospective amendment if compute is infeasible.
- External human review, contributor approvals, journal choice/fees and submission
  remain later human-dependent readiness items. No such review/approval is claimed.

All old archives and unrelated dirty/untracked work were preserved. No paid jobs,
new authors, commits, pushes, PRs, merges or submissions were performed. The two
read-only PowerShell audit-command issues and pre-run lint correction are recorded
in the results note; no stochastic acquisition failed or was retuned/replaced.

Next: implement week 12's unequal-calibration/target-delivery policy and cost-aware
fixed comparator, prove/check the actual fresh-sample inference contract, then run
only its predeclared bounded runtime pilot before expanding the experiment.
