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
OUTPUT = PROGRAM / "E07_original_BM_G2_root_verification_run001"
CPU, ADMISSION, WALL = 120, 90, 600
EXPECTED_MANIFESTS = dict(
    zip(
        (
            "E07_original_BM_G2_composition_run001",
            "E07_original_BM_G2_composition_audit_run001",
            "A02_BM_native_financial_bridge_root_verification_run001",
        ),
        (
            "c5cb25db09f079191908bf0ae4fea68239ee3bdc5222d19dd27d0d7c1d0ee2bc",
            "06b10c8974c130a61729d38ae94d168be8be1d27a0956c7b8ce0b4369870f7e9",
            "eab61f5775110021e4e514b7412ce56ca9b24aec13311e32d240dc1559cb59ab",
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
        "E07_original_BM_G2_composition_run001",
        "E07_original_BM_G2_composition_audit_run001",
    ):
        directory = PROGRAM / name
        summary = json.loads((directory / "summary.json").read_bytes())
        completion = json.loads((directory / "completion_outcome.json").read_bytes())
        require(
            summary["passed"] and completion["passed"] and completion["completed"],
            "Actual completed PASS",
        )
        require(
            not summary["budget_censored"] and not completion["budget_censored"],
            "Uncensored accounting",
        )
        require(
            summary["new_test_credit"] == 0 and summary["new_gate_replays"] == 0, "Zero recredit"
        )
        require(
            summary["both_exact_dollar_bounds_fit"] and summary["physical_failure_remains_NULL"],
            "Dollar bounds fit and physical NULL preserved",
        )
        require(
            not summary["complete_price_certified"]
            and not summary["G3_G4_G5_complete"]
            and not summary["adoption"]
            and not summary["cost_transfer"]
            and not summary["quantum_advantage"],
            "Scoped mathematical bias only",
        )
    audit = json.loads(
        (PROGRAM / "E07_original_BM_G2_composition_audit_run001/summary.json").read_bytes()
    )
    require(
        audit["independent_composition_audit_passed"]
        and audit["source_specific_mathematical_G2_bias_complete"],
        "Actual independent source-specific mathematical G2 closure",
    )
    require(
        audit["actual_composition_producer_manifest_SHA256"]
        == EXPECTED_MANIFESTS["E07_original_BM_G2_composition_run001"],
        "Audit exact producer binding",
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
            "schema": "root-original-BM-G2-composition-fresh-integrity-v1",
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
            "source_specific_mathematical_G2_bias_complete": True,
            "physical_failure_remains_NULL": True,
            "complete_price_certified": False,
            "G3_G4_G5_complete": False,
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
