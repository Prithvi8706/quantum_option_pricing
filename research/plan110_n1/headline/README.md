# N1-headline scripts

This folder holds the R1 recompute scripts. The outputs and the receipt are in `results/plan110_n1/headline/`, which has its own README.md and receipt.md.

| Script | Step |
|---|---|
| `e07_keff.py` | (2a) Exact-rational k_eff from the E07 rule, with π enclosed by BBP and M taken from the closed-form root. It reproduces 983,025 calls. |
| `floor_sheet.py` | (1) The analytic reaction-layer floor and T count per clean call and per Grover iterate, built from literature primitives cited in the docstring, plus the supply-limited D_eff. |
| `headline_m.py` | (2b, 3, 4) T_C from C2/C5 with a monotone envelope, the measured H16 ratios, the k classes, the M table, the sensitivity columns, the minimal stacked departures and the comparison with W0. |

Run them under `.context/frontier_t0_env/Scripts/python.exe -I -S -B`. They use the stdlib only. No W0 script was run or imported.
