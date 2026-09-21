"""Read-only reconciliation of complete or interrupted week-12 attempts."""

import json
from pathlib import Path
from .unequal_allocation import ARMS, PILOT


def event_prefix(path):
    if not path.exists():
        return [], False
    raw = path.read_bytes()
    lines = raw.splitlines(keepends=True)
    events = []
    truncated = False
    for i, line in enumerate(lines):
        try:
            event = json.loads(line.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            if i != len(lines) - 1 or line.endswith(b"\n"):
                raise ValueError("interior event corruption")
            truncated = True
            break
        events.append(event)
    return events, truncated


def reconcile(output):
    output = Path(output)
    schedule = json.loads((output / "schedule.json").read_text())
    events, truncated_tail = event_prefix(output / "events.jsonl")
    failure_attempt = None
    if (output / "failure.json").exists():
        try:
            failure_attempt = json.loads((output / "failure.json").read_text()).get("attempt")
        except (ValueError, UnicodeDecodeError):
            pass  # Keep unresolved; never fabricate a successful terminal state.
    grouped = {}
    for event in events:
        attempt = event["attempt"]
        if attempt is None and event["event"] == "failed":
            continue  # setup/finalization failure, not an invented trial
        if (
            isinstance(attempt, bool)
            or not isinstance(attempt, int)
            or not 0 <= attempt < len(schedule)
        ):
            raise ValueError("invalid event attempt")
        grouped.setdefault(attempt, []).append(event)
    rows, states = [], {}
    for spec in schedule:
        attempt = spec["attempt"]
        history = grouped.get(attempt, [])
        path = output / f"row_{attempt:05d}.json"
        if not history:
            if path.exists():
                raise ValueError("raw row without attempt")
            states[str(attempt)] = "not_started"
            continue
        if history[0]["event"] != "started":
            raise ValueError("missing attempt start")
        pending, purposes, plan = None, set(), None
        arm = spec["arm"]
        if arm not in ARMS:
            raise ValueError("unknown recovery arm")
        paid = arm in ("pilot_cp", "unequal_full", "unequal_target")
        order = (["pilot"] if paid else []) + ["calibration_0", "calibration_1", "pricing"]
        shots = cx = 0
        terminal = None
        for event in history[1:]:
            kind = event["event"]
            if terminal is not None:
                # Completed raw row followed by infrastructure failure is retained.
                if kind == "failed" and terminal == "completed":
                    terminal = "failed_after_completed"
                    continue
                raise ValueError("events after terminal state")
            if kind == "draw_started":
                if pending is not None or event["purpose"] in purposes:
                    raise ValueError("overlapping/duplicate draws")
                if len(purposes) >= len(order) or event["purpose"] != order[len(purposes)]:
                    raise ValueError("draw order/arm mismatch")
                if event["purpose"] not in ("pilot", "calibration_0", "calibration_1", "pricing"):
                    raise ValueError("unknown draw purpose")
                for field in ("shots", "logical_cx"):
                    if (
                        isinstance(event[field], bool)
                        or not isinstance(event[field], int)
                        or event[field] < (1 if field == "shots" else 0)
                    ):
                        raise ValueError("invalid draw resource")
                if event["purpose"] != "pilot" and plan is None:
                    raise ValueError("terminal draw before plan")
                expected_shots = (
                    PILOT
                    if event["purpose"] == "pilot"
                    else plan[
                        {"calibration_0": "m0", "calibration_1": "m1", "pricing": "n"}[
                            event["purpose"]
                        ]
                    ]
                )
                if event["shots"] != expected_shots or shots + event["shots"] > 65536:
                    raise ValueError("draw count/plan/budget mismatch")
                if event["purpose"].startswith("calibration") and event["logical_cx"] != 0:
                    raise ValueError("calibration CX model mismatch")
                pending = event
            elif kind == "draw_completed":
                if pending is None or any(
                    event[k] != pending[k] for k in ("purpose", "shots", "logical_cx")
                ):
                    raise ValueError("draw completion mismatch")
                count = event["successes"]
                if (
                    isinstance(count, bool)
                    or not isinstance(count, int)
                    or not 0 <= count <= event["shots"]
                ):
                    raise ValueError("invalid completed count")
                shots += event["shots"]
                cx += event["logical_cx"]
                purposes.add(event["purpose"])
                pending = None
            elif kind == "plan_frozen":
                if plan is not None or pending is not None:
                    raise ValueError("invalid plan boundary")
                plan = event["plan"]
                if not isinstance(plan, dict) or plan.get("arm") != arm:
                    raise ValueError("invalid frozen plan")
                if purposes != ({"pilot"} if paid else set()):
                    raise ValueError("pilot/plan order mismatch")
                if plan.get("pilot_shots") != (PILOT if paid else 0):
                    raise ValueError("pilot plan mismatch")
                for field in ("m0", "m1", "n"):
                    value = plan.get(field)
                    if isinstance(value, bool) or not isinstance(value, int) or value < 256:
                        raise ValueError("invalid plan counts")
                total = sum(plan[k] for k in ("pilot_shots", "m0", "m1", "n"))
                if total > 65536 or (
                    arm in ("fixed_cp", "pilot_cp", "unequal_full") and total != 65536
                ):
                    raise ValueError("plan budget mismatch")
            elif kind in ("completed", "failed"):
                if kind == "completed" and pending is not None:
                    raise ValueError("completed with in-flight draw")
                terminal = kind
            else:
                raise ValueError("unknown event")
        saved, incomplete_raw = None, False
        if path.exists():
            try:
                saved = json.loads(path.read_text())["result"]
            except (ValueError, KeyError, UnicodeDecodeError):
                incomplete_raw = True
        if saved is not None:
            if saved["spec"] != spec or saved["total_shots"] != shots or saved["total_cx"] != cx:
                raise ValueError("raw resource/identity mismatch")
        if terminal == "completed" and saved is None:
            raise ValueError("completed event missing raw row")
        if terminal == "completed" and plan is not None and purposes != set(order):
            raise ValueError("completed before terminal acquisitions")
        if failure_attempt == attempt:
            terminal = "failed"
        state = (
            "completed"
            if terminal == "completed"
            else "raw_needs_reconciliation"
            if incomplete_raw
            else "raw_needs_reconciliation"
            if saved is not None
            else "failed"
            if terminal == "failed"
            else "interrupted"
        )
        states[str(attempt)] = state
        rows.append(
            dict(
                spec=spec,
                state=state,
                completed_shots=shots,
                completed_cx=cx,
                in_flight_shots_upper=0 if pending is None else pending["shots"],
                in_flight_cx_upper=0 if pending is None else pending["logical_cx"],
                delivered=bool(state == "completed" and saved["status"] == "precision_met"),
                penalized_cost=saved["penalized_cost"] if state == "completed" else 65536,
            )
        )
    return dict(
        planned=len(schedule),
        started=len(rows),
        completed=sum(s == "completed" for s in states.values()),
        unattempted=sum(s == "not_started" for s in states.values()),
        states=states,
        attempted_outcomes=rows,
        completed_shots=sum(r["completed_shots"] for r in rows),
        unresolved_shots_upper=sum(r["in_flight_shots_upper"] for r in rows),
        truncated_event_tail=truncated_tail,
        resource_accounting_complete=not truncated_tail,
        mean_penalized_cost_among_started=None
        if not rows
        else sum(r["penalized_cost"] for r in rows) / len(rows),
    )
