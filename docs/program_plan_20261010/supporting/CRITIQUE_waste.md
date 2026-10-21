# CRITIQUE_waste: remaining waste in PLAN_110.md

Reviewer label: waste_critic. Scope: whether each scheduled item can change DP1 or the final result; rigour applied where a cheaper screen decides; serial steps that could run in parallel; repeated work; missing batching; padded estimates. Nothing was executed. The only things run were read-only checks on the plan and the triage rows (`scratchpad/plan110/_waste_check.py`).

## 0. Programmatic ID check (passed, with two consistency defects)

`python -I _waste_check.py .` against `rows_{A,C,E,F,H}.jsonl` and `PLAN_110.md`:

- Triage rows: 110 IDs, 110 unique.
- Appendix A: 110 rows, 110 unique, **0 missing, 0 extra, 0 duplicated**. The tier counts are T1 6 / T2 8 / T3 12 / T4 25 / T5 34 / T6 25.
- §3 tier member lists: 110 IDs after range expansion, no duplicates. Each tier's list matches the Appendix A tiers exactly.
- **Defect 1.** The "Content (41 items)" list in §4.4 contains **40** distinct IDs. It reaches 41 only if the conditional C08 is counted, so the §0 split of 66/41/3 depends on how C08 is counted. The plan should state that.
- **Defect 2.** H04 and H07 are scheduled in W0-WS4 ("zero-cost lines"), but Appendix A gives their wave as `TRIG-HWACT` only, and they are missing from the branch-N content list. Pick one of the two. Fix 6 below proposes register-only.
- The W0 workstreams hold 38 distinct items. Four branch-N items have no W0 slot (C09, C10, C12, E22), which is fine.

## 1. Main finding: DP1 depends on one product, and most of W0 does not feed it

The plan's own rule (§4.3) is M_DP1 = D_floor x 10 x k_lo x (sigma/e at e = eps) x 100 ns / T_C_env. Only **k_lo** and **D_floor** in it are unknown. Everything else is already in `gap_ledger.json`. Using the ledger's sigma/e and T_C, GO or GREY needs roughly

    k_lo x D_floor <= ~3.2e3 (B8x52 $0.03, best non-overhead eligible cell); <= ~1.1e3 (B8x52 $0.01); <= ~4.7e2 (B4x12 $0.001)

with GREY allowed up to 3 times these values. So DP1 is a **threshold test on one product**. It does not need a full decision table.

The following W0 outputs **do not enter M_DP1**:
- E02 k_eff table (DP1 uses k_lo, not k_eff);
- the H03 full-source recount (DP1 uses D_floor, not the current source depth);
- H01/H02/C15/H14/H04/H07/H17 (t_layer is fixed at 100 ns by fiat);
- C02 (the plan says either convention is safe for the negative);
- C04, C05, C13, F02, F04, F08, E08, E20 (each is < 1.1x, already computed in the rows, or not part of the formula);
- the P/O/I columns (already in §2.1-2.2);
- the F01 eps* crossover.

They are needed only for the branch-N manuscript, and N1 recomputes or recertifies every one of them. Running them in W0 means doing the same work twice.

## 2. Numbered fixes (item-specific)

1. **Shrink W0 to 2 agent workstreams plus one orchestrator script (saves about 2 agent workstreams in W0 and removes double work in N1).** WS3-core: E01 k_lo + C11 bracket. WS2: the A01 floor. Replace WS1 with an orchestrator-run extension of `gap_calc.py` (no agent). It adds four columns: the e = eps column (E24), marginal-compute T_C for overhead cells (F01/C09, from existing C5 data: 0.18 s for B8x52 $0.10), M_DP1 per cell, and D_needed = D_max at k_lo. Move the rest of WS1 (C02, C04, C05, C13, E02, F02, F04, H16) and all of WS4 except the background CPU pass into N1-a/N1-d, where they are produced once.

2. **Run k_lo before the full floor, and turn WS2 into a threshold test.** k_lo costs a fraction of a day (§2.3). Then WS2 begins with a half-day coarse idealized floor: stage count x idealized multiplier/adder depth, all favourable switches on at once (A02 free loader, A13 free exponential, A07 unproved width, A08/A09 literature constants, A16 temporary-AND, F05). It moves on to the A01_run014 DAG reweight only if k_lo x D_coarse falls within 10x of the threshold in §1. For DP1, report **one** number: the floor at ≤ 10x the width cap, the only value M_DP1 uses. Defer the unlimited-width and current-cap variants, the T-count, the category split and the per-lever ablations to N1-b.

3. **Remove "W0 still finishes, for the record" (§9 day 1-2).** If k_lo x (coarse floor) is above 30x the threshold, stop the remaining W0 work, write the DP1 memo, and leave the "record" numbers to N1. N1 produces them at higher rigour anyway, so the W0 versions would be thrown away.

4. **Drop W1-R as a separate post-W0 step.** It is the third computation of the A01 floor and the F31 table (W0, then W1-R, then the N1 R2 lifecycle with its own independent review). Make it conditional: run it only if min M_DP1 ≤ 10, where a 10% disagreement could flip the outcome. When it does run, start it **in parallel with W0**, from the same inputs and along the analytic path, without seeing W0 outputs. That makes it more independent, and the room exists once W0 has 2 workstreams.

5. **Drop W1-FAC on branch N.** Building a scope factory for two R2 scopes is a single-use abstraction, and its claimed 60-70% saving is not reflected in the N1 estimate: §7 gives 7-11M, which is about 2x(2-5M) + 2x1M with no saving applied. Either the factory saves nothing or N1 is overstated by about 2x. Copy the #43 artifacts directly for N1. Build the factory only after a GO, when A3 needs many R2 scopes. Also, W1-FAC currently runs *before* DP1, so it is spent even if the user stops at DP1.

6. **Register-only, no W0 slot:** H04, H07, H14 (the rows already hold the zero-cost results: one syndrome round ≥ 100 ns, cat gates in µs, 0.39/0.051 ns vs the photonic floor); E20 (the row already holds the width bound: P ~1e3-1e4, ≥ 4e9 logical qubits); F08 (< 1.1x); E08 (the 1.36x line is already in the P column); C13 (no combined emission exists on branch N); C04 (an identity assert inside the script); F02 (read-only check, done by construction in `gap_calc.py`); H06 (CCZ mapping frozen; the "fold" adds nothing). Together these remove about 11 items from agent workstreams.

7. **Do not re-derive the E01 threshold k*.** The E01 row already computes miss(k) ≈ 177k at B8x52 $0.001, and §2.2 tabulates the 36/356-layer thresholds. WS3's only new output should be k_lo, the smallest k with a published or analytic 99% worst-case guarantee for a [0, $38.82] payoff. **Merge E25 into the same literature query.** The E25 search for a worst-case coverage theorem and the E01 search for k_lo are the same search, and E25 is currently costed M on its own.

8. **E03/E04 credits: cite, do not screen.** The 2.0x and 1.75x values are already in the triage rows and the P column. In W0 they matter only if the literature k_lo comes out above the P value (~224). Gate any E03/E04 work on that condition.

9. **H03: take it off R2 and out of T1, and run the CPU pass once.** H03's full-source CCX recount refines only the "current depth" column, not D_floor, not M_DP1, and not the claim that even the idealized oracle misses. The measured leaf ratio of 4.00 (`h_tools/ccx_depth_screen.json`) is already the quantum-favourable credit. If the full pass is wanted, run it once in background at R0 and cite it by SHA256 in N1. §7 currently lists a "rerun of H03/A01 under the lifecycle" for N1, which contradicts §5.4 (re-verify only if the input hash changed). Delete that rerun.

10. **E02: move from T1 to N1-a only.** k_eff does not enter DP1. Its expected outputs (M = 2^13 / 2^14 / 2^19) are already the ledger's modelled values. The exact-rational emission is a headline-table certification, and it belongs only in the one lifecycle that certifies the headline table.

11. **Merge N1-a and N1-b into one R2 scope (#44), and consider R1.** Their dependency is hidden: N1-a's decision table consumes N1-b's certified D_floor, so the two cannot really run in parallel as §4.4 implies. §5.2 already allows one R2 scope to carry several certificates with shared inputs, and these two share A01_run014, A10 and the ledger. One lifecycle instead of two saves about 2-5M tokens and 2-4 days.

    Further, if min M_DP1 is ≥ 30, claim-grade precision on these numbers cannot change the conclusion. The D_floor is an idealized *construction* estimate, not a lower bound, so R2 certifies a modelling choice, not a fact about all oracles. In that case R1 (an independent recompute plus a receipt) is enough. Let the user choose R1 vs R2 at DP1, and make the margin the stated criterion.

12. **C09: fold it in as a column; do not run it as a separate N1-d slice.** Note against the plan's "adverse-only" framing: the C09 row says a symmetric distribution-free convention moves the net **2-5x in quantum's favour**. At Tier O that matters (an 8x miss divided by 5 is 1.6x), so it is not waste. It belongs with the H16 x16 sensitivity, which is also quantum-favourable (the row gives B8 1,018x → 64x at k = 3), as a sensitivity column in the same script/scope as M_DP1. Otherwise DP1 is decided without them and they reopen it in N1, which is repeated work. Put both columns into the DP1 computation now.

13. **C15: cite the anchors, do not verify them.** The plan's own kill rule ("if an anchor fails, state the negative only at the hypothetical 100/10 ns") means verification cannot change the result. The C15 row is costed M for about 10-20 anchor checks. Replace that with a citation list in N1-d. H01/H02 then reduce to that same table, and H17's two necessary-condition columns are arithmetic in the script (fix 1).

14. **F01 eps* crossover and C08: drop both.** Computing eps* in W0 is what creates the only trigger for C08, an M-cost scramble bootstrap ("only if the paper states an eps-extrapolated crossover"). The fixed task does not need an extrapolated crossover statement. Keep F01's measured/fitted/assumed labels (script), drop eps*, and move C08 to register-only.

15. **W1-REG: script only, and generate it in N2.** Appendix A plus `rows_*.jsonl` already contain the status, tier, dependency, kill criterion and notes. A script that joins them and adds the evidence pointer and reopen-rule fields produces all 110 records in minutes. Agent review in batches of 20 (§4.2, §9 day 4-5) is unnecessary for the 66 record-only items, which by definition cannot change anything. Spot-check about 10 records. The register is needed only for the N2 appendix, so DP1 does not have to wait for it. Change definition of done (a) to "script output 110/110 + DP1 decided".

16. **N2: draft in parallel with N1.** C12 labelling, E22 closed escape, the F20/F04/F05 "even with free X" sentences and the register appendix do not depend on the certified N1 numbers. One agent can draft them during N1, leaving only number substitution after N1. This cuts N2 from 4-5 days to about 2 days of review, audit and sign-off.

17. **Branch A, A1(a): drop the lean single-process T_C at $0.10/$0.03.** GO already requires a *non-overhead* eligible cell (§4.3), so removing intercepts in the overhead cells cannot change DP2. Keep only the H16 grid and C10/F06/F07 challengers on the cell that triggered GO. The same applies to the C10 classical PDE/sparse-grid challenger for B4x12: run it only if B4x12 is the GO cell.

18. **Re-tier for consistency once the fixes are in.**
    - T1 becomes {A01, E01, C11-bracket} for DP1, plus {F31/C14} as the headline table.
    - E02 and H03 drop to "N1 inputs".
    - H04, H07 and H14 go to T5 register (this also resolves Defect 2).
    - Restate the §0 split (66/41/3) after the moves. The branch-N content list falls from 40 (+C08) to about 30 items with real work.

## 3. Estimates

- **Padded or inconsistent.**
  - N1 7-11M ignores the claimed factory saving (fix 5).
  - The branch-N total is "13-20M" in §7 but "15-20M" in §0.
  - N1's 7-10 days assumes N1-a and N1-b run in parallel, which they cannot (fix 11), and still exceeds 2 R2 runs of 2-4 days.
  - W1's 2 days is spent entirely on work that fixes 4, 5 and 15 remove or move off the critical path.
- **Revised branch-N estimate with fixes 1-16:**
  - W0': 1.5-2 days, 2 agents plus a script, ~0.8-1.2M tokens.
  - DP1: unchanged.
  - N1': 4-6 days, 1 merged scope plus 2 R1 cards, ~4-7M at R2 or ~2-3M at R1.
  - N2': ~2 days, ~1-1.5M.
  - Total: **about 1.5-2 weeks and ~6-10M tokens**, against 3-4 weeks and 13-20M. That is roughly half, with no loss of anything the negative/frontier result or DP1 consumes.
- **Usage-limit fit.** The revised peak is 2-3 concurrent agents (W0': 2; N1': 3 including the N2 drafter). That is below the plan's 4-agent ceiling, which the last two capped waves suggest is itself too optimistic.

## 4. What is not waste (kept deliberately)

- A01 floor and E01/C11 k_lo: the only DP1 unknowns.
- The C09 and H16 quantum-favourable sensitivities, as columns (fix 12).
- One certified headline scope.
- The §8 STOP list. It is correct and should stand: E11/#44-U4, A-family percent-level certificates, C8 relaunch, GPU anchors and further timing precision.
