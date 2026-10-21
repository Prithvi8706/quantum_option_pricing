"""Prospective fixed F44 Stage K controller; root freeze required before work.

No cosine/financial claim. One52x38/F44/mod116 multiplier and one full72
signed ties-even rounder, exactly88 diagnostics plus array-matched structure.
"""

import argparse
import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
import hashlib
from importlib.util import spec_from_file_location, module_from_spec, cache_from_source
import json
import os
from pathlib import Path
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[4]
RESEARCH = Path(__file__).resolve().parent
ORIGINAL_RESEARCH = ROOT / "research/limitation_program_20261001"
PROGRAM = ROOT / "results/limitation_program_20261001"
AUTHOR = RESEARCH / "experiment_taylor_f44_stage_k.py"
BUILDER = RESEARCH / "taylor_f44_stage_k_source.py"
PREFLIGHT = RESEARCH / "a14_taylor_f44_stage_k_implementation_preflight.json"
METHOD_DOC = RESEARCH / "A14_TAYLOR_F44_STAGE_K_IMPLEMENTATION_PREFLIGHT.md"
PROSPECTUS = ORIGINAL_RESEARCH / "a14_taylor_f44_prospectus_v1.json"
PROSPECTUS_DOC = ORIGINAL_RESEARCH / "A14_TAYLOR_F44_PROSPECTUS_V1.md"
OUTPUT = PROGRAM / "A14_continuation_20261004_stage_k_producer_run001"
READY = RESEARCH / "PRODUCER_ROOT_READY_run001.json"
BUILDER_MODULE = "research.limitation_program_20261001.continuation_20261004.A14.taylor_f44_stage_k_source"
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
W, F, ABITS, BBITS, PRODUCT_BITS = 72, 44, 52, 38, 116
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
            and name not in {__name__, "research.limitation_program_20261001",
                                "research.limitation_program_20261001.continuation_20261004",
                                "research.limitation_program_20261001.continuation_20261004.A14", BUILDER_MODULE}
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


class StructuralReader:
    """Consume actual rows against an independent recurrence/allocator trace."""

    def __init__(self, circuit, ports):
        self.circuit = circuit
        self.row = 0
        self.wire = ports

    def register(self, size, declared=None):
        budget()
        result = list(range(self.wire, self.wire + size))
        self.wire += size
        if declared is not None:
            require(
                type(declared) is list
                and all(type(v) is int for v in declared)
                and declared == result,
                "Every declared register is a fresh dense allocation",
            )
        return result

    def gate(self, *wires):
        budget()
        require(self.row < self.circuit.rows, "Actual row exists")
        expected = (len(wires), *wires, *([0] * (3 - len(wires))))
        require(
            tuple(self.circuit.gates[4 * self.row : 4 * self.row + 4]) == expected,
            "Every actual native row matches recurrence",
        )
        self.row += 1

    def finish(self, descriptor, output_sources, outputs):
        compute_end = self.row
        require(descriptor["compute_gate_rows"] == [0, compute_end], "Complete compute boundary")
        for source, target in zip(output_sources, outputs, strict=True):
            self.gate(source, target)
        require(descriptor["copy_gate_rows"] == [compute_end, self.row], "Exactly72 output XORs")
        reverse_start = self.row
        for original in range(compute_end - 1, -1, -1):
            budget()
            require(
                tuple(self.circuit.gates[4 * self.row : 4 * self.row + 4])
                == tuple(self.circuit.gates[4 * original : 4 * original + 4]),
                "Literal complete reverse, no dropped row",
            )
            self.row += 1
        require(
            self.row == self.circuit.rows == descriptor["gate_rows"]
            and self.wire == self.circuit.qubits == descriptor["qubits"]
            and descriptor["inverse_gate_rows"] == [reverse_start, self.row],
            "Every actual row and allocated wire accounted",
        )


def structural_multiplier(circuit, descriptor):
    require(
        descriptor["schema"] == "a14-f44-stage-k-clean-arithmetic-leaf-v1"
        and descriptor["op"] == "mul"
        and descriptor["params"] == {}
        and descriptor["dirty_output_XOR"] is True
        and descriptor["input_preserved"] is True
        and descriptor["private_workspace_zero_entry_exit"] is True,
        "Exact multiplier descriptor claims",
    )
    require(
        descriptor["spec"]
        == {
            "width": 72,
            "fraction_bits": 44,
            "product_width": 116,
            "active_operand_bits": [52, 38],
            "input_contract": {"signed_operand_bits": [52, 38]},
            "variant": "retained-CSA-explicit-ripple-final-v1",
        },
        "Only fixed new multiplier contract",
    )
    a, b, out = [list(range(offset, offset + W)) for offset in (0, W, 2 * W)]
    require(
        descriptor["args"] == [a, b] and descriptor["outs"] == [out],
        "Actual full72 input/output ports",
    )
    reader, recipe = StructuralReader(circuit, 3 * W), descriptor["recipe"]
    columns = [[] for _ in range(PRODUCT_BITS)]
    correction, index = 0, 0
    for i in range(BBITS):
        for j in range(ABITS):
            budget()
            negative = (i == BBITS - 1) != (j == ABITS - 1)
            wire = reader.register(1)[0]
            require(
                recipe["partials"][index]
                == dict(a_bit=j, b_bit=i, column=i + j, negative=negative, wire=wire),
                "Complete signed partial-plane evidence",
            )
            index += 1
            if negative:
                reader.gate(wire)
                correction -= 1 << (i + j)
            reader.gate(a[j], b[i], wire)
            columns[i + j].append(wire)
    require(index == len(recipe["partials"]) == ABITS * BBITS, "No missing/extra partial product")
    correction %= 1 << PRODUCT_BITS
    require(recipe["correction"] == correction, "Full116 modular negative correction")
    require(
        correction == (-((1 << 89) - (1 << 51) - (1 << 37))) % (1 << 116),
        "Independent closed correction identity",
    )
    fixed = []
    for column in range(PRODUCT_BITS):
        if (correction >> column) & 1:
            wire = reader.register(1)[0]
            reader.gate(wire)
            columns[column].append(wire)
            fixed.append(dict(column=column, wire=wire))
    require(recipe["fixed"] == fixed, "Every full-modulus constant column paid")
    layers = []
    while max(len(column) for column in columns) > 2:
        following = [[] for _ in columns]
        steps = []
        for column, values in enumerate(columns):
            consumed = 0
            for offset in range(0, len(values) - 2, 3):
                x, y, z = values[offset : offset + 3]
                summed = reader.register(1)[0]
                reader.gate(x, summed)
                reader.gate(y, summed)
                carry = None
                if column + 1 < PRODUCT_BITS:
                    carry = reader.register(1)[0]
                    reader.gate(x, y, carry)
                    reader.gate(summed, z, carry)
                    following[column + 1].append(carry)
                reader.gate(z, summed)
                following[column].append(summed)
                steps.append(dict(column=column, inputs=[x, y, z], sum=summed, carry=carry))
                consumed = offset + 3
            following[column].extend(values[consumed:])
        layers.append(steps)
        columns = following
    require(
        recipe["CSA_layers"] == layers and recipe["final_columns"] == columns,
        "Complete modular CSA chronology",
    )
    left = reader.register(PRODUCT_BITS, recipe["left"])
    right = reader.register(PRODUCT_BITS, recipe["right"])
    product = reader.register(PRODUCT_BITS, recipe["product"])
    for column, values in enumerate(columns):
        if values:
            reader.gate(values[0], left[column])
        if len(values) == 2:
            reader.gate(values[1], right[column])
    propagate = reader.register(PRODUCT_BITS, recipe["propagate"])
    carry = reader.register(PRODUCT_BITS + 1, recipe["carry"])
    for bit in range(PRODUCT_BITS):
        reader.gate(left[bit], propagate[bit])
        reader.gate(right[bit], propagate[bit])
        reader.gate(left[bit], right[bit], carry[bit + 1])
        if bit:
            reader.gate(propagate[bit], carry[bit], carry[bit + 1])
        reader.gate(propagate[bit], product[bit])
        if bit:
            reader.gate(carry[bit], product[bit])
    require(recipe["output_source_bits"] == list(range(F, F + W)), "Exact window44..115")
    reader.finish(descriptor, product[F : F + W], out)
    return dict(
        array_matched=True,
        all_input_contract_words=True,
        signed90_minimum_times_minimum_preserved=True,
        all_low44_carries_retained=True,
        full_modulus116_correction_and_output_window=True,
        proof=[
            "Signed weights multiply; exactly-one-sign terms are negative.",
            "-t*2^k=(1-t)*2^k-2^k, correction modulo2^116 includes all negative weights.",
            "CSA s=x XOR y XOR z and c=xy XOR((x XOR y)z) satisfy x+y+z=s+2c.",
            "Ripple carry=xy XOR((x XOR y)c); its two terms are disjoint.",
            "All columns0..115 remain before extracting bits44..115.",
            "Both minima yield positive 2^88, requiring 90 signed bits; "
            "the modulus 116 image preserves it.",
            "floor((xy+k*2^116)/2^44)=floor(xy/2^44)+k*2^72.",
            "Compute does not read dirty output; 72 CX then literal reverse "
            "implements clean XOR for all contract inputs.",
        ],
    )


def structural_rounder(circuit, descriptor):
    require(
        descriptor["schema"] == "a14-f44-stage-k-clean-arithmetic-leaf-v1"
        and descriptor["op"] == "round_ties_even"
        and descriptor["params"] == {"discarded_fractional_bits": 4}
        and descriptor["dirty_output_XOR"] is True
        and descriptor["input_preserved"] is True
        and descriptor["private_workspace_zero_entry_exit"] is True,
        "Exact rounder descriptor claims",
    )
    z, out = list(range(W)), list(range(W, 2 * W))
    require(descriptor["args"] == [z] and descriptor["outs"] == [out], "Full72 rounder ports")
    require(
        descriptor["spec"]
        == dict(
            width=72,
            input_fraction_bits=44,
            output_fraction_bits=40,
            input_contract={},
            variant="retained-signed-quotient-parity-ripple-increment-v1",
        ),
        "Fixed universal rounder format",
    )
    reader, recipe = StructuralReader(circuit, 2 * W), descriptor["recipe"]
    q = reader.register(W, recipe["quotient"])
    r = reader.register(4, recipe["remainder"])
    ors = reader.register(3, recipe["OR_history"])
    inc = reader.register(1)[0]
    require(recipe["increment"] == inc, "Explicit increment wire")
    carry = reader.register(W + 1, recipe["carry"])
    result = reader.register(W, recipe["result"])
    sources = [z[min(j + 4, W - 1)] for j in range(W)]
    require(recipe["quotient_source_wires"] == sources, "Arithmetic signed quotient sign extension")
    for a, b in zip(sources, q, strict=True):
        reader.gate(a, b)
    for a, b in zip(z[:4], r, strict=True):
        reader.gate(a, b)
    for a, b, c in ((r[0], r[1], ors[0]), (ors[0], r[2], ors[1]), (ors[1], q[0], ors[2])):
        reader.gate(a, c)
        reader.gate(b, c)
        reader.gate(a, b, c)
    reader.gate(r[3], ors[2], inc)
    require(
        descriptor["predicate_compute_gate_rows"] == [0, reader.row], "Exact emitted Boolean prefix"
    )
    reader.gate(inc, carry[0])
    for bit in range(W):
        reader.gate(q[bit], result[bit])
        reader.gate(carry[bit], result[bit])
        reader.gate(q[bit], carry[bit], carry[bit + 1])
    reader.finish(descriptor, result, out)
    return dict(
        array_matched=True,
        all_full72_input_words=True,
        negative_floor_quotient_and_remainder=True,
        exact_ties_even=True,
        proof=[
            "Arithmetic shift yields q=floor(z/16) and remainder r in0..15 for signed z.",
            "OR target computes a XOR b XOR ab with a clean target.",
            "Increment=r3 AND(r0 OR r1 OR r2 OR q0) equals r>8 OR(r=8 AND q odd).",
            "Increment carry c_next=q_bit*c and sum=q_bit XOR c gives q+increment modulo2^72.",
            "Signed full72 z yields |q|<=2^67; adding at most1 cannot overflow signed72.",
            "Compute/output72XOR/literal reverse preserves input and zero private workspace.",
        ],
    )


def corpus():
    xlo, xhi = -(1 << 51), (1 << 51) - 1
    ylo, yhi = -(1 << 37), (1 << 37) - 1
    pairs = ((0, 0), (0, 1), (1, 0), (-1, 1), (xlo, ylo), (xhi, yhi), (xlo, yhi), (xhi, ylo))
    dirties = (0, (1 << W) - 1)
    return {
        "multiplier": [(a, b, d) for a, b in pairs for d in dirties],
        "rounder": [
            (16 * q + r, d) for q in (-2, -1, 0, 1) for r in (0, 7, 8, 9, 15) for d in dirties
        ],
        "Boolean_prefix": [(r, p) for r in range(16) for p in (0, 1)],
    }


def fill_word(state, wires, value):
    for bit, wire in enumerate(wires):
        budget()
        state[wire] = (value >> bit) & 1


def complete_state_equal(actual, expected, message):
    require(len(actual) == len(expected), "Every allocated wire compared")
    for index in range(len(actual)):
        budget()
        require(actual[index] == expected[index], message + ":" + str(index))


def basis_cases(builder, circuit, descriptor, rows, op):
    reports = []
    for number, case in enumerate(rows):
        budget(admission=True)
        if op == "mul":
            left, right, dirty = case
            require(
                -(1 << 51) <= left < (1 << 51) and -(1 << 37) <= right < (1 << 37),
                "Actual promised native inputs",
            )
            values = [left & ((1 << W) - 1), right & ((1 << W) - 1)]
            reference = ((left * right) // (1 << F)) & ((1 << W) - 1)
        else:
            z, dirty = case
            q, r = divmod(z, 16)
            reference = (q + int(r > 8 or (r == 8 and q % 2 == 1))) & ((1 << W) - 1)
            values = [z & ((1 << W) - 1)]
        initial = bytearray(circuit.qubits)
        for wires, value in zip(descriptor["args"], values, strict=True):
            fill_word(initial, wires, value)
        fill_word(initial, descriptor["outs"][0], dirty)
        expected = bytearray(initial)
        fill_word(expected, descriptor["outs"][0], dirty ^ reference)
        forward = None
        for inverse in (False, True):
            state = builder.run_rows(circuit, bytearray(initial), budget, inverse=inverse)
            complete_state_equal(state, expected, "Full input/dirty-output/private state")
            if not inverse:
                forward = bytearray(state)
        restored = builder.run_rows(circuit, forward, budget, inverse=True)
        complete_state_equal(restored, initial, "Literal inverse full restoration")
        reports.append(
            dict(
                case_index=number,
                inputs_signed=list(case[:-1]),
                dirty_output=dirty,
                reference_raw=reference,
                forward_passed=True,
                independent_inverse_direction_passed=True,
                forward_then_literal_reverse_passed=True,
                all_allocated_wires_compared=circuit.qubits,
            )
        )
    return reports


def boolean_cases(builder, circuit, descriptor, rows):
    reports = []
    recipe = descriptor["recipe"]
    begin, end = descriptor["predicate_compute_gate_rows"]
    for number, (r, parity) in enumerate(rows):
        budget(admission=True)
        z = 16 * parity + r
        initial = bytearray(circuit.qubits)
        fill_word(initial, descriptor["args"][0], z)
        expected = bytearray(initial)
        fill_word(expected, recipe["quotient"], parity)
        fill_word(expected, recipe["remainder"], r)
        bits = [(r >> j) & 1 for j in range(4)]
        histories = [
            bits[0] | bits[1],
            bits[0] | bits[1] | bits[2],
            bits[0] | bits[1] | bits[2] | parity,
        ]
        for wire, value in zip(recipe["OR_history"], histories, strict=True):
            expected[wire] = value
        reference = int(r > 8 or (r == 8 and parity == 1))
        expected[recipe["increment"]] = reference
        actual = builder.run_rows(circuit, bytearray(initial), budget, begin=begin, end=end)
        complete_state_equal(actual, expected, "Every Boolean-prefix allocated wire")
        restored = builder.run_rows(circuit, actual, budget, inverse=True, begin=begin, end=end)
        complete_state_equal(restored, initial, "Boolean-prefix literal inverse")
        reports.append(
            dict(
                case_index=number,
                remainder=r,
                quotient_parity=parity,
                increment=reference,
                actual_emitted_prefix_replayed=True,
                full_prefix_wire_state_passed=True,
                literal_reverse_passed=True,
                all_allocated_wires_compared=circuit.qubits,
            )
        )
    return reports


def emit_array(circuit, name):
    require(
        sys.byteorder == "little" and len(circuit.gates) == 4 * circuit.rows,
        "Little-endian int32 Nx4 ABI",
    )
    path = OUTPUT / name
    with path.open("xb") as stream:
        for offset in range(0, len(circuit.gates), 16384):
            budget()
            stream.write(circuit.gates[offset : offset + 16384].tobytes())
            budget()
    require(path.stat().st_size == 16 * circuit.rows, "Exact complete raw native row bytes")
    return dict(
        gate_file=name,
        gate_SHA256=digest(path, fresh=True),
        storage="little-endian signedint32 raw Nx4, no header",
        rows=circuit.rows,
        bytes=path.stat().st_size,
    )


def flags():
    return dict(
        new_test_credit=0,
        new_credited_gate_replays=0,
        new_price_samples=0,
        Stage_K_diagnostics_not_cosine_or_financial_certificate=True,
        Stage_C_release_authorized=False,
        full_G2=False,
        adoption=False,
        cost_transfer=False,
        quantum_advantage=False,
        independent_scientific_audit_still_required=True,
        previous_A14_rejected_rows_unchanged=True,
    )


def admission(expected_ready):
    ready = read(bind(READY, expected_ready))
    require(
        ready["schema"] == "root-a14-taylor-f44-stage-k-READY-v1"
        and ready["ready"] is True
        and ready["root_and_independent_static_reviews_passed"] is True,
        "External ROOT-reviewed prospective fixed release",
    )
    require(
        ready["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
        and ready["output"] == OUTPUT.relative_to(ROOT).as_posix()
        and ready["argv_prefix"]
        == [
            "-B",
            "-m",
            "research.limitation_program_20261001.continuation_20261004.A14.experiment_taylor_f44_stage_k",
            "--ready-sha256",
        ],
        "Exact fresh CLI/routes/clocks",
    )
    paths = (AUTHOR, BUILDER, PREFLIGHT, METHOD_DOC)
    pins = ready["author_method_SHA256"]
    require(
        type(pins) is dict and set(pins) == {path.name for path in paths},
        "Exactly four NEW frozen files",
    )
    for path in paths:
        bind(path, pins[path.name])
    policy = read(PREFLIGHT)
    require(
        policy["schema"] == "a14-taylor-f44-stage-k-implementation-preflight-v1"
        and policy["author_SHA256"]
        == {AUTHOR.name: pins[AUTHOR.name], BUILDER.name: pins[BUILDER.name]}
        and policy["method_document_SHA256"] == pins[METHOD_DOC.name]
        and policy["limits_CPU_admission_wall"] == [CPU, ADMISSION, WALL]
        and policy["owned_caps_files_bytes"] == [MAX_OWN_FILES, MAX_OWN_BYTES]
        and policy["native_gate_rows_maximum_across_two_primitives"] == MAX_NATIVE_ROWS
        and policy["fixed_diagnostic_counts"] == [16, 40, 32, 88],
        "Exact fixed reviewed Stage K policy",
    )
    require(
        policy["original_prospectus_SHA256"]
        == {PROSPECTUS.name: PROSPECTUS_SHA, PROSPECTUS_DOC.name: PROSPECTUS_DOC_SHA},
        "Immutable reviewed F44 paper pins",
    )
    bind(PROSPECTUS, PROSPECTUS_SHA)
    bind(PROSPECTUS_DOC, PROSPECTUS_DOC_SHA)
    method = read(PROSPECTUS)
    require(
        method["new_multiplier"]["active_operand_bits"] == [52, 38]
        and method["new_multiplier"]["retained_product_width"] == 116
        and method["stage_K"]["fixed_diagnostic_cases"] == 88,
        "Same single paper contract",
    )
    expected_packets = {name: pin for name, (pin, _) in EXISTING_PACKETS.items()}
    require(
        policy["required_existing_packet_manifest_SHA256"] == expected_packets
        and ready["required_existing_packet_manifest_SHA256"] == expected_packets,
        "Original A14 complete evidence pins",
    )
    for name, (pin, counts) in EXISTING_PACKETS.items():
        packet(name, pin, counts)
    cache_pins = ready["existing_new_code_cache_SHA256"]
    caches = {
        key_for(Path(cache_from_source(str(path)))): Path(cache_from_source(str(path)))
        for path in (AUTHOR, BUILDER)
        if Path(cache_from_source(str(path))).exists()
    }
    require(
        type(cache_pins) is dict and set(cache_pins) == set(caches),
        "Actual existing new-code caches explicitly pinned",
    )
    for key, path in caches.items():
        bind(path, cache_pins[key])
    runtime = own_runtime()
    return ready, policy, runtime


def load_builder(expected):
    budget(admission=True)
    require(BUILDER_MODULE not in sys.modules, "No prior builder import")
    loaded_origins()
    require(digest(BUILDER, fresh=True) == expected, "Exact frozen new builder before lazy import")
    spec = spec_from_file_location(BUILDER_MODULE, BUILDER)
    require(spec is not None and spec.loader is not None, "Exact declared loader")
    module = module_from_spec(spec)
    sys.modules[BUILDER_MODULE] = module
    spec.loader.exec_module(module)
    loaded_origins()
    require(
        (module.W, module.F, module.LEFT_BITS, module.RIGHT_BITS, module.PRODUCT_BITS)
        == (72, 44, 52, 38, 116),
        "Unchanged literal builder interface",
    )
    return module


def retain_failure(error):
    if not OUTPUT.is_dir():
        return
    try:
        budget()
        require(
            not (OUTPUT / "manifest.json").exists()
            and not (OUTPUT / "completion_outcome.json").exists(),
            "Partial terminal never resealed",
        )
        save(
            "failure.json",
            dict(
                failed=True,
                passed=False,
                error_type=type(error).__name__,
                error=str(error),
                traceback=traceback.format_exc(),
                budget=dict(
                    process_CPU_seconds=time.process_time(),
                    wall_seconds=time.monotonic() - _STARTED,
                ),
                **flags(),
            ),
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
    args = parser.parse_args()
    require(canonical(__file__) == AUTHOR and not OUTPUT.exists(), "Fresh fixed Stage K, no retry")
    try:
        ready, policy, runtime = admission(args.ready_sha256)
        first = fresh_union()
        budget(admission=True)
        OUTPUT.mkdir(exist_ok=False)
        for path in (AUTHOR, BUILDER, PREFLIGHT, METHOD_DOC, PROSPECTUS, PROSPECTUS_DOC, READY):
            copy(path, "executed_" + path.name)
        save(
            "run_started.json",
            dict(
                created_UTC=datetime.now(timezone.utc).isoformat(),
                PID=os.getpid(),
                ROOT_READY_SHA256=args.ready_sha256,
                limits_CPU_admission_wall=[CPU, ADMISSION, WALL],
                **flags(),
            ),
        )
        builder = load_builder(policy["author_SHA256"][BUILDER.name])
        fixed = corpus()
        require(builder.fixed_diagnostics() == fixed, "Exactly preregistered88 literal cases")
        multiplier, mul_desc = builder.build_multiplier(budget)
        rounder, round_desc = builder.build_rounder(budget)
        require(
            multiplier.rows + rounder.rows <= MAX_NATIVE_ROWS,
            "One million total rows across both primitives",
        )
        save("primitive_descriptors.json", dict(multiplier=mul_desc, rounder=round_desc))
        budget(admission=True)
        mul_proof = structural_multiplier(multiplier, mul_desc)
        round_proof = structural_rounder(rounder, round_desc)
        macro = (
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
        require(builder.CCX_PHASE_MACRO == macro, "Exact declared absolute7T chronology")
        save(
            "universal_structural_certificate.json",
            dict(
                multiplier=mul_proof,
                rounder=round_proof,
                phase_macro=[list(event) for event in macro],
                absolute_phase_proof=[
                    "a+b+c-(a XOR b)-(a XOR c)-(b XOR c)+(a XOR b XOR c)=4abc.",
                    "T/TD phase is exp(i*pi/4*integer parity polynomial), "
                    "hence exact CCZ without global offset.",
                    "Target H conjugation yields absolute CCX; "
                    "X and CX have exact real permutation matrices.",
                    "All native gates are self-inverse; complete literal reverse "
                    "implements F inverse on arbitrary superpositions.",
                ],
                finite_basis_diagnostics_are_not_the_universal_proof=True,
                **flags(),
            ),
        )
        native_arrays = {
            "multiplier": emit_array(multiplier, "multiplier.gates.bin"),
            "rounder": emit_array(rounder, "rounder.gates.bin"),
        }
        save("native_gate_arrays.json", native_arrays)
        save(
            "primitive_resources.json",
            dict(
                multiplier=builder.gate_resources(multiplier, budget),
                rounder=builder.gate_resources(rounder, budget),
                no_prior_resource_transfer=True,
                full_cosine_or_financial_cost_claim=False,
            ),
        )
        diagnostics = {
            "multiplier": basis_cases(builder, multiplier, mul_desc, fixed["multiplier"], "mul"),
            "rounder": basis_cases(builder, rounder, round_desc, fixed["rounder"], "rounder"),
            "Boolean_prefix": boolean_cases(builder, rounder, round_desc, fixed["Boolean_prefix"]),
        }
        require(
            [len(diagnostics[name]) for name in ("multiplier", "rounder", "Boolean_prefix")]
            == [16, 40, 32],
            "All88 fixed diagnostics retained",
        )
        save("fixed_diagnostics.json", dict(cases=diagnostics, fixed_total=88, **flags()))
        loaded_origins()
        second = fresh_union()
        require(
            not any(
                (OUTPUT / name).exists()
                for name in ("manifest.json", "completion_outcome.json", "FAILED_UNSEALED.json")
            ),
            "Exclusive terminal",
        )
        summary = dict(
            schema="a14-taylor-f44-stage-k-summary-v1",
            completed=True,
            passed=True,
            budget_censored=False,
            arithmetic_component_diagnostics_complete=True,
            actual_array_matched_universal_structure=True,
            absolute7T_phase_proof_bound=True,
            fixed_diagnostic_counts=[16, 40, 32, 88],
            native_rows_total=multiplier.rows + rounder.rows,
            actual_full_leaf_replay_calls=3 * (16 + 40),
            actual_Boolean_prefix_replay_calls=2 * 32,
            native_gate_arrays=native_arrays,
            current_runtime=runtime,
            both_full_uncached_input_unions=[first, second],
            limits_CPU_admission_wall=[CPU, ADMISSION, WALL],
            budget=dict(
                process_CPU_seconds=time.process_time(), wall_seconds=time.monotonic() - _STARTED
            ),
            **flags(),
        )
        save("summary.json", summary)
        save("completion_outcome.json", dict(summary, failed=False))
        owned, total = {}, 0
        for path in sorted(inventory(OUTPUT)):
            budget()
            total += path.stat().st_size
            require(
                len(owned) < MAX_OWN_FILES - 1 and total <= MAX_OWN_BYTES, "Full owned retention caps"
            )
            owned[path.relative_to(OUTPUT).as_posix()] = digest(path, fresh=True)
        save(
            "manifest.json",
            dict(
                schema="a14-taylor-f44-stage-k-manifest-v1",
                files=owned,
                frozen_inputs=_FROZEN,
                external_runtime_inputs=_EXTERNAL,
                manifest_self_hash_excluded=True,
                completed=True,
                passed=True,
                budget_censored=False,
                both_full_uncached_input_unions=[first, second],
                limits_CPU_admission_wall=[CPU, ADMISSION, WALL],
                terminal_budget_observation=dict(
                    process_CPU_seconds=time.process_time(),
                    wall_seconds=time.monotonic() - _STARTED,
                ),
                **flags(),
            ),
        )
        budget()
        print(
            json.dumps(
                dict(
                    passed=True,
                    manifest_SHA256=digest(OUTPUT / "manifest.json", fresh=True),
                    **flags(),
                )
            )
        )
    except BaseException as error:
        retain_failure(error)
        raise


if __name__ == "__main__":
    main()
