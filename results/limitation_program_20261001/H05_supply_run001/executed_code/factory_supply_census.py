"""Bounded H05 supply census and separate H06 conditional state interfaces."""

from fractions import Fraction
import hashlib
import json
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
MAGIC_ALLOWANCE = Fraction(1, 1000)
RAW_Z_ERROR = Fraction(1, 1000)
LEVELS = 3
ENCLOSURE_BITS = 192
CCZ_INPUT_Z_ERROR = Fraction(1, 1 << 33)
PAPER_DISTILLATION_ERROR = Fraction(45, 10**21)
CULTIVATION_ESCAPED_ERRORS = (Fraction(2, 10**9), Fraction(4, 10**11))
PAPERS = {
    "15-to-1": "https://arxiv.org/html/1905.06903v3",
    "cultivation-with-escape": "https://arxiv.org/html/2409.17595v1",
    "CCZ-and-catalysis-interface": "https://arxiv.org/html/1812.01238v3",
}
PHYSICAL_FIELDS = (
    "physical_noise_model_adopted",
    "actual_raw_state_error_bound",
    "finite_code_distances_adopted",
    "accepted_usable_output_error_upper_bound",
    "accepted_output_rate_per_second",
    "rejected_attempt_rate",
    "physical_factory_qubits",
    "data_storage_physical_qubits",
    "routing_and_buffer_physical_qubits",
    "usable_output_transport_error",
    "cycle_seconds",
    "decoder_and_feedback_seconds",
    "measurement_reaction_depth",
    "physical_qubit_cap",
    "executable_latency_seconds",
    "complete_physical_failure_upper_bound",
)


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1 << 20):
            value.update(block)
    return value.hexdigest()


def pair(value):
    value = Fraction(value)
    return [value.numerator, value.denominator]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def ceil_dyadic(value, bits=ENCLOSURE_BITS):
    value = Fraction(value)
    require(
        value >= 0 and type(bits) is int and bits >= 1,
        "Nonnegative value/positive precision required",
    )
    scaled = value * (1 << bits)
    return Fraction(-(-scaled.numerator // scaled.denominator), 1 << bits)


def detected_fault_bound(inputs, minimum_bad_faults, input_error):
    """Perfect Clifford circuit, independent input Z faults, accepted outputs.

    A bad accepted output needs at least d faulty inputs. The union of all
    d-subsets bounds this event by C(n,d)*p**d. A no-fault attempt is accepted,
    so P(accept)>= (1-p)**n. This is all orders, not the leading coefficient.
    """
    p = Fraction(input_error)
    require(
        type(inputs) is int
        and type(minimum_bad_faults) is int
        and 1 <= minimum_bad_faults <= inputs
        and 0 <= p < 1,
        "Invalid ideal detected-fault parameters",
    )
    acceptance = (1 - p) ** inputs
    conditional = min(
        Fraction(1), Fraction(comb(inputs, minimum_bad_faults)) * p**minimum_bad_faults / acceptance
    )
    return dict(
        input_Z_error_upper_exact=pair(p),
        acceptance_probability_lower_exact=pair(acceptance),
        rejected_attempt_probability_upper_exact=pair(1 - acceptance),
        conditional_bad_output_upper_exact=pair(conditional),
        expected_independent_attempts_per_accept_upper_exact=pair(1 / acceptance),
        perfect_Clifford_operations_required=True,
        independent_input_Z_faults_within_block_required=True,
        iid_retry_model_required_for_expected_attempt_bound=True,
        physical_factory_error_certificate=False,
    )


def ideal_cascade(target):
    target = Fraction(target)
    require(0 < target < 1, "Probability target required")
    p, raw_cost, rows = RAW_Z_ERROR, Fraction(1), []
    for level in range(1, LEVELS + 1):
        row = detected_fault_bound(15, 3, p)
        acceptance = Fraction(*row["acceptance_probability_lower_exact"])
        unrounded = Fraction(*row["conditional_bad_output_upper_exact"])
        p = ceil_dyadic(unrounded)
        raw_cost = 15 * raw_cost / acceptance
        rows.append(
            dict(
                level=level,
                ideal_bound=row,
                upward_dyadic_output_error_upper_exact=pair(p),
                upward_enclosure_bits=ENCLOSURE_BITS,
                expected_raw_input_consumption_upper_exact=pair(raw_cost),
                conditional_target_met=p <= target,
            )
        )
    return dict(
        input_Z_error_exact=pair(RAW_Z_ERROR),
        maximum_fixed_levels=LEVELS,
        rows=rows,
        first_fixed_level_meeting_target=next(
            (r["level"] for r in rows if r["conditional_target_met"]), None
        ),
        actual_Clifford_or_storage_fault_contribution=None,
        independent_fresh_blocks_and_retries_required=True,
        successive_disjoint_independent_input_blocks_required=True,
        physical_factory_or_retry_rate_adopted=False,
    )


def state_targets(t_count, native_ccx, residual_t):
    require(
        all(type(value) is int and value > 0 for value in (t_count, native_ccx, residual_t))
        and t_count == 7 * native_ccx + residual_t,
        "Exact seven-T CCX/residual inventory mismatch",
    )
    half = MAGIC_ALLOWANCE / 2
    conversion_ccz = (residual_t + 1) // 2
    return dict(
        unchanged_T_state_demand=t_count,
        unchanged_T_state_error_target_exact=pair(MAGIC_ALLOWANCE / t_count),
        unchanged_T_state_union_charge_at_target_exact=pair(MAGIC_ALLOWANCE),
        native_interface=dict(
            arithmetic_and_selector_reflection_CCZ_states=native_ccx,
            remaining_terminal_IQFT_T_states=residual_t,
            prospective_CCZ_failure_allocation_exact=pair(half),
            prospective_residual_T_failure_allocation_exact=pair(half),
            required_each_CCZ_error_upper_exact=pair(half / native_ccx),
            required_each_residual_T_error_upper_exact=pair(half / residual_t),
            summed_magic_union_charge_at_targets_exact=pair(MAGIC_ALLOWANCE),
            native_CCX_replacement_compiled=False,
            arbitrary_T_rotations_removed=False,
            new_Clifford_measurement_control_or_routing_opportunities=None,
        ),
        optional_catalysis_interface=dict(
            arithmetic_CCZ_states=native_ccx,
            additional_CCZ_states_consumed_to_supply_residual_T=conversion_ccz,
            total_consumed_CCZ_states=native_ccx + conversion_ccz,
            initial_T_catalyst_states=1,
            residual_T_states_delivered=2 * conversion_ccz,
            unused_last_output_T_states=2 * conversion_ccz - residual_t,
            independent_catalyzed_T_outputs_assumed=False,
            catalyst_fault_is_whole_algorithm_failure=True,
            independent_distillation_input_compatibility=False,
            conservative_whole_algorithm_first_fault_expression=(
                "seed_error + total_CCZ*CCZ_error + conversion_count*conversion_error "
                "+ catalyst_storage_error <= 1/1000"
            ),
            seed_error_upper=None,
            conversion_fault_upper=None,
            catalyst_storage_error_upper=None,
            complete_magic_failure_upper=None,
        ),
    )


def demand_binding(case):
    demand_path = PROGRAM / "H17_demand_run002" / case / "hardware_demand.json"
    audit_path = PROGRAM / "E02_IQFT_audit_run001" / (case + "_IQFT_audit.json")
    hardware_audit = PROGRAM / "H17_demand_audit_run001/summary.json"
    require(read(hardware_audit)["passed"], "Independent hardware audit failed")
    demand, audit = read(demand_path), read(audit_path)
    require(
        audit["passed"] and audit["full_T_count"] == demand["consumed_T_states"],
        "IQFT total demand mismatch",
    )
    counts = audit["independently_reconstructed_complete_primitive_counts"]
    require(counts["t"] == demand["consumed_T_states"], "Primitive T-state demand mismatch")
    native = demand["native_CCX_positions_before_exact_seven_T_expansion"]
    residual = demand["remaining_single_qubit_T_positions_in_terminal_IQFT"]
    gate_counts = audit["iqft_per_shot_physical_gate_counts"]
    require(
        residual == audit["serial_fresh_shots"] * (gate_counts["t"] + gate_counts["tdg"]),
        "Residual IQFT T/Tdag states not fully charged",
    )
    targets = state_targets(demand["consumed_T_states"], native, residual)
    recorded = demand["failure_requirements"]
    require(
        recorded["allocation_exact"]["magic_states"] == pair(MAGIC_ALLOWANCE),
        "Magic failure allocation changed",
    )
    require(
        recorded["required_error_per_consumed_T_state_exact"]
        == targets["unchanged_T_state_error_target_exact"],
        "Demand state quality target changed",
    )
    return dict(
        case=case,
        demand_path=demand_path.relative_to(ROOT).as_posix(),
        demand_sha256=digest(demand_path),
        independent_IQFT_audit_path=audit_path.relative_to(ROOT).as_posix(),
        independent_IQFT_audit_sha256=digest(audit_path),
        primitive_T_inventory_and_exact_seven_T_interface_reconciled=True,
        physical_failure_requirements=recorded,
        logical_qubits=demand["logical_qubits"],
        source_compatible=True,
        **targets,
    )


def census():
    cases = {case: demand_binding(case) for case in ("B4x12", "B8x52")}
    b4 = cases["B4x12"]
    target = Fraction(*b4["unchanged_T_state_error_target_exact"])
    baseline = dict(
        method="15-to-1",
        roadmap_item="H05",
        compatible_output_type="T or Clifford-corrected Tdag state",
        primary=PAPERS["15-to-1"],
        primary_sections="Table1; Sections2-4",
        computation_gate_lowering_unchanged=True,
        published_model_row=dict(
            label="(15-to-1)_{17,7,7}^6 x (15-to-1)_{41,17,17}",
            physical_circuit_noise_estimate_exact=[1, 1000],
            reported_output_error_estimate_exact=pair(PAPER_DISTILLATION_ERROR),
            reported_physical_footprint_qubits=73400,
            reported_code_cycles_per_output_estimate=128,
            reported_error_is_a_proved_device_upper_bound=False,
        ),
        reported_error_estimate_below_required_target=PAPER_DISTILLATION_ERROR <= target,
        conditional_union_charge_if_reported_error_were_valid_upper_exact=pair(
            b4["unchanged_T_state_demand"] * PAPER_DISTILLATION_ERROR
        ),
        fixed_ideal_input_Z_cascade=ideal_cascade(target),
        published_rate_or_footprint_adopted=False,
        **{field: None for field in PHYSICAL_FIELDS},
    )
    cultivation = dict(
        method="cultivation-with-escape",
        roadmap_item="H05",
        compatible_output_type="T state after usable-code escape",
        primary=PAPERS["cultivation-with-escape"],
        primary_sections="Figure2; Sections2.4-2.6,3.2,4",
        latest_arxiv_index_version="v1",
        retrieved_HTML_date="August 24, 2026",
        computation_gate_lowering_unchanged=True,
        escaped_published_output_error_estimates_exact=list(map(pair, CULTIVATION_ESCAPED_ERRORS)),
        reported_escaped_estimates_below_required_target=[
            p <= target for p in CULTIVATION_ESCAPED_ERRORS
        ],
        escaped_estimates_include_grafting=True,
        ungrown_low_error_row_is_usable_output=False,
        distance_three_T_to_S_proxy_is_assumption_not_general_error_theorem=True,
        sign_entangling_erratum_requires_corrected_circuit_verification=True,
        extrapolated_lower_error_certificate=None,
        paper_decoder_latency_adopted=False,
        published_rate_or_footprint_adopted=False,
        **{field: None for field in PHYSICAL_FIELDS},
    )
    ccz = dict(
        method="CCZ-and-catalysis-interface",
        roadmap_item="H06",
        primary=PAPERS["CCZ-and-catalysis-interface"],
        primary_sections="Sections2-3; Figures5-8",
        current_seven_T_lowering_source_compatible=False,
        replacement_requires_native_CCX_and_Clifford_mapping=True,
        controlled_and_literal_inverse_cases_must_be_validated=True,
        injected_CCZ_measurement_and_classical_Clifford_corrections_paid=None,
        one_fixed_ideal_eight_to_CCZ_input_Z_error_exact=pair(CCZ_INPUT_Z_ERROR),
        one_fixed_ideal_eight_to_CCZ_bound=detected_fault_bound(8, 2, CCZ_INPUT_Z_ERROR),
        catalysis_cannot_reuse_same_CCZ_for_arithmetic_and_T_outputs=True,
        catalysis_error_correlations_and_poisoning_retained=True,
        accepted_native_replacement_or_factory=False,
        **{field: None for field in PHYSICAL_FIELDS},
    )
    return dict(
        passed=True,
        local_only=True,
        primary_H05_case="B4x12",
        H05_factory_methods=2,
        H06_additional_conditional_interface_categories=1,
        demand_cases=cases,
        method_rows=[baseline, cultivation, ccz],
        only_H05_B4_fixed_supply_comparison_performed=True,
        B8_physical_factory_profile_or_supply_comparison_performed=False,
        physical_architectures_admitted=0,
        exact_failure_ledger_uses_marginal_union_bounds_without_global_independence=True,
        ideal_distillation_independence_and_perfect_Cliffords_not_device_claims=True,
        no_archived_C4_H8_cap_clock_or_factory_parameters_transferred=True,
        logical_T_depth_to_executable_time_conversion=False,
        full_G5_closed=False,
        next_eligible_supply_calculation=dict(
            case="B4x12",
            method="15-to-1",
            fixed_published_model_candidate=baseline["published_model_row"]["label"],
            reason=(
                "Reported modeled output quality is arithmetically compatible; "
                "adopted device quality remains unproved"
            ),
            next=(
                "Match a finite noise/input-error model and factory rejection/output process, "
                "verify usable delivered-state error, then size accepted supply/buffering "
                "for the actual batch profile with data and routing protected simultaneously"
            ),
            **{field: None for field in PHYSICAL_FIELDS},
        ),
        new_financial_prices_gate_replays_or_factory_simulations=0,
    )
