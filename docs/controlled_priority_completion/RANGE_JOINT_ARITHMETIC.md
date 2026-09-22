# Joint f40 arithmetic expectation certificate

**Status: deterministic certificate, independently reviewed by a separate AI
agent for the stated scope.** The
executed interval bounds are $0.000099876 (C4), $0.000051936 (C8), $0.000011763
(H4), and $0.000021978 (H8). They fit the numerical allocation after the already
certified finite-law/guard/control bridge. This does not certify policy regret,
the separately estimated baseline mean, or a tight second moment. It concerns
the joint expectation of the **digital** baseline and digital correction using
the **same digital exercise decision** on the **same q32 guarded path**. It does
not assert closeness to the old real-arithmetic policy or its exercise decision.
Existing baseline timings and certificates cannot be reused without a proved
transfer to this same digital baseline.

The implementation is `range_joint_arithmetic.py`, and the full numerical
ledger is `results/controlled_priority_completion/range_joint_arithmetic.json`.
All constants used below are evaluated by 80-digit interval arithmetic; stored
binary64 upper endpoints are rounded outward. No sampled maximum enters the
certificate. The intermediate no-overflow result is in `RANGE_AUDIT.md`.

## Elementary functions and the radial singularity

Write `u=2^-40`. Each stored log/cos/CDF coefficient is independently checked
against an interval formula. For normal CDF constant terms, the code evaluates
the entire integrated Gaussian power series through index 180 and encloses its
alternating remainder by the next term. At every center `|x|<8`, terms decrease
well before index 180. Higher CDF coefficients use exact probabilists' Hermite
polynomials times the interval Gaussian density. Log coefficients use their
closed forms; cosine coefficients use interval sine/cosine. This verifies all
2,848 coefficients without trusting their 90-digit generation routine.

For a Horner polynomial with local-coordinate radius `h<1`, coefficient error
at most `rho` and less than one `u` per fixed multiply give arithmetic error at
most `(rho+u)/(1-h)`. Add the analytic Taylor remainder:

- log: `h=1/64`, remainder at most `h^9/9`;
- cosine: `h=1/128`, remainder at most `(2*pi*h)^8/8!`;
- normal CDF: `h=1/32`, remainder at most
  `phi(0)*(8^7+21*8^5+105*8^3+105*8)*h^8/8!`.

CDF tail clipping adds `phi(8)/8`. Log normalization adds at most one `u`
for mantissa truncation and `40*|L-log(2)|` for the stored ln(2) coefficient.
For the Box--Muller inputs below one, normalization shifts left exactly, so
the mantissa truncation term is omitted.

For exp, the actual source has `|k|<=18`, `2^k<=8192` and reduced argument
`|r|<=0.694` on every financial exponential input in `[-12,9]`. The source's
integer range-reduction identity remains valid even if coefficient rounding
changes `k`. The proof pays the degree-12 Taylor remainder, every coefficient
error and Horner rounding, `exp(0.694+18*delta)*18*delta` for the ln(2)
coefficient error `delta`, and one final right-shift `u`. The code executes exact
integer checks of `k` and `r` over all `Xraw in [-12Q,9Q]`, where `Q=2^40`.
All guards, future
geometric means and analytic-control exponential arguments are inside this
domain. The resulting uniform exponential error is below `1.084e-7`.

The resulting uniform log errors are below `8.282e-12` for normal inputs and
`9.191e-12` generally; cosine error is below `1.374e-12`, CDF error below
`2.697e-11`.

For midpoint `U_q`, let `h=2^-32`, `r=sqrt(-2 log U_q)` and `r_max=sqrt(-2log(h/2))`.
The increasing function `1/sqrt(-2log u)` has integral `sqrt(pi/2)`. Shift the
first `2^32-1` midpoint rectangles to their right, and bound the final midpoint
separately, to obtain

```
E[1/r] <= sqrt(pi/2) + h/sqrt(-2log(1-h/2))
       <= sqrt(pi/2) + sqrt(h).
```

The nonnegative square-root map obeys
`|sqrt(max(a+e,0))-sqrt(a)| <= |e|/sqrt(a)`. Consequently

```
E[radial arithmetic error] <= 2*e_log*E[1/r] + u,
E[normal arithmetic error] <= (1+e_cos)*e_radial + r_max*e_cos + u.
```

This integrates the sensitivity near `u=1`; it never treats a uniform normal
approximation error as an expectation bound. Midpoint radial expectation is
bounded by `sqrt(pi/2)+h*r_max`. The executable certificate then checks
`E|Z_digital| <= (1+e_cos)*(sqrt(pi/2)+h*r_max+e_radial)+u < 2`, so each
coefficient-error term multiplying a digital normal is charged by this cap.

## Path and control error ledger

Every relevant rounded financial scalar is independently enclosed against its
decimal-model expression: log spot/guards, normal loadings, drift, discount,
support, averaging coefficients, mean return, geometric variance/mean shift,
and every component-call variance/mean shift. Each absolute constant error is
verified below `u`. Policy-fitting coefficients are not used in this argument:
the policy value cancels below and its final clamps are bounded separately.

Let `a,b` be the exact common/idiosyncratic normal loadings, `e_Z` the expected
normal arithmetic error, and `e_E` the uniform exp error. A log increment costs

```
e_step <= (a+b)*e_Z + 7*u.
```

The seven units pay two coefficient errors times `E|Z_q|<2`, two fixed
multiplications and the drift constant. Initial log rounding and both possible
guard/reset discrepancies give, at date `j`,

```
e_log,j <= 3*u + j*e_step,
e_stock,j <= 4097*e_log,j + e_E.
```

The derivative cap 4097 covers the tiny rounded guard displacement above 4096.
The code also bounds actual digital stock maxima, accrued values and expected
future average, and checks `|EA_d-k_d|<8500` using the stored coefficients.
The code then sums these expectation bounds, explicitly paying every rounded
averaging coefficient against its full finite-input range and every fixed
multiply. For example, future stock averaging adds `(d*n*4097+1)*u`, and
future log averaging adds `(d*n*12+1)*u`. This produces bounds for accrued value,
future arithmetic/geometric averages, tau basket, forward, and residual.

The analytic geometric and component controls have fixed, known positive
variances. Their stored variances and integer square roots are enclosed
directly, rather than bounding a small denominator with sampled values.
For `k>0`, `k>=u`, `k<=200`, `mu in [-12,9]` implies `|mu-log k|<40`.
With exact standard deviation `s`, digital deviation `s_d`, and certified
`delta_s`, division and log errors obey

```
e_d2 <= (e_log + 40*delta_s/s)/s_d + u,
e_d1 <= e_d2 + delta_s.
```

Normal-CDF propagation uses the global derivative bound `1/sqrt(2*pi)`.
Every relevant lognormal mean is below 5000; strike is at most 200 on the
positive-strike branch. Thus the implemented call or put differs from the
exact formula at its digital `mu,k`, but exact fixed model variance, by at most

```
(1+e_CDF)*e_mean
 + 5200*(e_CDF + (e_d2+delta_s)/sqrt(2*pi)) + 2*u.
```

The nonpositive-strike branch is paid by `e_mean`. Positive-part clipping is
nonexpansive. To compare digital state inputs with ideal finite-path inputs,
puts have strike sensitivity at most 1 and log-mean sensitivity at most 200;
calls have strike sensitivity at most 1 and log-mean sensitivity at most 5000.
All discounts, sums, averaging and products are paid in the machine-readable
ledger. No assumption about stability of the exercise decision is made.

## Why the policy value cancels, and final clipping is paid

Let `V_d` be the implemented policy value, `d=1(V_d>Kc)`, `D_d` its rounded outer
discount, and let exact finite-path Gaussian-control quantities be `c0,R`.
All arithmetic here is real interpretation of the already range-certified
fixed-point outputs. Before final correction clipping,

```
(V_d-Kc)+ + d*(c0_d-V_d-R_d) = d*(c0_d-Kc-R_d).
```

This identity requires no approximation bound on moment matching or regression.
The digital baseline multiplication introduces at most `10000*u+u`: range
audits put `V_d` well below 10000, the constant discount error is below `u`,
and the final fixed multiply loses less than `u`.
An additional executable domain check propagates the actual exponential/CDF
bounds through the lower/upper clamps and explicitly verifies `V_d<10000`.

Write exact continuation bounds `L,U`, and define `V*=clip(V_d,L,U)`. Because
the actual program clamps `V_d` to digital `L_d,U_d`, projection error is at
most `max(|L_d-L|,|U_d-U|)`. For
`L=max(F,0,geocall)` and `U=max(L,min(c0,scaled_average_calls))`, an expectation
bound is

```
e_projection <= 2*e_lower + e_c0 + e_upper_average.
```

The exact relations `F<=L<=U<=c0`, `0<=R<=B`, and `c0-L<=B` imply
`|d*(c0-V*-R)|<=B`, irrespective of whether `d=1(V*>Kc)`. Thus clipping the
digital correction to rounded support `B_d` changes its unrounded value by at
most `|c0_d-c0|+|R_d-R|+|V_d-V*|+|B_d-B|`. The final joint expectation bound is

```
e_joint <= (10000*u+u)
         + D*(2*e_c0 + 2*e_residual + e_projection + u).
```

This pays the final clip explicitly. It compares with the real finite-path
joint expression using the **implemented decision d**. The earlier financial
bridge still pays law/guard/control bias, and the regret of this particular
decision remains a separate nonnegative term. Existing regret samples from a
different real-arithmetic policy cannot be silently reused.

## Reproduction and interpretation

```
.context/antithetic_feasibility_env/Scripts/python.exe -m research.controlled_priority_completion.range_joint_arithmetic
.context/antithetic_feasibility_env/Scripts/python.exe -m pytest research/controlled_priority_completion/test_range_joint_arithmetic.py -q
```

Eight tests passed: independent high-precision references inside the erf-series
intervals; exhaustive finite midpoint checks of the reciprocal-radius inequality
at smaller bit counts; difficult fixed lognormal inputs against high-precision
analytic prices; and budget checks for all models. These tests supplement the
inequalities and interval calculation; they are not substitutes for them.

No measured quantum runtime, financial advantage, baseline-mean confidence,
finite-policy regret, or tight residual moment certificate follows from this
arithmetic result.
