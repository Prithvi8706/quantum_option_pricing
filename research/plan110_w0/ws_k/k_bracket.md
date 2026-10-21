# WS-k: k bracket for the fixed task (plan110 W0, R0 screen)

11 October 2026. Items: E01, C11 (bracket), E25, E08, E03 with U1/U2, E04, E20 (lanes).

- **Numbers:** `results/plan110_w0/ws_k/k_bracket.json` (sha256 `4780a16c…f2ed`).
- **Script:** `research/plan110_w0/ws_k/k_bracket.py` (sha256 `0b1ccc9d…ad36`). It ran under `.context/frontier_t0_env` 3.12.4 `-I -S -B`, stdlib only, in about 40 s.
- **Rows:** `results/plan110_w0/ws_k/rows.jsonl`.
- **Input SHA256s:** in `meta.inputs_sha256`.

Nothing in this work ran a controller, launcher or verifier, and nothing was written outside `ws_k/`.

**Convention.** `k = controlled-Grover calls / (sigma_q / e)`.
- sigma_q is **measured**: B4x12 5.66357, B8x52 5.18340, from `sigma_dev.json`.
- e = 0.45 eps is the primary value; e = eps is a sensitivity column.
- 99% per price. The estimator gets failure 0.003 (E07 allocation); 0.01 is the favourable sensitivity.

Labels: **M** measured, **Mod** modelled (exact arithmetic or numerics), **A** assumed, **L** literature. Directions: q+ quantum-favourable, q- adverse, 0 neutral.

## 0. Headline

| Quantity | B4x12 | B8x52 | Label / direction |
|---|---|---|---|
| k_eff today (E07, span 64, dyadic M, 15 medians), e = 0.45 eps, at $0.10 / 0.03 / 0.01 / 0.001 | 976.2 / 585.8 / **781.1** / 624.9 | 1066.7 / 640.0 / **853.4** / 682.7 | Mod (exact), 0 |
| same at e = eps | 542.1 / 650.8 / 867.8 / 694.3 | 592.4 / 711.1 / 948.2 / 758.6 | Mod, q+ sensitivity |
| **k_lo, explicit constants, worst-case 99%**: canonical + medians, span 38.82 (211,53), mean bound price + L1, non-dyadic M | 186.6-187.1 (every eps) | 197.6-198.2 | Mod; mean bound **A** (uncertified), wrapper is a design; q+ |
| k_lo, explicit, no mean certificate (span 38.82, non-dyadic M) | 323 | 353 | Mod; q+ |
| k_lo, explicit, dyadic M only (best certified-conditional) | 195-312 | 213-341 | Mod |
| IQAE / modified-IQAE theorems (explicit) | 2,997-5,267 | 3,275-5,755 | L formulas, q- vs canonical |
| **Window (DPSS/Kaiser) single chain, 99.7%**: span 64 no mean / span 38.82 + price+L1 | 23.6 / 8.3 | 25.7 / 8.7 | Mod numerics, **no explicit constant in any primary source** |
| **k_lat at W = 1e7** (lanes = 18 for B4, 2 for B8), E07 schedule, e = 0.45 eps | 39-65 | 341-569 | Mod, q+ |
| k_lat at W, with best dyadic E03 credit | 13-21 | 114-182 | Mod; mean **A** |
| Access-model lower bound (rigorous counting), Q-access, support class | 1.70 | 1.85 | Mod (analytic proof), q+ |
| Same, A-access and mean-bounded class (weakest) | 0.077 | 0.079 | Mod, q+ |

**Early-stop signal (fires for total k).** No method with explicit constants gets total k below about 187 (B4) or 198 (B8), even with every conditional credit. Without the uncertified mean bound the floor is about 323/353; at today's certified schedule it is 586-1,067.

**k_lat is different, and it is the primary convention (W0 card).**
- **B4x12 is below 100.** Its 18 lanes fit in W = 1e7, so all 15 median shots run at once. k_lat is 39-65 today and 13-21 with E03 credits.
- **B8x52 is not below 100.** Only 2 lanes fit, so it stays at 114-569, unless its per-lane width falls to at most 666,666 logical qubits (6.7x below the current 4,460,479).
- **Window methods.** The only route below about 30 in total k is one-chain window amplitude estimation (k ≈ 8-26). It has **no explicit finite worst-case constant in the literature**.

## 1. k_eff today (exact)

The schedule rule is a copy of the E07 code: Machin π enclosure; the least power of two M with 64(π/M + π²/M²) ≤ e; 15 medians from the exact binomial tail at 0.003. **The saved ε = $0.01 schedule is reproduced exactly: M = 65,536 and 983,025 calls in both cases.** The task formula, with the 2^-39 readout added, picks the same M in all 16 cells.

| case | eps | e | M | calls | k_eff | k per chain (M−1)e/σ |
|---|---|---|---|---|---|---|
| B4x12 | 0.10 | 0.045 | 8192 | 122,865 | 976.2 | 65.1 |
| B4x12 | 0.03 | 0.0135 | 16384 | 245,745 | 585.8 | 39.1 |
| B4x12 | 0.01 | 0.0045 | 65536 | 983,025 | 781.1 | 52.1 |
| B4x12 | 0.001 | 0.00045 | 524288 | 7,864,305 | 624.9 | 41.7 |
| B8x52 | 0.10 | 0.045 | 8192 | 122,865 | 1066.7 | 71.1 |
| B8x52 | 0.03 | 0.0135 | 16384 | 245,745 | 640.0 | 42.7 |
| B8x52 | 0.01 | 0.0045 | 65536 | 983,025 | 853.4 | 56.9 |
| B8x52 | 0.001 | 0.00045 | 524288 | 7,864,305 | 682.7 | 45.5 |

Exact rationals (calls·e/σ, with the measured float σ converted exactly) are in `part1_k_eff_today[*].k_eff.exact`. The e = eps rows are in the JSON. At $0.10, e = eps cuts M by 4x but k by only 1.8x, because σ/e also changes. The whole spread of k_eff (586-1,067) comes from the dyadic M step.

## 2. Access-model lower bound (E01)

**Rigorous counting bound (derived here; the analytic proof is in the script docstring).**
- After N uses of controlled Q / Q⁻¹, the final state is Σ_{j=−N..N} e^{2ijθ}|v_j⟩. This is the degree argument of Mande & de Wolf, Claim 5.3 (arXiv:2305.04908v3, Quantum 10, 2140 (2026), p.13). The state therefore lies in a fixed (2N+1)-dimensional subspace.
- Take K two-point payoff laws on [0, S] whose means are more than 2e apart. If each must be estimated to within e with probability at least 1−δ, then (1−δ)K ≤ 2N+1.
- With raw A/A⁻¹ access, at two queries per Q, the bound halves.
- At δ = 0.01 and e = 0.45 eps, the bound gives:

| class | B4x12 k_LB (Q-access / A-access) | B8x52 |
|---|---|---|
| all payoffs on [0, 38.818] (E03 support) | 1.70 / 0.85 | 1.85 / 0.93 |
| payoffs with mean ≤ price + L1 (**A**) | 0.156 / 0.078 | 0.159 / 0.079 |

The bound is the same at every eps, because K is proportional to 1/e. Its minimum over all cells, conventions and access models is **0.074**. That is above the E01 threshold k* ≈ 0.06, so E01's access-model sentence can cite an explicit-constant bound.

**Literature (L).**

| Source | What it gives | Constant |
|---|---|---|
| Mande & de Wolf, Thm 1.3, with the constant read from the proof of Claim 5.2 | A δ_phase-precise phase estimate with failure ε needs t ≥ ln(1/(2ε))/(48 δ_phase) uses of U or U⁻¹. The order Ω((1/δ)log(1/ε)) is tight | 1/48, weak |
| Nayak & Wu (STOC'99), as cited in Mande & de Wolf p.4 and Rall & Fuller p.3 | Ω(1/ε) for counting at constant success | not explicit |
| Kothari & O'Donnell, arXiv:2208.07544 | O(σ/ε) runs, optimal in n, for variance-normalised mean estimation | no explicit constant |

**Modelled reference (Mod).**
- The DPSS window is the exact optimum for single-register phase estimation under a uniform phase prior (Patel et al. §IV C). It needs c = N·Δφ ≈ 4.17 at δ = 0.003 and 3.50 at δ = 0.01.
- In k units this is about 8-26 (section 3). It is not a proven bound for amplitude estimation, because the amplitude-estimation phase lives on a half circle and its prior is not uniform.
- **Gap.** Rigorous lower bound (0.07-1.85) vs window value (8-26) vs explicit-constant achievability (≥ 187). Lower bounds cannot make "unreachable" wording safe. That fits the user's chosen achievability wording.

## 3. k_lo achievability by method (C11, E25, E08, F4)

| Method | Constant status | k_total, e = 0.45 eps (B4 / B8, $0.01) |
|---|---|---|
| Canonical BHMT Thm 12 + 15 medians (E07) | **explicit, certified** | 781 / 853 |
| BHMT k-parameter vs repetitions (E08) | explicit. k_B = 1 with 15 reps is optimal at 0.003; at 0.01, 11 reps (1.36x) | — |
| Canonical, span 38.82 + price+L1 mean + non-dyadic M | explicit formula. Conditional on a U1 mean certificate, the U2 (211,53) wrapper and a non-power-of-two QFT | **186.6 / 197.7** |
| IQAE, Grinko et al. Thm 1: 50/ε·ln((2/α)log₂(π/4ε)) | explicit (L). Reproduces 6,471,874. Worst case over a | 5,142 / 5,619 (span 64); 3,101 / 3,388 (span 38.82) |
| Modified IQAE, Fukuzawa et al. Lemma 3.7 | explicit (L). Reproduces 6,491,064 | 5,157 / 5,635 |
| Nakaji FAE (arXiv:2003.02417, Thm 1): 4.1e3/ε·ln(4log₂(2π/3ε)/δ), error on the amplitude a | explicit, but about 2 orders above canonical | not tabulated (q-) |
| MLAE (Suzuki et al.) | **no explicit constant**: asymptotic Fisher interval only | — |
| ChebAE / QSP-AE (Rall & Fuller, Quantum 7, 937 (2023)) | **no explicit constant**: empirical ≈ 4.66/ε at 95% | — |
| Kaiser-window AE (Berry et al., arXiv:2209.13581, Lemma 4 and App. D) | **no explicit constant**. Leading order is (1/2ε)ln(1/δ), with an unstated O(ε⁻¹ ln ln) term. The paper's own approximation (D13)/(D15) gives c = 5.06 (δ = 0.003) | modelled 23.6 / 25.7 (span 64); 8.3 / 8.7 (span 38.82 + mean) |
| DPSS tapered QPE (Patel et al., arXiv:2403.18927, Thm 2) | explicit but **average-case only**: K ≥ 175(log(10/δ)+1)² | about 8.5e5 (q-); Thm 3 is asymptotic only |
| Window numerics, this script (DPSS optimum ≈ Kaiser with α ≈ 1.23) | c = 4.168 (δ = 0.003) and 3.502 (δ = 0.01) at N = 400, converging. Uses symmetric W/W⁻¹ control, as in Berry et al. Continuous (zero-padded) readout makes success independent of the phase | equal to the Kaiser row above (Mod) |

**Reading (F4).**
- The window route is worth about **22.6x** over canonical with medians at equal span, mean and non-dyadic M: 15·2π/4.17.
  - About 2x of this is the symmetric W/W⁻¹ control. Canonical could take that factor as well, but no theorem covers it.
  - The rest (about 11x) is replacing the medians and the 8/π² shot.
- It is the only route to total k ≈ 8-26.
- No primary source gives a finite worst-case constant for it. The constant is plausibly certifiable by an exact computation of the window's concentration (an R1 task, with its rigour left open). E08's kill should be narrowed to "median allocation only", as F4 proposed.

## 4. Joint estimator credit (E03/U2 × mean × dyadic, screened with E04)

The formula is applied exactly: e(m, M) = 2π√(m(S−m))/M + Sπ²/M² + 2^-39 ≤ e, with π_hi. Credit is measured against span 64, worst case, dyadic M. The spans are 64, 128/3 (3,47) and 8192/211 (211,53); 2^-39 is a placeholder readout for the new spans. The mean m is the uncertified orientation price plus 0.045202052 (**A**; for B8 the #43 L1 is borrowed from B4). The full 3 spans × 3 means × 2 M rules × 2 splits grid is in `part4_joint_credit`.

| cell (e = 0.45 eps) | support-tight only | + price+L1 mean (dyadic) | + non-dyadic M | best k (dyadic / non-dyadic) |
|---|---|---|---|---|
| B4 $0.10 | 2 | **4** | 5.22 | 244 / 187 |
| B4 $0.03 | 1 | 2 | 3.14 | 293 / 187 |
| B4 $0.01 | 2 | **4** | 4.19 | 195 / 187 |
| B4 $0.001 | 1 | 2 | 3.35 | 312 / 187 |
| B8 $0.10 | 2 | **4** | 5.38 | 267 / 198 |
| B8 $0.03 | 1 | 2 | 3.24 | 320 / 198 |
| B8 $0.01 | 2 | **4** | 4.32 | 213 / 198 |
| B8 $0.001 | 1 | 2 | 3.46 | 341 / 198 |

**Self-checks (asserts passed).**
- The table reproduces every entry of the CRITIQUE F3 table: 2/4/5.2, 4/4/5.4, 2/4/4.3, 2/2/3.5 and 2/2/3.4.
- It reproduces the U2 §4 halving pattern: (3,47) halves at 1/10 and 1/100 only.
- **Correction to the U2 §4 sentence ("neither is reachable").** It is wrong. With (3,47), quartering is reached at B4 $0.10, B8 $0.10 and B8 $0.01, under the orientation price plus L1. B4 $0.01 reaches x4 only with (211,53).
- With (211,53), the barrier-free bound of about 6 USD (**A**) gives x4 at $0.10 and x2 elsewhere, both at e = 0.45 eps. At e = eps it gives x2 at most.

**E04, screened jointly.**
- The best toy controller cost is 280,800 at a = 1/8 (mean $8) and 525,056 at a = 1/4. Those numbers are **M** but come from toy laws only.
- A p-aware canonical at the same mean costs 491,505 / 983,025 with dyadic M and 443,370 / 580,470 with non-dyadic M.
- So E04's own residual over (E03 + non-dyadic) is **1.58x / 1.11x**. Its 1.75x against 983,025 is mostly E03's p-awareness.
- Rule: multiply the E03 credit by at most the non-dyadic residual (≤ 1.6x, uncertified, no delivery guarantee), never by 1.75x. The general IQAE theorems are 6.6x *worse* than canonical.

## 5. Lanes (E20; primary parallelism convention)

The lane width is the source's logical qubit count from the STATUS header (**A**: the QPE register and selector are ignored): B4 550,141 and B8 4,460,479. The 15 median shots run as independent lanes. k_lat = ceil(15/L)·(M−1)·e/σ, at e = 0.45 eps.

| W | B4 lanes | B4 k_lat (E07 / best dyadic E03) | B8 lanes | B8 k_lat (E07 / best E03) |
|---|---|---|---|---|
| 1e6 | 1 | 586-976 / 195-312 (= 1-lane values) | **0 (does not fit)** | — |
| **1e7** | **18** | **39.1-65.1 / 13.0-20.8** | **2** | **341-569 / 114-182** |
| 1e8 | 181 | 39.1-65.1 / 13.0-20.8 | 22 | 42.7-71.1 / 14.2-22.8 |

**Hypothetical floor widths at W = 1e7.**
- At width/4: B4 gets 72 lanes and the same k_lat. B8 gets 8 lanes, 2 rounds, k_lat 85-142 (E07) or 28-46 (E03).
- Full median parallelism needs lane width ≤ 666,666. B4 meets that today; B8 needs a 6.7x width cut.

**Supply at 100 ns** (Mod). B4: 15 lanes × 9.37e9 = 1.41e11 T/s. B8: 2 × 6.43e10 = 1.29e11 T/s. Both are below 1e12.

**Methods that lanes do not shorten.**
- Window methods are one coherent chain, so k_lat = k_total ≈ 8-26.
- Averaging independent sub-estimates cuts latency by at most √P, at √P more calls, and has no explicit 99% constant. It is not tabulated.

## 6. Caveats

- The window numerics use floats and a continuous-outcome readout. A finite readout grid adds an O(1/grid) error. c still increases slowly with N (4.152 at N = 100, 4.168 at N = 400); the large-N limit is estimated at about 4.17-4.2.
- The counting lower bound is for black-box (A or Q) access. The fixed task has known source code, so structural escapes (F04/F05/F20) are outside it.
- Every credit beyond the saved E07 schedule is conditional on one or more of: U1 (mean certificate, open), the U2 wrapper (not emitted), a non-power-of-two QFT, and the B8 L1 bridge (not established).
- IBM cloud hardware was not used (W0 card).
