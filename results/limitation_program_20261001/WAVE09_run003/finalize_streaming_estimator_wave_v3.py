"""Freeze evidence and keep strict-live versus archived integrity separate."""

import argparse
from datetime import datetime, timezone
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET

from research.limitation_program_20261001.constant_library import digest
from research.limitation_program_20261001.experiment_checkpoint import (
    PROGRAM,
    manifest,
    read,
    relative,
    save,
    verify,
)
from research.limitation_program_20261001.finalize_streaming_estimator_wave_v2 import (
    RECEIPTS as PREVIOUS_RECEIPTS,
    TEST_RECEIPTS as PREVIOUS_TEST_RECEIPTS,
)
from research.limitation_program_20261001.progress import ROOT
from research.limitation_program_20261001.validate_receipts_v3 import validate


ADDITIONAL_RECEIPTS = (
    "WAVE09_run001",
    "WAVE09_run002",
    "F02_ledger_run001",
    "E04_controller_run001",
    "E04_controller_audit_run001",
    "C06_quantile_rounding_run001",
    "C06_quantile_rounding_audit_run001",
    "A02_quantile_census_run001",
    "A02_quantile_central_run001",
    "A02_quantile_central_run002",
    "A02_quantile_central_audit_run001",
    "E24_grid_run001",
    "E21_conversion_run001",
    "E07_allocation_audit_run001",
    "E07_allocation_audit_run002",
    "A01_drift_run001",
    "A01_validator_run001",
    "E22_census_run001",
    "E22_census_run002",
    "E22_census_audit_run001",
    "C04_frontier_run001",
    "C04_frontier_run002",
    "C04_frontier_audit_run001",
    "H05_supply_run001",
    "H05_supply_audit_run001",
    "A05_loading_run001",
    "A05_loading_audit_run001",
    "A17_A12_census_run001",
)
ADDITIONAL_TEST_RECEIPTS = (
    "E04_controller_run001",
    "C06_quantile_rounding_run001",
    "E21_conversion_run001",
    "A01_drift_run001",
    "A01_validator_run001",
    "A02_quantile_central_run002",
    "H05_supply_run001",
    "A05_loading_run001",
)


def run(output):
    output.relative_to(PROGRAM.resolve())
    assert not output.exists()
    included = (*PREVIOUS_RECEIPTS, *ADDITIONAL_RECEIPTS)
    test_receipts = (*PREVIOUS_TEST_RECEIPTS, *ADDITIONAL_TEST_RECEIPTS)
    assert len(included) == len(set(included))
    summaries, frozen = {}, {}
    for name in included:
        directory = PROGRAM / name
        records = [
            directory / candidate
            for candidate in ("completion_outcome.json", "summary.json", "failed_tests.json")
        ]
        record = next(path for path in records if path.is_file())
        summaries[name] = read(record)
        for path in (directory / "manifest.json", record):
            frozen[relative(path)] = digest(path)
    previous = read(PROGRAM / "WAVE08_run001/summary.json")
    old_manifest = PROGRAM / "WAVE08_run001/manifest.json"
    frozen[relative(old_manifest)] = digest(old_manifest)
    progress = read(PROGRAM / "progress.json")
    assert len(progress["entries"]) == 110
    assert progress["accepted_baseline"] == relative(PROGRAM / "A10_coefficient_run001")
    own = Path(__file__).resolve()
    code = [
        own,
        *(
            ROOT / "research/limitation_program_20261001" / name
            for name in (
                "validate_receipts_v3.py",
                "finalize_streaming_estimator_wave_v2.py",
                "constant_library.py",
                "experiment_checkpoint.py",
                "progress.py",
            )
        ),
    ]
    frozen.update({relative(path): digest(path) for path in code})
    output.mkdir()
    for path in code:
        shutil.copy2(path, output / path.name)
    protocol = dict(
        created_utc=datetime.now(timezone.utc).isoformat(),
        local_only=True,
        before_credit_reconciliation_and_full_integrity_scan=True,
        frozen_inputs=frozen,
        included_receipts=list(included),
        selected_final_test_receipts=list(test_receipts),
        historical_base="WAVE08_run001",
        strict_live_failures_are_never_waived=True,
        separate_archived_integrity_can_pass_only_with_byte_exact_evidence=True,
        no_additional_financial_prices_or_replays=True,
        completed_packet_does_not_complete_overall_goal=True,
    )
    save(output / "protocol.json", protocol)
    verify(protocol)
    names, credits = set(), {}
    for receipt_name in test_receipts:
        assert summaries[receipt_name]["passed"]
        choices = list((PROGRAM / receipt_name).glob("*.xml"))
        assert len(choices) == 1
        document = ET.parse(choices[0]).getroot()
        suites = [document] if document.tag == "testsuite" else document.findall("testsuite")
        assert all(
            int(suite.get(field, 0)) == 0
            for suite in suites
            for field in ("failures", "errors", "skipped")
        )
        tests = {
            (case.get("classname"), case.get("name"))
            for suite in suites
            for case in suite.findall("testcase")
        }
        assert len(tests) == sum(int(suite.get("tests", 0)) for suite in suites)
        assert not names.intersection(tests)
        names.update(tests)
        credits[receipt_name] = dict(
            count=len(tests), junit=relative(choices[0]), cases=sorted(tests)
        )
    assert sum(credits[name]["count"] for name in PREVIOUS_TEST_RECEIPTS) == 424
    save(output / "test_case_credit.json", credits)
    failed = {name: summary for name, summary in summaries.items() if not summary["passed"]}
    save(output / "preserved_failed_attempts.json", failed)
    save(
        output / "method_outcomes.json",
        dict(
            central_first_proof=summaries["A02_quantile_central_run001"],
            central_second_proof=summaries["A02_quantile_central_run002"],
            component_fixture_pass_does_not_imply_scientific_target_pass=True,
            failed_uniform_full_path_composition=summaries["C07_composition_screen_run001"],
        ),
    )
    save(output / "progress_at_wave_freeze.json", progress)
    documents = output / "documents"
    documents.mkdir()
    for path in (ROOT / "docs/limitation_program_20261001").glob("*.md"):
        shutil.copy2(path, documents / path.name)
    # The provisional manifest binds this packet's existing artifacts during
    # the full scan; the final manifest additionally binds its scan and result.
    manifest(output, protocol)
    validation = validate(
        PROGRAM,
        PROGRAM / "A01_drift_run001/reconciliation.json",
        emit=False,
        raise_on_failure=False,
    )
    save(output / "validation.json", validation)
    archived_passed = validation["archived_or_current_integrity_passed"]
    summary = dict(
        passed=archived_passed,
        local_only=True,
        created_utc=datetime.now(timezone.utc).isoformat(),
        result_scope="Packet reconciliation plus separate archived-or-current file integrity",
        global_live_integrity=validation["global_live_integrity"],
        archived_or_current_integrity_passed=archived_passed,
        live_mismatch_references=len(validation["mismatches"]),
        distinct_live_mismatch_paths=len({row["path"] for row in validation["mismatches"]}),
        legitimate_expected_hashes_waived=False,
        validated_manifest_count=validation["manifest_count"],
        validated_distinct_files=validation["distinct_hashed_files"],
        included_receipts=list(included),
        completed_wave_does_not_complete_overall_goal=True,
        preferred_latency_source=progress["accepted_baseline"],
        preferred_latency_source_unchanged=True,
        new_distinct_pytest_cases=len(names),
        total_distinct_pytest_cases=previous["total_distinct_pytest_cases"] + len(names),
        new_complete_financial_clean_XOR_replays=0,
        total_financial_gate_replays=previous["total_financial_gate_replays"],
        new_B2_streaming_harness_gate_replays=6,
        new_financial_source_phase_marking_gate_replays=6,
        historical_extracted_subgraph_replays=3,
        tiny_complete_controlled_G_unitary_cases_verified=3,
        huge_financial_QPE_statevector_or_price_observations=0,
        failed_attempts_preserved=list(failed),
        different_quantile_sampler_adopted=False,
        full_physical_mapping_or_execution_fidelity_certified=False,
        original_continuous_financial_price_certified=False,
        quantum_advantage_established=False,
        G2_to_G5="open",
        work_continuing=progress["active_items"],
        next_action=progress["next_action"],
    )
    save(output / "summary.json", summary)
    manifest(output, protocol)
    if not archived_passed:
        raise AssertionError("Full scan has unverified archival/current expectations")
    print(
        "Local wave retained:",
        len(names),
        "new tests; strict live integrity",
        validation["global_live_integrity"],
        "; separately verified archival integrity",
        archived_passed,
        "; queue continues",
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output.resolve())
