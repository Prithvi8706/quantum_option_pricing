"""Number check for FRONTIER_NEGATIVE_RESULT_DRAFT_v4.md after the 22 Oct debt update. Copy of
research/frontier_probe_20261021/v4_check.py (not edited) with the original checks unchanged plus checks for every
debt-update number (A2a, U1, C11/U2, C03, H06/H17/H18, scope #44, register run009) and a few structural assertions.
Every number is recomputed from the result JSONs and must (a) appear verbatim in the draft and (b) equal the
recomputed value after rounding to the precision written.
Run (worktree root): ../../../.context/frontier_t0_env/Scripts/python.exe -I -S -B research/claim_debts_20261022/v4_check_debts.py [out_json]
"""
import hashlib
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DRAFT = ROOT / "manuscript/advantage-frontier-2026-09-23/FRONTIER_NEGATIVE_RESULT_DRAFT_v4.md"
R = ROOT / "results"
IN = dict(
    head=R / "frontier_probe_20261021/headline/run006/headline_table.json",
    p2=R / "frontier_probe_20261021/p2/run002/p2_window.json",
    sm=R / "frontier_probe_20261021/p2/run003_self_mean/p2c_self_mean.json",
    p1=R / "frontier_probe_20261021/p1/run001/p1_span.json",
    p1b=R / "frontier_probe_20261021/p1/run002/p1b_hybrid.json",
    p3=R / "frontier_probe_20261021/p3/run006/p3_desk.json",
    h16=R / "c10_challengers_20261022/h16_fast/run001/h16_fast.json",
    f32c=R / "c10_challengers_20261022/f32_consistency/run001/f32_consistency.json",
    ov=R / "c10_challengers_20261022/overrides_run006.json",
    c09_b8=R / "c10_challengers_20261022/c09/B8x52_0.001_run001/c09_g4.json",
    c09_b4=R / "c10_challengers_20261022/c09/case0_0.001_run001/c09_g4.json",
    c09_b8c=R / "c10_challengers_20261022/c09/case1_0.01_run001/c09_g4.json",
    c09_b4c=R / "c10_challengers_20261022/c09/case0_0.01_run001/c09_g4.json",
    c09b_b8=R / "c10_challengers_20261022/c09b/B8x52_0.001_run001/c09b_rep.json",
    c09b_b4=R / "c10_challengers_20261022/c09b/case0_0.001_run001/c09b_rep.json",
    c09b_b8c=R / "c10_challengers_20261022/c09b/case1_0.01_run001/c09b_rep.json",
    c09b_b4c=R / "c10_challengers_20261022/c09b/case0_0.01_run001/c09b_rep.json",
    tf32=R / "c10_challengers_20261022/timing_f32/run001/c10_timing_f32.json",
    a2a=R / "claim_debts_20261022/a2a/run001/summary.json",
    u1=R / "claim_debts_20261022/u1/run001/summary.json",
    c11=R / "claim_debts_20261022/c11/run001/summary.json",
    u2=R / "claim_debts_20261022/c11/run001/u2_wrapper.json",
    c03=R / "claim_debts_20261022/c03/run001/c03_ledger.json",
    h617=R / "claim_debts_20261022/h06_h17/run004/h06_h17.json",
    s44=R / "claim_debts_20261022/scope44/run001/scope44_receipt.json",
    reg9=R / "plan110_w0/register/run009/register.json",
    e02=R / "limitation_program_20261001/E02_financial_run002/B8x52/iterate.json",
)
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else R / "claim_debts_20261022/v4_check/run001.json"


def j(k):
    return json.loads(IN[k].read_text(encoding="utf-8"))


def fmt_ok(token, value):
    t = token.replace(",", "")
    dec = len(t.split(".")[1]) if "." in t and "e" not in t else 0
    if "e" in t:
        mant, ex = t.split("e")
        d = len(mant.split(".")[1]) if "." in mant else 0
        ref = float(f"{value:.{d}e}")
        return abs(float(t) - ref) <= 0.5 * 10 ** (-d) * 10 ** int(ex) + 1e-300, ref
    ref = round(value, dec)
    return abs(float(t) - value) <= 0.5 * 10 ** (-dec) + 1e-12, ref


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    text = DRAFT.read_text(encoding="utf-8")
    h = j("head")
    s = h["summary_min_M_eligible_non_overhead"]
    cell = [c for c in h["cells"] if c["case"] == "B8x52" and c["eps"] == 0.001][0]
    sm_k = j("sm")["cells"]["B8x52|0.001"]["best"]["k"]
    ratio_sm = sm_k / cell["k"]["window_certified_fail0003"]
    TC = cell["T_C"]
    se = cell["sigma_over_e"]
    D = cell["D_eff_primary"]["used"]
    dmax = TC / (10 * se * 1e-7)
    W = "window_certified_fail0003"
    p1 = j("p1")["cases"]["B8x52"]
    p1b = j("p1b")
    p3 = j("p3")["classes"][W]["designs"]
    h16 = j("h16")["cells"]["B8x52_H140|0.001"]["preint_fast"]["ratio_1_over_16"]
    ov = j("ov")
    checks = [
        ("T_C binding", "8.886", TC),
        ("T_C 8.89", "8.89", TC),
        ("T_C B4 0.001", "1.0475", h["T_C"]["B4x12|0.001"]["T_C"]),
        ("T_C B8 0.01", "0.3062", h["T_C"]["B8x52|0.01"]["T_C"]),
        ("T_C B4 0.01", "0.0583", h["T_C"]["B4x12|0.01"]["T_C"]),
        ("speedup product", "2.535", ov["overrides"]["tc_speedup"]["B8x52_H140|0.001"]),
        ("fast speedup QF", "2.078", ov["f32_applied"]["B8x52_H140|0.001"]["speedup_run005"]),
        ("f32 ratio", "1.220", ov["f32_applied"]["B8x52_H140|0.001"]["f32_over_fast"]),
        ("f32 B8 time", "4.11", j("tf32")["cells"]["B8x52_H140|0.001"]["median_wall"]["preint_fast32"]),
        ("sigma/e", "11,518.7", se),
        ("D_max(k=1)", "771.5", dmax),
        ("k_10x", "0.336", dmax / D),
        ("D_eff W0", "2,296", D),
        ("D_eff N1", "3,605", cell["D_eff_primary"]["N1"]),
        ("k certified", "682.7", cell["k"]["certified"]),
        ("k canonical", "197.6", cell["k"]["explicit_best"]),
        ("k window", "8.762", cell["k"][W]),
        ("k window 0.01", "7.359", cell["k"]["window_certified_fail001"]),
        ("k selfmean", "9.058", sm_k),
        ("k noDS", "17.52", cell["k"]["window_certified_noDS_fail0003"]),
        ("k noU1U2", "25.80", cell["k"]["window_certified_noU1U2_fail0003"]),
        ("k canonical 0.01", "144.9", cell["k"]["explicit_best_fail001"]),
        ("M certified", "2,032", s["certified"]["primary"][0]),
        ("M canonical", "588.1", s["explicit_best"]["primary"][0]),
        ("M canonical 0.01", "431.3", s["explicit_best_fail001"]["primary"][0]),
        ("M window", "26.1", s[W]["primary"][0]),
        ("M window 0.01", "21.9", s["window_certified_fail001"]["primary"][0]),
        ("M selfmean", "27.0", s[W]["primary"][0] * ratio_sm),
        ("M noDS", "52.2", s["window_certified_noDS_fail0003"]["primary"][0]),
        ("M noU1U2", "76.8", s["window_certified_noU1U2_fail0003"]["primary"][0]),
        ("all-free window", "1.29", s[W]["all_free_oracle"][0]),
        ("all-free selfmean", "1.34", s[W]["all_free_oracle"][0] * ratio_sm),
        ("all-free canonical", "29.2", s["explicit_best"]["all_free_oracle"][0]),
        ("all-free certified", "100.9", s["certified"]["all_free_oracle"][0]),
        ("symmetric window", "1.50", s[W]["distfree_stageC"][0]),
        ("symmetric selfmean", "1.55", s[W]["distfree_stageC"][0] * ratio_sm),
        ("symmetric canonical", "33.9", s["explicit_best"]["distfree_stageC"][0]),
        ("symmetric certified", "117.1", s["certified"]["distfree_stageC"][0]),
        ("allfree+sym window", "0.075", s[W]["all_free_distfree_stageC"][0]),
        ("allfree+sym selfmean", "0.077", s[W]["all_free_distfree_stageC"][0] * ratio_sm),
        ("allfree+sym canonical", "1.68", s["explicit_best"]["all_free_distfree_stageC"][0]),
        ("allfree+sym certified", "5.82", s["certified"]["all_free_distfree_stageC"][0]),
        ("1 lane window", "2.71", s[W]["one_lane_one_core"][0]),
        ("e=eps window", "11.7", s[W]["e_eq_eps"][0]),
        ("ineligible window", "36.2", s[W]["primary_B8_0.001_ineligible"][0]),
        ("supply 1e13 window", "8.40", s[W]["supply_1e13"][0]),
        ("10ns window", "22.5", s[W]["t_layer_10ns"][0]),
        ("W1e8 window", "21.3", s[W]["width_W1e8"][0]),
        ("distfree x5 window", "5.22", s[W]["distfree_x5"][0]),
        ("supply 1e11 window", "225", s[W]["supply_1e11"][0]),
        ("W1e6 window", "73.7", s[W]["width_W1e6"][0]),
        ("1us window", "84.0", s[W]["t_layer_1us"][0]),
        ("10us window", "840", s[W]["t_layer_10us"][0]),
        ("N1 floor window", "40.9", cell["M_N1_floor_only_primary"][W]),
        ("StageC sensitivity window", "10.3", s[W]["primary"][0] * TC / 22.529285950004123),
        ("limit window layers", "88.1", dmax / cell["k"][W]),
        ("limit window T", "8.8e6", dmax / cell["k"][W] * 1e5),
        ("limit selfmean layers", "85.2", dmax / sm_k),
        ("limit canonical layers", "3.90", dmax / cell["k"]["explicit_best"]),
        ("limit certified layers", "1.13", dmax / cell["k"]["certified"]),
        ("allfree over limit", "1.29", 114 / (dmax / cell["k"][W])),
        ("hardware t_layer ns", "11.9", (TC / 10 / (cell["k"][W] * se)) / 740 * 1e9),
        ("hardware T/s", "2.6e13", D * 1e5 / (TC / 10 / (cell["k"][W] * se))),
        ("P3 free loader", "13.8", p3["W0:free_loader_F05"]["M"]),
        ("P3 best loader+free exp", "2.45", p3["W0:best_loader+free_exp_A13"]["M"]),
        ("P3 N1 free loader exp", "1.96", p3["N1:free_loader_exp_n72"]["M"]),
        ("c(0.003)", "4.179", j("p2")["certified"]["delta=3/1000|gamma=0|with_impl_budget"]["c_certified"]),
        ("c(0.01)", "3.510", j("p2")["certified"]["delta=1/100|gamma=0|with_impl_budget"]["c_certified"]),
        ("N calls", "100,924", j("p2")["k"]["B8x52|0.001|0.45eps|8192/211|price+L1|with_impl_budget|fail 3/1000"]["N_calls"]),
        ("SM N1", "1,730", j("sm")["cells"]["B8x52|0.001"]["best"]["N1"]),
        ("SM N2", "102,602", j("sm")["cells"]["B8x52|0.001"]["best"]["N2"]),
        ("SM mU", "3.418", j("sm")["cells"]["B8x52|0.001"]["best"]["m_U_worst"]),
        ("SM c1", "6.052", j("sm")["cells"]["B8x52|0.001"]["best"]["c1"]),
        ("SM c2", "4.197", j("sm")["cells"]["B8x52|0.001"]["best"]["c2"]),
        ("H16 fast ratio", "9.62", h16),
        ("H16 f32 ratio", "9.56", j("f32c")["ratio_1_over_16"]),
        ("C09 iid B8", "33.8", j("c09_b8")["factor_df_over_practice"]),
        ("C09 iid B4", "37.6", j("c09_b4")["factor_df_over_practice"]),
        ("C09 iid B8c", "16.1", j("c09_b8c")["factor_df_over_practice"]),
        ("C09 iid B4c", "10.3", j("c09_b4c")["factor_df_over_practice"]),
        ("C09b B8", "17.3", j("c09b_b8")["factor_df_over_practice"]),
        ("C09b B4", "17.9", j("c09b_b4")["factor_df_over_practice"]),
        ("C09b B8c", "83.5", j("c09b_b8c")["factor_df_over_practice"]),
        ("C09b B4c", "49.3", j("c09b_b4c")["factor_df_over_practice"]),
        ("C09 f32", "17.5", j("f32c")["factor_df_over_practice"]),
        ("P1 span", "38.635", p1["raw"]["C1_geo_call"]["S_res_lower_bound"]),
        ("P1 U1 gain max", "1.59", max(v.get("gain_U1_max") or 0 for v in p1["raw"].values())),
        ("P1 pre lower", "15.61", p1["pre"]["replacement"]["S_h_lower_bound"]),
        ("P1 pre upper", "17.29", p1["pre"]["replacement"]["S_h_upper_bound"]),
        ("P1 pre gain lin", "2.49", p1["pre"]["replacement"]["gain_linear_max"]),
        ("P1 pre gain U1", "1.70", p1["pre"]["replacement"]["gain_U1_max"]),
        ("P1 hybrid D1", "3.42", p1b["hybrid"]["best_at_D1"]["net_at_D1"]),
        ("P1 hybrid Dstruct", "2.62", p1b["hybrid"]["best_at_D1"]["net_at_D_lo"]),
        ("P1 D struct", "1.30", p1b["D_ratio_pre"]["structure_aware"]),
        ("P1 multidir", "0.70", p1b["multi_direction"]["rows"][1]["net_at_D_floor"]),
    ]
    pairs = {tuple(f["departures"]): f["min_M"] for f in h["stacked_departures"][W]["best_pairs"]}
    checks += [("pair allfree+1lane", "0.135", pairs[("all_free", "one_lane_one_core")]),
               ("pair 1lane+sym", "0.156", pairs[("one_lane_one_core", "distfree_stageC")])]
    trip = h["stacked_departures"]["explicit_best"]["minimal_sets"][0]["min_M"]
    tripc = h["stacked_departures"]["certified"]["minimal_sets"][0]["min_M"]
    checks += [("canonical triple", "0.175", trip), ("certified triple", "0.604", tripc)]
    # ---- debt update (22 Oct) ----
    a2 = j("a2a")["cases"]
    u1 = j("u1")
    c11 = j("c11")
    u2 = j("u2")
    c03 = j("c03")["variants"]
    vU, vQ = c03["window_certified_U1"], c03["window_quantum_only_mean"]
    hU = {r["basis"].split(" ")[0]: r for r in vU["h18_condition"]}
    hQ = {r["basis"].split(" ")[0]: r for r in vQ["h18_condition"]}
    hh = j("h617")
    h17 = {(r["k_class"], r["iterate"]): r for r in hh["H17_necessary_conditions"]}
    fl, sv = h17[("window_certified", "floor_supply_aware")], h17[("window_certified", "saved_source")]
    flq = h17[("window_quantum_only_mean", "floor_supply_aware")]
    ccz = hh["H06"]["ccz_convention"]
    s44 = j("s44")
    m44 = s44["M_binding_cell"]
    reg9 = j("reg9")["meta"]

    def fr(s):
        a, b = s.split("/")
        return int(a) / int(b)

    checks += [
        ("A2a B8 bias e", "3.634e-4", a2["B8x52"]["certified_total_float"]),
        ("A2a B8 bias $", "0.0003634", a2["B8x52"]["certified_total_float"]),
        ("A2a numerator", "6703058386012589", a2["B8x52"]["certified_total_upper_rounded_up_2^-64"][0]),
        ("A2a paths rel diff", "9.4e-13", a2["B8x52"]["relative_difference"]),
        ("A2a run002 total", "0.0012396", a2["B8x52"]["run002_certified_total"]),
        ("A2a spare", "0.000187", a2["B8x52"]["margin_to_target"]),
        ("A2a B4 bias", "0.00001207", a2["B4x12"]["certified_total_float"]),
        ("A2a clip sites", "104", a2["B8x52"]["clipable_sites"]),
        ("A2a P_fin(C)", "1e-29", 10.0 ** a2["B8x52"]["P_fin_C_upper_primary_Bernstein_log10_approx"]),
        ("U1 m_cert", "3.28804", u1["m_cert_float"]),
        ("U1 sample mean", "3.27960", u1["pieces"]["sample_mean"]),
        ("U1 EB half-width", "0.00808", u1["pieces"]["eb_half_width"]),
        ("U1 P2 m", "3.32682", u1["p2_assumed_m"]),
        ("U1 margin", "0.0388", u1["margin_to_p2_m"]),
        ("U1 k at m", "8.715", u1["window_k_at_m_cert"]),
        ("U1 M at m", "25.94", u1["window_M_at_m_cert"]),
        ("U1 delta", "1e-4", fr(u1["delta_U"])),
        ("C11 T literal", "4,267,659,718", c11["iterate"]["t_count_literal"]),
        ("C11 T qf", "2.44e9", c11["iterate"]["t_count_qf"]),
        ("C11 Toffolis", "609,665,674", c11["iterate"]["ccx"]),
        ("C11 width", "4,460,627", c11["width"]["total_upper"]),
        ("C11 Toffoli depth", "201,263", c11["iterate"]["toffoli_depth"]),
        ("C11 T-depth literal", "776,965", c11["iterate"]["t_depth"]),
        ("C11 ratio literal", "18.6", c11["iterate"]["floor_ratio_T_literal"]),
        ("C11 ratio qf", "10.6", c11["iterate"]["floor_ratio_T_qf"]),
        ("C11 M window qf", "2,290", c11["M"]["window_qf"]),
        ("C11 M literal", "8,828", c11["M"]["window_literal"]),
        ("C11 M most fav", "1,084", c11["M"]["window_most_favourable_qf"]),
        ("C11 D most fav", "95,101", c11["D_eff"]["most_favourable_qf"]),
        ("C11 M supply only", "277", c11["M"]["supply_only_qf"]),
        ("C11 D supply only", "24,387", c11["D_eff"]["supply_only_qf"]),
        ("C11 M over floor", "87.8", c11["M_over_floor"]["window_qf"]),
        ("C11 M selfmean qf", "2,367", c11["M"]["self_mean_qf"]),
        ("U2 T delta", "11,578", c11["u2_delta_per_iterate"]["t_count_total"]),
        ("U2 rel T", "2.7e-6", c11["u2_delta_per_iterate"]["relative_t"]),
        ("U2 qubits", "0", c11["u2_delta_per_iterate"]["extra_logical_qubits"]),
        ("U2 exhaustive", "40,000", c11["checks"]["u2_exhaustive_cases"]),
        ("U2 full width", "4,281", c11["checks"]["u2_full_width_cases"]),
        ("U2 readout", "4.55e-13", u2["readout"]["allowance_used"]),
        ("E03 sup Yraw", "42,680,645,956,484", j("e02")["binding"]["payoff_raw_bounds"][1]),
        ("C03 physical U1", "0.0069", fr(vU["failure_ledger"][-1]["allocation"])),
        ("C03 physical QOM", "0.007", fr(vQ["failure_ledger"][-1]["allocation"])),
        ("H18 floor U1", "2.98e-16", hU["W0"]["required_logical_failure_per_T"]),
        ("H18 floor QOM", "2.92e-16", hQ["W0"]["required_logical_failure_per_T"]),
        ("H18 compiled U1", "2.80e-17", hU["C11"]["required_logical_failure_per_T"]),
        ("H18 compiled QOM", "2.75e-17", hQ["C11"]["required_logical_failure_per_T"]),
        ("H18 T per estimate", "2.32e13", hU["W0"]["T_total"]),
        ("H17 floor ns M1", "11.6", fl["M<=1"]["t_layer_required_s"] * 1e9),
        ("H17 floor ns M10", "116", fl["M<=10"]["t_layer_required_s"] * 1e9),
        ("H17 floor T/s M1", "2.61e13", fl["M<=1"]["T_per_s_required"]),
        ("H17 floor T/s M10", "2.61e12", fl["M<=10"]["T_per_s_required"]),
        ("H17 saved ps M1", "11.4", sv["M<=1"]["t_layer_required_s"] * 1e12),
        ("H17 saved ps M10", "114", sv["M<=10"]["t_layer_required_s"] * 1e12),
        ("H17 saved T/s M1", "4.85e14", sv["M<=1"]["T_per_s_required"]),
        ("H17 saved T/s M10", "4.85e13", sv["M<=10"]["T_per_s_required"]),
        ("H17 saved M", "8,749", sv["M_primary"]),
        ("H17 floor T", "229,603,168", fl["T_per_call"]),
        ("H17 saved T", "4,267,435,214", sv["T_per_call"]),
        ("H17 saved layers", "770,356", sv["L_per_call"]),
        ("H17 QOM tighter %", "3.4", (flq["M_primary"] / fl["M_primary"] - 1) * 100),
        ("H06 AND per call", "57,400,792", hh["H06"]["composition"]["floor_supply_aware"]["AND_per_call"]),
        ("H06 CCZ/s", "6.5e12", fl["M<=1"]["CCZ_per_s_required_if_all_AND"]),
        ("H06 CCZ 2T M", "13.0", ccz["CCZ_2T_equiv"]["window_certified"]["floor_M"]),
        ("H06 CCZ native M", "8.63", ccz["CCZ_native_1_unit"]["window_certified"]["floor_M"]),
        ("H06 reaction floor M", "8.40", ccz["CCZ_2T_equiv"]["window_certified"]["floor_M_lower_bound_reaction"]),
        ("H06 all-free stays", "1.29", ccz["CCZ_2T_equiv"]["window_certified"]["all_free_M"]),
        ("S44 primary", "26.08", m44["window_certified_fail0003"]["primary"]),
        ("S44 QOM primary", "26.96", m44["window_quantum_only_mean"]["primary"]),
        ("S44 compiled", "2,286", m44["window_certified_fail0003"]["compiled_iterate_primary"]),
        ("S44 all-free", "1.29", m44["window_certified_fail0003"]["all_free_oracle"]),
        ("S44 one lane", "2.71", m44["window_certified_fail0003"]["one_lane_one_core"]),
        ("S44 symmetric", "1.50", m44["window_certified_fail0003"]["symmetric_distfree"]),
        ("S44 allfree+sym", "0.075", m44["window_certified_fail0003"]["all_free_plus_symmetric"]),
        ("REG9 rows changed", "13", reg9["changed"]),
    ]
    asserts = [
        ("A2a all checks pass", j("a2a")["all_checks_pass"] is True),
        ("A2a meets 0.55 eps", a2["B8x52"]["meets_target"] is True),
        ("U1 all checks pass and covers P2 m", u1["all_checks_pass"] is True and u1["p2_assumption_covered"] is True),
        ("C11 all checks pass", c11["all_checks_pass"] is True),
        ("C03 both variants complete", vU["complete"] is True and vQ["complete"] is True),
        ("C03 failure totals 1/100", vU["failure_total"] == "1/100" and vQ["failure_total"] == "1/100"),
        ("C03 dollar ledger complete and fits", j("c03")["dollar_ledger_complete"] is True
         and j("c03")["dollar_bias_fits_reserve"] is True),
        ("S44 matches run006 exactly", all(v["rel_diff"] == 0.0 for v in s44["comparison_with_run006"].values())),
        ("S44 independent agreement", s44["independent_agreement_1e-9"] is True),
        ("S44 eligible on certified bias", s44["eligibility"]["eligible_on_certified_bias"] is True),
        ("S44 NO-GO under every single departure", s44["decision"]["no_go_holds_all_explicit_single_departures"] is True),
        ("REG9 tiers as Appendix A", reg9["tiers"] == {"T1": 4, "T2": 6, "T3": 11, "T4": 31, "T5": 33, "T6": 25}),
        ("v3 draft unchanged (sha256 prefix c7ab400d)", hashlib.sha256(
            (ROOT / "manuscript/advantage-frontier-2026-09-23/FRONTIER_NEGATIVE_RESULT_DRAFT_v3.md").read_bytes()
        ).hexdigest().startswith("c7ab400d")),
    ]
    rows, npass = [], 0
    for name, ok in asserts:
        npass += bool(ok)
        rows.append(dict(check=name, assertion=True, ok=bool(ok)))
        if not ok:
            print("FAIL", name, flush=True)
    for name, token, value in checks:
        present = token in text
        ok, ref = fmt_ok(token, value)
        passed = present and ok
        npass += passed
        rows.append(dict(check=name, token=token, recomputed=value, rounded=ref, present_in_draft=present, ok=passed))
        if not passed:
            print("FAIL", name, token, value, "present" if present else "MISSING", flush=True)
    res = dict(meta=dict(script="research/claim_debts_20261022/v4_check_debts.py", python=sys.version,
                         draft_sha256=hashlib.sha256(DRAFT.read_bytes()).hexdigest(),
                         inputs_sha256={k: hashlib.sha256(p.read_bytes()).hexdigest() for k, p in IN.items()}),
               n_checks=len(rows), n_pass=npass, n_fail=len(rows) - npass, rows=rows)
    with open(OUT, "x", encoding="utf-8") as f:
        json.dump(res, f, indent=1)
    print(f"{npass}/{len(rows)} pass")


if __name__ == "__main__":
    main()
