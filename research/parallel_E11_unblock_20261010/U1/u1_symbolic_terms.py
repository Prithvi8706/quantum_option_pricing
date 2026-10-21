"""U1 symbolic helper (design only, parallel E11 unblock 2026-10-10).

Emits exact term tables for two candidate continuous B4x12 price UPPER-bound routes
(ideal GBM law, original parameters) and checks exact pure-constant identities:

  R7  second-moment (Lo/Scarf) route:
        E[Y] <= d*E[(A-K)^+] <= (d/2)*(beta + sqrt(V + beta^2)),
        beta = E[A] - K,  V = Var(A),  everything a polynomial in q = exp(1/2000).
  R1  vanilla-domination (convexity) route:
        E[Y] <= (d/12) * sum_j E[(S(t_j) - K)^+], d1 = sqrt(t)/4, d2 = -sqrt(t)/20.

It NEVER evaluates exp, the normal CDF, a square root of a price quantity, or either
bound. The only evaluations are (i) polynomials at q = 1 (degenerate sanity), (ii) exact
first-order Taylor coefficients labelled screen-only, and (iii) an independent re-check
of the saved-schedule halving threshold m* (a pure schedule constant, not a price bound),
using the saved Machin pi enclosure of E07 (read only).

Writes one JSON with exclusive create; never overwrites. Usage:
    python -I -S -B u1_symbolic_terms.py <repo_root> <out_json>
"""
import json
import sys
from fractions import Fraction as F
from math import isqrt
from pathlib import Path

# Original B4x12 contract (G0_run003/B4x12_task.json; barrier_oracle_depth.py line 33),
# as the exact contractual decimals used by the #42 ideal law (run001.md: squares 3/1000, 9/2000).
SIGMA, RHO, RATE, T, S0, K, H = F(3, 10), F(2, 5), F(3, 100), F(1), F(100), F(100), F(140)
NA, NT = 4, 12
UNIT = F(1, 2000)  # q = exp(UNIT); every exponent below is an integer multiple of UNIT

CHECKS = {}


def check(name, cond):
    CHECKS[name] = bool(cond)
    if not cond:
        raise SystemExit("check failed: " + name)


def as_int_units(x):
    u = x / UNIT
    check("integral_exponent_" + str(x), u.denominator == 1)
    return int(u)


def padd(p, k, c):
    p[k] = p.get(k, F(0)) + c
    if p[k] == 0:
        del p[k]


def peval(p, q):
    return sum((c * q ** k for k, c in p.items()), F(0))


def ser(p):
    return {str(k): str(c) for k, c in sorted(p.items())}


def main(root, out):
    dt = T / NT
    t = [F(j, NT) for j in range(1, NT + 1)]
    mu = RATE - SIGMA ** 2 / 2
    a2, b2 = SIGMA ** 2 * RHO * dt, SIGMA ** 2 * (1 - RHO) * dt
    check("drift_mu_is_-3/200", mu == F(-3, 200))
    check("per_date_drift_is_-1/800", mu * dt == F(-1, 800))
    check("common_variance_per_date_3/1000_matches_run001", a2 == F(3, 1000))
    check("idio_variance_per_date_9/2000_matches_run001", b2 == F(9, 2000))
    check("S0_equals_K_so_log_moneyness_zero", S0 == K)

    # R1 coefficients: d1 = (r + s^2/2) sqrt(t)/s, d2 = (r - s^2/2) sqrt(t)/s since ln(S0/K)=0
    c1, c2 = (RATE + SIGMA ** 2 / 2) / SIGMA, (RATE - SIGMA ** 2 / 2) / SIGMA
    check("R1_d1_coeff_1/4", c1 == F(1, 4))
    check("R1_d2_coeff_-1/20", c2 == F(-1, 20))
    disc_units = as_int_units(RATE * T)  # d = q^-60
    r_units = [as_int_units(RATE * tj) for tj in t]  # 5j
    R1_terms = [dict(j=j + 1, t=str(tj), forward_factor_q_exponent=r_units[j] - disc_units,
                     discount_q_exponent=-disc_units, N_plus_argument="sqrt(%s)*1/4" % tj,
                     N_minus_argument="-sqrt(%s)*1/20" % tj)
                for j, tj in enumerate(t)]

    # R7: beta(q) = E[A]-K = (S0/NT) sum_j (q^{5j} - 1)
    beta = {}
    for j in range(NT):
        padd(beta, r_units[j], S0 / NT)
        padd(beta, 0, -S0 / NT)

    # V(q) grouped form: (S0^2/NT^2) sum_{j,l} q^{5(j+l)} [ (1/NA)(q^{15m}-1) + (1-1/NA)(q^{6m}-1) ]
    V_grouped, structured = {}, []
    for j in range(NT):
        for l in range(NT):
            m = min(j, l)
            base = r_units[j] + r_units[l]
            same = as_int_units(SIGMA ** 2 * t[m])
            cross = as_int_units(SIGMA ** 2 * RHO * t[m])
            for w, e in ((F(1, NA), same), (1 - F(1, NA), cross)):
                coef = S0 ** 2 / NT ** 2 * w
                check("structured_term_positive", coef > 0 and e > 0)
                structured.append((str(coef), base, e))  # coef * q^base * (q^e - 1)
                padd(V_grouped, base + e, coef)
                padd(V_grouped, base, -coef)

    # V(q) brute force over the 48x48 covariance, independent of the 1/NA grouping
    V_brute = {}
    n = NA * NT
    for i in range(NA):
        for j in range(NT):
            for k in range(NA):
                for l in range(NT):
                    m = min(j, l)
                    corr = F(1) if i == k else RHO
                    e = as_int_units(SIGMA ** 2 * corr * t[m])
                    base = r_units[j] + r_units[l]
                    padd(V_brute, base + e, S0 ** 2 / n ** 2)
                    padd(V_brute, base, -S0 ** 2 / n ** 2)
    check("V_grouped_equals_48x48_bruteforce", V_grouped == V_brute)
    check("beta_at_q1_zero", peval(beta, F(1)) == 0)
    check("V_at_q1_zero", peval(V_grouped, F(1)) == 0)
    smin = sum(min(j, l) for j in range(1, NT + 1) for l in range(1, NT + 1))
    check("sum_min_jl_650", smin == 650 == NT * (NT + 1) * (2 * NT + 1) // 6)
    max_exp = max(V_grouped)
    check("max_V_exponent_300_units", max_exp == 300)

    # screen-only first-order coefficients (d/dx at x=0 with q=e^x, times UNIT): NOT bounds
    beta1 = sum((c * k for k, c in beta.items()), F(0)) * UNIT
    V1 = sum((c * k for k, c in V_grouped.items()), F(0)) * UNIT
    check("beta1_is_13/8", beta1 == F(13, 8))
    check("V1_is_closed_form", V1 == S0 ** 2 * SIGMA ** 2 * (F(1, NA) + (1 - F(1, NA)) * RHO)
          * F(smin, NT ** 3))

    # independent re-check of the halving threshold m* at eps=1/100 (schedule constant only)
    sched = json.loads((Path(root) / "results/limitation_program_20261001/E07_schedule_run001/"
                        "schedule.json").read_text())
    (pn, pd), (qn, qd) = sched["pi_enclosure_exact"]
    pi_lo, pi_hi = F(pn, pd), F(qn, qd)
    check("pi_enclosure_ordered", F(3) < pi_lo < pi_hi < F(22, 7))
    delta = F(*sched["statistical_error_dollars_exact"])
    span, M = sched["normalization_span_dollars"], sched["M"]
    check("saved_schedule_eps_1/100", delta == F(9, 2000) and span == 64 and M == 65536)

    def m_star_inward(readout):
        Mp = M // 2
        R_lo = (delta - readout - span * pi_hi ** 2 / Mp ** 2) * Mp / (2 * pi_hi)
        check("R_in_(0,32)", 0 < R_lo < 32)
        X = 1024 - R_lo ** 2
        p = 128
        s_up = F(isqrt(X.numerator * 4 ** p // X.denominator) + 1, 2 ** p)
        check("outward_sqrt", s_up ** 2 >= X)
        return 32 - s_up

    m_ro, m_free = m_star_inward(F(1, 2 ** 39)), m_star_inward(F(0))

    res = dict(
        schema="u1-symbolic-terms-design-only-v1",
        design_only=True, bound_evaluated=False, exp_or_normal_cdf_evaluated=False,
        parameters=dict(sigma=str(SIGMA), rho=str(RHO), rate=str(RATE), maturity=str(T),
                        spot=str(S0), strike=str(K), barrier_strict=str(H), assets=NA,
                        dates=NT, times=[str(x) for x in t], weights="1/48",
                        discount="exp(-3/100) = q^-60", q="exp(1/2000)"),
        derived=dict(mu=str(mu), per_date_drift=str(mu * dt), a2=str(a2), b2=str(b2),
                     R1_d1_coeff=str(c1), R1_d2_coeff=str(c2)),
        R1_terms=R1_terms,
        R7_beta_poly_q=ser(beta),
        R7_V_poly_q=ser(V_grouped),
        R7_V_poly_term_count=len(V_grouped),
        R7_V_structured_term_count=len(structured),
        R7_V_structured_increasing_in_q_ge_1=True,
        screen_only_first_order_coefficients_not_bounds=dict(beta1=str(beta1), V1=str(V1)),
        halving_threshold_recheck_eps_1_100=dict(
            m_star_inward_with_readout_2pow_minus39=str(m_ro),
            m_star_inward_with_readout_decimal_floor_1e9=str(
                (m_ro.numerator * 10 ** 9 // m_ro.denominator)),
            m_star_inward_readout_free_decimal_floor_1e9=str(
                (m_free.numerator * 10 ** 9 // m_free.denominator)),
            note="schedule constant re-derivation, not a price bound; units 1e-9 USD"),
        checks=CHECKS,
    )
    with open(out, "x", encoding="utf-8", newline="\n") as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("ok", len(CHECKS), "checks; V terms", len(V_grouped), "; m* (1e-9 USD floor)",
          res["halving_threshold_recheck_eps_1_100"]["m_star_inward_with_readout_decimal_floor_1e9"])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
