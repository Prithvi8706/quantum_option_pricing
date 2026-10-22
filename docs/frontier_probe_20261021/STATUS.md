# Frontier probe, 21 October 2026: status

This probe ran P1 and P2 and then, because P2 cleared its target, the P3 desk estimate. It is an AI-assisted
probe on branch `claude/kind-carson-9eedd7`, which starts from `research/limitation-plan110-backlog` at
`10110ed9`. Nothing outside the three new `frontier_probe_20261021/` folders was written. The v3 draft, the
register, the DP1 memo, the receipts and `.context/` are untouched. The scope-#43 stop stands: no scope #44, U1
or U3 work.

All scripts are stdlib-only and ran under `.context/frontier_t0_env/Scripts/python.exe -I -S -B` (3.12.4) from the
repo root. Outputs were created with exclusive create (`run001`).

**Labels** follow the v3 number rule:
- meas (measured), mod (modelled), assm (assumed), lit (literature);
- q+ (quantum-favourable), q− (against quantum), 0 (neutral).

**Binding cell:** B8x52 at $0.001, under the primary conventions.

**Current numbers are round 2** (section "Round 2" at the end). Round 1 is kept below for the record.

| Probe | Result (round 2) | Verdict |
|---|---|---|
| P1: control-variate residual span (F20/F04) | Under consistent gain pairing, the best route nets **3.42** at D ratio 1 (clipped/hybrid preintegration) and **2.62** at the structure-aware D ratio of 1.30. Every closed-form control nets ≤ **1.59** | **Killed** (threshold 4). The R2 review upheld the narrow claims; its two open routes are now evaluated. Close F20/F04 |
| P2: explicit worst-case window constant | **c(0.003) = 4.179** for every N ≥ 800, with parts 1-4 explicit. Gives **k = 8.762** at the binding cell. The R2 review found no critical or major error | **Clears** the target. Explicit M falls from 232.0 to **10.29** |
| P3: oracle-cost desk estimate | With k = 8.762, M ≤ 1 needs D_eff ≤ **223 layers** and ≤ 2.2e7 T per iterate. Only designs with both the loader and the exponential near-free get there | Desk estimate only |

---

## P1: control-variate residual span (register F20, F04; v3 §6 lever 5)

**Question.** For a control g with a classically certifiable mean, how small can the worst-case range
S_res of the residual f − βg be, over the oracle's support and for any β? What is the net factor
(S/S_res)·(D_eff/D_eff,res)?

**Method.** Script: `research/frontier_probe_20261021/p1_control_span.py`. Outputs:
`results/frontier_probe_20261021/p1/run001/p1_span.json` and `rows.jsonl`.

- **Model.** The oracle's one-factor model:
  - log S_ij = ln S0 + j·m + a·ΣZc + b·ΣZi;
  - the payoff is f = e^{−rT}(A − K)^+·1{every date basket < H}, where A is the average over all assets and
    dates (the Stage C kernel).
- **Lower bounds on the span (the kill direction).** These come from explicit witness paths whose every
  normal satisfies |Z| ≤ 4.7. That is inside the q32 inverse-CDF grid (|Z| ≤ 6.5) and inside any Box-Muller
  pairing (radius 6.65 < 6.66).
  - f and the raw controls are evaluated in 50-digit decimal arithmetic.
  - F(β) = max over witness pairs of |Δf − βΔg| is convex and piecewise linear. Its exact minimum over **all**
    β is taken at the breakpoints, in exact rationals.
- **The U1-aware gain.** It replaces S by √(m(S−m)), the form the k = 197.6 row uses. It is bounded over every
  β on a 1e-3 grid with an endpoint argument per cell, plus a linear-growth argument in the tails.
- **Why the bound is large.** The witness pair (w_hi, w_ko) straddles the arithmetic-basket barrier. There f
  jumps from $38.635 to 0 while each control is continuous, so no β can cancel the jump. A closed-form control
  cannot carry the arithmetic-basket barrier on every date.
- **Controls** (means: mod, closed form, unless marked):
  - C1: geometric Asian-basket call;
  - C2a: the linear average A;
  - C2b: the barrier-free arithmetic call (mean from MC, assm);
  - C3a: a single-asset terminal knock-out call;
  - C3b: a geometric-average knock-out call;
  - C4: the preintegrated payoff h = E[f | y] used as a control. Its mean is the price itself, so it is not a
    valid control; it is shown only to confirm the argument.
- **F04, structured integration.** The first canonical PCA direction is integrated analytically, as in the
  classical comparator. The oracle then encodes h(y), or h − βĝ.
  - **Certified lower bound on sup h** (decimal monotone quadrature): at an explicit witness with |y| ≤ 4.65,
    in an alive, in-the-money interval verified at both ends.
  - **Analytic upper bound:** h(y) ≤ h*(z_H(y)), because every date basket for z < z_H is at most
    H·e^{−v_j(z_H−z)}.
  - **Universal lower bound** over any integration direction with nonnegative loadings (each loading
    ≤ σ√t_j): mod, on an unclamped support.

**Numbers (B8x52, the binding case; B4x12 is in the JSON).**

| Route | S_res lower bound | Gain S/S_res (linear) | Gain with U1 | D_eff,res / D_eff (desk) | Net, upper bound (D ratio floor 1) |
|---|---:|---:|---:|---:|---:|
| No control | 38.635 (S = 38.825) | 1.005 | n/a | 1 | 1.005 |
| C1 geometric call | 38.635 | 1.005 | 1.016 | 1.0014 | 1.016 |
| C2a linear A | 38.635 | 1.005 | 1.016 | 1.0001 | 1.016 |
| C2b arithmetic call | 38.635 | 1.005 | 1.016 | 1.0001 | 1.016 |
| C3a asset-1 terminal knock-out | 38.635 | 1.005 | 1.150 | 1.0001 | 1.150 |
| C3b geometric-average knock-out | 38.635 | 1.005 | 1.593 | 1.0014 | 1.593 |
| C4 preintegrated h as a control | 38.625 | 1.005 | n/a | n/a | n/a |
| **F04: encode h(y)** | **15.61** (upper bound 17.29) | **2.487** | 1.700 | **3.61** (T), 2.95 (reaction) | **2.49** (0.69 at the desk ratio) |
| F04: encode h − βĝ, any of C1-C3b | 15.6 | 2.485 | ≤ 1.719 | 3.61 | 2.49 |

Labels:
- **Spans and gains:** mod. They are rigorous lower bounds on the span from decimal witness values; the
  witness z-grid attainability by the discrete loader is argued, not emitted.
- **D ratios:** mod (desk), from the N1 floor-sheet stage Toffoli counts.
  - The closed-form controls add one exponential and a 416-word sum at most.
  - Coherent preintegration needs 53 root solves of at least 3 Newton steps each, plus 834 normal CDFs.
  - The kill does not use the D ratios: it holds at D ratio = 1 (q+).
- **Universal monotone-direction bound:** sup h ≥ 11.42, so the linear gain is ≤ 3.40 for any such direction
  (mod; unclamped). That is also below 4.
- **Measured σ** (plain MC, 16,384 paths, meas, 0): σ_f = 5.18. The variance-optimal controls give
  σ_f/σ_res = 1.02-1.18 only. The register's 4.5× is preintegration (σ_preint 1.146, meas), not a control.

**Against the thresholds** (M after the best route, consistent pairing): linear gain against the no-U1 k, U1
gain against the U1 k, D ratio 1 (q+).

| Threshold | Today | After the best route (F04 h) | After the best closed-form control (C3b) |
|---|---:|---:|---:|
| Box-Muller floor, primary | 232.0 | 136.5 | 145.6 |
| All-free floor | 11.5 | 6.78 | 7.23 |
| Symmetric distribution-free | 6.29 | 3.70 | 3.95 |

**Asymmetry.** The classical comparator already uses this preintegration (C2 `preint`). A preintegrated quantum
oracle therefore matches the classical method; it does not out-structure it.

**Kill.** No route reaches a net factor of 4. The best is 2.49 before the cost of coherent preintegration,
about 0.7 after it. **Recommendation: close F20 and F04 with this evidence.** F20's own kill rule is "close if the
credited miss stays ≥ 10x", and it is met: M ≥ 136 at the primary conventions.

---

## P2: explicit worst-case constant for window phase/amplitude estimation (v3 §6 lever 1; estimator card §5)

**Method.** Script: `research/frontier_probe_20261021/p2_window_constant.py`. Outputs:
`results/frontier_probe_20261021/p2/run001/p2_window.json` and `rows.jsonl`.

- **Window.** The Kaiser window w_n = I0(β√(1−(n/N)²)) for |n| < N, with half-weight end taps (pedestal
  fraction γ = 0; γ = 1 was also certified).
  - It uses exponents −N..N, so it costs N calls with direction-select (the WS-k convention).
  - For exactly N calls, the magnitude register uses a subset-sum step set {1, 2, 4, …, remainder}.
  - The continuous transform is closed form: 2 sinh(√(β²−η²))/√(β²−η²) − 2γ sin η/η.
- **Part 2 (concentration).** Poisson summation splits the window's DTFT into N·Φ(Nω) plus an explicit
  aliasing term R. The bound on R is |R| ≤ β²κ/(4N) + (1−γ)(2/π²)|ω|; the second part uses the exact identity
  for the half-weight rectangle, sin(Nω)·cot(ω/2), and cot(ω/2) − 2/ω has an all-same-sign Laurent series.
  - Expanding Σw_n² and the in-band energy exactly gives
    λ0 ≥ (N·I_c/2π − X_band) / (N·I_tot/2π + X + C_R²).
  - The corrections X, X_band and C_R are explicit and O(1) or O(1/N). Each, divided by N, decreases in N, so a
    bound certified at N0 = 800 holds for **every N ≥ 800**. This covers **part 1** too, with an explicit
    N0 below the smallest N the task uses.
  - **I_tot** is an exact rational series in (1−x²)^k, with a rational tail and a rational enclosure of π.
  - **I_c** uses the 50-digit decimal midpoint rule with the rigorous error term
    (2c)·h²·4Φ(0)²/24, using |Φ^(k)| ≤ ∫|x|^k φ ≤ Φ(0).
- **Part 3 (finite readout).** A G-point QFT (G ≥ 2N+1) plus a uniformly random, known register phase offset,
  which is query-free. This makes the success probability equal λ0 for every phase. It is the same argument as
  estimator card §2c.
- **Part 4 (implementation precision).** Not certified. A budget δ_impl = 1e-4 is reserved inside δ (assm).
- **Independent check.** Direct O(N²) float computation of the exact discrete concentration at N = 100, 400
  and 1000. The bound lies below the direct value in all 12 cases.
- **Literature** (one background agent; `results/frontier_probe_20261021/p2/lit_check.jsonl`, lit). These
  sources were checked:
  - Kothari-O'Donnell 2208.07544, Hamoudi 2108.12172, Rall 2103.09717, Kimmel-Low-Yoder 1502.02677,
    Belliardo-Giovannetti 2007.02994, AQAE 2407.16795;
  - RQAE 2204.13641 and Labib 2609.02715 (abstracts only).

  **None gives a worst-case coverage constant below canonical.** The best explicit one is AQAE Thm 2, with
  c(0.003) ≈ 409. Rall Prop 5 and Hamoudi Prop 4.1 are canonical plus medians, at about 97-110. The QSP, RMSE
  and maximum-likelihood routes have no certified constant.

**Numbers** (mod, q+ relative to today's explicit constant):

| Quantity | δ = 0.003 | δ = 0.01 |
|---|---:|---:|
| Certified c, every N ≥ 800 (Kaiser, γ = 0) | **4.178** (β = 3.87) | 3.509 (β = 3.19) |
| Same, with the 1e-4 part-4 budget | **4.197** | 3.515 |
| Kaiser-minus-pedestal (γ = 1), for comparison | 4.410 / 4.430 | 3.729 / 3.734 |
| WS-k DPSS value (uncertified, N = 400 numerics) | 4.168 | 3.502 |
| k at the binding cell (U1/U2 + direction-select, with budget) | **8.80** (N = 101,359 calls) | 7.37 |
| k without U1/U2 (span 64, no mean bound) | 25.9 | n/a |
| k without direction-select (exponents 0..2N) | 17.6 | n/a |

**Best certified k I can defend: 8.80**, at δ = 0.003 with the implementation budget. It is conditional on
the same U1/U2 credits as today's 197.6, on the direction-select call cost, and on part 4. It is not below the
counting floor of about 1.85. It is far below 187-198. **P2 clears its target.**

**Status of the certificate.** The derivation (Poisson split, aliasing bounds, monotonicity in N) is written
in the script docstring and code. It has been checked only numerically, against direct computation, and has
**not had an independent review**. Rigour is R0+: script plus receipt plus an independent numeric check.

---

## M recomputed (copy of headline_m.py)

Script: `research/frontier_probe_20261021/headline_m_probe.py`. It is a copy of
`research/plan110_n1/headline/headline_m.py`, whose sha `98e2259a…` is unedited. The changes are only:
- paths;
- the P2 classes;
- a per-cell Stage-C distribution-free column.

Output: `results/frontier_probe_20261021/headline/run001/headline_table.json`.

**Reproduction.** The copy reproduces every original M exactly (W0 comparison diff 0.000 in all 24 rows;
48/48 WS-k spot checks).

Binding cell, minimum over eligible non-overhead cells (mod):

| Class | k | Primary | All-free | 1 lane vs 1 core | Symmetric distribution-free (Stage C) | All-free + symmetric | e = ε | N1 floor alone |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Certified today | 682.7 | 801.5 | 39.8 | 78.3 | 21.7 | 1.08 | 400.7 | 1,258 |
| Explicit, canonical (U1 + U2 + non-dyadic) | 197.6 | 232.0 | 11.5 | 22.7 | 6.29 | 0.31 | 104.4 | 364.2 |
| **Window, certified here, δ = 0.003** | **8.80** | **10.33** | **0.513** | **1.009** | **0.280** | 0.014 | 4.65 | 16.2 |
| Window, certified here, δ = 0.01 | 7.37 | 8.65 | 0.430 | 0.845 | 0.234 | 0.012 | 3.89 | 13.6 |
| Window, certified, without U1/U2 | 25.9 | 30.4 | 1.51 | 2.97 | 0.82 | 0.04 | 13.7 | 47.8 |
| Window, certified, without direction-select | 17.6 | 20.7 | 1.03 | 2.02 | 0.56 | 0.03 | 9.30 | 32.4 |

Other results:
- **If the binding cell is ineligible**, so that B4x12 at $0.001 binds: window certified M = 14.16 (q−).
- **Minimal stacked departures to M ≤ 1, certified window class: one.**
  - Symmetric distribution-free: 0.28.
  - All-free floor: 0.51.
- **Explicit canonical class:** two departures, the best being all-free + symmetric at 0.31.
- **Certified-today class:** three departures.

## P3: desk estimate of oracle cuts (no circuit building)

Script: `research/frontier_probe_20261021/p3_oracle_desk.py`. Output:
`results/frontier_probe_20261021/p3/run001/p3_desk.json`.

**Method.** At fixed k, M is linear in D_eff (mod, q+). With the certified window (k = 8.80), M ≤ 1 needs
D_eff ≤ **222 layers** and ≤ **2.2e7 T per iterate**, against today's 2,296 (supply-bound, 2.3e8 T).

| Existing modelled design (B8x52, W = 1e7, 1e12 T/s, 100 ns) | D_eff | M (window, δ = 0.003) | M (window, δ = 0.01) |
|---|---:|---:|---:|
| Box-Muller current law (W0) | 2,296 | 10.33 | 8.65 |
| Inverse-CDF loader A02 | 2,140 | 9.63 | 8.06 |
| Best loader alone | 1,293 | 5.82 | 4.87 |
| Free loader alone (F05) | 1,211 | 5.45 | 4.56 |
| Box-Muller + free exponential (A13) | 1,219 | 5.48 | 4.59 |
| Box-Muller + unproved narrow words (A07) | 974 | 4.38 | 3.67 |
| **Best loader + free exponential** | **215.5** | **0.97** | 0.81 |
| Free loader + free exponential, 72-bit (N1 sheet) | 173 | 0.78 | 0.65 |
| All-free (W0) | 114 | 0.51 | 0.43 |

**Reading.**
- Neither the loader nor the exponential alone gets below M ≈ 4.4: each removes at most about 2× of the T
  count.
- Reaching M ≤ 1 needs **both** stages near-free together, about a 10× cut in T per iterate. In the N1 sheet,
  Box-Muller is 64% of compute Toffolis and the exponential 28%.
- None of these near-free designs exists. The free exponential (A13) and the free or best loader are W0
  idealizations.

## Rows, hashes, reproduction

Order of runs:
1. `p1_control_span.py`
2. `p2_window_constant.py`
3. `headline_m_probe.py` (reads the P2 output)
4. `p3_oracle_desk.py` (reads the headline output)

| File | sha256 |
|---|---|
| research/frontier_probe_20261021/p1_control_span.py | 4dc48fb5…9f53 |
| research/frontier_probe_20261021/p2_window_constant.py | 59a010a8…58f3 |
| research/frontier_probe_20261021/headline_m_probe.py | 5b49abb2…3bc6 |
| results/frontier_probe_20261021/p1/run001/p1_span.json | a704f9fe…6738 |
| research/frontier_probe_20261021/p3_oracle_desk.py | 6949299a…9c8e |
| results/frontier_probe_20261021/p2/run001/p2_window.json | bc322533…9372 |
| results/frontier_probe_20261021/headline/run001/headline_table.json | 9b53cbc5…47d4 |
| results/frontier_probe_20261021/p3/run001/p3_desk.json | ce5599e4…4e42 |

Each JSON also records the sha256 of its inputs.

**Not done.** Compute: no paid or cloud compute was used, no downloads beyond public arXiv pages, and no frozen
limitation scope was reopened. Review and the v3 draft:
- no independent review of the P2 derivation (recommended before any v3 edit; done in round 2);
- no edits to the v3 draft;
- nothing committed.

---

## Round 2 (continued autonomously, 21 Oct): reviews, parts 3-4, re-runs

Nothing in round 1 was overwritten. New outputs are `run002`, or new folders `coverage/`, `derived/` and
`review/`. `headline_m_probe.py` and `p3_oracle_desk.py` gained an argv run selector; with no argument they
reproduce `run001`.

### Independent R2 reviews

Two background agents reviewed the probe from the files alone.

**P2 review** (`results/frontier_probe_20261021/review/p2_review.jsonl`, 21 rows): **no critical or major
finding**.
- **Re-derivations.** Every inequality was re-derived:
  - Poisson validity and the half-weight rectangle DTFT;
  - A1 = 1.2376043;
  - the aliasing sum: the true value is ≤ 0.1487, against the 1/4 used;
  - |cot(ω/2) − 2/ω| ≤ (2/π²)|ω|, tight at π;
  - X, X_band and C_R;
  - the I_c and I_tot enclosures, against independent quadrature.
- **Monotonicity:** checked over 200 N in [800, 1e7].
- **Brute force:** exact λ0 at N from 800 to 300,007 showed no violation; the margin at large N is about 2.4e-5.
- **Minor findings and their fixes:**
  - **(i)** Decimal rounds to nearest, not outward. The effect is about 1e-45 against a margin of 3.9e-6. Noted;
    nothing changed.
  - **(ii)** 20 k cells have N < 800. Fixed with `coverage_check.py` (`coverage/run001`): all 20 are ε = 0.10,
    split e = ε and overhead-dominated, so none enters a reported minimum M.
  - **(iii)** The proof existed only in code. Fixed with [P2_DERIVATION.md](P2_DERIVATION.md).

**P1 review** (`review/p1_review.jsonl`, 6 rows):
- **Upheld (pass):**
  - the min-over-β span algorithm;
  - the witness paths, rebuilt in 60-digit arithmetic with every digit matching;
  - the U1 bound, whose exact supremum 1.59284 is below the reported 1.5933;
  - h(y_hi) = 15.623 by direct quadrature;
  - the 17.29 upper bound;
  - the jump argument for any finite set of controls continuous at the barrier.
- **Two major points:**
  - **(a)** Clipped/hybrid preintegration and preintegration over k > 1 directions were not covered.
  - **(b)** The desk D ratio of 3.61 overcounts. The first PCA loading is constant within a date, so the barrier
    roots are closed form.
- **Minor points:**
  - the 11.42 bound covers monotone directions only;
  - run001's "net upper bound" used max(linear, U1), which pairs a gain with the wrong baseline.

Both major points are evaluated in `p1b_hybrid.py` (below).

### P1 run002: the open routes evaluated

`research/frontier_probe_20261021/p1b_hybrid.py` writes `results/frontier_probe_20261021/p1/run002/p1b_hybrid.json`.

**Consistent pairing.** The span gain S/S′ applies to the no-U1 constant (M 414.4). The U1 gain √((S−m)/(S′−m))
applies to the U1 constant (M 232.0). The net factor is 232.0 / min(232.0/g_U1, 414.4/g_lin). On this basis
run001's routes net:
- closed-form controls ≤ 1.59;
- unclipped preintegration 1.70 at D = 1. Round 1's 2.49 was the loose max metric.

**Corrected D ratio** (mod, desk). The structure-aware count is 52 closed-form barrier roots, a 52-term strike
Newton and 106 CDFs, giving **1.30**. With a PCA-loader change (0 to +1.2, assm from the review) the range is
**1.30-2.50**. The round-1 value 3.61 is withdrawn.

**h distribution** (meas; 32,768 MC paths over y, B8x52):
- mean 3.285, against the price of 3.282;
- σ 1.148 (σ_preint 1.146 meas);
- maximum 7.30, q99.9 6.41.

The worst case over the box is still ≥ 15.6; that is the span a worst-case estimator must cover.

**Clipped/hybrid preintegration.** The oracle encodes min(h, τ) (span τ), and the tail E[(h−τ)⁺] is handled in
one of two ways:
- estimated classically, with its error share e_c set so that T_tail ≤ T_C/10, using
  T_tail/T_C = (σ_tail/σ_preint)²(e/e_c)² (assm, q+);
- absorbed in the spare bias reserve, 0.55ε − 0.000473 = 7.7e-5. This needs the MC tail mean (assm, not
  certified).

| τ | Tail handling | Tail mean (meas) | Gain linear / U1 | e_q / e | Net at D = 1 | Net at D = 1.30 |
|---:|---|---:|---:|---:|---:|---:|
| 4.83 | classical | 0.0383 | 8.04 / 4.86 | 0.539 | 2.62 | 2.01 |
| 5.33 | classical | 0.0111 | 7.29 / 4.21 | 0.773 | 3.26 | 2.50 |
| **5.83** | classical | 0.0023 | 6.66 / 3.77 | 0.906 | **3.42** | **2.62** |
| 6.33 | classical | 0.0003 | 6.14 / 3.44 | 0.968 | 3.33 | 2.56 |
| 7.08 | absorbed as bias | 8e-6 | 5.49 / 3.08 | 1.0 | 3.08 | 2.36 |

**Preintegration over k directions** (PCA 0..k−1). Each extra direction has no closed form and needs at least 2
quadrature nodes, so the D ratio is at least 1.30 × 2^(k−1). The witness lower bound on sup h_k, from 20-node
Gauss-Hermite at the run001 witness, is:

| k | sup h_k ≥ | Net at D = 1 | Net at the D floor |
|---:|---:|---:|---:|
| 1 | 15.62 | 1.70 | 1.30 |
| 2 | 13.92 | 1.83 | 0.70 |
| 3 | 13.25 | 1.89 | 0.36 |

Reaching 4 at the cost floor would need sup h_k ≤ 3.654 (k = 2) or ≤ 3.408 (k = 3). That is within 0.33 and 0.08
of the mean bound 3.327, against witnessed values of 13.9 and 13.3.

**Verdict.**
- Best net at D = 1, any evaluated route: **3.42**.
- Best at the structure-aware D ratio: **2.62**.
- Both are below the kill threshold of 4. **The F20/F04 close recommendation stands**, now with every route the
  review raised evaluated.

**Caveats.**
- The hybrid margin is modest: 3.42 against 4 at D = 1.
- It depends on an assumed classical tail-time model. That model is q+, because (h−τ)⁺ is less smooth than h.

The same hybrid on top of the P2 window estimator would give M ≈ 10.29 / 3.42 ≈ 3.0 at D = 1 (mod, derived).
That is still above 1 at the primary conventions.

### P2 run002: parts 3 and 4 explicit

`research/frontier_probe_20261021/p2b_parts34.py` writes `p2/run002/p2_window.json`.

- **Part 3:** a discrete random offset (K = 2^40) loses at most (2N+1)(1+4c)/(GK) < 1e-11, for every phase.
- **Part 4:** at most about 1.05e6 rotations synthesised to 2^-40 (Ross-Selinger, lit), plus angle rounding.
  At the largest N used (2.98e5) the failure probability rises by at most **1.9e-6**. A reserve of 4e-6 is
  asserted for every cell.
- **Re-certified:** **c(0.003) = 4.179** and **c(0.01) = 3.510**, for all N ≥ 800 (mod; parts 1-4 explicit;
  inherited U1/U2 and direction-select).
- **k at the binding cell: 8.762** (N = 100,924 calls) at δ = 0.003, and **7.359** at δ = 0.01.
- **Rotation T overhead:** about 3.4e7 per shot, against about 2.3e13 T in Grover iterates.

**Brute-force check at the binding N** (float, FFT autocorrelation, independent of the bound): 1 − λ0 =
2.97059e-3 ≤ 3e-3 at N = 100,924 and c = 4.179; 9.940e-3 ≤ 1e-2 at N = 84,767 and c = 3.510.

### M, round 2

`headline_m_probe.py run002` writes `headline/run002`; `derived_rows.py` writes `derived/run001`. Binding cell,
mod:

| Window certified (run002), credits | Failure | Direction-select | k | Primary | Symmetric (Stage C) | All-free | 1 lane vs 1 core |
|---|---|---|---:|---:|---:|---:|---:|
| U1 + U2 | 0.003 | yes | 8.762 | **10.29** | **0.279** | **0.511** | 1.005 |
| U1 + U2 | 0.01 | yes | 7.359 | 8.64 | 0.234 | 0.429 | 0.844 |
| U1 + U2 | 0.003 | no | 17.52 | 20.57 | 0.557 | 1.021 | 2.009 |
| U2 only (no orientation price) | 0.003 | yes | 15.65 | 18.37 | 0.498 | 0.912 | 1.795 |
| U1 only | 0.003 | yes | 11.46 | 13.45 | 0.364 | 0.668 | 1.313 |
| **none** (span 64, no mean bound) | 0.003 | yes | 25.80 | 30.29 | **0.821** | 1.504 | 2.958 |
| none | 0.003 | no | 51.60 | 60.57 | 1.642 | 3.007 | 5.917 |

Other results:
- **Ineligible binding cell** (B4x12 $0.001 binds): 14.10.
- **N1 floor alone:** 16.15.
- **Minimal departures for the window class: 1.** These are symmetric (0.279) and all-free (0.511).
- **Under the symmetric convention**, the certified window gets below 1 **with no conditional credit at all**,
  given direction-select: 0.82.

**P3, round 2** (`p3/run002`). The limit is D_eff ≤ 223.2 layers. Best loader + free exponential gives **0.965**,
the all-free floor 0.511, and either single cut ≥ 4.36.

### Round-2 hashes

| File | sha256 |
|---|---|
| research/frontier_probe_20261021/p2b_parts34.py | e9701d54…8245 |
| research/frontier_probe_20261021/p1b_hybrid.py | bcb0d176…799e |
| research/frontier_probe_20261021/coverage_check.py | f7badc7b…aa24 |
| research/frontier_probe_20261021/derived_rows.py | be9fc5c2…514d |
| research/frontier_probe_20261021/headline_m_probe.py (with run selector) | 04aa1e74…7653 |
| research/frontier_probe_20261021/p3_oracle_desk.py (with run selector) | 3b2da543…b928 |
| results/frontier_probe_20261021/p2/run002/p2_window.json | 0447dd06…1094 |
| results/frontier_probe_20261021/p1/run002/p1b_hybrid.json | 881a544b…6463 |
| results/frontier_probe_20261021/headline/run002/headline_table.json | a6d71cc3…c2a6 |
| results/frontier_probe_20261021/p3/run002/p3_desk.json | 1bbcf2f4…6958 |
| results/frontier_probe_20261021/derived/run001/derived.json | 63635c1d…e31c |
| results/frontier_probe_20261021/coverage/run001/coverage.json | 14cc556a…aa5c |
| results/frontier_probe_20261021/review/p1_review.jsonl | 75eb8ab2…1336 |
| results/frontier_probe_20261021/review/p2_review.jsonl | 889d802f…93b5 |

The P1 reviewer rewrote two of its own rows in place before finishing. That file is review output, not a
receipt.
