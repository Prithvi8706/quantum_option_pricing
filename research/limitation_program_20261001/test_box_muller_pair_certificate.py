"""Small exact arithmetic/coupling fixtures and unchanged literal-table checks."""

from fractions import Fraction
from pathlib import Path

import mpmath as mp
import pytest

from research.limitation_program_20261001 import box_muller_pair_certificate as certificate


ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(autouse=True)
def interval_precision():
    previous = mp.iv.dps
    mp.iv.dps = certificate.INTERVAL_DIGITS
    yield
    mp.iv.dps = previous


@pytest.mark.parametrize("raw", [0, 1, 1 << 31, (1 << 32) - 1])
def test_midpoint_is_exact_and_inside_its_uniform_cell(raw):
    value = certificate.midpoint(raw)
    assert value == Fraction(raw, 1 << 32) + Fraction(1, 1 << 33)
    assert Fraction(raw, 1 << 32) < value < Fraction(raw + 1, 1 << 32)


@pytest.mark.parametrize("raw", [-1, 1 << 32, True, Fraction(1, 2)])
def test_midpoint_rejects_changed_finite_law(raw):
    with pytest.raises(ValueError):
        certificate.midpoint(raw)


def test_interval_endpoints_are_exact_outward_rationals():
    low, high = certificate.enclosure(mp.iv.sqrt(certificate.iv(2)))
    assert low * low <= 2 <= high * high
    assert isinstance(low, Fraction) and isinstance(high, Fraction)
    assert certificate.decoded(certificate.encoded(high)) == high


def test_horner_floor_bound_handles_negative_signed_products():
    coefficients = [5, -3, 2, 1]
    bound = certificate.horner_floor_bound(3, Fraction(1, 2), Fraction(1, 16))
    assert bound == Fraction(7, 64)
    for raw in range(-8, 9):
        result = coefficients[-1]
        for value in reversed(coefficients[:-1]):
            result = value + (result * raw) // 16
        ideal = sum(
            Fraction(value, 16) * Fraction(raw, 16) ** j for j, value in enumerate(coefficients)
        )
        assert abs(Fraction(result, 16) - ideal) <= bound


@pytest.mark.parametrize("cutoff", [20, 24])
def test_radial_coupling_bounds_cover_cell_edges_and_upper_endpoint(cutoff):
    delta = Fraction(1, 1 << cutoff)
    result = certificate.radial_grid_bound(delta)
    bound = certificate.decoded(result["radial_grid_error_upper_exact"])
    first = (1 << 32) // (1 << cutoff)
    assert certificate.midpoint(first) == delta + Fraction(1, 1 << 33)
    for raw in [first, first + 1, (1 << 31) - 1, 1 << 31, (1 << 32) - 1]:
        middle = certificate.midpoint(raw)
        r_middle = mp.iv.sqrt(-2 * mp.iv.log(certificate.iv(middle)))
        for point in [Fraction(raw, 1 << 32), Fraction(raw + 1, 1 << 32)]:
            if point < delta:
                continue
            r_point = mp.iv.sqrt(-2 * mp.iv.log(certificate.iv(point)))
            assert certificate.upper(abs(r_point - r_middle)) <= bound


@pytest.mark.parametrize("delta", [Fraction(0), Fraction(-1, 4), Fraction(1, 3), Fraction(1, 2)])
def test_radial_bound_rejects_nonaligned_or_invalid_cutoffs(delta):
    with pytest.raises(ValueError):
        certificate.radial_grid_bound(delta)


@pytest.mark.parametrize("name", ["log", "cos"])
def test_every_actual_literal_coefficient_has_a_rigorous_enclosure(name):
    target = certificate.read(ROOT / certificate.SOURCE_BASE / "B4x12/min-depth/target.json")
    rows = target["tables"][name]
    result = certificate.table_certificate(name, rows)
    assert len(result["coefficient_checks"]) == (288 if name == "log" else 512)
    assert certificate.decoded(result["Taylor_remainder_upper_exact"]) > 0
    assert certificate.decoded(result["Horner_floor_upper_exact"]) > 0
    assert result["signed_overflow_excluded"] is True


@pytest.mark.parametrize("name", ["log", "cos"])
def test_altered_literal_table_cannot_inherit_the_rounding_proof(name):
    target = certificate.read(ROOT / certificate.SOURCE_BASE / "B4x12/min-depth/target.json")
    target["tables"][name][0][0] += 10
    with pytest.raises(ValueError, match="nearest rounding"):
        certificate.table_certificate(name, target["tables"][name])


def polynomial_fixture():
    return dict(
        width=8,
        fraction_bits=3,
        nodes=[
            dict(op="input", args=[], params={}, out=[0]),
            dict(op="mul", args=[0, 0], params={}, out=[1]),
            dict(op="const", args=[], params=dict(value=8), out=[2]),
            dict(op="add", args=[1, 2], params={}, out=[3]),
            dict(op="mul", args=[0, 3], params={}, out=[4]),
        ],
    )


def test_formal_polynomial_and_floor_recurrence_cover_all_tiny_signed_inputs():
    result = certificate.polynomial_floor_certificate(polynomial_fixture(), 4, 0, Fraction(1, 2))
    assert result["coefficients"] == {"1": [1, 1], "3": [1, 1]}
    assert certificate.decoded(result["evaluation_floor_error_upper_exact"]) == Fraction(3, 16)
    for raw in range(-4, 5):
        square = raw * raw // 8
        native = raw * (square + 8) // 8
        ideal = Fraction(raw, 8) ** 3 + Fraction(raw, 8)
        assert abs(Fraction(native, 8) - ideal) <= Fraction(3, 16)


def test_unsupported_polynomial_operation_is_not_free():
    target = polynomial_fixture()
    target["nodes"][-1]["op"] = "cmul"
    with pytest.raises(ValueError, match="Unexpected"):
        certificate.polynomial_floor_certificate(target, 4, 0, Fraction(1, 2))


def test_polynomial_native_overflow_is_rejected():
    with pytest.raises(ValueError, match="overflow"):
        certificate.polynomial_floor_certificate(polynomial_fixture(), 4, 0, Fraction(100))


def test_q32_log_normalization_is_a_lossless_native_left_shift():
    for raw in [0, 1, (1 << 31) - 1, (1 << 32) - 1]:
        native = raw * 256 + 128
        exponent = native.bit_length() - 1 - 40
        mantissa = native << (-exponent)
        assert -33 <= exponent <= -1
        assert 1 << 40 <= mantissa < 2 << 40
        assert Fraction(native, 1 << 40) == Fraction(mantissa, 1 << 40) * Fraction(2) ** exponent


@pytest.mark.parametrize("case", ["B4x12", "B8x52"])
def test_actual_independent_dollar_support_is_bound_before_tail_conversion(case):
    support, binding = certificate.support_binding(ROOT, case)
    assert 0 == support["payoff_raw_bounds"][0] < support["payoff_raw_bounds"][1] < 40 * (1 << 40)
    assert binding["payoff_difference_on_bad_event_upper_dollars_exact"] == [40, 1]
