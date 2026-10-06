# Implementation plan: arithmetic, coherent loading and reversible memory

Local plan, 1 October 2026. This covers **all 20 arithmetic/loading entries A01–A20** in the [atomic audit](../ARITHMETIC_AND_LOADING.md), mapped back to [WHY_NO_ADVANTAGE.md](../../../manuscript/advantage-frontier-2026-09-23/WHY_NO_ADVANTAGE.md). It defines what to build or prove, what constitutes a useful result, and how to move on without repeated requests for next-step approval. It authorizes no pushes, publishing, uploads or external messages. Future result directories must be fresh.

The existing exact compiler results are good local improvements. The requested 32-row lookup is complete. Carry-save variable multiplication and the signed-digit ln(2) specialization are retained components. The latest full arithmetic sources have T-depth **2,436,454** for B4x12 and **2,624,696** for B8x52 at the original caps of **550,158** and **4,460,490** logical qubits. The original Stage A depths were 6,032,678 and 6,393,144. These are emitted, capped logical-resource results under the exact seven-T CCX/all-to-all model; no hardware runtime or quantum advantage is inferred.

Existing evidence: [execution record](../EXECUTION_RESULTS.md), [ln(2) result](../CONSTANT_MULTIPLIER_RESULT.md), and [latest summary](../../../results/limitation_audit_20261001/constant_multiplier_v1/summary.json). Exact compact storage is verified only in the earlier serial source; its savings have not yet been combined with the parallel arithmetic result. The direct Gaussian prefix circuits are numerical preparation prototypes for a different finite law, not QSVT implementations or financial-law certificates.

**Immediate order:** A01 reconciles the current source; A06 combines exact compact storage with its actual capped schedule; A10 screens the remaining exact constants/squares and log-only signed range; A08 tests an exact fast adder. In parallel, A05 derives the required loading precision, and A07 establishes contract-specific ranges. A18 then tests real subgraph recomputation. Approximate-law candidates proceed as bounded prototypes, with financial adoption held to G2. The overall programme decides which of these ready tasks to run concurrently.

Status meanings: **complete** means the named component has already passed its stated checks; **partial** means a component exists but an integration/proof remains; **ready** identifies a concrete next local action; **conditional** requires a bounded feasibility result before expensive emission; **audit** can close with no code change if the existing implementation already resolves the claim. Priority 1 is first, priority 5 last. Completing an entry need not mean finding a speedup: a checked negative result also closes its proposed alternative.

Gate interfaces: **G0** fixes the financial task and provenance; **G1** verifies exact arithmetic/unitary/source validity; **G2** certifies the total dollar error; **G3** supplies an explicit estimator and 99% call/confidence schedule; **G4** supplies a matched genuinely timed classical comparator; **G5** maps physical resources/latency and tests the complete tenfold inequality. Dependencies below identify input interfaces, not a blanket demand to solve an entire neighbouring entry first.

Every run records frozen code/environment/target/library/schedule hashes and its stopping rule before execution. Use the existing `.context/frontier_t0_env/Scripts/python.exe` research environment first. Add routine isolated local dependencies only when required by the authorized test; keep their versions and provenance in its receipt. Choose the next unused run number if a proposed run001 directory exists. Preserve failed attempts and the previous baseline. Compare T count, T-depth, Clifford depth, setup time and peak qubits. Do not multiply overlapping speedup factors. Changed precision, functions or laws need G2 before adoption; an unchanged exact integer-source trial can proceed under G1 independently.

| ID | Status | Priority | Next bounded result |
|---|---|---:|---|
| A01 | ready | 1 | Build an analysis-only ledger for both latest B4x12 and B8x52 sources, assigning every node and emitted invocation to exactly one of uniform preparation, scalar normal generation, correlation, or path/payoff. |
| A02 | partial | 3 | Freeze one scalar Gaussian grid and its allocated error, then complete the Clifford+T cost of the existing prefix-rotation preparation/inverse before screening a separate QSVT Gaussian loader. |
| A03 | partial | 3 | Replace floating-point prefix probabilities at the first two Gaussian-loading levels with interval-certified probabilities and angle enclosures, then synthesize those rotations with a charged error budget. |
| A04 | partial | 3 | Emit a sequential preparation/inverse circuit for the existing ten-bit bond-eight Gaussian MPS compression, then measure synthesis error and resource cost against the prefix baseline. |
| A05 | ready | 2 | Prove a two-factor preparation-error bound and assign a numeric scalar allowance from a frozen dollar loading budget, then scale the proved construction to each actual draw count. |
| A06 | partial | 1 | Adapt compact SSA binding to the latest carry-save/ln(2) source and memory-capped wave scheduler without changing any arithmetic width or finite financial function. |
| A07 | ready | 2 | Create a new contract-specific interval/relational certificate for one B4x12 exponential, including its range-reduction integer and every intermediate coefficient/product/shift. |
| A08 | ready | 2 | Emit an exact modular clean-XOR carry-lookahead add/subtract leaf matching primitives.build, then compare it with the current ripple implementation at 72 bits. |
| A09 | partial | 2 | Inventory the proved active operand widths, then benchmark range-specific carry-save products at 24, 40 and 72 active bits against the already retained exact multiplier. |
| A10 | partial | 1 | Enumerate the remaining expensive coefficients and exact self-products, then prove whether the logarithm range-reduction integer can use seven signed bits in the already exact ln(2) specialization. |
| A11 | ready | 3 | Implement a non-restoring clean-XOR alternative for the current exact fixed-point square root, including root/remainder erasure; the baseline already implements digit-by-digit square root. |
| A12 | ready | 3 | Inventory actual divide denominators and prove one positive range, then implement reciprocal multiplication with a final quotient/remainder correction for that range. |
| A13 | ready | 3 | For the newly proved exponential domain, certify a finite grid of minimax degree/segment choices before emitting the best two complete function candidates; the current Estrin source is the baseline. |
| A14 | conditional | 4 | Compute a charged iteration/add/shift/cleanup resource bound for a reversible cosine on the exact Box-Muller domain; proceed to gates only if it can beat the measured polynomial block. |
| A15 | complete | 1 | Register the existing shared-prefix lookup as a completed component and carry its versioned leaf hashes and tests into every new combined-source manifest; do not rerun the already solved 32-row experiment without a code/table change. |
| A16 | partial | 3 | Build one three- or four-bit temporary-AND adder fragment with explicit measurement/feed-forward and verify its complete corrected channel in every branch before attempting compiler integration. |
| A17 | audit | 2 | Audit which complete estimator schedules already use fused=True, then phase-check a tiny complete compute-controlled-phase-uncompute/reflection iterate and identify any actual duplicate copy boundary. |
| A18 | partial | 2 | Extract one actual Gaussian-plus-exponential subgraph and emit checkpoint/recompute schedules at 75% and 50% of its measured baseline workspace, using the latest exact leaf library. |
| A19 | conditional | 3 | Build a two-asset/four-date monitored arithmetic-basket verification harness comparing existing SSA evaluation with a reversible current-state/violation-count design on identical finite draws. |
| A20 | conditional | 5 | Write and certify the two-asset/one-date arithmetic-basket predicates in log coordinates, preserving barrier >= H as knock-out, alive < H, and the separate positive-payoff strike test > K; then screen a sum-of-exponentials block encoding against two explicit exponential circuits. |

## Entry-by-entry execution decisions

## A01. Separate uniform preparation, normal loading, correlation and payoff costs

**Status:** ready. **Priority:** 1. **Required interfaces:** G0.

**Original limitation:** §3 item 1: coherent randomness and 468 Gaussians; §3 operation cost table; §6 better compilation.

**Next action:** Build an analysis-only ledger for both latest B4x12 and B8x52 sources, assigning every node and emitted invocation to exactly one of uniform preparation, scalar normal generation, correlation, or path/payoff.

**Small implementation steps:**

1. Read the latest target/source/schedule and annotate the roots of each normal and each correlation transform.
2. Partition shared nodes deterministically, reconcile forward, output-copy and inverse costs with the archived source, and report uniform Hadamards separately.
3. Identify the top three measured depth and work contributors and use them to order remaining arithmetic trials.

**Alternatives to screen:**

- Use producer/consumer reachability to assign shared constants once; retain a separate list of shared nodes rather than silently duplicating them.
- Report both emitted operation totals and critical-path attribution; do not add category depths as if they were serial.

**Acceptance:**

- 100% of non-input nodes and leaf invocations are assigned once, with no duplicates or omissions.
- T, X, CX and CCX totals reproduce each latest emitted resource total exactly; random-Hadamard counts reproduce input declarations.
- Recomputed dependency depth agrees with independent DAG accounting; schedule T-depth and peak qubits agree exactly with the current capped schedule. Category depth is labelled diagnostic and is not summed.

**Stop rule:** One ledger implementation and one independently recomputed reconciliation per case. If shared-node classification is ambiguous, retain its attribution as an explicit shared cost and resolve accounting before proposing loader savings.

**On pass:** Freeze this ledger as the baseline for all source changes and select the next trial by its measured contribution.

**On fail:** Fix provenance or attribution; do not alter financial code or infer an improvement from incomplete totals.

**Existing evidence and verified starting code:**

- [manuscript/advantage-frontier-2026-09-23/STAGE_A_RESULTS.md](../../../manuscript/advantage-frontier-2026-09-23/STAGE_A_RESULTS.md)
- [research/controlled_source_completion/finance.py](../../../research/controlled_source_completion/finance.py)
- [research/controlled_source_completion/compiler.py](../../../research/controlled_source_completion/compiler.py)
- [results/limitation_audit_20261001/constant_multiplier_v1/summary.json](../../../results/limitation_audit_20261001/constant_multiplier_v1/summary.json)
- [research/advantage_frontier_20260923/barrier_oracle_depth.py](../../../research/advantage_frontier_20260923/barrier_oracle_depth.py)

**Planned local artifacts:**

- `results/limitation_program_20261001/A01_run001/protocol.json`
- `results/limitation_program_20261001/A01_run001/cost_ledger.json`
- `results/limitation_program_20261001/A01_run001/summary.md`

## A02. Replace Box-Muller only after a complete scalar-loader comparison

**Status:** partial. **Priority:** 3. **Required interfaces:** G0, A01, A05.

**Original limitation:** §3 item 1: Box-Muller or equivalent loader; §5 root cause C: state loading.

**Next action:** Freeze one scalar Gaussian grid and its allocated error, then complete the Clifford+T cost of the existing prefix-rotation preparation/inverse before screening a separate QSVT Gaussian loader.

**Small implementation steps:**

1. Use the conditioned [-6,6] midpoint grid only as a clearly named alternative finite law; preserve the archived Box-Muller law as a separate baseline.
2. Bound rotation and coefficient errors, synthesize all rotations, and include preparation, inverse and any amplification/reflection overhead.
3. For QSVT, derive the degree and filling-fraction cost before emitting; emit one smallest viable instance only if the screen is competitive.
4. Compare complete scalar cost and then a source containing two draws; adoption at 468 draws requires G2, not merely a histogram.

**Alternatives to screen:**

- Existing exact numerical prefix preparation; arbitrary RY rotations must be synthesized and charged.
- QSVT preparation with explicit polynomial degree, block encoding, filling fraction, amplification and success handling.
- The emitted MPS candidate from A04 on precisely the same scalar target.

**Acceptance:**

- Prepared amplitudes are square roots of the specified masses, not the Gaussian density itself; normalization and grid units are verified.
- A preparation/inverse pair meets the preallocated scalar trace-distance/operator-error bound, including synthesis and unsuccessful branches.
- Under a frozen logical-qubit cap at least one complete scalar resource improves without an unpriced resource increase; full adoption additionally passes G2.
- The classical comparator can sample the same new finite law and is separately timed.

**Stop rule:** Screen prefix, QSVT and MPS at one common grid and three error targets; emit at most two candidates. Stop replacing Box-Muller if no candidate reaches the allocated error or if its complete cost is dominated.

**On pass:** Retain the best certified scalar loader, then compose two draws and finally the full input law through A05 and G2.

**On fail:** Keep Box-Muller for the exact source, record the failing synthesis/degree/normalization term, and continue exact arithmetic work.

**Existing evidence and verified starting code:**

- [research/limitation_audit_20261001/experiment_gaussian.py](../../../research/limitation_audit_20261001/experiment_gaussian.py)
- [results/limitation_audit_20261001/gaussian_v3/summary.json](../../../results/limitation_audit_20261001/gaussian_v3/summary.json)
- [docs/limitation_audit_20261001/EXECUTION_RESULTS.md](../../../docs/limitation_audit_20261001/EXECUTION_RESULTS.md)

**Planned local artifacts:**

- `results/limitation_program_20261001/A02_run001/protocol.json`
- `results/limitation_program_20261001/A02_run001/scalar_loader_comparison.json`
- `results/limitation_program_20261001/A02_run001/preparation_and_inverse.qasm`
- `results/limitation_program_20261001/A02_run001/error_certificate.json`

## A03. Certify recursive-loading integrals and conditional angles

**Status:** partial. **Priority:** 3. **Required interfaces:** G0, A05.

**Original limitation:** §3 item 1: equivalent loader; §5 root cause C: alternative state preparation.

**Next action:** Replace floating-point prefix probabilities at the first two Gaussian-loading levels with interval-certified probabilities and angle enclosures, then synthesize those rotations with a charged error budget.

**Small implementation steps:**

1. Extract the first two levels of the existing prefix loader, keeping its cutoff, bins and normalization fixed.
2. Enclose each probability ratio and the square-root/arccos angle; handle empty or tiny conditional masses explicitly.
3. Synthesize these angles, compare branch amplitudes to the enclosures, and derive a precision-dependent bound for deeper levels.
4. Count all distinct angles and setup work before claiming this method scales beyond the existing ten-bit prototype.

**Alternatives to screen:**

- Analytic normal-CDF interval differences evaluated deterministically.
- Certified rational/polynomial CDF approximations with explicit domain and error.
- Precomputed static angle structure; generation cost and storage remain part of setup.

**Acceptance:**

- Every first-two-level probability and angle is enclosed rigorously; interval divisions exclude zero or have a separately proved branch rule.
- Complete synthesis cost and cumulative preparation error are finite functions of requested precision.
- No Monte Carlo integration, oracle integral, small-angle pruning or arbitrary-rotation cost is left unpriced.
- Numerical simulation is an implementation check, not substituted for the interval proof.

**Stop rule:** Two certified levels and a full-tree count suffice for the first decision. Reject the cheap-recursive-loader claim if precision makes interval/angle generation or the exponential prefix table dominate A02’s comparator.

**On pass:** Extend certificates only to the loader candidate selected by A02; reuse them for the identical grid.

**On fail:** Retain the existing numerical prototype as exploratory evidence and prefer an analytically certified QSVT or MPS route if available.

**Existing evidence and verified starting code:**

- [research/limitation_audit_20261001/experiment_gaussian.py](../../../research/limitation_audit_20261001/experiment_gaussian.py)
- [results/limitation_audit_20261001/gaussian_v3/summary.json](../../../results/limitation_audit_20261001/gaussian_v3/summary.json)
- [docs/limitation_audit_20261001/ARITHMETIC_AND_LOADING.md](../../../docs/limitation_audit_20261001/ARITHMETIC_AND_LOADING.md)

**Planned local artifacts:**

- `results/limitation_program_20261001/A03_run001/protocol.json`
- `results/limitation_program_20261001/A03_run001/conditional_angle_intervals.json`
- `results/limitation_program_20261001/A03_run001/synthesis_cost.json`

## A04. Turn Gaussian MPS compression into an emitted, synthesized circuit

**Status:** partial. **Priority:** 3. **Required interfaces:** G0, A03, A05.

**Original limitation:** §3 item 1: coherent normal loading; §6 better compilation.

**Next action:** Emit a sequential preparation/inverse circuit for the existing ten-bit bond-eight Gaussian MPS compression, then measure synthesis error and resource cost against the prefix baseline.

**Small implementation steps:**

1. Convert normalized MPS cores into isometries with explicit scratch and a complete inverse.
2. Verify the uncompressed target probabilities, compressed state and emitted state separately; charge all three error sources.
3. Synthesize the circuit at scalar allowances delta, delta/10 and delta/100, including generation time.
4. If no financial allocation exists yet, use 1e-6, 1e-8 and 1e-10 as exploratory trace-distance targets and label them nonfinancial.

**Alternatives to screen:**

- Bond caps 2, 4 and 8 using the existing tensor-train decomposition.
- QSVT and certified prefix loaders from A02/A03.
- A larger bond only if the frozen accuracy target cannot be reached at bond eight; do not silently enlarge the initial screen.

**Acceptance:**

- Forward/inverse and reference-entangled checks pass, and every ancilla returns to its declared state.
- Compression, isometry-emission and synthesis errors sum to at most the chosen scalar allowance.
- Complete preparation/inverse resource counts include every arbitrary rotation; the numerical 3.49e-11 compression result is not treated as an emitted-circuit certificate.
- At least one certified circuit is nondominated against the prefix candidate at the same grid, error and cap; production adoption requires G2.

**Stop rule:** Three bonds and three error targets on the ten-bit grid, with at most three emitted candidates. If all are dominated or miss the error target, archive the negative result and stop this architecture.

**On pass:** Add the MPS circuit to A02’s matched loader frontier; compose it under A05 before source replacement.

**On fail:** Keep the compression observation only; do not credit a loading speedup in the complete circuit.

**Existing evidence and verified starting code:**

- [research/limitation_audit_20261001/experiment_gaussian.py](../../../research/limitation_audit_20261001/experiment_gaussian.py)
- [results/limitation_audit_20261001/gaussian_v3/summary.json](../../../results/limitation_audit_20261001/gaussian_v3/summary.json)
- [results/limitation_audit_20261001/gaussian_v3/gaussian_10.json](../../../results/limitation_audit_20261001/gaussian_v3/gaussian_10.json)

**Planned local artifacts:**

- `results/limitation_program_20261001/A04_run001/protocol.json`
- `results/limitation_program_20261001/A04_run001/mps_loader.qasm`
- `results/limitation_program_20261001/A04_run001/accuracy_frontier.json`

## A05. Allocate and compose loading error across independent draws

**Status:** ready. **Priority:** 2. **Required interfaces:** G0.

**Original limitation:** §3 item 1: 468 Gaussians; §4 Failure 5: input and workspace width; §5 root cause F: certification.

**Next action:** Prove a two-factor preparation-error bound and assign a numeric scalar allowance from a frozen dollar loading budget, then scale the proved construction to each actual draw count.

**Small implementation steps:**

1. Confirm the independent factors and correlation map in each source; use the actual count for each case rather than applying 468 everywhere.
2. Prove the joint law bound for two factors and derive a rigorous payoff bound M or a tail/moment alternative if no useful uniform bound exists.
3. Allocate the total dollar loading budget across tail truncation, grid, preparation, synthesis and correlation.
4. Compute the required per-coordinate delta for the full source and feed it to A02–A04; barrier discontinuities receive their own band term.

**Alternatives to screen:**

- Conservative product-state trace distance <= sum_j delta_j and bounded-payoff expectation error <= M times total variation.
- A coupling/Wasserstein bound for smooth path components plus a separate barrier-band probability bound.
- Unequal per-factor allowances based on rigorously bounded sensitivities; rank reduction is a separately budgeted model change.

**Acceptance:**

- Allocated nonnegative error terms sum to no more than the frozen loading budget; the overall pricing ledger remains within epsilon through G2.
- Every probability/trace-distance bound uses its stated law and normalization, and composition does not assume independent circuit errors without proof.
- No factor is dropped and no PCA rank is reduced under an exact-optimization label.
- The required scalar allowance is numeric for B4x12 and B8x52; infeasible precision is recorded as a failed candidate, not omitted.

**Stop rule:** Evaluate the conservative product bound and one contract-aware refinement. If both force an unattainable loader precision at the screened costs, suspend law replacement and keep exact-source work moving.

**On pass:** Supply the allocation to loader trials; require its certificate to be updated whenever the grid or draw count changes.

**On fail:** Retain the current law and document the dominant tail, grid or barrier term for the next formulation decision.

**Existing evidence and verified starting code:**

- [research/controlled_source_completion/finance.py](../../../research/controlled_source_completion/finance.py)
- [results/limitation_audit_20261001/gaussian_v3/summary.json](../../../results/limitation_audit_20261001/gaussian_v3/summary.json)
- [docs/limitation_audit_20261001/EXECUTION_RESULTS.md](../../../docs/limitation_audit_20261001/EXECUTION_RESULTS.md)

**Planned local artifacts:**

- `results/limitation_program_20261001/A05_run001/protocol.json`
- `results/limitation_program_20261001/A05_run001/loading_error_allocation.json`
- `results/limitation_program_20261001/A05_run001/two_factor_proof.md`

## A06. Combine exact compact storage with the latest arithmetic schedule

**Status:** partial. **Priority:** 1. **Required interfaces:** G0, A01.

**Original limitation:** §3 item 2: global 72-bit fixed point; §4 Failure 5: millions of retained SSA qubits; §5 root cause C: precision and representation.

**Next action:** Adapt compact SSA binding to the latest carry-save/ln(2) source and memory-capped wave scheduler without changing any arithmetic width or finite financial function.

**Small implementation steps:**

1. Recompute masks on the latest archived target and verify they match the same graph and table hashes.
2. Build a compact live layout for parallel waves, reserve distinct private leaf wires, and account for all concurrently active scratch. Supply this early live-width/capacity interface to A18/H15; do not wait for A18’s later pebbling screen to combine existing exact packing.
3. Emit schedules at the original caps and at 90% of each cap; replay the same seeded and uniform-endpoint inputs.
4. Choose a nondominated depth/width point; only then consider reducing arithmetic precision or changing representation.

**Alternatives to screen:**

- Reuse proven possible-one masks and distinct private zero-bit wires while keeping every leaf interface unchanged.
- Emit narrow flags/indexes only when operation semantics prove their active width.
- After exact packing, investigate per-node signed ranges and fractional precision via A07 and G2; floating point remains a separate bounded screen.

**Acceptance:**

- All operations compute the same 72/40 integer target, arbitrary output XOR remains valid, and every promised-zero/private wire is restored.
- Full B4x12 and B8x52 source replays match the independent integer interpreter; small graphs exhaust width/mask cases.
- The emitted peak qubits and concurrency are measured, not obtained by subtracting the earlier serial savings from a parallel total.
- At the original caps, accept only if source T-depth does not increase; alternatively retain a lower-cap frontier point with its full measured depth/work penalty.

**Stop rule:** One merged binding, two caps per case, and at most one scheduler adjustment after a failed cap. If compact private-wire lifetimes cannot be proved, retain the previously verified serial opt-in path.

**On pass:** Make this combined exact source the next baseline with fresh hashes, then use freed workspace for A08/A09/A18 candidates.

**On fail:** Keep serial packing and capped arithmetic as separate verified alternatives; record the precise allocation conflict and continue independent leaf trials.

**Existing evidence and verified starting code:**

- [research/controlled_source_completion/compact_storage.py](../../../research/controlled_source_completion/compact_storage.py)
- [research/controlled_source_completion/budget_schedule.py](../../../research/controlled_source_completion/budget_schedule.py)
- [research/limitation_audit_20261001/experiment_compact_storage.py](../../../research/limitation_audit_20261001/experiment_compact_storage.py)
- [results/limitation_audit_20261001/compact_storage_v1/summary.json](../../../results/limitation_audit_20261001/compact_storage_v1/summary.json)
- [results/limitation_audit_20261001/constant_multiplier_v1/summary.json](../../../results/limitation_audit_20261001/constant_multiplier_v1/summary.json)

**Planned local artifacts:**

- `results/limitation_program_20261001/A06_run001/protocol.json`
- `results/limitation_program_20261001/A06_run001/compact_wave_sources.json`
- `results/limitation_program_20261001/A06_run001/cap_frontier.json`
- `results/limitation_program_20261001/A06_run001/replay_receipts.json`

## A07. Prove reachable ranges before narrowing arithmetic

**Status:** ready. **Priority:** 2. **Required interfaces:** G0, A01.

**Original limitation:** §4 Failure 5: range-certified multipliers; §4 Failure 6: incomplete knock-out financial validation; §5 root cause C: precision choices.

**Next action:** Create a new contract-specific interval/relational certificate for one B4x12 exponential, including its range-reduction integer and every intermediate coefficient/product/shift.

**Small implementation steps:**

1. Identify the exponential on the measured critical path and its finite uniform-input domain.
2. Propagate signed bounds through range reduction and polynomial evaluation, including modulo arithmetic, shift limits and discarded-bit carry.
3. Attempt exact narrowing at one proved node, with same-graph proof dispatch and a fallback generic leaf.
4. For approximate narrowing, derive rounding accumulation and barrier-band probability separately; never borrow the compound-source certificate as if it covered this contract.

**Alternatives to screen:**

- Full finite-domain interval arithmetic with directed rounding.
- Affine or relational bounds when interval cancellation is too loose.
- Deliberate tail truncation only as a changed-law branch with a separately proved tail and barrier allowance under G2.

**Acceptance:**

- Every omitted bit is proved redundant for every declared finite input, or an explicit changed-law/error certificate is supplied.
- Coefficient intermediates, signed edges, overflow and underflow are included in the proof.
- A narrowed exact leaf matches the original integer result, including negative operands and arbitrary output, with restored workspace.
- Any approximate price claim passes G2, including probability-weighted barrier flips rather than a typical-path observation.

**Stop rule:** One exponential proof with interval propagation and one relational refinement. If the range remains too loose, preserve the wider node and move to another exact cost instead of repeatedly sampling paths.

**On pass:** Use the proved active widths in A06/A09/A10 and supply the certified approximation domain to A13.

**On fail:** Record the first unbounded or overflow-sensitive node and retain its full width; no narrowing based on sampled extrema.

**Existing evidence and verified starting code:**

- [research/controlled_priority_completion/range_joint_arithmetic.py](../../../research/controlled_priority_completion/range_joint_arithmetic.py)
- [research/controlled_priority_completion/range_audit.py](../../../research/controlled_priority_completion/range_audit.py)
- [research/controlled_source_completion/ir.py](../../../research/controlled_source_completion/ir.py)
- [manuscript/advantage-frontier-2026-09-23/STAGE_A_RESULTS.md](../../../manuscript/advantage-frontier-2026-09-23/STAGE_A_RESULTS.md)
- [research/advantage_frontier_20260923/barrier_oracle_depth.py](../../../research/advantage_frontier_20260923/barrier_oracle_depth.py)

**Planned local artifacts:**

- `results/limitation_program_20261001/A07_run001/protocol.json`
- `results/limitation_program_20261001/A07_run001/exponential_range_certificate.json`
- `results/limitation_program_20261001/A07_run001/narrow_leaf_replay.json`

## A08. Benchmark a matching clean carry-lookahead adder

**Status:** ready. **Priority:** 2. **Required interfaces:** G0, A01.

**Original limitation:** §3 add/subtract leaf row; §5 root cause C: arithmetic architecture; §6 better compilation.

**Next action:** Emit an exact modular clean-XOR carry-lookahead add/subtract leaf matching primitives.build, then compare it with the current ripple implementation at 72 bits.

**Small implementation steps:**

1. Specify signed two's-complement modular add/sub semantics and nonzero output behavior.
2. Exhaust all inputs/outputs at widths 1–5, then replay 72-bit carry chains, signed overflow and random values.
3. Measure T count, T-depth, Clifford depth, peak qubits and cache provenance under the current exact seven-T CCX model.
4. Screen at a 4,096-qubit leaf ceiling; compile the viable candidate in both full sources under their actual frozen caps.

**Alternatives to screen:**

- Out-of-place carry-lookahead plus copying and inverse.
- In-place carry-lookahead wrapped to the same clean output interface.
- Reuse ripple for tight workspace; measurement-based adders belong to A16’s distinct phase-aware backend.

**Acceptance:**

- Every small input pair and nonzero-output test matches the current leaf; inputs and workspace restore in both directions.
- Production tests include all-ones carry chains, signed extrema and modular wrap.
- Retain a logical candidate only if it is nondominated at the frozen cap; adoption requires measured full-source T-depth reduction or lower width without hidden work.
- G5 assesses routing, simultaneous magic-state demand and reaction latency before any runtime gain is claimed.

**Stop rule:** Two carry-lookahead variants at 24, 40 and 72 bits; emit full sources for at most the best two. Stop if every variant exceeds the cap or full-source depth is unchanged/worse.

**On pass:** Retain the matching adder and rerun only arithmetic leaves that actually use it; measure combined gains rather than multiplying factors.

**On fail:** Keep ripple and its verified semantics; use the result to limit A14’s shift-add feasibility screen.

**Existing evidence and verified starting code:**

- [research/controlled_source_completion/primitives.py](../../../research/controlled_source_completion/primitives.py)
- [research/journal_sprint/reversible_fixed_point.py](../../../research/journal_sprint/reversible_fixed_point.py)
- [research/controlled_source_completion/budget_schedule.py](../../../research/controlled_source_completion/budget_schedule.py)
- [results/limitation_audit_20261001/constant_multiplier_v1/summary.json](../../../results/limitation_audit_20261001/constant_multiplier_v1/summary.json)

**Planned local artifacts:**

- `results/limitation_program_20261001/A08_run001/protocol.json`
- `results/limitation_program_20261001/A08_run001/adder_frontier.json`
- `results/limitation_program_20261001/A08_run001/full_source_comparison.json`

## A09. Extend the measured multiplier frontier without assuming Karatsuba wins

**Status:** partial. **Priority:** 2. **Required interfaces:** G0, A01, A07.

**Original limitation:** §3 item 2: multiply cost; §4 Failure 5: range-narrow multiplication; §5 root cause C: quadratic schoolbook work.

**Next action:** Inventory the proved active operand widths, then benchmark range-specific carry-save products at 24, 40 and 72 active bits against the already retained exact multiplier.

**Small implementation steps:**

1. Keep the same signed floor(product/2^f) modulo 2^w output and count carry from discarded low bits.
2. Generate only justified operand/sign specializations and bind each through proof-aware dispatch with generic fallback.
3. Exhaust small signed words, then test each production active-width promise and invalid-promise negative control.
4. Compile at most two nondominated candidates under the whole-source caps, including recomputation and extra scratch.

**Alternatives to screen:**

- Truncated carry-save products with one final carry-propagating add.
- Carry-lookahead final addition if A08 establishes a matched benefit.
- A single reversible Karatsuba prototype only if a charged recursion/base-case gate screen can beat the current exact 72-bit leaf.

**Acceptance:**

- Small-width exhaustive tests cover all supported fractional widths and signed pairs; production checks cover signed extremes, nonzero output and inverse cleanup.
- Full-product costs are never compared to truncated-product costs without matching requested output bits.
- Every specialization has a static proof; all resource figures include sign corrections and uncomputation.
- Retain only a measured capped-source improvement; the existing 90,592-to-3,696 leaf result is evidence already earned, not a new forecast.

**Stop rule:** Three active widths and at most two new circuit families. Reject Karatsuba for this run if its complete estimate is dominated before emission; do not pursue its asymptotic exponent at arbitrary widths.

**On pass:** Adopt the measured proof-dispatched variant, preserve the current generic carry-save and low-workspace alternatives, and update A01.

**On fail:** Keep the verified carry-save backend; shift effort to width management or another measured bottleneck.

**Existing evidence and verified starting code:**

- [research/controlled_source_completion/carry_save_multiplier.py](../../../research/controlled_source_completion/carry_save_multiplier.py)
- [research/controlled_priority_completion/ranged_multiplier.py](../../../research/controlled_priority_completion/ranged_multiplier.py)
- [research/controlled_source_completion/budget_schedule.py](../../../research/controlled_source_completion/budget_schedule.py)
- [research/limitation_audit_20261001/test_carry_save_multiplier.py](../../../research/limitation_audit_20261001/test_carry_save_multiplier.py)
- [results/limitation_audit_20261001/multiplier_v2/summary.json](../../../results/limitation_audit_20261001/multiplier_v2/summary.json)
- [results/limitation_audit_20261001/constant_multiplier_v1/summary.json](../../../results/limitation_audit_20261001/constant_multiplier_v1/summary.json)

**Planned local artifacts:**

- `results/limitation_program_20261001/A09_run001/protocol.json`
- `results/limitation_program_20261001/A09_run001/active_width_inventory.json`
- `results/limitation_program_20261001/A09_run001/multiplier_frontier.json`

## A10. Finish constant-product and square specialization after the ln(2) win

**Status:** partial. **Priority:** 1. **Required interfaces:** G0, A01, A07.

**Original limitation:** §3 multiplication and polynomial arithmetic; §5 root cause C: separate squares and constant products.

**Next action:** Enumerate the remaining expensive coefficients and exact self-products, then prove whether the logarithm range-reduction integer can use seven signed bits in the already exact ln(2) specialization.

**Small implementation steps:**

1. Freeze the existing ln(2) result: 46,176 to 1,152 leaf T-depth and the measured 12.51%/12.37% complete-source reductions.
2. Prove the log exponent range [-40,31] from msb(x)-40 and the graph’s positive-input guard. A seven-bit specialization requires a static sign-extension promise for the upper operand, not just the existing zero-low-bit promise; keep exp-derived operands at their independently proved width.
3. Emit one narrower log-only coefficient leaf, or the next most expensive coefficient if the screen predicts no source benefit.
4. For actual self-products, derive an exact truncated square and run matched small/production checks; compile only the best two changes.

**Alternatives to screen:**

- Signed-digit shift-add for tighter scratch and signed-digit carry-save for lower depth; both already implemented for ln(2).
- General constant specialization with zero-low-bit contracts only where same-graph proofs justify them.
- A dedicated square using symmetric partial products, preserving discarded-bit carry and signed semantics.

**Acceptance:**

- The coefficient 762123384786 remains a positive integer, not an incorrectly signed 40-bit word.
- Each width/zero-low-bit promise is proved from the same graph; unproved calls retain the generic leaf.
- Signed floor/truncation, arbitrary output XOR, inverse execution and workspace restoration match the archived leaf exactly.
- Accept only measured full-source resource improvements under the frozen cap; do not reuse the prior 40.08x leaf gain as another multiplier.

**Stop rule:** Screen the top three constant coefficients and the top two square signatures; emit at most two candidates. Stop a candidate when its maximum attributable depth saving is below 0.1% of the current source or it is resource-dominated.

**On pass:** Keep the winning specialization with versioned proof-aware cache keys and refresh full-source accounting.

**On fail:** Retain the current verified ln(2) implementation and mark the screened coefficient/square as having no local benefit.

**Existing evidence and verified starting code:**

- [research/controlled_source_completion/constant_multiplier.py](../../../research/controlled_source_completion/constant_multiplier.py)
- [research/limitation_audit_20261001/experiment_constant_multiplier.py](../../../research/limitation_audit_20261001/experiment_constant_multiplier.py)
- [research/limitation_audit_20261001/test_constant_multiplier.py](../../../research/limitation_audit_20261001/test_constant_multiplier.py)
- [docs/limitation_audit_20261001/CONSTANT_MULTIPLIER_RESULT.md](../../../docs/limitation_audit_20261001/CONSTANT_MULTIPLIER_RESULT.md)
- [results/limitation_audit_20261001/constant_multiplier_v1/summary.json](../../../results/limitation_audit_20261001/constant_multiplier_v1/summary.json)

**Planned local artifacts:**

- `results/limitation_program_20261001/A10_run001/protocol.json`
- `results/limitation_program_20261001/A10_run001/constant_square_inventory.json`
- `results/limitation_program_20261001/A10_run001/specialization_comparison.json`

## A11. Match square-root interfaces and charge remainder cleanup

**Status:** ready. **Priority:** 3. **Required interfaces:** G0, A01, A07.

**Original limitation:** §3 square-root leaf row; §4 Failure 1: coherent Heston-step bottleneck; §5 root cause C: numerical functions.

**Next action:** Implement a non-restoring clean-XOR alternative for the current exact fixed-point square root, including root/remainder erasure; the baseline already implements digit-by-digit square root.

**Small implementation steps:**

1. Freeze the existing exact function out XOR floor(sqrt(unsigned(x)*2^f)), with its nonnegative caller guard. The baseline is already digit-by-digit with stored remainders; the new candidate must improve its architecture rather than relabel it.
2. Exhaust small widths and every supported fractional count; test zero, one input quantum and values adjacent to perfect squares.
3. Emit the 72/40 candidate and compare complete clean-leaf resources at the same input domain.
4. If Newton is screened, allocate approximation error and handle small denominators before any price adoption.

**Alternatives to screen:**

- Non-restoring integer square root with the exact input scaling, output bits and charged remainder cleanup; compare to the existing digit-by-digit implementation.
- Normalized Newton reciprocal-square-root plus multiplication, with a certified zero/small-input branch.
- Remove only Box-Muller square roots if A02 succeeds; Heston’s state-dependent square root remains.

**Acceptance:**

- Exact candidate matches the historical integer square-root function for every exhaustive input and all selected signed-domain guards.
- No root remainder or input-scaling work is omitted; arbitrary output and inverse cleanup are supported.
- Retain only a nondominated leaf and measure its actual complete-source contribution via A01.
- Approximate Newton substitution requires G2 and is never labelled integer-equivalent; a Gaussian-loader removal is not credited to the Heston step.

**Stop rule:** One exact root family and one analytic Newton resource/error screen at 24, 40 and 72 bits. Stop if no complete leaf improves or if the reachable near-zero domain prevents a bounded approximation.

**On pass:** Integrate the exact root into the unchanged source, or retain a separately certified approximate branch for G2 review.

**On fail:** Keep clean_sqrt and document whether scaling, remainder erasure, near-zero handling or sequential depth consumed the proposed saving.

**Existing evidence and verified starting code:**

- [research/controlled_source_completion/primitives.py](../../../research/controlled_source_completion/primitives.py)
- [research/antithetic_feasibility/reversible.py](../../../research/antithetic_feasibility/reversible.py)
- [research/controlled_source_completion/finance.py](../../../research/controlled_source_completion/finance.py)
- [docs/limitation_audit_20261001/EXECUTION_RESULTS.md](../../../docs/limitation_audit_20261001/EXECUTION_RESULTS.md)

**Planned local artifacts:**

- `results/limitation_program_20261001/A11_run001/protocol.json`
- `results/limitation_program_20261001/A11_run001/sqrt_semantics.json`
- `results/limitation_program_20261001/A11_run001/sqrt_frontier.json`

## A12. Screen reciprocal division with exact quotient correction

**Status:** ready. **Priority:** 3. **Required interfaces:** G0, A01, A07.

**Original limitation:** §3 divide leaf row; §4 Failure 4: controlled-source phase arithmetic; §5 root cause C: numerical arithmetic.

**Next action:** Inventory actual divide denominators and prove one positive range, then implement reciprocal multiplication with a final quotient/remainder correction for that range.

**Small implementation steps:**

1. Respect divide’s unsigned restoring semantics and zero-divisor behavior; Graph.div’s guard does not establish a useful away-from-zero bound by itself.
2. Prove the selected denominator’s minimum/maximum and bound the required reciprocal precision.
3. Compute a candidate quotient, charge comparison/multiply/subtract correction, and restore seed, iteration and remainder workspace.
4. Compare exact quotients on every small input and selected large boundary cases; separately ledger any approximate option.

**Alternatives to screen:**

- Constant or power-of-two divide specialization when the exact graph permits it.
- Normalized seed-table Newton reciprocal with exact correction.
- An approximate reciprocal-only branch with its own phase/payoff error allowance under G2.

**Acceptance:**

- An exact candidate returns the same low w quotient bits as floor(a*2^f/b), including saturation/wrap conventions and declared zero handling.
- The correction count has a proved finite bound on the selected range.
- All lookup, normalization, iteration and correction resources are included in the clean-leaf comparison.
- Approximate branches satisfy their allocated G2 term and do not inherit exact-source validity merely from small numerical errors.

**Stop rule:** Screen all denominator classes once; prototype the highest-cost proved-away-from-zero class and one constant class. Stop Newton replacement if correcting the quotient consumes its saving.

**On pass:** Dispatch exact proven denominator classes with fallback; offer the approximate branch only as a separate certified target.

**On fail:** Keep restoring division and record the minimum-denominator or correction bottleneck.

**Existing evidence and verified starting code:**

- [research/controlled_source_completion/primitives.py](../../../research/controlled_source_completion/primitives.py)
- [research/controlled_source_completion/ir.py](../../../research/controlled_source_completion/ir.py)
- [research/controlled_source_completion/phase_certificate.py](../../../research/controlled_source_completion/phase_certificate.py)
- [research/controlled_source_completion/phase_precision.py](../../../research/controlled_source_completion/phase_precision.py)

**Planned local artifacts:**

- `results/limitation_program_20261001/A12_run001/protocol.json`
- `results/limitation_program_20261001/A12_run001/denominator_inventory.json`
- `results/limitation_program_20261001/A12_run001/reciprocal_divide_comparison.json`

## A13. Search a bounded exponential degree/segment frontier

**Status:** ready. **Priority:** 3. **Required interfaces:** G0, A07.

**Original limitation:** §3 item 3: degree-12 exponential; §4 Failure 3: compiled exponential dominates; §5 root cause C: polynomial arithmetic.

**Next action:** For the newly proved exponential domain, certify a finite grid of minimax degree/segment choices before emitting the best two complete function candidates; the current Estrin source is the baseline.

**Small implementation steps:**

1. Fix the required absolute error from G2’s arithmetic allocation; without it, perform only an explicitly exploratory error/cost screen.
2. Screen degrees 4, 6, 8, 10 and 12 with 1, 2, 4 and 8 segments using rigorous approximation and coefficient-rounding bounds.
3. Include domain labels, coefficient reads, products, additions, shifts and all cleanup in each candidate estimate.
4. Emit current baseline plus the best two feasible candidates, then compare source depth at frozen caps.

**Alternatives to screen:**

- Piecewise minimax polynomials with static coefficient QROM.
- Taylor baseline and the already-used Estrin dependency arrangement.
- Alternative range reduction or mixed intermediate precision only with explicit conversions and G2 accounting.

**Acceptance:**

- Uniform approximation error is certified over the entire reachable interval, including range-reduction boundaries.
- Finite arithmetic rounding, coefficient quantization, overflow and any barrier-band impact are included under G2.
- The comparison uses whole-function costs; lower degree is not counted while omitting the larger table or selector.
- Adoption of changed polynomial semantics requires G2; optimization of the same polynomial may proceed under G1 alone.

**Stop rule:** Twenty degree/segment pairs in the first screen and at most two new emitted candidates. Stop if all violate error/cap requirements or the full source is resource-dominated.

**On pass:** Adopt a certified whole-function improvement with a new target identifier; re-time the classical comparator on that same target.

**On fail:** Keep the exact existing polynomial source and retain the cost/error frontier for future budgets.

**Existing evidence and verified starting code:**

- [research/controlled_source_completion/ir.py](../../../research/controlled_source_completion/ir.py)
- [research/controlled_source_completion/optimize.py](../../../research/controlled_source_completion/optimize.py)
- [research/controlled_priority_completion/range_joint_arithmetic.py](../../../research/controlled_priority_completion/range_joint_arithmetic.py)
- [manuscript/advantage-frontier-2026-09-23/STAGE_A_RESULTS.md](../../../manuscript/advantage-frontier-2026-09-23/STAGE_A_RESULTS.md)
- [results/limitation_audit_20261001/constant_multiplier_v1/summary.json](../../../results/limitation_audit_20261001/constant_multiplier_v1/summary.json)
- [research/advantage_frontier_20260923/barrier_oracle_depth.py](../../../research/advantage_frontier_20260923/barrier_oracle_depth.py)

**Planned local artifacts:**

- `results/limitation_program_20261001/A13_run001/protocol.json`
- `results/limitation_program_20261001/A13_run001/exponential_approximation_certificate.json`
- `results/limitation_program_20261001/A13_run001/function_frontier.json`

## A14. Bound CORDIC/log-cosine transfer before circuit work

**Status:** conditional. **Priority:** 4. **Required interfaces:** G0, A01, A08.

**Original limitation:** §3 items 1 and 3: log/cosine Gaussian arithmetic; §5 root cause C: alternative arithmetic families.

**Next action:** Compute a charged iteration/add/shift/cleanup resource bound for a reversible cosine on the exact Box-Muller domain; proceed to gates only if it can beat the measured polynomial block.

**Small implementation steps:**

1. Fix cosine’s [0,1] turn domain and a uniform allowed output error; handle periodic endpoints exactly.
2. Derive iteration count, signed branch history, constants, retained state and inverse cost.
3. Use the actually measured A08 or ripple adder costs, not a free shift-add assumption.
4. Emit one small reversible cosine and then a production-width candidate only after the screen passes; log is a separate subsequent screen.

**Alternatives to screen:**

- Piecewise minimax cosine/logarithm with the existing exact coefficient lookup.
- CORDIC cosine as an explicitly new transfer; the cited arcsine circuit does not establish its cost.
- Drop this optimization if a certified A02 loader removes the entire Box-Muller block more cheaply.

**Acceptance:**

- A prospective upper-bound circuit cost is lower than the complete cosine baseline under the same width/error convention.
- An emitted candidate has a uniform approximation certificate, explicit branch/history cleanup and complete inverse.
- The source ledger shows the saving survives integration; any altered numeric function passes G2.
- An ordinary classical CORDIC output or arcsine-paper factor alone does not satisfy acceptance.

**Stop rule:** One cosine feasibility screen and one minimax comparator; emit at most one production candidate. Suspend CORDIC if iteration/history cleanup dominates or A02 removes its use.

**On pass:** Emit and validate the smallest matched cosine, then consider a separate log candidate only if A01 still ranks it highly.

**On fail:** Keep current log/cosine functions and pursue higher-ranked source costs.

**Existing evidence and verified starting code:**

- [research/controlled_source_completion/ir.py](../../../research/controlled_source_completion/ir.py)
- [research/controlled_source_completion/primitives.py](../../../research/controlled_source_completion/primitives.py)
- [docs/limitation_audit_20261001/ARITHMETIC_AND_LOADING.md](../../../docs/limitation_audit_20261001/ARITHMETIC_AND_LOADING.md)
- [results/limitation_audit_20261001/lookup_v2/summary.json](../../../results/limitation_audit_20261001/lookup_v2/summary.json)

**Planned local artifacts:**

- `results/limitation_program_20261001/A14_run001/protocol.json`
- `results/limitation_program_20261001/A14_run001/cordic_cost_screen.json`
- `results/limitation_program_20261001/A14_run001/cosine_certificate.json`

## A15. Preserve the completed exact coefficient-lookup replacement

**Status:** complete. **Priority:** 1. **Required interfaces:** G0.

**Original limitation:** §5 root cause C: QROM/coefficient loading; §6 better compilation.

**Next action:** Register the existing shared-prefix lookup as a completed component and carry its versioned leaf hashes and tests into every new combined-source manifest; do not rerun the already solved 32-row experiment without a code/table change.

**Small implementation steps:**

1. Record all four real table results, including the requested 32x9 log lookup: 3,136 to 420 T gates and 1,600 to 226 T-depth at 724 qubits.
2. Retain exhaustive address/nonzero-output/inverse and reference-entangled phase checks.
3. Check provenance in each new combined manifest; invalidate caches when table values, dimensions or lowering change.

**Alternatives to screen:**

- Historical equality-scan lowering remains a selectable regression baseline.
- SelectSwap or dirty-ancilla QROM is a future conditional screen only for a new table shape or tighter hardware budget.
- Constant/partial-table simplifications are already covered by exact tests.

**Acceptance:**

- The exact function remains out[j] XOR table[address mod 2^bits][j], including signed coefficient words and unspecified-zero rows.
- Every address and borrowed/scratch wire contract is preserved; the existing default uses the shared-prefix lowering.
- Only the measured full-source gain is credited; the 86.61% log-lookup T reduction is not an entire-oracle reduction.

**Stop rule:** No new scientific run is scheduled for this completed component. Reopen only on changed table/contract/backend or a finite SelectSwap screen showing a nondominated resource point.

**On pass:** Reuse the validated component and continue to unsolved entries.

**On fail:** If a new integration breaks its contract, restore the verified leaf and fix the integration before continuing.

**Existing evidence and verified starting code:**

- [research/controlled_source_completion/exact_lookup.py](../../../research/controlled_source_completion/exact_lookup.py)
- [research/controlled_source_completion/primitives.py](../../../research/controlled_source_completion/primitives.py)
- [research/limitation_audit_20261001/test_lookup.py](../../../research/limitation_audit_20261001/test_lookup.py)
- [results/limitation_audit_20261001/lookup_v2/summary.json](../../../results/limitation_audit_20261001/lookup_v2/summary.json)
- [docs/limitation_audit_20261001/EXECUTION_RESULTS.md](../../../docs/limitation_audit_20261001/EXECUTION_RESULTS.md)

**Planned local artifacts:**

- `results/limitation_program_20261001/A15_run001/component_registry.json`

## A16. Extend measured cleanup into a verified dynamic arithmetic backend

**Status:** partial. **Priority:** 3. **Required interfaces:** G0.

**Original limitation:** §3 item 4: uncomputation doubles work; §4 Failure 4: complete controlled source; §5 root cause C: cleanup architecture.

**Next action:** Build one three- or four-bit temporary-AND adder fragment with explicit measurement/feed-forward and verify its complete corrected channel in every branch before attempting compiler integration.

**Small implementation steps:**

1. Use the existing branch-aware MCX harness to specify the intended adder channel, arbitrary output and reference system.
2. Enumerate every measurement branch and compare its corrected Kraus operator to the desired operation up to the correct branch scalar.
3. Include a negative control that omits the phase correction and a logical-inverse/channel composition check.
4. Only after fragment validity, implement a separate dynamic backend rather than placing measurements in Program.undo; charge measurement and feedback rounds in G5.

**Alternatives to screen:**

- Existing five-control MCX fragment already saves 49 to 28 T gates with three feedback rounds.
- Temporary-AND compute/uncompute in arithmetic where the permitted intermediate use conditions hold.
- Keep the fully unitary X/CX/CCX backend when reaction latency or phase conditions make measurement cleanup unattractive.

**Acceptance:**

- Every branch gives the intended coherent map and scratch reset, including superposition and reference entanglement.
- Basis truth tables alone cannot pass; all relative phases and feed-forward corrections are checked.
- T-count savings include forward compute and all corrections; reaction depth and classical latency are reported separately.
- The complete controlled source is adopted only after channel-level fusion/reflection checks in A17 and a physical cost decision.

**Stop rule:** One small adder fragment and one representative unitary-vs-dynamic schedule. Stop compiler integration if any branch violates coherence or the charged dynamic latency is dominated.

**On pass:** Retain a distinct verified dynamic backend and expand one arithmetic leaf at a time.

**On fail:** Keep the validated MCX fragment only; preserve the unitary source and record the first violated temporary-AND use condition.

**Existing evidence and verified starting code:**

- [research/limitation_audit_20261001/experiment_mcx_cleanup.py](../../../research/limitation_audit_20261001/experiment_mcx_cleanup.py)
- [results/limitation_audit_20261001/mcx_cleanup_v1/result.json](../../../results/limitation_audit_20261001/mcx_cleanup_v1/result.json)
- [results/limitation_audit_20261001/mcx_cleanup_v1/mcx5.qasm](../../../results/limitation_audit_20261001/mcx_cleanup_v1/mcx5.qasm)
- [docs/limitation_audit_20261001/FIRST_COMPONENT_RESULT.md](../../../docs/limitation_audit_20261001/FIRST_COMPONENT_RESULT.md)
- [research/controlled_source_completion/primitives.py](../../../research/controlled_source_completion/primitives.py)

**Planned local artifacts:**

- `results/limitation_program_20261001/A16_run001/protocol.json`
- `results/limitation_program_20261001/A16_run001/temporary_and_adder.qasm`
- `results/limitation_program_20261001/A16_run001/branch_channel_checks.json`

## A17. Audit existing fusion and phase-check remaining controlled boundaries

**Status:** audit. **Priority:** 2. **Required interfaces:** G0.

**Original limitation:** §3 item 5: controllability; §4 Failure 4: complete controlled source; §5 root cause F: estimator interface.

**Next action:** Audit which complete estimator schedules already use fused=True, then phase-check a tiny complete compute-controlled-phase-uncompute/reflection iterate and identify any actual duplicate copy boundary.

**Small implementation steps:**

1. Trace current source, phase, normalization, reflection and estimator manifests; distinguish arithmetic-source counts from complete controlled-iterate counts.
2. Use a tiny enumerated source and control in superposition to verify control-zero identity and control-one relative phase/reflection sign.
3. If a redundant boundary exists, remove only that boundary and compare literal emitted gates/resources.
4. Repeat channel-aware checks if measurement arithmetic is introduced; do not credit already-used fusion as a new gain.

**Alternatives to screen:**

- Existing compiler.envelope(fused=True) controls the middle bit phases while leaving financial arithmetic uncontrolled.
- Remove a proved duplicate source/phase copy boundary if one exists.
- A16’s dynamic channel may be fused only after its measurement corrections preserve cancellation.

**Acceptance:**

- Every reported complete-call count states whether it is fused and includes random preparation/inverse, reflection and phase precision.
- Control-zero is identity, control-one equals the intended signed controlled operation, and all scratch is reset.
- Relative phases agree with an independent small matrix/channel construction; global phases on a controlled branch cannot be dropped.
- Retain a code change only if actual emitted duplicate work decreases while G3’s estimator interface remains valid.

**Stop rule:** One schedule audit and one tiny complete phase check. If all eligible boundaries are already fused, close this entry as complete with zero additional speedup.

**On pass:** Freeze the verified controlled-call interface and feed its real cost to G3/G5.

**On fail:** Fix the smallest phase/sign/interface discrepancy before treating any arithmetic improvement as a complete oracle improvement.

**Existing evidence and verified starting code:**

- [research/controlled_source_completion/compiler.py](../../../research/controlled_source_completion/compiler.py)
- [research/controlled_source_completion/envelope.py](../../../research/controlled_source_completion/envelope.py)
- [research/controlled_source_completion/fusion_validation.py](../../../research/controlled_source_completion/fusion_validation.py)
- [research/controlled_source_completion/spectral_validation.py](../../../research/controlled_source_completion/spectral_validation.py)
- [research/controlled_priority_completion/combined_wrappers.py](../../../research/controlled_priority_completion/combined_wrappers.py)

**Planned local artifacts:**

- `results/limitation_program_20261001/A17_run001/protocol.json`
- `results/limitation_program_20261001/A17_run001/fusion_audit.json`
- `results/limitation_program_20261001/A17_run001/controlled_iterate_phase_checks.json`

## A18. Apply paid reversible pebbling to a real financial subgraph

**Status:** partial. **Priority:** 2. **Required interfaces:** G0, A01, A06.

**Original limitation:** §4 Failure 5: retained SSA memory; §5 root cause C: pebbling; §5 root cause E: workspace per parallel lane.

**Next action:** Extract one actual Gaussian-plus-exponential subgraph and emit checkpoint/recompute schedules at 75% and 50% of its measured baseline workspace, using the latest exact leaf library.

**Small implementation steps:**

1. Carry forward the toy evidence as a tradeoff only: 76 to 56 qubits but 15 to 27 leaf calls.
2. Create a subgraph manifest preserving actual input/output semantics and enumerate legal compute/uncompute moves.
3. Schedule both caps, emit every recomputation and cleanup invocation, and replay small/extracted cases.
4. Scale only a successful nondominated schedule to B4x12 before attempting B8x52; keep random input storage in the floor.

**Alternatives to screen:**

- Reversible pebbling with explicit predecessor availability and charged recomputation.
- Block checkpointing or heuristic schedules compared against retaining every intermediate.
- Exact compact storage is complementary, but combined savings must be emitted and measured.

**Acceptance:**

- Every erase has its required predecessors or a valid alternative cleanup; no dead value is overwritten while dirty.
- Inputs and arbitrary outputs match the independent integer target, with all checkpoints and scratch restored.
- Peak width is observed in the emitted schedule and is below the chosen cap; all recomputed T gates/depth are charged.
- Retain width-saving points even if slower, but credit pricing latency only if G5 improves under the physical cap.

**Stop rule:** Two caps and two pebbling heuristics on one real subgraph; at most one B4 full-source integration. Stop scaling if neither point is nondominated or legal cleanup cannot be proved.

**On pass:** Add a width/depth frontier to the combined source and choose the best point under actual physical/parallel budgets.

**On fail:** Keep the toy and compact-storage results separate; document the graph dependency that defeats the attempted cap.

**Existing evidence and verified starting code:**

- [research/controlled_source_completion/compiler.py](../../../research/controlled_source_completion/compiler.py)
- [research/controlled_source_completion/compact_storage.py](../../../research/controlled_source_completion/compact_storage.py)
- [research/limitation_audit_20261001/experiment_pebbling.py](../../../research/limitation_audit_20261001/experiment_pebbling.py)
- [results/limitation_audit_20261001/pebbling_v1/summary.json](../../../results/limitation_audit_20261001/pebbling_v1/summary.json)
- [results/limitation_audit_20261001/constant_multiplier_v1/summary.json](../../../results/limitation_audit_20261001/constant_multiplier_v1/summary.json)

**Planned local artifacts:**

- `results/limitation_program_20261001/A18_run001/protocol.json`
- `results/limitation_program_20261001/A18_run001/subgraph_pebbling_schedules.json`
- `results/limitation_program_20261001/A18_run001/resource_frontier.json`

## A19. Test reversible streaming on the unchanged monitored payoff

**Status:** conditional. **Priority:** 3. **Required interfaces:** G0, A18.

**Original limitation:** §4 Failure 5: path storage; §4 Failure 6: maxima and basket operations; §5 root cause C: path arithmetic.

**Next action:** Build a two-asset/four-date monitored arithmetic-basket verification harness comparing existing SSA evaluation with a reversible current-state/violation-count design on identical finite draws.

**Small implementation steps:**

1. Use barrier_oracle_depth.build and the Stage A target/manifests as the exact source. Keep its guarded log prices, monitored basket threshold, Asian average, discounting and finite rounding; a streaming design must preserve the same sequence-sensitive integer result.
2. Specify that any date's basket >= H knocks out the path (alive is max basket < H), together with the arithmetic basket weights, monitoring dates and payoff average over assets and dates.
3. Use legal update/checkpoint operations; finite multiplication and alive AND updates cannot be assumed invertible.
4. Exhaust a tiny draw grid and replay boundary cases, then measure current-state, sums/counts, history cleanup and loss of prefix parallelism.

**Alternatives to screen:**

- Count barrier violations reversibly, then test count==0 instead of overwriting alive.
- Retain/recompute local barrier decisions under checkpointing.
- Running sums for Asian statistics and block checkpoints for noninvertible finite-price updates; preserve the original parallel-prefix alternative.

**Acceptance:**

- The streaming and SSA circuits return exactly the same discrete payoff on all harness inputs, including equality at the barrier.
- Workspace and input restoration hold; lost information is retained or recomputed, never silently erased.
- Measured peak width decreases and the complete work/depth penalty is explicit.
- The harness does not replace B8x52 as the pricing task; full scaling requires an emitted matching source and G5 comparison.

**Stop rule:** One two-asset/four-date harness and two checkpoint placements. Stop full scaling if the width saving is dominated after cleanup or the serial-depth penalty makes its physical-cap frontier worse.

**On pass:** Integrate the best design into a full unchanged-contract source, compare with A18, and retain only measured nondominated points.

**On fail:** Preserve SSA/prefix construction and the exact harness as a negative result; identify whether barrier history or irreversible finite updates caused the failure.

**Existing evidence and verified starting code:**

- [research/controlled_source_completion/finance.py](../../../research/controlled_source_completion/finance.py)
- [research/controlled_source_completion/ir.py](../../../research/controlled_source_completion/ir.py)
- [research/controlled_source_completion/compiler.py](../../../research/controlled_source_completion/compiler.py)
- [results/limitation_audit_20261001/pebbling_v1/summary.json](../../../results/limitation_audit_20261001/pebbling_v1/summary.json)
- [research/advantage_frontier_20260923/barrier_oracle_depth.py](../../../research/advantage_frontier_20260923/barrier_oracle_depth.py)
- [research/frontier_completion_20260927/stage_a.py](../../../research/frontier_completion_20260927/stage_a.py)

**Planned local artifacts:**

- `results/limitation_program_20261001/A19_run001/protocol.json`
- `results/limitation_program_20261001/A19_run001/streaming_harness_target.json`
- `results/limitation_program_20261001/A19_run001/streaming_vs_ssa.json`

## A20. Test arithmetic-free loading on the actual sum-of-exponentials threshold

**Status:** conditional. **Priority:** 5. **Required interfaces:** G0, A05, A07.

**Original limitation:** §5 root cause C: arithmetic-free multi-asset path oracle; §4 Failure 6: arithmetic-basket barrier; §6 untested algorithmic routes.

**Next action:** Write and certify the two-asset/one-date arithmetic-basket predicates in log coordinates, preserving barrier >= H as knock-out, alive < H, and the separate positive-payoff strike test > K; then screen a sum-of-exponentials block encoding against two explicit exponential circuits.

**Small implementation steps:**

1. Freeze A = w1*exp(x1)+w2*exp(x2). For the monitored barrier, A >= H knocks out and alive means A < H; the positive-payoff strike test is separately A > K. Preserve these ties from the frozen contract and explicitly reject replacing A by an inequality on x1+x2 or a geometric basket.
2. Account for preparation, block-encoding normalization, polynomial degree, threshold approximation, amplification and inverse.
3. Certify the near-boundary band contribution and matched finite/continuous law error before emission.
4. Emit one smallest instance only if the charged screen is competitive; preserve the existing finite tilted-law sampler result without claiming it is coherent preparation.

**Alternatives to screen:**

- Keep truly monotone single-asset comparisons in log space.
- Integration-based loading for separable payoffs, including normalization and scalar estimator extraction.
- QSP/block encoding for a weighted sum of exponentials as a new construction, not an already supplied free oracle.

**Acceptance:**

- The construction implements the arithmetic basket with the frozen barrier ties (knock-out at A >= H, alive at A < H), the separate positive-payoff strike test A > K, and the same normalization as the explicit baseline.
- Approximation error is uniformly bounded away from the threshold, and probability-weighted boundary error fits the G2 allocation.
- Complete scalar-estimation source cost is lower at the same accuracy/cap; an amplitude-loading module factor alone cannot pass.
- Gaussian and path construction costs remain charged; the cited autocallable method is not credited with removing them.

**Stop rule:** One two-asset/one-date mathematical construction and one full cost screen; emit at most one candidate. Stop if a missing normalization/comparison oracle is needed or the candidate is dominated.

**On pass:** Retain the certified small oracle and test one additional date before any multi-asset/path extrapolation.

**On fail:** Record the exact missing operation or cost term and keep explicit basket arithmetic; do not turn the failure into a no-go theorem for every arithmetic-free method.

**Existing evidence and verified starting code:**

- [docs/limitation_audit_20261001/ARITHMETIC_AND_LOADING.md](../../../docs/limitation_audit_20261001/ARITHMETIC_AND_LOADING.md)
- [research/controlled_source_completion/ir.py](../../../research/controlled_source_completion/ir.py)
- [research/limitation_audit_20261001/experiment_bounded_probabilities.py](../../../research/limitation_audit_20261001/experiment_bounded_probabilities.py)
- [results/limitation_audit_20261001/bounded_probabilities_v1/summary.json](../../../results/limitation_audit_20261001/bounded_probabilities_v1/summary.json)

**Planned local artifacts:**

- `results/limitation_program_20261001/A20_run001/protocol.json`
- `results/limitation_program_20261001/A20_run001/arithmetic_basket_log_threshold.md`
- `results/limitation_program_20261001/A20_run001/block_encoding_cost_screen.json`

The machine-readable records in [arithmetic.json](arithmetic.json) contain the same decisions and can drive a local run queue. They are a plan, not a claim that the future circuits or certificates already exist.
