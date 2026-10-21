"""Caller-grid-only clamp-free Stage C component; no import-time evaluation.

The verified clamp builder is retained except its QROM event is the entire
immutable saved shared-prefix wrapper. All other emitter/helper ASTs remain
exact. Full72 input must already belong to D; preparation/bridge/source open.
"""

from array import array


W, Q, F = 72, 1 << 40, 44


MAX_ROWS = 2_000_000


MAX_QUBITS = 16_384


REPLAY_GUARD_ROWS = 128


ROW_ID = "TAYLOR_D6_S64_W72_F44_TO_F40_MUL52x38_CALLER_GRID_NO_AXIS_NO_INPUT_CLAMP_SHARED_QROM"


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

    def shared_qrom(self, address, table, admitted):
        """Splice one entire immutable clean wrapper; never nest a second wrapper."""
        require(
            len(address) == 72 and set(admitted) == {"descriptor", "words", "gate_SHA256"},
            "Full72 address and separately admitted saved QROM",
        )
        d, words = admitted["descriptor"], admitted["words"]
        require(
            d["algorithm"] == "shared"
            and d["qubits"] == 1301
            and d["args"] == [list(range(72))]
            and d["outs"] == [list(range(72 + 72 * j, 144 + 72 * j)) for j in range(8)]
            and d["private_address"] == list(range(648, 720))
            and d["private_outs"] == [list(range(720 + 72 * j, 792 + 72 * j)) for j in range(8)]
            and d["clean_prefix_ancillas"] == list(range(1296, 1301))
            and d["dirty_output_XOR"] is True
            and d["input_preserved"] is True
            and d["private648_and_prefix5_zero_entry_exit"] is True
            and d["rows"] == len(words) // 4
            and len(words) % 4 == 0,
            "Exact saved complete1301-wire dirty576 clean653 wrapper ABI",
        )
        output = [self.p.bank() for _ in range(8)]
        mapping = list(address) + [wire for bank in output for wire in bank] + self.workspace[:653]
        require(
            len(mapping) == 1301 and len(set(mapping)) == 1301,
            "Public address/output and complete private653 bijection",
        )
        begin = self.p.rows
        for offset in range(0, len(words), 4):
            self.p.checkpoint()
            kind, a, b, c = words[offset : offset + 4]
            operands = (a, b, c)[:kind]
            require(
                kind in (1, 2, 3)
                and len(set(operands)) == kind
                and all(0 <= wire < 1301 for wire in operands)
                and all(value == 0 for value in (a, b, c)[kind:]),
                "Every immutable saved canonical QROM row",
            )
            self.p.gate(*(mapping[wire] for wire in operands))
        self.trace.append(
            {
                "op": "QROM64x8",
                "args": [address],
                "outs": output,
                "params": {"table": table},
                "rows": [begin, self.p.rows],
                "compute_rows": [begin + value for value in d["body_rows"]],
                "copy_rows": [begin + value for value in d["output_XOR_rows"]],
                "inverse_rows": [begin + value for value in d["literal_body_inverse_rows"]],
                "inner_argument_copy_CX": 144,
                "full_private_bank_reused": True,
                "saved_whole_shared_wrapper": True,
                "saved_wrapper_gate_SHA256": admitted["gate_SHA256"],
                "saved_wrapper_qubits": 1301,
                "complete_private653_mapping": self.workspace[:653],
            }
        )
        return output


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


def build_caller_grid_cosine(table, leaves, checkpoint, *, shared_qrom, matching=None):
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
    one, minus = (c.helper("CONST", params={"raw": raw}) for raw in (Q, -Q))
    # Under the separately admitted full72 D promise, both roles equal the input.
    clamped, eager = c.input, c.input
    address = c.helper("ADDRESS34", [eager])
    rescaled = c.helper("SHIFT4", [eager])
    center, *coefficients = c.shared_qrom(address, table, shared_qrom)
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
    end = p.rows
    for a, b in zip(current, c.output, strict=True):
        p.gate(a, b)
    reverse = p.rows
    p.inverse(0, end)
    descriptor = {
        "schema": "f44-caller-grid-no-axis-no-input-clamp-shared-qrom-clean-prototype-v1",
        "row_id": ROW_ID,
        "caller_grid_contract_id": "Q32_MIDPOINT_MOD256_128_M_OR_WRAP3Q4",
        "certificate_scope": "PROMISED_CALLER_GRID_ONLY",
        "axis_tail_omitted": True,
        "generic_full72_equivalence_claimed": False,
        "actual_coherent32_preparation_array_audited": False,
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
        "input_full72_signed_clamp_0_to_Q": False,
        "input_clamp_and_eager_Q_gate_events_omitted": True,
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
