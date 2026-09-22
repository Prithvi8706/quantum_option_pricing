"""Independent checks of stored estimator certificates; never regenerates them.

This reviewer implementation uses direct matrix powers, independent binomial
sums, and high-precision interval checks of the archived selected schedules.
"""

from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path

import mpmath as mp
import numpy as np


DIRECTORY = Path("results/controlled_priority_completion")


def rational(pair):
    return Fraction(*pair)


def tail(n, p, start, stop):
    return sum(
        (Fraction(math.comb(n, k)) * p**k * (1 - p) ** (n - k)
         for k in range(start, stop)),
        Fraction(0),
    )


def interval(value):
    value = Fraction(value)
    return mp.iv.mpf(value.numerator) / value.denominator


def asin(value):
    return mp.iv.atan2(value, mp.iv.sqrt(1 - value * value))


def direct_plus(values, probabilities, calls):
    start = np.sqrt(probabilities)
    reflection = 2 * np.outer(start, start) - np.eye(len(start))
    # Direct application of the declared unitary, not the author's Schur routine.
    oracle = reflection @ np.diag(np.exp(-2j * np.arctan(values)))
    result = np.linalg.matrix_power(oracle, calls) @ start
    return float((1 + np.vdot(start, result).real) / 2)


def review_hadamard(row, rng):
    allocation = row["allocation"]
    radius = rational(allocation["initial_radius_exact"])
    assert radius * radius >= Fraction(allocation["moment"])
    rms = rational(allocation["normalized_RMS_upper_exact"])
    assert rms == 2 * radius / allocation["normalizer"]
    c = rational(allocation["c_exact"])
    contraction = (1 + c) / (1 + 3 * c)
    assert contraction == rational(allocation["contraction_exact"])
    width, assigned, actual = 2 * radius, Fraction(0), Fraction(0)
    C = allocation["C"]
    assert C * rms < 1
    si = interval(rms)
    eta = interval(Fraction(2, C * C))
    calls, tests, matrix_cases = 0, 0, 0
    margins = []
    stages = allocation["stages"]
    for index, stage in enumerate(stages):
        assert rational(stage["width_exact"]) == width
        eps = width / ((1 + 3 * c) * allocation["normalizer"])
        assert eps == rational(stage["test_epsilon_exact"])
        T, n, threshold = stage["T"], stage["repetitions"], stage["small_if_plus_count_at_least"]
        a = rational(stage["p_plus_small_lower_exact"])
        b = rational(stage["p_plus_large_upper_exact"])
        alpha = 2 * interval(eps) / (mp.iv.sqrt(1 + si * si) * (1 + C * si))
        beta = 2 * asin(interval((1 + 2 * c) * eps) / (1 - C * si))
        gamma = 2 * asin(interval(c * eps) / (1 - C * si))
        assert (T * gamma < mp.iv.pi) is True
        assert (T * alpha > 0) is True
        assert (T * beta < 2 * mp.iv.pi) is True
        assert (interval(a) <= (1 - eta) * (1 + mp.iv.cos(T * gamma)) / 2) is True
        for endpoint in (alpha, beta):
            assert (interval(b) >= eta + (1 - eta) * (1 + mp.iv.cos(T * endpoint)) / 2) is True
        small_failure = tail(n, a, 0, threshold)
        large_failure = tail(n, b, threshold, n + 1)
        delta = rational(stage["failure_allocation_exact"])
        assert max(small_failure, large_failure) <= delta
        assigned += delta
        actual += max(small_failure, large_failure)
        calls += n * T
        tests += n
        # Sample validation complements the proof; it is never its substitute.
        if index in (0, len(stages) // 2, len(stages) - 1):
            for small, mean in ((True, 0), (True, c * eps),
                                (False, eps), (False, (1 + 2 * c) * eps)):
                for rare in (1e-8, 0.01, 0.35):
                    for sign in (-1, 1):
                        p = np.array([rare, 0.2, 0.8 - rare])
                        z = rng.normal(size=3)
                        z[0] /= math.sqrt(rare)
                        z -= p @ z
                        variance = max(0, float(rms) ** 2 - float(mean) ** 2)
                        z *= math.sqrt(variance / float(p @ (z * z)))
                        values = z + sign * float(mean)
                        observed = direct_plus(values, p, T)
                        margin = observed - float(a) if small else float(b) - observed
                        assert margin >= -1e-7, (row["model"], stage["stage"], margin)
                        margins.append(margin)
                        matrix_cases += 1
        width *= contraction
    assert assigned <= Fraction(allocation["ideal_test_failure"])
    assert actual <= assigned
    assert width / 2 <= Fraction(allocation["error"])
    assert calls == allocation["controlled_U_calls"]
    assert tests == allocation["hadamard_test_executions"]
    assert calls * row["single_U"]["t_count"] == row["arithmetic_T_count"]
    assert 3 * 67 * calls == row["additional_single_qubit_rotations"]
    return dict(model=row["model"], mode=row["mode"],
                exact_tail_union=float(actual), allocated_failure=float(assigned),
                direct_matrix_cases=matrix_cases, smallest_matrix_margin=min(margins),
                controlled_U_calls=calls, all_selected_stage_intervals_checked=len(stages))


def review_bounded(row):
    a = row["allocation"]
    M, r = a["M"], a["repetitions"]
    assert M == 1 << a["qpe_bits"]
    assert (256 * (mp.iv.pi / M + mp.iv.pi**2 / M**2) <= interval(a["error"])) is True
    bad = rational(a["elementary_failure_upper_exact"])
    assert (interval(bad) >= 1 - 8 / mp.iv.pi**2) is True
    failure = tail(r, bad, r // 2 + 1, r + 1)
    assert failure <= Fraction(a["ideal_test_failure"])
    assert r * (M - 1) == a["controlled_grover_calls"]
    calls, q = a["controlled_grover_calls"], a["qpe_bits"]
    assert calls * row["single_iterate_T_count"] + 3 * r * (q - 1) == row["arithmetic_T_count"]
    assert row["arbitrary_single_qubit_IQFT_rotations"] == 3 * r * (q * (q - 1) // 2 - q + 1)
    # Explicit tiny sign check for G=(2|+><+|-I)(I-2Pi_good).
    # The global reflection sign changes controlled phases and is indispensable.
    cases = 0
    for size in (4, 8, 16):
        start = np.ones(size) / math.sqrt(size)
        reflection = 2 * np.outer(start, start) - np.eye(size)
        for good in range(size + 1):
            mark = np.diag([-1] * good + [1] * (size - good))
            oracle = reflection @ mark
            theta = math.asin(math.sqrt(good / size))
            for power in (1, 2, 7):
                observed = np.vdot(start, np.linalg.matrix_power(oracle, power) @ start)
                assert abs(observed - math.cos(2 * power * theta)) < 1e-12
                cases += 1
    return dict(model=row["model"], exact_median_failure=float(failure),
                controlled_grover_calls=calls, independent_reflection_sign_cases=cases)


def main():
    mp.iv.dps = 100
    paths = [DIRECTORY / name for name in ("estimator_hadamard.json", "estimator_bounded.json")]
    h, b = [json.loads(path.read_text()) for path in paths]
    rng = np.random.default_rng(2026092231)
    record = dict(
        status=("All independent checks passed; this does not close physical "
                "or financial obligations."),
        seed=2026092231,
        input_sha256={path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},
        hadamard=[review_hadamard(row, rng) for row in h],
        bounded=[review_bounded(row) for row in b],
    )
    out = DIRECTORY / "capacity_estimator_review.json"
    out.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
