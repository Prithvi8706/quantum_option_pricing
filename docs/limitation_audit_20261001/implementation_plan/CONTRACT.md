# Evidence and price contract implementation plan

These are planned local actions. Dependencies identify required input interfaces; a related investigation need not be fully solved to supply one. Existing evidence is preserved, and failed finite screens close only the tested branch.

## C01 One classical price is the current output

**Status:** ready. **Priority:** 1. **Inputs:** existing repository task definitions.

**Original point:** 1 output; 5 root cause F. **Next action:** Freeze a task contract for each original source family, specifying one classical discounted price and all financial inputs.

1. Resolve B4/B8 knock-out separately from C4/H8 residual and Heston/compound cases.
2. Copy original parameters and hash references.
3. Specify what a delivered numerical price must satisfy.

**Alternatives:** Scalar amplitude/observable interface; Separately labelled portfolio or state-output experiments.

**Accept only when:**

- Contract fixes payoff, model, dates, asset covariance, notional, tolerance and 99% per-price confidence.
- Every proposed algorithm returns the same scalar; variants never replace its benchmark.

**Stop or change approach:** No tuning until the task file is saved; unknown archived parameters are recovered from code/results rather than guessed.

**If accepted:** Close the task portion of G0 and start the frozen baseline inventory. **If rejected:** Mark unrecoverable fields as missing evidence and use another fully specified original case.

**Existing evidence:** `docs/limitation_audit_20261001/CONTRACT_AND_EVIDENCE.md`.

**New receipt:** `results/limitation_program_20261001/C01_<run>/`.

## C02 Dollar accuracy cannot be silently weakened

**Status:** ready. **Priority:** 1. **Inputs:** C01.

**Original point:** 1 accuracy; 7 extreme precision. **Next action:** Express all candidate error bounds in discounted dollars at the existing notional.

1. Identify price scale and discount.
2. Translate each approximation and estimator error.
3. Check units in every budget formula.

**Alternatives:** Absolute-error normalization; Relative/norm-error conversion with proved scale bounds.

**Accept only when:**

- Retain the original epsilon grid, including $0.001 only in its declared cases.
- Amplitude, payoff range and discount factors are explicitly converted; no unannounced relaxation.

**Stop or change approach:** One dimensional/unit audit per source family; unsupported conversions make the candidate ineligible.

**If accepted:** Supply dollar bounds to C03/C05. **If rejected:** Fix normalization or close that candidate interface; keep stricter tolerances as sensitivities only.

**Existing evidence:** `docs/limitation_audit_20261001/CONTRACT_AND_EVIDENCE.md`.

**New receipt:** `results/limitation_program_20261001/C02_<run>/`.

## C03 The complete price needs the complete confidence allowance

**Status:** ready. **Priority:** 1. **Inputs:** C01, C02.

**Original point:** 1 confidence; 5 root cause F. **Next action:** Create the common deterministic-error and probabilistic-failure ledger with an explicit allocation policy.

1. Enumerate law, discretization, arithmetic, synthesis and estimation errors. For compound/residual families include the same-policy baseline, surrogate and nonnegative exercise-policy regret terms; these are not obligations for a plain knock-out price.
2. Separate deterministic bias from failure probability.
3. Version allocations before outcome-sensitive experiments.

**Alternatives:** Original 0.45 epsilon statistical share; Cost-optimized shares after valid bounds exist.

**Accept only when:**

- The sum of certified dollar errors is at most epsilon; total allocated failure is at most 0.01.
- Every term is a bound, an assumption or unknown, with no zero-filled missing certificate.
- Hardware, moment pilots, reference checks and sequential stopping have distinct failure entries.

**Stop or change approach:** One complete ledger skeleton; unresolved terms keep G2/G3/G5 open rather than delaying unchanged integer experiments.

**If accepted:** Use the ledger to qualify changed precision/loaders and all full-runtime claims. **If rejected:** Retain exact finite-source results and investigate the largest unbounded term first.

**Existing evidence:** `docs/limitation_audit_20261001/CONTRACT_AND_EVIDENCE.md`.

**New receipt:** `results/limitation_program_20261001/C03_<run>/`.

## C04 Tenfold advantage is a chosen threshold

**Status:** audit. **Priority:** 2. **Inputs:** C01, H17.

**Original point:** 1 tenfold target; 2.2; 7. **Next action:** Regenerate onefold and tenfold ratios with separate source-only and complete-runtime fields.

1. Read actual before/after source costs.
2. Separate modelled and timed inputs.
3. Export onefold, tenfold and source-only fields.

**Alternatives:** Observed T_C/T_Q; Break-even and tenfold frontiers.

**Accept only when:**

- Verify tenfold budget miss equals 10*T_Q/T_C using identical timing conventions.
- A miss of the 10x target is not labelled a quantum slowdown unless T_Q exceeds T_C.

**Stop or change approach:** One unit/identity check over every emitted comparison row; unsupported complete times remain blank.

**If accepted:** Use ratios consistently in C14 and G5. **If rejected:** Correct interpretation and regenerate local tables without altering old evidence.

**Existing evidence:** `docs/limitation_audit_20261001/CONTRACT_AND_EVIDENCE.md`.

**New receipt:** `results/limitation_program_20261001/C04_<run>/`.

## C05 The statistical allowance of 0.45 epsilon is adjustable

**Status:** ready. **Priority:** 3. **Inputs:** C03, E24.

**Original point:** 2.1 statistical allowance. **Next action:** Optimize a small preregistered error-allocation grid after each component has a valid dollar bound.

1. Enumerate costs as functions of tolerance.
2. Round actual stage counts.
3. Price source changes, pilots and repeats together.

**Alternatives:** Original split; Two alternative feasible statistical/bias splits.

**Accept only when:**

- Each row satisfies epsilon and failure constraints with integer estimator rounds.
- Any selected cheaper source preserves the financial certificate and the same confidence.

**Stop or change approach:** Three feasible allocations for one case; if a source bound is missing, retain the original split and defer optimization.

**If accepted:** Adopt the minimum complete certified cost, then reevaluate C13/G5. **If rejected:** Keep the cheaper valid baseline rather than optimizing on unproved error estimates.

**Existing evidence:** `docs/limitation_audit_20261001/CONTRACT_AND_EVIDENCE.md`.

**New receipt:** `results/limitation_program_20261001/C05_<run>/`.

## C06 Correct digital arithmetic is not a continuous financial-law certificate

**Status:** conditional. **Priority:** 1. **Inputs:** C03.

**Original point:** 4 Failure 6 correctness; 7 certification. **Next action:** Prove one-coordinate Gaussian-to-digital-law bias before composing a full-path price certificate.

1. Write the exact finite sampler distribution.
2. Bound its discrepancy from the declared continuous law.
3. Propagate through a bounded truncated path and include remaining tails.

**Alternatives:** Coupling with payoff regularity; Explicit finite-grid/distribution discrepancy plus tail bounds.

**Accept only when:**

- Tail cutoff, finite-grid law, function approximation and payoff effects are bounded separately.
- Compose over all required normals; gate truth tables or random draws are not substituted for financial bias.

**Stop or change approach:** One coordinate plus one monitoring date first; a failed composition leaves the loader branch conditional and prompts a different bound.

**If accepted:** Close G2 for the chosen source: add C07 for barrier payoffs and E11 only if a variance-sensitive estimator needs the tight digital-moment bridge. **If rejected:** Preserve current precision/law; compare a refined grid or a tighter coupling before adopting a new loader.

**Existing evidence:** `docs/limitation_audit_20261001/CONTRACT_AND_EVIDENCE.md`; `manuscript/advantage-frontier-2026-09-23/STAGE_A_RESULTS.md`.

**New receipt:** `results/limitation_program_20261001/C06_<run>/`.

## C07 A few draws without barrier flips do not certify rare flips

**Status:** conditional. **Priority:** 1. **Inputs:** C03, C06.

**Original point:** 4 Failure 6 barrier checks. **Next action:** Bound the probability of the monitored basket lying within an arithmetic-error band around the barrier.

1. Find a valid conditional distribution or interval enclosure.
2. Bound one-date boundary mass.
3. Apply a justified union/composition bound over dates.

**Alternatives:** Conditional anti-concentration/density bound; Certified interval integration of a boundary band.

**Accept only when:**

- Prove path discrepancy eta and surviving-payoff discrepancy zeta on the stated truncated domain.
- Bound discount*(zeta + M*P(any barrier band)) and add independent law/tail errors.
- Targeted samples validate implementation only; they do not certify rare-event probability.

**Stop or change approach:** Try two analytic/interval bounds on one date; if neither composes within its allowance, forbid lower precision for this contract.

**If accepted:** Compose across dates and permit only precision choices meeting G2. **If rejected:** Keep current precision and record the failed precision-reduction branch.

**Existing evidence:** `docs/limitation_audit_20261001/CONTRACT_AND_EVIDENCE.md`.

**New receipt:** `results/limitation_program_20261001/C07_<run>/`.

## C08 Fitted convergence exponents are not lower bounds

**Status:** ready. **Priority:** 2. **Inputs:** C01, F01.

**Original point:** 2.3; 4 Failure 6 rates; 5 root cause A. **Next action:** Freeze PCA basis, development/validation split and exponent-fit procedure before evaluating alternative classical representations.

1. Respect the existing PCA degeneracy finding.
2. Freeze configuration and seeds.
3. Evaluate development selection once on reserved cases.

**Alternatives:** Canonical basis; Seeded alternative bases and eligible conditioning methods.

**Accept only when:**

- Report fit-window, scramble-unit uncertainty and rate intervals.
- Holdout outcomes are not used to select a basis or tune a slope; measured rates are not lower bounds.

**Stop or change approach:** Use the existing Stage C design where compatible; a changed design is a separate locally versioned experiment.

**If accepted:** Supply uncertainty-aware comparator inputs to C09/G4. **If rejected:** Report instability and widen the evidence range without preserving a desired advantage verdict.

**Existing evidence:** `docs/limitation_audit_20261001/CONTRACT_AND_EVIDENCE.md`; `manuscript/advantage-frontier-2026-09-23/STAGE_B_RESULTS.md`.

**New receipt:** `results/limitation_program_20261001/C08_<run>/`.

## C09 Modelled classical time is not a timed successful price

**Status:** ready. **Priority:** 1. **Inputs:** C01, C03.

**Original point:** 2.5 historical timing; 4 Failure 6 comparator. **Next action:** Complete the locally specified Stage C time-to-accuracy run using its actual target sample count and reference-price checks.

1. Inspect ongoing Stage C implementation and receipts.
2. Recover its preregistered configuration.
3. Run prescribed sample counts and report timing and uncertainty together.

**Alternatives:** Existing compiled RQMC kernels; One eligible challenger selected on development data.

**Accept only when:**

- Record actual setup/warm timing, delivered interval and reference agreement.
- Use the declared confidence procedure; modelled per-point extrapolation is labelled separately.
- Preserve existing Stage C work and its specification rather than replacing it.

**Stop or change approach:** Run one B4 target first, then the declared B8 target; a resource-limited incomplete run is reported incomplete, never timed-success evidence.

**If accepted:** Close G4 only for validated cases; use the fastest eligible successful price. **If rejected:** Fix reference/coverage/kernel issues in a new run, or mark that case unresolved and continue independent arithmetic.

**Existing evidence:** `docs/limitation_audit_20261001/CONTRACT_AND_EVIDENCE.md`; `manuscript/advantage-frontier-2026-09-23/ANALYSIS_SPEC_STAGE_C.md`; `research/frontier_classical_20261001/`.

**New receipt:** `results/limitation_program_20261001/C09_<run>/`.

## C10 The strongest tested classical method is not automatically the strongest applicable one

**Status:** ready. **Priority:** 2. **Inputs:** C01, F01.

**Original point:** 1 classical comparator; 5 root cause D. **Next action:** Make an applicability matrix of classical challengers before implementing the next one.

1. Check model and payoff compatibility.
2. Compare pilot work and mathematical error guarantees.
3. Validate the selected method on held-out cases.

**Alternatives:** Conditioning/RQMC/importance sampling; MLMC/PDE/tensor methods if the contract assumptions hold.

**Accept only when:**

- Every exclusion states the failed assumption; one eligible challenger receives the same task, error and setup accounting.
- Report strongest tested, not universally fastest, unless an exhaustive claim is independently justified.

**Stop or change approach:** Screen three families and implement the best eligible development candidate; stop an inapplicable method before performance claims.

**If accepted:** Update G4 and tighten quantum budgets if the challenger wins. **If rejected:** Keep the strongest demonstrated baseline and list bounded search exclusions.

**Existing evidence:** `docs/limitation_audit_20261001/CONTRACT_AND_EVIDENCE.md`.

**New receipt:** `results/limitation_program_20261001/C10_<run>/`.

## C11 A clean source is not an entire mean-estimation algorithm

**Status:** partial. **Priority:** 1. **Inputs:** C01, E02, H17.

**Original point:** 2 estimator model; 4 Failures 3-6; 8 evidence levels. **Next action:** Compile one complete estimator iterate for the same source family and reconcile every wrapper cost.

1. Match source and estimator contracts.
2. Test the small iterate including control-off identity.
3. Export exact calls and wrapper/synthesis costs.

**Alternatives:** Existing coherent fused wrapper; Measured bounded estimator where outer coherence is unnecessary.

**Accept only when:**

- Include normalization, source/inverse, reflection, rotations, synthesis, repeats, stopping and readout.
- Never multiply residual-estimator query counts by knock-out source depths.
- Source, estimator and price contracts share an explicit compatible identifier.

**Stop or change approach:** One small complete iterate/repetition schedule first; incompatible interfaces stop that combination.

**If accepted:** Use G2/G3/G4/H18 to produce a complete G5 scenario. **If rejected:** Keep the component result at L4 and repair the interface before claiming price runtime.

**Existing evidence:** `docs/limitation_audit_20261001/CONTRACT_AND_EVIDENCE.md`; `research/controlled_source_completion/compiler.py`; `research/controlled_priority_completion/combined_wrappers.py`.

**New receipt:** `results/limitation_program_20261001/C11_<run>/`.

## C12 Six constructions share three contracts and one toolchain

**Status:** partial. **Priority:** 3. **Inputs:** G0.

**Original point:** Introduction; 4 six attempts; 8 shared-toolchain evidence. **Next action:** Maintain an evidence-family table and independently structured replacements for shared toolchain components.

1. Map each construction to shared modules.
2. Attach existing independent arithmetic checks.
3. Identify remaining correlated assumptions.

**Alternatives:** Current exact lookup/multiplier replacements; Direct loading or a separate arithmetic backend.

**Accept only when:**

- Label six constructions over three contracts as shared evidence.
- Each independent replacement implements the same numerical target and has its own correctness/cost receipt.

**Stop or change approach:** Reuse existing exact replacement evidence; add a new independent backend only when its finite screen is promising.

**If accepted:** Credit the verified component gain once and update the shared-evidence map. **If rejected:** Report the bounded implementation result without inferring an algorithm-independent obstruction.

**Existing evidence:** `docs/limitation_audit_20261001/CONTRACT_AND_EVIDENCE.md`.

**New receipt:** `results/limitation_program_20261001/C12_<run>/`.

## C13 Optimizations interact and cannot be multiplied without a compatible schedule

**Status:** partial. **Priority:** 1. **Inputs:** G0.

**Original point:** 4 Failures 4-5; 6 better compilation. **Next action:** Adopt improvements only through one combined emitted source and a resource-matched schedule.

1. Start from constant_multiplier_v1.
2. Add the next exact change alone.
3. Compare actual full-source costs and valid capped replays.

**Alternatives:** Exact compact packing plus current arithmetic; Changed loader/precision only after G2.

**Accept only when:**

- Preserve unaffected target/leaf hashes and replay combined binding/cleanup.
- Compare at equal resource caps or show the full Pareto tradeoff.
- No product of overlapping module savings; removal of a module removes its separate optimization credit.

**Stop or change approach:** Combine two compatible changes at a time; reject a combination on correctness, cap or certified-cost failure.

**If accepted:** Set the new accepted local baseline, then re-rank the remaining hotspots. **If rejected:** Retain the last accepted baseline and record the interaction causing rejection.

**Existing evidence:** `docs/limitation_audit_20261001/CONTRACT_AND_EVIDENCE.md`; `docs/limitation_audit_20261001/CONSTANT_MULTIPLIER_RESULT.md`.

**New receipt:** `results/limitation_program_20261001/C13_<run>/`.

## C14 A classical cubic exponent is not necessary for a crossover

**Status:** audit. **Priority:** 2. **Inputs:** C04, C11, G4.

**Original point:** 7 requirements and expert summaries. **Next action:** Evaluate the actual complete inequality without imposing a classical cubic-exponent prerequisite.

1. Calculate T_C and complete T_Q at each declared epsilon.
2. Separate observed/modelled/extrapolated rows.
3. Propagate uncertainty and report both ratios.

**Alternatives:** Practical fixed-tolerance constants; Sensitivity curves with fit/extrapolation scope.

**Accept only when:**

- Use measured/certified inputs and compatible full quantum costs.
- Report break-even and tenfold conditions without universal exponent or impossibility claims.

**Stop or change approach:** One operating-point grid; unresolved estimator/hardware inputs are assumptions and cannot close G5.

**If accepted:** State a scoped crossover or scoped miss with its reproducible assumptions. **If rejected:** Preserve the negative/component result and identify the remaining dominant cost rather than forcing a new workload.

**Existing evidence:** `docs/limitation_audit_20261001/CONTRACT_AND_EVIDENCE.md`.

**New receipt:** `results/limitation_program_20261001/C14_<run>/`.

## C15 References and stale numerical summaries need individual checking

**Status:** audit. **Priority:** 2. **Inputs:** G0.

**Original point:** 3 external timing table; 7 external summaries; 9 evidence map; 10 references. **Next action:** Bind every reused numerical/literature claim to an exact version, locator and cost boundary.

1. Verify repository numerical claims locally against artifacts.
2. Read primary texts for externally reused claims when needed.
3. Record source dates, experimental/theoretical status and unresolved transfer assumptions.

**Alternatives:** Primary-source recovery; Explicit unverified/unrefreshed classification.

**Accept only when:**

- Store title, version/date, claim, locator, assumptions and transfer conditions.
- Every hardware anchor, external compiled-circuit timing and source-screen conclusion has a checked or unverified status.
- Do not refresh scientific claims from snippets or treat a selected screen as exhaustive.

**Stop or change approach:** Audit the references actually used by the next experiment first; missing primary evidence excludes that number from accepted costs.

**If accepted:** Use verified claims with their conditions and preserve historical manuscript evidence unchanged. **If rejected:** Mark the claim unverified, substitute a supported bound if available, and continue without fabricating a value.

**Existing evidence:** `docs/limitation_audit_20261001/CONTRACT_AND_EVIDENCE.md`; `docs/research_investigation/2026-09-23/ERRATA.md`.

**New receipt:** `results/limitation_program_20261001/C15_<run>/`.
