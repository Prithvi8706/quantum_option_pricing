import numpy as np
import pytest
from numpy.polynomial.chebyshev import chebval
from research.journal_sprint.combined_qsp import abs_polynomial, response
from research.journal_sprint.symmetric_phase import (
    symmetric_response, synthesize_even, uniform_phase_bound,
)


def test_analytic_jacobian():
    x = np.linspace(-1, 1, 21)
    r = np.random.default_rng(41).normal(size=5)
    _, jac = symmetric_response(x, r)
    for j in range(len(r)):
        step = np.eye(len(r))[j]*1e-6
        numerical = (symmetric_response(x, r+step)[0]-symmetric_response(x, r-step)[0])/2e-6
        assert np.allclose(jac[:, j], numerical, atol=2e-9)


@pytest.mark.parametrize("degree", [8, 16, 32])
def test_residual_fit_and_uniform_bound(degree):
    c, tail = abs_polynomial(degree)
    low, low_tail = abs_polynomial(4)
    c *= 1+tail
    c[:5] -= low*(1+low_tail)
    c /= 1.001*sum(abs(c))
    plan = synthesize_even(c)
    assert plan["fit_accepted"]
    bound = uniform_phase_bound(plan["phases"], c)
    assert bound["uniform_error_upper"] < 1e-8
    assert bound["uniform_error_upper"] >= plan["sampled_phase_error"]-5e-14


def test_interval_detects_bad_phases_not_only_grid():
    phases = [.23, -.9, 1.8, -.4, .1]
    c = [.1, 0, -.2, 0, .3]
    bound = uniform_phase_bound(phases, c)["uniform_error_upper"]
    x = np.linspace(-1, 1, 10001)
    assert bound >= np.max(abs(response(x, phases).real-chebval(x, c)))
    assert bound > .1


@pytest.mark.parametrize("c", [[1, 0, 0], [.1, .1, .1], [np.nan, 0, 0], [0, 0]])
def test_reject_bad_polynomials(c):
    with pytest.raises(ValueError):
        synthesize_even(c)
