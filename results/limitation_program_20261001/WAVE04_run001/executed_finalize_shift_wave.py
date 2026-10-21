"""Freeze the local signed7-shift adoption or stopped-screen decision."""

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
        (c.get("classname"), c.get("name")) for suite in suites for c in suite.findall("testcase")
    }
    assert len(names) == sum(int(s.get("tests", 0)) for s in suites)
    return names


def run(output):
    output = output.resolve()
    output.relative_to(PROGRAM.resolve())
    assert not output.exists()
    source, leaves, audit = (
        PROGRAM / name for name in ("A07_shift_run001", "A07_shift_leaf_run001", "A01_run009")
    )
    result, cost, leaf = (read(path / "summary.json") for path in (source, audit, leaves))
    assert result["passed"] and cost["passed"] and leaf["passed"]
    assert result["accepted"] == cost["accepted"] and result["selected"] == cost["selected"]
    leaf_xml = next(leaves.glob("*.xml"))
    leaf_names, integration_names = junit(leaf_xml), junit(source / "integration_tests.xml")
    assert not leaf_names & integration_names
    replay_count = sum(len(case["replays"]) for case in result["cases"])
    assert replay_count == (4 if result["accepted"] else 0)
    for case in result["cases"]:
        trial_source = read(source / case["case"] / "signed7-barrel/source.json")
        shift_entries = [
            e
            for e in entries(trial_source).values()
            if e.get("input_contract", {}).get("signed_shift_count_bits") == 7
        ]
        assert len(shift_entries) == 1 and shift_entries[0]["sha256"] == leaf["best"]["sha256"]
        for replay in case["replays"]:
            assert replay["passed"] and replay["actual"]["values"] == replay["expected"]
            assert replay["actual"]["all_input_and_workspace_bits_restored"]
    accepted = source if result["accepted"] else PROGRAM / "A11_run001"
    progress = read(PROGRAM / "progress.json")
    assert len(progress["entries"]) == 110
    assert progress["accepted_baseline"] == str(accepted.relative_to(ROOT)).replace("\\", "/")
    prior = read(PROGRAM / "WAVE03_run001/summary.json")
    with contextlib.redirect_stdout(io.StringIO()):
        validation = validate(PROGRAM)
    assert validation["passed"]
    output.mkdir()
    frozen = {}
    for path in (
        source / "manifest.json",
        leaves / "manifest.json",
        audit / "manifest.json",
        PROGRAM / "WAVE03_run001/manifest.json",
        PROGRAM / "A07_shift_scope_run002/manifest.json",
    ):
        frozen[str(path.relative_to(ROOT))] = digest(path)
    for name in ("finalize_shift_wave.py", "validate_receipts_v2.py"):
        path = ROOT / "research/limitation_program_20261001" / name
        shutil.copy2(path, output / ("executed_" + name))
        frozen[str(path.relative_to(ROOT))] = digest(path)
    for name in (
        "README.md",
        "STATUS.md",
        "NARROW_SHIFT_LEAF.md",
        "NARROW_SHIFT_INTEGRATION_REVIEW.md",
        "SHIFT_SOURCE_COSTS.md",
        "SHIFT_CONTROL_SCOPE.md",
        "NEXT_NONRESTORING_SQRT.md",
    ):
        snapshot = output / "documents" / name
        snapshot.parent.mkdir(exist_ok=True)
        shutil.copy2(ROOT / "docs/limitation_program_20261001" / name, snapshot)
    shutil.copy2(PROGRAM / "progress.json", output / "progress_at_completion.json")
    save(output / "validation.json", validation)
    save(
        output / "summary.json",
        {
            "passed": True,
            "local_only": True,
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "adopted": result["accepted"],
            "accepted_source": str(accepted.relative_to(ROOT)),
            "candidate_source": str(source.relative_to(ROOT)),
            "selected": result["selected"],
            "new_distinct_pytest_cases": len(leaf_names | integration_names),
            "new_complete_financial_gate_replays": replay_count,
            "total_distinct_pytest_cases": prior["total_distinct_pytest_cases"]
            + len(leaf_names | integration_names),
            "total_financial_gate_replays": prior["total_financial_gate_replays"] + replay_count,
            "cases": [
                {
                    "case": c["case"],
                    "before": c["baseline"],
                    "candidate": c["trials"][0]["resources"],
                    "eligible": c["trials"][0]["eligible"],
                }
                for c in result["cases"]
            ],
            "financial_target_bytes_precision_input_law_unchanged": True,
            "native_two_argument_copy_contract_and_ssa_storage_unchanged": True,
            "actual_ssa_count_interval_guard_revalidated_at_calls": True,
            "depth_only_branch_stopped": not result["accepted"],
            "G2_to_G5": "open",
            "A07_entire_limitation_closed": False,
            "next_action": progress["next_action"],
        },
    )
    files = {
        str(path.relative_to(ROOT)): digest(path) for path in output.rglob("*") if path.is_file()
    }
    save(output / "manifest.json", {"files": files, "frozen_inputs": frozen})
    print(
        json.dumps(
            {
                "passed": True,
                "adopted": result["accepted"],
                "new_tests": len(leaf_names | integration_names),
                "new_replays": replay_count,
                "output": str(output.relative_to(ROOT)),
            }
        ),
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    run(parser.parse_args().output)
