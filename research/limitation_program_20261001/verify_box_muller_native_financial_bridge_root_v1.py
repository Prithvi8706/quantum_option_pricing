"""Fresh local receipt integrity checks; no numerical kernel or fixture credit."""

import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
OUTPUT = PROGRAM / "A02_BM_native_financial_bridge_root_verification_run001"
CPU, ADMISSION, WALL = 120, 90, 600
EXPECTED_MANIFESTS = dict(
    zip(
        (
            "A02_BM_native_financial_bridge_run002",
            "A02_BM_native_financial_bridge_audit_run002",
            "A02_BM_native_financial_bridge_root_review_run002",
            "A02_polar_cdf_bv_root_verification_run002",
        ),
        (
            "78a8eea9dc937883b810cb6b3e2e26aec41297551b984a9c12bb15a435523162",
            "62074efc3bd5a20a9cbe72b3d020fd5c6bf13e32d41b188ef57570225dade2a0",
            "86b04e1720d94dc3cc7de61ff57e80dcc60769b8f4704f6e24da61a9d62a98f8",
            "d4ce20608e4de29f45cae794fe5e8b974db5996c655bfa5a4cfa131938a06391",
        ),
        strict=True,
    )
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def process_creation():
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
    stamps = [wintypes.FILETIME() for _ in range(4)]
    require(
        kernel.GetProcessTimes(
            kernel.GetCurrentProcess(), *[ctypes.byref(stamp) for stamp in stamps]
        ),
        "Actual process creation clock",
    )
    stamp = stamps[0]
    return ((stamp.dwHighDateTime << 32) | stamp.dwLowDateTime) / 10**7 - 11644473600


CREATION = process_creation()


def budget(admission=False):
    require(time.process_time() <= (ADMISSION if admission else CPU), "CPU guard")
    require(time.time() - CREATION <= WALL, "Wall guard")


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            budget()
            digest.update(chunk)
    return digest.hexdigest()


def main():
    require(not OUTPUT.exists(), "Fresh fixed root-verification receipt")
    frozen, external, packets = {}, {}, {}

    def add(path, expected):
        lexical = Path(path)
        if not lexical.is_absolute():
            lexical = ROOT / lexical
        actual = lexical.resolve(strict=True)
        require(actual.is_file(), "Actual regular input")
        require(actual == lexical.absolute(), "No input alias")
        if actual.is_relative_to(ROOT):
            key, mapping = actual.relative_to(ROOT).as_posix(), frozen
        else:
            base = Path(sys.base_prefix).resolve(strict=True)
            require(actual.is_relative_to(base), "Scoped actual external Python runtime")
            require(not actual.is_relative_to(base / "Lib/site-packages"), "No base packages")
            key, mapping = str(actual), external
        require(key not in mapping or mapping[key] == expected, "Conflicting expected SHA")
        mapping[key] = expected

    for name, expected in EXPECTED_MANIFESTS.items():
        directory = PROGRAM / name
        require(not (directory / "FAILED_UNSEALED.json").exists(), "Failed-unsealed packet")
        require(not (directory / "failure.json").exists(), "Failed packet")
        path = directory / "manifest.json"
        raw = path.read_bytes()
        require(hashlib.sha256(raw).hexdigest() == expected, "Pinned manifest")
        packet = json.loads(raw)
        require(packet.get("manifest_self_hash_excluded") is True, "Self-hash excluded")
        add(path, expected)
        counts = {}
        for group in ("files", "frozen_inputs", "external_runtime_inputs"):
            mapping = packet.get(group, {})
            counts[group] = len(mapping)
            for member, digest in mapping.items():
                budget()
                if group == "files":
                    owned = Path(member)
                    owned = (
                        ROOT / owned
                        if owned.parts[:2] == ("results", "limitation_program_20261001")
                        else directory / owned
                    )
                    require(
                        owned.resolve(strict=True).is_relative_to(directory),
                        "Confined owned receipt file",
                    )
                    add(owned, digest)
                else:
                    add(member, digest)
        packets[name] = counts

    for name in (
        "A02_BM_native_financial_bridge_run002",
        "A02_BM_native_financial_bridge_audit_run002",
    ):
        directory = PROGRAM / name
        summary = json.loads((directory / "summary.json").read_bytes())
        completion = json.loads((directory / "completion_outcome.json").read_bytes())
        require(
            summary["passed"] and completion["passed"] and completion["completed"],
            "Actual completed PASS",
        )
        require(
            summary["full_G2"] is False and summary["new_test_credit"] == 0,
            "Native financial certificate scope; zero new fixtures",
        )
    require(
        json.loads(
            (PROGRAM / "A02_BM_native_financial_bridge_audit_run002/summary.json").read_bytes()
        )["independent_audit_passed"],
        "Actual independent audit",
    )

    for name in (
        "A02_BM_native_financial_bridge_run002",
        "A02_BM_native_financial_bridge_audit_run002",
    ):
        summary = json.loads((PROGRAM / name / "summary.json").read_bytes())
        require(
            summary["native_financial_bias_certificate_valid"]
            and summary["financial_residual_fit"],
            "Actual native financial bound and residual PASS",
        )
        require(
            not summary["budget_censored"]
            and not summary["adoption"]
            and not summary["cost_transfer"],
            "Uncensored source-specific proof only",
        )

    source = Path(__file__).resolve(strict=True)
    add(source, sha(source))
    require(len(frozen) + len(external) <= 24000, "Finite verification inventory")
    total = 0
    for mapping in (frozen, external):
        for member, expected in mapping.items():
            path = Path(member) if Path(member).is_absolute() else ROOT / member
            total += path.stat().st_size
            require(total <= 2 * 1024**3, "Finite verification byte cap")
            require(sha(path) == expected, "Fresh actual input SHA mismatch: " + member)
    budget(admission=True)
    OUTPUT.mkdir()

    def write(name, value):
        with (OUTPUT / name).open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(value, stream, indent=2)
            stream.write("\n")

    try:
        copy = OUTPUT / source.name
        with copy.open("xb") as stream:
            stream.write(source.read_bytes())
        summary = {
            "schema": "root-original-BM-native-financial-bridge-fresh-integrity-v1",
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "local_only": True,
            "passed": True,
            "producer_and_independent_audit_terminal_PASS": True,
            "fresh_unique_input_paths": len(frozen) + len(external),
            "fresh_hashed_input_bytes": total,
            "SHA_mismatches": 0,
            "packet_map_counts": packets,
            "CPU_admission_wall_limits": [CPU, ADMISSION, WALL],
            "process_CPU_seconds": time.process_time(),
            "wall_seconds_from_actual_process_creation": time.time() - CREATION,
            "new_fixture_credit": 0,
            "scientific_kernels_executed": False,
            "full_G2": False,
            "native_financial_bias_certificate_valid": True,
            "G2_composition_ledger_still_required": True,
            "adoption": False,
            "quantum_advantage_claim": False,
        }
        write("summary.json", summary)
        files = {p.relative_to(ROOT).as_posix(): sha(p) for p in OUTPUT.iterdir() if p.is_file()}
        write(
            "manifest.json",
            {
                "files": files,
                "frozen_inputs": frozen,
                "external_runtime_inputs": external,
                "terminal_record": (OUTPUT / "summary.json").relative_to(ROOT).as_posix(),
                "manifest_self_hash_excluded": True,
                "new_fixture_credit": 0,
            },
        )
        budget()
        print(
            json.dumps(
                {
                    "passed": True,
                    "paths": len(frozen) + len(external),
                    "manifest_sha256": sha(OUTPUT / "manifest.json"),
                    "new_fixture_credit": 0,
                }
            )
        )
    except BaseException:
        write(
            "FAILED_UNSEALED.json",
            {
                "passed": False,
                "new_fixture_credit": 0,
                "partial_summary_or_manifest_is_not_success": True,
            },
        )
        raise


if __name__ == "__main__":
    main()
