"""Prospective E12 toy controller. Run only after an independent ROOT release.

The numerical certificate uses integers and rational numbers, not simulation
coverage. Pseudorandom traces are explicitly diagnostics, never an IID proof.
No finance implementation is imported, evaluated, or modified.
"""

from __future__ import annotations
import argparse
import ctypes
from ctypes import wintypes
from fractions import Fraction
import hashlib
import json
from math import isqrt
import os
from pathlib import Path
import random
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "research/limitation_program_20261001"
AUTHOR = HERE / "experiment_e12_anytime_moment_v1.py"
METHOD_MD = HERE / "E12_ANYTIME_MOMENT_PREFLIGHT_V1.md"
METHOD_JSON = HERE / "e12_anytime_moment_preflight_v1.json"
READY = ROOT / ".context/E12_anytime_moment_ROOT_READY_run001.json"
OUTPUT = ROOT / "results/limitation_program_20261001/E12_anytime_moment_run001"
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
BASE = Path("C:/Users/prith/AppData/Local/Programs/Python/Python312")
LAUNCHER_SHA = "41123879d2e991377997acadf5f0cf8f34fa10d86362eded8c69b6041e2893b5"
BASE_SHA = "fd5c46d73d29ba21b04c844bbaf9096066136526911230645a2a040d23fb612b"
REFERENCES = {
    "research/controlled_residual_feasibility/parity_iid.py": (
        "ea0866039c2d2998c1e9ebfa53b94a027a13ab6d21e173ee6e358474a352804d"
    ),
    "docs/limitation_audit_20261001/implementation_plan/roadmap.json": (
        "59333ddeba6ee73950cba5a7a669fdc6dd3a9db8629297335d507b65c6a02b6a"
    ),
    "docs/limitation_audit_20261001/ESTIMATION_AND_CERTIFICATION.md": (
        "e5189e840fc88fa1a1f73b08659c76257aa84c916b6873a8730ec9f7c53c6fad"
    ),
}
CPU_LIMIT, WORK_LIMIT, WALL_LIMIT = (180, 150, 600)
MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = (4096, 512 << 20)
MAX_FROZEN_FILES, MAX_FROZEN_BYTES = (16, 8 << 20)
MAX_OWNED_FILES, MAX_OWNED_BYTES = (16, 16 << 20)
MAX_SINGLE_BYTES = 64 << 20
SHA = re.compile("[0-9a-f]{64}\\Z")
ALPHA = Fraction(1, 1000)
CS_ALPHA = FALLBACK_ALPHA = ALPHA / 2
LAMBDAS = tuple((Fraction(1, 1 << j) for j in range(1, 17)))
CS_LOG_MAJORANT, FIXED_LOG_MAJORANT = (12, 9)
PRECISION = Fraction(1, 128)
N_CAP = 1 << 17
LOOKS = tuple((1 << j for j in range(6, 18)))
LAW_BITS = (1, 8, 16)
SEEDS = tuple((202610040000 + j for j in range(16)))
SQRT_BITS = 64
_ABSENT_CACHES = set()
_ATTEMPT_ROUTE_OWNED = False


def require(value, message):
    if not value:
        raise ValueError(message)


def started_clock():
    require(sys.platform == "win32", "Frozen experiment requires Windows")
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
    kernel.GetProcessTimes.restype = wintypes.BOOL
    values = [wintypes.FILETIME() for _ in range(4)]
    require(
        kernel.GetProcessTimes(kernel.GetCurrentProcess(), *(ctypes.byref(x) for x in values)),
        "Actual process creation time",
    )
    ticks = values[0].dwHighDateTime << 32 | values[0].dwLowDateTime
    elapsed = (time.time_ns() - (ticks - 116444736000000000) * 100) / 1000000000
    require(elapsed >= 0, "Nonnegative process age")
    return time.monotonic() - elapsed


def guard(started, admission=False):
    cpu, wall = (time.process_time(), time.monotonic() - started)
    if cpu >= (WORK_LIMIT if admission else CPU_LIMIT) or wall >= WALL_LIMIT:
        raise RuntimeError(f"E12 fixed budget reached: CPU={cpu}, wall={wall}")
    return (cpu, wall)


def stable_read(path, started):
    guard(started)
    require(
        path.is_absolute() and path.resolve(strict=True) == path, "Exact absolute path, no alias"
    )
    before = path.stat()
    require(path.is_file() and before.st_size <= MAX_SINGLE_BYTES, "Finite regular input")
    parts = []
    with path.open("rb") as stream:
        while True:
            guard(started)
            part = stream.read(1 << 20)
            if not part:
                break
            parts.append(part)
            require(sum(map(len, parts)) <= MAX_SINGLE_BYTES, "Bounded file read")
    data = b"".join(parts)
    after = path.stat()
    fields = (
        "st_dev",
        "st_ino",
        "st_size",
        "st_mtime_ns",
        "st_ctime_ns",
        "st_mode",
        "st_file_attributes",
        "st_reparse_tag",
    )
    require(all((getattr(before, k) == getattr(after, k) for k in fields)), "Stable file identity")
    require(path.resolve(strict=True) == path, "Exact nonredirected input after complete read")
    require(len(data) == before.st_size, "Full observed byte count")
    guard(started)
    return data


def checked_read(path, expected, started):
    require(isinstance(expected, str) and SHA.fullmatch(expected), "Exact expected SHA-256")
    data = stable_read(path, started)
    require(hashlib.sha256(data).hexdigest() == expected, "Fresh bytes equal frozen expected SHA")
    return data


def rational(value):
    return [value.numerator, value.denominator]


def write_json(path, value, started):
    guard(started)
    require(
        path.parent == OUTPUT and OUTPUT.resolve(strict=True) == OUTPUT,
        "Exact confined owned output directory",
    )
    require(not path.exists() and (not path.is_symlink()), "New owned output only")
    prior = set(OUTPUT.iterdir())
    prior_bytes = 0
    for member in prior:
        guard(started)
        require(
            member.is_file() and member.resolve(strict=True) == member,
            "Existing owned members are confined regular files",
        )
        prior_bytes += member.stat().st_size
    require(
        len(prior) + 1 <= MAX_OWNED_FILES and prior_bytes < MAX_OWNED_BYTES,
        "Prospective exclusive write stays within owned capacities",
    )
    encoded_bytes = 1
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        for fragment in json.JSONEncoder(indent=2, sort_keys=True, allow_nan=False).iterencode(
            value
        ):
            guard(started)
            encoded_bytes += len(fragment.encode("utf-8"))
            require(encoded_bytes <= MAX_SINGLE_BYTES, "Bounded exclusive JSON encoding")
            require(
                prior_bytes + encoded_bytes <= MAX_OWNED_BYTES,
                "Guarded encoded bytes stay within remaining owned capacity",
            )
            stream.write(fragment)
            guard(started)
        stream.write("\n")
    require(path.stat().st_size == encoded_bytes, "Exact actual UTF8 owned byte count")
    actual = set(OUTPUT.iterdir())
    require(
        actual == prior | {path} and len(actual) <= MAX_OWNED_FILES,
        "Exact guarded write ownership count",
    )
    actual_bytes = 0
    for member in actual:
        guard(started)
        require(
            member.is_file() and member.resolve(strict=True) == member,
            "Final written owned members retain exact routes",
        )
        actual_bytes += member.stat().st_size
    require(
        actual_bytes == prior_bytes + encoded_bytes <= MAX_OWNED_BYTES,
        "Actual complete guarded write ownership bytes",
    )
    guard(started)


def relative(path):
    return path.relative_to(ROOT).as_posix()


def invocation_check(started):
    require(sys.version_info[:3] == (3, 12, 4), "Pinned Python 3.12.4")
    require(sys.flags.isolated == 1 and sys.flags.no_site == 1, "Use -I -S")
    require(sys.dont_write_bytecode, "Use -B")
    require(Path(sys.executable).resolve(strict=True) == LAUNCHER, "Actual pinned launcher")
    require(Path(sys.base_prefix).resolve(strict=True) == BASE, "Actual pinned interpreter root")
    require(Path(sys.prefix).resolve(strict=True) == BASE, "No-site base interpreter prefix")
    expected_path = [str(BASE / "python312.zip"), str(BASE / "DLLs"), str(BASE / "Lib"), str(BASE)]
    require(sys.path == expected_path, "Exact isolated standard-library search path")
    require(not (BASE / "python312.zip").exists(), "Frozen absent runtime ZIP")
    require(not (BASE / "python312.zip").is_symlink(), "No dangling alias for absent runtime ZIP")
    require(
        not any((name == "site" or name.startswith("research.") for name in sys.modules)),
        "No site startup or scientific module admitted",
    )
    checked_read(LAUNCHER, LAUNCHER_SHA, started)
    checked_read(BASE / "python.exe", BASE_SHA, started)


def root_release(expected, started):
    raw = checked_read(READY, expected, started)
    ready = json.loads(raw)
    require(ready.get("schema") == "root-e12-anytime-moment-static-READY-v1", "Exact ROOT header")
    require(
        ready.get("passed") is True and ready.get("static_review_only") is True,
        "ROOT static release",
    )
    require(
        ready.get("scientific_execution_approved") is True, "Explicit bounded toy execution release"
    )
    require(ready.get("financial_adoption_approved") is False, "No financial promotion")
    expected_keys = {relative(AUTHOR), relative(METHOD_MD), relative(METHOD_JSON)} | set(REFERENCES)
    mapping = ready.get("frozen_inputs")
    require(
        isinstance(mapping, dict) and set(mapping) == expected_keys, "Exact six-input source packet"
    )
    require(
        all((mapping[k] == v for k, v in REFERENCES.items())), "Unchanged reference expected hashes"
    )
    total = 0
    for name, digest in mapping.items():
        total += len(checked_read(ROOT / name, digest, started))
    require(
        len(mapping) + 1 <= MAX_FROZEN_FILES and total + len(raw) <= MAX_FROZEN_BYTES,
        "Bounded frozen source includes ROOT_READY",
    )
    method = json.loads(checked_read(METHOD_JSON, mapping[relative(METHOD_JSON)], started))
    require(method.get("schema") == "e12-anytime-moment-preflight-v1", "Frozen method schema")
    require(method.get("output_route") == relative(OUTPUT), "Frozen exact output route")
    require(
        method.get("numerical_kernel") == "rational-finite-union-zero-predictor",
        "Exact selected kernel",
    )
    mapping = dict(mapping)
    mapping[relative(READY)] = expected
    return mapping


def runtime_packet(started):
    paths = {LAUNCHER, BASE / "python.exe"}
    require(BASE.resolve(strict=True) == BASE, "Exact base interpreter directory")
    for path in BASE.iterdir():
        guard(started)
        if path.is_file():
            paths.add(path)
    for tree in (BASE / "Lib", BASE / "DLLs"):
        for directory, names, files in os.walk(tree, followlinks=False):
            guard(started)
            parent = Path(directory)
            require(
                parent.resolve(strict=True) == parent, "Runtime inventory does not follow aliases"
            )
            names[:] = [name for name in names if name.casefold() != "site-packages"]
            for name in names:
                child = parent / name
                require(
                    not child.is_symlink() and child.resolve(strict=True) == child,
                    "No silently skipped runtime directory alias",
                )
            paths.update((parent / name for name in files))
            require(len(paths) <= MAX_RUNTIME_FILES, "Finite isolated runtime file count")
    mapping, total = ({}, 0)
    for path in sorted(paths, key=str):
        data = stable_read(path, started)
        total += len(data)
        require(total <= MAX_RUNTIME_BYTES, "Finite isolated runtime byte count")
        mapping[str(path)] = hashlib.sha256(data).hexdigest()
    return (mapping, total)


def loaded_runtime_check(runtime, started):
    origins = set()
    for module in tuple(sys.modules.values()):
        guard(started)
        spec = getattr(module, "__spec__", None)
        origin = getattr(spec, "origin", None)
        if origin in (None, "built-in", "frozen"):
            continue
        path = Path(origin)
        require(
            path.is_absolute() and path.resolve(strict=True) == path,
            "Loaded runtime origin has no lexical alias",
        )
        require(str(path) in runtime, "Every imported runtime module has a frozen input")
        origins.add(str(path))
        cache = getattr(spec, "cached", None)
        if cache:
            cache_path = Path(cache)
            require(cache_path.is_absolute(), "Declared loaded cache has an absolute route")
            if cache_path.exists():
                require(
                    cache_path.resolve(strict=True) == cache_path and str(cache_path) in runtime,
                    "Existing imported bytecode is exact and frozen",
                )
            else:
                require(not cache_path.is_symlink(), "No dangling alias for absent loaded cache")
                _ABSENT_CACHES.add(cache_path)
    require(
        not any((path.exists() or path.is_symlink() for path in _ABSENT_CACHES)),
        "Every declared absent loaded cache remains absent",
    )
    return len(origins)


def rehash(mapping, runtime, started, protocol_expected=None):
    invocation_check(started)
    current, _ = runtime_packet(started)
    require(current == runtime, "Complete runtime tree membership and hashes remain frozen")
    total = 0
    for key, digest in mapping.items():
        total += len(checked_read(ROOT / key, digest, started))
    for key, digest in runtime.items():
        total += len(checked_read(Path(key), digest, started))
    if protocol_expected is not None:
        total += len(checked_read(OUTPUT / "protocol.json", protocol_expected, started))
    return {
        "unique_paths": len(mapping) + len(runtime) + int(protocol_expected is not None),
        "bytes": total,
        "sha_mismatches": 0,
        "expected_hash_waivers": 0,
        "loaded_module_origins": loaded_runtime_check(runtime, started),
    }


def exp_lower(integer, terms, started):
    term = total = Fraction(1)
    for k in range(1, terms + 1):
        guard(started)
        term *= Fraction(integer, k)
        total += term
    return total


def boundary(v):
    require(isinstance(v, Fraction) and v >= 0, "Exact nonnegative empirical process")
    return min(((CS_LOG_MAJORANT + lam * lam * v / (2 * (1 - lam))) / lam for lam in LAMBDAS))


def boundary_integer_oracle(k):
    require(isinstance(k, int) and k >= 0, "Integer Bernoulli count")
    return min(
        (Fraction(24 * d * (d - 1) + k, 2 * (d - 1)) for d in (1 << j for j in range(1, 17)))
    )


def sqrt_upper(value):
    require(isinstance(value, Fraction) and value >= 0, "Nonnegative rational square-root input")
    scale = 1 << SQRT_BITS
    numerator = value.numerator * scale * scale
    floor = isqrt(numerator // value.denominator)
    ceil = floor if floor * floor * value.denominator == numerator else floor + 1
    return Fraction(ceil, scale)


def fixed_radius(n, k):
    require(
        isinstance(n, int) and isinstance(k, int) and (n >= 2) and (0 <= k <= n),
        "Valid fixed-N count",
    )
    variance = Fraction(k * (n - k), n * (n - 1))
    return sqrt_upper(Fraction(2 * FIXED_LOG_MAJORANT, n) * variance) + Fraction(
        7 * FIXED_LOG_MAJORANT, 3 * (n - 1)
    )


def structural_checks(started):
    per_sign_per_lambda = CS_ALPHA / (2 * len(LAMBDAS))
    cs_exp = exp_lower(CS_LOG_MAJORANT, 64, started)
    fixed_exp = exp_lower(FIXED_LOG_MAJORANT, 64, started)
    require(cs_exp > 1 / per_sign_per_lambda, "Strict rational proof of CS logarithm majorant")
    require(fixed_exp > 4 / FALLBACK_ALPHA, "Strict rational proof of fixed-N logarithm majorant")
    require(CS_ALPHA + FALLBACK_ALPHA == ALPHA, "Complete optional fallback failure allocation")
    require(boundary(Fraction(0)) == 24, "Zero observations have a positive confidence term")
    radius_max = sqrt_upper(Fraction(FIXED_LOG_MAJORANT, 2 * (N_CAP - 1))) + Fraction(21, N_CAP - 1)
    require(
        radius_max < PRECISION, "Fixed-N fallback passes the tolerance for every Bernoulli dataset"
    )
    history_count = 0
    for n in range(1, 9):
        totals = {bits: Fraction(0) for bits in LAW_BITS}
        for mask in range(1 << n):
            guard(started, admission=True)
            k = mask.bit_count()
            require(
                boundary(Fraction(k)) == boundary_integer_oracle(k),
                "Independent boundary expression",
            )
            for bits in LAW_BITS:
                p = Fraction(1, 1 << bits)
                totals[bits] += p**k * (1 - p) ** (n - k)
            history_count += 1
        require(
            all((value == 1 for value in totals.values())), "Exact complete history normalization"
        )
    sqrt_cases = (
        Fraction(0),
        Fraction(1),
        Fraction(2),
        Fraction(1, 3),
        Fraction(1, 1 << 128),
        Fraction(17, 31),
        Fraction(10**40 + 1, 10**20 + 3),
    )
    for value in sqrt_cases:
        upper = sqrt_upper(value)
        require(upper * upper >= value, "Exact upward square-root enclosure")
        previous = upper - Fraction(1, 1 << SQRT_BITS)
        require(upper == 0 or previous * previous < value, "Minimal dyadic square-root enclosure")
    checks = [
        {
            "id": "log-majorants",
            "passed": True,
            "cs_exp_lower": rational(cs_exp),
            "fixed_exp_lower": rational(fixed_exp),
            "per_sign_per_lambda_failure": rational(per_sign_per_lambda),
        },
        {"id": "all-data-fallback-radius", "passed": True, "radius_upper": rational(radius_max)},
        {
            "id": "complete-short-histories",
            "passed": True,
            "history_count": history_count,
            "laws": [rational(Fraction(1, 1 << b)) for b in LAW_BITS],
            "coverage_proof": False,
        },
        {"id": "sqrt-enclosures", "passed": True, "cases": len(sqrt_cases)},
        {
            "id": "zero-observation-term",
            "passed": True,
            "sum_bound": rational(boundary(Fraction(0))),
        },
    ]
    return checks


def diagnostic_trace(bits, seed, started):
    require(bits in LAW_BITS and seed in SEEDS, "Predeclared toy law and seed")
    generator = random.Random(seed)
    count, previous = (0, 0)
    stop, stop_count, stop_radius = (None, None, None)
    looks = []
    for n in LOOKS:
        guard(started, admission=True)
        for _ in range(n - previous):
            if _ % 4096 == 0:
                guard(started, admission=True)
            count += generator.getrandbits(bits) == 0
        radius = boundary(Fraction(count)) / n
        require(
            boundary_integer_oracle(count) / n == radius, "Independent exact trajectory boundary"
        )
        looks.append({"n": n, "count": count, "radius": rational(radius)})
        if stop is None and radius <= PRECISION:
            stop, stop_count, stop_radius = (n, count, radius)
        previous = n
    fixed = fixed_radius(N_CAP, count)
    require(fixed <= PRECISION, "Guaranteed capped fallback precision")
    chosen_n = N_CAP if stop is None else stop
    chosen_k = count if stop is None else stop_count
    chosen_radius = fixed if stop is None else stop_radius
    p = Fraction(1, 1 << bits)
    mean = Fraction(chosen_k, chosen_n)
    lo, hi = (max(Fraction(0), mean - chosen_radius), min(Fraction(1), mean + chosen_radius))
    return {
        "law": rational(p),
        "bits": bits,
        "seed": seed,
        "looks": looks,
        "selected_branch": "fixed-N-fallback" if stop is None else "anytime-CS",
        "selected_samples": chosen_n,
        "selected_count": chosen_k,
        "selected_radius": rational(chosen_radius),
        "selected_interval": [rational(lo), rational(hi)],
        "diagnostic_truth_in_interval": lo <= p <= hi,
        "fixed_baseline_samples": N_CAP,
        "fixed_baseline_count": count,
        "fixed_baseline_radius": rational(fixed),
        "draws_actually_generated_for_paired_diagnostic": N_CAP,
        "sample_saving_is_controller_count_not_measured_financial_latency": True,
        "pseudorandom_trace_is_iid_proof": False,
    }


def protocol_value(frozen, runtime, runtime_bytes):
    return {
        "schema": "e12-anytime-moment-protocol-v1",
        "local_only": True,
        "scientific_scope": (
            "Toy statistical controller only; no source, finance or estimator adoption"
        ),
        "frozen_inputs": frozen,
        "external_runtime_inputs": runtime,
        "external_runtime_bytes": runtime_bytes,
        "failure": {
            "total": rational(ALPHA),
            "CS": rational(CS_ALPHA),
            "fallback": rational(FALLBACK_ALPHA),
        },
        "precision": rational(PRECISION),
        "cap": N_CAP,
        "looks": list(LOOKS),
        "laws": [rational(Fraction(1, 1 << b)) for b in LAW_BITS],
        "seeds": list(SEEDS),
        "predictor": "constant zero, chosen before all observations",
        "runtime_layout": {
            "isolated": True,
            "no_site": True,
            "bytecode_writes": False,
            "sys_path": [
                str(BASE / "python312.zip"),
                str(BASE / "DLLs"),
                str(BASE / "Lib"),
                str(BASE),
            ],
            "base_prefix": str(BASE),
            "prefix": str(BASE),
            "python312_zip_expected_absent": True,
            "unused_site_packages_captured": False,
            "Windows_system_DLL_hashes_captured": False,
            "absent_loaded_cache_paths": sorted((str(path) for path in _ABSENT_CACHES)),
        },
        "lambda_values": [rational(x) for x in LAMBDAS],
        "log_majorants": {"CS": CS_LOG_MAJORANT, "fixed_N": FIXED_LOG_MAJORANT},
        "scope": {
            "program_fixture_credit": 0,
            "financial_replays": 0,
            "G2_transfer": False,
            "G3_price_delivery": False,
            "classical_comparator": False,
            "finance_execution": False,
            "quantum_gate_emissions": 0,
        },
        "budgets": {
            "CPU": CPU_LIMIT,
            "admission_CPU": WORK_LIMIT,
            "wall": WALL_LIMIT,
            "owned_files": MAX_OWNED_FILES,
            "owned_bytes": MAX_OWNED_BYTES,
            "runtime_files": MAX_RUNTIME_FILES,
            "runtime_bytes": MAX_RUNTIME_BYTES,
        },
    }


def prepare(args, started):
    global _ATTEMPT_ROUTE_OWNED
    invocation_check(started)
    require(not OUTPUT.exists(), "Never reuse a receipt route")
    frozen = root_release(args.root_ready_sha256, started)
    runtime, runtime_bytes = runtime_packet(started)
    require(
        str(LAUNCHER) in runtime and str(BASE / "python.exe") in runtime,
        "Both interpreters in runtime packet",
    )
    loaded_runtime_check(runtime, started)
    guard(started, admission=True)
    OUTPUT.mkdir(parents=False, exist_ok=False)
    _ATTEMPT_ROUTE_OWNED = True
    write_json(OUTPUT / "protocol.json", protocol_value(frozen, runtime, runtime_bytes), started)
    protocol_sha256 = hashlib.sha256(stable_read(OUTPUT / "protocol.json", started)).hexdigest()
    terminal = rehash(frozen, runtime, started, protocol_sha256)
    guard(started)
    print(
        json.dumps(
            {
                "prepare_passed": True,
                "scientific_evaluation": False,
                "protocol": relative(OUTPUT / "protocol.json"),
                "protocol_sha256": protocol_sha256,
                "prepare_terminal_full_verification": terminal,
                "frozen_inputs": len(frozen),
                "runtime_inputs": len(runtime),
                "observed_CPU": time.process_time(),
                "observed_wall": time.monotonic() - started,
            }
        ),
        flush=True,
    )


def seal(protocol, frozen, runtime, started, passed, error, before, after, protocol_expected):
    observed = guard(started)
    require(
        passed is True and error is None and (after is not None),
        "Only one successful complete terminal may be sealed",
    )
    require(
        {path.name for path in OUTPUT.iterdir()}
        == {
            "protocol.json",
            "run_started.json",
            "checks.json",
            "traces.json",
            "summary.json",
            "verification.json",
        },
        "Exact complete success artifacts; no failure marker, prior manifest or extra member",
    )
    owned, byte_count = ({}, 0)
    for path in sorted(OUTPUT.iterdir(), key=str):
        require(path.is_file() and path.name != "manifest.json", "Finite declared output set")
        data = stable_read(path, started)
        byte_count += len(data)
        owned[relative(path)] = hashlib.sha256(data).hexdigest()
    require(
        owned[relative(OUTPUT / "protocol.json")] == protocol_expected,
        "Original expected prepared protocol retained at terminal sealing",
    )
    manifest = {
        "schema": "e12-anytime-moment-manifest-v1",
        "passed": passed,
        "completed": passed,
        "budget_censored": bool(error and "budget" in error.lower()),
        "error": error,
        "owned_files": owned,
        "frozen_inputs": frozen,
        "external_runtime_inputs": runtime,
        "fresh_before": before,
        "fresh_after": after,
        "observed_CPU": observed[0],
        "observed_wall": observed[1],
        "scope": protocol["scope"],
        "financial_adoption_approved": False,
        "manifest_self_hash_excluded": True,
        "manifest_inclusive_owned_file_count": len(owned) + 1,
        "owned_nonmanifest_bytes": byte_count,
        "manifest_inclusive_retention_checked_before_sealing": True,
        "prepared_protocol_SHA256": owned[relative(OUTPUT / "protocol.json")],
    }
    size = 1
    for fragment in json.JSONEncoder(indent=2, sort_keys=True, allow_nan=False).iterencode(
        manifest
    ):
        guard(started)
        size += len(fragment.encode("utf-8"))
    require(
        len(owned) + 1 <= MAX_OWNED_FILES and byte_count + size <= MAX_OWNED_BYTES,
        "Manifest-inclusive owned file and byte caps",
    )
    write_json(OUTPUT / "manifest.json", manifest, started)
    actual = list(OUTPUT.iterdir())
    require(
        {relative(path) for path in actual} == set(owned) | {relative(OUTPUT / "manifest.json")}
        and len(actual) == len(owned) + 1 <= MAX_OWNED_FILES,
        "Exact complete final owned membership including manifest",
    )
    actual_bytes = 0
    for path in actual:
        guard(started)
        require(
            path.is_file() and path.resolve(strict=True) == path, "Final owned path confinement"
        )
        actual_bytes += path.stat().st_size
    require(
        (OUTPUT / "manifest.json").stat().st_size == size
        and actual_bytes == byte_count + size <= MAX_OWNED_BYTES,
        "Exact complete final owned bytes including manifest",
    )
    guard(started)


def run(args, started):
    global _ATTEMPT_ROUTE_OWNED
    require(
        OUTPUT.is_dir() and set((p.name for p in OUTPUT.iterdir())) == {"protocol.json"},
        "Fresh prepared route only",
    )
    _ATTEMPT_ROUTE_OWNED = True
    invocation_check(started)
    protocol_bytes = checked_read(OUTPUT / "protocol.json", args.protocol_sha256, started)
    protocol = json.loads(protocol_bytes)
    frozen = root_release(args.root_ready_sha256, started)
    require(
        protocol.get("schema") == "e12-anytime-moment-protocol-v1", "Frozen prospective protocol"
    )
    require(protocol.get("frozen_inputs") == frozen, "Protocol contains exact ROOT-frozen source")
    runtime = protocol["external_runtime_inputs"]
    fresh_runtime, runtime_bytes = runtime_packet(started)
    require(
        fresh_runtime == runtime and runtime_bytes == protocol["external_runtime_bytes"],
        "Exact complete runtime inventory unchanged",
    )
    loaded_runtime_check(runtime, started)
    require(
        protocol == protocol_value(frozen, runtime, protocol["external_runtime_bytes"]),
        "All fixed method fields and absent loaded cache states unchanged",
    )
    before = rehash(frozen, runtime, started, args.protocol_sha256)
    guard(started, admission=True)
    write_json(
        OUTPUT / "run_started.json",
        {
            "PID": os.getpid(),
            "protocol_expected_SHA256": args.protocol_sha256,
            "root_ready_expected_SHA256": args.root_ready_sha256,
            "observed_CPU": time.process_time(),
            "observed_wall": time.monotonic() - started,
            "scientific_checks_or_traces_started": False,
            "scope": protocol["scope"],
        },
        started,
    )
    after = None
    checks = structural_checks(started)
    traces = []
    compute_start = time.process_time()
    for bits in LAW_BITS:
        for seed in SEEDS:
            guard(started, admission=True)
            traces.append(diagnostic_trace(bits, seed, started))
    diagnostic_cpu = time.process_time() - compute_start
    require(len(traces) == 48, "All 48 fixed diagnostic traces completed")
    write_json(
        OUTPUT / "checks.json",
        {
            "passed": True,
            "checks": checks,
            "proof_basis": "Howard Theorem 4 and Lemma 1; finite union, rational majorants",
            "simulation_is_coverage_proof": False,
        },
        started,
    )
    write_json(OUTPUT / "traces.json", traces, started)
    rows = []
    for bits in LAW_BITS:
        selected = [r for r in traces if r["bits"] == bits]
        rows.append(
            {
                "law": rational(Fraction(1, 1 << bits)),
                "traces": len(selected),
                "CS_deliveries": sum((r["selected_branch"] == "anytime-CS" for r in selected)),
                "fallback_deliveries": sum(
                    (r["selected_branch"] == "fixed-N-fallback" for r in selected)
                ),
                "selected_samples": [r["selected_samples"] for r in selected],
                "baseline_samples_per_trace": N_CAP,
                "empirical_truth_in_interval": sum(
                    (r["diagnostic_truth_in_interval"] for r in selected)
                ),
                "empirical_coverage_is_not_a_certificate": True,
            }
        )
    write_json(
        OUTPUT / "summary.json",
        {
            "schema": "e12-anytime-moment-summary-v1",
            "passed": True,
            "bounded_toy_controller_complete": True,
            "rows": rows,
            "diagnostic_CPU": diagnostic_cpu,
            "decision": "Conditional toy component; finance and full estimator latency remain open",
            "scope": protocol["scope"],
            "missing_finance_premises": [
                "IID outer-group residual-squared source with a proved same-law support",
                "matching digital residual policy and finite arithmetic certificate",
                "charged acquisition-plus-estimation schedule at complete price confidence",
            ],
        },
        started,
    )
    after = rehash(frozen, runtime, started, args.protocol_sha256)
    write_json(
        OUTPUT / "verification.json",
        {
            "passed": True,
            "before": before,
            "after": after,
            "expected_hash_waivers": 0,
            "fixture_credit": 0,
            "finance_execution": False,
        },
        started,
    )
    seal(protocol, frozen, runtime, started, True, None, before, after, args.protocol_sha256)
    print(
        json.dumps(
            {
                "passed": True,
                "bounded_toy_controller_complete": True,
                "manifest": relative(OUTPUT / "manifest.json"),
                "rows": rows,
                "financial_adoption_approved": False,
                "fixture_credit": 0,
                "observed_CPU": time.process_time(),
                "observed_wall": time.monotonic() - started,
            }
        ),
        flush=True,
    )


def preserve_failure(error, started):
    """Every owned incomplete attempt is authoritative; no failed packet is resealed."""
    if not _ATTEMPT_ROUTE_OWNED or not OUTPUT.is_dir():
        return
    try:
        guard(started)
        if not (OUTPUT / "failure.json").exists():
            write_json(
                OUTPUT / "failure.json",
                {
                    "failed": True,
                    "passed": False,
                    "completed": False,
                    "error_type": type(error).__name__,
                    "error": str(error),
                    "observed_CPU": time.process_time(),
                    "observed_wall": time.monotonic() - started,
                    "no_partial_scientific_approval": True,
                    "original_expected_hashes_waived": False,
                    "fixture_credit": 0,
                    "finance_execution": False,
                },
                started,
            )
    except BaseException:
        pass
    try:
        require(OUTPUT.resolve(strict=True) == OUTPUT, "Confined failed attempt route")
        with (OUTPUT / "FAILED_UNSEALED.json").open("xb") as stream:
            stream.write(
                b'{"failed":true,"passed":false,"completed":false,"budget_censored":null,"hard_budget_state_uncertified":true,"partial_success_invalid":true,"fixture_credit":0,"finance_execution":false}\n'
            )
    except (OSError, ValueError):
        pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run"))
    parser.add_argument("--root-ready-sha256", required=True)
    parser.add_argument("--protocol-sha256")
    args = parser.parse_args()
    started = started_clock()
    require(
        args.mode == "prepare" or args.protocol_sha256 is not None,
        "ROOT must separately freeze prepared protocol",
    )
    try:
        if args.mode == "prepare":
            require(args.protocol_sha256 is None, "Prepare does not admit a pre-existing protocol")
            prepare(args, started)
        else:
            run(args, started)
    except BaseException as error:
        preserve_failure(error, started)
        raise


if __name__ == "__main__":
    main()
