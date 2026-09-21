"""Independent integer and phase-sensitive tests of emitted residual gates."""

import cmath
import json
import random
from itertools import product
from pathlib import Path

import pytest

from research.journal_sprint.reversible_fixed_point import Program, basis
from research.stronger_arithmetic.residual_circuits import (
    clean_control,
    clean_shifted_residual,
    residual_payoff_flag,
    residual_program,
)


def signed(value, width):
    value %= 2**width
    return value - 2**width if value >= 2 ** (width - 1) else value


def control_reference(delta, width, coefficients, f, reciprocal, scale):
    x = signed(signed(delta, width) * reciprocal // 2**f, width)
    y = coefficients[-1]
    for c in coefficients[-2::-1]:
        y = signed(x * y // 2**f + c, width)
    return signed(y * scale // 2**f, width)


def numerator_reference(delta, width, coefficients, f, reciprocal, scale, shift):
    control = control_reference(delta, width, coefficients, f, reciprocal, scale)
    return (max(signed(delta, width), 0) - control + shift) % 2**width


def evolve(gates, state):
    state = dict(state)
    for gate in gates:
        assert 1 <= len(gate) <= 3 and len(set(gate)) == len(gate)
        controls = sum(1 << b for b in gate[:-1])
        target = 1 << gate[-1]
        state = {(k ^ target if k & controls == controls else k): a for k, a in state.items()}
    return state


@pytest.mark.parametrize("width,f,reciprocal,scale", [(2, 0, 1, 1), (3, 1, 1, 3), (3, 2, 3, 2)])
@pytest.mark.parametrize("shifted", [False, True])
def test_all_signed_inputs_arbitrary_xor_outputs_and_clean_work(
    width, f, reciprocal, scale, shifted
):
    cs, shift = (1, -1, 1, 0, -1), 2 ** (width - 1) + 1
    p = Program(compact=True)
    delta, out = p.register(width), p.register(width)
    if shifted:
        clean_shifted_residual(p, delta, out, cs, f, reciprocal, scale, shift)
    else:
        clean_control(p, delta, out, cs, f, reciprocal, scale)
    for value, old in product(range(-(2 ** (width - 1)), 2 ** (width - 1)), range(2**width)):
        initial = basis(delta, value) | basis(out, old)
        expected = (
            numerator_reference(value, width, cs, f, reciprocal, scale, shift)
            if shifted
            else control_reference(value, width, cs, f, reciprocal, scale)
        )
        assert p.run(initial) == initial ^ basis(out, expected)


@pytest.mark.parametrize("selector_bits", [1, 3])
def test_unsigned_threshold_all_inputs_both_flags_no_truncation(selector_bits):
    cs, shift = (1, 0, 1, 0, -1), 5
    p, delta, selector, flag = residual_program(3, 1, cs, 1, 3, shift, selector_bits)
    saw_high_bit = False
    for value, u, bit in product(range(-4, 4), range(2**selector_bits), (0, 1)):
        numerator = numerator_reference(value, 3, cs, 1, 1, 3, shift)
        saw_high_bit |= numerator >= 4
        initial = basis(delta, value) | basis(selector, u) | (bit << flag)
        assert p.run(initial) == initial ^ (int(u < numerator) << flag)
    assert saw_high_bit  # comparison is unsigned and retains high numerator bits


def test_complete_g_coefficients_are_not_halved_again():
    p = Program()
    delta, out = p.register(4), p.register(4)
    # g=x/2, already encoded by the linear coefficient Q/2=1.
    clean_control(p, delta, out, (0, 1, 0, 0, 0), 1, 2, 2)
    for value in (-7, -5, -3, -1, 1, 3, 5, 7):
        assert p.run(basis(delta, value)) == basis(delta, value) | basis(out, value // 2)


def test_no_overflow_reference_matches_physical_control_equations():
    # Q=4, dB=4: reciprocal=1 and scale=16 exactly.
    p = Program(compact=True)
    delta, out = p.register(7), p.register(7)
    cs = (1, 0, 1, 0, -1)
    clean_shifted_residual(p, delta, out, cs, 2, 1, 16, 8)
    for value in range(-8, 9):
        x = value // 4
        y = cs[-1]
        for c in cs[-2::-1]:
            y = x * y // 4 + c
        control = y * 16 // 4
        numerator = max(value, 0) - control + 8
        assert 0 <= numerator < 128
        assert p.run(basis(delta, value)) == basis(delta, value) | basis(out, numerator)


def test_coherent_control_and_shifted_xor_preserve_relative_phases():
    for emitter in (clean_control, clean_shifted_residual):
        p = Program()
        delta, out = p.register(3), p.register(3)
        cs = (1, -1, 1, 0, -1)
        args = (cs, 1, 1, 3) + ((5,) if emitter is clean_shifted_residual else ())
        emitter(p, delta, out, *args)
        state, expected = {}, {}
        for value, old in product(range(8), repeat=2):
            initial = basis(delta, value) | basis(out, old)
            amplitude = cmath.exp(0.37j * (8 * value + old)) / 8
            result = (
                numerator_reference(value, 3, cs, 1, 1, 3, 5)
                if emitter is clean_shifted_residual
                else control_reference(value, 3, cs, 1, 1, 3)
            )
            state[initial] = amplitude
            expected[initial ^ basis(out, result)] = amplitude
        actual = evolve(p.gates, state)
        assert actual == expected
        assert evolve(reversed(p.gates), actual) == state


def test_coherent_threshold_phase_kickback_and_full_dirty_inverse():
    cs = (1, -1, 1, 0, -1)
    p, delta, selector, flag = residual_program(3, 1, cs, 1, 3, 5, 2)
    state, expected = {}, {}
    for value, u, bit in product(range(8), range(4), (0, 1)):
        initial = basis(delta, value) | basis(selector, u) | (bit << flag)
        amplitude = (-1) ** bit * cmath.exp(0.19j * (4 * value + u)) / 8
        good = u < numerator_reference(value, 3, cs, 1, 1, 3, 5)
        state[initial] = amplitude
        expected[initial] = (-1) ** good * amplitude
    actual = evolve(p.gates, state)
    assert actual == expected
    assert evolve(reversed(p.gates), actual) == state
    rng = random.Random(28)
    dirty = {rng.getrandbits(p.qubits): cmath.exp(0.3j * i) / 4 for i in range(16)}
    p.undo(0)
    assert evolve(p.gates, dirty) == dirty


def test_program_wrapper_matches_direct_emission_and_actual_counts():
    args = ((1, 0, 1, 0, -1), 1, 1, 3, 5)
    p = Program()
    delta, selector, flag = p.register(3), p.register(3), p.register(1)[0]
    residual_payoff_flag(p, delta, selector, flag, *args)
    compact, a, b, c = residual_program(3, args[1], args[0], *args[2:])
    assert (delta, selector, flag) == (a, b, c)
    assert list(p.gates) == list(compact.gates)
    assert p.resources() == compact.resources()
    counts = p.resources()
    assert sum(counts[k] for k in ("x", "cx", "ccx")) == len(p.gates)
    assert counts["ccx"] > 0 and counts["logical_depth"] <= len(p.gates)


def test_production_48_24_matches_residual_certificate_evaluator():
    from research.stronger_arithmetic.budget import reduced_plan
    from research.stronger_arithmetic.residual import (
        Q,
        control_offset_certificate,
        evaluate_control_integer,
        residual_plan,
    )

    archive = (
        Path(__file__).resolve().parents[1]
        / "results/journal_sprint/normalization_approximation_v1/model.json"
    )
    low = json.loads(archive.read_text())["low_coefficients"]
    means, factor = [4.6], [[0.1]]
    offset = control_offset_certificate(
        means, factor, q=2, strike=100, radius=100, low_coefficients=low, offset=0, discount=1
    )
    parent = reduced_plan(
        means,
        factor,
        normal_bits=2,
        strike=100,
        degree=12,
        reductions=2,
        fraction_bits=24,
        width=48,
    )
    certificate = residual_plan(
        parent, means, factor, radius=100, low_coefficients=low, offset_certificate=offset
    )
    assert certificate["overflow_safe"], certificate["overflow_failures"]
    args = (
        certificate["control_coefficients"],
        24,
        certificate["reciprocal_integer"],
        certificate["control_scale_integer"],
    )
    samples = (-Q - 1, 0, Q + 1)
    for emitter, field in [
        (clean_control, "control_integer"),
        (clean_shifted_residual, "threshold_integer"),
    ]:
        p = Program(compact=True)
        delta, out = p.register(48), p.register(48)
        extra = (certificate["shift_integer"],) if emitter is clean_shifted_residual else ()
        emitter(p, delta, out, *args, *extra)
        for value in samples:
            expected = evaluate_control_integer(value + certificate["strike_sum"], certificate)
            initial = basis(delta, value) | basis(out, 7)
            assert p.run(initial) == initial ^ basis(out, expected[field])

    p, delta, selector, flag = residual_program(
        48,
        24,
        args[0],
        args[2],
        args[3],
        certificate["shift_integer"],
        certificate["selector_bits"],
    )
    expected = evaluate_control_integer(certificate["strike_sum"], certificate)
    threshold = expected["threshold_integer"]
    assert 0 < threshold < 1 << len(selector)
    for u, bit in [(threshold - 1, 0), (threshold, 1)]:
        initial = basis(selector, u) | (bit << flag)
        assert p.run(initial) == initial ^ (int(u < threshold) << flag)


@pytest.mark.parametrize(
    "changes",
    [
        {"coefficients": None},
        {"coefficients": ()},
        {"coefficients": (1, 2)},
        {"coefficients": (1, 0, 0, 0, 4)},
        {"coefficients": (1, 0, 0, 0, True)},
        {"f": True},
        {"f": -1},
        {"f": 3},
        {"reciprocal": 0},
        {"reciprocal": 4},
        {"reciprocal": True},
        {"scale": 0},
        {"scale": -1},
        {"scale": 1.5},
        {"shift": -1},
        {"shift": 8},
        {"shift": True},
    ],
)
def test_bad_constants_rejected_before_mutation(changes):
    p = Program()
    delta, out = p.register(3), p.register(3)
    args = dict(coefficients=(1, 0, 1, 0, -1), f=1, reciprocal=1, scale=3, shift=5)
    args.update(changes)
    with pytest.raises(ValueError):
        clean_shifted_residual(p, delta, out, **args)
    assert p.qubits == 6 and not p.gates


@pytest.mark.parametrize("selector_bits", [0, -1, True, 4, 1.5])
def test_bad_wrapper_selector_width(selector_bits):
    with pytest.raises(ValueError):
        residual_program(3, 1, (1, 0, 1, 0, -1), 1, 3, 5, selector_bits)


def test_aliases_unallocated_wires_and_width_mismatch():
    for delta, selector, flag in [
        ((0, 1), (1,), 3),
        ((0, 1), (2,), 1),
        ((0, 1), (2,), 4),
        ((0,), (1, 2), 3),
    ]:
        p = Program()
        p.register(4)
        with pytest.raises(ValueError):
            residual_payoff_flag(p, delta, selector, flag, (1, 0, 0, 0, 0), 0, 1, 1, 0)
        assert p.qubits == 4 and not p.gates
    p = Program()
    a, b = p.register(3), p.register(2)
    with pytest.raises(ValueError):
        clean_control(p, a, b, (1, 0, 0, 0, 0), 1, 1, 1)
    assert p.qubits == 5 and not p.gates
