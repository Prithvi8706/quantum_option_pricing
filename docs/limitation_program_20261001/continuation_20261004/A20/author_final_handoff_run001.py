"""Finalize documentation only after an explicitly hashed root outcome notification.

No scientific imports or experiment execution. The root outcome file has schema
`a20-root-handoff-outcome-v1`, `notified_by_root: true`, an `outcome` in PASS,
FAILED or INCOMPLETE, `execution_summary` text, and `evidence_sha256` containing
actual ROOT-relative evidence file paths and SHA256 values. A PASS also needs
`producer_complete`, `audit_complete` and `full_fresh_integrity_complete` true.
No final document is written if notification is missing or a check fails.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
SHA = re.compile(r"[0-9a-f]{64}\Z")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root-outcome", required=True)
    parser.add_argument("--root-outcome-sha256", required=True)
    args = parser.parse_args()
    require(Path.cwd().resolve() == ROOT, "Fixed workspace")
    path = Path(args.root_outcome).resolve(strict=True)
    require(path.is_relative_to(ROOT), "Local root notification")
    require(SHA.fullmatch(args.root_outcome_sha256) is not None
            and digest(path) == args.root_outcome_sha256, "Actual notified root outcome bytes")
    notification = json.loads(path.read_text(encoding="utf-8"))
    require(notification["schema"] == "a20-root-handoff-outcome-v1"
            and notification["notified_by_root"] is True, "Explicit root outcome notification")
    outcome = notification["outcome"]
    require(outcome in ("PASS", "FAILED", "INCOMPLETE"), "Fixed terminal reporting status")
    require(isinstance(notification["execution_summary"], str)
            and notification["execution_summary"].strip(), "Concrete root execution summary")
    evidence = notification["evidence_sha256"]
    require(type(evidence) is dict and evidence, "Actual execution evidence pins")
    for key, expected in evidence.items():
        require(isinstance(key, str) and isinstance(expected, str)
                and SHA.fullmatch(expected) is not None, "Typed evidence expectations")
        item = (ROOT / key).resolve(strict=True)
        require(item.is_relative_to(ROOT) and item.relative_to(ROOT).as_posix() == key,
                "Canonical local evidence path")
        require(digest(item) == expected, "Actual execution evidence SHA")
    if outcome == "PASS":
        require(all(notification.get(field) is True for field in
                    ("producer_complete", "audit_complete", "full_fresh_integrity_complete")),
                "Root reports complete producer, independent audit and full fresh integrity")
        for role in ("producer", "audit"):
            directory = ROOT / f"results/limitation_program_20261001/A20_continuation_20261004_{role}_run004"
            manifest = directory / "manifest.json"
            require(manifest.relative_to(ROOT).as_posix() in evidence,
                    "Both actual complete manifest bytes are pinned")
            require(not any((directory / name).exists() for name in
                            ("FAILED_UNSEALED.json", "failed_unsealed.json", "failure.json",
                             "run_failure.json", "prepare_failure.json")),
                    "No failed or unsealed component release")
            record = json.loads(manifest.read_text(encoding="utf-8"))
            require(record.get("role") == role and record.get("passed") is True
                    and record.get("completed") is True and record.get("budget_censored") is False,
                    "Actual complete uncensored role manifest")
    draft = HERE / "HANDOFF_DRAFT_run001.md"
    source = draft.read_text(encoding="utf-8")
    require(source.count("<!-- ROOT_EXECUTION_OUTCOME -->") == 1, "Single preserved draft insertion")
    block = (
        "Root-notified execution outcome: **" + outcome + "**.\n\n"
        + notification["execution_summary"].strip() + "\n\n"
        + "Notification: `" + path.relative_to(ROOT).as_posix() + "`, SHA `"
        + args.root_outcome_sha256 + "`. Documentation authoring verified the listed evidence bytes; "
        + "root's separately pinned integrity receipt owns complete live/owned/external map validation. "
        + "No scientific rerun or independent full integrity replay occurred here.\n\n"
        + "Evidence pins:\n\n" + "\n".join("- `" + key + "`: `" + value + "`"
                                              for key, value in sorted(evidence.items()))
    )
    final = source.replace("# A20 continuation handoff draft", "# A20 continuation handoff", 1)
    final = final.replace(
        "Execution outcome: **PENDING_ROOT_NOTIFICATION**. This draft records prospective scope and retained history. "
        "It does not declare a producer, auditor or component PASS. Root is running the fixed V6 release and will "
        "supply the execution and fresh integrity outcomes separately.",
        "Execution outcome is documented from root's actual notification and evidence below. "
        "A20 remains partial; the restricted component's outcome does not establish a complete pricing-source result.", 1)
    final = final.replace("<!-- ROOT_EXECUTION_OUTCOME -->", block)
    final = final.replace("Their terminal results remain pending in this draft.",
                          "Their terminal results are the root-notified evidence above.", 1)
    require(len(final.encode("utf-8")) <= 2**20, "Bounded documentation output")
    target = HERE / "HANDOFF_run001.md"
    receipt = HERE / "HANDOFF_AUTHOR_RECEIPT_run001.json"
    require(not target.exists() and not receipt.exists(), "Fresh final handoff files")
    with target.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(final)
    metadata = {
        "schema": "a20-final-handoff-document-author-v1", "scientific_execution": False,
        "root_reported_outcome": outcome, "root_notification": path.relative_to(ROOT).as_posix(),
        "root_notification_sha256": args.root_outcome_sha256, "draft_sha256": digest(draft),
        "author_script_sha256": digest(Path(__file__)), "evidence_sha256": evidence,
        "final_handoff_sha256": digest(target), "complete_integrity_replayed_by_author": False,
        "A20_status": "partial", "new_financial_fixture_credit": 0, "new_gate_fixture_credit": 0,
        "full_G2": False, "adoption": False, "quantum_advantage": False,
    }
    with receipt.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"final_handoff": target.relative_to(ROOT).as_posix(),
                      "sha256": digest(target), "scientific_execution": False}))


if __name__ == "__main__":
    main()
