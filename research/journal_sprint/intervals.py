"""Conservative, all-branch inversion of independent binomial observations.

Coverage is conditional on the response model and declared noise envelope.
Bonferroni and Clopper-Pearson are established methods, not new contributions.
"""

from dataclasses import dataclass
import math

import numpy as np
from scipy.stats import beta

ROUNDING = 2e-14
# At most 8194 branch candidates per inversion. Discovery uses depths <= 8.
MAX_DEPTH = 4096


@dataclass(frozen=True)
class ConfidenceSet:
    components: tuple
    alpha: float

    @property
    def hull(self):
        return (self.components[0][0], self.components[-1][1]) if self.components else None

    @property
    def midpoint(self):
        return sum(self.hull) / 2 if self.hull else None

    @property
    def radius(self):
        return (self.hull[1] - self.hull[0]) / 2 if self.hull else None

    def contains(self, value):
        return any(lo <= value <= hi for lo, hi in self.components)


def _integers(values, name, minimum):
    arr = np.asarray(values, dtype=float)
    if (
        arr.ndim != 1
        or not arr.size
        or not np.all(np.isfinite(arr))
        or np.any(arr < minimum)
        or np.any(arr != np.floor(arr))
        or np.any(arr >= 2**63)
    ):
        raise ValueError(f"{name} must be a nonempty vector of integers >= {minimum}")
    if name == "depths" and np.any(arr > MAX_DEPTH):
        raise ValueError(f"depths exceed the safe inversion maximum {MAX_DEPTH}")
    return arr.astype(np.int64)


def clopper_pearson(counts, shots, alpha):
    counts = _integers(counts, "counts", 0)
    shots = _integers(shots, "shots", 1)
    if counts.shape != shots.shape or np.any(counts > shots):
        raise ValueError("counts and shots must match, with counts <= shots")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be in (0,1)")
    lo = np.zeros(len(counts))
    hi = np.ones(len(counts))
    use = counts > 0
    lo[use] = beta.ppf(alpha / 2, counts[use], shots[use] - counts[use] + 1)
    use = counts < shots
    hi[use] = beta.ppf(1 - alpha / 2, counts[use] + 1, shots[use] - counts[use])
    return lo, hi


def merge(intervals):
    result = []
    for lo, hi in sorted(intervals):
        if lo > hi:
            continue
        if result and lo <= result[-1][1] + ROUNDING:
            result[-1] = (result[-1][0], max(result[-1][1], hi))
        else:
            result.append((lo, hi))
    return result


def sine_preimage(lo, hi, depth):
    """All theta in [0,pi/2] with sin((2k+1)theta)^2 in [lo,hi]."""
    if (
        not (0 <= lo <= hi <= 1)
        or not math.isfinite(depth)
        or not 0 <= depth <= MAX_DEPTH
        or int(depth) != depth
    ):
        raise ValueError("invalid probability interval or depth")
    d = 2 * int(depth) + 1
    left, right = math.asin(math.sqrt(lo)), math.asin(math.sqrt(hi))
    intervals = []
    for m in range(d // 2 + 1):
        for start, end in ((left, right), (math.pi - right, math.pi - left)):
            lower = max(0.0, (m * math.pi + start) / d - ROUNDING)
            upper = min(math.pi / 2, (m * math.pi + end) / d + ROUNDING)
            if lower <= upper:
                intervals.append((lower, upper))
    return merge(intervals)


def intersect(first, second):
    result = []
    i = j = 0
    while i < len(first) and j < len(second):
        lo = max(first[i][0], second[j][0])
        hi = min(first[i][1], second[j][1])
        if lo <= hi:
            result.append((lo, hi))
        if first[i][1] < second[j][1]:
            i += 1
        else:
            j += 1
    return merge(result)


def invert(counts, shots, depths, eta_bounds=(0.0, 0.0), alpha=0.05):
    if not 0 < alpha < 1:
        raise ValueError("family-wise alpha must be in (0,1)")
    depths = _integers(depths, "depths", 0)
    shots = _integers(shots, "shots", 1)
    lo, hi = clopper_pearson(counts, shots, alpha / len(depths))
    if len(depths) != len(shots):
        raise ValueError("depths and observations must match")
    if len(eta_bounds) != 2 or not 0 <= eta_bounds[0] <= eta_bounds[1] <= 1:
        raise ValueError("eta bounds must satisfy 0 <= lower <= upper <= 1")
    result = [(0.0, math.pi / 2)]
    for k, qlo, qhi in zip(depths, lo, hi):
        qlo, qhi = max(0.0, qlo - ROUNDING), min(1.0, qhi + ROUNDING)
        vmin = (1 - eta_bounds[1]) ** (2 * int(k) + 1)
        vmax = (1 - eta_bounds[0]) ** (2 * int(k) + 1)
        if vmax == 0:
            if not qlo <= 0.5 <= qhi:
                return ConfidenceSet((), alpha)
            continue
        if vmin == 0:
            # Safe outer relaxation: do not exclude any a at this depth.
            continue
        corners = [0.5 + (q - 0.5) / v for q in (qlo, qhi) for v in (vmin, vmax)]
        plo, phi = max(0.0, min(corners)), min(1.0, max(corners))
        if plo > phi:
            return ConfidenceSet((), alpha)
        result = intersect(result, sine_preimage(plo, phi, k))
        if not result:
            break
    components = tuple(
        (max(0.0, math.sin(a) ** 2 - ROUNDING), min(1.0, math.sin(b) ** 2 + ROUNDING))
        for a, b in result
    )
    return ConfidenceSet(components, alpha)


def response(probability, depths, eta=0.0):
    depths = _integers(depths, "depths", 0)
    if not 0 <= probability <= 1 or not 0 <= eta <= 1:
        raise ValueError("probability and eta must lie in [0,1]")
    d = 2 * depths + 1
    theta = np.arcsin(np.sqrt(probability))
    return 0.5 + (1 - eta) ** d * (np.sin(d * theta) ** 2 - 0.5)


def price_decision(confidence, sensitivity, offset=0.0, bias_bound=0.0, tolerance=1.0):
    """Enclose an affine price map plus an externally established absolute bias."""
    if (
        not all(math.isfinite(x) for x in (sensitivity, offset, bias_bound, tolerance))
        or sensitivity <= 0
        or bias_bound < 0
        or tolerance <= 0
    ):
        raise ValueError("invalid price transformation")
    if confidence.hull is None:
        return {"status": "incompatible", "interval": None, "radius": None}
    lo, hi = confidence.hull
    interval = (offset + sensitivity * lo - bias_bound, offset + sensitivity * hi + bias_bound)
    radius = (interval[1] - interval[0]) / 2
    return {
        "status": "precision_met" if radius <= tolerance else "unresolved",
        "interval": interval,
        "radius": radius,
    }
