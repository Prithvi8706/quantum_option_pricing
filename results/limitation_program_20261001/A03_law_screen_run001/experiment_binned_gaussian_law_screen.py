"""Conditional uniform-grid law certificate; no price-bias lower bound."""

import argparse
from datetime import datetime, timezone
from fractions import Fraction
from math import factorial
from pathlib import Path
import shutil

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


def pair(value):
    return [value.numerator, value.denominator]


def run(output):
    output.relative_to(PROGRAM.resolve())
    assert not output.exists()
    paths = []
    for receipt_name, suffixes in (
        ("C06_quantile_grid_run001", ["B4x12_certificate.json", "B8x52_certificate.json"]),
        ("C06_quantile_grid_audit_run001", []),
        ("A05_loading_run001", ["certificate.json"]),
        ("A05_loading_audit_run001", []),
        ("G0_run003", ["B4x12_task.json", "B8x52_task.json"]),
    ):
        directory = PROGRAM / receipt_name
        assert read(directory / "summary.json")["passed"]
        receipt = read(directory / "manifest.json")
        for suffix in suffixes:
            path = directory / suffix
            assert digest(path) == receipt["files"][relative(path)]
            paths.append(path)
        paths.extend([directory / "summary.json", directory / "manifest.json"])
    own = Path(__file__).resolve()
    paths.extend(
        ROOT / "research/limitation_program_20261001" / name
        for name in (own.name, "constant_library.py", "experiment_checkpoint.py", "progress.py")
    )
    frozen = {relative(path): digest(path) for path in paths}
    output.mkdir()
    shutil.copy2(own, output / own.name)
    protocol = dict(
        local_only=True,
        created_utc=datetime.now(timezone.utc).isoformat(),
        before_conditional_law_and_tree_screen=True,
        frozen_inputs=frozen,
        fixed_truncation_exact=[6, 1],
        fixed_grid_bits=list(range(4, 33)),
        positive_exp_lower_polynomial_degree=128,
        explored_grid_law_bias_dollars_exact=[1, 1000],
        explored_preparation_bias_dollars_separate_exact=[1, 1000],
        two_distinct_allowances_not_double_spent=True,
        budgets_not_adopted_in_current_BM_price_ledger=True,
        original_ideal_GBM_coordinate_variation_upper_exact=[80, 1],
        stop_rule="29 fixed uniform-x grid widths per original model; no emitter or adaptation",
        new_tests_gates_financial_prices_or_replays=0,
    )
    save(output / "protocol.json", protocol)
    verify(protocol)
    # Mills: integral_6^infinity phi(x) dx <= integral_6^infinity x*phi(x)/6 dx.
    # phi(0)<2/5; positive Taylor terms give a rigorous lower bound on exp(18).
    exp_lower = sum((Fraction(18) ** k / factorial(k) for k in range(129)), Fraction(0))
    tail = Fraction(1, 15) / exp_lower
    assert 0 < tail < Fraction(1, 100000000)
    law_budget = Fraction(1, 1000)
    rows = []
    for case, draws in (("B4x12", 60), ("B8x52", 468)):
        task = read(PROGRAM / "G0_run003" / (case + "_task.json"))
        assert task["digital_source"]["normal_count"] == draws
        source_certificate = read(
            PROGRAM / "C06_quantile_grid_run001" / (case + "_certificate.json")
        )
        assert source_certificate["normal_coordinates"] == draws
        assert source_certificate["coordinate_total_variation_upper_dollars_exact"] == [80, 1]
        binding = source_certificate["original_model_binding"]
        assert binding["case"] == case and binding["assets"] == task["assets"]
        assert binding["dates"] == task["dates"] and binding["equal_asset_volatility"]
        assert binding["strike_dollars_exact"] == [100, 1]
        assert binding["barrier_dollars_exact"] == [140, 1]
        assert binding["rate_exact"] == [3, 100] and binding["maturity_years_exact"] == [1, 1]
        assert not source_certificate["accepted_Box_Muller_law_certified"]
        candidates = []
        for bits in protocol["fixed_grid_bits"]:
            spacing = Fraction(12, 1 << bits)
            ks_upper = tail + Fraction(2, 5) * spacing / (2 * (1 - 2 * tail))
            uniform_bound = 80 * draws * ks_upper
            candidates.append(
                dict(
                    grid_bits=bits,
                    grid_spacing_exact=pair(spacing),
                    scalar_CDF_distance_upper_exact=pair(ks_upper),
                    uniform_coordinate_BV_price_difference_upper_exact=pair(uniform_bound),
                    bounded_price_difference_upper_exact=pair(min(Fraction(40), uniform_bound)),
                    uniform_certificate_fits_grid_law_budget=uniform_bound <= law_budget,
                    complete_prefix_conditional_rotations=(1 << bits) - 1,
                    independent_draw_prefix_rotation_nodes=draws * ((1 << bits) - 1),
                    remaining_conditional_angles_certified=False,
                    emitted_synthesized_full_loader=False,
                )
            )
        minimum = next(row for row in candidates if row["uniform_certificate_fits_grid_law_budget"])
        original = next(row for row in candidates if row["grid_bits"] == 10)
        assert not original["uniform_certificate_fits_grid_law_budget"]
        rows.append(
            dict(
                case=case,
                independent_driver_count=draws,
                existing_q10_uniform_BV_certificate_rejected=True,
                existing_q10_uniform_bound_exact=original[
                    "uniform_coordinate_BV_price_difference_upper_exact"
                ],
                first_fixed_bits_passing_uniform_bound=minimum["grid_bits"],
                candidates=candidates,
            )
        )
    assert [row["first_fixed_bits_passing_uniform_bound"] for row in rows] == [24, 27]
    save(
        output / "certificate.json",
        dict(
            Mills_tail_proof="Q(6)<=phi(6)/6 < exp(-18)/15 <=1/(15*Taylor128_exp(18))",
            one_sided_tail_probability_upper_exact=pair(tail),
            normalized_conditional_CDF_difference_upper="Q(6)",
            midpoint_rounding_conditional_CDF_upper="(2/5)*(spacing/2)/(1-2*Q(6))",
            uniform_price_transfer=(
                "coordinate BV<=80 times scalar KS, summed over independent drivers"
            ),
            underlying_GBM_arithmetic_is_ideal_not_native=True,
            q10_price_bias_lower_bound_proved=False,
            MPS_compression_or_quantum_loading_impossible=False,
            original_finite_BM_or_quantile_law_adopted=False,
            rows=rows,
        ),
    )
    save(
        output / "summary.json",
        dict(
            passed=True,
            local_only=True,
            scalar_grid_widths_screened=29,
            model_rows=2,
            q10_uniform_certificate_meets_fixed_law_budget=False,
            first_fixed_widths_passing=[24, 27],
            full_prefix_nodes_at_first_passing_widths=[(1 << 24) - 1, (1 << 27) - 1],
            complete_implementation_or_native_price_bridge_certified=False,
            actual_price_bias_lower_bound_or_impossibility_claim=False,
            current_BM_price_ledger_changed=False,
            new_tests_gates_financial_prices_or_replays=0,
        ),
    )
    manifest(output, protocol)
    print(
        "q10 uniform law bound rejected; first fitting fixed widths24/27; no adoption", flush=True
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output.resolve())
