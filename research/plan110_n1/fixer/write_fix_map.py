"""N2-fixer: write results/plan110_n1/fixer/fix_map.json (defect -> location -> fix), exclusive create.

Run from the repository root:
    .context/frontier_t0_env/Scripts/python.exe -I -S -B research/plan110_n1/fixer/write_fix_map.py
"""
import hashlib
import json

V2 = "manuscript/advantage-frontier-2026-09-23/FRONTIER_NEGATIVE_RESULT_DRAFT_v2.md"
OUT = "results/plan110_n1/fixer/fix_map.json"
ROWS = "results/plan110_n1/fixer/rows.jsonl"
with open(V2, "rb") as fh:
    h = hashlib.sha256(fh.read()).hexdigest()

M = [
    (1, "major", ["Abstract (R1 paragraph)", "§4.1 Effect", "§5.1 readings table and verdict", "§8 Rigour level", "§9.1 item 1"],
     "Replaced 'two R1 recomputes confirm them' with: N1 recomputed k, T_C, sigma/e and the M arithmetic exactly; the oracle term is the smaller of W0's (R0) and N1's (R1) floors, about 1.55x apart; N1's floor alone gives 1,258 / 364.2 / 13.5; R1 supports the verdict, not the quoted values",
     "HT M_N1_floor_only_primary; FX d1_N1_floor_only"),
    (2, "major", ["Abstract (checkable threshold)", "§1 scope item 1", "§3 item 3 table", "§6 lever 2", "§8 oracle-floor bullet"],
     "Thresholds per controlled Grover iterate at the binding cell: explicit <= 9.90 layers and <= 9.9e5 T; certified <= 2.86 layers and <= 2.9e5 T (5.73 / 5.7e5 with direction-select); window 266 layers / 2.7e7 T; all-free floor above by 11.5x / 39.8x (N1 all-free 16.5x); symmetric-convention limits 365 / 106 layers. Scope reworded with 'or' because the two limits are joint necessary conditions",
     "FX d2_thresholds_B8_0.001; FX2 symmetric_thresholds; NC derived_for_review"),
    (3, "major", ["Abstract (binding-cell sentence)", "§2 conventions table, row B8x52 $0.001", "§3 ledger sigma/e label", "§5.1 readings table", "§5.2 e = eps row", "§5.3 zero-bias pair paragraph", "§8 eligibility bullet", "§9.1 item 13"],
     "Cell admitted on a modelled, uncertified clamp tightening (bias $0.000473 = 0.47 eps <= 0.55 eps), so the primary keeps e = 0.45 eps; strict zero-bias line 104.4 / 400.7 and pair 0.506; eligibility listed as a re-certification debt (ineligible: 318.0 at B4x12)",
     "FX d3_zero_bias; HT summary e_eq_eps; DC per_cell; research/plan110_w0/ws_small/README.md A1"),
    (4, "major", ["Abstract (asymmetry paragraph, table column, robustness bullets)", "§2 table classical-confidence row", "§4.3 C09 decomposition and M table", "§5.2 distribution-free row", "§5.3 Reading", "§6 lever 3", "§8 robustness bullet"],
     "Stated up front: classical practice CIs vs quantum worst-case 99%; the symmetric distribution-free convention costs classical 36.9x at the binding cell; under it explicit M 6.29 (11.2 without U1) and all-free + distribution-free 0.31; the negative is robust only at the primary practice-CI convention. Relabelled as the stricter symmetric standard. Decomposition 30.2 x 1.86 x 0.66 = 36.9",
     "HW classical rows and M_minima; FX d4_c09; NC derived_for_review"),
    (5, "major", ["Abstract robustness bullets"],
     "Fragility sentence rewritten: all-free + symmetric classical = 0.31; all-free + 1 lane vs 1 core = 1.125, or 0.97 with direction-select",
     "HW; HT stacked_departures; AD; DC"),
    (6, "major", ["Abstract", "§4.2 direction-select paragraph", "§5.1 table status column", "§5.3 direction-select heading and Reading", "§8 certified-class bullet"],
     "'Assumed' changed to 'satisfied in the paper's cost model; not yet certified for a compiled circuit'; certified class 400.7-801.5 at primary and 0.54-1.08 with all-free + symmetric classical; noted that the window chains already use the same call cost",
     "ES part1_k_eff_today; DC; FX d6_certified; EC §2b and §2c"),
    (7, "major", ["§6 lever 5 (new)", "§7.1 / §7.2 / §7.3 (restructured)", "Appendix A mapping and exceptions", "Abstract lever list"],
     "F05 moved to 'bounded by the all-free floor (M = 11.5)', kill rule met, register kept at T2; F20 and F04 moved to 'outside the claim, not closed'; control-variate residual-span lever moved to the open-escapes section with reasoning (span-normalised k, unmeasured residual span, first-order needed reduction 232x / 11.5x / 6.29x, i.e. residual span <= $0.17 / $3.37 / $6.18, register triggers met under stacked departures); sigma-normalised sentence softened to 'in the sources checked'; 'changes none' replaced by explicit exceptions",
     "register.json F04/F05/F20; FX d7_residual_span; HT; HW"),
    (8, "minor", ["§4.2 credit 2", "§4.3 orientation-price bullet and table column", "§5.2 no-U1 row", "§8 orientation-price bullet"],
     "Without U1: k = 353.0, M_distfree 11.2 (Box-Muller) / 0.56 (all-free), primary 414.4; circularity stated",
     "ES part2_summary; FX d8_no_U1; NC"),
    (9, "minor", ["Abstract (data qubits, latency scope)", "§2 table width and split rows", "§6 lever 2 (48-bit bias)", "§8 q+ conventions bullet"],
     "Disclosed: classical 0.45 eps share without bias reserve (QF in Stage C spec §0.4-0.5); factories outside W (logical data qubits); latency counts Grover iterates only; 48-bit word bias unchecked",
     "ANALYSIS_SPEC_STAGE_C.md §0.4-0.5; W0_CARD.md"),
    (10, "minor", ["§2 T_C paragraph", "§3 ledger T_C label", "§8 q- bullet"],
     "T_C labelled 'meas, q- (min over candidates)'; H16 rerun 23.46 s (+4.1%) gives explicit M 222.8",
     "HW h16; FX d10_TC"),
    (11, "minor", ["§3 item 2"],
     "At unlimited supply M would be 74.8; tenfold then needs 1.34 ns layers; at 1e12 T/s supply adds a further 3.10",
     "HT supply_1e13; FX d11_split"),
    (12, "minor", ["Abstract table, window row"],
     "8.62 (failure 0.01) / 10.26 (0.003, like for like)", "HT"),
    (13, "minor", ["§4.2 window-constant paragraph", "§4.2 window table", "§4.2 counting bound"],
     "Window k 8.25-8.77 and 6.93-7.37 with the $0.001 values shown; mean-bounded bound 0.15-0.16 at the primary split (0.14-0.16 over both; lowest 0.074); support bound at the primary split 1.691-1.696 / 1.848-1.853 with the both-split range; N1 recomputed c only at N <= 200, and the N = 400 values are WS-k's, extrapolated to N ~ 1e3-3e5",
     "ES part3 / part4 / part5; FX d13_ranges"),
    (14, "minor", ["Front matter Provenance", "Appendix B closing note"],
     "Provenance limited to N1 / drafter / review / fixer scripts; measured timings attributed to the Stage C / H16 harness with numpy and numba",
     "W0_CARD.md; research/plan110_w0/ws_small/README.md"),
    (15, "minor", ["Source keys [DN] row", "Appendix B item 4"],
     "Disclosed the certified_k_range_0.45eps defect with a pointer to the correction row in the drafter rows.jsonl",
     "results/plan110_n1/drafter/rows.jsonl"),
    (16, "minor", ["§4.1 method", "§4.3 C09 and hardware", "§6 hardware paragraph", "§8 literature bullet", "§9.1 item 9"],
     "Floor-sheet citations and Maurer & Pontil marked 'lit, not re-fetched in N1'; 2026 anchors marked as resting on the fetch log; Yang qualified 'among the sources checked'",
     "REVIEW.md defect 16"),
    (17, "minor", ["§4.3 direction note"],
     "H16 timed only preint; decision-cell T_C is preint, so the 1-lane result is unaffected", "HT T_C raw_best"),
    (18, "minor", ["§4.2 lanes"],
     "Only one lane of the primary-width design fits; the B4x12 credit uses three lanes of the W = 1e6 design", "EC §3"),
    (19, "minor", ["§1 first paragraph"],
     "Removed 'closes the last open contract'; the knock-out basket is Failure 6 of WHY_NO_ADVANTAGE.md, and the draft turns it into a scoped frontier statement",
     "WHY_NO_ADVANTAGE.md Failure 6"),
    (20, "minor", ["§4.1 after the floor table", "§9.1 item 12"],
     "Loader-share discrepancy (DP1 36-56% vs N1 52-53%) listed", "DP1_MEMO.md; receipt.md"),
    (21, "minor", ["Abstract scope line after the claim"],
     "Scope line added directly after the verbatim claim (family, task, tested method; 'certified constants' = estimator constant; oracle costs are modelled idealized floors; latency scope)",
     "N1_CARD.md"),
]
out = {"meta": {"draft_v2": V2, "draft_v2_sha256": h, "draft_v1_unchanged": "see fixer_check.json meta.v1_unchanged",
                "review": "results/plan110_n1/review/REVIEW.md",
                "changelog": "v2 section 'Changelog (v1 -> v2)'",
                "number_check": "results/plan110_n1/fixer/fixer_check.json (59 checks, 0 bad; claim verbatim)"},
       "fixes": [{"defect": d, "severity": s, "locations": loc, "fix": f, "sources": src} for d, s, loc, f, src in M],
       "extra": [{"item": "review method note (v1 §9.2 item 13, now 15)",
                  "fix": "says 'confirmed by derived arithmetic' in dirsel_confirm.json, not by a headline rerun"},
                 {"item": "window class under the symmetric convention",
                  "fix": "discloses M = 0.23 (failure 0.01) with no oracle idealization (HW M_minima); not in v1"}]}
with open(OUT, "x", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1, ensure_ascii=False)
with open(ROWS, "a", encoding="utf-8") as fh:
    fh.write(json.dumps({"ws": "n2_fixer", "sub": "fix_map_written", "value": {"n_fixes": len(M), "draft_v2_sha256": h},
                         "label": "record", "direction": "n/a", "source": OUT}) + "\n")
print(len(M), h)
