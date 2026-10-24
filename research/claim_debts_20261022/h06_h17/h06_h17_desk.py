"""H17 + H06 R1 desk record at the binding cell (B8x52, eps = $0.001, window estimator).

H17: the two necessary-condition columns of PLAN_110 (required magic-state rate and reaction time per layer; width
is checked against the budget). H06: AND/CCZ vs T composition and a CCZ-native supply sensitivity column.
Model (same as headline_m / the N1 hardware card): N = k (sigma/e) calls, each costing
max(L t_layer, T_call / R); M = N max(L t_layer, T_call / R) / (T_C / 10). Each necessary condition holds the
other resource unlimited, so it is necessary for M <= m; together they are also sufficient within this model.

Run (worktree root): <frontier_t0_env python> -I -S -B research/claim_debts_20261022/h06_h17/h06_h17_desk.py run001
"""
import hashlib
import json
import os
import sys
from fractions import Fraction as F

RUN = sys.argv[1]
OUT = os.path.join("results", "claim_debts_20261022", "h06_h17", RUN)
PROG = os.path.join("results", "claim_debts_20261022", "h06_h17", "progress.jsonl")
IN = {
    "floor": "results/plan110_w0/ws_floor/floor.json",
    "bias_desk": "results/plan110_w0/ws_small/bias_desk_run001/bias_desk.json",
    "headline": "results/frontier_probe_20261021/headline/run006/headline_table.json",
    "p2_self_mean": "results/frontier_probe_20261021/p2/run003_self_mean/p2c_self_mean.json",
}
C11 = "results/claim_debts_20261022/c11/run001/summary.json"  # hook: read only if it exists at run time
if os.path.exists(C11):
    IN["c11"] = C11


def load(k):
    with open(IN[k], encoding="utf-8") as fh:
        return json.load(fh)


def sha(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def progress(**row):
    with open(PROG, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, sort_keys=True) + "\n")


fl = load("floor")
ca = fl["coarse_all"]
base = ca["B8x52|W1e7|base|box_muller"]          # primary floor design family (W0 'box_muller_current_law')
allf = ca["B8x52|W1e7|a07_narrow+a13_free_exp|free"]  # W0 'all_free_and_narrow'
hd_bm = fl["headline"]["B8x52"]["W1e7"]["box_muller_current_law"]
assert base["call"] == hd_bm["call_reaction_layers"]["value"] and base["call_t"] == hd_bm["call_T_count"]["value"]
src = fl["a01_run014_current"]["B8x52"]
dc = load("bias_desk")["depth_convention"]["B8x52"]

cell = [c for c in load("headline")["cells"] if c["case"] == "B8x52" and abs(c["eps"] - 0.001) < 1e-12][0]
T_C = F(cell["T_C"])
SIG_E = F(cell["sigma_over_e"])
K = {"window_certified": F(cell["k"]["window_certified_fail0003"]),
     "window_quantum_only_mean": F(load("p2_self_mean")["cells"]["B8x52|0.001"]["best"]["k"])}
M_ref = cell["M"]["window_certified_fail0003"]["primary"]
T_LAYER, SUPPLY, WIDTH = F(1, 10**7), F(10**12), 10**7

# Iterate descriptions: (reaction layers L per call, T per call, label)
ITER = {
    "floor_min_depth": dict(L=base["call"], T=base["call_t"], ands=2 * base["forward_ands"], rot_t=base["forward_rot_t"],
                            width=None, label="mod, q+ (W0 idealized floor; min-depth design)"),
    "floor_supply_aware": dict(L=base["supply_aware_design"]["call"], T=base["supply_aware_design"]["call_t"],
                               ands=None, rot_t=0, width=base["supply_aware_design"]["width"],
                               label="mod, q+ (W0 floor design used in the headline; D_eff 2,296)"),
    "saved_source": dict(L=dc["per_call_iterate_t_depth"], T=src["t_count"], ands=None, rot_t=None,
                         width=src["logical_qubits"],
                         label="meas (A10 min-depth source: F + F^-1 T-count; per-call iterate T-depth incl. selector "
                               "and reflection); T excludes selector/reflection T (q+ by that amount; C11 hook)"),
}
# supply-aware design is all-AND (rot 0 in the base family): ANDs = T / 4
ITER["floor_supply_aware"]["ands"] = ITER["floor_supply_aware"]["T"] // 4
assert ITER["floor_supply_aware"]["ands"] * 4 == ITER["floor_supply_aware"]["T"]
assert ITER["floor_min_depth"]["ands"] * 4 + ITER["floor_min_depth"]["rot_t"] == ITER["floor_min_depth"]["T"]


def deff(L, T, units_per_T=F(1)):
    return max(F(L), F(T) * units_per_T / (SUPPLY * T_LAYER))


def M_of(k, D):
    return k * 10 * SIG_E * D * T_LAYER / T_C


# Self-check: the headline M is reproduced from the supply-aware floor design.
D_floor = deff(ITER["floor_supply_aware"]["L"], ITER["floor_supply_aware"]["T"])
assert abs(float(M_of(K["window_certified"], D_floor)) - M_ref) <= 1e-9 * M_ref
progress(step="selfcheck", D_floor=float(D_floor), M=float(M_of(K["window_certified"], D_floor)), M_run006=M_ref)

# ---- H17 necessary-condition columns ---------------------------------------------------------
h17 = []
for kname, k in K.items():
    N = k * SIG_E
    for iname, it in ITER.items():
        D = deff(it["L"], it["T"])
        row = dict(k_class=kname, k=float(k), calls=float(N), iterate=iname, label=it["label"],
                   L_per_call=it["L"], T_per_call=it["T"], D_eff_primary=float(D), M_primary=float(M_of(k, D)),
                   bound_at_primary="reaction" if F(it["L"]) >= F(it["T"]) / (SUPPLY * T_LAYER) else "supply",
                   width_logical=it["width"], width_over_budget=(it["width"] / WIDTH if it["width"] else None))
        for m in (1, 10):
            budget = m * T_C / 10  # quantum wall-clock allowed for M <= m
            t_req = budget / (N * it["L"])
            r_req = N * it["T"] / budget
            row[f"M<={m}"] = dict(t_layer_required_s=float(t_req), t_layer_required_over_100ns=float(t_req / T_LAYER),
                                  T_per_s_required=float(r_req), T_per_s_required_over_1e12=float(r_req / SUPPLY),
                                  CCZ_per_s_required_if_all_AND=float(r_req / 4))
        h17.append(row)
progress(step="h17", rows=len(h17))

# ---- H06: AND/CCZ composition and CCZ-native supply sensitivity ------------------------------
# u = supply units consumed per AND (CCZ). Primary convention: an AND costs 4 T from a T supply of 1e12 T/s.
CONV = {"primary_4T_per_AND": F(4), "CCZ_2T_equiv": F(2), "CCZ_native_1_unit": F(1)}
# Primary-law recorded designs only: the Box-Muller loader with base arithmetic (the other base|* keys change the
# loader, i.e. are departures). run001 wrongly searched all base|* loaders; superseded by run002.
designs = {k: v for k, v in ca.items() if k == "B8x52|W1e7|base|box_muller"}
L_FAMILY_MIN = min(min(v["call"], v["supply_aware_design"]["call"]) for v in designs.values())
h06 = dict(composition={}, ccz_convention={})
for iname in ("floor_min_depth", "floor_supply_aware"):
    it = ITER[iname]
    h06["composition"][iname] = dict(AND_per_call=it["ands"], T_from_AND=4 * it["ands"], rotation_T=it["rot_t"],
                                     AND_share_of_T=float(F(4 * it["ands"], it["T"])),
                                     CCZ_per_layer_at_primary=float(F(it["ands"]) / deff(it["L"], it["T"])))
h06["composition"]["saved_source"] = dict(
    T_per_call=src["t_count"], AND_count="not recorded in the saved summaries",
    CCZ_upper_if_every_T_is_in_a_4T_AND=src["t_count"] // 4,
    label="assm (composition unknown; the CCZ column below treats every T as part of a 4-T AND, q+)")
for cname, u in CONV.items():
    per = {}
    for kname, k in K.items():
        # best recorded primary-law design under this convention: min over designs of max(L, AND*u/1e5)
        best = None
        for dk, dv in designs.items():
            for L, T in ((dv["call"], dv["call_t"]), (dv["supply_aware_design"]["call"], dv["supply_aware_design"]["call_t"])):
                if dv["forward_rot_t"]:
                    continue  # rotation-bearing loaders are not CCZ-convertible
                D = deff(L, T, u / 4)
                if best is None or D < best[0]:
                    best = (D, dk, L, T)
        Dsrc = deff(ITER["saved_source"]["L"], ITER["saved_source"]["T"], u / 4)
        Dall = deff(allf["supply_aware_design"]["call"], allf["supply_aware_design"]["call_t"], u / 4)
        per[kname] = dict(floor_best_design=best[1], floor_best_point=[best[2], best[3]], floor_D_eff=float(best[0]),
                          floor_M=float(M_of(k, best[0])),
                          floor_M_lower_bound_reaction=float(M_of(k, F(L_FAMILY_MIN))),
                          all_free_D_eff=float(Dall), all_free_M=float(M_of(k, Dall)),
                          saved_source_D_eff=float(Dsrc), saved_source_M=float(M_of(k, Dsrc)))
    if u == 4:
        assert per["window_certified"]["floor_D_eff"] == float(D_floor)  # primary convention reproduces 2,296
    h06["ccz_convention"][cname] = dict(supply_units_per_AND=float(u), rate_units_per_s=1e12, **per)
h06["label"] = ("mod; CCZ_2T_equiv uses the catalysed CCZ->2T relation (Gidney & Fowler, Quantum 3, 135 (2019); lit) "
                "as a supply-unit convention; CCZ_native_1_unit is an extreme q+ convention (one CCZ per supply slot)")
progress(step="h06", conventions=list(CONV))

c11_hook = None
if "c11" in IN:
    c = load("c11")
    tpi = c.get("iterate", {}).get("t_count_literal")  # C11 run001 schema: compiled iterate incl. U2 selector and reflection
    if tpi:
        c11_hook = {kname: dict(T_per_iterate=tpi, D_eff=float(deff(ITER["saved_source"]["L"], tpi)),
                                M=float(M_of(k, deff(ITER["saved_source"]["L"], tpi)))) for kname, k in K.items()}

out = dict(
    meta=dict(script="research/claim_debts_20261022/h06_h17/h06_h17_desk.py", python=sys.version,
              inputs=IN, inputs_sha256={k: sha(v) for k, v in IN.items()},
              rigour="R1 desk (necessary conditions only; TRIG-HWACT dormant; no layout or architecture model)",
              conventions=dict(T_C_s=float(T_C), sigma_over_e=float(SIG_E), t_layer_s=float(T_LAYER),
                               supply_T_per_s=float(SUPPLY), width=WIDTH)),
    selfcheck=dict(D_eff_floor=float(D_floor), M_recomputed=float(M_of(K["window_certified"], D_floor)), M_run006=M_ref),
    H17_necessary_conditions=h17,
    H06=h06,
    c11_hook=c11_hook if c11_hook else "C11 summary absent at run time; saved-source T excludes selector/reflection T",
)
os.makedirs(OUT, exist_ok=False)
with open(os.path.join(OUT, "h06_h17.json"), "x", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1)
for r in h17:
    print(r["k_class"], r["iterate"], "M=%.4g" % r["M_primary"], r["bound_at_primary"],
          "t_req(M<=1)=%.3g s" % r["M<=1"]["t_layer_required_s"], "R_req(M<=1)=%.3g T/s" % r["M<=1"]["T_per_s_required"],
          "t_req(M<=10)=%.3g s" % r["M<=10"]["t_layer_required_s"], "R_req(M<=10)=%.3g T/s" % r["M<=10"]["T_per_s_required"])
print(json.dumps(h06, indent=1))
