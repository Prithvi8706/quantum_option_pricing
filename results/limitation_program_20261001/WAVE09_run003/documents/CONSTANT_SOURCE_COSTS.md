# Independent constant-source cost reconciliation

The completed local logarithm and inverse-ln2 screens were independently audited against every actual leaf array, the frozen original call categories, same target bytes, unchanged fallback metadata/gates and compact schedules. This audit runs no new gate or pricing replay. The source manifest's full-width serial accounting and the actual compact schedule remain separate scopes.

| Screen | Case | Selected strategy | T gates | Compact T-depth | Clifford+T depth | Actual logical qubits / cap |
|---|---|---|---:|---:|---:|---:|
| log | B4x12 | signed-digit-carry-save | 631,729,126 | 2,074,246 | 6,162,945 | 550,150 / 550,150 |
| log | B8x52 | signed-digit-carry-save | 5,187,257,894 | 2,272,184 | 6,768,275 | 4,460,481 / 4,460,481 |
| inverse | B4x12 | signed-digit-carry-save | 628,103,014 | 1,773,574 | 5,260,905 | 550,150 / 550,150 |
| inverse | B8x52 | signed-digit-carry-save | 5,155,831,590 | 1,824,984 | 5,426,165 | 4,460,481 / 4,460,481 |

All four candidates per case were checked, including rejection reasons, complete-source Pareto eligibility and the predeclared ordering. Actual gate-resource scans covered 67 unique arrays and 939 metadata locations. Exact argument/output register mapping includes retained one-bit SSA values, full-width external outputs and omitted-output wires counted as private scratch. Count identities include seven T/six CX/two H per CCX. All forward call totals, compact copies, every batch and the independent weighted DAG reconcile.

The signed7 promise is proved independently from the same guarded-log SSA chain: MSB is in0..71, its exponent after subtracting40 is in-40..31, and shift40 gives low40 zeros and the required sign extension. All72 MSB outcomes verify that interface. This proof applies to the operand promise; archived finite arbitrary-output gate replays and leaf tests remain finite correctness checks. The exponential calls sharing ln2 retain their original signed32 fallback. Generic inverse-ln2 replacements retain the complete signed72 domain and floor/shift semantics with no nonzero low-bit or narrow-range promise.

## Final B4x12 ledger

| Category | Clean T gates | Argument-copy CX | Overlapping capped T-depth diagnostic |
|---|---:|---:|---:|
| uniform_preparation | 0 | 0 | 0 |
| scalar_normals | 322,253,820 | 1,116,840 | 987,760 |
| correlation | 7,930,272 | 72,576 | 86,560 |
| path_payoff | 297,918,922 | 994,908 | 699,254 |
| shared | 0 | 0 | 0 |

Independent forward DAG T-depth: 459,299. Compact argument/output copy CX: 2,184,396. Retained SSA qubits: 355,052; named output: 72; peak private scratch: 195,026.

There are 144 actual same-SSA self-products. Their complete producer signatures, occurrence indices and current leaf resources are saved in the final ledger. Exact repeated operands establish a squaring opportunity, not an accepted squaring circuit or a capped-source saving.

Top three deterministic depth-owner leaves:

- `9d1f0ace5d924241b3d0`: mul, {}, 901,824 attributed layers; optimistic frozen-batch zero-cost saving 823,004.
- `64238d79903cb4f6c9b6`: sqrt, {}, 450,386 attributed layers; optimistic frozen-batch zero-cost saving 450,386.
- `3d4c35eaddb074bddc60`: shift, {}, 87,360 attributed layers; optimistic frozen-batch zero-cost saving 65,376.
## Final B8x52 ledger

| Category | Clean T gates | Argument-copy CX | Overlapping capped T-depth diagnostic |
|---|---:|---:|---:|
| uniform_preparation | 0 | 0 | 0 |
| scalar_normals | 2,513,579,796 | 8,711,352 | 987,760 |
| correlation | 59,480,512 | 614,016 | 76,352 |
| path_payoff | 2,582,771,282 | 9,050,668 | 760,872 |
| shared | 0 | 0 | 0 |

Independent forward DAG T-depth: 458,339. Compact argument/output copy CX: 18,376,108. Retained SSA qubits: 2,943,448; named output: 72; peak private scratch: 1,516,961.

There are 1248 actual same-SSA self-products. Their complete producer signatures, occurrence indices and current leaf resources are saved in the final ledger. Exact repeated operands establish a squaring opportunity, not an accepted squaring circuit or a capped-source saving.

Top three deterministic depth-owner leaves:

- `9d1f0ace5d924241b3d0`: mul, {}, 916,608 attributed layers; optimistic frozen-batch zero-cost saving 671,052.
- `64238d79903cb4f6c9b6`: sqrt, {}, 450,386 attributed layers; optimistic frozen-batch zero-cost saving 450,386.
- `3d4c35eaddb074bddc60`: shift, {}, 122,304 attributed layers; optimistic frozen-batch zero-cost saving 84,384.

Category depths overlap and cannot be serially summed. Batch ownership is deterministic attribution with tie effects; frozen-batch zero-cost savings are hypothetical, not measured improvements. The table records complete-source resources only, with no multiplication of independent leaf speedups.

Use the actual same-SSA self-product ledger to test an exact signed72 fixed-point squaring leaf with floor-after40-bit semantics, arbitrary-output XOR and cleanup. Compare it with the unchanged variable multiplication leaf first; if valid and worthwhile, replace only proved self-products and measure the complete compact source at the current accepted caps. General variable multiplication and sqrt remain separate alternatives; their hypothetical zero-cost screens do not count as measured gains.

Arithmetic improvement leaves G2 continuous-dollar error certification, G3 an explicit compatible99% estimator schedule, G4 matched actual classical timing and G5 physical10× runtime inequality unresolved. All receipts and code stayed local; no historical evidence or progress ledger was edited.

Receipts: [summary](../../results/limitation_program_20261001/A01_run005/summary.json), [full audit](../../results/limitation_program_20261001/A01_run005/), [producer](../../research/limitation_program_20261001/reconcile_constants.py).
