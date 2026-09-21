# Next experiment: application-level design draft

This is a **draft, not a frozen v2 protocol**. No new experiment is launched by
this document. It is informed by exploratory v1 results and therefore cannot
serve as retrospective preregistration for them.

## First target: make probability accuracy mean price accuracy

For the existing linearized payoff post-processing,

`price(a) = exp(-r*T)*(U-K)*2/(pi*c)*(a-.5+pi*c/4)`.

Hence the price sensitivity is `L_P=exp(-r*T)*(U-K)*2/(pi*c)`. Smaller payoff scale
c reduces linearization distortion but amplifies statistical price uncertainty.
That trade-off is where representation/resource selection might add value.

Before testing a controller, independently verify this map against the existing
implementation and derive/validate distinct support, finite-grid and encoding
bounds. Observed differences against a known answer are diagnostics, not bounds
available to a deployable controller. Keep exact answers outside selection inputs.

## Small discovery matrix to consider

- Reuse the existing C6 contracts as explicitly *discovery*, not newly held-out
  cases. Do not invent a claim that previously inspected contracts are unseen.
- Candidate representation sizes n=3,4,5,6 and payoff scales c=.125,.25,.5.
  These are proposals, not certified-feasible configurations.
- Keep the established support rule initially so that representation and payoff
  changes can be interpreted separately. Account for any new support selection.
- Compare fixed shallow/deeper schedules before adding an adaptive controller.
  Include the cheap fixed-128 response baseline that beat the v1 pilot on cost.
- Express target accuracy in dollars and as a stated relative-to-spot tolerance;
  select actual thresholds prospectively after deterministic feasibility checks,
  not after inspecting stochastic wins.
- Start ideal and declared known-noise response models; add a bounded uncertainty
  envelope only with an explicit explanation of where its bounds come from.
- Keep hardware spending at zero until actual compiled pricing-circuit positive
  controls establish what the chosen noise response does and does not represent.

## Controller interface

Allowed inputs: contract parameters, candidate configurations, resource budget,
valid deterministic/calibration bounds, independent pilot counts and target
accuracy/confidence. Forbidden inputs: Black-Scholes or exact finite-grid answers,
validation outcomes before selection, and post hoc winning configurations.

Output: one configuration for fresh validation, or a documented refusal before
validation. All pilot/setup/calibration costs count even when selection refuses.
If later work allows repeated validation, it needs a valid sequential error budget
or confidence-sequence argument, not repeated fixed-sample intervals.

## Required comparisons and gates

1. Verify mathematical targets and price interval transformations first.
2. Validate response sampling against small actual ideal/noisy pricing circuits;
   the current single-qubit statevector check is not sufficient for noisy pricing.
3. Compare against fixed IQAE, a modern noise-aware estimator, and direct quantum
   sampling with explicit cost conventions. BAE/BIQAE still need real reproduction.
4. Use analytic/quadrature European references and costed control-variate MC and
   scrambled Sobol RQMC. Restore Paper B's evidence using saved raw replications,
   not a chart alone. MC-only comparisons cannot support the intended paper.
5. Promote only if the controller beats a strong inexpensive fixed baseline on a
   predeclared completion/cost objective, with failures included. Otherwise retain
   the fixed conservative method and report adaptation as unsuccessful.
6. Freeze a separate untouched confirmation set and protocol after discovery.

## What to write next, before a full manuscript

A methods note containing the independent target ladder, conditional coverage
argument, cost definition, controller pseudocode, calibration limitation, and
primary outcomes. Do not write an abstract announcing an advantage that these
experiments have not established. The final manuscript structure can follow:
problem and gap; targets/assumptions; method and guarantee; reproducibility and
baselines; outcomes/ablations; limitations; conclusion.
