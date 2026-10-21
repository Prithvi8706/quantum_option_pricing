"""Prospective first-date continuous-GBM barrier-band preparation, locally only."""

from __future__ import annotations

# Protocol/proof literals remain readable and preserve the precise scope.
# ruff: noqa: E501

import argparse
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
import shutil
import sys
import time

import pytest

from research.limitation_program_20261001.barrier_band_certificate import (
    BUILDER,
    PROOF,
    assemble_dollar_bias,
    band_bounds,
    certify_one_date,
    common_variance,
    original_model,
    pair,
)
from research.limitation_program_20261001.constant_library import digest
from research.limitation_program_20261001.experiment_checkpoint import (
    BASELINE,
    PROGRAM,
    manifest,
    read,
    relative,
    save,
    verify,
)
from research.limitation_program_20261001.progress import ROOT


CODE = (
    "barrier_band_certificate.py",
    "test_barrier_band_certificate.py",
    "experiment_barrier_band.py",
    "financial_bounded_schedule.py",
)


def prepare(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM.resolve())
    if output.exists():
        raise FileExistsError("C07 prospective receipt must be new")
    output.mkdir()
    frozen = {}
    for name in CODE:
        path = ROOT / "research/limitation_program_20261001" / name
        snapshot = output / "executed_code" / name
        snapshot.parent.mkdir(exist_ok=True)
        shutil.copy2(path, snapshot)
        frozen[relative(path)] = digest(path)
    frozen[relative(BUILDER)] = digest(BUILDER)
    for name in ("target.json", "source.json", "schedule_capped.json"):
        path = BASELINE / "B4x12/min-depth" / name
        frozen[relative(path)] = digest(path)
    # AST extraction reads declared constants; no graph, gate or price evaluation.
    inventory = [original_model(case) for case in ("B4x12", "B8x52")]
    save(output / "original_model_inventory.json", inventory)
    protocol = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "local_only": True,
        "item": "C07 conditional common-Gaussian barrier anti-concentration prerequisite",
        "before_tests_and_probability_bound_evaluation": True,
        "production_case": "B4x12",
        "production_date": 1,
        "analytical_bound_forms": ["density", "centered_interval_maximum"],
        "analytical_bound_form_count": 2,
        "diagnostic_eta_dollars_exact": [1, 10000],
        "diagnostic_eta_is_a_proved_native_discrepancy": False,
        "eta_grid_or_adaptive_radius_search": False,
        "external_proofs": {
            "eta": None,
            "path_log_discrepancy": None,
            "bad_event_probability": None,
            "discounted_zeta": None,
            "discounted_payoff_cap": None,
            "any_date_band_probability": None,
            "discounted_tail_dollars": None,
        },
        "rigorous_numeric_method": "Exact rational Machin pi, integer sqrt enclosures, atanh log series with geometric remainder, 192-term integrated exponential Taylor and outward dyadic arithmetic",
        "precision_bits": 224,
        "integrated_taylor_terms": 192,
        "proof": PROOF,
        "acceptance": "Original GBM parameters, sigma/rho/t positive, exact factorization and Gaussian interval supremum, strict barrier endpoint measure, rigorous two-bound enclosure, externally proved clipping/exp/coupling scope required, every missing financial term remains null",
        "stop_rule": "Exactly two bound forms on B4 date1; one fixed exploratory eta=0.0001 dollar. No all-date union claim, no Gaussian independence claim for digital pairs, no conditioning Gaussian independence on the coupling good domain; no financial/quantum path samples",
        "continuous_price_error_certified": False,
        "full_G2_closed": False,
        "second_discount": False,
        "new_financial_gate_replays": 0,
        "new_financial_price_samples": 0,
        "process_cpu_limit_seconds": 120,
        "frozen_inputs": frozen,
        "python": sys.version,
        "executable": sys.executable,
    }
    save(output / "protocol.json", protocol)
    verify(protocol)
    print("C07 one-date/two-bound prospective protocol frozen", flush=True)


def run(output):
    output = Path(output).resolve()
    protocol = read(output / "protocol.json")
    if (output / "summary.json").exists():
        raise FileExistsError("C07 receipt already completed")
    verify(protocol)
    started = time.process_time()
    rc = pytest.main(
        [
            str(ROOT / "research/limitation_program_20261001/test_barrier_band_certificate.py"),
            "-q",
            "-p",
            "no:cacheprovider",
            "--junitxml=" + str(output / "tests.xml"),
        ]
    )
    if rc:
        save(output / "failed_tests.json", {"passed": False, "return_code": int(rc)})
        manifest(output, protocol)
        raise AssertionError("Frozen C07 proof fixtures failed")
    if time.process_time() - started > protocol["process_cpu_limit_seconds"]:
        save(output / "failed_limit.json", {"passed": False, "cpu_limit_seconds": 120})
        manifest(output, protocol)
        raise TimeoutError("C07 prospective CPU limit")
    certificate = certify_one_date(protocol["production_case"], protocol["production_date"])
    model = certificate["model"]
    diagnostic = band_bounds(
        Fraction(*protocol["diagnostic_eta_dollars_exact"]),
        model["barrier_dollars_exact"],
        common_variance(model, 1),
    )
    diagnostic.update(
        {
            "exploratory_only": True,
            "proved_native_discrepancy": False,
            "used_as_financial_error_certificate": False,
        }
    )
    certificate["fixed_exploratory_band_diagnostic"] = diagnostic
    certificate["dollar_bias_assembly"] = assemble_dollar_bias(model)
    save(output / "B4_date1_certificate.json", certificate)
    (output / "PROOF.md").write_text(
        "# Continuous one-date barrier-band proof\n\n" + "\n\n".join(PROOF.values()) + "\n",
        encoding="utf-8",
    )
    summary = {
        "passed": True,
        "local_only": True,
        "case": "B4x12",
        "date": 1,
        "analytical_bound_form_count": 2,
        "common_log_variance_exact": pair(common_variance(model, 1)),
        "fixed_exploratory_eta_dollars_exact": [1, 10000],
        "exploratory_density_probability_upper_exact": diagnostic["density"][
            "probability_upper_exact"
        ],
        "exploratory_centered_probability_upper_exact": diagnostic["centered_interval_maximum"][
            "probability_upper_exact"
        ],
        "eta_discrepancy_proof": None,
        "discounted_zeta_proof": None,
        "bad_event_probability_proof": None,
        "discounted_tail_dollars_proof": None,
        "any_date_band_probability_proof": None,
        "discounted_payoff_cap_proof": None,
        "native_clipping_and_exponential_discrepancy_proof": None,
        "full_continuous_dollar_error_upper": None,
        "full_G2_closed": False,
        "missing_bounds_are_zero": False,
        "gaussian_independence_asserted_for_finite_pairs": False,
        "gaussian_independence_conditioned_on_good_event": False,
        "all_dates_covered": False,
        "second_discount_applied": False,
        "new_financial_gate_replays": 0,
        "new_financial_price_samples": 0,
        "elapsed_cpu_seconds": time.process_time() - started,
        "next": "Bind externally proved C06 eta and separate bad-event probability; retain smooth Asian-payoff zeta, all-date band probability and discounted tail dollars as open obligations. Independently audit this analytic proof before adoption.",
    }
    save(output / "summary.json", summary)
    manifest(output, protocol)
    print("C07 rigorous band preparation passed; full financial error remains open", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    (prepare if args.mode == "prepare" else run)(args.output)
