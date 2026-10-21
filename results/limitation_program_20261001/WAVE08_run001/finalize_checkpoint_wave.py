"""Freeze the local A18 workspace frontier and its bounded negative evidence."""

import argparse
import contextlib
from datetime import datetime, timezone
import io
from pathlib import Path
import shutil
import sys
import xml.etree.ElementTree as ET

from research.limitation_program_20261001.constant_library import digest
from research.limitation_program_20261001.experiment_checkpoint import (
    PROGRAM,
    read,
    relative,
    save,
)
from research.limitation_program_20261001.progress import ROOT
from research.limitation_program_20261001.validate_receipts_v2 import validate


def junit(path):
    xml = ET.parse(path).getroot()
    suites = [xml] if xml.tag == "testsuite" else list(xml)
    assert all(int(s.get(f, 0)) == 0 for s in suites for f in ("failures", "errors", "skipped"))
    names = {(c.get("classname"), c.get("name")) for s in suites for c in s.findall("testcase")}
    assert len(names) == sum(int(s.get("tests", 0)) for s in suites)
    return names


def run(output):
    output.relative_to(PROGRAM.resolve())
    assert not output.exists()
    directories = [
        PROGRAM / name
        for name in (
            "A18_run001",
            "A01_run015",
            "A18_B4_run001",
            "A01_run016",
            "A18_budgetfix_run001",
        )
    ]
    sub, subaudit, full, fullaudit, budget = (read(p / "summary.json") for p in directories)
    assert all(r["passed"] for r in (sub, subaudit, full, fullaudit, budget))
    assert sub["retained_workspace_frontier"] == subaudit["retained_workspace_frontier"]
    assert full["retained_workspace_point"] == fullaudit["retained_workspace_point"]
    assert full["checkpoint_global_qubits_saved"] == fullaudit["checkpoint_qubits_saved"]
    testsets = [
        junit(directories[0] / "tests.xml"),
        junit(directories[2] / "tests.xml"),
        junit(directories[4] / "pytest.xml"),
    ]
    assert all(not a & b for i, a in enumerate(testsets) for b in testsets[i + 1 :])
    tests = set().union(*testsets)
    assert len(tests) == 80
    assert sub["new_extracted_subgraph_gate_replays"] == 3
    assert full["new_complete_financial_gate_replays"] == len(full["replays"]) == 3
    assert budget["financial_candidate_attempts"] == budget["complete_financial_replays"] == 0
    progress = read(PROGRAM / "progress.json")
    assert len(progress["entries"]) == 110 and progress["active_items"] == []
    assert (
        progress["accepted_baseline"]
        == "results/limitation_program_20261001/A10_coefficient_run001"
    )
    assert "A19" in progress["next_action"]
    previous = read(PROGRAM / "WAVE07_run001/summary.json")
    output.mkdir()
    frozen = {relative(p / "manifest.json"): digest(p / "manifest.json") for p in directories}
    old = PROGRAM / "WAVE07_run001/manifest.json"
    frozen[relative(old)] = digest(old)
    for name in ("finalize_checkpoint_wave.py", "validate_receipts_v2.py"):
        path = ROOT / "research/limitation_program_20261001" / name
        shutil.copy2(path, output / path.name)
        frozen[relative(path)] = digest(path)
    documents = output / "documents"
    documents.mkdir()
    for name in (
        "README.md",
        "STATUS.md",
        "CHECKPOINTING_RESULTS.md",
        "NEXT_CHECKPOINTING.md",
        "NEXT_STREAMING.md",
    ):
        shutil.copy2(ROOT / "docs/limitation_program_20261001" / name, documents / name)
    shutil.copy2(PROGRAM / "progress.json", output / "progress_at_completion.json")
    commands = []
    for module, arguments in (
        ("experiment_checkpoint", ["prepare", "--output", relative(directories[0])]),
        ("experiment_checkpoint", ["run", "--output", relative(directories[0])]),
        (
            "reconcile_checkpoint_v2",
            ["--producer", relative(directories[0]), "--output", relative(directories[1])],
        ),
        ("experiment_checkpoint_B4", ["prepare", "--output", relative(directories[2])]),
        ("experiment_checkpoint_B4", ["run", "--output", relative(directories[2])]),
        (
            "reconcile_checkpoint_B4",
            ["--producer", relative(directories[2]), "--output", relative(directories[3])],
        ),
        ("experiment_checkpoint_budgetfix", ["--output", relative(directories[4])]),
    ):
        commands.append(
            [sys.executable, "-m", "research.limitation_program_20261001." + module, *arguments]
        )
    save(output / "execution_commands.json", dict(local_only=True, commands=commands))
    summary = dict(
        passed=True,
        local_only=True,
        created_utc=datetime.now(timezone.utc).isoformat(),
        preferred_latency_source=progress["accepted_baseline"],
        preferred_latency_source_unchanged=True,
        retained_B4_workspace_point=relative(directories[2]),
        new_distinct_pytest_cases=len(tests),
        new_complete_financial_gate_replays=3,
        new_extracted_subgraph_gate_replays=3,
        total_distinct_pytest_cases=previous["total_distinct_pytest_cases"] + len(tests),
        total_financial_gate_replays=previous["total_financial_gate_replays"] + 3,
        subgraph_baseline_resources=sub["baseline_resources"],
        subgraph_attempts=sub["attempts"],
        full_B4_matched_control_resources=full["matched_retain_all_resources"],
        full_B4_workspace_resources=full["candidate_resources"],
        checkpoint_global_qubits_saved=full["checkpoint_global_qubits_saved"],
        actual_subgraph_arrays_audited=subaudit["actual_unique_gate_arrays_scanned"],
        actual_B4_arrays_audited=fullaudit["actual_unique_gate_arrays_scanned"],
        candidate_attempts=4,
        full_B4_candidates=1,
        B8_candidates=0,
        failed_cost_aware_budget_counter=100013,
        declared_recursive_budget=100000,
        extra_counter_checks_are_abort_unwinding=True,
        budget_fix_fixture_only=True,
        exact_target_precision_input_law_and_leaf_bytes_preserved=True,
        A18_entire_limitation_closed=False,
        G2_to_G5="open",
        quantum_advantage_established=False,
        next_action=progress["next_action"],
    )
    save(output / "summary.json", summary)
    assert all(digest(ROOT / p) == value for p, value in frozen.items())
    save(
        output / "manifest.json",
        dict(
            files={relative(p): digest(p) for p in output.rglob("*") if p.is_file()},
            frozen_inputs=frozen,
        ),
    )
    # Validation includes this packet. Its immutable manifest intentionally omits
    # the validation result produced afterward, avoiding a circular self-hash.
    with contextlib.redirect_stdout(io.StringIO()):
        result = validate(PROGRAM)
    assert result["passed"]
    save(output / "validation.json", result)
    print(
        "A18 wave frozen",
        len(tests),
        "new tests,3 full and3 extracted replays;",
        result["manifest_count"],
        "manifests,",
        result["distinct_hashed_files"],
        "hashes,0 mismatches",
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.output.resolve())
