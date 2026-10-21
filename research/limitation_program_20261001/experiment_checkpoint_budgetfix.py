"""Freeze and run tiny future budget fixtures without another financial attempt."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
RESULTS = ROOT / "results/limitation_program_20261001"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def create(path, data):
    with path.open("x", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, allow_nan=False)
        handle.write("\n")


def run(directory):
    directory = directory.resolve()
    directory.mkdir(parents=True, exist_ok=False)
    snapshot_directory = directory / "executed"
    snapshot_directory.mkdir()
    dependencies = [
        Path(__file__).resolve(),
        RESEARCH / "checkpoint_scheduler.py",
        RESEARCH / "checkpoint_scheduler_v2.py",
        RESEARCH / "test_checkpoint_scheduler_v2.py",
    ]
    frozen_inputs = {str(path.relative_to(ROOT)): sha(path) for path in dependencies}
    for name in ("block-checkpointing-75", "cost-aware-75"):
        path = RESULTS / "A18_run001" / name / "plan.json"
        frozen_inputs[str(path.relative_to(ROOT))] = sha(path)
    snapshots = []
    for path in dependencies:
        snapshot = snapshot_directory / path.name
        snapshot.write_bytes(path.read_bytes())
        snapshots.append(
            dict(
                original=str(path.relative_to(ROOT)),
                snapshot=str(snapshot.relative_to(directory)),
                sha256=sha(snapshot),
            )
        )
    create(
        directory / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            item="Future A18 scheduler exact global budget accounting",
            local_only=True,
            fixture_only=True,
            before_meaningful_test_execution=True,
            financial_candidate_attempts=0,
            complete_financial_replays=0,
            executed_dependencies=snapshots,
            declared_tests=10,
            event_budget_fixtures=[0, 1, 2, 5, 17, 40],
            other_fixtures=[
                "nested eviction bypasses ordinary failure catches",
                "paid invocation budget checked before append",
                "CPU limit admits no event",
                "terminal budget exception has distinct type",
            ],
            future_disposition="Keep the original four A18 candidate attempts unchanged. "
            "The v2 scheduler is tested only on tiny synthetic fixtures and is not "
            "applied to the frozen financial subgraph in this wave.",
            historical_deviation="The failed v1 cost-aware attempt recorded100013 "
            "tick checks against a100000 bound:100000 admitted checks and13 "
            "over-limit abort checks during exception unwinding. Its receipt is "
            "preserved and no new candidate rerun is authorized here.",
        ),
    )
    xml_path = directory / "pytest.xml"
    completed = subprocess.run(
        [
            str(ROOT / ".context/frontier_t0_env/Scripts/python.exe"),
            "-m",
            "pytest",
            "-q",
            str(RESEARCH / "test_checkpoint_scheduler_v2.py"),
            f"--junitxml={xml_path}",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    (directory / "pytest_stdout.txt").write_text(completed.stdout, encoding="utf-8")
    (directory / "pytest_stderr.txt").write_text(completed.stderr, encoding="utf-8")
    xml = ET.parse(xml_path).getroot()
    suites = [xml] if xml.tag == "testsuite" else list(xml.iter("testsuite"))
    tests = {
        field: sum(int(suite.attrib.get(field, 0)) for suite in suites)
        for field in ("tests", "failures", "errors", "skipped")
    }
    unchanged = all(sha(ROOT / path) == expected for path, expected in frozen_inputs.items())
    passed = (
        completed.returncode == 0
        and tests["tests"] == 10
        and not tests["failures"]
        and not tests["errors"]
        and not tests["skipped"]
        and unchanged
    )
    create(
        directory / "summary.json",
        dict(
            passed=passed,
            local_only=True,
            tests=tests,
            returncode=completed.returncode,
            frozen_inputs_unchanged=unchanged,
            future_scheduler_only=True,
            financial_candidate_attempts=0,
            complete_financial_replays=0,
            claim="Tiny fixtures establish exact budget accounting and terminal "
            "propagation; they supply no additional financial candidate or pricing evidence.",
        ),
    )
    files = {
        str(path.relative_to(ROOT)): sha(path)
        for path in sorted(directory.rglob("*"))
        if path.is_file()
    }
    create(
        directory / "manifest.json",
        dict(
            files=files,
            frozen_inputs=frozen_inputs,
            manifest_self_hash_excluded=True,
            historical_receipts_unchanged=True,
        ),
    )
    print(
        json.dumps(
            dict(passed=passed, tests=tests, directory=str(directory.relative_to(ROOT))), indent=2
        )
    )
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=RESULTS / "A18_budgetfix_run001")
    run(parser.parse_args().output)
