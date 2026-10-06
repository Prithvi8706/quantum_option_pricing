# Independent exact square source audit

The local same-SSA square screen was independently checked against actual emitted arrays, the accepted A11 circuits and unchanged financial targets. The sole preregistered Brent-Kung candidate was reconciled in both cases. This audit adds no financial or gate replay.

| Case | Candidate T gates | T change | Candidate T-depth | T-depth gain | Candidate CT-depth | Qubits / cap | Eligible |
|---|---:|---:|---:|---:|---:|---:|---|
| B4x12 | 605,771,782 | -28,167,552 | 961,916 | 1.7812% | 2,812,949 | 550,141 / 550,141 | False |
| B8x52 | 4,966,216,710 | -244,118,784 | 1,012,802 | 1.5820% | 2,984,383 | 4,460,474 / 4,460,481 | False |

The acceptance rule was at least 2% complete capped T-depth reduction separately in both cases, no Clifford+T depth increase, current qubit caps and at least one measured work/space improvement. The candidate failed the depth gate; A11 remains the accepted source. No new financial replay was run, as preregistered. The exact leaf remains available as a component.

Actual scans covered 61 unique gate arrays and 222 metadata locations. All 144 B4x12 and 1,248 B8x52 changed calls have actual repeated SSA operands. The native interface keeps two separate 72-bit arguments and one 72-bit arbitrary-XOR output, with unchanged compact masks, storage and copy counts. Every other target, metadata and gate file matches A11 bytes, including the accepted narrowed square root, generic prefix multiplier and all 32 literal lookup rows.

For signed x, expanding x*x gives diagonal bit x_i at column 2i and doubled cross terms x_i*x_j at column i+j+1. Only pairs containing the sign bit have negative cross weights. Complementing those bits plus the fixed modulo 2^112 correction 2^72 gives the exact low 112 product bits; all low 40 columns remain in CSA carrying before the final shift. The array parser checked each of 56 diagonal CX terms, every offdiagonal CCX, all 40 sign complements, the correction, every CSA carry, the full 112-bit frozen clean prefix adder, the 72 output copies and the literal reverse sequence. Thus all private workspace is counted and restored, with arbitrary output XOR. This combines an all-word polynomial argument with structural and finite emitted-test evidence; it is not exhaustive 72-bit input enumeration.

## Effective B4x12 ledger

Source: `results/limitation_program_20261001/A11_run001/B4x12`. T gates: 633,939,334; T-depth: 979,360; Clifford+T depth: 2,860,691; qubits: 550,141. Independent forward DAG depth: 310,888; compact argument/output copyCX: 2,184,396. Retained SSA storage: 355,052; named output: 72; peak private scratch: 195,017.

| Category | T gates | Overlapping capped T-depth diagnostic |
|---|---:|---:|
| uniform_preparation | 0 | 0 |
| scalar_normals | 317,727,900 | 451,618 |
| correlation | 7,930,272 | 86,560 |
| path_payoff | 308,281,162 | 441,182 |
| shared | 0 | 0 |

Top deterministic depth-owner leaves:

- `bc7cb29c7fc457640cb1`: mul, {}, 344,528 attributed layers; hypothetical fixed-batch zero-cost saving 170,276.
- `294576c955e4ce59687d`: sqrt, {}, 211,164 attributed layers; hypothetical fixed-batch zero-cost saving 211,164.
- `3d4c35eaddb074bddc60`: shift, {}, 87,360 attributed layers; hypothetical fixed-batch zero-cost saving 74,512.
## Effective B8x52 ledger

Source: `results/limitation_program_20261001/A11_run001/B8x52`. T gates: 5,210,335,494; T-depth: 1,029,082; Clifford+T depth: 3,026,413; qubits: 4,460,481. Independent forward DAG depth: 309,928; compact argument/output copyCX: 18,376,108. Retained SSA storage: 2,943,448; named output: 72; peak private scratch: 1,516,961.

| Category | T gates | Overlapping capped T-depth diagnostic |
|---|---:|---:|
| uniform_preparation | 0 | 0 |
| scalar_normals | 2,478,277,620 | 451,618 |
| correlation | 59,480,512 | 76,352 |
| path_payoff | 2,672,577,362 | 501,112 |
| shared | 0 | 0 |

Top deterministic depth-owner leaves:

- `bc7cb29c7fc457640cb1`: mul, {}, 358,648 attributed layers; hypothetical fixed-batch zero-cost saving 107,460.
- `294576c955e4ce59687d`: sqrt, {}, 211,164 attributed layers; hypothetical fixed-batch zero-cost saving 211,164.
- `3d4c35eaddb074bddc60`: shift, {}, 122,304 attributed layers; hypothetical fixed-batch zero-cost saving 102,656.

Category depth diagnostics overlap and cannot be added. Owner and zero-cost diagnostics identify candidate work; they do not establish separately attainable gains. Canonical serial and actual compact executed resource counts were reconciled separately.

Stop this square-only source branch under its predeclared >=2% both-case threshold; retain A11 unchanged. Keep the exact leaf as a separately proved reusable component. Choose the next dominant generic multiplication or shift limitation from the current accepted owner ranking; any future combined experiment requires a fresh protocol.

G2 continuous-dollar certification, G3 compatible99% estimator scheduling, G4 matched classical timing and G5 physical10x runtime accounting remain unresolved. This circuit screen does not establish quantum advantage. Everything remained local.

Receipts: [summary](../../results/limitation_program_20261001/A01_run008/summary.json), [complete audit](../../results/limitation_program_20261001/A01_run008/), [auditor](../../research/limitation_program_20261001/reconcile_square.py).
