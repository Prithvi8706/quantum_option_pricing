from decimal import Decimal, localcontext
from itertools import product
import math

import pytest

from research.journal_sprint.reversible_fixed_point import (
    Program, add, affine, basis, fixed_multiply, horner, less_than, positive_part,
    raw_payoff_flag,
)
from research.journal_sprint.fixed_exp_budget import exp_budget, evaluate_integer
from research.journal_sprint.arithmetic_plan import raw_plan


@pytest.mark.parametrize("width", [1, 2, 3, 4])
def test_add_all_inputs_and_inverse(width):
    p = Program()
    a, b, helper = p.register(width), p.register(width), p.register(1)
    add(p, a, b, helper[0])
    for x, y in product(range(1 << width), repeat=2):
        initial = basis(a, x) | basis(b, y)
        assert p.run(initial) == basis(a, x) | basis(b, (x+y) % (1 << width))
    p.undo(0)
    assert all(p.run(v) == v for v in range(1 << p.qubits))


@pytest.mark.parametrize("width,fraction", [(2, 0), (2, 1), (3, 1), (3, 3), (4, 2)])
def test_signed_product_all_inputs_clean_scratch(width, fraction):
    p = Program()
    a, b, out = (p.register(width) for _ in range(3))
    scratch, partial, helper = p.register(2*width), p.register(2*width), p.register(1)
    fixed_multiply(p, a, b, out, fraction, scratch, partial, helper[0])
    for x, y in product(range(-(1 << (width-1)), 1 << (width-1)), repeat=2):
        initial = basis(a, x) | basis(b, y) | basis(out, 1)
        expected = initial ^ basis(out, (x*y // (1 << fraction)) % (1 << width))
        assert p.run(initial) == expected


@pytest.mark.parametrize("width", [1, 2, 3, 4])
def test_comparator_all_inputs_and_flag_states(width):
    p = Program()
    a, b, flag = p.register(width), p.register(width), p.register(1)
    d, e, h = p.register(width+1), p.register(width+1), p.register(1)
    less_than(p, a, b, flag[0], d, e, h[0])
    for x, y, f in product(range(1 << width), range(1 << width), (0, 1)):
        initial = basis(a, x) | basis(b, y) | basis(flag, f)
        assert p.run(initial) == initial ^ basis(flag, int(x < y))


def test_positive_part():
    p = Program()
    a, out = p.register(4), p.register(4)
    positive_part(p, a, out)
    for x in range(-8, 8):
        for previous in range(16):
            initial = basis(a, x) | basis(out, previous)
            assert p.run(initial) == initial ^ basis(out, max(x, 0))


def test_horner_exhaustive_signed_clean_work():
    p = Program()
    x, out = p.register(5), p.register(5)
    coefficients = (3, 2, 1)
    horner(p, x, out, coefficients, 2)
    for value in range(-16, 16):
        initial = basis(x, value)
        expected = evaluate_integer(value, coefficients, 2)
        assert p.run(initial) == initial | basis(out, expected)


@pytest.mark.parametrize("radius,degree,fraction,width", [(1, 12, 20, 32), (3, 24, 32, 48), (5, 36, 40, 64)])
def test_exponential_budget_against_high_precision(radius, degree, fraction, width):
    budget = exp_budget(radius, "0.000001", degree, fraction, width)
    assert budget["overflow_safe"]
    with localcontext() as context:
        context.prec = 110
        for i in range(-100, 101):
            exact_x = Decimal(i) * radius / 100
            encoded_x = int(exact_x * (1 << fraction))
            approximate = Decimal(evaluate_integer(encoded_x, budget["coefficients"], fraction)) / (1 << fraction)
            actual = abs(approximate - 100 * exact_x.exp())
            assert actual <= Decimal(budget["total_error_upper"])


def test_overflow_is_not_certified():
    assert not exp_budget(5, 0, 20, 8, 10)["overflow_safe"]
    with pytest.raises(ValueError):
        exp_budget(1, 0, 5, 8, 16, spot="100.1")


def test_actual_quantum_comparator_nonzero_grover():
    # A true full-register statevector, including the comparator's work qubits.
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector
    p = Program()
    u, y, flag = p.register(1), p.register(1), p.register(1)
    d, e, h = p.register(2), p.register(2), p.register(1)
    less_than(p, u, y, flag[0], d, e, h[0])
    a = QuantumCircuit(p.qubits)
    a.h(u[0])
    # Nonuniform y gives a=sin(.37)^2/2, not a Grover fixed point.
    a.ry(.74, y[0])
    a.compose(p.to_qiskit(), inplace=True)
    state = Statevector.from_instruction(a)
    expected = math.sin(.37)**2 / 2
    good = [i for i in range(1 << p.qubits) if (i >> flag[0]) & 1]
    assert sum(abs(state.data[good])**2) == pytest.approx(expected)
    # Z_good, A^-1, S_zero, A (global sign immaterial).
    q = QuantumCircuit(p.qubits)
    q.z(flag[0])
    q.compose(a.inverse(), inplace=True)
    q.x(range(p.qubits))
    q.h(p.qubits-1)
    q.mcx(list(range(p.qubits-1)), p.qubits-1)
    q.h(p.qubits-1)
    q.x(range(p.qubits))
    q.compose(a, inplace=True)
    amplified = state.evolve(q)
    assert sum(abs(amplified.data[good])**2) == pytest.approx(math.sin(3*math.asin(math.sqrt(expected)))**2)
    work_mask = sum(1 << b for b in d+e+h)
    assert np.sum([abs(amplified.data[i])**2 for i in range(len(amplified.data)) if i & work_mask]) < 1e-20


def test_reject_aliases_and_bad_precision():
    p = Program()
    a, b, h = p.register(2), p.register(3), p.register(1)
    with pytest.raises(ValueError):
        add(p, a, a, h[0])
    with pytest.raises(ValueError):
        add(p, a, b, h[0])
    with pytest.raises(ValueError):
        p.gate(a[0], a[0])
    with pytest.raises(ValueError):
        p.register(True)


def test_affine_all_inputs_clean_scratch():
    p = Program()
    inputs, out = p.register(3), p.register(5)
    affine(p, inputs, out, -3, (2, -1, 4))
    for value in range(8):
        result = -3 + sum(((value >> i) & 1)*c for i, c in enumerate((2, -1, 4)))
        initial = basis(inputs, value) | basis(out, 3)
        assert p.run(initial) == basis(inputs, value) | basis(out, 3+result)


def test_table_free_composed_raw_payoff_and_cleanup():
    p = Program()
    inputs, selector, flag = p.register(2), p.register(4), p.register(1)
    rows = ((0, (2, -1)), (-1, (1, 2)))
    coefficients = (4, 4, 2)  # small development polynomial at scale 4
    raw_payoff_flag(p, inputs, selector, flag[0], 6, 2, rows, coefficients, 6)
    for value, u, f in product(range(4), range(16), (0, 1)):
        logs = [a + sum(((value >> i) & 1)*c for i, c in enumerate(cs)) for a, cs in rows]
        payoff = max(sum(evaluate_integer(x, coefficients, 2) for x in logs)-6, 0)
        assert payoff < 16
        initial = basis(inputs, value) | basis(selector, u) | basis(flag, f)
        assert p.run(initial) == initial ^ basis(flag, int(u < payoff))
    resources = p.resources()
    assert resources["ccx"] > 0
    assert resources["logical_depth"] <= len(p.gates)


def test_non_enumerative_plan_and_quantization_budget():
    plan = raw_plan([4.6, 4.59], [[.2, -.1], [.1, .2]], normal_bits=2,
                    fraction_bits=24, width=48)
    assert plan["overflow_safe"]
    assert not plan["application_admitted"]
    with localcontext() as context:
        context.prec = 110
        for indices in product(range(4), repeat=2):
            bits = [(index >> k) & 1 for index in indices for k in range(2)]
            approximations = []
            truth = Decimal(0)
            for mean, row, (intercept, cs) in zip([4.6, 4.59], [[.2, -.1], [.1, .2]], plan["affine_rows"]):
                encoded = intercept + sum(b*c for b, c in zip(bits, cs))
                actual_log = Decimal.from_float(mean)-Decimal(100).ln()+sum(Decimal.from_float(c)*(-3+2*i) for c, i in zip(row, indices))
                assert abs(Decimal(encoded)/(1 << 24)-actual_log) <= Decimal(plan["log_quantization_error_upper"])
                approximations.append(evaluate_integer(encoded, plan["exp_budget"]["coefficients"], 24))
                truth += 100*actual_log.exp()
            payoff = max(sum(approximations)-plan["strike_sum"], 0)
            assert payoff < (1 << plan["selector_bits"])
            assert abs(Decimal(payoff)/(1 << 24)/2 - max(truth/2-100, 0)) <= Decimal(plan["arithmetic_price_error_upper"])


@pytest.mark.parametrize("kwargs", [{"normal_bits": True}, {"fraction_bits": 64}, {"strike": 100.1}, {"cutoff": -1}])
def test_plan_invalid_inputs(kwargs):
    with pytest.raises(ValueError):
        raw_plan([4.6], [[.2]], **kwargs)


def test_compact_gate_storage_matches_tuple_program():
    programs = [Program(), Program(compact=True)]
    for p in programs:
        a, b, flag = p.register(2), p.register(2), p.register(1)
        d, e, h = p.register(3), p.register(3), p.register(1)
        less_than(p, a, b, flag[0], d, e, h[0])
        p.undo(0)
    assert list(programs[0].gates) == list(programs[1].gates)
    assert programs[0].resources() == programs[1].resources()
    for i in range(32):
        assert programs[0].run(i) == programs[1].run(i) == i
