"""Author-only exact A20 recipes and fixed checks; nothing runs on import.

All historical functions are AST-extracted only after producer admission.
No historical module, NumPy, scientific backend or native cache is imported.
This restricted interface is not a q32 path-law or full financial replacement.
"""

from __future__ import annotations

import ast
from collections import Counter
from fractions import Fraction
import hashlib
import json

W, F, Q, REFERENCE_BITS = 72, 40, 1 << 40, 53
MASK, MQ = (1 << W) - 1, 1 << REFERENCE_BITS
MAX_GATES, MAX_QUBITS, MAX_GATE_VISITS = 20000, 1024, 64000000
CHECK = None
GATE_VISITS = 0
BOUNDARY_WORDS = (0, 1, 2, (1 << 52) - 1, 1 << 52, (1 << 52) + 1, MQ - 2, MQ - 1)
DIRTY_WORDS = (0, MASK, sum(1 << bit for bit in range(0, W, 2)), 1 << 71)
SIGNED_PAIRS = (
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
NATIVE_NAMES = ("_disjoint", "copy", "add", "subtract", "less_than")
CCX_MACRO = (
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


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check():
    require(CHECK is not None, "No builder/check execution before admitted clock")
    CHECK()


def visit_gate():
    global GATE_VISITS
    GATE_VISITS += 1
    require(GATE_VISITS <= MAX_GATE_VISITS, "Fixed64million exact gate/state visits")
    check()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def fingerprint(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def signed(word, width=W):
    word &= (1 << width) - 1
    return word - (1 << width) if word >> (width - 1) else word


def extracted_functions(source, names):
    check()
    tree = ast.parse(source.decode("utf-8-sig"))
    definitions = [
        node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in names
    ]
    require(
        len(definitions) == len(names) and {node.name for node in definitions} == set(names),
        "Exact function selection",
    )
    scope = {"__builtins__": __builtins__}
    exec(
        compile(
            ast.Module(body=definitions, type_ignores=[]), "<pinned-A20-native-functions>", "exec"
        ),
        scope,
    )
    check()
    return {name: scope[name] for name in names}


def native_helpers(source_bytes, lookup_bytes):
    functions = extracted_functions(source_bytes, NATIVE_NAMES)
    functions.update(extracted_functions(lookup_bytes, ("lookup_shared",)))
    return functions


def phase_premise(proof, macro_bytes):
    check()
    expected = [
        dict(input=k, output=k ^ (((k & 1) & ((k >> 1) & 1)) << 2), exact_nonzero_phase=1)
        for k in range(8)
    ]
    require(proof == expected, "Sealed eight exact phase-one CCX columns")
    definitions = [
        node
        for node in ast.parse(macro_bytes.decode("utf-8-sig")).body
        if isinstance(node, ast.FunctionDef) and node.name == "ccx_seven_t"
    ]
    require(len(definitions) == 1, "One sealed exact CCX macro")
    returns = [node for node in definitions[0].body if isinstance(node, ast.Return)]
    require(len(returns) == 1 and isinstance(returns[0].value, ast.List), "Literal seven-T macro")
    rows = []
    for node in returns[0].value.elts:
        require(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "gate"
            and not node.keywords,
            "Literal gate call",
        )
        require(
            isinstance(node.args[0], ast.Constant)
            and all(isinstance(arg, ast.Name) for arg in node.args[1:]),
            "Literal gate arguments",
        )
        rows.append((node.args[0].value, *(arg.id for arg in node.args[1:])))
    require(tuple(rows) == CCX_MACRO, "Exact absolute phase and paid chronology")
    return {"proof_columns": 8, "exact_phase_one": True, "macro": [list(row) for row in rows]}


class Recipe:
    def __init__(self):
        self.qubits, self.gates = 0, []

    def register(self, width):
        check()
        require(
            type(width) is int and width > 0 and self.qubits + width <= MAX_QUBITS,
            "Fixed recipe wire cap",
        )
        result = tuple(range(self.qubits, self.qubits + width))
        self.qubits += width
        return result

    def emit(self, kind, *wires):
        check()
        sizes = {"X": 1, "CX": 2, "CCX": 3, "H": 1, "Z": 1, "CZ": 2}
        require(
            kind in sizes and len(wires) == sizes[kind] and len(set(wires)) == len(wires),
            "Native gate signature",
        )
        require(
            all(type(wire) is int and 0 <= wire < self.qubits for wire in wires),
            "Allocated distinct native wires",
        )
        require(len(self.gates) < MAX_GATES, "Fixed per-recipe gate cap")
        self.gates.append((kind, *wires))

    def gate(self, *wires):
        self.emit({1: "X", 2: "CX", 3: "CCX"}[len(wires)], *wires)

    def undo(self, start, stop=None):
        stop = len(self.gates) if stop is None else stop
        for row in reversed(self.gates[start:stop]):
            self.emit(row[0], *row[1:])

    def record(self, interfaces, phases=None):
        return {
            "schema": "A20-exact-native-gate-recipe-v2",
            "qubits": self.qubits,
            "gates": [list(row) for row in self.gates],
            "interfaces": {key: list(value) for key, value in interfaces.items()},
            "phase_ranges": phases or {},
            "recipe_sha256": fingerprint([self.qubits, self.gates, interfaces, phases or {}]),
        }


def less_than_leaf(helpers, width=W):
    p = Recipe()
    a, b, output = p.register(width), p.register(width), p.register(width)
    for register in (a, b):
        p.gate(register[-1])
    helpers["less_than"](
        p, a, b, output[0], p.register(width + 1), p.register(width + 1), p.register(1)[0]
    )
    for register in (a, b):
        p.gate(register[-1])
    return p.record({"a": a, "b": b, "output": output})


def qrom_leaf(helpers, words, controlled=False):
    require(
        len(words) == 8 and all(type(word) is int and 0 <= word < MQ for word in words),
        "Eight nonnegative native stock words",
    )
    p = Recipe()
    address, output = p.register(3), p.register(W)
    helpers["lookup_shared"](p, address, [output], [[word] for word in words], 3)
    if not controlled:
        return p.record({"address": address, "output": output})
    previous = p.gates
    p.gates = []
    control, temporary = p.register(1), p.register(1)
    for kind, *wires in previous:
        if kind == "X":
            p.gate(control[0], wires[0])
        elif kind == "CX":
            p.gate(control[0], *wires)
        else:
            require(kind == "CCX", "Only exact permutation lookup gates")
            p.gate(control[0], wires[0], temporary[0])
            p.gate(temporary[0], wires[1], wires[2])
            p.gate(control[0], wires[0], temporary[0])
    return p.record({"address": address, "output": output, "control": control})


def signal_recipe(helpers, words=None, width=W, reference_bits=REFERENCE_BITS, pair=True):
    """Actual H/lookup/LT/phase/inverse recipe, including outer control.

    A pair selects one word coherently, with a clean address and exact inverse.
    No arithmetic gate is declared free because it is used in a block encoding.
    """
    p = Recipe()
    control, reference, stock = p.register(1), p.register(width), p.register(width)
    predicate = p.register(1)
    interfaces = {"control": control, "reference": reference}
    if pair:
        require(
            width == W and words is not None and len(words) == 8,
            "Actual paired native QROM interface",
        )
        address0, address1, selector, selected = (
            p.register(3),
            p.register(3),
            p.register(1),
            p.register(3),
        )
        interfaces.update(address0=address0, address1=address1, selector=selector)
        p.emit("H", selector[0])
        selection_start = len(p.gates)
        for a, b, out in zip(address0, address1, selected):
            p.gate(a, out)
            p.gate(selector[0], a, out)
            p.gate(selector[0], b, out)
        selection_end = len(p.gates)
        lookup_start = len(p.gates)
        helpers["lookup_shared"](p, selected, [stock], [[word] for word in words], 3)
        lookup_end = len(p.gates)
    else:
        interfaces["stock"] = stock
    reference_start = len(p.gates)
    for wire in reference[:reference_bits]:
        p.emit("H", wire)
    core_start = len(p.gates)
    comparison_start = len(p.gates)
    for register in (reference, stock):
        p.gate(register[-1])
    helpers["less_than"](
        p,
        reference,
        stock,
        predicate[0],
        p.register(width + 1),
        p.register(width + 1),
        p.register(1)[0],
    )
    for register in (reference, stock):
        p.gate(register[-1])
    comparison_end = len(p.gates)
    p.emit("Z", control[0])
    p.emit("CZ", control[0], predicate[0])
    p.undo(comparison_start, comparison_end)
    core_end = len(p.gates)
    for wire in reference[:reference_bits]:
        p.emit("H", wire)
    reference_end = len(p.gates)
    if pair:
        p.undo(lookup_start, lookup_end)
        p.undo(selection_start, selection_end)
        p.emit("H", selector[0])
    phases = {
        "core": [core_start, core_end],
        "reference_transform": [reference_start, reference_end],
    }
    if pair:
        phases.update(selection=[selection_start, selection_end], lookup=[lookup_start, lookup_end])
    return p.record(interfaces, phases)


def stock_template_sharing_signature(nodes):
    """Semantic signature only; preserve every original ordered source array/hash."""
    comparison = []
    for row in nodes:
        check()
        arguments = list(row["args"])
        if row["op"] == "mul" and type(row["params"]) is dict and not row["params"]:
            require(len(arguments) == 2 and all(type(value) is int for value in arguments),
                    "Only parameter-free full72/F40 mul pairs may commute")
            arguments = sorted(arguments)
        comparison.append({**row, "args": arguments})
    # Exact JSON spelling preserves Boolean/integer/float literal distinctions.
    return canonical(comparison)


def stock_templates(target, census):
    check()
    require((target["width"], target["fraction_bits"]) == (W, F), "Original native72/f40 target")
    nodes = {}
    for node in target["nodes"]:
        check()
        require(len(node["out"]) == 1 or node["op"] == "lookup", "Typed target node")
        for value in node["out"]:
            require(value not in nodes, "Unique target SSA producer")
            nodes[value] = node
    results = []
    for asset in (0, 1):
        selected = [
            row
            for row in census["builder_label_proof"]["exponentials"]
            if row["asset"] == asset and row["date"] == 0
        ]
        require(len(selected) == 1, "Two exact original date0 stock occurrences")
        row, visited, sequence = selected[0], set(), []

        def visit(value):
            check()
            if value == row["clipped_log"] or value in visited:
                return
            require(value in nodes, "Stock dependency producer")
            node = nodes[value]
            require(
                node["op"] in ("const", "add", "sub", "mul", "cmul", "bits", "shift")
                and len(node["out"]) == 1,
                "Scalar stock-only closure",
            )
            for argument in node["args"]:
                visit(argument)
            visited.add(value)
            sequence.append(node)
            require(len(sequence) <= 64, "Fixed scalar closure cap")

        visit(row["stock"])
        identifiers = {row["clipped_log"]: 0}
        normalized = []
        for node in sequence:
            identifiers[node["out"][0]] = len(identifiers)
            normalized.append(
                {
                    "op": node["op"],
                    "args": [identifiers[value] for value in node["args"]],
                    "params": node["params"],
                    "out": identifiers[node["out"][0]],
                }
            )
        clips = [
            item
            for item in census["builder_label_proof"]["clips"]
            if item["out"] == row["clipped_log"]
        ]
        require(len(clips) == 1, "Exact source clamp membership")
        clamp = []
        for key in ("low", "high"):
            node = nodes[clips[0][key]]
            require(node["op"] == "const", "Literal native stock clamp")
            word = node["params"]["value"]
            require(type(word) is int and 0 <= word <= MASK, "CONST canonical modular72")
            clamp.append(signed(word))
        results.append(
            {
                "asset": asset,
                "date": 0,
                "clipped_log": row["clipped_log"],
                "stock": row["stock"],
                "clamps": clamp,
                "normalized_nodes": normalized,
                "output": identifiers[row["stock"]],
                "template_sha256": fingerprint(normalized),
            }
        )
    require(
        stock_template_sharing_signature(results[0]["normalized_nodes"])
        == stock_template_sharing_signature(results[1]["normalized_nodes"])
        and canonical(results[0]["clamps"]) == canonical(results[1]["clamps"]),
        "Exact scalar stock sharing: only parameter-free full72/F40 mul pairs commute",
    )
    return results


def scalar_stock(template, raw):
    require(
        template["clamps"][0] <= raw <= template["clamps"][1], "Fixed supported native stock input"
    )
    values = {0: raw & MASK}
    for node in template["normalized_nodes"]:
        check()
        op, params = node["op"], node["params"]
        words = [values[value] for value in node["args"]]
        args = [signed(value) for value in words]
        if op == "const":
            value = params["value"]
            require(type(value) is int and 0 <= value <= MASK, "Canonical CONST")
        elif op in ("add", "sub"):
            value = args[0] + args[1] if op == "add" else args[0] - args[1]
            require(-(1 << 71) <= value < (1 << 71), "Exact stock add/sub no wrap")
        elif op in ("mul", "cmul"):
            second = args[1] if op == "mul" else params["c"]
            require(
                type(second) is int and -(1 << 71) <= second < (1 << 71), "Signed CMUL or argument"
            )
            product = args[0] * second
            require(-(1 << 143) <= product < (1 << 143), "Full signed144 product")
            value = product >> F
            require(-(1 << 71) <= value < (1 << 71), "Stored stock product72 no wrap")
        elif op == "bits":
            shift, width = params["shift"], params["width"]
            require(
                type(shift) is int and type(width) is int and 1 <= width <= W, "Typed bits window"
            )
            value = args[0] if params.get("signed", False) else words[0]
            value = value >> shift if shift >= 0 else value << -shift
            value &= (1 << width) - 1
        elif op == "shift":
            require(-W < args[1] < W, "Actual bounded exponent shift")
            value = args[0] << args[1] if args[1] >= 0 else args[0] >> -args[1]
            require(-(1 << 71) <= value < (1 << 71), "Exact final shift72 no wrap")
        else:
            raise ValueError("Unsupported scalar stock operation")
        values[node["out"]] = value & MASK
    output = signed(values[template["output"]])
    require(0 <= output < MQ, "Fixed M=8192 strict nonnegative stock bound")
    return output


def store(state, register, word):
    for bit, wire in enumerate(register):
        if (word >> bit) & 1:
            state |= 1 << wire
    return state


def load(state, register):
    return sum(((state >> wire) & 1) << bit for bit, wire in enumerate(register))


def diagonal_basis(record, values, gate_range=None, inverse=False):
    """Exact native permutation and Z/CZ phase on one basis input, no H array."""
    check()
    state = 0
    for key, value in values.items():
        state = store(state, record["interfaces"][key], value)
    initial, phase = state, 1
    rows = record["gates"]
    if gate_range is not None:
        rows = rows[gate_range[0] : gate_range[1]]
    if inverse:
        rows = reversed(rows)
    for row in rows:
        visit_gate()
        kind, *wires = row
        if kind in ("X", "CX", "CCX"):
            if all((state >> wire) & 1 for wire in wires[:-1]):
                state ^= 1 << wires[-1]
        elif kind in ("Z", "CZ"):
            if all((state >> wire) & 1 for wire in wires):
                phase = -phase
        else:
            raise ValueError("Basis phase checker never executes Hadamards")
    occupied = {wire for register in record["interfaces"].values() for wire in register}
    require(
        all(((state >> wire) & 1) == 0 for wire in range(record["qubits"]) if wire not in occupied),
        "Native clean scratch",
    )
    return state, initial, phase


def qnormalize(value):
    a, b, power = value
    if a == b == 0:
        return (0, 0, 0)
    while power and a % 2 == b % 2 == 0:
        a, b, power = a // 2, b // 2, power - 1
    return a, b, power


def qadd(left, right):
    power = max(left[2], right[2])
    return qnormalize(
        (
            left[0] * (1 << (power - left[2])) + right[0] * (1 << (power - right[2])),
            left[1] * (1 << (power - left[2])) + right[1] * (1 << (power - right[2])),
            power,
        )
    )


def exact_vector(record, values):
    """Z[sqrt(2)]/dyadic arithmetic; tiny Hadamard register only."""
    state = 0
    for key, value in values.items():
        state = store(state, record["interfaces"][key], value)
    vector = {state: (1, 0, 0)}
    for row in record["gates"]:
        check()
        kind, *wires = row
        result = {}
        for word, amplitude in vector.items():
            visit_gate()
            if kind == "H":
                wire = wires[0]
                half = qnormalize((2 * amplitude[1], amplitude[0], amplitude[2] + 1))
                zero, one = word & ~(1 << wire), word | (1 << wire)
                sign = -1 if (word >> wire) & 1 else 1
                result[zero] = qadd(result.get(zero, (0, 0, 0)), half)
                result[one] = qadd(
                    result.get(one, (0, 0, 0)), (sign * half[0], sign * half[1], half[2])
                )
            else:
                if kind in ("X", "CX", "CCX") and all((word >> wire) & 1 for wire in wires[:-1]):
                    word ^= 1 << wires[-1]
                elif kind in ("Z", "CZ") and all((word >> wire) & 1 for wire in wires):
                    amplitude = (-amplitude[0], -amplitude[1], amplitude[2])
                result[word] = qadd(result.get(word, (0, 0, 0)), amplitude)
        vector = {word: amplitude for word, amplitude in result.items() if amplitude != (0, 0, 0)}
        require(len(vector) <= 8, "Fixed tiny sparse operator support")
    return vector, state


def resource_row(record):
    counts = Counter(row[0] for row in record["gates"])
    levels = [0] * record["qubits"]
    t_levels = levels.copy()
    for kind, *wires in record["gates"]:
        check()
        # Conservative expanded serial row, not a reused old whole-source schedule.
        cost = 15 if kind == "CCX" else 3 if kind == "CZ" else 1
        level, tlevel = (
            max(levels[wire] for wire in wires) + cost,
            max(t_levels[wire] for wire in wires) + (7 if kind == "CCX" else 0),
        )
        for wire in wires:
            levels[wire], t_levels[wire] = level, tlevel
    return {
        "qubits": record["qubits"],
        "source_gates": len(record["gates"]),
        "native_counts": {kind: counts[kind] for kind in ("X", "CX", "CCX", "H", "Z", "CZ")},
        "exact_CCX_T_count": 7 * counts["CCX"],
        "expanded_Clifford_CX": counts["CX"] + 6 * counts["CCX"] + counts["CZ"],
        "expanded_Clifford_H": counts["H"] + 2 * counts["CCX"] + 2 * counts["CZ"],
        "expanded_Clifford_Z": counts["Z"],
        "conservative_T_depth_upper": max(t_levels, default=0),
        "conservative_Clifford_T_depth_upper": max(levels, default=0),
        "schedule_scope": (
            "conservative recipe-only dependency upper bounds; "
            "not measured full-source or physical schedule"
        ),
        "all_lookup_copy_inverse_phase_and_preparation_gates_charged": True,
    }


def component_experiment(target, census, support, helpers):
    """One fixed construction, exactly charged recipes, no QSP/transcendental fit."""
    templates = stock_templates(target, census)
    lo, hi = templates[0]["clamps"]
    knots = (lo, lo + 1, 0, Q, 4 * Q, 5 * Q, hi - 1, hi)
    require(
        len(set(knots)) == 8 and all(lo <= raw <= hi for raw in knots),
        "Fixed knots are distinct and in original range",
    )
    require(
        support["passed"] is True and support["actual_stock_templates_checked"] == 48,
        "Pinned original B4 support premise",
    )
    cells = support["range_reduction_cells"]
    require(
        cells
        and all(0 <= cell["stock_interval"][0] <= cell["stock_interval"][1] < MQ for cell in cells),
        "All preserved support cells fit fixed M",
    )
    words = [scalar_stock(templates[0], raw) for raw in knots]
    recipes = {
        "native_signed_LT72": less_than_leaf(helpers),
        "QROM8_word72": qrom_leaf(helpers, words),
        "controlled_QROM8_word72": qrom_leaf(helpers, words, True),
        "controlled_one_stock53": signal_recipe(helpers, pair=False),
        "controlled_pair53": signal_recipe(helpers, words),
    }
    rows, checks = [], []
    for i, first in enumerate(words):
        for j, second in enumerate(words):
            check()
            total = first + second
            require(total < (1 << 71), "Two native stock sum no wrap")
            rows.append(
                {
                    "i": i,
                    "j": j,
                    "F1": first,
                    "F2": second,
                    "native_basket_raw": total // 2,
                    "alive": total < 280 * Q,
                    "positive": total >= 200 * Q + 2,
                    "one_stock_count_first": first,
                    "one_stock_count_second": second,
                    "pair_signal_exact": [total - MQ, MQ],
                }
            )
    boundary = []
    stock_low = min(cell["stock_interval"][0] for cell in cells)
    stock_high = max(cell["stock_interval"][1] for cell in cells)
    for label, center, offsets in (
        ("barrier", 280 * Q, (-1, 0, 1)),
        ("strike", 200 * Q, (-1, 0, 1, 2, 3)),
    ):
        for offset in offsets:
            total = center + offset
            basket = total // 2
            require(
                stock_low <= total // 2 <= stock_high
                and stock_low <= total - total // 2 <= stock_high,
                "Fixed boundary tuples in preserved native stock envelope; no preimage claim",
            )
            require(
                (basket < 140 * Q) == (total < 280 * Q)
                and ((basket - 100 * Q) > 0) == (total >= 200 * Q + 2),
                "Exact native integer tie contract",
            )
            boundary.append(
                {
                    "label": label,
                    "offset": offset,
                    "sum": total,
                    "F1": total // 2,
                    "F2": total - total // 2,
                    "alive": basket < 140 * Q,
                    "positive": basket > 100 * Q,
                }
            )
    for a, b in ((90 * Q, 90 * Q), (50 * Q, 162 * Q)):
        require(
            stock_low <= a <= stock_high and stock_low <= b <= stock_high,
            "Fixed equal-product tuples in native interface envelope",
        )
        boundary.append(
            {
                "label": "equal_product",
                "F1": a,
                "F2": b,
                "native_basket_raw": (a + b) // 2,
                "alive": (a + b) // 2 < 140 * Q,
                "positive": (a + b) // 2 > 100 * Q,
            }
        )
    for record_name in ("QROM8_word72", "controlled_QROM8_word72"):
        record = recipes[record_name]
        for address in range(8):
            for dirty in DIRTY_WORDS:
                for control in (0, 1) if "control" in record["interfaces"] else (1,):
                    inputs = {"address": address, "output": dirty}
                    if "control" in record["interfaces"]:
                        inputs["control"] = control
                    state, initial, phase = diagonal_basis(record, inputs)
                    require(
                        load(state, record["interfaces"]["output"])
                        == (dirty ^ (words[address] if control else 0))
                        and load(state, record["interfaces"]["address"]) == address
                        and phase == 1,
                        "Paid clean-XOR QROM absolute phase",
                    )
                    after = diagonal_basis(
                        record,
                        {**inputs, "output": load(state, record["interfaces"]["output"])},
                        inverse=True,
                    )
                    require(after[0] == initial and after[2] == 1, "QROM exact inverse")
                    checks.append(
                        {
                            "family": record_name,
                            "address": address,
                            "dirty": dirty,
                            "control": control,
                        }
                    )
    lt = recipes["native_signed_LT72"]
    pairs = tuple((a, b) for a in BOUNDARY_WORDS for b in BOUNDARY_WORDS) + SIGNED_PAIRS
    for a, b in pairs:
        for dirty in DIRTY_WORDS:
            state, initial, phase = diagonal_basis(
                lt, {"a": a & MASK, "b": b & MASK, "output": dirty}
            )
            require(
                load(state, lt["interfaces"]["output"]) == (dirty ^ int(a < b))
                and load(state, lt["interfaces"]["a"]) == (a & MASK)
                and load(state, lt["interfaces"]["b"]) == (b & MASK)
                and phase == 1,
                "Full72 signed comparator and dirty output",
            )
            inverse = diagonal_basis(
                lt,
                {"a": a & MASK, "b": b & MASK, "output": load(state, lt["interfaces"]["output"])},
                inverse=True,
            )
            require(inverse[0] == initial and inverse[2] == 1, "Full72 native LT actual inverse")
            checks.append({"family": "native_signed_LT72", "a": a, "b": b, "dirty": dirty})
    core = recipes["controlled_one_stock53"]
    for stock in BOUNDARY_WORDS:
        for reference in BOUNDARY_WORDS:
            for control in (0, 1):
                state, initial, phase = diagonal_basis(
                    core,
                    {"control": control, "reference": reference, "stock": stock},
                    core["phase_ranges"]["core"],
                )
                require(
                    state == initial and phase == (1 if not control or reference < stock else -1),
                    "Native53 reference/full72 phase, tie and inverse-clean ABI",
                )
                checks.append(
                    {"family": "native53_phase", "F": stock, "r": reference, "control": control}
                )
    # Tiny complete operators use only two uniform bits and a signed three-bit port.
    tiny = signal_recipe(helpers, width=3, reference_bits=2, pair=False)
    for stock in range(4):
        for reference in range(4):
            for control in (0, 1):
                vector, initial = exact_vector(
                    tiny, {"control": control, "reference": reference, "stock": stock}
                )
                allowed_outputs = set()
                for other in range(4):
                    expected = (
                        Fraction(int(other == reference), 1)
                        if not control
                        else sum(
                            (
                                Fraction(1 if r < stock else -1, 4)
                                * (-1) ** (((reference ^ other) & r).bit_count())
                                for r in range(4)
                            ),
                            Fraction(),
                        )
                    )
                    word = (
                        initial & ~sum(1 << wire for wire in tiny["interfaces"]["reference"])
                    ) | store(0, tiny["interfaces"]["reference"], other)
                    allowed_outputs.add(word)
                    actual = vector.get(word, (0, 0, 0))
                    require(
                        actual[1] == 0 and Fraction(actual[0], 1 << actual[2]) == expected,
                        "Independent tiny Walsh operator and absolute controlled phase",
                    )
                require(
                    len(vector) <= 4 and set(vector) <= allowed_outputs,
                    "Tiny stock/control inputs and every private scratch wire restored",
                )
                checks.append(
                    {
                        "family": "tiny_complete_operator",
                        "F": stock,
                        "r": reference,
                        "control": control,
                    }
                )
    # Native53 pair phase tests remove ONLY reference H gates in a declared
    # test view. The actual recipe retains/charges all106; counting proves its
    # 53-bit zero-block overlap. Selector H/control/lookup remain actual gates.
    pair = recipes["controlled_pair53"]
    reference_wires = set(pair["interfaces"]["reference"])
    removed = [
        index
        for index, row in enumerate(pair["gates"])
        if row[0] == "H" and row[1] in reference_wires
    ]
    require(len(removed) == 106, "Actual53-H preparation and inverse paid")
    removed_set = set(removed)
    test_view = {
        **pair,
        "gates": [row for index, row in enumerate(pair["gates"]) if index not in removed_set],
    }
    for i, first in enumerate(words):
        for j, second in enumerate(words):
            for reference in BOUNDARY_WORDS:
                for control in (0, 1):
                    for selector in (0, 1):
                        vector, initial = exact_vector(
                            test_view,
                            {
                                "address0": i,
                                "address1": j,
                                "reference": reference,
                                "control": control,
                                "selector": selector,
                            },
                        )
                        phases = (
                            1 if not control or reference < first else -1,
                            1 if not control or reference < second else -1,
                        )
                        for output in (0, 1):
                            word = initial ^ (
                                (selector ^ output) << pair["interfaces"]["selector"][0]
                            )
                            expected = Fraction(
                                phases[0] + phases[1]
                                if output == selector
                                else phases[0] - phases[1],
                                2,
                            )
                            amplitude = vector.get(word, (0, 0, 0))
                            require(
                                amplitude[1] == 0
                                and Fraction(amplitude[0], 1 << amplitude[2]) == expected,
                                "Actual native53 pair selected-QROM controlled absolute phase",
                            )
                        require(
                            len(vector) <= 2
                            and all(
                                word
                                in (initial, initial ^ (1 << pair["interfaces"]["selector"][0]))
                                for word in vector
                            ),
                            "All pair inputs and non-block scratch restored",
                        )
                        checks.append(
                            {
                                "family": "native53_pair_phase",
                                "i": i,
                                "j": j,
                                "r": reference,
                                "control": control,
                                "selector": selector,
                            }
                        )
    require(
        len(rows) == 64 and len(boundary) == 10 and len(checks) == 2608,
        "Fixed semantic and actual basis/operator inventory",
    )
    return {
        "templates": templates,
        "knots_raw": list(knots),
        "native_words": words,
        "offline_native_scalar_evaluations": 8,
        "offline_pair_truth_records": 64,
        "rows": rows,
        "boundary_cases": boundary,
        "checks": checks,
        "recipes": recipes,
        "tiny_recipe": tiny,
        "native_pair_phase_test_view": {
            "source_recipe_sha256": pair["recipe_sha256"],
            "removed_reference_H_indices": removed,
            "removed_gates_counted_in_actual_cost": True,
            "not_a_full53_statevector": True,
        },
        "exact_gate_state_visits": GATE_VISITS,
        "resources": {name: resource_row(recipe) for name, recipe in recipes.items()},
        "exact_counting_proof": {
            "uniform_reference_bits": 53,
            "uniform_states": MQ,
            "positive_phase_states_for_F": "exactly F",
            "one_stock_signal": "(2F-MQ)/MQ",
            "pair_signal": "(F1+F2-MQ)/MQ",
            "guaranteed_integer_half_threshold_gap": [1, 2 * MQ],
            "no_53bit_statevector": True,
        },
        "whole_source_comparison": {
            "status": "NOT_FULL_SOURCE_COSTED",
            "general_full72_or_q32_oracle_supplied": False,
            "threshold_transform_supplied": False,
            "new_financial_bias_allocation": None,
            "arithmetic_removal_or_adoption": False,
        },
    }
