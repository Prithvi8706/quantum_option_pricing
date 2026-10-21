"""Prospective shared OPERATIONAL receipt machinery only; no science on import."""

from __future__ import annotations

import ctypes
from ctypes import wintypes
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
PROGRAM = ROOT / "results/limitation_program_20261001"
CPU, WORK, WALL = 180, 150, 600
AUTHOR_NAMES = (
    "arithmetic_free_basket_signal_v4.py",
    "a20_signal_receipt_v4.py",
    "experiment_arithmetic_free_basket_signal_v4.py",
    "audit_arithmetic_free_basket_signal_v4.py",
    "A20_COMPARATOR_PHASE_IMPLEMENTATION_PREFLIGHT_V4.md",
    "a20_comparator_phase_implementation_preflight_v4.json",
)
ORIGINAL_PINS = {
    "A20_ARITHMETIC_FREE_LOADING_PROSPECTUS.md": (
        "19f08143e9be0aadac7f88f15a344ad9218ad359877c9e52aa6fc99715b5b291"
    ),
    "a20_arithmetic_free_loading_prospectus.json": (
        "c3d9b9301463069afe0813f726131f9f2af4a5ec0b7a7e5bf8c18950aae1f3f0"
    ),
}
HISTORICAL_V2_PINS = {
    "research/limitation_program_20261001/arithmetic_free_basket_signal_v2.py": (
        "4d7a7169d3bf13ef79417f97cb9dcf33bc9a7d009f9e9e6294284760f0a6ea1a"
    ),
    "research/limitation_program_20261001/a20_signal_receipt_v2.py": (
        "25fcef657d3699a54f5ee7daf0783ccf5948359604dd10e293b545739f2498bd"
    ),
    "research/limitation_program_20261001/experiment_arithmetic_free_basket_signal_v2.py": (
        "ca96c32e9d53e49da5e24b5d96df017d4f65b7ab913a3b74441d3e6d8645f4ed"
    ),
    "research/limitation_program_20261001/audit_arithmetic_free_basket_signal_v2.py": (
        "64327303b9658ecb920829241b1df9c42120773a2b3df3747e6d97af1ffd3c7d"
    ),
    "research/limitation_program_20261001/A20_COMPARATOR_PHASE_IMPLEMENTATION_PREFLIGHT_V2.md": (
        "3efd3f0850348f4a0c8759de84fca3632f029cca81c49e5689cb7f74512d4546"
    ),
    "research/limitation_program_20261001/a20_comparator_phase_implementation_preflight_v2.json": (
        "66eb828afe1ce31ff4b9d0be97f7ef889f9c9cc696ee7372ce2193fae507bbb5"
    ),
    ".context/A20_signal_producer_ROOT_READY_run001.json": (
        "08af3d467e1f9e235eb38943b4875999104ec110e92ab5a97cc7a15cb9beb4af"
    ),
    ".context/a20_signal_prepare_run001.log": (
        "6bbcb3b3bebc40221d3cef2b99b2d453090b4e34ae1f07b4bcd2bc511b5da394"
    ),
}
HISTORICAL_V2_ABSENT_ROUTES = (
    "A20_signal_semantics_run001",
    "A20_signal_semantics_audit_run001",
)
HISTORICAL_V3_PINS = {
    "research/limitation_program_20261001/A20_COMPARATOR_PHASE_IMPLEMENTATION_PREFLIGHT_V3.md": (
        "2a75285047b52ec7a1a9717e047c5c45419c6bc14acc4e5d32e57cd50cbfa7ee"
    ),
    "research/limitation_program_20261001/a20_comparator_phase_implementation_preflight_v3.json": (
        "694ad7f6e1aca0346938c43a83bfd721b669d7787edf3d1f6c1814f292f3b36c"
    ),
    "research/limitation_program_20261001/a20_signal_receipt_v3.py": (
        "79e70710f9c742fda57dff73704b66f791ee7905a88b0ab0128a2054aaebd6f2"
    ),
    "research/limitation_program_20261001/arithmetic_free_basket_signal_v3.py": (
        "4d7a7169d3bf13ef79417f97cb9dcf33bc9a7d009f9e9e6294284760f0a6ea1a"
    ),
    "research/limitation_program_20261001/audit_arithmetic_free_basket_signal_v3.py": (
        "5d0babd08382923458dd303309777085163e917b3c41e74ebae6c48c5762e187"
    ),
    "research/limitation_program_20261001/experiment_arithmetic_free_basket_signal_v3.py": (
        "eb7b523da38975278cd7e5d5c1a0993d67f04cc8b056f1897c5b1d08e9d9af62"
    ),
    ".context/A20_signal_producer_ROOT_READY_run002.json": (
        "fceee79c50b097a4de6da9ab67f450dac1f77431d447972d71214b869befd6ae"
    ),
    ".context/a20_signal_prepare_run002.log": (
        "2394d1e4b659b9c8cf10638e557460de1a01b290694af1919c25eb8145539ff2"
    ),
}
HISTORICAL_V3_ABSENT_ROUTES = (
    "A20_signal_semantics_run002",
    "A20_signal_semantics_audit_run002",
)
INTERPRETER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
FAILURE_NAMES = (
    "FAILED_UNSEALED.json",
    "failed_unsealed.json",
    "failure.json",
    "run_failure.json",
    "prepare_failure.json",
)
SHA = re.compile(r"[0-9a-f]{64}\Z")


def require(condition, message):
    if not condition:
        raise ValueError(message)


class Receipt:
    def __init__(self, role, ready_path, ready_sha, mode):
        require(role in ("producer", "audit") and mode in ("prepare", "run"), "Fixed A20 role/mode")
        self.role, self.mode = role, mode
        self.output = PROGRAM / (
            "A20_signal_semantics_run003"
            if role == "producer"
            else "A20_signal_semantics_audit_run003"
        )
        self.started = self.creation_clock()
        self.frozen, self.external, self.observed, self.cache, self.physical = {}, {}, {}, {}, {}
        self.hash_work, self.references, self.mutated = 0, 0, False
        self.runtime_absent = []
        self.source_packets = []
        self.owned_usage = None
        self.owned_expected = set()
        self.base = Path(os.path.abspath(sys.base_prefix))
        self.excluded = self.base / "Lib/site-packages"
        self.check()
        require(self.base.resolve(strict=True) == self.base, "Exact base runtime path")
        self.excluded_actual = self.excluded.resolve(strict=False)
        require(
            sys.version_info[:2] == (3, 12) and sys.dont_write_bytecode,
            "Pinned Python3.12 -B before module import",
        )
        require(
            Path(sys.executable).resolve(strict=True) == INTERPRETER,
            "Pinned isolated research interpreter",
        )
        require(Path.cwd().resolve(strict=True) == ROOT, "Fixed ROOT working directory")
        require(
            all(
                not os.environ.get(name) for name in ("PYTHONPATH", "PYTHONHOME", "NUMBA_CACHE_DIR")
            ),
            "No inherited external runtime overrides",
        )
        self.import_policy()
        self.ready_path = Path(ready_path)
        self.add(self.ready_path, ready_sha)
        self.ready = self.read(self.ready_path)
        require(
            self.ready["schema"] == "A20-comparator-phase-static-READY-v4"
            and self.ready["ready"] is True
            and self.ready["role"] == role,
            "Actual role-specific ROOT READY",
        )
        require(
            self.ready["budget"] == [CPU, WORK, WALL]
            and self.ready["science_executed_during_authoring"] is False,
            "Prospective fixed budgets and author scope",
        )
        require(
            self.ready["output"] == self.output.relative_to(ROOT).as_posix(),
            "Exact fresh fixed receipt",
        )
        self.add(INTERPRETER, self.ready["interpreter_sha256"])
        base_interpreter = self.canonical(Path(sys._base_executable))
        require(
            base_interpreter == self.base / "python.exe",
            "Exact base-prefix interpreter behind the pinned launcher",
        )
        self.add(base_interpreter, self.ready["base_interpreter_sha256"])
        authors = self.ready["author_sha256"]
        require(
            set(authors)
            == {str((RESEARCH / name).relative_to(ROOT).as_posix()) for name in AUTHOR_NAMES},
            "All six exact new authors pinned",
        )
        for key, expected in authors.items():
            self.add(ROOT / key, expected)
        self.admit_v2_history()
        self.admit_v3_history()
        for name, expected in ORIGINAL_PINS.items():
            self.add(RESEARCH / name, expected)
        old = self.read(RESEARCH / "a20_arithmetic_free_loading_prospectus.json")
        selected = self.ready["selected_prerequisite_sha256"]
        require(
            all(
                selected.get(key) == expected
                for key, expected in old["selected_original_expected_sha256"].items()
            ),
            "Original selected expected SHA never replaced",
        )
        for key, expected in selected.items():
            require(
                (ROOT / key).relative_to(ROOT).as_posix() == key, "Canonical selected ROOT spelling"
            )
            self.add(ROOT / key, expected)
        memberships = self.owner_memberships(self.ready["selected_owner_manifest_sha256"])
        require(
            all(
                (key, expected) in memberships
                for key, expected in selected.items()
                if not key.endswith("/manifest.json")
            ),
            "Every selected premise has exact sealed owner membership",
        )
        self.verify()

    def admit_v2_history(self):
        """Bind the actual pre-mkdir admission failure without promoting it."""
        for key, expected in HISTORICAL_V2_PINS.items():
            self.add(ROOT / key, expected)
        ready = self.read(ROOT / ".context/A20_signal_producer_ROOT_READY_run001.json")
        require(
            ready["schema"] == "A20-comparator-phase-static-READY-v2"
            and ready["role"] == "producer"
            and ready["ready"] is True
            and ready["budget"] == [CPU, WORK, WALL]
            and ready["output"] == "results/limitation_program_20261001/A20_signal_semantics_run001"
            and ready["author_sha256"]
            == {key: pin for key, pin in HISTORICAL_V2_PINS.items() if key.startswith("research/")},
            "Exact immutable V2 release and six historical expected authors",
        )
        log = self.read_bytes(ROOT / ".context/a20_signal_prepare_run001.log")
        require(
            log.startswith(b"\xef\xbb\xbf")
            and "ValueError: Exact selected owned member spelling" in log.decode("utf-8-sig"),
            "Exact raw UTF8-BOM original admission failure log",
        )
        self.verify_v2_absence()
        policy = self.read(RESEARCH / "a20_comparator_phase_implementation_preflight_v4.json")
        require(
            policy["immutable_V2_admission_history_expected_sha256"] == HISTORICAL_V2_PINS,
            "Prospective V4 method preserves every immutable V2 history pin",
        )
        self.history = {
            "schema": "A20-V2-pre-mkdir-admission-failure-history-v1",
            "historical_expected_sha256": HISTORICAL_V2_PINS,
            "failed_before_receipt_mkdir": True,
            "error": "ValueError: Exact selected owned member spelling",
            "historical_output_routes_absent": list(HISTORICAL_V2_ABSENT_ROUTES),
            "old_scientific_work_performed": False,
            "old_native_gate_emissions": 0,
            "original_CPU_seconds": None,
            "original_wall_seconds": None,
            "original_hard_budget_state_certified": False,
            "scientific_budget_censor_claim": None,
            "new_test_credit": 0,
            "failure_not_promoted_or_repaired": True,
        }

    def verify_v2_absence(self):
        self.check()
        require(
            not any(
                (PROGRAM / name).exists() or (PROGRAM / name).is_symlink()
                for name in HISTORICAL_V2_ABSENT_ROUTES
            ),
            "Historical V2 failed before its routes were created; no old retry",
        )

    def admit_v3_history(self):
        """Preserve the actual missing namespace-init admission failure unchanged."""
        for key, expected in HISTORICAL_V3_PINS.items():
            self.add(ROOT / key, expected)
        ready = self.read(ROOT / ".context/A20_signal_producer_ROOT_READY_run002.json")
        require(
            ready["schema"] == "A20-comparator-phase-static-READY-v3"
            and ready["role"] == "producer"
            and ready["ready"] is True
            and ready["budget"] == [CPU, WORK, WALL]
            and ready["output"] == "results/limitation_program_20261001/A20_signal_semantics_run002"
            and ready["author_sha256"]
            == {key: pin for key, pin in HISTORICAL_V3_PINS.items() if key.startswith("research/")}
            and ready["immutable_V2_history_SHA256"] == HISTORICAL_V2_PINS,
            "Exact immutable V3 release, six historical authors and original V2 pins",
        )
        log = self.read_bytes(ROOT / ".context/a20_signal_prepare_run002.log")
        require(
            log.startswith(b"\xef\xbb\xbf")
            and "FileNotFoundError: [WinError 2]" in log.decode("utf-8-sig")
            and r"limitation_program_20261001\\__init__.py" in log.decode("utf-8-sig"),
            "Exact raw UTF8-BOM missing namespace-init admission failure log",
        )
        self.verify_v3_absence()
        policy = self.read(RESEARCH / "a20_comparator_phase_implementation_preflight_v4.json")
        require(
            policy["immutable_V3_admission_history_expected_sha256"] == HISTORICAL_V3_PINS,
            "Prospective V4 method preserves every immutable V3 history pin",
        )
        self.history_v3 = {
            "schema": "A20-V3-pre-mkdir-admission-failure-history-v1",
            "historical_expected_sha256": HISTORICAL_V3_PINS,
            "failed_before_receipt_mkdir": True,
            "error_type": "FileNotFoundError",
            "error": "Missing namespace-package research/limitation_program_20261001/__init__.py",
            "historical_output_routes_absent": list(HISTORICAL_V3_ABSENT_ROUTES),
            "old_scientific_work_performed": False,
            "old_native_gate_emissions": 0,
            "original_CPU_seconds": None,
            "original_wall_seconds": None,
            "original_hard_budget_state_certified": False,
            "scientific_budget_censor_claim": None,
            "new_test_credit": 0,
            "failure_not_promoted_or_repaired": True,
        }

    def verify_v3_absence(self):
        self.check()
        require(
            not any(
                (PROGRAM / name).exists() or (PROGRAM / name).is_symlink()
                for name in HISTORICAL_V3_ABSENT_ROUTES
            ),
            "Historical V3 failed before its routes were created; no old retry or alias",
        )

    def admit_packet(self, directory, expected_manifest):
        directory = self.canonical(directory)
        require(
            directory.is_dir() and not any((directory / name).exists() for name in FAILURE_NAMES),
            "No failed/unsealed source packet",
        )
        manifest_path = self.add(directory / "manifest.json", expected_manifest)
        manifest = self.read(manifest_path)
        require(
            manifest.get("schema") == "A20-comparator-phase-component-manifest-v4"
            and manifest.get("role") == "producer"
            and manifest.get("passed") is True
            and manifest.get("completed") is True
            and manifest.get("budget_censored") is False
            and manifest.get("manifest_self_hash_excluded") is True,
            "Actual complete uncensored producer packet",
        )
        owned = set()
        for key, expected in manifest["files"].items():
            self.check()
            path = self.add(directory / key, expected)
            require(
                path.is_relative_to(directory)
                and path.relative_to(directory).as_posix() == key
                and path not in owned
                and path != manifest_path,
                "Unique canonical producer-owned member",
            )
            owned.add(path)
        require(
            self.inventory(directory) == owned | {manifest_path},
            "Exact producer actual owned inventory",
        )
        self.source_packets.append((directory, owned | {manifest_path}))
        for key, expected in manifest["frozen_inputs"].items():
            require((ROOT / key).relative_to(ROOT).as_posix() == key, "Canonical source frozen key")
            self.add(ROOT / key, expected)
        for key, expected in manifest["external_runtime_inputs"].items():
            require(
                Path(key).is_absolute() and str(Path(key)) == key,
                "Canonical scoped source external key",
            )
            self.add(Path(key), expected)
        self.verify()
        for name in ("summary.json", "completion_outcome.json"):
            data = self.read(directory / name)
            require(
                data.get("passed") is True
                and data.get("completed") is True
                and data.get("budget_censored") is False
                and data.get("new_test_credit") == 0
                and data.get("internal_component_checks") == 2608
                and data.get("full_G2") is False
                and data.get("adoption") is False,
                "Actual source outcome, scope and zero credit",
            )
        return manifest

    @staticmethod
    def creation_clock():
        require(os.name == "nt" and ctypes.sizeof(ctypes.c_void_p) == 8, "Pinned Win64")
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.GetCurrentProcess.argtypes, kernel.GetCurrentProcess.restype = [], wintypes.HANDLE
        kernel.GetProcessTimes.argtypes = [wintypes.HANDLE] + [
            ctypes.POINTER(wintypes.FILETIME)
        ] * 4
        kernel.GetProcessTimes.restype = wintypes.BOOL
        values = [wintypes.FILETIME() for _ in range(4)]
        require(
            kernel.GetProcessTimes(
                kernel.GetCurrentProcess(), *(ctypes.byref(value) for value in values)
            ),
            "Actual process creation clock",
        )
        ticks = (values[0].dwHighDateTime << 32) | values[0].dwLowDateTime
        age = time.time_ns() - (ticks - 116444736000000000) * 100
        require(age >= 0, "Actual creation precedes observation")
        return time.monotonic() - age / 1e9

    def check(self, admission=False):
        require(
            time.process_time() < (WORK if admission else CPU)
            and time.monotonic() - self.started < WALL,
            "Fixed A20 process CPU/wall guard",
        )

    @staticmethod
    def stamp(path):
        value = path.stat()
        return tuple(
            getattr(value, key, None)
            for key in (
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

    def canonical(self, path, fresh=False):
        self.check()
        lexical = Path(os.path.abspath(path))
        require(
            not lexical.is_relative_to(self.excluded)
            and not lexical.is_relative_to(self.excluded_actual),
            "Excluded base site lexical origin",
        )
        stamp = self.stamp(lexical)
        if not fresh and lexical in self.physical and self.physical[lexical][0] == stamp:
            return self.physical[lexical][1]
        actual = lexical.resolve(strict=True)
        require(
            actual == lexical and not actual.is_relative_to(self.excluded_actual),
            "No alias/reparse/excluded origin",
        )
        require(
            actual.is_relative_to(ROOT) or actual.is_relative_to(self.base),
            "Exact ROOT or scoped base runtime",
        )
        self.physical[lexical] = stamp, actual
        return actual

    def digest(self, path, fresh=False):
        path = self.canonical(path, fresh)
        stamp = self.stamp(path)
        if not fresh and path in self.cache and self.cache[path][0] == stamp:
            return self.cache[path][1]
        require(path.is_file() and stamp[2] <= 128 * 1024**2, "Bounded regular file")
        state, total = hashlib.sha256(), 0
        with path.open("rb") as stream:
            while chunk := stream.read(1 << 20):
                self.check()
                self.hash_work += len(chunk)
                total += len(chunk)
                require(
                    self.hash_work <= 24 * 1024**3 and total <= stamp[2], "Bounded stable hash work"
                )
                state.update(chunk)
        require(total == stamp[2] and self.stamp(path) == stamp, "Actual stable full byte SHA")
        digest = state.hexdigest()
        require(
            path not in self.observed or self.observed[path] == digest,
            "Previously observed actual bytes unchanged",
        )
        self.observed[path], self.cache[path] = digest, (stamp, digest)
        return digest

    def add(self, path, expected):
        self.references += 1
        require(
            self.references <= 100000 and isinstance(expected, str) and SHA.fullmatch(expected),
            "Fixed exact expected reference",
        )
        path = self.canonical(path)
        mapping, key = (
            (self.frozen, path.relative_to(ROOT).as_posix())
            if path.is_relative_to(ROOT)
            else (self.external, str(path))
        )
        require(key not in mapping or mapping[key] == expected, "Canonical equal-SHA guards")
        mapping[key] = expected
        return path

    def read_bytes(self, path):
        path = self.canonical(path)
        expected = (
            self.frozen.get(path.relative_to(ROOT).as_posix())
            if path.is_relative_to(ROOT)
            else self.external.get(str(path))
        )
        require(expected is not None and self.digest(path) == expected, "Read exact admitted bytes")
        before = self.stamp(path)
        require(before[2] <= 32 * 1024**2, "Bounded JSON/source bytes")
        with path.open("rb") as stream:
            chunks = []
            total = 0
            while chunk := stream.read(1 << 20):
                self.check()
                self.hash_work += len(chunk)
                total += len(chunk)
                require(
                    self.hash_work <= 24 * 1024**3 and total <= before[2],
                    "Charged stable bounded parsing bytes",
                )
                chunks.append(chunk)
        data = b"".join(chunks)
        require(
            total == before[2]
            and self.stamp(path) == before
            and hashlib.sha256(data).hexdigest() == expected,
            "Same exact parsed bytes",
        )
        self.check()
        return data

    def read(self, path):
        result = json.loads(self.read_bytes(path))
        self.check()
        return result

    def owner_memberships(self, owners):
        memberships = set()
        selected = self.ready["selected_prerequisite_sha256"]
        for key, expected in owners.items():
            path = self.add(ROOT / key, expected)
            require(path.name == "manifest.json", "Selected immutable owner manifest")
            packet = self.read(path)
            legacy_flat = "files" not in packet
            require(
                not any((path.parent / name).exists() for name in FAILURE_NAMES),
                "No failed premise owner",
            )
            if legacy_flat:
                require(
                    key
                    == "results/limitation_program_20261001/A10_coefficient_run001/manifest.json"
                    and expected
                    == "0a732d7f487bca1efd298e7eca4feb2f2d2e83d1958ebb9a14ee9b32a0d78a40"
                    and all(
                        isinstance(value, str) and SHA.fullmatch(value) for value in packet.values()
                    ),
                    "Only exact original A10 flat owner format",
                )
                packet = {"files": packet}
            require(isinstance(packet.get("files"), dict), "Owner files map")
            for field in ("files", "frozen_inputs"):
                for name, sha in packet.get(field, {}).items():
                    self.check()
                    self.references += 1
                    require(
                        self.references <= 100000, "Bounded selected owner membership references"
                    )
                    if field == "files":
                        # Only this exact hash-guarded legacy flat owner uses
                        # saved Windows separators. Modern maps stay strict.
                        spelling = name.replace("\\", "/") if legacy_flat else name
                        lexical = (
                            ROOT / spelling
                            if spelling.startswith(path.parent.relative_to(ROOT).as_posix() + "/")
                            else path.parent / spelling
                        )
                        selected_key = Path(os.path.abspath(lexical)).relative_to(ROOT).as_posix()
                        if selected_key not in selected:
                            continue
                        actual = lexical
                        actual = self.canonical(actual)
                        require(
                            actual.is_relative_to(path.parent), "Owned member confined to receipt"
                        )
                        require(
                            spelling
                            in (
                                actual.relative_to(ROOT).as_posix(),
                                actual.relative_to(path.parent).as_posix(),
                            ),
                            "Exact selected owned member spelling",
                        )
                    else:
                        if name not in selected:
                            continue
                        actual = self.canonical(ROOT / name)
                        require(
                            actual.relative_to(ROOT).as_posix() == name,
                            "Canonical frozen owner key",
                        )
                    require(isinstance(sha, str) and SHA.fullmatch(sha), "Owner exact SHA")
                    memberships.add((actual.relative_to(ROOT).as_posix(), sha))
        return memberships

    def verify(self, fresh=False):
        if fresh:
            self.verify_v2_absence()
            self.verify_v3_absence()
            self.verify_packet_inventory()
        union = {ROOT / key: value for key, value in self.frozen.items()}
        for key, value in self.external.items():
            require(
                Path(key) not in union or union[Path(key)] == value, "Canonical union equal SHA"
            )
            union[Path(key)] = value
        for path, value in self.observed.items():
            require(
                path not in union or union[path] == value,
                "Actual observations join immutable union",
            )
            union[path] = value
        size = 0
        for path in union:
            self.check()
            size += self.stamp(path)[2]
            require(size <= 8 * 1024**3, "Fixed8GiB unique input cap")
        for path, expected in sorted(union.items()):
            self.check()
            require(self.digest(path, fresh) == expected, "Full exact union verification")
        if fresh:
            self.verify_packet_inventory()
        return len(union)

    def verify_packet_inventory(self):
        for directory, expected in self.source_packets:
            self.check()
            require(
                not any((directory / name).exists() for name in FAILURE_NAMES)
                and self.inventory(directory) == expected,
                "Admitted source remains complete without new failure or unexpected owned members",
            )

    def inventory(self, directory):
        files, runtime_size, component_size, runtime_count, component_count = set(), 0, 0, 0, 0
        for base, directories, names in os.walk(directory, followlinks=False):
            self.check()
            for name in directories:
                path = self.canonical(Path(base) / name)
                require(
                    path.is_relative_to(directory) and not path.is_symlink(),
                    "Confined non-link owned directories",
                )
            for name in names:
                path = self.canonical(Path(base) / name)
                require(
                    path.is_relative_to(directory) and path not in files and path.is_file(),
                    "Unique confined owned file",
                )
                files.add(path)
                relative = path.relative_to(directory)
                if relative.parts[0] == "runtime_snapshot":
                    require(
                        len(relative.parts) == 2
                        and relative.name.isdecimal()
                        and str(int(relative.name)) == relative.name,
                        "Exact runtime snapshot member shape",
                    )
                    runtime_count += 1
                    runtime_size += path.stat().st_size
                    require(
                        runtime_count <= 24000 and runtime_size <= 2 * 1024**3,
                        "Separate complete runtime snapshot evidence cap",
                    )
                else:
                    component_count += 1
                    component_size += path.stat().st_size
                    require(
                        component_count <= 64 and component_size <= 128 * 1024**2,
                        "Separate fixed component evidence cap",
                    )
                require(len(files) <= 24064, "Combined prospectively declared owned cap")
        return files

    def runtime_paths(self):
        self.import_policy()
        prefix = Path(sys.prefix).resolve(strict=True)
        require(prefix == ROOT / ".context/frontier_t0_env", "Actual isolated prefix")
        self.check()
        config = (prefix / "pyvenv.cfg").read_text(encoding="utf-8")
        self.check()
        require("include-system-site-packages = false" in config.lower(), "No system-site runtime")
        roots = [self.base / "Lib", self.base / "DLLs", prefix / "Scripts"]
        found = set()
        absent = set()
        site = prefix / "Lib/site-packages"
        for root in (prefix, site):
            for path in root.iterdir():
                self.check()
                if path.is_file() and (
                    root == prefix or path.suffix in (".pth", ".py", ".pyc", ".pyd")
                ):
                    found.add(self.canonical(path))
                elif path.is_dir() and (
                    path.name == "__pycache__"
                    or (root == prefix and (path / "__init__.py").exists())
                    or path.name in ("sitecustomize", "usercustomize")
                ):
                    roots.append(self.canonical(path))
        for module in tuple(sys.modules.values()):
            for field in ("__file__", "__cached__"):
                name = getattr(module, field, None)
                if not name:
                    continue
                lexical = Path(os.path.abspath(name))
                require(
                    not lexical.is_relative_to(self.excluded)
                    and not lexical.resolve(strict=False).is_relative_to(self.excluded_actual),
                    "Excluded module/cache origin even if absent",
                )
                if lexical.is_relative_to(site):
                    relative = lexical.relative_to(site)
                    if len(relative.parts) > 1:
                        package = site / relative.parts[0]
                        if package.is_dir():
                            roots.append(self.canonical(package))
        for name in AUTHOR_NAMES:
            source = RESEARCH / name
            if source.suffix == ".py":
                found.add(self.canonical(source))
                cache = Path(importlib.util.cache_from_source(str(source)))
                if cache.exists():
                    found.add(self.canonical(cache))
                else:
                    absent.add(str(cache))

        def optional_init_member(path):
            self.check()
            require(
                path == Path(os.path.abspath(path))
                and not path.is_symlink()
                and path.resolve(strict=False) == path,
                "Exact package-init source/cache route including absent or dangling aliases",
            )
            if path.exists():
                require(path.is_file(), "Existing package-init source/cache is regular")
                found.add(self.canonical(path))
            else:
                absent.add(str(path))

        for source in (ROOT / "research/__init__.py", RESEARCH / "__init__.py"):
            self.canonical(source.parent)
            optional_init_member(source)
            optional_init_member(source.with_suffix(".pyc"))
            for optimization in ("", "1", "2"):
                optional_init_member(
                    Path(importlib.util.cache_from_source(str(source), optimization=optimization))
                )
            cache_directory = source.parent / "__pycache__"
            require(
                not cache_directory.is_symlink()
                and cache_directory.resolve(strict=False) == cache_directory,
                "Exact package-init cache directory including absent aliases",
            )
            if cache_directory.exists():
                require(cache_directory.is_dir(), "Package-init cache parent is a directory")
                self.canonical(cache_directory)
                for cache in cache_directory.glob("__init__*.pyc"):
                    optional_init_member(cache)
        for root in roots:
            require(root.is_dir(), "Declared runtime tree")
            for base, directories, names in os.walk(root, topdown=True, followlinks=False):
                self.check()
                directories[:] = [
                    name for name in directories if Path(base) / name != self.excluded
                ]
                for name in directories:
                    directory = self.canonical(Path(base) / name)
                    require(
                        directory.is_relative_to(root) and not directory.is_symlink(),
                        "Every runtime directory including empty aliases is confined",
                    )
                for name in names:
                    found.add(self.canonical(Path(base) / name))
        for root in (prefix, self.base):
            for path in root.iterdir():
                self.check()
                if path.is_file():
                    found.add(self.canonical(path))
        allowed_search = {
            ROOT,
            prefix,
            site,
            self.base,
            self.base / "Lib",
            self.base / "DLLs",
            self.base / "python312.zip",
        }
        for name in sys.path:
            lexical = Path(os.path.abspath(name or ROOT))
            require(
                lexical in allowed_search and not lexical.is_relative_to(self.excluded),
                "Declared finite sys.path",
            )
            if lexical.is_file():
                found.add(self.canonical(lexical))
            elif not lexical.exists():
                absent.add(str(lexical))
        for module in tuple(sys.modules.values()):
            for field in ("__file__", "__cached__"):
                name = getattr(module, field, None)
                if not name:
                    continue
                lexical = Path(os.path.abspath(name))
                require(
                    not lexical.is_relative_to(self.excluded)
                    and not lexical.resolve(strict=False).is_relative_to(self.excluded_actual),
                    "Excluded module/cache origin even if absent",
                )
                if lexical.exists():
                    actual = self.canonical(lexical)
                    require(
                        actual.is_relative_to(self.base)
                        or actual.is_relative_to(prefix)
                        or actual.is_relative_to(RESEARCH)
                        or actual
                        in (
                            ROOT / "research/__init__.py",
                            ROOT / "research/__init__.pyc",
                            ROOT / "research/__pycache__/__init__.cpython-312.pyc",
                        ),
                        "Bounded loaded origin",
                    )
                    found.add(actual)
                elif (
                    lexical.is_relative_to(self.base)
                    or lexical.is_relative_to(prefix)
                    or lexical.is_relative_to(RESEARCH)
                    or lexical
                    in (
                        ROOT / "research/__init__.pyc",
                        ROOT / "research/__pycache__/__init__.cpython-312.pyc",
                    )
                ):
                    absent.add(str(lexical))
                else:
                    require(False, "Unexpected absent loaded origin")
        size = 0
        for path in found:
            self.check()
            size += self.stamp(path)[2]
            require(len(found) <= 24000 and size <= 2 * 1024**3, "Fixed full reachable runtime cap")
        self.runtime_absent = sorted(absent)
        return sorted(found)

    def verify_loaded(self, protocol):
        self.import_policy()
        require(
            [str(path) for path in self.runtime_paths()] == protocol["runtime_paths"]
            and self.runtime_absent == protocol["runtime_absent"],
            "Complete runtime and absence inventory unchanged",
        )
        for module in tuple(sys.modules.values()):
            for field in ("__file__", "__cached__"):
                name = getattr(module, field, None)
                if name and Path(name).exists():
                    path = self.canonical(name)
                    expected = (
                        self.frozen.get(path.relative_to(ROOT).as_posix())
                        if path.is_relative_to(ROOT)
                        else self.external.get(str(path))
                    )
                    require(
                        expected is not None and self.digest(path) == expected,
                        "Every actual loaded origin/cache has captured exact bytes",
                    )

    def import_policy(self):
        forbidden = ("numpy", "numba", "scipy", "mpmath", "pytest", "qiskit", "cirq", "psutil")
        forbidden += (
            "research.limitation_program_20261001.arithmetic_free_basket_signal_v2",
            "research.limitation_program_20261001.experiment_arithmetic_free_basket_signal_v2",
            "research.limitation_program_20261001.audit_arithmetic_free_basket_signal_v2",
            "research.limitation_program_20261001.a20_signal_receipt_v2",
        )
        forbidden += (
            "research.limitation_program_20261001.arithmetic_free_basket_signal_v3",
            "research.limitation_program_20261001.experiment_arithmetic_free_basket_signal_v3",
            "research.limitation_program_20261001.audit_arithmetic_free_basket_signal_v3",
            "research.limitation_program_20261001.a20_signal_receipt_v3",
        )
        if self.role == "audit":
            forbidden += (
                "research.limitation_program_20261001.arithmetic_free_basket_signal_v4",
                "research.limitation_program_20261001.experiment_arithmetic_free_basket_signal_v4",
            )
        require(
            not any(
                name == prefix or name.startswith(prefix + ".")
                for name in sys.modules
                for prefix in forbidden
            ),
            "Stdlib-only component and independent auditor import policy",
        )

    def reserve_owned(self, path, size):
        """Enforce all prospective owned caps before opening a new file."""
        self.check()
        require(
            type(size) is int and 0 <= size <= 128 * 1024**2,
            "Bounded prospective owned file",
        )
        require(
            path.is_relative_to(self.output)
            and path.resolve(strict=False) == path
            and not path.exists(),
            "Confined canonical exclusive owned target",
        )
        if self.owned_usage is None:
            usage = [0, 0, 0, 0]
            current = self.inventory(self.output)
            require(
                current == self.owned_expected,
                "Only the explicitly admitted inventory initializes owned capacity",
            )
            for existing in current:
                self.check()
                kind = 0 if existing.relative_to(self.output).parts[0] == "runtime_snapshot" else 2
                usage[kind] += 1
                usage[kind + 1] += self.stamp(existing)[2]
            self.owned_usage = usage
        relative = path.relative_to(self.output)
        runtime = relative.parts[0] == "runtime_snapshot"
        if runtime:
            require(
                len(relative.parts) == 2
                and relative.name.isdecimal()
                and str(int(relative.name)) == relative.name,
                "Exact new runtime snapshot member shape",
            )
        index = 0 if runtime else 2
        updated = self.owned_usage.copy()
        updated[index] += 1
        updated[index + 1] += size
        require(
            updated[0] <= 24000
            and updated[1] <= 2 * 1024**3
            and updated[2] <= 64
            and updated[3] <= 128 * 1024**2
            and updated[0] + updated[2] <= 24064,
            "Prospective runtime, component and combined owned caps before mutation",
        )
        self.owned_usage = updated
        self.owned_expected.add(path)

    def write(self, name, value):
        self.check()
        data = json.dumps(value, sort_keys=True, indent=2, allow_nan=False).encode() + b"\n"
        self.check()
        require(len(data) <= 32 * 1024**2, "Bounded new JSON artifact")
        path = self.output / name
        path.parent.mkdir(parents=True, exist_ok=True)
        require(path.resolve(strict=False).is_relative_to(self.output), "Confined exclusive output")
        self.reserve_owned(path, len(data))
        with path.open("xb") as stream:
            for offset in range(0, len(data), 1 << 20):
                self.check()
                stream.write(data[offset : offset + (1 << 20)])
        self.check()
        require(
            self.digest(path, True) == hashlib.sha256(data).hexdigest(),
            "Fresh output-byte verification",
        )
        return path

    def prepare(self):
        require(not self.output.exists(), "Fresh exclusive receipt; no retry")
        runtime = self.runtime_paths()
        runtime_absent = self.runtime_absent.copy()
        self.check(admission=True)
        self.output.mkdir()
        self.mutated = True
        copies = {}
        for index, path in enumerate(runtime):
            self.check(admission=True)
            expected = self.digest(path, True)
            self.add(path, expected)
            target = self.output / "runtime_snapshot" / str(index)
            target.parent.mkdir(exist_ok=True)
            self.reserve_owned(target, self.stamp(path)[2])
            with path.open("rb") as source, target.open("xb") as sink:
                while chunk := source.read(1 << 20):
                    self.check(admission=True)
                    self.hash_work += len(chunk)
                    require(self.hash_work <= 24 * 1024**3, "Charged runtime copy/read work")
                    sink.write(chunk)
            require(
                self.digest(target, True) == expected and self.digest(path, True) == expected,
                "Actual snapshot matches live runtime expected bytes",
            )
            self.add(target, expected)
            copies[str(path)] = target.relative_to(ROOT).as_posix()
        for name in AUTHOR_NAMES:
            source = RESEARCH / name
            data = self.read_bytes(source)
            target = self.output / "executed_dependencies" / name
            target.parent.mkdir(exist_ok=True)
            self.reserve_owned(target, len(data))
            with target.open("xb") as sink:
                sink.write(data)
            self.add(target, self.frozen[source.relative_to(ROOT).as_posix()])
        history_copies = {}
        for key, expected in {**HISTORICAL_V2_PINS, **HISTORICAL_V3_PINS}.items():
            self.check(admission=True)
            source = ROOT / key
            data = self.read_bytes(source)
            target = self.output / "admission_history" / source.name
            target.parent.mkdir(exist_ok=True)
            self.reserve_owned(target, len(data))
            with target.open("xb") as sink:
                sink.write(data)
            self.add(target, expected)
            history_copies[key] = target.relative_to(ROOT).as_posix()
        v2_copies = {key: history_copies[key] for key in HISTORICAL_V2_PINS}
        v3_copies = {key: history_copies[key] for key in HISTORICAL_V3_PINS}
        self.write("V2_admission_history.json", {**self.history, "exact_byte_copies": v2_copies})
        self.write("V3_admission_history.json", {**self.history_v3, "exact_byte_copies": v3_copies})
        require(
            self.inventory(self.output) == self.owned_expected,
            "Exact freshly created prepared owned inventory",
        )
        self.verify(True)
        require(
            self.runtime_paths() == runtime and self.runtime_absent == runtime_absent,
            "Complete prepared runtime presence and exact absence remain unchanged",
        )
        self.check(admission=True)
        prepared_owned = {
            path.relative_to(self.output).as_posix(): self.digest(path)
            for path in sorted(self.owned_expected)
        }
        path = self.write(
            "protocol.json",
            {
                "schema": "A20-comparator-phase-prepared-protocol-v4",
                "role": self.role,
                "budget": [CPU, WORK, WALL],
                "root_READY_sha256": self.digest(self.ready_path),
                "frozen_inputs": self.frozen,
                "external_runtime_inputs": self.external,
                "runtime_live_to_snapshot": copies,
                "runtime_paths": [str(path) for path in runtime],
                "runtime_absent": self.runtime_absent,
                "immutable_V2_admission_failure_history": self.history,
                "immutable_V2_history_live_to_snapshot": v2_copies,
                "immutable_V3_admission_failure_history": self.history_v3,
                "immutable_V3_history_live_to_snapshot": v3_copies,
                "prepared_owned_files_protocol_self_hash_excluded": prepared_owned,
                "component_gate_emission_permitted_after_run_admission": True,
                "full_pricing_source_emission": False,
                "internal_checks_not_financial_fixtures": True,
            },
        )
        require(
            self.inventory(self.output) == self.owned_expected,
            "Exact complete prepared owned inventory after protocol write",
        )
        self.check()
        return self.digest(path, True)

    def admit_run(self, protocol_sha):
        require(
            self.output.is_dir()
            and not any(
                (self.output / name).exists()
                for name in ("manifest.json", "completion_outcome.json", "RUN_STARTED.json")
                + FAILURE_NAMES
            ),
            "One run of complete prepared receipt",
        )
        protocol_path = self.output / "protocol.json"
        self.add(protocol_path, protocol_sha)
        protocol = self.read(protocol_path)
        require(
            protocol["schema"] == "A20-comparator-phase-prepared-protocol-v4"
            and protocol["role"] == self.role
            and protocol["root_READY_sha256"] == self.digest(self.ready_path)
            and protocol["immutable_V2_admission_failure_history"] == self.history
            and protocol["immutable_V3_admission_failure_history"] == self.history_v3,
            "Same prepared protocol/root READY",
        )
        prepared_owned = set()
        for key, expected in protocol["prepared_owned_files_protocol_self_hash_excluded"].items():
            path = self.add(self.output / key, expected)
            require(
                path.is_relative_to(self.output)
                and path.relative_to(self.output).as_posix() == key
                and path != protocol_path
                and path not in prepared_owned,
                "Unique canonical prepared owned member",
            )
            prepared_owned.add(path)
        require(
            self.inventory(self.output) == prepared_owned | {protocol_path},
            "Exactly prepared owned inventory before exclusive run admission",
        )
        self.owned_expected = prepared_owned | {protocol_path}
        self.mutated = True
        self.write(
            "RUN_STARTED.json",
            {
                "role": self.role,
                "prepared_protocol_sha256": protocol_sha,
                "exclusive_no_retry": True,
                "process_CPU_seconds": time.process_time(),
                "creation_wall_seconds": time.monotonic() - self.started,
            },
        )
        for key, expected in protocol["frozen_inputs"].items():
            require((ROOT / key).relative_to(ROOT).as_posix() == key, "Canonical prepared ROOT key")
            self.add(ROOT / key, expected)
        for key, expected in protocol["external_runtime_inputs"].items():
            self.add(Path(key), expected)
        require(
            [str(path) for path in self.runtime_paths()] == protocol["runtime_paths"],
            "Complete actual runtime inventory unchanged",
        )
        require(
            self.runtime_absent == protocol["runtime_absent"],
            "Exact previously absent bytecode/zip origins still absent",
        )
        self.verify(True)
        self.check(admission=True)
        self.mutated = True
        return protocol

    def seal(self, summary):
        self.write("summary.json", summary)
        self.write("completion_outcome.json", {**summary, "authoritative_terminal_outcome": True})
        count = self.verify(True)
        self.check()
        owned = self.inventory(self.output)
        require(
            owned == self.owned_expected, "Exactly admitted and newly created terminal owned files"
        )
        files = {
            path.relative_to(self.output).as_posix(): self.digest(path, True)
            for path in sorted(owned)
        }
        self.check()
        manifest = {
            "schema": "A20-comparator-phase-component-manifest-v4",
            "role": self.role,
            "passed": True,
            "completed": True,
            "budget_censored": False,
            "files": files,
            "frozen_inputs": self.frozen,
            "external_runtime_inputs": self.external,
            "manifest_self_hash_excluded": True,
            "fresh_union_paths": count,
            "all_original_scientific_scopes_retained": True,
            "new_test_credit": 0,
        }
        self.write("manifest.json", manifest)
        require(
            self.inventory(self.output) == owned | {self.output / "manifest.json"},
            "Exact terminal owned inventory",
        )
        self.check()

    def fail(self, error):
        if not self.mutated or not self.output.exists():
            return
        manifest = self.output / "manifest.json"
        try:
            if manifest.exists():
                manifest.rename(self.output / "failed_manifest_attempt.json")
        except OSError:
            pass
        marker = (
            b'{"passed":false,"authoritative_failure":true,"budget_censored":null,'
            b'"hard_budget_state_uncertified":true,"new_test_credit":0,"adoption":false}\n'
        )
        try:
            with (self.output / "FAILED_UNSEALED.json").open("xb") as stream:
                stream.write(marker)
        except OSError:
            pass
        try:
            self.check()
            self.write(
                "failure.json",
                {
                    "passed": False,
                    "error_type": type(error).__name__,
                    "message": str(error)[:4096],
                    "budget": [CPU, WORK, WALL],
                    "new_test_credit": 0,
                    "adoption": False,
                },
            )
        except BaseException:
            pass
