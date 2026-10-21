"""Render the 110-item local execution ledger beside its frozen research plan."""

import json

from research.limitation_program_20261001.progress import ROOT


def render():
    program = ROOT / "results/limitation_program_20261001"
    state = json.loads((program / "progress.json").read_text(encoding="utf-8"))
    roadmap = json.loads(
        (ROOT / "docs/limitation_audit_20261001/implementation_plan/roadmap.json").read_text(
            encoding="utf-8"
        )
    )
    baseline = ROOT / state["accepted_baseline"]
    summary = json.loads((baseline / "summary.json").read_text(encoding="utf-8"))
    lines = [
        "# Local limitation-program status\n\n",
        "This is the current execution ledger for the "
        "[complete implementation plan](../limitation_audit_20261001/IMPLEMENTATION_PLAN.md). "
        "Current scope status comes from the live ledger; execution status records this program's "
        "scoped results. A passed component does not close the entire limitation.\n\n",
        f"Updated UTC: {state['updated_utc']}. All execution is local.\n\n",
        f"Current phase: {state['phase']}.\n\n",
        f"Next action: {state.get('next_action', 'See the plan dependencies')}.\n\n",
        f"Accepted source: [{baseline.name}]"
        f"(../../{baseline.relative_to(ROOT).as_posix()}/summary.json).\n\n",
        "| Case | T gates | T-depth | Clifford+T depth | Logical qubits |\n",
        "|---|---:|---:|---:|---:|\n",
    ]
    for case in summary["cases"]:
        resource = case.get("candidate", case.get("resources"))
        if resource is None:
            raise ValueError("accepted case has no resource row")
        lines.append(
            f"| {case['case']} | {resource['t_count']:,} | {resource['t_depth']:,} | "
            f"{resource['clifford_t_depth']:,} | {resource['logical_qubits']:,} |\n"
        )
    lines.append("\n## Evidence gates\n\n| Gate | Current status |\n|---|---|\n")
    for gate, status in state["gates"].items():
        lines.append(f"| {gate} | {status} |\n")
    sections = {
        "A": "Arithmetic",
        "E": "Estimators",
        "F": "Formulations",
        "H": "Hardware",
        "C": "Contract and evidence",
    }
    for prefix, title in sections.items():
        lines.extend(
            [
                f"\n## {title}\n\n",
                "| Item | Limitation / work item | "
                "Current scope status | Current execution |\n|---|---|---|---|\n",
            ]
        )
        for entry in roadmap["entries"]:
            if not entry["id"].startswith(prefix):
                continue
            execution = state["entries"][entry["id"]]["execution_status"].replace("|", "\\|")
            scope_status = state["entries"][entry["id"]]["plan_status"]
            lines.append(f"| {entry['id']} | {entry['title']} | {scope_status} | {execution} |\n")
    lines.append(
        "\nThe [machine-readable ledger](../../results/limitation_program_20261001/"
        "progress.json) preserves decisions and receipt links. G2 continuous-dollar "
        "error, G3 compatible estimation, G4 actual matched classical timings and "
        "G5 physical resources remain separate obligations.\n"
    )
    destination = ROOT / "docs/limitation_program_20261001/STATUS.md"
    destination.write_text("".join(lines), encoding="utf-8")
    print("Rendered", len(roadmap["entries"]), "work items", flush=True)
    return destination


if __name__ == "__main__":
    render()
