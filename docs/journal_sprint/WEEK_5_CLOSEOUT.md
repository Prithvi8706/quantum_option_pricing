# Week 5 closeout

Ongoing record: [project log](PROJECT_LOG.md), including week-6 work.

13 September 2026. The four planned local discovery work items are complete.
External review/publication gates are not complete. No commit, push, PR,
submission, paid hardware run or author-list change was made.

## Delivered

- Ten missing k=2 logical profiles, giving 30 combined circuit profiles.
- Forty fixed-cost comparisons separating A-equivalent and logical-CX budgets.
- Fixed discovery: 7200 attempts, 4800 acquisitions, 2400 pre-refusals;
  516 precision declarations and 4284 unresolved acquired datasets.
- Full record reconstruction, then a strengthened v2 replay checking exact
  declared configuration and archived/live Python identity. Results unchanged.
- A [week-6 pilot draft](WEEK_6_PILOT_DRAFT.md), selected from discovery findings,
  not yet executed or frozen as confirmation.

Only E001 delivered $1 precision. At the larger budget, CX-capped multidepth
delivered in 6/100 stationary and 95/100 transfer trials, versus direct's zero.
Other executed contracts delivered none. A-matched multidepth spends about
15.6 times the direct pricing CX count; it is not a gate-matched advantage.
See [full results and limitations](WEEK_5_FIXED_RESULTS.md).

## Checks and review disposition

The integrated suite passed 287 tests with 11 legacy dependency warnings in
194.08 seconds. Following the verifier-only fix, 11 targeted tests passed,
including five new configuration-mutation cases. The full suite was not rerun
after that fix. Ruff passes. Original experimental archives were preserved.

A separate reviewer requested with `gpt-6-astra` inspected sources, archive
hashes and aggregation. It found no result-changing interval/allocation bug.
Its configuration/source-identity finding was fixed and rechecked; 61 archived
Python files matched live sources. Its unsupported initial assertion that Astra
was unavailable was explicitly retracted. The reviewer did not independently
execute the full test suite or the numerical replay, and this is not proof.

The provenance finding is addressed by qualification: local protocol/decision
ordering is not independently timestamped preregistration. Completion hashes
alone cannot certify prospective commitment. Gate-cost and statistical claim
limitations remain explicit: observed containment is not universal coverage,
zero observed errors is not zero risk, and conditional-on-delivery coverage is
not established. Calibration costs are separate from pricing gate totals.

Macroscope remains unconnected and the PR remains held. Human contributor
work/author approvals, formal numerical guarantees, broader noise validity,
fair modern/classical comparisons and confirmatory validation remain open.

## Next

Week 6 should finalize the proposed transfer-position/calibration-size pilot
and its execution limits before acquiring observations. Do not promote an
adaptive controller or freeze confirmation from the current narrow signal.
Eleven scheduled weeks remain (6–16), plus the original reserve; this is not
an acceptance forecast.
