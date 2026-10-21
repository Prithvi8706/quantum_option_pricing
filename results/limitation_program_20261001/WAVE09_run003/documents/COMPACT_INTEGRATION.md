# Compact storage improves the existing complete arithmetic sources

Local result, 1 October 2026. **Combining proved compact SSA storage with the retained lookup, carry-save multiplication and ln(2) specialization reduces complete-source T-depth by another 14.9% for B4×12 and 13.4% for B8×52.** Both selected schedules fit the previous logical-qubit caps. The financial integer function, its 72-bit/40-fractional-bit precision, input law and every arithmetic leaf remain unchanged.

This is the first executed integration in the [110-point implementation plan](../limitation_audit_20261001/IMPLEMENTATION_PLAN.md), covering the immediate A06/H15/C13 interfaces. It follows the [ln(2) result](../limitation_audit_20261001/CONSTANT_MULTIPLIER_RESULT.md). These are arithmetic-source improvements; no complete pricing runtime or quantum advantage is claimed.

## What changed and why the binding is exact

The previous source retained one full 72-bit word for every SSA value. A conservative compositional mask now identifies high bits that are identically zero on the prepared input domain. Inputs, literal constants, comparisons, extraction, positive-part operations and coefficient tables supply explicit proofs. Values without a narrowing proof retain their full width.

B4's retained SSA storage falls from 410,256 to 355,052 qubits; B8's falls from 3,369,744 to 2,943,448. The financial arithmetic leaves still receive their original register formats. The executor copies each argument occurrence into its own local input slot, including repeated arguments such as a square. Every omitted leaf output bit receives a distinct private wire, because a clean leaf may temporarily flip bits that are zero at its interface boundaries.

Bindings use the leaf's actual argument/output wire metadata. Named outputs remain separate full 72-bit registers and preserve arbitrary initial words through XOR semantics. High named-output bits are preserved when the financial result's corresponding bits are proved zero. Private slots are disjoint within each parallel batch and checked clean afterward; reverse dependency batches erase the retained SSA computation.

The constructor checks the source/target operation and parameter relationship, authenticates literal lookup tables through the compiler's table-dependent leaf identity, and proves any specialized zero-low-bit input contract from the same graph. Gate-file hashes are checked during execution. These checks reject a changed constant or table even when the register bindings and possible-one masks are unchanged.

## Selected complete-source schedules

The comparison starts from the accepted ln(2) source. Costs use the same exact seven-T CCX decomposition and all-to-all logical scheduling.

| Source | Previous T-depth | Selected T-depth | Further decrease | Selected logical qubits / previous cap | T gates, unchanged |
|---|---:|---:|---:|---:|---:|
| B4×12 | 2,436,454 | **2,074,246** | **14.87%** | 550,150 / 550,158 | 632,258,326 |
| B8×52 | 2,624,696 | **2,272,184** | **13.43%** | 4,460,481 / 4,460,490 | 5,191,385,654 |

Selected Clifford+T depth also decreases from 7,226,923 to 6,162,945 and from 7,803,425 to 6,768,275. Compact storage frees retained space for more simultaneous leaf work at the fixed cap; it does not reduce the arithmetic leaves' T counts.

Argument/output copy CX counts fall from 2,711,016 to 2,184,396 for B4 and from 22,591,080 to 18,376,108 for B8: 526,620 and 4,214,972 fewer copies, respectively. This removes 19.4% and 18.7% of that copy work, not those percentages of the complete gate count.

Against the original Stage A sources, combined T-depth is now **2.91× lower for B4 and 2.81× lower for B8**. T gates remain approximately 30.3% and 30.4% below Stage A, as already established before this storage integration. Overlapping component gains are credited through these combined emitted schedules, not multiplied independently.

## Four declared memory budgets per source

The experiment tested four cap points using the stated first-fit dependency-wave schedule. Every saved candidate satisfies its actual allocation and dependency constraints.

| Source | Logical-qubit cap | Actual logical qubits | T-depth | Clifford+T depth |
|---|---:|---:|---:|---:|
| B4×12 | 550,158 | 550,150 | 2,074,246 | 6,162,945 |
| B4×12 | 522,556 | 522,546 | 2,207,302 | 6,553,829 |
| B4×12 | 494,954 | 494,954 | 2,436,454 | 7,226,967 |
| B4×12 | 467,352 | 467,327 | 3,219,480 | 9,538,801 |
| B8×52 | 4,460,490 | 4,460,481 | 2,272,184 | 6,768,275 |
| B8×52 | 4,247,342 | 4,247,316 | 2,410,328 | 7,173,795 |
| B8×52 | 4,034,194 | 4,034,194 | 2,624,696 | 7,803,357 |
| B8×52 | 3,821,046 | 3,821,037 | 3,274,186 | 9,723,111 |

The selected memory alternatives use **494,954 and 4,034,194 qubits**, about 10.0% and 9.6% below the previous caps, while preserving the previous T-depth. For B4, Clifford+T depth rises by 44 layers at this point; for B8 it falls by 68. The lowest tested budgets are correct schedules but have greater T-depth than the previous source and are retained as tradeoff evidence.

These are selected points from eight finite trials. They are not a global Pareto optimum, a minimum over all layouts, or a proof that no better scheduling exists.

## Verification and limits

**Six complete gate replays passed:** B4's previous random input, zero uniforms, maximum uniforms and the selected memory point's random input; B8's previous random input under the selected depth and memory schedules. Each output agrees with the independent financial IR after XOR into the nonzero 72-bit initial word, and every input/workspace bit is restored.

The new adversarial suite contains **16 distinct passing cases**: a 15-case primary run plus one separately run lookup-table negative control. It covers exhaustive small signed graphs, repeated arguments, aliases, inverse cleanup, real carry-save and promised constant leaves, nonuniform one-bit flag registers, multiple lookup outputs, temporarily revived private zero bits, invalid promises, cap failure, corrupt gates and complete 72-bit named outputs. A review found and fixed the operation/parameter and lookup-table provenance gaps before this financial execution.

The [independent review](../../results/limitation_program_20261001/A06_run001/independent_review.json) checked all eight saved schedules without repeating expensive gate execution. It independently reconciles DAG coverage, storage offsets and masks, actual private-wire allocation, shared-copy rounds, complete resource/depth sums, candidate selection and the six saved replay receipts. The copied source and target match their predecessor byte-for-byte; the same 53 leaf keys and their metadata/gate hashes are preserved for each case. Producer and implementation hashes match the prospective protocol.

Full financial replays sample inputs; they do not exhaust the financial domain. The structural zero-bit proofs, clean leaf contracts and exhaustive small binding tests support exact integration. Continuous-model error, estimator schedule/confidence, rotation synthesis where needed, physical routing, factory supply and complete price timing remain separate obligations. The independently proved signed-seven-bit logarithm exponent is a later interface and is **not included** in these source counts.

## Local evidence and reproduction

Implementation: [compact_parallel.py](../../research/controlled_source_completion/compact_parallel.py). Producer: [experiment_compact_parallel.py](../../research/limitation_program_20261001/experiment_compact_parallel.py). Tests: [test_compact_parallel.py](../../research/limitation_program_20261001/test_compact_parallel.py). Evidence: [protocol](../../results/limitation_program_20261001/A06_run001/protocol.json), [all trials and replays](../../results/limitation_program_20261001/A06_run001/summary.json), [B4 comparison](../../results/limitation_program_20261001/A06_run001/B4x12/comparison.json), [B8 comparison](../../results/limitation_program_20261001/A06_run001/B8x52/comparison.json), and [independent review](../../results/limitation_program_20261001/A06_run001/independent_review.json).

Run from the repository root with a fresh output directory:

```powershell
.context/frontier_t0_env/Scripts/python.exe -m research.limitation_program_20261001.experiment_compact_parallel --source-root results/limitation_audit_20261001/constant_multiplier_v1 --output results/limitation_program_20261001/A06_reproduction
```

The producer refuses an existing output root and preserves archived evidence. Everything remains local; nothing was pushed, published or uploaded.
