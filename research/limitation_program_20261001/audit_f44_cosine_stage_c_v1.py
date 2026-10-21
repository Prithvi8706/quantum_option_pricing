"""Unexecuted independent130 F44 Stage C auditor; ROOT release required.

All448 true coefficients and64 centers, exact rational oracle, all64 eager
native caller promises, one complete clean gate prototype and zero fixture credit.
No financial gate emission, changed-source G2, adoption or advantage claim.
"""

import argparse
from array import array
import ast
from collections import Counter
import ctypes
from ctypes import wintypes
from fractions import Fraction
import hashlib
from importlib import metadata
from importlib.util import cache_from_source
import json
from math import factorial
import os
from pathlib import Path
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
PROGRAM = ROOT / "results/limitation_program_20261001"
AUTHOR = RESEARCH / "audit_f44_cosine_stage_c_v1.py"
BUILDER = RESEARCH / "f44_cosine_stage_c_source.py"
BUILDER_MODULE = "research.limitation_program_20261001.f44_cosine_stage_c_source"
METHOD_DOC = RESEARCH / "A14_F44_COSINE_STAGE_C_INDEPENDENT_AUDIT_PREFLIGHT_V1.md"
PREFLIGHT = RESEARCH / "a14_f44_cosine_stage_c_independent_audit_preflight_v1.json"
PROSPECTUS = RESEARCH / "a14_taylor_f44_prospectus_v1.json"
PROSPECTUS_DOC = RESEARCH / "A14_TAYLOR_F44_PROSPECTUS_V1.md"
PROSPECTUS_SHA = "526b082ca8d9ab1d1583de58e3fc0e6f5632583f6f663088ad42d6d389c713f3"
PROSPECTUS_DOC_SHA = "e4c1a4ad5c1bc23e266d9cbf4cfc5adeb1528fda8cfd89179696108be5302b04"
READY = ROOT / ".context/A14_F44_COSINE_STAGE_C_AUDIT_ROOT_READY_run001.json"
OUTPUT = PROGRAM / "A14_taylor_f44_stage_C_audit_run001"
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
ROOT_INTEGRITY_NAME = "A14_taylor_f44_stage_K_root_verification_run001"
ROOT_INTEGRITY_SHA = "24e316217afd614b577fe53921f54b7ad7c346737ec6e21c93500a795a1517d9"
ROOT_INTEGRITY_COUNTS = [8, 811, 2842]
BUILDER_SHA = "6aa28c87416e30558e459efe2c602866dcc9b2d76e236e93faae05fe65826a74"
BUILDER_NOTE = RESEARCH / "F44_STAGE_C_BUILDER_INTERFACE_AUTHOR_V1.md"
BUILDER_NOTE_SHA = "b737562b5bafdc271d5c08cf4fa13c1f9bde53dea291fea6515b0830ee336141"
SOURCE_NAME, AUDIT_NAME = "A14_taylor_f44_stage_K_run001", "A14_taylor_f44_stage_K_audit_run001"
SOURCE, AUDIT = PROGRAM / SOURCE_NAME, PROGRAM / AUDIT_NAME
SOURCE_SHA = "b03c8a7cb62655301b9a231eb987f38e5ec496f612206ff6701143f6cefb8b88"
AUDIT_SHA = "2c253beba55b1271dec594db8231c8bdbfcaffbf4d797dedb840eda72568f5be"
SOURCE_COUNTS, AUDIT_COUNTS = [17, 774, 2842], [10, 796, 2842]
COSINE_PACKETS = {
    "A14_cosine_feasibility_run001": (
        "bdb01b0c69d8fab3ee3d61f1c48ce5764f1ae09488f564d186f658f180e4156b",
        [24, 672, 2842],
    ),
    "A14_cosine_feasibility_audit_run003": (
        "52c88dc17c6a53b1df30bd93a431d3e263cb202462901589aaaa30bb87631f0f",
        [17, 752, 2842],
    ),
}
ORIGINAL_METHOD = RESEARCH / "a14_cosine_feasibility_implementation_preflight.json"
BRIDGE = PROGRAM / "A02_BM_native_financial_bridge_run002"
BRIDGE_AUDIT = PROGRAM / "A02_BM_native_financial_bridge_audit_run002"
PHASE_PROOF = PROGRAM / "A17_quantile_divider_run001/exact_CCX_phase_proof.json"
PHASE_SOURCE = RESEARCH / "temporary_and_fulladder.py"
W, F, Q, IF, IQ = 72, 40, 1 << 40, 44, 1 << 44
EPS, IEPS, H = Fraction(1, Q), Fraction(1, IQ), Fraction(1, 128)
ROW_ID = "TAYLOR_D6_S64_W72_F44_TO_F40_MUL52x38"
CPU, ADMISSION, WALL, DIGITS = 300, 270, 900, 130
MAX_NATIVE_ROWS = 2000000
MAX_OWN_FILES, MAX_OWN_BYTES = 64, 128 * 1024**2
MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = 24000, 2 * 1024**3
MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK = 100000, 8 * 1024**3, 24 * 1024**3
CASES = {"B4x12": (4, 12, 30), "B8x52": (8, 52, 234)}
CASE_SITES = {"B4x12": 60, "B8x52": 468}
BASELINE = {"B4x12": (520720662, 555774, 550141), "B8x52": (4267435214, 663704, 4460479)}
RESOURCE_FIELDS = (
    "source_gates",
    "x",
    "cx",
    "ccx",
    "t_count",
    "t_depth",
    "clifford_t_depth",
    "clifford_cx",
    "clifford_h",
)
EXACT_CCX_MACRO = (
    ("H", "target"),
    ("CX", "b", "target"),
    ("Tdg", "target"),
    ("CX", "a", "target"),
    ("T", "target"),
    ("CX", "b", "target"),
    ("Tdg", "target"),
    ("CX", "a", "target"),
    ("T", "b"),
    ("T", "target"),
    ("H", "target"),
    ("CX", "a", "b"),
    ("T", "a"),
    ("Tdg", "b"),
    ("CX", "a", "b"),
)
FAILURE_NAMES = (
    "FAILED_UNSEALED.json",
    "failed_unsealed.json",
    "failure.json",
    "run_failure.json",
    "prepare_failure.json",
)
_FROZEN, _EXTERNAL, _OBSERVED = {}, {}, {}
_PATH_CACHE, _HASH_CACHE = {}, {}
_OWN_INVENTORIES, _ABSENT_RUNTIME = {}, set()
_CODE_CACHE_EXPECTED = {}
_BASE_SCOPE, _EXCLUDED_SCOPE = None, None
_STANDARD_RUNTIME_MEMBERS = set()
_HASH_WORK = _REFERENCES = 0
_STARTED = None
_SCIENCE_ADMITTED = False
_PACKAGE_TREES = ()
_OLD_DESCRIPTORS = {}
_OLD_DESCRIPTOR_MEMBERSHIPS = {}

INTEGER_DECIMAL_DIGITS, INTEGER_SERIALIZATION_BITS = 20000, 65536
MAX_SERIALIZATION_VALUES = MAX_OWN_BYTES
PRIOR_FAILED = PROGRAM / "A14_taylor_f44_stage_C_run001"
PRIOR_FAILURE_FREEZE = ROOT / ".context/A14_F44_STAGE_C_FAILED_OWNED_FROZEN_run001.json"
PRIOR_FAILURE_FREEZE_SHA = "60b2d2aa068169f19f72052738227588ea5ad2837498fbe0009db1d4a5c17c75"
PRIOR_READY = ROOT / ".context/A14_F44_COSINE_STAGE_C_ROOT_READY_run001.json"
PRIOR_READY_SHA = "2a6806788c576085aafd2ff3fed1a03908e33fcddffef8c1d5d2b1c866b047de"
PRIOR_LOG = ROOT / ".context/a14_f44_stage_c_run001.log"
PRIOR_LOG_SHA = "da9d69f12a2cd1a8cef93ce0e112bf79410b659fad6289d8ae7b75bac14ada69"
PRIOR_AUTHORS = {
    "experiment_f44_cosine_stage_c_v1.py": (
        "c4f1bcbce2fd8ab729667c2a28c6dc44c857a6cf6feb02e308d52f2e19751caf"
    ),
    "A14_F44_COSINE_STAGE_C_IMPLEMENTATION_PREFLIGHT_V1.md": (
        "fa1a8d58c88ff379f7dc0b87733dc75e653ea617f4e93fe92c9f9e5f05a22620"
    ),
    "a14_f44_cosine_stage_c_implementation_preflight_v1.json": (
        "3b34f4745c6459de8e6eb0f257383dc4e1c7e783b68aa6700711a8f72956564f"
    ),
    "f44_cosine_stage_c_source.py": BUILDER_SHA,
    "F44_STAGE_C_BUILDER_INTERFACE_AUTHOR_V1.md": BUILDER_NOTE_SHA,
}
_PRIOR_FAILED_MEMBERS = set()
PRIOR_V2_OUTPUT = PROGRAM / "A14_taylor_f44_stage_C_run002"
PRIOR_V2_WITNESS = ROOT / ".context/A14_F44_STAGE_C_V2_PREFIT_FAILURE_WITNESS_run002.json"
PRIOR_V2_WITNESS_SHA = "1de19d91d1359ffce383ffd917bc20f803c466d1b35a731c271f18a3b33b5be6"
PRIOR_V2_READY = ROOT / ".context/A14_F44_COSINE_STAGE_C_ROOT_READY_run002.json"
PRIOR_V2_READY_SHA = "b53f15f958c9da2b966c965a58bbbe0f4839a61c92ff4452b5ed759a608ee2bc"
PRIOR_V2_LOG = ROOT / ".context/a14_f44_stage_c_run002.log"
PRIOR_V2_LOG_SHA = "a893e7feec700c44f5a686199dfd6ae3ad42687c29e7e11173bcd65e3821bad7"
PRIOR_V2_AUTHORS = {
    "experiment_f44_cosine_stage_c_v2.py": (
        "0a8e72bfa675b07ecaf948024d51ae5fb91381fd67fc0e9ec8d565635bcfff1c"
    ),
    "A14_F44_COSINE_STAGE_C_IMPLEMENTATION_PREFLIGHT_V2.md": (
        "f1cc8f98add202206d30cd082d75a2672039551124af4170d98402d47be9a1c0"
    ),
    "a14_f44_cosine_stage_c_implementation_preflight_v2.json": (
        "40cd6de37e0aa811a8078be12f701d3df317a24732e2ef1ca276aa53beb14ecb"
    ),
}


def fixed_integer_policy():
    budget()
    require(
        "PYTHONINTMAXSTRDIGITS" not in os.environ
        and "int_max_str_digits" not in sys._xoptions
        and sys.flags.int_max_str_digits
        == sys.get_int_max_str_digits()
        == sys.int_info.default_max_str_digits
        == 4300,
        "Pinned default decimal conversion policy before one explicit bounded change",
    )
    sys.set_int_max_str_digits(INTEGER_DECIMAL_DIGITS)
    require(
        sys.get_int_max_str_digits() == INTEGER_DECIMAL_DIGITS, "Exactly fixed20000 decimal digits"
    )
    budget()


def guard_serialization_integers(value):
    """A bounded representation guard; it neither rounds nor changes a value."""
    budget()
    require(
        sys.get_int_max_str_digits() == INTEGER_DECIMAL_DIGITS,
        "Fixed finite decimal policy unchanged",
    )
    pending, count, maximum_bits = [value], 0, 0
    while pending:
        budget()
        item = pending.pop()
        count += 1
        require(count <= MAX_SERIALIZATION_VALUES, "Evidence-value traversal bounded by128MiB")
        if type(item) is int:
            bits = item.bit_length()
            require(bits <= INTEGER_SERIALIZATION_BITS, "Each serialized integer at most65536 bits")
            maximum_bits = max(maximum_bits, bits)
        elif isinstance(item, dict):
            for key, member in item.items():
                budget()
                pending.append(key)
                pending.append(member)
                require(len(pending) <= MAX_SERIALIZATION_VALUES, "Bounded serializer frontier")
        elif isinstance(item, (list, tuple)):
            for member in item:
                budget()
                pending.append(member)
                require(len(pending) <= MAX_SERIALIZATION_VALUES, "Bounded serializer frontier")
    budget()
    return {"visited_values": count, "maximum_integer_bits": maximum_bits}


def serialization_edge_diagnostics():
    """Fixed synthetic representation checks; no cosine/native/financial fixtures."""
    budget()
    # A simple exact majorant proves every admitted bit length fits20k digits.
    require(
        (1 << 1000) < 10**302 and 66 * 302 < INTEGER_DECIMAL_DIGITS,
        "Exact decimal majorant for65536-bit integers",
    )
    accepted = (
        0,
        -1,
        1,
        -((1 << 14900) - 1),
        (1 << 14900) - 1,
        -((1 << 65536) - 1),
        (1 << 65536) - 1,
    )
    records = []
    for value in accepted:
        budget()
        # Keep the original exact integer numerator/positive denominator schema.
        pair = [value, 1]
        guard = guard_serialization_integers(pair)
        content = json.dumps(pair, allow_nan=False, separators=(",", ":")).encode("utf-8")
        require(
            len(content) <= MAX_OWN_BYTES and json.loads(content) == pair,
            "Exact decimal JSON integer-pair round trip",
        )
        records.append(
            {
                "input_sign": (value > 0) - (value < 0),
                "input_bits": value.bit_length(),
                "exact_integer_pair_round_trip": True,
                "encoded_bytes": len(content),
                "guard": guard,
            }
        )
    rejected = []
    for value in (-(1 << 65536), 1 << 65536):
        budget()
        did_reject = False
        try:
            guard_serialization_integers([value, 1])
        except ValueError as error:
            require(
                str(error) == "Each serialized integer at most65536 bits",
                "Only the fixed representation bound rejects edge",
            )
            did_reject = True
        require(did_reject, "Both65537-bit edges rejected before conversion")
        rejected.append(
            {
                "input_sign": (value > 0) - (value < 0),
                "input_bits": value.bit_length(),
                "rejected_before_decimal_conversion": True,
            }
        )
    budget()
    return {
        "schema": "a14-f44-stage-c-serialization-edges-v2",
        "fixed_accepted_count": 7,
        "fixed_rejected_count": 2,
        "decimal_digit_limit": INTEGER_DECIMAL_DIGITS,
        "per_integer_bit_cap": INTEGER_SERIALIZATION_BITS,
        "integer_pair_schema_unchanged": True,
        "arithmetic_precision_changed": False,
        "accepted": records,
        "rejected": rejected,
        **flags(),
    }


def prior_failure_witnesses():
    budget()
    require(
        inventory(PRIOR_FAILED) == _PRIOR_FAILED_MEMBERS
        and (PRIOR_FAILED / "FAILED_UNSEALED.json").is_file()
        and not (PRIOR_FAILED / "manifest.json").exists()
        and not (PRIOR_FAILED / "manifest.json").is_symlink(),
        "Original13-file partial Stage C run remains immutable, failed and unapproved",
    )
    require(
        sum(fingerprint(path)[2] for path in _PRIOR_FAILED_MEMBERS) == 11426616,
        "Original failed-owned byte count unchanged",
    )
    require(
        not PRIOR_V2_OUTPUT.exists()
        and not PRIOR_V2_OUTPUT.is_symlink()
        and PRIOR_V2_OUTPUT.resolve(strict=False) == PRIOR_V2_OUTPUT,
        "Actual V2 startup failure stays before output creation and without physical alias",
    )
    budget()


def admit_prior_failure(ready, policy):
    require(
        ready["prior_failed_owned_freeze_SHA256"]
        == policy["prior_failed_owned_freeze_SHA256"]
        == PRIOR_FAILURE_FREEZE_SHA,
        "Externally frozen exact previous failure map",
    )
    record = read(bind(PRIOR_FAILURE_FREEZE, PRIOR_FAILURE_FREEZE_SHA))
    require(
        record["schema"] == "root-a14-f44-stage-c-failed-owned-freeze-v1"
        and record["metadata_freeze_only"] is True
        and record["passed"] is False
        and record["original_failure_is_authoritative"] is True
        and record["hard_budget_state_uncertified"] is True
        and record["all_expected_SHA_waivers"] == 0,
        "Previous failure freeze is metadata only",
    )
    require(
        record["failure_route"] == PRIOR_FAILED.relative_to(ROOT).as_posix()
        and record["owned_file_count"] == 13
        and record["owned_bytes"] == 11426616
        and record["original_READY_expected_sha256"] == PRIOR_READY_SHA
        and record["original_log_sha256"] == PRIOR_LOG_SHA,
        "Exact prior route/counts/READY/raw log",
    )
    members = record["observed_owned_files"]
    require(
        type(members) is dict and len(members) == 13, "All13 immutable prior owned observations"
    )
    for key, expected in members.items():
        budget()
        require(
            type(key) is str
            and "\\" not in key
            and (ROOT / key).relative_to(ROOT).as_posix() == key
            and ".." not in Path(key).parts,
            "Exact prior ROOT-relative owned spelling",
        )
        member = bind(ROOT / key, expected)
        require(
            member.is_relative_to(PRIOR_FAILED)
            and member not in _PRIOR_FAILED_MEMBERS
            and member.name != "manifest.json",
            "Unique physically confined prior failed-owned member",
        )
        _PRIOR_FAILED_MEMBERS.add(member)
    historical = read(bind(PRIOR_READY, PRIOR_READY_SHA))
    require(
        historical["schema"] == "root-a14-f44-cosine-stage-c-READY-v1"
        and historical["author_method_SHA256"] == PRIOR_AUTHORS
        and historical["output"] == PRIOR_FAILED.relative_to(ROOT).as_posix(),
        "All five exact original author bytes remain fixed",
    )
    for name, expected in PRIOR_AUTHORS.items():
        bind(RESEARCH / name, expected)
    bind(PRIOR_LOG, PRIOR_LOG_SHA)
    code_caches(
        [RESEARCH / "experiment_f44_cosine_stage_c_v1.py", BUILDER],
        historical["existing_new_code_cache_SHA256"],
        historical["absent_new_code_cache_paths"],
    )
    failure, marker = (
        read(PRIOR_FAILED / "failure.json"),
        read(PRIOR_FAILED / "FAILED_UNSEALED.json"),
    )
    require(
        failure["passed"] is False
        and failure["completed"] is False
        and failure["error_type"] == "ValueError"
        and "4300 digits" in failure["error"]
        and marker["passed"] is False
        and marker["completed"] is False
        and marker["hard_budget_state_uncertified"] is True
        and marker["budget_censored"] is None,
        "Exact previous decimal-serialization failure remains authoritative",
    )
    for key, expected in (
        ("prior_V2_prefit_failure_witness_SHA256", PRIOR_V2_WITNESS_SHA),
        ("prior_V2_READY_SHA256", PRIOR_V2_READY_SHA),
        ("prior_V2_log_SHA256", PRIOR_V2_LOG_SHA),
    ):
        require(
            ready[key] == policy[key] == expected,
            "Exact externally expected V2 startup failure metadata history",
        )
    require(
        ready["prior_V2_three_author_SHA256"]
        == policy["prior_V2_three_author_SHA256"]
        == PRIOR_V2_AUTHORS,
        "All three original V2 author expectations remain fixed",
    )
    witness = read(bind(PRIOR_V2_WITNESS, PRIOR_V2_WITNESS_SHA))
    require(
        witness["schema"] == "root-a14-stage-c-v2-prefit-failure-witness-v1"
        and witness["passed"] is False
        and witness["metadata_only"] is True
        and witness["actual_V2_failed_before_output_mkdir"] is True
        and witness["scientific_execution_started"] is False
        and witness["bounded_decimal_policy_set_by_V2_before_failure"] is False
        and witness["original_READY_expected_sha256"] == PRIOR_V2_READY_SHA
        and witness["original_log_expected_sha256"] == PRIOR_V2_LOG_SHA
        and witness["author_expected_SHA256"] == PRIOR_V2_AUTHORS
        and witness["output_route"] == PRIOR_V2_OUTPUT.relative_to(ROOT).as_posix()
        and witness["original_run001_failure_unchanged"] is True
        and witness["startup_flag_observed"]
        == witness["startup_effective_digit_limit_observed"]
        == witness["startup_documented_default_observed"]
        == 4300
        and witness["startup_environment_override_absent"] is True
        and witness["startup_xoption_override_absent"] is True
        and witness["new_fixture_credit"] == 0,
        "V2 startup guard failure has no scientific or bounded-policy result",
    )
    historical_V2 = read(bind(PRIOR_V2_READY, PRIOR_V2_READY_SHA))
    require(
        historical_V2["schema"] == "root-a14-f44-cosine-stage-c-READY-v2"
        and historical_V2["author_method_SHA256"]
        == {
            **PRIOR_V2_AUTHORS,
            BUILDER.name: BUILDER_SHA,
            BUILDER_NOTE.name: BUILDER_NOTE_SHA,
        }
        and historical_V2["output"] == PRIOR_V2_OUTPUT.relative_to(ROOT).as_posix()
        and historical_V2["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
        and historical_V2["integer_decimal_digit_limit"] == INTEGER_DECIMAL_DIGITS
        and historical_V2["integer_serialization_bit_cap"] == INTEGER_SERIALIZATION_BITS,
        "Exact V2 author trio, shared builder and bounded representation plan preserved",
    )
    for name, expected in PRIOR_V2_AUTHORS.items():
        bind(RESEARCH / name, expected)
    bind(PRIOR_V2_LOG, PRIOR_V2_LOG_SHA)
    code_caches(
        [RESEARCH / "experiment_f44_cosine_stage_c_v2.py", BUILDER],
        historical_V2["existing_new_code_cache_SHA256"],
        historical_V2["absent_new_code_cache_paths"],
    )
    prior_failure_witnesses()


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


def own_runtime():
    global _STANDARD_RUNTIME_MEMBERS
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
        require(
            not any(lexical.is_relative_to(scope) for scope in _EXCLUDED_SCOPE)
            and not any(
                lexical.resolve(strict=False).is_relative_to(scope) for scope in _EXCLUDED_SCOPE
            ),
            "No excluded search path even when absent",
        )
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
    candidates = standard_runtime_members()
    _STANDARD_RUNTIME_MEMBERS = candidates
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


def standard_runtime_members():
    base = canonical(sys.base_prefix)
    candidates = set()
    excluded = base / "Lib/site-packages"
    for tree in (base / "Lib", base / "DLLs", Path(sys.prefix) / "Scripts") + _PACKAGE_TREES:
        for root, dirs, names in os.walk(tree, topdown=True, followlinks=False):
            budget()
            dirs[:] = [name for name in dirs if Path(root) / name != excluded]
            for name in dirs:
                require(not (Path(root) / name).is_symlink(), "No runtime directory alias")
                canonical(Path(root) / name)
            for name in names:
                candidates.add(canonical(Path(root) / name))
                require(len(candidates) <= MAX_RUNTIME_FILES, "Finite complete runtime membership")
    for directory in (
        base,
        canonical(sys.prefix),
        canonical(Path(sys.prefix) / "Lib/site-packages"),
    ):
        for path in directory.iterdir():
            budget()
            if path.is_file():
                candidates.add(canonical(path))
                require(len(candidates) <= MAX_RUNTIME_FILES, "Finite adjacent runtime membership")
    return candidates


def key_for(path):
    return path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)


def bind(path, expected):
    actual = add(path, expected)
    require(digest(actual) == expected, "Actual admitted expected bytes")
    return actual


def packet(name, pin, counts):
    directory = canonical(PROGRAM / name)
    manifest = bind(directory / "manifest.json", pin)
    data = read(manifest)
    no_failure(directory)
    require(
        data.get("passed") is True
        and data.get("completed") is True
        and data.get("budget_censored") is False
        and data.get("manifest_self_hash_excluded") is True,
        "Actual completed uncensored scoped source/audit, not candidate eligibility",
    )
    require(
        [len(data[field]) for field in ("files", "frozen_inputs", "external_runtime_inputs")]
        == counts,
        "Complete original maps",
    )
    owned = {manifest}
    for field in ("files", "frozen_inputs", "external_runtime_inputs"):
        require(type(data[field]) is dict, "Typed complete original input maps")
        for key, expected in data[field].items():
            budget()
            require(type(key) is str, "Literal original key")
            if field == "external_runtime_inputs":
                require(Path(key).is_absolute(), "Scoped external original key")
                path = Path(key)
            else:
                require(
                    not Path(key).is_absolute() and "\\" not in key and ".." not in Path(key).parts,
                    "Exact slash-relative old key",
                )
                root_owned = key.startswith(directory.relative_to(ROOT).as_posix() + "/")
                path = ROOT / key if field == "frozen_inputs" or root_owned else directory / key
            actual = bind(path, expected)
            if field == "files":
                require(
                    actual.is_relative_to(directory)
                    and actual not in owned
                    and actual.relative_to(ROOT if root_owned else directory).as_posix() == key,
                    "Exact no-alias original own membership",
                )
                owned.add(actual)
            elif field == "frozen_inputs":
                require(
                    actual.is_relative_to(ROOT) and actual.relative_to(ROOT).as_posix() == key,
                    "Exact original ROOT membership",
                )
            else:
                require(
                    not actual.is_relative_to(ROOT) and str(actual) == key,
                    "Exact external original membership",
                )
    require(inventory(directory) == owned, "Exact complete prior inventory")
    _OWN_INVENTORIES[directory] = owned
    return data


def fresh_union():
    runtime_scopes()
    prior_failure_witnesses()
    for lexical, (actual, _) in tuple(_PATH_CACHE.items()):
        budget()
        require(canonical(lexical, fresh=True) == actual, "Every lexical alias freshly confined")
    union = {}
    for mapping in (_FROZEN, _EXTERNAL):
        for key, expected in mapping.items():
            budget()
            path = Path(key) if Path(key).is_absolute() else ROOT / key
            require(path not in union or union[path] == expected, "Equal-SHA complete union")
            union[path] = expected
    for path, value in tuple(_OBSERVED.items()):
        budget()
        require(path not in union or union[path] == value, "Observed never replaces expected")
        union[path] = value
    total = 0
    for path, expected in sorted(union.items()):
        budget()
        actual = canonical(path, fresh=True)
        total += actual.stat().st_size
        require(len(union) <= MAX_REFERENCES and total <= MAX_UNIQUE_BYTES, "Complete union caps")
        require(
            digest(actual, fresh=True, already_resolved=True) == expected, "Full fresh actual SHA"
        )
    for directory, members in _OWN_INVENTORIES.items():
        budget()
        require(inventory(directory) == members, "All original own inventories unchanged")
        no_failure(directory)
    require(
        standard_runtime_members() == _STANDARD_RUNTIME_MEMBERS,
        "Complete runtime membership unchanged",
    )
    require(
        not any(path.exists() or path.is_symlink() for path in _ABSENT_RUNTIME),
        "Absent standard zip and new-code caches still absent",
    )
    return {"unique_paths": len(union), "unique_bytes": total, "full_fresh_resolve_and_SHA": True}


def code_caches(sources, pins, absent_keys):
    """External presence/absence admission; source execution never reads these caches."""
    budget()
    paths = {
        key_for(Path(cache_from_source(str(source)))): Path(cache_from_source(str(source)))
        for source in sources
    }
    present = {key for key, path in paths.items() if path.exists()}
    require(
        type(pins) is dict
        and set(pins) == present
        and type(absent_keys) is list
        and absent_keys == sorted(set(paths) - present),
        "Exact external cache presence and absence declaration",
    )
    for key in present:
        path = bind(paths[key], pins[key])
        _CODE_CACHE_EXPECTED[path] = pins[key]
    for key in absent_keys:
        path = paths[key]
        require(not path.exists() and not path.is_symlink(), "No absent cache or dangling alias")
        _ABSENT_RUNTIME.add(path)
    budget()


def check_code_caches():
    budget()
    for path, expected in _CODE_CACHE_EXPECTED.items():
        require(digest(path, fresh=True) == expected, "Declared existing cache bytes unchanged")
    require(
        not any(path.exists() or path.is_symlink() for path in _ABSENT_RUNTIME),
        "Declared absent caches and standard zip remain absent",
    )
    budget()


def complete_manifest(value, owned, nonmanifest_bytes):
    """Check exact UTF8 JSON bytes and file count including the prospective manifest."""
    budget()
    require(len(owned) + 1 <= MAX_OWN_FILES, "Manifest-inclusive owned file cap")
    value["manifest_inclusive_owned_file_count"] = len(owned) + 1
    value["owned_nonmanifest_bytes"] = nonmanifest_bytes
    value["manifest_inclusive_retention_checked_before_sealing"] = True
    guard_serialization_integers(value)
    manifest_bytes = 1  # save() appends exactly one newline.
    for fragment in json.JSONEncoder(sort_keys=True, indent=2, allow_nan=False).iterencode(value):
        budget()
        manifest_bytes += len(fragment.encode("utf-8"))
        require(nonmanifest_bytes + manifest_bytes <= MAX_OWN_BYTES, "Manifest-inclusive128MiB cap")
    save("manifest.json", value)
    require(
        (OUTPUT / "manifest.json").stat().st_size == manifest_bytes, "Exact encoded manifest size"
    )
    actual = inventory(OUTPUT)
    require(
        actual == {OUTPUT / name for name in owned} | {OUTPUT / "manifest.json"}
        and len(actual) == len(owned) + 1 <= MAX_OWN_FILES,
        "Complete final manifest-inclusive inventory",
    )
    total = 0
    for path in actual:
        budget()
        total += path.stat().st_size
    require(
        total == nonmanifest_bytes + manifest_bytes <= MAX_OWN_BYTES,
        "Complete final owned byte cap",
    )
    budget()


def save(name, value):
    budget()
    guard_serialization_integers(value)
    target = OUTPUT / name
    require(target.parent == OUTPUT and not target.exists(), "Exclusive metadata output")
    pieces, new_bytes = [], 0
    for fragment in json.JSONEncoder(indent=2, sort_keys=True, allow_nan=False).iterencode(value):
        budget()
        part = fragment.encode("utf-8")
        new_bytes += len(part)
        require(new_bytes <= MAX_OWN_BYTES, "Bounded prospective UTF8 serialization")
        pieces.append(part)
    pieces.append(b"\n")
    new_bytes += 1
    members = inventory(OUTPUT)
    current_bytes = 0
    for member in members:
        budget()
        current_bytes += member.stat().st_size
    require(
        len(members) + 1 + (name != "manifest.json") <= MAX_OWN_FILES
        and current_bytes + new_bytes <= MAX_OWN_BYTES,
        "Inclusive owned byte/file cap with a final manifest slot",
    )
    with target.open("xb") as stream:
        for piece in pieces:
            budget()
            stream.write(piece)
    require(target.stat().st_size == new_bytes, "Exactly admitted output bytes")
    budget()


def copy(path, name):
    source = canonical(path)
    before, expected = fingerprint(source), digest(source)
    target = OUTPUT / name
    members = inventory(OUTPUT)
    require(target.parent == OUTPUT and not target.exists(), "New fixed copied output")
    require(
        len(members) + 2 <= MAX_OWN_FILES
        and sum(member.stat().st_size for member in members) + before[2] <= MAX_OWN_BYTES,
        "Admitted copied bytes with a manifest slot",
    )
    total = 0
    with source.open("rb") as incoming, target.open("xb") as outgoing:
        while block := incoming.read(65536):
            budget()
            total += len(block)
            require(total <= before[2], "Copied source cannot grow")
            outgoing.write(block)
    require(total == before[2] and fingerprint(source) == before, "Stable complete source copy")
    require(digest(target) == expected, "Exact preserved copied source bytes")


def retain_failure(error):
    if not OUTPUT.is_dir():
        return
    try:
        budget()
        save(
            "failure.json",
            {
                "passed": False,
                "completed": False,
                "error_type": type(error).__name__,
                "error": str(error),
                "traceback": traceback.format_exc(),
                **flags(),
            },
        )
    except BaseException:
        pass
    try:
        with (OUTPUT / "FAILED_UNSEALED.json").open("xb") as stream:
            stream.write(
                b'{"failed":true,"passed":false,"completed":false,"budget_censored":null,'
                b'"hard_budget_state_uncertified":true,"new_test_credit":0,'
                b'"Stage_C_release_authorized":false,"full_G2":false,"adoption":false}\n'
            )
    except OSError:
        pass


def package_runtime():
    """Freeze full mpmath package/metadata and every actually loaded startup package."""
    global _PACKAGE_TREES
    budget()
    require(
        not any(name == "mpmath" or name.startswith("mpmath.") for name in sys.modules),
        "No numerical package import before complete admission",
    )
    site_root = canonical(Path(sys.prefix) / "Lib/site-packages")
    distribution = metadata.distribution("mpmath")
    require(distribution.version == "1.3.0", "Exactly installed mpmath1.3.0")
    package = canonical(site_root / "mpmath")
    members = distribution.files
    require(members, "Complete installed distribution RECORD inventory")
    metadata_roots = set()
    for member in members:
        budget()
        actual = canonical(distribution.locate_file(member))
        require(
            actual.is_file() and actual.is_relative_to(site_root), "Confined mpmath RECORD member"
        )
        if actual.name == "METADATA" and actual.parent.name.endswith(".dist-info"):
            metadata_roots.add(actual.parent)
    require(len(metadata_roots) == 1, "Exactly one installed mpmath metadata directory")
    trees = {package, *metadata_roots}
    for module in tuple(sys.modules.values()):
        budget()
        origin = getattr(module, "__file__", None)
        if origin and Path(origin).is_file():
            actual = canonical(origin)
            if actual.is_relative_to(site_root):
                first = site_root / actual.relative_to(site_root).parts[0]
                if first.is_dir():
                    trees.add(canonical(first))
    _PACKAGE_TREES = tuple(sorted(trees))
    budget()
    return {
        "mpmath_version": distribution.version,
        "complete_package_metadata_and_loaded_startup_trees": [key_for(p) for p in _PACKAGE_TREES],
        "MPMATH_NOGMPY": "1",
        "MPMATH_NOSAGE": "1",
    }


def loaded_origins():
    forbidden = {"numpy", "scipy", "numba", "sympy", "gmpy", "gmpy2", "sage", "pytest"}
    require(
        not any(name.split(".", 1)[0] in forbidden for name in sys.modules),
        "No optional numerical backend or scientific package",
    )
    require(
        _SCIENCE_ADMITTED
        or not any(name == "mpmath" or name.startswith("mpmath.") for name in sys.modules),
        "mpmath only after admission",
    )
    allowed = {__name__, "research.limitation_program_20261001"}
    require(BUILDER_MODULE not in sys.modules, "No producer builder import in independent audit")
    require(
        not any(name.startswith("research.") and name not in allowed for name in sys.modules),
        "No old scientific producer/auditor/helper imports",
    )
    for module in tuple(sys.modules.values()):
        budget()
        for attribute in ("__file__", "__cached__"):
            origin = getattr(module, attribute, None)
            if not origin:
                continue
            lexical = Path(os.path.abspath(str(origin)))
            require(
                not any(
                    lexical.is_relative_to(scope)
                    or lexical.resolve(strict=False).is_relative_to(scope)
                    for scope in _EXCLUDED_SCOPE
                ),
                "No excluded base package origin/cache",
            )
            if lexical.is_file():
                actual = canonical(lexical, fresh=True)
                key = key_for(actual)
                mapping = _FROZEN if actual.is_relative_to(ROOT) else _EXTERNAL
                if key not in mapping:
                    require(
                        not _SCIENCE_ADMITTED,
                        "No newly observed source/cache admission after scientific loading",
                    )
                    add(actual, digest(actual, fresh=True, already_resolved=True))
                else:
                    require(
                        digest(actual, fresh=True, already_resolved=True) == mapping[key],
                        "Fresh loaded bytes match admitted expectation",
                    )


def admitted_bytes(path, maximum=128 * 1024**2):
    global _HASH_WORK
    budget()
    path = canonical(path)
    before = fingerprint(path)
    require(path.is_file() and before[2] <= maximum, "Bounded admitted byte source")
    expected = _FROZEN.get(key_for(path)) if path.is_relative_to(ROOT) else _EXTERNAL.get(str(path))
    require(expected is not None, "Bytes must belong to an externally admitted map")
    state, parts, total = hashlib.sha256(), [], 0
    with path.open("rb") as stream:
        while part := stream.read(65536):
            budget()
            total += len(part)
            _HASH_WORK += len(part)
            require(total <= before[2] and _HASH_WORK <= MAX_HASH_WORK, "Bounded admitted reads")
            state.update(part)
            parts.append(part)
    require(total == before[2] and fingerprint(path) == before, "Stable full admitted source")
    require(state.hexdigest() == expected, "Exact admitted expected byte digest")
    budget()
    return b"".join(parts)


def preserved_prerequisite_caches():
    declarations = (
        (
            ".context/A14_TAYLOR_F44_STAGE_K_ROOT_READY_run001.json",
            ("experiment_taylor_f44_stage_k.py", "taylor_f44_stage_k_source.py"),
        ),
        (
            ".context/A14_TAYLOR_F44_STAGE_K_AUDIT_ROOT_READY_run001.json",
            ("audit_taylor_f44_stage_k.py",),
        ),
        (
            ".context/A14_TAYLOR_F44_STAGE_K_INTEGRITY_ROOT_READY_run001.json",
            ("verify_taylor_f44_stage_k_root_v1.py",),
        ),
    )
    for key, names in declarations:
        budget()
        require(key in _FROZEN, "Historical READY already admitted through full K maps")
        historical = read(ROOT / key)
        for name in names:
            require(
                (RESEARCH / name).relative_to(ROOT).as_posix() in _FROZEN,
                "Historical source already admitted through full K maps",
            )
        code_caches(
            [RESEARCH / name for name in names],
            historical["existing_new_code_cache_SHA256"],
            historical["absent_new_code_cache_paths"],
        )
    old_runtime_records = (
        read(PROGRAM / "A14_cosine_feasibility_run001/interpreter.json"),
        read(PROGRAM / "A14_cosine_feasibility_audit_run003/protocol.json")["interpreter"],
    )
    for record in old_runtime_records:
        for spelling in record["absent_standard_runtime_paths"]:
            budget()
            path = Path(spelling)
            require(
                path.is_absolute()
                and path == Path(os.path.abspath(path))
                and path.resolve(strict=False) == path
                and not path.exists()
                and not path.is_symlink(),
                "Historical original/F40 runtime absence remains physically exact",
            )
            _ABSENT_RUNTIME.add(path)
    check_code_caches()


def same(first, second, message):
    require(
        json.dumps(first, sort_keys=True, separators=(",", ":"), allow_nan=False)
        == json.dumps(second, sort_keys=True, separators=(",", ":"), allow_nan=False),
        message,
    )


def unsigned_word(value):
    require(type(value) is int and 0 <= value < 1 << W, "Canonical unsigned72 CONST")
    return value - (1 << W) if value >= 1 << 71 else value


def signed_coefficient(value):
    return native_word(value)


def native_word(value):
    require(type(value) is int and -(1 << 71) <= value < 1 << 71, "Signed72 literal")
    return value


def nearest_fraction(value):
    value = Fraction(value)
    quotient, remainder = divmod(value.numerator, value.denominator)
    return quotient + int(
        2 * remainder > value.denominator or (2 * remainder == value.denominator and quotient % 2)
    )


class GraphAudit:
    """Own backward traversal on actual SSA; never constructs or evaluates it."""

    def __init__(self, target, started):
        self.target, self.started, self.nodes, self.ancestor_cache = target, started, {}, {}
        require((target["width"], target["fraction_bits"]) == (72, 40), "Native W72/F40")
        arities = {
            "input": 0,
            "const": 0,
            "add": 2,
            "sub": 2,
            "mul": 2,
            "cmul": 1,
            "lt": 2,
            "select": 3,
            "positive": 1,
            "msb": 1,
            "bits": 1,
            "shift": 2,
            "sqrt": 1,
            "lookup": 1,
        }
        next_value = 0
        for row in target["nodes"]:
            check(started)
            op, args, out, params = (row[k] for k in ("op", "args", "out", "params"))
            require(
                op in arities and type(args) is list and len(args) == arities[op], "Typed arity"
            )
            require(type(out) is list and type(params) is dict and out, "Typed node shape")
            require(all(type(v) is int and v in self.nodes for v in args), "Topological dependency")
            require(
                out == list(range(next_value, next_value + len(out))),
                "Exact contiguous output slots",
            )
            require(all(type(v) is int for v in out), "Typed SSA identities")
            next_value += len(out)
            require(op == "lookup" or len(out) == 1, "Single output native primitive")
            if op == "const":
                require(set(params) == {"value"}, "Exact constant fields")
                unsigned_word(params["value"])
            elif op == "cmul":
                require(set(params) == {"c"}, "Exact coefficient fields")
                signed_coefficient(params["c"])
            elif op == "bits":
                require(
                    set(params) == {"shift", "width", "signed"}
                    and type(params["shift"]) is int
                    and type(params["width"]) is int
                    and 1 <= params["width"] <= 72
                    and type(params["signed"]) is bool,
                    "Exact bit-extraction fields",
                )
            elif op == "lookup":
                require(
                    set(params) == {"table", "bits"} and type(params["bits"]) is int,
                    "Exact lookup fields",
                )
                table = target["tables"][params["table"]]
                require(
                    len(table) == 1 << params["bits"]
                    and all(len(entry) == len(out) for entry in table),
                    "Complete table shape",
                )
                for entry in table:
                    for coefficient in entry:
                        signed_coefficient(coefficient)
            elif op == "input":
                require(set(params) == {"name", "bits", "preparation"}, "Exact input fields")
            else:
                require(params == {}, "No undeclared arithmetic parameters")
            for value in out:
                self.nodes[value] = row

    def node(self, value, kind=None, params=None):
        check(self.started)
        require(type(value) is int and value in self.nodes, "Actual SSA identity")
        row = self.nodes[value]
        require(kind is None or row["op"] == kind, "Expected native operation")
        if params is not None:
            same(row["params"], params, "Exact native operation parameters")
        return row

    def constant(self, value, expected=None):
        result = unsigned_word(self.node(value, "const")["params"]["value"])
        require(expected is None or result == expected, "Actual decoded constant")
        return result

    def ancestors(self, value):
        if value not in self.ancestor_cache:
            pending, values = [value], set()
            while pending:
                check(self.started)
                current = pending.pop()
                if current not in values:
                    values.add(current)
                    pending.extend(self.node(current)["args"])
            self.ancestor_cache[value] = values
        return self.ancestor_cache[value]

    def clamp(self, value, low=None, high=None):
        topflag, middle, upper = self.node(value, "select")["args"]
        require(self.node(topflag, "lt")["args"] == [middle, upper], "Exact upper clamp")
        bottomflag, lower, original = self.node(middle, "select")["args"]
        require(self.node(bottomflag, "lt")["args"] == [original, lower], "Exact lower clamp")
        require(self.constant(lower, low) < self.constant(upper, high), "Ordered clamp literals")
        return original

    def midpoint(self, value, input_value):
        args = self.node(value, "add")["args"]
        shifted = [v for v in args if self.node(v)["op"] == "bits"]
        require(len(shifted) == 1, "One midpoint conversion")
        require(
            self.node(shifted[0], "bits", {"shift": -8, "width": 72, "signed": False})["args"]
            == [input_value],
            "Exact q32 to f40 conversion",
        )
        self.constant(next(v for v in args if v != shifted[0]), 128)

    def interpolation(self, result, table_name, input_value):
        bins, degree, lower, bits = (32, 8, Q, 5) if table_name == "log" else (64, 7, 0, 6)
        candidates = {
            tuple(self.node(v)["out"])
            for v in self.ancestors(result)
            if self.node(v)["op"] == "lookup" and self.node(v)["params"]["table"] == table_name
        }
        require(len(candidates) == 1, "One table supplies every Horner coefficient")
        coefficients = next(iter(candidates))
        require(len(coefficients) == degree + 1, "All actual polynomial coefficients")
        address = self.node(coefficients[0], "lookup", {"table": table_name, "bits": bits})["args"][
            0
        ]
        bounded = self.node(address, "bits", {"shift": 40 - bits, "width": bits, "signed": False})[
            "args"
        ][0]
        if lower:
            bounded, literal = self.node(bounded, "sub")["args"]
            self.constant(literal, lower)
        require(
            self.clamp(bounded, lower, lower + Q - 1) == input_value, "Interpolation input binding"
        )
        current, local = result, None
        for coefficient in coefficients[:-1]:
            args = self.node(current, "add")["args"]
            require(coefficient in args, "Horner coefficient order")
            factors = self.node(next(v for v in args if v != coefficient), "mul")["args"]
            if local is None:
                possible = [v for v in factors if self.node(v)["op"] == "sub"]
                require(len(possible) == 1, "One local variable in Horner")
                local = possible[0]
            require(local in factors, "Every Horner product uses same local variable")
            current = next(v for v in factors if v != local)
        require(current == coefficients[-1], "Horner terminal coefficient")
        actual, center = self.node(local, "sub")["args"]
        require(actual == bounded, "Local variable uses bounded argument")
        args = self.node(center, "add")["args"]
        shifted = [v for v in args if self.node(v)["op"] == "bits"]
        require(len(shifted) == 1, "Exact local center shift")
        require(
            self.node(shifted[0], "bits", {"shift": bits - 40, "width": 72, "signed": False})[
                "args"
            ]
            == [address],
            "Local center derives from same address",
        )
        self.constant(next(v for v in args if v != shifted[0]), lower + Q // (2 * bins))
        return dict(
            output=result,
            input=input_value,
            address=address,
            local=local,
            lookup_outputs=list(coefficients),
            floors=degree,
        )

    def joint_pair(self, first, second, input_u, input_v, ln2):
        products = [self.node(v, "mul")["args"] for v in (first, second)]
        shared = set(products[0]) & set(products[1])
        require(len(shared) == 1, "Actual pair shares one radius")
        radius = next(iter(shared))
        positive = self.node(radius, "sqrt")["args"][0]
        product = self.node(positive, "positive")["args"][0]
        logarithm = self.node(product, "cmul", {"c": -2 * Q})["args"][0]
        addends = self.node(logarithm, "add")["args"]
        exponent_terms = [v for v in addends if self.node(v)["op"] == "cmul"]
        require(len(exponent_terms) == 1, "Unique integer exponent literal product")
        term = exponent_terms[0]
        scaled = self.node(term, "cmul", {"c": ln2})["args"][0]
        exponent = self.node(scaled, "bits", {"shift": -40, "width": 72, "signed": False})["args"][
            0
        ]
        top, f = self.node(exponent, "sub")["args"]
        self.constant(f, 40)
        safe = self.node(top, "msb")["args"][0]
        flag, tiny, midpoint_u = self.node(safe, "select")["args"]
        self.constant(tiny, 1)
        require(self.node(flag, "lt")["args"] == [midpoint_u, tiny], "Actual positive-input guard")
        self.midpoint(midpoint_u, input_u)
        polynomial = next(v for v in addends if v != term)
        lookups = {
            tuple(self.node(v)["out"])
            for v in self.ancestors(polynomial)
            if self.node(v)["op"] == "lookup"
        }
        require(len(lookups) == 1, "Unique original log lookup")
        address = self.node(next(iter(lookups))[0])["args"][0]
        shifted = self.node(address)["args"][0]
        bounded = self.node(shifted, "sub")["args"][0]
        mantissa = self.clamp(bounded, Q, 2 * Q - 1)
        u, negated = self.node(mantissa, "shift")["args"]
        require(u == safe, "Same positive midpoint is normalized")
        zero, same_exponent = self.node(negated, "sub")["args"]
        self.constant(zero, 0)
        require(same_exponent == exponent, "Exact normalization exponent")
        log_scope = self.interpolation(polynomial, "log", mantissa)
        cosines = [next(v for v in args if v != radius) for args in products]
        turns = []
        for cosine in cosines:
            lookups = {
                tuple(self.node(v)["out"])
                for v in self.ancestors(cosine)
                if self.node(v)["op"] == "lookup"
            }
            require(len(lookups) == 1, "Unique original cosine lookup")
            address = self.node(next(iter(lookups))[0])["args"][0]
            bounded = self.node(address)["args"][0]
            turns.append(self.clamp(bounded, 0, Q - 1))
        midpoint_v, wrapped = turns
        self.midpoint(midpoint_v, input_v)
        total = self.node(wrapped, "bits", {"shift": 0, "width": 40, "signed": False})["args"][0]
        args = self.node(total, "add")["args"]
        require(midpoint_v in args, "Both angles derive from same midpoint")
        self.constant(next(v for v in args if v != midpoint_v), 3 * Q // 4)
        scopes = [self.interpolation(v, "cos", a) for v, a in zip(cosines, turns, strict=True)]
        dependencies = {
            v
            for root in (first, second)
            for v in self.ancestors(root)
            if self.node(v)["op"] == "input"
        }
        require(dependencies == {input_u, input_v}, "Exactly two independent pair input words")
        return dict(
            normal_values=[first, second],
            raw_uniform_values=[input_u, input_v],
            radius=radius,
            log=log_scope,
            cosines=scopes,
            original_shared_pair_preserved=True,
        )

    def sum_terms(self, value, stops):
        pending, result = [value], Counter()
        while pending:
            check(self.started)
            current = pending.pop()
            if current in stops:
                result[current] += 1
            else:
                pending.extend(self.node(current, "add")["args"])
        return result


def removal_fixed_point(graph, native, scopes, started):
    candidates = set()
    boundaries = set().union(
        *(graph.ancestors(cosine["input"]) for scope in scopes for cosine in scope["cosines"])
    )
    outputs = {cosine["output"] for scope in scopes for cosine in scope["cosines"]}
    authorized = {
        (cosine["output"], normal)
        for scope in scopes
        for cosine, normal in zip(scope["cosines"], scope["normal_values"], strict=True)
    }
    pending = list(outputs)
    while pending:
        check(started)
        value = pending.pop()
        if value in boundaries or value in candidates:
            continue
        node = graph.node(value)
        require(node["op"] != "input", "Cosine closure must stop at its exact turns argument")
        candidates.update(node["out"])
        pending.extend(node["args"])
    consumers = {value: set() for value in graph.nodes}
    for node in graph.target["nodes"]:
        check(started)
        for argument in node["args"]:
            consumers[argument].update(node["out"])
    retained = set()
    for value in candidates:
        check(started)
        if (
            any(
                user not in candidates and (value, user) not in authorized
                for user in consumers[value]
            )
            or value in graph.target["outputs"]
        ):
            retained.add(value)
    pending = list(retained)
    while pending:
        check(started)
        value = pending.pop()
        node = graph.node(value)
        for dependency in [*node["out"], *node["args"]]:
            if dependency in candidates and dependency not in retained:
                retained.add(dependency)
                pending.append(dependency)
    removed = candidates - retained
    require(
        outputs <= removed,
        "Every old cosine output has only its authorized replacement product edge",
    )
    calls = []
    for index, call in enumerate(native["forward_calls"]):
        check(started)
        if set(call["out"]) & removed:
            require(
                set(call["out"]) <= removed,
                "Multioutput lookup is removed as a complete actual invocation",
            )
            calls.append(call)
    require(
        {value for call in calls for value in call["out"]} == removed,
        "Exact removed full72 value/call inventory",
    )
    return dict(
        removed_value_ids=sorted(removed),
        removed_forward_calls=calls,
        retained_shared_or_outside_value_ids=sorted(retained),
        authorized_cosine_output_to_radius_product_edges=[
            list(edge) for edge in sorted(authorized)
        ],
        actual_user_fixed_point=True,
        original_storage_subtracted=False,
    )


PRIMARY = PROGRAM / "A14_taylor_f44_stage_C_run003"
PRIMARY_MANIFEST_SHA = "7e68fca590bd18e396b8280ed1577ca5a8fc4df48e561f22eab17f0bec69b9fa"
PRIMARY_COUNTS = [34, 851, 2842]
PRIMARY_READY = ROOT / ".context/A14_F44_COSINE_STAGE_C_ROOT_READY_run003.json"
PRIMARY_AUTHORS = {
    "experiment_f44_cosine_stage_c_v3.py": (
        "9dc012f3015dfa0ac7301bc14fc7bf5a69fe2169aa6c4c122d9bd9b1df1dfee6"
    ),
    "A14_F44_COSINE_STAGE_C_IMPLEMENTATION_PREFLIGHT_V3.md": (
        "e90ec80968a596fb2b16c80369c60832abfef2aee501f5e4162d1f0251c4185b"
    ),
    "a14_f44_cosine_stage_c_implementation_preflight_v3.json": (
        "85f0d5b8c7be6763c93c74eefce6ca9cbd54464f41ea29987831cb41d3561b41"
    ),
    BUILDER.name: BUILDER_SHA,
    BUILDER_NOTE.name: BUILDER_NOTE_SHA,
}
AUDIT_SCALE, AUDIT_ATAN_TERMS, AUDIT_TRIG_TERMS = 1 << 512, 200, 224


def check(started, *, admission=False):
    budget(admission=admission)


def flags():
    return {
        "independent130_component_audit_only": True,
        "original_scientific_receipts_unchanged": True,
        "previous_A14_rejected_rows_unchanged": True,
        "full_G2": False,
        "adoption": False,
        "cost_transfer": False,
        "global_financial_gate_emission_authorized": False,
        "quantum_advantage": False,
        "new_test_credit": 0,
        "new_credited_gate_replays": 0,
        "new_price_samples": 0,
    }


def audit_pair(pair):
    require(
        type(pair) is list
        and len(pair) == 2
        and all(type(x) is int for x in pair)
        and pair[1] > 0
        and all(abs(x).bit_length() <= 65536 for x in pair),
        "Canonical bounded exact integer pair",
    )
    value = Fraction(pair[0], pair[1])
    require([value.numerator, value.denominator] == pair, "Reduced rational pair")
    return value


def audit_pair_encode(value):
    return [value.numerator, value.denominator]


def audit_ceil(numerator, denominator):
    quotient, remainder = divmod(numerator, denominator)
    return quotient + bool(remainder)


def audit_enclose_fraction(lower, upper=None):
    upper = lower if upper is None else upper
    require(lower <= upper, "Ordered independent interval")
    return (
        lower.numerator * AUDIT_SCALE // lower.denominator,
        audit_ceil(upper.numerator * AUDIT_SCALE, upper.denominator),
    )


def audit_product(left, right):
    products = (left[0] * right[0], left[0] * right[1], left[1] * right[0], left[1] * right[1])
    return min(products) // AUDIT_SCALE, audit_ceil(max(products), AUDIT_SCALE)


def audit_add(left, right):
    return left[0] + right[0], left[1] + right[1]


def audit_scale_interval(value, divisor):
    require(type(divisor) is int and divisor > 0, "Positive independent divisor")
    return value[0] // divisor, audit_ceil(value[1], divisor)


def audit_negate(value):
    return -value[1], -value[0]


def audit_interval_pairs(value):
    return Fraction(value[0], AUDIT_SCALE), Fraction(value[1], AUDIT_SCALE)


def audit_pi():
    enclosures = []
    for inverse in (5, 239):
        partial = Fraction(0)
        for k in range(AUDIT_ATAN_TERMS):
            budget(admission=True)
            partial += Fraction(1 if k % 2 == 0 else -1, (2 * k + 1) * inverse ** (2 * k + 1))
        next_partial = partial + Fraction(
            1, (2 * AUDIT_ATAN_TERMS + 1) * inverse ** (2 * AUDIT_ATAN_TERMS + 1)
        )
        require(AUDIT_ATAN_TERMS == 200, "Fixed even Machin truncation")
        enclosures.append((partial, next_partial))
    low = 16 * enclosures[0][0] - 4 * enclosures[1][1]
    high = 16 * enclosures[0][1] - 4 * enclosures[1][0]
    require(Fraction(3) < low < high < Fraction(16, 5), "Independent exact Machin containment")
    return audit_enclose_fraction(low, high), (low, high)


def audit_trigonometric(argument, sine):
    """Descending factored factorial recurrence with outward dyadic divisions."""
    require(
        0 <= argument[0] <= argument[1] < 7 * AUDIT_SCALE,
        "All independent center arguments below seven",
    )
    square = audit_product(argument, argument)
    polynomial = (AUDIT_SCALE, AUDIT_SCALE)
    for k in range(AUDIT_TRIG_TERMS - 2, -1, -1):
        budget(admission=True)
        offset = int(sine)
        divisor = (2 * k + offset + 1) * (2 * k + offset + 2)
        correction = audit_scale_interval(audit_product(square, polynomial), divisor)
        polynomial = audit_add((AUDIT_SCALE, AUDIT_SCALE), audit_negate(correction))
    if sine:
        polynomial = audit_product(polynomial, argument)
    order = 2 * AUDIT_TRIG_TERMS + int(sine)
    remainder = audit_enclose_fraction(Fraction(7**order, factorial(order)))[1]
    return polynomial[0] - remainder, polynomial[1] + remainder


def audit_mp_endpoint(word):
    sign, mantissa, exponent, bits = word
    require(
        type(sign) is int
        and sign in (0, 1)
        and type(mantissa) is int
        and type(exponent) is int
        and type(bits) is int
        and bits >= 0,
        "Finite independent numerical endpoint",
    )
    numerator = -mantissa if sign else mantissa
    return (
        Fraction(numerator << exponent, 1) if exponent >= 0 else Fraction(numerator, 1 << -exponent)
    )


def audit_mp_bounds(value):
    return tuple(audit_mp_endpoint(word) for word in value._mpi_)


def audit_coefficient_literals(mp, primary):
    require(
        primary["row_id"] == ROW_ID
        and primary["coefficient_count"] == 448
        and primary["center_count"] == 64
        and primary["table_literal_count"] == 512
        and len(primary["coefficient_rows"]) == 448
        and len(primary["center_rows"]) == 64
        and len(primary["table"]) == 64,
        "Entire original448+64 literal material",
    )
    pi, exact_pi = audit_pi()
    original_pi = tuple(audit_pair(x) for x in primary["exact_Machin_pi_enclosure"])
    require(
        original_pi[0] <= exact_pi[0] < exact_pi[1] <= original_pi[1],
        "Independent exact Machin enclosure lies in saved primary pi bounds",
    )
    twice_pi = audit_product(pi, audit_enclose_fraction(Fraction(2)))
    powers = [(AUDIT_SCALE, AUDIT_SCALE)]
    for _ in range(6):
        powers.append(audit_product(powers[-1], twice_pi))
    rows, errors, primary_errors = [], [], []
    for segment in range(64):
        budget(admission=True)
        center = Fraction(2 * segment + 1, 128)
        center_word = (2 * segment + 1) << 37
        require(
            primary["center_rows"][segment]
            == {"segment": segment, "raw": center_word, "center_exact": audit_pair_encode(center)}
            and len(primary["table"][segment]) == 8
            and primary["table"][segment][0] == center_word,
            "Every exact center and entire native table row",
        )
        angle = audit_product(twice_pi, audit_enclose_fraction(center))
        cosine, sine = audit_trigonometric(angle, False), audit_trigonometric(angle, True)
        numerical_center = mp.iv.mpf(center.numerator) / center.denominator
        trig = (
            mp.iv.cos(2 * mp.iv.pi * numerical_center),
            mp.iv.sin(2 * mp.iv.pi * numerical_center),
        )
        for degree in range(7):
            budget(admission=True)
            phase = degree % 4
            interval = cosine if phase in (0, 2) else sine
            numerical = trig[0] if phase in (0, 2) else trig[1]
            if phase in (1, 2):
                interval, numerical = audit_negate(interval), -numerical
            oracle = audit_interval_pairs(
                audit_scale_interval(audit_product(interval, powers[degree]), factorial(degree))
            )
            numerical_bounds = audit_mp_bounds(
                numerical * (2 * mp.iv.pi) ** degree / factorial(degree)
            )
            require(
                oracle[1] - oracle[0] < Fraction(1, 10**130),
                "Fixed512bit oracle meets130digit width",
            )
            require(
                numerical_bounds[0] <= oracle[0] <= oracle[1] <= numerical_bounds[1],
                "Fresh130 interval contains independent exact coefficient oracle",
            )
            saved = primary["coefficient_rows"][7 * segment + degree]
            declared = tuple(audit_pair(x) for x in saved["true_coefficient_enclosure"])
            raw = saved["raw"]
            require(
                (saved["segment"], saved["degree"], saved["center_raw"])
                == (segment, degree, center_word)
                and type(raw) is int
                and -(1 << 71) <= raw < 1 << 71
                and primary["table"][segment][degree + 1] == raw,
                "All actual primary words retained; no independent refit or new selection",
            )
            require(
                declared[0] <= numerical_bounds[0] <= numerical_bounds[1] <= declared[1],
                "Fresh independently authorized130 enclosure within primary90 enclosure",
            )
            midpoint = (declared[0] + declared[1]) * IQ / 2
            require(
                nearest_fraction(midpoint) == raw
                and audit_pair(saved["exact_rounding_reference"])
                == (declared[0] + declared[1]) / 2,
                "Original ties-even selection matches exact saved midpoint",
            )
            paid_primary = max(abs(Fraction(raw, IQ) - x) for x in declared)
            paid_independent = max(abs(Fraction(raw, IQ) - x) for x in numerical_bounds)
            require(
                audit_pair(saved["actual_abs_error_upper"]) == paid_primary
                and paid_independent <= paid_primary <= IEPS / 2
                and saved["true_nearest_half_ULP_certified"] is True
                and saved["primary90_contains_exact_oracle"] is True,
                "Every individual true halfULP premise freshly independently authorized",
            )
            errors.append(paid_independent)
            primary_errors.append(paid_primary)
            rows.append(
                {
                    "segment": segment,
                    "degree": degree,
                    "raw": raw,
                    "independent130_enclosure": [audit_pair_encode(x) for x in numerical_bounds],
                    "independent512bit_oracle": [audit_pair_encode(x) for x in oracle],
                    "independent_abs_error_upper": audit_pair_encode(paid_independent),
                    "all_containment_half_ULP_checks_passed": True,
                }
            )
    return (
        {
            "passed": True,
            "digits": 130,
            "oracle_bits": 512,
            "Machin_terms": 200,
            "trig_terms": 224,
            "rows": rows,
            "exact_pi": [audit_pair_encode(x) for x in exact_pi],
            "fixed_words_unchanged": True,
            "center_count": 64,
            "coefficient_count": 448,
        },
        errors,
        primary_errors,
        exact_pi,
    )


def audit_uniform(primary, independent_errors, primary_errors, exact_pi, binding):
    old = audit_pair(binding["existing_E_old"]["cosine_error_upper"])
    tail = (2 * exact_pi[1] * H) ** 7 / factorial(7)
    floor = sum((IEPS * H**k for k in range(6)), Fraction(0))
    final = EPS / 2
    limit = Fraction(1009, 1270) * EPS
    require(
        tail < EPS / 5
        and (IEPS / 2) * sum((H**k for k in range(7)), Fraction(0)) + floor
        < Fraction(12, 127) * EPS
        and limit < EPS <= old,
        "Independent paper majorants and original error ledger",
    )
    require(
        primary["row_id"] == ROW_ID
        and len(primary["all64_closed_segments"]) == 64
        and primary["closed_local_interval"] == [audit_pair_encode(-H), audit_pair_encode(H)]
        and audit_pair(primary["conditional_paper_upper"]) == limit
        and audit_pair(primary["original_E_old"]) == old,
        "Exact full primary uniform domain and original allowance",
    )
    records, primary_totals = [], []
    for segment in range(64):
        budget(admission=True)
        independent_paid = sum(
            (independent_errors[7 * segment + k] * H**k for k in range(7)), Fraction(0)
        )
        primary_paid = sum((primary_errors[7 * segment + k] * H**k for k in range(7)), Fraction(0))
        saved = primary["all64_closed_segments"][segment]
        primary_tail = audit_pair(saved["Taylor_tail_upper"])
        require(
            saved["segment"] == segment
            and audit_pair(saved["actual_literal_error_upper"]) == primary_paid
            and audit_pair(saved["six_floor_upper"]) == floor
            and audit_pair(saved["final_signed_ties_even_rounding_upper"]) == final
            and tail <= primary_tail,
            "Every primary64-component ledger independently consumed",
        )
        primary_total = primary_paid + primary_tail + floor + final
        independent_total = independent_paid + tail + floor + final
        require(
            audit_pair(saved["cosine_error_upper"]) == primary_total
            and independent_total <= primary_total < limit < old,
            "All closed segments independently meet uniform gate",
        )
        primary_totals.append(primary_total)
        records.append(
            {
                "segment": segment,
                "cosine_error_upper": audit_pair_encode(independent_total),
                "literal_error_upper": audit_pair_encode(independent_paid),
                "tail_upper": audit_pair_encode(tail),
                "six_floors_upper": audit_pair_encode(floor),
                "final_rounding_upper": audit_pair_encode(final),
            }
        )
    require(
        audit_pair(primary["cosine_error_upper"]) == max(primary_totals)
        and primary["uniform_component_gate_passed"] is True,
        "Entire primary uniform maximum and acceptance independently verified",
    )
    return {
        "passed": True,
        "rows": records,
        "all64_closed_segments": True,
        "projection_and_exact_axes_nonexpansive": True,
        "cosine_error_upper": audit_pair_encode(
            max(audit_pair(x["cosine_error_upper"]) for x in records)
        ),
        "original_E_old": audit_pair_encode(old),
        "no_financial_allowance_transfer": True,
    }


def audit_native(table, primary):
    require(
        primary["row_id"] == ROW_ID and len(primary["segment_rows"]) == 64,
        "All original64 native segments present",
    )
    records = []
    for segment, row in enumerate(table):
        budget(admission=True)
        source_low, source_high = segment * (1 << 34), (segment + 1) * (1 << 34) - 1
        center = row[0]
        scaled = source_low * 16, source_high * 16
        local = scaled[0] - center, scaled[1] - center
        require(
            center == (2 * segment + 1) << 37
            and local == (-(1 << 37), (1 << 37) - 16)
            and center % 16 == 0
            and all(type(x) is int and -(1 << 51) <= x < 1 << 51 for x in row[1:])
            and 0 <= source_low <= source_high < Q
            and 0 <= scaled[0] <= scaled[1] < 1 << 71,
            "Independent full address/rescale/local/sign-extension caller proof",
        )
        interval = row[7], row[7]
        steps = []
        for degree in range(5, -1, -1):
            budget(admission=True)
            require(
                -(1 << 51) <= interval[0] <= interval[1] < 1 << 51,
                "Every eager first operand signed52",
            )
            corners = tuple(a * b for a in interval for b in local)
            product = min(corners), max(corners)
            require(
                -(1 << 89) <= product[0] <= product[1] < 1 << 89,
                "Full signed144 product lies in active signed90 and retained116 domain",
            )
            quotient = product[0] // (1 << 44), product[1] // (1 << 44)
            result = quotient[0] + row[degree + 1], quotient[1] + row[degree + 1]
            require(
                -(1 << 71) <= quotient[0] <= quotient[1] < 1 << 71
                and -(1 << 71) <= result[0] <= result[1] < 1 << 71,
                "Raw full72 floor and addition never wrap",
            )
            steps.append(
                {
                    "degree": degree,
                    "accumulator_operand_raw_interval": list(interval),
                    "signed52_operand_authorized": True,
                    "local_signed38_raw_interval": list(local),
                    "semantic_signed144_and_retained116_product_interval": list(product),
                    "signed90_product_safe": True,
                    "floor44_output_interval": list(quotient),
                    "signed72_floor_output_safe": True,
                    "exact_add_output_interval": list(result),
                    "signed72_add_safe": True,
                }
            )
            interval = result
        rounded = (
            nearest_fraction(Fraction(interval[0], 16)),
            nearest_fraction(Fraction(interval[1], 16)),
        )
        require(
            -(1 << 71) <= rounded[0] <= rounded[1] < 1 << 71,
            "Monotone signed ties-even endpoints safe",
        )
        expected = {
            "segment": segment,
            "exact_eager_u_interval": [source_low, source_high],
            "rescaled_F44_raw_interval": list(scaled),
            "center44_raw": center,
            "all_initial_rescale_center_local_literal_promises": True,
            "derived_digital_local_raw_interval": list(local),
            "Horner_steps": steps,
            "final_round_input_interval": list(interval),
            "round_output_interval": list(rounded),
            "all_eager_native_promises_passed": True,
        }
        require(
            primary["segment_rows"][segment] == expected,
            "Every complete native segment record independently reconstructed",
        )
        records.append(expected)
    require(
        primary["all64_native_promises_passed"] is True
        and primary["signed_clamp_0_to_Q_before_eager_work"] is True
        and primary["Q_selected_to_zero_before_lookup"] is True
        and primary["address_high66_bits_zero"] is True
        and primary["local_low_four_bits_zero"] is True
        and primary["hypothetical_closed_positive_endpoint_not_native_caller"] is True
        and primary["final_projected_signed72_output_interval"] == [-Q, Q],
        "Universal full72 clamp and digital native promises unchanged",
    )
    return {
        "passed": True,
        "segment_rows": records,
        "changed_public_clamp_Q_map_not_original_equivalence": True,
    }


def independent_input_bytes(path):
    return admitted_bytes(path, maximum=MAX_OWN_BYTES)


def audit_native_payload(path, rows, qubits, numpy_header=False):
    require(
        type(rows) is int and 0 < rows <= 2000000 and type(qubits) is int and 0 < qubits <= 16384,
        "Finite complete native payload contract",
    )
    data = independent_input_bytes(path)
    offset = 0
    if numpy_header:
        require(
            data[:6] == b"\x93NUMPY" and data[6:8] in (b"\x01\x00", b"\x02\x00"),
            "Only exact native NPY1/2 envelopes",
        )
        header_bytes = 2 if data[6] == 1 else 4
        header_length = int.from_bytes(data[8 : 8 + header_bytes], "little")
        offset = 8 + header_bytes + header_length
        require(header_length <= 4096 and offset <= len(data), "Bounded complete NPY header")
        header = ast.literal_eval(data[8 + header_bytes : offset].decode("latin1"))
        require(
            header == {"descr": "<i4", "fortran_order": False, "shape": (rows, 4)},
            "Exact little-endian int32 row-major array, no dtype conversion",
        )
    require(
        sys.byteorder == "little" and array("i").itemsize == 4 and len(data) - offset == 16 * rows,
        "All and only complete native rows",
    )
    words = array("i")
    words.frombytes(data[offset:])
    for index in range(rows):
        if index % 128 == 0:
            budget(admission=True)
        kind, a, b, c = words[4 * index : 4 * index + 4]
        operands = (a, b, c)[:kind]
        require(
            kind in (1, 2, 3)
            and len(set(operands)) == kind
            and all(0 <= wire < qubits for wire in operands)
            and all(x == 0 for x in (a, b, c)[kind:]),
            "Every full native opcode/wire/padding value independent validation",
        )
    budget(admission=True)
    return words


def audit_admitted_leaves(binding):
    leaves = {}
    for operation in ("ADD", "SUB"):
        profile = binding["cases"]["B4x12"]["selected_primitive_profiles"][operation]
        second = binding["cases"]["B8x52"]["selected_primitive_profiles"][operation]
        require(
            profile == second and not profile.get("resource_rejected"),
            "One identical independently authorized original BK72 leaf",
        )
        entries = read(ROOT / profile["descriptor_path"])
        require(type(entries) is list, "Actual full original descriptor list")
        selected = [
            entry
            for entry in entries
            if (entry["op"], entry["width"], entry["variant"])
            == (operation.lower(), 72, "brent-kung")
        ]
        require(len(selected) == 1, "One exact generic full72 native leaf")
        descriptor = selected[0]
        require(
            descriptor["args"] == [list(range(72)), list(range(72, 144))]
            and descriptor["outs"] == [list(range(144, 216))]
            and descriptor["resources"] == profile["resources"]
            and descriptor["spec"]["lowering"] == "clean-xor-prefix-add-sub-v1"
            and not descriptor["spec"].get("input_contract"),
            "Exact admitted unrestricted ADD/SUB clean ABI",
        )
        path = canonical(ROOT / profile["gate_path"])
        require(
            _FROZEN[key_for(path)] == profile["gate_sha256"], "Original saved raw expected leaf SHA"
        )
        leaves[operation] = {
            "descriptor": descriptor,
            "gate_SHA256": profile["gate_sha256"],
            "words": audit_native_payload(
                path,
                descriptor["resources"]["source_gates"],
                descriptor["resources"]["qubits"],
                True,
            ),
        }
    descriptors, arrays = (
        read(SOURCE / "primitive_descriptors.json"),
        read(SOURCE / "native_gate_arrays.json"),
    )
    for operation, key in (("MUL", "multiplier"), ("ROUND", "rounder")):
        descriptor, record = descriptors[key], arrays[key]
        arity = 2 if operation == "MUL" else 1
        require(
            descriptor["schema"] == "a14-f44-stage-k-clean-arithmetic-leaf-v1"
            and descriptor["spec"]["width"] == 72
            and descriptor["args"] == [list(range(72 * j, 72 * (j + 1))) for j in range(arity)]
            and descriptor["outs"] == [list(range(72 * arity, 72 * (arity + 1)))]
            and descriptor["input_preserved"] is True
            and descriptor["dirty_output_XOR"] is True
            and descriptor["private_workspace_zero_entry_exit"] is True,
            "Full72 previously independently proved K clean ports",
        )
        if operation == "MUL":
            require(
                descriptor["spec"]["fraction_bits"] == 44
                and descriptor["spec"]["product_width"] == 116
                and descriptor["spec"]["active_operand_bits"] == [52, 38]
                and descriptor["spec"]["input_contract"] == {"signed_operand_bits": [52, 38]}
                and descriptor["full_signed_semantic_product_bits"] == 144
                and descriptor["generic_active_signed_product_bits"] == 90,
                "Exact newly paid signed52x38/F44 K multiplier domain",
            )
        else:
            require(
                descriptor["spec"]["input_fraction_bits"] == 44
                and descriptor["spec"]["output_fraction_bits"] == 40
                and descriptor["spec"]["input_contract"] == {},
                "Universal signed ties-even K rounder",
            )
        path = canonical(SOURCE / record["gate_file"])
        require(
            _FROZEN[key_for(path)] == record["gate_SHA256"]
            and record["rows"] == descriptor["gate_rows"],
            "Actual K independent descriptor/full-binary expected binding",
        )
        leaves[operation] = {
            "descriptor": descriptor,
            "gate_SHA256": record["gate_SHA256"],
            "words": audit_native_payload(path, record["rows"], descriptor["qubits"]),
        }
    return leaves


def audit_source_binding():
    original = read(PROGRAM / "A14_cosine_feasibility_run001/source_binding.json")
    independent = read(
        PROGRAM / "A14_cosine_feasibility_audit_run003/independent_source_binding.json"
    )
    primary = read(PRIMARY / "original_source_binding.json")
    require(
        primary == original and independent == original,
        "Unchanged complete original primary/independent/StageC source binding",
    )
    normal_certificate = read(PROGRAM / "C06_pair_run001/certificate.json")
    old_cosine_table = None
    for case, (assets, dates, pairs) in CASES.items():
        budget(admission=True)
        saved = original["cases"][case]
        target, native, schedule = (
            read(ROOT / saved[name]) for name in ("target_path", "source_path", "schedule_path")
        )
        graph = GraphAudit(target, (0, _STARTED))
        inputs = [node for node in target["nodes"] if node["op"] == "input"]
        require(
            len(inputs) == 2 * pairs == dates * (assets + 1),
            "Complete original pair preparation roles",
        )
        for index, item in enumerate(inputs):
            require(
                item["params"]
                == {"name": "uniform_" + str(index), "bits": 32, "preparation": "uniform"},
                "Exact original q32 midpoint source roles",
            )
        normals = normal_certificate["source_bindings"][case]["normal_values"]
        require(
            normals == saved["normal_values"] and len(normals) == 2 * pairs,
            "Original independently bound pair output identities",
        )
        scopes = [
            graph.joint_pair(
                normals[2 * j],
                normals[2 * j + 1],
                inputs[2 * j]["out"][0],
                inputs[2 * j + 1]["out"][0],
                normal_certificate["source_bindings"][case]["literal_ln2"],
            )
            for j in range(pairs)
        ]
        require(
            scopes == saved["pair_scopes"]
            and removal_fixed_point(graph, native, scopes, (0, _STARTED)) == saved["removal"],
            "Fresh independent SSA/user closure matches every original removal and pair",
        )
        require(
            native["resources"] == saved["original_resources"]
            and schedule == saved["original_measured_schedule"]
            and [schedule["resources"][k] for k in ("t_count", "t_depth", "logical_qubits")]
            == list(BASELINE[case]),
            "Exact original serial resources and separate measured capped baseline",
        )
        if old_cosine_table is None:
            old_cosine_table = target["tables"]["cos"]
        require(
            target["tables"]["cos"] == old_cosine_table,
            "Every original512 cosine words stay identical",
        )
    envelope = read(ROOT / original["existing_E_old"]["path"])
    require(len(envelope["coefficient_checks"]) == 512, "All original512 literal-error obligations")
    errors = [Fraction(0)] * 64
    for index, check_row in enumerate(envelope["coefficient_checks"]):
        budget(admission=True)
        segment, degree = divmod(index, 8)
        require(
            (check_row["row"], check_row["degree"], check_row["raw"])
            == (segment, degree, old_cosine_table[segment][degree]),
            "All actual original literal identities",
        )
        lo, hi = tuple(audit_pair(x) for x in check_row["exact_coefficient_enclosure"])
        paid = max(abs(Fraction(check_row["raw"], Q) - lo), abs(Fraction(check_row["raw"], Q) - hi))
        require(
            audit_pair(check_row["actual_literal_error_upper"]) == paid,
            "Original literal ledger exact rational arithmetic",
        )
        errors[segment] += paid * H**degree
    old_floor = EPS * sum((H**degree for degree in range(7)), Fraction(0))
    old = max(errors) + old_floor + audit_pair(envelope["Taylor_degree7_remainder_upper"])
    require(
        old
        == audit_pair(envelope["cosine_error_upper"])
        == audit_pair(original["existing_E_old"]["cosine_error_upper"])
        and max(errors) == audit_pair(envelope["literal_rounding_upper"])
        and old_floor == audit_pair(envelope["Horner_floor_upper"])
        and EPS <= old,
        "Entire original seven-floor E_old formula freshly consumed",
    )
    return original


def audit_cost_catalog(binding):
    owner_path = PROGRAM / "A10_coefficient_run001/manifest.json"
    require(
        _FROZEN[key_for(owner_path)]
        == "0a732d7f487bca1efd298e7eca4feb2f2d2e83d1958ebb9a14ee9b32a0d78a40",
        "Only exact immutable original flat A10 owner allows selected separator interpretation",
    )
    owner = read(owner_path)
    result, memberships = {}, {}
    for case in CASES:
        route = owner_path.parent / case / "min-depth"
        native = read(ROOT / binding["cases"][case]["source_path"])
        catalog, case_memberships = {}, {}
        for call in native["forward_calls"]:
            budget()
            leaf = call["leaf"]
            require(
                type(leaf) is str
                and len(leaf) == 20
                and all(ch in "0123456789abcdef" for ch in leaf),
                "Exact original content key",
            )
            if leaf in catalog:
                continue
            path = route / "leaves" / (leaf + ".json")
            relative = path.relative_to(owner_path.parent).as_posix()
            selected = [
                (key, expected)
                for key, expected in owner.items()
                if type(key) is str and key.replace("\\", "/") == relative
            ]
            require(len(selected) == 1, "Unique original flat selected descriptor membership")
            key, expected = selected[0]
            require(
                _FROZEN[key_for(path)] == expected,
                "Every actual selected descriptor already primary expected input",
            )
            entry = read(path)
            require(
                entry["resources"]["schedule"]
                == "exact seven-T Toffoli; all-to-all ASAP within each leaf"
                and entry["resources"]["t_count"] == 7 * entry["resources"]["ccx"],
                "Same absolute exact7T leaf convention",
            )
            catalog[leaf] = entry
            case_memberships[leaf] = {
                "owner_manifest": key_for(owner_path),
                "owner_manifest_SHA256": _FROZEN[key_for(owner_path)],
                "original_key": key,
                "original_expected_SHA256": expected,
                "actual_selected_path": key_for(path),
            }
        result[case], memberships[case] = catalog, case_memberships
    return result, memberships


def audit_whole_source_cost(binding, descriptor, resources, saved):
    catalog, memberships = audit_cost_catalog(binding)
    serial = resources["matched_serial_event_chronology"]["sums"]
    clean = {key: serial[key] if key in serial else resources[key] for key in RESOURCE_FIELDS}
    require(
        clean["source_gates"] == descriptor["gate_rows"]
        and clean["t_count"] == resources["t_count"],
        "Same actual whole prototype counts and conservative matched serial-event schedule",
    )
    cases = {}
    for case in CASES:
        budget(admission=True)
        old = binding["cases"][case]
        native = read(ROOT / old["source_path"])
        forward = {key: 0 for key in RESOURCE_FIELDS}
        copies, copy_depth = 0, 0
        for call in native["forward_calls"]:
            budget()
            unit = catalog[case][call["leaf"]]["resources"]
            for key in RESOURCE_FIELDS:
                forward[key] += unit[key]
            copies += call["argument_copy_cx"]
            copy_depth += max(Counter(call["args"]).values(), default=0)
        baseline = {key: 2 * value for key, value in forward.items()}
        for key in ("source_gates", "cx", "clifford_cx"):
            baseline[key] += 2 * copies + 72 * len(native["outputs"])
        baseline["clifford_t_depth"] += 4 * copy_depth + max(
            Counter(native["outputs"].values()).values(), default=0
        )
        require(
            baseline == {key: old["original_resources"][key] for key in RESOURCE_FIELDS},
            "All original ordered leaf/copy/output costs reconstruct the complete serial baseline",
        )
        removed = {key: 0 for key in RESOURCE_FIELDS}
        for call in old["removal"]["removed_forward_calls"]:
            budget()
            require(
                call["argument_copy_cx"] == 144 * len(call["args"]),
                "All original removed full argument copies",
            )
            unit = catalog[case][call["leaf"]]["resources"]
            for key in RESOURCE_FIELDS:
                removed[key] += unit[key]
            for key in ("source_gates", "cx", "clifford_cx"):
                removed[key] += call["argument_copy_cx"]
            removed["clifford_t_depth"] += 2 * max(Counter(call["args"]).values(), default=0)
        sites = old["cosine_sites"]
        require(sites == CASE_SITES[case], "All60/468 charged cosine sites")
        outer = {key: 0 for key in RESOURCE_FIELDS}
        outer.update(source_gates=144, cx=144, clifford_t_depth=2, clifford_cx=144)
        added = {key: 2 * sites * (clean[key] + outer[key]) for key in RESOURCE_FIELDS}
        estimate = {key: baseline[key] - 2 * removed[key] + added[key] for key in RESOURCE_FIELDS}
        require(
            all(value >= 0 for value in estimate.values()), "No unmatched whole-source subtraction"
        )
        whole_qubits = old["original_resources"]["logical_qubits"] + descriptor["qubits"] - 144 + 72
        within = descriptor["qubits"] <= 131072 and whole_qubits <= BASELINE[case][2]
        improve = (
            estimate["t_count"] < baseline["t_count"] and estimate["t_depth"] < baseline["t_depth"]
        )
        expected = {
            "original_whole_source": baseline,
            "reconstructed_original_serial_baseline": baseline,
            "all_original_actual_leaf_memberships": memberships[case],
            "removed_twice": {key: 2 * value for key, value in removed.items()},
            "added_twice_complete_clean_plus_outercopies": added,
            "estimated_whole_source": estimate,
            "whole_qubits_conservative": whole_qubits,
            "standalone_clean_qubits": descriptor["qubits"],
            "new_full_SSA_private_history_banks": descriptor["SSA_full72_banks"],
            "actual_reused_private_bank_qubits": descriptor["full72_private_leaf_capacity"],
            "all_original_storage_and_scratch_retained": True,
            "outer_argument_bank_and_both144CX_copies_paid": True,
            "both_global_directions_paid": True,
            "within_original_caps": within,
            "T_count_and_matched_serial_T_depth_improve": improve,
            "original_measured_depth_context_only": BASELINE[case][1],
            "resource_gate_passed": within and improve,
        }
        require(
            saved["cases"][case] == expected,
            "Every saved whole-source resource field independently reconstructed",
        )
        cases[case] = expected
    require(
        saved["matched_serial_clean_function_resource"] == clean
        and saved["all_resource_gates_passed"]
        is all(value["resource_gate_passed"] for value in cases.values()),
        "Full resource gate, including valid rejection, independently reproduced",
    )
    return {
        "passed": True,
        "matched_serial_clean_function_resource": clean,
        "cases": cases,
        "all_resource_gates_passed": all(value["resource_gate_passed"] for value in cases.values()),
        "actual_capped_changed_financial_schedule_realized": False,
    }


def audit_release(ready_sha):
    require(
        PRIMARY_MANIFEST_SHA is not None and PRIMARY_COUNTS is not None,
        "Actual completed ROOT-supplied producer pin required, never observed-as-expected",
    )
    ready = read(bind(READY, ready_sha))
    require(
        ready["schema"] == "root-a14-f44-cosine-stage-c-audit-READY-v1"
        and ready["root_and_independent_static_reviews_passed"] is True
        and ready["independent130_component_audit_execution_authorized"] is True
        and ready["output"] == OUTPUT.relative_to(ROOT).as_posix()
        and ready["limits_CPU_admission_wall"] == [300, 270, 900]
        and ready["producer_manifest_SHA256"] == PRIMARY_MANIFEST_SHA
        and ready["producer_complete_counts"] == PRIMARY_COUNTS,
        "Exact separate independent-auditor external ROOT release",
    )
    for key in (
        "full_G2",
        "adoption",
        "cost_transfer",
        "quantum_advantage",
        "global_financial_gate_emission_authorized",
    ):
        require(
            ready[key] is False,
            "Independent component only, no financial/adoption/emission release",
        )
    require(ready["new_test_credit"] == 0, "No fixture or replay credit")
    authors = ready["author_method_SHA256"]
    require(
        type(authors) is dict and set(authors) == {AUTHOR.name, METHOD_DOC.name, PREFLIGHT.name},
        "Exactly the new independently reviewed three author files",
    )
    for name, expected in authors.items():
        bind(RESEARCH / name, expected)
    policy = read(PREFLIGHT)
    require(
        policy["schema"] == "a14-f44-stage-c-independent-audit-preflight-v1"
        and policy["author_SHA256"] == authors[AUTHOR.name]
        and policy["method_document_SHA256"] == authors[METHOD_DOC.name],
        "Exact author method pins",
    )
    for key, expected in {
        "producer_manifest_SHA256": PRIMARY_MANIFEST_SHA,
        "producer_complete_counts": PRIMARY_COUNTS,
        "limits_CPU_admission_wall": [300, 270, 900],
        "digits": 130,
        "oracle_bits": 512,
        "Machin_atan_terms": 200,
        "trig_Taylor_terms": 224,
        "integer_decimal_digit_limit": 20000,
        "integer_serialization_bit_cap": 65536,
        "owned_caps_files_bytes": [64, MAX_OWN_BYTES],
        "runtime_caps_files_bytes": [24000, MAX_RUNTIME_BYTES],
        "bookkeeping_caps": [100000, MAX_UNIQUE_BYTES, MAX_HASH_WORK],
        "bit_sliced_batch_case_counts": [32, 8],
        "physical_forward_reverse_sweeps": [2, 2],
        "row_id": ROW_ID,
        "native_rows_cap": MAX_NATIVE_ROWS,
        "native_wire_cap": 16384,
        "output": OUTPUT.relative_to(ROOT).as_posix(),
        "completed_prerequisite_manifest_SHA256": {
            **{name: packet[0] for name, packet in COSINE_PACKETS.items()},
            SOURCE_NAME: SOURCE_SHA,
            AUDIT_NAME: AUDIT_SHA,
            ROOT_INTEGRITY_NAME: ROOT_INTEGRITY_SHA,
        },
        "completed_prerequisite_complete_counts": {
            **{name: packet[1] for name, packet in COSINE_PACKETS.items()},
            SOURCE_NAME: SOURCE_COUNTS,
            AUDIT_NAME: AUDIT_COUNTS,
            ROOT_INTEGRITY_NAME: ROOT_INTEGRITY_COUNTS,
        },
    }.items():
        require(
            policy[key] == ready[key] == expected,
            "Fixed unchanged independent method limits and corpus",
        )
    primary = packet(PRIMARY.name, PRIMARY_MANIFEST_SHA, PRIMARY_COUNTS)
    require(
        primary["schema"] == "a14-f44-stage-c-primary90-manifest-v3"
        and primary["integer_decimal_digit_limit"] == 20000
        and primary["integer_serialization_bit_cap"] == 65536
        and primary["row_status"]
        in ("REJECTED", "COMPONENT_SCREEN_ELIGIBLE_PENDING_INDEPENDENT130"),
        "Completed primary method receipt is distinct from candidate eligibility",
    )
    for name, expected in PRIMARY_AUTHORS.items():
        require(
            _FROZEN[(RESEARCH / name).relative_to(ROOT).as_posix()] == expected,
            "All five original V3 author bytes, never substituted",
        )
    primary_ready = read(PRIMARY_READY)
    require(
        primary_ready["schema"] == "root-a14-f44-cosine-stage-c-READY-v3"
        and primary_ready["author_method_SHA256"] == PRIMARY_AUTHORS,
        "Original V3 release bytes externally inherited through full primary expected maps",
    )
    code_caches(
        [RESEARCH / "experiment_f44_cosine_stage_c_v3.py", BUILDER],
        primary_ready["existing_new_code_cache_SHA256"],
        primary_ready["absent_new_code_cache_paths"],
    )
    for name, (pin, counts) in COSINE_PACKETS.items():
        packet(name, pin, counts)
    packet(SOURCE_NAME, SOURCE_SHA, SOURCE_COUNTS)
    packet(AUDIT_NAME, AUDIT_SHA, AUDIT_COUNTS)
    packet(ROOT_INTEGRITY_NAME, ROOT_INTEGRITY_SHA, ROOT_INTEGRITY_COUNTS)
    native_audit = read(AUDIT / "summary.json")
    require(
        native_audit["schema"] == "a14-taylor-f44-stage-k-audit-summary-v1"
        and native_audit["source_manifest_SHA256"] == SOURCE_SHA
        and all(
            native_audit[key] is True
            for key in (
                "completed",
                "passed",
                "independent_scientific_audit_complete",
                "actual_array_matched_universal_structure",
                "actual_binary_independent_replay",
                "actual_resource_recount",
                "absolute7T_phase_proof_bound",
            )
        )
        and native_audit["Stage_C_release_authorized"] is False,
        "Completed independent native-leaf proof is a scoped composition premise",
    )
    native_root = read(PROGRAM / ROOT_INTEGRITY_NAME / "summary.json")
    require(
        native_root["schema"] == "a14-taylor-f44-stage-k-root-integrity-summary-v1"
        and native_root["source_manifest_SHA256"] == SOURCE_SHA
        and native_root["audit_manifest_SHA256"] == AUDIT_SHA
        and native_root["source_complete_counts"] == SOURCE_COUNTS
        and native_root["audit_complete_counts"] == AUDIT_COUNTS
        and all(
            native_root[key] is True
            for key in (
                "completed",
                "passed",
                "metadata_integrity_only",
                "original_scientific_receipts_integrity_verified",
                "saved_diagnostic_and_resource_metadata_reconciled",
            )
        )
        and native_root["new_scientific_evaluation"] is False
        and native_root["Stage_C_release_authorized"] is False,
        "Exact final native-leaf integrity preserves the separate Stage C release boundary",
    )
    preserved_prerequisite_caches()
    admit_prior_failure(ready, policy)
    code_caches(
        [AUTHOR], ready["existing_new_code_cache_SHA256"], ready["absent_new_code_cache_paths"]
    )
    executables = {canonical(LAUNCHER), canonical(Path(sys._base_executable))}
    admitted = set()
    for spelling, expected in ready["interpreter_expected_SHA256"].items():
        actual = canonical(spelling)
        require(
            actual in executables and actual not in admitted,
            "Exact actual distinct interpreter pins",
        )
        bind(actual, expected)
        admitted.add(actual)
    require(
        admitted == executables and len(executables) == 2, "Both actual interpreter expectations"
    )
    return primary


def audit_load_numerics():
    global _SCIENCE_ADMITTED
    require(
        not _SCIENCE_ADMITTED and BUILDER_MODULE not in sys.modules,
        "No builder or historical scientific source execution",
    )
    check_code_caches()
    require(
        standard_runtime_members() == _STANDARD_RUNTIME_MEMBERS,
        "Full runtime membership before numerical import",
    )
    loaded_origins()
    _SCIENCE_ADMITTED = True
    import mpmath as mp

    require(
        mp.__version__ == "1.3.0" and mp.libmp.BACKEND == "python",
        "Pinned purePython numerical package",
    )
    mp.mp.dps = mp.iv.dps = 130
    require(mp.mp.dps == mp.iv.dps == 130, "Exactly fixed130 numerical precision")
    loaded_origins()
    check_code_caches()
    budget(admission=True)
    return mp


def audit_producer_summary(row, uniform, native, costs):
    summary = read(PRIMARY / "summary.json")
    require(
        summary["schema"] == "a14-f44-stage-c-primary90-summary-v3"
        and summary["completed"] is True
        and summary["passed"] is True
        and summary["budget_censored"] is False
        and summary["row"] == row
        and summary["primary_digits"] == 90
        and summary["independent_digits_pending"] == 130
        and summary["coefficient_count"] == 448
        and summary["center_count"] == 64
        and summary["actual_prototype_completed"] is True
        and summary["fixed_native_diagnostic_counts_if_emitted"] == [32, 8]
        and summary["actual_native_replay_counts"] == [64, 16],
        "Entire actual completed primary diagnostic scope, not reused audit evidence",
    )
    eligible = uniform["passed"] and native["passed"] and costs["all_resource_gates_passed"]
    require(
        row["row_id"] == ROW_ID
        and row["uniform_component_gate_passed"] is True
        and row["all64_native_promises_passed"] is True
        and row["resource_gate_passed"] is costs["all_resource_gates_passed"]
        and row["candidate_eligible"] is eligible
        and row["status"]
        == ("COMPONENT_SCREEN_ELIGIBLE_PENDING_INDEPENDENT130" if eligible else "REJECTED"),
        "Resource rejection preserved independently despite mathematical component validity",
    )
    return eligible


def main():
    global _STARTED
    _STARTED = process_started()
    runtime_scopes()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ready-sha256", required=True)
    args = parser.parse_args()
    require(
        canonical(__file__) == AUTHOR and not OUTPUT.exists(),
        "One fresh immutable independent audit route",
    )
    try:
        fixed_integer_policy()
        for name in ("MPMATH_NOGMPY", "MPMATH_NOSAGE"):
            require(name not in os.environ, "No inherited optional numerical backend override")
            os.environ[name] = "1"
        for name in (
            "OMP_NUM_THREADS",
            "OPENBLAS_NUM_THREADS",
            "MKL_NUM_THREADS",
            "NUMEXPR_NUM_THREADS",
        ):
            require(
                os.environ.get(name) in (None, "1"),
                "One numerical thread, no inherited parallel override",
            )
            os.environ[name] = "1"
        audit_release(args.ready_sha256)
        package = package_runtime()
        runtime = own_runtime()
        loaded_origins()
        check_code_caches()
        first = fresh_union()
        budget(admission=True)
        OUTPUT.mkdir(exist_ok=False)
        for path in (AUTHOR, METHOD_DOC, PREFLIGHT, READY):
            copy(path, "executed_" + path.name)
        save(
            "run_started.json",
            {"PID": os.getpid(), "limits_CPU_admission_wall": [300, 270, 900], **flags()},
        )
        save("serialization_edge_diagnostics.json", serialization_edge_diagnostics())
        mp = audit_load_numerics()
        binding = audit_source_binding()
        save(
            "independent_source_binding_audit.json",
            {"passed": True, "complete_source_binding": binding, **flags()},
        )
        literals = read(PRIMARY / "primary90_literals.json")
        literal_audit, errors, primary_errors, pi = audit_coefficient_literals(mp, literals)
        save("independent130_literal_audit.json", literal_audit)
        uniform = audit_uniform(
            read(PRIMARY / "uniform_certificate.json"), errors, primary_errors, pi, binding
        )
        save("independent_uniform_audit.json", uniform)
        native = audit_native(literals["table"], read(PRIMARY / "all64_native_certificate.json"))
        save("independent_native_audit.json", native)
        leaves = audit_admitted_leaves(binding)
        descriptor = read(PRIMARY / "prototype_descriptor.json")
        array_record = read(PRIMARY / "native_gate_array.json")
        require(
            array_record["rows"] == descriptor["gate_rows"]
            and array_record["bytes"] == 16 * descriptor["gate_rows"]
            and array_record["row_format"] == "little-endian int32 Nx4 X/CX/CCX",
            "Same complete saved prototype descriptor and actual full array",
        )
        binary_path = canonical(PRIMARY / array_record["gate_file"])
        require(
            _FROZEN[key_for(binary_path)] == array_record["gate_SHA256"],
            "External expected complete primary array SHA",
        )
        words = audit_native_payload(binary_path, descriptor["gate_rows"], descriptor["qubits"])
        phase = c130_ccx_absolute_phase()
        save("independent_absolute_phase_audit.json", phase)
        structural = c130_gate_binding(words, descriptor, literals["table"], leaves)
        save("independent_gate_array_audit.json", structural)
        diagnostics = c130_fixed_diagnostics(
            words,
            descriptor,
            literals["table"],
            leaves["ROUND"]["words"],
            leaves["ROUND"]["descriptor"],
        )
        save("independent_bit_sliced_diagnostics.json", diagnostics)
        resources = c130_resources(words, descriptor)
        saved_resources = read(PRIMARY / "actual_prototype_resources.json")
        require(
            resources == saved_resources,
            "Every complete actual ASAP and serial-event resource field independently reproduced",
        )
        save("independent_actual_resources.json", resources)
        costs = audit_whole_source_cost(
            binding, descriptor, resources, read(PRIMARY / "whole_source_resource_comparison.json")
        )
        save("independent_whole_source_cost_audit.json", costs)
        eligible = audit_producer_summary(
            read(PRIMARY / "fixed_frontier_row.json"), uniform, native, costs
        )
        loaded_origins()
        check_code_caches()
        second = fresh_union()
        summary = {
            "schema": "a14-f44-stage-c-independent130-summary-v1",
            "completed": True,
            "passed": True,
            "budget_censored": False,
            "producer_manifest_SHA256": PRIMARY_MANIFEST_SHA,
            "producer_complete_counts": PRIMARY_COUNTS,
            "independent_digits": 130,
            "all448_true_coefficients_and64_centers_authorized": True,
            "all64_uniform_and_native_segments_independently_authorized": True,
            "complete_saved_array_structure_absolute_phase_and_resources_audited": True,
            "logical_whole_map_cases": 32,
            "logical_round_tie_cases": 8,
            "physical_forward_reverse_sweeps": [2, 2],
            "logical_forward_reverse_checks": [64, 16],
            "resource_gate_passed": costs["all_resource_gates_passed"],
            "component_candidate_eligible": eligible,
            "row_status": "COMPONENT_INDEPENDENTLY_AUDITED_PENDING_ROOT_INTEGRITY"
            if eligible
            else "REJECTED",
            "current_runtime": {**runtime, **package},
            "both_full_uncached_input_unions": [first, second],
            "limits_CPU_admission_wall": [300, 270, 900],
            **flags(),
        }
        save("summary.json", summary)
        save("completion_outcome.json", {**summary, "failed": False})
        owned, total = {}, 0
        for path in sorted(inventory(OUTPUT)):
            budget()
            total += path.stat().st_size
            require(
                len(owned) < MAX_OWN_FILES - 1 and total <= MAX_OWN_BYTES,
                "Complete manifest reserve",
            )
            owned[path.relative_to(OUTPUT).as_posix()] = digest(path, fresh=True)
        complete_manifest(
            {
                "schema": "a14-f44-stage-c-independent130-manifest-v1",
                "files": owned,
                "frozen_inputs": _FROZEN,
                "external_runtime_inputs": _EXTERNAL,
                "manifest_self_hash_excluded": True,
                "completed": True,
                "passed": True,
                "budget_censored": False,
                "producer_manifest_SHA256": PRIMARY_MANIFEST_SHA,
                "producer_complete_counts": PRIMARY_COUNTS,
                "row_status": summary["row_status"],
                "both_full_uncached_input_unions": [first, second],
                "integer_decimal_digit_limit": 20000,
                "integer_serialization_bit_cap": 65536,
                "limits_CPU_admission_wall": [300, 270, 900],
                "terminal_budget_observation": {
                    "process_CPU_seconds": time.process_time(),
                    "wall_seconds": time.monotonic() - _STARTED,
                },
                **flags(),
            },
            owned,
            total,
        )
        budget()
        print(
            json.dumps(
                {
                    "passed": True,
                    "row_status": summary["row_status"],
                    "manifest_SHA256": digest(OUTPUT / "manifest.json", fresh=True),
                    **flags(),
                }
            ),
            flush=True,
        )
    except BaseException as error:
        retain_failure(error)
        raise


"""AUTHOR ONLY, UNEXECUTED independent saved-gate consumer fragment.

Embed definitions as text into a separately reviewed auditor. The enclosing
module must provide require(condition, message) and budget(). This fragment
imports and calls no producer or builder. Universal functional composition is
conditional on independently admitted BK72 ADD/SUB and K MUL/ROUND clean maps
and independent all64 caller-range premises. No financial/G2/adoption credit.
"""

C130_CCX_MACRO = (
    ("H", 2),
    ("CX", 1, 2),
    ("TD", 2),
    ("CX", 0, 2),
    ("T", 2),
    ("CX", 1, 2),
    ("TD", 2),
    ("CX", 0, 2),
    ("T", 1),
    ("T", 2),
    ("H", 2),
    ("CX", 0, 1),
    ("T", 0),
    ("TD", 1),
    ("CX", 0, 1),
)


class C130SavedRows:
    """An actual-row proof cursor, never an emitter or a circuit builder."""

    def __init__(self, words, qubits, start=0, finish=None):
        budget()
        require(type(qubits) is int and 0 < qubits <= 16384, "Bounded actual allocated wires")
        require(
            len(words) % 4 == 0 and 0 < len(words) // 4 <= 2000000,
            "Complete bounded native Nx4 payload",
        )
        self.words, self.qubits, self.cursor = words, qubits, start
        self.finish = len(words) // 4 if finish is None else finish
        require(0 <= start <= self.finish <= len(words) // 4, "Actual-row cursor interval")

    def consume(self, wires):
        if self.cursor % 128 == 0:
            budget()
        require(
            1 <= len(wires) <= 3
            and len(set(wires)) == len(wires)
            and all(type(w) is int and 0 <= w < self.qubits for w in wires),
            "Canonical consumed native operands",
        )
        require(self.cursor < self.finish, "No implicit row, truncation or overrun")
        at = 4 * self.cursor
        require(
            self.words[at] == len(wires)
            and all(self.words[at + 1 + j] == wires[j] for j in range(len(wires)))
            and all(self.words[at + 1 + j] == 0 for j in range(len(wires), 3)),
            "Actual saved row satisfies independent local proof step",
        )
        self.cursor += 1

    def inverse_of(self, begin, end):
        require(0 <= begin <= end <= self.cursor, "Inverse refers only to consumed original rows")
        for index in range(end - 1, begin - 1, -1):
            at = 4 * index
            kind = self.words[at]
            require(kind in (1, 2, 3), "Canonical original inverse opcode")
            self.consume(tuple(self.words[at + 1 + j] for j in range(kind)))


def c130_full_bank(bank):
    require(
        type(bank) is list
        and len(bank) == 72
        and all(type(wire) is int for wire in bank)
        and bank == list(range(bank[0], bank[0] + 72)),
        "Canonical contiguous full72 bank",
    )
    return tuple(bank)


def c130_leaf_size(descriptor):
    result = descriptor["qubits"] if "qubits" in descriptor else descriptor["resources"]["qubits"]
    require(type(result) is int and 0 < result <= 16384, "Finite admitted native leaf capacity")
    return result


def c130_helper_body(cursor, operation, arguments, outputs, scratch, parameters):
    """Independent row obligations plus Boolean identities for each actual helper.

    Borrow identity: b_next=(~a & b) XOR (equal(a,b) & b_prev);
    terms are disjoint. Signed order follows by biasing both sign bits.
    SELECT=no XOR (flag AND (yes XOR no)). EQ is an AND of 72
    complemented differences. QROM implements all64 six-bit minterms;
    caller proof separately supplies zero high66 address bits.
    """
    if operation == "CONST":
        require(
            not arguments and len(outputs) == 1 and set(parameters) == {"raw"},
            "Fixed constant helper interface",
        )
        value = parameters["raw"]
        require(type(value) is int and -(1 << 71) <= value < (1 << 71), "Signed72 exact constant")
        for bit in range(72):
            if (value >> bit) & 1:
                cursor.consume((outputs[0][bit],))
    elif operation == "SHIFT4":
        require(len(arguments) == len(outputs) == 1 and not parameters, "Fixed left-shift helper")
        for source_bit in range(68):
            cursor.consume((arguments[0][source_bit], outputs[0][source_bit + 4]))
    elif operation == "ADDRESS34":
        require(len(arguments) == len(outputs) == 1 and not parameters, "Fixed right-shift helper")
        for output_bit in range(38):
            cursor.consume((arguments[0][output_bit + 34], outputs[0][output_bit]))
    elif operation == "SIGN":
        require(len(arguments) == len(outputs) == 1 and not parameters, "One signed flag")
        cursor.consume((arguments[0][71], outputs[0][0]))
    elif operation == "NOT":
        require(len(arguments) == len(outputs) == 1 and not parameters, "One Boolean complement")
        cursor.consume((outputs[0][0],))
        cursor.consume((arguments[0][0], outputs[0][0]))
    elif operation == "AND":
        require(
            len(arguments) == 2 and len(outputs) == 1 and not parameters, "One Boolean conjunction"
        )
        cursor.consume((arguments[0][0], arguments[1][0], outputs[0][0]))
    elif operation == "SELECT":
        require(
            len(arguments) == 3 and len(outputs) == 1 and not parameters and len(scratch) >= 72,
            "Full72 Boolean-controlled selection",
        )
        flag, yes, no = arguments
        for bit, delta in enumerate(scratch[:72]):
            cursor.consume((no[bit], outputs[0][bit]))
            cursor.consume((yes[bit], delta))
            cursor.consume((no[bit], delta))
            cursor.consume((flag[0], delta, outputs[0][bit]))
    elif operation == "EQ":
        require(
            len(arguments) == 2 and len(outputs) == 1 and not parameters and len(scratch) >= 143,
            "All72 equality operands and full prefix history",
        )
        a, b = arguments
        equality_bits, prefixes = scratch[:72], scratch[72:143]
        for bit, history in enumerate(equality_bits):
            cursor.consume((a[bit], history))
            cursor.consume((b[bit], history))
            cursor.consume((history,))
        cursor.consume((equality_bits[0], equality_bits[1], prefixes[0]))
        for bit in range(2, 72):
            cursor.consume((prefixes[bit - 2], equality_bits[bit], prefixes[bit - 1]))
        cursor.consume((prefixes[-1], outputs[0][0]))
    elif operation == "SIGNED_LT":
        require(
            len(arguments) == 2 and len(outputs) == 1 and not parameters and len(scratch) >= 217,
            "Complete signed72 subtraction-borrow comparison",
        )
        a, b = arguments
        equal_bits, complements, borrows = scratch[:72], scratch[72:144], scratch[144:217]
        cursor.consume((a[71],))
        cursor.consume((b[71],))
        for bit in range(72):
            cursor.consume((equal_bits[bit],))
            cursor.consume((a[bit], equal_bits[bit]))
            cursor.consume((b[bit], equal_bits[bit]))
            cursor.consume((complements[bit],))
            cursor.consume((a[bit], complements[bit]))
            cursor.consume((complements[bit], b[bit], borrows[bit + 1]))
            cursor.consume((equal_bits[bit], borrows[bit], borrows[bit + 1]))
        cursor.consume((borrows[72], outputs[0][0]))
        cursor.consume((a[71],))
        cursor.consume((b[71],))
    elif operation == "QROM64x8":
        require(
            len(arguments) == 1
            and len(outputs) == 8
            and set(parameters) == {"table"}
            and len(scratch) >= 5,
            "All64 eight-output signed72 QROM interface",
        )
        table, address = parameters["table"], arguments[0]
        require(
            type(table) is list
            and len(table) == 64
            and all(type(row) is list and len(row) == 8 for row in table),
            "Complete512 lookup literals",
        )
        for code in range(64):
            budget()
            inverted = tuple(bit for bit in range(6) if not ((code >> bit) & 1))
            for bit in inverted:
                cursor.consume((address[bit],))
            cursor.consume((address[0], address[1], scratch[0]))
            for bit in range(2, 6):
                cursor.consume((scratch[bit - 2], address[bit], scratch[bit - 1]))
            for column in range(8):
                value = table[code][column]
                require(
                    type(value) is int and -(1 << 71) <= value < (1 << 71),
                    "Every actual signed72 QROM literal",
                )
                for bit in range(72):
                    if (value >> bit) & 1:
                        cursor.consume((scratch[4], outputs[column][bit]))
            for bit in range(5, 1, -1):
                cursor.consume((scratch[bit - 2], address[bit], scratch[bit - 1]))
            cursor.consume((address[0], address[1], scratch[0]))
            for bit in reversed(inverted):
                cursor.consume((address[bit],))
    else:
        require(False, "Unrecognized native helper; no generic fallback")


def c130_expected_roles():
    """Algebra of the specified total integer function; no wire allocation."""
    raw, zero, one, minus = ("input",), ("const", 0), ("const", 1 << 40), ("const", -(1 << 40))
    clamp = ("select", ("negative", raw), zero, ("select", ("lt", raw, one), raw, one))
    eager = ("select", ("eq", clamp, one), zero, clamp)
    address = ("shr34", eager)
    rescaled, center = ("shl4", eager), ("table", address, 0)
    coefficients = [("table", address, column) for column in range(1, 8)]
    local = ("sub", rescaled, center)
    value = ("table", address, 7)
    horner = []
    for degree in range(5, -1, -1):
        product = ("mul44", value, local)
        following = ("add", product, coefficients[degree])
        horner.append(
            {
                "degree": degree,
                "accumulator": value,
                "local": local,
                "product": product,
                "coefficient": coefficients[degree],
                "sum": following,
            }
        )
        value = following
    rounded = ("round4", value)
    low = ("select", ("lt", rounded, minus), minus, rounded)
    projected = ("select", ("lt", one, low), one, low)
    value, axes = projected, []
    for point, exact in (
        (0, one),
        (1 << 38, zero),
        (1 << 39, minus),
        (3 << 38, zero),
        (1 << 40, one),
    ):
        flag = ("eq", clamp, ("const", point))
        following = ("select", flag, exact, value)
        axes.append(
            {
                "turn": point,
                "point": ("const", point),
                "flag": flag,
                "before": value,
                "after": following,
            }
        )
        value = following
    return {
        "clamped": clamp,
        "eager_Q_to_zero": eager,
        "address": address,
        "rescaled": rescaled,
        "center": center,
        "coefficients": coefficients,
        "local": local,
        "Horner": horner,
        "round_input": horner[-1]["sum"],
        "rounded": rounded,
        "projected": projected,
        "axes": axes,
        "final": value,
    }


def c130_expected_expression():
    return c130_expected_roles()["final"]


def c130_bind_internal_roles(internal, expressions):
    expected = c130_expected_roles()
    require(
        set(internal) == set(expected), "All named descriptor roles have exact independent meanings"
    )

    def meaning(bank):
        key = c130_full_bank(bank)
        require(
            key in expressions, "Internal role points only to an actual consumed full72 SSA bank"
        )
        return expressions[key]

    for name in expected:
        budget()
        if name == "coefficients":
            require(
                type(internal[name]) is list
                and len(internal[name]) == 7
                and [meaning(bank) for bank in internal[name]] == expected[name],
                "Every seven actual coefficient bank has its correct QROM column",
            )
        elif name in ("Horner", "axes"):
            require(
                type(internal[name]) is list and len(internal[name]) == len(expected[name]),
                "Complete fixed Horner and axis stage metadata",
            )
            literal = "degree" if name == "Horner" else "turn"
            for actual, target in zip(internal[name], expected[name], strict=True):
                require(
                    set(actual) == set(target)
                    and type(actual[literal]) is int
                    and actual[literal] == target[literal],
                    "Exact frozen stage index",
                )
                require(
                    all(meaning(actual[key]) == target[key] for key in target if key != literal),
                    "Every actual internal stage pointer has its independently specified algebra",
                )
        else:
            require(
                meaning(internal[name]) == expected[name],
                "Exact named actual internal bank semantics",
            )


def c130_expression(operation, args, parameters, outputs):
    if operation == "CONST":
        return [("const", parameters["raw"])]
    tags = {
        "SIGN": "negative",
        "SIGNED_LT": "lt",
        "SELECT": "select",
        "EQ": "eq",
        "SHIFT4": "shl4",
        "ADDRESS34": "shr34",
        "SUB": "sub",
        "ADD": "add",
        "MUL": "mul44",
        "ROUND": "round4",
        "NOT": "not",
        "AND": "and",
    }
    if operation == "QROM64x8":
        require(outputs == 8, "Complete eight-output table expression")
        return [("table", args[0], column) for column in range(8)]
    require(operation in tags and outputs == 1, "Recognized single-result semantic expression")
    return [(tags[operation], *args)]


def c130_gate_binding(words, descriptor, table, leaves):
    budget()
    require(
        set(leaves) == {"ADD", "SUB", "MUL", "ROUND"},
        "Exactly four externally admitted clean leaves",
    )
    require(
        type(table) is list
        and len(table) == 64
        and all(
            type(row) is list
            and len(row) == 8
            and all(type(value) is int and -(1 << 71) <= value < (1 << 71) for value in row)
            and row[0] == (2 * index + 1) * (1 << 37)
            for index, row in enumerate(table)
        ),
        "All512 exact signed72 table literals and all64 independent F44 centers",
    )
    require(
        descriptor["schema"] == "a14-f44-stage-c-clean-cosine-prototype-v1"
        and descriptor["row_id"] == "TAYLOR_D6_S64_W72_F44_TO_F40_MUL52x38",
        "One fixed saved clean cosine descriptor",
    )
    rows, wires = len(words) // 4, descriptor["qubits"]
    require(
        descriptor["gate_rows"] == rows
        and descriptor["args"] == [list(range(72))]
        and descriptor["outs"] == [list(range(72, 144))],
        "Actual full72 raw/dirty-output ports",
    )
    workspace = descriptor["shared_private_workspace"]
    capacity = max(c130_leaf_size(leaf["descriptor"]) for leaf in leaves.values())
    require(
        workspace == list(range(144, 144 + capacity))
        and capacity >= 653
        and descriptor["full72_private_leaf_capacity"] == capacity,
        "One exact full reusable private bank",
    )
    next_wire, position = 144 + capacity, 0
    expressions = {tuple(range(72)): ("input",)}
    forward_end = descriptor["forward_rows"][1]
    require(descriptor["forward_rows"] == [0, forward_end], "Forward begins at actual row0")
    cursor = C130SavedRows(words, wires, finish=forward_end)
    for event in descriptor["trace"]:
        budget()
        operation, arguments, outputs = event["op"], event["args"], event["outs"]
        require(
            event["rows"][0] == position == cursor.cursor
            and event["full_private_bank_reused"] is True,
            "Every forward row belongs to one exact contiguous event",
        )
        argument_keys = [c130_full_bank(bank) for bank in arguments]
        require(
            all(bank in expressions for bank in argument_keys),
            "Every argument is prior input/SSA, never dirty output",
        )
        for output in outputs:
            c130_full_bank(output)
            require(
                output == list(range(next_wire, next_wire + 72)),
                "Each result is a fresh monotone full72 SSA bank",
            )
            next_wire += 72
        arity, out_count = len(arguments), len(outputs)
        require(
            72 * (arity + out_count) <= capacity and event["inner_argument_copy_CX"] == 144 * arity,
            "Full copied arguments and private outputs fit the common bank",
        )
        for index, argument in enumerate(arguments):
            for bit in range(72):
                cursor.consume((argument[bit], workspace[72 * index + bit]))
        parameters = event.get("params", {})
        if operation in leaves:
            leaf, body_begin = leaves[operation], cursor.cursor
            leaf_descriptor, leaf_words = leaf["descriptor"], leaf["words"]
            size = c130_leaf_size(leaf_descriptor)
            require(
                arity == (1 if operation == "ROUND" else 2)
                and out_count == 1
                and leaf_descriptor["args"]
                == [list(range(72 * j, 72 * (j + 1))) for j in range(arity)]
                and leaf_descriptor["outs"] == [list(range(72 * arity, 72 * (arity + 1)))],
                "Every complete native clean-leaf full72 ABI",
            )
            require(
                event["leaf_gate_SHA256"] == leaf["gate_SHA256"] and len(leaf_words) % 4 == 0,
                "Leaf occurrence binds the independently admitted exact raw body",
            )
            remap = list(workspace[:size])
            remap[72 * arity : 72 * (arity + 1)] = outputs[0]
            require(
                len(set(remap)) == size, "Native remap is injective, including fresh output bank"
            )
            for index in range(len(leaf_words) // 4):
                if index % 128 == 0:
                    budget()
                at, opcode = 4 * index, leaf_words[4 * index]
                require(
                    opcode in (1, 2, 3)
                    and all(leaf_words[at + 1 + j] == 0 for j in range(opcode, 3)),
                    "Complete canonical admitted primitive body",
                )
                operands = tuple(leaf_words[at + 1 + j] for j in range(opcode))
                require(
                    len(set(operands)) == opcode and all(0 <= wire < size for wire in operands),
                    "Every native operand is valid before remapping",
                )
                cursor.consume(tuple(remap[wire] for wire in operands))
            require(
                event["actual_leaf_rows"] == [body_begin, cursor.cursor],
                "Complete remapped saved primitive interval",
            )
        else:
            body_begin = cursor.cursor
            private_arguments = [workspace[72 * j : 72 * (j + 1)] for j in range(arity)]
            private_outputs = [
                workspace[72 * (arity + j) : 72 * (arity + j + 1)] for j in range(out_count)
            ]
            if operation == "QROM64x8":
                require(
                    parameters == {"table": table},
                    "Every QROM literal equals the externally admitted complete table",
                )
            c130_helper_body(
                cursor,
                operation,
                private_arguments,
                private_outputs,
                workspace[72 * (arity + out_count) :],
                parameters,
            )
            body_end = cursor.cursor
            require(
                event["compute_rows"] == [body_begin, body_end], "Complete consumed helper body"
            )
            for source, target in zip(private_outputs, outputs, strict=True):
                for bit in range(72):
                    cursor.consume((source[bit], target[bit]))
            copy_end = cursor.cursor
            require(event["copy_rows"] == [body_end, copy_end], "Every actual full72 result copy")
            cursor.inverse_of(body_begin, body_end)
            require(
                event["inverse_rows"] == [copy_end, cursor.cursor],
                "Literal complete helper uncomputation",
            )
        for index, argument in enumerate(arguments):
            for bit in range(72):
                cursor.consume((argument[bit], workspace[72 * index + bit]))
        position = cursor.cursor
        require(event["rows"][1] == position, "No unconsumed helper/leaf row")
        meanings = c130_expression(
            operation, [expressions[bank] for bank in argument_keys], parameters, out_count
        )
        for output, meaning in zip(outputs, meanings, strict=True):
            expressions[tuple(output)] = meaning
    require(
        position == forward_end
        and next_wire == wires
        and descriptor["SSA_full72_banks"] == len(expressions) + 1,
        "Every allocated SSA/private wire and complete forward row consumed",
    )
    c130_bind_internal_roles(descriptor["internal"], expressions)
    middle_end = forward_end + 72
    require(
        descriptor["output_XOR_rows"] == [forward_end, middle_end]
        and descriptor["literal_global_inverse_rows"] == [middle_end, rows]
        and rows == middle_end + forward_end,
        "Whole clean F/72XOR/F^-1 shape",
    )
    cursor.finish = rows
    result_bank = []
    for bit in range(72):
        offset = 4 * cursor.cursor
        source = words[offset + 1]
        cursor.consume((source, 72 + bit))
        result_bank.append(source)
    require(
        tuple(result_bank) in expressions
        and expressions[tuple(result_bank)] == c130_expected_expression(),
        "Actual descriptor-driven SSA expression is the independently specified "
        "total integer function",
    )
    cursor.inverse_of(0, forward_end)
    require(
        cursor.cursor == rows
        and descriptor["input_preserved"] is True
        and descriptor["dirty_output_XOR"] is True
        and descriptor["private_and_SSA_zero_entry_exit"] is True
        and descriptor["input_full72_signed_clamp_0_to_Q"] is True
        and descriptor["outer_caller_copies_excluded"] is True
        and descriptor["prototype_native_rows_cap"] == 2000000
        and descriptor["prototype_native_wire_cap"] == 16384
        and descriptor["replay_guard_rows"] == 128
        and descriptor["full_financial_or_G2_certificate"] is False
        and descriptor["new_test_credit"] == 0,
        "Whole72 dirty-XOR clean composition and component-only scope",
    )
    budget()
    return {
        "all_actual_rows_consumed": rows,
        "all_actual_allocations_consumed": wires,
        "descriptor_driven_SSA_function_checked": True,
        "actual_global_inverse_checked_row_for_row": True,
        "all_internal_role_pointers_semantically_bound": True,
        "builder_or_MatchingCircuit_called": False,
        "second_array_generated": False,
        "universal_full72_clean_XOR_conditional": True,
        "required_external_premises": [
            "Independent BK72 ADD/SUB full72 clean-map certificates",
            "Independent K signed52x38 MUL and full72 ROUND certificates",
            "Independent all64 eager caller signed/no-wrap/address/low-bit proofs",
        ],
        "program_fixture_credit": 0,
        "financial_G2_or_adoption": False,
    }


def c130_integer_reference(raw, table):
    """Separate integer specification, including negative floor/tie behavior."""
    require(type(raw) is int and 0 <= raw < (1 << 72), "Unsigned full72 reference word")
    value = raw - (1 << 72) if raw & (1 << 71) else raw
    coordinate = max(0, min(1 << 40, value))
    exact_axes = {0: 1 << 40, 1 << 38: 0, 1 << 39: -(1 << 40), 3 << 38: 0, 1 << 40: 1 << 40}
    if coordinate in exact_axes:
        return exact_axes[coordinate] % (1 << 72)
    row = table[coordinate // (1 << 34)]
    delta = 16 * coordinate - row[0]
    result = row[7]
    for index in (6, 5, 4, 3, 2, 1):
        result = (result * delta) // (1 << 44) + row[index]
    quotient, remainder = divmod(result, 16)
    if remainder > 8 or (remainder == 8 and quotient % 2 == 1):
        quotient += 1
    return max(-(1 << 40), min(1 << 40, quotient)) % (1 << 72)


def c130_slice_initial(qubits, cases):
    require(
        type(qubits) is int and 144 <= qubits <= 16384 and len(cases) in (8, 32),
        "Fixed finite bit-slice lanes",
    )
    state = [0] * qubits
    for lane, (value, dirty) in enumerate(cases):
        budget()
        for bit in range(72):
            state[bit] |= ((value >> bit) & 1) << lane
            state[72 + bit] |= ((dirty >> bit) & 1) << lane
    return state


def c130_native_row(words, index, qubits):
    at = 4 * index
    opcode = words[at]
    require(
        type(opcode) is int and opcode in (1, 2, 3), "Actual native opcode is canonical integer"
    )
    operands = tuple(words[at + 1 + position] for position in range(opcode))
    require(
        len(set(operands)) == opcode
        and all(type(wire) is int and 0 <= wire < qubits for wire in operands)
        and all(words[at + 1 + position] == 0 for position in range(opcode, 3)),
        "All actual operands and padding are checked before every replay or schedule use",
    )
    return opcode, operands


def c130_bit_sweep(words, state, lane_count, inverse=False):
    budget()
    require(
        len(words) % 4 == 0
        and 0 < len(words) // 4 <= 2000000
        and 144 <= len(state) <= 16384
        and lane_count in (8, 32)
        and type(inverse) is bool,
        "Complete bounded bit-slice sweep",
    )
    full = (1 << lane_count) - 1
    for wire, value in enumerate(state):
        if wire % 128 == 0:
            budget()
        require(
            type(value) is int and 0 <= value <= full,
            "Every allocated wire contains exactly the admitted lane bits",
        )
    indices = range(len(words) // 4 - 1, -1, -1) if inverse else range(len(words) // 4)
    for step, index in enumerate(indices):
        if step % 128 == 0:
            budget()
        opcode, operands = c130_native_row(words, index, len(state))
        if opcode == 1:
            state[operands[0]] ^= full
        elif opcode == 2:
            state[operands[1]] ^= state[operands[0]]
        else:
            state[operands[2]] ^= state[operands[0]] & state[operands[1]]
    budget()


def c130_compare_slices(actual, initial, expected_outputs, lane_count):
    require(
        len(expected_outputs) == lane_count and len(actual) == len(initial),
        "Complete logical case-state dimensions",
    )
    for wire in range(len(actual)):
        if wire % 128 == 0:
            budget()
        expected = initial[wire]
        if 72 <= wire < 144:
            bit = wire - 72
            for lane, value in enumerate(expected_outputs):
                expected ^= ((value >> bit) & 1) << lane
        require(
            actual[wire] == expected,
            "Every logical case compares every allocated wire, including all zero history",
        )


def c130_fixed_diagnostics(words, descriptor, table, round_words, round_descriptor):
    budget()
    cap, mask = 1 << 40, (1 << 72) - 1
    inputs = (
        -(1 << 71),
        -1,
        0,
        1,
        (1 << 33) - 1,
        1 << 33,
        (1 << 34) - 1,
        1 << 34,
        (1 << 34) + 1,
        cap // 4,
        cap // 2,
        3 * cap // 4,
        cap - 1,
        cap,
        cap + 1,
        (1 << 71) - 1,
    )
    cases = [(value & mask, dirty) for value in inputs for dirty in (0, mask)]
    require(len(cases) == 32, "Exactly32 fixed full-map dirty-output lanes")
    initial = c130_slice_initial(descriptor["qubits"], cases)
    current = list(initial)
    expected = [c130_integer_reference(value, table) for value, _ in cases]
    c130_bit_sweep(words, current, 32)
    c130_compare_slices(current, initial, expected, 32)
    c130_bit_sweep(words, current, 32, inverse=True)
    require(
        current == initial, "All32 complete allocated states recover through actual reverse array"
    )
    ties = [(value & mask, dirty) for value in (-24, -8, 8, 24) for dirty in (0, mask)]
    size = c130_leaf_size(round_descriptor)
    require(
        round_descriptor["args"] == [list(range(72))]
        and round_descriptor["outs"] == [list(range(72, 144))],
        "Exact independent ROUND full72 ports",
    )
    initial_round = c130_slice_initial(size, ties)
    current_round = list(initial_round)
    expected_round = []
    for word, _ in ties:
        signed = word - (1 << 72) if word & (1 << 71) else word
        quotient, remainder = divmod(signed, 16)
        expected_round.append(
            (quotient + int(remainder > 8 or (remainder == 8 and quotient % 2))) & mask
        )
    c130_bit_sweep(round_words, current_round, 8)
    c130_compare_slices(current_round, initial_round, expected_round, 8)
    c130_bit_sweep(round_words, current_round, 8, inverse=True)
    require(
        current_round == initial_round, "All8 signed round ties recover complete original states"
    )
    budget()
    return {
        "full_map_case_count": 32,
        "standalone_round_tie_case_count": 8,
        "logical_whole_prototype_forward_calls": 32,
        "logical_whole_prototype_reverse_calls": 32,
        "logical_whole_prototype_total_replays": 64,
        "logical_standalone_round_total_replays": 16,
        "physical_prototype_sweeps": 2,
        "physical_ROUND_sweeps": 2,
        "bit_slice_lane_counts": [32, 8],
        "entire_allocated_state_forward_and_reverse_compared": True,
        "case_or_corpus_expansion": False,
        "producer_interpreter_or_scalar_reference_called": False,
        "program_fixture_credit": 0,
    }


def c130_schedule_interval(words, qubits, begin, end):
    budget()
    require(
        len(words) % 4 == 0
        and 0 < len(words) // 4 <= 2000000
        and type(qubits) is int
        and 0 < qubits <= 16384
        and type(begin) is int
        and type(end) is int
        and 0 <= begin <= end <= len(words) // 4,
        "Actual bounded schedule interval",
    )
    t_clock, full_clock, counts = [0] * qubits, [0] * qubits, [0, 0, 0]
    for index in range(begin, end):
        if (index - begin) % 128 == 0:
            budget()
        opcode, actual = c130_native_row(words, index, qubits)
        counts[opcode - 1] += 1
        expanded = (
            C130_CCX_MACRO if opcode == 3 else (("CX", 0, 1),) if opcode == 2 else (("X", 0),)
        )
        for event in expanded:
            affected = tuple(actual[position] for position in event[1:])
            next_t = max(t_clock[wire] for wire in affected) + (1 if event[0] in ("T", "TD") else 0)
            next_full = max(full_clock[wire] for wire in affected) + 1
            for wire in affected:
                t_clock[wire], full_clock[wire] = next_t, next_full
    budget()
    return {
        "rows": [begin, end],
        "source_gates": end - begin,
        "x": counts[0],
        "cx": counts[1],
        "ccx": counts[2],
        "t_count": 7 * counts[2],
        "t_depth": max(t_clock),
        "clifford_t_depth": max(full_clock),
    }


def c130_resources(words, descriptor):
    budget()
    rows, qubits = len(words) // 4, descriptor["qubits"]
    require(
        rows == descriptor["gate_rows"] and rows <= 2000000, "Complete actual saved resource source"
    )
    full = c130_schedule_interval(words, qubits, 0, rows)
    result = {key: value for key, value in full.items() if key != "rows"}
    result.update(
        qubits=qubits,
        clifford_cx=result["cx"] + 6 * result["ccx"],
        clifford_h=2 * result["ccx"],
        schedule="all-to-all ASAP full actual chronological exact7T expansion",
        entire_clean_prototype_not_leaf_sum_estimate=True,
        outer_caller_copies_excluded=True,
    )
    forward_end, reverse_begin = (
        descriptor["forward_rows"][1],
        descriptor["literal_global_inverse_rows"][0],
    )
    forward, inverse, position = [], [], 0
    for event in descriptor["trace"]:
        begin, end = event["rows"]
        require(
            begin == position and begin <= end <= forward_end,
            "Exact contiguous event serial chronology",
        )
        forward.append({"op": event["op"], **c130_schedule_interval(words, qubits, begin, end)})
        position = end
    require(position == forward_end, "Every forward row belongs to one actual serial event")
    output = c130_schedule_interval(words, qubits, forward_end, reverse_begin)
    require(
        output["source_gates"] == output["cx"] == 72 and output["x"] == output["ccx"] == 0,
        "All72 actual dirty-output copy rows paid",
    )
    for event in reversed(descriptor["trace"]):
        begin, end = event["rows"]
        actual_begin, actual_end = (
            reverse_begin + forward_end - end,
            reverse_begin + forward_end - begin,
        )
        inverse.append(
            {"op": event["op"], **c130_schedule_interval(words, qubits, actual_begin, actual_end)}
        )
    all_events = forward + [output] + inverse
    sums = {
        key: sum(event[key] for event in all_events)
        for key in ("source_gates", "x", "cx", "ccx", "t_count", "t_depth", "clifford_t_depth")
    }
    require(
        all(sums[key] == result[key] for key in ("source_gates", "x", "cx", "ccx", "t_count")),
        "Both complete scheduling conventions consume exactly the same actual row inventory",
    )
    result["matched_serial_event_chronology"] = {
        "forward_actual_events": forward,
        "output_XOR_actual_event": output,
        "inverse_actual_events": inverse,
        "sums": sums,
        "schedule": "serialize complete helper/leaf events; exact actual7T ASAP within each event",
        "matched_serial_whole_source_comparison_only": True,
        "distinct_from_standalone_ASAP_depth": True,
        "outer_caller_argument_copies_excluded": True,
    }
    budget()
    return result


def c130_phase_shift(vector, exponent):
    result = [0, 0, 0, 0]
    for degree, coefficient in enumerate(vector):
        power = (degree + exponent) % 8
        result[power % 4] += coefficient if power < 4 else -coefficient
    return tuple(result)


def c130_phase_add(mapping, state, vector, sign=1):
    previous = mapping.get(state, (0, 0, 0, 0))
    mapping[state] = tuple(previous[index] + sign * vector[index] for index in range(4))


def c130_ccx_absolute_phase():
    """Exact Z[zeta8]/(zeta8^4+1) coefficients; two Hadamards divide by2.

    Eight input basis columns verify the full operator, including its absolute
    phase. These are proof cases, not the frozen native diagnostic corpus.
    """
    budget()
    require(len(C130_CCX_MACRO) == 15, "One fixed exact15-event macro")
    for basis in range(8):
        budget()
        amplitudes, hadamards = {basis: (1, 0, 0, 0)}, 0
        for event in C130_CCX_MACRO:
            name, operands = event[0], event[1:]
            updated = {}
            if name == "H":
                hadamards += 1
            for state, vector in amplitudes.items():
                if name == "CX":
                    out = state ^ (1 << operands[1]) if state & (1 << operands[0]) else state
                    c130_phase_add(updated, out, vector)
                elif name in ("T", "TD"):
                    shifted = (
                        c130_phase_shift(vector, 1 if name == "T" else -1)
                        if state & (1 << operands[0])
                        else vector
                    )
                    c130_phase_add(updated, state, shifted)
                else:
                    require(name == "H" and len(operands) == 1, "Exact macro event alphabet")
                    bit = operands[0]
                    zero = state & ~(1 << bit)
                    one = zero | (1 << bit)
                    c130_phase_add(updated, zero, vector)
                    c130_phase_add(updated, one, vector, -1 if state & (1 << bit) else 1)
            amplitudes = {state: vector for state, vector in updated.items() if any(vector)}
        expected = basis ^ 4 if basis & 1 and basis & 2 else basis
        require(
            hadamards == 2 and amplitudes == {expected: (2, 0, 0, 0)},
            "Actual15-event macro equals exact CCX with positive absolute unit amplitude",
        )
    budget()
    return {
        "exact_absolute_phase_CCX": True,
        "basis_columns": 8,
        "events": 15,
        "T_or_Tdg_count": 7,
        "CX_count": 6,
        "H_count": 2,
        "cyclotomic_integer_proof": "zeta8^4=-1; common two-H denominator2",
        "relative_or_unknown_global_phase_accepted": False,
        "program_fixture_credit": 0,
    }


if __name__ == "__main__":
    main()
