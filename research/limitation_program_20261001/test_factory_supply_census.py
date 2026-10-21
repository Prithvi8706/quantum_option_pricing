"""Finite all-orders error, retry and source-interface accounting fixtures."""

from fractions import Fraction
from math import comb

import pytest

from research.limitation_program_20261001 import factory_supply_census as factory


@pytest.mark.parametrize(
    "t_count,ccx,residual",
    [
        (511911060861915, 73130151300300, 1759815),
        (4195204814583315, 599314973260500, 1759815),
    ],
)
def test_exact_current_demand_decomposition_and_union_targets(t_count, ccx, residual):
    result = factory.state_targets(t_count, ccx, residual)
    assert t_count == 7 * ccx + residual
    assert Fraction(*result["unchanged_T_state_error_target_exact"]) * t_count == Fraction(1, 1000)
    native = result["native_interface"]
    assert ccx * Fraction(*native["required_each_CCZ_error_upper_exact"]) == Fraction(1, 2000)
    assert residual * Fraction(*native["required_each_residual_T_error_upper_exact"]) == Fraction(
        1, 2000
    )


def test_bad_native_decomposition_cannot_eliminate_arbitrary_rotations():
    with pytest.raises(ValueError, match="inventory mismatch"):
        factory.state_targets(100, 14, 1)


@pytest.mark.parametrize("inputs,distance", [(15, 3), (8, 2)])
def test_finite_all_orders_postselection_bound_dominates_full_binomial_tail(inputs, distance):
    p = Fraction(1, 1000)
    row = factory.detected_fault_bound(inputs, distance, p)
    acceptance = (1 - p) ** inputs
    tail = sum(
        (
            Fraction(comb(inputs, k)) * p**k * (1 - p) ** (inputs - k)
            for k in range(distance, inputs + 1)
        ),
        Fraction(),
    )
    bound = Fraction(*row["conditional_bad_output_upper_exact"])
    assert tail / acceptance <= bound == comb(inputs, distance) * p**distance / acceptance
    assert row["perfect_Clifford_operations_required"]
    assert row["independent_input_Z_faults_within_block_required"]
    assert not row["physical_factory_error_certificate"]


def test_rejected_attempts_are_charged_under_explicit_independent_retry_model():
    row = factory.detected_fault_bound(15, 3, Fraction(1, 1000))
    acceptance = Fraction(*row["acceptance_probability_lower_exact"])
    reject = Fraction(*row["rejected_attempt_probability_upper_exact"])
    assert acceptance + reject == 1
    assert Fraction(*row["expected_independent_attempts_per_accept_upper_exact"]) * acceptance == 1
    assert row["iid_retry_model_required_for_expected_attempt_bound"]


@pytest.mark.parametrize("value", [Fraction(0), Fraction(1, 3), Fraction(7, 10**40)])
def test_fixed_dyadic_rounding_encloses_upward(value):
    upper = factory.ceil_dyadic(value)
    assert value <= upper < value + Fraction(1, 1 << factory.ENCLOSURE_BITS)
    assert (upper * (1 << factory.ENCLOSURE_BITS)).denominator == 1


def test_one_fixed_three_level_cascade_is_a_conditional_ideal_statement():
    target = Fraction(1, 511911060861915000)
    result = factory.ideal_cascade(target)
    assert len(result["rows"]) == 3 and result["first_fixed_level_meeting_target"] == 3
    assert result["successive_disjoint_independent_input_blocks_required"]
    assert result["actual_Clifford_or_storage_fault_contribution"] is None
    assert not result["physical_factory_or_retry_rate_adopted"]
    p = factory.RAW_Z_ERROR
    for row in result["rows"]:
        raw = comb(15, 3) * p**3 / (1 - p) ** 15
        p = Fraction(*row["upward_dyadic_output_error_upper_exact"])
        assert raw <= p and row["upward_enclosure_bits"] == 192
        assert row["conditional_target_met"] == (p <= target)


def test_cascade_raw_input_accounting_includes_all_levels_and_retries():
    result = factory.ideal_cascade(Fraction(1, 10**18))
    expected = Fraction(1)
    for row in result["rows"]:
        expected = (
            15 * expected / Fraction(*row["ideal_bound"]["acceptance_probability_lower_exact"])
        )
        assert Fraction(*row["expected_raw_input_consumption_upper_exact"]) == expected
        assert expected > 15 ** row["level"]


def test_leading_order_35_and_28_coefficients_are_not_used_as_finite_certificates():
    p = Fraction(1, 1000)
    fifteen = factory.detected_fault_bound(15, 3, p)
    eight = factory.detected_fault_bound(8, 2, p)
    assert Fraction(*fifteen["conditional_bad_output_upper_exact"]) > 35 * p**3
    assert Fraction(*eight["conditional_bad_output_upper_exact"]) > 28 * p**2


def test_catalysis_conversion_consumes_additional_ccz_and_one_correlated_seed():
    result = factory.state_targets(511911060861915, 73130151300300, 1759815)
    row = result["optional_catalysis_interface"]
    assert row["additional_CCZ_states_consumed_to_supply_residual_T"] == 879908
    assert row["total_consumed_CCZ_states"] == 73130151300300 + 879908
    assert row["initial_T_catalyst_states"] == row["unused_last_output_T_states"] == 1
    assert not row["independent_catalyzed_T_outputs_assumed"]
    assert not row["independent_distillation_input_compatibility"]
    assert row["complete_magic_failure_upper"] is None


def test_census_has_exactly_two_h05_methods_and_one_conditional_h06_category():
    result = factory.census()
    assert result["H05_factory_methods"] == 2
    assert result["H06_additional_conditional_interface_categories"] == 1
    assert [r["method"] for r in result["method_rows"]] == list(factory.PAPERS)
    assert result["primary_H05_case"] == "B4x12"
    assert result["physical_architectures_admitted"] == 0 and not result["full_G5_closed"]
    assert not result["B8_physical_factory_profile_or_supply_comparison_performed"]
    for row in result["method_rows"]:
        assert all(row[field] is None for field in factory.PHYSICAL_FIELDS)
    cultivation = result["method_rows"][1]
    assert cultivation["reported_escaped_estimates_below_required_target"] == [False, False]
    assert cultivation["sign_entangling_erratum_requires_corrected_circuit_verification"]
    assert cultivation["distance_three_T_to_S_proxy_is_assumption_not_general_error_theorem"]
    assert not cultivation["ungrown_low_error_row_is_usable_output"]


@pytest.mark.parametrize("case", ["B4x12", "B8x52"])
def test_existing_demand_and_iqft_audit_bindings_preserve_all_terminal_t_states(case):
    result = factory.demand_binding(case)
    assert result["primitive_T_inventory_and_exact_seven_T_interface_reconciled"]
    assert result["native_interface"]["remaining_terminal_IQFT_T_states"] == 1759815
    assert not result["native_interface"]["native_CCX_replacement_compiled"]
    assert not result["native_interface"]["arbitrary_T_rotations_removed"]


def test_primary_artifacts_match_read_only_fetch_provenance():
    folder = factory.ROOT / "research/limitation_program_20261001/factory_census_primary_20261002"
    rows = factory.read(folder / "fetch_manifest.json")
    assert len(rows) == 4
    for name, row in rows.items():
        assert row["primary_source"] and row["url"].startswith("https://arxiv.org/")
        assert row["bytes"] <= 1 << 20 and factory.digest(folder / name) == row["sha256"]
    latest = (folder / "cultivation_latest_record.html").read_text(encoding="utf-8")
    assert "2409.17595v1" in latest and "2409.17595v2" not in latest


def test_fixed_eight_to_ccz_bound_requires_input_quality_not_adopted_hardware():
    ideal = factory.detected_fault_bound(8, 2, factory.CCZ_INPUT_Z_ERROR)
    bound = Fraction(*ideal["conditional_bad_output_upper_exact"])
    b8 = factory.state_targets(4195204814583315, 599314973260500, 1759815)
    assert bound <= Fraction(*b8["native_interface"]["required_each_CCZ_error_upper_exact"])
    assert not ideal["physical_factory_error_certificate"]
