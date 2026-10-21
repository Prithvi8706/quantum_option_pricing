"""Record completed experiment status and hash this execution's evidence snapshot."""

import hashlib
import json
import platform
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/limitation_audit_20261001"


def save_new(path, data):
    with path.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(data, indent=2, allow_nan=False) + "\n")


def run():
    completed = {
        "lookup": "lookup_v2/summary.json",
        "mcx_cleanup": "mcx_cleanup_v1/result.json",
        "compact_storage": "compact_storage_v1/summary.json",
        "gaussian": "gaussian_v3/summary.json",
        "heston_screen": "heston_screen_v1/summary.json",
        "bounded_probabilities": "bounded_probabilities_v1/summary.json",
        "pebbling": "pebbling_v1/summary.json",
        "multiplier": "multiplier_v2/summary.json",
    }
    for relative in completed.values():
        assert json.loads((OUT / relative).read_text())["passed"]
    combined = json.loads((OUT / completed["multiplier"]).read_text())
    for case in combined["cases"]:
        assert case["gate_replay"]["passed"] and case["faster_at_same_cap"]
        assert case["candidate"]["logical_qubits"] <= case["qubit_cap"]
    failures = {
        "lookup_v1": dict(reason="Experiment used cosunit instead of table generator's cos key",
                           corrected_in="lookup_v2", correctness_failure=False),
        "gaussian_v1": dict(reason="Six-qubit state exceeded 1e-11 amplitude tolerance",
            observed_error=1.8779081129571829e-6,
            implementation="Qiskit UCRY, transpiler optimization level 2",
            corrected_in="gaussian_v3"),
        "gaussian_v2": dict(reason="Ten-qubit state exceeded 1e-11 amplitude tolerance",
            observed_error=3.459815767214991e-11,
            implementation="Qiskit UCRY, optimization level 1; small angles pruned in UCRY",
            corrected_in="gaussian_v3", correction="Explicit Walsh/Gray rotation decomposition"),
        "multiplier_v1": dict(reason="Uniform parallelism limits erased the depth benefit at cap",
            best_capped_b4_t_depth=6079060, lookup_only_b4_t_depth=6026790,
            corrected_in="multiplier_v2", correction="Pack actual leaf scratch sizes per wave"),
    }
    for name, failure in failures.items():
        save_new(OUT / name / "failed_attempt.json", dict(status="failed attempt", **failure))
    python = ".context/frontier_t0_env/Scripts/python.exe"
    base = python + " -m research.limitation_audit_20261001."
    commands = {}
    for name, receipt in completed.items():
        destination = "results/limitation_audit_20261001/" + receipt.split("/")[0]
        extra = ""
        if name in ("compact_storage", "multiplier"):
            extra = " --source-root results/limitation_audit_20261001/lookup_v2"
        commands[name] = base + "experiment_" + name + extra + " --output " + destination
    tests = [
        "research/limitation_audit_20261001/test_lookup.py",
        "research/limitation_audit_20261001/test_compact_storage.py",
        "research/limitation_audit_20261001/test_carry_save_multiplier.py",
        "research/limitation_audit_20261001/test_budget_schedule.py",
        "research/controlled_source_completion/test_completion.py",
        "research/controlled_priority_completion/test_parallel_source.py",
        "research/controlled_completion_followup/test_truncated_multiplier.py",
    ]
    verification = dict(
        created_utc=datetime.now(timezone.utc).isoformat(),
        completed_receipts=completed, commands=commands,
        reproduction="Use a fresh output directory; existing result roots are never overwritten",
        tests=dict(command=python + " -m pytest " + " ".join(tests) + " -q",
                   observed_passes=66, observed_warnings=3, observed_seconds=42.68,
                   warning_kind="Pre-existing Qiskit QFT PendingDeprecationWarning",
                   evidence="Observed terminal run; this finalizer does not rerun the tests"),
        ruff="All new implementation and experiment Python files passed",
        python_version=platform.python_version(),
        packages={name: metadata.version(name)
                  for name in ("numpy", "numba", "scipy", "qiskit", "mpmath", "pytest")},
        conclusion="Exact full-source improvements verified. No end-to-end pricing "
        "advantage, physical timing, or complete approximate-law certificate established.",
    )
    save_new(OUT / "execution_verification_v1.json", verification)
    paths = list((ROOT / "research/limitation_audit_20261001").glob("*.py"))
    paths += [ROOT / "research/controlled_source_completion" / name for name in (
        "primitives.py", "exact_lookup.py", "compact_storage.py", "carry_save_multiplier.py",
        "budget_schedule.py",
    )]
    paths += list((ROOT / "docs/limitation_audit_20261001").glob("*.md"))
    for relative in completed.values():
        paths += [p for p in (OUT / relative.split("/")[0]).rglob("*") if p.is_file()]
    paths += [OUT / "execution_verification_v1.json"]
    paths += [OUT / name / "failed_attempt.json" for name in failures]
    hashes = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(set(paths))}
    save_new(OUT / "execution_manifest_v1.json", dict(
        format="sha256-execution-snapshot-v1", files=hashes,
        note="The earlier audit_manifest.json remains a historical snapshot. This "
        "manifest covers the updated audit README, execution report and new evidence.",
    ))
    print("Verified eight completed experiments; hashed", len(hashes), "files")


if __name__ == "__main__":
    run()
