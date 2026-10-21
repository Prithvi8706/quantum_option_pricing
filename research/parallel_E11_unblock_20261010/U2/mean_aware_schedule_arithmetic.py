"""U2 design helper: pure-constant arithmetic of the saved E07 bounded-AE schedule formula.

Design/prospectus only. It evaluates no new scientific bound: no price, moment,
mean certificate or bias is computed. It only (a) reproduces the saved
eps=1/100 E07 schedule from the frozen executed_code snapshot, (b) evaluates
the same schedule formula at the three other declared targets, and (c) solves
the mean-aware variant of that formula for the threshold m* that a FUTURE
certified mean upper bound would have to meet. Every decision uses Fractions
and the saved Machin pi enclosure; sqrt thresholds are enclosed by integer
square roots (inward for the sufficient threshold).

Run (read-only on the program; writes one new JSON beside this file, exclusive create):
    python -I -S -B research/parallel_E11_unblock_20261010/U2/mean_aware_schedule_arithmetic.py
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
E07 = ROOT / "results/limitation_program_20261001/E07_schedule_run001"
SNAPSHOT = E07 / "executed_code/financial_bounded_schedule.py"
SNAPSHOT_SHA = "4452c3319e9b7c33b96276aeefe137905d41c4638e42037d264fd6bdd26f149c"
OUT = Path(__file__).resolve().parent / "mean_aware_schedule_arithmetic_run001.json"

SPAN = 64  # 2**46 / 2**40 dollars (E03 selector span)
FAILURE = F(3, 1000)  # E07 estimator failure allowance
READOUT = F(1, 2**39)  # E02 classical_readout_error_allowance (dollars)
TARGETS = [F(1, 10), F(3, 100), F(1, 100), F(1, 1000)]
SHARE = F(9, 20)  # C05 / E24 adopted statistical share
SCALE = 10**12  # threshold enclosure grid (dollars)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_snapshot():
    assert sha(SNAPSHOT) == SNAPSHOT_SHA, "E07 snapshot hash mismatch"
    spec = importlib.util.spec_from_file_location("e07_schedule_snapshot", SNAPSHOT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sqrt_enclosure(x):
    """Return (lo, hi) Fractions with lo <= sqrt(x) <= hi on a 1/SCALE grid."""
    x = F(x)
    assert x >= 0
    n = (x.numerator * SCALE * SCALE) // x.denominator
    r = isqrt(n)
    lo = F(r, SCALE)
    hi = F(r + 1, SCALE)
    assert lo * lo <= x <= hi * hi
    return lo, hi


def worst_case_error(M, pi_hi, readout=READOUT):
    return SPAN * (pi_hi / M + pi_hi**2 / M**2) + readout


def mean_aware_error(m, M, pi_hi, readout=READOUT):
    """Dollar error of Theorem 12 (k=1) on span 64 when E[g] <= m <= 32.

    span * 2*pi*sqrt(a(1-a))/M with a <= m/64 <= 1/2 equals 2*pi*sqrt(m(64-m))/M.
    Returned as an upper bound using an outward sqrt.
    """
    m = F(m)
    assert 0 <= m <= SPAN / 2
    _, root_hi = sqrt_enclosure(m * (SPAN - m))
    return 2 * pi_hi * root_hi / M + SPAN * pi_hi**2 / M**2 + readout


def threshold(delta, M, pi_hi, readout=READOUT):
    """Largest m with 2*pi*sqrt(m(64-m))/M + 64*pi^2/M^2 + readout <= delta.

    m* = 32 - sqrt(1024 - R^2), R = (delta - readout - 64*pi^2/M^2) * M / (2*pi).
    Returns None when the curvature term alone exceeds delta; returns the
    inward (sufficient) and outward enclosures of m* otherwise.
    """
    slack = delta - readout - SPAN * pi_hi**2 / M**2
    if slack <= 0:
        return None
    R = slack * M / (2 * pi_hi)
    if R >= SPAN / 2:
        return dict(no_mean_condition_needed=True)
    lo_s, hi_s = sqrt_enclosure(F(SPAN * SPAN, 4) - R * R)
    # sufficient: any m <= inward works (extra 1e-9 USD inward step absorbs the sqrt grid)
    inward = F(SPAN, 2) - hi_s - F(1, 10**9)
    outward = F(SPAN, 2) - lo_s  # necessary (for this formula): m <= outward
    assert inward <= outward
    # Verify sufficiency directly with the outward-sqrt error evaluation.
    assert mean_aware_error(inward, M, pi_hi, readout) <= delta
    return dict(inward=inward, outward=outward, R=R)


def as_pair(x):
    return [F(x).numerator, F(x).denominator]


def dec(x, places=6):
    x = F(x)
    q = x.numerator * 10**places // x.denominator
    return f"{q // 10**places}.{q % 10**places:0{places}d}"


def main():
    sched = load_snapshot()
    saved = json.loads((E07 / "schedule.json").read_text())
    lo, hi = sched.pi_interval()
    assert [as_pair(lo), as_pair(hi)] == saved["pi_enclosure_exact"]

    reproduced = sched.certified_schedule(F(9, 2000), FAILURE, SPAN)
    for key in ("M", "repetitions", "controlled_grover_calls", "ideal_error_upper_exact",
                "ideal_failure_upper_exact", "elementary_failure_upper_exact"):
        assert reproduced[key] == saved[key], key

    rows = []
    for eps in TARGETS:
        delta = SHARE * eps
        base = sched.certified_schedule(delta, FAILURE, SPAN)
        M = base["M"]
        reps = base["repetitions"]
        assert worst_case_error(M, hi) <= delta, "readout must still fit at baseline"
        row = dict(
            epsilon=dec(eps, 4),
            statistical_share_dollars=as_pair(delta),
            saved_schedule_exists=(eps == F(1, 100)),
            baseline_M=M,
            baseline_qpe_bits=base["qpe_bits"],
            repetitions=reps,
            baseline_calls=base["controlled_grover_calls"],
            baseline_worst_case_error_plus_readout=dec(worst_case_error(M, hi), 9),
            # Could worst-case M/2 ever fit? (it cannot by minimality)
            worst_case_half_fits=bool(worst_case_error(M // 2, hi) <= delta),
            reductions=[],
        )
        for divisor in (2, 4, 8):
            Mp = M // divisor
            t = threshold(delta, Mp, hi)
            t0 = threshold(delta, Mp, hi, readout=0)
            entry = dict(divisor=divisor, M=Mp, qpe_bits=Mp.bit_length() - 1,
                         calls=reps * (Mp - 1))
            if t is None:
                entry["feasible_for_any_m"] = False
            else:
                entry["feasible_for_any_m"] = True
                entry["m_star_sufficient_inward"] = dec(t["inward"], 9)
                entry["m_star_outward"] = dec(t["outward"], 9)
                entry["m_star_inward_exact"] = as_pair(t["inward"])
                entry["readout_free_m_star_inward"] = dec(t0["inward"], 9)
            row["reductions"].append(entry)
        rows.append(row)

    rotations = json.loads(
        (ROOT / "results/limitation_program_20261001/E02_IQFT_run001/rotations.json").read_text())
    rot_max = max(F(*v["operator_error_upper_exact"]) for v in rotations.values())

    result = dict(
        schema="U2-mean-aware-bounded-AE-schedule-arithmetic-v1",
        design_only=True,
        new_scientific_bound_evaluated=False,
        premises={
            str(SNAPSHOT.relative_to(ROOT)).replace("\\", "/"): sha(SNAPSHOT),
            "results/limitation_program_20261001/E07_schedule_run001/schedule.json":
                sha(E07 / "schedule.json"),
            "results/limitation_program_20261001/E02_IQFT_run001/rotations.json":
                sha(ROOT / "results/limitation_program_20261001/E02_IQFT_run001/rotations.json"),
        },
        saved_eps_1_100_schedule_reproduced=True,
        readout_allowance_dollars=as_pair(READOUT),
        certified_rotation_labels=sorted(rotations, key=lambda k: int(k.split("_")[-1])),
        certified_rotation_max_operator_error=dec(rot_max, 30),
        rows=rows,
        python=sys.version,
    )
    with OUT.open("x", encoding="utf-8") as handle:
        json.dump(result, handle, indent=1)
        handle.write("\n")
    print(json.dumps(rows, indent=1))


if __name__ == "__main__":
    main()
