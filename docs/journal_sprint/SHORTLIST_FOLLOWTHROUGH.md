# Follow-through: harder pricing, theorem applicability and encoding design

Date: 2026-09-15. This continues the [25-problem assessment](HARD_PRICING_25.md)
and [allocation study](ALLOCATION_RESULTS.md). Implemented work is distinguished
from analytical design and untested future work. No quantum advantage, novel
algorithm, market CVA result or full proof audit is claimed.

## 1. Decisions after investigation

- Keep Asian baskets as an honest, strong classical benchmark. The implemented
  cases are already priced accurately by classical methods; dimension alone has
  not created a compelling advantage target.
- Conditional integration is useful per sample, but its root/CDF work costs
  time. Quantum encoding must charge these operations too.
- Heston remains a theorem-to-resources investigation, not an interchangeable
  replacement model. Passing a few scalar conditions is not implementing the
  coherent sampler or establishing all theorem assumptions.
- Nested exposure remains interesting only when nesting cannot be removed
  analytically or by a strong classical approach. A controlled counterexample
  below demonstrates why a naive nested baseline can mislead.
- Do not promote the previous equal-calibration pilot allocator: it tied the
  fixed baseline. A more informative next design considers unequal calibration
  allocations and tolerance delivery, with valid fresh-sample inference.

## 2. Implemented Asian-basket benchmark

Code: `asian_basket.py`, `run_shortlist.py`; frozen
[protocol](PROTOCOL_SHORTLIST_V1.md). Archive:
`results/journal_sprint/shortlist_v1`. No historical results were changed.

The twelve contracts have 2/4 assets, 12/52 contractual monitoring dates and
strikes 90/100/110. Equal weights, spot 100, volatility .3, rate .03, maturity 1
and positive equicorrelation .5 are fixed. GBM is sampled exactly at those dates;
there is no SDE time-step bias for this discrete-monitoring target. This does
not certify model realism or continuous-monitoring prices.

For raw paths, construct the full covariance of log-price noise and use its
principal components in decreasing variance order. For conditional paths,
remove the covariance of the common terminal Brownian factor, sample the
remaining Gaussian vector and integrate that factor analytically. Both covariance
reconstructions are unit-tested. The conditional residual uses d*L normals;
the removed scalar factor is integrated, not independently sampled.

Four estimators were run at 1024 and 4096 payoff evaluations with eight independent
repetitions each, giving 768 estimate rows:

1. Antithetic IID Monte Carlo with geometric-basket-Asian control variate.
2. Scrambled Sobol RQMC without a control variate.
3. Scrambled Sobol RQMC with the geometric control.
4. Conditional scrambled Sobol with a conditional geometric control.

Raw and conditional control coefficients are fitted on separate 1024-observation
IID training sets per contract, independent of benchmark and reference streams.
The raw coefficient is shared by methods 1 and 3. Each method's standalone cost
must include its own needed training; sharing it in this experiment does not
make that cost zero in deployment. Coefficients stay fixed during evaluation.

The geometric control mean is analytic. If G is the geometric mean across all
asset/date observations, log G is normal with mean equal to the average log-price
mean and variance equal to the average entry of the log-price covariance matrix.
Its discounted call expectation is therefore a lognormal-call formula. The
conditional control uses the corresponding one-factor conditional formula.
One-asset/one-date limits and independent quadrature checks passed.

The conditional arithmetic payoff uses the scalar-root identity in the earlier
report, now implemented with an analytic bracket and 44 bisection steps. The
largest observed relative root residual over benchmark rows was about 2.052e-13.
This is numerical checking, not a directed-rounding error certificate.

References use 16 additional, independent RQMC-control scrambles of 8192 points
per contract: 192 reference estimates, 131072 reference evaluations per contract.
They are numerical references, NOT exact prices. Reference standard errors range
from .0001192 to .0002224 dollars. The errors below are empirical RMSE relative
to those reference means, not certified absolute error.

### Results at 4096 evaluations

| Assets | Dates | Strike | Numerical reference | MC + control RMSE | RQMC + control RMSE | Conditional + control RMSE |
|---|---|---|---:|---:|---:|---:|
| 2 | 12 | 90 | 13.163951 | .012590 | .000901 | .000521 |
| 2 | 12 | 100 | 7.057067 | .010048 | .001398 | .000280 |
| 2 | 12 | 110 | 3.306023 | .008600 | .001567 | .000372 |
| 2 | 52 | 90 | 12.886459 | .016935 | .001209 | .000566 |
| 2 | 52 | 100 | 6.724704 | .006666 | .001057 | .000176 |
| 2 | 52 | 110 | 3.022523 | .007757 | .001186 | .000410 |
| 4 | 12 | 90 | 12.794958 | .014296 | .000735 | .000407 |
| 4 | 12 | 100 | 6.518632 | .014501 | .001663 | .000376 |
| 4 | 12 | 110 | 2.804863 | .009001 | .001155 | .000410 |
| 4 | 52 | 90 | 12.544371 | .010608 | .001043 | .000513 |
| 4 | 52 | 100 | 6.210537 | .008363 | .001598 | .000196 |
| 4 | 52 | 110 | 2.550867 | .006012 | .001054 | .000159 |

All methods and both evaluation counts, including raw RQMC, are saved in the
archive. Conditional RMSE is lower than raw-control RQMC in these twelve cells,
but several values are near the reference uncertainty. Do not interpret the
ratio as a precisely measured asymptotic speedup or universal ranking.

Conditional evaluation-stage timings were roughly 4.48-8.69 times those of
RQMC-control at 4096 points. These are indicative local timings: they exclude
separately recorded joint setup/training/reference work, methods ran in fixed
order, and regression tests ran concurrently. Single-thread numerical libraries
were used, but this is NOT an isolated end-to-end timing benchmark. A runtime
crossover claim needs repeated, interleaved isolated timings at matched accuracy.

RQMC uncertainty uses independent scrambles. Within-net observations are not
IID Bernoulli trials. The recorded Student-t intervals over eight repetitions
are approximate, not exact finite-sample coverage. This limitation follows the
distinction discussed in the primary RQMC interval literature; no binomial
pricing certificate is applied to Sobol points. [1]

## 3. Heston: what the theorem actually requires

The focused reading covers the primitive CIR sampler, the restricted Heston
model, scalar truncation/discretization assumptions and the theorem discussion
in Herman et al. [2]. It does not independently verify every appendix proof.

The numerical screen checks the displayed conditions:

    Delta >= 1
    exp(-kappa*Delta/2) + exp(-kappa*Delta) < 1
    0 <= 2*kappa*sigma*rho - rho^2*sigma^2 < kappa^2
    (1+exp(-2*kappa*Delta))/4
      + (rho*sigma/kappa)*(1-exp(-2*kappa*Delta))/4
      < 1/[2*(1+exp(-kappa*Delta/2))]
    eta = 4*kappa*theta/sigma^2 >= 5.

Here sigma is volatility-of-volatility, not the GBM volatility above. Of 72
predeclared scalar parameter combinations, **14 pass these displayed tests**.
The field `full_theorem_applicability` remains `not_established` for every row.
No correlation-matrix construction, coherent integrated-CIR sampler or finite
logical-gate resource estimate has been implemented.

Do not generalize this to arbitrary variance cross-correlations or discontinuous
barrier payoffs. The paper's stronger distribution-regularity condition is not
merely the usual positivity condition. Also, changing a time unit without
transforming ALL SDE parameters and contractual times consistently is not a way
to force a monthly model through the scalar test.

Correction of emphasis from the previous shortlist: negative rho fails the
displayed middle inequality, but the authors explicitly discuss nonnegative rho
as the harder moment regime. Thus this failure alone does NOT identify a new
unsolved negative-correlation problem. First inspect the complete proof and other
tail bounds before claiming an extension. A source restriction is not evidence
of physical impossibility or a guaranteed novelty gap. [2]

### Concrete resource-audit work still needed

Freeze one admissible financial instance and its full correlation structure;
implement and validate the required conditional sampler; bound truncation,
quadrature and arithmetic errors; compile controlled sampling/payoff/uncompute;
then compare actual resources against a strong classical solver. A Big-O theorem
does not supply finite constants or a measured hardware crossover.

## 4. Nested expectations: stronger assumptions and a negative control

The quantum nested paper's main assumptions include a uniformly Lipschitz outer
map, known moment/variance bounds and access to the actual sampling procedures
that can be made reversible. A sample-only market API is not that access. Its
algorithm changes the multilevel construction: putting generic QAE around an
unchanged classical nesting scheme does not automatically preserve the improved
precision scaling. [3]

For exposure E[w(Y)*max(E[X|Y],0)], bounded weights give a Lipschitz outer map,
but a uniform conditional second-moment bound can fail on an unbounded market
state space. Ordinary finite unconditional variance is not the same assumption.
Options require justified truncation or an appropriate residual reformulation,
with its bias charged. Classical antithetic nested MLMC is an essential comparator;
its approximation/coupling assumptions also need verification. [4]

### Implemented negative control

Let Y~N(.2,1), X=Y+2Z with independent Z~N(0,1). Then E[X|Y]=Y and the target
is E[max(Y,0)] = **.5068946358632764**. Nesting is completely unnecessary.
If the inner expectation is nevertheless estimated with m IID samples, the
outer estimator's expectation is the positive-part mean of N(.2,1+4/m):

| Inner samples m | Exact bias of naive nested expectation |
|---|---:|
| 1 | .4887333 |
| 4 | .1629275 |
| 16 | .0462539 |
| 64 | .0120421 |
| 256 | .00304365 |

The archive contains 40 independent nested estimates (eight at each m, 2048
outer draws), their analytic-inner counterparts, and eight antithetic level
diagnostics. Fine/coarse corrections use genuinely shared inner samples; the
finite-sample telescoping identity and Jensen sign are tested. Level-correction
variance decreases from about .112835 at level 1 to .000216335 at level 8.
This is NOT a full optimally allocated MLMC solver or quantum implementation.

In its raw form this toy also lacks a uniform bound on E[X^2|Y=y]=y^2+4. It can
be rewritten with inner residual 2Z and outer map max(y+u,0), but that merely
exposes its analytically trivial inner mean. This diagnostic prevents us from
claiming a speedup over an unnecessarily nested benchmark.

The next genuine case should use a path-dependent inner claim that cannot be
eliminated this way. Preserve an analytic special case, then compare adaptive
classical nested MLMC/RQMC and fitted exposure surrogates before building quantum
circuits. A portfolio-level nesting claim must charge policy training, regression,
and approximation error rather than treating the fitted price as exact.

## 5. Encoding and state preparation: a concrete bound calculation

The current basket payoffs are unbounded. A bounded amplitude encoding therefore
needs a justified truncation and normalization. We calculated a conservative
screen without pretending to have synthesized the quantum circuit.

Write the arithmetic average A=M^-1 sum_i exp(mu_i+(FZ)_i), M=d*L. Its second
moment is computable from the Gaussian covariance C:

    E[A^2] = M^-2 sum_ij exp(mu_i+mu_j+(C_ii+C_jj)/2+C_ij).

Let D be the discount and H=D*sqrt(E[A^2]). Choose delta=(.1/(2H))^2 and
z=Phi^-1(1-delta/(2M)). The union bound gives Pr(any |Z_i|>z)<=delta. For the
nonnegative call payoff, Cauchy-Schwarz bounds discarded tail expectation.
Including normalization of the retained distribution, a conservative price bias
allowance is H*(sqrt(delta)+delta/(1-delta)). It is about **.05003 dollars** here.

On the retained cube a raw scale upper bound is

    S_raw = D*max(M^-1 sum_i exp(mu_i+z*||F_i||_1)-K,0).

For the conditional payoff, use the residual factor F_res and integrated loading
b. Jensen's inequality permits the same second-moment tail screen, and a valid
(loose) scale bound is D*M^-1 sum_i exp(mu_i+z*||F_res,i||_1+b_i^2/2).

Illustrative deterministic bounds at K=100:

| Assets | Dates | Cube z | Raw scale upper bound | Conditional scale upper bound |
|---|---|---:|---:|---:|
| 2 | 12 | 5.724 | 2980.74 | 2110.97 |
| 2 | 52 | 5.967 | 9285.20 | 6350.83 |
| 4 | 12 | 5.839 | 7547.77 | 4711.89 |
| 4 | 52 | 6.078 | 31606.07 | 18888.08 |

These are conservative sufficient upper bounds, not unavoidable sensitivities,
lower bounds, measured circuit costs or evidence of quantum impossibility.
They show why simply placing this integrand inside the existing encoding-aware
rule is not ready. Numerical quadrature/state-preparation/synthesis errors are
still missing; the .05003 tail allowance is NOT the full B required by the rule.

Potential work: tighter payoff-aware truncation, variance-aware mean estimation,
residual encoding with rigorous range bounds, or a structured sampler. Each must
be compared against classical conditioning/control variates. In particular,
arbitrary finite-table preparation is not a scalable answer. Published limitations
of Grover-Rudolph-based Monte Carlo preparation are another reason to account for
the entire loading procedure, not to declare all state preparation impossible. [5]

## 6. Allocation: a sharper design question, not another claimed win

The last pilot chose equal counts for the two calibration states and minimized
predicted radius at a fixed full budget. That can waste budget when the tolerance
has already been met or when one readout parameter barely influences the price.

For a=(q-f)/(1-f-g), c=1-f-g, the derivatives are 1/c, -(1-a)/c and a/c with
respect to q,f,g. A delta-method planning variance, excluding deterministic bias,
is therefore

    S^2/c^2 * [q(1-q)/n + (1-a)^2 f(1-f)/m0 + a^2 g(1-g)/m1].

Under a fixed equal-shot-cost total, minimizing this APPROXIMATION assigns
(n,m0,m1) proportional to the square roots of the three variance coefficients.
For illustrative f=.02,g=.07,a=.01 the proportions are approximately
(.54355,.44820,.00825), dramatically unlike equal calibration counts. At a=.5
they become (.71652,.10044,.18305). These calculations use assumed parameters;
they are not observed optimal allocations or finite-sample certificates.

A rigorous experiment would use a paid pilot/design model to choose unequal
m0,m1 and a pricing cap before fresh calibration/validation, then keep terminal
CP inference or an explicitly valid confidence sequence. Forecast delivery
probability and expected cost, not merely minimum width. CP endpoint behavior,
minimum calibration counts, transfer floors and pilot cost can invalidate the
normal-approximation efficiency prediction; they do not disappear in a real
planner. Optimizing a sum of conservative interval halfwidths gives a different
allocation law, so the criterion must be chosen explicitly.

No asymmetric allocation experiment was run this turn. The existing fixed_cp
baseline stays the reference; the tied pilot result is not overwritten or relabelled.

## 7. Verification and reproducibility

15 focused tests passed before acquisition, including covariance reconstruction,
geometric-call limits, conditional integration versus independent quadrature,
invalid inputs, theorem-screen scope, exact nested bias and telescoping identities.
Ruff passed all four new Python/test files.

Deterministic replay verified 76 archived files, all 768 main estimates, 192
reference estimates, 72 scalar Heston screens, 40 nested estimates and eight
level diagnostics. Timings are deliberately excluded from numeric replay; all
other numeric fields are checked at 1e-10 absolute/relative tolerance. Frozen
source and archive hashes are also checked. This is automated verification, not
independent human peer review. Final full regression passed all 504 tests, zero
failures/errors/skips, with 11 upstream warnings in 270.96 seconds
(`tests_shortlist_v1.xml`). The [project log](PROJECT_LOG.md) records the handoff.

Reproduce into a NEW directory, with numerical-library thread settings recorded:

```powershell
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
venv\Scripts\python.exe -m research.journal_sprint.run_shortlist --output results/journal_sprint/shortlist_NEW
venv\Scripts\python.exe -m research.journal_sprint.run_shortlist --output results/journal_sprint/shortlist_NEW --verify
```

## Sources and reading depth

1. [L'Ecuyer et al., Confidence Intervals for RQMC Estimators](https://digitalcommons.njit.edu/fac_pubs/2381/). Primary institutional abstract; not a proof audit. Geometric control/conditional integration also follow the previously cited baseline literature.
2. [Herman et al., Beyond Black-Scholes, v1](https://arxiv.org/html/2602.03725v1). Focused sections 6.1.1, 6.2.2-6.2.3, model definitions and adjacent discussion; not a complete appendix reading or verified new theorem.
3. [Blanchet et al., nonlinear Monte Carlo, v2 PDF](https://arxiv.org/pdf/2502.05094). Focused introduction, section 3 assumptions and algorithm motivation. HTML retrieval failed; PDF fallback succeeded. Not a full-paper reading.
4. [Haji-Ali and Spence, nested MLMC, v1 PDF](https://arxiv.org/pdf/2308.07835). Focused introduction and antithetic-coupling discussion. Requested v2 HTML was unavailable; the retrieved PDF identifies itself as v1, not v2.
5. [Herbert, Grover-Rudolph state preparation limitations](https://arxiv.org/abs/2101.02240). Abstract screen; the limitation is scoped to the analyzed construction, not every possible loader.

The new implementation uses established classical mathematics. None of these
papers' quantum algorithms has been implemented by merely running our classical
benchmark. No manuscript superiority claim or publication decision follows.
