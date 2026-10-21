"""Reuse exact-target archived Clifford/T strings for the current16-bit IQFT."""

from collections import Counter
from fractions import Fraction

from research.controlled_completion_followup.synthesis_rotations import interval_error_squared
from research.limitation_program_20261001.experiment_checkpoint import read


def verify_rotation_library(path, bits=16):
    if type(bits) is not int or not 3 <= bits <= 16:
        raise ValueError("the frozen retargeting covers3..16 IQFT bits")
    payload = read(path)
    epsilon = Fraction(*payload["common_operator_epsilon_exact"])
    records = {}
    for gap in range(2, bits):
        key = "pi_1_%d" % (1 << (gap + 1))
        original = payload["rotations"][key]
        spec = dict(kind="pi", numerator=1, denominator=1 << (gap + 1))
        if original["target"] != spec:
            raise ValueError("archived rotation has a different exact target")
        gates = original["matrix_product_gates"]
        if not gates or set(gates) - set("HTSXW"):
            raise ValueError("unsupported Clifford/T rotation token")
        squared = interval_error_squared(spec, gates, dps=120)
        if squared > epsilon**2 or squared > Fraction(original["frobenius_error_squared_upper"]):
            raise ValueError("archived rotation failed its independent interval matrix bound")
        if (
            gates.count("T") != original["t_count"]
            or sum(gates.count(x) for x in "HSX") != original["clifford_count"]
        ):
            raise ValueError("rotation gate count certificate disagrees with its string")
        records[key] = dict(
            target=spec,
            matrix_product_gates=gates,
            positive_execution_order="reverse string, omitting scalar W",
            negative_execution_order="forward string with daggered tokens, omitting scalar W",
            t_count=gates.count("T"),
            clifford_count=sum(gates.count(x) for x in "HSX"),
            global_w_count=gates.count("W"),
            physical_clifford_t_depth=len(gates) - gates.count("W"),
            operator_error_upper_exact=[epsilon.numerator, epsilon.denominator],
            frobenius_error_squared_upper_exact=[squared.numerator, squared.denominator],
            global_phase_scope=(
                "Uncontrolled single-qubit IQFT rotations; scalar W phases have no effect "
                "on QPE observation probabilities"
            ),
        )
    return records


def rz_operations(wire, gap, sign, records):
    if sign not in (-1, 1) or type(gap) is not int or gap < 1:
        raise ValueError("dyadic signed IQFT half-angle required")
    if gap == 1:
        return [dict(gate="t" if sign > 0 else "tdg", wires=[wire])]
    key = "pi_1_%d" % (1 << (gap + 1))
    string = records[key]["matrix_product_gates"]
    mapping = {"H": "h", "X": "x", "S": "s" if sign > 0 else "sdg", "T": "t" if sign > 0 else "tdg"}
    return [
        dict(gate=mapping[token], wires=[wire])
        for token in (reversed(string) if sign > 0 else string)
        if token != "W"
    ]


def iqft_operations(controls, records):
    if len(controls) < 2 or len(set(controls)) != len(controls):
        raise ValueError("distinct little-endian QPE wires required")
    operations = [
        dict(gate="swap", wires=[controls[j], controls[-1 - j]]) for j in range(len(controls) // 2)
    ]
    for j, target in enumerate(controls):
        for k in range(j):
            control, gap = controls[k], j - k
            # This product is CP(-pi/2**gap) up to a scalar phase. All three
            # Rz factors act unconditionally within the terminal IQFT.
            operations += rz_operations(control, gap, -1, records)
            operations += rz_operations(target, gap, -1, records)
            operations.append(dict(gate="cx", wires=[control, target]))
            operations += rz_operations(target, gap, 1, records)
            operations.append(dict(gate="cx", wires=[control, target]))
        operations.append(dict(gate="h", wires=[target]))
    return operations


def synthesized_row(row, records, recipe_path):
    bits = len(row["qpe_register_wires"])
    repetitions = row["serial_shots"]
    operations = iqft_operations(row["qpe_register_wires"], records)
    counts = Counter(operation["gate"] for operation in operations)
    usage = {"pi_1_%d" % (1 << (gap + 1)): repetitions * 3 * (bits - gap) for gap in range(2, bits)}
    if sum(usage.values()) != row["iqft_arbitrary_Rz_rotations"]:
        raise ValueError("source-compatible IQFT rotation usage mismatch")
    total_error = sum(
        (
            Fraction(*records[key]["operator_error_upper_exact"]) * count
            for key, count in usage.items()
        ),
        Fraction(0),
    )
    observation = 2 * total_error
    if observation > Fraction(*row["synthesis_observation_failure_allowance"]):
        raise ValueError("complete IQFT perturbation exceeds its failure allocation")
    synthesized_t = sum(records[key]["t_count"] * count for key, count in usage.items())
    synthesized_clifford = sum(
        records[key]["clifford_count"] * count for key, count in usage.items()
    )
    synthesized_ctd = synthesized_t + synthesized_clifford
    result = dict(row)
    result.update(
        schema="synthesized-source-compatible-bounded-estimator-ledger-v1",
        synthesis_certificate=str(recipe_path),
        synthesized_rotation_usage=usage,
        synthesized_single_qubit_T_count=synthesized_t,
        synthesized_single_qubit_clifford_count=synthesized_clifford,
        synthesis_total_observation_perturbation_upper_exact=[
            observation.numerator,
            observation.denominator,
        ],
        full_T_count=row["complete_known_T_count_excluding_arbitrary_rotation_synthesis"]
        + synthesized_t,
        full_T_depth=row["serial_known_T_depth_excluding_arbitrary_rotation_synthesis"]
        + synthesized_t,
        full_T_depth_convention=(
            "Valid conservative logical schedule: original financial batches, serial "
            "source/selector/reflection and serial terminal IQFT strings, serial fresh shots; "
            "physical routing/factory/readout time unproved"
        ),
        full_known_clifford_t_depth_upper=(
            repetitions
            * (
                ((1 << bits) - 1) * row["source_iterate_resources"]["clifford_t_depth"]
                + 1
                + 1
                + bits
                + 5 * (bits - 1)
                + 2 * (bits * (bits - 1) // 2 - (bits - 1))
                + 3 * (bits // 2)
            )
            + synthesized_ctd
        ),
        ideal_digital_estimator_with_synthesis_certificate=True,
        full_continuous_price_certificate=False,
        full_physical_execution_certificate=False,
        iqft_per_shot_physical_gate_counts=dict(counts),
        physical_runtime_seconds=None,
    )
    assert (
        repetitions * (counts["t"] + counts["tdg"]) == row["iqft_exact_CS_T_count"] + synthesized_t
    )
    return operations, result
