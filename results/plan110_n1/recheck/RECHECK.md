# N2 re-check of FRONTIER_NEGATIVE_RESULT_DRAFT_v2.md

12 October 2026. Re-checker: N2-rechecker (plan110 branch N). This is an AI-assisted check. I did not write v1, v2 or the review.

**Files checked.**
- **Draft:** `manuscript/advantage-frontier-2026-09-23/FRONTIER_NEGATIVE_RESULT_DRAFT_v2.md`, sha256 `51dcf89b…8132d00`. This matches the hash in the fixer's `fix_map_written` row.
- **v1:** sha256 `3d8e5900…c62b1c`, unchanged.
- **Inputs:** the review list `results/plan110_n1/review/REVIEW.md` (21 defects), N1 results, W0 results, and the DP1 memo with its errata block.

**Method.**
1. I read v2 in full against each REVIEW.md defect.
2. **Number check.** `research/plan110_n1/recheck/recheck_draft.py` (stdlib, run with `-I -S -B`) wrote `results/plan110_n1/recheck/number_recheck.json` and appended `rows.jsonl`. It adapts the review's `check_draft.py` to v2 and contains 129 checks.
   - Every number that v2 adds is re-derived from the primary files: `headline_table`, `hw_classical_card_v2`, `estimator_recompute`, `dirsel_confirm`, the W0 `bias_desk` and the register. It is not read from the fixer's `fixer_numbers*.json`. The fixer value is kept alongside as a second column.
   - Tolerance is set by the precision printed in v2.
   - Each quoted snippet must appear verbatim in v2.
   - The script also checks that the v1 phrases each defect targeted are absent from the v2 body.
3. **Probes.** Part 4 of the same script computes the derived quantities behind the new defects below. All are labelled "mod, derived".

**Result: 129 of 129 checks pass.**
- Every quoted number in v2 matches its cited file at printed precision. This includes all values new in v2:
  - the thresholds 9.90 / 9.9e5, 2.86 / 2.9e5, 5.73 / 5.7e5 and 266 / 2.7e7;
  - the floor excesses 11.5× / 39.8× / 19.9× / 16.5×;
  - the symmetric limits 365 / 3.7e7 and 106 / 1.1e7;
  - the C09 decomposition 30.2 × 1.86 × 0.66 = 36.9 (z₀.₉₉₅ recomputed with `statistics.NormalDist`);
  - the no-U1 values 353.0 / 414.4 / 11.2 / 0.56;
  - the zero-bias and ineligible readings 400.7 / 104.4 / 3.88 / 76.6 / 1,065 / 318.0 / 11.8;
  - the pair 0.506;
  - the bias values $0.000473 = 0.47ε and the bound $0.00124;
  - T_C against H16: 23.46 s, +4.1%, M 222.8;
  - the residual spans $0.17 / $3.37 / $6.18 of $38.82;
  - the distribution-free table 21.7 / 10.9 / 6.29 / 11.2 / 0.23 and 1.08 / 0.54 / 0.31 / 0.56 / 0.012.
- My independent derivations agree with the fixer's file values to float precision.
- The claim is verbatim from the N1 card.
- The register tiers and quoted rules for F04, F05, F20, E22 and C12 match `register.json`. The DP1 errata block exists and records "two departures, not three".

**Provenance note (not a v2 defect).** These output files record Python 3.12.4 but do not record interpreter flags: `headline_table.json`, `keff.json`, `floor_sheet.json` and `estimator_recompute.json`. Their READMEs and docstrings state `-I -S -B`. The drafter, hwclassical, review and fixer outputs do record `isolated=1, no_site=1`.

## 1. The 21 review defects

| # | Sev. | Status | Where fixed in v2 (line numbers in v2) |
|---|---|---|---|
| 1 | major | **Fixed** | Abstract L87-89; §4.1 "Effect" L323-327; §5.1 readings table L570 and verdict L575-577; §8 "Rigour level" L834-838; §9.1 item 1. N1-floor values 1,258 / 364.2 / 13.5 verified. |
| 2 | major | **Fixed** (see N3-3, N3-4) | Abstract L102-107; §1 scope item 1 L144-150; §3 item 3 table L255-270; §6 lever 2 L677-679; §8 L803-807. All threshold numbers verified. |
| 3 | major | **Fixed** (label nit N3-7) | Abstract L76-78; §2 table L189; §3 ledger L231; §5.1 L571, L573; §5.2 L597, L601; §5.3 L625-627; §8 L824-828; §9.1 item 13. The W0 bias desk gives k = 3 binades → $0.000473 (0.473ε) and baseline $0.00124. |
| 4 | major | **Fixed** | Abstract L64-69 plus the symmetric column of the abstract table; §2 table L184; §4.3 L462-500, including the 30.2 × 1.86 × 0.66 decomposition, which I re-derived independently; §5.2 L593; §8 L808-811. |
| 5 | major | **Fixed** | Abstract L109-117. It now says "idealization + symmetric convention → 0.31" and "idealization + 1 lane → 1.125 / 0.97". |
| 6 | major | **Fixed** (see N3-1, N3-4) | §4.2 L367-385 ("satisfied in this paper's cost model; not yet certified for a compiled circuit"); §5.1 L558, L572; §5.3 L635-642; §8 L812-815; abstract L83 and L112-114. |
| 7 | major | **Fixed** (residual N3-6) | §6 lever 5 L701-731; §7 split into 7.1 closed, 7.2 bounded (F05) and 7.3 outside the claim (F20, F04, σ-normalised line, softened). Appendix A L950-962 now lists the exceptions. |
| 8 | minor | **Fixed** | §4.2 L358-360; §4.3 L495-500; §5.2 L594; §8 L820-823. |
| 9 | minor | **Fixed** | Abstract L60-62 and L96-97; §2 table L185 and L188; §6 L684-685; §8 L843-850. |
| 10 | minor | **Fixed** | §2 L191-205; §3 ledger L230; §8 L851-853. |
| 11 | minor | **Fixed** | §3 item 2 L244-254. At 1e13 T/s, the W0 D_eff is 740 and reaction-bound, as v2 states. |
| 12 | minor | **Fixed** | Abstract table L85. |
| 13 | minor | **Fixed** | §4.2 L387-398 (ranges 8.25-8.77 and 6.93-7.37 plus the $0.001 values; c recomputed only at N = 50/100/200). L418-423: support bound per split and over both splits; mean-bounded bound 0.15-0.16 / 0.14-0.16 / 0.074. |
| 14 | minor | **Fixed** | Front matter L47-51; Appendix B L988-990. One nit: the provenance sentence lists "N1, review and fixer scripts" but leaves out the drafter. The drafter outputs record `-I -S` anyway. |
| 15 | minor | **Fixed** | Source keys L35; Appendix B L978-981. The `correction_certified_k_range` row exists in the drafter `rows.jsonl`. |
| 16 | minor | **Fixed** | §4.1 L279-281; §4.3 L469-470 and L518-521; Yang qualified L526 and L735-736; §8 L862-865; §9.1 item 9. |
| 17 | minor | **Fixed** | §4.3 L457-460. Verified: `raw_best` is `preint` in all four decision cells. |
| 18 | minor | **Fixed** | §4.2 L431-433. |
| 19 | minor | **Fixed** | §1 L128-134. WHY_NO_ADVANTAGE.md §"Failure 6" confirmed. |
| 20 | minor | **Fixed** | §4.1 L310-311; §9.1 item 12. |
| 21 | minor | **Fixed** | Abstract L93-97, directly after the verbatim claim. |
| Review method note | n/a | **Fixed** | §9.2 item 15 says "derived arithmetic … not confirmed by a headline rerun". |

All 21 are fixed, and none were fixed incorrectly. The v1 phrases the defects targeted are absent from the v2 body. They survive only as quotations in the changelog.

## 2. New defects (introduced by the fixes, or newly visible after them)

No blockers and no majors. There are 8 minor defects, all text-only. The numbers each fix needs are in `number_recheck.json` → `probes`.

**N3-1 (minor; the most substantive). The "every reading" floors are not floors once two of v2's own readings are combined.**
- **Where:** §5.1 verdict L577-578 ("certified … M ≥ 400.7 and best explicit … M ≥ 104.4") and §8 L839-840 ("holds under every reading of the primary (≥ 104.4 explicit, ≥ 400.7 certified)").
- **The problem:** v2 now treats direction-select as satisfied in its cost model, and it treats the strict zero-bias reading as a reading of the primary. Taken together, these give (mod, derived, q+):
  - certified M = **200.4** (k = 379.3 at e = ε);
  - explicit M ≈ **90** (approximately; HT has no e = ε direction-select explicit k, so I used 104.4 × the 0.864 ratio);
  - explicit M ≈ **66** at failure 0.01.
- **Effect on the verdict:** none. All of these are still above the 30× threshold that justifies R1, so the verdict and the R1 justification survive.
- **Fix:** say "taken one at a time", and add the combined floor: certified ≈ 200 and explicit ≈ 90 (≈ 66 at failure 0.01).

**N3-2 (minor; already in v1 L547 and missed by the review). §6 lever 3 is wrong for two of its items.**
- **Where:** L693-694: "Any one of these, stacked with lever 2's all-free floor, reaches or nearly reaches M = 1".
- **True for:** distribution-free (0.31) and one lane (1.125).
- **False for:** supply 1e13 T/s plus all-free gives **11.3**, because the D_eff only drops from 114 to 112. 10 ns plus all-free gives **7.3**, because the D_eff is supply-bound at 724 layers (mod, derived from the HT `D_eff_table`).
- **Fix:** restrict the sentence to the first two items and quote the other two values.

**N3-3 (minor; scope precision introduced by the defect-2 fix). The thresholds hold at the binding cell only.**
- **Where:** §1 scope item 1 and §8 L807 ("Any design above either limit is covered by the claim").
- **The problem:** these use the binding-cell limits only. Tenfold in *any* eligible decision cell would overturn the result, and the other cells have their own, tighter limits for the same estimator class (explicit, mod, derived):

  | Cell | Max layers per iterate | Max T per iterate |
  |---|---:|---:|
  | B4x12 $0.001 | 1.14 | 1.1e5 |
  | B4x12 $0.01 | 0.53 | 5.3e4 |
  | B8x52 $0.01 | 2.43 | 2.4e5 |

  A design above 9.9 layers at B8x52 but below about 1.1 layers at B4x12 would not be covered by the sentence as written.
- **Why it changes nothing in practice:** the B4x12 all-free floor is 94 layers.
- **Fix:** add "and above the corresponding per-cell limit in the other decision cells (B4x12 $0.001: 1.1 layers / 1.1e5 T)".

**N3-4 (minor; inconsistency with the defect-6 fix). The certified-class threshold is quoted in four places without its direction-select value.**
- **Where:** abstract L105, §1 L149-150, §6 L679 and §8 L806-807 give only 2.9 layers / 2.9e5 T.
- **The problem:** v2 elsewhere reports the certified class as 400.7-801.5 because direction-select is satisfied in its cost model. The matching limit, 5.73 layers / 5.7e5 T, appears only in the §3 table. As a result, a design at 3-5.7 layers is called "covered by the claim" (§8 L807), yet it reaches M ≤ 1 under the certified schedule with direction-select.
- **Fix:** quote 2.9-5.7 layers (2.9e5-5.7e5 T). Alternatively, say explicitly that the claim's "certified" means without direction-select.

**N3-5 (minor; label).** The abstract table row "Best explicit worst-case constant (every conditional credit granted)" (L84; already in v1 L62) shows 232.0 / 6.29.
- **The problem:** direction-select is a conditional credit too. With every credit granted, the values are **200.4** (primary) and about **5.43** (symmetric, mod, derived).
- **Fix:** relabel the row "(U1 + U2 + non-dyadic M)", or add the direction-select values as the certified row does.

**N3-6 (minor; residual of defect 7).** §7.1 "Closed for this task" lists "Lanes, E20" (L753; already in v1).
- **The problem:** `register.json` has E20 at **T2, "credited screen value / branch-A lever"**, not closed. Appendix A L954-955 says the draft "reads three dispositions differently from the register" (F05, F20, F04). E20 is a fourth.
- **Fix:** add E20 to the Appendix A exception list, or move it out of 7.1. Its kill rule ("state the width bound … and stop") would support "bounded".

**N3-7 (minor; convention label).**
- **Where:** §2 table L189: "The primary therefore keeps e = 0.45ε (mod, q+)".
- **The problem:** the q+ belongs to *admitting* the cell on an uncertified tightening. Keeping e = 0.45ε instead of e = ε is q− relative to the zero-bias reading.
- **Fix:** move the label to the admission clause, or write "(admission: mod, q+)".

**N3-8 (minor; style and provenance in the body).**
- **"The user" in the paper body.** The text refers to "the user" in L67 ("the primary convention the user chose") and L467 ("the user's chosen primary"). In a manuscript this is project-internal and attributes a choice to a person. Write "the primary convention fixed in [W0C]".
- **The §8 heading.** "Undisclosed-in-v1 quantum-favourable conventions" (L843) refers to draft history. Write "Further quantum-favourable conventions".
- **Nit:** the §5.1 table gives k as "n/a" for "Best explicit with direction-select". The binding-cell value is 170.7 (ES `N1 best: all credits incl. dirsel`).
- **Stale but accurate:** front matter L8 says the revision "has not been re-checked by a reviewer". That was true when written; a v3 should update it.

**Checked and not defects:**
- The new §6 lever 5 first-order span argument. It is correctly caveated (control cost, mean-bound position), and the register triggers it quotes (F04 and F20, "miss ≤ 4×") are verbatim.
- "36.9× is the largest single convention lever". The next largest is the 10 µs layer at 32.2×.
- "They change M by less than 2.5×" (§6 lever 4). The maximum is 2.22×, for the zero-bias reading.
- The window threshold row: 266 layers, so all-free gives M = 0.43.
- The §4.2 statement that the window chains already use the direction-select call cost (estimator card L132).
- Affiliation VIT Vellore, the AI-assisted statement, no author names and no approval claims are all present.

## 3. Recommendation

**Ready for user sign-off.** All 21 review defects are fixed, and 129 of 129 number checks pass against the cited files with independent re-derivation. No new defect changes the claim, the verdict or the R1 justification:
- the lowest combined primary-convention reading is certified ≈ 200 and explicit ≈ 66-90, still at least 30×;
- the fragility under the symmetric convention is stated prominently.

The 8 new minor items are text-only and need no new computation. Their values are in `number_recheck.json` → `probes`. They can be folded into a v3 touch-up at or after sign-off without another full review round.

If the user wants no known inaccuracy in the text before signing, fix these two first:
- **N3-1:** the "≥ 400.7 / ≥ 104.4 under every reading" floors in §5.1 and §8;
- **N3-2:** "any one of these … reaches or nearly reaches M = 1" in §6.

Then a check of those two sentences is enough.
