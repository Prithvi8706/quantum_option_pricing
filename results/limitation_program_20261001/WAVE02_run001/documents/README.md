# Local implementation results and next experiment

The exact square-root replacement is verified and adopted locally. Compared with the preceding accepted circuits, it reduces complete-source T-depth by **19.6% / 18.9%**, reduces T-gate work by **2.3% / 2.2%**, and uses the same logical qubit budgets. These are logical circuit improvements; quantum pricing advantage remains unestablished.

The [110-item execution status](STATUS.md) records scoped successes, stopped branches and work still queued. The [complete implementation plan](../limitation_audit_20261001/IMPLEMENTATION_PLAN.md) retains every limitation, alternatives, dependencies, acceptance criteria and stopping rules. The [progress ledger](../../results/limitation_program_20261001/progress.json) records the accepted source and decisions. A successful component does not close its entire limitation.

## Accepted current circuits

| Case | Previous A09 T-depth | Current T-depth | Current T gates | Logical qubits |
|---|---:|---:|---:|---:|
| B4×12 | 1,218,582 | 979,360 | 633,939,334 | 550,141 |
| B8×52 | 1,268,304 | 1,029,082 | 5,210,335,494 | 4,460,481 |

The [A11 source receipt](../../results/limitation_program_20261001/A11_run001/summary.json) combines exact compact SSA storage, guarded logarithm multiplication, inverse-ln(2) specialization, the signed carry-save/prefix multiplier and the guarded narrower square root. The previously verified 32-row coefficient lookup remains included. Financial target bytes, precision and input law are identical to the frozen baseline.

Square-root input ranges are proved at all **30 / 234 actual SSA sites**. Each operand is unsigned and fits 46 bits; bit 45 remains legal data. The selected leaf computes a 43-bit integer root using 45-bit stored remainders, then reverses all internal work. Its external input and output XOR remain 72 bits. Unproved generic sites retain their archived leaves. The experiment claims no new SSA storage or copy savings.

The complete circuits now have about **59.8% / 60.8% lower depth than the starting constant-multiplier baseline**, or **6.16× / 6.21× smaller depth than the original Stage A circuits**. These comparisons use combined emitted sources rather than multiplying independent leaf gains. T counts remain about 0.3% / 0.4% above the starting baseline; physical throughput, routing and error correction still require G5 accounting.

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

The square-root wave passed **78 new distinct pytest cases** and **four complete emitted financial circuit replays**. Together with the preceding wave, that is **231 distinct tests and 22 complete replays**. Small-word exhaustive checks and structural proofs support all promised input patterns; finite production samples corroborate those proofs. Independent auditing scanned 64 unique actual arrays and 550 metadata locations, recomputed all four candidate schedules, and checked cap, copy, fallback and selection accounting.

The two integration issues discovered during review—upstream target mutation and hidden input promises—were corrected before the full-source prospective protocol was frozen. Historical modules and receipts remain intact. The [first-wave packet](../../results/limitation_program_20261001/WAVE01_run001/summary.json) preserves the earlier accepted state.

## Next bounded experiment and remaining limits

Multiplication now owns the largest deterministic share of scheduled depth: **344,528 / 358,648 layers**, versus 211,164 for square root in each case. Actual same-SSA products provide **144 / 1,248 possible square sites**. The next screen derives symmetric signed partial products, preserves carry from discarded low columns, and checks whether changing those sites can affect complete-source depth. A leaf reduction is not automatically a source improvement.

A11 remains partial: non-restoring and Newton alternatives, and separate Heston validation, have not been completed by this Box–Muller optimization. No benefit is transferred to a different financial source or input domain without its own proof and measurements.

G2 continuous-dollar error certification, G3 an explicit compatible estimator at 99% confidence, G4 actual matched classical timings and G5 complete physical runtime remain open. Everything stays local; nothing was pushed, uploaded or published.
