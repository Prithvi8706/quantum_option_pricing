# The exact seven-bit logarithm constant leaf improves all three logical resources

Local A10 leaf experiment, 1 October 2026. **The retained logarithm-only ln(2) leaf uses 440 qubits, 2,576 T gates and 752 T-layers.** Its previous signed32 counterpart uses 1,405 qubits, 11,396 T gates and 1,152 T-layers. The new leaf has 68.7% fewer qubits, 77.4% fewer T gates and 34.7% lower T-depth. This is a verified leaf result; complete financial sources have not yet been integrated or replayed with it.

The [preceding metadata proof](LOG_EXPONENT_PROOF.md) identifies 30 eligible logarithm calls in B4x12 and 234 in B8x52. Their exponential counterparts—48 and 416 calls—retain the wider fallback. No improvement factor from this leaf is applied to the full circuit or pricing runtime.

## Exact interface and construction

The 72-bit input has low 40 bits zero. Its upper 32 bits must be the sign extension of a seven-bit signed integer q. The new metadata is:

~~~json
{"zero_low_bits": 40, "signed_upper_bits": 7}
~~~

The seven active bits occupy input positions 40–46; positions 47–71 equal bit 46. This is a static proof obligation, not a dynamic promise check. The source, fraction 40, coefficient 762123384786 and arbitrary 72-bit output-XOR contract remain unchanged.

We embed the existing exact constant multiplier at width 47, fraction 40 and zero-low-bit 40. Its input holds q·2^40 for every signed seven-bit q in [-64,63]. Its output q·762123384786 fits signed 47 bits, so sign extension produces the same full 72-bit result as the old general leaf. The coefficient stays a positive integer.

Two wrappers were implemented and tested:

1. **Clean child twice:** compute the child into a private 47-bit product, copy/sign-extend it into the outer 72-bit output, then repeat the clean child to erase that private product.
2. **Fused child copy:** verify the child's literal compute/copy-47-bit/reverse structure, route its copy into the outer output, extend the computed product sign bit into the higher output bits, and reverse the computation once.

Fusion requires an exact reversed gate sequence, untouched child output before the middle copy, one declared CX per copied bit and distinct product source wires. A malformed child is rejected. The outer output never controls a gate, so arbitrary initial output values cannot influence computation or cleanup. The builder emits only X, CX and exact CCX.

## All measured alternatives

Resources include the full output XOR and cleanup, using the same exact seven-T CCX and all-to-all logical scheduling as the previous result.

| Arithmetic strategy | Wrapper | Qubits | T gates | T-depth |
|---|---|---:|---:|---:|
| Binary shift-add | Child twice | 286 | 36,680 | 20,960 |
| Binary shift-add | Fused copy | 239 | 18,340 | 10,480 |
| Signed-digit shift-add | Child twice | 286 | 17,808 | 10,176 |
| Signed-digit shift-add | Fused copy | 239 | 8,904 | 5,088 |
| Binary carry-save | Child twice | 679 | 8,624 | 1,504 |
| Binary carry-save | Fused copy | 632 | 4,312 | 752 |
| Signed-digit carry-save | Child twice | 487 | 5,152 | 1,504 |
| **Signed-digit carry-save** | **Fused copy, retained** | **440** | **2,576** | **752** |

The selected leaf also has Clifford+T depth 2,259, compared with 3,459 for the retained signed32 leaf. The original general 72-bit leaf uses 433 qubits, 80,808 T gates and 46,176 T-depth. The new leaf is slightly wider than that original leaf, while using much less work and depth; it strictly improves width, work and depth against the current signed32 carry-save implementation.

The straightforward child-twice candidate does not reduce T-depth against the current implementation. The checked fusion resolves that overhead. The 239-qubit fused signed-digit shift-add remains a measured alternative for a tighter workspace budget.

## Verification and scope

**14 pytest tests passed in 3.50 seconds.** Across all eight candidate variants, every signed seven-bit value was checked with zero and nonzero initial outputs, both execution directions, restored input and workspace, and equivalence to the original general 72-bit leaf. That amounts to 4,096 new-leaf gate replays and 2,048 historical-leaf reference executions.

Tests also verify output wires never control computation and ignored input wires remain untouched. Four invalid-domain basis examples detect missing low-zero or sign-extension promises. Coefficient-only and incorrect-positive-guard patterns are rejected. Actual source classification reproduces all eligible logarithm counts and leaves every exponential call on fallback. A deliberately damaged child fails the fusion guard.

The [protocol](../../results/limitation_program_20261001/A10_leaf_run001/protocol.json) was saved before tests and measurements. It hashes the builder, executed test/experiment producer, reused arithmetic and graph-proof dependencies, and the preceding proof result. [Result](../../results/limitation_program_20261001/A10_leaf_run001/result.json), [verification](../../results/limitation_program_20261001/A10_leaf_run001/verification.json) and [manifest](../../results/limitation_program_20261001/A10_leaf_run001/manifest.json) preserve all candidates, gate arrays and baseline costs. Ruff and whitespace checks passed.

Implementation: [log_constant_multiplier.py](../../research/controlled_source_completion/log_constant_multiplier.py). Tests and local experiment: [test_log_constant_multiplier.py](../../research/limitation_program_20261001/test_log_constant_multiplier.py).

## Next integration boundary

The default builder selects the retained fused signed-digit carry-save variant. The exported same-SSA guard reuses the preceding complete log-chain proof; its versioned specification includes input contract, width, fraction, coefficient, child width, arithmetic strategy, wrapper and lowering. A new library must use that proof before dispatching and preserve exponential/unproved fallback.

The [next action](../../results/limitation_program_20261001/A10_leaf_run001/NEXT.md) is review, then compilation into the combined compact/capped financial sources and complete replay against the unchanged integer target. Only that experiment can establish a complete-source reduction. All work stayed local; no old compiler or constant multiplier was edited, and nothing was pushed or published.
