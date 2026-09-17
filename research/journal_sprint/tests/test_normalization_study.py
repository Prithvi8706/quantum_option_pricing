import numpy as np
import pytest
from numpy.polynomial.chebyshev import chebval
from research.journal_sprint.normalization_study import (
    radius_enclosures, truncated_candidate, normalized_residual,
)
from research.journal_sprint.decimal_enclosure import Interval as I


def test_centering_and_directed_radius():
    radii = radius_enclosures([0.], [[.2]], 1., 2.)
    assert float(radii["centered"].hi) == pytest.approx(np.exp(.4)-1)
    assert radii["centered"].hi < radii["original"].lo
    for value in np.linspace(-2, 2, 101):
        assert abs(np.exp(.2*value)-1) < float(radii["centered"].hi)+1e-15


def test_negative_constant_still_positive_radius():
    radii = radius_enclosures([0.], [[.2]], 3., 2.)
    assert float(radii["centered"].hi) == pytest.approx(np.exp(.4)+3-2*np.cosh(.4))


def test_residual_rounding_bridge():
    high, low = truncated_candidate(16), truncated_candidate(4)
    plan = normalized_residual(high["coefficients"], low["coefficients"])
    assert plan["coefficient_bridge_upper"] < 1e-15
    assert sum(abs(np.array(plan["coefficients"]))) < 1
    x = np.linspace(-1, 1, 10001)
    assert np.max(abs(chebval(x, high["coefficients"])-abs(x))) <= high["uniform_error_upper"]


def test_discount_bridge_for_exact_payoff_not_control():
    # Deliberately visible discount mismatch checks the bound, not just ulps.
    business_discount, archived_discount = I("0.97"), I(.96)
    upper = I(600)
    bound = (business_discount-archived_discount).absolute()*upper
    for basket in np.linspace(0, 600, 101):
        actual = (business_discount-archived_discount)*I(max(float(basket)-100, 0))
        assert actual.absolute().hi <= bound.hi
