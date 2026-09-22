# Controlled residual follow-up: frozen feasibility protocol

Date: 22 September 2026. Existing compound evidence and manuscript are retained.
This tests a new estimator, not a rerun of the failed raw nested schedule.

## Hypothesis and output contract

For the same twelve development compound Asian-basket contracts, a classical
continuation surrogate plus quantum estimation of a controlled policy residual
and a rigorously bounded/localized exercise-regret correction can deliver a
price at absolute error $0.01 and 99% per-price confidence at 10x lower total
latency than the strongest eligible classical calculation. Hardware and full
output costs remain obligations; no theorem about oracle queries is a runtime.
No held-out confirmation cases will be opened at this feasibility stage.

The quantum and classical methods receive the same geometric control, analytic
conditional bounds and independently trained policies. Both must pay for the
surrogate's mean, residual estimation, exercise-regret control and setup.

## Pre-acquisition gates

1. Derive conditional and unconditional second-moment bounds for the
   arithmetic-minus-geometric payoff residual. Do not replace them by sample
   variances or a pilot maximum. Derive a deterministic interval for the
   continuation value and the resulting exercise-regret envelope.
2. Acquire fresh diagnostics for ALL four previous models and strikes 3,6,9:
   16 independent randomized-QMC replicates, 1024 outer states and 2048 shared
   conditional paths. Root seed 2026092501. Record analytic bounds, conditional
   sample moments, the flat residual and a Jensen upper estimator of regret.
   Any apparent regret from approximate continuation remains an upper-estimator
   diagnostic, not the true regret or a proof of negligible bias.
3. Price with the same controls classically at 8192 outer states, 16 and 256
   inner paths, 32 independent randomizations (root 2026092502). Compare full
   intervals with the independent archived reference. Charge setup and policy
   training. Add fresh-process timing for representative C4 and H8 if useful.
4. Cost the flat residual with a proved global second moment and the repository's
   explicit signed mean-estimation schedule. Also report ideal unit-constant
   query sensitivity, clearly NOT an implemented algorithm or a lower bound.
   Charge existing source and inverse arithmetic. List additional geometric
   control/policy/encoding costs; a favorable omission cannot support a win.
5. A small apparent bias permits a separate fixed-N iid bound experiment only
   if it could change the decision. Its allocation and failure budget must be
   recorded before data acquisition. Fixed-sample confidence is not an anytime
   stopping rule. Floating-point and pseudorandom-generator obligations remain.

Continue to full new circuit compilation only if the complete feasible budget
can plausibly fit, with a proved estimator and explicit unresolved constants.
Stop this construction if even favorable component cost screens miss the
budget materially; this is not a proof against all quantum algorithms.

## Analysis obligations

The outer payoff is a call on the CONDITIONAL mean, not on one path payoff.
Flattening is valid only with the exercise-regret term retained or bounded.
No state-dependent average classical work is automatically a coherent runtime:
variable-time amplification or a fixed padded schedule must be specified.
Geometric-control moment improvements are not claimed as new mathematics.
Latest relevant primary theory and classical prior art must be checked.

Use append-only result directories, save commands, raw replicate summaries,
source hashes, error allocations, tests and reasons for stopping or continuing.
Acceptance is significant quantum-over-classical advantage, not a reduction
relative to our previous quantum schedule.
