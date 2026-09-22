# Capacity screen after the explicit estimator refinements

**Update:** exact range-specialized multiplication is recosted in
[CAPACITY_RANGE.md](CAPACITY_RANGE.md). The table below preserves the preceding
financial source; its narrow bare H8 failure no longer holds for the tight
Hadamard row after that source improvement.

22 September 2026. The estimator refinement materially improves the result:
the favorable one-T-per-nanosecond-per-physical-qubit work screen now **passes
for C4**, with either the conditional tight-moment Hadamard estimator or the
unconditional digital bounded-QAE estimator. It still does not establish a
physical crossover. The present allocation exceeds the qubit cap, and the
stated rotated-patch and factory capacity screens fail.

The [revised JSON](../../results/controlled_priority_completion/capacity_revised.json)
records six rows and exact SHA-256 bindings to `estimator_hadamard.json` and
`estimator_bounded.json`. It supersedes the previous estimator's capacity result
for the new schedules. Definitions and architecture premises are in
[the preceding derivation](CAPACITY_SCREEN.md).

## What changed

The tight-moment Hadamard schedule now uses 1,203,320 controlled-U calls for C4
or 2,967,610 for H8. It keeps the financial source and phase source and their
inverses. The shifted-probability QAE schedule uses 7,864,305 controlled Grover
iterates for either model; each contains financial compute/uncompute and the
exact selector/inverse, without an atan source. Neither quantum call is treated
as a cheap classical sample. Arbitrary rotation synthesis is granted for free
in these necessary arithmetic-work screens, favoring quantum feasibility.

| Estimator and model | Arithmetic T count | Bare work floor at 1 ns and one physical qubit per lane | 10x RQMC budget | Bare screen |
|---|---:|---:|---:|---|
| Tight-moment Hadamard, C4 | 1.636360e15 | 0.163636 s | 1.110592 s | Pass |
| Tight-moment Hadamard, H8 | 1.485259e16 | 1.485259 s | 1.384721 s | Fail |
| Digital shifted QAE, C4 | 1.059543e16 | 1.059543 s | 1.110592 s | Pass narrowly |
| Digital shifted QAE, H8 | 3.926105e16 | 3.926105 s | 1.384721 s | Fail |

These are work-conservation lower bounds **only under the stated per-lane
primitive and fixed workload**. Passing them does not demonstrate enough
parallelism or any feasible hardware. Treating the previous conservative
estimator's rejected work count as unavoidable would conceal this real
improvement. Conversely, the Hadamard tight moments remain conditional on the
unclosed transfer certificate; the shifted-QAE arithmetic schedule does not need
that certificate.

## Explicit encoded-lane and supply sensitivities

A distance-3 rotated patch occupies 17 physical data and syndrome qubits.
Granting one complete T consumption per patch per nanosecond, every physical
qubit to consumption lanes, and all data storage and state production for free,
the work floor rises to:

| Estimator | C4 | H8 |
|---|---:|---:|
| Tight-moment Hadamard | 2.782 s | 25.249 s |
| Digital shifted QAE | 18.012 s | 66.744 s |

This is an explicitly stated injection-lane model. It is not a necessary gate
cost for every code or native gate architecture. The JSON also varies code
cycle times from 1 ns to 1 microsecond and one versus d cycles per T. Those
coordinates are sensitivities, not demonstrated hardware specifications.

For the already stated 15-to-1 factory family, granting all ten million physical
qubits to final-stage factories, free lower-level states, no rejections, free
routing and up to ten million perfect initial states, the final-stage-only
capacity floor at distance 3 and a 1-ns code cycle is:

| Estimator | C4 | H8 |
|---|---:|---:|
| Tight-moment Hadamard | 1,009.798 s | 9,165.536 s |
| Digital shifted QAE | 6,538.437 s | 24,227.994 s |

The formula is `max(0,N_T-P)*121*(2d^2-1)*d*cycle/P`, conditional on each final
output occupying at least 11 tiles for 11d cycles in that specified factory
family. It is not a universal distillation lower bound. Alternative factory
protocols, native CCZ/T operations, catalysis or different codes need their own
verified supply calculation. Native-CCX work sensitivities are included but are
not substituted for a compiled implementation or high-fidelity CCZ factory.

## Memory and error correction remain separate obligations

Mapping the present allocated registers to one rotated patch each at distance
3 exceeds ten million physical qubits for every refined schedule. This is a
constraint on that mapping. It is not a lower bound on future pebbling,
recomputation, constant-register elimination or other source rewrites. No
physical impossibility follows solely from an upper allocation count.

For each comparator, the JSON also computes sufficient distances from the
adopted approximate noise fit, for p=1e-3 through 1e-6 and four cycle times. The
union-bound test is a certificate condition, not proof that every smaller
distance fails. The final-stage-only factory model leaves quality, rejection
and all earlier stages favorable; an actual proposal must restore those costs.

## Current decision

The improved estimators deserve credit as substantial quantum implementation
improvements. Neither supplies a conditional end-to-end physical advantage for
the present source. The current data mapping fails the cap, and all listed
distance-3-or-larger rotated-patch/factory scenarios fail the 10x RQMC budget.
The more generous C4 fixed-iid comparator changes bare consumption thresholds
but not the failed data mapping or chosen-family supply screen.

A source memory redesign and a verified faster injection/factory model would
change these premises and require recosting. They must not be dismissed using
the previous estimator's upper schedule. Full financial certification and
setup/output costs remain additional conditions even if those engineering
changes pass.

Reproduce:

```text
python -m research.controlled_priority_completion.capacity_revised
python -m pytest research/controlled_priority_completion/test_capacity_screen.py -q
```

Nine tests pass, including a test that the improved estimator can pass bare
capacity while failing storage and the specified factory screen. Targeted Ruff
checks pass. This is a computational capacity study, not a hardware experiment.
