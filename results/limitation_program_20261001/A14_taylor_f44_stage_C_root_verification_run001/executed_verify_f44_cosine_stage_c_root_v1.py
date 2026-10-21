"""Prospective Stage C ROOT metadata integrity; author-only until ROOT release.

All seven actual owners are externally pinned. This controller only hashes full
arrays and compares saved metadata. It evaluates no coefficient, interval,
oracle, gate, phase, replay or resource calculation. Resource rejection remains.
"""

import argparse
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
AUTHOR = RESEARCH / "verify_f44_cosine_stage_c_root_v1.py"
METHOD_DOC = RESEARCH / "F44_COSINE_STAGE_C_ROOT_INTEGRITY_PREFLIGHT_V1.md"
PREFLIGHT = RESEARCH / "f44_cosine_stage_c_root_integrity_preflight_v1.json"
READY = ROOT / ".context/A14_F44_COSINE_STAGE_C_INTEGRITY_ROOT_READY_run001.json"
OUTPUT = PROGRAM / "A14_taylor_f44_stage_C_root_verification_run001"
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
CPU, ADMISSION, WALL = 180, 150, 600
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
    "experiment_f44_cosine_stage_c_v3.py": "9dc012f3015dfa0ac7301bc14fc7bf5a69fe2169aa6c4c122d9bd9b1df1dfee6",
    "A14_F44_COSINE_STAGE_C_IMPLEMENTATION_PREFLIGHT_V3.md": "e90ec80968a596fb2b16c80369c60832abfef2aee501f5e4162d1f0251c4185b",
    "a14_f44_cosine_stage_c_implementation_preflight_v3.json": "85f0d5b8c7be6763c93c74eefce6ca9cbd54464f41ea29987831cb41d3561b41",
    "f44_cosine_stage_c_source.py": "6aa28c87416e30558e459efe2c602866dcc9b2d76e236e93faae05fe65826a74",
    "F44_STAGE_C_BUILDER_INTERFACE_AUTHOR_V1.md": "b737562b5bafdc271d5c08cf4fa13c1f9bde53dea291fea6515b0830ee336141",
}
AUDIT_AUTHORS = {
    "audit_f44_cosine_stage_c_v1.py": "548d444fdd61e97a7d249bcb2e271ae1489617d065d125114f2e1ec6d62a2167",
    "A14_F44_COSINE_STAGE_C_INDEPENDENT_AUDIT_PREFLIGHT_V1.md": "d37ca22d3595823fb53787d54613293ebab86b9ba406f3c72a6b0f293e7ef5c2",
    "a14_f44_cosine_stage_c_independent_audit_preflight_v1.json": "abafdfd42a1f4fa0d2f26926b42fc5142adee9740e6d2df2292a3a36f608185d",
}
INTERPRETER_PINS = {
    str(LAUNCHER): "41123879d2e991377997acadf5f0cf8f34fa10d86362eded8c69b6041e2893b5",
    "C:\\Users\\prith\\AppData\\Local\\Programs\\Python\\Python312\\python.exe": "fd5c46d73d29ba21b04c844bbaf9096066136526911230645a2a040d23fb612b",
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


def loaded_origins():
    forbidden = {"mpmath", "numpy", "scipy", "numba", "sympy", "gmpy", "gmpy2", "sage", "pytest"}
    require(
        not any(name.split(".", 1)[0] in forbidden for name in sys.modules),
        "No numerical or optional scientific imports",
    )
    require(
        not any(
            name.startswith("research.")
            and name not in {__name__, "research.limitation_program_20261001"}
            for name in sys.modules
        ),
        "No builder, producer, auditor or historical scientific imports",
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
                key = key_for(actual)
                mapping = _FROZEN if actual.is_relative_to(ROOT) else _EXTERNAL
                if key not in mapping:
                    add(actual, digest(actual))
                else:
                    require(digest(actual) == mapping[key], "Loaded bytes equal frozen expectation")


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


def flags():
    return dict(
        metadata_integrity_only=True,
        new_scientific_evaluation=False,
        coefficient_interval_oracle_gate_phase_replay_resources_evaluated=False,
        native_gate_binary_interpreted=False,
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
        resource_gate_passed=False,
        component_candidate_eligible=False,
        row_status="REJECTED",
        new_QROM_or_financial_source_release_authorized=False,
    )


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


def admission(ready_sha):
    ready = read(bind(READY, ready_sha))
    require(
        ready["schema"] == "root-a14-f44-stage-c-integrity-READY-v1"
        and ready["ready"] is True
        and ready["root_and_independent_static_reviews_passed"] is True,
        "Separate ROOT static release required",
    )
    require(
        ready["output"] == OUTPUT.relative_to(ROOT).as_posix()
        and ready["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
        and ready["completed_owner_manifest_SHA256"]
        == {name: data[0] for name, data in OWNERS.items()}
        and ready["completed_owner_complete_counts"]
        == {name: data[1] for name, data in OWNERS.items()},
        "Exactly seven externally frozen complete owners and fixed route",
    )
    require(
        ready["metadata_integrity_execution_authorized"] is True
        and ready["new_scientific_evaluation"] is False
        and ready["financial_adoption"] is False
        and ready["fixture_credit"] == 0,
        "Release approves metadata integrity only",
    )
    own = ready["author_method_SHA256"]
    require(
        set(own) == {AUTHOR.name, METHOD_DOC.name, PREFLIGHT.name}, "Exactly three new author files"
    )
    for name, expected in own.items():
        bind(RESEARCH / name, expected)
    policy = read(PREFLIGHT)
    require(
        policy["schema"] == "a14-f44-stage-c-root-integrity-preflight-v1"
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
        and policy["method_SHA256"] == own[METHOD_DOC.name]
        and policy["actual_audit_ROOT_result_review_SHA256"] == ACTUAL_AUDIT_ROOT_SHA
        and policy["new_scientific_evaluation"] is False,
        "Exact metadata-only method and bounded representation",
    )
    require(
        ready["interpreter_expected_SHA256"] == INTERPRETER_PINS,
        "Both fixed interpreter expectations",
    )
    manifests = {name: packet(name, pin, counts) for name, (pin, counts) in OWNERS.items()}
    for name in (SOURCE_NAME, AUDIT_NAME):
        component_scope(
            manifests[name],
            "a14-f44-stage-c-primary90-manifest-v3"
            if name == SOURCE_NAME
            else "a14-f44-stage-c-independent130-manifest-v1",
        )
        observed = manifests[name]["terminal_budget_observation"]
        require(
            0 <= observed["process_CPU_seconds"] < 300 and 0 <= observed["wall_seconds"] < 900,
            "Both actual terminal component clocks bounded",
        )
    require(
        manifests[AUDIT_NAME]["producer_manifest_SHA256"] == SOURCE_SHA
        and manifests[AUDIT_NAME]["producer_complete_counts"] == SOURCE_COUNTS
        and manifests[AUDIT_NAME]["row_status"] == "REJECTED",
        "Actual audit binds same producer and rejection",
    )
    source_ready, audit_ready = (
        read(bind(SOURCE_READY, SOURCE_READY_SHA)),
        read(bind(AUDIT_READY, AUDIT_READY_SHA)),
    )
    require(
        source_ready["schema"] == "root-a14-f44-cosine-stage-c-READY-v3"
        and source_ready["author_method_SHA256"] == SOURCE_AUTHORS
        and source_ready["output"] == SOURCE.relative_to(ROOT).as_posix(),
        "Exact V3 source release",
    )
    require(
        audit_ready["schema"] == "root-a14-f44-cosine-stage-c-audit-READY-v1"
        and audit_ready["author_method_SHA256"] == AUDIT_AUTHORS
        and audit_ready["producer_manifest_SHA256"] == SOURCE_SHA
        and audit_ready["producer_complete_counts"] == SOURCE_COUNTS
        and audit_ready["output"] == AUDIT.relative_to(ROOT).as_posix(),
        "Exact independent130 release",
    )
    originals = {
        name: data[0] for name, data in OWNERS.items() if name not in (SOURCE_NAME, AUDIT_NAME)
    }
    original_counts = {
        name: data[1] for name, data in OWNERS.items() if name not in (SOURCE_NAME, AUDIT_NAME)
    }
    for release in (source_ready, audit_ready):
        require(
            release["completed_prerequisite_manifest_SHA256"] == originals
            and release["completed_prerequisite_complete_counts"] == original_counts,
            "Original five premise owners retained",
        )
    for authors in (SOURCE_AUTHORS, AUDIT_AUTHORS):
        for name, expected in authors.items():
            bind(RESEARCH / name, expected)
    code_caches(
        [RESEARCH / "experiment_f44_cosine_stage_c_v3.py", BUILDER],
        source_ready["existing_new_code_cache_SHA256"],
        source_ready["absent_new_code_cache_paths"],
    )
    code_caches(
        [RESEARCH / "audit_f44_cosine_stage_c_v1.py"],
        audit_ready["existing_new_code_cache_SHA256"],
        audit_ready["absent_new_code_cache_paths"],
    )
    for key, pin, sources in HISTORICAL_CACHE_RELEASES:
        release = read(bind(ROOT / key, pin))
        code_caches(
            [RESEARCH / name for name in sources],
            release["existing_new_code_cache_SHA256"],
            release["absent_new_code_cache_paths"],
        )
    code_caches(
        [AUTHOR], ready["existing_new_code_cache_SHA256"], ready["absent_new_code_cache_paths"]
    )
    admit_prior_failure(ready, policy)
    actual_root = read(bind(ACTUAL_AUDIT_ROOT, ACTUAL_AUDIT_ROOT_SHA))
    require(
        actual_root["passed"] is True
        and actual_root["audit_manifest_SHA256"] == ROOT_DECLARED_AUDIT_SHA
        and actual_root["complete_counts"] == AUDIT_COUNTS
        and actual_root["inclusive_owned_files"] == 18
        and actual_root["all_audit_owned_hashes_and_inventory_verified"] is True
        and actual_root["science_and_resource_result_metadata_reconciled"] is True
        and actual_root["resource_REJECTED_confirmed"] is True
        and actual_root["full_new_fresh_input_union_and_runtime_membership_by_ROOT"] is False
        and actual_root["new_scientific_evaluation"] is False,
        "Scoped prior ROOT result check does not substitute this full rewalk",
    )
    for key, expected in ready["static_review_expected_SHA256"].items():
        require(
            key.startswith(".context/") and ".." not in Path(key).parts, "ROOT-local static review"
        )
        bind(ROOT / key, expected)


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
            "Every saved literal identity and prior authorized status agrees; no interval evaluation",
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


def main():
    global _STARTED
    _STARTED = process_started()
    runtime_scopes()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ready-sha256", required=True)
    args = parser.parse_args()
    require(canonical(__file__) == AUTHOR and not OUTPUT.exists(), "One fresh ROOT integrity route")
    try:
        require(sys.version_info[:3] == (3, 12, 4), "Pinned Python3.12.4 representation")
        for spelling, expected in INTERPRETER_PINS.items():
            bind(Path(spelling), expected)
        fixed_integer_policy()
        # Current standard runtime and both package trees admitted before JSON reads.
        runtime = own_runtime()
        admission(args.ready_sha256)
        loaded_origins()
        first = fresh_union()
        budget(admission=True)
        OUTPUT.mkdir(exist_ok=False)
        for path in (AUTHOR, METHOD_DOC, PREFLIGHT, READY):
            copy(path, "executed_" + path.name)
        save(
            "run_started.json",
            dict(
                created_UTC=datetime.now(timezone.utc).isoformat(),
                PID=os.getpid(),
                limits_CPU_admission_wall=[CPU, ADMISSION, WALL],
                **flags(),
            ),
        )
        report = reconcile_metadata()
        save("metadata_reconciliation.json", report)
        loaded_origins()
        check_code_caches()
        second = fresh_union()
        summary = dict(
            schema="a14-f44-stage-c-root-integrity-summary-v1",
            completed=True,
            passed=True,
            budget_censored=False,
            source_manifest_SHA256=SOURCE_SHA,
            audit_manifest_SHA256=ROOT_DECLARED_AUDIT_SHA,
            completed_owner_manifest_SHA256={name: data[0] for name, data in OWNERS.items()},
            completed_owner_complete_counts={name: data[1] for name, data in OWNERS.items()},
            both_full_uncached_input_unions=[first, second],
            current_runtime=runtime,
            original_scientific_receipts_integrity_verified=True,
            saved_scientific_and_resource_metadata_reconciled=True,
            limits_CPU_admission_wall=[CPU, ADMISSION, WALL],
            budget=dict(
                process_CPU_seconds=time.process_time(), wall_seconds=time.monotonic() - _STARTED
            ),
            **flags(),
        )
        save("summary.json", summary)
        save("completion_outcome.json", {**summary, "failed": False})
        owned, total = {}, 0
        for path in sorted(inventory(OUTPUT)):
            budget()
            total += path.stat().st_size
            require(
                len(owned) < MAX_OWN_FILES - 1 and total <= MAX_OWN_BYTES, "Inclusive own reserve"
            )
            owned[path.relative_to(OUTPUT).as_posix()] = digest(path, fresh=True)
        complete_manifest(
            dict(
                schema="a14-f44-stage-c-root-integrity-manifest-v1",
                files=owned,
                frozen_inputs=_FROZEN,
                external_runtime_inputs=_EXTERNAL,
                manifest_self_hash_excluded=True,
                completed=True,
                passed=True,
                budget_censored=False,
                source_manifest_SHA256=SOURCE_SHA,
                audit_manifest_SHA256=ROOT_DECLARED_AUDIT_SHA,
                completed_owner_manifest_SHA256={name: data[0] for name, data in OWNERS.items()},
                completed_owner_complete_counts={name: data[1] for name, data in OWNERS.items()},
                limits_CPU_admission_wall=[CPU, ADMISSION, WALL],
                both_full_uncached_input_unions=[first, second],
                integer_decimal_digit_limit=INTEGER_DECIMAL_DIGITS,
                integer_serialization_bit_cap=INTEGER_SERIALIZATION_BITS,
                terminal_budget_observation=dict(
                    process_CPU_seconds=time.process_time(),
                    wall_seconds=time.monotonic() - _STARTED,
                ),
                **flags(),
            ),
            owned,
            total,
        )
        budget()
        result = dict(
            passed=True, manifest_SHA256=digest(OUTPUT / "manifest.json", fresh=True), **flags()
        )
        guard_serialization_integers(result)
        print(json.dumps(result), flush=True)
    except BaseException as error:
        retain_failure(error)
        raise


if __name__ == "__main__":
    main()
