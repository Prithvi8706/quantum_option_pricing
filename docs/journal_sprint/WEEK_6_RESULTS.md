# Week 6: transfer-position and calibration-cost discovery

Evidence availability: historical result, reading and test paths below refer to
the originating local workspace unless explicitly listed as included in the PR.
See [archive inputs and reconstruction](ARCHIVE_INPUTS.md) for the preserved
location, exclusions and configurable verification commands.

Protocol: [locally predeclared grid](PROTOCOL_W6_TRANSFER_GRID.md).
Discovery selected from week 5, not held-out confirmation or independently
timestamped preregistration. All numbers below are synthetic model outcomes.

## Complete accounting

324 cells of 100 attempts: **32400 attempts, 21600 acquisitions, 10800
pre-refusals**. E030/E038 were refused by unchanged sufficient representation
bounds, before observations or diagnostic targets. There were 2729 precision
declarations, 18871 unresolved acquisitions and no incompatible acquisitions.

Price containment was **21597/21600**, not perfect. Three intervals missed:
one E014 and two E049 trials, all CX-capped, 16384 calibration shots per state,
position 2 (df=-.02,dg=.03). All were unresolved, hence none was an erroneous
$1-precision declaration. Zero erroneous declarations were observed among
2729 declarations. This is neither zero error probability, simultaneous matrix
coverage nor a conditional-on-delivery 95% guarantee. Rates with no acquisitions
or declarations remain undefined, not artificially reported as successful zeros.

## E001: all nine positions, not just the favorable corner

Delivery counts out of 100 per cell. Calibration columns are shots **per state**.
Direct sampling delivered zero in every cell at both calibration budgets.

| Position | df | dg | A-matched 4096 | A-matched 16384 | CX-capped 4096 | CX-capped 16384 |
|---|---:|---:|---:|---:|---:|---:|
| 0 | -.02 | -.03 | 99 | 100 | 0 | 2 |
| 1 | -.02 | 0 | 100 | 100 | 52 | 68 |
| 2 | -.02 | .03 | 100 | 100 | 99 | 99 |
| 3 | 0 | -.03 | 100 | 100 | 7 | 20 |
| 4 | 0 | 0 | 100 | 100 | 5 | 12 |
| 5 | 0 | .03 | 100 | 100 | 72 | 83 |
| 6 | .03 | -.03 | 100 | 100 | 96 | 99 |
| 7 | .03 | 0 | 100 | 100 | 46 | 82 |
| 8 | .03 | .03 | 100 | 100 | 19 | 64 |

CX-capped delivery ranges from **0–99%** at 4096 and **2–99%** at 16384.
More calibration did not produce uniformly high delivery on this grid. Its
within-position high-minus-low differences were 2,16,0,13,7,11,3,36,45 percentage
points. These are descriptive differences from independent trials, not paired
estimates or multiplicity-adjusted significance claims.

Across these equally represented nine positions, CX-capped totals were 396/900
and 529/900 (44.0% and 58.78%). This chosen-grid average is not an expected
performance estimate for real hardware drift. A-matched totals were 899/900
and 900/900, but at a much larger pricing gate budget.

## Other contracts: calibration expansion does not broadly rescue delivery

E014 delivered once in 5400 acquisitions; E025 four times; E049 never.
All five declarations were A-matched: E014 had 1/900 at low calibration and
0/900 at high; E025 had 1/900 and 3/900, respectively. Direct and CX-capped
delivered none for those contracts. E030/E038 have no acquired-trial rate.
Do not describe week 6 as exclusively E001 delivery—the five rare declarations
must remain visible—but useful frequent delivery is still concentrated there.

Finite-budget non-delivery does not prove a universal precision floor. This
experiment varies calibration size, not pricing budget or guard width, so it
cannot isolate all sources of non-delivery or establish the best allocation.

## Costs and predefined comparisons

Per acquired trial, increasing calibration adds **24576 shots** (8192 to 32768
total calibration shots). Pricing schedules remain fixed: direct 294912 shots,
A-matched 32768 at each depth 0/1/2, CX-capped 2097 at each depth. Their total
pricing CX counts are 82575360, 1290141696 and 82563084, respectively.
A-matched uses about **15.62 times** direct's pricing CX. The maxima across
acquired contracts (also E001's depths) are 42728 for either multidepth arm
versus direct's 436. E014/E025/E049 instead use 42723 versus 435.
Calibration shots are
charged separately; these are not complete routed-device costs.

Complete matrix totals: 2876450400 pricing shots + 442368000 calibration shots
= **3318818400 represented shots**, 4382618400 pricing A-equivalents and
10478017008000 pricing logical CX gates. Binomial draws represent these counts;
billions of circuits were not physically executed. Run wall time was 29.43 s.

Machine-readable analysis includes all **162 calibration contrasts**, **216
multidepth-minus-direct contrasts** and **36 nine-position range summaries**.
Original 324 cells retain radii, full denominators, containment and costs;
original trial records retain every confidence-set component.

## Verification and disposition

`results/journal_sprint/week6_closeout_v1` checks 71 archive hashes and 66
planned dependency hashes against snapshots/live files; rederives all bounds,
refusals, diagnostic targets and designs; and reconstructs all 32400 unique
records and 324 cell summaries. Replay uses the producing trial/numerical
helpers, so it is a consistency check, not an independent implementation proof.
It deliberately rejects live-source drift: future replay requires matching the
archived code/dependencies in an isolated environment, not running arbitrary
updated helpers against old data. This is not a portable replay launcher.
Integrated regression: **304 passed, 11 legacy warnings, 189.06 seconds**.
Separate review disposition is recorded in the final closeout.

Decision: **no-go for adaptive promotion or confirmatory main matrix yet**.
The cheaper pricing-gate design is strongly position-sensitive; greater
calibration alone does not broadly rescue precision. Retain this as a bounded
reliability/resource result, not generic estimator novelty or classical advantage.
Next work must separate pricing-shot, calibration and stipulated-guard effects
and settle fair baseline scope before freezing a main experiment.

Evidence: `results/journal_sprint/week6_transfer_grid_v1` (raw data),
`results/journal_sprint/week6_closeout_v1/verification.json` (replay),
`results/journal_sprint/week6_closeout_v1/contrasts.json` (all declared contrasts).
