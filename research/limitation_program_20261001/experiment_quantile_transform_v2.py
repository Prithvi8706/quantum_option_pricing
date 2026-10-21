"""Freeze one native q32 logarithm/root proof and fresh tail sensitivity ledger."""

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
import mpmath as mp

from research.limitation_program_20261001.constant_library import digest
from research.limitation_program_20261001.experiment_checkpoint import (
    PROGRAM,
    read,
    relative,
    save,
    verify,
)
from research.limitation_program_20261001.progress import ROOT
from research.limitation_program_20261001.quantile_transform_certificate import (
    CENTRAL,
    EXPONENTS,
    INTERVAL_DIGITS,
    PAIR,
    TAIL,
    TARGET,
    certify,
    source_inputs,
)
from research.limitation_program_20261001.quantile_transform_native import (
    mathematical_transform_word,
)


PAIR_AUDIT = PROGRAM / "C06_pair_audit_run001"
CENTRAL_AUDIT = PROGRAM / "A02_quantile_central_audit_run001"
TAIL_AUDIT = PROGRAM / "A02_quantile_tail_audit_run001"
SQRT_METADATA = PROGRAM / "A10_coefficient_run001/B4x12/min-depth/leaves/160a18dba2e09b8e1ad2.json"
CODE = (
    "quantile_transform_native.py",
    "quantile_transform_certificate.py",
    "test_quantile_transform_certificate.py",
    "experiment_quantile_transform_v2.py",
    "quantile_transform_preflight_v2.json",
)
FIXTURE_WORDS = (0, 1, (1 << 17) - 1, (1 << 28) - 1, 322122546, (1 << 32) - 1)
DECLARED_UNIQUE_TESTS = 26
EXECUTED_PREDECESSOR = (
    ROOT / "research/limitation_program_20261001/experiment_quantile_transform.py"
)
ADMISSION_FAILURE = PROGRAM / "A02_quantile_transform_admission_failure_run001"


def validate_prerequisite_manifest(receipt, case):
    allowed = {"files", "frozen_inputs", "manifest_self_hash_excluded"}
    if case == PAIR:
        allowed.add("historical_receipts_unchanged")
    if (
        not {"files", "frozen_inputs"}.issubset(receipt)
        or not set(receipt).issubset(allowed)
        or receipt.get("manifest_self_hash_excluded", True) is not True
        or (
            "historical_receipts_unchanged" in receipt
            and receipt["historical_receipts_unchanged"] is not True
        )
        or any(not isinstance(receipt[field], dict) for field in ("files", "frozen_inputs"))
    ):
        raise ValueError("Explicit prerequisite manifest schema required")


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


def verify_unique_testcases(path):
    suites = ET.parse(path).getroot()
    cases = list(suites.iter("testcase"))
    identities = [(case.attrib.get("classname", ""), case.attrib["name"]) for case in cases]
    if len(cases) != DECLARED_UNIQUE_TESTS or len(set(identities)) != DECLARED_UNIQUE_TESTS:
        raise AssertionError("Declared unique native-transform fixture count differs")
    if any(case.find(tag) is not None for case in cases for tag in ("failure", "error", "skipped")):
        raise AssertionError("Native-transform fixture failure/error/skip cannot receive credit")
    return {
        "declared_unique_tests": DECLARED_UNIQUE_TESTS,
        "actual_testcases": len(cases),
        "unique_actual_testcases": len(set(identities)),
        "failures_errors_and_skips": 0,
        "test_identities": [[classname, name] for classname, name in identities],
    }


def prepare(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM.resolve())
    if output.exists():
        raise FileExistsError("Fresh prospective native-transform receipt required")
    if not read(TAIL / "summary.json")["tail_certificate_succeeded"]:
        raise ValueError("Completed successful conditional tail certificate required")
    if not read(CENTRAL / "summary.json")["central_certificate_succeeded"]:
        raise ValueError("Completed successful central certificate required")
    if not read(PAIR_AUDIT / "summary.json")["passed"]:
        raise ValueError("Independently audited original native log/root semantics required")
    _, ln2, binding = source_inputs()
    sqrt = read(SQRT_METADATA)
    spec = sqrt["spec"]
    if not (
        spec["op"] == "sqrt"
        and spec["width"] == 72
        and spec["fraction_bits"] == 40
        and spec["active_input_bits"] == 46
        and spec["lowering"] == "unsigned-nonrestoring-sqrt-signed-remainder-v1"
        and spec["input_contract"] == {"unsigned_input_bits": 46}
    ):
        raise ValueError("Archived exact unsigned46 nonrestoring sqrt reference changed")
    frozen = {}
    receipts = [PAIR, PAIR_AUDIT, CENTRAL, CENTRAL_AUDIT, TAIL, TAIL_AUDIT]
    for case in receipts:
        summary = read(case / "summary.json")
        if summary.get("passed") is not True or summary.get("budget_censored", False) is not False:
            raise ValueError("Successful uncensored prerequisite required: " + case.name)
        receipt = read(case / "manifest.json")
        validate_prerequisite_manifest(receipt, case)
        for field in ("files", "frozen_inputs"):
            for name, sha in receipt[field].items():
                bind(frozen, name, sha)
        bind(frozen, case / "manifest.json", digest(case / "manifest.json"))
    for name in CODE:
        path = ROOT / "research/limitation_program_20261001" / name
        bind(frozen, path, digest(path))
    diagnostic = read(ADMISSION_FAILURE / "manifest.json")
    validate_prerequisite_manifest(diagnostic, ADMISSION_FAILURE)
    for field in ("files", "frozen_inputs"):
        for name, sha in diagnostic[field].items():
            bind(frozen, name, sha)
    bind(frozen, ADMISSION_FAILURE / "manifest.json", digest(ADMISSION_FAILURE / "manifest.json"))
    bind(frozen, EXECUTED_PREDECESSOR, digest(EXECUTED_PREDECESSOR))
    for path in (
        SQRT_METADATA,
        Path(sys.executable),
        ROOT / "research/controlled_source_completion/ir.py",
        ROOT / "research/controlled_source_completion/nonrestoring_sqrt.py",
        ROOT / "research/limitation_program_20261001/constant_library.py",
        ROOT / "research/limitation_program_20261001/experiment_checkpoint.py",
        ROOT / "research/limitation_program_20261001/progress.py",
    ):
        bind(frozen, path, digest(path))
    for path in sorted(Path(mp.__file__).parent.rglob("*.py")):
        bind(frozen, path, digest(path))
    verify({"frozen_inputs": frozen})
    output.mkdir()
    try:
        prepare_receipt(output, frozen, ln2, binding)
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
                "native_transform_certificate_succeeded": False,
                "new_original_financial_prices_or_gates": 0,
            },
        )
        finish_manifest(output, {"frozen_inputs": frozen})
        raise


def prepare_receipt(output, frozen, ln2, binding):
    for name in CODE:
        source = ROOT / "research/limitation_program_20261001" / name
        destination = output / name
        shutil.copy2(source, destination)
        if digest(destination) != frozen[relative(source)]:
            raise ValueError("Transform snapshot differs from frozen source bytes")
        bind(frozen, destination, frozen[relative(source)])
    protocol = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "local_only": True,
        "before_tests_or_native_transform_proof_evaluation": True,
        "operational_producer_version": 2,
        "demonstrated_predecessor_admission_failure_receipt": relative(ADMISSION_FAILURE),
        "executed_predecessor_source": relative(EXECUTED_PREDECESSOR),
        "known_C06_pair_manifest_provenance_marker": {"historical_receipts_unchanged": True},
        "unknown_manifest_fields_and_conflicting_historical_hashes_rejected": True,
        "proof_helpers_tests_method_precision_and_CPU_budget_changed": False,
        "declared_unique_tests": DECLARED_UNIQUE_TESTS,
        "mandatory_independent_tail_audit_receipt": relative(TAIL_AUDIT),
        "interpreter_and_all_mpmath_python_sources_hash_bound": True,
        "mpmath_version": mp.__version__,
        "uniform_bits": 32,
        "fraction_bits": 40,
        "native_word_width": 72,
        "ordinary_tail_probability_domain_exact": [[1, 1 << 33], [3, 40]],
        "upper_probability_endpoint_exclusive": True,
        "source_bindings": binding,
        "original_ln2_raw": ln2,
        "original_log_table_cells": 32,
        "original_log_polynomial_degree": 8,
        "fixed_exponent_classes": list(EXPONENTS),
        "fixed_table_cell_exponent_combinations": 960,
        "all_input_proof_method": (
            "Exact q32 midpoint/complement is odd*128; msb in[7,36], exponent[-33,-4]. "
            "Only left normalization shifts; mantissa in[1,2) with11 low zero bits. "
            "Input/mantissa clamps inactive. Every32-cell log table Taylor/rounding/ "
            "8-Horner-floor error is combined with all30 exponent ln2 literal errors. "
            "These960 conservative combinations include unreachable combinations."
        ),
        "interval_methods": 1,
        "interval_decimal_precision": INTERVAL_DIGITS,
        "continuous_uniform_midpoint_cutoff_coupling_used": False,
        "native_transform_method": (
            "Negate ALREADY floored native log by exact signed subtraction. "
            "Prove true negative log>2.59 and native log error<.001; native radicand> "
            "2.589>1.609^2>1.6^2. Both roots>=1.6 gives5Elog/16 perturbation; add "
            "isqrt(a_raw<<40) floor1ulp and nearest-f40(8/5) literal error. "
            "Prove rnative in[0,3.21], unsigned45 radicand input within accepted46 "
            "semantic promise, output43, stored72/full144/shiftedradicand86 safety."
        ),
        "fresh_rational_sensitivity_method": (
            "For each1024 frozen tail REAL-error rows, enlarge input interval by rho "
            "using proven native rdomain, bound positive coefficient/Horner errors plus "
            "rho times polynomial derivatives, divide by monotone native B lower, add "
            "divisionulp. rho REPLACES the prior hypothetical argument-floor1ulp. "
            "No old conditional-floor native arithmetic error is added."
        ),
        "fresh_tail_sensitivity_rows": 1024,
        "tail_interval_CDF_grid_reruns": 0,
        "central_divisor64_check": (
            "Derive monotone Bnative raw upper from frozen central rupper/rawB; "
            "check<2^64 and Bnative>=1; no compiled divisor interface adoption."
        ),
        "required_uniform_quantile_error_exact": [TARGET.numerator, TARGET.denominator],
        "fixed_classical_transform_fixture_words": list(FIXTURE_WORDS),
        "fixture_word_records_not_used_as_all_input_completeness": True,
        "accepted_sqrt_semantics_reference": {
            "metadata_path": relative(SQRT_METADATA),
            "metadata_sha256": digest(SQRT_METADATA),
            "active_input_bits": 46,
            "arithmetic": "isqrt(unsigned(argument)<<40)",
            "new_same_SSA_dispatch_or_gate_validation": False,
        },
        "process_CPU_limit_seconds": 120,
        "terminal_verification_and_bulk_output_hashing_within_CPU_budget": True,
        "adaptive_precision_domain_partition_or_retry": False,
        "acceptance": (
            "The single constant proof and fresh sensitivity ledger cover all q32 words "
            "mathematically and meet1e-8 with accepted central certificate, or preserve "
            "failed/censored result. Actual coherent leaf/division/cleanup/source and "
            "native financial-path/G2/cost obligations remain separate and open."
        ),
        "new_quantum_gates_or_compiled_leaves": 0,
        "new_original_financial_price_observations": 0,
        "accepted_Box_Muller_baseline_changed": False,
        "coherent_loader_implemented_or_adopted": False,
        "actual_quantum_gate_cost": None,
        "native_financial_path_arithmetic_certified": False,
        "full_G2_closed": False,
        "preexisting_Stage_C_jobs_edited": False,
        "frozen_inputs": frozen,
        "python": sys.version,
        "executable": sys.executable,
    }
    save(output / "protocol.json", protocol)
    verify(protocol)
    print("One960-combination native transform/sensitivity proof prospectively frozen", flush=True)


def run(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM.resolve())
    if (output / "summary.json").exists():
        raise FileExistsError("Native-transform receipt already completed")
    protocol = read(output / "protocol.json")
    started = time.process_time()
    try:
        run_transform(output, protocol, started)
    except BaseException as failure:
        if not (output / "summary.json").exists():
            save(
                output / "failure.json",
                {
                    "failure_type": type(failure).__name__,
                    "terminal_failure": traceback.format_exc(),
                    "partial_files_preserved": True,
                },
            )
            save(
                output / "summary.json",
                {
                    "passed": False,
                    "native_transform_certificate_succeeded": False,
                    "budget_censored": isinstance(failure, TimeoutError),
                    "terminal_failure": traceback.format_exc(),
                    "new_original_financial_prices_or_gates": 0,
                    "mathematical_partial_certificate_is_not_an_adopted_receipt": True,
                },
            )
            finish_manifest(output, protocol)
        raise


def run_transform(output, protocol, started):
    verify(protocol)
    rc = pytest.main(
        [
            str(
                ROOT / "research/limitation_program_20261001/test_quantile_transform_certificate.py"
            ),
            "-q",
            "-p",
            "no:cacheprovider",
            "--junitxml=" + str(output / "tests.xml"),
        ]
    )
    if rc:
        raise AssertionError("Frozen native-transform fixtures failed, rc=" + str(int(rc)))
    verify(protocol)
    reconciliation = verify_unique_testcases(output / "tests.xml")
    save(output / "test_credit_reconciliation.json", reconciliation)
    remaining = protocol["process_CPU_limit_seconds"] - (time.process_time() - started)
    if remaining <= 0:
        raise TimeoutError("Fixed120CPU native-transform budget after fixtures")
    result = certify(remaining)
    rows = result.pop("fresh_tail_rows")
    save(
        output / "fresh_tail_sensitivity.json",
        {"fixed_rows": 1024, "completed_rows": len(rows), "rows": rows},
    )
    if result["budget_censored"]:
        save(output / "native_transform_certificate.json", result)
        raise TimeoutError("Fixed120CPU native-transform proof censored")
    fixtures_started = time.process_time()
    table, ln2, _ = source_inputs()
    fixtures = [
        {"q32_raw": raw, **mathematical_transform_word(raw, table, ln2)} for raw in FIXTURE_WORDS
    ]
    save(
        output / "classical_transform_fixtures.json",
        {
            "fixtures": fixtures,
            "all_input_proof_basis": False,
            "classical_integer_solver_CPU_seconds": time.process_time() - fixtures_started,
            "actual_quantum_gate_cost": None,
        },
    )
    elapsed_after_fixtures = time.process_time() - started
    if elapsed_after_fixtures > protocol["process_CPU_limit_seconds"]:
        result["certified"] = False
        result["budget_censored"] = True
        result["reason"] = "fixed_CPU_limit_including_fixture_records"
    result["total_budget_checkpoint_after_fixture_generation_CPU_seconds"] = elapsed_after_fixtures
    save(output / "native_transform_certificate.json", result)
    tests = reconciliation["unique_actual_testcases"]
    verify(protocol)
    files = receipt_files(output)
    elapsed = time.process_time() - started
    if elapsed > protocol["process_CPU_limit_seconds"]:
        raise TimeoutError("Fixed120CPU including terminal verification and output hashing")
    save(
        output / "summary.json",
        {
            "passed": result["certified"] and not result["budget_censored"],
            "local_only": True,
            "fixtures_passed": tests,
            "native_transform_certificate_succeeded": result["certified"],
            "budget_censored": result["budget_censored"],
            "failure_reason": result["reason"],
            "log_table_cells": 32,
            "exponent_classes": 30,
            "table_exponent_combinations": 960,
            "fresh_tail_sensitivity_rows_completed": len(rows),
            "native_transform_error_upper_exact": result["transform"][
                "native_transform_error_upper_exact"
            ],
            "actual_native_tail_quantile_error_upper_exact": result.get(
                "actual_native_tail_quantile_error_upper_exact"
            ),
            "combined_mathematical_native_quantile_error_upper_exact": result.get(
                "combined_mathematical_native_quantile_error_upper_exact"
            ),
            "previous_conditional_floor_arithmetic_double_counted": False,
            "actual_coherent_leaf_or_quantum_gate_cost": None,
            "coherent_loader_implemented_or_adopted": False,
            "native_financial_path_arithmetic_certified": False,
            "accepted_Box_Muller_baseline_changed": False,
            "new_original_financial_prices_or_gates": 0,
            "full_G2_closed": False,
            "quantum_advantage_established": False,
            "elapsed_process_CPU_seconds": elapsed,
            "terminal_CPU_includes_tests_proof_fixtures_verification_and_output_hashing": True,
        },
    )
    finish_manifest(output, protocol, files)
    print(
        "Native transform mathematical proof completed; certified=" + str(result["certified"]),
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    (prepare if args.mode == "prepare" else run)(args.output)
