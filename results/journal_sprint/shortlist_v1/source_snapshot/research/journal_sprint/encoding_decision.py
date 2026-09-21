"""Finite-menu, calibration-first dollar certification for direct sampling.

Standard CP + Hoeffding bounds, not a novel quantum algorithm. No amplitude,
true price, or pricing observations enter representation selection.
"""

from dataclasses import dataclass
import math

from .intervals import clopper_pearson


def _number(value, name, minimum=0.0, strict=False):
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or (value <= minimum if strict else value < minimum)
    ):
        raise ValueError(f"invalid {name}")


def _integer(value, name, minimum=0):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"invalid {name}")


@dataclass(frozen=True)
class Encoding:
    name: str
    sensitivity: float
    offset: float
    bias: float
    cost_per_shot: float

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("encoding name required")
        _number(self.sensitivity, "sensitivity", strict=True)
        if isinstance(self.offset, bool) or not math.isfinite(self.offset):
            raise ValueError("invalid offset")
        _number(self.bias, "bias")
        _number(self.cost_per_shot, "cost_per_shot", strict=True)


@dataclass(frozen=True)
class Rectangle:
    fl: float
    fu: float
    gl: float
    gu: float

    def __post_init__(self):
        for value in (self.fl, self.fu, self.gl, self.gu):
            _number(value, "readout endpoint")
        if not 0 <= self.fl <= self.fu <= 1 or not 0 <= self.gl <= self.gu <= 1:
            raise ValueError("invalid readout rectangle")

    @property
    def contrast(self):
        return 1 - (self.fl + self.fu + self.gl + self.gu) / 2

    @property
    def uncertainty(self):
        return max(self.fu - self.fl, self.gu - self.gl) / 2


def calibration_menu(errors, shots, guard=0.0, alpha=0.025):
    """All 2*K fixed-size CP intervals jointly cover with probability >=1-alpha.

    Keys/menu, alpha, shots and guard must be fixed before calibration. Distinct
    encodings may have distinct rates; no independence across encodings is needed
    for the union bound. Each individual calibration sample must be binomial.
    """
    _integer(shots, "calibration shots", 1)
    _number(guard, "guard")
    _number(alpha, "alpha", strict=True)
    if guard > 1 or alpha >= 1 or not errors:
        raise ValueError("invalid calibration menu")
    out = {}
    for name, counts in errors.items():
        if not isinstance(name, str) or not name or len(counts) != 2:
            raise ValueError("two counts per named encoding required")
        for count in counts:
            _integer(count, "calibration count")
            if count > shots:
                raise ValueError("calibration count exceeds shots")
        low, high = clopper_pearson(counts, [shots, shots], alpha / (2 * len(errors)))
        # Engineering outward padding, not formally directed rounding.
        out[name] = Rectangle(
            max(0.0, float(low[0]) - guard - 1e-12),
            min(1.0, float(high[0]) + guard + 1e-12),
            max(0.0, float(low[1]) - guard - 1e-12),
            min(1.0, float(high[1]) + guard + 1e-12),
        )
    return out


def radius_bound(encoding, rectangle, shots, alpha_validation=0.025):
    """Uniform radius of the clipped midpoint-calibration estimator."""
    _integer(shots, "pricing shots", 1)
    _number(alpha_validation, "alpha_validation", strict=True)
    if alpha_validation >= 1 or rectangle.contrast <= 0:
        raise ValueError("invalid alpha or midpoint contrast")
    h = math.sqrt(math.log(2 / alpha_validation) / (2 * shots))
    return encoding.bias + encoding.sensitivity * (h + rectangle.uncertainty) / rectangle.contrast


def plan_menu(
    encodings,
    rectangles,
    tolerance,
    caps,
    calibration_shots,
    calibration_cost_per_shot,
    alpha_validation=0.025,
):
    """Choose the cheapest sufficient certificate, NOT the true optimal encoder.

    caps are per-encoding pricing-shot limits; acquisition cost includes ALL
    calibration states in the fixed menu. Cost units must match across inputs.
    For logical-CX ranking zero calibration CX is allowed, but those calibration
    shots are still counted. Returned plans are fixed before pricing begins.
    """
    _number(tolerance, "tolerance", strict=True)
    _integer(calibration_shots, "calibration shots", 1)
    _number(calibration_cost_per_shot, "calibration cost")
    _number(alpha_validation, "alpha_validation", strict=True)
    names = [e.name for e in encodings]
    if (
        not names or len(set(names)) != len(names)
        or set(names) != set(rectangles) or set(names) != set(caps)
        or alpha_validation >= 1
    ):
        raise ValueError("fixed menus must match")
    for cap in caps.values():
        _integer(cap, "pricing cap", 1)
    spent = 2 * len(encodings) * calibration_shots
    scores = []
    for e in encodings:
        r = rectangles[e.name]
        row = dict(encoding=e.name, status="certified", shots=None, total_cost=None)
        if e.bias >= tolerance:
            row["status"] = "bias_bound_exhausts_tolerance"
        elif r.fu + r.gu >= 1:
            row["status"] = "contrast_uncertified"
        else:
            floor = e.bias + e.sensitivity * r.uncertainty / r.contrast
            row["certificate_floor"] = floor
            margin = r.contrast * ((tolerance - e.bias) / e.sensitivity) - r.uncertainty
            if margin <= 0:
                row["status"] = "calibration_bound_exhausts_tolerance"
            elif radius_bound(e, r, caps[e.name], alpha_validation) > tolerance:
                row["status"] = "budget_not_certified"
            else:
                # Binary search avoids overflow near the calibration floor;
                # returns the smallest integer satisfying this bound within cap.
                lo, hi = 1, caps[e.name]
                while lo < hi:
                    mid = (lo + hi) // 2
                    if radius_bound(e, r, mid, alpha_validation) <= tolerance:
                        hi = mid
                    else:
                        lo = mid + 1
                row.update(
                    shots=lo,
                    radius=radius_bound(e, r, lo, alpha_validation),
                    total_cost=spent * calibration_cost_per_shot + lo * e.cost_per_shot,
                )
        scores.append(row)
    eligible = [r for r in scores if r["status"] == "certified"]
    chosen = min(eligible, key=lambda r: (r["total_cost"], r["encoding"])) if eligible else None
    return dict(
        selected=None if chosen is None else chosen["encoding"],
        shots=0 if chosen is None else chosen["shots"],
        calibration_shots=spent,
        total_shots=spent + (0 if chosen is None else chosen["shots"]),
        total_cost=spent * calibration_cost_per_shot if chosen is None else chosen["total_cost"],
        scores=scores,
    )


def fixed_price_interval(encoding, rectangle, successes, shots, alpha_validation=0.025):
    """ONE terminal interval using fresh pricing shots; not an anytime procedure."""
    _integer(successes, "pricing successes")
    radius = radius_bound(encoding, rectangle, shots, alpha_validation)
    if successes > shots:
        raise ValueError("successes exceed shots")
    fmid = (rectangle.fl + rectangle.fu) / 2
    amplitude = min(1.0, max(0.0, (successes / shots - fmid) / rectangle.contrast))
    center = encoding.offset + encoding.sensitivity * amplitude
    return center - radius, center + radius
