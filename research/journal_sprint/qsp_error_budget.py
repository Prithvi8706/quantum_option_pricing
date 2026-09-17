"""Partial directed dollar-error composition; unknown errors stay unknown."""

import math
import numpy as np
from mpmath.ctx_iv import MPIntervalContext


def residual_coefficients(degree, low=4):
    if type(degree) is not int or type(low) is not int or low < 2 or low % 2 or degree <= low or degree % 2:
        raise ValueError("even degrees with high>low>=2 required")
    c = np.zeros(degree+1)
    for k in range(low//2+1, degree//2+1):
        c[2*k] = 4/math.pi*(-1)**(k+1)/(4*k*k-1)
    rho = 1.001*float(sum(abs(c)))
    return c/rho, rho


def polynomial_error(degree, low, coefficients, rho):
    """Uniform |x| truncation and exact-target vs stored residual coefficients."""
    c = np.asarray(coefficients, float)
    residual_coefficients(degree, low)  # validation
    if len(c) != degree+1 or not np.isfinite(c).all() or not math.isfinite(rho) or rho <= 0:
        raise ValueError("invalid residual representation")
    iv = MPIntervalContext()
    iv.dps = 70
    coefficient_error = iv.mpf(0)
    for j, value in enumerate(c):
        exact = iv.mpf(0)
        if j > low and j % 2 == 0:
            k = j//2
            exact = 4/iv.pi*(-1)**(k+1)/(4*k*k-1)
        coefficient_error += abs(iv.mpf(float(value))*iv.mpf(float(rho))-exact)
    up = lambda x: math.nextafter(float(x.b), math.inf)
    return dict(truncation_upper=up(2/(iv.pi*(degree+1))),
                stored_coefficient_error_upper=up(coefficient_error))


def dollar_budget(*, degree, discount, radius, rho, polynomial, phase_error,
                  representation_upper, signal_operator_error=None,
                  preparation_state_error=None, control_offset_error=None,
                  execution_operator_error=None):
    """Ideal logical QSP telescoping plus continuous representation terms.

    An error delta in the prepared normalized state changes a norm-one
    expectation by <=2*delta. Each signal call's operator error contributes
    <=delta; degree calls telescope to degree*delta. Execution error is for
    the entire implemented unitary, not per primitive gate. No unknown is zero.
    """
    if type(degree) is not int or degree <= 0:
        raise ValueError("positive degree required")
    values = [discount, radius, rho, phase_error, representation_upper,
              polynomial["truncation_upper"], polynomial["stored_coefficient_error_upper"]]
    optional = [signal_operator_error, preparation_state_error, control_offset_error, execution_operator_error]
    if any(isinstance(x, bool) or not math.isfinite(x) or x < 0 for x in values+ [v for v in optional if v is not None]):
        raise ValueError("finite nonnegative bounds required")
    if min(discount, radius, rho) <= 0:
        raise ValueError("positive price scales required")
    iv = MPIntervalContext()
    iv.dps = 70
    factor = iv.mpf(float(discount))*iv.mpf(float(radius))/2
    beta = factor*iv.mpf(float(rho))
    up = lambda x: math.nextafter(float(x.b), math.inf)
    terms = dict(continuous_representation=representation_upper,
                 polynomial_truncation=up(factor*polynomial["truncation_upper"]),
                 stored_polynomial_coefficients=up(factor*polynomial["stored_coefficient_error_upper"]),
                 phase_response=up(beta*phase_error),
                 signal_implementation=None if signal_operator_error is None else up(beta*degree*signal_operator_error),
                 state_preparation=None if preparation_state_error is None else up(2*beta*preparation_state_error),
                 control_offset=control_offset_error,
                 execution=None if execution_operator_error is None else up(beta*execution_operator_error))
    known = sum((iv.mpf(float(v)) for v in terms.values() if v is not None), iv.mpf(0))
    missing = [k for k, v in terms.items() if v is None]
    return dict(components=terms, known_bound_sum=up(known), missing=missing,
                total_bound=None if missing else up(known), application_admitted=False,
                qualification="partial bound; supplied scale/representation bounds require their own provenance")
