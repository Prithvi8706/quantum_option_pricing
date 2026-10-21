"""Prospective one complete clean F44 cosine prototype; no author-stage execution.

Full72 ports and dirty output, one fixed64x8 table, eager Q-to-zero routing,
actual admitted leaf rows, full argument copies, and literal global inverse.
Only stdlib X/CX/CCX arrays. All calls require a controller-owned checkpoint.
"""

from array import array

W, Q, F = 72, 1 << 40, 44
MAX_ROWS = 2_000_000
MAX_QUBITS = 16_384
REPLAY_GUARD_ROWS = 128
ROW_ID = "TAYLOR_D6_S64_W72_F44_TO_F40_MUL52x38"
MACRO = (
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


def require(condition, message):
    if not condition:
        raise ValueError(message)


class Circuit:
    def __init__(self, checkpoint):
        require(callable(checkpoint) and array("i").itemsize == 4, "Bounded int32 native ABI")
        self.checkpoint, self.qubits, self.gates = checkpoint, 0, array("i")
        self._replay_masks = None

    @property
    def rows(self):
        return len(self.gates) // 4

    def bank(self, width=72):
        self.checkpoint()
        require(type(width) is int and width > 0, "Concrete bank width")
        start = self.qubits
        self.qubits += width
        require(self.qubits <= MAX_QUBITS, "Fixed finite native wire cap within int32 ABI")
        return list(range(start, self.qubits))

    def gate(self, *wires):
        self.checkpoint()
        require(
            1 <= len(wires) <= 3
            and self.rows < MAX_ROWS
            and len(set(wires)) == len(wires)
            and all(type(wire) is int and 0 <= wire < self.qubits for wire in wires),
            "Canonical bounded X/CX/CCX row",
        )
        self.gates.extend((len(wires), *wires, *([0] * (3 - len(wires)))))

    def inverse(self, begin, end):
        require(0 <= begin <= end <= self.rows, "Literal original interval")
        for index in range(end - 1, begin - 1, -1):
            self.checkpoint()
            offset = 4 * index
            kind = self.gates[offset]
            self.gate(*self.gates[offset + 1 : offset + 1 + kind])


def leaf_size(descriptor):
    return descriptor["qubits"] if "qubits" in descriptor else descriptor["resources"]["qubits"]


class Prototype:
    def __init__(self, leaves, checkpoint, circuit=None):
        require(set(leaves) == {"ADD", "SUB", "MUL", "ROUND"}, "Exactly four admitted leaf maps")
        self.p = Circuit(checkpoint) if circuit is None else circuit
        self.input, self.output = self.p.bank(), self.p.bank()
        self.leaves = leaves
        self.workspace = self.p.bank(max(leaf_size(item["descriptor"]) for item in leaves.values()))
        require(len(self.workspace) >= 653, "One complete reusable private leaf bank")
        self.trace = []

    def primitive(self, name, args):
        leaf = self.leaves[name]
        d, words = leaf["descriptor"], leaf["words"]
        arity = 1 if name == "ROUND" else 2
        require(len(args) == arity and all(len(bank) == 72 for bank in args), "Full argument ABI")
        require(
            d["args"] == [list(range(72 * j, 72 * (j + 1))) for j in range(arity)]
            and d["outs"] == [list(range(72 * arity, 72 * (arity + 1)))],
            "Exact admitted leaf ports",
        )
        size = leaf_size(d)
        rows = d["gate_rows"] if "gate_rows" in d else d["resources"]["source_gates"]
        require(len(words) == 4 * rows and size <= len(self.workspace), "Complete actual leaf rows")
        if name in {"ADD", "SUB"}:
            require(
                d["spec"]["width"] == 72
                and d["spec"]["op"] == name.lower()
                and d["spec"]["lowering"] == "clean-xor-prefix-add-sub-v1"
                and d["spec"]["variant"] == "brent-kung"
                and not d["spec"].get("input_contract"),
                "Only measured generic raw BK72 ADD/SUB",
            )
        elif name == "MUL":
            require(
                d["op"] == "mul"
                and d["spec"]["width"] == 72
                and d["spec"]["fraction_bits"] == 44
                and d["spec"]["product_width"] == 116
                and d["spec"]["active_operand_bits"] == [52, 38],
                "Actual paid K F44 leaf",
            )
        else:
            require(
                d["op"] == "round_ties_even"
                and d["spec"]["width"] == 72
                and d["spec"]["input_fraction_bits"] == 44
                and d["spec"]["output_fraction_bits"] == 40,
                "Actual paid K signed rounder",
            )
        output = self.p.bank()
        begin = self.p.rows
        for j, bank in enumerate(args):
            for bit in range(72):
                self.p.gate(bank[bit], self.workspace[72 * j + bit])
        body = self.p.rows
        mapping = list(self.workspace[:size])
        mapping[72 * arity : 72 * (arity + 1)] = output
        for offset in range(0, len(words), 4):
            self.p.checkpoint()
            kind, a, b, c = words[offset : offset + 4]
            operands = (a, b, c)[:kind]
            require(
                kind in (1, 2, 3)
                and len(set(operands)) == kind
                and all(0 <= wire < size for wire in operands)
                and all(value == 0 for value in (a, b, c)[kind:]),
                "Every admitted native row",
            )
            self.p.gate(*(mapping[wire] for wire in operands))
        body_end = self.p.rows
        for j, bank in enumerate(args):
            for bit in range(72):
                self.p.gate(bank[bit], self.workspace[72 * j + bit])
        self.trace.append(
            {
                "op": name,
                "args": args,
                "outs": [output],
                "rows": [begin, self.p.rows],
                "actual_leaf_rows": [body, body_end],
                "inner_argument_copy_CX": 144 * arity,
                "leaf_gate_SHA256": leaf["gate_SHA256"],
                "full_private_bank_reused": True,
            }
        )
        return output

    def helper(self, name, args=(), params=None, outputs=1):
        require(all(len(bank) == 72 for bank in args), "Every helper argument is full72")
        params = {} if params is None else params
        output = [self.p.bank() for _ in range(outputs)]
        arity = len(args)
        wargs = [self.workspace[72 * j : 72 * (j + 1)] for j in range(arity)]
        wouts = [self.workspace[72 * (arity + j) : 72 * (arity + j + 1)] for j in range(outputs)]
        scratch = self.workspace[72 * (arity + outputs) :]
        require(all(len(bank) == 72 for bank in wouts), "Full private result banks")
        begin = self.p.rows
        for source, target in zip(args, wargs, strict=True):
            for a, b in zip(source, target, strict=True):
                self.p.gate(a, b)
        compute = self.p.rows
        helper_compute(self.p, name, wargs, wouts, scratch, params)
        end = self.p.rows
        for source, target in zip(wouts, output, strict=True):
            for a, b in zip(source, target, strict=True):
                self.p.gate(a, b)
        copy_end = self.p.rows
        self.p.inverse(compute, end)
        inverse_end = self.p.rows
        for source, target in zip(args, wargs, strict=True):
            for a, b in zip(source, target, strict=True):
                self.p.gate(a, b)
        self.trace.append(
            {
                "op": name,
                "args": list(args),
                "outs": output,
                "params": params,
                "rows": [begin, self.p.rows],
                "compute_rows": [compute, end],
                "copy_rows": [end, copy_end],
                "inverse_rows": [copy_end, inverse_end],
                "inner_argument_copy_CX": 144 * arity,
                "full_private_bank_reused": True,
            }
        )
        return output[0] if outputs == 1 else output


def helper_compute(p, name, args, outs, scratch, params):
    """Fixed native helper recurrences; outputs/scratch initially zero."""
    if name == "CONST":
        require(not args and len(outs) == 1 and set(params) == {"raw"}, "One raw constant")
        raw = params["raw"]
        require(type(raw) is int and -(1 << 71) <= raw < 1 << 71, "Signed full72 literal")
        raw &= (1 << 72) - 1
        for bit in range(72):
            p.checkpoint()
            if (raw >> bit) & 1:
                p.gate(outs[0][bit])
    elif name in {"SHIFT4", "ADDRESS34", "SIGN", "NOT", "AND"}:
        require(len(outs) == 1 and not params, "Fixed Boolean/shift helper")
        if name == "SHIFT4":
            require(len(args) == 1, "One shift input")
            for bit in range(4, 72):
                p.gate(args[0][bit - 4], outs[0][bit])
        elif name == "ADDRESS34":
            require(len(args) == 1, "One unsigned address input")
            for bit in range(38):
                p.gate(args[0][bit + 34], outs[0][bit])
        elif name == "SIGN":
            require(len(args) == 1, "One sign input")
            p.gate(args[0][71], outs[0][0])
        elif name == "NOT":
            require(len(args) == 1, "One Boolean input")
            p.gate(outs[0][0])
            p.gate(args[0][0], outs[0][0])
        else:
            require(len(args) == 2, "Two Boolean inputs")
            p.gate(args[0][0], args[1][0], outs[0][0])
    elif name == "SELECT":
        require(
            len(args) == 3 and len(outs) == 1 and not params and len(scratch) >= 72,
            "Full72 controlled selection",
        )
        flag, yes, no = args
        delta = scratch[:72]
        for bit in range(72):
            p.gate(no[bit], outs[0][bit])
            p.gate(yes[bit], delta[bit])
            p.gate(no[bit], delta[bit])
            p.gate(flag[0], delta[bit], outs[0][bit])
    elif name == "EQ":
        require(
            len(args) == 2 and len(outs) == 1 and not params and len(scratch) >= 143,
            "Full72 equality",
        )
        delta, prefix = scratch[:72], scratch[72:143]
        for bit in range(72):
            p.gate(args[0][bit], delta[bit])
            p.gate(args[1][bit], delta[bit])
            p.gate(delta[bit])
        p.gate(delta[0], delta[1], prefix[0])
        for bit in range(2, 72):
            p.gate(prefix[bit - 2], delta[bit], prefix[bit - 1])
        p.gate(prefix[70], outs[0][0])
    elif name == "SIGNED_LT":
        require(
            len(args) == 2 and len(outs) == 1 and not params and len(scratch) >= 217,
            "One complete signed72 borrow comparator",
        )
        a, b = args
        p.gate(a[71])
        p.gate(b[71])
        neq, nota, borrow = scratch[:72], scratch[72:144], scratch[144:217]
        for bit in range(72):
            p.gate(neq[bit])
            p.gate(a[bit], neq[bit])
            p.gate(b[bit], neq[bit])
            p.gate(nota[bit])
            p.gate(a[bit], nota[bit])
            p.gate(nota[bit], b[bit], borrow[bit + 1])
            p.gate(neq[bit], borrow[bit], borrow[bit + 1])
        p.gate(borrow[72], outs[0][0])
        p.gate(a[71])
        p.gate(b[71])
    elif name == "QROM64x8":
        require(
            len(args) == 1 and len(outs) == 8 and set(params) == {"table"} and len(scratch) >= 5,
            "One fixed full72-address eight-output QROM",
        )
        table, address, prefix = params["table"], args[0], scratch[:5]
        require(
            type(table) is list
            and len(table) == 64
            and all(type(row) is list and len(row) == 8 for row in table),
            "Complete512 literal table",
        )
        for index, row in enumerate(table):
            p.checkpoint()
            negative = [bit for bit in range(6) if not (index >> bit) & 1]
            for bit in negative:
                p.gate(address[bit])
            p.gate(address[0], address[1], prefix[0])
            for bit in range(2, 6):
                p.gate(prefix[bit - 2], address[bit], prefix[bit - 1])
            for word, bank in zip(row, outs, strict=True):
                require(type(word) is int and -(1 << 71) <= word < 1 << 71, "Full72 lookup literal")
                raw = word & ((1 << 72) - 1)
                for bit in range(72):
                    p.checkpoint()
                    if (raw >> bit) & 1:
                        p.gate(prefix[4], bank[bit])
            for bit in range(5, 1, -1):
                p.gate(prefix[bit - 2], address[bit], prefix[bit - 1])
            p.gate(address[0], address[1], prefix[0])
            for bit in reversed(negative):
                p.gate(address[bit])
    else:
        raise ValueError("Unrecognized fixed native helper")


def build_cosine(table, leaves, checkpoint, *, matching=None):
    require(
        type(table) is list
        and len(table) == 64
        and all(type(row) is list and len(row) == 8 for row in table),
        "Complete512 fixed literals",
    )
    for index, row in enumerate(table):
        checkpoint()
        require(row[0] == (2 * index + 1) << 37, "Exact64 F44 centers")
    c = Prototype(leaves, checkpoint, matching)
    p = c.p
    zero, one, minus = (c.helper("CONST", params={"raw": raw}) for raw in (0, Q, -Q))
    sign = c.helper("SIGN", [c.input])
    below = c.helper("SIGNED_LT", [c.input, one])
    upper = c.helper("SELECT", [below, c.input, one])
    clamped = c.helper("SELECT", [sign, zero, upper])
    is_Q = c.helper("EQ", [clamped, one])
    eager = c.helper("SELECT", [is_Q, zero, clamped])
    address = c.helper("ADDRESS34", [eager])
    rescaled = c.helper("SHIFT4", [eager])
    center, *coefficients = c.helper("QROM64x8", [address], params={"table": table}, outputs=8)
    local = c.primitive("SUB", [rescaled, center])
    accumulator = coefficients[6]
    horner = []
    for degree in range(5, -1, -1):
        product = c.primitive("MUL", [accumulator, local])
        following = c.primitive("ADD", [product, coefficients[degree]])
        horner.append(
            {
                "degree": degree,
                "accumulator": accumulator,
                "local": local,
                "product": product,
                "coefficient": coefficients[degree],
                "sum": following,
            }
        )
        accumulator = following
    rounded = c.primitive("ROUND", [accumulator])
    low = c.helper("SIGNED_LT", [rounded, minus])
    projected_low = c.helper("SELECT", [low, minus, rounded])
    high = c.helper("SIGNED_LT", [one, projected_low])
    projected = c.helper("SELECT", [high, one, projected_low])
    current, axes = projected, []
    for turn, exact in ((0, zero), (Q // 4, zero), (Q // 2, minus), (3 * Q // 4, zero), (Q, one)):
        # The first axis is +Q, independently of the generic polynomial path.
        if turn == 0:
            exact = one
        point = c.helper("CONST", params={"raw": turn})
        flag = c.helper("EQ", [clamped, point])
        following = c.helper("SELECT", [flag, exact, current])
        axes.append(
            {"turn": turn, "point": point, "flag": flag, "before": current, "after": following}
        )
        current = following
    end = p.rows
    for a, b in zip(current, c.output, strict=True):
        p.gate(a, b)
    reverse = p.rows
    p.inverse(0, end)
    descriptor = {
        "schema": "a14-f44-stage-c-clean-cosine-prototype-v1",
        "row_id": ROW_ID,
        "args": [c.input],
        "outs": [c.output],
        "qubits": p.qubits,
        "gate_rows": p.rows,
        "forward_rows": [0, end],
        "output_XOR_rows": [end, reverse],
        "literal_global_inverse_rows": [reverse, p.rows],
        "trace": c.trace,
        "shared_private_workspace": c.workspace,
        "full72_private_leaf_capacity": len(c.workspace),
        "SSA_full72_banks": (p.qubits - len(c.workspace)) // 72,
        "internal": {
            "clamped": clamped,
            "eager_Q_to_zero": eager,
            "address": address,
            "rescaled": rescaled,
            "center": center,
            "coefficients": coefficients,
            "local": local,
            "Horner": horner,
            "round_input": accumulator,
            "rounded": rounded,
            "projected": projected,
            "axes": axes,
            "final": current,
        },
        "input_full72_signed_clamp_0_to_Q": True,
        "dirty_output_XOR": True,
        "input_preserved": True,
        "private_and_SSA_zero_entry_exit": True,
        "outer_caller_copies_excluded": True,
        "full_financial_or_G2_certificate": False,
        "prototype_native_rows_cap": MAX_ROWS,
        "prototype_native_wire_cap": MAX_QUBITS,
        "replay_guard_rows": REPLAY_GUARD_ROWS,
        "new_test_credit": 0,
    }
    checkpoint()
    return p, descriptor


def signed(word):
    require(type(word) is int and 0 <= word < 1 << 72, "Unsigned full72 raw word")
    return word - (1 << 72) if word >> 71 else word


def scalar_reference(raw, table):
    """Literal integer whole-map reference, called only under ROOT release."""
    clamped = min(Q, max(0, signed(raw)))
    u = 0 if clamped == Q else clamped
    index = u >> 34
    local = (u << 4) - table[index][0]
    require(-(1 << 37) <= local <= (1 << 37) - 16, "Actual discrete signed38 local operand")
    accumulator = table[index][7]
    require(-(1 << 51) <= accumulator < 1 << 51, "Initial signed52 literal")
    for degree in range(5, -1, -1):
        require(-(1 << 51) <= accumulator < 1 << 51, "Each actual K caller is signed52")
        product144 = accumulator * local
        require(-(1 << 143) <= product144 < 1 << 143, "Full semantic signed144 product")
        accumulator = (product144 >> 44) + table[index][degree + 1]
        require(-(1 << 71) <= accumulator < 1 << 71, "Eager raw addition does not wrap")
    quotient, remainder = divmod(accumulator, 16)
    result = quotient + int(remainder > 8 or (remainder == 8 and quotient & 1))
    result = min(Q, max(-Q, result))
    axes = {0: Q, Q // 4: 0, Q // 2: -Q, 3 * Q // 4: 0, Q: Q}
    return axes.get(clamped, result) & ((1 << 72) - 1)


def fixed_native_cases():
    values = (
        -(1 << 71),
        -1,
        0,
        1,
        (1 << 33) - 1,
        1 << 33,
        (1 << 34) - 1,
        1 << 34,
        (1 << 34) + 1,
        Q // 4,
        Q // 2,
        3 * Q // 4,
        Q - 1,
        Q,
        Q + 1,
        (1 << 71) - 1,
    )
    return [(value, dirty) for value in values for dirty in (0, (1 << 72) - 1)]


def replay(circuit, state, checkpoint, inverse=False):
    checkpoint()
    require(
        0 < circuit.qubits <= MAX_QUBITS
        and circuit.rows <= MAX_ROWS
        and len(circuit.gates) == 4 * circuit.rows,
        "Complete finite actual native array and wire allocation",
    )
    require(
        type(state) is int and 0 <= state < 1 << circuit.qubits, "Complete allocated wire state"
    )
    if getattr(circuit, "_replay_masks", None) is None:
        masks = []
        for wire in range(circuit.qubits):
            if wire % REPLAY_GUARD_ROWS == 0:
                checkpoint()
            masks.append(1 << wire)
        circuit._replay_masks = tuple(masks)
    masks = circuit._replay_masks
    require(len(masks) == circuit.qubits, "Exact immutable wire masks for this allocation")
    gates = circuit.gates
    indices = range(circuit.rows - 1, -1, -1) if inverse else range(circuit.rows)
    for step, index in enumerate(indices):
        if step % REPLAY_GUARD_ROWS == 0:
            checkpoint()
        offset = 4 * index
        kind, a, b, c = gates[offset], gates[offset + 1], gates[offset + 2], gates[offset + 3]
        if kind == 1:
            state ^= masks[a]
        elif kind == 2:
            if state & masks[a]:
                state ^= masks[b]
        else:
            require(kind == 3, "Recognized actual native replay row")
            if state & masks[a] and state & masks[b]:
                state ^= masks[c]
    checkpoint()
    return state


def resources(circuit, checkpoint, descriptor=None):
    counts, t_level, ct_level = [0, 0, 0], [0] * circuit.qubits, [0] * circuit.qubits
    for offset in range(0, len(circuit.gates), 4):
        checkpoint()
        kind, a, b, c = circuit.gates[offset : offset + 4]
        counts[kind - 1] += 1
        wires = (a, b, c)
        events = MACRO if kind == 3 else (("CX", 0, 1),) if kind == 2 else (("X", 0),)
        for event in events:
            checkpoint()
            touched = [wires[bit] for bit in event[1:]]
            td = max(t_level[wire] for wire in touched) + int(event[0] in {"T", "TD"})
            cd = max(ct_level[wire] for wire in touched) + 1
            for wire in touched:
                t_level[wire], ct_level[wire] = td, cd
    x, cx, ccx = counts
    result = {
        "qubits": circuit.qubits,
        "source_gates": circuit.rows,
        "x": x,
        "cx": cx,
        "ccx": ccx,
        "t_count": 7 * ccx,
        "t_depth": max(t_level),
        "clifford_t_depth": max(ct_level),
        "clifford_cx": cx + 6 * ccx,
        "clifford_h": 2 * ccx,
        "schedule": "all-to-all ASAP full actual chronological exact7T expansion",
        "entire_clean_prototype_not_leaf_sum_estimate": True,
        "outer_caller_copies_excluded": True,
    }
    if descriptor is not None:
        result["matched_serial_event_chronology"] = serial_resources(
            circuit, descriptor, checkpoint
        )
    return result


class MatchingCircuit(Circuit):
    """Consume the existing array against the fixed recurrence; emit no second array."""

    def __init__(self, actual, checkpoint):
        require(callable(checkpoint), "Mandatory structural checkpoint")
        self.checkpoint, self.qubits, self.gates = checkpoint, 0, actual.gates
        self.cursor = 0

    @property
    def rows(self):
        return self.cursor

    def gate(self, *wires):
        self.checkpoint()
        require(
            1 <= len(wires) <= 3
            and self.cursor < MAX_ROWS
            and len(set(wires)) == len(wires)
            and all(type(wire) is int and 0 <= wire < self.qubits for wire in wires),
            "Every consumed native row is canonical",
        )
        expected = (len(wires), *wires, *([0] * (3 - len(wires))))
        require(
            tuple(self.gates[4 * self.cursor : 4 * self.cursor + 4]) == expected,
            "Every actual prototype row matches the exact fixed helper/leaf recurrence",
        )
        self.cursor += 1


def verify_prototype(circuit, descriptor, table, leaves, checkpoint):
    consumer = MatchingCircuit(circuit, checkpoint)
    matched, expected_descriptor = build_cosine(table, leaves, checkpoint, matching=consumer)
    require(
        matched.rows == circuit.rows
        and matched.qubits == circuit.qubits
        and len(circuit.gates) == 4 * circuit.rows
        and descriptor == expected_descriptor,
        "Complete actual array, allocation, ABI and every recurrence descriptor consumed",
    )
    return {
        "actual_array_and_allocation_matched": True,
        "second_gate_array_generated": False,
        "primary_consumes_same_fixed_recurrence_not_independent_audit": True,
        "independent_scientific_audit_still_required": True,
        "universal_map_requires_all64_segment_native_promises": True,
        "absolute_phase_from_exact_X_CX_and_K_authorized_7T_CCX": True,
        "identities": [
            "Biasing both sign bits orders signed72 exactly as unsigned72.",
            "borrow_next=(~a & b) XOR (~(a XOR b) & borrow); its terms are disjoint.",
            "SELECT output=no XOR(flag AND(yes XOR no)); every output has full72 dirty-XOR ports.",
            "EQ complements all72 XOR differences then ANDs them; "
            "every prefix/history is reversed.",
            "QROM tests all64 complete six-bit addresses, pays actual signed72 "
            "literal popcounts and resets equality history.",
            "Clamp+Q-to-zero precedes eager shift/address/center/local operations; "
            "actual local range is signed38.",
            "Every actual K signed52x38 call is authorized by the separate "
            "all64-segment native range certificate.",
            "Actual raw full72 ADD/SUB maps are fraction-label independent "
            "and have separate signed no-wrap proofs.",
            "K rounding is exact signed ties-even; signed projection and "
            "exact-axis selections cannot enlarge cosine error.",
            "Each inner clean leaf preserves full arguments and cleans shared "
            "workspace; full F/output72XOR/F^-1 cleans every SSA bank.",
            "All native gates have exact absolute phase; whole-input clean-XOR "
            "proof applies to superpositions in the certified domain.",
        ],
        "full_financial_G2_or_source_adoption": False,
        "new_test_credit": 0,
    }


def interval_depth(circuit, begin, end, checkpoint):
    require(0 <= begin <= end <= circuit.rows, "Concrete actual event interval")
    t, ct, count = [0] * circuit.qubits, [0] * circuit.qubits, [0, 0, 0]
    for index in range(begin, end):
        checkpoint()
        kind, a, b, c = circuit.gates[4 * index : 4 * index + 4]
        count[kind - 1] += 1
        wires = (a, b, c)
        events = MACRO if kind == 3 else (("CX", 0, 1),) if kind == 2 else (("X", 0),)
        for event in events:
            checkpoint()
            affected = [wires[position] for position in event[1:]]
            td = max(t[wire] for wire in affected) + int(event[0] in {"T", "TD"})
            cd = max(ct[wire] for wire in affected) + 1
            for wire in affected:
                t[wire], ct[wire] = td, cd
    return {
        "rows": [begin, end],
        "source_gates": end - begin,
        "x": count[0],
        "cx": count[1],
        "ccx": count[2],
        "t_count": 7 * count[2],
        "t_depth": max(t),
        "clifford_t_depth": max(ct),
    }


def serial_resources(circuit, descriptor, checkpoint):
    """Full actual event rows; reset clocks only to impose conservative serial barriers."""
    end = descriptor["forward_rows"][1]
    reverse = descriptor["literal_global_inverse_rows"][0]
    forward, inverse, position = [], [], 0
    for event in descriptor["trace"]:
        begin, finish = event["rows"]
        require(
            begin == position and begin <= finish <= end, "Exact contiguous complete forward events"
        )
        forward.append({"op": event["op"], **interval_depth(circuit, begin, finish, checkpoint)})
        position = finish
    require(position == end, "Every forward row belongs to an actual event")
    output = interval_depth(circuit, end, reverse, checkpoint)
    require(
        output["source_gates"] == 72 and output["x"] == output["ccx"] == 0,
        "Exact full72 dirty output copy event",
    )
    for event in reversed(descriptor["trace"]):
        begin, finish = event["rows"]
        actual_begin, actual_end = reverse + end - finish, reverse + end - begin
        inverse.append(
            {"op": event["op"], **interval_depth(circuit, actual_begin, actual_end, checkpoint)}
        )
    events = forward + [output] + inverse
    sums = {
        key: sum(event[key] for event in events)
        for key in ("source_gates", "x", "cx", "ccx", "t_count", "t_depth", "clifford_t_depth")
    }
    require(
        sums["source_gates"] == circuit.rows and sums["t_count"] == 7 * sums["ccx"],
        "Serialized chronology consumes every actual row exactly once",
    )
    return {
        "forward_actual_events": forward,
        "output_XOR_actual_event": output,
        "inverse_actual_events": inverse,
        "sums": sums,
        "schedule": "serialize complete helper/leaf events; exact actual7T ASAP within each event",
        "matched_serial_whole_source_comparison_only": True,
        "distinct_from_standalone_ASAP_depth": True,
        "outer_caller_argument_copies_excluded": True,
    }
