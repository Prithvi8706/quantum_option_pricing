# Reengineering Quantum Option Pricing for Journal Publication

The strongest route is to turn Paper A into a study of **reliable price accuracy under constrained quantum resources**, with an explicit method for allocating those resources and declining to claim precision that the evidence cannot support. A larger depolarizing-noise sweep alone would be an incremental contribution. A tested decision procedure, supported by conditional statistical guarantees, modern quantum comparators, and credible classical alternatives, has considerably more scientific value.

This assessment covers literature and official publishing information available through **9 September 2026**. It assumes roughly three to six months, three contributing researchers, local simulation, limited IBM access, and a preference for zero publication fees. Timeline and compute estimates below are planning assumptions, not measured forecasts. The author confirmed on 9 September 2026 that neither manuscript has been submitted or published. The project can therefore be redesigned directly for an original journal submission.

The recommended first target is **Quantum Information Processing**, using its subscription route with no APC. **Quantum** is a stretch target if the project produces a general methodological result; **Quantum Science and Technology** is a stretch target for a broadly useful algorithm-and-hardware result. Journal acceptance cannot be inferred from completed experiments or a fixed timetable.[^20][^21][^22]

## 1. Assessment of the existing evidence

### 1.1 What is worth keeping

The repository contains a useful foundation: classical references, European and digital quantum circuits, Asian-option experiments, a dashboard, a 250-row historical noise dataset, manuscripts, and an isolated `research/paper_a/` package. The July specification already recognizes most of the scientific weaknesses and proposes a much stronger error-budget study. In the preceding workspace review, the full suite returned **164 passing tests**, and the E0 runner passed its eight semantic checks, selecting support-tail parameter `q_total=1e-5`.

Those results establish that specific software checks pass. They do not validate every manuscript claim or establish that the proposed research phases have been completed. The new package is a foundation and smoke pipeline; the repository does not yet contain the full proposed E1–E7 experimental program.

The next phase should extend that package. The dashboard is useful for communication, but its display-oriented behavior and cached estimates should not define research references.

### 1.2 Critical corrections before any submission

| Existing statement or practice | Evidence from the repository | Required correction |
|---|---|---|
| The noise experiment measures error against Black–Scholes | `expand_sweep()` reads `grid[key]["price"]`; `precompute_qae.py` populated that field using `quantum_call()` | Relabel historical deviations and reconstruct continuous, grid, and circuit references independently |
| $0.203 is an irreducible discretization floor | The stored value is a mean deviation from a cached QAE result, with one stochastic observation per cell | Withdraw that interpretation; isolate deterministic bias and sampling error |
| Amplitude tolerance 0.01 is a one-cent price guarantee | IQAE receives `epsilon_target=0.01` before a contract-dependent payoff transformation | Convert amplitude tolerances and intervals into currency using the actual transformation |
| Approximately 14 queries represent oracle depth/cost | The historical counter is `sum(2*k+1 for k in result.powers)` | Distinguish schedule count, executed shots, A/A-dagger calls, Grover calls, circuit depth, and gate burden |
| A one-qubit IBM run validates full pricing or the noise model | The hardware circuit is a single rotation followed by measurement | Describe it as a primitive sanity check; use pricing circuits for application-level evidence |
| All earlier pricing work ignores noise | The foundational 2020 paper includes quantum hardware and error mitigation | Replace sweeping novelty claims with a precise comparison to prior work[^1] |
| One depolarizing parameter represents current IBM hardware | The historical script uses a synthetic channel without archived device calibration | Call it controlled synthetic noise; identify any device-derived experiment by backend, timestamp, mapping, and channel assumptions |
| All figures support the same 50-contract claim | Springer figure code reads the 10-contract CSV for the heatmap/mean plot and the 50-contract CSV for the frontier | Generate primary figures from one frozen manifest; label intentional subsets |
| Paper B's manuscript has the corrected dimension result | Its actual DOCX still contains slopes −1.14/−0.65 and a crossover near 16–32 | Audit and reconcile manuscript, raw replication outputs, tables, and narrative before reuse |

The latest DOCX finding contradicts optimistic status notes in the README/roadmap. The actual document and its underlying data must determine readiness. Neither the old crossover nor the replacement −0.98/−0.77 values should be promoted to a journal claim solely because a prose file calls them canonical.

### 1.3 A directly reproduced reference mismatch

Recomputing Black–Scholes from each CSV row's original `S0,K,r,sigma,T` gives:

| Synthetic p | Historical mean stored deviation | Recomputed mean absolute error against Black–Scholes |
|---|---:|---:|
| 0 | 0.203334 | 0.303837 |
| 0.0001 | 0.220154 | 0.289059 |
| 0.001 | 0.656951 | 0.751565 |
| 0.005 | 3.478250 | 3.596089 |
| 0.01 | 6.162819 | 6.304171 |

All values are in price units. The mean absolute gap between the cached reference and Black–Scholes is **0.240812** over these 50 contracts. These are arithmetic reanalyses of the old CSV, not new stochastic experiments or corrected publication results. In particular, the slight decrease between the first two Black–Scholes-error rows does not establish beneficial noise; sampling variability and signed bias cancellation have not been resolved.

The historical dataset has volatility values 0.15, 0.20, 0.25, and 0.30, so the known dashboard clamp below 0.15 does not explain this particular mismatch. It still belongs outside a general-purpose scientific pricer.

### 1.4 Additional engineering risks to close

The invocation recorder currently appends records to an in-memory list before running a circuit. That is useful exception instrumentation, but an in-memory append is not durable storage against process termination. Before long experiments, persist planned, started, completed, and failed events; test recovery after interruption between raw and resource writes. A missing shot count must fail or remain explicitly unknown, never silently become zero cost.

Audit noise application against the actual transpiled gate set. The historical code attaches one-qubit noise to `u1/u2/u3`, but source inspection alone does not establish that every executed one-qubit instruction had that name or received the intended channel. Use tiny positive-control circuits and record the submitted instruction stream. Do not claim that noise was absent without reproducing that failure.

## 2. Research landscape and novelty constraints

The field already has noise-aware estimation, low-depth schedules, bias analysis, state-preparation criticism, and resource estimates. The promising gap is their interaction with delivered application accuracy and reliable decision-making. “First error decomposition,” “first noisy QAE,” and “first fair benchmark” would be unsafe descriptions.

| Work and publication status | Relevant established contribution | Consequence for this redesign |
|---|---|---|
| Stamatopoulos et al., *Option Pricing using Quantum Computers*, Quantum, 2020[^1] | Pricing circuits, hardware execution, and mitigation | Hardware noise in quantum pricing is established prior art |
| Brown, Goktas & Tham, *Quantum Amplitude Estimation in the Presence of Noise*, 2020 preprint[^2] | Noise-dependent depth/schedule trade-offs | An optimal-depth observation alone is insufficient novelty |
| Tanaka et al., *Amplitude estimation via maximum likelihood on noisy quantum computer*, QIP, 2021[^3] | Noise-aware likelihood estimation and superconducting-device experiments | Include a competent noise-aware comparator |
| Chakrabarti et al., *A Threshold for Quantum Advantage in Derivative Pricing*, Quantum, 2021[^4] | Detailed derivative-pricing resource estimates | An oracle-count-only break-even argument is below the established standard |
| Herbert, *The Problem with Grover-Rudolph State Preparation for Quantum Monte-Carlo*, PRE, 2021[^5] | A no-speedup result under a particular state-preparation setting | Count loading/preprocessing; do not generalize its theorem to all encodings |
| Giurgica-Tiron et al., *Low depth algorithms for quantum amplitude estimation*, Quantum, 2022[^6] | Depth/query trade-offs and noisy comparisons | Depth capping needs application-level or statistical differentiation |
| *Noise tailoring for robust amplitude estimation*, NJP, 2023[^7] | Randomized compiling to better match a usable noise model | Model mismatch and mitigation cost are established concerns |
| *On the bias in iterative quantum amplitude estimation*, EPJ QT, 2024[^8] | Stopping-related IQAE bias and mitigation by repeating the final round | Do not rediscover adaptive-stopping bias as a new phenomenon |
| Manzano et al., *Alternative pipeline for option pricing using quantum computers*, EPJ QT, 2025[^9] | Direct encoding, signed payoffs, and a modified real-amplitude estimator | More payoff types alone do not establish novelty |
| Ramôa & Santos, *Bayesian Quantum Amplitude Estimation*, Quantum, September 2025[^10] | Adaptive noise-aware estimation, cost trade-offs, and model assessment | The proposed method must outperform or complement a strong modern approach |
| Kashif et al., *Evaluating QAE for Pricing Multi-Asset Basket Options*, IEEE QAI 2025[^11] | Qubit/asset-count accuracy–resource comparisons | A basket extension with qubit sweeps is already occupied |
| Hok & Leitao, *Quantum computing for multidimensional option pricing: End-to-end pipeline*, January 2026 preprint[^12] | Market-calibrated marginals, copulas, and quantum integration | Market-data realism alone is also insufficient differentiation |
| Li et al., *Harnessing Bayesian Statistics to Accelerate IQAE*, Quantum, January 2026[^13] | Bayesian interval construction and improved sampling efficiency | Strong interval methods belong in the comparison set |
| Tabarraei, *Stabilized Maximum-Likelihood IQAE for Structural CVaR*, February 2026 preprint[^14] | Confidence-controlled inference and ambiguity management in another application | Search beyond finance before claiming new statistical safeguards |
| Labib, *QAE beyond power-of-two schedules*, 2 September 2026 preprint[^15] | Improved nonadaptive schedules, depth limits, and noise-aware likelihoods | A new schedule ratio or “noise-aware MLE” is not enough |
| Recchia et al., *Quantum Quasi-Monte Carlo: a window for pre-asymptotic quantum advantage*, 3 September 2026 preprint[^16] | Coherent Sobol construction and a finite-query advantage-window analysis | Directly relevant new work for any quantum-versus-RQMC claim |

Preprints are research claims, not equivalent to reviewed journal results. The two September preprints are particularly recent and should be reproduced before their numerical claims are adopted. This is a targeted literature assessment, not proof that no competing method exists anywhere.

### 2.1 Open directions explicitly identified by prior authors

**Richer noise and real-device validation.** BAE's conclusions identify more complex noise models and real-device execution as future work. A pricing study can test how inference survives coherent error, damping, readout asymmetry, and drift when payoff scaling amplifies amplitude uncertainty.[^10]

**State preparation and payoff normalization.** Manzano et al. identify costly distribution preparation, excessive Grover depth, and normalization/truncation as remaining barriers. A useful response is to quantify and optimize the joint error/cost effect of encoding choices, including their classical setup cost.[^9]

**Noise-adapted schedules.** Labib's September preprint leaves systematic noise-adapted ladder design to future work. The opportunity here is selecting schedules under uncertain, gate-dependent noise and a dollar-accuracy requirement. Its calibrated per-oracle depolarizing parameter must not be treated as an experimentally measured two-qubit gate error.[^15]

**Application-specific quantum QMC.** Recchia et al. explicitly leave financial derivatives and the cost of implementing more complex functions for future study. Their discussion distinguishes comparisons of upper bounds from comparisons of actual errors. A careful option-pricing replication with loading, arithmetic, shots, and noise is a credible longer-term project.[^16]

**Hardware resource constraints in calibrated pricing.** Hok & Leitao identify richer dependence structures, path dependence, and hardware implementation as extensions. Replacing every component with market calibration would considerably expand this project's scope; this is better treated as a later application of the validated methodology.[^12]

### 2.2 Classical competition has also advanced

Use RQMC with competent coordinate construction. Recent work examines effective dimension, Brownian bridge, smoothing, and importance sampling; Fourier-domain RQMC supplies another useful multi-asset comparator.[^17][^18] Nominal path dimension alone does not determine QMC difficulty.

A measured log–log slope close to −1 on a finite sample-size range is not an asymptotic theorem and does not rule out finite-budget quantum improvements. Conversely, an ideal QAE query bound does not demonstrate a runtime advantage. These distinctions should replace Paper B's universal statements.

## 3. Recommended research contribution

### 3.1 Working title and central question

**Reliable Precision in Quantum Option Pricing: Error Budgets, Noise-Aware Resource Allocation, and Classical Benchmarks**

Central question:

> Given an option, a requested price tolerance, a confidence requirement, and a compute budget, which quantum configuration can meet that request under stated assumptions, and when should the procedure return an unresolved or infeasible result?

The hypothesized contribution is a **joint selection-and-validation procedure** over uncertainty resolution, payoff encoding scale, circuit-depth schedule, and shot allocation. It must account for deterministic approximation, finite-shot uncertainty, and noise-model uncertainty in the same price units. The experiments should test whether this procedure improves the reliability–cost trade-off over fixed settings and existing noise-aware estimators.

This is an original research proposal, not a proven new algorithm. Its novelty depends on the implemented rule, the conditional analysis, the demonstrated effect, and the comparison with the work above. A triangle-inequality error budget or a union bound by itself is standard mathematics.

### 3.2 The publishable result should have three parts

1. A validated application-level account of when narrow estimator intervals fail to imply accurate prices, separating representation error from noise-model misspecification and estimator failures.
2. An implementable procedure that selects resources and returns a price interval or an explicit inability to establish the target precision, with a conditional guarantee for the model class actually analyzed.
3. Evidence of the procedure's value on held-out contracts: fewer erroneous precision claims, reduced resource use at comparable reliability, or a well-explained limitation that also affects strong modern comparators.

The main result does not need to be quantum advantage. A rigorous improvement in how quantum algorithms are evaluated or operated can matter to a quantum journal. However, a collection of expected negative outcomes without a general lesson or methodological advance may remain too incremental for the stretch venues.

### 3.3 Alternative routes and selection

| Route | Scientific upside | Main risk | Planning horizon |
|---|---|---|---|
| Finish the July error-budget study | Credible empirical QAE resource study | Correct but insufficiently distinctive | Approximately 8–12 focused weeks |
| **Recommended: add reliable price intervals and joint resource allocation** | Method plus reusable experimental evidence | Conservative intervals may be uninformative; modern baselines may match it | Approximately 12–20 weeks, plus review buffer |
| Quantum QMC implementation for derivatives | Addresses a newly explicit application/resource gap | New arithmetic/loading stack; rapidly moving literature | Approximately 6–9 months |
| Full fault-tolerant derivative-pricing resource estimate | Strong systems/theory potential | Substantial oracle synthesis and architecture assumptions | Approximately 6–12 months or more |

Choose one main route. A QNN, a new PDE solver, a QGAN loader, mitigation, Greeks, Heston, and a quantum QMC circuit do not all belong in the same redesign. The April 2026 QNN option-pricing preprint illustrates that this is a separate competing direction, not a shortcut to making an IQAE study novel.[^19]

## 4. Mathematical design

### 4.1 Preserve the six-price reference ladder

For each contract and circuit configuration, preserve:

`continuous price → support-conditioned price → finite-grid price → ideal encoded circuit price → ideal finite-shot output → noisy finite-shot output`.

With the repository's notation,

\[
P_{\rm circuit}-P_{\rm BS}
=e_{\rm support}+e_{\rm grid}+e_{\rm encode}.
\]

For any raw noisy estimate,

\[
\widehat P_{\rm noisy}-P_{\rm BS}
=e_{\rm support}+e_{\rm grid}+e_{\rm encode}
+(\widehat P_{\rm noisy}-P_{\rm circuit}).
\]

This is an exact signed identity. Do not add absolute errors and call that an equality. Do not assume independently sampled noisy and noiseless outputs isolate a per-run noise effect; compare procedure-level distributions or predeclared expectation contrasts. Adaptive runs under noise can choose different Grover schedules, so there need not be a single scalar “noisy amplitude” common to every round.

### 4.2 Convert requested price accuracy into amplitude accuracy

For the current linearized payoff encoding,

\[
P(a)=e^{-rT}(U-K)\frac{2}{\pi c}
\left(a-\frac12+\frac{\pi c}{4}\right),
\qquad
L_P=\left|\frac{dP}{da}\right|
=e^{-rT}(U-K)\frac{2}{\pi c}.
\]

Here `U>K` and `c>0` belong to the validated domain. An amplitude half-width \(\epsilon_a\) maps to price half-width \(L_P\epsilon_a\). For example, if \(U-K=50\), \(rT=0.05\), and \(c=0.25\), then \(L_P\approx121.1\): amplitude tolerance 0.01 corresponds to about **1.21 price units**, even before deterministic approximation error. This is an illustrative calculation, not an observed benchmark result.

If a deterministic error bound is \(B_{\rm det}\), a sufficient ideal-model condition is

\[
L_P\epsilon_a+B_{\rm det}\le\epsilon_{\$}.
\]

When \(B_{\rm det}\ge\epsilon_{\$}\), this particular sufficient certificate cannot succeed by reducing sampling error alone. That does not prove every configuration is infeasible: the bound may be loose, or the representation can change.

The interaction is scientifically useful: smaller `c` can reduce linearization bias while amplifying the price sensitivity to amplitude uncertainty. More qubits can reduce grid error while increasing circuit cost and exposure to noise. The procedure should choose among these trade-offs jointly.

### 4.3 A concrete, conservative statistical prototype

Start with a fixed schedule chosen from independent pilot data. For each executed depth `k`, collect counts and form a simultaneous binomial interval `[l_k,u_k]` for the physical success probability. Allocate a total statistical failure budget across the fixed set of depths; keep calibration uncertainty in a separate budget.

Under a declared response family \(q_k(a,\eta)\), calibration set \(\mathcal H\), and justified discrepancy bounds \(\delta_k\), construct

\[
\mathcal A=\{a\in[0,1]:\exists\eta\in\mathcal H,
\;q_k(a,\eta)\in[l_k-\delta_k,u_k+\delta_k]
\text{ for every executed }k\}.
\]

Clip probability limits to `[0,1]`. Preserve every feasible amplitude component: a multimodal likelihood cannot safely be reduced to its most convenient peak. If the set is empty, report model incompatibility at the selected test level or numerical failure pending diagnosis; it is not evidence of high precision.

Map a conservative hull of `A` through the validated payoff transformation and expand by a deterministic error bound. Return a precision-qualified price only when the resulting interval meets the requested width. Otherwise return `precision unresolved within budget`, with the limiting layer identified.

**Proof obligation.** If shot sampling satisfies the declared binomial assumptions, the actual response lies within the noise/model envelope, the calibration set contains its nuisance parameters with its stated probability, and the deterministic bound is valid, the simultaneous-event argument yields containment of the continuous target with failure probability at most the allocated sum. A union bound does not require independence between those good events; their individual probability statements still need justification. Pilot-based selection requires valid inference conditional on the pilot, or a separate selection-aware construction.

**Limits.** Fitting a depolarizing curve and failing to reject it does not prove the envelope contains real hardware behavior. Arbitrary unknown coherent errors or drift invalidate such a guarantee unless included in the assumptions. Use the phrase **conditional price certificate** only where these conditions are established. Elsewhere report empirical containment, model diagnostics, and sensitivity to the envelope. Finite-grid numerical inversion also needs a conservative enclosure or a documented numerical error allowance.

A first version should use a fresh, fixed validation batch. An anytime-valid adaptive version is a substantial additional statistics problem and should be promoted only after the fixed version works. Recent Bayesian and robust-estimation papers make it necessary to distinguish this construction from existing interval and noise-assessment methods.[^10][^13][^24]

### 4.4 Resource-selection objective

Choose a configuration \(z=(n,c,k_{\max},\text{schedule},\text{shots})\) to minimize a declared cost proxy, subject to meeting the conditional precision criterion. Use a small enumerated candidate family before proposing a complex optimizer. Include calibration, pilot, compilation, preprocessing, and failed-attempt costs in the appropriate reporting level.

For each submitted circuit `j`, record effective shots `s_j`, Grover power `k_j`, depth `D_j`, and two-qubit count `G2_j`. At minimum report

\[
M_A=\sum_j s_j(2k_j+1),\qquad
M_Q=\sum_j s_j k_j,\qquad
G_2^{\rm total}=\sum_j s_jG2_j,\qquad
D_{\max}=\max_jD_j.
\]

The first expression counts A-equivalent invocations for the conventional construction; it is not a gate count. Custom implementations may need a different decomposition. Report simulator runtime as simulation cost, never as a prediction of QPU speed.

Distinguish one-off pricing from repeated pricing with amortized setup. A controller allowed to consult an exact price during selection has received the answer; ground truth belongs in offline evaluation. Cheap analytic bias bounds are permissible algorithm inputs, but their computation must be counted and their availability stated.

## 5. Experimental program

### 5.1 Workloads

Use European calls as the complete diagnostic benchmark because independent prices are available. They cannot establish practical quantum advantage over their own closed-form solution. Add digital calls as a discontinuous-payoff control. Add a small **arithmetic Asian** test as the primary path-dependent stress case, using geometric Asian prices/control variates for validation.

For larger-dimensional classical experiments, use monitoring dimensions such as 4, 8, 16, 32, and 64. Quantum execution need only cover dimensions that pass the pilot. Do not portray a large classical dimension sweep as if equally large quantum circuits had run. A two-date quantum Asian circuit can test transfer of the method; it cannot establish scalable advantage.

Keep market-model uncertainty distinct from numerical accuracy conditional on the model. Real quotes and heavier-tailed dynamics can be a later extension; they introduce calibration, licensing, and reference questions without automatically strengthening the central contribution.

### 5.2 Required comparators

| Comparator | Purpose |
|---|---|
| Existing IQAE with fixed settings | Historical baseline and failure characterization |
| IQAE with the published final-round bias treatment, where applicable | Distinguish known stopping bias from new effects |
| Depth-limited likelihood estimator | Isolate the value of schedule/depth control |
| BAE or aBAE with a declared noise model | Primary modern noise-aware baseline |
| BIQAE or the September nonadaptive method on a focused subset | Protect against an outdated comparator set |
| Direct `k=0` quantum sampling | Reveal when amplification is not worth its cost |
| Proposed allocation/interval procedure | Test the new contribution |
| Black–Scholes and deterministic quadrature/exact finite-grid summation | Correct targets and strong low-dimensional classical methods |
| Naive MC, control-variate MC, scrambled Sobol RQMC | Practical sampling comparisons |
| Brownian-bridge or PCA RQMC for path dependence | Avoid confusing poor coordinate construction with quantum opportunity |

Reproduce at least one documented benchmark for each imported quantum estimator. Report deviations from reference code, implementation effort, convergence failures, and tuning budgets. Bayesian credible intervals and frequentist confidence intervals must be labeled distinctly; compare their actual target-containment behavior empirically.

### 5.3 Noise models and controls

Use a staged progression: ideal finite-shot sampling; controlled gate depolarization; relaxation/dephasing plus asymmetric readout; then coherent over-rotation or drift as a deliberate model-mismatch challenge. Record channel definitions, parameter units, instruction coverage, topology, optimization level, transpiler seed, and submitted circuit hashes.

A scalar per-gate depolarizing sweep is a controlled intervention, not a universal model of a commercial processor. If hardware access exists, archive backend properties and use narrow matched pricing circuits with `k=0,1,2,4` where feasible. Repeat across calibration sessions if studying drift. Include raw counts, mapping, job IDs, calibration shots, and any mitigation overhead. Do not spend the critical path obtaining a decorative one-qubit result.

### 5.4 Staged matrices and feasibility

The July protocol freezes `c=0.25`, a benchmark, subsets, and limited scope. The proposal here deliberately expands that scope to selectable `c`, stronger baselines, and uncertainty-aware decisions. These changes require a **new prospective protocol version**; they must not silently overwrite or reinterpret outputs from the July design.

| Stage | Initial candidate workload | Completion gate |
|---|---|---|
| R0: evidence audit | Historical CSVs, actual manuscripts, reference pipeline | Every retained claim has a traceable target and source |
| R1: deterministic atlas | 50 European contracts; `n=2..6`; `c={0.05,0.10,0.25,0.50}`; 1,000 reference configurations | Reference identities and encoding bounds verified; `n=6` promoted only if feasible |
| R2: execution pilot | Frozen six-contract subset; `n={3,4}`; three algorithms; two conditions; five independent replicates = 360 runs | Measured cost/failure projections support the next stage |
| R3: core replicated experiment | 50 contracts; `n={3,4}`; ideal plus two controlled noisy conditions; fixed IQAE and proposed method; 20 replicates = 12,000 runs | Budget approval embodied in the frozen protocol; first-attempt outcomes retained |
| R4: comparator and mismatch study | Fixed 12-contract subset; modern estimators; coherent/damping/readout challenges | Matched tuning, independent seeds, interpretable intervals |
| R5: concentrated reliability study | Fixed small set spanning low/mid/high amplitudes and difficult cases; cheap response sampling plus circuit checks | Enough trials to resolve the prespecified failure-rate difference |
| R6: application transfer | Digital calls and feasible arithmetic Asian instances | Independently validated references and matched classical baselines |
| R7: hardware subset | Conditional on access and depth feasibility | Application circuits and traceable calibration, or documented omission |

These are **planning matrices**, not promises to run all combinations. At 30 seconds per run, R3 alone is about 100 hours; at two minutes it is about 400 hours. Those are arithmetic scenarios, excluding scheduling and analysis overhead. Do not launch it before measuring runtime, memory, and failures. If it exceeds the budget, freeze a smaller confirmatory design before examining its outcomes and reduce the claim's scope accordingly.

Use a two-level simulation strategy. For tiny fixed circuits and memoryless stationary noise, exact response probabilities can be computed once and reused for independent binomial resampling of estimator runs. This permits thousands of reliability trials cheaply. Validate sampled response tables against actual circuit execution and identify them as such; they do not replace full-circuit noise studies or model time-correlated drift. All inferential algorithms receive sampled observations, not the stored ground truth.

### 5.5 Statistics that support the claim

The co-primary outcomes should be **delivered price accuracy**, **erroneous precision claims**, and **completion/abstention**, with resource burden reported alongside them. RMSE alone can hide a procedure that sometimes gives a very confident wrong answer.

Define an erroneous precision claim as a run that declares the requested precision established while its estimate lies farther than the requested tolerance from the continuous reference. Report both its unconditional probability and its frequency among declarations. Report the declaration rate too: a procedure that always abstains cannot win merely by producing no false claims.

Twenty repetitions per cell are useful for exploratory RMSE, but inadequate for precise 95% reliability claims. For an independent Bernoulli rate near 0.95, a normal-approximation planning calculation gives roughly 456 repetitions for a 95% interval half-width of 0.02, and 1,825 for 0.01. Use exact/Wilson intervals in the analysis, and conduct a dedicated sample-size calculation for the intended comparison. With zero failures in `R` independent trials, the one-sided 95% upper bound is `1-0.05^(1/R)`; zero failures does not imply zero risk.

For a fixed 50-contract benchmark, primary aggregation should preserve equal contract weights and resample replicates within contract. Bootstrap contracts only for a separately justified claim about a sampled contract population. Set seeds independently by algorithm and run; do not claim common-random-number variance reduction unless the coupling has been designed and checked.

Report raw estimates and intervals before display clipping. Keep exceptions, timeouts, invalid intervals, empty confidence sets, and out-of-budget runs in the first-attempt denominator. Publish sensitivity analyses for missing outcomes. Use held-out contracts or regimes for controller evaluation; a retrospective best configuration is an explicitly labeled oracle comparator.

For RQMC, budget all independent scrambles. For example, 32 scrambles of 1,024 paths cost 32,768 path evaluations, not 1,024. Fit control-variate coefficients on independent pilot data or use a justified alternative. Keep reference uncertainty substantially below the error being resolved, or propagate it into results.

## 6. Ablations and decision gates

| Ablation | Question it resolves |
|---|---|
| Remove deterministic error allowance | Are apparent successes caused by ignoring representation bias? |
| Fix `c` versus select `c` | Does joint payoff scaling matter beyond qubit tuning? |
| Fix `n` versus select `n` | Is a larger circuit always worth the added noise burden? |
| Fix depth versus noise-aware depth | What improvement is already explained by known scheduling methods? |
| Plug-in noise estimate versus calibration uncertainty | Does nuisance uncertainty materially affect reliability? |
| Matched versus misspecified noise family | Where do claimed guarantees stop applying? |
| Remove fresh validation batch | Does reuse of selection data create apparent overconfidence? |
| Ignore versus include setup/calibration costs | Does the practical recommendation change? |

After approximately four weeks, require a correct fixed-schedule prototype and a specific prior-work distinction. After approximately eight weeks, require either evidence of a useful reliability–cost improvement over a modern comparator or a clearly explained limitation worth reporting. These are assessment checkpoints, not deadlines for manufacturing a positive result.

If the method only produces wider intervals and nearly universal abstention, investigate the conservatism and identifiability limits. Do not claim success. If BAE achieves equal or better reliability/cost, the paper can still establish an application-level evaluation result, but its algorithmic novelty claim should shrink. If only fixed-IQAE comparisons are affordable, target the narrower error-budget paper and avoid broad “state-of-the-art” language.

The required novelty gate is a matrix of the **actual** implemented contribution against the closest papers, ideally reviewed by a supervisor or experienced researcher. No web search can guarantee uniqueness. Repeat the search immediately before submission, especially around the September preprints.

## 7. Figures and manuscript architecture

Build six primary figures from one immutable analysis manifest:

1. **Error-layer atlas:** signed support, grid, encoding, and estimation behavior over resolution/scaling; show aggregate and difficult contracts.
2. **Reported precision versus delivered accuracy:** interval width, target containment, erroneous declarations, and abstention.
3. **Reliability–resource frontier:** methods compared at matched accuracy/reliability; include calibration and selection costs.
4. **Resource-selection map:** which resolution/scaling/depth the method chooses as tolerance and noise change, including unresolved regions.
5. **Misspecification stress test:** performance under matched noise, damping/readout asymmetry, coherent errors, and drift.
6. **Application/classical transfer:** digital/Asian cases and strong classical baselines; hardware is an optional panel or supplement if informative.

A useful manuscript sequence is: introduction and scoped contribution; related work and comparison matrix; target definitions/error ladder; procedure and conditional guarantee; preregistered experimental design; main reliability/resource results; application transfer and classical context; limitations and conclusion. Put full manifests, per-contract tables, response diagnostics, mathematical details, and environment specifications in supplements.

Draft the abstract last. Do not promise quantum advantage, universal noise robustness, or a better asymptotic exponent before establishing them. Use publication-quality figures, but scientific coherence should determine the number of figures and pages.

## 8. Journal strategy and cost

Fees below were checked on official publisher pages. Optional gold open access and free subscription publication are different routes. Taxes, institutional agreements, eligibility rules, and prices at acceptance may affect actual charges.

| Journal | Verified cost route | Recommended positioning |
|---|---|---|
| **Quantum Information Processing** | Subscription: **no APC**. Optional OA currently £2,190 / US$3,090 / €2,490[^20] | **Primary target** for a rigorous quantum-method/application study; publishes related noisy-AE research |
| **Quantum** | Standard fee **€600** from January 2025; reduced fee/full waiver options for researchers without publishing funding[^22] | Stretch if there is a significant, generalizable methodological contribution; low cost does not mean an easy review |
| **Quantum Science and Technology** | Subscription publication explicitly **free of charge**. Optional OA £2,930 / €3,335 / US$4,090[^21] | Stretch for broad quantum relevance and a substantial advance; the journal explicitly describes itself as highly selective |
| **EPJ Quantum Technology** | Fully OA; current APC £1,790 / US$2,190 / €1,990; funding/waiver possibilities need confirmation[^23] | Good topical fit, but financially secondary unless actual support is secured |

For a cash-constrained team, QIP's subscription route is the most straightforward starting point. A preprint can improve accessibility, subject to the journal's posting/licensing rules. Quantum is worth considering if the core result applies beyond this one finance benchmark; avoid choosing it simply because its fee is lower than commercial OA journals.

Check VIT's library agreements before paying for OA. Do not assume an Indian affiliation automatically supplies a waiver, and do not pay a publication intermediary to arrange acceptance. No acceptance-rate or turnaround estimate is provided because a reliable project-specific estimate cannot be established from the available evidence.

Neither existing manuscript has been submitted or published, as confirmed by the author. No conference-extension justification or withdrawal from another venue is needed for the present redesign. The unpublished A/B structure can be reconsidered: include enough classical benchmarking to support the strongest coherent journal contribution, without reserving essential evidence merely to preserve a planned paper count. Separate future papers should have distinct research questions and results. Submit overlapping work to only one journal at a time and follow the chosen venue's preprint policy.[^26]

## 9. Collaboration, authorship, and schedule

Additional authors should earn authorship through the redesign. QIP's guidelines describe substantial contributions, intellectual drafting/revision, approval, and accountability; IOP likewise requires all four criteria and prohibits trading authorship.[^20][^25] An administrative or visa-related benefit is not a research contribution. An assigned task is only a plan: the final contribution statement must describe completed work truthfully.

| Researcher | Substantive ownership | Reviewable outputs |
|---|---|---|
| Lead author | Research question, circuit semantics, allocation method, mathematical argument, synthesis | Method specification, reference implementation, derivations, integrated manuscript |
| Collaborator 1 | Statistical design and classical comparisons | Independently validated RQMC/CV baselines, uncertainty analysis, replication code, methods/results drafting |
| Collaborator 2 | Noise experiments and reproducibility | Channel validation, modern quantum baseline reproduction, execution records, optional hardware analysis, methods/results drafting |

Each author should understand the central claim, critically review the final manuscript, approve submission, and take responsibility for their work and the integrity of the paper. If either collaborator cannot contribute at that level, use acknowledgments for appropriate actual contributions rather than an invented authorship role. Publication and review timing cannot be guaranteed to meet an external administrative deadline.

| Period | Scientific work | Exit condition |
|---|---|---|
| Weeks 1–2 | Correct the evidence map, define the integrated contribution, reproduce nearest comparators, draft protocol amendment | Specific contribution and feasible initial matrix |
| Weeks 3–4 | Deterministic atlas, price-unit mapping, response-model prototype, interval validation | Correct minimal procedure with clear assumptions |
| Weeks 5–6 | Resource selection, fixed validation batch, pilot timing/memory/failure study | Frozen confirmatory design and no ground-truth leakage |
| Weeks 7–10 | Core experiments, modern comparators, concentrated reliability tests | Auditable primary results and denominator accounting |
| Weeks 11–12 | Model mismatch and digital/Asian transfer; optional hardware | Scope of generalization established |
| Weeks 13–14 | Ablations, independent reproduction, draft figures/manuscript | Every claim traceable to data or proof |
| Weeks 15–16 | External critique, refreshed search, journal fit decision, submission package | Scientifically defensible submission |
| Reserve: 4–8 weeks | Failed pilots, compute limits, theory revisions, external feedback | Honest schedule adjustment |

This targets readiness, not acceptance. Review and revisions follow on a separate, uncontrolled schedule. If only eight weeks are available, complete the existing error-budget core, narrow the claims, and use the more ambitious method as future work if it is not ready.

## 10. Repository implementation map

Retain the research isolation and introduce new components only after the scientific design is fixed:

| Existing location | Proposed extension |
|---|---|
| `references.py`, `errors.py`, `payoff.py` | Bound provenance, price sensitivities, deterministic atlas exports |
| `recording.py`, `schema.py`, `resources.py` | Durable attempt events, raw counts, retries, interrupted-run reconciliation, total costs |
| `configs/` | Versioned pilot/core/mismatch manifests and amendment record |
| Proposed `estimators/` | Fixed IQAE adapter, modern comparator adapters, conservative interval prototype |
| Proposed `noise/` | Gate coverage tests, response models, calibration envelopes, mismatch cases |
| Proposed `allocation.py` | Enumerated resource policy, cost prediction, independent validation allocation |
| Proposed `analysis/` | Fixed-benchmark aggregation, reliability intervals, ablations, manifest-driven figures |
| Proposed `classical/` | Independently tested CV/RQMC/quadrature comparators |
| Proposed `scripts/` runners | Pilot, deterministic atlas, core, reliability, transfer, and report validation |

Reference implementation tests must challenge the science: deliberately wrong discounting; a mismatched grid; unknown shot costs; incorrect gate coverage; multimodal feasible amplitudes; calibration drift; invalid intervals; interrupted writes; and deliberately infeasible accuracy targets. Do not rely solely on tests that repeat the implementation's own formulas.

Before release, archive the exact code revision or dirty patch, dependencies, configs, streams, hashes, calibration data, first-attempt records, and figure inputs. Publish a documented small reproduction path and separate expensive full runs. Reference truth used in benchmark evaluation should never be confused with computational work performed by the pricing algorithm.

## 11. Submission readiness criteria

The redesigned manuscript is ready for scientific review when:

- The contribution survives a direct comparison with BAE, BIQAE, noisy likelihood methods, low-depth AE, and relevant pricing papers.
- Price units, targets, confidence semantics, and noise assumptions are explicit.
- The algorithm works on held-out cases and has a useful, honestly measured reliability–cost outcome.
- Strong classical baselines and direct quantum sampling are included at matched accuracy and confidence where meaningful.
- Resource totals include shots, failed attempts, calibration, and relevant setup.
- Exact references are independent; their costs and any uncertainty are disclosed.
- Known manuscript/data discrepancies are resolved, with historical data retained under accurate labels.
- All authors have actually made the stated contributions and approved submission.
- Prior-publication status, funding, data availability, and applicable AI-use disclosures are accurate.

The immediate priority is a two-week novelty-and-feasibility sprint around the conservative interval prototype and a modern baseline. If that establishes a distinct, useful effect, invest in the full redesign. If it does not, the existing error-budget foundation still supports a narrower, more defensible empirical paper.

## Sources

The references below are primary papers and official publisher policies. Publication dates are those of the cited records; online journal policies were checked on 9 September 2026. Full-text methods/discussions were inspected for the closest recent papers, including BAE, BIQAE, Manzano et al., Hok–Leitao, and the two September preprints. Other entries include abstract-level screening where indicated by the arXiv link; they should be read completely before implementation or a formal novelty claim.

[^1]: N. Stamatopoulos et al. [Option Pricing using Quantum Computers](https://quantum-journal.org/papers/q-2020-07-06-291/). *Quantum* 4, 291, 6 July 2020. Hardware/noise and pricing prior art.
[^2]: E. G. Brown, O. Goktas, W. K. Tham. [Quantum Amplitude Estimation in the Presence of Noise](https://arxiv.org/abs/2006.14145). arXiv:2006.14145, June 2020. Noise/schedule trade-offs; abstract-level screening.
[^3]: T. Tanaka et al. [Amplitude estimation via maximum likelihood on noisy quantum computer](https://link.springer.com/article/10.1007/s11128-021-03215-9). *Quantum Information Processing* 20, 2021.
[^4]: S. Chakrabarti et al. [A Threshold for Quantum Advantage in Derivative Pricing](https://quantum-journal.org/papers/q-2021-06-01-463/). *Quantum* 5, 463, 1 June 2021. Resource-accounting precedent.
[^5]: S. Herbert. [The Problem with Grover-Rudolph State Preparation for Quantum Monte-Carlo](https://arxiv.org/abs/2101.02240). *Physical Review E* 103, 063302, 2021; arXiv record revised 18 May 2021. Abstract-level theorem-scope screening.
[^6]: T. Giurgica-Tiron et al. [Low depth algorithms for quantum amplitude estimation](https://quantum-journal.org/papers/q-2022-06-27-745/). *Quantum* 6, 745, 27 June 2022.
[^7]: [Noise tailoring for robust amplitude estimation](https://doi.org/10.1088/1367-2630/acb5bc). *New Journal of Physics*, 2023. Noise-model matching and randomized compiling.
[^8]: [On the bias in iterative quantum amplitude estimation](https://link.springer.com/article/10.1140/epjqt/s40507-024-00253-x). *EPJ Quantum Technology*, 25 June 2024. Stopping bias and final-round treatment.
[^9]: A. Manzano, G. Ferro, Á. Leitao, C. Vázquez, A. Gómez. [Alternative pipeline for option pricing using quantum computers](https://link.springer.com/article/10.1140/epjqt/s40507-025-00328-3). *EPJ Quantum Technology* 12, 28, 25 February 2025. Especially conclusions and implementation limitations.
[^10]: A. Ramôa, L. P. Santos. [Bayesian Quantum Amplitude Estimation](https://quantum-journal.org/papers/q-2025-09-11-1856/). *Quantum* 9, 1856, 11 September 2025. [Full text](https://arxiv.org/html/2412.04394v5), especially §6.
[^11]: M. Kashif et al. [Evaluating Quantum Amplitude Estimation for Pricing Multi-Asset Basket Options](https://arxiv.org/abs/2509.09432). IEEE QAI 2025; arXiv submitted 11 September 2025. [Full text](https://arxiv.org/html/2509.09432v1).
[^12]: J. Hok, Á. Leitao. [Quantum computing for multidimensional option pricing: End-to-end pipeline](https://arxiv.org/html/2601.04049v1). arXiv:2601.04049, 7 January 2026. Preprint; especially §4.
[^13]: Q. Li, A. Vidwans, Y. Wang, M. B. Soley. [Harnessing Bayesian Statistics to Accelerate Iterative Quantum Amplitude Estimation](https://quantum-journal.org/papers/q-2026-01-14-1962/). *Quantum* 10, 1962, 14 January 2026. [Full text](https://arxiv.org/html/2507.23074v2).
[^14]: A. Tabarraei. [Stabilized Maximum-Likelihood Iterative Quantum Amplitude Estimation for Structural CVaR under Correlated Random Fields](https://arxiv.org/abs/2602.09847). arXiv:2602.09847, 10 February 2026. Preprint; abstract-level neighboring-method screening.
[^15]: F. Labib. [Quantum amplitude estimation beyond power-of-two schedules](https://arxiv.org/html/2609.02715v1). arXiv:2609.02715, 2 September 2026. Preprint; especially §VII.
[^16]: P. Recchia, Z. Yu, K. Koor, P. Rebentrost. [Quantum Quasi-Monte Carlo: a window for pre-asymptotic quantum advantage](https://arxiv.org/html/2609.03625v1). arXiv:2609.03625, 3 September 2026. Preprint; especially §6.
[^17]: L. Albieri, S. Kucherenko, S. Scoleri, M. Bianchetti. [Effective dimensionality reduction for Greeks computation using Randomized QMC](https://arxiv.org/abs/2504.11576). arXiv:2504.11576, 15 April 2025. Abstract-level screening; motivation for competent coordinate/smoothing baselines.
[^18]: [Quasi-Monte Carlo with Domain Transformation for Efficient Fourier Pricing of Multi-Asset Options](https://arxiv.org/abs/2403.02832). arXiv:2403.02832, initially March 2024. Abstract-level screening of a stronger classical alternative.
[^19]: [Option Pricing on Noisy Intermediate-Scale Quantum Computers: A Quantum Neural Network Approach](https://arxiv.org/abs/2604.19832). arXiv:2604.19832, 20 April 2026. Preprint; abstract-level screening of a separate research direction.
[^20]: Springer Nature. [Quantum Information Processing: publishing options and fees](https://link.springer.com/journal/11128/how-to-publish-with-us); [submission and authorship guidelines](https://link.springer.com/journal/11128/submission-guidelines). Current official policies.
[^21]: IOP Publishing. [About Quantum Science and Technology](https://publishingsupport.iopscience.iop.org/journals/quantum-science-technology/about-quantum-science-technology/). Scope, selectivity, subscription and OA charges.
[^22]: Quantum. [Publication charges to update in 2025](https://quantum-journal.org/updated-publication-charges/), 16 December 2024; [About Quantum](https://quantum-journal.org/about/). Fee/waiver and editorial criteria.
[^23]: Springer Nature. [EPJ Quantum Technology: publishing options and fees](https://link.springer.com/journal/40507/how-to-publish-with-us). Current official policy.
[^24]: R. Kshirsagar, A. Katabarwa, P. D. Johnson. [On proving the robustness of algorithms for early fault-tolerant quantum computers](https://quantum-journal.org/papers/q-2024-11-20-1531/). *Quantum* 8, 1531, 20 November 2024. Model-conditional robustness precedent; abstract-level screening.
[^25]: IOP Publishing. [Author roles and responsibilities](https://publishingsupport.iopscience.iop.org/questions/ethics-of-authorship/). Current official authorship policy.
[^26]: IOP Publishing. [Quantum Science and Technology author guidelines](https://publishingsupport.iopscience.iop.org/journals/quantum-science-technology/). Prior publication, conference extensions, preprints, and manuscript requirements.

Local evidence: `src/noise_experiments.py` (`expand_sweep`), `app/precompute_qae.py` (`run_grid`), `src/black_scholes.py`, `src/quantum.py`, `data/noise_sweep_expanded.csv`, `research/paper_a/payoff.py`, `research/paper_a/recording.py`, `research/paper_a/scripts/run_smoke.py`, `outputs/paper_a_springer/main.tex`, `outputs/paper_a_springer/HANDOFF_CONTEXT.md`, `outputs/paper_a_springer/regenerate_figures_white.py`, `outputs/Paper_B_The_Wrong_Baseline.docx`, and `docs/superpowers/specs/2026-07-27-paper-a-error-budget-roadmap-design.md`. Local files inspected directly; older status descriptions were not accepted as independent evidence of completed research.
