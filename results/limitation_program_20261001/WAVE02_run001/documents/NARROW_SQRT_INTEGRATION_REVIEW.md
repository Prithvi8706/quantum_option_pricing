# Independent review of unsigned square-root integration

The reviewed implementation safely narrows square-root arithmetic when an exact range proof at that SSA invocation establishes `0 <= operand < 2^46`. The external interface remains a 72-bit input and a 72-bit output XOR at fraction precision 40. Generic or unproved invocations retain their archived leaf bytes. This is a G1 optimization of the existing digital function; it does not close the continuous financial error, estimator, classical timing, or physical advantage gates G2–G5.

Reviewed implementation:

- [narrow_sqrt.py](../../research/controlled_source_completion/narrow_sqrt.py): unsigned restoring square root, stored remainder cleanup, and full-width wrappers.
- [prove_sqrt_input.py](../../research/limitation_program_20261001/prove_sqrt_input.py): same-SSA range guard, specification/key binding, and native interface validation.
- [sqrt_library.py](../../research/limitation_program_20261001/sqrt_library.py): guarded dispatch, unchanged fallback, validated cache reuse, and whole-target compiler wrapper.
- [compact_parallel_v2.py](../../research/controlled_source_completion/compact_parallel_v2.py): independent promise validation before scheduling or executing actual emitted gates.
- [test_sqrt_integration.py](../../research/limitation_program_20261001/test_sqrt_integration.py): independent integer oracle, integration checks, and negative controls.

## Arithmetic and cleanup

The narrowed operand is unsigned. Its bit 45 may be set, and must not become a sign bit when the active arithmetic width becomes 46. The tests explicitly exercise `2^45`, adjacent words, and `2^46 - 1`. They compare against Python's exact `math.isqrt(raw << 40)`, without a positivity clamp or a floating-point approximation.

For 46 active input bits and 40 fraction bits, the radicand has at most 86 bits and the root needs 43 bits. In the tight restoring recurrence, let the accumulated partial root be `q` and its remainder be `r`. The square-root invariant gives `0 <= r < 2*q + 1`. At a stage with an `s`-bit partial root, the next pre-subtraction remainder `4*r + digit` is strictly below `2^(s+3)`. The largest stage has `s = k - 1`, so `k + 2` remainder bits are sufficient; here `k = 43` and that width is 45. The trial `4*q + 1` also fits. The arithmetic reduction therefore does not rely on sampled small remainders.

Each remainder remains stored until the emitted computation is reversed. The fused embedding validates a literal compute/copy/exact-reverse boundary, verifies that output wires do not participate in forward computation, and copies only the result bits into the full native output. This preserves arbitrary initial output words, including their high bits. It also restores the private root and remainder registers. Reversibility and exact basis-state behavior support coherent execution throughout the promised input subspace; finite test vectors are corroboration, not a substitute for the invariant and static range proof.

The integration keeps the existing SSA active-mask storage proof. A proved 43-bit square-root result is not credited as a new SSA storage optimization in this experiment.

## Static proof and trusted consumption boundary

The guard derives intervals from the validated target's declared input domain and actual producers. It checks the operand at every square-root invocation. A 72-bit generic input, or a `provided` input whose range is not established by the uniform preparation rule, receives no new narrowing promise. Bounds from every literal lookup row participate in the proof; changing a table can invalidate it.

The new leaf specification binds external width, fraction precision, active input width, unsigned domain, child/result/remainder widths, algorithm, embedding, lowering, and input contract to its hash key. The native arguments and output must retain the complete contiguous 72-bit interface. Cache reuse verifies metadata, gate SHA, actual resources, and the expected specification.

The review found and resolved two integration gaps before the full experiment protocol was frozen:

1. The generic compiler skips input nodes. A caller could alter an upstream input declaration after constructing a library while requesting the same square-root node. The new `compile_sqrt_graph` wrapper compares the entire target with the frozen snapshot before compilation. This covers input width, preparation/domain, outputs, and unused tables. A retained regression also verifies that the versioned scheduler independently rejects an invalid promise even when the older generic compiler is called directly.
2. A narrowed leaf's outer `input_contract` could be removed or replaced while its specification still declared unsigned narrowing. The versioned readers now recognize narrowed leaves from both metadata and specification/lowering and require a consistent valid outer contract. Missing, empty, unrelated, and mismatched promises are rejected before use.

The accepted consumption path is the bound compiler wrapper followed by the versioned scheduler/executor. The historical generic compiler and historical scheduler are not substitutes for this guarded path when consuming the newly promised leaves.

## Independent verification

The final local development run passed **36 pytest cases in 12.78 seconds**; Ruff passed for the test file. The full experiment subsequently runs the frozen test file and archives its own JUnit evidence. The 36 cases cover:

- Exact integer square roots on boundaries and square-adjacent inputs, including legal active bit 45.
- Full 72-bit output XOR from nonzero initial words, output aliases, repeated argument copies, and complete input/workspace restoration.
- Byte-identical generic fallback for full unsigned 72-bit operands and unproved input preparation.
- All-row lookup range proof and fresh reload of both cached leaves and an already specialized source.
- Invalid widths, malformed contracts, hidden promises, incorrect native interface, and promise forgery on unproved graphs.
- Disk and in-memory metadata corruption, specification mismatch, resource mismatch, and gate SHA corruption.
- Target bindings, upstream input declarations, tables, named outputs, compiler snapshots, schedule fingerprints, storage proofs, and raw input domain violations.

These checks independently support exact integration. Full financial source replays, actual emitted gate recounts, schedule/cap verification, and prospective receipt validation remain the separate requirements for adopting a candidate. Any reduction reported from those receipts is a logical arithmetic resource improvement under the stated all-to-all 7-T-per-CCX model. No physical runtime or quantum advantage conclusion follows from this review.
