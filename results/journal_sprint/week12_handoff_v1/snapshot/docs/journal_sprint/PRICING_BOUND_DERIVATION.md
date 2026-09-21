# Deterministic price-bound derivation

These are standard coupling, total-variation and Taylor-remainder arguments,
not a claimed new theorem. Their implementation preserves the existing pointwise
density grid. Claims below concern exact arithmetic; SciPy/NumPy evaluations are
tested but are not formally verified interval arithmetic.

Let D=exp(-rT), g(s)=(s-K)+, A=[L,U], retained probability m, omitted probability
delta=1-m, and M=U-K. The support construction ensures 0<L<K<U. Write
P=D E[g(S)] and P_support=D E[g(S)|A].

## Support

The difference P_support-P equals delta*P_support minus discounted omitted payoff.
Since 0<=g(S)<=M inside A, an absolute bound is

`B_support = D*(E[g(S) 1_(S>U)] + delta*M)`.

The omitted lower region has zero call payoff. For log S~N(mu,sigma_ln^2), set
z=(log(U)-mu)/sigma_ln. The upper payoff moment is

`exp(mu+sigma_ln^2/2)*Phi_bar(z-sigma_ln) - K*Phi_bar(z)`.

This is an explicit distributional tail bound, not the observed difference
between a computed support price and Black-Scholes. It relies on the declared
lognormal model. Tail calculations and support construction are classical work
that an eventual resource comparison must count.

## Finite grid: do not substitute bin masses for point densities

Let x_i be the circuit's uniform endpoint grid, spacing h. Its probabilities are
pi_i=f(x_i)/sum_j f(x_j). Define w_i separately as the exact conditional mass of
the nearest-grid-point cell around x_i; endpoint cells have half width. These
integrated masses are used only in the proof/bound, not as replacement circuit
probabilities.

Couple S|A with its nearest grid point Q(S). Then |S-Q(S)|<=h/2. Because the call
payoff is 1-Lipschitz, their payoff expectations differ by at most h/2. On the
grid the payoff ranges from 0 to M, so changing weights w to pi changes its
expectation by at most M*TV(w,pi), where TV is half the sum of absolute weight
differences. Thus

`B_grid = D*(h/2 + M*TV(w,pi))`.

CDF or survival-function differences evaluate the cell masses. The implementation
uses survival differences in the upper tail to reduce cancellation. The bound
is deliberately simple and can be loose, especially on wide support intervals.
It requires O(2^n) classical distribution evaluations; it is not free preprocessing.

## Payoff encoding

Put y=g(x)/M in [0,1] and t=pi*c*(y-.5). The objective probability is
a(x)=.5+.5*sin(t). Linearized inverse post-processing gives

`h(a(x))/M = .5 + sin(t)/(pi*c)`.

Subtract y. The bound |sin(t)-t|<=|t|^3/6 and |t|<=pi*c/2 yield

`B_encoding = D*M*pi^2*c^2/48`.

The pointwise bound also bounds its expectation. The implementation limits c to
(0,1]. Smaller c reduces this term but increases price sensitivity to probability
uncertainty. It is not a uniformly beneficial knob.

## Combined statistical interval

Define `L_P=D*M*2/(pi*c)` and `offset=L_P*(-.5+pi*c/4)`. The mathematical encoded
price is offset+L_P*a. By the triangle inequality,

`|P-(offset+L_P*a)| <= B_support+B_grid+B_encoding = B`.

For a confidence hull [a_lo,a_hi], expand its mapped interval to

`[offset+L_P*a_lo-B, offset+L_P*a_hi+B]`.

Its radius is L_P*(a_hi-a_lo)/2+B. For tolerance epsilon, the statistical
probability-radius allowance is max(0,(epsilon-B)/L_P). A positive allowance is
only a necessary opening for this sufficient certificate: it does not guarantee
that a finite-shot procedure will attain it. B>=epsilon is labeled unresolved,
not an impossibility theorem about actual error or alternative bounds.

The bound routine does not call Black-Scholes, the exact finite-grid payoff
expectation, or the exact encoded objective. Those appear only in a separate
diagnostic path to check correctness. Ideal pricing circuits have been checked
for the six discovery contracts at n=3,c=.25. No compiled-noise, calibration,
hardware, or formal floating-point correctness guarantee has been added.
