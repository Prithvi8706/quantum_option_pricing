"""Independent exact A20 audit, author-stage draft; no work runs on import.

The admitted controller will bind every source byte before these kernels run.
No producer, builder, numerical package or historical scientific module is imported.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
import time

WIDTH = 72
FRACTION_BITS = 40
UNIT = 1 << FRACTION_BITS
WORD_MASK = (1 << WIDTH) - 1
REFERENCE_BITS = 53
REFERENCE_SIZE = 1 << REFERENCE_BITS
WIRE_LIMIT = 1024
RECIPE_GATE_LIMIT = 20000
VISIT_LIMIT = 64000000
ADMITTED_CHECK = None
VISITS = 0
BOUNDARIES = (
    0,
    1,
    2,
    (1 << 52) - 1,
    1 << 52,
    (1 << 52) + 1,
    REFERENCE_SIZE - 2,
    REFERENCE_SIZE - 1,
)
DIRTY_OUTPUTS = (0, WORD_MASK, sum(1 << j for j in range(0, WIDTH, 2)), 1 << 71)
SIGNED_BOUNDARIES = (
    (-(1 << 71), -(1 << 71)),
    (-(1 << 71), -1),
    (-(1 << 71), 0),
    (-(1 << 71), (1 << 71) - 1),
    (-1, -(1 << 71)),
    (-1, -1),
    (-1, 0),
    (0, -1),
    (0, 0),
    (0, 1),
    ((1 << 71) - 1, 0),
    ((1 << 71) - 1, (1 << 71) - 1),
)
SEVEN_T_SEQUENCE = (
    ("H", "target"),
    ("CX", "b", "target"),
    ("Tdg", "target"),
    ("CX", "a", "target"),
    ("T", "target"),
    ("CX", "b", "target"),
    ("Tdg", "target"),
    ("CX", "a", "target"),
    ("T", "b"),
    ("T", "target"),
    ("H", "target"),
    ("CX", "a", "b"),
    ("T", "a"),
    ("Tdg", "b"),
    ("CX", "a", "b"),
)


def insist(condition, message):
    if not condition:
        raise ValueError(message)


def checkpoint():
    insist(ADMITTED_CHECK is not None, "No kernel before complete admission")
    ADMITTED_CHECK()


def gate_visit():
    global VISITS
    VISITS += 1
    insist(VISITS <= VISIT_LIMIT, "Fixed exact gate/state visit cap")
    checkpoint()


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def object_sha(value):
    return hashlib.sha256(encoded(value).encode("utf-8")).hexdigest()


def signed_word(value, width=WIDTH):
    insist(type(value) is int and 0 <= value < 1 << width, "Canonical modular word")
    return value if value < 1 << (width - 1) else value - (1 << width)


def phase_binding(columns, text):
    """Bind absolute phase one for the exact paid fifteen-row CCX macro."""
    checkpoint()
    insist(
        columns
        == [
            dict(input=i, output=i ^ (((i & 1) & ((i >> 1) & 1)) << 2), exact_nonzero_phase=1)
            for i in range(8)
        ],
        "All eight exact CCX permutation/absolute-phase columns",
    )
    tree = ast.parse(text.decode("utf-8-sig"))
    found = [
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "ccx_seven_t"
    ]
    insist(len(found) == 1, "Unique pinned CCX definition")
    returns = [node for node in found[0].body if isinstance(node, ast.Return)]
    insist(len(returns) == 1 and isinstance(returns[0].value, ast.List), "Literal CCX return")
    rows = []
    for node in returns[0].value.elts:
        checkpoint()
        insist(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "gate"
            and not node.keywords
            and isinstance(node.args[0], ast.Constant)
            and all(isinstance(item, ast.Name) for item in node.args[1:]),
            "Literal exact-phase native chronology",
        )
        rows.append((node.args[0].value, *(item.id for item in node.args[1:])))
    insist(tuple(rows) == SEVEN_T_SEQUENCE, "Exact source-bound seven-T convention")
    return dict(proof_columns=8, exact_phase_one=True, macro=[list(row) for row in rows])


def independent_ccx_phase_columns(macro):
    """The eight complete columns in exact Q(sqrt2,i), with zero-other amplitudes."""
    ports = {"a": 0, "b": 1, "target": 2}
    zero = (Fraction(), Fraction(), Fraction(), Fraction())
    columns = []
    for basis in range(8):
        checkpoint()
        vector = {basis: (Fraction(1), Fraction(), Fraction(), Fraction())}
        for kind, *names in macro:
            checkpoint()
            wires = [ports[name] for name in names]
            next_vector = {}
            for state, amplitude in vector.items():
                gate_visit()
                a, b, c, d = amplitude
                if kind == "H":
                    half = (b, a / 2, d, c / 2)
                    low, high = state & ~(1 << wires[0]), state | (1 << wires[0])
                    sign = -1 if state & (1 << wires[0]) else 1
                    next_vector[low] = tuple(
                        x + y for x, y in zip(next_vector.get(low, zero), half)
                    )
                    next_vector[high] = tuple(
                        x + sign * y for x, y in zip(next_vector.get(high, zero), half)
                    )
                elif kind == "CX":
                    if state & (1 << wires[0]):
                        state ^= 1 << wires[1]
                    next_vector[state] = tuple(
                        x + y for x, y in zip(next_vector.get(state, zero), amplitude)
                    )
                else:
                    insist(kind in ("T", "Tdg"), "Only the exact source-bound CCX macro rows")
                    if state & (1 << wires[0]):
                        amplitude = (
                            (b - d, (a - c) / 2, b + d, (a + c) / 2)
                            if kind == "T"
                            else (b + d, (a + c) / 2, d - b, (c - a) / 2)
                        )
                    next_vector[state] = tuple(
                        x + y for x, y in zip(next_vector.get(state, zero), amplitude)
                    )
            vector = {state: value for state, value in next_vector.items() if value != zero}
            insist(len(vector) <= 8, "Fixed complete three-qubit macro dimension")
        output = basis ^ (((basis & 1) & ((basis >> 1) & 1)) << 2)
        insist(
            vector == {output: (Fraction(1), Fraction(), Fraction(), Fraction())},
            "Exact full CCX column: absolute phase+1 and every other amplitude zero",
        )
        columns.append(
            dict(
                input=basis,
                output=output,
                exact_nonzero_phase=1,
                all_other_output_amplitudes_exact_zero=True,
            )
        )
    return columns


class IndependentCircuit:
    """Fresh structural reconstruction from bit equations, without old builders."""

    def __init__(self):
        self.wires = 0
        self.rows = []

    def bank(self, size):
        checkpoint()
        insist(
            type(size) is int and 0 < size and self.wires + size <= WIRE_LIMIT,
            "Exact finite full-port bank allocation",
        )
        bank = tuple(range(self.wires, self.wires + size))
        self.wires += size
        return bank

    def append(self, kind, *ports):
        checkpoint()
        arity = {"X": 1, "CX": 2, "CCX": 3, "H": 1, "Z": 1, "CZ": 2}
        insist(
            kind in arity
            and len(ports) == arity[kind]
            and len(ports) == len(set(ports))
            and all(type(wire) is int and 0 <= wire < self.wires for wire in ports),
            "Every emitted native gate has allocated distinct ports",
        )
        insist(len(self.rows) < RECIPE_GATE_LIMIT, "Fixed per-recipe gate limit")
        self.rows.append([kind, *ports])

    def reverse(self, first, last):
        for row in reversed(self.rows[first:last]):
            self.append(*row)

    def publish(self, interfaces, ranges=None):
        ranges = {} if ranges is None else ranges
        ports = {key: list(bank) for key, bank in interfaces.items()}
        return {
            "schema": "A20-exact-native-gate-recipe-v2",
            "qubits": self.wires,
            "gates": self.rows,
            "interfaces": ports,
            "phase_ranges": ranges,
            "recipe_sha256": object_sha([self.wires, self.rows, ports, ranges]),
        }


def independent_add_rows(a, b, carry):
    """MAJ propagates majority; reversed UMA restores a/carry and adds into b."""
    insist(len(a) == len(b) and len(a) > 0, "Equal nonempty adder operands")
    rows = []
    triples = [(a[j], b[j], carry if j == 0 else a[j - 1]) for j in range(len(a))]
    for x, y, z in triples:
        rows.extend((["CX", x, y], ["CX", x, z], ["CCX", z, y, x]))
    for x, y, z in reversed(triples):
        rows.extend((["CCX", z, y, x], ["CX", x, z], ["CX", z, y]))
    return rows


def independent_comparison(circuit, a, b, flag):
    """Unsigned widened subtract, then sign bit XOR and exact uncomputation."""
    size = len(a)
    difference, extended = circuit.bank(size + 1), circuit.bank(size + 1)
    carry = circuit.bank(1)[0]
    start = len(circuit.rows)
    for source, target in zip(a, difference):
        circuit.append("CX", source, target)
    for source, target in zip(b, extended):
        circuit.append("CX", source, target)
    for row in reversed(independent_add_rows(extended, difference, carry)):
        circuit.append(*row)
    end = len(circuit.rows)
    circuit.append("CX", difference[-1], flag)
    circuit.reverse(start, end)


def independent_lookup(circuit, address, output, words):
    """All eight data rows, factored constant, explicit clean shared prefixes."""
    insist(
        len(address) == 3
        and len(words) == 8
        and all(type(word) is int and 0 <= word < REFERENCE_SIZE for word in words),
        "Restricted exact QROM data and address contract",
    )
    for bit, target in enumerate(output):
        if words[0] & (1 << bit):
            circuit.append("X", target)
    delta = [word ^ words[0] for word in words]
    if not any(delta):
        return
    stack = circuit.bank(2)

    def subtree(bit_index, prefix, offset):
        checkpoint()
        if not any(delta[offset : offset + (1 << (bit_index + 1))]):
            return
        if bit_index < 0:
            for j, wire in enumerate(output):
                if delta[offset] & (1 << j):
                    circuit.append("CX", prefix, wire)
            return
        flag, bit = stack[bit_index], address[bit_index]
        circuit.append("CCX", prefix, bit, flag)
        subtree(bit_index - 1, flag, offset + (1 << bit_index))
        circuit.append("CX", prefix, flag)
        subtree(bit_index - 1, flag, offset)
        circuit.append("CX", prefix, flag)
        circuit.append("CCX", prefix, bit, flag)

    subtree(1, address[2], 4)
    circuit.append("X", address[2])
    subtree(1, address[2], 0)
    circuit.append("X", address[2])


def independently_expected_recipes(words):
    """Recognize every source row, including controls, copies, H and inverses."""
    result = {}
    circuit = IndependentCircuit()
    a, b, out = circuit.bank(WIDTH), circuit.bank(WIDTH), circuit.bank(WIDTH)
    circuit.append("X", a[-1])
    circuit.append("X", b[-1])
    independent_comparison(circuit, a, b, out[0])
    circuit.append("X", a[-1])
    circuit.append("X", b[-1])
    result["native_signed_LT72"] = circuit.publish(dict(a=a, b=b, output=out))
    for controlled in (False, True):
        circuit = IndependentCircuit()
        address, out = circuit.bank(3), circuit.bank(WIDTH)
        independent_lookup(circuit, address, out, words)
        interfaces = dict(address=address, output=out)
        if controlled:
            original = circuit.rows
            circuit.rows = []
            control, scratch = circuit.bank(1)[0], circuit.bank(1)[0]
            interfaces["control"] = (control,)
            for kind, *ports in original:
                if kind == "X":
                    circuit.append("CX", control, *ports)
                elif kind == "CX":
                    circuit.append("CCX", control, *ports)
                else:
                    insist(kind == "CCX", "Only clean classical permutation lookup rows")
                    circuit.append("CCX", control, ports[0], scratch)
                    circuit.append("CCX", scratch, ports[1], ports[2])
                    circuit.append("CCX", control, ports[0], scratch)
        result[("controlled_" if controlled else "") + "QROM8_word72"] = circuit.publish(interfaces)
    result["controlled_one_stock53"] = independent_signal(None, WIDTH, REFERENCE_BITS)
    result["controlled_pair53"] = independent_signal(words, WIDTH, REFERENCE_BITS)
    return result, independent_signal(None, 3, 2)


def independent_signal(words, width, uniform_bits):
    circuit = IndependentCircuit()
    control, reference, stock = circuit.bank(1), circuit.bank(width), circuit.bank(width)
    predicate = circuit.bank(1)[0]
    ports = dict(control=control, reference=reference)
    if words is None:
        ports["stock"] = stock
    else:
        a0, a1, selector, selected = (
            circuit.bank(3),
            circuit.bank(3),
            circuit.bank(1),
            circuit.bank(3),
        )
        ports.update(address0=a0, address1=a1, selector=selector)
        circuit.append("H", selector[0])
        select_start = len(circuit.rows)
        for x, y, out in zip(a0, a1, selected):
            circuit.append("CX", x, out)
            circuit.append("CCX", selector[0], x, out)
            circuit.append("CCX", selector[0], y, out)
        select_end = len(circuit.rows)
        lookup_start = len(circuit.rows)
        independent_lookup(circuit, selected, stock, words)
        lookup_end = len(circuit.rows)
    transform_start = len(circuit.rows)
    for wire in reference[:uniform_bits]:
        circuit.append("H", wire)
    core_start = len(circuit.rows)
    compare_start = len(circuit.rows)
    circuit.append("X", reference[-1])
    circuit.append("X", stock[-1])
    independent_comparison(circuit, reference, stock, predicate)
    circuit.append("X", reference[-1])
    circuit.append("X", stock[-1])
    compare_end = len(circuit.rows)
    circuit.append("Z", control[0])
    circuit.append("CZ", control[0], predicate)
    circuit.reverse(compare_start, compare_end)
    core_end = len(circuit.rows)
    for wire in reference[:uniform_bits]:
        circuit.append("H", wire)
    transform_end = len(circuit.rows)
    ranges = dict(core=[core_start, core_end], reference_transform=[transform_start, transform_end])
    if words is not None:
        circuit.reverse(lookup_start, lookup_end)
        circuit.reverse(select_start, select_end)
        circuit.append("H", selector[0])
        ranges.update(selection=[select_start, select_end], lookup=[lookup_start, lookup_end])
    return circuit.publish(ports, ranges)


def independently_bind_stock(target, census):
    checkpoint()
    insist(
        (target["width"], target["fraction_bits"]) == (WIDTH, FRACTION_BITS),
        "Original signed72/f40 source domain",
    )
    producer = {}
    for node in target["nodes"]:
        checkpoint()
        insist(
            type(node["op"]) is str
            and type(node["args"]) is list
            and type(node["out"]) is list
            and type(node["params"]) is dict,
            "Typed actual source node",
        )
        for value in node["out"]:
            insist(type(value) is int and value not in producer, "Unique actual SSA result")
            producer[value] = node
    templates = []
    for asset in (0, 1):
        occurrences = [
            row
            for row in census["builder_label_proof"]["exponentials"]
            if row["asset"] == asset and row["date"] == 0
        ]
        insist(len(occurrences) == 1, "One actual original occurrence per selected asset/date")
        occurrence = occurrences[0]
        anchor = occurrence["clipped_log"]
        order, seen = [], set()

        def collect(value):
            checkpoint()
            if value == anchor or value in seen:
                return
            insist(value in producer, "Actual scalar exponential dependency")
            node = producer[value]
            insist(
                node["op"] in {"const", "add", "sub", "mul", "cmul", "bits", "shift"}
                and node["out"] == [value],
                "Closed original scalar stock operations",
            )
            for arg in node["args"]:
                collect(arg)
            seen.add(value)
            order.append(node)
            insist(len(order) <= 64, "Fixed complete scalar closure")

        collect(occurrence["stock"])
        numbers, normalized = {anchor: 0}, []
        for node in order:
            checkpoint()
            key = node["out"][0]
            numbers[key] = len(numbers)
            normalized.append(
                dict(
                    op=node["op"],
                    args=[numbers[arg] for arg in node["args"]],
                    params=node["params"],
                    out=numbers[key],
                )
            )
        clips = [row for row in census["builder_label_proof"]["clips"] if row["out"] == anchor]
        insist(len(clips) == 1, "Exact selected original clamp")
        bounds = []
        for label in ("low", "high"):
            node = producer[clips[0][label]]
            insist(node["op"] == "const", "Native clamp literal")
            bounds.append(signed_word(node["params"]["value"]))
        templates.append(
            dict(
                asset=asset,
                date=0,
                clipped_log=anchor,
                stock=occurrence["stock"],
                clamps=bounds,
                normalized_nodes=normalized,
                output=numbers[occurrence["stock"]],
                template_sha256=object_sha(normalized),
            )
        )
    insist(
        templates[0]["normalized_nodes"] == templates[1]["normalized_nodes"]
        and templates[0]["clamps"] == templates[1]["clamps"],
        "Actual literal/argument-order template equality before shared table use",
    )
    return templates


def independent_stock_word(template, raw):
    insist(template["clamps"][0] <= raw <= template["clamps"][1], "Actual supported stock input")
    values = {0: raw}
    for row in template["normalized_nodes"]:
        checkpoint()
        op, p = row["op"], row["params"]
        args = [values[index] for index in row["args"]]
        if op == "const":
            value = signed_word(p["value"])
        elif op == "add":
            value = args[0] + args[1]
        elif op == "sub":
            value = args[0] - args[1]
        elif op in ("mul", "cmul"):
            multiplier = args[1] if op == "mul" else p["c"]
            insist(
                type(multiplier) is int and -(1 << 71) <= multiplier < 1 << 71,
                "Canonical signed CMUL/native operand",
            )
            product = args[0] * multiplier
            insist(-(1 << 143) <= product < 1 << 143, "Full signed144 product")
            value = product // UNIT
        elif op == "bits":
            shift, bits = p["shift"], p["width"]
            insist(
                type(shift) is int and type(bits) is int and 1 <= bits <= WIDTH,
                "Exact native bits window",
            )
            operand = args[0] if p.get("signed", False) else args[0] & WORD_MASK
            value = (operand >> shift if shift >= 0 else operand << -shift) & ((1 << bits) - 1)
            value = signed_word(value)
        else:
            insist(op == "shift" and -WIDTH < args[1] < WIDTH, "Actual native stock shift")
            value = args[0] << args[1] if args[1] >= 0 else args[0] >> -args[1]
        insist(
            type(value) is int and -(1 << 71) <= value < 1 << 71,
            "Every eagerly retained scalar node fits signed72 without wrap",
        )
        values[row["out"]] = value
    word = values[template["output"]]
    insist(0 <= word < REFERENCE_SIZE, "Source-bound exact nonnegative F below fixed MQ")
    return word


def write_word(state, wires, word):
    insist(type(word) is int and 0 <= word < 1 << len(wires), "Canonical interface word")
    for bit, wire in enumerate(wires):
        if word & (1 << bit):
            state |= 1 << wire
    return state


def read_word(state, wires):
    return sum(((state >> wire) & 1) << bit for bit, wire in enumerate(wires))


def initial_state(recipe, inputs):
    state = 0
    for name, value in inputs.items():
        state = write_word(state, recipe["interfaces"][name], value)
    return state


def basis_action(recipe, inputs, rows=None, reverse=False):
    """Actual array traversal, with absolute Z/CZ phase and all scratch checked."""
    initial = initial_state(recipe, inputs)
    state, phase = initial, 1
    rows = recipe["gates"] if rows is None else rows
    if reverse:
        rows = reversed(rows)
    for kind, *ports in rows:
        gate_visit()
        if kind in ("X", "CX", "CCX"):
            if all((state >> wire) & 1 for wire in ports[:-1]):
                state ^= 1 << ports[-1]
        else:
            insist(kind in ("Z", "CZ"), "Basis checker never drops or executes an H")
            if all((state >> wire) & 1 for wire in ports):
                phase *= -1
    occupied = {wire for bank in recipe["interfaces"].values() for wire in bank}
    insist(
        not state & sum(1 << wire for wire in range(recipe["qubits"]) if wire not in occupied),
        "Every private wire restored after actual basis traversal",
    )
    return state, initial, phase


def amplitude_add(left, right):
    return left[0] + right[0], left[1] + right[1]


def sparse_operator(recipe, inputs):
    """Independent exact a+b*sqrt(2) representation using rational components."""
    initial = initial_state(recipe, inputs)
    vector = {initial: (Fraction(1), Fraction())}
    for kind, *ports in recipe["gates"]:
        checkpoint()
        next_vector = {}
        for state, amplitude in vector.items():
            gate_visit()
            if kind == "H":
                wire = ports[0]
                transformed = amplitude[1], amplitude[0] / 2
                zero, one = state & ~(1 << wire), state | (1 << wire)
                sign = -1 if state & (1 << wire) else 1
                next_vector[zero] = amplitude_add(
                    next_vector.get(zero, (Fraction(), Fraction())), transformed
                )
                next_vector[one] = amplitude_add(
                    next_vector.get(one, (Fraction(), Fraction())),
                    (sign * transformed[0], sign * transformed[1]),
                )
            else:
                if kind in ("X", "CX", "CCX"):
                    if all((state >> wire) & 1 for wire in ports[:-1]):
                        state ^= 1 << ports[-1]
                else:
                    insist(kind in ("Z", "CZ"), "Recognized exact phase op")
                    if all((state >> wire) & 1 for wire in ports):
                        amplitude = -amplitude[0], -amplitude[1]
                # Every admitted non-H row is an injective basis permutation
                # times an exact sign. Preserve its amplitude directly; only
                # H rows require additions from colliding output branches.
                insist(state not in next_vector, "Exact non-H basis action is injective")
                next_vector[state] = amplitude
        vector = {state: amp for state, amp in next_vector.items() if amp != (0, 0)}
        insist(len(vector) <= 8, "No full53/full72 statevector; fixed tiny sparse support")
    return vector, initial


def independently_count_resources(recipe):
    counts = Counter()
    ct, td = [0] * recipe["qubits"], [0] * recipe["qubits"]
    for kind, *ports in recipe["gates"]:
        checkpoint()
        counts[kind] += 1
        duration = 15 if kind == "CCX" else 3 if kind == "CZ" else 1
        end = max(ct[wire] for wire in ports) + duration
        tend = max(td[wire] for wire in ports) + (7 if kind == "CCX" else 0)
        for wire in ports:
            ct[wire], td[wire] = end, tend
    return dict(
        qubits=recipe["qubits"],
        source_gates=len(recipe["gates"]),
        native_counts={kind: counts[kind] for kind in ("X", "CX", "CCX", "H", "Z", "CZ")},
        exact_CCX_T_count=7 * counts["CCX"],
        expanded_Clifford_CX=counts["CX"] + 6 * counts["CCX"] + counts["CZ"],
        expanded_Clifford_H=counts["H"] + 2 * counts["CCX"] + 2 * counts["CZ"],
        expanded_Clifford_Z=counts["Z"],
        conservative_T_depth_upper=max(td, default=0),
        conservative_Clifford_T_depth_upper=max(ct, default=0),
        schedule_scope=(
            "conservative recipe-only dependency upper bounds; "
            "not measured full-source or physical schedule"
        ),
        all_lookup_copy_inverse_phase_and_preparation_gates_charged=True,
    )


def independent_universal_obligations():
    """Finite Boolean identities plus induction explain recognized whole-width recipes."""
    rows = []
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                checkpoint()
                x, y, z = a, b ^ a, c ^ a
                x ^= z & y
                insist(x == int(a + b + c >= 2), "MAJ computes exact carry")
                x ^= z & y
                z ^= x
                y ^= z
                insist(
                    (x, y, z) == (a, (a + b + c) % 2, c),
                    "UMA restores operand/carry and leaves exact sum bit",
                )
                rows.append(
                    dict(a=a, b=b, carry=c, majority=int(a + b + c >= 2), sum_bit=(a + b + c) % 2)
                )
    return {
        "recognized_actual_arrays_equal_independent_recipe": True,
        "local_MAJ_UMA_boolean_identities": rows,
        "whole_width_induction": (
            "MAJ ripples the carry through every operand bit; "
            "reversed UMA restores all a/carry bits "
            "and stores a+b modulo2^n in b. Its literal inverse subtracts. Copying unsigned n-bit "
            "a,b into n+1 zero words makes a-b lie in[-(2^n-1),2^n-1]; the top bit is exactly a<b. "
            "XOR-copy that bit then literal-invert the subtract/copies restores every scratch bit. "
            "Flipping both signed operand MSBs maps signed order to unsigned order and is undone."
        ),
        "QROM_induction": (
            "At each address prefix, CCX creates prefix*bit; CX(prefix,flag) switches to "
            "prefix*(1-bit); inverse CX/CCX restores zero. Leaf CX writes exactly the residual "
            "word, factored base X writes row0. The two top-MSB branches cover all8 addresses. "
            "Controlling X/CX directly and CCX with a fresh zero temporary implements each "
            "original permutation iff the external control is1, with exact temporary cleanup."
        ),
        "controlled_phase": "Z(c)CZ(c,p)=(-1)^(c*(1+p)); equals+1 for c0 or p1 and-1 for c1,p0",
        "reference_counting": (
            "For every integer0<=F<2^53, exactly F padded53-bit reference states satisfy r<F"
        ),
        "one_stock_zero_block": "2*F/2^53-1",
        "selector_zero_block": (
            "(F1+F2)/2^53-1; coherent selector amplitudes, not averaged probabilities"
        ),
        "uncontrolled_compute_uncompute_valid": (
            "Controls and selected input words do not change "
            "between exact comparator and its literal inverse"
        ),
        "absolute_phase_source_CCX_premise_required": True,
        "finite_diagnostics_are_not_substituted_for_universal_induction": True,
    }


def independent_component(source_result, target, census, support):
    """Every fixed semantic/basis/operator row is recomputed, never sampled."""
    templates = independently_bind_stock(target, census)
    insist(source_result["templates"] == templates, "Independent literal stock-template binding")
    lo, hi = templates[0]["clamps"]
    knots = [lo, lo + 1, 0, UNIT, 4 * UNIT, 5 * UNIT, hi - 1, hi]
    insist(
        len(set(knots)) == 8 and all(lo <= raw <= hi for raw in knots), "Fixed eight stock knots"
    )
    insist(
        support["passed"] is True and support["actual_stock_templates_checked"] == 48,
        "Exact source-bound B4 support premise",
    )
    cells = support["range_reduction_cells"]
    insist(
        cells
        and all(
            0 <= row["stock_interval"][0] <= row["stock_interval"][1] < REFERENCE_SIZE
            for row in cells
        ),
        "Full preserved native stock support below fixed M",
    )
    words = [independent_stock_word(templates[0], raw) for raw in knots]
    insist(
        source_result["knots_raw"] == knots and source_result["native_words"] == words,
        "All eight original stock values independently recomputed",
    )
    recipes, tiny = independently_expected_recipes(words)
    insist(
        source_result["recipes"] == recipes and source_result["tiny_recipe"] == tiny,
        "All actual gate/wire/port/range/recipe-SHA rows exactly recognized",
    )
    insist(
        source_result["tiny_resource"] == independently_count_resources(tiny),
        "Separately counted tiny test recipe, never a native53/full-source schedule",
    )
    semantic = []
    for i, a in enumerate(words):
        for j, b in enumerate(words):
            checkpoint()
            total = a + b
            insist(total < 1 << 71, "Native positive sum72 no wrap")
            semantic.append(
                dict(
                    i=i,
                    j=j,
                    F1=a,
                    F2=b,
                    native_basket_raw=total // 2,
                    alive=total < 280 * UNIT,
                    positive=total >= 200 * UNIT + 2,
                    one_stock_count_first=a,
                    one_stock_count_second=b,
                    pair_signal_exact=[total - REFERENCE_SIZE, REFERENCE_SIZE],
                )
            )
    minimum = min(row["stock_interval"][0] for row in cells)
    maximum = max(row["stock_interval"][1] for row in cells)
    boundary_rows = []
    for name, center, offsets in (
        ("barrier", 280 * UNIT, (-1, 0, 1)),
        ("strike", 200 * UNIT, (-1, 0, 1, 2, 3)),
    ):
        for offset in offsets:
            total = center + offset
            a, b = total // 2, total - total // 2
            insist(
                minimum <= a <= maximum and minimum <= b <= maximum,
                "Fixed native interface boundary inside saved envelope, no preimage claim",
            )
            insist(
                (total // 2 < 140 * UNIT) == (total < 280 * UNIT)
                and (total // 2 > 100 * UNIT) == (total >= 200 * UNIT + 2),
                "Exact native strict-barrier/positive-strike ties",
            )
            boundary_rows.append(
                dict(
                    label=name,
                    offset=offset,
                    sum=total,
                    F1=a,
                    F2=b,
                    alive=total // 2 < 140 * UNIT,
                    positive=total // 2 > 100 * UNIT,
                )
            )
    for a, b in ((90 * UNIT, 90 * UNIT), (50 * UNIT, 162 * UNIT)):
        insist(
            minimum <= a <= maximum and minimum <= b <= maximum,
            "Fixed equal-product diagnostic support",
        )
        boundary_rows.append(
            dict(
                label="equal_product",
                F1=a,
                F2=b,
                native_basket_raw=(a + b) // 2,
                alive=(a + b) // 2 < 140 * UNIT,
                positive=(a + b) // 2 > 100 * UNIT,
            )
        )
    insist(
        source_result["rows"] == semantic and source_result["boundary_cases"] == boundary_rows,
        "All64 and10 raw semantic rows, no ideal substitutions",
    )
    checks = []
    for family in ("QROM8_word72", "controlled_QROM8_word72"):
        recipe = recipes[family]
        for address in range(8):
            for dirty in DIRTY_OUTPUTS:
                for control in (0, 1) if "control" in recipe["interfaces"] else (1,):
                    inputs = dict(address=address, output=dirty)
                    if "control" in recipe["interfaces"]:
                        inputs["control"] = control
                    state, initial, phase = basis_action(recipe, inputs)
                    output = read_word(state, recipe["interfaces"]["output"])
                    insist(
                        output == dirty ^ (words[address] if control else 0)
                        and read_word(state, recipe["interfaces"]["address"]) == address
                        and phase == 1,
                        "All dirty QROM controlled/noncontrolled outputs/phase",
                    )
                    restored, _, inverse_phase = basis_action(
                        recipe, dict(inputs, output=output), reverse=True
                    )
                    insist(
                        restored == initial and inverse_phase == 1, "Actual literal QROM inverse"
                    )
                    checks.append(
                        dict(family=family, address=address, dirty=dirty, control=control)
                    )
    recipe = recipes["native_signed_LT72"]
    for a, b in tuple((a, b) for a in BOUNDARIES for b in BOUNDARIES) + SIGNED_BOUNDARIES:
        for dirty in DIRTY_OUTPUTS:
            inputs = dict(a=a & WORD_MASK, b=b & WORD_MASK, output=dirty)
            state, initial, phase = basis_action(recipe, inputs)
            output = read_word(state, recipe["interfaces"]["output"])
            insist(
                output == dirty ^ int(a < b)
                and read_word(state, recipe["interfaces"]["a"]) == (a & WORD_MASK)
                and read_word(state, recipe["interfaces"]["b"]) == (b & WORD_MASK)
                and phase == 1,
                "Full signed72 comparator absolute phase/dirty-output ABI",
            )
            restored, _, inverse_phase = basis_action(
                recipe, dict(inputs, output=output), reverse=True
            )
            insist(restored == initial and inverse_phase == 1, "Literal comparator inverse")
            checks.append(dict(family="native_signed_LT72", a=a, b=b, dirty=dirty))
    recipe = recipes["controlled_one_stock53"]
    first, last = recipe["phase_ranges"]["core"]
    for stock in BOUNDARIES:
        for reference in BOUNDARIES:
            for control in (0, 1):
                state, initial, phase = basis_action(
                    recipe,
                    dict(control=control, reference=reference, stock=stock),
                    rows=recipe["gates"][first:last],
                )
                insist(
                    state == initial and phase == (1 if control == 0 or reference < stock else -1),
                    "Actual53-reference native controlled phase, ties and all scratch",
                )
                checks.append(dict(family="native53_phase", F=stock, r=reference, control=control))
    for stock in range(4):
        for reference in range(4):
            for control in (0, 1):
                vector, initial = sparse_operator(
                    tiny, dict(control=control, reference=reference, stock=stock)
                )
                expected_states = set()
                reference_mask = sum(1 << wire for wire in tiny["interfaces"]["reference"])
                for output in range(4):
                    expected = (
                        Fraction(int(output == reference))
                        if control == 0
                        else sum(
                            (
                                Fraction(1 if r < stock else -1, 4)
                                * (-1) ** (((reference ^ output) & r).bit_count())
                                for r in range(4)
                            ),
                            Fraction(),
                        )
                    )
                    state = (initial & ~reference_mask) | write_word(
                        0, tiny["interfaces"]["reference"], output
                    )
                    insist(
                        vector.get(state, (Fraction(), Fraction())) == (expected, 0),
                        "Independent complete tiny Walsh/counting operator "
                        "with absolute control phase",
                    )
                    if expected:
                        expected_states.add(state)
                insist(
                    set(vector) == expected_states, "All tiny inputs and private wires preserved"
                )
                checks.append(
                    dict(family="tiny_complete_operator", F=stock, r=reference, control=control)
                )
    recipe = recipes["controlled_pair53"]
    reference_wires = set(recipe["interfaces"]["reference"])
    removed = [
        j for j, row in enumerate(recipe["gates"]) if row[0] == "H" and row[1] in reference_wires
    ]
    insist(len(removed) == 106, "Both actual53-H layers retained and charged")
    removed_set = set(removed)
    test_view = dict(
        recipe, gates=[row for j, row in enumerate(recipe["gates"]) if j not in removed_set]
    )
    for i, a in enumerate(words):
        for j, b in enumerate(words):
            for reference in BOUNDARIES:
                for control in (0, 1):
                    for selector in (0, 1):
                        vector, initial = sparse_operator(
                            test_view,
                            dict(
                                address0=i,
                                address1=j,
                                reference=reference,
                                control=control,
                                selector=selector,
                            ),
                        )
                        phases = [1 if control == 0 or reference < word else -1 for word in (a, b)]
                        expected_states = set()
                        for output in (0, 1):
                            state = initial ^ (
                                (selector ^ output) << recipe["interfaces"]["selector"][0]
                            )
                            expected = Fraction(
                                phases[0] + phases[1]
                                if output == selector
                                else phases[0] - phases[1],
                                2,
                            )
                            insist(
                                vector.get(state, (Fraction(), Fraction())) == (expected, 0),
                                "Actual pair selected lookup/phase/inverse/H all-wire tiny view",
                            )
                            if expected:
                                expected_states.add(state)
                        insist(
                            set(vector) == expected_states,
                            "All native pair input and scratch restoration",
                        )
                        checks.append(
                            dict(
                                family="native53_pair_phase",
                                i=i,
                                j=j,
                                r=reference,
                                control=control,
                                selector=selector,
                            )
                        )
    insist(
        len(checks) == 2608 and checks == source_result["checks"],
        "Exact independent2608 fixed component checks",
    )
    resources = {name: independently_count_resources(recipe) for name, recipe in recipes.items()}
    insist(
        resources == source_result["resources"],
        "Every actual control/lookup/copy/inverse/H/phase cost independently counted",
    )
    view = dict(
        source_recipe_sha256=recipe["recipe_sha256"],
        removed_reference_H_indices=removed,
        removed_gates_counted_in_actual_cost=True,
        not_a_full53_statevector=True,
    )
    insist(
        source_result["native_pair_phase_test_view"] == view,
        "Only the declared106-H test-view deletion",
    )
    count_proof = dict(
        uniform_reference_bits=53,
        uniform_states=REFERENCE_SIZE,
        positive_phase_states_for_F="exactly F",
        one_stock_signal="(2F-MQ)/MQ",
        pair_signal="(F1+F2-MQ)/MQ",
        guaranteed_integer_half_threshold_gap=[1, 2 * REFERENCE_SIZE],
        no_53bit_statevector=True,
    )
    insist(
        source_result["exact_counting_proof"] == count_proof, "Exact whole-reference counting proof"
    )
    insist(
        source_result["offline_native_scalar_evaluations"] == 8
        and source_result["offline_pair_truth_records"] == 64,
        "All paid offline source words/pairs retained",
    )
    return dict(
        templates=templates,
        native_words=words,
        knots_raw=knots,
        independent_semantic_rows=semantic,
        independent_boundary_cases=boundary_rows,
        independent_component_checks=checks,
        independent_resources=resources,
        universal_obligations=independent_universal_obligations(),
        counting_proof=count_proof,
        native_pair_phase_test_view=view,
        exact_gate_state_visits=VISITS,
        complete_source_cost_or_adoption=False,
        no_new_fixture_credit=True,
    )


SELECTED_PREMISES = {
    "research/journal_sprint/reversible_fixed_point.py": (
        "52584dee87c84541b9f9e2f070114d7276de3d49d306d33c471214795b729b8b"
    ),
    "research/controlled_source_completion/exact_lookup.py": (
        "a63e27f9995adcacad707808fd6565fe9bf62920b73203c3021dd67861822b6c"
    ),
    "results/limitation_program_20261001/E22_census_run002/B4x12_predicate_census.json": (
        "35b9cf84b23b10d871dbb64e5af1bdfe9c9ce58db811ac089f7729c6eebfabb3"
    ),
    "results/limitation_program_20261001/A17_quantile_divider_run001/exact_CCX_phase_proof.json": (
        "714698f92a1d94f61ec26f746e77f9a7aa936a41308a9b82e6e93495fa92a55c"
    ),
    "research/limitation_program_20261001/temporary_and_fulladder.py": (
        "34bb7f93d07b51de54c44d2fd8c124678d280db01066df848bb7eac43aa2dfeb"
    ),
}


def read_source_groups(receipt, directory):
    checkpoint()
    binding = receipt.read(directory / "source_binding.json")
    truth = receipt.read(directory / "native_truth.json")
    gates = receipt.read(directory / "gate_recipes.json")
    checks = receipt.read(directory / "component_checks.json")
    counting = receipt.read(directory / "exact_counting_proof.json")
    resources = receipt.read(directory / "resource_ledger.json")
    insist(
        binding["schema"] == "A20-restricted-native-stock-source-binding-v2"
        and binding["selected_expected_sha256"] == receipt.ready["selected_prerequisite_sha256"]
        and binding["offline_truth_construction_charged"] is True
        and binding["general_q32_reachability_or_law_claim"] is False,
        "Exact producer source-binding scope and unchanged expected pins",
    )
    insist(
        truth["boundary_words_are_interface_only_not_proven_reachable"] is True,
        "No restricted interface-to-path reachability transfer",
    )
    insist(
        gates["schema"] == "A20-exact-paid-gate-recipes-v2"
        and gates["one_component_construction"] is True
        and gates["original_word_width"] == 72
        and gates["original_fractional_bits"] == 40
        and gates["native_reference_bits"] == 53
        and gates["reference_upper19_zero_promised"] is True
        and gates["reference_and_selector_block_output_garbage_allowed"] is True
        and gates["stock_address_and_internal_scratch_restored"] is True
        and gates["full_pricing_source_emitted"] is False,
        "Native signal ABI and full-source nonclaim",
    )
    families = {
        "QROM8_word72": 32,
        "controlled_QROM8_word72": 64,
        "native_signed_LT72": 304,
        "native53_phase": 128,
        "tiny_complete_operator": 32,
        "native53_pair_phase": 2048,
    }
    insist(
        checks["total_internal_checks"] == 2608
        and checks["new_test_credit"] == 0
        and checks["internal_checks_are_not_distinct_pytest_or_financial_fixtures"] is True
        and checks["native53_pair_tests_are_H_removed_reference_test_view"] is True
        and checks["family_counts"] == families
        and dict(Counter(row["family"] for row in checks["checks"])) == families
        and type(checks["exact_gate_state_visits"]) is int
        and 0 < checks["exact_gate_state_visits"] <= VISIT_LIMIT,
        "All fixed source checks retained with honest zero fixture credit",
    )
    insist(
        counting["reference_upper19_zero_promised"] is True
        and counting["strict_F_domain"] == [0, REFERENCE_SIZE - 1]
        and counting["control_zero_full_identity"] is True
        and counting["threshold_transform_or_full_pricing_oracle_supplied"] is False,
        "Counting premise, control phase and threshold scope",
    )
    insist(
        resources["offline_native_evaluations"] == 8
        and resources["offline_pair_truth_records"] == 64
        and resources["constructed_recipe_count_including_tiny"] == 6
        and resources["native_CCX_absolute_phase_and_seven_T_paid"] is True
        and resources["QROM_address_selection_copy_cleanup_and_H_Z_CZ_paid"] is True
        and resources["depths_are_conservative_recipe_upper_bounds_not_full_source_schedules"]
        is True
        and resources["classical_offline_build_storage_and_load_amortization_not_assumed_free"]
        is True,
        "Exact charged component cost scope",
    )
    for name in (
        "component_work_CPU_seconds_including_emission_and_checks",
        "component_work_wall_seconds_including_emission_and_checks",
    ):
        observation = resources[name]
        insist(
            type(observation) in (int, float)
            and 0 <= observation
            and observation < (180 if "CPU" in name else 600),
            "Finite recorded producer component observation, no measured-price timing",
        )
    expected_scope = {
        "status": "NOT_FULL_SOURCE_COSTED",
        "general_full72_or_q32_oracle_supplied": False,
        "threshold_transform_supplied": False,
        "new_financial_bias_allocation": None,
        "arithmetic_removal_or_adoption": False,
    }
    insist(
        resources["whole_source_comparison"] == expected_scope,
        "No arithmetic removal, financial or full-source cost approval",
    )
    count_keys = (
        "uniform_reference_bits",
        "uniform_states",
        "positive_phase_states_for_F",
        "one_stock_signal",
        "pair_signal",
        "guaranteed_integer_half_threshold_gap",
        "no_53bit_statevector",
    )
    return {
        "templates": binding["templates"],
        "knots_raw": binding["knots_raw"],
        "native_words": binding["native_words"],
        "offline_native_scalar_evaluations": binding["offline_native_scalar_evaluations"],
        "rows": truth["rows"],
        "boundary_cases": truth["boundary_cases"],
        "offline_pair_truth_records": truth["offline_pair_truth_records"],
        "recipes": gates["recipes"],
        "tiny_recipe": gates["tiny_recipe"],
        "checks": checks["checks"],
        "native_pair_phase_test_view": checks["native_pair_phase_test_view"],
        "resources": resources["resources"],
        "tiny_resource": resources["tiny_resource"],
        "exact_counting_proof": {name: counting[name] for name in count_keys},
    }


def run_independent_audit(receipt, protocol, program, research):
    global ADMITTED_CHECK, VISITS
    receipt.verify_loaded(protocol)
    receipt.verify(True)
    receipt.check(admission=True)
    ADMITTED_CHECK, VISITS = receipt.check, 0
    source = program / "A20_continuation_20261004_producer_run002"
    for name in ("summary.json", "completion_outcome.json"):
        terminal = receipt.read(source / name)
        insist(
            terminal["schema"] == "A20-comparator-phase-component-summary-v2"
            and terminal["role"] == "producer"
            and terminal["component_semantics_verified"] is True
            and terminal["independent_audit_still_required"] is True
            and terminal["restricted_pair_truth_rows"] == 64
            and terminal["interface_boundary_cases"] == 10
            and terminal["general_full72_or_q32_oracle"] is False
            and terminal["threshold_QSP_transform"] is False
            and terminal["complete_financial_bias_allocation"] is None
            and terminal["new_gate_replay_credit"] == 0
            and terminal["new_financial_replay_credit"] == 0
            and terminal["quantum_advantage"] is False,
            "Source component success is a bounded access result, no source-finance approval",
        )
    groups = read_source_groups(receipt, source)
    phase = phase_binding(
        receipt.read(program / "A17_quantile_divider_run001/exact_CCX_phase_proof.json"),
        receipt.read_bytes(research / "temporary_and_fulladder.py"),
    )
    insist(
        receipt.read(source / "phase_premise.json") == phase,
        "Independent literal exact-phase macro and sealed eight-column premise",
    )
    full_phase_columns = independent_ccx_phase_columns(phase["macro"])
    work_cpu, work_wall = time.process_time(), time.monotonic()
    result = independent_component(
        groups,
        receipt.read(program / "A10_coefficient_run001/B4x12/min-depth/target.json"),
        receipt.read(program / "E22_census_run002/B4x12_predicate_census.json"),
        receipt.read(program / "E03_support_audit_run002/B4x12_audit.json"),
    )
    elapsed_cpu, elapsed_wall = time.process_time() - work_cpu, time.monotonic() - work_wall
    receipt.check(admission=True)
    receipt.write(
        "independent_source_binding.json",
        {
            "templates": result["templates"],
            "knots_raw": result["knots_raw"],
            "native_words": result["native_words"],
            "offline_native_scalar_evaluations": 8,
            "all_actual_original_dependency_order_and_literals_bound": True,
            "general_q32_reachability_or_law_claim": False,
        },
    )
    receipt.write(
        "independent_native_truth.json",
        {
            "rows": result["independent_semantic_rows"],
            "boundary_cases": result["independent_boundary_cases"],
            "offline_pair_truth_records": 64,
        },
    )
    receipt.write(
        "independent_component_checks.json",
        {
            "checks": result["independent_component_checks"],
            "internal_component_checks": 2608,
            "exact_gate_state_visits": result["exact_gate_state_visits"],
            "native_pair_phase_test_view": result["native_pair_phase_test_view"],
            "full_native_arrays_recognized_and_reexecuted": True,
            "all_private_wires_and_inputs_preserved": True,
            "absolute_controlled_phase_checked": True,
            "finite_checks_not_whole_q32_or_financial_fixtures": True,
            "new_test_credit": 0,
        },
    )
    receipt.write(
        "independent_counting_and_structural_proof.json",
        {
            "exact_counting_proof": result["counting_proof"],
            "universal_obligations": result["universal_obligations"],
            "phase_premise": phase,
            "independent_exact_CCX_full_operator_columns": full_phase_columns,
            "integer_half_gap_applies_to_affine_pair_signal_only": True,
            "no_threshold_polynomial_or_QSP_transform_approval": True,
        },
    )
    receipt.write(
        "independent_resource_ledger.json",
        {
            "resources": result["independent_resources"],
            "tiny_resource": independently_count_resources(groups["tiny_recipe"]),
            "whole_source_comparison": {
                "status": "NOT_FULL_SOURCE_COSTED",
                "general_full72_or_q32_oracle_supplied": False,
                "threshold_transform_supplied": False,
                "new_financial_bias_allocation": None,
                "arithmetic_removal_or_adoption": False,
            },
            "independent_work_CPU_seconds": elapsed_cpu,
            "independent_work_wall_seconds": elapsed_wall,
            "depths_are_conservative_recipe_upper_bounds_not_measured_full_source": True,
            "every_control_lookup_copy_inverse_and_preparation_gate_counted": True,
        },
    )
    receipt.verify_loaded(protocol)
    receipt.verify(True)
    summary = {
        "schema": "A20-comparator-phase-independent-audit-summary-v2",
        "role": "audit",
        "completed": True,
        "passed": True,
        "budget_censored": False,
        "component_semantics_verified": True,
        "independent_audit": True,
        "source_manifest_sha256": receipt.ready["producer_manifest_sha256"],
        "source_author_pair": {
            key: pin
            for key, pin in receipt.ready["author_sha256"].items()
            if Path(key).name
            in (
                "experiment_arithmetic_free_basket_signal_continuation_v4.py",
                "arithmetic_free_basket_signal_v2.py",
            )
        },
        "independent_source_template_reconstruction": True,
        "independent_recipe_reconstruction_and_actual_array_traversal": True,
        "universal_structural_and_absolute_phase_premises_verified": True,
        "internal_component_checks": 2608,
        "offline_native_scalar_evaluations": 8,
        "restricted_pair_truth_rows": 64,
        "interface_boundary_cases": 10,
        "general_full72_or_q32_oracle": False,
        "threshold_QSP_transform": False,
        "complete_financial_bias_allocation": None,
        "full_G2": False,
        "new_test_credit": 0,
        "new_gate_replay_credit": 0,
        "new_financial_replay_credit": 0,
        "adoption": False,
        "quantum_advantage": False,
        "original_scientific_precision_and_strict_ties_retained": True,
        "physical_runtime": None,
        "process_CPU_seconds_at_preseal_checkpoint": time.process_time(),
        "creation_clock_wall_seconds_at_preseal_checkpoint": time.monotonic() - receipt.started,
    }
    receipt.seal(summary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run"))
    parser.add_argument("--ready", required=True)
    parser.add_argument("--ready-sha256", required=True)
    parser.add_argument("--protocol-sha256")
    arguments = parser.parse_args()
    # This explicitly shared module provides only operational receipt functions.
    from research.limitation_program_20261001.a20_signal_receipt_continuation_v4 import (
        PROGRAM,
        RESEARCH,
        Receipt,
    )

    receipt = None
    try:
        receipt = Receipt("audit", arguments.ready, arguments.ready_sha256, arguments.mode)
        insist(
            all(
                receipt.ready["selected_prerequisite_sha256"].get(key) == pin
                for key, pin in SELECTED_PREMISES.items()
            ),
            "Unchanged original helper/census/exact-phase expected source pins",
        )
        receipt.admit_packet(
            PROGRAM / "A20_continuation_20261004_producer_run002", receipt.ready["producer_manifest_sha256"]
        )
        if arguments.mode == "prepare":
            insist(arguments.protocol_sha256 is None, "No protocol pin before fresh prepare")
            print("PREPARED_PROTOCOL_SHA256=" + receipt.prepare())
        else:
            insist(
                arguments.protocol_sha256 is not None,
                "Actual ROOT-issued prepared-protocol pin required",
            )
            protocol = receipt.admit_run(arguments.protocol_sha256)
            run_independent_audit(receipt, protocol, PROGRAM, RESEARCH)
            print("A20 independent restricted component audit PASS; zero program fixture credit")
        return 0
    except BaseException as error:
        if receipt is not None:
            receipt.fail(error)
        print(type(error).__name__ + ": " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
