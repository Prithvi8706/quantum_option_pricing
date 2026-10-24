"""C03/E07 complete-price allocation at the binding cell (B8x52, eps = $0.001), R1 desk ledger.

Usage (from the worktree root):
    <frontier_t0_env python> -I -S -B research/claim_debts_20261022/c03/c03_allocation.py RUN [A2A_SUMMARY] [C11_SUMMARY]

Failure side: every row is either cited to a saved certificate (with sha256) or an explicit,
labelled hardware premise. Dollar side: A1 from P2; A2a from the clip-split certificate if given
(else the saved bridge total and the desk value are reported, not certified); A2c/A1a readout
from the U2 compile if given. Exact Fractions throughout; outputs are exclusive-create.
"""
import hashlib
import json
import os
import sys
from fractions import Fraction as F

ROOT = os.getcwd()
RUN = sys.argv[1]
A2A = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != "-" else None
C11 = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] != "-" else None
U1 = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] != "-" else None
OUT = os.path.join(ROOT, "results", "claim_debts_20261022", "c03", RUN)

LP = "results/limitation_program_20261001/"
IN = {
    "g2_ledger": LP + "E07_original_BM_G2_composition_run001/B8x52_G2_composed_ledger.json",
    "e07_ledger": LP + "E07_complete_run001/B8x52_complete_price_ledger.json",
    "e07_schedule": LP + "E07_schedule_run001/schedule.json",
    "e03_audit": LP + "E03_support_audit_run002/summary.json",
    "p2_window": "results/frontier_probe_20261021/p2/run002/p2_window.json",
    "p2_self_mean": "results/frontier_probe_20261021/p2/run003_self_mean/p2c_self_mean.json",
    "headline": "results/frontier_probe_20261021/headline/run006/headline_table.json",
    "bias_desk": "results/plan110_w0/ws_small/bias_desk_run001/bias_desk.json",
}
if A2A:
    IN["a2a_summary"] = A2A
if C11:
    IN["c11_summary"] = C11
if U1:
    IN["u1_summary"] = U1


def sha(p):
    with open(os.path.join(ROOT, p), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def load(k):
    with open(os.path.join(ROOT, IN[k]), encoding="utf-8") as f:
        return json.load(f)


def frac(x):
    if isinstance(x, list):
        return F(int(x[0]), int(x[1]))
    if isinstance(x, str):
        return F(x)
    return F(x)


def disp(x):
    return float(x)


g2 = load("g2_ledger")
sm = load("p2_self_mean")["cells"]["B8x52|0.001"]["best"]
hd = load("headline")
desk = load("bias_desk")["cases"]["B8x52"]

EPS = F(1, 1000)
FAIL_CAP = F(1, 100)

# --- facts read from saved certificates ---------------------------------------------------
g2_fail_names = [t["name"] for t in g2["failure_terms"]]
g2_dollar = {t["name"]: t for t in g2["dollar_terms"]}
bridge = g2_dollar["original_joint_law_and_native_financial_bias"]
bridge_total = frac(bridge["bound"])
bridge_covers = bridge["covers"]
assert "finite_input_law_and_joint_Box_Muller" in bridge_covers
assert "clipped_log_tail" in bridge_covers
assert "native_arithmetic_and_polynomial" in bridge_covers
for name in ("monitoring_policy", "surrogate", "random_preparation"):
    assert frac(g2_dollar[name]["bound"]) == 0
acq = [t for t in g2["failure_terms"] if t["name"] == "certificate_acquisition"][0]
assert frac(acq["bound"]) == 0
# No failure term in the composed ledger is attached to the source / bridge: the bridge is a
# deterministic bound on an expectation (pay once), not an event with a probability.
assert not any("bridge" in n or "source" in n or "law" in n for n in g2_fail_names), g2_fail_names

d1, d2 = F(sm["delta1"]), F(sm["delta2"])
N1, N2 = int(sm["N1"]), int(sm["N2"])
N_sm = N1 + N2
assert N_sm == int(sm["N_total"])

# D_eff floor at the binding cell, read from the headline run.
cell = [c for c in hd["cells"] if c["case"] == "B8x52" and abs(c["eps"] - 0.001) < 1e-12][0]
D_eff_floor = F(str(cell["D_eff_primary"]["used"]))
T_PER_LAYER = 10**12 * F(100, 10**9)  # 1e12 T/s x 100 ns = 1e5 T per layer (primary convention)
WIDTH = 10**7  # primary qubit budget

# --- failure ledger (union bound), one per estimator variant --------------------------------
pw = load("p2_window")["k"]["B8x52|0.001|0.45eps|8192/211|price+L1|with_impl_budget|fail 3/1000"]
u1 = load("u1_summary") if U1 else None
u1_ok = bool(u1 and u1.get("all_checks_pass") and u1.get("p2_assumption_covered"))
B3 = F(0)  # source / financial bridge: deterministic dollar bound (cited above)
B_acq = F(0)  # deterministic all-input support, no statistical acquisition
B5 = F(0)  # direction-select and controlled powers: exact in the Clifford+T cost model
VARIANTS = {
    "window_quantum_only_mean": dict(k=sm["k"], N=N_sm, B1=d1 + d2, B2=F(0),
        B1_ev=IN["p2_self_mean"], B2_status="removed",
        B2_ev="quantum-only first stage (delta1 = %s) replaces U1; no classical price enters" % d1),
    "window_certified_U1": dict(k=pw["k_direction_select"], N=int(pw["N_calls"]), B1=F(3, 1000),
        B2=F(u1["delta_U"]) if u1_ok else None, B1_ev=IN["p2_window"],
        B2_status="cert (R1)" if u1_ok else "unknown (no U1 certificate)",
        B2_ev=(IN["u1_summary"] + ": m_cert = %.10f covers the P2 premise m = %.10f" % (u1["m_cert_float"], u1["p2_assumed_m"]))
        if u1_ok else ""),
}


def h18(N, B4, T_per_iterate, label):
    T_total = N * T_per_iterate
    layers = N * (T_per_iterate / T_PER_LAYER)
    qlayers = layers * WIDTH
    return {"basis": label, "iterates": N, "T_per_iterate": disp(T_per_iterate), "T_total": disp(T_total),
            "logical_layers": disp(layers), "qubit_layers": disp(qlayers),
            "required_logical_failure_per_T": disp(B4 / T_total),
            "required_logical_failure_per_qubit_layer": disp(B4 / qlayers)}


c11 = load("c11_summary") if C11 else None
ledgers = {}
for vname, v in VARIANTS.items():
    if v["B2"] is None:
        ledgers[vname] = {"complete": False, "reason": v["B2_status"]}
        continue
    B4 = FAIL_CAP - (v["B1"] + v["B2"] + B3 + B_acq + B5)
    assert B4 > 0
    rows_h18 = [h18(v["N"], B4, D_eff_floor * T_PER_LAYER, "W0 floor D_eff = %s layers (mod, q+)" % float(D_eff_floor))]
    if c11:
        rows_h18.append(h18(v["N"], B4, F(c11["iterate"]["t_count_qf"]),
                            "C11 compiled iterate, 4 T per Toffoli (q+; literal count %d)" % c11["iterate"]["t_count_literal"]))
    failure = [
        {"row": "B1", "event": "window estimator (parts 3-4 inside)", "allocation": str(v["B1"]), "status": "cert",
         "evidence": v["B1_ev"]},
        {"row": "B2", "event": "U1 classical mean certificate", "allocation": str(v["B2"]), "status": v["B2_status"],
         "evidence": v["B2_ev"]},
        {"row": "B3", "event": "source / financial-bridge events", "allocation": "0", "status": "cert (by citation)",
         "evidence": IN["g2_ledger"] + ": the A02 bridge is a pay-once dollar bound covering " + ", ".join(bridge_covers)
         + "; the composed ledger's failure terms are " + ", ".join(g2_fail_names) + " only"},
        {"row": "B3a", "event": "certificate acquisition", "allocation": "0", "status": "cert (by citation)",
         "evidence": IN["g2_ledger"] + " certificate_acquisition bound 0 (deterministic all-input support)"},
        {"row": "B5", "event": "direction-select and controlled powers", "allocation": "0",
         "status": "exact in cost model", "evidence": "v4 sec. 4.2"},
        {"row": "B4", "event": "physical (logical) failure over the whole computation", "allocation": str(B4),
         "status": "assm (explicit hardware premise; H18 condition)", "evidence": "h18_condition"},
    ]
    assert sum(F(r["allocation"]) for r in failure) == FAIL_CAP
    ledgers[vname] = {"k": v["k"], "iterates": v["N"], "failure_ledger": failure,
                      "failure_total": str(FAIL_CAP), "h18_condition": rows_h18, "complete": True}

# --- dollar ledger --------------------------------------------------------------------------
A1 = F(45, 100) * EPS
bias_reserve = EPS - A1
dollar = [{"row": "A1", "term": "statistical (window AE, parts 1-4)", "bound": disp(A1), "status": "cert", "evidence": IN["p2_window"]}]
a2a_cert = None
if A2A:
    a2 = load("a2a_summary")
    a2a_cert = a2["cases"]["B8x52"].get("certified_total_upper_rounded_up_2^-64") if a2.get("all_checks_pass") else None
    if a2a_cert is not None:
        a2a_cert = frac(a2a_cert)
if a2a_cert is not None:
    dollar.append({"row": "A2a", "term": "finite law + clipped tail + native arithmetic (clip-split certificate)",
                   "bound": disp(a2a_cert), "status": "cert (R1)", "evidence": IN["a2a_summary"]})
else:
    dollar.append({"row": "A2a", "term": "finite law + clipped tail + native arithmetic",
                   "bound": disp(bridge_total), "status": "cert, but exceeds the 0.55 eps reserve; desk k=3 value %.4g is mod"
                   % desk["clamp_lowered_by_k_binades"]["3"]["total"], "evidence": IN["g2_ledger"]})
readout = None
if c11 and c11["checks"]["u2_readout_within_2_pow_m39"]:
    # bound 2^-41 + S'*(enclosure width) <= 2^-39 for every (j, l); C11 run001 u2_wrapper.json readout block
    readout = F(1, 2**39)
    dollar.append({"row": "A1a/A2c", "term": "U2 wrapper readout and binary64 post-processing", "bound": disp(readout),
                   "status": "cert (R1)", "evidence": IN["c11_summary"]})
else:
    dollar.append({"row": "A1a/A2c", "term": "U2 wrapper readout", "bound": None, "status": "open (C11/U2 pending)", "evidence": ""})

bias_used = (a2a_cert if a2a_cert is not None else bridge_total) + (readout if readout is not None else 0)
dollar_complete = a2a_cert is not None and readout is not None
fits = bias_used <= bias_reserve

out = {
    "meta": {
        "script": "research/claim_debts_20261022/c03/c03_allocation.py",
        "python": sys.version,
        "inputs_sha256": {k: sha(v) for k, v in IN.items()},
        "inputs": IN,
        "rigour": "R1 desk ledger (exact arithmetic; certificates cited by sha256; no new physics)",
        "cell": "B8x52, eps = $0.001, primary conventions, window estimator variants",
    },
    "variants": ledgers,
    "dollar_ledger": dollar,
    "dollar_bias_reserve": disp(bias_reserve),
    "dollar_bias_used": disp(bias_used),
    "dollar_bias_fits_reserve": fits,
    "dollar_ledger_complete": dollar_complete,
}
for vname, lg in ledgers.items():
    lg["complete_price_status"] = (
        ("failure budget fully allocated (B4 = %s explicit hardware premise)" % lg["failure_ledger"][-1]["allocation"]
         if lg["complete"] else "failure budget NOT allocated: " + lg["reason"])
        + "; dollar side " + ("complete and within the 0.55 eps reserve" if (dollar_complete and fits) else "NOT complete"))
out["complete_price_status"] = {v: lg["complete_price_status"] for v, lg in ledgers.items()}
os.makedirs(OUT, exist_ok=False)
with open(os.path.join(OUT, "c03_ledger.json"), "x", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
print(json.dumps({k: out[k] for k in ("dollar_bias_used", "dollar_bias_fits_reserve", "dollar_ledger_complete",
                                       "complete_price_status")}, indent=1))
for vname, lg in ledgers.items():
    for r in lg.get("h18_condition", []):
        print(vname, r)
