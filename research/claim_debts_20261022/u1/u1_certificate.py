"""U1 certificate (R1): a certified upper bound m on the digital mean E[g] = E[Y_N] at B8x52, eps = $0.001.

    E[g] = E[Y_N] <= E[Y] + |E Y_N - E Y| <= UCB_{1-delta_U}(E Y) + A2a,

- UCB: one-sided empirical Bernstein (Maurer & Pontil 2009, Thm 4) on the fixed-n raw-payoff sample
  (eb_sample.json), range R = 40 >= 40 e^{-rT} (analytic: on survival A <= max_j B_j < 140);
- A2a: certified bias bound |E Y_N - E Y| <= 6703058386012589/2^64 (results/claim_debts_20261022/a2a/run001).
Then: does m stay below the 'price + L1' value P2 used for the window class (k = 8.762), and what are k and M at m?

Run (worktree root): <frontier_t0_env python> -I -S -B research/claim_debts_20261022/u1/u1_certificate.py RUN
"""
import hashlib
import json
import math
import os
import sys
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, getcontext
from fractions import Fraction as F

getcontext().prec = 60
RUN = sys.argv[1]
OUT = os.path.join("results", "claim_debts_20261022", "u1", RUN)
IN = {
    "eb_sample": OUT + "/eb_sample.json",
    "a2a_summary": "results/claim_debts_20261022/a2a/run001/summary.json",
    "c09_saved": "results/c10_challengers_20261022/c09/B8x52_0.001_run001/c09_g4.json",
    "p2_window": "results/frontier_probe_20261021/p2/run002/p2_window.json",
    "p2_script": "research/frontier_probe_20261021/p2_window_constant.py",
    "sigma": "results/frontier_classical_20261001/sigma_dev/sigma_dev.json",
    "c1": "results/frontier_classical_20261001/c1/c1_summary.json",
    "eb_script": "research/claim_debts_20261022/u1/eb_sample.py",
}
DELTA_U = F(1, 10000)
R_RAW = F(40)
EPS = F(1, 1000)
E_STAT = F(9, 20) * EPS
S = F(8192, 211)
L1_OLD = F(45202052, 10 ** 9)  # the B4x12-borrowed L1 P2 used (not a B8x52 certificate)
READOUT = F(1, 2 ** 39)
FLOAT_SLACK = F(1, 10 ** 9)  # dollars; covers per-sample float rounding in the simulated payoff (assm, generous)
D_EFF, T_LAYER, T_C = F("2296.03168"), F(1, 10 ** 7), F("8.886479314695709")


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def load(k):
    with open(IN[k], encoding="utf-8") as f:
        return json.load(f)


def dec(x):
    x = F(x)
    return Decimal(x.numerator) / Decimal(x.denominator)


def up(d):
    """Decimal -> Fraction rounded up at 1e-40 (outward)."""
    return F(d.quantize(Decimal("1e-40"), rounding=ROUND_CEILING))


def ln_upper(x):
    return up(dec(x).ln() + Decimal("1e-50"))


def sqrt_upper(x):
    return up(dec(x).sqrt() + Decimal("1e-50"))


def eb_ucb(mean, var, n, R, delta):
    """One-sided Maurer-Pontil Thm 4 scaled to [0, R]: E <= mean + sqrt(2 V ln(2/d)/n) + 7 R ln(2/d) / (3(n-1))."""
    lg = ln_upper(2 / delta)
    half = sqrt_upper(2 * var * lg / n) + 7 * R * lg / (3 * (n - 1))
    return mean + half, half


def delta_phi(m, S_, e):
    """Copied from research/frontier_probe_20261021/p2_window_constant.py (unchanged logic)."""
    A2 = m * (S_ - m)
    lo, hi = F(0), F(1)
    for _ in range(200):
        mid = (lo + hi) / 2
        lhs_lin = mid * F(math.sqrt(float(A2)) * (1 + 1e-15))  # outward
        if lhs_lin + S_ * mid * mid / 4 + READOUT <= e:
            lo = mid
        else:
            hi = mid
    return lo


def main():
    eb = load("eb_sample")
    n = int(eb["n"])
    # exact rational mean / unbiased variance from the saved fsum totals
    s1, s2 = F(eb["sum"]), F(eb["sum_sq"])
    mean = s1 / n
    var = (s2 - s1 * s1 / n) / (n - 1)
    assert 0 <= eb["min"] and eb["max"] <= float(R_RAW) and F(eb["range_upper"]) <= R_RAW
    ucb, half = eb_ucb(mean + FLOAT_SLACK, var, n, R_RAW, DELTA_U)

    a2a = load("a2a_summary")
    assert a2a["all_checks_pass"] is True
    bias = F(*a2a["cases"]["B8x52"]["certified_total_upper_rounded_up_2^-64"])
    m_cert = ucb + bias
    assert m_cert <= S / 2

    price = F(str(load("c1")["port_check"]["B8x52"]["price"]))
    m_old = price + L1_OLD

    # window constant c (certified; delta = 3/1000 with the part-4 budget), from P2 run002
    p2 = load("p2_window")
    key = "B8x52|0.001|0.45eps|8192/211|price+L1|with_impl_budget|fail 3/1000"
    c = F(str(p2["k"][key]["c"]))
    sig_over_e = F(str(load("sigma")["cases"]["B8x52"]["sigma_q"])) / E_STAT

    def k_and_M(m):
        D = delta_phi(m, S, E_STAT)
        N = math.ceil(c / D)
        k = F(N) / sig_over_e
        M = k * 10 * sig_over_e * D_EFF * T_LAYER / T_C
        return dict(m=float(m), Delta=float(D), N_calls=N, k=float(k), M=float(M))

    at_old, at_cert = k_and_M(m_old), k_and_M(m_cert)
    assert at_old["N_calls"] == p2["k"][key]["N_calls"], (at_old, p2["k"][key]["N_calls"])

    # cross-check (mod): saved C09 preintegrated sample, R = 17.30 from P1 (float-evaluated analytic bound)
    c09 = load("c09_saved")["main"]
    ucb_pre, half_pre = eb_ucb(F(c09["mean"]), F(c09["var"]), int(c09["n"]), F("17.30"), DELTA_U)

    covered = m_cert <= m_old
    cert = dict(
        meta=dict(script="research/claim_debts_20261022/u1/u1_certificate.py", python=sys.version,
                  flags=dict(isolated=sys.flags.isolated, no_site=sys.flags.no_site),
                  inputs={k: v for k, v in IN.items()}, inputs_sha256={k: sha(v) for k, v in IN.items()},
                  rigour="R1 (exact/outward arithmetic; independent recompute in u1_independent.py); NOT R2"),
        statement="With probability >= 1 - delta_U over the classical sample (fixed before any quantum run): "
                  "E[g] = E[Y_N] <= m_cert.",
        delta_U=str(DELTA_U),
        failure_share="delta_U = 1e-4 is charged to the C03 failure union, taken from the 0.007 physical share "
                      "(physical becomes 0.0069); the window estimator keeps its 0.003",
        sample=dict(n=n, mean=float(mean), var_unbiased=float(var), min=eb["min"], max=eb["max"],
                    range_used=str(R_RAW), float_slack=str(FLOAT_SLACK)),
        eb_half_width=float(half), ucb_EY=[str(ucb.numerator), str(ucb.denominator)], ucb_EY_float=float(ucb),
        a2a_bias=[str(bias.numerator), str(bias.denominator)], a2a_bias_float=float(bias),
        m_cert=[str(m_cert.numerator), str(m_cert.denominator)], m_cert_float=float(m_cert),
        m_cert_display_up=str(Decimal(m_cert.numerator) / Decimal(m_cert.denominator)),
        p2_assumed_m=dict(value=float(m_old), form="uncertified RQMC price %.13f + B4x12 L1 0.045202052" % price),
        p2_assumption_covered=covered, margin_to_p2_m=float(m_old - m_cert),
        window_class=dict(c=float(c), S="8192/211", e=float(E_STAT), sigma_over_e=float(sig_over_e),
                          at_p2_m=at_old, at_m_cert=at_cert,
                          k_certified_premise=at_old["k"] if covered else at_cert["k"],
                          note=("m_U only needs to upper-bound E[g]; since m_cert <= the P2 value and sqrt(m(S-m)) is "
                                "increasing on [0, S/2], P2's k = %.4f is valid with the certified premise "
                                "(the tighter m_cert would give k = %.4f)" % (at_old["k"], at_cert["k"])) if covered
                          else ("m_cert exceeds the P2 value, so P2's k = %.4f is not covered; the certified premise "
                                "gives k = %.4f" % (at_old["k"], at_cert["k"]))),
        M_inputs=dict(D_eff=float(D_EFF), t_layer=float(T_LAYER), T_C=float(T_C)),
        crosscheck_preint_C09=dict(n=int(c09["n"]), mean=c09["mean"], ucb=float(ucb_pre), half=float(half_pre),
                                   m_with_bias=float(ucb_pre + bias),
                                   label="mod (preintegrated estimand; R = 17.30 from a float-evaluated analytic "
                                         "bound; kernel equality to E[Y|y] in float64)"),
        labels=dict(sample="meas (PRNG iid-ness assm)", range="analytic (A <= max_j B_j < 140 on survival)",
                    bias="cert R1 (A2a)", m_cert="cert R1, conditional on the PRNG iid assumption"),
    )
    with open(os.path.join(OUT, "u1_certificate.json"), "x", encoding="utf-8") as f:
        json.dump(cert, f, indent=1)
    print(json.dumps({k: cert[k] for k in ("m_cert_float", "ucb_EY_float", "eb_half_width", "a2a_bias_float",
                                           "p2_assumption_covered", "margin_to_p2_m")}, indent=1))
    print(json.dumps(cert["window_class"], indent=1))
    print(json.dumps(cert["crosscheck_preint_C09"], indent=1))


if __name__ == "__main__":
    main()
