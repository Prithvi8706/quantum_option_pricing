# Controlled policy residual: derivation and access-model obligations

## Financial contract and notation

Let tau=T/2, d0=exp(-r*tau), d1=exp(-r*(T-tau)), a be the accrued
contribution to the complete arithmetic average, and A,G be equal-weight
arithmetic/geometric averages of FUTURE asset fixings. In this project's
contract exactly half the fixings are future. Set q=d1/2 and k=2(K-a).
Then H=q(A-k)+, the geometric call is Hg=q(G-k)+, C=E[H|X], and the
compound price is d0 E[(C-Kc)+]. Brownian increments are simulated exactly
at contractual dates. No artificial time-discretization hierarchy is added.

## First control and proved moments

For capped H and Hg, D=H-Hg is nonnegative because A>=G. The capped call
map is q-Lipschitz, so 0<=D<=min(B,q(A-G)). Thus

    E[D|X] <= q(E[A|X]-E[G|X]),
    E[D^2|X] <= min(B^2,q^2 E[(A-G)^2|X]).                 (1)

All spread moments are analytic. For lognormal components exp(Z_i), equal
weights 1/m, Gaussian means mu_i and covariance Sigma, write
muG=mean(mu), vG=mean(Sigma), c_i=mean_j Sigma_ij. Then

    E[A^2] = mean_ij exp(mu_i+mu_j+(Sigma_ii+Sigma_jj)/2+Sigma_ij),
    E[AG]  = mean_i exp(mu_i+muG+(Sigma_ii+vG)/2+c_i),
    E[G^2] = exp(2muG+2vG),
    E[(A-G)^2] = E[A^2]-2E[AG]+E[G^2].                   (2)

Conditional moments use exercise spots and FUTURE elapsed times. Unconditional
moments use initial spots and ABSOLUTE future fixing dates, including pre-tau
uncertainty. Mixing those time origins would invalidate the global bound.
`test_bounds.py` checks the tower identity independently.

The first control also supplies continuation bounds. A lower bound is the
conditional geometric capped call. Jensen supplies an arithmetic uncapped
intrinsic lower bound, minus an upper bound on the cap tail. Jensen supplies
an upper call bound by the average individual future-asset call prices.
Intersect these with [g, min(B,g+q E[A-G])]. One cannot apply convex Jensen
directly to the capped call, because it is not convex globally.

## Parity improvement for the original, uncapped contract

Define F=q(E[A|X]-k), Pg=q E[(k-G)+|X], and

    R=q[(k-G)+-(k-A)+].

Put-call parity gives the exact conditional identity

    C = F+Pg-E[R|X].                                    (3)

Since A>=G, R>=0. Accrued a>=0 and G>=0 imply

    0<=R<=q(k-G)+<=d1*K=:Bput.                          (4)

This bounded residual works directly for the UNCAPPED price, despite the
unbounded lognormal underlying. It does not bound the full price or the
surrogate, nor remove the finite-input quantum implementation obligation.

Let c0=F+Pg. We construct a deterministic interval

    L=max(0,F,g) <= C <= U=min(c0,individual-call upper) .(5)

Clip the fixed continuation approximation V into [L,U]. Hence
0<=h=c0-V<=Pg<=Bput. The conditional complement moment satisfies

    E[R^2|X] <= min(q^2 E[(A-G)^2|X],q^2 E[(k-G)+^2|X]). (6)

For lognormal G, mu=E[log G], variance v and z=(log k-mu)/sqrt(v),

    E[(k-G)+^2] = k^2 Phi(z)-2k exp(mu+v/2)Phi(z-sqrt(v))
                  +exp(2mu+2v)Phi(z-2sqrt(v))            (7)

when k>0, and zero otherwise. This is a population formula, not an empirical
fit. Real-arithmetic derivations do not automatically certify floating-point
evaluation of cancellations in these expressions.

## Flattening and its non-removable regret term

For d=1(V>Kc), define Y=d(h-R), and

    regret = (C-Kc)+ - d(C-Kc) >= 0.

Because (V-Kc)+=d(V-Kc),

    P=d0 { E[(V-Kc)+] + E[Y] + E[regret] }.              (8)

Only the first two terms are nonnested. Omitting regret without a bound changes
the financial target. For C in [L,U],

    regret <= d(Kc-L)+ +(1-d)(U-Kc)+.                    (9)

The interval identifies states where the policy is certainly correct. A small
fraction of unresolved states does not alone bound their price contribution.

Y lies in [-Bput,Bput]. A conditional second-moment envelope is

    E[Y^2|X] <= d { m2(X)+h^2-2h(c0-U) },              (10)

where m2 is (6). Intersect this bound with Bput^2. The negative cross term is
valid because E[R|X]=c0-C>=c0-U and h>=0. A purely analytic global fallback
is 2q^2 E[(A-G)^2], since R<=q(A-G) and h<=q E[A-G|X].

## Statistical bounds and what they do not prove

Given independent inner samples, Z=c0-mean(R) is conditionally unbiased for C.
The function r_d(z)=(z-Kc)+-d(z-Kc) is convex. Consequently

    E[regret] <= E[r_d(Z)].                             (11)

For the clipped policy and this residual, 0<=r_d(Z)<=Bput. If d=1 then
r_d(Z)=(Kc-Z)+ <= (V-Z)+ <= Bput; if d=0 then
r_d(Z)=(Z-Kc)+ <= (Z-V)+ <= Bput.

Fixed-N iid outer samples and DISJOINT independent inner groups let us apply
Maurer-Pontil Theorem4. For sample variance s^2, range W and failure delta,
the implemented conservative two-sided radius is

    sqrt(2*s^2*log(4/delta)/N)+7*W*log(4/delta)/(3*(N-1)). (12)

We bound both E[(10)] and E[mean_j Y_j^2], splitting the .001 moment failure
budget before taking their minimum. The smaller observed upper bound is valid
by that union bound; taking an unadjusted minimum would not be justified.
The mean of squared samples is essential: the square of the inner sample mean
would underestimate the single-sample quantum source's second moment.

The same experiment estimates the residual mean classically. This makes its
time especially important: using it as free quantum preprocessing would hide
useful classical pricing work. All statistical guarantees idealize iid draws
and real arithmetic. Finite Gaussian encoding, PRNG and rounding are separate.
Zero observed regret still has a positive range term in (12).

## Quantum cost contract

The flattened mean source prepares an exercise state and future trajectory,
evaluates arithmetic and geometric puts, c0 and V, and returns the signed Y.
An estimator must charge source/inverse operations, bin encodings, controls,
uncomputation and all requested classical outputs. Analytic does not mean
free on a quantum computer: normal CDFs, logs, exponentials, comparisons and
policy evaluation need explicit reversible implementations.

The explicit signed-dyadic schedule consumes a proved second moment. Its
queries are counted, but its complete parity finance circuit is not emitted.
Existing emitted arithmetic gives a favorable path-generation subtotal.
An ideal sqrt(moment)/epsilon curve with coefficient one omits confidence,
constants and some inverse work: it is neither an implementation nor a lower
bound on every quantum algorithm. Pilot moments in that curve are diagnostic
only. A modern adaptive mean estimator might avoid our particular variance
preprocessing; its cost must be established rather than assumed equal to zero.

Small conditional moments do not automatically give a uniform small bound in
the nonlinear theorem. Using state-dependent stopping or rejection into a
boundary region requires a specified coherent algorithm, including preparation
and variable-time overhead. Classical mean runtime is not coherent runtime.
