"""Model-conditional anytime sets; beta-mixture/Ville is established prior art."""

import math
from functools import lru_cache

from scipy.special import betaln, xlogy, xlog1py

from .intervals import ConfidenceSet, ROUNDING, _integers, clopper_pearson, intersect, sine_preimage


@lru_cache(maxsize=20000, typed=True)
def bernoulli_cs(successes, shots, alpha):
    if (
        isinstance(shots, bool)
        or not isinstance(shots, int)
        or not 0 <= shots <= 10_000_000
        or isinstance(successes, bool)
        or not isinstance(successes, int)
        or not 0 <= successes <= shots
        or not 0 < alpha < 1
    ):
        raise ValueError("invalid Bernoulli confidence-sequence input")
    if shots == 0:
        return 0.0, 1.0
    constant = betaln(successes + 0.5, shots - successes + 0.5) - betaln(0.5, 0.5)
    threshold = math.log(1 / alpha)

    def accepted(p):
        return constant - xlogy(successes, p) - xlog1py(shots - successes, -p) <= threshold

    center = successes / shots
    if not accepted(center):
        raise ArithmeticError("mixture minimum failed")
    left, right = 0.0, center
    for _ in range(60):
        mid = (left + right) / 2
        if accepted(mid):
            right = mid
        else:
            left = mid
    lo = left
    left, right = center, 1.0
    for _ in range(60):
        mid = (left + right) / 2
        if accepted(mid):
            left = mid
        else:
            right = mid
    # Engineering padding; not a formal directed-rounding certificate.
    return max(0.0, lo - 1e-12), min(1.0, right + 1e-12)


def calibrated_cs(
    counts,
    shots,
    depths,
    calibration_errors,
    calibration_shots,
    guard=0.0,
    alpha_validation=0.025,
    alpha_calibration=0.025,
):
    """Fixed depth menu, stationary response at each depth, predictable sampling.

    Include every permitted depth, with zero shots for unobserved depths. Do
    not change the menu/alpha split after observing outcomes. Calibration is
    one fixed independent acquisition, reused without repeated alpha spending.
    """
    depths = _integers(depths, "depths", 0)
    counts = _integers(counts, "counts", 0)
    shots = _integers(shots, "shots", 0)
    if (
        len(depths) != len(shots)
        or len(counts) != len(shots)
        or any(counts > shots)
        or len(set(depths)) != len(depths)
        or not math.isfinite(guard)
        or not 0 <= guard <= 1
        or not 0 < alpha_validation < 1
        or not 0 < alpha_calibration < 1
        or alpha_validation + alpha_calibration >= 1
    ):
        raise ValueError("invalid fixed-menu inference input")
    low, high = clopper_pearson(calibration_errors, calibration_shots, alpha_calibration / 2)
    if len(low) != 2:
        raise ValueError("two calibration states required")
    fl, gl = [max(0.0, v - guard - ROUNDING) for v in low]
    fu, gu = [min(1.0, v + guard + ROUNDING) for v in high]
    alpha = alpha_validation + alpha_calibration
    if fu + gu >= 1:
        return ConfidenceSet(((0.0, 1.0),), alpha)
    result = [(0.0, math.pi / 2)]
    for s, n, k in zip(counts, shots, depths):
        qlo, qhi = bernoulli_cs(int(s), int(n), alpha_validation / len(depths))
        plo = max(0.0, (qlo - ROUNDING - fu) / (1 - fu - gl) - ROUNDING)
        phi = min(1.0, (qhi + ROUNDING - fl) / (1 - fl - gu) + ROUNDING)
        if plo > phi:
            return ConfidenceSet((), alpha)
        result = intersect(result, sine_preimage(plo, phi, int(k)))
    return ConfidenceSet(
        tuple(
            (max(0.0, math.sin(a) ** 2 - ROUNDING), min(1.0, math.sin(b) ** 2 + ROUNDING))
            for a, b in result
        ),
        alpha,
    )
