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
OUTPUT = PROGRAM / "A02_polar_cdf_bv_root_verification_run002"
CPU, ADMISSION, WALL = 120, 90, 600
EXPECTED_MANIFESTS = dict(
    zip(
        (
            "A02_polar_cdf_bv_run003",
            "A02_polar_cdf_bv_audit_run003",
            "A02_polar_cdf_bv_root_review_run003",
            "A02_polar_cdf_bv_admission_observation_correction_run001",
        ),
        (
            "86dcd6b400233b58f62d4197127e38c6d2598c05e1903d207b0947168b326a05",
            "75ed7d7d6d5b929571d64d8fa54d53f6bf146c283d18133a5d191ac612724eb9",
            "296bb3a68d743dfe3c92a86839b1dfea30f57c67170c8ba37d8ca4197b8b5538",
            "6d133c5e3f848d7af17be1e796b65b1851a6f6c4d8cdb669c201520065125eea",
        ),
        strict=True,
    )
)
OLD_VERIFIER_SHA = "637dfa208c4f3ba1fa67480dc481ca773037e86337f09aa36feeb0c2f3072e6a"


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

    for name in ("A02_polar_cdf_bv_run003", "A02_polar_cdf_bv_audit_run003"):
        directory = PROGRAM / name
        summary = json.loads((directory / "summary.json").read_bytes())
        completion = json.loads((directory / "completion_outcome.json").read_bytes())
        require(
            summary["passed"] and completion["passed"] and completion["completed"],
            "Actual completed PASS",
        )
        require(
            summary["full_G2"] is False and summary["new_test_credit"] == 0,
            "Partial proof scope; zero new fixtures",
        )
    require(
        json.loads((PROGRAM / "A02_polar_cdf_bv_audit_run003/summary.json").read_bytes())[
            "independent_audit_passed"
        ],
        "Actual independent audit",
    )

    source = Path(__file__).resolve(strict=True)
    add(source, sha(source))
    previous = source.with_name("verify_box_muller_polar_cdf_bv_root_v1.py")
    add(previous, OLD_VERIFIER_SHA)
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
            "schema": "root-original-polar-cdf-bv-fresh-integrity-v1",
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
            "previous_root_verifier_exit_code": 1,
            "previous_root_verifier_failed_before_mkdir": True,
            "previous_intended_root_receipt_absent": not (
                PROGRAM / "A02_polar_cdf_bv_root_verification_run001"
            ).exists(),
            "previous_root_verifier_error": (
                "FileNotFoundError: receipt-relative angular_guards.json "
                "was incorrectly resolved against ROOT"
            ),
            "previous_root_verifier_immutable_source_SHA256": OLD_VERIFIER_SHA,
            "full_G2": False,
            "native_financial_bridge_open": True,
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
