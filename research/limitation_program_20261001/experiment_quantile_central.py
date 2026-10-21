"""One frozen AS241 central-only interval certificate, without quantum gates."""

import argparse
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
import re
import shutil
import sys
import time
import traceback
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
from research.limitation_program_20261001.quantile_central_certificate import (
    A,
    A_DECIMALS,
    B,
    B_DECIMALS,
    CELLS,
    F,
    QMAX,
    RMAX,
    TARGET,
    W,
    run_fixed_cells,
)
from research.limitation_program_20261001.quantile_central_interval import (
    CDF_TERMS,
    DOMAIN,
    EXP_TERMS,
    PRECISION,
)


CENSUS = PROGRAM / "A02_quantile_census_run001"
SOURCE = CENSUS / "primary_sources/R_qnorm.c"
CODE = (
    "quantile_central_interval.py",
    "quantile_central_certificate.py",
    "test_quantile_central_certificate.py",
    "experiment_quantile_central.py",
)


def source_coefficients():
    source = SOURCE.read_text(encoding="utf-8")
    central = source.split("if (fabs(q) <= .425)", 1)[1].split("else {", 1)[0]
    numerator, denominator = central.split("val =", 1)[1].split("/", 1)
    pattern = r"(?<!\w)(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?"
    num = tuple(Fraction(token) for token in reversed(re.findall(pattern, numerator)))
    den = tuple(Fraction(token) for token in reversed(re.findall(pattern, denominator)))
    if num != A or den != B:
        raise ValueError("Published official-source central coefficient lists changed")
    return {
        "primary_source": "https://svn.r-project.org/R/trunk/src/nmath/qnorm.c",
        "local_path": relative(SOURCE),
        "sha256": digest(SOURCE),
        "coefficient_tokens_exactly_match_official_central_branch": True,
        "A_decimals_ascending": list(A_DECIMALS),
        "B_decimals_ascending": list(B_DECIMALS),
        "coefficient_fit_or_tuning": False,
    }


def prepare(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM.resolve())
    if output.exists():
        raise FileExistsError("Fresh prospective central certificate receipt required")
    if not read(CENSUS / "summary.json")["passed"]:
        raise ValueError("Completed bounded loader census required")
    coefficients = source_coefficients()
    receipt = read(CENSUS / "manifest.json")
    frozen = {
        name.replace("\\", "/"): sha
        for field in ("files", "frozen_inputs")
        for name, sha in receipt[field].items()
    }
    frozen[relative(CENSUS / "manifest.json")] = digest(CENSUS / "manifest.json")
    for name in CODE:
        path = ROOT / "research/limitation_program_20261001" / name
        frozen[relative(path)] = digest(path)
    verify({"frozen_inputs": frozen})
    output.mkdir()
    for name in CODE:
        shutil.copy2(ROOT / "research/limitation_program_20261001" / name, output / name)
    protocol = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "local_only": True,
        "before_tests_or_fixed_cell_certificate_evaluation": True,
        "source_coefficients": coefficients,
        "uniform_bits": 32,
        "fraction_bits": F,
        "native_word_width": W,
        "domain_u_exact": [[3, 40], [37, 40]],
        "domain_q_exact": [[-QMAX.numerator, QMAX.denominator], [QMAX.numerator, QMAX.denominator]],
        "rconstant_exact": [RMAX.numerator, RMAX.denominator],
        "required_uniform_absolute_quantile_error_exact": [TARGET.numerator, TARGET.denominator],
        "fixed_equal_q_cells": CELLS,
        "interval_methods": 1,
        "dyadic_outward_precision_bits": PRECISION,
        "Taylor_jet_degree": 3,
        "CDF_integrated_Taylor_degree": CDF_TERMS,
        "density_exponential_Taylor_degree": EXP_TERMS,
        "Gaussian_domain_exact": [
            [-DOMAIN.numerator, DOMAIN.denominator],
            [DOMAIN.numerator, DOMAIN.denominator],
        ],
        "real_error_method": (
            "At each fixed cell center bound g=Phi(z(q))-q-1/2,g',g''; "
            "bound sup|g'''| on the cell with exact rational order3 jets. "
            "Use mean-value intersections from higher to lower derivatives "
            "within the same jets. Taylor residual is|g0|+h|g1|+h²|g2|/2+h³sup|g3|/6. "
            "Prove z andtruequantile inside±1.5 andphi>=1/8, so inverse error<=8residual."
        ),
        "native_rounding_rules": (
            "Nearest-even published coefficients; CEIL_f40 rconstant; "
            "q32 midpoint/q exactlyrepresentable; floorq² and positiveHorner "
            "multiply/add; positive-magnitude unsigneddividefloor; signedrestoration. "
            "This is a NEWcentral approximation law, not prior exactfloorquantilelaw."
        ),
        "native_error_method": (
            "Coefficientwise Horner roundoff plus polynomial derivative times "
            "rargumenterror; denominatornative>=1; ratioerror<=numeratorerror "
            "+1.5denominatorerror+divisionULP; prove stored72/product144/dividend112 "
            "bounds. The documented kernel semantics remain a mathematical "
            "interface lemma, not emitted/replayed gate-level validation."
        ),
        "process_CPU_limit_seconds": 180,
        "adaptive_partition_or_precision_retry": False,
        "acceptance": (
            "All2048 fixedcell bounds plus declarednative rounding prove total "
            "uniformcentral error<=1e-8. Otherwise preserve failed/budgetcensored "
            "certificate without additional attempts. Alltails/globalinterfaces/ "
            "nativefinancialpath/loader/cost/G2 remainopen."
        ),
        "new_reversible_leaves_or_quantum_gates": 0,
        "new_original_financial_price_observations": 0,
        "existing_division_source_path": "research/controlled_source_completion/primitives.py",
        "actual_division_gate_cost": None,
        "coherent_loader_implemented_or_adopted": False,
        "full_G2_closed": False,
        "preexisting_Stage_C_jobs_edited": False,
        "frozen_inputs": frozen,
        "python": sys.version,
        "executable": sys.executable,
    }
    save(output / "protocol.json", protocol)
    verify(protocol)
    print("One2048-cell AS241 central-only certificate prospectively frozen", flush=True)


def run(output):
    output = Path(output).resolve()
    if (output / "summary.json").exists():
        raise FileExistsError("Central certificate receipt already completed")
    protocol = read(output / "protocol.json")
    verify(protocol)
    started = time.process_time()
    rc = pytest.main(
        [
            str(ROOT / "research/limitation_program_20261001/test_quantile_central_certificate.py"),
            "-q",
            "-p",
            "no:cacheprovider",
            "--junitxml=" + str(output / "tests.xml"),
        ]
    )
    if rc:
        save(
            output / "summary.json",
            {
                "passed": False,
                "fixture_return_code": int(rc),
                "central_certificate_succeeded": False,
            },
        )
        manifest(output, protocol)
        raise AssertionError("Frozen central certificate fixtures failed")
    verify(protocol)
    source_coefficients()
    try:
        result = run_fixed_cells(
            max(0, protocol["process_CPU_limit_seconds"] - (time.process_time() - started))
        )
    except Exception:
        save(
            output / "summary.json",
            {
                "passed": False,
                "central_certificate_succeeded": False,
                "terminal_failure": traceback.format_exc(),
                "new_reversible_leaves_or_quantum_gates": 0,
            },
        )
        manifest(output, protocol)
        raise
    cells = result.pop("cells_completed")
    save(
        output / "cell_bounds.json",
        {"fixed_cells": CELLS, "completed_cells": len(cells), "cells": cells},
    )
    certificate = {
        **result,
        "source_coefficients": protocol["source_coefficients"],
        "uniform_bits": 32,
        "fraction_bits": F,
        "native_word_width": W,
        "central_domain_only": True,
        "domain_u_exact": protocol["domain_u_exact"],
        "completed_fixed_cells": len(cells),
        "new_approximation_law_not_prior_exact_floor_law": True,
        "ordinary_and_extreme_tails_certified": False,
        "native_mathematical_interface_proof_contingent_on_complete_cells": True,
        "actual_reversible_leaf_or_division_gate_cost": None,
        "native_financial_path_arithmetic_certified": False,
        "coherent_loader_implemented": False,
        "full_G2_closed": False,
        "accepted_Box_Muller_baseline_changed": False,
    }
    save(output / "central_certificate.json", certificate)
    suites = ET.parse(output / "tests.xml").getroot()
    tests = sum(int(s.attrib["tests"]) for s in suites.iter("testsuite"))
    save(
        output / "summary.json",
        {
            "passed": True,
            "local_only": True,
            "fixtures_passed": tests,
            "central_certificate_succeeded": result["certified"],
            "budget_censored": result["budget_censored"],
            "failure_reason": result["reason"],
            "fixed_cells": CELLS,
            "completed_cells": len(cells),
            "total_central_quantile_error_upper_exact": result.get(
                "total_central_quantile_error_upper_exact"
            ),
            "required_uniform_quantile_error_exact": [TARGET.numerator, TARGET.denominator],
            "source_coefficients_unmodified": True,
            "new_central_approximation_law": True,
            "ordinary_and_extreme_tails_certified": False,
            "actual_quantile_leaf_or_division_cost_charged": False,
            "all_native_global_loader_and_full_price_obligations_open": True,
            "new_original_financial_prices_or_gates": 0,
            "full_G2_closed": False,
            "quantum_advantage_established": False,
            "elapsed_process_CPU_seconds": time.process_time() - started,
            "next": (
                "Independent review of the fixedcentral proof; retain tails and "
                "actual nativeinterface/gatecleanup/cost as distinct prerequisites "
                "before any complete quantileloader or sourceadoption."
            ),
        },
    )
    manifest(output, protocol)
    print("Central-only bounded proof completed; certified=" + str(result["certified"]), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    (prepare if args.mode == "prepare" else run)(args.output)
