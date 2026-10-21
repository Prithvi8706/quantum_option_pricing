"""Independent exact audit of a conditional uniform-grid law upper bound.

No producer functions, observations, gate strings, or fixtures are executed.
The screen concerns ideal GBM with independent scalar inputs, not native BM.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from decimal import Decimal
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
SOURCE = PROGRAM / "A03_law_screen_run001"
CASES = (("B4x12", 60, 4, 12), ("B8x52", 468, 8, 52))
WIDTHS = list(range(4, 33))
EXP_DEGREE = 128
BUDGET = Fraction(1, 1000)
BV = Fraction(80)
CPU_LIMIT = 60


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"), parse_float=Decimal)


def create(path, value):
    with Path(path).open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def relative(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def pair(value):
    return [value.numerator, value.denominator]


def exact(value):
    assert isinstance(value, list) and len(value) == 2
    assert all(type(number) is int for number in value) and value[1] > 0
    answer = Fraction(*value)
    assert pair(answer) == value
    return answer


def verify(frozen):
    for name, expected in frozen.items():
        assert sha(ROOT / name) == expected, ("Frozen dependency changed", name)


def independent_pi_lower():
    """A finite alternating Machin enclosure; no producer/helper import."""
    sums = []
    for base in (5, 239):
        power, total = Fraction(1, base), Fraction(0)
        for k in range(20):
            total += (-1) ** k * power / (2 * k + 1)
            power /= base * base
        following = total + power / 41
        sums.append((total, following))
    return 16 * sums[0][0] - 4 * sums[1][1]


def independent_exp_lower():
    """Rational Horner recursion, separately from factorial summation."""
    value = Fraction(1)
    for degree in range(EXP_DEGREE, 0, -1):
        value = 1 + Fraction(18, degree) * value
    return value


def mathematical_proof(tail):
    pi_lower = independent_pi_lower()
    assert pi_lower > Fraction(25, 8)
    assert 0 < tail < Fraction(1, 100000000)
    # Check the affine conditional-CDF discrepancy at its two extrema.
    for continuous_cdf, desired in ((tail, -tail), (1 - tail, tail)):
        conditional_cdf = (continuous_cdf - tail) / (1 - 2 * tail)
        assert conditional_cdf - continuous_cdf == desired
    return dict(
        independent_Machin_pi_lower_exact=pair(pi_lower),
        Gaussian_peak_density_proof="pi>25/8 implies1/sqrt(2*pi)<2/5",
        Mills_tail_proof=(
            "For x>=6,1<=x/6. Thus Q(6)<=integral_6^infinity x*phi(x)/6 dx"
            "=phi(6)/6<exp(-18)/15. Every omitted positive term of exp(18)"
            " is nonnegative, so the rational Horner polynomial is a lower bound"
            " and its reciprocal supplies an upper bound."
        ),
        normalized_truncation_proof=(
            "Write q=Q(6). On[-6,6],F_T(x)=(F(x)-q)/(1-2q). Its difference"
            " from F is q*(2F-1)/(1-2q); because F lies in[q,1-q], its"
            " magnitude is at most q. Outside[-6,6] it is also at most q."
            " This is a one-sided-tail bound, not the two-sided2q mass."
        ),
        midpoint_CDF_proof=(
            "Binning conditional mass into uniform-x midpoints makes its"
            " discrete CDF at any x equal the conditional CDF at an adjacent"
            " bin edge at distance at most h/2. The density is at most"
            " phi(0)/(1-2q), so the discrepancy is at most"
            " phi(0)*h/[2*(1-2q)], including left/right limits at the atoms."
            " Triangle inequality and q<=q_upper then yield the saved KS upper."
        ),
        coordinate_BV_transfer=(
            "For a bounded-variation scalar observable, Stieltjes/step-function"
            " integration bounds an expectation difference by TV(f)*KS."
            " The original positive GBM coefficients make each coordinate payoff"
            " increase on a single survival half-line and then drop to zero."
            " Each discounted payoff lies in[0,40], so variation is at most80."
            " This bound is uniform in every other continuous or discrete driver."
            " Replacing independent scalar laws one at a time gives80*d*KS."
        ),
        clipping_to_40_reason=(
            "Both ideal original and alternative laws use the same strict"
            " monitored barrier and already-discounted payoff in[0,40]."
            " Their absolute expectation difference is also at most40."
        ),
        actual_price_bias_lower_bound=False,
        native_exp_clipping_and_payoff_arithmetic_included=False,
        paired_Box_Muller_outputs_assumed_independent=False,
    )


def prepare(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM)
    assert not output.exists()
    source_manifest = read(SOURCE / "manifest.json")
    frozen = {**source_manifest["files"], **source_manifest["frozen_inputs"]}
    frozen[relative(SOURCE / "manifest.json")] = sha(SOURCE / "manifest.json")
    own = Path(__file__).resolve()
    frozen[relative(own)] = sha(own)
    frozen[relative(Path(sys.executable))] = sha(sys.executable)
    verify(frozen)
    output.mkdir()
    snapshot = output / "executed_audit_binned_gaussian_law.py"
    snapshot.write_bytes(own.read_bytes())
    create(
        output / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            local_only=True,
            before_independent_law_formula_reconciliation=True,
            source_receipt=relative(SOURCE),
            frozen_inputs=frozen,
            executed_dependencies=[
                dict(original=relative(own), snapshot=snapshot.name, sha256=sha(snapshot))
            ],
            fixed_grid_bits=WIDTHS,
            fixed_truncation_exact=[6, 1],
            fixed_exp_Horner_polynomial_degree=EXP_DEGREE,
            independent_Machin_arctan_terms=20,
            fixed_cases=[
                dict(case=case, independent_drivers=drivers) for case, drivers, _, _ in CASES
            ],
            grid_law_bias_allowance_dollars_exact=pair(BUDGET),
            separate_preparation_bias_allowance_dollars_exact=pair(BUDGET),
            producer_functions_imported_or_executed=0,
            additional_fixture_test_credit=0,
            new_gates_financial_prices_or_replays=0,
            process_CPU_limit_seconds=CPU_LIMIT,
            law_loading_adoption=False,
        ),
    )
    print("A03 law-screen audit prospectively frozen", flush=True)


def run(output):
    started = time.process_time()
    output = Path(output).resolve()
    assert not (output / "summary.json").exists()
    protocol = read(output / "protocol.json")
    verify(protocol["frozen_inputs"])
    source_protocol = read(SOURCE / "protocol.json")
    assert source_protocol["before_conditional_law_and_tree_screen"] is True
    assert source_protocol["fixed_grid_bits"] == WIDTHS
    assert source_protocol["fixed_truncation_exact"] == [6, 1]
    assert source_protocol["positive_exp_lower_polynomial_degree"] == EXP_DEGREE
    assert source_protocol["explored_grid_law_bias_dollars_exact"] == pair(BUDGET)
    assert source_protocol["explored_preparation_bias_dollars_separate_exact"] == pair(BUDGET)
    assert source_protocol["two_distinct_allowances_not_double_spent"] is True
    assert source_protocol["budgets_not_adopted_in_current_BM_price_ledger"] is True
    assert source_protocol["original_ideal_GBM_coordinate_variation_upper_exact"] == pair(BV)
    assert source_protocol["new_tests_gates_financial_prices_or_replays"] == 0
    certificate = read(SOURCE / "certificate.json")
    tail = Fraction(1, 15) / independent_exp_lower()
    assert exact(certificate["one_sided_tail_probability_upper_exact"]) == tail
    proof = mathematical_proof(tail)
    assert certificate["underlying_GBM_arithmetic_is_ideal_not_native"] is True
    for field in (
        "q10_price_bias_lower_bound_proved",
        "MPS_compression_or_quantum_loading_impossible",
        "original_finite_BM_or_quantile_law_adopted",
    ):
        assert certificate[field] is False
    assert len(certificate["rows"]) == len(CASES)
    audited = []
    for row, (case, drivers, assets, dates) in zip(certificate["rows"], CASES):
        assert row["case"] == case and row["independent_driver_count"] == drivers
        original = read(PROGRAM / "C06_quantile_grid_run001" / (case + "_certificate.json"))
        assert original["normal_coordinates"] == drivers == (assets + 1) * dates
        assert exact(original["coordinate_total_variation_upper_dollars_exact"]) == BV
        model = original["original_model_binding"]
        assert model["assets"] == assets and model["dates"] == dates
        assert model["equal_asset_volatility"] is True
        assert exact(model["volatility_exact"]) == Fraction(3, 10)
        assert exact(model["correlation_exact"]) == Fraction(2, 5)
        assert exact(model["strike_dollars_exact"]) == 100
        assert exact(model["barrier_dollars_exact"]) == 140
        assert exact(model["rate_exact"]) == Fraction(3, 100)
        assert model["digital_paired_outputs_claimed_independent_gaussian"] is False
        assert original["accepted_Box_Muller_law_certified"] is False
        assert original["native_rounded_inverse_CDF_or_path_certified"] is False
        assert original["continuous_ideal_grid_law_certificate"] is True
        assert 2 * BUDGET < exact(original["headroom_exact"])
        assert len(row["candidates"]) == len(WIDTHS)
        first, reconstructed = None, []
        for candidate, bits in zip(row["candidates"], WIDTHS):
            spacing = Fraction(12, 2**bits)
            rounding = Fraction(1, 5) * spacing / (1 - 2 * tail)
            ks = tail + rounding
            dollars = BV * drivers * ks
            fits = dollars <= BUDGET
            if fits and first is None:
                first = bits
            assert candidate["grid_bits"] == bits
            assert exact(candidate["grid_spacing_exact"]) == spacing
            assert exact(candidate["scalar_CDF_distance_upper_exact"]) == ks
            assert exact(candidate["uniform_coordinate_BV_price_difference_upper_exact"]) == dollars
            assert exact(candidate["bounded_price_difference_upper_exact"]) == min(40, dollars)
            assert candidate["uniform_certificate_fits_grid_law_budget"] is fits
            assert candidate["complete_prefix_conditional_rotations"] == 2**bits - 1
            assert candidate["independent_draw_prefix_rotation_nodes"] == drivers * (2**bits - 1)
            assert candidate["remaining_conditional_angles_certified"] is False
            assert candidate["emitted_synthesized_full_loader"] is False
            reconstructed.append(
                dict(
                    grid_bits=bits,
                    scalar_KS_upper_exact=pair(ks),
                    price_formula_upper_exact=pair(dollars),
                    fits_fixed_law_budget=fits,
                    potential_prefix_nodes_per_driver=2**bits - 1,
                )
            )
        assert row["first_fixed_bits_passing_uniform_bound"] == first
        q10 = reconstructed[WIDTHS.index(10)]
        assert row["existing_q10_uniform_BV_certificate_rejected"] is True
        assert q10["fits_fixed_law_budget"] is False
        assert row["existing_q10_uniform_bound_exact"] == q10["price_formula_upper_exact"]
        audited.append(
            dict(
                case=case,
                independent_scalar_drivers=drivers,
                first_fixed_width_passing=first,
                q10=q10,
                rows=reconstructed,
            )
        )
    assert [row["first_fixed_width_passing"] for row in audited] == [24, 27]
    summary = read(SOURCE / "summary.json")
    assert summary["passed"] is True
    assert summary["scalar_grid_widths_screened"] == 29 and summary["model_rows"] == 2
    assert summary["first_fixed_widths_passing"] == [24, 27]
    assert summary["full_prefix_nodes_at_first_passing_widths"] == [2**24 - 1, 2**27 - 1]
    for field in (
        "q10_uniform_certificate_meets_fixed_law_budget",
        "complete_implementation_or_native_price_bridge_certified",
        "actual_price_bias_lower_bound_or_impossibility_claim",
        "current_BM_price_ledger_changed",
    ):
        assert summary[field] is False
    assert summary["new_tests_gates_financial_prices_or_replays"] == 0
    create(output / "independent_law_bound_proof.json", proof)
    create(output / "independent_grid_formula_rows.json", audited)
    verify(protocol["frozen_inputs"])
    assert time.process_time() - started < CPU_LIMIT
    create(
        output / "summary.json",
        dict(
            passed=True,
            local_only=True,
            fixed_widths_per_case=29,
            exact_formula_rows_reconciled=58,
            producer_fixtures_reexecuted=0,
            additional_fixture_test_credit=0,
            new_gates_financial_prices_or_replays=0,
            independent_rational_Horner_Mills_bound=True,
            conditional_normal_vs_full_normal_KS_is_one_sided_tail_bound=True,
            ideal_GBM_uniform_coordinate_BV_transfer_valid=True,
            first_fixed_widths_passing=[24, 27],
            q10_chosen_uniform_formula_meets_law_budget=False,
            separate_exploratory_law_and_preparation_dollars_exact=[pair(BUDGET), pair(BUDGET)],
            law_or_loading_allocation_adopted=False,
            actual_price_bias_lower_bound_or_MPS_impossibility=False,
            full_native_G2_or_implementation_certificate=False,
            accepted_Box_Muller_source_or_current_ledger_changed=False,
            elapsed_process_CPU_seconds=time.process_time() - started,
        ),
    )
    finish_manifest(output)
    print("A03 binned Gaussian law-screen independent audit PASS", flush=True)


def finish_manifest(output):
    create(
        output / "manifest.json",
        dict(
            files={relative(path): sha(path) for path in output.rglob("*") if path.is_file()},
            frozen_inputs=read(output / "protocol.json")["frozen_inputs"],
            manifest_self_hash_excluded=True,
        ),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, default=PROGRAM / "A03_law_screen_audit_run001")
    args = parser.parse_args()
    if args.phase == "prepare":
        prepare(args.output)
    else:
        try:
            run(args.output)
        except Exception as failure:
            output = args.output.resolve()
            (output / "failure.txt").write_text(traceback.format_exc(), encoding="utf-8")
            create(
                output / "summary.json",
                dict(
                    passed=False,
                    local_only=True,
                    failure_type=type(failure).__name__,
                    message=str(failure),
                    additional_fixture_test_credit=0,
                    new_gates_financial_prices_or_replays=0,
                    accepted_Box_Muller_source_or_current_ledger_changed=False,
                ),
            )
            finish_manifest(output)
            raise
