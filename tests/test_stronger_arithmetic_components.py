"""Small emitted circuits only; no production menu acquisition."""

import json

import pytest

from research.stronger_arithmetic import components as module
from research.journal_sprint.fixed_exp_budget import evaluate_integer
from research.journal_sprint.reversible_fixed_point import Program


def tiny_plan():
    return dict(
        normal_qubits=2,
        selector_bits=4,
        width=6,
        fraction_bits=1,
        affine_rows=[(-1, [1, 2]), (0, [1, 0])],
        exp_budget=dict(coefficients=[2, 2], intermediate_magnitude_upper="3"),
        strike_sum=3,
        overflow_safe=True,
    )


@pytest.fixture(autouse=True)
def clear_cache():
    module._acquire.cache_clear()
    module._kernel.cache_clear()
    yield
    module._acquire.cache_clear()
    module._kernel.cache_clear()


def test_actual_remapped_program_depth_semantics_and_native(monkeypatch):
    ledgers = []
    original_init, original_extend = module._Ledger.__init__, module._Ledger.extend

    def init(self, qubits):
        original_init(self, qubits)
        self.recording = Program(compact=True)
        self.recording.register(qubits)
        ledgers.append(self)

    def extend(self, p, mapping, inverse=False):
        original_extend(self, p, mapping, inverse)
        for gate in reversed(p.gates) if inverse else p.gates:
            self.recording.gate(*(mapping[b] for b in gate))

    monkeypatch.setattr(module._Ledger, "__init__", init)
    monkeypatch.setattr(module._Ledger, "extend", extend)
    plan = tiny_plan()
    result = module.components(plan)
    json.dumps(result, allow_nan=False)
    assert result["reused"]["qubits"] < result["retained"]["qubits"]
    assert result["reused"]["native"] == result["retained"]["native"]
    for ledger, name in zip(ledgers, ("retained", "reused")):
        p, report = ledger.recording, result[name]
        actual = p.resources()
        for key in ("qubits", "x", "cx", "ccx", "logical_depth"):
            assert report[key] == actual[key]
        assert report["emitted_gate_applications"] == len(p.gates)
        for key in ("x", "cx", "ccx"):
            assert report[key] == (
                2 * report["conversion_forward"][key]
                + 2 * report["aggregation"][key]
                + 2 * report["postaggregation_payoff"][key]
                + report["comparator"][key]
            )
        for packed in range(4):
            prices = [
                evaluate_integer(
                    a + sum(((packed >> k) & 1) * c for k, c in enumerate(cs)), [2, 2], 1
                )
                for a, cs in plan["affine_rows"]
            ]
            payoff = max(sum(prices) - plan["strike_sum"], 0)
            for selector in range(16):
                for flag in (0, 1):
                    initial = packed | (selector << 2) | (flag << 6)
                    assert p.run(initial) == initial ^ (int(selector < payoff) << 6)
        assert all(r["clean_workspace"] for r in report["row_checks"])
    from qiskit import transpile

    native = transpile(
        ledgers[1].recording.to_qiskit(), basis_gates=["u", "cx"], optimization_level=0
    )
    assert result["reused"]["native"] == dict(native.count_ops())


def test_reduced_endpoint_map_and_paired_interface():
    plan = tiny_plan()
    plan.update(reductions=1, spot=2)
    plan["exp_budget"].update(
        reductions=1, spot=2, overflow_safe=True, output_integer_bounds=[0, 6]
    )
    both = module.components(plan, reduced=True)
    assert module.components(plan, reuse=True, reduced=True) == both["reused"]
    for row in both["reused"]["row_checks"]:
        y = evaluate_integer(row["log_integer"] >> 1, [2, 2], 1)
        assert row["price_integer"] == 2 * (y * y // 2)
    assert module._acquire.cache_info().hits == 1


@pytest.mark.parametrize("reduced", [False, True])
def test_bulk_remap_matches_actual_emitters(reduced):
    from research.journal_sprint.reversible_fixed_point import affine, horner
    from research.stronger_arithmetic.circuits import conversion_program

    kernel = module._kernel(
        5,
        1,
        (2, 2),
        reduced,
        1 if reduced else 0,
        2,
        module.MAX_CONVERSION_GATES,
        module.MAX_CONVERSION_QUBITS,
    )
    p, inputs, log, out = module._conversion(2, 5, (-1, (1, 2)), kernel)
    if reduced:
        expected, ei, el, eo = conversion_program(2, 5, (-1, (1, 2)), (2, 2), 1, 1, 2)
    else:
        expected = Program(compact=True)
        ei, el, eo = expected.register(2), expected.register(5), expected.register(5)
        affine(expected, ei, el, -1, (1, 2))
        horner(expected, el, eo, (2, 2), 1)
    assert (inputs, log, out) == (ei, el, eo)
    assert p.qubits == expected.qubits
    assert list(p.gates) == list(expected.gates)


def test_equal_effective_coefficients_cache_and_independent_returns():
    plan = tiny_plan()
    first = module.components(plan)
    plan["degree"] = 12
    plan["exp_budget"]["coefficients"] += [0, 0]
    second = module.components(plan)
    assert module._acquire.cache_info().hits == 1
    assert first == second
    second["reused"]["native"]["cx"] = -1
    assert module.components(plan) == first


@pytest.mark.parametrize(
    "change,message",
    [
        (dict(overflow_safe=False), "overflow_safe"),
        (dict(selector_bits=1), "universal selector"),
        (dict(strike_sum=25), "universal sum/poststrike"),
    ],
)
def test_universal_certificate_before_emission(monkeypatch, change, message):
    def forbidden(*args, **kwargs):
        pytest.fail("emitted before validating certificate")

    monkeypatch.setattr(module, "_kernel", forbidden)
    plan = tiny_plan()
    plan.update(change)
    with pytest.raises(ArithmeticError, match=message):
        module.components(plan)


@pytest.mark.parametrize(
    "cap,value",
    [("MAX_CONVERSION_GATES", 10), ("MAX_CONVERSION_QUBITS", 10), ("MAX_COMPONENT_GATES", 10)],
)
def test_protocol_caps(monkeypatch, cap, value):
    monkeypatch.setattr(module, cap, value)
    with pytest.raises(module.ResourceLimitError):
        module.components(tiny_plan())


def test_certificate_revalidated_on_cache_hit():
    plan = tiny_plan()
    module.components(plan)
    plan["payoff_upper_integer"] = 0
    with pytest.raises(ArithmeticError, match="checked payoff"):
        module.components(plan)


def test_selector_certificate_can_use_tighter_plan_bound():
    plan = tiny_plan()
    plan.update(selector_bits=3, payoff_upper_integer=4)
    result = module.components(plan)
    assert result["retained"]["poststrike_bounds"]["universal_selector_safe"]
