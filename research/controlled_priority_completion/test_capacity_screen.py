"""Checks of capacity accounting and its finite-state boundary conditions."""

import math
import json

import pytest

from research.controlled_priority_completion.capacity_screen import (
    capacity_bound,
    certificate_distance,
    distillation_certificate,
    generate,
    magic_supply_bound,
    patch_qubits,
)
from research.controlled_priority_completion.capacity_revised import revised_rows, screen
from research.controlled_priority_completion import capacity_revised


def test_capacity_bound_is_work_over_available_lanes():
    # Three usable lanes; the fourth two-qubit lane does not fit seven qubits.
    assert capacity_bound(12, 7, 2, 0.25) == 1.0
    assert capacity_bound(12, 1, 2, 0.25) is None
    assert capacity_bound(0, 7, 2, 0.25) == 0.0
    with pytest.raises(ValueError):
        capacity_bound(-1, 7, 2, 0.25)


def test_surface_code_patch_counts_and_distance_certificate():
    assert patch_qubits(3) == 17
    assert patch_qubits(7) == 97
    with pytest.raises(ValueError):
        patch_qubits(2)
    loose = certificate_distance(600_000, 1, 1e-6, 1e-3)
    tight = certificate_distance(600_000, 1, 1e-9, 1e-3)
    assert tight["distance"] >= loose["distance"]
    assert tight["modeled_data_fault_union_bound"] <= 0.001
    assert not tight["fits_data_cap"]


def test_distillation_uses_all_orders_conditional_quality_bound():
    result = distillation_certificate(10**18, 1e-3)
    assert result["levels_sufficient_under_bound"] == 3
    assert result["total_accepted_error_union_bound"] <= 0.0005
    assert distillation_certificate(1, 1e-4)["levels_sufficient_under_bound"] == 0


def test_magic_supply_grants_prestored_inventory_and_omits_lower_stages():
    assert magic_supply_bound(100, 100, 3, 1e-6) == 0
    assert math.isclose(magic_supply_bound(200, 100, 3, 1e-6), 121 * 17 * 3e-6)


def test_archived_actual_schedule_fails_even_unencoded_nanosecond_work_screen():
    result = generate()
    assert len(result["rows"]) == 4
    for row in result["rows"]:
        assert row["minimum_distance_three_patch_qubits"] > result["physical_qubit_cap"]
        for contract in row["contract_screens"]:
            actual = contract["workload_screens"]["actual_arithmetic_T"]
            scenario = actual["sensitivity"][0]
            assert scenario["primitive_seconds"] == 1e-9
            assert scenario["physical_qubits_per_lane"] == 1
            assert not scenario["passes_necessary_work_screen"]
            assert actual["largest_per_lane_seconds_to_fit_with_one_physical_qubit_per_lane"] < 1e-9


def test_revised_native_ccx_count_excludes_exact_qft_t_rotations():
    bounded = dict(
        model="C4",
        allocation=dict(controlled_grover_calls=3),
        single_iterate_T_count=14,
        arithmetic_T_count=42 + 9,
        logical_qubits_upper=100,
        tenfold_total_budget_seconds=1,
    )
    row = revised_rows([], [bounded])[0]
    assert row["arithmetic_ccx"] == 6
    assert row["arithmetic_t"] == 51


def test_work_capacity_can_pass_for_improved_estimator_without_approving_full_price():
    row = dict(
        model="C4",
        method="synthetic_capacity_boundary",
        calls=1,
        arithmetic_t=10**15,
        arithmetic_ccx=10**14,
        allocated_qubits_upper=650_000,
        required_budget_seconds=1,
    )
    result = screen(row)
    assert result["contracts"][0]["free_data_free_factory_work_capacity"][0][
        "passes_necessary_screen"
    ]
    assert not result["allocated_rotated_patch_storage"][1]["fits_cap"]
    assert result["free_data_15_to_1_top_stage_supply"][0]["minimum_supply_seconds"] > 1


def test_financial_rebinding_counts_one_clean_oracle_and_checks_interface(tmp_path, monkeypatch):
    monkeypatch.setattr(capacity_revised, "ROOT", tmp_path)
    monkeypatch.setattr(capacity_revised, "BASE", tmp_path / "old")
    old = tmp_path / "old/compile_v2/C4_f40/source.json"
    new = tmp_path / "new/C4_f40/source.json"
    interface = dict(word_width=72, fraction_bits=40, inputs=[], outputs={"Y_6": 3})
    for path, resources in ((old, dict(t_count=98, ccx=14, logical_qubits=100)),
                            (new, dict(t_count=49, ccx=7, logical_qubits=80))):
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(dict(**interface, resources=resources)))
    row = dict(model="C4", calls=3, arithmetic_t=600, arithmetic_ccx=60,
               allocated_qubits_upper=123)
    result = capacity_revised.replace_financial_source(row, tmp_path / "new")
    assert result["arithmetic_t"] == 453
    assert result["arithmetic_ccx"] == 39
    assert result["allocated_qubits_upper"] == 103
    # Forward plus inverse is one clean source, not two clean source calls.
    assert row["arithmetic_t"] == 600
    invalid = json.loads(new.read_text())
    invalid["fraction_bits"] = 39
    new.write_text(json.dumps(invalid))
    with pytest.raises(ValueError, match="interface changed"):
        capacity_revised.replace_financial_source(row, tmp_path / "new")


def test_hadamard_mapping_uses_single_control_instead_of_prior_qpe_register():
    row = dict(model="C4", mode="test", allocation=dict(controlled_U_calls=10),
               arithmetic_T_count=700, single_U=dict(ccx=10, logical_qubits=200),
               logical_qubits_upper=179, tenfold_total_budget_seconds=1)
    assert revised_rows([row], [])[0]["allocated_qubits_upper"] == 179
