"""WS-floor (plan110 W0): idealized clean-call reaction-layer floor, R0 screen.

Item A01 with A16, A09, A08, A02, A07, A13, F05 and F20 as parameters. See SPEC.md.

Stdlib only. Run under .context/frontier_t0_env/Scripts/python.exe -I -S -B (3.12.4).
All outputs are written with exclusive create (mode "x"). rows.jsonl is created
exclusively and then appended one row per sub-result.

Unit: one reaction layer = one layer of parallel temporary-AND gates (A16). The clean call
is forward + reverse = 2 x forward reaction layers; call T-count = 2 x 4 x forward ANDs
(+ synthesized-rotation T where a loader uses them). These are idealized literature-constant
constructions, not lower bounds.
"""

import argparse
import hashlib
import json
import math
import os
import sys
import time
from fractions import Fraction
from heapq import heappop, heappush

REPO = "C:/Users/prith/quantum_option_pricing"
RL = REPO + "/results/limitation_program_20261001"
SCRATCH = ("C:/Users/prith/AppData/Local/Temp/claude/C--Users-prith-quantum-option-pricing/"
           "3cc032fb-36f0-4c77-b733-779e62fbfea3/scratchpad/plan110")
CASES = {"B4x12": (4, 12), "B8x52": (8, 52)}
INPUTS = {
    "w0_card": REPO + "/research/plan110_w0/W0_CARD.md",
    "gap_ledger": REPO + "/docs/program_plan_20261010/supporting/gap_ledger.json",
    "a01_run014_summary": RL + "/A01_run014/summary.json",
    "ccx_depth_screen": SCRATCH + "/h_tools/ccx_depth_screen.json",
    "gap_calc": SCRATCH + "/gap_calc.py",
}
for _c in CASES:
    INPUTS["source_" + _c] = RL + "/A10_coefficient_run001/" + _c + "/source.json"
LIBDIR = {c: RL + "/A10_coefficient_run001/" + c + "/min-depth/leaves" for c in CASES}

# Financial constants of the accepted builder (research/advantage_frontier_20260923/
# barrier_oracle_depth.py, read in this session); used only to locate DAG boundaries and
# CSD weights; the DAG self-check verifies them.
SIGMA, CORR, T_MAT = 0.3, 0.4, 1.0
FRAC = 40
UNIFORM_BITS = 32
WIDTHS = {"unlimited": None, "W1e7": 10**7, "W1e6": 10**6}
B_SET = (4, 6, 8, 10, 12, 14, 16, 20)  # table address bits; <= 20 is the "unlimited" cap
T_LAYERS = {"10ns": Fraction(1, 10**8), "100ns": Fraction(1, 10**7),
            "1us": Fraction(1, 10**6), "10us": Fraction(1, 10**5)}
SUPPLY = {"1e11": 10**11, "1e12": 10**12, "1e13": 10**13}
F20_CREDIT = {"B4x12": Fraction(573, 125), "B8x52": Fraction(515, 114)}  # rows_F F20 text
E_EQ_EPS = Fraction(20, 9)  # N_calls ~ sigma/e; e = eps instead of 0.45 eps


def lab(value, label, direction, note=None):
    out = {"value": value, "label": label, "direction": direction}
    if note:
        out["note"] = note
    return out


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


class Rows:
    def __init__(self, path):
        self.path = path
        with open(path, "x", encoding="utf-8", newline="\n"):
            pass

    def add(self, row):
        row = dict(row, ts=time.strftime("%Y-%m-%dT%H:%M:%S"))
        with open(self.path, "a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(row, sort_keys=True) + "\n")


# ----------------------------------------------------------------------------- primitives
def clog2(x):
    return (int(x) - 1).bit_length() if x > 1 else 0


def adder(w):
    """Kogge-Stone carry-lookahead (A08 floor): ceil(log2 w)+1 AND layers."""
    if w <= 1:
        return 0, 0
    lv = clog2(w)
    return lv + 1, w + sum(2 * max(w - 2 ** j, 0) for j in range(lv))


def comparator(w):
    """Carry-out tree only."""
    return (clog2(w) + 1, 3 * w) if w > 1 else (0, 0)


DADDA = [2]
while DADDA[-1] < 10 ** 9:
    DADDA.append(DADDA[-1] * 3 // 2)


def dadda(h):
    """3:2 stages to reduce h rows to 2 (one AND layer each: maj = a^((a^b)(a^c)))."""
    if h <= 2:
        return 0
    return next(j for j, d in enumerate(DADDA) if d >= h)


def mul(a, b, pw=None):
    """Dadda/Wallace multiplier with temporary-AND (A09 floor)."""
    rows, cols = min(a, b), max(a, b)
    pw = pw or a + b
    ad, aa = adder(pw)
    return 1 + dadda(rows) + ad, a * b + max(rows - 2, 0) * cols + aa


def fma(rows, cols):
    ad, aa = adder(rows + cols)
    return 1 + dadda(rows + 1) + ad, rows * cols + max(rows - 1, 0) * cols + aa


def cmul(h, w):
    """Constant multiply: h = CSD (NAF) weight rows of shifted copies (Clifford)."""
    if h <= 1:
        return 0, 0
    ad, aa = adder(w)
    if h == 2:
        return ad, aa
    return dadda(h) + ad, (h - 2) * w + aa


def lookup(b):
    """Fan-out QROM: AND-tree minterms ceil(log2 b) layers, 2^(b+1) ANDs; data XOR is Clifford."""
    if b <= 1:
        return 0, 0
    return clog2(b), 2 ** (b + 1)


def naf_weight(c):
    c, w = abs(int(c)), 0
    while c:
        if c & 1:
            z = 2 - (c & 3)
            c -= z
            w += 1
        c >>= 1
    return w


def fe(p_rel, rows, addr_bits, b_res):
    """Piecewise polynomial f on 2^b_res segments; degree d with (d+1)*b_res >= p_rel; Estrin."""
    dp1 = max(1, -(-p_rel // b_res))
    levels = clog2(dp1)
    lk_d, lk_a = lookup(addr_bits)
    rows = max(rows, 1)
    f_d, f_a = fma(rows, p_rel)
    s_d, s_a = mul(rows, rows)
    n_fma, n_sq = dp1 - 1, max(levels - 1, 0)
    level1 = (dp1 // 2) * f_a + (s_a if levels > 1 else 0)
    return {"depth": lk_d + levels * f_d, "ands": lk_a + n_fma * f_a + n_sq * s_a,
            "peak": lk_a + 2 * level1, "words": dp1 + n_fma + n_sq, "degree": dp1 - 1,
            "levels": levels, "addr_bits": addr_bits}


# ----------------------------------------------------------------------------- loaders
def loader_options(kind, p, u=UNIFORM_BITS):
    """Yield (params, per-instance dict) for one loader kind ("..._q<grid bits>" suffix).

    per-instance dict: depth, ands, rot_t, peak, words, normals (outputs per instance).
    """
    q = int(kind.rsplit("_q", 1)[1]) if "_q" in kind else 0
    if kind == "free":  # F05
        yield {}, {"depth": 0, "ands": 0, "rot_t": 0, "peak": 0, "words": 1, "normals": 1}
    elif kind == "box_muller":  # current law, idealized leaves (two-sided msb range reduction)
        rr_d, e_bits = clog2(u) + 1, clog2(u)
        rr_a = 2 * (u * clog2(u) + u * u) + u
        m_d, m_a = mul(p, p)
        for bg in B_SET:
            g = fe(p, u - 1 - bg, bg + e_bits + 1, bg)
            for bc in B_SET:
                c = fe(p, u - 2 - bc, bc, bc)
                yield {"b_g": bg, "b_cos": bc, "deg_g": g["degree"], "deg_cos": c["degree"]}, {
                    "depth": max(rr_d + 1 + g["depth"], c["depth"]) + m_d,
                    "ands": rr_a + g["ands"] + 2 * c["ands"] + 2 * m_a, "rot_t": 0,
                    "peak": max(rr_a + g["peak"] + 2 * c["peak"], 4 * m_a),
                    "words": 3 + g["words"] + 2 * c["words"] + 2, "normals": 2}
    elif kind == "icdf":  # A02 quantile: one uniform per normal, midpoint-law complement Clifford
        rr_d, e_bits = clog2(u) + 1, clog2(u)
        rr_a = u * clog2(u) + u * u
        for b in B_SET:
            g = fe(p, u - 1 - b, b + e_bits, b)
            yield {"b": b, "deg": g["degree"]}, {
                "depth": rr_d + g["depth"], "ands": rr_a + g["ands"], "rot_t": 0,
                "peak": rr_a + g["peak"], "words": 2 + g["words"], "normals": 1}
    elif kind.startswith("alias_q"):  # coherent alias sampling (Babbush et al. 2018) on q-bit grid
        lk_d, lk_a = lookup(q)
        c_d, c_a = comparator(p)
        yield {"q": q, "mu": p}, {"depth": lk_d + c_d + 1, "ands": lk_a + c_a + q, "rot_t": 0,
                                  "peak": lk_a + c_a + q, "words": 2, "normals": 1}
    elif kind.startswith("gr_qrom_q"):  # Grover-Rudolph, QROM angles + phase-gradient adder
        ad, aa = adder(p)
        depth = sum(lookup(level)[0] + ad for level in range(q))
        ands = sum(lookup(level)[1] + aa + p for level in range(q))
        yield {"q": q, "b_rot": p}, {"depth": depth, "ands": ands, "rot_t": 0,
                                     "peak": 2 * (lookup(q - 1)[1] + aa + p), "words": 1,
                                     "normals": 1}
    elif kind.startswith("a03_gr_synth_q"):  # A03 recursive GR, Ross-Selinger rotations 3 log2(1/d)
        rot = (2 ** q - 1) * 3 * p
        yield {"q": q, "b_rot": p, "t_per_rotation": 3 * p}, {
            "depth": rot, "ands": 0, "rot_t": rot, "peak": 0, "words": 1, "normals": 1}
    elif kind.startswith("a04_mps_chi8_q"):  # A04 MPS bond 8, column-by-column isometry, QROM mux
        chi = 8
        s = clog2(chi) + 1
        mux = 2 * s * chi
        lk_d, lk_a = lookup(s - 1)
        ad, aa = adder(p)
        yield {"q": q, "chi": chi, "mux_per_site": mux, "b_rot": p}, {
            "depth": q * mux * (lk_d + ad), "ands": q * mux * (lk_a + aa + p), "rot_t": 0,
            "peak": 2 * (lk_a + aa + p), "words": 1, "normals": 1}
    else:
        raise ValueError(kind)


LOADERS = ("box_muller", "icdf", "alias_q10", "alias_q16", "alias_q20", "gr_qrom_q10",
           "a03_gr_synth_q10", "a04_mps_chi8_q10", "free")
GRID_LOADERS = ("alias_q10", "alias_q16", "alias_q20", "gr_qrom_q10", "a03_gr_synth_q10",
                "a04_mps_chi8_q10")


# ----------------------------------------------------------------------------- coarse model
def stage(name, depth, inst, ands, peak, words, out_words, rot_t=0, local_ok=True):
    return {"name": name, "depth": depth, "inst": inst, "ands": ands, "peak": peak,
            "words": words, "out_words": out_words, "rot_t": rot_t, "local_ok": local_ok}


def path_stage_options(na, nt, n, p, free_exp):
    dt = Fraction(1, nt)
    cc = round(SIGMA * math.sqrt(float(dt) * CORR) * 2 ** FRAC)
    ci = round(SIGMA * math.sqrt(float(dt) * (1 - CORR)) * 2 ** FRAC)
    h_inc = naf_weight(cc) + naf_weight(ci) + 1 + 1  # + drift row + log S0 row
    inc_d = dadda(h_inc)
    prefix = {}
    prefix["tree"] = [
        stage("increments", inc_d, na * nt, (h_inc - 2) * n, (h_inc - 2) * n * 2, 2, 2),
        stage("date_prefix", dadda(2 * nt), na,
              sum(max(2 * t - 2, 0) * n for t in range(1, nt + 1)),
              2 * sum(max(2 * t - 2, 0) * n for t in range(1, nt + 1)), 2 * nt, 2 * nt)]
    lv = clog2(nt)
    prefix["hillis_steele_cs"] = [
        stage("increments", inc_d, na * nt, (h_inc - 2) * n, (h_inc - 2) * n * 2, 2, 2),
        stage("date_prefix", 2 * lv, na, lv * nt * 2 * n, 2 * nt * 2 * n, lv * nt * 2, 2 * nt)]
    merged_a = sum(max(t * h_inc - 2, 0) * n for t in range(1, nt + 1))
    prefix["merged"] = [stage("increments+date_prefix", dadda(nt * h_inc), na, merged_a,
                              2 * merged_a, 2 * nt, 2 * nt)]
    cpa_d, cpa_a = adder(n)
    cl_d, cl_a = comparator(n)
    post = [stage("carry_propagate", cpa_d, na * nt, cpa_a, 2 * cpa_a, 1, 1),
            stage("clip", cl_d + 1, na * nt, 2 * cl_a + 2 * n, 2 * (2 * cl_a + 2 * n), 1, 1)]
    exps = {}
    if free_exp:  # A13 free-exponential bound
        exps["free"] = [stage("exp", 0, na * nt, 0, 0, 1, 1)]
    else:
        for b in B_SET:
            f = fe(p + 12, p - b, 5 + b, b)  # bounded clip domain: 5 integer address bits
            exps["direct_b%d" % b] = [stage("exp", f["depth"], na * nt, f["ands"], f["peak"],
                                            f["words"], 1)]
            hk = naf_weight(round(2 ** FRAC / math.log(2)))
            k_d, k_a = cmul(hk, n)
            r_d, r_a = cmul(5 + 1, n)
            sh_d, sh_a = clog2(5) + 1, 2 ** 6 + n * 32
            f2 = fe(p + 12, p - b, b, b)
            exps["ln2_rr_b%d" % b] = [stage(
                "exp", k_d + r_d + f2["depth"] + sh_d, na * nt, k_a + r_a + f2["ands"] + sh_a,
                max(2 * (k_a + r_a), f2["peak"]), f2["words"] + 3, 1)]
    al_d1, al_a1 = cmul(na + 1, n)
    al_c, al_ca = comparator(n + 3)
    av_h = na * nt + 1
    av_d, av_a = cmul(av_h, n + clog2(na * nt))
    tail = {"alive": (dadda(na + 1) + al_c + clog2(nt), nt * ((na - 1) * n + al_ca) + nt),
            "average": (av_d, av_a)}
    return prefix, post, exps, tail, {"c_common": cc, "c_idio": ci, "h_inc_rows": h_inc}


def evaluate(stages, tail, n, W, uniform_bits, modes):
    """Return dict or None (infeasible). modes: set of stage names run in local-cleanup mode."""
    retained = uniform_bits + 1  # + payoff flag
    for s in stages:
        retained += s["inst"] * (s["out_words"] if s["name"] in modes else s["words"]) * n
    retained += 2 * n  # alive/average outputs
    if W is not None and retained >= W:
        return None
    free = None if W is None else W - retained
    total, ands, rot, peak_used, detail = 0, 0, 0, 0, []
    for s in stages:
        mult = 2 if s["name"] in modes else 1
        pk = s["inst"] * s["peak"]
        rounds = 1 if free is None or pk <= free else -(-pk // free)
        if free is not None and s["peak"] > free:
            return None
        d = s["depth"] * mult * rounds
        total += d
        ands += s["inst"] * s["ands"] * mult
        rot += s["inst"] * s["rot_t"] * mult
        peak_used = max(peak_used, min(pk, free) if free is not None else pk)
        detail.append({"stage": s["name"], "depth_per_round": s["depth"] * mult,
                       "rounds": rounds, "depth": d, "instances": s["inst"],
                       "local_cleanup": s["name"] in modes})
    td = max(tail["alive"][0], tail["average"][0]) + 2
    total += td
    ands += tail["alive"][1] + tail["average"][1] + 2 * n
    detail.append({"stage": "barrier_and_payoff", "depth_per_round": td, "rounds": 1,
                   "depth": td, "instances": 1, "local_cleanup": False})
    return {"forward": total, "forward_ands": ands, "forward_rot_t": rot,
            "width": retained + peak_used, "retained_qubits": retained, "stages": detail}


def coarse_floor(case, W, loader_kind, n, p, free_exp):
    na, nt = CASES[case]
    n_norm = nt * (na + 1)
    prefix, post, exps, tail, consts = path_stage_options(na, nt, n, p, free_exp)
    best, best_sup = None, None
    mode_sets = [set(), {"loader"}, {"exp"}, {"loader", "exp"},
                 {"loader", "exp", "date_prefix", "increments+date_prefix", "increments"}]
    t_per_layer = Fraction(SUPPLY["1e12"]) * T_LAYERS["100ns"]  # primary supply x layer time
    for lp, li in loader_options(loader_kind, p):
        inst = -(-n_norm // li["normals"])
        lst = stage("loader", li["depth"], inst, li["ands"], li["peak"], li["words"],
                    li["normals"], li["rot_t"])
        for pk, pst in prefix.items():
            for ek, est in exps.items():
                stages = [lst] + pst + post + est
                for modes in mode_sets:
                    r = evaluate(stages, tail, n, W, n_norm * UNIFORM_BITS, modes)
                    if r is None:
                        continue
                    tc = 2 * (4 * r["forward_ands"] + r["forward_rot_t"])
                    key = (r["forward"], tc)
                    choice = {"loader_params": lp, "prefix": pk, "exp": ek,
                              "local_cleanup": sorted(modes)}
                    if best is None or key < best[0]:
                        best = (key, dict(r, **choice))
                    eff = max(Fraction(2 * r["forward"]), Fraction(tc) / t_per_layer)
                    if best_sup is None or (eff, tc) < best_sup[0]:
                        best_sup = ((eff, tc), {"call": 2 * r["forward"], "call_t": tc,
                                                "width": r["width"],
                                                "eff_depth_1e12_100ns": float(eff), **choice})
    if best is None:
        return None
    r = best[1]
    r["supply_aware_design"] = best_sup[1]
    loader_depth = sum(s["depth"] for s in r["stages"] if s["stage"] == "loader")
    exp_depth = sum(s["depth"] for s in r["stages"] if s["stage"] == "exp")
    r.update(call=2 * r["forward"], call_t=2 * (4 * r["forward_ands"] + r["forward_rot_t"]),
             loader_depth=loader_depth, exp_depth=exp_depth,
             loader_share=str(Fraction(loader_depth, r["forward"])) if r["forward"] else "0",
             loader_share_float=loader_depth / r["forward"] if r["forward"] else 0.0,
             consts=consts)
    return r


# ----------------------------------------------------------------------------- DAG reweight
def load_dag(case):
    src = json.load(open(INPUTS["source_" + case], encoding="utf-8"))
    keys = sorted({c["leaf"] for c in src["forward_calls"]})
    leaves = {}
    for k in keys:
        m = json.load(open(os.path.join(LIBDIR[case], k + ".json"), encoding="utf-8"))
        leaves[k] = {"op": m["op"], "params": m.get("params", {}), "spec": m.get("spec", {}),
                     "input_contract": m.get("input_contract") or {},
                     "t_depth": m["resources"]["t_depth"], "outs": len(m["outs"])}
    calls = src["forward_calls"]
    producer = {}
    for i, c in enumerate(calls):
        for v in c["out"]:
            producer[v] = i
    parents = [sorted({producer[v] for v in c["args"] if v in producer}) for c in calls]
    return src, leaves, calls, producer, parents


def topo(parents):
    n = len(parents)
    children = [[] for _ in range(n)]
    indeg = [len(p) for p in parents]
    for i, ps in enumerate(parents):
        for p in ps:
            children[p].append(i)
    order = [i for i in range(n) if not indeg[i]]
    k = 0
    while k < len(order):
        i = order[k]
        k += 1
        for ch in children[i]:
            indeg[ch] -= 1
            if not indeg[ch]:
                order.append(ch)
    assert len(order) == n, "cyclic DAG"
    return order, children


def longest(order, parents, depth):
    arr = [0] * len(order)
    for i in order:
        arr[i] = depth[i] + max((arr[p] for p in parents[i]), default=0)
    return arr


def classify(case, calls, leaves, producer, parents, children, order):
    na, nt = CASES[case]
    dt = 1.0 / nt
    cc = round(SIGMA * math.sqrt(dt * CORR) * 2 ** FRAC)
    ci = round(SIGMA * math.sqrt(dt * (1 - CORR)) * 2 ** FRAC)
    op = [leaves[c["leaf"]]["op"] for c in calls]
    normals = {c["args"][0] for i, c in enumerate(calls)
               if op[i] == "cmul" and leaves[c["leaf"]]["params"].get("c") in (cc, ci)}
    assert len(normals) == nt * (na + 1), ("normal count", len(normals))
    loader = set()
    stack = [producer[v] for v in normals if v in producer]
    while stack:
        i = stack.pop()
        if i in loader:
            continue
        loader.add(i)
        stack.extend(parents[i])
    # increments: add(add(cmul(z), cmul(z)), const)
    incr = []
    for i, c in enumerate(calls):
        if op[i] != "add" or len(c["args"]) != 2:
            continue
        ps = [producer.get(v) for v in c["args"]]
        if None in ps:
            continue
        kinds = sorted(op[j] for j in ps)
        if kinds != ["add", "const"]:
            continue
        a = ps[0] if op[ps[0]] == "add" else ps[1]
        inner = [producer.get(v) for v in calls[a]["args"]]
        if None not in inner and all(op[j] == "cmul" and calls[j]["args"][0] in normals
                                     for j in inner):
            incr.append(i)
    assert len(incr) == na * nt, ("increment count", len(incr))

    def desc(seeds):
        seen, st = set(), list(seeds)
        while st:
            i = st.pop()
            if i in seen:
                continue
            seen.add(i)
            st.extend(children[i])
        return seen

    def anc(seeds):
        seen, st = set(), list(seeds)
        while st:
            i = st.pop()
            if i in seen:
                continue
            seen.add(i)
            st.extend(parents[i])
        return seen

    norm_consumers = [i for i, c in enumerate(calls) if any(v in normals for v in c["args"])]
    corr = (desc(norm_consumers) & anc(incr)) - loader
    path = set(range(len(calls))) - loader - corr
    inv_ln2 = round(2 ** FRAC / math.log(2))
    x_consumers = [i for i, c in enumerate(calls)
                   if op[i] == "cmul" and leaves[c["leaf"]]["params"].get("c") == inv_ln2]
    assert len(x_consumers) == na * nt, ("exp count", len(x_consumers))
    xvals = {calls[i]["args"][0] for i in x_consumers}
    xc = [i for i, c in enumerate(calls) if any(v in xvals for v in c["args"])]
    dx = desc(xc)
    shifts = [i for i in dx if op[i] == "shift"]
    assert len(shifts) == na * nt, ("exp shift count", len(shifts))
    exp_region = dx & anc(shifts)
    return {"normals": normals, "loader": loader, "corr": corr, "path": path,
            "exp": exp_region, "op": op, "c_common": cc, "c_idio": ci}


def ideal_weight(leaf, n_scale=Fraction(1), b_sqrt=12):
    """Idealized (reaction depth, forward ANDs) for one DAG leaf; widths scaled for A07."""
    def w(x):
        return max(1, -(-(Fraction(x) * n_scale).numerator // (Fraction(x) * n_scale).denominator))
    o, prm, spec = leaf["op"], leaf["params"], leaf["spec"]
    n = w(72)
    if o in ("bits", "const"):
        return 0, 0
    if o in ("add", "sub"):
        return adder(n)
    if o == "lt":
        return comparator(n)
    if o in ("select", "positive"):
        return 1, n
    if o == "msb":
        return clog2(n), n * clog2(n)
    if o == "shift":
        cb = spec.get("count_bits", 7)
        return clog2(cb) + 1, 2 ** (cb + 1) + n * 2 ** cb
    if o == "lookup":
        return lookup(prm["bits"])
    if o == "mul":
        a1, a2 = spec.get("active_operand_bits", [72, 72])
        pw = spec.get("product_width", a1 + a2)
        return mul(w(a1), w(a2), w(pw))
    if o == "cmul":
        return cmul(naf_weight(prm["c"]), n)
    if o == "sqrt":
        ib = w(spec.get("active_input_bits", 46))
        ob = w(spec.get("result_bits", 43))
        f = fe(ob, ib - b_sqrt, b_sqrt + 1, b_sqrt)
        return (clog2(ib) + 1 + f["depth"] + 1,
                ib * clog2(ib) + ib * ib + f["ands"] + ob * clog2(ib))
    raise ValueError(o)


def schedule(order, parents, children, depth, ands, avail, max_skip=64):
    """Greedy critical-path list schedule under a live-AND cap (garbage held 2d)."""
    n = len(order)
    bl = [0] * n
    for i in reversed(order):
        bl[i] = depth[i] + max((bl[c] for c in children[i]), default=0)
    if any(a > avail for a in ands):
        return None
    indeg = [len(p) for p in parents]
    ready = sorted((-bl[i], i) for i in range(n) if not indeg[i])  # sorted list is a heap
    events, t, done, finish, free = [], 0, 0, 0, avail
    while done < n:
        skipped, fails = [], 0
        while ready and fails < max_skip:
            nb, i = heappop(ready)
            if ands[i] <= free:
                free -= ands[i]
                if depth[i] == 0:
                    free += ands[i]
                    done += 1
                    finish = max(finish, t)
                    for ch in children[i]:
                        indeg[ch] -= 1
                        if not indeg[ch]:
                            heappush(ready, (-bl[ch], ch))
                else:
                    heappush(events, (t + depth[i], 0, i))
                    heappush(events, (t + 2 * depth[i], 1, i))
            else:
                skipped.append((nb, i))
                fails += 1
        for x in skipped:
            heappush(ready, x)
        if done >= n:
            break
        t = events[0][0]
        while events and events[0][0] == t:
            _, kind, i = heappop(events)
            if kind == 0:
                done += 1
                finish = max(finish, t)
                for ch in children[i]:
                    indeg[ch] -= 1
                    if not indeg[ch]:
                        heappush(ready, (-bl[ch], ch))
            else:
                free += ands[i]
    return finish


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--skip-dag", action="store_true")
    args = ap.parse_args()
    out = args.out
    os.makedirs(out, exist_ok=True)
    rows = Rows(os.path.join(out, "rows.jsonl"))
    t0 = time.time()
    hashes = {k: sha256(v) for k, v in INPUTS.items()}
    rows.add({"sub": "inputs", "sha256": hashes, "python": sys.version.split()[0],
              "flags": {"isolated": sys.flags.isolated, "no_site": sys.flags.no_site,
                        "dont_write_bytecode": sys.flags.dont_write_bytecode}})
    ledger = json.load(open(INPUTS["gap_ledger"], encoding="utf-8"))
    a01 = json.load(open(INPUTS["a01_run014_summary"], encoding="utf-8"))
    ccx = json.load(open(INPUTS["ccx_depth_screen"], encoding="utf-8"))
    ccx_ratio = sorted({v["ratio"] for v in ccx.values()})
    a01_cases = {c["case"]: c for c in a01["cases"]}

    variants = {"base": (72, 40, False), "a07_narrow": (40, 24, False),
                "a13_free_exp": (72, 40, True), "a07_narrow+a13_free_exp": (40, 24, True)}
    coarse = {}
    for case in CASES:
        for wk, W in WIDTHS.items():
            for vk, (n, p, fx) in variants.items():
                for lk in LOADERS:
                    r = coarse_floor(case, W, lk, n, p, fx)
                    key = "|".join((case, wk, vk, lk))
                    coarse[key] = r
                    rows.add({"sub": "coarse", "case": case, "width": wk, "variant": vk,
                              "loader": lk, "label": "modelled", "direction": "quantum-favourable",
                              "feasible": r is not None,
                              **({} if r is None else {
                                  "forward": r["forward"], "call": r["call"],
                                  "call_t": r["call_t"], "width_qubits": r["width"],
                                  "loader_depth": r["loader_depth"],
                                  "loader_share": r["loader_share_float"],
                                  "exp_depth": r["exp_depth"], "prefix": r["prefix"],
                                  "exp": r["exp"], "loader_params": r["loader_params"],
                                  "local_cleanup": r["local_cleanup"],
                                  "supply_aware": r["supply_aware_design"],
                                  "stages": r["stages"]})})

    def best_loader(case, wk, vk, pool=GRID_LOADERS + ("box_muller", "icdf")):
        cand = [(coarse["|".join((case, wk, vk, lk))], lk) for lk in pool]
        cand = [(r, lk) for r, lk in cand if r is not None]
        return min(cand, key=lambda x: (x[0]["call"], x[0]["call_t"])) if cand else (None, None)

    # threshold cells
    cells = []
    for r in ledger["rows"]:
        cells.append({"case": r["case"], "eps": r["eps"], "T_C": r["T_C"],
                      "T_C_conv": r["T_C_conv"], "classical_best": r["classical_best"],
                      "sigma_over_e": r["sigma_over_e"], "source_bias_fits": r["source_bias_fits"],
                      "Dmax_k1": {t: r["Dmax_k1_" + t] for t in T_LAYERS}})

    def compare(r, case):
        """Unlimited-supply columns use the depth-optimal design; supply columns use the
        better of the depth-optimal and supply-aware designs (min effective depth)."""
        case_floor_call = r["call"]
        designs = [(r["call"], r["call_t"]),
                   (r["supply_aware_design"]["call"], r["supply_aware_design"]["call_t"])]
        res = []
        for c in cells:
            if c["case"] != case:
                continue
            row = {"eps": c["eps"], "T_C": c["T_C"], "T_C_conv": c["T_C_conv"],
                   "source_bias_fits": c["source_bias_fits"], "by_t_layer": {}}
            for tk, tl in T_LAYERS.items():
                d1 = Fraction(c["Dmax_k1"][tk])
                conv = {"base": d1, "e_eq_eps": d1 * E_EQ_EPS, "f20_sigma_credit": d1 * F20_CREDIT[case],
                        "e_eq_eps+f20": d1 * E_EQ_EPS * F20_CREDIT[case]}
                ent = {}
                for ck, dm in conv.items():
                    e = {"Dmax_k1": float(dm),
                         "k_10x_unlimited_supply": float(dm / case_floor_call),
                         "k_early_stop_unlimited_supply": float(30 * dm / case_floor_call)}
                    for sk, R in SUPPLY.items():
                        eff = min(max(Fraction(dc), Fraction(dt_) / (R * tl))
                                  for dc, dt_ in designs)
                        e["eff_depth_supply_" + sk] = float(eff)
                        e["k_10x_supply_" + sk] = float(dm / eff)
                        e["k_early_stop_supply_" + sk] = float(30 * dm / eff)
                    ent[ck] = e
                row["by_t_layer"][tk] = ent
            res.append(row)
        return res

    # refinement trigger: coarse floor x 3 within 10x of D_max(k=1) at 100 ns (any cell)
    trig = {}
    for case in CASES:
        r, lk = best_loader(case, "W1e7", "base")
        bm = coarse["|".join((case, "W1e7", "base", "box_muller"))]
        f = min(x["call"] for x in (r, bm) if x is not None)
        dm = max(c["Dmax_k1"]["100ns"] for c in cells if c["case"] == case)
        trig[case] = {"coarse_call_floor_W1e7": f, "max_Dmax_k1_100ns": dm,
                      "floor_times_k3_over_Dmax_k1": 3 * f / dm,
                      "within_10x": 3 * f <= 10 * dm}
    refine = any(v["within_10x"] for v in trig.values())
    rows.add({"sub": "refinement_trigger", "label": "modelled", "direction": "neutral",
              "rule": "coarse call floor x k=3 <= 10 x D_max(k=1) at 100 ns in some cell",
              "per_case": trig, "refine": refine})

    dag = {}
    selfcheck = {}
    if refine and not args.skip_dag:
        for case in CASES:
            src, leaves, calls, producer, parents = load_dag(case)
            order, children = topo(parents)
            # self-check: archived leaf T-depths reproduce A01_run014 dependency depth
            arr0 = longest(order, parents, [leaves[c["leaf"]]["t_depth"] for c in calls])
            yprod = producer[src["outputs"]["Y"]]
            got, want = arr0[yprod], a01_cases[case]["independent_forward_dependency_t_depth"]
            cls = classify(case, calls, leaves, producer, parents, children, order)
            selfcheck[case] = {"reproduced_forward_dependency_t_depth": got, "a01_run014": want,
                               "match": got == want, "normals": len(cls["normals"]),
                               "loader_calls": len(cls["loader"]), "corr_calls": len(cls["corr"]),
                               "path_calls": len(cls["path"]), "exp_region_calls": len(cls["exp"]),
                               "c_common": cls["c_common"], "c_idio": cls["c_idio"]}
            rows.add({"sub": "dag_selfcheck", "case": case, "label": "measured",
                      "direction": "neutral", **selfcheck[case]})
            assert got == want, selfcheck[case]
            na, nt = CASES[case]
            n_vals = src["values"]
            dres = {}
            for vk, scale in (("as_is", Fraction(1)), ("a07_narrow", Fraction(40, 72))):
                nbits = 72 if scale == 1 else 40
                wt = [ideal_weight(leaves[c["leaf"]], scale) for c in calls]
                dep = [x[0] for x in wt]
                an = [x[1] for x in wt]
                arr = longest(order, parents, dep)
                F = arr[yprod]
                # critical-path loader contribution: latest normal arrival on the Y path
                loader_cp = max(arr[producer[v]] for v in cls["normals"] if v in producer)
                dep_fl = [0 if i in cls["loader"] else d for i, d in enumerate(dep)]
                F_free = longest(order, parents, dep_fl)[yprod]
                dep_fx = [0 if i in cls["exp"] else d for i, d in enumerate(dep)]
                F_freeexp = longest(order, parents, dep_fx)[yprod]
                dep_both = [0 if (i in cls["exp"] or i in cls["loader"]) else d
                            for i, d in enumerate(dep)]
                F_both = longest(order, parents, dep_both)[yprod]
                ands_all = sum(an)
                ands_loader = sum(an[i] for i in cls["loader"])
                ands_exp = sum(an[i] for i in cls["exp"])
                # substitute best coarse loader (W unlimited, same width variant)
                cvk = "base" if scale == 1 else "a07_narrow"
                sub = {}
                for lk in LOADERS:
                    lr = coarse["|".join((case, "unlimited", cvk, lk))]
                    if lr is None:
                        continue
                    ld = lr["loader_depth"]
                    dep_s = [0 if i in cls["loader"] else d for i, d in enumerate(dep)]
                    # normals arrive at ld: add ld to every consumer chain that starts at a normal
                    arr_s = [0] * len(calls)
                    for i in order:
                        base = max((arr_s[p] for p in parents[i]), default=0)
                        if any(v in cls["normals"] for v in calls[i]["args"]):
                            base = max(base, ld)
                        arr_s[i] = dep_s[i] + base
                    sub[lk] = {"forward": arr_s[yprod], "loader_depth": ld}
                widths = {}
                for wk, W in WIDTHS.items():
                    retained = n_vals * nbits + len(src["inputs"]) * UNIFORM_BITS
                    if W is None:
                        widths[wk] = {"forward": F, "call": 2 * F, "feasible": True,
                                      "retained_qubits": retained}
                        continue
                    avail = W - retained
                    if avail <= 0:
                        widths[wk] = {"feasible": False, "retained_qubits": retained,
                                      "reason": "full SSA retention exceeds W; pebbling needed"}
                        continue
                    area = Fraction(sum(2 * d * a for d, a in zip(dep, an)), avail)
                    mk = schedule(order, parents, children, dep, an, avail)
                    widths[wk] = {"feasible": mk is not None, "retained_qubits": retained,
                                  "forward": mk, "call": None if mk is None else 2 * mk,
                                  "area_lower_bound_forward": float(max(Fraction(F), area))}
                dres[vk] = {"forward_unlimited": F, "call_unlimited": 2 * F,
                            "loader_critical_path_contribution": loader_cp,
                            "loader_share_critical_path": loader_cp / F,
                            "forward_free_loader": F_free,
                            "loader_share_marginal": 1 - F_free / F,
                            "forward_free_exp": F_freeexp, "forward_free_loader_and_exp": F_both,
                            "forward_ands": ands_all, "call_t": 8 * ands_all,
                            "loader_ands": ands_loader, "exp_ands": ands_exp,
                            "best_loader_substitution": sub, "by_width": widths,
                            "required_T_per_s_100ns": {
                                wk: float(Fraction(8 * ands_all) / (v["call"] * T_LAYERS["100ns"]))
                                for wk, v in widths.items() if v.get("call")},
                            "supply_limited_call_1e12_100ns": {
                                wk: max(v["call"], 8 * ands_all / 10 ** 5)
                                for wk, v in widths.items() if v.get("call")},
                            "labels": "modelled; quantum-favourable (idealized leaves on the "
                                      "accepted A10 DAG structure)"}
                rows.add({"sub": "dag_reweight", "case": case, "variant": vk,
                          "label": "modelled", "direction": "quantum-favourable",
                          **{k: v for k, v in dres[vk].items()}})
            dag[case] = dres

    # headline assembly
    headline = {}
    for case in CASES:
        hc = {}
        for wk in WIDTHS:
            def g(vk, lk):
                return coarse["|".join((case, wk, vk, lk))], lk
            r_best, lk_best = best_loader(case, wk, "base")
            r_bfx, lk_bfx = best_loader(case, wk, "a13_free_exp")
            r_ball, lk_ball = best_loader(case, wk, "a07_narrow+a13_free_exp",
                                          GRID_LOADERS + ("box_muller", "icdf", "free"))
            ent = {}
            for nm, (r, lk) in (("box_muller_current_law", g("base", "box_muller")),
                                ("icdf_A02", g("base", "icdf")),
                                ("best_loader", (r_best, lk_best)),
                                ("free_loader_F05", g("base", "free")),
                                ("box_muller+free_exp_A13", g("a13_free_exp", "box_muller")),
                                ("best_loader+free_exp_A13", (r_bfx, lk_bfx)),
                                ("box_muller+narrow_A07", g("a07_narrow", "box_muller")),
                                ("all_free_and_narrow", (r_ball, lk_ball))):
                if r is None:
                    ent[nm] = {"feasible": False}
                    continue
                sa = r["supply_aware_design"]
                req = {tk: float(Fraction(r["call_t"]) / (r["call"] * tl)) for tk, tl in T_LAYERS.items()}
                ent[nm] = {
                    "call_reaction_layers": lab(r["call"], "modelled", "quantum-favourable"),
                    "call_T_layers_rT1": lab(r["call"], "modelled", "quantum-favourable",
                                             "T-depth-1 AND (Jones 2013)"),
                    "call_T_layers_rT2": lab(2 * r["call"], "modelled", "neutral",
                                             "Gidney temporary AND T-depth 2"),
                    "call_T_layers_rT4": lab(4 * r["call"], "modelled", "adverse",
                                             "repo-measured CCX T-depth ratio %s" % ccx_ratio),
                    "forward": r["forward"], "loader_depth": r["loader_depth"],
                    "loader_share": lab(r["loader_share_float"], "modelled", "neutral"),
                    "call_T_count": lab(r["call_t"], "modelled", "quantum-favourable"),
                    "width_qubits": lab(r["width"], "modelled", "neutral"),
                    "required_T_per_s": lab(req, "modelled", "neutral",
                                            "T_call/(call depth x t_layer)"),
                    "loader": lk, "design": {k: r[k] for k in ("loader_params", "prefix",
                                                                "exp", "local_cleanup")},
                    "stages": r["stages"],
                    "supply_aware_design": lab(sa, "modelled", "quantum-favourable",
                                               "min max(call, T_call/(1e12 x 100 ns))"),
                    "comparison": compare(r, case)}
            hc[wk] = ent
            rows.add({"sub": "headline", "case": case, "width": wk, "label": "modelled",
                      "direction": "quantum-favourable",
                      "entries": {nm: (None if "call_reaction_layers" not in e else {
                          "loader": e["loader"], "call": e["call_reaction_layers"]["value"],
                          "loader_share": e["loader_share"]["value"],
                          "call_T": e["call_T_count"]["value"],
                          "width": e["width_qubits"]["value"],
                          "req_T_per_s_100ns": e["required_T_per_s"]["value"]["100ns"],
                          "supply_aware_eff_1e12_100ns":
                              e["supply_aware_design"]["value"]["eff_depth_1e12_100ns"]})
                          for nm, e in ent.items()}})
        headline[case] = hc

    # early-stop signal: max over cells and conventions of k_es (100 ns primary; all t)
    # scopes: "primary" = W0-card primaries (base split, no F20, 100 ns; supply 1e12 or none);
    # "all_conventions" = max over t_layer, e split and F20 credit as well.
    es = {}
    for case in CASES:
        for wk in WIDTHS:
            for nm, e in headline[case][wk].items():
                if "comparison" not in e:
                    continue
                for row in e["comparison"]:
                    for tk, ent in row["by_t_layer"].items():
                        for ck, v in ent.items():
                            for sk in ("unlimited_supply", "supply_1e12"):
                                for scope in ("primary", "all_conventions"):
                                    if scope == "primary" and (tk != "100ns" or ck != "base"):
                                        continue
                                    key = (wk, nm, sk, scope)
                                    val = (v["k_early_stop_" + sk], v["k_10x_" + sk])
                                    if key not in es or val[0] > es[key][0][0]:
                                        es[key] = (val, case, row["eps"], tk, ck)
    early = [{"width": k[0], "floor": k[1], "supply": k[2], "scope": k[3],
              "max_k_early_stop": v[0][0], "max_k_10x": v[0][1],
              "cell": "%s eps=%s" % (v[1], v[2]), "t_layer": v[3], "convention": v[4]}
             for k, v in sorted(es.items())]
    rows.add({"sub": "early_stop_k", "label": "modelled", "direction": "quantum-favourable",
              "rule": "early stop fires iff k_lat > max_k_early_stop (= 30 D_max(k=1)/floor)",
              "entries": early})

    prim = {}
    for case in CASES:
        pc = {}
        for nm in ("box_muller_current_law", "best_loader"):
            e = headline[case]["W1e7"][nm]
            pc[nm] = {
                "loader": e["loader"],
                "call_reaction_layers": e["call_reaction_layers"],
                "loader_share": e["loader_share"], "call_T_count": e["call_T_count"],
                "width_qubits": e["width_qubits"],
                "required_T_per_s_100ns": lab(e["required_T_per_s"]["value"]["100ns"], "modelled",
                                              "neutral", "vs 1e12 supply (W0 card)"),
                "supply_limited_call_1e12_100ns": lab(
                    e["supply_aware_design"]["value"]["eff_depth_1e12_100ns"], "modelled",
                    "quantum-favourable"),
                "k_10x_100ns_base": {str(r["eps"]): {
                    "unlimited_supply": r["by_t_layer"]["100ns"]["base"]["k_10x_unlimited_supply"],
                    "supply_1e12": r["by_t_layer"]["100ns"]["base"]["k_10x_supply_1e12"]}
                    for r in e["comparison"]}}
        prim[case] = pc
    es_prim = {e["floor"] + "|" + e["supply"]: e["max_k_early_stop"] for e in early
               if e["width"] == "W1e7" and e["scope"] == "primary"}
    es_all = {e["floor"] + "|" + e["supply"]: e["max_k_early_stop"] for e in early
              if e["width"] == "W1e7" and e["scope"] == "all_conventions"}
    rows.add({"sub": "primary_summary", "label": "modelled", "direction": "quantum-favourable",
              "per_case": prim, "early_stop_k_primary": es_prim, "early_stop_k_all": es_all})

    result = {
        "primary_summary": {"conventions": "W=1e7, supply 1e12 T/s, t_layer 100 ns, e=0.45 eps, "
                                           "no F20; floors are coarse idealized-algorithm floors",
                            "per_case": prim,
                            "early_stop_k_threshold_primary_conventions": es_prim,
                            "early_stop_k_threshold_all_conventions": es_all,
                            "early_stop_rule": "W0 stops iff k_lat > threshold under every "
                                               "convention, i.e. k_lat > all-conventions value"},
        "label": "WS-floor idealized clean-call reaction-layer floor (plan110 W0, R0 screen)",
        "items": ["A01", "A16", "A09", "A08", "A02", "A07", "A13", "F05", "F20", "A03", "A04"],
        "inputs_sha256": hashes, "python": sys.version.split()[0],
        "isolated_flags": {"I": sys.flags.isolated, "S": sys.flags.no_site,
                           "B": sys.flags.dont_write_bytecode},
        "conventions": {
            "unit": "reaction layer = one layer of parallel temporary-AND gates (A16)",
            "call": "2 x forward (forward + reverse); garbage cleanup overlaps downstream (assumed, QF)",
            "T_count": "2 x 4 x forward ANDs + synthesized-rotation T (A03 only)",
            "t_layer_primary": lab("100ns", "assumed", "quantum-favourable", "W0 card"),
            "supply_primary": lab(10 ** 12, "assumed", "neutral", "W0 card, 1e5 factories"),
            "width_primary": lab(10 ** 7, "assumed", "neutral", "W0 card logical qubits"),
            "ccx_t_depth_ratio_repo": lab(ccx_ratio, "measured", "neutral", "ccx_depth_screen.json"),
            "table_bits_cap": lab(20, "assumed", "adverse",
                                  "excludes exponential-width full lookup (AND-depth ceil(log2 N)+1)"),
            "F20_sigma_credit": lab({k: float(v) for k, v in F20_CREDIT.items()}, "modelled",
                                    "quantum-favourable", "rows_F F20, zero added depth"),
            "precision_bits_base": lab({"word": 72, "fe_precision": 40}, "measured", "neutral",
                                       "A10 source word_width/fraction_bits"),
            "precision_bits_a07": lab({"word": 40, "fe_precision": 24}, "assumed",
                                      "quantum-favourable", "unproved narrow widths"),
            "loader_grid_q": lab(10, "assumed", "quantum-favourable",
                                 "q10 grid passes A05 numeric thresholds per A04/A05 records; law change needs G2"),
        },
        "headline": headline,
        "refinement_trigger": trig, "refined": bool(dag),
        "dag_selfcheck": selfcheck, "dag_reweight": dag,
        "a01_run014_current": {c: {"forward_dependency_t_depth": a01_cases[c]["independent_forward_dependency_t_depth"],
                                   "category_critical_path": {k: v.get("one_critical_path_t_depth_contribution")
                                                              for k, v in a01_cases[c]["category_costs"].items()},
                                   "capped_call_t_depth": a01_cases[c]["resources"]["t_depth"],
                                   "t_count": a01_cases[c]["resources"]["t_count"],
                                   "logical_qubits": a01_cases[c]["resources"]["logical_qubits"]}
                               for c in CASES},
        "early_stop": early,
        "coarse_all": {k: (None if v is None else {kk: vv for kk, vv in v.items() if kk != "stages"} |
                           {"stages": v["stages"]}) for k, v in coarse.items()},
        "runtime_s": time.time() - t0,
    }
    with open(os.path.join(out, "floor.json"), "x", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, indent=1, sort_keys=True, default=str)
    rows.add({"sub": "done", "runtime_s": result["runtime_s"]})
    print(json.dumps({c: {w: {k: (v.get("call_reaction_layers", {}).get("value"),
                                  v.get("loader_share", {}).get("value"),
                                  v.get("call_T_count", {}).get("value"),
                                  v.get("width_qubits", {}).get("value"), v.get("loader"))
                              for k, v in headline[c][w].items()} for w in WIDTHS} for c in CASES},
                     indent=1))
    print("trigger", json.dumps(trig))
    print("selfcheck", json.dumps(selfcheck))
    for c in dag:
        for vk, d in dag[c].items():
            print(c, vk, {k: d[k] for k in ("forward_unlimited", "loader_critical_path_contribution",
                                            "loader_share_marginal", "forward_free_loader",
                                            "forward_free_exp", "forward_free_loader_and_exp",
                                            "call_t")},
                  {lk: s["forward"] for lk, s in d["best_loader_substitution"].items()},
                  d["by_width"])


if __name__ == "__main__":
    main()
