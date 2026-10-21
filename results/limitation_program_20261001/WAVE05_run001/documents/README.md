# Local implementation results and next experiment

The exact non-restoring square-root experiment is complete and **adopted locally**. Compared with the accepted signed7-shift source, full-circuit T-depth falls by **15.93% / 15.39%** and T-gate work by **1.57% / 1.49%**, at the same logical-qubit caps. All four financial gate replays and the independent audit passed. The verified shifts, 32-row lookup and financial target are preserved. Quantum pricing advantage remains unestablished.

The [110-item execution status](STATUS.md) records scoped successes, stopped branches and work still queued. The [complete implementation plan](../limitation_audit_20261001/IMPLEMENTATION_PLAN.md) retains every limitation, alternatives, dependencies, acceptance criteria and stopping rules. The [progress ledger](../../results/limitation_program_20261001/progress.json) records the accepted source and decisions. A successful component does not close its entire limitation.

## Latest non-restoring root experiment

| Case | Accepted T gates | Accepted T-depth | T-work reduction from shift source | T-depth reduction from shift source | Logical qubits |
|---|---:|---:|---:|---:|---:|
| B4x12 | 619,528,126 | 787,566 | 1.5724% | 15.9311% | 550,141 |
| B8x52 | 5,095,520,430 | 820,268 | 1.4924% | 15.3937% | 4,460,481 |

The exact 72/40 root leaf, under its unsigned46 guard, uses **54,180 T gates, T-depth 30,960 and 2,213 qubits**, versus 219,128, 105,582 and 2,350 for the accepted tight digit-by-digit root. It stores all 44 signed 45-bit remainder words, derives root bits from completed remainder signs, copies the exact 43-bit result into the arbitrary full 72-bit output, then reverses every root/remainder/adder/helper gate. The top active input bit45 remains legal data. Temporary modular overflow is permitted only because final signed remainders satisfy the independently verified bound.

This wave passed **88 new distinct tests** (28 leaf and 60 integration) and **four complete financial gate replays**, with dirty output and complete input/workspace restoration. All 30 / 234 actual unsigned46 root guards and all 78 / 650 accepted signed7 shifts are revalidated. The independent audit scanned 61 actual arrays and 221 metadata locations, parsed all 43 recurrence stages and Cuccaro gates, rebuilt both capped schedules, and checked unchanged targets, precision/input law, masks/copies and every nonsqrt metadata/gate byte, including the 32-row lookup. Successful program totals are now **468 distinct tests and 30 complete financial replays**.

The first independent audit stopped on an obsolete assumption of two replay vectors per case. That failed audit is preserved as A01_run010. The versioned auditor in A01_run011 enforces the actual frozen three-B4/one-B8 baseline and four total replays; labels, inputs, dirty outputs, expected values and cleanup checks remain strict. No circuit, pricing target or adoption criterion changed after the source protocol freeze.

Receipts: [leaf](NONRESTORING_SQRT_LEAF.md), [integration review](NONRESTORING_INTEGRATION_REVIEW.md), [independent source audit](NONRESTORING_SOURCE_COSTS.md), [research context](NONRESTORING_RESEARCH_CONTEXT.md), [frozen wave packet](../../results/limitation_program_20261001/WAVE05_run001/summary.json). This completes the tested exact non-restoring alternative; separate Newton/Heston work and G2-G5 remain open.

## Previous shift experiment

| Case | Accepted T gates | Accepted T-depth | T-work reduction from A11 | T-depth reduction from A11 | Logical qubits |
|---|---:|---:|---:|---:|---:|
| B4x12 | 629,425,006 | 936,810 | 0.7121% | 4.3447% | 550,141 |
| B8x52 | 5,172,716,094 | 969,512 | 0.7220% | 5.7887% | 4,460,481 |

The native shift leaf uses **8,162 T gates, 4,481 T-depth and 807 qubits**, versus 37,100, 8,736 and 1,735 for the archived full-count shift. Both native 72-bit inputs, the unscaled signed count, full output XOR and workspace cleanup are retained. Positive counts shift left modulo 2^72; negative counts shift right arithmetically. The signed minimum -64 is represented with unsigned magnitude64.

The wave passed **79 new distinct tests**: 27 leaf cases and 52 integration cases. All 78 / 650 actual shift counts have static signed7 interval proofs. **Four complete financial gate replays** passed, including arbitrary nonzero output words and full input/workspace restoration. Independent auditing checked 61 actual arrays, 220 metadata locations and 561 frozen inputs, parsed the exact reversible construction and rebuilt the capped schedules. Target bytes, financial precision/input law, SSA masks/copies and all nonspecialized leaf bytes, including the 32-row lookup, match A11. At completion of that shift wave, the successful totals were **380 distinct tests and 26 complete financial replays**.

Receipts: [leaf](NARROW_SHIFT_LEAF.md), [integration review](NARROW_SHIFT_INTEGRATION_REVIEW.md), [full source audit](SHIFT_SOURCE_COSTS.md), [frozen wave packet](../../results/limitation_program_20261001/WAVE04_run001/summary.json). This closes the tested shift-control component; broader A07 and G2-G5 remain open.

## Previous square experiment

| Case | Candidate T gates | Candidate T-depth | T-work reduction | T-depth reduction | Adopted |
|---|---:|---:|---:|---:|---|
| B4×12 | 605,771,782 | 961,916 | 4.44% | 1.7812% | No |
| B8×52 | 4,966,216,710 | 1,012,802 | 4.69% | 1.5820% | No |

The native signed 72/40 square leaf uses **107,912 T gates and 7,915 qubits**, versus 205,716 and 14,861 for general multiplication. It preserves two full-width native input registers, arbitrary 72-bit output XOR, all low-column carries and complete workspace cleanup. Dispatch requires actual same-SSA arguments; equal sampled values are insufficient.

The experiment passed **70 new distinct tests**: 21 leaf cases and 49 integration cases. An independent implementation audited 61 actual arrays and 222 metadata locations, checked every symmetric partial/carry/cleanup gate, re-proved all 144 / 1,248 actual dispatch sites, and rebuilt the capped schedules. The financial targets, 32-row lookup, other leaves, storage masks and copy counts match A11 bytes. No new complete financial gate replay was run because the pre-set resource threshold failed. At completion of that previous wave, the program had **301 distinct successful tests and 22 complete financial replays**.

Receipts: [leaf](SIGNED_SQUARE_LEAF.md), [integration review](SIGNED_SQUARE_INTEGRATION_REVIEW.md), [full source audit](SQUARE_SOURCE_COSTS.md), [frozen wave packet](../../results/limitation_program_20261001/WAVE03_run001/summary.json). This stops the square-only depth branch; future work/space or combined-source experiments require a fresh protocol and their own acceptance/replay checks.

## Accepted current circuits

| Case | Previous shift T-depth | Current T-depth | Current T gates | Logical qubits |
|---|---:|---:|---:|---:|
| B4x12 | 936,810 | 787,566 | 619,528,126 | 550,141 |
| B8x52 | 969,512 | 820,268 | 5,095,520,430 | 4,460,481 |

The [current non-restoring source](../../results/limitation_program_20261001/A11_nonrestoring_run001/summary.json) extends the [signed7 shift source](../../results/limitation_program_20261001/A07_shift_run001/summary.json) with the exact non-restoring root. It combines exact compact SSA storage, guarded logarithm multiplication, inverse-ln(2) specialization, the signed carry-save/prefix multiplier and the guarded non-restoring square root. The previously verified 32-row coefficient lookup remains included. Financial target bytes, precision and input law are identical to the frozen baseline.

Square-root input ranges are proved at all **30 / 234 actual SSA sites**. Each operand is unsigned and fits 46 bits; bit 45 remains legal data. The selected non-restoring leaf computes a 43-bit integer root using 44 stored signed45-bit remainders, then reverses all internal work. Its external input and output XOR remain 72 bits. Unproved generic sites retain their archived leaves. The experiment claims no new SSA storage or copy savings.

The complete circuits now have about **67.7% / 68.7% lower depth than the starting constant-multiplier baseline**, or **7.66x / 7.79x smaller depth than the original Stage A circuits**. These comparisons use combined emitted sources rather than multiplying independent leaf gains. T counts are about 2.01% / 1.85% below that starting baseline; physical throughput, routing and error correction still require G5 accounting.

## What passed and what stopped

| Component | Result | Evidence |
|---|---|---|
| G0/A01 baseline and accounting | Original task rebuilt; source counts and costs reconciled | [Baseline](BASELINE.md) |
| A06/H15/C13 compact parallel storage | Exact smaller storage and capped scheduling adopted | [Integration](COMPACT_INTEGRATION.md) |
| A07/A10 logarithm and inverse-ln(2) | Guarded exact constants integrated | [Constant source audit](CONSTANT_SOURCE_COSTS.md) |
| A08 direct prefix add/sub | Exact leaves missed the 2% complete-source threshold; baseline retained | [Stopped screen](CARRY_LOOKAHEAD.md) |
| A09 signed CSA/prefix multiplication | Brent–Kung variant selected and replay verified | [Implementation](PREFIX_MULTIPLIER.md), [audit](PREFIX_SOURCE_COSTS.md) |
| A07 radius range proof | All current square-root sites proved within unsigned46 input / 43-bit output bounds | [Proof](../../results/limitation_program_20261001/A07_run003/summary.json), [review](NORMAL_RANGE_REVIEW.md) |
| A11 narrowed exact square root | Previous four-variant screen adopted tight digit-by-digit/fused copy, now the comparison baseline | [Leaf](NARROW_SQRT_LEAF.md), [integration review](NARROW_SQRT_INTEGRATION_REVIEW.md), [source audit](SQRT_SOURCE_COSTS.md) |
| A11 exact non-restoring root | Signed-remainder alternative adopted after exact tests, both capped screens, four replays and independent audit | [Leaf](NONRESTORING_SQRT_LEAF.md), [audit](NONRESTORING_SOURCE_COSTS.md) |
| A10 symmetric signed square | Exact leaf verified; full-source depth gain below 2% criterion; work candidate preserved, A11 retained | [Source audit](SQUARE_SOURCE_COSTS.md) |
| A07 signed7 shift control | All 78 / 650 guards proved; exact shift adopted after full capped screen, four financial replays and audit | [Scope proof](SHIFT_CONTROL_SCOPE.md), [audit](SHIFT_SOURCE_COSTS.md) |

The square-root wave passed **78 new distinct pytest cases** and **four complete emitted financial circuit replays**. Together with the preceding wave, that is **231 distinct tests and 22 complete replays**. Small-word exhaustive checks and structural proofs support all promised input patterns; finite production samples corroborate those proofs. Independent auditing scanned 64 unique actual arrays and 550 metadata locations, recomputed all four candidate schedules, and checked cap, copy, fallback and selection accounting.

The two integration issues discovered during review—upstream target mutation and hidden input promises—were corrected before the full-source prospective protocol was frozen. Historical modules and receipts remain intact. The [first-wave packet](../../results/limitation_program_20261001/WAVE01_run001/summary.json) preserves the earlier accepted state.

## Next bounded experiment and remaining limits

Generic multiplication still owns the largest deterministic share of accepted scheduled depth: **344,528 / 358,648 layers**. Other constant leaves now rank above the improved root in the independent owner ledger. The emitted square circuit implements the [symmetric signed identity](SQUARE_SITE_SCOPE.md) with 2,356 terms instead of 4,688. It nearly halves leaf work/workspace, but its remaining cleanup and workspace costs limit the complete-source gain.

The previous [A11-cap packing screen](SQUARE_SCHEDULE_SCREEN.md) found that reducing square workspace can matter even when square depth ties ordinary multiplication. Under that frozen A11 dependency-wave, storage and non-square-leaf model, the most favorable possible extra T-depth gains were **3.4071% / 3.6180%**. These are ceilings from a hypothetical zero-work, zero-scratch square, rather than realized gains or bounds for the newly adopted shift source. Independent capacity bounds match that hypothetical packing; 64 exact synthetic packing checks also passed.

The signed-width inventory for generic multiplication is complete. It covers **1,440 / 11,856 actual calls**; at least one operand fits signed40 at **527 / 4,451** sites, while both operands fit signed40 at only seven sites per case and none fit signed24 together. The next queued component is a bounded range-specific carry-save/prefix frontier using these actual guards. It will keep the native72 interface, all low-column carry effects, signed floor semantics and cleanup, while retaining accepted root/shift/lookup bytes. The [inventory receipt](../../results/limitation_program_20261001/A09_range_scope_run001/summary.json) and [next experiment brief](NEXT_MULTIPLIER_RANGE.md) record the guards and stopping rule. No narrowed multiplier has been emitted or credited yet.

A11 remains partial: the exact non-restoring alternative is complete for this target; Newton alternatives and separate Heston validation have not been completed by this Box–Muller optimization. No benefit is transferred to a different financial source or input domain without its own proof and measurements.

G2 continuous-dollar error certification, G3 an explicit compatible estimator at 99% confidence, G4 actual matched classical timings and G5 complete physical runtime remain open. Everything stays local; nothing was pushed, uploaded or published.
