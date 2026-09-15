# Twenty-five harder pricing problems: solution designs and advantage tests

Assessment: 2026-09-15. This is a research shortlist, not 25 newly discovered
open problems or 25 solved quantum applications. The items are distinct payoff,
exercise, exposure or model variants; several share numerical machinery.
All solution designs below are proposals, NOT implementations or measured results.
Pricing adjustments are labelled separately from standalone option prices.

## Executive assessment

Best first application: **arithmetic Asian basket** with a reproducible strong
classical baseline. Best theory-led extension: **restricted multi-asset Heston
with a Lipschitz payoff**. Best larger-scope direction: **genuinely nested exposure
valuation**. Autocallables/TARFs offer existing quantum resource studies to improve,
but simply implementing those studies would not establish novelty.

An important additional paper found in this search is Herman et al. (February
2026): it gives end-to-end asymptotic results for CIR and a restricted multi-asset
Heston construction. Its Heston result is not for arbitrary cross-correlated
variance processes; payoff regularity and truncation/parameter conditions matter.
The selected model definitions and theorem/discussion were inspected, not the
entire proof independently verified. This is a theory lead, not present hardware
advantage or a result produced in our repository. [R1]

Every candidate must pass four questions: Is the classical problem actually hard
after conditioning/variance reduction? Can the quantum distribution/path oracle
be built without enumerating all paths? Does the dollar-error accounting include
all approximations? Does the claimed advantage survive the SAME cost metric?

Below, **first experiment** is an intentionally proposed design, not an executed
benchmark. Priority A means a useful near-term investigation, B means a later
extension, C means substantial prerequisite work or a weak first target. These
are qualitative judgments, not probabilities of discovering an advantage.

## A. Multi-asset terminal and path functionals

### 01. Arithmetic Asian basket call — A

Target: discounted E[(sum_j w_j sum_l S_j(t_l)/L - K)+], initially correlated GBM.
Difficulty: joint asset/time integration and the strike kink.
Design: exact GBM transitions at contractual dates; reversible running weighted
sum; piecewise payoff encoding plus amplitude estimation. Avoid a full path table.
Classical opponent: independently scrambled Sobol RQMC with PCA or Brownian
bridge, antithetics and a geometric-Asian control variate. Conditioning may help.
First experiment: assets 2/4/8, dates 12/52, relative strikes .8/1/1.2, multiple
dollar tolerances. Freeze control-variate training separately. Reject a claimed
benefit if it only beats raw MC or omits coherent path generation. [R2,R3]

### 02. Restricted multi-asset Heston basket call — A (theory-led)

Target: a weighted basket call in the particular asset/variance correlation
structure admitted by R1. Difficulty: volatility integration and tail control.
Design: audit R1's sampling/truncation assumptions, then resource a piecewise
linear Lipschitz basket payoff and its coherent sampler. Do not substitute an
arbitrary Heston Euler circuit and claim the theorem transfers.
Classical opponent: appropriate Heston simulation with RQMC and bias control;
Fourier methods where the payoff/model permits them. First experiment: two
assets in admissible and deliberately inadmissible parameter cells; report the
theorem applicability separately from numerical success. Stop if loading or
truncation constants dominate the theoretical precision benefit. [R1,R4]

### 03. Best-of / maximum multi-asset call — B

Target: E[(max_j S_j(T)-K)+]. Difficulty: piecewise payoff regions and dependence.
Design: reversible comparison tree, maximum register, payoff rotation, uncompute.
Classical opponent: terminal Gaussian RQMC, conditional integration and available
multi-asset Fourier pricing. First experiment: 4/8/16 assets across correlation
regimes, with price and circuit costs versus tolerance. Reject any dimensional
advantage argument based only on d growing: terminal simulation may stay cheap,
and special low-dimensional formulas are controls, not quantum benchmarks. [R4]

### 04. Three-asset spread option with stochastic volatility — B

Target: E[(S1-a*S2-b*S3-K)+]. Difficulty: dependence, cancellation and volatility.
Design: signed reversible arithmetic followed by a positive-part encoder; include
the range of the signed sum in the dollar sensitivity. Classical opponent:
Fourier/COS where characteristic functions exist, plus conditional RQMC.
First experiment: validate a constant-volatility slice against Fourier pricing,
then introduce a specified stochastic-volatility extension. Stop if a low-dimensional
transform method remains cheaper at the same error. The quantum approach is an
extension proposal, not a new spread-pricing algorithm. [R5]

### 05. Discretely monitored barrier basket option — A

Target: basket terminal payoff multiplied by survival at contractual dates.
Design: reversible alive flag and conditional-survival smoothing where it has
a tractable, correctly weighted implementation. Classical opponent: one-step
survival/conditional MC with RQMC, not a naive indicator estimator.
First experiment: barriers near/far from initial basket, 12/52 monitoring dates.
Discrete monitoring is the target; a continuous-barrier claim requires an additional
crossing correction/bias analysis. Stop if smoothing helps the classical algorithm
more than the coherent circuit. Discontinuity prevents casually importing a
Lipschitz-payoff theorem. [R3,R6]

### 06. Parisian basket knock-out — B

Target: knock out after a specified consecutive time below a barrier; this is
different from cumulative occupation time. Design: track excursion duration in
an auxiliary reversible register; bound clock discretization. Classical opponent:
augmented-state dynamic programming/CTMC in low dimension and conditional RQMC
for the basket. First experiment: one-asset Markov-chain reference, then two assets.
Stop if duration-state expansion dominates or a lower-dimensional reduction solves
the case. Existing one-dimensional Parisian solvers are strong controls, not
evidence that a basket implementation has quantum advantage. [R7]

### 07. Floating-strike lookback on a basket — B

Target: E[(basket_T-min_l basket_l)+]. Design: reversible running minimum and
payoff difference with explicit monitoring convention. Classical opponent:
conditional extrema simulation where available and MLMC for a continuous-monitoring
target. First experiment: single-asset tractable slice, then basket paths.
Keep contractual discrete monitoring separate from continuous-monitoring bias.
Stop if storing/uncomputing extrema consumes the query benefit. A new VarQITE
or QAE label alone is not a new financial contribution. [R8]

### 08. Callable range-accrual note with stochastic rates — C

Target: accrued coupons proportional to time a rate/spread stays in a range,
with issuer call dates. Design: occupation counter plus a separately validated
exercise policy; quantum estimation can evaluate that policy but cannot simply
replace its optimization. Classical opponent: low-factor PDE/CTMC and regression
Monte Carlo. First experiment: non-callable reference followed by one call date.
Non-callable linear coupon sums can often be reduced to marginal probabilities:
perform that reduction before calling the problem path-hard. Stop if the purported
quantum problem was avoidable through this decomposition. [R9,R10]

## B. Structured cash-flow contracts

### 09. Globally capped/floored cliquet under stochastic volatility — B

Target: global cap/floor applied to a sum of locally capped returns. Design:
reversible local clipping and cumulative-sum payoff; quantify every approximation
near cap thresholds. Classical opponent: Fourier/convolution methods when increment
structure permits, otherwise conditional RQMC. First experiment: independent-return
slice as a control, then dependent volatility. Stop if only local coupons are present
and the expectation decomposes into cheaply priced marginal claims. [R11]

### 10. Worst-of autocallable — A (resource study)

Target: multi-date automatic redemption based on the worst underlying, with specified
coupon and terminal protection rules. Design: reversible first-hit/alive state,
discounted cash-flow accumulator and uncomputation; compare arithmetic with QSP
where appropriate. Classical opponent: optimized conditional RQMC using identical
term-sheet rules. First experiment: 2/4 assets and 4/12 call dates, validate hand-built
paths before prices. Stop if claimed novelty merely repeats published autocallable
resource estimates or excludes state preparation. [R12,R13]

### 11. Memory-coupon autocallable — B

Target: item 10 plus unpaid coupons carried forward; distinguish coupon trigger
from redemption trigger. Design: coupon-memory counter and cash-flow circuit.
Classical opponent: path-vectorized RQMC with conditional smoothing where valid.
First experiment: paths exercising every combination of missed/recovered coupons
and early redemption; then compare memory on/off with equal market inputs.
Stop if the extra quantum memory/gates create no resource benefit. This is a
distinct contract-state extension, not an independent algorithmic family. [R12]

### 12. Target accrual redemption forward (TARF) — A (resource study)

Target: successive FX settlements until cumulative qualifying gains hit a target;
last-payment and loss-treatment conventions must be fixed. Design: signed payment
arithmetic, gain counter and termination flag. Classical opponent: conditional
RQMC and an independently checked scalar path evaluator. First experiment:
contractual variants with and without final-payment truncation. Stop if precision
near the target dominates the oracle cost or the result only reproduces the existing
TARF quantum resource benchmark. [R12]

### 13. Quanto arithmetic Asian with stochastic FX/volatility — B

Target: a foreign-underlying average paid at a fixed conversion rate. Design:
first specify the domestic pricing measure and quanto drift correctly, then encode
the correlated equity/FX/volatility path. Classical opponent: dimension-reduced
conditional RQMC and approximation controls for simple model slices.
First experiment: constant-volatility domestic-measure identity before stochastic
volatility. Stop if the claimed difficulty came from a wrong numeraire or unnecessary
FX state. This is our proposed model extension; the Asian stochastic-volatility
literature is an entry point, not a theorem covering this quanto design. [R14]

## C. Exercise and control problems

### 14. Bermudan maximum option on several assets — A (later stage)

Target: optimal exercise of a max-call on fixed dates. Design: quantum-assisted
continuation estimation/interpolation only after defining state domain and error
propagation. Classical opponent: cross-fitted LSM plus primal-dual bounds and
modern regression alternatives. First experiment: 2/5 assets and 4/12 dates;
separate policy training, policy evaluation and dual upper-bound simulation.
Stop if a quantum estimator evaluates a poor fixed policy and is compared against
an optimized option value, or if interpolation grows exponentially. [R10,R15,R16]

### 15. Bermudan arithmetic Asian — B

Target: early exercise where accumulated average is an additional state variable.
Design: augmented-state continuation approximation and coherent running sum.
Classical opponent: LSM/low-dimensional PDE where practical, with out-of-sample
policy evaluation and upper/lower bounds. First experiment: one asset and a few
exercise dates before baskets. Stop if training/representation complexity erases
the estimation gain. Pricing a European Asian and adding a max at maturity does
not solve this exercise problem. [R10,R15]

### 16. Multifactor Bermudan swaption — B

Target: exercise into a swap under a specified curve/numeraire model. Design:
first classical factor reduction, then reversible discount/cash-flow computation
and continuation estimation. Classical opponent: factor-reduced regression Monte
Carlo and tree/PDE references in small-factor slices. First experiment: one-factor
reference, then two/three factors with explicit curve conventions. Stop if the
effective dimension is low enough that a classical solver dominates. Quantum
stopping papers motivate an investigation, not a ready swaption oracle. [R15,R17]

### 17. Energy swing option — C

Target: multiple exercise rights subject to local and total volume constraints.
Design: inventory/rights state and constrained backward induction; use quantum
expectation estimation only inside a fully specified control algorithm.
Classical opponent: regression dynamic programming, stochastic control PDEs and
dual bounds where available. First experiment: tiny rights/volume grid with exact
enumeration, then larger inventory. Stop if discretized action-state complexity
dominates. A single-exercise Bermudan implementation is not a swing solution. [R18]

### 18. Callable convertible bond with credit risk — C

Target: equity conversion, issuer call rights and specified recovery/default model.
Design: solve the stopping/game and credit conventions first; possible quantum
subroutine is conditional continuation estimation, not generic terminal QAE.
Classical opponent: coupled complementarity PDEs, CTMC and lattice/regression.
First experiment: no-call/no-default bond-floor limits, then one extra feature at
a time. Stop if default recovery or exercise priority is inconsistent. This is
not a suitable first quantum demonstrator despite its financial complexity. [R19]

## D. Exposure and valuation-adjustment problems

### 19. Netted-portfolio CVA with wrong-way risk — A (larger scope)

Target: discounted positive net exposure at default under correlated market/default
factors. Design: identify whether exposure truly needs inner valuation; if so,
use nested/quantum-multilevel techniques with explicit outer positive-part bias.
Classical opponent: adaptive nested MLMC/RQMC, regression exposure and tractable
change-of-measure reductions. First experiment: small portfolio with analytic
inner values, then replace one component with a genuinely path-dependent claim.
Stop if a surrogate or analytic conditioning removes the expensive nesting.
CABIQAE is close prior art, so generic noise-aware CVA is not novel. [R20,R21,R22]

### 20. Collateralized CVA with margin-period exposure — B

Target: exposure after collateral calls, thresholds and a specified margin period
of risk. Design: collateral state and delayed exposure calculation; budget time-grid,
regression and nested estimation errors separately. Classical opponent: nested
MLMC, exposure regression and multi-layer valuation solvers. First experiment:
zero-margin-period and fully collateralized limits before nonzero delays.
Stop if collateral assumptions, not computation, explain the price difference.
This is a valuation adjustment, not a standalone option. [R21,R23]

### 21. CVA of an early-exercisable portfolio — B

Target: credit adjustment with future exercise decisions. Design: train/freeze
exercise policy independently, evaluate exposures, then account for policy bias
before attempting quantum acceleration of the nested layer. Classical opponent:
LSM plus exposure regression/adaptive nested estimation. First experiment: a single
Bermudan with small-state reference. Stop if treating the learned policy as exact
creates an unbudgeted bias. Shared path samples for exposure/policy fitting require
careful sample splitting; the present Bernoulli certifier does not solve that. [R15,R21]

### 22. Funding/collateral XVA with nonlinear feedback — C

Target: a specified nonlinear valuation/BSDE problem, not generally a single
discounted expectation. Design: stable fixed-point/BSDE iteration, with any quantum
estimation errors propagated through it. Classical opponent: PDEs at low dimension,
regression BSDE and validated deep-BSDE methods at higher dimension.
First experiment: symmetric-funding linear limit, then one nonlinear term.
Stop if a QAE estimate of clean value is being mislabeled as full XVA, or if solver
training/convergence dominates. Deep BSDE point estimates alone are not rigorous
reference truths. [R23,R24]

## E. Difficult dynamics and monitoring

### 23. Arithmetic Asian under rough Bergomi — B

Target: path-average payoff with non-Markovian volatility. Design: finite-factor
Markovian approximation or coherent Gaussian construction, with a certified model
approximation allowance before pricing error. Classical opponent: variance-reduced
RQMC, sparse quadrature where applicable and hybrid/Markovian approximations.
First experiment: decreasing factor/grid error and a strong RQMC baseline before
compiling the oracle. Stop if loading the covariance structure dominates, or if
the approximation bias is larger than the purported quantum gain. [R25,R26]

### 24. VIX option under rough forward variance — B

Target: an option on the square root of a future variance integral. Design:
derive the conditional variance representation before choosing whether nesting
actually remains; then encode the integral and nonlinear payoff. Classical
opponent: the established MLMC/trapezoidal approach and Gaussian RQMC.
First experiment: reference the same integral discretization and separately
refine it. Stop if a naive nested estimator is used when the model permits direct
sampling of the relevant Gaussian functional. [R27]

### 25. Jump-diffusion basket barrier — B

Target: monitored survival plus terminal basket payoff with correlated jumps.
Design: truncated jump-count/register construction with explicit tail budget;
discrete monitoring first, then any continuous-crossing treatment. Classical
opponent: jump-adapted conditional MC/RQMC and MLMC where appropriate.
First experiment: zero-jump-intensity reference, then rare/frequent jump regimes.
Stop if jump-count truncation or barrier-crossing bias is not bounded. A theorem
for smooth diffusion payoffs cannot simply be inherited by this discontinuous
jump problem. [R6,R8]

## Three concrete solution-development packages

### Package A: smoothed Asian/barrier basket integration (01 and 05)

Build a scalar path evaluator with branch-boundary tests; a vectorized classical
engine; independent Sobol scrambles with control-variate coefficients fitted on
separate training samples; and conditional smoothing where mathematically valid.
Use exact GBM transitions at contractual dates. RQMC uncertainty is across
independent scrambles, not a binomial CI over correlated Sobol points. Student-t
error bars over a few scrambles are approximate, not exact dollar certificates.

Quantum proposal: generate Gaussian coordinates coherently, accumulate only
required path statistics, encode the smoothed payoff, and uncompute. Compare
arithmetic, piecewise/QSP and finite-table small controls. A proposed contribution
is an error/resource analysis showing WHEN smoothing reduces total quantum cost
after applying the SAME smoothing to the classical comparator. This contribution
has not been established or implemented.

### Package B: theorem-to-resources Heston study (02)

Create an explicit applicability checklist from the primary theorem; implement a
classical sampler reference; audit truncation and precision; resource the required
coherent sampler and payoff separately. Vary precision while keeping the financial
model fixed. Distinguish a theoretical gate-complexity benefit from an estimated
fault-tolerant crossover and from measured runtime. A useful new result would need
improved constants/encoding or a rigorously supported new regime, not just citing
an existing asymptotic theorem. No such new result is claimed here.

### Package C: genuinely nested exposure (19)

Write the target explicitly as E[w(Y)*max(E[X|Y],0)] with model-appropriate weights,
or the correct extension if weights and exposure need additional joint state.
Use analytic-inner controls to measure nested estimator bias. Compare adaptive
classical nested MLMC and nested RQMC before attempting quantum-inside-quantum
estimation. Reuse no classical inner answer as an uncharged quantum oracle.
The open project question is whether a faithful financial instance and efficient
coherent access survive all error/resource requirements, not whether standard
QAE reduces the ideal query exponent. [R20,R21,R28]

## Common error/resource contract

### A concrete conditional solution for a restricted Asian-basket subproblem

There is a useful analytical reduction to implement before claiming this basket
is difficult. Under positive equicorrelation rho, condition on the common Brownian
bridge and all idiosyncratic paths, leaving Z=W_common(T)/sqrt(T). With positive
weights, the conditional arithmetic basket average has the form

    A(Z) = sum_i c_i exp(b_i Z),  c_i>0, b_i>0,
    b_(j,l) = sigma_j sqrt(rho) t_l / sqrt(T).

For K>0 there is a unique root z_star of A(z_star)=K. Completing the square in
the Gaussian integral gives the EXACT conditional payoff identity

    E[(A(Z)-K)+ | remaining coordinates]
      = sum_i c_i exp(b_i^2/2) Phi(b_i-z_star) - K Phi(-z_star).

Discount this expression using the specified pricing model. A scalar bracketed
root solve replaces the strike discontinuity in that integration coordinate.
Conditioning reduces ordinary MC variance, but does not by itself prove an RQMC
rate improvement or quantum advantage. Mixed-sign weights/loadings can destroy
monotonicity and require a different construction. This is an established
conditional-Monte-Carlo idea specialized to our proposed problem, not a new
identity claimed for publication. [R3]

Deterministic numerical check performed this turn: c=(20,30,50) or (5,15,80),
b=(.1,.2,.3) or (.1,.4,.8), K=80/100/120, giving 12 cases. Brent root tolerance
1e-13; independent direct payoff quadrature on [-12,12], split at the root,
epsabs=1e-10 and epsrel=1e-11. Maximum identity-versus-quadrature difference:
1.0658141036401503e-14. Maximum quadrature error estimate: 3.4650804068845687e-10;
maximum upper-tail bound sum_i c_i exp(b_i^2/2) Phi(b_i-12):
2.2493822249685826e-27. The lower tail contributes zero for these roots.
These are component checks, not full option prices, a rigorously rounded proof,
or measured performance of the proposed 25 applications.

The quantum design question is nontrivial: a coherent root solve and normal-CDF
evaluation might cost more than the unsmoothed payoff. Use the same reduction
classically, then charge these operations on the quantum side. Reduced classical
variance alone does not reduce the bounded-amplitude scale S in our certifier.

### A precise theorem-applicability question

R1's displayed Heston truncation conditions include
2*kappa*sigma*rho-rho^2*sigma^2 >= 0. For kappa,sigma>0 and rho<0, this particular
sufficient condition fails algebraically. Investigating a different tail bound
is a concrete direction; failure of that lemma is NOT impossibility of quantum
pricing or proof that no other literature handles the regime. Additional timestep
and discretization conditions must also be checked before applying the theorem.

### Shared accounting requirements

For any chosen package, split dollar tolerance among model approximation, tail
truncation, time/grid discretization, payoff/synthesis, exercise/regression and
statistical error. Include only applicable terms, but never silently set them to
zero. Hold market parameters fixed while comparing solvers. Charge preprocessing,
loading, payoff evaluation, uncomputation, calibration, measurements and fault
tolerance when making an end-to-end claim. State what was excluded.

The current encoding-aware rule can rank encodings only after a trustworthy
bound B and dollar sensitivity S exist. For nested/control problems those require
new analysis. It is NOT a drop-in certificate for all 25 proposed applications.
The continuation in this turn remains a controlled European regression experiment
for calibration allocation; it must not be presented as testing these 25 problems.

## Source ledger and reading depth

Primary sources only support the scientific statements; suggested extensions and
priority rankings are our inferences. Unless specified, reading was abstract or
selected publisher text, not a full-paper proof audit. Search-engine crawl dates
were not treated as publication dates. Older foundations are not called new.

- R1: [Herman et al., Quantum Speedups for Derivative Pricing Beyond Black-Scholes (2026)](https://arxiv.org/html/2602.03725v1). Focused model definitions, contributions and Heston theorem/discussion; not complete proof verification.
- R2: [L'Ecuyer, Randomized Quasi-Monte Carlo tutorial](https://www.iro.umontreal.ca/~lecuyer/myftp/papers/mcqmc16tutorial-paper.pdf). Selected Asian/control-variate discussion.
- R3: [Conditional QMC and dimension reduction for discontinuous pricing/hedging functions (2018)](https://www.sciencedirect.com/science/article/am/pii/S0377042718302747). Selected smoothing/methods discussion.
- R4: [QMC with domain transformation for multi-asset Fourier pricing](https://arxiv.org/abs/2403.02832). Abstract and selected numerical-results excerpt.
- R5: [Pellegrino and Sabino, multi-asset spread Fourier/COS pricing](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2410176). Primary author abstract.
- R6: [Glasserman and Staum, Conditioning on One-Step Survival (2001)](https://pubsonline.informs.org/doi/10.1287/opre.49.6.923.10018). Publisher abstract.
- R7: [A General Approach for Parisian Stopping Times under Markov Processes](https://arxiv.org/abs/2107.06605), and [American Parisian options under time-inhomogeneous Markov models (2025)](https://arxiv.org/abs/2503.11053). Abstracts; one-dimensional scope.
- R8: [Giles's author-maintained MLMC research collection](https://people.maths.ox.ac.uk/gilesm/mlmc.html). Selected descriptions of basket, extrema and jump-diffusion work; not full-paper readings.
- R9: [Algorithms for Option Prices in Markov Chain Models](https://www.rocq.inria.fr/mathfi/pdf-publications/livre.pdf). Search excerpt only; general computational background, not a reviewed solution for item 08.
- R10: [Miyamoto, Bermudan pricing with QAE and Chebyshev interpolation](https://arxiv.org/abs/2108.09014). Abstract and selected publisher LSM background.
- R11: [Cliquet option pricing with Meixner processes](https://www.vmsta.org/journal/VMSTA/article/107/text). Selected publisher excerpt; not the proposed stochastic-volatility extension.
- R12: [Chakrabarti et al., A Threshold for Quantum Advantage in Derivative Pricing](https://arxiv.org/abs/2012.03819). Abstract; autocallable/TARF resource study.
- R13: [Stamatopoulos and Zeng, Derivative Pricing using QSP](https://arxiv.org/abs/2307.14310). Previously screened source; no new full reading this turn.
- R14: [Short-maturity Asian options in local-stochastic volatility models](https://arxiv.org/abs/2409.08377). Abstract; no quanto theorem inferred.
- R15: [Doriguello et al., quantum stochastic optimal stopping](https://arxiv.org/abs/2111.15332). Abstract, revised 2023; access/approximation assumptions matter.
- R16: [Andersen and Broadie, Primal-Dual Simulation for Multidimensional American Options](https://pubsonline.informs.org/doi/pdf/10.1287/mnsc.1040.0258). Publisher abstract.
- R17: [Andersen and Andreasen, Factor Dependence of Bermudan Swaption Prices](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=209988). Primary abstract.
- R18: [Optimal Exercise of Swing Contracts in Energy Markets](https://arxiv.org/abs/1307.1320). Abstract.
- R19: [A Unifying Approach for the Pricing of Debt Securities](https://arxiv.org/abs/2403.06303), and [Valuation of Convertible Bonds with Credit Risk](https://ecommons.cornell.edu/entities/publication/03d7fefb-b471-4558-bedb-64d0d7ae15d6). Abstracts.
- R20: [Blanchet et al., Quantum speedup of non-linear Monte Carlo problems](https://arxiv.org/abs/2502.05094). Abstract; nested conditional expectations.
- R21: [Giles and Haji-Ali, Multilevel nested simulation for efficient risk estimation](https://arxiv.org/abs/1802.05016), and [Nested MLMC with biased and antithetic sampling](https://arxiv.org/abs/2308.07835). Abstracts; applicability must be checked per target functional.
- R22: [Borras Espert et al., noise-aware quantum CVA (July 2026)](https://arxiv.org/abs/2607.12990). Abstract this turn; earlier focused methods reading is recorded separately.
- R23: [Multi-Layer Deep xVA (2025)](https://arxiv.org/abs/2502.14766). Abstract; layered valuation and margin-period treatment.
- R24: [Arbitrage-Free XVA](https://arxiv.org/abs/1608.02690). Abstract; nonlinear valuation distinction.
- R25: [Adaptive sparse grids and QMC under rough Bergomi](https://arxiv.org/abs/1812.08533). Abstract.
- R26: [Markovian approximation of rough Bergomi](https://arxiv.org/abs/2007.02113), and [Turbocharging rough-Bergomi Monte Carlo](https://arxiv.org/abs/1708.02563). Abstracts.
- R27: [MLMC for VIX options in rough Bergomi](https://arxiv.org/abs/2105.05356). Abstract and author-code link discovery; code not executed.
- R28: [Efficient risk estimation via nested multilevel QMC](https://arxiv.org/abs/2011.11898). Abstract.

Do not confuse older "quantum finance" field-theoretic market models appearing
in search results with algorithms executed on quantum computing hardware. Those
results were not used as evidence of a computational speedup here.
