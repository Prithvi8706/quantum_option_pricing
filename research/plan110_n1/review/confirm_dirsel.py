"""N2-reviewer: per-cell confirmation of the drafter's direction-select cross-products
(draft section 9.2 item 13 asks the reviewer to confirm 0.97 before it is quoted).

Path differs from draft_addendum.py: instead of multiplying the binding-cell minima, it
recomputes every eligible non-overhead cell (eps in {0.01, 0.001}, both cases, B8x52 $0.001
eligible as in the primary convention) from per-cell values and takes the minimum, so a
change of binding cell would show up.

Per cell (all modelled; T_C and the H16 ratio measured):
  M_allfree_1lane     = M_allfree(cell) / h16(cell)                (headline single departures)
  M_allfree_distfree  = M_allfree(cell) / C09factor(cell)          (hwclassical Stage-C factor)
  dirsel ratio        = k_dirsel(cell) / k(cell)  from estimator part7 (M ratio, same k_10x)
Also: the zero-bias-consistent reading (e = eps at B8x52 $0.001) of the pair all-free + 1 lane,
and the distribution-free M without the U1 mean credit (symmetric-rigour reading).

Run: .context/frontier_t0_env/Scripts/python.exe -I -S -B research/plan110_n1/review/confirm_dirsel.py
Output (exclusive create): results/plan110_n1/review/dirsel_confirm.json; appends rows.
"""
import hashlib
import json
import sys

F = {
    "HT": "results/plan110_n1/headline/headline_table.json",
    "ES": "results/plan110_n1/estimator/estimator_recompute.json",
    "HW": "results/plan110_n1/hwclassical/hw_classical_card_v2.json",
    "AD": "results/plan110_n1/drafter/addendum.json",
}
OUT = "results/plan110_n1/review/dirsel_confirm.json"
ROWS = "results/plan110_n1/review/rows.jsonl"
J = {k: json.load(open(p, encoding="utf-8")) for k, p in F.items()}
HT, ES, HW, AD = J["HT"], J["ES"], J["HW"], J["AD"]

cells = {(c["case"], c["eps"]): c for c in HT["cells"] if c["eps"] in (0.01, 0.001)}
p7 = {(r["case"], r["eps"]): r for r in ES["part7_M_primary"]}
c09 = {(r["case"], r["eps"]): r["factor_df_over_practice"] for r in HW["classical"]["rows"]}
p2s = {(r["case"], r["eps"]): r for r in ES["part2_summary"]}

per = {}
for key, c in cells.items():
    r = p7[key]
    ratio_e = r["M_N1_explicit_best_dirsel"] / r["M_W0_explicit_best"]
    ratio_c = r["M_certified_today_dirsel"] / r["M_certified_today"]
    Me, Mc = c["M"]["explicit_best"], c["M"]["certified"]
    k_nomean = p2s[key]["span+nondyadic (no mean cert)"]["k"]
    per["%s|%s" % key] = {
        "dirsel_ratio_explicit": ratio_e,
        "dirsel_ratio_certified": ratio_c,
        "explicit_allfree_1lane": Me["all_free_oracle"] / c["h16_ratio"],
        "explicit_allfree_1lane_dirsel": Me["all_free_oracle"] / c["h16_ratio"] * ratio_e,
        "explicit_allfree_distfree_dirsel": Me["all_free_oracle"] / c09[key] * ratio_e,
        "certified_allfree_distfree": Mc["all_free_oracle"] / c09[key],
        "certified_allfree_distfree_dirsel": Mc["all_free_oracle"] / c09[key] * ratio_c,
        "certified_allfree_1lane_dirsel": Mc["all_free_oracle"] / c["h16_ratio"] * ratio_c,
        "explicit_no_U1_distfree_BM": Me["primary"] / c09[key] * k_nomean / c["k"]["explicit_best"],
        "explicit_no_U1_distfree_allfree": Me["all_free_oracle"] / c09[key] * k_nomean / c["k"]["explicit_best"],
        "explicit_eq_eps_allfree_1lane": Me["all_free_oracle"] / c["h16_ratio"] * Me["e_eq_eps"] / Me["primary"],
    }

keys = list(next(iter(per.values())).keys())
mins = {}
for k in keys:
    if k.startswith("dirsel_ratio"):
        continue
    cell_min = min(per, key=lambda c: per[c][k])
    mins[k] = [per[cell_min][k], cell_min]

compare = {
    "explicit_allfree_1lane_dirsel": [mins["explicit_allfree_1lane_dirsel"][0], AD["explicit_dirsel"]["all_free+one_lane_one_core"]],
    "explicit_allfree_distfree_dirsel": [mins["explicit_allfree_distfree_dirsel"][0], AD["explicit_dirsel"]["all_free+distfree_stageC"]],
    "certified_allfree_distfree_dirsel": [mins["certified_allfree_distfree_dirsel"][0], AD["certified_dirsel"]["all_free+distfree_stageC"]],
    "explicit_allfree_1lane_vs_headline_pair": [mins["explicit_allfree_1lane"][0],
                                                HT["stacked_departures"]["explicit_best"]["best_pairs"][0]["min_M"]],
}
agree = all(abs(a - b) <= 1e-9 * abs(b) for a, b in compare.values())
out = {
    "meta": {"script": "research/plan110_n1/review/confirm_dirsel.py", "python": sys.version,
             "flags": {"isolated": sys.flags.isolated, "no_site": sys.flags.no_site},
             "inputs_sha256": {k: hashlib.sha256(open(p, "rb").read()).hexdigest() for k, p in F.items()},
             "label": "modelled (per-cell arithmetic on N1 values; T_C, H16 measured; dirsel call cost assumed)",
             "direction": "quantum-favourable departures"},
    "per_cell": per, "min_over_eligible_non_overhead": mins, "compare_to_drafter": compare,
    "drafter_values_confirmed": agree,
}
with open(OUT, "x", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1)
with open(ROWS, "a", encoding="utf-8") as fh:
    fh.write(json.dumps({"ws": "n2_review", "sub": "dirsel_crossproduct_confirm",
                         "value": {"confirmed": agree, "compare": compare},
                         "label": "modelled (derived; dirsel call cost assumed)", "direction": "quantum-favourable",
                         "source": OUT}) + "\n")
    fh.write(json.dumps({"ws": "n2_review", "sub": "symmetric_and_zero_bias_readings",
                         "value": {k: mins[k] for k in ("explicit_no_U1_distfree_BM", "explicit_no_U1_distfree_allfree",
                                                        "explicit_eq_eps_allfree_1lane", "certified_allfree_distfree",
                                                        "certified_allfree_1lane_dirsel")},
                         "label": "modelled (derived)", "direction": "quantum-favourable readings of the conventions",
                         "source": OUT}) + "\n")
print(json.dumps({"mins": mins, "compare": compare, "agree": agree}, indent=1))
