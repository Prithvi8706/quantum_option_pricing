# Encoding-aware continuation: paid pilot and matched total budget

Date: 2026-09-15. Status: implemented and replay-verified method development.
No novel algorithm, hardware advantage or improved delivery over the strongest
fixed baseline was established. This experiment still uses the six European
regression contracts, NOT the [25 proposed harder problems](HARD_PRICING_25.md).

## What changed

The [previous planner](ENCODING_DECISION_RULE.md) calibrated every menu encoding
and used a worst-case Hoeffding certificate. The new modules are
`research/journal_sprint/allocation_rule.py` and `run_allocation.py`. Historical
modules and archives are unchanged.

First select an encoding before observing any data, using the design proxy

    cost_per_shot * S^2 / (tau-B)^2, for B<tau.

The implementation ranks log scores to avoid overflow. In this check shot cost
is 1 for both encodings, and the exact table is selected in all cases. This
removes unused-encoder calibration by design, not by pretending its readout is
identical or proving dominance under arbitrary encoder-specific noise. An
unfavorable preselection could be statistically valid but inefficient.

Then compare three prespecified arms under a 65536 TOTAL acquisition-shot cap:

| Arm | Acquisition and decision |
|---|---|
| fixed_cp | 16384 shots per calibration state; 32768 pricing; terminal calibrated CP inversion |
| pilot_cp | 1024 paid pilot shots; choose calibration/pricing split; acquire both fresh; terminal calibrated CP inversion |
| single_hoeffding | 16384 per calibration state; previous sufficient planner within remaining 32768 pricing shots; may refuse or finish early |

The main comparison is pilot_cp versus fixed_cp, which both spend exactly the
same total. The Hoeffding arm is a diagnostic and can spend less by refusing.

## Allocation is a forecast, not a certificate

After the pilot, rank m={1024,4096,8192,16384,24576} calibration shots per state;
the remaining pricing budget is n=65536-1024-2m. Compute projected CP widths from
the observed pilot rate and declared design readout f=.02,g=.07. Round expected
counts for those projections, explicitly stored as FORECASTS; they are never
reported as acquired observations. Choose smallest projected dollar radius,
tie by m. Execute even when the forecast is unfavorable.

All final calibration and pricing observations are fresh. No pilot observations
are pooled into validation. Actual terminal intervals, not forecasts, decide
whether dollar tolerance is met. The second readout scenario reverses f,g to
(.07,.02), checking a design-assumption mismatch while retaining stationarity.

This heuristic minimizes a forecast radius in a finite allocation menu, not true
expected cost or probability of successful delivery. It is not a proven optimal
allocation. It currently uses the full budget for CP even on extremely easy
contracts; reducing that over-allocation is a separate prospective design task.

## Conditional validity argument

The encoding is fixed before data. Condition on the paid pilot history: chosen
m and n are now fixed. The fresh calibration observations satisfy the specified
binomial model, so two CP intervals with noncoverage .025/2 each jointly cover
the two rates with probability at least .975. Expand by the supplied guard.
The fresh pricing sample yields a CP interval with noncoverage .025. The usual
calibrated inversion and dollar bias propagation then give at least .95 joint
containment by a union bound, conditional on any pilot history. Unconditioning
preserves the bound. No multiplicity correction over the five allocations is
needed because only one is executed with fresh data after selection.

This argument does NOT require the design readout assumption to equal actual
rates. It DOES require valid calibration-to-pricing transfer, the conditional
binomial model, correct bias bounds and no further data-dependent stopping.
The pilot can mislead efficiency without invalidating terminal coverage.

The probability of an erroneous dollar declaration is at most .05 per invocation
under these assumptions. This is neither conditional-on-declaration coverage nor
simultaneous coverage across 3240 rows or a post hoc choice among three methods.
CP, conditional sample splitting and the union bound are established techniques,
not novelty claims. Floating-point inversion is not a directed-rounding proof.

## All results, including the non-improvement

[Protocol](PROTOCOL_ALLOCATION_V1.md) was frozen before acquisition. Archive:
`results/journal_sprint/allocation_v1`. Six contracts x three guards x two
stationary readout scenarios x three arms x 30 independent repetitions = 3240
rows. Streams are new relative to previous experiments and independent across
arms; these are not paired encoding/allocation contrasts.

| Arm | Declarations / 1080 | Mean calibration shots | Mean pricing shots |
|---|---:|---:|---:|
| fixed_cp | 300 | 32768 | 32768 |
| pilot_cp | 300 | 31110.64 | 33401.36 |
| single_hoeffding | 180 | 32768 | 99.96 |

pilot_cp additionally spends 1024 pilot shots in EVERY trial. Its lower average
calibration cost does not lower the total: both CP arms use 65536 shots each.
The small Hoeffding pricing average includes 900 refusals; it is not the cost of
successful pricing across the suite. All observed interval misses and erroneous
declarations were zero; this is not proof of zero risk.

CP delivery patterns match cell-for-cell (observed, not proven equivalent):

- E001: 30/30 at every guard and both noise scenarios (180 per arm).
- E014: 30/30 only at zero guard in design_match (30 per arm).
- E025: 30/30 at design_match guards 0 and .003 and swapped guard 0 (90 per arm).
- E030, E038, E049: 0/30 in every cell.

Both CP arms recover the E014/E025 delivery that the conservative planner fails
to certify, but the strong fixed_cp baseline already does so. Thus the pilot
allocator did NOT create a new delivery improvement. Equal observed rates from
30 repetitions do not establish equivalence or superiority.

Pilot calibration allocations per state across its 1080 trials:

| m | Trials |
|---|---:|
| 1024 | 2 |
| 4096 | 35 |
| 8192 | 57 |
| 16384 | 982 |
| 24576 | 4 |

The heuristic chooses the baseline allocation in most cases while paying a pilot
overhead. For E001, design_match, guard zero, mean CP radii are .0407172 (fixed)
and .0458514 (pilot), both far below the $1 target. The single-encoding Hoeffding
arm uses mean total 33139.77 shots with mean radius .999349 there, versus the
old two-encoding planner's 65912.43 in the earlier experiment. This is a useful
accounting change on that easy problem, not a matched independent superiority
result or quantum-versus-classical advantage. The datasets and alpha splits differ.

## Checks and limits

18 focused tests passed before acquisition: proxy selection, allocation minimality
within forecast menu, total-cost identities, endpoint cases, invalid inputs,
reference CP corner inversion, pilot-free inference interface, and deterministic
runner fixtures. Ruff passed all three new Python/test files.

Replay regenerated all 3240 records, checked identical summary and shot accounting,
and verified 98 archived files plus input profile and live source hashes. Replay
uses the same implementation; independent corner-formula tests and a separate
accounting inspection provide additional checks, not external peer review.
Final full regression passed all 489 tests, zero failures/errors/skips, with
11 upstream warnings in 278.14 seconds (`tests_allocation_v1.xml`). Separate
PowerShell checks verified all shot/CX identities, equal primary-arm budgets
and declared radii. The [project log](PROJECT_LOG.md) records the full handoff.

The source archives are exclusive and unchanged. No experiment failed or was
retuned in this allocation stage. No hardware execution, new manuscript advantage
claim, author change, commit, push or PR occurred.

## Decision

Retain preselection and transparent cost accounting. Keep fixed_cp as the strong
baseline. Do not promote the pilot allocator as superior. A next allocation study
should optimize probability of meeting tolerance/expected cost instead of spending
the entire budget to minimize predicted radius. It requires a fresh protocol,
appropriate stopping validity, and matched-total-cost comparisons.

For a potential publication contribution, the higher-value next work is a strong
classical Asian/basket benchmark or a theorem-applicability/resource audit from
the 25-problem shortlist. More tuning of this six-contract k=0 experiment cannot
by itself demonstrate a quantum computational advantage.

Reproduce without overwriting an existing archive:

```powershell
venv\Scripts\python.exe -m research.journal_sprint.run_allocation --output results/journal_sprint/allocation_NEW
venv\Scripts\python.exe -m research.journal_sprint.run_allocation --output results/journal_sprint/allocation_NEW --verify
venv\Scripts\python.exe -m pytest research/journal_sprint/tests/test_allocation_rule.py -q
```
