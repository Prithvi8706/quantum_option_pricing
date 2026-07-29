"""Annex A: the frozen 50-contract European benchmark and supported domain.

The table is GENERATED from the construction rule and the strata grid, then
asserted against the frozen literal values in the spec by the test suite. That
direction matters: the rule is normative, the printed table is its rendering.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

K_FIXED = 100.0
R_FIXED = 0.05
WEIGHT = 0.02

MONEYNESS = ((0.80, "M1 deep OTM"), (0.90, "M2 OTM"), (1.00, "M3 ATM"),
             (1.10, "M4 ITM"), (1.20, "M5 deep ITM"))
MATURITY = ((0.25, "T1 short"), (0.50, "T2 short"), (1.00, "T3 medium"),
            (1.50, "T4 long"), (2.00, "T5 long"))
VOLATILITY = ((0.15, "V1 low"), (0.30, "V2 high"))

R_MIN_RATE, R_MAX_RATE = 0.0, 0.10
T_MIN, T_MAX = 0.25, 2.00
SIGMA_MIN, SIGMA_MAX = 0.15, 0.30


class DomainError(ValueError):
    """Raised for any input outside the supported research domain."""

    def __init__(self, code: str, detail: str) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code


@dataclass(frozen=True)
class Contract:
    id: str
    S0: float
    K: float
    r: float
    T: float
    sigma: float
    m_F: float  # noqa: N815
    m_stratum: str
    t_stratum: str
    vol_stratum: str
    weight: float


def _build() -> tuple[Contract, ...]:
    rows = []
    idx = 1
    for m_F, m_label in MONEYNESS:
        for T, t_label in MATURITY:
            for sigma, v_label in VOLATILITY:
                S0 = round(100.0 * m_F * math.exp(-R_FIXED * T), 8)
                rows.append(Contract(
                    id=f"E{idx:03d}", S0=S0, K=K_FIXED, r=R_FIXED, T=T,
                    sigma=sigma, m_F=m_F, m_stratum=m_label,
                    t_stratum=t_label, vol_stratum=v_label, weight=WEIGHT,
                ))
                idx += 1
    return tuple(rows)


BENCHMARK: tuple[Contract, ...] = _build()
_BY_ID = {c.id: c for c in BENCHMARK}


def by_id(cid: str) -> Contract:
    return _BY_ID[cid]


def validate_domain(S0: float, K: float, r: float, T: float, sigma: float,
                    dividend: float = 0.0) -> None:
    """Reject any out-of-domain input with a named error. Never clamps."""
    if S0 <= 0:
        raise DomainError("NONPOSITIVE_SPOT", f"S0={S0}")
    if K <= 0:
        raise DomainError("NONPOSITIVE_STRIKE", f"K={K}")
    if not R_MIN_RATE <= r <= R_MAX_RATE:
        raise DomainError("RATE_OUT_OF_RANGE", f"r={r}")
    if not T_MIN <= T <= T_MAX:
        raise DomainError("MATURITY_OUT_OF_RANGE", f"T={T}")
    if not SIGMA_MIN <= sigma <= SIGMA_MAX:
        raise DomainError("VOLATILITY_OUT_OF_RANGE", f"sigma={sigma}")
    if dividend != 0.0:
        raise DomainError("NONZERO_DIVIDEND_UNSUPPORTED", f"q={dividend}")
