"""Independent prospective F44 binary-array auditor; ROOT freeze gates all work.

No builder or producer imports. Native arrays, whole-wire integer replay,
descriptor recurrence, exact cyclotomic CCX phase and fresh cost are checked
independently. Component-only; no cosine, financial or adoption authority.
"""

import argparse
from array import array
import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
from importlib.util import cache_from_source
import json
import os
from pathlib import Path
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[5]
RESEARCH = Path(__file__).resolve().parent
ORIGINAL_RESEARCH = ROOT / "research/limitation_program_20261001"
PROGRAM = ROOT / "results/limitation_program_20261001"
AUTHOR = RESEARCH / "audit_taylor_f44_stage_k.py"
SOURCE_AUTHOR = RESEARCH / "experiment_taylor_f44_stage_k.py"
BUILDER = RESEARCH / "taylor_f44_stage_k_source.py"
SOURCE_POLICY = RESEARCH / "a14_taylor_f44_stage_k_implementation_preflight.json"
SOURCE_DOC = RESEARCH / "A14_TAYLOR_F44_STAGE_K_IMPLEMENTATION_PREFLIGHT.md"
PREFLIGHT = RESEARCH / "a14_taylor_f44_stage_k_audit_preflight.json"
METHOD_DOC = RESEARCH / "A14_TAYLOR_F44_STAGE_K_AUDIT_PREFLIGHT.md"
SOURCE = PROGRAM / "A14_continuation_20261004_stage_k_producer_run002"
OUTPUT = PROGRAM / "A14_continuation_20261004_stage_k_audit_run002"
READY = RESEARCH / "AUDIT_ROOT_READY_run002.json"
SOURCE_READY = RESEARCH / "PRODUCER_ROOT_READY_run002.json"
PROSPECTUS = ORIGINAL_RESEARCH / "a14_taylor_f44_prospectus_v1.json"
PROSPECTUS_DOC = ORIGINAL_RESEARCH / "A14_TAYLOR_F44_PROSPECTUS_V1.md"
PROSPECTUS_SHA = "526b082ca8d9ab1d1583de58e3fc0e6f5632583f6f663088ad42d6d389c713f3"
PROSPECTUS_DOC_SHA = "e4c1a4ad5c1bc23e266d9cbf4cfc5adeb1528fda8cfd89179696108be5302b04"
EXISTING_PACKETS = {
    "A14_cosine_feasibility_run001": (
        "bdb01b0c69d8fab3ee3d61f1c48ce5764f1ae09488f564d186f658f180e4156b",
        [24, 672, 2842],
    ),
    "A14_cosine_feasibility_audit_run003": (
        "52c88dc17c6a53b1df30bd93a431d3e263cb202462901589aaaa30bb87631f0f",
        [17, 752, 2842],
    ),
}
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
W, F, PRODUCT_BITS = 72, 44, 116
CPU, ADMISSION, WALL = 180, 150, 600
MAX_OWN_FILES, MAX_OWN_BYTES = 64, 128 * 1024**2
MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = 24000, 2 * 1024**3
MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK = 100000, 8 * 1024**3, 24 * 1024**3
MAX_NATIVE_ROWS = 1000000
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
_BASE_SCOPE, _EXCLUDED_SCOPE = None, None
_STANDARD_RUNTIME_MEMBERS = set()
_HASH_WORK = _REFERENCES = 0
_STARTED = None
FAILURE_HISTORY = {'research/limitation_program_20261001/continuation_20261004/A14/experiment_taylor_f44_stage_k.py': 'a5fc4b0a2b80716f9a89586c04f156372590b474f5b34cc660a82b5b345d3549', 'research/limitation_program_20261001/continuation_20261004/A14/taylor_f44_stage_k_source.py': 'fd1324ef0b9e0e0135a40a7af4706db8ec0a8b4d35808ba555f8cbf1856ce4c9', 'research/limitation_program_20261001/continuation_20261004/A14/a14_taylor_f44_stage_k_implementation_preflight.json': 'eddb65a09b89b6a9d9ce393023e9e92b812b705456c0e4b74cfb8fed00e5fca4', 'research/limitation_program_20261001/continuation_20261004/A14/A14_TAYLOR_F44_STAGE_K_IMPLEMENTATION_PREFLIGHT.md': '568ad097db4de41fd7ac7e58ae87646ae4dea0a3f2f6bcf51889982f8a19642b', 'research/limitation_program_20261001/continuation_20261004/A14/authoring_freeze.json': 'c1b8f1b498fb2f4c784aa5a8b4cd42fdbef3c42cc994eaa0463b91ea414a4a9f', 'research/limitation_program_20261001/continuation_20261004/A14/PRODUCER_ROOT_READY_run001.json': '3cdc703bcda036ab59bc84923873adf8acf01119356caeb1b7355c97839ee2f2', 'research/limitation_program_20261001/continuation_20261004/A14/producer_launch_run001.log': '4651b5d27085fde4c8d14ccfd830d8cda3a4feca8629d5630318649906437c49', 'results/limitation_program_20261001/A14_continuation_20261004_stage_k_admission_failure_run001/manifest.json': 'dde459d6520ed01b7a14b369dee6112a5485ef778e3ebf81b3d17867d481dde1', 'results/limitation_program_20261001/A14_continuation_20261004_stage_k_admission_failure_run001/retained_a14_taylor_f44_stage_k_implementation_preflight.json': 'eddb65a09b89b6a9d9ce393023e9e92b812b705456c0e4b74cfb8fed00e5fca4', 'results/limitation_program_20261001/A14_continuation_20261004_stage_k_admission_failure_run001/retained_A14_TAYLOR_F44_STAGE_K_IMPLEMENTATION_PREFLIGHT.md': '568ad097db4de41fd7ac7e58ae87646ae4dea0a3f2f6bcf51889982f8a19642b', 'results/limitation_program_20261001/A14_continuation_20261004_stage_k_admission_failure_run001/retained_authoring_freeze.json': 'c1b8f1b498fb2f4c784aa5a8b4cd42fdbef3c42cc994eaa0463b91ea414a4a9f', 'results/limitation_program_20261001/A14_continuation_20261004_stage_k_admission_failure_run001/retained_experiment_taylor_f44_stage_k.py': 'a5fc4b0a2b80716f9a89586c04f156372590b474f5b34cc660a82b5b345d3549', 'results/limitation_program_20261001/A14_continuation_20261004_stage_k_admission_failure_run001/retained_producer_launch_run001.log': '4651b5d27085fde4c8d14ccfd830d8cda3a4feca8629d5630318649906437c49', 'results/limitation_program_20261001/A14_continuation_20261004_stage_k_admission_failure_run001/retained_PRODUCER_ROOT_READY_run001.json': '3cdc703bcda036ab59bc84923873adf8acf01119356caeb1b7355c97839ee2f2', 'results/limitation_program_20261001/A14_continuation_20261004_stage_k_admission_failure_run001/retained_taylor_f44_stage_k_source.py': 'fd1324ef0b9e0e0135a40a7af4706db8ec0a8b4d35808ba555f8cbf1856ce4c9', 'results/limitation_program_20261001/A14_continuation_20261004_stage_k_admission_failure_run001/summary.json': 'a279f32dfdbfb8624270cdfd60a5c01691fe7e43d273fb0d3183aabf1dbb7fb1'}


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
    for tree in (base / "Lib", base / "DLLs", Path(sys.prefix) / "Scripts"):
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
    require(not any(path.exists() for path in _ABSENT_RUNTIME), "Absent standard zip still absent")
    return {"unique_paths": len(union), "unique_bytes": total, "full_fresh_resolve_and_SHA": True}


def save(name, value):
    budget()
    path = OUTPUT / name
    require(path.parent == OUTPUT and not path.exists(), "Exclusive fixed output")
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        for fragment in json.JSONEncoder(sort_keys=True, indent=2, allow_nan=False).iterencode(
            value
        ):
            budget()
            stream.write(fragment)
            budget()
        stream.write("\n")
    require(path.stat().st_size <= MAX_OWN_BYTES, "Owned file cap")
    budget()


def copy(path, name):
    actual = canonical(path)
    before, expected = fingerprint(actual), digest(actual)
    total = 0
    with actual.open("rb") as incoming, (OUTPUT / name).open("xb") as outgoing:
        while block := incoming.read(65536):
            budget()
            total += len(block)
            require(total <= before[2], "Input copy did not grow")
            outgoing.write(block)
            budget()
    require(total == before[2] and fingerprint(actual) == before, "Stable full copy")
    require(digest(OUTPUT / name) == expected, "Exact copied bytes")


def loaded_origins():
    forbidden = {"mpmath", "numpy", "scipy", "numba", "sympy", "gmpy", "gmpy2", "sage", "pytest"}
    require(
        not any(name.split(".", 1)[0] in forbidden for name in sys.modules),
        "No optional scientific kernel imports",
    )
    require(
        not any(
            name.startswith("research.")
            and name not in {__name__, "research.limitation_program_20261001",
                     "research.limitation_program_20261001.continuation_20261004",
                     "research.limitation_program_20261001.continuation_20261004.A14", "research.limitation_program_20261001.continuation_20261004.A14.run002"}
            for name in sys.modules
        ),
        "Independent auditor imports no producer/builder",
    )
    for module in list(sys.modules.values()):
        for attr in ("__file__", "__cached__"):
            origin = getattr(module, attr, None)
            if not origin:
                continue
            lexical = Path(os.path.abspath(str(origin)))
            require(
                not any(
                    lexical.is_relative_to(scope)
                    or lexical.resolve(strict=False).is_relative_to(scope)
                    for scope in _EXCLUDED_SCOPE
                ),
                "Excluded loaded origin/cache",
            )
            if lexical.is_file():
                actual = canonical(lexical)
                require(
                    actual.is_relative_to(ROOT) or actual.is_relative_to(_BASE_SCOPE),
                    "Confined actual source/cache origin",
                )
                key = key_for(actual)
                expected = (_FROZEN if actual.is_relative_to(ROOT) else _EXTERNAL).get(key)
                if expected is None:
                    add(actual, digest(actual))
                else:
                    require(digest(actual) == expected, "Loaded admitted bytes unchanged")


def native_array(name, descriptor, index):
    require(
        type(index) is dict
        and index["gate_file"] == name
        and index["storage"] == "little-endian signedint32 raw Nx4, no header",
        "Fixed independent native ABI",
    )
    path = SOURCE / name
    require(
        path.stat().st_size == index["bytes"] == 16 * index["rows"]
        and index["rows"] == descriptor["gate_rows"]
        and 0 < index["rows"] <= MAX_NATIVE_ROWS,
        "Full native array size",
    )
    require(digest(path, fresh=True) == index["gate_SHA256"], "Native full byte digest")
    require(array("i").itemsize == 4 and sys.byteorder == "little", "Pinned int32 ABI")
    words = array("i")
    before = fingerprint(path)
    with path.open("rb") as stream:
        while block := stream.read(65536):
            budget()
            words.frombytes(block)
    require(
        fingerprint(path) == before and len(words) == 4 * index["rows"], "Stable complete raw array"
    )
    qubits = descriptor["qubits"]
    require(type(qubits) is int and 0 < qubits < 1 << 31, "Full concrete wire count")
    for offset in range(0, len(words), 4):
        budget()
        kind, a, b, c = words[offset : offset + 4]
        operands = (a, b, c)[:kind]
        require(
            kind in (1, 2, 3)
            and all(0 <= wire < qubits for wire in operands)
            and len(set(operands)) == kind
            and all(value == 0 for value in (a, b, c)[kind:]),
            "Every actual row has canonical distinct operands",
        )
    return words


class Consumer:
    """Independently consume actual bytes; allocate no circuit or native rows."""

    def __init__(self, words, descriptor, ports):
        self.words, self.descriptor = words, descriptor
        self.position, self.next_wire = 0, ports

    def bank(self, width, saved=None):
        budget()
        bank = list(range(self.next_wire, self.next_wire + width))
        self.next_wire += width
        if saved is not None:
            require(
                saved == bank and all(type(wire) is int for wire in saved),
                "Exact fresh contiguous bank",
            )
        return bank

    def accept(self, *operands):
        budget()
        offset = 4 * self.position
        expect = (len(operands), *operands, *([0] * (3 - len(operands))))
        require(
            tuple(self.words[offset : offset + 4]) == expect, "Independent exact recurrence row"
        )
        self.position += 1

    def cleanup(self, output_sources, outputs):
        end = self.position
        require(self.descriptor["compute_gate_rows"] == [0, end], "All compute rows retained")
        for a, b in zip(output_sources, outputs, strict=True):
            self.accept(a, b)
        reverse = self.position
        require(
            self.descriptor["copy_gate_rows"] == [end, reverse] and reverse - end == 72,
            "All dirty output XOR rows",
        )
        for index in range(end - 1, -1, -1):
            budget()
            require(
                self.words[4 * self.position : 4 * self.position + 4]
                == self.words[4 * index : 4 * index + 4],
                "Complete literal self-inverse cleanup",
            )
            self.position += 1
        require(
            self.position * 4 == len(self.words)
            and self.position == self.descriptor["gate_rows"]
            and self.next_wire == self.descriptor["qubits"]
            and self.descriptor["inverse_gate_rows"] == [reverse, self.position],
            "Every actual gate and allocated wire consumed",
        )


def ports(descriptor, count, operation):
    args = [list(range(72 * j, 72 * (j + 1))) for j in range(count)]
    out = list(range(72 * count, 72 * (count + 1)))
    require(
        descriptor["schema"] == "a14-f44-stage-k-clean-arithmetic-leaf-v1"
        and descriptor["op"] == operation
        and descriptor["args"] == args
        and descriptor["outs"] == [out]
        and descriptor["private_workspace_zero_entry_exit"] is True
        and descriptor["dirty_output_XOR"] is True
        and descriptor["input_preserved"] is True,
        "Concrete native promised clean XOR ports",
    )
    return args, out


def multiplication_proof(words, desc):
    args, out = ports(desc, 2, "mul")
    a, b = args
    require(
        desc["params"] == {}
        and desc["spec"]
        == {
            "width": 72,
            "fraction_bits": 44,
            "product_width": 116,
            "active_operand_bits": [52, 38],
            "input_contract": {"signed_operand_bits": [52, 38]},
            "variant": "retained-CSA-explicit-ripple-final-v1",
        },
        "Single promised signed52x38 family",
    )
    require(
        desc["full_signed_semantic_product_bits"] == 144
        and desc["generic_active_signed_product_bits"] == 90
        and desc["minimum_times_minimum_positive_power"] == 88
        and desc["product_modulus_bits"] == 116
        and desc["low_product_columns_discarded_before_carry"] is False,
        "Full semantic product and retained116 contract",
    )
    c, recipe = Consumer(words, desc, 216), desc["recipe"]
    columns = [[] for _ in range(116)]
    partials, signed_offset = [], 0
    for i in range(38):
        for j in range(52):
            budget()
            negative = (i == 37) ^ (j == 51)
            term = c.bank(1)[0]
            partials.append(
                {"a_bit": j, "b_bit": i, "column": i + j, "negative": negative, "wire": term}
            )
            if negative:
                c.accept(term)
                signed_offset -= 1 << (i + j)
            c.accept(a[j], b[i], term)
            columns[i + j].append(term)
    correction = signed_offset % (1 << 116)
    require(
        recipe["partials"] == partials
        and correction == (-(2**89 - 2**51 - 2**37)) % (1 << 116)
        and recipe["correction"] == correction,
        "Independent complete signed-plane identity",
    )
    constants = []
    for j in range(116):
        budget()
        if (correction >> j) & 1:
            wire = c.bank(1)[0]
            c.accept(wire)
            constants.append({"column": j, "wire": wire})
            columns[j].append(wire)
    require(recipe["fixed"] == constants, "All full116 negative-weight corrections")
    layer_index = 0
    while any(len(column) > 2 for column in columns):
        budget()
        following, layer = [[] for _ in range(116)], []
        for j in range(116):
            entries = columns[j]
            consumed = len(entries) // 3 * 3
            for offset in range(0, consumed, 3):
                x, y, z = entries[offset : offset + 3]
                summed = c.bank(1)[0]
                c.accept(x, summed)
                c.accept(y, summed)
                carry = None
                if j < 115:
                    carry = c.bank(1)[0]
                    c.accept(x, y, carry)
                    c.accept(summed, z, carry)
                    following[j + 1].append(carry)
                c.accept(z, summed)
                following[j].append(summed)
                layer.append({"column": j, "inputs": [x, y, z], "sum": summed, "carry": carry})
            following[j].extend(entries[consumed:])
        require(
            layer_index < len(recipe["CSA_layers"]) and recipe["CSA_layers"][layer_index] == layer,
            "Every actual CSA layer",
        )
        layer_index += 1
        columns = following
    require(
        layer_index == len(recipe["CSA_layers"]) and columns == recipe["final_columns"],
        "Complete CSA reduction with no hidden layers",
    )
    row_a = c.bank(116, recipe["left"])
    row_b = c.bank(116, recipe["right"])
    product = c.bank(116, recipe["product"])
    for j, column in enumerate(columns):
        if column:
            c.accept(column[0], row_a[j])
        if len(column) == 2:
            c.accept(column[1], row_b[j])
    propagate, carry = c.bank(116, recipe["propagate"]), c.bank(117, recipe["carry"])
    for j in range(116):
        c.accept(row_a[j], propagate[j])
        c.accept(row_b[j], propagate[j])
        c.accept(row_a[j], row_b[j], carry[j + 1])
        if j:
            c.accept(propagate[j], carry[j], carry[j + 1])
        c.accept(propagate[j], product[j])
        if j:
            c.accept(carry[j], product[j])
    require(recipe["output_source_bits"] == list(range(44, 116)), "Retained44..115 output window")
    c.cleanup(product[44:116], out)
    return {
        "actual_array_matched": True,
        "all_promised_signed52x38_inputs": True,
        "whole_low44_carry_and_sign_correction": True,
        "minimum_times_minimum_exact_positive_2_to_88": True,
        "all_input_dirty_output_cleanup_states": True,
        "identities": [
            "-t*2^k=(1-t)*2^k-2^k; complementary bit plane plus full116 correction "
            "equals a*b modulo2^116.",
            "x+y+z=(x XOR y XOR z)+2*(xy XOR((x XOR y)z)); terms of carry are disjoint.",
            "Ripple propagates every column before output bits44..115 are copied.",
            "floor((a*b+k*2^116)/2^44)=floor(a*b/2^44)+k*2^72.",
            "Compute ignores dirty output; exact72XOR and full reverse give clean XOR "
            "on the contract subspace.",
        ],
    }


def rounding_proof(words, desc):
    (z,), out = ports(desc, 1, "round_ties_even")
    require(
        desc["params"] == {"discarded_fractional_bits": 4}
        and desc["spec"]
        == {
            "width": 72,
            "input_fraction_bits": 44,
            "output_fraction_bits": 40,
            "input_contract": {},
            "variant": "retained-signed-quotient-parity-ripple-increment-v1",
        }
        and desc["negative_rounding_is_floor_quotient"] is True,
        "Universal signed rounder contract",
    )
    c, recipe = Consumer(words, desc, 144), desc["recipe"]
    quotient = c.bank(72, recipe["quotient"])
    remainder = c.bank(4, recipe["remainder"])
    history = c.bank(3, recipe["OR_history"])
    increment = c.bank(1)[0]
    require(recipe["increment"] == increment, "Fresh increment wire")
    carry, result = c.bank(73, recipe["carry"]), c.bank(72, recipe["result"])
    sources = [z[j + 4] if j < 68 else z[71] for j in range(72)]
    require(recipe["quotient_source_wires"] == sources, "Signed arithmetic quotient")
    for source, target in zip(sources, quotient, strict=True):
        c.accept(source, target)
    for source, target in zip(z[:4], remainder, strict=True):
        c.accept(source, target)
    for a, b, target in (
        (remainder[0], remainder[1], history[0]),
        (history[0], remainder[2], history[1]),
        (history[1], quotient[0], history[2]),
    ):
        c.accept(a, target)
        c.accept(b, target)
        c.accept(a, b, target)
    c.accept(remainder[3], history[2], increment)
    require(
        desc["predicate_compute_gate_rows"] == [0, c.position], "Actual predicate prefix boundary"
    )
    c.accept(increment, carry[0])
    for j in range(72):
        c.accept(quotient[j], result[j])
        c.accept(carry[j], result[j])
        c.accept(quotient[j], carry[j], carry[j + 1])
    c.cleanup(result, out)
    return {
        "actual_array_matched": True,
        "all_full_signed72_words": True,
        "negative_floor_and_Euclidean_remainder": True,
        "ties_even_not_add8_shift": True,
        "all_input_dirty_output_cleanup_states": True,
        "identities": [
            "z=16*q+r with q=floor(z/16),0<=r<16 for positive and negative signed72 inputs.",
            "r3&(r0|r1|r2|q0) equals r>8 or (r=8 and q odd).",
            "Full72 ripple adds increment0or1; |q|<=2^67, so no signed72 overflow.",
            "All arithmetic history is retained and literally reversed after72 dirty output XORs.",
        ],
    }


def whole_state(words, initial, inverse=False, begin=0, end=None):
    """Different integer-mask interpreter: every wire is represented in one int."""
    end = len(words) // 4 if end is None else end
    require(
        type(initial) is int and initial >= 0 and 0 <= begin <= end <= len(words) // 4,
        "Concrete whole state and exact slice",
    )
    state = initial
    indices = range(end - 1, begin - 1, -1) if inverse else range(begin, end)
    for index in indices:
        budget()
        kind, a, b, c = words[4 * index : 4 * index + 4]
        if kind == 1:
            state ^= 1 << a
        elif kind == 2:
            state ^= ((state >> a) & 1) << b
        else:
            state ^= (((state >> a) & 1) & ((state >> b) & 1)) << c
    budget()
    return state


def basis_diagnostics(words, desc, rows, operation):
    reports = []
    mask = (1 << 72) - 1
    for index, case in enumerate(rows):
        budget(admission=True)
        if operation == "mul":
            a, b, dirty = case
            require(
                -(1 << 51) <= a < 1 << 51 and -(1 << 37) <= b < 1 << 37,
                "Fixed corpus respects input promise",
            )
            reference, values = ((a * b) >> 44) & mask, (a & mask, b & mask)
        else:
            z, dirty = case
            lower = z // 16
            remainder = z - 16 * lower
            reference = (lower + (remainder > 8 or (remainder == 8 and lower % 2))) & mask
            values = (z & mask,)
        initial = sum(value << (72 * j) for j, value in enumerate(values))
        initial |= dirty << (72 * len(values))
        expected = (initial & ~(mask << (72 * len(values)))) | (
            (dirty ^ reference) << (72 * len(values))
        )
        forward = whole_state(words, initial)
        backward = whole_state(words, initial, inverse=True)
        restored = whole_state(words, forward, inverse=True)
        require(
            forward == backward == expected and restored == initial,
            "Independent whole allocated state input/output/cleanup in both directions",
        )
        reports.append(
            {
                "case_index": index,
                "inputs_signed": list(case[:-1]),
                "dirty_output": dirty,
                "reference_raw": reference,
                "forward_passed": True,
                "independent_inverse_direction_passed": True,
                "forward_then_literal_reverse_passed": True,
                "all_allocated_wires_compared": desc["qubits"],
            }
        )
    return reports


def set_bank(value, wires):
    result = 0
    for bit, wire in enumerate(wires):
        budget()
        result |= ((value >> bit) & 1) << wire
    return result


def prefix_diagnostics(words, desc, rows):
    begin, end = desc["predicate_compute_gate_rows"]
    recipe = desc["recipe"]
    reports = []
    for index, (r, parity) in enumerate(rows):
        budget(admission=True)
        initial = 16 * parity + r
        expected = initial | set_bank(parity, recipe["quotient"]) | set_bank(r, recipe["remainder"])
        first, second, third = int(bool(r & 3)), int(bool(r & 7)), int(bool(r & 7 or parity))
        expected |= set_bank(first | (second << 1) | (third << 2), recipe["OR_history"])
        increment = int(r > 8 or (r == 8 and parity == 1))
        expected |= increment << recipe["increment"]
        actual = whole_state(words, initial, begin=begin, end=end)
        require(
            actual == expected
            and whole_state(words, actual, inverse=True, begin=begin, end=end) == initial,
            "Actual prefix complete allocated state and exact inverse",
        )
        reports.append(
            {
                "case_index": index,
                "remainder": r,
                "quotient_parity": parity,
                "increment": increment,
                "actual_emitted_prefix_replayed": True,
                "full_prefix_wire_state_passed": True,
                "literal_reverse_passed": True,
                "all_allocated_wires_compared": desc["qubits"],
            }
        )
    return reports


MACRO = (
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


def exact_macro_phase():
    """Exact Q[zeta]/(zeta^4+1) amplitude proof for all8 columns, not floating point."""
    zero = (Fraction(0),) * 4
    one = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))

    def add(a, b, sign=1):
        return tuple(x + sign * y for x, y in zip(a, b, strict=True))

    def phase(a, exponent):
        result = [Fraction(0)] * 4
        for j, value in enumerate(a):
            index = (j + exponent) % 8
            result[index % 4] += value if index < 4 else -value
        return tuple(result)

    def half_root_two(a):
        return tuple(value / 2 for value in add(phase(a, 1), phase(a, 3), -1))

    for basis in range(8):
        budget()
        state = [zero] * 8
        state[basis] = one
        for event in MACRO:
            budget()
            if event[0] == "H":
                wire = event[1]
                following = [zero] * 8
                for index in range(8):
                    if not (index >> wire) & 1:
                        partner = index ^ (1 << wire)
                        following[index] = half_root_two(add(state[index], state[partner]))
                        following[partner] = half_root_two(add(state[index], state[partner], -1))
                state = following
            elif event[0] == "CX":
                control, target = event[1:]
                following = [zero] * 8
                for index, amplitude in enumerate(state):
                    following[index ^ (((index >> control) & 1) << target)] = amplitude
                state = following
            else:
                wire = event[1]
                state = [
                    phase(value, 1 if event[0] == "T" else -1) if (index >> wire) & 1 else value
                    for index, value in enumerate(state)
                ]
        expected = basis ^ (((basis & 1) & ((basis >> 1) & 1)) << 2)
        require(
            state == [one if index == expected else zero for index in range(8)],
            "Absolute exact7T CCX matrix column, no global or relative phase",
        )
    return {
        "all_eight_exact_operator_columns": True,
        "algebra": "Q[zeta]/(zeta^4+1), zeta=exp(i*pi/4)",
        "global_phase_exactly_one": True,
        "T_TD_events": 7,
        "CX_events": 6,
        "H_events": 2,
        "finite_primitive_diagnostic_count_unchanged": 88,
    }


def resources(words, qubits):
    native = [0, 0, 0]
    t_clock, ct_clock = [0] * qubits, [0] * qubits
    for offset in range(0, len(words), 4):
        budget()
        kind, a, b, c = words[offset : offset + 4]
        native[kind - 1] += 1
        wires = (a, b, c)
        events = MACRO if kind == 3 else (("CX", 0, 1),) if kind == 2 else (("X", 0),)
        for event in events:
            budget()
            affected = tuple(wires[j] for j in event[1:])
            next_t = max(t_clock[wire] for wire in affected) + (event[0] in {"T", "TD"})
            next_ct = max(ct_clock[wire] for wire in affected) + 1
            for wire in affected:
                t_clock[wire], ct_clock[wire] = next_t, next_ct
    x, cx, ccx = native
    return {
        "qubits": qubits,
        "source_gates": len(words) // 4,
        "x": x,
        "cx": cx,
        "ccx": ccx,
        "t_count": ccx * 7,
        "t_depth": max(t_clock),
        "clifford_t_depth": max(ct_clock),
        "clifford_cx": cx + 6 * ccx,
        "clifford_h": 2 * ccx,
        "phase_macro": "absolute exact7T CCX; parity polynomial4abc, H target conjugation",
        "schedule": "all-to-all ASAP chronological expansion of every native row",
        "caller_argument_copy_CX_not_in_leaf": True,
        "no_F40_or_prior_multiplier_resource_transfer": True,
    }


def fixed_corpus():
    pairs = (
        (0, 0),
        (0, 1),
        (1, 0),
        (-1, 1),
        (-(1 << 51), -(1 << 37)),
        ((1 << 51) - 1, (1 << 37) - 1),
        (-(1 << 51), (1 << 37) - 1),
        ((1 << 51) - 1, -(1 << 37)),
    )
    dirties = (0, (1 << 72) - 1)
    return {
        "multiplier": [(a, b, d) for a, b in pairs for d in dirties],
        "rounder": [
            (16 * q + r, d) for q in (-2, -1, 0, 1) for r in (0, 7, 8, 9, 15) for d in dirties
        ],
        "Boolean_prefix": [(r, parity) for r in range(16) for parity in (0, 1)],
    }


def flags():
    return {
        "new_test_credit": 0,
        "new_credited_gate_replays": 0,
        "new_price_samples": 0,
        "Stage_K_diagnostics_not_cosine_or_financial_certificate": True,
        "Stage_C_release_authorized": False,
        "full_G2": False,
        "adoption": False,
        "cost_transfer": False,
        "quantum_advantage": False,
        "independent_scientific_audit_complete": True,
        "ROOT_integrity_still_required": True,
        "previous_A14_rejected_rows_unchanged": True,
    }


def admission(expected_ready, expected_source):
    ready = read(bind(READY, expected_ready))
    for key, pin in FAILURE_HISTORY.items():
        bind(ROOT / key, pin)
    require(
        ready["schema"] == "root-a14-taylor-f44-stage-k-audit-READY-v1"
        and ready["ready"] is True
        and ready["root_and_independent_static_reviews_passed"] is True,
        "Externally reviewed separate audit release",
    )
    require(
        ready["source_manifest_SHA256"] == expected_source
        and ready["output"] == OUTPUT.relative_to(ROOT).as_posix()
        and ready["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
        and ready["argv_prefix"]
        == [
            "-B",
            "-m",
            "research.limitation_program_20261001.continuation_20261004.A14.run002.audit_taylor_f44_stage_k",
            "--ready-sha256",
        ],
        "Exact source, route, clocks and CLI",
    )
    paths = (AUTHOR, PREFLIGHT, METHOD_DOC)
    pins = ready["author_method_SHA256"]
    require(
        type(pins) is dict and set(pins) == {path.name for path in paths},
        "Exactly three frozen audit files",
    )
    for path in paths:
        bind(path, pins[path.name])
    policy = read(PREFLIGHT)
    require(
        policy["schema"] == "a14-taylor-f44-stage-k-audit-preflight-v1"
        and policy["author_SHA256"] == {AUTHOR.name: pins[AUTHOR.name]}
        and policy["method_document_SHA256"] == pins[METHOD_DOC.name]
        and policy["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
        and policy["owned_caps_files_bytes"] == [MAX_OWN_FILES, MAX_OWN_BYTES]
        and policy["fixed_diagnostic_counts"] == [16, 40, 32, 88],
        "Exact fixed independent audit policy",
    )
    source_pins = policy["producer_author_method_SHA256"]
    require(
        source_pins == ready["producer_author_method_SHA256"]
        and set(source_pins)
        == {path.name for path in (SOURCE_AUTHOR, BUILDER, SOURCE_POLICY, SOURCE_DOC)},
        "Exactly four producer files remain immutable",
    )
    for path in (SOURCE_AUTHOR, BUILDER, SOURCE_POLICY, SOURCE_DOC):
        bind(path, source_pins[path.name])
    bind(PROSPECTUS, PROSPECTUS_SHA)
    bind(PROSPECTUS_DOC, PROSPECTUS_DOC_SHA)
    bind(SOURCE_READY, ready["producer_ROOT_READY_SHA256"])
    for name, (pin, counts) in EXISTING_PACKETS.items():
        packet(name, pin, counts)
    source_manifest = read(bind(SOURCE / "manifest.json", expected_source))
    counts = ready["source_complete_counts"]
    require(
        type(counts) is list
        and len(counts) == 3
        and all(type(count) is int and count > 0 for count in counts),
        "ROOT freezes actual full source maps after its PASS",
    )
    packet(SOURCE.name, expected_source, counts)
    require(
        source_manifest["schema"] == "a14-taylor-f44-stage-k-manifest-v1"
        and source_manifest["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
        and source_manifest["Stage_C_release_authorized"] is False
        and source_manifest["full_G2"] is False
        and source_manifest["adoption"] is False,
        "Only actual original component source PASS",
    )
    observed = source_manifest["terminal_budget_observation"]
    require(
        0 <= observed["process_CPU_seconds"] < CPU and 0 <= observed["wall_seconds"] < WALL,
        "Actual source terminal observation stays within the unchanged clocks",
    )
    require(
        source_manifest["frozen_inputs"][SOURCE_READY.relative_to(ROOT).as_posix()]
        == ready["producer_ROOT_READY_SHA256"],
        "Actual producer release bound by source",
    )
    for path in (SOURCE_AUTHOR, BUILDER, SOURCE_POLICY, SOURCE_DOC):
        key = path.relative_to(ROOT).as_posix()
        require(
            source_manifest["frozen_inputs"][key] == source_pins[path.name]
            and digest(SOURCE / ("executed_" + path.name), fresh=True) == source_pins[path.name],
            "Original executed producer author and method copies remain exact",
        )
    require(
        digest(SOURCE / ("executed_" + SOURCE_READY.name), fresh=True)
        == ready["producer_ROOT_READY_SHA256"],
        "Original executed producer ROOT release copy",
    )
    cache = Path(cache_from_source(str(AUTHOR)))
    caches = {key_for(cache): digest(cache)} if cache.exists() else {}
    require(
        ready["existing_new_code_cache_SHA256"] == caches,
        "Exact audit cache presence and pinned bytes",
    )
    for key, expected in caches.items():
        bind(ROOT / key, expected)
    runtime = own_runtime()
    return ready, runtime


def retain_failure(error):
    if not OUTPUT.is_dir():
        return
    try:
        budget()
        require(
            not (OUTPUT / "manifest.json").exists()
            and not (OUTPUT / "completion_outcome.json").exists(),
            "Never repair or reseal partial terminal",
        )
        save(
            "failure.json",
            {
                "failed": True,
                "passed": False,
                "error_type": type(error).__name__,
                "error": str(error),
                "traceback": traceback.format_exc(),
                "independent_scientific_audit_complete": False,
                "observed_CPU_seconds": time.process_time(),
                "observed_wall_seconds": time.monotonic() - _STARTED,
            },
        )
    except BaseException:
        pass
    try:
        with (OUTPUT / "FAILED_UNSEALED.json").open("xb") as stream:
            stream.write(
                b'{"failed":true,"completed":false,"passed":false,"budget_censored":null,"hard_budget_state_uncertified":true,"partial_success_invalid":true,"new_test_credit":0,"full_G2":false,"adoption":false}\n'
            )
    except OSError:
        pass


def main():
    global _STARTED
    _STARTED = process_started()
    runtime_scopes()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ready-sha256", required=True)
    parser.add_argument("--source-manifest-sha256", required=True)
    args = parser.parse_args()
    require(
        canonical(__file__) == AUTHOR and not OUTPUT.exists(), "One fresh audit route, no retry"
    )
    try:
        ready, runtime = admission(args.ready_sha256, args.source_manifest_sha256)
        first = fresh_union()
        budget(admission=True)
        OUTPUT.mkdir(exist_ok=False)
        for path in (AUTHOR, PREFLIGHT, METHOD_DOC, READY):
            copy(path, "executed_" + path.name)
        save(
            "run_started.json",
            {
                "created_UTC": datetime.now(timezone.utc).isoformat(),
                "PID": os.getpid(),
                "ROOT_READY_SHA256": args.ready_sha256,
                "source_manifest_SHA256": args.source_manifest_sha256,
                "limits_CPU_admission_wall": [CPU, ADMISSION, WALL],
                "scope": "independent component arrays only; no Stage C release",
            },
        )
        desc = read(SOURCE / "primitive_descriptors.json")
        index = read(SOURCE / "native_gate_arrays.json")
        require(
            set(desc) == set(index) == {"multiplier", "rounder"},
            "Exactly two fixed original arrays",
        )
        arrays = {name: native_array(name + ".gates.bin", desc[name], index[name]) for name in desc}
        require(
            sum(len(words) // 4 for words in arrays.values()) <= MAX_NATIVE_ROWS,
            "Fixed total native row cap",
        )
        mul = multiplication_proof(arrays["multiplier"], desc["multiplier"])
        rounding = rounding_proof(arrays["rounder"], desc["rounder"])
        phase = exact_macro_phase()
        producer_certificate = read(SOURCE / "universal_structural_certificate.json")
        require(
            producer_certificate["phase_macro"] == [list(event) for event in MACRO]
            and producer_certificate["multiplier"]["array_matched"] is True
            and producer_certificate["rounder"]["array_matched"] is True,
            "Actual producer proof bound; independent proof is separately derived",
        )
        save(
            "independent_universal_certificate.json",
            {"multiplier": mul, "rounder": rounding, "absolute_phase": phase, **flags()},
        )
        cost = {name: resources(arrays[name], desc[name]["qubits"]) for name in arrays}
        source_cost = read(SOURCE / "primitive_resources.json")
        require(
            all(cost[name] == source_cost[name] for name in cost)
            and source_cost["no_prior_resource_transfer"] is True
            and source_cost["full_cosine_or_financial_cost_claim"] is False,
            "Every independently recounted native gate and macro depth equals actual source",
        )
        save("independent_primitive_resources.json", {**cost, **flags()})
        corpus = fixed_corpus()
        diagnostic = {
            "multiplier": basis_diagnostics(
                arrays["multiplier"], desc["multiplier"], corpus["multiplier"], "mul"
            ),
            "rounder": basis_diagnostics(
                arrays["rounder"], desc["rounder"], corpus["rounder"], "rounder"
            ),
            "Boolean_prefix": prefix_diagnostics(
                arrays["rounder"], desc["rounder"], corpus["Boolean_prefix"]
            ),
        }
        original_diagnostic = read(SOURCE / "fixed_diagnostics.json")
        require(
            original_diagnostic["cases"] == diagnostic and original_diagnostic["fixed_total"] == 88,
            "All actual88 producer reports exactly match independent binary replay",
        )
        save(
            "independent_fixed_diagnostics.json",
            {"cases": diagnostic, "fixed_total": 88, **flags()},
        )
        source_summary = read(SOURCE / "summary.json")
        source_outcome = read(SOURCE / "completion_outcome.json")
        for summary in (source_summary, source_outcome):
            require(
                summary["completed"] is True
                and summary["passed"] is True
                and summary["budget_censored"] is False
                and summary["fixed_diagnostic_counts"] == [16, 40, 32, 88]
                and summary["actual_full_leaf_replay_calls"] == 168
                and summary["actual_Boolean_prefix_replay_calls"] == 64
                and summary["native_gate_arrays"] == index
                and summary["native_rows_total"]
                == sum(len(words) // 4 for words in arrays.values())
                and summary["arithmetic_component_diagnostics_complete"] is True
                and summary["actual_array_matched_universal_structure"] is True
                and summary["absolute7T_phase_proof_bound"] is True
                and summary["Stage_C_release_authorized"] is False
                and summary["full_G2"] is False
                and summary["adoption"] is False,
                "Actual complete scoped producer summary and outcome",
            )
            require(
                0 <= summary["budget"]["process_CPU_seconds"] < CPU
                and 0 <= summary["budget"]["wall_seconds"] < WALL,
                "Actual producer summary and outcome remain within scientific clocks",
            )
        require(source_outcome["failed"] is False, "Producer authoritative successful terminal")
        loaded_origins()
        second = fresh_union()
        summary = {
            "schema": "a14-taylor-f44-stage-k-audit-summary-v1",
            "completed": True,
            "passed": True,
            "budget_censored": False,
            "source_manifest_SHA256": args.source_manifest_sha256,
            "actual_array_matched_universal_structure": True,
            "absolute7T_phase_proof_bound": True,
            "actual_binary_independent_replay": True,
            "actual_resource_recount": True,
            "fixed_diagnostic_counts": [16, 40, 32, 88],
            "current_runtime": runtime,
            "both_full_uncached_input_unions": [first, second],
            "limits_CPU_admission_wall": [CPU, ADMISSION, WALL],
            "budget": {
                "process_CPU_seconds": time.process_time(),
                "wall_seconds": time.monotonic() - _STARTED,
            },
            **flags(),
        }
        save("summary.json", summary)
        save("completion_outcome.json", {**summary, "failed": False})
        owned, total = {}, 0
        for path in sorted(inventory(OUTPUT)):
            budget()
            total += path.stat().st_size
            require(
                len(owned) < MAX_OWN_FILES - 1 and total <= MAX_OWN_BYTES, "Strict total owned caps"
            )
            owned[path.relative_to(OUTPUT).as_posix()] = digest(path, fresh=True)
        save(
            "manifest.json",
            {
                "schema": "a14-taylor-f44-stage-k-audit-manifest-v1",
                "files": owned,
                "frozen_inputs": _FROZEN,
                "external_runtime_inputs": _EXTERNAL,
                "manifest_self_hash_excluded": True,
                "completed": True,
                "passed": True,
                "budget_censored": False,
                "source_manifest_SHA256": args.source_manifest_sha256,
                "both_full_uncached_input_unions": [first, second],
                "limits_CPU_admission_wall": [CPU, ADMISSION, WALL],
                "terminal_budget_observation": {
                    "process_CPU_seconds": time.process_time(),
                    "wall_seconds": time.monotonic() - _STARTED,
                },
                **flags(),
            },
        )
        budget()
        print(
            json.dumps(
                {
                    "passed": True,
                    "manifest_SHA256": digest(OUTPUT / "manifest.json", fresh=True),
                    **flags(),
                }
            )
        )
    except BaseException as error:
        retain_failure(error)
        raise


if __name__ == "__main__":
    main()
