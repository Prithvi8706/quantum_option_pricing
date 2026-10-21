"""Separate conservative diagnostic of frozen Stage C coverage estimates.

No new prices, paths, timing, or recalibration of the declared Stage C study.
All execution requires root clearance after the live timing supervisor finishes.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
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

import numpy as np  # noqa: E402
import _pytest  # noqa: E402
import pytest  # noqa: E402
import scipy  # noqa: E402
from scipy.stats import t as student_t  # noqa: E402

from research.limitation_program_20261001.conservative_coverage import (  # noqa: E402
    COUNT_FAILURE,
    COUNT_INTERVALS,
    PER_INTERVAL_FAILURE,
    binary64,
    classify,
    clopper_pearson_outward,
    conditional_joint_confidence,
)

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
RESEARCH = ROOT / "research/limitation_program_20261001"
PRIOR = PROGRAM / "C09_stagec_update_run001"
SNAPSHOT = PRIOR / "snapshots/results/frontier_classical_20261001"
CODE = (
    "conservative_coverage.py",
    "test_conservative_coverage.py",
    "experiment_conservative_coverage.py",
    "conservative_coverage_preflight.json",
)
ARMS = (
    ("B4x12", "B4x12_levels10to13.npy", (10, 11, 12, 13)),
    ("B8x52", "B8x52_levels10to13.npy", (10, 11, 12, 13)),
    ("B4x12", "B4x12_level17.npy", (17,)),
)
TESTS = 21
CPU_LIMIT = 120
WALL_LIMIT = 300


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def create(path, value):
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path):
    return path.resolve().relative_to(ROOT).as_posix()


def pair(value):
    return [value.numerator, value.denominator]


def verify(frozen):
    for name, expected in frozen.items():
        path = (ROOT / name).resolve()
        path.relative_to(ROOT)
        if sha(path) != expected:
            raise ValueError("Frozen coverage diagnostic input changed: " + name)


def bind_frozen(frozen, name, expected):
    path = (ROOT / str(name).replace("\\", "/")).resolve()
    path.relative_to(ROOT)
    name = relative(path)
    if name in frozen and frozen[name] != expected:
        raise ValueError("Prior coverage inspection hashes disagree: " + name)
    frozen[name] = expected


def prepare(output):
    output = output.resolve()
    output.relative_to(PROGRAM)
    if output.exists():
        raise FileExistsError("Fresh prospective coverage diagnostic receipt required")
    previous = read(PRIOR / "summary.json")
    if previous.get("passed") is not True or previous.get("budget_censored", False) is not False:
        raise ValueError("Completed Stage C snapshot inspection prerequisite required")
    original = read(PRIOR / "manifest.json")
    frozen = {}

    def bind(name, expected):
        bind_frozen(frozen, name, expected)

    for field in ("files", "frozen_inputs"):
        for name, expected in original[field].items():
            bind(name, expected)
    bind(relative(PRIOR / "manifest.json"), sha(PRIOR / "manifest.json"))
    paths = [RESEARCH / name for name in CODE] + [Path(sys.executable)]
    for module in (np, scipy, pytest, _pytest):
        paths.extend(
            path
            for path in Path(module.__file__).parent.rglob("*")
            if path.is_file() and path.suffix in (".py", ".pyd", ".dll")
        )
    for module in (np, scipy):
        libraries = Path(module.__file__).parent.parent / (module.__name__ + ".libs")
        if libraries.exists():
            paths.extend(path for path in libraries.rglob("*.dll") if path.is_file())
    for path in paths:
        bind(relative(path), sha(path))
    verify(frozen)
    output.mkdir()
    try:
        prepare_files(output, frozen)
    except BaseException as failure:
        create(
            output / "preparation_failure.json",
            {
                "failure_type": type(failure).__name__,
                "message": str(failure),
                "traceback": traceback.format_exc(),
                "partial_files_preserved": True,
                "fixed_receipt_terminal_no_retry": True,
            },
        )
        create(
            output / "summary.json",
            {
                "passed": False,
                "preparation_failed": True,
                "budget_censored": isinstance(failure, TimeoutError),
                "new_test_credit": 0,
                "new_prices_paths_scrambles_timings": 0,
                "fixed_receipt_terminal_no_retry": True,
            },
        )
        finish_manifest(output, {"frozen_inputs": frozen})
        raise


def prepare_files(output, frozen):
    for name in CODE:
        shutil.copy2(RESEARCH / name, output / name)
        if sha(output / name) != frozen[relative(RESEARCH / name)]:
            raise ValueError("Frozen coverage code snapshot differs: " + name)
    verify(frozen)
    create(
        output / "protocol.json",
        {
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "local_only": True,
            "before_tests_classification_or_binomial_probability_evaluations": True,
            "frozen_inputs": frozen,
            "requires_all_stage_c_script_supervisors_and_exclusive_timing_jobs_terminal": True,
            "source_estimates": "Immutable completed C4 snapshots only",
            "original_nominal_confidence_levels": [0.99, 0.95],
            "original_t_degrees_of_freedom": 15,
            "original_scrambles": 16,
            "original_replications_per_cell": 1000,
            "fixed_method_cells": 18,
            "fixed_count_intervals": COUNT_INTERVALS,
            "count_classifications": ["guaranteed", "reference_point", "possible"],
            "count_simultaneous_failure_exact": pair(COUNT_FAILURE),
            "per_two_sided_count_interval_failure_exact": pair(PER_INTERVAL_FAILURE),
            "root_bits": 64,
            "integer_binomial_tail_comparisons": True,
            "counts_use_exact_binary64_rational_interval_geometry": True,
            "original_float_generated_mean_and_t_half_width_preserved": True,
            "analysis_is_separate_posthoc_diagnostic": True,
            "original_Stage_C_outputs_and_stop_rule_changed": False,
            "new_prices_paths_scrambles_or_timings": 0,
            "reference_true_price_99_percent_confidence_is_verified": False,
            "conditional_IID_binomial_model_is_verified": False,
            "true_price_99_percent_delivery_theorem_is_proved": False,
            "declared_unique_tests": TESTS,
            "process_CPU_limit_seconds": CPU_LIMIT,
            "new_work_admission_CPU_seconds": 90,
            "wall_limit_seconds": WALL_LIMIT,
            "python": sys.version,
            "canonical_frozen_hash_insertions_preserve_all_prior_expectations": True,
            "partial_preparation_failure_is_terminal_and_preserved": True,
            "bulk_output_hashing_precedes_terminal_CPU_and_wall_check": True,
        },
    )
    print("Separate exact conservative coverage diagnostic prospectively frozen", flush=True)


def receipt_files(output):
    return {
        relative(path): sha(path)
        for path in sorted(output.rglob("*"))
        if path.is_file() and path.name != "manifest.json"
    }


def finish_manifest(output, protocol, checked_files=None):
    if checked_files is None:
        checked_files = receipt_files(output)
    else:
        checked_files = dict(checked_files)
        checked_files[relative(output / "summary.json")] = sha(output / "summary.json")
    create(
        output / "manifest.json",
        {
            "files": checked_files,
            "frozen_inputs": protocol["frozen_inputs"],
            "manifest_self_hash_excluded": True,
        },
    )


def run(output):
    output = output.resolve()
    output.relative_to(PROGRAM)
    if (output / "summary.json").exists():
        raise FileExistsError("Finished conservative diagnostic is immutable")
    protocol = read(output / "protocol.json")
    cpu_start, wall_start = time.process_time(), time.monotonic()
    cells = []
    checked_files = None

    def admit():
        if time.process_time() - cpu_start >= 90 or time.monotonic() - wall_start >= WALL_LIMIT:
            raise TimeoutError("Fixed coverage work-admission budget exceeded")

    try:
        verify(protocol["frozen_inputs"])
        rc = pytest.main(
            [
                str(RESEARCH / "test_conservative_coverage.py"),
                "-q",
                "-p",
                "no:cacheprovider",
                "--junitxml=" + str(output / "tests.xml"),
            ]
        )
        suites = ET.parse(output / "tests.xml").getroot()
        cases = list(suites.iter("testcase"))
        identities = {(case.attrib.get("classname"), case.attrib["name"]) for case in cases}
        if rc != 0 or len(cases) != len(identities) or len(cases) != TESTS:
            raise ValueError("Fixed conservative coverage fixture set did not pass")
        if any(list(suites.iter(tag)) for tag in ("failure", "error", "skipped")):
            raise ValueError("Failed or skipped cases cannot receive credit")
        scored = read(SNAPSHOT / "c4_score/c4_coverage.json")
        raw = read(SNAPSHOT / "c4/c4_raw.json")
        if raw["replications"] != 1000 or raw["scrambles"] != 16:
            raise ValueError("Original declared coverage dimensions differ")
        for case, filename, levels in ARMS:
            admit()
            estimates = np.load(SNAPSHOT / "c4" / filename, allow_pickle=False)
            if (
                estimates.shape != (1000, 16, len(levels))
                or estimates.dtype != np.dtype("float64")
                or not np.all(np.isfinite(estimates))
            ):
                raise ValueError("Complete finite original coverage array required")
            ref = scored["references"][case]
            if not ref["agreement_passed"]:
                raise ValueError("Fixed weighted-reference diagnostic branch required")
            reference, radius = map(binary64, (ref["reference"], ref["reference_hw99"]))
            means, standard = estimates.mean(1), estimates.std(1, ddof=1)
            for column, level in enumerate(levels):
                for nominal in (0.99, 0.95):
                    admit()
                    critical = float(student_t.ppf(1 - (1 - nominal) / 2, 15))
                    half_widths = critical * standard[:, column] / 4
                    memberships = [
                        classify(binary64(float(center)), binary64(float(half)), reference, radius)
                        for center, half in zip(means[:, column], half_widths, strict=True)
                    ]
                    counts = {
                        name: sum(getattr(item, name) for item in memberships)
                        for name in ("guaranteed", "reference_point", "possible")
                    }
                    assert counts["guaranteed"] <= counts["reference_point"] <= counts["possible"]
                    original_count = int(
                        (np.abs(means[:, column] - ref["reference"]) <= half_widths).sum()
                    )
                    saved = scored["cases"][case]["weighted"][str(2**level)][str(nominal)]
                    if original_count / 1000 != saved["raw"]:
                        raise ValueError("Original saved float score could not be reproduced")
                    intervals = {}
                    for label, k in counts.items():
                        admit()
                        lower, upper = clopper_pearson_outward(k, 1000)
                        intervals[label] = {"lower_exact": pair(lower), "upper_exact": pair(upper)}
                    cells.append(
                        {
                            "case": case,
                            "points_per_scramble": 2**level,
                            "nominal": nominal,
                            "reference_center_exact": pair(reference),
                            "reference_radius_exact": pair(radius),
                            "original_float_raw_successes": original_count,
                            "exact_geometry_successes": counts,
                            "exact_point_vs_original_float_count_difference": counts[
                                "reference_point"
                            ]
                            - original_count,
                            "count_intervals": intervals,
                            "true_price_probability_is_only_conditionally_sandwiched": True,
                        }
                    )
        assert len(cells) == 18
        create(output / "coverage_cells.json", cells)
        conditional_confidence = pair(
            conditional_joint_confidence(COUNT_FAILURE, (Fraction(1, 100),) * 2)
        )
        verify(protocol["frozen_inputs"])
        checked_files = receipt_files(output)
        cpu, wall = time.process_time() - cpu_start, time.monotonic() - wall_start
        if cpu >= CPU_LIMIT or wall >= WALL_LIMIT:
            raise TimeoutError("Fixed conservative coverage budget exceeded")
        create(
            output / "summary.json",
            {
                "passed": True,
                "budget_censored": False,
                "local_only": True,
                "fixtures_passed": TESTS,
                "unique_testcases": len(identities),
                "method_cells": len(cells),
                "directed_exact_binomial_intervals": 54,
                "original_saved_float_scores_reproduced": True,
                "classification_nesting_and_closed_ties_checked": True,
                "reference_true_price_confidence_premise_verified": False,
                "conditional_IID_binomial_model_verified": False,
                "conditional_joint_confidence_if_refs_99_percent_counts_95_percent_exact": (
                    conditional_confidence
                ),
                "conditional_joint_bound_is_not_an_established_confidence_theorem": True,
                "true_price_99_percent_delivery_proved": False,
                "original_Stage_C_rule_or_output_changed": False,
                "new_prices_paths_scrambles_timings": 0,
                "quantum_advantage_established": False,
                "CPU_seconds": cpu,
                "wall_seconds": wall,
            },
        )
    except BaseException as failure:
        checked_files = None
        create(output / "completed_cells.json", cells)
        create(
            output / "failure.json",
            {
                "passed": False,
                "budget_censored": isinstance(failure, TimeoutError),
                "new_test_credit": 0,
                "failure_type": type(failure).__name__,
                "message": str(failure),
                "traceback": traceback.format_exc(),
            },
        )
        if not (output / "summary.json").exists():
            create(
                output / "summary.json",
                {
                    "passed": False,
                    "budget_censored": isinstance(failure, TimeoutError),
                    "new_test_credit": 0,
                    "local_only": True,
                    "failure_type": type(failure).__name__,
                    "message": str(failure),
                    "true_price_99_percent_delivery_proved": False,
                },
            )
        raise
    finally:
        finish_manifest(output, protocol, checked_files)
    print(
        "Exact conservative geometry/count diagnostic retained; true-price premise still open",
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, default=PROGRAM / "C09_conservative_coverage_run001")
    args = parser.parse_args()
    (prepare if args.mode == "prepare" else run)(args.output)
