# N1 estimator card (plan110 branch N, rigour R1)

12 October 2026. Items: E01, C11 (bracket), E03, E04, E08, E25, E20. This card checks WS-k (`research/plan110_w0/ws_k/`) along a different path and verifies its literature against the primary sources. The conventions are those of `research/plan110_w0/W0_CARD.md`.

- **Units.** k = controlled-Grover calls ÷ (σ_q/e).
  - σ_q is **measured**: B4x12 5.66357, B8x52 5.18340.
  - The primary split is e = 0.45 ε.
  - Each price is held to 99%; the estimator's share of the failure budget is δ = 0.003 (the E07 allocation).
- **Labels.** Every number is labelled measured, modelled, assumed or literature, and carries a direction: q+ (quantum-favourable), q− (adverse) or 0 (neutral).

**Receipt (R1).**
- Script: `research/plan110_n1/estimator/recompute_estimator.py` (sha256 `1633e8a6…cbcfde`). It is stdlib only and ran under `.context/frontier_t0_env` 3.12.4 `-I -S -B` in about 6 s.
- Output: `results/plan110_n1/estimator/estimator_recompute.json` (sha256 `2020d1d0…afe3`). Its `meta.inputs_sha256` holds the SHA256 of each of the 5 inputs.
- Rows: `results/plan110_n1/estimator/rows.jsonl` holds 26 rows. The first 9 are the literature checks from the run cut off by the logout.

**How the recompute differs from WS-k.**

| Quantity | WS-k method | N1 method |
|---|---|---|
| π enclosure | Machin series | Euler series, arctan(1/2) + arctan(1/3) |
| Median repetitions | Closed binomial tail on a value rounded to 2^-40 | Exact DP convolution on 1 − 8/π_hi² |
| Least M | Doubling, then bisection | Closed-form root of the error quadratic, checked exactly at M and M−1 |
| Window constant c | Tridiagonal DPSS eigenvector | Power iteration on the even-reduced prolate (sinc) matrix |
| Lanes | Source widths | WS-floor design table, with T supply shared across lanes |

Every WS-k number the decision table uses was reproduced, as the asserts in the script check:
- 983,025 calls;
- 15 and 11 medians;
- k 586-1,067 and 186.6-198.2;
- the window c to 1e-12 at N = 100 and 200;
- primary M of 801, 232 and 8.62.

---

## 1. Access model (E01)

**What the quantum estimator is assumed to have.**
- **Black-box access only.** The estimator touches the payoff through a state-preparation unitary A, with A|0⟩ = √(1−a)|ψ₀⟩|0⟩ + √a|ψ₁⟩|1⟩ and mean payoff μ = S·a, where S is the wrapper span.
- **Allowed operations:**
  - preparing A|0⟩;
  - controlled applications of the Grover iterate Q = −A S₀ A† S_χ and of Q⁻¹ (or a direction-select between them);
  - any query-free unitaries and measurements.
- **Guarantee.** The output μ̂ satisfies |μ̂ − μ| ≤ e with probability ≥ 1 − δ for **every** A in the class, which is every payoff law on [0, S]. This is the worst-case 99% guarantee the certified schedule provides.
- **Cost unit.** One cost unit is one controlled Grover iterate, which is the per-call depth of WS-small and WS-floor.

**The counting lower bound and why it applies.** The bound is a rigorous analytic result derived in WS-k and re-derived here; it is labelled modelled and is a floor (q+).

1. **The hard family.** Take A_θ = R_y(2θ) acting on one payoff qubit, with the other registers left idle. Then a = sin²θ and the payoff law is S·Bernoulli(a). An estimator correct on the whole class must be correct on this family.
2. **The degree argument.**
   - Q_θ, Q_θ⁻¹, the direction-select operation and their controlled versions all have eigenvectors that do not depend on θ. Their eigenvalues lie in {1, e^{±2iθ}}.
   - This is exactly the premise of the degree argument in Mande & de Wolf, Claim 5.3, which is verified below.
   - So after N calls the state lies in span{e^{2ijθ}|v_j⟩ : |j| ≤ N}, a space of dimension ≤ 2N+1.
   - One copy of A|0⟩ multiplies by e^{±iθ}. Only odd exponents then appear, so the dimension is ≤ 2N+2.
   - Intermediate measurements are deferred without changing the call count.
3. **The counting step.**
   - Take K laws whose means are spaced more than 2e apart in [0, S]; K = ⌈S/2e⌉.
   - The sets of correct outputs are disjoint.
   - For final states in a space V, Σ_i ⟨ψ_i|E_i|ψ_i⟩ ≤ tr(P_V).
   - Therefore (1 − δ)K ≤ 2N + 2.
4. **In k units.** N ≥ ((1−δ)K − 2)/2, so k_LB ≈ (1−δ)·S/(4σ).

| Class and access model (δ = 0.01, e = 0.45 ε) | B4x12 | B8x52 |
|---|---|---|
| Support [0, 38.818], Q-access (WS-k) | 1.695-1.696 | 1.852-1.854 |
| Same, plus one free copy of A\|0⟩ (N1 correction) | 1.691-1.696 | 1.848-1.853 |
| Same, A/A† access at half a Q each | 0.85 | 0.93 |
| Mean-bounded [0, price+L1] (mean bound **assumed**) | 0.15-0.16 | 0.15-0.16 |

- **The constant does not depend on ε,** because K is proportional to 1/e. The lowest value in any cell or access model is 0.074.
- **WS-k's 1.70 / 1.85 is verified.** The "+one copy of A" correction changes only the fourth digit, and only at ε = 0.10.
- **What the bound does not cover:**
  - white-box estimators that use the known source code (the structural escapes F04, F05 and F20);
  - estimators promised a narrower class of laws.
- **Why it is quoted in units of σ_task.** The hard laws have σ up to S/2 ≈ 19.4. Quoting the bound in units of the task's σ is a convention; it does not give the bound for a σ-aware estimator.

**Use in the manuscript.** The bound is a floor at about 1.7-1.85. The achievable values sit above it: 187-198 with explicit constants, or about 8-26 for the window methods. The bound cannot make "unreachable" wording safe. The claim stays an achievability claim, as the N1 card requires.

---

## 2. Achievability bracket (C11, E03, E04, E08, E25)

### 2a. Certified today: k = 586-1,067 (modelled, exact; 0)

The schedule is the E07 schedule: canonical BHMT Thm 12 with k_B = 1, 15 medians at δ = 0.003, span 64, dyadic M and M−1 calls per shot.

| ε | 0.10 | 0.03 | 0.01 | 0.001 |
|---|---|---|---|---|
| M | 8,192 | 16,384 | 65,536 | 524,288 |
| B4x12 k | 976.2 | 585.8 | 781.1 | 624.9 |
| B8x52 k | 1,066.7 | 640.0 | 853.4 | 682.7 |

- **E08.** k_B = 1 with 15 repetitions is the cheapest choice; k_B ∈ {3, 4, 5, 6, 8} all cost more. At δ = 0.01 the count drops to 11 repetitions, a ×1.36 gain.

### 2b. Best explicit worst-case 99% constant: k = 187-198, with every conditional credit applied (modelled; q+)

Per cell: B4x12 is 187.1 / 186.7 / 186.6 / 186.6 and B8x52 is 198.2 / 197.8 / 197.7 / 197.6, at ε = 0.10 / 0.03 / 0.01 / 0.001. The credits, one at a time:

| # | Credit | Effect | Certificate it needs | Status |
|---|---|---|---|---|
| 1 | **U2 support-tight wrapper** (211,53): span 8192/211 = 38.82 in place of 64 | Alone ×1-2 (×2 only at ε = 0.10 and 0.01, through the (3,47) wrapper) | E03 audited support, sup g ≤ 38.818 (exists). Also the wrapper circuit emitted and verified, and a readout bound for the new span (2^-39 is a placeholder) | Design only |
| 2 | **U1 mean certificate**: m ≤ price + L1 | Replaces √(a(1−a)) ≤ ½ with the mean-aware value. With #1 and dyadic M, k = 195-341 | A certified upper bound on E[payoff]. The price used is an uncertified RQMC orientation value (**assumed**). For B8x52 the #43 L1 = 0.045202052 is borrowed from B4x12, because the B8 L1 bridge does not exist | Open |
| 3 | **Non-dyadic M** | With #1 and #2: 187-198. With #1 only: 323-353 | A QFT over Z_M that is exact or carries an error budget, with its rotations certified. BHMT Thm 12 holds for any integer M (verified) | Not built |
| (fixed) | 15 medians at δ = 0.003, e = 0.45 ε | none | The E07 allocation, already certified | Done |

- **E04** (adaptive controllers, IQAE family). Its explicit theorems are q− against canonical:
  - Grinko Thm 1 gives k = 2,997-5,755;
  - Fukuzawa Lemma 3.7 gives about the same.
  - E04's measured toy residual over a p-aware non-dyadic canonical is ≤ 1.6×. That is measured on toy laws only, with no worst-case guarantee, so it is not credited.
- **E25** (Bayesian or likelihood designs, i.e. MLAE and ChebAE). No worst-case coverage theorem with an explicit constant exists in the sources checked, so E25 adds nothing to the explicit class.

**N1 finding: an extra conditional credit, direction-select control, ×~2.** It is labelled modelled and is q+.

- **The argument.** Replace Q^j by Q^(j−c) in BHMT's Λ_M(Q).
  - Each Q eigen-branch picks up only a global phase, and the two branches are orthogonal.
  - So the register's outcome distribution, and with it every guarantee in BHMT Thm 12, is unchanged.
  - The construction: plain control on bit 0, plus direction-select Q^(±2^(b−1)) on bits b ≥ 1. This realises j − c with 2^(n−1) = M/2 calls per shot, against M − 1.
- **This corrects WS-k.** WS-k said that "no theorem covers" giving canonical the symmetric-control factor. In fact BHMT Thm 12 covers it unchanged.
- **The one missing certificate is a call-cost certificate.** A direction-select iterate is [S_χ controlled on 0]·A S₀ A†·[S_χ controlled on 1]. It needs to cost no more than one controlled Grover iterate in the program cost model, which holds when only the reflections are controlled. This cost is **assumed** here.
- **Effect (conditional):**

| Quantity | Before | With direction-select |
|---|---|---|
| Certified-schedule k | 586-1,067 | 293-533 (491,520 calls at ε = 0.01) |
| Best k with every credit | 187-198 | 98-171 (dyadic; non-dyadic M gains nothing once direction-select is used) |
| Primary M, certified | 801 | 401 |
| Primary M, explicit best | 232 | 200 |

The verdict does not change.

### 2c. Window / QSP amplitude estimation: k ≈ 7-26, with no explicit worst-case constant (modelled; q+)

| Convention (direction-select; N calls cover exponents −N..N) | B4x12 | B8x52 |
|---|---|---|
| δ = 0.003, span 64, no mean bound (no conditional credits) | 23.5 | 25.7 |
| δ = 0.003, span 38.82 + price+L1 (credits #1 and #2) | 8.25 | 8.74 |
| δ = 0.01, span 38.82 + price+L1 (**the DP1 row**) | 6.93 | 7.34 |

**How the constant was obtained.**
- c = N·Δ is the DPSS optimum.
  - At δ = 0.003 it is 4.131, 4.152 and 4.163 at N = 50, 100 and 200.
  - At δ = 0.01 it is 3.471, 3.489 and 3.498.
  - These match WS-k to 1e-12. WS-k's N = 400 values, 4.168 and 3.502, are used.
- The task needs N ≈ 8.5e2-3e5, so c is extrapolated a little upward, to about 4.17-4.2. The effect is under 1%.
- Kaiser with α ≈ 1.23 matches DPSS. The approximate formula of Berry et al., (D13)/(D15), gives c = 5.06.

**The window route against canonical.** With the same credits, the window route is about 11-13× below canonical once canonical also takes direction-select: 341 against 25.7, or 171 against 8.7. Against canonical without direction-select it is about 22×.

**Patel et al. Thm 2 can be made worst-case** (argument here, not stated in the source). Apply a uniformly random, known phase offset to the register; this needs no oracle calls. The success probability at every phase then equals the phase average, so the explicit average-case Thm 2 becomes an explicit worst-case bound. It is useless in practice: 15 extra ancillas, and k = 6.8e5-9.3e5. So the precise statement is that **no primary source gives a usable explicit worst-case constant**. WS-k's "explicit but average-case only" was correct as written.

---

## 3. Lanes at W = 1e7 (E20)

Here the 15 median shots run as parallel lanes. The lanes share the 1e12 T/s supply, and the call designs come from the WS-floor table (Box-Muller current law, base). All values are modelled and q+.

| | B4x12 | B8x52 |
|---|---|---|
| Width of the primary floor design at W = 1e7 | 5,279,689 (1 lane) | 10,000,000 (1 lane) |
| Single-lane effective call depth at 1e12 T/s, 100 ns | 364 (supply-aware design, 2.43M wide) | 2,296 (supply-bound) |
| Best lane credit at 1e12 T/s | **1.29×** (3 lanes of the W = 1e6 design) | **1.00×** |
| Cap on that credit set by the T supply (total T ÷ supply) | 1.29× | 1.00× |
| Best lane credit with unlimited supply (sensitivity) | 3.36× (4 lanes, 2.43M wide) | 1.00× |

- **The supply argument.** Latency is at least (total T count)/(supply), whatever the lane count. That holds for independent median lanes and for entangled-parallel AE alike, so E20 gives nothing beyond this cap.
- **The decision-critical cell, B8x52 at $0.001, gets no lane credit under any modelled supply.**
- **B4x12 at $0.001.** A 1.29× credit would move M from 318 to 247 (W0 explicit best), or from 266 to 207 (with direction-select). Neither changes the minimum M, which is set by B8x52.
- **Window and QSP chains are one coherent chain:** k_lat = k_total.
- **WS-k's k_lat figures** (18 and 2 lanes; 39-65 and 341-569) assume source-width oracles at source depth: 555,774 and 663,704. They must not be combined with the floor's k_10x. The decision table did not combine them; it used k_total.

---

## 4. Literature verified against primary sources

The earlier run fetched 8 sources; this run fetched none, for 8 fetches in total against a cap of 15.

| Source | Claim as WS-k used it | What the source says | Verdict |
|---|---|---|---|
| Mande & de Wolf, arXiv:2305.04908v3 (Quantum 10, 2140 (2026)), Sec. 5 | t ≥ ln(1/(2ε))/(48 δ) uses of controlled U/U⁻¹; Claim 5.3 degree argument | Claim 5.3: with t controlled-U_θ^{±1} applications and no intermediate measurement, amplitudes are degree-t trig polynomials in θ. In the proof of Claim 5.2, Thm 2.7 with s = 6δ and n = 2t gives 1/(2ε) ≤ exp(48tδ). Thm 1.3 states only Ω | **Verified.** 1/48 is read from the proof. Claim 5.3 applies to the hard family because its eigenvectors do not depend on θ (§1) |
| Grinko et al., arXiv:1912.05559v3, Thm 1, eq. (9) | N < (50/ε) ln((2/α) log₂(π/(4ε))), ε on the amplitude a | As used; natural log; worst case over a; the source calls the bound loose | **Verified** (q− against canonical) |
| Fukuzawa et al., arXiv:2208.14612v4, Lemma 3.7 | N = (3πC/(8ε)) ln(√27/α), C = 1/(sin²(π/21) sin²(8π/21)) | Eq. (3.31) as used. The lemma rounds it to (62/ε) ln(6/α) and counts Q applications | **Verified** |
| Berry et al., arXiv:2209.13581v3, Lemma 4 and App. D | N = (π/ε)√(1+α²) ≈ (1/(2ε)) ln(1/δ) + O(ε⁻¹ lnln); no certified constant | App. D is approximate throughout: Gaussian normalisation, Bessel asymptotics, a tail bound with sin set to 1, arcsinh ≈ ln(2α). (D13) uses ≈ and (D14)/(D15) carry O(lnln). N calls cover m = −N..N | **Verified.** No finite worst-case constant. Lemma 4 is stated for an amplitude; WS-k uses the phase-error reading that App. D derives |
| Patel et al., arXiv:2403.18927v3, Remark 1, Thms 1-3 | DPSS optimal on average; Thm 2 explicit, average-case; Thm 3 asymptotic | As used. Thm 2: m = ⌈log₂(⌈175(log(10/ε̄)+1)²⌉+1)⌉+1 extra ancillas, for average success. Thm 3 holds for N ≥ N₀ with N₀ unspecified | **Verified.** A random offset makes Thm 2 worst-case, but useless (§2c) |
| BHMT, quant-ph/0005055, Thm 12 | \|ã−a\| ≤ 2πk√(a(1−a))/M + k²π²/M², with probability ≥ 8/π² (k = 1) or > 1 − 1/(2(k−1)) (k ≥ 2); any integer M | As used; exactly M evaluations of f; F_M for general M | **Verified.** It also covers the direction-select shift (§2b) |
| Rall & Fuller, arXiv:2207.08628v3, Empirical Claims 18 and 20 | ChebAE ≈ 4.66/ε, IQAE ≈ 9.93/ε at 95% | Fits at a = 0.5, δ = 0.05, average query count | **Verified.** Not a worst-case 99% constant |
| Nakaji, arXiv:2003.02417v3, Thm 1 | N < (4.1e3/ε) ln(4 log₂(2π/(3ε))/δ) | As used | **Verified** (constant and form) |
| Kothari & O'Donnell; Nayak & Wu; Suzuki et al. (MLAE) | No explicit constants | Not re-fetched; no number depends on them | Not verified (not needed) |

No source contradicts a claim WS-k used.

---

## 5. The open problem the frontier section should name

**An explicit, non-asymptotic, worst-case 99% constant for window/QSP amplitude estimation.** Stated precisely, it needs all of the following:

1. **A guarantee for every amplitude.** For every a ∈ [0, 1], an algorithm making at most N ≤ c(δ)/Δ + c₀ calls returns φ̂ with |φ̂ − 2θ| ≤ Δ (mod 2π, up to sign) with probability ≥ 1 − δ.
   - A call is one controlled Q, Q⁻¹ or direction-select iterate, which costs one controlled Grover iterate.
   - δ = 0.003 (or 0.01), and c(δ) and c₀ are explicit numbers.
   - It must hold either for all N, or for an explicit N ≥ N₀ with N₀ below about 8e2, the smallest N the task uses (at ε = 0.10).
   - The BHMT inequality then turns Δ into the dollar error.
2. **A certified concentration bound.** The window (DPSS, Kaiser or another) needs a rigorous lower bound on its concentration λ₀(N, Δ) ≥ 1 − δ.
   - That can be closed-form and uniform in N, or an interval-arithmetic computation at the N actually used, which is about 8.5e2-3e5.
   - The Slepian asymptotics (Patel Thm 3) and Berry's App. D are not certified.
   - The non-asymptotic Patel Thm 2 route through [KRD21] loses a factor of about 1e5.
3. **Worst case over phase, finite readout included.**
   - The continuous-readout success is independent of the phase. A finite QFT grid adds an offset-dependent leakage term that must be bounded explicitly.
   - Alternatively, a random known register offset can be used (§2c), but the window's bound must then be the average over grid offsets, not an asymptotic one.
4. **Every finite-size error inside δ.** This covers the window-state preparation, the precision of the QFT and phase rotations, and the handling of both eigen-branches near a ∈ {0, 1}.
5. **The QSP/ChebAE alternative.** A proven worst-case coverage statement with explicit constants for the adaptive schedule. Rall & Fuller give only fits at a = 0.5 and 95%.

**Target.** c(0.003) ≈ 4.2, which means k ≈ 8.7 with the U1/U2 credits and ≈ 26 without them.
- The DP1 memo says this lever alone moves M from 232 to about 9-10: 10.3 at δ = 0.003, 8.6 at δ = 0.01.
- Even then M stays above 1 unless the oracle also approaches the idealized all-free floor.
- **Item 2 may be a certified computation rather than new mathematics. N1 does not claim the problem is hard; it claims only that no checked primary source supplies the constant.**

---

## 6. Discrepancies against W0

1. **Direction-select control.**
   - WS-k said "canonical could take that factor as well, but no theorem covers it". That is wrong: BHMT Thm 12 covers it, by the exact distributional identity in §2b.
   - It is a new conditional credit of ×~2, and it needs a call-cost certificate.
   - Effect: primary M 801 → 401 (certified schedule) and 232 → 200 (explicit best). NO-GO is unchanged.
2. **The DP1 window row (k 6.9-7.4, M 8.6) uses δ = 0.01.** The certified and explicit rows use δ = 0.003. Like for like, the window row is k 8.25-8.77 and M 10.3. It also already includes the U1/U2 credits; without them k is 23.5-25.7.
3. **WS-k's lane k_lat** (18 and 2 lanes at W = 1e7) mixes source widths with source depth. With floor designs and a shared T supply, the lane credit is 1.00× for B8x52 and 1.29× for B4x12. The decision table gave no lane credit, which is correct for the decision-critical cell.
4. **The counting bound.**
   - W0 quotes "~1.7-1.85" without the access model. It holds for Q-access (controlled Q^{±1} plus one copy of A|0⟩). Under A/A† access it is 0.85/0.93.
   - The "+one copy of A" term changes it by at most 0.004.
5. **"No explicit constant in any primary source" for window/QSP needs sharpening** to "no usable explicit worst-case constant". Patel Thm 2 plus a random offset is explicit and worst-case, but it is about 1e5× too large.
6. **A label in `decision_table.py`.** `k_classes()` counts "explicit but average-case only" (Patel Thm 2) as an explicit_best candidate. Those rows are never minimal, so no number changes.
7. **WS-k README** says the Grinko and Fukuzawa formulas were not re-fetched. N1 fetched both and verified them.

## 7. Caveats

- Every value here is modelled, apart from σ_q, which is measured. k_10x is taken from WS-floor and was not recomputed here; the headline workstream recomputes it.
- The window c comes from float numerics with a continuous readout, at N ≤ 400. It is extrapolated to N of about 1e4-1e5.
- Lane widths and T counts are the WS-floor modelled designs.
- The direction-select call cost is assumed equal to that of one controlled Grover iterate.
