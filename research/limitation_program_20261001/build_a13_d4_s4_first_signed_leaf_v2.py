"""Prospective first ordered d4_s4 signed multiplication leaf; author-only.

Exact completed inventory and independent audit bindings require new ROOT release.
Every public bank stays72 bits; modular112 computation retains all low carries.
Only a separately reviewed controller/READY may construct an actual array.
"""

from array import array

W, F, RESIDUE_BITS = 72, 40, 112
MAX_ROWS, MAX_WIRES = 1_000_000, 32768
EXPECTED_ROW_ID, EXPECTED_VALUE, EXPECTED_ORDERED_ARGS = "d4_s4", 6, (0, 2)
EXPECTED_INVENTORY_MANIFEST_SHA256 = "a5b51dde9ac50bb742fa571d35182128f361d99e0b9d11cc427e505029c14eae"
EXPECTED_INVENTORY_COMPLETE_COUNTS = [31, 1547, 2842]
EXPECTED_INDEPENDENT_INVENTORY_VERIFICATION_SHA256 = "387926b180770fa08a2308bf107e88bf42b1d3439a3bfd0c7b2e630a86fa9cb1"
EXPECTED_NATIVE_AUDIT_MANIFEST_SHA256 = "c6583d3a46da731dc26cf5fa2e1b1056ef951543f81c8247f289ad717b31e70b"
EXPECTED_NATIVE_AUDIT_COMPLETE_COUNTS = [37, 1584, 2842]
EXPECTED_ORDERED_ACTIVE_WIDTHS = [38, 42]
EXPECTED_COMPLETE_ORDERED_ABI_SIGNATURE = {'coherent_absolute_unit_phase_and_literal_inverse_required': True, 'fraction_bits': 40, 'input_ports': [72, 72], 'leaf_lowering_selected_or_emitted': False, 'lower40_columns_and_all_signed_correction_carries_must_be_proved': True, 'mathematical_signed_product_width': 144, 'ordered_active_signed_widths': [38, 42], 'output_port': 72, 'output_semantics': 'dirty72 XOR ((signed72(a)*signed72(b) >>40) mod2^72)', 'possible_low_residue_implementation_bits': 112, 'required_promised_span': 'all sign-extended ordered active signed operands, arbitrary dirty72 output, zero private workspace'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


class Circuit:
    def __init__(self, checkpoint):
        require(callable(checkpoint), "Mandatory fixed-budget callback")
        require(array("i").itemsize == 4, "Strict signed-int32 row words")
        self.checkpoint = checkpoint
        self.qubits = 0
        self.gates = array("i")

    @property
    def rows(self):
        return len(self.gates) // 4

    def register(self, bits):
        self.checkpoint()
        require(type(bits) is int and bits > 0, "Concrete positive width")
        start = self.qubits
        require(start + bits <= MAX_WIRES, "Fixed prospective allocated-wire guard")
        self.qubits += bits
        return list(range(start, self.qubits))

    def gate(self, *wires):
        self.checkpoint()
        require(1 <= len(wires) <= 3 and self.rows < MAX_ROWS, "Finite X/CX/CCX rows")
        require(
            all(type(wire) is int and 0 <= wire < self.qubits for wire in wires)
            and len(set(wires)) == len(wires),
            "Distinct actual native gate operands",
        )
        self.gates.extend((len(wires), *wires, *([0] * (3 - len(wires)))))
        self.checkpoint()

    def reverse_compute(self, begin, end):
        self.checkpoint()
        require(0 <= begin <= end <= self.rows, "Exact retained compute interval")
        for index in range(end - 1, begin - 1, -1):
            self.checkpoint()
            offset = 4 * index
            kind = self.gates[offset]
            self.gate(*self.gates[offset + 1 : offset + 1 + kind])


def authorize_contract(binding, contract):
    """Reject null prerequisites before any plane, allocation or gate construction."""
    required = (
        EXPECTED_INVENTORY_MANIFEST_SHA256,
        EXPECTED_INVENTORY_COMPLETE_COUNTS,
        EXPECTED_INDEPENDENT_INVENTORY_VERIFICATION_SHA256,
        EXPECTED_ORDERED_ACTIVE_WIDTHS,
        EXPECTED_COMPLETE_ORDERED_ABI_SIGNATURE,
    )
    require(all(value is not None for value in required), "Exact completed independently audited inventory release")
    require(
        binding["inventory_manifest_SHA256"] == EXPECTED_INVENTORY_MANIFEST_SHA256
        and binding["inventory_complete_counts"] == EXPECTED_INVENTORY_COMPLETE_COUNTS
        and binding["independent_inventory_verification_SHA256"]
        == EXPECTED_INDEPENDENT_INVENTORY_VERIFICATION_SHA256
        and binding["native_audit_manifest_SHA256"] == EXPECTED_NATIVE_AUDIT_MANIFEST_SHA256
        and binding["native_audit_complete_counts"] == EXPECTED_NATIVE_AUDIT_COMPLETE_COUNTS
        and binding["separate_first_standalone_leaf_ROOT_release"] is True
        and binding["row_id"] == EXPECTED_ROW_ID
        and binding["complete_maps_and_owned_inventories_verified"] is True
        and binding["all240_native_slots_verified"] is True,
        "Only separately verified exact selected inventory may supply operands",
    )
    require(
        contract["value"] == EXPECTED_VALUE
        and contract["ordered_args"] == list(EXPECTED_ORDERED_ARGS)
        and contract["complete_ordered_ABI_signature"] == EXPECTED_COMPLETE_ORDERED_ABI_SIGNATURE
        and contract["hull_covers_both_cases_every_reachable_segment_class"] is True
        and contract["runtime_operand_swap_or_width_switch"] is False,
        "First exact ordered v6=(v0,v2) contract only, no source-call substitution",
    )
    widths = EXPECTED_ORDERED_ACTIVE_WIDTHS
    signature = EXPECTED_COMPLETE_ORDERED_ABI_SIGNATURE
    require(
        type(widths) is list
        and len(widths) == 2
        and all(type(value) is int and 1 <= value <= W for value in widths)
        and signature["ordered_active_signed_widths"] == widths
        and signature["input_ports"] == [W, W]
        and signature["output_port"] == W
        and signature["fraction_bits"] == F
        and signature["mathematical_signed_product_width"] == 144
        and signature["possible_low_residue_implementation_bits"] == RESIDUE_BITS
        and signature["coherent_absolute_unit_phase_and_literal_inverse_required"] is True
        and signature["lower40_columns_and_all_signed_correction_carries_must_be_proved"] is True
        and signature["leaf_lowering_selected_or_emitted"] is False,
        "Immutable ordered full72/F40/signed144 ABI with no runtime width dispatch",
    )
    return tuple(widths)


def signed_planes(left_bits, right_bits, checkpoint):
    """Exact sign-complement terms modulo112; no lower column is omitted."""
    require(
        type(left_bits) is int
        and type(right_bits) is int
        and 1 <= left_bits <= W
        and 1 <= right_bits <= W,
        "Concrete ordered sign-extension widths",
    )
    terms, correction = [], 0
    for i in range(right_bits):
        for j in range(min(left_bits, RESIDUE_BITS - i)):
            checkpoint()
            negative = (j == left_bits - 1) != (i == right_bits - 1)
            terms.append((j, i, j + i, negative))
            if negative:
                correction -= 1 << (j + i)
    return terms, correction & ((1 << RESIDUE_BITS) - 1)


def build_first_leaf(binding, contract, checkpoint):
    """Only separately ROOT-released full72 dirty XOR of signed144 floor40."""
    left_bits, right_bits = authorize_contract(binding, contract)
    require(callable(checkpoint), "Mandatory bounded-work callback")
    terms, correction = signed_planes(left_bits, right_bits, checkpoint)
    p = Circuit(checkpoint)
    a, b, out = (p.register(W) for _ in range(3))
    columns = [[] for _ in range(RESIDUE_BITS)]
    partials, fixed = [], []
    begin = p.rows
    for j, i, column, negative in terms:
        checkpoint()
        value = p.register(1)[0]
        if negative:
            p.gate(value)
        p.gate(a[j], b[i], value)
        columns[column].append(value)
        partials.append(dict(a_bit=j, b_bit=i, column=column, negative=negative, wire=value))
    for column in range(RESIDUE_BITS):
        checkpoint()
        if (correction >> column) & 1:
            value = p.register(1)[0]
            p.gate(value)
            columns[column].append(value)
            fixed.append(dict(column=column, wire=value))
    layers = []
    while max(map(len, columns)) > 2:
        checkpoint()
        following = [[] for _ in range(RESIDUE_BITS)]
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
                if column + 1 < RESIDUE_BITS:
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
    left, right, product = (p.register(RESIDUE_BITS) for _ in range(3))
    for column, values in enumerate(columns):
        checkpoint()
        if values:
            p.gate(values[0], left[column])
        if len(values) == 2:
            p.gate(values[1], right[column])
    propagate = p.register(RESIDUE_BITS)
    carry = p.register(RESIDUE_BITS + 1)
    for bit in range(RESIDUE_BITS):
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
        "schema": "a13-d4-s4-first-ordered-signed-leaf-descriptor-v1",
        "row_id": EXPECTED_ROW_ID,
        "value": EXPECTED_VALUE,
        "ordered_args": list(EXPECTED_ORDERED_ARGS),
        "op": "mul",
        "params": {},
        "spec": {
            "width": W,
            "fraction_bits": F,
            "product_width": RESIDUE_BITS,
            "active_operand_bits": [left_bits, right_bits],
            "input_contract": {"signed_operand_bits": [left_bits, right_bits]},
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
        "product_modulus_bits": RESIDUE_BITS,
        "constructed_only_under_separate_first_leaf_ROOT_release": True,
        "actual_cost_or_source_transfer_claim": False,
    }
    checkpoint()
    return p, descriptor


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
