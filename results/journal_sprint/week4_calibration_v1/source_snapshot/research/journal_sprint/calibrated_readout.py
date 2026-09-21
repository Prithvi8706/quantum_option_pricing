"""Conservative readout inversion with finite independent calibration data."""

import numpy as np

from .intervals import (
    ConfidenceSet,
    ROUNDING,
    _integers,
    clopper_pearson,
    intersect,
    sine_preimage,
)


def invert_calibrated(
    counts,
    shots,
    depths,
    calibration_errors,
    calibration_shots,
    alpha_validation=0.025,
    alpha_calibration=0.025,
):
    """Calibration entries: false positives on |0>, false negatives on |1>."""
    if not (
        0 < alpha_validation < 1
        and 0 < alpha_calibration < 1
        and alpha_validation + alpha_calibration < 1
    ):
        raise ValueError("invalid confidence allocation")
    depths = _integers(depths, "depths", 0)
    low, high = clopper_pearson(counts, shots, alpha_validation / len(depths))
    if len(low) != len(depths):
        raise ValueError("depths and observations must match")
    clow, chigh = clopper_pearson(calibration_errors, calibration_shots, alpha_calibration / 2)
    if len(clow) != 2:
        raise ValueError("exactly two calibration states are required")
    fl, gl = np.maximum(0, clow - ROUNDING)
    fu, gu = np.minimum(1, chigh + ROUNDING)
    calibration = {
        "false_positive": [float(fl), float(fu)],
        "false_negative": [float(gl), float(gu)],
        "positive_contrast_certified": bool(fu + gu < 1),
    }
    alpha = alpha_validation + alpha_calibration
    if fu + gu >= 1:
        return ConfidenceSet(((0.0, 1.0),), alpha), calibration
    result = [(0.0, np.pi / 2)]
    for qlo, qhi, depth in zip(low, high, depths):
        plo = max(0.0, (qlo - ROUNDING - fu) / (1 - fu - gl) - ROUNDING)
        phi = min(1.0, (qhi + ROUNDING - fl) / (1 - fl - gu) + ROUNDING)
        if plo > phi:
            return ConfidenceSet((), alpha), calibration
        result = intersect(result, sine_preimage(plo, phi, int(depth)))
        if not result:
            break
    return ConfidenceSet(
        tuple(
            (max(0.0, float(np.sin(l) ** 2) - ROUNDING), min(1.0, float(np.sin(u) ** 2) + ROUNDING))
            for l, u in result
        ),
        alpha,
    ), calibration
