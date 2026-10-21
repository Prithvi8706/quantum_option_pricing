# N1-headline: R1 recompute of the DP1 headline

This folder holds the R1 independent recompute (12 October 2026). The previous run of this workstream was cut off by a logout. It left only `e07_keff.py`, which had not been run and had written no outputs, so this run executed everything fresh.

**Result:** DP1 NO-GO is confirmed. The details are in `receipt.md`.
- Primary M with the best explicit constant is **232**, at B8x52 $0.001, using the more quantum-favourable floor. This run's own floor alone gives 364.
- Reaching M ≤ 1 with an explicit constant needs **3 stacked departures**. For example, the all-free oracle plus zero bias plus one lane against one core gives M = 0.506.

## Files

| File | What it holds | Produced by |
|---|---|---|
| `keff.json` | Exact-rational k_eff for every cell, with the E07 rule reproduced: 983,025 calls at ε = 0.01 | `research/plan110_n1/headline/e07_keff.py` |
| `floor_sheet.json` | The analytic idealized clean-call floor, stage by stage, at W = 1e6, 1e7, 1e8 and unlimited, supply 1e11-1e13 T/s, and t_layer 10 ns-10 µs | `research/plan110_n1/headline/floor_sheet.py` |
| `headline_table.json` | T_C, the H16 ratios, the k classes, D_eff (this run, W0, and the value used), the M table with sensitivity columns, the stacked departures and the comparison with W0 | `research/plan110_n1/headline/headline_m.py` |
| `receipt.md` | The R1 receipt: what agrees, the logged discrepancies, and the verdict | written by hand from the JSON files above |
| `rows.jsonl` | One row per sub-result, with labels and directions | appended by all three scripts, plus a final receipt row |

Run the scripts in this order: `e07_keff.py`, then `floor_sheet.py`, then `headline_m.py`. Use `.context/frontier_t0_env/Scripts/python.exe -I -S -B`. Each script creates its outputs with exclusive create and refuses to overwrite them.
