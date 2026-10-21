"""Render floor.md from floor.json (WS-floor, plan110 W0). Stdlib only; exclusive create."""

import argparse
import json
import os

CELLS_ORDER = (0.1, 0.03, 0.01, 0.001)


def f(x, nd=0):
    if x is None:
        return "n/a"
    if isinstance(x, float) and (abs(x) >= 1e5 or (0 < abs(x) < 1e-2)):
        return "%.2e" % x
    if isinstance(x, int) and abs(x) >= 1e5:
        return "%.2e" % x
    return ("{:,.%df}" % nd).format(x)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    a = ap.parse_args()
    d = json.load(open(os.path.join(a.dir, "floor.json"), encoding="utf-8"))
    H = d["headline"]
    L = []
    w = L.append
    w("# WS-floor: idealized clean-call reaction-layer floor (plan110 W0, R0 screen)\n")
    w("Items: A01, with A16, A09, A08, A02, A07, A13, F05, F20, A03 and A04 as parameters. "
      "Generated from `floor.json` by `render_md.py`. Every number below is **modelled** "
      "(idealized literature-constant constructions; quantum-favourable unless stated), except the "
      "D_max inputs (inherited from `gap_ledger.json`: T_C measured or fitted per cell) and the "
      "conventions (assumed, W0 card).\n")
    w("Unit: one **reaction layer** is one layer of parallel temporary-AND gates (A16). "
      "The call is forward plus reverse, so it is 2 x forward. "
      "**T-layers:** x1 with a T-depth-1 AND, x2 with a Gidney AND, x4 at the repo's measured CCX ratio of 4.0. "
      "Call T-count = 2 x 4 x forward ANDs.\n")

    w("## 1. Headline: floor per contract under each width (t_layer 100 ns)\n")
    w("| case | W | design | loader | call reaction layers | T-layers r=1/2/4 | loader share | "
      "T per call | width (qubits) | required T/s | supply-limited depth at 1e12 T/s |")
    w("|---|---|---|---|---|---|---|---|---|---|---|")
    for case, hc in H.items():
        for wk, ent in hc.items():
            for nm in ("box_muller_current_law", "icdf_A02", "best_loader", "free_loader_F05",
                       "box_muller+free_exp_A13", "best_loader+free_exp_A13",
                       "box_muller+narrow_A07", "all_free_and_narrow"):
                e = ent.get(nm, {})
                if "call_reaction_layers" not in e:
                    w("| %s | %s | %s | | infeasible | | | | | | |" % (case, wk, nm))
                    continue
                c = e["call_reaction_layers"]["value"]
                sa = e["supply_aware_design"]["value"]
                w("| %s | %s | %s | %s | %s | %s/%s/%s | %.0f%% | %s | %s | %s | %s |" % (
                    case, wk, nm, e["loader"], f(c), f(c), f(2 * c), f(4 * c),
                    100 * e["loader_share"]["value"], f(e["call_T_count"]["value"]),
                    f(e["width_qubits"]["value"]), f(e["required_T_per_s"]["value"]["100ns"]),
                    f(sa["eff_depth_1e12_100ns"])))
    cur = d["a01_run014_current"]
    w("\nFor reference, the current accepted source (A01_run014, measured):")
    for c, v in cur.items():
        w("- %s: capped call T-depth %s, forward dependency T-depth %s, T-count %s, %s logical qubits." % (
            c, f(v["capped_call_t_depth"]), f(v["forward_dependency_t_depth"]), f(v["t_count"]),
            f(v["logical_qubits"])))
    w("")

    w("## 2. Tenfold reach: k_10x = D_max(k=1) / floor (largest estimator constant that still reaches 10x)\n")
    w("W = 1e7, t_layer = 100 ns, e = 0.45 eps. `unl` means unlimited magic-state supply. "
      "`1e12` means the supply-limited depth at 1e12 T/s. F20 applies the zero-depth sigma credit (x4.5).\n")
    w("| case | eps | T_C (s) | T_C convention | D_max(k=1) | BM unl | BM 1e12 | best unl | best 1e12 | "
      "BM 1e12 +F20 | best 1e12 +F20 |")
    w("|---|---|---|---|---|---|---|---|---|---|---|")
    for case, hc in H.items():
        bm = hc["W1e7"]["box_muller_current_law"]["comparison"]
        be = hc["W1e7"]["best_loader"]["comparison"]
        for rb, rr in zip(bm, be):
            b, r = rb["by_t_layer"]["100ns"], rr["by_t_layer"]["100ns"]
            w("| %s | %s | %s | %s | %s | %.2f | %.2f | %.2f | %.2f | %.2f | %.2f |" % (
                case, rb["eps"], f(rb["T_C"], 3), rb["T_C_conv"]
                + ("" if rb["source_bias_fits"] else " (bias bound ineligible; W0: eligible at zero bias)"),
                f(b["base"]["Dmax_k1"]), b["base"]["k_10x_unlimited_supply"],
                b["base"]["k_10x_supply_1e12"], r["base"]["k_10x_unlimited_supply"],
                r["base"]["k_10x_supply_1e12"], b["f20_sigma_credit"]["k_10x_supply_1e12"],
                r["f20_sigma_credit"]["k_10x_supply_1e12"]))
    w("")

    w("## 3. Loader share and alternative loaders (CRITIQUE F7)\n")
    w("Coarse model, base precision (72-bit word, 40-bit function precision). The table gives the forward loader depth and call floor for each loader. "
      "Loaders on a grid (alias, GR, A03, A04) change the law to a q-bit grid, so a new G2 is needed (assumed acceptable at q=10 per the A05 records).\n")
    w("| case | W | loader | forward loader depth | call floor | loader share | T per call |")
    w("|---|---|---|---|---|---|---|")
    for key, r in sorted(d["coarse_all"].items()):
        case, wk, vk, lk = key.split("|")
        if vk != "base" or wk != "W1e7" or r is None:
            continue
        w("| %s | %s | %s | %s | %s | %.0f%% | %s |" % (case, wk, lk, f(r["loader_depth"]),
                                                     f(r["call"]), 100 * r["loader_share_float"],
                                                     f(r["call_t"])))
    w("")

    w("## 4. Refinement: A01_run014 DAG reweight\n")
    t = d["refinement_trigger"]
    w("Trigger rule: coarse call floor x k=3 <= 10 x D_max(k=1) at 100 ns in some cell. "
      "Result: %s, so the refinement ran.\n" % "; ".join(
          "%s floor x 3 / D_max(k=1) = %.2f" % (c, v["floor_times_k3_over_Dmax_k1"]) for c, v in t.items()))
    w("Self-check (measured): reweighting the DAG with the archived leaf T-depths reproduces the A01_run014 "
      "forward dependency T-depth: %s.\n" % "; ".join(
          "%s %s vs %s (%s)" % (c, f(v["reproduced_forward_dependency_t_depth"]), f(v["a01_run014"]),
                               "match" if v["match"] else "MISMATCH") for c, v in d["dag_selfcheck"].items()))
    w("| case | variant | forward (unlimited) | call (unlimited) | call W=1e7 | call W=1e6 | loader share (critical path / marginal) | "
      "free loader | free exp | both free | best substituted loader (forward) | T per call | required T/s (unlimited width) |")
    w("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for c, vv in d["dag_reweight"].items():
        for vk, r in vv.items():
            bw = r["by_width"]
            sub = r["best_loader_substitution"]
            bl = min((s["forward"], k) for k, s in sub.items() if k != "free")
            w("| %s | %s | %s | %s | %s | %s | %.0f%% / %.0f%% | %s | %s | %s | %s (%s) | %s | %s |" % (
                c, vk, f(r["forward_unlimited"]), f(r["call_unlimited"]),
                f(bw["W1e7"].get("call")) if bw["W1e7"].get("feasible") else "infeasible",
                f(bw["W1e6"].get("call")) if bw["W1e6"].get("feasible") else "infeasible (retention > W)",
                100 * r["loader_share_critical_path"], 100 * r["loader_share_marginal"],
                f(r["forward_free_loader"]), f(r["forward_free_exp"]),
                f(r["forward_free_loader_and_exp"]), f(bl[0]), bl[1], f(r["call_t"]),
                f(r["required_T_per_s_100ns"].get("unlimited"))))
    w("\nThe DAG keeps the current algorithm. That means Horner log and cos, binary adders between every step, a max tree over dates, and a degree-12 exp with ln2 range reduction. "
      "So it gives the construction-anchored idealized floor. The coarse model restructures the algorithm: carry-save chains, Estrin with larger tables, an AND of comparisons, and a direct exp table. That is standard and quantum-favourable, so the coarse value is the floor of record.\n")

    w("## 5. Early-stop signal (W0 card; W = 1e7 rows; every width is in floor.json)\n")
    w("The early stop fires iff k_lat > max k_es, where k_es = 30 x D_max(k=1) / floor and the maximum is over cells, and over conventions in scope.\n")
    w("| W | floor | supply | scope | max k_es | max k_10x | at cell | t_layer | convention |")
    w("|---|---|---|---|---|---|---|---|---|")
    for e in d["early_stop"]:
        if e["floor"] not in ("box_muller_current_law", "best_loader", "all_free_and_narrow"):
            continue
        if e["width"] != "W1e7":
            continue
        w("| %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            e["width"], e["floor"], e["supply"], e["scope"], f(e["max_k_early_stop"], 1),
            f(e["max_k_10x"], 2), e["cell"], e["t_layer"], e["convention"]))
    w("")

    w("## 6. Caveats\n")
    for s in (
        "These are idealized literature constructions, **not lower bounds**. The multiplier's AND-degree bound "
        "(ceil(log2 2n) ~ 8 layers vs ~20 used) shows that the arithmetic could still shrink by up to ~2.5x. With truly unlimited "
        "width, any function of N input bits has AND-depth ceil(log2 N)+1 (~12-15 here) via an exponential-width lookup. "
        "Table address bits are therefore capped at 20.",
        "The ways the model favours quantum: Cliffords, fan-out, routing and the amplitude-encoding envelope cost zero; the discount "
        "and 1/(assets x dates) scaling are folded into the envelope; garbage cleanup overlaps downstream compute; 100 ns per reaction layer; "
        "and T-depth-1 ANDs.",
        "The ways the model works against quantum, or is simply crude: width is handled by uniform per-stage rounds or stage-local recomputation, "
        "and garbage is double-counted while cleanup overlaps. The W = 1e6 B8x52 numbers are dominated by this crude width model.",
        "Grid loaders (alias, GR, A03, A04) change the sampling law. Box-Muller and ICDF keep the 32-bit-uniform continuous law at the "
        "base precision. The A07 narrow widths (40-bit word, 24-bit precision) are unproved.",
        "T-count uses full (not truncated) multiplier partial products. Truncated fixed-point multipliers could cut the "
        "multiplier T by up to ~2x, which would lower the supply-limited depth by up to ~2x (quantum-favourable; not applied).",
        "The supply-limited depth is min over the depth-optimal and supply-aware designs of max(call, T_call/(R x t_layer)).",
        "The eps = 0.10 and 0.03 cells use overhead-dominated classical small-n marks (gap_ledger caveat). The most favourable "
        "k_10x values sit in those cells.",
    ):
        w("- " + s)
    w("")
    with open(os.path.join(a.dir, "floor.md"), "x", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L))


if __name__ == "__main__":
    main()
