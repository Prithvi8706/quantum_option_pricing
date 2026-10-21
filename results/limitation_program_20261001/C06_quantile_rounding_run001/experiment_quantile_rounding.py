"""Prospectively freeze a bounded q32/f40 rounded-quantile prerequisite."""

import argparse
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
import shutil
import sys
import time
import xml.etree.ElementTree as ET

import pytest

from research.limitation_program_20261001.constant_library import digest
from research.limitation_program_20261001.experiment_checkpoint import (
    PROGRAM,
    manifest,
    read,
    relative,
    save,
    verify,
)
from research.limitation_program_20261001.progress import ROOT
from research.limitation_program_20261001.quantile_rounding_certificate import (
    F,
    MAX_STEPS,
    Q,
    RAW_WORDS,
    W,
    defined_law_certificate,
    normal_cdf_interval,
    solve_quantile_word,
)


GRID = PROGRAM / "C06_quantile_grid_run001"
GRID_AUDIT = PROGRAM / "C06_quantile_grid_audit_run001"
GAUSSIAN = PROGRAM / "C07_barrier_run002"
GAUSSIAN_AUDIT = PROGRAM / "C07_barrier_audit_run001"
CODE = (
    "quantile_rounding_certificate.py",
    "test_quantile_rounding_certificate.py",
    "experiment_quantile_rounding.py",
)


def prepare(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM.resolve())
    if output.exists():
        raise FileExistsError("New prospective rounded-quantile receipt required")
    for directory in (GRID, GRID_AUDIT, GAUSSIAN, GAUSSIAN_AUDIT):
        if not read(directory / "summary.json")["passed"]:
            raise ValueError("Accepted Gaussian enclosure and independent ideal-law audit required")
    if not read(GRID_AUDIT / "summary.json")[
        "independent_ideal_scalar_midpoint_grid_theorem_audit"
    ]:
        raise ValueError("Independent original financial BV/product theorem audit required")
    frozen = {}
    for directory in (GRID, GRID_AUDIT, GAUSSIAN, GAUSSIAN_AUDIT):
        receipt = read(directory / "manifest.json")
        for field in ("files", "frozen_inputs"):
            for name, sha in receipt[field].items():
                frozen[name.replace("\\", "/")] = sha
        frozen[relative(directory / "manifest.json")] = digest(directory / "manifest.json")
    for name in CODE:
        path = ROOT / "research/limitation_program_20261001" / name
        frozen[relative(path)] = digest(path)
    for name in (
        "barrier_band_certificate.py",
        "financial_bounded_schedule.py",
        "experiment_checkpoint.py",
        "constant_library.py",
        "progress.py",
    ):
        path = ROOT / "research/limitation_program_20261001" / name
        frozen[relative(path)] = digest(path)
    verify({"frozen_inputs": frozen})
    output.mkdir()
    for name in CODE:
        shutil.copy2(ROOT / "research/limitation_program_20261001" / name, output / name)
    protocol = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "local_only": True,
        "before_tests_and_actual_quantile_word_evaluations": True,
        "cases": ["B4x12", "B8x52"],
        "uniform_bits": Q,
        "fraction_bits": F,
        "word_width": W,
        "rounding": "downward FLOOR",
        "raw_words": list(RAW_WORDS),
        "raw_words_hex": [f"{raw:08x}" for raw in RAW_WORDS],
        "word_selection": (
            "Exactly min/max and theirneighbors, four centerneighbors, four "
            "quarterboundaryneighbors, four literal fixed hexadecimal seedwords"
        ),
        "maximum_actual_quantile_words": 16,
        "enclosure_methods": 1,
        "method": "Audited C07 integratedGaussianTaylor192/precision224 plus symmetry",
        "initial_quantile_bracket": [-8, 8],
        "maximum_bisection_steps_per_word": MAX_STEPS,
        "precision_extension_or_retry_allowed": False,
        "domain_proof": (
            "Two additional fixed endpointCDFenclosures prove allq32 exact "
            "quantiles liein[-8,8]; this proves range of the defined function "
            "and does not establish allword solver completeness"
        ),
        "fixture_scope": (
            "FixedGaussianCDF arguments0,1/2,1,2,8 and theirsymmetry; synthetic "
            "CDF solverfixtures only, no extraactualGaussianquantile words"
        ),
        "law_bound": "KS<=2^-33+(2/5)*2^-40; discountedpricebias<=dimension*80*KS",
        "all_input_defined_law_distinct_from_solver_completeness": True,
        "acceptance": (
            "Emit a signed72f40word only when the exact open root interval "
            "proves oneFLOORbin; preserve every unresolved input as censored/null. "
            "Record classicalsolverCPU/steps/CDFcalls without quantumcost transfer. "
            "Retain conditionalKS/BVproduct theorem with allnative/loader/fullprice flagsfalse"
        ),
        "process_cpu_limit_seconds": 300,
        "actual_quantum_gate_emissions_or_replays": 0,
        "original_B4_B8_price_observations": 0,
        "coherent_loader_adopted": False,
        "preexisting_Stage_C_jobs_edited": False,
        "frozen_inputs": frozen,
        "python": sys.version,
        "executable": sys.executable,
    }
    save(output / "protocol.json", protocol)
    verify(protocol)
    print("q32/f40 sixteen-word quantile prerequisite prospectively frozen", flush=True)


def run(output):
    output = Path(output).resolve()
    if (output / "summary.json").exists():
        raise FileExistsError("Rounded-quantile receipt already completed")
    protocol = read(output / "protocol.json")
    verify(protocol)
    started = time.process_time()
    rc = pytest.main(
        [
            str(
                ROOT / "research/limitation_program_20261001/test_quantile_rounding_certificate.py"
            ),
            "-q",
            "-p",
            "no:cacheprovider",
            "--junitxml=" + str(output / "tests.xml"),
        ]
    )
    if rc:
        save(output / "summary.json", {"passed": False, "fixture_return_code": int(rc)})
        manifest(output, protocol)
        raise AssertionError("Frozen rounded-quantile fixtures failed")
    domain_started = time.process_time()
    left, right = normal_cdf_interval(Fraction(-8)), normal_cdf_interval(Fraction(8))
    endpoint = Fraction(1, 2**33)
    if not left[1] < endpoint or not right[0] > 1 - endpoint:
        save(
            output / "summary.json",
            {
                "passed": False,
                "terminal_failure": "fixed_allinput_quantile_range_unproved",
            },
        )
        manifest(output, protocol)
        raise ArithmeticError("Fixed all-input q32 quantile domain proof failed")
    domain = {
        "proved": True,
        "minimum_probability_exact": [1, 2**33],
        "maximum_probability_exact": [2**33 - 1, 2**33],
        "initial_quantile_bracket": [-8, 8],
        "endpoint_CDF_intervals_exact": [
            [[value.numerator, value.denominator] for value in left],
            [[value.numerator, value.denominator] for value in right],
        ],
        "defined_quantile_floor_f40_signed_absolute_upper": 8 * 2**40,
        "defined_floor_word_within_native_signed72": True,
        "all_input_solver_completeness_certified": False,
        "CDF_enclosure_evaluations": 2,
        "classical_domain_proof_CPU_seconds": time.process_time() - domain_started,
    }
    save(output / "defined_quantile_domain.json", domain)
    words = []
    for raw in protocol["raw_words"]:
        if time.process_time() - started > protocol["process_cpu_limit_seconds"]:
            save(
                output / "summary.json",
                {
                    "passed": False,
                    "terminal_failure": "prospective_classical_CPU_limit",
                    "completed_actual_word_records": len(words),
                },
            )
            manifest(output, protocol)
            raise TimeoutError("Prospective rounded-quantile CPU limit")
        row = solve_quantile_word(raw)
        words.append(row)
        save(output / "words" / (f"{raw:08x}" + ".json"), row)
        print(f"{raw:08x}", "certified" if row["certified"] else "censored", flush=True)
    wordfile = output / "quantile_words.json"
    save(wordfile, {"uniform_bits": Q, "fraction_bits": F, "word_width": W, "words": words})
    rows = []
    for case in protocol["cases"]:
        previous = read(GRID / (case + "_certificate.json"))
        row = defined_law_certificate(case)
        if previous["normal_coordinates"] != row["normal_coordinates"]:
            raise ValueError("Original ideal-law coordinate dimension changed")
        row["original_model_binding"] = previous["original_model_binding"]
        row["coordinate_BV_proof_audit"] = relative(GRID_AUDIT / (case + "_audit.json"))
        row["coordinate_BV_proof_audit_sha256"] = digest(GRID_AUDIT / (case + "_audit.json"))
        row["finite_word_records"] = relative(wordfile)
        row["finite_word_records_sha256"] = digest(wordfile)
        row["finite_word_count"] = len(words)
        row["all_input_quantile_domain_proof"] = relative(output / "defined_quantile_domain.json")
        save(output / (case + "_certificate.json"), row)
        rows.append({key: value for key, value in row.items() if key != "proof"})
    suites = ET.parse(output / "tests.xml").getroot()
    tests = sum(int(suite.attrib["tests"]) for suite in suites.iter("testsuite"))
    certified = sum(row["certified"] for row in words)
    elapsed = time.process_time() - started
    summary = {
        "passed": True,
        "local_only": True,
        "fixtures_passed": tests,
        "cases": rows,
        "actual_quantile_words_attempted": len(words),
        "actual_quantile_words_certified": certified,
        "actual_quantile_words_censored": len(words) - certified,
        "censor_reasons": dict(Counter(row["censor_reason"] for row in words if row["censored"])),
        "total_actual_word_bisection_steps": sum(row["bisection_steps"] for row in words),
        "total_actual_word_CDF_enclosure_evaluations": sum(
            row["CDF_enclosure_evaluations"] for row in words
        ),
        "maximum_actual_word_bisection_steps": max(row["bisection_steps"] for row in words),
        "classical_actual_word_solver_CPU_seconds": sum(
            row["classical_solver_CPU_seconds"] for row in words
        ),
        "elapsed_process_CPU_seconds_including_tests_and_theorem": elapsed,
        "classical_solver_work_charged_only_as_classical": True,
        "all_input_defined_rounded_law_certificate": True,
        "all_input_solver_completeness_certified": False,
        "accepted_Box_Muller_law_certified": False,
        "native_financial_path_arithmetic_certified": False,
        "coherent_loader_implemented_or_adopted": False,
        "full_G2_closed": False,
        "original_B4_B8_price_observations_or_gate_replays": 0,
        "quantum_gate_costs_extrapolated": False,
        "quantum_advantage_established": False,
        "preexisting_Stage_C_jobs_edited": False,
        "next": (
            "Independent audit of each emitted floorbin and the conditionalKS/BVlaw "
            "theorem; a complete bounded quantilealgorithm and coherent reversible "
            "implementation/nativepath errorproof remain separate obligations"
        ),
    }
    save(output / "summary.json", summary)
    manifest(output, protocol)
    print(
        "Local rounded-quantile prerequisite complete; loader/native path remain open", flush=True
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    (prepare if args.mode == "prepare" else run)(args.output)
