# Week 5 fixed-design delivery comparison

Discovery results under the [predeclared protocol](PROTOCOL_W5_FIXED_DISCOVERY.md).
Here, predeclared means local protocol and decision ordering before simulated
observations, not independently timestamped preregistration. Completion hashes
protect archived contents; they do not independently prove prospective commitment.
Not held-out confirmation, a native BAE/BIQAE comparison, a classical-pricing
comparison, or evidence of practical quantum advantage.

## Executed matrix

C6, n=6/c=.125, two reference budgets, two readout conditions, three fixed
designs, 100 repetitions: **7200 attempted design datasets**. E030/E038 are
pre-refused by the unchanged sufficient deterministic bound, producing
**4800 acquisitions and 2400 refusals**. Every acquired design pays for its own
4096-shot calibration of each state, with separate calibration/validation
streams. Direct sampling appears once, even though it supports two contrasts.

All designs use the same supplied .03 rate-transfer allowances and the same
.025 calibration / .025 validation failure allocation. Stationary f=.02,g=.07
and validation-transfer f=.05,g=.04 are both within those synthetic allowances.
The result is conditional on this stipulated model, not measured device drift.

## Useful $1 delivery is restricted to one contract

E001 delivery counts, out of 100 per cell:

| Reference A budget | Condition | Direct | A-matched multidepth | CX-capped multidepth |
|---|---|---:|---:|---:|
| 73728 | Stationary | 0 | 98 | 0 |
| 73728 | Constant transfer | 0 | 100 | 17 |
| 294912 | Stationary | 0 | 100 | 6 |
| 294912 | Constant transfer | 0 | 100 | 95 |

E014/E025/E049 deliver **0/100 in every executed design/condition/budget cell**.
E030/E038 remain refusals, not omitted successes or failed stochastic trials.
Every executed cell contains the price in 100/100 recorded intervals, with no
observed erroneous declarations. This does not prove zero risk, universal
coverage, or <=.05 error conditional on a declaration.

The two multidepth columns answer different cost questions. A-matched
multidepth pays roughly 15.6 times the direct pricing CX count at n=6; its
delivery cannot be presented as equal-gate superiority. CX-capped multidepth
uses 524/2097 shots per depth at the smaller/larger budget, respectively,
against direct's 73728/294912 shots. Integer slack is explicit in the ledger.

At the larger budget, E001's median dollar radii are approximately:

| Condition | Direct | A-matched | CX-capped |
|---|---:|---:|---:|
| Stationary | 2.206 | .817 | 1.136 |
| Constant transfer | 2.235 | .350 | .779 |

The direction/position of a response inside a supplied nuisance envelope can
change the intersection geometry. The transfer cell's better delivery is not
a claim that noise generally improves pricing. Both cells use the same broad
guard and different independent observations. A single favorable boundary
condition is insufficient for promotion; the next pilot tests that sensitivity.

## Cost and evidence

Actual synthetic acquisitions total **438828000 shots**, including 39321600
calibration shots and 399506400 pricing shots. Pricing alone represents
608695200 A-equivalents and 1455272265600 logical CX gates. These are arithmetic
resource counts represented by binomial draws, not that many executed circuits.
Calibration is counted separately; no routing/reset/measurement time or complete
hardware runtime is inferred from this logical cost axis.

The verifier checked all 67 run hashes, 7200 unique identities, 4800 calibration
and validation datasets, every interval/decision and all 72 cell summaries.
It also reconstructed the analytical bounds, diagnostic encoded amplitudes,
Black–Scholes prices, source-manifest lineage and fixed designs/cost ledgers.
It reuses producing numerical helpers and is not an independent proof.

Full regression passed: 287 tests, 11 legacy dependency warnings, 194.08 seconds.
After review, the verifier gained exact configuration and archived/live Python
identity checks. Its v2 reconstruction passed with unchanged results; 11 targeted
tests passed (six runner tests and five new configuration-mutation tests).
Bounded separate review requested with `gpt-6-astra` found no result-changing
bug and accepted the verifier fix. It inspected sources, hashes and aggregation,
not an independent numerical implementation or mathematical proof.
Macroscope remains unconnected; no PR was created.

## Decision

Do not promote an adaptive controller or freeze confirmation. There is a
limited fixed-design delivery signal for E001, but no broad useful precision
across C6, and the result is sensitive to the specified transfer condition.
The [next pilot draft](WEEK_6_PILOT_DRAFT.md) examines this dependence before
attempting resource selection. It is not an additional result or a frozen
confirmatory experiment.

Archives: `results/journal_sprint/week5_fixed_discovery_v1` and
`results/journal_sprint/week5_fixed_verify_v1`, with strengthened replay in
`results/journal_sprint/week5_fixed_verify_v2`.
