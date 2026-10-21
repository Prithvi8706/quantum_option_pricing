"""Prospective root receipt verifier/registrar; no scientific imports or reruns.

Author-only until root pins this file and issues the local READY packet. Verification
and registration each have a process CPU180/wall600 hard bound. Maps, XML and recorded
outcomes are inspected; no circuit, operator, numerical bound or test is evaluated.
Work admission is CPU150/wall540, leaving30CPU/60wall for bounded failure retention
inside those hard limits. The prospective100,000-reference/8GiB union cap accounts
for the full prior15k inputs plus package/source/bytecode trees in both new packets;
it is a bookkeeping bound, with no asserted measured fit and no scientific change.
Fresh immutable verification/registration receipts retain every failure. Mutable
progress/status bytes are copied as snapshots and never become frozen live keys.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time
import traceback
import xml.etree.ElementTree as ET

ROOT = Path("C:/Users/prith/quantum_option_pricing").resolve()
PROGRAM = ROOT / "results/limitation_program_20261001"
PINNED_PYTHON = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
PRODUCER = PROGRAM / "A02_two_draw_loader_resource_run002"
AUDIT = PROGRAM / "A02_two_draw_loader_resource_audit_run002"
LABELS = ("AS241_two_actual_scalar_invocations", "BoxMuller_one_actual_shared_pair")
CPU, WALL = 180, 600
ADMISSION_CPU, ADMISSION_WALL = 150, 540
MAX_REFERENCES, MAX_BYTES, MAX_OWN, MAX_JSON = 100_000, 8 * 1024**3, 512, 32 * 1024**2
SHA = re.compile(r"[0-9a-f]{64}\Z")
W10_SHA = "2a04693db9c76acdd5dd038248ee7a9dcaf2f32e4ce1dd9c325dc96ccd4a1320"
MPS_SHA = "bfe81ce4277ea6d4301c6529cf230cb5936f5e5005cca33a2aafcdc2270cece1"
FAILED_ADMISSION_SHA = "b2911a9d8d1c961f75f6f8a2418ed8d0d04e8011ea869b1c5006279f03cc4bdd"
PAIRED_FILES = (
    "two_draw_loader_source_v2.py",
    "experiment_two_draw_loader_resource_v2.py",
    "test_two_draw_loader_source_v2.py",
    "audit_two_draw_loader_resource_v2.py",
    "TWO_DRAW_LOADER_IMPLEMENTATION_PREFLIGHT_V2.md",
    "two_draw_loader_implementation_preflight_v2.json",
    "TWO_DRAW_LOADER_RESOURCE_PREFLIGHT.md",
    "two_draw_loader_resource_preflight.json",
)
_PATHS = {}
_ACTIVE_GUARD = None


def require(condition, message):
    if not condition:
        raise ValueError(message)


class Guard:
    def __init__(self):
        # Include interpreter startup and stdlib import CPU in the process cap.
        self.cpu_start = 0.0
        self.wall_start = time.monotonic()
        self.hashed_bytes = 0
        self.observed_hashes = {}

    def check(self, *, terminal=False):
        cpu_limit, wall_limit = (CPU, WALL) if terminal else (ADMISSION_CPU, ADMISSION_WALL)
        require(self.cpu_elapsed() < cpu_limit, "Verifier process CPU budget exhausted")
        require(
            time.monotonic() - self.wall_start < wall_limit,
            "Verifier process wall budget exhausted",
        )

    def cpu_elapsed(self):
        return time.process_time() - self.cpu_start


def canonical(name, *, must_exist=True, fresh=False):
    path = Path(name)
    if not path.is_absolute():
        require(not path.drive and "\\" not in str(name), "Canonical ROOT-relative key required")
        require(path.as_posix() == str(name), "Noncanonical lexical ROOT key")
        path = ROOT / path
    lexical = str(path)
    if not fresh and lexical in _PATHS:
        return _PATHS[lexical]
    resolved = path.resolve(strict=must_exist)
    resolved.relative_to(ROOT)
    require(path == resolved, "Symlink/alias receipt path rejected")
    if fresh and lexical in _PATHS:
        require(_PATHS[lexical] == resolved, "Previously confined path changed")
    _PATHS[lexical] = resolved
    return resolved


def key(path):
    return canonical(path).relative_to(ROOT).as_posix()


def read(path, guard):
    guard.check()
    path = canonical(path)
    require(path.stat().st_size <= MAX_JSON, "Bounded JSON/XML metadata exceeded")
    value = json.loads(path.read_bytes())
    guard.check()
    return value


def digest(path, guard, *, fresh=False):
    guard.check()
    path = canonical(path, fresh=fresh)
    before = path.stat()
    identity = str(path)
    fingerprint = (
        before.st_dev,
        before.st_ino,
        before.st_size,
        before.st_mtime_ns,
        before.st_ctime_ns,
        getattr(before, "st_file_attributes", None),
    )
    cached = guard.observed_hashes.get(identity)
    if not fresh and cached is not None and cached[0] == fingerprint:
        return cached[1]
    value = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            guard.hashed_bytes += len(block)
            require(guard.hashed_bytes <= MAX_BYTES * 3, "Whole verifier hash-work bound exceeded")
            value.update(block)
            guard.check()
    after = path.stat()
    require(
        fingerprint
        == (
            after.st_dev,
            after.st_ino,
            after.st_size,
            after.st_mtime_ns,
            after.st_ctime_ns,
            getattr(after, "st_file_attributes", None),
        ),
        "File changed while verifying: " + str(path),
    )
    actual = value.hexdigest()
    guard.observed_hashes[identity] = fingerprint, actual
    return actual


def merge(mapping, name, expected):
    require(isinstance(expected, str) and SHA.fullmatch(expected), "Explicit SHA256 required")
    path = canonical(name)
    require(
        not Path(name).is_absolute() and key(path) == name,
        "Manifest keys must be canonical ROOT-relative",
    )
    require(
        name not in mapping or mapping[name] == expected, "Conflicting canonical SHA expectation"
    )
    mapping[name] = expected


def receipt(directory, guard, frozen, *, optional=False):
    directory = canonical(directory, must_exist=not optional)
    if optional and not directory.exists():
        return {"classification": "not_run", "complete": False, "summary": {}}
    for marker in (
        "FAILED_UNSEALED.json",
        "failed_unsealed.json",
        "failure_retention_unsealed.json",
    ):
        require(
            not (directory / marker).exists(),
            "Authoritative failed-unsealed receipt: " + key(directory),
        )
    manifest_path = directory / "manifest.json"
    require(manifest_path.is_file(), "Incomplete preparation has no terminal manifest")
    manifest = read(manifest_path, guard)
    require(set(manifest) >= {"files", "frozen_inputs"}, "Recognized owned/frozen maps required")
    require(
        manifest.get("manifest_self_hash_excluded") is True,
        "Manifest self-hash convention required",
    )
    require(
        all(
            not isinstance(value, dict) or field in ("files", "frozen_inputs")
            for field, value in manifest.items()
        ),
        "Unknown manifest maps cannot be omitted",
    )
    owned, merged = {}, {}
    for field in ("files", "frozen_inputs"):
        require(isinstance(manifest[field], dict), "Manifest map must be a dictionary")
        for name, expected in manifest[field].items():
            guard.check()
            merge(merged, name, expected)
            if field == "files":
                require(canonical(name).is_relative_to(directory), "Owned file escaped receipt")
                merge(owned, name, expected)
    require(
        len(owned) <= MAX_OWN and len(merged) <= MAX_REFERENCES, "Fixed inventory bound exceeded"
    )
    actual = set()
    for path in directory.rglob("*"):
        guard.check()
        if path.is_file() and path != manifest_path:
            actual.add(key(path))
            require(len(actual) <= MAX_OWN, "Actual own inventory bound exceeded")
    require(actual == set(owned), "Own manifest inventory differs from actual receipt")
    byte_total = 0
    for name, expected in merged.items():
        path = canonical(name)
        byte_total += path.stat().st_size
        require(byte_total <= MAX_BYTES, "Receipt byte inventory bound exceeded")
        require(digest(path, guard) == expected, "Owned/frozen input SHA mismatch: " + name)
        merge(frozen, name, expected)
        require(len(frozen) <= MAX_REFERENCES, "Complete combined reference bound exceeded")
    merge(frozen, key(manifest_path), digest(manifest_path, guard))
    terminals = [
        directory / name
        for name in ("completion_outcome.json", "summary.json")
        if (directory / name).is_file()
    ]
    require(terminals, "Terminal result absent")
    terminal = terminals[0]
    require(key(terminal) in owned, "Authoritative terminal is not owned/manifest-bound")
    if "terminal_record" in manifest:
        require(manifest["terminal_record"] == key(terminal), "Terminal manifest pointer differs")
    summary = read(terminal, guard)
    require(type(summary.get("passed")) is bool, "Terminal passed boolean required")
    require(type(summary.get("budget_censored", False)) is bool, "Ambiguous censor flag")
    for name in (
        "failed",
        "failed_unsealed",
        "prepare_failed",
        "run_failed",
        "integrity_not_certified",
    ):
        if name in summary:
            require(type(summary[name]) is bool, "Ambiguous terminal failure flag")
            require(
                not (summary["passed"] and summary[name]),
                "Terminal failure flag prohibits successful credit",
            )
    failures = [
        name
        for name in ("run_failure.json", "prepare_failure.json", "completion_outcome.json")
        if (directory / name).exists()
    ]
    complete = (
        summary["passed"] is True and summary.get("budget_censored") is False and not failures
    )
    require(not (summary["passed"] and failures), "Failure evidence prohibits successful credit")
    protocol = (
        read(directory / "protocol.json", guard) if (directory / "protocol.json").exists() else {}
    )
    if "frozen_inputs" in protocol:
        require(
            protocol["frozen_inputs"] == manifest["frozen_inputs"], "Protocol frozen map differs"
        )
    return dict(
        classification="complete"
        if complete
        else "censored"
        if summary.get("budget_censored")
        else "failed",
        complete=complete,
        summary=summary,
        protocol=protocol,
        manifest=key(manifest_path),
        manifest_sha256=digest(manifest_path, guard),
        owned_files=len(owned),
        distinct_merged_paths=len(merged),
        byte_inventory=byte_total,
    )


def xml_identities(path, guard):
    guard.check()
    require(path.stat().st_size <= MAX_JSON, "XML byte bound exceeded")
    document = ET.parse(path).getroot()
    require(document.tag in ("testsuite", "testsuites"), "Unknown JUnit root")
    cases = list(document.iter("testcase"))
    identities = [(row.get("classname", ""), row.get("name")) for row in cases]
    require(
        len(identities) == len(set(identities)) and all(c and n for c, n in identities),
        "Duplicate/unnamed XML identities",
    )
    require(
        not any(
            row.find(tag) is not None for row in cases for tag in ("failure", "error", "skipped")
        ),
        "XML defects prohibit credit",
    )
    suites = [row for row in document.iter("testsuite") if row.findall("testcase")]
    require(
        sum(int(row.get("tests", 0)) for row in suites) == len(cases), "XML suite count differs"
    )
    require(
        all(
            int(row.get(field, 0)) == 0
            for row in suites
            for field in ("failures", "errors", "skipped")
        ),
        "XML suite defects",
    )
    guard.check()
    return set(identities)


def released_prior_identities(guard, frozen):
    known = set()
    for owner, wanted in (("WAVE10_run002", W10_SHA), ("A04_mps_u_bridge_run001", MPS_SHA)):
        directory = PROGRAM / owner
        manifest_path = directory / "manifest.json"
        require(digest(manifest_path, guard) == wanted, "Immutable released prior manifest changed")
        merge(frozen, key(manifest_path), wanted)
        manifest = read(manifest_path, guard)
        names = (
            ("historical_identity_reconciliation.json", "test_case_credit.json")
            if owner.startswith("WAVE")
            else ("tests.xml",)
        )
        for name in names:
            path = directory / name
            expected = manifest["files"][key(path)]
            require(digest(path, guard) == expected, "Prior identity evidence SHA mismatch")
            merge(frozen, key(path), expected)
            if name.endswith(".xml"):
                known.update(xml_identities(path, guard))
            elif name.startswith("historical"):
                for row in read(path, guard)["packets"].values():
                    known.update(tuple(case) for case in row["cases"])
            else:
                for row in read(path, guard)["packets"].values():
                    known.update(tuple(case) for case in row.get("credited_cases", []))
    require(len(known) == 1708, "Released available identity inventory changed")
    return known


def admit_ready(path, guard, frozen):
    ready = read(path, guard)
    require(
        ready.get("schema") == "paired-local-continuation-ready-v1"
        and ready.get("ready") is True
        and ready.get("local_execution_authorized") is True,
        "Actual root READY release required",
    )
    require(
        ready["producer_receipt"] == key(PRODUCER) and ready["audit_receipt"] == key(AUDIT),
        "Root-selected paired v2 receipts differ",
    )
    require(
        ready["producer_preflight_filename"] == "two_draw_loader_implementation_preflight_v2.json"
        and ready["fixture_module_basename"] == "test_two_draw_loader_source_v2",
        "V2 fixed fixture/preflight labels differ",
    )
    required = {"research/limitation_program_20261001/" + name for name in PAIRED_FILES}
    required.add("research/limitation_program_20261001/verify_two_draw_loader_receipts.py")
    require(
        required <= set(ready["source_sha256"]), "Root READY missing reviewed code/preflight pins"
    )
    for name in sorted(required):
        expected = ready["source_sha256"][name]
        require(
            digest(canonical(name), guard) == expected, "Root READY frozen source differs: " + name
        )
        merge(frozen, name, expected)
    require(
        ready["verifier_limits"]
        == {
            "process_CPU_seconds": CPU,
            "work_admission_CPU_seconds": ADMISSION_CPU,
            "wall_seconds": WALL,
            "work_admission_wall_seconds": ADMISSION_WALL,
            "maximum_references": MAX_REFERENCES,
            "maximum_union_bytes": MAX_BYTES,
        },
        "Root READY verifier operational limits differ",
    )
    python_pin = ready["tools"]["python"]
    require(
        canonical(python_pin["path"]) == PINNED_PYTHON
        and digest(PINNED_PYTHON, guard) == python_pin["sha256"],
        "Root READY pinned interpreter differs",
    )
    merge(frozen, key(PINNED_PYTHON), python_pin["sha256"])
    merge(frozen, key(path), digest(path, guard))
    return ready


def verify_pair(guard, frozen, ready):
    require(
        not (PROGRAM / "A02_two_draw_loader_resource_run001").exists(),
        "Pre-mkdir failed pairedrun001 must remain absent",
    )
    failed_path = PROGRAM / "A02_two_draw_loader_admission_failure_run001/manifest.json"
    require(
        digest(failed_path, guard) == FAILED_ADMISSION_SHA,
        "Original paired admission failure manifest changed",
    )
    failure = receipt(failed_path.parent, guard, frozen)
    require(
        failure["summary"]["passed"] is False and not failure["complete"],
        "Original admission failure cannot receive credit",
    )
    require(
        failure["summary"]["failed_intended_receipt_absent"] is True
        and failure["summary"]["protocol_or_array_or_cost_or_replay_or_fixture_execution"] is False
        and failure["summary"]["fixed_CPU_hard_admission_wall_seconds"] == [300, 240, 600]
        and failure["summary"]["new_test_credit"] == 0,
        "Original failed admission must remain pre-mkdir with zero fixture credit",
    )
    require(
        all(
            value == 0
            for name, value in failure["summary"].items()
            if name.endswith("credit") and isinstance(value, (int, float))
        ),
        "Original admission failure claims credit",
    )
    producer = receipt(PRODUCER, guard, frozen)
    audit = receipt(AUDIT, guard, frozen, optional=True)
    result = dict(
        producer=producer,
        audit=audit,
        producer_fixture_credit=0,
        audit_fixture_credit=0,
        component_preferred=False,
        identities=[],
        financial_source_adopted=False,
        quantum_advantage_established=False,
        unqualified_cumulative_distinct_total=None,
        historical_identity_gap=46,
        prior_failed_admission=failure,
        original_paired_run001_absent=True,
    )
    if not producer["complete"]:
        result["outcome"] = producer["classification"]
        return result
    summary, protocol = producer["summary"], producer["protocol"]
    preflight = read(PRODUCER / ready["producer_preflight_filename"], guard)
    require(
        digest(PRODUCER / ready["producer_preflight_filename"], guard)
        == ready["source_sha256"][
            "research/limitation_program_20261001/" + ready["producer_preflight_filename"]
        ],
        "Executed producer preflight copy differs from root release",
    )
    require(
        preflight["fixed_fixture_count"] == protocol["declared_unique_tests"] == 32,
        "Exact declared32 inventory required",
    )
    require(
        preflight["fixed_labels"] == protocol["fixed_labels"] == list(LABELS),
        "Fixed comparison labels changed",
    )
    require(
        protocol["fixed_input_pairs"] == preflight["input_pairs"]
        and protocol["dirty_outputs_each72"] == preflight["dirty_outputs_each72"]
        and len(preflight["input_pairs"]) == 8
        and len(preflight["dirty_outputs_each72"]) == 2,
        "Fixed preregistered input/dirty-output inventory changed",
    )
    require(
        (
            protocol["process_CPU_seconds"],
            protocol["admission_CPU_seconds"],
            protocol["wall_seconds"],
        )
        == (300, 240, 600),
        "Producer bounds changed",
    )
    identities = xml_identities(PRODUCER / "tests.xml", guard)
    wanted = {
        f"test_actual_complete_native_loader_and_literal_inverse[{label}-pair{pair}-dirty{dirty}]"
        for label in LABELS
        for pair in range(8)
        for dirty in range(2)
    }
    require(
        len(identities) == 32 and {name for _, name in identities} == wanted,
        "XML differs from exact fixed fixture definitions",
    )
    require(
        all(
            c == ready["fixture_module_basename"]
            or c.endswith("." + ready["fixture_module_basename"])
            for c, _ in identities
        ),
        "Unexpected fixture module",
    )
    credit = read(PRODUCER / "test_credit_reconciliation.json", guard)
    require(
        {tuple(row) for row in credit["test_identities"]} == identities
        and credit["unique_new_fixtures_passed"] == 32
        and credit["prior_fixture_counts_added_again"] == 0,
        "Saved fixture reconciliation differs",
    )
    known = released_prior_identities(guard, frozen)
    require(
        not known.intersection(identities), "Historical fixture identities cannot be recredited"
    )
    replay = read(PRODUCER / "actual_gate_replays.json", guard)
    slots = {(row["loader"], row["pair_index"], row["dirty_index"]) for row in replay["rows"]}
    require(
        len(replay["rows"]) == replay["completed_replays"] == 32
        and slots == {(label, p, d) for label in LABELS for p in range(8) for d in range(2)},
        "Actual saved basis fixture inventory differs",
    )
    require(
        all(
            row[field] is True
            for row in replay["rows"]
            for field in (
                "full_native_inputs72_preserved",
                "all_full_SSA_and_native_private_bits_clean",
                "literal_inverse_restores_complete_state",
                "all_allocated_bits_checked",
                "actual_immutable_gate_replay",
            )
        ),
        "Recorded basis fixture failure",
    )
    require(
        all(
            row["q32_raw"] == preflight["input_pairs"][row["pair_index"]]
            and row["initial_outputs72"]
            == [preflight["dirty_outputs_each72"][row["dirty_index"]]] * 2
            and row["lane"] == 2 * row["pair_index"] + row["dirty_index"]
            and row["observed_outputs72"] == row["expected_outputs72"]
            for row in replay["rows"]
        ),
        "Saved lane/input/output evidence differs from declared fixtures",
    )
    require(
        all(
            summary[field] == 32
            for field in (
                "tests_completed",
                "new_test_credit",
                "new_unique_fixtures_passed",
                "completed_actual_basis_fixtures",
            )
        ),
        "Producer fixture totals differ",
    )
    require(
        summary["old_fixture_recredit"] == 0
        and summary["both_complete_dirty72_clean_ABI_validated"] is True
        and summary["actual_loader_rows"] == 2,
        "Complete clean ABI scope required",
    )
    require(
        summary["full_financial_sampler_or_estimator_adopted"] is False
        and summary["full_G2"] is False
        and summary["quantum_advantage_established"] is False
        and summary["full_financial_native_cost"] is None
        and summary["physical_runtime"] is None,
        "Component cannot claim full finance or advantage",
    )
    require(
        summary["all_110_obligations_retained"] is True,
        "Broad limitation obligations must remain open",
    )
    decision = read(PRODUCER / "paired_component_decision.json", guard)
    ledger = read(PRODUCER / "native_resource_ledger.json", guard)
    require(
        set(ledger) == set(LABELS) and decision == summary["paired_component_decision"],
        "Two resource rows/decision differ",
    )
    require(
        all(
            type(ledger[label]["clean_resources"][field]) is int
            and ledger[label]["clean_resources"][field] >= 0
            for label in LABELS
            for field in ("t_count", "logical_qubits")
        ),
        "Invalid recorded resource integer",
    )
    require(
        summary["logical_qubit_cap"]
        == protocol["logical_qubit_cap"]
        == preflight["logical_qubit_cap"]
        == 45_000
        and all(ledger[label]["clean_resources"]["logical_qubits"] <= 45_000 for label in LABELS)
        and summary["initial_Hadamards_separate"]
        == protocol["uniform_preparation_H_separate"]
        == 64,
        "Whole-loader cap or separate uniform preparation changed",
    )
    improvement = (
        ledger[LABELS[0]]["clean_resources"]["t_count"]
        < ledger[LABELS[1]]["clean_resources"]["t_count"]
    )
    require(
        decision["AS241_component_strict_T_improvement"] is improvement
        and decision["AS241_component_eligible_pending_independent_audit"] is improvement,
        "Strict T decision differs from recorded exact counts",
    )
    require(
        decision["paired_AS241_component_adopted"] is False
        and decision["independent_resource_audit_still_required"] is True
        and decision["both_losing_or_winning_resource_rows_preserved"] is True
        and decision["financial_source_cost_divided_by_coordinate_count"] is False
        and decision["complete_financial_sampler_or_estimator_adopted"] is False,
        "Premature adoption or false cost boundary",
    )
    require(
        decision["comparison_unit"]
        == "two actual AS241 scalar invocations versus one actual unchanged shared BM pair",
        "Complete paired comparison unit changed",
    )
    result.update(
        producer_fixture_credit=32,
        identities=[list(row) for row in sorted(identities)],
        strict_T_improvement=improvement,
        outcome="passed_cost_improvement_pending_audit" if improvement else "passed_cost_rejected",
        available_prior_identity_count=1708,
        available_prior_plus_new_identities=1740,
    )
    if audit["complete"]:
        value = audit["summary"]
        audit_protocol = audit["protocol"]
        require(
            (
                audit_protocol["process_CPU_seconds"],
                audit_protocol["admission_CPU_seconds"],
                audit_protocol["wall_seconds"],
            )
            == (180, 150, 600)
            and audit_protocol["source_receipt"] == key(PRODUCER)
            and audit_protocol["independent_native_reexecutions"] == 32
            and audit_protocol["unique_new_fixture_credit"] == 0,
            "Independent audit source, budgets or fixture scope changed",
        )
        require(
            value["independent_two_draw_resource_audit_passed"] is True
            and value["producer_actual_tests_verified"]
            == value["independent_native_reexecutions"]
            == 32,
            "Independent audit scope differs",
        )
        require(
            value["new_test_credit"] == value["old_fixture_recredit"] == 0
            and value["component_AS241_adopted_under_strict_T_rule"] is improvement,
            "Audit credit/adoption differs",
        )
        require(
            value["financial_source_adopted"] is False
            and value["full_G2_established"] is False
            and value["quantum_advantage_claim"] is False,
            "Audit cannot adopt full financial source",
        )
        independent = read(AUDIT / "independent_native_resource_ledger.json", guard)
        require(independent == ledger, "Saved independent resource ledger differs")
        independent_replay = read(AUDIT / "independent_actual_gate_replays.json", guard)
        require(
            independent_replay["completed_independent_reexecutions"] == 32
            and independent_replay["unique_new_fixture_credit"] == 0
            and independent_replay["all_allocated_lane_masks_compared"] is True
            and independent_replay["rows"] == replay["rows"],
            "Saved independent basis records differ",
        )
        require(
            value["every_allocated_wire_and_fixed_lane_mask_matches_producer"] is True
            and value["losing_resource_rows_retained"] is True
            and value["financial_source_cost_divided_by_coordinate_count"] is False,
            "Independent complete-row scope or cost boundary differs",
        )
        result.update(
            component_preferred=improvement,
            outcome="passed_cost_improvement_audited"
            if improvement
            else "passed_cost_rejected_audited",
        )
    elif audit["classification"] != "not_run":
        result["outcome"] = "producer_passed_audit_" + audit["classification"]
    return result


def write_new(path, data, *, terminal=False):
    _ACTIVE_GUARD.check(terminal=terminal)
    require(len(data) <= MAX_JSON, "Bounded new metadata bytes exceeded")
    with path.open("xb") as stream:
        for offset in range(0, len(data), 1 << 20):
            _ACTIVE_GUARD.check(terminal=terminal)
            stream.write(data[offset : offset + (1 << 20)])
    _ACTIVE_GUARD.check(terminal=terminal)


def new_json(path, value, *, terminal=False):
    _ACTIVE_GUARD.check(terminal=terminal)
    data = (json.dumps(value, indent=2, allow_nan=False) + "\n").encode("utf-8")
    _ACTIVE_GUARD.check(terminal=terminal)
    write_new(path, data, terminal=terminal)


def snapshot(path, destination, guard, frozen):
    guard.check()
    require(canonical(path).stat().st_size <= MAX_JSON, "Snapshot byte bound exceeded")
    data = canonical(path).read_bytes()
    guard.check()
    require(len(data) <= MAX_JSON, "Snapshot byte bound exceeded")
    write_new(destination, data)
    actual = hashlib.sha256(data).hexdigest()
    require(digest(destination, guard) == actual, "Snapshot copy differs")
    merge(frozen, key(destination), actual)
    return data


def seal(output, summary, frozen, guard):
    guard.check()
    require(len(frozen) <= MAX_REFERENCES, "Combined frozen reference inventory exceeded")
    union_bytes = 0
    for name, expected in frozen.items():
        guard.check()
        union_bytes += canonical(name).stat().st_size
        require(union_bytes <= MAX_BYTES, "Complete frozen union byte bound exceeded")
        require(
            digest(canonical(name, fresh=True), guard, fresh=True) == expected,
            "Final fresh input changed: " + name,
        )
    new_json(output / "summary.json", summary)
    files = {key(path): digest(path, guard) for path in output.rglob("*") if path.is_file()}
    require(len(files) <= MAX_OWN, "Verifier own inventory exhausted")
    guard.check(terminal=True)
    content = (
        json.dumps(
            dict(
                files=files,
                frozen_inputs=frozen,
                terminal_record=key(output / "summary.json"),
                manifest_self_hash_excluded=True,
                process_CPU_limit_seconds=CPU,
                process_wall_limit_seconds=WALL,
                single_immutable_manifest=True,
                process_CPU_seconds_after_bulk_hashing=guard.cpu_elapsed(),
                wall_seconds_after_bulk_hashing=time.monotonic() - guard.wall_start,
                fresh_unique_frozen_rehashes=len(frozen),
            ),
            indent=2,
        )
        + "\n"
    ).encode()
    guard.check(terminal=True)
    write_new(output / "manifest.json", content, terminal=True)


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
        require(count == 1, "Exactly one existing status metadata row required: " + prefix)
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


def replace_metadata(path, data, expected, guard):
    guard.check()
    require(
        digest(path, guard) == expected, "Concurrent root metadata change; registration stopped"
    )
    temporary = path.with_name(path.name + ".paired-" + str(os.getpid()) + ".tmp")
    with temporary.open("xb") as stream:
        for offset in range(0, len(data), 1 << 20):
            guard.check()
            stream.write(data[offset : offset + (1 << 20)])
        stream.flush()
        os.fsync(stream.fileno())
    guard.check()
    require(digest(path, guard) == expected, "Concurrent metadata change before replace")
    os.replace(temporary, path)


def registration(args, output, guard, frozen):
    previous = read(args.verification, guard)
    require(
        previous["passed"] is True and previous["safe_to_register_progress"] is True,
        "Verified final outcome required",
    )
    verified_owner = receipt(canonical(args.verification).parent, guard, frozen)
    require(verified_owner["complete"], "Verification owner is not a complete terminal packet")
    ready = admit_ready(args.ready, guard, frozen)
    pair = verify_pair(guard, frozen, ready)
    require(pair == previous["pair"], "Producer/audit outcome changed after verification")
    require(
        ready.get("ready") is True
        and ready.get("local_execution_authorized") is True
        and ready.get("registration_authorized") is True,
        "Root READY registration release absent",
    )
    require(
        isinstance(ready.get("next_action_after_pair"), str) and ready["next_action_after_pair"],
        "Root next action required",
    )
    snapshot(args.ready, output / "root_READY_snapshot.json", guard, frozen)
    progress_path = PROGRAM / "progress.json"
    status_path = ROOT / "docs/limitation_program_20261001/STATUS.md"
    old_progress = snapshot(progress_path, output / "progress_before.json", guard, frozen)
    old_status = snapshot(status_path, output / "STATUS_before.md", guard, frozen)
    progress = json.loads(old_progress)
    require(len(progress["entries"]) == 110, "All110 entries must remain present")
    pending = progress["evidence_totals"].setdefault("later_receipts_pending_cumulative_packet", {})
    counts = pending.setdefault("by_receipt", {})
    require(PRODUCER.name not in counts, "Producer already registered; no retries/recredit")
    count = pair["producer_fixture_credit"]
    counts[PRODUCER.name] = count
    pending.update(
        distinct_new_cases=sum(counts.values()),
        duplicate_audit_credit=0,
        new_complete_financial_replays=0,
        unqualified_cumulative_distinct_total=None,
    )
    # These remain explicitly pending the next cumulative packet. No missing
    # historical identities or audit reexecutions are added to fixture credit.
    if set(counts) <= {"A04_mps_u_bridge_run001", PRODUCER.name}:
        pending["running_available_identity_count"] = 1702 + sum(counts.values())
        pending["running_reported_qualified_count"] = 1748 + sum(counts.values())
    progress["evidence_totals"]["distinct_pytest_cases"] = None
    progress["evidence_totals"]["quantum_advantage_established"] = False
    entry = progress["entries"]["A02"]
    description = (
        f" Paired-loader final outcome {pair['outcome']}; root SHA/XML verification gives "
        f"{count} producer fixtures, zero audit credit. Component preference requires "
        "the independent audit; full financial adoption/cost/advantage remain false/open."
    )
    entry["execution_status"] += description
    for directory in (PRODUCER, AUDIT):
        if directory.exists() and key(directory) not in entry.setdefault("receipts", []):
            entry["receipts"].append(key(directory))
    progress["updated_utc"] = datetime.now(timezone.utc).isoformat()
    progress["phase"] = "Paired-loader verified final outcome: " + pair["outcome"]
    progress["next_action"] = ready["next_action_after_pair"]
    progress["history"].append(
        dict(
            time_utc=progress["updated_utc"],
            items=["A02"],
            phase=progress["phase"],
            decision=description.strip(),
            receipts=[key(PRODUCER), key(output)],
        )
    )
    new_progress = (json.dumps(progress, indent=2, allow_nan=False) + "\n").encode()
    new_status = render(progress, old_status)
    write_new(output / "progress_after.json", new_progress)
    write_new(output / "STATUS_after.md", new_status)
    # Snapshot/new-byte verification precedes both reversible metadata updates.
    require(
        digest(output / "progress_after.json", guard) == hashlib.sha256(new_progress).hexdigest(),
        "New progress copy mismatch",
    )
    require(
        digest(output / "STATUS_after.md", guard) == hashlib.sha256(new_status).hexdigest(),
        "New status copy mismatch",
    )
    replace_metadata(progress_path, new_progress, hashlib.sha256(old_progress).hexdigest(), guard)
    new_json(
        output / "progress_update_completed.json",
        dict(
            mutable_path=key(progress_path), immutable_snapshot=key(output / "progress_after.json")
        ),
    )
    replace_metadata(status_path, new_status, hashlib.sha256(old_status).hexdigest(), guard)
    new_json(
        output / "status_update_completed.json",
        dict(mutable_path=key(status_path), immutable_snapshot=key(output / "STATUS_after.md")),
    )
    return pair


def main():
    global _ACTIVE_GUARD
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("verify", "register"))
    parser.add_argument("--producer", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--verification", type=Path)
    parser.add_argument("--ready", type=Path, required=True)
    args = parser.parse_args()
    require(
        canonical(args.producer, must_exist=False) == PRODUCER
        and canonical(args.audit, must_exist=False) == AUDIT,
        "Fixed paired receipts only",
    )
    require(
        (args.phase != "register") or (args.verification is not None and args.ready is not None),
        "Registration requires verification and root READY",
    )
    guard = Guard()
    _ACTIVE_GUARD = guard
    require(
        canonical(sys.executable) == PINNED_PYTHON and sys.dont_write_bytecode,
        "Pinned local Python with -B before this script is required",
    )
    output = canonical(args.output, must_exist=False)
    require(
        output.parent == PROGRAM and not output.exists(),
        "Fresh verifier/registration receipt required",
    )
    output.mkdir(exist_ok=False)
    frozen = {}
    try:
        snapshot(Path(__file__), output / Path(__file__).name, guard, frozen)
        merge(frozen, key(sys.executable), digest(Path(sys.executable), guard))
        ready = admit_ready(args.ready, guard, frozen)
        require(
            digest(output / Path(__file__).name, guard)
            == ready["source_sha256"][
                "research/limitation_program_20261001/verify_two_draw_loader_receipts.py"
            ],
            "Executed verifier snapshot differs from root release",
        )
        pair = (
            verify_pair(guard, frozen, ready)
            if args.phase == "verify"
            else registration(args, output, guard, frozen)
        )
        summary = dict(
            passed=True,
            budget_censored=False,
            local_only=True,
            pair=pair,
            safe_to_register_progress=True,
            new_test_credit=0,
            verified_producer_fixture_credit=pair["producer_fixture_credit"],
            audit_fixture_credit=0,
            financial_source_adopted=False,
            quantum_advantage_established=False,
            verification_monotonic_start=guard.wall_start,
            verifier_process_CPU_seconds=guard.cpu_elapsed(),
            verifier_wall_seconds_before_bulk_hashing=time.monotonic() - guard.wall_start,
            process_CPU_limit_seconds=CPU,
            process_wall_limit_seconds=WALL,
            new_work_admission_CPU_seconds=ADMISSION_CPU,
            new_work_admission_wall_seconds=ADMISSION_WALL,
            complete_frozen_union_reference_cap=MAX_REFERENCES,
            complete_frozen_union_byte_cap=MAX_BYTES,
            numerical_imports_tests_replays_proof_evaluations=0,
            mutable_progress_or_status_in_frozen_input_map=False,
        )
        seal(output, summary, frozen, guard)
    except BaseException as failure:
        if (output / "manifest.json").exists():
            (output / "manifest.json").rename(output / "manifest_invalid_after_hard_guard.json")
        try:
            guard.check(terminal=True)
            new_json(
                output / "failure.json",
                dict(
                    passed=False,
                    error=repr(failure)[:8192],
                    traceback=traceback.format_exc()[:65536],
                    partial_files_preserved=True,
                    no_retry_or_overwrite=True,
                    producer_fixture_credit=0,
                ),
                terminal=True,
            )
            if not (output / "summary.json").exists():
                new_json(
                    output / "summary.json",
                    dict(
                        passed=False,
                        budget_censored="exhausted" in str(failure),
                        new_test_credit=0,
                        safe_to_register_progress=False,
                        partial_files_preserved=True,
                    ),
                    terminal=True,
                )
        except BaseException:
            pass  # The constant marker below is the only emergency write.
        # Never turn an incomplete input check, an unsealed source packet or an
        # exhausted verification budget into a manifest integrity certificate.
        with (output / "FAILED_UNSEALED.json").open("xb") as stream:
            stream.write(
                b'{"passed":false,"new_test_credit":0,"integrity_not_certified":true,"partial_files_preserved":true,"metadata_may_have_partially_updated":true,"emergency_constant_marker_no_budget_certificate":true}\n'
            )
        raise


if __name__ == "__main__":
    main()
