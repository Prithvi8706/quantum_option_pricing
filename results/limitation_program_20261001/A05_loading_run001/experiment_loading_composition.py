"""One conservative and one pure-product loading-budget composition screen."""

import argparse
from datetime import datetime, timezone
from decimal import Decimal
from fractions import Fraction
import json
from pathlib import Path
import shutil

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
from research.limitation_program_20261001.loading_error_composition import allowances
from research.limitation_program_20261001.progress import ROOT


def pair(value):
    return [value.numerator, value.denominator]


def run(output):
    output.relative_to(PROGRAM.resolve())
    assert not output.exists()
    paths = []
    for receipt_name, suffixes in (
        ("G0_run003", ["B4x12_task.json", "B8x52_task.json"]),
        (
            "E07_complete_run001",
            ["B4x12_complete_price_ledger.json", "B8x52_complete_price_ledger.json"],
        ),
        ("A02_quantile_census_run001", ["archived_prefix_summary.json"]),
    ):
        directory = PROGRAM / receipt_name
        receipt = read(directory / "manifest.json")
        assert read(directory / "summary.json")["passed"]
        for suffix in suffixes:
            path = directory / suffix
            assert digest(path) == receipt["files"][relative(path)]
            paths.append(path)
        paths.extend([directory / "summary.json", directory / "manifest.json"])
    own = Path(__file__).resolve()
    for name in (
        own.name,
        "loading_error_composition.py",
        "test_loading_error_composition.py",
        "constant_library.py",
        "experiment_checkpoint.py",
        "progress.py",
    ):
        paths.append(ROOT / "research/limitation_program_20261001" / name)
    frozen = {relative(path): digest(path) for path in paths}
    output.mkdir()
    for path in paths:
        if path.parent == own.parent:
            shutil.copy2(path, output / path.name)
    protocol = dict(
        local_only=True,
        created_utc=datetime.now(timezone.utc).isoformat(),
        before_tests_and_loading_allowance_screen=True,
        frozen_inputs=frozen,
        loading_bias_dollars_exact=[1, 1000],
        bounded_payoff_span_dollars_exact=[40, 1],
        loading_budget_is_exploratory_not_adopted_in_current_BM_ledger=True,
        families=["general tensor-product telescoping", "independent pure-product fidelity"],
        fixed_dyadic_scalar_allowance_bits=128,
        actual_driver_counts=[60, 468],
        archive_diagnostic_grid_bits=10,
        archive_bond_caps=[2, 4, 8],
        stop_rule="Two composition methods and three existing q10 compression diagnostics only",
        coherent_gate_operator_errors_are_separate_from_state_preparation_law_bias=True,
        no_new_loading_circuits_or_synthesis_or_financial_paths=True,
    )
    save(output / "protocol.json", protocol)
    verify(protocol)
    rc = pytest.main(
        [
            str(own.parent / "test_loading_error_composition.py"),
            "-q",
            "-p",
            "no:cacheprovider",
            "--junitxml=" + str(output / "tests.xml"),
        ]
    )
    if rc:
        save(output / "summary.json", dict(passed=False, fixture_return_code=int(rc)))
        manifest(output, protocol)
        raise AssertionError("Prospective loading composition fixtures failed")
    archive = json.loads(
        (PROGRAM / "A02_quantile_census_run001/archived_prefix_summary.json").read_text(
            encoding="utf-8"
        ),
        parse_float=Decimal,
    )
    q10 = next(row for row in archive["cases"] if row["bits"] == 10)
    rows = []
    for case, draws in (("B4x12", 60), ("B8x52", 468)):
        task = read(PROGRAM / "G0_run003" / (case + "_task.json"))
        assert task["digital_source"]["normal_count"] == draws
        assert task["barrier_dollars"] - task["strike_dollars"] == 40
        assert task["annual_rate"] >= 0
        complete = read(PROGRAM / "E07_complete_run001" / (case + "_complete_price_ledger.json"))
        headroom = Fraction(*complete["assessment"]["remaining_dollar_headroom"])
        assert Fraction(1, 1000) < headroom
        row = allowances(draws)
        serial = row["conservative_scalar_trace_allowance"]
        pure = row["pure_product_scalar_trace_allowance_lower"]
        diagnostics = []
        for compression in q10["mps"]:
            error = Fraction(compression["trace_distance"])
            diagnostics.append(
                dict(
                    bond_cap=compression["bond_cap"],
                    recorded_numerical_scalar_trace_error_exact=pair(error),
                    below_conservative_scalar_allowance_numerically=error <= serial,
                    below_pure_product_scalar_allowance_numerically=error <= pure,
                    error_is_a_rigorous_preparation_certificate=False,
                    emitted_and_synthesized_MPS_circuit=False,
                    q10_binned_truncated_law_matches_current_q32_BM=False,
                    full_continuous_price_bridge_certified=False,
                )
            )
        rows.append(
            dict(
                case=case,
                draws=draws,
                loading_bias_dollars_exact=pair(row["loading_dollars"]),
                payoff_span_dollars_exact=pair(row["payoff_span"]),
                total_preparation_trace_allowance_exact=pair(row["total_trace_allowance"]),
                conservative_scalar_trace_allowance_exact=pair(serial),
                pure_product_scalar_trace_allowance_lower_exact=pair(pure),
                pure_product_scalar_trace_allowance_square_upper_exact=pair(
                    row["pure_product_scalar_allowance_square_upper"]
                ),
                exact_product_distance_squared_formula="1-(1-tau^2)^draws",
                product_distance_squared_proved_upper_exact=pair(draws * pure**2),
                pure_product_independence_and_purity_required=True,
                scalar_operator_norm_guarantee_supplied=False,
                coherent_rotation_errors_or_correlated_noise_included=False,
                current_price_ledger_changed=False,
                archived_q10_diagnostics=diagnostics,
            )
        )
    save(
        output / "certificate.json",
        dict(
            two_factor_identity="D_product^2 = D1^2+D2^2-D1^2*D2^2 for independent pure products",
            general_bound="D(tensor rho_i,tensor sigma_i) <= min(1,sum_i D(rho_i,sigma_i))",
            pure_bound="D_product^2 = 1-product_i(1-D_i^2) <= sum_i D_i^2",
            bounded_observable_bound="0<=Y<=40 implies |Tr[Y(rho-sigma)]|<=40*D(rho,sigma)",
            trace_distance_convention="one half of trace norm",
            purity_failure_or_factor_correlation_requires_general_valid_joint_bound=True,
            basis_state_preparation_error_is_not_full_unitary_operator_error=True,
            approximate_law_bias_and_repeated_gate_execution_error_are_distinct=True,
            rows=rows,
        ),
    )
    save(
        output / "summary.json",
        dict(
            passed=True,
            local_only=True,
            composition_families=2,
            actual_driver_profiles=2,
            archived_numerical_diagnostics=6,
            loading_budget_dollars_exact=[1, 1000],
            actual_certified_and_synthesized_MPS_candidates=0,
            law_replacement_adopted=False,
            current_complete_price_ledger_changed=False,
            new_financial_prices_or_gates=0,
            full_continuous_price_or_physical_certificate=False,
            next=(
                "Certify first two Gaussian prefix probability/angle levels, keeping full-tree cost"
            ),
        ),
    )
    manifest(output, protocol)
    print(
        "Two rigorous composition bounds; scalar allowances fixed; no loader adoption", flush=True
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output.resolve())
