"""Verify and freeze completed local run receipts without repeating experiments."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from research.limitation_program_20261001.progress import ROOT


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def create(path, value):
    with path.open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(value, indent=2, allow_nan=False) + "\n")


def finalize(directory, test_xml=None, reports=()):
    directory = directory.resolve()
    summary, protocol = read(directory / "summary.json"), read(directory / "protocol.json")
    if not summary["passed"]:
        raise ValueError("failed experiment cannot be finalized as passed")
    dependencies = {str(Path(__file__).relative_to(ROOT)): sha(Path(__file__))}
    if "executed_dependencies" in protocol:
        for frozen in protocol["executed_dependencies"]:
            if sha(directory / frozen["snapshot"]) != frozen["sha256"]:
                raise ValueError("executed snapshot changed")
    else:
        checks = (
            ("executed_compact_parallel.py", "implementation_sha256"),
            ("executed_experiment_compact_parallel.py", "producer_sha256"),
        )
        for filename, field in checks:
            if sha(directory / filename) != protocol[field]:
                raise ValueError("executed snapshot disagrees with prospective protocol")
        review = read(directory / "independent_review.json")
        if not review["passed"] or review["validated_trial_count"] != 8:
            raise ValueError("independent compact schedule review failed")
    replay_count = 0
    for case in summary["cases"]:
        for replay in case["replays"]:
            if not replay["passed"] or replay["expected"] != replay["actual"]["values"]:
                raise ValueError("saved gate replay did not match expected outputs")
            if not replay["actual"]["all_input_and_workspace_bits_restored"]:
                raise ValueError("saved gate replay failed cleanup")
            replay_count += 1
        if case.get("accepted"):
            if not case["replay_passed"] or not case["replays"]:
                raise ValueError("accepted case has no replay evidence")
            path = directory / case["case"]
            schedule = read(path / "schedule_capped.json")
            if schedule["resources"] != case["candidate"]:
                raise ValueError("saved accepted schedule differs from summary")
    tests = None
    if test_xml:
        test_xml = test_xml.resolve()
        root = ET.parse(test_xml).getroot()
        suites = [root] if root.tag == "testsuite" else list(root.iter("testsuite"))
        tests = {
            field: sum(int(s.attrib.get(field, 0)) for s in suites)
            for field in ("tests", "errors", "failures", "skipped")
        }
        if not tests["tests"] or tests["errors"] or tests["failures"]:
            raise ValueError("test receipt is empty or failed")
        tests.update(xml=str(test_xml.relative_to(ROOT)), sha256=sha(test_xml))
        dependencies[str(test_xml.relative_to(ROOT))] = sha(test_xml)
    for report in reports:
        report = report.resolve()
        dependencies[str(report.relative_to(ROOT))] = sha(report)
    create(
        directory / "final_verification.json",
        dict(
            passed=True,
            accepted=summary["accepted"],
            verified_utc=datetime.now(timezone.utc).isoformat(),
            complete_gate_replay_receipts=replay_count,
            regression=tests,
            executed_snapshots_match_prospective_protocol=True,
            scope="Exact digital-source gates and saved logical-resource receipts. "
            "Structural proofs extend beyond the finite replay samples; this is not "
            "a continuous financial error or physical runtime certificate.",
            local_only=True,
        ),
    )
    with (directory / "NEXT.md").open("x", encoding="utf-8") as handle:
        handle.write(
            "# Next local action\n\nUse the current progress ledger to select "
            "the next bounded experiment. Retain only verified complete-source "
            "improvements and reconcile their costs. G2–G5 remain open; no "
            "financial error, estimator, classical timing or physical advantage "
            "claim follows from this arithmetic result.\n"
        )
    files = {
        str(path.relative_to(ROOT)): sha(path)
        for path in sorted(directory.rglob("*"))
        if path.is_file() and path.name != "manifest.json"
    }
    create(
        directory / "manifest.json",
        dict(
            files=files,
            frozen_inputs=dependencies,
            manifest_self_hash_excluded=True,
            historical_receipts_unchanged=True,
        ),
    )
    if any(sha(ROOT / path) != value for path, value in {**files, **dependencies}.items()):
        raise ValueError("receipt changed while being frozen")
    print(
        directory.name,
        "verified",
        replay_count,
        "gate replay receipts;",
        len(files),
        "artifact hashes",
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--test-xml", type=Path)
    parser.add_argument("--report", action="append", type=Path, default=[])
    args = parser.parse_args()
    finalize(args.directory, args.test_xml, args.report)
