"""Week-12 fixed-fresh-batch policies; forecasts are not certificates.

No evaluator truth or terminal observations enter planning. The acquisition
runner must enforce fresh, disjoint terminal observations after this choice.
"""

from dataclasses import dataclass
import math

from .allocation_rule import allocate
from .calibrated_readout import invert_calibrated
from .encoding_decision import Encoding, _integer, _number
from .intervals import price_decision


ARMS = ("fixed_cp", "pilot_cp", "unequal_full", "unequal_target", "fixed_target")
COUNTS = (256, 1024, 4096, 8192, 16384, 24576)
CAPS = (8192, 16384, 32768, 65536)
PILOT = 1024
DESIGN_READOUT = (.02, .07)
DESIGN_AMPLITUDE = .5  # Prior design assumption, never the evaluator amplitude.
TARGET_FRACTION = .9
Z = 2.241402727604947  # Standard-normal 0.9875 quantile; planning heuristic only.


@dataclass(frozen=True)
class BatchPlan:
    arm: str
    pilot_shots: int
    m0: int
    m1: int
    n: int
    forecast_radius: float
    forecast_target_met: bool
    rationale: str

    @property
    def total_shots(self):
        return self.pilot_shots + self.m0 + self.m1 + self.n


def _inputs(encoding, q, guard, tolerance):
    if not isinstance(encoding, Encoding):
        raise ValueError("a known-bias Encoding is required")
    _number(q, "design probability")
    _number(guard, "guard")
    _number(tolerance, "tolerance", strict=True)
    if q > 1 or guard > 1:
        raise ValueError("probability/guard outside [0,1]")


def forecast_radius(encoding, q, m0, m1, n, guard=0.):
    """Delta-method radius proxy, including a first-order transfer allowance.

This does not approximate CP joint tails reliably enough to certify delivery.
Pilot q uses Jeffreys smoothing to avoid zero estimated variance at extremes.
The declared readout model is fixed even when evaluator noise is swapped.
"""
    _inputs(encoding, q, guard, 1.)
    for count in (m0, m1, n):
        _integer(count, "forecast count", 1)
    f, g = DESIGN_READOUT
    contrast = 1-f-g
    amplitude = min(1., max(0., (q-f)/contrast))
    variance = (q*(1-q)/n + (1-amplitude)**2*f*(1-f)/m0
                + amplitude**2*g*(1-g)/m1)
    result = encoding.bias + encoding.sensitivity/contrast*(Z*math.sqrt(variance)+guard)
    if not math.isfinite(result):
        raise ValueError("nonfinite forecast")
    return result


def candidate_counts(pilot_shots, full_cap=False):
    """The same declared menu for fixed/paid target policies, paid costs included."""
    if pilot_shots not in (0, PILOT) or isinstance(pilot_shots, bool):
        raise ValueError("invalid pilot count")
    return tuple((m0, m1, cap-pilot_shots-m0-m1)
                 for cap in ((CAPS[-1],) if full_cap else CAPS)
                 for m0 in COUNTS for m1 in COUNTS
                 if cap-pilot_shots-m0-m1 >= 256)


def choose_batch(encoding, arm, pilot_successes=None, guard=0., tolerance=1.):
    """Freeze the complete batch before terminal observations.

Encoding preselection must precede any pilot; bias-exhausted encodings are
rejected here and must be recorded by the runner as zero-acquisition refusals.
Every feasible but pessimistic forecast still yields a batch, not a certificate.
"""
    if arm not in ARMS:
        raise ValueError("unknown arm")
    paid = arm in ("pilot_cp", "unequal_full", "unequal_target")
    if paid:
        _integer(pilot_successes, "pilot successes")
        if pilot_successes > PILOT:
            raise ValueError("pilot successes exceed shots")
    elif pilot_successes is not None:
        raise ValueError("fixed arm cannot inspect a current-trial pilot")
    q = ((pilot_successes+.5)/(PILOT+1) if paid else
         DESIGN_READOUT[0]+(1-sum(DESIGN_READOUT))*DESIGN_AMPLITUDE)
    _inputs(encoding, q, guard, tolerance)
    if encoding.bias >= tolerance:
        raise ValueError("preselect/refuse before acquiring pilot: bias exhausts tolerance")
    p = PILOT if paid else 0
    if arm == "fixed_cp":
        counts, rationale = (16384, 16384, 32768), "historical fixed full-cap comparator"
    elif arm == "pilot_cp":
        # Preserve the historical unsmoothed CP forecast/menu exactly.
        old = allocate(encoding, pilot_successes, guard=guard)
        counts = (old["calibration_per_state"], old["calibration_per_state"], old["pricing_shots"])
        rationale = "historical equal-calibration pilot comparator"
    else:
        candidates = [(forecast_radius(encoding, q, *c, guard), c)
                      for c in candidate_counts(p, arm == "unequal_full")]
        eligible = [(radius, c) for radius, c in candidates
                    if radius <= TARGET_FRACTION*tolerance]
        if arm != "unequal_full" and eligible:
            _, counts = min(eligible, key=lambda x: (sum(x[1])+p, x[0], *x[1]))
            rationale = "least-cost candidate meeting forecast margin"
        else:
            _, counts = min(candidates, key=lambda x: (x[0], sum(x[1])+p, *x[1]))
            rationale = "minimum forecast radius; no delivery promise"
    radius = forecast_radius(encoding, q, *counts, guard)
    return BatchPlan(arm, p, *counts, radius, radius <= TARGET_FRACTION*tolerance, rationale)


def terminal_decision(encoding, count, n, calibration, m0, m1, guard=0., tolerance=1.):
    """One terminal CP inversion; no pilot observations are accepted.

Caller must enforce independent fresh binomial batches with these fixed sizes.
Coverage is conditional on the readout/transfer and deterministic bias model.
"""
    _inputs(encoding, 0., guard, tolerance)
    for shots in (n, m0, m1):
        _integer(shots, "terminal shots", 1)
    if not isinstance(calibration, (tuple, list)) or len(calibration) != 2:
        raise ValueError("two calibration counts required")
    for successes, shots in zip((count, *calibration), (n, m0, m1)):
        _integer(successes, "terminal successes")
        if successes > shots:
            raise ValueError("successes exceed shots")
    confidence, calibration_set = invert_calibrated(
        [count], [n], [0], calibration, [m0, m1],
        alpha_validation=.025, alpha_calibration=.025,
        transfer_bounds=(guard, guard),
    )
    result = price_decision(confidence, encoding.sensitivity, encoding.offset,
                            encoding.bias, tolerance)
    return dict(status=result["status"], radius=result["radius"],
                interval=None if result["interval"] is None else list(result["interval"]),
                calibration=calibration_set)
