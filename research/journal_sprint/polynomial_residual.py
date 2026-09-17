"""Finite-model moment controls and QSP preconditioning development."""

import math
import numpy as np
from numpy.polynomial import Polynomial, Chebyshev
from numpy.polynomial.chebyshev import chebval
from scipy.optimize import least_squares
from .combined_qsp import abs_polynomial, response


def compositions(total, dimensions):
    if dimensions == 1:
        yield (total,)
    else:
        for first in range(total+1):
            for rest in compositions(total-first, dimensions-1):
                yield (first,)+rest


def basket_moments(means, factor, nodes, marginal, degree):
    """E[A^k], k<=degree, for the product-normal FINITE distribution."""
    means, factor, nodes, marginal = map(np.asarray, (means, factor, nodes, marginal))
    dimension = len(means)
    if type(degree) is not int or not 0 <= degree <= 8 or not 1 <= dimension <= 8:
        raise ValueError("bounded moment expansion requires degree<=8,dimension<=8")
    if factor.shape != (dimension, dimension) or nodes.shape != marginal.shape or not np.isclose(marginal.sum(), 1):
        raise ValueError("moment model shape/probability mismatch")
    if not all(np.isfinite(a).all() for a in (means, factor, nodes, marginal)) or np.any(marginal < 0):
        raise ValueError("invalid finite model")
    moments, terms = [], 0
    for power in range(degree+1):
        values = []
        for alpha in compositions(power, dimension):
            multinomial = math.factorial(power)//math.prod(math.factorial(a) for a in alpha)
            alpha = np.asarray(alpha)
            loading = alpha @ factor
            independent = np.prod([marginal @ np.exp(value*nodes) for value in loading])
            values.append(multinomial*math.exp(float(alpha @ means))*independent/dimension**power)
            terms += 1
        moments.append(math.fsum(values))
    return np.asarray(moments), terms


def polynomial_control(basket_values, strike, radius, discount, moments, degree=4):
    coefficients, tail = abs_polynomial(degree)
    p = Chebyshev(coefficients*(1+tail)).convert(kind=Polynomial)
    variable = Polynomial([-strike/radius, 1/radius])
    control = discount*radius/2*(variable+p(variable))
    expectation = float(control.coef @ moments[:len(control.coef)])
    return control(basket_values), expectation


def residual_synthesis(high, low=4):
    if high <= low:
        raise ValueError("high degree must exceed control degree")
    high_coefficients, high_tail = abs_polynomial(high)
    low_coefficients, low_tail = abs_polynomial(low)
    coefficients = high_coefficients*(1+high_tail)
    coefficients[:low+1] -= low_coefficients*(1+low_tail)
    rho = 1.001*float(np.sum(abs(coefficients)))  # small synthesis slack below |P|=1
    normalized = coefficients/rho
    nodes = np.cos(np.pi*(np.arange(4*high+1)+.5)/(4*high+1))
    target = chebval(nodes, normalized)
    attempts, candidates = [], []
    for seed in (1201, 1202, 1203):
        initial = np.random.default_rng(seed).uniform(-np.pi, np.pi, high+1)
        fit = least_squares(lambda phases: response(nodes, phases).real-target, initial,
                            max_nfev=1500, ftol=1e-12, xtol=1e-12, gtol=1e-12)
        error = float(np.max(abs(response(nodes, fit.x).real-target)))
        attempts.append(dict(seed=seed, evaluations=int(fit.nfev), solver_success=bool(fit.success), node_error=error))
        candidates.append((error, seed, fit.x))
    _, seed, phases = min(candidates, key=lambda item: (item[0], item[1]))
    mesh = np.linspace(-1, 1, 4097)
    error = float(np.max(abs(response(mesh, phases).real-chebval(mesh, normalized))))
    return dict(high=high, low=low, coefficients=coefficients.tolist(), rho=rho,
                phases=phases.tolist(), attempts=attempts, selected_seed=seed,
                sampled_phase_error=error, fit_accepted=error < 1e-8,
                uniform_phase_certificate=False)
