"""Independent modular references and coherent checks of emitted gates."""

import cmath
import math
import random
from itertools import product

import pytest

from research.journal_sprint.reversible_fixed_point import (
    Program,
    affine,
    basis,
    horner,
    raw_payoff_flag as parent_payoff,
)
from research.stronger_arithmetic.circuits import (
    clean_exp,
    clean_row_sum,
    conversion_program,
    raw_payoff_flag,
)


def signed(value, width):
    value %= 2**width
    return value - 2**width if value >= 2 ** (width - 1) else value


def reference(x, coefficients, width, f, reductions, spot):
    reduced = signed(x, width) // 2**reductions
    y = coefficients[-1]
    for c in coefficients[-2::-1]:
        y = signed((reduced * y) // 2**f + c, width)
    for _ in range(reductions):
        y = signed((y * y) // 2**f, width)
    return (y * spot) % 2**width


def evolve(gates, state):
    """Sparse complex state evolution, preserving amplitudes and phases.

    Interpret the actual X/CX/CCX list independently of Program.run; no dense
    allocation across scratch wires and no probability-only comparison.
    """
    state = dict(state)
    for gate in gates:
        assert 1 <= len(gate) <= 3 and len(set(gate)) == len(gate)
        control = sum(1 << b for b in gate[:-1])
        target = 1 << gate[-1]
        state = {(k ^ target if k & control == control else k): a for k, a in state.items()}
    return state


@pytest.mark.parametrize("width,f", [(1, 0), (2, 0), (2, 1), (3, 1), (3, 2)])
@pytest.mark.parametrize("reductions,spot", [(0, 1), (1, 1), (2, 3), (4, 0), (1, 19)])
def test_exp_exhaustive_signed_and_arbitrary_output(width, f, reductions, spot):
    p = Program(compact=True)
    x, out = p.register(width), p.register(width)
    cs = (0, -1) if width == 1 else (1, -1, 1, 0)
    clean_exp(p, x, out, cs, f, reductions, spot)
    for value, old in product(range(-(2 ** (width - 1)), 2 ** (width - 1)), range(2**width)):
        initial = basis(x, value) | basis(out, old)
        expected = initial ^ basis(out, reference(value, cs, width, f, reductions, spot))
        assert p.run(initial) == expected  # includes EVERY scratch bit


def test_unreduced_is_exact_parent_gate_program():
    for cs in [(2,), (2, -1, 1), (2, -1, 0, 0)]:
        programs = [Program(compact=True), Program(compact=True)]
        for p, emitter in zip(programs, [horner, clean_exp]):
            x, out = p.register(3), p.register(3)
            if emitter is horner:
                emitter(p, x, out, cs, 1)
            else:
                emitter(p, x, out, cs, 1, 0, 1)
        assert programs[0].qubits == programs[1].qubits
        assert list(programs[0].gates) == list(programs[1].gates)


def test_exp_coherent_sparse_state_and_full_inverse():
    p = Program()
    x, out = p.register(3), p.register(3)
    cs = (2, 2, 1)
    clean_exp(p, x, out, cs, 1, 2, 3)
    state = {
        basis(x, v) | basis(out, old): cmath.exp(0.37j * (8 * v + old)) / 8
        for v, old in product(range(8), repeat=2)
    }
    expected = {
        k ^ basis(out, reference(v, cs, 3, 1, 2, 3)): state[k]
        for v, old in product(range(8), repeat=2)
        for k in [basis(x, v) | basis(out, old)]
    }
    actual = evolve(p.gates, state)
    assert actual == expected
    assert evolve(reversed(p.gates), actual) == state
    # A full gate inverse is identity even outside the clean-work subspace.
    rng = random.Random(71)
    dirty = {rng.getrandbits(p.qubits): cmath.exp(0.21j * i) / 4 for i in range(16)}
    assert evolve(reversed(p.gates), evolve(p.gates, dirty)) == dirty
    p.undo(0)
    assert evolve(p.gates, dirty) == dirty


@pytest.mark.parametrize("reductions,spot", [(0, 1), (1, 2)])
def test_conversion_interface_and_clean_scratch(reductions, spot):
    row, cs = (-2, (1, 3)), (2, 2, 1)
    p, inputs, log, out = conversion_program(2, 4, row, cs, 1, reductions, spot)
    assert inputs + log + out == tuple(range(10))
    for value in range(4):
        x = row[0] + sum(((value >> i) & 1) * c for i, c in enumerate(row[1]))
        expected = (
            basis(inputs, value)
            | basis(log, x)
            | basis(out, reference(x, cs, 4, 1, reductions, spot))
        )
        assert p.run(basis(inputs, value)) == expected
    p.undo(0)
    assert all(p.run(basis(inputs, v)) == basis(inputs, v) for v in range(4))


def test_conversion_default_matches_parent_affine_horner():
    p, inputs, log, out = conversion_program(2, 4, (-1, (2, -3)), (2, 2, 1), 1)
    parent = Program(compact=True)
    a, b, c = parent.register(2), parent.register(4), parent.register(4)
    affine(parent, a, b, -1, (2, -3))
    horner(parent, b, c, (2, 2, 1), 1)
    assert list(p.gates) == list(parent.gates)
    assert p.qubits == parent.qubits


@pytest.mark.parametrize("reductions,spot", [(0, 1), (1, 2)])
def test_row_sum_reuses_full_conversion_and_cleans(reductions, spot):
    rows, cs = ((-1, (1, -2)), (1, (-1, 2))), (2, 1)
    sizes = []
    for selected in [rows[:1], rows, rows * 2]:
        p = Program(compact=True)
        inputs, out = p.register(2), p.register(4)
        clean_row_sum(p, inputs, out, selected, cs, 1, reductions, spot)
        sizes.append((p.qubits, len(p.gates)))
        for value, previous in product(range(4), range(16)):
            total = sum(
                reference(
                    a + sum(((value >> i) & 1) * c for i, c in enumerate(coeff)),
                    cs,
                    4,
                    1,
                    reductions,
                    spot,
                )
                for a, coeff in selected
            )
            initial = basis(inputs, value) | basis(out, previous)
            assert p.run(initial) == basis(inputs, value) | basis(out, previous + total)
    assert sizes[0][0] == sizes[1][0] == sizes[2][0]
    assert sizes[1][1] > sizes[0][1]
    assert sizes[2][1] == 2 * sizes[1][1]


@pytest.mark.parametrize("reductions,spot", [(0, 1), (1, 2)])
def test_payoff_basis_coherent_phase_kickback_and_inverse(reductions, spot):
    p = Program(compact=True)
    inputs, selector, flag = p.register(1), p.register(3), p.register(1)[0]
    rows, cs, strike = ((0, (1,)), (1, (-1,))), (2, 1), 3
    raw_payoff_flag(p, inputs, selector, flag, 5, 1, rows, cs, strike, reductions, spot)
    coherent, expected = {}, {}
    for v, u in product(range(2), range(8)):
        payoff = max(
            sum(reference(a + v * c[0], cs, 5, 1, reductions, spot) for a, c in rows) - strike, 0
        )
        assert payoff < 8
        good = int(u < payoff)
        for bit in (0, 1):
            initial = basis(inputs, v) | basis(selector, u) | (bit << flag)
            assert p.run(initial) == initial ^ (good << flag)
            # |-> flag: compare phases of every amplitude, not probabilities.
            coherent[initial] = (-1) ** bit * cmath.exp(0.13j * (8 * v + u)) / math.sqrt(32)
            expected[initial] = (-1) ** good * coherent[initial]
    actual = evolve(p.gates, coherent)
    assert actual == expected
    assert evolve(reversed(p.gates), actual) == coherent
    if reductions == 0:
        parent = Program()
        a, b, c = parent.register(1), parent.register(3), parent.register(1)[0]
        parent_payoff(parent, a, b, c, 5, 1, rows, cs, strike)
        assert evolve(parent.gates, coherent) == actual
        assert p.qubits < parent.qubits


@pytest.mark.parametrize(
    "changes",
    [
        {"coefficients": ()},
        {"coefficients": None},
        {"coefficients": (True,)},
        {"coefficients": (4,)},
        {"coefficients": (-5,)},
        {"f": True},
        {"f": -1},
        {"f": 3},
        {"reductions": True},
        {"reductions": -1},
        {"reductions": 1.5},
        {"spot": -1},
        {"spot": 1.2},
        {"spot": True},
    ],
)
def test_exp_rejects_bad_parameters_without_mutation(changes):
    p = Program()
    x, out = p.register(3), p.register(3)
    args = dict(coefficients=(1, 1), f=1, reductions=1, spot=1)
    args.update(changes)
    with pytest.raises(ValueError):
        clean_exp(p, x, out, **args)
    assert p.qubits == 6 and not p.gates


@pytest.mark.parametrize(
    "x,out",
    [
        ((0, 1), (1, 2)),
        ((0, 0), (2, 3)),
        ((0, 1), (2, 4)),
        ((True, 1), (2, 3)),
        ((), (2, 3)),
        ((0,), (2, 3)),
    ],
)
def test_exp_rejects_invalid_registers(x, out):
    p = Program()
    p.register(4)
    with pytest.raises(ValueError):
        clean_exp(p, x, out, (1,), 0, 1, 1)
    assert p.qubits == 4 and not p.gates


@pytest.mark.parametrize(
    "rows", [(), None, ((1, ()),), ((True, (1,)),), ((0, (1.2,)),), ((1,),), ((1, None),)]
)
def test_row_validation_is_atomic(rows):
    p = Program()
    inputs, out = p.register(1), p.register(3)
    with pytest.raises(ValueError):
        clean_row_sum(p, inputs, out, rows, (1,), 1)
    assert p.qubits == 4 and not p.gates


@pytest.mark.parametrize(
    "changes",
    [
        {"width": True},
        {"width": 0},
        {"width": 1},
        {"fraction_bits": 4},
        {"strike_sum": -1},
        {"strike_sum": 8},
        {"strike_sum": True},
        {"affine_rows": ((0, ()),)},
        {"reductions": -1},
        {"spot": 1.5},
    ],
)
def test_payoff_validation_is_atomic(changes):
    p = Program()
    inputs, selector, flag = p.register(1), p.register(2), p.register(1)[0]
    args = dict(
        width=4, fraction_bits=1, affine_rows=((0, (1,)),), exp_coefficients=(2, 1), strike_sum=1
    )
    args.update(changes)
    with pytest.raises(ValueError):
        raw_payoff_flag(p, inputs, selector, flag, **args)
    assert p.qubits == 4 and not p.gates


@pytest.mark.parametrize("n,w", [(True, 4), (0, 4), (1, True), (1, 0)])
def test_conversion_validates_dimensions(n, w):
    with pytest.raises(ValueError):
        conversion_program(n, w, (0, (1,)), (2, 1), 1)
