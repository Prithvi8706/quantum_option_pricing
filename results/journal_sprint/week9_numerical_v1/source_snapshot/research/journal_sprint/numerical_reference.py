"""Independent high-precision small-count reference, not directed interval arithmetic."""

from fractions import Fraction
from functools import lru_cache

import mpmath as mp

PRECISION = 80
STEPS = 160


def polynomial(a, depth):
    if depth == 0:
        return a
    if depth == 1:
        return a * (9 + a * (-24 + 16 * a))
    if depth == 2:
        return a * (25 + a * (-200 + a * (560 + a * (-640 + 256 * a))))
    raise ValueError("reference only supports depths 0,1,2")


@lru_cache(maxsize=None)
def beta_bracket(probability, a, b, precision):
    with mp.workdps(precision):
        target = mp.mpf(probability)
        lo, hi = mp.mpf(0), mp.mpf(1)
        for _ in range(STEPS):
            mid = (lo + hi) / 2
            if mp.betainc(a, b, 0, mid, regularized=True) < target:
                lo = mid
            else:
                hi = mid
        return lo, hi


def cp(count, shots, alpha):
    if not 0 <= count <= shots or shots < 1 or not 0 < alpha < 1:
        raise ValueError("invalid binomial interval input")
    lo = (
        mp.mpf(0)
        if count == 0
        else beta_bracket(mp.nstr(alpha / 2, PRECISION), count, shots - count + 1, mp.mp.dps)[0]
    )
    hi = (
        mp.mpf(1)
        if count == shots
        else beta_bracket(mp.nstr(1 - alpha / 2, PRECISION), count + 1, shots - count, mp.mp.dps)[1]
    )
    return lo, hi


def union(parts):
    result = []
    for lo, hi in sorted(parts):
        if lo > hi:
            continue
        if result and lo <= result[-1][1]:
            result[-1] = (result[-1][0], max(result[-1][1], hi))
        else:
            result.append((lo, hi))
    return result


def preimage(low, high, depth):
    if not 0 <= low <= high <= 1:
        return []
    if depth == 0:
        return [(low, high)]
    if depth not in (1, 2):
        raise ValueError("unsupported reference depth")
    d = 2 * depth + 1
    edges = [mp.mpf(0)] + [mp.sin(mp.pi * j / (2 * d)) ** 2 for j in range(1, d)] + [mp.mpf(1)]
    result = []
    for j, (left, right) in enumerate(zip(edges, edges[1:])):
        increasing = j % 2 == 0

        def root(target):
            if target == 0:
                v = left if increasing else right
                return v, v
            if target == 1:
                v = right if increasing else left
                return v, v
            lo, hi = left, right
            for _ in range(STEPS):
                mid = (lo + hi) / 2
                if (polynomial(mid, depth) < target) == increasing:
                    lo = mid
                else:
                    hi = mid
            return lo, hi

        a, b = (root(low)[0], root(high)[1]) if increasing else (root(high)[0], root(low)[1])
        result.append((a, b))
    return union(result)


def reference(case):
    with mp.workdps(PRECISION):
        guard = mp.mpf(case["guard"])
        alpha = mp.mpf("0.025")
        cal = [cp(k, 64, alpha / 2) for k in case["calibration_errors"]]
        fl, fu = max(0, cal[0][0] - guard), min(1, cal[0][1] + guard)
        gl, gu = max(0, cal[1][0] - guard), min(1, cal[1][1] + guard)
        if fu + gu >= 1:
            return [(mp.mpf(0), mp.mpf(1))]
        result = [(mp.mpf(0), mp.mpf(1))]
        for k, depth in zip(case["counts"], case["depths"]):
            lo, hi = cp(k, 128, alpha / len(case["depths"]))
            p_lo = max(0, (lo - fu) / (1 - fu - gl))
            p_hi = min(1, (hi - fl) / (1 - fl - gu))
            branch = preimage(p_lo, p_hi, depth)
            result = union([(max(a, c), min(b, d)) for a, b in result for c, d in branch])
        return result


def case_table():
    amplitudes = (".001", ".01", ".1", ".17", ".3", ".5", ".7", ".9", ".999")
    cases = []
    for si, depths in enumerate(([0], [0, 1, 2])):
        counts = [
            [
                round(128 * (Fraction(2, 100) + Fraction(91, 100) * polynomial(Fraction(a), k)))
                for k in depths
            ]
            for a in amplitudes
        ]
        counts += [
            [0] * len(depths),
            [128] * len(depths),
            [0 if j % 2 == 0 else 128 for j in range(len(depths))],
            [128 if j % 2 == 0 else 0 for j in range(len(depths))],
        ]
        for ci, cal in enumerate(((0, 0), (1, 4), (5, 1), (32, 32))):
            for gi, guard in enumerate(("0", ".01", ".03")):
                for oi, observed in enumerate(counts):
                    cases.append(
                        dict(
                            case_id=f"s{si}_c{ci}_g{gi}_o{oi}",
                            depths=depths,
                            calibration_errors=list(cal),
                            guard=guard,
                            counts=observed,
                        )
                    )
    return cases
