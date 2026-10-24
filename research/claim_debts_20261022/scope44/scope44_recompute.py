"""Scope #44 independent recompute of the binding-cell headline row (B8x52, eps = $0.001).

Written from the definitions in docs/claim_debts_20261022/SCOPE44_PROSPECTUS.md; does not import or copy
headline_m.py / headline_m_probe.py. Reads raw inputs, recomputes M for the window classes and the
single/stacked departure columns, and compares with headline run006.

Usage (from the worktree root):
    <frontier_t0_env python> -I -S -B research/claim_debts_20261022/scope44/scope44_recompute.py RUN A2A C03 [C11]
A2A, C03, C11 are summary/ledger JSON paths, or "-" if absent.
"""
import hashlib
import json
import os
import sys

RUN = sys.argv[1]
OPT = {k: (sys.argv[i] if len(sys.argv) > i and sys.argv[i] != "-" else None)
       for i, k in ((2, "a2a"), (3, "c03"), (4, "c11"))}
OUT = os.path.join("results", "claim_debts_20261022", "scope44", RUN)

CASE, EPS = "B8x52", 0.001
KEY = "B8x52_H140|0.001"
SRC = {
    "p2_window": "results/frontier_probe_20261021/p2/run002/p2_window.json",
    "p2_self_mean": "results/frontier_probe_20261021/p2/run003_self_mean/p2c_self_mean.json",
    "sigma": "results/frontier_classical_20261001/sigma_dev/sigma_dev.json",
    "c2": "results/frontier_classical_20261001/c2/c2_timing.json",
    "c5": "results/frontier_classical_20261001/c5/timing/c5_timing.json",
    "overrides": "results/c10_challengers_20261022/overrides_run006.json",
    "floor_w0": "results/plan110_w0/ws_floor/floor.json",
    "floor_n1": "results/plan110_n1/headline/floor_sheet.json",
    "reference_run006": "results/frontier_probe_20261021/headline/run006/headline_table.json",
}
SRC.update({k: v for k, v in OPT.items() if v})


def read(name):
    with open(SRC[name], encoding="utf-8") as fh:
        return json.load(fh)


def digest(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


# ---- inputs -----------------------------------------------------------------------------------
pw = read("p2_window")["k"]
k_window = pw["B8x52|0.001|0.45eps|8192/211|price+L1|with_impl_budget|fail 3/1000"]["k_direction_select"]
k_selfmean = read("p2_self_mean")["cells"]["B8x52|0.001"]["best"]["k"]

sigma_q = read("sigma")["cases"][CASE]["sigma_q"]
sig_over_e = sigma_q / (0.45 * EPS)

ov = read("overrides")
speed = ov["f32_applied"][KEY]["speedup_run005"] * ov["f32_applied"][KEY]["f32_over_fast"]
assert abs(speed - ov["overrides"]["tc_speedup"][KEY]) < 1e-12 * speed
h16 = ov["overrides"]["h16_ratio"][KEY]
distfree = ov["overrides"]["distfree_factor"][KEY]

# Classical wall: smallest measured 'primary' wall over C2/C5 blocks at eps = 0.001 (the tightest target, so the
# monotone envelope is the cell itself); the preint block is divided by the paired fast-method speedup.
walls = []
for name in ("c2", "c5"):
    for block, val in read(name)["blocks"].items():
        case, method = block.split("/")
        if case != CASE:
            continue
        for e_key, rec in val["t_c"].items():
            if float(e_key) == EPS:
                t = rec["primary"] / (speed if method == "preint" else 1.0)
                walls.append((t, name, method, rec["primary"]))
T_C, T_src, T_method, T_stageC = min(walls)

w0 = read("floor_w0")["headline"][CASE]
n1 = read("floor_n1")["cases"][CASE]


def d_eff(n1_design, w0_design):
    a = n1[n1_design]["by_width"]["W1e7"]["1e12|100ns"]["D_eff"]
    b = w0["W1e7"][w0_design]["comparison"][0]["by_t_layer"]["100ns"]["base"]["eff_depth_supply_1e12"]
    return min(a, b), a, b


D_primary, D_p_n1, D_p_w0 = d_eff("primary_n72", "box_muller_current_law")
D_allfree, D_a_n1, D_a_w0 = d_eff("all_free_n48_f32", "all_free_and_narrow")
T_LAYER = 1e-7


def M(k, D=D_primary, tc=T_C):
    # M = k / k_10x with k_10x = T_C / (10 (sigma/e) D t_layer)
    return k * 10.0 * sig_over_e * D * T_LAYER / tc


def columns(k):
    return {
        "primary": M(k),
        "all_free_oracle": M(k, D=D_allfree),
        "one_lane_one_core": M(k, tc=T_C * h16),
        "symmetric_distfree": M(k, tc=T_C * distfree),
        "all_free_plus_symmetric": M(k, D=D_allfree, tc=T_C * distfree),
    }


rows = {"window_certified_fail0003": columns(k_window), "window_quantum_only_mean": columns(k_selfmean)}

c11 = read("c11") if OPT["c11"] else None
D_compiled = c11["D_eff"]["qf_floor_convention"] if c11 and c11.get("all_checks_pass") else None
if D_compiled:
    for name, k in (("window_certified_fail0003", k_window), ("window_quantum_only_mean", k_selfmean)):
        rows[name]["compiled_iterate_primary"] = M(k, D=D_compiled)

# ---- comparison with run006 ---------------------------------------------------------------------
ref = [c for c in read("reference_run006")["cells"] if c["case"] == CASE and abs(c["eps"] - EPS) < 1e-12][0]
refM = ref["M"]["window_certified_fail0003"]
pairs = {
    "primary": refM["primary"], "all_free_oracle": refM["all_free_oracle"],
    "one_lane_one_core": refM["one_lane_one_core"], "symmetric_distfree": refM["distfree_stageC"],
    "all_free_plus_symmetric": refM["all_free_distfree_stageC"],
}
comparison = {c: {"recomputed": rows["window_certified_fail0003"][c], "run006": v,
                  "rel_diff": abs(rows["window_certified_fail0003"][c] - v) / v} for c, v in pairs.items()}
inputs_match = {
    "T_C": abs(T_C - ref["T_C"]) / ref["T_C"],
    "sigma_over_e": abs(sig_over_e - ref["sigma_over_e"]) / ref["sigma_over_e"],
    "D_eff": abs(D_primary - ref["D_eff_primary"]["used"]) / ref["D_eff_primary"]["used"],
    "k_window": abs(k_window - ref["k"]["window_certified_fail0003"]) / ref["k"]["window_certified_fail0003"],
}
agree = all(v["rel_diff"] <= 1e-9 for v in comparison.values()) and all(v <= 1e-9 for v in inputs_match.values())

# ---- gates --------------------------------------------------------------------------------------
bias_reserve = 0.55 * EPS
a2a = read("a2a") if OPT["a2a"] else None
bias = None
if a2a and a2a.get("all_checks_pass") is True:
    b = a2a["cases"]["B8x52"]["certified_total_upper_rounded_up_2^-64"]
    bias = int(b[0]) / int(b[1]) if isinstance(b, list) else float(b)
eligible = bias is not None and bias <= bias_reserve
c03 = read("c03") if OPT["c03"] else None

explicit_cols = ["primary", "all_free_oracle", "one_lane_one_core", "symmetric_distfree"]
no_go = all(rows[r][c] > 1 for r in rows for c in explicit_cols)
margin = min(rows[r]["primary"] for r in rows)
out = {
    "meta": {"script": "research/claim_debts_20261022/scope44/scope44_recompute.py", "python": sys.version,
             "inputs_sha256": {k: digest(v) for k, v in SRC.items()}, "inputs": SRC,
             "prospectus": "docs/claim_debts_20261022/SCOPE44_PROSPECTUS.md",
             "prospectus_sha256": digest("docs/claim_debts_20261022/SCOPE44_PROSPECTUS.md")},
    "inputs_recomputed": {"k_window": k_window, "k_quantum_only_mean": k_selfmean, "sigma_q": sigma_q,
                          "sigma_over_e": sig_over_e, "T_C": T_C, "T_C_source": [T_src, T_method],
                          "T_C_stageC": T_stageC, "speedup": speed, "h16_ratio": h16, "distfree_factor": distfree,
                          "D_eff_primary": [D_primary, {"N1": D_p_n1, "W0": D_p_w0}],
                          "D_eff_all_free": [D_allfree, {"N1": D_a_n1, "W0": D_a_w0}],
                          "D_eff_compiled": D_compiled},
    "M_binding_cell": rows,
    "comparison_with_run006": comparison,
    "input_rel_diffs": inputs_match,
    "independent_agreement_1e-9": agree,
    "eligibility": {"bias_upper": bias, "reserve": bias_reserve, "eligible_on_certified_bias": eligible},
    "c03_status": c03.get("complete_price_status") if c03 else None,
    "decision": {"no_go_holds_all_explicit_single_departures": no_go, "window_margin_primary": margin,
                 "rigour": "R1" if margin >= 30 else "R1 delivered; R2 required by PLAN_110 sec. 4 (margin < 30x)"},
}
os.makedirs(OUT, exist_ok=False)
with open(os.path.join(OUT, "scope44_receipt.json"), "x", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1)
print(json.dumps({k: out[k] for k in ("M_binding_cell", "independent_agreement_1e-9", "eligibility", "decision")},
                 indent=1))
