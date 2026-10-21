# Independent prefix-multiplier source audit

The completed local A09 screen was independently checked against actual leaf arrays and frozen task/call categories. Both variants were checked at both accepted baseline caps. This audit adds no financial or gate replay.

| Case | Selected variant | T gates | T change | Compact T-depth | Clifford+T depth | Logical qubits / cap |
|---|---|---:|---:|---:|---:|---:|
| B4x12 | brent-kung | 648,827,494 | +20,724,480 | 1,218,582 | 3,569,495 | 550,141 / 550,150 |
| B8x52 | brent-kung | 5,326,463,142 | +170,631,552 | 1,268,304 | 3,735,217 | 4,460,481 / 4,460,481 |

The predeclared rule requires at least 2% complete-source T-depth reduction separately in both cases, no Clifford+T depth increase and the prior actual qubit caps. A single variant is chosen by summed T-depth, then T gates, then qubits. Extra T gates are permitted by that experiment and are fully reported; a shallower source does not establish a faster physical runtime. Actual scans covered 62 unique arrays and 330 metadata locations.

For the full signed72/f40 product, the independent coefficient certificate matches 4,688 retained partial terms and 82 negative terms. Complementing each negative Boolean term adds a fixed weight; correction 4722366482869645213696 (bits [72]) cancels it modulo 2^112. Every low column is retained through carrying. Euclidean division proves bit extraction implements floor(signed(a)*signed(b)/2^40) modulo 2^72, including negative products. No narrowed input or zero-low-bit promise is introduced.

Actual emitted partial gates match those coefficients and correction. The outer output is touched by exactly one contiguous full-width CX copy block, never controls a gate, and the surrounding computation/uncomputation segments are literal reverses. This proves arbitrary-output XOR behavior and complete input/workspace restoration structurally for the compute-copy-reverse circuit. Remaining functional circuit equivalence is supported by the saved finite leaf tests and selected full-source replay receipts; signed72 inputs are not exhaustively enumerated.

## Final B4x12 ledger

Independent forward DAG T-depth: 430,499; compact argument/output copy CX: 2,184,396. Retained SSA qubits: 355,052, external output: 72, peak private scratch: 195,017. Actual same-SSA self-products: 144; complete signatures and occurrences are saved.

| Category | T gates | Overlapping capped T-depth diagnostic |
|---|---:|---:|
| uniform_preparation | 0 | 0 |
| scalar_normals | 332,616,060 | 690,840 |
| correlation | 7,930,272 | 86,560 |
| path_payoff | 308,281,162 | 441,182 |
| shared | 0 | 0 |

Top three deterministic depth-owner leaves:

- `64238d79903cb4f6c9b6`: sqrt, {}, 450,386 attributed layers; hypothetical fixed-batch zero-cost saving 450,386.
- `bc7cb29c7fc457640cb1`: mul, {}, 344,528 attributed layers; hypothetical fixed-batch zero-cost saving 170,276.
- `3d4c35eaddb074bddc60`: shift, {}, 87,360 attributed layers; hypothetical fixed-batch zero-cost saving 74,512.
## Final B8x52 ledger

Independent forward DAG T-depth: 429,539; compact argument/output copy CX: 18,376,108. Retained SSA qubits: 2,943,448, external output: 72, peak private scratch: 1,516,961. Actual same-SSA self-products: 1,248; complete signatures and occurrences are saved.

| Category | T gates | Overlapping capped T-depth diagnostic |
|---|---:|---:|
| uniform_preparation | 0 | 0 |
| scalar_normals | 2,594,405,268 | 690,840 |
| correlation | 59,480,512 | 76,352 |
| path_payoff | 2,672,577,362 | 501,112 |
| shared | 0 | 0 |

Top three deterministic depth-owner leaves:

- `64238d79903cb4f6c9b6`: sqrt, {}, 450,386 attributed layers; hypothetical fixed-batch zero-cost saving 450,386.
- `bc7cb29c7fc457640cb1`: mul, {}, 358,648 attributed layers; hypothetical fixed-batch zero-cost saving 107,460.
- `3d4c35eaddb074bddc60`: shift, {}, 122,304 attributed layers; hypothetical fixed-batch zero-cost saving 102,656.

Every call is attributed once using frozen categories; category depths overlap and cannot be serially summed. Batch owners and zero-cost diagnostics guide the next bounded screen and do not represent attainable independent speedups. Canonical serial source resources and actual compact executed resources were reconciled as separate scopes. The source format, financial target bytes, precision, law and fallback leaves remain unchanged.

Use the recomputed full-source owner ranking to screen square root or remaining cmul/shift separately at the current accepted caps. Exact self-products remain a squaring alternative; any circuit replacement needs its own bounded proof/tests and complete-source selection. If extra T work was accepted for shallower multiplication, carry that exact increase into the physical factory/runtime ledger before claiming speedup.

G2 continuous-dollar certification, G3 the explicit compatible 99% estimator schedule, G4 matched classical target timing and G5 physical 10× runtime accounting remain unresolved. All work stayed local.

Receipts: [summary](../../results/limitation_program_20261001/A01_run006/summary.json), [complete audit](../../results/limitation_program_20261001/A01_run006/), [producer](../../research/limitation_program_20261001/reconcile_prefix.py).
