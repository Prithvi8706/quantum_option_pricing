"""Freeze one two-contract, actual-source-bound native AS241 price-bias proof.

Only saved SSA is inspected. No builder/frontend regeneration, finance sample,
gate array, new sampler setting or numerical proof runs during preparation.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import time
import traceback
import xml.etree.ElementTree as ET

os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["NUMBA_NUM_THREADS"] = "1"

import mpmath as mp  # noqa: E402
import pytest  # noqa: E402

from research.limitation_program_20261001.as241_financial_certificate import (  # noqa: E402
    ALLOWANCE,
    CPU_LIMIT,
    DIGITS,
    EXPONENTS,
    BudgetCensoredError,
    certify_case,
    check_cpu,
    true_midpoint_quantile_bracket,
)
from research.limitation_program_20261001.as241_financial_native import (  # noqa: E402
    CASES,
    LAW,
    canonical_hash,
    extract_financial,
    pair,
    require,
    validate_ledger,
    validate_normalization,
    validate_scalar_invocations,
)
from research.limitation_program_20261001.audit_quantile_grid import (  # noqa: E402
    audit_builder_contract,
    audit_task,
    independent_model,
)
from research.limitation_program_20261001.quantile_as241_law_certificate import (  # noqa: E402
    validate_native_error,
)

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
FRONTEND = PROGRAM / "A02_quantile_financial_target_run001"
SCALAR = PROGRAM / "A02_quantile_scalar_run001"
TRANSFORM = PROGRAM / "A02_quantile_transform_run002"
CODE = (
    "as241_financial_native.py",
    "as241_financial_certificate.py",
    "test_as241_financial_certificate.py",
    "experiment_as241_financial.py",
)
RECEIPTS = (
    "A02_quantile_financial_target_run001",
    "A02_quantile_scalar_run001",
    "A02_quantile_scalar_audit_run001",
    "A02_quantile_transform_run002",
    "A02_quantile_transform_audit_run001",
    "A02_quantile_law_run001",
    "A02_quantile_law_audit_run001",
    "C06_quantile_grid_audit_run001",
    "C06_pair_run001",
    "C06_pair_audit_run001",
    "E03_support_run001",
    "E03_support_audit_run002",
)
DEPENDENCIES = (
    "audit_quantile_grid.py",
    "quantile_as241_law_certificate.py",
    "AS241_FINANCIAL_BIAS_PREFLIGHT.md",
)
DECLARED_TESTS = 21
WALL_LIMIT = 600


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def relative(path):
    return Path(path).resolve().relative_to(ROOT.resolve()).as_posix()


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def verify(frozen):
    for name, sha in frozen.items():
        require(
            isinstance(name, str) and isinstance(sha, str) and len(sha) == 64,
            "Explicit SHA256 artifact mapping",
        )
        path = (ROOT / name.replace("\\", "/")).resolve()
        path.relative_to(ROOT.resolve())
        require(digest(path) == sha, "Frozen financial proof input changed: " + name)


def bind_frozen(frozen, name, sha):
    require(isinstance(name, (str, Path)), "Explicit frozen dependency path")
    require(
        isinstance(sha, str) and len(sha) == 64 and all(char in "0123456789abcdef" for char in sha),
        "Explicit canonical SHA256 expectation",
    )
    path = (ROOT / str(name).replace("\\", "/")).resolve()
    path.relative_to(ROOT.resolve())
    normalized = relative(path)
    require(
        normalized not in frozen or frozen[normalized] == sha,
        "Existing frozen SHA expectation may not be replaced: " + normalized,
    )
    frozen[normalized] = sha


def add_receipt(frozen, directory):
    summary = read(directory / "summary.json")
    require(summary.get("passed") is True, "Successful prerequisite: " + directory.name)
    require(summary.get("budget_censored", False) is False, "Uncensored financial premise required")
    record = read(directory / "manifest.json")
    allowed = {"files", "frozen_inputs", "manifest_self_hash_excluded"}
    if "historical_receipts_unchanged" in record:
        require(
            directory.name == "C06_pair_run001"
            and record["historical_receipts_unchanged"] is True,
            "Only demonstrated C06_pair historical receipt marker may be true",
        )
        allowed.add("historical_receipts_unchanged")
    require(
        {"files", "frozen_inputs"}.issubset(record) and set(record).issubset(allowed),
        "Explicit structured financial prerequisite manifest",
    )
    require(record.get("manifest_self_hash_excluded", True) is True, "Exact self-exclusion marker")
    for field in ("files", "frozen_inputs"):
        for path, sha in record[field].items():
            bind_frozen(frozen, path, sha)
    bind_frozen(frozen, directory / "manifest.json", digest(directory / "manifest.json"))


def bind_case(case, scalar):
    """Inventory all saved producer IDs and literals; evaluate no financial math."""
    directory = FRONTEND / case
    target, bundle, ledger = [
        read(directory / name)
        for name in ("target.json", "bundle.json", "new_source_matched_ledger.json")
    ]
    require(
        bundle.get("schema") == "as241-financial-target-bundle-v1" and bundle["case"] == case,
        "Actual frontend bundle schema/case",
    )
    scalar_record = validate_scalar_invocations(target, bundle, scalar)
    ns = bundle["normal_source"]
    require(
        ns["scalar_receipt"] == relative(SCALAR)
        and ns["scalar_actual_source"] == relative(SCALAR / "candidate64/source.json"),
        "Actual scalar receipt/source path binding",
    )
    for field, name in (
        ("scalar_target_file_sha256", "scalar_target.json"),
        ("scalar_bindings_file_sha256", "semantic_bindings.json"),
        ("scalar_proofs_file_sha256", "new_site_proofs.json"),
        ("scalar_actual_source_file_sha256", "candidate64/source.json"),
    ):
        require(ns[field] == digest(SCALAR / name), "Actual scalar proof/source file binding")
    normalized = bundle["financial_normalization"]
    archive_path = ROOT / normalized["accepted_target"].replace("\\", "/")
    source_path = ROOT / normalized["accepted_source"].replace("\\", "/")
    require(
        digest(archive_path) == normalized["accepted_target_sha256"], "Accepted actual target bytes"
    )
    require(
        digest(source_path) == normalized["accepted_source_sha256"], "Accepted actual source bytes"
    )
    archive = read(archive_path)
    pair_binding = read(PROGRAM / "C06_pair_run001/certificate.json")["source_bindings"][case]
    require(
        pair_binding["target_sha256"] == digest(archive_path)
        and pair_binding["normal_values"] == normalized["original_boundary_values"],
        "Audited archived common/idiosyncratic normal roles",
    )
    normalization = validate_normalization(target, bundle, archive, pair_binding["normal_values"])
    require(
        ledger == bundle["new_source_matched_ledger"],
        "Separate actual new price ledger equals source bundle",
    )
    validate_ledger(ledger, canonical_hash(target))
    scope = extract_financial(target, bundle)
    require(len(scope["sites"]) == CASES[case][0] * CASES[case][1], "Every stock exponential site")
    return (
        target,
        scope,
        normalization["financial_values"],
        {
            "case": case,
            "actual_new_target_sha256": canonical_hash(target),
            "actual_new_target_file_sha256": digest(directory / "target.json"),
            "actual_bundle_file_sha256": digest(directory / "bundle.json"),
            "actual_new_ledger_file_sha256": digest(directory / "new_source_matched_ledger.json"),
            "normalized_financial_closure_sha256": normalization["normalized_closure_sha256"],
            "all_stock_exp_sites": len(scope["sites"]),
            "all_financial_values": len(normalization["financial_values"]),
            "scalar_binding": scalar_record,
            "literal_scope": scope,
            "old_Box_Muller_law_or_old_E02_costs_transferred": False,
        },
    )


def prepare(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM.resolve())
    if output.exists():
        raise FileExistsError("Fresh prospective native AS241 financial receipt required")
    frozen = {}
    try:
        prepare_body(output, frozen)
    except BaseException as failure:
        if output.exists():
            if not (output / "protocol.json").exists():
                save(
                    output / "protocol.json",
                    {
                        "local_only": True,
                        "frozen_inputs": frozen,
                        "terminal_partial_preparation": True,
                        "declared_unique_tests": DECLARED_TESTS,
                    },
                )
            save(
                output / "preparation_failure.json",
                {
                    "failure_type": type(failure).__name__,
                    "message": str(failure),
                    "traceback": traceback.format_exc(),
                    "partial_files_preserved": True,
                    "fixed_receipt_terminal_no_retry": True,
                },
            )
            save(
                output / "summary.json",
                {
                    "passed": False,
                    "preparation_failed": True,
                    "budget_censored": isinstance(failure, (BudgetCensoredError, TimeoutError)),
                    "new_test_credit": 0,
                    "new_unique_fixtures_passed": 0,
                    "partial_files_preserved": True,
                    "fixed_receipt_terminal_no_retry": True,
                    "financial_prices_or_gate_replays": 0,
                    "new_source_matched_native_financial_bias_certificate_adopted": False,
                    "accepted_joint_Box_Muller_obligation_filled": False,
                    "old_E02_source_or_wrapper_costs_transferred": False,
                    "quantum_advantage_established": False,
                },
            )
            finish(output, {"frozen_inputs": frozen})
        raise


def prepare_body(output, frozen):
    for name in RECEIPTS:
        add_receipt(frozen, PROGRAM / name)
    scalar_summary = read(SCALAR / "summary.json")
    require(
        scalar_summary.get("actual_scalar_clean_XOR_source_emitted") is True
        and scalar_summary.get("all_Q32_uniform_law_proof_from_new_site_recipe_not_samples")
        is True,
        "Actual scalar semantic recipe and source receipt prerequisite",
    )
    require(
        read(FRONTEND / "summary.json").get(
            "actual_scalar_producers_and_normalized_original_finance_bound"
        )
        is True,
        "Full actual frontend source binding prerequisite",
    )
    scalar = read(SCALAR / "scalar_target.json")
    inventories = {}
    for case in CASES:
        _, _, _, inventories[case] = bind_case(case, scalar)
    require(
        sum(row["all_stock_exp_sites"] for row in inventories.values()) == 464,
        "Complete464 native financial exponential sites before proof freeze",
    )
    for name in CODE + DEPENDENCIES:
        path = ROOT / "research/limitation_program_20261001" / name
        bind_frozen(frozen, path, digest(path))
    bind_frozen(frozen, Path(sys.executable), digest(Path(sys.executable)))
    builder = ROOT / "research/advantage_frontier_20260923/barrier_oracle_depth.py"
    bind_frozen(frozen, builder, digest(builder))
    for case in CASES:
        task = PROGRAM / "G0_run003" / (case + "_task.json")
        bind_frozen(frozen, task, digest(task))
    # The inherited proof inputs pin mpmath; explicitly add its actual source
    # tree so this new numerical proof cannot depend on unrecorded interval code.
    for path in Path(mp.__file__).parent.rglob("*.py"):
        bind_frozen(frozen, path, digest(path))
    verify(frozen)
    output.mkdir()
    for name in CODE:
        shutil.copy2(ROOT / "research/limitation_program_20261001" / name, output / name)
        require(
            digest(output / name)
            == frozen[relative(ROOT / "research/limitation_program_20261001" / name)],
            "Frozen financial code snapshot differs: " + name,
        )
    verify(frozen)
    protocol = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "local_only": True,
        "before_new_fixtures_or_numerical_financial_proof": True,
        "partial_preparation_failures_are_terminal_and_preserved": True,
        "copied_source_bytes_and_frozen_inputs_reverified_before_protocol": True,
        "cases": list(CASES),
        "new_source_law": LAW,
        "actual_source_inventories": inventories,
        "all_stock_exp_sites": 464,
        "uniform_bits_each": 32,
        "native_word_width": 72,
        "fraction_bits": 40,
        "independent_midpoint_driver_counts": {"B4x12": 60, "B8x52": 468},
        "new_source_matched_epsilon_dollars_exact": [1, 100],
        "new_statistical_allowance_dollars_exact": [9, 2000],
        "new_residual_financial_allowance_dollars_exact": pair(ALLOWANCE),
        "declared_unique_tests": DECLARED_TESTS,
        "previous_fixture_credit_added_again": 0,
        "interval_decimal_digits": DIGITS,
        "fixed_exp_degree": 12,
        "fixed_integer_exp_classes_per_case": list(EXPONENTS),
        "true_all_q32_quantile_bracket_method": (
            "Fixed analytic integrated-exp degree160 CDF at-6.5, exact100-term Machin pi; "
            "symmetry/monotonicity"
        ),
        "band_method": (
            "Unconditional accumulated-common-factor density "
            "plus exact-grid closed-band BV2 transfer"
        ),
        "clamp_method": (
            "Deterministic lower allowance; upper events removed only by paid BOTH-path knockout"
        ),
        "dead_path_arithmetic": (
            "Every actual financial value checked against signed72/product144 limits"
        ),
        "native_support": (
            "Actual integer Asian and discount coefficients; strict alive floor; Y<40"
        ),
        "process_CPU_limit_seconds": CPU_LIMIT,
        "elapsed_wall_limit_seconds": WALL_LIMIT,
        "adaptive_partition_precision_cutoff_or_retry": False,
        "financial_price_observations": 0,
        "financial_gate_replays": 0,
        "new_graph_constructions": 0,
        "new_quantum_leaf_generations_or_dispatch_adoptions": 0,
        "accepted_joint_Box_Muller_obligation_filled": False,
        "old_E02_source_or_wrapper_costs_transferred": False,
        "actual_source_or_wrapper_quantum_cost": None,
        "physical_runtime_or_error": None,
        "complete_estimator_or_financial_sampler_adopted": False,
        "quantum_advantage_established": False,
        "preexisting_Stage_C_jobs_edited": False,
        "frozen_inputs": frozen,
        "python": sys.version,
        "executable": sys.executable,
    }
    save(output / "protocol.json", protocol)
    verify(frozen)
    print("One two-contract native AS241 financial bias method frozen", flush=True)


def test_credit(path):
    records = list(ET.parse(path).getroot().iter("testcase"))
    identities = [(item.attrib.get("classname", ""), item.attrib["name"]) for item in records]
    require(
        len(records) == len(set(identities)) == DECLARED_TESTS, "Exact frozen21 distinct fixtures"
    )
    require(
        not any(
            item.find(tag) is not None
            for item in records
            for tag in ("failure", "error", "skipped")
        ),
        "Failed/error/skipped fixtures receive no success credit",
    )
    return {
        "unique_actual_testcases": DECLARED_TESTS,
        "identities": [list(item) for item in identities],
        "previous_fixture_counts_credited_again": 0,
    }


def receipt_files(output):
    return {
        relative(path): digest(path)
        for path in sorted(output.rglob("*"))
        if path.is_file() and path.name != "manifest.json"
    }


def finish(output, protocol, checked_files=None):
    if checked_files is None:
        checked_files = receipt_files(output)
    else:
        # Source verification and existing receipt hashes were charged before
        # the success budget guard; only the newly written summary remains.
        checked_files[relative(output / "summary.json")] = digest(output / "summary.json")
    save(
        output / "manifest.json",
        {
            "files": checked_files,
            "frozen_inputs": protocol["frozen_inputs"],
            "manifest_self_hash_excluded": True,
        },
    )


def run(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM.resolve())
    if (output / "summary.json").exists():
        raise FileExistsError("Native AS241 financial receipt already terminal")
    protocol = read(output / "protocol.json")
    started, wall = time.process_time(), time.monotonic()
    completed, credit = [], None
    try:
        verify(protocol["frozen_inputs"])
        rc = pytest.main(
            [
                str(
                    ROOT
                    / "research/limitation_program_20261001/test_as241_financial_certificate.py"
                ),
                "-q",
                "-p",
                "no:cacheprovider",
                "--junitxml=" + str(output / "tests.xml"),
            ]
        )
        require(rc == 0, "Frozen native financial proof-contract fixtures failed")
        credit = test_credit(output / "tests.xml")
        save(output / "test_credit_reconciliation.json", credit)
        check_cpu(started)
        mp.iv.dps = DIGITS
        error = validate_native_error(
            read(TRANSFORM / "native_transform_certificate.json"),
            read(TRANSFORM / "fresh_tail_sensitivity.json"),
        )
        save(
            output / "same_input_scalar_error_reconciliation.json",
            {
                "uniform_native_quantile_error_upper_exact": pair(error),
                "log_table_exponent_classes": 960,
                "fresh_tail_sensitivity_rows": 1024,
                "old_conditional_floor_tail_error_added": False,
                "scalar_KS_E_or_previous_exact_floor_grid_ULP_added": False,
            },
        )
        bracket = true_midpoint_quantile_bracket(started)
        save(output / "true_midpoint_quantile_bracket.json", bracket)
        builder = audit_builder_contract()
        scalar = read(SCALAR / "scalar_target.json")
        for case in protocol["cases"]:
            check_cpu(started)
            if time.monotonic() - wall > WALL_LIMIT:
                raise BudgetCensoredError("Fixed600-second elapsed wall limit")
            model = independent_model(case)
            audit_task(read(PROGRAM / "G0_run003" / (case + "_task.json")), case)
            require(
                model["builder_sha256"] == builder["builder_sha256"],
                "Original economic contract binding",
            )
            target, scope, financial_values, inventory = bind_case(case, scalar)
            require(
                inventory == protocol["actual_source_inventories"][case],
                "Frozen complete source inventory changed",
            )
            directory = output / case

            def stage(name, value):
                save(directory / (name + ".json"), value)

            def exponent_class(k, value):
                save(
                    directory / "exponent_classes" / ("class" + str(k + 17).zfill(2) + ".json"),
                    value,
                )

            row = certify_case(
                target, scope, financial_values, error, bracket, started, stage, exponent_class
            )
            row["actual_source_binding"] = inventory
            row["original_ideal_GBM_model"] = model
            save(output / (case + "_certificate.json"), row)
            completed.append(
                {
                    key: row[key]
                    for key in (
                        "case",
                        "new_source_matched_native_financial_bias_certified",
                        "complete_original_contract_bias_upper_exact",
                        "bias_fits_frozen_residual_financial_allowance",
                        "ideal_continuous_to_exact_grid_bias_upper_exact",
                        "already_discounted_smooth_bias_upper_exact",
                        "barrier_switch_bias_upper_exact",
                    )
                }
            )
        verify(protocol["frozen_inputs"])
        checked_files = receipt_files(output)
        check_cpu(started)
        censored = time.monotonic() - wall > WALL_LIMIT
        fit = all(row["bias_fits_frozen_residual_financial_allowance"] for row in completed)
        save(
            output / "summary.json",
            {
                "passed": not censored and fit,
                "new_test_credit": credit["unique_actual_testcases"] if not censored and fit else 0,
                "budget_censored": censored,
                "reason": "fixed_wall_limit"
                if censored
                else None
                if fit
                else "financial_bias_exceeds_frozen_residual",
                "new_unique_fixtures_passed": credit["unique_actual_testcases"],
                "previous_fixture_counts_credited_again": 0,
                "cases": completed,
                "all_two_actual_source_math_bounds_completed": True,
                "both_new_native_financial_bias_bounds_fit_residual": fit,
                "new_source_matched_native_financial_bias_certificate_adopted": False,
                "independent_financial_bias_audit_required": True,
                "financial_prices_or_gate_replays": 0,
                "new_graph_constructions_or_quantum_leaves": 0,
                "accepted_joint_Box_Muller_obligation_filled": False,
                "old_E02_source_or_wrapper_costs_transferred": False,
                "new_source_estimator_cost_or_physical_time": None,
                "complete_estimator_or_sampler_adopted": False,
                "quantum_advantage_established": False,
                "elapsed_process_CPU_seconds": time.process_time() - started,
                "elapsed_wall_seconds": time.monotonic() - wall,
            },
        )
    except BaseException as exc:
        save(
            output / "failure.json",
            {
                "failure_type": type(exc).__name__,
                "message": str(exc),
                "traceback": traceback.format_exc(),
                "budget_censored": isinstance(exc, (BudgetCensoredError, TimeoutError)),
                "new_test_credit": 0,
                "partial_files_preserved": True,
            },
        )
        save(
            output / "summary.json",
            {
                "passed": False,
                "budget_censored": isinstance(exc, (BudgetCensoredError, TimeoutError)),
                "new_test_credit": 0,
                "terminal_failure": traceback.format_exc(),
                "completed_cases": completed,
                "new_unique_fixtures_passed": 0,
                "observed_completed_unique_fixtures_passed": credit["unique_actual_testcases"]
                if credit
                else 0,
                "previous_fixture_counts_credited_again": 0,
                "financial_prices_or_gate_replays": 0,
                "new_source_matched_native_financial_bias_certificate_adopted": False,
                "accepted_joint_Box_Muller_obligation_filled": False,
                "old_E02_source_or_wrapper_costs_transferred": False,
                "new_source_estimator_cost_or_physical_time": None,
                "quantum_advantage_established": False,
                "elapsed_process_CPU_seconds": time.process_time() - started,
                "elapsed_wall_seconds": time.monotonic() - wall,
            },
        )
        finish(output, protocol)
        raise
    finish(output, protocol, checked_files)
    print(
        "Fixed native AS241 financial bound retained; "
        "independent audit and quantum cost remain open",
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    (prepare if args.mode == "prepare" else run)(args.output)
