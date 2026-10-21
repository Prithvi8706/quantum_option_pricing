"""Freeze one scalar AS241-law transfer after the native transform proof passes."""

import argparse
from datetime import datetime, timezone
from pathlib import Path
import re
import shutil
import sys
import time
import traceback
import xml.etree.ElementTree as ET

import pytest

from research.limitation_program_20261001.audit_quantile_grid import (
    BUILDER,
    audit_builder_contract,
    audit_task,
    independent_model,
)
from research.limitation_program_20261001.constant_library import digest
from research.limitation_program_20261001.experiment_checkpoint import (
    PROGRAM,
    read,
    relative,
    save,
    verify,
)
from research.limitation_program_20261001.progress import ROOT
from research.limitation_program_20261001.quantile_as241_law_certificate import (
    ALLOWANCE,
    CASES,
    TARGET,
    law_bound,
    pair,
    validate_native_error,
)


TRANSFORM = PROGRAM / "A02_quantile_transform_run002"
GRID_AUDIT = PROGRAM / "C06_quantile_grid_audit_run001"
TRANSFORM_AUDIT = PROGRAM / "A02_quantile_transform_audit_run001"
CODE = (
    "quantile_as241_law_certificate.py",
    "test_quantile_as241_law_certificate.py",
    "experiment_quantile_as241_law.py",
)
DECLARED_UNIQUE_TESTS = 36
CPU_LIMIT = 60


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


def _test_credit(path):
    cases = list(ET.parse(path).getroot().iter("testcase"))
    names = [(case.attrib.get("classname", ""), case.attrib["name"]) for case in cases]
    if len(cases) != DECLARED_UNIQUE_TESTS or len(set(names)) != DECLARED_UNIQUE_TESTS:
        raise AssertionError("Frozen AS241-law unique fixture count differs")
    if any(case.find(tag) is not None for case in cases for tag in ("failure", "error", "skipped")):
        raise AssertionError("Only distinct nonfailed nonskipped fixtures receive credit")
    return {
        "declared_unique_tests": DECLARED_UNIQUE_TESTS,
        "unique_actual_testcases": len(set(names)),
        "test_identities": [list(value) for value in names],
        "failure_error_or_skip_count": 0,
    }


def prepare(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM.resolve())
    if output.exists():
        raise FileExistsError("Fresh prospective AS241-law receipt required")
    transform_summary = read(TRANSFORM / "summary.json")
    if (
        transform_summary.get("passed") is not True
        or transform_summary.get("native_transform_certificate_succeeded") is not True
        or transform_summary.get("budget_censored") is not False
    ):
        raise ValueError(
            "Successful uncensored native transform receipt required before law transfer"
        )
    if read(GRID_AUDIT / "summary.json").get("passed") is not True:
        raise ValueError("Accepted original model/coordinate variation audit required")
    receipts = [TRANSFORM, GRID_AUDIT, TRANSFORM_AUDIT]
    frozen = {}
    for receipt_dir in receipts:
        summary = read(receipt_dir / "summary.json")
        if summary.get("passed") is not True or summary.get("budget_censored", False) is not False:
            raise ValueError("Successful uncensored prerequisite required: " + receipt_dir.name)
        receipt = read(receipt_dir / "manifest.json")
        if (
            not {"files", "frozen_inputs"}.issubset(receipt)
            or not set(receipt).issubset({"files", "frozen_inputs", "manifest_self_hash_excluded"})
            or receipt.get("manifest_self_hash_excluded", True) is not True
        ):
            raise ValueError("Explicit prerequisite manifest schema required")
        for field in ("files", "frozen_inputs"):
            for path, sha in receipt[field].items():
                bind(frozen, path, sha)
        bind(frozen, receipt_dir / "manifest.json", digest(receipt_dir / "manifest.json"))
    dependencies = (
        "audit_quantile_grid.py",
        "constant_library.py",
        "experiment_checkpoint.py",
        "progress.py",
    )
    for name in CODE + dependencies:
        path = ROOT / "research/limitation_program_20261001" / name
        bind(frozen, path, digest(path))
    bind(frozen, BUILDER, digest(BUILDER))
    bind(frozen, Path(sys.executable), digest(Path(sys.executable)))
    tasks = {case: PROGRAM / "G0_run003" / (case + "_task.json") for case in CASES}
    for path in tasks.values():
        bind(frozen, path, digest(path))
    verify({"frozen_inputs": frozen})
    output.mkdir()
    try:
        prepare_receipt(output, frozen, tasks)
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
                "different_AS241_scalar_law_ideal_GBM_bias_certificate": False,
                "new_financial_price_observations_or_gate_replays": 0,
            },
        )
        finish_manifest(output, {"frozen_inputs": frozen})
        raise


def prepare_receipt(output, frozen, tasks):
    for name in CODE:
        source = ROOT / "research/limitation_program_20261001" / name
        destination = output / name
        shutil.copy2(source, destination)
        if digest(destination) != frozen[relative(source)]:
            raise ValueError("Law snapshot differs from frozen source bytes")
        bind(frozen, destination, frozen[relative(source)])
    protocol = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "local_only": True,
        "before_tests_and_new_law_bound_evaluation": True,
        "declared_unique_tests": DECLARED_UNIQUE_TESTS,
        "new_laws": 1,
        "law": "independent q32 midpoint inputs, mathematical-native signed-restored AS241",
        "uniform_bits": 32,
        "fraction_bits": 40,
        "native_word_width": 72,
        "cases": list(CASES),
        "all_input_quantile_premise_receipt": relative(TRANSFORM),
        "mandatory_independent_transform_audit": relative(TRANSFORM_AUDIT),
        "all_input_quantile_premise_target_exact": pair(TARGET),
        "quantile_premise_reconciliation": (
            "Successful uncensored transform; complete960 table/exponent classes; "
            "complete1024 fresh tail sums/rho flags; saved exact tail/central maximum."
        ),
        "transfer_theorems": 1,
        "transfer_method": (
            "Pointwise same-input quantile displacement implies Fgrid(x-E)<=Fnew(x) "
            "<=Fgrid(x+E), without monotonicity. Gaussian pdf<2/5 and midpoint CDF "
            "error2^-33 imply KS<=2^-33+(2/5)E. Coordinate BV<=80 dollars and "
            "independent product telescope give idealGBM bias<=80*d*KS."
        ),
        "independence": "Independent raw q32 words; no finite Box-Muller pair independence claim",
        "fixed_separate_exploratory_law_allowance_dollars_exact": pair(ALLOWANCE),
        "original_model_builder": relative(BUILDER),
        "original_model_tasks": {case: relative(path) for case, path in tasks.items()},
        "fixtures": (
            "Exact nonmonotone finite-output CDF sandwich; strict/closed half-line "
            "atoms; exact two-coordinate abstract BV knockout; prerequisite forgery guards."
        ),
        "numerical_normal_CDF_or_quantile_evaluations": 0,
        "new_q32_word_or_interval_cell_evaluations": 0,
        "original_financial_price_observations_or_gate_replays": 0,
        "prior_exact_floor_quantile_law_ULP_added": False,
        "process_CPU_limit_seconds": CPU_LIMIT,
        "interpreter_and_every_frozen_insertion_preserve_historical_expectations": True,
        "bulk_output_hashing_and_verification_before_terminal_CPU_check": True,
        "adaptive_method_precision_partition_or_retry": False,
        "native_financial_exp_clipping_or_path_certified": False,
        "coherent_loader_or_divider_adopted": False,
        "actual_quantum_gate_cost": None,
        "accepted_Box_Muller_baseline_changed": False,
        "complete_original_price_certified": False,
        "full_G2_closed": False,
        "quantum_advantage_established": False,
        "preexisting_Stage_C_jobs_edited": False,
        "frozen_inputs": frozen,
        "python": sys.version,
        "executable": sys.executable,
    }
    save(output / "protocol.json", protocol)
    verify(protocol)
    print("One all-input AS241 ideal-law transfer prospectively frozen", flush=True)


def run(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM.resolve())
    if (output / "summary.json").exists():
        raise FileExistsError("AS241-law receipt is already terminal")
    protocol = read(output / "protocol.json")
    started = time.process_time()
    files = None
    try:
        verify(protocol)
        rc = pytest.main(
            [
                str(
                    ROOT
                    / "research/limitation_program_20261001/test_quantile_as241_law_certificate.py"
                ),
                "-q",
                "-p",
                "no:cacheprovider",
                "--junitxml=" + str(output / "tests.xml"),
            ]
        )
        if rc:
            raise AssertionError("Frozen AS241-law theorem fixtures failed: " + str(int(rc)))
        verify(protocol)
        credit = _test_credit(output / "tests.xml")
        save(output / "test_credit_reconciliation.json", credit)
        native = read(TRANSFORM / "native_transform_certificate.json")
        sensitivity = read(TRANSFORM / "fresh_tail_sensitivity.json")
        error = validate_native_error(native, sensitivity)
        save(
            output / "native_error_reconciliation.json",
            {
                "passed": True,
                "prerequisite_manifest_sha256": digest(TRANSFORM / "manifest.json"),
                "native_quantile_error_upper_exact": pair(error),
                "native_log_class_count": 960,
                "fresh_tail_row_count": 1024,
                "old_conditional_floor_arithmetic_error_added": False,
                "previous_exact_floor_quantile_law_ULP_added": False,
                "previous_test_counts_credited_again": 0,
            },
        )
        builder = audit_builder_contract()
        cases = []
        for case in protocol["cases"]:
            model = independent_model(case)
            audit_task(read(ROOT / protocol["original_model_tasks"][case]), case)
            if model["builder_sha256"] != builder["builder_sha256"]:
                raise ValueError("Original economic builder binding differs")
            row = law_bound(model, error)
            row["proof_premise_bound_to_successful_all_input_certificate"] = True
            row["original_model_binding"] = model
            row["original_economic_template_checked"] = builder
            save(output / (case + "_certificate.json"), row)
            cases.append({key: value for key, value in row.items() if key != "proof"})
        verify(protocol)
        files = receipt_files(output)
        elapsed = time.process_time() - started
        budget_censored = elapsed > protocol["process_CPU_limit_seconds"]
        save(
            output / "summary.json",
            {
                "passed": not budget_censored,
                "local_only": True,
                "budget_censored": budget_censored,
                "reason": "fixed_process_CPU_limit" if budget_censored else None,
                "new_unique_fixtures_passed": credit["unique_actual_testcases"],
                "previous_fixture_counts_credited_again": 0,
                "different_AS241_scalar_law_ideal_GBM_bias_certificate": not budget_censored,
                "cases": cases,
                "both_bias_bounds_fit_separate_exploratory_allowance": all(
                    row["new_law_bias_fits_separate_exploratory_allowance"] for row in cases
                ),
                "native_financial_path_price_bound": None,
                "coherent_loader_or_divider_adopted": False,
                "accepted_Box_Muller_baseline_changed": False,
                "complete_original_price_certified": False,
                "full_G2_closed": False,
                "quantum_advantage_established": False,
                "new_financial_price_observations_or_gate_replays": 0,
                "elapsed_process_CPU_seconds": elapsed,
            },
        )
    except BaseException as failure:
        save(
            output / "summary.json",
            {
                "passed": False,
                "budget_censored": isinstance(failure, TimeoutError),
                "different_AS241_scalar_law_ideal_GBM_bias_certificate": False,
                "terminal_failure": traceback.format_exc(),
                "new_financial_price_observations_or_gate_replays": 0,
            },
        )
        finish_manifest(output, protocol, files)
        raise
    finish_manifest(output, protocol, files)
    print(
        "AS241 law transfer retained; native financial path and coherent loader remain open",
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    (prepare if args.mode == "prepare" else run)(args.output)
