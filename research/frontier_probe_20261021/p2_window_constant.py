"""P2 of the 21 Oct 2026 frontier probe: an explicit worst-case constant for window phase/amplitude estimation
(v3 sec 6 lever 1; estimator card sec 5 parts 1-4).

Window. Kaiser family with pedestal fraction gamma in [0, 1]:
    phi(x) = I0(beta sqrt(1 - x^2)) - gamma on [-1, 1],  w_n = phi(n / N) for |n| < N,  w_{+-N} = (1 - gamma) / 2,
so 2N + 1 taps, exponents -N..N, N controlled calls with direction-select (the WS-k window convention).
Its continuous transform is closed form: Phi(eta) = 2 sinh(sqrt(beta^2 - eta^2)) / sqrt(beta^2 - eta^2)
- 2 gamma sin(eta) / eta (sinh -> sin past eta = beta).

Concentration. With continuous readout (or a G-point QFT, G >= 2N + 1, plus a uniformly random known phase
offset of the register, which is query-free) the estimate satisfies, for EVERY eigenphase phi,
    P(|phi_hat - phi| <= Delta) = lambda0(N, Delta) = (1 / 2pi) int_{-Delta}^{Delta} W(w)^2 dw / sum_n w_n^2.
Poisson summation (phi_1 = phi - (1 - gamma) 1_[-1,1] is continuous with phi_1(+-1) = 0; the rectangular part
with half-weight ends has DTFT sin(N w) cot(w / 2) exactly) gives W(w) = N Phi(N w) + R(w) with
    |R(w)| <= beta^2 kappa / (4N) + (1 - gamma) |sin(N w)| |cot(w/2) - 2/w|,   |cot(w/2) - 2/w| <= (2/pi^2)|w|.
Expanding sum w_n^2 = (1/2pi) int (N Phi(N w) + R)^2 and the in-band integral the same way gives
    lambda0 >= (N I_c / 2pi - X_band) / (N I_tot / 2pi + X + C_R^2),
I_c = int_{-c}^{c} Phi^2, I_tot = int_R Phi^2 = 2 pi int phi^2, c = N Delta, and X, X_band, C_R explicit O(1),
O(1/N) terms. Every correction divided by N decreases with N, so the bound certified at N0 holds for all
N >= N0 (part 1 with an explicit N0, part 2).

Certification. I_tot: exact rational series in (1 - x^2)^k with a rational tail bound and rational pi
enclosure. I_c: composite midpoint rule at 50 decimal digits with the rigorous error term
(2c) h^2 max|(Phi^2)''| / 24 and max|(Phi^2)''| <= 4 Phi(0)^2 (|Phi^(k)| <= int |x|^k phi <= Phi(0)).
Part 3 (finite grid) is handled by the random offset; part 4 (state-preparation / QFT / rotation precision)
is NOT certified: a budget delta_impl is reserved and labelled assm.

Run (repo root): .context/frontier_t0_env/Scripts/python.exe -I -S -B research/frontier_probe_20261021/p2_window_constant.py
"""
import hashlib
import json
import math
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

getcontext().prec = 50
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "frontier_probe_20261021" / "p2" / "run001"
IN = dict(
    sigma=ROOT / "results/frontier_classical_20261001/sigma_dev/sigma_dev.json",
    c1=ROOT / "results/frontier_classical_20261001/c1/c1_summary.json",
    kb=ROOT / "results/plan110_w0/ws_k/k_bracket.json",
)
PI_LO = Fraction("3.14159265358979323")
PI_HI = Fraction("3.14159265358979324")
D_PI = Decimal("3.1415926535897932384626433832795028841971693993751")
N0 = 800  # below the smallest N any decision or overhead cell uses (about 1.0e3 at B4x12 eps = 0.10)
DELTA_IMPL = Fraction(1, 10000)  # part-4 budget reserved inside delta (assm, not certified)
L1 = Fraction(45202052, 10 ** 9)
READOUT = Fraction(1, 2 ** 39)
S_SPAN = {"64": Fraction(64), "8192/211": Fraction(8192, 211)}
EPS = (0.1, 0.03, 0.01, 0.001)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def row(d):
    with open(OUT / "rows.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(d, sort_keys=True, default=str) + "\n")


# ------------------------------------------------------------------ exact total energy (upper bound)
def int_phi_sq_upper(beta2, gamma, kmax=60):
    """Upper bound on int_{-1}^{1} phi^2 dx, phi = (1 - gamma) + sum_{k>=1} c_k (1 - x^2)^k, c_k = (beta^2/4)^k / (k!)^2,
    int (1 - x^2)^m = 2^(2m+1) (m!)^2 / (2m+1)!. Tail: c_k ratio < 1/2 beyond kmax, J_m <= 2."""
    c = [Fraction(1) - gamma]
    for k in range(1, kmax + 1):
        c.append((beta2 / 4) ** k / Fraction(math.factorial(k)) ** 2)
    assert (beta2 / 4) / (kmax + 1) ** 2 < Fraction(1, 2)
    J = [Fraction(2 ** (2 * m + 1) * math.factorial(m) ** 2, math.factorial(2 * m + 1)) for m in range(2 * kmax + 1)]
    s = sum(c[k] * c[l] * J[k + l] for k in range(kmax + 1) for l in range(kmax + 1))
    tail_c = 2 * (beta2 / 4) ** (kmax + 1) / Fraction(math.factorial(kmax + 1)) ** 2
    total_c = sum(c) + tail_c
    return s + 2 * 2 * total_c * tail_c + 2 * tail_c ** 2  # generous: cross terms with J <= 2


# ------------------------------------------------------------------ decimal transcendental helpers
def d_sin(x):
    x = Decimal(x)
    term, s, n = x, x, 1
    while abs(term) > Decimal(10) ** -48:
        term = -term * x * x / ((n + 1) * (n + 2))
        s += term
        n += 2
    return s


def d_sinh_over(s):
    """sinh(s)/s for s >= 0 (series for small s)."""
    if s < Decimal("0.5"):
        term, tot, n = Decimal(1), Decimal(1), 1
        while term > Decimal(10) ** -48:
            term = term * s * s / ((n + 1) * (n + 2))
            tot += term
            n += 2
        return tot
    e = s.exp()
    return (e - 1 / e) / (2 * s)


def d_sinc(s):
    if s == 0:
        return Decimal(1)
    if s < Decimal("0.5"):
        term, tot, n = Decimal(1), Decimal(1), 1
        while abs(term) > Decimal(10) ** -48:
            term = -term * s * s / ((n + 1) * (n + 2))
            tot += term
            n += 2
        return tot
    return d_sin(s) / s


def Phi_dec(eta, beta, gamma):
    eta, beta, gamma = Decimal(eta), Decimal(beta), Decimal(gamma)
    b2, e2 = beta * beta, eta * eta
    if e2 < b2:
        a = 2 * d_sinh_over((b2 - e2).sqrt())
    else:
        a = 2 * d_sinc((e2 - b2).sqrt())
    return a - 2 * gamma * d_sinc(abs(eta))


def I_c_lower(c, beta, gamma, h):
    """Lower bound on int_{-c}^{c} Phi^2 by the midpoint rule with the rigorous second-derivative error term."""
    c = Fraction(c)
    n = int(math.ceil(c / h))
    hh = c / n
    acc = Decimal(0)
    for i in range(n):
        mid = (Fraction(2 * i + 1) * hh) / 2
        v = Phi_dec(Decimal(mid.numerator) / Decimal(mid.denominator), beta, gamma)
        acc += v * v
    mid_sum = 2 * acc * (Decimal(hh.numerator) / Decimal(hh.denominator))
    phi0 = Phi_dec(0, beta, gamma)
    m2 = 4 * phi0 * phi0
    err = (2 * Decimal(c.numerator) / Decimal(c.denominator)) * (Decimal(hh.numerator) / Decimal(hh.denominator)) ** 2 * m2 / 24
    return mid_sum - err, dict(n=n, midpoint=mid_sum, err_bound=err, phi0=phi0)


# ------------------------------------------------------------------ finite-N lower bound
def lambda_lower(N, c, beta, gamma, Ic_lo, Itot_hi, phi0):
    """Certified lambda0(N, c/N) >= value, all terms rounded in the safe direction (Decimal, 50 digits)."""
    D = Decimal
    N_ = D(N)
    pl = D("3.14159265358979323")
    ph = D("3.14159265358979324")
    b = D(beta)
    b2 = b * b
    g = D(gamma)
    cd = D(c)
    eta_min = N_ * pl
    s_min = (eta_min * eta_min - b2).sqrt()
    kappa = (1 + 1 / s_min) / (1 - b2 / (eta_min * eta_min))
    C_R = b2 * kappa / (4 * N_) + (1 - g) * 2 / pl
    # |Phi_1(eta)| <= A1 / eta^2 for |eta| >= eta1 = 2 beta; |Phi_1| <= Phi_1(0) = 2 sinh(beta)/beta - 2
    eta1 = 2 * b
    A1 = D("1.23761") * b2 * (1 + 2 / (D(3).sqrt() * eta1))
    phi1_0 = 2 * d_sinh_over(b) - 2
    U1 = 2 * (eta1 * phi1_0 + A1 / eta1)
    V1 = 2 * (eta1 * eta1 * phi1_0 / 2 + A1 * (N_ * ph / eta1).ln())
    L1Phi = U1 + (1 - g) * 4 * (1 + (N_ * ph).ln())
    L1etaPhi = V1 + (1 - g) * 8 * N_
    X = (b2 * kappa / (4 * N_) * L1Phi + (1 - g) * (2 / (pl * pl)) * L1etaPhi / N_) / pl
    X_band = (b2 * kappa / (4 * N_) + (1 - g) * (2 / (pl * pl)) * cd / N_) * 2 * cd * phi0 / pl
    P = N_ * Ic_lo / (2 * ph)
    Q = N_ * Itot_hi / (2 * pl)
    lam = (P - X_band) / (Q + X + C_R * C_R)
    return lam, dict(C_R=C_R, X=X, X_band=X_band, P=P, Q=Q, kappa=kappa)


def float_c(beta, gamma, delta):
    """Float exploration only (continuous leakage), used to pick beta; not part of the certificate."""
    def i0(x):
        t = s = 1.0
        k = 0
        while t > 1e-18 * s:
            k += 1
            t *= (x / 2) ** 2 / (k * k)
            s += t
        return s

    def Phi(e):
        if e == 0:
            return 2 * math.sinh(beta) / beta - 2 * gamma
        if abs(e) < beta:
            s = math.sqrt(beta * beta - e * e)
            a = 2 * math.sinh(s) / s
        elif abs(e) > beta:
            s = math.sqrt(e * e - beta * beta)
            a = 2 * math.sin(s) / s
        else:
            a = 2.0
        return a - 2 * gamma * math.sin(e) / e
    n = 20000
    tot = 2 * math.pi * sum((i0(beta * math.sqrt(max(0, 1 - (-1 + (i + .5) * 2 / n) ** 2))) - gamma) ** 2
                            for i in range(n)) * 2 / n

    def leak(c):
        m = int(c / 2e-3)
        hh = c / m
        return 1 - 2 * sum(Phi((i + .5) * hh) ** 2 for i in range(m)) * hh / tot
    lo, hi = 2.0, 8.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if leak(mid) > delta:
            lo = mid
        else:
            hi = mid
    return hi


def direct_lambda(N, c, beta, gamma):
    """Independent float check: exact discrete concentration by autocorrelation (O(N^2)), small N only."""
    def i0(x):
        t = s = 1.0
        k = 0
        while t > 1e-18 * s:
            k += 1
            t *= (x / 2) ** 2 / (k * k)
            s += t
        return s
    w = [i0(beta * math.sqrt(max(0.0, 1 - (n / N) ** 2))) - gamma for n in range(-N, N + 1)]
    w[0] = w[-1] = (1 - gamma) / 2
    L = len(w)
    D = c / N
    r = [math.fsum(w[j] * w[j + d] for j in range(L - d)) for d in range(L)]
    tot = r[0] * D / math.pi + math.fsum(2 * r[d] * math.sin(d * D) / (math.pi * d) for d in range(1, L))
    return tot / r[0]


def certify(beta_str, gamma, delta_target, Itot_hi, c_lo, c_hi, h):
    """Smallest c on a 0.001 grid in [c_lo, c_hi] with certified lambda_lower(N0, c) >= 1 - delta_target."""
    beta = Decimal(beta_str)
    cache = {}

    def ok(ci):
        c = Fraction(ci, 1000)
        if ci not in cache:
            Ic, info = I_c_lower(c, beta, Decimal(gamma.numerator) / Decimal(gamma.denominator), h)
            lam, parts = lambda_lower(N0, Decimal(ci) / 1000, beta, Decimal(gamma.numerator) / Decimal(gamma.denominator),
                                      Ic, Decimal(Itot_hi.numerator) / Decimal(Itot_hi.denominator), info["phi0"])
            cache[ci] = (lam, Ic, info, parts)
        return cache[ci][0] >= 1 - Decimal(delta_target.numerator) / Decimal(delta_target.denominator)
    lo, hi = int(c_lo * 1000), int(c_hi * 1000)
    assert ok(hi) and not ok(lo), (beta_str, gamma, delta_target, lo, hi)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid
    lam, Ic, info, parts = cache[hi]
    return Fraction(hi, 1000), dict(lambda_lower_N0=lam, I_c_lower=Ic, quad=info, parts=parts)


def delta_phi(m, S, e):
    """Largest Delta (Fraction-exact bisection) with sqrt(m (S - m)) Delta + S Delta^2 / 4 + 2^-39 <= e (WS-k rule)."""
    m = S / 2 if m is None else m
    A2 = m * (S - m)
    lo, hi = Fraction(0), Fraction(1)
    for _ in range(200):
        mid = (lo + hi) / 2
        lhs_lin = mid * Fraction(math.sqrt(float(A2)) * (1 + 1e-15))  # outward
        if lhs_lin + S * mid * mid / 4 + READOUT <= e:
            lo = mid
        else:
            hi = mid
    return lo


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    sig = load(IN["sigma"])["cases"]
    price = {c: Fraction(str(load(IN["c1"])["port_check"][c]["price"])) for c in ("B4x12", "B8x52")}
    meta = dict(script="research/frontier_probe_20261021/p2_window_constant.py", python=sys.version,
                flags=dict(isolated=sys.flags.isolated, no_site=sys.flags.no_site),
                inputs_sha256={k: sha(v) for k, v in IN.items()}, N0=N0, delta_impl=str(DELTA_IMPL))
    res = dict(meta=meta, certified={}, checks={}, k={})
    designs = []
    for delta in (Fraction(3, 1000), Fraction(1, 100)):
        for gamma in (Fraction(0), Fraction(1)):
            # pick beta by float exploration (not part of the certificate), round to 2 decimals
            best = min((float_c(b / 100, float(gamma), float(delta)), b) for b in range(250, 460, 5))
            bb = best[1]
            best = min((float_c(b / 100, float(gamma), float(delta)), b) for b in range(bb - 5, bb + 6))
            designs.append((delta, gamma, best[1], best[0]))
            row(dict(step="beta_pick", delta=str(delta), gamma=str(gamma), beta=best[1] / 100, c_float=best[0],
                     label="mod (float exploration; not certified)"))
    for delta, gamma, b100, c_float in designs:
        beta_str = f"{b100 / 100:.2f}"
        beta2 = Fraction(b100, 100) ** 2
        Itot_hi = 2 * PI_HI * int_phi_sq_upper(beta2, gamma)
        for tag, dtarget in (("no_impl_budget", delta), ("with_impl_budget", delta - DELTA_IMPL)):
            c_cert, info = certify(beta_str, gamma, dtarget, Itot_hi, c_float - 0.05, c_float + 0.10,
                                   Fraction(1, 1000))
            key = f"delta={delta}|gamma={gamma}|{tag}"
            res["certified"][key] = dict(beta=beta_str, gamma=str(gamma), delta=str(delta), delta_target=str(dtarget),
                                         c_certified=float(c_cert), c_float_continuous=c_float, N0=N0,
                                         I_tot_upper=float(Itot_hi), **{k: str(v) for k, v in info.items()},
                                         label="mod (certified: exact rationals + 50-digit decimal with rigorous "
                                               "quadrature error; analytic aliasing bound derived here)",
                                         direction="q+ relative to today's explicit constant")
            row(dict(step="certified_c", key=key, beta=beta_str, c_certified=float(c_cert),
                     lambda_lower_N0=str(info["lambda_lower_N0"]), c_float=c_float))
            print(key, "beta", beta_str, "c_cert", float(c_cert), "lambda_LB(N0)", str(info["lambda_lower_N0"])[:12])
            # monotonicity sanity in N (the proof is structural; this is a numeric spot check)
            Ic = info["I_c_lower"]
            lams = []
            for N in (N0, 2000, 10 ** 4, 10 ** 5, 10 ** 6):
                lam, _ = lambda_lower(N, Decimal(c_cert.numerator) / Decimal(c_cert.denominator), Decimal(beta_str),
                                      Decimal(gamma.numerator) / Decimal(gamma.denominator), Ic,
                                      Decimal(Itot_hi.numerator) / Decimal(Itot_hi.denominator), info["quad"]["phi0"])
                lams.append((N, lam))
            assert all(lams[i][1] <= lams[i + 1][1] for i in range(len(lams) - 1)), lams
            res["certified"][key]["lambda_lower_vs_N"] = [(n, str(l)) for n, l in lams]
    # independent float check of the finite-N bound against the exact discrete concentration (small N)
    for delta, gamma, b100, c_float in designs:
        key = f"delta={delta}|gamma={gamma}|no_impl_budget"
        c_cert = res["certified"][key]["c_certified"]
        beta = b100 / 100
        Itot_hi = 2 * PI_HI * int_phi_sq_upper(Fraction(b100, 100) ** 2, gamma)
        Ic, info = I_c_lower(Fraction(str(c_cert)), Decimal(f"{beta:.2f}"), Decimal(gamma.numerator) / Decimal(gamma.denominator), Fraction(1, 1000))
        chk = []
        for N in (100, 400, 1000):
            lam_b, _ = lambda_lower(N, Decimal(str(c_cert)), Decimal(f"{beta:.2f}"), Decimal(gamma.numerator) / Decimal(gamma.denominator),
                                    Ic, Decimal(Itot_hi.numerator) / Decimal(Itot_hi.denominator), info["phi0"])
            lam_d = direct_lambda(N, c_cert, beta, float(gamma))
            chk.append(dict(N=N, bound=float(lam_b), direct=lam_d, ok=float(lam_b) <= lam_d))
        assert all(x["ok"] for x in chk), chk
        res["checks"][key] = chk
        row(dict(step="direct_check", key=key, checks=chk, label="mod (float, independent algorithm)"))
    # estimator constants k = N / (sigma / e) with N = ceil(c / Delta), WS-k Delta rule
    best_c = {}
    for tag in ("no_impl_budget", "with_impl_budget"):
        for delta in (Fraction(3, 1000), Fraction(1, 100)):
            cands = {k: v for k, v in res["certified"].items() if k.startswith(f"delta={delta}|") and k.endswith(tag)}
            kbest = min(cands, key=lambda k: cands[k]["c_certified"])
            best_c[(tag, delta)] = (cands[kbest]["c_certified"], kbest)
    kb = load(IN["kb"])
    for case in ("B4x12", "B8x52"):
        s = Fraction(str(sig[case]["sigma_q"]))
        for eps in EPS:
            for split, sp in (("0.45eps", Fraction(9, 20)), ("eps", Fraction(1))):
                e = sp * Fraction(str(eps))
                se = s / e
                for spl, S in S_SPAN.items():
                    for ml, m in (("no mean", None), ("price+L1", price[case] + L1)):
                        D_ = delta_phi(m, S, e)
                        for (tag, delta), (c, src) in best_c.items():
                            Ncalls = math.ceil(Fraction(str(c)) / D_)
                            k_ds = Ncalls / float(se)
                            res["k"][f"{case}|{eps}|{split}|{spl}|{ml}|{tag}|fail {delta}"] = dict(
                                c=c, design=src, N_calls=Ncalls, covered_by_N0_certificate=Ncalls >= N0,
                                k_direction_select=k_ds,
                                k_without_direction_select=2 * k_ds, label="mod", direction="q+")
    # WS-k comparison rows (DPSS numerics, no explicit constant)
    ws = {}
    for r in kb["part3_k_lo_methods"]:
        if r["case"] == "B8x52" and r["eps"] == 0.001 and r["split"] == "0.45eps" and r["method"].startswith("window/DPSS"):
            ws[r["method"]] = r["k_total"]
    res["ws_k_dpss_binding_cell"] = ws
    bc = {k: v for k, v in res["k"].items() if k.startswith("B8x52|0.001|0.45eps|8192/211|price+L1")}
    for k, v in bc.items():
        print(k, round(v["k_direction_select"], 4), "N", v["N_calls"])
    print("WS-k DPSS (binding cell):", ws)
    with open(OUT / "p2_window.json", "x", encoding="utf-8") as f:
        json.dump(res, f, indent=1, default=str)


if __name__ == "__main__":
    main()
