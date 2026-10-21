# Full native AS241 financial-bias preflight

Static design only. No proof evaluation, graph, test, price observation, gate
array, or certificate has been produced by this document. Stage C timing jobs
remain untouched. All quantities below are prospective proof obligations.
The proposed sampler is a different law from the accepted finite paired
Box-Muller source; that source and its receipts remain unchanged.

The future attempt has exactly two fixed contracts, B4x12 and B8x52, q32
midpoint inputs, signed native72/f40 arithmetic, the original stock-only clamps,
strict basket survival, arithmetic Asian call, and original discount. There is
one proof method and no precision, partition, cutoff, or parameter sweep.

## Three laws and one error route

Let `N=2^32`, `S=2^40`, and `eps=1/S`. For each original independent common or
idiosyncratic driver use one independent uniform raw word `k` and its exact
midpoint `(k+1/2)/N`. Distinguish these prices:

1. `P_cont`: the original continuous independent-Gaussian ideal GBM, with exact
   unguarded exponential stocks, exact positive-weight averages, strict barrier,
   and exact discount.
2. `P_grid`: the same ideal financial function at exact independent
   `Phi_inverse((k+1/2)/N)` drivers. It has no scalar quantile rounding and no
   financial arithmetic or clipping.
3. `P_native`: the proposed signed-restored AS241 output at those SAME raw
   words, followed by the original native financial operation graph, including
   its literal coefficient values, floors, stock clamps and discount.

The fixed route is `P_cont -> P_grid -> P_native`. The audited ideal-grid
bounded-variation argument supplies

```
d = (na+1)*nt
abs(P_cont-P_grid) <= 40*d/N.
```

For the second arrow, require an independently accepted all-input AS241
certificate `abs(Z_native(k)-Phi_inverse(midpoint(k))) <= E`. Use its saved exact
maximum of central and fresh native-tail errors. `E` already includes native
scalar coefficient, Horner, log, sqrt, argument and quotient errors once.
Do not add the old exact-floor quantile ULP, the hypothetical floor-transform
tail arithmetic, Box-Muller pair/cutoff terms, or an AS241 `KS(E)` price term.
The separate AS241 scalar-law theorem is useful evidence for a different ideal
submodel; its numerical bias is not a fourth term in this coupling route.

## Bind the actual financial operation graph

Prerequisites are the successful scalar IR/semantic receipt and its independent
`A02_quantile_scalar_audit_run001` source audit, independent native-transform/law
audits, the accepted ideal-grid audit, original economic
task files, original builder, and the financial portion of the accepted A10
target/source for BOTH cases. A future full target or precisely specified
compositional source must explicitly bind each AS241 scalar output to the
original common/idiosyncratic input interface. A free-normal placeholder or
changed-law claim on the old Box-Muller target is insufficient.

Before evaluating bounds, freeze the new source and all scalar/financial
coefficient literals, source/optimizer fingerprints, economic contracts, proof
code, dependency code, and prerequisite manifests. Compare the actual financial
SSA against the original builder and archived target. Preserve these semantics:

- `mu=(RATE-SIGMA^2/2)*dt`, with `dt=T/nt` and original initial `log(S0)`.
- Positive common/idiosyncratic increment coefficients, all contractual dates,
  and the original common driver shared among assets at a date.
- Hillis-Steele prefixes of RAW log increments. A clipped stock-evaluation log
  is never fed into a later raw prefix. This is not recursive clipped-state GBM.
- Original stock evaluation `exp_estrin(clip(raw_log,lo,hi))`; degree12,
  archived nearest-f40 coefficient literals, actual range-reduction literals,
  actual signed floors, native bit extraction and shifts.
- Basket coefficient `1/na` exactly represented for na4/8, the rounded
  `1/(na*nt)` Asian coefficient, strike/barrier constants, original positive
  part, rounded discount coefficient, and final native multiplication floor.
- `alive iff every native basket < H`; equality is knockout. The Asian strike
  uses a positive part, so equality gives zero. No digital tie is discarded.

The old full-source or leaf-range proofs cannot automatically validate a new
SSA call site. Prove the original native72 semantics and every new whole-source
producer invariant before any compact width, special leaf or clamp deletion is
adopted. Mathematical financial error alone supplies no quantum implementation.
Normalize the new financial SSA against the actual E03 support derivation and
bind its literal arithmetic and hypotheses, without treating the old complete
Box-Muller source hash as a new-source support certificate. Require a NEW
source-matched price ledger: epsilon1/100 dollars, statistical9/2000 dollars,
and residual11/2000 dollars. This AS241 result cannot fill the accepted named
joint-Box-Muller obligation or inherit old E02 source/wrapper resource counts.

## Uniform raw-log discrepancy

Let `a=sigma*sqrt(dt*rho)`, `b=sigma*sqrt(dt*(1-rho))`,
`mu=(rate-sigma^2/2)*dt`, and `L0=log(S0)`. Let `a_hat`, `b_hat`, `mu_hat`,
`L0_hat` denote the ACTUAL archived f40 values. Obtain exact outward errors by
comparing their integer literals with the true analytic quantities. Do not
assume that frontend binary64 conversion equals exact nearest-even rounding.

Use the all-input exact-grid normal range `abs(X)<=G`, with fixed `G=13/2`, only
after binding the saved TRUE-quantile bracket for every q32 midpoint, including
both extreme endpoints. A bound on approximate rational outputs alone does not
prove this premise. Then `abs(Z_native)<=G+E`.
For a signed native constant multiplication, floor contributes less than one
`eps`, including at negative inputs. A uniform per-stock/date bound is

```
inc_error = abs(a_hat-a)*G + abs(b_hat-b)*G
            + (abs(a_hat)+abs(b_hat))*E + 2*eps
            + abs(mu_hat-mu)
Lambda_j = abs(L0_hat-L0) + j*inc_error
abs(raw_log_native(i,j)-raw_log_grid(i,j)) <= Lambda_j.
```

If actual coefficients vary by site, retain the exact site-specific errors and
sum the first j of them; taking their maximum is allowed only after the complete
inventory. All native additions and prefix permutations are exact modulo words,
so they add no new f40 rounding, but their signed overflow must be excluded.
Check every internal prefix as well as the final log. Exact triangle bounds on
`G+E`, all literal products, each prefix, every later stock sum and every
stored72/product144 word must stay inside the corresponding signed/unsigned
limits. A wrapped prefix invalidates the coupling even though a later clamp
would produce a bounded stock.
All eagerly evaluated prefixes and stock sums need safety on the full raw-word
domain, including branches and dates whose final payoff is zero. Do not use an
alive-only bound to validate a dead-path register or typed arithmetic leaf.

## Original native stock exponential

Certify ONE fixed stock-exp template over the WHOLE actual clipped word domain
`[lo_hat,hi_hat]`, then verify each of the 48/416 stock sites matches it. Use
the actual range-reduction integer

```
k = floor(x_raw*C_invln2/S^2)
r_raw = x_raw - k*C_ln2.
```

Signed flooring and signed bit extraction must match the actual graph. The
`k*S` times `C_ln2` multiplication cancels the f40 scale exactly; do not charge
an additional floor there or silently replace actual k by the exact-real
`floor(x/log(2))`. Reconcile the fixed classes k=-17..12 with complete integer
word coverage of the clipped domain. Empty classes may be recorded, not omitted
from a completeness argument.

Expand the actual Estrin add/multiply DAG with its raw coefficients. Bound its
coefficient differences, degree12 Taylor remainder, every floor including the
power-square subgraphs, and all intermediate magnitudes. Account for
`C_ln2/S-log(2)` at the actual k. A left shift is exact only after proving no
overflow; a right shift of a positive word contributes an ADDITIVE `eps`, rather
than a large artificial relative error at the smallest stock.

Require a saved pair of uniform bounds `alpha>=0`, `beta>=0`, `alpha<1`:

```
(1-alpha)*exp(x) - beta <= Exp_native(x)
Exp_native(x) <= (1+alpha)*exp(x) + beta
for every native clipped argument x.
```

Include all range reduction, coefficient, polynomial and shift errors in those
bounds. Verify positivity at every native stock site and all supported-domain
stored/product/shift widths. The original E03 support proof is reusable only
after normalized structural/literal equality is proved for the new financial
subgraph; its old Box-Muller source hash alone is not a new-source support proof.
The 464 stock sites are not an exclusion rule: inventory every actual native
exponential site and certify any additional strike/payoff/discount site if the
new graph contains one. The original discount is an archived constant, not a
free runtime exponential. Every site requires positivity and width safety even
when its final path payoff is dead.

## Treat stock clamps without a tail event

The lower clamp cannot be assumed inactive. The first fixed method includes it
deterministically. On a path without a native upper-clamp event, define

```
L = exp(lo_hat)
a_j = (1-alpha)*exp(-Lambda_j)
b_j = (1+alpha)*exp( Lambda_j)
l = (1+alpha)*L + beta.
```

For the exact-grid ideal stock `S_ij>0`, native stock satisfies

```
a_j*S_ij - beta <= S_native(i,j) <= b_j*S_ij + l.
```

Indeed, `exp(max(raw_log_native,lo_hat))` is no smaller than the unclamped
native-log exponential and no larger than that exponential plus `L`. This
charges the rounded lower-clamp constant and all native exp error. It needs no
claim that a very low stock is rare or irrelevant to the basket/Asian payoff.

Remove an upper-clamp event ONLY after both of these interval guards are proved,
for every case/date:

```
Exp_native(hi_hat) >= na*H
exp(hi_hat-Lambda_j) > na*H.
```

With all stocks nonnegative and basket coefficient exactly `1/na`, the first
forces a native monitored basket at least H; the second forces the exact-grid
ideal basket above H. Both complete payoffs are therefore zero at any such
date. The original all-date barrier remembers that violation even if later
stocks fall. This proof uses na<=8 and the ACTUAL hi/exp lower bound; it is not
an assertion that upper clipping is generally harmless. No Gaussian law is
conditioned on this event or on its complement. If either guard fails, stop the
fixed certificate rather than omit the event.

## Basket bands and transfer under the exact grid

Exact native stock sums must not overflow. The actual power-of-two basket mean
has at most one `eps` downward floor. On the no-upper-clamp domain,

```
a_j*B_j - (beta+eps) <= B_native_j <= b_j*B_j + l,
```

where `B_j` is the exact-grid IDEAL positive-weight basket. Require `l<H` and
`a_j>0`. A strict barrier-decision disagreement implies the closed ideal band

```
L_j = (H-l)/b_j
U_j = (H+beta+eps)/a_j
B_j in [L_j,U_j].
```

Native equality is included. Both nonnegative payoffs are zero outside the
removed upper-clamp domain, so these unconditional bands still cover every
remaining switch. Do not condition a Gaussian density theorem on survival,
small errors, the absence of clamps, or a coupling good event.

At original observation time `t_j=j*T/nt`, condition only on the continuous
idiosyncratic drivers. The ideal basket factorizes as

```
B_cont_j = W_j*exp(s_j*Z),   W_j>0,
Z standard Gaussian independent of W_j,
s_j^2 = sigma^2*rho*t_j.
```

The variance uses the accumulated common Brownian driver through date j, not
the one-step variance `sigma^2*rho*dt`. The fixed probability method is the
unconditional shift-uniform DENSITY bound

```
v_j = min(1, log(U_j/L_j) / sqrt(2*pi*s_j^2)).
```

No numerical common factor, basket realization, or financial sample enters it.
The exact-grid band is not a Gaussian variable. Transfer the event instead:
it depends on `d_j=(na+1)*j` independent ideal driver coordinates. Fixing every
other coordinate, the positive ideal basket is nondecreasing in the remaining
one. The indicator of a CLOSED finite basket band therefore has total variation
at most two, including finite-grid endpoint ties and the case of no dependence.
The midpoint/product bounded-variation bound yields

```
P_grid(B_j in [L_j,U_j]) <= min(1, v_j + 2*d_j*2^-33)
                        = min(1, v_j + d_j/N).
p_switch <= min(1, sum_j min(1, v_j + d_j/N)).
```

This `d_j/N` is a band-probability term, distinct from the once-paid full-price
ideal-grid term `40*d/N`. Quantile E enters `Lambda_j` only. Do not replace this
transfer with the AS241 KS bound, add both transfers, or claim finite paired
Box-Muller independence.

## Smooth Asian and native discount errors

Only a path where BOTH flags are alive needs a smooth-payoff discrepancy.
Then every ideal basket is below H. Original native basket survival also implies
`sum_i stock_native(i,j)_raw < na*H_raw` exactly: its coefficient is `1/na`, H is
an exact f40 constant, and an integer floor below H cannot hide a sum at least
`na*H_raw`. Thus both unrounded asset/date stock averages are below H.
This does NOT imply the rounded native Asian average is below H: its coefficient
can exceed `1/(na*nt)`. The native Y<40 support proof must charge that coefficient
and output floor, the exact strike and the actual rounded discount separately.
An exact-integer support route, contingent on all positivity/no-overflow and
structural premises, is

```
sum_all_stock_raw <= m*H_raw - nt
A_raw <= floor(Cavg*(m*H_raw-nt)/S)
Y_raw <= floor(Cdisc*max(floor(Cavg*(m*H_raw-nt)/S)-K_raw,0)/S)
require this ACTUAL literal upper bound < 40*S.
```

Here `Cavg` and `Cdisc` are the archived INTEGER coefficient parameters, not
exact-real reciprocals or discounts. This inequality has not been evaluated
here. It is a required new-source support obligation and cannot be replaced
by the assertion that the unrounded mean is below H.

Set `delta_j=max(1-a_j,b_j-1)`, with the certified guards `a_j<=1<=b_j`.
The fixed conservative mean-stock discrepancy on this domain is

```
mean_stock_error <= (1/nt)*sum_j (H*delta_j + max(beta,l)).
```

Let `cA` be the actual rounded native Asian coefficient divided by S and
`m=na*nt`. Charge its literal difference and its one output floor:

```
epsilon_A = mean_stock_error + m*H*abs(cA-1/m) + eps.
```

The balanced stock sums and strike subtraction add no rounding after overflow
is excluded. Strike100 is exact. Positive part is 1-Lipschitz. With the actual
native discount literal `D_hat`, exact discount `D=exp(-rate*T)`, and proven
`0<D_hat<=1`, an ALREADY-DISCOUNTED smooth bound is

```
zeta = D_hat*epsilon_A + 40*abs(D_hat-D) + eps.
```

The final `eps` charges native discount multiplication floor. Bind the original
discount coefficient by its exact word; no second discount is applied. Reprove
or structurally adopt `0<=Y_native<40` for the new source and retain
`0<=Y_grid<40`. Hence the payoff difference on a switch is at most 40, not 80.

The one fixed prospective full financial-bias expression is

```
abs(P_native-P_cont) <= 40*d/N + zeta + 40*p_switch.
```

There is no missing tail term set to zero: the finite-grid/native comparison
is all-input, lower clipping is deterministic, and upper-clamp events have a
proved BOTH-path zero-payoff identity. Failure of a required domain/overflow/
support/clamp premise means no full certificate, not a zero error contribution.

## One future bounded attempt and its stopping rule

After root clears Stage C timing and the prerequisite scalar/source receipts
pass, separately review and freeze one producer protocol. Suggested fixed method:

- BOTH B4x12 and B8x52 once; q32/native72/f40, archived financial source, saved
  all-input scalar E, and fixed G=13/2. No new sampler settings.
- One90-digit outward interval calculation with exact rational saved endpoints;
  exact integer/SSA completeness and overflow checks. Reconcile all coefficient
  literals and all 464 stock template bindings.
- The same30 k classes and degree12 actual Estrin/Taylor proof; no adaptive grid,
  alternate polynomial, higher precision, or post-outcome coefficient change.
- The same deterministic lower-clamp allowance, both upper-knockout guards,
  and density band method at all 12/52 original dates. No rare-event optimization
  or centered-interval alternative in this first attempt.
- CPU180 seconds including fixtures and reconciliation; one terminal receipt
  preserving failed/censored prerequisites and every completed bound. A later
  retry, alternate tail treatment or method needs a fresh version/receipt.
- Before the attempt, require the NEW source-matched ledger to bind the original
  epsilon1/100-dollar objective, statistical9/2000-dollar allowance, and
  residual11/2000-dollar allowance. Compare this route's total with that residual
  only. Retain each component and each case independently. No weaker target or
  revised allocation after reading an outcome; no insertion into the accepted
  joint-Box-Muller error row and no transfer of old E02 gate costs.
- Zero financial sampling, quantum observations, gate replay, synthesis,
  native leaf dispatch changes, or classical timing reruns. Bounded fixtures
  must check proof identities, endpoint ties, signed floors, clamp guards,
  source mutations and error accounting; their exact list/count is frozen
  separately before execution.

An accepted mathematical result would be a full original-contract bias bound
for the precisely bound NEW native AS241 financial function. It would not adopt
that sampler, certify reversible scalar/financial gates or cleanup, validate
old leaf ranges at new call sites, supply hardware seconds, settle classical
reference coverage, or establish quantum advantage. A failed/censored result
keeps all those conclusions open and does not replace the accepted source.

## Local evidence read for this preflight

- `quantile_grid_certificate.py`, `audit_quantile_grid.py`, and
  `C06_quantile_grid_audit_run001`: ideal-grid price BV/telescope and original
  economic/strict-barrier template.
- `barrier_band_certificate.py`, `C07_bound_date1_run001`, and
  `C06_pair_audit_run001`: accumulated common-factor variance and unconditional
  one-date band theorem. The one-date native Box-Muller discrepancy is not
  transferred to AS241 or to later dates.
- Original `barrier_oracle_depth.py`, archived A10 `ir.py`, and E03 support
  receipts: stock-only clamp location, signed native floors, actual Estrin
  financial structure, and conditional new-source support obligations.
- `AS241_SCALAR_IR_PREFLIGHT.md` and the author-stage native transform/law files:
  the distinct signed-restored sampler, eagerly paid unused-branch guards,
  archived coefficients, fresh rho accounting and actual-gate boundaries.
