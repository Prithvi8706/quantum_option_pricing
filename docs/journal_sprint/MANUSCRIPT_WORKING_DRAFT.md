# Delivered-precision intervals for quantum option-pricing experiments

Historical week-1/2 draft. Superseded for current scientific claims by the
[week-9 synchronized manuscript](MANUSCRIPT_RELIABILITY_DRAFT.md).
The original text below is retained as history, not current execution status.

Working methods manuscript. Discovery results only; not submission-ready. This is the replacement scientific draft, not a silent edit of the preserved historical DOCX/LaTeX files. Author names and contribution statements are intentionally omitted until real contributions and approvals are recorded.

This draft's results/limitations text reflects the week-1/2 writing milestone.
Later evidence is documented in [week 3](WEEK_3_BASELINES_AND_REVIEW.md) and
[week 4](WEEK_4_TRANSFER_RESULTS.md), [week 5](WEEK_5_FIXED_RESULTS.md), and
[week 6](WEEK_6_RESULTS.md), [week 7](WEEK_7_RESULTS.md) and
[week 8](WEEK_8_RESULTS.md); their incorporation into the full manuscript
remains a writing-stage task. Do not treat the older “next tests” list as the
current execution status or submit this unsynchronized draft.

## Abstract

Quantum amplitude-estimation accuracy does not directly specify the accuracy of a continuous financial derivative value. Support truncation, finite-grid representation and payoff encoding can consume a substantial part of a requested dollar tolerance before statistical estimation begins. We study a conditional interval procedure that propagates these deterministic bounds through an affine price transformation and retains all amplitude branches consistent with simultaneous binomial intervals. A six-contract discovery experiment examines 72 representation configurations. A cancellation-aware grid bound increases configurations with a positive one-dollar statistical allowance from 4 to 14. A subsequent model-based finite-shot experiment records 43,200 attempts, including explicit refusals. At the largest tested budget, a fixed ideal multidepth procedure delivers one-dollar intervals in 613 of 1,200 attempts, compared with 400 for equal-A-query direct quantum sampling. These findings establish limited feasibility, not practical quantum advantage; calibrated noise, stronger comparators and held-out transfer remain necessary.

## 1. Problem and scope

The target is a discounted European call value under a specified lognormal model. The independent Black–Scholes value serves as validation truth, not a selector input or a realistic classical algorithm to beat with quantum simulation. The study asks whether the output interval accounts for the gap between the mathematical price and the encoded circuit target.

Earlier exploratory data in this repository measured deviations from a precomputed quantum estimate, not isolated grid bias or necessarily Black–Scholes error. Those deviations do not establish a universal discretization floor and are not used as such here. The manuscript makes no protected irreducible-floor claim. Historical dimension-decay slopes with unresolved raw provenance are excluded.

## 2. Related work and candidate distinction

Adaptive Bayesian amplitude estimation, Bayesian transfer between IQAE stages, noisy maximum-likelihood estimation, stopping-bias investigation and geometric depth schedules provide established methods and important comparators. Quantum quasi-Monte Carlo also separates finite representation and estimation error. The detailed [literature supplement](LITERATURE_SUPPLEMENT.md) supplies versioned references and identifies overlap; its cited sources form the initial bibliography for this draft.

The candidate distinction is application-level delivered precision: selecting or rejecting a representation using deterministic bounds and measuring useful dollar intervals under explicitly counted resources. The current procedure combines standard mathematical tools. No claim of a new generic amplitude estimator, first error decomposition, or globally optimal controller is made.

## 3. Target ladder and deterministic budget

Let P be the continuous discounted call value. Let P_sup be the support-conditioned value, P_grid the implemented pointwise-density-weighted grid value, and P_enc the ideal encoded price. Then

`P_enc-P = (P_sup-P) + (P_grid-P_sup) + (P_enc-P_grid)`.

The signed identity is checked independently. Bounds on the absolute components yield `|P_enc-P| <= B_sup+B_grid+B_enc = B`. Observed errors against a known answer are diagnostics, not deployable bounds.

For support [L,U], scale c and objective probability a, the implemented affine map is

`P_enc = b + L_P*a`, where `L_P = exp(-r*T)*(U-K)*2/(pi*c)`.

The support and encoding bounds are derived in [PRICING_BOUND_DERIVATION.md](PRICING_BOUND_DERIVATION.md). The tighter grid construction in [TIGHTER_GRID_DERIVATION.md](TIGHTER_GRID_DERIVATION.md) integrates a constant-density payoff difference within each nearest-grid cell and bounds the remaining density variation by derivative suprema. It retains the correction between integrated cell masses and implemented pointwise weights. This does not change the underlying grid semantics.

## 4. Conditional statistical procedure

For predetermined depths k_j and sample sizes N_j, observations satisfy independent binomial laws with response

`q_j(a,eta)=1/2+(1-eta)^(2*k_j+1)*(sin²((2*k_j+1)*arcsin(sqrt(a)))-1/2)`.

This is the declared response model, not a universal device-noise law. The true eta is assumed to belong to a supplied envelope. At each depth, construct a Clopper–Pearson interval at failure level alpha/J. Invert all sinusoidal branches and retain every amplitude consistent with some admissible response at each depth. Allowing the nuisance value to vary independently by depth is a conservative outer relaxation of a common eta.

If the feasible amplitude hull is [a_l,a_u], report `[b+L_P*a_l-B, b+L_P*a_u+B]`. If the set is empty, report incompatibility without a price interval. Declare precision only when the expanded interval radius is at most the requested dollar tolerance. A representation can refuse before sampling when its sufficient deterministic bound leaves no positive statistical allowance.

### Conditional containment proposition

Assume valid deterministic bound B, the stipulated independent-binomial response model, a valid nuisance envelope and exact conservative numerical inversion. Conditional on any independently selected fixed validation design, the probability that at least one per-depth binomial interval misses its true response is at most alpha by the union bound. On the complementary event the true amplitude remains in every inverted constraint, hence in their intersection and hull. The affine transformation and deterministic expansion therefore contain P.

It follows that `Pr(precision declared and |midpoint-P|>tolerance) <= alpha`. This is an **unconditional** error bound over validation observations, not an alpha bound conditional on declarations. If the nuisance envelope itself fails with probability beta, an additional valid calibration argument gives at most alpha+beta, without requiring independence for the union bound.

The current implementation uses small floating-point padding and tests, not verified special-function enclosures. The analytical proposition is conditional; formal numerical certification is not claimed. Reusing validation data for optional stopping would require a different statistical argument.

## 5. Discovery design

C6 comprises E001, E014, E025, E030, E038 and E049. The 72 candidates use n=3–6 and c=.125,.25,.5 with the fixed support rule. V2A implements the initial deterministic bounds. V2B changes only the grid bound. The prospective protocols and source snapshots distinguish these iterations from confirmation.

V2C compares fixed n=6,c=.125 against a bound-only representation selector. It uses k=(0,1,2,4,8), three shot budgets, 200 repetitions per cell and ideal, known-noise and supplied-envelope conditions. The direct comparator uses k=0 at the same A-equivalent budget. Raw counts, intervals, refusals and failure states are retained. Truth is used only after representation selection for data generation and evaluation.

## 6. Results

The revised deterministic bound gives a positive one-dollar statistical allowance to 14 of 72 configurations, compared with 4 previously, spanning four rather than one of the six contracts. E030 and E038 remain bound-infeasible in the tested menu. This does not rule out other representations, tighter bounds or different tolerances.

V2C contains 36,000 executed model-based trials and 7,200 pre-refusals. Overall states include 11,814 precision declarations, 24,032 unresolved outputs and 154 incompatible outputs. Twelve erroneous declarations occur across the heterogeneous experiment; detailed cell-level denominators and uncertainty are retained rather than treating this aggregate as an IID rate.

At 32,768 shots per depth, fixed ideal multidepth delivery is 51.08%, versus 33.33% for direct sampling. Executed-trial price containment is respectively 98.42% and 100%. Both use 1,146,880 A-equivalent calls per executed trial. The selected ideal arm delivers in 51.50% of all attempts; it executes only four contracts and its 99.25% containment uses the 800 executed trials, not the 1,200 attempts. No erroneous declarations are observed at this largest budget, which does not prove zero risk.

Full results, including noisy conditions, lower budgets and runtime qualifications, are in [PRICE_INTERVALS_V2C_RESULTS.md](PRICE_INTERVALS_V2C_RESULTS.md). All 43,200 records were checked for unique trial identity, valid counts, interval reconstruction and resource arithmetic. The source comparator's separate golden tests and reduced replication establish a modern reference-code foothold, not a head-to-head pricing victory.

## 7. Limitations and next tests

All stochastic pricing results use a stationary response model. Actual noisy pricing-circuit validation, calibration transfer, drift and correlated observations remain outside the established claim. The six contracts are discovery cases. The selector's aggregate cost reduction is mainly refusal of two bound-infeasible contracts; it does not demonstrate resource-optimal adaptation.

Black–Scholes and quadrature are stronger classical approaches for these validation contracts. A meaningful application comparison requires costed control-variate MC, scrambled Sobol RQMC and a path-dependent transfer case. BAE/BIQAE reproduction, compiled gate accounting and held-out trials are not complete. The [prospective amendment](PROSPECTIVE_AMENDMENT_DRAFT.md) specifies the next gates without presenting unperformed work as results.

## 8. Conclusion

Propagating deterministic representation bounds changes which quantum pricing experiments can legitimately claim dollar precision. Conservative multidepth intervals show useful model-based delivery on part of a small benchmark, while explicit refusals reveal limitations hidden by amplitude-only accuracy targets. The present evidence supports further reliability-focused development, not a submission-ready claim of quantum advantage.

## Reproducibility and declarations

The study uses versioned local source snapshots, raw trial records and hash manifests under `results/journal_sprint/`. The historical CSV/manuscript evidence remains preserved. Before submission, publish a curated reproducibility package after removing unrelated/private material, and add actual funding, competing-interest, code/data availability and applicable AI-assistance statements. Independent author review, contribution confirmation and final approval remain outstanding; they must not be inferred from this draft.
