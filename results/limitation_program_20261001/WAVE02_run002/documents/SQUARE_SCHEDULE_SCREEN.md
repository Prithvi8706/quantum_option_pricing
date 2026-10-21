# Same-SSA square scheduling screen after A11

The square specialization remains worth one bounded circuit experiment. Its most favorable complete-source T-depth improvement is **3.4071% for B4×12 and 3.6180% for B8×52** within the current dependency-wave schedule model. This leaves room above both the 2% adoption threshold and the plan's 0.1% stop threshold. The figures are hypothetical ceilings, not achieved circuit savings.

| Current A11 case | Actual clean T-depth | Zero square work and scratch, re-packed | Favorable ceiling | Actual → hypothetical batches |
|---|---:|---:|---:|---:|
| B4×12 | 979,360 | 945,992 | 3.4071% | 174 → 162 |
| B8×52 | 1,029,082 | 991,850 | 3.6180% | 186 → 173 |

The model retains all SSA and named-output storage, the original copy contract, the actual dependency waves, and every non-square leaf. It relaxes all 144 / 1,248 eligible same-SSA square calls to zero work and zero private scratch, then re-packs the non-square calls under the accepted qubit caps of 550,141 / 4,460,481. This relaxation cannot be implemented as a real square-root or multiplier circuit; it deliberately favors the square branch when deciding whether to investigate it.

Fixed-group zero-work diagnostics gave only 0.2884% / 0%. Those figures missed the possibility that reduced square workspace can remove whole batches of other multipliers. A synthetic tied-maximum example demonstrates this directly: two 4-qubit non-square calls and one 6-qubit square, each at depth 10, require two batches under a 10-qubit cap. Zeroing square work in the existing batches leaves depth 20. Removing its scratch and re-packing reduces the hypothetical depth to 10. A fixed-group diagnostic is therefore not a global bound on achievable scheduling improvement.

## Why the favorable ceilings are bounded

For each unchanged dependency wave and each positive non-square depth threshold `t`, any packing must contain at least enough batches to hold the total scratch of calls with depth at least `t`. Volume, identical-size counts, and large-item cardinality bounds provide valid lower bounds on that required batch count. The sum of batch maxima equals the integral of the number of batches whose maximum is at least the threshold. Integrating these mandatory counts gives a lower bound on total forward depth; doubling it accounts for complete compute/copy/uncompute.

The independent threshold-capacity lower bounds exactly match the favorable first-fit re-packing results in both cases. Thus, under this relaxation and the stated wave/storage/unchanged-leaf model, the favorable re-packing is optimal and the percentages above are valid ceilings. Merely counting the minimum number of batches and multiplying by the largest leaf depth would not be sound when batches have different maxima.

This does not bound schedules that overlap or change dependency waves, reduce retained SSA storage, or alter non-square leaves. It is not a lower bound on all possible reversible circuits or on physical runtime. Copy and Clifford depth are retained as contracts; no new complete Clifford-depth result or hardware timing is inferred from this T-depth-only diagnostic.

## Next experiment and stopping rule

Emit one exact full-width signed symmetric-square leaf using the existing carry-save reduction and Brent–Kung final adder. Keep all 112 relevant product columns for width 72 / fraction precision 40 so low-column carries remain exact. Dispatch only when the actual validated target node binds both multiplication operands to the same SSA value. Preserve generic multiplication fallback.

The simplest integration keeps the existing native interface: two 72-bit argument registers and one 72-bit output XOR register, with a guarded equality promise at a same-SSA invocation. The second input can remain untouched while the specialized gates use the first. A one-input interface would require explicit versioned argument rebinding, arity validation, and revised copy accounting; it must not silently replace the current bindings.

First verify emitted gates against exact signed integers, arbitrary initial output words, inverse cleanup, and historical multiplication. Then compute actual leaf work/workspace and re-pack both complete financial sources under their current caps. Continue to full financial gate replays only if the actual candidate clears the prospectively declared adoption criterion. If it fails, retain A11 and stop the depth-only branch. Any separately motivated T-work or workspace candidate needs its own measured gates and declared Pareto criterion; neither benefit has been demonstrated by this screen.

## Evidence

The prospective protocol and executable were frozen before analysis. The screen independently reconstructed every accepted A11 batch and validated all eligible call indices against the actual target, source, and frozen square inventory. The capacity-bound implementation passed the tied-maximum counterexample and 64 seeded small-wave checks against an exact subset-partition oracle. Ruff passed. All frozen input hashes remained unchanged.

- [Prospective protocol](../../results/limitation_program_20261001/A10_square_schedule_run001/protocol.json)
- [Summary and bounded results](../../results/limitation_program_20261001/A10_square_schedule_run001/summary.json)
- [Per-wave B4×12 evidence](../../results/limitation_program_20261001/A10_square_schedule_run001/B4x12_screen.json)
- [Per-wave B8×52 evidence](../../results/limitation_program_20261001/A10_square_schedule_run001/B8x52_screen.json)
- [Synthetic verification](../../results/limitation_program_20261001/A10_square_schedule_run001/synthetic_validation.json)
- [Receipt manifest](../../results/limitation_program_20261001/A10_square_schedule_run001/manifest.json)
- [Versioned local producer](../../research/limitation_program_20261001/screen_square_schedule.py)

No financial circuit was emitted or replayed by this diagnostic, and no G2–G5 gate was closed.
