"""N1-headline steps 2b, 3 and the W0 comparison.

Inputs (read only): this workstream's keff.json and floor_sheet.json; C2/C5 classical timings; the measured
H16 worker grid rows; WS-k k_bracket.json part3 (explicit / no-explicit estimator constants); W0 floor.json and
decision run002 (comparison only). W0 scripts are not run or imported.

Definitions: k_10x = T_C / (10 (sigma/e) D_eff t_layer); M = k / k_10x; M <= 1 means 10x reached.
D_eff = Grover-iterate effective depth = max(reaction depth, T_iterate / (supply * t_layer)).
Run: .context/frontier_t0_env/Scripts/python.exe -I -S -B research/plan110_n1/headline/headline_m.py

FRONTIER PROBE COPY (21 Oct 2026). Copied from research/plan110_n1/headline/headline_m.py (sha256 98e2259a...dd1f),
which is not edited. Changes, and only these:
  1. ROOT is this checkout and OUT is results/frontier_probe_20261021/headline/run001/ (the N1 inputs keff.json and
     floor_sheet.json are still read from results/plan110_n1/headline/).
  2. Two estimator classes from P2 (results/frontier_probe_20261021/p2/run001/p2_window.json): the certified Kaiser
     window constant with the U1/U2 credits and the part-4 budget reserved, at estimator failure 0.003
     ("window_certified_fail0003") and 0.01 ("window_certified_fail001"), plus the same at 0.003 without the U1/U2
     credits ("window_certified_noU1U2_fail0003") and without direction-select ("window_certified_noDS_fail0003").
  3. One sensitivity column "distfree_stageC": T_C times the per-cell Stage-C distribution-free factor of
     results/plan110_n1/hwclassical/hw_classical_card_v2.json (classical rows, factor_df_over_practice).
P1 (control-variate residual span) closed with no route reaching a net factor of 4, so it changes no input here.
Run: .context/frontier_t0_env/Scripts/python.exe -I -S -B research/frontier_probe_20261021/headline_m_probe.py [run001|run002]
"""
import glob
import hashlib
import itertools
import json
import sys
from fractions import Fraction
from math import comb
from pathlib import Path

ROOT = str(Path(__file__).resolve().parents[2]).replace("\\", "/") + "/"
N1H = ROOT + "results/plan110_n1/headline/"
RUN = sys.argv[1] if len(sys.argv) > 1 else "run001"  # run002+ read P2 run002 (parts 3-4 explicit)
# run003+: optional argv[2] = C10 paired-timing JSON; measured-cell T_C is divided by the paired speedup of
# preint_fast over Stage C preint (same points, same machine state); see research/c10_challengers_20261022/.
C10 = sys.argv[2] if len(sys.argv) > 2 else None
OUT = ROOT + f"results/frontier_probe_20261021/headline/{RUN}/"
IN = dict(
    keff=N1H + "keff.json",
    floor_n1=N1H + "floor_sheet.json",
    p2=ROOT + f"results/frontier_probe_20261021/p2/{'run001' if RUN == 'run001' else 'run002'}/p2_window.json",
    hw=ROOT + "results/plan110_n1/hwclassical/hw_classical_card_v2.json",
    c2=ROOT + "results/frontier_classical_20261001/c2/c2_timing.json",
    c5=ROOT + "results/frontier_classical_20261001/c5/timing/c5_timing.json",
    sigma=ROOT + "results/frontier_classical_20261001/sigma_dev/sigma_dev.json",
    kb=ROOT + "results/plan110_w0/ws_k/k_bracket.json",
    w0_floor=ROOT + "results/plan110_w0/ws_floor/floor.json",
    w0_dec=ROOT + "results/plan110_w0/decision/run002/decision_summary.json",
)
H16 = ROOT + "results/plan110_w0/ws_small/h16_grid/run001/rows/"
CASES = ("B4x12", "B8x52")
EPS = (0.1, 0.03, 0.01, 0.001)
TL = {"10ns": 1e-8, "100ns": 1e-7, "1us": 1e-6, "10us": 1e-5}


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def row(d):
    with open(OUT + "rows.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(d, sort_keys=True) + "\n")


def median(xs):
    xs = sorted(xs)
    n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


# ---------------- classical T_C ----------------
def t_c_table():
    c2, c5 = load(IN["c2"]), load(IN["c5"])
    raw = {}
    for src, d in (("C2", c2), ("C5", c5)):
        for blk, v in d["blocks"].items():
            case, meth = blk.split("/")
            for e, t in v["t_c"].items():
                tt = t["primary"]
                if C10_BEFORE_ENV and meth == "preint" and f"{case}_H140|{float(e)}" in C10_SPEED:
                    tt = tt / C10_SPEED[f"{case}_H140|{float(e)}"]  # run005+: speedup before the envelope
                raw.setdefault((case, float(e)), []).append(
                    dict(source=src, method=meth, t=tt, convention=t["convention"]))
    out = {}
    for case in CASES:
        for e in EPS:
            best = min(raw[(case, e)], key=lambda r: r["t"])
            # monotone envelope: a run meeting a tighter tolerance also meets this one
            tighter = [min(raw[(case, e2)], key=lambda r: r["t"]) for e2 in EPS if e2 <= e]
            env = min(tighter, key=lambda r: r["t"])
            tcv = env["t"]
            if C10 and not C10_BEFORE_ENV and best["method"] == "preint" and f"{case}_H140|{e}" in C10_SPEED:
                tcv = env["t"] / C10_SPEED[f"{case}_H140|{e}"]
            out[(case, e)] = dict(raw_best=best, T_C=tcv, T_C_stageC=env["t"], envelope_from=env,
                                  envelope_applied=env is not best and env["t"] < best["t"],
                                  overhead=best["convention"] != "measured confirmation",
                                  label="measured (C2/C5 'primary' wall at 16 workers) + envelope",
                                  direction="neutral (envelope is quantum-unfavourable)")
    return out


C10_SPEED, OV_H16, OV_DF, C10_BEFORE_ENV = {}, {}, {}, False
if C10:
    _j = json.load(open(C10, encoding="utf-8"))
    if "overrides" in _j:  # run004+: {"overrides": {"tc_speedup": {}, "h16_ratio": {}, "distfree_factor": {}}}
        C10_SPEED = _j["overrides"]["tc_speedup"]
        OV_H16 = _j["overrides"].get("h16_ratio", {})
        OV_DF = _j["overrides"].get("distfree_factor", {})
        C10_BEFORE_ENV = bool(_j["overrides"].get("apply_before_envelope", False))
    else:  # run003: the C10 paired-timing JSON itself
        for _k, _v in _j["cells"].items():
            C10_SPEED[_k] = _v["speedup_median"]["preint_fast"]


def h16_ratio():
    walls = {}
    for p in glob.glob(H16 + "*.json"):
        r = load(p)
        walls[(r["case"], float(r["eps"]), int(r["workers"]))] = median([x["wall"] for x in r["runs"]])
    out = {(c, e): walls[(c, e, 1)] / walls[(c, e, 16)] for (c, e, w) in walls if w == 1}
    for k, v in OV_H16.items():  # run004+: measured 1/16-worker ratio of the C10 fast method
        c, e = k.split("|")
        out[(c.replace("_H140", ""), float(e))] = v
    return out


# ---------------- estimator k classes ----------------
def pi_bbp(terms=30):
    s = Fraction(0)
    for k in range(terms):
        s += Fraction(1, 16 ** k) * (Fraction(4, 8 * k + 1) - Fraction(2, 8 * k + 4)
                                     - Fraction(1, 8 * k + 5) - Fraction(1, 8 * k + 6))
    return s, s + Fraction(1, 16 ** terms) * Fraction(4, 8 * terms + 1) * Fraction(16, 15)


def min_int_M(span, err, pi):
    """Smallest integer M with span*(pi/M + pi^2/M^2) <= err (worst case over a)."""
    M = int(span * pi / err)
    while span * (pi / M + pi * pi / (M * M)) > err:
        M += 1
    while M > 1 and span * (pi / (M - 1) + pi * pi / ((M - 1) ** 2)) <= err:
        M -= 1
    return M


def reps_for(fail, pi_hi):
    q = 1 - Fraction(8) / (pi_hi * pi_hi)
    r = 1
    while sum(comb(r, j) * q ** j * (1 - q) ** (r - j) for j in range(r // 2 + 1, r + 1)) > fail:
        r += 2
    return r


def k_classes(keff, sigma):
    kb = load(IN["kb"])
    cert = {(c["case"], c["eps"], c["split"]): c for c in keff["cells"] if c["M_rule"].startswith("dyadic")}
    pi_lo, pi_hi = pi_bbp()
    r003, r01 = reps_for(Fraction(3, 1000), pi_hi), reps_for(Fraction(1, 100), pi_hi)
    # independent spot check of WS-k non-dyadic, no-mean entries (part4 rows) with this script's arithmetic
    checks = []
    for r in kb["part4_joint_credit"]:
        if r["mean_bound"].startswith("none") and r["M_rule"].startswith("non-dyadic"):
            sp = r["span"].split(" ")[0]
            span = Fraction(sp)
            e = Fraction(9, 20) * Fraction(str(r["eps"])) if r["split"] == "0.45eps" else Fraction(str(r["eps"]))
            M = min_int_M(span, e, pi_hi)
            checks.append(dict(case=r["case"], eps=r["eps"], split=r["split"], span=sp, M_w0=r["M"], M_n1=M,
                               calls_w0=r["calls"], calls_n1=r003 * (M - 1), match=(M == r["M"] and r003 * (M - 1) == r["calls"])))
    out = {}
    for case in CASES:
        for e in EPS:
            for split in ("0.45eps", "eps"):
                rs = [r for r in kb["part3_k_lo_methods"]
                      if r["case"] == case and r["eps"] == e and r["split"] == split]
                expl = [r for r in rs if r["constant_status"].startswith("explicit")
                        and "average-case" not in r["constant_status"]]
                noex = [r for r in rs if r["constant_status"].startswith("no explicit")]
                be = min(expl, key=lambda r: r["k_total"])
                nx3 = min([r for r in noex if "fail 0.003" in r["method"]], key=lambda r: r["k_total"])
                nx1 = min([r for r in noex if "fail 0.01" in r["method"]], key=lambda r: r["k_total"])
                med = "medians" in be["method"]
                p2k = load(IN["p2"])["k"]
                pk = lambda spl, ml, fail, field="k_direction_select": p2k[
                    f"{case}|{e}|{split}|{spl}|{ml}|with_impl_budget|fail {fail}"][field]
                out[(case, e, split)] = dict(
                    window_certified_fail0003=dict(k=pk("8192/211", "price+L1", "3/1000"),
                                                   source=f"P2 certified Kaiser window (probe {RUN})",
                                                   label="modelled; U1/U2 + direction-select conditional, part-4 budget assm"),
                    window_certified_fail001=dict(k=pk("8192/211", "price+L1", "1/100"), source="P2"),
                    window_certified_noU1U2_fail0003=dict(k=pk("64", "no mean", "3/1000"), source="P2"),
                    window_certified_noDS_fail0003=dict(k=pk("8192/211", "price+L1", "3/1000",
                                                             "k_without_direction_select"), source="P2"),
                    certified=dict(k=cert[(case, e, split)]["k_eff"], source="N1 exact rational (keff.json)",
                                   label="modelled-exact x measured sigma"),
                    explicit_best=dict(k=be["k_total"], method=be["method"], status=be["constant_status"],
                                       source="WS-k part3 (input)", label="modelled (WS-k)"),
                    explicit_best_fail001=dict(k=be["k_total"] * (r01 / r003 if med else 1),
                                               note=f"median reps {r003}->{r01} at estimator failure 0.01 (N1)",
                                               label="modelled; quantum-favourable allocation"),
                    no_explicit_fail0003=dict(k=nx3["k_total"], method=nx3["method"]),
                    no_explicit_fail001=dict(k=nx1["k_total"], method=nx1["method"]),
                    sigma_over_e=sigma[case]["sigma_q"] / ((0.45 if split == "0.45eps" else 1.0) * e))
    return out, checks, (r003, r01)


# ---------------- D_eff (N1 sheet vs W0 floor) ----------------
def deff_tables():
    n1, w0 = load(IN["floor_n1"]), load(IN["w0_floor"])
    dmap = {"primary": ("primary_n72", "box_muller_current_law"),
            "all_free": ("all_free_n48_f32", "all_free_and_narrow")}
    wmap = {"W1e6": ("W1e6", "W1e6"), "W1e7": ("W1e7", "W1e7"), "W1e8": ("W1e8", "unlimited"),
            "unlimited": ("unlimited", "unlimited")}
    tab = {}
    for case in CASES:
        for dn, (d1, d0) in dmap.items():
            for wn, (w1, w0n) in wmap.items():
                for sup in ("1e11", "1e12", "1e13"):
                    for tl in TL:
                        a = n1["cases"][case][d1]["by_width"][w1][f"{sup}|{tl}"]["D_eff"]
                        h = w0["headline"][case][w0n][d0]
                        b = h["comparison"][0]["by_t_layer"][tl]["base"][f"eff_depth_supply_{sup}"] if h else None
                        cand = [x for x in (a, b) if x is not None]
                        use = min(cand) if cand else None
                        agree = None if (a is None or b is None) else abs(a - b) / min(a, b) <= 0.10
                        tab[(case, dn, wn, sup, tl)] = dict(
                            N1=a, W0=b, used=use, agree_10pct=agree,
                            used_from="N1" if use == a and a is not None and (b is None or a < b) else "W0",
                            note=("W0 value at W1e8 is its unlimited-width floor (lower bound)" if wn == "W1e8" else ""))
    return tab


def main():
    Path(OUT).mkdir(parents=True, exist_ok=False)
    keff, sig = load(IN["keff"]), load(IN["sigma"])["cases"]
    tc, r1 = t_c_table(), h16_ratio()
    kc, checks, (r003, r01) = k_classes(keff, sig)
    dt = deff_tables()
    w0dec = load(IN["w0_dec"])
    meta = dict(script="research/plan110_n1/headline/headline_m.py", python=sys.version,
                inputs_sha256={k: sha(v) for k, v in IN.items()},
                definitions="k_10x = T_C/(10 (sigma/e) D_eff t_layer); M = k/k_10x; M<=1 reaches 10x",
                median_reps=dict(fail_0003=r003, fail_001=r01))
    for k, v in tc.items():
        row(dict(ws="headline", step="2b_T_C", case=k[0], eps=k[1], T_C=v["T_C"], raw_best=v["raw_best"],
                 envelope_applied=v["envelope_applied"], overhead=v["overhead"], label=v["label"],
                 direction=v["direction"]))
    for k, v in r1.items():
        row(dict(ws="headline", step="2b_h16_ratio", case=k[0], eps=k[1], one_core_over_16=v,
                 label="measured (median wall w1 / median wall w16, H16 grid run001)", direction="neutral"))
    row(dict(ws="headline", step="3_ws_k_spotcheck", n=len(checks), all_match=all(c["match"] for c in checks),
             label="modelled (N1 exact-rational recompute of WS-k non-dyadic worst-case rows)"))

    dfc = {(r["case"], float(r["eps"])): r["factor_df_over_practice"]
           for r in load(IN["hw"])["classical"]["rows"]}
    for k, v in OV_DF.items():  # run004+: measured C09 distribution-free factor (same-state ratio)
        c, e = k.split("|")
        dfc[(c.replace("_H140", ""), float(e))] = v

    def M_of(case, e, split, kname, design="primary", W="W1e7", sup="1e12", tl="100ns",
             one_core=False, distfree=1.0, distfree_cell=False):
        kk = kc[(case, e, split)]
        k = kk[kname]["k"]
        D = dt[(case, design, W, sup, tl)]["used"]
        if D is None:
            return None
        T = tc[(case, e)]["T_C"] * distfree * (dfc[(case, e)] if distfree_cell else 1.0)
        if one_core:
            if (case, e) not in r1:
                return None
            T *= r1[(case, e)]
        k10 = T / (10 * kk["sigma_over_e"] * D * TL[tl])
        return k / k10

    classes = ("certified", "explicit_best", "explicit_best_fail001", "no_explicit_fail0003", "no_explicit_fail001",
               "window_certified_fail0003", "window_certified_fail001", "window_certified_noU1U2_fail0003",
               "window_certified_noDS_fail0003")
    cells = []
    for case in CASES:
        for e in EPS:
            c = dict(case=case, eps=e, T_C=tc[(case, e)]["T_C"], overhead_T_C=tc[(case, e)]["overhead"],
                     h16_ratio=r1.get((case, e)),
                     D_eff_primary=dt[(case, "primary", "W1e7", "1e12", "100ns")],
                     sigma_over_e=kc[(case, e, "0.45eps")]["sigma_over_e"], k={}, M={})
            for cl in classes:
                c["k"][cl] = kc[(case, e, "0.45eps")][cl]["k"]
                M = dict(primary=M_of(case, e, "0.45eps", cl),
                         one_lane_one_core=M_of(case, e, "0.45eps", cl, one_core=True),
                         distfree_x2=M_of(case, e, "0.45eps", cl, distfree=2.0),
                         distfree_x5=M_of(case, e, "0.45eps", cl, distfree=5.0),
                         e_eq_eps=M_of(case, e, "eps", cl),
                         all_free_oracle=M_of(case, e, "0.45eps", cl, design="all_free"),
                         distfree_stageC=M_of(case, e, "0.45eps", cl, distfree_cell=True),
                         all_free_distfree_stageC=M_of(case, e, "0.45eps", cl, design="all_free", distfree_cell=True))
                for W in ("W1e6", "W1e8", "unlimited"):
                    M[f"width_{W}"] = M_of(case, e, "0.45eps", cl, W=W)
                for sup in ("1e11", "1e13"):
                    M[f"supply_{sup}"] = M_of(case, e, "0.45eps", cl, sup=sup)
                for tl in ("10ns", "1us", "10us"):
                    M[f"t_layer_{tl}"] = M_of(case, e, "0.45eps", cl, tl=tl)
                c["M"][cl] = M
                # same cell, N1-only floor (own path), for the receipt
            c["M_N1_floor_only_primary"] = {
                cl: c["k"][cl] / (c["T_C"] / (10 * c["sigma_over_e"] * c["D_eff_primary"]["N1"] * 1e-7))
                for cl in classes}
            cells.append(c)
            row(dict(ws="headline", step="3_M_cell", case=case, eps=e, overhead=c["overhead_T_C"],
                     M_primary={cl: c["M"][cl]["primary"] for cl in classes},
                     M_N1_floor_only=c["M_N1_floor_only_primary"], D_eff=c["D_eff_primary"],
                     label="modelled (k modelled, T_C measured, D_eff modelled)", direction="see receipt"))

    def eligible(c, b8_ineligible=False):
        if c["overhead_T_C"]:
            return False
        return not (b8_ineligible and c["case"] == "B8x52" and c["eps"] == 0.001)

    def minM(cl, col="primary", b8_inel=False):
        vals = [(c["M"][cl][col], c["case"], c["eps"]) for c in cells
                if eligible(c, b8_inel) and c["M"][cl][col] is not None]
        return min(vals) if vals else None

    summary = {}
    for cl in classes:
        summary[cl] = {col: minM(cl, col) for col in cells[0]["M"][cl]}
        summary[cl]["primary_B8_0.001_ineligible"] = minM(cl, "primary", True)

    # ---- minimal stacked departures to M <= 1 (explicit-constant classes) ----
    deps = dict(all_free="design", zero_bias_e_eq_eps="split", one_lane_one_core="one_core",
                distfree_x5="distfree", t_layer_10ns="tl", supply_1e13="sup", width_unlimited="W",
                estimator_fail_001="fail", distfree_stageC="distfree_cell")
    stack = {}
    for base in ("explicit_best", "certified", "no_explicit_fail0003", "window_certified_fail0003"):
        found = []
        for size in range(0, len(deps) + 1):
            for combo in itertools.combinations(deps, size):
                kw = dict(design="primary", W="W1e7", sup="1e12", tl="100ns", one_core=False, distfree=1.0,
                          distfree_cell=False)
                split, cl = "0.45eps", base
                for dname in combo:
                    if dname == "all_free":
                        kw["design"] = "all_free"
                    elif dname == "zero_bias_e_eq_eps":
                        split = "eps"
                    elif dname == "one_lane_one_core":
                        kw["one_core"] = True
                    elif dname == "distfree_x5":
                        kw["distfree"] = 5.0
                    elif dname == "distfree_stageC":
                        kw["distfree_cell"] = True
                    elif dname == "t_layer_10ns":
                        kw["tl"] = "10ns"
                    elif dname == "supply_1e13":
                        kw["sup"] = "1e13"
                    elif dname == "width_unlimited":
                        kw["W"] = "unlimited"
                    elif dname == "estimator_fail_001":
                        cl = {"explicit_best": "explicit_best_fail001", "certified": "certified",
                              "no_explicit_fail0003": "no_explicit_fail001",
                              "window_certified_fail0003": "window_certified_fail001"}[base]
                        if base == "certified":
                            cl = None
                if cl is None:
                    continue
                vals = []
                for c in cells:
                    if not eligible(c):
                        continue
                    m = M_of(c["case"], c["eps"], split, cl, **kw)
                    if m is not None:
                        vals.append((m, c["case"], c["eps"]))
                if not vals:
                    continue
                best = min(vals)
                found.append(dict(departures=list(combo), size=size, min_M=best[0], cell=f"{best[1]} {best[2]}"))
        reach = [f for f in found if f["min_M"] <= 1]
        smin = min(f["size"] for f in reach) if reach else None
        stack[base] = dict(min_departures_to_M_le_1=smin,
                           minimal_sets=sorted([f for f in reach if f["size"] == smin], key=lambda f: f["min_M"]),
                           best_single=sorted([f for f in found if f["size"] == 1], key=lambda f: f["min_M"])[:3],
                           best_pairs=sorted([f for f in found if f["size"] == 2], key=lambda f: f["min_M"])[:3])
        row(dict(ws="headline", step="3_stacked_departures", k_class=base, min_departures=smin,
                 minimal_sets=stack[base]["minimal_sets"][:6], best_single=stack[base]["best_single"],
                 label="modelled", direction="quantum-favourable departures"))

    # ---- comparison with W0 decision run002 ----
    w0rows = {(r["case"], r["eps"], r["k_class"]): r for r in w0dec["primary_rows"]}
    cmp_rows = []
    for c in cells:
        for cl_n1, cl_w0 in (("certified", "certified_today"), ("explicit_best", "explicit_best"),
                             ("no_explicit_fail001", "no_explicit_constant")):
            w = w0rows.get((c["case"], c["eps"], cl_w0))
            if not w:
                continue
            mine = c["M"][cl_n1]["primary"]
            cmp_rows.append(dict(case=c["case"], eps=c["eps"], k_class=cl_w0,
                                 k_N1=c["k"][cl_n1], k_W0=w["k"], T_C_N1=c["T_C"], T_C_W0=w["T_C"],
                                 M_N1_headline=mine, M_W0=w["M_practice_16core"],
                                 M_N1_own_floor=c["M_N1_floor_only_primary"][cl_n1],
                                 rel_diff=abs(mine - w["M_practice_16core"]) / min(mine, w["M_practice_16core"]),
                                 M_1lane_N1=c["M"][cl_n1]["one_lane_one_core"], M_1lane_W0=w["M_1lane_1core"]))
    for r in cmp_rows:
        row(dict(ws="headline", step="4_compare_W0", **r, label="modelled vs modelled", direction="neutral"))

    out = dict(meta=meta, cells=cells, summary_min_M_eligible_non_overhead=summary, stacked_departures=stack,
               ws_k_spotcheck=checks, T_C={f"{k[0]}|{k[1]}": v for k, v in tc.items()},
               h16_one_core_ratio={f"{k[0]}|{k[1]}": v for k, v in r1.items()},
               D_eff_table={"|".join(k): v for k, v in dt.items()}, compare_W0=cmp_rows,
               w0_dp1=dict(certified=801.4765075667697, explicit_best=231.9631113906583,
                           no_explicit=8.619120442999092))
    with open(OUT + "headline_table.json", "x", encoding="utf-8") as f:
        json.dump(out, f, indent=1, default=str)
    for cl in classes:
        print(cl, "primary min M:", summary[cl]["primary"], "| all_free:", summary[cl]["all_free_oracle"],
              "| 1lane:", summary[cl]["one_lane_one_core"], "| B8 inel:", summary[cl]["primary_B8_0.001_ineligible"])
    for b, s in stack.items():
        print(b, "min departures:", s["min_departures_to_M_le_1"], [ (f["departures"], round(f["min_M"], 3)) for f in s["minimal_sets"][:5]])
        print("   best single:", [(f["departures"], round(f["min_M"], 3)) for f in s["best_single"]])
        print("   best pairs:", [(f["departures"], round(f["min_M"], 3)) for f in s["best_pairs"]])
    for r in cmp_rows:
        print(r["case"], r["eps"], r["k_class"], "N1 %.3f W0 %.3f own-floor %.3f diff %.3f" % (
            r["M_N1_headline"], r["M_W0"], r["M_N1_own_floor"], r["rel_diff"]))
    print("WS-k spot checks:", len(checks), all(c["match"] for c in checks))


if __name__ == "__main__":
    main()
