"""N2-reviewer: programmatic check of the numbers quoted in
manuscript/advantage-frontier-2026-09-23/FRONTIER_NEGATIVE_RESULT_DRAFT.md
against the N1 (and W0) result files they cite.

Run from the repo root:
  .context/frontier_t0_env/Scripts/python.exe -I -S -B research/plan110_n1/review/check_draft.py

stdlib only. Output (exclusive create): results/plan110_n1/review/number_check.json
Appends one row per failed/flagged check plus one summary row to
results/plan110_n1/review/rows.jsonl.
Labels: every check compares a quoted (draft) number to a file value; the file
value keeps its source label (measured / modelled / assumed / literature).
"""
import hashlib
import json
import math
import sys

DRAFT = "manuscript/advantage-frontier-2026-09-23/FRONTIER_NEGATIVE_RESULT_DRAFT.md"
F = {
    "HT": "results/plan110_n1/headline/headline_table.json",
    "KF": "results/plan110_n1/headline/keff.json",
    "FS": "results/plan110_n1/headline/floor_sheet.json",
    "ES": "results/plan110_n1/estimator/estimator_recompute.json",
    "HW": "results/plan110_n1/hwclassical/hw_classical_card_v2.json",
    "DN": "results/plan110_n1/drafter/draft_numbers.json",
    "AD": "results/plan110_n1/drafter/addendum.json",
    "REG": "results/plan110_w0/register/run001/register.json",
    "WSK": "results/plan110_w0/ws_k/k_bracket.json",
    "W0DEC": "results/plan110_w0/decision/run002/decision_summary.json",
}
OUT = "results/plan110_n1/review/number_check.json"
ROWS = "results/plan110_n1/review/rows.jsonl"


def sha(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


J = {k: json.load(open(p, encoding="utf-8")) for k, p in F.items()}
draft = open(DRAFT, encoding="utf-8").read()
HT, ES, HW, DN, AD = J["HT"], J["ES"], J["HW"], J["DN"], J["AD"]
S = HT["summary_min_M_eligible_non_overhead"]
cell = {(c["case"], c["eps"]): c for c in HT["cells"]}
B8 = cell[("B8x52", 0.001)]
hwmin = HW["classical"]["M_minima"]
hwrow = {(r["case"], r["eps"]): r for r in HW["classical"]["rows"]}
nec = {(n["k_class"], n["floor_design"]): n for n in HW["necessary_conditions"]
       if n["case"] == "B8x52" and n["eps"] == 0.001}
sd = {s["departures"].__str__(): s["min_M"] for cls in ("explicit_best",)
      for grp in ("minimal_sets", "best_pairs", "best_single")
      for s in HT["stacked_departures"][cls][grp]}
sdc = HT["stacked_departures"]["certified"]
fsum = DN["floor_sheet_summary"]
p1 = ES["part1_k_eff_today"]
p2s = {(r["case"], r["eps"]): r for r in ES["part2_summary"]}

results = []


def chk(cid, where, snippet, quoted, actual, tol, src, label):
    """tol: ('abs', x) or ('rel', x)."""
    present = snippet in draft
    if isinstance(actual, (list, tuple)):
        ok = all(_ok(q, a, tol) for q, a in zip(quoted, actual))
    else:
        ok = _ok(quoted, actual, tol)
    results.append({"id": cid, "where": where, "snippet": snippet, "snippet_in_draft": present,
                    "quoted": quoted, "file_value": actual, "tol": tol, "match": ok,
                    "source": src, "label": label})


def _ok(q, a, tol):
    if a is None:
        return False
    kind, x = tol
    if kind == "abs":
        return abs(q - a) <= x * 1.0000001
    return abs(q - a) <= x * abs(a)


A = lambda nd: ("abs", 0.5 * 10 ** (-nd))
R = lambda r: ("rel", r)

# ---- headline M (abstract, section 3, 5.1) ----
chk("M_cert", "abstract/3/5.1", "**801.5**", 801.5, S["certified"]["primary"][0], A(1), "HT", "modelled")
chk("M_expl", "abstract/3/5.1", "**232.0**", 232.0, S["explicit_best"]["primary"][0], A(1), "HT", "modelled")
chk("M_win001", "abstract", "**8.62**", 8.62, S["no_explicit_fail001"]["primary"][0], A(2), "HT", "modelled")
chk("M_win0003", "3", "10.26", 10.26, S["no_explicit_fail0003"]["primary"][0], A(2), "HT", "modelled")
chk("M_allfree_distfree", "abstract", "M = 0.31", 0.31, hwmin["all_free_and_narrow|explicit_best"]["min_M_distfree"], A(2), "HW", "modelled")
chk("M_pair", "abstract", "M = 1.125", 1.125, HT["stacked_departures"]["explicit_best"]["best_pairs"][0]["min_M"], A(3), "HT", "modelled")
chk("M_pair_dirsel", "abstract", "becomes 0.97", 0.97, AD["explicit_dirsel"]["all_free+one_lane_one_core"], A(2), "AD", "modelled (derived)")
# ---- section 2 ----
chk("sigma_q", "2", "σ_q = 5.66357", [5.66357, 5.18340],
    [hwrow[("B4x12", 0.001)]["sigma_q"], hwrow[("B8x52", 0.001)]["sigma_q"]], A(5), "HW", "measured")
chk("T_C", "2", "**22.529 s**", [0.1244, 2.688, 0.5535, 22.529],
    [cell[("B4x12", 0.01)]["T_C"], cell[("B4x12", 0.001)]["T_C"], cell[("B8x52", 0.01)]["T_C"], B8["T_C"]],
    R(0.0005), "HT", "measured")
# ---- section 3 ledger ----
chk("sigma_over_e", "3", "11,518.7", 11518.7, B8["sigma_over_e"], A(1), "HT", "modelled (sigma measured)")
chk("D_max", "3", "1,955.9 layers", 1955.9, DN["B8x52_0.001"]["D_max_k1_layers"], A(1), "DN", "modelled")
chk("D_eff_W0", "3", "2,296 layers", 2296, B8["D_eff_primary"]["W0"], A(0), "HT", "modelled")
chk("D_eff_N1", "3", "3,605 layers", 3605, B8["D_eff_primary"]["N1"], A(0), "HT", "modelled")
chk("k10x", "3", "| k_10x | 0.852", 0.852, DN["B8x52_0.001"]["k_10x"], A(3), "DN", "modelled")
chk("k_B8", "3", "682.7 / 197.6 / 7.34 / 8.74", [682.7, 197.6, 7.34, 8.74],
    [B8["k"]["certified"], B8["k"]["explicit_best"], B8["k"]["no_explicit_fail001"], B8["k"]["no_explicit_fail0003"]],
    R(0.0008), "HT", "modelled")
chk("split", "3", "74.8 × 3.10", [74.8, 3.10],
    [DN["M232_split"]["layer_time_factor"], DN["M232_split"]["supply_factor"]], A(1), "DN", "modelled")
chk("t_req_expl", "3", "1.34 ns", 1.34e-9, nec[("explicit_best", "box_muller_current_law")]["t_layer_required_s"], R(0.004), "HW", "modelled")
chk("floor740", "3", "740 layers", 740, nec[("explicit_best", "box_muller_current_law")]["floor_layers"], A(0), "HW", "modelled")
chk("M10ns_B8", "3", "binding-cell M stays\n   232.0", 232.0, B8["M"]["explicit_best"]["t_layer_10ns"], A(1), "HT", "modelled")
chk("M10ns_min", "3", "minimum of 197.8", 197.8, S["explicit_best"]["t_layer_10ns"][0], A(1), "HT", "modelled")
# ---- 4.1 floor ----
chk("compute_depth", "4.1", "| Compute critical path | 270 layers | 278 layers |", [270, 278],
    [fsum["B4x12"]["compute_depth"], fsum["B8x52"]["compute_depth"]], A(0), "DN/FS", "modelled")
chk("compute_T", "4.1", "| T per compute | 2.26e7 | 1.87e8 |", [2.26e7, 1.87e8],
    [fsum["B4x12"]["compute_T"], fsum["B8x52"]["compute_T"]], R(0.003), "DN/FS", "modelled")
chk("bm_share", "4.1", "| 53% | 52% |", [0.53, 0.52],
    [fsum["B4x12"]["box_muller_share_of_compute_path"], fsum["B8x52"]["box_muller_share_of_compute_path"]], A(2), "DN/FS", "modelled")
chk("bm_depth", "4.1", "(144 layers)", 144, fsum["B8x52"]["box_muller_depth"], A(0), "DN/FS", "modelled")
chk("iter_B4", "4.1", "563 layers, reaction-bound", 563, fsum["B4x12"]["W1e7_1e12_100ns"]["D_eff"], A(0), "DN/FS", "modelled")
chk("iter_B8", "4.1", "1,409 layers and 3.61e8 T", [1409, 3.61e8],
    [fsum["B8x52"]["W1e7_1e12_100ns"]["depth"], fsum["B8x52"]["W1e7_1e12_100ns"]["T"]], R(0.002), "DN/FS", "modelled")
chk("iter_B8_unl", "4.1", "585 layers and 1.88e8 T", [585, 1.88e8, 1875, 5.03e7],
    [fsum["B8x52"]["unlimited_1e12_100ns"]["depth"], fsum["B8x52"]["unlimited_1e12_100ns"]["T"],
     fsum["B8x52"]["unlimited_1e12_100ns"]["D_eff"], fsum["B8x52"]["unlimited_1e12_100ns"]["width"]],
    R(0.003), "DN/FS", "modelled")
chk("allfree_path", "4.1", "| 59 layers | 67 layers |", [59, 67],
    [fsum["B4x12"]["all_free_compute_depth"], fsum["B8x52"]["all_free_compute_depth"]], A(0), "DN/FS", "modelled")
D = HT["D_eff_table"]
feas = [k for k in D if D[k]["N1"] is not None]
chk("floor_disagree", "4.1/8/9", "165 of 180", [165, 180],
    [sum(not D[k]["agree_10pct"] for k in feas), len(feas)], A(0), "HT", "modelled")
chk("floor_N1_fav", "4.1", "more favourable in 33 pairs", 33, sum(D[k]["used_from"] == "N1" for k in feas), A(0), "HT", "modelled")
chk("N1_only_M", "4.1", "1,258 (certified), 364.2 (explicit)", [1258, 364.2, 13.5],
    [B8["M_N1_floor_only_primary"]["certified"], B8["M_N1_floor_only_primary"]["explicit_best"],
     B8["M_N1_floor_only_primary"]["no_explicit_fail001"]], R(0.004), "HT", "modelled")
chk("rate_req", "4.1/4.3", "3.3e14", 3.3e14, nec[("explicit_best", "box_muller_current_law")]["T_per_s_required"], R(0.02), "HW", "modelled")
chk("N1_ratio", "8", "1.55-1.57×", [1.55, 1.57],
    [D["B4x12|primary|W1e7|1e12|100ns"]["N1"] / D["B4x12|primary|W1e7|1e12|100ns"]["W0"],
     D["B8x52|primary|W1e7|1e12|100ns"]["N1"] / D["B8x52|primary|W1e7|1e12|100ns"]["W0"]], A(2), "HT", "modelled")
# ---- 4.2 estimator ----
kf = J["KF"]
chk("e07", "4.2", "983,025", 983025, DN["e07_reproduction"]["recomputed"]["calls"], A(0), "DN/KF", "modelled exact")
kk = [r["k_eff"] for r in p1 if r["split"] == "0.45eps"]
chk("cert_range", "4.2", "**585.8-1,066.7**", [585.8, 1066.7], [min(kk), max(kk)], A(1), "ES", "modelled")
kds = [r["k_eff_direction_select"] for r in p1 if r["split"] == "0.45eps"]
chk("cert_dirsel", "4.2", "Certified-schedule k: 293-533", [293, 533], [min(kds), max(kds)], A(0), "ES", "modelled")
cd = [r["calls_direction_select"] for r in p1 if r["eps"] == 0.01 and r["split"] == "0.45eps"]
chk("calls_dirsel", "4.2", "491,520 calls", 491520, cd[0], A(0), "ES", "modelled")
eb = [p2s[c]["W0 explicit best: span+mean+nondyadic"]["k"] for c in p2s]
chk("expl_range", "4.2", "k = 186.6-198.2", [186.6, 198.2], [min(eb), max(eb)], A(1), "ES", "modelled")
nm = [p2s[c]["span+nondyadic (no mean cert)"]["k"] for c in p2s]
chk("no_mean", "4.2", "323-353 without the mean certificate", [323, 353], [min(nm), max(nm)], A(0), "ES", "modelled")
dy = [p2s[c]["span+mean dyadic"]["k"] for c in p2s]
chk("dyadic", "4.2", "195-341 with dyadic M", [195, 341], [min(dy), max(dy)], A(0), "ES", "modelled")
nb = [p2s[c]["N1 best: all credits incl. dirsel"]["k"] for c in p2s]
chk("best_dirsel", "4.2", "Best k: 98-171", [98, 171], [min(nb), max(nb)], A(0), "ES", "modelled")
m7 = [r for r in ES["part7_M_primary"] if r["case"] == "B8x52" and r["eps"] == 0.001][0]
chk("M_dirsel", "4.2", "801.5 → 400.7", [400.7, 200.4], [m7["M_certified_today_dirsel"], m7["M_N1_explicit_best_dirsel"]], A(1), "ES", "modelled")
chk("c_window", "4.2", "c = 4.168", [4.168, 3.502],
    [ES["part4_window_c"]["c_used_N400_from_WS_k"]["0.003"], ES["part4_window_c"]["c_used_N400_from_WS_k"]["0.01"]], A(3), "ES", "modelled")
w = ES["part5_window_k"]
def wr(span, fail):
    v = [r["k_window"] for r in w if r["span"] == span and r["fail"] == fail]
    return [min(v), max(v)]
chk("win_nocred", "4.2", "| 23.5-25.7 |", [23.5, 25.7], wr("64", 0.003), A(1), "ES", "modelled")
chk("win_0003", "4.2", "| 8.25-8.74 |", [8.25, 8.74], wr("8192/211", 0.003), A(2), "ES", "modelled")
chk("win_001", "4.2", "| 6.93-7.34 |", [6.93, 7.34], wr("8192/211", 0.01), A(2), "ES", "modelled")
pk = [r["k"] for r in ES["part5_patel_thm2_randomised_offset"]["rows"]]
chk("patel", "4.2", "k = 6.8e5-9.3e5", [6.8e5, 9.3e5], [min(pk), max(pk)], R(0.01), "ES", "modelled")
gk = [r["k_total"] for r in J["WSK"]["part3_k_lo_methods"] if "Grinko" in r["method"] and r["split"] == "0.45eps"]
chk("grinko", "4.2", "k = 2,997-5,755", [2997, 5755], [min(gk), max(gk)], A(0), "WSK (W0 file, quoted via EC card)", "modelled from literature")
cl = ES["part3_counting_lower_bound"]
def lb(case, key, cls="support [0, 38.818]"):
    v = [r[key] for r in cl if r["case"] == case and r["class"] == cls and r["delta"] == 0.01]  # both splits, as the draft quotes
    return [min(v), max(v)]
chk("lb_B4", "4.2", "k_LB = 1.687-1.696", [1.687, 1.696], lb("B4x12", "k_LB_Q_plus_one_A"), A(3), "ES", "modelled (rigorous)")
chk("lb_B8", "4.2", "1.843-1.853 for B8x52", [1.843, 1.853], lb("B8x52", "k_LB_Q_plus_one_A"), A(3), "ES", "modelled (rigorous)")
chk("lb_AA", "4.2", "0.85 / 0.93", [0.85, 0.93], [lb("B4x12", "k_LB_A_access")[1], lb("B8x52", "k_LB_A_access")[1]], A(2), "ES", "modelled")
mb = [r["k_LB_Q_plus_one_A"] for r in cl if r["class"].startswith("mean") and r["delta"] == 0.01]
chk("lb_mean", "4.2", "0.15-0.16", [0.15, 0.16], [min(mb), max(mb)], ("abs", 0.0051), "ES", "modelled")
ln = {(r["case"], r["supply"]): r["lane_credit"] for r in ES["part6_lanes_W1e7"]["rows"]}
chk("lanes", "4.2", "1.29× for B4x12", [1.00, 1.29, 3.36, 1.00],
    [ln[("B8x52", "supply_1e12")], ln[("B4x12", "supply_1e12")], ln[("B4x12", "unlimited")], ln[("B8x52", "unlimited")]], A(2), "ES", "modelled")
fw = ES["part6_lanes_W1e7"]["floor_design_width_primary"]
chk("lane_width", "4.2", "5.28M qubits wide", [5.28e6, 1.0e7], [fw["B4x12"], fw["B8x52"]], R(0.002), "ES", "modelled")
# ---- 4.3 classical / hardware ----
h16 = {h["cell"]: h for h in HW["classical"]["h16"]}
chk("h16", "4.3", "| B8x52 $0.001 | 10.24× |", [6.44, 9.36, 7.38, 10.24],
    [h16[c]["speedup_16_vs_1"] for c in ("B4x12/0.01", "B4x12/0.001", "B8x52/0.01", "B8x52/0.001")], A(2), "HW", "measured")
pe = [h["parallel_efficiency_16"] for h in h16.values()]
chk("h16_eff", "4.3", "0.40-0.64", [0.40, 0.64], [min(pe), max(pe)], A(2), "HW", "measured")
rv = [h["w16_vs_c2"] - 1 for h in h16.values()]
chk("h16_repro", "4.3", "within\n4-10%", [0.04, 0.10], [min(rv), max(rv)], A(2), "HW", "measured")
chk("M_1lane", "4.3/5.2", "22.7", 22.7, S["explicit_best"]["one_lane_one_core"][0], A(1), "HT", "modelled")
chk("sig_preint", "4.3", "1.248 (B4) and 1.146 (B8)", [1.248, 1.146],
    [hwrow[("B4x12", 0.001)]["sigma_preint"], hwrow[("B8x52", 0.001)]["sigma_preint"]], A(3), "HW", "measured")
pp = HW["classical"]["per_point_cost_s_16w"]
chk("pp_cost", "4.3", "1.15 µs and 10.4 µs", [1.15e-6, 10.4e-6], [pp["B4x12|preint"], pp["B8x52|preint"]], R(0.005), "HW", "measured")
chk("c09", "4.3", "| B8x52 $0.001 | **36.9** |", [40.3, 36.9, 10.6, 18.9],
    [hwrow[(c, e)]["factor_df_over_practice"] for c, e in (("B4x12", 0.001), ("B8x52", 0.001), ("B4x12", 0.01), ("B8x52", 0.01))],
    A(1), "HW", "modelled from measured")
chk("M_df", "4.3", "| Box-Muller | 21.7 | **6.29** |", [21.7, 6.29, 1.08, 0.31],
    [hwmin["box_muller_current_law|certified_today"]["min_M_distfree"], hwmin["box_muller_current_law|explicit_best"]["min_M_distfree"],
     hwmin["all_free_and_narrow|certified_today"]["min_M_distfree"], hwmin["all_free_and_narrow|explicit_best"]["min_M_distfree"]],
    ("abs", 0.051), "HW", "modelled")
anc = {a["id"]: a for a in HW["anchors_time"]}
chk("anchors", "4.3", "| 446 ns | 4.5× |", [446e-9, 550e-9, 1.1e-6, 1e-6, 1e-5, 2.5e-5],
    [anc[i]["value_s"] for i in ("A02", "A01", "A03a", "A04a", "A04b", "A04c")], R(0.001), "HW", "literature")
n_c = nec[("certified_today", "box_muller_current_law")]
n_w = nec[("no_explicit_constant", "box_muller_current_law")]
n_af = nec[("explicit_best", "all_free_and_narrow")]
chk("nec_table", "4.3", "| Explicit constant, all-free floor | 8.8 ns | 1.3e13 T/s | 1.85e6 qubits |",
    [0.39e-9, 1.1e15, 36e-9, 1.2e13, 8.8e-9, 1.3e13, 1.85e6],
    [n_c["t_layer_required_s"], n_c["T_per_s_required"], n_w["t_layer_required_s"], n_w["T_per_s_required"],
     n_af["t_layer_required_s"], n_af["T_per_s_required"], n_af["logical_width"]], R(0.04), "HW", "modelled")
chk("nec_326", "4.3", "326× the budget", 326, nec[("explicit_best", "box_muller_current_law")]["T_per_s_required_over_budget"], A(0), "HW", "modelled")
ar = {a["id"]: a["value"] for a in HW["anchors_rate"] + HW["anchors_width"]}
chk("rate_anchors", "4.3", "about 2.4e5 CCZ/s", [2.4e5, 3e4, 48], [ar["A04d"], ar["A05b"], ar["A09"]], R(0.05), "HW", "literature (derived)")
# ---- 5.2 / 5.3 ----
E = S["explicit_best"]
chk("dep_table", "5.2", "| All-free oracle (free loader and exponential, narrow words) | 11.5 |",
    [11.5, 46.4, 116.0, 74.8, 104.4, 189.5, 318.0, 1978, 648, 748, 7476],
    [E["all_free_oracle"][0], E["distfree_x5"][0], E["distfree_x2"][0], E["supply_1e13"][0], E["e_eq_eps"][0],
     E["width_W1e8"][0], E["primary_B8_0.001_ineligible"][0], E["supply_1e11"][0], E["width_W1e6"][0],
     E["t_layer_1us"][0], E["t_layer_10us"][0]], ("abs", 0.51), "HT", "modelled")
chk("dep_fail001", "5.2", "| Estimator failure 0.01 | 170.1 |", 170.1, S["explicit_best_fail001"]["primary"][0], A(1), "HT", "modelled")
chk("win_dep", "5.2", "0.43 at failure 0.01, or 0.51 at 0.003", [0.43, 0.51, 0.84, 1.002],
    [S["no_explicit_fail001"]["all_free_oracle"][0], S["no_explicit_fail0003"]["all_free_oracle"][0],
     S["no_explicit_fail001"]["one_lane_one_core"][0], S["no_explicit_fail0003"]["one_lane_one_core"][0]], A(2), "HT", "modelled")
ms = HT["stacked_departures"]["explicit_best"]["minimal_sets"]
chk("stack3", "5.3", "| All-free + 1 lane vs 1 core + distribution-free ×5 | 0.225 |",
    [0.225, 0.506, 0.714, 0.825], [m["min_M"] for m in ms], A(3), "HT", "modelled")
chk("cert_stack", "5.3", "gives 0.777", [0.777, 3.89], [sdc["minimal_sets"][0]["min_M"], sdc["best_pairs"][0]["min_M"]], A(2), "HT", "modelled")
chk("ad_table", "5.3", "| All-free + distribution-free (Stage C), certified schedule | 0.54 |", [0.97, 0.27, 0.54],
    [AD["explicit_dirsel"]["all_free+one_lane_one_core"], AD["explicit_dirsel"]["all_free+distfree_stageC"],
     AD["certified_dirsel"]["all_free+distfree_stageC"]], A(2), "AD", "modelled (derived)")
# ---- section 9 / appendix ----
tc03 = HT["T_C"]["B4x12|0.03"]
chk("quirk", "9", "0.12677 s", [0.12677, 0.12440], [tc03["raw_best"]["t"], tc03["T_C"]], A(5), "HT", "measured")
chk("W1e6", "9", "D_eff of 11,034", 11034, D["B8x52|primary|W1e6|1e12|100ns"]["W0"], A(0), "HT", "modelled")
chk("persist", "9", "3.4e6\n    qubits", 3.4e6, fsum["B8x52"]["persistent_outputs"], R(0.02), "DN/FS", "modelled")
import collections
tiers = collections.Counter(i["tier"] for i in J["REG"]["items"])
chk("register", "App A", "| T6 | Parked as a different task | 25 |", [4, 8, 12, 26, 35, 25],
    [tiers[t] for t in ("T1", "T2", "T3", "T4", "T5", "T6")], A(0), "REG (W0)", "register record")
t6 = sorted(i["id"] for i in J["REG"]["items"] if i["tier"] == "T6")
exp_t6 = ["E10"] + ["E%d" % i for i in range(14, 20)] + ["F%02d" % i for i in range(9, 20)] + ["F21", "F22"] + \
         ["F%d" % i for i in range(26, 30)] + ["F32"]
results.append({"id": "T6_list", "where": "7", "match": sorted(exp_t6) == t6, "quoted": exp_t6, "file_value": t6,
                "source": "REG", "label": "register record", "snippet": "E10, E14-E19", "snippet_in_draft": "E10, E14-E19" in draft})
disp = {i["id"]: (i["tier"], i["disposition"]) for i in J["REG"]["items"]}
results.append({"id": "closed_escapes_dispositions", "where": "7/App A", "match": all(disp[x][0] == "T4" for x in ("E22", "C12", "F04", "F05", "F20")),
                "quoted": "listed as closed escapes", "file_value": {x: disp[x] for x in ("E22", "C12", "F04", "F05", "F20", "C14")},
                "source": "REG", "label": "register record", "snippet": "**§7 (closed escapes):** E22, C12, F04, F05 and F20",
                "snippet_in_draft": "**§7 (closed escapes):** E22, C12, F04, F05 and F20" in draft})

# ---- derived reviewer quantities (modelled; used in REVIEW.md) ----
k10 = DN["B8x52_0.001"]["k_10x"]
kexp = B8["k"]["explicit_best"]
D_used = B8["D_eff_primary"]["used"]
derived = {
    "explicit_M_le_1_needs_D_eff_layers_at_most": D_used / (kexp / k10),
    "explicit_M_le_1_needs_T_per_iterate_at_most_at_1e12_100ns": D_used / (kexp / k10) * 1e12 * 1e-7,
    "W0_all_free_D_eff_B8": D["B8x52|all_free|W1e7|1e12|100ns"]["W0"],
    "factor_below_all_free_floor_needed": D["B8x52|all_free|W1e7|1e12|100ns"]["W0"] / (D_used / (kexp / k10)),
    "no_mean_cert_k_B8_0.001": p2s[("B8x52", 0.001)]["span+nondyadic (no mean cert)"]["k"],
    "distfree_M_without_U1_mean_credit_BM": hwmin["box_muller_current_law|explicit_best"]["min_M_distfree"]
        * p2s[("B8x52", 0.001)]["span+nondyadic (no mean cert)"]["k"] / kexp,
    "distfree_M_without_U1_mean_credit_allfree": hwmin["all_free_and_narrow|explicit_best"]["min_M_distfree"]
        * p2s[("B8x52", 0.001)]["span+nondyadic (no mean cert)"]["k"] / kexp,
    "e_eq_eps_explicit_M_B8": B8["M"]["explicit_best"]["e_eq_eps"],
    "N1_floor_allfree_D_eff_B8": D["B8x52|all_free|W1e7|1e12|100ns"]["N1"],
    "iid_CLT_points_B8_0.001_over_EB_points": ((2.5758293035489 * hwrow[("B8x52", 0.001)]["sigma_preint"] / 0.00045) ** 2)
        / (HW["classical"]["rows"][4]["routes"]["S40"]["iid_preint_EB"]["n"]),
    "practice_points_B8_0.001": hwrow[("B8x52", 0.001)]["practice_points"],
    "EB_points_B8_0.001": hwrow[("B8x52", 0.001)]["routes"]["S40"]["iid_preint_EB"]["n"],
}

fails = [r for r in results if not r["match"] or not r["snippet_in_draft"]]
out = {
    "meta": {"script": "research/plan110_n1/review/check_draft.py", "python": sys.version,
             "flags": {"isolated": sys.flags.isolated, "no_site": sys.flags.no_site},
             "inputs_sha256": {**{k: sha(p) for k, p in F.items()}, "draft": sha(DRAFT)},
             "label": "checks compare quoted draft numbers to file values; derived values are modelled arithmetic on N1 values"},
    "n_checks": len(results), "n_fail_or_missing_snippet": len(fails),
    "checks": results, "derived_for_review": derived,
}
with open(OUT, "x", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1)
with open(ROWS, "a", encoding="utf-8") as fh:
    for r in fails:
        fh.write(json.dumps({"ws": "n2_review", "sub": "number_check_flag", "value": r, "label": r["label"],
                             "direction": "n/a (check)", "source": OUT}) + "\n")
    fh.write(json.dumps({"ws": "n2_review", "sub": "number_check_summary",
                         "value": {"n_checks": len(results), "n_flagged": len(fails),
                                   "flagged_ids": [r["id"] for r in fails]},
                         "label": "check", "direction": "n/a", "source": OUT}) + "\n")
    fh.write(json.dumps({"ws": "n2_review", "sub": "derived_for_review", "value": derived,
                         "label": "modelled (arithmetic on N1 values)", "direction": "see REVIEW.md", "source": OUT}) + "\n")
print("checks", len(results), "flagged", len(fails))
for r in fails:
    print("FLAG", r["id"], "snippet_in_draft=", r["snippet_in_draft"], "quoted=", r["quoted"], "file=", r["file_value"])
print(json.dumps(derived, indent=1))
