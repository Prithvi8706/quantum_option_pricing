"""Freeze a completed local wave while the broader limitation queue continues."""

import argparse
import contextlib
from datetime import datetime, timezone
import io
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET

from research.limitation_program_20261001.constant_library import digest
from research.limitation_program_20261001.experiment_checkpoint import (
    PROGRAM,
    read,
    relative,
    save,
)
from research.limitation_program_20261001.progress import ROOT
from research.limitation_program_20261001.validate_receipts_v2 import validate


RECEIPTS = (
    "A19_reference_run001",
    "A19_run001",
    "A19_run002",
    "A19_audit_run001",
    "E03_support_run001",
    "E03_support_audit_run001",
    "E03_support_audit_run002",
    "E02_archive_run001",
    "E02_archive_run002",
    "E02_archive_run003",
    "E07_schedule_run001",
    "E02_financial_run001",
    "E02_financial_run002",
    "E02_financial_audit_run001",
    "E02_IQFT_run001",
    "E02_IQFT_audit_run001",
    "E07_complete_run001",
    "C06_pair_run001",
    "C06_pair_audit_run001",
    "C07_barrier_run001",
    "C07_barrier_run002",
    "C07_barrier_audit_run001",
    "C07_bound_date1_run001",
    "C07_composition_screen_run001",
    "C07_composition_audit_run001",
    "C06_quantile_grid_run001",
    "C06_quantile_grid_audit_run001",
    "H17_demand_run001",
    "H17_demand_run002",
    "H17_demand_audit_run001",
    "C09_audit_run001",
    "E04_theorem_run001",
)
TEST_RECEIPTS = (
    "A19_reference_run001",
    "A19_run002",
    "E03_support_run001",
    "E02_archive_run003",
    "E07_schedule_run001",
    "E02_financial_run002",
    "E02_IQFT_run001",
    "C06_pair_run001",
    "C07_barrier_run002",
    "C07_barrier_audit_run001",
    "C07_bound_date1_run001",
    "C07_composition_screen_run001",
    "C07_composition_audit_run001",
    "C06_quantile_grid_run001",
    "C06_quantile_grid_audit_run001",
    "H17_demand_run002",
    "E04_theorem_run001",
)


def run(output):
    output.relative_to(PROGRAM.resolve())
    assert not output.exists()
    previous = read(PROGRAM / "WAVE08_run001/summary.json")
    progress = read(PROGRAM / "progress.json")
    assert len(progress["entries"]) == 110
    assert (
        progress["accepted_baseline"]
        == "results/limitation_program_20261001/A10_coefficient_run001"
    )
    output.mkdir()
    frozen = {}
    summaries = {}
    for name in RECEIPTS:
        directory = PROGRAM / name
        record = directory / "summary.json"
        if not record.exists():
            record = directory / "failed_tests.json"
        summaries[name] = read(record)
        path = directory / "manifest.json"
        frozen[relative(path)] = digest(path)
    old_manifest = PROGRAM / "WAVE08_run001/manifest.json"
    frozen[relative(old_manifest)] = digest(old_manifest)
    for name in ("finalize_streaming_estimator_wave_v2.py", "validate_receipts_v2.py"):
        path = ROOT / "research/limitation_program_20261001" / name
        frozen[relative(path)] = digest(path)
        shutil.copy2(path, output / name)
    credits, tests = {}, set()
    for name in TEST_RECEIPTS:
        assert summaries[name]["passed"]
        choices = list((PROGRAM / name).glob("*xml"))
        assert len(choices) == 1
        document = ET.parse(choices[0]).getroot()
        suites = [document] if document.tag == "testsuite" else document.findall("testsuite")
        assert all(int(s.get(f, 0)) == 0 for s in suites for f in ("failures", "errors", "skipped"))
        names = {(c.get("classname"), c.get("name")) for s in suites for c in s.findall("testcase")}
        assert len(names) == sum(int(s.get("tests", 0)) for s in suites)
        assert not tests.intersection(names)
        tests.update(names)
        credits[name] = dict(count=len(names), junit=relative(choices[0]), cases=sorted(names))
    assert len(tests) == 424
    assert summaries["A19_run002"]["new_harness_gate_replays"] == 6
    assert summaries["E02_financial_run002"]["new_source_marking_gate_replays"] == 6
    assert summaries["E02_financial_run002"]["new_complete_clean_XOR_financial_replays"] == 0
    assert not summaries["C07_composition_screen_run001"]["optimistic_uniform_composition_can_fit"]
    assert summaries["H17_demand_audit_run001"]["passed"]
    assert summaries["C06_quantile_grid_audit_run001"]["passed"]
    failed = {name: r for name, r in summaries.items() if not r["passed"]}
    save(output / "preserved_failed_attempts.json", failed)
    save(output / "test_case_credit.json", credits)
    save(output / "progress_at_wave_freeze.json", progress)
    documents = output / "documents"
    documents.mkdir()
    for name in (
        "README.md",
        "STATUS.md",
        "STREAMING_RESULTS.md",
        "ESTIMATOR_PROGRESS.md",
        "FINANCIAL_LAW_RESULTS.md",
        "HARDWARE_DEMAND_RESULTS.md",
        "CLASSICAL_EVIDENCE_RESULTS.md",
    ):
        shutil.copy2(ROOT / "docs/limitation_program_20261001" / name, documents / name)
    save(
        output / "summary.json",
        dict(
            passed=True,
            local_only=True,
            created_utc=datetime.now(timezone.utc).isoformat(),
            included_receipts=list(RECEIPTS),
            completed_wave_does_not_complete_overall_goal=True,
            preferred_latency_source=progress["accepted_baseline"],
            preferred_latency_source_unchanged=True,
            new_distinct_pytest_cases=len(tests),
            total_distinct_pytest_cases=previous["total_distinct_pytest_cases"] + len(tests),
            new_complete_financial_clean_XOR_replays=0,
            total_financial_gate_replays=previous["total_financial_gate_replays"],
            new_B2_streaming_harness_gate_replays=6,
            new_financial_source_phase_marking_gate_replays=6,
            historical_extracted_subgraph_replays=3,
            tiny_complete_controlled_G_unitary_cases_verified=3,
            huge_financial_QPE_statevector_or_price_observations=0,
            failed_attempts_preserved=list(failed),
            interrupted_v1_completed_test_credit=0,
            favorable_first_date_component_retained=True,
            fixed_uniform_full_path_composition_method_rejected=True,
            different_ideal_quantile_grid_law_certified=True,
            different_quantile_sampler_adopted=False,
            full_physical_mapping_or_execution_fidelity_certified=False,
            original_continuous_financial_price_certified=False,
            quantum_advantage_established=False,
            G2_to_G5="open",
            work_continuing=progress["active_items"],
            next_action=progress["next_action"],
        ),
    )
    assert all(digest(ROOT / name) == value for name, value in frozen.items())
    save(
        output / "manifest.json",
        dict(
            files={relative(p): digest(p) for p in output.rglob("*") if p.is_file()},
            frozen_inputs=frozen,
        ),
    )
    with contextlib.redirect_stdout(io.StringIO()):
        validation = validate(PROGRAM)
    assert validation["passed"]
    save(output / "validation.json", validation)
    print(
        "Local wave frozen:424new tests;6streaming+6phase-marking replays;",
        validation["manifest_count"],
        "manifests;0hash mismatches; queue continues",
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output.resolve())
