"""Preselected encoding and paid-pilot allocation; forecasts are not certificates."""

import math

from .calibrated_readout import invert_calibrated
from .encoding_decision import _integer, _number
from .intervals import price_decision


def preselect(encodings, tolerance=1.0):
    """Noiseless design proxy, not a dominance proof with different readout rates."""
    _number(tolerance, "tolerance", strict=True)
    if not encodings or len({e.name for e in encodings}) != len(encodings):
        raise ValueError("nonempty unique encoding menu required")
    scores = []
    for e in encodings:
        # Log score avoids overflow and preserves the finite positive cost ordering.
        score = None if e.bias >= tolerance else (
            math.log(e.cost_per_shot) + 2 * math.log(e.sensitivity)
            - 2 * math.log(tolerance - e.bias)
        )
        scores.append(dict(encoding=e.name, log_proxy=score))
    eligible = [s for s in scores if s["log_proxy"] is not None]
    chosen = min(eligible, key=lambda s: (s["log_proxy"], s["encoding"])) if eligible else None
    return dict(selected=None if chosen is None else chosen["encoding"], scores=scores)


def cp_decision(encoding, count, shots, calibration, cal_shots, guard=0.0, tolerance=1.0):
    """Terminal inference with fresh fixed-size acquisitions, not the pilot."""
    _integer(shots, "shots", 1)
    _integer(count, "count")
    _integer(cal_shots, "cal_shots", 1)
    if count > shots or len(calibration) != 2:
        raise ValueError("invalid terminal counts")
    for s in calibration:
        _integer(s, "calibration count")
        if s > cal_shots:
            raise ValueError("invalid calibration count")
    confidence, _ = invert_calibrated(
        [count], [shots], [0], calibration, [cal_shots, cal_shots],
        transfer_bounds=(guard, guard),
    )
    raw = price_decision(confidence, encoding.sensitivity, encoding.offset,
                         encoding.bias, tolerance)
    return dict(status=raw["status"], radius=raw["radius"],
                interval=None if raw["interval"] is None else list(raw["interval"]))


def allocate(
    encoding, pilot_successes, pilot_shots=1024, total_budget=65536, guard=0.0,
    menu=(1024, 4096, 8192, 16384, 24576), design_readout=(0.02, 0.07),
):
    """Freeze m,n after pilot; forecast only. No actual validation input accepted.

    The design noise assumption influences efficiency, not terminal CP validity.
    Even an unfavorable forecast is executed to evaluate that heuristic honestly.
    """
    _integer(pilot_shots, "pilot_shots", 1)
    _integer(pilot_successes, "pilot_successes")
    _integer(total_budget, "total_budget", 1)
    if pilot_successes > pilot_shots or not menu or len(set(menu)) != len(menu):
        raise ValueError("invalid pilot/menu")
    if len(design_readout) != 2:
        raise ValueError("two design rates required")
    for rate in design_readout:
        _number(rate, "design rate")
    if sum(design_readout) >= 1:
        raise ValueError("positive design contrast required")
    qhat = pilot_successes / pilot_shots
    forecasts = []
    for m in menu:
        _integer(m, "calibration allocation", 1)
        n = total_budget - pilot_shots - 2 * m
        if n < 1:
            raise ValueError("all menu entries must leave positive validation budget")
        projected_cal = [int(round(m * r)) for r in design_readout]
        projected = cp_decision(encoding, int(round(n * qhat)), n, projected_cal, m, guard)
        forecasts.append(dict(calibration_per_state=m, pricing_shots=n,
                              projected_radius=projected["radius"]))
    usable = [f for f in forecasts if f["projected_radius"] is not None]
    # Incompatibility of the forecast with the design model is not grounds to
    # invent data or return a certificate. Fall back to the first declared entry.
    best = min(usable, key=lambda f: (f["projected_radius"], f["calibration_per_state"])) \
        if usable else forecasts[0]
    return dict(calibration_per_state=best["calibration_per_state"],
                pricing_shots=best["pricing_shots"], pilot_shots=pilot_shots,
                total_shots=total_budget, forecasts=forecasts,
                forecast_only=True)
