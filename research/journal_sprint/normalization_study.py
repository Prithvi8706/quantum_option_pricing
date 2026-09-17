"""Directed scales and coefficient bridges for the bounded approximation study."""

import numpy as np
from .decimal_enclosure import Interval as I, pi_interval, product
from .encoding_enclosure import upward_float
from .combined_qsp import abs_polynomial


def radius_enclosures(means, factor, strike, cutoff):
    if len(means) == 0 or len(factor) != len(means) or any(len(r) != len(means) for r in factor):
        raise ValueError("nonempty square model required")
    if not np.isfinite([strike, cutoff]).all() or strike < 0 or cutoff <= 0:
        raise ValueError("invalid strike/cutoff")
    upper, center = I(0), I(0)
    for mu, row in zip(means, factor):
        scales = [I(float(b)).absolute()*I(float(cutoff)) for b in row]
        upper += (I(float(mu))+sum(scales, I(0))).exp()/len(means)
        center += I(float(mu)).exp()*product((t.exp()+(-t).exp())/2 for t in scales)/len(means)
    centered = upper-center+(center-I(float(strike))).absolute()
    original = upper+I(float(strike))
    return dict(original=original, centered=centered, cube_basket_upper=upper, basket_center=center)


def truncated_candidate(degree):
    coefficients, _ = abs_polynomial(degree)
    # Use direct formula, so archived coefficients have a simple exact bridge.
    coefficients[0] = 2/np.pi
    for k in range(1, degree//2+1):
        coefficients[2*k] = 4/np.pi*(-1)**(k+1)/(4*k*k-1)
    error = I(0)
    for j, value in enumerate(coefficients):
        exact = 2/pi_interval() if j == 0 else I(0)
        if j and j % 2 == 0:
            k = j//2
            exact = 4/pi_interval()*(-1)**(k+1)/(4*k*k-1)
        error += (I(float(value))-exact).absolute()
    bound = 2/(pi_interval()*(degree+1))+error
    return dict(coefficients=coefficients.tolist(), solver_success=True,
                uniform_error_upper=upward_float(bound.hi),
                certificate="analytic Chebyshev tail plus directed stored-coefficient discrepancy")


def normalized_residual(high, low):
    high, low = np.asarray(high, float), np.asarray(low, float)
    if (high.ndim != 1 or low.ndim != 1 or len(high) <= len(low)
            or not np.isfinite(high).all() or not np.isfinite(low).all()):
        raise ValueError("finite nested polynomial coefficients required")
    residual = high.copy()
    residual[:len(low)] -= low
    rho = 1.001*float(np.sum(abs(residual)))
    if rho <= 0:
        raise ValueError("nonzero residual required")
    normalized = residual/rho
    error = I(0)
    for k, value in enumerate(normalized):
        desired = I(float(high[k]))-(I(float(low[k])) if k < len(low) else I(0))
        error += (desired-I(float(rho))*I(float(value))).absolute()
    return dict(coefficients=normalized.tolist(), rho=rho,
                coefficient_bridge_upper=upward_float(error.hi))
