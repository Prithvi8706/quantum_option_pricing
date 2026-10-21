"""WS-k k bracket (plan110 W0, rigour R0).

Run: .context/frontier_t0_env/Scripts/python.exe -I -S -B research/plan110_w0/ws_k/k_bracket.py
Stdlib only.  Schedule arithmetic uses fractions (exact); window-function
numerics and literature formulas use floats and are labelled 'modelled'.
Writes results/plan110_w0/ws_k/k_bracket.json (exclusive create) and appends
one row per sub-result to results/plan110_w0/ws_k/rows.jsonl.

k convention: k = (controlled Grover calls) / (sigma/e), sigma = sigma_q from
sigma_dev.json, e = statistical dollar share (0.45 eps primary, eps column).
"""

import hashlib
import json
import math
import sys
from fractions import Fraction as F
from math import comb

ROOT = "C:/Users/prith/quantum_option_pricing/"
OUT = sys.argv[1] if len(sys.argv) > 1 else ROOT + "results/plan110_w0/ws_k/"
ROWS = OUT + "rows.jsonl"
INPUTS = {
    "sigma_dev": "results/frontier_classical_20261001/sigma_dev/sigma_dev.json",
    "c1_summary": "results/frontier_classical_20261001/c1/c1_summary.json",
    "E07_schedule": "results/limitation_program_20261001/E07_schedule_run001/schedule.json",
    "E07_code": "results/limitation_program_20261001/E07_schedule_run001/executed_code/financial_bounded_schedule.py",
    "E04_controller_summary": "results/limitation_program_20261001/E04_controller_run001/summary.json",
    "E04_theorem_screen": "results/limitation_program_20261001/E04_theorem_run001/screen.json",
    "E03_support_summary": "results/limitation_program_20261001/E03_support_run001/summary.json",
    "STATUS": "docs/limitation_program_20261001/STATUS.md",
    "U2": "docs/parallel_E11_unblock_20261010/U2_MEAN_AWARE_SCHEDULE.md",
    "CRITIQUE_wrongly_killed": "docs/program_plan_20261010/supporting/CRITIQUE_wrongly_killed.md",
    "W0_CARD": "research/plan110_w0/W0_CARD.md",
}


def sha(rel):
    with open(ROOT + rel, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def load(rel):
    with open(ROOT + rel, encoding="utf-8") as f:
        return json.load(f)


def row(d):
    d = dict(ws="ws_k", **d)
    with open(ROWS, "a", encoding="utf-8") as f:
        f.write(json.dumps(d) + "\n")


def fr(x):
    x = F(x)
    return {"exact": [x.numerator, x.denominator], "approx": float(x)}


# ---------------------------------------------------------------- pi (E07 copy)
def atan_interval(inverse, terms):
    total = sum((F((-1) ** k, (2 * k + 1) * inverse ** (2 * k + 1)) for k in range(terms)), F(0))
    following = total + F((-1) ** terms, (2 * terms + 1) * inverse ** (2 * terms + 1))
    return min(total, following), max(total, following)


def pi_interval(terms=80):
    a, b = atan_interval(5, terms), atan_interval(239, terms)
    return 16 * a[0] - 4 * b[1], 16 * a[1] - 4 * b[0]


PI_LO, PI_HI = pi_interval()
READOUT = F(1, 2 ** 39)


def binomial_majority_tail(r, p):
    return sum((comb(r, k) * p ** k * (1 - p) ** (r - k) for k in range(r // 2 + 1, r + 1)), F(0))


def elementary_failure():
    el = 1 - 8 / PI_HI ** 2
    den = 1 << 40
    return F((el.numerator * den + el.denominator - 1) // el.denominator, den)


def median_reps(failure, p=None):
    p = elementary_failure() if p is None else p
    r = 1
    while binomial_majority_tail(r, p) > failure:
        r += 2
    return r


def e07_M(error, span=64):
    """Exact E07 rule: least power of two with span*(pi/M+pi^2/M^2) <= error."""
    M = 1
    while span * (PI_HI / M + PI_HI ** 2 / M ** 2) > error:
        M *= 2
    assert not (M > 1 and span * (PI_LO / (M // 2) + PI_LO ** 2 / (M // 2) ** 2) <= error)
    return M


def fits(m, S, M, target, readout=READOUT):
    """e(m,M)=2 pi sqrt(m(S-m))/M + S pi^2/M^2 + readout <= target, exact (pi_hi)."""
    rhs = target - S * PI_HI ** 2 / F(M) ** 2 - readout
    if rhs <= 0:
        return False
    return 4 * PI_HI ** 2 * m * (S - m) <= F(M) ** 2 * rhs ** 2


def min_M(m, S, target, dyadic=True):
    m = S / 2 if m is None else m
    assert 0 <= m <= S / 2
    M = 1
    while not fits(m, S, M, target):
        M *= 2
    if dyadic:
        return M
    lo, hi = M // 2, M  # lo fails (or 0), hi fits
    if lo < 1:
        return hi
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if fits(m, S, mid, target):
            hi = mid
        else:
            lo = mid
    return hi


# ---------------------------------------------------------------- inputs
sig = load(INPUTS["sigma_dev"])["cases"]
c1 = load(INPUTS["c1_summary"])["port_check"]
SIGMA = {c: F(sig[c]["sigma_q"]) for c in ("B4x12", "B8x52")}
PRICE = {c: F(c1[c]["price"]) for c in ("B4x12", "B8x52")}
L1_DISPLAY = F(45202052, 10 ** 9)  # #43 outward display, B4x12 bridge (U2 sec 2.4)
SUP_G = F(42680645928225, 2 ** 40)  # E03 audited support (U2 sec 2.2)
WIDTH = {"B4x12": 550141, "B8x52": 4460479}  # STATUS header, logical qubits
DEPTH = {"B4x12": 555774, "B8x52": 663704}  # STATUS T-depth (A10 source)
TCOUNT = {"B4x12": 520720662, "B8x52": 4267435214}
EPS = [F(1, 10), F(3, 100), F(1, 100), F(1, 1000)]
SPLITS = {"0.45eps": F(9, 20), "eps": F(1)}
FAIL_EST = F(3, 1000)  # E07 estimator failure allowance
FAIL_ALL = F(1, 100)  # whole 99% budget (quantum-favourable sensitivity)
CASES = ("B4x12", "B8x52")
SPANS = {"64": F(64), "128/3 (3,47)": F(128, 3), "8192/211 (211,53)": F(8192, 211)}


def means(case):
    return {
        "none (worst case m=S/2)": None,
        "price+L1 (uncertified orientation; assumed)": PRICE[case] + L1_DISPLAY,
        "barrier-free ~6 (assumed)": F(6),
    }


R15 = median_reps(FAIL_EST)
R_ALL = median_reps(FAIL_ALL)

result = {
    "meta": {
        "script": "research/plan110_w0/ws_k/k_bracket.py",
        "inputs_sha256": {k: sha(v) for k, v in INPUTS.items()},
        "k_convention": "k = controlled Grover calls / (sigma_q/e); e = split*eps",
        "pi_enclosure": [fr(PI_LO)["approx"], fr(PI_HI)["approx"]],
        "median_reps_at_0.003": R15,
        "median_reps_at_0.01": R_ALL,
    }
}
assert R15 == 15

# ------------------------------------------------------------ 1. k_eff today
part1 = []
for case in CASES:
    s = SIGMA[case]
    for eps in EPS:
        for sl, sp in SPLITS.items():
            e = sp * eps
            M = e07_M(e)
            M_task = min_M(None, F(64), e)  # task formula incl. 2^-39 readout
            calls = R15 * (M - 1)
            k = calls * e / s
            kc = (M - 1) * e / s
            rec = {
                "case": case, "eps": float(eps), "split": sl, "e": fr(e), "M": M,
                "M_task_formula_with_readout": M_task, "calls": calls,
                "sigma_over_e": float(s / e), "k_eff": fr(k), "k_chain_one_shot": fr(kc),
                "label": "modelled (exact schedule arithmetic; sigma measured)",
                "saved_schedule_reproduced": (calls == 983025) if (eps == F(1, 100) and sp == F(9, 20)) else None,
                "direction": "neutral",
            }
            assert M == M_task
            part1.append(rec)
            if sl == "0.45eps":
                row({"item": "E24/E07", "sub": "k_eff", "case": case, "eps": float(eps), "M": M,
                     "calls": calls, "k_eff": float(k), "k_chain": float(kc),
                     "label": "modelled (exact; sigma measured)", "direction": "neutral"})
saved = [r for r in part1 if r["saved_schedule_reproduced"]]
assert len(saved) == 2  # both cases share 983,025 at eps=0.01
result["part1_k_eff_today"] = part1

# ---------------------------------------------- 2. access-model lower bounds
def counting_lb(R, e, delta):
    """K hypotheses with means spaced > 2e in [0,R]; final state lies in span of
    2D+1 fixed vectors (D = Laurent degree); success >= 1-delta each => (1-delta)K <= 2D+1."""
    x = R / (2 * e)
    K = math.ceil(x)
    K = max(K, 1)
    D = ((1 - delta) * K - 1) / 2  # minimal degree
    return K, D


part2 = {"statement": (
    "Rigorous counting bound (analytic, this script): any algorithm using N controlled-Q / Q^-1 calls "
    "(Q = Grover iterate) produces a final state sum_{j=-N..N} e^{2 i j theta}|v_j> (Mande-de Wolf "
    "Claim 5.3 degree argument), i.e. inside a (2N+1)-dim subspace; discriminating K two-point laws "
    "on [0,S] with means spaced >2e, each with success >= 1-delta, forces (1-delta)K <= 2N+1. "
    "With raw A / A^-1 access (2 queries per Q) the subspace is (2T+1)-dim in e^{i theta}, so "
    "N_equiv = T/2 >= ((1-delta)K-1)/4."),
    "rows": []}
for case in CASES:
    s = SIGMA[case]
    for eps in EPS:
        for sl, sp in SPLITS.items():
            e = sp * eps
            for rl, R in (("support class [0, sup g=38.818]", SUP_G),
                          ("mean-bounded class [0, price+L1] (assumed m)", PRICE[case] + L1_DISPLAY)):
                for delta in (FAIL_ALL, FAIL_EST):
                    K, D = counting_lb(R, e, delta)
                    kq = D * e / s
                    ka = (D / 2) * e / s
                    part2["rows"].append({
                        "case": case, "eps": float(eps), "split": sl, "class": rl, "delta": float(delta),
                        "K": K, "N_Q_min": float(D), "k_LB_Q_access": float(kq),
                        "k_LB_A_access": float(ka),
                        "label": "modelled (rigorous analytic lower bound; access model)",
                        "direction": "quantum-favourable (a lower bound)"})
lb_min = min(r["k_LB_A_access"] for r in part2["rows"])
lb_sup = [r for r in part2["rows"] if r["class"].startswith("support") and r["delta"] == 0.01 and r["split"] == "0.45eps"]
part2["min_k_LB_any_cell"] = lb_min
part2["E01_threshold_k_star_0.06_exceeded_everywhere"] = lb_min > 0.06
part2["literature"] = [
    {"source": "Mande & de Wolf, arXiv:2305.04908v3 / Quantum 10, 2140 (2026), Thm 1.3 + Claim 5.2 proof",
     "bound": "t >= ln(1/(2 eps_fail)) / (48 delta_phase) uses of controlled-U, U^-1 (constant from 1/(2eps) <= exp(48 t delta))",
     "label": "literature", "note": "explicit but weak; phase-estimation access; Omega((1/delta) log(1/eps)) tight"},
    {"source": "Nayak & Wu STOC'99 (quant-ph/9804066), cited in Mande-de Wolf p.4",
     "bound": "Omega(1/eps) at constant success for approximate counting", "label": "literature",
     "note": "no explicit constant read"},
    {"source": "Kothari & O'Donnell arXiv:2208.07544 (abstract)",
     "bound": "O(sigma/eps) runs optimal in n; variance access", "label": "literature",
     "note": "no explicit constant"},
]
row({"item": "E01", "sub": "counting_lower_bound", "min_k_LB_A_access_any_cell": lb_min,
     "support_class_k_LB_Q_access_0.45eps_delta0.01": {f"{r['case']}@{r['eps']}": round(r["k_LB_Q_access"], 4) for r in lb_sup},
     "label": "modelled (rigorous analytic)", "direction": "quantum-favourable"})
result["part2_lower_bounds"] = part2

# ------------------------------------------------------- 4. joint credit table
part4 = []
for case in CASES:
    s = SIGMA[case]
    for eps in EPS:
        for sl, sp in SPLITS.items():
            e = sp * eps
            base = R15 * (min_M(None, F(64), e) - 1)
            for spl, S in SPANS.items():
                for ml, m in means(case).items():
                    for dy in (True, False):
                        M = min_M(m, S, e, dyadic=dy)
                        calls = R15 * (M - 1)
                        part4.append({
                            "case": case, "eps": float(eps), "split": sl, "span": spl, "mean_bound": ml,
                            "M_rule": "dyadic" if dy else "non-dyadic (any integer M)", "M": M, "calls": calls,
                            "credit_vs_span64_worstcase_dyadic": float(F(base, calls)),
                            "k": float(calls * e / s),
                            "label": ("modelled (exact formula; mean bound " +
                                      ("assumed" if m is not None else "not needed") +
                                      "; span " + ("saved" if spl == "64" else "new-wrapper design, readout 2^-39 placeholder") + ")"),
                            "direction": "quantum-favourable" if calls < base else "neutral"})
result["part4_joint_credit"] = part4


def best(case, eps, sl, mean_ok, dy_ok):
    c = [r for r in part4 if r["case"] == case and r["eps"] == float(eps) and r["split"] == sl
         and (mean_ok or r["mean_bound"].startswith("none"))
         and (dy_ok or r["M_rule"] == "dyadic")
         and not r["mean_bound"].startswith("barrier")]
    return max(c, key=lambda r: r["credit_vs_span64_worstcase_dyadic"])


credit_summary = []
for case in CASES:
    for eps in EPS:
        for sl in SPLITS:
            b1 = best(case, eps, sl, False, False)
            b2 = best(case, eps, sl, True, False)
            b3 = best(case, eps, sl, True, True)
            credit_summary.append({
                "case": case, "eps": float(eps), "split": sl,
                "support_tight_only_dyadic": [b1["span"], b1["credit_vs_span64_worstcase_dyadic"]],
                "plus_price_L1_mean_dyadic": [b2["span"], b2["credit_vs_span64_worstcase_dyadic"]],
                "plus_nondyadic_M": [b3["span"], b3["mean_bound"], round(b3["credit_vs_span64_worstcase_dyadic"], 4)],
                "k_after_best_dyadic": b2["k"], "k_after_best_nondyadic": b3["k"]})
            if sl == "0.45eps":
                row({"item": "E03/U2", "sub": "joint_credit", "case": case, "eps": float(eps),
                     "credit_support_only": b1["credit_vs_span64_worstcase_dyadic"],
                     "credit_with_mean": b2["credit_vs_span64_worstcase_dyadic"],
                     "credit_nondyadic": b3["credit_vs_span64_worstcase_dyadic"],
                     "k_best_dyadic": b2["k"], "label": "modelled (exact; mean assumed)",
                     "direction": "quantum-favourable"})
result["part4_credit_summary"] = credit_summary


# self-check against CRITIQUE_wrongly_killed F3 table (0.45 eps): span64+mean, (3,47)+mean, nondyadic 38.82+mean
def cred(case, eps, span, mean_prefix, dy):
    return [r for r in part4 if r["case"] == case and r["eps"] == eps and r["split"] == "0.45eps"
            and r["span"] == span and r["mean_bound"].startswith(mean_prefix)
            and (r["M_rule"] == "dyadic") == dy][0]["credit_vs_span64_worstcase_dyadic"]


for case, eps, c64, c3, cnd in (("B4x12", 0.1, 2, 4, 5.2), ("B8x52", 0.1, 4, 4, 5.4), ("B8x52", 0.01, 2, 4, 4.3),
                                ("B8x52", 0.001, 2, 2, 3.5), ("B4x12", 0.001, 2, 2, 3.4)):
    assert round(cred(case, eps, "64", "price", True)) == c64
    assert round(cred(case, eps, "128/3 (3,47)", "price", True)) == c3
    assert abs(cred(case, eps, "8192/211 (211,53)", "price", False) - cnd) < 0.06
# U2 sec 4: (3,47) halves M without a mean bound at 1/10 and 1/100, not at 3/100 or 1/1000
for eps, halves in ((0.1, True), (0.03, False), (0.01, True), (0.001, False)):
    assert (round(cred("B4x12", eps, "128/3 (3,47)", "none", True)) == 2) == halves
result["part4_self_checks"] = "CRITIQUE F3 table and U2 sec 4 halving pattern reproduced (asserts passed)"

# E04 joint screen (toy laws, eps=0.01, split 0.45, span 64)
e = F(9, 2000)
e04 = []
for law, m, toy in (("coin-Y0-or16 (a=1/8, mean $8)", F(8), 280800), ("coin-Y0-or32 (a=1/4, mean $16)", F(16), 525056)):
    cd = R15 * (min_M(m, F(64), e) - 1)
    cn = R15 * (min_M(m, F(64), e, dyadic=False) - 1)
    e04.append({"law": law, "E04_best_toy_paid_source_pairs": toy, "paware_canonical_dyadic": cd,
                "paware_canonical_nondyadic": cn, "E04_residual_vs_paware_dyadic": cd / toy,
                "E04_residual_vs_paware_nondyadic": cn / toy,
                "E04_vs_worstcase_983025": 983025 / toy,
                "label": "measured (toy controller, uncertified at financial a) / modelled canonical",
                "direction": "quantum-favourable"})
result["part4_E04_joint_screen"] = {
    "rows": e04,
    "reading": ("E04's 1.75x vs 983,025 is mostly the same p-awareness E03 credits: against a p-aware "
                "non-dyadic canonical at the same mean its residual is ~1.1-1.6x, on toy laws only, "
                "with no worst-case delivery guarantee; general IQAE theorem bounds are 6.6x worse than "
                "canonical. Multiply E03 credit by at most the non-dyadic residual, never by 1.75x.")}
row({"item": "E04", "sub": "joint_screen_with_E03", "rows": e04, "label": "measured toy / modelled",
     "direction": "quantum-favourable"})

# --------------------------------------------- 3. k_lo achievability by method
# (a) BHMT Theorem 12 parameter (k_B) vs repetitions, exact
bh = []
for fail in (FAIL_EST, FAIL_ALL):
    for kb in range(1, 9):
        if kb == 1:
            p = elementary_failure()
        elif kb == 2:
            continue  # success bound 1/2: medians impossible
        else:
            p = F(1, 2 * (kb - 1))
        r = median_reps(fail, p)
        bh.append({"failure": float(fail), "BHMT_k": kb, "per_shot_failure": float(p), "reps": r,
                   "cost_factor_k_times_reps": kb * r})
best_bh = {float(f): min((x for x in bh if x["failure"] == float(f)), key=lambda x: x["cost_factor_k_times_reps"])
           for f in (FAIL_EST, FAIL_ALL)}


# (b) window numerics: concentration of a real window w (length L) in |x|<=Delta
def autocorr(w):
    L = len(w)
    return [sum(w[j] * w[j + d] for j in range(L - d)) for d in range(L)]


def concentration(r, Delta):
    tot = r[0] * Delta / math.pi
    for d in range(1, len(r)):
        tot += 2 * r[d] * math.sin(d * Delta) / (math.pi * d)
    return tot / r[0]


def i0(x):
    t, s, k = 1.0, 1.0, 0
    while t > 1e-17 * s:
        k += 1
        t *= (x / 2) ** 2 / (k * k)
        s += t
    return s


def kaiser(N, alpha):
    return [i0(math.pi * alpha * math.sqrt(max(0.0, 1 - (m / N) ** 2))) for m in range(-N, N + 1)]


def dpss0(L, Delta):
    W = Delta / (2 * math.pi)
    d = [((L - 1) / 2 - n) ** 2 * math.cos(2 * math.pi * W) for n in range(L)]
    o = [(n + 1) * (L - n - 1) / 2 for n in range(L - 1)]

    def count_below(x):
        c, q = 0, d[0] - x
        if q < 0:
            c += 1
        for i in range(1, L):
            q = d[i] - x - o[i - 1] ** 2 / (q if q != 0 else 1e-300)
            if q < 0:
                c += 1
        return c

    lo = min(d) - 2 * max(o)
    hi = max(d) + 2 * max(o)
    for _ in range(200):
        mid = (lo + hi) / 2
        if count_below(mid) >= L:
            hi = mid
        else:
            lo = mid
    lam = hi + 1e-9 * abs(hi)
    x = [1.0] * L
    for _ in range(4):
        b = [d[i] - lam for i in range(L)]
        c = [o[i] if i < L - 1 else 0.0 for i in range(L)]
        cp, dp = [0.0] * L, [0.0] * L
        cp[0], dp[0] = c[0] / b[0], x[0] / b[0]
        for i in range(1, L):
            den = b[i] - o[i - 1] * cp[i - 1]
            cp[i] = c[i] / den
            dp[i] = (x[i] - o[i - 1] * dp[i - 1]) / den
        y = [0.0] * L
        y[-1] = dp[-1]
        for i in range(L - 2, -1, -1):
            y[i] = dp[i] - cp[i] * y[i + 1]
        nrm = math.sqrt(sum(v * v for v in y))
        x = [v / nrm for v in y]
    return x


def solve_delta(fail_fn, target, lo=1e-4, hi=3.0):
    for _ in range(60):
        mid = (lo + hi) / 2
        if fail_fn(mid) > target:
            lo = mid
        else:
            hi = mid
    return hi


window = {"convention": ("symmetric control (W vs W^-1) as in Berry et al. Lemma 4: L=2N+1 register "
                         "points, N calls, phase per point = Q eigenphase phi; continuous-outcome (zero-padded) "
                         "readout, so success is phase-independent (worst case = average); c = N*Delta"),
          "rows": []}
for target in (0.003, 0.01):
    for N in (100, 200, 400):
        L = 2 * N + 1

        def fdp(Delta, L=L):
            return 1 - concentration(autocorr(dpss0(L, Delta)), Delta)

        Dd = solve_delta(fdp, target, 1.0 / N, 12.0 / N)
        window["rows"].append({"window": "DPSS (optimal concentration)", "target_failure": target, "N": N,
                               "c": N * Dd, "label": "modelled (float numerics)"})
    # Kaiser: scan alpha at N=200, refine at N=400
    for N in (200, 400):
        bestc = None
        alphas = [0.6 + 0.02 * i for i in range(101)] if N == 200 else \
            [bestK - 0.06 + 0.01 * i for i in range(13)]
        for al in alphas:
            r = autocorr(kaiser(N, al))
            Dk = solve_delta(lambda D, r=r: 1 - concentration(r, D), target, 1.0 / N, 20.0 / N)
            if bestc is None or N * Dk < bestc[0]:
                bestc = (N * Dk, al)
        bestK = bestc[1]
        window["rows"].append({"window": "Kaiser (alpha optimised)", "target_failure": target, "N": N,
                               "alpha": round(bestc[1], 3), "c": bestc[0], "label": "modelled (float numerics)"})


def berry_formula_c(delta):
    """Berry et al. (D13)/(D15): ln(1/delta) = 2 pi a - ln(8 ln(2a) sqrt a); N*eps = pi sqrt(1+a^2)."""
    lo, hi = 0.6, 10.0
    f = lambda a: 2 * math.pi * a - math.log(8 * math.log(2 * a) * math.sqrt(a)) - math.log(1 / delta)
    for _ in range(100):
        mid = (lo + hi) / 2
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    return math.pi * math.sqrt(1 + hi * hi), hi


for target in (0.003, 0.01):
    cb, ab = berry_formula_c(target)
    window["rows"].append({"window": "Kaiser, Berry et al. (D13)/(D15) approximate formula",
                           "target_failure": target, "alpha": ab, "c": cb,
                           "leading_order_c": 0.5 * math.log(1 / target), "label": "literature formula (approximate)"})
# sanity: rectangular window, Delta = pi/N (canonical-equivalent), success should exceed 8/pi^2
rect_succ = concentration(autocorr([1.0] * 401), 2 * math.pi / 401 * 1.0)
window["self_check_rectangular_success_at_Delta_2pi_over_L"] = rect_succ
assert rect_succ > 8 / math.pi ** 2


def cval(name, target):
    rr = [r for r in window["rows"] if r["window"].startswith(name) and r["target_failure"] == target]
    return rr[-1]["c"]


C_DPSS = {t: cval("DPSS", t) for t in (0.003, 0.01)}
C_KAIS = {t: cval("Kaiser (alpha", t) for t in (0.003, 0.01)}
C_BERRY = {t: berry_formula_c(t)[0] for t in (0.003, 0.01)}
# self-checks: optimum <= Kaiser <= Berry's loose tail bound; bisection not at its bracket edge
for t in (0.003, 0.01):
    assert C_DPSS[t] <= C_KAIS[t] + 1e-3 and C_KAIS[t] <= C_BERRY[t], (t, C_DPSS, C_KAIS, C_BERRY)
    assert all(r["c"] < 11.5 for r in window["rows"])
result["part3_window_numerics"] = window
row({"item": "F4/E08", "sub": "window_constants_c", "c_DPSS": C_DPSS, "c_Kaiser_numeric": C_KAIS,
     "c_Berry_formula": C_BERRY, "label": "modelled (float numerics; literature formula)",
     "direction": "quantum-favourable"})


def delta_phi(m, S, e):
    """Largest Delta with sqrt(m(S-m))*Delta + S*Delta^2/4 + 2^-39 <= e (float)."""
    m = S / 2 if m is None else m
    A = math.sqrt(float(m * (S - m)))
    Sf, ef = float(S), float(e - READOUT)
    return (-A + math.sqrt(A * A + Sf * ef)) / (Sf / 2)


def iqae(eps_a, alpha):
    return 50 / eps_a * math.log((2 / alpha) * math.log2(math.pi / (4 * eps_a)))


def miqae(eps_a, alpha):
    return 3 * math.pi / (8 * eps_a * math.sin(math.pi / 21) ** 2 * math.sin(8 * math.pi / 21) ** 2) * \
        math.log(math.sqrt(27) / alpha)


assert math.ceil(iqae(float(F(9, 128000)), 0.003)) == 6471874
assert abs(math.ceil(miqae(float(F(9, 128000)), 0.003)) - 6491064) <= 1


def patel_thm2_calls(Delta, delta):
    mb = math.ceil(math.log2(175 * (math.log(10 / delta) + 1) ** 2 + 1)) + 1
    dc = Delta / (2 * math.pi)  # cycles
    tau = 1
    while dc < 1 / 2 ** (tau + 1):
        tau += 1
    return 2 ** (tau + mb) - 1, mb


part3 = []
for case in CASES:
    s = float(SIGMA[case])
    for eps in EPS:
        for sl, sp in SPLITS.items():
            e = sp * eps
            ef = float(e)
            se = s / ef
            mb = PRICE[case] + L1_DISPLAY
            recs = []
            k0 = R15 * (min_M(None, F(64), e) - 1) / se
            recs.append(("canonical BHMT Thm12 + 15 medians (E07, span 64, dyadic)", k0, "explicit (certified schedule)"))
            for spl, S in SPANS.items():
                for ml, m in (("no mean", None), ("price+L1", mb)):
                    for dy in (True, False):
                        if spl == "64" and m is None and dy:
                            continue
                        kk = R15 * (min_M(m, S, e, dy) - 1) / se
                        recs.append((f"canonical + medians, span {spl}, {ml}, {'dyadic' if dy else 'non-dyadic'} M",
                                     kk, "explicit formula; conditional on " +
                                     ("U1 mean certificate + " if m is not None else "") +
                                     ("U2 wrapper" if spl != "64" else "saved wrapper") +
                                     ("" if dy else " + non-power-of-two QFT")))
            for spl, S in (("64", F(64)), ("8192/211", F(8192, 211))):
                eps_a = ef / float(S)
                recs.append((f"IQAE Grinko et al. Thm1 (span {spl}, worst case over a)", iqae(eps_a, 0.003) / se,
                             "explicit (literature theorem)"))
                recs.append((f"modified IQAE Fukuzawa et al. Lemma 3.7 (span {spl})", miqae(eps_a, 0.003) / se,
                             "explicit (literature theorem)"))
            for spl, S in (("64", F(64)), ("8192/211", F(8192, 211))):
                for ml, m in (("no mean", None), ("price+L1", mb)):
                    D = delta_phi(m, S, e)
                    for t in (0.003, 0.01):
                        recs.append((f"window/DPSS one chain, span {spl}, {ml}, fail {t}", C_DPSS[t] / D / se,
                                     "no explicit constant (modelled numerics; DPSS is the average-case optimum)"))
                        recs.append((f"window/Kaiser one chain, span {spl}, {ml}, fail {t}", C_KAIS[t] / D / se,
                                     "no explicit constant (modelled numerics)"))
                        recs.append((f"window/Kaiser Berry formula, span {spl}, {ml}, fail {t}", C_BERRY[t] / D / se,
                                     "no explicit constant (literature asymptotic formula)"))
                    calls_p, mbits = patel_thm2_calls(D, 0.003)
                    recs.append((f"tQPE Patel et al. Thm2 explicit (average-case), span {spl}, {ml}", calls_p / se,
                                 "explicit but average-case only (not a worst-case guarantee)"))
            for name, kk, lab in recs:
                part3.append({"case": case, "eps": float(eps), "split": sl, "method": name, "k_total": kk,
                              "constant_status": lab, "label": "modelled", "direction": "quantum-favourable"
                              if kk < k0 else "adverse" if kk > k0 else "neutral"})
result["part3_BHMT_k_vs_reps"] = {"rows": bh, "best": best_bh}
result["part3_k_lo_methods"] = part3
result["part3_unexplicit_methods"] = [
    {"method": "MLAE (Suzuki et al. 2020)", "status": "no explicit constant (asymptotic Fisher-information CI only)"},
    {"method": "ChebAE / QSP-AE (Rall & Fuller, Quantum 7, 937 (2023))", "status": "no explicit constant (empirical ~4.66/eps at 95%)"},
    {"method": "Kaiser-window AE (Berry et al. PRX Quantum 5, 010319 (2024), App. D)", "status": "no explicit constant (leading order ln(1/delta)/(2 eps) plus unstated O(eps^-1 lnln) term)"},
    {"method": "Kothari-O'Donnell sigma-normalised", "status": "no explicit constant"},
    {"method": "Nakaji FAE (arXiv:2003.02417 Thm 1)", "status": "explicit 4.1e3/eps ln(4log2(2pi/3eps)/delta) on amplitude a; >>canonical"},
]
for case in CASES:
    for eps in EPS:
        sub = [r for r in part3 if r["case"] == case and r["eps"] == float(eps) and r["split"] == "0.45eps"]
        ex = [r for r in sub if r["constant_status"].startswith("explicit") and "average" not in r["constant_status"]]
        bx = min(ex, key=lambda r: r["k_total"])
        bw = min((r for r in sub if r["method"].startswith("window/DPSS") and "fail 0.003" in r["method"]),
                 key=lambda r: r["k_total"])
        row({"item": "C11/E25/E08", "sub": "k_lo", "case": case, "eps": float(eps),
             "k_lo_explicit_best": [bx["method"], bx["k_total"], bx["constant_status"]],
             "k_window_modelled_best": [bw["method"], bw["k_total"]],
             "label": "modelled", "direction": "quantum-favourable"})

# ------------------------------------------------------------------ 5. lanes
part5 = []
for case in CASES:
    s = SIGMA[case]
    w = WIDTH[case]
    trate = TCOUNT[case] / (DEPTH[case] * 1e-7)
    for Wb in (10 ** 6, 10 ** 7, 10 ** 8):
        for wl, ww in (("current", w), ("current/2", w // 2), ("current/4", w // 4), ("current/10", w // 10)):
            lanes = Wb // ww
            for eps in EPS:
                for sl, sp in SPLITS.items():
                    e = sp * eps
                    M = min_M(None, F(64), e)
                    b = best(case, eps, sl, True, False)
                    Mb = b["M"]
                    rec = {"case": case, "W": Wb, "lane_width": wl, "lane_width_qubits": ww, "lanes": lanes,
                           "eps": float(eps), "split": sl}
                    if lanes == 0:
                        rec["k_lat"] = None
                        rec["note"] = "one lane does not fit in W"
                    else:
                        rounds = -(-R15 // lanes)
                        rec["rounds"] = rounds
                        rec["k_lat_E07"] = float(rounds * (M - 1) * e / s)
                        rec["k_lat_best_E03_dyadic"] = float(rounds * (Mb - 1) * e / s)
                        rec["k_lat_1lane_E07"] = float(R15 * (M - 1) * e / s)
                        rec["required_T_per_s_at_100ns"] = min(lanes, R15) * trate
                    rec["label"] = "modelled (width assumed = source logical qubits; QPE register ignored)"
                    rec["direction"] = "quantum-favourable"
                    part5.append(rec)
result["part5_lanes"] = part5
result["part5_notes"] = {
    "full_median_parallelism_needs_lane_width_at_most": 10 ** 7 // 15,
    "window_methods": "single coherent chain: k_lat = k_total; lanes do not shorten it",
    "independent_subestimate_averaging": "sqrt(P) latency cut at sqrt(P) more calls; needs unbiasedness/variance argument; no explicit 99% constant (not tabulated)",
    "T_rate_per_lane_at_100ns": {c: TCOUNT[c] / (DEPTH[c] * 1e-7) for c in CASES},
}
for case in CASES:
    for eps in EPS:
        r = [x for x in part5 if x["case"] == case and x["W"] == 10 ** 7 and x["lane_width"] == "current"
             and x["eps"] == float(eps) and x["split"] == "0.45eps"][0]
        row({"item": "E20", "sub": "k_lat_at_W", "case": case, "eps": float(eps), "lanes": r["lanes"],
             "k_lat_E07": r.get("k_lat_E07"), "k_lat_best_E03": r.get("k_lat_best_E03_dyadic"),
             "k_1lane": r.get("k_lat_1lane_E07"), "label": "modelled", "direction": "quantum-favourable"})

with open(OUT + "k_bracket.json", "x", encoding="utf-8") as f:
    json.dump(result, f, indent=1)
print("done")
