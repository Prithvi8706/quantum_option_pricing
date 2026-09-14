# Week 4 readout transfer and dollar-precision discovery

Declared before execution. This is an extension of finite-calibration discovery,
not confirmation, a new gate-noise guarantee, or a matched comparator benchmark.

## Statistical extension

Supply bounds df/dg on the absolute changes from calibration error probabilities
to each validation depth's false-positive/false-negative rate. Expand both
calibration Clopper–Pearson intervals by these amounts, clipped to [0,1], then
apply the existing all-branch readout inversion. The same .025 calibration and
.025 validation allocation applies. If expanded upper rates sum to >=1, return
the full amplitude interval. Supplied bounds are assumptions, not estimates.
Conditional independent binomial observations remain necessary.

## Fixed prospective matrix

C6 discovery contracts, n=6 and scale .125 for all, dollar tolerance 1. Refuse
before acquiring either calibration or validation shots when the analytical
deterministic bound is >=1. Preserve all six contract denominators. No selector
uses Black–Scholes or the true encoded amplitude. Evaluate those answers only
after bounds/fixed representation decisions, for simulation and diagnostics.

Five conditions with baseline f=.02,g=.07:

1. Stationary calibration and validation.
2. Constant transfer: validation f=.05,g=.04; original calibration rates.
3. Depth transfer: validation f=.02+[0,.015,.03], g=.07-[0,.015,.03].
4. Imperfect calibration preparation: each calibration input independently flips
   with probability .02. Observed calibration rates are f+.02*(1-f-g) and
   g+.02*(1-f-g); validation keeps original rates. This explicitly breaks the
   earlier perfect-preparation assumption. Supplied .03 transfer bounds cover
   the resulting effective rate differences in this synthetic example only.
5. Out-of-bound transfer: validation f=.10,g=.07. This is an intentional failure
   stress outside the supplied .03 bound; no containment guarantee applies.

For each condition/contract: 200 attempts, giving 6000 attempted datasets.
Acquire 4096 calibration shots per state and 32768 validation shots at each of
depths (0,1,2), only for bound-feasible contracts. No repeated validation, adaptive
stopping or retries. Use separate purpose-separated streams for both stages.

Analyze the same counts with two procedures: unexpanded calibration intervals
(transfer bounds 0,0), and supplied-bound guarded intervals (.03,.03). Save all
amplitude components and calibration rectangles; map each hull to dollars with
the unchanged analytical deterministic bound. Negative price endpoints are not
clipped. Record containment, delivery, incompatibility and false declarations.
Report erroneous declarations both per attempted/executed dataset and among
declarations. No conditional-on-delivery guarantee is asserted.

Costs per executed dataset: 98304 validation shots, 294912 validation pricing
A-equivalents, 8192 simple calibration shots, 106496 total shots. Both inference
procedures share observations; do not double acquisition cost. Pre-refusal costs
zero quantum shots but bound computation is real classical setup and is timed.
No comparison to the week-3 classical wall times is a quantum speedup result.

Source/protocol snapshots and fixed representation decisions precede stochastic
observations. Save plan, raw records, summary, failures and completion hashes.
As before, floating-point padding is not formal numerical certification.
