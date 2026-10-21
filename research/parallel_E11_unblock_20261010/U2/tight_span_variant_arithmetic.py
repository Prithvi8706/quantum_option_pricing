"""U2 design helper 2: schedule-formula arithmetic for a support-tight normalization variant.

Design/prospectus only; no new scientific bound is evaluated. The only
scientific premise is the already-certified, independently audited E03
all-input native support 0 <= Yraw <= 42680645928225 (units 2^-40 USD).

Variant: compare a b-bit Hadamard selector against the exact integer c*Yraw
instead of Yraw against a 46-bit selector. If c*sup(Yraw) <= 2^b the amplitude is
p' = c*E[Yraw]/2^b = E[g]/S' with effective span S' = 2^(b-40)/c dollars, and the
decoded price is S'*p'. The saved E07 schedule formula is then evaluated with
S' in place of 64 (worst case), and its mean-aware form is solved for m*.
Readout allowance 2^-39 USD is carried over unchanged as a placeholder.

Run: python -I -S -B research/parallel_E11_unblock_20261010/U2/tight_span_variant_arithmetic.py
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from fractions import Fraction as F
from math import isqrt
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
SNAPSHOT = ROOT / "results/limitation_program_20261001/E07_schedule_run001/executed_code/financial_bounded_schedule.py"
SNAPSHOT_SHA = "4452c3319e9b7c33b96276aeefe137905d41c4638e42037d264fd6bdd26f149c"
E03 = ROOT / "results/limitation_program_20261001/E03_support_run001/summary.json"
OUT = Path(__file__).resolve().parent / "tight_span_variant_arithmetic_run001.json"

FAILURE = F(3, 1000)
READOUT = F(1, 2**39)
TARGETS = [F(1, 10), F(3, 100), F(1, 100), F(1, 1000)]
SHARE = F(9, 20)
VARIANTS = [(1, 46), (3, 47), (13, 49), (105, 52), (211, 53)]  # (c, b)
SCALE = 10**12


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_snapshot():
    assert sha(SNAPSHOT) == SNAPSHOT_SHA
    spec = importlib.util.spec_from_file_location("e07_schedule_snapshot", SNAPSHOT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sqrt_hi(x):
    x = F(x)
    n = -((-x.numerator * SCALE * SCALE) // x.denominator)
    r = isqrt(n)
    if r * r < n:
        r += 1
    return F(r, SCALE)


def sqrt_lo(x):
    x = F(x)
    return F(isqrt((x.numerator * SCALE * SCALE) // x.denominator), SCALE)


def worst(S, M, pi):
    return S * (pi / M + pi**2 / M**2) + READOUT


def mean_aware(S, m, M, pi):
    return 2 * pi * sqrt_hi(m * (S - m)) / M + S * pi**2 / M**2 + READOUT


def m_star(S, delta, M, pi):
    slack = delta - READOUT - S * pi**2 / M**2
    if slack <= 0:
        return None
    R = slack * M / (2 * pi)
    if R >= S / 2:
        return "any"
    inward = S / 2 - sqrt_hi(S * S / 4 - R * R) - F(1, 10**9)
    if inward <= 0:
        return None
    assert mean_aware(S, inward, M, pi) <= delta
    return inward


def dec(x, places=9):
    x = F(x)
    q = x.numerator * 10**places // x.denominator
    return f"{q // 10**places}.{q % 10**places:0{places}d}"


def main():
    sched = load_snapshot()
    _, hi = sched.pi_interval()
    case = json.loads(E03.read_text())["cases"][0]
    assert case["case"] == "B4x12"
    lo_raw, sup_raw = case["payoff_raw_bounds"]
    assert lo_raw == 0 and sup_raw == 42680645928225
    rows = []
    for eps in TARGETS:
        delta = SHARE * eps
        base = sched.certified_schedule(delta, FAILURE, 64)
        M, reps = base["M"], base["repetitions"]
        for c, b in VARIANTS:
            assert c * sup_raw <= 2**b, (c, b)
            S = F(2 ** (b - 40), c)
            entry = dict(epsilon=dec(eps, 4), c=c, selector_bits=b, span=dec(S, 6),
                         baseline64_M=M)
            for divisor in (1, 2, 4):
                Mp = M // divisor
                key = f"M_over_{divisor}"
                wc = worst(S, Mp, hi) <= delta
                ms = m_star(S, delta, Mp, hi)
                entry[key] = dict(
                    M=Mp, calls=reps * (Mp - 1),
                    worst_case_fits_without_mean=bool(wc),
                    mean_threshold_sufficient=(None if ms is None else
                                               ("any" if ms == "any" else dec(ms))),
                )
            rows.append(entry)
    result = dict(
        schema="U2-tight-span-variant-arithmetic-v1",
        design_only=True,
        new_scientific_bound_evaluated=False,
        premises={
            "results/limitation_program_20261001/E07_schedule_run001/executed_code/financial_bounded_schedule.py": SNAPSHOT_SHA,
            "results/limitation_program_20261001/E03_support_run001/summary.json": sha(E03),
        },
        sup_raw=sup_raw,
        rows=rows,
        python=sys.version,
    )
    with OUT.open("x", encoding="utf-8") as handle:
        json.dump(result, handle, indent=1)
        handle.write("\n")
    for r in rows:
        print(r["epsilon"], r["c"], r["selector_bits"], r["span"],
              {k: (v["M"], v["worst_case_fits_without_mean"], v["mean_threshold_sufficient"])
               for k, v in r.items() if k.startswith("M_over")})


if __name__ == "__main__":
    main()
