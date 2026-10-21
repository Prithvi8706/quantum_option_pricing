"""Prospective two-shape AS241 financial SSA splice; no source/gate compilation."""

import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import re
import shutil
import sys
import time
import traceback
import xml.etree.ElementTree as ET

os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["NUMBA_NUM_THREADS"] = "1"

import pytest  # noqa: E402

from research.limitation_program_20261001.as241_financial_target import (  # noqa: E402
    CASES,
    SCALAR,
    build_financial_target,
    load_archive,
    load_scalar,
    validate_financial_binding,
)
from research.limitation_program_20261001.experiment_checkpoint import (  # noqa: E402
    relative,
    save,
    verify,
)
from research.limitation_program_20261001.scalar_quantile_ir import (  # noqa: E402
    ROOT,
    PROGRAM,
    read,
)
from research.limitation_program_20261001.scalar_quantile_source import digest  # noqa: E402


CODE = (
    "as241_financial_target.py",
    "test_as241_financial_target.py",
    "experiment_as241_financial_target.py",
    "as241_financial_target_preflight.json",
)
RECEIPTS = (
    "A02_quantile_scalar_run001",
    "A02_quantile_scalar_audit_run001",
    "A02_quantile_transform_run002",
    "A02_quantile_law_run001",
    "C06_pair_run001",
    "C06_pair_audit_run001",
    "E03_support_run001",
    "E03_support_audit_run002",
)
DEPENDENCIES = (
    "research/limitation_program_20261001/scalar_quantile_ir.py",
    "research/limitation_program_20261001/scalar_quantile_source.py",
    "research/limitation_program_20261001/experiment_checkpoint.py",
    "research/limitation_program_20261001/constant_library.py",
    "research/limitation_program_20261001/progress.py",
    "research/controlled_source_completion/ir.py",
    "research/controlled_source_completion/compiler.py",
    "research/controlled_priority_completion/parallel_source.py",
    "research/advantage_frontier_20260923/barrier_oracle_depth.py",
    "research/controlled_source_completion/finance.py",
)
DECLARED_TESTS = 36
CPU_LIMIT = 180
WALL_LIMIT = 600
ADMISSION_CPU = 150


def bind(frozen, name, expected):
    path = Path(str(name).replace("\\", "/"))
    path = path.resolve() if path.is_absolute() else (ROOT / path).resolve()
    normalized = relative(path)
    if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
        raise ValueError("Explicit prerequisite SHA256 required")
    if normalized in frozen and frozen[normalized] != expected:
        raise ValueError("Historical prerequisite bytes conflict: " + normalized)
    frozen[normalized] = expected


def receipt_files(output):
    return {
        relative(path): digest(path)
        for path in sorted(output.rglob("*"))
        if path.is_file() and path.name != "manifest.json"
    }


def finish_manifest(output, protocol, files=None):
    if files is None:
        files = receipt_files(output)
    else:
        files = dict(files)
        files[relative(output / "summary.json")] = digest(output / "summary.json")
    save(
        output / "manifest.json",
        {
            "files": files,
            "frozen_inputs": protocol["frozen_inputs"],
            "manifest_self_hash_excluded": True,
        },
    )


def _prerequisite_inputs():
    frozen = {}
    for name in RECEIPTS:
        directory = PROGRAM / name
        summary = read(directory / "summary.json")
        if summary.get("passed") is not True or summary.get("budget_censored", False) is not False:
            raise ValueError("Successful prerequisite required: " + name)
        if (
            name
            in (
                "A02_quantile_scalar_run001",
                "A02_quantile_scalar_audit_run001",
                "A02_quantile_transform_run002",
            )
            and summary.get("budget_censored") is not False
        ):
            raise ValueError("Uncensored scalar and transform prerequisites required")
        receipt = read(directory / "manifest.json")
        allowed = {"files", "frozen_inputs", "manifest_self_hash_excluded"}
        if name == "C06_pair_run001":
            allowed.add("historical_receipts_unchanged")
        if not {"files", "frozen_inputs"}.issubset(receipt) or not set(receipt).issubset(allowed):
            raise ValueError("Explicit structured prerequisite manifest schema required")
        if (
            "manifest_self_hash_excluded" in receipt
            and receipt["manifest_self_hash_excluded"] is not True
        ):
            raise ValueError("Manifest self-exclusion marker must be exactly true")
        if (
            "historical_receipts_unchanged" in receipt
            and receipt["historical_receipts_unchanged"] is not True
        ):
            raise ValueError("Historical-receipts marker must be exactly true")
        for field in ("files", "frozen_inputs"):
            if not isinstance(receipt[field], dict):
                raise ValueError("Explicit structured prerequisite path hashes required")
            for path, expected in receipt[field].items():
                bind(frozen, path, expected)
        bind(frozen, directory / "manifest.json", digest(directory / "manifest.json"))
    return frozen


def prepare(output):
    """Admission reads only existing accepted artifacts; constructs no graph."""
    output = Path(output).resolve()
    output.relative_to(PROGRAM.resolve())
    if output.exists():
        raise FileExistsError("Fresh two-shape financial-target receipt required")
    frozen = _prerequisite_inputs()
    load_scalar()
    for case in CASES:
        _, archive = load_archive(case)
        for key in ("accepted_target", "accepted_source", "original_builder"):
            path = ROOT / archive[key]
            if archive[key + "_sha256"] != digest(path):
                raise ValueError("Archived financial source binding differs")
            bind(frozen, path, digest(path))
    for path in [ROOT / "research/limitation_program_20261001" / name for name in CODE] + [
        ROOT / name for name in DEPENDENCIES
    ]:
        bind(frozen, path, digest(path))
    bind(frozen, Path(sys.executable), digest(Path(sys.executable)))
    verify({"frozen_inputs": frozen})
    output.mkdir()
    try:
        prepare_receipt(output, frozen)
    except BaseException as failure:
        save(
            output / "preparation_failure.json",
            {"failure": traceback.format_exc(), "partial_files_preserved": True},
        )
        save(
            output / "summary.json",
            {
                "passed": False,
                "preparation_failed": True,
                "budget_censored": isinstance(failure, TimeoutError),
                "new_financial_path_or_price_evaluations": 0,
                "full_financial_quantum_source_compilations": 0,
            },
        )
        finish_manifest(output, {"frozen_inputs": frozen})
        raise


def prepare_receipt(output, frozen):
    for name in CODE:
        source = ROOT / "research/limitation_program_20261001" / name
        destination = output / name
        shutil.copy2(source, destination)
        if digest(destination) != frozen[relative(source)]:
            raise ValueError("Financial frontend snapshot differs from frozen source bytes")
        bind(frozen, destination, frozen[relative(source)])
    protocol = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "local_only": True,
        "before_tests_or_full_financial_target_construction": True,
        "fixed_financial_shapes": list(CASES),
        "scalar_receipt": relative(SCALAR),
        "independent_scalar_source_audit_receipt": (
            "results/limitation_program_20261001/A02_quantile_scalar_audit_run001"
        ),
        "required_complete_successful_receipts": list(RECEIPTS),
        "uniform_inputs_per_shape": {"B4x12": 60, "B8x52": 468},
        "uniform_bits_each": 32,
        "native_width": 72,
        "fraction_bits": 40,
        "new_normal_law": "Independent q32 midpoint mathematical-native signed-restored AS241",
        "normal_order": "date major: common, then each asset idiosyncratic",
        "graph_construction": (
            "Independent renamed copies of accepted scalar SSA; original financial Y closure "
            "copied verbatim with only SSA IDs remapped at original normal boundaries"
        ),
        "financial_source_equality": (
            "Complete boundary-normalized financial DAG, ordered op/arity/raw params/lookup "
            "hashes; actual reconstructed original-to-new correspondence, semantic inventory"
        ),
        "target_sha256_algorithm": (
            "SHA256(sorted compact canonical JSON UTF8); file hashes separately bound"
        ),
        "financial_literal_policy": (
            "Exact archive raw literals, no float APIs or table regeneration"
        ),
        "optimizer": "none",
        "declared_unique_tests": DECLARED_TESTS,
        "financial_path_or_price_evaluations": 0,
        "full_financial_gate_replays": 0,
        "new_quantum_leaf_generations": 0,
        "full_quantum_financial_source_compilations": 0,
        "native_financial_bias_proof_or_sampler_adoption": False,
        "complete_estimator_or_price_adoption": False,
        "old_joint_Box_Muller_price_ledger_filled": False,
        "old_E02_source_or_wrapper_costs_transferred": False,
        "new_source_ledger_epsilon_exact": [1, 100],
        "new_source_statistical_allowance_exact": [9, 2000],
        "new_source_financial_residual_allowance_exact": [11, 2000],
        "all_new_source_wrapper_or_estimator_gate_resources": None,
        "full_G2_or_quantum_advantage_established": False,
        "process_CPU_limit_seconds": CPU_LIMIT,
        "interpreter_and_every_frozen_insertion_preserve_historical_expectations": True,
        "bulk_output_hashing_and_verification_before_terminal_CPU_wall_check": True,
        "elapsed_wall_limit_seconds": WALL_LIMIT,
        "new_work_admission_CPU_seconds": ADMISSION_CPU,
        "numerical_threads_per_process": 1,
        "adaptive_source_shape_or_fixture_retry": False,
        "preexisting_Stage_C_jobs_edited": False,
        "frozen_inputs": frozen,
        "python": sys.version,
        "executable": sys.executable,
    }
    save(output / "protocol.json", protocol)
    verify(protocol)
    print("Exactly two financial target shapes prospectively frozen; no compilation", flush=True)


def _credit(path):
    cases = list(ET.parse(path).getroot().iter("testcase"))
    identities = [(case.attrib.get("classname", ""), case.attrib["name"]) for case in cases]
    if len(cases) != DECLARED_TESTS or len(set(identities)) != DECLARED_TESTS:
        raise AssertionError("Declared unique financial splice fixture count differs")
    if any(case.find(tag) is not None for case in cases for tag in ("failure", "error", "skipped")):
        raise AssertionError("Failed/error/skipped financial fixtures cannot receive credit")
    return {
        "new_unique_test_cases": DECLARED_TESTS,
        "prior_test_counts_added_again": 0,
        "identities": [list(identity) for identity in identities],
    }


def run(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM.resolve())
    if (output / "summary.json").exists():
        raise FileExistsError("Financial-target receipt already terminal")
    protocol = read(output / "protocol.json")
    start_cpu, start_wall = time.process_time(), time.monotonic()
    files = None

    def admit():
        if (
            time.process_time() - start_cpu >= ADMISSION_CPU
            or time.monotonic() - start_wall >= WALL_LIMIT
        ):
            raise TimeoutError("Fixed financial-target work admission reached; no new shape/retry")

    try:
        verify(protocol)
        rc = pytest.main(
            [
                str(ROOT / "research/limitation_program_20261001/test_as241_financial_target.py"),
                "-q",
                "-p",
                "no:cacheprovider",
                "--junitxml=" + str(output / "tests.xml"),
            ]
        )
        if rc:
            raise AssertionError("Financial splice structural fixtures failed: " + str(int(rc)))
        credit = _credit(output / "tests.xml")
        save(output / "test_credit_reconciliation.json", credit)
        rows = []
        for case in CASES:
            admit()
            target, bundle = build_financial_target(case)
            checked = validate_financial_binding(target, bundle)
            directory = output / case
            save(directory / "target.json", target)
            save(directory / "bundle.json", bundle)
            save(directory / "new_source_matched_ledger.json", bundle["new_source_matched_ledger"])
            save(directory / "source_binding_validation.json", checked)
            rows.append(
                {
                    "case": case,
                    "assets": bundle["assets"],
                    "dates": bundle["dates"],
                    "independent_uniform_normal_producers": len(bundle["normal_values"]),
                    "uniform_input_qubits": 32 * len(target["inputs"]),
                    "target_nodes": len(target["nodes"]),
                    "target_sha256": bundle["target_sha256"],
                    "target_file_sha256": digest(directory / "target.json"),
                    "bundle_file_sha256": digest(directory / "bundle.json"),
                    "normalized_financial_closure_sha256": checked[
                        "normalized_financial_closure_sha256"
                    ],
                    "source_binding_validation_passed": True,
                    "actual_source_gate_resources": None,
                    "actual_wrapper_gate_resources": None,
                    "native_financial_bias_bound": None,
                }
            )
        verify(protocol)
        files = receipt_files(output)
        cpu, wall = time.process_time() - start_cpu, time.monotonic() - start_wall
        censored = cpu > CPU_LIMIT or wall > WALL_LIMIT
        save(
            output / "summary.json",
            {
                "passed": not censored,
                "local_only": True,
                "budget_censored": censored,
                "unique_new_pytest_cases": DECLARED_TESTS,
                "prior_test_counts_added_again": 0,
                "cases": rows,
                "new_financial_target_shapes": 2,
                "actual_scalar_producers_and_normalized_original_finance_bound": True,
                "original_raw_literals_stock_clamps_and_strict_barrier_preserved": True,
                "new_source_matched_ledger_separate_from_old_joint_Box_Muller": True,
                "new_financial_path_or_price_evaluations": 0,
                "new_financial_gate_replays": 0,
                "new_quantum_leaf_generations": 0,
                "full_financial_quantum_source_compilations": 0,
                "native_financial_bias_certificate_adopted": False,
                "complete_estimator_or_price_certificate_adopted": False,
                "old_E02_source_or_wrapper_costs_transferred": False,
                "full_G2_or_quantum_advantage_established": False,
                "CPU_seconds": cpu,
                "wall_seconds": wall,
            },
        )
    except BaseException as failure:
        save(
            output / "summary.json",
            {
                "passed": False,
                "budget_censored": isinstance(failure, TimeoutError),
                "terminal_failure": traceback.format_exc(),
                "new_financial_path_or_price_evaluations": 0,
                "new_financial_gate_replays": 0,
                "full_financial_quantum_source_compilations": 0,
            },
        )
        finish_manifest(output, protocol, files)
        raise
    finish_manifest(output, protocol, files)
    print(
        "Two exact financial target splices retained; native bias/source compilation open",
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    (prepare if args.mode == "prepare" else run)(args.output)
