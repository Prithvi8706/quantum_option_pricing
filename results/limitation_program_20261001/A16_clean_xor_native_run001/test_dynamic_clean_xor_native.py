"""Bounded native channel, carry lifetime, phase and coherent-control checks."""

from dataclasses import replace
from itertools import product
import json
import os
from pathlib import Path

import numpy as np
import pytest

from research.controlled_source_completion.primitives import array_gates
from research.limitation_program_20261001.dynamic_clean_xor_adder import (
    measured_schedule as prior_w2,
)
from research.limitation_program_20261001.dynamic_clean_xor_native import (
    basis_macro_replay,
    build_channel,
    dense_branch,
    ideal_abstract_branch_scale,
    layout,
    macro_events,
    native_unitary_control,
    paid_resources,
    RecordNamespace,
    validate_primitives,
    verify_recipe,
)


def independent_logical_destination(word, width, controlled):
    mask = (1 << width) - 1
    a, b, old = word & mask, (word >> width) & mask, (word >> (2 * width)) & mask
    control = ((word >> (3 * width)) & 1) if controlled else 1
    output = old ^ (((a + b) & mask) if control else 0)
    return (word & ~((mask) << (2 * width))) | (output << (2 * width))


@pytest.mark.parametrize("controlled,outcome", product((False, True), (0, 1)))
def test_full_two_bit_primitive_branch_and_coherent_control_phase(controlled, outcome):
    program = build_channel(2, controlled)
    logical = 1 << program.layout.logical_qubits
    injection = np.zeros((1 << program.layout.qubits, logical), dtype=complex)
    injection[:logical] = np.eye(logical)
    actual = dense_branch(program, injection, (outcome,))
    target = np.zeros_like(injection)
    for word in range(logical):
        target[independent_logical_destination(word, 2, controlled), word] = 1 / np.sqrt(2)
    assert np.max(np.abs(actual - target)) < 1e-12
    assert np.max(np.abs(actual.conj().T @ actual - np.eye(logical) / 2)) < 1e-12


@pytest.mark.parametrize("outcomes", tuple(product((0, 1), repeat=3)))
def test_three_bit_carry_lifetimes_preserve_entangled_reference_and_phase(outcomes):
    program = build_channel(3)
    logical = 1 << program.layout.logical_qubits
    coefficients = np.asarray(
        [[complex(i + 1, (5 * i + j) % 17) for j in range(2)] for i in range(logical)]
    )
    coefficients /= np.linalg.norm(coefficients)
    injection = np.zeros((1 << program.layout.qubits, 2), dtype=complex)
    injection[:logical] = coefficients
    target = np.zeros_like(injection)
    for word in range(logical):
        target[independent_logical_destination(word, 3, False)] = coefficients[word] / np.sqrt(8)
    actual = dense_branch(program, injection, outcomes)
    assert np.max(np.abs(actual - target)) < 1e-12
    assert abs(np.linalg.norm(actual) ** 2 - 1 / 8) < 1e-12


def test_prior_w2_macro_contract_is_preserved_up_to_commuting_output_copy_order():
    # The new explicit generic copy orders p0,p1,c1 identically to the old toy.
    assert np.array_equal(build_channel(2).operations, prior_w2())


@pytest.mark.parametrize("width", (2, 3))
def test_exhaustive_small_dirty_words_and_new_adjoint_invocation(width):
    mask = (1 << width) - 1
    for controlled in (False, True):
        program = build_channel(width, controlled)
        inverse = program.adjoint(RecordNamespace.after(program))
        verify_recipe(program)
        verify_recipe(inverse)
        assert inverse.measurement_start == program.layout.measurements
        for a, b, old in product(range(mask + 1), repeat=3):
            for control in (0, 1) if controlled else (1,):
                output = basis_macro_replay(program, a, b, old, control)
                assert output == old ^ (((a + b) & mask) if control else 0)
                assert basis_macro_replay(inverse, a, b, output, control) == old
        with pytest.raises(TypeError, match="literal"):
            program.literal_reverse()


def fixed_native_pairs():
    mask = (1 << 72) - 1
    return (
        (0, 0),
        (mask, 1),
        (1 << 71, 1 << 71),
        (mask, mask),
        (int("55" * 9, 16), int("aa" * 9, 16)),
        ((1 << 40) - 1, 1),
    )


def primitive_unitary_basis(program, args, output, control_wire, a, b, old, control):
    bits = [0] * program.qubits
    for register, value in ((args[0], a), (args[1], b), (output, old)):
        for bit, wire in enumerate(register):
            bits[wire] = (value >> bit) & 1
    if control_wire is not None:
        bits[control_wire] = control
    before = list(bits)
    gates = array_gates(program)
    for kind, first, second, third in gates.tolist():
        if kind == 1:
            bits[first] ^= 1
        elif kind == 2:
            bits[second] ^= bits[first]
        else:
            bits[third] ^= bits[first] & bits[second]
    result = sum(bits[wire] << bit for bit, wire in enumerate(output))
    for wire in range(program.qubits):
        if wire not in output:
            assert bits[wire] == before[wire]
    for kind, first, second, third in gates[::-1].tolist():
        if kind == 1:
            bits[first] ^= 1
        elif kind == 2:
            bits[second] ^= bits[first]
        else:
            bits[third] ^= bits[first] & bits[second]
    assert bits == before
    return result


@pytest.fixture(scope="module")
def native_programs():
    programs = {mode: build_channel(72, mode) for mode in (False, True)}
    controls = {mode: native_unitary_control(72, mode) for mode in (False, True)}
    destination = os.environ.get("A16_NATIVE_ADD_EVIDENCE_PATH")
    if destination:
        out = Path(destination)
        out.mkdir()
        for mode, program in programs.items():
            name = "controlled" if mode else "uncontrolled"
            np.save(out / (name + "_dynamic.npy"), program.operations, allow_pickle=False)
            inverse = program.adjoint(RecordNamespace.after(program))
            np.save(out / (name + "_dynamic_adjoint.npy"), inverse.operations, allow_pickle=False)
            np.save(
                out / (name + "_control.npy"), array_gates(controls[mode][0]), allow_pickle=False
            )
        proof = {str(mode): verify_recipe(program) for mode, program in programs.items()}
        (out / "recipe_binding.json").write_text(
            json.dumps(proof, indent=2) + "\n", encoding="utf-8"
        )
    return programs, controls


def test_actual_native72_macro_contract_dirty_output_and_matched_unitary_arrays(native_programs):
    programs, controls = native_programs
    mask = (1 << 72) - 1
    for mode, program in programs.items():
        verify_recipe(program)
        inverse = program.adjoint(RecordNamespace.after(program))
        p, args, outs, control_wire = controls[mode]
        for a, b in fixed_native_pairs():
            for old in (0, mask, 1 << 71, int("55" * 9, 16)):
                for control in (0, 1) if mode else (1,):
                    dynamic = basis_macro_replay(program, a, b, old, control)
                    expected = old ^ (((a + b) & mask) if control else 0)
                    unitary = primitive_unitary_basis(
                        p, args, outs[0], control_wire, a, b, old, control
                    )
                    assert dynamic == unitary == expected
                    assert basis_macro_replay(inverse, a, b, dynamic, control) == old


def test_native_resources_pay_measurement_control_copy_and_record_namespace(native_programs):
    programs, _ = native_programs
    for controlled, tcount, slots in ((False, 564, 2687), (True, 1565, 4689)):
        program = programs[controlled]
        resources = paid_resources(program)
        assert (resources["T_count"], resources["fixed_serial_operation_slots"]) == (tcount, slots)
        assert resources["fresh_scratch"] == 284 and resources["retained_record_bits"] == 141
        assert resources["measurements"] == resources["feedback_CZ_slots"] == 141
        assert ideal_abstract_branch_scale(program).denominator == 1 << 141
        namespace = RecordNamespace.after(program)
        assert program.adjoint(namespace).measurement_start == 141
        assert program.adjoint(namespace).measurement_start == 282
        assert resources["full_financial_source_resources"] is None


def test_forged_phase_lifetime_and_disjoint_layout_are_rejected():
    program = build_channel(3)
    forged = program.operations.copy()
    first = next(i for i, row in enumerate(forged) if row[0] == 3)
    forged[first, 0] = 2
    with pytest.raises(ValueError, match="certified"):
        macro_events(replace(program, operations=forged))
    # Keeping a macro but changing a pre-copy CX changes carry lifetimes.
    forged = program.operations.copy()
    forged[0, 2] = program.layout.p[1]
    with pytest.raises(ValueError, match="recipe"):
        verify_recipe(replace(program, operations=forged))
    bad_layout = replace(program.layout, output=program.layout.a)
    with pytest.raises(ValueError, match="disjoint"):
        validate_primitives(replace(program, layout=bad_layout))


def test_bad_width_control_fresh_record_and_dense_allocation_are_rejected():
    for width in (1, 73, True, 2.0):
        with pytest.raises(ValueError, match="width"):
            layout(width)
    with pytest.raises(ValueError, match="bool"):
        layout(72, 1)
    for offset in (-1, True, 32767):
        with pytest.raises(ValueError, match="record"):
            build_channel(72, measurement_start=offset)
    with pytest.raises(ValueError, match="at most17"):
        dense_branch(build_channel(72), np.zeros((1, 1)), (0,) * 141)
    oversized_view = np.broadcast_to(np.zeros((1, 1)), (1 << 17, 9))
    with pytest.raises(ValueError, match="memory"):
        dense_branch(build_channel(3), oversized_view, (0,) * 3)
    with pytest.raises(ValueError, match="namespace"):
        build_channel(72).adjoint(RecordNamespace())
