"""Audit reported budget structure; not a fresh analytic error certificate."""

from fractions import Fraction as F  # noqa: N817 - exact rational arithmetic notation
import math

ARITHMETIC = {"representation", "arithmetic", "preparation", "aggregation", "decoding"}
REFLECTION = {
    "representation",
    "discount_bridge",
    "payoff",
    "residual_coefficients",
    "phase_response",
    "signal",
    "preparation",
    "projector",
    "radius_bridge",
    "offset",
    "beta_rounding",
    "decoding_rounding",
}


def verify_budget(row):
    b = row["budget"]
    parts = b["components"]
    expected = REFLECTION if row["mode"] == "reflection" else ARITHMETIC
    if set(parts) != expected:
        raise ValueError("missing or unexpected budget components")
    if type(b["deterministic_upper"]) is bool or any(type(v) is bool for v in parts.values()):
        raise ValueError("boolean is not a numerical allowance")
    values = [F(v) for v in parts.values()]
    total = F(b["deterministic_upper"])
    if total < 0 or any(v < 0 for v in values):
        raise ValueError("negative deterministic allowance")
    # Reflection reports each component rounded upward separately. Its total
    # is rounded from the unrounded sum, so allow only those individual ULPs.
    slack = sum((F(math.ulp(v)) for v in parts.values() if isinstance(v, float)), F(0))
    if sum(values) > total + slack:
        raise ValueError("reported total understates components")
    if b["physical_execution_error"] is not None or b["confirmation_admitted"] is not False:
        raise ValueError("unsupported physical admission")
    if row["mode"] != "reflection":
        if b["decoder_scale"] != 2 * b["beta_upper"] or F(b["decoder_bridge_upper"]) > F(
            parts["decoding"]
        ):
            raise ValueError("decoder bridge or scale mismatch")
    return True
