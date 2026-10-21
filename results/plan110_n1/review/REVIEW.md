# N2 adversarial review of FRONTIER_NEGATIVE_RESULT_DRAFT.md

12 October 2026. Reviewer: N2-reviewer (plan110 branch N, wave 2). I did not write the draft.

**What was reviewed.** `manuscript/advantage-frontier-2026-09-23/FRONTIER_NEGATIVE_RESULT_DRAFT.md`, sha256 `3d8e5900…c62b1c`. This is the same hash the drafter recorded, so the file has not changed since it was written. I checked it against the N1 results in `results/plan110_n1/{headline,estimator,hwclassical,drafter}/` and the W0 results in `results/plan110_w0/`. The conventions are the ones in `research/plan110_w0/W0_CARD.md`, and the claim wording is the one in `research/plan110_n1/N1_CARD.md`.

**Method.**
1. **Number check.** `research/plan110_n1/review/check_draft.py` (stdlib, run with `-I -S -B`) wrote `number_check.json`. It holds 78 programmatic checks: every quoted number I could map to a file value, with tolerance set by the precision the draft prints, plus a test that each quoted snippet appears verbatim in the draft.
   - **74 checks pass.** 3 are small range mismatches (defect 13). 1 is a register-disposition contradiction (defect 7).
   - The input SHA-256s of `headline_table.json`, `estimator_recompute.json`, `hw_classical_card_v2.json`, `keff.json` and `floor_sheet.json` match the hashes the drafter recorded.
2. **Cross-product check.** `research/plan110_n1/review/confirm_dirsel.py` wrote `dirsel_confirm.json`. It recomputes the drafter's direction-select cross-products per cell, over every eligible non-overhead cell, along a different path from `draft_addendum.py`.
   - **They are confirmed.** The values 0.9718, 0.2696 and 0.5392 match to 1e-15. The binding cell stays B8x52 $0.001.
   - This answers the request in draft §9.2 item 13. It is derived arithmetic, not a headline rerun, so that item should say "confirmed by derived arithmetic".
3. **Reading.** The cards, the receipt, `register.json`, the W0 bias desk (`ws_small/README.md`) and the Stage C spec (`ANALYSIS_SPEC_STAGE_C.md` §0.4-0.5).

**Labels.** Every number in this review keeps its source label: meas (measured), mod (modelled), assm (assumed) or lit (literature). It also carries a direction: q+ (quantum-favourable), q− (against quantum) or 0 (neutral). Numbers I derived are "mod, derived" and are recorded in `number_check.json` → `derived_for_review` and in `dirsel_confirm.json`.

## Bottom line

**The claim survives.** Under the primary conventions (mod), every reading I could construct leaves the certified-constant class at M ≥ 400.7 and the explicit class at M ≥ 104.4. Both are above the 30× threshold that justifies R1.

**The text overclaims in five places:**
- what the R1 recompute confirmed;
- "no design";
- the zero-bias treatment;
- the abstract's silence about the classical confidence asymmetry;
- the closed-escapes list.

**It also understates one fragility.** With the direction-select credit, whose call-cost condition is already satisfied inside the draft's own cost model, the *certified-constant* class reaches M = 0.54 with one oracle idealization plus the symmetric classical convention.

**There are no blockers.** There are 7 major defects and 14 minor ones.

---

## Defects

### Major

**1. (major) "Two R1 recomputes along different paths confirm them" overstates what was confirmed.** Abstract; also §5.1 "Verdict at R1".
- **What was confirmed.** N1 reproduced k, T_C, σ/e and the M arithmetic exactly (mod; HT `compare_W0` rel_diff ≤ 2e-16).
- **What was not.** It did not reproduce the oracle term D_eff:
  - N1's independent floor is 1.547× (B4x12) and 1.570× (B8x52) *less* favourable at the primary conventions (mod, HT `D_eff_table`).
  - The two floors disagree by more than 10% in 165 of 180 pairs.
  - The quoted 801.5 / 232.0 / 8.62 use W0's floor, which is rigour R0.
  - N1's own floor gives 1,258 / 364.2 / 13.5 (mod).
- **What R1 actually establishes** is that both independent constructions give M ≫ 30 (q− for the floor choice is excluded by taking the minimum). That supports the verdict, not the quoted values.
- **Fix.** Replace the sentence with: "N1 recomputed the estimator constants, classical times and M arithmetic exactly. The oracle term is the smaller of two independent idealized floors, W0's (R0) and N1's (R1), which differ by about 1.55×. With N1's floor alone, M is 1,258 / 364 / 13.5."
- Make the same change in §5.1 and §8 "Rigour level".

**2. (major) "No design" rests on a modelled floor that is not a lower bound on the oracle.** §1 scope item 1, §3, §8.
- **The gap.** Scope item 1 covers *every* coherent fixed-point oracle in the family. The evidence covers oracles that cost at least the idealized floor, which is a specific construction: Box-Muller, Chebyshev/Estrin, Kogge-Stone (mod, q+). §8 concedes that "neither is a tight bound", but nowhere states what an oracle would have to achieve to overturn the result.
- **The thresholds.** At the binding cell under the primary conventions (mod, derived):

  | Class | Max D_eff for M ≤ 1 | Max T per iterate (1e12 T/s, 100 ns) |
  |---|---:|---:|
  | Explicit | 9.90 reaction layers | 9.9e5 |
  | Certified | 2.86 layers | 2.9e5 |

  The idealized all-free floor, with a free loader and a free exponential, is 114 layers (mod, q+, W0). It would have to be beaten by a further 11.5×.
- **Fix.** Add one sentence to §3 or §8 giving these two thresholds. Reword the scope as "no design in this family whose Grover iterate costs more than about 10 reaction layers and 1e6 T (explicit) or 3 layers and 3e5 T (certified)". That turns "no design" from an implicit universal into an explicit, checkable statement.

**3. (major) The B8x52 $0.001 "zero deterministic bias" treatment is internally inconsistent, and the margin depends on which reading is taken.** §2 conventions table, abstract ("most quantum-favourable eligible cell"), §5.2.
- **What the files say.**
  - The W0 bias desk (`ws_small/README.md` A1) admits the cell by lowering the stock clamp 3 binades. That gives bias $0.000473 = 0.47ε (mod, q+). It is **uncertified**, and needs the A02 bridge rerun plus the A07/A13 re-proofs.
  - The table then uses e = 0.45ε at that cell. σ/e = 11,518.7 = 5.18340/(0.45 × 0.001) (mod), which reserves 0.55ε for a nonzero bias.
- **Why it matters.**
  - "Eligible at zero deterministic bias" is therefore not what is computed.
  - If the bias really were treated as zero, the consistent split is e = ε. The primary binding-cell M would then be **104.4** (explicit) and **400.7** (certified) (mod, HT `e_eq_eps`), not 232 / 801.5.
  - The pair "all-free + 1 lane vs 1 core" would reach **0.506** (mod). Under that reading, two departures suffice even with W0's C09 range.
- **Fix.**
  - State that the cell is admitted on a modelled, uncertified clamp tightening (bias 0.47ε ≤ 0.55ε), and that the primary therefore keeps e = 0.45ε.
  - Report the strict zero-bias reading as its own line: 104.4 / 400.7, and pair 0.506.
  - Add to §8 that the binding cell's eligibility is itself a re-certification debt. If it is ineligible, M is 318.0 (explicit) at B4x12 (mod, q−). This is already in §5.2.

**4. (major) The abstract hides the largest convention asymmetry, which is classical practice confidence intervals against quantum worst-case 99%.**
- **The problem.** The abstract says both sides price "at 99% confidence". The quantum k is a worst-case 99% guarantee (mod). The classical T_C uses Student-t practice CIs from 16 RQMC scrambles (meas), which are not a guaranteed 99%.
- **The size.** The symmetric distribution-free convention slows the classical side 36.9× at the binding cell (mod from meas inputs, q+). That is larger than any other single convention lever in the paper.
- **The labelling.** The draft calls this column a "favourable departure" and, in the abstract, an "idealized change". It is the *stricter* classical standard, and it was the user's chosen primary that departs from symmetry.
- **The composition.** The 36.9× is mostly the loss of RQMC's rate (about 30×). The empirical-Bernstein tail adds about 1.9× over a CLT iid run (mod, derived: CLT n 4.30e7 vs EB n 8.02e7 vs RQMC 1.43e6 points).
- **Fix.**
  - In the abstract, say "classical: practice confidence intervals (Stage C); quantum: worst-case 99%", and give M = 6.29 (explicit) and 21.7 (certified) under the symmetric convention next to 232 / 801.5.
  - In §4.3, add the one-line decomposition above.

**5. (major) The abstract's fragility sentence contradicts its own bullets.**
- **The contradiction.** "One idealized change on each side … is enough to reach tenfold" is followed by M = 1.125 for all-free + 1 lane vs 1 core, which is not ≤ 1. Only all-free + distribution-free (0.31, mod) reaches it, and that pair contains the symmetric convention (defect 4), not an idealization.
- **Fix.** "One oracle idealization (the all-free floor) plus the symmetric distribution-free classical convention gives M = 0.31. One oracle idealization plus one lane against one core gives 1.125, or 0.97 with the conditional direction-select credit."

**6. (major) The direction-select credit is described as "assumed", but the draft's own cost model already meets its condition. The certified-constant class then fails under one idealization plus the symmetric convention.** §4.2, §5.3, §8.
- **The condition is already met.**
  - The estimator card says the one missing certificate is that a direction-select iterate costs no more than one controlled Grover iterate, and that this "holds when only the reflections are controlled".
  - The N1 floor sheet already assumes "Only the reflections are controlled" (draft §4.1).
  - I checked the identity: Q^(j−c) multiplies each eigen-branch by a global phase, and the branches are orthogonal on the unmeasured register. That leaves the readout distribution unchanged and the cost at M/2 per shot. The identity is correct.
- **What follows.**
  - Within the paper's cost model, certified-schedule M is **400.7** (mod), not 801.5.
  - Certified + all-free + Stage-C distribution-free gives **0.539** (mod, derived; confirmed per cell in `dirsel_confirm.json`).
  - Without direction-select it is **1.078**, only 8% above 1.
- **Consequence.** The claim's own class, certified constants, is only robust at the primary conventions. That is fine for the claim as worded, but the abstract and §8 should say so.
- **Fix.**
  - Report the certified class as 400.7-801.5 (primary).
  - Report 0.54-1.08 with all-free + symmetric classical.
  - Change "assumed" to "satisfied in the paper's cost model; not yet certified for a compiled circuit".

**7. (major) The "Closed escapes" section contradicts the register and leaves the F20/F04 escape open.** §7 and Appendix A; number-check id `closed_escapes_dispositions`.
- **The register contradiction.**
  - F05 and F20 are **T2, "credited screen value / branch-A lever"** in `register.json`, not closed. Appendix A still lists them under "§7 (closed escapes)" and says "this draft changes none of [the dispositions]".
  - F04 is T4 but "closes on the F20 zero-depth credit". That is exactly the credit run002 removed, so F04's stated closure basis no longer exists.
- **The argument has a gap.** It treats a control/residual only as a σ reduction. A residual oracle (payoff − control with a classically known mean) also changes the **span** S, and bounded AE's k *is* span-normalised. A smaller residual range would lower the call count directly. Neither N1 nor W0 measured the residual span.
- **The literature line is unverified.** "No explicit-constant source supplies a σ-normalised estimator" has not been checked:
  - WS-k listed only Kothari & O'Donnell (arXiv:2208.07544), and the N1 card marks it "not verified (not needed)";
  - Montanaro (2015) and Hamoudi (2021) variance-aware estimators were not checked.
- **Fix.**
  - Move F05 to "bounded by the all-free floor (M = 11.5)". F05's own kill rule, "close if ≥10× miss remains", is met. Say the register disposition is updated here, or keep it T2.
  - Move F20 and F04 to a separate list, "outside the claim (white-box residual oracles), not closed".
  - State that residual-span reduction is not costed.
  - Soften the σ-normalised sentence to "in the sources checked (Kothari & O'Donnell, not re-fetched)".
  - Change "changes none of them" to list these exceptions.

### Minor

**8. (minor) The uncertified orientation price is not carried into the symmetric-rigour sensitivity or into §8.**
- **The problem.** The explicit k uses the U1 mean bound m ≤ price + L1. The price is an uncertified classical RQMC value (assm), and the B8 L1 is borrowed from B4x12. Under a symmetric distribution-free convention, the quantum side should not lean on an uncertified classical estimate. There is also a circularity: the quantum run consumes a classical price.
- **The effect.** Without U1, the binding-cell k is 353.0, so M_distfree is **11.2** (Box-Muller) and **0.56** (all-free) (mod, derived). The conclusion does not change: two departures still suffice.
- **Fix.** Add this line to §4.3 and add the orientation price explicitly to §8.

**9. (minor) Undisclosed q+ conventions, each of which strengthens the negative.** List these in §2 or §8:
- the classical side is also held to 0.45ε, although it carries no 0.55ε deterministic-bias reserve (Stage C spec §0.4-0.5 labels this QF);
- the magic-state factory footprint is outside W, which W0_CARD defines as "logical *data* qubits", while the draft's table says "1e7 logical qubits";
- the quantum latency counts only Grover iterates, not readout, reset, the inverse QFT, decoder tail or classical post-processing (the draft says "complete latency");
- the bias effect of the all-free floor's 48-bit words was not checked.

**10. (minor) An undisclosed q− choice is labelled neutral.**
- **The choice.** T_C is the minimum over noisy C2/C5 candidates. Stage C spec §0.5 labels "the minimum over noisy candidates" CF. The binding-cell T_C of 22.53 s (meas) is also below the H16 rerun's 23.46 s (meas), about 4%.
- **The draft's label.** It marks T_C "meas, 0".
- **Fix.** Use "meas, q− (min over candidates)". The effect on M is ≤ 4%.

**11. (minor) "74.8 is layer time" mislabels the factor.** §3 item 2.
- **Why.** 74.8 is M at the 740-layer reaction depth, which equals the M at 1e13 T/s (mod). It is the product of every non-supply term. "Equivalently, a 1.34 ns layer" is one reading of it. Calling it "layer time" sits awkwardly next to "faster layers alone do not help".
- **Fix.** "At unlimited supply M would be 74.8; reaching tenfold then needs 1.34 ns layers, and at 1e12 T/s supply adds a further 3.10."

**12. (minor) The abstract's window row mixes failure allocations.** 8.62 uses estimator failure 0.01, while 801.5 and 232.0 use 0.003. §3 and §9 disclose this, but the abstract does not.
- **Fix.** Show "8.62 (failure 0.01) / 10.26 (0.003, like for like)".

**13. (minor) Small number mismatches.** These come from `number_check.json`. All are modelled.
- **Window k ranges (§4.2 table).** "8.25-8.74" and "6.93-7.34" are the values at ε = $0.001 for B4x12 and B8x52. The ranges over all ε are **8.25-8.77** and **6.93-7.37**.
  - Fix: either label them "B4x12 / B8x52 at $0.001" or use the full ranges. The card's §6 already says 8.25-8.77.
- **Mean-bounded counting bound.** "0.15-0.16" should be **0.14-0.16** at δ = 0.01. The card notes the lowest value in any cell or access model is 0.074.
- **Counting bound for B4x12.** "1.687-1.696" spans both splits; at the primary split it is 1.691-1.696. B8x52 likewise: 1.848-1.853 at the primary split.
  - Fix: say "over both splits" or quote the primary-split values.
- **Window constant (§4.2).** "N1 confirmed it to 1e-12 by power iteration" holds at N = 100 and 200 only. The constants actually used, c = 4.168 and 3.502, are WS-k's N = 400 values, which N1 did not recompute. They are also extrapolated from N ≤ 400 to N ≈ 1e3-3e5.
  - Fix: say so in one clause.

**14. (minor) The provenance statement is too broad.**
- **The problem.** "All scripts whose numbers appear here ran under … -I -S -B (stdlib only)" is false for the measured T_C and H16 numbers. Those come from the Stage C C2 harness and `h16_worker_grid.py`, which use numpy and numba without `-I` (W0_CARD, ws_small README).
- **Fix.** "All N1 and drafter scripts …; the measured classical timings come from the Stage C / H16 harness in the same environment, with numpy and numba."

**15. (minor) [DN] has a known defective field that is not disclosed.**
- **The problem.** `draft_numbers.json` → `certified_k_range_0.45eps` reads [532.5, 1066.7]. The drafter's correction row gives 585.8-1,066.7. The draft cites [DN] generally.
- **Fix.** Add one line to Appendix B pointing to the correction row in `results/plan110_n1/drafter/rows.jsonl`.

**16. (minor) Some literature has not been re-verified, and one claim needs qualifying.**
- **Floor-sheet citations.** These were not fetched in N1: Jones, PRA 87, 022328 (2013); Gidney, Quantum 2, 74 (2018); Fowler, arXiv:1210.4626; Babbush et al., PRX 8, 041015 (2018).
  - Their bibliographic details match the reviewer's knowledge, and the uses (4-T AND, free Cliffords, QROM) are standard.
  - Mark them "lit, not re-fetched in N1".
- **Maurer & Pontil (2009) Thm 4** is likewise not re-fetched.
- **The 2026 anchors.** arXiv:2603.16203, 2605.04892 and 2510.26078 are beyond the reviewer's independent knowledge and rely on the hwclassical fetch log alone.
- **One overclaim.** "Yang … the only demonstrated complete readout-to-feedback loop" should be qualified "among the sources checked".

**17. (minor) The 1-lane departure needs a direction note.** It applies the measured H16 ratio (meas) to the Stage C T_C. The H16 grid timed only `preint`, while the decision T_C may come from C5 methods in other cells.
- In the decision cells T_C is `preint` (HT `T_C` → `raw_best`), so the result is unaffected. Say so in §4.3.

**18. (minor) §4.2 "Only one primary floor design fits" is confusing.** The B4x12 lane credit of 1.29× uses 3 lanes of the *W = 1e6* design.
- **Fix.** "Only one lane of the primary-width design fits; the B4x12 credit uses three lanes of the narrower W = 1e6 design."

**19. (minor) §1 says "This draft closes the last open contract".**
- **The problem.** WHY_NO_ADVANTAGE.md already treats the knock-out basket as Failure 6.
- **Fix.** "This draft turns the sixth construction (the knock-out basket that Stage C measured) into a scoped frontier statement."

**20. (minor) A discrepancy against W0 is not listed.** DP1 gives the loader as 36-56% of the floor. N1's Box-Muller share of the compute path is 52-53% (mod; receipt). The draft quotes the N1 value without listing the difference.
- **Fix.** Add it to §9.1.

**21. (minor) The claim sentence appears without its scope.**
- **The problem.** The verbatim N1 wording must stay. But in the abstract it stands alone, and "certified constants" can be read as covering the oracle. Only the *estimator* constant is certified; oracle costs are modelled.
- **Fix.** Directly after the claim line, add: "Scope: this construction family (coherent fixed-point oracle plus bounded amplitude estimation), the fixed task, and the strongest tested classical method. 'Certified constants' refers to the estimator constant; oracle costs are modelled idealized floors."

---

## Checks that passed (not defects)

- **Headline values.** 801.5, 232.0, 8.62 and 10.26, and k at the binding cell (682.7 / 197.6 / 7.34 / 8.74).
- **The gap ledger.** σ/e 11,518.7, D_max 1,955.9, k_10x 0.852, D_eff 2,296 / 3,605, and the split 74.8 × 3.10.
- **The 10 ns columns.** B8x52 stays at 232.0; the B4x12 minimum is 197.8.
- **The floor table.** 270/278 layers, 2.26e7/1.87e8 T, 53%/52%, 563, 1,409 and 3.61e8, 585, 1.88e8, 1,875 and 5.03e7, and 59/67.
- **The floor comparison.** 165/180 and 33 pairs, and the ratio 1.55-1.57.
- **Estimator values:**
  - E07: 983,025 calls;
  - certified k 585.8-1,066.7;
  - explicit k 186.6-198.2, 323-353 and 195-341;
  - direction-select: 293-533, 491,520 calls, 98-171, 400.7 and 200.4;
  - Patel 6.8e5-9.3e5 and Grinko 2,997-5,755 (the latter is a WS-k file value quoted through the card);
  - lanes: 1.00 / 1.29 / 3.36, and widths 5.28M / 10M.
- **H16.** The ratios, efficiency 0.40-0.64, Stage C reproduction 3.8-10.1%, and 22.7.
- **C09.** Factors 40.3 / 36.9 / 10.6 / 18.9, σ_preint, per-point costs, and M_distfree 21.7 / 6.29 / 1.08 / 0.31.
- **Hardware.** The anchor values and ratios, and the necessary-condition table (0.39 ns, 1.1e15; 36 ns, 1.2e13; 8.8 ns, 1.3e13, 1.85e6; 326×).
- **The §5.2 departure table and the §5.3 stacked sets.** 0.225 / 0.506 / 0.714 / 0.825, 1.125, 0.777, 3.89, and 0.97 / 0.27 / 0.54.
- **Register.** The tiers (4/8/12/26/35/25), the T6 list, and E22's 0 of 3,106.
- **§9 items.** The quirk (0.12677 vs 0.12440) and W = 1e6 (11,034; 3.4e6 persistent qubits).
- **The claim wording** is verbatim from the N1 card.
- **The C10 monotonicity argument and the "conditional credits make the negative more conservative" argument** are both correct.

## Recommendation

**Needs another round.** The revision is text only and needs no new computation. Then a short re-check against this list.

The claim, "no design with certified constants reaches 10× under the stated conventions", is supported at R1 by a wide margin: certified ≥ 400.7, explicit ≥ 104.4 under every reading of the primary conventions (mod). Defects 1-7 change what the abstract and §5/§7/§8 say about rigour, scope and fragility, and the user should see that revised framing before signing off. The numbers the fixes need are already in `number_check.json` (`derived_for_review`) and `dirsel_confirm.json`.

The optional extra analysis is a residual-span measurement for F20/F04 (defect 7). Without it, that escape should be stated as outside the claim, not closed.
