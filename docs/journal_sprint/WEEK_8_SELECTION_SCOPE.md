# Week 8: what paid selection can and cannot claim

This is a scoped argument for the declared interface, not a new generic
amplitude estimator, formal floating-point certificate or hardware validation.

## Observable choice and fixed validation

The deterministic menu is built from contract parameters, analytical bounds and
compiled resource profiles. It contains no exact option price or amplitude.
The ranking function accepts exactly `{n, radius}` per candidate, where radius
is the pilot confidence-set hull transformed to dollars with the deterministic
bound added. Empty hulls rank worst; ties pick n5. That radius is not a forecast
of final precision. Equal pilot shots have unequal CX costs, and the remaining
validation allocation also differs by representation.

Let H denote the complete pilot history. Once H is fixed, the selected candidate
and its final shot counts are fixed. If fresh calibration and fresh binomial
validation draws satisfy the declared model conditional on H, the existing
calibration (.025) plus validation (.025) construction applies to that one fixed
choice. It does not need a union bound over candidates for the **single fresh
final interval** merely because an independent pilot selected the candidate.
This reasoning depends on actual conditional independence and a valid supplied
transfer allowance for every final depth, not on a good pilot fit.

The synthetic implementation separates pilot/final and calibration/validation
seed namespaces. It writes the pilot observations, score, choice and final
schedule as a durable event before requesting final counts. Exact targets are
used only by the simulator to produce draws and by outcome diagnostics; the
ranking function never receives them. Replay checks event/data agreement, while
source order and tests check the callback precedes final acquisition. Local
hashes do not independently certify real-world chronological preregistration.

## Declared precision versus coverage

In exact arithmetic under the model and deterministic-bound assumptions, price
containment plus final radius <=$1 implies midpoint error <=$1. Thus erroneous
$1 declaration is a subset of noncontainment, but the converse need not hold.
The resulting per-procedure argument is not 95% correctness **conditional on
delivery**, nor simultaneous coverage of all benchmark cells. Numerical padding
has not been formally certified. No pilot interval is substituted for a final
interval, and no failed or empty final interval triggers a retry.

## Cost and contribution limits

The equal cap applies to pricing CX across pilot plus final circuits. Selected
procedures can spend 49152 calibration shots versus a fixed policy's 32768.
Final acquisitions, pilot acquisitions and procedure attempts have distinct
denominators; max depth/qubits are maxima, not sums. Classical setup and synthetic
run time are recorded separately, not converted to quantum gate advantage.

A changed delivery rate is evidence about this small declared policy/menu/model.
It is not proof of an optimal allocation, a superiority claim over native
BAE/BIQAE, a classical-pricing speedup or a journal-worthy new estimator.
If the readiness screen fails, keep the result and narrow the contribution
rather than retrospectively changing guard widths, menu or success criteria.
