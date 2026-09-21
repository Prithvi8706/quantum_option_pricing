# Signed residual arithmetic: implemented method and certificate

Date: 2026-09-21. This is a method note for the separate bounded development
study governed by the [signed residual protocol](SIGNED_RESIDUAL_PROTOCOL_20260921.md).
It contains no acquisition results, winning configurations, or performance claims.
It does not amend the frozen primary study or imply human review, confirmation,
physical execution admission, or quantum-over-classical advantage.

## Target, constants, and executable interface

The target remains the discounted arithmetic Asian-basket call. On the ideal
finite midpoint model, write

\[
A(z)=\frac1d\sum_{i=1}^d \exp(\mu_i+F_i z),\qquad
V_q=D\,\mathbb E_q[(A-K)_+].
\]

The independent normal coordinates have exact normal cell masses conditional
on the cutoff cube and exact cell midpoints. Production uses cutoff 4 and q10.
The continuous-to-finite representation allowance remains that of the matching
raw-payoff parent; the control identity below does not change the target.

All archived binary64 model parameters, radius, and polynomial coefficients are
interpreted as their exact binary values. The control and parent arithmetic both
use signed width 48 and fractional precision 24, with \(Q=2^{24}\), \(u=Q^{-1}\).
The fixed exponential menu is degrees 8, 12, 16 crossed with reduction exponents
1, 2, 3, separately for D1 and D2. The control evaluator does not select a
precision based on acquisition outcomes.

The authoritative implementations are
[residual.py](../../research/stronger_arithmetic/residual.py),
[residual_circuits.py](../../research/stronger_arithmetic/residual_circuits.py),
[residual_components.py](../../research/stronger_arithmetic/residual_components.py),
and [run_residual.py](../../research/stronger_arithmetic/run_residual.py).
The parent [range-reduced certificate](../../research/stronger_arithmetic/budget.py)
supplies a per-spot, undiscounted error bound \(E\), along with integer sum and
post-strike bounds. Thus \(|\widehat A-A|\le E\).

`residual_plan` reconstructs the parent certificate for the supplied model and
compares its required fields using canonical JSON. Tuple/list serialization
differences are permitted; booleans are not interchangeable with numbers.
The separately produced offset certificate is trusted mathematical evidence,
with its model, q, cutoff, strike, radius, and low-polynomial binding checked.
Checking that binding is not a replacement for generating or replaying the
offset enclosure and checking archive provenance.

## Exact control identity and uniform signed bound

Let the archived degree-four Chebyshev polynomial be
\(p_4(x)=\sum_{k=0}^4 c_k T_k(x)\), and set

\[
x=(A-K)/B,\qquad g(x)=\frac{x+p_4(x)}2,\qquad C(A)=B g(x).
\]

The certificate first proves \(|A-K|\le B\) on the entire cutoff cube, using
outward exponential bounds on each spot and summing them. Consequently
\(|x|\le1\). The exact monomial coefficients \(b_k\) of \(g\) are

\[
(b_0,b_1,b_2,b_3,b_4)=
\left(\frac{c_0-c_2+c_4}{2},\frac{1+c_1-3c_3}{2},
c_2-4c_4,2c_3,4c_4\right).
\]

They are constructed as rational numbers before quantization. The true residual
is

\[
r(A)=(A-K)_+-C(A)=\frac B2\bigl(|x|-p_4(x)\bigr).
\]

The exact Chebyshev coefficients of the degree-four truncation of \(|x|\) are
\((2/\pi,0,4/(3\pi),0,-4/(15\pi))\). Since \(|T_k(x)|\le1\) on
\([-1,1]\), the stored-coefficient discrepancy contributes at most
\(\eta=\sum_{k=0}^4|c_k-c_k^*|\). The omitted tail telescopes:

\[
\sum_{j=3}^{\infty}\frac4{\pi(4j^2-1)}=\frac2{5\pi}.
\]

It follows that

\[
|r(A)|\le B\rho,\qquad \rho=\frac1{5\pi}+\frac\eta2.
\]

The implementation evaluates this expression with directed intervals. This is
a universal residual-magnitude bound used for encoding, not an additive pricing
bias: the residual is estimated, rather than discarded.

An exact domain witness for the archived polynomial is
\(r(K)/B=-(c_0-c_2+c_4)/2<0\); at \(x=1\) the normalized residual is
\((1-\sum_k c_k)/2>0\). Thus a universal residual oracle cannot clip negative
residuals or reinterpret them as unsigned integers. These algebraic witnesses
do not assert that either point is a reachable node of every finite grid.

## Integer map emitted by the control oracle

The input `sum_integer` is the sum of the parent's spot integers, not the
averaged basket. Define exact integer constants

\[
k=\left\lfloor\frac{Q}{dB}\right\rfloor,\qquad
a_j=\lfloor Qb_j\rfloor,\qquad S=\lfloor QdB\rfloor.
\]

The required order of operations is:

```python
t = sum_integer - d * K * Q
x_int = t * k // Q
y = a[4]
for j in (3, 2, 1, 0):
    y = x_int * y // Q + a[j]
control_int = y * S // Q
payoff_int = max(t, 0)
residual_int = payoff_int - control_int
threshold_int = residual_int + H
```

Every `//` is signed floor division, including negative products. The five
coefficients describe the complete \(g\): there is no additional linear term
or halving after Horner. The final scale multiplication is quantized and rounded;
it is not the exact integer spot multiplication used inside the parent.

`evaluate_control_integer` is the unbounded integer reference. The gate kernels
perform modular arithmetic and agree with this reference when the signed range
certificate passes. `residual_components` wraps the delta-input kernel with
sum-to-post-strike subtraction and its inverse, so the external sum register is
restored. All control intermediates, the shift, and comparison work are uncomputed.

## Error certificate for the implemented evaluator

Let \(\epsilon_k=|k/Q-1/(dB)|\). Since
\(t/Q=d(\widehat A-K)\), the normalization error is bounded by

\[
\Delta_x=\frac EB+d(B+E)\epsilon_k+u.
\]

Proof: replacing \(A\) by \(\widehat A\) contributes \(E/B\); reciprocal
quantization contributes at most \(|t/Q|\epsilon_k\), with
\(|t/Q|\le d(B+E)\); the floor-rescaled multiplication contributes less than
\(u\). Set \(R=1+\Delta_x\). Both the true input and its implemented
approximation, and the line segment between them, lie in \([-R,R]\).

For coefficient errors \(\delta_j=|b_j-a_j/Q|\), propagate

\[
h_4=\delta_4,\qquad h_j=R h_{j+1}+u+\delta_j\quad(j=3,2,1,0).
\]

Then \(h_0\) bounds the fixed Horner error relative to \(g\) at the implemented
input. A derivative bound and polynomial-magnitude bound are

\[
L_g=\sum_{j=1}^4 j|b_j|R^{j-1},\qquad
G=\sum_{j=0}^4|b_j|R^j.
\]

Let \(\epsilon_S=|S/Q-dB|\). The sum-scaled control error is

\[
E_C=dB(L_g\Delta_x+h_0)+\epsilon_S(G+h_0)+u.
\]

To see the scale term, write the pre-rounded result as
\((S/Q)\widehat g\). Its difference from \(dB g(x)\) is bounded by
\(dB|\widehat g-g(x)|+|S/Q-dB|\,|\widehat g|\), and
\(|\widehat g|\le G+h_0\). The last multiplication adds at most \(u\).

Positive part is 1-Lipschitz. Its sum-scaled payoff error is therefore at most
\(dE\), even if the parent approximations are signed. The sum-scaled residual
error is

\[
E_R=dE+E_C.
\]

This proves
\(|R_{\rm int}/Q-d r(A)|\le E_R\). The discounted per-basket arithmetic allowance
is \(D E_R/d\), evaluated upward. Parent arithmetic is already included here and
must not be added again in the completed price budget.

## Universal overflow and shifted selector proof

The certificate checks signed width 48 for every retained word and width 96 for
each full multiplication product. Products use all four endpoint combinations;
floor division is monotone, so endpoint division gives valid retained intervals.
The multiplication result is checked before each coefficient addition.

The parent sum, strike, and post-strike intervals are checked first. The
post-strike interval is tightened by intersecting it with an independently
derived true basket-support interval enlarged by the parent error. Integer
lower bounds use ceiling and upper bounds use floor. Direct interval propagation
then covers normalization, Horner, scale multiplication, and positive part.

For the residual subtraction, intersect its direct interval with
\([-J,J]\), where

\[
J=\left\lfloor\operatorname{upper}\{Q(dB\rho+E_R)\}\right\rfloor.
\]

Using floor is safe because the quantity being bounded is an integer. This
intersection uses an independently proved analytic bound; it does not assume
absence of overflow in the modular circuit. Establish the unbounded reference
range first, then conclude that the modular subtraction has that signed value.

The implementation chooses \(H=2^{\operatorname{bitlength}(J)}\), including
\(H=1\) when \(J=0\), and \(m=\operatorname{bitlength}(H)\). Hence

\[
|R_{\rm int}|\le J<H,\qquad
0<R_{\rm int}+H<2H=2^m.
\]

The shift constant and shifted result must also fit their signed word, and
\(m<48\). Any failed range check makes the certificate infeasible. The circuit
can support a broader unsigned numerator interface, but this study uses the
stronger signed-word certificate.

For a uniform m-bit selector U, a clean comparator encodes

\[
a=\Pr[U<R_{\rm int}+H]=\frac{\mathbb E[R_{\rm int}]+H}{2^m}.
\]

This identity is exact; it introduces no threshold discretization allowance.

## Offset acquisition, model binding, and decoding

Let \(D_0\) be the exact binary64 discount used for the archived classical
control. The matching q10 reflection offset \(O\) is re-certified against
\(D_0\mathbb E_q[C(A)]\) using
[directed finite-model moments](../../research/journal_sprint/control_offset_enclosure.py).
The moments expand the basket powers through degree four without enumerating
the production product grid. The offset certificate records the resulting
expectation interval, the discrepancy of the actual chosen float O, and its
classical preparation work.

The arithmetic parent's real discount D may differ from \(D_0\). Charge

\[
E_{\rm offset}=|O-D_0\mathbb E_q[C(A)]|,\qquad
E_{\rm bridge}\le |D-D_0|\,B\sum_{j=0}^4|b_j|.
\]

The latter follows from \(|x|\le1\), not from the enlarged implementation domain.
An archived offset is not used without re-enclosure. The runner checks that its
chosen q10 reflection offset is common to the archived degree menu. Diagnostics
at q1 and q2 acquire their own finite-model expectations; reusing q10's offset
there would change the target.

The ideal affine decoder for an amplitude a is

\[
\alpha+La,
\qquad \alpha=O-\frac{DH}{dQ},\qquad L=\frac{D2^m}{dQ}.
\]

The implementation stores binary64 constants \(\widehat\alpha,\widehat L\) and
performs the two operations `intercept + scale * amplitude`. For a supplied
binary64 amplitude in [0,1], its certificate charges

\[
E_{\rm decode}\le
|\widehat\alpha-\alpha|+|\widehat L-L|
+8\,2^{-52}(|\widehat\alpha|+|\widehat L|)+2^{-1022}.
\]

The constant discrepancies are outward-enclosed; the remaining terms
conservatively cover the two binary64 operations, including subnormal error.
Conversion of another amplitude representation into binary64 is a separate
obligation. The study's ideal AE-label convention does not certify native
phase estimation, finite-precision trigonometric decoding, or hardware noise.

## Completed ledger and statistical convention

`deterministic_partial_upper` contains arithmetic, offset, discount bridge, and
decoder allowances. `complete_budget` adds the matching parent's continuous
representation allowance and the product-loader allowance

\[
E_{\rm prep}=2 L_{\rm upper} d\epsilon_{\rm loader}.
\]

The tensor-product preparation error is at most \(d\epsilon_{\rm loader}\),
and probability perturbation is bounded by twice that state error. The constant
decoder offset contributes no additional loader sensitivity. Ripple aggregation
and the stated logical X/CX/CCX arithmetic are exact in this ideal model; native
and physical implementation errors remain unknown, not experimentally zero.

With total deterministic allowance \(E_{\rm det}\), the existing
[rational AE schedule](../../research/journal_sprint/claim_assessment.py) chooses
a power-of-two M satisfying

\[
L_{\rm upper}\left(\frac{\pi}{M}+\frac{\pi^2}{M^2}\right)
\le 1-E_{\rm det}.
\]

It retains the declared 17-repetition confidence convention and call cap.
Insufficient deterministic margin, query-cap failure, failed overflow, missing
parent component evidence, and resource-cap failure are distinct statuses.
Feasibility of this ledger is not a claim of physical implementation accuracy.

## Finite diagnostics and resource evidence

The runner enumerates q1/q2 scalar grids for every declared configuration. It
checks the integer threshold range, the implemented residual against the exact
payoff-minus-control expression evaluated numerically, and the restored
expectation against the same finite call target. Coordinate zero occupies the
low-order input bits, consistently with the affine plan.

These diagnostics use binary64 exponentials, polynomial evaluation, CDF-derived
weights, and finite sums, with a numerical comparison tolerance. They are not
directed proofs, statistical AE samples, or continuous-price experiments. Their
universal justification comes from the independent certificate above. The
observed pointwise residual discrepancy is per basket, whereas the certificate
field `residual_sum_error_upper` is sum-scaled and must be divided by d before
comparison. A report must preserve that unit distinction.

Resource composition replaces the parent's post-strike/positive-part/comparator
segment with the emitted signed-control oracle. Conversion and aggregation
counts are inherited only from exactly matched primary plans, including their
inverses. The new complete oracle includes sum-to-delta conversion and reversal,
normalization, control, positive part, subtraction, shift, comparison, and cleanup.
Loader gates and selector Hadamards are added separately before the common AE
projection. Allocated conversion and oracle workspace is retained in the width
ledger. Residual depth is a conservative composition upper bound, not the
primary route's measured remapped dependency depth.

Missing primary component evidence can block a residual cost row even when its
error/query certificate passes. That is an evidence/implementation limitation,
not a mathematical impossibility result. Comparisons must retain all declared
rows, failures, ties, and the distinction between pairwise residual/reflection
comparison and an overall minimum including primary arithmetic.

This note supplies mathematical derivations and implementation scope only.
Acquisition manifests, replay coverage, emitted gate evidence, and independent
review must be reported by their actual artifacts. No human review or external
contact is asserted or initiated by this method.
