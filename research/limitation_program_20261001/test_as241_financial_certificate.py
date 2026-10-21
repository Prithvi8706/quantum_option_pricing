"""Bounded proof-contract fixtures; no finance sampling or graph generation."""

from copy import deepcopy
from fractions import Fraction

import pytest

from research.limitation_program_20261001.as241_financial_native import (
    LAW,
    S,
    EPS,
    canonical_hash,
    check_word,
    multiply_bounds,
    native_support,
    polynomial_intervals,
    signed,
    validate_ledger,
    validate_normalization,
    validate_scalar_invocations,
)
from research.limitation_program_20261001.as241_financial_certificate import bias_components


def ledger():
    return {
        "source_target_sha256": "new-target",
        "law": LAW,
        "epsilon_dollars_exact": [1, 100],
        "statistical_allowance_dollars_exact": [9, 2000],
        "residual_financial_allowance_dollars_exact": [11, 2000],
        "source_resources": None,
        "wrapper_resources": None,
        "accepted_joint_Box_Muller_obligation_filled": False,
        "old_E02_source_or_wrapper_costs_transferred": False,
    }


@pytest.mark.parametrize("value,expected", [(-1, -1), ((1 << 72) - 1, -1)])
def test_negative_native_word(value, expected):
    assert signed(value) == expected
    assert multiply_bounds((value if value < 0 else -1,) * 2, (1, 1)) == (-1, -1)


def test_signed_floor_not_truncation():
    assert multiply_bounds((-S - 1, -S - 1), (1, 1)) == (-2, -2)
    assert int(Fraction(-S - 1, S)) == -1


def test_correlated_square_keeps_nonnegative_lower():
    assert multiply_bounds((-S, S), (-S, S), square=True) == (0, S)
    assert multiply_bounds((-S, S), (-S, S)) == (-S, S)


def test_stored_overflow_rejected():
    with pytest.raises(ValueError, match="storage"):
        check_word((0, 1 << 71))


def test_full_product_overflow_rejected():
    with pytest.raises(ValueError, match="product"):
        multiply_bounds((1 << 80, 1 << 80), (1 << 80, 1 << 80))


def test_exact_new_source_ledger():
    result = validate_ledger(ledger(), "new-target")
    assert result["epsilon_dollars_exact"] == sum(
        [
            result["statistical_allowance_dollars_exact"],
            result["residual_financial_allowance_dollars_exact"],
        ]
    )


@pytest.mark.parametrize(
    "field,replacement",
    [
        ("source_target_sha256", "old-BM-target"),
        ("law", "paired finite Box-Muller"),
        ("residual_financial_allowance_dollars_exact", [1, 100]),
        ("old_E02_source_or_wrapper_costs_transferred", True),
    ],
)
def test_changed_law_budget_or_cost_transfer_rejected(field, replacement):
    item = ledger()
    item[field] = replacement
    with pytest.raises(ValueError):
        validate_ledger(item, "new-target")


def test_actual_rounded_asian_coefficient_support():
    scope = {
        "assets": 4,
        "dates": 12,
        "barrier_raw": 140 * S,
        "strike_raw": 100 * S,
        "average_coefficient": (S + 47) // 48,
        "discount_coefficient": S * 97 // 100,
    }
    row = native_support(scope)
    assert row["surviving_rounded_asian_average_raw_upper"] >= 140 * S
    assert row["native_payoff_raw_bounds"][1] < 40 * S
    assert row["average_coefficient_rounding_charged"]


def test_incorrect_asian_rounding_can_fail_support():
    scope = {
        "assets": 4,
        "dates": 12,
        "barrier_raw": 140 * S,
        "strike_raw": 100 * S,
        "average_coefficient": S // 47,
        "discount_coefficient": S,
    }
    with pytest.raises(ValueError, match="support"):
        native_support(scope)


def test_strict_barrier_floor_cannot_hide_equality():
    for na in (4, 8):
        h = 140 * S
        assert (na * h - 1) // na < h
        assert (na * h) // na == h
        assert max(sum([na * h - 1] * 3), 0) == 3 * na * h - 3


def test_lower_clamp_paid_sandwich_is_deterministic():
    lower = Fraction(1, 65536)
    for stock in (lower / 10, lower, 2 * lower, 100):
        clamped = max(stock, lower)
        assert stock <= clamped <= stock + lower


def test_closed_band_ties_and_coordinate_variation_two():
    values = [Fraction(j, 8) for j in range(9)]
    flags = [int(Fraction(1, 4) <= value <= Fraction(3, 4)) for value in values]
    assert flags[2] == flags[6] == 1
    assert sum(abs(a - b) for a, b in zip(flags, flags[1:])) == 2


def test_all_price_terms_paid_once_without_ks_or_double_discount():
    grid, smooth, switch, total = bias_components(60, Fraction(1, 10000), Fraction(1, 100000))
    assert grid == Fraction(2400, 1 << 32)
    assert smooth == Fraction(1, 10000) and switch == Fraction(1, 2500)
    assert total == grid + Fraction(1, 2000)


def scalar_copies():
    scalar = {
        "width": 72,
        "fraction_bits": 40,
        "tables": {},
        "inputs": [0],
        "outputs": {"Z": 0},
        "nodes": [
            {
                "op": "input",
                "args": [],
                "out": [0],
                "params": {"name": "k", "bits": 32, "preparation": "uniform"},
            }
        ],
    }
    target = deepcopy(scalar)
    target["inputs"] = list(range(60))
    target["nodes"] = [
        dict(
            op="input",
            args=[],
            out=[i],
            params={"name": "as241_uniform_" + str(i), "bits": 32, "preparation": "uniform"},
        )
        for i in range(60)
    ]
    for i in range(1, 60):
        target["nodes"].append(
            dict(op="add", args=[0 if i == 1 else 59 + i - 1, i], out=[59 + i], params={})
        )
    target["outputs"] = {"Y": 118}
    bundle = {
        "case": "B4x12",
        "normal_values": list(range(60)),
        "target_sha256": canonical_hash(target),
        "normal_source": {
            "law": LAW,
            "scalar_target_sha256": canonical_hash(scalar),
            "input_names": ["as241_uniform_" + str(i) for i in range(60)],
            "invocations": [
                dict(
                    coordinate=i,
                    date_index=i // 5,
                    role="common" if i % 5 == 0 else "idiosyncratic",
                    asset_index=None if i % 5 == 0 else i % 5 - 1,
                    input_name="as241_uniform_" + str(i),
                    input_value=i,
                    output_value=i,
                    value_offset=i,
                    scalar_values=1,
                )
                for i in range(60)
            ],
        },
    }
    return scalar, target, bundle


def test_actual_driver_roles_independent_inputs():
    scalar, target, bundle = scalar_copies()
    assert (
        validate_scalar_invocations(target, bundle, scalar)["independent_scalar_invocations"] == 60
    )


def test_scalar_boundary_role_mutation_rejected():
    scalar, target, bundle = scalar_copies()
    bundle["normal_source"]["invocations"][1]["role"] = "common"
    with pytest.raises(ValueError, match="roles"):
        validate_scalar_invocations(target, bundle, scalar)


def test_actual_financial_literal_mutation_rejected():
    _, old, _ = scalar_copies()
    new = deepcopy(old)
    new["nodes"][-1]["op"] = "sub"
    bundle = {"case": "B4x12", "assets": 4, "dates": 12, "normal_values": list(range(60))}
    with pytest.raises(ValueError, match="function changed"):
        validate_normalization(new, bundle, old, list(range(60)))


def test_actual_polynomial_negative_floor_and_power_square():
    target = {
        "width": 72,
        "fraction_bits": 40,
        "nodes": [
            {"op": "const", "args": [], "out": [0], "params": {"value": 0}},
            {"op": "mul", "args": [0, 0], "out": [1], "params": {}},
            {"op": "const", "args": [], "out": [2], "params": {"value": S + 1}},
            {"op": "mul", "args": [0, 2], "out": [3], "params": {}},
            {"op": "add", "args": [1, 3], "out": [4], "params": {}},
        ],
    }
    actual, values, _ = polynomial_intervals(target, {"remainder": 0, "polynomial": 4}, (-S, S))
    assert values[1] == (0, S)
    assert values[3] == (-S - 1, S + 1)
    assert actual == (-S - 1, 2 * S + 1)
    assert EPS == Fraction(1, 1 << 40)
