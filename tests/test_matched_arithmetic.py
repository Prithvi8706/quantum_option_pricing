"""Small exact integer tests, with no financial accuracy claim."""

import json

import pytest

from research.journal_sprint.matched_arithmetic import arithmetic_components, compiler_counts
from research.journal_sprint.fixed_exp_budget import evaluate_integer
from research.journal_sprint.reversible_fixed_point import Program, basis, raw_payoff_flag


def tiny_plan():
    return dict(normal_qubits=2, selector_bits=3, width=5, fraction_bits=1,
                affine_rows=[(0, [1, 2]), (1, [1, 0])],
                exp_budget=dict(coefficients=[2, 2], intermediate_magnitude_upper="3"),
                strike_sum=4,
                overflow_safe=True)


def test_exhaustive_reference_and_counts():
    plan = tiny_plan()
    result = arithmetic_components(plan, checks=range(4))
    json.dumps(result, allow_nan=False)
    p = Program(compact=True)
    inputs, selector, flag = p.register(2), p.register(3), p.register(1)
    raw_payoff_flag(p, inputs, selector, flag[0], 5, 1,
                    plan["affine_rows"], [2, 2], 4)
    for packed in range(4):
        logs = [a+sum(((packed >> i) & 1)*c for i, c in enumerate(cs))
                for a, cs in plan["affine_rows"]]
        payoff = max(sum(evaluate_integer(x, [2, 2], 1) for x in logs)-4, 0)
        assert result["semantic_checks"][packed]["payoff_integer"] == payoff
        for u in range(8):
            for b in range(2):
                initial = basis(inputs, packed) | basis(selector, u) | basis(flag, b)
                assert p.run(initial) == initial ^ basis(flag, int(u < payoff))
    resources = p.resources()
    for key in ("x", "cx", "ccx"):
        assert result["total_excluding_aggregation"][key] == (
            2*result["conversion_forward"][key]
            + 2*result["postaggregation_payoff"][key]+result["comparator"][key])
    # Two forward plus two reverse width-5 Cuccaro additions.
    assert resources["x"] == result["total_excluding_aggregation"]["x"]
    assert resources["cx"] == result["total_excluding_aggregation"]["cx"] + 4*20
    assert resources["ccx"] == result["total_excluding_aggregation"]["ccx"] + 4*10
    assert result["A_num_qubits_excluding_loader_ancillas"] == sum(result["wire_layout"].values())
    # Separate comparator carry deliberately costs one more than raw_payoff_flag.
    assert result["A_num_qubits_excluding_loader_ancillas"] == p.qubits+1
    assert result["a_qubits_excluding_aggregation_helper"] == p.qubits+1
    assert result["native_excluding_aggregation"] == {
        k: result["compiler_counts"][k] for k in ("u", "cx")}
    assert result["poststrike_bounds"]["difference_integer_lower"] == -16


def test_compiler_counts():
    assert compiler_counts(dict(x=2, cx=3, ccx=1)) == dict(
        u=11, cx=9, controlled_u=148, controlled_cx=76)
    with pytest.raises(ValueError):
        compiler_counts(dict(x=-1, cx=0, ccx=0))


def test_overflow_refused_before_construction():
    with pytest.raises(ArithmeticError, match="overflow_safe"):
        arithmetic_components(dict(overflow_safe=False))


@pytest.mark.parametrize("checks", [[], [-1], [4], [True], [1, True], list(range(257))])
def test_invalid_checks(checks):
    with pytest.raises(ValueError):
        arithmetic_components(tiny_plan(), checks=checks)


def test_false_certificate_detected_at_checked_boundary():
    plan = tiny_plan()
    plan["selector_bits"] = 1
    with pytest.raises(ArithmeticError, match="sum/payoff"):
        arithmetic_components(plan)


def test_negative_log_and_zero_payoff():
    plan = tiny_plan()
    plan["affine_rows"] = [(-2, [1, 1])]
    result = arithmetic_components(plan, checks=range(4))
    assert all(row["payoff_integer"] == 0 for row in result["semantic_checks"])
    assert all(row["clean_workspace"] for row in result["row_checks"])


def test_universal_negative_price_difference_overflow_refused():
    plan = tiny_plan()
    # Both aggregate magnitude 12 and strike 5 individually fit a signed
    # five-bit word, but their difference can reach -17: fail before gates.
    plan["strike_sum"] = 5
    with pytest.raises(ArithmeticError, match="universal poststrike"):
        arithmetic_components(plan)


def test_missing_magnitude_proof_refused():
    plan = tiny_plan()
    del plan["exp_budget"]["intermediate_magnitude_upper"]
    with pytest.raises(ArithmeticError, match="magnitude bound"):
        arithmetic_components(plan)
