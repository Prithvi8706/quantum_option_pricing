"""Prospective tiny fixtures for terminal scheduler budget exhaustion."""

import pytest

from research.limitation_program_20261001 import checkpoint_scheduler_v2 as scheduler


def tiny_chain():
    return dict(
        floor=4,
        groups=[
            dict(
                id=gid,
                preds=[gid - 1] if gid else [],
                width=2,
                private=1,
                cost=10 + gid,
                outputs=[gid],
            )
            for gid in range(3)
        ],
        outputs=[dict(outputname="out", value=2, group=2)],
    )


@pytest.mark.parametrize("budget", (0, 1, 2, 5, 17, 40))
def test_end_to_end_budget_edges_never_increment_past_declared_limit(monkeypatch, budget):
    monkeypatch.setitem(scheduler.LIMITS, "max_events", budget)
    result = scheduler.schedule(tiny_chain(), 11, "cost-aware")
    assert result["events"] <= budget
    if result["passed"]:
        assert result["aborted_budget_checks"] == 0
        assert result["leaf_invocations"] == 6
        assert result["legality"]["all_intermediates_erased"]
    else:
        assert result["reason"] == "recursive event limit"
        assert result["events"] == budget
        assert result["aborted_budget_checks"] == 1
        assert not result["moves"]


def test_nested_eviction_does_not_catch_terminal_budget_as_ordinary_failure(monkeypatch):
    planner = scheduler._PlannerV2(tiny_chain(), 9, "cost-aware")
    planner.ensure(0, set())
    planner.ensure(1, set())
    monkeypatch.setitem(scheduler.LIMITS, "max_events", planner.events + 1)
    restored = []
    original_restore = planner.restore

    def track_restore(snapshot):
        restored.append(True)
        original_restore(snapshot)

    monkeypatch.setattr(planner, "restore", track_restore)
    with pytest.raises(scheduler.BudgetExceededError, match="recursive event limit"):
        planner.make_room(3, {1})
    assert not restored, "ordinary eviction caught terminal global budget exhaustion"
    assert planner.events == scheduler.LIMITS["max_events"]
    assert planner.aborted_budget_checks == 1
    assert len(planner.moves) == 2


def test_paid_invocation_budget_is_terminal_and_checked_before_append(monkeypatch):
    monkeypatch.setitem(scheduler.LIMITS, "max_moves", 2)
    result = scheduler.schedule(tiny_chain(), 9, "cost-aware")
    assert not result["passed"]
    assert result["reason"] == "paid invocation limit"
    assert result["discarded_partial_moves"] == 2
    assert result["aborted_budget_checks"] == 1
    assert not result["moves"]


def test_cpu_limit_does_not_admit_an_event(monkeypatch):
    planner = scheduler._PlannerV2(tiny_chain(), 11, "cost-aware")
    monkeypatch.setattr(scheduler, "process_time", lambda: planner.started + 901)
    with pytest.raises(scheduler.BudgetExceededError, match="process CPU limit"):
        planner.tick()
    assert planner.events == 0
    assert planner.aborted_budget_checks == 1


def test_budget_exception_is_not_an_ordinary_eviction_error():
    assert not issubclass(scheduler.BudgetExceededError, scheduler.PlanningError)
