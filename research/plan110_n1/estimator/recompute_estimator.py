"""N1 estimator card: independent recompute (rigour R1) of the WS-k k bracket.

Run from the repo root:
  .context/frontier_t0_env/Scripts/python.exe -I -S -B research/plan110_n1/estimator/recompute_estimator.py [out_dir]

Stdlib only. Different path from research/plan110_w0/ws_k/k_bracket.py:
  * pi enclosure from Euler's arctan(1/2)+arctan(1/3) series (WS-k: Machin);
  * median repetitions by exact dynamic-programming convolution, with the
    per-shot failure 1-8/pi_hi^2 taken exactly (WS-k: closed binomial tail on a
    2^-40-rounded value);
  * least M from the closed-form root of the error quadratic, then checked
    exactly at M and M-1 (WS-k: doubling then bisection);
  * window constant c from power iteration on the even-reduced prolate (sinc)
    matrix (WS-k: tridiagonal DPSS eigenvector + autocorrelation);
  * lanes from the WS-floor design table (width, depth, T count) with the
    magic-state supply shared between lanes (WS-k: source widths, no supply share).
Writes <out_dir>/estimator_recompute.json (exclusive create) and appends one
row per sub-result to <out_dir>/rows.jsonl.
"""

import hashlib
import json
import math
import sys
import time
from fractions import Fraction as F

ROOT = "C:/Users/prith/quantum_option_pricing/"
OUT = sys.argv[1] if len(sys.argv) > 1 else ROOT + "results/plan110_n1/estimator/"
ROWS = OUT + "rows.jsonl"
INPUTS = {
    "sigma_dev": "results/frontier_classical_20261001/sigma_dev/sigma_dev.json",
    "c1_summary": "results/frontier_classical_20261001/c1/c1_summary.json",
    "ws_k_bracket": "results/plan110_w0/ws_k/k_bracket.json",
    "ws_floor": "results/plan110_w0/ws_floor/floor.json",
    "decision_run002": "results/plan110_w0/decision/run002/decision_summary.json",
}
T0 = time.time()


def sha(rel):
    with open(ROOT + rel, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def load(rel):
    with open(ROOT + rel, encoding="utf-8") as f:
        return json.load(f)


def row(d):
    d = dict(ws="n1_estimator", **d)
    with open(ROWS, "a", encoding="utf-8") as f:
        f.write(json.dumps(d) + "\n")


# ------------------------------------------------------------------ pi (Euler)
def atan_inv_enclosure(q, terms):
    """Alternating series for arctan(1/q): consecutive partial sums bracket it."""
    s = F(0)
    for k in range(terms):
        s += F((-1) ** k, (2 * k + 1) * q ** (2 * k + 1))
    nxt = s + F((-1) ** terms, (2 * terms + 1) * q ** (2 * terms + 1))
    return min(s, nxt), max(s, nxt)


a2, a3 = atan_inv_enclosure(2, 140), atan_inv_enclosure(3, 140)
PI_LO, PI_HI = 4 * (a2[0] + a3[0]), 4 * (a2[1] + a3[1])
assert PI_LO < PI_HI and PI_HI - PI_LO < F(1, 10 ** 60)
assert F(314159265358979, 10 ** 14) < PI_LO and PI_HI < F(314159265358980, 10 ** 14)

READOUT = F(1, 2 ** 39)
EPS = [F(1, 10), F(3, 100), F(1, 100), F(1, 1000)]
SPLITS = {"0.45eps": F(9, 20), "eps": F(1)}
CASES = ("B4x12", "B8x52")
SUP_G = F(42680645928225, 2 ** 40)  # E03 audited support (as WS-k)
L1 = F(45202052, 10 ** 9)  # #43 L1 outward display (B4 bridge; borrowed for B8)
SPANS = {"64": F(64), "128/3 (3,47)": F(128, 3), "8192/211 (211,53)": F(8192, 211)}
sig = load(INPUTS["sigma_dev"])["cases"]
c1 = load(INPUTS["c1_summary"])["port_check"]
SIGMA = {c: F(sig[c]["sigma_q"]) for c in CASES}
PRICE = {c: F(c1[c]["price"]) for c in CASES}

res = {"meta": {"script": "research/plan110_n1/estimator/recompute_estimator.py",
                "python": sys.version, "inputs_sha256": {k: sha(v) for k, v in INPUTS.items()},
                "pi_enclosure_euler": [float(PI_LO), float(PI_HI)],
                "labels": "measured (sigma, price from Stage C files), modelled (exact arithmetic or float numerics), "
                          "assumed (mean bound, widths), literature (formulas)"}}


# ------------------------------------------------------------- medians (E08)
def majority_fail(r, p):
    """P[#failures >= (r+1)/2] for r iid shots, by exact DP convolution."""
    dist = [F(1)]
    for _ in range(r):
        nd = [F(0)] * (len(dist) + 1)
        for j, v in enumerate(dist):
            nd[j] += v * (1 - p)
            nd[j + 1] += v * p
        dist = nd
    return sum(dist[(r + 1) // 2:], F(0))


def reps_for(fail, p):
    r = 1
    while majority_fail(r, p) > fail:
        r += 2
    return r


P1 = 1 - 8 / PI_HI ** 2  # per-shot failure upper bound, BHMT Thm 12 k=1
R15 = reps_for(F(3, 1000), P1)
R11 = reps_for(F(1, 100), P1)
assert R15 == 15 and R11 == 11
e08 = []
for fail in (F(3, 1000), F(1, 100)):
    for kb in (1, 3, 4, 5, 6, 8):
        p = P1 if kb == 1 else F(1, 2 * (kb - 1))
        r = reps_for(fail, p)
        e08.append({"failure": float(fail), "BHMT_k": kb, "per_shot_failure": float(p), "reps": r,
                    "cost_factor": kb * r})
best = {str(float(f)): min((x for x in e08 if x["failure"] == float(f)), key=lambda x: x["cost_factor"])
        for f in (F(3, 1000), F(1, 100))}
res["E08_medians"] = {"rows": e08, "best": best,
                      "label": "modelled (exact; BHMT Thm 12 success bounds are literature, verified)"}
row({"item": "E08", "sub": "R1_median_reps", "reps_0.003": R15, "reps_0.01": R11,
     "best_k_times_reps": {k: [v["BHMT_k"], v["reps"]] for k, v in best.items()},
     "agrees_with_WS_k": True, "label": "modelled (exact DP)", "direction": "neutral"})


# --------------------------------------------------------- least-M machinery
def fits(m, S, M, target, readout):
    rhs = target - S * PI_HI ** 2 / F(M) ** 2 - readout
    if rhs <= 0:
        return False
    return 4 * PI_HI ** 2 * m * (S - m) <= F(M) ** 2 * rhs ** 2


def least_M(m, S, target, readout, dyadic):
    """Closed-form root of S pi^2 x^2 + 2 pi sqrt(m(S-m)) x - (target-readout) = 0, x = 1/M."""
    m = S / 2 if m is None else m
    a = float(S) * math.pi ** 2
    b = 2 * math.pi * math.sqrt(float(m * (S - m)))
    c = float(target - readout)
    x = (-b + math.sqrt(b * b + 4 * a * c)) / (2 * a)
    Mr = 1 / x
    if dyadic:
        M = 1 << max(0, math.ceil(math.log2(Mr)) - 1)
        while not fits(m, S, M, target, readout):
            M *= 2
        assert M == 1 or not fits(m, S, M // 2, target, readout)
        return M
    M = max(1, math.floor(Mr) - 3)
    while not fits(m, S, M, target, readout):
        M += 1
    assert M == 1 or not fits(m, S, M - 1, target, readout)
    return M


def e07_fits(M, error, span=64):
    return span * (PI_HI / M + PI_HI ** 2 / F(M) ** 2) <= error


def e07_M(error):
    x = (-math.pi + math.sqrt(math.pi ** 2 + 4 * math.pi ** 2 * float(error) / 64)) / (2 * math.pi ** 2)
    M = 1 << max(0, math.ceil(math.log2(1 / x)) - 1)
    while not e07_fits(M, error):
        M *= 2
    assert not e07_fits(M // 2, error)
    return M


def calls_canonical(M):
    return R15 * (M - 1)


def calls_direction_select(M):
    """Exponents j - c via plain control on bit 0 and direction-select Q^(+-2^(b-1)) on bits b>=1:
    1 + sum_{b=1}^{n-1} 2^(b-1) = 2^(n-1) calls per shot for a 2^n-point register (n>=1)."""
    n = (M - 1).bit_length()
    return R15 * (1 << (n - 1)) if M > 1 else 0


# ------------------------------------------------------ k_eff today (E07/E24)
part1 = []
for case in CASES:
    s = SIGMA[case]
    for eps in EPS:
        for sl, sp in SPLITS.items():
            e = sp * eps
            M = e07_M(e)
            assert M == least_M(None, F(64), e, READOUT, True)
            calls = calls_canonical(M)
            cds = calls_direction_select(M)
            part1.append({"case": case, "eps": float(eps), "split": sl, "M": M, "calls": calls,
                          "k_eff": float(calls * e / s), "calls_direction_select": cds,
                          "k_eff_direction_select": float(cds * e / s),
                          "label": "modelled (exact; sigma measured)", "direction": "neutral"})
assert all(r["calls"] == 983025 for r in part1 if r["eps"] == 0.01 and r["split"] == "0.45eps")
p1p = [r for r in part1 if r["split"] == "0.45eps"]
res["part1_k_eff_today"] = part1
row({"item": "C11/E07", "sub": "R1_k_eff_today", "k_eff_range_0.45eps": [min(r["k_eff"] for r in p1p), max(r["k_eff"] for r in p1p)],
     "per_cell": {f"{r['case']}@{r['eps']}": [r["M"], r["calls"], round(r["k_eff"], 2)] for r in p1p},
     "saved_983025_reproduced": True, "label": "modelled (exact; sigma measured)", "direction": "neutral"})
row({"item": "C11", "sub": "N1_new_direction_select_credit_on_certified_schedule",
     "k_eff_range_0.45eps": [min(r["k_eff_direction_select"] for r in p1p), max(r["k_eff_direction_select"] for r in p1p)],
     "calls_at_eps0.01": [r["calls_direction_select"] for r in p1p if r["eps"] == 0.01][0],
     "argument": "shifting all register exponents j -> j - c multiplies each Q eigen-branch by a global phase, so the BHMT "
                 "output distribution (hence Thm 12) is unchanged; plain control on bit 0 plus direction-select Q^(+-2^(b-1)) "
                 "on bits b>=1 realise j - c with M/2 calls instead of M-1",
     "conditional_on": "cost certificate: a direction-select iterate (controlled S_chi before or after A S0 A^dagger) costs no more "
                       "than one controlled Grover iterate in the program cost model; schedule not re-emitted",
     "label": "modelled (exact distributional identity + assumed equal call cost)", "direction": "quantum-favourable"})

# ------------------------------------------------ explicit-constant k_lo (C11)
CREDITS = {
    "span": "U2 support-tight wrapper (E03 audited sup g <= 38.818; wrapper not emitted; 2^-39 readout placeholder for new span)",
    "mean": "U1 mean certificate m <= price + L1 (price is an uncertified RQMC orientation value; for B8x52 the #43 L1 is borrowed from B4x12, B8 L1 bridge not established)",
    "nondyadic": "non-power-of-two QFT over Z_M (BHMT Thm 12 covers any M: verified) with an exact or error-budgeted implementation",
    "dirsel": "direction-select call-cost certificate (N1 argument, not in W0)",
}
part2 = []
for case in CASES:
    s = SIGMA[case]
    for eps in EPS:
        for sl, sp in SPLITS.items():
            e = sp * eps
            for spl, S in SPANS.items():
                for ml, m in (("none", None), ("price+L1", PRICE[case] + L1)):
                    for dy in (True, False):
                        M = least_M(m, S, e, READOUT, dy)
                        for ds in (False, True):
                            if ds and not dy:
                                continue  # direction-select on a non-dyadic register costs 2^(n-1) = dyadic value
                            calls = calls_direction_select(M) if ds else calls_canonical(M)
                            need = ([] if spl == "64" else ["span"]) + ([] if m is None else ["mean"]) + \
                                   ([] if dy else ["nondyadic"]) + (["dirsel"] if ds else [])
                            part2.append({"case": case, "eps": float(eps), "split": sl, "span": spl, "mean": ml,
                                          "M_rule": "dyadic" if dy else "non-dyadic", "direction_select": ds,
                                          "M": M, "calls": calls, "k": float(calls * e / s), "credits_needed": need,
                                          "label": "modelled (exact)" + ("; mean assumed" if m is not None else ""),
                                          "direction": "quantum-favourable"})
res["part2_explicit_k"] = part2
res["part2_credit_definitions"] = CREDITS


def kbest(case, eps, sl, allowed):
    c = [r for r in part2 if r["case"] == case and r["eps"] == float(eps) and r["split"] == sl
         and set(r["credits_needed"]) <= set(allowed)]
    return min(c, key=lambda r: r["k"])


summ = []
for case in CASES:
    for eps in EPS:
        sl = "0.45eps"
        rec = {"case": case, "eps": float(eps)}
        for name, allowed in (("certified_today", []), ("span_only", ["span"]),
                              ("span+nondyadic (no mean cert)", ["span", "nondyadic"]),
                              ("span+mean dyadic", ["span", "mean"]),
                              ("W0 explicit best: span+mean+nondyadic", ["span", "mean", "nondyadic"]),
                              ("dirsel only", ["dirsel"]),
                              ("N1 best: all credits incl. dirsel", ["span", "mean", "nondyadic", "dirsel"])):
            b = kbest(case, eps, sl, allowed)
            rec[name] = {"k": b["k"], "M": b["M"], "calls": b["calls"], "span": b["span"], "mean": b["mean"],
                         "M_rule": b["M_rule"], "direction_select": b["direction_select"]}
        summ.append(rec)
res["part2_summary"] = summ
w0best = [r["W0 explicit best: span+mean+nondyadic"]["k"] for r in summ]
n1best = [r["N1 best: all credits incl. dirsel"]["k"] for r in summ]
nomean = [r["span+nondyadic (no mean cert)"]["k"] for r in summ]
dymean = [r["span+mean dyadic"]["k"] for r in summ]
row({"item": "C11/E03", "sub": "R1_explicit_best_k", "W0_explicit_best_range": [min(w0best), max(w0best)],
     "no_mean_certificate_range": [min(nomean), max(nomean)], "dyadic_with_mean_range": [min(dymean), max(dymean)],
     "per_cell_W0_best": {f"{r['case']}@{r['eps']}": round(r["W0 explicit best: span+mean+nondyadic"]["k"], 2) for r in summ},
     "credits": ["span", "mean", "nondyadic"], "label": "modelled (exact; mean assumed)", "direction": "quantum-favourable"})
row({"item": "C11", "sub": "N1_best_with_direction_select", "range": [min(n1best), max(n1best)],
     "per_cell": {f"{r['case']}@{r['eps']}": [round(r["N1 best: all credits incl. dirsel"]["k"], 2),
                                              r["N1 best: all credits incl. dirsel"]["M_rule"]] for r in summ},
     "label": "modelled (exact; mean assumed; direction-select cost assumed)", "direction": "quantum-favourable"})

# ----------------------------------------------- E01 counting lower bound
part3 = []
for case in CASES:
    s = SIGMA[case]
    for eps in EPS:
        for sl, sp in SPLITS.items():
            e = sp * eps
            for cl, R in (("support [0, 38.818]", SUP_G), ("mean-bounded [0, price+L1] (assumed)", PRICE[case] + L1)):
                x = R / (2 * e)
                K = -(-x.numerator // x.denominator)  # ceil; spacing R/(K-1) > 2e
                if K > 1:
                    assert R / (K - 1) > 2 * e
                for delta in (F(1, 100), F(3, 1000)):
                    nq = ((1 - delta) * K - 1) / 2  # Q-access only: dim <= 2N+1
                    nq1 = ((1 - delta) * K - 2) / 2  # plus one copy of A|0>: odd exponents, dim <= 2N+2
                    na = ((1 - delta) * K - 1) / 4  # A/A^dagger access, 2 A-calls per Q-equivalent
                    part3.append({"case": case, "eps": float(eps), "split": sl, "class": cl, "delta": float(delta),
                                  "K": K, "k_LB_Q_access": float(nq * e / s), "k_LB_Q_plus_one_A": float(nq1 * e / s),
                                  "k_LB_A_access": float(na * e / s),
                                  "label": "modelled (rigorous analytic bound; proof in card)",
                                  "direction": "quantum-favourable (a floor no black-box estimator can beat)"})
res["part3_counting_lower_bound"] = part3
lbp = [r for r in part3 if r["split"] == "0.45eps" and r["delta"] == 0.01 and r["class"].startswith("support")]
row({"item": "E01", "sub": "R1_counting_lower_bound",
     "k_LB_Q_access_support_delta0.01": {f"{r['case']}@{r['eps']}": round(r["k_LB_Q_access"], 4) for r in lbp},
     "k_LB_Q_plus_one_A": {f"{r['case']}@{r['eps']}": round(r["k_LB_Q_plus_one_A"], 4) for r in lbp},
     "k_LB_A_access": {f"{r['case']}@{r['eps']}": round(r["k_LB_A_access"], 4) for r in lbp},
     "min_any_cell_A_access": min(r["k_LB_A_access"] for r in part3),
     "hard_family": "A_theta = R_y(2 theta) on one payoff qubit, payoff R*Bernoulli(sin^2 theta); Q_theta and A_theta have "
                    "theta-independent eigenvectors, so Mande-de Wolf Claim 5.3 degree argument applies to this family",
     "label": "modelled (rigorous analytic)", "direction": "quantum-favourable"})


# --------------------------------------------- window constant c (F4/E08)
def top_even_eig(N, Delta, v0=None):
    """Largest eigenvalue of the (2N+1)x(2N+1) prolate matrix A_mn = sin((m-n)Delta)/(pi(m-n)), restricted to even
    vectors (the top eigenvector is even), via power iteration on the (N+1)-dim reduced operator."""
    A = [Delta / math.pi] + [math.sin(d * Delta) / (math.pi * d) for d in range(1, 2 * N + 1)]
    B = [[A[m] if n == 0 else A[abs(m - n)] + A[m + n] for n in range(N + 1)] for m in range(N + 1)]
    v = v0[:] if v0 else [math.cos(0.5 * math.pi * n / (N + 1)) for n in range(N + 1)]

    def ip(u, w):
        return u[0] * w[0] + 2 * sum(u[i] * w[i] for i in range(1, N + 1))

    lam_old = 0.0
    for it in range(2000):
        w = [sum(Bm[n] * v[n] for n in range(N + 1)) for Bm in B]
        lam = ip(v, w) / ip(v, v)
        nrm = math.sqrt(ip(w, w))
        v = [x / nrm for x in w]
        if it > 5 and abs(lam - lam_old) < 1e-15:
            break
        lam_old = lam
    return lam, v


def c_window(N, target):
    lo, hi = 1.0 / N, 12.0 / N
    v = None
    for _ in range(46):
        mid = (lo + hi) / 2
        lam, v = top_even_eig(N, mid, v)
        if 1 - lam > target:
            lo = mid
        else:
            hi = mid
    return N * hi


win = []
for target in (0.003, 0.01):
    for N in (50, 100, 200):
        win.append({"target_failure": target, "N": N, "c_DPSS_power_iteration": c_window(N, target),
                    "label": "modelled (float numerics)"})
wsk = load(INPUTS["ws_k_bracket"])["part3_window_numerics"]["rows"]
for r in win:
    ref = [x["c"] for x in wsk if x["window"].startswith("DPSS") and x["target_failure"] == r["target_failure"]
           and x["N"] == r["N"]]
    r["WS_k_c_same_N"] = ref[0] if ref else None
    if ref:
        assert abs(ref[0] - r["c_DPSS_power_iteration"]) < 2e-3, (r, ref)
C_WIN = {t: [x["c"] for x in wsk if x["window"].startswith("DPSS") and x["target_failure"] == t and x["N"] == 400][0]
         for t in (0.003, 0.01)}  # WS-k N=400 value, confirmed at N<=200 by this path; c rises slowly with N
res["part4_window_c"] = {"rows": win, "c_used_N400_from_WS_k": C_WIN,
                         "convention": "N calls realise exponents -N..N (direction-select); continuous readout; success "
                                       "= concentration of |W|^2 in |x| <= Delta, phase-independent"}
row({"item": "F4/E08", "sub": "R1_window_constant_c", "rows": [[r["target_failure"], r["N"], round(r["c_DPSS_power_iteration"], 5),
                                                                r["WS_k_c_same_N"]] for r in win],
     "agrees_with_WS_k_within": 2e-3, "label": "modelled (float numerics, different algorithm)", "direction": "quantum-favourable"})


def delta_phi(m, S, e):
    m = S / 2 if m is None else m
    A = math.sqrt(float(m * (S - m)))
    Sf, ef = float(S), float(e - READOUT)
    return (-A + math.sqrt(A * A + Sf * ef)) / (Sf / 2)


part5 = []
for case in CASES:
    s = float(SIGMA[case])
    for eps in EPS:
        e = F(9, 20) * eps
        for spl, S, ml, m in (("64", F(64), "none", None), ("8192/211", F(8192, 211), "price+L1", PRICE[case] + L1)):
            D = delta_phi(m, S, e)
            for t in (0.003, 0.01):
                part5.append({"case": case, "eps": float(eps), "span": spl, "mean": ml, "fail": t,
                              "N_calls": C_WIN[t] / D, "k_window": C_WIN[t] / D * float(e) / s,
                              "label": "modelled (no explicit constant in any primary source)",
                              "direction": "quantum-favourable"})
res["part5_window_k"] = part5
kw = lambda span, t: [r["k_window"] for r in part5 if r["span"] == span and r["fail"] == t]
row({"item": "F4/C11", "sub": "R1_window_k", "span64_nomean_fail0.003": [min(kw("64", 0.003)), max(kw("64", 0.003))],
     "span38.82_mean_fail0.003": [min(kw("8192/211", 0.003)), max(kw("8192/211", 0.003))],
     "span38.82_mean_fail0.01 (DP1 row)": [min(kw("8192/211", 0.01)), max(kw("8192/211", 0.01))],
     "label": "modelled", "direction": "quantum-favourable"})


# Patel Thm 2 made worst-case by a random known register phase offset (argument here, not in the source)
def patel_calls(Delta, delta):
    mb = math.ceil(math.log2(math.ceil(175 * (math.log(10 / delta) + 1) ** 2) + 1)) + 1
    dc = Delta / (2 * math.pi)
    tau = 1
    while dc < 1 / 2 ** (tau + 1):
        tau += 1
    return 2 ** (tau + mb) - 1, mb


pat = []
for case in CASES:
    s = float(SIGMA[case])
    for eps in (F(1, 100), F(1, 1000)):
        e = F(9, 20) * eps
        D = delta_phi(None, F(64), e)
        calls, mb = patel_calls(D, 0.003)
        pat.append({"case": case, "eps": float(eps), "extra_ancillas": mb, "calls": calls, "k": calls * float(e) / s})
res["part5_patel_thm2_randomised_offset"] = {"rows": pat, "note": (
    "Patel et al. Thm 2 is explicit but average-case over the phase. Applying a uniformly random known phase "
    "offset to the register (no oracle calls) makes the success probability at every phase equal to the "
    "average, so Thm 2 becomes an explicit worst-case guarantee; its constant is ~1e5 above the window value. "
    "Argument here (modelled), not stated in the source.")}
row({"item": "F4/E08", "sub": "patel_thm2_worst_case_via_random_offset", "rows": pat,
     "label": "modelled (literature theorem + offset argument)", "direction": "adverse"})

# ---------------------------------------------------------- lanes (E20)
floor = load(INPUTS["ws_floor"])["coarse_all"]
RATE = {"supply_1e12": 1e12, "unlimited": None}
TL = 1e-7
W = 10 ** 7
lanes = []
for case in CASES:
    designs = []
    for wk in ("W1e6", "W1e7"):
        v = floor[f"{case}|{wk}|base|box_muller"]
        designs.append((f"{wk} depth-optimal", v["call"], v["call_t"], v["width"]))
        sa = v["supply_aware_design"]
        designs.append((f"{wk} supply-aware", sa["call"], sa["call_t"], sa["width"]))
    for sk, R in RATE.items():
        def eff(dep, t, L):
            return dep if R is None else max(dep, L * t / (R * TL))
        single = min(eff(d, t, 1) for _, d, t, w in designs if w <= W)
        best_lat, best_cfg = 15 * single, ("1 lane", 1)
        for name, d, t, w in designs:
            for L in range(1, min(15, W // w) + 1):
                lat = -(-15 // L) * eff(d, t, L)
                if lat < best_lat - 1e-9:
                    best_lat, best_cfg = lat, (name, L)
        tmin = min(t for _, d, t, w in designs if w <= W)
        lanes.append({"case": case, "supply": sk, "single_lane_eff_depth": single,
                      "best_15_shot_latency_layers": best_lat, "best_config": best_cfg,
                      "lane_credit": 15 * single / best_lat,
                      "supply_bound_credit_cap": None if R is None else single / (tmin / (R * TL)),
                      "label": "modelled (WS-floor designs; widths modelled)", "direction": "quantum-favourable"})
srcw = {"B4x12": 550141, "B8x52": 4460479}
res["part6_lanes_W1e7"] = {"rows": lanes,
                           "source_width_lanes_WS_k": {c: W // srcw[c] for c in CASES},
                           "floor_design_width_primary": {c: floor[f"{c}|W1e7|base|box_muller"]["width"] for c in CASES},
                           "note": "WS-k k_lat (18 / 2 lanes) uses source widths with source depth; the decision table's "
                                   "k_10x uses the floor depth at W=1e7, where the primary design is 5.28M / 10M wide."}
row({"item": "E20", "sub": "R1_lanes_at_W1e7", "rows": [[r["case"], r["supply"], round(r["lane_credit"], 3), r["best_config"]] for r in lanes],
     "label": "modelled", "direction": "quantum-favourable"})

# --------------------------------------------- M = k / k_10x (primary)
dec = load(INPUTS["decision_run002"])
k10 = {}
for r in dec["primary_rows"]:
    k10[(r["case"], r["eps"])] = r["k_10x"]
Mtab = []
for case in CASES:
    for eps in (0.01, 0.001):
        rec = next(x for x in summ if x["case"] == case and x["eps"] == eps)
        kt = k10[(case, eps)]
        lc = next(x["lane_credit"] for x in lanes if x["case"] == case and x["supply"] == "supply_1e12")
        wk = [r for r in part5 if r["case"] == case and r["eps"] == eps and r["span"] == "8192/211"]
        Mtab.append({"case": case, "eps": eps, "k_10x": kt,
                     "M_certified_today": rec["certified_today"]["k"] / kt,
                     "M_certified_today_dirsel": rec["dirsel only"]["k"] / kt,
                     "M_W0_explicit_best": rec["W0 explicit best: span+mean+nondyadic"]["k"] / kt,
                     "M_N1_explicit_best_dirsel": rec["N1 best: all credits incl. dirsel"]["k"] / kt,
                     "M_window_fail0.003": [r["k_window"] for r in wk if r["fail"] == 0.003][0] / kt,
                     "M_window_fail0.01": [r["k_window"] for r in wk if r["fail"] == 0.01][0] / kt,
                     "lane_credit_supply_1e12": lc,
                     "label": "modelled (k_10x from WS-floor, not recomputed here)", "direction": "neutral"})
res["part7_M_primary"] = Mtab
row({"item": "C11", "sub": "M_primary_recomputed", "rows": [[m["case"], m["eps"], round(m["M_certified_today"], 1),
     round(m["M_certified_today_dirsel"], 1), round(m["M_W0_explicit_best"], 1), round(m["M_N1_explicit_best_dirsel"], 1),
     round(m["M_window_fail0.003"], 2), round(m["M_window_fail0.01"], 2)] for m in Mtab],
     "columns": ["case", "eps", "certified", "certified+dirsel", "W0 explicit best", "N1 best incl dirsel", "window 0.003", "window 0.01"],
     "label": "modelled", "direction": "neutral"})

res["meta"]["runtime_s"] = time.time() - T0
with open(OUT + "estimator_recompute.json", "x", encoding="utf-8") as f:
    json.dump(res, f, indent=1)
print(json.dumps({"k_today": [min(r["k_eff"] for r in p1p), max(r["k_eff"] for r in p1p)],
                  "W0_best": [min(w0best), max(w0best)], "N1_best": [min(n1best), max(n1best)],
                  "nomean": [min(nomean), max(nomean)], "dymean": [min(dymean), max(dymean)],
                  "M": Mtab, "lanes": lanes, "win": win, "runtime": res["meta"]["runtime_s"]}, indent=1))
