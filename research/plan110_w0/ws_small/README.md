# WS-small (plan110 W0): C02 + A07/G2 bias desk, C14 depth closure, H16 grid runner

Rigour R0 screen. Rows: `results/plan110_w0/ws_small/rows.jsonl` (8 rows). Numbers: `results/plan110_w0/ws_small/bias_desk_run001/bias_desk.json`, with input SHA-256s, from `bias_desk.py` under `.context/frontier_t0_env/Scripts/python.exe -I -S -B`. Self-check: the recomputed totals match the certified totals, with a relative difference of 1.7e-16 or less.

## A1. B8x52 bias bound $0.001239557505461456, by term (measured: certified record terms)

The bound is `Total = H_price + zeta + 40*P_switch`, where `P_switch = sum over dates of (Gaussian closed-band probability + relevant_pairs*(4*DS + 2/N))`.

| Term | $ | Share |
|---|---|---|
| 40 × Gaussian closed barrier band | 0.000863 | 69.6% |
| 40 × pair-law radius KS (4·DS per pair) | 0.000129 | 10.4% |
| 40 × pair-law grid (2/N per pair) | 0.000116 | 9.3% |
| H_price polar angle grid (C·(dates+1)/N per pair) | 0.000112 | 9.0% |
| zeta smooth payoff | 0.0000149 | 1.2% |
| H_price radius KS | 0.0000047 | 0.4% |

B4x12 ($0.000205) splits the same way: 87% Gaussian band and 7% zeta. Its bias/eps is 0.205 at $0.001, so B4x12 is already eligible.

**The loose term.** The Gaussian band width, and also zeta, are set by `ell = 2^-16`. That is the leak from the native stock lower clamp, `exp(-11.09)`. Its relative band width `ell/140 = 1.1e-7` is 180-3,000 times the multiplicative arithmetic envelope (3e-11 to 6e-10). So `ell` drives 71% of the B8 bound.

## A1. Tightening to ≤ $0.00055 (modelled, quantum-favourable)

- **Lower the stock clamp by k binades** (`ell = 2^-(16+k)`). B8 totals: k=2 gives $0.000582, which misses the target; **k=3 gives $0.000473 (0.47 eps)**; k=8 gives $0.000367. The minimum is k = 3, a clamp literal of -13.17.
  - **Depth cost: about 0%** (modelled; 0.01% assumed upper bound) of the 770,356 per-call depth. No word or grid bits are added. The exponent count interval goes from [-17,12] to [-20,12], which is still inside the adopted signed7 shift-count contract [-64,63]. The 72-bit/f40 words already resolve 2^-40. The shift floor is charged additively (beta), so alpha does not change.
  - **Cost is re-certification only:** an A02 bridge rerun (stock classes 30→33) and A07/A13 interval re-proofs.
- **Better bounding with no source change.** Split the lower-clip event out of the band. The clip is about a 50-sigma event under continuous GBM. This gives $0.000363, provided a hybrid-law tail bound is proven (the tail term is assumed negligible).
- **Structural floor at the current N=2^32 and DS:** about $0.00036.
  - q33 alone gives $0.00113, which misses the target.
  - Cap 40 → 38.818 is free but saves only 2.6%.

## A2. C14 "2× forward" reading: closed as an error (measured)

`555,774 / 663,704` is already forward F plus literal inverse F: 277,887 + 277,887 and 331,852 + 331,852. This is recomputed from the per-batch ASAP depths in E02_financial_run002.

**Correct per-call depth.** One controlled Grover iterate is F + selector + CZ + selector⁻¹ + F⁻¹ + uniform reflection:
- B4x12: **571,034**, which is 1.0275 × the source depth;
- B8x52: **770,356**, which is 1.1607 × the source depth.

C14's 1,111,548 / 1,327,408 overstate the per-call depth by 1.95× / 1.72×.

The iterate binds the **same** A10 min-depth source (SHA match), so the gap-ledger note "older source" is wrong.

The B8 excess is the 105,148-layer linear CCX ladder in the 15,022-wire reflection. A log-depth reflection would give about 664k (modelled).

## B. H16 grid runner (authored; only `--dry-run` executed)

`h16_worker_grid.py` reuses C2's `all16`, `wait_idle`/`NotIdleError`, `warm_up`/`wait_workers` and C2's measured-confirmation accuracy rule. It times `preint` at W = 16, 8, 4, 2, 1 for B4x12 and B8x52 at eps = $0.01 (20 reps) and $0.001 (5 reps); $0.03 is opt-in with `--eps`.
- Scrambles are paired across W, with the new root 2026101116.
- Output is checkpointed per row with exclusive create under `results/plan110_w0/ws_small/h16_grid/<run>/`.
- Estimated upper runtime is **1.37 h** (1.55 h with $0.03).
- The dry-run self-check passed: `score()` reproduces C2's T_C from C2's own runs.

Run it on an idle machine on AC power:

```
cd C:/Users/prith/quantum_option_pricing
.context/frontier_t0_env/Scripts/python.exe -B -m research.plan110_w0.ws_small.h16_worker_grid --run run001
```

Use the T0 env: it is 3.12.4 with numpy 2.0.2 and numba, and matches the C2 meta. Do not use `venv/`, which is 3.9 with no numba. Do not pass `-I`/`-S`.
