"""Prospectively freeze one bounded ordinary-tail rational certificate."""

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
from research.limitation_program_20261001.quantile_tail_certificate import (
    A,
    A_DECIMALS,
    B,
    B_DECIMALS,
    CELLS,
    F,
    RMAX,
    SHIFT,
    TARGET,
    TMAX,
    W,
    run_fixed_cells,
)
from research.limitation_program_20261001.quantile_tail_interval import (
    CDF_TERMS,
    DOMAIN,
    EXP_ARGUMENT_MAX,
    EXP_TERMS,
    PRECISION,
)


CENSUS = PROGRAM / "A02_quantile_census_run001"
CENTRAL = PROGRAM / "A02_quantile_central_run002"
CENTRAL_AUDIT = PROGRAM / "A02_quantile_central_audit_run001"
SOURCE = CENSUS / "primary_sources/R_qnorm.c"
CODE = (
    "quantile_tail_interval.py",
    "quantile_tail_certificate.py",
    "test_quantile_tail_certificate.py",
    "experiment_quantile_tail.py",
)


def source_coefficients():
    source = SOURCE.read_text(encoding="utf-8")
    ordinary = source.split("if (r <= 5.)", 1)[1].split("else if(r <= 27)", 1)[0]
    if "r += -1.6;" not in ordinary:
        raise ValueError("Official ordinary-tail argument shift changed")
    numerator, denominator = ordinary.split("val =", 1)[1].split("/", 1)
    pattern = r"(?<!\w)(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?"
    num = tuple(Fraction(token) for token in reversed(re.findall(pattern, numerator)))
    den = tuple(Fraction(token) for token in reversed(re.findall(pattern, denominator)))
    if num != A or den != B:
        raise ValueError("Exact official-source ordinary-tail coefficients changed")
    return {
        "primary_source": "https://svn.r-project.org/R/trunk/src/nmath/qnorm.c",
        "local_path": relative(SOURCE),
        "sha256": digest(SOURCE),
        "exact_official_ordinary_tail_coefficients_and_shift_match": True,
        "A_decimals_ascending": list(A_DECIMALS),
        "B_decimals_ascending": list(B_DECIMALS),
        "coefficient_fit_or_tuning": False,
        "published_accuracy_statement_adopted_as_proof": False,
    }


def prepare(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM.resolve())
    if output.exists():
        raise FileExistsError("Fresh prospective ordinary-tail receipt required")
    if not read(CENTRAL / "summary.json")["central_certificate_succeeded"]:
        raise ValueError("Completed successful central certificate required")
    if not read(CENTRAL_AUDIT / "summary.json")["passed"]:
        raise ValueError("Independent central audit required")
    coefficients = source_coefficients()
    frozen = {}
    for case in (CENSUS, CENTRAL, CENTRAL_AUDIT):
        receipt = read(case / "manifest.json")
        for field in ("files", "frozen_inputs"):
            for name, sha in receipt[field].items():
                normalized = name.replace("\\", "/")
                if normalized in frozen and frozen[normalized] != sha:
                    raise ValueError("Prerequisite receipt hashes disagree")
                frozen[normalized] = sha
        frozen[relative(case / "manifest.json")] = digest(case / "manifest.json")
    for name in CODE:
        path = ROOT / "research/limitation_program_20261001" / name
        frozen[relative(path)] = digest(path)
    for name in ("primitives.py", "ir.py"):
        path = ROOT / "research/controlled_source_completion" / name
        frozen[relative(path)] = digest(path)
    verify({"frozen_inputs": frozen})
    output.mkdir()
    for name in CODE:
        shutil.copy2(ROOT / "research/limitation_program_20261001" / name, output / name)
    protocol = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "local_only": True,
        "before_tests_or_fixed_cell_tail_evaluation": True,
        "source_coefficients": coefficients,
        "uniform_bits": 32,
        "fraction_bits": F,
        "native_word_width": W,
        "ordinary_tail_probability_domain_exact": [[1, 1 << 33], [3, 40]],
        "upper_probability_endpoint_exclusive": True,
        "transform": "r=sqrt(-ln(min(u,1-u)))-8/5, exact mathematical transform",
        "expanded_r_domain_exact": [[0, 1], [RMAX.numerator, RMAX.denominator]],
        "expanded_t_domain_exact": [
            [SHIFT.numerator, SHIFT.denominator],
            [TMAX.numerator, TMAX.denominator],
        ],
        "required_conditioned_uniform_quantile_error_exact": [TARGET.numerator, TARGET.denominator],
        "fixed_equal_r_cells": CELLS,
        "interval_methods": 1,
        "Taylor_jet_degree": 4,
        "dyadic_outward_precision_bits": PRECISION,
        "CDF_integrated_Taylor_degree": CDF_TERMS,
        "CDF_remainder": "|z|^259/(2^129*129!*259), absolute integral remainder",
        "Gaussian_domain_exact": [
            [-DOMAIN.numerator, DOMAIN.denominator],
            [DOMAIN.numerator, DOMAIN.denominator],
        ],
        "positive_exponential_Taylor_degree": EXP_TERMS,
        "fixed_Taylor_evaluation_order": (
            "Ascending terms: term_k=term_(k-1)*s/k. Sum positive terms for exp(s); "
            "sum (-1)^k*term_k/(2k+1), then multiply by z for the Gaussian integral."
        ),
        "exponential_argument_domain_exact": [
            [0, 1],
            [EXP_ARGUMENT_MAX.numerator, EXP_ARGUMENT_MAX.denominator],
        ],
        "exponential_remainder": (
            "25^129/(129!*(1-25/130)); invert positive exp enclosure for exp(-s)"
        ),
        "real_error_method": (
            "g(r)=Phi(-A(r)/B(r))-exp(-(r+8/5)^2). Bound center g0,g1,g2,g3; "
            "mean-value intersections degrees3,2,1,0; remainder h^4*sup|g4|/24. "
            "Gaussian Chernoff proves true quantile magnitude<=sqrt(2)*t. "
            "Prove positive rational magnitude^2<=2*t_lower^2 in each cell; "
            "inverse-density lower bound is prefactor_lo*exp(-t_upper^2). "
            "Separately prove true/rational magnitude<=6.5."
        ),
        "q32_domain_method": (
            "Positive degree4 exp(.7)>2 proves ln2<.7. Then33ln2<23.1<4.81^2<25; "
            "all exact q32 inputs avoid the extreme-tail branch. "
            "exp(-1.6^2)>3/40 proves transformed lower endpoint r>0."
        ),
        "conditional_native_rounding": (
            "HYPOTHETICAL exact transform FLOOR_f40(r), error<=1ulp. "
            "Nearest-even published coefficients; positive Horner multiply/add floors; "
            "unsigned dividefloor; sign restore. Cellwise native denominator lower "
            "bounds divide numeratorerror+6.5*denominatorerror; then add divisionulp. "
            "Prove stored72/product144/dividend112/denominator64, guard and quotient safety."
        ),
        "conditional_error_budget": (
            "real rational error + conditioned native rational arithmetic <=1e-8; "
            "actual log/sqrt error not included"
        ),
        "actual_coherent_log_sqrt_input_error_certificate": None,
        "actual_coherent_log_sqrt_transform_implemented": False,
        "actual_reversible_divider_width_cleanup_validation": None,
        "actual_quantum_gate_cost": None,
        "process_CPU_limit_seconds": 300,
        "adaptive_partition_or_precision_retry": False,
        "acceptance": (
            "All1024 fixed cells prove the conditional1e-8 target; otherwise preserve "
            "failed/censored receipt. No coherent transform/loader/source-path adoption "
            "or free division/gate-cost/full-price claim follows."
        ),
        "new_reversible_leaves_or_quantum_gates": 0,
        "new_original_financial_price_observations": 0,
        "accepted_Box_Muller_baseline_changed": False,
        "native_financial_path_certified": False,
        "full_G2_closed": False,
        "preexisting_Stage_C_jobs_edited": False,
        "frozen_inputs": frozen,
        "python": sys.version,
        "executable": sys.executable,
    }
    save(output / "protocol.json", protocol)
    verify(protocol)
    print("One 1024-cell ordinary-tail conditional proof prospectively frozen", flush=True)


def run(output):
    output = Path(output).resolve()
    if (output / "summary.json").exists():
        raise FileExistsError("Ordinary-tail receipt already completed")
    protocol = read(output / "protocol.json")
    verify(protocol)
    started = time.process_time()
    rc = pytest.main(
        [
            str(ROOT / "research/limitation_program_20261001/test_quantile_tail_certificate.py"),
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
                "tail_certificate_succeeded": False,
                "new_original_financial_prices_or_gates": 0,
            },
        )
        manifest(output, protocol)
        raise AssertionError("Frozen ordinary-tail fixtures failed")
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
                "tail_certificate_succeeded": False,
                "terminal_failure": traceback.format_exc(),
                "new_original_financial_prices_or_gates": 0,
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
        "ordinary_tail_only": True,
        "completed_fixed_cells": len(cells),
        "conditioned_on_hypothetical_exact_transform_floor": True,
        "actual_coherent_log_sqrt_input_error_certificate": None,
        "actual_coherent_log_sqrt_transform_implemented": False,
        "native_mathematical_interface_proof_contingent_on_complete_cells": True,
        "actual_reversible_divider_width_cleanup_validation": None,
        "actual_quantum_gate_cost": None,
        "coherent_loader_implemented_or_adopted": False,
        "native_financial_path_arithmetic_certified": False,
        "accepted_Box_Muller_baseline_changed": False,
        "full_G2_closed": False,
    }
    save(output / "tail_certificate.json", certificate)
    tests = sum(
        int(s.attrib["tests"]) for s in ET.parse(output / "tests.xml").getroot().iter("testsuite")
    )
    save(
        output / "summary.json",
        {
            "passed": True,
            "local_only": True,
            "fixtures_passed": tests,
            "tail_certificate_succeeded": result["certified"],
            "budget_censored": result["budget_censored"],
            "failure_reason": result["reason"],
            "fixed_cells": CELLS,
            "completed_cells": len(cells),
            "total_conditioned_tail_quantile_error_upper_exact": result.get(
                "total_conditioned_tail_quantile_error_upper_exact"
            ),
            "required_conditioned_uniform_quantile_error_exact": [
                TARGET.numerator,
                TARGET.denominator,
            ],
            "actual_coherent_transform_error_included": False,
            "actual_quantile_leaf_or_division_cost_charged": False,
            "native_financial_path_arithmetic_certified": False,
            "coherent_loader_implemented_or_adopted": False,
            "all_actual_transform_interface_loader_and_full_price_obligations_open": True,
            "new_original_financial_prices_or_gates": 0,
            "full_G2_closed": False,
            "quantum_advantage_established": False,
            "elapsed_process_CPU_seconds": time.process_time() - started,
        },
    )
    manifest(output, protocol)
    print(
        "Bounded ordinary-tail rational proof completed; certified=" + str(result["certified"]),
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    (prepare if args.mode == "prepare" else run)(args.output)
