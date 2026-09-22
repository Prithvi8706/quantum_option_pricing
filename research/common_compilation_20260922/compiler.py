"""One explicit, unoptimized U/CX policy for every compared route.

Profiles count ideal exact decomposition identities. Numeric Qiskit parameters
are not a newly certified native execution. Serial depth is a valid chosen
schedule, not optimized dependency depth. No inter-block cancellation is used.
"""

from dataclasses import asdict, dataclass

from qiskit import QuantumCircuit, transpile


@dataclass(frozen=True)
class Profile:
    u: int = 0
    cx: int = 0

    def __post_init__(self):
        if any(type(x) is not int or x < 0 for x in (self.u, self.cx)):
            raise ValueError("nonnegative integer counts required")

    def __add__(self, other):
        return Profile(self.u + other.u, self.cx + other.cx)

    def times(self, count):
        if type(count) is not int or count < 0:
            raise ValueError("nonnegative repetition count required")
        return Profile(count * self.u, count * self.cx)

    def record(self):
        return dict(asdict(self), serial_depth_upper=self.u + self.cx)


def compile_block(circuit):
    """Basis translation only; no optimized blocks inherited from old ledgers."""
    native = transpile(circuit, basis_gates=["u", "cx"], optimization_level=0, seed_transpiler=717)
    counts = native.count_ops()
    if set(counts) - {"u", "cx"}:
        raise ValueError("unexpected operation in compiled block")
    return Profile(int(counts.get("u", 0)), int(counts.get("cx", 0)))


def arithmetic_profile(counts):
    values = [counts[name] for name in ("x", "cx", "ccx")]
    if any(type(x) is not int or x < 0 for x in values):
        raise ValueError("invalid emitted primitive counts")
    x, cx, ccx = values
    return Profile(x + 9 * ccx, cx + 6 * ccx)


def controlled(profile):
    """Fixed CU: 5 U (one identity padding) + 2 CX; CCX: 9 U + 6 CX.

    One further phase U on the new control preserves the block's global phase,
    including zero. No special-angle or identity elimination is permitted.
    """
    return Profile(5 * profile.u + 9 * profile.cx + 1, 2 * profile.u + 6 * profile.cx)


def explicit_control(native):
    """Small-circuit semantic validation of the exact policy, including phase."""
    from qiskit.circuit.library import CCXGate

    result = QuantumCircuit(native.num_qubits + 1)
    result.u(0, 0, float(native.global_phase), 0)
    for item in native.data:
        qubits = [native.find_bit(q).index + 1 for q in item.qubits]
        if item.operation.name == "u":
            theta, phi, lam = map(float, item.operation.params)
            target = qubits[0]
            result.u(0, 0, 0, 0)  # Fixed padding: never optimize identities.
            result.u(0, 0, (lam + phi) / 2, 0)
            result.u(0, 0, (lam - phi) / 2, target)
            result.cx(0, target)
            result.u(-theta / 2, 0, -(phi + lam) / 2, target)
            result.cx(0, target)
            result.u(theta / 2, phi, 0, target)
        elif item.operation.name == "cx":
            block = QuantumCircuit(3)
            block.append(CCXGate(), range(3))
            decomposed = transpile(block, basis_gates=["u", "cx"], optimization_level=0)
            result.compose(decomposed, [0] + qubits, inplace=True)
        else:
            raise ValueError("explicit_control requires U/CX input")
    return result


def ae_profile(a, zero, size, repetitions, cancelled):
    """Canonical full IQFT, swaps, phase Hs, good-state CZ and Grover phase.

    The Grover global minus sign contributes one control phase U per iterate.
    In the cancelled circuit controlled(A S A^-1) uses unconditional A/A^-1;
    the new control still controls both reflections. A^-1 has identical counts.
    """
    if type(size) is not int or size < 2 or size & (size - 1):
        raise ValueError("power-of-two AE size required")
    if type(repetitions) is not int or repetitions < 1:
        raise ValueError("positive repetitions required")
    bits = size.bit_length() - 1
    used = a if cancelled else controlled(a)
    # Full IQFT: H per wire, CP=3U+2CX per pair, SWAP=3CX.
    pairs = bits * (bits - 1) // 2
    qft = Profile(bits + 3 * pairs, 2 * pairs + 3 * (bits // 2))
    # CZ=H-CX-H and global minus=phase(pi) on the AE control.
    iterate = used.times(2) + zero + Profile(3, 1)
    return (a + Profile(bits, 0) + iterate.times(size - 1) + qft).times(repetitions)
