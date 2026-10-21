"""Root-authorized stdlib-only metadata preservation of actual V2 pre-mkdir failure.

No cosine module, scientific import, source walker, bounds, gates or proof run.
Current capture runtime provenance is separate from original attempt provenance.
Fixed180CPU/150admission/600wall,64ownedfiles/128MiB,zero scientific credit.
"""

import ast
import ctypes
from ctypes import wintypes
import hashlib
import json
import os
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
PROGRAM = ROOT / "results/limitation_program_20261001"
AUTHOR = RESEARCH / "capture_cosine_audit_admission_failure_v1.py"
OUTPUT = PROGRAM / "A14_cosine_audit_admission_failure_run002"
FAILED = PROGRAM / "A14_cosine_feasibility_audit_run002"
RELEASE = PROGRAM / "A14_cosine_feasibility_audit_root_review_run002"
RELEASE_SHA = "a2edeb0d4bbf41b2ec2f3591d5ace657c935682b980499dfbf8850118b323051"
LOG = ROOT / ".context/a14_cosine_audit_prepare_run002.log"
LOG_SHA = "1b3886341ff468441b9b6b018883778b3ab573721bcfab7d74b575625212f647"
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
GOOD = "7511709f30647a2dd6aa6b277ae38ddedf7c81cb975c9eac2dd1d70415d3d059"
BAD = "7511709f30647a2dd6aa6b277ae38ddeddf7c81cb975c9eac2dd1d70415d3d059"
ORIGINAL = {
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
CPU, ADMISSION, WALL = 180, 150, 600
MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = 24000, 2 * 1024**3
MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK = 100000, 8 * 1024**3, 24 * 1024**3
MAX_OWN_FILES, MAX_OWN_BYTES = 64, 128 * 1024**2
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


def raw_bytes(path, maximum):
    global _HASH_WORK
    budget()
    actual = canonical(path)
    before, total, state, parts = fingerprint(actual), 0, hashlib.sha256(), []
    require(actual.is_file() and before[2] <= maximum, "Finite original metadata/source bytes")
    with actual.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            budget()
            total += len(chunk)
            _HASH_WORK += len(chunk)
            require(total <= before[2] and _HASH_WORK <= MAX_HASH_WORK, "Charged stable raw reads")
            state.update(chunk)
            parts.append(chunk)
    observed = state.hexdigest()
    require(
        total == before[2]
        and fingerprint(actual) == before
        and _FROZEN.get(actual.relative_to(ROOT).as_posix()) == observed,
        "Every parsed metadata byte belongs to the preserved SHA map",
    )
    require(actual not in _OBSERVED or _OBSERVED[actual] == observed, "Unchanged observed bytes")
    _OBSERVED[actual], _HASH_CACHE[actual] = observed, (before, observed)
    budget()
    return b"".join(parts)


def release_inputs():
    manifest_path = add(RELEASE / "manifest.json", RELEASE_SHA)
    manifest = read(manifest_path)
    require(
        manifest.get("manifest_self_hash_excluded") is True
        and manifest.get("completed") is True
        and manifest.get("passed") is True
        and manifest.get("static_review_only") is True
        and manifest.get("budget_censored") is False,
        "Exact original static release, never scientific approval",
    )
    require(
        [
            len(manifest.get(field, {}))
            for field in ("files", "frozen_inputs", "external_runtime_inputs")
        ]
        == [1, 7, 0],
        "All exact V2 release maps retained",
    )
    members = {manifest_path}
    for key, expected in manifest["files"].items():
        budget()
        require(
            type(key) is str
            and "\\" not in key
            and not Path(key).is_absolute()
            and ".." not in Path(key).parts,
            "Canonical original owned ROOT key",
        )
        actual = add(ROOT / key, expected)
        require(
            actual.is_relative_to(RELEASE)
            and actual.relative_to(ROOT).as_posix() == key
            and actual not in members,
            "Exact original owned release route",
        )
        members.add(actual)
    for key, expected in manifest["frozen_inputs"].items():
        budget()
        require(
            type(key) is str
            and "\\" not in key
            and not Path(key).is_absolute()
            and ".." not in Path(key).parts,
            "Canonical original ROOT frozen key",
        )
        actual = add(ROOT / key, expected)
        require(
            actual.relative_to(ROOT).as_posix() == key, "No original metadata path substitution"
        )
    require(inventory(RELEASE) == members, "Exact complete actual static release inventory")
    _OWN_INVENTORIES[RELEASE] = members
    for name, pin in ORIGINAL.items():
        require(
            manifest["frozen_inputs"].get((RESEARCH / name).relative_to(ROOT).as_posix()) == pin,
            "All three executed V2 author bytes remain original expected-SHA inputs",
        )
        add(RESEARCH / name, pin)
    summary = read(RELEASE / "summary.json")
    require(
        summary["schema"] == "root-a14-cosine-independent-audit-static-READY-v2"
        and summary["ready"] is True
        and summary["passed"] is True
        and summary["new_three_author_pins_frozen"] is True
        and summary["new_test_credit"] == 0,
        "Actual V2 static release preserved without promotion",
    )
    add(LOG, LOG_SHA)
    return manifest


def failure_observation():
    source = raw_bytes(RESEARCH / "audit_cosine_feasibility_v2.py", 2 * 1024**2)
    tree = ast.parse(source)
    budget()
    values = [
        node.value.value
        for node in tree.body
        if isinstance(node, ast.Assign)
        and isinstance(node.value, ast.Constant)
        and any(
            isinstance(target, ast.Name) and target.id == "LITERAL_DIAGNOSTIC_REVIEW_SHA256"
            for target in node.targets
        )
    ]
    require(
        values == [BAD] and len(BAD) == 65 and len(GOOD) == 64,
        "Actual immutable faulty constant, not an inferred alternate source",
    )
    policy = read(RESEARCH / "a14_cosine_feasibility_audit_implementation_preflight_v2.json")
    require(
        policy["literal_diagnostic_root_review_manifest_SHA256"] == GOOD,
        "Exact original policy pin differs from faulty source constant",
    )
    log = raw_bytes(LOG, 2 * 1024**2).decode("utf-8-sig")
    require(
        "ValueError: Exact audit-only source, prior failure and fresh route" in log
        and "implementation_policy" in log
        and "prepare(args.output.resolve())" in log,
        "Exact actual pre-mkdir preparation failure log, not a scientific result",
    )
    require(not FAILED.exists(), "Original intended audit002 truly absent")
    return dict(
        schema="a14-cosine-audit-pre-mkdir-admission-failure-v2",
        passed=False,
        failed=True,
        diagnostic_integrity=True,
        original_attempt_failed=True,
        intended_receipt=FAILED.relative_to(ROOT).as_posix(),
        intended_receipt_absent=True,
        no_original_protocol_receipt_or_math_result=True,
        scientific_execution=False,
        original_attempt_CPU_wall_not_recorded=True,
        original_bad_review_SHA256=BAD,
        exact_required_review_SHA256=GOOD,
        original_bad_constant_length=65,
        exact_required_constant_length=64,
        error_type="ValueError",
        error="Exact audit-only source, prior failure and fresh route",
        actual_failed_prepare_log=LOG.relative_to(ROOT).as_posix(),
        actual_failed_prepare_log_SHA256=LOG_SHA,
        prior_audit_v2_author_SHA256=ORIGINAL,
        prior_audit_v2_root_review_manifest_SHA256=RELEASE_SHA,
        original_six_and_primary_source_unchanged=True,
        original_source_or_audit_replayed=False,
        new_test_credit=0,
        full_G2=False,
        adoption=False,
        cost_transfer=False,
    )


def emergency_failure(error):
    if not OUTPUT.is_dir():
        return
    try:
        with (OUTPUT / "FAILED_UNSEALED.json").open("xb") as stream:
            stream.write(
                b'{"failed":true,"passed":false,"completed":false,"diagnostic_integrity":false,"budget_censored":null,"hard_budget_state_uncertified":true,"partial_manifest_is_invalid":true,"scientific_execution":false,"new_test_credit":0}\n'
            )
    except OSError:
        pass


def main():
    global _STARTED
    _STARTED = process_started()
    runtime_scopes()
    require(
        sys.argv[1:] == []
        and canonical(__file__) == AUTHOR
        and not OUTPUT.exists()
        and not FAILED.exists(),
        "Exact fresh capture, no retry or scope override",
    )
    try:
        add(AUTHOR, digest(AUTHOR))
        release_inputs()
        runtime = own_runtime()
        observation = failure_observation()
        first = fresh_union()
        budget(admission=True)
        OUTPUT.mkdir()
        copy_input(AUTHOR, "executed_capture.py")
        copy_input(LOG, "failed_prepare.log")
        loaded_origins()
        second = fresh_union()
        require(
            not FAILED.exists(),
            "Original intended audit remains absent after full fresh verification",
        )
        observation.update(
            capture_runtime_inventory=runtime,
            capture_author_SHA256=digest(AUTHOR),
            two_fresh_full_union_passes=[first, second],
            capture_CPU_admission_wall_limits=[CPU, ADMISSION, WALL],
            capture_process_CPU_seconds=time.process_time(),
            capture_wall_seconds=time.monotonic() - _STARTED,
            capture_runtime_not_claimed_as_original_attempt_provenance=True,
        )
        write("summary.json", observation)
        write(
            "completion_outcome.json",
            dict(
                completed=True,
                passed=False,
                failed=True,
                diagnostic_integrity=True,
                original_attempt_failed=True,
                scientific_execution=False,
                budget_censored=False,
                new_test_credit=0,
                full_G2=False,
                adoption=False,
                cost_transfer=False,
                capture_process_CPU_seconds=time.process_time(),
                capture_wall_seconds=time.monotonic() - _STARTED,
            ),
        )
        owned = inventory(OUTPUT)
        require(
            len(owned) <= MAX_OWN_FILES
            and sum(path.stat().st_size for path in owned) <= MAX_OWN_BYTES,
            "Fixed64 files/128MiB metadata retention",
        )
        files = {}
        for path in sorted(owned):
            budget()
            files[path.relative_to(ROOT).as_posix()] = digest(path, fresh=True)
        write(
            "manifest.json",
            dict(
                schema="a14-cosine-audit-admission-failure-manifest-v2",
                files=files,
                frozen_inputs=_FROZEN,
                external_runtime_inputs=_EXTERNAL,
                manifest_self_hash_excluded=True,
                completed=True,
                passed=False,
                failed=True,
                diagnostic_integrity=True,
                original_attempt_failed=True,
                budget_censored=False,
                original_expected_hashes_waived=False,
                scientific_execution=False,
                new_test_credit=0,
            ),
        )
        budget()
    except BaseException as error:
        emergency_failure(error)
        raise


if __name__ == "__main__":
    main()
