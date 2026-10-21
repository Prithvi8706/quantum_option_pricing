# Independent signed7-count shift source audit

The sole local signed7-count barrel-shift candidate was reconciled against actual emitted arrays, the accepted A11 circuits and unchanged financial targets. This audit runs no new financial or gate replay.

| Case | Candidate T gates | T change | Candidate T-depth | T-depth gain | Candidate CT-depth | Qubits / cap | Eligible |
|---|---:|---:|---:|---:|---:|---:|---|
| B4x12 | 629,425,006 | -4,514,328 | 936,810 | 4.3447% | 2,781,579 | 550,141 / 550,141 | True |
| B8x52 | 5,172,716,094 | -37,619,400 | 969,512 | 5.7887% | 2,912,185 | 4,460,481 / 4,460,481 | True |

The predeclared rule requires at least 2% complete capped T-depth reduction separately in both cases, no Clifford+T-depth increase, the current actual qubit caps and T work or scratch improvement for every changed clean leaf. The candidate passed and all four saved full-source replays were reconciled.

The scanner checked 61 unique gate arrays and 220 metadata locations. All 78 B4x12 and 650 B8x52 shift-count arguments have actual validated SSA intervals within [-64,63], without sampling. The native interface keeps two distinct full 72-bit arguments and one full 72-bit arbitrary-XOR output. Compact masks, retained storage and argument/output copy counts are unchanged. Every nonspecialized metadata and gate file matches A11 bytes, including narrowed sqrt, generic prefix multiplication and all 32 literal lookup rows.

Magnitude arithmetic uses unsigned 7-bit words: the signed minimum -64 becomes unsigned 64. Direction follows the financial IR: nonnegative counts shift left modulo 2^72; negative counts shift right arithmetically. Conditional bit reversal before and after one left-shift barrel gives the negative direction, with fill equal to count-sign AND original data-sign. Each conditional stage shifts by 2^j with exact fill and a difference ancilla restored immediately for reuse. Their composition yields the declared digital shift for all 72-bit data under the guard. Actual forward gate parsing checks magnitude construction, both reversals, every mux stage, signed fill, 72 output CX gates and the literal reverse cleanup. The largest magnitude 64 is smaller than 72, which justifies removing the oversized-count branch only under this proved contract.

## Effective B4x12 ledger

Source: `results/limitation_program_20261001/A07_shift_run001/B4x12`. T gates:629,425,006; T-depth:936,810; Clifford+T-depth:2,781,579; qubits:550,141. Independently recomputed forward DAG depth:302,378; compact argument/output copyCX:2,184,396. Retained SSA storage:355,052; named output:72; peak private scratch:195,017.

| Category | T gates | Overlapping capped T-depth diagnostic |
|---|---:|---:|
| uniform_preparation | 0 | 0 |
| scalar_normals | 315,991,620 | 443,108 |
| correlation | 7,930,272 | 86,560 |
| path_payoff | 305,503,114 | 407,142 |
| shared | 0 | 0 |

Top deterministic depth-owner leaves:

- `bc7cb29c7fc457640cb1`:mul,{},344,528 attributed layers; hypothetical fixed-batch zero-cost saving172,580.
- `294576c955e4ce59687d`:sqrt,{},211,164 attributed layers; hypothetical fixed-batch zero-cost saving211,164.
- `8949b1865708cb2c154d`:cmul,{'c': 60222732077},81,952 attributed layers; hypothetical fixed-batch zero-cost saving12,640.
## Effective B8x52 ledger

Source: `results/limitation_program_20261001/A07_shift_run001/B8x52`. T gates:5,172,716,094; T-depth:969,512; Clifford+T-depth:2,912,185; qubits:4,460,481. Independently recomputed forward DAG depth:301,418; compact argument/output copyCX:18,376,108. Retained SSA storage:2,943,448; named output:72; peak private scratch:1,516,961.

| Category | T gates | Overlapping capped T-depth diagnostic |
|---|---:|---:|
| uniform_preparation | 0 | 0 |
| scalar_normals | 2,464,734,636 | 443,108 |
| correlation | 59,480,512 | 76,352 |
| path_payoff | 2,648,500,946 | 450,052 |
| shared | 0 | 0 |

Top deterministic depth-owner leaves:

- `bc7cb29c7fc457640cb1`:mul,{},358,648 attributed layers; hypothetical fixed-batch zero-cost saving107,460.
- `294576c955e4ce59687d`:sqrt,{},211,164 attributed layers; hypothetical fixed-batch zero-cost saving211,164.
- `9e25d8fc5dc5529e0efc`:cmul,{'c': 1067016148260},81,696 attributed layers; hypothetical fixed-batch zero-cost saving79,360.

Category depth diagnostics overlap and cannot be added. Zero-cost owner diagnostics do not establish attainable speedup. Serial and actual compact resource counts were reconciled separately.

Use the accepted full-source owner ranking for the next bounded local screen. Remaining generic multiplication, square-root and shift leaves require separate exact guarded replacements and full-cap screening. Keep G2-G5 open and carry measured T work and qubit use into physical accounting.

G2 continuous-dollar certification, G3 compatible99% estimator scheduling, G4 matched classical timing and G5 physical10x runtime accounting remain unresolved. This screen establishes no quantum advantage. Everything remained local.

Receipts:[summary](../../results/limitation_program_20261001/A01_run009/summary.json),[complete audit](../../results/limitation_program_20261001/A01_run009/),[auditor](../../research/limitation_program_20261001/reconcile_shift.py).
