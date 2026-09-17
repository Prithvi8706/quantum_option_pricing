import numpy as np
import pytest
from numpy.polynomial.chebyshev import chebval
from research.journal_sprint.certified_payoff import (
    discrete_minimax, uniform_abs_bound, comparison_allowance,
)


@pytest.mark.parametrize("degree", [4, 16, 32])
def test_lp_and_independent_bound(degree):
    fit = discrete_minimax(degree, 2049)
    assert fit["solver_success"]
    assert not fit["continuous_minimax_proven"]
    bound = uniform_abs_bound(fit["coefficients"])
    mesh = np.linspace(-1, 1, 20001)
    error = np.max(abs(chebval(mesh, fit["coefficients"])-abs(mesh)))
    assert error <= bound["uniform_error_upper"]
    assert bound["uniform_error_upper"] < 2/(np.pi*(degree+1))
    assert bound["evaluation_error_upper"] < 1e-10


@pytest.mark.parametrize("c", [[0., 0, 0], [.5, 0, .5], [.1, 0, -.4, 0, .2]])
def test_adversarial_coefficients(c):
    bound = uniform_abs_bound(c)
    mesh = np.linspace(-1, 1, 100001)
    assert np.max(abs(chebval(mesh, c)-abs(mesh))) <= bound["uniform_error_upper"]


def test_units_match_for_near_threshold_phase():
    assert comparison_allowance(19.2005158, 8.00000034e-9) > 1.53604134e-7
    with pytest.raises(ValueError):
        comparison_allowance(-1, 0)


@pytest.mark.parametrize("c", [[1, 1, 1], [np.nan, 0, 0], [0, 0], [11, 0, 0]])
def test_bad_coefficients(c):
    with pytest.raises(ValueError):
        uniform_abs_bound(c)
