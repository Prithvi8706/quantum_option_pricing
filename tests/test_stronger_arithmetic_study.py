"""Menu and decision-boundary tests for the bounded comparator study."""

from copy import deepcopy

import pytest

from research.stronger_arithmetic.run_study import CONFIG, menu, resources, summarize


def test_complete_predeclared_cartesian_menu():
    entries = menu()
    assert len(entries) == 36
    assert len({tuple(sorted(row.items())) for row in entries}) == 36
    assert {r["fraction_bits"] for r in entries} == {20, 24}
    assert {r["width"] for r in entries} == {40, 48}
    assert {r["degree"] for r in entries} == {8, 12, 16}
    assert {r["reductions"] for r in entries} == {1, 2, 3}
    assert CONFIG["cases"] == ["D1", "D2"]
    assert not CONFIG["confirmation"]


def test_composed_cost_includes_both_a_directions_and_iqft_swaps(monkeypatch):
    monkeypatch.setattr("research.stronger_arithmetic.run_study.zero_cost", lambda n: 41)
    ae = dict(status="ideal_plan", M=8, repetitions=17, phase_qubits=3)
    actual = resources(dict(cx=20, u=13), 4, ae)
    assert actual["control_cancelled_total_cx_projection"] == 17 * (20 + 7 * (40 + 41 + 1) + 6 + 3)
    assert actual["total_cx_projection"] == 17 * (20 + 7 * (2 * (120 + 26) + 41 + 1) + 6 + 3)
    assert actual["total_qubits"] == 9
    assert actual["physical_execution_error"] is None


@pytest.mark.parametrize("status", ["query_cap", "deterministic_budget_exhausted"])
def test_failed_schedule_has_no_total_cost(monkeypatch, status):
    monkeypatch.setattr("research.stronger_arithmetic.run_study.zero_cost", lambda n: 41)
    result = resources(dict(cx=20, u=13), 4, dict(status=status))
    assert result["total_cx_projection"] is None
    assert result["control_cancelled_total_cx_projection"] is None
    assert result["total_qubits"] is None


@pytest.mark.parametrize(
    "arithmetic,expected", [(50, "arithmetic"), (100, "tie"), (200, "reflection")]
)
def test_summary_preserves_ties_and_reversals(arithmetic, expected):
    references = {
        case: {
            "alternatives": [
                {"mode": "reflection", "resources": {"control_cancelled_total_cx_projection": 100}},
                {"mode": "ripple", "resources": {"control_cancelled_total_cx_projection": 300}},
            ]
        }
        for case in CONFIG["cases"]
    }
    rows = [
        dict(
            case=case,
            arm="range_reduced",
            status="ideal_plan",
            resources={"control_cancelled_total_cx_projection": arithmetic},
        )
        for case in CONFIG["cases"]
    ]
    bad = deepcopy(rows[0])
    bad.update(status="deterministic_budget_exhausted", resources=None)
    result = summarize(rows + [bad], references)
    assert all(r["winner"] == expected for r in result)
    assert all(r["feasible_rows"] == 1 for r in result)


def test_summary_does_not_promote_missing_feasible_plan():
    references = {
        case: {
            "alternatives": [
                {"mode": "reflection", "resources": {"control_cancelled_total_cx_projection": 100}},
                {"mode": "ripple", "resources": {"control_cancelled_total_cx_projection": 300}},
            ]
        }
        for case in CONFIG["cases"]
    }
    assert all(r["best_reduced"] is None for r in summarize([], references))
