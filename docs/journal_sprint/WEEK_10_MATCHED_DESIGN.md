# Matched native/classical feasibility decision

2026-09-15. Design gate, not executed head-to-head or frozen confirmation.

## Concrete minimal comparison

Use E001, n=5, rescaling 0.125, support-tail rule 1e-5, ideal sampling.
Recomputed the representation using `tighter_bounds_for`; all printed bound
fields agree with the saved week-8 menu. Its saved B=0.09302785803773954,
S=55.86951031830576, O=-22.449778809913862 imply
epsilon=(1-B)/S=0.016233758570550587 for a $1 tolerance.
Continuous target: discounted risk-neutral expected call payoff, not expected
terminal underlying value. Encoded target: sum of grid probabilities times
the exact objective-qubit probabilities, mapped by O+S*a.

Classical sampling draws a grid index and evaluates that index's objective
probability in [0,1], not an unnecessary extra Bernoulli measurement.
The fixed-sample Hoeffding bound gives N=ceil(log(2/.05)/(2*epsilon^2))=6999.
It is a conservative baseline, not the best available classical algorithm.
Exact summation over the 32 grid points must also be reported, with preparation
and evaluation costs; a speedup claim against sampling alone is inappropriate.

Native arm: installed `qiskit_algorithms` IQAE accepts epsilon_target, alpha,
confidence method and sampler. The existing smoke uses epsilon=.05, which
does NOT meet this representation's remaining tolerance. A matched run must
use epsilon=0.016233758570550587 and alpha=.05, ideal finite-shot sampling,
the same circuit/encoding, and raw interval mapped once to dollars plus B.
This is a new runner configuration, not a relabeling of old smoke results.

## Coverage and stopping qualification

Inspected local `amplitude_estimators/iae.py`: its beta mode allocates alpha
over a computed maximum round count and can accumulate shots at repeated
powers. We have not established a new proof that every implementation-specific
adaptive look preserves a 95% frequentist guarantee. Native nominal intervals
must not be equated with the fixed-sample bound merely because alpha matches.
Before confirmation, either audit the native stopping argument against the
implementation, or use fresh fixed validation data for an explicitly labeled
modified procedure and account for its entire cost. That procedure is no longer
an unmodified native IQAE benchmark. Bayesian posterior widths also remain
separate from frequentist guarantees.

The original IQAE reference is
[Grinko et al.](https://www.nature.com/articles/s41534-021-00379-1).
The publisher fetch failed during this turn; the assessment above is grounded
in inspected local code, not a claimed fresh full-paper verification.

## Feasibility and decision

The target and classical sample budget are feasible. Existing circuit builders,
grid probabilities and recorded native sampling provide implementation pieces.
There is no completed matched runner or native stopping audit yet. Do not run a
nominally matched accuracy table until this guarantee mismatch is resolved.
Suggested future development smoke: one fixed contract, ten purpose-separated
seeds, 1024 shots per native invocation, 120 seconds and 100000 total shots per
trial; record capped trials as unresolved. These are proposed resource limits,
not approved confirmatory power calculations. Freeze exact settings only after
the stopping decision; never replace failures or tune on confirmation seeds.

Cost ledger must include setup, exact summation, classical evaluations, native
shots, executed powers, A-equivalent calls, logical CX, and failures. Simulator
time is not hardware time. Calibration/pilot entries are zero for this ideal,
fixed-representation comparison; do not hide them when extending to noisy or
adaptive designs. Statistical delivery, containment and midpoint error stay
separate. E001 is a discovered favorable contract, not broad-contract evidence.
