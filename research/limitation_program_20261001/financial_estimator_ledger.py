"""Expand the source-compatible controlled iterate into a serial QPE schedule."""

from fractions import Fraction


def assemble_estimator_row(wrapper, schedule):
    if wrapper["binding"]["dollar_span"] != schedule["normalization_span_dollars"]:
        raise ValueError("Source normalization does not match the finite estimator")
    bits, repetitions, calls = (
        schedule["qpe_bits"],
        schedule["repetitions"],
        schedule["controlled_grover_calls"],
    )
    unit = wrapper["resources"]
    if bits > unit["qpe_controls_available_in_old_output_buffer"]:
        raise ValueError("Original output buffer cannot hold the complete QPE register")
    all_cp = repetitions * bits * (bits - 1) // 2
    exact_cp = repetitions * (bits - 1)
    rotations = 3 * (all_cp - exact_cp)
    # Use a conservative sum of operator errors, with factor two for total
    # observation variation. This is an obligation until synthesis is emitted.
    rotation_error = Fraction(1, 1000) / (2 * rotations) if rotations else Fraction(0)
    readout_error = Fraction(2, 1 << 40)
    certified_error = Fraction(*schedule["ideal_error_upper_exact"]) + readout_error
    statistical_allowance = Fraction(*schedule["statistical_error_dollars_exact"])
    if certified_error > statistical_allowance:
        raise ValueError("Finite dollar readout does not fit the statistical allowance")
    fixed_t = calls * unit["t_count"] + 3 * exact_cp
    fixed_td = calls * unit["t_depth"] + 3 * exact_cp
    n_random = len(wrapper["random_wires"])
    return dict(
        schema="source-compatible-bounded-estimator-invocation-ledger-v1",
        case=wrapper["binding"]["case"],
        binding=wrapper["binding"],
        wrapper_format=wrapper["format"],
        probability_law=wrapper["probability_law"],
        price_output_already_discounted=True,
        second_discount_applied=False,
        normalization_span_dollars=64,
        statistical_error_dollars_exact=schedule["statistical_error_dollars_exact"],
        ideal_failure_upper_exact=schedule["ideal_failure_upper_exact"],
        ideal_error_plus_readout_upper_exact=[
            certified_error.numerator,
            certified_error.denominator,
        ],
        classical_readout_error_allowance=[readout_error.numerator, readout_error.denominator],
        fresh_preparations=repetitions,
        financial_forwards=calls,
        financial_literal_inverses=calls,
        source_graph_directions=2 * calls,
        selector_forwards=calls,
        selector_literal_inverses=calls,
        controlled_predicate_CZ=calls,
        controlled_signed_reflections=calls,
        uniform_preparation_H=repetitions * n_random,
        qpe_preparation_H=repetitions * bits,
        iqft_H=repetitions * bits,
        iqft_controlled_phase_gates=all_cp,
        iqft_exact_CS_gates=exact_cp,
        iqft_exact_CS_T_count=3 * exact_cp,
        iqft_controlled_phase_CX=2 * all_cp,
        iqft_swaps_CX=3 * repetitions * (bits // 2),
        iqft_arbitrary_Rz_rotations=rotations,
        required_each_rotation_operator_error=[
            rotation_error.numerator,
            rotation_error.denominator,
        ],
        synthesis_observation_failure_allowance=[1, 1000],
        synthesis_certificate=None,
        measured_QPE_bits=repetitions * bits,
        source_and_selector_reset_bits=repetitions * n_random,
        qpe_reset_bits=repetitions * bits,
        additional_classical_controller_work=(
            "Exact interval sin-square decode for each outcome; median of the prices; "
            "new quantum inputs/preparation each repetition"
        ),
        adaptive_quantum_rounds=0,
        serial_shots=repetitions,
        longest_single_shot_grover_chain=schedule["M"] - 1,
        longest_single_shot_known_T_depth=(schedule["M"] - 1) * unit["t_depth"] + 3 * (bits - 1),
        complete_known_T_count_excluding_arbitrary_rotation_synthesis=fixed_t,
        serial_known_T_depth_excluding_arbitrary_rotation_synthesis=fixed_td,
        complete_known_clifford_CX=(
            calls * unit["clifford_cx"] + 2 * all_cp + 3 * repetitions * (bits // 2)
        ),
        complete_known_clifford_H=(
            calls * unit["clifford_h"] + repetitions * n_random + 2 * repetitions * bits
        ),
        complete_known_clifford_CZ=calls * unit["clifford_cz"],
        complete_known_clifford_Z=calls * unit["clifford_z"],
        complete_known_X=calls * unit["x"],
        financial_selector_reflection_T_depth=calls * unit["t_depth"],
        full_T_count=None,
        full_T_depth=None,
        source_iterate_resources=unit,
        logical_qubits=unit["logical_qubits"],
        qpe_register_wires=wrapper["allowed_qpe_control_wires"][:bits],
        total_readout_or_reset_seconds=None,
        full_physical_runtime_seconds=None,
        ideal_digital_mean_error_confidence_certificate=True,
        full_continuous_price_certificate=False,
        full_physical_execution_certificate=False,
        G2_to_G5="open",
    )
