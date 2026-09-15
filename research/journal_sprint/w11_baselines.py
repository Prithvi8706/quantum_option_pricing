"""Method-specific setup and fresh, separately costed classical deployments."""

import math
import time

import numpy as np

from .asian_basket import estimate, fit_control, lognormal_call, pca_factor
from .storage import rng_for


METHODS = ("mc_cv", "rqmc_raw", "rqmc_cv", "conditional_cv")
NAMESPACE = "w11_baselines_v1"


def seed_for(*keys):
    return int(rng_for(NAMESPACE, *keys).integers(0, 2**32 - 1))


def method_setup(contract, method):
    """Same covariance/mean as historical setup, only needed factorization.

    The scalar analytic control mean remains shared setup, including for raw
    RQMC. No second, unused eigendecomposition is charged to a raw method.
    """
    if method not in METHODS:
        raise ValueError("unknown baseline")
    d, steps = contract.assets, contract.dates
    times = np.linspace(contract.maturity / steps, contract.maturity, steps)
    covariance = contract.sigma**2 * np.kron(
        (1 - contract.correlation) * np.eye(d) + contract.correlation,
        np.minimum.outer(times, times),
    )
    means = np.tile(math.log(contract.spot)
                    + (contract.rate - contract.sigma**2 / 2) * times, d)
    model = dict(means=means, covariance=covariance,
                 expected_control=float(lognormal_call(
                     float(means.mean()), float(covariance.mean()), contract.strike
                 ) * math.exp(-contract.rate * contract.maturity)))
    if method == "conditional_cv":
        load = contract.sigma * math.sqrt(contract.correlation) * np.tile(
            times / math.sqrt(contract.maturity), d
        )
        model.update(load=load, residual=pca_factor(covariance - np.outer(load, load)))
    else:
        model["factor"] = pca_factor(covariance)
    return model


def pilot_schedule():
    """Four global warmups followed by 128 blocked, interleaved deployments."""
    rows = []
    for method in METHODS:
        rows.append(dict(assets=2, dates=12, strike=100., power=8,
                         rep=0, method=method, phase="warmup"))
    for assets in (2, 4):
        for dates in (12, 52):
            for power in (8, 10):
                for rep in range(4):
                    order = rng_for(NAMESPACE, "order", assets, dates, power, rep).permutation(
                        len(METHODS)
                    )
                    for i in order:
                        rows.append(dict(assets=assets, dates=dates, strike=100., power=power,
                                         rep=rep, method=METHODS[int(i)], phase="pilot"))
    return [dict(row, attempt=i) for i, row in enumerate(rows)]


def deployment(contract, spec):
    """One standalone deployment, with a fresh training stream per method/run."""
    method = spec["method"]
    keys = (spec["phase"], spec["assets"], spec["dates"], spec["strike"],
            spec["power"], spec["rep"], method)
    before = time.perf_counter()
    model = method_setup(contract, method)
    setup_seconds = time.perf_counter() - before
    beta, training_residual = 0., 0.
    training_count = 0 if method == "rqmc_raw" else 1024
    before = time.perf_counter()
    if training_count:
        beta, training_residual = fit_control(
            contract, model, rng_for(NAMESPACE, "training", *keys),
            conditional=method == "conditional_cv", count=training_count,
        )
    training_seconds = time.perf_counter() - before if training_count else 0.
    before = time.perf_counter()
    value, residual = estimate(contract, model, spec["power"],
                               seed_for("evaluation", *keys), method, beta)
    evaluation_seconds = time.perf_counter() - before
    return dict(value=value, beta=beta, training_count=training_count,
                evaluation_count=2**spec["power"],
                max_root_residual=max(residual, training_residual),
                setup_seconds=setup_seconds, training_seconds=training_seconds,
                evaluation_seconds=evaluation_seconds,
                standalone_seconds=setup_seconds + training_seconds + evaluation_seconds,
                amortized_10_seconds=evaluation_seconds + (setup_seconds+training_seconds)/10,
                amortized_100_seconds=evaluation_seconds + (setup_seconds+training_seconds)/100)
