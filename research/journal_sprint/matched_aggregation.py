"""Matched *aggregation-only* reversible circuits, not pricing or advantage.

Inputs are already digitized unsigned prices. No loading, exponentiation,
payoff, uncomputation of prices, AE, or fault-tolerant synthesis is included.
The Fourier construction is standard Draper addition; the Kim/Cui/Lee/Park
2026 Fourier-arithmetic preprint is conceptual context, not a cost source.
All resource counts below come from actual circuits, not paper formulas.
"""

import math

from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFT

from research.journal_sprint.decimal_enclosure import Interval as I, pi_interval  # noqa: N817
from research.journal_sprint.reversible_fixed_point import Program, add


def _validate(width, terms, mode):
    for value in (width, terms):
        if type(value) is not int or value < 1:
            raise ValueError("width and terms must be positive integers")
    if mode not in ("ripple", "fourier"):
        raise ValueError("mode must be 'ripple' or 'fourier'")


def aggregation_angle_error_upper(width, terms, mode, *, zero_initialized=False):
    """Directed Decimal upper bound on the logical CP operator-norm bridge.

    Sum |stored binary64 angle - exact angle| using outward intervals and a
    certified pi enclosure. Telescoping and |exp(i*a)-exp(i*b)| <= |a-b|
    bound the whole aggregation unitary, including both QFTs (only the inverse
    QFT when zero_initialized=True). H, SWAP and
    ripple X/CX/CCX are ideal here. The same bound holds after exact control
    or inversion; multiple uses must be charged separately by the caller.

    This is NOT an accuracy certificate for transpiled U/CX parameters,
    native rotation synthesis, physical noise, or a pricing probability.
    QFT's stored angles use pi*2**(-distance), as in the pinned Terra QFT;
    tests compare these analytic loops against actual QFT CP parameters.
    No simulation or compilation is needed, including at width 40.
    """
    _validate(width, terms, mode)
    if type(zero_initialized) is not bool:
        raise ValueError("zero_initialized must be boolean")
    total = I(0)
    if mode == "ripple":
        return total.hi
    pi = pi_interval()
    # Positive forward and negative inverse QFT angles have equal deviations.
    for distance in range(1, width):
        stored = math.pi * (2.0 ** (-distance))
        deviation = (I(stored) - pi / (1 << distance)).absolute()
        total += (1 if zero_initialized else 2) * (width - distance) * deviation
    for bit in range(width):
        for frequency_bit in range(width - bit):
            exponent = bit + frequency_bit - width
            stored = math.ldexp(2 * math.pi, exponent)
            deviation = (I(stored) - 2 * pi / (1 << (-exponent))).absolute()
            total += terms * deviation
    return total.hi


def _modular_add(program, operand, accumulator, helper):
    """Cuccaro sum without unused top carry: (2w-2) CCX, (4w-2) CX.

    At w=1 the sum is a single CX. Lower MAJ/UMA stages propagate and
    erase carry; the top bit receives operand and carry directly.
    """
    width = len(operand)
    if width == 1:
        program.gate(operand[0], accumulator[0])
        return
    for i in range(width - 1):
        x, y, z = operand[i], accumulator[i], helper if i == 0 else operand[i - 1]
        program.gate(x, y)
        program.gate(x, z)
        program.gate(z, y, x)
    program.gate(operand[-1], accumulator[-1])
    program.gate(operand[-2], accumulator[-1])
    for i in reversed(range(width - 1)):
        x, y, z = operand[i], accumulator[i], helper if i == 0 else operand[i - 1]
        program.gate(z, y, x)
        program.gate(x, z)
        program.gate(z, y)


def aggregation_circuit(width, terms, mode, *, zero_initialized=False):
    """Return |x_0,...,x_(d-1),s> -> |x_0,...,s+sum(x) mod 2**w>.

    Little-endian operand j occupies [j*w,(j+1)*w); the accumulator
    occupies [d*w,(d+1)*w). Initialize it to zero to obtain the sum.
    Ripple alone appends one helper, which must start zero and returns zero.
    Operands are preserved coherently. Overflow is deliberately modular;
    callers must separately justify interpreting this as a financial sum.

    Fourier uses the full positive-exponent QFT with swaps, diagonal phases
    exp(2*pi*i*x*y/2**w), and its inverse. Only identity (integer-turn)
    phases are omitted: there is no approximate-QFT cutoff. Angles are
    floating-point representations of exact logical rotations, not a
    finite-gate-set synthesis guarantee.

    zero_initialized=True selects a cheaper unitary valid only when s=0:
    ripple copies the first operand then uses top-carry-omitted addition;
    Fourier replaces the initial QFT by H**width. To uncompute, use this
    actual circuit's inverse, not a separately constructed general adder.
    """
    _validate(width, terms, mode)
    if type(zero_initialized) is not bool:
        raise ValueError("zero_initialized must be boolean")
    if mode == "ripple":
        program = Program()
        operands = [program.register(width) for _ in range(terms)]
        accumulator = program.register(width)
        helper = program.register(1)[0]
        if zero_initialized:
            for source, target in zip(operands[0], accumulator):
                program.gate(source, target)
            for operand in operands[1:]:
                _modular_add(program, operand, accumulator, helper)
        else:
            for operand in operands:
                add(program, operand, accumulator, helper)
        circuit = program.to_qiskit()
    else:
        circuit = QuantumCircuit((terms + 1) * width)
        accumulator = list(range(terms * width, (terms + 1) * width))
        qft = QFT(width, approximation_degree=0, do_swaps=True).to_gate()
        if zero_initialized:
            circuit.h(accumulator)
        else:
            circuit.append(qft, accumulator)
        for term in range(terms):
            for bit in range(width):
                for frequency_bit in range(width - bit):
                    angle = math.ldexp(2 * math.pi, bit + frequency_bit - width)
                    circuit.cp(angle, term * width + bit,
                               accumulator[frequency_bit])
        circuit.append(qft.inverse(), accumulator)
    circuit.name = "aggregation_" + mode
    circuit.metadata = {"scope": "aggregation_only", "width": width,
                        "terms": terms, "mode": mode,
                        "zero_initialized": zero_initialized,
                        "accumulator": list(range(terms * width, (terms + 1) * width)),
                        "helper": (terms + 1) * width if mode == "ripple" else None}
    return circuit


def compiled_versions(circuit):
    """Compile actual bare and singly controlled circuits to u/cx at level 0.

    Control is wire zero in the controlled version, followed by the original
    wire order. Control the complete gate, including its global phase: a
    global phase becomes a relative phase upon control. No dense matrices or
    statevectors are constructed. Counts depend on the installed Qiskit.
    """
    bare = transpile(circuit, basis_gates=["u", "cx"], optimization_level=0)
    controlled = QuantumCircuit(bare.num_qubits + 1)
    controlled.append(bare.to_gate().control(1), range(controlled.num_qubits))
    controlled = transpile(controlled, basis_gates=["u", "cx"],
                           optimization_level=0)
    return {"uncontrolled": bare, "controlled": controlled}


def aggregation_resources(width, terms, mode, *, zero_initialized=False):
    """Count actual logical u/cx circuits, including single-control overhead.

    No connectivity, physical noise, rotation synthesis or pricing costs.
    Global phase is retained by the compiled circuits and reported in radians.
    angle_error_upper is a decimal string (not a nearest-rounded float): it
    bounds only the logical CP bridge described by aggregation_angle_error_upper.
    """
    circuits = compiled_versions(aggregation_circuit(
        width, terms, mode, zero_initialized=zero_initialized))
    result = {"scope": "aggregation_only", "width": width, "terms": terms,
              "mode": mode, "basis_gates": ["u", "cx"], "optimization_level": 0,
              "zero_initialized": zero_initialized,
              "angle_error_upper": str(aggregation_angle_error_upper(
                  width, terms, mode, zero_initialized=zero_initialized)),
              "angle_error_scope": "logical_cp_bridge_only"}
    for label, circuit in circuits.items():
        counts = circuit.count_ops()
        result[label] = {"qubits": circuit.num_qubits, "u": int(counts.get("u", 0)),
                         "cx": int(counts.get("cx", 0)), "depth": circuit.depth(),
                         "global_phase": float(circuit.global_phase)}
    return result
