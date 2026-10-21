# N1 hardware and classical card (plan110 branch N, R1)

Items: H01, H02, C15, H17 (columns), H14/H04/H07 (lines), C09, C10, H16. Written 12 October 2026 under `research/plan110_n1/N1_CARD.md` and the conventions in `research/plan110_w0/W0_CARD.md`.

**Numbers.** All numbers come from `results/plan110_n1/hwclassical/hw_classical_card_v2.json`.
- Script: `hw_classical_v2.py`, run under `.context/frontier_t0_env/Scripts/python.exe -I -S -B` (3.12.4, stdlib).
- Self-check passes with a maximum relative error of 2.2e-16.
- The v1 output is kept but superseded: it used the raw T_C instead of the T_C envelope, which affected only the ε = 0.03 overhead cells.
- Rows: `results/plan110_n1/hwclassical/rows.jsonl`.

**Labels.** Every number below is tagged L = literature (with citation), M = measured, Mo = modelled or A = assumed. Each also has a direction: QF = quantum-favourable, AQ = against quantum, N = neutral.

## 1. Anchor table: logical-cycle and reaction-loop times (H01, H02, C15)

Twelve anchors were checked against primary sources (15 fetches, which is the cap). "Loop" means readout to feedback, unless the row says otherwise.

| id | quantity (its own endpoint definition) | value | × 100 ns | d | platform | year | status | source | verified |
|---|---|---:|---:|---|---|---|---|---|---|
| A02 | decoding-feedback pipeline: syndrome bits → correction ready. **No qubits; excludes readout, ADC/demod and DAC** | 446 ns | 4.5 | 3 | 3× ZCU216 RFSoC, RF loopback | 2026 | demonstrated (partial loop) | L: Liu et al., arXiv:2603.16203 | yes |
| A01 | **complete** loop: end of readout pulse → start of feedback pulse, on a live processor (222 ns DAQ/cabling + 124 ns NN decoder + 180 ns other stages, ≈ 550 ns) | 550 ns | 5.5 | 3 | superconducting, FPGA NN decoder | 2026 | demonstrated (memory, ~0.07-0.10 logical error/round) | L: Yang et al., arXiv:2605.04892 | yes |
| A07 | cat-qubit cycle (a logical gate spans at least one cycle) | 500 ns | 5 | n/a | repetition cat | 2023 | projected | L: Gouzien et al., arXiv:2302.06639 | yes (abstract) |
| A03a | surface-code QEC cycle | 1.1 µs | 11 | 7 | superconducting (Willow) | 2024 | demonstrated (memory) | L: arXiv:2408.13687 | yes |
| A04a | surface-code cycle | 1 µs | 10 | 25 | superconducting | 2025 | projected | L: Gidney, arXiv:2505.15917 | yes |
| A05a | syndrome round = reaction time (options-pricing table I) | 1 µs | 10 | n/a | superconducting | 2025 | projected | L: McArdle et al., arXiv:2510.26078 | yes |
| A06 | fast-feedback response, 8-qubit stability experiment | 9.6 µs | 96 | n/a | superconducting (Rigetti) | 2024 | demonstrated | L: Caune et al., arXiv:2410.05202 | yes (abstract) |
| A04b | reaction time | 10 µs | 100 | 25 | superconducting | 2025 | projected | L: arXiv:2505.15917 | yes |
| A04c | lattice-surgery / CCZ period | 25 µs | 250 | 25 | superconducting | 2025 | projected | L: arXiv:2505.15917 | yes |
| A03b | average real-time decoder latency (no logical feedback loop closed) | 63 µs | 630 | 5 | superconducting (Willow) | 2024 | demonstrated | L: arXiv:2408.13687 | yes |
| A09 | logical processor: 48 logical qubits, 280 atoms, d = 3-7. The repo's 0.5-4 ms neutral-atom layer time is **not** on the primary pages | n/a | n/a | 3-7 | neutral atoms | 2023 | demonstrated | L: arXiv:2312.03982 | existence only |
| A12 | 448-atom fault-tolerant architecture. No absolute cycle time on the abstract page | n/a | n/a | 3-4 | neutral atoms | 2025 | demonstrated | L: arXiv:2506.20661 | partial |
| A08 | active volume: 44× for RSA-2048. The repo's "reaction ≈ 1 µs" is not on the abstract page | n/a | n/a | n/a | photonic/general | 2022 | projected | L: arXiv:2211.15465 | partial |
| A10 | logical magic-state distillation with d = 3 and 5 colour codes. No rate is stated | n/a | n/a | 3, 5 | neutral atoms | 2024 | demonstrated | L: arXiv:2412.15165 | existence only |
| A11 | constant-round transversal fault tolerance. Gain is "potentially > 10×" space-time; no physical time | n/a | n/a | n/a | theory and simulation | 2024 | theory | L: arXiv:2406.17653 | yes |

### Checks on the repo's 446-550 ns d = 3 figures

These figures appear in `docs/limitation_audit_20261001/HARDWARE_AND_COST_MODEL.md` (H01, H02) and in the register rows for H01 and H02.
- **550 ns (Yang): matches the primary source.** It is a complete live-processor loop.
- **446 ns (Liu): the value and d = 3 match, but the register wording "complete loops ... readout-to-feedback" is wrong for Liu.** It is a control-system pipeline with no physical qubits. It excludes the readout pulse, ADC, demodulation and discrimination, and the feedback DAC, so a complete loop on that system would take longer than 446 ns. The repo's own audit document describes it correctly. Liu's d ≤ 21 figure of "under 1 µs" is an extrapolation.
- **Two anchors are unverified** and stay repo-cited: the neutral-atom 0.5-4 ms layer time, and the active-volume reaction time of about 1 µs.
- **Where 100 ns sits (A, QF).** It is below every anchor:
  - 4.5× below the partial 446 ns pipeline;
  - 5.5× below the only complete demonstrated loop, which is at d = 3;
  - 10-11× below demonstrated d = 7 and projected d = 25 cycles;
  - 100-250× below projected application-scale reaction and CCZ periods.
- **No demonstrated d ≥ 15 complete loop exists**, so H01 closes under its own rule. The 100 ns layer is a hypothetical, quantum-favourable convention.

## 2. Necessary-condition columns (H17)

**Requirement.** A 10× win needs k · (σ/e) · F · t_layer ≤ T_C / 10. For the W0 floor F, with W = 1e7 and the Box-Muller current law, this gives the following necessary conditions:
- t_req = T_C / (10 · k · (σ/e) · F);
- an accepted T-state rate of T_call / (F · t_req);
- the floor's logical width.

**Independent path.** T_C (envelope) and σ/e are read from the gap ledger. As a self-check, t_req / 100 ns = k_10x(unlimited) / k.

**Labels.** T_C is M. The floor and k are Mo, and the floor is QF because Cliffords and routing are free.

**Binding cell (B8x52 at $0.001, eligible at zero bias):**

| k class (k) | floor | t_layer required | vs 100 ns | vs 550 ns loop (A01) | T/s required | vs 1e12 budget | logical width (budget 1e7) |
|---|---|---:|---:|---:|---:|---:|---:|
| certified today (682.7) | Box-Muller, 740 layers | 0.39 ns | 258× faster | 1,420× | 1.1e15 | 1,130× | 1.0e7 (= budget) |
| best explicit (197.6) | Box-Muller | 1.34 ns | 75× | 411× | 3.3e14 | 326× | 1.0e7 |
| no explicit constant (7.3) | Box-Muller | 36 ns | 2.8× | 15× | 1.2e13 | 12× | 1.0e7 |
| best explicit (197.6) | all-free + narrow, 112 layers | 8.8 ns | 11× | 62× | 1.3e13 | 13× | 1.85e6 |
| certified today (682.7) | all-free + narrow | 2.6 ns | 39× | 215× | 4.3e13 | 43× | 1.85e6 |

**All non-overhead cells (Box-Muller floor; ε = $0.01 and $0.001; both cases; all k classes):**
- t_req is 0.039-36 ns.
- The required rate is 1.2e13-5.7e15 T/s.

**Comparison with rate and width anchors:**
- Gidney's projected 6 factories × 1/25 µs gives about 2.4e5 CCZ/s (L, derived).
- McArdle's 1e10 T in 3.7 days implies about 3e4 T/s (L, derived).
- The largest demonstrated logical width is 48 (L, arXiv:2312.03982). The projected options-pricing width is 1e4 (L, arXiv:2510.26078).

**Result.** Every necessary condition fails against every anchor, and against the W0 budget, by 1-3 orders of magnitude (t_layer and rate) and by 5 orders of magnitude (width against demonstrated hardware).

**One W0 note (Mo).** At the binding cell M = 232 = 75 × 3.1. The 75 is t_layer. The 3.1 is supply: at 1e12 T/s the call is supply-limited at 2,296 layers, not 740.

## 3. Hardware lines (H14, H04, H07)

- **H14, photonic clock (L, Mo; QF for the claim).** A GHz resource-state clock is not a logical-layer time. The certified and explicit rows need 0.39-1.34 ns, which is below even a 1 ns layer. Only the idealized all-free floor (2.6-8.8 ns) would sit above a GHz clock. A reaction-limited layer still pays detection, feed-forward and decoding, and no anchor has a loop below 446 ns. The item closes as non-closing.
- **H04, constant-round AFT (L: arXiv:2406.17653, verified).** It removes the d-fold round repetition, but each layer still costs at least one syndrome round plus decoding: about 1 µs on superconducting hardware (A03a, A05a), and ms-scale on neutral atoms (repo-cited, unverified). That is ≥ 10× slower than 100 ns, so the latency branch stays closed.
- **H07, cat qubits (L: arXiv:2302.06639, verified).** The projected cycle is 500 ns, so a logical gate is ≥ 5× slower than 100 ns. The benefit is removing the distillation footprint, which acts on the supply and space terms, not on latency.

## 4. Classical side (H16, C09, C10)

### H16 (M; QF only if a 1-core convention is used)

The grid in `results/plan110_w0/ws_small/h16_grid/run001` times preintegration on the Intel Core Ultra 7 155H. The 16-worker times reproduce Stage C C2 within 3.8-10%.

| cell | T(1) s | T(16) s | speedup, 1 → 16 | parallel efficiency |
|---|---:|---:|---:|---:|
| B4x12 $0.01 | 0.882 | 0.137 | 6.44 | 0.40 |
| B4x12 $0.001 | 26.11 | 2.789 | 9.36 | 0.59 |
| B8x52 $0.01 | 4.359 | 0.591 | 7.38 | 0.46 |
| B8x52 $0.001 | 240.18 | 23.46 | 10.24 | 0.64 |

Going from 1 lane to 1 core costs 6.4-10.2×, not 16×. The minimum M for one lane against one core, best explicit constant, is 22.7, so it stays > 1.

### C09: practice CI against a distribution-free 99% CI, quantified from Stage C data

**Practice convention (M; Stage C C2).** 16 RQMC scrambles, Student-t at 99% (t₀.₉₉₅,₁₅ = 2.947), half-width ≤ 0.45 ε, on 16 workers. The quantum k is already a worst-case 99% guarantee: bounded amplitude estimation over the $64 span, with explicit constants. A symmetric distribution-free convention therefore slows only the classical side.

**Distribution-free route (Mo from M inputs).**
- **Bound.** The classical method must use a bound that is valid for any law on [0, S]. It cannot certify QMC rates, so it is restricted to iid replicates. Empirical Bernstein (Maurer & Pontil 2009, Thm 4) is used two-sided at δ = 0.01 with ln(4/δ). S = $40 (A, from the contract: strike 100, knock-out at a basket average of 140); S = $64 is a sensitivity.
- **Routes.** Four routes were costed. The best is iid preintegration:
  - measured σ_preint = 1.248 (B4) and 1.146 (B8), from 2^20 paths in `sigma_dev.json`;
  - measured marginal cost of 1.15 µs per point (B4) and 10.4 µs per point (B8) at 16 workers, from the C2 warm runs.
- **Other routes:**
  - iid plain MC with σ_Q: about 7-9× slower;
  - Hoeffding: about 80-120× slower;
  - RQMC blocks with EB across blocks: 1.1-9× slower, because the S-term forces about 1e6 blocks.

| cell | T_C, practice (M) | n under distribution-free (Mo) | T_C, distribution-free (Mo) | **factor** | factor at S = 64 |
|---|---:|---:|---:|---:|---:|
| B4x12 $0.001 | 2.69 s | 9.46e7 | 108 s | **40.3** | 40.9 |
| B8x52 $0.001 | 22.53 s | 8.02e7 | 831 s | **36.9** | 37.6 |
| B4x12 $0.01 | 0.124 s | 1.16e6 | 1.3 s | **10.6** | 11.9 |
| B8x52 $0.01 | 0.554 s | 1.01e6 | 10.5 s | **18.9** | 21.4 |
| ε = 0.03 / 0.1 (overhead) | intercept-dominated | n/a | n/a | 0.5-3.0 (not used) | n/a |

**M under the distribution-free convention** (primary otherwise; minimum over non-overhead cells, always B8x52 at $0.001):

| k class | Box-Muller floor | all-free floor |
|---|---:|---:|
| certified today | 21.7 (from 801) | 1.08 (from 39.8) |
| best explicit | **6.29** (from 232) | **0.31** (from 11.5) |
| no explicit constant (not eligible under a symmetric convention) | 0.23 | 0.012 |

**Reading.**
- The factor is 10.6-40× in the decision cells, not the 2-5× that W0 assumed. The triage's "quantum needs 10-20× more calls" is already inside W0's span-normalised k, so netting it again double-counts it.
- Under the primary floor, the NO-GO survives this convention (M = 6.3 > 1 for explicit constants), but the margin falls below 30×.
- With this convention plus the idealized all-free oracle, two departures reach M = 0.31. DP1 said three departures were needed.
- **Direction of the remaining uncertainty.** The EB route is conservative. A betting confidence sequence would cut n by up to about 12%, and better iid variance reduction would cut it further. Both lower the factor, so 37-40 is close to the quantum-favourable end. The per-point cost excludes the ≤ 1 s fixed intercept, which is negligible at $0.001.

### C10: scope label (N; AQ, it strengthens the negative)

**Label.** "Strongest *tested* classical method": preintegration + RQMC on a 16-core CPU, numba kernels, practice CI.

**Untested challengers:**
- a GPU implementation (C6 timing missing);
- PDE, finite-difference or sparse-grid solvers (most plausible on B4x12 after dimension reduction);
- multilevel and multi-index MC/QMC;
- control variates (for example, a closed-form geometric basket);
- importance sampling, and conditional MC beyond preintegration;
- compiled C/Fortran kernels;
- regression or neural surrogates.

**Why they can only strengthen the negative.** Any eligible challenger that is faster lowers T_C, which lowers D_max and k_10x and raises M. Leaving a challenger out cannot raise T_C above the measured preintegration baseline. The negative claim is therefore monotone in the classical side, and stating it against the strongest *tested* method is conservative. The same monotonicity also lowers the C09 factor, because a faster iid estimator has smaller σ.

## 5. Discrepancies with W0 and the repo

1. **C09 factor.** The W0 decision table used a modelled 2-5× (`C09_FACTORS` in `decision_table.py`). The Stage C data give 10.6-40.3× in non-overhead cells (36.9× in the binding cell). So M_distfree for best explicit is 6.3, not 46-116; for certified today it is 21.7, not 160-401.
2. **Overturning list.** The DP1 memo says M ≤ 1 with explicit constants needs at least three stacked departures. The all-free oracle plus distribution-free classical rigour, two departures, gives 0.31. The memo does list "a distribution-free classical rigour" as a relaxed convention, but the size of its effect was understated.
3. **H01 register wording.** "Complete loops ... 446-550 ns readout-to-feedback (Yang; Liu)" is wrong for Liu, which is a partial pipeline with no qubits. Only Yang's 550 ns is a complete loop.
4. **Unverified repo citations.**
   - The neutral-atom 0.5-4 ms logical layer and the active-volume reaction time of about 1 µs could not be verified within the fetch cap.
   - The cat-qubit Toffoli duration was not re-verified beyond the 500 ns cycle.
5. **v1 of this card's script** read raw T_C and failed its own self-check in the ε = 0.03 overhead cells. It is superseded by v2.
