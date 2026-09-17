# Study Week 2: application validation

Status: bounded Week2 completed and verified. Candidate remains
standby. No manuscript promotion, production replacement, PR, merge, or
hardware run is part of this work package.

## Scope

[Frozen protocol](MINIMAL_PIVOT_WEEK2_PROTOCOL.md),
[integration/error derivation](MINIMAL_PIVOT_WEEK2_METHOD.md),
[targeted prior-art assessment](MINIMAL_PIVOT_WEEK2_PRIOR_ART.md).

The study keeps the arithmetic Asian basket, known risk-neutral GBM, equal
averaging and existing finite encoding. Four fresh acquisitions vary basket
size, volatility, correlation and strike. D1/D2 are development; E1/E2 are
reserved evaluation cases, not independent statistical confirmation or an
assertion that no historical sweep has ever used those parameter values.

## What was implemented

Product-normal loading, original/reflection signals, residual QSP, directed
classical offset, Hadamard readout, canonical AE, explicit clean-workspace
zero reflections, outcome decoding and an encoding/degree selection rule.
Selection minimizes projected composition CX only among logically feasible
dollar1/95% candidates. Physical execution remains unbounded, so production
selection always refuses; this is separate from the ideal-plan choice.

The production-resolution study constructs q10 signal circuits and compiles
their components. It does not run a full production-size pricing circuit.
Whole-algorithm resource figures are composition projections, not measured
full-circuit or fault-tolerant costs. QFT and controlled logical operations
are ideal in the mathematical schedule; native decomposition/noise remains
outside the certified budget.

## Integrated logical-plan results

32 configurations:4 cases x2 encodings x4 polynomial degrees. Nine configurations
pass the logical deterministic-plus-AE planning gate; the lowest projected
cost is selected within each encoding. All32 refuse physical promotion.

| Case | Original best degree / A calls | Reflection best degree / A calls | Original/reflection projected CX ratio |
| --- | ---: | ---: | ---: |
| D1 | 128 /17,391 | 64 /4,335 | 4.0318 |
| D2 | 128 /69,615 | 128 /17,391 | 2.0139 |
| E1 | 128 /139,247 | 128 /17,391 | 4.0195 |
| E2 | No feasible degree | No feasible degree | Not applicable |

Selected reflection deterministic/statistical dollar bounds are
0.454738/0.440523 (D1),0.600398/0.263636 (D2),0.652158/0.292337 (E1),
rounded upward here. Their sums are below1 under the stated ideal assumptions.
The corresponding qubit projections, including AE and clean workspace, are
55,103,79. Projected total CX counts are approximately3.54e11,1.06e13,4.28e12:
large absolute costs despite favorable relative ratios. These are ratios of
composition projections, not guaranteed ratios of optimized physical costs.

E2 fails even at degree128: original deterministic bound1.535048, reflection
1.316544. There is no remaining statistical budget. This is failure of the
fixed q10/degree<=128 menu, not an impossibility theorem for the option.

A final accounting audit noticed that the explicit tiny AE adapter uses inverse
QFT swaps whereas the initial production projection charged only its controlled
rotations. Analysis v2 adds3CX per swap, floor(m/2) swaps per repetition, to
every eligible alternative before selection. The adjustment is153-306CX for
the reported plans and does not change the choices or rounded ratios. Raw
acquisition and analysis v1 remain intact; analysis v2 is authoritative.

## Completed small-circuit execution

Both d2/q1/degree16 pipelines actually ran as ideal statevector circuits,
including canonical AE with three evaluation qubits (10 total qubits).
The integrated pre-estimation price matches independent scalar QSP evaluation
within3.9e-13; the full AE distribution matches the independent Fourier-kernel
formula within2.25e-12. These are numerical diagnostics, not error certificates.

The finite midpoint truth here is21.5833936, NOT the continuous D1 price10.2072.
Original/reflection polynomial prices are19.8109611/21.6410812. With the fixed
M8 and21 simulated repetitions, AE outputs16.5161191/20.7330629, with broad
theorem statistical radii19.6501/8.56092. The apparently sub-dollar realized
error of the centered draw is not certified dollar1 delivery. Retain this
coarse-budget result and do not headline a single favorable random draw.

Actually compiled full AE circuits use911,871 original versus1,147,295
reflection CX at this SAME degree/M. Thus centering loses fixed-schedule gate
cost; production projections can favor it only after degree/AE-budget selection.

## Classical continuous-target results

At16 independent replicates of4096 paths each, plus1024 pilot paths:

| Case | Conditional RQMC price | Approximate95% halfwidth |
| --- | ---: | ---: |
| D1:1asset,2dates,sigma.2,K95,rho.3 | 10.2072042 | 0.0000601 |
| D2:2assets,2dates,sigma.25,K105,rho.4 | 5.4118578 | 0.0001525 |
| E1:1asset,3dates,sigma.35,K110,rho.6 | 6.9419303 | 0.0002153 |
| E2:2assets,2dates,sigma.4,K90,rho.7 | 17.7801327 | 0.0003054 |

All24 classical method/budget cells (MC+control, RQMC+control, conditional
RQMC+control, powers10/12) are retained. These are replicate Student-t
diagnostics, NOT proved coverage or exact truths. Ordinary RQMC is faster in
the recorded environment while conditional RQMC has smaller halfwidths.
Setup/pilot/evaluation timings are separate artifacts; they must not be
compared with quantum simulation time as a hardware-speedup claim.

## Development interruption and repair

The initial tiny AE acquisition and its replay were stopped: the library's
controlled-power construction repeatedly expanded large circuits. Their
planned manifests and interruption records remain in the v1 directories;
neither has a completion marker. The explicit replacement compiles one Grover
iterate, controls it once, repeats it for QPE, then applies inverse QFT. It
preserves M8,21 repetitions, the same phases/contract and315 A-equivalent calls.
Small analytic-distribution tests verify the replacement's probability and
bit-order convention. This is an implementation repair, not favorable tuning.

Authoritative tiny evidence is v2; production/classical evidence is v1.
Directed outcome decoding separately encloses sin^2(pi*y/M) and the median
price, avoiding reliance on binary libm sine for certified decoding. The
original floating tiny diagnostic is checked against this enclosure; it is
not silently relabeled a directed computation.

## Evidence locations

Under `results/journal_sprint/`:

- `minimal_pivot_week2_production_v1` and `_production_replay_v1`.
- `minimal_pivot_week2_classical_v1` and `_classical_replay_v1`.
- `minimal_pivot_week2_tiny_v2` and `_tiny_replay_v2`.
- `minimal_pivot_week2_final_verification_v1.json` (final checker).
- `minimal_pivot_week2_analysis_v2.json` (corrected comparisons and analytic AE checks).
- `minimal_pivot_week2_full_tests_v3.xml` (final integrated tests).

Final full suite:1,142 passed,12 legacy warnings,562.74seconds. The28 new tests
also passed in the separate pinned environment; these overlap the full suite.
The preceding v2 full run had1 failure/1141 passes: an old W12 provenance test
correctly detected that `analyze_week2.py` was edited during its frozen-source
check. The differing hash was identified, the isolated test passed after
freezing edits, and the final full rerun passed. No guard was weakened. The
failed receipt is preserved alongside the earlier1131-pass v1 receipt.

The full1142-test run preceded the final report-only IQFT swap correction.
That correction has its own regression test and a final29-test focused run;
these tests overlap the full suite, not1142+29 distinct tests. No production
experiment producer or numerical error-budget code changed in that correction.

The final checker is `research.journal_sprint.verify_week2_final`, not the
earlier v1-only checker. Only timestamps/environment and measured wall times
are excluded from numeric equality; every archived file remains hash checked.
All pricing values, intervals, counts and decisions must reproduce exactly.
Same-producer replay is not independent scientific peer review.

All six completed acquisition/replay archives passed source/artifact integrity
and exact numeric-payload comparison (175-180 recorded source files per archive).
All32 schedule/decision rows passed fail-closed checks. Corrected analysis v2
also reproduced exactly in the separate environment, and its live source hash
matches its receipt. The IQFT correction leaves all selected encodings/degrees
unchanged. Ruff F and Git whitespace checks passed.

Reproduce using the existing pinned week15 environment and single-thread BLAS:

```powershell
venv/Scripts/python.exe -m research.journal_sprint.run_minimal_pivot_week2 production NEW_PRODUCTION_DIRECTORY
venv/Scripts/python.exe -m research.journal_sprint.run_minimal_pivot_week2 classical NEW_CLASSICAL_DIRECTORY
venv/Scripts/python.exe -m research.journal_sprint.run_week2_explicit_ae NEW_TINY_DIRECTORY
venv/Scripts/python.exe -m research.journal_sprint.verify_week2_final NEW_VERIFICATION.json
venv/Scripts/python.exe -m research.journal_sprint.analyze_week2 NEW_ANALYSIS.json
```

The final verifier/analyzer read the named authoritative archive directories;
producer output directories and receipt files must be new. Do not rerun the
legacy `tiny` option of the original runner: use the explicit-AE runner above.
Raw production projections require the final analysis step to charge explicit
IQFT swaps. Compilation/certification timings are per-case across all degree
and encoding alternatives, not hardware runtimes for the selected plan.

## Claim boundary

This work closes integration gaps in an ideal logical model; it does not
establish classical superiority, physical dollar1 delivery, global algorithmic
novelty or journal readiness. New prior art reinforces the need to charge
shots, oracle inverses and loading. The candidate stays standby as requested.
No production or confirmation gate is promoted by this study.
