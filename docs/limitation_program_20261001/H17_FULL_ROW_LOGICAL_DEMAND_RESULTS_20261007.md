# H17: logical demand for the complete cheaper approximation row

The complete optimized degree-four approximation row now has verified logical T-state demand histograms and a bounded commitment to every touched-wire dependency. The corrected local run completed, independent saved-checker review passed, and [ROOT saved verification](../../.context/H17_FULL16_LOGICAL_DEMAND_V2_ACTUAL_RESULT_ROOT_VERIFICATION_run001.json) checked the sealed packet. All nine derived resource fields equal the already verified circuit's totals.

| Saved quantity | Result |
|---|---:|
| Logical qubits | 11,853 |
| Native X/CX/CCX rows | 424,966 |
| Primitive events | 3,284,270 |
| Paid T-family states | 1,429,652 |
| Logical T horizon | 30,103 |
| Logical Clifford+T horizon | 82,531 |
| Peak T-layer batch | 1,266 |
| Peak Clifford+T-layer batch | 428 |

The [saved histogram display](../../.context/H17_FULL16_VERIFIED_LOGICAL_HISTOGRAM_DISPLAY_run001.json) records 30,103 occupied T layers and 56,111 occupied Clifford+T layers. Each histogram sums to the same 1,429,652 paid states. These coordinates remain separate, and neither has a physical-time calibration.

The transform decodes only the current optimized candidate array. It includes the selector, coefficient lookup, all sixteen nodes, copies, inverse/dirty-output contract and spectator. The event commitment uses an injective 68-byte little-endian record carrying event identity, native row, macro index, ordered wires and predecessor nodes, both logical clocks and paid-state flag. Its 223,330,360 conceptual record bytes are streamed into a digest; that journal is not materialized or saved. The nine saved files occupy 1,260,810 bytes. The saved verifier checks the commitment's type and links, rather than reconstructing the event trace.

Eight actual prefix rows have a separate direct recurrence check. Five artificial malformed-row controls reject duplicate wires, out-of-range wires, nonzero padding, boolean slots and an unsupported opcode. The T-dagger Clifford/frame premise remains explicit; T and native CCZ states are not interchangeable for free. The parent's phase contract is inherited within its existing conditional scope and is not replayed here.

The first attempt stopped before array decoding and output creation because its library namespace guard omitted the unchanged module docstring. The [failed attempt](../../.context/H17_FULL16_LOGICAL_DEMAND_V1_ROOT_FAILURE_CAPTURE_run001.json) remains frozen. V2 repairs only that guard and current routes; the event encoding, clocks, cohort and caps are unchanged.

Recorded preseal CPU time was 68.125 seconds and sampled peak RSS was 44,011,520 bytes. ROOT observed terminal exit zero after 70.1083663 wall seconds. The caps remain 180 process-CPU, 150 admission-CPU and 600 wall seconds, 150 MiB RSS and 64 MiB outputs. These are local software observations.

The [completed fixed88 buffer test](H17_FULL_ROW_CONDITIONAL_BUFFER_RESULTS_20261007.md) now applies the existing rule to these complete-row histograms and verifies all88 failures. Under its arrival-then-overflow-then-consume batching rule, capacity below 1,266 cannot serve the largest T batch; capacity below 428 cannot serve the largest Clifford+T batch. These are necessary conditions for this hypothetical model, not physical buffer requirements. The grid has now completed both its actual run and independent saved verification; it supplies scoped negative evidence.

Physical layer duration, usable-state quality, yield, transport delay, storage noise, correction cost and whole-estimator scheduling remain open. This result does not recertify the financial source, full G2, hardware feasibility or quantum advantage.

The [sealed manifest](../../.context/full_row_logical_demand_20261007/actual_full16_run002/manifest.json) SHA256 is `f40625467f96dbf7c07a8d2b75a4522714bb69a7ddb24ad7959e580896746abc`. ROOT saved verification SHA256 is `b50c918705ba9666d48b0e05896b56e20f54c36ea792a22c145cce88b426bf19`. All work remains local.
