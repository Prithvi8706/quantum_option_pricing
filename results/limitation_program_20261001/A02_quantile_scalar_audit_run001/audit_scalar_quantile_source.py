"""Independent audit of saved guarded AS241 scalar native sources.

No producer graph builder, compiler, leaf generator, resource calculator or
gate evaluator is imported. This audit reads existing arrays; it never emits
or replays gates. Its integer fixtures reconcile preserved replay evidence,
not a new all-input sampling argument or financial adoption.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import sys
import time
import traceback
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
RESEARCH = ROOT / "research/limitation_program_20261001"
SCALAR = PROGRAM / "A02_quantile_scalar_run001"
DIVIDER = PROGRAM / "A17_quantile_divider_run001"
CENTRAL = PROGRAM / "A02_quantile_central_run002"
TAIL = PROGRAM / "A02_quantile_tail_run001"
TRANSFORM = PROGRAM / "A02_quantile_transform_run002"
SQRT = PROGRAM / "A10_coefficient_run001/B4x12/min-depth/leaves/160a18dba2e09b8e1ad2.json"
RECEIPTS = (
    SCALAR,
    DIVIDER,
    CENTRAL,
    TAIL,
    PROGRAM / "A02_quantile_central_audit_run001",
    PROGRAM / "A02_quantile_tail_audit_run001",
    TRANSFORM,
    PROGRAM / "A02_quantile_transform_audit_run001",
    PROGRAM / "A02_quantile_law_run001",
    PROGRAM / "A02_quantile_law_audit_run001",
)
CODE = ("audit_scalar_quantile_source.py", "scalar_quantile_source_audit_preflight.json")
W, F, S = 72, 40, 1 << 40
MASK = (1 << W) - 1
KTAIL, KCENTRAL = 322122546, 322122547
PTAIL, PCENTRAL = (2 * KTAIL + 1) << 7, (2 * KCENTRAL + 1) << 7
QCENTRAL = S // 2 - PCENTRAL
WORDS = (
    0,
    (1 << 32) - 1,
    KTAIL,
    KCENTRAL,
    (1 << 32) - 1 - KTAIL,
    (1 << 32) - 1 - KCENTRAL,
    (1 << 31) - 1,
    1 << 31,
)
CPU_LIMIT, ADMISSION_CPU, WALL_LIMIT = 180, 150, 600
SCAN_FIELDS = ("x", "cx", "ccx", "source_gates", "t_count", "t_depth", "clifford_t_depth")
CCX = (
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


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def create(path, value):
    with Path(path).open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def fingerprint(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def q(value):
    if type(value) is int:
        return Fraction(value)
    if (
        isinstance(value, list)
        and len(value) == 2
        and all(type(item) is int for item in value)
        and value[1] > 0
    ):
        return Fraction(*value)
    raise ValueError("An exact integer or rational pair is required")


def pair(value):
    return [value.numerator, value.denominator]


def same(actual, expected, label):
    if canonical(actual) != canonical(expected):
        raise ValueError("Independent scalar source reconciliation failed: " + label)


def require(condition, label):
    if not condition:
        raise ValueError("Independent scalar source premise missing: " + label)


def verify(frozen):
    for name, expected in frozen.items():
        path = (ROOT / name).resolve()
        path.relative_to(ROOT)
        require(sha(path) == expected, "frozen bytes: " + name)


def bound_path(path, frozen):
    path = Path(path).resolve()
    name = relative(path)
    require(name in frozen and frozen[name] == sha(path), "manifest membership: " + name)
    return path


class Specification:
    """An independent symbolic recorder; no SDK or producer Graph is used."""

    def __init__(self):
        self.nodes, self.constants, self.values = [], {}, 0

    def emit(self, operation, *args, params=None, count=1):
        outs = list(range(self.values, self.values + count))
        self.values += count
        self.nodes.append(
            {"op": operation, "args": list(args), "params": params or {}, "out": outs}
        )
        return outs[0] if count == 1 else outs

    def constant(self, raw):
        if raw not in self.constants:
            self.constants[raw] = self.emit("const", params={"value": raw})
        return self.constants[raw]

    def minimum(self, a, b):
        return self.emit("select", self.emit("lt", a, b), a, b)

    def maximum(self, a, b):
        return self.emit("select", self.emit("lt", a, b), b, a)

    def bits(self, value, shift, width=W):
        return self.emit("bits", value, params={"shift": shift, "width": width, "signed": False})

    def polynomial(self, raw_coefficients, argument):
        value = self.constant(raw_coefficients[-1])
        for raw in raw_coefficients[-2::-1]:
            # This multiplication always has its own floor before the next add.
            product = self.emit("mul", value, argument)
            value = self.emit("add", product, self.constant(raw))
        return value


def audit_recipe(target, bindings, literals, central, tail, native):
    require(
        all(item.get("certified") is True for item in (central, tail, native)),
        "complete central/tail/native arithmetic certificates",
    )
    require(native.get("budget_censored") is False, "uncensored native transform")
    same(
        (literals["width"], literals["fraction_bits"], literals["uniform_bits"]),
        (W, F, 32),
        "scalar representation",
    )
    same(
        literals["central_A_raw"],
        central["native_arithmetic"]["native_A_raw_ascending"],
        "central numerator literal coefficients",
    )
    same(
        literals["central_B_raw"],
        central["native_arithmetic"]["native_B_raw_ascending"],
        "central denominator literal coefficients",
    )
    same(
        literals["tail_A_raw"],
        tail["native_interface"]["native_A_raw_ascending"],
        "tail numerator literal coefficients",
    )
    same(
        literals["tail_B_raw"],
        tail["native_interface"]["native_B_raw_ascending"],
        "tail denominator literal coefficients",
    )
    same(
        literals["log_table"],
        [
            [entry["literal_raw"] for entry in row["coefficient_checks"]]
            for row in native["transform"]["log_table_cells"]
        ],
        "all original log coefficient literals",
    )
    same(
        (literals["central_rconstant_raw"], literals["tail_shift_raw"], literals["ln2_raw"]),
        (198599287768, 1759218604442, 762123384786),
        "exact source constants",
    )
    require(native["transform"]["original_ln2_raw"] == literals["ln2_raw"], "ln2 provenance")
    for name in ("central_A_raw", "central_B_raw", "tail_A_raw", "tail_B_raw"):
        require(
            len(literals[name]) == 8
            and all(type(raw) is int and 0 < raw < 1 << 71 for raw in literals[name]),
            "eight positive signed72 polynomial coefficients",
        )
    require(
        literals["central_B_raw"][0] == literals["tail_B_raw"][0] == S,
        "positive denominator constant",
    )
    require(
        len(literals["log_table"]) == 32
        and all(
            len(row) == 9 and all(type(raw) is int and -(1 << 71) <= raw < 1 << 71 for raw in row)
            for row in literals["log_table"]
        ),
        "32 by 9 signed72 archive table",
    )
    branch = (3 * S + 20) // 40  # nearest integer; this rational is not a tie.
    require(
        PTAIL < Fraction(3 * S, 40) < PCENTRAL
        and PTAIL < branch < PCENTRAL
        and PCENTRAL - PTAIL == 256
        and PTAIL % 256 == PCENTRAL % 256 == 128
        and branch % 256 != 128
        and 0 < QCENTRAL < Fraction(17 * S, 40),
        "exact adjacent actual q32 branch words",
    )
    g = Specification()
    raw = g.emit("input", params={"name": "k", "bits": 32, "preparation": "uniform"})
    zero, scale, half = (g.constant(value) for value in (0, S, S // 2))
    uniform = g.emit("add", g.bits(raw, -8), g.constant(128))
    displacement = g.emit("sub", uniform, half)
    negative = g.emit("lt", uniform, half)
    absolute = g.emit("select", negative, g.emit("sub", zero, displacement), displacement)
    probability = g.minimum(uniform, g.emit("sub", scale, uniform))
    is_tail = g.emit("lt", probability, g.constant(branch))
    central_q = g.minimum(absolute, g.constant(QCENTRAL))
    tail_p = g.minimum(probability, g.constant(PTAIL))
    central_r = g.emit(
        "sub", g.constant(literals["central_rconstant_raw"]), g.emit("mul", central_q, central_q)
    )
    ca, cb = (
        g.polynomial(literals[name], central_r) for name in ("central_A_raw", "central_B_raw")
    )
    central_numerator = g.emit("mul", central_q, ca)
    guarded = g.maximum(tail_p, g.constant(1))
    top = g.emit("msb", guarded)
    exponent = g.emit("sub", top, g.constant(F))
    mantissa = g.emit("shift", guarded, g.emit("sub", zero, exponent))
    # The original clip call materializes BOTH constant arguments before its
    # inner maximum. Preserve even this instruction/constant-cache ordering.
    clip_lower, clip_upper = g.constant(S), g.constant(2 * S - 1)
    clipped = g.minimum(g.maximum(mantissa, clip_lower), clip_upper)
    index = g.bits(g.emit("sub", clipped, g.constant(S)), F - 5, 5)
    center = g.emit("add", g.bits(index, -(F - 5)), g.constant(S + (1 << (F - 6))))
    local = g.emit("sub", clipped, center)
    table_coefficients = g.emit("lookup", index, params={"table": "log", "bits": 5}, count=9)
    polynomial = table_coefficients[-1]
    for coefficient in table_coefficients[-2::-1]:
        polynomial = g.emit("add", g.emit("mul", polynomial, local), coefficient)
    scaled_exponent = g.bits(exponent, -F)
    exponent_product = g.emit("cmul", scaled_exponent, params={"c": literals["ln2_raw"]})
    logarithm = g.emit("add", polynomial, exponent_product)
    negative_log = g.emit("sub", zero, logarithm)
    root_argument = g.emit("positive", negative_log)
    root = g.emit("sqrt", root_argument)
    tail_r = g.emit("sub", root, g.constant(literals["tail_shift_raw"]))
    ta, tb = (g.polynomial(literals[name], tail_r) for name in ("tail_A_raw", "tail_B_raw"))
    numerator = g.emit("select", is_tail, ta, central_numerator)
    denominator = g.emit("select", is_tail, tb, cb)
    divisor = g.maximum(denominator, g.constant(1))
    quotient = g.emit("divide", numerator, divisor)
    output = g.emit("select", negative, g.emit("sub", zero, quotient), quotient)
    expected_target = {
        "format": "reversible-fixed-point-ssa-v1",
        "fraction_bits": F,
        "width": W,
        "nodes": g.nodes,
        "inputs": [raw],
        "outputs": {"Z": output},
        "tables": {"log": literals["log_table"]},
        "semantics": "Signed two-complement fixed-point; flags and indexes are unscaled integers; "
        "all output arithmetic is modulo 2^width.",
    }
    expected_bindings = {
        "raw_input": raw,
        "uniform": uniform,
        "q": displacement,
        "negative": negative,
        "qabs": absolute,
        "probability": probability,
        "tail": is_tail,
        "central_qguard": central_q,
        "tail_pguard": tail_p,
        "central_r": central_r,
        "central_A": ca,
        "central_B": cb,
        "central_numerator": central_numerator,
        "log_guarded_input": guarded,
        "log_exponent": exponent,
        "log_mantissa": mantissa,
        "log_clipped_mantissa": clipped,
        "log_index": index,
        "log_local": local,
        "log_output": logarithm,
        "log_scaled_exponent": scaled_exponent,
        "log_exponent_product": exponent_product,
        "negative_log": negative_log,
        "sqrt_argument": root_argument,
        "square_root": root,
        "tail_r": tail_r,
        "tail_A": ta,
        "tail_B": tb,
        "selected_numerator": numerator,
        "selected_denominator": denominator,
        "guarded_divisor": divisor,
        "quotient": quotient,
        "output": output,
    }
    same(target, expected_target, "complete independently reconstructed guarded SSA")
    same(bindings, expected_bindings, "every semantic producer binding")
    return g.values


def audit_site_proofs(target, bindings, literals, proofs, central, tail, native):
    same(proofs["target_sha256"], fingerprint(target), "typed complete target hash")
    same(proofs["literal_sha256"], fingerprint(literals), "typed literal hash")
    for flag in (
        "all_q32_inputs_covered_structurally",
        "guarded_unused_branches_have_certified_domains",
        "central_positive_multiply_before_divide_preserved",
    ):
        require(proofs.get(flag) is True, flag)
    for flag in (
        "range_certificate_based_on_sampled_inputs",
        "selected_branch_guard_changes_result",
        "native_financial_path_or_Box_Muller_law_adopted",
    ):
        require(proofs.get(flag) is False, flag)
    require(proofs["shared_divide_count"] == 1, "one selected native divide")
    cn, tn, cd = (
        central["native_arithmetic"],
        tail["native_interface"],
        native["central_denominator64"],
    )
    required = (
        (
            cn,
            (
                "signed72_stored_values_no_overflow",
                "signed144_full_multiply_products_no_overflow",
                "unsigned112_division_numerator_no_truncation",
                "native_divider_clamp_inactive",
            ),
        ),
        (
            tn,
            (
                "signed72_stored_values_no_overflow",
                "signed144_full_products_no_overflow",
                "unsigned112_dividend_no_truncation",
                "unsigned64_denominator_no_truncation",
                "native_denominator_floor_at_one_guard_inactive",
            ),
        ),
        (cd, ("unsigned64_denominator_no_truncation",)),
    )
    for record, flags in required:
        for flag in flags:
            require(record.get(flag) is True, "trusted prior all-input native guard: " + flag)
    require(
        native.get("actual_q32_native_transform_error_included") is True,
        "actual native transform, rather than hypothetical exact input",
    )
    require(
        q(native["transform"]["native_negative_log_lower_exact"]) > 0,
        "native positive-root guard is inactive throughout the guarded tail domain",
    )
    require(
        q(cn["r_native_lower_exact"]) == 0
        and q(native["transform"]["actual_native_r_range_exact"][0]) > 0,
        "both positive-coefficient denominators are at least their constant S",
    )
    maximum_divisor = max(
        q(cd["maximum_central_denominator_raw_upper_exact"]),
        q(tn["maximum_denominator_raw_upper_exact"]),
    )
    maximum_numerator = (
        max(
            q(cn["maximum_shifted_division_numerator_raw_upper_exact"]),
            q(tn["maximum_shifted_division_numerator_raw_upper_exact"]),
        )
        / S
    )
    maximum_root_input = q(native["transform"]["native_negative_log_upper_exact"]) * S
    require(
        S <= maximum_divisor < 1 << 64
        and 0 <= maximum_numerator < 1 << W
        and 0 < maximum_root_input < 1 << 45,
        "strict full native operand guard arithmetic",
    )
    expected = {
        "divide": {
            "value": bindings["quotient"],
            "args": [bindings["selected_numerator"], bindings["guarded_divisor"]],
            "unsigned_numerator_lower": 0,
            "unsigned_numerator_upper_exact": pair(maximum_numerator),
            "denominator_lower": S,
            "denominator_upper_exact": pair(maximum_divisor),
            "input_contract": {"unsigned_denominator_bits": 64},
            "raw_one_denominator_guard_inactive": True,
        },
        "sqrt": {
            "value": bindings["square_root"],
            "args": [bindings["sqrt_argument"]],
            "unsigned_input_upper_exact": pair(maximum_root_input),
            "input_contract": {"unsigned_input_bits": 46},
            "positive_guard_inactive": True,
        },
    }
    same(proofs["sites"], expected, "every typed operand/producer/range proof field")
    return expected


def audit_ccx_prior(frozen):
    proof = read(bound_path(DIVIDER / "exact_CCX_phase_proof.json", frozen))
    same(
        proof,
        [
            {
                "input": value,
                "output": value ^ (((value & 1) & ((value >> 1) & 1)) << 2),
                "exact_nonzero_phase": 1,
            }
            for value in range(8)
        ],
        "eight preserved exact Q(omega) phase-one proof columns",
    )
    path = bound_path(RESEARCH / "temporary_and_fulladder.py", frozen)
    functions = [
        node
        for node in ast.parse(path.read_text(encoding="utf-8")).body
        if isinstance(node, ast.FunctionDef) and node.name == "ccx_seven_t"
    ]
    require(len(functions) == 1, "one frozen seven-T macro definition")
    returned = [node for node in functions[0].body if isinstance(node, ast.Return)]
    require(len(returned) == 1 and isinstance(returned[0].value, ast.List), "literal macro list")
    rows = []
    for item in returned[0].value.elts:
        require(
            isinstance(item, ast.Call)
            and isinstance(item.func, ast.Name)
            and item.func.id == "gate"
            and not item.keywords,
            "literal macro gate call",
        )
        require(
            isinstance(item.args[0], ast.Constant)
            and all(isinstance(arg, ast.Name) for arg in item.args[1:]),
            "literal macro operands",
        )
        rows.append((item.args[0].value, *(arg.id for arg in item.args[1:])))
    same(rows, CCX, "paid macro chronology bound to the exact prior phase proof")
    same(
        Counter(row[0] for row in rows),
        {"H": 2, "CX": 6, "T": 4, "Tdg": 3},
        "full seven-T, six-CX, two-H primitive",
    )


def make_scanner():
    """Compile only this independent counter after the audit has been frozen."""
    import numpy as np
    from numba import njit

    @njit(cache=False)
    def scan(gates, qubits, inverse):
        # Single-wire T/H and two-wire CX rows from the hash-bound exact macro.
        # The native inverse reverses X/CX/CCX rows; these native gates are self-inverse.
        t_layers = np.zeros(qubits, np.int64)
        gate_layers = np.zeros(qubits, np.int64)
        counts = np.zeros(3, np.int64)
        wire_pairs = np.empty((15, 2), np.int64)
        is_t = (
            False,
            False,
            True,
            False,
            True,
            False,
            True,
            False,
            True,
            True,
            False,
            False,
            True,
            True,
            False,
        )
        for position in range(len(gates)):
            index = len(gates) - 1 - position if inverse else position
            kind, a, b, c = gates[index]
            if not 1 <= kind <= 3 or not 0 <= a < qubits:
                raise ValueError("Invalid native opcode or first wire")
            if kind < 2 and b != 0 or kind < 3 and c != 0:
                raise ValueError("Nonzero unused packed native columns")
            if kind >= 2 and (not 0 <= b < qubits or a == b):
                raise ValueError("Invalid/aliased native second wire")
            if kind == 3 and (not 0 <= c < qubits or a == c or b == c):
                raise ValueError("Invalid/aliased native third wire")
            counts[kind - 1] += 1
            if kind == 1:
                gate_layers[a] += 1
            elif kind == 2:
                level = max(t_layers[a], t_layers[b])
                depth = max(gate_layers[a], gate_layers[b]) + 1
                t_layers[a] = t_layers[b] = level
                gate_layers[a] = gate_layers[b] = depth
            else:
                wire_pairs[0] = (c, c)
                wire_pairs[1] = (b, c)
                wire_pairs[2] = (c, c)
                wire_pairs[3] = (a, c)
                wire_pairs[4] = (c, c)
                wire_pairs[5] = (b, c)
                wire_pairs[6] = (c, c)
                wire_pairs[7] = (a, c)
                wire_pairs[8] = (b, b)
                wire_pairs[9] = (c, c)
                wire_pairs[10] = (c, c)
                wire_pairs[11] = (a, b)
                wire_pairs[12] = (a, a)
                wire_pairs[13] = (b, b)
                wire_pairs[14] = (a, b)
                for slot in range(15):
                    first, second = wire_pairs[slot]
                    level = max(t_layers[first], t_layers[second]) + int(is_t[slot])
                    depth = max(gate_layers[first], gate_layers[second]) + 1
                    t_layers[first] = t_layers[second] = level
                    gate_layers[first] = gate_layers[second] = depth
        return counts, np.max(t_layers), np.max(gate_layers)

    return np, scan


def scan_array(path, qubits, np, scanner, checkpoint):
    checkpoint()
    array = np.load(path, mmap_mode="r", allow_pickle=False)
    require(
        array.dtype == np.dtype("int32") and array.ndim == 2 and array.shape[1] == 4,
        "exact packed int32 native gate array ABI",
    )
    require(type(qubits) is int and 0 < qubits < 1 << 20, "bounded explicit native allocation")
    result = []
    for reverse in (False, True):
        checkpoint()
        counts, td, depth = scanner(array, qubits, reverse)
        x, cx, ccx = map(int, counts)
        result.append(
            dict(
                x=x,
                cx=cx,
                ccx=ccx,
                source_gates=len(array),
                t_count=7 * ccx,
                t_depth=int(td),
                clifford_t_depth=int(depth),
            )
        )
    return result


def generic_key(node, target):
    table = target["tables"].get(node["params"].get("table"))
    spec = {
        "op": node["op"],
        "width": W,
        "fraction_bits": F,
        "params": node["params"],
        "table": table,
    }
    if node["op"] == "lookup":
        spec["lowering"] = "shared-prefix-xor-v1"
    return fingerprint(spec)[:20]


def divider_spec(candidate):
    if not candidate:
        return {"op": "divide", "width": W, "fraction_bits": F}
    return {
        "op": "divide",
        "width": W,
        "fraction_bits": F,
        "denominator_bits": 64,
        "lowering": "unsigned-restoring-denominator-width-clean-xor-v1",
        "unsigned_inputs": True,
        "input_contract": {"unsigned_denominator_bits": 64},
        "zero_divisor_behavior": "Full output mask, matching original unsigned divider",
        "division_output": "Low width bits of floor((unsigned_a << fraction_bits)/unsigned_b)",
        "dirty_output_XOR": True,
        "input_words_preserved": True,
        "literal_gate_inverse": True,
        "scratch_initial_and_final_zero": True,
        "unpriced_quantile_sign_restore_and_path_interface": True,
        "current_Box_Muller_source_dispatch": False,
    }


def audit_one_source(label, target, proofs, bindings, words, np, scanner, frozen, checkpoint):
    directory = SCALAR / label
    source = read(bound_path(directory / "source.json", frozen))
    same(read(bound_path(directory / "target.json", frozen)), target, label + " target file")
    candidate = label == "candidate64"
    require(
        source["format"] == "hierarchical-clean-xor-source-v1"
        and source["word_width"] == W
        and source["fraction_bits"] == F
        and source["values"] == words
        and source["exact_clifford_t"] is True
        and source["arbitrary_rotations"] == 0,
        "full scalar source format",
    )
    same(source["outputs"], target["outputs"], "named full72 output bank")
    same(
        source["inputs"],
        [node for node in target["nodes"] if node["op"] == "input"],
        "full72 input bank with only32 uniform prepared bits",
    )
    same(source["new_site_proofs"], proofs, "source embeds exact typed new-site proofs")
    require(
        source["fixed_optimizer"] == "none: exact guarded SSA recipe and floor order retained"
        and source["scalar_law"] == "independent q32 mathematical-native signed-restored AS241"
        and source["accepted_Box_Muller_source_changed"] is False,
        "one unoptimized NEW scalar law, not inherited old BM costs",
    )
    same(
        source["clean_schedule"],
        [
            "forward_calls",
            "CX each named SSA output to its separate output register",
            "reverse forward_calls with each leaf inverted",
        ],
        "literal clean dispatch sequence",
    )
    same(
        source["invocation_semantics"],
        "Copy every argument to a distinct clean local slot; bind output slots to fresh SSA "
        "output registers; execute leaf; uncopy arguments. "
        "Shared non-output local slots start/end zero.",
        "distinct copied argument slots and clean scratch dispatch",
    )
    same(
        source["inverse_semantics"],
        "Reverse the clean schedule and invert every leaf; all basis gates are self-inverse.",
        "literal inverse dispatch",
    )
    library = (directory / "leaves").resolve()
    for field in ("library", "library_workspace_relative"):
        raw = str(source[field]).replace("\\", "/")
        resolved = Path(raw).resolve() if Path(raw).is_absolute() else (ROOT / raw).resolve()
        require(resolved == library, "source library confined to its immutable receipt")
    nodes = [node for node in target["nodes"] if node["op"] != "input"]
    calls = source["forward_calls"]
    require(len(calls) == len(nodes), "every noninput SSA node invoked once in order")
    keys = sorted({call["leaf"] for call in calls})
    same(source["library_keys"], keys, "complete source library dispatch set")
    same(sorted(path.stem for path in library.glob("*.json")), keys, "no unlisted leaf metadata")
    same(sorted(path.stem for path in library.glob("*.npy")), keys, "no unlisted native arrays")
    divider_rows = read(bound_path(DIVIDER / "leaf_ledgers.json", frozen))
    require(len(divider_rows) == 2, "exactly two preserved divider arrays")
    divider_records = {row["name"]: row for row in divider_rows}
    require(set(divider_records) == {"candidate64", "original72"}, "divider record names")
    root_entry = read(bound_path(SQRT, frozen))
    root_spec = root_entry["spec"]
    same(
        {
            name: root_spec[name]
            for name in (
                "op",
                "width",
                "fraction_bits",
                "active_input_bits",
                "input_contract",
                "lowering",
            )
        },
        {
            "op": "sqrt",
            "width": W,
            "fraction_bits": F,
            "active_input_bits": 46,
            "input_contract": {"unsigned_input_bits": 46},
            "lowering": "unsigned-nonrestoring-sqrt-signed-remainder-v1",
        },
        "archived sqrt46 ABI",
    )
    metadata, native_rows, admissions = {}, {}, []
    for key in keys:
        checkpoint()
        require(
            len(key) == 20 and all(char in "0123456789abcdef" for char in key),
            "safe canonical leaf key",
        )
        entry = read(bound_path(library / (key + ".json"), frozen))
        require(entry["key"] == key and entry["gate_file"] == key + ".npy", "metadata/file key ABI")
        path = bound_path(library / entry["gate_file"], frozen)
        digest = sha(path)
        require(digest == entry["sha256"], "actual native gate byte hash")
        registers = entry["args"] + entry["outs"]
        same(
            registers,
            [list(range(index * W, (index + 1) * W)) for index in range(len(registers))],
            "all full72 native input/output slots",
        )
        qubits = entry["resources"]["qubits"]
        require(qubits >= W * len(registers), "native I/O included in complete allocation")
        forward, inverse = scan_array(path, qubits, np, scanner, checkpoint)
        for field in SCAN_FIELDS:
            same(entry["resources"][field], forward[field], "native forward metadata " + field)
        same(
            entry["resources"]["clifford_cx"],
            forward["cx"] + 6 * forward["ccx"],
            "every exact CCX's six paid Clifford CX",
        )
        same(
            entry["resources"]["clifford_h"],
            2 * forward["ccx"],
            "every exact CCX's two paid Clifford H",
        )
        native_rows[key] = {
            "qubits": qubits,
            "gate_sha256": digest,
            "native_args": entry["args"],
            "native_outputs": entry["outs"],
            "forward": forward,
            "literal_inverse": inverse,
        }
        metadata[key] = entry
    forward_totals, inverse_totals = Counter(), Counter()
    old_operation, copies, copy_rounds, scratch = {}, 0, 0, 0
    for node, call in zip(nodes, calls, strict=True):
        entry = metadata[call["leaf"]]
        same(
            call,
            {
                "leaf": call["leaf"],
                "args": node["args"],
                "out": node["out"],
                "argument_copy_cx": 2 * W * len(node["args"]),
            },
            "actual forward invocation",
        )
        same((entry["op"], entry["params"]), (node["op"], node["params"]), "leaf operation/params")
        require(
            len(entry["args"]) == len(node["args"]) and len(entry["outs"]) == len(node["out"]),
            "native invocation input/output arity",
        )
        table = target["tables"].get(node["params"].get("table"))
        same(
            entry["table_bits"],
            0 if table is None else len(table) * len(table[0]) * W,
            "all native lookup outputs/table bits included",
        )
        if node["op"] in ("sqrt", "divide"):
            site = proofs["sites"][node["op"]]
            same(
                (node["args"], node["out"]),
                (site["args"], [site["value"]]),
                "exact new producer site guard",
            )
            if node["op"] == "sqrt":
                same(
                    (node["args"], node["out"]),
                    ([bindings["sqrt_argument"]], [bindings["square_root"]]),
                    "sqrt producer identity",
                )
                origin, original = SQRT, root_entry
                same(entry["spec"], original["spec"], "unchanged actual unsigned46 sqrt spec")
                for field in ("args", "outs", "resources"):
                    same(entry[field], original[field], "unchanged full native sqrt " + field)
                same(call["leaf"], original["key"], "exact sqrt registry key")
                origin_array = bound_path(SQRT.parent / original["gate_file"], frozen)
                same(entry["input_contract"], {"unsigned_input_bits": 46}, "sqrt operand contract")
            else:
                row = divider_records["candidate64" if candidate else "original72"]
                same(
                    row["spec"],
                    divider_spec(candidate),
                    "preserved candidate/control division spec",
                )
                same(entry["spec"], row["spec"], "actual selected divider ABI")
                same(entry["args"], row["input_registers"], "divider full72 inputs")
                same(entry["outs"], row["output_registers"], "divider full72 dirty output")
                same(entry["resources"], row["resources"], "complete preserved divider allocation")
                same(
                    call["leaf"],
                    fingerprint({"spec": row["spec"], "params": {}})[:20],
                    "divider canonical registry key",
                )
                same(
                    entry["input_contract"],
                    {"unsigned_denominator_bits": 64} if candidate else {},
                    "selected divider dispatch contract",
                )
                origin = DIVIDER / "leaf_ledgers.json"
                origin_array = bound_path(ROOT / row["actual_gate_file"].replace("\\", "/"), frozen)
                require(
                    sha(origin_array) == row["actual_gate_sha256"], "original divider saved bytes"
                )
            same(entry["sha256"], sha(origin_array), "typed native bytes equal the frozen original")
            same(entry["proof_target_sha256"], fingerprint(target), "typed leaf whole-target hash")
            same(
                entry["origin_receipt_or_metadata"].replace("\\", "/"),
                relative(origin),
                "typed original metadata provenance",
            )
            same(entry["origin_gate_sha256"], sha(origin_array), "typed original gate provenance")
            admissions.append(
                {
                    "op": node["op"],
                    "out": node["out"],
                    "args": node["args"],
                    "leaf": call["leaf"],
                    "whole_target_sha256": fingerprint(target),
                    "all_input_new_site_proof": True,
                    "native_gate_sha256": entry["sha256"],
                }
            )
        else:
            same(call["leaf"], generic_key(node, target), "generic72 native registry fingerprint")
        row = native_rows[call["leaf"]]
        forward_totals.update(row["forward"])
        inverse_totals.update(row["literal_inverse"])
        copies += 2 * W * len(node["args"])
        copy_rounds += max(Counter(node["args"]).values(), default=0)
        scratch = max(scratch, row["qubits"] - len(node["out"]) * W)
        bucket = old_operation.setdefault(node["op"], Counter(calls=0, t_count=0, t_depth=0))
        bucket["calls"] += 1
        for field in ("t_count", "t_depth"):
            bucket[field] += row["forward"][field]
    same(source["typed_native_admissions"], admissions, "every typed native dispatch admission")
    same(source["forward_operation_costs"], old_operation, "forward operation-count reference")
    output_copy = W * len(target["outputs"])
    clean = {field: int(forward_totals[field] + inverse_totals[field]) for field in SCAN_FIELDS}
    clean["source_gates"] += 2 * copies + output_copy
    clean["cx"] += 2 * copies + output_copy
    clean["clifford_t_depth"] += 4 * copy_rounds + 1
    clean.update(
        {
            "clifford_cx": clean["cx"] + 6 * clean["ccx"],
            "clifford_h": 2 * clean["ccx"],
            "logical_qubits": (words + 1) * W + scratch,
            "random_hadamards": 32,
            "ssa_words": words,
            "output_words": 1,
            "max_reused_scratch_qubits": scratch,
            "t_depth_schedule": (
                "serial complete native leaves, ASAP7T per direction; all copies paid"
            ),
            "ccx_expansion": "exact7T CCX; X/CX/CCX arrays, no relative phase substitutions",
        }
    )
    same(source["resources"], clean, "complete actual forward/output/literal-inverse source cost")
    reference = {field: int(2 * forward_totals[field]) for field in SCAN_FIELDS}
    reference["source_gates"] += 2 * copies + output_copy
    reference["cx"] += 2 * copies + output_copy
    reference["clifford_t_depth"] += 4 * copy_rounds + 1
    reference.update(
        {
            name: clean[name]
            for name in (
                "logical_qubits",
                "random_hadamards",
                "ssa_words",
                "output_words",
                "max_reused_scratch_qubits",
            )
        }
    )
    reference.update(
        {
            "clifford_cx": reference["cx"] + 6 * reference["ccx"],
            "clifford_h": 2 * reference["ccx"],
            "t_depth_schedule": "serial clean leaves, ASAP inside each leaf; valid upper bound, "
            "not optimal circuit depth",
            "ccx_expansion": "exact 7 T and 6 CX, 2 H per CCX; no relative-phase substitution",
        }
    )
    same(
        source["compiler_resource_reference"], reference, "preserved compiler-reference arithmetic"
    )
    expected_ledger = {
        "native_leaves": native_rows,
        "forward_native_resources": dict(forward_totals),
        "literal_inverse_native_resources": dict(inverse_totals),
        "clean_resources": clean,
        "argument_copy_CX_forward": copies,
        "argument_copy_CX_inverse": copies,
        "named_full72_output_copy_CX": output_copy,
        "all_native_high_input_output_and_private_wires_charged": True,
        "flat_full_gate_array_materialized": False,
        "actual_scalar_component_cost_only": True,
        "financial_loader_path_or_runtime_cost_extrapolated": False,
        "initial_Hadamards_counted_separately": 32,
        "fraction_scale": S,
    }
    same(
        read(bound_path(SCALAR / (label + "_actual_cost.json"), frozen)),
        expected_ledger,
        "independently reconstructed complete saved cost ledger",
    )
    # The private bank maps native input slots and every non-output native wire.
    # Native outputs alone bind fresh SSA banks. Each invocation's mapping is
    # injective; scratch starts/ends zero under its hash-bound clean leaf ABI.
    scratch_base = (words + 1) * W
    layout = {
        "full72_SSA_bank_qubits": words * W,
        "separate_named_output72_offset": words * W,
        "private_bank_offset": scratch_base,
        "private_bank_qubits": scratch,
        "allocation_end": scratch_base + scratch,
        "input_preparation_H_separate": 32,
        "arithmetic_H": clean["clifford_h"],
        "complete_preparation_plus_arithmetic_H": 32 + clean["clifford_h"],
        "serial_per_leaf_ASAP_depth_is_a_valid_upper_bound_not_runtime": True,
    }
    require(layout["allocation_end"] == clean["logical_qubits"], "physical bank endpoint")
    return (
        source,
        expected_ledger,
        {
            "label": label,
            "clean_resources": clean,
            "bank_layout": layout,
            "native_leaf_count": len(keys),
            "forward_call_count": len(calls),
        },
    )


def integer_quantile(raw, literals):
    """Direct signed integer formula, not SSA evaluation or gate execution."""
    require(type(raw) is int and 0 <= raw < 1 << 32, "actual unsigned q32 midpoint")
    p = (2 * raw + 1) << 7
    negative = p < S // 2
    absolute, probability = abs(p - S // 2), min(p, S - p)

    def horner(coefficients, argument):
        value = coefficients[-1]
        for coefficient in coefficients[-2::-1]:
            value = (value * argument) // S + coefficient
        return value

    if probability < Fraction(3 * S, 40):
        exponent = probability.bit_length() - 1 - F
        mantissa = probability << -exponent
        index = (mantissa - S) >> (F - 5)
        local = mantissa - (S + (index << (F - 5)) + (1 << (F - 6)))
        logarithm = horner(literals["log_table"][index], local) + exponent * literals["ln2_raw"]
        argument = math.isqrt((-logarithm) << F) - literals["tail_shift_raw"]
        numerator = horner(literals["tail_A_raw"], argument)
        denominator = horner(literals["tail_B_raw"], argument)
    else:
        argument = literals["central_rconstant_raw"] - (absolute * absolute) // S
        a = horner(literals["central_A_raw"], argument)
        denominator = horner(literals["central_B_raw"], argument)
        numerator = (absolute * a) // S  # The actual separate central floor is mandatory.
    require(
        0 <= numerator < 1 << W and S <= denominator < 1 << 64,
        "archived fixture integer native operand contract",
    )
    value = (numerator << F) // denominator
    return (-value if negative else value) & MASK


def audit_replay_evidence(literals, sources, frozen):
    saved = read(bound_path(SCALAR / "actual_gate_replays.json", frozen))
    expected_points = [
        (label, word, dirty)
        for label, words in (("candidate64", WORDS), ("control72", (KCENTRAL,)))
        for word in words
        for dirty in (0, MASK)
    ]
    require(
        saved["completed_replays"] == 18 and len(saved["rows"]) == 18,
        "all sixteen candidate and two control preserved actual replays",
    )
    reconciled = []
    for row, (label, word, dirty) in zip(saved["rows"], expected_points, strict=True):
        expected = dirty ^ integer_quantile(word, literals)
        same(
            row,
            {
                "source": label,
                "q32_raw": word,
                "initial_output72": dirty,
                "expected_XOR_output72": expected,
                "observed_output72": expected,
                "all_work_and_native_scratch_clean": True,
                "full_native_input72_preserved": True,
                "allocated_state_qubits": sources[label]["resources"]["logical_qubits"],
                "actual_gate_replay": True,
                "all_input_law_completeness_inferred_from_this_fixture": False,
            },
            "preserved actual gate replay versus independent integer formula",
        )
        reconciled.append(
            {
                "source": label,
                "q32_raw": word,
                "initial_output72": dirty,
                "independent_expected_XOR_output72": expected,
            }
        )
    cases = list(ET.parse(bound_path(SCALAR / "tests.xml", frozen)).getroot().iter("testcase"))
    identities = [(item.attrib.get("classname", ""), item.attrib["name"]) for item in cases]
    require(
        len(cases) == len(set(identities)) == 27
        and not any(
            item.find(tag) is not None for item in cases for tag in ("failure", "error", "skipped")
        ),
        "27 successful original distinct fixture records, without recredit",
    )
    same(
        read(bound_path(SCALAR / "test_credit_reconciliation.json", frozen)),
        {
            "unique_new_fixtures_passed": 27,
            "prior_fixture_counts_added_again": 0,
            "test_identities": [list(item) for item in identities],
        },
        "original fixture credit evidence",
    )
    return {
        "preserved_actual_candidate_replays_checked": 16,
        "preserved_actual_control_replays_checked": 2,
        "rows": reconciled,
        "new_gate_replays_performed": 0,
        "prior27_fixtures_recredited": 0,
        "fixtures_are_not_the_all_input_semantic_or_width_proof": True,
    }


def package_inputs():
    """Bounded literal installed dependencies for the independent JIT scanner."""
    import numpy
    import numba
    import llvmlite

    roots = [Path(module.__file__).resolve().parent for module in (numpy, numba, llvmlite)]
    files = set()
    for base in roots + [roots[0].parent / "numpy.libs", roots[0].parent / "llvmlite.libs"]:
        if not base.exists():
            continue
        base.relative_to(ROOT)
        for path in base.rglob("*"):
            if (
                path.is_file()
                and "__pycache__" not in path.parts
                and path.suffix.lower() in (".py", ".pyd", ".dll", ".so")
            ):
                files.add(path)
                require(len(files) <= 12288, "bounded installed scanner dependency inventory")
    return sorted(files), {
        "numpy": numpy.__version__,
        "numba": numba.__version__,
        "llvmlite": llvmlite.__version__,
        "modules": {
            module.__name__: {
                "module_file": relative(Path(module.__file__)),
                "sha256": sha(Path(module.__file__)),
                "version": module.__version__,
            }
            for module in (numpy, numba, llvmlite)
        },
        "numba_disk_cache": False,
        "scanner_imports_producer_code": False,
    }


def verify_scanner_packages(protocol):
    import numpy
    import numba
    import llvmlite

    for module in (numpy, numba, llvmlite):
        record = protocol["scanner_packages"]["modules"][module.__name__]
        name = relative(Path(module.__file__))
        require(
            name == record["module_file"]
            and module.__version__ == record["version"]
            and protocol["frozen_inputs"].get(name)
            == record["sha256"]
            == sha(Path(module.__file__)),
            "actual scanner package module/version/frozen membership",
        )


def interpreter_binding(bind):
    launcher = Path(sys.executable).resolve()
    bind(relative(launcher), sha(launcher))
    base = Path(getattr(sys, "_base_executable", sys.executable)).resolve()
    try:
        base_name = relative(base)
    except ValueError:
        # The system Python installation is not placed into a workspace path
        # map. Only this actual runtime's base executable is read and hashed.
        base_record = {
            "absolute_path": str(base),
            "sha256": sha(base),
            "scope": "read-only actual base interpreter outside workspace",
            "included_in_workspace_frozen_map": False,
        }
    else:
        bind(base_name, sha(base))
        base_record = {
            "workspace_relative": base_name,
            "sha256": sha(base),
            "included_in_workspace_frozen_map": True,
        }
    return {
        "launcher_workspace_relative": relative(launcher),
        "launcher_sha256": sha(launcher),
        "base_interpreter": base_record,
    }


def verify_interpreter(protocol):
    record = protocol["interpreter_binding"]
    launcher = Path(sys.executable).resolve()
    require(
        relative(launcher) == record["launcher_workspace_relative"],
        "actual invoked interpreter launcher identity",
    )
    require(
        protocol["frozen_inputs"].get(relative(launcher))
        == record["launcher_sha256"]
        == sha(launcher),
        "explicit interpreter launcher frozen membership/hash",
    )
    base_record = record["base_interpreter"]
    base = Path(getattr(sys, "_base_executable", sys.executable)).resolve()
    if base_record["included_in_workspace_frozen_map"]:
        require(
            relative(base) == base_record["workspace_relative"]
            and protocol["frozen_inputs"].get(relative(base)) == base_record["sha256"],
            "explicit in-workspace base interpreter membership",
        )
    else:
        require(
            str(base) == base_record["absolute_path"],
            "explicit scoped external base interpreter identity",
        )
    require(sha(base) == base_record["sha256"], "actual base interpreter bytes")


def prepare(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM)
    require(not output.exists(), "a fresh prospective independent audit receipt")
    frozen = {}
    try:
        prepare_body(output, frozen)
    except BaseException as failure:
        if output.exists():
            if not (output / "protocol.json").exists():
                create(
                    output / "protocol.json",
                    dict(
                        local_only=True,
                        frozen_inputs=frozen,
                        terminal_partial_preparation=True,
                        new_test_credit=0,
                    ),
                )
            create(
                output / "preparation_failure.json",
                dict(
                    failure_type=type(failure).__name__,
                    message=str(failure),
                    traceback=traceback.format_exc(),
                    partial_files_preserved=True,
                    fixed_receipt_terminal_no_retry=True,
                ),
            )
            create(
                output / "summary.json",
                dict(
                    passed=False,
                    budget_censored=isinstance(failure, TimeoutError),
                    local_only=True,
                    preparation_failed=True,
                    new_test_credit=0,
                    failure_type=type(failure).__name__,
                    message=str(failure),
                    fixed_receipt_terminal_no_retry=True,
                    new_gate_replays_leaves_prices_or_financial_compiles=0,
                ),
            )
            create(
                output / "manifest.json",
                dict(
                    files={
                        relative(path): sha(path)
                        for path in sorted(output.rglob("*"))
                        if path.is_file() and path.name != "manifest.json"
                    },
                    frozen_inputs=frozen,
                    manifest_self_hash_excluded=True,
                ),
            )
        raise


def prepare_body(output, frozen):

    def bind(name, digest):
        name = name.replace("\\", "/")
        path = (ROOT / name).resolve()
        path.relative_to(ROOT)
        name = relative(path)
        require(
            isinstance(digest, str)
            and len(digest) == 64
            and all(char in "0123456789abcdef" for char in digest),
            "explicit canonical dependency SHA256",
        )
        require(
            name not in frozen or frozen[name] == digest,
            "equal aliases retain every prerequisite frozen-hash expectation",
        )
        frozen[name] = digest

    for directory in RECEIPTS:
        summary = read(directory / "summary.json")
        require(
            summary.get("passed") is True and summary.get("budget_censored", False) is False,
            "successful complete uncensored receipt: " + directory.name,
        )
        if directory == SCALAR:
            require(
                summary.get("actual_scalar_clean_XOR_source_emitted") is True,
                "actual emitted scalar source prerequisite",
            )
        if directory == DIVIDER:
            require(
                summary.get("exact_seven_T_primitive_phase_proved") is True
                and summary.get("actual_saved_gate_arrays") == 2,
                "actual phase-exact divider pair",
            )
        receipt = read(directory / "manifest.json")
        for field in ("files", "frozen_inputs"):
            for name, expected in receipt[field].items():
                bind(name, expected)
        bind(relative(directory / "manifest.json"), sha(directory / "manifest.json"))
    native_sqrt = read(SQRT)
    files, packages = package_inputs()
    for path in (
        [RESEARCH / name for name in CODE] + files + [SQRT, SQRT.parent / native_sqrt["gate_file"]]
    ):
        bind(relative(path), sha(path))
    interpreter = interpreter_binding(bind)
    verify(frozen)
    output.mkdir()
    for name in CODE:
        shutil.copy2(RESEARCH / name, output / name)
        require(
            sha(output / name) == frozen[relative(RESEARCH / name)],
            "independent scalar-audit code snapshot bytes",
        )
    create(
        output / "protocol.json",
        {
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "local_only": True,
            "before_source_parsing_recipe_reconstruction_native_scans_or_integer_reconciliation": (
                True
            ),
            "requires_all_stage_c_supervisors_descendants_and_known_pool_orphans_terminal": True,
            "frozen_inputs": frozen,
            "executed_dependencies": [
                {
                    "original": relative(RESEARCH / name),
                    "snapshot": name,
                    "sha256": frozen[relative(RESEARCH / name)],
                }
                for name in CODE
            ],
            "scanner_packages": packages,
            "interpreter_binding": interpreter,
            "independent_saved_opcode_ASAP_scanner": True,
            "producer_graph_compiler_resource_or_evaluator_imports": 0,
            "fixed_sources": ["candidate64", "control72"],
            "initial_H_separate": 32,
            "preserved_actual_candidate_replay_records": 16,
            "preserved_actual_control_replay_records": 2,
            "full72_input_output_copy_and_scratch_banks_charged": True,
            "native_inverse": (
                "Reverse existing X/CX/CCX rows; each native gate is exactly self-inverse"
            ),
            "all_input_claim_basis": (
                "independent complete recipe plus successful independent arithmetic audits"
            ),
            "new_test_credit": 0,
            "all_frozen_insertions_resolve_aliases_without_SHA_overrides": True,
            "partial_preparation_failure_is_terminal_no_retry": True,
            "explicit_scanner_package_module_membership_required": True,
            "new_leaf_generation_gate_replays_prices_or_financial_compiles": 0,
            "old_Box_Muller_cost_or_financial_law_adoption": False,
            "process_CPU_limit_seconds": CPU_LIMIT,
            "new_work_admission_CPU_seconds": ADMISSION_CPU,
            "wall_limit_seconds": WALL_LIMIT,
            "python": sys.version,
            "executable": sys.executable,
        },
    )
    verify(frozen)
    protocol = read(output / "protocol.json")
    verify_interpreter(protocol)
    verify_scanner_packages(protocol)
    print("Independent scalar native source audit prospectively frozen", flush=True)


def run(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM)
    require(not (output / "summary.json").exists(), "nonterminal fresh scalar source audit")
    protocol = read(output / "protocol.json")
    cpu_start, wall_start = time.process_time(), time.monotonic()
    checked_files = None

    def checkpoint():
        if (
            time.process_time() - cpu_start >= ADMISSION_CPU
            or time.monotonic() - wall_start >= WALL_LIMIT
        ):
            raise TimeoutError("The fixed scalar source audit admission budget was reached")

    try:
        frozen = protocol["frozen_inputs"]
        verify(frozen)
        verify_interpreter(protocol)
        verify_scanner_packages(protocol)
        target = read(bound_path(SCALAR / "scalar_target.json", frozen))
        literals = read(bound_path(SCALAR / "literals.json", frozen))
        bindings = read(bound_path(SCALAR / "semantic_bindings.json", frozen))
        proofs = read(bound_path(SCALAR / "new_site_proofs.json", frozen))
        central = read(bound_path(CENTRAL / "central_certificate.json", frozen))
        tail = read(bound_path(TAIL / "tail_certificate.json", frozen))
        native = read(bound_path(TRANSFORM / "native_transform_certificate.json", frozen))
        checkpoint()
        words = audit_recipe(target, bindings, literals, central, tail, native)
        sites = audit_site_proofs(target, bindings, literals, proofs, central, tail, native)
        audit_ccx_prior(frozen)
        create(
            output / "semantic_and_site_audit.json",
            {
                "passed": True,
                "target_sha256": fingerprint(target),
                "literal_sha256": fingerprint(literals),
                "complete_independent_recipe_and_every_binding_reconciled": True,
                "separate_central_product_floor_before_selected_division_preserved": True,
                "all_eager_unused_branch_guards_and_original_log_literals_preserved": True,
                "sites": sites,
                "independent_all_input_arithmetic_audits_required": True,
                "integer_fixtures_used_as_completeness_proof": False,
            },
        )
        checkpoint()
        np, scanner = make_scanner()
        sources, ledgers, rows = {}, {}, []
        for label in ("candidate64", "control72"):
            source, ledger, row = audit_one_source(
                label, target, proofs, bindings, words, np, scanner, frozen, checkpoint
            )
            sources[label], ledgers[label] = source, ledger
            rows.append(row)
            create(output / (label + "_cost_audit.json"), {"passed": True, **row, "ledger": ledger})
        for candidate_call, control_call in zip(
            sources["candidate64"]["forward_calls"],
            sources["control72"]["forward_calls"],
            strict=True,
        ):
            key = candidate_call["leaf"]
            if key in ledgers["control72"]["native_leaves"]:
                same(candidate_call, control_call, "same nondivide invocation in matched control")
                same(
                    ledgers["candidate64"]["native_leaves"][key],
                    ledgers["control72"]["native_leaves"][key],
                    "byte-identical matched nondivide leaves",
                )
            else:
                require(
                    candidate_call["out"] == [bindings["quotient"]]
                    and control_call["out"] == [bindings["quotient"]],
                    "sole paid divider substitution",
                )
        replay = audit_replay_evidence(literals, sources, frozen)
        create(output / "preserved_replay_audit.json", {"passed": True, **replay})
        summary = read(bound_path(SCALAR / "summary.json", frozen))
        same(
            summary["candidate_clean_resources"],
            sources["candidate64"]["resources"],
            "summary candidate costs",
        )
        same(
            summary["paid_control_clean_resources"],
            sources["control72"]["resources"],
            "summary paid control costs",
        )
        require(
            summary["candidate_actual_gate_replays"] == 16
            and summary["control_actual_gate_replays"] == 2
            and summary["initial_Hadamards_separate_from_arithmetic"] == 32
            and summary["complete_native_high_wires_copy_and_scratch_charged"] is True,
            "terminal producer source/copy/preparation/replay consistency",
        )
        for flag in (
            "old_Box_Muller_financial_source_changed",
            "full_financial_sampler_or_price_certificate_adopted",
            "financial_cost_or_physical_latency_extrapolated",
            "full_G2_or_quantum_advantage_established",
        ):
            require(summary[flag] is False, "component scope remains open: " + flag)
        require(
            summary["native_financial_path_error_bound"] is None
            and summary["new_financial_prices_or_replays"] == 0,
            "no inherited financial delivery",
        )
        verify(frozen)
        verify_interpreter(protocol)
        verify_scanner_packages(protocol)
        checked_files = {
            relative(path): sha(path) for path in sorted(output.rglob("*")) if path.is_file()
        }
        cpu, wall = time.process_time() - cpu_start, time.monotonic() - wall_start
        if cpu >= CPU_LIMIT or wall >= WALL_LIMIT:
            raise TimeoutError("The fixed scalar source audit terminal budget was exceeded")
        create(
            output / "summary.json",
            {
                "passed": True,
                "budget_censored": False,
                "local_only": True,
                "new_test_credit": 0,
                "complete_guarded_scalar_SSA_and_native_sites_independently_verified": True,
                "actual_native_forward_and_literal_reverse_arrays_independently_scanned": True,
                "all_argument_copies_full72_banks_native_scratch_and_serial_depth_paid": True,
                "initial_Hadamards_separate": 32,
                "preserved_actual_replay_records_checked": 18,
                "new_gate_replays_leaves_prices_or_financial_compiles": 0,
                "previous27_fixtures_added_again": 0,
                "sources": rows,
                "old_Box_Muller_cost_or_financial_law_adopted": False,
                "actual_full_financial_error_estimator_cost_or_physical_runtime": None,
                "full_G2_or_quantum_advantage_established": False,
                "CPU_seconds": cpu,
                "wall_seconds": wall,
            },
        )
    except BaseException as failure:
        create(
            output / "failure.json",
            {
                "failure_type": type(failure).__name__,
                "message": str(failure),
                "traceback": traceback.format_exc(),
            },
        )
        if not (output / "summary.json").exists():
            create(
                output / "summary.json",
                {
                    "passed": False,
                    "budget_censored": isinstance(failure, TimeoutError),
                    "new_test_credit": 0,
                    "message": str(failure),
                    "actual_financial_error_or_cost_adopted": False,
                },
            )
        raise
    finally:
        if checked_files is None or (output / "failure.json").exists():
            checked_files = {
                relative(path): sha(path) for path in sorted(output.rglob("*")) if path.is_file()
            }
        else:
            # All previous outputs and dependencies were hashed before the
            # terminal CPU check. Only the new small terminal summary remains.
            checked_files[relative(output / "summary.json")] = sha(output / "summary.json")
        create(
            output / "manifest.json",
            {
                "files": checked_files,
                "frozen_inputs": protocol["frozen_inputs"],
                "manifest_self_hash_excluded": True,
            },
        )
    print(
        "Independent scalar source/cost audit retained; full financial obligations stay open",
        flush=True,
    )


if __name__ == "__main__":
    for variable in (
        "OPENBLAS_NUM_THREADS",
        "MKL_NUM_THREADS",
        "OMP_NUM_THREADS",
        "NUMBA_NUM_THREADS",
    ):
        os.environ[variable] = "1"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, default=PROGRAM / "A02_quantile_scalar_audit_run001")
    args = parser.parse_args()
    (prepare if args.mode == "prepare" else run)(args.output)
