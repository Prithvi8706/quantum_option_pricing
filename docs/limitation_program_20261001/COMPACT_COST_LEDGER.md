# Reconciled compact-source cost ledger

Local A01 follow-up, 1 October 2026. The accepted A06 compact sources were independently checked against frozen original tasks, node categories and immutable leaf hashes. No gate replay was repeated. The same exact financial IR, precision and arithmetic leaves remain; lower argument-copy CX and different memory packing account for the resource change. The untouched source.json still describes its canonical full-width serial implementation; schedule_capped.json describes the accepted compact execution.

| Case | T gates | Compact T-depth | Clifford+T depth | Actual logical qubits / cap | Retained SSA qubits | Saved copy CX | Batches |
|---|---:|---:|---:|---:|---:|---:|---:|
| B4x12 | 632,258,326 | 2,074,246 | 6,162,945 | 550,150 / 550,158 | 355,052 | 526,620 | 173 |
| B8x52 | 5,191,385,654 | 2,272,184 | 6,768,275 | 4,460,481 / 4,460,490 | 2,943,448 | 4,214,972 | 183 |

All X/CCX/T counts remain unchanged. source_gates, CX and expanded Clifford CX each decrease by exactly the saved copy count. Every active-bit width/offset/mask, actual leaf argument/output register, omitted-output scratch wire, zero-low input promise, call occurrence, dependency wave, batch depth and peak allocation reconciles. External named outputs remain full width; one-bit SSA flags do not cause accidental one-bit external-output allocation.

## B4x12 attribution

| Category | Clean T gates | Clean argument-copy CX | Copy CX saved | Overlapping capped T-depth diagnostic |
|---|---:|---:|---:|---:|
| uniform_preparation | 0 | 0 | 0 | 0 |
| scalar_normals | 322,783,020 | 1,116,840 | 377,880 | 987,760 |
| correlation | 7,930,272 | 72,576 | 0 | 86,560 |
| path_payoff | 301,545,034 | 994,908 | 148,740 | 999,926 |
| shared | 0 | 0 | 0 | 0 |

Top three deterministic depth-owner operations: mul (901,824 attributed layers), cmul (565,280 attributed layers), sqrt (450,386 attributed layers).

Top three individual depth-owner leaves:

- `9d1f0ace5d924241b3d0`: mul, params `{}`, 901,824 attributed layers; its optimistic frozen-batch zero-cost saving is 823,004 layers.
- `64238d79903cb4f6c9b6`: sqrt, params `{}`, 450,386 attributed layers; its optimistic frozen-batch zero-cost saving is 450,386 layers.
- `18e3e6a4b0b5c576252e`: cmul, params `{"c": 1586259972792}`, 315,008 attributed layers; its optimistic frozen-batch zero-cost saving is 307,022 layers.

Independent forward DAG depth remains 496,883. The ledger checks 320 retained one-bit values, 72 named-output qubits and peak private scratch of 195,026. Existing A06 evidence contains 4 complete replay records for this case; this audit reuses them.

## B8x52 attribution

| Category | Clean T gates | Clean argument-copy CX | Copy CX saved | Overlapping capped T-depth diagnostic |
|---|---:|---:|---:|---:|
| uniform_preparation | 0 | 0 | 0 | 0 |
| scalar_normals | 2,517,707,556 | 8,711,352 | 2,947,464 | 987,760 |
| correlation | 59,480,512 | 614,016 | 0 | 76,352 |
| path_payoff | 2,614,197,586 | 9,050,668 | 1,267,508 | 1,208,072 |
| shared | 0 | 0 | 0 | 0 |

Top three deterministic depth-owner operations: mul (909,216 attributed layers), cmul (712,864 attributed layers), sqrt (450,386 attributed layers).

Top three individual depth-owner leaves:

- `9d1f0ace5d924241b3d0`: mul, params `{}`, 909,216 attributed layers; its optimistic frozen-batch zero-cost saving is 667,244 layers.
- `18e3e6a4b0b5c576252e`: cmul, params `{"c": 1586259972792}`, 472,512 attributed layers; its optimistic frozen-batch zero-cost saving is 453,472 layers.
- `64238d79903cb4f6c9b6`: sqrt, params `{}`, 450,386 attributed layers; its optimistic frozen-batch zero-cost saving is 450,386 layers.

Independent forward DAG depth remains 495,923. The ledger checks 2,524 retained one-bit values, 72 named-output qubits and peak private scratch of 1,516,961. Existing A06 evidence contains 2 complete replay records for this case; this audit reuses them.

Category depths overlap within batches and are not serial elapsed-time sums. Deterministic batch ownership is additive bookkeeping only, with tie effects; frozen-batch zero-cost rows are optimistic prioritization diagnostics. Repacking or a different leaf can change the remaining maxima. No independent speedup factors are multiplied.

Next: finish the already proved seven-bit logarithm-exponent integration, verify the resulting complete compact schedules, and rerank. The current operation ranking prioritizes multiplication, other expensive constants and square root. Source validity is an arithmetic result; G2 continuous-dollar certification, G3 an explicit compatible estimator, G4 actual matched classical target timing and G5 physical resources remain unresolved. All work stayed local.

Receipts: [summary](../../results/limitation_program_20261001/A01_run004/summary.json), [complete accounting](../../results/limitation_program_20261001/A01_run004/), [producer](../../research/limitation_program_20261001/compact_ledger.py). The frozen original [baseline](BASELINE.md) and its manifests remain unchanged.
