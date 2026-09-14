# Reliability and resource accounting in quantum option pricing

Reading history retained. Current empirical claims and positioning are in the
[week-9 audit](WEEK_9_CLAIM_EVIDENCE.md) and
[focused research refresh](WEEK_9_RESEARCH_REFRESH.md); the tested paid selector
did not improve delivery. Earlier feasibility language is not its current result.

## Research assessment

The defensible candidate is a precision-aware pricing procedure, not a new generic amplitude estimator. Its purpose is to return a dollar interval, or an explicit unresolved result, while accounting for representation error and finite observations. A credible paper must establish when that procedure delivers useful precision, what it costs, and which assumptions invalidate its containment statement. It must not substitute a narrow interval around a discretized circuit target for a narrow interval around the continuous option value.

The six principal readings substantially narrow the novelty claim. Bayesian adaptation, noise-aware likelihoods, depth scheduling, stopping-bias analysis and deterministic-plus-statistical error decompositions already exist. A potential contribution is their careful application to contract-dependent representation selection, with auditable refusal and delivered-precision outcomes. The present evidence establishes feasibility on a small discovery set, not priority, broad usefulness, or quantum advantage.

This supplement updates the larger [reengineering report](../JOURNAL_REENGINEERING_RESEARCH_2026-09-09.md). The relevant versions are identified below; the two September 2026 works remain preprints. Publication recommendations in the earlier report are preliminary and require a fee/policy recheck before submission.

## Findings from the primary papers

### Bayesian quantum amplitude estimation

Ramoa and Santos combine sequential Monte Carlo inference with greedy experimental design and an expanding depth-search window. Their annealed variant selects controls using effective sample size. The noisy simulations use exponential visibility decay; coherence is estimated in a preprocessing phase, while the framework also discusses joint estimation. The reported learning curves use response-model sampling, with randomized amplitudes and several processing conventions. Appendices address numerical representation, parallelism, tuning and classical cost. More complex noise models and execution on real devices are identified as future directions.[^1]

For the pricing study, a noise-aware adaptive schedule alone is therefore not new. BAE is a suitable future comparator, but its posterior uncertainty must retain its Bayesian interpretation. A Gaussian interval constructed from a reported standard deviation is not automatically a finite-sample frequentist confidence interval.

### Bayesian iterative amplitude estimation

Li et al. transfer posterior information between IQAE stages. Normal-BIQAE supplies asymptotic analytical insight; Beta-BIQAE uses conjugate updates and a sampled, fitted beta approximation at stage transitions. Appendix A.8 explicitly distinguishes optimal approximation within the beta family from guaranteed closeness to the exact transformed distribution. Appendix A.9 treats Jeffreys and Clopper–Pearson intervals as practically comparable, rather than algebraically identical. Numerical resource conventions also distinguish Grover-weighted counts from A-equivalent counts. Noise-aware schedules and near-term noise treatment remain future work.[^2]

The comparison must pin the actual source implementation and interval formula, not rely on the label “IQAE-CP.” Reported empirical coverage and asymptotic approximations do not establish a uniform finite-shot noisy pricing guarantee. The practical opportunity is to evaluate such efficient estimators alongside a conservative validation layer, while counting the layer's overhead.

### Maximum likelihood under noise

Tanaka et al. jointly estimate amplitude and a depolarizing-noise parameter. Their decay parameter is tied to Grover iterations, which differs from the pilot's A-equivalent visibility convention. The Fisher-information analysis identifies amplitude/noise confounding and anomalous amplitudes. The paper includes device experiments, classical optimization costs, and an accuracy-to-gate-error/depth/runtime discussion, including detailed appendices. Device benefits depend on the circuit and noise regime; calibration is not universally portable between circuits.[^3]

Consequently, neither joint noise estimation nor accuracy-to-hardware accounting is an unoccupied contribution. The pricing procedure currently assumes a supplied noise value or envelope; it does not reproduce joint estimation. A future measured envelope needs circuit-specific evidence and an explicit failure budget.

### Bias in iterative amplitude estimation

Miyamoto studies a particular modified IQAE procedure with an amplitude-based stopping rule and maximum-likelihood output. Bias is linked to final-stage selection and termination. A fresh final batch with fixed depth and sample size reduces bias empirically, at additional query cost. The investigation includes amplitude-dependent patterns and pseudocode; it is not a universal correction for every implementation called IQAE.[^4]

For the planned comparator, inspect its stopping rule before adopting a correction. A fresh validation batch is a standard protection against reusing selection observations, not a new theorem by itself. Every discarded or replacement observation still contributes to cost.

### Geometric schedules and global ambiguity

Labib studies constant-factor performance of geometric depth schedules, including depth-limited and noise-aware variants. The principal constants are prior-averaged empirical error quantiles, not pointwise interval-coverage guarantees. The appendices examine finite-grid likelihood optimization and numerical Ziv–Zakai bounds; these are not machine-verified global certificates. Near-optimal behavior depends on the percentile and estimator objective. A systematic noise-adapted ladder study remains open.[^5]

The pilot's reference-code replication is useful evidence that this comparator is understood, but it does not establish superiority of the pricing procedure. The latter optimizes a different outcome: useful dollar intervals with explicit non-delivery. Both cost conventions and statistical objectives must be reconciled before ranking the methods.

### Quantum quasi-Monte Carlo

Recchia et al. coherently generate Sobol points and separate finite-net error from amplitude-estimation error. Their higher-dimensional feasibility analysis uses an explicitly empirical model for the finite-net quality parameter. The implementation studies small linear integrands with fixed-point arithmetic. Section 5.2 distinguishes physical cost from the displayed effective cost, which omits shot repetitions; the numerical experiments use 2,048 shots. Section 6 distinguishes comparison of error upper bounds from comparison of actual errors and leaves financial derivatives and implementation costs for further study.[^6]

This is adjacent prior work, not evidence that a finance-specific quantum advantage already follows. A pricing comparison must include all repetitions, finite arithmetic error, nonlinear payoff loading and strong classical alternatives. An upper bound that is smaller than another upper bound does not order the two actual errors.

## Candidate contribution and overlap

| Proposed component | Existing coverage | Defensible status here |
|---|---|---|
| Adapt depth under noise | BAE; noisy likelihood; geometric schedules | Standard comparison axis |
| Transfer information across AE stages | BIQAE | Prior work, not a new claim |
| Account for stopping effects | IQAE-bias study | Implementation-specific audit requirement |
| Split representation and estimation error | Quantum QMC and earlier pricing literature | Standard decomposition |
| Convert amplitude uncertainty into dollars | Affine payoff post-processing | Necessary correctness step |
| Choose representation without exact answers | Application-level candidate | Needs stronger controller and held-out evidence |
| Refuse unsupported dollar precision | Reliability-centered candidate | Feasible pilot; usefulness remains conditional |
| Prove all-branch fixed-sample containment | Standard binomial inversion and union bound | Conditional proposition, not a new statistical method |

The promising central question is: **Can a contract-aware procedure improve delivered precision per counted resource without concealing deterministic error, model uncertainty or non-delivery?** This is narrower and more testable than claiming a superior amplitude-estimation algorithm.

The grid-bound improvement is useful engineering evidence. It exploits cancellation within nearest-grid cells and bounds the remainder using a density derivative; it does not establish a new general integration theorem. Its value should be measured through the number of contracts and tolerances that become feasible, and through the added preprocessing cost.

## What the pilot currently establishes

The 72-configuration discovery grid spans six European contracts, four register sizes and three payoff scales. At the same configurations, the tighter grid bound increases the number with a positive one-dollar statistical allowance from 4 to 14. Four of six contracts have at least one feasible candidate. The two remaining contracts are not proved impossible to price accurately; they fail this particular sufficient bound and candidate menu.

The subsequent finite-shot experiment has 43,200 attempt records, including 7,200 predetermined refusals. It uses synthetic independent binomial observations from a declared visibility model. Exact ideal circuit targets provide simulation truth after configuration selection; this is not execution of tens of thousands of pricing circuits on a noisy device.

At the largest tested per-depth shot count, the fixed ideal multidepth arm declares one-dollar precision in 613 of 1,200 attempts, versus 400 of 1,200 for equal-A-query direct sampling. This demonstrates a pilot difference in delivered precision under the specified response model. It does not compare against Black–Scholes runtime, quadrature, optimized RQMC or the strongest modern AE implementation.

The representation selector changes only one feasible contract's scale and refuses the two bound-infeasible contracts. Its aggregate cost reduction is mainly the consequence of not executing those two cases. The current result therefore does not justify a claim that adaptive resource optimization beats a well-designed fixed procedure.

## Open problems worth pursuing

### Reliable calibration transfer

The largest validity gap is between an illustrative response envelope and a defensible envelope for the actual pricing circuit. First compare actual ideal circuit responses with the analytical model. Then attach noise to specified gates, run positive controls, and measure discrepancies over depth and representation. Calibration uncertainty and model discrepancy must be included separately; a good fit is not a proof that future probabilities remain in an envelope.

The useful negative outcome is a documented boundary where the one-parameter model fails. Introducing more parameters is justified only if their identifiability and calibration costs are controlled. Otherwise the paper should remain explicitly conditional on a response model.

### Representation-aware decision quality

The present selector maximizes the residual probability allowance, not expected total cost. A stronger controller could choose register size, payoff scale, depth cap and validation budget jointly using contract parameters, analytical bounds and independent pilot counts. Its decision rule must be frozen before confirmation and compared with the best inexpensive fixed configurations selected on the same discovery data.

Smaller payoff scale decreases encoding error but increases dollar sensitivity to amplitude error. Larger register size can decrease the deterministic bound while increasing state-preparation and reflection costs. This is the practical trade-off to quantify; a query-only optimization can choose an expensive representation and create an illusory improvement.

### Coverage, delivery and selective reporting

Three outcomes must remain separate: containment of a reported interval, delivery of the requested radius, and the accuracy of the delivered midpoint. A procedure that refuses every task has no erroneous declarations but no utility. Conversely, conditioning only on delivered results can conceal failures. Report refusal-inclusive delivery and error rates, as well as conditional rates with explicit denominators.

The fixed-sample inversion uses simultaneous binomial confidence intervals across depths and retains all feasible amplitude components. Extending this to repeatedly inspected validation data requires a sequential argument or a prospective error allocation. Numerical inversion also needs an explicit rounding analysis before the implementation is described as formally certified.

### Classical competition and path dependence

European Black–Scholes contracts are validation cases, not a realistic setting for speedup over the classical best method. Arithmetic Asian payoffs supply a more demanding transfer case, but their classical baselines need control variates, independent scrambles and Brownian-bridge or PCA construction. All paths and replications count; a per-scramble point count is not total computational work.

Historical dimension-decay slopes are excluded until their raw observations and analysis can be linked. A fresh, fully recorded experiment could replace them, but cannot retroactively validate an undocumented historical run. A quantum claim must also identify the dimensions actually executed quantumly, separately from larger classical-only sweeps.

## Additional current leads

Erle and Koczor's August 2026 preprint claims a nearly optimal depth/repetition trade-off with uniform angle accuracy including boundaries. Huang and Koczor's revised May 2026 preprint formulates amplitude estimation through statistical eigengap estimation and reports a low-depth trade-off. Their abstracts make them relevant comparator-screening candidates, not fully reviewed or reproduced methods in this sprint.[^7][^8]

These leads reinforce the need to avoid a generic “low depth” novelty claim. They should be read and implementation-screened before freezing the main comparator set. The first-two-week feasibility decision can proceed without pretending that this additional screening is complete.

## Recommendation

Advance a **bounded methods-development stage**, not a submission campaign. Preserve the current fixed conservative procedure as the baseline. Promote the adaptive version only after it improves a predeclared delivery/cost outcome on untouched cases and its noise assumptions survive circuit-level checks. If these gates fail, retain the narrower error-budget and reliability study, including the negative findings.

The manuscript should present a modest conditional proposition, independently checked targets, full cost accounting and reproducible evidence. The work is materially stronger than an unqualified noisy-pricing sweep, but publication-worthiness remains contingent on the next validation stage and independent review.

## Sources

[^1]: Alexandra Ramoa and Luis Paulo Santos. [Bayesian Quantum Amplitude Estimation](https://arxiv.org/abs/2412.04394v5), Quantum 9, 1856 (2025). Full-text version v5; Sections 3–6 and Appendices A–J.
[^2]: Qilin Li, Atharva Vidwans, Yazhen Wang and Micheline B. Soley. [Harnessing Bayesian Statistics to Accelerate Iterative Quantum Amplitude Estimation](https://arxiv.org/abs/2507.23074v2), Quantum 10, 1962 (2026), [published version](https://doi.org/10.22331/q-2026-01-14-1962). Sections 3–5; Appendices A.8–A.10, B and C.
[^3]: Tomoki Tanaka et al. [Amplitude estimation via maximum likelihood on noisy quantum computer](https://arxiv.org/abs/2006.16223), Quantum Information Processing 20, 293 (2021). Full PDF v3; Sections 3–4 and Appendices A–C. [Published version](https://doi.org/10.1007/s11128-021-03215-9).
[^4]: Koichi Miyamoto. [On the bias in iterative quantum amplitude estimation](https://arxiv.org/abs/2311.16560v2), EPJ Quantum Technology 11, 42 (2024). [Published version](https://doi.org/10.1140/epjqt/s40507-024-00253-x); Algorithms 1–4 and numerical bias analysis.
[^5]: Farrokh Labib. [Quantum amplitude estimation beyond power-of-two schedules](https://arxiv.org/abs/2609.02715v1), September 2026 preprint. Sections on depth, noise and ambiguity; Appendices A–B. Code replication is documented in the sprint results.
[^6]: Paolo Recchia, Zhan Yu, Kelvin Koor and Patrick Rebentrost. [Quantum Quasi-Monte Carlo: a window for pre-asymptotic quantum advantage](https://arxiv.org/abs/2609.03625v1), September 2026 preprint. Sections 3–6 and Appendices A–C, particularly Section 5.2's query conventions.
[^7]: Jona Erle and Balint Koczor. [Nearly Optimal Amplitude Estimation at any Depth](https://arxiv.org/abs/2608.24434v1), 25 August 2026 preprint. Abstract and version metadata only.
[^8]: Po-Wei Huang and Balint Koczor. [Low-depth amplitude estimation via statistical eigengap estimation](https://arxiv.org/abs/2603.05475v2), revised 7 May 2026 preprint. Abstract and version metadata only.
