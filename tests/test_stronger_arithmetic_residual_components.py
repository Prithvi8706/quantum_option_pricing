"""Tiny emitted residual circuits; no production conversion reconstruction."""

from copy import deepcopy
import json

import pytest

from research.journal_sprint.reversible_fixed_point import Program, basis, constant, subtract
from research.stronger_arithmetic.components import components
from research.stronger_arithmetic import residual_components as module
from research.stronger_arithmetic.residual_circuits import residual_program


@pytest.fixture(scope="module")
def evidence():
    parent = dict(
        normal_qubits=2,
        selector_bits=4,
        width=6,
        fraction_bits=1,
        affine_rows=[(0, [1, 1]), (0, [1, 0])],
        reductions=0,
        spot=1,
        exp_budget=dict(
            coefficients=[2, 2],
            intermediate_magnitude_upper="3",
            reductions=0,
            spot=1,
            output_integer_bounds=[0, 6],
            overflow_safe=True,
        ),
        strike_sum=5,
        overflow_safe=True,
    )
    base = components(parent, reuse=True, reduced=True)
    base["parent_plan"] = deepcopy(parent)
    cert = dict(
        schema="signed_residual_plan_v1",
        parent_plan=deepcopy(parent),
        width=6,
        fraction_bits=1,
        strike_sum=5,
        dimension=2,
        selector_bits=4,
        reciprocal_integer=2,
        control_coefficients=[2, 1, 0, 0, 0],
        control_scale_integer=2,
        shift_integer=8,
        residual_integer_bounds=[-3, 3],
        threshold_integer_bounds=[5, 11],
        overflow_safe=True,
        overflow_failures=[],
    )
    return parent, cert, base


def test_composition_count_identity_allocation_and_evidence(evidence, monkeypatch):
    parent, cert, base = evidence

    # An accidental conversion rebuild would violate the acquisition contract.
    def forbidden(*args, **kwargs):
        pytest.fail("primary conversion emission is forbidden")

    monkeypatch.setattr("research.stronger_arithmetic.components._kernel", forbidden)
    result = module.residual_components(parent, cert, base)
    json.dumps(result, allow_nan=False)
    assert result["actual_remapped_depth"] is False
    assert "logical_depth" not in result
    assert result["qubits"] == sum(result["wire_layout"].values())
    for k in ("x", "cx", "ccx"):
        expected = (
            base["total"][k]
            - 2 * base["postaggregation_payoff"][k]
            - base["comparator"][k]
            + result["complete_postoracle"][k]
        )
        assert result["total"][k] == expected
    assert result["emitted_gate_applications"] == sum(result["total"].values())
    assert all(
        row["clean_workspace"] and row["inverse_checked"] and row["both_initial_flags_checked"]
        for row in result["semantic_checks"]
    )
    assert any(row["residual_integer"] < 0 for row in result["semantic_checks"])
    assert result["depth_upper"] >= result["complete_postoracle"]["logical_depth"]
    assert base["parent_plan"] == parent


def test_strike_wrapper_matches_residual_program_and_exhaustive_basis(evidence):
    _, cert, _ = evidence
    actual, total, selector, flag = module._oracle(cert)
    kernel, delta, local_selector, local_flag = residual_program(
        6, 1, cert["control_coefficients"], 2, 2, 8, 4
    )
    expected = Program(compact=True)
    et, es, ef = expected.register(6), expected.register(4), expected.register(1)[0]
    strike, helper = expected.register(6), expected.register(1)[0]
    start = len(expected.gates)
    constant(expected, strike, 5)
    subtract(expected, strike, et, helper)
    stop = len(expected.gates)
    private = expected.register(kernel.qubits - 6 - 4 - 1)
    mapping = et + es + (ef,) + private
    for gate in kernel.gates:
        expected.gate(*(mapping[b] for b in gate))
    expected.undo(start, stop)
    assert actual.qubits == expected.qubits
    assert list(actual.gates) == list(expected.gates)
    cases = []
    for summed in range(0, 12):
        reference = module._reference(summed, cert)
        # Independent closed form for these degree-one fixed-point constants.
        delta_value = summed - 5
        threshold = max(delta_value, 0) - (delta_value // 2 + 2) + 8
        assert reference["threshold_integer"] == threshold
        for u in range(16):
            for b in (0, 1):
                initial = basis(total, summed) | basis(selector, u) | (b << flag)
                cases.append((initial, initial ^ (int(u < threshold) << flag)))
    module._packed_checks(actual, cases)
    # The parallel evaluator is checked against the original scalar simulator.
    for initial, expected_state in cases[::47]:
        assert actual.run(initial) == expected_state


def test_packed_checks_detect_dirty_scratch(evidence):
    _, cert, _ = evidence
    p, total, selector, flag = module._oracle(cert)
    initial = basis(total, 4) | basis(selector, 0)
    expected = initial ^ (1 << flag)
    p.gate(p.qubits - 1)
    with pytest.raises(ArithmeticError, match="clean workspace"):
        module._packed_checks(p, [(initial, expected)])


@pytest.mark.parametrize(
    "mutation,message",
    [
        ("binding", "parent_plan"),
        ("counts", "count identity"),
        ("qubits", "allocation identity"),
        ("native", "native counts"),
        ("endpoint", "endpoint conversion"),
        ("selector", "selector bounds"),
        ("overflow", "overflow certificate"),
        ("parent", "parent_plan mismatch"),
    ],
)
def test_bad_evidence_fails_before_emission(evidence, mutation, message, monkeypatch):
    parent, cert, base = deepcopy(evidence)
    if mutation == "binding":
        del base["parent_plan"]
    elif mutation == "counts":
        base["total"]["cx"] += 1
    elif mutation == "qubits":
        base["qubits"] -= 1
    elif mutation == "native":
        base["native"]["cx"] += 1
    elif mutation == "endpoint":
        base["row_checks"][0]["price_integer"] += 1
    elif mutation == "selector":
        cert["selector_bits"] = 2
    elif mutation == "overflow":
        cert["overflow_safe"] = False
    else:
        cert["parent_plan"]["strike_sum"] += 1

    def forbidden(*args, **kwargs):
        pytest.fail("oracle emitted before evidence validation")

    monkeypatch.setattr(module, "_oracle", forbidden)
    with pytest.raises((ValueError, ArithmeticError), match=message):
        module.residual_components(parent, cert, base)


@pytest.mark.parametrize("cap", ["MAX_ORACLE_GATES", "MAX_ORACLE_QUBITS", "MAX_COMPONENT_GATES"])
def test_resource_caps(evidence, monkeypatch, cap):
    monkeypatch.setattr(module, cap, 1)
    with pytest.raises(module.ResourceLimitError):
        module.residual_components(*evidence)


def test_json_roundtrip_plan_binding(evidence):
    parent, cert, base = evidence
    cert = json.loads(json.dumps(cert))
    base = json.loads(json.dumps(base))
    result = module.residual_components(parent, cert, base)
    assert len(result["parent_plan_sha256"]) == 64
