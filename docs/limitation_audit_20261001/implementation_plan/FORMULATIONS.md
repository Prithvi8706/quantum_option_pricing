# Implementation plan: formulations and classical comparators (F01-F32)

Date: 1 October 2026. This is the local execution plan for all 32 entries in [the formulation audit](../FORMULATIONS_AND_CLASSICAL_COMPARATORS.md), grounded in [WHY_NO_ADVANTAGE.md](../../../manuscript/advantage-frontier-2026-09-23/WHY_NO_ADVANTAGE.md). Its machine-readable mirror is [formulations.json](formulations.json). It specifies future work; no new scientific experiment was executed to write this plan.

The exact arithmetic improvements already obtained are useful component results. They do not establish that the continuous option price meets its error budget or that a complete quantum estimator beats the strongest classical method. The task remains one classical discounted price, the declared absolute-dollar error, at least 99% confidence, and complete quantum latency at most one tenth the fastest eligible complete classical latency. Changing the law, payoff, output, monitoring dates or confidence creates a separately labelled task.

For every item, execute the listed small steps in order, record a pass/fail/deferred decision, keep successful local components, and move to the next ready item without asking whether a negative screen is acceptable. A failed sufficient theorem condition closes that direct theorem transfer; it is not an impossibility result. A successful identity, smaller variance or cheap loader completes its component only. A branch is solved for the stated workload when its precise acceptance checks are supported; it is closed when its finite candidate screen fails, and deferred when a named missing mathematical premise prevents an honest test.

Dependencies below require a specific input artifact or interface, not completion of every related investigation. Independent arithmetic work may proceed while a different formulation proof is deferred. G0 freezes task, provenance and protocol. G1 checks reversible arithmetic and cleanup. G2 certifies all dollar-price errors. G3 supplies an explicit estimator schedule with a joint 99% guarantee. G4 supplies actual matched classical timings. G5 includes physical memory, routing, state-factory supply, reaction time and the tenfold complete-latency inequality.

Priority 1 fixes accounting and inputs used by all branches. Priority 2 screens small same-contract transforms or allocations. Priority 3 tackles conditional proofs and cost changes in existing contracts. Priorities 4 and 5 are broader or changed-task research branches; they are deferred unless their G0 financial/output justification exists. This order keeps direct exact-source work ahead of costly speculative formulations.

A proposed 20% improvement is a development screening threshold chosen to justify further implementation; it is not a theorem, an observed result or the 10x advantage target. Small-sample variance and bootstrap/predictive diagnostics may select a development candidate, but cannot supply the final 99% population-price certificate by themselves. An expensive full circuit is justified only after a valid task/law specification, usable error/moment or normalization bounds, a fully specified source/estimator cost ledger, and a frozen comparison against the strongest eligible classical alternative. An unresolved premise is recorded as unresolved, never assigned zero cost.

Freeze training/validation splits, candidate counts, sample sizes, stopping rules and thresholds before new acquisition. Keep all candidate and failed-attempt receipts, and do not tune on validation scrambles or open held-out confirmation cases merely to seek a favorable result. Use the existing pinned environment, new result directories with overwrite refusal, protocol and code hashes, commands, and hash manifests. All implementation and results remain local; no push, publication, upload or external application is part of this plan.

The two most important completed negative screens are retained explicitly. F08's finite-law identity and mixture sampler succeeded, while its equal-source two-probability screen was 10.1519 times worse and the naive shifted-bin sampler changed the law. F15's direct published-bound transfer failed all current cases; A1 still needs a negative-leverage tail proof, and A4 also violates the needed decoupled variance/cross-covariance form. Neither branch earns a replacement pricing circuit from the old pilot alone.

## F01 - Keep measured classical slopes inside their validated range

Status: **ready**. Priority: **1**. WHY source: 2.3, 4 Failure 6, 5A, 6. Inputs: G0.

Existing evidence: [H1_FALSIFIER_RESULTS.md](../../../docs/research_investigation/2026-09-23/H1_FALSIFIER_RESULTS.md), [barrier_fast_classical.py](../../../research/advantage_frontier_20260923/barrier_fast_classical.py), [scrambles.py](../../../research/frontier_classical_20261001/scrambles.py).

Extract the archived independent-scramble errors and timings; fit adjacent three-size windows before acquiring one next-size B4x12 development batch.

1. Record sample counts, scramble IDs, timing inclusion rules and error references; exclude historical modelled times from direct timing rows.
2. Fit uncertainty across scrambles, not across dependent points inside a scramble, and freeze the next-size predictive interval before acquisition.
3. Acquire 32 new development scrambles at one next sample size, using the existing best transform, and compare the observed error and time with the frozen prediction.

Alternatives: Piecewise finite-range cost curves; A conservative measured-range envelope; Direct acquisition at the target accuracy if the projected range is unsupported.

Acceptance checks:

- Every timing row is labelled measured, fitted or assumed.
- The held-out development batch's replicate-error estimate lies inside the preregistered 99% predictive interval and the timing prediction is within 20% of the measured batch time.
- Claims outside the validated sample-count range retain extrapolation uncertainty and never become a classical lower bound.

Stop rule: Use archived fits plus at most one new next-size batch. If prediction fails, close that extrapolation and use measured-range rows; do not refit and reacquire repeatedly until a preferred exponent appears.

On pass: Deliver a validated finite-range cost table to G4 and F31; retain alternative classical methods in the eligible menu.

On failure: Replace the unsupported frontier with measured points and uncertainty; the original source-cost optimization can still proceed.

Fresh artifacts:

- `results/limitation_program_20261001/F01_<run>/protocol.json`
- `results/limitation_program_20261001/F01_<run>/slope_windows.csv`
- `results/limitation_program_20261001/F01_<run>/prediction_check.json`

## F02 - Separate path variance from randomized-quadrature variance

Status: **audit**. Priority: **1**. WHY source: 2.1, 2.2, 2.3, 4 Failure 3. Inputs: G0.

Existing evidence: [H1_FALSIFIER_RESULTS.md](../../../docs/research_investigation/2026-09-23/H1_FALSIFIER_RESULTS.md), [RESULTS.md](../../../docs/controlled_residual_feasibility/RESULTS.md), [parity.py](../../../research/controlled_residual_feasibility/parity.py).

Build one ledger row per estimand/transform distinguishing one-path sigma, residual bounds, and independent-scramble estimator variance.

1. Name the exact classical integrand and quantum finite-law integer function for each row.
2. Attach the covariance/normalization proof or measurement to each claimed variance reduction.
3. Reject any ledger row that assigns a smoothed classical variance to an unsmoothed quantum oracle; retain the valid accounting row without rerunning established identities.

Alternatives: Plain-payoff quantum estimation with independently optimized classical RQMC; Implement the same coherent control and charge its cost; Compare distinct eligible transforms at the same final dollar error.

Acceptance checks:

- All candidate rows distinguish sample variance and variance of an independently scrambled estimate.
- Every quantum variance benefit has an implemented source or fully specified coherent transform with error and cleanup costs.
- The ledger does not use an iid Monte Carlo sigma/e cost law as a substitute for measured RQMC error.

Stop rule: Audit the finite set of active benchmark rows once. Mark unsupported benefits unavailable until their source interface exists; do not block other valid rows.

On pass: Supply the estimand/variance interface to G3, G4 and F20.

On failure: Remove the unsupported variance credit and recompute that row's screen; this fixes accounting rather than proving a new speedup.

Fresh artifacts:

- `results/limitation_program_20261001/F02_<run>/estimand_ledger.json`
- `results/limitation_program_20261001/F02_<run>/unsupported_credits.json`

## F03 - Verify smoothness of the transformed Gaussian integrand

Status: **ready**. Priority: **2**. WHY source: 2.3, 5A. Inputs: G0.

Existing evidence: [barrier_fast_classical.py](../../../research/advantage_frontier_20260923/barrier_fast_classical.py), [H1_FALSIFIER_RESULTS.md](../../../docs/research_investigation/2026-09-23/H1_FALSIFIER_RESULTS.md).

Write the mixed-derivative and tail assumptions for one existing preintegrated call and one barrier integrand before assigning an RQMC theorem rate.

1. Express the actual inverse-normal/PCA/preintegration map and locate exercise, active-date and endpoint singularities.
2. Bound the required mixed derivatives in the claimed function space, including Gaussian endpoint behavior; numerical finite differences are diagnostics only.
3. Try one tail-preserving alternative coordinate transform if the assumptions fail and keep the original contract and law.

Alternatives: A weighted Gaussian function-space analysis; Preintegration plus explicit tail truncation/error bound; Report a measured rate without a theorem claim.

Acceptance checks:

- Each theorem hypothesis is either proved for the implemented integrand or marked unverified.
- Any truncation or transformation bias is bounded by its G2-assigned dollar allowance.
- A failed smoothness proof does not erase directly measured classical performance or assert a lower bound.

Stop rule: Inspect two integrands and at most one alternative transform. If a required derivative bound remains absent, close the theorem-transfer claim and retain empirical performance.

On pass: Use the proved function-space interface in F04 and classical comparison; no high-dimensional rate is inferred from a two-dimensional pilot.

On failure: Keep slopes as measurements, identify the actual singularity, and hand active-date issues to F06.

Fresh artifacts:

- `results/limitation_program_20261001/F03_<run>/assumption_map.md`
- `results/limitation_program_20261001/F03_<run>/derivative_bounds.json`

## F04 - Test structured integration of a certified residual

Status: **conditional**. Priority: **3**. WHY source: 2.3, 5A. Inputs: G0, F03, F02.

Existing evidence: [FORMULATIONS_AND_CLASSICAL_COMPARATORS.md](../../../docs/limitation_audit_20261001/FORMULATIONS_AND_CLASSICAL_COMPARATORS.md), [polynomial_residual.py](../../../research/journal_sprint/polynomial_residual.py), [run_polynomial_residual.py](../../../research/journal_sprint/run_polynomial_residual.py).

Build two frozen interpolation levels for one already-smoothed two-dimensional development integral and certify the residual range or moments.

1. Use an analytically integrated coarse interpolant and record all construction samples and classical work.
2. Bound the residual on the declared truncated domain and charge its tail separately; measure the same residual with classical RQMC.
3. Specify a clean residual oracle and an explicit 99% schedule, then screen total interpolation, source and readout cost against plain AE and interpolant-plus-RQMC.

Alternatives: Piecewise Chebyshev interpolation; Sparse-grid residual integration; Hierarchical quadrature with deterministic coarse mean.

Acceptance checks:

- The certified residual and tail satisfy the assigned G2 error budget.
- A source-plus-estimator ledger predicts at least 20% lower complete quantum cost than plain AE at the same error and confidence before full compilation.
- The paired classical comparison includes the identical interpolant and its training/setup cost; any Sobolev theorem uses verified smoothness and dimension assumptions.

Stop rule: Try two interpolation levels on one two-dimensional case. If certification is unavailable or neither complete schedule improves the quantum baseline, close this pilot before high-dimensional circuits.

On pass: Compile one small clean residual and hand its certified cost interface to G1/G3; transfer to the barrier is a separate proof task.

On failure: Archive the residual bounds and best classical result; do not claim generic p_Q has changed for the repository barrier.

Fresh artifacts:

- `results/limitation_program_20261001/F04_<run>/interpolant.json`
- `results/limitation_program_20261001/F04_<run>/residual_certificate.md`
- `results/limitation_program_20261001/F04_<run>/paired_cost.json`

## F05 - Charge the whole payoff in coherent Sobol integration

Status: **conditional**. Priority: **3**. WHY source: 6. Inputs: G0, F01, F02.

Existing evidence: [FORMULATIONS_AND_CLASSICAL_COMPARATORS.md](../../../docs/limitation_audit_20261001/FORMULATIONS_AND_CLASSICAL_COMPARATORS.md), [basis.py](../../../research/frontier_classical_20261001/basis.py), [scrambles.py](../../../research/frontier_classical_20261001/scrambles.py).

Specify a coherent XOR network for the exact small Sobol matrices used by one actual development payoff, with classical enumeration of the same points.

1. Check each coordinate bit against classical Sobol generation and include the inverse network.
2. Compare the same payoff, point count and truncation using classical independent scrambles rather than discrepancy bounds alone.
3. Add the real payoff source, finite-net bias and 99% estimation schedule to the net-generation cost.

Alternatives: Direct binary-linear Sobol preparation; Digital shift/scramble networks with charged randomness; Classical RQMC with the same matrices and coordinate ordering.

Acceptance checks:

- The small coherent coordinate generator matches every enumerated index and cleans all ancillas.
- Finite-net approximation error has a valid dollar allowance, separate from the quantum sampling uncertainty.
- Complete scheduled cost, including payoff and confidence, improves its plain-source quantum baseline by at least 20% before large compilation, and remains compared with measured RQMC.

Stop rule: One small net and two powers of two are sufficient to screen the route. Stop if the query saving disappears after confidence or full-source cost; a cheap loader alone does not reopen advantage.

On pass: Deliver the proved coordinate-loader interface to G1/G2/G3 and retain the strongest classical transform.

On failure: Close the tested quantum-QMC schedule while retaining exact net generation as a reusable component.

Fresh artifacts:

- `results/limitation_program_20261001/F05_<run>/sobol_network.json`
- `results/limitation_program_20261001/F05_<run>/point_equivalence.json`
- `results/limitation_program_20261001/F05_<run>/complete_screen.json`

## F06 - Isolate the active barrier-date switching surface

Status: **ready**. Priority: **2**. WHY source: 4 Failure 6, 5A, 6. Inputs: G0, F02.

Existing evidence: [barrier_fast_classical.py](../../../research/advantage_frontier_20260923/barrier_fast_classical.py), [H1_FALSIFIER_RESULTS.md](../../../docs/research_investigation/2026-09-23/H1_FALSIFIER_RESULTS.md), [run_barrier_development.py](../../../research/journal_sprint/run_barrier_development.py).

Instrument the existing B4x12 development preintegration to record the minimizing barrier date and gap between the two smallest roots.

1. Use fixed development paths to relate root ties to replicate error without changing the monitoring dates.
2. Implement one tie-local domain partition and one two-direction conditioning pilot, each with an explicit treatment of the residual integration.
3. Freeze choices on pilot scrambles, then compare 32 independent validation scrambles at two sample sizes with full timing.

Alternatives: Partition by active barrier date; Smooth only near two-root ties; Two-direction preintegration with certified numerical quadrature.

Acceptance checks:

- The transformed method computes the same discretely monitored barrier payoff; any quadrature bias is bounded within the assigned G2 allowance.
- On independent validation data, cost times replicate variance is at most 0.8 of the existing preintegration at both frozen sizes, with uncertainty reported.
- Price differences agree with a valid independent error interval; empirical agreement alone is not a continuous-price certificate.

Stop rule: Test exactly two local transforms on B4x12. Retain failures, and stop before B8 or coherent smoothing if neither passes the frozen cost/error screen.

On pass: Improve the matched G4 comparator first; only a separately charged coherent version may receive the same smoothing credit.

On failure: Close these two smoothing mechanisms and retain the diagnosed switching surface; do not assert that every possible barrier smoother fails.

Fresh artifacts:

- `results/limitation_program_20261001/F06_<run>/active_date_diagnostics.json`
- `results/limitation_program_20261001/F06_<run>/paired_scrambles.csv`
- `results/limitation_program_20261001/F06_<run>/decision.json`

## F07 - Screen rare-event proposals with their likelihood-ratio costs

Status: **ready**. Priority: **2**. WHY source: 4 Failure 6, 6. Inputs: G0, F02.

Existing evidence: [barrier_oss_pilot.py](../../../research/advantage_frontier_20260923/barrier_oss_pilot.py), [barrier_fast_classical.py](../../../research/advantage_frontier_20260923/barrier_fast_classical.py), [H1_FALSIFIER_RESULTS.md](../../../docs/research_investigation/2026-09-23/H1_FALSIFIER_RESULTS.md).

Fit one scalar or low-rank Gaussian tilt using separate B4x12 development training data, freeze it, and measure the exact weighted estimator.

1. Write and test the density ratio under the repository covariance; prove absolute continuity and the needed moment or boundedness conditions.
2. Charge the fit, proposal generation, weighted payoff and any smoothing; validate with 32 independent scrambles on the frozen proposal.
3. Compare with existing preintegration and one-step survival at equal final error; specify a coherent likelihood-ratio circuit only if the total screen passes.

Alternatives: Frozen Gaussian mean tilt; Tilt plus active-subspace preintegration; A separately specified unbiased survival SMC estimator with dependence-aware uncertainty.

Acceptance checks:

- The estimator preserves the original law and payoff, with a verified likelihood-ratio identity and tail/error accounting.
- Training-inclusive cost times replicate variance is at most 0.8 of the best existing comparator on two frozen sample sizes.
- An SMC alternative uses an uncertainty analysis valid for its dependence; no coherent resampling or likelihood ratio is credited for free.

Stop rule: One trained tilt and one optional active-subspace extension; no repeated proposal tuning on validation scrambles. Defer SMC if the simpler route fails and lacks an explicit uncertainty proof.

On pass: Update G4 with the best matched classical method; feed the fully specified transform to F20 before any quantum circuit work.

On failure: Archive the negative equal-time result and close that fitted proposal; other rare-event methods remain untested rather than disproved.

Fresh artifacts:

- `results/limitation_program_20261001/F07_<run>/frozen_proposal.json`
- `results/limitation_program_20261001/F07_<run>/likelihood_ratio_proof.md`
- `results/limitation_program_20261001/F07_<run>/equal_time_screen.json`

## F08 - Keep the exact bounded rewrite; reject the losing two-probability shortcut

Status: **partial**. Priority: **2**. WHY source: 2.1, 5A, 5F. Inputs: G0, F02.

Branch decisions: finite identity and sampler: **complete**; equal source two probability shortcut: **closed**; naive shifted finite grid: **closed**; single predicate rewrite: **conditional**.

Existing evidence: [experiment_bounded_probabilities.py](../../../research/limitation_audit_20261001/experiment_bounded_probabilities.py), [summary.json](../../../results/limitation_audit_20261001/bounded_probabilities_v1/summary.json), [EXECUTION_RESULTS.md](../../../docs/limitation_audit_20261001/EXECUTION_RESULTS.md).

Derive the finite-law single-indicator identity m*P_QA(U*A>K and survival), with exact finite tilt weights, and screen its normalization before compiling a sampler.

1. Retain the executed finite identity error 3.11e-15 and exact mixture sampler; mark the equal-source two-probability schedule closed because its inverse-precision screen is 10.1519 times worse.
2. Write the finite-uniform rounding bound, interval for m, and complete dollar-error allocation for the single predicate; do not replace finite tilt by shifted CDF bins.
3. Compare the single-predicate schedule with direct bounded-payoff estimation and the same classical measure change, including mixture, path and barrier work.

Alternatives: One bounded predicate under the exact size-biased finite law; The bounded payoff (1-K/A)+ with a charged reciprocal; Retain the original source when normalization cost dominates.

Acceptance checks:

- The finite-law identity is checked by exhaustive enumeration on a small grid, including A=0 and event endpoints.
- Finite-uniform, normalization, sampler, arithmetic and continuous-law errors each have assigned bounds whose sum satisfies G2.
- The complete explicit 99% schedule is at least 20% cheaper than direct bounded-payoff estimation before sampler compilation; changing normalization alone is insufficient.

Stop rule: Evaluate the one-predicate and reciprocal ledgers once. If neither beats direct estimation, close both for this workload; do not repeat the already losing two-probability screen without a quantitatively new source-cost premise.

On pass: Emit one tiny certified finite-mixture sampler and predicate; only then hand it to G1/G2/G3 for scale-up.

On failure: Keep the exact mathematical identity and finite sampler as completed components, but leave the pricing implementation unchanged. The naive shifted-grid branch stays rejected because it changes the finite law.

Fresh artifacts:

- `results/limitation_program_20261001/F08_<run>/single_predicate_proof.md`
- `results/limitation_program_20261001/F08_<run>/error_ledger.json`
- `results/limitation_program_20261001/F08_<run>/normalization_screen.json`

## F09 - Do not retain variance-based quantum rates in an infinite-variance model

Status: **conditional**. Priority: **5**. WHY source: 5A, 7. Inputs: G0, F08.

Existing evidence: [FORMULATIONS_AND_CLASSICAL_COMPARATORS.md](../../../docs/limitation_audit_20261001/FORMULATIONS_AND_CLASSICAL_COMPARATORS.md), [summary.json](../../../results/limitation_audit_20261001/bounded_probabilities_v1/summary.json).

Write a separate candidate contract only if a financially justified heavy-tail law is already needed; prove its first and p-th moments before proposing an estimator.

1. Keep current GBM cases outside this branch: they do not supply an infinite-variance example.
2. Search first for a tractable bounded re-expression or change of measure and compare robust classical estimation and importance sampling.
3. If 1<p<2 is the usable premise, substitute the correct quantum precision exponent and all moment constants into a finite-confidence ledger.

Alternatives: A bounded probability representation; Truncation with a verified p-th-moment tail bound; Robust classical mean estimation and importance sampling.

Acceptance checks:

- The new contract and model are explicitly separate from the original one-price GBM/Heston benchmark.
- An explicit usable moment bound and coherent sampler specification exist; at p=3/2 the quantum exponent is 3/2 rather than one.
- The complete cost screen includes truncation, confidence and the strongest eligible robust classical methods.

Stop rule: One assumption audit and one ledger per justified model. If no independently justified model or finite usable moment constant exists, defer the branch without inventing a harder distribution.

On pass: Create a separate exploration protocol and pass its moment interface to G2/G3; its success does not solve the original contract.

On failure: Close the nominated heavy-tail model or defer the branch; never treat high classical exponents alone as evidence of advantage.

Fresh artifacts:

- `results/limitation_program_20261001/F09_<run>/candidate_contract.json`
- `results/limitation_program_20261001/F09_<run>/moment_proof.md`
- `results/limitation_program_20261001/F09_<run>/matched_screen.json`

## F10 - Reallocate multilevel work using separate classical and quantum costs

Status: **partial**. Priority: **2**. WHY source: 4 Failure 1. Inputs: G0, F02.

Existing evidence: [RESULTS.md](../../../docs/antithetic_feasibility/RESULTS.md), [multilevel.py](../../../research/antithetic_feasibility/multilevel.py), [estimator.py](../../../research/antithetic_feasibility/estimator.py), [cost_model.py](../../../research/antithetic_feasibility/cost_model.py).

Reuse the archived antithetic correction variances and enumerate all hybrid classical/quantum level assignments with their complete source costs.

1. Retain the demonstrated 570-600-fold correction-variance reduction as a component result shared by both architectures.
2. Optimize allocations under one explicit dollar/failure-probability budget, including base uncertainty and signed correction estimation.
3. Use current certified per-level costs or clearly labelled optimistic bounds; reacquire a level variance only if the selected allocation depends on an unsupported measurement.

Alternatives: Classical base plus selected quantum correction levels; All-classical optimal MLMC; Analytic coarse mean plus residual base and antithetic corrections.

Acceptance checks:

- The allocation includes every level, setup, bias and joint 99% failure budget.
- The best candidate improves the complete original quantum schedule, and its optimistic complete cost is below the fastest eligible classical total before further compilation.
- An advantage claim is deferred to G5; tiny correction variance or free-correction arithmetic alone never passes.

Stop rule: Enumerate the finite existing level menu once. If even free quantum corrections leave a base cost above the tenfold classical budget, close that allocation and hand the base question to F11.

On pass: Compile only the winning correction-level interface and pass the full allocation to G3.

On failure: Keep the antithetic coupling and strongest classical allocation, close the tested hybrid schedule, and avoid another large variance pilot.

Fresh artifacts:

- `results/limitation_program_20261001/F10_<run>/level_inputs.json`
- `results/limitation_program_20261001/F10_<run>/hybrid_allocations.csv`
- `results/limitation_program_20261001/F10_<run>/decision.json`

## F11 - Reduce the base cost before spending on fine corrections

Status: **ready**. Priority: **3**. WHY source: 4 Failure 1. Inputs: G0, F02.

Existing evidence: [RESULTS.md](../../../docs/antithetic_feasibility/RESULTS.md), [hybrid_classical.py](../../../research/antithetic_feasibility/hybrid_classical.py), [bounded_classical.py](../../../research/antithetic_feasibility/bounded_classical.py).

Test one analytically priced coarse control and one conditioned level-zero residual on the existing A4 development case, retuning the full allocation.

1. Record the existing fixed-allocation 10.17/13.75-second base floor and its 1.35-fold free-correction ceiling as historical, allocation-specific evidence.
2. Measure training-inclusive residual/base cost and certify the added control expectation and bias.
3. Reoptimize the base and corrections with the same total error; allow reuse only if the actual workload declares repeated delivered prices.

Alternatives: Geometric or frozen-volatility coarse control; Conditional analytic coarse mean; A residual base with a proved expectation.

Acceptance checks:

- The proposed control preserves the same Heston law and contractual dates, with a valid control-mean proof.
- Complete base plus uncertainty is cheaper than the existing base, and below the candidate tenfold budget before a hybrid advantage attempt proceeds.
- Classical use of the same control is timed and included; single-price setup cannot be amortized across invented future requests.

Stop rule: Two coarse-base candidates only. If the base alone still exceeds the tenfold complete-classical budget, stop the associated hybrid branch before compiling fine paths.

On pass: Deliver the certified cheaper base to F10; recompute the full hybrid screen rather than preserving the previous 74% allocation.

On failure: Close the tested base controls and retain the existing base floor only for its stated allocation, not as a universal theorem.

Fresh artifacts:

- `results/limitation_program_20261001/F11_<run>/base_control_proofs.md`
- `results/limitation_program_20261001/F11_<run>/base_timings.csv`
- `results/limitation_program_20261001/F11_<run>/retuned_allocation.json`

## F12 - Separate positivity, coupling quality and Heston convergence proofs

Status: **ready**. Priority: **3**. WHY source: 4 Failure 1. Inputs: G0.

Existing evidence: [RESULTS.md](../../../docs/antithetic_feasibility/RESULTS.md), [hierarchy.py](../../../research/antithetic_feasibility/hierarchy.py), [classical.py](../../../research/antithetic_feasibility/classical.py), [validate.py](../../../research/antithetic_feasibility/validate.py).

Freeze S4 and compare the current coupling with one boundary-adapted CIR/variance transition at four existing refinement levels using matched random inputs.

1. Retain Feller ratio 0.64 and the measured beta near 1.24 as this case's observations.
2. Measure correction variance and per-path time while separately tracking weak bias against a refined or independently validated reference.
3. Write the boundary, coefficient-regularity and moment assumptions needed before quoting a beta=2 theorem.

Alternatives: Exact CIR variance transitions with a coupled equity approximation; A positivity-preserving boundary-adapted scheme; A transformed-variance coupling with separately controlled bias.

Acceptance checks:

- No model parameters, leverage or monitoring dates change; matching random inputs and law checks are documented.
- The candidate improves cost times correction variance by at least 20% on at least three of four frozen levels without violating its assigned bias budget.
- A measured beta improvement is labelled numerical; theorem use requires every boundary and moment hypothesis to be proved.

Stop rule: One alternative coupling and four levels with a frozen maximum sample budget. Stop if bias cannot be bounded or the cost/variance advantage is absent; positivity alone never passes.

On pass: Update the level-cost/variance interface for F10, and compile a transition only after a complete allocation screen improves.

On failure: Retain the valid negative S4 coupling result without asserting a universal lower bound on Heston MLMC rates.

Fresh artifacts:

- `results/limitation_program_20261001/F12_<run>/coupling_protocol.json`
- `results/limitation_program_20261001/F12_<run>/bias_variance_levels.csv`
- `results/limitation_program_20261001/F12_<run>/assumption_map.md`

## F13 - Audit non-Lipschitz antithetic theory at the square-root boundary

Status: **audit**. Priority: **3**. WHY source: 4 Failure 1. Inputs: G0.

Existing evidence: [FORMULATIONS_AND_CLASSICAL_COMPARATORS.md](../../../docs/limitation_audit_20261001/FORMULATIONS_AND_CLASSICAL_COMPARATORS.md), [classical.py](../../../research/antithetic_feasibility/classical.py).

Create an assumption-by-assumption transfer table for the nominated non-globally-Lipschitz theorem and the fixed S4 coefficients.

1. Check coefficient derivatives at v=0, one-sided monotonicity, inverse/positive moments and growth at infinity separately.
2. Test at most one justified variable transform, carrying its Ito correction, boundary behavior and inverse-map regularity.
3. Record the exact first failed premise and prohibit citing the theorem as an S4 repair while it remains unproved.

Alternatives: A boundary-specific theorem; A justified Lamperti-type transform with its own assumptions; An empirical coupling study under F12 without a theorem claim.

Acceptance checks:

- Every cited hypothesis has an explicit proof or a counterexample for the actual parameters.
- A transform preserves the original process and satisfies all transformed theorem premises, rather than just eliminating a square root in notation.
- No quantum or classical convergence exponent is upgraded because of a paper title or abstract.

Stop rule: One theorem map and one optional transform. A failed required hypothesis closes that direct transfer; it does not require new path simulation.

On pass: Supply the proven rate premise to F12/F10 and retain constants/error norm qualifications.

On failure: Close this theorem-transfer branch and identify precisely which boundary-specific result would be needed to reopen it.

Fresh artifacts:

- `results/limitation_program_20261001/F13_<run>/theorem_assumptions.md`
- `results/limitation_program_20261001/F13_<run>/transfer_decision.json`

## F14 - Screen exact Heston transitions at contractual dates

Status: **conditional**. Priority: **3**. WHY source: 4 Failure 1, 6. Inputs: G0.

Existing evidence: [RESULTS.md](../../../docs/antithetic_feasibility/RESULTS.md), [classical.py](../../../research/antithetic_feasibility/classical.py), [summary.json](../../../results/limitation_audit_20261001/heston_screen_v1/summary.json).

List and validate the one-asset A1 Broadie-Kaya or Poisson-conditioned transition primitives at the twelve contractual dates before writing a quantum transition.

1. Specify CIR endpoints, conditional integrated variance, inversion/series truncation and leverage-dependent stock increment, including error tolerances.
2. Implement one local classical transition reference and check conditional moments and prices against the existing refined method with a valid uncertainty interval.
3. Build a complete coherent primitive ledger, with inversion, special functions, precision, cleanup and all twelve dates charged.

Alternatives: Broadie-Kaya integrated-variance sampling; Poisson-conditioned exact simulation; A boundary-adapted approximate transition with a certified bias allowance.

Acceptance checks:

- The exact-transition law is preserved within a stated numerical sampling/error bound, including negative leverage.
- Complete transition cost at the assigned error is cheaper than the current refined construction; deleting internal steps alone is not evidence.
- A4 scale-up requires an exact joint covariance construction; independent variance processes cannot replace the repository correlation silently.

Stop rule: One A1 transition pilot and one primitive-cost ledger. If inversion/tail accuracy cannot be certified or the optimistic ledger does not improve the source, stop before circuit compilation.

On pass: Compile one clean A1 transition and send its law/cost interface to G1/G2; correlated A4 remains a separate F15 covariance task.

On failure: Close the nominated exact sampler for this cost target and keep a useful classical reference if valid.

Fresh artifacts:

- `results/limitation_program_20261001/F14_<run>/transition_spec.md`
- `results/limitation_program_20261001/F14_<run>/law_checks.json`
- `results/limitation_program_20261001/F14_<run>/primitive_costs.json`

## F15 - Repair the actual fast-forwarding assumptions before compilation

Status: **partial**. Priority: **3**. WHY source: 4 Failure 1, 6. Inputs: G0.

Branch decisions: direct published bound transfer: **closed**; A1 negative leverage tail extension: **conditional**; original A4 joint covariance extension: **conditional**; changed independent variance model: **different_task**.

Existing evidence: [experiment_heston_screen.py](../../../research/limitation_audit_20261001/experiment_heston_screen.py), [summary.json](../../../results/limitation_audit_20261001/heston_screen_v1/summary.json), [EXECUTION_RESULTS.md](../../../docs/limitation_audit_20261001/EXECUTION_RESULTS.md), [classical.py](../../../research/antithetic_feasibility/classical.py).

Attempt one A1 negative-leverage tail/truncation proof independent of the paper's failed sufficient condition; do not rerun the already completed direct-transfer screen.

1. Treat direct use of the full published bound as closed: A1 passes eta=8 and covariance but fails literal tail/truncation premises; A4 additionally has variance off-diagonal covariance 0.075 and cross-equity/variance terms 0.15.
2. Try the Heston affine-MGF Chernoff bound and, if necessary, one Holder/CIR exponential-moment bound. Verify the actual moment domain before deriving A1's stock/integrated-variance cutoffs for leverage -0.5 and all twelve contractual dates.
3. Only if A1 succeeds, enumerate a joint-law extension for the original A4 covariance; S4/B8 fail eta and remain outside direct transfer, and knock-out discontinuity requires its own payoff argument.

Alternatives: A new negative-leverage tail bound for A1; A different exact-transition route under F14; A clearly separate independent-variance basket model, labelled a new benchmark.

Acceptance checks:

- A1 receives a proved finite cutoff and total sampling/loading/truncation dollar error within its assigned G2 allowance.
- Time rescaling transforms all SDE coefficients and never erases the sign of the failed tail expression.
- Before any large circuit, all applicable model, payoff, precision and covariance assumptions are mapped, and a complete transition ledger improves the existing source by at least 20%.

Stop rule: At most the two named A1 bounding methods and one primitive screen. If neither yields an explicit usable tail bound, defer the fast-forward compiler; changing leverage, covariance or eta starts a separate task branch rather than fixing this one.

On pass: Compile only the certified A1 transition interface; escalate to A4 only after a law-preserving joint-covariance construction is proved.

On failure: Keep the completed negative compatibility result and record the exact missing tail/covariance lemma; no further large Heston circuit is authorized by this plan until new mathematical evidence exists.

Fresh artifacts:

- `results/limitation_program_20261001/F15_<run>/negative_leverage_tail_proof.md`
- `results/limitation_program_20261001/F15_<run>/cutoff_error_ledger.json`
- `results/limitation_program_20261001/F15_<run>/reopening_decision.json`

## F16 - Identify the exact failed factorization before changing a nested model

Status: **audit**. Priority: **4**. WHY source: 4 Failure 2, 5D. Inputs: G0.

Existing evidence: [RESULTS.md](../../../docs/compound_feasibility/RESULTS.md), [model.py](../../../research/compound_feasibility/model.py), [streaming.py](../../../research/compound_feasibility/streaming.py).

Document the current GBM future-factor reuse identity and annotate which assumptions a separately justified alternative model would break.

1. List the reusable future factors, sufficient outer state and conditional geometric control for the existing contract.
2. For at most one independently motivated candidate, enumerate its conditional-state dimension and test reusable regression/control approximations before claiming hard nesting.
3. Specify the additional coherent state update and conditional loading costs; a non-Markov label earns no cost credit.

Alternatives: State-dependent volatility with a separately declared contract; A higher-dimensional Markov state with an audited conditional solver; Retain GBM reuse and optimize its exact source.

Acceptance checks:

- The original factorization and its scope are accurately recorded.
- Any new model is a separate protocol, with matched classical factorization/regression/PDE/control candidates.
- The candidate has a real financial motivation and a complete cost screen; absence of Markov structure is never imposed as a universal requirement.

Stop rule: One existing-factorization audit and at most one candidate-model screen. If classical reuse still succeeds or coherent work grows faster, close that alternative without running a large nested estimator.

On pass: Hand a defined new-task conditional-state interface to F18/F19; do not alter the original verdict.

On failure: Keep the strong current GBM comparator and close the nominated changed-model branch.

Fresh artifacts:

- `results/limitation_program_20261001/F16_<run>/factorization_map.md`
- `results/limitation_program_20261001/F16_<run>/candidate_screen.json`

## F17 - Certify exercise-policy error near the continuation boundary

Status: **ready**. Priority: **3**. WHY source: 4 Failure 2. Inputs: G0.

Existing evidence: [RESULTS.md](../../../docs/compound_feasibility/RESULTS.md), [model.py](../../../research/compound_feasibility/model.py), [precision.py](../../../research/compound_feasibility/precision.py), [bounds.py](../../../research/controlled_residual_feasibility/bounds.py).

Construct continuation upper/lower bounds and a boundary-band error ledger for the existing development compound contract.

1. Separate the exact expectation inequalities from the observed 4e-8 to 6e-6-dollar sampled brackets.
2. Evaluate three frozen boundary widths and bound both the contribution inside the band and misclassification outside it, including unsampled tails.
3. Compare localized continuation work with the current uniform policy/Jensen calculation; specify reversible flags and a fixed or valid variable-cost quantum schedule only after the bound passes.

Alternatives: Analytic conditional geometric lower/upper controls; A certified continuation interval; Boundary-local residual estimation shared with classical pricing.

Acceptance checks:

- The total population policy error, not merely sampled mean gap, is bounded within its assigned G2 allowance.
- Outside-band decisions are certified by continuation intervals; inside-band and tail contributions are explicitly charged.
- A localized schedule reduces complete work by at least 20% before compilation and includes its boundary-detection and confidence cost.

Stop rule: Three preregistered band widths on existing development cases. If population certification is unavailable or total cost does not improve, close localization and retain the empirical bracket as an observation only.

On pass: Supply a certified policy-error/source interface to G2/G3 and update the matched classical method.

On failure: Do not credit the narrow sampled bracket as a population guarantee; keep the conservative current error bound.

Fresh artifacts:

- `results/limitation_program_20261001/F17_<run>/continuation_bounds.md`
- `results/limitation_program_20261001/F17_<run>/boundary_band_ledger.json`
- `results/limitation_program_20261001/F17_<run>/localization_screen.json`

## F18 - Match nested-estimation theorems to the actual contract and costs

Status: **audit**. Priority: **2**. WHY source: 4 Failure 2. Inputs: G0.

Existing evidence: [RESULTS.md](../../../docs/compound_feasibility/RESULTS.md), [multilevel.py](../../../research/compound_feasibility/multilevel.py), [quantum_schedule.py](../../../research/compound_feasibility/quantum_schedule.py).

Audit outer Lipschitz constants, terminal moments, nesting depth, conditional access costs and error norms for the current compound contract.

1. Check the exact outer function and whether any exercise discontinuity is inside the theorem's scope.
2. Separate asymptotic unit-cost oracle statements from actual conditional-source timings and circuit costs.
3. Translate the supplied RMSE or moment guarantee to an explicit common 99% dollar guarantee, or mark that conversion absent.

Alternatives: Nested MLMC; Randomized multilevel conditional estimation; Regression/factorized conditional evaluation; Deterministic-level quantum nesting under its actual assumptions.

Acceptance checks:

- Every quoted complexity exponent has an assumption map and the correct error norm.
- The cost ledger charges actual function/conditional-sampling work and setup rather than unit-cost theorem oracles.
- The paired comparison includes the current factor-reuse/control classical method and a valid joint 99% schedule.

Stop rule: One current-contract theorem map; repeat only for a formally distinct candidate protocol. Missing premises close theorem transfer without requiring expensive quantum simulation.

On pass: Provide valid assumptions and cost interfaces to F19/G3/G4.

On failure: Retain applicable weaker bounds and measurements; reject unsupported universal epsilon^-2 or epsilon^-1 claims for arbitrary nesting.

Fresh artifacts:

- `results/limitation_program_20261001/F18_<run>/nested_assumptions.md`
- `results/limitation_program_20261001/F18_<run>/error_norm_conversion.json`
- `results/limitation_program_20261001/F18_<run>/actual_cost_ledger.json`

## F19 - Expand one deterministic nested schedule instead of hiding depth constants

Status: **conditional**. Priority: **3**. WHY source: 4 Failure 2. Inputs: G0, F18.

Existing evidence: [quantum_schedule.py](../../../research/compound_feasibility/quantum_schedule.py), [RESULTS.md](../../../docs/compound_feasibility/RESULTS.md), [FORMULATIONS_AND_CLASSICAL_COMPARATORS.md](../../../docs/limitation_audit_20261001/FORMULATIONS_AND_CLASSICAL_COMPARATORS.md).

Write one explicit fixed-D=2 deterministic-level schedule with all error, failure and source/inverse counts, using the already nominated contract.

1. Keep D fixed; expand every level and repetition in the epsilon^-1 log^(3D+1) expression instead of treating it as a unit constant.
2. Count conditional loader, arithmetic, inverse, control and readout calls, then validate the schedule on a tiny classical distribution.
3. Compare the total against the existing nested schedule and best classical conditional method at the same dollar error.

Alternatives: Deterministic level scheduling; A flat certified residual estimator when algebra permits; The strongest classical nested or factorized schedule.

Acceptance checks:

- An explicit call-count table and per-level joint failure allocation sum to at most 0.01.
- The tiny validation matches the target expectation and the schedule's stated error/confidence contract; it does not substitute for a theorem proof.
- Complete calls reduce the old quantum schedule by at least 20%, and a labelled optimistic total-time ledger is no greater than the fastest eligible measured classical time before large compilation.

Stop rule: One fixed-depth schedule and two frozen error targets. Stop if hidden logarithmic/confidence constants leave the complete schedule above the comparator screen; do not increase depth to seek a larger exponent gap.

On pass: Hand the deterministic schedule interface to G3 and compile only the required primitive source.

On failure: Close the tested nested schedule and retain the correct fixed-depth asymptotic qualification.

Fresh artifacts:

- `results/limitation_program_20261001/F19_<run>/expanded_schedule.json`
- `results/limitation_program_20261001/F19_<run>/tiny_validation.json`
- `results/limitation_program_20261001/F19_<run>/matched_cost.json`

## F20 - Evaluate controls by residual size times full oracle cost

Status: **partial**. Priority: **2**. WHY source: 4 Failure 3, 5D. Inputs: G0, F02.

Existing evidence: [RESULTS.md](../../../docs/controlled_residual_feasibility/RESULTS.md), [parity.py](../../../research/controlled_residual_feasibility/parity.py), [cost.py](../../../research/controlled_residual_feasibility/cost.py), [CONSTANT_MULTIPLIER_RESULT.md](../../../docs/limitation_audit_20261001/CONSTANT_MULTIPLIER_RESULT.md).

Attach full source cost to one existing parity-control residual and one bounded-measure-change ledger, using the latest exact arithmetic costs.

1. Retain the proved iid accounting relation relative_gain=a*b_C/b_Q; shared controls are not intrinsically disqualifying.
2. Measure control fitting, evaluation and moment-certification work; compile or fully specify both residual sources and their inverse/cleanup cost.
3. For RQMC use measured independent-scramble error rather than the iid variance formula, and optimize each architecture independently.

Alternatives: Parity residual plus cheaper coherent arithmetic; A numeraire/size-biased representation; An analytic control with separately certified mean.

Acceptance checks:

- Every residual benefit is paired with full b_Q and b_C costs, including fitting and certification.
- A candidate's complete quantum cost falls by at least 20% at the same G2/G3 contract before new full-source compilation.
- Only G5's matched complete-time inequality establishes advantage; variance reduction or quantum-exclusive availability is not a standalone requirement.

Stop rule: Screen the two named rewrites once using current costs. If neither source-plus-estimator total improves, close those rewrites; rerun only after a documented new cost or bound changes the decision.

On pass: Compile the winning residual source, update G4 with the same control, and deliver a complete schedule interface to G3.

On failure: Keep useful classical controls and exact identities; do not repeat a variance-only pilot or assert that algebra can never reduce coherent cost.

Fresh artifacts:

- `results/limitation_program_20261001/F20_<run>/control_cost_ledger.json`
- `results/limitation_program_20261001/F20_<run>/paired_ratio_screen.json`

## F21 - Treat rough-volatility precision rates as measured contract-specific results

Status: **conditional**. Priority: **5**. WHY source: 6. Inputs: G0.

Existing evidence: [FORMULATIONS_AND_CLASSICAL_COMPARATORS.md](../../../docs/limitation_audit_20261001/FORMULATIONS_AND_CLASSICAL_COMPARATORS.md).

Create a separate rough-model protocol only if independently motivated, specifying the model, payoff and four separate approximation errors.

1. Distinguish rough Bergomi from rough Heston and keep the current GBM/Heston contract unchanged.
2. Separate kernel, time-grid, quadrature and floating-point errors; benchmark bridge, smoothing and RQMC candidates at a frozen parameter point.
3. Acquire at most four refinement/sample levels with independent replicates and report total cost/error uncertainty rather than assigning a universal 1.3-1.6 exponent.

Alternatives: Brownian-bridge RQMC with payoff-specific smoothing; Sparse-grid integration or extrapolation; A Markovian lift under F22.

Acceptance checks:

- The branch has a distinct contract and error allocation; published European rates are not imported to a path barrier.
- Measured total time-to-error includes all four approximation errors and setup with a common 99% output guarantee.
- Only a complete paired source-cost screen, rather than a difficult classical exponent, earns quantum implementation work.

Stop rule: One justified model/parameter point and four frozen levels. Without a valid bias reference or financial motivation, defer before circuit compilation.

On pass: Deliver a separate-task comparator and error interface to F22/G2/G4; do not relabel it as a fix of the original benchmark.

On failure: Close the nominated rough-contract pilot or defer it; retain no universal precision exponent.

Fresh artifacts:

- `results/limitation_program_20261001/F21_<run>/rough_contract.json`
- `results/limitation_program_20261001/F21_<run>/four_error_ledger.json`
- `results/limitation_program_20261001/F21_<run>/cost_error_curve.csv`

## F22 - Charge factor rank and bias in a Markovian rough-process lift

Status: **conditional**. Priority: **5**. WHY source: 4 Failure 2, 6. Inputs: G0, F21.

Existing evidence: [FORMULATIONS_AND_CLASSICAL_COMPARATORS.md](../../../docs/limitation_audit_20261001/FORMULATIONS_AND_CLASSICAL_COMPARATORS.md).

For the single justified rough-model branch, compare ranks 2, 4, 8 and 16 while independently refining the time step.

1. State the kernel approximation and payoff-specific weak-error assumptions; a European theorem is not automatically a barrier guarantee.
2. Separate lift-rank bias from time discretization using a valid reference/error bound, and record factor-update time and memory.
3. Construct a reversible one-factor update ledger only for the smallest rank satisfying the declared bias budget, allowing the same lift classically.

Alternatives: Sum-of-exponentials lift; A quadrature-derived positive factor lift; Direct convolution simulation with fast classical methods.

Acceptance checks:

- The lift approximates the nominated model within its assigned G2 allowance, including payoff-specific assumptions.
- The selected rank lowers complete path time/memory cost relative to the direct method at equal error.
- A quantum screen charges every factor and update, with an optimized classical lift as comparator.

Stop rule: Four ranks and two frozen time steps. If no rank passes the bias budget or the lifted total does not improve, close this lift/rank target without compiling all factors.

On pass: Deliver a rank/error/update interface to G1/G2 and reassess the complete paired schedule.

On failure: Close the nominated approximation; failure does not rule out all rough-process approximations.

Fresh artifacts:

- `results/limitation_program_20261001/F22_<run>/lift_spec.json`
- `results/limitation_program_20261001/F22_<run>/rank_time_bias.csv`
- `results/limitation_program_20261001/F22_<run>/update_cost.json`

## F23 - Certify dimension compression on both architectures

Status: **ready**. Priority: **3**. WHY source: 6. Inputs: G0.

Existing evidence: [basis.py](../../../research/frontier_classical_20261001/basis.py), [barrier_fast_classical.py](../../../research/advantage_frontier_20260923/barrier_fast_classical.py), [CONSTANT_MULTIPLIER_RESULT.md](../../../docs/limitation_audit_20261001/CONSTANT_MULTIPLIER_RESULT.md).

Compute covariance-mode residuals for the existing B4x12 and B8x52 laws and derive a payoff-appropriate dollar error bound for omitted modes.

1. Try three frozen covariance ranks while retaining every contractual monitoring date.
2. For calls derive a Lipschitz/coupling bound; for barriers additionally bound probability mass near monitoring thresholds rather than applying the call bound blindly.
3. Time the same compressed law classically and build a charged quantum Gaussian/path/schedule ledger only for a rank satisfying the error budget.

Alternatives: Exact factor sparsity if present; Certified low-rank covariance approximation; Temporal transforms retaining all contractual observations.

Acceptance checks:

- The omitted-mode price error is bounded within its assigned G2 allowance; both architectures use the same certified law.
- No contractual dates are deleted and any model approximation is declared rather than silently substituted.
- The full quantum/classical ratio improves on the uncompressed baseline before large compilation; fewer qubits alone is not the criterion.

Stop rule: Three ranks on the two existing development sizes. If the barrier boundary bound is unavailable or no rank passes, keep full rank and close compression for this tolerance.

On pass: Supply the shared rank/law/error interface to G1/G2/G4 and compile only the accepted rank.

On failure: Retain exact PCA reordering without covariance truncation; do not extrapolate arbitrary-dimension scaling from two cases.

Fresh artifacts:

- `results/limitation_program_20261001/F23_<run>/covariance_spectra.json`
- `results/limitation_program_20261001/F23_<run>/payoff_error_bound.md`
- `results/limitation_program_20261001/F23_<run>/paired_rank_screen.json`

## F24 - Specify the exact Asian/barrier PDE before costing a quantum solve

Status: **conditional**. Priority: **4**. WHY source: 6. Inputs: G0.

Existing evidence: [FORMULATIONS_AND_CLASSICAL_COMPARATORS.md](../../../docs/limitation_audit_20261001/FORMULATIONS_AND_CLASSICAL_COMPARATORS.md), [barrier_fast_classical.py](../../../research/advantage_frontier_20260923/barrier_fast_classical.py).

Formulate a one-asset development Asian/barrier backward PDE with average-state augmentation and updates at the actual discrete monitoring dates.

1. Write boundary/terminal data and explain how discrete average and knock-out events update the augmented state.
2. On two small grids compute sparsity, stability, condition estimates, payoff preparation and extraction normalization; validate the classical finite-difference reference with a bias bound.
3. Screen a complete quantum matrix-access/solve/point-price extraction ledger against both the small-grid solver and strongest simulation comparator.

Alternatives: Backward finite-difference PDE with state augmentation; Sparse/low-rank classical PDE or tensor solvers; Retain path simulation when augmented dimension dominates.

Acceptance checks:

- The PDE encodes the same payoff, law and discrete dates rather than continuous monitoring or a European substitute.
- Grid/time truncation and scalar-price extraction errors fit assigned G2 allowances.
- A labelled optimistic complete quantum time is no greater than the fastest eligible measured classical time before a large PDE circuit; a state of grid values alone does not count as a delivered price.

Stop rule: One exact small-contract formulation and two grid sizes. If state augmentation, conditioning or scalar extraction already defeats the optimistic screen, close this PDE route before high-dimensional compilation.

On pass: Implement one small coherent matrix/observable interface and hand its costs to G1/G2/G3.

On failure: Retain the useful PDE reference and record the dominating ledger term; do not compare solely with an untuned grid method.

Fresh artifacts:

- `results/limitation_program_20261001/F24_<run>/augmented_pde.md`
- `results/limitation_program_20261001/F24_<run>/grid_conditioning.csv`
- `results/limitation_program_20261001/F24_<run>/scalar_extraction_ledger.json`

## F25 - Propagate overlap readout error into dollars and repeated evolution cost

Status: **conditional**. Priority: **4**. WHY source: 1, 6. Inputs: G0.

Existing evidence: [FORMULATIONS_AND_CLASSICAL_COMPARATORS.md](../../../docs/limitation_audit_20261001/FORMULATIONS_AND_CLASSICAL_COMPARATORS.md).

For one nominated forward-PDE formulation, write the normalization/overlap price formula and derive a stable absolute-dollar error bound before evolving a quantum state.

1. Bound relevant denominators and norms away from unstable values; prove any claimed short-factor payoff representation.
2. Allocate overlap and state-evolution errors, then compute swap-test copies at 99% confidence, charging complete state preparation/evolution for each copy.
3. Screen overlap estimation and an explicitly specified amplitude-estimation alternative against direct classical density/payoff integration.

Alternatives: Swap-test readout with its epsilon^-2 copies; Coherent overlap amplitude estimation with additional reflection cost; Direct observable loading if its normalization is certified.

Acceptance checks:

- The overlap/ratio formula has a valid dollar-error propagation bound for the actual payoff.
- The copy count includes every repeated input-state preparation, evolution and confidence repetition.
- Both the forward state and payoff representation preserve the nominated contract; labelled optimistic total quantum time is no greater than the fastest eligible measured classical time before implementation.

Stop rule: One stable-normalization audit and two readout ledgers. Stop if no denominator bound exists or even the optimistic repeated-evolution total exceeds the eligible classical screen.

On pass: Build only the small stable observable interface and pass its normalization/call-count ledger to G2/G3.

On failure: Close the nominated readout route while preserving the forward-PDE mathematical construction; a cheap swap gate is not a pricing cost reduction.

Fresh artifacts:

- `results/limitation_program_20261001/F25_<run>/overlap_error_proof.md`
- `results/limitation_program_20261001/F25_<run>/repeated_state_cost.json`

## F26 - Audit one SPDE/BDSDE update only for an independently justified model

Status: **conditional**. Priority: **5**. WHY source: 6. Inputs: G0.

Existing evidence: [FORMULATIONS_AND_CLASSICAL_COMPARATORS.md](../../../docs/limitation_audit_20261001/FORMULATIONS_AND_CLASSICAL_COMPARATORS.md).

Define a separate financially justified SPDE contract and enumerate one forward/backward update's arithmetic, encoding and strong-error assumptions.

1. Declare new noise/model/output features and keep the original Heston/GBM task intact.
2. Audit encoding, conditional access, regularity, moments and representation/discretization bias for the nominated update.
3. Cost a complete multilevel allocation using real reversible update operations and matched classical PDE/BDSDE/MLMC methods.

Alternatives: Classical BDSDE/MLMC; A simpler direct Heston transition under F14/F15; An independently justified stochastic environment with its own protocol.

Acceptance checks:

- The new model has an external financial justification beyond making classical pricing harder.
- All efficient-encoding and strong-error hypotheses are explicit and charged; square-root query improvement alone does not pass.
- The labelled optimistic complete update/allocation time is no greater than the fastest eligible measured classical time before substantial circuit compilation.

Stop rule: One update audit and one allocation screen. If justification or an access premise is absent, defer; direct existing-model improvements retain priority.

On pass: Create a separately labelled experimental interface and pass it to G1/G2/G3/G4.

On failure: Close or defer this changed-model branch without changing the original advantage verdict.

Fresh artifacts:

- `results/limitation_program_20261001/F26_<run>/spde_contract.json`
- `results/limitation_program_20261001/F26_<run>/update_assumptions.md`
- `results/limitation_program_20261001/F26_<run>/allocation_screen.json`

## F27 - Choose the exact multi-output error norm before pricing its penalty

Status: **audit**. Priority: **4**. WHY source: 6. Inputs: G0.

Existing evidence: [FORMULATIONS_AND_CLASSICAL_COMPARATORS.md](../../../docs/limitation_audit_20261001/FORMULATIONS_AND_CLASSICAL_COMPARATORS.md), [model.py](../../../research/compound_feasibility/model.py).

Write a separate output contract for K prices, one portfolio total or a vector norm, and map it to the nominated multivariate estimator access model.

1. Keep one classical price as the default original task; additional outputs are declared new branches.
2. Specify componentwise versus aggregate error and per-output versus simultaneous 99% confidence, with covariance and normalization.
3. Count shared source/payoff work, binary-value or phase access, readout and valid confidence amplification; allow equivalent classical path reuse.

Alternatives: Independent prices with a union-bounded failure budget; Covariance-sensitive vector estimation; One aggregate observable under F29.

Acceptance checks:

- The output norm and joint failure requirement match on both architectures.
- The estimator's access and precision regimes are checked; sqrt(K) is not inserted as a universal rule.
- The complete ledger includes all delivered classical outputs and shared setup, without comparing vector RMSE to separate 99% prices.

Stop rule: One nominated output contract and one theorem/access audit. If outputs are unspecified, defer the branch and continue the original single-price implementation.

On pass: Deliver a distinct multi-output interface to G3/G4 and screen total cost.

On failure: Close the unsupported penalty or estimator claim; retain the original one-price contract.

Fresh artifacts:

- `results/limitation_program_20261001/F27_<run>/output_contract.json`
- `results/limitation_program_20261001/F27_<run>/access_norm_ledger.json`

## F28 - Match a valid barrier Greek against a classical adjoint or smoothed estimator

Status: **conditional**. Priority: **5**. WHY source: 6. Inputs: G0, F27.

Existing evidence: [barrier_fast_classical.py](../../../research/advantage_frontier_20260923/barrier_fast_classical.py), [FORMULATIONS_AND_CLASSICAL_COMPARATORS.md](../../../docs/limitation_audit_20261001/FORMULATIONS_AND_CLASSICAL_COMPARATORS.md).

Specify one first-order barrier sensitivity as a separate output task and derive a valid conditional-smoothed classical derivative estimator.

1. Check whether differentiation crosses exercise/barrier discontinuities and derive the missing boundary or likelihood-ratio terms.
2. Validate the estimator on a small case against refined finite differences or analytic reference while separately bounding derivative bias.
3. Compare valid adjoint/shared-path and smoothing methods with a fully specified quantum gradient source, precision and readout ledger.

Alternatives: Conditional smoothing plus pathwise/adjoint differentiation; Likelihood-ratio or Malliavin estimator; Quantum gradient estimation with a certified smooth oracle.

Acceptance checks:

- The derivative target, absolute units and 99% error guarantee are explicitly declared.
- The classical comparator handles discontinuities correctly and includes any available shared adjoint work.
- Quantum finite-difference/gradient precision, oracle calls and synthesis errors are charged; K independent classical repricings are not used when a valid adjoint exists.

Stop rule: One first-order Greek, one small validation and two eligible classical derivative methods. If derivative bias or oracle smoothness remains uncertified, defer quantum compilation; second-order Greeks require a new analysis.

On pass: Create a separately labelled Greek benchmark and pass a valid smooth/conditional source interface to G1/G2/G3/G4.

On failure: Close the nominated Greek representation without claiming a result for the original one-price task.

Fresh artifacts:

- `results/limitation_program_20261001/F28_<run>/greek_contract.json`
- `results/limitation_program_20261001/F28_<run>/derivative_proof.md`
- `results/limitation_program_20261001/F28_<run>/adjoint_quantum_screen.json`

## F29 - Treat an aggregate portfolio as one declared observable

Status: **conditional**. Priority: **4**. WHY source: 1, 6. Inputs: G0, F27.

Existing evidence: [FORMULATIONS_AND_CLASSICAL_COMPARATORS.md](../../../docs/limitation_audit_20261001/FORMULATIONS_AND_CLASSICAL_COMPARATORS.md), [model.py](../../../research/compound_feasibility/model.py).

Freeze one small signed portfolio and derive its aggregate payoff and normalization before choosing either estimator.

1. Specify whether only the total or every constituent price is delivered; preserve the separate original single-contract benchmark.
2. Derive aggregate moments/range and charge payoff sharing, netting and any extra comparator/control work.
3. Measure classical shared-path evaluation and screen one coherent aggregate source; amortize setup only over the actual declared delivered-request count.

Alternatives: One aggregate linear observable; Shared-path individual outputs with a joint error budget; A reusable representation for a genuinely declared request batch.

Acceptance checks:

- Aggregate and constituent-output contracts are never interchanged.
- Normalization, cancellation and moment/error bounds are valid for signed weights and the exact payoff.
- Training/setup and all outputs are charged equally; the complete paired ratio improves before large compilation.

Stop rule: One fixed portfolio and one declared reuse count. If netting helps the classical comparator equally or source overhead dominates, close the quantum portfolio screen.

On pass: Deliver a separate aggregate-source/error interface to G1/G2/G3/G4.

On failure: Keep any useful classical payoff sharing and close the tested aggregate quantum schedule; it does not alter the original benchmark verdict.

Fresh artifacts:

- `results/limitation_program_20261001/F29_<run>/portfolio_contract.json`
- `results/limitation_program_20261001/F29_<run>/aggregate_bound.md`
- `results/limitation_program_20261001/F29_<run>/reuse_screen.json`

## F30 - Compare tensor compression with direct classical contraction

Status: **conditional**. Priority: **4**. WHY source: 5D, 6. Inputs: G0.

Existing evidence: [FORMULATIONS_AND_CLASSICAL_COMPARATORS.md](../../../docs/limitation_audit_20261001/FORMULATIONS_AND_CLASSICAL_COMPARATORS.md), [kernels.py](../../../research/frontier_classical_20261001/kernels.py).

Fit tensor-train ranks 2, 4 and 8 to one small existing development integrand with frozen training data and separate validation data.

1. Charge every training evaluation and separate pointwise fit diagnostics from an integral or price-error certificate.
2. Measure direct classical contraction and its error; bound the approximation contribution to the original price.
3. Specify coherent loading plus estimation for the same tensor, including all rotation/normalization costs, then compare with direct contraction.

Alternatives: Tensor-train direct integration; Low-rank payoff or distribution loader; Sparse-grid or interpolant residuals under F04.

Acceptance checks:

- Tensor approximation error is bounded within the assigned G2 dollar allowance; random test-point accuracy alone does not pass.
- Rank/training growth is recorded as dimensions change, without claiming a universal barrier-rank bound.
- Quantum loading-plus-estimation beats its uncompressed quantum baseline by at least 20% and survives direct classical contraction before compilation.

Stop rule: Three frozen ranks on one small case. If certification is absent or direct contraction dominates, close quantum loading for this representation and retain the classical benefit.

On pass: Build one small clean loader interface and hand the tensor/error/cost record to G1/G2/G3/G4.

On failure: Close the quantum tensor route for this rank target; do not count a classical-trained compact representation as free quantum state preparation.

Fresh artifacts:

- `results/limitation_program_20261001/F30_<run>/tensor_training.json`
- `results/limitation_program_20261001/F30_<run>/integral_error_certificate.md`
- `results/limitation_program_20261001/F30_<run>/contraction_loading_screen.json`

## F31 - Replace exponent requirements with the matched complete-time inequality

Status: **audit**. Priority: **1**. WHY source: 1, 2.4, 4 Failure 2, 5D, 7, 8. Inputs: G0.

Existing evidence: [WHY_NO_ADVANTAGE.md](../../../manuscript/advantage-frontier-2026-09-23/WHY_NO_ADVANTAGE.md), [CONSTANT_MULTIPLIER_RESULT.md](../../../docs/limitation_audit_20261001/CONSTANT_MULTIPLIER_RESULT.md), [FORMULATIONS_AND_CLASSICAL_COMPARATORS.md](../../../docs/limitation_audit_20261001/FORMULATIONS_AND_CLASSICAL_COMPARATORS.md).

Encode one frontier ledger that accepts actual setup, certified estimator calls, source/inverse/readout and matched classical timing inputs without requiring p_C>=3.

1. Keep the section-7 rows as historical sensitivity conditions, not universal necessities.
2. Support measured, certified-bound and assumed inputs as distinct evidence types; missing input means unresolved, never zero.
3. Use current component interfaces as they arrive and evaluate complete T_Q<=T_C/10 only after G2/G3/G4/G5 are satisfied for that candidate.

Alternatives: Equal-exponent finite-constant crossover; Paired structured-integration exponents; Extra mixing/moment parameters with a separately justified access model.

Acceptance checks:

- No candidate is rejected solely for p_C<3 or accepted solely for p_C>=3.
- Setup, arithmetic, cleanup, confidence, readout and physical overhead are present in the ledger, and measured classical timing includes matched setup.
- The final candidate passes the G5 tenfold inequality using its declared physical assumptions and conservative evidence bounds; a source-depth gain remains an L4 result until then.

Stop rule: Build and validate the ledger once using known pass/fail synthetic accounting cases and the current negative operating point. Rerun only when a changed interface could change the decision.

On pass: Provide the reusable decision interface for every route; a full G5 pass is conditional L2 unless an end-to-end hardware execution establishes L1.

On failure: Record the dominating missing/budget term and close the tested operating point, while retaining successful exact component changes.

Fresh artifacts:

- `results/limitation_program_20261001/F31_<run>/frontier_schema.json`
- `results/limitation_program_20261001/F31_<run>/accounting_checks.json`
- `results/limitation_program_20261001/F31_<run>/candidate_decisions.json`

## F32 - Use quantum walks only when the financial input has a real mixing bottleneck

Status: **conditional**. Priority: **5**. WHY source: 5A. Inputs: G0.

Existing evidence: [FORMULATIONS_AND_CLASSICAL_COMPARATORS.md](../../../docs/limitation_audit_20261001/FORMULATIONS_AND_CLASSICAL_COMPARATORS.md), [barrier_fast_classical.py](../../../research/advantage_frontier_20260923/barrier_fast_classical.py).

Record that direct GBM Gaussian sampling has no MCMC bottleneck; nominate a walk branch only for an independently justified input distribution lacking a competitive direct sampler.

1. Declare any posterior calibration or constrained input as a new workload and time direct, rejection, importance and classical chain alternatives.
2. Specify reversibility, stationary distribution, warm-start overlap and a credible gap/mixing bound; observable autocorrelation measurements are not a spectral-gap proof.
3. Charge coherent transition, reflection, preparation schedule, estimation and readout before seeking a quadratic mixing gain.

Alternatives: Direct Gaussian/structured sampling; Classical importance or rejection sampling; Quantum walk for a genuine reversible-chain distribution.

Acceptance checks:

- The pricing workload actually includes the difficult distribution; an artificial chain is not introduced to manufacture an advantage.
- Required reversibility, overlap and gap/access assumptions are proved or explicitly conditional, and observable uncertainty is correctly certified.
- A complete walk-preparation-plus-estimation cost screen beats the best eligible classical sampler before circuit implementation.

Stop rule: One nominated justified distribution and one sampler/access audit. If a competitive direct sampler exists or the premises are unsupported, close the walk branch; current GBM needs no new experiment here.

On pass: Create a separately labelled distribution-access benchmark and hand a transition/overlap/error interface to G1/G2/G3/G4.

On failure: Close or defer the quantum-walk route and retain direct sampling for the original contract.

Fresh artifacts:

- `results/limitation_program_20261001/F32_<run>/distribution_contract.json`
- `results/limitation_program_20261001/F32_<run>/sampler_access_audit.md`
- `results/limitation_program_20261001/F32_<run>/mixing_cost_screen.json`

