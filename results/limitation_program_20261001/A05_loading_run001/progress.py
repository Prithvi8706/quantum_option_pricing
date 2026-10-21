"""Local progress memory for the authorized limitation implementation programme."""

from datetime import datetime, timezone
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"


def update_progress(
    active, phase, decision=None, receipts=None, baseline=None, next_action=None, gates=None
):
    PROGRAM.mkdir(parents=True, exist_ok=True)
    path = PROGRAM / "progress.json"
    if path.exists():
        state = json.loads(path.read_text(encoding="utf-8"))
    else:
        roadmap = json.loads(
            (ROOT / "docs/limitation_audit_20261001/implementation_plan/roadmap.json").read_text(
                encoding="utf-8"
            )
        )
        state = dict(
            schema="local-limitation-progress-v1",
            local_only=True,
            entries={
                e["id"]: dict(
                    plan_status=e["status"],
                    execution_status=(
                        "existing verified component"
                        if e["status"] == "complete"
                        else "not started"
                    ),
                )
                for e in roadmap["entries"]
            },
            gates={g: "open" for g in roadmap["gates"]},
            history=[],
            accepted_baseline="results/limitation_audit_20261001/constant_multiplier_v1",
            scope="Exact B4/B8 knock-out arithmetic; other source families "
            "retain their own receipts",
        )
    now = datetime.now(timezone.utc).isoformat()
    state.update(updated_utc=now, active_items=active, phase=phase)
    if gates:
        state["gates"].update(gates)
    if baseline is not None:
        state["accepted_baseline"] = baseline
    if next_action is not None:
        state["next_action"] = next_action
    if decision:
        state["history"].append(
            dict(
                time_utc=now, items=active, phase=phase, decision=decision, receipts=receipts or []
            )
        )
        for item in active:
            if item in state["entries"]:
                state["entries"][item].update(execution_status=decision, receipts=receipts or [])
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)
    return state
