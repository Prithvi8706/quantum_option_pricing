"""Future scheduler budget guards; the four frozen A18 attempts remain v1.

Global budget exhaustion bypasses ordinary legal-eviction failures.  The event
counter records admitted checks only, and a separate counter records the single
terminal failed budget check.  Arithmetic and allocation heuristics are inherited
unchanged from the immutable first implementation.
"""

from copy import deepcopy
from time import process_time

from research.limitation_program_20261001.checkpoint_scheduler import (
    HEURISTICS,
    LIMITS,
    PlanningError,
    _Planner,
    _scope_plan,
    minimum_required,
    retain_all,
    validate_schedule,
)


ALGORITHM = "paid-atomic-dag-checkpointing-v2"


class BudgetExceededError(RuntimeError):
    """Terminal global exhaustion, deliberately outside PlanningError catches."""


class _PlannerV2(_Planner):
    def __init__(self, plan, cap, heuristic):
        super().__init__(plan, cap, heuristic)
        self.aborted_budget_checks = 0

    def fail_budget(self, reason):
        self.aborted_budget_checks += 1
        raise BudgetExceededError(reason)

    def tick(self):
        if process_time() - self.started > LIMITS["max_cpu_seconds"]:
            self.fail_budget("process CPU limit")
        if self.events >= LIMITS["max_events"]:
            self.fail_budget("recursive event limit")
        self.events += 1

    def record(self, move):
        if move["kind"] != "copy_output":
            if self.paid_moves >= LIMITS["max_moves"]:
                self.fail_budget("paid invocation limit")
            self.paid_moves += 1
        self.moves.append(move)


def schedule(plan, cap, heuristic):
    """Plan with exact global guards; intended only for future protocols."""
    if heuristic not in HEURISTICS:
        raise ValueError("undeclared checkpointing heuristic")
    minimum = minimum_required(plan)
    if int(cap) < minimum["total"]:
        return dict(
            passed=False,
            algorithm=ALGORITHM,
            heuristic=heuristic,
            cap=int(cap),
            reason="mandatory leaf and live predecessor lower bound exceeds cap",
            infeasible_proved=True,
            minimum_required=minimum,
            moves=[],
            events=0,
            aborted_budget_checks=0,
            limits=deepcopy(LIMITS),
        )
    planner = _PlannerV2(plan, cap, heuristic)
    try:
        result = planner.run()
        result.update(
            algorithm=ALGORITHM,
            minimum_required=minimum,
            aborted_budget_checks=planner.aborted_budget_checks,
        )
        result["legality"] = validate_schedule(plan, result)
        return result
    except (PlanningError, BudgetExceededError) as exc:
        return dict(
            passed=False,
            algorithm=ALGORITHM,
            heuristic=heuristic,
            cap=int(cap),
            reason=str(exc),
            infeasible_proved=False,
            minimum_required=minimum,
            moves=[],
            discarded_partial_moves=len(planner.moves),
            events=planner.events,
            aborted_budget_checks=planner.aborted_budget_checks,
            process_cpu_seconds=process_time() - planner.started,
            limits=deepcopy(LIMITS),
        )


def plan_checkpoint(scope, cap, heuristic):
    names = {"block-checkpointing": "block", "cost-aware": "cost-aware"}
    if heuristic not in names:
        raise ValueError("undeclared financial checkpointing heuristic")
    result = schedule(_scope_plan(scope), cap, names[heuristic])
    result["heuristic"] = heuristic
    result["feasible"] = result["passed"]
    return result


def retain_all_plan(scope):
    result = retain_all(_scope_plan(scope))
    result["feasible"] = result["passed"]
    return result
