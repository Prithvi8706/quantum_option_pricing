# A19 exact reversible streaming result

The date-by-date design retains a verified memory alternative on the original two-asset/four-date harness. It uses37,186 logical qubits versus92,475 for the matched compact SSA control:59.79% less memory. It pays1.998 times the T gates and7.194 times the T-depth. The two-date block design is dominated by the date design. The accepted B4/B8 coefficient source remains the latency baseline; no streaming B4 or B8 circuit was run.

| Actual harness circuit | Logical qubits | T gates | T-depth | Clifford+T depth |
|---|---:|---:|---:|---:|
| Matched compact SSA control | 92,475 | 95,684,806 | 774,992 | 2,241,133 |
| Date boundaries, retained | 37,186 | 191,150,372 | 5,575,494 | 17,461,870 |
| Two-date blocks, dominated | 72,241 | 197,537,956 | 8,859,182 | 27,347,230 |

The native72/fraction40 function,12 independent32-bit midpoint uniform words, original Box–Muller pairs and coefficient tables are fixed. Current raw log words equal the original modular prefix sums. Clipping applies only to temporary exponential inputs. A reversible native stock-word sum preserves the original average rounding. A three-bit count retains every strict barrier violation; a basket equal to140 knocks out the path. Every in-place update, saved snapshot, rewind, redo, original leaf invocation and literal inverse is charged.

The reference passed12 tests, and the candidate suite passed61. Five actual date-streaming replays and one control replay passed, including full72-bit dirty output XOR, endpoint inputs, one positive-payoff path,2047 original SSA trace checks per streaming replay and restoration of all inputs, constants, Gaussian outputs, raw logs, Asian sum, counter and scratch. The prospectively fixed4096 endpoint combinations were checked classically; all had zero payoff. They are neither4096 gate replays nor evidence of exhaustive full-law gate coverage. A separate positive-payoff gate replay exercises the active output branch. The general argument uses modular identities, original source binding and legal reversible cleanup.

The first run failed26 stage tests because its fixture passed the compiler's return tuple as a source dictionary. It emitted no financial candidate. The original fixture and failure receipt remain immutable. A versioned fixture changes only tuple unpacking; the same two placements, precision, laws and acceptance rules then passed. The independent auditor reconstructed actual arrays and both direction costs, stage packing, allocation, copies, inverses, symbolic financial boundaries and nondominance.

Receipts: [reference](../../results/limitation_program_20261001/A19_reference_run001/summary.json), [preserved fixture failure](../../results/limitation_program_20261001/A19_run001/failed_tests.json), [bounded result](../../results/limitation_program_20261001/A19_run002/summary.json), [independent audit](../../results/limitation_program_20261001/A19_audit_run001/summary.json).

This completes the declared A19 harness screen. Logical memory savings do not supply a physical pricing latency gain. The original full-source scaling condition requires a compatible physical-cap comparison, which remains open. The autonomous queue therefore advances to source-compatible estimation and financial certification instead of scaling this slower harness prematurely. [Next packages](AUTONOMOUS_QUEUE.md).
