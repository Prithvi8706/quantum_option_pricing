# N1-headline receipt: R1 independent recompute of the DP1 decision

12 October 2026. This is workstream N1-headline under `research/plan110_n1/N1_CARD.md`, at rigour R1: an independent recompute along a different path, with this receipt. The conventions are the ones in `research/plan110_w0/W0_CARD.md`. The W0 scripts were not run, read or imported. W0 outputs were read only to compare against at the end.

## Verdict

**DP1 NO-GO is confirmed.** The recompute agrees with DP1 on the primary margin, the binding cell and the minimal number of stacked departures.

- **The binding cell.** In the best eligible, non-overhead cell (B8x52 at $0.001), the best explicit-constant estimator gives **M = 232**. This is the more quantum-favourable of the two floors, which is W0's here. The independent floor alone gives M = 364.
- **Departures needed.** With an explicit constant, reaching M ≤ 1 needs **at least 3 favourable departures stacked together**. The best pair is the all-free oracle plus one lane against one core, which still gives M = 1.13. DP1's example, the all-free oracle plus zero bias plus one lane against one core, recomputes to M = 0.506; DP1 gave 0.51.

M = k / k_10x, and M ≤ 1 means a 10× complete-latency win. Here k_10x = T_C / (10 (σ/e) D_eff t_layer), and D_eff is the effective Grover-iterate depth: max(reaction depth, T per iterate / (supply × t_layer)).

## What was recomputed, and how the path differs

| Step | N1 path | Result | Label |
|---|---|---|---|
| (1) Oracle floor | An analytic formula sheet (`floor_sheet.py`) built from cited literature structures, detailed below. | B4x12: compute 270 layers, 2.26e7 T per call; Grover iterate 563 layers. B8x52: compute 278 layers, 1.87e8 T. At W = 1e7 the B8x52 iterate takes 1,409 layers and 3.6e8 T, so it is supply-bound: D_eff = 3,605 at 1e12 T/s. At unlimited width it takes 585 layers and 1.88e8 T, so D_eff = 1,875. | modelled; quantum-favourable (idealized) |
| (2a) k_eff, E07 rule | Exact rationals. π is enclosed with BBP, not Machin. M comes from the closed-form root of the quadratic, then is rounded up to a power of two. The failure tail is exact, with no 2^-40 grid. | **Reproduces the saved 983,025 calls** at ε = 0.01 (M = 65,536, 15 medians). Certified k is 585.8-1,066.7 at e = 0.45ε. | modelled-exact × measured σ |
| (2b) T_C | The minimum "primary" wall time over C2 (preint, rqmc) and C5 (oss_bb, oss), followed by a monotone envelope over tighter ε. | B8x52 at $0.001: 22.529 s, measured confirmation with preint. The envelope lowers the B4x12 and B8x52 values at ε = 0.03. | measured |
| (2b) H16 ratio | Median wall time with 1 worker divided by median wall time with 16 workers, taken from the run001 rows. | 6.44-10.24×, the same as W0. | measured |
| (3) k classes | Certified: the N1 value. Explicit best: the minimum over the WS-k part3 worst-case explicit methods. No-explicit: the minimum over window and QSP methods, at estimator failure 0.003 and at 0.01. Separately, 48 of the WS-k non-dyadic worst-case rows were recomputed with N1 arithmetic: **48/48 match exactly**. | Explicit best at B8x52 $0.001 is 197.6 (span 8192/211, with the price+L1 mean credit and non-dyadic M). | modelled |

### How the floor sheet works

- **Gates and timing.**
  - Each AND costs 4 T and one reaction layer (Jones 2013; Gidney 2018).
  - Only reaction layers take time; Clifford gates are free (Fowler 2012).
- **Arithmetic blocks.**
  - Adders are Kogge-Stone carry-lookahead. Multi-operand sums use Dadda 3:2 trees.
  - Multipliers are truncated fixed-point multipliers and FMAs.
  - Constant multiplications use canonical signed digits.
  - Coefficients are fetched with a QROM lookup (Babbush 2018).
  - Functions are piecewise Chebyshev polynomials evaluated with Estrin's scheme: ln, sqrt and cos/sin for Box-Muller, and 2^r for the exponential. Each (degree, segment count) pair is chosen against a 2^-41 error bound.
- **The call, stage by stage:**
  1. uniform preparation;
  2. Box-Muller;
  3. correlation, kept in carry-save form;
  4. prefix log-spots;
  5. clip;
  6. exponential;
  7. the basket and barrier branch, run in parallel with the payoff sum;
  8. flag and mask;
  9. comparator encoding.
- **One Grover iterate** is one uncompute plus one compute, plus the S0 reflection. Only the reflections are controlled.
- **Width.** Each stage either keeps its AND garbage or cleans it locally and recomputes it in A†. All keep/clean choices are enumerated under W, and the one with the lowest D_eff is kept.
- **Loader share.** Box-Muller is 52-53% of the compute critical path. W0 reported 36-56%.

## Comparison with W0 (the 10% rule)

Agreement within 10% counts as agreement. Where the two disagree by more, the more quantum-favourable value was adopted and the discrepancy is logged below.

| Quantity | N1 | W0 | Within 10%? | Used |
|---|---|---|---|---|
| E07 calls at ε = 0.01 | 983,025 | 983,025 (saved certificate) | yes, exact | equal |
| Certified k, all 16 cells | identical to 1e-12 | identical | yes | equal |
| T_C, eligible non-overhead cells | 0.1244 / 2.688 / 0.5535 / 22.529 s | same | yes | equal |
| H16 one-core ratio | 6.44 / 9.36 / 7.38 / 10.24 | same | yes | equal |
| D_eff, B4x12 primary (W = 1e7, 1e12 T/s, 100 ns) | 563 (reaction-bound) | 364 | **no** | W0 (364) |
| D_eff, B8x52 primary (W = 1e7, 1e12 T/s, 100 ns) | 3,605 (supply-bound) | 2,296 | **no** | W0 (2,296) |
| D_eff, B8x52 at unlimited width, 1e12 T/s | 1,875 | 2,296 | **no** | **N1 (1,875)** |
| D_eff, all-free oracle (B4x12 / B8x52, W = 1e7) | 141 / 163 | 94 / 114 | **no** | W0 |
| D_eff, B4x12 primary at 1e11 T/s | 2,265 | 3,380 | **no** | N1 |
| D_eff, all 180 convention pairs | n/a | n/a | 15 of 180 agree; N1 is more favourable in 33 | the minimum, per pair |
| **M primary, explicit, B8x52 $0.001** | **232.0** (own floor alone: 364.2) | 232.0 | yes, once the favourable D is used | **232** |
| M primary, certified, B8x52 $0.001 | 801.5 (own floor alone: 1,258) | 801.5 | yes, once the favourable D is used | 801 |
| M primary, no-explicit, B8x52 $0.001 | 8.62 at failure 0.01; 10.26 at 0.003 | 8.62 | yes at 0.01 | 8.62 |

## Discrepancies logged

1. **The two floors differ by more than 10% in 165 of 180 convention pairs.**
   - At the primary conventions, N1's own floor is 1.55-1.57× less favourable than W0's.
   - The main cause is that N1 puts a carry-propagate adder after every Estrin level, with an FMA depth of 19. N1 also uses 72-bit words throughout.
   - W0's leaf choices are deeper-optimized: a merged prefix, narrower tables and a supply-aware design.
   - Per the rule, the more quantum-favourable value is used, so the claim stays conservative. Using N1's own floor alone would raise every M by about 1.5×.
2. **Unlimited or 1e8 width, B8x52.**
   - The N1 floor is the more favourable one here: T per iterate is 1.88e8 against W0's 2.30e8.
   - The best explicit M at W ≥ 1e8 is therefore **189.5**. W0's unlimited-width value would give 232.
   - This does not change the verdict.
3. **Inconsistent estimator failure allocation in WS-k.**
   - The window/QSP class value of 8.62 uses estimator failure 0.01. The explicit class (197.6) and the E07 protocol use 0.003.
   - Under a consistent 0.01 allocation, the medians drop from 15 to 11 (computed exactly here), and the explicit M becomes **170.1**.
   - Under a consistent 0.003 allocation, the window M becomes **10.26**.
   - Neither change affects NO-GO. The headline keeps the DP1 convention: explicit 232, window 8.62. The 0.01 allocation is reported as a further favourable departure.
4. **A reporting quirk in the W0 decision table.** At B4x12 ε = 0.03, `decision_summary.json` prints the raw T_C of 0.12677 s, but its k_10x uses the envelope value of 0.12440 s. M is unaffected, and N1 reproduces it exactly.
5. **W = 1e6.** The N1 sheet is infeasible for B8x52, because the persistent registers alone take 3.4e6 qubits. W0's value is used: D_eff = 11,034.

## Sensitivity: minimum M over eligible, non-overhead cells

All of these use the explicit-best class with the favourable D_eff.

| Column | M |
|---|---:|
| Primary | 232.0 |
| 1 lane against 1 core (H16) | 22.7 |
| Distribution-free classical ×2 / ×5 (assumed range, C09 b) | 116.0 / 46.4 |
| e = ε (zero deterministic bias) | 104.4 |
| All-free oracle | 11.5 |
| W = 1e6 / 1e8 | 648 (B4x12) / 189.5 |
| Supply 1e11 / 1e13 T/s | 1,978 (B4x12) / 74.8 |
| t_layer 10 ns / 1 µs / 10 µs | 197.8 (B4x12) / 748 / 7,476 |
| B8x52 $0.001 ineligible (current $0.00124 bound) | 318.0 (B4x12 $0.001) |

For the other classes:
- **Certified:** primary 801.5. The minimum takes 3 departures (all-free + 1 lane against 1 core + distribution-free ×5), giving 0.777.
- **No-explicit (window/QSP):** primary 8.62. A single departure gets below 1: the all-free oracle gives 0.43 (at failure 0.003 it gives 0.51), and 1 lane against 1 core gives 0.84 (at failure 0.003 it gives 1.002).

### Minimal stacked departures to M ≤ 1 with an explicit constant

All of these sets have 3 departures. No set of 2 reaches M ≤ 1.

| Departures | M |
|---|---:|
| all-free + 1 lane against 1 core + distribution-free ×5 | 0.225 |
| all-free + zero bias (e = ε) + 1 lane against 1 core | **0.506** (DP1: 0.51) |
| all-free + 1 lane against 1 core + 10 ns layers | 0.714 |
| all-free + 1 lane against 1 core + estimator failure 0.01 | 0.825 |

The best pair is all-free + 1 lane against 1 core, at M = 1.125.

## Files

All files are in `results/plan110_n1/headline/`, and each one records the SHA256 of its inputs.
- `keff.json`: exact k_eff for every cell, plus the reproduction of 983,025.
- `floor_sheet.json`: the formula-sheet floor, stage by stage, at each width, supply and layer time.
- `headline_table.json`: the M table, the sensitivity columns, the stacked departures, the WS-k spot checks, the D_eff comparison table and the comparison with W0.
- `rows.jsonl`: one row per sub-result.

The scripts are in `research/plan110_n1/headline/`. They were run under `.context/frontier_t0_env/Scripts/python.exe -I -S -B` (3.12.4, stdlib and fractions only).
