# Week 13 alternative audit: Heston and remaining Asian exposure

2026-09-16. One bounded research block under the Week 13 alternative-audit
allowance. Read-only source inspection and primary-literature research; no
experiments, implementation, commits, or changes to the main route. No quantum
advantage, full proof verification, or market CVA result is claimed.

**Route decision:** retain the small Asian-basket raw/geometric-control encoding
work. Heston remains a theorem-to-resources audit with applicability unestablished.
Retain the signed Asian exposure below as a specified research candidate only;
neither alternative passes an implementation/promotion gate in this audit.

Repository basis: [shortlist follow-through](SHORTLIST_FOLLOWTHROUGH.md),
[rescue research](QUANTUM_RESCUE_RESEARCH.md),
[diagnostics code](../../research/journal_sprint/shortlist_diagnostics.py),
[Week 12 closeout](WEEK_12_CLOSEOUT.md), and
[Week 13 scope](WEEKS_11_16_IMPLEMENTATION_PLAN.md). Inspection confirms that
`heston_conditions` evaluates scalar inequalities only and always returns
`full_theorem_applicability="not_established"`. `nested_diagnostic` has an exact
Gaussian inner mean and explicitly labels itself avoidable nesting. Its observed
level variances establish nothing about the Asian target below.

## Heston: theorem dependency audit

[Herman et al., v1](https://arxiv.org/html/2602.03725v1), Definition 2.5,
Sections 5.2.2 and 6.2, Theorems 6.4–6.6, and Appendix D.4: Theorem 6.6 gives
constant-success additive-error pricing with gate complexity
`O-tilde(poly(d,T,B)/epsilon)` for piecewise-linear, B-Lipschitz path payoffs.
Here T counts monitoring steps. Its derivation inherits the truncation and
discretization restrictions; the short theorem statement does not repeat them.
Variance drivers are independent across assets, with own-asset leverage and a
correlation matrix for residual equity drivers. This is not arbitrary joint
Heston correlation. Arithmetic Asian calls fit the payoff class; geometric
controls do not automatically inherit its piecewise-linear argument.

The sampler needs Gaussian/chi-square primitives, recursive CIR endpoints,
endpoint-conditioned integrated variance, correlated Gaussian equity increments,
and reversible payoff arithmetic. Integrated-CIR loading uses Fourier inversion
of a Bessel-function characteristic function. With variance cutoff H, interval
width w, grid N and loading error e, its displayed bounds are
`N=Omega(exp(H)*w/e)` and
`O(H^4*[log^2(N)*log^2(H*N/w)+log^3(N)])` gates.
Near-zero integrated variance also needs exclusion. These are asymptotic bounds,
not compiled costs. The loading corollary contains an apparent copied Lévy-area
cross-reference; Equation 5.12 identifies the CIR distribution. This warrants
checking before implementation, not silently correcting the source.

For clarity, the existing code's scalar checklist, required for each asset, is:

```text
kappa, theta, sigma, Delta > 0; |rho| <= 1; eta=4*kappa*theta/sigma^2
Delta >= 1
exp(-kappa*Delta/2)+exp(-kappa*Delta) < 1
0 <= 2*kappa*sigma*rho-rho^2*sigma^2 < kappa^2
(1+exp(-2*kappa*Delta))/4
  +(rho*sigma/kappa)*(1-exp(-2*kappa*Delta))/4
  < 1/(2*(1+exp(-kappa*Delta/2)))
eta >= 5
```

Missing project evidence: a financial instance with initial spot/variance,
consistent time units and contractual grid; the full positive-semidefinite
correlation construction; finite payoff/Lipschitz and tail constants; numeric
cutoffs, including near-zero exclusion; and an error ledger covering loading,
normalization, quadrature, arithmetic and synthesis. Explicitly reconcile the
source's integrated-CIR interval `2*Delta` with the chosen contractual times.
Passing the scalar grid cannot supply any of these artifacts. A failure at
negative rho is not a proof of impossible pricing or an original research gap.

Moment audit still needed for any proposed instance: establish the particular
payoff/residual moments used by its estimator at every required horizon. Do not
substitute CIR positivity or the displayed screen for a numerical second-moment
bound. The GBM lognormal second-moment calculation in the shortlist is not a
Heston calculation. Likewise, a smaller empirical residual variance is not a
proved bounded encoding range. Account for coherent sampler inverses, controls,
work registers, and repeated calls before forming a resource comparison.

## One path-dependent nested target with a nontrivial exposure sign

Audit construction, not an experiment or a claim copied from a paper: use the
existing two-asset, twelve-fixing GBM basket model, K=100, and a netting set that
receives one arithmetic Asian call and pays fixed cash c=5 at maturity T=1.
Use a single exposure date t=t_6 first. Let B_j be the equally weighted asset
basket, R_m=sum(j<=m) B_j, and Y_m=(S(t_m),R_m). Define

```text
A_T = (R_m + sum(j>m) B_j)/L,       F = (A_T-K)^+ - c
phi_m(Y_m,Z) = exp(-r*(T-t_m))*F
v_m(Y_m) = E[phi_m(Y_m,Z) | Y_m]
CVA_grid = (1-Recovery)*sum_m q_m*exp(-r*t_m)*E[v_m(Y_m)^+]
```

Here q_m are prescribed default probabilities for disjoint intervals,
independent of market paths. This is a discretely approximated unilateral,
uncollateralized exposure target; continuous default timing, wrong-way risk,
funding and closeout changes are outside its definition. The one-date case
isolates one summand. R_m preserves past fixings; replacing it by current spot
changes the contract. Future arithmetic averaging leaves a conditional Asian
valuation. The cash liability allows positive and negative conditional values,
so the positive part cannot generally be moved inside the conditional mean.

This fixes an important negative control: for c=0 the call value is nonnegative,
and `exp(-r*t_m)*E[v_m]=exp(-r*T)*E[(A_T-K)^+]`. With these default assumptions,
the expected-exposure nesting collapses by the tower property even though the
payoff is path-dependent. For c=5, this particular collapse fails; that does
not prove that expensive nested simulation is necessary. A low-dimensional
value-function solver or surrogate may still remove its practical cost.
Keep the one-asset, one-remaining-fixing limit as a conditional lognormal-call
reference, with the accumulated sum incorporated into the effective strike.

[Blanchet et al., v2](https://arxiv.org/pdf/2502.05094v2), Section 3,
Assumptions 1–5 and Theorem 3.2, requires a uniformly K-Lipschitz outer function,
a known uniform conditional second-moment bound V, a known outer variance bound
S, evaluable inner/outer functions, and access to both sampling algorithms.
The stated `O-tilde(K*sqrt(S*V)*log(1/delta)/epsilon)` cost treats these calls
as unit cost. Full reversible sampling access includes garbage registers;
sample-only access does not suffice. Its specialized nested multilevel algorithm
is not obtained merely by wrapping the existing toy's levels in amplitude
estimation. These assumptions have not been established for the target above.

An explicit bound route is available, but remains uninstantiated. On a retained
outer domain `S_i(t_m)<=U`, `R_m<=Rmax`, under the fixed positive-rate,
constant-volatility GBM model, Minkowski's inequality gives

```text
sqrt(E[A_T^2 | Y_m]) <= Rmax/L
  + ((L-m)/L)*U*exp((r+sigma_GBM^2/2)*(T-t_m)) = M_m
E[phi_m^2 | Y_m] <= exp(-2*r*(T-t_m))*(M_m+c)^2 = V_m
```

This uses a bound on each future fixing's second moment and needs no independence
between assets. Without the outer cutoff, a uniform bound fails as spot grows;
finite unconditional lognormal moments do not fix that. For a one-date weight
w_m, the outer Lipschitz constant is w_m and variance is at most `w_m^2*V_m`
on the retained domain. Charge outer discarded-tail and renormalization bias
using unconditional moment/tail bounds, then future-path truncation and numerical
encoding errors separately. If U and Rmax grow with requested precision, V_m
also grows: a bare inverse-epsilon complexity claim would hide that dependence.
Coherent access still requires conditional future Gaussian generation, correlated
paths, running sums, exponentials, both payoff signs, rotations and uncomputation.

## Comparators and bounded exit

The following are comparison obligations, not new work scheduled by this audit:

| Comparator | Required fair treatment |
|---|---|
| Classical antithetic/adaptive nested MLMC | Couple fine inner samples with their two coarse halves; account for inner bias and behavior near v_m=0. Verify moment and coupling rates instead of borrowing the Gaussian toy's rates. Exact contractual-date GBM has no SDE step bias; inner sample levels remain relevant. |
| RQMC with geometric control/conditioning | Allow the same remaining-fixing geometry, PCA or bridge construction and independently fitted control as the quantum arm. Use independent scrambles for uncertainty; measure nested bias separately from scramble variance. |
| Exposure regression or interpolation | Fit v_m on spot and accumulated average; charge training/reference labels, domain coverage, evaluation and held-out approximation error. Since positive part is 1-Lipschitz, expected absolute valuation error bounds the exposure error after weighting. |
| Heston classical solvers | For vanilla limits use semi-analytic pricing; for paths compare an appropriate coupled MLMC scheme and RQMC/control methods. Include time-discretization bias where present and match total accuracy, not path counts. |

Primary comparator evidence: [Haji-Ali and Spence, v1](https://arxiv.org/pdf/2308.07835v1)
develop antithetic nested MLMC with approximate inner/outer simulation; Sections
2–4 make moment, near-kink and coupling assumptions material to the rates.
[Petroni and Sabino](https://arxiv.org/abs/0907.3092) study Asian-basket QMC
and path-generation costs. [Dingec and Hormann](https://doi.org/10.1016/j.insmatheco.2013.03.002)
study geometric controls and conditional Monte Carlo for GBM Asian/basket pricing.
[Feng et al., institutional publication record](https://ir.cwi.nl/pub/24772)
documents exposure-function approximation that avoids nesting for Bermudan
swaptions; it supports the comparator family, not proven accuracy for our Asian
netting set.

Exit: neither alternative currently has a matched dollar-error/resource contract.
Heston lacks a concrete coherent sampler and instantiated theorem constants;
the signed Asian exposure lacks calibrated truncation/moment bounds and evidence
against the strong classical alternatives. These are reasons to retain the
bounded audit status, not to replace or expand the main Week 13 experiment.

Reading depth: focused primary theorem, model, sampler and dependency inspection
for Herman; full displayed five-assumption/theorem inspection for Blanchet;
focused assumptions/coupling inspection for Haji-Ali–Spence; abstract/publisher
records for QMC, conditional-control and surrogate comparators. PDF fallback was
used where arXiv HTML failed. No appendix proof was independently certified and
no published numerical result was reproduced.
