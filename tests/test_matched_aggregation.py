"""Aggregation-only semantics and compiled-resource checks (at most 11 qubits)."""

import numpy as np
import pytest
from decimal import Decimal, localcontext
from qiskit.circuit.library import QFT
from qiskit.quantum_info import Statevector

from research.journal_sprint.decimal_enclosure import Interval as I, pi_interval  # noqa: N817
from research.journal_sprint.matched_aggregation import (
    aggregation_angle_error_upper, aggregation_circuit, aggregation_resources, compiled_versions,
)


def mapped(index, width, terms=2):
    mask = (1 << width) - 1
    operand_bits = terms * width
    total = sum((index >> (j * width)) & mask for j in range(terms))
    total += (index >> operand_bits) & mask
    return (index & ((1 << operand_bits) - 1)) | ((total & mask) << operand_bits)


@pytest.mark.parametrize("mode", ["ripple", "fourier"])
@pytest.mark.parametrize("width", [1, 2, 3])
@pytest.mark.parametrize("zero_initialized", [False, True])
def test_exhaustive_zero_accumulator_basis(width, mode, zero_initialized):
    circuit = aggregation_circuit(width, 2, mode, zero_initialized=zero_initialized)
    assert circuit.num_qubits <= 12
    for index in range(1 << (2 * width)):
        actual = Statevector.from_int(index, 1 << circuit.num_qubits).evolve(circuit).data
        expected = np.zeros_like(actual)
        expected[mapped(index, width)] = 1
        # Exact amplitude comparison catches relative/global phases as well as
        # overflow, changed operands and dirty helper wires.
        np.testing.assert_allclose(actual, expected, atol=2e-13, rtol=0)


@pytest.mark.parametrize("mode", ["ripple", "fourier"])
@pytest.mark.parametrize("width", [1, 2, 3])
def test_coherent_arbitrary_accumulator_and_control(width, mode):
    circuit = aggregation_circuit(width, 2, mode)
    versions = {"logical": circuit, **compiled_versions(circuit)}
    rng = np.random.default_rng(893 + width)
    for label, implementation in versions.items():
        controlled = label == "controlled"
        assert implementation.num_qubits <= 12
        # Support is every operand/accumulator value; helper remains zero.
        active = 1 << (3 * width + int(controlled))
        amplitudes = rng.normal(size=active) + 1j * rng.normal(size=active)
        amplitudes /= np.linalg.norm(amplitudes)
        initial = np.zeros(1 << implementation.num_qubits, dtype=complex)
        initial[:active] = amplitudes
        expected = np.zeros_like(initial)
        for index, amplitude in enumerate(amplitudes):
            if controlled:
                target = ((mapped(index >> 1, width) << 1) | 1) if index & 1 else index
            else:
                target = mapped(index, width)
            expected[target] = amplitude
        actual = Statevector(initial).evolve(implementation).data
        np.testing.assert_allclose(actual, expected, atol=3e-12, rtol=0)


@pytest.mark.parametrize("mode", ["ripple", "fourier"])
def test_control_retains_nonzero_global_phase(mode):
    circuit = aggregation_circuit(2, 2, mode)
    circuit.global_phase += 0.37
    controlled = compiled_versions(circuit)["controlled"]
    initial = np.zeros(1 << controlled.num_qubits, dtype=complex)
    # Control superposition, input prices 3 and 2; overflow sum is 1.
    index = 3 | (2 << 2)
    initial[index << 1] = initial[(index << 1) | 1] = 1 / np.sqrt(2)
    expected = np.zeros_like(initial)
    expected[index << 1] = 1 / np.sqrt(2)
    expected[(mapped(index, 2) << 1) | 1] = np.exp(0.37j) / np.sqrt(2)
    np.testing.assert_allclose(Statevector(initial).evolve(controlled).data,
                               expected, atol=3e-12, rtol=0)


@pytest.mark.parametrize("mode", ["ripple", "fourier"])
@pytest.mark.parametrize("width,terms", [(1, 1), (2, 2), (3, 2), (8, 4)])
def test_actual_compiled_counts(width, terms, mode):
    report = aggregation_resources(width, terms, mode)
    versions = compiled_versions(aggregation_circuit(width, terms, mode))
    assert report["scope"] == "aggregation_only"
    assert report["angle_error_scope"] == "logical_cp_bridge_only"
    assert Decimal(report["angle_error_upper"]) == aggregation_angle_error_upper(width, terms, mode)
    for label, circuit in versions.items():
        assert set(circuit.count_ops()) <= {"u", "cx"}
        assert report[label] == {"qubits": circuit.num_qubits,
                                 "u": circuit.count_ops().get("u", 0),
                                 "cx": circuit.count_ops().get("cx", 0),
                                 "depth": circuit.depth(),
                                 "global_phase": float(circuit.global_phase)}
    assert report["controlled"]["qubits"] == report["uncontrolled"]["qubits"] + 1


@pytest.mark.parametrize("width,terms,mode", [
    (0, 2, "ripple"), (-1, 2, "fourier"), (True, 2, "ripple"),
    (1.5, 2, "ripple"), (2, 0, "fourier"), (2, False, "fourier"),
    (2, 2.0, "fourier"), (2, 2, "unknown"), (2, 2, None),
])
def test_bad_inputs(width, terms, mode):
    with pytest.raises(ValueError):
        aggregation_circuit(width, terms, mode)
    with pytest.raises(ValueError):
        aggregation_resources(width, terms, mode)
    with pytest.raises(ValueError):
        aggregation_angle_error_upper(width, terms, mode)


@pytest.mark.parametrize("width,terms", [(1, 2), (2, 2), (3, 2), (40, 2), (40, 4)])
@pytest.mark.parametrize("zero_initialized", [False, True])
def test_angle_bound_against_actual_stored_cp_angles(width, terms, zero_initialized):
    # Inspect gate lists, never production-width matrices or statevectors.
    # Independently recover exact targets from wire locations for every CP.
    pi = pi_interval()
    total = I(0)
    for inverse in ((True,) if zero_initialized else (False, True)):
        qft = QFT(width, do_swaps=True, approximation_degree=0, inverse=inverse).decompose()
        found = 0
        for instruction in qft.data:
            if instruction.operation.name != "cp":
                continue
            wires = [qft.find_bit(bit).index for bit in instruction.qubits]
            distance = abs(wires[0] - wires[1])
            target = pi / (1 << distance)
            if inverse:
                target = -target
            total += (I(float(instruction.operation.params[0])) - target).absolute()
            found += 1
        assert found == width * (width - 1) // 2
    circuit = aggregation_circuit(width, terms, "fourier", zero_initialized=zero_initialized)
    found = 0
    for instruction in circuit.data:
        if instruction.operation.name != "cp":
            continue
        source, target = [circuit.find_bit(bit).index for bit in instruction.qubits]
        exponent = width - source % width - (target - terms * width)
        angle = 2 * pi / (1 << exponent)
        total += (I(float(instruction.operation.params[0])) - angle).absolute()
        found += 1
    assert found == terms * width * (width + 1) // 2
    upper = aggregation_angle_error_upper(width, terms, "fourier",
                                          zero_initialized=zero_initialized)
    # Different directed summation orders may differ in their last decimal.
    assert total.lo <= upper
    assert (I(upper) - I(total.hi)).absolute().hi < Decimal("1e-85")
    assert Decimal(0) < upper < Decimal("1e-12")
    assert aggregation_angle_error_upper(width, terms, "ripple") == 0
    # An external caller's ambient decimal precision cannot weaken the bound.
    with localcontext() as context:
        context.prec = 6
        assert aggregation_angle_error_upper(width, terms, "fourier",
                                             zero_initialized=zero_initialized) == upper


def test_width_one_bound_against_independent_pi_digits():
    # Independent high-precision pi digits give a scalar rounding cross-check.
    pi_digits = Decimal("3.141592653589793238462643383279502884197169399375105820974944"
                        "592307816406286208998628")
    with localcontext() as context:
        context.prec = 90
        stored_pi = Decimal.from_float(float(np.pi))
        expected = 2 * abs(stored_pi - pi_digits)  # w=1, two accumulation CPs
        upper = aggregation_angle_error_upper(1, 2, "fourier")
        assert upper >= expected
        assert upper - expected < Decimal("1e-75")


@pytest.mark.parametrize("mode", ["ripple", "fourier"])
@pytest.mark.parametrize("width,terms", [(1, 2), (2, 2), (3, 2), (2, 3), (3, 1)])
def test_zero_initialized_coherent_compute_uncompute(width, terms, mode):
    circuit = aggregation_circuit(width, terms, mode, zero_initialized=True)
    rng = np.random.default_rng(329)
    for label, implementation in {"logical": circuit, **compiled_versions(circuit)}.items():
        controlled = label == "controlled"
        assert implementation.num_qubits <= 12
        active = 1 << (terms * width + int(controlled))
        amplitudes = rng.normal(size=active) + 1j * rng.normal(size=active)
        amplitudes /= np.linalg.norm(amplitudes)
        initial = np.zeros(1 << implementation.num_qubits, dtype=complex)
        initial[:active] = amplitudes
        expected = np.zeros_like(initial)
        for index, amplitude in enumerate(amplitudes):
            if controlled:
                target = ((mapped(index >> 1, width, terms) << 1) | 1) if index & 1 else index
            else:
                target = mapped(index, width, terms)
            expected[target] = amplitude
        output = Statevector(initial).evolve(implementation)
        np.testing.assert_allclose(output.data, expected, atol=4e-12, rtol=0)
        np.testing.assert_allclose(output.evolve(implementation.inverse()).data,
                                   initial, atol=5e-12, rtol=0)


@pytest.mark.parametrize("width,terms", [(1, 1), (1, 4), (2, 2), (3, 4), (40, 2), (40, 4)])
def test_short_ripple_gate_counts(width, terms):
    circuit = aggregation_circuit(width, terms, "ripple", zero_initialized=True)
    counts = circuit.count_ops()
    assert counts.get("ccx", 0) == (terms - 1) * (2 * width - 2)
    assert counts["cx"] == width + (terms - 1) * (1 if width == 1 else 4 * width - 2)
    assert set(counts) <= {"cx", "ccx"}


@pytest.mark.parametrize("mode", ["ripple", "fourier"])
def test_short_resource_interface(mode):
    report = aggregation_resources(3, 2, mode, zero_initialized=True)
    assert report["zero_initialized"] is True
    assert Decimal(report["angle_error_upper"]) == aggregation_angle_error_upper(
        3, 2, mode, zero_initialized=True)
    versions = compiled_versions(aggregation_circuit(3, 2, mode, zero_initialized=True))
    for name, circuit in versions.items():
        assert report[name]["cx"] == circuit.count_ops().get("cx", 0)
        assert report[name]["u"] == circuit.count_ops().get("u", 0)


@pytest.mark.parametrize("invalid", [0, 1, None, "yes"])
def test_zero_initialized_requires_boolean(invalid):
    for function in (aggregation_circuit, aggregation_resources, aggregation_angle_error_upper):
        with pytest.raises(ValueError):
            function(2, 2, "ripple", zero_initialized=invalid)
