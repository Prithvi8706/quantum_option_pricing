# Encoding and sequential-validity discovery protocol

Locally declared 2026-09-15 before circuit profiling or stochastic experiments.
This is new discovery after week 10, not confirmation and not a replacement
for historical archives. Analytic screening of existing bound formulas informed
the choice: removing sinusoidal linearization reduces S by pi*c/2 at c=.125
and removes the encoding allowance, but not support/grid error.

## Hypotheses and fixed design

H1: an exact finite-grid payoff oracle improves dollar delivery versus the
existing linearized oracle under equal shots and separately equal logical CX.
H2: an anytime-valid confidence sequence supports early stopping while keeping
the same model-conditional error allowance; it may cost more than fixed-time CP.
Neither technique is claimed new; integration novelty remains to be established.

Contracts: E001,E014,E025,E030,E038,E049; n=6; c=.125 for old oracle;
support q=1e-5. Exact oracle uses the same point-density PMF, with uniformly
controlled Ry(2 asin sqrt(max(x-K,0)/(U-K))) rotations. No target prices are
used to build the oracle. Exact summation is an explicit classical comparator.
Encoding table length is 64, exponential in n; no scalable QROM claim.

Compile both representations at depths 0,1,2 to u/cx, optimization level 1,
seed 1729, no routing. Check statevector marginal at each depth against the
independent finite-grid amplitude and amplified sine law (absolute <=1e-9).
Only depth 0 is used for delivery experiments to isolate the encoding effect;
depth 1/2 resource profiles are not accelerated-estimator performance evidence.

Readout f=.02, g=.07, fixed independent calibration 16384 shots per state.
Validation rates equal calibration rates; supplied guards 0,.003,.03 remain
assumed allowances. No gate noise, hardware replay or physical-noise claim.
Two resource axes: 32768 pricing shots each; or CX cap equal to 32768 times
the OLD depth-0 CX count for that contract. Each arm takes floor(cap/its CX).
Calibration costs recorded separately, same across arms. 30 replicates per
contract/guard/axis/encoding: 2160 acquisitions, two shared-data inference
outcomes each (4320 inference rows). Distinct streams between encodings and
resource axes: their delivery contrasts are unpaired descriptive differences.

Fixed comparator: CP calibration alpha .025 total and final validation .025.
Sequential comparator: same calibration, Jeffreys beta-mixture Bernoulli
confidence sequence at validation alpha .025. Inspect cumulative observations
at 1024,2048,4096,... below cap and at cap, stop at first $1 declaration;
never re-use a fixed-time CP interval for repeated stopping. Unresolved and
incompatible outcomes remain. B>=1 refuses before acquisition. All generated
paths are simulation data; sequential costs include only the observed prefix,
while fixed and sequential arms share its underlying synthetic path.

Record containment, erroneous $1 declarations, delivery, used shots, total
shots, CX, A-equivalent calls, interval widths and exact-summation error/cost.
No quantum-vs-classical speedup conclusion is possible for 64-term summation.
Promotion screen: exact oracle improves descriptive delivery on at least two
non-E001 contracts at guard zero on both axes, with zero observed erroneous
declarations. Report all guards/contracts even if promotion fails. This is a
discovery screen without significance or universal coverage certification.

Exclusive output, source snapshots, per-record flush, retain failures, no
silent retries. 1800-second between-case budget and 1 GB free disk required.
Numerical CS tests compare double-precision enclosures with 80-digit likelihood
inversion and exact finite-horizon boundary-crossing probabilities. Those
checks support implementation, not formal directed rounding or physical validity.
