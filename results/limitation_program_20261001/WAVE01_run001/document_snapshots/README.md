# Local implementation results and next experiment

The first implementation wave is complete. The accepted circuits have **50.0% / 51.7% lower T-depth than the baseline at the start of this round**, at the existing qubit budgets. Relative to the original Stage A circuits, their depths are **4.95× / 5.04× smaller**. These are measured logical circuit improvements; quantum pricing advantage remains unestablished.

The [110-item execution status](STATUS.md) records scoped successes, stopped branches and work still queued. The [complete implementation plan](../limitation_audit_20261001/IMPLEMENTATION_PLAN.md) retains every limitation, alternatives, dependencies, acceptance criteria and stopping rules. The [machine-readable progress ledger](../../results/limitation_program_20261001/progress.json) stores the current accepted source and decisions.

## Accepted current circuits

| Case | T-depth before this round | Current T-depth | Current T gates | Current logical qubits |
|---|---:|---:|---:|---:|
| B4×12 | 2,436,454 | 1,218,582 | 648,827,494 | 550,141 |
| B8×52 | 2,624,696 | 1,268,304 | 5,326,463,142 | 4,460,481 |

The accepted [A09 source](../../results/limitation_program_20261001/A09_run001/summary.json) combines exact compact SSA storage, the guarded seven-bit logarithm multiplier, general inverse-ln(2) specialization and the signed carry-save/prefix multiplier. The previously verified 32-row coefficient lookup is included. The financial target bytes, precision and input law are identical to the frozen baseline.

The last multiplier change trades about **3.3% more T gates for 30–31% lower complete-source T-depth** against the preceding inverse-ln(2) baseline. Across this whole round, T counts increase by about 2.6%. Physical factory throughput and runtime must price that tradeoff. Each reported depth comes from the combined emitted source; independent leaf improvement factors are never multiplied.

## What passed and what stopped

| Component | Result | Evidence |
|---|---|---|
| G0/A01 baseline and accounting | Original task rebuilt; source counts and costs reconciled | [Baseline](BASELINE.md) |
| A06/H15/C13 compact parallel storage | Further 14.9% / 13.4% depth reduction; memory alternatives retained | [Integration](COMPACT_INTEGRATION.md) |
| A07/A10 signed-seven-bit logarithm | Exact narrower leaf; lower full-source T count, unchanged full-source depth | [Leaf](LOG_CONSTANT_LEAF.md), [source audit](CONSTANT_SOURCE_COSTS.md) |
| A10 general inverse-ln(2) | Four candidates; chosen source improves both complete circuits | [Leaf](INVERSE_LN2_LEAF.md), [source audit](CONSTANT_SOURCE_COSTS.md) |
| A08 direct prefix add/sub | Exact leaves; 0.7–1.5% source depth gains missed the 2% threshold; baseline retained | [Stopped screen](CARRY_LOOKAHEAD.md) |
| A09 signed CSA/prefix multiplication | Both candidates screened; Brent–Kung selected and replay verified | [Implementation](PREFIX_MULTIPLIER.md), [independent audit](PREFIX_SOURCE_COSTS.md) |
| A07 radius range proof | All 30 / 234 square-root sites have unsigned input bounds of 46 bits and output bounds of 43 bits | [Proof receipt](../../results/limitation_program_20261001/A07_run003/summary.json), [independent review](NORMAL_RANGE_REVIEW.md) |

Successful runs passed **153 distinct pytest cases** and **18 complete emitted financial circuit replays**. Separate audits checked actual gate arrays, arbitrary-output XOR, cleanup, source bindings, packing, resource counts and dependency depths. Exhaustive small-word checks and structural proofs extend the evidence beyond the finite production replay samples. Failed preparation attempts are preserved with their corrections and executable snapshots.

## Next bounded experiment

Square root is now the largest depth contributor: its deterministic batch attribution is 450,386 layers in each case. A11 will use the reviewed radius bounds to emit a narrower exact square-root leaf, retain a generic fallback, test its full 72-bit output XOR and workspace cleanup, then screen both complete circuits at the current caps. Only a worthwhile replay-verified source improvement should replace the current baseline.

The 46-bit radius input bound is **unsigned**. A signed 46-bit positive clamp would discard some valid inputs. Preserve the original unsigned square-root semantics and every carry/remainder needed for exact floor-root and cleanup. The bounds are a proof component; a narrowed circuit has not yet been built or credited.

G2 continuous-dollar error certification, G3 an explicit compatible estimator at 99% confidence, G4 actual matched classical timings and G5 complete physical runtime remain open. All work stays local; nothing was pushed, uploaded or published.
