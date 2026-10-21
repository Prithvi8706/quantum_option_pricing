"""Prospective C8 input capture; author-only until a separately authorized launch.

No producer edits or numerical outcomes. The imported frozen functions below are
called only by main(), after exact code/runtime snapshots have been sealed.
Factors are expected source-derived inputs, never worker-observed attestations.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import re
import shutil
import site
import subprocess
import sys
import time
import zipfile

COMMIT = "b4a4bdc9bd21099fd1382dff7f9e57c470a54d3a"
ROOT = Path("C:/Users/prith/quantum_option_pricing")
CASE_INDICES = tuple(range(100, 124))
MAX_FILES = 24_000  # Prospective: actual metadata count20,754 including all existing bytecode.
MAX_BYTES = 2 * 1024**3
EXTERNAL_RUNTIME_OVERRIDES = ("PYTHONPATH", "PYTHONHOME", "NUMBA_CACHE_DIR")

PREVIOUS_AUTHOR_SHA256 = {
    "run_c8_supervised.py": "b9613c6e9a4d3ff888cb00beba39f4e9acdc95d12922f1f6d746f4daefa98358",
    "capture_c8_prerun_inventory.py": (
        "9daffa3f839a0b56ab3b25126ccc52029fd37c3b39540142c9a8cf3943a0e369"
    ),
    "c8_execution_preflight.json": (
        "6b1e03a241febcd5ab5a4304fab3f2e06ec10234720c4446aca86262870d39ad"
    ),
    "C8_EXECUTION_PREFLIGHT.md": "57eb2e82fa2c87b2bd8ea92bd85513fac44b98964e122b0a61cc77670d5997eb",
}
PREVIOUS_DIAGNOSTIC = ROOT / "results/limitation_program_20261001/C8_admission_failure_run001"
PREVIOUS_MANIFEST_SHA256 = "f5850813ecc8a31219a60c8009eeee2258769fa508571bb57c005fac2a9bfc61"


def bind_previous_admission(frozen, check, value):
    """Bind the immutable original attempt and diagnosis before any helper/science import."""
    check()
    expected_policy = dict(
        diagnostic_receipt="results/limitation_program_20261001/C8_admission_failure_run001",
        diagnostic_manifest_sha256=PREVIOUS_MANIFEST_SHA256,
        original_author_sha256=PREVIOUS_AUTHOR_SHA256,
        prior_failure_fixture_or_measurement_credit=0,
    )
    if value.get("previous_admission_bindings") != expected_policy:
        raise RuntimeError(
            "fixed original admission provenance cannot be replaced by caller expectations"
        )

    def path(name):
        check()
        value = Path(name)
        if not value.is_absolute():
            if value.drive or "\\" in str(name) or value.as_posix() != str(name):
                raise RuntimeError("canonical ROOT-relative prior admission reference required")
            value = ROOT / value
        resolved = value.resolve(strict=True)
        resolved.relative_to(ROOT.resolve(strict=True))
        return resolved

    def hashed(source):
        check()
        result = hashlib.sha256()
        with source.open("rb") as stream:
            while block := stream.read(1024 * 1024):
                check()
                result.update(block)
                check()
        check()
        return result.hexdigest()

    def add(name, expected):
        check()
        if (
            type(expected) is not str
            or len(expected) != 64
            or any(character not in "0123456789abcdef" for character in expected)
        ):
            raise RuntimeError("explicit canonical prior admission SHA256 required")
        source = path(name)
        identity = os.path.normcase(str(source))
        if identity in frozen and frozen[identity] != expected:
            raise RuntimeError("prior admission expected SHA cannot be overwritten")
        if hashed(source) != expected:
            raise RuntimeError("immutable prior admission bytes changed: " + str(source))
        frozen[identity] = expected

    manifest_path = PREVIOUS_DIAGNOSTIC / "manifest.json"
    add(manifest_path, PREVIOUS_MANIFEST_SHA256)
    manifest = json.loads(manifest_path.read_bytes())
    check()
    if (
        set(manifest) != {"files", "frozen_inputs", "manifest_self_hash_excluded"}
        or manifest["manifest_self_hash_excluded"] is not True
        or type(manifest["files"]) is not dict
        or type(manifest["frozen_inputs"]) is not dict
    ):
        raise RuntimeError("exact root diagnostic owned/frozen map schema required")
    own = set()
    for field in ("files", "frozen_inputs"):
        for name, expected in manifest[field].items():
            check()
            source = path(name)
            if field == "files":
                source.relative_to(PREVIOUS_DIAGNOSTIC.resolve(strict=True))
                own.add(source)
            add(name, expected)
    actual_own = set()
    for source in PREVIOUS_DIAGNOSTIC.rglob("*"):
        check()
        if source.is_file() and source != manifest_path:
            actual_own.add(path(source))
    if actual_own != own:
        raise RuntimeError("complete prior diagnostic owned inventory required")
    old_receipt = ROOT / "results/limitation_program_20261001/C8_execution_run001"
    expected_old = {
        path(name)
        for name in manifest["frozen_inputs"]
        if path(name).is_relative_to(old_receipt.resolve(strict=True))
    }
    actual_old = set()
    for source in old_receipt.rglob("*"):
        check()
        if source.is_file():
            actual_old.add(path(source))
    if actual_old != expected_old:
        raise RuntimeError("every original failed C8 receipt file remains a strict active binding")
    for name, expected in PREVIOUS_AUTHOR_SHA256.items():
        check()
        add(ROOT / "research/limitation_program_20261001" / name, expected)
        copied = old_receipt / "executed_sources" / name
        copied_key = copied.relative_to(ROOT).as_posix()
        if manifest["frozen_inputs"].get(copied_key) != expected:
            raise RuntimeError(
                "original executed author source belongs to root diagnostic manifest"
            )
    summary = json.loads((PREVIOUS_DIAGNOSTIC / "summary.json").read_bytes())
    check()
    if (
        summary["passed"] is not False
        or summary["original_attempt_immutable"] is not True
        or summary["original_rates_launched"] is not False
        or summary["original_timing_launched"] is not False
        or summary["new_test_or_measurement_credit"] != 0
        or summary["inventory_job_terminal_active_processes"] != 0
        or summary["source_receipt"] != "results/limitation_program_20261001/C8_execution_run001"
        or summary["all_actual_receipt_files_bound"] != len(actual_old)
    ):
        raise RuntimeError(
            "diagnosed original operational admission failure, no numerical retry or credit"
        )
    check()
    return dict(
        original_source_receipt=summary["source_receipt"],
        original_diagnostic_manifest_sha256=PREVIOUS_MANIFEST_SHA256,
        original_author_sources_bound=4,
        all_original_receipt_files_bound=len(actual_old),
        original_failure_fixture_or_measurement_credit=0,
        original_rates_or_timing_launched=False,
        newly_preregistered_operational_admission_not_numerical_retry=True,
    )


class Guard:
    def __init__(self, seconds: float, started: float | None = None):
        self.started = time.monotonic() if started is None else started
        self.seconds = seconds

    def check(self):
        if time.monotonic() - self.started >= self.seconds:
            raise TimeoutError(f"wall guard {self.seconds:g}s exhausted")

    def remaining(self):
        self.check()
        return self.seconds - (time.monotonic() - self.started)


def canonical(path: str | Path) -> str:
    return os.path.normcase(str(Path(path).resolve(strict=True)))


def confined(path: Path, parent: Path) -> Path:
    resolved = path.resolve(strict=True)
    resolved.relative_to(parent.resolve(strict=True))
    if path.is_symlink():
        raise RuntimeError(f"symlink rejected: {path}")
    return resolved


def json_new(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write("\n")


def digest(path: Path, guard: Guard) -> str:
    guard.check()
    before = path.stat()
    total = 0
    hashed = hashlib.sha256()
    with path.open("rb") as stream:
        while data := stream.read(1024 * 1024):
            guard.check()
            total += len(data)
            hashed.update(data)
    after = path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise RuntimeError(f"file changed while hashing: {path}")
    if total != before.st_size:
        raise RuntimeError(f"short hash read: {path}")
    guard.check()
    return hashed.hexdigest()


def snapshot(source: Path, target: Path, guard: Guard) -> dict:
    """Copy once and verify actual source/copy equal-SHA, never accept overrides."""
    guard.check()
    if source.is_symlink() or target.exists():
        raise RuntimeError(f"unsafe snapshot source/target: {source} -> {target}")
    source_hash = digest(source, guard)
    target.parent.mkdir(parents=True, exist_ok=True)
    with source.open("rb") as incoming, target.open("xb") as outgoing:
        while block := incoming.read(1024 * 1024):
            guard.check()
            outgoing.write(block)
    target_hash = digest(target, guard)
    if digest(source, guard) != source_hash or target_hash != source_hash:
        raise RuntimeError(f"snapshot unequal SHA: {source}")
    return dict(
        actual_path=canonical(source),
        snapshot_path=canonical(target),
        sha256=source_hash,
        size=source.stat().st_size,
    )


def git(worktree: Path, args: list[str], guard: Guard, *, acceptable=(0,)):
    guard.check()
    completed = subprocess.run(
        ["git", "-C", str(worktree), *args], capture_output=True, timeout=min(30, guard.remaining())
    )
    if completed.returncode not in acceptable:
        raise RuntimeError(f"git command failed {args!r}: {completed.stderr!r}")
    return completed


def assert_checkout(worktree: Path, guard: Guard):
    if git(worktree, ["rev-parse", "HEAD"], guard).stdout.decode().strip() != COMMIT:
        raise RuntimeError("checkout HEAD is not the frozen C8 commit")
    if git(worktree, ["symbolic-ref", "-q", "HEAD"], guard, acceptable=(0, 1)).returncode != 1:
        raise RuntimeError("C8 checkout must be detached")
    if git(worktree, ["status", "--porcelain", "--untracked-files=all"], guard).stdout.strip():
        raise RuntimeError("C8 checkout is dirty; no cleanup or reuse allowed")


def policy(path: Path, guard: Guard) -> dict:
    guard.check()
    value = json.loads(path.read_bytes())
    if value["commit"] != COMMIT or canonical(value["workspace_root"]) != canonical(ROOT):
        raise RuntimeError("preflight root/commit is outside the fixed C8 scope")
    if value["cases"]["count"] != 24 or value["original_methods"]["rates_scrambles"] != 32:
        raise RuntimeError("fixed C8 settings changed")
    if value["original_methods"]["rate_m_max"] != 17:
        raise RuntimeError("fixed C8 rate budget changed")
    if value["supervisor"]["rates_entire_phase_wall_seconds"] != 43_200:
        raise RuntimeError("fixed rates external wall guard changed")
    if value["supervisor"]["timing_entire_phase_wall_seconds"] != 28_800:
        raise RuntimeError("fixed timing external wall guard changed")
    return value


def reject_external_runtime_overrides():
    for key in EXTERNAL_RUNTIME_OVERRIDES:
        if os.environ.get(key):
            raise RuntimeError(f"nonempty inherited {key} is outside captured C8 runtime scope")


def runtime_scope(path: Path, scopes: list[tuple[str, Path]]) -> tuple[str, Path]:
    resolved = path.resolve(strict=path.exists())
    for label, parent in scopes:
        if resolved.is_relative_to(parent.resolve(strict=True)):
            parent = parent.resolve(strict=True)
            if resolved.is_dir() and label == "venv" and resolved != parent:
                if not any(resolved.is_relative_to(parent / part) for part in ("Lib", "Scripts")):
                    raise RuntimeError("venv sys.path directory is outside copied Lib/Scripts")
            if resolved.is_dir() and label == "base" and resolved != parent:
                if not any(
                    resolved.is_relative_to(parent / part) for part in ("Lib", "DLLs")
                ) or resolved.is_relative_to(parent / "Lib/site-packages"):
                    raise RuntimeError("base sys.path directory is outside copied stdlib/DLLs")
            return label, resolved
    raise RuntimeError(f"runtime path outside captured permitted roots: {path}")


def capture_source_runtime(value: dict, out: Path, guard: Guard) -> dict:
    """Seal every bounded source/runtime byte before importing original code."""
    reject_external_runtime_overrides()
    worktree = Path(value["execution_worktree"]).resolve(strict=True)
    assert_checkout(worktree, guard)
    expected = value["source_git_blob_sha256"]
    stage_files = git(
        worktree,
        ["ls-tree", "-r", "--name-only", COMMIT, "research/frontier_classical_20261001"],
        guard,
    )
    paths = [p for p in stage_files.stdout.decode().splitlines() if p.endswith(".py")]
    paths.extend(
        (
            "manuscript/advantage-frontier-2026-09-23/ANALYSIS_SPEC_STAGE_C.md",
            "research/frontier_replay_20261001/t0_requirements.lock",
        )
    )
    if set(paths) != set(expected):
        raise RuntimeError("preflight has missing/extra frozen source expectations")
    bindings = []
    for relative in sorted(paths):
        guard.check()
        blob = git(worktree, ["show", f"{COMMIT}:{relative}"], guard).stdout
        if hashlib.sha256(blob).hexdigest() != expected[relative]:
            raise RuntimeError(f"Git blob mismatch: {relative}")
        # A checkout may apply Git EOL filters: preserve and bind its actual bytes.
        wanted = git(worktree, ["rev-parse", f"{COMMIT}:{relative}"], guard).stdout.strip()
        actual = git(
            worktree, ["hash-object", f"--path={relative}", relative], guard
        ).stdout.strip()
        if actual != wanted:
            raise RuntimeError(f"checkout content differs from frozen Git blob: {relative}")
        source = confined(worktree / relative, worktree)
        source_bytes = source.read_bytes()
        guard.check()
        if source_bytes == blob:
            newline_relation = "exact-byte-equality"
        elif source_bytes.replace(b"\r\n", b"\n") == blob.replace(b"\r\n", b"\n"):
            newline_relation = "only-CRLF-versus-LF"
        else:
            raise RuntimeError(f"checkout bytes differ beyond LF/CRLF: {relative}")
        row = snapshot(source, out / "source" / relative, guard)
        if row["sha256"] != hashlib.sha256(source_bytes).hexdigest():
            raise RuntimeError("source changed between Git-byte check and snapshot")
        row.update(
            kind="frozen_checkout_file",
            git_blob_sha256=expected[relative],
            git_blob_object=wanted.decode(),
            checkout_newline_relation=newline_relation,
            checkout_sha_equals_git_blob=(row["sha256"] == expected[relative]),
        )
        bindings.append(row)

    if sys.version_info[:2] != (3, 12):
        raise RuntimeError("C8 requires Python 3.12")
    if canonical(sys.executable) != canonical(value["interpreter"]):
        raise RuntimeError("not the pinned C8 interpreter")
    if not sys.dont_write_bytecode:
        raise RuntimeError("capture must start with PYTHONDONTWRITEBYTECODE=1")
    runtime = dict(
        python=sys.version,
        executable=canonical(sys.executable),
        base_executable=canonical(getattr(sys, "_base_executable", sys.executable)),
        prefix=str(Path(sys.prefix).resolve()),
        base_prefix=str(Path(sys.base_prefix).resolve()),
        dont_write_bytecode=sys.dont_write_bytecode,
        distributions={},
        platform=platform.platform(),
        machine=platform.machine(),
        logical_cpu_count=os.cpu_count(),
        user_site_enabled=site.ENABLE_USER_SITE,
    )
    if site.ENABLE_USER_SITE is not False:
        raise RuntimeError("pinned venv must disable user-site packages before input generation")
    venv = Path(sys.prefix).resolve(strict=True)
    base = Path(sys.base_prefix).resolve(strict=True)
    executed_source_dir = (out.parent / "executed_sources").resolve(strict=True)
    scopes = [
        ("venv", venv),
        ("base", base),
        ("worktree", worktree),
        ("executed_sources", executed_source_dir),
    ]
    sys_paths, archives = [], {}
    for raw_path in sys.path:
        guard.check()
        path = Path(raw_path) if raw_path else Path.cwd()
        label, resolved = runtime_scope(path, scopes)
        exists = resolved.exists()
        kind = "absent" if not exists else "directory" if resolved.is_dir() else "zip_archive"
        if exists and resolved.is_file():
            if not zipfile.is_zipfile(resolved):
                raise RuntimeError(
                    f"sys.path file is not a bounded permitted zip archive: {resolved}"
                )
            archives[canonical(resolved)] = (resolved, label)
        sys_paths.append(
            dict(
                raw_entry=raw_path,
                resolved_path=os.path.normcase(str(resolved)),
                scope=label,
                kind=kind,
                existed_before_import=exists,
            )
        )
    runtime["permitted_sys_path_entries"] = sys_paths
    runtime["installed_distribution_locations"] = []
    lock_path = worktree / "research/frontier_replay_20261001/t0_requirements.lock"
    locked = re.findall(
        r"^([A-Za-z0-9_.-]+)==([^\s\\]+)", lock_path.read_text(), flags=re.MULTILINE
    )
    if not locked:
        raise RuntimeError("frozen lock has no requirements")
    for name, version in locked:
        guard.check()
        if importlib.metadata.version(name) != version:
            raise RuntimeError(f"installed distribution differs from lock: {name}")
    for distribution in importlib.metadata.distributions():
        guard.check()
        name = distribution.metadata["Name"]
        if not name or name.lower() in runtime["distributions"]:
            raise RuntimeError("missing/duplicate distribution identity")
        runtime["distributions"][name.lower()] = distribution.version
        location = distribution.locate_file("")
        if isinstance(location, zipfile.Path):
            archive = Path(location.root.filename)
            label, resolved = runtime_scope(archive, scopes)
            if not zipfile.is_zipfile(resolved):
                raise RuntimeError("distribution archive is not a permitted zip file")
            archives[canonical(resolved)] = (resolved, label)
            distribution_location = dict(
                path=canonical(resolved),
                scope=label,
                zip_member_prefix=location.at,
                zip_archive=True,
            )
        else:
            label, resolved = runtime_scope(Path(location), scopes)
            if not resolved.is_dir():
                raise RuntimeError(
                    "installed distribution location is missing/not a captured directory"
                )
            distribution_location = dict(path=canonical(resolved), scope=label, zip_archive=False)
        runtime["installed_distribution_locations"].append(
            dict(name=name, version=distribution.version, location=distribution_location)
        )
    for name, version in value["required_runtime_versions"].items():
        if name != "python" and importlib.metadata.version(name) != version:
            raise RuntimeError(f"required C8 version mismatch: {name}")

    candidates = {}
    venv_config = (venv / "pyvenv.cfg").read_text()
    if not re.search(
        r"^include-system-site-packages\s*=\s*false\s*$",
        venv_config,
        flags=re.IGNORECASE | re.MULTILINE,
    ):
        raise RuntimeError("pinned venv must exclude unbound base-site packages")
    selections = [
        (venv / "Scripts", "venv/Scripts"),
        (venv / "Lib", "venv/Lib"),
        (base / "DLLs", "base/DLLs"),
        (base / "Lib", "base/Lib"),
    ]
    for selected, prefix in selections:
        guard.check()
        if not selected.is_dir():
            raise RuntimeError(f"missing runtime directory: {selected}")
        for file in selected.rglob("*"):
            guard.check()
            if not file.is_file():
                continue
            if prefix == "base/Lib" and "site-packages" in file.relative_to(selected).parts:
                continue
            confined(file, selected)
            candidates[canonical(file)] = (file, Path(prefix) / file.relative_to(selected))
            if len(candidates) > MAX_FILES:
                raise RuntimeError("runtime inventory file bound exceeded")
    for file in (
        venv / "pyvenv.cfg",
        Path(sys.executable),
        Path(runtime["base_executable"]),
        base / "python3.dll",
        base / "python312.dll",
    ):
        guard.check()
        if not file.is_file():
            raise RuntimeError(f"missing interpreter/runtime dependency: {file}")
        parent, prefix = (venv, "venv") if file.resolve().is_relative_to(venv) else (base, "base")
        confined(file, parent)
        candidates[canonical(file)] = (file, Path(prefix) / file.relative_to(parent))
    # CPython also loads adjacent CRT/runtime DLLs outside its DLLs subdirectory.
    for file in base.glob("*.dll"):
        guard.check()
        confined(file, base)
        candidates[canonical(file)] = (file, Path("base") / file.relative_to(base))
    # Top-level importable runtime files and every permitted sys.path archive.
    for parent, prefix in ((venv, "venv"), (base, "base")):
        for file in parent.iterdir():
            guard.check()
            if file.is_file() and file.suffix.lower() in (
                ".py",
                ".pyc",
                ".pyd",
                ".dll",
                ".zip",
                ".egg",
                "._pth",
            ):
                confined(file, parent)
                candidates[canonical(file)] = (file, Path(prefix) / file.relative_to(parent))
    for identity, (file, label) in archives.items():
        parent = dict(scopes)[label]
        relative = Path(label) / file.relative_to(parent)
        if label not in ("venv", "base"):
            relative = Path("permitted_sys_path_archives") / relative
        candidates[identity] = (file, relative)
    git_exe = Path(shutil.which("git") or "")
    if not git_exe.is_file():
        raise RuntimeError("git executable unresolved")
    candidates[canonical(git_exe)] = (git_exe, Path("tools/git.exe"))
    total = 0
    for actual_path, (file, relative) in sorted(candidates.items()):
        guard.check()
        total += file.stat().st_size
        if len(candidates) > MAX_FILES or total > MAX_BYTES:
            raise RuntimeError("bounded runtime inventory exhausted; no partial admission")
        row = snapshot(file, out / "runtime" / relative, guard)
        if row["actual_path"] != actual_path:
            raise RuntimeError("canonical runtime source changed")
        row["kind"] = "runtime_dependency"
        bindings.append(row)
    runtime.update(
        runtime_files=len(candidates),
        runtime_bytes=total,
        thread_environment={
            key: os.environ.get(key)
            for key in (
                "OPENBLAS_NUM_THREADS",
                "MKL_NUM_THREADS",
                "OMP_NUM_THREADS",
                "NUMBA_NUM_THREADS",
            )
        },
        numba_cache_dir=os.environ.get("NUMBA_CACHE_DIR"),
        scientific_control_environment={
            key: os.environ.get(key)
            for key in (
                "PYTHONPATH",
                "PYTHONHOME",
                "PYTHONHASHSEED",
                "PYTHONDONTWRITEBYTECODE",
                "NUMBA_CPU_NAME",
                "NUMBA_CPU_FEATURES",
                "NUMBA_THREADING_LAYER",
                "NPY_DISABLE_CPU_FEATURES",
                "OPENBLAS_CORETYPE",
                "MKL_CBWR",
                "SCIPY_ARRAY_API",
            )
        },
        sys_path_before_scientific_import=list(sys.path),
        locked_distribution_version_equality_verified=True,
        installed_files_not_reconstructed_locked_wheel_hash_proof=True,
    )
    result = dict(
        commit=COMMIT,
        bindings=bindings,
        runtime=runtime,
        permitted_sys_path_entries=sys_paths,
        every_expected_factor_generated_yet=False,
        frozen_input_sha256={row["snapshot_path"]: row["sha256"] for row in bindings},
        live_paths_are_observed_provenance_not_frozen_snapshot_keys=True,
    )
    json_new(out / "source_runtime_capture_before_generation.json", result)
    guard.check()
    return result


def verify_capture(capture: dict, guard: Guard):
    reject_external_runtime_overrides()
    for row in capture.get("permitted_sys_path_entries", []):
        guard.check()
        path = Path(row["resolved_path"])
        if path.exists() != row["existed_before_import"]:
            raise RuntimeError("permitted sys.path presence changed after capture")
        if path.exists() and canonical(path) != row["resolved_path"]:
            raise RuntimeError("permitted sys.path canonical identity changed")
    seen = {}
    for row in capture["bindings"]:
        guard.check()
        for key in ("actual_path", "snapshot_path"):
            path = Path(row[key])
            identity = canonical(path)
            previous = seen.setdefault(identity, row["sha256"])
            if previous != row["sha256"] or digest(path, guard) != row["sha256"]:
                raise RuntimeError(f"live/copy runtime/source SHA mismatch: {path}")


def verify_scientific_module_bytes(capture: dict, guard: Guard):
    expected = {row["actual_path"]: row["sha256"] for row in capture["bindings"]}
    checked, modules = {}, []
    for name, module in list(sys.modules.items()):
        if not (
            name.split(".", 1)[0] in ("numpy", "scipy", "numba", "llvmlite")
            or name.startswith("research.frontier_classical_20261001.")
        ):
            continue
        for role in ("__file__", "__cached__"):
            actual = getattr(module, role, None)
            if actual is None:
                continue
            path = Path(actual)
            if role == "__cached__" and not path.exists():
                continue  # No bytecode file exists with PYTHONDONTWRITEBYTECODE=1.
            identity = canonical(path)
            if identity not in expected:
                raise RuntimeError(
                    f"scientific module bytes absent from captured inventory: {name} {role}"
                )
            if identity not in checked:
                checked[identity] = digest(path, guard)
            if checked[identity] != expected[identity]:
                raise RuntimeError(f"scientific module bytes changed after capture: {name}")
            modules.append(
                dict(module=name, role=role, actual_path=identity, sha256=checked[identity])
            )
    return modules


def seal_inputs(value: dict, out: Path, capture: dict, guard: Guard) -> dict:
    """Future automatic input-only computation, with no human/outcome inspection."""
    worktree = Path(value["execution_worktree"]).resolve(strict=True)
    guard.check()
    verify_capture(capture, guard)
    assert_checkout(worktree, guard)
    sys.path.insert(0, str(worktree))
    module = importlib.import_module("research.frontier_classical_20261001.c7_c8_cases")
    basis = importlib.import_module("research.frontier_classical_20261001.basis")
    np = importlib.import_module("numpy")
    scipy = importlib.import_module("scipy")
    numba = importlib.import_module("numba")
    for imported in (module, basis):
        if canonical(imported.__file__) != canonical(
            worktree / Path(*imported.__name__.split(".")).with_suffix(".py")
        ):
            raise RuntimeError("original generator/factor module escaped frozen checkout")
    if np.__version__ != "2.0.2" or not Path(np.__file__).resolve().is_relative_to(
        Path(sys.prefix).resolve()
    ):
        raise RuntimeError("NumPy actual import is not the pinned environment")
    for imported, version in ((scipy, "1.13.1"), (numba, "0.60.0")):
        if imported.__version__ != version or not Path(imported.__file__).resolve().is_relative_to(
            Path(sys.prefix).resolve()
        ):
            raise RuntimeError("actual scientific import escaped the pinned environment")
    for name, imported in list(sys.modules.items()):
        if name.startswith("research.frontier_classical_20261001.") and getattr(
            imported, "__file__", None
        ):
            expected = worktree / Path(*name.split(".")).with_suffix(".py")
            if canonical(imported.__file__) != canonical(expected):
                raise RuntimeError("transitive original Stage C module escaped the frozen checkout")
    scientific_module_bindings = verify_scientific_module_bytes(capture, guard)
    cases = module.c8_cases()
    if tuple(case.case_index for case in cases) != CASE_INDICES:
        raise RuntimeError("generated C8 inventory differs from the fixed 24 cases")
    rows = []
    for case in cases:
        guard.check()
        factor, groups = basis.canonical_factor(
            case.na, case.nt, case.sigma, case.rho, case.maturity
        )
        if (
            factor.dtype != np.dtype("float64")
            or not factor.flags.c_contiguous
            or factor.shape != (case.dim, case.dim)
        ):
            raise RuntimeError("factor dtype/order/shape differs from the frozen method")
        raw = factor.tobytes(order="C")
        file = out / "expected_factors" / f"case{case.case_index}.float64_c.bin"
        file.parent.mkdir(parents=True, exist_ok=True)
        with file.open("xb") as stream:
            stream.write(raw)
        hashed = hashlib.sha256(raw).hexdigest()
        if digest(file, guard) != hashed:
            raise RuntimeError("expected-factor immutable bytes failed verification")
        rows.append(
            dict(
                case=case.__dict__,
                factor_shape=list(factor.shape),
                factor_dtype=factor.dtype.str,
                generation_seed_key=[
                    2026092301,
                    (case.case_index - 100) // 4,
                    (case.case_index - 100) % 4,
                ],
                generation_draw_order=["barrier_ratio", "sigma", "rho"],
                factor_order="C",
                factor_snapshot=canonical(file),
                factor_sha256=hashed,
                factor_bytes=len(raw),
                repeated_eigenvalue_groups=groups,
                rate_keys=[[2026100181, case.case_index, 0, 0, s] for s in range(32)],
                timing_keys=[[2026100181, case.case_index, 1, 0, s] for s in range(16)],
                sigma_key=[2026100107, case.case_index, 7, 0, 0],
                rate_bootstrap_key=[2026100112, case.case_index, 0, 0, 0],
                sigma_bootstrap_key=[2026100112, case.case_index, 7, 0, 0],
            )
        )
    verify_capture(capture, guard)
    verify_scientific_module_bytes(capture, guard)
    assert_checkout(worktree, guard)
    result = dict(
        passed=True,
        expected_case_count=24,
        cases=rows,
        expected_factors_source_derived_not_worker_observed=True,
        producer_has_started=False,
        payoff_or_outcome_evaluations=0,
        no_human_input_inspection_or_adaptive_selection=True,
        numpy_build_configuration=getattr(np.__config__, "CONFIG", None),
        actual_scientific_module_versions=dict(
            numpy=np.__version__, scipy=scipy.__version__, numba=numba.__version__
        ),
        imported_scientific_module_byte_bindings_before_case_generation=scientific_module_bindings,
        actual_thread_environment={
            key: os.environ.get(key)
            for key in (
                "OPENBLAS_NUM_THREADS",
                "MKL_NUM_THREADS",
                "OMP_NUM_THREADS",
                "NUMBA_NUM_THREADS",
            )
        },
        fixture_credit=0,
        quantum_advantage_claim=False,
    )
    if any(setting != "1" for setting in result["actual_thread_environment"].values()):
        raise RuntimeError("original import did not pin all four thread settings")
    json_new(out / "expected_inputs_sealed.json", result)
    guard.check()
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preflight", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    guard = Guard(900)
    reject_external_runtime_overrides()
    value = policy(Path(args.preflight), guard)
    previous_frozen = {}
    previous_admission = bind_previous_admission(previous_frozen, guard.check, value)
    out = Path(args.out)
    wanted = Path(value["receipt"]) / "inventory"
    if out.absolute() != wanted.absolute() or out.exists():
        raise RuntimeError("inventory must use the fresh exact receipt subdirectory")
    out.mkdir(parents=True, exist_ok=False)
    json_new(
        out / "capture_started.json",
        dict(
            commit=COMMIT,
            own_source=canonical(__file__),
            own_source_sha256=digest(Path(__file__), guard),
            preflight=canonical(args.preflight),
            preflight_sha256=digest(Path(args.preflight), guard),
            fixture_credit=0,
        ),
    )
    json_new(
        out / "previous_admission_bindings.json",
        dict(
            provenance=previous_admission,
            original_owned_and_frozen_inputs=previous_frozen,
            original_failure_fixture_or_measurement_credit=0,
        ),
    )
    try:
        capture = capture_source_runtime(value, out, guard)
        seal_inputs(value, out, capture, guard)
        json_new(
            out / "inventory_terminal.json",
            dict(
                passed=True,
                wall_seconds=time.monotonic() - guard.started,
                fixture_credit=0,
                worker_factor_sha_observed=False,
            ),
        )
    except BaseException as exc:
        # The parent owns the overall terminal manifest; this diagnostic is never credit.
        json_new(
            out / "inventory_terminal_failure.json",
            dict(
                passed=False,
                error=repr(exc),
                wall_seconds=time.monotonic() - guard.started,
                fixture_credit=0,
            ),
        )
        raise


if __name__ == "__main__":
    main()
