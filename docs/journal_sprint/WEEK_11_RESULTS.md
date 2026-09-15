# Week 11: classical baseline and reference evidence

Date 2026-09-15. Development measurements, not quantum experiments or confirmation.
Protocols: [stage A](PROTOCOL_W11_BASELINES_V1.md),
[stages B/C](PROTOCOL_W11_MAIN_V1.md). Quantum contribution status is separately
recorded in the [prior-work checkpoint](WEEK_11_NOVELTY_MATRIX.md).

## Implementation and pre-acquisition verification

`w11_baselines.py` provides method-specific PCA setup with the same means,
covariance, analytic control expectation and estimates as the old combined setup.
Raw methods do not pay for a conditional residual eigendecomposition; the
conditional method does not pay for the raw eigendecomposition. Both retain the
common payoff evaluator; raw Sobol still computes unused control values in that
shared implementation. This is a strong tested baseline, not proof of optimal
classical implementation or absence of further optimization opportunities.

`run_w11_baselines.py` runs only the timing pilot. `run_w11_main.py` separately
gates reference/main stages. Archives contain planned schedules, source and
protocol snapshots, dirty tracked patch, environment/BLAS/thread information,
durable attempt events, numerical outputs and sampled system-load/memory data.
Every standalone control estimator gets fresh 1024-observation training. Raw
Sobol has no training cost. Seeds separate method/order/training/evaluation and
pilot/reference/main purposes. No held-out candidate cases are acquired.

Pre-acquisition checks: 39 tests passed for stage A and the existing shortlist
mathematics; seven additional stage-B/C tests passed before those acquisitions.
Tests cover setup/estimate equivalence, seed/order separation, all-repetition
accounting, reference gates, injected failure preservation, soft-cap partial
archives, raw/event reconciliation and numerical replay/tamper detection.
Ruff passed all five new Python/test files after one line-length fix before runs.

## Stage A: timing/memory pilot

Archive: `results/journal_sprint/w11_baseline_pilot_v1`.
128 pilot rows plus four global warmups, all complete; acquisition wall time
7.8744 seconds. Peak process working set 97,746,944 bytes. CPU-utilization
samples ranged 0-60%, mean 11.73%; external contention was not controlled.

Mean standalone seconds across the pilot's balanced dimensions and N=256/1024:

| Method | Setup | Training | Evaluation | Standalone |
|---|---:|---:|---:|---:|
| Antithetic MC + control | .003160 | .006659 | .003041 | .012860 |
| Raw RQMC | .003279 | 0 | .015938 | .019217 |
| RQMC + control | .002833 | .007171 | .016899 | .026903 |
| Conditional RQMC + control | .003024 | .095793 | .059801 | .158618 |

These are pilot timings at unequal accuracy, not a cost-to-accuracy ranking.
The prospectively recorded linear-in-N feasibility extrapolation gave 253.02
reference seconds and 602.68 main seconds, excluding archive overhead; these
forecasts are not measured scaling laws. The full matrices were retained before
stage-B/C observations. Replay verified 234 files and all 132 numerical rows;
timings were excluded from numeric equality and not overwritten by replay.

## Stage B: refined references

Archive: `results/journal_sprint/w11_references_v1`.
All 384 independent estimates complete: twelve contracts, 32 scrambles each,
32768 evaluations per scramble. Total 12,582,912 reference evaluations plus
393,216 independent control-training evaluations. Acquisition 150.1999 seconds;
summary computation .0011 seconds. Peak process working set 249,593,856 bytes;
sampled system CPU 3.9-48.2%, mean 10.39%.

Reference standard errors range .00003506-.00006125 dollars, satisfying the
predeclared SE <= .001 diagnostic in all twelve cases. Reference means and
uncertainties are saved in `analysis.json`. They remain numerical references,
not exact prices or finite-sample absolute-error guarantees. Errors near that
uncertainty must not support precise RMSE-ratio claims.

Replay verified 490 files and all 384 numerical rows before main acquisition.
No reference was selected for agreement with a preferred main estimator.

## Stage C: full development comparison

Archive: `results/journal_sprint/w11_main_v1`.
All 2304 main rows plus four warmups completed, with no acquisition failures.
Acquisition wall time 557.6676 seconds; analysis .0621 seconds. Main work totals
16,515,072 evaluation observations and 1,769,472 control-training observations;
the four warmups add 1024 evaluations and 3072 training observations separately.
Peak process working set 173,641,728 bytes. Sampled system CPU ranged 0-100%,
mean 13.28%; short-interval samples are noisy and do not establish an idle system.

Each range below spans twelve contracts. RMSE is for individual deployments
relative to the independent numerical reference, estimated over 16 repetitions.
Seconds are mean standalone setup + training + evaluation, averaged across the
twelve contracts; they are NOT the total cost of a 16-deployment mean/interval.

| N per deployment | Method | Reference-relative RMSE range ($) | Mean standalone seconds |
|---:|---|---:|---:|
| 1024 | MC + control | .013302-.034574 | .01636 |
| 1024 | Raw RQMC | .005562-.014743 | .02452 |
| 1024 | RQMC + control | .002082-.004084 | .03072 |
| 1024 | Conditional + control | .000810-.002091 | .18872 |
| 4096 | MC + control | .007975-.014854 | .03596 |
| 4096 | Raw RQMC | .001764-.002907 | .06251 |
| 4096 | RQMC + control | .000748-.001421 | .06993 |
| 4096 | Conditional + control | .000221-.000458 | .45371 |
| 16384 | MC + control | .003973-.008572 | .10181 |
| 16384 | Raw RQMC | .000403-.000853 | .19607 |
| 16384 | RQMC + control | .000293-.000494 | .20513 |
| 16384 | Conditional + control | .000068-.000164 | 1.41257 |

Conditional-control RQMC has lower observed RMSE than raw-control RQMC in all
36 matched contract/N cells, but standalone time is 5.29-9.01 times greater at
the SAME N. Neither this ratio nor the table is a matched-accuracy speedup claim.
At N=16384 some conditional errors approach reference SE, limiting fine ranking.
All twelve RQMC-control N=1024 cells have empirical RMSE below one cent. That
shows these tasks are already classically tractable at this research threshold;
it is NOT a 95% finite-sample guarantee of one-cent error on each invocation.

The archive's 144-cell analysis retains approximate t halfwidths for the mean of
16 independent deployments, alongside the SUM of all 16 deployment costs and
observation counts. It also records training/setup and hypothetical 10/100-reuse
accounting separately. No result was dropped for favoring a classical method.

Independent post-processing in PowerShell recomputed all 144 RMSEs and aggregate
cost denominators directly from raw rows: largest RMSE discrepancy 4.663e-16;
all groups have 16 deployments. Initial read-only audit commands had a pipeline
syntax error and then a strike-key formatting mismatch (90.0 versus 90); corrected
commands passed. These were audit-command issues, not acquisition/analysis
failures, and no data or experiment was rerun to repair them.

Final main replay verified 2415 files and all 2308 numerical rows, including
source snapshots, event/row reconciliation, reference-manifest provenance and
the saved 144-cell analysis. Replay excludes measured timings/telemetry; it does
not replace the original timing observations. This is automated verification,
not independent human peer review.

Full regression passed 569 tests, no failures/errors/skips, 11 upstream Qiskit
warnings, in 277.76 seconds (`results/journal_sprint/tests_week11_v1.xml`). The
test run and main replay overlapped AFTER acquisition; their wall times are not
benchmark observations. Ruff passed all seven week-11 Python/test files including
the previously added shared contract. See [week closeout](WEEK_11_CLOSEOUT.md).

## Reproduction and limitations

Set OMP_NUM_THREADS, OPENBLAS_NUM_THREADS and MKL_NUM_THREADS to 1 before starting
Python, then invoke the corresponding runner from the repository root with a
NEW output directory. `--verify` checks manifests/live-versus-snapshot sources
and numerically replays acquired observations; it does not reproduce runtime.
Use the archive's source/environment when live sources change. Existing files
are never overwritten; retries use distinct paths and retain original failures.

No test suite, other agent-launched benchmark or replay ran alongside acquisition.
Documentation edits, read-only result inspection and remote literature browsing
did occur; external machine activity remained uncontrolled and sampled telemetry
cannot fully attribute contention. Interleaving mitigates order confounding but
does not produce hardware-independent performance conclusions. Peak memory is
process-lifetime, not each method's individual maximum. The NumPy metadata
warning about optional PyYAML is informational, not an acquisition failure.
No noise/quantum circuit claim, new algorithm or statistical coverage theorem
follows from these classical observations.
