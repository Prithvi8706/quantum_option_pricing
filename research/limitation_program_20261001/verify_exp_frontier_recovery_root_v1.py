"""Fresh A13 recovery receipt integrity only; no scientific import or evaluation.

Prospective fixed120 process CPU/90 work admission/600 wall, one thread,
24k runtime files/2GiB,100k references/8GiB union/24GiB byte hashing.
Architecture copied from immutable verify_exp_frontier_allocation_root_v2.py,
SHA b0aac76928ad41a48cb1884d14f76168d8ef783595f918177857e5b13a91861f.
Caches only actual confined resolutions and observed byte hashes
under unchanged full stat/reparse identity. BOTH unique union passes still
freshly resolve every member and fully hash its bytes; no expected SHA override.
Root executes this NEW file only after static review and exact-byte freezing.
The thin producer certifies metadata only. Mathematical approval is reported
only as the actual independently executed130 auditor's all20 indexed result.
Gzip compressed bytes/header are verified without decompression or proof reuse.
Uncompressed size/hash remain the pinned auditor's metadata, not a ROOT reproof.
"""

import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
PROGRAM = ROOT / "results/limitation_program_20261001"
OUTPUT = PROGRAM / "A13_recovery_root_verification_run001"
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
SOURCE = PROGRAM / "A13_recovery_run001"
AUDIT = PROGRAM / "A13_recovery_audit_run004"
FAILED = PROGRAM / "A13_run001"
MATERIAL = PROGRAM / "A13_run002"
ORIGIN = RESEARCH / "verify_exp_frontier_allocation_root_v2.py"
ORIGIN_SHA = "b0aac76928ad41a48cb1884d14f76168d8ef783595f918177857e5b13a91861f"
SOURCE_SHA = "e3c23aaa0697727952a7c979503424146c0224e8b2c8c32cff652974ab557dc9"
AUDIT_SHA = None  # Root supplies only the actual sealed independent terminal PASS pin.
FAILURE_DIAGNOSTIC = PROGRAM / "A13_terminal_failure_capture_run002"
FAILURE_DIAGNOSTIC_SHA = "20126972220fc8ae35aae71e789e96b4dde6b755b9c692c97b4e89dfdb9285c3"
CPU, ADMISSION, WALL = 120, 90, 600
MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = 24000, 2 * 1024**3
MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK = 100000, 8 * 1024**3, 24 * 1024**3
AUTHORS = {
    "A13_EXP_FRONTIER_RECOVERY_PREFLIGHT.md": (
        "2d86febd3e35963e051113da6490b5e8ed352b7be10c79e6d8187cdf8950b747"
    ),
    "a13_exp_frontier_recovery_preflight.json": (
        "c36d9c97266144a73373c1dd55922585a2271206d0a5cc1ddf0f42ddaa9ce291"
    ),
    "experiment_exp_frontier_recovery.py": (
        "9a83c9ed87df61415af94b1ee15840c97714f48c90bebcf2c1d0b1367d79b8d9"
    ),
    "audit_exp_frontier_recovery.py": (
        "e10184be6b451dff12f01e74aa67786c116a089ac814e42df542e63d0449e6ed"
    ),
    "A13_EXP_FRONTIER_RECOVERY_IMPLEMENTATION_PREFLIGHT.md": (
        "b44deaeca4d2a39fdb88e484bc85c3575d45aea8a805aaf953b049bb3bddc2a3"
    ),
    "a13_exp_frontier_recovery_implementation_preflight.json": (
        "926b787958e8a482fb707d209b6f4284ecc389b2fabfd648a3e37873e3871986"
    ),
}
SOURCE_AUTHORS = AUTHORS
AUDIT_V2_AUTHORS = {
    "audit_exp_frontier_recovery_v2.py": (
        "411930cf13eaf4a61b7f5d9e3e34870644fa2960a7d8d18afef90e26672a31af"
    ),
    "A13_EXP_FRONTIER_RECOVERY_AUDIT_IMPLEMENTATION_PREFLIGHT_V2.md": (
        "8731ab0d15e12a590aa0c9ebdabf7bb696ceb780630d281ebea2f86b0a2fec44"
    ),
    "a13_exp_frontier_recovery_audit_implementation_preflight_v2.json": (
        "a559e03871cc5295401843fc011bca581fc6bd4e9e23aa23785032eef6cc5aea"
    ),
}
AUDIT_V3_AUTHORS = {
    "audit_exp_frontier_recovery_v3.py": (
        "f094a5bd4738735bfae4775b6149fc354a9a15bad7e28850811aa1f0f27d7a3c"
    ),
    "A13_EXP_FRONTIER_RECOVERY_AUDIT_IMPLEMENTATION_PREFLIGHT_V3.md": (
        "66df965afd04126ebdd3bf742676fbe12c5944626bd03201cc9e0a92e29e10ff"
    ),
    "a13_exp_frontier_recovery_audit_implementation_preflight_v3.json": (
        "479cd7b015ba530abcd1b73099cfdca1e9ebed976c316a8ebe6943dc9da99cd1"
    ),
}
NEW_AUDIT_AUTHORS = {
    "audit_exp_frontier_recovery_v4.py": (
        "61c05812abd7c7c042ab654a025e14b96afcfff00afd5398e72ea334307d07ba"
    ),
    "A13_EXP_FRONTIER_RECOVERY_AUDIT_IMPLEMENTATION_PREFLIGHT_V4.md": (
        "75b962da0239f371f34bc4c675243fba29b504038a68975a6b347fa0596af3f5"
    ),
    "a13_exp_frontier_recovery_audit_implementation_preflight_v4.json": (
        "8b1bf237dd2739fdbfe59c5af4cd2bf776dc29ce198d02dcf8c900bedae1e1ea"
    ),
}
DP_AUTHORS = {
    "A13_EXP_FRONTIER_RECOVERY_DP_OPTIMIZATION_PREFLIGHT_V4.md": (
        "86e0185742c7ae425372675806dad6da772e0303ca0d1d8fab1d8a59eb7c717c"
    ),
    "a13_exp_frontier_recovery_dp_optimization_preflight_v4.json": (
        "5a98e3e210b3e4911b7b00042504f22a1ba406fe97e0b5e286904c741d2d53fd"
    ),
    "verify_a13_recovery_dp_equivalence_v4.py": (
        "13b23612efd580e6af38258a09536af86073828ca17869cffcb2b13ff860884d"
    ),
}
VALIDATION = PROGRAM / "A13_recovery_DP_equivalence_check_run001"
VALIDATION_SHA = "cea188580eefe2d4a64c73890385c482b3264dba7a1afef3d2cf8d5f3ea25a4b"
NEW_AUDIT_REVIEW = "A13_recovery_root_review_run004"
NEW_AUDIT_REVIEW_SHA = "c427b46bf39133fddbccc2d9022d14d8756545885f7a4279e788a3fbc04dec1a"
NEW_AUDIT_REVIEW_FROZEN_COUNT = 37
GRID = tuple((d, s) for d in (4, 6, 8, 10, 12) for s in (1, 2, 4, 8))
FAILED_AUDIT = PROGRAM / "A13_recovery_audit_run001"
FAILED_AUDIT_SHA = "2770a360c67ba6ee5c1df720679a6376679f5efcaba91052683af698cfb66c72"
FAILED_AUDIT_V2 = PROGRAM / "A13_recovery_audit_run002"
FAILED_AUDIT_V2_SHA = "ba3b0715f9ee994c157e7422e12919b808916105f6ab1a1b8350017b7ceb9dcd"
FAILED_AUDIT_V3 = PROGRAM / "A13_recovery_audit_run003"
FAILED_AUDIT_V3_SHA = "753ffde46904f2b4995efbdcb42b89161386e9267108179f9b0cc9dfe9a14551"
PREREQUISITES = {
    "A13_terminal_failure_capture_run002": FAILURE_DIAGNOSTIC_SHA,
    "A13_recovery_root_review_run001": (
        "2aac4a58ed85fc672a9a83fb9cae555534287a3998edf42ea28a57cf66cd77b6"
    ),
    "A13_run001": "d77077cfb2d67ee2973a02b236ea6e6b2336962f35fed6ce4aeb48ef8bb65aa8",
    "A13_exp_frontier_root_review_run001": (
        "744e04e887ef94a218004845a8655014389cc2f4cf5d4d41153c352d7db4ebce"
    ),
    "A13_exp_frontier_root_review_run002": (
        "6834a90acb76a5489f3fac66ce874adf81357692ba2bade7cd709455846626e3"
    ),
    "A13_recovery_audit_run001": FAILED_AUDIT_SHA,
    "A13_recovery_audit_run002": FAILED_AUDIT_V2_SHA,
    "A13_recovery_audit_run003": FAILED_AUDIT_V3_SHA,
    "A13_recovery_root_review_run002": (
        "47a49e01e1395d21a3d08873ebfee9b17906bd0f48184c89e0614f5b075fefb2"
    ),
    "A13_recovery_root_review_run003": (
        "0108b046dcf9ebf55a85926d68f8e7d02036e039f9966d654e1773df61de96a6"
    ),
}
FAILURE_NAMES = (
    "FAILED_UNSEALED.json",
    "failed_unsealed.json",
    "failure.json",
    "run_failure.json",
    "prepare_failure.json",
)
_FROZEN, _EXTERNAL, _OBSERVED, _PACKETS = {}, {}, {}, {}
_HASH_WORK = _REFERENCES = 0
_STARTED = None
_OWN_INVENTORIES, _ABSENT_RUNTIME = {}, set()
_ABSENT_HISTORICAL = set()
_PATH_CACHE, _HASH_CACHE = {}, {}
_BASE_SCOPE, _EXCLUDED_SCOPE = None, None


def require(condition, message):
    if not condition:
        raise ValueError(message)


def process_started():
    require(os.name == "nt" and ctypes.sizeof(ctypes.c_void_p) == 8, "Pinned Win64")
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.GetCurrentProcess.argtypes = []
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
    kernel.GetProcessTimes.restype = wintypes.BOOL
    stamps = [wintypes.FILETIME() for _ in range(4)]
    require(
        kernel.GetProcessTimes(
            kernel.GetCurrentProcess(), *[ctypes.byref(stamp) for stamp in stamps]
        ),
        "Actual process creation clock",
    )
    ticks = (stamps[0].dwHighDateTime << 32) | stamps[0].dwLowDateTime
    age_ns = time.time_ns() - (ticks - 116444736000000000) * 100
    require(age_ns >= 0, "Actual UTC creation precedes observation")
    # GetCurrentProcess is a pseudo-handle, never an owned handle to close.
    return time.monotonic() - age_ns / 1_000_000_000


def budget(admission=False):
    require(time.process_time() < (ADMISSION if admission else CPU), "Process CPU guard")
    require(time.monotonic() - _STARTED < WALL, "Creation-derived wall guard")


def runtime_scopes():
    global _BASE_SCOPE, _EXCLUDED_SCOPE
    budget()
    lexical = Path(os.path.abspath(sys.base_prefix))
    actual = lexical.resolve(strict=True)
    require(actual == lexical, "Actual base prefix has no alias")
    excluded = lexical / "Lib/site-packages"
    physical_excluded = excluded.resolve(strict=False)
    scopes = (actual, (excluded, physical_excluded))
    if _BASE_SCOPE is not None:
        require(scopes == (_BASE_SCOPE, _EXCLUDED_SCOPE), "Actual runtime scopes unchanged")
    _BASE_SCOPE, _EXCLUDED_SCOPE = scopes
    budget()


def canonical(path, fresh=False):
    budget()
    path = Path(path)
    require(not path.drive or path.is_absolute(), "No ambiguous drive-relative input")
    lexical = Path(os.path.abspath(str(path)))
    require(
        not any(lexical.is_relative_to(scope) for scope in _EXCLUDED_SCOPE),
        "Excluded base packages lexical path",
    )
    key = str(lexical)
    if not fresh and key in _PATH_CACHE:
        cached, identity = _PATH_CACHE[key]
        if fingerprint(lexical) == identity:
            budget()
            return cached
    actual = lexical.resolve(strict=True)
    require(
        not any(actual.is_relative_to(scope) for scope in _EXCLUDED_SCOPE),
        "Excluded base package alias",
    )
    require(actual == lexical, "No lexical-to-physical input alias")
    require(
        key not in _PATH_CACHE or _PATH_CACHE[key][0] == actual,
        "Previously confined lexical input did not redirect",
    )
    _PATH_CACHE[key] = (actual, fingerprint(lexical))
    budget()
    return actual


def fingerprint(path):
    stat = path.stat()
    return tuple(
        getattr(stat, name, None)
        for name in (
            "st_dev",
            "st_ino",
            "st_size",
            "st_mtime_ns",
            "st_ctime_ns",
            "st_mode",
            "st_file_attributes",
            "st_reparse_tag",
        )
    )


def digest(path, fresh=False, already_resolved=False):
    global _HASH_WORK
    budget()
    path = path if already_resolved else canonical(path, fresh=fresh)
    require(path.is_file(), "Actual regular SHA input")
    before, total, state = fingerprint(path), 0, hashlib.sha256()
    if not fresh and path in _HASH_CACHE and _HASH_CACHE[path][0] == before:
        budget()
        return _HASH_CACHE[path][1]
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            budget()
            total += len(chunk)
            _HASH_WORK += len(chunk)
            require(_HASH_WORK <= MAX_HASH_WORK, "Fixed24GiB hashing-work cap")
            require(total <= before[2], "Input grew while hashing")
            state.update(chunk)
    require(total == before[2] and fingerprint(path) == before, "Stable actual byte hash")
    result = state.hexdigest()
    require(
        path not in _OBSERVED or _OBSERVED[path] == result, "Previously observed bytes unchanged"
    )
    _OBSERVED.setdefault(path, result)
    _HASH_CACHE[path] = (before, result)
    budget()
    return result


def add(path, expected):
    global _REFERENCES
    budget()
    _REFERENCES += 1
    require(_REFERENCES <= MAX_REFERENCES, "Fixed100k map-reference cap")
    require(
        type(expected) is str
        and len(expected) == 64
        and all(char in "0123456789abcdef" for char in expected),
        "Exact expected SHA",
    )
    actual = canonical(path)
    require(actual.is_file(), "Regular preserved input")
    if actual.is_relative_to(ROOT):
        key, mapping = actual.relative_to(ROOT).as_posix(), _FROZEN
    else:
        require(actual.is_relative_to(_BASE_SCOPE), "Actual external base runtime")
        key, mapping = str(actual), _EXTERNAL
    require(key not in mapping or mapping[key] == expected, "Canonical equal-SHA expectations")
    mapping[key] = expected
    return actual


def read(path):
    global _HASH_WORK
    budget()
    path = canonical(path)
    before = fingerprint(path)
    require(path.is_file() and before[2] <= 128 * 1024**2, "Bounded regular JSON input")
    chunks, total, state = [], 0, hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            budget()
            total += len(chunk)
            _HASH_WORK += len(chunk)
            require(_HASH_WORK <= MAX_HASH_WORK and total <= before[2], "Bounded JSON reads")
            chunks.append(chunk)
            state.update(chunk)
    require(total == before[2] and fingerprint(path) == before, "Stable JSON bytes")
    expected = (
        _FROZEN.get(path.relative_to(ROOT).as_posix())
        if path.is_relative_to(ROOT)
        else _EXTERNAL.get(str(path))
    )
    observed = state.hexdigest()
    require(expected is not None and observed == expected, "JSON belongs to exact admitted SHA")
    require(path not in _OBSERVED or _OBSERVED[path] == observed, "Stable observed JSON SHA")
    _OBSERVED[path] = observed
    _HASH_CACHE[path] = (before, observed)
    budget()
    result = json.loads(b"".join(chunks))
    budget()
    return result


def no_failure(directory):
    require(
        not any((directory / name).exists() for name in FAILURE_NAMES),
        "Authoritative failure marker prohibits admission",
    )


def inventory(directory):
    found, total = set(), 0
    for root, dirs, names in os.walk(directory, followlinks=False):
        budget()
        for name in dirs:
            candidate = Path(root) / name
            require(canonical(candidate).is_relative_to(directory), "No owned directory escape")
            require(not candidate.is_symlink(), "No owned directory link")
        for name in names:
            actual = canonical(Path(root) / name)
            require(actual.is_relative_to(directory) and actual not in found, "Unique owned path")
            require(actual.is_file(), "Regular actual owned entry")
            found.add(actual)
            total += actual.stat().st_size
            require(len(found) <= 25000 and total <= MAX_UNIQUE_BYTES, "Finite owned inventory")
    return found


def packet(name, expected):
    directory = canonical(PROGRAM / name)
    preserved_failure = directory in (FAILED, FAILED_AUDIT, FAILED_AUDIT_V2, FAILED_AUDIT_V3)
    if not preserved_failure:
        no_failure(directory)
    mf_path = add(directory / "manifest.json", expected)
    mf = read(mf_path)
    require(mf.get("manifest_self_hash_excluded") is True, "Exact self-hash exclusion")
    owned, frozen, external = (
        mf.get(key, {}) for key in ("files", "frozen_inputs", "external_runtime_inputs")
    )
    require(
        type(owned) is dict and owned and type(frozen) is dict and type(external) is dict,
        "Complete recognized owned/frozen/external maps",
    )
    actual_owned = set()
    for original, expected_sha in owned.items():
        budget()
        require(type(original) is str and not Path(original).is_absolute(), "Relative own key")
        key = original.replace("\\", "/")
        candidate = ROOT / key if key.startswith("results/") else directory / key
        actual = add(candidate, expected_sha)
        require(actual.is_relative_to(directory) and actual != mf_path, "Owned receipt confinement")
        require(actual not in actual_owned, "No duplicate own alias")
        actual_owned.add(actual)
        parent = ROOT if key.startswith("results/") else directory
        require(key == actual.relative_to(parent).as_posix(), "Exact canonical owned key")
    for original, expected_sha in frozen.items():
        budget()
        require(type(original) is str and not Path(original).is_absolute(), "ROOT frozen key")
        key = original.replace("\\", "/")
        actual = add(ROOT / key, expected_sha)
        require(
            actual.is_relative_to(ROOT) and actual.relative_to(ROOT).as_posix() == key,
            "Canonical ROOT frozen input",
        )
    for key, expected_sha in external.items():
        budget()
        require(type(key) is str and Path(key).is_absolute(), "Explicit scoped external key")
        actual = add(key, expected_sha)
        require(not actual.is_relative_to(ROOT) and str(actual) == key, "Canonical external key")
    exact_owned = actual_owned | {mf_path}
    require(inventory(directory) == exact_owned, "Exact actual owned membership")
    _OWN_INVENTORIES[directory] = exact_owned
    summary = read(directory / "summary.json") if (directory / "summary.json").is_file() else None
    outcome = (
        read(directory / "completion_outcome.json")
        if (directory / "completion_outcome.json").is_file()
        else None
    )
    if preserved_failure:
        counts = {
            FAILED: [13, 832, 2842],
            FAILED_AUDIT: [19, 931, 2842],
            FAILED_AUDIT_V2: [20, 957, 2842],
            FAILED_AUDIT_V3: [35, 984, 2842],
        }[directory]
        require(
            [len(owned), len(frozen), len(external)] == counts and expected == PREREQUISITES[name],
            "Exact original failed packet maps",
        )
        require(
            mf["completed"] is False
            and mf["passed"] is False
            and mf["budget_censored"] is (directory == FAILED_AUDIT_V3)
            and outcome["completed"] is False
            and outcome["passed"] is False
            and outcome["failed"] is True
            and outcome["budget_censored"] is (directory == FAILED_AUDIT_V3)
            and outcome["new_test_credit"] == 0
            and outcome["limits_CPU_admission_wall"] == [300, 270, 900]
            and (directory / "failure.json").is_file(),
            "Sealed original failures retain exact censor classification and zero credit",
        )
        if directory == FAILED_AUDIT_V3:
            failure = read(directory / "failure.json")
            require(
                failure["error_type"] == "BudgetCensoredError"
                and failure["error"] == "Fixed independent A13 CPU/wall censor"
                and failure["new_test_credit"] == 0
                and 270 <= failure["budget"]["process_CPU_seconds"] < 300
                and "audit_fit_segment" in failure["traceback"],
                "Actual failed003 admission censor is not a mathematical rejection or PASS",
            )
            require(
                sorted(
                    member.relative_to(directory).as_posix()
                    for member in actual_owned
                    if member.is_relative_to(directory / "rows")
                )
                == sorted(f"rows/d{degree}_s{count}.json.gz" for degree, count in GRID[:14]),
                "All fourteen failed003 partial gzip rows remain failure-only provenance",
            )
            _ABSENT_HISTORICAL.update(
                (directory / "summary.json", directory / "fixed_inventory_authorization.json")
            )
            require(not any(p.exists() for p in _ABSENT_HISTORICAL), "No promoted old audit PASS")
    elif directory == VALIDATION:
        require(
            expected == VALIDATION_SHA
            and [len(owned), len(frozen), len(external)] == [2, 3, 0]
            and mf["schema"] == "a13-recovery-exact-dp-finite-equivalence-manifest-v1"
            and mf["completed"] is True
            and mf["passed"] is True
            and mf["new_test_credit"] == 0,
            "Actual fixed finite-selector QA packet only",
        )
        require(
            summary["schema"] == "a13-recovery-exact-dp-finite-equivalence-summary-v1"
            and summary["completed"] is True
            and summary["passed"] is True
            and summary["fixed_case_count"] == 16
            and summary["subsets_enumerated"] == 240
            and summary["all_cases_equal_independent_exhaustive_subset_oracle"] is True
            and summary["legacy_fraction_reference_also_equal"] is True
            and summary["old_and_new_auditor_modules_imported"] is False
            and summary["source_corpus_or_fitting_replayed"] is False
            and summary["all20_scientific_screen_approved"] is False
            and summary["new_test_credit"] == summary["new_gate_replays"] == 0
            and summary["new_price_samples"] == 0
            and summary["gate_emission_authorized"] is False
            and summary["adoption"] is False
            and summary["candidate_G2_established"] is False
            and summary["limits_CPU_work_wall_seconds"] == [10, 8, 30]
            and 0 <= summary["actual_process_CPU_seconds"] < 10
            and 0 <= summary["actual_creation_wall_seconds"] < 30,
            "Finite QA must never substitute for the actual all20 independent audit",
        )
        records = read(directory / "finite_equivalence_results.json")
        require(
            type(records) is list
            and len(records) == len({row["case"] for row in records}) == 16
            and sum(row["subsets_enumerated"] for row in records) == 240
            and all(
                row["both_selectors_equal_exhaustive_oracle"] is True
                and 2 <= row["candidate_locations"] <= 8
                and 1 <= row["length"] <= 6
                for row in records
            ),
            "Actual QA's sixteen distinct bounded selector queries are integrity-only evidence",
        )
        require(
            frozen
            == {
                (RESEARCH / "audit_exp_frontier_recovery_v3.py").relative_to(ROOT).as_posix():
                AUDIT_V3_AUTHORS["audit_exp_frontier_recovery_v3.py"],
                (RESEARCH / "audit_exp_frontier_recovery_v4.py").relative_to(ROOT).as_posix():
                NEW_AUDIT_AUTHORS["audit_exp_frontier_recovery_v4.py"],
                (RESEARCH / "verify_a13_recovery_dp_equivalence_v4.py").relative_to(ROOT).as_posix():
                DP_AUTHORS["verify_a13_recovery_dp_equivalence_v4.py"],
            },
            "Exact frozen old/new selector and independent validation source bytes",
        )
    elif directory == FAILURE_DIAGNOSTIC:
        require(
            expected == FAILURE_DIAGNOSTIC_SHA
            and [len(owned), len(frozen), len(external)] == [3, 891, 2842],
            "Exact failed-material diagnostic maps",
        )
        require(
            summary["passed"] is True
            and summary["diagnostic_integrity"] is True
            and summary["original_attempt_failed"] is True
            and summary["original_partial_success_invalid"] is True
            and summary["original_owned_files"] == 42
            and summary["original_owned_bytes"] == 243935317
            and summary["original_receipt"] == MATERIAL.relative_to(ROOT).as_posix()
            and summary["new_fixture_credit"] == summary["new_gate_replays"] == 0
            and summary["scientific_import_or_evaluation_executed"] is False
            and summary["mathematical_result_or_candidate_adoption_claim"] is False
            and summary["all_old_expected_hashes_retained"] is True,
            "Diagnostic certifies failed original bytes only",
        )
        require(
            outcome["completed"] is True
            and outcome["passed"] is True
            and outcome["diagnostic_integrity"] is True
            and outcome["original_attempt_failed"] is True
            and outcome["new_fixture_credit"] == 0
            and 0 <= outcome["process_CPU_seconds"] < 300
            and 0 <= outcome["wall_seconds"] < 900,
            "Actual bounded diagnostic integrity outcome",
        )
    elif directory in (SOURCE, AUDIT):
        if directory == SOURCE:
            require(
                [len(owned), len(frozen), len(external)] == [16, 909, 2842],
                "Exact unchanged thin metadata producer maps",
            )
        owned_bytes = 0
        for member in actual_owned:
            budget()
            owned_bytes += member.stat().st_size
        require(
            len(actual_owned) <= 64 and owned_bytes <= 128 * 1024**2,
            "Original fresh recovery source/audit owned artifact caps",
        )
        for value in (mf, outcome, summary):
            require(
                type(value) is dict
                and value.get("completed") is True
                and value.get("passed") is True
                and value.get("budget_censored") is False
                and value.get("failed", False) is False
                and value.get("rejection", False) is False,
                "Complete uncensored actual terminal PASS",
            )
        require(
            outcome["limits_CPU_admission_wall"] == [300, 270, 900],
            "Original fixed recovery process contract",
        )
    else:
        review_counts = {
            "A13_recovery_root_review_run001": [1, 17, 0],
            "A13_recovery_root_review_run002": [1, 23, 0],
            "A13_recovery_root_review_run003": [1, 28, 0],
            NEW_AUDIT_REVIEW: [1, NEW_AUDIT_REVIEW_FROZEN_COUNT, 0],
        }
        if name in review_counts:
            require(
                [len(owned), len(frozen), len(external)] == review_counts[name],
                "Exact original metadata source versus new audit-only static review maps",
            )
        require(
            summary["passed"] is True
            and summary["new_fixture_credit"] == 0
            and summary.get("new_scientific_execution_during_review", False) is False,
            "Static root/peer release, zero scientific credit",
        )
    if outcome is not None and directory != FAILURE_DIAGNOSTIC:
        for observation in (outcome["budget"], mf["terminal_budget_observation"]):
            require(
                0 <= observation["process_CPU_seconds"] < 300
                and 0 <= observation["wall_seconds"] < 900,
                "Original terminal hard budgets",
            )
    _PACKETS[name] = {
        "files": len(owned),
        "frozen_inputs": len(frozen),
        "external_runtime_inputs": len(external),
        "preserved_failure": preserved_failure,
    }
    return summary, outcome, mf


def retained_material():
    diagnostic = read(FAILURE_DIAGNOSTIC / "summary.json")
    index = read(FAILURE_DIAGNOSTIC / "frozen_reference_index.json")
    source_inventory = read(SOURCE / "material_inventory.json")
    require(type(index) is dict and len(index) == 42, "Exactly42 old immutable members")
    require(
        set(index) == set(diagnostic["preserved_members"])
        and source_inventory["exact_file_count"] == 42
        and source_inventory["original_file_bytes"] == 243935317
        and source_inventory["capture_manifest_SHA256"] == FAILURE_DIAGNOSTIC_SHA
        and source_inventory["original_terminal_failure_authoritative"] is True
        and source_inventory["original_manifest_absent"] is True
        and source_inventory["original_independent_audit_absent"] is True,
        "Same independently retained failed material",
    )
    actual, total, table = set(), 0, {}
    for key, pin in index.items():
        budget()
        member = add(ROOT / key, pin)
        require(
            member.is_relative_to(MATERIAL) and member.relative_to(ROOT).as_posix() == key,
            "Exact old material owner key",
        )
        actual.add(member)
        size = member.stat().st_size
        total += size
        table[member.relative_to(MATERIAL).as_posix()] = {
            "ROOT_relative_path": key,
            "sha256": pin,
            "bytes": size,
        }
    require(
        inventory(MATERIAL) == actual and total == 243935317 and source_inventory["files"] == table,
        "Every original42 file preserved with exact sizes/SHAs",
    )
    _OWN_INVENTORIES[MATERIAL] = actual
    _ABSENT_HISTORICAL.update((MATERIAL / "manifest.json", PROGRAM / "A13_audit_run002"))
    require(not any(p.exists() for p in _ABSENT_HISTORICAL), "No invented original success/audit")
    marker = read(MATERIAL / "FAILED_UNSEALED.json")
    require(
        marker == diagnostic["original_failure_marker"]
        and marker["failed"] is True
        and marker["passed"] is False
        and marker["completed"] is False
        and marker["budget_censored"] is True
        and marker["new_test_credit"] == 0
        and marker["partial_summary_or_manifest_is_not_terminal_success"] is True,
        "Old failed-unsealed marker overrides partial summary/completion",
    )
    protocol = read(MATERIAL / "protocol.json")
    require(
        protocol["schema"] == "a13-exp-frontier-protocol-v1"
        and protocol["operational_A13_version"] == 2
        and protocol["CPU_admission_wall_seconds"] == [300, 270, 900]
        and len(protocol["frozen_inputs"]) == 848
        and len(protocol["external_runtime_inputs"]) == 2842,
        "Complete original prepared maps, never a mathematical PASS",
    )
    for original, pin in protocol["frozen_inputs"].items():
        budget()
        actual = add(ROOT / original, pin)
        require(actual.relative_to(ROOT).as_posix() == original, "Exact original ROOT map")
    for original, pin in protocol["external_runtime_inputs"].items():
        budget()
        actual = add(original, pin)
        require(str(actual) == original and not actual.is_relative_to(ROOT), "Original base map")
    original_inventory = read(MATERIAL / "fixed_inventory.json")
    expected = [dict(degree=d, segments=s, row_id=f"d{d}_s{s}") for d, s in GRID]
    require(
        original_inventory["schema"] == "a13-fixed-inventory-v1"
        and original_inventory["rows"] == expected
        and original_inventory["no_adaptive_degrees_segments_or_precision"] is True
        and original_inventory["separate_original_baseline"]
        == dict(degree=12, segments=1, new_degree12_fit_is_not_original_baseline=True),
        "All20 preregistered choices with a separate original baseline",
    )


def method_checks():
    method = read(RESEARCH / "a13_exp_frontier_recovery_preflight.json")
    implementation = read(RESEARCH / "a13_exp_frontier_recovery_implementation_preflight.json")
    require(
        method["schema"] == "a13-exp-frontier-recovery-author-preflight-v1"
        and method["fixed_grid"] == [list(pair) for pair in GRID]
        and method["primary_digits"] == 90
        and method["independent_digits"] == 130
        and method["primary_Taylor_order"] == 80
        and method["independent_Taylor_order"] == 112
        and method["CPU_admission_wall_seconds"] == [300, 270, 900]
        and method["threads"] == 1
        and method["original_material_files"] == 42
        and method["capture_manifest_SHA256"] == FAILURE_DIAGNOSTIC_SHA
        and method["candidate_material_untrusted"] is True
        and method["independent130_all20_validation_required"] is True
        and method["candidate_G2_absolute_stock_error_allocation"] is None
        and method["candidate_G2_barrier_band_allocation"] is None
        and method["gate_emission_authorized"] is False,
        "Unchanged held recovery contract",
    )
    for key in (
        "author_sha256",
        "method_document_SHA256",
        "original_method_document_SHA256",
        "prior_A13_author_SHA256",
        "prior_A13_v2_author_SHA256",
    ):
        for name, pin in implementation[key].items():
            add(RESEARCH / name, pin)
    old_review = read(PROGRAM / "A13_recovery_root_review_run001/summary.json")
    require(
        old_review["schema"] == "root-a13-exp-frontier-recovery-static-READY-v1"
        and old_review["passed"] is True
        and old_review["ready"] is True
        and old_review["root_and_independent_TEXT_static_reviews"] is True
        and old_review["Ruff_syntax_JSON_and_actual_pins_PASS"] is True
        and old_review["source_metadata_integrity_only"] is True
        and old_review["original_FAILED_UNSEALED_remains_authoritative"] is True
        and old_review["refit_authorized"] is False
        and old_review["candidate_G2_allocations"] is None
        and old_review["new_fixture_credit"] == 0,
        "Exact old producer release remains distinct from future v2 audit release",
    )
    protocol = read(SOURCE / "protocol.json")
    require(
        protocol["author_sha256"]
        == {
            name: SOURCE_AUTHORS[name]
            for name in ("experiment_exp_frontier_recovery.py", "audit_exp_frontier_recovery.py")
        }
        and protocol["primary_digits"] == 90
        and protocol["independent_digits"] == 130
        and protocol["fixed_grid"] == [list(pair) for pair in GRID]
        and protocol["CPU_admission_wall_seconds"] == [300, 270, 900]
        and protocol["new_fixture_credit"] == 0
        and protocol["candidate_material_untrusted"] is True
        and protocol["independent130_validation_required"] is True,
        "Original untrusted metadata producer's exact immutable pairing",
    )


def audit_only_release():
    names = {
        "audit_exp_frontier_recovery_v4.py",
        "A13_EXP_FRONTIER_RECOVERY_AUDIT_IMPLEMENTATION_PREFLIGHT_V4.md",
        "a13_exp_frontier_recovery_audit_implementation_preflight_v4.json",
    }
    require(set(NEW_AUDIT_AUTHORS) == names, "Exact new audit-only three author bindings")
    policy = read(RESEARCH / "a13_exp_frontier_recovery_audit_implementation_preflight_v4.json")
    pair = {
        name: SOURCE_AUTHORS[name]
        for name in ("experiment_exp_frontier_recovery.py", "audit_exp_frontier_recovery.py")
    }
    require(
        policy["schema"] == "a13-exp-frontier-recovery-audit-only-implementation-preflight-v4"
        and policy["author_sha256"]
        == {
            "audit_exp_frontier_recovery_v4.py": NEW_AUDIT_AUTHORS[
                "audit_exp_frontier_recovery_v4.py"
            ]
        }
        and policy["original_recovery_source_author_sha256"] == pair
        and policy["original_recovery_author_SHA256"] == SOURCE_AUTHORS
        and policy["source_manifest_SHA256"] == SOURCE_SHA
        and policy["prior_recovery_audit_failed_manifest_SHA256"] == FAILED_AUDIT_SHA
        and policy["prior_recovery_root_review_manifest_SHA256"]
        == PREREQUISITES["A13_recovery_root_review_run001"]
        and policy["prior_recovery_audit_v2_author_SHA256"] == AUDIT_V2_AUTHORS
        and policy["prior_recovery_audit_v2_failed_manifest_SHA256"] == FAILED_AUDIT_V2_SHA
        and policy["prior_recovery_audit_v2_root_review_manifest_SHA256"]
        == PREREQUISITES["A13_recovery_root_review_run002"]
        and policy["prior_recovery_audit_v3_author_SHA256"] == AUDIT_V3_AUTHORS
        and policy["prior_recovery_audit_v3_failed_manifest_SHA256"] == FAILED_AUDIT_V3_SHA
        and policy["prior_recovery_audit_v3_root_review_manifest_SHA256"]
        == PREREQUISITES["A13_recovery_root_review_run003"]
        and policy["exact_DP_optimization_method_document_SHA256"]
        == {name: pin for name, pin in DP_AUTHORS.items() if name.endswith((".md", ".json"))}
        and policy["original_source_owned_frozen_external_counts"] == [16, 909, 2842]
        and policy["failed_audit_owned_frozen_external_counts"] == [19, 931, 2842]
        and policy["original_root_review_owned_frozen_counts"] == [1, 17],
        "Original immutable source pair and failed audit remain separate from new auditor",
    )
    require(
        policy["implementation_receipt_route_override"]
        == {
            "source": SOURCE.relative_to(ROOT).as_posix(),
            "audit": AUDIT.relative_to(ROOT).as_posix(),
        }
        and policy["audit_only_versioning"] is True
        and policy["successful_metadata_source_reexecuted"] is False
        and policy["original_failed_audit_remains_failed"] is True
        and policy["previous_failed_audit_credit"] == 0
        and policy["original_partial_or_failed_mathematical_pass_promoted"] is False
        and policy["CPU_admission_wall_seconds"] == [300, 270, 900]
        and policy["fixed_grid"] == [list(value) for value in GRID]
        and policy["primary_digits"] == 90
        and policy["independent_digits"] == 130
        and policy["threads"] == 1,
        "Fresh auditor route with unchanged fixed scientific/operational scope",
    )
    protocol = read(AUDIT / "protocol.json")
    require(
        protocol["schema"] == "a13-exp-frontier-recovery-independent-audit-protocol-v1"
        and protocol["operational_recovery_audit_version"] == 4
        and protocol["source"] == SOURCE.relative_to(ROOT).as_posix()
        and protocol["output"] == AUDIT.relative_to(ROOT).as_posix()
        and protocol["author_sha256"] == policy["author_sha256"]
        and protocol["original_recovery_source_author_sha256"] == pair
        and protocol["original_recovery_author_SHA256"] == SOURCE_AUTHORS
        and protocol["source_manifest_SHA256"] == SOURCE_SHA
        and protocol["source_manifest_sha256"] == SOURCE_SHA
        and protocol["prior_recovery_audit_failed_manifest_SHA256"] == FAILED_AUDIT_SHA
        and protocol["prior_recovery_audit_v2_author_SHA256"] == AUDIT_V2_AUTHORS
        and protocol["prior_recovery_audit_v2_failed_manifest_SHA256"] == FAILED_AUDIT_V2_SHA
        and protocol["prior_recovery_audit_v2_root_review_manifest_SHA256"]
        == PREREQUISITES["A13_recovery_root_review_run002"]
        and protocol["prior_recovery_audit_v3_author_SHA256"] == AUDIT_V3_AUTHORS
        and protocol["prior_recovery_audit_v3_failed_manifest_SHA256"] == FAILED_AUDIT_V3_SHA
        and protocol["prior_recovery_audit_v3_root_review_manifest_SHA256"]
        == PREREQUISITES["A13_recovery_root_review_run003"]
        and protocol["exact_DP_optimization_method_document_SHA256"]
        == policy["exact_DP_optimization_method_document_SHA256"]
        and protocol["metadata_source_not_mathematical_PASS"] is True
        and protocol["CPU_admission_wall_seconds"] == [300, 270, 900]
        and protocol["primary_digits"] == 90
        and protocol["independent_digits"] == 130
        and protocol["threads"] == 1
        and protocol["startup_B_required"] is True
        and protocol["pure_Python_mpmath_backend_required"] is True,
        "Actual executed audit-only release and original source provenance",
    )
    for name, pin in NEW_AUDIT_AUTHORS.items():
        copied = (AUDIT / "executed_code" / name).relative_to(ROOT).as_posix()
        require(_FROZEN.get(copied) == pin, "Actual new auditor/preflight copied byte pin")
    for name, pin in DP_AUTHORS.items():
        if name.endswith((".md", ".json")):
            copied = (AUDIT / "executed_code" / name).relative_to(ROOT).as_posix()
            require(_FROZEN.get(copied) == pin, "Actual fixed integer-DP prospectus copy pin")


def check_release(source, audit, audit_manifest):
    global _HASH_WORK
    for value in (source, read(SOURCE / "completion_outcome.json")):
        require(
            value["metadata_integrity"] is True
            and value["candidate_material_untrusted"] is True
            and value["independent130_validation_required"] is True
            and value["scientific_screen_complete"] is False
            and value["recovered_mathematical_pass_claim"] is False
            and value["new_test_credit"] == 0,
            "Thin producer PASS certifies metadata, not mathematics",
        )
    require(
        source["original_attempt_still_failed"] is True
        and source["original_partial_success_invalid"] is True
        and source["old_summary_or_completion_promoted"] is False
        and source["original_mathematics_refitted_or_reexecuted"] is False
        and source["capture_manifest_SHA256"] == FAILURE_DIAGNOSTIC_SHA,
        "No promotion or rerun of the failed primary",
    )
    require(
        audit["schema"] == "a13-exp-frontier-recovery-independent-audit-summary-v1"
        and audit["independent_audit_passed"] is True
        and audit["metadata_source_passed"] is True
        and audit["scientific_screen_complete"] is True
        and audit["failed_original_source_mathematical_PASS"] is False
        and audit["all_untrusted_claimed_rows_independently_recertified"] is True
        and audit["original_failure_remains_authoritative_zero_credit"] is True
        and audit["capture_manifest_sha256"] == FAILURE_DIAGNOSTIC_SHA
        and audit["source_manifest_sha256"] == SOURCE_SHA
        and audit["fixed_architecture_rows"] == 20,
        "New actual audit is the sole mathematical authority for recovered material",
    )
    require(
        audit["operational_recovery_audit_version"] == 4
        and audit["prior_failed_recovery_audit_credit"] == 0,
        "Actual separately versioned auditor preserves prior failed audits at zero credit",
    )
    require(
        audit["prior_failed_recovery_audit_v2_credit"] == 0,
        "Auditor explicitly keeps failed002 at zero credit",
    )
    require(
        audit["prior_failed_recovery_audit_v3_credit"] == 0
        and audit["exact_dyadic_integer_two_pass_prefix_selection"] is True
        and audit["selection_objective_or_declared_transcript_changed"] is False
        and audit["old_censored_proof_rows_promoted_or_reused"] is False,
        "Fresh V4 authorizations never promote the fourteen failed003 rows",
    )
    for flag in (
        "every_claimed_primary80_uniform_bound_authorized_by_independent130",
        "independent112_uniform_witnesses_retained_separately",
        "exact_finite_fitting_transcript_and_single_tie_even_quantization_checked",
        "all_claimed_native_intermediate72_product144_and_shift_guards_independently_recomputed",
        "all_claimed_selector_QROM_argument_output_copies_banks_and_cleanup_costs_independently_reconstructed",
        "global_financial_forward_and_inverse_clean_function_invocations_paid",
        "symbolic_resources_not_actual_source_or_capped_schedule",
    ):
        require(audit[flag] is True, "Actual independent approval: " + flag)
    for summary in (source, audit):
        require(
            summary["candidate_G2_absolute_stock_error_allocation"] is None
            and summary["candidate_G2_barrier_band_allocation"] is None
            and summary["gate_emission_authorized"] is False
            and summary["full_G2"] is False
            and summary["adoption"] is False
            and summary["cost_transfer"] is False
            and summary["new_test_credit"] == 0,
            "Exploratory result, no candidate allocation/emission/adoption",
        )
    require(
        audit["new_gate_replays"] == audit["new_price_samples"] == 0
        and audit["feasible_architecture_or_realized_cost_improvement_claim"] is False
        and audit["scientific_producer_or_helper_imports"] is False
        and audit["source_expected_hashes_waived"] is False,
        "No scientific reexecution, realized resource claim or expected-hash waiver",
    )
    outcome = read(AUDIT / "completion_outcome.json")
    require(
        outcome["independent_audit_passed"] is True
        and outcome["metadata_source_passed"] is True
        and outcome["scientific_screen_complete"] is True
        and outcome["gate_emission_authorized"] is False
        and outcome["new_test_credit"] == 0,
        "Authoritative new independent terminal outcome",
    )
    authorization = read(AUDIT / "fixed_inventory_authorization.json")
    require(
        authorization["original_baseline_retained_separately"] is True
        and authorization["all20_rows_and_rejections_retained"] is True,
        "Separate original baseline and every outcome retained",
    )
    statuses, rows = authorization["fixed_row_statuses"], authorization["independent_row_artifacts"]
    require(
        type(statuses) is list
        and type(rows) is list
        and len(statuses) == len(rows) == 20
        and statuses == audit["fixed_row_statuses"],
        "All20 exact audit summary/index row statuses",
    )
    approved, referenced, report = 0, set(), []
    exact_keys = {
        "degree",
        "segments",
        "row_id",
        "status",
        "actual_row_file",
        "artifact_encoding",
        "compression_level",
        "gzip_mtime",
        "gzip_filename",
        "compact_sorted_JSON",
        "uncompressed_bytes",
        "uncompressed_JSON_SHA256",
        "compressed_bytes",
        "compressed_SHA256",
    }
    for (degree, segments), status, row in zip(GRID, statuses, rows, strict=True):
        budget()
        identity = dict(degree=degree, segments=segments, row_id=f"d{degree}_s{segments}")
        require(
            set(status) == set(identity) | {"status"}
            and all(type(status[key]) is int for key in ("degree", "segments"))
            and all(status[key] == val for key, val in identity.items())
            and status["status"]
            in ("CERTIFIED_ESTIMATE", "FIT_FAILED", "CERTIFICATE_REJECTED", "RESOURCE_REJECTED"),
            "Exact finite ordered row identity/status",
        )
        require(
            type(row) is dict
            and set(row) == exact_keys
            and all(row[key] == val for key, val in status.items()),
            "Unique proof reference shares exact outcome identity",
        )
        name = "rows/" + identity["row_id"] + ".json.gz"
        require(
            row["actual_row_file"] == name
            and row["artifact_encoding"] == "canonical-gzip-json-v1"
            and row["compression_level"] == 1
            and row["gzip_mtime"] == 0
            and row["gzip_filename"] == ""
            and row["compact_sorted_JSON"] is True,
            "Pinned auditor's canonical compressed retention format",
        )
        require(
            type(row["uncompressed_bytes"]) is int
            and 0 < row["uncompressed_bytes"] <= 128 * 1024**2
            and type(row["compressed_bytes"]) is int
            and 18 <= row["compressed_bytes"] <= 128 * 1024**2
            and type(row["uncompressed_JSON_SHA256"]) is str
            and len(row["uncompressed_JSON_SHA256"]) == 64
            and all(c in "0123456789abcdef" for c in row["uncompressed_JSON_SHA256"]),
            "Finite uncompressed metadata; no independent decompression/reproof",
        )
        member = add(AUDIT / name, row["compressed_SHA256"])
        require(
            member not in referenced
            and member.relative_to(AUDIT).as_posix() == name
            and member.stat().st_size == row["compressed_bytes"]
            and audit_manifest["files"].get(name) == row["compressed_SHA256"],
            "Unique actual gzip owned membership/size/expected compressed SHA",
        )
        referenced.add(member)
        before = fingerprint(member)
        with member.open("rb") as stream:
            header = stream.read(10)
        _HASH_WORK += len(header)
        require(_HASH_WORK <= MAX_HASH_WORK, "Fixed24GiB header-read bookkeeping cap")
        budget()
        require(
            fingerprint(member) == before and header == bytes.fromhex("1f8b08000000000004ff"),
            "Actual deterministic single-writer gzip header",
        )
        approved += status["status"] == "CERTIFIED_ESTIMATE"
        report.append(
            {**status, "actual_row_file": name, "compressed_SHA256": row["compressed_SHA256"]}
        )
    require(
        {p for p in _OWN_INVENTORIES[AUDIT] if p.is_relative_to(AUDIT / "rows")} == referenced,
        "Exactly all20 indexed actual gzip proof artifacts, no extra rows",
    )
    require(
        audit["certified_estimate_rows"] == approved
        and audit["retained_rejected_rows"] == 20 - approved
        and audit["all20_uniformly_certified"] is (approved == 20),
        "Honest certified-versus-rejected count from new audit only",
    )
    return report, approved


def own_runtime():
    require(
        canonical(sys.executable) == canonical(LAUNCHER)
        and sys.dont_write_bytecode is True
        and canonical(Path.cwd()) == ROOT,
        "Exact pinned launcher/cwd and startup -B",
    )
    require(
        not any(os.environ.get(key) for key in ("PYTHONPATH", "PYTHONHOME", "NUMBA_CACHE_DIR")),
        "No inherited runtime search/cache overrides",
    )
    require(canonical(sys.prefix) == ROOT / ".context/frontier_t0_env", "Pinned isolated prefix")
    cfg = Path(sys.prefix) / "pyvenv.cfg"
    add(cfg, digest(cfg))
    require(
        "include-system-site-packages = false" in cfg.read_text(encoding="utf-8").lower(),
        "Base site packages disabled",
    )
    base = canonical(sys.base_prefix)
    permitted = {
        ROOT,
        RESEARCH,
        base,
        canonical(sys.prefix),
        canonical(Path(sys.prefix) / "Lib/site-packages"),
        canonical(base / "Lib"),
        canonical(base / "DLLs"),
    }
    for entry in sys.path:
        lexical = Path(os.path.abspath(str(ROOT if not entry else entry)))
        if not lexical.exists():
            expected_zip = base / (
                "python" + str(sys.version_info.major) + str(sys.version_info.minor) + ".zip"
            )
            require(
                lexical == expected_zip and lexical.resolve(strict=False) == expected_zip,
                "Only the exact absent standard interpreter zip search entry",
            )
            _ABSENT_RUNTIME.add(lexical)
            continue
        path = canonical(ROOT if not entry else entry)
        require(
            path in permitted or (path.is_file() and path.parent == base and path.suffix == ".zip"),
            "Finite actual runtime search path",
        )
        if path.is_file():
            add(path, digest(path))
    roots = [base / "Lib", base / "DLLs", Path(sys.prefix) / "Scripts"]
    candidates = set()
    excluded = base / "Lib/site-packages"
    for tree in roots:
        for root, dirs, names in os.walk(tree, topdown=True, followlinks=False):
            budget()
            dirs[:] = [name for name in dirs if Path(root) / name != excluded]
            for name in dirs:
                require(not (Path(root) / name).is_symlink(), "No runtime directory alias")
                canonical(Path(root) / name)
            for name in names:
                candidates.add(canonical(Path(root) / name))
    for directory in (
        base,
        canonical(sys.prefix),
        canonical(Path(sys.prefix) / "Lib/site-packages"),
    ):
        for path in directory.iterdir():
            budget()
            if path.is_file():
                candidates.add(canonical(path))
    total = 0
    for path in sorted(candidates):
        require(path.is_file(), "Regular complete runtime member")
        total += path.stat().st_size
        require(
            len(candidates) <= MAX_RUNTIME_FILES and total <= MAX_RUNTIME_BYTES,
            "Fixed24k runtime files/2GiB",
        )
        add(path, digest(path))
    loaded_origins()
    return {
        "files": len(candidates),
        "bytes": total,
        "base_site_packages_pruned_and_rejected": True,
    }


def loaded_origins():
    forbidden = {"mpmath", "numpy", "scipy", "numba", "sympy", "gmpy", "gmpy2", "sage", "pytest"}
    require(
        not any(name.split(".", 1)[0] in forbidden for name in sys.modules),
        "No optional/scientific kernels imported",
    )
    require(
        not any(
            name.startswith("research.")
            and name not in {__name__, "research.limitation_program_20261001"}
            for name in sys.modules
        ),
        "No historical scientific module imported",
    )
    for module in list(sys.modules.values()):
        for attr in ("__file__", "__cached__"):
            origin = getattr(module, attr, None)
            if not origin:
                continue
            lexical = Path(os.path.abspath(str(origin)))
            base_site = Path(sys.base_prefix) / "Lib/site-packages"
            require(
                not lexical.is_relative_to(base_site)
                and not lexical.resolve(strict=False).is_relative_to(base_site.resolve()),
                "No excluded loaded origin or cache",
            )
            if lexical.is_file():
                actual = canonical(lexical)
                require(
                    actual.is_relative_to(ROOT)
                    or actual.is_relative_to(canonical(sys.base_prefix)),
                    "Confined actual stdlib/owned origin",
                )
                key = (
                    actual.relative_to(ROOT).as_posix()
                    if actual.is_relative_to(ROOT)
                    else str(actual)
                )
                mapping = _FROZEN if actual.is_relative_to(ROOT) else _EXTERNAL
                if key not in mapping:
                    add(actual, digest(actual))
                else:
                    require(digest(actual) == mapping[key], "Loaded origin same exact bytes")


def fresh_union():
    runtime_scopes()
    union = {}
    for mapping in (_FROZEN, _EXTERNAL):
        for member, expected in mapping.items():
            path = Path(member) if Path(member).is_absolute() else ROOT / member
            require(
                path not in union or union[path] == expected, "Equal-SHA unique verification union"
            )
            union[path] = expected
    # Include observed actual JSON/runtime/owned-copy paths, without placing
    # this receipt's own outputs in its immutable frozen input map.
    for path, observed in list(_OBSERVED.items()):
        require(
            path not in union or union[path] == observed, "Observed actual SHA equals expectation"
        )
        union[path] = observed
    total = count = 0
    for original, expected in union.items():
        budget()
        path = canonical(original, fresh=True)
        count += 1
        total += path.stat().st_size
        require(
            count <= MAX_REFERENCES and total <= MAX_UNIQUE_BYTES,
            "Fixed bounded complete union",
        )
        require(
            digest(path, fresh=True, already_resolved=True) == expected,
            "Fresh whole-union actual SHA mismatch: " + str(original),
        )
    for name in _PACKETS:
        if name not in (FAILED.name, FAILED_AUDIT.name, FAILED_AUDIT_V2.name, FAILED_AUDIT_V3.name):
            no_failure(PROGRAM / name)
    for directory, members in _OWN_INVENTORIES.items():
        require(inventory(directory) == members, "Terminal exact owned directory inventory")
    require(
        not any(path.exists() for path in _ABSENT_RUNTIME), "Absent standard zip remains absent"
    )
    require(
        not any(path.exists() for path in _ABSENT_HISTORICAL),
        "Original failed002 remains without manifest or original audit",
    )
    return count, total


def write(name, value):
    budget()
    encoder = json.JSONEncoder(indent=2, allow_nan=False)
    with (OUTPUT / name).open("x", encoding="utf-8", newline="\n") as stream:
        for chunk in encoder.iterencode(value):
            budget()
            stream.write(chunk)
        stream.write("\n")
    budget()


def copy_input(path, name):
    budget()
    with path.open("rb") as source, (OUTPUT / name).open("xb") as target:
        while chunk := source.read(1024 * 1024):
            budget()
            target.write(chunk)
    require(digest(OUTPUT / name) == digest(path), "Exact immutable executed input copy")


def fail(error):
    # Do not hash/retry/seal once the hard reserve is exhausted. A constant
    # failed-unsealed marker remains authoritative even beside a partial seal.
    if OUTPUT.is_dir():
        try:
            if (OUTPUT / "manifest.json").exists():
                (OUTPUT / "manifest.json").rename(OUTPUT / "partial_manifest.json")
        except OSError:
            pass
        try:
            if time.process_time() < CPU - 1 and time.monotonic() - _STARTED < WALL - 2:
                write(
                    "failure.json",
                    {
                        "failed": True,
                        "passed": False,
                        "error_type": type(error).__name__,
                        "error": str(error)[:2000],
                        "new_fixture_credit": 0,
                        "scientific_kernels_executed": False,
                    },
                )
        except BaseException:
            pass
        try:
            with (OUTPUT / "FAILED_UNSEALED.json").open("xb") as stream:
                stream.write(
                    b'{"failed":true,"passed":false,"budget_censored":null,"hard_budget_state_uncertified":true,"partial_success_invalid":true,"new_fixture_credit":0,"scientific_kernels_executed":false}\n'
                )
        except OSError:
            pass


def main():
    global _STARTED
    _STARTED = process_started()
    runtime_scopes()
    require(
        type(AUDIT_SHA) is str
        and len(AUDIT_SHA) == 64
        and type(NEW_AUDIT_AUTHORS) is dict
        and NEW_AUDIT_AUTHORS
        and type(NEW_AUDIT_REVIEW) is str
        and type(NEW_AUDIT_REVIEW_SHA) is str
        and type(NEW_AUDIT_REVIEW_FROZEN_COUNT) is int,
        "Actual independent004 terminal PASS and static release pins required before execution",
    )
    require(not OUTPUT.exists(), "Fresh fixed root verification receipt; no retry")
    require(sys.argv[1:] == [], "Fixed CLI without scope overrides")
    budget(admission=True)
    OUTPUT.mkdir()
    try:
        source = canonical(__file__)
        add(source, digest(source))
        add(ORIGIN, ORIGIN_SHA)
        copy_input(source, source.name)
        for mapping in (SOURCE_AUTHORS, AUDIT_V2_AUTHORS, AUDIT_V3_AUTHORS, NEW_AUDIT_AUTHORS, DP_AUTHORS):
            for name, pin in mapping.items():
                add(RESEARCH / name, pin)
        source_summary, _, _ = packet(SOURCE.name, SOURCE_SHA)
        audit_summary, _, audit_manifest = packet(AUDIT.name, AUDIT_SHA)
        for name, pin in PREREQUISITES.items():
            packet(name, pin)
        packet(NEW_AUDIT_REVIEW, NEW_AUDIT_REVIEW_SHA)
        packet(VALIDATION.name, VALIDATION_SHA)
        retained_material()
        method_checks()
        audit_only_release()
        rows, approved = check_release(source_summary, audit_summary, audit_manifest)
        runtime = own_runtime()
        copy_input(
            PROGRAM / "A13_recovery_root_review_run001/manifest.json",
            "original_metadata_source_root_review_manifest.json",
        )
        copy_input(
            PROGRAM / NEW_AUDIT_REVIEW / "manifest.json",
            "actual_new_audit_root_review_manifest.json",
        )
        count, total = fresh_union()
        budget(admission=True)
        write(
            "admission.json",
            {
                "complete_packet_map_counts": _PACKETS,
                "untrusted_source_metadata_only": True,
                "actual_independent_audit_is_sole_mathematical_authority": True,
                "original_source_pair_and_new_audit_author_bindings_kept_separate": True,
                "own_runtime": runtime,
                "fresh_unique_input_paths": count,
                "fresh_input_bytes": total,
                "all_original42_and_four_sealed_failed_packets_preserved_zero_credit": True,
                "finite16_selector_QA_integrity_verified_not_all20_scientific_approval": True,
            },
        )
        write("verified_compressed_proof_references.json", rows)
        loaded_origins()
        count, total = fresh_union()
        summary = {
            "schema": "root-exp-frontier-recovery-fresh-integrity-v1",
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "local_only": True,
            "passed": True,
            "completed": True,
            "budget_censored": False,
            "primary_metadata_integrity_only": True,
            "original_failed_source_mathematical_PASS": False,
            "actual_independent130_terminal_PASS": True,
            "primary_manifest_sha256": SOURCE_SHA,
            "audit_manifest_sha256": AUDIT_SHA,
            "independently_finalized_fixed_rows": 20,
            "independently_certified_estimate_rows": approved,
            "independently_retained_rejected_rows": 20 - approved,
            "all20_uniformly_certified_by_actual_new_audit": approved == 20,
            "compressed_proof_bytes_ownership_and_headers_verified": True,
            "uncompressed_content_not_decompressed_or_reproved": True,
            "primary90_order80_authorized_by_actual130_order80_reconstruction": True,
            "actual_auditor112_witnesses_retained_separately": True,
            "resource_numbers_symbolic_estimates_only": True,
            "fresh_unique_input_paths": count,
            "fresh_hashed_input_bytes": total,
            "SHA_mismatches": 0,
            "packet_map_counts": _PACKETS,
            "both_full_union_passes_uncached_resolution_and_actual_bytes": True,
            "actual_only_resolution_and_digest_cache_with_full_stat_reparse_guard": True,
            "original001_raw002_and_all_three_failed_audits_remain_failed": True,
            "finite16_selector_QA_manifest_sha256": VALIDATION_SHA,
            "finite_selector_QA_not_a_substitute_for_actual_all20_audit": True,
            "capture_manifest_sha256": FAILURE_DIAGNOSTIC_SHA,
            "CPU_admission_wall_limits": [CPU, ADMISSION, WALL],
            "process_CPU_seconds": time.process_time(),
            "wall_seconds_from_actual_process_creation": time.monotonic() - _STARTED,
            "new_fixture_credit": 0,
            "new_gate_replays": 0,
            "new_price_samples": 0,
            "scientific_kernels_executed": False,
            "fit_or_sourcewalk_or_proof_or_gate_execution": False,
            "actual_candidate_G2_feasibility": False,
            "candidate_G2_absolute_stock_error_allocation": None,
            "candidate_G2_barrier_band_allocation": None,
            "held_A13_fields_changed": False,
            "gate_emission_authorized": False,
            "full_G2": False,
            "adoption": False,
            "cost_transfer": False,
            "quantum_advantage_claim": False,
            "live_progress_or_STATUS_modified": False,
        }
        write("summary.json", summary)
        owned = inventory(OUTPUT)
        files = {
            path.relative_to(ROOT).as_posix(): digest(path, fresh=True) for path in sorted(owned)
        }
        budget()
        write(
            "manifest.json",
            {
                "schema": "root-exp-frontier-recovery-integrity-manifest-v1",
                "files": files,
                "frozen_inputs": _FROZEN,
                "external_runtime_inputs": _EXTERNAL,
                "terminal_record": (OUTPUT / "summary.json").relative_to(ROOT).as_posix(),
                "manifest_self_hash_excluded": True,
                "new_fixture_credit": 0,
                "scientific_kernels_executed": False,
            },
        )
        budget()
        terminal_sha = digest(OUTPUT / "manifest.json", fresh=True)
        budget()
        print(
            json.dumps(
                {
                    "passed": True,
                    "manifest_sha256": terminal_sha,
                    "paths": count,
                    "bytes": total,
                    "new_fixture_credit": 0,
                    "process_CPU_seconds": time.process_time(),
                    "wall_seconds": time.monotonic() - _STARTED,
                }
            )
        )
        budget()
    except BaseException as error:
        fail(error)
        raise


if __name__ == "__main__":
    main()
