# WS-floor: idealized clean-call reaction-layer floor (plan110 W0, R0 screen)

Items: A01, with A16, A09, A08, A02, A07, A13, F05, F20, A03 and A04 as parameters. Generated from `floor.json` by `render_md.py`. Every number below is **modelled** (idealized literature-constant constructions; quantum-favourable unless stated), except the D_max inputs (inherited from `gap_ledger.json`: T_C measured or fitted per cell) and the conventions (assumed, W0 card).

Unit: one **reaction layer** is one layer of parallel temporary-AND gates (A16). The call is forward plus reverse, so it is 2 x forward. **T-layers:** x1 with a T-depth-1 AND, x2 with a Gidney AND, x4 at the repo's measured CCX ratio of 4.0. Call T-count = 2 x 4 x forward ANDs.

## 1. Headline: floor per contract under each width (t_layer 100 ns)

| case | W | design | loader | call reaction layers | T-layers r=1/2/4 | loader share | T per call | width (qubits) | required T/s | supply-limited depth at 1e12 T/s |
|---|---|---|---|---|---|---|---|---|---|---|
| B4x12 | W1e6 | box_muller_current_law | box_muller | 742 | 742/1,484/2,968 | 41% | 2.82e+07 | 1.00e+06 | 3.80e+11 | 742 |
| B4x12 | W1e6 | icdf_A02 | icdf | 664 | 664/1,328/2,656 | 35% | 3.18e+07 | 1.00e+06 | 4.79e+11 | 664 |
| B4x12 | W1e6 | best_loader | alias_q10 | 456 | 456/912/1,824 | 5% | 2.09e+07 | 1.00e+06 | 4.59e+11 | 456 |
| B4x12 | W1e6 | free_loader_F05 | free | 432 | 432/864/1,728 | 0% | 1.99e+07 | 1.00e+06 | 4.60e+11 | 432 |
| B4x12 | W1e6 | box_muller+free_exp_A13 | box_muller | 406 | 406/812/1,624 | 75% | 1.56e+07 | 1.00e+06 | 3.84e+11 | 406 |
| B4x12 | W1e6 | best_loader+free_exp_A13 | alias_q10 | 126 | 126/252/504 | 19% | 2.71e+06 | 2.22e+05 | 2.15e+11 | 126 |
| B4x12 | W1e6 | box_muller+narrow_A07 | box_muller | 410 | 410/820/1,640 | 55% | 1.63e+07 | 1.00e+06 | 3.98e+11 | 410 |
| B4x12 | W1e6 | all_free_and_narrow | free | 94 | 94/188/376 | 0% | 3.18e+06 | 7.30e+05 | 3.39e+11 | 94 |
| B4x12 | W1e7 | box_muller_current_law | box_muller | 326 | 326/652/1,304 | 36% | 6.47e+07 | 5.28e+06 | 1.98e+12 | 364 |
| B4x12 | W1e7 | icdf_A02 | icdf | 290 | 290/580/1,160 | 28% | 6.00e+07 | 4.82e+06 | 2.07e+12 | 328 |
| B4x12 | W1e7 | best_loader | alias_q10 | 234 | 234/468/936 | 10% | 2.50e+07 | 2.35e+06 | 1.07e+12 | 236 |
| B4x12 | W1e7 | free_loader_F05 | free | 210 | 210/420/840 | 0% | 2.40e+07 | 2.35e+06 | 1.14e+12 | 212 |
| B4x12 | W1e7 | box_muller+free_exp_A13 | box_muller | 216 | 216/432/864 | 54% | 4.64e+07 | 5.23e+06 | 2.15e+12 | 246 |
| B4x12 | W1e7 | best_loader+free_exp_A13 | alias_q10 | 124 | 124/248/496 | 19% | 6.82e+06 | 1.32e+06 | 5.50e+11 | 124 |
| B4x12 | W1e7 | box_muller+narrow_A07 | box_muller | 270 | 270/540/1,080 | 41% | 3.76e+07 | 3.55e+06 | 1.39e+12 | 298 |
| B4x12 | W1e7 | all_free_and_narrow | free | 94 | 94/188/376 | 0% | 3.18e+06 | 7.30e+05 | 3.39e+11 | 94 |
| B4x12 | unlimited | box_muller_current_law | box_muller | 258 | 258/516/1,032 | 33% | 3.36e+10 | 4.15e+09 | 1.30e+15 | 364 |
| B4x12 | unlimited | icdf_A02 | icdf | 222 | 222/444/888 | 22% | 3.26e+10 | 4.03e+09 | 1.47e+15 | 328 |
| B4x12 | unlimited | best_loader | alias_q10 | 198 | 198/396/792 | 12% | 4.14e+08 | 5.12e+07 | 2.09e+13 | 236 |
| B4x12 | unlimited | free_loader_F05 | free | 174 | 174/348/696 | 0% | 4.13e+08 | 5.12e+07 | 2.37e+13 | 212 |
| B4x12 | unlimited | box_muller+free_exp_A13 | box_muller | 184 | 184/368/736 | 46% | 3.32e+10 | 4.15e+09 | 1.81e+15 | 246 |
| B4x12 | unlimited | best_loader+free_exp_A13 | alias_q10 | 124 | 124/248/496 | 19% | 6.82e+06 | 1.32e+06 | 5.50e+11 | 124 |
| B4x12 | unlimited | box_muller+narrow_A07 | box_muller | 206 | 206/412/824 | 39% | 5.80e+10 | 4.03e+09 | 2.82e+15 | 298 |
| B4x12 | unlimited | all_free_and_narrow | free | 94 | 94/188/376 | 0% | 3.18e+06 | 7.30e+05 | 3.39e+11 | 94 |
| B8x52 | W1e6 | box_muller_current_law | box_muller | 11,034 | 11,034/22,068/44,136 | 50% | 4.58e+08 | 1.00e+06 | 4.15e+11 | 11,034 |
| B8x52 | W1e6 | icdf_A02 | icdf | 9,274 | 9,274/18,548/37,096 | 40% | 4.27e+08 | 1.00e+06 | 4.60e+11 | 9,274 |
| B8x52 | W1e6 | best_loader | alias_q10 | 5,658 | 5,658/11,316/22,632 | 2% | 2.57e+08 | 1.00e+06 | 4.55e+11 | 5,658 |
| B8x52 | W1e6 | free_loader_F05 | free | 5,562 | 5,562/11,124/22,248 | 0% | 2.41e+08 | 1.00e+06 | 4.33e+11 | 5,562 |
| B8x52 | W1e6 | box_muller+free_exp_A13 | box_muller | 5,658 | 5,658/11,316/22,632 | 97% | 2.38e+08 | 1.00e+06 | 4.22e+11 | 5,658 |
| B8x52 | W1e6 | best_loader+free_exp_A13 | alias_q10 | 268 | 268/536/1,072 | 27% | 2.15e+07 | 1.00e+06 | 8.04e+11 | 268 |
| B8x52 | W1e6 | box_muller+narrow_A07 | box_muller | 3,124 | 3,124/6,248/12,496 | 57% | 1.16e+08 | 1.00e+06 | 3.73e+11 | 3,124 |
| B8x52 | W1e6 | all_free_and_narrow | free | 128 | 128/256/512 | 0% | 7.24e+06 | 1.00e+06 | 5.66e+11 | 128 |
| B8x52 | W1e7 | box_muller_current_law | box_muller | 740 | 740/1,480/2,960 | 39% | 3.23e+08 | 1.00e+07 | 4.36e+12 | 2,296 |
| B8x52 | W1e7 | icdf_A02 | icdf | 668 | 668/1,336/2,672 | 33% | 2.95e+08 | 1.00e+07 | 4.41e+12 | 2,140 |
| B8x52 | W1e7 | best_loader | alias_q10 | 472 | 472/944/1,888 | 5% | 1.89e+08 | 1.00e+07 | 4.00e+12 | 1,293 |
| B8x52 | W1e7 | free_loader_F05 | free | 448 | 448/896/1,792 | 0% | 1.81e+08 | 1.00e+07 | 4.03e+12 | 1,211 |
| B8x52 | W1e7 | box_muller+free_exp_A13 | box_muller | 410 | 410/820/1,640 | 71% | 1.65e+08 | 1.00e+07 | 4.02e+12 | 1,219 |
| B8x52 | W1e7 | best_loader+free_exp_A13 | alias_q10 | 142 | 142/284/568 | 17% | 3.09e+07 | 3.35e+06 | 2.18e+12 | 215 |
| B8x52 | W1e7 | box_muller+narrow_A07 | box_muller | 316 | 316/632/1,264 | 35% | 1.20e+08 | 8.36e+06 | 3.79e+12 | 973 |
| B8x52 | W1e7 | all_free_and_narrow | free | 112 | 112/224/448 | 0% | 1.24e+07 | 1.85e+06 | 1.11e+12 | 114 |
| B8x52 | unlimited | box_muller_current_law | box_muller | 274 | 274/548/1,096 | 31% | 2.63e+11 | 3.24e+10 | 9.59e+15 | 2,296 |
| B8x52 | unlimited | icdf_A02 | icdf | 238 | 238/476/952 | 20% | 2.55e+11 | 3.14e+10 | 1.07e+16 | 2,140 |
| B8x52 | unlimited | best_loader | alias_q10 | 214 | 214/428/856 | 11% | 3.70e+09 | 4.44e+08 | 1.73e+14 | 1,293 |
| B8x52 | unlimited | free_loader_F05 | free | 190 | 190/380/760 | 0% | 3.69e+09 | 4.44e+08 | 1.94e+14 | 1,211 |
| B8x52 | unlimited | box_muller+free_exp_A13 | box_muller | 200 | 200/400/800 | 42% | 2.59e+11 | 3.24e+10 | 1.30e+16 | 1,219 |
| B8x52 | unlimited | best_loader+free_exp_A13 | alias_q10 | 140 | 140/280/560 | 17% | 1.65e+08 | 3.82e+07 | 1.18e+13 | 215 |
| B8x52 | unlimited | box_muller+narrow_A07 | box_muller | 222 | 222/444/888 | 36% | 4.75e+11 | 3.14e+10 | 2.14e+16 | 973 |
| B8x52 | unlimited | all_free_and_narrow | free | 110 | 110/220/440 | 0% | 8.71e+07 | 2.12e+07 | 7.92e+12 | 114 |

For reference, the current accepted source (A01_run014, measured):
- B4x12: capped call T-depth 5.56e+05, forward dependency T-depth 1.46e+05, T-count 5.21e+08, 5.50e+05 logical qubits.
- B8x52: capped call T-depth 6.64e+05, forward dependency T-depth 1.85e+05, T-count 4.27e+09, 4.46e+06 logical qubits.

## 2. Tenfold reach: k_10x = D_max(k=1) / floor (largest estimator constant that still reaches 10x)

W = 1e7, t_layer = 100 ns, e = 0.45 eps. `unl` means unlimited magic-state supply. `1e12` means the supply-limited depth at 1e12 T/s. F20 applies the zero-depth sigma credit (x4.5).

| case | eps | T_C (s) | T_C convention | D_max(k=1) | BM unl | BM 1e12 | best unl | best 1e12 | BM 1e12 +F20 | best 1e12 +F20 |
|---|---|---|---|---|---|---|---|---|---|---|
| B4x12 | 0.1 | 0.063 | measured small-n mark | 502 | 1.54 | 1.38 | 2.15 | 2.13 | 6.33 | 9.76 |
| B4x12 | 0.03 | 0.127 | measured small-n mark | 297 | 0.91 | 0.81 | 1.27 | 1.26 | 3.73 | 5.76 |
| B4x12 | 0.01 | 0.124 | measured confirmation | 99 | 0.30 | 0.27 | 0.42 | 0.42 | 1.24 | 1.92 |
| B4x12 | 0.001 | 2.688 | measured confirmation | 214 | 0.66 | 0.59 | 0.91 | 0.90 | 2.69 | 4.15 |
| B8x52 | 0.1 | 0.414 | measured small-n mark | 3,592 | 4.85 | 1.56 | 7.61 | 2.78 | 7.07 | 12.55 |
| B8x52 | 0.03 | 0.910 | measured small-n mark | 1,442 | 1.95 | 0.63 | 3.05 | 1.12 | 2.84 | 5.04 |
| B8x52 | 0.01 | 0.554 | measured confirmation | 481 | 0.65 | 0.21 | 1.02 | 0.37 | 0.95 | 1.68 |
| B8x52 | 0.001 | 22.529 | measured confirmation (bias bound ineligible; W0: eligible at zero bias) | 1,956 | 2.64 | 0.85 | 4.14 | 1.51 | 3.85 | 6.83 |

## 3. Loader share and alternative loaders (CRITIQUE F7)

Coarse model, base precision (72-bit word, 40-bit function precision). The table gives the forward loader depth and call floor for each loader. Loaders on a grid (alias, GR, A03, A04) change the law to a q-bit grid, so a new G2 is needed (assumed acceptable at q=10 per the A05 records).

| case | W | loader | forward loader depth | call floor | loader share | T per call |
|---|---|---|---|---|---|---|
| B4x12 | W1e7 | a03_gr_synth_q10 | 1.23e+05 | 2.46e+05 | 100% | 3.87e+07 |
| B4x12 | W1e7 | a04_mps_chi8_q10 | 5,760 | 11,730 | 98% | 1.62e+08 |
| B4x12 | W1e7 | alias_q10 | 12 | 234 | 10% | 2.50e+07 |
| B4x12 | W1e7 | alias_q16 | 12 | 234 | 10% | 8.70e+07 |
| B4x12 | W1e7 | alias_q20 | 169 | 548 | 62% | 1.03e+09 |
| B4x12 | W1e7 | box_muller | 58 | 326 | 36% | 6.47e+07 |
| B4x12 | W1e7 | free | 0 | 210 | 0% | 2.40e+07 |
| B4x12 | W1e7 | gr_qrom_q10 | 91 | 392 | 46% | 2.71e+07 |
| B4x12 | W1e7 | icdf | 40 | 290 | 28% | 6.00e+07 |
| B8x52 | W1e7 | a03_gr_synth_q10 | 1.23e+05 | 2.46e+05 | 100% | 2.96e+08 |
| B8x52 | W1e7 | a04_mps_chi8_q10 | 5,760 | 11,968 | 96% | 1.26e+09 |
| B8x52 | W1e7 | alias_q10 | 12 | 472 | 5% | 1.89e+08 |
| B8x52 | W1e7 | alias_q16 | 84 | 616 | 27% | 6.72e+08 |
| B8x52 | W1e7 | alias_q20 | 1,378 | 3,204 | 86% | 8.03e+09 |
| B8x52 | W1e7 | box_muller | 146 | 740 | 39% | 3.23e+08 |
| B8x52 | W1e7 | free | 0 | 448 | 0% | 1.81e+08 |
| B8x52 | W1e7 | gr_qrom_q10 | 91 | 630 | 29% | 2.05e+08 |
| B8x52 | W1e7 | icdf | 110 | 668 | 33% | 2.95e+08 |

## 4. Refinement: A01_run014 DAG reweight

Trigger rule: coarse call floor x k=3 <= 10 x D_max(k=1) at 100 ns in some cell. Result: B4x12 floor x 3 / D_max(k=1) = 1.40; B8x52 floor x 3 / D_max(k=1) = 0.39, so the refinement ran.

Self-check (measured): reweighting the DAG with the archived leaf T-depths reproduces the A01_run014 forward dependency T-depth: B4x12 1.46e+05 vs 1.46e+05 (match); B8x52 1.85e+05 vs 1.85e+05 (match).

| case | variant | forward (unlimited) | call (unlimited) | call W=1e7 | call W=1e6 | loader share (critical path / marginal) | free loader | free exp | both free | best substituted loader (forward) | T per call | required T/s (unlimited width) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B4x12 | a07_narrow | 564 | 1,128 | 1,128 | 1,160 | 54% / 54% | 258 | 453 | 147 | 269 (alias_q10) | 5.29e+07 | 4.69e+11 |
| B4x12 | as_is | 661 | 1,322 | 1,322 | 2,496 | 56% / 56% | 291 | 535 | 165 | 303 (alias_q10) | 1.42e+08 | 1.07e+12 |
| B8x52 | a07_narrow | 597 | 1,194 | 1,198 | infeasible (retention > W) | 51% / 51% | 291 | 486 | 180 | 302 (alias_q10) | 4.35e+08 | 3.64e+12 |
| B8x52 | as_is | 699 | 1,398 | 2,054 | infeasible (retention > W) | 53% / 53% | 329 | 573 | 203 | 341 (alias_q10) | 1.16e+09 | 8.32e+12 |

The DAG keeps the current algorithm. That means Horner log and cos, binary adders between every step, a max tree over dates, and a degree-12 exp with ln2 range reduction. So it gives the construction-anchored idealized floor. The coarse model restructures the algorithm: carry-save chains, Estrin with larger tables, an AND of comparisons, and a direct exp table. That is standard and quantum-favourable, so the coarse value is the floor of record.

## 5. Early-stop signal (W0 card; W = 1e7 rows; every width is in floor.json)

The early stop fires iff k_lat > max k_es, where k_es = 30 x D_max(k=1) / floor and the maximum is over cells, and over conventions in scope.

| W | floor | supply | scope | max k_es | max k_10x | at cell | t_layer | convention |
|---|---|---|---|---|---|---|---|---|
| W1e7 | all_free_and_narrow | supply_1e12 | all_conventions | 14,940.8 | 498.03 | B8x52 eps=0.1 | 10ns | e_eq_eps+f20 |
| W1e7 | all_free_and_narrow | supply_1e12 | primary | 945.2 | 31.51 | B8x52 eps=0.1 | 100ns | base |
| W1e7 | all_free_and_narrow | unlimited_supply | all_conventions | 96,584.6 | 3,219.49 | B8x52 eps=0.1 | 10ns | e_eq_eps+f20 |
| W1e7 | all_free_and_narrow | unlimited_supply | primary | 962.1 | 32.07 | B8x52 eps=0.1 | 100ns | base |
| W1e7 | best_loader | supply_1e12 | all_conventions | 836.7 | 27.89 | B8x52 eps=0.1 | 10ns | e_eq_eps+f20 |
| W1e7 | best_loader | supply_1e12 | primary | 83.3 | 2.78 | B8x52 eps=0.1 | 100ns | base |
| W1e7 | best_loader | unlimited_supply | all_conventions | 22,918.4 | 763.95 | B8x52 eps=0.1 | 10ns | e_eq_eps+f20 |
| W1e7 | best_loader | unlimited_supply | primary | 228.3 | 7.61 | B8x52 eps=0.1 | 100ns | base |
| W1e7 | box_muller_current_law | supply_1e12 | all_conventions | 471.1 | 15.70 | B8x52 eps=0.1 | 10ns | e_eq_eps+f20 |
| W1e7 | box_muller_current_law | supply_1e12 | primary | 46.9 | 1.56 | B8x52 eps=0.1 | 100ns | base |
| W1e7 | box_muller_current_law | unlimited_supply | all_conventions | 14,618.2 | 487.27 | B8x52 eps=0.1 | 10ns | e_eq_eps+f20 |
| W1e7 | box_muller_current_law | unlimited_supply | primary | 145.6 | 4.85 | B8x52 eps=0.1 | 100ns | base |

## 6. Caveats

- These are idealized literature constructions, **not lower bounds**. The multiplier's AND-degree bound (ceil(log2 2n) ~ 8 layers vs ~20 used) shows that the arithmetic could still shrink by up to ~2.5x. With truly unlimited width, any function of N input bits has AND-depth ceil(log2 N)+1 (~12-15 here) via an exponential-width lookup. Table address bits are therefore capped at 20.
- The ways the model favours quantum: Cliffords, fan-out, routing and the amplitude-encoding envelope cost zero; the discount and 1/(assets x dates) scaling are folded into the envelope; garbage cleanup overlaps downstream compute; 100 ns per reaction layer; and T-depth-1 ANDs.
- The ways the model works against quantum, or is simply crude: width is handled by uniform per-stage rounds or stage-local recomputation, and garbage is double-counted while cleanup overlaps. The W = 1e6 B8x52 numbers are dominated by this crude width model.
- Grid loaders (alias, GR, A03, A04) change the sampling law. Box-Muller and ICDF keep the 32-bit-uniform continuous law at the base precision. The A07 narrow widths (40-bit word, 24-bit precision) are unproved.
- T-count uses full (not truncated) multiplier partial products. Truncated fixed-point multipliers could cut the multiplier T by up to ~2x, which would lower the supply-limited depth by up to ~2x (quantum-favourable; not applied).
- The supply-limited depth is min over the depth-optimal and supply-aware designs of max(call, T_call/(R x t_layer)).
- The eps = 0.10 and 0.03 cells use overhead-dominated classical small-n marks (gap_ledger caveat). The most favourable k_10x values sit in those cells.
