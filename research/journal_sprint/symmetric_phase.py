"""Bounded symmetric QSP fitting and interval Laurent-error enclosure.

Independent implementation of palindromic phase parameterization, motivated by
Dong et al., arXiv:2307.12468. This is SciPy least squares with an analytic
Jacobian, not an implementation or benchmark of their Newton solver.
"""

import math
import numpy as np
from numpy.polynomial.chebyshev import chebval
from scipy.optimize import least_squares
from mpmath.ctx_iv import MPIntervalContext

from .combined_qsp import response


def symmetric_response(x, reduced):
    """Imaginary response and analytic reduced-phase Jacobian, even parity."""
    x, reduced = np.asarray(x, float), np.asarray(reduced, float)
    size = len(reduced)
    indices = list(range(size-1, 0, -1))+[0]+list(range(1, size))
    a, b = np.ones(x.shape, complex), np.zeros(x.shape, complex)
    da, db = np.zeros((len(x), size), complex), np.zeros((len(x), size), complex)
    off = 1j*np.sqrt(np.maximum(0, 1-x*x))
    for step, index in enumerate(indices):
        if step:
            a, b = x*a+off*b, off*a+x*b
            da, db = x[:, None]*da+off[:, None]*db, off[:, None]*da+x[:, None]*db
        scale = 2 if index == 0 else 1
        phase = np.exp(1j*scale*reduced[index])
        a, b = phase*a, phase.conjugate()*b
        da, db = phase*da, phase.conjugate()*db
        da[:, index] += 1j*scale*a
        db[:, index] -= 1j*scale*b
    return a.imag, da.imag


def synthesize_even(coefficients, max_nfev=150):
    c = np.asarray(coefficients, float)
    if (c.ndim != 1 or len(c) < 3 or len(c) % 2 != 1 or not np.isfinite(c).all()
            or np.any(c[1::2] != 0) or np.sum(abs(c)) >= 1
            or type(max_nfev) is not int or max_nfev < 1):
        raise ValueError("even finite polynomial, coefficient l1<1 and positive cap required")
    degree = len(c)-1
    nodes = np.cos(np.pi*(np.arange(2*degree+1)+.5)/(4*degree+2))
    target = chebval(nodes, c)
    reduced = np.zeros(degree//2+1)
    attempts = []
    for fraction in (.25, .5, .75, 1.):
        fit = least_squares(lambda r: symmetric_response(nodes, r)[0]-fraction*target,
                            reduced, jac=lambda r: symmetric_response(nodes, r)[1],
                            max_nfev=max_nfev, ftol=1e-13, xtol=1e-13, gtol=1e-13)
        reduced = fit.x
        attempts.append(dict(target_fraction=fraction, evaluations=int(fit.nfev),
                             solver_success=bool(fit.success),
                             node_error=float(np.max(abs(fit.fun)))))
    phases = np.r_[reduced[:0:-1], 2*reduced[0], reduced[1:]]
    # Multiplying the output row by -i converts the imaginary response to real.
    phases[-1] -= math.pi/2
    mesh = np.linspace(-1, 1, 8193)
    error = float(np.max(abs(response(mesh, phases).real-chebval(mesh, c))))
    return dict(degree=degree, coefficients=c.tolist(), phases=phases.tolist(),
                attempts=attempts, sampled_phase_error=error, fit_accepted=error < 1e-8,
                method="palindromic imaginary response, analytic Jacobian, continuation least squares")


def uniform_phase_bound(phases, coefficients):
    """Directed interval l1 Laurent bound, for exact archived binary inputs.

    x=(z+z^-1)/2, i*sin(theta)=(z-z^-1)/2. On the unit circle,
    real(a) has coefficients (a_k+conj(a_-k))/2. Sum coefficient
    magnitude upper bounds gives a uniform error for x in [-1,1].
    This certifies ideal phase response only, not hardware rotations or the
    approximation of |x| by the target polynomial.
    """
    phases, coefficients = np.asarray(phases, float), np.asarray(coefficients, float)
    if (phases.ndim != 1 or coefficients.ndim != 1 or len(phases) < 1
            or len(coefficients) > len(phases) or not np.isfinite(phases).all()
            or not np.isfinite(coefficients).all()):
        raise ValueError("finite phase and coefficient vectors required")
    iv = MPIntervalContext()
    iv.dps = 70
    zero = iv.mpc(0)
    def conjugate(value):
        # mpmath 1.3.0 interval-complex .conjugate uses scalar internals.
        return iv.mpc(value.real, -value.imag)
    def phase(value):
        value = iv.mpf(float(value))
        return iv.mpc(iv.cos(value), iv.sin(value))
    a, b = {0: phase(phases[0])}, {0: zero}
    for value in phases[1:]:
        aa, bb = {}, {}
        for k in set(a) | set(b):
            av, bv = a.get(k, zero), b.get(k, zero)
            for shift in (-1, 1):
                aa[k+shift] = aa.get(k+shift, zero)+(av+shift*bv)/2
                bb[k+shift] = bb.get(k+shift, zero)+(shift*av+bv)/2
        p = phase(value)
        a = {k: p*v for k, v in aa.items()}
        b = {k: conjugate(p)*v for k, v in bb.items()}
    degree = len(phases)-1
    bound = iv.mpf(0)
    for k in range(-degree, degree+1):
        target = iv.mpf(float(coefficients[abs(k)])) if abs(k) < len(coefficients) else iv.mpf(0)
        if k:
            target /= 2
        difference = (a.get(k, zero)+conjugate(a.get(-k, zero)))/2-target
        # |re|+|im| is an outward upper bound for the complex magnitude.
        bound += abs(difference.real)+abs(difference.imag)
    upper = math.nextafter(float(bound.b), math.inf)
    return dict(uniform_error_upper=upper, interval_decimal_precision=70,
                domain=[-1, 1], scope="ideal response to exact binary archived coefficients/phases",
                method="directed interval Laurent coefficient l1 bound",
                hardware_error_included=False)
