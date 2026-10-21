"""N2-fixer: recompute every number that the v2 draft adds or changes relative to v1.

Run from the repository root:
    .context/frontier_t0_env/Scripts/python.exe -I -S -B research/plan110_n1/fixer/fixer_numbers.py

Stdlib only. Reads N1 result files (and the review's dirsel_confirm.json), writes
results/plan110_n1/fixer/fixer_numbers.json with exclusive create, and appends one row per
sub-result to results/plan110_n1/fixer/rows.jsonl as it goes.
All outputs are modelled arithmetic on N1 values (T_C, sigma, H16 times measured).
"""
import hashlib
import json
import os
import sys

ROOT = os.getcwd()
F = {
    "HT": "results/plan110_n1/headline/headline_table.json",
    "HW": "results/plan110_n1/hwclassical/hw_classical_card_v2.json",
    "ES": "results/plan110_n1/estimator/estimator_recompute.json",
    "DC": "results/plan110_n1/review/dirsel_confirm.json",
    "NC": "results/plan110_n1/review/number_check.json",
}
OUT = "results/plan110_n1/fixer/fixer_numbers.json"
ROWS = "results/plan110_n1/fixer/rows.jsonl"


def sha(p):
    with open(os.path.join(ROOT, p), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def load(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as fh:
        return json.load(fh)


def row(sub, value, label, direction, source, defect):
    with open(os.path.join(ROOT, ROWS), "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"ws": "n2_fixer", "defect": defect, "sub": sub, "value": value,
                             "label": label, "direction": direction, "source": source}) + "\n")
    return value


HT, HW, ES, DC, NC = (load(F[k]) for k in ("HT", "HW", "ES", "DC", "NC"))
T_LAYER, SUPPLY = 1e-7, 1e12
cell = {(c["case"], c["eps"]): c for c in HT["cells"]}
B8 = cell[("B8x52", 0.001)]
D_used = B8["D_eff_primary"]["used"]
T_C = B8["T_C"]
soe = B8["sigma_over_e"]
D_max = T_C / (10 * soe * T_LAYER)
k = B8["k"]
D_allfree = HT["D_eff_table"]["B8x52|all_free|W1e7|1e12|100ns"]
res = {}

# ---- defect 2: checkable thresholds (max D_eff and max T per iterate for M <= 1) ----
cert_dirsel_k = None
for r in ES["part1_k_eff_today"]:
    if r["case"] == "B8x52" and r["eps"] == 0.001 and r["split"] == "0.45eps":
        cert_dirsel_k = r["k_eff_direction_select"]
thr = {}
for name, kk in (("explicit_best", k["explicit_best"]), ("certified", k["certified"]),
                 ("certified_dirsel", cert_dirsel_k), ("window_fail001", k["no_explicit_fail001"]),
                 ("window_fail0003", k["no_explicit_fail0003"])):
    dmax = D_max / kk
    thr[name] = {"k": kk, "max_D_eff_layers": dmax, "max_T_per_iterate": dmax * SUPPLY * T_LAYER,
                 "W0_allfree_D_eff_over_threshold": D_allfree["W0"] / dmax,
                 "N1_allfree_D_eff_over_threshold": D_allfree["N1"] / dmax,
                 "primary_D_eff_over_threshold": D_used / dmax}
res["d2_thresholds_B8_0.001"] = row("thresholds", {"D_max_k1": D_max, **thr},
                                    "modelled (derived)", "neutral (threshold)", "HT, ES", 2)

# ---- defect 3: zero-bias reading ----
s = {kc: {kd: v[0] for kd, v in d.items()} for kc, d in HT["summary_min_M_eligible_non_overhead"].items()}
res["d3_zero_bias"] = row("strict_zero_bias", {
    "explicit_e_eq_eps": s["explicit_best"]["e_eq_eps"], "certified_e_eq_eps": s["certified"]["e_eq_eps"],
    "window001_e_eq_eps": s["no_explicit_fail001"]["e_eq_eps"],
    "pair_allfree_1lane_at_e_eq_eps": DC["per_cell"]["B8x52|0.001"]["explicit_eq_eps_allfree_1lane"],
    "ineligible_explicit_B4x12": s["explicit_best"]["primary_B8_0.001_ineligible"],
    "ineligible_certified_B4x12": s["certified"]["primary_B8_0.001_ineligible"],
    "bias_after_clamp_tightening_usd": 0.000473, "bias_over_eps": 0.473,
    "sigma_over_e_check": 5.183395545396595 / (0.45 * 0.001)},
    "modelled", "q+ (zero-bias reading) / q- (ineligible reading)", "HT, DC, W0 ws_small README A1", 3)

# ---- defect 4: C09 decomposition at the binding cell ----
hwrow = {(r["case"], r["eps"]): r for r in HW["classical"]["rows"]}
r8 = hwrow[("B8x52", 0.001)]
z = 2.5758293035489004  # z_{0.995}
n_clt = (z * r8["sigma_preint"] / r8["e"]) ** 2
n_eb = r8["routes"]["S40"]["iid_preint_EB"]["n"]
n_pr = r8["practice_points"]
c_iid = HW["classical"]["per_point_cost_s_16w"]["B8x52|preint"]
c_pr = r8["T_C_practice_s"] / n_pr
dec = {"factor_total": r8["factor_df_over_practice"], "practice_points": n_pr, "iid_CLT_points": n_clt,
       "EB_points": n_eb, "points_ratio_CLT_over_practice": n_clt / n_pr, "EB_over_CLT": n_eb / n_clt,
       "per_point_cost_iid_s": c_iid, "per_point_time_practice_s": c_pr,
       "cost_ratio_iid_over_practice": c_iid / c_pr,
       "time_ratio_CLT_iid_over_practice": n_clt * c_iid / r8["T_C_practice_s"],
       "product_check": (n_clt / n_pr) * (n_eb / n_clt) * (c_iid / c_pr)}
mm = HW["classical"]["M_minima"]
dec["M_distfree"] = {"BM_explicit": mm["box_muller_current_law|explicit_best"]["min_M_distfree"],
                     "BM_certified": mm["box_muller_current_law|certified_today"]["min_M_distfree"],
                     "allfree_explicit": mm["all_free_and_narrow|explicit_best"]["min_M_distfree"],
                     "allfree_certified": mm["all_free_and_narrow|certified_today"]["min_M_distfree"],
                     "BM_window001": mm["box_muller_current_law|no_explicit_constant"]["min_M_distfree"]}
res["d4_c09"] = row("c09_decomposition", dec, "modelled from measured inputs", "q+ (classical slows)", "HW", 4)

# ---- defect 6: direction-select readings of the certified class ----
pc = DC["per_cell"]["B8x52|0.001"]
res["d6_certified"] = row("certified_class", {
    "certified_primary": s["certified"]["primary"],
    "certified_dirsel_primary": s["certified"]["primary"] * pc["dirsel_ratio_certified"],
    "certified_dirsel_k": cert_dirsel_k,
    "certified_allfree_distfree": pc["certified_allfree_distfree"],
    "certified_allfree_distfree_dirsel": pc["certified_allfree_distfree_dirsel"],
    "certified_BM_distfree_dirsel": dec["M_distfree"]["BM_certified"] * pc["dirsel_ratio_certified"],
    "explicit_dirsel_primary": s["explicit_best"]["primary"] * pc["dirsel_ratio_explicit"]},
    "modelled (derived)", "q+", "HT, HW, DC", 6)

# ---- defect 7: residual-span threshold (first order: bounded-AE calls ~ span) ----
span = 8192 / 211
res["d7_residual_span"] = row("residual_span_threshold", {
    "span_used_usd": span,
    "span_reduction_needed_BM_floor_primary": s["explicit_best"]["primary"],
    "max_residual_span_BM_floor_usd": span / s["explicit_best"]["primary"],
    "span_reduction_needed_allfree_primary": s["explicit_best"]["all_free_oracle"],
    "max_residual_span_allfree_usd": span / s["explicit_best"]["all_free_oracle"],
    "span_reduction_needed_BM_distfree": dec["M_distfree"]["BM_explicit"],
    "max_residual_span_BM_distfree_usd": span / dec["M_distfree"]["BM_explicit"],
    "sigma_reduction_hard_cap_register_F20": 5.15 / 1.14,
    "note": "first order only: ignores the control's coherent cost (raises D_eff) and the mean-bound position of the residual"},
    "modelled (derived, first order)", "q+ (lower bound on the needed reduction)", "HT, HW, register F20", 7)

# ---- defect 8: without U1 ----
p2s = {(r["case"], r["eps"]): r for r in ES["part2_summary"]}
k_noU1 = p2s[("B8x52", 0.001)]["span+nondyadic (no mean cert)"]["k"]
res["d8_no_U1"] = row("no_U1", {
    "k_noU1": k_noU1, "M_primary_noU1": s["explicit_best"]["primary"] * k_noU1 / k["explicit_best"],
    "M_distfree_noU1_BM": dec["M_distfree"]["BM_explicit"] * k_noU1 / k["explicit_best"],
    "M_distfree_noU1_allfree": dec["M_distfree"]["allfree_explicit"] * k_noU1 / k["explicit_best"]},
    "modelled (derived)", "q- relative to the U1-credited row", "ES, HW", 8)

# ---- defect 10: T_C min-over-candidates vs H16 rerun ----
h16 = {h["cell"]: h for h in HW["classical"]["h16"]}
t16 = h16["B8x52/0.001"]["t_c_by_workers"]["16"]
res["d10_TC"] = row("T_C_vs_H16", {"T_C": T_C, "H16_16w": t16, "ratio": t16 / T_C,
                                   "M_explicit_with_H16_T_C": s["explicit_best"]["primary"] * T_C / t16},
                    "measured (times); modelled (M)", "q- (min over noisy candidates)", "HT, HW", 10)

# ---- defect 11: split ----
res["d11_split"] = row("unlimited_supply_split", {
    "M_supply_1e13": s["explicit_best"]["supply_1e13"],
    "supply_factor": s["explicit_best"]["primary"] / s["explicit_best"]["supply_1e13"],
    "t_layer_needed_ns": 100 / s["explicit_best"]["supply_1e13"]},
    "modelled", "neutral", "HT", 11)

# ---- defect 13: ranges ----
win = {}
for r in ES["part5_window_k"]:
    if r["span"] == "8192/211" and r["mean"] == "price+L1":
        win.setdefault((r["fail"], r["case"]), []).append((r["eps"], r["k_window"]))
wr = {}
for (fail, case), v in win.items():
    ks = [x[1] for x in v]
    wr[f"{case}|{fail}"] = {"all_eps": [min(ks), max(ks)], "at_0.001": [x[1] for x in v if x[0] == 0.001][0]}
lb = {}
for r in ES["part3_counting_lower_bound"]:
    if r["delta"] != 0.01:
        continue
    key = (r["case"], r["class"].split()[0], r["split"])
    lb.setdefault(key, []).append(r["k_LB_Q_plus_one_A"])
lbr = {"|".join(kk): [min(v), max(v)] for kk, v in lb.items()}
mean_all = [x for kk, v in lb.items() if kk[1] == "mean-bounded" for x in v]
lbr["mean-bounded_all_cases_both_splits"] = [min(mean_all), max(mean_all)]
mean_prim = [x for kk, v in lb.items() if kk[1] == "mean-bounded" and kk[2] == "0.45eps" for x in v]
lbr["mean-bounded_all_cases_primary_split"] = [min(mean_prim), max(mean_prim)]
sup_both = {c: [min(lb[(c, "support", "0.45eps")] + lb[(c, "support", "eps")]),
                max(lb[(c, "support", "0.45eps")] + lb[(c, "support", "eps")])] for c in ("B4x12", "B8x52")}
lbr["support_both_splits"] = sup_both
res["d13_ranges"] = row("ranges", {"window_k": wr, "counting_LB_delta001_Q_plus_one_A": lbr,
                                   "window_c_N400_used": ES["part4_window_c"]["c_used_N400_from_WS_k"],
                                   "window_c_N1_recomputed_N": sorted({x["N"] for x in ES["part4_window_c"]["rows"]})},
                        "modelled", "q+", "ES", 13)

# ---- defect 1: N1-floor-only M ----
res["d1_N1_floor_only"] = row("N1_floor_only", {
    **B8["M_N1_floor_only_primary"],
    "floor_ratio_B8": B8["D_eff_primary"]["N1"] / B8["D_eff_primary"]["W0"],
    "floor_ratio_B4": cell[("B4x12", 0.001)]["D_eff_primary"]["N1"] / cell[("B4x12", 0.001)]["D_eff_primary"]["W0"],
    "compare_W0_max_rel_diff_note": "see HT compare_W0"}, "modelled", "q- (N1 floor less favourable)", "HT", 1)

out = {"meta": {"script": "research/plan110_n1/fixer/fixer_numbers.py", "python": sys.version,
                "flags": {"isolated": sys.flags.isolated, "no_site": sys.flags.no_site,
                          "dont_write_bytecode": sys.flags.dont_write_bytecode},
                "inputs_sha256": {kk: sha(p) for kk, p in F.items()},
                "label": "modelled arithmetic on N1 values (T_C, sigma, H16 measured)"},
       **res}
with open(os.path.join(ROOT, OUT), "x", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1)
print(json.dumps(out, indent=1))
