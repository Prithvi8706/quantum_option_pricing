"""Theorem-condition screen and an analytically soluble nested negative control."""

import math

import numpy as np
from scipy.special import ndtr

from .storage import rng_for


def heston_conditions(kappa, theta, volvol, rho, delta):
    if (not all(math.isfinite(v) for v in (kappa, theta, volvol, rho, delta))
            or min(kappa, theta, volvol, delta) <= 0 or not -1 <= rho <= 1):
        raise ValueError("invalid Heston scalar parameters")
    middle = 2 * kappa * volvol * rho - rho * rho * volvol * volvol
    eta = 4 * kappa * theta / volvol**2
    tests = dict(
        delta_at_least_one=delta >= 1,
        exponential_sum=math.exp(-kappa * delta / 2) + math.exp(-kappa * delta) < 1,
        middle_nonnegative=middle >= 0,
        middle_below_kappa_squared=middle < kappa**2,
        fourth_inequality=(1 + math.exp(-2 * kappa * delta)) / 4
        + rho * volvol / kappa * (1 - math.exp(-2 * kappa * delta)) / 4
        < 1 / (2 * (1 + math.exp(-kappa * delta / 2))),
        eta_at_least_five=eta >= 5,
    )
    return dict(kappa=kappa, theta=theta, volvol=volvol, rho=rho, delta=delta,
                eta=eta, tests=tests, displayed_scalar_screen=all(tests.values()),
                full_theorem_applicability="not_established")


def heston_grid():
    return [heston_conditions(k, t, v, r, delta)
            for k in (.5, 2.) for t in (.04, .5) for v in (.2, .6)
            for r in (-.7, 0., .3) for delta in (1 / 12, 1., 3.)]


def normal_positive_mean(mu, variance):
    if not math.isfinite(mu) or not math.isfinite(variance) or variance < 0:
        raise ValueError("invalid Gaussian moments")
    if variance == 0:
        return max(mu, 0.0)
    std = math.sqrt(variance)
    return std * math.exp(-mu * mu / (2 * variance)) / math.sqrt(2 * math.pi) + mu * ndtr(
        mu / std
    )


def antithetic_correction(inner_samples):
    x = np.asarray(inner_samples, dtype=float)
    if x.ndim != 2 or x.shape[1] < 2 or x.shape[1] % 2 or not np.all(np.isfinite(x)):
        raise ValueError("finite even-width inner samples required")
    half = x.shape[1] // 2
    fine = np.maximum(x.mean(axis=1), 0)
    coarse = (np.maximum(x[:, :half].mean(axis=1), 0)
              + np.maximum(x[:, half:].mean(axis=1), 0)) / 2
    return fine - coarse


def nested_diagnostic():
    truth = float(normal_positive_mean(.2, 1))
    rows = []
    for m in (1, 4, 16, 64, 256):
        expected = float(normal_positive_mean(.2, 1 + 4 / m))
        for rep in range(8):
            rng = rng_for("shortlist_v1", "nested", m, rep)
            y = rng.normal(.2, 1, size=2048)
            z = rng.normal(size=(2048, m))
            estimate = float(np.maximum(y + 2 * z.mean(axis=1), 0).mean())
            rows.append(dict(inner=m, rep=rep, estimate=estimate,
                             expected_naive=expected, exact_bias=expected - truth,
                             inner_evaluations=2048 * m,
                             analytic_inner_estimate=float(np.maximum(y, 0).mean())))
    levels = []
    for level in range(1, 9):
        m = 2**level
        rng = rng_for("shortlist_v1", "nested_correction", level)
        y = rng.normal(.2, 1, size=(4096, 1))
        x = y + 2 * rng.normal(size=(4096, m))
        correction = antithetic_correction(x)
        expected = float(normal_positive_mean(.2, 1 + 4 / m)
                         - normal_positive_mean(.2, 1 + 8 / m))
        levels.append(dict(level=level, inner=m, mean=float(correction.mean()),
                           variance=float(correction.var(ddof=1)), expected=expected,
                           inner_evaluations=4096 * m))
    return dict(target=truth, rows=rows, levels=levels,
                scope="avoidable nesting control, not real CVA or quantum implementation")
