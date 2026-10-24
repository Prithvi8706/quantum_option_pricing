"""Compare the primary and independent A2a clip-split paths and write summary.json (exclusive create)."""
import hashlib
import json
import sys
from decimal import Decimal as D
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "results/claim_debts_20261022/a2a"


def main(run):
    sys.set_int_max_str_digits(0)
    out = OUT / run
    prim = json.loads((out / "certificate.json").read_text())
    ind = json.loads((out / "independent.json").read_text())
    cases, ok = {}, True
    for case in ("B4x12", "B8x52"):
        p, i = prim["cases"][case], ind["cases"][case]
        tp = F(*p["total_clip_split"]["exact"])
        ti = F(D(i["total_upper"]))
        # display: primary total rounded up to the 2^-64 grid (still an upper bound)
        disp = F(-((-tp.numerator << 64) // tp.denominator), 1 << 64)
        rel = abs(tp - ti) / tp
        agree = rel <= F(1, 10**9)
        meets = p["meets_target"] and i["meets_target_0p55eps"]
        ok = ok and agree and meets and p["clipable_sites"] == i["clipable_sites"]
        cases[case] = {
            "certified_total_upper_rounded_up_2^-64": [disp.numerator, disp.denominator],
            "certified_total_float": float(tp),
            "independent_total_upper": i["total_upper"][:24],
            "relative_difference": float(rel),
            "paths_agree_1e-9": agree,
            "run002_certified_total": p["total_certified_run002"]["float"],
            "H_price": p["H_price"]["float"],
            "zeta_noclip": p["zeta_noclip"]["float"],
            "switch_noclip": p["switch_noclip"]["float"],
            "P_fin_C_upper_primary_Bernstein_log10_approx": p.get("P_fin_C_upper_log10_approx"),
            "P_fin_C_upper_independent_Bennett": i["P_fin_C_upper"][:12] + ("..." + i["P_fin_C_upper"][-6:] if "E" in i["P_fin_C_upper"] else ""),
            "clipable_sites": p["clipable_sites"],
            "target_0p55eps": 0.00055,
            "meets_target": meets,
            "margin_to_target": 0.00055 - float(tp),
        }
    doc = {
        "schema": "a2a-clip-split-summary-v1",
        "rigour": "R1 (two independent exact/outward paths agree); NOT R2: no preregistration, sealed run or human peer review",
        "label": "cert (R1) for B8x52 eps=$0.001 deterministic bias row A2a; inputs are certified run002 bridge records cited by sha256",
        "all_checks_pass": ok,
        "files_sha256": {n: hashlib.sha256((out / n).read_bytes()).hexdigest() for n in ("certificate.json", "independent.json")},
        "producers_sha256": {n: hashlib.sha256((ROOT / "research/claim_debts_20261022/a2a" / n).read_bytes()).hexdigest()
                             for n in ("clip_split_certificate.py", "independent_recompute.py", "summarize.py")},
        "interpreter": sys.version,
        "cases": cases,
    }
    with open(out / "summary.json", "x") as fh:
        json.dump(doc, fh, indent=1)
    print(json.dumps({c: {k: v for k, v in r.items() if k in ("certified_total_float", "relative_difference", "meets_target", "clipable_sites")} for c, r in cases.items()}), "ALL_OK", ok)


if __name__ == "__main__":
    main(sys.argv[1])
