"""Reconcile the fixed, terminal local quantile/loading wave without reruns.

Only receipt bytes, XML identities and recorded outcomes are inspected. The
single manifest is created last; no provisional manifest is overwritten.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import traceback
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
RESEARCH = ROOT / "research/limitation_program_20261001"
OUTPUT = PROGRAM / "WAVE10_run001"
PREFLIGHT = RESEARCH / "wave10_finalizer_preflight.json"
BASE = "WAVE09_run003"
CPU_LIMIT, WALL_LIMIT = 300, 900
ADMISSION_CPU, ADMISSION_WALL = 270, 810
MAX_OUTPUT_FILES = 64
SHA_PATTERN = re.compile(r"[0-9a-f]{64}\Z")
FIXED_RECEIPTS = (
    "C09_stagec_timing_update_run001",
    "A02_quantile_tail_audit_run001",
    "A02_quantile_transform_run002",
    "A02_quantile_transform_audit_run001",
    "A02_quantile_law_run001",
    "A02_quantile_law_audit_run001",
    "A16_direct_control_run001",
    "A16_clean_xor_w2_run001",
    "A04_structure_run002",
    "A17_quantile_divider_run001",
    "A02_quantile_scalar_run001",
    "A02_quantile_scalar_audit_run001",
    "A16_clean_xor_native_run001",
    "C09_conservative_coverage_run001",
    "A02_quantile_financial_target_run001",
    "A02_quantile_financial_run005",
    "A02_quantile_financial_audit_run001",
    "A04_mps_run001",
)
FIXTURE_COUNTS = {
    "A02_quantile_transform_run002": 26,
    "A02_quantile_law_run001": 36,
    "A16_direct_control_run001": 5,
    "A16_clean_xor_w2_run001": 8,
    "A04_structure_run002": 16,
    "A17_quantile_divider_run001": 17,
    "A02_quantile_scalar_run001": 27,
    "A16_clean_xor_native_run001": 19,
    "C09_conservative_coverage_run001": 21,
    "A02_quantile_financial_target_run001": 36,
    "A02_quantile_financial_run005": 25,
    "A04_mps_run001": 16,
}
LATER_FIXTURES = {
    "A03_prefix_run001": 18,
    "A02_quantile_tail_run001": 40,
    "A16_dynamic_run001": 15,
}
LATER_ZERO_CREDIT = (
    "A03_prefix_audit_run001",
    "A03_law_screen_run001",
    "A03_law_screen_audit_run001",
    "C09_stagec_update_run001",
)
FAILED_RECEIPTS = (
    "A04_structure_run001",
    "A02_quantile_transform_admission_failure_run001",
    "A02_quantile_financial_admission_failure_run001",
    "A02_quantile_financial_admission_failure_run002",
    "A02_quantile_financial_run003",
    "A02_quantile_financial_run004",
)
# Literal XML inventories follow the predecessor summaries and their executed
# finalizers. They do not inspect test code or collect/run pytest.
HISTORICAL_WAVES = (
    (
        "WAVE01_run001",
        153,
        (
            ("A06_run001", "regression.xml"),
            ("A10_log_run001", "regression.xml"),
            ("A07_run003", "regression.xml"),
        ),
    ),
    (
        "WAVE02_run002",
        78,
        (
            ("A11_leaf_run001", "regression.xml"),
            ("A11_run001", "integration_tests.xml"),
        ),
    ),
    (
        "WAVE03_run001",
        70,
        (
            ("A10_square_leaf_run001", "regression.xml"),
            ("A10_square_run001", "integration_tests.xml"),
        ),
    ),
    (
        "WAVE04_run001",
        79,
        (
            ("A07_shift_leaf_run001", "regression.xml"),
            ("A07_shift_run001", "integration_tests.xml"),
        ),
    ),
    (
        "WAVE05_run001",
        88,
        (
            ("A11_nonrestoring_leaf_run001", "regression.xml"),
            ("A11_nonrestoring_run001", "integration_tests.xml"),
        ),
    ),
    (
        "WAVE06_run001",
        113,
        (
            ("A09_range_leaf_run001", "regression.xml"),
            ("A09_range_run001", "integration_tests.xml"),
        ),
    ),
    (
        "WAVE07_run001",
        191,
        (
            ("A10_coefficient_leaf_run001", "regression.xml"),
            ("A10_coefficient_run001", "integration_tests.xml"),
        ),
    ),
    (
        "WAVE08_run001",
        80,
        (
            ("A18_run001", "tests.xml"),
            ("A18_B4_run001", "tests.xml"),
            ("A18_budgetfix_run001", "pytest.xml"),
        ),
    ),
)
MISSING_BASE_IDENTITIES = (
    {"wave": "WAVE01_run001", "receipt": "A08_run001/attempt002", "reported_cases": 22},
    {"wave": "WAVE01_run001", "receipt": "A09_run001", "reported_cases": 24},
)


class BudgetCensoredError(RuntimeError):
    """Stop admissions while reserving time to retain a terminal receipt."""


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def encoded(value):
    return (json.dumps(value, indent=2, allow_nan=False) + "\n").encode("utf-8")


def create(path, value):
    create_bytes(path, encoded(value))


def create_bytes(path, data):
    with Path(path).open("xb") as handle:
        handle.write(data)


def canonical(name, base=ROOT):
    path = Path(str(name).replace("\\", "/"))
    require(not path.drive or path.is_absolute(), "Ambiguous drive-relative path")
    result = path.resolve() if path.is_absolute() else (base / path).resolve()
    result.relative_to(ROOT.resolve())
    return result


def relative(path):
    return canonical(path).relative_to(ROOT.resolve()).as_posix()


def budget(started, terminal=False):
    cpu = time.process_time() - started[0]
    wall = time.monotonic() - started[1]
    limits = (CPU_LIMIT, WALL_LIMIT) if terminal else (ADMISSION_CPU, ADMISSION_WALL)
    if cpu >= limits[0] or wall >= limits[1]:
        raise BudgetCensoredError("Fixed finalizer CPU/wall budget reached")
    return cpu, wall


def sha(path, started=None, terminal=False):
    if started is not None:
        budget(started, terminal=terminal)
    value = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            value.update(block)
            if started is not None:
                budget(started, terminal=terminal)
    return value.hexdigest()


def bind(frozen, name, expected, base=ROOT):
    normalized = relative(canonical(name, base))
    require(
        isinstance(expected, str) and SHA_PATTERN.fullmatch(expected), "Explicit SHA256 required"
    )
    require(
        normalized not in frozen or frozen[normalized] == expected,
        "Conflicting canonical SHA256 expectation: " + normalized,
    )
    frozen[normalized] = expected


def verify(frozen, started):
    for name, expected in frozen.items():
        require(sha(canonical(name), started) == expected, "Frozen input changed: " + name)


def manifest_maps(path):
    """Decode only the historical map forms understood by the v3 validator."""
    data = read(path)
    require(isinstance(data, dict) and data, "Nonempty receipt manifest required")
    maps = []
    if all(isinstance(value, str) and SHA_PATTERN.fullmatch(value) for value in data.values()):
        maps.append((data, path.parent, "flat"))
    else:
        for field in (
            "files",
            "external_files",
            "frozen_inputs",
            "dependency_sha256",
            "additional_files",
            "report",
            "sha256",
        ):
            if field not in data:
                continue
            require(isinstance(data[field], dict), "Manifest map is not a dictionary: " + field)
            base = (
                path.parent
                if field == "sha256" or (field == "files" and "external_files" in data)
                else ROOT
            )
            maps.append((data[field], base, field))
        for row_name, row in data.get("inputs", {}).items():
            require(isinstance(row, dict), "Manifest input row is not a dictionary")
            for field, value in row.items():
                partner = field[:-5] + "_sha256"
                if field.endswith("_path") and partner in row:
                    maps.append(({value: row[partner]}, ROOT, "inputs." + row_name))
    require(maps, "No supported file maps in manifest: " + relative(path))
    return data, maps


def receipt(name, frozen, started, merge_dependencies=False):
    """Require terminal records and bind all owned bytes, including failed packets."""
    directory = canonical(PROGRAM / name)
    require(directory.is_dir(), "Required terminal receipt is absent: " + name)
    manifest_path = directory / "manifest.json"
    if not manifest_path.is_file():
        manifest_path = directory / "TOP_MANIFEST.json"
    require(manifest_path.is_file(), "Required terminal manifest is absent: " + name)
    record = next(
        (
            directory / candidate
            for candidate in (
                "completion_outcome.json",
                "summary.json",
                "FINAL_RECEIPT.json",
                "failed_tests.json",
            )
            if (directory / candidate).is_file()
        ),
        None,
    )
    require(record is not None, "Required terminal outcome is absent: " + name)
    summary = read(record)
    require(isinstance(summary.get("passed"), bool), "Terminal passed boolean is absent: " + name)
    require(isinstance(summary.get("budget_censored", False), bool), "Ambiguous censor metadata")
    data, maps = manifest_maps(manifest_path)
    owned, dependency_maps = {}, []
    for mapping, base, field in maps:
        for key, expected in mapping.items():
            path = canonical(key, base)
            local = path.is_relative_to(directory)
            if local:
                bind(owned, path, expected)
            if merge_dependencies:
                bind(frozen, path, expected)
            elif local:
                bind(frozen, path, expected)
        if field != "files" and field != "flat":
            dependency_maps.append(field)
    # Some old finalizers deliberately wrote validation after their one manifest.
    # This exact linked-wave artifact is newly SHA-bound, never retroactively
    # described as a member of its old manifest.
    extras = (
        {relative(directory / "validation.json")}
        if name
        in {
            "WAVE08_run001",
            "WAVE02_run002",
            "WAVE03_run001",
            "WAVE04_run001",
            "WAVE05_run001",
            "WAVE06_run001",
            "WAVE07_run001",
        }
        else set()
    )
    if name == "A09_run001":
        extras.update(
            relative(directory / filename)
            for filename in (
                "FINAL_RECEIPT.json",
                "executed_code/__pycache__/prefix_multiplier.cpython-312.pyc",
            )
        )
    actual = {
        relative(path) for path in directory.rglob("*") if path.is_file() and path != manifest_path
    }
    require(set(owned).issubset(actual), "Owned manifest members are missing: " + name)
    require(
        actual - set(owned) <= extras,
        "Unbound receipt bytes: " + name + ": " + repr(sorted(actual - set(owned))),
    )
    record_has_original_membership = relative(record) in owned
    recognized_current_terminal_extra = (
        name == "A09_run001" and record.name == "FINAL_RECEIPT.json" and relative(record) in extras
    )
    require(
        record_has_original_membership or recognized_current_terminal_extra,
        "Terminal outcome is not manifest-bound or an exact scoped legacy extra: " + name,
    )
    verify(owned, started)
    for key in sorted(actual - set(owned)):
        bind(frozen, key, sha(canonical(key), started))
    bind(frozen, manifest_path, sha(manifest_path, started))
    return summary, {
        "terminal_record": relative(record),
        "terminal_record_original_manifest_membership": record_has_original_membership,
        "terminal_record_current_metadata_observation_only": recognized_current_terminal_extra,
        "manifest": relative(manifest_path),
        "owned_files": len(owned),
        "all_owned_bytes_verified": True,
        "legacy_unmanifested_artifacts_newly_bound": sorted(actual - set(owned)),
        "legacy_extra_original_manifest_membership_verified": not (actual - set(owned)),
        "legacy_extra_historical_execution_or_cache_provenance_claimed": False,
        "budget_censor_flag_present": "budget_censored" in summary,
        "missing_censor_flag_uses_legacy_successful_terminal_convention": (
            "budget_censored" not in summary
        ),
        "dependency_map_fields": dependency_maps,
    }


def xml_cases(path, require_success=True):
    document = ET.parse(path).getroot()
    require(document.tag in ("testsuites", "testsuite"), "Unknown JUnit document")
    cases = list(document.iter("testcase"))
    identities = [(case.get("classname", ""), case.get("name")) for case in cases]
    require(all(isinstance(name, str) and name for _, name in identities), "Unnamed XML testcase")
    defects = sum(
        case.find(tag) is not None for case in cases for tag in ("failure", "error", "skipped")
    )
    if require_success:
        suites = [suite for suite in document.iter("testsuite") if list(suite.findall("testcase"))]
        require(cases and len(cases) == len(set(identities)), "XML cases are empty or duplicated")
        require(not defects, "Failed, errored or skipped XML cannot receive fixture credit")
        require(
            sum(int(suite.get("tests", 0)) for suite in suites) == len(cases),
            "XML suite counts differ from actual testcase identities",
        )
        require(
            all(
                int(suite.get(field, 0)) == 0
                for suite in suites
                for field in ("failures", "errors", "skipped")
            ),
            "XML suite has failures",
        )
    return set(identities), {
        "junit": relative(path),
        "actual_testcases": len(cases),
        "actual_unique_testcases": len(set(identities)),
        "failure_error_skip_nodes": defects,
    }


def xml_choice(name):
    choices = sorted((PROGRAM / name).glob("*.xml"))
    require(len(choices) == 1, "Exactly one actual fixture XML required: " + name)
    return choices[0]


def interpreter_binding(frozen, started):
    launcher = canonical(sys.executable)
    launcher_sha = sha(launcher, started)
    bind(frozen, launcher, launcher_sha)
    base = Path(getattr(sys, "_base_executable", sys.executable)).resolve()
    base_sha = sha(base, started)
    try:
        base_name = relative(base)
    except ValueError:
        base_record = {
            "absolute_path": str(base),
            "sha256": base_sha,
            "included_in_workspace_frozen_map": False,
            "scope": "Only the actual external base interpreter is read and hashed",
        }
    else:
        bind(frozen, base_name, base_sha)
        base_record = {
            "workspace_relative": base_name,
            "sha256": base_sha,
            "included_in_workspace_frozen_map": True,
        }
    return {
        "launcher_workspace_relative": relative(launcher),
        "launcher_sha256": launcher_sha,
        "base_interpreter": base_record,
        "python_version": sys.version,
        "prefix": sys.prefix,
        "base_prefix": sys.base_prefix,
    }


def verify_interpreter(record, frozen, started):
    require(
        relative(sys.executable) == record["launcher_workspace_relative"],
        "Actual invoked interpreter launcher differs",
    )
    require(sys.version == record["python_version"], "Actual interpreter version differs")
    base = Path(getattr(sys, "_base_executable", sys.executable)).resolve()
    identity = record["base_interpreter"]
    key = "workspace_relative" if identity["included_in_workspace_frozen_map"] else "absolute_path"
    actual = relative(base) if identity["included_in_workspace_frozen_map"] else str(base)
    require(
        actual == identity[key] and sha(base, started) == identity["sha256"],
        "Actual base interpreter identity or bytes differ",
    )
    require(
        frozen[relative(sys.executable)] == record["launcher_sha256"], "Launcher frozen binding"
    )


def process_clearance(started):
    require(os.name == "nt", "This fixed local packet requires Windows process observation")
    command = (
        "Get-CimInstance Win32_Process | "
        "Select-Object ProcessId,ParentProcessId,Name,ExecutablePath,CommandLine | "
        "ConvertTo-Json -Compress"
    )
    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    )
    rows = json.loads(result.stdout)
    rows = [rows] if isinstance(rows, dict) else rows
    require(isinstance(rows, list) and rows, "Complete process observation required")
    by_pid = {int(row["ProcessId"]): row for row in rows}
    require(os.getpid() in by_pid, "Own process must appear in the process observation")
    ancestors, parent = set(), int(by_pid[os.getpid()]["ParentProcessId"])
    while parent in by_pid and parent not in ancestors:
        ancestors.add(parent)
        parent = int(by_pid[parent]["ParentProcessId"])
    interpreter_paths = {
        str(Path(sys.executable).resolve()).casefold(),
        str(Path(getattr(sys, "_base_executable", sys.executable)).resolve()).casefold(),
    }
    own_module = "research.limitation_program_20261001.finalize_quantile_loading_wave"
    own_script = str(RESEARCH / "finalize_quantile_loading_wave.py").lower().replace("\\", "/")
    launcher_ancestors = []
    roots, workers = set(), set()
    for row in rows:
        pid, name = int(row["ProcessId"]), str(row["Name"]).lower()
        line = str(row.get("CommandLine") or "").lower().replace("\\", "/")
        if pid == os.getpid():
            continue
        executable = row.get("ExecutablePath")
        module_command = re.search(r"(?:^|\s)-m\s+" + re.escape(own_module) + r"(?=\s|$)", line)
        script_command = own_script in line and " -c " not in line
        if (
            pid in ancestors
            and "python" in name
            and isinstance(executable, str)
            and str(Path(executable).resolve()).casefold() in interpreter_paths
            and (module_command or script_command)
        ):
            # A Windows venv redirector can remain alive as this process's
            # launcher. Only the matching actual interpreter ancestor is
            # exempted; arbitrary Python parents remain blocking.
            launcher_ancestors.append(
                {
                    "pid": pid,
                    "executable": str(Path(executable).resolve()),
                    "sha256": sha(Path(executable), started),
                    "matching_finalizer_command": True,
                }
            )
            continue
        supervisor = name in {"bash.exe", "sh.exe", "cmd.exe", "wsl.exe"} and re.search(
            r"stage_c_day[^\s\"']*\.sh", line
        )
        timing = (
            "python" in name
            and "research.frontier_classical_20261001." in line
            and any(marker in line for marker in ("c5_smoothers", "c7_c8_cases", "c2_timing"))
        )
        experiment = "python" in name and "research.limitation_program_20261001." in line
        if supervisor or timing or experiment:
            roots.add(pid)
        if "python" in name and any(
            marker in line
            for marker in ("spawn_main", "--multiprocessing-fork", "resource_tracker")
        ):
            workers.add(pid)
    descendants = set(roots)
    while True:
        more = {int(row["ProcessId"]) for row in rows if int(row["ParentProcessId"]) in descendants}
        if more.issubset(descendants):
            break
        descendants.update(more)
    relevant = [row for row in rows if int(row["ProcessId"]) in descendants | workers]
    require(not relevant, "Exclusive local queue has live workers: " + json.dumps(relevant))
    return {
        "observed_utc": datetime.now(timezone.utc).isoformat(),
        "live_stage_c_or_limitation_roots_and_descendants": [],
        "live_spawn_and_resource_tracker_workers": [],
        "verified_own_interpreter_launcher_ancestors": launcher_ancestors,
        "observation_is_not_a_future_process_guarantee": True,
    }


def reconstruct_base(frozen, started):
    cases, owners, rows, missing = set(), {}, {}, []
    for wave, declared, inventory in HISTORICAL_WAVES:
        summary, _ = receipt(wave, frozen, started)
        field = (
            "distinct_successful_pytest_cases"
            if wave == "WAVE01_run001"
            else "new_distinct_pytest_cases"
        )
        require(
            summary["passed"] is True and summary[field] == declared,
            "Historical wave count changed",
        )
        wave_cases = set()
        for name, filename in inventory:
            packet, _ = receipt(name, frozen, started)
            require(
                packet["passed"] is True and not packet.get("budget_censored", False),
                "Historical credited packet is not successful/uncensored",
            )
            path = PROGRAM / name / filename
            if not path.is_file():
                missing.append(
                    {
                        "wave": wave,
                        "receipt": name,
                        "junit": relative(path),
                        "reason": "Required historical XML is missing",
                    }
                )
                continue
            identities, row = xml_cases(path)
            require(relative(path) in frozen, "Historical XML has no frozen manifest binding")
            row.update(wave=wave, cases=sorted(identities))
            rows[name] = row
            wave_cases.update(identities)
            for identity in identities:
                owners.setdefault(identity, []).append(name)
        if wave == "WAVE01_run001":
            require(len(wave_cases) == 107, "Actual first-wave55/41/11 XML identity count changed")
            for gap in MISSING_BASE_IDENTITIES:
                packet, _ = receipt(gap["receipt"], frozen, started)
                require(packet["passed"] is True, "Missing-identity successful receipt changed")
                require(
                    not list((PROGRAM / gap["receipt"]).glob("*.xml")),
                    "Additional first-wave XML now exists; version the finite inventory",
                )
                missing.append(
                    dict(gap, reason="Successful receipt has no saved XML identity ledger")
                )
        else:
            require(
                len(wave_cases) == declared,
                "Historical wave actual distinct XML count changed: " + wave,
            )
        cases.update(wave_cases)
    previous, _ = receipt(BASE, frozen, started)
    require(
        previous["total_distinct_pytest_cases"] == 1423
        and previous["total_financial_gate_replays"] == 41,
        "Reported1423-test/41-financial-replay baseline changed",
    )
    ledger = read(PROGRAM / BASE / "test_case_credit.json")
    require(
        sum(row["count"] for row in ledger.values()) == 571, "Wave09 actual ledger count changed"
    )
    wave9_cases = set()
    for name, row in ledger.items():
        packet, _ = receipt(name, frozen, started)
        require(
            packet["passed"] is True and not packet.get("budget_censored", False),
            "Wave09 credited packet is not successful/uncensored",
        )
        path = canonical(row["junit"])
        path.relative_to((PROGRAM / name).resolve())
        identities, observed = xml_cases(path)
        require(relative(path) in frozen, "Wave09 XML is not frozen manifest-bound")
        require(
            identities == {tuple(case) for case in row["cases"]}
            and len(identities) == row["count"],
            "Wave09 ledger differs from actual XML",
        )
        require(not wave9_cases.intersection(identities), "Repeated Wave09 identities")
        wave9_cases.update(identities)
        rows[name] = dict(observed, wave=BASE, cases=sorted(identities))
        for identity in identities:
            owners.setdefault(identity, []).append(name)
    cases.update(wave9_cases)
    duplicates = [
        {"case": identity, "receipts": names}
        for identity, names in sorted(owners.items())
        if len(names) > 1
    ]
    return (
        previous,
        cases,
        {
            "reported_historical_base_count": 1423,
            "available_actual_distinct_identity_count": len(cases),
            "packets": rows,
            "cross_wave_duplicate_identities": duplicates,
            "missing_identity_evidence": missing,
            "missing_reported_identity_count": sum(row.get("reported_cases", 0) for row in missing),
            "complete_historical_identity_ledger_available": not missing,
        },
    )


def strict_validation(output, prior, frozen, started):
    # Before trusting the old validator, enforce ROOT confinement and equal-SHA
    # alias merges in EACH historical manifest. Historical live disagreements
    # across different receipts remain separate legitimate expectations.
    for path in sorted(
        set(PROGRAM.rglob("manifest.json")) | set(PROGRAM.rglob("TOP_MANIFEST.json"))
    ):
        _, maps = manifest_maps(path)
        local = {}
        for mapping, base, _ in maps:
            for name, expected in mapping.items():
                bind(local, name, expected, base)
        protocol_path = path.parent / "protocol.json"
        if protocol_path.is_file():
            dependencies = read(protocol_path).get("executed_dependencies", [])
            require(isinstance(dependencies, list), "Executed dependency rows must be a list")
            for row in dependencies:
                require(isinstance(row, dict), "Executed dependency row must be a dictionary")
                snapshot = canonical(row["snapshot"], path.parent)
                snapshot.relative_to(path.parent.resolve())
                bind(local, snapshot, row["sha256"])
        budget(started)
    spec = importlib.util.spec_from_file_location(
        "wave10_frozen_validator", output / "validate_receipts_v3.py"
    )
    require(spec is not None and spec.loader is not None, "Frozen validator cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    old_bytecode_setting = sys.dont_write_bytecode
    try:
        sys.dont_write_bytecode = True
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = old_bytecode_setting
    module.digest = lambda path: sha(path, started) if Path(path).is_file() else None
    validation = module.validate(
        PROGRAM,
        PROGRAM / "A01_drift_run001/reconciliation.json",
        workspace_root=ROOT,
        emit=False,
        raise_on_failure=False,
    )
    old = read(PROGRAM / BASE / "validation.json")

    def signatures(rows):
        return {
            (
                relative(row["path"]),
                row["expected"],
                row["actual"],
                relative(row["manifest"]),
                row["source_map"],
                row["source_key"],
            )
            for row in rows
        }

    require(
        prior["global_live_integrity"] is False and old["global_live_integrity"] is False,
        "Prior strict global live integrity changed",
    )
    require(
        validation["global_live_integrity"] is False
        and len(validation["mismatches"]) == 36
        and len({relative(row["path"]) for row in validation["mismatches"]}) == 9,
        "Strict global live result must retain exactly36 references/nine paths",
    )
    require(
        signatures(validation["mismatches"]) == signatures(old["mismatches"]),
        "Strict live mismatch reference bytes/owners changed",
    )
    require(
        validation["legitimate_expected_hashes_waived"] is False,
        "Legitimate historical expectations cannot be waived",
    )
    require(
        validation["archived_or_current_integrity_passed"] is True,
        "Archived/current receipt validity failed",
    )
    validation["wave10_manifest_not_yet_created_during_global_scan"] = True
    validation["wave10_own_bytes_verified_separately_before_single_terminal_manifest"] = True
    verify(frozen, started)
    return validation


def reconcile(output, frozen, started):
    progress_path = PROGRAM / "progress.json"
    progress_bytes = progress_path.read_bytes()
    progress = json.loads(progress_bytes.decode("utf-8"))
    progress_sha = hashlib.sha256(progress_bytes).hexdigest()
    progress_snapshot = output / "progress_snapshot.json"
    create_bytes(progress_snapshot, progress_bytes)
    require(sha(progress_snapshot, started) == progress_sha, "Exact progress snapshot copy differs")
    bind(frozen, progress_snapshot, progress_sha)
    require(
        tuple(progress["static_author_preflights"]["dependency_order"]) == FIXED_RECEIPTS,
        "Fixed18 dependency order changed",
    )
    require(
        progress["accepted_baseline"]
        == "results/limitation_program_20261001/A10_coefficient_run001",
        "Accepted financial latency source changed",
    )
    preflight = read(PREFLIGHT)
    require(
        preflight["fixed_dependency_order"] == list(FIXED_RECEIPTS)
        and preflight["fixture_counts_are_inventory_not_credit"] == FIXTURE_COUNTS
        and preflight["fixed_fixture_inventory_count_not_credit"] == sum(FIXTURE_COUNTS.values())
        and preflight["process_CPU_limit_seconds"] == CPU_LIMIT
        and preflight["wall_limit_seconds"] == WALL_LIMIT,
        "Preflight inventory differs",
    )
    require(
        not (PROGRAM / "A02_quantile_transform_run001").exists(),
        "Pre-mkdir failed transformrun001 must remain absent",
    )
    require(
        not (PROGRAM / "A02_quantile_financial_run001").exists(),
        "Pre-mkdir failed financialrun001 must remain absent",
    )
    require(
        not (PROGRAM / "A02_quantile_financial_run002").exists(),
        "Pre-mkdir failed financialrun002 must remain absent",
    )
    actual_interpreter = interpreter_binding(frozen, started)
    source = Path(__file__).resolve()
    require(
        source == RESEARCH / "finalize_quantile_loading_wave.py",
        "Run the authorized research source",
    )
    for path in (source, PREFLIGHT, RESEARCH / "validate_receipts_v3.py"):
        expected = sha(path, started)
        bind(frozen, path, expected)
        destination = output / path.name
        shutil.copy2(path, destination)
        require(sha(destination, started) == expected, "Copied source/preflight differs")
        bind(frozen, destination, expected)
    outcomes, terminal = {}, {}
    for name in (*FIXED_RECEIPTS, *LATER_FIXTURES, *LATER_ZERO_CREDIT, *FAILED_RECEIPTS):
        outcomes[name], terminal[name] = receipt(name, frozen, started, merge_dependencies=True)
    for name in FAILED_RECEIPTS:
        require(outcomes[name]["passed"] is False, "Known failed attempt must remain failed")
    previous, known, historical = reconstruct_base(frozen, started)
    create(output / "historical_identity_reconciliation.json", historical)
    credits, collisions, new_cases = {}, [], set()
    for name, declared in {**LATER_FIXTURES, **FIXTURE_COUNTS}.items():
        packet = outcomes[name]
        successful = packet["passed"] is True and packet.get("budget_censored", False) is False
        choices = sorted((PROGRAM / name).glob("*.xml"))
        observed, identities = None, set()
        if successful:
            identities, observed = xml_cases(xml_choice(name))
            require(
                len(identities) == declared,
                "Actual unique XML differs from fixed inventory: " + name,
            )
        elif choices:
            require(len(choices) == 1, "Failed packet XML is ambiguous: " + name)
            identities, observed = xml_cases(choices[0], require_success=False)
        overlap = identities.intersection(known | new_cases) if successful else set()
        if overlap:
            collisions.append({"receipt": name, "cases": sorted(overlap)})
        credit = identities - known - new_cases if successful else set()
        new_cases.update(credit)
        credits[name] = {
            "declared_inventory_count": declared,
            "successful_uncensored_packet": successful,
            "credited_count": len(credit),
            "credited_cases": sorted(credit),
            "actual_xml": observed,
            "duplicate_cases_not_recredited": sorted(overlap),
            "failed_or_censored_packet_zero_credit": not successful,
        }
    for name in (*FIXED_RECEIPTS, *LATER_ZERO_CREDIT, *FAILED_RECEIPTS):
        if name not in credits:
            credits[name] = {"credited_count": 0, "audit_or_snapshot_or_failed_packet": True}
    financial = outcomes["A02_quantile_financial_run005"]
    audit = outcomes["A02_quantile_financial_audit_run001"]
    require(
        financial.get("new_source_matched_native_financial_bias_certificate_adopted") is False,
        "Native financial bound must retain zero source adoption",
    )
    rejected = (
        financial["passed"] is False
        and financial.get("budget_censored", False) is False
        and financial.get("reason") == "financial_bias_exceeds_frozen_residual"
        and financial.get("all_two_actual_source_math_bounds_completed") is True
    )
    arithmetic = (
        rejected and audit["passed"] is True and audit.get("budget_censored", False) is False
    )
    if arithmetic:
        require(
            audit.get("independent_financial_source_and_arithmetic_audit_passed") is True
            and audit.get("original_method_rejected_solely_for_financial_budget") is True
            and audit.get("both_saved_bounds_fit_frozen_residual") is False,
            "Complete residual rejection does not match independent arithmetic audit",
        )
        require(
            credits["A02_quantile_financial_run005"]["credited_count"] == 0,
            "Failed financial budget method cannot receive fixture credit",
        )
    create(
        output / "test_case_credit.json",
        {
            "packets": credits,
            "cross_wave_collisions": collisions,
            "actual_distinct_new_identities_among_available_evidence": len(new_cases),
            "historical_missing_identities_prevent_unqualified_cumulative_distinct_claim": True,
        },
    )
    create(
        output / "preserved_failed_attempts.json",
        {
            name: value
            for name, value in outcomes.items()
            if value["passed"] is False or value.get("budget_censored", False)
        },
    )
    create(
        output / "method_outcomes.json",
        {
            "packets": outcomes,
            "terminal_receipt_verification": terminal,
            "complete_valid_financial_arithmetic_retained_despite_residual_overrun": arithmetic,
            "residual_overrun_method_fixture_credit": 0 if rejected else None,
            "financial_source_sampler_or_estimator_adoption": False,
            "financial_correctness_residual_fit_and_adoption_are_separate": True,
            "pre_mkdir_transformrun001_absent": True,
            "pre_mkdir_financialrun001_absent": True,
        },
    )
    create(output / "progress_at_wave_freeze.json", progress)
    create(
        output / "protocol.json",
        {
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "local_only": True,
            "fixed_dependency_order": list(FIXED_RECEIPTS),
            "all_fixed18_terminal_before_reconciliation": True,
            "frozen_inputs": frozen,
            "interpreter_binding": actual_interpreter,
            "progress_observation": {
                "observed_mutable_workspace_path": relative(progress_path),
                "observed_SHA256": progress_sha,
                "mutable_path_in_live_frozen_input_map": False,
                "immutable_snapshot": relative(progress_snapshot),
                "immutable_snapshot_SHA256": progress_sha,
                "one_observed_byte_sequence_parsed_and_copied_exactly": True,
            },
            "all_canonical_workspace_SHA_insertions_preserve_equal_prior_expectations": True,
            "external_runtime_binding_is_scoped_separately_from_workspace_maps": True,
            "copied_code_and_preflight_immutable": True,
            "partial_failure_terminal_without_retry": True,
            "single_final_manifest_only": True,
            "new_tests_circuits_prices_or_replays": 0,
            "process_CPU_limit_seconds": CPU_LIMIT,
            "wall_limit_seconds": WALL_LIMIT,
            "admission_CPU_seconds_with_terminal_reserve": ADMISSION_CPU,
            "admission_wall_seconds_with_terminal_reserve": ADMISSION_WALL,
        },
    )
    validation = strict_validation(output, previous, frozen, started)
    create(output / "validation.json", validation)
    create(output / "terminal_process_clearance.json", process_clearance(started))
    verify_interpreter(actual_interpreter, frozen, started)
    complete = historical["complete_historical_identity_ledger_available"]
    return {
        "passed": True,
        "local_only": True,
        "result_scope": "Finite terminal receipt reconciliation",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "global_live_integrity": False,
        "live_mismatch_references": 36,
        "distinct_live_mismatch_paths": 9,
        "legitimate_expected_hashes_waived": False,
        "archived_or_current_integrity_passed": True,
        "validated_manifest_count": validation["manifest_count"],
        "validated_distinct_files": validation["distinct_hashed_files"],
        "reported_historical_distinct_pytest_cases": 1423,
        "historical_actual_available_distinct_identity_count": len(known),
        "missing_historical_identity_evidence": historical["missing_identity_evidence"],
        "new_distinct_pytest_cases_among_available_evidence": len(new_cases),
        "new_distinct_pytest_cases": len(new_cases) if complete else None,
        "total_distinct_pytest_cases": len(known | new_cases) if complete else None,
        "total_available_actual_distinct_pytest_identities": len(known | new_cases),
        "unqualified_cumulative_distinct_count_verified": complete,
        "historical_base_plus_current_packet_credits_is_not_a_verified_distinct_count": True,
        "later_fixture_packet_credit": sum(
            credits[name]["credited_count"] for name in LATER_FIXTURES
        ),
        "fixed18_fixture_packet_credit": sum(
            credits[name]["credited_count"] for name in FIXTURE_COUNTS
        ),
        "all_audits_failed_and_censored_packets_receive_zero_fixture_credit": True,
        "historical_clean_XOR_financial_gate_replays": 41,
        "total_financial_gate_replays": 41,
        "historical_streaming_harness_gate_replays": 6,
        "historical_source_phase_marking_gate_replays": 6,
        "historical_extracted_subgraph_replays": 3,
        "current_scalar_candidate_replays_retained_separately": outcomes[
            "A02_quantile_scalar_run001"
        ].get("candidate_actual_gate_replays", 0),
        "current_scalar_control_replays_retained_separately": outcomes[
            "A02_quantile_scalar_run001"
        ].get("control_actual_gate_replays", 0),
        "new_tests_circuits_prices_financial_or_component_gate_replays_executed_by_finalizer": 0,
        "complete_valid_financial_arithmetic_retained_despite_residual_overrun": arithmetic,
        "financial_sampler_source_or_estimator_adopted": False,
        "preferred_latency_source": progress["accepted_baseline"],
        "preferred_latency_source_unchanged": True,
        "huge_financial_QPE_statevector_or_price_observations": 0,
        "original_continuous_financial_price_certified": False,
        "full_physical_mapping_or_execution_fidelity_certified": False,
        "quantum_advantage_established": False,
        "G2_to_G5": "open",
        "completed_wave_does_not_complete_overall_goal": True,
        "included_receipts": list(outcomes),
        "work_continuing": progress["active_items"],
        "next_action": progress["next_action"],
    }


def finish(output, frozen, started, summary):
    """Hash every bulk output and verify inputs before the terminal manifest."""
    verify(frozen, started)
    create(output / "summary.json", summary)
    files = {
        relative(path): sha(path, started) for path in sorted(output.rglob("*")) if path.is_file()
    }
    require(len(files) <= MAX_OUTPUT_FILES, "Fixed finalizer output inventory exceeded")
    cpu, wall = budget(started, terminal=True)
    terminal_manifest = encoded(
        {
            "files": files,
            "frozen_inputs": frozen,
            "manifest_self_hash_excluded": True,
            "terminal_record": relative(output / "summary.json"),
            "all_input_verification_and_bulk_output_hashing_before_terminal": True,
            "preterminal_process_CPU_seconds": cpu,
            "preterminal_wall_seconds": wall,
            "process_CPU_limit_seconds": CPU_LIMIT,
            "wall_limit_seconds": WALL_LIMIT,
            "single_immutable_manifest": True,
        }
    )
    budget(started, terminal=True)
    create_bytes(output / "manifest.json", terminal_manifest)


def run(output):
    output = canonical(output)
    require(output == OUTPUT.resolve(), "Only the prospective WAVE10_run001 is authorized")
    require(not output.exists(), "Fresh receipt required; terminal/partial receipts cannot retry")
    started, frozen = (time.process_time(), time.monotonic()), {}
    output.mkdir()  # Exclusive creation; all subsequent failures preserve this directory.
    try:
        create(output / "initial_process_clearance.json", process_clearance(started))
        summary = reconcile(output, frozen, started)
        finish(output, frozen, started, summary)
    except BaseException as failure:
        create(
            output / "finalization_failure.json",
            {
                "failure_type": type(failure).__name__,
                "message": str(failure),
                "traceback": traceback.format_exc(),
                "partial_files_preserved": True,
                "fixed_receipt_terminal_no_retry": True,
            },
        )
        terminal = output / (
            "completion_outcome.json" if (output / "summary.json").exists() else "summary.json"
        )
        create(
            terminal,
            {
                "passed": False,
                "local_only": True,
                "budget_censored": isinstance(
                    failure, (BudgetCensoredError, TimeoutError, subprocess.TimeoutExpired)
                ),
                "finalization_failed": True,
                "new_test_credit": 0,
                "new_tests_circuits_prices_or_replays": 0,
                "partial_files_preserved": True,
                "fixed_receipt_terminal_no_retry": True,
                "elapsed_process_CPU_seconds": time.process_time() - started[0],
                "elapsed_wall_seconds": time.monotonic() - started[1],
            },
        )
        # Reserve is used only to retain failure bytes, never to continue science
        # or turn a budget stop into a successful packet. No input is re-admitted.
        if not (output / "manifest.json").exists():
            try:
                files = {
                    relative(path): sha(path, started, terminal=True)
                    for path in sorted(output.rglob("*"))
                    if path.is_file()
                }
                budget(started, terminal=True)
                terminal_manifest = encoded(
                    {
                        "files": files,
                        "frozen_inputs": frozen,
                        "manifest_self_hash_excluded": True,
                        "terminal_record": relative(terminal),
                        "partial_failure_terminal_without_retry": True,
                        "failed_finalizer_fixture_credit": 0,
                    }
                )
                budget(started, terminal=True)
                create_bytes(output / "manifest.json", terminal_manifest)
            except BudgetCensoredError:
                create(
                    output / "failure_retention_unsealed.json",
                    {
                        "passed": False,
                        "budget_censored": True,
                        "hard_terminal_reserve_exhausted": True,
                        "partial_files_preserved": True,
                        "all_bytes_manifest_not_certified": True,
                        "fixed_receipt_terminal_no_retry": True,
                        "new_test_credit": 0,
                    },
                )
        raise
    print(
        "WAVE10 reconciled; strict live integrity false; historical identity gap retained",
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    run(parser.parse_args().output)
