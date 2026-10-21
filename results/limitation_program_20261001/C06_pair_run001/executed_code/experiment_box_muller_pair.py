"""Freeze one joint-pair coupling with two cutoffs, then certify one B4 date."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

from research.limitation_program_20261001 import box_muller_pair_certificate as certificate


ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
RESULTS = ROOT / "results/limitation_program_20261001"
DECLARED_TESTS = 26


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def create(path, value):
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def upper_display(value):
    return math.nextafter(float(certificate.decoded(value)), math.inf)


def run(directory):
    directory = directory.resolve()
    if not directory.is_relative_to(ROOT):
        raise ValueError("Local workspace receipt required")
    directory.mkdir(parents=True, exist_ok=False)
    executed = directory / "executed_code"
    executed.mkdir()
    code = [
        Path(__file__).resolve(),
        RESEARCH / "box_muller_pair_certificate.py",
        RESEARCH / "test_box_muller_pair_certificate.py",
    ]
    inputs = [
        RESEARCH / "baseline.py",
        ROOT / "research/controlled_source_completion/finance.py",
        ROOT / "research/controlled_source_completion/ir.py",
        ROOT / "research/advantage_frontier_20260923/barrier_oracle_depth.py",
        ROOT / "docs/limitation_audit_20261001/implementation_plan/CONTRACT.md",
        RESULTS / "E07_schedule_run001/complete_price_ledger.json",
        RESULTS / "E07_schedule_run001/summary.json",
    ]
    for case in certificate.CASES:
        inputs += [
            ROOT / certificate.SOURCE_BASE / case / "min-depth" / file
            for file in ("target.json", "source.json", "schedule_capped.json")
        ]
        inputs += [
            RESULTS / "E03_support_run001" / f"{case}_certificate.json",
            RESULTS / "E03_support_audit_run002" / f"{case}_audit.json",
        ]
    for run_name in ("E03_support_run001", "E03_support_audit_run002"):
        inputs += [RESULTS / run_name / "manifest.json", RESULTS / run_name / "summary.json"]
    dependencies = sorted(set(code + inputs))
    frozen = {path.relative_to(ROOT).as_posix(): sha(path) for path in dependencies}
    price_summary = certificate.read(RESULTS / "E07_schedule_run001/summary.json")
    if price_summary["complete_price_assessment"]["remaining_dollar_headroom"] != [11, 2000]:
        raise ValueError("Frozen complete-price headroom changed")
    snapshots = []
    for path in code:
        target = executed / path.name
        target.write_bytes(path.read_bytes())
        snapshots.append(
            dict(
                original=path.relative_to(ROOT).as_posix(),
                snapshot=target.relative_to(directory).as_posix(),
                sha256=sha(target),
            )
        )
    create(
        directory / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            item="C06 joint Box-Muller pair and one B4 date",
            local_only=True,
            before_meaningful_tests_and_certification=True,
            executed_dependencies=snapshots,
            declared_tests=DECLARED_TESTS,
            coupling=(
                "U,V independent continuous uniforms; q32 integer cells and exact f40 midpoints; "
                "retain the joint shared-input output pair"
            ),
            cutoff_bits=list(certificate.CUTOFF_BITS),
            cutoff_candidates=2,
            method_families=1,
            interval_decimal_precision=certificate.INTERVAL_DIGITS,
            mpmath_version=certificate.mp.__version__,
            interpreter_sha256=sha(ROOT / ".context/frontier_t0_env/Scripts/python.exe"),
            law_changes=0,
            finite_grid_sample_enumerations=0,
            sampled_variance_estimates=0,
            pair_counts=dict(B4x12=30, B8x52=234),
            scalar_counts=dict(B4x12=60, B8x52=468),
            observation_scope=dict(case="B4x12", date=1, time_exact=[1, 12], used_joint_pairs=3),
            unallocated_dollar_headroom_exact=[11, 2000],
            acceptance=(
                "Each analytic enclosure must hold for the actual literal tables/typed graph. "
                "A valid one-date component is retained even if larger than headroom. "
                "Neither component comparison nor tail union closes full-path G2."
            ),
            proof_terms=[
                "radial and angular midpoint coupling",
                "all actual Taylor coefficients enclosed by mp.iv",
                "table Taylor remainder",
                "every native Horner floor",
                "exact mantissa normalization and integer exponent",
                "ln2 literal",
                "square-root Holder and native floor",
                "native final product floor",
                "actual date1 coefficients/drift/logspot",
                "actual Estrin polynomial/floors/range reconstruction",
                "tail union with independently bound nonnegative payoff support",
            ],
            new_financial_gate_replays=0,
            new_quantum_unitary_tests=0,
            full_path_clipping_and_barrier_composition=(
                "Explicitly unfinished; null dollar/band fields preserved"
            ),
            freeze_rule=(
                "Preserve this first execution even on failure; "
                "code changes require a new version and receipt"
            ),
        ),
    )
    create(directory / "frozen_inputs.json", frozen)
    xml_path = directory / "pytest.xml"
    completed = subprocess.run(
        [
            str(ROOT / ".context/frontier_t0_env/Scripts/python.exe"),
            "-m",
            "pytest",
            "-q",
            str(RESEARCH / "test_box_muller_pair_certificate.py"),
            f"--junitxml={xml_path}",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    (directory / "pytest_stdout.txt").write_text(completed.stdout, encoding="utf-8")
    (directory / "pytest_stderr.txt").write_text(completed.stderr, encoding="utf-8")
    suites = list(ET.parse(xml_path).getroot().iter("testsuite"))
    tests = {
        field: sum(int(suite.attrib.get(field, 0)) for suite in suites)
        for field in ("tests", "failures", "errors", "skipped")
    }
    result, error = None, None
    try:
        result = certificate.certify(ROOT)
        create(directory / "certificate.json", result)
    except Exception as exception:
        error = dict(type=type(exception).__name__, message=str(exception))
        create(directory / "certificate_error.json", error)
    unchanged = all(sha(ROOT / relative) == expected for relative, expected in frozen.items())
    passed = (
        completed.returncode == 0
        and tests["tests"] == DECLARED_TESTS
        and not any(tests[key] for key in ("failures", "errors", "skipped"))
        and result is not None
        and unchanged
    )
    candidates = []
    if result:
        for candidate in result["candidates"]:
            date = candidate["B4_date1"]
            candidates.append(
                dict(
                    cutoff_bits=candidate["cutoff_bits"],
                    coordinate_discrepancy_display_upper=upper_display(
                        candidate["coordinate_discrepancy_upper_exact"]
                    ),
                    date1_log_discrepancy_display_upper=upper_display(
                        date["log_discrepancy_exact"]
                    ),
                    date1_stock_discrepancy_display_upper_dollars=upper_display(
                        date["spot_discrepancy_dollars_exact"]
                    ),
                    date1_basket_discrepancy_display_upper_dollars=upper_display(
                        date["basket_discrepancy_dollars_exact"]
                    ),
                    date1_component_below_headroom=date[
                        "one_date_component_below_unallocated_headroom"
                    ],
                    B4_full_bad_pair_tail_display_upper_dollars=upper_display(
                        candidate["tail_payoff_difference_dollars_upper_exact"][
                            "B4_all30_pairs_bad_event_only"
                        ]
                    ),
                )
            )
    create(
        directory / "summary.json",
        dict(
            passed=passed,
            tests=tests,
            returncode=completed.returncode,
            certificate_error=error,
            frozen_inputs_unchanged=unchanged,
            local_only=True,
            candidates=candidates,
            display_floats_rounded_upward=True,
            exact_bounds_in="certificate.json",
            new_financial_gate_replays=0,
            new_quantum_unitary_tests=0,
            full_G2_closed=False,
            complete_price_certified=False,
            remaining=[
                "full-path stock and clipping discrepancy",
                "barrier boundary mass",
                "full smooth payoff discrepancy and date composition",
            ],
        ),
    )
    files = {
        path.relative_to(ROOT).as_posix(): sha(path)
        for path in sorted(directory.rglob("*"))
        if path.is_file()
    }
    create(
        directory / "manifest.json",
        dict(
            files=files,
            frozen_inputs=frozen,
            manifest_self_hash_excluded=True,
            historical_receipts_unchanged=unchanged,
        ),
    )
    print(
        json.dumps(
            dict(passed=passed, tests=tests, certificate_error=error, candidates=candidates),
            indent=2,
        )
    )
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=RESULTS / "C06_pair_run001")
    run(parser.parse_args().output)
