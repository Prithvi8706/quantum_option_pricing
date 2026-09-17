# Restricted results supporting the pricing construction

These propositions formalize what the implementation can claim. Proposition 1
is a corollary of standard unitary contraction and LCU facts, not a new quantum
primitive. Proposition 2 is a conditional optimization identity. Neither is a
quantum-over-classical advantage theorem. Separate AI mathematical reviewer Ampere agreed
with these statements subject to the domain and degeneracy conditions below.

## Proposition 1: sharp normalization on an independent probability cube

Let c_i >= 0, C=sum_i c_i, K>=0, and t range over the whole cube [0,1]^m.
Define f(t)=sum_i c_i*t_i-K. Exclude C=K=0. Among exact block encodings valid
uniformly on this cube with one fixed positive normalization alpha, the minimum
normalization is

    alpha_* = max(K, |C-K|) = C/2 + |C/2-K|.

Suppose each t_i is the zero-state probability of an available preparation V_i.
Then signed LCU of V_i^dagger R V_i, with R=2|0><0|-I, row coefficients c_i/2
and constant coefficient h=C/2-K, attains this normalization in exact arithmetic.

Proof. Any projected block of a unitary is a contraction. Hence alpha must be
at least sup_t |f(t)|. The function ranges from -K to C-K, including both
endpoints, so that supremum is max(K,|C-K|). Each row reflection has projected
entry 2t_i-1; thus

    sum_i (c_i/2)*(2t_i-1) + (C/2-K) = f(t).

LCU with coefficient magnitudes divided by their absolute sum realizes f/alpha_*,
and the absolute sum equals the lower bound. This proves attainment. The
row-indexed preparation can share one reflection through block-diagonal control.
The resulting exact signal is a Hermitian involution, supplying the signal-plane
structure used by the QSP walk; an arbitrary unitary with the same projected
block cannot be substituted without checking that structure.

Within this fixed affine representation, comparing independent coefficients
also forces w_i=c_i/2 and h=C/2-K. That scalar uniqueness does not imply a unique
PREP circuit, unitary extension, or minimum gate count.

The actual basket has t_i(z)=prod_j a_ij(z_j), sharing the same z. It does not
generally attain the independent cube. Example: one constant asset with c=1,
t=1, K=3/4 has actual norm1/4, whereas the universal cube normalization is3/4.
The theorem therefore gives no instance-optimality claim for that basket.
The enclosing independent cube is an expressly enlarged domain: closing the
actual correlated basket support does not generally yield that cube. Attainment
on the cube does not imply attainability on the finite grid. Stored rotations
approximate the exact construction and require
the separate logical error certificate.

Degeneracies: if C=0,K>0 the target is constant -K and alpha_*=K. If C=K=0,
the target is zero: any alpha>0 works and the infimum is zero; division by zero
is not an encoding. Negative row weights are excluded from this proposition
and from the current positive-exponential implementation.

Foundations: [qubitization, Section 3.1](https://arxiv.org/pdf/1610.06546) and
[QSVT, Definition 51/Lemma 52](https://arxiv.org/pdf/1806.01838).

## Proposition 2: normalization and per-query cost must be traded jointly

Assume positive constants g,beta,a,e, independent of continuous degree n, and
the *specified planning proxy*

    W(n) = g*beta*n^2/(e*n-a),  n>a/e.

Here a/n represents approximation error, e the remaining price allowance,
g*n the per-query work and beta/(e-a/n) the query dependence, with fixed
confidence constants absorbed into g. The unique minimum is

    n_* = 2a/e,   W_* = 4g*beta*a/e^2.

Proof by an exact nonnegative difference:

    W(n)-W_* = g*beta*(e*n-2a)^2 / [e^2*(e*n-a)] >= 0.

Equality holds only at n_*. Approximation and statistical allowances each use
e/2. Comparing two encodings with the same e reduces to comparing g*beta*a.
With different e_j, compare g_j*beta_j*a_j/e_j^2. Under the additional common
constants beta proportional to B and a proportional to B, and the same e for
both encodings, reflection improves
this proxy precisely when g_ref/g_orig < (B_orig/B_ref)^2.

For unequal remaining allowances the right side additionally contains
(e_ref/e_orig)^2, under those same proportionality assumptions.

This is not an asymptotic theorem for the implemented algorithm: degree choices
are discrete; beta/residual normalization and other error terms may depend on
degree; AE uses powers of two and caps; loader precision can grow; physical costs
are unspecified. The four archived polynomial degrees do not prove a universal
a/n law. Ordinary calculus of this proxy is not a field-wide novelty claim.

## Proposition 3: finite-menu decision and the limit of projected ratios

For a fixed menu, let E_j be justified deterministic bounds and S_j the AE price
bound under its exact logical model. Feasibility requires E_j+S_j<=epsilon,
with the confidence condition and resource cap also satisfied. Exhaustive
selection of the smallest stated composition cost among feasible entries
minimizes that cost function over this menu. It proves neither optimality over
unlisted constructions nor minimum physical cost. A null physical error entry
cannot satisfy a physical-delivery claim.

Moreover, if actual costs T_j <= U_j, the ordering of upper projections U_j
does not establish the ordering of T_j. For example, U_orig=200,U_ref=100 and
T_orig=10,T_ref=90 satisfy both upper bounds but reverse the ranking. Therefore
the reported ratios compare conservative composition formulas. They are not
certified speedup factors or upper/lower bounds on optimized physical ratios.

## Implementation correction discovered during review

The frozen ReflectionSignal constructor classifies a constant enclosure
[-epsilon,0] as nonnegative. A reproducer is means=[-1e-80], factor=[[0]],
strike=.5, q=1,L=1, which yields [-1E-80,0E-80]. Use a negative sign when the
lower endpoint is negative and the upper endpoint is nonpositive; exact zero
has zero weight and is harmless with either sign. Strictly straddling intervals
continue to be rejected.

`reviewed_reflection_signal.ReviewedReflectionSignal` implements that rule as
an explicit new version, using the inherited constructor and circuit adapter.
The archived producers remain unchanged for exact provenance. The correction
does not change coefficient magnitudes or PREP bounds. Its tests cover the
reproducer, exact zero, both signs and projected-block/involution identities.
This is an edge-case proof/implementation repair; it is not evidence that an
archived total operator bound was exceeded. The four W2 production contracts
have strictly positive centered constants, far from the problematic endpoint.
