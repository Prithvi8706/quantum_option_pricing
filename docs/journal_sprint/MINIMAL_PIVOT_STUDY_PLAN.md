# Minimal-pivot study: two weeks, separate from historical weeks 14/15

User mandate: original research contribution, substantial quantum-method
improvement if supported, and the least possible change to the pricing problem.
Journal quartile/acceptance is not an experimental outcome we can guarantee.

Historical status: weeks13/14 merged; week15 reproduction complete, its
confirmation campaign explicitly blocked. Call this study W1/W2, not a
retroactive completion of that campaign.

## Study week 1: construction and bounded feasibility (this work package)

1. Keep arithmetic Asian basket, constant-parameter risk-neutral GBM, existing
   Gaussian factor model, strike100, cutoff4 and cell-midpoint finite encoding.
2. Derive a reflection-centered encoding of A-K that avoids enumerating the
   centered coordinate subsets. No change to the option or averaging rule.
3. Implement it and an equally multiplexed original encoding as a strong quantum
   control. Preserve the previous subset encoding and all old archives.
4. Check good blocks, full unitarity/involution, controlled phase conventions and
   short QSP walks on bounded circuits. Derive an ideal logical signal-operator
   certificate including coefficient/angle preparation and compiler rounding.
5. Predeclare resource grid: d=2,4 and q=1,2 for compiled original/new circuits;
   subset comparison only d2/q1 (cost cap). Structural d=4,8,16 and q10 plans,
   plus a full d4/q10 new-circuit compilation. No joint path enumeration there.
6. Reuse archived minimax certificates at degrees16,32,64,128 to compare uniform
   payoff error envelopes at the same degree and common error-target query-cost
   proxies. These are not full runtime/AE claims. Keep losses as well as wins.
7. Tests, separate-environment replay, log results and an explicit W2 decision.

This is adaptive development; protocol is written before the new acquisition,
after algebraic inspection of prior results. Not statistical preregistration or
independent confirmation. Fixed bounded scope prevents endless favorable tuning.

## Study week 2: application validation and contribution decision (not started)

Development amendment after the first acquisition: add an equally multiplexed
centered-subset baseline on d=2,4 and q=1,2. This prevents attributing a compiler
improvement to the reflection construction. Preserve v1 acquisitions; v2 uses
the stored binary radius consistently in scalar error envelopes and removes
unused imports. The added baseline is adaptive, not predeclared confirmation.

1. Freeze surviving construction and its original-encoding control. Integrate
   probability loading, scalar offset, payoff transformation and AE schedule.
2. Complete dollar-level accounting for that implemented pipeline, explicitly
   distinguishing exact logical gates from synthesized/fault-tolerant execution.
3. New development-to-confirmation split over basket sizes, volatility,
   correlation and strikes; do not call reused cases held out.
4. Compare against conditional RQMC and classical controls with matched continuous
   target, tolerance and confidence. Count classical setup and oracle inverses.
5. Ablate normalization versus compilation versus reflection centering. Compare
   published approaches only where targets/resource conventions genuinely match.
6. Extend prior-art search around the precise construction, not generic finance.
   Novelty is provisional until that search and independent expert review.
7. Go/no-go: advance a supported resource/error theorem or measured improvement;
   claim classical advantage only if the complete comparison supports it. No
   silent pivot to an easier comparator or different payoff if the candidate loses.

## Candidate derivation to test

Write A(z)=sum_i c_i*prod_j a_ij(z_j), with c_i>0 and 0<=a_ij<=1,
c_i=exp(mu_i+L*sum_j|F_ij|)/d. Let C=sum_i c_i and h=C/2-K.
For each row a product of RY rotations prepares probability prod_j a_ij on
all-zero signal ancillas. Reflect about those all-zero ancillas and unprepare;
the good block is 2*prod_j a_ij-1. LCU coefficients c_i/2 and h therefore give
A-K with scale B=C/2+|C/2-K|=max(K,C-K), rather than C+K.

Do not implement a separate controlled reflection per row: multiplex the row
preparations, apply one signal-ancilla reflection, and unprepare. A negative
constant coefficient needs its index phase. This shares the reflection and
retains only d+1 coefficient slots, not 1+d*(2^d-1).

The probability-to-reflection and LCU primitives are established techniques.
The research candidate is their explicit, certified, low-cost realization for
this separable basket and the resulting error/resource tradeoff—not invention
of reflection or LCU. Multiplexing controls must also be given to the baseline.
