# Finite-law financial bridge and remaining certificate

22 September 2026. This follows the **same** controlled compound Asian-basket
source. It closes its real-arithmetic probability-law and analytic-control bias
obligations at 32 random bits. It does **not** close P4: the implemented financial
arithmetic and finite-policy regret remain uncertified. No held-out case or new
advantage direction was used.

The executable bounds in
[financial_bridge.json](../../results/controlled_completion_followup/financial_bridge.json)
are deterministic expectation bounds, evaluated with 70-digit interval arithmetic
and outward-rounded binary64 output. They use no sampled maximum, price sample,
quadrature estimate, or fitted boundary density.

| Model | Gaussian midpoint law | Guarding and tau reset | Analytic-control bias | Total, dollars |
|---|---:|---:|---:|---:|
| C4 | 0.000003504 | <3e-76 | 0.000002700 | 0.000006204 |
| C8 | 0.000007008 | <4.01e-20 | 0.000005400 | 0.000012407 |
| H4 | 0.000011794 | 0.000000794 | 0.000010009 | 0.000022596 |
| H8 | 0.000015543 | 0.000000589 | 0.000012859 | 0.000028990 |

Displayed totals are rounded upward; use JSON for full precision. All three
compound strikes have the same bounds. These terms leave at least $0.001971 of
the $0.002 numerical budget for arithmetic. At 16 random bits this particular
bound is $0.3592/$0.7184/$1.2148/$1.6093 and fails. A failed upper bound does not
establish a true expectation error of that size.

## Coupling midpoint Box--Muller, including its singular first cell

Let h=2^-q, Q map each cell to its midpoint, r(u)=sqrt(-2 log u),
R=r(h), and Rm=r(h/2). Couple each continuous uniform with Q(U). Integration by
parts and the Gaussian Mills upper bound give

    I(x) = integral_0^x r(u) du <= x [r(x)+1/r(x)].

The absolute radial error in the first cell is exactly 2 I(h/2)-I(h), at most
h[Rm-R+1/Rm]. On all other cells, monotonicity bounds the summed error by hR/2.
Consequently

    er = E|r(U)-r(Q(U))| <= h[Rm-R/2+1/Rm],
    ez = E|Z-Zq| <= er + pi*h[sqrt(pi/2)+er].

The angular term follows from the 1-Lipschitz sine/cosine functions and
|2pi V-2pi Q(V)|<=pi h. The same bound holds for each of the paired normal
coordinates. At q=32, ez <= 1.750592522e-9. No uniform error for all continuous
U is asserted; the normal tail is integrated, including U approaching zero.

For one asset's log increment define

    e_step = sigma*sqrt(dt)*(sqrt(rho)+sqrt(1-rho))*ez.

Dependence between adjacent paired coordinates does not affect this triangle
bound. All four models have an **even** number n(d+1) of normal coordinates
before tau. Thus no Box--Muller pair straddles the exercise/future split, and
future words are independent of the past. This premise is checked by tests.

Let N=2n be the number of dates and M=4096. Clipping log spots is nonexpansive;
exp(clip(log spot)) is M-Lipschitz. The source resets its log state only at tau.
Coupling the continuously driven guarded process to its finite-word counterpart
therefore gives E|Sbar_j-Sq_j| <= M*j*e_step, including dates after the reset.
The discounted compound-price difference is bounded by

    e_quant <= exp(-rT)*M*e_step*(N+1)/2.

To justify the outer option as well as the inner payoff, couple independent
future increments conditional on each pair of past histories. Conditional
expectation contracts L1, and both call positive-part maps are 1-Lipschitz.
Quantized histories need not determine the continuous exercise state exactly.

## Tail and reset error

Write ell=2^-16, L_t=log S_t and g(s)=clip(s,ell,M). For an original continuous
GBM path and the continuously driven guarded/reset path,

    E|S_t-Sbar_t| <= T_S(t),                              t<=tau,
    E|S_t-Sbar_t| <= T_S(t)+exp(r(t-tau))*T_S(tau),       t>tau,

where T_S(t)=E|S_t-g(S_t)|. The second term explicitly pays for resetting at tau:
the future multiplicative GBM factor is independent and has mean exp(r(t-tau)).
Average these bounds over all fixings and multiply by exp(-rT).

For L~N(mu,v), sd=sqrt(v), define zlo=(mu-log ell)/sd,
zhi=(log M-mu)/sd, and ztilt=(log M-mu-v)/sd. All three are positive for every
date/model here. Let phi be the standard-normal density and f(z)=phi(z)/(1+z²).
The Mills lower inequality Q(z)>=phi(z)*z/(1+z²) implies

    T_log <= sd [f(zlo)+f(zhi)],
    T_S <= ell*sd*f(zlo) + exp(mu+v/2)*sd*f(ztilt).

The stock bound also uses 1-exp(-x)<=x and exponential tilting of the Gaussian.
Thus the executable certificate needs only interval exp/log/sqrt and avoids
subtracting nearly equal normal tails. These are conservative upper bounds,
not purported exact tail integrals. Independent tests compare them with the
closed-form normal/lognormal stop-loss formulas.

## The finite-law control is biased, and the bias is now bounded

Let Cq denote the true finite-law continuation, computed in exact real
arithmetic with the specified spot guards. The source instead uses Gaussian
analytic F and Pg at its finite guarded state Xq. For its real residual Rq,

    c0(Xq)-E[Rq|Xq] = Cq(Xq)+b(Xq),
    b = d1/2 { E_Gauss[A|Xq]-E_fin[Aq|Xq]
               + E_Gauss[(k-G)+|Xq]-E_fin[(k-Gq)+|Xq] }.

Here d1=exp(-r(T-tau)), and the virtual Gaussian future starts at the finite
guarded tau state but has no subsequent spot guard. The two conditional laws
are different. To bound their **average** discrepancy, couple that virtual
future with the original continuous path and finite path. Let bars over T
denote an average over the future contractual dates, and let
Rbar=mean_j exp(r*j*dt). Then

    E|A_virtual-Aq| <= bar(T_S) + Rbar[T_S(tau)+M*n*e_step]
                      + M*e_step*(n+1)/2,
    E|mean(log S_virtual)-mean(log Sq)|
                   <= bar(T_log)+T_log(tau)+e_step*(3n+1)/2.

For k<=2K, the map x -> (k-exp(x))+ is k_+-Lipschitz and hence 2K-Lipschitz.
This avoids an invalid global Lipschitz assertion for the geometric mean as
a function of arbitrarily small stock levels. Therefore d0 E|b| is at most
d0*d1/2 times the first displayed bound plus 2K times the second.

The old exact identity really is false for this source. The JSON contains
interval-verified reachable C8/H4/H8 states obtained with every radial word 0
and angular word 2^(q-3), q=32. Every tau stock is guarded to 4096; the accrued
contribution exceeds K, so k<0 and all puts vanish. Finite future A<=4096, whereas
the Gaussian analytic mean is 4096*Rbar>4096. The conditional bias is at least
$17.7492/$52.2398/$48.4778 before outer discount. The H8 witness past-word event
has probability 2^-3456; this refutes exact or uniformly tiny control transfer,
while being consistent with the small certified **expectation** bias above.

## Policy boundaries, regret, and the complete error statement

For any past-measurable decision d, including the implemented comparison, set

    regret_q = (Cq-Kc)+ - d(Cq-Kc) >= 0.

If the exact real baseline and residual use a common policy value V and
d=1(V>Kc), then their V terms cancel:

    (V-Kc)+ + d(c0-V-Rq) = d(c0-Kc-Rq).

Thus no density assumption or sampled absence of exercise mismatches is needed
to bridge the **joint** price. Instead, arithmetic must bound the joint error
relative to the same implemented decision, and that decision's finite-law
regret must be paid. Writing e_arith for this discounted joint arithmetic error,

    |P_cont - (E[base_d]+d0 E[Y_d])|
      <= e_clip + e_quant + d0 E|b| + e_arith + d0 E[regret_q].

This is a usable complete decomposition, with the first three terms closed.
It is not a proof that the remaining terms vanish. The final source clipping of
Y is included in e_arith, as are baseline rounding and use of an approximate
discount. It cannot silently be removed from that obligation.

A sound finite-law regret certificate can use independent future samples and
Z=c0-mean(Rq). For h_d(x)=(x-Kc)+-d(x-Kc), convexity and 1-Lipschitz continuity give

    regret_q <= E[h_d(Z)|Xq] + |b(Xq)|.

This formula remains valid at policy boundaries. Evaluating it requires a
fresh finite-law certificate or a proved transfer for the existing statistic.
The archived continuous-law sampling result does not become such a certificate
by algebra alone. H8's archived upper bounds $0.009067/$0.006818/$0.005056 already
miss the allocated $0.003 at all strikes. Those are failures of that certificate,
not lower bounds on true regret.

Similarly, the source's exact output clipping retains the unconditional
E[Y_d²]<=B² bound. This is the rigorous moment replacement. Transferring the
tighter archived moments needs an L2/source or policy-mismatch bound; a small
expectation bias in the *sum* of baseline and residual does not provide it.

## Arithmetic: one uniform claim falsified, high precision still open

[financial_arithmetic_edges.json](../../results/controlled_completion_followup/financial_arithmetic_edges.json)
contains 128 deterministic corner cases across all models and both precisions.
Exact integer reconstruction found no signed pre-reduction overflow in those
cases. This is a diagnostic, not exhaustive verification of the input space.

There is a stronger, interval-certified counterexample at f=24/q=16. For H8,
every radial word 0 and angular word 8192, compound strike 6:

    digital baseline = 3106.3320588469505, digital Y = 0,
    exact finite-law real baseline in
        [3106.337232657013, 3106.337232657014],
    absolute arithmetic error > 0.005173810063272295.

The interval calculation uses the actual past paths and guards. Since k<0,
the geometric puts vanish and the continuation interval collapses to the
analytic forward, so no numerical normal CDF or quadrature is needed to certify
the reference. This reachable input **refutes a uniform $0.002 arithmetic bound
at f=24**. Its rarity means it does not refute a $0.002 expectation bound.

For f=40/q=32 the largest edge baseline discrepancy is about 1.020e-7, larger
than the previous small random diagnostic but still small. It is explicitly
not a uniform certificate. The remaining precise obligation is an expectation
or uniform bound on the joint financial output, including coefficient rounding,
Taylor remainders, all fixed-point shifts/divisions, intermediate signed ranges,
and final clipping, below the residual numerical margins in the JSON (H8:
$0.001971010429168483). Leaf permutation correctness and a bounded final Y do
not establish correct intermediate financial values.

No full 99% financial certificate is claimed. The law/control analysis is a
completed partial closure; arithmetic, finite-policy regret, the separately
estimated surrogate mean, and any use of tight moments remain explicit gates.

## Reproduce

From the repository root, use the existing numerical environment:

```powershell
.context/antithetic_feasibility_env/Scripts/python.exe -m research.controlled_completion_followup.financial_bridge
.context/antithetic_feasibility_env/Scripts/python.exe -m research.controlled_completion_followup.financial_arithmetic_audit
.context/antithetic_feasibility_env/Scripts/python.exe -m pytest research/controlled_completion_followup/test_financial_bridge.py -q
```

The implementation is in
[financial_bridge.py](../../research/controlled_completion_followup/financial_bridge.py)
and [financial_arithmetic_audit.py](../../research/controlled_completion_followup/financial_arithmetic_audit.py).
The tests check the singular first-cell integral, tail inequalities, all
model/date premises, every q32 law bound, the reachable control counterexamples,
and the certified f24 arithmetic failure. The inequalities and interval
enclosures carry the guarantee; tests are independent error detection.
