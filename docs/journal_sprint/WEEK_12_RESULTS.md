# Week 12 results: no incremental target-policy benefit established

2026-09-16. Synthetic development study, not hardware execution or confirmation.
Producing source freeze `9a97228a`; protocols were fixed before production draws.
The [review record](WEEK_12_REVIEW.md) documents the pilot-v1 test exposure and
prospective pilot-v2 correction. No primary/secondary production namespace was
used in those fixtures. Policy and thresholds were not tuned on study outcomes.

## Acquisition and verification

- Runtime pilot-v2: 90/90 rows, 1.739s acquisition; projection 1244.864s <7200s.
  Strict replay: 90 rows/205 files; independent audit: 30 cells.
- Main: 7400/7400 rows (2000 primary, 5400 secondary), 150.700s acquisition.
  Full gate/setup/acquisition/automatic-replay workflow: 297.210s.
- Strict numerical/event/source replay: 7400 rows/7721 files; original manifests
  unchanged. Timings are not reproduced. Independent stdlib audit checked all
  185 cells, threshold arithmetic and aggregate draw/resource totals.
- Main resources: 413,220,864 simulated shots; 31,338,155,520 modeled logical CX.
  Every planned trial started/completed; zero unattempted or unresolved draws,
  no torn event tails or production exceptions. Statistical no-declaration
  outcomes are not erased as execution failures.
- Pre-acquisition regression: 684 passed, 11 legacy Qiskit warnings, 321.87s.
  Focused final tests: 104 passed. The existing Windows/Python environment was
  reused, not installed afresh. Optional PyYAML warning affects NumPy's metadata
  formatting, not numerical acquisition; no dependency change was made mid-study.

Archived receipts are `w12_runtime_pilot_receipt_v2.json`,
`w12_runtime_pilot_verification_v2.json`, and `w12_development_receipt_v1.json`
under `results/journal_sprint`. Main's nested pilot evidence is an immutable copy,
not another 90 observations. Execution times are local workflow measurements,
not physical-quantum runtime or a speedup comparison.

## Primary case: E001, design readout, guard zero

Each arm has 400 independent trials. Cost columns include all pilot/calibration/
pricing samples. Failed delivery costs 65536 in the penalty column, regardless
of actual consumed shots.

| Arm | Delivery | Mean actual shots | Mean penalized shots | Interval misses | Erroneous $1 declarations |
|---|---:|---:|---:|---:|---:|
| Fixed full-budget CP | 400/400 | 65536 | 65536 | 0 | 0 |
| Historical equal-pilot CP | 399/400 | 65536 | 65536 | 0 | 0 |
| Unequal full-budget | 400/400 | 65536 | 65536 | 0 | 0 |
| Unequal target-cost | 400/400 | 8192 | 8192 | 1 | 0 |
| Cost-aware fixed target | 400/400 | 8192 | 8192 | 0 | 0 |

Target-cost reduces observed penalized cost by 87.5% versus the full-budget fixed
arm, but **0% versus cost-aware fixed target**. Both required comparisons must
reach 15% reduction, so the predeclared interest gate **FAILS**. This is not an
incremental adaptive-policy win. Both target arms hit the lowest declared cap;
this experiment does not determine behavior below that cap and it is not amended
after seeing the tie. The historical equal-pilot arm returned one empty interval;
the target arm's one noncontaining interval still had midpoint error below $1.
Containment failure and erroneous tolerance declaration are different outcomes.

Pointwise 95% CP delivery interval for 400/400 is [0.990820,1]; for 399/400 it is
[0.986150,0.999937]. Zero erroneous declarations in 400 trials has upper CP bound
0.009180, not zero risk. The target's interval-miss rate 1/400 has interval
[0.0000633,0.013850]. Conservative target-minus-fixed delivery intervals are
[-0.010895,0.010895] for each fixed comparator, individually, not simultaneously.

Raw analysis retains approximate t/delta cost intervals. On the primary case
these collapse because observed costs/penalties have zero sample variance. They
are **not exact uncertainty bounds on future expected penalized costs**, and
must not be interpreted as certain 87.5% improvement or a proven true tie.
The observed comparison and the failed development gate are the supported claims.

## Secondary matrix: exploratory, not pooled confirmation

Each arm has 1080 trials across 36 contract/readout/guard cells (30 per cell).

| Arm | Deliveries /1080 | Mean actual shots | Mean penalized shots |
|---|---:|---:|---:|
| Fixed full-budget CP | 300 | 65536 | 65536 |
| Historical equal-pilot CP | 300 | 65536 | 65536 |
| Unequal full-budget | 300 | 65536 | 65536 |
| Unequal target-cost | 182 | 51139.319 | 55978.667 |
| Cost-aware fixed target | 240 | 55978.667 | 55978.667 |

Target-cost consumes fewer actual shots but delivers less often; its penalized
cost ties fixed target. This is not a broad delivery improvement. All arms have
zero observed secondary interval misses and erroneous declarations; per-cell
uncertainty and no-declaration denominators remain in `analysis.json`. Do not
interpret this heterogeneous aggregate as a single-binomial coverage estimate.
The repeated E001 cell is descriptive and not extra independent confirmation.

Forecast-versus-observed radius diagnostics are retained on comparable rows.
For example, the primary target's common delta proxy was below the observed radius
in 102/400 rows despite all forecasts meeting its margin. This illustrates why
the heuristic is not a delivery certificate. Historical equal-pilot selection
uses its separately stored CP forecast, not the common delta diagnostic.

## Scientific decision

Week-12 development tasks are complete. Do not promote this policy to a superiority
or novelty claim and do not launch a confirmation campaign on its behalf. Retain
the fixed-target comparator and the negative/tied result. Unequal-full changes
the menu and forecast as well as symmetry, so its comparisons are not a pure
unequal-calibration ablation. No theorem of optimality or quantum advantage exists.

The quantum-centered program can proceed to week 13's bounded encoding/state-
preparation feasibility work. It still needs a genuine quantum resource/algorithm
contribution against strong classical baselines; allocation software alone does
not meet that objective. A reliability-only paper is not silently substituted.
