# Local implementation results and next experiment

The exact signed7-count shift experiment is complete and **adopted locally**. Compared with the accepted A11 source, full-circuit T-depth falls by **4.34% / 5.79%** and T-gate work by **0.71% / 0.72%**, with the same logical-qubit caps. All four financial gate replays and the independent audit passed. The earlier exact square candidate remains preserved separately. Quantum pricing advantage remains unestablished.

The [110-item execution status](STATUS.md) records scoped successes, stopped branches and work still queued. The [complete implementation plan](../limitation_audit_20261001/IMPLEMENTATION_PLAN.md) retains every limitation, alternatives, dependencies, acceptance criteria and stopping rules. The [progress ledger](../../results/limitation_program_20261001/progress.json) records the accepted source and decisions. A successful component does not close its entire limitation.

## Latest shift experiment

| Case | Accepted T gates | Accepted T-depth | T-work reduction from A11 | T-depth reduction from A11 | Logical qubits |
|---|---:|---:|---:|---:|---:|
| B4x12 | 629,425,006 | 936,810 | 0.7121% | 4.3447% | 550,141 |
| B8x52 | 5,172,716,094 | 969,512 | 0.7220% | 5.7887% | 4,460,481 |

The native shift leaf uses **8,162 T gates, 4,481 T-depth and 807 qubits**, versus 37,100, 8,736 and 1,735 for the archived full-count shift. Both native 72-bit inputs, the unscaled signed count, full output XOR and workspace cleanup are retained. Positive counts shift left modulo 2^72; negative counts shift right arithmetically. The signed minimum -64 is represented with unsigned magnitude64.

The wave passed **79 new distinct tests**: 27 leaf cases and 52 integration cases. All 78 / 650 actual shift counts have static signed7 interval proofs. **Four complete financial gate replays** passed, including arbitrary nonzero output words and full input/workspace restoration. Independent auditing checked 61 actual arrays, 220 metadata locations and 561 frozen inputs, parsed the exact reversible construction and rebuilt the capped schedules. Target bytes, financial precision/input law, SSA masks/copies and all nonspecialized leaf bytes, including the 32-row lookup, match A11. The successful program totals are now **380 distinct tests and 26 complete financial replays**.

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

| Case | Previous A11 T-depth | Current T-depth | Current T gates | Logical qubits |
|---|---:|---:|---:|---:|
| B4x12 | 979,360 | 936,810 | 629,425,006 | 550,141 |
| B8x52 | 1,029,082 | 969,512 | 5,172,716,094 | 4,460,481 |

The [current shift source receipt](../../results/limitation_program_20261001/A07_shift_run001/summary.json) extends [A11](../../results/limitation_program_20261001/A11_run001/summary.json) with the proved signed7 shift. It combines exact compact SSA storage, guarded logarithm multiplication, inverse-ln(2) specialization, the signed carry-save/prefix multiplier and the guarded narrower square root. The previously verified 32-row coefficient lookup remains included. Financial target bytes, precision and input law are identical to the frozen baseline.

Square-root input ranges are proved at all **30 / 234 actual SSA sites**. Each operand is unsigned and fits 46 bits; bit 45 remains legal data. The selected leaf computes a 43-bit integer root using 45-bit stored remainders, then reverses all internal work. Its external input and output XOR remain 72 bits. Unproved generic sites retain their archived leaves. The experiment claims no new SSA storage or copy savings.

The complete circuits now have about **61.6% / 63.1% lower depth than the starting constant-multiplier baseline**, or **6.44x / 6.59x smaller depth than the original Stage A circuits**. These comparisons use combined emitted sources rather than multiplying independent leaf gains. T counts are about 0.45% / 0.36% below that starting baseline; physical throughput, routing and error correction still require G5 accounting.

## What passed and what stopped

| Component | Result | Evidence |
|---|---|---|
| G0/A01 baseline and accounting | Original task rebuilt; source counts and costs reconciled | [Baseline](BASELINE.md) |
| A06/H15/C13 compact parallel storage | Exact smaller storage and capped scheduling adopted | [Integration](COMPACT_INTEGRATION.md) |
| A07/A10 logarithm and inverse-ln(2) | Guarded exact constants integrated | [Constant source audit](CONSTANT_SOURCE_COSTS.md) |
| A08 direct prefix add/sub | Exact leaves missed the 2% complete-source threshold; baseline retained | [Stopped screen](CARRY_LOOKAHEAD.md) |
| A09 signed CSA/prefix multiplication | Brent–Kung variant selected and replay verified | [Implementation](PREFIX_MULTIPLIER.md), [audit](PREFIX_SOURCE_COSTS.md) |
| A07 radius range proof | All current square-root sites proved within unsigned46 input / 43-bit output bounds | [Proof](../../results/limitation_program_20261001/A07_run003/summary.json), [review](NORMAL_RANGE_REVIEW.md) |
| A11 narrowed exact square root | Four variants screened; tight digit-by-digit with fused output copy adopted | [Leaf](NARROW_SQRT_LEAF.md), [integration review](NARROW_SQRT_INTEGRATION_REVIEW.md), [source audit](SQRT_SOURCE_COSTS.md) |
| A10 symmetric signed square | Exact leaf verified; full-source depth gain below 2% criterion; work candidate preserved, A11 retained | [Source audit](SQUARE_SOURCE_COSTS.md) |
| A07 signed7 shift control | All 78 / 650 guards proved; exact shift adopted after full capped screen, four financial replays and audit | [Scope proof](SHIFT_CONTROL_SCOPE.md), [audit](SHIFT_SOURCE_COSTS.md) |

The square-root wave passed **78 new distinct pytest cases** and **four complete emitted financial circuit replays**. Together with the preceding wave, that is **231 distinct tests and 22 complete replays**. Small-word exhaustive checks and structural proofs support all promised input patterns; finite production samples corroborate those proofs. Independent auditing scanned 64 unique actual arrays and 550 metadata locations, recomputed all four candidate schedules, and checked cap, copy, fallback and selection accounting.

The two integration issues discovered during review—upstream target mutation and hidden input promises—were corrected before the full-source prospective protocol was frozen. Historical modules and receipts remain intact. The [first-wave packet](../../results/limitation_program_20261001/WAVE01_run001/summary.json) preserves the earlier accepted state.

## Next bounded experiment and remaining limits

Generic multiplication still owns the largest deterministic share of accepted scheduled depth: **344,528 / 358,648 layers**, versus 211,164 for square root. The emitted square circuit implements the [symmetric signed identity](SQUARE_SITE_SCOPE.md) with 2,356 terms instead of 4,688. It nearly halves leaf work/workspace, but its remaining cleanup and workspace costs limit the complete-source gain.

The previous [A11-cap packing screen](SQUARE_SCHEDULE_SCREEN.md) found that reducing square workspace can matter even when square depth ties ordinary multiplication. Under that frozen A11 dependency-wave, storage and non-square-leaf model, the most favorable possible extra T-depth gains were **3.4071% / 3.6180%**. These are ceilings from a hypothetical zero-work, zero-scratch square, rather than realized gains or bounds for the newly adopted shift source. Independent capacity bounds match that hypothetical packing; 64 exact synthetic packing checks also passed.

The next queued experiment is **one exact non-restoring square-root leaf**, matching the existing unsigned46 domain, native72 input/output and exact integer function. It must charge signed remainder storage and complete cleanup, retain the accepted signed7 shift bytes/promises, and pass independent exhaustive tests before any full capped source screen. The [next experiment brief](NEXT_NONRESTORING_SQRT.md) records the interfaces, checks and stopping rule. The [preceding square wave packet](../../results/limitation_program_20261001/WAVE03_run001/summary.json) preserves the earlier accepted state.

A11 remains partial: non-restoring and Newton alternatives, and separate Heston validation, have not been completed by this Box–Muller optimization. No benefit is transferred to a different financial source or input domain without its own proof and measurements.

G2 continuous-dollar error certification, G3 an explicit compatible estimator at 99% confidence, G4 actual matched classical timings and G5 complete physical runtime remain open. Everything stays local; nothing was pushed, uploaded or published.
