"""Prospective dollar-error/resource interface; not a proof or noise model.

Evidence labels are attestations supplied by the caller, not verified proofs.
Unknown bounds/costs are never silently replaced with zero. Archived encodings
remain unchanged; the adapter below is opt-in for new experiments.
"""

from dataclasses import dataclass
import math
from typing import Optional, Tuple

from .encoding_decision import Encoding


BIAS_COMPONENTS = (
    "tail_and_renormalization", "discretization", "state_preparation",
    "payoff_arithmetic", "rotation_synthesis", "numerical_enclosure",
)
STAGES = ("setup", "pilot", "calibration_0", "calibration_1", "pricing")


def _text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be nonempty text")


def _finite(value, name, positive=False, signed=False):
    if (isinstance(value, bool) or not isinstance(value, (int, float))
            or not math.isfinite(value)
            or (not signed and (value <= 0 if positive else value < 0))):
        raise ValueError(f"invalid {name}")


@dataclass(frozen=True)
class BiasComponent:
    name: str
    bound: Optional[float]
    evidence: str
    observed_error: Optional[float] = None

    def __post_init__(self):
        if self.name not in BIAS_COMPONENTS:
            raise ValueError("unknown bias component")
        _text(self.evidence, "evidence or missing-bound explanation")
        if self.bound is not None:
            _finite(self.bound, "price-unit bound")
        if self.observed_error is not None:
            _finite(self.observed_error, "observed error", signed=True)


@dataclass(frozen=True)
class PriceContract:
    target_id: str
    target_definition: str
    currency: str
    encoding_name: str
    offset: float
    sensitivity: float
    components: Tuple[BiasComponent, ...]
    composition_evidence: str
    assumptions: Tuple[str, ...]

    def __post_init__(self):
        for name in ("target_id", "target_definition", "currency", "encoding_name",
                     "composition_evidence"):
            _text(getattr(self, name), name)
        _finite(self.offset, "offset", signed=True)
        _finite(self.sensitivity, "sensitivity", positive=True)
        if (not isinstance(self.components, tuple)
                or not all(isinstance(c, BiasComponent) for c in self.components)
                or len(self.components) != len(BIAS_COMPONENTS)
                or {c.name for c in self.components} != set(BIAS_COMPONENTS)):
            raise ValueError("one immutable entry per bias component required")
        if not isinstance(self.assumptions, tuple) or not self.assumptions:
            raise ValueError("explicit immutable assumptions required")
        for assumption in self.assumptions:
            _text(assumption, "assumption")

    @property
    def bias_bound(self):
        """Sum supplied price-unit bounds, conditional on composition evidence.

        This float sum is not directed-rounding certification. The numerical
        enclosure component must cover relevant computational rounding errors.
        """
        if any(c.bound is None for c in self.components):
            return None
        try:
            result = math.fsum(c.bound for c in self.components)
        except OverflowError as exc:
            raise ValueError("bias sum overflow") from exc
        if not math.isfinite(result):
            raise ValueError("nonfinite bias sum")
        return result

    def readiness(self, tolerance):
        """Representation screen only, never a delivered-price certificate."""
        _finite(tolerance, "tolerance", positive=True)
        bound = self.bias_bound
        if bound is None:
            return "unknown_bias"
        if bound >= tolerance:
            return "bias_bound_exhausts_tolerance"
        return "eligible_for_statistical_design"

    def to_encoding(self, cost_per_shot):
        """Explicit adapter; caller must use a single consistent cost axis."""
        if self.bias_bound is None:
            raise ValueError("unknown bias cannot enter certification planner")
        return Encoding(self.encoding_name, self.sensitivity, self.offset,
                        self.bias_bound, cost_per_shot)


@dataclass(frozen=True)
class ResourceEntry:
    stage: str
    kind: str
    evidence: str
    shots: Optional[int] = None
    logical_cx: Optional[int] = None
    elapsed_seconds: Optional[float] = None

    def __post_init__(self):
        if self.stage not in STAGES or self.kind not in ("measured", "projected"):
            raise ValueError("invalid resource stage or evidence kind")
        _text(self.evidence, "resource provenance")
        for name in ("shots", "logical_cx"):
            value = getattr(self, name)
            if value is not None and (
                isinstance(value, bool) or not isinstance(value, int) or value < 0
            ):
                raise ValueError(f"invalid {name}")
        if self.elapsed_seconds is not None:
            _finite(self.elapsed_seconds, "elapsed seconds")


def resource_totals(entries):
    """Sum disjoint stage totals in separate units, including failed attempts.

    Exactly one entry per stage forces explicit zero/not-applicable accounting.
    Stages must be nonoverlapping for elapsed-time addition; concurrent spans
    require a different accounting model. Depth/qubits are not additive here.
    """
    entries = tuple(entries)
    if (len(entries) != len(STAGES)
            or not all(isinstance(e, ResourceEntry) for e in entries)
            or {e.stage for e in entries} != set(STAGES)):
        raise ValueError("one total per acquisition stage required")
    if len({e.kind for e in entries}) != 1:
        raise ValueError("measured and projected costs cannot be mixed")
    totals = {"kind": entries[0].kind}
    for name in ("shots", "logical_cx", "elapsed_seconds"):
        values = [getattr(e, name) for e in entries]
        if any(v is None for v in values):
            totals[name] = None
        elif name == "elapsed_seconds":
            try:
                totals[name] = math.fsum(values)
            except OverflowError as exc:
                raise ValueError("elapsed-time sum overflow") from exc
            if not math.isfinite(totals[name]):
                raise ValueError("nonfinite elapsed-time sum")
        else:
            totals[name] = sum(values)
    return totals
