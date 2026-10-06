# Independent signed-range multiplication audit

Both complete native arguments remain 72 bits. The narrowed signed plane is allowed only when both actual SSA intervals fit their selected signed widths. The complement correction is reduced modulo the full 112-bit product width; every low carry is retained. The audit parsed every actual partial, correction, compressor, prefix gate, output copy and literal inverse, and ran no new gate or pricing replay.

| Portfolio | Case | T gates | T-depth | T-depth gain | CT-depth | Qubits / cap | Eligible |
|---|---|---:|---:|---:|---:|---:|---|
| mixed40 | B4x12 | 539,737,534 | 725,350 | 7.8998% | 2,168,049 | 550,141 / 550,141 | True |
| mixed24-40 | B4x12 | 521,330,110 | 719,916 | 8.5898% | 2,154,117 | 550,141 / 550,141 | True |
| mixed40 | B8x52 | 4,427,035,662 | 754,372 | 8.0335% | 2,292,791 | 4,460,479 / 4,460,481 | True |
| mixed24-40 | B8x52 | 4,267,504,654 | 743,064 | 9.4120% | 2,264,545 | 4,460,479 / 4,460,481 | True |

Adopted `mixed24-40` after both-case eligibility and four saved complete-source replays.

Use the accepted complete-source owner ranking for the next bounded local limitation. Keep G2-G5 open and everything local.

G2 continuous-dollar certification, G3 compatible 99% estimator schedule, G4 matched classical timing and G5 physical runtime accounting remain unresolved. This audit establishes no quantum advantage. Everything stayed local.

Receipts: [summary](../../results/limitation_program_20261001/A01_run012/summary.json), [complete audit](../../results/limitation_program_20261001/A01_run012/), [auditor](../../research/limitation_program_20261001/reconcile_range.py).
