# Nonlinear expectations and early-exercise pricing: selective investigation

Search and execution date: **22 September 2026**. This is a bounded investigation, not exhaustive coverage. Existing `ADVANTAGE_RESEARCH_DIRECTIONS.md` and the opening assessment in `QUANTUM_RESCUE_RESEARCH.md` were checked. No manuscript claims were changed.

**No defensible significant quantum advantage established yet.** Nonlinear estimation has a stronger theorem than naive nested amplitude estimation, but the apparent extra classical nesting cost is often removable. A one-decision compound Asian-basket contract is the smallest direct-pricing test. Repeated Bermudan recursion is a worse first implementation: substantial prior art, large depth-dependent constants, and unresolved coherent costs. A newly identified antithetic quantum-MLMC opening is potentially a better direct-pricing research target; see the final section.

## Source screening and reading record

Reading depth means what was actually examined. Downloaded PDFs and extracted text are under `sources/`; they are research reading copies, not project code. A publication label is not an endorsement of a theorem or practical advantage.

| Source, date and status | Reading depth; mechanism | Relevant comparator and assumptions | Decision; evidence and novelty |
|---|---|---|---|
| [Blanchet, Hamoudi, Szegedy, Wang, 2502.05094](https://arxiv.org/abs/2502.05094), v2 22 Oct 2025; [NeurIPS 2025 main-track proceedings](https://proceedings.nips.cc/paper_files/paper/2025/hash/1b12cec51490d59484096f178c0f81be-Abstract-Conference.html) | Full 18-page paper, Algorithms 1–4, Theorem 3.2, Appendices A–C. Quantum estimates construct a new telescoping sequence. | Classical antithetic nested MLMC, plus structural quadrature/regression. Unit-cost reversible source access, Lipschitz outer function, known uniform conditional second-moment and outer-variance bounds. | Investigate resources for one nesting. Level 3 relative to general MLMC; generic mean-estimation lower bound does not establish hardness of a financial subclass. Direct compound-call application already appears in §4. |
| [Sun, Wang, Blanchet, 2602.08120](https://arxiv.org/abs/2602.08120), 8 Feb 2026; [official ICML 2026 poster page](https://icml.cc/virtual/2026/poster/63263) | Accessible arXiv v1: §§1–3 and Appendices A–D read; Algorithm 6 visually checked. Fixed-schedule recursive quantum MLMC. | READ, LSMC, dual methods. Fixed nesting depth, Lipschitz constants treated as constants; trajectory steps charged unit cost and function evaluation free in stated model. | Background/conditional extension, level 3. Already occupies general repeated-nesting/optimal-stopping extension. Final OpenReview PDF/reviews inaccessible (403); do not assert v1 issue persists in final. |
| [Li et al., SPDE/BDSDE pricing, 2606.31076](https://arxiv.org/abs/2606.31076), 30 Jun 2026 preprint | 70-page PDF: §§II–III, theorem assumptions, §IV.F, §V definitions, §VI–VII, Appendix A and selected strong-error arguments inspected; not all long proofs independently checked. Strong-order-one forward/backward scheme plus conditional/nested QA-MLMC. | Classical MLMC, conditional integration, PDE/BSDE solvers, regression. Assumed reversible update oracles; smoothness/moment assumptions; conditional constants depend on noise realization. | Background; level-3 claim. No compiled resources or practical comparison. §VI tests a smooth sine terminal function, not a basket-option crossover. |
| [Chen, Naslidnyk, Briol, Nested Expectations with Kernel Quadrature](https://proceedings.mlr.press/v267/chen25av.html), ICML 2025, 13–19 Jul | Main paper §§3–5, Theorem 1/Corollary 1, Appendices D.2 and F.1/F.3 inspected; author [code](https://github.com/hudsonchen/nest_kq) located, not executed. | Nested MC, MLMC, nested RQMC. Smooth integrands/densities, kernel mean embeddings, dimension-dependent rates; generic dense solve cost matters. | Required classical challenger where feasible. Its finance experiment is shocked butterfly-loss estimation, not direct compound-option pricing. Smoothness theorem fails at max kink; empirical success still matters. |
| [Bartuska et al., 2412.07723](https://arxiv.org/abs/2412.07723), first 10 Dec 2024 | Abstract and metadata only. Multilevel randomized QMC nested integration. | Nested MC and QMC; regularity and inner discretization work. | Investigate as classical comparator before confirming quantum benefit. No theorem applicability asserted from abstract. |
| [Xu, Wang, 2604.03122](https://arxiv.org/abs/2604.03122), 3 Apr 2026 preprint | Abstract only. Outer-variable preintegration removes indicator discontinuity, then nested MLMC/RQMC. | Strong threat to risk-estimation pivots. | Background until full review; financial risk is a larger scope change than direct pricing. |
| [Syed, Wang, READ](https://proceedings.mlr.press/v202/syed23a.html), ICML 2023 | Proceedings abstract, numerical section and author [repository](https://github.com/guanyangwang/rMLMC_RNE) inspected; not full proof audit. Recursive randomized MLMC. | Near-quadratic precision cost under general Lipschitz assumptions; quadratic under stronger conditions, fixed depth. | Include if multiple exercise dates are pursued. Comparing only with exponentially nested plain MC is invalid. |
| [Miyamoto, Bermudan QAE/Chebyshev](https://link.springer.com/article/10.1140/epjqt/s40507-022-00124-3), EPJ Quantum Technology, 7 Feb 2022 | Published abstract/introduction/limitations inspected. Continuation interpolation with QAE values. | LSMC, classical interpolation, PDE; interpolation dimension and continuation regularity. | Prior art, level 3 relative to stated MC methods. QAE plus early exercise is not novel. |
| [Doriguello et al., stochastic optimal stopping](https://drops.dagstuhl.de/storage/00lipics/lipics-vol232-tqc2022/LIPIcs.TQC.2022.2/LIPIcs.TQC.2022.2.pdf), TQC 2022; [full version](https://arxiv.org/abs/2111.15332) revised 2023 | Official proceedings and abstract screened. Quantum least-squares MC. | Classical LSMC; regression approximation and conditioning. | Prior art; do not present generic quantum optimal stopping as a new contribution. |
| [Bayer, Pelizzari, Schoenmakers, primal/dual signatures](https://link.springer.com/article/10.1007/s00780-025-00570-8), Finance and Stochastics 2025; [rough-volatility extension](https://arxiv.org/abs/2501.06758), Jan 2025 | Abstract, framework and author [code availability](https://github.com/lucapelizzari/Optimal_Stopping_with_signatures) screened; not full proof audit. | Path-dependent regression and martingale upper bounds, including non-Markovian models. | Classical threat if switching to rough-volatility American pricing; path dependence alone is insufficient. |

Official [QIP 2026 accepted papers](https://qip2026.lu.lv/programme/accepted-papers/) and [TQC 2026 accepted papers](https://tqc-conference.org/2026/accepted-papers/) were screened. QIP's list includes fault-tolerant QRAM/QLDPC work, but this branch has no quantified pricing consequence. TQC's stochastic-oracle sampling/optimization entry is adjacent; the abstract does not establish option-pricing benefit. Conference posters were distinguished from proceedings. Searches for corrections, follow-up applications and official code for the two nonlinear quantum papers found no accessible author implementation; that is a search limitation, not proof none exists.

## What the strongest nonlinear theorem actually buys

For normalized payoff units, write

\[
P=E_X[g(X,E[\phi(X,Y)\mid X])].
\]

The NeurIPS result replaces the usual inner sample-mean hierarchy with progressively more accurate quantum inner estimates. Its printed complexity is \(\widetilde O(K\sqrt{SV}\log(1/\delta)/\eta)\), compared with \(\widetilde O(\eta^{-2})\) classical nested MLMC; naive double QAE also costs approximately \(\eta^{-2}\). Appendix A exposes extra logarithms and nonzero base-level terms hidden by the shorthand. Source-code access must implement each simulator coherently, with its inverse and workspace. The lower-bound argument concerns general oracle mean estimation, not Black–Scholes compound calls or the best structural pricing algorithm. These are level-3 statements. [Full theorem and proofs](https://arxiv.org/pdf/2502.05094).

Our implications: choose dollar scale B explicitly and \(\eta=\epsilon/B\). Do not insert dollar-valued variances into an asymptotic formula and interpret its coefficient as seconds. Compute the actual sum of per-level quantum calls, both directions of each oracle, clipping, coherent medians and signed arithmetic. A classical median after measurement cannot replace an inner median that the outer estimator must query coherently. Known bounds on conditional **raw second moments**, uniform in outer states, may be much larger than observed unconditional residual variance. Lognormal tails violate a naive bounded-state interpretation; cap/localize with an explicit price-error bound or use a valid finite-moment extension.

For the repeated-nesting paper, Theorem 1.6/Proposition 3.4 has \(O(\eta^{-1}\log^{1+3(D-d)}(1/\eta))\) sample complexity with fixed depth and RMSE. It is not a depth-uniform efficient American-option algorithm. The inaccessible final version prevents checking whether printed v1 pseudocode issues were corrected. [Accessible v1](https://arxiv.org/pdf/2602.08120).

Our independent diagnostic of Algorithm 6: its displayed level-difference expression applies also at n=0, with no special base term. If the terminal payoff is identically 1 and intermediate functions are identity, every displayed difference is 1−1 and their sum is 0, although the answer is 1. Explicitly adding the coarse base fixes this toy calculation. This is an apparent omitted convention in accessible v1, not a disproof of the intended theorem. A constant-payoff regression check is therefore mandatory before implementing any recursive scheme.

SPDE/BDSDE inference: conditional-on-future-noise values are not automatically the ordinary present price. If the final contract requests an unconditional linear expectation, the tower property can remove an artificial outer nesting. A nonlinear risk functional must not be silently substituted for the requested price. For genuine compound/early-exercise payoffs, nonlinear decisions can preserve nesting. The June preprint's Heston discussion explicitly requires localization, regularization or another valid route at the square-root boundary; formal smooth-payoff results cannot be transferred directly to unregularized Heston kinked payoffs. [§III, Remark 5 and §VI](https://arxiv.org/pdf/2606.31076).

## Concrete direct-pricing hypothesis, not a current recommendation to claim advantage

Let \(H=e^{-r(t_2-t_1)}(A_{t_2}-K_2)^+\), where A is a discretely monitored arithmetic basket average, and X contains the asset vector and accrued average at \(t_1\). Price the call on that Asian basket:

\[
P=e^{-rt_1}E[(C(X)-K_1)^+],\qquad C(X)=E[H\mid X].
\]

This remains direct option pricing, although a more specialized contract than the current Asian basket. It has exactly one financially meaningful exercise decision. Start with GBM so numerical time stepping cannot create artificial classical difficulty; simulate each contractual monitoring date exactly. Add stochastic volatility only if a market-model justification and separate discretization analysis exist.

**Falsifiable hypothesis:** for 4–16 correlated assets and 12–52 contractual monitoring dates, at absolute errors $0.01–$0.10 per $100 initial basket and 99% confidence, a compiled variance-sensitive quantum-inside-quantum estimator could cost at most one tenth of the fastest validated classical implementation, including training/setup, under a declared fault-tolerant machine model. This 10× threshold is a research choice, not a theorem: the margin must survive estimation and hardware-model uncertainty. Require it on at least 80% of a predeclared held-out region, no accuracy failures, and no unexplained adverse subregion. Present currency tolerance independently of option price; do not switch to relative errors on low-price contracts.

The new element relative to September's abstract-only suggestion is the full theorem/access audit, 2026 repeated-nesting prior art, and 2025–26 stronger classical competition. Reopening this direction is justified as a short falsification exercise, not because previous failure has disappeared.

### Classical benchmark to build first

The minimum credible implementation is vectorized RQMC with Brownian bridge/PCA, a conditional geometric-Asian control, and antithetic nested MLMC; compare with a separately trained continuation surrogate evaluated out of sample. At small state dimensions, include adaptive conditional quadrature/sparse-grid interpolation. Test nested kernel quadrature if its kernel embeddings and matrix solves remain affordable; count hyperparameter selection, factorization and memory. The ICML kernel result has precision exponent \(d_X/s_X+d_\Theta/s_\Theta\) under its smoothness assumptions, so classical nested integration need not retain the MC exponent. Its generic dense linear-algebra cost is \(O(TN^3+T^3)\), with special reductions; do not use only sample counts. [Theorem 1, Corollary 1, §§3–5 and Appendix F](https://raw.githubusercontent.com/mlresearch/v267/main/assets/chen25av/chen25av.pdf).

Our proposed certification construction avoids treating surrogate accuracy as truth. For any frozen decision \(d(X)\in\{0,1\}\),

\[
E[d(X)(H-K_1)]\le E[(C(X)-K_1)^+]
 \le E[(\bar H_M-K_1)^+],
\]

where \(\bar H_M\) is a conditionally unbiased inner average. The left inequality is pointwise after conditioning; the right is Jensen. Thus train d separately, estimate the policy lower bound on independent paths, and estimate a controlled nested upper bound. A genuine bracket can certify the reference without assuming the regression approximates continuation uniformly. All uncertainty, including training-dependent selection and quadrature bias, must be included. Conditional controls known exactly can reduce inner noise on both sides. A close bracket makes nested quantum evaluation unnecessary for that case.

For several exercise dates, add LSMC and a martingale-dual upper bound, plus READ and practical deep/signature methods as appropriate. Training a surrogate on both platforms cannot be given for free. Classical batch/strike amortization frequently helps more than scalar quantum readout; charge every requested output and any simultaneous-confidence correction.

### Cost relation in consistent units

Measure the best classical wall time \(T_C(\eta)\), including required setup. Let Q be the **full** number of reversible primitive calls generated by the chosen quantum schedule, and \(\tau_Q\) seconds per primitive including fault-tolerant implementation. Then

\[
T_Q=T_{Q,setup}+\sum_\ell Q_\ell\tau_{Q,\ell}+T_{decode},
\qquad T_Q\le T_C/10.
\]

For a provisional model \(T_C=A_C\eta^{-p_C}\) and \(Q=A_Q\eta^{-1}F(\eta)\), where F contains all logarithms/confidence constants, the necessary per-call budget is

\[
\tau_Q\le \frac{T_C/10-T_{Q,setup}-T_{decode}}
 {A_Q\eta^{-1}F(\eta)}.
\]

If RQMC/surrogates give \(p_C\approx1\), tightening accuracy does not create an asymptotic escape from coherent overhead; F can make the quantum side worse. If \(p_C>1\), a crossover remains possible but its location depends on measured constants. These are local slope models, not extrapolation licenses.

An executed **illustrative sensitivity calculation**, assuming Q=1/eta and zero setup, gives the following at eta=0.0001. These are hypothetical budgets, neither lower bounds nor hardware timings:

| Best classical price time | Maximum seconds per quantum primitive for 10× |
|---:|---:|
| 0.01 s | 0.0000001 s = 0.1 microseconds |
| 1 s | 0.00001 s = 10 microseconds |
| 100 s | 0.001 s = 1 millisecond |

Any extra quantum factor A_Q F divides these budgets. Derive \(\tau_Q\) from scheduled T-depth, T-state factory throughput, Clifford depth, routing and decoding. Charge physical qubits and failure budget, including the number of independent quantum jobs. Optimistic hardware assumptions cannot fill unknown oracle constants. This is why measuring classical runtime and compiling one representative coupled oracle are more useful than counting ideal amplitude-estimation calls alone.

## Executed checks and limits

`nonlinear_diagnostics.py` and `nonlinear_diagnostics.json` contain the checks. No quantum circuit or hardware was run.

1. Nine one-asset Black–Scholes call-on-call cases (outer strikes 2, 5, 10; volatility 0.15, 0.30, 0.60; S0=100; inner strike 100; r=0.03; t1=0.5; t2=1) were reduced to a single deterministic Gaussian integral by evaluating the inner call analytically. Observed Python/SciPy calculation times were **2.9–5.5 ms** per case, with 735–861 integrand evaluations. QUADPACK error estimates were at most 1.34e−9 dollars; these estimates are not rigorous enclosures. The separately derived omitted-tail bound was at most 4.93e−16 dollars at nine standard deviations. The demonstration is deliberately not an optimized benchmark; it establishes that this illustrative nested workload is structurally easy and unsuitable as a positive-advantage showcase.
2. The literal v1 recursive telescoping diagnostic returned 0 for exact target 1; the explicit-base version returned 1. This checks an algebraic convention, not the complete algorithm or theorem.
3. Per-oracle time budgets above were evaluated in seconds.

## Proposed one-week falsification stage

Keep all current manuscript/results frozen. Use a separate experiment registry and output directory. A developer workstation suffices for a bounded classical pilot; cap initial work at 16 CPU-hours and 16 GB memory, and report wall time separately from CPU time. GPU confirmation is a later dependency, not an assumed speed factor.

Days 1–2: implement the one-decision contract and policy/inner-average brackets; validate against single-asset conditional quadrature and deterministic-payoff checks. Development cases: d=4,8, m=12, correlation 0.2/0.7, equal weights, volatility 0.2/0.4, maturity 1/3 years, decision at half maturity, inner strike/basket=0.9/1.0/1.1. Define outer strike using 0.5/1.0/1.5 times an independently computed approximate underlying-option value; charge that computation and freeze it before comparisons.

Days 3–4: compare antithetic nested MLMC, ML-RQMC and frozen surrogate with independent lower-bound evaluation. Pilot 16 independent scrambles per grid size, 2^8 through 2^14 outer points where affordable; inner levels 1 through 2^10 with adaptive allocation fixed from pilot data. Training sizes 2^12, 2^14, 2^16; geometric control and PCA/bridge tuning use training/development data only. Fixed root seed 22092026; streams encode method/case/replicate with separate reference seeds. Report empirical interval coverage as empirical; do not label a 16-scramble t interval a finite-sample theorem.

Days 5–7: derive resource schedules for eta corresponding to $0.10, $0.03, $0.01. Compile representative source/coherent conditional/payoff/control subroutines at two precision levels; report gates, signed output accuracy, uncomputation, memory and T-depth. If an optimistic **explicit** compiled cost already cannot approach T_C/10 anywhere, stop this candidate. A pessimistic upper bound failing crossover alone does not prove impossibility; in that situation revise the implementation or report an unresolved constant rather than claim a negative theorem.

Only after a pilot pass, freeze 24 held-out cases drawn from d=6,12,16; m=24,52; correlation 0.1–0.8; nonuniform weights with maximum weight <=0.35; heterogeneous volatilities 0.15–0.50; maturity 0.75–3 years; exercise fractions 0.3–0.7. Use 32 independent randomized replicates for final timing/precision comparisons and independent reference brackets of total width <=epsilon/5. Both methods must price the same continuously distributed **discretely monitored contract**; monitoring dates are contractual, not a numerical-discretization error. Hold out parameter cases as well as seeds. Allocate the 1% familywise failure budget over all claimed cases/outputs or explicitly label confidence per price.

Continue only if the full cost model supports >=10× across >=80% of this frozen region and all relevant methods meet the same output contract. Revise if only a narrow mechanism survives, then register a new confirmation set. Stop if structural classical integration/bracketing defeats the predicted resource budget, or the quantum uniform-moment/tail requirements destroy savings. Do not add harder-looking products after seeing confirmation outcomes.

Four-to-six-week extension, conditional on passing: week 2 complete the best classical implementation and certify reference gaps; week 3 implement and verify the coherent nested primitive; week 4 complete physical resource sensitivity; week 5 run frozen confirmation; week 6 audit novelty and write a conditional crossover claim only if achieved. Many-exercise Bermudans and CVA are separate later projects.

## Newly identified antithetic MLMC opening: stronger direct-pricing alternative

[Herman et al., 2602.03725, §7.1](https://arxiv.org/html/2602.03725v1#S7.SS1) explicitly leaves quantum use of Giles–Szpruch antithetics unresolved. [Giles–Szpruch, Annals of Applied Probability 2014](https://arxiv.org/abs/1202.6283) constructs no-Levy-area corrections with variance order 2 for smooth payoffs, almost 3/2 for piecewise smooth payoffs under additional assumptions. Author [code](https://people.maths.ox.ac.uk/gilesm/mlmc/) includes `antithetic.m`, a Heston example. [Pang–Wang](https://arxiv.org/abs/2305.12992), published in Stochastic Processes and their Applications 178 (December 2024), 104467, extends antithetic methods to some non-globally-Lipschitz SDEs. The abstract, Assumption 3.2 and §6 examples were inspected: twice continuously differentiable diffusion is assumed; the numerical Heston example is a **3/2-Heston** model, not ordinary square-root Heston. This does not automatically resolve that boundary problem. The full HTML of [An et al. 2021](https://arxiv.org/html/2012.06283) was searched for antithetic treatment, with no matching occurrence.

Our mechanism assessment: compute **the value**

\[
Y_\ell=\tfrac12(P_\ell^{fine}+P_\ell^{swapped})-P_{\ell-1}^{coarse}
\]

on one common register of Brownian increments, arithmetically form its signed value, then uncompute. Randomly choosing one fine branch, even through a quantum ancilla, does not preserve the pointwise cancellation. Once the correct random variable has a coherent implementation, generic variance-sensitive quantum MLMC should inherit its variance rate. With cost exponent gamma=1 and weak order alpha=1, beta=3/2 would imply precision exponent 5/4 (up to arbitrarily small losses/logs), whereas beta=2 gives exponent 1 up to logs. These are conditional derivations, not established pricing claims.

The arithmetic coherification itself looks straightforward and may be too small for algorithmic novelty. A meaningful contribution would establish finite-precision distribution/coupling/rounding bounds, compile total costs, and identify a crossover against **the same** classical antithetic MLMC plus conditional smoothing/ML-RQMC. It could extend the correlation regime beyond the current restricted analysis, but that requires proof. Signed residual machinery in this repository is relevant; existing empirical residual variance is not a substitute for a variance-sensitive quantum theorem.

Payoff kinks prevent assuming beta=2 merely from Lipschitz continuity. Heston's square-root boundary prevents importing global smooth-coefficient theorems; Feller's condition alone is not a complete discretization/variance proof. Arithmetic and state-preparation errors must stay below both per-level bias allowances and the decaying level variance. More assets are not themselves helpful. Search strings combining quantum, antithetic MLMC, Giles–Szpruch and Levy areas did not locate an exact prior construction in this bounded search; this is **not** a priority claim.

This route is more tightly connected to direct Asian-basket pricing and has a sharper newly documented mechanism than generic nonlinear nesting. The best next action is a classical antithetic level-variance pilot with a faithful finite-precision signed correction, alongside a minimal reversible resource count. If those fail, the one-decision compound option remains a falsifiable fallback; neither currently fulfills the advantage objective.
