"""P2 extension: replace the U1 mean credit (an uncertified classical orientation price) by a quantum-only first stage.

Stage 1: the certified Kaiser-window estimator with failure delta1 and phase half-width D1 and no mean credit gives
a_hat with |a_hat - a| <= D1/2 + D1^2/4 (worst case over a). Its upper bound a_U = a_hat + that error satisfies
a <= a_U <= a + 2 (D1/2 + D1^2/4) with probability >= 1 - delta1.
Stage 2: the same estimator with failure delta2 = 0.003 - delta1 and the WS-k Delta rule with mean bound
m_U = S a_U (needs m_U <= S/2): sqrt(m_U (S - m_U)) D2 + S D2^2 / 4 + 2^-39 <= e.
Calls: N1 = ceil(c(delta1)/D1) + N2 = ceil(c(delta2)/D2(m_U)), with the worst case over stage-1 outcomes,
m_U = m + 2 S (D1/2 + D1^2/4), m the true mean (the task's price; the U1 row also evaluates k at the task's mean,
via price + L1). D1 is optimised. Union bound: total estimator failure delta1 + delta2 = 0.003.
c(delta) values are certified with the P2 machinery (p2_window_constant.certify), every N >= 800 (stage 1's N1 is
checked against N0 = 800; if smaller, N1 is raised to 800).
Run (repo root): .context/frontier_t0_env/Scripts/python.exe -I -S -B research/frontier_probe_20261021/p2c_self_mean.py
"""
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import p2_window_constant as p2  # noqa: E402

ROOT = HERE.parents[1]
OUT = ROOT / "results" / "frontier_probe_20261021" / "p2" / "run003_self_mean"
DELTA34 = Fraction(4, 10 ** 6)  # parts 3-4 reserve, as P2 run002


def certified_c(delta):
    """Pick beta by the float exploration, certify c at delta - DELTA34 (gamma = 0, the better family)."""
    gamma = Fraction(0)
    best = min((p2.float_c(b / 100, 0.0, float(delta)), b) for b in range(250, 720, 10))
    bb = best[1]
    best = min((p2.float_c(b / 100, 0.0, float(delta)), b) for b in range(bb - 10, bb + 11, 2))
    assert best[0] < 7.9, ("c bracket", delta, best)
    beta_str = f"{best[1] / 100:.2f}"
    Itot_hi = 2 * p2.PI_HI * p2.int_phi_sq_upper(Fraction(beta_str) ** 2, gamma)
    c, info = p2.certify(beta_str, gamma, delta - DELTA34, Itot_hi, best[0] - 0.05, best[0] + 0.15, Fraction(1, 1000))
    return float(c), beta_str, str(info["lambda_lower_N0"])


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    sig = p2.load(p2.IN["sigma"])["cases"]
    price = {c: Fraction(str(p2.load(p2.IN["c1"])["port_check"][c]["price"])) for c in ("B4x12", "B8x52")}
    S = p2.S_SPAN["8192/211"]
    res = dict(meta=dict(script="research/frontier_probe_20261021/p2c_self_mean.py", python=sys.version,
                         inputs_sha256={k: hashlib.sha256(Path(v).read_bytes()).hexdigest() for k, v in p2.IN.items()},
                         delta34=str(DELTA34)), constants={}, cells={})
    cache = {}
    for d1 in (Fraction(1, 10000), Fraction(3, 10000), Fraction(1, 1000)):
        d2 = Fraction(3, 1000) - d1
        for d in (d1, d2):
            if d not in cache:
                cache[d] = certified_c(d)
                res["constants"][str(d)] = dict(c=cache[d][0], beta=cache[d][1], lambda_lower_N0=cache[d][2])
                print("certified c", str(d), cache[d], flush=True)
    for case in ("B4x12", "B8x52"):
        s = Fraction(str(sig[case]["sigma_q"]))
        m = price[case]
        for eps in p2.EPS:
            e = Fraction(9, 20) * Fraction(str(eps))
            se = s / e
            best = None
            for d1 in (Fraction(1, 10000), Fraction(3, 10000), Fraction(1, 1000)):
                d2 = Fraction(3, 1000) - d1
                c1, c2 = cache[d1][0], cache[d2][0]
                for j in range(1, 400):
                    D1 = Fraction(j, 4000)  # phase half-width of stage 1
                    err_a = D1 / 2 + D1 * D1 / 4
                    mU = m + 2 * S * err_a
                    if mU > S / 2:
                        continue
                    N1 = max(math.ceil(Fraction(str(c1)) / D1), p2.N0)
                    D2 = p2.delta_phi(mU, S, e)
                    N2 = math.ceil(Fraction(str(c2)) / D2)
                    tot = N1 + N2
                    if best is None or tot < best["N_total"]:
                        best = dict(delta1=str(d1), delta2=str(d2), D1=float(D1), m_U_worst=float(mU), N1=N1, N2=N2,
                                    N_total=tot, k=tot / float(se), c1=c1, c2=c2)
            # reference: the U1 row (price + L1) and the U2-only row at delta 0.003, same certified c(0.003-4e-6)
            res["cells"][f"{case}|{eps}"] = dict(best=best, label="mod (certified constants; worst case over stage-1 "
                                                                  "outcomes; evaluated at the task's mean)")
            print(case, eps, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in best.items()}, flush=True)
    with open(OUT / "p2c_self_mean.json", "x", encoding="utf-8") as f:
        json.dump(res, f, indent=1)


if __name__ == "__main__":
    main()
