"""Freeze the verified local square-root wave without modifying old receipts."""

import argparse
import contextlib
from datetime import datetime, timezone
import io
import json
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET

from research.controlled_priority_completion.parallel_source import entries
from research.limitation_program_20261001.constant_library import digest
from research.limitation_program_20261001.progress import ROOT
from research.limitation_program_20261001.validate_receipts_v2 import validate

PROGRAM = ROOT / "results/limitation_program_20261001"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def junit(path):
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else root.findall("testsuite")
    assert suites and all(
        int(s.get(k, 0)) == 0 for s in suites for k in ("failures", "errors", "skipped")
    )
    names = {
        (case.get("classname"), case.get("name"))
        for suite in suites
        for case in suite.findall("testcase")
    }
    count = sum(int(s.get("tests", 0)) for s in suites)
    assert len(names) == count
    return count, names


def run(output):
    output = output.resolve()
    output.relative_to(PROGRAM.resolve())
    assert not output.exists()
    source = PROGRAM / "A11_run001"
    audit = PROGRAM / "A01_run007"
    leaves = PROGRAM / "A11_leaf_run001"
    summary, cost, leaf = (read(path / "summary.json") for path in (source, audit, leaves))
    assert summary["passed"] and summary["accepted"] and cost["passed"] and cost["accepted"]
    assert summary["selected"] == cost["selected"]
    assert leaf["passed"]
    leaf_count, leaf_names = junit(leaves / "regression.xml")
    integration_count, integration_names = junit(source / "integration_tests.xml")
    assert (leaf_count, integration_count) == (42, 36)
    assert not leaf_names & integration_names
    replays = sum(len(case["replays"]) for case in summary["cases"])
    assert replays == 4
    for case in summary["cases"]:
        assert case["accepted"] and case["replay_passed"]
        source_metadata = entries(read(source / case["case"] / "source.json"))
        sqrt_entries = [entry for entry in source_metadata.values() if entry["op"] == "sqrt"]
        assert len(sqrt_entries) == 1 and sqrt_entries[0]["sha256"] == leaf["best"]["sha256"]
        for replay in case["replays"]:
            assert replay["passed"] and replay["actual"]["values"] == replay["expected"]
            assert replay["actual"]["all_input_and_workspace_bits_restored"]
    progress = read(PROGRAM / "progress.json")
    assert len(progress["entries"]) == 110
    assert progress["accepted_baseline"] == str(source.relative_to(ROOT)).replace("\\", "/")
    with contextlib.redirect_stdout(io.StringIO()):
        validation = validate(PROGRAM)
    assert validation["passed"]
    output.mkdir()
    frozen = {}
    for directory in (source, audit, leaves, PROGRAM / "WAVE01_run001"):
        path = directory / "manifest.json"
        frozen[str(path.relative_to(ROOT))] = digest(path)
    for filename in ("finalize_sqrt_wave.py", "validate_receipts_v2.py"):
        path = ROOT / "research/limitation_program_20261001" / filename
        snapshot = output / ("executed_" + filename)
        shutil.copy2(path, snapshot)
        frozen[str(path.relative_to(ROOT))] = digest(path)
    docs = [
        "README.md",
        "STATUS.md",
        "NARROW_SQRT_LEAF.md",
        "NARROW_SQRT_INTEGRATION_REVIEW.md",
        "SQRT_SOURCE_COSTS.md",
    ]
    square = PROGRAM / "A09_square_scope_run001"
    if (square / "manifest.json").is_file():
        frozen[str((square / "manifest.json").relative_to(ROOT))] = digest(square / "manifest.json")
        docs.append("SQUARE_SITE_SCOPE.md")
    square_schedule = PROGRAM / "A10_square_schedule_run001"
    if (square_schedule / "manifest.json").is_file():
        path = square_schedule / "manifest.json"
        frozen[str(path.relative_to(ROOT))] = digest(path)
        docs.append("SQUARE_SCHEDULE_SCREEN.md")
    for filename in docs:
        path = ROOT / "docs/limitation_program_20261001" / filename
        snapshot = output / "documents" / filename
        snapshot.parent.mkdir(exist_ok=True)
        shutil.copy2(path, snapshot)
    shutil.copy2(PROGRAM / "progress.json", output / "progress_at_completion.json")
    save(output / "validation.json", validation)
    result = {
        "passed": True,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "local_only": True,
        "accepted_source": str(source.relative_to(ROOT)),
        "selected": summary["selected"],
        "new_distinct_pytest_cases": leaf_count + integration_count,
        "new_complete_financial_gate_replays": replays,
        "prior_wave_distinct_pytest_cases": 153,
        "prior_wave_financial_gate_replays": 18,
        "total_distinct_pytest_cases": 153 + leaf_count + integration_count,
        "total_financial_gate_replays": 18 + replays,
        "cases": [
            {
                "case": c["case"],
                "before": c["baseline"],
                "after": c["candidate"],
                "t_depth_reduction_percent": 100
                * (1 - c["candidate"]["t_depth"] / c["baseline"]["t_depth"]),
            }
            for c in summary["cases"]
        ],
        "whole_target_bytes_input_law_and_precision_unchanged": True,
        "ssa_storage_and_copy_accounting_unchanged": True,
        "all_actual_sqrt_inputs_have_structural_unsigned46_proof": True,
        "G2_to_G5": "open",
        "A11_entire_limitation_closed": False,
        "remaining_A11_scope": "Non-restoring/Newton comparisons and separate Heston validation",
        "next_action": progress["next_action"],
        "frozen_manifest_count": validation["manifest_count"],
    }
    save(output / "summary.json", result)
    files = {
        str(path.relative_to(ROOT)): digest(path) for path in output.rglob("*") if path.is_file()
    }
    save(output / "manifest.json", {"files": files, "frozen_inputs": frozen})
    print(
        json.dumps(
            {
                "passed": True,
                "output": str(output.relative_to(ROOT)),
                "new_tests": leaf_count + integration_count,
                "new_replays": replays,
            }
        ),
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    run(parser.parse_args().output)
