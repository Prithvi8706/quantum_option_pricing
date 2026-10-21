"""AUTHOR-ONLY independent fresh A14 receipt integrity, never numerical replay.

Runtime/cache/confinement patterns copied as text from executed passed
verify_exp_frontier_allocation_root_v2.py, exact frozen SHA
b0aac76928ad41a48cb1884d14f76168d8ef783595f918177857e5b13a91861f.
Fixed180 process CPU/150 admission/600 wall, one thread. Both complete unique
source/audit/review/runtime unions freshly resolve and fully hash every byte.
The original source PASS pin is fixed; audit003 and its new static release require
explicit root-issued expected manifest pins on the CLI before this NEW verifier
can execute. Those pins are never derived from freshly observed hashes.
The old failed audit,
actual bounded angle diagnostic and all original reviews remain separate inputs.
A completed two-row screen never implies component eligibility or adoption.
"""

import argparse
import ctypes
from ctypes import wintypes
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
PROGRAM = ROOT / "results/limitation_program_20261001"
AUTHOR = RESEARCH / "verify_cosine_feasibility_root_v3.py"
OUTPUT = PROGRAM / "A14_cosine_feasibility_root_verification_run003"
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
SOURCE = PROGRAM / "A14_cosine_feasibility_run001"
AUDIT = PROGRAM / "A14_cosine_feasibility_audit_run003"
SOURCE_SHA = "bdb01b0c69d8fab3ee3d61f1c48ce5764f1ae09488f564d186f658f180e4156b"
AUDIT_SHA = None
FAILED = PROGRAM / "A14_cosine_feasibility_audit_run001"
FAILED_SHA = "3b423ce15bd752745747807bf2970a2d7888a057d6c86ced1f2ed0efd98ece6e"
DIAGNOSTIC = PROGRAM / "A14_cosine_literal_diagnostic_run001"
DIAGNOSTIC_SHA = "c2dc33d96b0604d09666351ddefcd754d048b787f66e350174eda75c9b9fe8af"
NEW_AUDIT_AUTHORS = {
    "audit_cosine_feasibility_v3.py": (
        "55070e0f64c3f68697bcbeb931d87f3f38190dcf43537ad4e48fe2d91d08b96f"
    ),
    "A14_COSINE_FEASIBILITY_AUDIT_IMPLEMENTATION_PREFLIGHT_V3.md": (
        "001eb0fc772e1e9f878e237b884be9af4cf48b4a860eb63893a2ee63a07097f2"
    ),
    "a14_cosine_feasibility_audit_implementation_preflight_v3.json": (
        "c1bc565152bca1bb0d600452cfff811ba0b68f7c538bfcc55c7949724e5a5a4d"
    ),
}
NEW_REVIEW_NAME = "A14_cosine_feasibility_audit_root_review_run003"
NEW_REVIEW_SHA = "db63fda477c28adecde7038a928541661b3a2e5278dfe1b817a15764e41624a4"
PRIOR_V2_AUDIT = PROGRAM / "A14_cosine_feasibility_audit_run002"
PRIOR_V2_AUTHORS = {
    "audit_cosine_feasibility_v2.py": (
        "4f871b9455e08df902439a3ad1fbf84a92201db29da6b656104d0c7a5f4b4984"
    ),
    "A14_COSINE_FEASIBILITY_AUDIT_IMPLEMENTATION_PREFLIGHT_V2.md": (
        "5b6c17d387a491028c3e83b02a1e74d558cf352a223397c8c0d7eda9d2b985a8"
    ),
    "a14_cosine_feasibility_audit_implementation_preflight_v2.json": (
        "17e05e2515bfd4bacd0e8cd6ae27610f2df2815aaf66fb60e4315922569d622c"
    ),
}
PRIOR_V2_FAILURE = PROGRAM / "A14_cosine_audit_admission_failure_run002"
PRIOR_V2_FAILURE_SHA = "9ff4a87b66876597c696bcaea84b20d68002f25b59ccc5151a6b695acc261dd7"
PRIOR_V2_REVIEW = PROGRAM / "A14_cosine_feasibility_audit_root_review_run002"
PRIOR_V2_REVIEW_SHA = "a2edeb0d4bbf41b2ec2f3591d5ace657c935682b980499dfbf8850118b323051"
PRIOR_V2_LOG = ROOT / ".context/a14_cosine_audit_prepare_run002.log"
PRIOR_V2_LOG_SHA = "1b3886341ff468441b9b6b018883778b3ab573721bcfab7d74b575625212f647"
ORIGIN = RESEARCH / "verify_exp_frontier_allocation_root_v2.py"
ORIGIN_SHA = "b0aac76928ad41a48cb1884d14f76168d8ef783595f918177857e5b13a91861f"
CPU, ADMISSION, WALL = 180, 150, 600
MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = 24000, 2 * 1024**3
MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK = 100000, 8 * 1024**3, 24 * 1024**3
MAX_OWN_FILES, MAX_OWN_BYTES = 64, 128 * 1024**2
ROWS = ("CORDIC_N48_W72_F56_BK72", "TAYLOR_D6_S64_W72_F40")
AUTHORS = {
    "experiment_cosine_feasibility.py": (
        "dba562b13f4d250c04376927f431e5a39ceaedfdcfc5e8ebc579bb9cdad27112"
    ),
    "audit_cosine_feasibility.py": (
        "020a9428c4a13088201f6bef5abafa6b3daee73a8ef20166efffd83147df2e35"
    ),
    "A14_COSINE_FEASIBILITY_PREFLIGHT.md": (
        "e4a66f142f2cd7458d566fbace4acd883634308534d7b5bc66cd47e4478d874b"
    ),
    "a14_cosine_feasibility_preflight.json": (
        "ae4d0d56b720a72682eeef55ad809e97d74a84631542d9de334d56af583754ad"
    ),
    "A14_COSINE_FEASIBILITY_IMPLEMENTATION_PREFLIGHT.md": (
        "1dc635235419f54f343cc9a0cf05f79ecd434ea85a7e3bf60ae248bf3f8ba8a4"
    ),
    "a14_cosine_feasibility_implementation_preflight.json": (
        "0bbf8860c0cfbe474b88e3193a35265e3b622477c42ccfbfcf3d8fcee2a467e2"
    ),
}
REVIEWS = {
    "A14_cosine_feasibility_root_review_run001": (
        "94d7577ac27385c7d2ee2aab7e421b7b5d48a899b8c19308d4a5c6e11b5a843f"
    ),
    "A14_cosine_feasibility_root_review_run002": (
        "34eb866f076cbc75226ff48b8079cb09b001fb7388f4d9944e0a3e5848652d18"
    ),
    "A14_cosine_literal_diagnostic_root_review_run001": (
        "7511709f30647a2dd6aa6b277ae38ddedf7c81cb975c9eac2dd1d70415d3d059"
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
_PATH_CACHE, _HASH_CACHE = {}, {}
_BASE_SCOPE, _EXCLUDED_SCOPE = None, None
_STANDARD_RUNTIME_MEMBERS = set()


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


def canonical_sha(value):
    return type(value) is str and len(value) == 64 and all(c in "0123456789abcdef" for c in value)


def same(first, second, message):
    budget()
    require(
        json.dumps(first, sort_keys=True, separators=(",", ":"), allow_nan=False)
        == json.dumps(second, sort_keys=True, separators=(",", ":"), allow_nan=False),
        message,
    )
    budget()


def packet(
    directory, expected, *, static_review=False, failed=False, diagnostic=False, capture=False
):
    require(canonical_sha(expected), "Actual terminal manifest pin must be fixed before execution")
    directory = canonical(directory)
    require(directory.parent == PROGRAM, "Exact finite A14 receipt inventory")
    require(sum((static_review, failed, diagnostic, capture)) <= 1, "One exact packet scope")
    if failed:
        require(
            directory == FAILED and not (directory / "FAILED_UNSEALED.json").exists(),
            "Only the exact original sealed failure",
        )
    else:
        no_failure(directory)
    mf_path = add(directory / "manifest.json", expected)
    mf = read(mf_path)
    current_static_release = static_review and directory.name == NEW_REVIEW_NAME
    if current_static_release:
        require(
            expected == NEW_REVIEW_SHA
            and mf.get("schema") == "root-a14-cosine-independent-audit-static-manifest-v3"
            and mf.get("manifest_self_hash_excluded") is True
            and mf.get("passed") is True
            and mf.get("ready") is True
            and mf.get("new_test_credit") == 0
            and mf.get("failed", False) is False
            and mf.get("original_expected_hashes_waived", False) is False,
            "Exact issued V3 static release schema is provenance, never science completion",
        )
    else:
        require(
            mf.get("manifest_self_hash_excluded") is True
            and mf.get("completed") is (not failed)
            and mf.get("passed") is (not (failed or capture))
            and mf.get("budget_censored") is False
            and mf.get("original_expected_hashes_waived", False if static_review else None)
            is False,
            "Sealed complete uncensored original terminal without SHA waiver",
        )
    owned, frozen, external = [
        mf.get(field, {}) for field in ("files", "frozen_inputs", "external_runtime_inputs")
    ]
    require(
        type(owned) is dict and owned and type(frozen) is dict and type(external) is dict,
        "Recognized complete original maps",
    )
    members = set()
    for key, pin in owned.items():
        budget()
        require(
            type(key) is str
            and not Path(key).is_absolute()
            and "\\" not in key
            and ".." not in Path(key).parts,
            "Canonical relative own key",
        )
        root_relative = key.startswith("results/")
        actual = add(ROOT / key if root_relative else directory / key, pin)
        require(
            actual.is_relative_to(directory) and actual != mf_path and actual not in members,
            "Unique actual owned receipt membership",
        )
        require(
            actual.relative_to(ROOT if root_relative else directory).as_posix() == key,
            "Exact own lexical route, never an alias",
        )
        members.add(actual)
    for key, pin in frozen.items():
        budget()
        require(
            type(key) is str
            and not Path(key).is_absolute()
            and "\\" not in key
            and ".." not in Path(key).parts,
            "Canonical ROOT input key",
        )
        actual = add(ROOT / key, pin)
        require(
            actual.is_relative_to(ROOT) and actual.relative_to(ROOT).as_posix() == key,
            "Exact original ROOT input route",
        )
    for key, pin in external.items():
        budget()
        require(type(key) is str and Path(key).is_absolute(), "Exact external runtime key")
        actual = add(key, pin)
        require(
            not actual.is_relative_to(ROOT) and str(actual) == key,
            "Exact actual external runtime route",
        )
    exact_inventory = members | {mf_path}
    require(inventory(directory) == exact_inventory, "Exact complete original owned inventory")
    _OWN_INVENTORIES[directory] = exact_inventory
    _PACKETS[directory.name] = {
        "manifest_sha256": expected,
        "owned": len(owned),
        "frozen_inputs": len(frozen),
        "external_runtime_inputs": len(external),
        "static_review_only": static_review,
        "failed_original": failed,
        "diagnostic_only": diagnostic,
        "pre_mkdir_failure_capture_only": capture,
    }
    if failed:
        require(
            [len(owned), len(frozen), len(external)] == [13, 697, 2842],
            "Complete exact failed-audit maps retained",
        )
        outcome = read(directory / "completion_outcome.json")
        failure = read(directory / "failure.json")
        require(
            outcome.get("failed") is True
            and outcome.get("passed") is False
            and outcome.get("completed") is False
            and outcome.get("budget_censored") is False
            and outcome.get("independent_audit_passed") is False
            and outcome.get("new_test_credit") == 0
            and failure.get("error_type") == "ValueError"
            and failure.get("error")
            == "Fresh130 true-angle inclusion and actual absolute error authorization"
            and failure.get("budget_censored") is False,
            "Original uncensored authorization failure never promoted",
        )
        require(not (directory / "summary.json").exists(), "No old independent PASS summary")
        return {"manifest": mf, "outcome": outcome, "failure": failure}
    summary = read(directory / "summary.json")
    if capture:
        outcome = read(directory / "completion_outcome.json")
        require(
            directory == PRIOR_V2_FAILURE
            and [len(owned), len(frozen), len(external)] == [5, 54, 2842]
            and mf.get("schema") == "a14-cosine-audit-admission-failure-manifest-v2"
            and mf.get("failed") is True
            and mf.get("diagnostic_integrity") is True
            and mf.get("original_attempt_failed") is True
            and mf.get("scientific_execution") is False
            and mf.get("new_test_credit") == 0,
            "Complete exact metadata-only capture retains the failed V2 preparation",
        )
        require(
            summary.get("schema") == "a14-cosine-audit-pre-mkdir-admission-failure-v2"
            and summary.get("passed") is False
            and summary.get("failed") is True
            and summary.get("diagnostic_integrity") is True
            and summary.get("original_attempt_failed") is True
            and summary.get("intended_receipt") == PRIOR_V2_AUDIT.relative_to(ROOT).as_posix()
            and summary.get("intended_receipt_absent") is True
            and summary.get("no_original_protocol_receipt_or_math_result") is True
            and summary.get("original_attempt_CPU_wall_not_recorded") is True
            and summary.get("original_source_or_audit_replayed") is False
            and summary.get("original_six_and_primary_source_unchanged") is True
            and summary.get("scientific_execution") is False
            and summary.get("error_type") == "ValueError"
            and summary.get("error") == "Exact audit-only source, prior failure and fresh route"
            and summary.get("original_bad_constant_length") == 65
            and summary.get("exact_required_constant_length") == 64
            and summary.get("exact_required_review_SHA256")
            == REVIEWS["A14_cosine_literal_diagnostic_root_review_run001"]
            and summary.get("original_log_bytes_not_converted") is True
            and summary.get("original_log_decoding") == "utf-16",
            "Real pre-mkdir failure and exact unchanged log bytes, never scientific approval",
        )
        bad = summary["original_bad_review_SHA256"]
        require(
            type(bad) is str
            and len(bad) == 65
            and bad.replace("38ddeddf", "38ddedf", 1) == summary["exact_required_review_SHA256"],
            "Only the recorded extra-character defect was corrected",
        )
        same(summary["prior_audit_v2_author_SHA256"], PRIOR_V2_AUTHORS, "Old V2 trio retained")
        require(
            summary["prior_audit_v2_root_review_manifest_SHA256"] == PRIOR_V2_REVIEW_SHA
            and summary["actual_failed_prepare_log"] == PRIOR_V2_LOG.relative_to(ROOT).as_posix()
            and summary["actual_failed_prepare_log_SHA256"] == PRIOR_V2_LOG_SHA
            and summary["capture_runtime_not_claimed_as_original_attempt_provenance"] is True
            and not PRIOR_V2_AUDIT.exists(),
            "No fabricated original packet, timing or runtime provenance",
        )
        for value in (summary, outcome):
            require(
                value.get("passed") is False
                and value.get("failed") is True
                and value.get("diagnostic_integrity") is True
                and value.get("original_attempt_failed") is True
                and value.get("scientific_execution") is False
                and value.get("new_test_credit") == 0
                and all(value.get(key) is False for key in ("full_G2", "adoption", "cost_transfer"))
                and 0 <= value["capture_process_CPU_seconds"] < 180
                and 0 <= value["capture_wall_seconds"] < 600,
                "Diagnostic integrity keeps the original scientific attempt failed at zero credit",
            )
        require(
            outcome.get("completed") is True and outcome.get("budget_censored") is False,
            "Actual metadata capture completed uncensored",
        )
        for name, pin in PRIOR_V2_AUTHORS.items():
            budget()
            require(
                frozen.get((RESEARCH / name).relative_to(ROOT).as_posix()) == pin,
                "Capture retains every old V2 author expectation",
            )
        require(
            frozen.get(PRIOR_V2_LOG.relative_to(ROOT).as_posix()) == PRIOR_V2_LOG_SHA
            and frozen.get((PRIOR_V2_REVIEW / "manifest.json").relative_to(ROOT).as_posix())
            == PRIOR_V2_REVIEW_SHA,
            "Capture retains exact original log and complete release provenance",
        )
        return {"manifest": mf, "summary": summary, "outcome": outcome}
    if static_review:
        require(
            (current_static_release or mf.get("static_review_only") is True)
            and mf.get("new_test_credit") == 0,
            "Static release is not scientific evidence",
        )
        return {"manifest": mf, "summary": summary}
    outcome = read(directory / "completion_outcome.json")
    for value in (summary, outcome):
        require(
            value.get("completed") is True
            and value.get("passed") is True
            and value.get("budget_censored", False) is False
            and value.get("failed", False) is False,
            "Actual complete uncensored retained screen, not partial success",
        )
        require(
            value.get("new_test_credit") == 0
            and all(
                value.get(field) is False for field in ("full_G2", "adoption", "cost_transfer")
            ),
            "Zero credit and no financial, cost or source adoption",
        )
    require(
        outcome.get("budget_censored") is False,
        "Authoritative actual outcome explicitly records uncensored completion",
    )
    if diagnostic:
        require(
            directory == DIAGNOSTIC
            and [len(owned), len(frozen), len(external)] == [8, 716, 2842]
            and mf.get("schema") == "a14-literal-interval-diagnostic-manifest-v1"
            and mf.get("diagnostic_only") is True
            and summary.get("diagnostic_complete") is True
            and outcome.get("diagnostic_complete") is True
            and summary.get("actual_comparison_failing_indices") == [0]
            and summary.get("first_actual_comparison_failing_index") == 0
            and summary.get("fixed_angle_count") == 48
            and summary.get("finite_gain_count") == 1
            and summary.get("gain_comparison_passes") is True
            and summary.get("candidate_certificate") is False
            and summary.get("independent_audit_passed") is False
            and summary.get("source_manifest_sha256") == SOURCE_SHA
            and summary.get("failed_audit_manifest_sha256") == FAILED_SHA,
            "Actual fixed diagnostic is comparison evidence, never audit approval",
        )
        for value in (summary, outcome):
            require(
                0 <= value["process_CPU_seconds"] < 180
                and 0 <= value["wall_seconds_from_actual_process_creation"] < 600,
                "Actual bounded diagnostic terminal observations",
            )
        return {"manifest": mf, "summary": summary, "outcome": outcome}
    require(
        summary.get("scientific_screen_complete") is True
        and outcome.get("scientific_screen_complete") is True,
        "Both fixed retained outcomes completed",
    )
    for observation in (outcome["budget"], mf["terminal_budget_observation"]):
        require(
            0 <= observation["process_CPU_seconds"] < 300
            and 0 <= observation["wall_seconds"] < 900,
            "Original fixed hard terminal limits",
        )
    protocol = read(directory / "protocol.json")
    same(protocol["CPU_admission_wall_seconds"], [300, 270, 900], "Original work/hard/wall limits")
    same(
        protocol["author_sha256"],
        {
            k: v
            for k, v in (AUTHORS if directory == SOURCE else NEW_AUDIT_AUTHORS).items()
            if k.endswith(".py")
        },
        "Exact original source pair or separately released new auditor",
    )
    same(
        protocol["method_document_SHA256"],
        {
            k: v
            for k, v in AUTHORS.items()
            if k in ("A14_COSINE_FEASIBILITY_PREFLIGHT.md", "a14_cosine_feasibility_preflight.json")
        },
        "Exact immutable method pair",
    )
    require(
        protocol["primary_digits"] == 90
        and protocol["independent_digits"] == 130
        and protocol["threads"] == 1,
        "Exact original precision and single thread",
    )
    for field in ("frozen_inputs", "external_runtime_inputs"):
        for key, pin in protocol[field].items():
            budget()
            require(mf[field].get(key) == pin, "Every prepared original binding retained unchanged")
    for name, pin in (AUTHORS if directory == SOURCE else NEW_AUDIT_AUTHORS).items():
        budget()
        add(RESEARCH / name, pin)
        add(directory / "executed_code" / name, pin)
    require((directory / "RUN_STARTED.json").is_file(), "Actual single exclusive run marker")
    if directory == SOURCE:
        require(
            mf["schema"] == "a14-cosine-feasibility-terminal-manifest-v1"
            and protocol["schema"] == "a14-cosine-feasibility-protocol-v1"
            and outcome["gates_emitted"] is False
            and summary["gates_emitted"] is False,
            "Primary screen never emits a changed source",
        )
        same(protocol["fixed_rows"], list(ROWS), "Exact primary candidate identities")
        same(
            mf["historical_global_LIVE_integrity"],
            {
                "passed": False,
                "mismatch_references": 36,
                "distinct_paths": 9,
                "expected_hashes_waived": False,
            },
            "Historical global integrity remains separate and unwaived",
        )
        require(
            mf["scoped_selected_receipt_validity_separate"] is True,
            "Selected current receipt validity is not global LIVE validity",
        )
    else:
        require(
            directory == AUDIT
            and mf["schema"] == "a14-cosine-feasibility-independent-audit-manifest-v1"
            and protocol["schema"] == "a14-cosine-feasibility-independent-audit-protocol-v3"
            and protocol["operational_audit_version"] == 3
            and protocol["previous_failed_audit_credit"] == 0
            and protocol["previous_failed_audit_v2_credit"] == 0
            and protocol["only_i0_exact_analytic_authorization"] is True
            and summary["independent_audit_passed"] is True
            and outcome["independent_audit_passed"] is True,
            "Actual independent complete terminal certificate",
        )
        same(protocol["row_ids"], list(ROWS), "Exact independent candidate identities")
        require(
            protocol["source_receipt"] == SOURCE.relative_to(ROOT).as_posix()
            and protocol["source_manifest_sha256"] == SOURCE_SHA,
            "Independent packet binds the actual pinned primary terminal",
        )
        same(protocol["original_author_SHA256"], AUTHORS, "All original six remain immutable")
        same(
            protocol["original_source_author_SHA256"],
            {k: v for k, v in AUTHORS.items() if k.endswith(".py")},
            "New auditor never relabels the original source author pair",
        )
        require(
            protocol["prior_failed_audit_manifest_SHA256"] == FAILED_SHA
            and protocol["literal_diagnostic_manifest_SHA256"] == DIAGNOSTIC_SHA
            and protocol["prior_audit_v2_admission_failure_manifest_SHA256"] == PRIOR_V2_FAILURE_SHA
            and protocol["prior_audit_v2_root_review_manifest_SHA256"] == PRIOR_V2_REVIEW_SHA
            and protocol["prior_audit_v2_failed_log_SHA256"] == PRIOR_V2_LOG_SHA
            and summary["all_other_47_angles_and_gain_numerical_guards_retained"] is True,
            "Exact original failure and actual diagnostic remain strict separate prerequisites",
        )
        same(
            protocol["prior_audit_v2_author_SHA256"],
            PRIOR_V2_AUTHORS,
            "The failed V2 preparation remains separate immutable provenance",
        )
    return {"manifest": mf, "summary": summary, "protocol": protocol, "outcome": outcome}


def fraction(value):
    require(
        type(value) is list
        and len(value) == 2
        and all(type(v) is int for v in value)
        and value[1] > 0,
        "Exact rational metadata",
    )
    result = Fraction(*value)
    require([result.numerator, result.denominator] == value, "Canonical reduced rational")
    return result


def read_jsonlines(path):
    global _HASH_WORK
    budget()
    path = canonical(path)
    before = fingerprint(path)
    require(
        path.is_file() and before[2] <= 128 * 1024**2, "Bounded actual literal diagnostic stream"
    )
    parts, state, total = [], hashlib.sha256(), 0
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            budget()
            total += len(chunk)
            _HASH_WORK += len(chunk)
            require(total <= before[2] and _HASH_WORK <= MAX_HASH_WORK, "Charged diagnostic stream")
            parts.append(chunk)
            state.update(chunk)
    require(total == before[2] and fingerprint(path) == before, "Stable diagnostic stream bytes")
    key = path.relative_to(ROOT).as_posix()
    observed = state.hexdigest()
    require(
        _FROZEN.get(key) == observed and (path not in _OBSERVED or _OBSERVED[path] == observed),
        "Literal stream belongs to the actual sealed independent owned map",
    )
    _OBSERVED[path], _HASH_CACHE[path] = observed, (before, observed)
    data = b"".join(parts)
    budget()
    lines = data.splitlines()
    require(len(lines) == 49 and data.endswith(b"\n"), "Exactly48 angles and one gain record")
    rows = []
    for line in lines:
        budget()
        rows.append(json.loads(line))
    budget()
    return rows


def literal_evidence():
    diagnostic = read(DIAGNOSTIC / "angle_gain_diagnostics.json")
    literal = read(SOURCE / "cordic_literals.json")
    saved = diagnostic["angle_rows"]
    require(
        len(saved) == 48
        and [row["i"] for row in saved] == list(range(48))
        and diagnostic["actual_comparison_failing_indices"] == [0]
        and saved[0]["primary_contains_independent130"] is False
        and saved[0]["independent130_error_no_greater_than_saved"] is True
        and all(row["original_guard_comparison_passes"] is True for row in saved[1:])
        and diagnostic["reciprocal_gain"]["original_guard_comparison_passes"] is True,
        "Actual diagnostic identifies only exact-endpoint angle0 nesting",
    )
    stream = read_jsonlines(AUDIT / "cordic_literal_authorization_diagnostics.jsonl")
    for index, row in enumerate(stream[:48]):
        budget()
        old = saved[index]
        require(
            row["schema"] == "a14-cordic-literal-authorization-diagnostic-v2"
            and row["literal_kind"] == "angle"
            and row["i"] == index
            and row["scientific_row_authorized"] is False
            and row["new_test_credit"] == 0,
            "Exact per-angle metadata attaches before the new audit guard",
        )
        same(row["primary"], literal["angle_rows"][index], "Original primary literal immutable")
        own = row["independent_130"]
        same(
            own["true_turns_enclosure"],
            old["independent130_endpoints"],
            "Fresh independent saved endpoints match actual bounded diagnostic",
        )
        same(
            own["actual_abs_error_upper"],
            old["independent130_abs_error_upper"],
            "Fresh independent saved error matches diagnostic exact rational",
        )
        require(
            own["i"] == index
            and own["raw"] == old["raw"]
            and row["numerical_interval_inclusion"] is old["primary_contains_independent130"]
            and row["numerical_absolute_error_authorization"]
            is old["independent130_error_no_greater_than_saved"],
            "All original numerical diagnostic booleans retained without alteration",
        )
        if index == 0:
            exact = old["exact_analytic_a0_identity_diagnostic"]
            require(
                row["exact_analytic_first_angle_used"] is True
                and row["exact_analytic_first_angle_authorized"] is True
                and fraction(row["analytic_true_turns"]) == Fraction(1, 8)
                and fraction(row["analytic_actual_literal_error_upper"]) == 0
                and own["raw"] == (1 << 56) // 8
                and exact["actual_raw_equals_Q_over8"] is True
                and exact["primary_contains_exact_point"] is True
                and exact["independent130_contains_exact_point"] is True
                and fraction(exact["exact_literal_error"]) == 0
                and row["analytic_identity"] == "atan2(1,1)/(2*pi)=1/8",
                "Only exact1/8 mathematical witness substitutes the angle0 nesting requirement",
            )
        else:
            require(
                row["exact_analytic_first_angle_used"] is False
                and row["exact_analytic_first_angle_authorized"] is False
                and row["numerical_interval_inclusion"] is True
                and row["numerical_absolute_error_authorization"] is True,
                "Every other literal retains the original numerical guard",
            )
    gain = stream[-1]
    old_gain = diagnostic["reciprocal_gain"]
    same(gain["primary"], literal["gain_reciprocal"], "Original primary gain literal immutable")
    same(
        gain["independent_130"]["true_reciprocal_gain_enclosure"],
        old_gain["independent130_endpoints"],
        "Actual independent gain endpoints match diagnostic",
    )
    same(
        gain["independent_130"]["actual_abs_error_upper"],
        old_gain["independent130_abs_error_upper"],
        "Actual independent gain error matches diagnostic",
    )
    require(
        gain["literal_kind"] == "gain"
        and gain["exact_analytic_first_angle_used"] is False
        and gain["numerical_interval_inclusion"] is True
        and gain["numerical_absolute_error_authorization"] is True
        and gain["scientific_row_authorized"] is False
        and gain["new_test_credit"] == 0,
        "Finite gain keeps its original strict numerical authorization",
    )
    return {
        "exact_angle0_witness_only": True,
        "remaining47_and_gain_numeric_guards": True,
        "full49_literal_records_attached": True,
        "new_math_or_approval_from_ROOT_helper": False,
    }


def diagnostic_projection(value):
    """Project only rejected free-text; every successful numeric/SHA field stays exact."""
    budget()
    if type(value) is dict:
        rejected = value.get("resource_rejected") is True or (
            value.get("resource_contract_passed") is False and value.get("rejected") is True
        )
        if rejected:
            require(
                value.get("no_cost_or_contract_claim") is True
                and type(value.get("reason")) is str
                and value["reason"],
                "Independent rejection carries diagnostics but no numerical resource claim",
            )
        return {
            key: diagnostic_projection(item)
            for key, item in value.items()
            if not rejected or key not in ("reason", "error_type")
        }
    if type(value) is list:
        return [diagnostic_projection(item) for item in value]
    return value


def retained_rows(source, audit):
    frontier = read(SOURCE / "fixed_frontier.json")
    independent = read(AUDIT / "independent_fixed_frontier.json")
    require(
        frontier["schema"] == "a14-fixed-cosine-frontier-v1"
        and independent["schema"] == "a14-independent-fixed-cosine-frontier-v1",
        "Canonical two-row frontier artifacts",
    )
    same([row["row_id"] for row in frontier["rows"]], list(ROWS), "Exactly two fixed outcomes")
    same(independent["rows"], frontier["rows"], "Actual independent authorization of each outcome")
    resources = read(SOURCE / "resource_estimates.json")
    require(
        resources["schema"] == "a14-symbolic-source-resource-estimates-v1"
        and set(resources["rows"]) == set(ROWS),
        "Exactly the two resource recipes",
    )
    binding = read(SOURCE / "source_binding.json")
    require(
        binding["schema"] == "a14-original-cosine-source-binding-v1"
        and set(binding["cases"]) == {"B4x12", "B8x52"},
        "Actual two-source binding",
    )
    same(
        diagnostic_projection(read(AUDIT / "independent_source_binding.json")),
        diagnostic_projection(binding),
        "Independent exact source membership and selected profiles",
    )
    original_error = fraction(binding["existing_E_old"]["cosine_error_upper"])
    radius = fraction(binding["existing_E_old"]["pinned_native_radius_upper"])
    require(original_error > 0 and radius > 0, "Pinned actual component comparison metadata")
    eligible = []
    statuses = {}
    for index, row in enumerate(frontier["rows"]):
        budget()
        name = row["row_id"]
        prefix = "cordic" if index == 0 else "taylor6"
        uniform = read(SOURCE / (prefix + "_uniform_certificate.json"))
        native = read(SOURCE / (prefix + "_native_safety.json"))
        proof = read(AUDIT / (name + ".json"))
        same(proof["decision"], row, "Independent evidence attaches to this exact retained row")
        for field in (
            "uniform_certificate_passed",
            "native_safety_passed",
            "resource_contract_passed",
            "E_at_most_E_old",
            "improvement_on_both_sources",
            "within_caps",
            "component_screen_eligible",
        ):
            require(type(row[field]) is bool, "Explicit boolean component decision")
        require(
            all(row[field] is False for field in ("full_G2", "adoption", "cost_transfer"))
            and row["whole_financial_G2_proof_still_required"] is True,
            "Component comparison is not changed-source financial or physical acceptance",
        )
        require(
            uniform["passed"] is row["uniform_certificate_passed"]
            and native["passed"] is row["native_safety_passed"],
            "Retained outcome matches exact emitted component artifacts",
        )
        if row["uniform_certificate_passed"]:
            error = fraction(uniform["cosine_error_upper"])
            require(
                error >= 0
                and fraction(row["uniform_error_upper"]) == error
                and row["E_at_most_E_old"] is (error <= original_error)
                and fraction(row["conditional_remaining_coordinate_error_upper"])
                == radius * error + Fraction(1, 1 << 40),
                "Exact pay-once component metadata",
            )
        else:
            require(
                uniform["rejected"] is True
                and "cosine_error_upper" not in uniform
                and row["uniform_error_upper"] is None
                and row["conditional_remaining_coordinate_error_upper"] is None
                and row["E_at_most_E_old"] is False,
                "Rejected premise has no uniform bound",
            )
        resource = resources["rows"][name]
        require(
            resource["resource_contract_passed"] is row["resource_contract_passed"],
            "Exact resource-contract decision",
        )
        if not row["native_safety_passed"]:
            require(
                native["rejected"] is True
                and native["native_arithmetic_safety_claim"] is False
                and resource["cases"] == {}
                and resource["resource_contract_passed"] is False,
                "Physical native rejection carries no safety or resource credit",
            )
        else:
            same(
                proof["complete_plan_native_safety"],
                native["complete_recipe_certificate"],
                "Independent evidence attaches to every actual eager native bound",
            )
        same(
            diagnostic_projection(proof["independent_resource_estimates"]),
            diagnostic_projection(resource["cases"]),
            "Independent evidence attaches to all exact successful resource components",
        )
        if row["native_safety_passed"] and row["resource_contract_passed"]:
            require(set(resource["cases"]) == {"B4x12", "B8x52"}, "Both original resource sources")
            improved = all(
                case["whole_source"]["comparison_with_both_original_T_and_matched_serial_depth"]
                for case in resource["cases"].values()
            )
            within = all(case["whole_source"]["within_caps"] for case in resource["cases"].values())
            require(
                row["improvement_on_both_sources"] is improved and row["within_caps"] is within,
                "Both-source cost/cap evidence attaches exactly",
            )
        elif row["native_safety_passed"]:
            require(
                set(resource["cases"]) == {"B4x12", "B8x52"}
                and any(
                    case["resource_contract_passed"] is False for case in resource["cases"].values()
                )
                and row["improvement_on_both_sources"] is False
                and row["within_caps"] is False,
                "Missing used contract remains resource rejection",
            )
        eligibility = all(
            row[field]
            for field in (
                "E_at_most_E_old",
                "native_safety_passed",
                "resource_contract_passed",
                "improvement_on_both_sources",
                "within_caps",
            )
        )
        status = (
            "NATIVE_REJECTED"
            if not row["native_safety_passed"]
            else "UNIFORM_REJECTED"
            if not row["E_at_most_E_old"]
            else "RESOURCE_REJECTED"
            if not eligibility
            else "COMPONENT_SCREEN_PASS"
        )
        require(
            row["component_screen_eligible"] is eligibility and row["status"] == status,
            "Scientific screen completeness and row eligibility remain separate",
        )
        statuses[name] = status
        if eligibility:
            eligible.append(name)
    same(source["summary"]["component_screen_eligible_rows"], eligible, "Primary eligible subset")
    same(audit["summary"]["component_eligible_rows"], eligible, "Independent eligible subset")
    require(
        eligible == [] and statuses == {ROWS[0]: "RESOURCE_REJECTED", ROWS[1]: "UNIFORM_REJECTED"},
        "Actual unchanged source retained two meaningful rejections without a selected candidate",
    )
    require(
        source["summary"]["at_most_one_later_production_candidate_external_ROOT_release_required"]
        is True
        and frontier["financial_bridge_open"] is True
        and frontier["actual_root_total_map_authorization_still_required_before_production"] is True
        and frontier["changed_source_not_emitted"] is True
        and frontier["new_fixture_credit"] == 0,
        "No automatic future emission or adoption",
    )
    return {
        "retained_statuses": statuses,
        "component_eligible_rows": eligible,
        "scientific_screen_complete": True,
        "production_authorized": False,
        "changed_source_financial_G2_certified": False,
        "cost_transfer": False,
        "adoption": False,
    }


def fresh_union():
    runtime_scopes()
    for lexical, (previous, _) in tuple(_PATH_CACHE.items()):
        budget()
        require(
            canonical(lexical, fresh=True) == previous, "Fresh original lexical alias unchanged"
        )
    union = {}
    for mapping in (_FROZEN, _EXTERNAL):
        for member, expected in mapping.items():
            budget()
            path = Path(member) if Path(member).is_absolute() else ROOT / member
            require(
                path not in union or union[path] == expected, "Equal-SHA unique full input union"
            )
            union[path] = expected
    for path, observed in tuple(_OBSERVED.items()):
        budget()
        require(
            path not in union or union[path] == observed, "Actual and expected SHA remain separate"
        )
        union[path] = observed
    total = 0
    for original, expected in sorted(union.items()):
        budget()
        actual = canonical(original, fresh=True)
        total += actual.stat().st_size
        require(
            len(union) <= MAX_REFERENCES and total <= MAX_UNIQUE_BYTES,
            "Fixed full unique union count/byte caps",
        )
        require(
            digest(actual, fresh=True, already_resolved=True) == expected,
            "Every complete unique union member freshly hashed",
        )
    for directory, expected in _OWN_INVENTORIES.items():
        budget()
        if directory == FAILED:
            require(
                not (directory / "FAILED_UNSEALED.json").exists(),
                "Original failed audit stays sealed and cannot be promoted",
            )
        else:
            no_failure(directory)
        require(inventory(directory) == expected, "Final original owned inventory unchanged")
    require(
        standard_runtime_members() == _STANDARD_RUNTIME_MEMBERS,
        "Complete captured reachable standard runtime membership unchanged",
    )
    require(not any(path.exists() for path in _ABSENT_RUNTIME), "Absent interpreter zip unchanged")
    require(not PRIOR_V2_AUDIT.exists(), "The original V2 preparation still has no receipt")
    return {
        "unique_paths": len(union),
        "unique_bytes": total,
        "full_fresh_resolve_and_hash": True,
        "expected_hashes_waived": False,
    }


def write(name, value):
    budget()
    data = (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()
    budget()
    require(len(data) <= MAX_OWN_BYTES, "Bounded own metadata output")
    with (OUTPUT / name).open("xb") as stream:
        for offset in range(0, len(data), 1 << 20):
            budget()
            stream.write(data[offset : offset + (1 << 20)])
            budget()


def copy_input(path, name):
    actual = canonical(path)
    expected, before = digest(actual), fingerprint(actual)
    with actual.open("rb") as incoming, (OUTPUT / name).open("xb") as outgoing:
        while chunk := incoming.read(1 << 20):
            budget()
            outgoing.write(chunk)
            budget()
    require(
        fingerprint(actual) == before and digest(OUTPUT / name) == expected,
        "Exclusive immutable source copy",
    )


def emergency_failure(error):
    if not OUTPUT.is_dir():
        return
    try:
        budget()
        require(
            not (OUTPUT / "manifest.json").exists()
            and not (OUTPUT / "completion_outcome.json").exists(),
            "Partial terminal blocks failure resealing",
        )
        write(
            "failure.json",
            {
                "failed": True,
                "passed": False,
                "completed": False,
                "error_type": type(error).__name__,
                "error": str(error),
                "process_CPU_seconds": time.process_time(),
                "wall_seconds": time.monotonic() - _STARTED,
                "new_test_credit": 0,
                "full_G2": False,
                "adoption": False,
            },
        )
    except BaseException:
        pass
    try:
        with (OUTPUT / "FAILED_UNSEALED.json").open("xb") as stream:
            stream.write(
                b'{"failed":true,"passed":false,"completed":false,"budget_censored":null,"hard_budget_state_uncertified":true,"partial_summary_or_manifest_is_not_terminal_success":true,"new_test_credit":0,"full_G2":false,"adoption":false,"requires_fresh_version_and_receipt":true}\n'
            )
    except OSError:
        pass


def main():
    global _STARTED, AUDIT_SHA, NEW_REVIEW_SHA
    _STARTED = process_started()
    budget()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-manifest-sha256", required=True)
    parser.add_argument("--root-release-manifest-sha256", required=True)
    args = parser.parse_args()
    AUDIT_SHA = args.audit_manifest_sha256
    require(
        args.root_release_manifest_sha256 == NEW_REVIEW_SHA,
        "ROOT-supplied release expected hash equals the already issued exact static pin",
    )
    runtime_scopes()
    require(
        canonical(Path(__file__)) == AUTHOR and not OUTPUT.exists(),
        "Exact new verifier and fresh receipt, no retry",
    )
    require(
        canonical_sha(SOURCE_SHA)
        and canonical_sha(AUDIT_SHA)
        and canonical_sha(NEW_REVIEW_SHA)
        and all(canonical_sha(value) for value in NEW_AUDIT_AUTHORS.values()),
        "Actual audit003 PASS and new ROOT release expected pins must be supplied by ROOT",
    )
    try:
        runtime = own_runtime()
        add(ORIGIN, ORIGIN_SHA)
        for name, pin in AUTHORS.items():
            add(RESEARCH / name, pin)
        for name, pin in NEW_AUDIT_AUTHORS.items():
            add(RESEARCH / name, pin)
        for name, pin in PRIOR_V2_AUTHORS.items():
            add(RESEARCH / name, pin)
        add(PRIOR_V2_LOG, PRIOR_V2_LOG_SHA)
        source = packet(SOURCE, SOURCE_SHA)
        audit = packet(AUDIT, AUDIT_SHA)
        packet(FAILED, FAILED_SHA, failed=True)
        packet(DIAGNOSTIC, DIAGNOSTIC_SHA, diagnostic=True)
        capture = packet(PRIOR_V2_FAILURE, PRIOR_V2_FAILURE_SHA, capture=True)
        prior_release = packet(PRIOR_V2_REVIEW, PRIOR_V2_REVIEW_SHA, static_review=True)
        require(
            prior_release["summary"]["schema"]
            == "root-a14-cosine-independent-audit-static-READY-v2"
            and prior_release["summary"].get("passed") is True
            and prior_release["summary"].get("ready") is True
            and _PACKETS[PRIOR_V2_REVIEW.name]["owned"] == 1
            and _PACKETS[PRIOR_V2_REVIEW.name]["frozen_inputs"] == 7
            and _PACKETS[PRIOR_V2_REVIEW.name]["external_runtime_inputs"] == 0,
            "Original V2 release stays preserved static evidence despite pre-mkdir failure",
        )
        for name, pin in PRIOR_V2_AUTHORS.items():
            budget()
            require(
                prior_release["manifest"]["frozen_inputs"].get(
                    (RESEARCH / name).relative_to(ROOT).as_posix()
                )
                == pin,
                "Original V2 ROOT release retains every exact original author pin",
            )
        for name, pin in REVIEWS.items():
            packet(PROGRAM / name, pin, static_review=True)
        release = packet(PROGRAM / NEW_REVIEW_NAME, NEW_REVIEW_SHA, static_review=True)
        require(
            release["summary"]["schema"] == "root-a14-cosine-independent-audit-static-READY-v3"
            and release["summary"].get("passed") is True
            and release["summary"].get("ready") is True
            and release["summary"].get("actual_new_release_pins_PASS") is True
            and release["summary"].get("independent_text_peer_PASS") is True
            and release["summary"].get("actual_V2_failure_diagnostic_integrity_PASS") is True
            and release["summary"].get("static_release_runtime_reaudit_claim") is False
            and release["summary"].get("new_fixture_credit") == 0
            and release["summary"].get("full_G2") is False
            and release["summary"].get("adoption") is False
            and _PACKETS[NEW_REVIEW_NAME]["owned"] == 1
            and _PACKETS[NEW_REVIEW_NAME]["frozen_inputs"] == 12
            and _PACKETS[NEW_REVIEW_NAME]["external_runtime_inputs"] == 0,
            "New audit-only external ROOT release remains static evidence",
        )
        require(
            release["summary"]["capture_manifest_SHA256"] == PRIOR_V2_FAILURE_SHA
            and release["manifest"]["frozen_inputs"].get(
                (PRIOR_V2_FAILURE / "manifest.json").relative_to(ROOT).as_posix()
            )
            == PRIOR_V2_FAILURE_SHA
            and release["manifest"]["frozen_inputs"].get(
                (PRIOR_V2_REVIEW / "manifest.json").relative_to(ROOT).as_posix()
            )
            == PRIOR_V2_REVIEW_SHA,
            "Issued V3 release retains the complete original V2 failure and static release",
        )
        same(
            release["summary"]["capture_owned_frozen_external_counts"],
            [5, 54, 2842],
            "Exact actual V2 failed-preparation capture scope",
        )
        for key, pin in prior_release["manifest"]["frozen_inputs"].items():
            budget()
            require(
                release["manifest"]["frozen_inputs"].get(key) == pin,
                "Every original V2 release reference remains strict in V3 release",
            )
        for name, pin in NEW_AUDIT_AUTHORS.items():
            require(
                release["manifest"]["frozen_inputs"].get(
                    (RESEARCH / name).relative_to(ROOT).as_posix()
                )
                == pin,
                "New ROOT static release binds every exact reviewed audit-only byte",
            )
        budget(admission=True)
        OUTPUT.mkdir()
        copy_input(AUTHOR, "executed_verifier.py")
        copy_input(ORIGIN, "copied_pattern_origin.py")
        first = fresh_union()
        budget(admission=True)
        scope = retained_rows(source, audit)
        literals = literal_evidence()
        loaded_origins()
        second = fresh_union()
        budget()
        outcome = {
            "schema": "a14-cosine-feasibility-fresh-root-integrity-v3",
            "passed": True,
            "completed": True,
            "budget_censored": False,
            "receipt_integrity_only": True,
            "scientific_proof_or_sourcewalk_reexecuted": False,
            "primary_manifest_sha256": SOURCE_SHA,
            "audit_manifest_sha256": AUDIT_SHA,
            "exact_author_sha256": AUTHORS,
            "static_review_manifest_sha256": REVIEWS,
            "new_audit_author_sha256": NEW_AUDIT_AUTHORS,
            "new_audit_static_review_manifest_sha256": NEW_REVIEW_SHA,
            "expected_future_manifest_pins_supplied_by_root_CLI": True,
            "old_failed_audit_manifest_sha256": FAILED_SHA,
            "actual_angle_diagnostic_manifest_sha256": DIAGNOSTIC_SHA,
            "old_audit_v2_pre_mkdir_failure_capture_manifest_sha256": PRIOR_V2_FAILURE_SHA,
            "old_audit_v2_static_review_manifest_sha256": PRIOR_V2_REVIEW_SHA,
            "old_audit_v2_author_sha256": PRIOR_V2_AUTHORS,
            "old_audit_v2_failure_capture_scope": {
                "diagnostic_integrity": capture["summary"]["diagnostic_integrity"],
                "original_attempt_failed": True,
                "original_intended_receipt_absent": True,
                "scientific_execution": False,
                "new_test_credit": 0,
            },
            "original_failed_audit_remains_failed": True,
            "literal_diagnostic_evidence": literals,
            "source_screen_validity_and_component_eligibility_separate": True,
            "retained_component_scope": scope,
            "first_fresh_union": first,
            "second_fresh_union": second,
            "runtime_inventory": runtime,
            "new_test_credit": 0,
            "new_gate_replays": 0,
            "full_G2": False,
            "cost_transfer": False,
            "adoption": False,
            "gates_emitted": False,
            "original_expected_hashes_waived": False,
            "CPU_admission_wall_limits": [CPU, ADMISSION, WALL],
            "process_CPU_seconds": time.process_time(),
            "wall_seconds": time.monotonic() - _STARTED,
        }
        write("summary.json", outcome)
        write("completion_outcome.json", outcome)
        owned = inventory(OUTPUT)
        require(
            len(owned) <= MAX_OWN_FILES
            and sum(path.stat().st_size for path in owned) <= MAX_OWN_BYTES,
            "Fixed own 64-file/128MiB cap",
        )
        files = {}
        for path in sorted(owned):
            budget()
            files[path.relative_to(OUTPUT).as_posix()] = digest(path, fresh=True)
        write(
            "manifest.json",
            {
                "schema": "a14-cosine-feasibility-root-integrity-manifest-v3",
                "files": files,
                "frozen_inputs": _FROZEN,
                "external_runtime_inputs": _EXTERNAL,
                "manifest_self_hash_excluded": True,
                "completed": True,
                "passed": True,
                "budget_censored": False,
                "new_test_credit": 0,
                "verification_and_output_hashing_before_terminal": True,
                "terminal_outcome_file": "completion_outcome.json",
                "terminal_budget_observation": {
                    "process_CPU_seconds": time.process_time(),
                    "wall_seconds": time.monotonic() - _STARTED,
                },
                "original_expected_hashes_waived": False,
            },
        )
        budget()
    except BaseException as error:
        emergency_failure(error)
        raise


if __name__ == "__main__":
    main()
