"""Author-only caller-typed Stage C axis-tail component. ROOT release required.

No author execution. New saved arrays, every-row independent consumer, bounded
128-lane diagnostic and actual component resource/phase checks are prospective.
Original complete scientific receipts and resource rejection remain unchanged.
"""

import argparse
import ast
from array import array
import importlib.util
import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
import hashlib
from importlib.util import cache_from_source
import json
import os
from pathlib import Path
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
PROGRAM = ROOT / "results/limitation_program_20261001"
AUTHOR = RESEARCH / "experiment_f44_cosine_caller_grid_axis_v1.py"
METHOD_DOC = RESEARCH / "F44_COSINE_CALLER_GRID_AXIS_PREFLIGHT_V1.md"
PREFLIGHT = RESEARCH / "f44_cosine_caller_grid_axis_preflight_v1.json"
READY = ROOT / ".context/A14_F44_COSINE_CALLER_GRID_AXIS_ROOT_READY_run001.json"
OUTPUT = PROGRAM / "A14_taylor_f44_stage_C_grid_axis_run001"
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
SOURCE_NAME = "A14_taylor_f44_stage_C_run003"
AUDIT_NAME = "A14_taylor_f44_stage_C_audit_run001"
SOURCE, AUDIT = PROGRAM / SOURCE_NAME, PROGRAM / AUDIT_NAME
SOURCE_SHA = "7e68fca590bd18e396b8280ed1577ca5a8fc4df48e561f22eab17f0bec69b9fa"
# ROOT supplied this verified terminal expectation; never populated from a scan.
ROOT_DECLARED_AUDIT_SHA = "3de0e4a36928a630481ff12ba727e2fdc50512b6bd60b2cc2e94edbeb95d42ee"
SOURCE_COUNTS, AUDIT_COUNTS = [34, 851, 2842], [17, 890, 2842]
SOURCE_READY = ROOT / ".context/A14_F44_COSINE_STAGE_C_ROOT_READY_run003.json"
SOURCE_READY_SHA = "b781c1c80bc2ee381c9e35b3b83f9c4cadd0fc141c2e88ab214b73f5de2c67c0"
AUDIT_READY = ROOT / ".context/A14_F44_COSINE_STAGE_C_AUDIT_ROOT_READY_run001.json"
AUDIT_READY_SHA = "499c77ac13357e93bc1707ae27e6542429edd983879cb2b023da8243dca554df"
ACTUAL_AUDIT_ROOT = (
    ROOT / ".context/A14_F44_STAGE_C_AUDIT_ACTUAL_OWNED_ROOT_VERIFICATION_run001.json"
)
ACTUAL_AUDIT_ROOT_SHA = "b8af47d51348433f194a161c5eaa620c64c194d4b0ce37f9cd85a42e5cf2cd4d"
ROW_ID = "TAYLOR_D6_S64_W72_F44_TO_F40_MUL52x38"
CPU, ADMISSION, WALL = 300, 270, 900
MAX_OWN_FILES, MAX_OWN_BYTES = 64, 128 * 1024**2
MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = 24000, 2 * 1024**3
MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK = 100000, 8 * 1024**3, 24 * 1024**3
INTEGER_DECIMAL_DIGITS, INTEGER_SERIALIZATION_BITS = 20000, 65536
MAX_SERIALIZATION_VALUES = MAX_OWN_BYTES
FAILURE_NAMES = (
    "FAILED_UNSEALED.json",
    "failed_unsealed.json",
    "failure.json",
    "run_failure.json",
    "prepare_failure.json",
)
OWNERS = {
    "A14_cosine_feasibility_run001": [
        "bdb01b0c69d8fab3ee3d61f1c48ce5764f1ae09488f564d186f658f180e4156b",
        [24, 672, 2842],
    ],
    "A14_cosine_feasibility_audit_run003": [
        "52c88dc17c6a53b1df30bd93a431d3e263cb202462901589aaaa30bb87631f0f",
        [17, 752, 2842],
    ],
    "A14_taylor_f44_stage_K_run001": [
        "b03c8a7cb62655301b9a231eb987f38e5ec496f612206ff6701143f6cefb8b88",
        [17, 774, 2842],
    ],
    "A14_taylor_f44_stage_K_audit_run001": [
        "2c253beba55b1271dec594db8231c8bdbfcaffbf4d797dedb840eda72568f5be",
        [10, 796, 2842],
    ],
    "A14_taylor_f44_stage_K_root_verification_run001": [
        "24e316217afd614b577fe53921f54b7ad7c346737ec6e21c93500a795a1517d9",
        [8, 811, 2842],
    ],
    SOURCE_NAME: [SOURCE_SHA, SOURCE_COUNTS],
    AUDIT_NAME: [ROOT_DECLARED_AUDIT_SHA, AUDIT_COUNTS],
}
SOURCE_AUTHORS = {
    "experiment_f44_cosine_stage_c_v3.py": (
        "9dc012f3015dfa0ac7301bc14fc7bf5a69fe2169aa6c4c122d9bd9b1df1dfee6"
    ),
    "A14_F44_COSINE_STAGE_C_IMPLEMENTATION_PREFLIGHT_V3.md": (
        "e90ec80968a596fb2b16c80369c60832abfef2aee501f5e4162d1f0251c4185b"
    ),
    "a14_f44_cosine_stage_c_implementation_preflight_v3.json": (
        "85f0d5b8c7be6763c93c74eefce6ca9cbd54464f41ea29987831cb41d3561b41"
    ),
    "f44_cosine_stage_c_source.py": (
        "6aa28c87416e30558e459efe2c602866dcc9b2d76e236e93faae05fe65826a74"
    ),
    "F44_STAGE_C_BUILDER_INTERFACE_AUTHOR_V1.md": (
        "b737562b5bafdc271d5c08cf4fa13c1f9bde53dea291fea6515b0830ee336141"
    ),
}
AUDIT_AUTHORS = {
    "audit_f44_cosine_stage_c_v1.py": (
        "548d444fdd61e97a7d249bcb2e271ae1489617d065d125114f2e1ec6d62a2167"
    ),
    "A14_F44_COSINE_STAGE_C_INDEPENDENT_AUDIT_PREFLIGHT_V1.md": (
        "d37ca22d3595823fb53787d54613293ebab86b9ba406f3c72a6b0f293e7ef5c2"
    ),
    "a14_f44_cosine_stage_c_independent_audit_preflight_v1.json": (
        "abafdfd42a1f4fa0d2f26926b42fc5142adee9740e6d2df2292a3a36f608185d"
    ),
}
INTERPRETER_PINS = {
    str(LAUNCHER): "41123879d2e991377997acadf5f0cf8f34fa10d86362eded8c69b6041e2893b5",
    "C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312\\python.exe": (
        "fd5c46d73d29ba21b04c844bbaf9096066136526911230645a2a040d23fb612b"
    ),
}
HISTORICAL_CACHE_RELEASES = (
    (
        ".context/A14_TAYLOR_F44_STAGE_K_ROOT_READY_run001.json",
        "ce6e00b8cb2f53e05383d14e20e003e36207cd65096b232bb47df157782df3ba",
        ("experiment_taylor_f44_stage_k.py", "taylor_f44_stage_k_source.py"),
    ),
    (
        ".context/A14_TAYLOR_F44_STAGE_K_AUDIT_ROOT_READY_run001.json",
        "67bf1f1a944f8aafd94f5eafdd418210ff053bf84a3586fd5c2b85c4b67a304a",
        ("audit_taylor_f44_stage_k.py",),
    ),
    (
        ".context/A14_TAYLOR_F44_STAGE_K_INTEGRITY_ROOT_READY_run001.json",
        "6d873e903c3f6e85ef488c8a9c2d4f635370a0af3191f3c65cc66537617f19c9",
        ("verify_taylor_f44_stage_k_root_v1.py",),
    ),
)
_FROZEN, _EXTERNAL, _OBSERVED = {}, {}, {}
_PATH_CACHE, _HASH_CACHE = {}, {}
_OWN_INVENTORIES, _ABSENT_RUNTIME = {}, set()
_CODE_CACHE_EXPECTED = {}
_BASE_SCOPE, _EXCLUDED_SCOPE = None, None
_STANDARD_RUNTIME_MEMBERS = set()
_HASH_WORK = _REFERENCES = 0
_STARTED = None
_PACKAGE_TREES = (
    ROOT / ".context/frontier_t0_env/Lib/site-packages/mpmath",
    ROOT / ".context/frontier_t0_env/Lib/site-packages/mpmath-1.3.0.dist-info",
)

BUILDER = RESEARCH / "f44_cosine_stage_c_source.py"

BUILDER_SHA = "6aa28c87416e30558e459efe2c602866dcc9b2d76e236e93faae05fe65826a74"

BUILDER_NOTE = RESEARCH / "F44_STAGE_C_BUILDER_INTERFACE_AUTHOR_V1.md"

BUILDER_NOTE_SHA = "b737562b5bafdc271d5c08cf4fa13c1f9bde53dea291fea6515b0830ee336141"

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


FINAL_ROOT_NAME = "A14_taylor_f44_stage_C_root_verification_run001"
FINAL_ROOT_SHA = "18da7c127f649014945cd4a3cc07360053a6394ac48f70851a40d786850a618d"
FINAL_ROOT_COUNTS = [8, 916, 2842]
FINAL_ROOT_READY = ROOT / ".context/A14_F44_COSINE_STAGE_C_INTEGRITY_ROOT_READY_run001.json"
FINAL_ROOT_READY_SHA = "2b50451df6f1b948b51bf3d337c574d96e95c1981cd53930fdd88c49f48e4029"
FINAL_ROOT_AUTHORS = {
    "verify_f44_cosine_stage_c_root_v1.py": (
        "3cc9b714b9a3adcb7a32e20dc38a215276361faa7a721c5d4d87ac0feabc76ae"
    ),
    "F44_COSINE_STAGE_C_ROOT_INTEGRITY_PREFLIGHT_V1.md": (
        "66806ac48df395058ec99f6455f5d235400b7479b7ba9642315fdfaa55cf49c3"
    ),
    "f44_cosine_stage_c_root_integrity_preflight_v1.json": (
        "ead3ed99d8a15673c01b191a0fe0db4938005b5993524dcc094e947dffccf810"
    ),
}
OWNERS[FINAL_ROOT_NAME] = [FINAL_ROOT_SHA, FINAL_ROOT_COUNTS]
GRID_HELPER = RESEARCH / "f44_cosine_caller_grid_axis_source_v1.py"
GRID_MODULE = "_f44_caller_grid_axis_builder_v1"
GRID_ROW_ID = "TAYLOR_D6_S64_W72_F44_TO_F40_MUL52x38_CALLER_GRID_NO_AXIS"
GRID_CONTRACT_ID = "Q32_MIDPOINT_MOD256_128_M_OR_WRAP3Q4"
MAX_NATIVE_ROWS = 2000000
NATIVE_SOURCE = PROGRAM / "A14_taylor_f44_stage_K_run001"
PRIMARY = SOURCE
_SCIENCE_ADMITTED = False
_OUTPUT_NATIVE_EXPECTED = {}
GRID_DESIGN_PINS = {
    ".context/F44_STAGE_C_CALLER_GRID_AXIS_REMOVAL_DESIGN_run001.md": (
        "49ffa09b50230de03e97e98922ebe6a16cdf5f427136dc04156ceff494482c65"
    ),
    ".context/F44_STAGE_C_CALLER_GRID_AXIS_REMOVAL_DESIGN_run001.json": (
        "aa7c8a986de52be213054481f5e46a2f36aa60c418117101828aafbfef57d0cc"
    ),
    ".context/F44_STAGE_C_CALLER_GRID_AXIS_REMOVAL_INDEPENDENT_STATIC_PEER_run001.json": (
        "3290f0a883512b4932fbc8ec8092d1c1c4b8df69a0e463d47d89e9622ffab423"
    ),
}


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
    guard_serialization_integers(result)
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
    prior_failure_witnesses()
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
    target = OUTPUT / name
    require(target.parent == OUTPUT and not target.exists(), "Exclusive metadata output")
    guard_serialization_integers(value)
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
        and historical_V2["limits_CPU_admission_wall"] == [300, 270, 900]
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


def component_scope(record, schema):
    require(
        record["schema"] == schema
        and record["passed"] is True
        and record["completed"] is True
        and record["budget_censored"] is False
        and record["limits_CPU_admission_wall"] == [300, 270, 900],
        "Actual uncensored fixed component process; no new science",
    )
    for key in (
        "full_G2",
        "adoption",
        "cost_transfer",
        "quantum_advantage",
        "global_financial_gate_emission_authorized",
    ):
        require(record[key] is False, "Original component does not authorize financial promotion")
    for key in ("new_test_credit", "new_credited_gate_replays", "new_price_samples"):
        require(type(record[key]) is int and record[key] == 0, "No fixture or price credit")
    require(
        record["original_scientific_receipts_unchanged"] is True
        and record["previous_A14_rejected_rows_unchanged"] is True,
        "Original scope remains explicit",
    )


def reconcile_metadata():
    source_summary, source_outcome = (
        read(SOURCE / "summary.json"),
        read(SOURCE / "completion_outcome.json"),
    )
    audit_summary, audit_outcome = (
        read(AUDIT / "summary.json"),
        read(AUDIT / "completion_outcome.json"),
    )
    for record in (source_summary, source_outcome):
        component_scope(record, "a14-f44-stage-c-primary90-summary-v3")
        require(
            record["primary_digits"] == 90
            and record["coefficient_count"] == 448
            and record["center_count"] == 64
            and record["actual_native_replay_counts"] == [64, 16]
            and record["actual_prototype_completed"] is True,
            "Same completed primary90 component scope",
        )
    for record in (audit_summary, audit_outcome):
        component_scope(record, "a14-f44-stage-c-independent130-summary-v1")
        require(
            record["producer_manifest_SHA256"] == SOURCE_SHA
            and record["producer_complete_counts"] == SOURCE_COUNTS
            and record["independent_digits"] == 130
            and record["logical_forward_reverse_checks"] == [64, 16]
            and record["physical_forward_reverse_sweeps"] == [2, 2]
            and record["all448_true_coefficients_and64_centers_authorized"] is True
            and record["all64_uniform_and_native_segments_independently_authorized"] is True
            and record["complete_saved_array_structure_absolute_phase_and_resources_audited"]
            is True
            and record["resource_gate_passed"] is False
            and record["component_candidate_eligible"] is False
            and record["row_status"] == "REJECTED",
            "Exact saved independent130 authorization and rejection",
        )
    require(
        source_outcome["failed"] is False and audit_outcome["failed"] is False,
        "Both authoritative successful outcomes",
    )
    row = read(SOURCE / "fixed_frontier_row.json")
    require(
        source_summary["row"] == source_outcome["row"] == row
        and row["row_id"] == ROW_ID
        and row["status"] == "REJECTED"
        and row["resource_gate_passed"] is False
        and row["candidate_eligible"] is False
        and row["native_rows"] == 436366
        and row["native_qubits"] == 10364,
        "Unchanged actual source resource rejection",
    )
    binding = read(SOURCE / "original_source_binding.json")
    own_binding = read(AUDIT / "independent_source_binding_audit.json")
    require(
        own_binding["passed"] is True and own_binding["complete_source_binding"] == binding,
        "Full saved original source-binding metadata agrees",
    )
    literals, own_literals = (
        read(SOURCE / "primary90_literals.json"),
        read(AUDIT / "independent130_literal_audit.json"),
    )
    require(
        literals["coefficient_count"] == own_literals["coefficient_count"] == 448
        and literals["center_count"] == own_literals["center_count"] == 64
        and literals["table_literal_count"] == 512
        and own_literals["passed"] is True
        and own_literals["digits"] == 130
        and own_literals["oracle_bits"] == 512
        and own_literals["Machin_terms"] == 200
        and own_literals["trig_terms"] == 224
        and own_literals["fixed_words_unchanged"] is True
        and len(literals["table"]) == 64
        and all(len(bank) == 8 for bank in literals["table"]),
        "Literal inventory metadata only; exact oracle pairs remain opaque",
    )
    require(
        len(literals["coefficient_rows"]) == len(own_literals["rows"]) == 448
        and len(literals["center_rows"]) == 64,
        "Every saved coefficient and center record",
    )
    for primary, independent in zip(
        literals["coefficient_rows"], own_literals["rows"], strict=True
    ):
        budget()
        require(
            [primary[key] for key in ("segment", "degree", "raw")]
            == [independent[key] for key in ("segment", "degree", "raw")]
            and independent["all_containment_half_ULP_checks_passed"] is True,
            "Every saved literal identity and prior authorized status agrees; "
            "no interval evaluation",
        )
    native, own_native = (
        read(SOURCE / "all64_native_certificate.json"),
        read(AUDIT / "independent_native_audit.json"),
    )
    require(
        native["all64_native_promises_passed"] is True
        and own_native["passed"] is True
        and native["segment_rows"] == own_native["segment_rows"]
        and len(native["segment_rows"]) == 64,
        "All64 saved native records equal; no recurrence evaluation",
    )
    uniform, own_uniform = (
        read(SOURCE / "uniform_certificate.json"),
        read(AUDIT / "independent_uniform_audit.json"),
    )
    require(
        uniform["uniform_component_gate_passed"] is True
        and own_uniform["passed"] is True
        and own_uniform["all64_closed_segments"] is True
        and len(own_uniform["rows"]) == 64
        and uniform["original_E_old"] == own_uniform["original_E_old"]
        and own_uniform["no_financial_allowance_transfer"] is True,
        "Saved uniform scope and original allowance identity; no bound arithmetic",
    )
    resources, own_resources = (
        read(SOURCE / "actual_prototype_resources.json"),
        read(AUDIT / "independent_actual_resources.json"),
    )
    cost, own_cost = (
        read(SOURCE / "whole_source_resource_comparison.json"),
        read(AUDIT / "independent_whole_source_cost_audit.json"),
    )
    require(
        resources == own_resources
        and cost["actual_clean_prototype_resource"] == resources
        and own_cost["passed"] is True
        and cost["cases"] == own_cost["cases"]
        and cost["matched_serial_clean_function_resource"]
        == own_cost["matched_serial_clean_function_resource"]
        and cost["all_resource_gates_passed"] is own_cost["all_resource_gates_passed"] is False
        and own_cost["actual_capped_changed_financial_schedule_realized"] is False,
        "Exact saved ASAP/serial and complete-source cost agreement; no resource recount",
    )
    array, gates = (
        read(SOURCE / "native_gate_array.json"),
        read(AUDIT / "independent_gate_array_audit.json"),
    )
    require(
        array["rows"] == gates["all_actual_rows_consumed"] == 436366
        and gates["all_actual_allocations_consumed"] == 10364
        and array["gate_SHA256"]
        == _FROZEN[(SOURCE / array["gate_file"]).relative_to(ROOT).as_posix()]
        and gates["actual_global_inverse_checked_row_for_row"] is True
        and gates["universal_full72_clean_XOR_conditional"] is True
        and gates["builder_or_MatchingCircuit_called"] is False,
        "Saved array consumer metadata and exact binary pin; bytes only hashed here",
    )
    phase = read(AUDIT / "independent_absolute_phase_audit.json")
    require(
        phase["exact_absolute_phase_CCX"] is True
        and phase["relative_or_unknown_global_phase_accepted"] is False,
        "Prior exact phase audit retained; no phase calculation",
    )
    diagnostics, own_diagnostics = (
        read(SOURCE / "fixed_native_diagnostics.json"),
        read(AUDIT / "independent_bit_sliced_diagnostics.json"),
    )
    require(
        diagnostics["full_map_case_count"] == own_diagnostics["full_map_case_count"] == 32
        and diagnostics["standalone_round_tie_case_count"]
        == own_diagnostics["standalone_round_tie_case_count"]
        == 8
        and diagnostics["whole_prototype_total_replays"]
        == own_diagnostics["logical_whole_prototype_total_replays"]
        == 64
        and diagnostics["standalone_round_leaf_total_replays"]
        == own_diagnostics["logical_standalone_round_total_replays"]
        == 16
        and own_diagnostics["entire_allocated_state_forward_and_reverse_compared"] is True
        and own_diagnostics["physical_prototype_sweeps"]
        == own_diagnostics["physical_ROUND_sweeps"]
        == 2
        and own_diagnostics["case_or_corpus_expansion"] is False,
        "Same saved fixed diagnostics; no replay or scalar oracle",
    )
    return dict(
        source_manifest_SHA256=SOURCE_SHA,
        audit_manifest_SHA256=ROOT_DECLARED_AUDIT_SHA,
        source_complete_counts=SOURCE_COUNTS,
        audit_complete_counts=AUDIT_COUNTS,
        saved_source_binding_literals_native_uniform_scope_agrees=True,
        saved_actual_ASAP_serial_and_whole_source_resource_metadata_equal=True,
        saved_phase_and_fixed_diagnostic_metadata_reconciled=True,
        universal_helper_proof_remains_conditional_on_original_full72_leaf_and_all64_range_premises=True,
        source_public_Q_endpoint_map_not_original_equivalence=True,
        **flags(),
    )


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
        read(NATIVE_SOURCE / "primitive_descriptors.json"),
        read(NATIVE_SOURCE / "native_gate_arrays.json"),
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
        path = canonical(NATIVE_SOURCE / record["gate_file"])
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


def grid_bind_internal_roles(internal, expressions):
    expected = grid_expected_roles()
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


def grid_gate_binding(words, descriptor, table, leaves):
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
        descriptor["schema"] == "f44-caller-grid-no-axis-clean-prototype-v1"
        and descriptor["row_id"] == GRID_ROW_ID,
        "One fixed saved clean cosine descriptor",
    )
    require(
        descriptor["caller_grid_contract_id"] == GRID_CONTRACT_ID
        and descriptor["certificate_scope"] == "PROMISED_CALLER_GRID_ONLY"
        and descriptor["axis_tail_omitted"] is True
        and descriptor["generic_full72_equivalence_claimed"] is False
        and descriptor["actual_coherent32_preparation_array_audited"] is False,
        "Only separately pinned caller-grid certificate, no generic72 or prepared array claim",
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
    grid_bind_internal_roles(descriptor["internal"], expressions)
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
        and expressions[tuple(result_bank)] == grid_expected_expression(),
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
        "caller_grid_full72_interface_clean_XOR_conditional": True,
        "required_external_premises": [
            "Independent BK72 ADD/SUB full72 clean-map certificates",
            "Independent K signed52x38 MUL and full72 ROUND certificates",
            "Independent all64 eager caller signed/no-wrap/address/low-bit proofs",
            "Prepared Q32 grid at full72 component input; a future whole-source "
            "40-active/32-zero argument bridge must be emitted and audited separately",
        ],
        "program_fixture_credit": 0,
        "financial_G2_or_adoption": False,
    }


def grid_slice_initial(qubits, cases):
    require(
        type(qubits) is int and 144 <= qubits <= 16384 and len(cases) == 128,
        "Fixed finite bit-slice lanes",
    )
    state = [0] * qubits
    for lane, (value, dirty) in enumerate(cases):
        budget()
        for bit in range(72):
            state[bit] |= ((value >> bit) & 1) << lane
            state[72 + bit] |= ((dirty >> bit) & 1) << lane
    return state


def grid_bit_sweep(words, state, lane_count, inverse=False):
    budget()
    require(
        len(words) % 4 == 0
        and 0 < len(words) // 4 <= 2000000
        and 144 <= len(state) <= 16384
        and lane_count == 128
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


def flags():
    return dict(
        caller_typed_component_only=True,
        caller_grid_entry_promise_required=True,
        actual_coherent32_preparation_array_audited=False,
        whole_source_40_active_to72_zero_padded_bridge_audited=False,
        generic_full72_map_equivalence_claimed=False,
        whole_financial_source_emitted=False,
        new_test_credit=0,
        new_credited_gate_replays=0,
        new_price_samples=0,
        full_G2=False,
        adoption=False,
        cost_transfer=False,
        quantum_advantage=False,
        global_financial_gate_emission_authorized=False,
        original_scientific_receipts_unchanged=True,
        previous_A14_rejected_rows_unchanged=True,
        generic_StageC_resource_gate_passed=False,
        generic_StageC_row_status="REJECTED",
        new_QROM_release_authorized=False,
        whole_source_capped_depth_transfer=False,
    )


def loaded_origins():
    forbidden = {"mpmath", "numpy", "scipy", "numba", "sympy", "gmpy", "gmpy2", "sage", "pytest"}
    require(
        not any(name.split(".", 1)[0] in forbidden for name in sys.modules),
        "Stdlib-only component; no numerical package or historical scientific imports",
    )
    require(
        not any(
            name.startswith("research.")
            and name not in {__name__, "research.limitation_program_20261001"}
            for name in sys.modules
        ),
        "No imported historical builder/producer/auditor",
    )
    if GRID_MODULE in sys.modules:
        require(_SCIENCE_ADMITTED, "New helper only after full admission")
        require(
            canonical(sys.modules[GRID_MODULE].__file__) == GRID_HELPER,
            "Only new externally pinned helper origin",
        )
    for module in tuple(sys.modules.values()):
        budget()
        for attribute in ("__file__", "__cached__"):
            origin = getattr(module, attribute, None)
            if not origin:
                continue
            lexical = Path(os.path.abspath(str(origin)))
            require(
                not lexical.is_relative_to(_EXCLUDED_SCOPE[0])
                and not lexical.resolve(strict=False).is_relative_to(_EXCLUDED_SCOPE[1]),
                "No excluded runtime origin or cache",
            )
            if lexical.is_file():
                actual = canonical(lexical)
                if actual.is_relative_to(RESEARCH):
                    require(
                        actual in {AUTHOR, GRID_HELPER} or actual in _CODE_CACHE_EXPECTED,
                        "Historical scientific sources are reference bytes only",
                    )
                key = key_for(actual)
                mapping = _FROZEN if actual.is_relative_to(ROOT) else _EXTERNAL
                if key not in mapping:
                    require(
                        actual == AUTHOR or not actual.is_relative_to(RESEARCH),
                        "Only startup main source may precede its external READY pin",
                    )
                    add(actual, digest(actual))
                else:
                    require(digest(actual) == mapping[key], "Loaded bytes equal frozen expectation")


def admission(ready_sha):
    ready = read(bind(READY, ready_sha))
    require(
        ready["schema"] == "root-f44-caller-grid-axis-READY-v1"
        and ready["ready"] is True
        and ready["root_and_independent_static_reviews_passed"] is True,
        "Separate ROOT scientific component release required",
    )
    require(
        ready["output"] == OUTPUT.relative_to(ROOT).as_posix()
        and ready["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
        and ready["completed_owner_manifest_SHA256"]
        == {name: item[0] for name, item in OWNERS.items()}
        and ready["completed_owner_complete_counts"]
        == {name: item[1] for name, item in OWNERS.items()},
        "All eight externally fixed complete owners; exact fresh route and StageC caps",
    )
    require(
        ready["caller_typed_native_component_execution_authorized"] is True
        and ready["caller_grid_entry_promise_required"] is True
        and ready["actual_coherent32_preparation_array_audited"] is False
        and ready["financial_adoption"] is False
        and ready["fixture_credit"] == 0,
        "Only conditional prepared-grid component, no whole-source or generic72 release",
    )
    own = ready["author_method_SHA256"]
    require(
        set(own) == {AUTHOR.name, GRID_HELPER.name, METHOD_DOC.name, PREFLIGHT.name},
        "Exactly four separately frozen new authors",
    )
    for name, expected in own.items():
        bind(RESEARCH / name, expected)
    policy = read(PREFLIGHT)
    require(
        policy["schema"] == "f44-caller-grid-axis-preflight-v1"
        and policy["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
        and policy["owned_caps_files_bytes"] == [MAX_OWN_FILES, MAX_OWN_BYTES]
        and policy["runtime_caps_files_bytes"] == [MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES]
        and policy["bookkeeping_reference_unique_bytes_hash_work_caps"]
        == [MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK]
        and policy["completed_owner_manifest_SHA256"] == ready["completed_owner_manifest_SHA256"]
        and policy["completed_owner_complete_counts"] == ready["completed_owner_complete_counts"]
        and policy["integer_decimal_digit_limit"] == INTEGER_DECIMAL_DIGITS
        and policy["integer_serialization_bit_cap"] == INTEGER_SERIALIZATION_BITS
        and policy["author_SHA256"] == own[AUTHOR.name]
        and policy["helper_SHA256"] == own[GRID_HELPER.name]
        and policy["method_SHA256"] == own[METHOD_DOC.name]
        and policy["grid_input_cases_dirty_patterns_logical_lanes"] == [64, 2, 128]
        and policy["physical_whole_array_sweeps"] == 2
        and policy["whole_source_capped_depth_transfer"] is False,
        "Exact fixed component scope and bounded representation",
    )
    require(
        ready["interpreter_expected_SHA256"] == INTERPRETER_PINS, "Both original fixed interpreters"
    )
    manifests = {name: packet(name, pin, counts) for name, (pin, counts) in OWNERS.items()}
    for name in (SOURCE_NAME, AUDIT_NAME):
        component_scope(
            manifests[name],
            "a14-f44-stage-c-primary90-manifest-v3"
            if name == SOURCE_NAME
            else "a14-f44-stage-c-independent130-manifest-v1",
        )
    require(
        manifests[AUDIT_NAME]["producer_manifest_SHA256"] == SOURCE_SHA
        and manifests[AUDIT_NAME]["producer_complete_counts"] == SOURCE_COUNTS
        and manifests[AUDIT_NAME]["row_status"] == "REJECTED",
        "Same completed generic Stage C resource rejection",
    )
    final = manifests[FINAL_ROOT_NAME]
    require(
        final["schema"] == "a14-f44-stage-c-root-integrity-manifest-v1"
        and final["source_manifest_SHA256"] == SOURCE_SHA
        and final["audit_manifest_SHA256"] == ROOT_DECLARED_AUDIT_SHA
        and final["completed_owner_manifest_SHA256"]
        == {name: item[0] for name, item in OWNERS.items() if name != FINAL_ROOT_NAME}
        and final["completed_owner_complete_counts"]
        == {name: item[1] for name, item in OWNERS.items() if name != FINAL_ROOT_NAME},
        "Original final ROOT whole-map integrity scope, not new array approval",
    )
    source_ready = read(bind(SOURCE_READY, SOURCE_READY_SHA))
    audit_ready = read(bind(AUDIT_READY, AUDIT_READY_SHA))
    final_ready = read(bind(FINAL_ROOT_READY, FINAL_ROOT_READY_SHA))
    require(
        source_ready["schema"] == "root-a14-f44-cosine-stage-c-READY-v3"
        and source_ready["author_method_SHA256"] == SOURCE_AUTHORS
        and source_ready["output"] == SOURCE.relative_to(ROOT).as_posix(),
        "Immutable generic producer release",
    )
    require(
        audit_ready["schema"] == "root-a14-f44-cosine-stage-c-audit-READY-v1"
        and audit_ready["author_method_SHA256"] == AUDIT_AUTHORS
        and audit_ready["producer_manifest_SHA256"] == SOURCE_SHA
        and audit_ready["producer_complete_counts"] == SOURCE_COUNTS
        and audit_ready["output"] == AUDIT.relative_to(ROOT).as_posix(),
        "Immutable independent130 release",
    )
    require(
        final_ready["schema"] == "root-a14-f44-stage-c-integrity-READY-v1"
        and final_ready["author_method_SHA256"] == FINAL_ROOT_AUTHORS
        and final_ready["limits_CPU_admission_wall"] == [180, 150, 600]
        and final_ready["output"] == (PROGRAM / FINAL_ROOT_NAME).relative_to(ROOT).as_posix(),
        "Exact historical ROOT release; its caps are not the new scientific caps",
    )
    originals = {
        name: item[0]
        for name, item in OWNERS.items()
        if name not in (SOURCE_NAME, AUDIT_NAME, FINAL_ROOT_NAME)
    }
    original_counts = {
        name: item[1]
        for name, item in OWNERS.items()
        if name not in (SOURCE_NAME, AUDIT_NAME, FINAL_ROOT_NAME)
    }
    for release in (source_ready, audit_ready):
        require(
            release["completed_prerequisite_manifest_SHA256"] == originals
            and release["completed_prerequisite_complete_counts"] == original_counts,
            "All original five native/numerical premise owners retained",
        )
    for authors in (SOURCE_AUTHORS, AUDIT_AUTHORS, FINAL_ROOT_AUTHORS):
        for name, expected in authors.items():
            bind(RESEARCH / name, expected)
    for release, sources in (
        (source_ready, [RESEARCH / "experiment_f44_cosine_stage_c_v3.py", BUILDER]),
        (audit_ready, [RESEARCH / "audit_f44_cosine_stage_c_v1.py"]),
        (final_ready, [RESEARCH / "verify_f44_cosine_stage_c_root_v1.py"]),
    ):
        code_caches(
            sources,
            release["existing_new_code_cache_SHA256"],
            release["absent_new_code_cache_paths"],
        )
    for key, pin, sources in HISTORICAL_CACHE_RELEASES:
        release = read(bind(ROOT / key, pin))
        code_caches(
            [RESEARCH / name for name in sources],
            release["existing_new_code_cache_SHA256"],
            release["absent_new_code_cache_paths"],
        )
    code_caches(
        [AUTHOR, GRID_HELPER],
        ready["existing_new_code_cache_SHA256"],
        ready["absent_new_code_cache_paths"],
    )
    admit_prior_failure(ready, policy)
    bind(ACTUAL_AUDIT_ROOT, ACTUAL_AUDIT_ROOT_SHA)
    for key, expected in GRID_DESIGN_PINS.items():
        bind(ROOT / key, expected)
    require(
        policy["grid_design_expected_SHA256"] == GRID_DESIGN_PINS,
        "Same peer-reviewed conditional grid design",
    )
    design = read(ROOT / ".context/F44_STAGE_C_CALLER_GRID_AXIS_REMOVAL_DESIGN_run001.json")
    legacy_path = ROOT / design["original_evidence"]["A10_original_flat_manifest"]["path"]
    require(
        _FROZEN[key_for(legacy_path)]
        == design["original_evidence"]["A10_original_flat_manifest"]["SHA256"],
        "Original A10 flat manifest remains an admitted provenance reference",
    )
    legacy = read(legacy_path)
    directory = ROOT / design["original_evidence"]["original_executed_code_directory"]
    for name, expected in design["original_evidence"][
        "original_executed_code_owned_SHA256"
    ].items():
        require(
            legacy["executed_code\\" + name] == expected,
            "Selected historical ABI text has original manifest membership",
        )
        bind(directory / name, expected)
    for key, expected in ready["static_review_expected_SHA256"].items():
        require(
            key.startswith(".context/") and ".." not in Path(key).parts, "ROOT-local static review"
        )
        bind(ROOT / key, expected)
    return ready, policy


def independent_input_bytes(path):
    global _HASH_WORK
    budget()
    actual = canonical(path)
    key = key_for(actual)
    expected = _FROZEN.get(key) if actual.is_relative_to(ROOT) else _EXTERNAL.get(key)
    if actual.is_relative_to(OUTPUT):
        require(
            actual == OUTPUT / "cosine.gates.bin",
            "Only current owned complete native array may be interpreted",
        )
        expected = _OUTPUT_NATIVE_EXPECTED.get(actual)
    require(
        expected is not None and digest(actual) == expected,
        "Admitted original or own full native bytes",
    )
    before = fingerprint(actual)
    require(0 < before[2] <= MAX_OWN_BYTES, "Bounded native or original text input")
    parts, total = [], 0
    with actual.open("rb") as stream:
        while block := stream.read(65536):
            budget()
            total += len(block)
            _HASH_WORK += len(block)
            require(
                total <= before[2] and _HASH_WORK <= MAX_HASH_WORK,
                "All interpretation read bytes charged",
            )
            parts.append(block)
    result = b"".join(parts)
    require(
        total == before[2]
        and fingerprint(actual) == before
        and hashlib.sha256(result).hexdigest() == expected,
        "Stable whole admitted native input",
    )
    return result


def helper_text_delta_guard():
    old = ast.parse(independent_input_bytes(BUILDER))
    new = ast.parse(independent_input_bytes(GRID_HELPER))
    names = ("require", "Circuit", "leaf_size", "Prototype", "helper_compute")
    for name in names:
        before = next(
            n for n in old.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == name
        )
        after = next(
            n for n in new.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == name
        )
        require(
            ast.dump(before, include_attributes=False) == ast.dump(after, include_attributes=False),
            "Every retained emitter/primitive/helper definition exact original AST",
        )
    function = next(
        n
        for n in new.body
        if isinstance(n, ast.FunctionDef) and n.name == "build_caller_grid_cosine"
    )
    require(
        not any(
            isinstance(n, ast.For)
            and isinstance(n.target, ast.Tuple)
            and [x.id for x in n.target.elts if isinstance(x, ast.Name)] == ["turn", "exact"]
            for n in ast.walk(function)
        ),
        "Only axis override loop omitted in new named builder",
    )
    return {
        "retained_definition_AST_exact": list(names),
        "new_helper_expected_SHA256": _FROZEN[key_for(GRID_HELPER)],
        "scientific_functions_evaluated_by_text_guard": False,
    }


def caller_binding_inventory():
    binding = read(SOURCE / "original_source_binding.json")
    records = {}
    for case, expected in (("B4x12", (30, 60)), ("B8x52", (234, 468))):
        budget(admission=True)
        saved = binding["cases"][case]
        target, source, schedule = (
            read(ROOT / saved[k]) for k in ("target_path", "source_path", "schedule_path")
        )
        require(
            target["width"] == source["word_width"] == 72
            and target["fraction_bits"] == source["fraction_bits"] == 40,
            "Same full72 original native target",
        )
        require(
            schedule["format"] == "compact-clean-xor-capped-wave-schedule-v7"
            and schedule["input_contract"]
            == "Nonnegative raw bit patterns within each declared input bit width",
            "Explicit original preparation contract, not a variable-name inference",
        )
        require(
            len(target["nodes"]) <= 100000 and len(source["forward_calls"]) <= 100000,
            "Bounded complete original structural inventory",
        )
        locations = {value: node for node in target["nodes"] for value in node["out"]}
        calls = {value: call for call in source["forward_calls"] for value in call["out"]}
        inputs = [node for node in target["nodes"] if node["op"] == "input"]
        require(
            source["inputs"] == inputs and len(inputs) == expected[1],
            "All original input allocations and pair roles",
        )
        noninputs = [node for node in target["nodes"] if node["op"] != "input"]
        require(len(noninputs) == len(source["forward_calls"]), "Every original call retained")
        for index, (node, call) in enumerate(zip(noninputs, source["forward_calls"], strict=True)):
            if index % 128 == 0:
                budget(admission=True)
            require(
                node["args"] == call["args"] and node["out"] == call["out"],
                "Whole actual ordered call/SSA mapping",
            )
        arguments = []
        require(len(saved["pair_scopes"]) == expected[0], "Every complete original joint pair")
        for index, pair in enumerate(saved["pair_scopes"]):
            budget(admission=True)
            raw_u, raw_v = pair["raw_uniform_values"]
            require(
                pair["raw_uniform_values"]
                == [inputs[2 * index]["out"][0], inputs[2 * index + 1]["out"][0]],
                "Complete ordered prepared q32 input pairing",
            )
            for raw in (raw_u, raw_v):
                node = locations[raw]
                require(
                    node["op"] == "input"
                    and node["params"]["bits"] == 32
                    and node["params"]["preparation"] == "uniform"
                    and schedule["widths"][raw] == 32,
                    "Native retained32 preparation promise and zero-padding obligation",
                )
            midpoint, wrapped = [item["input"] for item in pair["cosines"]]
            arguments.extend((midpoint, wrapped))
            node = locations[midpoint]
            shifts = [value for value in node["args"] if locations[value]["op"] == "bits"]
            constants = [value for value in node["args"] if locations[value]["op"] == "const"]
            require(
                node["op"] == "add" and len(shifts) == len(constants) == 1,
                "Exact original midpoint chain",
            )
            shift = locations[shifts[0]]
            require(
                shift["args"] == [raw_v]
                and shift["params"] == {"shift": -8, "width": 72, "signed": False}
                and locations[constants[0]]["params"] == {"value": 128},
                "Unsigned raw32 left8 plus literal midpoint128",
            )
            wrap = locations[wrapped]
            require(
                wrap["op"] == "bits"
                and wrap["params"] == {"shift": 0, "width": 40, "signed": False}
                and len(wrap["args"]) == 1,
                "Original sole low40 wrap",
            )
            summed = locations[wrap["args"][0]]
            other = [value for value in summed["args"] if value != midpoint]
            require(
                summed["op"] == "add"
                and midpoint in summed["args"]
                and len(other) == 1
                and locations[other[0]]["op"] == "const"
                and locations[other[0]]["params"] == {"value": 824633720832},
                "Same midpoint plus exact3Qquarter; no independent sine draw",
            )
            require(
                schedule["widths"][midpoint] == schedule["widths"][wrapped] == 40
                and schedule["widths"][wrap["args"][0]] == 41,
                "Original native m/sum/w storage obligations unchanged",
            )
            for value in (shifts[0], constants[0], midpoint, other[0], wrap["args"][0], wrapped):
                node, call = locations[value], calls[value]
                require(
                    node["args"] == call["args"]
                    and node["out"] == call["out"]
                    and call["argument_copy_cx"] == {0: 0, 1: 144, 2: 288}[len(node["args"])],
                    "Every original conversion call/copy record unchanged",
                )
        require(
            arguments == saved["cosine_argument_values"] and len(arguments) == expected[1],
            "All original cosine m/w callers bound",
        )
        records[case] = {
            "all_joint_pairs": expected[0],
            "all_cosine_callers": expected[1],
            "full_actual_caller_ABI_joined": True,
            "all_argument_ancestors_and_original_storage_retained": True,
        }
    return {
        "cases": records,
        "caller_grid_contract_id": GRID_CONTRACT_ID,
        "entry_promise_required": True,
        "actual_coherent32_preparation_array_audited": False,
        "symbolic_grid": "256*n+128 with0<=n<2^32; wrapped branch is a permutation",
        "axis_equalities_constant_false_on_prepared_grid": True,
        **flags(),
    }


def grid_expected_roles():
    roles = c130_expected_roles()
    roles["axes"] = []
    roles["final"] = roles["projected"]
    return roles


def grid_expected_expression():
    return grid_expected_roles()["final"]


def grid_fixed_inputs():
    # Exactly64 input values fixed before emission. No tests or calculations run on import.
    values = []
    for segment in range(64):
        if segment in (0, 16, 32, 48):
            value = segment * (1 << 34) + 128
        elif segment in (15, 31, 47, 63):
            value = (segment + 1) * (1 << 34) - 128
        else:
            value = segment * (1 << 34) + (1 << 33) + 128
        require(
            128 <= value <= (1 << 40) - 128 and value % 256 == 128 and value >> 34 == segment,
            "Every fixed case belongs to the full prepared grid and exact designated segment",
        )
        values.append(value)
    require(len(values) == len(set(values)) == 64, "Exactly64 distinct complete-grid inputs")
    return tuple(values)


def grid_fixed_diagnostics(words, descriptor, table):
    values, mask = grid_fixed_inputs(), (1 << 72) - 1
    cases = [(value, dirty) for value in values for dirty in (0, mask)]
    require(len(cases) == 128, "Exactly64 complete-grid inputs times two full72 dirty patterns")
    initial = grid_slice_initial(descriptor["qubits"], cases)
    current = list(initial)
    expected = [c130_integer_reference(value, table) for value, _ in cases]
    grid_bit_sweep(words, current, 128)
    c130_compare_slices(current, initial, expected, 128)
    grid_bit_sweep(words, current, 128, inverse=True)
    require(current == initial, "Every allocated wire restores for all128 actual reverse lanes")
    return {
        "input_case_count": 64,
        "dirty_patterns": [0, mask],
        "logical_forward_calls": 128,
        "logical_reverse_calls": 128,
        "physical_whole_array_sweeps": 2,
        "logical_case_count": 128,
        "inputs": list(values),
        "full72_input_dirty_output_private_and_SSA_forward_reverse_compared": True,
        "same_fixed_case_formula_no_adaptive_expansion": True,
        "producer_reference_or_generic_replay_called": False,
        "new_standalone_round_corpus": False,
        "program_fixture_credit": 0,
        **flags(),
    }


def actual_axis_only_array_delta(words, descriptor):
    original = read(SOURCE / "prototype_descriptor.json")
    record = read(SOURCE / "native_gate_array.json")
    require(
        len(original["internal"]["axes"]) == 5 and len(original["trace"]) >= 15,
        "Exact saved generic five-axis tail",
    )
    tail = original["trace"][-15:]
    require(
        [event["op"] for event in tail] == ["CONST", "EQ", "SELECT"] * 5,
        "All and only15 original axis events",
    )
    for axis, constant, equality, selected in zip(
        original["internal"]["axes"], tail[0::3], tail[1::3], tail[2::3], strict=True
    ):
        require(
            constant["params"] == {"raw": axis["turn"]}
            and constant["outs"] == [axis["point"]]
            and equality["args"] == [original["internal"]["clamped"], axis["point"]]
            and equality["outs"] == [axis["flag"]]
            and selected["args"][0] == axis["flag"]
            and selected["args"][2] == axis["before"]
            and selected["outs"] == [axis["after"]],
            "Complete saved EQ/SELECT axis roles, no unverified suffix",
        )
    retained_end = tail[0]["rows"][0]
    require(
        descriptor["trace"] == original["trace"][:-15]
        and descriptor["forward_rows"] == [0, retained_end]
        and descriptor["internal"]["axes"] == []
        and descriptor["internal"]["final"] == descriptor["internal"]["projected"],
        "Exactly same retained trace/allocations/operations with axis tail omitted",
    )
    for key in original["internal"]:
        if key not in {"axes", "final"}:
            require(
                descriptor["internal"][key] == original["internal"][key],
                "Every retained actual bank identity unchanged",
            )
    require(
        record["rows"] == original["gate_rows"]
        and record["row_format"] == "little-endian int32 Nx4 X/CX/CCX",
        "Externally pinned complete generic array",
    )
    generic = audit_native_payload(SOURCE / record["gate_file"], record["rows"], original["qubits"])
    for row in range(retained_end):
        if row % 128 == 0:
            budget()
        require(
            words[4 * row : 4 * row + 4] == generic[4 * row : 4 * row + 4],
            "Every retained actual forward row equals immutable generic prefix",
        )
    return {
        "all_retained_forward_rows_exact_saved_generic_prefix": True,
        "all_retained_trace_ports_and_allocations_exact": True,
        "omitted_axis_stages": 5,
        "only_axis_CONST_EQ_SELECT_suffix_removed": True,
        "no_second_emission_or_generic_array_replay": True,
        "generic_array_expected_SHA256": record["gate_SHA256"],
        "new_component_global_inverse_verified_separately_row_for_row": True,
        **flags(),
    }


def load_grid_helper():
    global _SCIENCE_ADMITTED
    require(
        not _SCIENCE_ADMITTED and GRID_MODULE not in sys.modules,
        "Only one new helper after complete admission",
    )
    check_code_caches()
    require(
        standard_runtime_members() == _STANDARD_RUNTIME_MEMBERS,
        "Complete current runtime before sole new scientific helper import",
    )
    loaded_origins()
    budget(admission=True)
    _SCIENCE_ADMITTED = True
    spec = importlib.util.spec_from_file_location(GRID_MODULE, GRID_HELPER)
    require(
        spec is not None and spec.loader is not None and canonical(spec.origin) == GRID_HELPER,
        "Exact admitted helper loader",
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[GRID_MODULE] = module
    spec.loader.exec_module(module)
    require(
        module.ROW_ID == GRID_ROW_ID
        and module.MACRO == C130_CCX_MACRO
        and module.MAX_ROWS == 2000000
        and module.MAX_QUBITS == 16384
        and module.REPLAY_GUARD_ROWS == 128,
        "Same paid absolute7T expansion and finite guards",
    )
    loaded_origins()
    check_code_caches()
    budget(admission=True)
    return module


def main():
    global _STARTED
    _STARTED = process_started()
    runtime_scopes()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ready-sha256", required=True)
    args = parser.parse_args()
    require(
        canonical(__file__) == AUTHOR and not OUTPUT.exists(), "One fresh typed component route"
    )
    try:
        require(
            sys.version_info[:3] == (3, 12, 4)
            and sys.byteorder == "little"
            and array("i").itemsize == 4,
            "Pinned Python3.12.4 int32 representation",
        )
        for spelling, expected in INTERPRETER_PINS.items():
            bind(Path(spelling), expected)
        fixed_integer_policy()
        runtime = own_runtime()
        ready, policy = admission(args.ready_sha256)
        loaded_origins()
        first = fresh_union()
        budget(admission=True)
        OUTPUT.mkdir(exist_ok=False)
        for path in (AUTHOR, GRID_HELPER, METHOD_DOC, PREFLIGHT, READY):
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
        retained = reconcile_metadata()
        save("retained_original_metadata_reconciliation.json", retained)
        save(
            "retained_original_whole_source_accounting.json",
            {
                "original_comparison": read(SOURCE / "whole_source_resource_comparison.json"),
                "original_independent_comparison": read(
                    AUDIT / "independent_whole_source_cost_audit.json"
                ),
                "all_original_argument_copy_inverse_storage_and_baseline_obligations_retained": True,  # noqa: E501 -- exact scope key
                "new_whole_source_comparator_or_capped_schedule_evaluated": False,
                **flags(),
            },
        )
        caller = caller_binding_inventory()
        save("caller_grid_binding.json", caller)
        save("helper_text_delta_guard.json", helper_text_delta_guard())
        table = read(SOURCE / "primary90_literals.json")["table"]
        leaves = audit_admitted_leaves(read(SOURCE / "original_source_binding.json"))
        builder = load_grid_helper()
        circuit, descriptor = builder.build_caller_grid_cosine(table, leaves, budget)
        save("prototype_descriptor.json", descriptor)
        record = save_gate_array(circuit)
        _OUTPUT_NATIVE_EXPECTED[canonical(OUTPUT / record["gate_file"])] = record["gate_SHA256"]
        save("native_gate_array.json", record)
        words = audit_native_payload(
            OUTPUT / record["gate_file"], descriptor["gate_rows"], descriptor["qubits"]
        )
        delta = actual_axis_only_array_delta(words, descriptor)
        save("actual_axis_only_array_delta.json", delta)
        structural = grid_gate_binding(words, descriptor, table, leaves)
        save("independent_whole_array_consumer.json", structural)
        phase = c130_ccx_absolute_phase()
        save("independent_absolute_phase_proof.json", phase)
        diagnostic = grid_fixed_diagnostics(words, descriptor, table)
        save("fixed_grid_diagnostics.json", diagnostic)
        resources = c130_resources(words, descriptor)
        save(
            "actual_component_resources.json",
            {
                "same_ASAP_and_complete_serial_event_accounting": resources,
                "outer_source_call_full72_copies_required_separately": True,
                "outer_call_copy_CX_per_forward_clean_invocation": 144,
                "whole_source_capped_depth_transfer": False,
                **flags(),
            },
        )
        loaded_origins()
        check_code_caches()
        second = fresh_union()
        summary = {
            "schema": "f44-caller-grid-axis-component-summary-v1",
            "completed": True,
            "passed": True,
            "budget_censored": False,
            "row_id": GRID_ROW_ID,
            "certificate_scope": "PROMISED_CALLER_GRID_ONLY",
            "input_case_count": 64,
            "logical_forward_reverse_calls": [128, 128],
            "physical_whole_array_sweeps": 2,
            "same_retained_generic_prefix_actual_rows_verified": True,
            "all_actual_rows_and_allocations_independently_consumed": True,
            "full72_dirty_XOR_input_and_zero_private_restoration": True,
            "literal_global_inverse_and_absolute7T_phase_verified": True,
            "completed_owner_manifest_SHA256": {name: item[0] for name, item in OWNERS.items()},
            "completed_owner_complete_counts": {name: item[1] for name, item in OWNERS.items()},
            "both_full_uncached_input_unions": [first, second],
            "current_runtime": runtime,
            "limits_CPU_admission_wall": [CPU, ADMISSION, WALL],
            **flags(),
        }
        save("summary.json", summary)
        save("completion_outcome.json", summary)
        owned = inventory(OUTPUT)
        files = {path.name: digest(path, fresh=True) for path in sorted(owned)}
        budget()
        manifest = {
            "schema": "f44-caller-grid-axis-component-manifest-v1",
            "passed": True,
            "completed": True,
            "budget_censored": False,
            "manifest_self_hash_excluded": True,
            "files": files,
            "frozen_inputs": _FROZEN,
            "external_runtime_inputs": _EXTERNAL,
            "row_id": GRID_ROW_ID,
            "source_manifest_SHA256": SOURCE_SHA,
            "audit_manifest_SHA256": ROOT_DECLARED_AUDIT_SHA,
            "final_ROOT_manifest_SHA256": FINAL_ROOT_SHA,
            "ROOT_READY_SHA256": args.ready_sha256,
            "completed_owner_manifest_SHA256": summary["completed_owner_manifest_SHA256"],
            "completed_owner_complete_counts": summary["completed_owner_complete_counts"],
            "both_full_uncached_input_unions": [first, second],
            "limits_CPU_admission_wall": [CPU, ADMISSION, WALL],
            "terminal_budget_observation": {
                "process_CPU_seconds": time.process_time(),
                "wall_seconds": time.monotonic() - _STARTED,
            },
            "certificate_scope": "PROMISED_CALLER_GRID_ONLY",
            "diagnostic_input_case_count": 64,
            "logical_forward_reverse_calls": [128, 128],
            **flags(),
        }
        complete_manifest(manifest, files, sum(path.stat().st_size for path in owned))
        budget()
        print(
            json.dumps(
                {
                    "passed": True,
                    "completed": True,
                    "certificate_scope": "PROMISED_CALLER_GRID_ONLY",
                    "CPU": time.process_time(),
                    "wall": time.monotonic() - _STARTED,
                    **flags(),
                },
                sort_keys=True,
            )
        )
        return 0
    except BaseException as error:
        retain_failure(error)
        raise


if __name__ == "__main__":
    raise SystemExit(main())
