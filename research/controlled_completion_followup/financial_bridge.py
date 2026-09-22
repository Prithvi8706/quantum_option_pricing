"""Analytic expectation bounds for the existing finite compound source.

No Monte Carlo values enter these bounds. Decimal model parameters are enclosed
by interval arithmetic; only outward-rounded upper endpoints are serialized.
The financial arithmetic itself is deliberately a separate obligation.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import mpmath as mp

from research.compound_feasibility.model import MODELS


def iv(value):
    return value if hasattr(value, "_mpi_") else mp.iv.mpf(str(value))


def upper(value):
    return math.nextafter(float(value.b), math.inf)


def normal_l1_bound(random_bits):
    """Coupled one-coordinate Box--Muller error, including the first cell."""
    h = iv(2) ** (-random_bits)
    rh = mp.iv.sqrt(-2 * mp.iv.log(h))
    rm = mp.iv.sqrt(-2 * mp.iv.log(h / 2))
    radial = h * (rm - rh / 2 + 1 / rm)
    return radial + mp.iv.pi * h * (mp.iv.sqrt(mp.iv.pi / 2) + radial)


def clipping_bounds(model, time):
    """Upper bounds on E|S-clip(S)| and E|log S-clip(log S)|.

    Mills' lower bound Q(z)>=phi(z)*z/(1+z*z), z>0, implies
    E[(N(0,1)-z)+]<=phi(z)/(1+z*z). Exponential tilting and
    1-exp(-x)<=x give the stock bounds, without subtracting nearly equal tails.
    """
    t = iv(time)
    sigma, rate = iv(model.sigma), iv(model.rate)
    variance = sigma * sigma * t
    sd = mp.iv.sqrt(variance)
    mu = mp.iv.log(iv(model.spot)) + (rate - sigma * sigma / 2) * t
    lo, hi = iv(2) ** -16, iv(4096)

    def loss(z):
        if float(z.a) <= 0:
            raise ValueError("This tail formula requires positive standardized gaps")
        return mp.iv.exp(-z * z / 2) / (mp.iv.sqrt(2 * mp.iv.pi) * (1 + z * z))

    zlo = (mu - mp.iv.log(lo)) / sd
    zhi = (mp.iv.log(hi) - mu) / sd
    ztilt = (mp.iv.log(hi) - mu - variance) / sd
    log_tail = sd * (loss(zlo) + loss(zhi))
    stock_tail = lo * sd * loss(zlo) + mp.iv.exp(mu + variance / 2) * sd * loss(ztilt)
    return stock_tail, log_tail


def certificate(model, random_bits=32):
    mp.iv.dps = 70
    n = model.dates // 2
    count = model.dates
    maturity = iv(model.maturity)
    dt = maturity / count
    tau = maturity / 2
    rate = iv(model.rate)
    d0 = mp.iv.exp(-rate * tau)
    d1 = d0
    tails = [clipping_bounds(model, dt * j) for j in range(1, count + 1)]
    tau_stock, tau_log = tails[n - 1]
    normal_error = normal_l1_bound(random_bits)
    step_error = (
        iv(model.sigma)
        * mp.iv.sqrt(dt)
        * (mp.iv.sqrt(iv(model.rho)) + mp.iv.sqrt(1 - iv(model.rho)))
        * normal_error
    )
    spot_cap = iv(4096)
    # Coupling exact-date continuous GBM to the clipped process that resets at tau.
    clip_stock_errors = [tail[0] for tail in tails[:n]]
    clip_stock_errors += [
        tails[n + j - 1][0] + mp.iv.exp(rate * dt * j) * tau_stock for j in range(1, n + 1)
    ]
    clipping_price = d0 * d1 * sum(clip_stock_errors) / count
    quantization_price = d0 * d1 * spot_cap * step_error * (count + 1) / 2
    # Analytic controls use unguarded Gaussian future paths starting at the finite
    # guarded tau state. Their finite-law identity error has two terms.
    mean_return = sum(mp.iv.exp(rate * dt * j) for j in range(1, n + 1)) / n
    future_stock_tail = sum(x[0] for x in tails[n:]) / n
    future_log_tail = sum(x[1] for x in tails[n:]) / n
    arithmetic_control = (
        future_stock_tail
        + mean_return * (tau_stock + spot_cap * n * step_error)
        + spot_cap * step_error * (n + 1) / 2
    )
    geometric_log = future_log_tail + tau_log + step_error * (3 * n + 1) / 2
    # k <= 2K and x -> (k-exp(x))+ is k_+-Lipschitz in x.
    geometric_control = 2 * iv(model.strike) * geometric_log
    control_bias = d0 * d1 * (arithmetic_control + geometric_control) / 2
    total = clipping_price + quantization_price + control_bias
    return {
        "model": model.name,
        "random_bits": random_bits,
        "one_normal_L1_upper": upper(normal_error),
        "continuous_to_guarded_price_upper": upper(clipping_price),
        "guarded_to_finite_price_upper": upper(quantization_price),
        "finite_analytic_control_bias_upper": upper(control_bias),
        "law_and_controls_total_upper": upper(total),
        "financial_numerical_budget": 0.002,
        "remaining_for_arithmetic": math.nextafter(0.002 - upper(total), -math.inf),
        "passes_law_and_controls_only": upper(total) < 0.002,
        "premises": [
            "Exact real evaluation of the stated finite midpoint/guarded law",
            "Independent uniform words and the existing even split of Box--Muller pairs at tau",
            "Exact Gaussian analytic controls and real clipped policy",
            "Final numerical arithmetic and finite-policy regret are separate obligations",
        ],
    }


def control_identity_counterexample(model, random_bits=32):
    """Reachable guarded states disprove exact finite/Gaussian identity transfer."""
    mp.iv.dps = 70
    n = model.dates // 2
    dt = iv(model.maturity) / model.dates
    rate, sigma = iv(model.rate), iv(model.sigma)
    h = iv(2) ** -random_bits
    radius = mp.iv.sqrt(-2 * mp.iv.log(h / 2))
    angle = 2 * mp.iv.pi * (iv(1) / 8 + h / 2)
    # sin(angle)>cos(angle)>0 here, so this bounds every normal from below.
    zlower = radius * mp.iv.cos(angle)
    step_lower = (rate - sigma * sigma / 2) * dt + sigma * mp.iv.sqrt(dt) * (
        mp.iv.sqrt(iv(model.rho)) + mp.iv.sqrt(1 - iv(model.rho))
    ) * zlower
    tau_log_lower = mp.iv.log(iv(model.spot)) + n * step_lower
    if float(tau_log_lower.a) <= float(mp.iv.log(iv(4096)).b):
        return None
    accrued_lower = iv(4096) / model.dates
    if float(accrued_lower.a) <= model.strike:
        raise AssertionError("The advertised negative-k witness must be reachable")
    mean_return = sum(mp.iv.exp(rate * dt * j) for j in range(1, n + 1)) / n
    discount = mp.iv.exp(-rate * iv(model.maturity) / 2)
    bias = discount * iv(4096) * (mean_return - 1) / 2
    return {
        "model": model.name,
        "random_bits": random_bits,
        "radial_word": 0,
        "angular_word": 2 ** (random_bits - 3),
        "tau_log_lower": math.nextafter(float(tau_log_lower.a), -math.inf),
        "guard_log_upper": upper(mp.iv.log(iv(4096))),
        "accrued_lower": math.nextafter(float(accrued_lower.a), -math.inf),
        "conditional_control_bias_lower_before_outer_discount": math.nextafter(
            float(bias.a), -math.inf
        ),
        "past_word_event_probability_power_of_two": -random_bits * n * (model.assets + 1),
        "reason": (
            "All tau stocks equal 4096 and k<0; finite future A<=4096, "
            "Gaussian EA=4096*mean(exp(r*t))>4096"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/controlled_completion_followup/financial_bridge.json"),
    )
    args = parser.parse_args()
    rows = [certificate(model, bits) for bits in (16, 32) for model in MODELS]
    report = {
        "method": (
            "Analytic coupling inequalities, evaluated by 70-digit mpmath interval arithmetic"
        ),
        "normal_tail_method": (
            "Mills inequalities and exponential tilting; no sampled tail or quadrature"
        ),
        "rounding": "Upper interval endpoint converted to binary64 then nextafter toward +infinity",
        "status": (
            "Partial certificate: law/control bounds closed; arithmetic and policy regret remain"
        ),
        "rows": rows,
        "exact_control_identity_counterexamples": [
            witness
            for model in MODELS
            if (witness := control_identity_counterexample(model)) is not None
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
