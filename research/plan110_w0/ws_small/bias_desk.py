"""WS-small bias desk (plan110 W0, rigour R0 screen).

Task A1: decompose the certified continuous-to-native dollar bias bounds
(B4x12 $0.000205060901822378, B8x52 $0.001239557505461456) of
A02_BM_native_financial_bridge_run002 into their component terms, and price
tightening options (lower stock clamp / better clip bounding / finer uniform
grid) against the $0.00055 = 0.55*eps target at eps = $0.001.

Task A2: close C14's "per-call = 2 x forward" depth reading from the saved
E02_financial_run002 per-iterate records.

Stdlib only. Run from anywhere with
    .context/frontier_t0_env/Scripts/python.exe -I -S -B research/plan110_w0/ws_small/bias_desk.py
Writes exactly one new folder results/plan110_w0/ws_small/bias_desk_<run>/ (exclusive create).

Formulas are transcribed from the executed producer
A02_BM_native_financial_bridge_run002/executed_code/experiment_box_muller_native_financial_bridge_v2.py
(closed_barrier_bands, smooth_payoff_bounds, complete_financial_bounds). Scenario values are
MODELLED (float logs on exact Fraction inputs, not interval-certified).
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
A02 = ROOT / "results/limitation_program_20261001/A02_BM_native_financial_bridge_run002"
A02_AUDIT = ROOT / "results/limitation_program_20261001/A02_BM_native_financial_bridge_audit_run002"
E02 = ROOT / "results/limitation_program_20261001/E02_financial_run002"
A10_SRC = ROOT / "results/limitation_program_20261001/A10_coefficient_run001"
OUT_PARENT = ROOT / "results/plan110_w0/ws_small"

Q, N = 1 << 40, 1 << 32  # producer constants (line 45 of the executed producer)
EPS_CONTRACT = Fraction(1, 1000)
TARGET = Fraction(55, 100) * EPS_CONTRACT  # 0.55*eps headroom -> e >= 0.45 eps
CASES = {"B4x12": (4, 12, 30), "B8x52": (8, 52, 234)}
SWITCH_CAP = Fraction(40)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fr(pair) -> Fraction:
    return Fraction(pair[0], pair[1])


def load(path: Path, inputs: dict):
    inputs[str(path.relative_to(ROOT)).replace("\\", "/")] = sha(path)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def log_ratio(upper: Fraction, lower: Fraction) -> float:
    """ln(upper/lower) via log1p of the exact relative gap (float, modelled)."""
    return math.log1p(float((upper - lower) / lower))


def case_model(case, bands, smooth, bounds, ell_scale=Fraction(1), ell_floor_only=False,
               n_scale=1, cap=SWITCH_CAP):
    """Recompute every term; ell_scale multiplies the clamp leakage (ell - beta).

    n_scale multiplies the uniform grid size N in the 1/N terms only (DS held fixed).
    Gaussian terms are rescaled from the CERTIFIED per-date values by the modelled
    ratio of log band widths, so the baseline reproduces the record exactly.
    """
    assets, dates, pairs = CASES[case]
    b = bands["cases"][case]
    beta = fr(b["beta_upper"])
    ell0 = fr(b["ell_upper"])
    leak0 = ell0 - beta
    ell = beta if ell_floor_only else leak0 * ell_scale + beta
    eps_lsb = Fraction(1, Q)
    DS = fr(bands["pinned_squared_radius_KS_upper"])
    gauss = Fraction(0)
    gauss_float = 0.0
    pair = Fraction(0)
    for row in b["dates"]:
        a, bb = fr(row["a_lower"]), fr(row["b_upper"])
        up = (140 + beta + eps_lsb) / a
        lo0, lo = (140 - ell0) / bb, (140 - ell) / bb
        assert lo0 == fr(row["closed_band_lower"]) and up == fr(row["closed_band_upper"])
        g0 = fr(row["gaussian_closed_band_probability_upper"])
        ratio = log_ratio(up, lo) / log_ratio(up, lo0)
        gauss_float += float(g0) * ratio
        j = row["elapsed_dates"]
        rp = ((assets + 1) * j + 1) // 2
        assert rp == row["relevant_whole_pairs"]
        allow = rp * (4 * DS + Fraction(2, N * n_scale))
        if n_scale == 1:
            assert allow == fr(row["pair_law_allowance"])
        pair += allow
        gauss += g0
    s = smooth["cases"][case]
    d_hat = Fraction(s["actual_discount_literal"], Q)
    zeta0 = fr(s["smooth_discounted_payoff_error_upper"])
    # every date error contains max(beta, ell) = ell once; averaged over dates -> d_hat*ell
    zeta = zeta0 - d_hat * (ell0 - ell)
    cb = bounds["cases"][case]
    C_up = fr(cb["pinned_primary_exact_cap_enclosure"][1])
    H_ks = pairs * 4 * C_up * DS
    H_grid = pairs * C_up * Fraction(dates + 1, N * n_scale)
    H0 = fr(cb["pinned_primary_hybrid_price_upper"])
    if n_scale == 1:
        assert H_ks + H_grid == H0
    terms = {
        "H_price_polar_KS_radius": float(H_ks),
        "H_price_polar_angle_grid_1_over_N": float(H_grid),
        "zeta_smooth_payoff": float(zeta),
        "switch_gaussian_band_x_cap": float(cap) * gauss_float,
        "switch_pair_law_KS_x_cap": float(cap * pairs_sum_ks(b, DS, assets)),
        "switch_pair_law_grid_x_cap": float(cap * (pair - pairs_sum_ks(b, DS, assets))),
    }
    total = sum(terms.values())
    return dict(
        ell=float(ell), terms=terms, total=total,
        baseline_gauss_sum_certified=float(gauss),
    )


def pairs_sum_ks(b, DS, assets):
    return sum(((assets + 1) * r["elapsed_dates"] + 1) // 2 for r in b["dates"]) * 4 * DS


def main():
    run = sys.argv[1] if len(sys.argv) > 1 else "run001"
    out = OUT_PARENT / f"bias_desk_{run}"
    out.mkdir(parents=True, exist_ok=False)
    inputs = {}
    bands = load(A02 / "closed_barrier_bands.json", inputs)
    smooth = load(A02 / "smooth_payoff_bounds.json", inputs)
    bounds = load(A02 / "complete_financial_bounds.json", inputs)
    audit_summary = load(A02_AUDIT / "summary.json", inputs)
    inputs["results/limitation_program_20261001/A02_BM_native_financial_bridge_run002/executed_code/experiment_box_muller_native_financial_bridge_v2.py"] = sha(
        A02 / "executed_code/experiment_box_muller_native_financial_bridge_v2.py")

    result = {"schema": "plan110-w0-ws_small-bias-desk-v1", "rigour": "R0 screen",
              "audit_summary_passed": audit_summary.get("passed"),
              "eps_contract": float(EPS_CONTRACT), "target_bias": float(TARGET), "cases": {}}
    selfcheck = {}
    for case in CASES:
        base = case_model(case, bands, smooth, bounds)
        cert = float(fr(bounds["cases"][case]["continuous_to_native_dollars_upper"]))
        selfcheck[case] = {"recomputed_total": base["total"], "certified_total": cert,
                           "rel_diff": abs(base["total"] - cert) / cert}
        assert selfcheck[case]["rel_diff"] < 1e-12, selfcheck[case]
        shares = {k: v / base["total"] for k, v in base["terms"].items()}
        clamp_k = {}
        for k in (1, 2, 3, 4, 6, 8, 16, 24):
            m = case_model(case, bands, smooth, bounds, ell_scale=Fraction(1, 1 << k))
            clamp_k[str(k)] = {"ell": m["ell"], "total": m["total"],
                               "total_over_eps": m["total"] / float(EPS_CONTRACT),
                               "meets_0p55eps": m["total"] <= float(TARGET), "terms": m["terms"]}
        ideal = case_model(case, bands, smooth, bounds, ell_floor_only=True)
        q33 = case_model(case, bands, smooth, bounds, n_scale=2)
        q33_k3 = case_model(case, bands, smooth, bounds, n_scale=2, ell_scale=Fraction(1, 8))
        cap_tight = case_model(case, bands, smooth, bounds,
                               cap=fr(smooth["cases"][case]["native_cap_upper"]))
        k_min = next((int(k) for k, v in clamp_k.items() if v["meets_0p55eps"]), None)
        result["cases"][case] = {
            "baseline_terms_usd": base["terms"], "baseline_shares": shares,
            "baseline_total_usd": base["total"], "ell_usd": base["ell"],
            "ell_driven_share": shares["switch_gaussian_band_x_cap"] + shares["zeta_smooth_payoff"],
            "clamp_lowered_by_k_binades": clamp_k,
            "min_k_binades_for_0p55eps": k_min,
            "ideal_clip_split_ell_to_lsb": {"total": ideal["total"], "terms": ideal["terms"]},
            "q33_grid_only_DS_fixed": {"total": q33["total"], "terms": q33["terms"]},
            "q33_plus_clamp_k3": {"total": q33_k3["total"]},
            "switch_cap_40_to_native_cap": {"cap": float(fr(smooth["cases"][case]["native_cap_upper"])),
                                            "total": cap_tight["total"]},
        }

    # ---- Task A2: per-call depth convention from E02 per-iterate records ----
    depth = {}
    for case in CASES:
        it = load(E02 / case / "iterate.json", inputs)
        costs = it["financial_native_costs"]
        fwd = sum(max(costs[c["leaf"]]["forward"]["t_depth"] for c in b["calls"])
                  for b in it["financial_batches"])
        inv = sum(max(costs[c["leaf"]]["inverse"]["t_depth"] for c in b["calls"])
                  for b in it["financial_batches"])
        fin = it["financial_resources"]["t_depth"]
        sel = it["selector_costs"]["forward"]["t_depth"] + it["selector_costs"]["inverse"]["t_depth"]
        refl = it["reflection_resources"]["t_depth"]
        per_call = it["resources"]["t_depth"]
        src_path = A10_SRC / case / "min-depth" / "source.json"
        src_sha = sha(src_path)
        depth[case] = {
            "sequence": it["sequence"],
            "forward_F_t_depth": fwd, "inverse_F_t_depth": inv,
            "F_plus_Finv_t_depth": fin, "fwd_plus_inv_equals_recorded": fwd + inv == fin,
            "selector_pair_t_depth": sel, "reflection_t_depth": refl,
            "per_call_iterate_t_depth": per_call,
            "sum_check": fin + sel + refl == per_call,
            "per_call_over_clean_source": per_call / fin,
            "C14_reading_2x_source": 2 * fin,
            "C14_overstatement_vs_per_call": 2 * fin / per_call,
            "iterate_bound_source_sha256": it["binding"]["hashes"]["source.json"],
            "A10_min_depth_source_sha256": src_sha,
            "same_source_as_A10_accepted": src_sha == it["binding"]["hashes"]["source.json"],
            "depth_convention_record": it["depth_convention"],
        }
    result["depth_convention"] = depth
    result["selfcheck"] = selfcheck
    result["inputs_sha256"] = inputs
    result["interpreter"] = sys.version
    with open(out / "bias_desk.json", "x", encoding="utf-8") as f:
        json.dump(result, f, indent=1)
    print(json.dumps({c: {"total": v["baseline_total_usd"], "shares": v["baseline_shares"],
                          "k_min": v["min_k_binades_for_0p55eps"],
                          "k": {k: round(x["total"], 9) for k, x in v["clamp_lowered_by_k_binades"].items()},
                          "ideal": v["ideal_clip_split_ell_to_lsb"]["total"],
                          "q33": v["q33_grid_only_DS_fixed"]["total"],
                          "q33k3": v["q33_plus_clamp_k3"]["total"],
                          "cap": v["switch_cap_40_to_native_cap"]}
                      for c, v in result["cases"].items()}, indent=1))
    print(json.dumps(depth, indent=1))
    print(json.dumps(selfcheck))


if __name__ == "__main__":
    main()
