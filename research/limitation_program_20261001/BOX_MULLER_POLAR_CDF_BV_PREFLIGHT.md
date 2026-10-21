# Original Box–Muller polar CDF and conditional variation preflight

This is a held author-only plan, with no executor or execution receipt. It
preregisters a possible law-transfer bound from independent continuous
Box–Muller pairs to the original native internal radius and exact angular
midpoint grid, evaluated through the **unclipped exact GBM reference**. It does
not certify the native financial payoff or close G2. All prior authors and
receipts remain immutable. No numerical bound, proof replay, arrays, tests,
synthesis, sampler or pricing execution occurred to author these two files.

The only contracts are B4x12 and B8x52: respectively 30 and 234 original joint
pair blocks, including pairs that straddle dates. The exact reference has
S0=100, K=100, H=140, sigma=3/10, rho=2/5, rate=3/100, T=1, equal date spacing,
the arithmetic mean over all assets and monitored dates, and strict survival
`max_j basket_j < H`. Its cap is derived from that reference:
`C=(H-K)*exp(-rate*T)`, since survival makes the all-date average less than H.
The prior native support bound is not transferred to this ideal model; native
averaging/discount literals and equality handling require their own bridge.

The JSON pins the two accepted A10 targets/native invocation sources, original
sampler and price source, C06 certificate, and independent scope/table/domain
audits with their owner manifests. Future code must reconcile each selected
binding with its original manifest membership and exact expected SHA, preserving
any legitimate archived route explicitly. Prior global LIVE integrity remains
false with 36 references across nine paths; no expected SHA is waived.

Write N=2^32, Q=2^40, epsilon=1/Q and U_k=(k+1/2)/N. The exact internal input
integer is `(2*k+1)*128`. Native log normalization uses exponent -33 through -1
and only exact left shifts; integer exponent times the frozen f40 ln2 literal
and multiplication by -2 have no extra floor term. A fresh source-bound replay
must establish the full-domain table error E_table and literal error E_ln2,
including all actual Horner floors and signed intermediates. Put
`E_L=E_table+33*E_ln2`. The source-semantic radius is
`R_raw=isqrt(max(-2*L_raw,0)*Q)` and `Rhat=R_raw/Q`, with wrapping excluded.
For an all-midpoint radius bound `0<=Rhat<=B`,
`0<=max(-2*Lhat,0)-Rhat^2<2*epsilon*Rhat+epsilon^2`, hence
`|Rhat^2-(-2*log U_k)|<=eta=2*E_L+2*epsilon*B+epsilon^2`.
Rhat is the internal radius word, never the norm of the two final rounded
normal outputs. Existing C06 all-q32 provenance is a prerequisite, not a new
polar-CDF or dollar certificate.

The squared exact continuous radius has CDF `F(s)=1-exp(-s/2)` for s>=0,
extended by zero for s<0. The equally weighted S_k=-2*log U_k grid has KS
distance exactly `1/(2*N)`. A possibly nonmonotone native radius map still gives
`F_grid(t-eta)<=F_RhatSquared(t)<=F_grid(t+eta)` by event inclusions. The CDF is
globally 1/2-Lipschitz, so preregister `D_S<=min(1,1/(2*N)+eta/2)`. No ordering
of the native radius map, cutoff event or Holder square-root coupling is used.

For the radial conditional lemma, fix every other pair and this pair's angle.
Each exact stock is `c_i,j*exp(beta_i,j*r)`, with c positive and beta any real.
Baskets and the Asian average are convex on r>=0. Every strict basket sublevel
is an interval, and all-date survival is their interval intersection I. On I,
the smooth payoff `h=discount*(average-K)^+` is convex, between zero and C.
Its variation inside I is at most 2C; at most two knockout endpoint jumps add
at most 2C. Thus payoff TV in r, and after r=sqrt(s), is at most 4C. Empty,
full, unbounded, constant and strict-endpoint cases must be retained explicitly.
The radial price step is bounded by `4*C*D_S`. No native or clipped convexity
claim is made.

For the angular lemma at a fixed bounded Rhat=r, the raw exact log dependence
is `r*(a_i*cos(theta)+b_i*sin(theta))`, where a_i,b_i>=0. For each basket or
the Asian average define `A_i=r*a_i`, `B_i=r*b_i`,
`x_i=A_i*cos(theta)+B_i*sin(theta)`,
`y_i=-A_i*sin(theta)+B_i*cos(theta)`, `w_i=c_i*exp(x_i)`, and
`kappa=max_i sqrt(A_i^2+B_i^2)`. Preregister the strict guard kappa<sqrt(2).
In quadrant I let s=sin(theta), c=cos(theta). At a stationary point,
`c*sum(w*B)=s*sum(w*A)`. For `X=sum(w*x)`, this gives
`sum(w*A)=c*X`, `sum(w*B)=s*X`. Nonnegative A,B and their norm bound imply
`y_i^2<=kappa*(s^2*A_i+c^2*B_i)`. Consequently
`sum(w*y^2)<=kappa*s*c*(s+c)*X<=kappa*X/sqrt(2)`, and
`basket''=sum(w*(y^2-x))<0` at every nonconstant stationary point.
Thus quadrant I has at most one maximum. Quadrants II and IV have respectively
negative and positive derivative; quadrant III has strictly positive second
derivative and one minimum. Zero endpoint derivatives force an all-one-axis
case; r=0 or all-zero vectors gives a constant function. The future checker
must retain these cases and justify the stationary-crossing argument explicitly.

Every strict basket threshold indicator therefore has circular TV<=2,
including a threshold at the maximum which removes one point and still costs
two jumps. The capped smooth payoff `min(C,discount*(average-K)^+)` has
circular TV<=2C and equals the true smooth payoff on survival. Multiplication
by the nt strict survival indicators gives payoff TV<=`2*C*(nt+1)`.
Midpoint quadrature on the unit-turn circle costs at most TV/(2N); ties at a
grid midpoint remain included in TV. Thus the angular price step is at most
`C*(nt+1)/N`, with no extra 2*pi probability factor. A **closed finite basket
band** has TV<=4, not 2 (also retain the separate ideal radial band TV<=4);
any future native-error band transfer is a separate
open obligation.

The source role grammar is flat index `t*(na+1)+role`, role zero common and
roles 1..na distinct idiosyncratic drivers. Adjacent joint pairs are
common+first-idio, two distinct same-date idios, or last-idio(t)+common(t+1).
Each driver enters a later raw log prefix once. For a given stock both pair
coordinates can affect it only as one common plus one idio; otherwise at most
one applies. Future exact source/role/prefix binding must prove
`a^2+b^2<=sigma^2*T/nt`. A sufficient guard is then
`B^2*sigma^2*T/nt<2`, separately for both contracts. This guard has not been
numerically evaluated. Ideal coefficients are distinct from rounded native
finance coefficients and floors.

Telescope continuous-to-hybrid law replacement **radial first, then angular
for each original joint pair**. Its angular step then has bounded Rhat. Other
pairs may remain continuous and unbounded: they only change positive weights,
and the conditional lemmas are uniform in those weights. Do not apply the
angular lemma to an unbounded current continuous radius. Each pair contributes
at most `4*C*D_S+C*(nt+1)/N`; multiply by the original 30 or 234 joint blocks,
without dividing by coordinates. No dollar value or passing claim is recorded.

The native source directly evaluates a frozen polynomial for cos(2*pi*v);
there is no rounded 2*pi multiplication to charge. The q32 midpoint and f40
`+.75` turn plus low40-bit wrap are integer-exact, giving the exact reference
identity `cos(theta+3*pi/2)=+sin(theta)` and permuting the midpoint grid. Finite
digital normal outputs are still one joint pair, not independent normals.
The proposed hybrid uses Rhat and **ideal** midpoint cosine/sine. The pay-once
ledger assigns log/ln2/root and radial discretization to D_S, and angular
discretization to the circular quadrature term. Remaining native cosine table,
Horner/floor and radius-product errors are separate. Their future isolated
coordinate envelope is `B*E_cos+epsilon`, subject to the actual cosine/table,
product and no-wrap premises; it contains no radius approximation term. Do not
reuse the full old C06 normal-arithmetic bound: that includes
`sqrt(2*log_error)+epsilon` for radius approximation already paid by D_S.
Do not add its continuous-to-grid radial or angular coupling terms again. Native increment,
average, discount and stock arithmetic, clipping, eager signed-word safety,
strict barrier and closed-band transfers, full native price bias, costs,
adoption and quantum advantage all remain open.

Root fixed prospective producer and independent-auditor limits to 180 process
CPU / 150 work-admission CPU / 600 wall seconds each, including all provenance,
verification, output and failure retention. Primary outward interval precision
is fixed at 90 decimal digits and independent replay at 130, with exact rational
endpoints and unchanged q32/f40/w72 semantics. Future proof replay is finite:
all actual pair scopes and roles in these two contracts; the frozen log table,
ln2 and root/domain premises; source cap and symbolic BV obligations; the
strict angular guard and both resulting ideal-law inequalities. No grid sweep,
samples, CDF fit, new circuits, gate replays, pricing estimator, tests or synthesis
is authorized. Future implementations must be independently reviewed and
freeze their code/preflights, actual interpreter/base/dependency origins before
work; use canonical confined equal-SHA merges, invocation-local actual-byte
caches with stat guards, final fresh complete input verification, exclusive
outputs and budget-charged terminal hashing. Failure is terminal, never a retry;
exhausted retention is explicitly failed-unsealed. Root fixed the intended
unexecuted author filenames to `experiment_box_muller_polar_cdf_bv.py` and
`audit_box_muller_polar_cdf_bv.py`, and prospective receipts to
`A02_polar_cdf_bv_run001` and `A02_polar_cdf_bv_audit_run001`. Each future module
uses `prepare` and `run` with `--output` pointing to its exact receipt, launched
with the pinned interpreter's `-B -m` CLI. These labels imply no present code,
execution or passing receipt; actual executor/auditor own SHA pins must be
fixed by root and peer review before preparation. The unchanged 11/2000 dollar
residual is reported beside the two prospective partial hybrid bounds only.
It is neither spent nor reallocated, and supplies no full G2 or adoption
acceptance threshold while the native financial bridge is absent. Fixture
credit remains zero, and execution waits for all numerical and timing owners
and descendants to be terminal.
