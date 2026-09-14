# Cancellation-aware grid bound

This tightens V2A's h/2 term without changing its support, point-density circuit
weights, total-variation correction or payoff scale. It is a standard
density-expansion/remainder argument, not a novel quantum algorithm. Claims are
in exact arithmetic; the implementation uses tested, ordinary floating point.

Let cell i be [l_i,r_i], mapped to grid point x_i. Write f for the lognormal
density and g(s)=(s-K)+. The conditional quantization error is

`(1/m) sum_i integral_cell (g(x_i)-g(s))*f(s) ds`.

Expand f(s)=f(x_i)+(f(s)-f(x_i)). Define

`A_i = (r_i-l_i)*g(x_i) - ((r_i-K)_+^2-(l_i-K)_+^2)/2`.

This integrates the payoff difference against a **constant** density, not the
true distribution. Interior cells entirely above or below K have cancellation;
the formula also covers the kink cell and asymmetric endpoint cells.

Set `L_i = sup_cell |f'(s)|`. The call is 1-Lipschitz and the mean-value theorem
gives `|f(s)-f(x_i)| <= L_i*|s-x_i|`. Consequently, the absolute remainder on each
cell is at most

`L_i*((x_i-l_i)^3+(r_i-x_i)^3)/3`.

Retain the signed constant-density sum before taking its absolute value. A valid
conditional quantization bound is therefore

`Q_new = (abs(sum_i f(x_i)*A_i) + sum_i remainder_i)/m`.

Both Q_new and h/2 are valid, so take their minimum. The complete grid bound is

`B_grid_new = D*(min(h/2,Q_new) + (U-K)*TV(w,pi))`.

As before, w are integrated conditional cell masses used in the correction and
pi are the circuit's normalized point-density weights. The method does not
replace pi with w. The tighter bound cannot exceed the old one in exact arithmetic.

## Derivative extrema, not a sampled maximum

For log S~N(mu,s^2), put v=(log(x)-mu)/s^2. Then

`f'(x) = -f(x)*(1+v)/x`,

`f''(x) = f(x)/x^2 * ((1+v)*(2+v)-1/s^2)`.

The two possible interior stationary points of f' occur at

`v=(-3 +/- sqrt(1+4/s^2))/2`, `x=exp(mu+s^2*v)`.

Evaluate |f'| at both cell endpoints and at each such point that lies inside the
cell. This supplies the supremum analytically. Numerical dense-sample comparisons
are regression tests, not the justification for an upper bound.

## Scope and cost

No Black-Scholes answer, exact finite-grid payoff expectation or exact encoded
objective is consulted by the bound routine. Diagnostics use those quantities
only after budgets are formed. Integration of elementary payoff polynomials and
evaluation of densities/CDFs/derivatives are still classical preprocessing,
scaling with the number of grid points. This cost must enter later comparisons.

The combined support/grid/encoding bound and affine price interval use the V2A
derivation unchanged. A positive remaining probability-radius budget does not
mean that any specified finite-shot procedure has achieved that budget. Integrated
price-interval tests use constructed containing probability intervals; they are
not new statistical coverage experiments, noisy-circuit tests or hardware evidence.
