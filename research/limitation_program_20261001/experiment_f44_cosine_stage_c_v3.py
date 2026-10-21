"""Unexecuted one-row primary90 F44 cosine component; ROOT release required.

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
from datetime import datetime, timezone
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
from types import ModuleType

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
PROGRAM = ROOT / "results/limitation_program_20261001"
AUTHOR = RESEARCH / "experiment_f44_cosine_stage_c_v3.py"
BUILDER = RESEARCH / "f44_cosine_stage_c_source.py"
BUILDER_MODULE = "research.limitation_program_20261001.f44_cosine_stage_c_source"
METHOD_DOC = RESEARCH / "A14_F44_COSINE_STAGE_C_IMPLEMENTATION_PREFLIGHT_V3.md"
PREFLIGHT = RESEARCH / "a14_f44_cosine_stage_c_implementation_preflight_v3.json"
PROSPECTUS = RESEARCH / "a14_taylor_f44_prospectus_v1.json"
PROSPECTUS_DOC = RESEARCH / "A14_TAYLOR_F44_PROSPECTUS_V1.md"
PROSPECTUS_SHA = "526b082ca8d9ab1d1583de58e3fc0e6f5632583f6f663088ad42d6d389c713f3"
PROSPECTUS_DOC_SHA = "e4c1a4ad5c1bc23e266d9cbf4cfc5adeb1528fda8cfd89179696108be5302b04"
READY = ROOT / ".context/A14_F44_COSINE_STAGE_C_ROOT_READY_run003.json"
OUTPUT = PROGRAM / "A14_taylor_f44_stage_C_run003"
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
CPU, ADMISSION, WALL, DIGITS = 300, 270, 900, 90
ORACLE_BITS, ATAN_TERMS, COS_TERMS = 384, 160, 160
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


def encode(value):
    value = Fraction(value)
    return [value.numerator, value.denominator]


def rational(value):
    require(
        type(value) is list
        and len(value) == 2
        and all((type(item) is int for item in value))
        and (value[1] > 0),
        "Canonical rational pair",
    )
    result = Fraction(*value)
    require(encode(result) == value, "Reduced exact rational")
    return result


def interval_endpoint(value):
    sign, mantissa, exponent, bits = value
    require(
        sign in (0, 1)
        and type(mantissa) is int
        and (type(exponent) is int)
        and (type(bits) is int)
        and (mantissa >= 0)
        and (bits >= 0),
        "Finite outward binary endpoint",
    )
    return Fraction((-1 if sign else 1) * mantissa) * Fraction(2) ** exponent


def endpoints(value):
    result = tuple((interval_endpoint(item) for item in value._mpi_))
    require(len(result) == 2 and result[0] <= result[1], "Ordered outward enclosure")
    return result


def outward(mp, value):
    value = Fraction(value)
    return mp.iv.mpf(value.numerator) / mp.iv.mpf(value.denominator)


def nearest(value):
    value = Fraction(value)
    quotient, remainder = divmod(value.numerator, value.denominator)
    return quotient + int(
        2 * remainder > value.denominator or (2 * remainder == value.denominator and quotient % 2)
    )


class ActualGraph:
    """Read-only typed actual SSA matching; never builds or evaluates a Graph."""

    def __init__(self, target, started):
        self.started, self.target, self.nodes = (started, target, {})
        require(target["width"] == W and target["fraction_bits"] == 40, "Actual native W72/F40")
        arities = dict(
            input=0,
            const=0,
            bits=1,
            add=2,
            sub=2,
            mul=2,
            cmul=1,
            lt=2,
            select=3,
            msb=1,
            shift=2,
            positive=1,
            sqrt=1,
            lookup=1,
        )
        for node in target["nodes"]:
            legacy_tick(started)
            op, args, outputs, params = (node[key] for key in ("op", "args", "out", "params"))
            require(
                op in arities and type(args) is list and (len(args) == arities[op]),
                "Typed op/arity",
            )
            require(type(params) is dict and type(outputs) is list and outputs, "Typed node fields")
            require(
                all((type(value) is int and value in self.nodes for value in args)),
                "Topological inputs",
            )
            require(
                all(
                    (
                        type(value) is int and value >= 0 and (value not in self.nodes)
                        for value in outputs
                    )
                ),
                "Unique SSA IDs",
            )
            require(len(set(outputs)) == len(outputs), "Unique multioutput SSA IDs")
            if op != "lookup":
                require(len(outputs) == 1, "Single output operation")
            if op in ("input", "bits", "lookup"):
                require(type(params.get("bits", params.get("width"))) is int, "Integer width field")
            if op == "bits":
                require(
                    type(params.get("shift")) is int and type(params.get("signed")) is bool,
                    "Typed bit shift",
                )
            if op in ("const", "cmul"):
                raw = params["value" if op == "const" else "c"]
                require(
                    set(params) == {"value" if op == "const" else "c"},
                    "Exact native literal parameter keys",
                )
                require(type(raw) is int, "Native literals are JSON ints, never flags")
                require(
                    0 <= raw < 1 << 72 if op == "const" else -(1 << 71) <= raw < 1 << 71,
                    "Const unsigned72/cmul signed72 canonical representations",
                )
                literal(raw)
            if op not in ("input", "const", "cmul", "bits", "lookup"):
                require(params == {}, "Exact arithmetic parameters")
            for value in outputs:
                self.nodes[value] = node
        require(set(self.nodes) == set(range(len(self.nodes))), "Contiguous actual SSA inventory")

    def node(self, value, op=None, params=None):
        legacy_tick(self.started)
        require(type(value) is int and value in self.nodes, "Actual SSA value identity")
        node = self.nodes[value]
        require(op is None or node["op"] == op, "Expected actual operation: " + str(value))
        if params is not None:
            same(node["params"], params, "Exact actual operation parameters")
        return node

    def const(self, value, raw=None):
        actual = literal(self.node(value, "const")["params"]["value"])
        require(raw is None or actual == raw, "Exact constant literal")
        return actual

    def clip(self, value, low=None, high=None):
        flag, middle, hi = self.node(value, "select")["args"]
        require(self.node(flag, "lt")["args"] == [middle, hi], "Upper clamp structure")
        lo_flag, lo, raw = self.node(middle, "select")["args"]
        require(self.node(lo_flag, "lt")["args"] == [raw, lo], "Lower clamp structure")
        lower, upper = (self.const(lo, low), self.const(hi, high))
        require(lower < upper, "Ordered literal clamp")
        return raw

    def midpoint(self, value, input_id):
        args = self.node(value, "add")["args"]
        shifts = [arg for arg in args if self.node(arg)["op"] == "bits"]
        require(len(shifts) == 1, "Exact midpoint shift")
        shift = shifts[0]
        require(
            self.node(shift, "bits", dict(shift=-8, width=72, signed=False))["args"] == [input_id],
            "Midpoint raw input",
        )
        self.const(next((arg for arg in args if arg != shift)), 128)

    def ancestors(self, value):
        found, pending = (set(), [value])
        while pending:
            legacy_tick(self.started)
            current = pending.pop()
            if current not in found:
                found.add(current)
                pending.extend(self.node(current)["args"])
        return found

    def interpolation(self, value, name, argument):
        segments, degree, lo, index_bits = (32, 8, Q, 5) if name == "log" else (64, 7, 0, 6)
        candidates = {
            tuple(self.node(v)["out"])
            for v in self.ancestors(value)
            if self.node(v)["op"] == "lookup" and self.node(v)["params"]["table"] == name
        }
        require(len(candidates) == 1, "One actual interpolation lookup")
        outputs = next(iter(candidates))
        lookup = self.node(outputs[0], "lookup", dict(table=name, bits=index_bits))
        require(len(outputs) == degree + 1, "Complete actual Horner coefficient outputs")
        index = lookup["args"][0]
        address = self.node(
            index, "bits", dict(shift=40 - index_bits, width=index_bits, signed=False)
        )["args"][0]
        if lo:
            address, lower = self.node(address, "sub")["args"]
            self.const(lower, lo)
        bounded = address
        require(self.clip(bounded, lo, lo + Q - 1) == argument, "Actual interpolation domain")
        current, local = (value, None)
        for j in range(degree):
            args = self.node(current, "add")["args"]
            require(outputs[j] in args, "Actual Horner coefficient ordering")
            product = next((arg for arg in args if arg != outputs[j]))
            factors = self.node(product, "mul")["args"]
            if local is None:
                possible = [v for v in factors if self.node(v)["op"] == "sub"]
                require(len(possible) == 1, "Unique Horner local coordinate")
                local = possible[0]
            require(local in factors, "Every actual Horner multiplication uses local")
            current = next((arg for arg in factors if arg != local))
        require(current == outputs[-1], "Actual Horner degree8/7 terminal coefficient")
        actual_x, center = self.node(local, "sub")["args"]
        require(actual_x == bounded, "Actual local-coordinate input")
        args = self.node(center, "add")["args"]
        shifts = [v for v in args if self.node(v)["op"] == "bits"]
        require(len(shifts) == 1, "Actual segment center shift")
        shift = shifts[0]
        require(
            self.node(shift, "bits", dict(shift=index_bits - 40, width=72, signed=False))["args"]
            == [index],
            "Actual center address",
        )
        self.const(next((v for v in args if v != shift)), lo + Q // (2 * segments))
        return dict(
            output=value,
            input=argument,
            address=index,
            local=local,
            lookup_outputs=list(outputs),
            floors=degree,
        )

    def pair(self, roots, raw_u, raw_v, ln2):
        require(len(roots) == 2, "One original joint pair")
        factors = [self.node(value, "mul")["args"] for value in roots]
        common = set(factors[0]) & set(factors[1])
        require(len(common) == 1, "Exactly one shared actual radius")
        radius = next(iter(common))
        positive = self.node(radius, "sqrt")["args"][0]
        negative_two = self.node(positive, "positive")["args"][0]
        log_value = self.node(negative_two, "cmul", dict(c=-2 * Q))["args"][0]
        log_args = self.node(log_value, "add")["args"]
        terms = [v for v in log_args if self.node(v)["op"] == "cmul"]
        require(len(terms) == 1, "Unique exponent-ln2 product")
        term = terms[0]
        scaled = self.node(term, "cmul", dict(c=ln2))["args"][0]
        exponent = self.node(scaled, "bits", dict(shift=-40, width=72, signed=False))["args"][0]
        top, fraction = self.node(exponent, "sub")["args"]
        self.const(fraction, 40)
        safe = self.node(top, "msb")["args"][0]
        flag, tiny, mid_u = self.node(safe, "select")["args"]
        self.const(tiny, 1)
        require(self.node(flag, "lt")["args"] == [mid_u, tiny], "Actual safe positive log input")
        self.midpoint(mid_u, raw_u)
        poly = next((v for v in log_args if v != term))
        lookups = [self.node(v) for v in self.ancestors(poly) if self.node(v)["op"] == "lookup"]
        require(len({tuple(node["out"]) for node in lookups}) == 1, "Unique log lookup")
        index = lookups[0]["args"][0]
        address = self.node(index)["args"][0]
        clipped = self.node(address, "sub")["args"][0]
        mantissa = self.clip(clipped, Q, 2 * Q - 1)
        u, negated = self.node(mantissa, "shift")["args"]
        require(u == safe, "Actual mantissa normalized from safe midpoint")
        zero, actual_exponent = self.node(negated, "sub")["args"]
        self.const(zero, 0)
        require(actual_exponent == exponent, "Actual left-shift exponent")
        log_scope = self.interpolation(poly, "log", mantissa)
        cosines = [next((v for v in row if v != radius)) for row in factors]
        arguments = []
        for cosine in cosines:
            lookup = [
                self.node(v) for v in self.ancestors(cosine) if self.node(v)["op"] == "lookup"
            ]
            require(len({tuple(node["out"]) for node in lookup}) == 1, "Unique cosine lookup")
            clip = self.node(lookup[0]["args"][0])["args"][0]
            arguments.append(self.clip(clip, 0, Q - 1))
        mid_v, quarter = arguments
        self.midpoint(mid_v, raw_v)
        wrapped = self.node(quarter, "bits", dict(shift=0, width=40, signed=False))["args"][0]
        args = self.node(wrapped, "add")["args"]
        require(mid_v in args, "Positive sine convention uses same midpoint")
        self.const(next((v for v in args if v != mid_v)), 3 * Q // 4)
        scopes = [self.interpolation(v, "cos", a) for v, a in zip(cosines, arguments, strict=True)]
        inputs = {
            v for root in roots for v in self.ancestors(root) if self.node(v)["op"] == "input"
        }
        require(inputs == {raw_u, raw_v}, "Original pair input closure")
        return dict(
            normal_values=list(roots),
            raw_uniform_values=[raw_u, raw_v],
            radius=radius,
            log=log_scope,
            cosines=scopes,
            original_shared_pair_preserved=True,
        )

    def flatten(self, value, stops, op="add"):
        result, pending = (Counter(), [value])
        while pending:
            legacy_tick(self.started)
            current = pending.pop()
            if current in stops:
                result[current] += 1
            else:
                pending.extend(self.node(current, op)["args"])
        return result

    def maxima(self, value, stops):
        result, pending = (Counter(), [value])
        while pending:
            current = pending.pop()
            if current in stops:
                result[current] += 1
                continue
            flag, hi, lo = self.node(current, "select")["args"]
            require(self.node(flag, "lt")["args"] == [lo, hi], "Exact basket maximum tree")
            pending.extend((lo, hi))
        return result


def literal(value):
    require(type(value) is int and -(1 << 71) <= value < 1 << W, "Canonical source literal")
    return value - (1 << W) if value >= 1 << 71 else value


def one_primitive_profile(record, case, source, frozen, external, started):
    profiles = {}
    paths = record["primitive_descriptor_paths"][case]
    require(
        paths and set(paths) <= {"ADD", "SUB", "MUL"}, "Only measured full72 arithmetic profiles"
    )
    for op, key in paths.items():
        legacy_tick(started)
        path = legacy_resolved(ROOT / key, started)
        require(
            legacy_relative(path, started) in frozen, "Measured profile frozen before source work"
        )
        data = legacy_read(path, started)
        if op in ("ADD", "SUB"):
            require(type(data) is list, "A08 actual fullwidth screen")
            candidates = [
                row
                for row in data
                if row["op"] == op.lower()
                and row["width"] == W
                and (row["variant"] == "brent-kung")
            ]
            require(len(candidates) == 1, "ONE fixed measured BK72 profile")
            descriptor = candidates[0]
            spec = descriptor["spec"]
            require(
                spec["lowering"] == "clean-xor-prefix-add-sub-v1"
                and spec["variant"] == "brent-kung",
                "Exact raw modular full72 adder family",
            )
            gate_path = legacy_resolved(
                path.parent / descriptor["gate_file"].replace("\\", "/"), started
            )
            builder_path = path.parent / "executed_code/carry_lookahead.py"
            require(
                legacy_relative(builder_path, started) in frozen,
                "Exact measured raw builder source frozen",
            )
            builder_module = ast.parse(legacy_read_bytes(builder_path, started).decode("utf-8"))
            builder_defs = {
                node.name: node for node in builder_module.body if isinstance(node, ast.FunctionDef)
            }
            require(
                {"build_carry_lookahead", "prefix_pairs", "_compose"} <= set(builder_defs),
                "Complete actual raw prefix builder source",
            )
            same(
                [arg.arg for arg in builder_defs["build_carry_lookahead"].args.args],
                ["op", "width", "variant"],
                "Raw builder accepts no fraction or scale input",
            )
            for name in ("build_carry_lookahead", "prefix_pairs", "_compose"):
                for item in ast.walk(builder_defs[name]):
                    legacy_tick(started)
                    require(
                        not isinstance(item, ast.Name)
                        or not any((token in item.id.lower() for token in ("fraction", "scale"))),
                        "Raw bit-map construction independent of fractional label",
                    )
        else:
            descriptor = data
            spec = descriptor["spec"]
            require(
                spec["fraction_bits"] == F and spec["product_width"] == W + F,
                "Actual generic full72 f40 signed144-to112 multiplier",
            )
            gate_path = path.with_suffix(".npy")
        require(
            spec["op"] == op.lower() and spec["width"] == W and (spec["params"] == {}),
            "Explicit actual operation/fullwidth emptyparams",
        )
        require(
            not spec.get("input_contract")
            and (not descriptor.get("input_contract"))
            and (not spec.get("active_operand_bits"))
            and (not descriptor.get("active_operand_bits")),
            "No narrow unit borrowed",
        )
        same(descriptor["args"], [list(range(W)), list(range(W, 2 * W))], "Full72 argument ABI")
        same(descriptor["outs"], [list(range(2 * W, 3 * W))], "Full72 dirty-XOR output ABI")
        gate_key = legacy_relative(gate_path, started)
        require(gate_key in frozen, "Actual measured gates originally owned and frozen")
        resources = descriptor["resources"]
        require(
            all(
                (
                    type(resources[field]) is int and resources[field] >= 0
                    for field in RESOURCE_FIELDS
                )
            ),
            "Typed measured resource fields",
        )
        require(resources["t_count"] == 7 * resources["ccx"], "Actual paid exact7T profile")
        profiles[op] = dict(
            descriptor_path=legacy_relative(path, started),
            descriptor_sha256=frozen[legacy_relative(path, started)],
            gate_path=gate_key,
            gate_sha256=frozen[gate_key],
            op=op.lower(),
            spec=spec,
            args=descriptor["args"],
            outs=descriptor["outs"],
            resources=resources,
            compiled_source_format=source["format"],
            word_width=W,
            fraction_bits=F,
            raw_modular_ADD_SUB_fraction_label_reuse_only=op in ("ADD", "SUB"),
        )
        if op in ("ADD", "SUB"):
            profiles[op]["raw_bit_map_fraction_label_independence"] = dict(
                builder_path=legacy_relative(builder_path, started),
                builder_sha256=frozen[legacy_relative(builder_path, started)],
                physical_call_arguments=[op.lower(), W, "brent-kung"],
                raw_map="(a+b) mod2^72" if op == "ADD" else "(a-b) mod2^72",
                fraction_label_is_metadata_only=True,
                independent_signed_range_proofs_still_required=True,
                new_gate_or_builder_execution=False,
            )
    return profiles


def primitive_profiles(record, case, source, frozen, external, started):
    declared = record["primitive_descriptor_paths"][case]
    require(set(declared) == {"ADD", "SUB", "MUL"}, "Exact measured primitive path scope")
    result = {}
    for op, key in declared.items():
        path = legacy_resolved(ROOT / key, started)
        require(
            legacy_relative(path, started) in frozen,
            "Profile path must have original bound membership",
        )
        single = dict(record, primitive_descriptor_paths={case: {op: key}})
        try:
            result.update(one_primitive_profile(single, case, source, frozen, external, started))
        except (ValueError, KeyError, TypeError) as error:
            result[op] = dict(
                resource_rejected=True,
                op=op.lower(),
                descriptor_path=key,
                descriptor_sha256=frozen[legacy_relative(path, started)],
                reason=str(error),
                error_type=type(error).__name__,
                no_cost_or_contract_claim=True,
            )
    return result


def phase_premise(started):
    proof = legacy_read(PHASE_PROOF, started)
    same(
        proof,
        [
            dict(input=k, output=k ^ (k & 1 & (k >> 1 & 1)) << 2, exact_nonzero_phase=1)
            for k in range(8)
        ],
        "Frozen exact phase-one3wire CCX proof",
    )
    source = ast.parse(legacy_read_bytes(PHASE_SOURCE, started).decode("utf-8"))
    found = [
        node
        for node in source.body
        if isinstance(node, ast.FunctionDef) and node.name == "ccx_seven_t"
    ]
    require(len(found) == 1, "One frozen CCX source")
    returns = [node for node in found[0].body if isinstance(node, ast.Return)]
    require(
        len(returns) == 1 and isinstance(returns[0].value, ast.List), "Literal paid CCX chronology"
    )
    rows = []
    for item in returns[0].value.elts:
        require(
            isinstance(item, ast.Call)
            and isinstance(item.func, ast.Name)
            and (item.func.id == "gate")
            and (not item.keywords)
            and isinstance(item.args[0], ast.Constant)
            and all((isinstance(arg, ast.Name) for arg in item.args[1:])),
            "Typed literal CCX row",
        )
        rows.append((item.args[0].value, *(arg.id for arg in item.args[1:])))
    same(rows, list(EXACT_CCX_MACRO), "Both control phases/literal macro chronology")
    return dict(
        exact_macro=[list(row) for row in rows],
        native_phase_one=True,
        direct_recipe_T_depth_per_CCX=7,
        direct_recipe_Clifford_T_serial_depth_per_CCX=15,
        fresh_gate_or_phase_simulation_executed=False,
    )


def removable_cosine_calls(graph, source, cosine_outputs, arguments, radius_products, started):
    stops = set().union(*(graph.ancestors(value) for value in arguments))
    candidates = set().union(*(graph.ancestors(value) for value in cosine_outputs)) - stops
    users = {value: set() for value in graph.nodes}
    for node in graph.target["nodes"]:
        legacy_tick(started)
        for value in node["args"]:
            users[value].update(node["out"])
    authorized = set(zip(cosine_outputs, radius_products, strict=True))
    proposed = set(candidates)
    changed = True
    while changed:
        changed = False
        for value in sorted(proposed):
            legacy_tick(started)
            node_outputs = set(graph.node(value)["out"])
            if any(
                (
                    user not in proposed and (output, user) not in authorized
                    for output in node_outputs
                    for user in users[output]
                )
            ):
                proposed.difference_update(node_outputs)
                changed = True
                break
    require(
        set(cosine_outputs) <= proposed,
        "Every cosine endpoint replaceable only at actual radius product",
    )
    calls = [call for call in source["forward_calls"] if set(call["out"]) <= proposed]
    require(
        {value for call in calls for value in call["out"]} == proposed,
        "Complete removable node/call inventory",
    )
    return dict(
        removed_value_ids=sorted(proposed),
        removed_forward_calls=calls,
        retained_shared_or_outside_value_ids=sorted(candidates - proposed),
        authorized_cosine_output_to_radius_product_edges=[
            list(edge) for edge in sorted(authorized)
        ],
        actual_user_fixed_point=True,
        original_storage_subtracted=False,
    )


def source_binding(record, frozen, external, started):
    legacy_tick(started, admission=True)
    certificate = legacy_read(PROGRAM / "C06_pair_run001/certificate.json", started)
    archived = legacy_read(PROGRAM / "C06_pair_audit_run001/actual_pair_scope_audit.json", started)
    cases, graphs = ({}, {})
    for case, (assets, dates, pairs) in CASES.items():
        legacy_tick(started)
        directory = PROGRAM / "A10_coefficient_run001" / case / "min-depth"
        target_path, source_path, schedule_path = (
            directory / name for name in ("target.json", "source.json", "schedule_capped.json")
        )
        for path in (target_path, source_path, schedule_path):
            require(
                legacy_relative(path, started) in frozen, "Actual source frozen before graph walk"
            )
        target, source, schedule = (
            legacy_read(path, started) for path in (target_path, source_path, schedule_path)
        )
        graph = ActualGraph(target, started)
        graphs[case] = graph
        require(
            source["format"] == "hierarchical-clean-xor-source-v1"
            and source["word_width"] == W
            and (source["fraction_bits"] == F),
            "Original full72/f40 hierarchical clean source",
        )
        inputs = [node for node in target["nodes"] if node["op"] == "input"]
        require(len(inputs) == 2 * pairs == dates * (assets + 1), "Actual pair/driver count")
        same(source["inputs"], inputs, "Full original input ABI")
        same(source["outputs"], target["outputs"], "Named dirty output ABI")
        for index, node in enumerate(inputs):
            same(
                node["params"],
                dict(name="uniform_" + str(index), bits=32, preparation="uniform"),
                "Actual joint q32 roles",
            )
        noninputs = [node for node in target["nodes"] if node["op"] != "input"]
        require(
            len(noninputs) == len(source["forward_calls"]), "Every eager original call retained"
        )
        calls = {}
        for node, call in zip(noninputs, source["forward_calls"], strict=True):
            legacy_tick(started)
            same(
                [node["args"], node["out"]], [call["args"], call["out"]], "Actual full call mapping"
            )
            require(
                call["argument_copy_cx"] == 2 * W * len(node["args"]),
                "Every full72 original argument copy paid",
            )
            for value in node["out"]:
                calls[value] = call
        original = certificate["source_bindings"][case]
        normals, ln2 = (original["normal_values"], original["literal_ln2"])
        require(len(normals) == 2 * pairs, "All original normals jointly retained")
        scopes, cosines, arguments, radius_products = ([], [], [], [])
        for pair in range(pairs):
            legacy_tick(started)
            roots = normals[2 * pair : 2 * pair + 2]
            scope = graph.pair(
                roots, inputs[2 * pair]["out"][0], inputs[2 * pair + 1]["out"][0], ln2
            )
            scopes.append(scope)
            cosines.extend((row["output"] for row in scope["cosines"]))
            arguments.extend((row["input"] for row in scope["cosines"]))
            radius_products.extend(roots)
        same(
            scopes,
            archived[case]["independently_walked_pair_scopes"],
            "Exact archived independently verified pair scopes",
        )
        require(len(cosines) == CASE_SITES[case], "Both cosine/sine calls in each joint pair")
        require(
            source["resources"]["t_count"] == BASELINE[case][0],
            "Actual original whole-source T count",
        )
        require(
            schedule["resources"]["t_count"] == BASELINE[case][0]
            and schedule["resources"]["t_depth"] == BASELINE[case][1]
            and (schedule["resources"]["logical_qubits"] == BASELINE[case][2]),
            "Exact measured original capped schedule context/caps",
        )
        cases[case] = dict(
            assets=assets,
            dates=dates,
            joint_pairs=pairs,
            cosine_sites=len(cosines),
            target_path=legacy_relative(target_path, started),
            source_path=legacy_relative(source_path, started),
            schedule_path=legacy_relative(schedule_path, started),
            target_sha256=frozen[legacy_relative(target_path, started)],
            source_sha256=frozen[legacy_relative(source_path, started)],
            schedule_sha256=frozen[legacy_relative(schedule_path, started)],
            original_resources=source["resources"],
            original_measured_schedule=schedule,
            normal_values=normals,
            pair_scopes=scopes,
            cosine_output_values=cosines,
            cosine_argument_values=arguments,
            cosine_calls=[calls[value] for value in cosines],
            selected_primitive_profiles=primitive_profiles(
                record, case, source, frozen, external, started
            ),
            removal=removable_cosine_calls(
                graph, source, cosines, arguments, radius_products, started
            ),
            source_convention_exact=True,
            cross_date_pair_coordinates_not_divided=True,
        )
    old_path = BRIDGE / "cosine_envelope.json"
    old = legacy_read(old_path, started)
    error = rational(old["cosine_error_upper"])
    require(error >= EPS, "Freshly bound original seven propagated floors include final fullULP")
    same(
        graphs["B4x12"].target["tables"]["cos"],
        graphs["B8x52"].target["tables"]["cos"],
        "Actual source cosine tables agree",
    )
    table = graphs["B4x12"].target["tables"]["cos"]
    require(len(old["coefficient_checks"]) == 512, "All old512 coefficient checks retained")
    row_errors = [Fraction(0) for _ in range(64)]
    for index, check in enumerate(old["coefficient_checks"]):
        legacy_tick(started)
        row, degree = divmod(index, 8)
        require(
            check["row"] == row
            and check["degree"] == degree
            and (check["raw"] == table[row][degree]),
            "E_old exact original coefficient inventory",
        )
        lo, hi = (rational(value) for value in check["exact_coefficient_enclosure"])
        paid = rational(check["actual_literal_error_upper"])
        require(
            paid == max(abs(Fraction(check["raw"], Q) - lo), abs(Fraction(check["raw"], Q) - hi)),
            "Exact old actual-literal error arithmetic",
        )
        row_errors[row] += paid * H**degree
    floor_bound = EPS * sum((H**degree for degree in range(7)), Fraction(0))
    require(
        rational(old["literal_rounding_upper"]) == max(row_errors)
        and rational(old["Horner_floor_upper"]) == floor_bound
        and (
            error == max(row_errors) + floor_bound + rational(old["Taylor_degree7_remainder_upper"])
        ),
        "Original E_old complete source-specific formula, never a numerical guess",
    )
    radius = rational(old["pinned_native_radius_upper"])
    require(
        radius > 0 and rational(old["remaining_coordinate_error_upper"]) == radius * error + EPS,
        "Already-paid native radius and remaining cosine/product error ledger",
    )
    return (
        dict(
            schema="a14-original-cosine-source-binding-v1",
            cases=cases,
            existing_E_old=dict(
                path=legacy_relative(old_path, started),
                sha256=frozen[legacy_relative(old_path, started)],
                cosine_error_upper=encode(error),
                pinned_native_radius_upper=encode(radius),
                remaining_coordinate_error_upper=encode(radius * error + EPS),
                all512_actual_coefficient_words_and_error_formula_bound=True,
                source_manifest_sha256=record["existing_owner_manifest_SHA256"][
                    legacy_relative(BRIDGE / "manifest.json", started)
                ],
                audit_manifest_sha256=record["existing_owner_manifest_SHA256"][
                    legacy_relative(BRIDGE_AUDIT / "manifest.json", started)
                ],
            ),
            phase_premise=phase_premise(started),
            arbitrary_signed_input_policy="new charged signed clamp [0,Q]",
            new_public_total_map_differs_from_original_Q_minus_one=True,
            actual_midpoint_wrap_domains_strictly_between_zero_and_Q=True,
            full_G2=False,
            cost_transfer=False,
        ),
        graphs,
    )


def same(actual, expected, message):
    require(actual == expected, message)


def legacy_tick(started, admission=False):
    require(started == (0, _STARTED), "Inherited source walker includes actual process creation")
    budget(admission=admission)


def legacy_read(path, started):
    legacy_tick(started)
    return read(path)


def legacy_resolved(path, started):
    legacy_tick(started)
    return canonical(path)


def legacy_relative(path, started):
    legacy_tick(started)
    actual = canonical(path)
    require(actual.is_relative_to(ROOT), "Inherited source member is workspace confined")
    return actual.relative_to(ROOT).as_posix()


def legacy_read_bytes(path, started):
    """Exact admitted bytes only; neither a scientific import nor an expectation waiver."""
    legacy_tick(started)
    return admitted_bytes(path)


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


def flags():
    return {
        "one_fixed_cosine_component_screen": True,
        "original_scientific_receipts_unchanged": True,
        "previous_A14_rejected_rows_unchanged": True,
        "independent130_scientific_audit_still_required": True,
        "full_G2": False,
        "adoption": False,
        "cost_transfer": False,
        "global_financial_gate_emission_authorized": False,
        "quantum_advantage": False,
        "new_test_credit": 0,
        "new_credited_gate_replays": 0,
        "new_price_samples": 0,
    }


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
    if _SCIENCE_ADMITTED:
        allowed.add(BUILDER_MODULE)
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


def dyadic(lower, upper=None):
    budget()
    lower = Fraction(lower)
    upper = lower if upper is None else Fraction(upper)
    require(lower <= upper, "Ordered exact oracle interval")
    scale = 1 << ORACLE_BITS
    return (
        lower.numerator * scale // lower.denominator,
        -((-upper.numerator * scale) // upper.denominator),
    )


def d_add(first, second):
    return first[0] + second[0], first[1] + second[1]


def d_neg(value):
    return -value[1], -value[0]


def d_multiply(first, second):
    budget()
    products = [left * right for left in first for right in second]
    scale = 1 << ORACLE_BITS
    return min(products) // scale, -((-max(products)) // scale)


def d_divide(value, divisor):
    require(type(divisor) is int and divisor > 0, "Exact positive interval divisor")
    return value[0] // divisor, -((-value[1]) // divisor)


def d_fraction(value):
    scale = 1 << ORACLE_BITS
    return Fraction(value[0], scale), Fraction(value[1], scale)


def exact_pi_oracle():
    """Machin identity and fixed alternating atan partial sums, with exact remainders."""

    def atan(inverse):
        total = Fraction(0)
        for index in range(ATAN_TERMS):
            budget()
            total += Fraction((-1) ** index, (2 * index + 1) * inverse ** (2 * index + 1))
        following = total + Fraction(
            (-1) ** ATAN_TERMS, (2 * ATAN_TERMS + 1) * inverse ** (2 * ATAN_TERMS + 1)
        )
        return min(total, following), max(total, following)

    first, second = atan(5), atan(239)
    bounds = 16 * first[0] - 4 * second[1], 16 * first[1] - 4 * second[0]
    require(
        Fraction(3) < bounds[0] <= bounds[1] < Fraction(16, 5), "Exact Machin pi paper premises"
    )
    return dyadic(*bounds), bounds


def exact_coefficient_oracle(pi, segment, degree):
    """Outward dyadic polynomial plus derivative-bounded cosine Taylor remainder."""
    budget()
    scale = 1 << ORACLE_BITS
    one = scale, scale
    twice = d_multiply(pi, dyadic(2))
    argument = d_multiply(pi, dyadic(Fraction(2 * segment + 1, 64) + Fraction(degree, 2)))
    require(0 <= argument[0] <= argument[1] < 16 * scale, "Every fixed trig argument in [0,16)")
    square = d_multiply(argument, argument)
    term, total = one, one
    for index in range(1, COS_TERMS):
        budget()
        term = d_divide(d_multiply(term, square), (2 * index - 1) * (2 * index))
        total = d_add(total, d_neg(term) if index % 2 else term)
    remainder = Fraction(16 ** (2 * COS_TERMS), factorial(2 * COS_TERMS))
    remainder_word = dyadic(0, remainder)[1]
    cosine = total[0] - remainder_word, total[1] + remainder_word
    power = one
    for _ in range(degree):
        power = d_multiply(power, twice)
    answer = d_divide(d_multiply(power, cosine), factorial(degree))
    bounds = d_fraction(answer)
    require(
        bounds[1] - bounds[0] < Fraction(1, 10**DIGITS),
        "Fixed exact oracle exceeds90 decimal digits",
    )
    budget()
    return bounds


def make_literals(mp):
    budget()
    pi, exact_pi = exact_pi_oracle()
    rows, centers, table = [], [], []
    all_half, all_contained = True, True
    for segment in range(64):
        budget()
        center = Fraction(2 * segment + 1, 128)
        center_raw = (2 * segment + 1) << 37
        require(
            Fraction(center_raw, IQ) == center, "Every center has exact native F44 representation"
        )
        centers.append({"segment": segment, "raw": center_raw, "center_exact": encode(center)})
        native_row = [center_raw]
        for degree in range(7):
            budget()
            oracle = exact_coefficient_oracle(pi, segment, degree)
            value = (
                (2 * mp.iv.pi) ** degree
                * mp.iv.cos(2 * mp.iv.pi * outward(mp, center) + degree * mp.iv.pi / 2)
                / factorial(degree)
            )
            primary = endpoints(value)
            contained = primary[0] <= oracle[0] <= oracle[1] <= primary[1]
            raw = nearest(IQ * (primary[0] + primary[1]) / 2)
            require(
                type(raw) is int and -(1 << 71) <= raw < 1 << 71, "Canonical signed72 F44 literal"
            )
            error = max(abs(Fraction(raw, IQ) - bound) for bound in primary)
            half = error <= IEPS / 2
            all_half, all_contained = all_half and half, all_contained and contained
            rows.append(
                {
                    "segment": segment,
                    "degree": degree,
                    "center_raw": center_raw,
                    "raw": raw,
                    "true_coefficient_enclosure": [encode(v) for v in primary],
                    "exact_rational_oracle_enclosure": [encode(v) for v in oracle],
                    "primary90_contains_exact_oracle": contained,
                    "exact_rounding_reference": encode((primary[0] + primary[1]) / 2),
                    "actual_abs_error_upper": encode(error),
                    "true_nearest_half_ULP_certified": half,
                }
            )
            native_row.append(raw)
        table.append(native_row)
    return {
        "schema": "a14-f44-stage-c-primary90-literals-v1",
        "row_id": ROW_ID,
        "coefficient_rows": rows,
        "center_rows": centers,
        "coefficient_count": 448,
        "center_count": 64,
        "table": table,
        "table_literal_count": 512,
        "primary_digits": DIGITS,
        "oracle_bits": ORACLE_BITS,
        "Machin_atan_terms": ATAN_TERMS,
        "cosine_Taylor_terms": COS_TERMS,
        "exact_Machin_pi_enclosure": [encode(v) for v in exact_pi],
        "all_primary_intervals_authorized_by_exact_oracle": all_contained,
        "all_actual_half_ULP_premises_certified": all_half,
        "literal_selection": "exact ties-even of2^44 times saved rational90 midpoint",
    }


def uniform_certificate(literals, old_error):
    budget()
    pi_hi = rational(literals["exact_Machin_pi_enclosure"][1])
    tail = (2 * pi_hi * H) ** 7 / factorial(7)
    floors = IEPS * sum((H**exponent for exponent in range(6)), Fraction(0))
    rounding = EPS / 2
    records = []
    for segment in range(64):
        budget()
        rows = literals["coefficient_rows"][7 * segment : 7 * (segment + 1)]
        require(
            [(r["segment"], r["degree"]) for r in rows] == [(segment, d) for d in range(7)],
            "Complete canonical fixed coefficient order",
        )
        paid = sum(
            (rational(row["actual_abs_error_upper"]) * H ** row["degree"] for row in rows),
            Fraction(0),
        )
        records.append(
            {
                "segment": segment,
                "actual_literal_error_upper": encode(paid),
                "Taylor_tail_upper": encode(tail),
                "six_floor_upper": encode(floors),
                "final_signed_ties_even_rounding_upper": encode(rounding),
                "cosine_error_upper": encode(paid + tail + floors + rounding),
            }
        )
    actual = max(rational(row["cosine_error_upper"]) for row in records)
    premises = (
        literals["all_primary_intervals_authorized_by_exact_oracle"]
        and literals["all_actual_half_ULP_premises_certified"]
    )
    conditional = Fraction(1009, 1270) * EPS
    paper_checks = (
        tail < EPS / 5
        and (IEPS / 2) * sum(H**j for j in range(7)) + floors < Fraction(12, 127) * EPS
        and conditional < EPS <= old_error
    )
    passed = premises and paper_checks and actual < conditional and actual < old_error
    return {
        "schema": "a14-f44-stage-c-uniform-certificate-v1",
        "row_id": ROW_ID,
        "all64_closed_segments": records,
        "cosine_error_upper": encode(actual),
        "conditional_paper_upper": encode(conditional),
        "original_E_old": encode(old_error),
        "closed_local_interval": [encode(-H), encode(H)],
        "all_actual_half_ULP_and_oracle_premises": premises,
        "paper_tail_geometric_and_original_formula_checks": paper_checks,
        "uniform_component_gate_passed": passed,
        "projection_and_exact_axes_nonexpansive": True,
        **flags(),
    }


def native_certificate(literals):
    budget()
    local = -(1 << 37), (1 << 37) - 16
    records, all_passed = [], True
    for segment, table_row in enumerate(literals["table"]):
        budget()
        center, words = table_row[0], table_row[1:]
        u = segment << 34, ((segment + 1) << 34) - 1
        rescaled = u[0] << 4, u[1] << 4
        require(
            (rescaled[0] - center, rescaled[1] - center) == local,
            "Every exact digital segment derives signed38 local range",
        )
        value, steps = (words[6], words[6]), []
        initial_promises = (
            0 <= u[0] <= u[1] < Q
            and center == (2 * segment + 1) << 37
            and 0 <= center < 1 << 71
            and 0 <= rescaled[0] <= rescaled[1] < 1 << 71
            and -(1 << 37) <= local[0] <= local[1] < 1 << 37
            and center % 16 == 0
            and all(-(1 << 51) <= v < 1 << 51 for v in words)
        )
        passed = initial_promises
        for degree in range(5, -1, -1):
            budget()
            signed52 = -(1 << 51) <= value[0] <= value[1] < 1 << 51
            products = [a * b for a in value for b in local]
            product = min(products), max(products)
            product_safe = -(1 << 89) <= product[0] <= product[1] < 1 << 89
            floor = product[0] // IQ, product[1] // IQ
            floor_safe = -(1 << 71) <= floor[0] <= floor[1] < 1 << 71
            following = floor[0] + words[degree], floor[1] + words[degree]
            stored = -(1 << 71) <= following[0] <= following[1] < 1 << 71
            passed = passed and signed52 and product_safe and floor_safe and stored
            steps.append(
                {
                    "degree": degree,
                    "accumulator_operand_raw_interval": list(value),
                    "signed52_operand_authorized": signed52,
                    "local_signed38_raw_interval": list(local),
                    "semantic_signed144_and_retained116_product_interval": list(product),
                    "signed90_product_safe": product_safe,
                    "floor44_output_interval": list(floor),
                    "signed72_floor_output_safe": floor_safe,
                    "exact_add_output_interval": list(following),
                    "signed72_add_safe": stored,
                }
            )
            value = following
        rounded = nearest(Fraction(value[0], 16)), nearest(Fraction(value[1], 16))
        round_safe = -(1 << 71) <= rounded[0] <= rounded[1] < 1 << 71
        passed = passed and round_safe
        all_passed = all_passed and passed
        records.append(
            {
                "segment": segment,
                "exact_eager_u_interval": list(u),
                "rescaled_F44_raw_interval": list(rescaled),
                "center44_raw": center,
                "all_initial_rescale_center_local_literal_promises": initial_promises,
                "derived_digital_local_raw_interval": list(local),
                "Horner_steps": steps,
                "final_round_input_interval": list(value),
                "round_output_interval": list(rounded),
                "all_eager_native_promises_passed": passed,
            }
        )
    return {
        "schema": "a14-f44-stage-c-all64-native-certificate-v1",
        "row_id": ROW_ID,
        "segment_rows": records,
        "all64_native_promises_passed": all_passed,
        "signed_clamp_0_to_Q_before_eager_work": True,
        "Q_selected_to_zero_before_lookup": True,
        "address_high66_bits_zero": True,
        "local_low_four_bits_zero": True,
        "hypothetical_closed_positive_endpoint_not_native_caller": True,
        "final_projected_signed72_output_interval": [-Q, Q],
        **flags(),
    }


def native_words(path, *, numpy_header, expected_rows=None, qubits):
    budget()
    require(
        sys.byteorder == "little" and array("i").itemsize == 4, "Exact Win64 little-endian int32"
    )
    content = admitted_bytes(path, 32 * 1024**2 + 65536)
    offset = 0
    if numpy_header:
        require(
            content[:6] == b"\x93NUMPY" and content[6:8] in (b"\x01\x00", b"\x02\x00"),
            "Only fixed bounded NumPy file versions1/2, no NumPy import",
        )
        width = 2 if content[6] == 1 else 4
        require(len(content) >= 8 + width, "Complete fixed NumPy length header")
        count = int.from_bytes(content[8 : 8 + width], "little")
        offset = 8 + width + count
        require(0 < count <= 65536 and offset <= len(content), "Bounded complete native header")
        header = ast.literal_eval(content[8 + width : offset].decode("ascii"))
        require(
            type(header) is dict
            and set(header) == {"descr", "fortran_order", "shape"}
            and header["descr"] == "<i4"
            and header["fortran_order"] is False,
            "Only strict little-endian int32 row-major native array",
        )
        shape = header["shape"]
        require(
            type(shape) is tuple
            and len(shape) == 2
            and shape[1] == 4
            and type(shape[0]) is int
            and 0 <= shape[0] <= MAX_NATIVE_ROWS,
            "Complete Nx4 actual native shape",
        )
        require(expected_rows is None or shape[0] == expected_rows, "Declared native row count")
        expected_rows = shape[0]
    require(
        type(expected_rows) is int
        and 0 <= expected_rows <= MAX_NATIVE_ROWS
        and len(content) - offset == expected_rows * 16,
        "Exact complete int32 payload size",
    )
    words = array("i")
    words.frombytes(content[offset:])
    for row in range(expected_rows):
        if row % 128 == 0:
            budget()
        kind, a, b, c = words[4 * row : 4 * row + 4]
        wires = (a, b, c)[:kind]
        require(
            kind in (1, 2, 3)
            and len(set(wires)) == kind
            and all(0 <= wire < qubits for wire in wires)
            and all(value == 0 for value in (a, b, c)[kind:]),
            "Every actual X/CX/CCX native row is canonical and confined",
        )
    budget()
    return words


def admitted_leaves(binding):
    budget()
    leaves = {}
    for name in ("ADD", "SUB"):
        first = binding["cases"]["B4x12"]["selected_primitive_profiles"][name]
        second = binding["cases"]["B8x52"]["selected_primitive_profiles"][name]
        require(
            not first.get("resource_rejected") and first["gate_sha256"] == second["gate_sha256"],
            "Same actual valid BK72 raw leaf across both original sources",
        )
        entries = read(ROOT / first["descriptor_path"])
        require(type(entries) is list, "Actual A08 leaf_screen is a list")
        chosen = [
            entry
            for entry in entries
            if entry["op"] == name.lower()
            and entry["width"] == W
            and entry["variant"] == "brent-kung"
        ]
        require(len(chosen) == 1, "ONE actual full72 Brent-Kung leaf")
        descriptor = chosen[0]
        require(
            descriptor["args"] == [list(range(72)), list(range(72, 144))]
            and descriptor["outs"] == [list(range(144, 216))]
            and descriptor["resources"] == first["resources"],
            "Actual descriptor/port/resource agreement",
        )
        gate_path = ROOT / first["gate_path"]
        require(
            _FROZEN[key_for(canonical(gate_path))] == first["gate_sha256"],
            "Original expected native leaf SHA",
        )
        words = native_words(
            gate_path,
            numpy_header=True,
            expected_rows=descriptor["resources"]["source_gates"],
            qubits=descriptor["resources"]["qubits"],
        )
        leaves[name] = {
            "descriptor": descriptor,
            "words": words,
            "gate_SHA256": first["gate_sha256"],
        }
    descriptors = read(SOURCE / "primitive_descriptors.json")
    arrays = read(SOURCE / "native_gate_arrays.json")
    for name, key in (("MUL", "multiplier"), ("ROUND", "rounder")):
        descriptor, saved = descriptors[key], arrays[key]
        require(
            descriptor["schema"] == "a14-f44-stage-k-clean-arithmetic-leaf-v1"
            and descriptor["spec"]["width"] == 72
            and descriptor["input_preserved"] is True
            and descriptor["dirty_output_XOR"] is True
            and descriptor["private_workspace_zero_entry_exit"] is True,
            "Exact independently audited Stage K full72 clean leaf",
        )
        arity = 2 if name == "MUL" else 1
        require(
            descriptor["args"] == [list(range(72 * i, 72 * (i + 1))) for i in range(arity)]
            and descriptor["outs"] == [list(range(72 * arity, 72 * (arity + 1)))],
            "Exact K actual full72 port/argument maps",
        )
        if name == "MUL":
            require(
                descriptor["spec"]["fraction_bits"] == 44
                and descriptor["spec"]["product_width"] == 116
                and descriptor["spec"]["active_operand_bits"] == [52, 38]
                and descriptor["spec"]["input_contract"] == {"signed_operand_bits": [52, 38]}
                and descriptor["full_signed_semantic_product_bits"] == 144
                and descriptor["generic_active_signed_product_bits"] == 90,
                "Only exact fresh52x38/F44/116 realization, not old F40 costs",
            )
        else:
            require(
                descriptor["spec"]["input_fraction_bits"] == 44
                and descriptor["spec"]["output_fraction_bits"] == 40
                and descriptor["spec"]["input_contract"] == {},
                "Actual universal signed ties-even K leaf",
            )
        gate_path = SOURCE / saved["gate_file"]
        require(
            saved["rows"] == descriptor["gate_rows"]
            and _FROZEN[key_for(canonical(gate_path))] == saved["gate_SHA256"],
            "Actual K binary tied to exact expected descriptor/array receipt",
        )
        words = native_words(
            gate_path, numpy_header=False, expected_rows=saved["rows"], qubits=descriptor["qubits"]
        )
        leaves[name] = {
            "descriptor": descriptor,
            "words": words,
            "gate_SHA256": saved["gate_SHA256"],
        }
    budget()
    return leaves


def kernel_checkpoint():
    """Fixed128 callback guard plus controller entry/exit guards; no adaptive cadence."""
    kernel_checkpoint.calls += 1
    if kernel_checkpoint.calls % 128 == 0:
        budget()


kernel_checkpoint.calls = 0


def call_kernel(function, *args, **kwargs):
    budget()
    result = function(*args, **kwargs)
    budget()
    return result


def prototype_diagnostics(builder, circuit, descriptor, table, leaves):
    budget()
    cases = builder.fixed_native_cases()
    expected_inputs = (
        -(1 << 71),
        -1,
        0,
        1,
        (1 << 33) - 1,
        1 << 33,
        (1 << 34) - 1,
        1 << 34,
        (1 << 34) + 1,
        Q // 4,
        Q // 2,
        3 * Q // 4,
        Q - 1,
        Q,
        Q + 1,
        (1 << 71) - 1,
    )
    require(
        cases == [(v, dirty) for v in expected_inputs for dirty in (0, (1 << 72) - 1)],
        "Exactly32 frozen full-map cases; no sampled/expanded corpus",
    )
    records, mask = [], (1 << 72) - 1
    for value, dirty in cases:
        budget()
        original = (value & mask) | (dirty << 72)
        expected = (value & mask) | ((dirty ^ builder.scalar_reference(value & mask, table)) << 72)
        forward = call_kernel(builder.replay, circuit, original, budget)
        reverse = call_kernel(builder.replay, circuit, forward, budget, inverse=True)
        matched = forward == expected and reverse == original
        require(matched, "Actual forward/reverse entire allocated state, private+SSA zero")
        records.append(
            {
                "input_signed_raw": value,
                "dirty_output": dirty,
                "expected_output": (expected >> 72) & mask,
                "actual_output": (forward >> 72) & mask,
                "entire_allocated_state_compared": True,
                "forward_and_literal_inverse_passed": matched,
            }
        )
    round_leaf = leaves["ROUND"]
    rounding_circuit = builder.Circuit(kernel_checkpoint)
    rounding_circuit.qubits = round_leaf["descriptor"]["qubits"]
    rounding_circuit.gates = round_leaf["words"]
    ties = []
    for value in (-24, -8, 8, 24):
        for dirty in (0, mask):
            budget()
            original = (value & mask) | (dirty << 72)
            exact = nearest(Fraction(value, 16)) & mask
            expected = (value & mask) | ((dirty ^ exact) << 72)
            forward = call_kernel(builder.replay, rounding_circuit, original, budget)
            reverse = call_kernel(builder.replay, rounding_circuit, forward, budget, inverse=True)
            require(
                forward == expected and reverse == original,
                "Eight fixed K signed round ties retain full wire state",
            )
            ties.append(
                {
                    "F44_input_raw": value,
                    "dirty_output": dirty,
                    "expected_F40_output": exact,
                    "entire_allocated_state_forward_inverse_passed": True,
                }
            )
    return {
        "schema": "a14-f44-stage-c-fixed-native-diagnostics-v1",
        "full_map_cases": records,
        "standalone_round_ties": ties,
        "full_map_case_count": 32,
        "whole_prototype_forward_calls": 32,
        "whole_prototype_actual_reverse_calls": 32,
        "whole_prototype_total_replays": 64,
        "standalone_round_tie_case_count": 8,
        "standalone_round_leaf_total_replays": 16,
        "K_Boolean_diagnostics_duplicated": False,
        **flags(),
    }


def save_gate_array(circuit):
    budget()
    require(0 < circuit.rows <= MAX_NATIVE_ROWS, "ONE complete bounded clean prototype")
    target = OUTPUT / "cosine.gates.bin"
    members = inventory(OUTPUT)
    bytes_total = circuit.rows * 16
    require(
        not target.exists()
        and len(members) + 2 <= MAX_OWN_FILES
        and sum(path.stat().st_size for path in members) + bytes_total <= MAX_OWN_BYTES,
        "Actual gate bytes admitted with final manifest slot",
    )
    with target.open("xb") as stream:
        for offset in range(0, len(circuit.gates), 16384):
            budget()
            stream.write(circuit.gates[offset : offset + 16384].tobytes())
    require(target.stat().st_size == bytes_total, "Complete actual saved gate payload")
    return {
        "gate_file": target.name,
        "gate_SHA256": digest(target, fresh=True),
        "rows": circuit.rows,
        "bytes": bytes_total,
        "row_format": "little-endian int32 Nx4 X/CX/CCX",
    }


def complete_source_resources(binding, descriptor, resources):
    budget()
    serial = resources["matched_serial_event_chronology"]["sums"]
    clean = {
        field: (serial[field] if field in serial else resources[field]) for field in RESOURCE_FIELDS
    }
    require(
        clean["source_gates"] == descriptor["gate_rows"]
        and clean["t_count"] == resources["t_count"],
        "Same actual clean prototype counts and matched serial event depths",
    )
    outer = {field: 0 for field in RESOURCE_FIELDS}
    outer.update(source_gates=144, cx=144, clifford_t_depth=2, clifford_cx=144)
    cases = {}
    for case, original in binding["cases"].items():
        budget()
        source = read(ROOT / original["source_path"])
        sums = {field: 0 for field in RESOURCE_FIELDS}
        copies, copy_depth = 0, 0
        for call in source["forward_calls"]:
            kernel_checkpoint()
            old = _OLD_DESCRIPTORS[(case, call["leaf"])]
            unit = old["resources"]
            require(
                unit["t_count"] == 7 * unit["ccx"]
                and unit["schedule"] == "exact seven-T Toffoli; all-to-all ASAP within each leaf",
                "Every original actual leaf uses the same paid exact7T schedule",
            )
            for field in RESOURCE_FIELDS:
                sums[field] += unit[field]
            copies += call["argument_copy_cx"]
            copy_depth += max(Counter(call["args"]).values(), default=0)
        rebuilt = {field: 2 * sums[field] for field in RESOURCE_FIELDS}
        for field in ("source_gates", "cx", "clifford_cx"):
            rebuilt[field] += 2 * copies + 72 * len(source["outputs"])
        rebuilt["clifford_t_depth"] += 4 * copy_depth + max(
            Counter(source["outputs"].values()).values(), default=0
        )
        baseline = {field: original["original_resources"][field] for field in RESOURCE_FIELDS}
        require(
            rebuilt == baseline,
            "All original call resources/copy multiplicities reconstruct the exact baseline",
        )
        removed = {field: 0 for field in RESOURCE_FIELDS}
        for call in original["removal"]["removed_forward_calls"]:
            budget()
            old = _OLD_DESCRIPTORS[(case, call["leaf"])]
            require(
                call["argument_copy_cx"] == 2 * 72 * len(call["args"]),
                "Every removed old argument copy paid",
            )
            for field in RESOURCE_FIELDS:
                removed[field] += old["resources"][field]
            for field in ("source_gates", "cx", "clifford_cx"):
                removed[field] += call["argument_copy_cx"]
            removed["clifford_t_depth"] += 2 * max(Counter(call["args"]).values(), default=0)
        sites = original["cosine_sites"]
        require(sites == CASE_SITES[case], "All60/468 cosine sites, both pair coordinates retained")
        added = {field: 2 * sites * (clean[field] + outer[field]) for field in RESOURCE_FIELDS}
        estimated = {
            field: baseline[field] - 2 * removed[field] + added[field] for field in RESOURCE_FIELDS
        }
        require(
            all(value >= 0 for value in estimated.values()),
            "No unmatched negative whole-source subtraction",
        )
        workspace = descriptor["qubits"] - 2 * 72
        whole_qubits = original["original_resources"]["logical_qubits"] + workspace + 72
        standalone = descriptor["qubits"]
        within = standalone <= 131072 and whole_qubits <= BASELINE[case][2]
        improvement = (
            estimated["t_count"] < baseline["t_count"]
            and estimated["t_depth"] < baseline["t_depth"]
        )
        cases[case] = {
            "original_whole_source": baseline,
            "reconstructed_original_serial_baseline": rebuilt,
            "all_original_actual_leaf_memberships": _OLD_DESCRIPTOR_MEMBERSHIPS[case],
            "removed_twice": {k: 2 * v for k, v in removed.items()},
            "added_twice_complete_clean_plus_outercopies": added,
            "estimated_whole_source": estimated,
            "whole_qubits_conservative": whole_qubits,
            "standalone_clean_qubits": standalone,
            "new_full_SSA_private_history_banks": descriptor["SSA_full72_banks"],
            "actual_reused_private_bank_qubits": descriptor["full72_private_leaf_capacity"],
            "all_original_storage_and_scratch_retained": True,
            "outer_argument_bank_and_both144CX_copies_paid": True,
            "both_global_directions_paid": True,
            "within_original_caps": within,
            "T_count_and_matched_serial_T_depth_improve": improvement,
            "original_measured_depth_context_only": BASELINE[case][1],
            "resource_gate_passed": within and improvement,
        }
    return {
        "schema": "a14-f44-stage-c-complete-source-resource-comparison-v1",
        "actual_clean_prototype_resource": resources,
        "matched_serial_clean_function_resource": clean,
        "cases": cases,
        "all_resource_gates_passed": all(v["resource_gate_passed"] for v in cases.values()),
        "fixed_point_removal_and_serial_clean_workspace_reuse_only": True,
        **flags(),
    }


def admit_original_cost_descriptors():
    """Only exact A10 flat-owner selected JSON closure, before numerical admission."""
    budget()
    owner_directory = PROGRAM / "A10_coefficient_run001"
    owner_path = owner_directory / "manifest.json"
    owner_sha = "0a732d7f487bca1efd298e7eca4feb2f2d2e83d1958ebb9a14ee9b32a0d78a40"
    require(
        _FROZEN[key_for(canonical(owner_path))] == owner_sha,
        "Only the exact already source-bound legacy flat A10 owner may decode separators",
    )
    owner = read(bind(owner_path, owner_sha))
    require(type(owner) is dict, "Exact flat original coefficient owner")
    for case in CASES:
        budget()
        directory = owner_directory / case / "min-depth"
        source = read(directory / "source.json")
        require(
            source["format"] == "hierarchical-clean-xor-source-v1"
            and source["word_width"] == 72
            and source["fraction_bits"] == 40,
            "Actual immutable original complete caller source",
        )
        memberships = {}
        for call in source["forward_calls"]:
            kernel_checkpoint()
            leaf = call["leaf"]
            require(
                type(leaf) is str
                and len(leaf) == 20
                and all(char in "0123456789abcdef" for char in leaf),
                "Exact original content-key leaf",
            )
            cache_key = case, leaf
            if cache_key in _OLD_DESCRIPTORS:
                continue
            path = directory / "leaves" / (leaf + ".json")
            relative = path.relative_to(owner_directory).as_posix()
            found = [
                (key, expected)
                for key, expected in owner.items()
                if type(key) is str and key.replace("\\", "/") == relative
            ]
            require(
                len(found) == 1, "Unique exact original flat-owner selected descriptor spelling"
            )
            key, expected = found[0]
            actual = bind(path, expected)
            require(
                actual.relative_to(owner_directory).as_posix() == relative,
                "Legacy separator decoding never relaxes actual selected physical spelling",
            )
            entry = read(actual)
            unit = entry["resources"]
            require(
                all(type(unit[field]) is int and unit[field] >= 0 for field in RESOURCE_FIELDS),
                "Exact nonnegative actual original cost fields",
            )
            _OLD_DESCRIPTORS[cache_key] = entry
            memberships[leaf] = {
                "owner_manifest": key_for(owner_path),
                "owner_manifest_SHA256": owner_sha,
                "original_key": key,
                "original_expected_SHA256": expected,
                "actual_selected_path": key_for(actual),
            }
        _OLD_DESCRIPTOR_MEMBERSHIPS[case] = memberships
    budget()


def admission(expected_ready_sha):
    budget()
    ready = read(bind(READY, expected_ready_sha))
    require(
        ready["schema"] == "root-a14-f44-cosine-stage-c-READY-v3"
        and ready["ready"] is True
        and ready["root_and_independent_static_reviews_passed"] is True
        and ready["Stage_C_component_execution_authorized"] is True,
        "Separate externally ROOT-frozen Stage C component release",
    )
    require(
        ready["output"] == OUTPUT.relative_to(ROOT).as_posix()
        and ready["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL],
        "Fixed route and process budgets",
    )
    for key in (
        "full_G2",
        "financial_adoption",
        "cost_transfer",
        "quantum_advantage",
        "global_financial_gate_emission_authorized",
    ):
        require(ready[key] is False, "ROOT release never authorizes a financial transfer")
    require(ready["fixture_credit"] == 0, "No added fixture credit")
    own = ready["author_method_SHA256"]
    require(
        set(own) == {AUTHOR.name, BUILDER.name, BUILDER_NOTE.name, METHOD_DOC.name, PREFLIGHT.name},
        "Exactly five new controller/builder/method files",
    )
    require(
        own[BUILDER.name] == BUILDER_SHA and own[BUILDER_NOTE.name] == BUILDER_NOTE_SHA,
        "Independent builder's externally supplied stable pins",
    )
    for name, expected in own.items():
        bind(RESEARCH / name, expected)
    policy = read(PREFLIGHT)
    require(
        policy["schema"] == "a14-f44-cosine-stage-c-implementation-preflight-v3"
        and policy["row_id"] == ROW_ID
        and policy["primary_digits"] == DIGITS
        and policy["independent_digits"] == 130
        and policy["oracle_bits_atan_terms_cosine_terms"] == [ORACLE_BITS, ATAN_TERMS, COS_TERMS]
        and policy["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
        and policy["owned_caps_files_bytes"] == [MAX_OWN_FILES, MAX_OWN_BYTES]
        and policy["runtime_caps_files_bytes"] == [MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES]
        and policy["reference_unique_bytes_hash_work_caps"]
        == [MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK]
        and policy["native_rows_cap"] == MAX_NATIVE_ROWS
        and policy["fixed_native_diagnostic_counts"] == [32, 8]
        and policy["fixed_native_replay_counts"] == [64, 16],
        "Exact prospectively fixed finite method",
    )
    for path, expected in ((PROSPECTUS, PROSPECTUS_SHA), (PROSPECTUS_DOC, PROSPECTUS_DOC_SHA)):
        bind(path, expected)
    prospectus = read(PROSPECTUS)
    require(
        prospectus["row_id"] == ROW_ID
        and prospectus["internal"]["coefficient_words"] == 448
        and prospectus["internal"]["center_words"] == 64
        and prospectus["stage_C"]["producer_CPU_admission_wall_seconds"] == [CPU, ADMISSION, WALL],
        "Same one-row original F44 prospectus",
    )
    expected_packets = {name: pin for name, (pin, _) in COSINE_PACKETS.items()}
    expected_packets.update(
        {SOURCE_NAME: SOURCE_SHA, AUDIT_NAME: AUDIT_SHA, ROOT_INTEGRITY_NAME: ROOT_INTEGRITY_SHA}
    )
    expected_counts = {name: counts for name, (_, counts) in COSINE_PACKETS.items()}
    expected_counts.update(
        {
            SOURCE_NAME: SOURCE_COUNTS,
            AUDIT_NAME: AUDIT_COUNTS,
            ROOT_INTEGRITY_NAME: ROOT_INTEGRITY_COUNTS,
        }
    )
    require(
        ready["completed_prerequisite_manifest_SHA256"] == expected_packets
        and ready["completed_prerequisite_complete_counts"] == expected_counts
        and policy["completed_prerequisite_manifest_SHA256"] == expected_packets
        and policy["completed_prerequisite_complete_counts"] == expected_counts,
        "All five exact completed prerequisites externally pinned, never observed-as-expected",
    )
    admitted = {}
    for name, expected in expected_packets.items():
        admitted[name] = packet(name, expected, expected_counts[name])
    integrity = admitted[ROOT_INTEGRITY_NAME]
    require(
        integrity["schema"] == "a14-taylor-f44-stage-k-root-integrity-manifest-v1"
        and integrity["metadata_integrity_only"] is True
        and integrity["new_scientific_evaluation"] is False
        and integrity["source_manifest_SHA256"] == SOURCE_SHA
        and integrity["audit_manifest_SHA256"] == AUDIT_SHA
        and integrity["Stage_C_release_authorized"] is False
        and len(integrity["both_full_uncached_input_unions"]) == 2
        and all(
            item["full_fresh_resolve_and_SHA"] is True
            for item in integrity["both_full_uncached_input_unions"]
        ),
        "Scoped actual K ROOT integrity PASS",
    )
    for name in (SOURCE_NAME, AUDIT_NAME, ROOT_INTEGRITY_NAME):
        packet_value = admitted[name]
        require(
            all(
                packet_value[k] is False
                for k in ("full_G2", "adoption", "cost_transfer", "quantum_advantage")
            )
            and all(
                type(packet_value[k]) is int and packet_value[k] == 0
                for k in ("new_test_credit", "new_credited_gate_replays", "new_price_samples")
            ),
            "All historical K receipts retain exact zero scientific/financial credit",
        )
    admit_original_cost_descriptors()
    source_summary, audit_summary = read(SOURCE / "summary.json"), read(AUDIT / "summary.json")
    require(
        source_summary["actual_array_matched_universal_structure"] is True
        and source_summary["absolute7T_phase_proof_bound"] is True
        and source_summary["fixed_diagnostic_counts"] == [16, 40, 32, 88]
        and audit_summary["independent_scientific_audit_complete"] is True
        and audit_summary["actual_binary_independent_replay"] is True
        and audit_summary["actual_resource_recount"] is True
        and audit_summary["source_manifest_SHA256"] == SOURCE_SHA,
        "Exact fresh primitives have both actual primary and independent scientific evidence",
    )
    executables = {canonical(LAUNCHER), canonical(sys._base_executable)}
    require(
        len(executables) == 2 and canonical(sys._base_executable) == _BASE_SCOPE / "python.exe",
        "Distinct exact actual launcher/base executables",
    )
    declared_executables = set()
    for spelling, expected in ready["interpreter_expected_SHA256"].items():
        actual = canonical(spelling)
        require(
            actual in executables and actual not in declared_executables,
            "Only distinct actual interpreter pins",
        )
        declared_executables.add(actual)
        bind(actual, expected)
    require(declared_executables == executables, "Both actual executable expected pins")
    require(
        ready["integer_decimal_digit_limit"]
        == policy["integer_decimal_digit_limit"]
        == INTEGER_DECIMAL_DIGITS
        and ready["integer_serialization_bit_cap"]
        == policy["integer_serialization_bit_cap"]
        == INTEGER_SERIALIZATION_BITS,
        "Exactly fixed bounded integer representation policy",
    )
    admit_prior_failure(ready, policy)
    preserved_prerequisite_caches()
    code_caches(
        [AUTHOR, BUILDER],
        ready["existing_new_code_cache_SHA256"],
        ready["absent_new_code_cache_paths"],
    )
    budget()
    return ready, policy


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


def load_science():
    global _SCIENCE_ADMITTED
    budget()
    require(
        not _SCIENCE_ADMITTED and BUILDER_MODULE not in sys.modules,
        "No earlier scientific source execution",
    )
    content = admitted_bytes(BUILDER)
    parsed = ast.parse(content)
    imports = [node for node in parsed.body if isinstance(node, (ast.Import, ast.ImportFrom))]
    require(
        len(imports) == 1
        and isinstance(imports[0], ast.ImportFrom)
        and imports[0].module == "array"
        and imports[0].level == 0
        and [(a.name, a.asname) for a in imports[0].names] == [("array", None)],
        "Builder has only its fixed stdlib array import",
    )
    check_code_caches()
    require(
        standard_runtime_members() == _STANDARD_RUNTIME_MEMBERS,
        "Complete admitted runtime membership unchanged immediately before loading",
    )
    loaded_origins()
    _SCIENCE_ADMITTED = True
    module = ModuleType(BUILDER_MODULE)
    module.__file__ = str(BUILDER)
    module.__package__ = "research.limitation_program_20261001"
    module.__cached__ = cache_from_source(str(BUILDER))
    sys.modules[BUILDER_MODULE] = module
    exec(compile(parsed, str(BUILDER), "exec"), module.__dict__)
    import mpmath as mp

    require(
        mp.__version__ == "1.3.0" and mp.libmp.BACKEND == "python",
        "Only pinned purePython mpmath1.3.0",
    )
    mp.mp.dps = DIGITS
    mp.iv.dps = DIGITS
    require(
        mp.mp.dps == mp.iv.dps == DIGITS
        and os.environ.get("MPMATH_NOGMPY") == os.environ.get("MPMATH_NOSAGE") == "1",
        "Exactly fixed primary90 with optional backends disabled",
    )
    loaded_origins()
    check_code_caches()
    budget()
    return module, mp


def main():
    global _STARTED
    _STARTED = process_started()
    runtime_scopes()
    fixed_integer_policy()
    for key in ("SAGE_ROOT", "MPMATH_SAGE"):
        require(not os.environ.get(key), "No inherited optional-backend overrides")
    for key in (
        "MPMATH_NOGMPY",
        "MPMATH_NOSAGE",
        "OMP_NUM_THREADS",
        "OPENBLAS_NUM_THREADS",
        "MKL_NUM_THREADS",
        "NUMEXPR_NUM_THREADS",
    ):
        os.environ[key] = "1"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ready-sha256", required=True)
    args = parser.parse_args()
    require(
        canonical(__file__) == AUTHOR and not OUTPUT.exists(),
        "One new fixed route; no automatic retry",
    )
    try:
        _, policy = admission(args.ready_sha256)
        package = package_runtime()
        runtime = own_runtime()
        loaded_origins()
        first = fresh_union()
        budget(admission=True)
        OUTPUT.mkdir(exist_ok=False)
        for path in (
            AUTHOR,
            BUILDER,
            BUILDER_NOTE,
            METHOD_DOC,
            PREFLIGHT,
            PROSPECTUS,
            PROSPECTUS_DOC,
            READY,
        ):
            copy(path, "executed_" + path.name)
        save(
            "run_started.json",
            {
                "created_UTC": datetime.now(timezone.utc).isoformat(),
                "PID": os.getpid(),
                "limits_CPU_admission_wall": [CPU, ADMISSION, WALL],
                **flags(),
            },
        )
        for path in (PRIOR_FAILURE_FREEZE, PRIOR_READY, PRIOR_LOG):
            copy(path, "prior_" + path.name)
        for path in (
            PRIOR_V2_WITNESS,
            PRIOR_V2_READY,
            PRIOR_V2_LOG,
            *(RESEARCH / name for name in PRIOR_V2_AUTHORS),
        ):
            copy(path, "prior_prefit_" + path.name)
        save(
            "prior_failed_owned_expected_map.json",
            read(PRIOR_FAILURE_FREEZE)["observed_owned_files"],
        )
        save("serialization_edge_diagnostics.json", serialization_edge_diagnostics())
        builder, mp = load_science()
        original_policy = read(ORIGINAL_METHOD)
        require(
            original_policy["author_sha256"]["experiment_cosine_feasibility.py"]
            == "dba562b13f4d250c04376927f431e5a39ceaedfdcfc5e8ebc579bb9cdad27112",
            "Exact admitted original source-walker text provenance",
        )
        binding, _ = source_binding(original_policy, _FROZEN, _EXTERNAL, (0, _STARTED))
        old_binding = read(PROGRAM / "A14_cosine_feasibility_run001/source_binding.json")
        require(
            binding == old_binding,
            "Full original source walk/user fixed point/error/ABI remains identical",
        )
        save("original_source_binding.json", binding)
        literals = make_literals(mp)
        save("primary90_literals.json", literals)
        uniform = uniform_certificate(
            literals, rational(binding["existing_E_old"]["cosine_error_upper"])
        )
        save("uniform_certificate.json", uniform)
        native = native_certificate(literals)
        save("all64_native_certificate.json", native)
        can_emit = (
            uniform["uniform_component_gate_passed"] and native["all64_native_promises_passed"]
        )
        resource_passed, prototype_complete = False, False
        row = {
            "row_id": ROW_ID,
            "uniform_component_gate_passed": uniform["uniform_component_gate_passed"],
            "all64_native_promises_passed": native["all64_native_promises_passed"],
            "prototype_gate_emission_admitted_after_all_promises": can_emit,
            "candidate_eligible": False,
            **flags(),
        }
        if can_emit:
            leaves = admitted_leaves(binding)
            circuit, descriptor = call_kernel(
                builder.build_cosine, literals["table"], leaves, kernel_checkpoint
            )
            require(
                0 < circuit.rows <= MAX_NATIVE_ROWS
                and descriptor["gate_rows"] == circuit.rows
                and descriptor["qubits"] == circuit.qubits <= 16384,
                "One full bounded actual clean prototype",
            )
            structure = call_kernel(
                builder.verify_prototype,
                circuit,
                descriptor,
                literals["table"],
                leaves,
                kernel_checkpoint,
            )
            require(
                structure["actual_array_and_allocation_matched"] is True
                and structure["second_gate_array_generated"] is False,
                "Complete same-array structural binding",
            )
            save("prototype_descriptor.json", descriptor)
            save("actual_structural_certificate.json", {**structure, **flags()})
            save("native_gate_array.json", save_gate_array(circuit))
            diagnostics = prototype_diagnostics(
                builder, circuit, descriptor, literals["table"], leaves
            )
            save("fixed_native_diagnostics.json", diagnostics)
            resources = call_kernel(builder.resources, circuit, kernel_checkpoint, descriptor)
            save("actual_prototype_resources.json", resources)
            comparison = complete_source_resources(binding, descriptor, resources)
            save("whole_source_resource_comparison.json", comparison)
            resource_passed = comparison["all_resource_gates_passed"]
            prototype_complete = True
            row.update(
                native_rows=circuit.rows,
                native_qubits=circuit.qubits,
                actual_prototype_structure_diagnostics_resources_completed=True,
                resource_gate_passed=resource_passed,
            )
        else:
            row.update(
                actual_prototype_structure_diagnostics_resources_completed=False,
                resource_gate_passed=False,
                rejection_reason=(
                    "Fixed true-coefficient/half-ULP or native caller premise uncertified; "
                    "no gate emitted"
                ),
            )
        row["candidate_eligible"] = can_emit and resource_passed
        row["status"] = (
            "COMPONENT_SCREEN_ELIGIBLE_PENDING_INDEPENDENT130"
            if row["candidate_eligible"]
            else "REJECTED"
        )
        save("fixed_frontier_row.json", row)
        loaded_origins()
        check_code_caches()
        second = fresh_union()
        summary = {
            "schema": "a14-f44-stage-c-primary90-summary-v3",
            "representation_policy": {
                "decimal_digit_limit": INTEGER_DECIMAL_DIGITS,
                "per_integer_bit_cap": INTEGER_SERIALIZATION_BITS,
                "exact_rational_integer_pair_schema_unchanged": True,
                "fixed_serialization_edge_counts": [7, 2],
            },
            "prior_failed_run001_expected_freeze_SHA256": PRIOR_FAILURE_FREEZE_SHA,
            "prior_failed_run001_not_reused_or_approved": True,
            "prior_V2_prefit_failure_witness_expected_SHA256": PRIOR_V2_WITNESS_SHA,
            "prior_V2_output_still_absent": True,
            "startup_flag_effective_default4300_and_no_overrides_verified": True,
            "completed": True,
            "passed": True,
            "budget_censored": False,
            "row": row,
            "completed_prerequisites": policy["completed_prerequisite_manifest_SHA256"],
            "primary_digits": DIGITS,
            "independent_digits_pending": 130,
            "coefficient_count": 448,
            "center_count": 64,
            "actual_prototype_completed": prototype_complete,
            "fixed_native_diagnostic_counts_if_emitted": [32, 8],
            "actual_native_replay_counts": [64, 16] if prototype_complete else [0, 0],
            "both_full_uncached_input_unions": [first, second],
            "current_runtime": {**runtime, **package},
            "budget": {
                "process_CPU_seconds": time.process_time(),
                "wall_seconds": time.monotonic() - _STARTED,
            },
            "limits_CPU_admission_wall": [CPU, ADMISSION, WALL],
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
                "Own reserve includes final manifest",
            )
            owned[path.relative_to(OUTPUT).as_posix()] = digest(path, fresh=True)
        complete_manifest(
            {
                "schema": "a14-f44-stage-c-primary90-manifest-v3",
                "integer_decimal_digit_limit": INTEGER_DECIMAL_DIGITS,
                "integer_serialization_bit_cap": INTEGER_SERIALIZATION_BITS,
                "prior_failed_run001_expected_freeze_SHA256": PRIOR_FAILURE_FREEZE_SHA,
                "prior_failed_run001_not_reused_or_approved": True,
                "prior_V2_prefit_failure_witness_expected_SHA256": PRIOR_V2_WITNESS_SHA,
                "prior_V2_output_still_absent": True,
                "startup_flag_effective_default4300_and_no_overrides_verified": True,
                "files": owned,
                "frozen_inputs": _FROZEN,
                "external_runtime_inputs": _EXTERNAL,
                "manifest_self_hash_excluded": True,
                "completed": True,
                "passed": True,
                "budget_censored": False,
                "row_status": row["status"],
                "both_full_uncached_input_unions": [first, second],
                "limits_CPU_admission_wall": [CPU, ADMISSION, WALL],
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
                    "row_status": row["status"],
                    "manifest_SHA256": digest(OUTPUT / "manifest.json", fresh=True),
                    **flags(),
                }
            ),
            flush=True,
        )
    except BaseException as error:
        retain_failure(error)
        raise


if __name__ == "__main__":
    main()
