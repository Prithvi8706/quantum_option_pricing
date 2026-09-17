"""Partial, directed enclosures for the existing Gaussian midpoint encoding.

No circuit is constructed, no payoff table is enumerated, and no application is
admitted: preparation, arithmetic and rotation errors remain separately unknown.
See CONFIRMATION_GATE_BOUNDS.md for target semantics and proofs.
"""

from dataclasses import replace
from decimal import Decimal
import math

from .decimal_enclosure import Interval as I, normal_cdf, product  # noqa: N817
from .price_contract import BiasComponent


def _decimal_parameter(value):
    # Business parameters are exact decimals spelled by str(value); archived
    # binary model coefficients instead enter as exact binary-float values.
    return I(str(value))


def _cap_probability(value):
    return I(max(Decimal(0), value.lo), min(Decimal(1), value.hi))


def _sum_square(values):
    return sum((value.absolute() ** 2 for value in values), I(0))


def _tilted_mass(row, cutoff):
    return product(_cap_probability(normal_cdf(cutoff - b) - normal_cdf(-cutoff - b)) for b in row)


def _price_coupling(mean_a, var_a, mean_b, var_b, factor_distance):
    log_distance = ((mean_a - mean_b).absolute() ** 2 + factor_distance**2).sqrt()
    second_moment = (2 * ((2 * mean_a + 2 * var_a).exp() + (2 * mean_b + 2 * var_b).exp())).sqrt()
    return log_distance * second_moment


def base_enclosure(contract, model, cutoff, representation):
    if representation not in ("raw", "residual"):
        raise ValueError("unknown representation")
    if isinstance(cutoff, bool) or not math.isfinite(cutoff) or not 0.5 <= cutoff <= 6:
        raise ValueError("cutoff must lie in [0.5,6]")
    dim = contract.assets * contract.dates
    if dim > 32:
        raise ValueError("bounded audit supports at most32 Gaussian dimensions")
    if len(model["means"]) != dim or len(model["factor"]) != dim:
        raise ValueError("model dimensions mismatch")
    if any(len(row) != dim for row in model["factor"]):
        raise ValueError("factor must be square")
    means = [I(float(x)) for x in model["means"]]
    factor = [[I(float(x)) for x in row] for row in model["factor"]]
    if any(x.absolute().hi > 2 for row in factor for x in row):
        raise ValueError("factor coefficient outside supported [-2,2]")
    if any(x.absolute().hi > 30 for x in means):
        raise ValueError("log mean outside supported [-30,30]")
    cutoff = _decimal_parameter(cutoff)
    spot, sigma, rate, maturity, correlation, strike = (
        _decimal_parameter(getattr(contract, name))
        for name in ("spot", "sigma", "rate", "maturity", "correlation", "strike")
    )
    dt = maturity / contract.dates
    times = [dt * (i % contract.dates + 1) for i in range(dim)]
    true_means = [spot.ln() + (rate - sigma * sigma / 2) * t for t in times]
    covariance = [
        [
            sigma
            * sigma
            * dt
            * min(i % contract.dates + 1, j % contract.dates + 1)
            * (I(1) if i // contract.dates == j // contract.dates else correlation)
            for j in range(dim)
        ]
        for i in range(dim)
    ]
    approx_cov = [
        [sum((factor[i][k] * factor[j][k] for k in range(dim)), I(0)) for j in range(dim)]
        for i in range(dim)
    ]
    residual_norm = _sum_square(
        approx_cov[i][j] - covariance[i][j] for i in range(dim) for j in range(dim)
    ).sqrt()
    # For positive equicorrelation, lambda_min(R)>=1-rho; uniform Brownian
    # temporal covariance has lambda_min>=dt/4 (also safe for one date).
    eigen_lower = sigma * sigma * (1 - correlation) * dt / 4
    factor_distance = residual_norm / eigen_lower.sqrt()
    discount = (-rate * maturity).exp()
    bridge = (
        discount
        * sum(
            (
                _price_coupling(
                    means[i], approx_cov[i][i], true_means[i], covariance[i][i], factor_distance
                )
                for i in range(dim)
            ),
            I(0),
        )
        / dim
    )

    marginal_mass = _cap_probability(normal_cdf(cutoff) - normal_cdf(-cutoff))
    cube_mass = marginal_mass**dim
    if cube_mass.lo <= 0:
        raise ArithmeticError("cube mass not bounded away from zero")
    expected = [(means[i] + approx_cov[i][i] / 2).exp() for i in range(dim)]
    tilted = [_tilted_mass(row, cutoff) for row in factor]
    conditional = [expected[i] * tilted[i] / cube_mass for i in range(dim)]
    omitted_upper = discount * sum((expected[i] * (1 - tilted[i]) for i in range(dim)), I(0)) / dim
    negative_upper = (1 - cube_mass) * discount * sum(conditional, I(0)) / dim
    # Signed truncation identity gives max(T,(1-p)*conditional upper), not sum.
    tail = I(max(omitted_upper.lo, negative_upper.lo), max(omitted_upper.hi, negative_upper.hi))
    terms = [
        (discount * conditional[i] / dim, sum((x.absolute() for x in factor[i]), I(0)))
        for i in range(dim)
    ]
    offset_error = I(0)
    control_interval = None
    cube_spot_upper = (
        sum(
            (
                (means[i] + cutoff * sum((x.absolute() for x in factor[i]), I(0))).exp()
                for i in range(dim)
            ),
            I(0),
        )
        / dim
    )
    raw_scale = discount * I(
        max(Decimal(0), (cube_spot_upper - strike).lo),
        max(Decimal(0), (cube_spot_upper - strike).hi),
    )
    safe_scale = raw_scale
    if representation == "residual":
        # Hoeffding's bounded-log spread inequality: A-G <= A*(1-exp(-R^2/8)).
        spreads = [
            (means[i] - means[j]).absolute()
            + cutoff * sum(((factor[i][k] - factor[j][k]).absolute() for k in range(dim)), I(0))
            for i in range(dim)
            for j in range(dim)
        ]
        spread_upper = I(max(x.hi for x in spreads))
        gap_scale = discount * cube_spot_upper * (1 - (-(spread_upper**2) / 8).exp())
        safe_scale = I(
            max(Decimal(0), min(raw_scale.lo, gap_scale.lo)), min(raw_scale.hi, gap_scale.hi)
        )
        geom_mean = sum(means, I(0)) / dim
        geom_factor = [sum((factor[i][j] for i in range(dim)), I(0)) / dim for j in range(dim)]
        geom_variance = _sum_square(geom_factor)
        geom_conditional = (geom_mean + geom_variance / 2).exp() * (
            _tilted_mass(geom_factor, cutoff) / cube_mass
        )
        terms.append((discount * geom_conditional, sum((x.absolute() for x in geom_factor), I(0))))
        true_geom_mean = sum(true_means, I(0)) / dim
        true_geom_variance = sum((x for row in covariance for x in row), I(0)) / dim**2
        bridge += discount * _price_coupling(
            geom_mean,
            geom_variance,
            true_geom_mean,
            true_geom_variance,
            factor_distance / I(dim).sqrt(),
        )
        sd = true_geom_variance.sqrt()
        d2 = (true_geom_mean - strike.ln()) / sd
        control_interval = discount * (
            (true_geom_mean + true_geom_variance / 2).exp() * normal_cdf(d2 + sd)
            - strike * normal_cdf(d2)
        )
        offset_error = (I(float(model["expected_control"])) - control_interval).absolute()
    return dict(
        tail=tail,
        bridge=bridge,
        offset_error=offset_error,
        terms=terms,
        cutoff=cutoff,
        dim=dim,
        cube_mass=cube_mass,
        covariance_residual=residual_norm,
        factor_distance=factor_distance,
        control_interval=control_interval,
        representation=representation,
        safe_scale=safe_scale,
    )


def at_precision(base, precision):
    if isinstance(precision, bool) or not isinstance(precision, int) or not 1 <= precision <= 32:
        raise ValueError("precision must be an integer in [1,32]")
    h = base["cutoff"] / 2**precision
    discretization = sum((weight * ((h * norm).exp() - 1) for weight, norm in base["terms"]), I(0))
    partial = base["tail"] + discretization + base["bridge"] + base["offset_error"]
    record = {
        name: base[name].record()
        for name in (
            "tail",
            "bridge",
            "offset_error",
            "cube_mass",
            "covariance_residual",
            "factor_distance",
        )
    }
    record.update(
        precision=precision,
        representation=base["representation"],
        discretization=discretization.record(),
        partial_sum=partial.record(),
        normal_qubits=base["dim"] * precision,
        payoff_table_entries=str(2 ** (base["dim"] * precision)),
        missing=[
            "state_preparation",
            "payoff_arithmetic",
            "rotation_synthesis",
            "remaining_implementation_numerical_error",
        ],
        application_admitted=False,
        safe_cube_scale=base["safe_scale"].record(),
    )
    if base["control_interval"] is not None:
        record["analytic_control"] = base["control_interval"].record()
    return record


def upward_float(upper):
    value = float(upper)
    if not math.isfinite(value):
        raise ValueError("upper bound does not fit finite float")
    if Decimal.from_float(value) < upper:
        value = math.nextafter(value, math.inf)
    if not math.isfinite(value):
        raise ValueError("outward upper bound does not fit finite float")
    return value


def screened_contract(original, record):
    """Opt-in stronger partial bounds; never fills unknown implementation errors.

    Caller must provide the matching archived encoding/model. This function is
    not a cryptographic identity check or complete numerical-error certificate.
    """
    if original.encoding_name != record["representation"]:
        raise ValueError("representation mismatch")
    known = {"tail_and_renormalization": record["tail"], "discretization": record["discretization"]}
    parts = []
    for component in original.components:
        if component.name in known:
            parts.append(
                BiasComponent(
                    component.name,
                    upward_float(Decimal(known[component.name]["upper"])),
                    "directed enclosure; CONFIRMATION_GATE_BOUNDS derivation",
                )
            )
        else:
            # Partial record does not discharge ANY preexisting implementation attestation.
            parts.append(
                BiasComponent(component.name, None, "not discharged by partial encoding enclosure")
            )
    return replace(
        original,
        components=tuple(parts),
        assumptions=original.assumptions
        + ("partial model bridge/offset recorded separately; full implementation budget unknown",),
    )
