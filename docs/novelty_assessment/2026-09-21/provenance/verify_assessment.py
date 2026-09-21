"""Read-only documentation, receipt-binding and frozen-history delivery checks."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote
import xml.etree.ElementTree as ET


HERE = Path(__file__).resolve().parent
BASE = HERE.parent
ROOT = HERE.parents[3]
TAKEOVER = "49b8f0a5a1394198b98e20b6e091f86a5f1ad532"
LOCAL_MAIN = "103ddfd1391e3e9800a0cf73b552be10fe3aa01f"
REMOTE_MAIN = "da3080d19a8f746cab31bbee157a5d591c6b56fb"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def verify(require_pushed=False):
    required = (
        "PROJECT_STATE SEARCH_LOG PRIMARY_SOURCE_BIBLIOGRAPHY NEAREST_PRIOR_ART_MATRIX "
        "CLAIM_BY_CLAIM_ASSESSMENT MATHEMATICAL_AUDIT COMPARATOR_FAIRNESS_AUDIT "
        "REFEREE_REPORT PUBLICATION_DECISION BOUNDED_FOLLOWUP_PLAN HUMAN_EXPERT_PACKET "
        "REVIEW_RECORD BRANCH_CONSOLIDATION MAIN_BATCH_PLAN"
    ).split()
    assert all((BASE / (name + ".md")).is_file() for name in required)
    documents = sorted(BASE.rglob("*.md")) + [
        ROOT / "README.md", ROOT / "checklist_17.9.26.md",
        ROOT / "docs/journal_sprint/PROJECT_LOG.md",
    ]
    links = 0
    for document in documents:
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", document.read_text(encoding="utf-8")):
            if target.startswith(("https:", "http:", "mailto:", "#")):
                continue
            target = unquote(target.split("#")[0].split("?")[0].strip("<>"))
            assert (document.parent / target).exists(), (document, target)
            links += 1

    bindings = 0
    # Old v1 is bound to its historical committed source; v2 to the reviewed source now.
    for name, historical in [("label_bridge_v1.json", "5f96b9ec"),
                             ("label_bridge_v2.json", None)]:
        receipt = read(HERE / name)
        for path, expected in receipt["source_hashes"].items():
            data = (subprocess.check_output(["git", "show", f"{historical}:{path}"], cwd=ROOT)
                    if historical else (ROOT / path).read_bytes())
            assert hashlib.sha256(data).hexdigest() == expected, (name, path)
            bindings += 1
        for path, expected in receipt["input_hashes"].items():
            assert sha(ROOT / path) == expected, (name, path)
            bindings += 1
        assert receipt["labels_checked"] == 384 and len(receipt["rows"]) == 18
        assert receipt["all_schedules_unchanged"]
        assert not receipt["physical_errors_certified"] and not receipt["confirmation_admitted"]

    math = read(BASE / "reviews/math/independent_checks.json")
    for path, expected in math["input_sha256"].items():
        assert sha(ROOT / path) == expected, path
        bindings += 1
    assert sha(BASE / "reviews/math/check_certificates.py") == math["script_sha256"]
    assert sha(BASE / "reviews/math/PROTOCOL.md") == math["protocol_sha256"]
    assert math["passed"] and math["certificate_rows_checked"] == 18 and math["node_count"] == 1332
    resources = read(BASE / "reviews/resources/archived_resource_check.json")
    resource_script = BASE / "reviews/resources/check_archived_resources.py"
    assert sha(resource_script) == resources["checker_sha256"]
    assert resources["passed"] and resources["cx_ledgers_checked"] == 332
    bindings += 3

    selected = resources["selected"]
    expected_selected = {
        "D1": (36469403102, 55, 104719289723, 4733),
        "D2": (1101392680835, 103, 375312500844, 5162),
    }
    state = (BASE / "PROJECT_STATE.md").read_text(encoding="utf-8")
    for case, expected in expected_selected.items():
        row = selected[case]
        actual = (row["reflection"]["control_cancelled_cx"], row["reflection"]["total_qubits"],
                  row["residual"]["control_cancelled_cx"], row["residual"]["total_qubits"])
        assert actual == expected
        assert all(f"{n:,}" in state for n in expected)
    assert resources["primary_rows_checked"] == 148 and resources["residual_rows_checked"] == 18

    tests = ET.parse(HERE / "label_bridge_tests.xml")
    assert len(tests.findall(".//testcase")) == 19
    assert not tests.findall(".//failure") and not tests.findall(".//error")
    assert not tests.findall(".//skipped")
    frozen_changes = git("diff", TAKEOVER, "--name-status", "--diff-filter=DMRT", "--",
                         "research", "results", "tests", "docs/release")
    assert not frozen_changes, frozen_changes
    old_tips = read(HERE / "initial_refs.json")
    for tip in {row["sha"] for row in old_tips}:
        subprocess.run(["git", "merge-base", "--is-ancestor", tip, "dev"], cwd=ROOT, check=True)
    local = dict(line.split() for line in git(
        "for-each-ref", "--format=%(refname) %(objectname)", "refs/heads").splitlines())
    remote = {line.split()[1]: line.split()[0]
              for line in git("ls-remote", "--heads", "origin").splitlines()}
    assert set(local) == set(remote) == {"refs/heads/main", "refs/heads/dev"}
    assert local["refs/heads/main"] == LOCAL_MAIN and remote["refs/heads/main"] == REMOTE_MAIN
    head = git("rev-parse", "HEAD")
    assert local["refs/heads/dev"] == head
    if require_pushed:
        assert remote["refs/heads/dev"] == head
    assert git("rev-parse", "refs/stash") == "d20fdc626c8bf823505281402f1004071f9ed38f"
    assert git("rev-parse", "refs/original/refs/heads/main") == (
        "145dafc40a1c2ad1909d7adcb473cc750b87c314"
    )
    preservation = read(HERE / "preservation_verification.json")
    assert preservation["all_matched"]
    assert preservation["original_files_matched_to_git_index"] == 13783
    return {
        "date": "2026-09-21", "checked_head": head,
        "required_assessment_documents": len(required),
        "markdown_documents_checked": len(documents),
        "local_link_targets_checked": links, "receipt_source_input_hashes_checked": bindings,
        "new_and_existing_decoder_tests_passed": 19, "frozen_tracked_files_unchanged": True,
        "initial_branch_tips_reachable_from_dev": True,
        "local_branches": local, "remote_branches": remote,
        "dev_remote_equals_local": remote["refs/heads/dev"] == head,
        "main_unchanged": True,
        "document_sha256": {p.relative_to(ROOT).as_posix(): sha(p) for p in documents},
        "checker_sha256": sha(Path(__file__)), "passed": True,
        "scope": "Consistency/delivery checks; no new pricing data or external-link validation.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--require-pushed", action="store_true")
    args = parser.parse_args()
    report = verify(args.require_pushed)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2)
        stream.write("\n")
    print(json.dumps({k: v for k, v in report.items() if k != "document_sha256"}, indent=2))


if __name__ == "__main__":
    main()
