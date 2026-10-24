"""A2a clip-split bias certificate (R1), independent path.

Different arithmetic and different tail inequality from clip_split_certificate.py:
- decimal interval arithmetic with directed rounding (prec 80), margins on ln/exp/sqrt;
- exact natural log for the band width (not U/L - 1), pi from a decimal Machin series;
- Bennett's inequality (not Bernstein) for the clip event;
- E_H[Rhat^2] <= 2 + eta from |Rhat_k^2 - S_k| <= eta and the midpoint rule for the convex
  -2 ln u (not the KS route);
- every term re-read from the raw JSONs and re-summed here.

Run from the worktree root:
  ../../../.context/frontier_t0_env/Scripts/python.exe -I -S -B research/claim_debts_20261022/a2a/independent_recompute.py run001
"""
import decimal
import hashlib
import json
import sys
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BRIDGE = ROOT / "results/limitation_program_20261001/A02_BM_native_financial_bridge_run002"
POLAR = ROOT / "results/limitation_program_20261001/A02_polar_cdf_bv_run003"
OUT = ROOT / "results/claim_debts_20261022/a2a"
FILES = [BRIDGE / n for n in ("closed_barrier_bands.json", "smooth_payoff_bounds.json",
                              "complete_financial_bounds.json", "stock_exponential_envelopes.json",
                              "raw_log_prefix_envelopes.json")] + [POLAR / "log_radius_envelope.json",
                                                                   POLAR / "ideal_hybrid_bounds.json"]
CASES = {"B4x12": (4, 12, 30), "B8x52": (8, 52, 234)}
PREC = 80
DN = decimal.Context(prec=PREC, rounding=decimal.ROUND_FLOOR, Emin=-10**8, Emax=10**8)
UP = decimal.Context(prec=PREC, rounding=decimal.ROUND_CEILING, Emin=-10**8, Emax=10**8)
NE = decimal.Context(prec=PREC + 10, rounding=decimal.ROUND_HALF_EVEN, Emin=-10**8, Emax=10**8)
REL = D(10) ** (-(PREC - 5))  # margin for half-even transcendental results


class I:
    """Closed interval [lo, hi] of Decimals with outward rounding."""

    def __init__(self, lo, hi=None):
        self.lo, self.hi = lo, (lo if hi is None else hi)
        assert self.lo <= self.hi

    @staticmethod
    def frac(num, den):
        return I(DN.divide(D(num), D(den)), UP.divide(D(num), D(den)))

    def __add__(s, o):
        o = o if isinstance(o, I) else I(D(o))
        return I(DN.add(s.lo, o.lo), UP.add(s.hi, o.hi))

    def __sub__(s, o):
        o = o if isinstance(o, I) else I(D(o))
        return I(DN.subtract(s.lo, o.hi), UP.subtract(s.hi, o.lo))

    def __mul__(s, o):
        o = o if isinstance(o, I) else I(D(o))
        ps = [(x, y) for x in (s.lo, s.hi) for y in (o.lo, o.hi)]
        return I(min(DN.multiply(x, y) for x, y in ps), max(UP.multiply(x, y) for x, y in ps))

    def __truediv__(s, o):
        o = o if isinstance(o, I) else I(D(o))
        assert o.lo > 0
        ps = [(x, y) for x in (s.lo, s.hi) for y in (o.lo, o.hi)]
        return I(min(DN.divide(x, y) for x, y in ps), max(UP.divide(x, y) for x, y in ps))

    def maxi(s, o):
        return I(max(s.lo, o.lo), max(s.hi, o.hi))


def widen(x):
    m = abs(x) * REL + D("1E-1000")
    return DN.subtract(x, m), UP.add(x, m)


def ln(x):
    assert x.lo > 0
    return I(widen(NE.ln(x.lo))[0], widen(NE.ln(x.hi))[1])


def exp(x):
    return I(widen(NE.exp(x.lo))[0], widen(NE.exp(x.hi))[1])


def sqrt(x):
    assert x.lo >= 0
    return I(widen(NE.sqrt(x.lo))[0], widen(NE.sqrt(x.hi))[1])


def pi():
    def atan_inv(n):  # atan(1/n), alternating; error < first omitted term
        x, s, k, t = NE.divide(1, n), D(0), 0, NE.divide(1, n)
        while t > D(10) ** (-(PREC + 8)):
            s = NE.add(s, t if k % 2 == 0 else -t)
            k += 1
            t = NE.divide(NE.power(x, 2 * k + 1), 2 * k + 1)
        return s
    v = NE.subtract(NE.multiply(16, atan_inv(5)), NE.multiply(4, atan_inv(239)))
    m = D(10) ** (-(PREC - 2))
    return I(DN.subtract(v, m), UP.add(v, m))


def X(v):
    return I.frac(v[0], v[1])


def main(run):
    sys.set_int_max_str_digits(0)
    out = OUT / run
    assert (out / "certificate.json").exists(), "primary path must run first"
    js = {p.name: json.loads(p.read_text()) for p in FILES}
    bands_all, smooth_all = js["closed_barrier_bands.json"], js["smooth_payoff_bounds.json"]
    comp_all, stock_all = js["complete_financial_bounds.json"], js["stock_exponential_envelopes.json"]
    pref_all, rad, hyb_all = js["raw_log_prefix_envelopes.json"], js["log_radius_envelope.json"], js["ideal_hybrid_bounds.json"]
    Q, N = 2 ** 40, 2 ** 32
    eps = I.frac(1, Q)
    PI = pi()
    B, DS, eta = X(rad["internal_radius_upper"]), X(rad["squared_radius_KS_upper"]), X(rad["square_error_eta_upper"])
    m2 = I(D(2)) + eta  # E_H[Rhat^2] <= mean_k S_k + eta <= 2 + eta (midpoint rule, -2 ln u convex)
    log100 = ln(I(D(100)))
    res = {}
    for case, (na, nt, pairs) in CASES.items():
        bands, smooth, comp = bands_all["cases"][case], smooth_all["cases"][case], comp_all["cases"][case]
        stock, pref, hyb = stock_all["cases"][case], pref_all["cases"][case], hyb_all["cases"][case]
        beta = X(bands["beta_upper"])
        lo_raw = stock["lower_clamp_raw"]
        L = I.frac(lo_raw, Q)
        # H_price from the pinned identity
        C = X(hyb["exact_cap_enclosure"][1])
        Hp = I(D(pairs)) * (I(D(4)) * C * DS + C * I.frac(nt + 1, N))
        Hj = X(comp["pinned_primary_hybrid_price_upper"])
        assert Hp.lo <= Hj.hi and Hj.lo <= Hp.hi
        # zeta with leak beta (C^c)
        errs = I(D(0))
        for r in bands["dates"]:
            a, b = X(r["a_lower"]), X(r["b_upper"])
            errs = errs + I(D(140)) * (I(D(1)) - a).maxi(b - I(D(1))) + beta
        avg = errs / I(D(nt)) + I(D(na * nt * 140)) * X(smooth["exact_average_literal_error"]) + eps
        zeta0 = I.frac(smooth["actual_discount_literal"], Q) * avg + I(D(40)) * X(smooth["discount_literal_error_upper"]) + eps
        # bands with leak beta, exact log
        sw0 = I(D(0))
        for r in bands["dates"]:
            a, b = X(r["a_lower"]), X(r["b_upper"])
            U = (I(D(140)) + beta + eps) / a
            Lb = (I(D(140)) - beta) / b
            var = I.frac(9 * r["elapsed_dates"], 250 * nt)
            g = ln(U / Lb) / sqrt(I(D(2)) * PI * var)
            h = g + X(r["pair_law_allowance"])
            sw0 = sw0 + I(min(h.lo, D(1)), min(h.hi, D(1)))
        # clip event: Bennett per clipable site
        a2b2 = I.frac(9, 100 * nt)
        M = B * sqrt(I(D(2)) * I.frac(27, 500 * nt))
        mu = I.frac(-3, 200 * nt)
        PC, nsites, worst = I(D(0)), 0, None
        for p in pref["prefixes"]:
            j, lam = p["elapsed_dates"], X(p["lambda_upper"])
            k = sum(1 for bd in p["actual_raw_log_bounds"] if bd[0] < lo_raw)
            if not k:
                continue
            s = log100 + I(D(j)) * mu - L - lam
            V = m2 / I(D(2)) * I(D(j)) * a2b2
            u_star = (I(M.hi) * I(s.lo) / I(V.hi)).lo
            one_u = I(D(1)) + I(u_star)
            hval = one_u * ln(one_u) - I(u_star)
            Elo = (I(V.hi) / (I(M.hi) * I(M.hi))).lo
            Elo = (I(Elo) * hval).lo
            assert Elo > 0
            p_site = exp(I(-Elo)).hi
            PC = PC + I(D(k)) * I(p_site)
            nsites += k
            worst = p_site if worst is None else max(worst, p_site)
        total = Hp + zeta0 + I(D(40)) * (PC + sw0)
        res[case] = {"H_price_upper": str(Hp.hi), "zeta_noclip_upper": str(zeta0.hi),
                     "switch_noclip_upper": str(sw0.hi), "P_fin_C_upper": str(PC.hi),
                     "worst_site_probability_upper": str(worst) if worst is not None else None,
                     "clipable_sites": nsites, "total_upper": str(total.hi), "total_lower_of_upper": str(total.lo),
                     "meets_target_0p55eps": total.hi <= D("0.00055")}
    doc = {"schema": "a2a-clip-split-independent-v1",
           "rigour": "R1 independent recompute (decimal intervals, Bennett, midpoint-Jensen second moment, exact log)",
           "inputs_sha256": {str(p.relative_to(ROOT)).replace("\\", "/"): hashlib.sha256(p.read_bytes()).hexdigest() for p in FILES},
           "interpreter": sys.version, "decimal_precision": PREC, "E_H_Rhat2_upper": str(m2.hi), "cases": res}
    with open(out / "independent.json", "x") as fh:
        json.dump(doc, fh, indent=1)
    for c, r in res.items():
        print(c, r["total_upper"][:22], "P_C", r["P_fin_C_upper"][:12], "sites", r["clipable_sites"], "meets", r["meets_target_0p55eps"])


if __name__ == "__main__":
    main(sys.argv[1])
