"""Count identities, paid native interfaces, fault targets and honest latency bounds."""

from collections import Counter
from copy import deepcopy
from fractions import Fraction

import pytest

from research.limitation_program_20261001.checkpoint_circuit import fingerprint
from research.limitation_program_20261001.hardware_demand import (
    ALLOCATIONS,
    PHYSICAL_ALLOWANCE,
    assess_error_proposal,
    bottleneck_lower_bound,
    complete_price_demand,
    exact,
    expanded_native_counts,
    iqft_token_counts,
    pair,
    source_batch_profile,
)


def _cost(x, cx, ccx, td, ctd, **extra):
    h, cz, z = (extra.get(name, 0) for name in ("h", "cz", "z"))
    return {
        "source_gates": x + cx + ccx + h + cz + z,
        "x": x,
        "cx": cx,
        "ccx": ccx,
        "t_count": 7 * ccx,
        "clifford_cx": cx + 6 * ccx,
        "clifford_h": h + 2 * ccx,
        "t_depth": td,
        "clifford_t_depth": ctd,
        **extra,
    }


@pytest.fixture
def context():
    source = {
        "word_width": 4,
        "values": 4,
        "inputs": [{"out": [0]}],
        "outputs": {"Y": 3},
        "forward_calls": [
            {"leaf": "lookup", "args": [0], "out": [1, 2]},
            {"leaf": "add", "args": [1, 1], "out": [3]},
        ],
    }
    native = {
        "lookup": {"forward": _cost(1, 2, 1, 3, 12), "inverse": _cost(1, 2, 1, 3, 13)},
        "add": {"forward": _cost(0, 1, 2, 6, 20), "inverse": _cost(0, 1, 2, 7, 21)},
    }
    metadata = {
        "lookup": {
            "args": [list(range(4))],
            "outs": [list(range(4, 8)), list(range(8, 12))],
            "resources": {"qubits": 13, **native["lookup"]["forward"]},
        },
        "add": {
            "args": [list(range(4)), list(range(4, 8))],
            "outs": [list(range(8, 12))],
            "resources": {"qubits": 13, **native["add"]["forward"]},
        },
    }
    groups = [
        {"wave": 1, "call_indices": [0], "private_scratch_qubits": 11, "copy_rounds": 1},
        {"wave": 2, "call_indices": [1], "private_scratch_qubits": 9, "copy_rounds": 2},
    ]
    capped = {
        "widths": [1, 1, 1, 4],
        "offsets": [0, 1, 2, 3],
        "retained_ssa_qubits": 7,
        "groups": groups,
        "resources": {"logical_qubits": 22},
        "qubit_cap": 22,
    }
    financial = {
        "source_gates": 26,
        "x": 2,
        "cx": 18,
        "ccx": 6,
        "t_count": 42,
        "clifford_cx": 54,
        "clifford_h": 12,
        "t_depth": 19,
        "clifford_t_depth": 78,
    }
    unit = _cost(6, 18, 8, 23, 109, h=4, cz=2, z=1, clifford_cz=2, clifford_z=1, logical_qubits=22)
    wrapper = {
        "binding": {"case": "B4x12", "fixture": True},
        "source_fingerprint": fingerprint(source),
        "capped_fingerprint": fingerprint(capped),
        "private_base": 11,
        "financial_native_costs": native,
        "financial_resources": financial,
        "selector_costs": {"forward": _cost(0, 0, 0, 0, 0), "inverse": _cost(0, 0, 0, 0, 0)},
        "reflection_resources": _cost(4, 0, 2, 4, 30, h=4, cz=1, z=1),
        "resources": unit,
        "random_wires": [0, 7],
        "financial_batches": [
            {
                "wave": 1,
                "copy_rounds": 1,
                "calls": [
                    {"call_index": 0, "leaf": "lookup", "private_base": 11, "private_width": 11}
                ],
            },
            {
                "wave": 2,
                "copy_rounds": 2,
                "calls": [{"call_index": 1, "leaf": "add", "private_base": 11, "private_width": 9}],
            },
        ],
    }
    operations = [
        {"gate": gate, "wires": wires}
        for gate, wires in (
            ("swap", [9, 10]),
            ("h", [9]),
            ("h", [10]),
            ("t", [9]),
            ("tdg", [10]),
            ("s", [9]),
            ("sdg", [10]),
            ("x", [10]),
            ("cz", [9, 10]),
        )
    ]
    row = {
        "binding": wrapper["binding"],
        "source_iterate_resources": unit,
        "controlled_grover_calls": 5,
        "serial_shots": 3,
        "source_graph_directions": 10,
        "financial_forwards": 5,
        "financial_literal_inverses": 5,
        "qpe_register_wires": [9, 10],
        "iqft_per_shot_physical_gate_counts": dict(Counter(op["gate"] for op in operations)),
        "full_T_count": 286,
        "full_T_depth": 121,
        "full_known_clifford_t_depth_upper": 600,
        "logical_qubits": 22,
        # Superseded partial fields deliberately disagree. Reusing them
        # alongside the complete IQFT recipe would double count these gates.
        "iqft_H": 1000,
        "iqft_exact_CS_T_count": 1000,
        "complete_known_T_count_excluding_arbitrary_rotation_synthesis": 1000,
    }
    return wrapper, source, capped, metadata, row, operations


def _demand(context):
    wrapper, source, capped, metadata, row, operations = context
    profile = source_batch_profile(wrapper, source, capped, metadata)
    return complete_price_demand(wrapper, row, operations, profile)


def test_seven_t_expansion_has_no_native_ccx_double_count():
    native = _cost(1, 2, 3, 10, 30, h=4, cz=2, z=1)
    assert expanded_native_counts(native) == {
        "x": 1,
        "cx": 20,
        "h": 10,
        "t": 21,
        "s": 0,
        "z": 1,
        "cz": 2,
    }
    assert sum(expanded_native_counts(native).values()) == 55


@pytest.mark.parametrize("field", ["source_gates", "t_count", "clifford_cx", "clifford_h"])
def test_changed_native_expansion_identity_is_rejected(field):
    native = _cost(1, 2, 3, 10, 30)
    native[field] += 1
    with pytest.raises(ValueError, match="identity changed"):
        expanded_native_counts(native)


def test_iqft_counts_include_all_tokens_and_expand_swaps(context):
    operations = context[-1]
    raw, expanded = iqft_token_counts(operations, [9, 10])
    assert raw["swap"] == 1 and raw["t"] == raw["tdg"] == 1
    assert expanded == {"x": 1, "cx": 3, "h": 2, "t": 2, "s": 2, "z": 0, "cz": 1}


@pytest.mark.parametrize(
    "operation",
    [
        {"gate": "rz", "wires": [9]},
        {"gate": "swap", "wires": [9, 9]},
        {"gate": "cx", "wires": [9, 22]},
        {"gate": "h", "wires": [9, 10]},
    ],
)
def test_iqft_rejects_unlowered_or_invalid_operations(operation):
    with pytest.raises(ValueError):
        iqft_token_counts([operation], [9, 10])


def test_atomic_outputs_and_full_native_high_scratch_are_paid(context):
    wrapper, source, capped, metadata, _, _ = context
    profile = source_batch_profile(wrapper, source, capped, metadata)
    first, second = profile["batches"]
    assert first["components"] == {
        "private_qubits": 11,
        "native_input_copy_register_qubits": 4,
        "native_internal_scratch_qubits": 1,
        "unused_native_high_output_scratch_qubits": 6,
        "active_output_qubits": 2,
        "active_argument_copy_bits": 1,
        "native_leaf_qubits": 13,
    }
    assert second["components"]["native_input_copy_register_qubits"] == 8
    assert second["components"]["private_qubits"] == 9
    assert profile["compiled_logical_qubits"] == 7 + 4 + 11 == 22
    assert profile["financial_resources_per_iterate"]["t_depth"] == 19


def test_repeated_ssa_arguments_get_distinct_native_copy_slots(context):
    wrapper, source, capped, metadata, _, _ = context
    profile = source_batch_profile(wrapper, source, capped, metadata)
    repeated = profile["batches"][1]
    assert repeated["shared_SSA_argument_occurrences"] == {"1": 2}
    assert repeated["max_shared_SSA_argument_occurrences"] == 2
    assert repeated["max_shared_SSA_copy_target_bits"] == 2
    assert repeated["argument_copy_CX_per_direction"] == 4
    assert repeated["resources"]["forward"]["clifford_t_depth"] == 24
    assert repeated["resources"]["inverse"]["clifford_t_depth"] == 25


@pytest.mark.parametrize(
    "fault",
    ["private", "copy_rounds", "leaf", "inverse_count", "native_alias", "coverage", "storage"],
)
def test_structural_financial_profile_forgeries_are_rejected(context, fault):
    wrapper, source, capped, metadata, _, _ = deepcopy(context)
    if fault == "private":
        wrapper["financial_batches"][0]["calls"][0]["private_width"] -= 1
    elif fault == "copy_rounds":
        wrapper["financial_batches"][1]["copy_rounds"] = 1
    elif fault == "leaf":
        wrapper["financial_batches"][0]["calls"][0]["leaf"] = "add"
    elif fault == "inverse_count":
        wrapper["financial_native_costs"]["add"]["inverse"]["ccx"] += 1
    elif fault == "native_alias":
        metadata["add"]["args"][1][0] = metadata["add"]["args"][0][0]
    elif fault == "coverage":
        wrapper["financial_batches"] = wrapper["financial_batches"][:1]
    else:
        capped["offsets"][1] += 1
        wrapper["capped_fingerprint"] = fingerprint(capped)
    with pytest.raises(ValueError):
        source_batch_profile(wrapper, source, capped, metadata)


def test_full_price_counts_include_fresh_preparations_and_iqft_once(context):
    demand = _demand(context)
    assert demand["primitive_elementary_gate_counts"] == {
        "x": 33,
        "cx": 339,
        "h": 118,
        "t": 286,
        "s": 6,
        "z": 5,
        "cz": 13,
    }
    assert demand["primitive_elementary_gate_count"] == 800
    assert demand["consumed_T_states"] == 286
    assert demand["native_CCX_positions_before_exact_seven_T_expansion"] == 40
    assert demand["remaining_single_qubit_T_positions_in_terminal_IQFT"] == 6
    assert demand["financial_graph_directions"] == 10
    assert demand["financial_batches_executed"] == 20
    assert demand["fresh_uniform_and_QPE_preparation_H"] == 12
    assert demand["measurement_reaction_depth"] is None
    assert demand["physical_qubit_cap"] is None and demand["architecture_rows"] == []


@pytest.mark.parametrize("fault", ["binding", "full_t", "iqft", "directions"])
def test_full_price_changed_recipe_or_multiplicity_is_rejected(context, fault):
    wrapper, source, capped, metadata, row, operations = deepcopy(context)
    if fault == "binding":
        row["binding"] = {"case": "different"}
    elif fault == "full_t":
        row["full_T_count"] += 1
    elif fault == "iqft":
        operations.pop()
    else:
        row["source_graph_directions"] += 1
    profile = source_batch_profile(wrapper, source, capped, metadata)
    with pytest.raises(ValueError):
        complete_price_demand(wrapper, row, operations, profile)


def test_failure_allocations_use_full_price_and_full_elementary_denominators(context):
    requirements = _demand(context)["failure_requirements"]
    assert sum(ALLOCATIONS.values()) == PHYSICAL_ALLOWANCE == Fraction(3, 1000)
    assert exact(requirements["required_error_per_consumed_T_state_exact"]) == Fraction(1, 286000)
    assert exact(requirements["required_data_error_per_elementary_logical_gate_exact"]) == Fraction(
        1, 800000
    )
    assert exact(
        requirements["required_control_error_per_elementary_logical_operation_exact"]
    ) == Fraction(1, 800000)
    assert requirements["idle_or_code_cycle_opportunity_count"] is None
    assert requirements["physical_control_reset_feedback_opportunity_count"] is None
    assert requirements["complete_execution_failure_upper"] is None


def test_passing_known_gate_targets_does_not_admit_unprotected_hardware(context):
    demand = _demand(context)
    result = assess_error_proposal(
        demand, Fraction(1, 286000), Fraction(1, 800000), Fraction(1, 800000)
    )
    assert all(result["known_operation_certificate_condition_passes"].values())
    assert result["hardware_admitted"] is None
    assert result["idle_code_cycles_and_control_feedback_remain_unproved"]
    assert not result["physical_runtime_certified"]


def test_factory_quality_failure_rejects_transfer_without_proving_true_failure(context):
    result = assess_error_proposal(_demand(context), Fraction(1, 100), 0, 0)
    assert result["hardware_admitted"] is False
    assert not result["known_operation_certificate_condition_passes"]["magic_states"]
    assert not result["failed_sufficient_union_condition_proves_actual_failure"]


def test_all_unknown_runtime_components_stay_null(context):
    result = bottleneck_lower_bound(_demand(context))
    assert result["lower_bound_seconds_exact"] is None
    assert all(value is None for value in result["conditional_terms_seconds_exact"].values())
    assert result["executable_latency_seconds"] is None


def test_populated_bottlenecks_are_a_lower_bound_even_when_every_term_is_known(context):
    result = bottleneck_lower_bound(
        _demand(context),
        reaction_depth=10,
        reaction_seconds=Fraction(1, 100),
        delivered_T_states_per_second=100,
        routing_seconds=3,
        other_dependency_seconds=2,
    )
    assert result["lower_bound_seconds_exact"] == pair(3)
    assert result["all_parameters_supplied"]
    assert not result["bound_is_an_executable_latency"]
    assert result["executable_latency_seconds"] is None


@pytest.mark.parametrize(
    "parameters",
    [
        {"reaction_depth": 10},
        {"reaction_seconds": [1, 100]},
        {"delivered_T_states_per_second": 0},
        {"routing_seconds": -1},
        {"reaction_depth": 10, "reaction_seconds": 0.001},
    ],
)
def test_incomplete_or_inexact_architecture_parameters_reject(parameters, context):
    with pytest.raises(ValueError):
        bottleneck_lower_bound(_demand(context), **parameters)


@pytest.mark.parametrize("value", [True, 0.1, [1, 0], [1.0, 2]])
def test_hardware_numeric_parameters_are_exact(value):
    with pytest.raises(ValueError):
        exact(value)
