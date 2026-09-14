# Week 7 results: pricing, calibration and valid transfer-guard ablation

Discovery under the [local prospective protocol](PROTOCOL_W7_ABLATION.md).
This is not confirmation, a real-device experiment, or a generic estimator win.

## Complete acquisition and inference accounting

**21600 acquisition attempts** across 216 cells: 14400 acquired datasets and
7200 pre-refusals (E030/E038). Each acquired dataset has one calibration draw
and one pricing draw. Valid guard arms reuse those observations, so the
**43200 arm attempts** contain 28800 executed inferences and 14400 refused
arms. Arms are not independent datasets and do not multiply acquisition cost.

There were **5042 arm-level precision declarations, 23758 unresolved inferences,
and no incompatible inferences**. E001 accounts for 5034 declarations; E025
eight; E014/E049 zero. These arm totals are not counts of distinct successful
acquisitions. Refused contracts remain visible in both attempt denominators.

Price containment: **28791/28800 executed arms**. Nine misses are preserved in
`week7_closeout_v1/containment_misses.json`. Three E001 misses were precision
declarations, but all three midpoint errors remained <=$1. The other six misses
were unresolved. Thus there were zero **erroneous $1 declarations**, not zero
interval noncontainment. Do not confuse the returned interval's radius with
the user tolerance when defining these events. No zero-risk, simultaneous-arm,
or conditional-on-delivery coverage conclusion follows from these frequencies.

## Increasing pricing shots helps E001 under the broad guard

CX-capped E001 delivery, out of 100 per cell, guard=.03 throughout:

| Reference A budget | Calibration per state | Stationary | Small transfer | Boundary transfer |
|---:|---:|---:|---:|---:|
| 294912 | 4096 | 5 | 6 | 95 |
| 294912 | 16384 | 12 | 18 | 99 |
| 1179648 | 4096 | 96 | 100 | 100 |
| 1179648 | 16384 | 100 | 100 | 100 |

Direct sampling delivered zero in every corresponding broad-guard cell;
A-matched delivered 100 in each. A-matched spends about 15.62 times the direct
pricing CX count, so its success is not equal-gate superiority.

At fixed calibration, pricing-budget increases are independent-acquisition
descriptive contrasts, not paired draws. The large improvements for E001 do
not generalize to all bound-feasible contracts. E025's eight declarations all
occurred at the larger budget under A-matched; E014/E049 still had none across
all guard arms, even the stationary zero-transfer arm. This is not proof of a
universal precision floor or failure of every possible representation/schedule.

## Guard uncertainty is distinct from simulated drift

Under **the same stationary observations**, direct E001 delivery was:

| Budget | Calibration per state | Guard 0 | Guard .01 | Guard .03 |
|---:|---:|---:|---:|---:|
| 294912 | 4096 | 100 | 0 | 0 |
| 294912 | 16384 | 100 | 3 | 0 |
| 1179648 | 4096 | 100 | 0 | 0 |
| 1179648 | 16384 | 100 | 100 | 0 |

Guard zero here means stipulated zero transfer, **not known exact readout**:
finite calibration uncertainty is still propagated. It cannot be selected for
hardware merely because it gives better delivery. Narrower guard arms were
never applied to a condition whose declared transfer they do not cover.

All **19200 paired component-enclosure checks** passed: widening a valid guard
enclosed the narrower amplitude set (within the declared numerical comparison
padding). This is a useful implementation check, not floating-point certification.
Guard contrasts are paired analyses on shared data; pricing/calibration/design
contrasts use separate draws. There is no causal claim that drift improves pricing.

## Cost accounting

Across unique acquisitions: 4794091200 pricing shots + 294912000 calibration
shots = **5089003200 represented shots**. Pricing A-equivalents: 7304385600;
pricing logical CX: 17463456172800. These are represented by synthetic binomial
draws, not billions of physically executed circuits. Run elapsed 34.48 seconds;
bound/design setup measured separately at approximately .04466 seconds.

At larger reference budget, direct uses 1179648 pricing shots and 330301440
pricing CX. CX-capped uses **8389 shots per depth**, 25167 pricing shots and
330291708 CX (9732 gate slack). It is not exactly four times the smaller integer
allocation. A-matched uses 131072 shots per depth and 5160566784 pricing CX.
Increasing calibration costs 24576 additional shots per acquired trial, not
per inference arm. Logical gate costs omit routing and full-device overhead.

## Predeclared analysis and readiness decision

All **1008 contrasts** are archived: 216 pricing, 216 calibration, 288 design
and 288 paired guard contrasts. Missing acquisition/declaration denominators
remain null; no favorable cells were silently dropped.

The screen required a single fixed CX-capped budget/calibration candidate to
deliver >=90/100 and beat direct by >=10 percentage points in each of 12
contract/condition cells (four feasible contracts, three conditions), at guard
.03. **All four candidates failed.** The two smaller-budget candidates passed
only 1/12 cells each; larger-budget candidates passed 3/12 each, all E001.
This engineering screen was declared before these data; it is not a significance
test or a guarantee about population reliability.

**Decision: no adaptive-policy promotion and no confirmatory main matrix.**
E001's signal merits a bounded statement about sensitivity to costs/assumptions,
not a broad pricing advantage. The [native comparator audit](WEEK_7_COMPARATOR_SCOPE.md)
also rules out a native BAE/BIQAE calibrated-transfer superiority claim using the
current adapters. Further method/claim work must precede that comparison.

## Verification

`results/journal_sprint/week7_closeout_v1` verifies 77 archive hashes and 71
planned dependency hashes, rederives bounds/designs/targets, replays all 21600
records, reconstructs 216 cell summaries and checks guard nesting. It reuses
producing helpers and rejects live-source drift; it is not independent proof
or a portable archived-environment launcher. Original archives are unchanged.
Final tests and review disposition are recorded in [week-7 closeout](WEEK_7_CLOSEOUT.md).
