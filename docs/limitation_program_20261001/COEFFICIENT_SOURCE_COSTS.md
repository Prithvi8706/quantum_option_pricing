# Independent full-domain coefficient audit

The fixed top-three coefficient frontier uses the same native signed 72-bit input and arbitrary 72-bit XOR output, with all 112 product columns retained. Each exact binary or signed-digit expansion, complemented sign/correction term, Cuccaro or compressor/prefix gate, native output copy and literal inverse was independently parsed from actual arrays. Existing guarded multiplication, root, shift and 32-row lookup metadata and gates remain byte-identical. This audit ran no new emitted gate or pricing replay.

| Portfolio | Case | T gates | T-depth | T-depth gain | CT-depth | Qubits / cap | Eligible |
|---|---|---:|---:|---:|---:|---:|---|
| min-depth | B4x12 | 520,720,662 | 555,774 | 22.8002% | 1,661,253 | 550,141 / 550,141 | True |
| min-work | B4x12 | 520,062,438 | 559,596 | 22.2693% | 1,673,157 | 550,141 / 550,141 | True |
| min-depth | B8x52 | 4,267,435,214 | 663,704 | 10.6801% | 2,026,465 | 4,460,479 / 4,460,479 | True |
| min-work | B8x52 | 4,267,411,862 | 664,952 | 10.5121% | 2,030,205 | 4,460,479 / 4,460,479 | True |

Adopted `min-depth` after both-case eligibility and four saved complete-source replays.

Use the accepted full-source owner ranking for the next bounded local limitation. Keep G2-G5 open and everything local.

G2 continuous-dollar certification, G3 compatible 99% estimator schedule, G4 matched classical timing and G5 physical runtime accounting remain unresolved. This audit establishes no quantum advantage. Everything stayed local.

Receipts: [summary](../../results/limitation_program_20261001/A01_run014/summary.json), [complete audit](../../results/limitation_program_20261001/A01_run014/), [auditor](../../research/limitation_program_20261001/reconcile_coefficients_v2.py).
