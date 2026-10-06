# Estimation, confidence, and output: atomic limitation audit

Research checked on 1 October 2026. This is a decomposition of the estimator-related claims in [WHY_NO_ADVANTAGE.md](../../manuscript/advantage-frontier-2026-09-23/WHY_NO_ADVANTAGE.md), with proposed small experiments. It does not change the original benchmark or report new pricing runs. Paper results below are algorithmic results unless otherwise stated. A solved subproblem is not an end-to-end quantum advantage.

The most immediate findings are: phase estimation is optional; controlling every arithmetic gate is unnecessary and already avoided locally; expensive classical moment certification is not required by every quantum estimator; and QSP has already been applied to a structured multi-asset, multi-date contract. None supplies a free replacement for this project's complete source, normalization, financial certificate, or classical comparator.

## Primary sources actually accessed

The following register distinguishes a paper inspected from a possible lead. All links are primary papers or author-hosted papers. Source summaries are deliberately brief; experiment designs below are this audit's proposals.

| ID | Accessed source/version | Relevant evidence |
|---|---|---|
| S1 | [Grinko et al., Iterative quantum amplitude estimation](https://www.nature.com/articles/s41534-021-00379-1), 2021 full article | IQAE uses measured Grover powers without QPE and has rigorous error bounds. Its algorithm is adaptive; removing QPE does not eliminate long Grover chains. |
| S2 | [Fukuzawa et al., Modified IQAE](https://arxiv.org/html/2208.14612v4), 23 February 2023 full HTML | The proved upper bound is `62/eta * ln(6/alpha)` Grover queries. A cost-dependent allocation of failure across rounds removes IQAE's extra log-log factor. |
| S3 | [Kothari and O'Donnell](https://arxiv.org/html/2208.07544v1), 16 August 2022 full HTML | Theorem 1.1 gives error `sigma/n` with constant success using `O(n)` source-code queries, without prior sigma. Sections 3.6 and 4.2 cover Hadamard tests and unknown-variance reductions. Appendix A discusses gate complexity. |
| S4 | [Hamoudi, Quantum Sub-Gaussian Mean Estimator](https://arxiv.org/html/2108.12172v1), 27 August 2021 full HTML | A finite-variance estimator needs no prior variance; quantile estimation handles heavy tails. Theorem 6.6 distinguishes reversible oracle access from access only to prepared state copies. |
| S5 | [Howard et al., Time-uniform, nonparametric, nonasymptotic confidence sequences](https://arxiv.org/html/1810.08240v5), full HTML, published 2021 | Theorem 4 supplies a bounded-variable empirical-Bernstein confidence sequence valid under optional stopping. |
| S6 | [Oshio, Wada and Yamamoto, Parallel amplitude estimation](https://arxiv.org/html/2508.06121v3), 29 June 2026 full HTML | General theorem: RMSE `eta`, query depth `O(1/(eta P)+log P)`, total source/inverse queries `O(1/eta+P log P)`, and `P(n+1)` qubits. Uses GHZ correlations and QSP. |
| S7 | [Stamatopoulos and Zeng, Derivative Pricing using QSP](https://arxiv.org/html/2307.14310v2), 16 April 2024 full HTML | Sections 5.2–6 treat a 3-asset, 20-date autocallable; log-return predicates and QSP remove explicit register exponentiation for that payoff structure. |
| S8 | [Sun, Wang and Blanchet, Repeatedly Nested Expectation Estimation](https://arxiv.org/html/2602.08120v1), 8 February 2026 full HTML | Fixed-depth nesting with Lipschitz outer functions and square-integrable terminal function; deterministic level schedules address variable-time overhead. This audit verified the preprint, not the original document's ICML 2026 attribution. |
| S9 | [Cornelissen, Hamoudi and Jerbi, Near-Optimal Quantum Algorithms for Multivariate Mean Estimation](https://yassine-hamoudi.github.io/files/publications/Mean.pdf), author-hosted full PDF | Input model, covariance, norm, dimension and precision all matter. A dimension penalty and a low-precision regime without a generic advantage preclude a universal scalar-to-vector translation. |
| S10 | [Stamatopoulos et al., Quantum Gradient Algorithms for Financial Market Risk](https://arxiv.org/html/2111.12509v2), full HTML, Quantum 2022 | Quantum gradient estimation can improve on separately computed sensitivities; the discussion explicitly acknowledges classical adjoint automatic differentiation. |
| S11 | [Heinrich, Quantum Summation with an Application to Integration](https://arxiv.org/pdf/quant-ph/0105116), full PDF | Quantum summation/integration under bounded Lp norms, including moment classes beyond bounded payoffs. The access and function class must be matched. |
| S12 | [Ramôa and Santos, Bayesian Quantum Amplitude Estimation](https://quantum-journal.org/papers/q-2025-09-11-1856/), published 11 September 2025, publisher abstract accessed | Bayesian, noise-aware experiment selection is a candidate for numerical constants. Full proof and coverage audit not performed here. |

Local files inspected include [the original source derivation](../controlled_source_completion/DERIVATION.md), [the estimator redesign](../controlled_priority_completion/ESTIMATOR_REDESIGN.md), [the claim ledger](../controlled_priority_completion/CLAIM_LEDGER.md), [the residual derivation](../controlled_residual_feasibility/DERIVATION.md), [the compound results](../compound_feasibility/RESULTS.md), and the corresponding wrapper and schedule code linked below.

## E01 — The quadratic ceiling is a statement about an access problem

**Original location:** §2.1 and §5 Root cause A. **Atomic limitation:** a generic mean-estimation routine cannot obtain an arbitrarily large precision exponent improvement merely by changing its estimator.

**Alternative and status:** Exploit a restricted financial structure before applying mean estimation, or replace the integration algorithm itself. S3 supplies an optimal generic source-access scaling; it does not prove that every pricing formula requires generic mean estimation. **Generic query limitation established; structured escape remains workload-dependent.**

**Transfer conditions:** Identify the same input family, information access, precision norm, output and classical algorithms. A quantum algorithm for a different input representation does not refute a lower bound for the original representation.

**Small experiment:** For one proposed structured escape, write its input oracle and reduce the current payoff to it, counting that reduction. Pass only if the reduced source plus estimator beats the current quantum resource product on the same price. A new asymptotic expression with an unbuilt oracle fails this gate.

## E02 — The symbol k conceals several different costs

**Original location:** §2.1, Failure 4 and §7. **Atomic limitation:** `k*sigma/e` is a sensitivity coordinate, not an executable query schedule.

**Alternative and status:** Replace k with integer counts: source preparations, forward/inverse passes, Grover iterates, maximum chain length, repetitions, phase transformations and readout. **Accounting problem solvable now.** Locally, this already exists for several constructions; no new theorem is required.

**Transfer conditions:** Choose one estimator and its actual source. Compare the redesigned counts, not the superseded billion-call schedule: [ESTIMATOR_REDESIGN.md](../controlled_priority_completion/ESTIMATOR_REDESIGN.md) records 1,203,320/2,967,610 controlled iterations for conditional Hadamard C4/H8, and 7,864,305 for the bounded variant.

**Small experiment:** Produce a single C4 row reconciling forward, inverse and wrapper invocations to the existing emitted wrapper. Pass if every multiply-used routine appears exactly once in the expanded ledger. Report the resulting effective k only afterward; do not assume k=1.

## E03 — Bounded AE pays for range, not automatically residual standard deviation

**Original location:** §2.1 caveat and Failure 6's favorable sensitivity corner. **Atomic limitation:** an attractive variance can be incompatible with the chosen amplitude oracle.

**Alternative and status:** Compare two fully specified constructions: range-normalized bounded AE versus the signed variance-sensitive phase construction. **Partly solved locally:** the implementations are different and have separate counts.

**Transfer conditions:** The existing selector has `p=E[(Y+128)/256]`; dollar mean error e requires amplitude error `eta=e/256`. Replacing its count by `sigma/e` is invalid. For the phase method, the tight moment must apply to the identical digital Y.

**Small experiment:** Feed the same two-point digital distribution to both exact small-register constructions and recover its mean. Pass if error and failure are stated in dollars and all forward/inverse calls are counted. This isolates normalization errors before any finance simulation.

## E04 — QFT and a phase register are optional

**Original location:** §2.1's phase-estimation discretization and §5 Root cause F. **Atomic limitation:** canonical QAE incurs phase-grid and QFT overhead.

**Alternative and status:** IQAE and modified IQAE remove QPE/QFT while retaining bounded-AE guarantees (S1–S2). **Solved algorithmic subproblem.** The existing local Hadamard estimator also already has no IQFT.

**Transfer conditions:** IQAE is a replacement for the bounded-amplitude estimator, not automatically the signed complex-phase estimator. Retain E03's normalization and include initial preparations and the deepest `Q^m` circuit. The published modified-IQAE bound is conservative; it does not establish a small effective k for this price.

**Small experiment:** Reuse the unchanged bounded selector and compare canonical-QAE and modified-IQAE schedules at `eta=(0.002/discount)/256`, `alpha=0.003`. Pass if a valid finite-confidence schedule reduces total compiled source work or paid latency; merely deleting QFT rotations does not pass.

**Immediate arithmetic screen:** S2's general bound at these parameters is approximately `60,320,762 * discount` Grover queries, versus 7,864,305 in the saved canonical schedule. For the project's discount factors near one, that upper bound alone certifies no improvement. Actual adaptive schedules can be much cheaper; they need their own valid latency/query accounting. This is a bound comparison, not a lower bound against IQAE.

## E05 — Every financial arithmetic gate need not be controlled

**Original location:** §3 item 5, “Be controllable.” **Atomic limitation:** an external estimator control might appear to add a control to every arithmetic gate.

**Alternative and status:** IQAE applies ordinary Grover powers. Even controlled reflection/conjugation can factor as `C(A S A†)=(I⊗A) C(S) (I⊗A†)`, with only S controlled; the control-zero branch cancels. **Solved identity, already used here.**

**Local evidence:** [envelope.py](../../research/controlled_source_completion/envelope.py), `controlled_U`, emits uncontrolled graph calls around controlled phase gates. [estimator_bounded.py](../../research/controlled_priority_completion/estimator_bounded.py), `emitted_wrapper`, emits financial/comparator forward calls, controlled Z, and their inverses. The reflection's external-control Z preserves its sign convention.

**Small experiment:** Exact small-unitary comparison of factored and direct-controlled constructions, including a superposed control and clean workspace. Pass requires matrix agreement, including relative phase. The result corrects the explanation; arithmetic savings against these existing factored wrappers are zero.

## E06 — “Uncompute doubles work” depends on the interface boundary

**Original location:** §3 item 4 and Failure 4. **Atomic limitation:** composing individually clean routines can compute and erase intermediates more times than the full phase oracle needs.

**Alternative and status:** Retain arithmetic until phase kickback, then reverse once. **Already solved locally for this redundancy:** `controlled_U(..., fused=True)` and the bounded wrapper operate on graph halves. [DERIVATION.md](../controlled_source_completion/DERIVATION.md) explicitly records the removed redundant cleanup pair.

**Transfer conditions:** This does not erase the need to restore workspace before the next reflection. A classical destructive computation cannot simply substitute for a coherent inverse. Further storage/recomputation changes belong to the compiler audit.

**Small experiment:** Symbolically expand a clean-source composition and its fused graph, then count financial graph traversals. Pass if they implement the same clean phase oracle and one pair is actually removed from a still-unfused caller. If the caller already uses the fused wrapper, record no new gain.

## E07 — 99% confidence does not mandate median amplification

**Original location:** §5 Root cause F. **Atomic limitation:** the text presents repeated runs, medians and fine phase resolution as unavoidable consequences of 99% confidence.

**Alternative and status:** A certified iterative confidence interval, exact hypothesis tests, or another valid estimator can enforce the failure allocation. S1–S2 are constructive examples; local Hadamard tests use exact binomial tails and no IQFT. **This architectural requirement is already removed.**

**Transfer conditions:** Confidence is still required. The complete price's 0.01 failure allowance is shared with source, financial bridge and physical failures; the residual estimator locally receives 0.003. A nominal 99% quantum mean interval is not a 99% complete-price certificate.

**Small experiment:** Reconcile every event in one saved estimator row to an overall union bound. Pass if total failure remains at most 0.01 and error at most the contracted epsilon. Reassigning a deleted error term needs an explicit new ledger.

## E08 — Uniform confidence allocation can waste expensive late-stage queries

**Original location:** Failure 4, “k was enormous.” **Atomic limitation:** a conservative confidence schedule inflates the cost.

**Alternative and status:** Optimize failure allocations and exact finite-sample tests. S2 demonstrates asymptotic benefit from unequal allocations; local priority completion already allocates failure proportional to chain length and certifies binomial tails. **Partly solved and already responsible for the reported large reduction.**

**Transfer conditions:** Adaptive stages need a conditional validity argument. Searching thresholds after seeing favorable measurement outcomes without accounting for that search invalidates the guarantee.

**Small experiment:** Hold the selected local stage geometry fixed; optimize only its rational failure allocation. Pass if exact tail calculations certify the same total failure and fewer weighted controlled calls. Use the current optimized schedule as baseline, not the original conservative QPE schedule.

## E09 — A costly classical variance pilot is not universally necessary

**Original location:** Failure 3 and §5 Root cause F. **Atomic limitation:** certifying moments classically cost 72–255 seconds.

**Alternative and status:** S3's unknown-variance algorithm uses quantile and centering reductions; the local implementation is explicitly only a known-second-moment variant. **Solved in the source-code query model; unimplemented at this project's gate level.** The earlier residual results already acknowledge this escape.

**Transfer conditions:** A fixed-n `sigma/n` theorem does not itself tell us when unknown sigma makes the dollar error small enough. The proposed implementation must supply a valid absolute-error stopping/calibration rule and its cost. It must retain coherent access to source and inverse.

**Small experiment:** Specify the unknown-variance algorithm completely for a bounded, rare-event two-point source, including its stopping rule and all quantile calls. Pass if it supplies an absolute error certificate without importing a pilot variance. A fixed-budget relative-to-unknown-sigma guarantee alone fails the pricing contract.

## E10 — Analytic moment bounds are a concrete alternative to pilots

**Original location:** Failure 3's certification cost. **Atomic limitation:** tight moments were obtained statistically despite a tractable continuous model.

**Alternative and status:** Use proved model identities and interval evaluation. **Already partly solved locally:** [residual DERIVATION.md](../controlled_residual_feasibility/DERIVATION.md), equations (1), (2), (6), (7), (10), supplies lognormal spread moments, truncated put moments, and the global fallback `E[Y²] <= 2 q² E[(A-G)²]` under its stated real-model policy construction.

**Transfer conditions:** Evaluate cancellation-prone formulas with outward error control. These are bounds for the stated continuous law and policy, not automatic bounds for guarded, clipped, finite Box–Muller Y_d. Analytic control expectations may change under that finite law.

**Small experiment:** Evaluate the global analytic fallback for C4 with interval arithmetic and insert it into the existing known-moment schedule. Pass for this subproblem if the bound is rigorous and cheaper to acquire than the pilot; report whether looseness increases quantum query cost enough to offset acquisition savings.

## E11 — A continuous-law certificate cannot silently become a digital-source certificate

**Original location:** §7's unresolved financial errors; tight-moment Failure 5 rows. **Atomic limitation:** the actual estimator's Y_d may have a different moment from real-arithmetic Y.

**Alternative and status:** Derive an L2 coupling bound or bound digital moments directly. **Unresolved for the tight rows.** This is separate from choosing a better mean estimator.

**Audit derivation:** If a proved coupling gives `||Y_d-Y||_2 <= b`, then Minkowski gives `sqrt(E[Y_d²]) <= sqrt(E[Y²])+b`. An L1 expected payoff error by itself does not give the needed L2 bound. Support-only `|Y_d|<100` remains a valid fallback.

**Small experiment:** For one elementary finite-law transform, prove an L2 error bound and propagate it through a restricted smooth payoff. Pass only with all-input/tail control; a small sampled maximum error fails. The final policy indicator will need a separate boundary argument.

## E12 — Sequential statistics can make certification valid under stopping

**Original location:** §5 Root cause F and fixed-N pilot obligations. **Atomic limitation:** one cannot repeatedly inspect a fixed-N interval and stop when it looks favorable.

**Alternative and status:** A confidence sequence for bounded residual-squared observations gives an anytime-valid moment bound (S5, Theorem 4). **Statistical validity solved under the theorem's assumptions; cost benefit unknown.**

**Transfer conditions:** Apply it to independent outer groups or another process satisfying the conditional-mean assumptions. Individual correlated Sobol points are not iid observations. The bounded support term survives a run of zeros; optional stopping cannot prove that unseen rare events are absent.

**Small experiment:** On an exact bounded rare-event distribution, compare the fixed-N pilot and a confidence-sequence stopping rule with the same failure allocation. Pass if validity follows from the theorem and acquisition cost improves on the selected finance case. Coverage simulation is a diagnostic, not the proof.

## E13 — Amplitude loading need not require an arbitrary data-dependent rotation

**Original location:** §2.1 normalization and §5 Root cause C's payoff loading. **Atomic limitation:** converting a fixed-point signed payoff into an amplitude may add transcendental rotation arithmetic.

**Alternative and status:** Append a uniform selector and compare against a shifted integer payoff. **Exactly solved locally:** [estimator_bounded.py](../../research/controlled_priority_completion/estimator_bounded.py), `shifted_selector`, implements the span-256 probability without atan or a moment certificate.

**Transfer conditions:** All selector bits and the financial random bits belong to the reflected state. Range guarantees and signed representation must be valid on every source word. This changes the source/estimator combination and returns to range-dependent query cost.

**Small experiment:** Exhaustively check an 8-bit analog, including negative Y, both flag inputs, range endpoints, and comparator cleanup. Pass requires exact probability and inverse restoration. Production wrapper reuse, not another independently invented amplitude loader, is the next integration step.

## E14 — Enormous nested query counts are not a universal nesting lower bound

**Original location:** Failure 2's `1.1e15`–`4.9e16` conditional calls. **Atomic limitation:** explicit conservative inner and outer schedules multiply into a prohibitive count.

**Alternative and status:** Instantiate sharper nested mean-estimation results with explicit constants. The [local schedule](../../research/compound_feasibility/quantum_schedule.py) uses bounded inner QAE and a signed dyadic outer estimator; its documentation says the stronger estimator is uncompiled. S8 offers deterministic level scheduling for repeated nesting. **Algorithmic alternative established; project cost reduction unquantified.**

**Transfer conditions:** S8 prices a trajectory step as one and function evaluation as zero; D and Lipschitz constants are fixed. Its oracle abstraction does not pay this compiler's arithmetic. Increased logarithmic dependence on D does not change the leading epsilon exponent when D is fixed.

**Small experiment:** Instantiate D=1, a bounded scalar two-point transition, and one Lipschitz outer function. Compute actual integer calls and the coherent wrapper. Pass if the same error/failure budget costs fewer source calls than the local hierarchy, before introducing finance arithmetic.

## E15 — A measured IQAE inner loop cannot directly serve a coherent outer oracle

**Original location:** Failure 2, quantum-inside-quantum estimation. **Atomic limitation:** an outer quantum estimator needs a coherent inner computation and its inverse.

**Alternative and status:** Use a reversible fixed schedule, coherently record all branches, or flatten the financial problem using a certified policy residual. **Partly solved:** flattening is implemented locally, while its policy-regret and baseline certificates remain separate obligations.

**Transfer conditions:** IQAE's intermediate measurement and adaptive classical choice of powers are not a clean unitary. Deferring measurements may require storing records, padding branches and uncomputing the controller. The local compound results explicitly require coherent medians, not measured inner medians.

**Small experiment:** Build a two-outer-state toy: coherently compute an inner estimate, apply the outer payoff, and invert. Pass if the outer-state coherence and all scratch are restored. A routine returning a classical estimate for each separately sampled state fails this test.

## E16 — Heavy tails with finite variance are already within modern mean-estimation theory

**Original location:** §5 Root cause A, heavy-tailed payoffs. **Atomic limitation:** a bounded-payoff AE formulation is inconvenient for unbounded payoffs.

**Alternative and status:** S4 provides quantile-based finite-variance estimation without prior variance information; it does not require a sub-Gaussian input distribution despite its title. **Solved query-model subproblem, conditional implementation.**

**Transfer conditions:** Establish finite second moment for the chosen risk-neutral payoff, a finite-precision source approximation, and a dollar bias budget. An importance sampler must include likelihood weights in its moment and arithmetic costs. The favorable variance of an unweighted sample is irrelevant after reweighting.

**Small experiment:** Use an exactly evaluable lognormal scalar payoff. Compare a proved tail cap, a quantile method and an analytically weighted change of measure. Pass if the full bias plus estimator error is certified and the cost product decreases. This tests tails without a multi-asset compiler.

## E17 — Infinite variance needs a different contract or a different moment theorem

**Original location:** §5 Root cause A, integrability caveat. **Atomic limitation:** `sigma/e` has no meaning when sigma is infinite.

**Alternative and status:** Investigate Lp methods (S11), or explicit clipping with a known pth-moment bound. **Conditional mathematical alternatives; no finance transfer established here.**

**Audit derivation:** If `E|Y|^p <= M_p` for `1<p<2`, clipping at B gives `E|Y-clip(Y,-B,B)| <= M_p/B^(p-1)`. This proves a controllable bias, but its range B grows as the tolerance tightens. Plain bounded AE can therefore be expensive; stronger Lp algorithms deserve separate evaluation.

**Small experiment:** Fix a Pareto toy with known pth moment and finite mean. Derive the cap from the dollar bias, then compare complete finite-precision counts with a robust classical estimator. Pass requires no use of a sample maximum as a tail certificate. A divergent mean makes the requested price undefined, not quantum-hard.

## E18 — Multi-output overhead is not universally sqrt(K)

**Original location:** §6, “Many strikes, portfolios, Greeks.” **Atomic limitation:** the summary compresses several output problems into a single dimension penalty.

**Alternative and status:** Use multivariate mean estimation (S9), exploit payoff correlations or a low-dimensional output basis, or estimate only the requested weighted portfolio scalar. **Conditional:** the task's norm and access model decide the applicable bound.

**Transfer conditions:** K separate prices, one weighted price, and a simultaneous confidence band are different deliverables. Per-output 99% confidence is not 99% simultaneous confidence. Low-rank compression requires a proved reconstruction-error bound, not only pilot covariance.

**Small experiment:** Take three strikes with a shared exact toy distribution. Compare separate AE, scalar portfolio AE and a common output basis under their explicitly different contracts. Pass for the original task only if every requested price meets the same componentwise error and confidence.

## E19 — Greeks can use quantum gradients, but classical adjoints are mandatory comparators

**Original location:** §6, Greeks and shared classical paths. **Atomic limitation:** pricing each derivative separately needlessly multiplies both costs.

**Alternative and status:** Quantum gradient estimation is a real finance algorithmic direction (S10). Its own discussion recognizes classical AAD, which can obtain many pathwise sensitivities together. **Conditional research opportunity; not a universal multi-Greek advantage.**

**Transfer conditions:** Check differentiability/smoothing, the parameter-superposition oracle, gradient bias, units, and which Greeks are delivered. Barrier indicators complicate pathwise derivatives. Quantum gradient access must be synthesized from the actual source.

**Small experiment:** Choose a smooth two-parameter scalar payoff with analytic Greeks. Compare coherent gradient estimation against reverse-mode pathwise differentiation with shared paths. Pass if both price and sensitivity biases are bounded and the total compiled cost improves at the declared precision.

## E20 — Quantum amplitude estimation can parallelize more strongly than independent repeats

**Original location:** §5 Root cause E. **Atomic limitation:** long serial Grover chains limit latency.

**Alternative and status:** S6's entangled parallel AE achieves nearly linear query-depth improvement over a useful P range. **Solved algorithmic depth tradeoff; original text already recognizes it.** Independent repetitions and entangled P-lane AE must not be costed as the same algorithm.

**Transfer conditions:** Each lane contains the source workspace. The theorem's unit-query depth does not equal logical T-depth: multiply by the implemented source depth and charge QSP, GHZ preparation, routing, factories and memory. P is determined by the current compiled source and architecture, not a universal 1–10.

**Small experiment:** Produce P=1,2,4 resource rows using one fixed source manifest and one fixed physical budget. Pass if a finite circuit schedule improves complete latency within the budget. Dividing serial time by P while retaining one source's memory fails.

## E21 — RMSE is not the requested 99% absolute-error guarantee

**Original location:** §1 output contract versus §5 Root cause E's parallel result. **Atomic limitation:** importing an RMSE theorem can hide a confidence overhead.

**Alternative and status:** Convert the guarantee explicitly, or derive a direct high-probability schedule. **Elementary conversion available; optimal constants unresolved.** S6's displayed theorem is an RMSE statement.

**Audit derivation:** If RMSE is at most e/10, Markov's inequality on squared error gives `Pr(|error|>e) <= 0.01`. Alternatively RMSE e/2 gives failure at most 1/4; independent medians can amplify that. With the estimator's smaller allocated failure alpha, the one-run conversion uses RMSE `e*sqrt(alpha)`.

**Small experiment:** Recompute E20's P=2 row with a valid `alpha=0.003` conversion and include repeated runs. Pass if its latency benefit survives. This removes a comparison mismatch without claiming the conservative conversion is optimal.

## E22 — QSP already handles some multi-asset path-dependent payoffs

**Original location:** §5 Root cause C, “simple one-dimensional payoffs.” **Atomic limitation:** register exponentials and payoff arithmetic dominate some sources.

**Alternative and status:** S7 treats a 3-asset, 20-date autocallable. Conditions can be checked in log-return registers and terminal payoff loaded by QSP. Table 1 reports Grover depth 36k to 7.8k, T-count 6.6M to 414k, and 19.2k to 4.7k logical qubits versus its stated arithmetic baseline. **Solved for that structured contract; transfer not established for this basket.**

**Transfer conditions:** A barrier on a sum of asset prices is not a threshold on one log return. Arithmetic averages of exponentials do not inherit this simplification. The cited runtime comparison uses 68% confidence and an assumed one-second classical price, unlike this project's contract.

**Small experiment:** Classify every current barrier/payoff predicate as monotone in one asset, maximum/minimum, sum, or other. Pass a replacement only if a proved log-domain predicate is identical for all inputs. Implement just that predicate before proposing a complete arithmetic-free source.

## E23 — QSP degree, synthesis error and payoff bias must be counted together

**Original location:** §5 Root cause C's arithmetic-free direction. **Atomic limitation:** moving a function from registers to amplitudes can hide polynomial degree and rotation precision.

**Alternative and status:** Choose the encoding and approximation interval jointly, then certify amplitude-to-price error. S7 supplies a concrete example of this design; it is not a universal low-degree payoff compiler. **Partly solved methodology.**

**Transfer conditions:** Count each signal-oracle invocation, state preparation inside it if needed, QSP angle synthesis and repetitions inside AE. If the target amplitude is f and approximation p satisfies `|p-f|<=b`, then probability error is bounded by `b(|p|+|f|)`; dollar normalization multiplies it again.

**Small experiment:** Approximate one bounded scalar payoff factor on a certified interval and use interval extrema to bound its error. Pass if total source-plus-QSP cost beats the emitted arithmetic module at the same dollar bias, not merely at the same polynomial approximation tolerance.

## E24 — The error split e=0.45 epsilon is an optimization choice

**Original location:** §2.1 and §2.4. **Atomic limitation:** the fixed split may buy excessive arithmetic precision or excessive estimator repetitions.

**Alternative and status:** Jointly allocate tail, discretization, arithmetic, estimator and synthesis errors under a single financial contract. **Direct optimization opportunity, not yet evaluated in this audit.**

**Transfer conditions:** Keep deterministic biases separate from failure probabilities. A reduction in one module permits reallocation only when its error certificate is valid. Different estimators may need different normalization and different source precision.

**Small experiment:** Enumerate a small grid of already-certified word widths and three statistical-error allocations. Pass if one valid complete ledger lowers the compiled resource product. Unsupported interpolation between certified widths fails. This experiment can run entirely from existing resource manifests before any new financial sampling.

## E25 — Bayesian or likelihood constants are useful leads, not automatic coverage certificates

**Original location:** §5 Root cause F's call for smaller constants. **Atomic limitation:** conservative worst-case confidence schedules may overspend on benign amplitudes.

**Alternative and status:** S12 proposes Bayesian, noise-adaptive experiment selection. Maximum-likelihood and Bayesian designs merit controlled comparison, but this audit accessed only S12's publisher abstract. **Lead, not a verified replacement.**

**Transfer conditions:** A posterior credible interval is not automatically a uniform frequentist 99% guarantee. Device-noise calibration, priors, aliasing and adaptive experiment selection enter the statistical model. A favorable average count over amplitudes cannot replace a worst-case obligation without changing the declared standard.

**Small experiment:** On a small exact amplitude grid plus adversarial near-alias points, compare design choices with a certified frequentist wrapper. Pass only after proving the selected stopping interval's coverage; empirical coverage alone cannot close the guarantee.

## Suggested order of work

First complete E03–E05 as one tiny bounded-estimator audit: preserve the existing selector, establish the exact normalization, and demonstrate why uncontrolled arithmetic already suffices. This avoids rediscovering a paid optimization. Then compare a certified modified-IQAE schedule to the existing bounded schedule. Separately evaluate E10's existing analytic moment fallback; it is much smaller than compiling a complete unknown-variance algorithm.

The stronger next research branch is E22's predicate classification. It asks whether the *specific contract structure* permits removal of expensive arithmetic. The answer can be settled predicate by predicate. E14's nested estimator, E19's quantum gradients and E20's entangled parallelization are broader branches requiring new source and output models; they should not be combined numerically with the existing favorable sigma, oracle depth and classical timing until those combinations are actually implemented and certified.
