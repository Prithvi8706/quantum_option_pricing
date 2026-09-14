# Week 4 finite-readout-calibration discovery protocol

Declared before execution. Stationary response-level model, independent shots,
perfect preparation of calibration states 0/1, and the same readout rates in
calibration and validation. None of these assumptions is hardware-verified.
True false-positive f=.02 and false-negative g=.07 are simulation inputs only.

At fixed Grover depths (0,1,2), the ideal response is
`p_k(a)=sin²((2k+1)asin(sqrt(a)))`, and the reported response is
`q_k=f+(1-f-g)p_k`. No amplitude damping or gate-noise model is asserted.

## Uncertainty propagation

Allocate total error .05 as .025 calibration plus .025 validation. Two
Clopper–Pearson calibration intervals each use failure .025/2. Three validation
intervals each use .025/3. With calibration rectangles [fl,fu] and [gl,gu],
if `fu+gu<1`, all responses lie between
`fl+(1-fl-gu)p` and `fu+(1-fu-gl)p` for p in [0,1]. Hence response interval
[ql,qu] implies the outer interval
`[(ql-fu)/(1-fu-gl), (qu-fl)/(1-fl-gu)]`, intersected with [0,1].
Invert every sine branch and intersect across depths. Treating the common
calibration rectangle independently per depth is a conservative relaxation.
If positive contrast cannot be certified, return the full amplitude interval,
not a fabricated precise estimate. Empty inversions are incompatibility.

On simultaneous calibration/validation containment the true amplitude remains
in the result. A union bound gives unconditional miscoverage at most .05 under
the model and exact conservative inversion. Floating-point padding is not
formal numerical certification. This does not guarantee correctness conditional
on a precision declaration, or transfer under drift/preparation errors.

## Matrix and comparisons

Amplitudes .1/.4/.8; calibration shots per prepared state 256/4096; validation
shots 1024 per depth; 200 repetitions per cell. Total: 1200 independent datasets.
Each stores both calibration counts and all validation counts. Reuse the same
observations for three analyses: true-known readout (.05 validation budget),
plug-in estimated readout (.05; illustrative, not guaranteed), and finite-
calibration conservative inversion (.025+.025). Known-rate analysis is an
oracle diagnostic, not a deployable calibrated algorithm.

Record every confidence-set component, containment, radius, incompatibility,
calibration rectangle and seed key. Report per-cell coverage counts, not pooled
IID binomial inference across heterogeneous amplitudes. No precision threshold
is selected from these outcomes. There are 3072 validation shots and 9216
validation A-equivalents per dataset. Add 512/8192 calibration shots separately:
they are simple state-preparation/readout operations, not pricing-A calls.
Calibration may not be amortized over hypothetical future jobs.

These budgets are a plumbing/discovery check, not high-confidence empirical
certification of a 95% rate. Compare interval width and calibration cost without
promising that uncertainty-aware correction will outperform an oracle.
