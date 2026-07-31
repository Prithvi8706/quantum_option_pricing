from research.paper_a.benchmark import VALIDATION_SET, by_id
from research.paper_a.payoff import C_RESCALING
from research.paper_a.validation import all_passed, run_e0_gates

GATES = ("probability_normalization", "pmf_max_elementwise", "pmf_l1",
         "objective_probability", "dollar_round_trip", "error_identity",
         "discount_applied_once", "raw_and_clipped_separate")


def test_every_named_gate_is_reported():
    results = run_e0_gates([by_id("E025")], 1e-4, (3,), C_RESCALING)
    assert {r.name for r in results} == set(GATES)


def test_gates_pass_on_the_validation_fixtures():
    results = run_e0_gates(list(VALIDATION_SET)[:4], 1e-4, (2, 3),
                           C_RESCALING)
    failures = [r for r in results if not r.passed]
    assert not failures, [(f.name, f.worst, f.tolerance) for f in failures]


def test_gates_pass_across_all_specified_qubit_counts():
    results = run_e0_gates([by_id("E025")], 1e-4, (2, 3, 4, 5), C_RESCALING)
    assert all_passed(results)


def test_each_result_reports_its_worst_value_and_tolerance():
    for r in run_e0_gates([by_id("E025")], 1e-4, (3,), C_RESCALING):
        assert r.tolerance >= 0   # boolean gates carry tolerance 0.0
        assert r.worst >= 0
        assert r.passed == (r.worst <= r.tolerance)


def test_all_passed_is_false_when_any_gate_fails():
    from research.paper_a.validation import GateResult
    mixed = [GateResult("a", True, 0.0, 1e-10, ""),
             GateResult("b", False, 1.0, 1e-10, "")]
    assert not all_passed(mixed)
