"""Local metadata recovery for the failed paired-loader registration, with no reruns.

This NEW invocation has prospective CPU300/admission270/wall900 bounds. It verifies
immutable receipts and their actual XML identities, proves the exact old authorized
before-to-after metadata change, and classifies that bookkeeping failure without
adding fixture credit again. Scientific modules, tests and proof code are not imported.
"""

from __future__ import annotations

import time

import argparse
import copy
import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import traceback
import xml.etree.ElementTree as ET

ROOT = Path("C:/Users/prith/quantum_option_pricing").resolve()
PROGRAM = ROOT / "results/limitation_program_20261001"
RESEARCH = ROOT / "research/limitation_program_20261001"
PYTHON = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
PRODUCER = PROGRAM / "A02_two_draw_loader_resource_run002"
AUDIT = PROGRAM / "A02_two_draw_loader_resource_audit_run002"
VERIFICATION = PROGRAM / "A02_two_draw_root_verification_run002"
FAILED = PROGRAM / "A02_two_draw_root_registration_run002"
DIAGNOSTIC = PROGRAM / "A02_two_draw_registration_failure_run002"
OUTPUT = PROGRAM / "A02_two_draw_registration_recovery_run001"
READY = PROGRAM / "A02_two_draw_verifier_READY_run002.json"
PROGRESS = PROGRAM / "progress.json"
STATUS = ROOT / "docs/limitation_program_20261001/STATUS.md"
PREFLIGHT = RESEARCH / "two_draw_registration_recovery_preflight.json"
PREFLIGHT_MD = RESEARCH / "TWO_DRAW_REGISTRATION_RECOVERY_PREFLIGHT.md"
CPU, ADMISSION_CPU, WALL, ADMISSION_WALL = 300, 270, 900, 840
MAX_REFERENCES, MAX_BYTES = 100_000, 8 * 1024**3
MAX_JSON, MAX_OWN = 32 * 1024**2, 512
SHA = re.compile(r"[0-9a-f]{64}\Z")
LABELS = ("AS241_two_actual_scalar_invocations", "BoxMuller_one_actual_shared_pair")
PINS = {
    "verification": "fe2badc38a00d7c3ccb15a122c18d39eca86576cd914e2b5ca0703d7a1dde0c2",
    "diagnostic": "33acc75e62f1ec24d91201fe83f6fdba8f88da75d7ebfc745e366856df661ffd",
    "producer": "b001ce2c3d4ec126241115d96207a213c335abff4b1748ae0bef8d7a9c9002a1",
    "audit": "45fb8eeef1b41756aa0cdd5efcdd634f574f4b68ab10b21863bab88423ffbb6d",
    "ready": "897a4b561f22bb2999ff6febf9a89c9a67b201e8d68382d47fceb7cef67889bc",
    "old_verifier": "f841b337db37adb2e0a359503938d8894607e3af6bb7ac3fb08e31c962fa70de",
    "wave10": "2a04693db9c76acdd5dd038248ee7a9dcaf2f32e4ce1dd9c325dc96ccd4a1320",
    "mps": "bfe81ce4277ea6d4301c6529cf230cb5936f5e5005cca33a2aafcdc2270cece1",
}
FAILED_NAMES = {
    "FAILED_UNSEALED.json",
    "failure.json",
    "progress_after.json",
    "progress_before.json",
    "progress_update_completed.json",
    "root_READY_snapshot.json",
    "STATUS_after.md",
    "STATUS_before.md",
    "status_update_completed.json",
    "summary.json",
    "verify_two_draw_loader_receipts.py",
}
DIAGNOSTIC_NAMES = {"progress_observed.json", "STATUS_observed.md", "summary.json"}
PATHS = {}
KEY_SPELLINGS = {}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def fingerprint(path):
    stat = path.stat()
    return (
        stat.st_dev,
        stat.st_ino,
        stat.st_size,
        stat.st_mtime_ns,
        stat.st_ctime_ns,
        getattr(stat, "st_file_attributes", None),
        getattr(stat, "st_reparse_tag", None),
    )


class Guard:
    def __init__(self):
        require(os.name == "nt", "This prospective recovery is pinned to the local Windows host")
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.GetCurrentProcess.argtypes = []
        kernel.GetCurrentProcess.restype = wintypes.HANDLE
        kernel.GetProcessTimes.argtypes = [wintypes.HANDLE] + [
            ctypes.POINTER(wintypes.FILETIME)
        ] * 4
        kernel.GetProcessTimes.restype = wintypes.BOOL
        fields = [wintypes.FILETIME() for _ in range(4)]
        require(
            kernel.GetProcessTimes(kernel.GetCurrentProcess(), *(ctypes.byref(f) for f in fields)),
            "Actual process creation time unavailable",
        )
        creation = ((fields[0].dwHighDateTime << 32) | fields[0].dwLowDateTime) / 10_000_000
        creation -= 11_644_473_600
        self.wall_start = time.monotonic() - max(0.0, time.time() - creation)
        self.hashes = {}
        self.hashed_bytes = 0
        self.jsons = {}
        self.external_runtime = []

    def check(self, *, terminal=False):
        cpu, wall = (CPU, WALL) if terminal else (ADMISSION_CPU, ADMISSION_WALL)
        require(time.process_time() < cpu, "Recovery process CPU budget exhausted")
        require(time.monotonic() - self.wall_start < wall, "Recovery process wall budget exhausted")


def canonical(name, *, exists=True, fresh=False):
    path = Path(name)
    if not path.is_absolute():
        require(
            isinstance(name, str) and not path.drive and "\\" not in name,
            "Canonical ROOT-relative POSIX key required",
        )
        require(path.as_posix() == name, "Noncanonical lexical ROOT-relative key")
        path = ROOT / path
    lexical = str(path)
    if not fresh and lexical in PATHS:
        return PATHS[lexical]
    resolved = path.resolve(strict=exists)
    resolved.relative_to(ROOT)
    require(path == resolved, "Symlink or alias path rejected")
    if fresh and lexical in PATHS:
        require(PATHS[lexical] == resolved, "Previously confined path changed")
    PATHS[lexical] = resolved
    return resolved


def key(path):
    return canonical(path).relative_to(ROOT).as_posix()


def bytes_read(path, guard, *, terminal=False):
    guard.check(terminal=terminal)
    path = canonical(path)
    before = fingerprint(path)
    require(before[2] <= MAX_JSON, "Metadata byte bound exceeded")
    blocks = []
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            guard.check(terminal=terminal)
            blocks.append(block)
    require(fingerprint(path) == before, "Metadata changed during read")
    data = b"".join(blocks)
    guard.check(terminal=terminal)
    require(len(data) <= MAX_JSON, "Metadata byte bound exceeded")
    return data


def read_json(path, guard):
    path = canonical(path)
    before = fingerprint(path)
    cached = guard.jsons.get(str(path))
    if cached is not None and cached[0] == before:
        guard.check()
        return cached[1]
    data = bytes_read(path, guard)
    value = json.loads(data)
    guard.check()
    require(fingerprint(path) == before, "JSON changed during decode")
    guard.jsons[str(path)] = (before, value)
    return value


def digest(path, guard, *, fresh=False, terminal=False):
    guard.check(terminal=terminal)
    path = canonical(path, fresh=fresh)
    before = fingerprint(path)
    cached = guard.hashes.get(str(path))
    if not fresh and cached is not None and cached[0] == before:
        return cached[1]
    result = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            guard.hashed_bytes += len(block)
            require(guard.hashed_bytes <= MAX_BYTES * 3, "Complete hash-work byte bound exceeded")
            result.update(block)
            guard.check(terminal=terminal)
    require(fingerprint(path) == before, "File changed while hashing: " + str(path))
    actual = result.hexdigest()
    guard.hashes[str(path)] = (before, actual)
    return actual


def merge(mapping, name, expected):
    require(
        isinstance(name, str) and not Path(name).is_absolute(), "ROOT-relative map key required"
    )
    require(isinstance(expected, str) and SHA.fullmatch(expected), "Explicit SHA256 required")
    require(key(canonical(name)) == name, "Canonical ROOT-relative map key required")
    require(
        name.casefold() not in KEY_SPELLINGS or KEY_SPELLINGS[name.casefold()] == name,
        "Windows case alias of a canonical key rejected",
    )
    KEY_SPELLINGS[name.casefold()] = name
    require(
        name not in mapping or mapping[name] == expected, "Conflicting equal-path SHA expectations"
    )
    mapping[name] = expected
    require(len(mapping) <= MAX_REFERENCES, "Complete reference cap exceeded")


def owned_inventory(directory, guard):
    actual = set()
    for parent, folders, files in os.walk(directory, followlinks=False):
        guard.check()
        for folder in folders:
            canonical(Path(parent) / folder, fresh=True)
        for name in files:
            path = canonical(Path(parent) / name, fresh=True)
            if path != directory / "manifest.json":
                actual.add(key(path))
                require(len(actual) <= MAX_OWN, "Actual receipt own-file cap exceeded")
    return actual


def receipt(directory, wanted, guard, frozen, *, failed_diagnostic=False):
    directory = canonical(directory)
    manifest_path = directory / "manifest.json"
    require(digest(manifest_path, guard) == wanted, "Pinned receipt manifest differs")
    manifest = read_json(manifest_path, guard)
    require(set(manifest) >= {"files", "frozen_inputs"}, "Recognized files/frozen_inputs required")
    require(manifest.get("manifest_self_hash_excluded") is True, "Self-hash convention differs")
    require(
        all(
            not isinstance(v, dict) or n in ("files", "frozen_inputs") for n, v in manifest.items()
        ),
        "Unknown manifest maps cannot be omitted",
    )
    owned, local = {}, {}
    for field in ("files", "frozen_inputs"):
        require(isinstance(manifest[field], dict), "Manifest map must be a dictionary")
        for name, expected in manifest[field].items():
            guard.check()
            merge(local, name, expected)
            if field == "files":
                require(canonical(name).is_relative_to(directory), "Owned path escaped receipt")
                merge(owned, name, expected)
    require(len(owned) <= MAX_OWN, "Declared own-file cap exceeded")
    require(owned_inventory(directory, guard) == set(owned), "Exact own-file inventory differs")
    byte_count = 0
    for name, expected in local.items():
        path = canonical(name)
        byte_count += path.stat().st_size
        require(byte_count <= MAX_BYTES, "Receipt byte union exceeded")
        require(digest(path, guard) == expected, "Actual owned/frozen SHA differs: " + name)
        merge(frozen, name, expected)
    merge(frozen, key(manifest_path), wanted)
    terminal = directory / "summary.json"
    require(key(terminal) in owned, "Terminal summary must be owned")
    require(
        manifest.get("terminal_record", key(terminal)) == key(terminal), "Terminal pointer differs"
    )
    summary = read_json(terminal, guard)
    if failed_diagnostic:
        require(summary.get("passed") is False, "Failure diagnostic cannot become success")
    else:
        require(
            summary.get("passed") is True and summary.get("budget_censored") is False,
            "Complete uncensored sealed PASS required",
        )
        for marker in (
            "FAILED_UNSEALED.json",
            "failed_unsealed.json",
            "failure_retention_unsealed.json",
            "failure.json",
            "run_failure.json",
            "prepare_failure.json",
            "completion_outcome.json",
        ):
            require(
                not (directory / marker).exists(), "Authoritative failure evidence blocks admission"
            )
        for flag in (
            "failed",
            "failed_unsealed",
            "prepare_failed",
            "run_failed",
            "integrity_not_certified",
        ):
            require(
                flag not in summary or summary[flag] is False,
                "Terminal failure flag blocks admission",
            )
    protocol = (
        read_json(directory / "protocol.json", guard)
        if (directory / "protocol.json").exists()
        else {}
    )
    if "frozen_inputs" in protocol:
        require(
            protocol["frozen_inputs"] == manifest["frozen_inputs"], "Protocol frozen map differs"
        )
    return manifest, summary, protocol


def xml_cases(path, guard):
    data = bytes_read(path, guard)
    root = ET.fromstring(data)
    require(root.tag in ("testsuite", "testsuites"), "Unknown JUnit root")
    rows = list(root.iter("testcase"))
    identities = [(row.get("classname", ""), row.get("name", "")) for row in rows]
    require(
        all(c and n for c, n in identities) and len(set(identities)) == len(identities),
        "Unnamed or duplicate actual XML identity",
    )
    require(
        not any(row.find(t) is not None for row in rows for t in ("failure", "error", "skipped")),
        "Actual XML defect prohibits fixture admission",
    )
    suites = [suite for suite in root.iter("testsuite") if suite.findall("testcase")]
    require(
        sum(int(s.get("tests", 0)) for s in suites) == len(rows), "JUnit tests declaration differs"
    )
    require(
        all(int(s.get(f, 0)) == 0 for s in suites for f in ("failures", "errors", "skipped")),
        "JUnit declared defects prohibit fixture admission",
    )
    guard.check()
    return set(identities)


def prior_cases(guard, frozen):
    identities = set()
    for owner, pin in (("WAVE10_run002", PINS["wave10"]), ("A04_mps_u_bridge_run001", PINS["mps"])):
        directory = PROGRAM / owner
        manifest_path = directory / "manifest.json"
        require(digest(manifest_path, guard) == pin, "Prior released manifest differs")
        merge(frozen, key(manifest_path), pin)
        manifest = read_json(manifest_path, guard)
        names = (
            ("historical_identity_reconciliation.json", "test_case_credit.json")
            if owner.startswith("WAVE")
            else ("tests.xml",)
        )
        for name in names:
            path = directory / name
            expected = manifest["files"][key(path)]
            require(digest(path, guard) == expected, "Prior owned identity evidence differs")
            merge(frozen, key(path), expected)
            if name.endswith(".xml"):
                identities.update(xml_cases(path, guard))
            else:
                field = "cases" if name.startswith("historical") else "credited_cases"
                evidence = read_json(path, guard)
                if name.startswith("historical"):
                    require(
                        evidence["reported_historical_base_count"] == 1423
                        and evidence["available_actual_distinct_identity_count"] == 1377
                        and evidence["missing_reported_identity_count"] == 46
                        and evidence["complete_historical_identity_ledger_available"] is False,
                        "The actual46 historical identity gap must remain explicit",
                    )
                else:
                    require(
                        evidence["actual_distinct_new_identities_among_available_evidence"] == 325
                        and evidence[
                            "historical_missing_identities_prevent_unqualified_cumulative_distinct_claim"
                        ]
                        is True,
                        "WAVE10 available new identity credit differs",
                    )
                for packet in evidence["packets"].values():
                    identities.update(tuple(row) for row in packet.get(field, []))
    require(len(identities) == 1708, "Released available historical identity count differs")
    return identities


def verify_scientific_metadata(guard, frozen):
    _, verified, _ = receipt(VERIFICATION, PINS["verification"], guard, frozen)
    require(
        verified["safe_to_register_progress"] is True and verified["new_test_credit"] == 0,
        "Sealed root verification must be safe and zero new science credit",
    )
    require(
        verified["numerical_imports_tests_replays_proof_evaluations"] == 0,
        "Previous root verification must remain metadata-only",
    )
    require(
        verified["mutable_progress_or_status_in_frozen_input_map"] is False,
        "Previous root verification must not bind mutable metadata",
    )
    pair = verified["pair"]
    require(
        pair["outcome"] == "passed_cost_rejected_audited"
        and pair["producer_fixture_credit"] == 32
        and pair["audit_fixture_credit"] == 0
        and pair["component_preferred"] is False
        and pair["strict_T_improvement"] is False
        and pair["financial_source_adopted"] is False
        and pair["quantum_advantage_established"] is False,
        "Verified paired final scope differs",
    )
    require(
        pair["historical_identity_gap"] == 46
        and pair["unqualified_cumulative_distinct_total"] is None
        and pair["available_prior_identity_count"] == 1708
        and pair["available_prior_plus_new_identities"] == 1740,
        "Qualified identity scope differs",
    )
    ready = read_json(READY, guard)
    require(digest(READY, guard) == PINS["ready"], "Frozen root registration authorization differs")
    merge(frozen, key(READY), PINS["ready"])
    require(
        ready["ready"] is True
        and ready["local_execution_authorized"] is True
        and ready["registration_authorized"] is True,
        "Original registration was not authorized",
    )
    require(
        ready["producer_receipt"] == key(PRODUCER) and ready["audit_receipt"] == key(AUDIT),
        "Original selected paired receipts differ",
    )
    require(
        ready["source_sha256"][key(RESEARCH / "verify_two_draw_loader_receipts.py")]
        == PINS["old_verifier"],
        "Frozen original verifier source pin differs",
    )
    for name, expected in ready["source_sha256"].items():
        require(digest(canonical(name), guard) == expected, "Frozen reviewed source differs")
        merge(frozen, name, expected)
    require(
        canonical(ready["tools"]["python"]["path"]) == PYTHON
        and digest(PYTHON, guard) == ready["tools"]["python"]["sha256"],
        "Pinned interpreter differs",
    )
    merge(frozen, key(PYTHON), ready["tools"]["python"]["sha256"])
    _, producer, pp = receipt(PRODUCER, PINS["producer"], guard, frozen)
    _, audit, ap = receipt(AUDIT, PINS["audit"], guard, frozen)
    require(
        pair["producer"]["summary"] == producer
        and pair["producer"]["protocol"] == pp
        and pair["producer"]["manifest_sha256"] == PINS["producer"],
        "Producer differs from root proof",
    )
    require(
        pair["audit"]["summary"] == audit
        and pair["audit"]["protocol"] == ap
        and pair["audit"]["manifest_sha256"] == PINS["audit"],
        "Independent audit differs from root proof",
    )
    require(
        (pp["process_CPU_seconds"], pp["admission_CPU_seconds"], pp["wall_seconds"])
        == (300, 240, 600)
        and (ap["process_CPU_seconds"], ap["admission_CPU_seconds"], ap["wall_seconds"])
        == (180, 150, 600),
        "Original scientific budgets differ",
    )
    preflight = read_json(PRODUCER / "two_draw_loader_implementation_preflight_v2.json", guard)
    require(
        preflight["fixed_fixture_count"] == pp["declared_unique_tests"] == 32
        and preflight["fixed_labels"] == pp["fixed_labels"] == list(LABELS)
        and preflight["input_pairs"] == pp["fixed_input_pairs"]
        and len(preflight["input_pairs"]) == 8
        and preflight["dirty_outputs_each72"] == pp["dirty_outputs_each72"]
        and len(preflight["dirty_outputs_each72"]) == 2,
        "Exact declared paired inventory differs",
    )
    identities = xml_cases(PRODUCER / "tests.xml", guard)
    wanted = {
        f"test_actual_complete_native_loader_and_literal_inverse[{label}-pair{p}-dirty{d}]"
        for label in LABELS
        for p in range(8)
        for d in range(2)
    }
    require(
        len(identities) == 32
        and {n for _, n in identities} == wanted
        and all(
            c == "test_two_draw_loader_source_v2" or c.endswith(".test_two_draw_loader_source_v2")
            for c, _ in identities
        ),
        "Actual32 XML identities differ from fixed declared tests",
    )
    require(
        identities == {tuple(row) for row in pair["identities"]},
        "Actual XML differs from sealed root proof",
    )
    credit = read_json(PRODUCER / "test_credit_reconciliation.json", guard)
    require(
        {tuple(row) for row in credit["test_identities"]} == identities
        and credit["unique_new_fixtures_passed"] == 32
        and credit["prior_fixture_counts_added_again"] == 0,
        "Producer credit reconciliation differs",
    )
    previous = prior_cases(guard, frozen)
    require(
        not previous.intersection(identities) and len(previous | identities) == 1740,
        "Actual identity union is duplicated or incomplete",
    )
    require(
        all(
            producer[f] == 32
            for f in (
                "tests_completed",
                "new_test_credit",
                "new_unique_fixtures_passed",
                "completed_actual_basis_fixtures",
            )
        )
        and producer["old_fixture_recredit"] == 0
        and producer["both_complete_dirty72_clean_ABI_validated"] is True,
        "Producer fixture admission differs",
    )
    require(
        producer["full_financial_sampler_or_estimator_adopted"] is False
        and producer["full_G2"] is False
        and producer["quantum_advantage_established"] is False
        and producer["full_financial_native_cost"] is None
        and producer["physical_runtime"] is None
        and producer["all_110_obligations_retained"] is True,
        "Producer cannot claim full financial adoption or advantage",
    )
    require(
        audit["new_test_credit"] == audit["old_fixture_recredit"] == 0
        and audit["producer_actual_tests_verified"]
        == audit["independent_native_reexecutions"]
        == 32
        and audit["independent_two_draw_resource_audit_passed"] is True
        and audit["component_AS241_adopted_under_strict_T_rule"] is False
        and audit["financial_source_adopted"] is False
        and audit["full_G2_established"] is False
        and audit["quantum_advantage_claim"] is False,
        "Audit scope, zero credit or rejection differs",
    )
    require(
        ap["source_receipt"] == key(PRODUCER)
        and ap["independent_native_reexecutions"] == 32
        and ap["unique_new_fixture_credit"] == 0,
        "Independent audit source or zero-credit protocol differs",
    )
    ledger = read_json(PRODUCER / "native_resource_ledger.json", guard)
    require(
        set(ledger) == set(LABELS)
        and ledger == read_json(AUDIT / "independent_native_resource_ledger.json", guard),
        "Saved exact independent resource rows differ",
    )
    for label in LABELS:
        require(
            type(ledger[label]["clean_resources"]["t_count"]) is int
            and ledger[label]["clean_resources"]["t_count"] >= 0,
            "Invalid exact resource integer",
        )
    require(
        not (
            ledger[LABELS[0]]["clean_resources"]["t_count"]
            < ledger[LABELS[1]]["clean_resources"]["t_count"]
        ),
        "Actual strict-T rejected outcome differs",
    )
    decision = read_json(PRODUCER / "paired_component_decision.json", guard)
    require(
        decision == producer["paired_component_decision"]
        and decision["AS241_component_strict_T_improvement"] is False
        and decision["paired_AS241_component_adopted"] is False,
        "Recorded strict-T decision differs",
    )
    require(
        not (PROGRAM / "A02_two_draw_loader_resource_run001").exists()
        and pair["original_paired_run001_absent"] is True,
        "Original pre-mkdir failed run must remain absent",
    )
    return pair, ready


def verify_failed_registration(guard, frozen):
    manifest, summary, _ = receipt(
        DIAGNOSTIC, PINS["diagnostic"], guard, frozen, failed_diagnostic=True
    )
    require(
        {Path(n).name for n in manifest["files"]} == DIAGNOSTIC_NAMES
        and len(manifest["files"]) == 3,
        "Diagnostic must own exactly its original3 files",
    )
    require(
        len(manifest["frozen_inputs"]) == 12,
        "Failure diagnostic must retain all original12 input bindings",
    )
    expected_failed = {key(FAILED / name) for name in FAILED_NAMES}
    require(
        set(manifest["frozen_inputs"]) == expected_failed | {key(VERIFICATION / "manifest.json")},
        "Diagnostic does not bind exactly old11 plus root verification",
    )
    require(
        not (FAILED / "manifest.json").exists()
        and owned_inventory(FAILED, guard) == expected_failed,
        "Failed registration must remain unsealed with exact original11 files",
    )
    require(
        summary["all11_partial_files_bound"] is True
        and summary["failed_receipt_unsealed"] is True
        and summary["new_scientific_test_credit"] == 0
        and summary["registration_count_not_added_again"] is True
        and summary["producer_auditor_and_root_verification_previously_sealed_PASS"] is True
        and summary["root_verification_manifest_sha256"] == PINS["verification"],
        "Failure diagnostic classification differs",
    )
    require(
        summary["failure_phase"] == "terminal fresh hashing after progress and STATUS writes"
        and summary["observed_live_progress_equal_failed_progress_after"] is True
        and summary["observed_live_STATUS_equal_failed_STATUS_after"] is True
        and summary["CPU_bookkeeping_censor_does_not_claim_science_failure"] is True,
        "Original root diagnostic must distinguish bookkeeping from scientific outcome",
    )
    marker = read_json(FAILED / "FAILED_UNSEALED.json", guard)
    failed = read_json(FAILED / "summary.json", guard)
    failure = read_json(FAILED / "failure.json", guard)
    require(
        marker["passed"] is False
        and marker["integrity_not_certified"] is True
        and marker["new_test_credit"] == 0
        and marker["metadata_may_have_partially_updated"] is True,
        "Original failed-unsealed marker remains authoritative",
    )
    require(
        failed["passed"] is False
        and failed["budget_censored"] is True
        and failed["safe_to_register_progress"] is False
        and failed["new_test_credit"] == 0,
        "Original registration cannot become a certified PASS",
    )
    require(
        failure["passed"] is False
        and failure["producer_fixture_credit"] == 0
        and "CPU budget exhausted" in failure["error"],
        "Original failure must remain bookkeeping CPU censor",
    )
    require(
        digest(FAILED / "verify_two_draw_loader_receipts.py", guard) == PINS["old_verifier"]
        and digest(FAILED / "root_READY_snapshot.json", guard) == PINS["ready"],
        "Original executed verifier/authorization bytes changed",
    )
    return summary


def encode(value, guard, *, terminal=False):
    guard.check(terminal=terminal)
    data = (json.dumps(value, indent=2, allow_nan=False) + "\n").encode("utf-8")
    guard.check(terminal=terminal)
    require(len(data) <= MAX_JSON, "Encoded metadata byte cap exceeded")
    return data


def write_new(path, data, guard, *, terminal=False):
    guard.check(terminal=terminal)
    require(len(data) <= MAX_JSON, "New metadata byte cap exceeded")
    with path.open("xb") as stream:
        for offset in range(0, len(data), 1 << 20):
            guard.check(terminal=terminal)
            stream.write(data[offset : offset + (1 << 20)])
        stream.flush()
        os.fsync(stream.fileno())
    guard.check(terminal=terminal)


def new_json(path, value, guard, *, terminal=False):
    write_new(path, encode(value, guard, terminal=terminal), guard, terminal=terminal)


def snapshot(path, destination, guard, frozen):
    data = bytes_read(path, guard)
    actual = hashlib.sha256(data).hexdigest()
    write_new(destination, data, guard)
    require(
        digest(destination, guard) == actual and digest(path, guard) == actual,
        "Snapshot bytes differ",
    )
    merge(frozen, key(destination), actual)
    return data


def render(progress, old_bytes):
    text = old_bytes.decode("utf-8")
    replacements = {
        "Updated UTC": "Updated UTC: " + progress["updated_utc"] + ". All execution is local.",
        "Current phase": "Current phase: " + progress["phase"] + ".",
        "Next action": "Next action: " + progress["next_action"],
    }
    for prefix, replacement in replacements.items():
        text, count = re.subn(
            r"(?m)^" + re.escape(prefix) + r":[^\r\n]*", lambda _: replacement, text
        )
        require(count == 1, "Exactly one existing status metadata row required")
    row = progress["entries"]["A02"]

    def paired_row(match):
        columns = match.group().split("|")
        require(len(columns) == 6, "Existing A02 status row shape changed")
        return (
            "| A02 |"
            + columns[2]
            + "| "
            + row["plan_status"]
            + " | "
            + row["execution_status"].replace("|", "&#124;")
            + " |"
        )

    text, count = re.subn(r"(?m)^\| A02 \|[^\r\n]*", paired_row, text)
    require(count == 1, "Exactly one existing A02 status row required")
    return text.encode("utf-8")


def certify_original_mutation(pair, ready, guard):
    before_data = bytes_read(FAILED / "progress_before.json", guard)
    after_data = bytes_read(FAILED / "progress_after.json", guard)
    status_before = bytes_read(FAILED / "STATUS_before.md", guard)
    status_after = bytes_read(FAILED / "STATUS_after.md", guard)
    before, after = json.loads(before_data), json.loads(after_data)
    require(
        len(before["entries"]) == len(after["entries"]) == 110, "All110 entries must remain present"
    )
    require(
        before["evidence_totals"]["later_receipts_pending_cumulative_packet"]["by_receipt"]
        == {"A04_mps_u_bridge_run001": 6},
        "Original before-credit inventory differs",
    )
    old_counts = before["evidence_totals"]["later_receipts_pending_cumulative_packet"]
    require(
        old_counts["distinct_new_cases"] == 6
        and old_counts["duplicate_audit_credit"] == 0
        and old_counts["new_complete_financial_replays"] == 0
        and old_counts["running_available_identity_count"] == 1708
        and old_counts["running_reported_qualified_count"] == 1754,
        "Actual old qualified/available count metadata differs",
    )
    expected = copy.deepcopy(before)
    pending = expected["evidence_totals"]["later_receipts_pending_cumulative_packet"]
    pending["by_receipt"][PRODUCER.name] = 32
    pending.update(
        distinct_new_cases=38,
        duplicate_audit_credit=0,
        new_complete_financial_replays=0,
        unqualified_cumulative_distinct_total=None,
        running_available_identity_count=1740,
        running_reported_qualified_count=1786,
    )
    expected["evidence_totals"]["distinct_pytest_cases"] = None
    expected["evidence_totals"]["quantum_advantage_established"] = False
    description = (
        f" Paired-loader final outcome {pair['outcome']}; root SHA/XML verification gives "
        "32 producer fixtures, zero audit credit. Component preference requires "
        "the independent audit; full financial adoption/cost/advantage remain false/open."
    )
    entry = expected["entries"]["A02"]
    entry["execution_status"] += description
    for directory in (PRODUCER, AUDIT):
        if key(directory) not in entry.setdefault("receipts", []):
            entry["receipts"].append(key(directory))
    timestamp = after["updated_utc"]
    require(
        isinstance(timestamp, str)
        and timestamp.endswith("+00:00")
        and datetime.fromisoformat(timestamp).utcoffset().total_seconds() == 0,
        "Recorded original registration UTC timestamp required",
    )
    expected["updated_utc"] = timestamp
    expected["phase"] = "Paired-loader verified final outcome: " + pair["outcome"]
    expected["next_action"] = ready["next_action_after_pair"]
    expected["history"].append(
        dict(
            time_utc=timestamp,
            items=["A02"],
            phase=expected["phase"],
            decision=description.strip(),
            receipts=[key(PRODUCER), key(FAILED)],
        )
    )
    require(
        expected == after,
        "Original before-to-after metadata differs from exact authorized registration",
    )
    require(encode(expected, guard) == after_data, "Original progress_after encoding differs")
    require(
        render(after, status_before) == status_after,
        "Original STATUS_before-to-after rendering differs",
    )
    require(
        read_json(FAILED / "progress_update_completed.json", guard)
        == {
            "mutable_path": key(PROGRESS),
            "immutable_snapshot": key(FAILED / "progress_after.json"),
        },
        "Original progress write completion record differs",
    )
    require(
        read_json(FAILED / "status_update_completed.json", guard)
        == {"mutable_path": key(STATUS), "immutable_snapshot": key(FAILED / "STATUS_after.md")},
        "Original status write completion record differs",
    )
    require(
        bytes_read(DIAGNOSTIC / "progress_observed.json", guard) == after_data
        and bytes_read(DIAGNOSTIC / "STATUS_observed.md", guard) == status_after,
        "Root diagnostic observed snapshots differ from original after bytes",
    )
    require(
        bytes_read(PROGRESS, guard) == after_data and bytes_read(STATUS, guard) == status_after,
        "Mutable root metadata changed since failed registration; no recovery overwrite",
    )
    return after, after_data, status_after


def replace_metadata(path, data, expected, guard):
    guard.check()
    require(digest(path, guard, fresh=True) == expected, "Concurrent mutable metadata change")
    temporary = path.with_name(path.name + ".recovery-" + str(os.getpid()) + ".tmp")
    write_new(temporary, data, guard)
    require(digest(path, guard, fresh=True) == expected, "Metadata changed before replacement")
    guard.check()
    os.replace(temporary, path)
    require(
        digest(path, guard, fresh=True) == hashlib.sha256(data).hexdigest(),
        "Replacement bytes differ",
    )


def runtime_capture(guard, frozen):
    """Copy only this stdlib process's observed files; external paths stay scoped."""
    files = {Path(sys.executable), Path(sys._base_executable)}
    forbidden = {"numpy", "scipy", "numba", "qiskit", "mpmath", "torch"}
    require(
        not any(name.split(".")[0] in forbidden for name in sys.modules),
        "Scientific module unexpectedly loaded in metadata-only process",
    )
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.GetModuleFileNameW.argtypes = [wintypes.HMODULE, wintypes.LPWSTR, wintypes.DWORD]
    kernel.GetModuleFileNameW.restype = wintypes.DWORD
    name_buffer = ctypes.create_unicode_buffer(32768)
    length = kernel.GetModuleFileNameW(
        wintypes.HMODULE(ctypes.pythonapi._handle), name_buffer, len(name_buffer)
    )
    require(0 < length < len(name_buffer), "Actual executing Python DLL path unavailable")
    files.add(Path(name_buffer.value))
    for module in tuple(sys.modules.values()):
        for attribute in ("__file__", "__cached__"):
            value = getattr(module, attribute, None)
            if value and Path(value).is_file():
                files.add(Path(value))
    destination = OUTPUT / "observed_runtime"
    destination.mkdir(exist_ok=False)
    for index, path in enumerate(sorted(files, key=lambda p: str(p).casefold())):
        guard.check()
        resolved = path.resolve(strict=True)
        require(path == resolved, "Observed runtime alias rejected")
        require(path.stat().st_size <= MAX_JSON, "Observed runtime individual byte cap exceeded")
        before = fingerprint(path)
        data = path.read_bytes()
        guard.check()
        require(fingerprint(path) == before, "Runtime file changed during capture")
        copy_path = destination / (f"{index:04d}_" + path.name)
        write_new(copy_path, data, guard)
        expected = hashlib.sha256(data).hexdigest()
        require(digest(copy_path, guard) == expected, "Observed runtime copy differs")
        merge(frozen, key(copy_path), expected)
        guard.external_runtime.append(
            dict(
                actual_path=str(path),
                immutable_copy=key(copy_path),
                sha256=expected,
                fingerprint=list(before),
                actual_live_path_in_ROOT_frozen_map=False,
            )
        )
    new_json(
        OUTPUT / "runtime_provenance.json",
        dict(
            no_scientific_imports=True,
            observed_loaded_stdlib_startup_support_and_interpreters_only=True,
            external_live_paths_are_separately_scoped=True,
            files=guard.external_runtime,
        ),
        guard,
    )


def final_fresh_union(frozen, guard):
    total = 0
    for name, expected in frozen.items():
        guard.check()
        path = canonical(name, fresh=True)
        total += path.stat().st_size
        require(total <= MAX_BYTES, "Complete unique frozen union byte cap exceeded")
        require(
            digest(path, guard, fresh=True) == expected,
            "Fresh terminal frozen SHA changed: " + name,
        )
    # Observed external stdlib paths are not falsely called ROOT map keys. Their
    # actual bytes are also freshly read and compared with the owned immutable copy.
    for row in guard.external_runtime:
        guard.check()
        path = Path(row["actual_path"])
        require(
            path.resolve(strict=True) == path and fingerprint(path) == tuple(row["fingerprint"]),
            "Observed executed runtime path changed",
        )
        before = fingerprint(path)
        result = hashlib.sha256()
        with path.open("rb") as stream:
            while block := stream.read(1 << 20):
                result.update(block)
                guard.hashed_bytes += len(block)
                require(
                    guard.hashed_bytes <= MAX_BYTES * 3, "Complete hash-work byte bound exceeded"
                )
                guard.check()
        require(
            fingerprint(path) == before and result.hexdigest() == row["sha256"],
            "Observed executed runtime bytes changed",
        )
    return total


def run(guard, frozen):
    preflight = read_json(PREFLIGHT, guard)
    require(
        preflight["schema"] == "paired-registration-recovery-preflight-v1"
        and preflight["hard_CPU_admission_CPU_hard_wall_admission_wall_seconds"]
        == [CPU, ADMISSION_CPU, WALL, ADMISSION_WALL]
        and preflight["pinned_manifest_sha256"] == PINS,
        "Prospective recovery preflight limits or immutable source pins differ",
    )
    require(
        preflight["maximum_references"] == MAX_REFERENCES
        and preflight["maximum_union_bytes"] == MAX_BYTES,
        "Prospective recovery inventory limits differ",
    )
    for path in (Path(__file__), PREFLIGHT, PREFLIGHT_MD):
        snapshot(path, OUTPUT / path.name, guard, frozen)
        merge(frozen, key(path), digest(path, guard))
    runtime_capture(guard, frozen)
    pair, ready = verify_scientific_metadata(guard, frozen)
    diagnostic = verify_failed_registration(guard, frozen)
    current, progress_before, status_before = certify_original_mutation(pair, ready, guard)
    snapshot(PROGRESS, OUTPUT / "progress_before.json", guard, frozen)
    snapshot(STATUS, OUTPUT / "STATUS_before.md", guard, frozen)
    recovered = copy.deepcopy(current)
    timestamp = datetime.now(timezone.utc).isoformat()
    description = (
        " Paired-loader registration bookkeeping censored during terminal SHA verification "
        "after progress/STATUS writes; producer, independent audit and root verification remain "
        "sealed PASS with strict-T preference rejected. Recovery verified the exact authorized "
        "prior 32-fixture insertion; no fixture credit was added again. The failed registration "
        "and its root failure diagnostic remain immutable."
    )
    recovered["entries"]["A02"]["execution_status"] += description
    recovered["updated_utc"] = timestamp
    recovered["phase"] = (
        "Paired-loader registration bookkeeping recovered; strict-T component remains rejected"
    )
    recovered["history"].append(
        dict(
            time_utc=timestamp,
            items=["A02"],
            phase=recovered["phase"],
            decision=description.strip(),
            receipts=[key(FAILED), key(DIAGNOSTIC), key(OUTPUT)],
        )
    )
    require(
        recovered["evidence_totals"] == current["evidence_totals"],
        "Recovery must not change any credit total",
    )
    require(
        recovered["next_action"] == current["next_action"],
        "Recovery must not change the scientific queue",
    )
    require(
        recovered["entries"]["A02"]["plan_status"] == current["entries"]["A02"]["plan_status"],
        "Recovery must not change plan completion status",
    )
    progress_after = encode(recovered, guard)
    status_after = render(recovered, status_before)
    write_new(OUTPUT / "progress_after.json", progress_after, guard)
    write_new(OUTPUT / "STATUS_after.md", status_after, guard)
    for name in ("progress_after.json", "STATUS_after.md"):
        merge(frozen, key(OUTPUT / name), digest(OUTPUT / name, guard))
    new_json(
        OUTPUT / "original_mutation_certificate.json",
        dict(
            original_before_to_after_exactly_reconstructed=True,
            original_recorded_registration_utc=current["updated_utc"],
            original_authorization_READY_sha256=PINS["ready"],
            progress_live_equal_original_after=True,
            STATUS_live_equal_original_after=True,
            original_before_counts={"A04_mps_u_bridge_run001": 6},
            original_after_counts={"A04_mps_u_bridge_run001": 6, PRODUCER.name: 32},
            fixture_credit_insertion_count=1,
            recovery_new_fixture_credit=0,
            current_available_actual_identities=1740,
            current_reported_qualified_count=1786,
            historical_identity_gap=46,
            unqualified_cumulative_distinct_total=None,
            failed_original_registration_remains_authoritative_failed_unsealed=True,
            old11_files_verified_without_changes=True,
            diagnostic3_owned12_frozen_verified=True,
            scientific_component_outcome=pair["outcome"],
            component_adoption=False,
            full_financial_adoption=False,
            quantum_advantage_established=False,
        ),
        guard,
    )
    require(
        key(PROGRESS) not in frozen and key(STATUS) not in frozen,
        "Mutable live docs must never become frozen input keys",
    )
    new_json(
        OUTPUT / "protocol.json",
        dict(
            schema="paired-registration-recovery-protocol-v1",
            local_only=True,
            no_scientific_imports_tests_replays_proof_evaluations=True,
            frozen_inputs=dict(frozen),
            source_inputs_verified_before_mutable_classification=True,
            original_registration_already_applied=True,
            recovery_fixture_credit=0,
            immutable_snapshots_only_for_mutable_docs=True,
            hard_CPU_admission_CPU_hard_wall_admission_wall_seconds=[
                CPU,
                ADMISSION_CPU,
                WALL,
                ADMISSION_WALL,
            ],
            maximum_references=MAX_REFERENCES,
            maximum_union_bytes=MAX_BYTES,
            maximum_total_hashwork_bytes=MAX_BYTES * 3,
            final_fresh_full_unique_union_required_after_metadata_updates=True,
            failure_preserves_partial_metadata_and_never_retries=True,
        ),
        guard,
    )
    guard.check()
    replace_metadata(PROGRESS, progress_after, hashlib.sha256(progress_before).hexdigest(), guard)
    new_json(
        OUTPUT / "progress_update_completed.json",
        dict(
            mutable_path=key(PROGRESS),
            immutable_snapshot=key(OUTPUT / "progress_after.json"),
            classification_only_no_fixture_readdition=True,
        ),
        guard,
    )
    replace_metadata(STATUS, status_after, hashlib.sha256(status_before).hexdigest(), guard)
    new_json(
        OUTPUT / "status_update_completed.json",
        dict(
            mutable_path=key(STATUS),
            immutable_snapshot=key(OUTPUT / "STATUS_after.md"),
            classification_only_no_fixture_readdition=True,
        ),
        guard,
    )
    return pair, diagnostic


def seal(pair, diagnostic, frozen, guard):
    unique_bytes = final_fresh_union(frozen, guard)
    require(
        bytes_read(PROGRESS, guard) == bytes_read(OUTPUT / "progress_after.json", guard)
        and bytes_read(STATUS, guard) == bytes_read(OUTPUT / "STATUS_after.md", guard),
        "Live metadata differs after recovery write",
    )
    require(
        owned_inventory(FAILED, guard) == {key(FAILED / n) for n in FAILED_NAMES}
        and not (FAILED / "manifest.json").exists(),
        "Original failed11 inventory changed at terminal",
    )
    new_json(
        OUTPUT / "summary.json",
        dict(
            passed=True,
            budget_censored=False,
            local_only=True,
            registration_bookkeeping_recovery_completed=True,
            original_failed_registration_preserved_unchanged=True,
            original_root_failure_diagnostic_preserved_unchanged=True,
            original_mutation_independently_certified=True,
            existing_producer_fixture_credit_retained=32,
            new_test_credit=0,
            duplicate_audit_credit=0,
            registration_fixture_credit_added_again=0,
            running_available_identity_count=1740,
            running_reported_qualified_count=1786,
            retained_historical_identity_gap=46,
            unqualified_cumulative_distinct_total=None,
            source_outcome=pair["outcome"],
            component_adopted=False,
            financial_source_adopted=False,
            quantum_advantage_established=False,
            no_scientific_imports_tests_replays_proof_evaluations=True,
            mutable_progress_or_status_in_frozen_input_map=False,
            complete_fresh_union_rehashed_paths=len(frozen),
            complete_unique_union_bytes=unique_bytes,
            external_observed_runtime_actual_files_freshly_verified=len(guard.external_runtime),
            actual_total_hashwork_bytes=guard.hashed_bytes,
            process_CPU_seconds_before_terminal_serialization=time.process_time(),
            wall_seconds_before_terminal_serialization=time.monotonic() - guard.wall_start,
            hard_CPU_admission_CPU_hard_wall_admission_wall_seconds=[
                CPU,
                ADMISSION_CPU,
                WALL,
                ADMISSION_WALL,
            ],
            old_failure_phase=diagnostic["failure_phase"],
        ),
        guard,
    )
    owned = {name: digest(canonical(name), guard) for name in owned_inventory(OUTPUT, guard)}
    manifest = dict(
        files=owned,
        frozen_inputs=frozen,
        terminal_record=key(OUTPUT / "summary.json"),
        manifest_self_hash_excluded=True,
        single_immutable_manifest=True,
        complete_fresh_unique_frozen_rehashes=len(frozen),
        process_CPU_limit_seconds=CPU,
        process_wall_limit_seconds=WALL,
        process_CPU_seconds_after_bulk_hashing=time.process_time(),
        wall_seconds_after_bulk_hashing=time.monotonic() - guard.wall_start,
    )
    data = encode(manifest, guard, terminal=True)
    guard.check(terminal=True)
    write_new(OUTPUT / "manifest.json", data, guard, terminal=True)


def retain_failure(output, error, guard):
    emergency = (
        b'{"passed":false,"new_test_credit":0,"integrity_not_certified":true,'
        b'"partial_files_preserved":true,"metadata_may_have_partially_updated":true,'
        b'"emergency_constant_marker_no_budget_certificate":true}\n'
    )
    try:
        if (output / "manifest.json").exists():
            (output / "manifest.json").rename(output / "manifest_invalid_after_hard_guard.json")
        guard.check(terminal=True)
        new_json(
            output / "failure.json",
            dict(
                passed=False,
                new_test_credit=0,
                registration_fixture_credit_added_again=0,
                error=repr(error)[:4000],
                traceback=traceback.format_exc()[-16000:],
                partial_files_preserved=True,
                metadata_may_have_partially_updated=True,
                old_failed_registration_unchanged=True,
                no_retry_or_overwrite=True,
            ),
            guard,
            terminal=True,
        )
        guard.check(terminal=True)
    except BaseException:
        pass
    # An exhausted hard budget cannot produce a certificate or a new full hash
    # pass. This bounded constant marker explicitly records that lack of sealing.
    with (output / "FAILED_UNSEALED.json").open("xb") as stream:
        stream.write(emergency)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    guard = Guard()
    require(
        canonical(sys.executable) == PYTHON and sys.dont_write_bytecode,
        "Pinned local Python -B before -m is required",
    )
    require(
        sys.orig_argv[1:4]
        == ["-B", "-m", "research.limitation_program_20261001.recover_two_draw_registration"]
        and args.output.is_absolute(),
        "Exact preregistered -B -m CLI and absolute output required",
    )
    require(
        all(not os.environ.get(n) for n in ("PYTHONPATH", "PYTHONHOME", "NUMBA_CACHE_DIR")),
        "Inherited external runtime override rejected",
    )
    output = canonical(args.output, exists=False)
    require(
        output == OUTPUT and not output.exists(),
        "Exactly the fresh fixed recovery receipt is required",
    )
    guard.check()
    output.mkdir(exist_ok=False)
    frozen = {}
    try:
        pair, diagnostic = run(guard, frozen)
        seal(pair, diagnostic, frozen, guard)
        return 0
    except BaseException as error:
        retain_failure(output, error, guard)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
