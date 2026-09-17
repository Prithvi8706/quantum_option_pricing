import pytest
from research.journal_sprint.qsp_error_budget import (
    residual_coefficients, polynomial_error, dollar_budget,
)


def test_exact_coefficients_and_unknowns():
    c, rho = residual_coefficients(32)
    polynomial = polynomial_error(32, 4, c, rho)
    assert polynomial["stored_coefficient_error_upper"] < 1e-15
    budget = dollar_budget(degree=32, discount=1, radius=200, rho=rho,
                          polynomial=polynomial, phase_error=1e-10, representation_upper=.2)
    assert budget["total_bound"] is None
    assert len(budget["missing"]) == 4
    assert budget["known_bound_sum"] > .2
    assert not budget["application_admitted"]


def test_sensitivity_factors_and_complete_inputs_do_not_admit():
    p = dict(truncation_upper=.01, stored_coefficient_error_upper=.001)
    budget = dollar_budget(degree=10, discount=1, radius=20, rho=.1,
                          polynomial=p, phase_error=.003, representation_upper=.004,
                          signal_operator_error=.005, preparation_state_error=.006,
                          control_offset_error=.007, execution_operator_error=.008)
    assert budget["components"]["signal_implementation"] == pytest.approx(.05)
    assert budget["components"]["state_preparation"] == pytest.approx(.012)
    assert budget["total_bound"] >= sum([.1, .01, .003, .004, .05, .012, .007, .008])
    assert not budget["application_admitted"]


def test_perturbed_coefficients_are_counted():
    c, rho = residual_coefficients(16)
    c[0] = .1
    assert polynomial_error(16, 4, c, rho)["stored_coefficient_error_upper"] >= rho*.1


def test_bad_bounds_rejected():
    with pytest.raises(ValueError):
        dollar_budget(degree=2, discount=1, radius=1, rho=1,
                      polynomial=dict(truncation_upper=0, stored_coefficient_error_upper=0),
                      phase_error=0, representation_upper=0, signal_operator_error=-1)
