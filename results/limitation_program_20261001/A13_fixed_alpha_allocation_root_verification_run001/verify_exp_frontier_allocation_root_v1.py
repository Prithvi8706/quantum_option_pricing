"""Fresh fixed-alpha receipt integrity only; no scientific import or evaluation.

Prospective fixed120 process CPU/90 work admission/600 wall, one thread,
24k runtime files/2GiB,100k references/8GiB union/24GiB byte hashing.
Architecture copied from immutable verify_original_bm_g2_root_v1.py,
SHA a739ba6fc86633776a7f771768b96c730d68a900dc6664cf11913da0e66b1ddf.
Root executes this NEW file only after static review and exact-byte freezing.
"""

import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
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
OUTPUT = PROGRAM / "A13_fixed_alpha_allocation_root_verification_run001"
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
SOURCE = PROGRAM / "A13_fixed_alpha_allocation_run001"
AUDIT = PROGRAM / "A13_fixed_alpha_allocation_audit_run001"
FAILED = PROGRAM / "A02_BM_native_financial_bridge_run001"
ORIGIN = RESEARCH / "verify_original_bm_g2_root_v1.py"
ORIGIN_SHA = "a739ba6fc86633776a7f771768b96c730d68a900dc6664cf11913da0e66b1ddf"
SOURCE_SHA = "4c863e4a031a458c5a424c75774f791f49c25c9c25e030a6fd28e5e8ec91236f"
AUDIT_SHA = "829712c9c71925ba74e98059a294c99c812fe659fd0b31a44c50ef35c6b31358"
CPU, ADMISSION, WALL = 120, 90, 600
MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = 24000, 2 * 1024**3
MAX_REFERENCES, MAX_UNIQUE_BYTES, MAX_HASH_WORK = 100000, 8 * 1024**3, 24 * 1024**3
AUTHORS = {
    "A13_FIXED_RELATIVE_ENVELOPE_ALLOCATION_PREFLIGHT.md": (
        "b93d4eccd355eb4169086596348f25158d35d76ed506af0dfe9f862a7fee6145"
    ),
    "a13_fixed_relative_envelope_allocation_preflight.json": (
        "4c5fa041a3da20da4ccfc93b943643a6c190a3804895347d4c8a4f788e9dd33e"
    ),
    "experiment_exp_frontier_allocation.py": (
        "2dd11428fa4bb09d0b0612771187e3abcd12075960db7b87e9326f9b03355aff"
    ),
    "audit_exp_frontier_allocation.py": (
        "c239a3379b3e78e7549607532d05f492254bf471fbb5c8c064e2d993d691fe0f"
    ),
    "EXP_FRONTIER_ALLOCATION_IMPLEMENTATION_PREFLIGHT.md": (
        "67fa898a7d6977b2719a30cc735bd6f1c2e2eb1842364bab544220973b3fffc0"
    ),
    "exp_frontier_allocation_implementation_preflight.json": (
        "c51d12707595cd9636f576cbe57ff84bf88c6f1c05d42da0abc7776fe91a9188"
    ),
}
READY_PINS = {
    "A13_fixed_alpha_allocation_ROOT_READY_run001.json": (
        "3e32c0c85eb4e53f16008085380686dfef65f6a4a28e1f983d18efbd4f84c277"
    ),
    "A13_fixed_alpha_allocation_AUDIT_READY_run001.json": (
        "546077ddfc6fe7ad5a1d7586b1d5ecb085cb55cc4c66f06a9c945ddd1e7d41d1"
    ),
}
PREREQUISITES = {
    "A02_BM_native_financial_bridge_run002": (
        "78a8eea9dc937883b810cb6b3e2e26aec41297551b984a9c12bb15a435523162"
    ),
    "A02_BM_native_financial_bridge_audit_run002": (
        "62074efc3bd5a20a9cbe72b3d020fd5c6bf13e32d41b188ef57570225dade2a0"
    ),
    "A02_polar_cdf_bv_run003": "86dcd6b400233b58f62d4197127e38c6d2598c05e1903d207b0947168b326a05",
    "A02_polar_cdf_bv_audit_run003": (
        "75ed7d7d6d5b929571d64d8fa54d53f6bf146c283d18133a5d191ac612724eb9"
    ),
    "A10_coefficient_run001": "0a732d7f487bca1efd298e7eca4feb2f2d2e83d1958ebb9a14ee9b32a0d78a40",
    "E03_support_run001": "fe9ec5382ca69d570b1ec67c4c8b2e61c97de4bd354089fcb7293a2f711ae9a2",
    "E03_support_audit_run002": "f10e80022cff82caf99a1ed5237d102374fedc001cad0c1138baa3d55b626544",
    "A02_BM_native_financial_bridge_root_verification_run001": (
        "eab61f5775110021e4e514b7412ce56ca9b24aec13311e32d240dc1559cb59ab"
    ),
    "A02_BM_native_financial_bridge_run001": (
        "8beb20bfe88407479953ddd7be284fd8fe94cea1e964c392340c4ab1a2376e02"
    ),
    "A02_BM_native_financial_bridge_root_review_run001": (
        "60c5c37bed87950e555ed89e09176ce2f87a1cb3daffd481111b17572ded316c"
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


def canonical(path):
    budget()
    path = Path(path)
    lexical = Path(os.path.abspath(str(path)))
    base_site = Path(sys.base_prefix) / "Lib/site-packages"
    require(not lexical.is_relative_to(base_site), "Excluded base packages lexical path")
    actual = lexical.resolve(strict=True)
    require(not actual.is_relative_to(base_site.resolve()), "Excluded base package alias")
    require(actual == lexical, "No lexical-to-physical input alias")
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


def digest(path):
    global _HASH_WORK
    budget()
    path = canonical(path)
    require(path.is_file(), "Actual regular SHA input")
    before, total, state = fingerprint(path), 0, hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            budget()
            total += len(chunk)
            _HASH_WORK += len(chunk)
            require(_HASH_WORK <= MAX_HASH_WORK, "Fixed24GiB hashing-work cap")
            require(total <= before[2], "Input grew while hashing")
            state.update(chunk)
    require(total == before[2] and fingerprint(path) == before, "Stable actual byte hash")
    budget()
    return state.hexdigest()


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
        require(actual.is_relative_to(canonical(sys.base_prefix)), "Actual external base runtime")
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
    preserved_failure = directory == FAILED
    if not preserved_failure:
        no_failure(directory)
    mf_path = add(directory / "manifest.json", expected)
    mf = read(mf_path)
    flat = name == "A10_coefficient_run001" and "files" not in mf
    if flat:
        owned, frozen, external = mf, {}, {}
    else:
        require(mf.get("manifest_self_hash_excluded") is True, "Exact self-hash exclusion")
        owned, frozen, external = (
            mf.get(key, {})
            for key in (
                "files",
                "frozen_inputs",
                "external_runtime_inputs",
            )
        )
    require(
        type(owned) is dict and owned and type(frozen) is dict and type(external) is dict,
        "Complete recognized maps",
    )
    actual_owned = set()
    for original, expected_sha in owned.items():
        require(type(original) is str and not Path(original).is_absolute(), "Relative own key")
        key = original.replace("\\", "/")
        candidate = ROOT / key if key.startswith("results/") else directory / key
        actual = add(candidate, expected_sha)
        require(actual.is_relative_to(directory) and actual != mf_path, "Owned receipt confinement")
        require(actual not in actual_owned, "No duplicate own alias")
        actual_owned.add(actual)
        normalized = actual.relative_to(
            ROOT if key.startswith("results/") else directory
        ).as_posix()
        require(key == normalized, "Canonical own key with explicit historical slash normalization")
    for original, expected_sha in frozen.items():
        require(type(original) is str and not Path(original).is_absolute(), "ROOT frozen key")
        key = original.replace("\\", "/")
        actual = add(ROOT / key, expected_sha)
        require(
            actual.is_relative_to(ROOT) and actual.relative_to(ROOT).as_posix() == key,
            "Canonical ROOT frozen input",
        )
    for key, expected_sha in external.items():
        require(type(key) is str and Path(key).is_absolute(), "Explicit external key")
        actual = add(key, expected_sha)
        require(
            not actual.is_relative_to(ROOT) and str(actual) == key, "Canonical scoped external key"
        )
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
        require(
            expected == PREREQUISITES[FAILED.name]
            and len(owned) == 20
            and len(frozen) == 346
            and len(external) == 2842,
            "Exact historical failure maps",
        )
        require(
            mf["completed"] is False
            and mf["passed"] is False
            and outcome["completed"] is False
            and outcome["passed"] is False
            and outcome["failed"] is True
            and outcome["new_test_credit"] == 0
            and (directory / "failure.json").is_file(),
            "Preserved failure remains zero-credit failure",
        )
    else:
        if summary is not None:
            if name == "A02_BM_native_financial_bridge_root_review_run001":
                require(
                    summary["root_and_independent_mathematical_source_protocol_review_passed"]
                    is True
                    and summary["authors_frozen"] is True
                    and summary["scientific_code_or_proof_or_source_walk_executed_by_static_review"]
                    is False
                    and summary["new_fixture_credit"] == 0
                    and [len(owned), len(frozen), len(external)] == [1, 11, 0],
                    "Actual static review, not a scientific result",
                )
            else:
                require(
                    summary.get("passed") is True
                    and summary.get("budget_censored", False) is False,
                    "Successful original packet summary",
                )
            require(
                summary.get("failed", False) is False and summary.get("rejection", False) is False,
                "No failed or rejected prerequisite",
            )
        if outcome is not None:
            for value in (mf, outcome, summary):
                require(
                    type(value) is dict
                    and value.get("completed") is True
                    and value.get("passed") is True
                    and value.get("budget_censored") is False
                    and value.get("failed", False) is False
                    and value.get("rejection", False) is False,
                    "Complete uncensored terminal PASS",
                )
        no_failure(directory)
    if outcome is not None:
        limits = (
            (180, 600)
            if name
            in (
                SOURCE.name,
                AUDIT.name,
                FAILED.name,
                "A02_BM_native_financial_bridge_run002",
                "A02_BM_native_financial_bridge_audit_run002",
                "A02_polar_cdf_bv_run003",
                "A02_polar_cdf_bv_audit_run003",
            )
            else (300, 900)
        )
        for observation in (outcome["budget"], mf["terminal_budget_observation"]):
            require(
                0 <= observation["process_CPU_seconds"] < limits[0]
                and 0 <= observation["wall_seconds"] < limits[1],
                "Original terminal hard budgets",
            )
    _PACKETS[name] = {
        "files": len(owned),
        "frozen_inputs": len(frozen),
        "external_runtime_inputs": len(external),
        "preserved_failure": preserved_failure,
    }
    return summary, outcome


def fraction(value):
    require(
        type(value) is list
        and len(value) == 2
        and all(type(item) is int for item in value)
        and value[1] > 0,
        "Exact JSON rational",
    )
    result = Fraction(*value)
    require([result.numerator, result.denominator] == value, "Canonical reduced rational")
    return result


def check_release(source, audit):
    for directory, summary, digits in ((SOURCE, source, 90), (AUDIT, audit, 130)):
        outcome = read(directory / "completion_outcome.json")
        require(
            outcome["limits_CPU_work_wall"] == [180, 150, 600]
            and outcome["interval_digits"] == digits,
            "Original fixed interval/process contract",
        )
        for value in (summary, outcome):
            require(
                value["conditional_allocation_release_eligible"] is True
                and value["new_test_credit"] == 0
                and value["new_gate_replays"] == 0,
                "Eligible zero-credit terminal allocation",
            )
        require(
            summary["one_fixed_alpha_certificate_valid"] is True
            and summary["both_financial_residual_fit"] is True
            and summary["all_nonempty_allowances_strict_positive"] is True
            and summary["alpha"] == [1, 16777216],
            "One fixed-alpha valid release",
        )
        for key in (
            "exploratory_A13_held_method_or_null_fields_changed",
            "actual_candidate_G2_feasibility_established",
            "actual_fit_gate_emission_fixture_or_sourcewalk_executed",
            "full_G2",
            "adoption",
            "cost_transfer",
            "quantum_advantage",
        ):
            require(summary[key] is False, "Narrow certificate scope: " + key)
    require(
        source["independent_allocation_audit_passed"] is False
        and audit["independent_allocation_audit_passed"] is True
        and audit["actual_source_manifest_sha256"] == SOURCE_SHA,
        "Actual independent exact primary binding",
    )
    authorization = read(AUDIT / "primary_allocation_authorization.json")
    require(
        authorization["independent130_authorizes_complete_primary90_result"] is True
        and authorization["conditional_allocation_release_eligible"] is True
        and authorization["source_manifest_sha256"] == SOURCE_SHA
        and authorization["new_fixture_credit"] == 0,
        "Actual independent complete authorization",
    )
    release = source["conditional_E_allow_lower"]
    require(
        release
        == audit["conditional_E_allow_lower"]
        == authorization["approved_primary_E_allow_lower"]
        and fraction(release) > 0,
        "Same exact positive primary release",
    )
    polynomial = read(SOURCE / "uniform_poly_allowance.json")
    require(
        polynomial["interval_digits"] == 90
        and polynomial["alpha"] == [1, 16777216]
        and polynomial["all_nonempty_allowances_strict_positive"] is True
        and polynomial["E_allow_lower"] == release,
        "Exact primary scalar artifact",
    )
    require(
        set(source["case_financial_F_upper"])
        == set(audit["case_financial_F_upper"])
        == {"B4x12", "B8x52"},
        "Both fixed contracts",
    )
    for name, bound in source["case_financial_F_upper"].items():
        require(
            0 <= fraction(bound) <= Fraction(11, 2000)
            and 0 <= fraction(audit["case_financial_F_upper"][name]) <= fraction(bound),
            "Exact accepted financial fit and independently tighter own value",
        )
    return release


def ready_checks():
    author_map = {
        (RESEARCH / name).relative_to(ROOT).as_posix(): pin for name, pin in AUTHORS.items()
    }
    manifest_map = {
        (PROGRAM / name / "manifest.json").relative_to(ROOT).as_posix(): pin
        for name, pin in PREREQUISITES.items()
    }
    values = []
    for name, pin in READY_PINS.items():
        path = add(PROGRAM / name, pin)
        value = read(path)
        require(
            value["schema"] == "a13-fixed-alpha-allocation-root-READY-v1"
            and value["ready"] is True
            and value["author_inputs"] == author_map
            and value["manifest_inputs"] == manifest_map
            and value["limits_CPU_work_wall"] == [180, 150, 600]
            and value["interval_digits_primary_independent"] == [90, 130]
            and value["threads"] == 1
            and value["alpha"] == [1, 16777216],
            "Exact immutable fixed READY policy",
        )
        add(LAUNCHER, value["interpreter_sha256"])
        for role, module, receipt in (
            ("producer", "experiment_exp_frontier_allocation", SOURCE),
            ("auditor", "audit_exp_frontier_allocation", AUDIT),
        ):
            for operation in ("prepare", "run"):
                require(
                    value["commands"][role + "_" + operation]
                    == [
                        str(LAUNCHER),
                        "-B",
                        "-m",
                        "research.limitation_program_20261001." + module,
                        operation,
                        "--output",
                        str(receipt),
                    ],
                    "Exact pinned original CLI",
                )
        values.append(value)
    require(
        values[1]["actual_allocation_producer_manifest_SHA256"] == SOURCE_SHA,
        "Separate audit READY binds actual primary",
    )
    for directory, ready_name in ((SOURCE, next(iter(READY_PINS))), (AUDIT, list(READY_PINS)[1])):
        require(
            read(directory / "root_READY_snapshot.json") == read(PROGRAM / ready_name),
            "Immutable executed READY copy equality",
        )
    method = read(RESEARCH / "a13_fixed_relative_envelope_allocation_preflight.json")
    require(method["actual_prerequisite_manifest_pins"] == manifest_map, "Method same ten owners")
    implementation = read(RESEARCH / "exp_frontier_allocation_implementation_preflight.json")
    for mapping in (
        method["held_method_pins"],
        implementation["required_method_SHA256"],
        implementation["actual_author_SHA256"],
    ):
        for key, pin in mapping.items():
            add(ROOT / key, pin)


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
    total = count = 0
    for mapping in (_FROZEN, _EXTERNAL):
        for member, expected in mapping.items():
            budget()
            path = canonical(Path(member) if Path(member).is_absolute() else ROOT / member)
            count += 1
            total += path.stat().st_size
            require(
                count <= MAX_REFERENCES and total <= MAX_UNIQUE_BYTES,
                "Fixed bounded complete union",
            )
            require(digest(path) == expected, "Fresh whole-union actual SHA mismatch: " + member)
    for name in _PACKETS:
        if name != FAILED.name:
            no_failure(PROGRAM / name)
    for directory, members in _OWN_INVENTORIES.items():
        require(inventory(directory) == members, "Terminal exact owned directory inventory")
    require(
        not any(path.exists() for path in _ABSENT_RUNTIME), "Absent standard zip remains absent"
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
    require(not OUTPUT.exists(), "Fresh fixed root verification receipt; no retry")
    require(sys.argv[1:] == [], "Fixed CLI without scope overrides")
    budget(admission=True)
    OUTPUT.mkdir()
    try:
        source = canonical(__file__)
        add(source, digest(source))
        add(ORIGIN, ORIGIN_SHA)
        copy_input(source, source.name)
        for name, pin in AUTHORS.items():
            add(RESEARCH / name, pin)
        source_summary, _ = packet(SOURCE.name, SOURCE_SHA)
        audit_summary, _ = packet(AUDIT.name, AUDIT_SHA)
        for name, pin in PREREQUISITES.items():
            packet(name, pin)
        ready_checks()
        release = check_release(source_summary, audit_summary)
        runtime = own_runtime()
        for name in READY_PINS:
            copy_input(PROGRAM / name, name)
        count, total = fresh_union()
        budget(admission=True)
        write(
            "admission.json",
            {
                "complete_packet_map_counts": _PACKETS,
                "exact_ready_and_six_author_pins": True,
                "own_runtime": runtime,
                "fresh_unique_input_paths": count,
                "fresh_input_bytes": total,
                "all_old_failure_maps_retained_zero_credit": True,
            },
        )
        loaded_origins()
        count, total = fresh_union()
        summary = {
            "schema": "root-exp-frontier-fixed-alpha-fresh-integrity-v1",
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "local_only": True,
            "passed": True,
            "completed": True,
            "budget_censored": False,
            "actual_primary90_and_independent130_terminal_PASS": True,
            "primary_manifest_sha256": SOURCE_SHA,
            "audit_manifest_sha256": AUDIT_SHA,
            "conditional_allocation_release_eligible": True,
            "conditional_E_allow_lower": release,
            "alpha": [1, 16777216],
            "fresh_unique_input_paths": count,
            "fresh_hashed_input_bytes": total,
            "SHA_mismatches": 0,
            "packet_map_counts": _PACKETS,
            "CPU_admission_wall_limits": [CPU, ADMISSION, WALL],
            "process_CPU_seconds": time.process_time(),
            "wall_seconds_from_actual_process_creation": time.monotonic() - _STARTED,
            "new_fixture_credit": 0,
            "new_gate_replays": 0,
            "scientific_kernels_executed": False,
            "actual_candidate_G2_feasibility": False,
            "held_A13_fields_changed": False,
            "adoption": False,
            "cost_transfer": False,
            "quantum_advantage_claim": False,
            "live_progress_or_STATUS_modified": False,
        }
        write("summary.json", summary)
        owned = inventory(OUTPUT)
        files = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(owned)}
        budget()
        write(
            "manifest.json",
            {
                "schema": "root-exp-frontier-allocation-integrity-manifest-v1",
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
        terminal_sha = digest(OUTPUT / "manifest.json")
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
