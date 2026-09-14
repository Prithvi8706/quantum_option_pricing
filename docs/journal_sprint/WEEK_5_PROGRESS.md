# Week 5 progress: measured fixed-design costs

Latest: the [fixed-design comparison](WEEK_5_FIXED_RESULTS.md) is now executed
and reconstructed, with the [next pilot drafted](WEEK_6_PILOT_DRAFT.md).
Integrated tests and bounded Astra-requested review are complete; see the
[closeout](WEEK_5_CLOSEOUT.md). Macroscope/PR remain held. The resource
milestone narrative below records its earlier state, not current execution status.

13 September 2026. Week 5 started; first resource/ledger milestone complete.
The fixed-design response experiment is declared but has not been executed.
See [week-5 plan](WEEK_5_PLAN.md) and
[prospective comparison protocol](PROTOCOL_W5_FIXED_DISCOVERY.md).

## Missing circuit profiles completed

All ten n=5/6, k=2 circuits passed the 1e-9 ideal-response check; maximum
discrepancy was 6.94e-14. The resource run took 107.45 seconds. n=5 uses 7186
CX gates at k=2; n=6 uses 25968. Combined with the archived k=0/1 profiles,
there are 30 profiles and 40 two-axis fixed-cost comparisons.

These are all-to-all logical circuits at optimization level zero, not routed
hardware counts or a runtime forecast. Their large reflection costs are specific
to this construction/compilation; do not claim an unavoidable lower bound for
all amplitude-estimation circuits.

## Equal queries do not mean equal gates

For E001/n6/c=.125 at reference budget 294912 A-equivalents:

| Fixed design | Shots by depth | Pricing A-equivalents | Pricing CX gates |
|---|---|---:|---:|
| Direct, k=0 | 294912 | 294912 | 82575360 |
| A-matched, k=0/1/2 | 32768 each | 294912 | 1290141696 |
| CX-capped, k=0/1/2 | 2097 each | 18873 | 82563084 |

The A-matched multidepth schedule uses about **15.6 times** as many CX gates as
direct. At the direct schedule's CX cap, only 2097 shots per multidepth circuit
fit, with 12276 CX units unused due to integer rounding. Every design separately
budgets 8192 calibration shots. Calibration is not included in pricing gate
totals; the ledger also retains u-gate counts, qubits, depth and total shots.
Neither budget axis is a full physical-cost model.

## Checks and remaining work

117 sprint tests passed, 11 legacy warnings, 15.80 seconds. Ruff and tracked
whitespace checks pass. This is not a rerun of the full repository suite;
week 4's 271-test result remains historical. New tests retain the original
week-3 matrix and check allocation/cost arithmetic and invalid input handling.
Source archives are hash-checked when building the ledger; producing ledger
code is snapshotted. A separate check loaded all 30 QPY circuits and verified
their gate counts, circuit depths and qubit counts against the saved records.

Next: implement the declared 7200-attempt comparison with direct, query-matched
multidepth and CX-capped multidepth, preserving all refusals and independent
calibration costs. No fixed-design delivery winner is established by this ledger.
Adaptive promotion and held-out confirmation remain off. The earlier Astra
review does not cover this new milestone; Macroscope and the PR remain pending.

Archives: `results/journal_sprint/week5_resources_v1` and
`results/journal_sprint/week5_fixed_costs_v1`.
