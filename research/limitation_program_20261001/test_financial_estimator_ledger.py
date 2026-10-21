"""Reject incompatible estimator/source interfaces and hidden synthesis costs."""

from copy import deepcopy

import pytest

from research.limitation_program_20261001.financial_estimator_ledger import assemble_estimator_row


def fixtures():
    from research.limitation_program_20261001.financial_bounded_schedule import certified_schedule

    wrapper = dict(
        format="test source wrapper",
        binding=dict(case="test", dollar_span=64),
        probability_law="test exact support law",
        random_wires=list(range(4)),
        allowed_qpe_control_wires=list(range(47, 72)),
        resources=dict(
            t_count=700,
            t_depth=60,
            logical_qubits=100,
            qpe_controls_available_in_old_output_buffer=25,
            clifford_cx=900,
            clifford_h=200,
            clifford_cz=2,
            clifford_z=1,
            x=20,
        ),
    )
    return wrapper, certified_schedule()


def test_fresh_preparations_directions_and_unknown_costs_are_explicit():
    wrapper, schedule = fixtures()
    row = assemble_estimator_row(wrapper, schedule)
    assert row["fresh_preparations"] == row["serial_shots"] == 15
    assert row["financial_forwards"] == row["financial_literal_inverses"] == 983025
    assert row["source_graph_directions"] == 1966050
    assert row["qpe_register_wires"] == list(range(47, 63))
    assert (
        row["full_T_count"] is row["full_T_depth"] is row["full_physical_runtime_seconds"] is None
    )
    assert row["iqft_arbitrary_Rz_rotations"] > 0
    assert not row["second_discount_applied"]


@pytest.mark.parametrize("damage", ("span", "controls", "readout"))
def test_incompatible_contracts_fail_before_pricing_claim(damage):
    wrapper, schedule = fixtures()
    wrapper, schedule = deepcopy(wrapper), deepcopy(schedule)
    if damage == "span":
        wrapper["binding"]["dollar_span"] = 256
    elif damage == "controls":
        wrapper["resources"]["qpe_controls_available_in_old_output_buffer"] = 15
    else:
        schedule["ideal_error_upper_exact"] = schedule["statistical_error_dollars_exact"]
    with pytest.raises(ValueError):
        assemble_estimator_row(wrapper, schedule)
