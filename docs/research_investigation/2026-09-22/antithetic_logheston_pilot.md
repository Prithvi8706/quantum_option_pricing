# Executed development diagnostic: antithetic log-Heston corrections

Date: 2026-09-22. This is a variance-decay diagnostic, not a quantum-advantage
experiment, continuous-model price certificate, or confirmation set. A1 (one
asset) and A4 (four assets) were specified before this run by the research
investigation. They remain development cases. No old project files were changed.

## Frozen workload and construction

The output is a discounted arithmetic Asian call on the equal-weight basket,
with exactly 12 equally spaced contractual dates, one-year expiry, S0=K=100,
r=0.03, kappa=2, theta=v0=0.09, and xi=0.3. A level-l path uses
12*2^l numerical steps but averages only the 12 contractual dates. The model
therefore remains fixed as l changes.

The supplied drift-implicit Milstein update was implemented directly:

```
log S' = log S + (r-v/2)h + sqrt(v) dWs
         + xi/4 * (dWs*dWv-rho_sv*h)
v' = [v+kappa*theta*h+xi*sqrt(v)*dWv
      + xi^2/4*(dWv^2-h)] / (1+kappa*h).
```

No Levy-area variables or variance clipping are used. For these parameters the
variance-update numerator equals
`(sqrt(v)+xi*dWv/2)^2+(kappa*theta-xi^2/4)*h`, which is strictly positive.
This algebraic property of the discrete update does not establish the continuous
SDE's boundary regularity or the assumptions of a convergence theorem.

Equity Brownian correlation is 0.3 off-diagonal, and each equity/own-variance
correlation is -0.5. A common equity normal plus independent local equity normals
construct the equity vector. For each asset, the variance normal is
`-.5*equity_normal+sqrt(.75)*independent_normal`. Consequently cross-asset
variance correlation is 0.075 and cross-asset equity/variance correlation is
-0.15. These induced correlations are part of the workload, not independent
variance processes. The complete covariance matrix is recorded in the JSON and
checked positive definite. This general correlated model is not automatically
covered by restricted-correlation fast-forwarding results.

For each coarse interval the fine path receives Gaussian vectors `(Z0,Z1)`,
and its antithetic partner receives `(Z1,Z0)`. All components are swapped
simultaneously. The coarse path receives summed Brownian increments. We record
both `Pf-Pc` and `(Pf+Pa)/2-Pc` using the same three simulated paths.

Levels 1--5 each use eight independent replicates of 2,048 coupled paths.
Seeds are NumPy SeedSequence words `[20260922, assets, level, replicate]`.
Level zero was independently measured using eight batches of 2,048 direct
12-step paths with the corresponding level-zero seeds. The generator is
NumPy's default_rng. JSON records package versions and source hashes.

## Results

All variances below are in squared price units. Slopes fit
`log2(variance)` against level, using levels 1--5; the reported beta is its
negative. Eight per-replicate slope fits provide descriptive t radii. These
are not rigorous confidence statements about an asymptotic exponent.

| Case | Plain beta | Antithetic beta | Antithetic variance at l=1 | At l=5 | Plain/antithetic variance at l=5 |
|---|---:|---:|---:|---:|---:|
| A1 | 0.966 | 1.965 | 0.0115527 | 0.0000492349 | 571.5 |
| A4 | 0.980 | 1.973 | 0.00284391 | 0.0000111604 | 603.3 |

Descriptive 95% t radii for the antithetic slopes are 0.0823 (A1) and 0.0743
(A4). Fits excluding the first one or two levels are also in the JSON. Full
level-by-level correction means, variances, replicate values, timing partitions,
and seeds are retained; no cases or replicates were excluded.

The finest antithetic correction means are -0.00003834 +/- 0.00014289 for A1
and -0.00015555 +/- 0.00005118 for A4, using empirical 95% t intervals over the
eight replicate means. Neither interval bounds the remaining discretization
bias. A4's nonzero finest correction emphasizes that variance decay and bias
control are separate obligations.

Level-zero sample variances are 135.584 (A1) and 63.0278 (A4). Their large size
relative to the corrections means a credible variance-sensitive quantum cost
estimate must include the base level and useful controls; reporting correction
decay alone can hide the dominant cost. Level-zero sample means are 7.96043 and
5.70879, with broad empirical 95% radii 0.19729 and 0.15453. These are noisy
discrete-level estimates, not reference prices.

The correction pilot took 9.703 seconds of measured internal CPU-process wall
time; the independent level-zero plus memory supplement took 0.757 seconds.
The level-zero batches took 0.0556 seconds (A1) and 0.1509 seconds (A4), including
random-number generation and arithmetic, or 3.39 and 9.21 microseconds per path.
These tiny NumPy workloads were not warmed, GPU optimized, or independently
timing-calibrated. They are reproducibility diagnostics, not strong classical
benchmark throughput or coherent-oracle times.

The supplemental repeat of one largest-shape batch (A4, l=5, 2,048 paths)
recorded a Windows peak working set of 76,378,112 bytes (0.0711 GiB), including
Python imports, below the 16 GiB budget. The original full ensemble was not
memory instrumented. The implementation streams time steps and retains no
complete path histories, so state-array shape is independent of level.

## Verification and interpretation

With xi=0 and v0=theta, fine, swapped-fine and coarse payoffs agree pathwise
within 1.8e-12 in a four-asset check. All executed states/payoffs were finite and
all variances positive; the smallest variance state in the main ensemble was
approximately 0.000848. This checks coupling, monitoring, and the deterministic
variance limit. It does not verify weak-error order for stochastic volatility.

The result supports investigating the empirical beta approximately 2 premise
on these benign development parameters. It provides the same useful variance
reduction to classical antithetic MLMC. It does not resolve Heston square-root
boundary assumptions, a theorem for the proposed quantum algorithm, bounded
coherent input approximation, Gaussian preparation, reversible arithmetic,
amplitude-estimation constants, or competition from multilevel RQMC with
conditioning and controls. No quantum computation was simulated or timed.

The most informative next measurement is a strong classical price/error/runtime
curve on this exact contract using antithetic MLMC and multilevel RQMC, including
base-level controls and bias validation. Compare its available latency budget
with an independently compiled coherent step and base-level estimator before
expanding the case grid. A beta estimate alone is not a continue criterion for
an advantage claim.

## Reproduction and artifacts

From the repository root:

```
python docs/research_investigation/2026-09-22/antithetic_logheston_pilot.py
python docs/research_investigation/2026-09-22/antithetic_logheston_level0.py
```

These commands regenerate their adjacent JSON outputs. Preserve the current
outputs before a timing rerun. Dependencies are NumPy, SciPy, and psutil for the
memory supplement. Original executed evidence:

- [Main pilot source](antithetic_logheston_pilot.py) and [raw output](antithetic_logheston_pilot.json).
- [Independent level-zero/memory source](antithetic_logheston_level0.py) and [raw output](antithetic_logheston_level0.json).
- [QqMC/classical literature review](qqmc_review.md), [sanity script](qqmc_sanity.py), and [sanity output](qqmc_sanity.json).
