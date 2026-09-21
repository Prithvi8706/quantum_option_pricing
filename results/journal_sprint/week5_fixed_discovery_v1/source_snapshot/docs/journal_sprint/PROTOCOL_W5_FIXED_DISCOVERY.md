# Week 5 fixed-design comparison: prospective discovery matrix

Declared before response observations. Run only after the k=2 resource profiles
and fixed-cost ledger pass integrity checks. This is not held-out confirmation
or a comparison with the native BAE/BIQAE estimators or strong classical pricing.

## Fixed designs and resource axes

All C6 contracts, n=6/c=.125, unchanged analytical dollar bounds and tolerance 1.
Pre-refuse bound >=1 before calibration or validation acquisition. Keep all
six contract denominators. Use the logical gate profiles for executable designs.

At reference budgets B=73728/294912 pricing A-equivalents:

- Direct: B shots at k=0.
- A-matched multidepth: B/9 shots at each of k=0,1,2.
- CX-capped multidepth: floor(B*CX0/(CX0+CX1+CX2)) shots at each depth.

The first multidepth contrast exactly matches A-equivalents. The second respects
the same pricing-CX cap as direct, with integer-rounding slack recorded; it is
not necessarily exactly equal cost. Report u gates, max circuit depth/qubits,
shots and A-equivalents alongside CX. No single axis represents full device
cost; routing, reset, measurement and hardware time remain unmodeled.

## Calibration and observations

100 repetitions per contract/budget/condition/design. Two conditions: stationary
f=.02,g=.07, and constant validation transfer to f=.05,g=.04. Calibration rates
remain .02/.07 in both. Each design acquires its own independent calibration
and validation draws with unique seed namespaces. Charge 4096 calibration shots
per state to each acquired design, with no hypothetical amortization.

All designs use guarded finite calibration (.03 per rate), alpha_cal=.025 and
alpha_validation=.025. The guard is a supplied valid assumption in these
synthetic conditions, not estimated device drift. Fixed validation occurs once;
no optional stopping, resampling failed intervals or outcome-dependent schedule.
Exact amplitudes/Black–Scholes are diagnostic inputs only after design/refusal.

Total matrix: 7200 attempted design datasets; under the unchanged refusal menu,
4800 acquisitions and 2400 pre-refusals. The single direct design serves both
comparison axes; do not create or charge a second copy merely to plot both.
No results have been produced for this protocol at declaration time.

## Outcomes and decision

Record all raw counts, calibration rectangles, amplitude components, dollar
intervals, state (refused/incompatible/unresolved/delivered), and cost ledgers.
Summarize per cell: interval containment, delivery, erroneous declarations per
attempt/acquisition and among declarations. Identify undefined conditional rates
when there are no declarations. Do not pool heterogeneous IID confidence claims.
This 100-trial matrix screens delivery/cost plumbing, not rare-error certification.

Compare direct against each predeclared multidepth arm at the appropriate axis.
Do not select the best observed configuration as a confirmatory controller.
Use the outcomes to plan a later discovery pilot and decide whether useful
fixed-design delivery warrants further work. Adaptive promotion remains off.
