"""Review finding 5b: which P2 run002 k cells lie below N0 = 800, and does any of them enter a reported minimum M?

A cell enters the headline minima only if its T_C is not overhead-dominated. This script lists every
uncovered cell, its headline eligibility, and the certified lower bound lambda_lower at that cell's own N (which
need not reach 1 - delta_target, because lambda_lower increases in N).
Run (repo root): .context/frontier_t0_env/Scripts/python.exe -I -S -B research/frontier_probe_20261021/coverage_check.py
"""
import hashlib
import json
import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import p2_window_constant as p2  # noqa: E402

ROOT = HERE.parents[1]
OUT = ROOT / "results" / "frontier_probe_20261021" / "coverage" / "run001"
IN = dict(p2=ROOT / "results/frontier_probe_20261021/p2/run002/p2_window.json",
          head=ROOT / "results/frontier_probe_20261021/headline/run002/headline_table.json")


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    p = json.loads(IN["p2"].read_text(encoding="utf-8"))
    h = json.loads(IN["head"].read_text(encoding="utf-8"))
    overhead = {(c["case"], c["eps"]): c["overhead_T_C"] for c in h["cells"]}
    rows = []
    cache = {}
    for key, v in p["k"].items():
        if v["covered_by_N0_certificate"]:
            continue
        case, eps, split, spl, ml, tag, fail = key.split("|")
        design = p["certified"][v["design"]]
        delta = Fraction(design["delta"])
        target = delta - (Fraction(4, 10 ** 6) if tag == "with_impl_budget" else 0)
        beta, gamma, c = design["beta"], Fraction(design["gamma"]), Fraction(str(v["c"]))
        if (beta, gamma, c) not in cache:
            Ic, info = p2.I_c_lower(c, Decimal(beta), Decimal(gamma.numerator) / Decimal(gamma.denominator),
                                    Fraction(1, 1000))
            Itot = 2 * p2.PI_HI * p2.int_phi_sq_upper(Fraction(beta) ** 2, gamma)
            cache[(beta, gamma, c)] = (Ic, info["phi0"], Decimal(Itot.numerator) / Decimal(Itot.denominator))
        Ic, phi0, Itot = cache[(beta, gamma, c)]
        lam, _ = p2.lambda_lower(v["N_calls"], Decimal(c.numerator) / Decimal(c.denominator), Decimal(beta),
                                 Decimal(gamma.numerator) / Decimal(gamma.denominator), Ic, Itot, phi0)
        rows.append(dict(cell=key, N_calls=v["N_calls"], eligible=not overhead[(case, float(eps))],
                         lambda_lower_at_N=str(lam), target=str(1 - target), certified_at_N=lam >= 1 - Decimal(
                             target.numerator) / Decimal(target.denominator)))
    eligible_uncertified = [r for r in rows if r["eligible"] and not r["certified_at_N"]]
    out = dict(meta=dict(script="research/frontier_probe_20261021/coverage_check.py", python=sys.version,
                         inputs_sha256={a: hashlib.sha256(b.read_bytes()).hexdigest() for a, b in IN.items()}),
               n_uncovered=len(rows), n_eligible_uncertified=len(eligible_uncertified), rows=rows,
               label="mod")
    with open(OUT / "coverage.json", "x", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    print("uncovered cells:", len(rows), "| eligible:", sum(r["eligible"] for r in rows),
          "| certified at own N:", sum(r["certified_at_N"] for r in rows),
          "| eligible and uncertified:", len(eligible_uncertified))
    for r in rows[:6]:
        print(r)


if __name__ == "__main__":
    main()
