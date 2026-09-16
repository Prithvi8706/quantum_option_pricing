# Week 14 finite-target comparison protocol v1

Prospective development, not fresh confirmation. Continuous-price admission
failed week13; no application policy is admitted and no bias field is filled
with an empirical discrepancy. This protocol executes the finite diagnostics
allowed by the handoff and records other roadmap deliverables as blocked where
their prerequisites are missing. No automatic week15 promotion.

## Frozen target, runs and comparisons

Use week13 case3: assets2, dates2, strike100, all original Basket defaults,
one bit per independent Gaussian, cutoff3. Sixteen weighted midpoint paths;
four state qubits and one flag. Do not substitute this finite expectation for
the original continuous-normal GBM expectation or 12/52-fixing contracts.
Raw and beta1 geometric residual use their existing product loaders and full
payoff tables. Residual offset here is the FINITE geometric expectation.
No continuous analytic offset in these finite comparisons.

1. For each representation and k=0,1,2,3,4 execute compiled Q^k A statevectors.
   Independently evolve full density matrices using compiled A/A-inverse and
   explicit flag/zero reflections. Apply global depolarization eta=0 or.02 after
   EVERY A/A-inverse, not after reflections. Validate good-flag probability
   against .5+(1-eta)^(2k+1)*(sin²((2k+1)asin(sqrt(a)))-.5), tolerance1e-10.
   Check trace/Hermiticity and eigenvalue floor -1e-10. This is a deliberately
   defined noise model, not physical per-gate calibration. Record actual logical
   u/cx counts, qubits and full compiled depth including reflections.
2. Fixed project CP diagnostics: depth ladder[0,1,2,3,4] with128shots each;
   k0 baseline640shots (same shots) and3200shots (same A-equivalents). Sixteen
   trials per cell. Noise/model pairs(0,0),(.02,.02),(.02,0). Counts sampled from
   density-validated responses, not new repeated hardware simulations. Matched
   and ignored noise analyses share observations. Fixed alpha=.05 Bonferroni
   all-branch CP inversion; no native IQAE label for this project method.
3. Native pinned Terra0.46.3 IQAE, beta intervals, alpha=.05, dollar target1,
   epsilon=min(.49,1/scale), shots256 per batch, persistent seeded Generator.
   Eight independent runs per representation, ideal finite-shot Sampler using
   actual circuits. Native stopping unchanged. External safety limits k<=16,
   batches<=64 and A-equivalents<=65536; a capped run is an explicit abstention,
   with every completed batch retained. No exact-probability sampler fallback.
4. Unchanged vendored csAE at commit202ffb8a, flagship_schedule(cap4,base64),
   16trials per representation/noise-model pair above. Source simulates bad-flag
   cos² observations; set its evaluator amplitude range to(sqrt(a),sqrt(a)),
   map theta_hat back to sin²(theta_hat) for pricing. Preserve raw outputs and
   counts; source amplitude-error constants are NOT price-error constants.
   This is a modern depth-limited noise-aware POINT estimator with known eta,
   not a confidence procedure. Truth is used only by its observation simulator
   and scoring, not passed to its likelihood search. Synthetic counts remain
   distinct from native IQAE's executed circuit batches.
5. Week12 policy ablations: all five unchanged arms, 16trials each, readout
   calibration f=.02,g=.07. Pricing drift/declared guard=(0,0),(.03,0),(.03,.03).
   Independent pilot and fresh calibration/pricing batches; finite diagnostic
   Encoding bias0 means the ideal numerical-table target ONLY. Drift changes
   both readout errors; eta depolarization is NOT mixed into this experiment.
   Guard influences planning and terminal inversion, so this is a policy-level
   comparison, not a pure fixed-plan transfer ablation. All pilot/calibration
   shots charged; basis-state calibration has zero logical CX in this ideal
   circuit model, but is not zero-time or free hardware calibration.
6. Sixteen IID finite-path estimates using3200paths per representation, with
   shared path draws, identical control and finite offset. Compare with exact
   finite summation, already available after table setup. Continuous-model
   MC/RQMC/conditional comparisons retain week11 evidence and week13 references;
   they cannot be compared as the same target in this finite campaign.

All streams purpose-separated under week14_development_v1. Tests use different
contracts/namespace and smaller trial counts, not production study observations.
Setup/table/compilation time and estimator time remain simulator/classical time.
Report shots, A-equivalents, Grover queries, logical CX and maximum depth
separately; do not add counts for components already included in full circuits.
Native source-query conventions must be shown alongside corrected accounting.
One-time table setup is not free; its exact sum makes a finite-table advantage
claim unsupported regardless of fewer shots. No physical-clock crossover.

## Analysis, gates and archive

For confidence methods report declarations, abstention/incompatibility, interval
misses and >$1 erroneous declarations with unconditional and declaration-only
denominators. Give pointwise binomial CP intervals for within-cell rates;16trials
are diagnostic and cannot establish rare-event reliability. Point-only csAE/MC
report estimates/errors and costs, not invented delivery/coverage. No selection
of winning seeds, post-result tuning, pooled heterogeneous coverage or formal
method-interest significance test. Correct matching assumes noiseless reflections
and known global eta; ignored noise/drift are outside-model stresses.

Containment means the delivered hull interval, not every disconnected component
of the original confidence set. Empty/incompatible project sets count as misses
in unconditional containment; returned-interval containment also has its own
denominator. Native caps remain attempts and non-deliveries without invented
intervals; unconditional containing-output rate treats them as no containing
output, while native returned-interval misses are separate. Erroneous declaration
is declared AND absolute error>$1. Zero declarations gives an undefined
declaration-only error rate. A matched CP 5% unconditional error bound does NOT
imply a5% error rate conditional on declaration. Mismatched cells explicitly
carry no in-model coverage guarantee, even if interval width meets tolerance.
Depths are reported both unitary-only and measurement-inclusive; native oracle
decomposition is preserved, not silently replaced by the diagnostic reflection.

Exclusive archive, frozen producer/protocol and input identity, source snapshots,
library version/native source hashes, per-task starts, durable raw-draw/batch
checkpoints before project analysis, complete outcomes and immutable manifest.
Catchable failures retain stage, elapsed time and unknown costs; a native csAE
batch may be interrupted inside upstream generation before counts are available,
which is explicitly incomplete accounting, not zero spent cost. Do not retry
into an existing directory. Completion published atomically after fsync.
Replay checks complete file inventory, checksums, source/input/environment,
and recomputes every deterministic output in the producing environment.

Deliver updated comparison/resource/claim reports, independent software/scientific
reviews, and a bounded human-collaborator review packet. Human sign-off stays
pending unless actually obtained. Confirmation protocol must NOT be labelled
signed off with failed application/novelty gates. Completing this bounded week
does not claim completion of prerequisite-blocked certified experiments.
