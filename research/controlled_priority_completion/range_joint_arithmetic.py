"""Interval-evaluated joint financial arithmetic bound for f40/q32.

The policy value cancels from baseline plus correction. This does not certify
policy regret, a tight second moment, or the separately sampled baseline mean.
"""

import json
import math
from pathlib import Path

import mpmath as mp
import numpy as np

from research.compound_feasibility.model import MODELS
from research.controlled_completion_followup.financial_bridge import iv, upper
from research.controlled_source_completion.ir import coefficients

F = 40
Q = 1 << F


def hermite(n, x):
    a, b = iv(1), x
    if n == 0:
        return a
    for k in range(1, n):
        a, b = b, x * b - k * a
    return b


def cdf_interval(x):
    """Entire erf series, with a certified alternating remainder after n=180."""
    total, power, factorial = iv(0), x, 1
    for j in range(181):
        term = power / (iv(2) ** j * factorial * (2 * j + 1))
        total += term if j % 2 == 0 else -term
        power *= x * x
        factorial *= j + 1
    tail = abs(power / (iv(2) ** 181 * factorial * 363))
    # At |x|<8 these terms decrease after j=32; n=181 is well past that.
    error = upper(tail)
    return iv(".5") + (total + mp.iv.mpf([-error, error])) / mp.iv.sqrt(2 * mp.iv.pi)


def coefficient_certificate():
    mp.iv.dps = 80
    unit = iv(1) / Q
    worst = {}
    specs = [("log", 32, 8, 1, 2), ("cos", 64, 7, 0, 1), ("cdf", 256, 7, -8, 8)]
    for name, segments, degree, lo, hi in specs:
        rows = coefficients(name, segments, degree, F)
        maximum = 0.0
        for i, row in enumerate(rows):
            center = iv(lo) + (iv(i) + iv(".5")) * (hi - lo) / segments
            for k, stored in enumerate(row):
                if name == "log":
                    exact = mp.iv.log(center) if k == 0 else ((-1) ** (k + 1)) / (k * center**k)
                elif name == "cos":
                    phase = 2 * mp.iv.pi * center + k * mp.iv.pi / 2
                    exact = (2 * mp.iv.pi) ** k * mp.iv.cos(phase) / math.factorial(k)
                elif k == 0:
                    exact = cdf_interval(center)
                else:
                    exact = (
                        ((-1) ** (k - 1)) * hermite(k - 1, center) * mp.iv.exp(-center * center / 2)
                    )
                    exact /= mp.iv.sqrt(2 * mp.iv.pi) * math.factorial(k)
                maximum = max(maximum, upper(abs(iv(stored) / Q - exact)))
        assert maximum < float(unit.a), (name, maximum)
        worst[name] = maximum
    ln2raw = round(math.log(2) * Q)
    ln2_error = abs(iv(ln2raw) / Q - mp.iv.log(2))
    hlog, hcos, hcdf = iv(1) / 64, iv(1) / 128, iv(1) / 32
    log_interp = (iv(worst["log"]) + unit) / (1 - hlog) + hlog**9 / 9
    cos_error = (iv(worst["cos"]) + unit) / (1 - hcos) + (
        2 * mp.iv.pi * hcos
    ) ** 8 / math.factorial(8)
    # |H_7(x)| <= |x|^7+21|x|^5+105|x|^3+105|x|, |x|<=8.
    derivative8 = (8**7 + 21 * 8**5 + 105 * 8**3 + 105 * 8) / mp.iv.sqrt(2 * mp.iv.pi)
    cdf_error = (iv(worst["cdf"]) + unit) / (1 - hcdf) + derivative8 * hcdf**8 / math.factorial(8)
    cdf_error += mp.iv.exp(-32) / (8 * mp.iv.sqrt(2 * mp.iv.pi))
    log_normal = log_interp + 40 * ln2_error
    log_general = log_normal + unit  # right-normalization loses less than one raw ulp
    polynomial_error = max(
        upper(abs(iv(round((1 / math.factorial(j)) * Q)) / Q - iv(1) / math.factorial(j)))
        for j in range(13)
    )
    h = iv(".694")
    exp_error = (
        iv(8192)
        * (
            (iv(polynomial_error) + unit) / (1 - h)
            + mp.iv.exp(h) * h**13 / math.factorial(13)
            + mp.iv.exp(h + 18 * ln2_error) * 18 * ln2_error
        )
        + unit
    )
    inverse_log2 = round((1 / math.log(2)) * Q)
    xlo, xhi = -12 * Q, 9 * Q
    kmin, kmax = xlo * inverse_log2 // (Q * Q), xhi * inverse_log2 // (Q * Q)
    coefficient_product_error = Q * Q - inverse_log2 * ln2raw
    endpoints = [x * coefficient_product_error for x in (xlo, xhi)]
    reduced_lo = -((-min(endpoints)) // (Q * Q))
    reduced_hi = (max(endpoints) + ln2raw * Q * Q - 1) // (Q * Q)
    assert -18 <= kmin <= kmax <= 13
    assert max(abs(reduced_lo), abs(reduced_hi)) * 1000 <= 694 * Q
    return dict(
        coefficient_error=worst,
        log_normal=upper(log_normal),
        log_general=upper(log_general),
        cos=upper(cos_error),
        cdf=upper(cdf_error),
        exp=upper(exp_error),
        log2_coefficient_error=upper(ln2_error),
        exp_domain=[-12, 9],
        exp_integer_exponent_abs_bound=18,
        exp_binary_scale_bound=8192,
        exp_verified_integer_reduction=dict(
            kmin=kmin, kmax=kmax, raw_r_min=reduced_lo, raw_r_max=reduced_hi
        ),
    )


def checked_constants(model):
    """Verify every non-policy scalar used by the hand financial bound."""
    d, n = model.assets, model.dates // 2
    t = np.arange(1, n + 1) * (model.maturity / model.dates)
    mt = np.minimum.outer(t, t)
    dt = iv(model.maturity) / model.dates
    sigma, rate, rho = iv(model.sigma), iv(model.rate), iv(model.rho)
    times = [dt * j for j in range(1, n + 1)]
    vg = (
        sigma
        * sigma
        * (rho + (1 - rho) / d)
        * sum(min(i, j) for i in range(1, n + 1) for j in range(1, n + 1))
        * dt
        / (n * n)
    )
    vg_float = model.sigma**2 * (model.rho + (1 - model.rho) / d) * mt.mean()
    discount = mp.iv.exp(-rate * iv(model.maturity) / 2)
    discount_float = math.exp(-model.rate * model.maturity / 2)
    pairs = [
        ("logspot", math.log(model.spot), mp.iv.log(iv(model.spot))),
        ("loglow", math.log(2**-16), mp.iv.log(iv(2) ** -16)),
        ("loghigh", math.log(4096), mp.iv.log(4096)),
        (
            "common",
            model.sigma * math.sqrt(model.maturity / model.dates * model.rho),
            sigma * mp.iv.sqrt(dt * rho),
        ),
        (
            "individual",
            model.sigma * math.sqrt(model.maturity / model.dates * (1 - model.rho)),
            sigma * mp.iv.sqrt(dt * (1 - rho)),
        ),
        (
            "drift",
            (model.rate - 0.5 * model.sigma**2) * (model.maturity / model.dates),
            (rate - sigma * sigma / 2) * dt,
        ),
        ("discount", discount_float, discount),
        ("scale", 0.5 * discount_float, discount / 2),
        ("support", discount_float * model.strike, discount * iv(model.strike)),
        (
            "meanreturn",
            float(np.exp(model.rate * t).mean()),
            sum(mp.iv.exp(rate * x) for x in times) / n,
        ),
        (
            "geom_mu_shift",
            (model.rate - 0.5 * model.sigma**2) * float(t.mean()),
            (rate - sigma * sigma / 2) * sum(times) / n,
        ),
        ("geom_variance", vg_float, vg),
    ]
    for divisor in (d, d * n, d * model.dates):
        pairs.append(("mean_%d" % divisor, 1 / divisor, iv(1) / divisor))
    controls = [("geometric", vg_float, vg)]
    for j, (tj, exact_t) in enumerate(zip(t, times)):
        pairs.extend(
            [
                (
                    "mu_shift_%d" % j,
                    (model.rate - 0.5 * model.sigma**2) * tj,
                    (rate - sigma * sigma / 2) * exact_t,
                ),
                ("variance_%d" % j, model.sigma**2 * tj, sigma * sigma * exact_t),
            ]
        )
        controls.append(("upper_%d" % j, model.sigma**2 * tj, sigma * sigma * exact_t))
    rows = []
    for name, value, exact in pairs:
        raw = round(float(value) * Q)
        error = upper(abs(iv(raw) / Q - exact))
        assert error < 1 / Q, (name, error)
        rows.append(dict(name=name, raw=raw, error=error))
    # All control means lie below 5000; their exponential arguments stay in [-12,9].
    assert upper(mp.iv.exp(mp.iv.log(4096) + rate * iv(model.maturity) / 2 + iv(2) / Q)) < 5000
    return rows, controls, discount, vg, times


def domain_certificate(model, constants, elementary):
    """Exact raw domains for every financial exp and explicit magnitude caps."""
    raw = {c["name"]: c["raw"] for c in constants}
    d, n = model.assets, model.dates // 2
    lo, hi = raw["loglow"], raw["loghigh"]
    domains = [(lo, hi)]
    mean_raw = raw["mean_%d" % (d * n)]
    domains.append((d * n * lo * mean_raw // Q, d * n * hi * mean_raw // Q))
    domains.append(
        (
            lo - 1 + raw["geom_mu_shift"] + raw["geom_variance"] // 2,
            hi + raw["geom_mu_shift"] + raw["geom_variance"] // 2,
        )
    )
    mu_domains = [(lo - 1 + raw["geom_mu_shift"], hi + raw["geom_mu_shift"])]
    for j in range(n):
        domains.append(
            (
                lo + raw["mu_shift_%d" % j] + raw["variance_%d" % j] // 2,
                hi + raw["mu_shift_%d" % j] + raw["variance_%d" % j] // 2,
            )
        )
        mu_domains.append((lo + raw["mu_shift_%d" % j], hi + raw["mu_shift_%d" % j]))
    assert all(-12 * Q <= a <= b <= 9 * Q for a, b in domains)
    assert all(-12 * Q <= a <= b <= 9 * Q for a, b in mu_domains)
    stock_max = mp.iv.exp(iv(hi) / Q) + iv(elementary["exp"])
    assert upper(stock_max) < 4097
    ea_max = stock_max * iv(raw["meanreturn"]) / Q
    accrued_max = d * n * stock_max * iv(raw["mean_%d" % (d * model.dates)]) / Q
    absolute_k = max(200.0, upper(2 * accrued_max - 200))
    assert upper(ea_max + iv(absolute_k)) < 8500
    control_mean_max = mp.iv.exp(iv(max(b for _, b in domains[2:])) / Q) + iv(elementary["exp"])
    cdf_error = iv(elementary["cdf"])
    unit = iv(1) / Q
    forward_max = (ea_max + iv(absolute_k)) * iv(raw["scale"]) / Q + unit
    call_max = max(
        upper(control_mean_max * (1 + cdf_error) + 200 * cdf_error + 2 * unit),
        upper(control_mean_max + iv(absolute_k)),
    )
    call_scaled = iv(call_max) * iv(raw["scale"]) / Q + unit
    put_scaled = (200 * (1 + cdf_error) + control_mean_max * cdf_error + 2 * unit) * iv(
        raw["scale"]
    ) / Q + unit
    policy_max = max(upper(forward_max + put_scaled), upper(call_scaled))
    assert policy_max < 10000
    # Exact conditional call means at digital mu and exact variance are <5000;
    # the earlier interval check includes the largest future risk-free drift.
    return dict(
        exp_raw_domains=domains,
        mu_raw_domains=mu_domains,
        source_stock_upper=upper(stock_max),
        mean_minus_strike_abs_upper=upper(ea_max + iv(absolute_k)),
        digital_policy_upper=policy_max,
    )


def control_arithmetic(vfloat, variance, elementary):
    unit = iv(1) / Q
    vraw = round(float(vfloat) * Q)
    sd_raw = math.isqrt(vraw * Q)
    sd = iv(sd_raw) / Q
    sd_error = abs(sd - mp.iv.sqrt(variance))
    var_error = abs(iv(vraw) / Q - variance)
    # mu in [-12,9], k in [one ulp,200], so |mu-log k|<40.
    d2_error = (iv(elementary["log_general"]) + 40 * sd_error / mp.iv.sqrt(variance)) / sd + unit
    cdf_error = iv(elementary["cdf"]) + (d2_error + sd_error) / mp.iv.sqrt(2 * mp.iv.pi)
    mean_error = iv(elementary["exp"]) + 5001 * (var_error / 2 + unit)
    payoff_error = (1 + iv(elementary["cdf"])) * mean_error + 5200 * cdf_error + 2 * unit
    return payoff_error, dict(
        variance_raw=vraw,
        sd_raw=sd_raw,
        sd_error=upper(sd_error),
        d2_error=upper(d2_error),
        lognormal_payoff_error=upper(payoff_error),
    )


def certificate(model, elementary):
    constants, controls, discount, vg, times = checked_constants(model)
    unit = iv(1) / Q
    d, n, N = model.assets, model.dates // 2, model.dates
    h = iv(2) ** -32
    reciprocal_radius = mp.iv.sqrt(mp.iv.pi / 2) + mp.iv.sqrt(h)
    radial_max = mp.iv.sqrt(-2 * mp.iv.log(h / 2))
    radial_error = 2 * iv(elementary["log_normal"]) * reciprocal_radius + unit
    normal_error = (
        (1 + iv(elementary["cos"])) * radial_error + radial_max * iv(elementary["cos"]) + unit
    )
    digital_normal_abs_mean = (1 + iv(elementary["cos"])) * (
        mp.iv.sqrt(mp.iv.pi / 2) + h * radial_max + radial_error
    ) + unit
    assert upper(digital_normal_abs_mean) < 2
    step_scale = (
        iv(model.sigma)
        * mp.iv.sqrt(iv(model.maturity) / N)
        * (mp.iv.sqrt(iv(model.rho)) + mp.iv.sqrt(1 - iv(model.rho)))
    )
    step_error = step_scale * normal_error + 7 * unit
    # One initial log, up to two guard constants (including reset), all charged.
    logs = [3 * unit + j * step_error for j in range(1, N + 1)]
    exp_error = iv(elementary["exp"])
    stocks = [4097 * x + exp_error for x in logs]
    accrued_error = sum(stocks[:n]) / N + unit * (d * n * 4097 + 1)
    future_average_error = sum(stocks[n:]) / n + unit * (d * n * 4097 + 1)
    future_log_error = sum(logs[n:]) / n + unit * (d * n * 12 + 1)
    geometric_error = 4097 * future_log_error + exp_error
    k_error = 2 * accrued_error
    basket_error = stocks[n - 1] + unit * (d * 4097 + 1)
    meanreturn = sum(mp.iv.exp(iv(model.rate) * x) for x in times) / n
    ea_error = meanreturn * basket_error + unit * 4097 + unit
    forward_error = discount / 2 * (ea_error + k_error) + 8500 * unit + unit
    mu_error = logs[n - 1] + unit * (d * 12 + 2)
    controls_out = []
    call_errors = []
    for name, vfloat, v in controls:
        arithmetic, details = control_arithmetic(vfloat, v, elementary)
        controls_out.append(dict(name=name, **details))
        call_errors.append(arithmetic)
    geometric_put_error = discount / 2 * (call_errors[0] + k_error + 200 * mu_error) + 201 * unit
    geometric_call_error = discount / 2 * (call_errors[0] + k_error + 5000 * mu_error) + 9001 * unit
    c0_error = forward_error + geometric_put_error
    lower_error = forward_error + geometric_call_error
    # Each component call uses a tau log and its own rounded deterministic shift.
    call_average_error = sum(call_errors[1:]) / n + k_error + 5000 * (logs[n - 1] + unit)
    call_average_error += unit * (d * n * 9000 + 1)
    upper_average_error = discount / 2 * call_average_error + 9001 * unit
    # Projection into exact [lower,upper] costs at most 2*lower+c0+upper_average.
    projection_error = 2 * lower_error + c0_error + upper_average_error
    residual_error = (
        discount / 2 * (2 * k_error + geometric_error + future_average_error) + 401 * unit
    )
    baseline_discount_error = 10000 * unit + unit
    joint = baseline_discount_error + discount * (
        2 * c0_error + 2 * residual_error + projection_error + unit
    )
    return dict(
        model=model.name,
        fraction_bits=40,
        random_bits=32,
        constants=constants,
        verified_domains=domain_certificate(model, constants, elementary),
        control_evaluations=controls_out,
        expectation_terms={
            "normal": upper(normal_error),
            "digital_normal_absolute_mean_upper": upper(digital_normal_abs_mean),
            "one_log_increment": upper(step_error),
            "accrued": upper(accrued_error),
            "future_average": upper(future_average_error),
            "geometric": upper(geometric_error),
            "forward": upper(forward_error),
            "c0": upper(c0_error),
            "lower": upper(lower_error),
            "upper_average": upper(upper_average_error),
            "residual": upper(residual_error),
            "policy_projection": upper(projection_error),
            "joint_arithmetic_dollars": upper(joint),
        },
        uniform_numerical_budget=0.002,
        claim=(
            "Bound for joint arithmetic expectation only; same implemented digital "
            "decision and baseline/correction policy; no regret or tight-moment claim."
        ),
    )


def main():
    elementary = coefficient_certificate()
    rows = [certificate(m, elementary) for m in MODELS]
    value = dict(
        status=(
            "Deterministic joint arithmetic expectation certificate; independent AI "
            "mathematical review completed for the stated finite-path scope."
        ),
        elementary=elementary,
        models=rows,
        remaining=[
            "finite-policy regret",
            "baseline mean confidence",
            "tight moment transfer if used",
        ],
    )
    p = Path("results/controlled_priority_completion/range_joint_arithmetic.json")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, indent=2) + "\n")
    print(
        json.dumps({r["model"]: r["expectation_terms"]["joint_arithmetic_dollars"] for r in rows}),
        flush=True,
    )


if __name__ == "__main__":
    main()
