"""v3 self-check for manuscript/advantage-frontier-2026-09-23/FRONTIER_NEGATIVE_RESULT_DRAFT_v3.md.

Copied from research/plan110_n1/recheck/recheck_draft.py (the N2 re-check of v2) and adapted:
  (a) Part 0: v1 and v2 SHA-256 are unchanged (v1 3d8e5900...c62b1c, v2 51dcf89b...8132d00);
  (b) Part 6: each N3-1..N3-8 target phrase from results/plan110_n1/recheck/RECHECK.md is
      gone from the v3 body (text before the first "## Changelog") and its correction is
      present (whitespace-normalised matching);
  (c) Parts 1-3: the re-check's 129 number / text / register checks, now run against v3
      (only the snippet of `dirsel_k_expl_b8` changes, because N3-8 replaces "n/a" by 170.7);
      Part 4: the re-check probes re-computed and compared with number_recheck.json;
      Part 5: every number v3 adds, re-derived here from the primary N1 / W0 files, with the
      re-check probe value and the v3_numbers.json value kept as extra columns.
A unified diff v2 -> v3 is written alongside.

Run from the repo root:
  .context/frontier_t0_env/Scripts/python.exe -I -S -B research/plan110_n1/v3/check_v3.py
  (add --dry to print results without writing any files)

stdlib only. Outputs (exclusive create): results/plan110_n1/v3/check_v3.json and
results/plan110_n1/v3/v2_to_v3.diff. Rows are appended to results/plan110_n1/v3/rows.jsonl.
Labels: each check keeps the source label of the file value (measured / modelled /
assumed / literature); derived values are "modelled (derived)".
"""
import difflib
import re
import collections
import hashlib
import json
import statistics
import sys

V1 = "manuscript/advantage-frontier-2026-09-23/FRONTIER_NEGATIVE_RESULT_DRAFT.md"
V2 = "manuscript/advantage-frontier-2026-09-23/FRONTIER_NEGATIVE_RESULT_DRAFT_v2.md"
V3 = "manuscript/advantage-frontier-2026-09-23/FRONTIER_NEGATIVE_RESULT_DRAFT_v3.md"
V1_SHA = "3d8e590044016b3208402e7e16a76e49eabe14ec01081ebfba08938221c62b1c"
V2_SHA = "51dcf89b8ad127187843a1e734e2a9e7f59f45dc4b7d66571100ece5b8132d00"
RK_PATH = "results/plan110_n1/recheck/number_recheck.json"
V3N_PATH = "results/plan110_n1/v3/v3_numbers.json"
F = {
    "HT": "results/plan110_n1/headline/headline_table.json",
    "KF": "results/plan110_n1/headline/keff.json",
    "FS": "results/plan110_n1/headline/floor_sheet.json",
    "ES": "results/plan110_n1/estimator/estimator_recompute.json",
    "HW": "results/plan110_n1/hwclassical/hw_classical_card_v2.json",
    "DN": "results/plan110_n1/drafter/draft_numbers.json",
    "AD": "results/plan110_n1/drafter/addendum.json",
    "DC": "results/plan110_n1/review/dirsel_confirm.json",
    "NC": "results/plan110_n1/review/number_check.json",
    "FX": "results/plan110_n1/fixer/fixer_numbers.json",
    "FX2": "results/plan110_n1/fixer/fixer_numbers_2.json",
    "REG": "results/plan110_w0/register/run001/register.json",
    "WSK": "results/plan110_w0/ws_k/k_bracket.json",
    "BD": "results/plan110_w0/ws_small/bias_desk_run001/bias_desk.json",
}
DP1 = "docs/program_plan_20261010/DP1_MEMO.md"
OUT = "results/plan110_n1/v3/check_v3.json"
DIFF = "results/plan110_n1/v3/v2_to_v3.diff"
ROWS = "results/plan110_n1/v3/rows.jsonl"


def sha(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


DRY = "--dry" in sys.argv  # dry run: no files written


def row(sub, value, label="check", direction="n/a"):
    if DRY:
        return
    with open(ROWS, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"ws": "v3_check", "sub": sub, "value": value, "label": label,
                             "direction": direction}, default=str) + "\n")


J = {k: json.load(open(p, encoding="utf-8")) for k, p in F.items()}
draft = open(V3, encoding="utf-8").read()
v2_text = open(V2, encoding="utf-8").read()
RK = json.load(open(RK_PATH, encoding="utf-8"))
V3N = json.load(open(V3N_PATH, encoding="utf-8"))
dp1 = open(DP1, encoding="utf-8").read()
HT, ES, HW, DN, AD, DC, FX, FX2 = (J[k] for k in ("HT", "ES", "HW", "DN", "AD", "DC", "FX", "FX2"))
S = HT["summary_min_M_eligible_non_overhead"]
cell = {(c["case"], c["eps"]): c for c in HT["cells"]}
B8 = cell[("B8x52", 0.001)]
hwmin = HW["classical"]["M_minima"]
hwrow = {(r["case"], r["eps"]): r for r in HW["classical"]["rows"]}
nec = {(n["k_class"], n["floor_design"]): n for n in HW["necessary_conditions"]
       if n["case"] == "B8x52" and n["eps"] == 0.001}
sdc = HT["stacked_departures"]["certified"]
fsum = DN["floor_sheet_summary"]
p1 = ES["part1_k_eff_today"]
p2s = {(r["case"], r["eps"]): r for r in ES["part2_summary"]}
D = HT["D_eff_table"]
T_LAYER, SUPPLY = 1e-7, 1e12

results = []


def _ok(q, a, tol):
    if a is None:
        return False
    kind, x = tol
    if kind == "sig":  # quoted value equals the file value rounded to x significant figures
        return q == float(f"{a:.{x}g}")
    if kind == "abs":
        return abs(q - a) <= x * 1.0000001
    return abs(q - a) <= x * abs(a)


def chk(cid, where, snippet, quoted, actual, tol, src, label, fixer=None):
    present = snippet in draft
    if isinstance(actual, (list, tuple)):
        tols = [(tol[0], x) for x in tol[1]] if isinstance(tol[1], list) else [tol] * len(actual)
        ok = len(quoted) == len(actual) and all(_ok(q, a, t) for q, a, t in zip(quoted, actual, tols))
    else:
        ok = _ok(quoted, actual, tol)
    r = {"id": cid, "where": where, "snippet": snippet, "snippet_in_v3": present,
         "quoted": quoted, "file_value": actual, "tol": tol, "match": ok,
         "source": src, "label": label}
    if fixer is not None:
        r["fixer_value"] = fixer
    results.append(r)


A = lambda nd: ("abs", 0.5 * 10 ** (-nd))
G = lambda n: ("sig", n)
R = lambda r: ("rel", r)

# =====================================================================
# Part 1: numbers carried from v1 (same checks as the re-check; v3 snippets)
# =====================================================================
chk("M_cert", "abstract/3/5.1", "**801.5**", 801.5, S["certified"]["primary"][0], A(1), "HT", "modelled")
chk("M_expl", "abstract/3/5.1", "**232.0**", 232.0, S["explicit_best"]["primary"][0], A(1), "HT", "modelled")
chk("M_win001", "abstract", "**8.62** (failure 0.01)", 8.62, S["no_explicit_fail001"]["primary"][0], A(2), "HT", "modelled")
chk("M_win0003", "abstract/3", "10.26 (failure 0.003, like for like)", 10.26, S["no_explicit_fail0003"]["primary"][0], A(2), "HT", "modelled")
chk("M_allfree_distfree", "abstract", "gives M = 0.31", 0.31, hwmin["all_free_and_narrow|explicit_best"]["min_M_distfree"], A(2), "HW", "modelled")
chk("M_pair", "abstract", "M = 1.125, or 0.97 with direction-select", [1.125, 0.97],
    [HT["stacked_departures"]["explicit_best"]["best_pairs"][0]["min_M"], AD["explicit_dirsel"]["all_free+one_lane_one_core"]],
    A(2), "HT/AD", "modelled")
chk("sigma_q", "2", "σ_q = 5.66357", [5.66357, 5.18340],
    [hwrow[("B4x12", 0.001)]["sigma_q"], hwrow[("B8x52", 0.001)]["sigma_q"]], A(5), "HW", "measured")
chk("T_C", "2", "| B8x52 $0.001 | **22.529 s** |", [0.1244, 2.688, 0.5535, 22.529],
    [cell[("B4x12", 0.01)]["T_C"], cell[("B4x12", 0.001)]["T_C"], cell[("B8x52", 0.01)]["T_C"], B8["T_C"]],
    R(0.0005), "HT", "measured")
chk("sigma_over_e", "3", "11,518.7 = 5.18340 / (0.45 × $0.001)", 11518.7, B8["sigma_over_e"], A(1), "HT", "modelled (sigma measured)")
D_max = B8["T_C"] / (10 * B8["sigma_over_e"] * T_LAYER)
chk("D_max", "3", "| D_max(k=1) | 1,955.9 layers |", 1955.9, D_max, A(1), "HT (re-derived)", "modelled")
chk("D_eff_W0", "3", "2,296 layers, supply-bound", 2296, B8["D_eff_primary"]["W0"], A(0), "HT", "modelled")
chk("D_eff_N1", "3", "3,605 layers, supply-bound", 3605, B8["D_eff_primary"]["N1"], A(0), "HT", "modelled")
k10 = D_max / B8["D_eff_primary"]["used"]
chk("k10x", "3", "| k_10x | 0.852 |", 0.852, k10, A(3), "HT (re-derived)", "modelled")
chk("k_B8", "3", "682.7 / 197.6 / 7.34 / 8.74", [682.7, 197.6, 7.34, 8.74],
    [B8["k"]["certified"], B8["k"]["explicit_best"], B8["k"]["no_explicit_fail001"], B8["k"]["no_explicit_fail0003"]],
    R(0.0008), "HT", "modelled")
chk("M_ledger", "3", "**801.5 / 232.0 / 8.62 / 10.26**", [801.5, 232.0, 8.62, 10.26],
    [S["certified"]["primary"][0], S["explicit_best"]["primary"][0], S["no_explicit_fail001"]["primary"][0],
     S["no_explicit_fail0003"]["primary"][0]], R(0.0007), "HT", "modelled")
chk("split", "3", "M = 232.0 = 74.8 × 3.10", [74.8, 3.10],
    [S["explicit_best"]["supply_1e13"][0], S["explicit_best"]["primary"][0] / S["explicit_best"]["supply_1e13"][0]],
    G(3), "HT (re-derived)", "modelled", fixer=[FX["d11_split"]["M_supply_1e13"], FX["d11_split"]["supply_factor"]])
chk("t_req_expl", "3", "1.34 ns layer", 1.34e-9, nec[("explicit_best", "box_muller_current_law")]["t_layer_required_s"], R(0.004), "HW", "modelled")
chk("t_req_expl_2", "3 (re-derived)", "1.34 ns layer", 1.34, 100 / S["explicit_best"]["supply_1e13"][0], A(2), "HT", "modelled")
chk("floor740", "3", "740-layer Box-Muller floor", 740, nec[("explicit_best", "box_muller_current_law")]["floor_layers"], A(0), "HW", "modelled")
chk("M10ns_B8", "3", "At 10 ns the binding-cell M stays\n   232.0", 232.0, B8["M"]["explicit_best"]["t_layer_10ns"], A(1), "HT", "modelled")
chk("M10ns_min", "3", "to a minimum of 197.8", 197.8, S["explicit_best"]["t_layer_10ns"][0], A(1), "HT", "modelled")
chk("compute_depth", "4.1", "| Compute critical path | 270 layers | 278 layers |", [270, 278],
    [fsum["B4x12"]["compute_depth"], fsum["B8x52"]["compute_depth"]], A(0), "DN/FS", "modelled")
chk("compute_T", "4.1", "| T per compute | 2.26e7 | 1.87e8 |", [2.26e7, 1.87e8],
    [fsum["B4x12"]["compute_T"], fsum["B8x52"]["compute_T"]], R(0.003), "DN/FS", "modelled")
chk("bm_share", "4.1", "(144 layers) | 53% | 52% |", [0.53, 0.52],
    [fsum["B4x12"]["box_muller_share_of_compute_path"], fsum["B8x52"]["box_muller_share_of_compute_path"]], A(2), "DN/FS", "modelled")
chk("bm_depth", "4.1", "(144 layers)", 144, fsum["B8x52"]["box_muller_depth"], A(0), "DN/FS", "modelled")
chk("iter_B4", "4.1", "563 layers, reaction-bound", 563, fsum["B4x12"]["W1e7_1e12_100ns"]["D_eff"], A(0), "DN/FS", "modelled")
chk("iter_B8", "4.1", "1,409 layers and 3.61e8 T", [1409, 3.61e8],
    [fsum["B8x52"]["W1e7_1e12_100ns"]["depth"], fsum["B8x52"]["W1e7_1e12_100ns"]["T"]], R(0.002), "DN/FS", "modelled")
chk("iter_B8_unl", "4.1", "585 layers and 1.88e8 T: supply-bound, D_eff = 1,875 (5.03e7 qubits)", [585, 1.88e8, 1875, 5.03e7],
    [fsum["B8x52"]["unlimited_1e12_100ns"]["depth"], fsum["B8x52"]["unlimited_1e12_100ns"]["T"],
     fsum["B8x52"]["unlimited_1e12_100ns"]["D_eff"], fsum["B8x52"]["unlimited_1e12_100ns"]["width"]],
    R(0.003), "DN/FS", "modelled")
chk("allfree_path", "4.1", "| 59 layers | 67 layers |", [59, 67],
    [fsum["B4x12"]["all_free_compute_depth"], fsum["B8x52"]["all_free_compute_depth"]], A(0), "DN/FS", "modelled")
feas = [k for k in D if D[k]["N1"] is not None]
chk("floor_disagree", "4.1/8/9", "165 of 180", [165, 180],
    [sum(not D[k]["agree_10pct"] for k in feas), len(feas)], A(0), "HT", "modelled")
chk("floor_N1_fav", "4.1", "more favourable in 33 pairs", 33, sum(D[k]["used_from"] == "N1" for k in feas), A(0), "HT", "modelled")
chk("floor_B4_vs", "4.1", "563 against 364 (B4x12)", [563, 364],
    [D["B4x12|primary|W1e7|1e12|100ns"]["N1"], D["B4x12|primary|W1e7|1e12|100ns"]["W0"]], A(0), "HT", "modelled")
chk("floor_ratio", "4.1", "ratios 1.547× and 1.570×", [1.547, 1.570],
    [D["B4x12|primary|W1e7|1e12|100ns"]["N1"] / D["B4x12|primary|W1e7|1e12|100ns"]["W0"],
     D["B8x52|primary|W1e7|1e12|100ns"]["N1"] / D["B8x52|primary|W1e7|1e12|100ns"]["W0"]], A(3), "HT", "modelled")
chk("floor_ratio_8", "8", "1.55-1.57×", [1.55, 1.57],
    [D["B4x12|primary|W1e7|1e12|100ns"]["N1"] / D["B4x12|primary|W1e7|1e12|100ns"]["W0"],
     D["B8x52|primary|W1e7|1e12|100ns"]["N1"] / D["B8x52|primary|W1e7|1e12|100ns"]["W0"]], A(2), "HT", "modelled")
chk("N1_unl", "4.1", "1,875 against 2,296", [1875, 2296],
    [D["B8x52|primary|unlimited|1e12|100ns"]["N1"] if "B8x52|primary|unlimited|1e12|100ns" in D else None,
     D["B8x52|primary|W1e7|1e12|100ns"]["W0"]], A(0), "HT", "modelled")
chk("N1_only_M", "4.1", "1,258 (certified), 364.2\n  (explicit) and 13.5", [1258, 364.2, 13.5],
    [B8["M_N1_floor_only_primary"]["certified"], B8["M_N1_floor_only_primary"]["explicit_best"],
     B8["M_N1_floor_only_primary"]["no_explicit_fail001"]], R(0.004), "HT", "modelled")
chk("N1_only_M_abs", "abstract", "M is 1,258 / 364 / 13.5", [1258, 364, 13.5],
    [B8["M_N1_floor_only_primary"]["certified"], B8["M_N1_floor_only_primary"]["explicit_best"],
     B8["M_N1_floor_only_primary"]["no_explicit_fail001"]], R(0.004), "HT", "modelled")
chk("rate_req", "4.1/4.3", "3.3e14 T/s", 3.3e14, nec[("explicit_best", "box_muller_current_law")]["T_per_s_required"], R(0.02), "HW", "modelled")
chk("e07", "4.2", "983,025\n  controlled Grover calls", 983025, DN["e07_reproduction"]["recomputed"]["calls"], A(0), "DN/KF", "modelled exact")
kk = [r["k_eff"] for r in p1 if r["split"] == "0.45eps"]
chk("cert_range", "4.2", "**585.8-1,066.7**", [585.8, 1066.7], [min(kk), max(kk)], A(1), "ES", "modelled")
kds = [r["k_eff_direction_select"] for r in p1 if r["split"] == "0.45eps"]
chk("cert_dirsel", "4.2", "Certified-schedule k: 293-533", [293, 533], [min(kds), max(kds)], A(0), "ES", "modelled")
kds_b8 = [r["k_eff_direction_select"] for r in p1 if r["split"] == "0.45eps" and r["case"] == "B8x52" and r["eps"] == 0.001][0]
chk("cert_dirsel_b8", "4.2/5.1", "341.4 at the binding cell", 341.4, kds_b8, A(1), "ES", "modelled")
cd = [r["calls_direction_select"] for r in p1 if r["eps"] == 0.01 and r["split"] == "0.45eps"]
chk("calls_dirsel", "4.2", "491,520 calls", 491520, cd[0], A(0), "ES", "modelled")
eb = [p2s[c]["W0 explicit best: span+mean+nondyadic"]["k"] for c in p2s]
chk("expl_range", "4.2", "k = 186.6-198.2", [186.6, 198.2], [min(eb), max(eb)], A(1), "ES", "modelled")
nm = [p2s[c]["span+nondyadic (no mean cert)"]["k"] for c in p2s]
chk("no_mean", "4.2", "323-353 without the mean certificate (353.0 at the binding cell)", [323, 353, 353.0],
    [min(nm), max(nm), p2s[("B8x52", 0.001)]["span+nondyadic (no mean cert)"]["k"]], A(0), "ES", "modelled")
dy = [p2s[c]["span+mean dyadic"]["k"] for c in p2s]
chk("dyadic", "4.2", "195-341 with dyadic M", [195, 341], [min(dy), max(dy)], A(0), "ES", "modelled")
nb = [p2s[c]["N1 best: all credits incl. dirsel"]["k"] for c in p2s]
chk("best_dirsel", "4.2", "Best k: 98-171", [98, 171], [min(nb), max(nb)], A(0), "ES", "modelled")
m7 = [r for r in ES["part7_M_primary"] if r["case"] == "B8x52" and r["eps"] == 0.001][0]
chk("M_dirsel", "4.2", "801.5 → 400.7 (certified) and 232.0 → 200.4", [400.7, 200.4],
    [m7["M_certified_today_dirsel"], m7["M_N1_explicit_best_dirsel"]], A(1), "ES", "modelled")
chk("c_window", "4.2", "c = 4.168 at δ = 0.003 and 3.502 at δ = 0.01", [4.168, 3.502],
    [ES["part4_window_c"]["c_used_N400_from_WS_k"]["0.003"], ES["part4_window_c"]["c_used_N400_from_WS_k"]["0.01"]], A(3), "ES", "modelled")
cN = sorted({x["N"] for x in ES["part4_window_c"]["rows"]})
results.append({"id": "c_window_N", "where": "4.2", "snippet": "only at N = 50, 100 and 200",
                "snippet_in_v3": "only at N = 50, 100 and 200" in draft, "quoted": [50, 100, 200], "file_value": cN,
                "match": cN == [50, 100, 200], "source": "ES", "label": "modelled"})
w = ES["part5_window_k"]


def wr(span, fail, case=None, eps=None):
    v = [r["k_window"] for r in w if r["span"] == span and r["fail"] == fail
         and (case is None or r["case"] == case) and (eps is None or r["eps"] == eps)
         and (span == "64" or r["mean"] == "price+L1")]
    return [min(v), max(v)]


chk("win_nocred", "4.2", "| 23.5-25.7 |", [23.5, 25.7], wr("64", 0.003), A(1), "ES", "modelled")
chk("win_0003", "4.2", "| 8.25-8.77 | 8.25 / 8.74 |", [8.25, 8.77, 8.25, 8.74],
    wr("8192/211", 0.003) + [wr("8192/211", 0.003, "B4x12", 0.001)[0], wr("8192/211", 0.003, "B8x52", 0.001)[0]],
    A(2), "ES", "modelled")
chk("win_001", "4.2", "| 6.93-7.37 | 6.93 / 7.34 |", [6.93, 7.37, 6.93, 7.34],
    wr("8192/211", 0.01) + [wr("8192/211", 0.01, "B4x12", 0.001)[0], wr("8192/211", 0.01, "B8x52", 0.001)[0]],
    A(2), "ES", "modelled")
pk = [r["k"] for r in ES["part5_patel_thm2_randomised_offset"]["rows"]]
chk("patel", "4.2", "k = 6.8e5-9.3e5", [6.8e5, 9.3e5], [min(pk), max(pk)], R(0.01), "ES", "modelled")
gk = [r["k_total"] for r in J["WSK"]["part3_k_lo_methods"] if "Grinko" in r["method"] and r["split"] == "0.45eps"]
chk("grinko", "4.2", "k = 2,997-5,755", [2997, 5755], [min(gk), max(gk)], A(0), "WSK via EC", "modelled from literature")
cl = ES["part3_counting_lower_bound"]


def lb(case, key, split=None, cls="support [0, 38.818]"):
    v = [r[key] for r in cl if r["case"] == case and r["class"] == cls and r["delta"] == 0.01
         and (split is None or r["split"] == split)]
    return [min(v), max(v)]


chk("lb_B4_prim", "4.2", "k_LB = 1.691-1.696 for B4x12", [1.691, 1.696], lb("B4x12", "k_LB_Q_plus_one_A", "0.45eps"), A(3), "ES", "modelled (rigorous)")
chk("lb_B8_prim", "4.2", "1.848-1.853 for B8x52", [1.848, 1.853], lb("B8x52", "k_LB_Q_plus_one_A", "0.45eps"), A(3), "ES", "modelled (rigorous)")
chk("lb_both", "4.2", "1.687-1.696 and 1.843-1.853", [1.687, 1.696, 1.843, 1.853],
    lb("B4x12", "k_LB_Q_plus_one_A") + lb("B8x52", "k_LB_Q_plus_one_A"), A(3), "ES", "modelled (rigorous)")
chk("lb_AA", "4.2", "halves to 0.85 / 0.93", [0.85, 0.93], [lb("B4x12", "k_LB_A_access")[1], lb("B8x52", "k_LB_A_access")[1]], A(2), "ES", "modelled")
mb_p = [r["k_LB_Q_plus_one_A"] for r in cl if r["class"].startswith("mean") and r["delta"] == 0.01 and r["split"] == "0.45eps"]
mb_b = [r["k_LB_Q_plus_one_A"] for r in cl if r["class"].startswith("mean") and r["delta"] == 0.01]
chk("lb_mean", "4.2", "0.15-0.16 at the primary split (0.14-0.16 over both", [0.15, 0.16, 0.14, 0.16],
    [min(mb_p), max(mb_p), min(mb_b), max(mb_b)], A(2), "ES", "modelled")
allk = [r[kk2] for r in cl for kk2 in r if kk2.startswith("k_LB") and isinstance(r[kk2], (int, float))]
chk("lb_lowest", "4.2", "the lowest value in any cell or access model is 0.074", 0.074, min(allk), A(3), "ES", "modelled")
ln = {(r["case"], r["supply"]): r["lane_credit"] for r in ES["part6_lanes_W1e7"]["rows"]}
chk("lanes", "4.2", "1.29× for B4x12", [1.00, 1.29, 3.36, 1.00],
    [ln[("B8x52", "supply_1e12")], ln[("B4x12", "supply_1e12")], ln[("B4x12", "unlimited")], ln[("B8x52", "unlimited")]], A(2), "ES", "modelled")
fw = ES["part6_lanes_W1e7"]["floor_design_width_primary"]
chk("lane_width", "4.2", "5.28M\n  qubits wide (B4x12) and 10M wide", [5.28e6, 1.0e7], [fw["B4x12"], fw["B8x52"]], R(0.002), "ES", "modelled")
h16 = {h["cell"]: h for h in HW["classical"]["h16"]}
chk("h16", "4.3", "| B8x52 $0.001 | 10.24× |", [6.44, 9.36, 7.38, 10.24],
    [h16[c]["speedup_16_vs_1"] for c in ("B4x12/0.01", "B4x12/0.001", "B8x52/0.01", "B8x52/0.001")], A(2), "HW", "measured")
pe = [h["parallel_efficiency_16"] for h in h16.values()]
chk("h16_eff", "4.3", "0.40-0.64", [0.40, 0.64], [min(pe), max(pe)], A(2), "HW", "measured")
rv = [h["w16_vs_c2"] - 1 for h in h16.values()]
chk("h16_repro", "4.3", "within\n4-10%", [0.04, 0.10], [min(rv), max(rv)], A(2), "HW", "measured")
chk("M_1lane", "4.3/5.2", "The minimum explicit M becomes 22.7", 22.7, S["explicit_best"]["one_lane_one_core"][0], A(1), "HT", "modelled")
tcsrc = {k2: HT["T_C"][k2]["raw_best"] for k2 in ("B4x12|0.01", "B4x12|0.001", "B8x52|0.01", "B8x52|0.001")}
results.append({"id": "TC_is_preint", "where": "4.3 direction note", "snippet": "In all four decision cells T_C is `preint`",
                "snippet_in_v3": "In all four decision cells T_C is `preint`" in draft, "quoted": "preint in all four",
                "file_value": tcsrc, "match": all("preint" in json.dumps(v) for v in tcsrc.values()),
                "source": "HT", "label": "measured"})
chk("sig_preint", "4.3", "1.248 (B4) and 1.146 (B8)", [1.248, 1.146],
    [hwrow[("B4x12", 0.001)]["sigma_preint"], hwrow[("B8x52", 0.001)]["sigma_preint"]], A(3), "HW", "measured")
pp = HW["classical"]["per_point_cost_s_16w"]
chk("pp_cost", "4.3", "1.15 µs and 10.4 µs", [1.15e-6, 10.4e-6], [pp["B4x12|preint"], pp["B8x52|preint"]], R(0.005), "HW", "measured")
chk("c09", "4.3", "| B8x52 $0.001 | **36.9** |", [40.3, 36.9, 10.6, 18.9],
    [hwrow[(c, e)]["factor_df_over_practice"] for c, e in (("B4x12", 0.001), ("B8x52", 0.001), ("B4x12", 0.01), ("B8x52", 0.01))],
    A(1), "HW", "modelled from measured")
anc = {a["id"]: a for a in HW["anchors_time"]}
chk("anchors", "4.3", "| 446 ns | 4.5× |", [446e-9, 550e-9, 1.1e-6, 1e-6, 1e-5, 2.5e-5],
    [anc[i]["value_s"] for i in ("A02", "A01", "A03a", "A04a", "A04b", "A04c")], R(0.001), "HW", "literature")
n_e = nec[("explicit_best", "box_muller_current_law")]
n_c = nec[("certified_today", "box_muller_current_law")]
n_w = nec[("no_explicit_constant", "box_muller_current_law")]
n_af = nec[("explicit_best", "all_free_and_narrow")]
chk("nec_table", "4.3", "| Explicit constant, all-free floor | 8.8 ns | 1.3e13 T/s | 1.85e6 qubits |",
    [1.34e-9, 3.3e14, 0.39e-9, 1.1e15, 36e-9, 1.2e13, 8.8e-9, 1.3e13, 1.85e6],
    [n_e["t_layer_required_s"], n_e["T_per_s_required"], n_c["t_layer_required_s"], n_c["T_per_s_required"],
     n_w["t_layer_required_s"], n_w["T_per_s_required"],
     n_af["t_layer_required_s"], n_af["T_per_s_required"], n_af["logical_width"]], R(0.04), "HW", "modelled")
chk("nec_326", "4.3", "326× the budget", 326, n_e["T_per_s_required_over_budget"], A(0), "HW", "modelled")
ar = {a["id"]: a["value"] for a in HW["anchors_rate"] + HW["anchors_width"]}
chk("rate_anchors", "4.3", "about 2.4e5 CCZ/s", [2.4e5, 3e4, 48], [ar["A04d"], ar["A05b"], ar["A09"]], R(0.05), "HW", "literature (derived)")
E = S["explicit_best"]
chk("dep_table", "5.2", "| All-free oracle (free loader and exponential, narrow words) | 11.5 |",
    [11.5, 46.4, 116.0, 74.8, 104.4, 189.5, 197.8, 318.0, 1978, 648, 748, 7476],
    [E["all_free_oracle"][0], E["distfree_x5"][0], E["distfree_x2"][0], E["supply_1e13"][0], E["e_eq_eps"][0],
     E["width_W1e8"][0], E["t_layer_10ns"][0], E["primary_B8_0.001_ineligible"][0], E["supply_1e11"][0], E["width_W1e6"][0],
     E["t_layer_1us"][0], E["t_layer_10us"][0]], ("abs", 0.51), "HT", "modelled")
chk("dep_fail001", "5.2", "| Estimator failure 0.01 | 170.1 |", 170.1, S["explicit_best_fail001"]["primary"][0], A(1), "HT", "modelled")
chk("win_dep", "5.2", "0.43 at failure 0.01, or 0.51 at 0.003", [0.43, 0.51, 0.84, 1.002],
    [S["no_explicit_fail001"]["all_free_oracle"][0], S["no_explicit_fail0003"]["all_free_oracle"][0],
     S["no_explicit_fail001"]["one_lane_one_core"][0], S["no_explicit_fail0003"]["one_lane_one_core"][0]], A(2), "HT", "modelled")
ms = HT["stacked_departures"]["explicit_best"]["minimal_sets"]
chk("stack3", "5.3", "| All-free + 1 lane vs 1 core + distribution-free ×5 | 0.225 |",
    [0.225, 0.506, 0.714, 0.825], [m["min_M"] for m in ms], A(3), "HT", "modelled")
chk("cert_stack", "5.3", "gives 0.777. Its best pair gives\n3.89", [0.777, 3.89], [sdc["minimal_sets"][0]["min_M"], sdc["best_pairs"][0]["min_M"]], A(2), "HT", "modelled")
chk("ad_table", "5.3", "| All-free + distribution-free (Stage C), certified schedule | 0.54 |", [0.97, 0.27, 0.54],
    [AD["explicit_dirsel"]["all_free+one_lane_one_core"], AD["explicit_dirsel"]["all_free+distfree_stageC"],
     AD["certified_dirsel"]["all_free+distfree_stageC"]], A(2), "AD", "modelled (derived)")
pcd = DC["per_cell"]["B8x52|0.001"]
chk("dc_digits", "9.2", "0.9718, 0.2696 and 0.5392", [0.9718, 0.2696, 0.5392],
    [pcd["explicit_allfree_1lane_dirsel"], pcd["explicit_allfree_distfree_dirsel"], pcd["certified_allfree_distfree_dirsel"]],
    A(4), "DC", "modelled (derived)")
tc03 = HT["T_C"]["B4x12|0.03"]
chk("quirk", "9", "0.12677 s", [0.12677, 0.12440], [tc03["raw_best"]["t"], tc03["T_C"]], A(5), "HT", "measured")
chk("W1e6", "9", "D_eff of 11,034", 11034, D["B8x52|primary|W1e6|1e12|100ns"]["W0"], A(0), "HT", "modelled")
chk("persist", "9", "3.4e6\n    qubits", 3.4e6, fsum["B8x52"]["persistent_outputs"], R(0.02), "DN/FS", "modelled")
row("part1_carried", {"n": len(results), "bad": [r["id"] for r in results if not (r["match"] and r["snippet_in_v3"])]})
n_part1 = len(results)

# =====================================================================
# Part 2: numbers new in v2 (kept in v3), re-derived from primary files (fixer value alongside)
# =====================================================================
k_e, k_c, k_w1 = B8["k"]["explicit_best"], B8["k"]["certified"], B8["k"]["no_explicit_fail001"]
af_W0 = D["B8x52|all_free|W1e7|1e12|100ns"]["W0"]
af_N1 = D["B8x52|all_free|W1e7|1e12|100ns"]["N1"]
thr = {n: D_max / kv for n, kv in (("expl", k_e), ("cert", k_c), ("certds", kds_b8), ("win", k_w1))}
fxt = FX["d2_thresholds_B8_0.001"]
chk("thr_layers", "abstract/3/6/8", "| Best explicit (197.6) | 9.90 | 9.9e5 | 11.5× |",
    [9.90, 9.9e5, 2.86, 2.9e5, 5.73, 5.7e5, 266, 2.7e7],
    [thr["expl"], thr["expl"] * SUPPLY * T_LAYER, thr["cert"], thr["cert"] * SUPPLY * T_LAYER,
     thr["certds"], thr["certds"] * SUPPLY * T_LAYER, thr["win"], thr["win"] * SUPPLY * T_LAYER], ("sig", [3, 2, 3, 2, 3, 2, 3, 2]),
    "HT, ES (re-derived)", "modelled (derived)",
    fixer=[fxt["explicit_best"]["max_D_eff_layers"], fxt["certified"]["max_D_eff_layers"], fxt["certified_dirsel"]["max_D_eff_layers"]])
chk("thr_over", "3", "| Certified today (682.7) | 2.86 | 2.9e5 | 39.8× |", [11.5, 39.8, 19.9, 0.43, 16.5],
    [af_W0 / thr["expl"], af_W0 / thr["cert"], af_W0 / thr["certds"], af_W0 / thr["win"], af_N1 / thr["expl"]], A(1),
    "HT (re-derived)", "modelled (derived)")
chk("thr_af_114", "abstract/3", "oracle floor is 114 layers", 114, af_W0, A(0), "HT", "modelled")
chk("thr_af_N1", "3", "The N1 all-free floor is 163 layers", 163, af_N1, A(0), "HT", "modelled")
fac = hwrow[("B8x52", 0.001)]["factor_df_over_practice"]
chk("sym_thr", "3", "365 layers\n   and 3.7e7 T (explicit), 106 layers and 1.1e7 T (certified)", [365, 3.7e7, 106, 1.1e7],
    [thr["expl"] * fac, thr["expl"] * fac * 1e5, thr["cert"] * fac, thr["cert"] * fac * 1e5], ("sig", [3, 2, 3, 2]),
    "HT, HW (re-derived)", "modelled (derived)",
    fixer=[FX2["symmetric_thresholds"]["explicit_best"]["max_D_eff_layers"], FX2["symmetric_thresholds"]["certified"]["max_D_eff_layers"]])
# C09 decomposition
r8 = hwrow[("B8x52", 0.001)]
z = statistics.NormalDist().inv_cdf(0.995)
n_clt = (z * r8["sigma_preint"] / r8["e"]) ** 2
n_eb = r8["routes"]["S40"]["iid_preint_EB"]["n"]
n_pr = r8["practice_points"]
c_pp_pr = r8["T_C_practice_s"] / n_pr
c_iid = pp["B8x52|preint"]
chk("c09_dec", "4.3", "30.2 × 1.86 × 0.66 = 36.9", [30.2, 1.86, 0.66, 36.9],
    [n_clt / n_pr, n_eb / n_clt, c_iid / c_pp_pr, (n_clt / n_pr) * (n_eb / n_clt) * (c_iid / c_pp_pr)], ("sig", [3, 3, 2, 3]),
    "HW (re-derived)", "modelled from measured", fixer=FX["d4_c09"]["product_check"])
chk("c09_n", "4.3", "needs 4.30e7 points against 1.43e6 RQMC", [4.30e7, 1.43e6, 8.02e7, 15.8e-6],
    [n_clt, n_pr, n_eb, c_pp_pr], R(0.004), "HW (re-derived)", "modelled from measured")
chk("c09_total_vs_factor", "4.3", "**36.9**", 36.9, (n_eb * c_iid) / r8["T_C_practice_s"], A(1), "HW (re-derived)", "modelled")
# distfree table
chk("df_table", "4.3", "| Box-Muller | 21.7 | 10.9 | **6.29** | 11.2 | 0.23 |",
    [21.7, 10.9, 6.29, 11.2, 0.23, 1.08, 0.54, 0.31, 0.56, 0.012],
    [hwmin["box_muller_current_law|certified_today"]["min_M_distfree"],
     hwmin["box_muller_current_law|certified_today"]["min_M_distfree"] * kds_b8 / k_c,
     hwmin["box_muller_current_law|explicit_best"]["min_M_distfree"],
     hwmin["box_muller_current_law|explicit_best"]["min_M_distfree"] * nm[0] / nm[0] *
     p2s[("B8x52", 0.001)]["span+nondyadic (no mean cert)"]["k"] / k_e,
     hwmin["box_muller_current_law|no_explicit_constant"]["min_M_distfree"],
     hwmin["all_free_and_narrow|certified_today"]["min_M_distfree"],
     hwmin["all_free_and_narrow|certified_today"]["min_M_distfree"] * kds_b8 / k_c,
     hwmin["all_free_and_narrow|explicit_best"]["min_M_distfree"],
     hwmin["all_free_and_narrow|explicit_best"]["min_M_distfree"] * p2s[("B8x52", 0.001)]["span+nondyadic (no mean cert)"]["k"] / k_e,
     hwmin["all_free_and_narrow|no_explicit_constant"]["min_M_distfree"]], ("sig", [3, 3, 3, 3, 2, 3, 2, 2, 2, 2]),
    "HW, ES (re-derived)", "modelled (derived)")
results.append({"id": "df_at_binding_cell", "where": "abstract table", "snippet": "M at the binding cell (all\nmod)",
                "snippet_in_v3": "M at the binding cell (all\nmod)" in draft, "quoted": "symmetric column is at the binding cell",
                "file_value": {k2: v["at_distfree"] for k2, v in hwmin.items()},
                "match": all(v["at_distfree"] == ["B8x52", 0.001] for v in hwmin.values()), "source": "HW", "label": "modelled"})
k_noU1 = p2s[("B8x52", 0.001)]["span+nondyadic (no mean cert)"]["k"]
chk("noU1", "4.3/8", "Without\n  U1 the primary explicit M is 414.4", [414.4, 11.2, 0.56],
    [E["primary"][0] * k_noU1 / k_e, hwmin["box_muller_current_law|explicit_best"]["min_M_distfree"] * k_noU1 / k_e,
     hwmin["all_free_and_narrow|explicit_best"]["min_M_distfree"] * k_noU1 / k_e], ("abs", 0.051),
    "ES, HT, HW (re-derived)", "modelled (derived)", fixer=FX["d8_no_U1"])
# zero-bias / ineligible readings
Sc, Sw = S["certified"], S["no_explicit_fail001"]
chk("readings", "5.1", "| Strict zero-bias reading of the binding cell (e = ε) | 400.7 | 104.4 | 3.88 |",
    [400.7, 104.4, 3.88, 1065, 318.0, 11.8, 76.6],
    [Sc["e_eq_eps"][0], E["e_eq_eps"][0], Sw["e_eq_eps"][0], Sc["primary_B8_0.001_ineligible"][0],
     E["primary_B8_0.001_ineligible"][0], Sw["primary_B8_0.001_ineligible"][0], S["explicit_best_fail001"]["e_eq_eps"][0]],
    ("abs", 0.51), "HT", "modelled")
chk("ds_row", "5.1", "| Direction-select (condition met in this cost model) | 400.7 | 200.4 | 8.62 (already uses it) |",
    [400.7, 200.4], [m7["M_certified_today_dirsel"], m7["M_N1_explicit_best_dirsel"]], A(1), "ES", "modelled")
chk("fail001_row", "5.1", "| Best explicit at a consistent failure of 0.01 | 144.9 | 170.1 |", [144.9, 170.1],
    [B8["k"]["explicit_best_fail001"], S["explicit_best_fail001"]["primary"][0]], A(1), "HT", "modelled")
chk("dirsel_k_expl_b8", "5.1 (k now 170.7, N3-8)", "| Best explicit with direction-select | 170.7 | 200.4 |", [170.7, 200.4],
    [p2s[("B8x52", 0.001)]["N1 best: all credits incl. dirsel"]["k"], m7["M_N1_explicit_best_dirsel"]], A(1), "ES", "modelled")
chk("pair_zb", "5.3", "is a **pair** that gives 0.506", 0.506, ms[1]["min_M"], A(3), "HT", "modelled")
# bias desk
bd8 = J["BD"]["cases"]["B8x52"]
chk("bias", "2/8", "bias $0.000473 = 0.47ε ≤ 0.55ε", [0.00047, 0.47],
    [bd8["clamp_lowered_by_k_binades"]["3"]["total"], bd8["clamp_lowered_by_k_binades"]["3"]["total_over_eps"]],
    G(2), "BD (W0)", "modelled")
chk("bias_ok", "2", "≤ 0.55ε", 1.0, 1.0 if bd8["clamp_lowered_by_k_binades"]["3"]["meets_0p55eps"] else 0.0, A(0), "BD (W0)", "modelled")
chk("bias_bound", "2", "current certified bias bound of $0.00124", 0.00124, bd8["baseline_total_usd"], ("abs", 0.000005), "BD (W0)", "measured (certified record terms)")
# T_C vs H16
t16 = h16["B8x52/0.001"]["t_c_by_workers"]["16"]
chk("tc_h16", "2/8", "23.46 s, 4.1% higher", [23.46, 4.1, 222.8],
    [t16, (t16 / B8["T_C"] - 1) * 100, E["primary"][0] * B8["T_C"] / t16], A(1), "HW, HT (re-derived)", "measured / modelled",
    fixer=FX["d10_TC"])
# residual span
span = 8192 / 211
chk("res_span", "6 lever 5", "≤ $0.17 against the $38.82 support-tight span", [0.17, 3.37, 6.18, 38.82],
    [span / E["primary"][0], span / E["all_free_oracle"][0],
     span / hwmin["box_muller_current_law|explicit_best"]["min_M_distfree"], span], A(2), "HT, HW (re-derived)", "modelled (derived, first order)")
chk("f20_cap", "6 lever 5", "about 4.5× (σ 5.15 → 1.14, F20)", 4.5, 5.15 / 1.14, A(1), "REG F20", "register record")
row("part2_new_numbers", {"n": len(results) - n_part1,
                          "bad": [r["id"] for r in results[n_part1:] if not (r["match"] and r["snippet_in_v3"])]})
n_part2 = len(results)

# =====================================================================
# Part 3: register / DP1 / text checks
# =====================================================================
REG = J["REG"]
tiers = collections.Counter(i["tier"] for i in REG["items"])
chk("register", "App A", "| T6 | Parked as a different task | 25 |", [4, 8, 12, 26, 35, 25],
    [tiers[t] for t in ("T1", "T2", "T3", "T4", "T5", "T6")], A(0), "REG (W0)", "register record")
t6 = sorted(i["id"] for i in REG["items"] if i["tier"] == "T6")
exp_t6 = ["E10"] + ["E%d" % i for i in range(14, 20)] + ["F%02d" % i for i in range(9, 20)] + ["F21", "F22"] + \
         ["F%d" % i for i in range(26, 30)] + ["F32"]
results.append({"id": "T6_list", "where": "7", "match": sorted(exp_t6) == t6, "quoted": exp_t6, "file_value": t6,
                "source": "REG", "label": "register record", "snippet": "E10, E14-E19", "snippet_in_v3": "E10, E14-E19" in draft})
it = {i["id"]: i for i in REG["items"]}
claims = {"F05": ("T2", "Close as a standalone route if >=10x miss remains"),
          "F20": ("T2", "Cost coherent preintegration only if the other levers reach miss <=4x"),
          "F04": ("T4", "closes on the F20 zero-depth credit. Reopen if the other levers bring miss <=4x"),
          "E22": ("T4", "0 of 3,106"), "C12": ("T4", "six constructions, three contracts, one toolchain"),
          "C14": ("T1", "")}
for rid, (tier, phrase) in claims.items():
    txt = json.dumps(it[rid])
    results.append({"id": "reg_" + rid, "where": "6/7/App A", "snippet": rid, "snippet_in_v3": rid in draft,
                    "quoted": [tier, phrase], "file_value": [it[rid]["tier"], phrase in txt],
                    "match": it[rid]["tier"] == tier and (phrase == "" or phrase in txt), "source": "REG", "label": "register record"})
results.append({"id": "dp1_errata", "where": "5.3/9.1", "snippet": "the DP1\nerrata block corrects it [DP1]",
                "snippet_in_v3": "the DP1\nerrata block corrects it [DP1]" in draft, "quoted": "DP1 errata records two departures",
                "file_value": "Two departures, not three" in dp1, "match": "Two departures, not three" in dp1,
                "source": "DP1", "label": "record"})
claim = '"No design with certified constants reaches a 10× complete-latency advantage for the fixed B4x12/B8x52 knock-out task under the stated conventions."'
results.append({"id": "claim_verbatim", "where": "abstract", "snippet": claim, "snippet_in_v3": claim in draft,
                "quoted": "verbatim N1 claim", "file_value": claim in open("research/plan110_n1/N1_CARD.md", encoding="utf-8").read(),
                "match": claim in open("research/plan110_n1/N1_CARD.md", encoding="utf-8").read(), "source": "N1_CARD", "label": "record"})
v1sha = sha(V1)
results.append({"id": "v1_unchanged", "where": "front matter", "snippet": "(`FRONTIER_NEGATIVE_RESULT_DRAFT.md`, unchanged)",
                "snippet_in_v3": "(`FRONTIER_NEGATIVE_RESULT_DRAFT.md`, unchanged)" in draft, "quoted": "3d8e5900…c62b1c",
                "file_value": v1sha, "match": v1sha.startswith("3d8e5900") and v1sha.endswith("c62b1c"),
                "source": "v1 file", "label": "record"})
# v1 phrases that the fixes should have removed (absence = fixed)
gone = {1: "two R1 recomputes along different paths confirm them", 5: "one idealized change on each side",
        11: "74.8 is layer time", 19: "closes the last open", 18: "Only one primary floor design fits",
        3: "Eligible at zero deterministic bias", 7: "This draft changes none of them",
        6: "That cost is assumed here", 16: "the only demonstrated complete readout-to-feedback loop, d = 3",
        14: "(Python 3.12.4, standard library only). All scripts"}
body = draft.split("## Changelog")[0]  # the changelog quotes the removed v1 wording
for d, ph in gone.items():
    results.append({"id": "v1_phrase_gone_d%d" % d, "where": "v3 body (before changelog)", "snippet": "(absence) " + ph,
                    "snippet_in_v3": True, "quoted": "absent", "file_value": ph in body, "match": ph not in body,
                    "source": "v3", "label": "text"})
# provenance flags of every N1 / review / fixer output whose numbers v3 uses
prov = {}
for kx in ("HT", "KF", "FS", "ES", "HW", "DN", "AD", "DC", "NC", "FX", "FX2"):
    m = J[kx].get("meta") or J[kx]
    fl = m.get("flags") or m.get("isolated_flags") or {}
    prov[kx] = {"isolated": fl.get("isolated", "not recorded (README claims -I -S -B)"),
                "no_site": fl.get("no_site", "not recorded (README claims -I -S -B)"), "python": str(m.get("python", ""))[:6]}
results.append({"id": "provenance_flags", "where": "front matter/App B", "snippet": "-I -S -B", "snippet_in_v3": "-I -S -B" in draft,
                "quoted": "3.12.4; isolated=1, no_site=1 where recorded", "file_value": prov,
                "match": all(v["python"] == "3.12.4" and v["isolated"] not in (0, False) and v["no_site"] not in (0, False)
                             for v in prov.values()),
                "source": "meta of each file", "label": "record"})
row("part3_text_register", {"n": len(results) - n_part2,
                            "bad": [r["id"] for r in results[n_part2:] if not (r["match"] and r["snippet_in_v3"])]})
n_part3 = len(results)

# =====================================================================
# Part 4: probes for NEW defects (modelled, derived; not checks of quoted values)
# =====================================================================
probe = {}
# (a) readings combined: zero-bias (e = eps) + direction-select, both "within the primary" in v2
r_eps = [r for r in p1 if r["case"] == "B8x52" and r["eps"] == 0.001 and r["split"] == "eps"][0]
soe_eps = B8["sigma_over_e"] * 0.45
Dmax_eps = B8["T_C"] / (10 * soe_eps * T_LAYER)
probe["zero_bias_plus_dirsel"] = {
    "certified_M": r_eps["k_eff_direction_select"] * B8["D_eff_primary"]["used"] / Dmax_eps,
    "certified_M_without_dirsel_check_vs_400.7": r_eps["k_eff"] * B8["D_eff_primary"]["used"] / Dmax_eps,
    "explicit_M_approx (e=eps explicit x dirsel ratio at 0.45eps)": E["e_eq_eps"][0] * pcd["dirsel_ratio_explicit"],
    "explicit_fail001_e_eq_eps_x_dirsel_ratio_approx": S["explicit_best_fail001"]["e_eq_eps"][0] * pcd["dirsel_ratio_explicit"],
    "ineligible_B4x12_dirsel": {"certified": [r for r in ES["part7_M_primary"] if r["case"] == "B4x12" and r["eps"] == 0.001][0]["M_certified_today_dirsel"],
                                "explicit": [r for r in ES["part7_M_primary"] if r["case"] == "B4x12" and r["eps"] == 0.001][0]["M_N1_explicit_best_dirsel"]},
    "label": "modelled (derived)", "direction": "q+"}
row("probe_combined_readings", probe["zero_bias_plus_dirsel"], "modelled (derived)", "q+")
# (b) per-cell thresholds: the binding-cell limits are not the limits in the other decision cells
pc = {}
for (cs, ep) in (("B4x12", 0.01), ("B4x12", 0.001), ("B8x52", 0.01), ("B8x52", 0.001)):
    c = cell[(cs, ep)]
    dm = c["T_C"] / (10 * c["sigma_over_e"] * T_LAYER)
    pc[f"{cs}|{ep}"] = {"D_max_k1": dm, "explicit_max_layers": dm / c["k"]["explicit_best"],
                        "explicit_max_T": dm / c["k"]["explicit_best"] * 1e5,
                        "certified_max_layers": dm / c["k"]["certified"],
                        "W0_primary_D_eff": c["D_eff_primary"]["W0"],
                        "W0_allfree_D_eff": D[f"{cs}|all_free|W1e7|1e12|100ns"]["W0"]}
probe["per_cell_thresholds"] = pc
row("probe_per_cell_thresholds", pc, "modelled (derived)", "0")
# (c) all-free stacked with supply 1e13 or 10 ns (section 6 lever 3 says 'reaches or nearly reaches')
af13 = D["B8x52|all_free|W1e7|1e13|100ns"]["used"]
af10 = D["B8x52|all_free|W1e7|1e12|10ns"]["used"]
probe["allfree_stacks_explicit_B8"] = {
    "allfree+supply1e13": k_e * af13 / D_max,
    "allfree+10ns": k_e * af10 / (D_max * 10),
    "allfree+1lane": HT["stacked_departures"]["explicit_best"]["best_pairs"][0]["min_M"],
    "allfree+distfree_stageC": hwmin["all_free_and_narrow|explicit_best"]["min_M_distfree"]}
row("probe_allfree_stacks", probe["allfree_stacks_explicit_B8"], "modelled (derived)", "q+")
# (d) best explicit k with direction-select at the binding cell (v2 table shows n/a)
probe["best_explicit_dirsel_k_B8"] = p2s[("B8x52", 0.001)]["N1 best: all credits incl. dirsel"]["k"]
# (e) 'every conditional credit granted' label vs direction-select
probe["explicit_all_credits_incl_dirsel"] = {"primary": m7["M_N1_explicit_best_dirsel"],
                                             "symmetric_BM": hwmin["box_muller_current_law|explicit_best"]["min_M_distfree"] * pcd["dirsel_ratio_explicit"]}
row("probe_misc", {"best_explicit_dirsel_k_B8": probe["best_explicit_dirsel_k_B8"],
                   "explicit_all_credits_incl_dirsel": probe["explicit_all_credits_incl_dirsel"]}, "modelled (derived)", "q+")
# (f) mentions of 'the user' inside the manuscript (style / provenance); v3 should have none
probe["user_mentions_lines"] = [i + 1 for i, ln_ in enumerate(draft.splitlines()) if "user" in ln_]

# Part 4 comparison: every probe re-computed here must equal the re-check's printed probe
# (same code on the same primary files); user_mentions_lines is a v2 text probe, so skipped.


def _flat(d, pre=""):
    o = {}
    for k_, v_ in d.items():
        if isinstance(v_, dict):
            o.update(_flat(v_, pre + k_ + "/"))
        else:
            o[pre + k_] = v_
    return o


fp_new, fp_rk = _flat({k_: v_ for k_, v_ in probe.items() if k_ != "user_mentions_lines"}), \
    _flat({k_: v_ for k_, v_ in RK["probes"].items() if k_ != "user_mentions_lines"})
for k_ in sorted(fp_rk):
    a_, b_ = fp_new.get(k_), fp_rk[k_]
    ok_ = (a_ == b_) if not isinstance(b_, float) else (isinstance(a_, float) and abs(a_ - b_) <= 1e-12 * max(1.0, abs(b_)))
    results.append({"id": "probe_match/" + k_, "where": "Part 4 (probes vs number_recheck.json)", "snippet": "(probe)",
                    "snippet_in_v3": True, "quoted": b_, "file_value": a_, "match": ok_, "source": "RK", "label": "modelled (derived)"})
row("part4_probe_match", {"n": len(results) - n_part3,
                          "bad": [r["id"] for r in results[n_part3:] if not r["match"]]})
n_part4 = len(results)

# =====================================================================
# Part 5: numbers new in v3, re-derived here from the primary files.
# Snippet presence uses whitespace-normalised matching (v3 wraps lines); the re-check probe
# value and the v3_numbers.json value are kept as extra columns.
# =====================================================================


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


ndraft = norm(draft)
V3V = V3N["values"]
rkp = RK["probes"]


def chkn(cid, where, snippet, quoted, actual, tol, src, label, probe_value=None, v3n_value=None):
    chk(cid, where, snippet, quoted, actual, tol, src, label)
    r_ = results[-1]
    r_["snippet_in_v3"] = norm(snippet) in ndraft
    r_["snippet_matching"] = "whitespace-normalised"
    if probe_value is not None:
        r_["recheck_probe_value"] = probe_value
    if v3n_value is not None:
        r_["v3_numbers_value"] = v3n_value


Sw = S["no_explicit_fail001"]
ratio = pcd["dirsel_ratio_explicit"]
k_ds_eps = r_eps["k_eff_direction_select"]
cert_comb = k_ds_eps * B8["D_eff_primary"]["used"] / Dmax_eps
expl_comb = E["e_eq_eps"][0] * ratio
expl_comb001 = S["explicit_best_fail001"]["e_eq_eps"][0] * ratio
zb = rkp["zero_bias_plus_dirsel"]
c1 = V3V["N3_1_combined_reading"]
# N3-1
chkn("v3_comb_cert", "5.1 verdict", "certified M = 200.4 (k = 379.3 at e = ε [ES])", [200.4, 379.3],
     [cert_comb, k_ds_eps], A(1), "ES, HT (re-derived)", "modelled (derived), q+",
     [zb["certified_M"]], [c1["certified_M"], c1["k_certified_dirsel_e_eq_eps"]])
chkn("v3_comb_expl", "5.1 verdict", "best explicit M ≈ 90, or ≈ 66 at failure 0.01", [90, 66],
     [expl_comb, expl_comb001], ("abs", 0.5), "HT, DC (re-derived)", "modelled (derived, approximate), q+",
     [zb["explicit_M_approx (e=eps explicit x dirsel ratio at 0.45eps)"], zb["explicit_fail001_e_eq_eps_x_dirsel_ratio_approx"]],
     [c1["explicit_M_approx"], c1["explicit_M_fail001_approx"]])
chkn("v3_comb_inputs", "5.1 verdict",
     "the zero-bias values 104.4 and 76.6 multiplied by the binding-cell direction-select ratio at e = 0.45ε, 0.864 [DC]",
     [104.4, 76.6, 0.864], [E["e_eq_eps"][0], S["explicit_best_fail001"]["e_eq_eps"][0], ratio],
     ("abs", [0.05, 0.05, 0.0005]), "HT, DC", "modelled")
chkn("v3_comb_row", "5.1 readings table",
     "| Strict zero-bias reading + direction-select (the lowest combination) | 200.4 | ≈ 90 (approximate; ≈ 66 at failure 0.01) | 3.88 (already uses it) |",
     [200.4, 90, 66, 3.88], [cert_comb, expl_comb, expl_comb001, Sw["e_eq_eps"][0]], ("abs", [0.05, 0.5, 0.5, 0.005]),
     "ES, HT, DC (re-derived)", "modelled (derived), q+")
chkn("v3_comb_s8", "8 rigour", "gives certified 200.4 and explicit ≈ 90, or ≈ 66 at failure 0.01", [200.4, 90, 66],
     [cert_comb, expl_comb, expl_comb001], ("abs", [0.05, 0.5, 0.5]), "ES, HT, DC (re-derived)", "modelled (derived), q+")
singles_c = [S["certified"]["primary"][0], B8["M_N1_floor_only_primary"]["certified"], S["certified"]["e_eq_eps"][0],
             m7["M_certified_today_dirsel"], S["certified"]["primary_B8_0.001_ineligible"][0]]
singles_e = [E["primary"][0], B8["M_N1_floor_only_primary"]["explicit_best"], E["e_eq_eps"][0],
             m7["M_N1_explicit_best_dirsel"], E["primary_B8_0.001_ineligible"][0]]
chkn("v3_one_at_a_time", "5.1 verdict / 8",
     "Taken one at a time, the readings above keep the certified class at M ≥ 400.7 and the best explicit class at M ≥ 104.4",
     [400.7, 104.4], [min(singles_c), min(singles_e)], A(1), "HT, ES", "modelled")
chkn("v3_above_30", "5.1 verdict", "All of these are above the 30× threshold that justifies R1", 1.0,
     1.0 if min(cert_comb, expl_comb, expl_comb001, min(singles_c), min(singles_e)) > 30 else 0.0, A(0),
     "derived", "modelled (derived)")
# N3-2
a2 = V3V["N3_2_allfree_stacks"]
M13 = k_e * af13 / D_max
M10 = k_e * af10 / (D_max * 10)
chkn("v3_lever3_first_two", "6 lever 3", "0.31 (distribution-free) and 1.125 (one lane)", [0.31, 1.125],
     [hwmin["all_free_and_narrow|explicit_best"]["min_M_distfree"], HT["stacked_departures"]["explicit_best"]["best_pairs"][0]["min_M"]],
     ("abs", [0.005, 0.0005]), "HW, HT", "modelled")
chkn("v3_lever3_other_two", "6 lever 3",
     "with 1e13 T/s the all-free M is 11.3, because D_eff only drops from 114 to 112 layers, and with a 10 ns layer it is 7.3, because the iterate becomes supply-bound at 724 layers of 10 ns",
     [11.3, 114, 112, 7.3, 724], [M13, af_W0, af13, M10, af10], ("abs", [0.05, 0.5, 0.5, 0.05, 0.5]),
     "HT (re-derived)", "modelled (derived), q+",
     [rkp["allfree_stacks_explicit_B8"]["allfree+supply1e13"], rkp["allfree_stacks_explicit_B8"]["allfree+10ns"]],
     [a2["M_allfree_supply1e13"], a2["M_allfree_10ns"]])
results.append({"id": "v3_lever3_supply_bound_10ns", "where": "6 lever 3", "snippet": "supply-bound at 724 layers of 10 ns",
                "snippet_in_v3": "supply-bound at 724 layers of 10 ns" in ndraft, "quoted": "D_eff at 10 ns exceeds the 100 ns reaction-bound depth",
                "file_value": [af10, af_W0], "match": af10 > af_W0 and M13 > 1 and M10 > 1, "source": "HT", "label": "modelled"})
# N3-3
pcv = V3V["N3_3_N3_4_limits"]["per_cell"]
chkn("v3_per_cell_explicit", "3 item 3",
     "For the best explicit constant they are 1.14 layers / 1.1e5 T at B4x12 $0.001, 0.53 / 5.3e4 at B4x12 $0.01 and 2.43 / 2.4e5 at B8x52 $0.01",
     [1.14, 1.1e5, 0.53, 5.3e4, 2.43, 2.4e5],
     [pc["B4x12|0.001"]["explicit_max_layers"], pc["B4x12|0.001"]["explicit_max_T"], pc["B4x12|0.01"]["explicit_max_layers"],
      pc["B4x12|0.01"]["explicit_max_T"], pc["B8x52|0.01"]["explicit_max_layers"], pc["B8x52|0.01"]["explicit_max_T"]],
     ("sig", [3, 2, 2, 2, 3, 2]), "HT (re-derived)", "modelled (derived)",
     [rkp["per_cell_thresholds"]["B4x12|0.001"]["explicit_max_layers"]], [pcv["B4x12|0.001"]["explicit_max_layers"]])
kds_b4 = [r for r in p1 if r["split"] == "0.45eps" and r["case"] == "B4x12" and r["eps"] == 0.001][0]["k_eff_direction_select"]
chkn("v3_per_cell_certified", "3 item 3", "(at B4x12 $0.001: 0.34 layers, or 0.68 with direction-select)", [0.34, 0.68],
     [pc["B4x12|0.001"]["certified_max_layers"], pc["B4x12|0.001"]["D_max_k1"] / kds_b4], A(2), "HT, ES (re-derived)",
     "modelled (derived)", [rkp["per_cell_thresholds"]["B4x12|0.001"]["certified_max_layers"]],
     [pcv["B4x12|0.001"]["certified_max_layers"], pcv["B4x12|0.001"]["certified_dirsel_max_layers"]])
b4_loose = max(pc["B4x12|0.001"]["explicit_max_layers"], pc["B4x12|0.01"]["explicit_max_layers"])
chkn("v3_per_cell_loosest_B4", "3 item 3", "for B4x12 the loosest limit is 1.1 layers / 1.1e5 T at $0.001 (explicit)", [1.1, 1.1e5],
     [b4_loose, b4_loose * SUPPLY * T_LAYER], G(2), "HT (re-derived)", "modelled (derived)")
results[-1]["match"] = results[-1]["match"] and b4_loose == pc["B4x12|0.001"]["explicit_max_layers"]
chkn("v3_per_cell_scope1", "1 scope item 1", "(B4x12 $0.001: 1.1 layers / 1.1e5 T for the best explicit constant", [1.1, 1.1e5],
     [pc["B4x12|0.001"]["explicit_max_layers"], pc["B4x12|0.001"]["explicit_max_T"]], G(2), "HT (re-derived)", "modelled (derived)")
chkn("v3_per_cell_s8", "8", "(B4x12 $0.001: 1.1 layers / 1.1e5 T for the explicit constant", [1.1, 1.1e5],
     [pc["B4x12|0.001"]["explicit_max_layers"], pc["B4x12|0.001"]["explicit_max_T"]], G(2), "HT (re-derived)", "modelled (derived)")
results.append({"id": "v3_certified_lower_every_cell", "where": "1 / 3", "snippet": "lower for the certified constant",
                "snippet_in_v3": "lower for the certified constant" in ndraft, "quoted": "certified limits < explicit limits in every cell",
                "file_value": {ck: [pcv[ck]["certified_max_layers"], pcv[ck]["certified_dirsel_max_layers"], pcv[ck]["explicit_max_layers"]] for ck in pcv},
                "match": all(pcv[ck]["certified_dirsel_max_layers"] < pcv[ck]["explicit_max_layers"] for ck in pcv),
                "source": "V3 / HT, ES", "label": "modelled (derived)"})
chkn("v3_B4_allfree_floor", "3 item 3", "the B4x12 all-free floor is 94 layers [HT]", 94,
     D["B4x12|all_free|W1e7|1e12|100ns"]["W0"], A(0), "HT", "modelled")
# N3-4
chkn("v3_cert_thr_abstract", "abstract", "today's certified constant the limits are 2.9-5.7 layers and 2.9e5-5.7e5 T",
     [2.9, 5.7, 2.9e5, 5.7e5], [thr["cert"], thr["certds"], thr["cert"] * SUPPLY * T_LAYER, thr["certds"] * SUPPLY * T_LAYER],
     G(2), "HT, ES (re-derived)", "modelled (derived)", None,
     [pcv["B8x52|0.001"]["certified_max_layers"], pcv["B8x52|0.001"]["certified_dirsel_max_layers"]])
chkn("v3_cert_thr_scope1", "1 scope item 1", "more than 2.9-5.7 layers or 2.9e5-5.7e5 T", [2.9, 5.7, 2.9e5, 5.7e5],
     [thr["cert"], thr["certds"], thr["cert"] * SUPPLY * T_LAYER, thr["certds"] * SUPPLY * T_LAYER], G(2), "HT, ES (re-derived)", "modelled (derived)")
chkn("v3_cert_thr_lever2", "6 lever 2", "or 2.9-5.7 layers and 2.9e5-5.7e5 T (certified; the upper values with direction-select) [FX]",
     [2.9, 5.7, 2.9e5, 5.7e5], [thr["cert"], thr["certds"], thr["cert"] * SUPPLY * T_LAYER, thr["certds"] * SUPPLY * T_LAYER],
     G(2), "HT, ES (re-derived)", "modelled (derived)")
chkn("v3_cert_thr_s8", "8", "the 5.7 / 5.7e5 values if direction-select is granted and 2.9 / 2.9e5 if not", [5.7, 5.7e5, 2.9, 2.9e5],
     [thr["certds"], thr["certds"] * SUPPLY * T_LAYER, thr["cert"], thr["cert"] * SUPPLY * T_LAYER], G(2), "HT, ES (re-derived)", "modelled (derived)")
chkn("v3_cert_over", "abstract", "a further 11.5× (explicit) or 20-40× (certified)", [11.5, 20, 40],
     [af_W0 / thr["expl"], af_W0 / thr["certds"], af_W0 / thr["cert"]], ("sig", [3, 1, 1]), "HT, ES (re-derived)", "modelled (derived)",
     None, [V3N["values"]["N3_3_N3_4_limits"]["binding_allfree_over_certified_dirsel_limit"],
            V3N["values"]["N3_3_N3_4_limits"]["binding_allfree_over_certified_limit"]])
# N3-5
k_noU1_b8 = p2s[("B8x52", 0.001)]["span+nondyadic (no mean cert)"]["k"]
bm_df = hwmin["box_muller_current_law|explicit_best"]["min_M_distfree"]
chkn("v3_abstract_row", "abstract table",
     "| Best explicit worst-case constant (U1 + U2 + non-dyadic M) | **232.0** (200.4 with direction-select) | **6.29** (11.2 without the U1 mean credit; about 5.43 with direction-select, derived) |",
     [232.0, 200.4, 6.29, 11.2, 5.43], [E["primary"][0], m7["M_N1_explicit_best_dirsel"], bm_df, bm_df * k_noU1_b8 / k_e, bm_df * ratio],
     ("abs", [0.05, 0.05, 0.005, 0.05, 0.005]), "HT, ES, HW, DC (re-derived)", "modelled (derived)",
     [rkp["explicit_all_credits_incl_dirsel"]["primary"], rkp["explicit_all_credits_incl_dirsel"]["symmetric_BM"]],
     [V3V["N3_5_explicit_dirsel"]["primary_M"], V3V["N3_5_explicit_dirsel"]["symmetric_BM_M_approx"]])
# N3-6
e20 = it["E20"]
e20_ok = (e20["tier"] == "T2" and e20["disposition"] == "credited screen value / branch-A lever"
          and e20["kill_or_defer"].startswith("State the width bound") and "and stop" in e20["kill_or_defer"]
          and e20["optimistic_max_factor"].startswith(">10x only with >=15x logical width"))
results.append({"id": "v3_E20_register", "where": "7.2 / App A", "snippet": "The register file keeps E20 at T2 (\"credited screen value / branch-A lever\")",
                "snippet_in_v3": norm("The register file keeps E20 at T2 (\"credited screen value / branch-A lever\")") in ndraft,
                "quoted": ["T2", "credited screen value / branch-A lever", "State the width bound … and stop", ">10x only with >=15x"],
                "file_value": [e20["tier"], e20["disposition"], e20["kill_or_defer"], e20["optimistic_max_factor"][:40]],
                "match": e20_ok, "source": "REG", "label": "register record"})
chkn("v3_E20_lane", "7.2", "the binding cell gets a lane credit of 1.00× under every modelled supply", [1.00, 1.00],
     [ln[("B8x52", "supply_1e12")], ln[("B8x52", "unlimited")]], A(2), "ES", "modelled")
# N3-8 (k for 'Best explicit with direction-select') is checked by dirsel_k_expl_b8 in Part 2
row("part5_v3_numbers", {"n": len(results) - n_part4,
                         "bad": [r["id"] for r in results[n_part4:] if not (r["match"] and r["snippet_in_v3"])]})
n_part5 = len(results)

# =====================================================================
# Part 0: SHA-256 of v1 / v2 (must be unchanged) and provenance of the v3 inputs
# =====================================================================
sha_v1, sha_v2, sha_v3 = sha(V1), sha(V2), sha(V3)
build_rows = [json.loads(x) for x in open(ROWS, encoding="utf-8") if '"build_v3"' in x]
v3n_inputs = V3N["meta"]["inputs_sha256"]
v3n_paths = {"HT": F["HT"], "ES": F["ES"], "HW": F["HW"], "DC": F["DC"], "RK": RK_PATH, "REG": F["REG"]}
sha_checks = {
    "v1_unchanged": {"expected": V1_SHA, "actual": sha_v1, "ok": sha_v1 == V1_SHA},
    "v2_unchanged": {"expected": V2_SHA, "actual": sha_v2, "ok": sha_v2 == V2_SHA and sha_v2.startswith("51dcf89b")},
    "recheck_was_run_on_this_v2_and_v1": {"actual": [RK["meta"]["inputs_sha256"]["v2"], RK["meta"]["inputs_sha256"]["v1"]],
                                          "ok": RK["meta"]["inputs_sha256"]["v2"] == V2_SHA and RK["meta"]["inputs_sha256"]["v1"] == V1_SHA},
    "v3_matches_build_row": {"actual": sha_v3, "build_rows": [b_.get("v3_sha256") for b_ in build_rows],
                             "ok": len(build_rows) == 1 and build_rows[0]["v3_sha256"] == sha_v3 and build_rows[0]["v2_sha256"] == V2_SHA},
    "v3_numbers_inputs_unchanged": {"ok": all(v3n_inputs[k_] == sha(p_) for k_, p_ in v3n_paths.items())},
    "v3_numbers_flags": {"actual": V3N["meta"]["flags"], "ok": V3N["meta"]["flags"]["isolated"] == 1 and V3N["meta"]["flags"]["no_site"] == 1},
}

# =====================================================================
# Part 6: N3-1..N3-8 target phrases gone from the v3 body, corrections present
# (whitespace-normalised; each "gone" phrase must also have been present in the v2 body)
# =====================================================================
body3 = norm(draft.split("## Changelog")[0])
body2 = norm(v2_text.split("## Changelog")[0])
N3 = {
    "N3-1": {"gone": ["Under every reading above", "under every reading of the primary",
                      "the certified class stays at M ≥ 400.7"],
             "present": ["Taken one at a time, the readings above keep the certified class at M ≥ 400.7",
                         "certified M = 200.4 (k = 379.3 at e = ε [ES]) and best explicit M ≈ 90, or ≈ 66 at failure 0.01",
                         "The two explicit values are approximate",
                         "| Strict zero-bias reading + direction-select (the lowest combination) | 200.4 | ≈ 90 (approximate; ≈ 66 at failure 0.01) |",
                         "gives certified 200.4 and explicit ≈ 90, or ≈ 66 at failure 0.01 (mod, derived, q+; the explicit values approximate) [RK]"]},
    "N3-2": {"gone": ["Any one of these, stacked with lever 2's all-free floor, reaches or nearly reaches"],
             "present": ["the first two reach or nearly reach M = 1: 0.31 (distribution-free) and 1.125 (one lane)",
                         "The other two do not", "the all-free M is 11.3",
                         "it is 7.3, because the iterate becomes supply-bound at 724 layers of 10 ns"]},
    "N3-3": {"gone": ["Any design above either limit is covered by the claim."],
             "present": [("above the corresponding per-cell limit in the other decision cells (B4x12 $0.001: 1.1 layers / 1.1e5 T", 2),
                         "These limits are for the binding cell.",
                         "A design is covered by the claim only if its iterate is above the limit in every decision cell"]},
    "N3-4": {"gone": ["2.9 layers and 2.9e5 T", "about 3 layers or 3e5 T", "a further 11.5× (explicit) or 40×"],
             "present": [("2.9-5.7 layers and 2.9e5-5.7e5 T", 3), "2.9-5.7 layers or 2.9e5-5.7e5 T", "or 20-40× (certified)",
                         "the 5.7 / 5.7e5 values if direction-select is granted and 2.9 / 2.9e5 if not"]},
    "N3-5": {"gone": ["(every conditional credit granted)"],
             "present": ["| Best explicit worst-case constant (U1 + U2 + non-dyadic M) | **232.0** (200.4 with direction-select) |",
                         "about 5.43 with direction-select"]},
    "N3-6": {"gone": ["**Lanes, E20.**", "reads three dispositions differently"],
             "present": ["reads four dispositions differently", "- **E20** stays T2 in the register",
                         "F05 and E20 (both T2 in the register)",
                         "**E20: entangled parallel amplitude estimation (lanes).**"]},
    "N3-7": {"gone": ["The primary therefore keeps e = 0.45ε (mod, q+)"],
             "present": ["clamp tightening (admission: mod, q+)",
                         "keeps e = 0.45ε, which is q− relative to the strict zero-bias reading"]},
    "N3-8": {"gone": ["the user", "user's", "Undisclosed-in-v1", "| Best explicit with direction-select | n/a |",
                      "has not been re-checked by a reviewer"],
             "present": [("the primary convention fixed in [W0C]", 2), "**Further quantum-favourable conventions**",
                         "| Best explicit with direction-select | 170.7 | 200.4 |",
                         "checked only by the script `research/plan110_n1/v3/check_v3.py`"]},
}
n3 = {}
for dk, spec in N3.items():
    items = []
    for ph in spec["gone"]:
        p_ = norm(ph)
        items.append({"kind": "gone", "phrase": ph, "in_v2_body": p_ in body2, "in_v3_body": p_ in body3,
                      "ok": (p_ in body2) and (p_ not in body3)})
    for ph in spec["present"]:
        ph, need = (ph if isinstance(ph, tuple) else (ph, 1))
        cnt = body3.count(norm(ph))
        items.append({"kind": "present", "phrase": ph, "count_v3_body": cnt, "need": need, "ok": cnt >= need})
    n3[dk] = {"items": items, "ok": all(i_["ok"] for i_ in items)}
# extra structural checks
sec = lambda a_, b_: draft.split(a_)[1].split(b_)[0]
s71, s72 = sec("### 7.1 Closed for this task", "### 7.2"), sec("### 7.2 Bounded at the primary conventions", "### 7.3")
n3["N3-6"]["items"].append({"kind": "section", "phrase": "E20 absent from 7.1 and present in 7.2",
                            "ok": "E20" not in s71 and "E20" in s72})
n3["N3-6"]["ok"] = all(i_["ok"] for i_ in n3["N3-6"]["items"])
n3["N3-8"]["items"].append({"kind": "regex", "phrase": r"\buser (case-insensitive, whole v3 file)",
                            "ok": re.search(r"\buser", draft, re.I) is None and probe["user_mentions_lines"] == []})
n3["N3-8"]["ok"] = all(i_["ok"] for i_ in n3["N3-8"]["items"])
general = {
    "claim_verbatim_from_N1_card": claim in draft and claim in open("research/plan110_n1/N1_CARD.md", encoding="utf-8").read(),
    "affiliation_VIT_Vellore": "Affiliation: VIT Vellore" in draft and "Chennai" not in draft,
    "AI_assisted_statement": "This is an **AI-assisted draft**" in draft,
    "no_author_or_approval_claims": "It does not assert author names, human approval" in draft
    and not re.search(r"\b(approved by|signed off by|sign-off was given|has been approved)\b", draft, re.I),
    "v2_changelog_kept_verbatim": v2_text[v2_text.index("## Changelog (v1 → v2)"):] in draft,
    "v3_changelog_rows_N3_1_to_8": "## Changelog v3 (v2 → v3)" in draft
    and all(f"| N3-{i_} | minor |" in draft.split("## Changelog v3 (v2 → v3)")[1] for i_ in range(1, 9)),
}

# diff v2 -> v3
diff_lines = list(difflib.unified_diff(v2_text.splitlines(keepends=True), draft.splitlines(keepends=True),
                                       fromfile=V2, tofile=V3, n=1))
n_hunks = sum(1 for x in diff_lines if x.startswith("@@"))

bad = [r for r in results if not (r["match"] and r["snippet_in_v3"])]
num_parts = {}
bounds =[(0, n_part1, "part1_carried_v1"), (n_part1, n_part2, "part2_new_in_v2"), (n_part2, n_part3, "part3_text_register"),
          (n_part3, n_part4, "part4_probe_match"), (n_part4, n_part5, "part5_new_in_v3")]
for lo, hi, nm_ in bounds:
    num_parts[nm_] = {"n": hi - lo, "pass": sum(1 for r in results[lo:hi] if r["match"] and r["snippet_in_v3"])}
summary = {
    "sha_checks_ok": all(v_["ok"] for v_ in sha_checks.values()),
    "n3_status": {dk: ("fixed" if v_["ok"] else "NOT FIXED") for dk, v_ in n3.items()},
    "general_ok": all(general.values()),
    "number_check": {"n_checks": len(results), "n_pass": len(results) - len(bad), "n_bad": len(bad),
                     "recheck_carried_129": {"n": n_part3, "pass": sum(1 for r in results[:n_part3] if r["match"] and r["snippet_in_v3"])},
                     "by_part": num_parts},
    "diff_hunks_v2_to_v3": n_hunks,
}
out = {"meta": {"script": "research/plan110_n1/v3/check_v3.py", "adapted_from": "research/plan110_n1/recheck/recheck_draft.py",
                "python": sys.version,
                "flags": {"isolated": sys.flags.isolated, "no_site": sys.flags.no_site,
                          "dont_write_bytecode": sys.flags.dont_write_bytecode},
                "inputs_sha256": {**{k: sha(p) for k, p in F.items()}, "v1": sha_v1, "v2": sha_v2, "v3": sha_v3,
                                  "RK": sha(RK_PATH), "V3N": sha(V3N_PATH), "DP1": sha(DP1)},
                "label": "checks compare quoted v3 numbers to file values or to values re-derived here from primary files"},
       "summary": summary, "sha_checks": sha_checks, "n3_phrase_checks": n3, "general_checks": general,
       "n_checks": len(results), "n_bad": len(bad), "bad_ids": [r["id"] for r in bad],
       "checks": results, "probes": probe}
if not DRY:
    with open(DIFF, "x", encoding="utf-8") as fh:
        fh.writelines(diff_lines)
    with open(OUT, "x", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, default=str)
row("summary", {**summary, "out": OUT, "diff": DIFF, "v3_sha256": sha_v3})
print(json.dumps(summary, indent=1))
print("sha_checks", {k_: v_["ok"] for k_, v_ in sha_checks.items()})
print("general", general)
for dk, v_ in n3.items():
    for i_ in v_["items"]:
        if not i_["ok"]:
            print("N3 FAIL", dk, i_)
for r in bad:
    print("BAD", r["id"], "in_v3=", r["snippet_in_v3"], "quoted=", r["quoted"], "file=", r["file_value"])
