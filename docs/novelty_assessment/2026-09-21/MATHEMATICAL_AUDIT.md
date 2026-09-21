# Mathematical audit and certificate disposition

Date 2026-09-21. The detailed independent derivations, inspected implementation
files and primary theorem locations are in
[MATHEMATICAL_REVIEW.md](reviews/MATHEMATICAL_REVIEW.md). This document records
the conclusions the project should use. It is not formal verification of the
entire codebase or a claim of human mathematical review.

## Restricted results

1. **Independent-cube normalization.** For c_i≥0, K≥0, C=sum c_i and
   `f(t)=sum c_i t_i-K` on the *whole independent cube*, excluding C=K=0,
   the minimum exact fixed normalization is
   `max(K,|C-K|)=C/2+|C/2-K|`. Contraction gives the lower bound; row-reflection
   LCU with coefficients c_i/2 and C/2-K attains it. Shared block-diagonal
   conjugation retains the needed involution. This specializes standard
   LCU facts, not a new primitive. With fixed t=1, C=1, K=3/4 the actual
   norm is 1/4 while cube normalization is 3/4: instance optimality is false.
   Negative weights are outside scope; the all-zero target needs no division.
2. **Continuous planning proxy.** With fixed positive g,beta,a,e,
   `W(n)=g beta n²/(en-a)`, n>a/e, has minimum at n=2a/e and value
   `4g beta a/e²`; the documented nonnegative-difference proof is correct.
   Discrete degree, dyadic M, precision changes and degree-dependent constants
   prevent treating it as the implemented algorithm's complexity theorem.
3. **Finite-menu selection.** A minimum among feasible rows optimizes only
   its supplied objective/menu. If actual costs T_i≤U_i, ordering U_i does
   not order T_i: U=(200,100), T=(10,90) is an exact counterexample.

These statements are useful correctness results but cannot support the
proposed work as a new abstract-theorem paper. See the
[frozen restricted propositions](../../journal_sprint/CLAIM_THEOREMS_20260917.md).

## Signed residual chain

For `x=(A-K)/B`, `g=(x+p4)/2`, the exact residual is
`r=(A-K)+-Bg=B(|x|-p4)/2`. The Chebyshev tail and exact stored-coefficient
bridge give `|r|≤B rho`, with `rho=1/(5pi)+eta/2`.
**This is normalization, not an additive approximation bias.** The residual
is estimated and the control expectation restored. At A=K the residual is
strictly negative for the stored polynomial; clipping or unsigned
reinterpretation would change the target. That witness need not be a
reachable grid point to refute a universal unsigned construction.

The arithmetic input is the *sum* of d spot words. Every signed division
floors, including negative products. Reciprocal quantization and input error
give `Delta_x=E/B+d(B+E)epsilon_k+1/Q`. On `R=1+Delta_x`, Horner rounding
and coefficient discrepancies give h0; derivative/magnitude sums give Lg/G.
The control error is
`E_C=dB(Lg Delta_x+h0)+epsilon_S(G+h0)+1/Q` and the residual error is
`E_R=dE+E_C`. The discounted per-basket allowance is `D E_R/d`.
Parent error is already included; adding it again double counts, while
dropping the d-unit conversion can undercount. Current records use correct units.

Full signed 96-bit products and 48-bit retained words are checked before
coefficient addition. The analytic residual bound and direct integer bounds
are intersected for an unbounded reference before concluding no modular
overflow. Integrality justifies `J=floor(upper Q(dB rho+E_R))`.
`H=2^bitlength(J)>J`, including J=0, and `2^m=2H` ensure the selector lies
strictly within range. A uniform comparison gives exactly
`a=(E[R_int]+H)/2^m`; it adds no threshold discretization bias.

The offset certifies the same q10 finite-model control expectation, with a
separate D-versus-D0 discount bridge. The decoder restores it as
`O-DH/(dQ)+D2^m a/(dQ)`. Binding checks alone cannot make an arbitrary offset
certificate true; the actual archive supplies re-enclosure and provenance.
The q1/q2 diagnostics use their own offsets and are not continuous-price proof.

## Range reduction, preparation and AE

The shift obeys `0≤X/(2^s Q)-floor(X/2^s)/Q≤(2^s-1)/(2^s Q)` for either
sign. Taylor/coefficient/floor errors propagate through each square as
`2Be+e²+1/Q`, then through exact integer spot multiplication. All product,
sum, poststrike and selector ranges are checked; merely checking the final
payoff would be insufficient. Shared scratch is reused only after coherent
cleanup. Small basis/phase tests supplement this argument, not replace it.

A product-loader state error is bounded by d times a marginal error, and
probability error by twice the state error; the affine slope L gives
`2L d epsilon_loader`. The constant offset creates no loader sensitivity.
Representation error covers the continuous Gaussian-to-finite-model bridge.
It does not address continuous monitoring or physical errors.

Canonical AE has uniform bound `pi/M+pi²/M²` by BHMT Theorem 12. Seventeen
independent trials with conservative per-trial success .8 have median failure
at most `exp(-.18*17)<.05`. The independent exact binomial calculation is
0.0025814628368384, but no archived schedule was retuned to use it. Logical A,
its exact inverse, ideal controlled powers/QFT and independence are assumptions.

## Consequential issue found and repaired outside frozen producers

The frozen residual decoder certifies its affine constants and two binary64
operations **given a binary64 amplitude**. BHMT supplies an exact real
`sin²(pi*y/M)` label. That conversion was not certified by the frozen
interface, even with perfect quantum gates. Its abstract exact-label resource
plans remain meaningful; complete executable binary64 delivery required more.

The opt-in [adapter](../../../research/assessment_20260921/label_bridge.py)
uses the existing directed trigonometric enclosure, checks the actual float's
distance from it and encloses the median through sorted endpoints. An added
allowance `L_upper*eta` composes with the existing decoder budget. This is
not a physical-noise allowance or a retroactive edit to acquisition evidence.

Under the [pre-execution bounded protocol](LABEL_BRIDGE_PROTOCOL.md), all
384 possible labels for M=128/M=256 and all 18 original schedules pass.
[Final receipt](provenance/label_bridge_v2.json): added allowance is about
1.7020e-15 dollars in D1 and 3.4159e-15 in D2; the smallest remaining margin
is about $0.0230714. No M, circuit count or ranking changes. The reviewer
requested a lower-pi bound to reject previous M; the final verifier uses it.
The original source/receipt remains in history, clearly superseded for that
minimality wording. Nineteen targeted tests passed in the pinned environment:
15 new adapter tests and four existing decoder tests.

## Evidence and residual uncertainty

Independent exact-rational reconstruction checked all 18 residual rows;
the fixed diagnostic menu checked 1,332 q10 nodes, with no violation.
[Protocol](reviews/math/PROTOCOL.md),
[script](reviews/math/check_certificates.py),
[receipt](reviews/math/independent_checks.json) distinguish fresh deterministic
checks from prior producer replay. The review analytically inspected parent,
model and offset mechanisms, but did not independently recompute every
historical representation/QSP-phase theorem or simulate every production circuit.

Nominal Taylor degree 12/16 pairs quantize to the same coefficients (effective degree 9
at f=20 and 10 at f=24). Their remainder bounds can differ, but treating them as
independent circuit families is incorrect. Physical/native synthesis remains
unbounded. Classical replicate t intervals remain approximate diagnostics.
No test count, directed replay or AI review closes these limitations.
