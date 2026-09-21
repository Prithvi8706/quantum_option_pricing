"""Post-run integrity checks and descriptive response-model diagnostics."""

from .checks import require

import importlib.metadata
import json
import shutil

from .storage import ROOT, finish_run, sha256, start_run, write_json


def main():
    source = ROOT / "results/journal_sprint/week3_circuits_v1_retry1"
    manifest = json.loads((source / "complete.json").read_text())
    for name, value in manifest["sha256"].items():
        require(sha256(source / name) == value, name)
    summary = json.loads((source / "summary.json").read_text())
    rows = summary["rows"]
    require(len(rows) == 24 and len({r["id"] for r in rows}) == 24)
    events = [json.loads(line) for line in (source / "events.jsonl").read_text().splitlines()]
    require(len(events) == 48)
    for row, planned, completed in zip(rows, events[::2], events[1::2]):
        require(planned == {"event": "planned", "id": row["id"]})
        require(completed == {"event": "completed", "id": row["id"]})
    path = start_run(
        "results/journal_sprint/week3_circuit_analysis_v1",
        {
            "purpose": "post-run diagnostics, not preregistered model fitting",
            "source_manifest_sha256": sha256(source / "complete.json"),
        },
    )
    shutil.copy2(__file__, path / "analyze_circuit_gate.py")
    diagnostics = []
    for row in rows:
        for kind, noise in row["noise"].items():
            # The old model allows only q=.5+v*(ideal-.5), 0<=v<=1.
            lower, upper = sorted([0.5, row["ideal"]])
            value = noise["probability"]
            diagnostics.append(
                {
                    "id": row["id"],
                    "channel": kind,
                    "probability": value,
                    "ideal": row["ideal"],
                    "allowed_symmetric_range": [lower, upper],
                    "outside_any_eta_response": value < lower - 1e-9 or value > upper + 1e-9,
                    "channel_locations": noise["channel_locations"],
                }
            )
    write_json(path / "diagnostics.json", diagnostics)
    write_json(
        path / "verification.json",
        {
            "artifacts_verified": len(manifest["sha256"]),
            "events_verified": len(events),
            "max_ideal_difference": summary["max_ideal_difference"],
            "outside_symmetric_response": {
                kind: sum(
                    d["outside_any_eta_response"] for d in diagnostics if d["channel"] == kind
                )
                for kind in ("depolarizing", "amplitude_damping")
            },
            "environment": {
                name: importlib.metadata.version(name)
                for name in ("qiskit-terra", "qiskit-aer", "qiskit-finance", "numpy", "scipy")
            },
            "all_integrity_checks_pass": True,
            "limitation": "Inside the range does not establish a common eta across depths",
        },
    )
    finish_run(path)
    print((path / "verification.json").read_text())


if __name__ == "__main__":
    main()
