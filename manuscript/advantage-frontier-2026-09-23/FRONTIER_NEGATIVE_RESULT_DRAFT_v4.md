# No certified tenfold: a scoped negative result and frontier for quantum pricing of a knock-out basket

**Draft manuscript v4.** 22 October 2026. Affiliation: VIT Vellore.

This is an **AI-assisted draft**. It does not assert author names, review outcome or submission.

**Status of this version**
- **Approval.** The user approved drafting v4 on 22 October 2026. v4 is written from v3
  (`FRONTIER_NEGATIVE_RESULT_DRAFT_v3.md`, unchanged, sha c7ab400d…) by applying the edit list
  `docs/frontier_probe_20261021/V3_EDITS_CURRENT.md`.
- **New inputs.** All new numbers come from:
  - the 21 October frontier probe (P1-P3);
  - the 22 October checklist work on register items C10, C09, H16, C03 and H18.
- **Single source of numbers.** `docs/plan110_status_20261022/CURRENT_NUMBERS.md` (headline run006).
- **Review status.**
  - **The window constant (P2).** Its derivation has had an AI R2 review only; no human review.
  - **Classical-side changes (C10/C09).** These and the later additions had two further AI R2 reviews [REV].
- **Certification debts (debt update, 22 October).** The user authorized every claim-grade debt on 22 October 2026,
  including circuit work. Each one is now done at **R1**: two independent computation paths, or one exact path plus
  an independent recount, with inputs cited by sha256 and outputs created exclusively.
  - **A2a.** The binding cell's bias is certified at 3.634e-4 ≤ 0.55ε with the source unchanged [A2A]. This replaces
    the A02 bridge rerun and the A07/A13 re-proofs.
  - **U1.** The mean certificate is issued [U1C].
  - **U2 and C11.** The U2 support-tight wrapper is built and verified, and the full Grover iterate is compiled
    [C11C].
  - **C03/E07.** The complete-price ledger is complete for both window classes [C03L].
  - **H06, H17 and H18.** These have necessary-condition columns [H617], [C03L].
  - **Scope #44.** The merged headline scope is an independent recompute in new code [S44].
- **What is still not done (R2).** None of the debts is R2. R2 additionally needs:
  - preregistration through the limitation program's lifecycle;
  - a sealed run with a saved verifier and a receipt (writing under `.context/` is reserved for the user);
  - human peer review, in particular of the P2 derivation, A2a proof steps 2 and 4, and the U1 premises.

  PLAN_110 §4 requires R2 for the window class, because its margin (26×) is below 30×.
- **Sign-off.** The N1 card's sign-off requirement applies to whichever version is submitted.

**Number rule.** Every number below comes from a result file named by a source key, or is a product or ratio of
such numbers computed by a named script. Each number carries a label and a direction:

- labels: **meas** (measured), **mod** (modelled), **assm** (assumed), **lit** (literature, with citation);
- directions: **q+** (quantum-favourable), **q−** (against quantum), **0** (neutral).

**Where measurements disagree.** Where a measured input was uncertain, v4 takes the quantum-favourable (QF) end, as
the Stage C specification requires ([SPC] §0.5). The one exception is the classical comparator, which is a minimum
over validated methods ([SPC] §0.3). That choice is classical-favourable (CF) and is labelled.

Source keys (paths relative to the repository root). Keys from v3 are kept; new keys are marked *new*.

| Key | File | Producer |
|---|---|---|
| [HT] | `results/plan110_n1/headline/headline_table.json` | N1-headline, `headline_m.py` (v3 inputs) |
| [HT6] *new* | `results/frontier_probe_20261021/headline/run006/headline_table.json` | copy of `headline_m.py` with measured overrides: `research/frontier_probe_20261021/headline_m_probe.py run006 results/c10_challengers_20261022/overrides_run006.json` |
| [RC] | `results/plan110_n1/headline/receipt.md` | N1-headline receipt |
| [KF] | `results/plan110_n1/headline/keff.json` | N1-headline, `e07_keff.py` |
| [FS] | `results/plan110_n1/headline/floor_sheet.json` | N1-headline, `floor_sheet.py` |
| [ES] | `results/plan110_n1/estimator/estimator_recompute.json` | N1-estimator |
| [EC] | `research/plan110_n1/estimator/estimator_card.md` | N1-estimator card |
| [HW] | `results/plan110_n1/hwclassical/hw_classical_card_v2.json` | N1-hwclassical |
| [HC] | `research/plan110_n1/hwclassical/hw_classical_card.md` | N1-hwclassical card |
| [P1] *new* | `results/frontier_probe_20261021/p1/run001/p1_span.json`, `p1/run002/p1b_hybrid.json` | probe P1, `p1_control_span.py`, `p1b_hybrid.py` |
| [P2] *new* | `results/frontier_probe_20261021/p2/run002/p2_window.json`; `docs/frontier_probe_20261021/P2_DERIVATION.md` | probe P2, `p2_window_constant.py`, `p2b_parts34.py` |
| [SM] *new* | `results/frontier_probe_20261021/p2/run003_self_mean/p2c_self_mean.json` | `p2c_self_mean.py` |
| [P3] *new* | `results/frontier_probe_20261021/p3/run006/p3_desk.json` | `p3_oracle_desk.py run006` |
| [C10] *new* | `docs/c10_challengers_20261022/STATUS.md`; `results/c10_challengers_20261022/timing/run001`, `timing_f32/run001`, `f32/run001.json`, `c2_harness_today/run001.json`, `rate_cv/`, `rate_smooth2/`, `f06_f07/` | C10 wave |
| [C09] *new* | `results/c10_challengers_20261022/c09/*/c09_g4.json`, `c09b/*/c09b_rep.json`, `f32_consistency/run001` | `c09_g4.py`, `c09b_rep.py`, `f32_consistency.py` |
| [H16F] *new* | `results/c10_challengers_20261022/h16_fast/run001/h16_fast.json` | `h16_fast.py` |
| [C03] *new* | `docs/c03_skeleton_20261022/C03_SKELETON.md` | C03/H18 desk record |
| [LIT2] *new* | `results/frontier_probe_20261021/p2/lit_check.jsonl` | literature check (8 sources) |
| [REV] *new* | `results/frontier_probe_20261021/review/p1_review.jsonl`, `p2_review.jsonl`, `r3_review.jsonl`; `results/c10_challengers_20261022/review/c10_review.jsonl` | AI R2 reviews |
| [BD] | `results/plan110_w0/ws_small/bias_desk_run001/bias_desk.json` | W0 bias desk |
| [SPC] | `manuscript/advantage-frontier-2026-09-23/ANALYSIS_SPEC_STAGE_C.md` §0.3-0.5 | Stage C specification |
| [W0C] | `research/plan110_w0/W0_CARD.md` | conventions |
| [REG] | `results/plan110_w0/register/run001/REGISTER.md` (W0) and `run008/REGISTER.md` | 110-item register |
| [DP1] | `docs/program_plan_20261010/DP1_MEMO.md` | DP1 decision memo |
| [A2A] *debt* | `results/claim_debts_20261022/a2a/run001/{certificate,independent,summary}.json`; `docs/claim_debts_20261022/A2A_CLIP_SPLIT_CERTIFICATE.md`; review `results/claim_debts_20261022/review/a2a_review_summary.md` | `clip_split_certificate.py`, `independent_recompute.py` |
| [U1C] *debt* | `results/claim_debts_20261022/u1/run001/{eb_sample,u1_certificate,u1_independent,summary}.json`; `docs/claim_debts_20261022/U1_CERTIFICATE.md` | `eb_sample.py`, `u1_certificate.py`, `u1_independent.py` |
| [C11C] *debt* | `results/claim_debts_20261022/c11/run001/{u2_wrapper,iterate_compile,iterate_recount_pathB,estimator_compile,summary}.json`; `docs/claim_debts_20261022/C11_U2_COMPILE.md` | `u2_wrapper.py`, `iterate_compile.py`, `recount_independent.py`, `estimator_compile.py` |
| [C03L] *debt* | `results/claim_debts_20261022/c03/run001/c03_ledger.json` | `research/claim_debts_20261022/c03/c03_allocation.py` |
| [H617] *debt* | `results/claim_debts_20261022/h06_h17/run004/h06_h17.json`; `docs/claim_debts_20261022/H06_H17_DESK.md` | `h06_h17_desk.py run004` |
| [S44] *debt* | `results/claim_debts_20261022/scope44/run001/scope44_receipt.json`; prospectus `docs/claim_debts_20261022/SCOPE44_PROSPECTUS.md` | `scope44_recompute.py` (new code; does not import the headline script) |
| [REG9] *debt* | `results/plan110_w0/register/run009/REGISTER.md` and `CHANGES.md` (current register) | `research/claim_debts_20261022/register_run009.py` |

Keys marked *debt* were added by the 22 October debt update; `docs/claim_debts_20261022/CLAIM_DEBTS_STATUS.md`
summarizes them.

The v3 keys [DN], [AD], [NC], [DC], [FX], [FX2], [RK] and [V3] are kept for the numbers v4 inherits unchanged. See
v3's source table.

**Provenance.**
- **Stdlib scripts.** The probe, register and checker scripts ran under `.context/frontier_t0_env/Scripts/python.exe
  -I -S -B` (3.12.4).
- **Harness scripts.** The classical timings, the distribution-free runs and the RQMC rate studies use the Stage C
  harness (numpy, numba, scipy, same environment), run without `-I`.
- **Number check.** `research/frontier_probe_20261021/v4_check.py` checks every headline number in this draft
  against the result files (`results/frontier_probe_20261021/v4_check/run001.json`).
  `research/claim_debts_20261022/v4_check_debts.py` repeats those checks and adds the debt-update numbers
  (`results/claim_debts_20261022/v4_check/run001.json`).
- **Isolated environment location.** In the worktree the isolated environment is reached as
  `../../../.context/frontier_t0_env/Scripts/python.exe`. It lives in the main repository root.

---

## Abstract

We ask whether any quantum amplitude-estimation design can price one fixed, discretely monitored basket knock-out
call with at least ten times lower complete latency than the strongest classical method we tested. There are two
cases, 4 assets × 12 dates (B4x12) and 8 assets × 52 dates (B8x52), priced to $0.01 or $0.001 per $100 notional. We
compare a quantum machine of 1e7 logical data qubits (magic-state factories not counted), 100 ns logical layers and
1e12 T states per second against one measured 16-core CPU.

**The two sides are not held to the same confidence standard.** The quantum side must meet a worst-case 99%
guarantee. The classical side uses practice confidence intervals (Student-t over 16 RQMC scrambles), which are not
a guaranteed 99%. This is the primary convention fixed in [W0C]. Holding the classical side to the symmetric,
distribution-free 99% standard costs it **17.3×** at the binding cell. That factor is measured: it is the cheapest
of two timed distribution-free methods, and it replaces v3's modelled 36.9× (meas, q+) [C09].

We write the requirement as one ratio, M = k / k_10x:
- k is the estimator constant achieved (controlled Grover calls per σ/e);
- k_10x is the largest constant that still gives a tenfold win, given an idealized oracle-call depth floor and the
  measured classical time.

M ≤ 1 means tenfold is reached. The binding cell is B8x52 at $0.001. It is now eligible on a **certified** bias
bound, 3.634e-4 ≤ 0.55ε (R1), with the source unchanged [A2A] (§2).

The **classical time** is T_C = **8.89 s** at the binding cell (meas, CF selection) [C10]. This is the Stage C
estimator with faster arithmetic: closed-form date roots, compiled inverse normals, and a single-precision matrix
multiply that passes the specification's ε/10 rule. Taking the QF end of the measured speedups, it is 2.54× faster
than Stage C's 22.53 s, which is kept as a sensitivity (§4.3).

M at the binding cell (all mod) [HT6]:

| Estimator class | k | M, primary | Best single departure | Departures needed for M ≤ 1 |
|---|---:|---:|---|---:|
| Certified today (E07 schedule) | 682.7 | **2,032** | all-free oracle 100.9 | 3 |
| Canonical explicit (U1 + U2 + non-dyadic M) | 197.6 | 588.1 | all-free oracle 29.2 | 3 |
| **Window, explicit worst-case constant (this work; U1 + U2 + direction-select)** | **8.762** | **26.1** | all-free oracle **1.29**; symmetric classical 1.50 | **2** |
| Window, quantum-only mean bound (U2 + direction-select) | 9.058 | 27.0 | all-free oracle 1.34; symmetric classical 1.55 | 2 |

**What is new in v4: an explicit constant for the window estimator.** v3 listed window/QSP amplitude estimation
as having "no usable explicit worst-case constant". v4 supplies one (§4.2):
- **The bound.** A Kaiser window with closed-form transform, plus an explicit Poisson-aliasing bound, gives a
  concentration bound certified at N₀ = 800 that holds for every larger N.
- **The constant.** With finite readout and implementation error made explicit, c(0.003) = **4.179** [P2]. That
  gives **k = 8.762** at the binding cell.
- **Without the classical price.** A two-stage version earns the mean bound quantumly instead of from an
  uncertified classical price, at k = 9.058 [SM].

**Claim:** "No design with certified constants reaches a 10× complete-latency advantage for the fixed B4x12/B8x52
knock-out task under the stated conventions."

Scope:
- **What the claim covers:** this construction family (coherent fixed-point oracle plus bounded amplitude
  estimation), the fixed task, and the strongest tested classical method.
- **"Certified constants"** refers to the estimator constant; oracle costs are modelled idealized floors.
- **"Complete latency"** counts the Grover iterates only (§8).
- **Achievability, not a lower bound.** The rigorous black-box lower bound on k is about 1.85, against 8.76
  achieved.

**As a checkable threshold** (mod, derived) [HT6], [P3]: at the binding cell and primary conventions, a
window-class design reaches tenfold only if one controlled Grover iterate takes at most **88 reaction layers and
8.8e6 T**. The idealized all-free oracle floor is 114 layers, so it misses by 29% (M = 1.29).

**Robustness.** At the primary conventions the negative holds with a **26× margin**. **No single favourable
departure overturns it** for any explicit class (closest: the idealized all-free oracle, 1.29). **Two departures
together do:**
- all-free oracle + symmetric distribution-free classical, 0.075;
- all-free + one quantum lane against one classical core, 0.135;
- one lane + symmetric, 0.156.

We name the levers that would overturn the result (§6):
- an oracle within about 1.3× of the idealized all-free floor, which would also need a free exponential;
- a change of two conventions or idealizations at once;
- a further estimator gain of about 26× at the current oracle.

Three escapes v3 left open are now closed:
- the control-variate residual oracle (F20/F04), closed by probe P1;
- the classical control variates under RQMC, closed by C10;
- multi-direction smoothing, closed by C10.

**Certification status (debt update, 22 October; R1, not R2).**
- **Window premises.** The window class's premises are now certified at R1:
  - U1: a mean bound m = 3.28804 ≥ E[g] with probability 1 − 1e-4, which covers the m that P2 assumed [U1C];
  - U2: the support-tight wrapper, built and verified, at +11,578 T per iterate [C11C].
- **Complete price.** The ledger is complete at the binding cell for both window classes. The failure budget is
  allocated in full, with the physical-failure share stated as an explicit hardware premise. The bias plus readout
  fits inside 0.55ε [C03L].
- **Compiled iterate.** Compiling the full controlled Grover iterate of the saved source gives a window M of
  **2,290** at the floor's own conventions, and at least 277 under every reading [C11C]. The headline floor is
  therefore quantum-favourable by about 88×.
- **Independent recompute.** A recompute in new code reproduces the binding-cell headline row exactly [S44].

---

## 1. Introduction and scope

The project's foundation document, [WHY_NO_ADVANTAGE.md](WHY_NO_ADVANTAGE.md), explains why six constructions
failed to produce a significant advantage. Those six span three option contracts and were built with one toolchain
(register item C12). The sixth, Failure 6, is the discretely monitored knock-out basket that Stage C measured
([STAGE_C_STATUS.md](STAGE_C_STATUS.md)). This draft turns that construction into a scoped frontier statement.

The question is whether **any** design in this construction family can reach tenfold once each of three
ingredients is pushed to its idealized limit:
- the oracle call;
- the estimator constant;
- the hardware.

The **scope** of the claim is the conjunction of three things:
1. **This construction family.** A coherent fixed-point oracle for the payoff (not a residual or preintegrated
   payoff), wrapped in bounded amplitude estimation.
   - The evidence covers oracles that cost at least the idealized floor (§4.1).
   - **As a checkable threshold (§3):** the claim covers every window-class design whose Grover iterate at the
     binding cell costs more than about 88 reaction layers or more than about 8.8e6 T. It also requires that the
     iterate exceed the corresponding per-cell limit in the other decision cells (§3).
   - **Weaker estimator classes** have proportionally tighter limits: canonical explicit 3.9 layers / 3.9e5 T,
     certified today 1.1 layers / 1.1e5 T.
2. **The fixed task.** One discounted price of the contract in §2, for the two cases.
3. **The strongest tested classical method.** Preintegration plus RQMC with faster arithmetic (§4.3) on a 16-core
   CPU, with practice confidence intervals.

**What the claim does not say.** It does not say that quantum advantage in option pricing is impossible. It does
not cover other tasks, other access models or untested classical challengers (§6-§8). Residual and preintegrated
oracles are not covered by the claim's wording either. The P1 probe examined them separately and closed them (§7.1).

---

## 2. The task and its conventions

**Contract.** An equal-weight basket knock-out call, with S0 = K = 100, barrier H = 140, σ = 0.3, ρ = 0.4,
r = 0.03 and T = 1.
- The payoff is e^{−rT}(A − K)⁺·1{every date basket < H}, where A averages over all assets and dates.
- It is monitored on 12 dates over 4 assets (B4x12) and on 52 dates over 8 assets (B8x52).

**Payoff and error.**
- The payoff support is [0, 38.818] (E03).
- The quantum-side payoff standard deviation is σ_q = 5.66357 (B4x12) and 5.18340 (B8x52) (meas, 0) [EC].
- The output is one price within ε ∈ {$0.10, $0.03, $0.01, $0.001} at 99% confidence. Only ε = $0.01 and $0.001 are
  decision cells.

**Conventions.** These were fixed in [W0C] on 11 October 2026. The primary value is used for the claim; every other
value is a sensitivity column.

| Convention | Primary | Sensitivity columns |
|---|---|---|
| Parallelism matching | One quantum machine against one 16-core classical machine | 1 lane vs 1 core; L lanes vs 16 cores |
| Classical confidence | Practice confidence intervals (Student-t over 16 RQMC scrambles; not a guaranteed 99%). This is the convention that departs from symmetry | Distribution-free 99%, symmetric with the quantum worst-case guarantee. **Now measured** (§4.3) |
| Width budget W | 1e7 logical **data** qubits; factories outside W (q+) | 1e6, 1e8, unlimited |
| Magic-state supply | 1e12 accepted T states per second | 1e11, 1e13 |
| Logical layer time | 100 ns | 10 ns, 1 µs, 10 µs |
| Statistical split | e = 0.45ε on both sides (classical share labelled QF in [SPC]) | e = ε |
| B8x52 at $0.001 | **Eligible on a certified bias**: ≤ 6703058386012589/2^64 = $0.0003634 ≤ 0.55ε, with the source unchanged (R1; two paths agree to 9.4e-13) [A2A]. The clamp-tightening route ($0.000473, mod [BD]) and its A02/A07/A13 re-certification are no longer needed | Strict zero-bias reading e = ε: window 11.7. Counterfactual "ineligible" reading: B4x12 $0.001 binds, window 36.2 (q−) [HT6] |

**The binding cell's bias certificate (A2a; mod, R1)** [A2A].
- **The old bound.** The saved finite-source-to-continuous-price bridge (A02 run002, independently audited) bounds
  the bias at $0.0012396 for B8x52. That is above 0.55ε. The clamp leak ℓ ≈ 2^-16 from the native stock lower clamp
  drives 71% of it [BD].
- **The split.** The new certificate separates out the event C that some native stock site takes its lower clamp:
  - on C^c the leak drops to the 2^-40 grid;
  - on C the payoff error is at most the $40 cap.
- **The clamp probability.** P_fin(C) is bounded under the finite Box-Muller input law by a one-sided Bernstein bound
  (primary) or a Bennett bound (independent). Each is combined with a union over the 104 sites that can clip (all 8
  assets at dates 40-52): P_fin(C) ≤ 1e-29.
- **Result.**
  - B8x52 bias ≤ $0.0003634, with $0.000187 to spare under 0.55ε.
  - B4x12 ≤ $0.00001207; no site there can clip.
- **Review.** An independent AI adversarial review found the certificate sound, with two minor documentation fixes
  (both applied) and no major finding. There has been no human review.
- **Premises.** It inherits every premise of the run002 bridge.

**The classical time.** T_C is the minimum measured time over validated estimators, with a monotone envelope
across ε ([SPC] §0.3; meas, CF selection) [HT6], [C10]. In the decision cells:

| Cell | T_C (v4) | Stage C T_C (v3) |
|---|---:|---:|
| B4x12 $0.01 | 0.0583 s | 0.1244 s |
| B4x12 $0.001 | 1.0475 s | 2.688 s |
| B8x52 $0.01 | 0.3062 s | 0.5535 s |
| B8x52 $0.001 | **8.886 s** | 22.529 s |

**Machine-state caveat** (§4.3, §8). The v4 times come from the 1 October Stage C times divided by speedups
measured as same-state ratios on 22 October. On 22 October the laptop ran the unchanged Stage C harness 2.2× faster
than on 1 October (Windows power-mode overlay at Best performance; meas) [C10]. Absolute times measured on
22 October are therefore used only as CF sensitivities.

---

## 3. The inequality and the gap ledger

Let D_eff be the effective depth of one controlled Grover iterate, in reaction layers:

> D_eff = max(reaction depth, T per iterate / (supply × t_layer)).

The largest per-call depth that still gives a tenfold win, written for k = 1, is
D_max(k=1) = T_C / (10 · (σ/e) · t_layer). From this, k_10x = D_max(k=1) / D_eff and **M = k / k_10x**.

**Gap ledger at the binding cell, B8x52 at $0.001, primary conventions:**

| Quantity | Value | Label | Source |
|---|---:|---|---|
| T_C | 8.886 s (Stage C 22.529 s) | meas; CF selection; QF end of the speedups | [HT6], [C10] |
| σ/e | 11,518.7 | mod (σ measured), 0 | [HT6] |
| D_max(k=1) | 771.5 layers | mod, 0 | [HT6] (derived) |
| D_eff, W0 floor (used) | 2,296 layers, supply-bound | mod, q+ | [HT6] |
| D_eff, N1 floor (not used) | 3,605 layers | mod, q+ | [HT6] |
| k_10x | 0.336 | mod, 0 | [HT6] |
| k: certified / canonical explicit / window certified / window quantum-only mean | 682.7 / 197.6 / 8.762 / 9.058 | mod | [HT6], [P2], [SM] |
| **M: certified / canonical / window / window (quantum-only mean)** | **2,032 / 588.1 / 26.1 / 27.0** | mod, 0 | [HT6] |

Three features of the ledger matter for everything that follows.

1. **Even k = 1 fails, by a factor of 3.** k_10x = 0.336, so an estimator at the rigorous black-box floor (about
   1.85) would still miss by about 5.5×.
2. **Supply binds before depth.** At 1e12 T/s the B8x52 iterate is supply-bound at 2,296 layers against its 740
   reaction layers.
   - At 1e13 T/s the window M is 8.40.
   - At 10 ns layers it is 22.5, with the minimum moving to B4x12. The B8x52 iterate stays supply-bound [HT6].
3. **The thresholds a design must beat** (mod, derived) [HT6], [P3]. M ≤ 1 needs D_eff ≤ D_max(k=1) / k. With
   D_eff = max(reaction depth, T / (1e12 T/s × 100 ns)), a design must meet **both** limits below on one controlled
   Grover iterate at the binding cell:

   | Estimator class (k at the binding cell) | Max reaction layers per iterate | Max T per iterate | Idealized all-free floor (114 layers) |
   |---|---:|---:|---|
   | **Window, certified (8.762)** | **88.1** | **8.8e6** | above the limit by 1.29× (M = 1.29) |
   | Window, quantum-only mean (9.058) | 85.2 | 8.5e6 | above by 1.34× |
   | Canonical explicit (197.6) | 3.90 | 3.9e5 | above by 29.2× |
   | Certified today (682.7) | 1.13 | 1.1e5 | above by 101× |

   - **Symmetric convention.** Under the symmetric distribution-free classical convention, every limit rises by
     the measured factor of 17.3. For the window class that is about 1,530 layers, which the all-free floor
     satisfies (M = 0.075 for that pair).
   - **Other decision cells.** These limits are for the binding cell; each other decision cell has its own,
     generally lower, limit. The B4x12 all-free floor (94 layers [HT]) is above the window limits there too (§5).

---

## 4. Results

### 4.1 The oracle floor, and why supply binds

Unchanged from v3 (mod, q+) [FS], [RC], [HT]:
- **Two independent floors.** W0's floor and N1's analytic formula sheet, from cited literature constructions
  (lit, not re-fetched).
- **B8x52 compute path.** 278 layers, 1.87e8 T per compute.
- **B8x52 Grover iterate** at W = 1e7, 1e12 T/s and 100 ns. It is supply-bound in both floors: D_eff = 3,605 for N1
  and 2,296 for W0, the more favourable one, which is used.
- **All-free oracle** (free loader and exponential, 48-bit words): D_eff = 114 for W0 and 163 for N1.

The two floors differ by more than 10% in 165 of 180 convention pairs; the more quantum-favourable value is used in
each pair. With N1's floor alone, the binding-cell window M is 40.9 [HT6].

**What a design would need (P3; desk, mod) [P3].** These are existing modelled variants of the W0 and N1 floors at
the binding cell, with the window constant:

| Oracle design (B8x52, W = 1e7, 1e12 T/s, 100 ns) | D_eff (layers) | Window M |
|---|---:|---:|
| Box-Muller, current law (W0) | 2,296 | 26.1 |
| Free loader alone (F05) | 1,211 | 13.8 |
| Best loader + free exponential | 215.5 | 2.45 |
| Free loader + free exponential, 72-bit (N1 sheet) | 173 | 1.96 |
| All-free and narrow (W0) | 114 | 1.29 |

Neither the loader nor the exponential alone helps much. Even both near-free together (the all-free floor) leave M
at 1.29. M ≤ 1 at the primary conventions needs D_eff ≤ 88 layers.

**The compiled iterate against the floor (C11; R1)** [C11C].
- **What was compiled.** The full controlled Grover iterate of the saved B8x52 source (A10 min-depth source, E02
  wrapper), with the U2 selector in place of the 46-bit selector. The parts are F, the selector, CZ, the selector
  inverse, F⁻¹ and the controlled reflection.
- **Counts per iterate** (meas):

  | Quantity | Value |
  |---|---:|
  | T, literal count (seven T per Toffoli) | 4,267,659,718 |
  | T, at the floor's 4 T per Toffoli | 2.44e9 |
  | Toffolis | 609,665,674 |
  | Logical qubits, including estimator registers | 4,460,627 (inside 1e7) |
  | Toffoli depth | 201,263 |
  | Literal T-depth | 776,965 |

  Against the floor's 2.30e8 T, the literal count is 18.6× and the 4-T-per-Toffoli count is 10.6×.
- **Recount.** Two independent recount paths agree exactly on every field, and both reproduce the saved
  `iterate.json`.

| Reading of the compiled iterate (window certified, N = 100,924, primary conventions) | D_eff (layers) | Window M |
|---|---:|---:|
| Floor (W0, used in the headline; mod, q+) | 2,296 | 26.1 |
| Compiled, floor conventions (reaction-bound Toffoli depth; meas counts, mod convention) | 201,263 | **2,290** |
| Compiled, literal seven-T T-depth | 776,965 | 8,828 |
| Compiled, most favourable (unlimited-width leaf schedule plus an unbuilt log-depth reflection; mod, q+) | 95,101 | 1,084 |
| Compiled, supply only, ignoring reaction depth (floor conventions; q+) | 24,387 | 277 |

- **Ratio to the floor.** At the floor's conventions the compiled window M is 87.8× the floor's. The compile can only
  raise M, so the headline floor is a quantum-favourable reading and the negative is conservative on the quantum
  side.
- **Two figures for the compiled M.** The quantum-only-mean class gives 2,367 at floor conventions. The C11 figure
  (2,290) includes the estimator-level step code and phase register. The scope #44 recompute uses iterate depth only
  and gives 2,286 [S44].

### 4.2 The estimator constant bracket and its access model

**Access model** (unchanged) [EC] §1.
- **Access.** Black-box state preparation A, controlled Q, Q⁻¹ or direction-select, plus query-free operations.
- **Guarantee.** |μ̂ − μ| ≤ e with probability ≥ 1 − δ for every payoff law on [0, S].
- **Cost unit.** One controlled Grover iterate.
- **Failure share.** The estimator's share of the failure budget is δ = 0.003.

**Certified today** (unchanged) [KF]. The canonical BHMT Theorem 12 schedule with 15 medians, giving
k = 585.8-1,066.7 over all cells (682.7 at the binding cell).

**Canonical explicit** (unchanged) [EC] §2b. k = 186.6-198.2, with three conditional credits:
- U2, the support-tight wrapper;
- U1, the mean certificate (price + L1, an uncertified classical orientation value);
- non-dyadic M.

Without U1 it is 353.0 at the binding cell.

**New: an explicit worst-case constant for window amplitude estimation** (mod, q+ relative to the canonical
constant) [P2]. The full derivation is in `docs/frontier_probe_20261021/P2_DERIVATION.md`.

- **Window.** The Kaiser window w_n = I0(β√(1−(n/N)²)) for |n| < N, with half-weight end taps and β = 3.87.
  - Its exponents run −N..N, so N controlled calls with direction-select.
  - Its continuous transform is closed form.
- **Parts 1-2 of the open problem** (concentration, uniform in N).
  - Poisson summation splits the window's transform into N·Φ(Nω) plus an aliasing term with an explicit bound.
  - Expanding the energies exactly gives λ0(N, c/N) ≥ (N·I_c/2π − X_band)/(N·I_tot/2π + X + C_R²). Every correction is
    explicit and O(1) or O(1/N).
  - The bound increases with N, so certifying it at N₀ = 800 covers every larger N.
  - I_tot is an exact rational series; I_c uses 50-digit quadrature with a rigorous error term.
- **Part 3** (finite readout, every phase). A G-point QFT with G ≥ 2N+1 and a discrete random known phase offset
  (K = 2⁴⁰). The loss is at most (2N+1)(1+4c)/(GK) < 1e-11.
- **Part 4** (implementation precision). Rotations are synthesized to 2⁻⁴⁰ (Ross-Selinger; lit). The failure
  probability rises by at most 1.9e-6, and 4e-6 is reserved.
- **Result.**
  - c(0.003) = **4.179** and c(0.01) = 3.510, for all N ≥ 800, parts 1-4 explicit.
  - At the binding cell, **k = 8.762** (N = 100,924 calls) at δ = 0.003 and 7.359 at δ = 0.01.
  - The uncertified DPSS numerics of v3 gave 4.168.
- **Checks.**
  - The exact discrete concentration (FFT, float) gives 1 − λ0 = 2.97059e-3 ≤ 3e-3 at the binding N.
  - An AI R2 review re-derived every inequality, brute-forced N up to 300,007 with no violation, and found no
    critical or major error [REV].
- **Conditions it inherits:**
  - the U1/U2 credits, as the canonical explicit row does. Both are now certified at R1 (below).
  - the direction-select call cost. It is exact in this paper's Clifford+T cost model. The compiled step code that
    drives the controlled powers is built and verified for every phase value [C11C].

**Debt update: the U1 and U2 premises certified (R1).**
- **U1 mean certificate** (mod; meas sample) [U1C].
  - **Statement.** With probability ≥ 1 − 1e-4, E[g] ≤ m = **3.28804**. It combines three pieces:
    - a one-sided empirical-Bernstein bound (Maurer & Pontil; lit) on 2^23 raw continuous payoffs, with n fixed
      before sampling, range R = 40 (analytic), sample mean 3.27960 and half-width 0.00808;
    - a 1e-9 float slack (assm);
    - the A2a bias bound [A2A].
  - **Coverage.** m is 0.0388 below the m = 3.32682 that P2 assumed (uncertified price plus a B4x12-borrowed L1).
    So **k = 8.762 now rests on a certified premise**. Using m itself would give k 8.715 and M 25.94; v4 keeps 8.762.
  - **Failure budget.** The certificate's failure share, 1e-4, is charged to the failure budget (§8).
  - **Premises (assm).** The generator's draws are iid, and the float slack is assumed rather than derived.
- **U2 support-tight wrapper** (meas counts) [C11C]. Built as an explicit gate list:
  - **Design.** A ×211 constant multiplier and a 53-bit comparator, with uncompute.
  - **Tests.** 40,000 exhaustive small-width cases and 4,281 full-width edge and random cases pass. Built with
    multiplier 1 and 46 bits, the builder reproduces the saved selector exactly.
  - **Support.** 211 · 42,680,645,956,484 < 2^53, from the audited E03 support.
  - **Cost.** +11,578 T per iterate (2.7e-6 relative) and 0 extra logical qubits.
  - **Readout.** The re-derived readout allowance is 4.55e-13, inside the 2^-39 placeholder (mod).

**New: the U1 credit replaced by a quantum-only first stage** (mod) [SM].
- **Stage 1** (failure 1e-4, no mean credit, 1,730 calls) gives a certified upper bound on the mean, worst case
  3.418 against the true 3.282.
- **Stage 2** (failure 0.0029, 102,602 calls) uses that bound.
- **Cost.** k = **9.058**, about 3.4% more than with U1's classical price. No classical input remains; the
  remaining conditions are U2 and direction-select. Both are now certified at R1 (above).
- **Constants.** Both stages' constants are certified by the same machinery: c(1e-4) = 6.052 and c(0.0029) = 4.197.
- **Tail case.** The 104,332-call cost is the worst case over stage-1 successes. With probability ≤ 1e-4 the capped
  stage 2 can take up to 182,785 calls [REV].

**Without the conditional credits.** The window class gives k = 25.8 (span 64, no mean bound; M 76.8) or 17.5
without direction-select (M 52.2) [HT6].

**Literature** (lit) [EC] §4, [LIT2]. Eight further primary sources were checked:
- **Kothari & O'Donnell** (2208.07544): not explicit; σ-normalised.
- **Hamoudi** (2108.12172): Thm 4.2 not explicit; Prop 4.1 is canonical plus medians.
- **Rall** (2103.09717): Prop 5 is canonical plus medians; the QSP results are not explicit.
- **Kimmel-Low-Yoder** (1502.02677) and **Belliardo-Giovannetti** (2007.02994): RMSE only.
- **AQAE** (2407.16795) Thm 2: explicit, with c(0.003) ≈ 409.
- **RQAE** (2204.13641) and **Labib** (2609.02715): abstracts only.

None gives a worst-case coverage constant below canonical. The window certificate above is this work's derivation,
not a literature result.

**Counting lower bound** (unchanged; mod, rigorous) [EC] §1. k_LB = 1.848-1.853 for B8x52 at δ = 0.01. The
achievability gap is now 8.762 / 1.85 ≈ **4.7×**; it was about 100× in v3.

**Lanes** (unchanged) [EC] §3. The binding cell gets no lane credit; window chains are one coherent chain.

### 4.3 Classical parallelism, classical confidence, the comparator, and hardware coverage

**The comparator (C10)** (meas) [C10]. The Stage C `preint` estimator is unchanged: the first canonical PCA
direction is integrated analytically. Its arithmetic is faster:
- **Closed-form date roots.** The first canonical column has loading constant within each date. So the 52 barrier
  roots are closed form, the strike root is a 52-term Newton solve, and the integral needs 2·52 + 2 normal CDFs
  instead of 2·416 + 2.
- **Compiled inverse normal.** Wichura AS241, matching scipy to 1.2e-15 relative.
- **Single-precision GEMM.** It passes the specification's ε/10 admission rule (mean shift about 1e-9, largest
  per-point difference 1e-5).
- **Same estimand.** Per-point agreement with the Stage C kernel is |Δ| ≤ 9.5e-13 on fresh and extreme points [REV].

**Paired timing** under the item C2 protocol: 16 workers, 16 scrambles, item C2's n_run, the same Sobol points
across methods, interleaved.

| Binding cell B8x52 $0.001 | Time |
|---|---:|
| Stage C pipeline | 10.26-11.22 s |
| Fast kernel + AS241 | 4.94-5.01 s |
| + float32 GEMM | 4.11 s |

These are 22 October absolute times, CF. The speedups used are QF:
- fast over Stage C: 2.078, the minimum over three same-state measurements (2.08-2.25);
- float32 over fast: 1.220 (paired);
- product: **2.535**, so **T_C = 8.89 s**. Multiplying the two ratios assumes the ratios carry over to the
  1 October machine state (assm).

**Challengers killed:**
- **Control variates on top of preintegration.** iid σ ratio 1.81, but RQMC error ratio 1.00 at every n from 2⁶ to
  2¹⁸, because RQMC already integrates the smooth controls.
- **Two-direction smoothing.** About 1.3-1.5× slower than preint at the quadrature order needed for bias ≤ 0.1ε.
- **Rare-event importance sampling (F07).** The top 1% of payoffs carry 6.6% of the price.
- **Isolating the barrier-date switching surface (F06).** The surface is dense: the two smallest roots are within
  0.05 in 44% of paths.

**Untested:** GPU (no CUDA device; q−). PDE/sparse grids and MLMC/MIMC are not applicable (desk) [C10].

**Classical parallelism (H16)** (meas) [H16F]. The 1-worker / 16-worker ratio of the fast method at the binding
cell is 9.62 (9.56 with float32; QF maximum used). The 1 lane vs 1 core window M is **2.71** [HT6].

**Classical confidence (C09)** (meas, q+ because it slows the classical side) [C09]. The symmetric
distribution-free 99% price is now **timed and successful**, not modelled. Both methods use preintegrated samples
with the two-sided empirical-Bernstein bound (Maurer & Pontil, Thm 4; lit) at δ = 0.01, with range R = 17.30. R
comes from the analytic bound sup h ≤ 17.29 on the preintegrated payoff [P1]; v3 assumed $40. n is fixed from an
independent pilot. Each factor is a same-state ratio to practice RQMC.

| Cell | iid EB factor | Replicated-RQMC EB factor (16-point digitally shifted Sobol nets) | Used: minimum over methods | v3 (modelled) |
|---|---:|---:|---:|---:|
| B8x52 $0.001 | 33.8 | **17.3** (17.5 with float32) | **17.3** | 36.9 |
| B4x12 $0.001 | 37.6 | 17.9 | 17.9 | 40.3 |
| B8x52 $0.01 | 16.1 | 83.5 (pilot-dominated) | 16.1 | 18.9 |
| B4x12 $0.01 | 10.3 | 49.3 (pilot-dominated) | 10.3 | 10.6 |

All eight runs met the bound.
- **The minimum over methods is CF**, as T_C is ([SPC] §0.3).
- **Pilot cost.** The replicated-RQMC wall time includes a four-way pilot search (QF; about 9% of points).
- **Thin margin.** Its success margin was thin, 0.34% (q−) [REV].

**Resulting M at the binding cell** (mod) [HT6]:

| Floor | Certified | Canonical explicit | Window certified | Window, quantum-only mean |
|---|---:|---:|---:|---:|
| Box-Muller, symmetric convention | 117.1 | 33.9 | **1.50** | 1.55 |
| All-free, symmetric convention | 5.82 | 1.68 | **0.075** | 0.077 |

**Coverage (C10)** (0). The comparator is the strongest *tested* method; untested challengers can only lower T_C
and raise M.

**Hardware coverage** (unchanged anchors; lit) [HW], [HC] §1-3. The 100 ns layer is faster than every verified
anchor; the best complete readout-to-feedback loop among the sources checked is 550 ns at d = 3.

What the binding cell would need for tenfold with the window constant at the Box-Muller floor (mod, derived)
[HT6]: **≤ 11.9 ns logical layers and ≥ 2.6e13 accepted T/s simultaneously**, at 1e7 logical qubits. The
reaction-bound part (740 layers) and the supply-bound part (2.30e8 T per iterate) must both fit in 8.8 µs per call.

**Necessary-condition columns (H17, H06, H18; debt update, R1 desk)** [H617], [C03L]. Each H17 column holds the other
resource unlimited, so each is a necessary condition only, not a hardware model. Window certified, binding cell:

| Iterate | Window M at primary | Bound by | Reaction time per layer for M ≤ 1 / ≤ 10 | Accepted T/s for M ≤ 1 / ≤ 10 |
|---|---:|---|---:|---:|
| Floor (headline design: 760 layers, 229,603,168 T; mod, q+) | 26.1 | supply | 11.6 ns / 116 ns | 2.61e13 / 2.61e12 |
| Saved A10 source (770,356 T-layers, 4,267,435,214 T; meas) | 8,749 | reaction | 11.4 ps / 114 ps | 4.85e14 / 4.85e13 |

For the quantum-only mean class every limit is about 3.4% tighter.

- **H06 (supply composition).** All of the floor's T comes from AND gates: 57,400,792 per call, or 6.5e12 CCZ
  states per second for M ≤ 1 (mod).
  - **Supply-unit convention as a sensitivity.** With a catalysed CCZ counted as 2 T (Gidney & Fowler 2019; lit), the
    floor window M is **13.0**. The extreme case of one CCZ per supply slot gives 8.63, which is reaction-bound.
  - **Reaction floor.** No supply convention goes below the 740-layer reaction floor, M ≥ 8.40.
  - **All-free column.** It is reaction-bound and stays at 1.29.
  - **Verdict.** A CCZ-native supply convention therefore adds no single-departure flip.
- **H18 (logical failure).** The complete-price ledger allocates the physical-failure share explicitly (§8):
  - 0.0069 for the window class with U1, which needs ≤ 2.98e-16 logical failure per T gate at the floor (2.32e13 T
    per estimate) and ≤ 2.80e-17 per T for the compiled iterate;
  - 0.007 for the quantum-only mean class, which needs ≤ 2.92e-16 and ≤ 2.75e-17.

  These are orders of magnitude below demonstrated logical error rates. They are premises, not certificates.
- **Scope.** TRIG-HWACT has not fired. No layout, routing, factory or decoder model is attached.

---

## 5. The decision table

### 5.1 Primary M

The minimum M over eligible, non-overhead cells; the binding cell is B8x52 at $0.001 in every row. All values mod
[HT6].

| Estimator class | k at the binding cell | **M, primary** | Status of the constant |
|---|---:|---:|---|
| Certified today (E07 schedule) | 682.7 | **2,032** | Certified |
| Canonical explicit (U1 + U2 + non-dyadic M) | 197.6 | 588.1 | Three conditional credits |
| Canonical explicit at failure 0.01 | 144.9 | 431.3 | As above; 11 medians |
| **Window, explicit constant (U1 + U2 + direction-select)** | **8.762** | **26.1** | Explicit worst-case constant, parts 1-4 (this work; AI R2 reviewed) |
| Window, explicit constant, failure 0.01 | 7.359 | 21.9 | As above |
| Window, quantum-only mean (U2 + direction-select) | 9.058 | 27.0 | As above; no classical input |
| Window without direction-select | 17.52 | 52.2 | U1 + U2 |
| Window without U1/U2 (span 64, no mean bound) | 25.80 | 76.8 | Direction-select only |

**Readings of the primary conventions** (window certified, δ = 0.003; mod) [HT6]:

| Reading | M |
|---|---:|
| As quoted (W0 floor, e = 0.45ε) | 26.1 |
| N1 floor alone | 40.9 |
| Strict zero-bias reading of the binding cell (e = ε) | 11.7 |
| Binding cell ineligible (counterfactual since the A2a certificate; B4x12 $0.001 binds; q−) | 36.2 |
| Stage C T_C instead of the C10 comparator (sensitivity, q+) | 10.3 |
| Compiled iterate instead of the floor (floor conventions; q−) [C11C] | 2,290 |

The Stage C row is the window M recomputed with T_C = 22.53 s (26.1 × 8.886 / 22.53; mod, derived).

**Eligibility and independent recompute (debt update; R1)** [A2A], [S44].
- **Eligibility.** The binding cell is eligible on the certified bias, 3.634e-4 ≤ 0.55ε.
- **Scope #44.** The merged headline scope recomputes the binding-cell row in new code from the raw inputs. The scope
  was preregistered in its prospectus before running, and the code does not import the headline script.
- **Agreement.** It matches run006 exactly (relative difference 0) for every column checked:
  - primary 26.08;
  - all-free 1.29;
  - one lane 2.71;
  - symmetric 1.50;
  - all-free + symmetric 0.075.

  It gives 26.96 for the quantum-only mean class.
- **Decision rule.** Its rule, fixed in advance, finds the NO-GO holding under every single departure.
- **Rigour.** The scope is R1. PLAN_110 §4 asks for R2 at a margin below 30×.

The window class stays above 10 under every reading taken one at a time. The canonical explicit class stays above
230 and the certified class above 800; their lowest readings are the Stage C sensitivity, 232 and 801.

### 5.2 One departure at a time

Window certified (δ = 0.003), binding-cell minimum; each row is quantum-favourable unless marked q− [HT6].

| Departure | M | Direction |
|---|---:|---|
| Primary | 26.1 | n/a |
| All-free oracle (free loader and exponential, narrow words) | **1.29** | q+ (oracle idealization) |
| Symmetric distribution-free classical (measured factor 17.3) | **1.50** | q+ (stricter classical standard) |
| 1 lane vs 1 core (H16, measured) | 2.71 | q+ |
| Supply 1e13 T/s | 8.40 | q+ |
| Catalysed-CCZ supply convention (1 CCZ = 2 T; H06) [H617] | 13.0 | q+ (does not flip; reaction floor 8.40) |
| e = ε (strict zero-bias reading) | 11.7 | q+ |
| Distribution-free ×5 (W0's assumed range) | 5.22 | q+ |
| W = 1e8 or unlimited | 21.3 | q+ |
| 10 ns layers (minimum at B4x12) | 22.5 | q+ |
| Estimator failure 0.01 | 21.9 | q+ |
| B8x52 $0.001 ineligible (counterfactual; the cell is now eligible on certified bias) | 36.2 | q− |
| Supply 1e11 / W = 1e6 / 1 µs / 10 µs | 225 / 73.7 / 84.0 / 840 | q− |

For the canonical explicit class the best single departure is all-free at 29.2; for certified today it is 100.9.

### 5.3 Minimal stacked departures to M ≤ 1

| Class | Minimal number | Best sets [HT6] |
|---|---:|---|
| **Window certified** | **2** | all-free + symmetric **0.075**; all-free + 1 lane 0.135; 1 lane + symmetric 0.156 |
| Canonical explicit | 3 | all-free + 1 lane + symmetric 0.175 (best pair: all-free + symmetric 1.68) |
| Certified today | 3 | all-free + 1 lane + symmetric 0.604 (best pair 5.82) |

**Reading.**
- **No single departure reaches M ≤ 1** for any explicit class at δ = 0.003. In v3 the window class did: 0.23 under
  the modelled symmetric convention. The change comes from two measured classical-side results:
  - a faster comparator with the same estimator, T_C ÷ 2.54;
  - a cheaper measured distribution-free method, 17.3× instead of 36.9×.
- **Two departures still suffice for the window class.** One is an oracle idealization (all-free) that no
  construction in this project approaches.

---

## 6. The frontier: what would overturn the result

Each lever is stated with its effect at the binding cell.

1. **An explicit worst-case constant for window/QSP amplitude estimation.** **Met in this version**: c(0.003) =
   4.179, k = 8.762 [P2].
   - **Done at R1 in the debt update:**
     - the U1 and U2 certificates [U1C], [C11C];
     - the compiled step code for direction-select and the controlled powers [C11C];
     - the allocation of the whole failure budget [C03L].
   - **What remains open:**
     - a human check of the derivation;
     - R2 for all of the above.
2. **An oracle below the thresholds of §3.** With the window constant, one controlled Grover iterate at the binding
   cell must take at most **88 reaction layers and 8.8e6 T**.
   - The idealized all-free floor (114) misses by 1.29×.
   - Best loader + free exponential gives 2.45; a free loader alone gives 13.8 [P3].
   - No construction in this project approaches the all-free floor. Its 48-bit words' bias effect is unchecked.
   - The project's compiled iterate has a Toffoli depth of 201,263, against the 88-layer limit (window M 2,290)
     [C11C].
3. **A different comparison convention.** No single convention change reaches M ≤ 1:
   - symmetric distribution-free 1.50;
   - one lane against one core 2.71;
   - supply 1e13 T/s 8.40;
   - catalysed-CCZ supply units 13.0 [H617];
   - e = ε 11.7.

   Paired with the all-free floor, the first two reach 0.075 and 0.135.
4. **A further estimator gain.** k would have to fall from 8.762 to about 0.34 at the current oracle. That is below
   the rigorous counting floor of about 1.85, so this lever **cannot overturn the result alone** in this access
   model.
5. **Control-variate residual or preintegrated oracles (F20/F04).** **Closed by P1** (§7.1).

**What a hardware programme would have to show** (window constant, Box-Muller floor): an 11.9 ns logical layer,
2.6e13 accepted T states per second and 1e7 logical qubits, simultaneously. The best verified complete loop among
the sources checked is 550 ns at d = 3.

---

## 7. Closed escapes, bounded escapes, and escapes outside the claim

### 7.1 Closed for this task

- **F20 and F04: control-variate residual and preintegrated oracles** (probe P1; mod) [P1], [REV].
  - **Closed-form controls cannot cancel the knock-out jump.** The payoff jumps by $38.6 across the arithmetic-basket
    barrier, where every control with a closed-form mean is continuous. So the residual span is ≥ $38.635 of $38.82
    for every β (certified from decimal witness paths): a span gain ≤ 1.005×, or ≤ 1.59× with the U1 mean credit.
  - **Coherent preintegration** encodes a range of [15.61, 17.29], a gain ≤ 2.49× linear or 1.70× with U1.
  - **Clipped/hybrid preintegration** nets at most 3.42 at a cost ratio of 1, or 2.62 at the structure-aware cost
    ratio of 1.30.
  - **Two or three integration directions** net ≤ 0.70.
  - No route reaches the kill threshold of 4. The measured σ reduction from closed-form controls is only 1.02-1.18×.
- **E25: Bayesian or likelihood designs.** Kill rule met: no worst-case coverage theorem in the sources checked;
  the best explicit is AQAE at about 409 [LIT2]. The window estimator supersedes this route.
- **Classical-side negatives (C10):** CV under RQMC, two-direction smoothing, F06 and F07 (§4.3).
- **Certification debts closed at R1 (debt update, 22 October)** [A2A], [U1C], [C11C], [C03L], [S44], [REG9]:
  - **The binding cell's eligibility.** The bias is certified at 3.634e-4 ≤ 0.55ε, so the A02 bridge rerun and the
    A07/A13 re-proofs are not needed.
  - **The complete-price ledger (C03/E07).** The failure budget is fully allocated and the dollar side fits.
  - **U1, U2 and the C11 compile.**

  These are R1 records. R2 is still open (§8).
- **From v3:**
  - E22, log-domain QSP: 0 of 3,106 predicates eligible;
  - C14's "2×" depth reading;
  - latency lines H14, H04 and H07.

### 7.2 Bounded at the primary conventions

- **F05: free coherent loading.** With the window constant a free loader alone gives 13.8, which still meets F05's
  ≥ 10× kill rule. F05 remains a parameter of the joint loader-plus-exponential lever (2.45) [P3].
- **E20: entangled parallel amplitude estimation.** Bounded by the width budget; lane credit 1.00× at the binding
  cell (unchanged).

### 7.3 Outside the claim

- **The σ-normalised estimator line.** Kothari & O'Donnell is σ-normalised and not explicit [LIT2].
- **Parked as a different task.** 25 register items (T6), unchanged from v3.

---

## 8. Limitations and scope

- **Achievability only.** Between the rigorous black-box floor (about 1.85) and the best explicit constant (8.76)
  is a gap of about 4.7×.
- **The oracle floor is modelled, not a lower bound.** As a checkable threshold (§3), a window-class design reaches
  tenfold at the binding cell only if one controlled Grover iterate takes at most 88 reaction layers and 8.8e6 T.
- **Robustness.** The negative is robust to any single favourable departure at the primary conventions. It is
  overturned by two together (closest 0.075).
- **The window constant.**
  - Its derivation has had an AI R2 review only, with no human review [REV].
  - Its U1 and U2 premises are certified at R1 [U1C], [C11C].
    - The U1 certificate assumes iid generator draws and a 1e-9 float slack (assm).
    - U1 can also be replaced entirely at k = 9.058 [SM].
  - The direction-select call cost is exact in this paper's cost model. The step code is compiled and verified, but
    the window state-preparation rotation network is not built: its cost is modelled at 130 T per rotation (lit).
- **Complete-price ledger (C03/E07; R1 desk, exact arithmetic)** [C03L]. Binding cell, union bound over a 0.01
  failure budget:

  | Row | Window class with U1 (k 8.762) | Quantum-only mean class (k 9.058) | Status |
  |---|---:|---:|---|
  | Window estimator (parts 3-4 inside) | 0.003 | 0.003 (1e-4 + 0.0029) | cert |
  | U1 mean certificate | 1e-4 | 0 | cert (R1) / not used |
  | Source and financial-bridge events; certificate acquisition | 0 | 0 | cert by citation: the bridge is a deterministic pay-once bound and the support is all-input |
  | Physical (logical) failure | 0.0069 | 0.007 | **assm: explicit hardware premise** (H18, §4.3) |

  - **Dollar side.** 0.45ε statistical (cert), plus bias 3.634e-4 [A2A], plus readout 2^-39. The sum fits inside ε.
  - **Physical share.** It is a stated premise, not a certificate. No software certificate can discharge it.
- **The binding cell's eligibility** is no longer a debt: the bias is certified at R1 [A2A]. The ineligible reading
  (B4x12 $0.001 binds, window M 36.2, q−) is kept as a counterfactual.
- **The headline floor against the compiled circuit.** The compiled iterate gives window M 2,290 at floor
  conventions [C11C]. So the floor is quantum-favourable by about 88× against what this project has built.
- **Provenance note on the compile.** One repository helper's lookup-key check fails in this checkout. It affects
  no count, and the widths were read from the hash-checked schedule. It must be rechecked before any R2 run
  [C11C].
- **Machine state and timing conventions.**
  - The classical times are 1 October Stage C times divided by 22 October same-state speedups, at the QF end of
    their measured range. Multiplying the fast and float32 ratios is assm.
  - Absolute 22 October times are CF: the Best-performance overlay ran the unchanged harness 2.2× faster.
  - With the Stage C time, window M is 10.3 (q+ sensitivity).
  - A 20-replication rerun under the 1 October machine state would remove the ratio assumption.
- **The distribution-free factor** is the minimum of two timed methods.
  - The replicated-RQMC run passed its bound by 0.34%.
  - A better distribution-free bound (for example betting confidence sequences) could lower the factor further,
    which would raise M (q−).
- **Rigour level.**
  - The headline is R1 for the certified-today and canonical classes, whose margins are ≥ 260×.
  - The window class sits at 26×. Its headline row has an independent R1 recompute [S44], and its debts are closed
    at R1.
  - PLAN_110 §4 requires R2 below 30×. **R2 is open.** It needs:
    1. human peer review of P2_DERIVATION.md, A2a proof steps 2 and 4, the U1 premises, and the C11 provenance note;
    2. preregistration, a sealed run with a saved verifier and a receipt for scope #44 (writing under `.context/` is
       reserved for the user).
- **Further quantum-favourable conventions** (unchanged):
  - the classical 0.45ε share has no bias reserve;
  - factories are outside W;
  - latency counts Grover iterates only;
  - the all-free floor's 48-bit word bias is unchecked.
- **Literature.** Not every citation was re-fetched in this round. The 2026 hardware anchors rest on the
  hwclassical fetch log.
- **Scope.** One contract (two cases), one construction family, one access model.

---

## 9. Discrepancies

### 9.1 v3 → v4 (the v4 value is used)

1. **Classical comparator.** Stage C 22.53 s against **8.89 s**: the same estimator with faster arithmetic, QF end
   of the speedups [C10].
2. **Symmetric factor.** 36.9× (modelled from an iid route with R = $40) against **17.3×** (measured, minimum over
   methods, R = 17.30) [C09].
3. **Window constant.** WS-k's DPSS c(0.003) = 4.168 (uncertified numerics) against the certified Kaiser **4.179**
   (+0.3%) [P2].
4. **Number of departures.** v3: one departure suffices (symmetric 0.23 for the window class). v4: two are needed
   (§5.3).
5. **F20/F04.** v3: open lever. v4: closed (P1).
6. **E25.** v3: credited lever. v4: closed by its kill rule [LIT2].
7. **One-core ratio.** H16 run001 10.24 (Stage C) against 9.62 (fast method, same state) [H16F].

Items 1-15 of v3 §9 (N1 against W0, between N1 workstreams) are unchanged and not repeated here.

### 9.2 Within v4: the debt update of 22 October (the new value is used)

1. **Binding-cell bias.** Modelled clamp-tightening $0.000473 [BD] against **$0.0003634**, certified at R1 with the
   source unchanged [A2A]. The certified run002 bridge value was $0.0012396.
2. **H18.** The earlier desk range (≤ 4.3e-17 to 2.6e-16 per T for a share of 0.001-0.006) is replaced by the
   allocated shares 0.0069 / 0.007:
   - ≤ 2.98e-16 / 2.92e-16 per T at the floor;
   - ≤ 2.80e-17 / 2.75e-17 per T for the compiled iterate [C03L].
3. **U1 premise.** P2's assumed m = 3.32682 (uncertified) against the certified m = 3.28804 [U1C]. k is kept at
   8.762.
4. **Compiled iterate against the floor.** The floor's 2.30e8 T per iterate against 4,267,659,718 T compiled, which
   is 18.6× literal and 10.6× at 4 T per Toffoli [C11C].

---

## Appendix A. The 110-item register

The current register is [results/plan110_w0/register/run009/REGISTER.md](../../results/plan110_w0/register/run009/REGISTER.md)
[REG9]. It is run001 plus eight runs of explicit deltas, each with a CHANGES.md.

**run009 (the debt update).** It updates 13 rows: C02, A02, A07, A13, C03, E07, C11, E03, E11, E23, H06, H17 and H18.
- C03 and E07 are marked complete at R1.
- C11 is marked compiled at R1.
- H06, H17 and H18 are marked desk done.

Tiers are unchanged from run008, because each item still needs R2 before publication.

| Tier | Meaning | Count, run001 | Count, run009 |
|---|---|---:|---:|
| T1 | Decision-critical, done | 4 | 4 |
| T2 | Credited levers | 8 | 6 |
| T3 | Deferred certification debts (now done at R1, R2 open) | 12 | 11 |
| T4 | Closed or folded | 26 | 31 |
| T5 | Dormant with triggers | 35 | 33 |
| T6 | Parked as a different task | 25 | 25 |

How the register maps onto this draft:
- **§4.1:** A01 and its parameter items.
- **§2:** C02 and A02/A07/A13, through the A2a bias certificate.
- **§4.1:** C11, the compiled iterate.
- **§4.2:** E01, C11 (bracket 1.85-8.76), E03 (U1/U2 certified at R1), E04, E08 and E20.
- **§4.3:** H01, H02, H06, H14, H16, H17, H18, C09 (measured), C10 (closed: complete for applicable challengers).
- **§3:** F31 and C14.
- **§7.1:** F20, F04, E25, F06, F07, E22, C12 and C14; the C03/E07/C11/eligibility debts at R1.
- **§7.2:** F05 and E20.
- **§8:** C03, E07, E23 and H18.

## Appendix B. Reproduction

Steps 1-8 of v3 Appendix B are unchanged. New in v4:
- **Probe.** `research/frontier_probe_20261021/p1_control_span.py`, `p1b_hybrid.py`, `p2_window_constant.py`,
  `p2b_parts34.py`, `p2c_self_mean.py` and `p3_oracle_desk.py run006`.
- **C10.** `research/c10_challengers_20261022/selfcheck.py`, `run_timing.py`, `run_timing_f32.py`, `f32_check.py`,
  `rate_cv.py`, `rate_smooth2.py` and `f06_f07_screen.py`. These use the Stage C harness without `-I`.
- **C09 and H16.** `c09_g4.py`, `c09b_rep.py`, `f32_consistency.py` and `h16_fast.py`.
- **Headline.** `build_overrides_run006.py`, then
  `research/frontier_probe_20261021/headline_m_probe.py run006 results/c10_challengers_20261022/overrides_run006.json`.
- **Register.** `research/frontier_probe_20261021/register_run002.py`, then
  `research/c10_challengers_20261022/register_run003.py` … `register_run008.py`.
- **Number check.** `research/frontier_probe_20261021/v4_check.py`.
- **Debt update (22 October).** All in `research/claim_debts_20261022/`:
  - `a2a/clip_split_certificate.py`, `a2a/independent_recompute.py`, `a2a/summarize.py`;
  - `u1/eb_sample.py` (Stage C environment without `-I`), `u1/u1_certificate.py`, `u1/u1_independent.py`;
  - `c11/u2_wrapper.py`, `c11/iterate_compile.py`, `c11/recount_independent.py`, `c11/estimator_compile.py`,
    `c11/summary.py`;
  - `c03/c03_allocation.py run001` (with the A2a, C11 and U1 summaries as arguments);
  - `h06_h17/h06_h17_desk.py run004`;
  - `scope44/scope44_recompute.py run001`;
  - `register_run009.py`;
  - the number check `v4_check_debts.py`.

Every output records the SHA-256 of its inputs and is created with exclusive create.

---

## Changelog v3 → v4

Items are those of `docs/frontier_probe_20261021/V3_EDITS_CURRENT.md`.

| Edit | Applied in v4 |
|---|---|
| 1. Abstract M table with current numbers; window row as the explicit constant; certified today 2,032 (run006) | Abstract table; §5.1 |
| 2. Comparator: same estimator, faster arithmetic; T_C 8.89 s (run006); Stage C as sensitivity | Abstract; §1 scope item 3; §2 T_C table; §4.3; §5.1 readings; §8 |
| 3. Checkable threshold 88 layers and 8.8e6 T (run006); all-free floor misses | Abstract; §1 item 1; §3 item 3; §6 lever 2; §8 |
| 4. Robustness wording: robust to any single departure; two overturn | Abstract; §5.3 reading; §8 |
| 5. §4.2: P2 certificate, quantum-only mean, literature rows | §4.2 |
| 6. §4.3 C09 measured factors (iid and replicated RQMC), R = 17.30 | §4.3 C09 table; Abstract |
| 7. §4.3 H16 fast ratio | §4.3 |
| 8. §4.3 C10 tried, adopted, killed, untried | §4.3; §7.1 |
| 9. Achievability gap about 4.7× | Abstract; §4.2; §8 |
| 10. §5.1-5.3 tables and reading | §5 |
| 11. §6 levers 1 (met), 2, 3, 5 (closed) | §6 |
| 12. §7.1 closed escapes | §7.1 |
| 13. §8 C03 ledger, H18, machine-state caveat | §8 |
| 14. §8 rigour | §8 |
| 15. §9 discrepancies | §9.1 |

Numbers moved after V3_EDITS_CURRENT.md was written. The float32-GEMM challenger (headline run006) changed several
of them, so v4 uses run006 throughout:

| Quantity | V3_EDITS_CURRENT (run005) | v4 (run006) |
|---|---:|---:|
| Window M | 21.4 | 26.1 |
| All-free | 1.06 | 1.29 |
| Symmetric | 1.23 | 1.50 |
| One lane vs one core | 2.22 | 2.71 |
| T_C | 10.84 s | 8.89 s |
| Window threshold | 107 layers | 88 layers |

Consequential edits: the title-line status block; new source keys; Appendix A tier counts from register run008;
Appendix B new steps.

### v4 → v4 (debt update, 22 October)

The user authorized every claim-grade debt on 22 October 2026. Each result below is R1. This update changes no
headline M.

| Change | Where |
|---|---|
| Status block: debts done at R1; the R2 items still needed; P2 still AI-reviewed only | Title-line status block |
| Source keys [A2A], [U1C], [C11C], [C03L], [H617], [S44], [REG9]; the debt checker | Source table; Provenance |
| Binding cell eligible on a certified bias of 3.634e-4 (was the modelled clamp tightening) | Abstract; §2 conventions table and A2a paragraph; §5.1; §5.2; §7.1; §8; §9.2 |
| Compiled iterate against the floor (window M 2,290 at floor conventions; 8,828 literal; ≥ 277 in every reading) | Abstract; §4.1; §5.1 readings; §6 lever 2; §8; §9.2 |
| U1 and U2 certified at R1 | Abstract; §4.2; §6 lever 1; §8 |
| H06/H17/H18 necessary-condition columns; catalysed-CCZ sensitivity of 13.0 (no flip) | §4.3; §5.2; §6 lever 3; §9.2 |
| C03/E07 complete-price ledger, with the physical share as an explicit premise | §6 lever 1; §7.1; §8 |
| Scope #44 independent recompute matches run006 exactly | Abstract; §5.1; §8 rigour |
| Register run009 (13 rows; tiers unchanged) | Appendix A |
| Debt-update scripts | Appendix B |
