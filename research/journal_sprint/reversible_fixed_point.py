"""Development-only, table-free X/CX/CCX arithmetic in little-endian registers.

All arithmetic is modular. Callers must separately prove absence of overflow.
The gate list is an actual reversible permutation, not a resource-count formula.
No loading, noise, synthesis or continuous-price certificate is implied.
"""

from collections import Counter
from array import array


class CompactGates:
    """Fixed-size integer records; avoids millions of Python tuple objects."""
    def __init__(self):
        self.data = array("i")

    def __len__(self):
        return len(self.data)//4

    def __getitem__(self, key):
        if isinstance(key, slice):
            return [self[i] for i in range(*key.indices(len(self))) ]
        if key < 0:
            key += len(self)
        if not 0 <= key < len(self):
            raise IndexError(key)
        i = 4*key
        return tuple(self.data[i+1:i+1+self.data[i]])

    def __setitem__(self, key, values):
        indices = list(range(*key.indices(len(self))))
        values = list(values)
        if len(indices) != len(values):
            raise ValueError("only length-preserving gate replacement supported")
        for i, gate in zip(indices, values):
            self.data[4*i:4*i+4] = array("i", (len(gate), *gate, *([0]*(3-len(gate)))))

    def append(self, gate):
        self.data.extend((len(gate), *gate, *([0]*(3-len(gate)))))

    def extend(self, gates):
        for gate in gates:
            self.append(gate)


class Program:
    def __init__(self, compact=False):
        self.qubits = 0
        self.gates = CompactGates() if compact else []

    def register(self, width):
        if isinstance(width, bool) or not isinstance(width, int) or width < 1:
            raise ValueError("positive integer register width required")
        result = tuple(range(self.qubits, self.qubits + width))
        self.qubits += width
        return result

    def gate(self, *bits):
        if not 1 <= len(bits) <= 3 or len(set(bits)) != len(bits):
            raise ValueError("X/CX/CCX require distinct wires")
        if any(type(b) is not int or not 0 <= b < self.qubits for b in bits):
            raise ValueError("unallocated wire")
        self.gates.append(tuple(bits))

    def undo(self, start, stop=None):
        stop = len(self.gates) if stop is None else stop
        self.gates.extend(self.gates[i] for i in range(stop-1, start-1, -1))

    def run(self, state):
        if type(state) is not int or not 0 <= state < (1 << self.qubits):
            raise ValueError("invalid computational basis state")
        for gate in self.gates:
            if all((state >> b) & 1 for b in gate[:-1]):
                state ^= 1 << gate[-1]
        return state

    def resources(self):
        count = Counter({1: 0, 2: 0, 3: 0})
        depth = [0] * self.qubits
        for gate in self.gates:
            count[len(gate)] += 1
            level = 1 + max(depth[b] for b in gate)
            for b in gate:
                depth[b] = level
        return dict(qubits=self.qubits, x=count[1], cx=count[2], ccx=count[3],
                    logical_depth=max(depth, default=0))

    def to_qiskit(self):
        from qiskit import QuantumCircuit
        circuit = QuantumCircuit(self.qubits)
        for gate in self.gates:
            (circuit.x, circuit.cx, circuit.ccx)[len(gate) - 1](*gate)
        return circuit


def read(state, register, signed=False):
    value = sum(((state >> b) & 1) << i for i, b in enumerate(register))
    return value - (1 << len(register)) if signed and value >> (len(register)-1) else value


def basis(register, value):
    return sum(((value >> i) & 1) << b for i, b in enumerate(register))


def _disjoint(*registers):
    wires = [b for r in registers for b in r]
    if not all(registers) or len(wires) != len(set(wires)):
        raise ValueError("nonempty disjoint registers required")


def copy(p, source, target):
    _disjoint(source, target)
    if len(source) != len(target):
        raise ValueError("equal widths required")
    for a, b in zip(source, target):
        p.gate(a, b)


def constant(p, target, value):
    if type(value) is not int:
        raise ValueError("integer constant required")
    for i, b in enumerate(target):
        if (value >> i) & 1:
            p.gate(b)


def add(p, a, b, helper):
    """Cuccaro fixed-width b += a; helper must start zero and returns zero."""
    _disjoint(a, b, (helper,))
    if len(a) != len(b):
        raise ValueError("equal widths required")

    def maj(x, y, z):
        p.gate(x, y)
        p.gate(x, z)
        p.gate(z, y, x)

    def uma(x, y, z):
        p.gate(z, y, x)
        p.gate(x, z)
        p.gate(z, y)

    maj(a[0], b[0], helper)
    for i in range(len(a)-1):
        maj(a[i+1], b[i+1], a[i])
    for i in reversed(range(len(a)-1)):
        uma(a[i+1], b[i+1], a[i])
    uma(a[0], b[0], helper)


def subtract(p, a, b, helper):
    start = len(p.gates)
    add(p, a, b, helper)
    p.gates[start:] = reversed(p.gates[start:])


def multiply(p, a, b, out, partial, helper):
    """out += signed(a)*signed(b) modulo 2**len(out); clean partial/helper.

    Sign extension is in read controls only. Partial products are added and
    immediately uncomputed, with no basis-state enumeration.
    """
    _disjoint(a, b, out, partial, (helper,))
    n = len(out)
    if len(partial) != n or n < max(len(a), len(b)):
        raise ValueError("invalid product workspace")
    aa = tuple(a) + (a[-1],) * (n-len(a))
    bb = tuple(b) + (b[-1],) * (n-len(b))
    for i in range(n):
        start = len(p.gates)
        for j in range(n-i):
            p.gate(aa[j], bb[i], partial[j])
        end = len(p.gates)
        add(p, partial[:n-i], out[i:], helper)
        p.undo(start, end)


def fixed_multiply(p, a, b, out, fraction_bits, product, partial, helper):
    """out XOR= floor(signed(a)*signed(b)/2**f) mod 2**width.

    Exact full signed product, then copy a bit slice and uncompute. All scratch
    starts/ends zero; output may be nonzero. Overflow in the retained word is
    the caller's responsibility, not silently certified here.
    """
    _disjoint(a, b, out, product, partial, (helper,))
    w = len(a)
    if len(b) != w or len(out) != w or len(product) != 2*w:
        raise ValueError("equal input/output widths and double-width product required")
    if type(fraction_bits) is not int or not 0 <= fraction_bits <= w:
        raise ValueError("invalid fractional width")
    start = len(p.gates)
    multiply(p, a, b, product, partial, helper)
    end = len(p.gates)
    copy(p, product[fraction_bits:fraction_bits+w], out)
    p.undo(start, end)


def less_than(p, a, b, flag, difference, extended_b, helper):
    """flag XOR= unsigned(a)<unsigned(b); clean double operand workspace."""
    _disjoint(a, b, (flag,), difference, extended_b, (helper,))
    n = len(a)
    if len(b) != n or len(difference) != n+1 or len(extended_b) != n+1:
        raise ValueError("comparator requires n+1-bit scratch")
    start = len(p.gates)
    copy(p, a, difference[:n])
    copy(p, b, extended_b[:n])
    subtract(p, extended_b, difference, helper)
    end = len(p.gates)
    p.gate(difference[-1], flag)
    p.undo(start, end)


def positive_part(p, signed_input, out):
    """out XOR= max(signed_input,0), same fixed-point scale, clean sign."""
    _disjoint(signed_input, out)
    if len(signed_input) != len(out):
        raise ValueError("equal widths required")
    sign = signed_input[-1]
    p.gate(sign)
    for a, b in zip(signed_input[:-1], out[:-1]):
        p.gate(sign, a, b)
    p.gate(sign)


def horner(p, x, out, coefficients, fraction_bits):
    """Clean out XOR= fixed-point Horner polynomial, allocating explicit work.

    Stored stages trade qubits for straightforward Bennett uncomputation.
    Coefficients are integers at the same binary scale as x. No overflow
    promise: use a separate domain/precision certificate before interpretation.
    """
    _disjoint(x, out)
    w = len(x)
    if len(out) != w or not coefficients or any(type(c) is not int for c in coefficients):
        raise ValueError("equal widths and integer coefficients required")
    if type(fraction_bits) is not int or not 0 <= fraction_bits < w:
        raise ValueError("invalid fractional width")
    if any(not -(1 << (w-1)) <= c < (1 << (w-1)) for c in coefficients):
        raise ValueError("coefficient outside signed word")
    coefficients = tuple(coefficients)
    while len(coefficients) > 1 and coefficients[-1] == 0:
        coefficients = coefficients[:-1]
    stages = [p.register(w) for _ in coefficients]
    product, partial, cword = p.register(2*w), p.register(2*w), p.register(w)
    helper = p.register(1)[0]
    start = len(p.gates)
    constant(p, stages[0], coefficients[-1])
    for i, c in enumerate(reversed(coefficients[:-1])):
        fixed_multiply(p, x, stages[i], stages[i+1], fraction_bits,
                       product, partial, helper)
        constant(p, cword, c)
        add(p, cword, stages[i+1], helper)
        constant(p, cword, c)
    end = len(p.gates)
    copy(p, stages[-1], out)
    p.undo(start, end)


def affine(p, inputs, out, intercept, bit_coefficients):
    """out += intercept + sum(bit_i*c_i), modulo word size, clean scratch."""
    _disjoint(inputs, out)
    if type(intercept) is not int or len(inputs) != len(bit_coefficients):
        raise ValueError("one integer coefficient per input bit required")
    if any(type(c) is not int for c in bit_coefficients):
        raise ValueError("integer bit coefficients required")
    temp, helper = p.register(len(out)), p.register(1)[0]
    constant(p, temp, intercept)
    add(p, temp, out, helper)
    constant(p, temp, intercept)
    for bit, value in zip(inputs, bit_coefficients):
        start = len(p.gates)
        for i, wire in enumerate(temp):
            if (value >> i) & 1:
                p.gate(bit, wire)
        end = len(p.gates)
        add(p, temp, out, helper)
        p.undo(start, end)


def raw_payoff_flag(p, inputs, selector, flag, width, fraction_bits,
                    affine_rows, exp_coefficients, strike_sum):
    """Clean raw-call flag from bitwise affine logs, Horner exp, integer sum.

    Flag XOR= selector < max(sum(exp_approx(log_i))-strike_sum,0).
    Selector is uniform only if the caller prepares it so. The caller MUST
    certify all intermediate signed words and that payoff < 2**len(selector).
    Not a continuous-price oracle or Gaussian state loader by itself.
    """
    _disjoint(inputs, selector, (flag,))
    if type(width) is not int or not 1 <= len(selector) < width:
        raise ValueError("selector must fit positive signed word")
    if not affine_rows or type(strike_sum) is not int or not 0 <= strike_sum < 1 << (width-1):
        raise ValueError("nonempty rows and representable nonnegative strike required")
    total, strike, payoff = p.register(width), p.register(width), p.register(width)
    helper = p.register(1)[0]
    start = len(p.gates)
    for intercept, coefficients in affine_rows:
        log, spot = p.register(width), p.register(width)
        affine(p, inputs, log, intercept, coefficients)
        horner(p, log, spot, exp_coefficients, fraction_bits)
        add(p, spot, total, helper)
    constant(p, strike, strike_sum)
    subtract(p, strike, total, helper)
    positive_part(p, total, payoff)
    end = len(p.gates)
    difference, extended = p.register(len(selector)+1), p.register(len(selector)+1)
    less_than(p, selector, payoff[:len(selector)], flag, difference, extended, helper)
    p.undo(start, end)
