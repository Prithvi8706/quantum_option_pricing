# Arithmetic, loading and reversible storage: atomic limitation audit

Research screen dated **1 October 2026**. This memo audits the implementation claims in [WHY_NO_ADVANTAGE.md](../../manuscript/advantage-frontier-2026-09-23/WHY_NO_ADVANTAGE.md), especially section 3, Failures 1/4/5/6, root cause C, and the compilation row of section 6. The newer [STAGE_A_RESULTS.md](../../manuscript/advantage-frontier-2026-09-23/STAGE_A_RESULTS.md) takes precedence for emitted knock-out source costs.

**Several small obstacles already have solutions elsewhere in quantum computing. None of the sources checked here establishes the required end-to-end advantage for this project's contracts.** In particular, Box-Muller, linear-depth addition, seven-T expansion of every Toffoli, symmetric-cost uncomputation, and retaining every intermediate are implementation choices. Their replacement is a concrete research programme, not evidence that the full gap is closed.

This is a bounded primary-source screen, not an exhaustive literature classification. Papers and their linked full text were opened on 1 October 2026. The search covered quantum arithmetic, quantum simulation state preparation, tensor networks, reversible compilation, QROM, CORDIC and quantum finance. It included 2025/2026 results. No new circuit or pricing experiment was executed for this memo. Proposed tests below have prospective pass/fail conditions.

## What the existing implementation actually establishes

Stage A emits a **clean financial source**, with input preserved and workspace restored, for a particular discrete law. B8x52 uses 6,393,144 scheduled T-layers, 7,458,042,774 T gates and 4,460,490 logical qubits in the unrestricted wave schedule. These are not lower bounds. The historical 789.448-layer tenfold budget is conditional on historical classical timing and a hypothetical estimator constant; it is not a certified current crossover target.

The following inspected code explains some of the cost:

- [ir.py](../../research/controlled_source_completion/ir.py): `Graph.__init__` sets one global width `f + integer_bits`, normally 40 + 32. `interpolate` uses coefficient tables and polynomial arithmetic; `exp` uses range reduction and a degree-12 polynomial. Stage A subsequently applies its Estrin optimization.
- [primitives.py](../../research/controlled_source_completion/primitives.py): `lookup` constructs an equality flag separately for every table row, writes that row, then erases the flag. `build('add')` itself computes, copies and uncomputes a temporary sum. `gate_resources` uses an exact seven-T Toffoli expansion.
- [compiler.py](../../research/controlled_source_completion/compiler.py): `compile_graph` gives all SSA values permanent storage and doubles forward leaf resources for source cleanup. `envelope` already has a fused compute-phase-uncompute option; it does not control every arithmetic gate.
- [range_joint_arithmetic.py](../../research/controlled_priority_completion/range_joint_arithmetic.py): range/error certificates exist for particular earlier compound sources. Stage A explicitly does not transfer those certificates to knock-outs.

Here **solved as a primitive** means a construction or theorem exists for the stated subproblem. **Conditional here** means its integration and resource benefit remain unverified. **Local existing** means the repository already implements part of the idea. These statuses must not be collapsed into “pricing solved”.

## A01. Coherent randomness is being conflated with Gaussian conversion

**Original location:** section 3, numbered item 1; Stage A's separate uniform-Hadamard count.

**Small claim:** The source needs a reproducible coherent distribution, but creating uniform random bits and transforming them into Gaussian values are different costs. Hadamards prepare the uniform superposition; the expensive part of this implementation is the deterministic map into Gaussian samples. B8x52's 14,976 uniform Hadamards are not its multi-million-layer bottleneck.

**Alternative:** Prepare Gaussian amplitudes directly on a numerical grid, then perform path arithmetic on the grid index. This changes the finite source representation while keeping the intended continuous Gaussian law as the target. A QSVT construction for this task is available in [McArdle, Gilyen and Berta](https://arxiv.org/html/2210.14892v2); its final publication is [PRL 136, 240603 (2026)](https://journals.aps.org/prl/abstract/10.1103/ntvs-c48s).

**Status:** Uniform preparation is local existing; direct Gaussian preparation is solved as a primitive and conditional here. It is incorrect to infer that removing Box-Muller makes the entire source free.

**Next small test:** Draw a cost ledger with four separate rows: uniform preparation, Gaussian conversion/preparation, correlation, and path/payoff. Pass when every archived node belongs to exactly one row and the sums reproduce the emitted source accounting. This is an accounting result, requiring no new heavy compilation.

## A02. Box-Muller's log, square root and cosine are not mandatory

**Original location:** section 3, item 1; root cause C.

**Small claim:** The current loader pays for an inverse radial transform and a trigonometric function for each constructed normal. This is a property of the chosen sampler.

**Alternative and evidence:** The QSVT state-preparation paper above supplies a Gaussian preparation theorem, an explicit bounded-polynomial construction and amplification costs. The method uses three ancillary qubits for definite-parity functions; a general version uses four. Its cost depends on approximation degree and the filling fraction. These are accounted quantities, not a free Gaussian oracle. Its illustrative Gaussian resource table is at a different precision and grid from this project and is not a direct replacement cost.

**Applicability:** Prepare **square roots of probability masses**. Confusing a Gaussian amplitude profile with the desired Gaussian probability profile changes the variance. Account for the physical grid scaling, truncation and normalization, and construct both preparation and inverse. The same law must also be available to the classical comparator.

**Status:** A real alternative exists; the project's calibrated loader is unverified.

**Next small test:** For one scalar normal, freeze a truncation interval, grid and loader error allowance. Compile one QSVT preparation/inverse pair and the current scalar Box-Muller block to the same gate and timing model. Pass only if the induced distribution meets that allowance and either depth or width improves without an unacceptable increase in the other resource. Carry this result forward before building 468 copies.

## A03. “Efficiently integrable” does not make recursive state loading cheap enough

**Original location:** section 3's “equivalent loader”; root cause C's state-loading alternatives.

**Small claim:** Replacing Box-Muller by Grover-Rudolph is useful only after paying for its conditional probability integrals and rotation angles at the required accuracy.

**Alternative:** For an analytic normal distribution, use certified deterministic approximations to interval probabilities, precomputed angle structure, or the direct preparation in A02. Do not estimate each required integral by fresh Monte Carlo and label its cost negligible.

**Evidence:** [Herbert's analysis](https://arxiv.org/html/2101.02240v1) identifies how numerical integration used inside Grover-Rudolph can consume the proposed Monte Carlo speedup. Its proof should not be expanded into a prohibition on all analytic Gaussian loaders; its own discussion points to other preparation methods.

**Status:** The hidden-integration objection is understood. A cheaper recursive loader for these exact domains is conditional here.

**Next small test:** Implement just the first two conditional-angle levels, including certified approximation and synthesized rotations. Pass when the angle error and complete cost are bounded as functions of precision; fail the “cheap loader” proposal if it needs an unpriced numerical-integration oracle. This closes one assumption before choosing a full loader architecture.

## A04. Tensor-network Gaussian loading offers short circuits, with an accuracy tradeoff

**Original location:** section 3, item 1; section 6's untested compilation opportunities.

**Small claim:** Smooth one-dimensional distributions can have compressed representations that avoid explicit inverse-transform arithmetic.

**Alternative and evidence:** [Iaconis, Johri and Zhu (2024)](https://arxiv.org/html/2303.01562v2), published in [npj Quantum Information](https://www.nature.com/articles/s41534-024-00805-0), construct normal-distribution states using matrix product states and demonstrate up to 20 qubits on trapped-ion hardware. Their finite-depth approximation has error from both the distribution approximation and circuit compression. They explicitly discuss limitations in accuracy scaling.

**Applicability:** This is a candidate for a small scalar-normal loader. A visually convincing histogram or high average fidelity does not certify penny-level path-dependent pricing after hundreds of draws. Tensor-network compressibility also offers the classical side possible benefits; it is not by itself a quantum advantage argument.

**Status:** Demonstrated distribution loading; high-accuracy integration here is unverified.

**Next small test:** At fixed scalar grid, compare QSVT and MPS loaders against the same exact target vector at three progressively tighter error targets. Include classical circuit-generation time and rotation synthesis. Pass only if a certified distance bound reaches the per-coordinate allowance; otherwise retain MPS as a low-accuracy candidate rather than claiming it solves loading.

## A05. Hundreds of independent normals need not be one monolithic loading problem

**Original location:** section 3's count of 468 Gaussians; Failure 5's width issue.

**Small claim:** The path distribution is built from scalar independent sources plus a model-specific correlation transform. It is unnecessary to prepare an arbitrary state over the entire joint grid by a generic loader.

**Alternative:** Tensor-product scalar loaders, correlated factors represented through the existing model structure, and reuse of one scalar-loader design. This is a proposed integration of A02/A04 with the current model, not a claim from those papers that the full basket oracle is solved. Removing factors or reducing PCA rank is **not** an exact optimization; it needs a separately budgeted model approximation.

**Applicability:** For product preparation with coordinate trace-distance errors `delta_j`, a conservative bound on joint trace distance is `sum_j delta_j`. For a payoff bounded in `[0,M]`, the induced expectation error is at most `M` times the resulting total-variation distance. These elementary bounds provide a safe starting point; a sharper contract-specific bound may materially reduce the required loader precision.

**Status:** Product construction is straightforward; the useful error allocation is unverified.

**Next small test:** Solve the error allocation for **two** factors, then extrapolate the proved bound to 468. Pass if the proposed scalar accuracy composes within the financial error ledger; fail if the only justification is that each marginal looks close.

## A06. Forty fractional bits and 32 integer bits for every value are design choices

**Original location:** section 3, item 2; root cause C; Stage A Q6-Q10.

**Small claim:** Uniform 72-bit storage and arithmetic need not be optimal for an error tolerance stated in dollars. Flags, indexes, polynomial intermediates, prices and exponents do not share the same range or error sensitivity.

**Alternatives:** Per-node fixed-point widths; exact narrow Boolean/index registers; range-specific scaling; mixed precision across approximation stages; or a reversible floating-point representation. [Quantum circuits for floating-point arithmetic](https://arxiv.org/html/1807.02023v1) gives actual addition and multiplication circuits, so floating point is not excluded by reversibility. It also brings exponent alignment and normalization costs; fewer mantissa bits alone is not a saving certificate.

**Applicability:** The local IR encodes all outputs with the same `w`, even flags. Narrowing exact flags/indexes is a less ambiguous first step than reducing financial precision. Per-node fraction changes need explicit conversions and rounding semantics.

**Status:** Alternative representations exist; mixed-width compilation is not established for Stage A.

**Next small test:** Add an analysis-only bit-width annotation pass for Boolean and index nodes. Pass if required active widths follow from operation semantics on every input and the projected live-bit count decreases. Follow with one exact narrow flag/comparator emission before trying a global f=24 change.

## A07. Safe range narrowing is a proof obligation, not a typical-path observation

**Original location:** Failure 5's range-specialized multipliers; Stage A's prohibition on borrowing unrelated range certificates.

**Small claim:** Generic widths pay for values that may be unreachable, but a sampled minimum/maximum is insufficient to remove those bits safely.

**Alternative:** Propagate intervals or stronger affine/relational bounds on the finite input domain, and separately bound any deliberate Gaussian tail truncation. Use dimensional scaling to keep arithmetic ranges small. [Bhaskar et al.](https://arxiv.org/html/1511.08253v1) illustrates arithmetic design with explicit truncation/error guarantees; the local range-certificate module offers a project-specific starting point.

**Applicability:** Polynomial coefficients can be large even when their final sum is small. Barrier decisions require an additional discontinuity argument: if an approximation to a monitored quantity has error at most `eta`, a classification change can occur only in the `eta` band around the barrier. Bound the probability and payoff weight of that band rather than assuming smooth payoff error propagation.

**Status:** Range specialization is local existing for earlier sources; transfer to this contract is unverified.

**Next small test:** Certify the input and output interval of one B4x12 exponential and its range-reduction integers. Pass if all coefficient, product and shift ranges are bounded with no unbudgeted overflow. A failure is useful: it identifies the single node requiring a wider representation or a tail allowance.

## A08. Addition need not have the listed 1,152-layer depth

**Original location:** section 3's leaf-cost table, add/subtract row.

**Small claim:** That row measures a selected implementation and cleanup convention, not an addition lower bound.

**Alternative and evidence:** [Draper, Kutin, Rains and Svore's carry-lookahead adder](https://arxiv.org/html/quant-ph/0406142v1) has logarithmic depth with linear ancillary space. It targets carry propagation, precisely the dependence that parallelizing separate leaf calls cannot remove. Different variants implement in-place or out-of-place and modular addition, so the interface must match the repository.

**Applicability:** This is likely a useful logical-depth candidate at 72 bits. It can use more ancillas, connectivity and simultaneous magic states. Neither asymptotic depth nor T count determines physical runtime alone.

**Status:** The circuit-level linear-depth obstruction is solved; the matching clean-XOR leaf and physical benefit are conditional here.

**Next small test:** Emit a 72-bit clean-XOR carry-lookahead leaf matching existing `build('add')`, including arbitrary initial output. Exhaustively check small widths and replay carry-chain/signed-wrap cases at 72 bits. Pass if semantics and cleanup match and the depth-width tradeoff beats the current leaf under a frozen ancilla cap. Report the achieved factor, not an asymptotic promise.

## A09. Quadratic multiplication is not fundamental, but Karatsuba is not an automatic 72-bit win

**Original location:** section 3, item 2; root cause C's schoolbook multiplication.

**Alternative and evidence:** [Gidney's reversible Karatsuba construction](https://arxiv.org/html/1904.07356v1) achieves linear space with subquadratic gate complexity. Its published implementation crossed schoolbook at roughly **10,000 bits**, and the author did not optimize constants. That is strong evidence against simply substituting its asymptotic exponent into a 72-bit estimate. It does not prove that every future Karatsuba implementation loses at 72 bits.

**Applicability:** First optimize the actual signed, fixed-point, truncated output product rather than a larger integer product. Parallel partial-product reduction and fast adders are other candidates, with width costs. Preserve negative-number rounding and discarded-bit carry effects.

**Status:** Subquadratic reversible multiplication is solved asymptotically; a practical win at this width is unverified.

**Next small test:** Compare emitted gate counts at 24, 40 and 72 active bits for the existing truncated multiplier and one alternative using identical output bits and signs. Pass only on measured resources with the same interface. Reject a claimed benefit that counts a full product on one side and a truncated product on the other.

## A10. Multiplication by a constant and squaring deserve separate circuits

**Original location:** section 3's generic multiply discussion; root cause C.

**Small claim:** General products, squares and fixed-constant products have different structure. Treating all three as an interchangeable “multiply” obscures opportunities and can also undercount expensive calls.

**Alternative:** Use signed-digit/addition-chain constant products; a dedicated square exploiting symmetric partial products; and constant propagation before arithmetic emission. The repository already has a `cmul` operation and constant folding, so these are refinements, not wholly missing features. [Heavey's 2025 arithmetic study](https://arxiv.org/html/2504.19626v1) gives distinct multiplication and squaring constructions with T-count and active-volume accounting.

**Applicability:** For a fixed-point product, changing the order of shifts and additions can change truncation. A smaller circuit must compute the intended finite function or supply an error proof.

**Status:** Specialized primitives exist; further savings beyond local specialization remain conditional.

**Next small test:** Count repeated coefficients and exact self-products in one optimized graph. Select the single most expensive constant product and compare a signed-digit lowering against its existing leaf. Pass when exact integer results, clean workspace and cost improvement all hold, including negative inputs at range endpoints.

## A11. The 225,193-layer square root is not the cost of all reversible square roots

**Original location:** section 3's square-root row; Failure 1's Heston-step bottleneck.

**Alternatives:** Digit-by-digit/non-restoring square root, Newton reciprocal-square-root with normalization and seed lookup, and algorithmic removal through direct Gaussian preparation. The removal helps Box-Muller but does not remove Heston's state-dependent square root. [Bhaskar et al.](https://arxiv.org/html/1511.08253v1) provides numerical-function circuits with worst-case error guarantees. [Heavey, section 4.1](https://arxiv.org/html/2504.19626v1) updates a non-restoring construction and separately counts reaction depth.

**Applicability:** An integer square-root circuit returning root and remainder is not yet the clean-XOR fixed-point interface used locally. Count input scaling, extra fractional bits, copying and erasing the remainder. Newton methods need a safe zero/small-input branch, especially for Heston near zero variance.

**Status:** Several solved primitives; no matched local cost result.

**Next small test:** Freeze one input domain and requested output accuracy; compare the current leaf and a non-restoring implementation including remainder cleanup. Pass if complete clean-leaf cost improves. Separately test zero, one quantum of input, and values immediately around perfect squares. Do not substitute a quoted T count for the repository's T depth.

## A12. Long division can sometimes become reciprocal approximation plus multiplication

**Original location:** section 3's 398,256-layer divide row; controlled-source phase arithmetic.

**Small claim:** Local `divide` uses restoring unsigned division. `Graph.div` guards its denominator, but its semantics and reachable range must be preserved.

**Alternative and evidence:** Use exponent normalization, a seed table, then Newton reciprocal iterations; multiply the numerator by that reciprocal. [Bhaskar et al., reciprocal section](https://arxiv.org/html/1511.08253v1), gives the numerical framework. Constant or power-of-two denominators can instead use specialized arithmetic; the compiler may already fold some cases.

**Applicability:** If the quotient must exactly equal the existing truncated integer division, an approximate reciprocal needs a correction step. If approximated arithmetic is allowed, propagate its error into the payoff/phase ledger. Very small denominators can destroy a naïve uniform bound.

**Status:** Conditional replacement; neither exact-semantic benefit nor approximate-financial benefit established here.

**Next small test:** Inventory division denominators and prove their minimum positive value. Select one bounded interval away from zero, implement one reciprocal-based divide, and compare against the exact integer quotient. Pass either with exact correction or a proved error below a preassigned allowance. Keep those two meanings of pass separate.

## A13. Degree-12 exponential evaluation is not a certified optimum

**Original location:** section 3, item 3; Failure 3's expensive compiled exponential.

**Alternatives:** Minimax rather than Taylor approximation, more/fewer subintervals, low-degree interpolation with QROM coefficients, a different range reduction, and mixed-precision intermediate products. [Haner, Roetteler and Svore](https://arxiv.org/html/1805.12445v1) supplies a quantum piecewise-function compiler using Remez approximation and explicit register/depth tradeoffs. The project already uses piecewise functions and Stage A already uses Estrin; neither should be counted as a fresh improvement.

**Applicability:** A lower polynomial degree can require a larger lookup table. Estrin reduces dependency depth but can increase work/storage. Compare the sum of domain labeling, table reads, products, additions, shifts and cleanup.

**Status:** Established design space; the optimum on this exact domain is unverified.

**Next small test:** Freeze one reachable exponential interval and absolute error allowance. Generate a small grid of degree/segment choices and certified approximation errors before emitting gates. Emit only the best two candidates plus the current baseline. Pass when the full leaf improves on a width-depth frontier while respecting the same numerical error budget.

## A14. Polynomial logarithm/trigonometry is not the only arithmetic family

**Original location:** section 3, item 1 and item 3; root cause C.

**Alternatives:** Piecewise minimax, specialized power/reciprocal identities, or shift-add iterative algorithms. [Quantum CORDIC — Arcsine on a Budget](https://arxiv.org/html/2411.14434v2) is a concrete quantum adaptation from the digital-signal-processing family, including a numerical-to-amplitude application. It implements arcsine; it is **not** evidence that an equally good reversible cosine or logarithm is ready for this source.

**Applicability:** A CORDIC-derived cosine/logarithm is a research transfer candidate, competing with the existing small coefficient tables. Arithmetic without general multipliers may still contain long sequential chains, sign history and cleanup. The relevant tradeoff can favor lower T count but worse latency.

**Status:** Arcsine construction exists; transfer to the current Box-Muller functions is unverified. Removing Box-Muller in A02 may dominate optimizing it.

**Next small test:** First screen total add/shift iteration counts on the actual cosine domain and precision. Proceed to emission only if that upper-bound cost can beat the existing cosine block under the same carry architecture. Pass requires a uniform approximation bound and a complete inverse; a classical CORDIC output alone is not the quantum prototype.

## A15. Existing lookup circuits can be replaced without changing the financial law

**Original location:** root cause C; Stage A's actual-node-parameter/table binding.

**Small claim:** QROM cost is real, but this implementation's row-by-row equality construction is not the only circuit for the exact same table.

**Alternative and evidence:** [Low, Kliuchnikov and Schaeffer](https://arxiv.org/html/1812.00954v2), published in [Quantum (2024)](https://quantum-journal.org/papers/q-2024-06-17-1375/), gives SelectSwap data lookup with a tunable space/non-Clifford tradeoff. Unary-iteration style selection and common-control sharing should also be compared. This is static compiled read-only data, not an assumption of free QRAM.

**Applicability:** The local coefficient tables have 32, 64 or 256 addresses and several output words. Address width is small enough for exhaustive address verification. Dirty-qubit techniques require restoration for arbitrary, possibly entangled, borrowed states.

**Status:** Solved lookup constructions; integration and net benefit unverified. This is a particularly clean first compiler experiment because it can preserve every output bit.

**Next small test:** Replace only the 32-row logarithm coefficient-table loader. Exhaust every address with nonzero output registers, check inverse cleanup and any borrowed-qubit restoration, then compare T count, T depth, Clifford depth and peak width. Pass if it computes `out XOR table[address]` exactly and improves at least one resource without exceeding a frozen cap. Do not claim an entire-oracle factor from the table's factor.

## A16. Cleanup is required; paying the same T cost twice is not

**Original location:** section 3, item 4 (“doubles the work”); Failure 4; local compiler's exact doubling.

**Alternative and evidence:** [Gidney's temporary logical AND](https://arxiv.org/html/1709.06648v3) costs four T gates to compute and zero T gates to erase using measurement and a conditional Clifford correction. The paper also gives an out-of-place adder with T-free uncomputation. This disproves a universal equality between forward and inverse T cost, under the construction's conditions.

**Applicability:** Garbage that encodes which path occurred cannot simply be measured and discarded. Phase corrections and the allowed intermediate uses of temporary values are essential. The current X/CX/CCX basis simulator cannot verify relative phases or measurement branches. Reaction latency must be counted even when erasure has zero T count.

**Status:** Primitive improvement is solved; whole-source substitution is conditional here.

**Next small test:** Implement one 3- or 4-bit temporary-AND adder fragment in a phase-aware simulator. Check coherent superpositions and every measurement branch after feed-forward, with an arbitrary reference register where practical. Pass if the corrected channel equals the intended coherent operation and scratch resets. Basis truth tables alone cannot pass this test. The companion [first component result](FIRST_COMPONENT_RESULT.md) records the separate investigation of the underlying AND-cleanup identity; that smaller identity does not certify an entire adder or source substitution.

## A17. Controllability does not require controlling all financial arithmetic

**Original location:** section 3, item 5; Failure 4's controlled-source schedule.

**Small claim:** If a computation has the form `F inverse · controlled phase · F`, only the middle phase must depend on the estimator control. When the control is zero, the computation and its inverse cancel. This is an elementary circuit identity, subject to the correct signs and phase convention.

**Local evidence:** `compiler.envelope` explicitly computes the financial and angle graphs without control and controls the bit phases. Its fused option avoids extra clean-copy source invocations. Its reflection includes the external-control sign that a controlled operation cannot discard as a global phase.

**Alternatives:** Extend fusion across source/phase interfaces and select a compatible estimator envelope. Temporary arithmetic from A16 can be considered, but cancellation must hold as a channel including measurement corrections, not merely as basis values.

**Status:** Much of this solution is **already local existing**. It cannot be multiplied again into a future speedup forecast.

**Next small test:** Audit which reported schedule uses `fused=True`, identify any remaining duplicate copy/cleanup boundaries, and phase-check a tiny complete controlled iterate with control in superposition. Pass if the control-zero branch is identity and control-one branch has the exact intended relative phase, with lower emitted work where a duplicate boundary was removed.

## A18. Millions of permanent SSA qubits are not a workspace lower bound

**Original location:** Failure 5; Stage A's width table and explicit SSA-storage qualification.

**Small claim:** Limiting how many leaves run simultaneously is not the same as freeing dead intermediates. Current schedules retain each SSA value until final cleanup.

**Alternative and evidence:** [Meuli et al.'s reversible pebbling compiler](https://arxiv.org/html/1904.02121v1) chooses recomputation/uncomputation strategies under a memory limit; its [Caterpillar documentation](https://github.com/gmeuli/caterpillar/blob/master/docs/qmmanagement.rst) exposes the same problem. This imports techniques from logic synthesis and quantum cryptographic circuit compilation.

**Applicability:** A liveness analysis alone is insufficient: erasing a value requires its predecessors or an alternative valid cleanup. Recomputing predecessors saves width but costs depth/work. The complete random input register may remain live and places its own floor on width.

**Status:** Memory-management methods exist; the project's width-depth frontier is unmeasured.

**Next small test:** Extract one Gaussian-plus-exponential subgraph and solve/heuristically schedule it under two explicit workspace caps. Emit and replay both compute/uncompute schedules. Pass when all outputs match and the lower peak width is achieved in emitted operations, with recomputation fully charged. Then scale to the whole graph; do not extrapolate a fixed width factor blindly.

## A19. Path payoffs can use streaming statistics, but reversible overwrite needs design

**Original location:** Failure 5's storage issue; Failure 6's path maximum and basket operations.

**Small claim:** A classical monitored knock-out evaluator needs current prices and an alive flag, not all historical prices simultaneously. An Asian needs accumulated sums. The quantum source's permanent path history is partly a compilation choice.

**Alternative:** Use block checkpointing, reversible running sums, and a reversible representation of barrier status, informed by the pebbling framework in A18. This is a proposed domain-specific design rather than a paper proving a result for this contract.

**Applicability:** Updating `alive = alive AND survived` overwrites information and is not directly reversible. Retain or reconstruct the lost information, or reversibly compute a count of violations and test for zero. Finite-precision path updates may also fail to be invertible. A sequential streaming circuit may sacrifice the parallel-prefix depth advantage already used locally.

**Status:** Plausible conditional width reduction; no complete implementation or speedup established.

**Next small test:** Build a two-asset, four-date exact discrete knock-out source with one running sum/current-state design and one existing SSA design. Use the identical draws and finite payoff semantics. Pass when final payoff and clean inverse match, peak width decreases, and the depth/work penalty is explicitly measured. Keep this small workload solely as a verification harness; the original B8x52 contract remains the target.

## A20. Removing payoff arithmetic is possible for some structures; the basket sum remains the test

**Original location:** root cause C's arithmetic-free route and reference to arXiv:2507.19039.

**Evidence and necessary refinement:** [Autocallable Options Pricing with Integration-Based Exponential Amplitude Loading](https://arxiv.org/html/2507.19039v1) performs comparisons in log-return space and replaces an arithmetic conversion to returns with integration-based loading. Its reported approximately 50-fold improvement is for an amplitude-loading subroutine. It still prepares Gaussians and accumulates log returns. Thus the foundation document should say that it does not eliminate the current basket path construction; saying it never touches conversion/path arithmetic is too broad.

**Alternatives:** Keep monotone comparisons in log space; use integration-based amplitude loading when the payoff separates; or build a QSP/block-encoding representation for a sum of exponentials. The last is a new construction to investigate, not a supplied oracle. A barrier on a sum of asset prices is not equivalent to a comparison on the sum of their logs. Replacing an arithmetic basket with a geometric basket would change the contract.

**Status:** Specific payoff-loading removal exists; the multi-asset monitored arithmetic-basket implementation remains unverified.

**Next small test:** Start with two assets and one date. Write the exact arithmetic-basket threshold in log coordinates, then attempt a full block encoding or loading construction including normalization, comparison approximation and scalar-estimation interface. Pass only if it matches that threshold with a certified near-boundary error allowance and costs less than the explicit two-exponential circuit. Failure pinpoints the missing operation instead of dismissing all arithmetic-free methods.

## Proposed order: close one small question at a time

The first **exact-semantics** experiment should be A15's coefficient-table loader or A08's adder. They admit narrow interfaces, small exhaustive checks and a direct comparison to current emitted leaves. The first **distribution-changing** experiment should be A02's single-normal loader, after an explicit A05 error allocation. The first **storage** experiment should be A18 on one subgraph, then A19 on a short verified path.

Before using any approximate arithmetic or new distribution to support a price claim, close the Stage A financial-law bridge: barrier flips, tail/grid error and the continuous contract's total error allocation. Small prototypes can proceed independently, but they cannot retroactively certify the archived source.

The statement in section 6 that remaining known compilation levers are worth approximately 100 times should be treated as an unverified estimate unless supported by a compatible emitted combination. Factors for lower width, QROM, adders, QSVT loading and uncomputation overlap; multiplying them would double-count some changes. Conversely, the archived failed implementations do not prove a 100-fold ceiling on all future compilation.

## Source register and checks

All source records below were checked on **1 October 2026**. Full text was opened through the linked arXiv HTML. The npj publisher page failed to open through the browser tool, so the complete arXiv v2 was used; publisher metadata was available in search. The PRL publication record was opened separately. Dates distinguish initial preprint from final publication; a recent crawl date is not a publication date.

| Source | Verified scope used here | Important boundary |
|---|---|---|
| [McArdle, Gilyen, Berta, arXiv:2210.14892v2](https://arxiv.org/html/2210.14892v2); [PRL 2026](https://journals.aps.org/prl/abstract/10.1103/ntvs-c48s) | QSVT state preparation; Gaussian theorem; synthesis/amplification costs | Scalar preparation, not full basket pricing |
| [Herbert, arXiv:2101.02240](https://arxiv.org/html/2101.02240v1) | Cost of numerical integration inside Grover-Rudolph | Do not turn it into an all-loader impossibility theorem |
| [Iaconis, Johri, Zhu, full text](https://arxiv.org/html/2303.01562v2), npj QI 2024 | MPS normal loading and hardware demonstration; accuracy discussion | Does not certify this project's aggregate path bias |
| [Haner et al., arXiv:1807.02023](https://arxiv.org/html/1807.02023v1) | Reversible floating-point addition/multiplication | Representation change is not automatically cheaper |
| [Bhaskar et al., arXiv:1511.08253](https://arxiv.org/html/1511.08253v1), QIC 2016 | Reciprocal, root, log and finite-error arithmetic framework | Interface and error ledger must be matched |
| [Draper et al., quant-ph/0406142](https://arxiv.org/html/quant-ph/0406142v1), QIC 2006 | Logarithmic-depth carry lookahead | Width, routing and factory costs remain |
| [Gidney, arXiv:1904.07356](https://arxiv.org/html/1904.07356v1) | Linear-space Karatsuba; reported crossover | Asymptotic result is not a 72-bit win |
| [Heavey, arXiv:2504.19626v1](https://arxiv.org/html/2504.19626v1), 2025 preprint | Updated arithmetic and reaction/active-volume accounting | No matched clean-source integration here |
| [Haner, Roetteler, Svore, arXiv:1805.12445](https://arxiv.org/html/1805.12445v1) | Piecewise approximation, Remez and storage tradeoffs | Existing local piecewise/Estrin work already counts |
| [Quantum CORDIC, arXiv:2411.14434v2](https://arxiv.org/html/2411.14434v2) | Concrete quantum arcsine algorithm | Cosine/log transfer remains a research hypothesis |
| [Low, Kliuchnikov, Schaeffer, arXiv:1812.00954v2](https://arxiv.org/html/1812.00954v2), Quantum 2024 | SelectSwap lookup space/T tradeoff | Static QROM is not free QRAM |
| [Gidney, arXiv:1709.06648v3](https://arxiv.org/html/1709.06648v3), Quantum 2018 | Temporary AND and cheaper uncomputation | Phase correctness and measurement feedback required |
| [Meuli et al., arXiv:1904.02121](https://arxiv.org/html/1904.02121v1), DATE 2019 | Reversible pebbling for quantum memory | Recomputations must be charged |
| [Autocallable loading, arXiv:2507.19039v1](https://arxiv.org/html/2507.19039v1), 2025 preprint | Log-space comparisons and integration-based exponential loading | Reported factor is a module comparison |

These papers establish meaningful local alternatives. The missing result is their **compatible, certified combination** for the unchanged pricing task, followed by a comparison against the strongest eligible classical method at the same error and confidence.
