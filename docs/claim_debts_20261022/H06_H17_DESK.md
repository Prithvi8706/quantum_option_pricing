# H17 and H06 at the binding cell: necessary conditions (R1 desk)

22 October 2026. AI-assisted. **Rigour: R1 desk.** The record uses exact Fraction arithmetic on saved records, with
one self-check: it reproduces headline run006, window M = 26.076. It states necessary conditions only. TRIG-HWACT
stays dormant: there is no physical layout, no factory footprint and no architecture model.

**Cell:** B8x52, ε = $0.001, at the primary conventions:
- W = 1e7 qubits;
- supply 1e12 T/s;
- t_layer 100 ns;
- T_C = 8.886 s;
- σ/e = 11,518.66.

**Window estimator:**
- k = 8.762 (certified window), N = k·σ/e = 100,925 calls;
- k = 9.058 (quantum-only mean), 104,332 calls.

**Model.** This is the same model as headline_m and the N1 hardware card. Each call costs max(L·t_layer, T_call/R),
where L is the reaction layers per call and R is the magic-state rate. Then M = N·max(...)/(T_C/10). Each condition
below holds the other resource unlimited. So each is **necessary** for M ≤ m, and together they are sufficient
within this model.

## H17: the two necessary-condition columns (PLAN_110: "required T/s and width become necessary-condition columns", plus the reaction time)

All rows are for the certified window, k = 8.762. The quantum-only mean needs about 3.4% tighter values; both classes
are in the JSON.

| Iterate | L per call | T per call | Bound at primary | M (primary) | Reaction time per layer needed for M ≤ 1 / ≤ 10 | Magic-state rate needed for M ≤ 1 / ≤ 10 | Width / 1e7 | Label |
|---|---:|---:|---|---:|---|---|---:|---|
| W0 floor, supply-aware design (used in the headline) | 760 | 229,603,168 | supply | **26.08** | 11.6 ns / 116 ns | **2.61e13** / 2.61e12 T/s (26× / 2.6× the 1e12 budget) | 1.00 | mod, q+ |
| W0 floor, min-depth design | 740 | 322,810,048 | supply | 36.66 | 11.9 ns / 119 ns | 3.67e13 / 3.67e12 T/s | — | mod, q+ |
| Saved A10 source (F + F⁻¹; per-call iterate T-depth) | 770,356 | 4,267,435,214 | reaction | **8,749** | **11.4 ps** / 114 ps | 4.85e14 / 4.85e13 T/s | 0.45 | meas. T excludes the selector and reflection T, so it is q+ by that amount (C11 hook) |

How to read the table:
- **Floor.** M ≤ 1 needs reaction layers of about **12 ns**, 8.6 times faster than 100 ns. It also needs about
  **2.6e13 T/s**, 26 times the assumed factory supply. These are joint requirements. Relaxing either one alone leaves
  M > 1.
- **Saved circuit as emitted.** It is reaction-bound: 770,356 T-layers per call. M ≤ 1 would need about
  **11 ps per layer**, which is 8,749 times faster than 100 ns.

## H06: AND/CCZ versus T composition and a CCZ-native supply column

**Composition.** In the floor family the T count is 2 × 4 × the forward ANDs, with no rotation T. So 100% of the
floor's T comes from ANDs:
- supply-aware design: 57,400,792 ANDs per call;
- min-depth design: 80,702,512 ANDs per call.

At the primary D_eff, that is 25,000 CCZ (AND) states per 100 ns layer, or 6.5e12 CCZ/s for M ≤ 1. The saved source
does not record an AND count. The CCZ column below treats every saved T as part of a 4-T AND: at most 1,066,858,803
ANDs per call (assm, q+).

**Supply conventions.** The table gives D_eff and M for each convention for supplying ANDs. The rate stays at
1e12 units/s. The best recorded primary-law design (W1e7, base, Box-Muller) is taken in each column.

| Convention | Units per AND | Floor D_eff | Floor M (window) | Floor M (quantum-only mean) | All-free M | Saved source M |
|---|---:|---:|---:|---:|---:|---:|
| Primary: an AND costs 4 T | 4 | 2,296.0 | **26.08** | 26.96 | 1.29 | 8,749 |
| CCZ factory, catalysed CCZ → 2T (Gidney & Fowler 2019; lit) | 2 | 1,148.0 | **13.04** | 13.48 | 1.29 | 8,749 |
| CCZ-native, 1 unit per CCZ (extreme, q+) | 1 | 760.0 (reaction-bound) | **8.63** | 8.92 | 1.29 | 8,749 |

The reaction-depth lower bound for the family is 740 layers, which gives M ≥ 8.40 under any supply convention.

Conclusions:
1. **A CCZ-native supply convention changes D_eff at the primary conventions,** because the floor is supply-bound.
   It lowers the window M to 13.0 (2T-equivalent) or 8.6 (extreme). That is a 2-3× favourable departure, still with
   M > 1.
2. **It does not move the all-free column** (D_eff 114, reaction-bound) **or the saved source** (reaction-bound). So
   H06 adds **no single-departure flip**, and the v4 statement "no single favourable departure reaches M ≤ 1" stands
   with a CCZ supply convention added.
3. **The factory-mix condition.** The floor iterate is entirely AND/Toffoli. A matched supply means CCZ (or 4 |T⟩)
   states at 25,000 per layer, or 6.5e12 CCZ/s for M ≤ 1. A T-only factory mix is the primary convention. Any
   architecture that delivers CCZ cheaper than 4 T moves M at most to the 8.4 reaction floor.

## What remains

- **C11 hook.** This run was made before the C11 compile summary existed. The saved-source T excludes the selector
  and reflection T. When `results/claim_debts_20261022/c11/run001/summary.json` exists, rerun as run003 and the
  script fills `c11_hook` automatically. The saved-source row is reaction-bound, so its M does not change unless the
  compiled T-depth differs.
- **R2.** Independent peer review. The rest of the hardware program (H03 reaction map, factory footprints, routing)
  stays dormant until TRIG-HWACT. The window M is 26 > 10 at 100 ns.
- **run001 is superseded.** Its CCZ columns searched all recorded `base|*` loader designs, including the free and alias
  loaders, which are departures, not the primary law. run002 restricts the search to the Box-Muller primary law and
  asserts that the primary convention reproduces D_eff = 2,296. The H17 columns are identical in both runs.

## Files and premises

| File | sha256 |
|---|---|
| `research/claim_debts_20261022/h06_h17/h06_h17_desk.py` | fd4ba2f510b8cc351c35dd582d7ab2d0188e015ad2b81481144d8f75c885e05b |
| `results/claim_debts_20261022/h06_h17/run002/h06_h17.json` (current) | f8b130662aad5e2f64f5eb56fe09927a827f9acc09c4a0753d5bc63849fc3e9b |
| `results/claim_debts_20261022/h06_h17/run001/h06_h17.json` (superseded) | 41b2228a083b7fe5a279795e44ee87adc8f3916768bcca9f7152626d789e891a |
| premise `results/plan110_w0/ws_floor/floor.json` | 469b2a19ccf5e7c678c44a155f64dfc4c3ea3f0032d368032d3c3f66a49e8229 |
| premise `results/plan110_w0/ws_small/bias_desk_run001/bias_desk.json` (per-call iterate T-depth 770,356) | 5bc61e9b3003a6d1e23e9ad5f4477c3b3187c33cec38f636fb6b86f792bd835d |
| premise `results/frontier_probe_20261021/headline/run006/headline_table.json` | fd1eba885642fa61fae7cdc6abf67b875ed395d5c2bfd9c4cbfdd07c73057c7c |
| premise `results/frontier_probe_20261021/p2/run003_self_mean/p2c_self_mean.json` | 184cfe14576b6b48d443aca6dca7aec44a0a52c64ca84009acf02fcf1cf11dec |

Run from the worktree root:

```bash
../../../.context/frontier_t0_env/Scripts/python.exe -I -S -B research/claim_debts_20261022/h06_h17/h06_h17_desk.py run002
```
