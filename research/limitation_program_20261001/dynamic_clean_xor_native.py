"""Measured clean-XOR addition with an explicit channel-adjoint ABI.

The native width is 72. Independent measurement records and zero scratch are
part of every invocation, including the adjoint and coherent controlled copy.
No measurement array is reversed or inserted into the old Program.undo API.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction

import numpy as np

from research.limitation_program_20261001.temporary_and_fulladder import (
    and_compute,
    ccx_seven_t,
    encode,
)

NAMES = {1: "H", 2: "T", 3: "Tdg", 4: "Sdg", 5: "CX", 6: "CZ", 7: "MZ", 8: "X"}
MAX_DENSE_ELEMENTS = 1 << 20


@dataclass(frozen=True)
class AddLayout:
    width: int
    coherent_control: bool
    a: tuple[int, ...]
    b: tuple[int, ...]
    output: tuple[int, ...]
    control: int | None
    p: tuple[int, ...]
    g: tuple[int, ...]
    h: tuple[int, ...]
    carry: tuple[int, ...]
    qubits: int

    @property
    def logical_qubits(self):
        return 3 * self.width + int(self.coherent_control)

    @property
    def scratch(self):
        return self.p + self.g + self.h + self.carry

    @property
    def measurements(self):
        return 2 * self.width - 3


@dataclass(frozen=True)
class Macro:
    kind: str
    controls: tuple[int, int]
    target: int
    first: int
    stop: int
    result: int = -1


@dataclass(frozen=True)
class AddChannel:
    layout: AddLayout
    operations: np.ndarray
    macros: tuple[Macro, ...]
    measurement_start: int

    def adjoint(self, record_namespace):
        """A new forward invocation, with new record IDs and zero scratch."""
        if not isinstance(record_namespace, RecordNamespace) or (
            record_namespace.next_record < self.measurement_start + self.layout.measurements
        ):
            raise ValueError(
                "Caller-owned record namespace must follow every retained forward record"
            )
        return build_channel(
            self.layout.width,
            self.layout.coherent_control,
            record_namespace.reserve(self.layout.measurements),
        )

    def literal_reverse(self):
        raise TypeError(
            "Measurements have no literal gate-list inverse; use the fresh adjoint channel"
        )


class RecordNamespace:
    """A caller-owned monotone namespace shared by composed invocations.

    Independent experiments may each use a new namespace. A composed circuit
    must share one object; recreating namespaces does not reserve global IDs.
    """

    def __init__(self, next_record=0):
        if type(next_record) is not int or not 0 <= next_record <= 32767:
            raise ValueError("Bounded int16 measurement-record namespace required")
        self.next_record = next_record

    def reserve(self, count):
        if type(count) is not int or count <= 0 or self.next_record + count > 32767:
            raise ValueError("Fresh int16 measurement-record namespace exhausted")
        start = self.next_record
        self.next_record += count
        return start

    @classmethod
    def after(cls, program):
        return cls(program.measurement_start + program.layout.measurements)


def layout(width=72, coherent_control=False):
    if type(width) is not int or not 2 <= width <= 72:
        raise ValueError("Integer width in the fixed range2..72 required")
    if type(coherent_control) is not bool:
        raise ValueError("Coherent-control choice must be an actual bool")
    cursor = 0

    def allocate(length):
        nonlocal cursor
        wires = tuple(range(cursor, cursor + length))
        cursor += length
        return wires

    a, b, output = allocate(width), allocate(width), allocate(width)
    control = allocate(1)[0] if coherent_control else None
    p, g, h, carry = allocate(width), allocate(width - 1), allocate(width - 2), allocate(width - 1)
    return AddLayout(width, coherent_control, a, b, output, control, p, g, h, carry, cursor)


def mapped_macro(kind, a, b, target, result=-1):
    if kind == "cleanup":
        return [
            [1, target, -1, -1, -1],
            [7, target, -1, -1, result],
            [6, a, b, 1, result],
            [8, target, -1, 1, result],
        ]
    if kind not in ("AND", "CCX"):
        raise ValueError("Only fresh AND, cleanup or exact dirty-target CCX supported")
    template = encode((and_compute if kind == "AND" else ccx_seven_t)(0, 1, 5))
    mapping = {0: a, 1: b, 5: target}
    rows = template.tolist()
    for row in rows:
        row[1] = mapping[row[1]]
        if row[2] >= 0:
            row[2] = mapping[row[2]]
    return rows


def build_channel(width=72, coherent_control=False, measurement_start=0):
    wire = layout(width, coherent_control)
    if (
        type(measurement_start) is not int
        or not 0 <= measurement_start <= 32767 - wire.measurements
    ):
        raise ValueError("Fresh bounded int16 measurement-record interval required")
    rows, macros = [], []

    def cx(a, target):
        rows.append([5, a, target, -1, -1])

    def macro(kind, a, b, target, result=-1):
        first = len(rows)
        rows.extend(mapped_macro(kind, a, b, target, result))
        macros.append(Macro(kind, (a, b), target, first, len(rows), result))

    for i in range(width):
        cx(wire.a[i], wire.p[i])
        cx(wire.b[i], wire.p[i])
    for i in range(width - 1):
        macro("AND", wire.a[i], wire.b[i], wire.g[i])
        cx(wire.g[i], wire.carry[i])
        if i:
            macro("AND", wire.p[i], wire.carry[i - 1], wire.h[i - 1])
            cx(wire.h[i - 1], wire.carry[i])
    for i in range(width):
        for source in (wire.p[i],) + ((wire.carry[i - 1],) if i else ()):
            if coherent_control:
                macro("CCX", wire.control, source, wire.output[i])
            else:
                cx(source, wire.output[i])
    result = measurement_start
    for i in reversed(range(width - 1)):
        if i:
            cx(wire.h[i - 1], wire.carry[i])
        cx(wire.g[i], wire.carry[i])
        if i:
            macro("cleanup", wire.p[i], wire.carry[i - 1], wire.h[i - 1], result)
            result += 1
        macro("cleanup", wire.a[i], wire.b[i], wire.g[i], result)
        result += 1
    for i in reversed(range(width)):
        cx(wire.b[i], wire.p[i])
        cx(wire.a[i], wire.p[i])
    assert result == measurement_start + wire.measurements
    array = np.asarray(rows, dtype=np.int16)
    array.flags.writeable = False
    program = AddChannel(wire, array, tuple(macros), measurement_start)
    validate_primitives(program)
    return program


def validate_primitives(program):
    array, wire = program.operations, program.layout
    if wire != layout(wire.width, wire.coherent_control):
        raise ValueError("The complete canonical disjoint native wire layout is required")
    if type(program.measurement_start) is not int or not (
        0 <= program.measurement_start <= 32767 - wire.measurements
    ):
        raise ValueError("Fresh bounded int16 measurement-record interval required")
    if array.dtype != np.dtype(np.int16) or array.ndim != 2 or array.shape[1] != 5:
        raise ValueError("Signed int16 five-column dynamic primitive array required")
    observed = set()
    for code, a, b, condition, result in array.tolist():
        if code not in NAMES or not 0 <= a < wire.qubits:
            raise ValueError("Unsupported primitive or unallocated wire")
        if code in (5, 6):
            if not 0 <= b < wire.qubits or a == b:
                raise ValueError("Distinct allocated two-qubit wires required")
        elif b != -1:
            raise ValueError("One-qubit gate has no second wire")
        if code == 7:
            if (
                condition != -1
                or result in observed
                or not (
                    program.measurement_start
                    <= result
                    < program.measurement_start + wire.measurements
                )
            ):
                raise ValueError("One fresh measurement record per AND erasure required")
            observed.add(result)
        elif condition == -1:
            if result != -1:
                raise ValueError("Unconditional primitive has no result dependency")
        elif code not in (6, 8) or condition != 1 or result not in observed:
            raise ValueError("Only measured outcome-one CZ/reset feedback is supported")
    if len(observed) != wire.measurements:
        raise ValueError("The declared measurement count must be present")


def macro_events(program):
    """Bind every primitive to a proved macro or a single actual CX."""
    validate_primitives(program)
    indexed = {macro.first: macro for macro in program.macros}
    if len(indexed) != len(program.macros):
        raise ValueError("Overlapping macro start positions")
    events, cursor = [], 0
    while cursor < len(program.operations):
        if cursor in indexed:
            item = indexed[cursor]
            a, b = item.controls
            expected = np.asarray(
                mapped_macro(item.kind, a, b, item.target, item.result), dtype=np.int16
            )
            if item.stop != cursor + len(expected) or not np.array_equal(
                program.operations[cursor : item.stop], expected
            ):
                raise ValueError(
                    "Actual macro rows differ from the exact certified primitive template"
                )
            events.append((item.kind, a, b, item.target, item.result))
            cursor = item.stop
        else:
            row = program.operations[cursor].tolist()
            if row[0] != 5 or row[3:] != [-1, -1]:
                raise ValueError("Every nonmacro operation must be one unconditioned CX")
            events.append(("CX", row[1], row[2]))
            cursor += 1
    if sum(event[0] != "CX" for event in events) != len(program.macros):
        raise ValueError("Hidden or overlapping macro metadata")
    return tuple(events)


def verify_recipe(program):
    """Exact structural and lifetime binding of the fixed carry lemma.

    Primitive phase certification is a separate prerequisite. This verifier
    binds the actual arrays to that lemma; it does not call a floating simulator.
    """
    w = program.layout
    actual = iter(macro_events(program))

    def expect(event):
        if next(actual, None) != event:
            raise ValueError("Carry recipe, copy or cleanup lifetime was changed")

    for a, b, p in zip(w.a, w.b, w.p, strict=True):
        expect(("CX", a, p))
        expect(("CX", b, p))
    for bit in range(w.width - 1):
        expect(("AND", w.a[bit], w.b[bit], w.g[bit], -1))
        expect(("CX", w.g[bit], w.carry[bit]))
        if bit:
            expect(("AND", w.p[bit], w.carry[bit - 1], w.h[bit - 1], -1))
            expect(("CX", w.h[bit - 1], w.carry[bit]))
    for bit, destination in enumerate(w.output):
        for source in (w.p[bit],) + ((w.carry[bit - 1],) if bit else ()):
            expect(
                ("CCX", w.control, source, destination, -1)
                if w.coherent_control
                else ("CX", source, destination)
            )
    record = program.measurement_start
    for bit in reversed(range(w.width - 1)):
        if bit:
            expect(("CX", w.h[bit - 1], w.carry[bit]))
        expect(("CX", w.g[bit], w.carry[bit]))
        if bit:
            expect(("cleanup", w.p[bit], w.carry[bit - 1], w.h[bit - 1], record))
            record += 1
        expect(("cleanup", w.a[bit], w.b[bit], w.g[bit], record))
        record += 1
    for bit in reversed(range(w.width)):
        expect(("CX", w.b[bit], w.p[bit]))
        expect(("CX", w.a[bit], w.p[bit]))
    if next(actual, None) is not None:
        raise ValueError("Undeclared operations after cleanup")
    # Eight exact carry cases are the width-independent induction step.
    for a in (0, 1):
        for b in (0, 1):
            for carry in (0, 1):
                p, g, h = a ^ b, a & b, (a ^ b) & carry
                assert g * h == 0
                assert (g ^ h) == (a + b + carry) // 2
                assert (p ^ carry) == (a + b + carry) % 2
    n = w.measurements
    return {
        "actual_primitive_macro_and_lifetime_binding": True,
        "carry_induction_exact_boolean_cases": 8,
        "supported_width": w.width,
        "supports_signed_and_unsigned_modular_addition": True,
        "coherent_control_is_untouched_and_not_measured": w.coherent_control,
        "AND_fresh_targets": n,
        "cleanup_records": n,
        "all_histories_branch_probability_exact": [1, 1 << n],
        "all_histories_Kraus_identity": (
            "K_m=2^(-N/2)*U, contingent on exact AND/CCX primitive phase receipts"
        ),
        "arbitrary_reference_entanglement_by_linearity": True,
        "zero_scratch_required_and_restored": True,
        "adjoint_is_new_forward_invocation_not_measurement_reversal": True,
        "new_measurement_record_interval": [
            program.measurement_start,
            program.measurement_start + n,
        ],
        "continuous_financial_law_or_physical_runtime_proved": False,
    }


def basis_macro_replay(program, a, b, old_output, control=1):
    """Replay actual bound macro events with exact integer carry operations.

    This uses independently certified macro semantics, not a large statevector.
    It does not claim to execute the primitive Clifford/T measurement channel.
    """
    wire = program.layout
    limit = 1 << wire.width
    if any(type(value) is not int or not 0 <= value < limit for value in (a, b, old_output)):
        raise ValueError("Unsigned full-width native words required")
    if type(control) is not int or control not in (0, 1):
        raise ValueError("Binary coherent-control value required")
    bits = [0] * wire.qubits
    for register, value in ((wire.a, a), (wire.b, b), (wire.output, old_output)):
        for bit, index in enumerate(register):
            bits[index] = (value >> bit) & 1
    if wire.control is not None:
        bits[wire.control] = control
    for event in macro_events(program):
        if event[0] == "CX":
            bits[event[2]] ^= bits[event[1]]
        else:
            kind, left, right, target, result = event
            product = bits[left] & bits[right]
            if kind == "AND":
                assert bits[target] == 0, "AND target is not fresh"
                bits[target] = product
            elif kind == "cleanup":
                assert bits[target] == product, "AND controls were changed before erasure"
                bits[target] = 0
            else:
                bits[target] ^= product
    values = [
        sum(bits[index] << bit for bit, index in enumerate(register))
        for register in (wire.a, wire.b, wire.output)
    ]
    assert values[:2] == [a, b] and not any(bits[index] for index in wire.scratch)
    if wire.control is not None:
        assert bits[wire.control] == control
    return values[2]


def dense_branch(program, columns, outcomes):
    """Small-width primitive corroboration; never allocate a native statevector."""
    validate_primitives(program)
    if program.layout.qubits > 17:
        raise ValueError("Dense corroboration is restricted to at most17 qubits")
    n = program.layout.measurements
    if len(outcomes) != n or any(type(bit) is not int or bit not in (0, 1) for bit in outcomes):
        raise ValueError("One binary outcome per declared measurement required")
    size = 1 << program.layout.qubits
    shape = np.shape(columns)
    if len(shape) != 2 or shape[0] != size or shape[1] <= 0:
        raise ValueError("Full bounded columns required")
    if shape[0] * shape[1] > MAX_DENSE_ELEMENTS:
        raise ValueError("Fixed dense element and memory bound would be exceeded")
    value = np.asarray(columns, dtype=np.complex128)
    indices = np.arange(size)
    for code, a, b, condition, result in program.operations.tolist():
        outcome = outcomes[result - program.measurement_start] if result >= 0 else -1
        if condition == 1 and outcome != 1:
            continue
        selected = ((indices >> a) & 1) != 0
        if code == 7:
            value = value.copy()
            value[selected != bool(outcome)] = 0
        elif code in (5, 8):
            flip = np.where(selected, 1 << b, 0) if code == 5 else 1 << a
            value = value[indices ^ flip].copy()
        elif code == 1:
            zero, one = indices[~selected], indices[~selected] | (1 << a)
            following = value.copy()
            following[zero] = (value[zero] + value[one]) / np.sqrt(2)
            following[one] = (value[zero] - value[one]) / np.sqrt(2)
            value = following
        else:
            if code == 6:
                phase = np.where(selected & (((indices >> b) & 1) != 0), -1, 1)
            else:
                phase = np.where(
                    selected, {2: (1 + 1j) / np.sqrt(2), 3: (1 - 1j) / np.sqrt(2), 4: -1j}[code], 1
                )
            value = phase[:, None] * value
    return value


def paid_resources(program):
    validate_primitives(program)
    counts = Counter(NAMES[int(row[0])] for row in program.operations)
    tcount = counts["T"] + counts["Tdg"]
    w = program.layout
    assert counts["MZ"] == counts["CZ"] == counts["X"] == w.measurements
    expected = 8 * w.width - 12 + (7 * (2 * w.width - 1) if w.coherent_control else 0)
    assert tcount == expected
    return {
        "width": w.width,
        "coherent_control": w.coherent_control,
        "logical_input_output_and_control_qubits": w.logical_qubits,
        "allocated_qubits": w.qubits,
        "fresh_scratch": len(w.scratch),
        "actual_primitive_counts": dict(sorted(counts.items())),
        "T_count": tcount,
        "T_depth_fixed_serial": tcount,
        "fixed_serial_operation_slots": len(program.operations),
        "measurements": counts["MZ"],
        "feedback_CZ_slots": counts["CZ"],
        "conditional_reset_X_slots": counts["X"],
        "retained_record_bits": w.measurements,
        "record_probability_exact": [1, 1 << w.measurements],
        "record_entropy_bits": w.measurements,
        "feedback_routing_factory_seconds": None,
        "full_financial_source_resources": None,
        "native_literal_undo_supported": False,
        "best_possible_unitary_optimality_proved": False,
    }


def ideal_abstract_branch_scale(program):
    """Squared scalar is exact; phase identity needs the frozen primitive proof."""
    return Fraction(1, 1 << program.layout.measurements)


def native_unitary_control(width=72, coherent_control=False):
    """Actual original Cuccaro compute/copy/literal-undo comparator.

    Coherent control is paid only on the output copy, while reversible work is
    computed and erased unconditionally. This is one available comparator,
    without a claim that it is the best possible unitary adder.
    """
    layout(width, coherent_control)
    from research.journal_sprint.reversible_fixed_point import Program, add, copy

    p = Program(compact=True)
    a, b, output = (p.register(width) for _ in range(3))
    control = p.register(1)[0] if coherent_control else None
    work, helper = p.register(width), p.register(1)[0]
    first = len(p.gates)
    copy(p, a, work)
    add(p, b, work, helper)
    stop = len(p.gates)
    if coherent_control:
        for source, target in zip(work, output, strict=True):
            p.gate(control, source, target)
    else:
        copy(p, work, output)
    p.undo(first, stop)
    return p, (a, b), (output,), control
