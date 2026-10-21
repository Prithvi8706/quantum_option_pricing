"""N1-headline step 2a: exact-rational k_eff per cell from the E07 rule, recomputed independently.

Different path from E07/W0: pi is enclosed with the BBP series (not Machin), M is found from the
closed-form root of e*M^2 - S*pi*M - S*pi^2 = 0 then rounded up to a power of two (not by doubling),
and the majority tail uses the exact elementary failure 1 - 8/pi_hi^2 (no 2^-40 rounding grid).

Rule (Brassard-Hoyer-Mosca-Tapp 2002, Thm 12 with k=1): |a~ - a| <= 2 pi sqrt(a(1-a))/M + pi^2/M^2
<= pi/M + pi^2/M^2 in amplitude units with success >= 8/pi^2; dollars = span * amplitude; span $64;
statistical error e = split*eps; failure 3/1000 (E07 protocol estimator allowance); odd median reps.
k_eff = controlled Grover calls / (sigma_q / e), sigma_q measured (sigma_dev.json, 2^20 paths).

Run: .context/frontier_t0_env/Scripts/python.exe -I -S -B research/plan110_n1/headline/e07_keff.py
"""
import hashlib
import json
import sys
from fractions import Fraction
from math import comb, isqrt

ROOT = "C:/Users/prith/quantum_option_pricing/"
OUT = ROOT + "results/plan110_n1/headline/"
SIGMA_DEV = ROOT + "results/frontier_classical_20261001/sigma_dev/sigma_dev.json"
E07_SCHEDULE = ROOT + "results/limitation_program_20261001/E07_schedule_run001/schedule.json"


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def row(d):
    with open(OUT + "rows.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(d, sort_keys=True) + "\n")


def pi_bbp(terms=30):
    """Bailey-Borwein-Plouffe: every term positive; tail after K terms < 16^-K * 4/(8K+1) * 16/15."""
    s = Fraction(0)
    for k in range(terms):
        s += Fraction(1, 16**k) * (Fraction(4, 8 * k + 1) - Fraction(2, 8 * k + 4)
                                   - Fraction(1, 8 * k + 5) - Fraction(1, 8 * k + 6))
    tail = Fraction(1, 16**terms) * Fraction(4, 8 * terms + 1) * Fraction(16, 15)
    return s, s + tail


def min_M_real(span, err, pi):
    """Smallest real M with span*(pi/M + pi^2/M^2) <= err, as an exact upper rational via isqrt."""
    a, b, c = err, span * pi, span * pi * pi  # a M^2 - b M - c >= 0
    disc = b * b + 4 * a * c
    num, den = disc.numerator, disc.denominator
    root_hi = Fraction(isqrt(num * den) + 1, den)  # >= sqrt(disc)
    return (b + root_hi) / (2 * a)


def error_ok(span, err, pi, M):
    return span * (pi / M + pi * pi / (M * M)) <= err


def majority_tail(r, q):
    return sum(comb(r, j) * q**j * (1 - q) ** (r - j) for j in range(r // 2 + 1, r + 1))


def schedule(span, err, fail, pi_lo, pi_hi, dyadic=True):
    m_real = min_M_real(span, err, pi_hi)
    if dyadic:
        M = 1
        while M < m_real:
            M <<= 1
    else:
        M = -(-m_real.numerator // m_real.denominator)
    while M > 1 and error_ok(span, err, pi_hi, M - (M // 2 if dyadic else 1)):
        M = M - (M // 2 if dyadic else 1)  # guard: never larger than needed
    assert error_ok(span, err, pi_hi, M)
    q = 1 - Fraction(8) / (pi_hi * pi_hi)  # worst elementary failure
    r = 1
    while majority_tail(r, q) > fail:
        r += 2
    return dict(M=M, reps=r, calls=r * (M - 1), q_upper=float(q),
                tail=float(majority_tail(r, q)))


def main():
    sig = json.load(open(SIGMA_DEV))["cases"]
    pi_lo, pi_hi = pi_bbp()
    assert pi_lo < Fraction(314159265358979, 10**14) + Fraction(1, 10**14) and pi_hi > Fraction(314159265358979, 10**14)
    span, fail = Fraction(64), Fraction(3, 1000)
    eps_list = [Fraction(1, 10), Fraction(3, 100), Fraction(1, 100), Fraction(1, 1000)]
    out = dict(meta=dict(script="research/plan110_n1/headline/e07_keff.py", python=sys.version,
                         inputs_sha256={"sigma_dev.json": sha(SIGMA_DEV), "E07 schedule.json": sha(E07_SCHEDULE)},
                         pi_enclosure=[float(pi_lo), float(pi_hi)], pi_method="BBP 30 terms + tail bound",
                         span=64, failure="3/1000",
                         labels="schedule arithmetic modelled-exact; sigma measured; neutral direction"),
               cells=[])
    saved = json.load(open(E07_SCHEDULE))
    for split_name, split in (("0.45eps", Fraction(9, 20)), ("eps", Fraction(1))):
        for eps in eps_list:
            e = split * eps
            for dy in (True, False):
                s = schedule(span, e, fail, pi_lo, pi_hi, dyadic=dy)
                for case in ("B4x12", "B8x52"):
                    sigma = sig[case]["sigma_q"]
                    s_over_e = sigma / float(e)
                    k = s["calls"] / s_over_e
                    c = dict(case=case, eps=float(eps), split=split_name, e=[e.numerator, e.denominator],
                             M_rule="dyadic (E07)" if dy else "non-dyadic integer M (conditional credit)",
                             M=s["M"], reps=s["reps"], calls=s["calls"], sigma_q=sigma,
                             sigma_over_e=s_over_e, k_eff=k,
                             label="modelled (exact rational schedule) x measured sigma", direction="neutral")
                    out["cells"].append(c)
                    row(dict(ws="headline", step="2a_keff", **c))
    # reproduction of the saved certificate at eps = 0.01
    rep = [c for c in out["cells"] if c["eps"] == 0.01 and c["split"] == "0.45eps" and c["M_rule"].startswith("dyadic")]
    sv = dict(M=saved.get("M"), reps=saved.get("repetitions"), calls=saved.get("controlled_grover_calls"))
    ok = all(c["calls"] == 983025 and c["M"] == 65536 and c["reps"] == 15 for c in rep) and sv["calls"] == 983025
    out["reproduction_eps0.01"] = dict(saved=sv, recomputed=dict(M=rep[0]["M"], reps=rep[0]["reps"], calls=rep[0]["calls"]),
                                       match=ok, label="measured (saved certificate) vs modelled (this script)")
    row(dict(ws="headline", step="2a_reproduce_983025", match=ok, saved=sv))
    with open(OUT + "keff.json", "x", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    for c in out["cells"]:
        if c["M_rule"].startswith("dyadic"):
            print(c["case"], c["eps"], c["split"], c["M"], c["reps"], c["calls"], round(c["k_eff"], 3))
    print("reproduce 983,025:", ok)


if __name__ == "__main__":
    main()
