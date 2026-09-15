# Week 11 classical baseline protocol, v1

Design recorded 2026-09-15 before new week-11 stochastic observations.
Status: prospective development protocol; runner/acquisition not yet implemented.
Freeze a copy and SHA256 in each actual run. Changes require a dated amendment;
do not describe this document alone as an executed or confirmed experiment.

Implementation clarification, recorded before stage-A acquisition: four warmups
are global (one per method on the 2-asset/12-date strike-100 case), followed by
128 pilot rows. Every method/repetition uses fresh independent control training
where needed. Only its required factorization is computed; the cheap scalar
control mean and the existing common payoff evaluator are retained for raw RQMC.
The deadline is checked between deployments, allowing at most one deployment's
overrun; acquisition wall time includes durable row/event writes but excludes
archive initialization. Peak working set is a process-lifetime high-water mark,
not per-method peak allocation. psutil records sampled system utilization;
uncontrolled external load remains a timing limitation. Numerical replay excludes
all timings/telemetry and does not replace original measurements. Stage B/C are
not launched by the stage-A runner. The initial status above describes the
protocol's creation; actual execution is recorded separately in the working log.

## Question and role

Establish trustworthy classical cost-to-accuracy baselines for the existing
discretely monitored GBM Asian baskets. Refine uncertain references and remove
the concurrent-load/fixed-order timing weaknesses of `shortlist_v1`.
This does not test a quantum algorithm or authorize a quantum advantage claim.

The old twelve contracts and every old outcome remain development evidence.
They are not fresh held-out tasks merely because new random seeds are used.

## Targets and accuracy

Development matrix: assets 2/4, dates 12/52, strikes 90/100/110, equal weights,
spot 100, volatility .3, rate .03, maturity 1, positive equicorrelation .5.
Target: discounted expected call on the equally weighted arithmetic average
over those assets and contractual dates. GBM sampling is exact at the dates;
no continuous-monitoring or empirically calibrated market-model claim.

Dollar tolerance ladder: .01, .05, .10 and 1.00 per normalized claim with spot
100. These are transparent research design choices (cent, five-cent, ten-cent
and dollar precision), NOT evidence of actual desk requirements or an industry
standard. Retain all thresholds regardless of which method wins. Economic
relevance of the final primary threshold remains a manuscript scope question.

Keep distinct: reference-relative RMSE, approximate confidence-interval width,
and a certified delivered-price error. A numerical reference is not exact truth.
The nominal interval level is .95; Student-t intervals across independent
scrambles/replicates are approximate and are not binomial CP certificates.

## Held-out reservation

Reserve three assets, 24 contractual dates, strikes 95/105, volatilities .2/.4
and correlations .25/.75 (eight combinations); other parameters unchanged.
Do not acquire these results during week 11 or use them to tune allocation,
encoding or tolerances. Audit existing archives for accidental prior exposure
before week-14 confirmation freeze; replace contaminated cells prospectively.
The eight cases are a reserved candidate set, not a statistical power calculation
or a promise of quantum circuits at all dimensions. No population claim follows
from this deliberately selected set.

## Methods and work accounting

Reuse independently tested PCA GBM, analytic geometric control mean, conditional
common-factor integration and antithetic MC from `asian_basket.py`:

1. Antithetic MC with geometric control.
2. Scrambled Sobol without control.
3. Scrambled Sobol with geometric control.
4. Conditional scrambled Sobol with conditional geometric control.

For each independent deployment repetition, fit needed coefficients on separate
1024-evaluation IID pilots, independent of evaluation and reference streams.
Raw methods may share the same frozen pilot for paired comparisons, but each
standalone cost includes its own necessary training. Raw Sobol pays no control
training. Conditional fitting must be costed, not supplied free from old runs.
Count antithetic N as N payoff evaluations, formed from N/2 independent draws.

Separate setup, control fitting, evaluation, interval/analysis time and reference
construction. Count all repeated scrambles/evaluations needed for a reported
interval; a 16-scramble estimate does not have the cost of one scramble.
Reference generation is evaluation infrastructure, not a deployed pricer input;
report it separately and never feed its value to the controller.

The current setup computes raw and conditional factorizations jointly. The
timing runner must either separate method-required setup with equivalence tests,
or explicitly report the shared implementation overhead without claiming an
optimized standalone baseline. Do not selectively charge unused setup to a rival.
One-off cost is primary. Amortized setup/training is secondary, with declared
reuse counts of 10 and 100 compatible estimates; no unexplained free training.

## Bounded acquisition stages

### A. Timing/memory pilot

Four development contracts: each assets/date pair at strike 100. Four methods,
N=256/1024, four independent repetitions: 128 estimate rows. Use fresh purpose-
separated streams under `w11_baselines_v1`, never the `shortlist_v1` namespace.
One unscored warmup per method at N=256 is charged as experiment overhead.
Persist all warmup/pilot attempts; excluded from accuracy comparisons by design.

Record hardware, OS, Python/library/BLAS versions, thread settings, source hashes,
method order, wall times and peak process memory (or explicitly unavailable).
Single-thread numerical libraries; no simultaneous test suite or benchmark job
launched by this agent. External machine load cannot be assumed absent: record
observed contention and qualify/repeat timing rather than claiming isolation.

Interleave methods within contract/N/repetition blocks using a seeded permutation
independent of sample streams. Avoid running all repetitions of one method first.
Cap the pilot at 20 minutes wall time; record a partial run, never silently drop
unfinished cells. Use measured costs/memory to approve or reduce the next-stage
matrix in a versioned amendment BEFORE acquiring it. Pilot data remain discovery.

### B. Reference refinement (only after pilot feasibility)

For each of twelve development contracts: 32 independent raw-control RQMC
scrambles at N=32768, with separately fitted independent reference control
coefficients. Fixed work, not stop when the reference happens to look favorable.
Use batching if needed, documenting the implementation and numerical replay
tolerances. A different estimator/size requires an explicit amendment.

Report reference mean and between-scramble standard error. A provisional
adequacy screen is reference SE <= .001 (10% of the smallest tolerance .01).
This is a precision diagnostic, not a certified error bound. Comparisons near
that reference uncertainty cannot support precise RMSE ratios. If the screen
fails, mark unresolved and predeclare a separate refinement; retain stage B.

### C. Main development timings (only after feasibility/reference review)

Proposed cap: twelve contracts, four methods, N=1024/4096/16384, 16 independent
repetitions = 2304 estimate rows. This is a development cost/variance study,
not the week-15 confirmation campaign. Stage-A timings determine whether this
cap is affordable; final execution matrix must be frozen in the run manifest.
Do not select N retrospectively from which method appears to win.

Report per-cell means, between-repetition uncertainty, reference-relative RMSE,
setup/training/evaluation times, total work and failures. Approximate t intervals
over all 16 repetitions describe their average and must charge all 16 runs.
Single-run RMSE and an interval on the 16-run mean are different outcomes.
Runtime-to-tolerance conclusions require uncertainty-aware comparison; no
asymptotic slope or crossover inferred from three sample sizes alone.

## Validation, provenance and stopping

Before observations: setup equivalence, analytic geometric/one-date limits,
independent conditional quadrature, seed separation, method-order reproducibility,
cost accounting and interrupt/replay tests. Record source/environment before
running and use an exclusive output directory. Persist intended, started,
completed and failed events; preserve first attempts and separate retries.

Replay numerical quantities against source snapshots; exclude elapsed time from
numeric equality checks. Retain timing measurements rather than replacing them
with replay times. Stop on semantic/reference failures and report them. No paid
hardware, market-data acquisition or external submission is part of this protocol.

## Subsequent design decision

Only after these development findings, freeze the week-12 asymmetric-allocation
manifest and compute budget. Keep fixed CP and equal-calibration pilot CP as
strong baselines. Choose repetitions and practical effect criteria prospectively;
this classical protocol does not supply a power calculation for quantum trials.
