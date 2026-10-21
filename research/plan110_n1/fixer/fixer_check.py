"""N2-fixer: check that the numbers v2 adds or changes appear in the draft and match file values.

Run from the repository root:
    .context/frontier_t0_env/Scripts/python.exe -I -S -B research/plan110_n1/fixer/fixer_check.py
Writes results/plan110_n1/fixer/fixer_check.json (exclusive create) and appends a summary row.
"""
import hashlib
import json
import os
import sys

ROOT = os.getcwd()
V1 = "manuscript/advantage-frontier-2026-09-23/FRONTIER_NEGATIVE_RESULT_DRAFT.md"
V2 = "manuscript/advantage-frontier-2026-09-23/FRONTIER_NEGATIVE_RESULT_DRAFT_v2.md"
FX = "results/plan110_n1/fixer/fixer_numbers.json"
FX2 = "results/plan110_n1/fixer/fixer_numbers_2.json"
HT = "results/plan110_n1/headline/headline_table.json"
HW = "results/plan110_n1/hwclassical/hw_classical_card_v2.json"
DC = "results/plan110_n1/review/dirsel_confirm.json"
OUT = "results/plan110_n1/fixer/fixer_check.json"
ROWS = "results/plan110_n1/fixer/rows.jsonl"


def rd(p, mode="r"):
    with open(os.path.join(ROOT, p), mode, **({} if "b" in mode else {"encoding": "utf-8"})) as fh:
        return fh.read()


def sha(p):
    return hashlib.sha256(rd(p, "rb")).hexdigest()


text = rd(V2)
fx, fx2, ht, hw, dc = (json.loads(rd(p)) for p in (FX, FX2, HT, HW, DC))
s = ht["summary_min_M_eligible_non_overhead"]
mm = hw["classical"]["M_minima"]
t = fx["d2_thresholds_B8_0.001"]
checks = [
    # (id, snippet in v2, quoted value, file value, abs tol)
    ("thr_expl_layers", "9.90", 9.90, t["explicit_best"]["max_D_eff_layers"], 0.005),
    ("thr_expl_T", "9.9e5", 9.9e5, t["explicit_best"]["max_T_per_iterate"], 0.05e5),
    ("thr_cert_layers", "2.86", 2.86, t["certified"]["max_D_eff_layers"], 0.005),
    ("thr_cert_T", "2.9e5", 2.9e5, t["certified"]["max_T_per_iterate"], 0.05e5),
    ("thr_certds_layers", "5.73", 5.73, t["certified_dirsel"]["max_D_eff_layers"], 0.005),
    ("thr_certds_T", "5.7e5", 5.7e5, t["certified_dirsel"]["max_T_per_iterate"], 0.05e5),
    ("thr_win", "| 266 |", 266, t["window_fail001"]["max_D_eff_layers"], 0.5),
    ("thr_win_T", "2.7e7", 2.7e7, t["window_fail001"]["max_T_per_iterate"], 0.05e7),
    ("allfree_over_expl", "11.5×", 11.5, t["explicit_best"]["W0_allfree_D_eff_over_threshold"], 0.05),
    ("allfree_over_cert", "39.8×", 39.8, t["certified"]["W0_allfree_D_eff_over_threshold"], 0.05),
    ("allfree_over_certds", "19.9×", 19.9, t["certified_dirsel"]["W0_allfree_D_eff_over_threshold"], 0.05),
    ("N1allfree_over_expl", "16.5×", 16.5, t["explicit_best"]["N1_allfree_D_eff_over_threshold"], 0.05),
    ("sym_expl_layers", "365 layers", 365, fx2["symmetric_thresholds"]["explicit_best"]["max_D_eff_layers"], 0.5),
    ("sym_expl_T", "3.7e7 T", 3.7e7, fx2["symmetric_thresholds"]["explicit_best"]["max_T_per_iterate"], 0.05e7),
    ("sym_cert_layers", "106 layers", 106, fx2["symmetric_thresholds"]["certified"]["max_D_eff_layers"], 0.5),
    ("sym_cert_T", "1.1e7 T", 1.1e7, fx2["symmetric_thresholds"]["certified"]["max_T_per_iterate"], 0.05e7),
    ("c09_points", "**30.2×**", 30.2, fx["d4_c09"]["points_ratio_CLT_over_practice"], 0.05),
    ("c09_EB", "**1.86×**", 1.86, fx["d4_c09"]["EB_over_CLT"], 0.005),
    ("c09_cost", "0.66×", 0.66, fx["d4_c09"]["cost_ratio_iid_over_practice"], 0.005),
    ("c09_clt_n", "4.30e7", 4.30e7, fx["d4_c09"]["iid_CLT_points"], 0.005e7),
    ("c09_pr_n", "1.43e6", 1.43e6, fx["d4_c09"]["practice_points"], 0.005e6),
    ("c09_eb_n", "8.02e7", 8.02e7, fx["d4_c09"]["EB_points"], 0.005e7),
    ("c09_pp_practice", "15.8 µs", 15.8e-6, fx["d4_c09"]["per_point_time_practice_s"], 0.05e-6),
    ("c09_total", "**36.9**", 36.9, fx["d4_c09"]["factor_total"], 0.05),
    ("cert_ds_df_BM", "| 10.9 |", 10.9, fx["d6_certified"]["certified_BM_distfree_dirsel"], 0.05),
    ("cert_ds_df_AF", "| 0.54 |", 0.54, fx["d6_certified"]["certified_allfree_distfree_dirsel"], 0.005),
    ("cert_ds_k", "341.4", 341.4, fx["d6_certified"]["certified_dirsel_k"], 0.05),
    ("cert_ds_M", "400.7", 400.7, fx["d6_certified"]["certified_dirsel_primary"], 0.05),
    ("win_df", "0.23 (failure 0.01)", 0.23, mm["box_muller_current_law|no_explicit_constant"]["min_M_distfree"], 0.005),
    ("win_df_AF", "| 0.012 |", 0.012, mm["all_free_and_narrow|no_explicit_constant"]["min_M_distfree"], 0.0005),
    ("noU1_k", "353.0", 353.0, fx["d8_no_U1"]["k_noU1"], 0.05),
    ("noU1_BM", "**11.2**", 11.2, fx["d8_no_U1"]["M_distfree_noU1_BM"], 0.05),
    ("noU1_AF", "**0.56**", 0.56, fx["d8_no_U1"]["M_distfree_noU1_allfree"], 0.005),
    ("noU1_primary", "414.4", 414.4, fx["d8_no_U1"]["M_primary_noU1"], 0.05),
    ("zb_expl", "104.4", 104.4, fx["d3_zero_bias"]["explicit_e_eq_eps"], 0.05),
    ("zb_cert", "400.7", 400.7, fx["d3_zero_bias"]["certified_e_eq_eps"], 0.05),
    ("zb_win", "3.88", 3.88, fx["d3_zero_bias"]["window001_e_eq_eps"], 0.005),
    ("zb_pair", "0.506", 0.506, fx["d3_zero_bias"]["pair_allfree_1lane_at_e_eq_eps"], 0.0005),
    ("zb_fail001", "76.6", 76.6, s["explicit_best_fail001"]["e_eq_eps"][0], 0.05),
    ("inel_cert", "1,065", 1065, fx["d3_zero_bias"]["ineligible_certified_B4x12"], 0.5),
    ("inel_win", "11.8", 11.8, s["no_explicit_fail001"]["primary_B8_0.001_ineligible"][0], 0.05),
    ("tc_h16", "23.46 s", 23.46, fx["d10_TC"]["H16_16w"], 0.005),
    ("tc_pct", "4.1%", 4.1, (fx["d10_TC"]["ratio"] - 1) * 100, 0.05),
    ("tc_M", "222.8", 222.8, fx["d10_TC"]["M_explicit_with_H16_T_C"], 0.05),
    ("split_74", "**74.8**", 74.8, fx["d11_split"]["M_supply_1e13"], 0.05),
    ("split_310", "**3.10**", 3.10, fx["d11_split"]["supply_factor"], 0.005),
    ("span_BM", "$0.17", 0.17, fx["d7_residual_span"]["max_residual_span_BM_floor_usd"], 0.005),
    ("span_AF", "$3.37", 3.37, fx["d7_residual_span"]["max_residual_span_allfree_usd"], 0.005),
    ("span_DF", "$6.18", 6.18, fx["d7_residual_span"]["max_residual_span_BM_distfree_usd"], 0.005),
    ("span_used", "$38.82", 38.82, fx["d7_residual_span"]["span_used_usd"], 0.005),
    ("win_range_0003", "8.25-8.77", 8.77, fx["d13_ranges"]["window_k"]["B8x52|0.003"]["all_eps"][1], 0.005),
    ("win_range_001", "6.93-7.37", 7.37, fx["d13_ranges"]["window_k"]["B8x52|0.01"]["all_eps"][1], 0.005),
    ("lb_B4_prim", "1.691-1.696", 1.691, fx["d13_ranges"]["counting_LB_delta001_Q_plus_one_A"]["B4x12|support|0.45eps"][0], 0.0005),
    ("lb_B8_prim", "1.848-1.853", 1.848, fx["d13_ranges"]["counting_LB_delta001_Q_plus_one_A"]["B8x52|support|0.45eps"][0], 0.0005),
    ("lb_mean_prim", "0.15-0.16 at the primary", 0.15, fx["d13_ranges"]["counting_LB_delta001_Q_plus_one_A"]["mean-bounded_all_cases_primary_split"][0], 0.005),
    ("lb_mean_both", "0.14-0.16 over both", 0.14, fx["d13_ranges"]["counting_LB_delta001_Q_plus_one_A"]["mean-bounded_all_cases_both_splits"][0], 0.005),
    ("floor_ratio_B4", "1.547×", 1.547, fx["d1_N1_floor_only"]["floor_ratio_B4"], 0.0005),
    ("floor_ratio_B8", "1.570×", 1.570, fx["d1_N1_floor_only"]["floor_ratio_B8"], 0.0005),
    ("dc_097", "0.9718", 0.9718, dc["per_cell"]["B8x52|0.001"]["explicit_allfree_1lane_dirsel"], 0.00005),
]
res = []
for cid, snip, q, v, tol in checks:
    res.append({"id": cid, "snippet": snip, "in_v2": snip in text, "quoted": q, "file_value": v,
                "tol_abs": tol, "match": abs(q - v) <= tol})
bad = [r for r in res if not (r["in_v2"] and r["match"])]
claim = '"No design with certified constants reaches a 10× complete-latency advantage for the fixed B4x12/B8x52 knock-out task under the stated conventions."'
out = {"meta": {"script": "research/plan110_n1/fixer/fixer_check.py", "python": sys.version,
                "flags": {"isolated": sys.flags.isolated, "no_site": sys.flags.no_site},
                "inputs_sha256": {p: sha(p) for p in (V1, V2, FX, FX2, HT, HW, DC)},
                "v1_sha256_expected_prefix_suffix": ["3d8e5900", "c62b1c"],
                "v1_unchanged": sha(V1).startswith("3d8e5900") and sha(V1).endswith("c62b1c")},
       "claim_verbatim_in_v2": claim in text,
       "n_checks": len(res), "n_bad": len(bad), "checks": res}
with open(os.path.join(ROOT, OUT), "x", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1)
with open(os.path.join(ROOT, ROWS), "a", encoding="utf-8") as fh:
    fh.write(json.dumps({"ws": "n2_fixer", "sub": "v2_number_check",
                         "value": {"n_checks": len(res), "n_bad": len(bad), "bad": [r["id"] for r in bad],
                                   "v1_unchanged": out["meta"]["v1_unchanged"],
                                   "claim_verbatim": out["claim_verbatim_in_v2"]},
                         "label": "check", "direction": "n/a", "source": OUT}) + "\n")
print(json.dumps({k: out[k] for k in ("claim_verbatim_in_v2", "n_checks", "n_bad")}), out["meta"]["v1_unchanged"])
for r in bad:
    print(r)
