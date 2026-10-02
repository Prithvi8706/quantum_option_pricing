"""Verify immutable Stage A bytes and the scope of post-run source changes."""

import ast
import hashlib
import json
from pathlib import Path

from research.frontier_completion_20260927.stage_a import OUT, ROOT


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def functions(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return {
        n.name: ast.dump(n, include_attributes=False)
        for n in tree.body
        if isinstance(n, ast.FunctionDef)
    }


def verify():
    inventory = json.loads((OUT / "artifact_hashes.json").read_text())
    mismatches = [name for name, expected in inventory.items() if digest(OUT / name) != expected]
    if mismatches:
        raise AssertionError(mismatches)
    receipt = json.loads((OUT / "environment.json").read_text())
    executed = OUT / "executed_stage_a.py"
    assert digest(executed) == receipt["script_sha256"]
    spec = ROOT / "manuscript/advantage-frontier-2026-09-23/ANALYSIS_SPEC.md"
    assert digest(spec) == receipt["analysis_spec_sha256"]
    original, current = functions(executed), functions(Path(__file__).with_name("stage_a.py"))
    scientific = sorted(set(original) - {"main"})
    assert all(original[name] == current[name] for name in scientific)
    summary = json.loads((OUT / "summary.json").read_text())
    assert summary["artifact_count"] == len(inventory)
    for case in summary["cases"]:
        records = json.loads((OUT / case["case"] / "basis_replay.json").read_text())
        assert len(records) == (20 if case["case"] == "B4x12" else 4)
        assert all(record["passed"] for record in records)
        assert len(records) == case["basis_cases_passed"]
    return dict(
        files_verified=len(inventory),
        executed_script_matches_receipt=True,
        specification_matches_receipt=True,
        unchanged_scientific_functions=scientific,
        post_run_changes="Formatting; main adds distinct --output, refuses nonempty directories "
        "and archives its own source. Original executed source is preserved.",
        basis_cases=24,
        complete_pricing_or_physical_certification=False,
    )


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
