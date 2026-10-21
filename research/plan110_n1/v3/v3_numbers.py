"""v3 numbers: the few values the v3 touch-up of FRONTIER_NEGATIVE_RESULT_DRAFT_v2.md quotes
that are not already printed in results/plan110_n1/recheck/number_recheck.json -> probes,
plus the probe values themselves re-derived from the primary N1 / W0 files for cross-checking.

New here (not in the probes): the certified-with-direction-select per-cell limits, the
k = 379.3 behind the combined certified reading, the 0.864 direction-select ratio, and the
all-free D_eff values 114 / 112 / 724 behind the section 6 lever 3 correction.

Run from the repo root:
  .context/frontier_t0_env/Scripts/python.exe -I -S -B research/plan110_n1/v3/v3_numbers.py

stdlib only. Output (exclusive create): results/plan110_n1/v3/v3_numbers.json.
One row is appended to results/plan110_n1/v3/rows.jsonl. All values "modelled (derived)"
unless a direct file copy (then the source file's label).
"""
import hashlib
import json
import sys

F = {
    "HT": "results/plan110_n1/headline/headline_table.json",
    "ES": "results/plan110_n1/estimator/estimator_recompute.json",
    "HW": "results/plan110_n1/hwclassical/hw_classical_card_v2.json",
    "DC": "results/plan110_n1/review/dirsel_confirm.json",
    "RK": "results/plan110_n1/recheck/number_recheck.json",
    "REG": "results/plan110_w0/register/run001/register.json",
}
OUT = "results/plan110_n1/v3/v3_numbers.json"
ROWS = "results/plan110_n1/v3/rows.jsonl"
T_LAYER, SUPPLY = 1e-7, 1e12


def sha(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


J = {k: json.load(open(p, encoding="utf-8")) for k, p in F.items()}
HT, ES, HW, DC, RK = (J[k] for k in ("HT", "ES", "HW", "DC", "RK"))
probes = RK["probes"]
cell = {(c["case"], c["eps"]): c for c in HT["cells"]}
D = HT["D_eff_table"]
S = HT["summary_min_M_eligible_non_overhead"]
p1 = {(r["case"], r["eps"], r["split"]): r for r in ES["part1_k_eff_today"]}
p2 = {(r["case"], r["eps"]): r for r in ES["part2_summary"]}
m7 = {(r["case"], r["eps"]): r for r in ES["part7_M_primary"]}
hwmin = HW["classical"]["M_minima"]
ratio_expl = DC["per_cell"]["B8x52|0.001"]["dirsel_ratio_explicit"]
B8 = cell[("B8x52", 0.001)]
out = {}

# N3-1: zero-bias reading (e = eps) combined with direction-select, binding cell
k_ds_eps = p1[("B8x52", 0.001, "eps")]["k_eff_direction_select"]
dmax_eps = B8["T_C"] / (10 * B8["sigma_over_e"] * 0.45 * T_LAYER)
out["N3_1_combined_reading"] = {
    "k_certified_dirsel_e_eq_eps": k_ds_eps,
    "certified_M": k_ds_eps * B8["D_eff_primary"]["used"] / dmax_eps,
    "dirsel_ratio_explicit_at_0.45eps (DC)": ratio_expl,
    "explicit_M_e_eq_eps (HT)": S["explicit_best"]["e_eq_eps"][0],
    "explicit_M_e_eq_eps_fail001 (HT)": S["explicit_best_fail001"]["e_eq_eps"][0],
    "explicit_M_approx": S["explicit_best"]["e_eq_eps"][0] * ratio_expl,
    "explicit_M_fail001_approx": S["explicit_best_fail001"]["e_eq_eps"][0] * ratio_expl,
    "window_M_e_eq_eps_fail001 (HT, already uses dirsel)": S["no_explicit_fail001"]["e_eq_eps"][0],
    "note": "explicit values approximate: HT has no explicit k with direction-select at e = eps",
}

# N3-2: all-free floor stacked with supply 1e13 or 10 ns (binding cell, explicit class)
d_max = B8["T_C"] / (10 * B8["sigma_over_e"] * T_LAYER)
k_e = B8["k"]["explicit_best"]
af = {"1e12|100ns": D["B8x52|all_free|W1e7|1e12|100ns"]["used"],
      "1e13|100ns": D["B8x52|all_free|W1e7|1e13|100ns"]["used"],
      "1e12|10ns": D["B8x52|all_free|W1e7|1e12|10ns"]["used"]}
out["N3_2_allfree_stacks"] = {
    "D_eff_allfree_layers": af,
    "M_allfree": k_e * af["1e12|100ns"] / d_max,
    "M_allfree_supply1e13": k_e * af["1e13|100ns"] / d_max,
    "M_allfree_10ns": k_e * af["1e12|10ns"] / (d_max * 10),
}

# N3-3 / N3-4: per-cell limits per controlled Grover iterate (primary conventions)
pc = {}
for (cs, ep) in (("B4x12", 0.01), ("B4x12", 0.001), ("B8x52", 0.01), ("B8x52", 0.001)):
    c = cell[(cs, ep)]
    dm = c["T_C"] / (10 * c["sigma_over_e"] * T_LAYER)
    kds = p1[(cs, ep, "0.45eps")]["k_eff_direction_select"]
    pc[f"{cs}|{ep}"] = {
        "D_max_k1": dm,
        "explicit_max_layers": dm / c["k"]["explicit_best"],
        "explicit_max_T": dm / c["k"]["explicit_best"] * SUPPLY * T_LAYER,
        "certified_max_layers": dm / c["k"]["certified"],
        "certified_dirsel_max_layers": dm / kds,
        "certified_dirsel_max_T": dm / kds * SUPPLY * T_LAYER,
        "W0_allfree_D_eff": D[f"{cs}|all_free|W1e7|1e12|100ns"]["W0"],
    }
b = pc["B8x52|0.001"]
out["N3_3_N3_4_limits"] = {
    "per_cell": pc,
    "binding_allfree_over_certified_limit": af["1e12|100ns"] / b["certified_max_layers"],
    "binding_allfree_over_certified_dirsel_limit": af["1e12|100ns"] / b["certified_dirsel_max_layers"],
}

# N3-5: abstract explicit row with direction-select
out["N3_5_explicit_dirsel"] = {
    "primary_M": m7[("B8x52", 0.001)]["M_N1_explicit_best_dirsel"],
    "symmetric_BM_M_approx": hwmin["box_muller_current_law|explicit_best"]["min_M_distfree"] * ratio_expl,
}

# N3-6: register record for E20 (quoted verbatim in section 7.2 / Appendix A)
e20 = [i for i in J["REG"]["items"] if i["id"] == "E20"][0]
out["N3_6_E20_register"] = {k: e20[k] for k in ("tier", "disposition", "kill_or_defer", "optimistic_max_factor")}

# N3-8: k for "Best explicit with direction-select" at the binding cell
out["N3_8_best_explicit_dirsel_k_B8"] = p2[("B8x52", 0.001)]["N1 best: all credits incl. dirsel"]["k"]

# cross-check against the re-check probes (same quantities, independent code path)
cmp = {
    "certified_M": (out["N3_1_combined_reading"]["certified_M"], probes["zero_bias_plus_dirsel"]["certified_M"]),
    "explicit_M_approx": (out["N3_1_combined_reading"]["explicit_M_approx"],
                          probes["zero_bias_plus_dirsel"]["explicit_M_approx (e=eps explicit x dirsel ratio at 0.45eps)"]),
    "explicit_M_fail001_approx": (out["N3_1_combined_reading"]["explicit_M_fail001_approx"],
                                  probes["zero_bias_plus_dirsel"]["explicit_fail001_e_eq_eps_x_dirsel_ratio_approx"]),
    "allfree+supply1e13": (out["N3_2_allfree_stacks"]["M_allfree_supply1e13"], probes["allfree_stacks_explicit_B8"]["allfree+supply1e13"]),
    "allfree+10ns": (out["N3_2_allfree_stacks"]["M_allfree_10ns"], probes["allfree_stacks_explicit_B8"]["allfree+10ns"]),
    "best_explicit_dirsel_k_B8": (out["N3_8_best_explicit_dirsel_k_B8"], probes["best_explicit_dirsel_k_B8"]),
    "explicit_dirsel_primary": (out["N3_5_explicit_dirsel"]["primary_M"], probes["explicit_all_credits_incl_dirsel"]["primary"]),
    "explicit_dirsel_symmetric": (out["N3_5_explicit_dirsel"]["symmetric_BM_M_approx"], probes["explicit_all_credits_incl_dirsel"]["symmetric_BM"]),
}
for key in ("explicit_max_layers", "explicit_max_T", "certified_max_layers", "W0_allfree_D_eff"):
    for ck in pc:
        cmp[f"{ck}|{key}"] = (pc[ck][key], probes["per_cell_thresholds"][ck][key])
out["cross_check_vs_recheck_probes"] = {
    k: {"v3": a, "probe": p, "rel_diff": abs(a - p) / abs(p) if p else abs(a - p)} for k, (a, p) in cmp.items()}
max_rel = max(v["rel_diff"] for v in out["cross_check_vs_recheck_probes"].values())

doc = {"meta": {"script": "research/plan110_n1/v3/v3_numbers.py", "python": sys.version,
                "flags": {"isolated": sys.flags.isolated, "no_site": sys.flags.no_site,
                          "dont_write_bytecode": sys.flags.dont_write_bytecode},
                "inputs_sha256": {k: sha(p) for k, p in F.items()},
                "label": "modelled (derived) unless a direct file copy", "direction": "see each N3 item"},
       "max_rel_diff_vs_probes": max_rel, "values": out}
with open(OUT, "x", encoding="utf-8") as fh:
    json.dump(doc, fh, indent=1)
with open(ROWS, "a", encoding="utf-8") as fh:
    fh.write(json.dumps({"ws": "v3", "sub": "v3_numbers", "out": OUT, "sha256": sha(OUT),
                         "max_rel_diff_vs_probes": max_rel, "label": "modelled (derived)"}) + "\n")
print("max_rel_diff_vs_probes", max_rel)
print(json.dumps(out, indent=1))
