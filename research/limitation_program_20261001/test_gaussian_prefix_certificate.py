"""New probability, convention, budget, and complete-prefix checks only."""

from fractions import Fraction

import mpmath as mp
import pytest

from research.limitation_program_20261001 import gaussian_prefix_certificate as prefix

QASM = "\n".join(
    [
        "OPENQASM 3.0;",
        'include "stdgates.inc";',
        "qubit[10] q;",
        "ry(pi/2) q[9];",
        "ry(pi/2) q[8];",
        "cx q[9], q[8];",
        "ry(1.466830424129055) q[8];",
        "cx q[9], q[8];",
    ]
)


def a05_rows():
    return [
        dict(case=case, conservative_scalar_trace_allowance_exact=[1, 40000 * draws])
        for case, draws in (("B4x12", 60), ("B8x52", 468))
    ]


def test_zero_cdf_is_exact_half():
    assert prefix.gaussian_cdf(0) == (Fraction(1, 2),) * 2


def test_cdf_reflection_is_exact_rational_complement():
    for value in (3, 6):
        lo, hi = prefix.gaussian_cdf(value)
        assert prefix.gaussian_cdf(-value) == (1 - hi, 1 - lo)


def test_cdf_enclosures_contain_independent_high_precision_erf():
    with mp.workdps(180):
        for value in (3, 6):
            lo, hi = prefix.gaussian_cdf(value)
            reference = (1 + mp.erf(mp.mpf(value) / mp.sqrt(2))) / 2
            assert mp.mpf(lo.numerator) / lo.denominator <= reference
            assert reference <= mp.mpf(hi.numerator) / hi.denominator


def test_finite_taylor_remainder_covers_coarse_polynomial():
    with mp.workdps(80):
        lo, hi = prefix.gaussian_cdf(3, degree=8)
        reference = (1 + mp.erf(3 / mp.sqrt(2))) / 2
        assert mp.mpf(lo.numerator) / lo.denominator <= reference
        assert reference <= mp.mpf(hi.numerator) / hi.denominator


def test_float_probability_boundary_is_rejected():
    with pytest.raises(ValueError):
        prefix.gaussian_cdf(3.0)


def test_outside_fixed_cdf_domain_is_rejected():
    with pytest.raises(ValueError):
        prefix.gaussian_cdf(7)


def test_machin_enclosure_contains_independent_pi_reference():
    with mp.workdps(380):
        lo, hi = prefix.pi_bounds()
        assert mp.mpf(lo.numerator) / lo.denominator < mp.pi
        assert mp.pi < mp.mpf(hi.numerator) / hi.denominator


def test_conditional_mass_ratio_has_correct_normalization():
    result = prefix.quotient((Fraction(1, 8),) * 2, (Fraction(1, 2),) * 2)
    assert result[0] <= Fraction(1, 4) <= result[1]


def test_nonpositive_mass_denominator_is_rejected():
    with pytest.raises(ValueError):
        prefix.quotient((Fraction(1, 8),) * 2, (Fraction(0), Fraction(1, 2)))


def test_monotone_angle_inversion_covers_known_pi_third():
    lo, hi = prefix.angle_over_pi((Fraction(1, 4),) * 2)
    assert lo <= Fraction(1, 3) <= hi
    assert hi - lo == Fraction(1, 1 << prefix.BISECTION_STEPS)


def test_noninterior_probability_inversion_is_rejected():
    with pytest.raises(ValueError):
        prefix.angle_over_pi((Fraction(0), Fraction(1, 2)))


def test_midpoint_rounding_charges_whole_interval():
    enclosure = Fraction(2, 3), Fraction(3, 4)
    target, error = prefix.rounded_midpoint(enclosure, bits=4)
    assert target.denominator <= 16
    assert error == max(abs(target - endpoint) for endpoint in enclosure) / 2


def test_tree_count_and_conditional_vs_walsh_count_are_separate():
    result = prefix.archive_counts(QASM)
    assert result["full_tree_conditional_nodes"] == 1023
    assert result["theoretical_multiplexor_CX_count"] == 1022
    assert result["first_two_levels_conditional_nodes"] == 3
    assert result["first_two_levels_emitted_Walsh_Ry_rotations"] == 3
    assert result["archived_operation_counts"] == dict(ry=3, cx=2)
    assert result["full_preparation_trace_error"] is None


def test_scalar_wire_escape_is_rejected():
    with pytest.raises(ValueError):
        prefix.archive_counts(QASM + "\nry(1) q[10];")


def test_all_1023_rotations_share_conservative_468_factor_budget():
    rows = prefix.budget_rows(a05_rows())
    assert rows[1]["conditional_bounded_observable_dollars_exact"] == [1, 1000]
    assert Fraction(*rows[0]["conditional_bounded_observable_dollars_exact"]) < Fraction(1, 1000)
    assert all(row["pure_product_refinement_used"] is False for row in rows)
    assert all(row["full_tree_rotations_all_within_allowance"] is None for row in rows)


def test_unmatched_a05_scalar_allowance_is_rejected():
    rows = a05_rows()
    rows[0]["conservative_scalar_trace_allowance_exact"] = [1, 2400001]
    with pytest.raises(ValueError):
        prefix.budget_rows(rows)


def test_complete_prefix_unitary_checks_w_phase_and_ry_axis():
    lo, hi = prefix.pi_bounds()
    beta = lo / 2, hi / 2
    target, _ = prefix.rounded_midpoint(beta)
    checked = prefix.verify_string(beta, target, "WWWWWWWS")
    assert Fraction(*checked["complete_prefix_Frobenius_error_squared_upper_exact"]) < Fraction(
        1, 10**250
    )
    assert checked["scalar_W_phase_included_in_interval_verification"] is True


def test_synthesis_invalid_tokens_and_wrong_target_are_rejected():
    with pytest.raises(ValueError):
        prefix.matrix_product("HTA")
    with pytest.raises(ArithmeticError):
        prefix.verify_string((Fraction(1, 2),) * 2, Fraction(1, 2), "")
