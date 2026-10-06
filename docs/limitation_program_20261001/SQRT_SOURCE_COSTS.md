# Independent unsigned square-root source audit

The local A11 screen was independently checked against actual emitted arrays, the accepted A09 baseline and the unchanged target. All four preregistered variants were reconciled in both cases; this audit adds no financial or gate replay.

| Case | Selected variant | T gates | T change | Compact T-depth | Clifford+T depth | Logical qubits / cap |
|---|---|---:|---:|---:|---:|---:|
| B4x12 | tight-digit-by-digit__fused-child-copy | 633,939,334 | -14,888,160 | 979,360 | 2,860,691 | 550,141 / 550,141 |
| B8x52 | tight-digit-by-digit__fused-child-copy | 5,210,335,494 | -116,127,648 | 1,029,082 | 3,026,413 | 4,460,481 / 4,460,481 |

The predeclared complete-source rule requires at least 2% T-depth reduction in each case, no Clifford+T depth increase and the current accepted logical qubit caps. A common variant is selected by summed T-depth, T work and qubits. Actual scans covered 64 unique gate arrays and 550 metadata locations.

All 30 B4x12 and 234 B8x52 square-root calls have their actual same-SSA input range recomputed against all literal lookup rows and declared input widths: nonnegative unsigned raw inputs below 2^46. Bit45 remains active and may be one; no signed46 reinterpretation is accepted. The external input/output registers remain72 bits, and existing SSA masks, storage, argument copies and output copies are identical to A09. Every fallback metadata and gate file and the target file match their baseline bytes.

For N=x*2^40, the integer restoring recurrence maintains prefix=q^2+r and 0<=r<2q+1. Processing the next base-four digit d gives candidate 4r+d, trial 4q+1 and q'=2q+t. Conditional subtraction yields the same invariant and uniquely selects floor(sqrt(N)). With86 radicand bits there are43 stages; all intermediate candidates fit45 unsigned remainder bits. Every remainder is allocated, counted and restored. Structural checks independently verify the fused compute/copy/reverse case and the repeated self-inverse child case, arbitrary-output XOR, unchanged high output bits and restored private workspace. Saved finite emitted tests and full-source replays support circuit realization; this is not exhaustive72 input enumeration.

## Final B4x12 ledger

Independent forward DAG T-depth: 310,888; compact argument/output copy CX: 2,184,396. Retained SSA qubits: 355,052; full external output: 72; peak private scratch: 195,017. Exact same-SSA self-products: 144.

| Category | T gates | Overlapping capped T-depth diagnostic |
|---|---:|---:|
| uniform_preparation | 0 | 0 |
| scalar_normals | 317,727,900 | 451,618 |
| correlation | 7,930,272 | 86,560 |
| path_payoff | 308,281,162 | 441,182 |
| shared | 0 | 0 |

Top three deterministic depth-owner leaves:

- `bc7cb29c7fc457640cb1`: mul, {}, 344,528 attributed layers; hypothetical fixed-batch zero-cost saving 170,276.
- `294576c955e4ce59687d`: sqrt, {}, 211,164 attributed layers; hypothetical fixed-batch zero-cost saving 211,164.
- `3d4c35eaddb074bddc60`: shift, {}, 87,360 attributed layers; hypothetical fixed-batch zero-cost saving 74,512.
## Final B8x52 ledger

Independent forward DAG T-depth: 309,928; compact argument/output copy CX: 18,376,108. Retained SSA qubits: 2,943,448; full external output: 72; peak private scratch: 1,516,961. Exact same-SSA self-products: 1,248.

| Category | T gates | Overlapping capped T-depth diagnostic |
|---|---:|---:|
| uniform_preparation | 0 | 0 |
| scalar_normals | 2,478,277,620 | 451,618 |
| correlation | 59,480,512 | 76,352 |
| path_payoff | 2,672,577,362 | 501,112 |
| shared | 0 | 0 |

Top three deterministic depth-owner leaves:

- `bc7cb29c7fc457640cb1`: mul, {}, 358,648 attributed layers; hypothetical fixed-batch zero-cost saving 107,460.
- `294576c955e4ce59687d`: sqrt, {}, 211,164 attributed layers; hypothetical fixed-batch zero-cost saving 211,164.
- `3d4c35eaddb074bddc60`: shift, {}, 122,304 attributed layers; hypothetical fixed-batch zero-cost saving 102,656.

Category depth diagnostics overlap and cannot be summed. Owner/zero-cost diagnostics identify candidate work; they do not claim attainable independent gains. Canonical serial and actual compact executed resources were separately reconciled.

Use the newly recomputed complete-source owner ranking for the next bounded local screen. An exact same-SSA squaring replacement for remaining variable products is a candidate; cmul/shift alternatives need their own leaf proof and full-source cap/replay check. Carry exact T work and width into G5 before asserting physical runtime improvement.

G2 continuous-dollar certification, G3 compatible99% estimator scheduling, G4 matched classical timing and G5 physical10x runtime accounting remain unresolved. This circuit improvement does not establish quantum advantage. Everything remained local.

Receipts: [summary](../../results/limitation_program_20261001/A01_run007/summary.json), [complete audit](../../results/limitation_program_20261001/A01_run007/), [auditor](../../research/limitation_program_20261001/reconcile_sqrt.py).
