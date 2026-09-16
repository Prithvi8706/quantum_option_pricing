# Mathematical specification of the rescue prototype

## Status and attribution

This is a derivation for the implemented procedure, not a claim of a new
martingale inequality, new rotation-synthesis method or formally verified proof.
Likelihood-ratio mixtures and anytime-valid inference are established; see
[Howard et al.](https://arxiv.org/abs/1810.08240) and
[Waudby-Smith and Ramdas, section 2](https://arxiv.org/html/2010.09686v7).
The following elementary Bernoulli derivation makes the implementation's
assumptions explicit instead of borrowing a posterior-coverage interpretation.

## 1. Fixed-menu sequential observation model

Let D be a finite menu of permitted Grover depths fixed before observations.
The representation is also fixed. At each time the next depth is chosen using
only the past. When depth k is chosen, its next outcome is Bernoulli with
conditional probability q_k=f_k+(1-f_k-g_k)*p_k(a), where
p_k(a)=sin^2((2k+1)*asin(sqrt(a))). The probabilities q_k must remain fixed
throughout the procedure. Predictable choice of depth does not permit changes
to that depth's mean or arbitrary correlations in its conditional response.

One independent, fixed-size zero/one calibration acquisition gives two CP
intervals whose total noncoverage is alpha_cal. Supplied transfer allowances
must simultaneously bound the difference from calibration to every validation
depth's f_k and g_k. Allowances are assumptions, not estimated truth. Depth-wise
rates can differ within those allowances, but each depth's q_k is stationary.
This is not a model of arbitrary coherent gate noise or dynamic drift.

## 2. Bernoulli likelihood-ratio mixture

For an interior null probability q and a fixed alternative u in (0,1), define
L_n(u,q)=(u/q)^s*((1-u)/(1-q))^(n-s). Under the null, conditioning on the past
gives expected multiplicative increment
q*(u/q)+(1-q)*((1-u)/(1-q))=1. Thus L is a nonnegative unit-initialized
martingale. Mixing u using a Beta(1/2,1/2) law fixed before observations yields

M_n(q)=B(s+1/2,n-s+1/2)/[B(1/2,1/2)*q^s*(1-q)^(n-s)].

Nonnegativity allows the conditional expectation and integral to be exchanged.
Ville's inequality gives P_q(exists n: M_n(q)>=1/alpha_k)<=alpha_k.
Using the closed acceptance set M_n(q)<=1/alpha_k only enlarges the interval
at threshold equality. At q=0 or 1, the actually possible outcome sequence
gives a nonnegative supermartingale by the limiting construction, and the
corresponding boundary is retained. At n=0, return [0,1].

The log ratio equals log B(s+1/2,n-s+1/2)-log B(1/2,1/2)
-s log q-(n-s) log(1-q). It is convex on (0,1) and minimized at s/n, including
the boundary cases. Therefore its sublevel set is an interval. The code bisects
both sides and returns outer brackets with additional engineering padding.
The mathematical construction is exact; the floating-point code is not a
directed-rounding implementation.

## 3. Sampling depths adaptively

For each fixed k, update its martingale only when k is sampled and leave it
unchanged otherwise. Since choosing k is predictable, the stopped-clock
process remains a martingale under its null. Choose positive alpha_k summing
to alpha_val before observations. The implemented equal allocation is
alpha_val/|D|; include unobserved depths with n_k=0 rather than changing D.
A union bound then gives simultaneous containment of all q_k at all times
with probability at least 1-alpha_val. No extra spending per inspection is
required. The intervals need not be nested for this statement to hold.

Intersecting with previous confidence sets would also be valid, but the current
code uses each time's all-depth intersection and does not rely on monotonicity.
The discovery experiment tests only k=0. The general fixed-menu construction
does not mean an adaptive-depth scheduler has already been benchmarked.

## 4. Readout inversion and dollar propagation

On the calibration event, expanded endpoints contain the validation rates.
If the rectangle cannot establish f+g<1, the code returns [0,1] in amplitude.
Otherwise a validation interval [qL,qU] implies the outer p interval

pL=max(0,(qL-fU)/(1-fU-gL)),
pU=min(1,(qU-fL)/(1-fL-gU)).

If pL>pU, the observations and allowed model are incompatible. Otherwise invert
every monotone branch of p_k and intersect the resulting unions for all depths.
On the joint calibration/validation event, the true amplitude remains in the
intersection at every time. Allocating alpha_cal=.025 and alpha_val=.025 gives
at least .95 simultaneous containment in exact arithmetic under the assumptions.

For an externally justified deterministic bound
|P_continuous-(O+S*a)|<=B with S>0, map the amplitude hull [aL,aU] to
[O+S*aL-B,O+S*aU+B]. Any data-dependent stopping time based on past and current
observations preserves the joint-event guarantee. Declare tolerance tau only
when this price interval's radius is <=tau. On that event and joint containment,
its midpoint error is <=tau. Therefore the probability of an erroneous
declaration is at most alpha_cal+alpha_val, under exact arithmetic and the model.

This is NOT a 95% coverage statement conditional on declaration. It does not
validate B, prove transfer allowances physically, allow representation selection
without adjustment, or retroactively certify a different native AE algorithm.

## 5. Exact finite-grid payoff intervention

Let pi_i be the existing point-density grid distribution, not integrated cell
masses. Set y_i=max(x_i-K,0)/(U-K), with U>K. The controlled Ry angle
2 asin(sqrt(y_i)) produces success probability y_i. Linearity of expectation
then gives a=sum_i pi_i*y_i and P_grid=exp(-rT)*(U-K)*a. No exact continuous
price is required to construct these angles. They depend on the known payoff
function and grid, not on an expectation estimated from the experiment.

Keep the existing support/grid allowances, set the analytic linearization
allowance to zero, set O=0 and S=exp(-rT)*(U-K). This removes only the old
sinusoidal approximation. Numerical angle error, state-preparation error and
physical noise are not proved absent by this algebra; the statevector check is
an ideal numerical diagnostic. Large-scale fault-tolerant synthesis would
require a separate rotation-precision budget.

## 6. Why a cost-aware criterion must include the encoding

With known f,g, c_r=1-f-g>0 and direct Bernoulli sampling, a Hoeffding interval
has amplitude radius at most sqrt(log(2/alpha)/(2N))/c_r. Mapping to dollars
requires S*sqrt(log(2/alpha)/(2N))/c_r+B<=tau. Rearranging gives

N >= log(2/alpha)/2 * (S/[c_r*(tau-B)])^2, for B<tau.

This is a conservative sufficient condition, not a lower bound or empirical
sample-complexity fit. Multiplying by a measured per-shot circuit cost yields
a bound-based representation score. Finite calibration, all-branch ambiguity
and the cost of acquiring calibration cannot be discarded in the operational
version. Optimizing only amplitude precision or Grover-query counts misses
the dependence on S, B and actual circuit cost.

The prototype demonstrates the components needed for that operational
question; it does not yet implement a proven optimal policy. The claim of
novelty, if any, must rest on an additional meaningful decision result and
its comparison with prior work, not on renaming this standard inequality.

## 7. Separately declared conditional pilot mixture

The follow-up reserves the first m=1024 pricing observations as a pilot with
s_p successes. Conditional on this history, freeze a Beta(s_p+1/2,m-s_p+1/2)
mixing law. Apply the likelihood ratio only to the subsequent n-m observations
and s-s_p successes. Its normalization is the beta function of the frozen pilot
parameters, not the original Jeffreys beta function. Section 2's martingale
argument applies conditional on the pilot because every fixed-alternative
ratio starts at one on the validation sample, regardless of the mixing law.

Do not reuse pilot observations as validation successes: that would invalidate
this simple conditional argument. The total cost still includes every pilot
shot. The code returns a full interval at n=m and cannot declare from pilot
data alone. Calibration and transfer assumptions are unchanged. This validity
argument says nothing about whether a particular random pilot is statistically
efficient; it can produce an unfavorable mixture and delay stopping.

The guarantee above is prospective for a fixed procedure. Selecting this
follow-up after inspecting the original experiment is method development;
reusing those validation paths does not itself give a selection-adjusted 95%
guarantee for the post hoc choice among procedures. Fresh confirmation or an
explicit across-method correction is needed for that stronger interpretation.
