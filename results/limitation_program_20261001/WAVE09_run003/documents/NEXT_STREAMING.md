# Next bounded component: reversible streaming of the monitored payoff

A19 starts with the original plan's two-asset/four-date verification harness. It asks whether retaining current state and reversible sufficient statistics can reduce path storage while preserving the exact monitored arithmetic-basket payoff. Any later full-source trial starts with B4x12; the harness is not a replacement for B4x12 or B8x52. Read the accepted arithmetic source and the completed A18 workspace receipts from the live progress ledger, preserving both as separate comparison points. The [independently reconciled A18 B4 point](CHECKPOINTING_RESULTS.md) uses 365,630 logical qubits, 674,115,932 T gates and 20,209,444 T-depth; the preferred parallel coefficient baseline remains unchanged. Do not multiply A18 and streaming savings.

## Freeze the exact harness before execution

Use `barrier_oracle_depth.build(2, 4, free_gaussians=False, q=32)` and the existing optimizer as the independent SSA reference. Record the builder, original and optimized graph fingerprints, literal coefficient tables, native leaf hashes, input declarations, output contract and code/environment hashes. The financial constants, 72-bit words, 40 fractional bits, original midpoint input law, Box-Muller generation, correlation, drift, clipping and degree-12 Estrin exponential remain fixed. The 32-row coefficient lookup and the 32-bit random-input words are different quantities.

Freeze one harness and exactly two checkpoint placements before testing or measuring candidates. Use date boundaries for one placement and two-date block boundaries for the other; specify the actual retained registers, reversible updates and legal cleanup moves at each boundary. Declare the tiny draw grid, boundary fixtures, dirty-output patterns, resource caps, tie-breaking and CPU/replay limits prospectively. Keep the existing parallel-prefix/SSA construction as the control.

The payoff remains the discounted positive part of the average over every asset/date stock, multiplied by the survival indicator. Each monitoring date uses the original rounded equal-weight arithmetic basket. A basket greater than or equal to the barrier knocks out the path; survival requires every basket to be strictly below the barrier. Preserve equality handling and the separate positive-payoff strike test. A geometric basket or a threshold on summed log prices would be a different function.

## Small exact changes to investigate

1. Retain a current accumulated raw log price for each asset. Compare an explicitly reversible modular addition update with the original parallel-prefix result. Clip only the temporary log used by the stock exponential: feeding a clipped log back into subsequent updates would change the original path. Replacing `exp(total log)` with repeated finite stock multiplications also needs an exact equivalence proof and cannot be assumed valid.
2. Accumulate the original native stock words into a reversible running Asian sum. Apply the original average coefficient and discount at the original arithmetic boundaries. Summing already rounded date baskets can change finite rounding and requires proof before use.
3. Compute each date's original basket and strict barrier predicate. Use a reversible violation count, with sufficient width to avoid overflow, and test count equal to zero at the end. Alternatively retain or recompute local decisions under the declared checkpoints. Overwriting an `alive` bit with an AND or overwriting a maximum discards information; provide retained history or a proved reversible construction. Do not silently skip later monitoring dates after a violation.
4. Erase temporary stocks, predicates, clipped logs and Gaussian intermediates only with their required predecessors available. Preserve common/idiosyncratic normals, constants and atomic lookup outputs while they have shared consumers, or regenerate them through charged gates. In-place finite multiplication is not generally invertible. Every modified current-state register needs an explicit inverse and complete cleanup proof.

Charge all random preparation, native input copies and un-copies, coefficient/table preparation, recomputation, saved decisions, old-state history, unused high output scratch, output copies and inverses. Record physical allocation spans, observed peak usage, complete T count, T depth, Clifford-plus-T depth and setup time. Report the lost parallelism from sequential date updates. Combine storage savings only through an emitted schedule; do not multiply the A18 and streaming percentages.

## Validation and the original acceptance rule

Exhaust the prospectively declared tiny draw grid against the independent SSA integer evaluator. Its exhaustive coverage applies to that grid, not the entire 32-bit product input law. Exercise below/equal/above-barrier arithmetic predicates, strike ties, endpoint inputs, finite wraparound, repeated arguments, shared normals/constants, lookup atomicity, dirty full-width outputs and checkpoint cleanup. Separately verify the reversible update identities and replay actual emitted harness gates. If an exact-barrier financial input is not available, label an equality predicate fixture explicitly rather than claiming a full path equality replay.

The original A19 acceptance requires all of the following:

- Streaming and SSA circuits return exactly the same discrete payoff on all harness inputs, including equality at the barrier.
- Inputs and workspace restore completely; lost information is retained or recomputed and every restoration cost is charged.
- Measured peak width decreases, with the complete work/depth penalty explicit.
- The harness does not replace B8x52 as the pricing task. Full scaling requires an emitted matching source and a G5 comparison.

The original stop rule is one two-asset/four-date harness and two checkpoint placements. Stop full scaling if cleanup eliminates the width saving or makes it dominated, or if the serial-depth penalty worsens the frontier under the physical cap. An unresolved physical comparison remains unresolved; logical width alone does not establish a pricing latency gain.

On a verified useful result, compare the best exact design with A18 and the accepted arithmetic source, and retain only measured nondominated points. Freeze a prospective B4 integration separately before executing it. Keep B8 scaling outside this first bounded run. On failure, preserve the SSA/prefix source and archive the exact negative harness result, identifying whether barrier history, irreversible finite updates, shared dependencies or cleanup consumed the saving.

G2 continuous dollar-error certification, G3 a compatible 99% estimator, G4 matched classical timing and G5 physical runtime remain open. No approximate law, lower-precision arithmetic or continuous-price claim is adopted here. Everything remains local: no push, upload, publishing or cloud execution.

Evidence: [original A19 plan](../limitation_audit_20261001/implementation_plan/ARITHMETIC.md), [original roadmap entry](../limitation_audit_20261001/implementation_plan/roadmap.json), [live progress](../../results/limitation_program_20261001/progress.json), [financial builder](../../research/advantage_frontier_20260923/barrier_oracle_depth.py), [Stage A source provenance](../../research/frontier_completion_20260927/stage_a.py).
