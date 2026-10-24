"""Independent recompute of the U1 certificate (different arithmetic: integers and Fractions only).

- ln(2/delta) by the atanh series with an explicit geometric remainder (upper bound);
- square roots by integer isqrt at 2^-200 resolution (rounded up);
- Delta by the closed-form root of  a*D + S*D^2/4 + 2^-39 = e  (a = sqrt(m(S-m)), rounded down), not bisection.
Agreement with u1_certificate.json: m_cert within 1e-30 USD and identical call counts.

Run (worktree root): <frontier_t0_env python> -I -S -B research/claim_debts_20261022/u1/u1_independent.py RUN
"""
import json
import math
import os
import sys
from fractions import Fraction as F

RUN = sys.argv[1]
OUT = os.path.join("results", "claim_debts_20261022", "u1", RUN)
SCALE = 2 ** 200


def sqrt_up(x):
    x = F(x)
    v = x * SCALE * SCALE
    r = math.isqrt(v.numerator // v.denominator)
    while F(r * r) < v:
        r += 1
    return F(r, SCALE)


def sqrt_down(x):
    x = F(x)
    v = x * SCALE * SCALE
    r = math.isqrt(v.numerator // v.denominator)
    return F(r, SCALE)


def ln_up(x):
    """ln x = 2 atanh((x-1)/(x+1)) = 2 sum_k y^(2k+1)/(2k+1); remainder after K terms <= 2 y^(2K+1)/((2K+1)(1-y^2))."""
    x = F(x)
    # reduce: ln x = j ln 2 + ln(x / 2^j), with x/2^j in [1, 2)
    j = 0
    while x >= 2:
        x /= 2
        j += 1
    def series(z, terms=80):
        y = (z - 1) / (z + 1)
        s, p = F(0), y
        for k in range(terms):
            s += p / (2 * k + 1)
            p *= y * y
        rem = 2 * p / ((2 * terms + 1) * (1 - y * y))
        return 2 * s, rem
    s, r = series(x)
    l2, r2 = series(F(2))
    return s + r + j * (l2 + r2)


with open(os.path.join(OUT, "eb_sample.json"), encoding="utf-8") as f:
    eb = json.load(f)
with open(os.path.join(OUT, "u1_certificate.json"), encoding="utf-8") as f:
    cert = json.load(f)
with open("results/claim_debts_20261022/a2a/run001/summary.json", encoding="utf-8") as f:
    a2a = json.load(f)
with open("results/frontier_classical_20261001/sigma_dev/sigma_dev.json", encoding="utf-8") as f:
    sigma_q = F(str(json.load(f)["cases"]["B8x52"]["sigma_q"]))
with open("results/frontier_probe_20261021/p2/run002/p2_window.json", encoding="utf-8") as f:
    p2k = json.load(f)["k"]["B8x52|0.001|0.45eps|8192/211|price+L1|with_impl_budget|fail 3/1000"]
with open("results/frontier_classical_20261001/c1/c1_summary.json", encoding="utf-8") as f:
    price = F(str(json.load(f)["port_check"]["B8x52"]["price"]))

n = int(eb["n"])
sum1, sum2 = F(eb["sum"]), F(eb["sum_sq"])
var = (n * sum2 - sum1 * sum1) / (n * (n - 1))
mean = sum1 / n + F(1, 10 ** 9)
lg = ln_up(F(2) / F(1, 10000))
ucb = mean + sqrt_up(2 * var * lg / n) + 7 * 40 * lg / (3 * (n - 1))
bias = F(*a2a["cases"]["B8x52"]["certified_total_upper_rounded_up_2^-64"])
m_cert = ucb + bias
m_primary = F(int(cert["m_cert"][0]), int(cert["m_cert"][1]))

S, e, ro = F(8192, 211), F(9, 20000), F(1, 2 ** 39)
c = F(str(p2k["c"]))


def calls(m):
    a = sqrt_up(m * (S - m))
    # largest D with a D + S D^2/4 + ro <= e:  D = 2(-a + sqrt(a^2 + S (e - ro))) / S  (rounded down)
    D = 2 * (sqrt_down(a * a + S * (e - ro)) - a) / S
    return math.ceil(c / D)


N_old, N_cert = calls(price + F(45202052, 10 ** 9)), calls(m_cert)
res = dict(
    script="research/claim_debts_20261022/u1/u1_independent.py", python=sys.version,
    ln_2e4_upper=float(lg), ucb_EY=float(ucb), m_cert=float(m_cert),
    m_cert_abs_diff_vs_primary=float(abs(m_cert - m_primary)),
    N_calls_at_p2_m=N_old, N_calls_primary_at_p2_m=cert["window_class"]["at_p2_m"]["N_calls"],
    N_calls_at_m_cert=N_cert, N_calls_primary_at_m_cert=cert["window_class"]["at_m_cert"]["N_calls"],
    k_at_p2_m=N_old * float(F(9, 20000) / sigma_q), k_at_m_cert=N_cert * float(F(9, 20000) / sigma_q),
)
res["agree"] = (res["m_cert_abs_diff_vs_primary"] <= 1e-30 and N_old == res["N_calls_primary_at_p2_m"]
                and N_cert == res["N_calls_primary_at_m_cert"] and N_old == p2k["N_calls"])
with open(os.path.join(OUT, "u1_independent.json"), "x", encoding="utf-8") as f:
    json.dump(res, f, indent=1)
print(json.dumps(res, indent=1))
