# Price requirements and gaps in the comparison evidence

Investigation date: 1 October 2026. These entries cover the assumptions surrounding the circuit, rather than treating every failed comparison as a circuit limitation. They are mainly deductions from the project's own records; proposed experiments are identified as proposals. References to sections are to [WHY_NO_ADVANTAGE.md](../../manuscript/advantage-frontier-2026-09-23/WHY_NO_ADVANTAGE.md).

## C01 One classical price is the current output

**Location:** section 1 and root cause F. A quantum state containing prices is not the contracted output. **Alternative:** a scalar observable or amplitude that can be estimated directly, rather than reconstructing a full state. **Status:** useful interface designs exist, but their measurement cost must be included. **Small test:** specify the number returned to the user and its estimator before accepting a PDE, QSVT or quantum-linear-system construction. See [formulation alternatives](FORMULATIONS_AND_CLASSICAL_COMPARATORS.md) and E18–E23 in [estimation alternatives](ESTIMATION_AND_CERTIFICATION.md). A portfolio, decision or quantum-state output is a separately labelled task.

## C02 Dollar accuracy cannot be silently weakened

**Location:** section 1 and section 7's extreme-accuracy suggestion. The chosen tolerance is a workload requirement. **Alternative:** optimize algorithms and their error allocation at that tolerance. **Status:** a declared tradeoff, not a universal obstruction. **Small test:** convert every paper's amplitude, relative or norm error to the same discounted dollars per notional. Tighter accuracy can be a sensitivity experiment, but its financial usefulness is unestablished here. Looser accuracy is not a solution to the original comparison.

## C03 The complete price needs the complete confidence allowance

**Location:** section 1, root cause F. Estimation confidence, moment certification, numerical approximation and hardware failure are not interchangeable. Deterministic approximation bounds consume error allowance rather than statistical failure probability; probabilistic certificates consume both as applicable. **Alternative:** one explicit error and failure ledger. **Status:** a solvable accounting task, incomplete for the proposed new constructions. **Small test:** check that dollar-error allowances sum within epsilon and probabilistic failures within 0.01. See E07, E11 and H18.

## C04 Tenfold advantage is a chosen threshold

**Location:** sections 1, 2.2 and 7. Failing a tenfold target does not establish that a quantum algorithm is slower; a budget miss is not the runtime ratio. **Alternative:** report the runtime ratio as well as the onefold and tenfold frontiers. **Status:** interpretation can be corrected without a new algorithm. **Small test:** for each row verify `tenfold_budget_miss = 10 * T_Q/T_C`, where both times use the same conventions. [Stage A](../../manuscript/advantage-frontier-2026-09-23/STAGE_A_RESULTS.md) explicitly makes this distinction.

## C05 The statistical allowance of 0.45 epsilon is adjustable

**Location:** section 2.1. That split is not a law of amplitude estimation. **Alternative:** minimize total implementation cost subject to a fixed complete-price error ledger; cheaper arithmetic can justify a different split. **Status:** optimization opportunity, not permission to exceed epsilon. **Small test:** sweep two allocations with an explicit source-error bound and integer estimator schedule. Keep the same total confidence. E24 provides the estimator-side analysis.

## C06 Correct digital arithmetic is not a continuous financial-law certificate

**Location:** Failure 6's payoff checks, section 7 and the Stage A qualifications. **Alternative:** bound tail truncation, finite-grid distribution error, function approximation and payoff classification separately. **Status:** open for the full Stage A bridge. **Small test:** certify one source coordinate and its propagation through one monitored basket evaluation, then compose the bounds. A valid gate truth table establishes a different fact from financial bias. [Stage A remaining Q4 task](../../manuscript/advantage-frontier-2026-09-23/STAGE_A_RESULTS.md).

## C07 A few draws without barrier flips do not certify rare flips

**Location:** Failure 6 and erratum E4. **Alternative:** a boundary-probability argument with targeted validation. For two bounded, truncated payoff implementations in `[0,M]`, suppose the monitored basket discrepancy is at most eta and their surviving-payoff discrepancy is at most zeta. A classification change can occur only if a monitored basket is within eta of its barrier. Thus an elementary bound is

`absolute price difference <= discount * (zeta + M * P(any monitored basket lies in its eta barrier band))`.

Add separately justified tail/distribution errors when returning to the continuous model. This is our bound under the stated hypotheses, not a certificate already proved for this source. **Small test:** obtain a valid density, conditioning or interval bound on the boundary-band probability; sampled frequency alone is not enough for a deterministic guarantee. **Status:** a concrete mathematical subproblem that can be isolated before reducing financial precision.

## C08 Fitted convergence exponents are not lower bounds

**Location:** section 2.3, Failure 6 and root cause A. **Alternative:** estimate uncertainty, vary valid representations and test stronger classical algorithms. **Status:** the original measurements remain evidence for tested methods. [Stage B](../../manuscript/advantage-frontier-2026-09-23/STAGE_B_RESULTS.md) finds different valid PCA bases give different measured rates. **Small test:** freeze a canonical basis, compare seeded alternatives without selecting on the final evaluation set, and report rate intervals. A faster classical result tightens the quantum budget; it is useful evidence even if it reduces the chance of advantage.

## C09 Modelled classical time is not a timed successful price

**Location:** section 2.5, Failure 6, erratum E5. **Alternative:** execute time-to-accuracy runs with setup and warm cost reported separately. **Status:** unresolved comparison evidence, not evidence that classical pricing fails. **Small test:** run one already specified target sample count and verify its confidence procedure and reference-price agreement. Do not substitute the original fitted time for that result. The existing [Stage C specification](../../manuscript/advantage-frontier-2026-09-23/ANALYSIS_SPEC_STAGE_C.md) is ongoing work outside this audit.

## C10 The strongest tested classical method is not automatically the strongest applicable one

**Location:** section 1 comparator list and root cause D. **Alternative:** add relevant conditioning, QMC, MLMC, deterministic or PDE methods after checking assumptions. **Status:** a bounded benchmark can be valid without being exhaustive, if described accurately. **Small test:** implement one mathematically eligible challenger on the unchanged contract, with equal accounting for setup and tuning. See the formulation memo's sequential importance-sampling, PDE and tensor-network candidates.

## C11 A clean source is not an entire mean-estimation algorithm

**Location:** sections 2, 4 and 8. **Alternative:** compile one complete iterate and an executable repetition/stopping schedule, including source and inverse, reflection, normalization, rotation synthesis and readout. **Status:** some compound constructions do this more completely than the knock-out sensitivity model. **Small test:** reconcile one full iterator with its source resource ledger before quoting a price runtime. E02–E06 give the relevant accounting distinctions.

## C12 Six constructions share three contracts and one toolchain

**Location:** introduction, section 4 and section 8. **Alternative:** repeat a narrowly chosen operation with an independently structured implementation. **Status:** the shared failures are real but not independent evidence against all representations. **Small test:** compare a table-driven normal loader with direct state preparation or a new arithmetic leaf, using the same numerical target. A successful replacement would test the toolchain dependence without inventing a new financial problem. [Erratum E8](../research_investigation/2026-09-23/ERRATA.md).

## C13 Optimizations interact and cannot be multiplied without a compatible schedule

**Location:** Failures 4–5, section 6's remaining compilation estimate. **Alternative:** a resource ledger with one final representation, estimator and architecture. **Status:** the statement that only about another factor of 100 remains is not a demonstrated upper bound. **Small test:** combine just two improvements and remeasure the affected source; inspect shared cost terms and workspace pressure. A loader that removes square roots eliminates the opportunity to separately claim a square-root speedup on those same gates. H17 and the hardware memo explain the runtime consequences.

## C14 A classical cubic exponent is not necessary for a crossover

**Location:** section 7's requirements table and expert-summary paragraph. **Alternative:** use actual constants and a compatible cost model. Even equal precision exponents can give a constant-factor quantum win in principle; a better exponent can still lose at practical precision. **Status:** the document partly acknowledges this already; retain that qualification everywhere. **Small test:** evaluate the actual complete inequality for each candidate. Do not demand `p_C >= 3` as a theorem, or treat a general expert assessment as a lower bound on this workload.

## C15 References and stale numerical summaries need individual checking

**Location:** sections 3, 7, 9 and 10. **Alternative:** source-level verification linked to exact claims and paper versions. **Status:** this audit found meaningful scope changes, including the QSP contract class, nested-rate interpretation and decoder timings. **Small test:** before reusing a literature number, recover its table, circuit boundary, confidence and hardware assumptions. The original 3.7-day external-circuit comparison and every individual vendor timing were not fully rederived in this pass; retain them as unrefreshed claims, not newly verified facts. Our findings do not require those numbers.

## What these entries resolve

They define which improvements preserve the original task and what would count as evidence that a small obstruction has been removed. They do not invalidate the existing negative results at their recorded operating points. They also prevent those recorded results from being treated as universal impossibility statements.
