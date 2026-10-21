"""Unexecuted producer for one H32/template and two saved shared-QROM component wrappers.

H has a separate JSON representation. Native rows remain X/CX/CCX. The
producer does not import or regenerate any historical component or QROM.
"""

from array import array


SHARED_DESCRIPTOR_SCHEMA = 'f44-caller-grid-no-axis-no-input-clamp-shared-qrom-clean-prototype-v1'
PAID_COMPONENT_ROW_ID = 'TAYLOR_D6_S64_W72_F44_TO_F40_MUL52x38_CALLER_GRID_NO_AXIS_NO_INPUT_CLAMP_SHARED_QROM'
PAID_COMPONENT_MANIFEST_SHA256 = '59d624529f7a8b991bd176f4dac85271185d570c98e53d403d2c45df7d8cd493'

MAX_ROWS = 2_000_000
MAX_QUBITS = 16_384
REPLAY_GUARD_ROWS = 128
ROW_ID = 'F44_Q32_H32_TWO_COMPACT40_TWO_PAID_SHARED_QROM_WRAPPERS_V1'
H_SCHEMA = "f44-separate-positive-H32-records-v1"
MACRO = (
    ("H", 2), ("CX", 1, 2), ("TD", 2), ("CX", 0, 2), ("T", 2),
    ("CX", 1, 2), ("TD", 2), ("CX", 0, 2), ("T", 1), ("T", 2),
    ("H", 2), ("CX", 0, 1), ("T", 0), ("TD", 1), ("CX", 0, 1),
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
            self.gate(*self.gates[offset + 1:offset + 1 + kind])


def H32_records(targets, *, inverse=False):
    require(type(targets) is list and len(targets) == len(set(targets)) == 32,
            "Exactly one injective q32 target list")
    require(type(inverse) is bool, "Explicit H direction")
    ordered = list(reversed(targets)) if inverse else list(targets)
    return {
        "schema": H_SCHEMA,
        "direction": "inverse" if inverse else "forward",
        "native_Nx4_reinterpreted": False,
        "targets_in_logical_little_endian_order": list(targets),
        "records": [{"op": "H", "target": target} for target in ordered],
        "exact_field": "Q(sqrt(2)); sqrt(2) is the positive real root",
        "matrix_columns_Qsqrt2_pairs": [
            [["0", "1/2"], ["0", "1/2"]],
            [["0", "1/2"], ["0", "-1/2"]],
        ],
        "zero_entry_source_required": True,
        "sampled_uniformity_claim": False,
    }


def build_preparation_wrapper(saved_words, paid_descriptor, checkpoint, original_first_arguments):
    """Emit only after complete external release/admission; no import-time work."""
    require(paid_descriptor["qubits"] > 144
            and paid_descriptor["args"] == [list(range(72))]
            and paid_descriptor["outs"] == [list(range(72, 144))]
            and len(saved_words) == 4 * paid_descriptor["gate_rows"],
            "One complete immutable paid clamp002 with full72 public ports")
    require(original_first_arguments == {"B4x12": [6, 61], "B8x52": [6, 61]},
            "Original argument IDs, not final polynomial MUL72/92")
    require(paid_descriptor["schema"] == SHARED_DESCRIPTOR_SCHEMA
            and paid_descriptor["row_id"] == PAID_COMPONENT_ROW_ID,
            "Exactly the completed full saved shared-QROM component, never standalone lookup or inner emission")
    p = Circuit(checkpoint)
    n = p.bank(32)
    m = p.bank(40)
    m_neighbors = p.bank(32)
    w = p.bank(40)
    w_neighbors = p.bank(32)
    dirty_m, dirty_w = p.bank(72), p.bank(72)
    argument = p.bank(72)
    private = p.bank(paid_descriptor["qubits"] - 144)
    events, wrappers = [], []

    begin = p.rows
    p.gate(m[7])
    for bit in range(32):
        p.gate(n[bit], m[bit + 8])
    events.append({"op": "ENCODE_M", "rows": [begin, p.rows]})

    begin = p.rows
    for bit in range(40):
        p.gate(m[bit], w[bit])
    p.gate(w[38], w[39])
    p.gate(w[39])
    p.gate(w[38])
    events.append({"op": "ENCODE_W", "rows": [begin, p.rows]})

    for branch, source, output in (("m", m, dirty_m), ("w", w, dirty_w)):
        begin = p.rows
        for bit in range(40):
            p.gate(source[bit], argument[bit])
        body = p.rows
        mapping = argument + output + private
        require(len(mapping) == len(set(mapping)) == paid_descriptor["qubits"],
                "Injective full paid allocation, no private or retained-SSA shortening")
        for index in range(paid_descriptor["gate_rows"]):
            if index % REPLAY_GUARD_ROWS == 0:
                checkpoint()
            kind, a, b, c = saved_words[4 * index:4 * index + 4]
            operands = (a, b, c)[:kind]
            require(kind in (1, 2, 3) and len(set(operands)) == kind
                    and all(0 <= wire < len(mapping) for wire in operands)
                    and all(value == 0 for value in (a, b, c)[kind:]),
                    "Every complete original native opcode/wire/padding")
            p.gate(*(mapping[wire] for wire in operands))
        body_end = p.rows
        for bit in range(39, -1, -1):
            p.gate(source[bit], argument[bit])
        wrappers.append({
            "branch": branch, "source40": list(source), "argument72": list(argument),
            "dirty_output72": list(output), "private_and_retained_SSA": list(private),
            "whole_old_wire_to_new_wire": mapping,
            "rows": [begin, p.rows], "copy_rows": [begin, body],
            "complete_paid_component_rows": [body, body_end],
            "uncopy_rows": [body_end, p.rows],
        })
        events.append({"op": "WRAP_" + branch.upper(), "rows": [begin, p.rows]})

    end = p.rows
    p.inverse(0, end)
    descriptor = {
        "schema": "f44-q32-two-compact40-two-saved-shared-qrom-wrapper-prototype-v1",
        "row_id": ROW_ID, "qubits": p.qubits, "gate_rows": p.rows,
        "paid_component_manifest_SHA256": PAID_COMPONENT_MANIFEST_SHA256,
        "paid_component_row_id": paid_descriptor["row_id"],
        "native_format": "little-endian int32 Nx4 X/CX/CCX",
        "n32": n, "m40": m, "w40": w,
        "m_adjacent32_sentinels": m_neighbors, "w_adjacent32_sentinels": w_neighbors,
        "dirty_m72": dirty_m, "dirty_w72": dirty_w,
        "argument72": argument, "private_and_retained_SSA": private,
        "compact_source_lists": {"m": list(m), "w": list(w)},
        "original_first_argument_values": original_first_arguments,
        "wrap_top_bit_gate_order": ["CX_original_x_to_y", "X_y", "X_x"],
        "events": events, "wrappers": wrappers,
        "arithmetic_forward_rows": [0, end], "actual_arithmetic_inverse_rows": [end, p.rows],
        "composition_chronology": [
            "H32", "ENCODE_M", "ENCODE_W", "WRAP_M", "WRAP_W",
            "WRAP_W_inverse", "WRAP_M_inverse", "ENCODE_W_inverse", "ENCODE_M_inverse",
            "H32_inverse",
        ],
        "zero_entry_uniform_source_required": True,
        "dirty_outputs_full72_arbitrary": True,
        "high32_argument_padding_zero_entry": True,
        "whole_financial_source_emitted": False, "fixture_credit": 0,
        "prototype_native_rows_cap": MAX_ROWS, "prototype_native_wire_cap": MAX_QUBITS,
    }
    checkpoint()
    return p, descriptor, H32_records(n), H32_records(n, inverse=True)
