"""Discrete minimax candidate plus independent whole-interval error bound.

The LP is a numerical candidate generator, not a continuous minimax certificate.
The certificate combines explicit binary64 evaluation error with Markov's
inequality for the polynomial p(x)-x on [0,1]. Evenness covers [-1,1].
"""

import math
import numpy as np
from numpy.polynomial.chebyshev import chebvander
from scipy.optimize import linprog
from .decimal_enclosure import Interval as I
from .encoding_enclosure import upward_float


def discrete_minimax(degree, fit_points=8193):
    if type(degree) is not int or degree < 2 or degree % 2 or degree > 128:
        raise ValueError("even degree in [2,128] required")
    if type(fit_points) is not int or fit_points < 4*degree or fit_points > 32769:
        raise ValueError("bounded fit grid must have at least 4*degree points")
    x = (1-np.cos(np.linspace(0, np.pi, fit_points)))/2
    design = chebvander(x, degree)[:, ::2]
    constraints = np.vstack((np.c_[design, -np.ones(len(x))],
                             np.c_[-design, -np.ones(len(x))]))
    objective = np.r_[np.zeros(design.shape[1]), 1.]
    fit = linprog(objective, A_ub=constraints, b_ub=np.r_[x, -x],
                  bounds=[(None, None)]*design.shape[1]+[(0, None)], method="highs",
                  options={"maxiter": 10000, "primal_feasibility_tolerance": 1e-9,
                           "dual_feasibility_tolerance": 1e-9})
    record = dict(degree=degree, fit_points=fit_points, solver_success=bool(fit.success),
                  solver_status=int(fit.status), solver_message=str(fit.message),
                  iterations=int(fit.nit), continuous_minimax_proven=False)
    if fit.success:
        coefficients = np.zeros(degree+1)
        coefficients[::2] = fit.x[:-1]
        record.update(coefficients=coefficients.tolist(), sampled_lp_error=float(fit.x[-1]))
    return record


def uniform_abs_bound(coefficients):
    """Outward bound on ||p-|x|||, conditional on IEEE binary64 operations.

    For r=p-x on [0,1], Markov gives ||r'|| <= 2*d*d*||r||.
    A dyadic grid of N segments is at distance <=1/(2N) from every x,
    so ||r|| <= max_grid |r|/(1-d*d/N). Grid evaluation errors are paid.
    Chebyshev recurrence residuals propagate through U_j with |U_j|<=j+1,
    not the exponentially pessimistic naive interval recurrence.
    """
    c = np.asarray(coefficients, dtype=np.float64)
    if (c.ndim != 1 or len(c) < 3 or len(c) > 129 or len(c) % 2 != 1
            or not np.isfinite(c).all() or np.any(c[1::2] != 0)
            or np.max(abs(c)) > 10):
        raise ValueError("bounded even polynomial coefficients required")
    degree = len(c)-1
    segments = 1 << (8*degree*degree-1).bit_length()
    # Integer/dyadic construction is exact in binary64 for this bounded size.
    x = np.arange(segments+1, dtype=np.float64)/segments
    twice_x = 2*x
    previous, current = np.ones_like(x), x.copy()
    total = np.full_like(x, c[0])
    gamma = I(2.**-53)/(1-I(2.**-53))
    eta = I("1e-323")  # conservative absolute underflow allowance per operation
    recurrence_max, evaluation_error = I(0), I(0)
    for k in range(2, degree+1):
        product = twice_x*current
        following = product-previous
        if not np.isfinite(following).all():
            raise ArithmeticError("nonfinite certification recurrence")
        residual = gamma*(I(float(np.max(abs(product))))+I(float(np.max(abs(following)))))+2*eta
        recurrence_max = I(max(recurrence_max.hi, residual.hi))
        recurrence_error = recurrence_max*(k*(k-1)//2)
        term = c[k]*following
        total = total+term
        if not np.isfinite(total).all():
            raise ArithmeticError("nonfinite certification sum")
        rounding = gamma*(I(float(np.max(abs(term))))+I(float(np.max(abs(total)))))+2*eta
        evaluation_error += I(float(c[k])).absolute()*recurrence_error+rounding
        previous, current = current, following
    differences = total-x
    maximum = float(np.max(abs(differences)))
    evaluation_error += gamma*I(maximum)+eta
    denominator = 1-I(degree*degree)/segments
    bound = (I(maximum)+evaluation_error)/denominator
    return dict(uniform_error_upper=upward_float(bound.hi), grid_error=maximum,
                evaluation_error_upper=upward_float(evaluation_error.hi),
                segments=segments, markov_denominator_lower=str(denominator.lo),
                domain=[-1, 1], exact_binary_coefficients=True,
                assumptions="IEEE binary64 round-to-nearest with gradual underflow, no reassociation; explicit NumPy multiply/subtract/add",
                certificate="Chebyshev recurrence rounding enclosure plus Markov grid-to-uniform bound")


def comparison_allowance(beta, phase_error, coefficient_error=0., numerical_allowance=1e-9):
    """Dollar-scaled check, replacing the frozen runner's fixed-unit mismatch."""
    values = (beta, phase_error, coefficient_error, numerical_allowance)
    if any(isinstance(v, bool) or not math.isfinite(v) or v < 0 for v in values):
        raise ValueError("finite nonnegative comparison bounds required")
    return upward_float((I(beta)*I(phase_error)+I(coefficient_error)+I(numerical_allowance)).hi)
