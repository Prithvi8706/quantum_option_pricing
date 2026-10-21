"""One prospective F44 Stage K realization; authoring never builds a circuit.

Full72 ports, ordered signed52x38 input promise, full modular116 product,
retained CSA/ripple histories, exact output XOR and literal reverse. The signed
rounder accepts every full72 input. Only stdlib X/CX/CCX rows are constructed.
"""

from array import array

W, F, LEFT_BITS, RIGHT_BITS, PRODUCT_BITS = 72, 44, 52, 38, 116
MAX_NATIVE_ROWS = 1_000_000


def require(condition, message):
    if not condition:
        raise ValueError(message)


class Circuit:
    def __init__(self, checkpoint):
        require(callable(checkpoint), "Mandatory bounded-work callback")
        require(array("i").itemsize == 4, "Signed int32 native row storage")
        self.checkpoint = checkpoint
        self.qubits = 0
        self.gates = array("i")

    @property
    def rows(self):
        return len(self.gates) // 4

    def register(self, bits):
        self.checkpoint()
        require(type(bits) is int and bits > 0, "Positive concrete register width")
        start = self.qubits
        self.qubits += bits
        require(self.qubits < 1 << 31, "Int32 wire addresses")
        return list(range(start, self.qubits))

    def gate(self, *wires):
        self.checkpoint()
        require(1 <= len(wires) <= 3 and self.rows < MAX_NATIVE_ROWS, "Finite X/CX/CCX rows")
        require(
            all(type(wire) is int and 0 <= wire < self.qubits for wire in wires)
            and len(set(wires)) == len(wires),
            "Distinct in-range native operands",
        )
        self.gates.extend((len(wires), *wires, *([0] * (3 - len(wires)))))
        self.checkpoint()

    def reverse_compute(self, begin, end):
        self.checkpoint()
        require(0 <= begin <= end <= self.rows, "Fixed original compute interval")
        for row in range(end - 1, begin - 1, -1):
            self.checkpoint()
            offset = 4 * row
            kind = self.gates[offset]
            self.gate(*self.gates[offset + 1 : offset + 1 + kind])


def signed_plane():
    """-t*2^k=(1-t)*2^k-2^k; correction uses the full116 modulus."""
    terms, correction = [], 0
    for i in range(RIGHT_BITS):
        for j in range(LEFT_BITS):
            negative = (j == LEFT_BITS - 1) != (i == RIGHT_BITS - 1)
            terms.append((j, i, j + i, negative))
            if negative:
                correction -= 1 << (j + i)
    return terms, correction & ((1 << PRODUCT_BITS) - 1)


def build_multiplier(checkpoint):
    p = Circuit(checkpoint)
    a, b, out = (p.register(W) for _ in range(3))
    columns = [[] for _ in range(PRODUCT_BITS)]
    partials, fixed = [], []
    terms, correction = signed_plane()
    begin = p.rows
    for j, i, column, negative in terms:
        checkpoint()
        value = p.register(1)[0]
        if negative:
            p.gate(value)
        p.gate(a[j], b[i], value)
        columns[column].append(value)
        partials.append(dict(a_bit=j, b_bit=i, column=column, negative=negative, wire=value))
    for column in range(PRODUCT_BITS):
        checkpoint()
        if (correction >> column) & 1:
            value = p.register(1)[0]
            p.gate(value)
            columns[column].append(value)
            fixed.append(dict(column=column, wire=value))
    layers = []
    while max(map(len, columns)) > 2:
        checkpoint()
        following = [[] for _ in range(PRODUCT_BITS)]
        full_adders = []
        for column, values in enumerate(columns):
            checkpoint()
            consumed = 0
            for offset in range(0, len(values) - 2, 3):
                x, y, z = values[offset : offset + 3]
                summed = p.register(1)[0]
                p.gate(x, summed)
                p.gate(y, summed)
                carry = None
                if column + 1 < PRODUCT_BITS:
                    carry = p.register(1)[0]
                    p.gate(x, y, carry)
                    p.gate(summed, z, carry)
                    following[column + 1].append(carry)
                p.gate(z, summed)
                following[column].append(summed)
                full_adders.append(dict(column=column, inputs=[x, y, z], sum=summed, carry=carry))
                consumed = offset + 3
            following[column].extend(values[consumed:])
        layers.append(full_adders)
        columns = following
    left, right, product = (p.register(PRODUCT_BITS) for _ in range(3))
    for column, values in enumerate(columns):
        checkpoint()
        if values:
            p.gate(values[0], left[column])
        if len(values) == 2:
            p.gate(values[1], right[column])
    propagate = p.register(PRODUCT_BITS)
    carry = p.register(PRODUCT_BITS + 1)
    for bit in range(PRODUCT_BITS):
        checkpoint()
        p.gate(left[bit], propagate[bit])
        p.gate(right[bit], propagate[bit])
        p.gate(left[bit], right[bit], carry[bit + 1])
        if bit:
            p.gate(propagate[bit], carry[bit], carry[bit + 1])
        p.gate(propagate[bit], product[bit])
        if bit:
            p.gate(carry[bit], product[bit])
    end = p.rows
    for source, target in zip(product[F : F + W], out, strict=True):
        p.gate(source, target)
    p.reverse_compute(begin, end)
    descriptor = {
        "schema": "a14-f44-stage-k-clean-arithmetic-leaf-v1",
        "op": "mul",
        "params": {},
        "spec": {
            "width": W,
            "fraction_bits": F,
            "product_width": PRODUCT_BITS,
            "active_operand_bits": [LEFT_BITS, RIGHT_BITS],
            "input_contract": {"signed_operand_bits": [LEFT_BITS, RIGHT_BITS]},
            "variant": "retained-CSA-explicit-ripple-final-v1",
        },
        "args": [a, b],
        "outs": [out],
        "qubits": p.qubits,
        "gate_rows": p.rows,
        "compute_gate_rows": [begin, end],
        "copy_gate_rows": [end, end + W],
        "inverse_gate_rows": [end + W, p.rows],
        "recipe": {
            "partials": partials,
            "correction": correction,
            "fixed": fixed,
            "CSA_layers": layers,
            "final_columns": columns,
            "left": left,
            "right": right,
            "product": product,
            "propagate": propagate,
            "carry": carry,
            "output_source_bits": list(range(F, F + W)),
        },
        "private_workspace_zero_entry_exit": True,
        "dirty_output_XOR": True,
        "input_preserved": True,
        "low_product_columns_discarded_before_carry": False,
        "full_signed_semantic_product_bits": 144,
        "generic_active_signed_product_bits": 90,
        "minimum_times_minimum_positive_power": 88,
        "product_modulus_bits": PRODUCT_BITS,
        "actual_gate_emission_claim_during_authoring": False,
    }
    checkpoint()
    return p, descriptor


def append_or(p, left, right, output):
    """Clean-zero target OR: a XOR b XOR ab; retains both inputs."""
    p.gate(left, output)
    p.gate(right, output)
    p.gate(left, right, output)


def build_rounder(checkpoint):
    p = Circuit(checkpoint)
    z, out = (p.register(W) for _ in range(2))
    quotient, remainder = p.register(W), p.register(4)
    ors, increment = p.register(3), p.register(1)[0]
    carry, result = p.register(W + 1), p.register(W)
    begin = p.rows
    quotient_sources = [z[min(bit + 4, W - 1)] for bit in range(W)]
    for source, target in zip(quotient_sources, quotient, strict=True):
        p.gate(source, target)
    for source, target in zip(z[:4], remainder, strict=True):
        p.gate(source, target)
    append_or(p, remainder[0], remainder[1], ors[0])
    append_or(p, ors[0], remainder[2], ors[1])
    append_or(p, ors[1], quotient[0], ors[2])
    p.gate(remainder[3], ors[2], increment)
    predicate_end = p.rows
    p.gate(increment, carry[0])
    for bit in range(W):
        checkpoint()
        p.gate(quotient[bit], result[bit])
        p.gate(carry[bit], result[bit])
        p.gate(quotient[bit], carry[bit], carry[bit + 1])
    end = p.rows
    for source, target in zip(result, out, strict=True):
        p.gate(source, target)
    p.reverse_compute(begin, end)
    descriptor = {
        "schema": "a14-f44-stage-k-clean-arithmetic-leaf-v1",
        "op": "round_ties_even",
        "params": {"discarded_fractional_bits": 4},
        "spec": {
            "width": W,
            "input_fraction_bits": F,
            "output_fraction_bits": 40,
            "input_contract": {},
            "variant": "retained-signed-quotient-parity-ripple-increment-v1",
        },
        "args": [z],
        "outs": [out],
        "qubits": p.qubits,
        "gate_rows": p.rows,
        "compute_gate_rows": [begin, end],
        "predicate_compute_gate_rows": [begin, predicate_end],
        "copy_gate_rows": [end, end + W],
        "inverse_gate_rows": [end + W, p.rows],
        "recipe": {
            "quotient": quotient,
            "quotient_source_wires": quotient_sources,
            "remainder": remainder,
            "OR_history": ors,
            "increment": increment,
            "carry": carry,
            "result": result,
        },
        "private_workspace_zero_entry_exit": True,
        "dirty_output_XOR": True,
        "input_preserved": True,
        "negative_rounding_is_floor_quotient": True,
        "actual_gate_emission_claim_during_authoring": False,
    }
    checkpoint()
    return p, descriptor


def row_at(circuit, index):
    require(type(index) is int and 0 <= index < circuit.rows, "Native row index")
    offset = 4 * index
    return tuple(circuit.gates[offset : offset + 4])


def run_rows(circuit, state, checkpoint, *, inverse=False, begin=0, end=None):
    """Literal scalar interpreter; fixed basis diagnostics only, never JIT."""
    end = circuit.rows if end is None else end
    require(len(state) == circuit.qubits and 0 <= begin <= end <= circuit.rows, "Full wire state")
    indices = range(end - 1, begin - 1, -1) if inverse else range(begin, end)
    for index in indices:
        checkpoint()
        kind, a, b, c = row_at(circuit, index)
        if kind == 1:
            require(b == c == 0, "Zero unused X operands")
            state[a] ^= 1
        elif kind == 2:
            require(c == 0 and a != b, "Canonical CX operands")
            state[b] ^= state[a]
        else:
            require(kind == 3 and len({a, b, c}) == 3, "Canonical CCX operands")
            state[c] ^= state[a] & state[b]
    checkpoint()
    return state


def signed_word(word, width=W):
    require(type(word) is int and 0 <= word < 1 << width, "Unsigned raw word")
    return word - (1 << width) if word >> (width - 1) else word


def promised_word(word, active_bits):
    low = word & ((1 << active_bits) - 1)
    return word == (signed_word(low, active_bits) & ((1 << W) - 1))


def rounding_reference(word):
    z = signed_word(word)
    q, r = divmod(z, 16)
    return (q + int(r > 8 or (r == 8 and q & 1))) & ((1 << W) - 1)


def fixed_diagnostics():
    """Literal fixed corpus; calling it is root-only prospective work."""
    xmin, xmax = -(1 << 51), (1 << 51) - 1
    ymin, ymax = -(1 << 37), (1 << 37) - 1
    pairs = [
        (0, 0),
        (0, 1),
        (1, 0),
        (-1, 1),
        (xmin, ymin),
        (xmax, ymax),
        (xmin, ymax),
        (xmax, ymin),
    ]
    dirty = [0, (1 << W) - 1]
    return {
        "multiplier": [(left, right, value) for left, right in pairs for value in dirty],
        "rounder": [
            (16 * q + r, value) for q in (-2, -1, 0, 1) for r in (0, 7, 8, 9, 15) for value in dirty
        ],
        "Boolean_prefix": [(r, parity) for r in range(16) for parity in (0, 1)],
    }


CCX_PHASE_MACRO = (
    ("H", 2),
    ("CX", 1, 2),
    ("TD", 2),
    ("CX", 0, 2),
    ("T", 2),
    ("CX", 1, 2),
    ("TD", 2),
    ("CX", 0, 2),
    ("T", 1),
    ("T", 2),
    ("H", 2),
    ("CX", 0, 1),
    ("T", 0),
    ("TD", 1),
    ("CX", 0, 1),
)


def gate_resources(circuit, checkpoint):
    """Fresh actual chronological expansion; no borrowed multiplier profile."""
    counts = [0, 0, 0]
    t_levels, ct_levels = [0] * circuit.qubits, [0] * circuit.qubits
    for index in range(circuit.rows):
        checkpoint()
        kind, a, b, c = row_at(circuit, index)
        require(1 <= kind <= 3, "Recognized exact native opcode")
        counts[kind - 1] += 1
        wires = (a, b, c)
        events = (("X", 0),) if kind == 1 else (("CX", 0, 1),) if kind == 2 else CCX_PHASE_MACRO
        for event in events:
            checkpoint()
            affected = [wires[operand] for operand in event[1:]]
            require(len(set(affected)) == len(affected), "Distinct macro-event operands")
            td = max(t_levels[wire] for wire in affected) + int(event[0] in ("T", "TD"))
            cd = max(ct_levels[wire] for wire in affected) + 1
            for wire in affected:
                t_levels[wire], ct_levels[wire] = td, cd
    x, cx, ccx = counts
    checkpoint()
    return {
        "qubits": circuit.qubits,
        "source_gates": circuit.rows,
        "x": x,
        "cx": cx,
        "ccx": ccx,
        "t_count": 7 * ccx,
        "t_depth": max(t_levels),
        "clifford_t_depth": max(ct_levels),
        "clifford_cx": cx + 6 * ccx,
        "clifford_h": 2 * ccx,
        "phase_macro": "absolute exact7T CCX; parity polynomial4abc, H target conjugation",
        "schedule": "all-to-all ASAP chronological expansion of every native row",
        "caller_argument_copy_CX_not_in_leaf": True,
        "no_F40_or_prior_multiplier_resource_transfer": True,
    }
