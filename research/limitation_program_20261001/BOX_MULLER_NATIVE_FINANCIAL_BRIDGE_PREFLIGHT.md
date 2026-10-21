# Original Box–Muller native financial bridge

This NEW preflight is author-only. No executor, numerical value, proof replay,
source walk, pricing sample, circuit compilation, fixture or receipt is produced.
It fixes a prospective bridge from the original native-radius/ideal-angle hybrid
to the ORIGINAL B4x12 and B8x52 native financial sources. Existing sources,
receipts, costs, methods, precision, barrier ties and adoption decisions stay
immutable. During the current timing reservation, all author work is text-only.

The exact reference retains S0=100, K=100, H=140, sigma=3/10, rho=2/5,
rate=3/100, maturity1, positive equal-weight arithmetic baskets, equally spaced
12 or52 dates, and strict all-date survival B_j<H. Its Asian value is the exact
mean over all asset/date stocks, discounted by d=exp(-3/100). The source is
q32/f40/w72, with30 or234 ORIGINAL joint pairs. No AS241 scalar/financial theorem,
cost or adoption transfers into this proof.

The prerequisite is a complete uncensored PASS of BOTH future polar receipts
`A02_polar_cdf_bv_run001` and `A02_polar_cdf_bv_audit_run001`. Reject
FAILED_UNSEALED.json or failure.json BEFORE any success-looking summary,
completion or manifest. Rejection, missing artifacts or incomplete ownership
also blocks admission. Their
actual manifest and executor/auditor byte pins must be fixed in a root release
after they exist; this preflight does not fabricate those pins or outcomes.
Read `source_binding.json`, `log_radius_envelope.json`, `angular_guards.json`
and `ideal_hybrid_bounds.json`, together with the independent130 artifacts.
Require the same original source identities/roles, certified internal-radius B,
squared-radius KS D_S, positive reference cap C_H=40d and both strict angular
guards. Preserve the actual primary and independent bounds; do not relabel the
hybrid component as a native-price certificate.

The intended future fresh labels are `experiment_box_muller_native_financial_bridge.py`,
`audit_box_muller_native_financial_bridge.py`, `A02_BM_native_financial_bridge_run001`
and `A02_BM_native_financial_bridge_audit_run001`. Modules would use pinned local
Python `-B -m <module> prepare|run --output <exact absolute fresh receipt>`.
These labels are prospective, with no present implementation or authorization
to execute during timing. Root fixed finite proof limits BEFORE implementation:
180 process CPU,150 work-admission CPU and600 wall seconds for each process,
primary90 and independent130 outward decimal digits, one numerical thread.
The existing polar limits are also180/150/600. All provenance, verification,
output and failure retention count within those hard limits. No precision
escalation, retry or sweep is allowed.

## Remaining normal and log error

Set epsilon=2^-40 and N=2^32. The radial certificate already pays the q32 radius
law, log table/Horner/ln2 error and native root floor. Its angular quadrature
already pays the ideal midpoint angle grid. The only remaining coordinate
envelope is `delta_Z=B*E_cos+epsilon`: E_cos pays the ORIGINAL64x8 literal cosine
table, Taylor error and signed Horner floors; epsilon pays the actual final
radius-product floor, including negative results. Actual lookup addresses,
dyadic centers, v-center subtraction, native product144/stored72 safety and
shared radius must be bound. The table is for cos(2*pi*v) directly. Midpoint
conversion and+.75 f40 turn/low40 wrap are exact; the second ideal coordinate
is +sin(theta). There is no rounded2pi multiplication or independent-normal
assumption for the finite pair.

For each original date prefix prove
`lambda_j=e_logS0+sum_t<=j((|a_hat_t|+|b_hat_t|)*delta_Z`
`+(e_a_t+e_b_t)*B+e_mu_t+2*epsilon)`.
Here true a,b,mu are the unchanged exact continuous-contract coefficients;
the errors compare their exact values with decoded native literals. Every
common/idio input appears once in the appropriate Hillis–Steele prefix.
Additions contribute zero rounding ONLY after fresh no-wrap bounds for every
stored raw prefix/partial sum, before clipping. Pay both signed multiplication
floors per increment, initial log-spot and drift/literal errors. Do not use the
AS241 endpoint6.5, an old cutoff radius, old Holder normal error or a scalar
KS correction in this envelope.

## Original stock arithmetic and clipping

Bind all48+416 actual stock sites to the actual original degree12 Estrin DAG,
signed reduction/shift semantics and decoded clamp words L,U. Canonical
72-bit constants must be decoded as signed where the operator requires it;
an unsigned lower-clamp comparison is invalid. Partition EVERY clipped integer
input into its exact k=floor(x_raw*inverse_ln2_raw/2^80) cell. A prospective
30-class superset k=-17..12 may include empty extremes; empty classes are not
required to be occupied. Every nonempty cell and both clamp endpoints must
be covered without an integer gap or overlap.

On a cell, reconstruct the polynomial's13 literal coefficients and every
Estrin multiplication/floor. Let E_k bound its deviation from exp(r), paying
coefficient error, Taylor remainder and native polynomial evaluation. For the
actual remainder interval [r_min,r_max] and ln2-literal error e_ln2, one valid
relative envelope is
`alpha_k=exp(|k|*e_ln2)*(1+E_k*exp(-r_min))-1`.
Take alpha over nonempty cells; require0<=alpha<1. Native k*ln2 multiplication
is integer-exact after source/range proof; positive final shifts are exact
after no-wrap, while negative final shifts pay additive beta=epsilon. This gives
`(1-alpha)*exp(clip(x_hat))-beta <= S_N`
`<= (1+alpha)*exp(clip(x_hat))+beta`.
The polynomial, all144-bit products, stored72 outputs, signed extraction,
shift controls, raw prefixes and ALL eager dead-path operations need safety.

Original E03 support and independent actual-SSA audit receipts may be reused
only through exact owner-membership/source pins and matching original targets.
They already support stock positivity, clipped-cell arithmetic, stock tree
sums/max/average/subtract/discount safety and nonnegative native payoff below40.
They do not replace the new raw-log error, raw-prefix safety or approximation
envelope. Do not import/rebuild historical builders or transfer an AS241 v5
financial certificate; fresh producer/auditor checks bind the original source.

Set `a_j=(1-alpha)*exp(-lambda_j)`, `b_j=(1+alpha)*exp(lambda_j)` and
`ell=(1+alpha)*exp(L)+beta`. Require0<a_j<=1<=b_j and0<=ell<H. Prove BOTH:
the actual native stock at U is at least na*H, so upper clipping knocks out the
native basket; and `exp(U-lambda_j)>na*H`, so that same event knocks out the
ideal hybrid basket. Native nonnegative stocks and exact binary1/na averaging
are premises. With upper-clamp events thus removed from either survivor,
`a_j*B_H-beta-epsilon <= B_N <= b_j*B_H+ell`.
Different strict one-date decisions imply the CLOSED ideal-hybrid band
`L_j=(H-ell)/b_j <= B_H <= U_j=(H+beta+epsilon)/a_j`.
Native equality at H and all band-endpoint ties remain included.

## Band transport and smooth price

Use POINTWISE total variation: the left limit to the actual point value and
the actual point value to the right limit are both counted. Functions are not
identified merely almost everywhere. A retained singleton contact therefore
costs two jumps, even if the continuous reference gives that point zero mass.
Open/closed threshold and band probabilities use the appropriate one-sided
CDF values F(t-) and F(t); the continuous reference agrees at both while the
finite hybrid may have an atom. The circular convention includes the periodic
seam, and exact midpoint singleton ties remain part of the quadrature error.

For a fixed current pair's ideal angle, each ideal stock is positive c*exp(v*r),
so its basket is convex in r>=0. A closed finite basket band is at most two
intervals, including singleton contacts, and its indicator has radial TV<=4.
For fixed bounded current Rhat, original positive pair roles and the already
certified strict kappa<sqrt2 guard give an angular basket with one maximum and
one minimum, including axis/constant/zero-radius degeneracies. A closed band
is at most two arcs and has circular TV<=4; do not substitute strict-threshold
TV2. Telescope radius FIRST, then angle, one WHOLE joint pair at a time.
Other continuous pairs only change positive weights. At date j use exactly
`m_j=ceil((na+1)*j/2)` relevant whole pairs, retaining the unused future partner
when a pair straddles dates. The band-law allowance is
`Q_j=m_j*(4*D_S+2/N)`.

The continuous Gaussian reference alone has independent common/idiosyncratic
Brownian drivers. Conditioning there gives B_j=exp(s_j*Z)*W, W>0 independent
of Z, with `s_j^2=sigma^2*rho*j/nt`. Thus the unconditional CLOSED-band bound
is `p_Gj<=min(1,log(U_j/L_j)/(s_j*sqrt(2*pi)))`. No conditioning on survival,
clipping or a radial good event is used. Under the finite hybrid law,
`p_Hj<=min(1,p_Gj+Q_j)` and `P_H(any switch)<=min(1,sum_j p_Hj)`.
Finite paired outputs are never called independent Gaussian coordinates.

The original Asian source averages ALL native stock words, not the rounded
date baskets. If S_j_raw is the integer sum of nonnegative date stock words,
the exact binary basket coefficient gives B_N_raw=floor(S_j_raw/na). The actual
strict comparison B_N_raw<140*Q, with140*Q an integer, implies
S_j_raw<na*140*Q, hence the UNROUNDED native date stock mean itself is <H.
Thus every surviving native total stock sum is <na*nt*H in real units, just
like the ideal strictly surviving total; no margin is assumed away because
the predicate contains a floor. On both-path strict survival, one safe unrounded mean-stock
error is `D_j=H*max(1-a_j,b_j-1)+max(beta,ell)`. Let c_A and d_hat be the actual
average and discount literals. A paid smooth bound is
`A_err=sum_j D_j/nt + na*nt*H*|c_A-1/(na*nt)|+epsilon`,
`zeta=d_hat*A_err+40*|d_hat-d|+epsilon`.
Require0<d_hat<=1, exact strike and native positive-part/sum/subtract safety.
The basket floor occurs in the lower barrier band, not a second Asian-average
charge. zeta and both payoff caps are already discounted. For switches use
`C_star=max(C_H,C_native)<=40` from BOTH actual support certificates, or the
fixed safe40-dollar cap. Do not silently substitute only the ideal cap or pay
80 dollars for two nonnegative payoffs in the same[0,40] support.

## Pay-once ledger and unchanged acceptance

The prerequisite hybrid price-law bound is
`H_price=M*(4*C_H*D_S+C_H*(nt+1)/N)` for M30 or234. The NEW bridge adds
`Bridge=zeta+C_star*min(1,sum_j min(1,p_Gj+Q_j))`.
The sole proposed complete financial bound is `Total=H_price+Bridge`.
The band-law allowance is an additional variation obligation for band
indicators; a price-expectation certificate does not make it free. Equivalently,
transfer the augmented envelopes `Y_H +/- C_star*1{any band}` once, with price
and band variations explicitly itemized. These two presentations must not be
summed as separate bounds. Log/root or midpoint coupling terms must not be
added to delta_Z, lambda, a new cutoff tail or a generic40*dimension/N term.
If implementation uses the explicit ledger, preserve the certified PRIMARY
polar B, D_S, cap enclosure and hybrid price bound as pinned rational inputs;
the independent polar audit confirms them. The bridge auditor independently
rederives its fresh cosine/log/stock/clip/band/smooth bounds at130 digits against
the same pinned premise set, with no producer-helper import or precision
escalation. Independent outward bounds need not equal90-digit fractions;
they must justify every primary claimed upper bound and the fixed scope.

Final acceptance requires complete independently audited original-source and
native-safety proofs for BOTH contracts and each outward `Total<=11/2000`
dollars ($0.0055). Overall epsilon1/100 and statistical allowance9/2000 remain
unchanged. No outcome-dependent reallocation, new cutoff, precision search,
method selection, model change or relaxed predicate is allowed. A valid proof
whose bound exceeds the residual is a retained certificate-method rejection;
failed guards, budget censor and failed-unsealed are separate terminal failures.
No numerical value, passing claim or G2 closure is asserted here.

Any future accepted theorem covers only continuous-to-native dollar bias for
these two exact ORIGINAL tasks. Separate source execution/replay/cost adoption,
complete estimator99% delivery, matched successful classical timing, physical
schedule/fault certificate, other contracts and quantum advantage remain open.
No new fixtures, gate replays or historical counts are credited by this proof.

Future execution requires reviewed/frozen fresh producer/auditor and preflights,
actual interpreter/base/mpmath/backend/cache origins before work, exclusive
fresh outputs, finite source/word/class inventory, and all hashing/output/
retention charged to the fixed bounds. The auditor independently decodes source
words and rederives130-digit envelopes; it never imports producer helpers.
Existing own-map schemas must be explicitly identified: canonical ROOT keys
for historical receipts, or declared receipt-local owned keys confined and
rebased to canonical ROOT keys for the prospective polar packet. All frozen
maps use exact equal-SHA merges; scoped external runtime inputs remain separate
and are verified in full. Actual-hash caches need unchanged stat fingerprints;
terminal verification freshly resolves and hashes the complete unique input
union. No provisional success manifest, expected override, missing ledger waiver,
overwrite or retry is permitted. Global LIVE36/9 remains false with no waiver.
Selected original source pins are declared expectations copied from existing
manifest metadata, not a current SHA verification. Before future preparation,
verify actual bytes and equal-SHA OWNED/FROZEN membership for each selected
nonmanifest input; verify each selected owner manifest separately without
inventing self-membership. Source-bound archived routes must preserve both
the original identity/expected SHA and exact executed snapshot bytes. This is
a selected evidence scope, not a claim that all historical LIVE inputs pass.
All work is local; no commit, push, upload or cloud action occurs.
