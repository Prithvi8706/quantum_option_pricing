"""A2a clip-split bias certificate (R1), primary path. Exact rationals (fractions) only.

Re-bounds the certified A02 native financial bridge (run002) with the native stock
lower-clip event C split out of the barrier band:

    |E Y_N - E Y_cont| <= H_price + zeta0 + 40 * (P_fin(C) + sum_j P_H(band0_j))

zeta0 and band0 are the certified chains with the clamp leak ell replaced by the final
shift floor beta (valid on C^c). P_fin(C) is a Bernstein bound under the hybrid law H
(native radius Rhat at midpoint quantiles, ideal midpoint angle), with
E[Rhat^2] <= 2 + DS*B^2 from the pinned squared-radius KS distance.

Run from the worktree root:
  ../../../.context/frontier_t0_env/Scripts/python.exe -I -S -B research/claim_debts_20261022/a2a/clip_split_certificate.py run001
"""
import hashlib
import json
import sys
from fractions import Fraction as F
from math import isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BRIDGE = ROOT / "results/limitation_program_20261001/A02_BM_native_financial_bridge_run002"
POLAR = ROOT / "results/limitation_program_20261001/A02_polar_cdf_bv_run003"
OUT = ROOT / "results/claim_debts_20261022/a2a"
INPUTS = {
    "bands": BRIDGE / "closed_barrier_bands.json",
    "smooth": BRIDGE / "smooth_payoff_bounds.json",
    "complete": BRIDGE / "complete_financial_bounds.json",
    "stocks": BRIDGE / "stock_exponential_envelopes.json",
    "prefixes": BRIDGE / "raw_log_prefix_envelopes.json",
    "radius": POLAR / "log_radius_envelope.json",
    "hybrid": POLAR / "ideal_hybrid_bounds.json",
    "bridge_summary": BRIDGE / "summary.json",
}
CASES = {"B4x12": (4, 12, 30), "B8x52": (8, 52, 234)}
Q, N = 1 << 40, 1 << 32
EPS = F(1, Q)
TARGET = F(11, 20000)  # 0.55 * eps at eps = $0.001
CAP = 40


def ex(v):
    assert type(v) is list and len(v) == 2 and v[1] > 0
    return F(v[0], v[1])


def enc(x):
    x = F(x)
    return {"exact": [x.numerator, x.denominator], "float": float(x)}


def sqrt_lo(q, bits=256):
    q = F(q)
    return F(isqrt((q.numerator << (2 * bits)) // q.denominator), 1 << bits)


def sqrt_hi(q, bits=256):
    return sqrt_lo(q, bits) + F(1, 1 << bits)


def atan_bounds(x, terms):
    """Alternating series; partial sums ending on + are upper, on - are lower."""
    s, out = F(0), []
    for k in range(terms):
        s += (-1) ** k * x ** (2 * k + 1) / (2 * k + 1)
        out.append(s)
    return min(out[-1], out[-2]), max(out[-1], out[-2])


def pi_bounds():
    a_lo, a_hi = atan_bounds(F(1, 5), 40)
    b_lo, b_hi = atan_bounds(F(1, 239), 20)
    return 16 * a_lo - 4 * b_hi, 16 * a_hi - 4 * b_lo


def exp_lower(x, terms=400):
    """x >= 0: every Taylor term is positive, so a partial sum is a lower bound."""
    assert x >= 0
    s, t = F(0), F(1)
    for k in range(terms):
        s += t
        t = t * x / (k + 1)
    return s


def exp_upper(x, K=80):
    """0 <= x < K+2: Taylor partial sum plus geometric tail bound."""
    assert 0 <= x < K + 2
    s, t = F(0), F(1)
    for k in range(K + 1):
        s += t
        t = t * x / (k + 1)
    return s + t / (1 - x / (K + 2))


def round_down(x, bits=40):
    x = F(x)
    return F((x.numerator << bits) // x.denominator, 1 << bits)


def round_up(x, bits=40):
    return -round_down(-F(x), bits)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(run):
    sys.set_int_max_str_digits(0)
    out = OUT / run
    out.mkdir(parents=True, exist_ok=False)
    data = {k: json.loads(p.read_text()) for k, p in INPUTS.items()}
    pi_lo, pi_hi = pi_bounds()
    assert F(314159265358979, 10**14) < pi_lo < pi_hi < F(314159265358980, 10**14)
    # log(100) lower bound: exp_upper(q) <= 100 implies log 100 >= q.
    log100_lo = F(46051, 10000)
    assert exp_upper(log100_lo) <= 100
    B = ex(data["radius"]["internal_radius_upper"])
    DS = ex(data["radius"]["squared_radius_KS_upper"])
    second_moment_hi = 2 + DS * B * B  # E_H[Rhat^2] <= 2 + DS*B^2 (KS over [0, B^2])
    report = {}
    for case, (na, nt, pairs) in CASES.items():
        bands = data["bands"]["cases"][case]
        smooth = data["smooth"]["cases"][case]
        comp = data["complete"]["cases"][case]
        stock = data["stocks"]["cases"][case]
        pref = data["prefixes"]["cases"][case]
        hyb = data["hybrid"]["cases"][case]
        beta, ell = ex(bands["beta_upper"]), ex(bands["ell_upper"])
        assert beta == EPS and ell > beta
        L = F(stock["lower_clamp_raw"], Q)
        assert ex(bands["decoded_lower_clamp"]) == L

        # --- H_price: pinned identity, recomputed
        H_price = ex(comp["pinned_primary_hybrid_price_upper"])
        C_up = ex(hyb["exact_cap_enclosure"][1])
        assert H_price == pairs * (4 * C_up * DS + C_up * F(nt + 1, N))

        # --- zeta: reproduce certified exactly with ell, then ell -> beta
        d_hat = F(smooth["actual_discount_literal"], Q)
        avg_lit_err = ex(smooth["exact_average_literal_error"])
        disc_err = ex(smooth["discount_literal_error_upper"])

        def zeta(leak):
            errs = [
                140 * max(1 - ex(r["a_lower"]), ex(r["b_upper"]) - 1) + max(beta, leak)
                for r in bands["dates"]
            ]
            avg = sum(errs, F(0)) / nt + na * nt * 140 * avg_lit_err + EPS
            return d_hat * avg + 40 * disc_err + EPS

        zeta_cert = ex(smooth["smooth_discounted_payoff_error_upper"])
        assert zeta(ell) == zeta_cert, "zeta reproduction"
        zeta0 = zeta(beta)

        # --- bands: log(U/L) <= U/L - 1; sqrt(2 pi var) >= sqrt_lo(2 pi_lo var)
        def band(row, leak):
            a, b = ex(row["a_lower"]), ex(row["b_upper"])
            lo_b, up_b = F(140 - leak) / b, F(140 + beta + EPS) / a
            var = F(9 * row["elapsed_dates"], 250 * nt)
            assert ex(row["exact_continuous_common_variance"]) == var
            g = min(F(1), (up_b / lo_b - 1) / sqrt_lo(2 * pi_lo * var))
            allow = ex(row["pair_law_allowance"])
            return g, min(F(1), g + allow)

        rows, sw_cert_re, sw0 = [], F(0), F(0)
        for r in bands["dates"]:
            g_re, h_re = band(r, ell)
            g_c = ex(r["gaussian_closed_band_probability_upper"])
            assert g_c <= g_re <= g_c * (1 + F(1, 10**5)), "band reproduction (outward)"
            g0, h0 = band(r, beta)
            sw_cert_re += h_re
            sw0 += h0
            rows.append({"date": r["date"], "gaussian_cert": float(g_c), "gaussian_recomputed_with_ell": float(g_re),
                         "gaussian_noclip": float(g0), "pair_law_allowance": float(ex(r["pair_law_allowance"])),
                         "hybrid_noclip": float(h0)})
        sw_cert_re, sw0 = min(F(1), sw_cert_re), min(F(1), sw0)
        sw_cert = ex(bands["hybrid_any_switch_probability_upper"])
        assert sw_cert <= sw_cert_re
        total_cert = ex(comp["continuous_to_native_dollars_upper"])
        assert total_cert == H_price + zeta_cert + CAP * sw_cert

        # --- P_fin(C): Bernstein under H, union over sites that can clip
        a2b2 = F(9, 100 * nt)  # a^2 + b^2 with a^2 = 9/(250nt), b^2 = 27/(500nt)
        M_hi = B * sqrt_hi(2 * F(27, 500 * nt))  # any two coordinates in one pair: <= sqrt(2) * max(a, b)
        mu = F(-3, 200 * nt)
        sites, PC, site_rows = 0, F(0), []
        for p in pref["prefixes"]:
            j, lam = p["elapsed_dates"], ex(p["lambda_upper"])
            clipable = [k for k, bd in enumerate(p["actual_raw_log_bounds"]) if bd[0] < stock["lower_clamp_raw"]]
            if not clipable:
                site_rows.append({"elapsed_dates": j, "clipable_sites": 0})
                continue
            s_lo = log100_lo + j * mu - L - lam
            assert s_lo > 0
            V_hi = second_moment_hi / 2 * j * a2b2
            E_lo = round_down(s_lo * s_lo / (2 * (V_hi + M_hi * s_lo / 3)))
            p_site = round_up(1 / exp_lower(E_lo), 400)
            sites += len(clipable)
            PC += len(clipable) * p_site
            site_rows.append({"elapsed_dates": j, "clipable_sites": len(clipable), "s_lower": float(s_lo),
                              "variance_upper": float(V_hi), "bernstein_exponent_lower": float(E_lo),
                              "per_site_probability_upper_log10": float(-E_lo) / 2.302585092994046})
        PC = min(F(1), round_up(PC, 400))  # outward rounding keeps the stored rational small
        total0 = H_price + zeta0 + CAP * min(F(1), PC + sw0)
        report[case] = {
            "H_price": enc(H_price),
            "zeta_certified": enc(zeta_cert),
            "zeta_noclip": enc(zeta0),
            "switch_certified": enc(sw_cert),
            "switch_recomputed_with_ell_outward": enc(sw_cert_re),
            "switch_noclip": enc(sw0),
            "P_fin_C_upper": enc(PC),
            "clipable_sites": sites,
            "total_certified_run002": enc(total_cert),
            "total_clip_split": enc(total0),
            "target_0p55eps": enc(TARGET),
            "meets_target": total0 <= TARGET,
            "dates": rows,
            "sites": site_rows,
        }
        # coarse log10 display of PC (digit-count difference) without float underflow
        report[case]["P_fin_C_upper_log10_approx"] = (len(str(PC.numerator)) - len(str(PC.denominator))) if PC else None
    doc = {
        "schema": "a2a-clip-split-certificate-v1",
        "rigour": "R1 (primary path; independent recompute in independent.json)",
        "labels": "mod from cert inputs; every bound exact rational or outward",
        "constants": {"B_internal_radius_upper": enc(B), "DS_squared_radius_KS_upper": enc(DS),
                      "E_H_Rhat2_upper": enc(second_moment_hi), "pi_lower": enc(pi_lo), "log100_lower": enc(log100_lo),
                      "N_angle_grid": N, "cap": CAP},
        "method": {
            "split": "|Y_N - Y_I| <= 40*1_C + zeta0*1_{C^c, no switch} + 40*1_{C^c, switch}; C^c and switch_j imply ideal basket in band0_j = [(140-beta)/b_j, (140+beta+eps)/a_j]",
            "band_probability": "certified Gaussian anti-concentration log(U/L)/sqrt(2 pi var) with log(U/L) <= U/L - 1, plus the unchanged whole-pair allowance",
            "clip_event": "C subset union over clipable sites of {x_I <= L + lambda_j}; x_I = log 100 + j mu + sum of independent zero-mean pair terms under H",
            "tail": "Bernstein: P(sum X >= s) <= exp(-s^2 / (2 (V + M s / 3))), X_k = -Y_k, |Y_k| <= M, E Y_k = 0 and E Y_k^2 = E[Rhat^2] |c_k|^2 / 2 exactly on the N-point midpoint angle grid",
        },
        "inputs_sha256": {str(p.relative_to(ROOT)).replace("\\", "/"): sha(p) for p in INPUTS.values()},
        "interpreter": sys.version,
        "cases": report,
    }
    with open(out / "certificate.json", "x") as fh:
        json.dump(doc, fh, indent=1)
    for case in CASES:
        r = report[case]
        print(case, "total", r["total_clip_split"]["float"], "meets", r["meets_target"], "P_C log10 <=",
              r["P_fin_C_upper_log10_approx"], "sites", r["clipable_sites"], "zeta0", r["zeta_noclip"]["float"],
              "sw0", r["switch_noclip"]["float"])


if __name__ == "__main__":
    main(sys.argv[1])
