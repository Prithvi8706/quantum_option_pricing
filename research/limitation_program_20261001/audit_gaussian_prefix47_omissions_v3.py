"""Independent archived-slot and ideal symbolic omission audit; no numerics.

This module imports no Gaussian producer, numerical library or evaluator. Its
symbolic kernel checks rational polynomial and bit-character identities only.
It does not compute CDFs, conditional angles, a Walsh table or a statevector.
"""

from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
PROGRAM = ROOT / "results/limitation_program_20261001"
OUTPUT = PROGRAM / "A03_prefix47_omission_audit_run002"
PREFLIGHT = RESEARCH / "gaussian_prefix47_omission_audit_preflight_v3.json"
DOC = RESEARCH / "GAUSSIAN_PREFIX47_OMISSION_AUDIT_PREFLIGHT_V3.md"
OLD_PREFLIGHT = RESEARCH / "gaussian_prefix47_omission_audit_preflight.json"
OLD_DOC = RESEARCH / "GAUSSIAN_PREFIX47_OMISSION_AUDIT_PREFLIGHT.md"
ARCHIVE = ROOT / "results/limitation_audit_20261001/gaussian_v3"
ORIGINAL_SOURCE = ROOT / "research/limitation_audit_20261001/experiment_gaussian.py"
INTERPRETER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
FAILED_MANIFEST_SHA = "1c47fee27c640587c2a52d988112c4411a9928eb7fc4df301ddae3a2ae0d97d5"
PREFIX_FAILURE_SHA = "44bb90f7b2be50ab2c6692861f92e387b2af5673e338b224965d22735b3d16ab"
PREFIX_REVIEW_SHA = "2f96122496445a19ca6019b510bd87addcb374b8b2d12249ae84bc0a68afc852"
ORIGINAL_AUTHOR_SHA = {
    "audit_gaussian_prefix47_omissions_v2.py": (
        "4054a3807a45f3a3fac7fe8a092b42dca322f5f859dddd54e8bf757f6ef0b2c1"
    ),
    "gaussian_prefix47_omission_audit_preflight_v2.json": (
        "959eeaca8fef00857eb8eb513866d56b9fd24bb8723f38fdc953c52b199d8f4d"
    ),
    "GAUSSIAN_PREFIX47_OMISSION_AUDIT_PREFLIGHT_V2.md": (
        "8d10cabb222391516bd1564ccf4ac21690594a819c054770deb3e34961f35b09"
    ),
}
CPU, ADMISSION, WALL = 180, 150, 600
SCIENTIFIC_CPU, SCIENTIFIC_ADMISSION, SCIENTIFIC_WALL = 60, 45, 120
Q, N = 10, 1 << 10
_PATHS, _HASHES, _OBSERVED = {}, {}, {}

PROBABILITY_FUNCTION = """
def gaussian_probabilities(bits, cutoff=6):
    mp.mp.dps = 90
    size = 1 << bits
    edges = [-mp.mpf(cutoff) + mp.mpf(2 * cutoff) * i / size for i in range(size + 1)]
    cdf = [(1 + mp.erf(x / mp.sqrt(2))) / 2 for x in edges]
    mass = cdf[-1] - cdf[0]
    return np.array([float((cdf[i + 1] - cdf[i]) / mass) for i in range(size)])
"""
PREPARATION_FUNCTION = """
def prepare(probabilities):
    bits = len(probabilities).bit_length() - 1
    circuit = QuantumCircuit(bits)
    for level in range(bits):
        blocks = probabilities.reshape(1 << level, -1)
        left = blocks[:, :blocks.shape[1] // 2].sum(axis=1)
        total = blocks.sum(axis=1)
        angles = 2 * np.arccos(np.sqrt(np.clip(left / total, 0, 1)))
        target = bits - level - 1
        controls = list(range(target + 1, bits))
        beta = angles.copy()
        stride = 1
        while stride < len(beta):
            for start in range(0, len(beta), 2 * stride):
                left = beta[start:start + stride].copy()
                right = beta[start + stride:start + 2 * stride].copy()
                beta[start:start + stride] = left + right
                beta[start + stride:start + 2 * stride] = left - right
            stride *= 2
        beta /= len(beta)
        for index in range(len(beta)):
            gray = index ^ (index >> 1)
            if beta[gray] != 0:
                circuit.ry(float(beta[gray]), target)
            if controls:
                following = (index + 1) % len(beta)
                next_gray = following ^ (following >> 1)
                changed = (gray ^ next_gray).bit_length() - 1
                circuit.cx(controls[changed], target)
    return circuit
"""
RY = re.compile(r"ry\((pi/2|[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)\) q\[(\d+)\];")
CX = re.compile(r"cx q\[(\d+)\], q\[(\d+)\];")
ZERO = re.compile(r"[+-]?0+(?:\.0*)?(?:[eE][+-]?\d+)?")


class BudgetCensoredError(RuntimeError):
    """Fixed terminal CPU/wall censor, with no retry or extra work."""


class ScientificClock:
    """Original scientific clock nested inside the disclosed total clock."""

    def __init__(self, total_started):
        self.total_started = total_started
        self.started = (time.process_time(), time.monotonic())
        self.finished = None

    def elapsed(self):
        if self.finished is not None:
            return self.finished
        return time.process_time() - self.started[0], time.monotonic() - self.started[1]

    def finish(self):
        self.finished = budget(self)
        return self.finished


def require(condition, message):
    if not condition:
        raise ValueError(message)


def budget(started, admission=False):
    if isinstance(started, ScientificClock):
        budget(started.total_started, admission=admission)
        cpu, wall = started.elapsed()
        if (
            cpu >= (SCIENTIFIC_ADMISSION if admission else SCIENTIFIC_CPU)
            or wall >= SCIENTIFIC_WALL
        ):
            raise BudgetCensoredError("Original scientific 60CPU/45admission/120wall budget")
        return cpu, wall
    cpu, wall = time.process_time() - started[0], time.monotonic() - started[1]
    if cpu >= (ADMISSION if admission else CPU) or wall >= WALL:
        raise BudgetCensoredError("Disclosed total 180CPU/150admission/600wall budget")
    return cpu, wall


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def same(actual, expected, message):
    require(canonical(actual) == canonical(expected), message)


def read(path):
    # Retain every archived decimal as text; no floating-point interpretation.
    return json.loads(Path(path).read_text(encoding="utf-8"), parse_float=str)


def save(path, value, started=None):
    if started is not None:
        budget(started)
    encoded = (json.dumps(value, indent=2, allow_nan=False) + "\n").encode()
    if started is not None:
        budget(started)
    with Path(path).open("xb") as stream:
        for offset in range(0, len(encoded), 1 << 20):
            if started is not None:
                budget(started)
            stream.write(encoded[offset : offset + (1 << 20)])
            if started is not None:
                budget(started)


def resolve(path, started, fresh=False):
    budget(started)
    value = Path(path)
    require(not value.drive or value.is_absolute(), "No drive-relative path")
    lexical = str(value.absolute())
    if not fresh and lexical in _PATHS:
        return _PATHS[lexical]
    actual = value.resolve()
    actual.relative_to(ROOT)
    require(
        not fresh or lexical not in _PATHS or _PATHS[lexical] == actual,
        "Previously confined path resolution changed",
    )
    _PATHS[lexical] = actual
    _PATHS.setdefault(str(actual), actual)
    budget(started)
    return actual


def relative(path, started):
    return resolve(path, started).relative_to(ROOT).as_posix()


def sha(path, started, fresh=False):
    budget(started)
    lexical = Path(path).absolute()
    if lexical.is_relative_to(ROOT):
        actual = resolve(lexical, started, fresh=fresh)
    else:
        base = Path(getattr(sys, "_base_executable", sys.executable)).resolve(strict=True)
        actual = lexical.resolve(strict=True)
        require(
            actual == base and lexical == base,
            "Only the exact actual base interpreter may be hashed outside ROOT",
        )
        budget(started)
    stat = actual.stat()
    fingerprint = (
        stat.st_dev,
        stat.st_ino,
        stat.st_size,
        stat.st_mtime_ns,
        stat.st_ctime_ns,
        getattr(stat, "st_file_attributes", None),
        getattr(stat, "st_reparse_tag", None),
    )
    key = str(actual.absolute())
    if not fresh and key in _HASHES and _HASHES[key][0] == fingerprint:
        budget(started)
        return _HASHES[key][1]
    result = hashlib.sha256()
    with actual.open("rb") as stream:
        while block := stream.read(1 << 20):
            result.update(block)
            budget(started)
    after = actual.stat()
    require(
        fingerprint
        == (
            after.st_dev,
            after.st_ino,
            after.st_size,
            after.st_mtime_ns,
            after.st_ctime_ns,
            getattr(after, "st_file_attributes", None),
            getattr(after, "st_reparse_tag", None),
        ),
        "Input changed during hashing",
    )
    budget(started)
    value = result.hexdigest()
    require(
        key not in _OBSERVED or _OBSERVED[key] == value,
        "Previously observed actual SHA changed within this invocation",
    )
    _OBSERVED.setdefault(key, value)
    _HASHES[key] = (fingerprint, value)
    return value


def bind(frozen, path, expected, started):
    key = relative(ROOT / str(path).replace("\\", "/"), started)
    require(
        type(expected) is str
        and len(expected) == 64
        and all(ch in "0123456789abcdef" for ch in expected),
        "Canonical SHA256 expectation",
    )
    require(
        key not in frozen or frozen[key] == expected, "Conflicting canonical expected SHA: " + key
    )
    frozen[key] = expected
    budget(started)


def bound(path, frozen, started):
    key = relative(path, started)
    require(key in frozen, "Unfrozen input: " + key)
    return ROOT / key


def verify(frozen, started, fresh=False):
    for key, expected in frozen.items():
        path = resolve(ROOT / key, started, fresh=fresh)
        require(sha(path, started, fresh=fresh) == expected, "Strict frozen input mismatch: " + key)


def owned_manifest(directory, frozen, started, expected=None, full_inputs=False):
    manifest = directory / "manifest.json"
    actual = sha(manifest, started)
    require(expected is None or actual == expected, "Pinned prior manifest bytes")
    data = read(manifest)
    require(
        type(data.get("files")) is dict
        and type(data.get("frozen_inputs", {})) is dict
        and data.get("manifest_self_hash_excluded") is True,
        "Complete recognized prior manifest",
    )
    owned = {
        relative(path, started)
        for path in directory.rglob("*")
        if path.is_file() and path != manifest
    }
    recorded = set()
    for key, value in data["files"].items():
        path = resolve(ROOT / str(key).replace("\\", "/"), started)
        require(
            path.is_relative_to(resolve(directory, started)), "Owned map stays within its receipt"
        )
        recorded.add(relative(path, started))
        bind(frozen, path, value, started)
    require(recorded == owned, "Prior manifest binds every owned byte")
    if full_inputs:
        for key, value in data["frozen_inputs"].items():
            bind(frozen, key, value, started)
    bind(frozen, manifest, actual, started)
    return data


def no_numerical_or_producer_imports():
    prefixes = ("numpy", "scipy", "mpmath", "qiskit", "numba", "llvmlite")
    imported = [
        name
        for name in sys.modules
        if any(name == prefix or name.startswith(prefix + ".") for prefix in prefixes)
        or name.startswith("research.limitation_audit_20261001.")
        or (
            name.startswith("research.limitation_program_20261001.")
            and name != "research.limitation_program_20261001.audit_gaussian_prefix47_omissions_v3"
        )
    ]
    require(not imported, "No numerical or producer modules may be imported: " + repr(imported))


def interpreter(frozen, started, expected=None):
    no_numerical_or_producer_imports()
    require(
        resolve(sys.executable, started) == resolve(INTERPRETER, started), "Actual pinned launcher"
    )
    launcher_sha = sha(INTERPRETER, started)
    bind(frozen, INTERPRETER, launcher_sha, started)
    base = Path(getattr(sys, "_base_executable", sys.executable)).resolve()
    base_sha = sha(base, started)
    inside = base.is_relative_to(ROOT)
    if inside:
        bind(frozen, base, base_sha, started)
    record = dict(
        launcher=relative(INTERPRETER, started),
        launcher_sha256=launcher_sha,
        actual_python_version=sys.version,
        base_interpreter=dict(
            absolute_path=str(base), sha256=base_sha, included_in_ROOT_frozen_map=inside
        ),
        numerical_dependencies=0,
        numerical_or_producer_modules_imported=0,
    )
    if expected is not None:
        same(record, expected, "Actual interpreter/base provenance unchanged")
    return record


def source_conventions(frozen, started):
    source = bound(ORIGINAL_SOURCE, frozen, started)
    module = ast.parse(source.read_text(encoding="utf-8"))
    functions = {node.name: node for node in module.body if isinstance(node, ast.FunctionDef)}
    bindings = []
    for name, template in (
        ("gaussian_probabilities", PROBABILITY_FUNCTION),
        ("prepare", PREPARATION_FUNCTION),
    ):
        budget(started)
        require(name in functions, "Actual source convention function exists")
        actual = ast.dump(functions[name], include_attributes=False)
        expected = ast.dump(ast.parse(template).body[0], include_attributes=False)
        require(
            actual == expected,
            "Actual archived function differs from the checked source convention",
        )
        bindings.append(
            dict(function=name, exact_AST_sha256=hashlib.sha256(actual.encode()).hexdigest())
        )
    run = functions["run"]
    assignments = [node for node in run.body if isinstance(node, ast.Assign)]
    require(
        any(
            ast.dump(node, include_attributes=False)
            == ast.dump(ast.parse("cutoff, rows = 6, []").body[0], include_attributes=False)
            for node in assignments
        ),
        "Actual source run uses cutoff6",
    )
    loops = [node for node in run.body if isinstance(node, ast.For)]
    require(
        len(loops) == 1
        and ast.dump(loops[0].iter, include_attributes=False)
        == ast.dump(ast.parse("(4, 6, 8, 10)", mode="eval").body, include_attributes=False),
        "Actual archived run includes q10",
    )
    expected_call = ast.dump(
        ast.parse("probabilities = gaussian_probabilities(bits, cutoff)").body[0],
        include_attributes=False,
    )
    require(
        any(ast.dump(node, include_attributes=False) == expected_call for node in loops[0].body),
        "Actual archived run binds intended Gaussian law before binary64 conversion",
    )
    metadata = read(bound(ARCHIVE / "gaussian_10.json", frozen, started))
    require(
        metadata["bits"] == Q
        and metadata["cutoff"] == 6
        and metadata["operations"] == {"cx": 1022, "ry": 976}
        and metadata["rotation_synthesis_t_count"] is None,
        "Original q10 archive scope unchanged",
    )
    require(
        read(bound(ARCHIVE / "summary.json", frozen, started))["passed"] is True,
        "Original archive numerical observation retained without extending its proof scope",
    )
    convention = read(
        bound(PROGRAM / "A03_prefix_run001/archive_convention_binding.json", frozen, started)
    )
    require(
        convention["q9_control_bit_is_MSB"] is True
        and convention["q8_child_bit_is_next"] is True
        and convention["original_angle_convention"] == "theta=2*acos(sqrt(left conditional mass))",
        "Prior narrow source/provenance convention agrees",
    )
    counts = read(bound(PROGRAM / "A03_prefix_run001/full_tree_and_budget.json", frozen, started))[
        "counts"
    ]
    require(
        counts["full_tree_conditional_nodes"] == 1023
        and counts["remaining_conditional_nodes_without_angle_certificates"] == 1020
        and counts["omitted_float_Walsh_values_proved_zero"] is False,
        "All remaining source angle and literal gaps retained",
    )
    return dict(
        function_AST_bindings=bindings,
        exact_bin_law_only=True,
        original_90_digit_to_binary64_conversion_present=True,
        binary64_target_reflection_certified=False,
        numerical_functions_evaluated=0,
    )


def archived_slots(frozen, plan, started):
    text = bound(ARCHIVE / "gaussian_10.qasm", frozen, started).read_text(encoding="utf-8")
    lines = text.splitlines()
    require(
        lines[:3] == ["OPENQASM 3.0;", 'include "stdgates.inc";', "qubit[10] q;"],
        "Exact archived QASM declaration, scalar10 lane",
    )
    operations = []
    for number, literal in enumerate(lines[3:], 4):
        budget(started)
        if not literal.strip():
            continue
        ry, cx = RY.fullmatch(literal.strip()), CX.fullmatch(literal.strip())
        require((ry is None) != (cx is None), "Only complete archived RY/CX operation grammar")
        if ry:
            target = int(ry[2])
            require(0 <= target < Q, "Archived RY wire scope")
            operations.append(dict(line=number, op="ry", target=target, literal=ry[1]))
        else:
            control, target = int(cx[1]), int(cx[2])
            require(0 <= target < control < Q, "Archived scalar CX wire scope")
            operations.append(dict(line=number, op="cx", control=control, target=target))
    require(
        len(operations) == 1998
        and sum(row["op"] == "ry" for row in operations) == 976
        and sum(row["op"] == "cx" for row in operations) == 1022,
        "All actual archived operation rows",
    )
    same(
        operations[0],
        dict(line=4, op="ry", target=9, literal="pi/2"),
        "Archived root exact half-pi RY",
    )
    cursor, slots, omissions, zeros = 1, [], [], []
    for level in range(1, Q):
        size, target = 1 << level, Q - level - 1
        for index in range(size):
            budget(started)
            mask = index ^ (index >> 1)
            present = operations[cursor]["op"] == "ry" if cursor < len(operations) else False
            rotation = operations[cursor] if present else None
            if present:
                require(
                    rotation["target"] == target,
                    "Actual rotation belongs to its unique source slot",
                )
                cursor += 1
            require(cursor < len(operations), "Every non-root source slot retains its following CX")
            following = (index + 1) % size
            difference = mask ^ (following ^ (following >> 1))
            require(
                difference > 0 and difference & (difference - 1) == 0,
                "Cyclic Gray transition changes one bit",
            )
            control = target + difference.bit_length()
            row = operations[cursor]
            require(
                row["op"] == "cx" and row["target"] == target and row["control"] == control,
                "Complete actual1022 cyclic Gray controls, targets and chronology",
            )
            record = dict(
                level=level,
                target_qubit=target,
                gray_sequence_index=index,
                Walsh_mask=mask,
                mask_Hamming_weight=mask.bit_count(),
                following_CX_QASM_line=row["line"],
                following_CX_control=control,
                following_CX_target=target,
            )
            slots.append(
                dict(
                    **record,
                    RY_present=present,
                    RY_QASM_line=rotation["line"] if present else None,
                    RY_literal=rotation["literal"] if present else None,
                )
            )
            if not present:
                omissions.append(record)
            elif ZERO.fullmatch(rotation["literal"]):
                zeros.append(
                    dict(**record, RY_QASM_line=rotation["line"], RY_literal=rotation["literal"])
                )
            cursor += 1
    require(
        cursor == len(operations) and len(slots) == 1022 and len(omissions) == 47,
        "All potential1023 RY slots accounted for, exactly47 absences",
    )
    same(
        omissions,
        plan["archived_readonly_inventory"]["omission_slots"],
        "Independent actual omissions match every pinned author inventory row",
    )
    require(
        len(zeros) == 740
        and sum(row["mask_Hamming_weight"] % 2 == 0 for row in zeros) == 455
        and sum(row["mask_Hamming_weight"] % 2 == 1 for row in zeros) == 285,
        "Separate740 emitted literalzero rows,455even and285odd",
    )
    return operations, slots, omissions, zeros


def polynomial_add(*values):
    result = {}
    for value in values:
        for monomial, coefficient in value.items():
            result[monomial] = result.get(monomial, Fraction(0)) + coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def polynomial_scale(value, coefficient):
    return {monomial: term * coefficient for monomial, term in value.items() if term * coefficient}


def polynomial_multiply(left, right):
    result = {}
    for left_variables, left_coefficient in left.items():
        for right_variables, right_coefficient in right.items():
            monomial = tuple(sorted(left_variables + right_variables))
            result[monomial] = (
                result.get(monomial, Fraction(0)) + left_coefficient * right_coefficient
            )
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def rational(value):
    value = Fraction(value)
    return [value.numerator, value.denominator]


def polynomial_record(value):
    return [
        dict(monomial=list(monomial), coefficient=rational(coefficient))
        for monomial, coefficient in sorted(value.items())
    ]


def ideal_symbolic_certificate(omissions, source, started):
    """Algebraic proof obligations, no evaluated density, angle or Walsh array."""
    one, x, j = {(): Fraction(1)}, {("x",): Fraction(1)}, {("j",): Fraction(1)}
    density_exponent = polynomial_scale(polynomial_multiply(x, x), Fraction(-1, 2))
    reflected_exponent = polynomial_scale(
        polynomial_multiply(polynomial_scale(x, -1), polynomial_scale(x, -1)), Fraction(-1, 2)
    )
    require(density_exponent == reflected_exponent, "Exact Gaussian exponent invariant under x->-x")
    edge = polynomial_add(polynomial_scale(one, -6), polynomial_scale(j, Fraction(12, N)))
    reflected_index = polynomial_add(polynomial_scale(one, N), polynomial_scale(j, -1))
    reflected_edge = polynomial_add(
        polynomial_scale(one, -6), polynomial_scale(reflected_index, Fraction(12, N))
    )
    require(reflected_edge == polynomial_scale(edge, -1), "Exact rational e_(1024-j)=-e_j")
    prefix_proofs = []
    for level in range(Q):
        budget(started)
        size, block = 1 << level, N // (1 << level)
        a = polynomial_scale(j, block)
        middle = polynomial_add(a, polynomial_scale(one, Fraction(block, 2)))
        end = polynomial_add(a, polynomial_scale(one, block))
        complement = polynomial_add(polynomial_scale(one, size - 1), polynomial_scale(j, -1))
        ca = polynomial_scale(complement, block)
        cm = polynomial_add(ca, polynomial_scale(one, Fraction(block, 2)))
        ce = polynomial_add(ca, polynomial_scale(one, block))
        require(
            ca == polynomial_add(polynomial_scale(one, N), polynomial_scale(end, -1))
            and cm == polynomial_add(polynomial_scale(one, N), polynomial_scale(middle, -1))
            and ce == polynomial_add(polynomial_scale(one, N), polynomial_scale(a, -1)),
            "Complemented contiguous prefix swaps reflected left/right intervals",
        )
        require(
            block >= 2 and block % 2 == 0, "Every checked ideal child has positive interval width"
        )
        prefix_proofs.append(
            dict(
                level=level,
                prefixes=size,
                bins_per_prefix=block,
                original_left_bin_endpoints=[polynomial_record(a), polynomial_record(middle)],
                original_right_bin_endpoints=[polynomial_record(middle), polynomial_record(end)],
                reflected_left_bin_endpoints=[polynomial_record(ca), polynomial_record(cm)],
                reflected_right_bin_endpoints=[polynomial_record(cm), polynomial_record(ce)],
            )
        )
    left, right = {("L",): Fraction(1)}, {("R",): Fraction(1)}
    total = polynomial_add(left, right)
    require(
        polynomial_add(total, polynomial_scale(left, -1)) == right,
        "Reflected conditional ratio R/(L+R)=1-L/(L+R)",
    )
    r = {("r",): Fraction(1)}
    require(
        polynomial_add(r, polynomial_add(one, polynomial_scale(r, -1))) == one,
        "Exact principal sine/cosine squared complement identity",
    )
    # A small induction kernel for the ordinary binary Walsh butterfly:
    # a new upper mask bit selects sum versus difference; a new input bit
    # selects left versus right. No Walsh values/table are evaluated.
    butterfly = []
    for upper_mask in (0, 1):
        for upper_input in (0, 1):
            source_coefficient = -1 if upper_mask and upper_input else 1
            character_factor = (-1) ** (upper_mask * upper_input)
            require(
                source_coefficient == character_factor,
                "Butterfly coefficient equals added bit character",
            )
            butterfly.append(
                dict(
                    new_mask_bit=upper_mask,
                    new_input_bit=upper_input,
                    sum_or_difference_coefficient=source_coefficient,
                    character_factor=character_factor,
                )
            )
    theta, pi, chi = {("theta",): Fraction(1)}, {("pi",): Fraction(1)}, {("chi",): Fraction(1)}
    reflected_theta = polynomial_add(pi, polynomial_scale(theta, -1))
    paired = polynomial_add(
        polynomial_multiply(theta, chi), polynomial_multiply(reflected_theta, chi)
    )
    require(
        paired == polynomial_multiply(pi, chi),
        "Even-character paired angles reduce exactly to pi*chi",
    )
    require(
        polynomial_add(one, polynomial_scale(one, -1)) == {},
        "Nontrivial character toggle pair cancels exactly",
    )
    witnesses = []
    for row in omissions:
        budget(started)
        level, mask = row["level"], row["Walsh_mask"]
        require(
            1 <= level < Q and 0 < mask < 1 << level and mask.bit_count() % 2 == 0,
            "Every actual absent slot is a nonzero even character",
        )
        witness = (mask & -mask).bit_length() - 1
        require(
            0 <= witness < level and ((mask >> witness) & 1) == 1,
            "Nonzero mask gives a no-fixed-point toggle involution",
        )
        # A parity character is represented by its coefficient bitmask and
        # constant term. Complement replaces b_k by 1-b_k, while a toggle
        # replaces only its witness bit by 1-b_k. These identities hold for
        # every formal input bit assignment, without enumerating assignments.
        complemented_character = (mask, mask.bit_count() % 2)
        toggled_character = (mask, (mask >> witness) & 1)
        require(
            complemented_character == (mask, 0) and toggled_character == (mask, 1),
            "Complement preserves even character; selected toggle negates it",
        )
        witnesses.append(
            dict(
                **row,
                cancellation_toggle_bit=witness,
                complemented_character=[mask, 0],
                toggled_character=[mask, 1],
                exact_ideal_beta_zero=True,
                actual_binary64_or_QASM_accuracy_proved=False,
            )
        )
    return dict(
        schema="ideal-Gaussian47-symbolic-obligations-v1",
        source_binding=source,
        analytic_premises=[
            "Standard erf CDF derivative is exp(-x*x/2)/sqrt(2*pi), "
            "the positive standard Gaussian density.",
            "Even integrable density gives I(a,b)=I(-b,-a) "
            "by orientation-preserving change of variable.",
            "Positive density and positive interval width give L>0,R>0 "
            "and a common positive normalizer.",
            "For r in(0,1), principal acos(sqrt(r)) is in(0,pi/2); sin is positive there.",
            "sin^2(alpha)+cos^2(alpha)=1 and cos(pi/2-alpha)=sin(alpha); principal acos is unique.",
            "A finite bijection preserves a symbolic sum; "
            "a no-fixed-point sign-negating involution cancels it.",
        ],
        density_exponent=polynomial_record(density_exponent),
        reflected_density_exponent=polynomial_record(reflected_exponent),
        edge_polynomial=polynomial_record(edge),
        reflected_edge_polynomial=polynomial_record(reflected_edge),
        normalized_bin_identity=(
            "p_j=p_(1023-j): reflected intervals, even density, identical positive denominator"
        ),
        prefix_interval_obligations=prefix_proofs,
        conditional_ratio_obligation=dict(
            total=polynomial_record(total), total_minus_left=polynomial_record(right)
        ),
        angle_complement_derivation=[
            "Set alpha=acos(sqrt(r)); cos(alpha)=sqrt(r) and sin(alpha)=sqrt(1-r).",
            "The reflected ratio is1-r, and acos(sqrt(1-r))=pi/2-alpha by the principal range.",
            "Therefore theta_jbar=pi-theta_j; at root theta_0=pi/2. Ideal clipping is inactive.",
        ],
        butterfly_induction=dict(
            base_coefficient=1,
            next_bit_kernel=butterfly,
            low_and_high_bit_intersections_disjoint=True,
            induction=(
                "chi_(h+2^k*a)(j+2^k*b)=chi_h(j)*(-1)^(a*b); "
                "stride-doubling source matches this kernel"
            ),
            final_normalization="1/2^level from the source division by len(beta)",
        ),
        even_character_paired_polynomial=polynomial_record(paired),
        cancellation_derivation=[
            "Complement jbar=2^level-1-j is a bijection; even mask implies chi_h(jbar)=chi_h(j).",
            "Let A=sum_j theta_j*chi_h(j). "
            "Then2*A=sum_j(theta_j+theta_jbar)*chi_h(j)=pi*sum_j chi_h(j).",
            "For h!=0 choose a set bit k; "
            "j->j xor2^k is a no-fixed-point involution and negates chi_h.",
            "Thus sum_j chi_h(j)=0 and beta_h=A/2^level=0. No odd-mask zero follows.",
        ],
        actual_absent_slot_witnesses=witnesses,
        exact_ideal_absence_applicability_count=47,
        CDF_conditional_angle_Walsh_table_or_statevector_evaluations=0,
        binary64_target_reflection_certified=False,
        literal_zero740_accuracy_certified=False,
        complete_loader_accuracy_certified=False,
        financial_law_adopted=False,
    )


def final_verify(frozen, started):
    budget(started)
    # Recheck every original lexical alias and every observed actual file.
    # Expected hashes remain separate premises and never enter the actual cache.
    observed = dict(_OBSERVED)
    aliases = tuple(_PATHS.items())
    for lexical, previous in aliases:
        require(
            resolve(lexical, started, fresh=True) == previous,
            "Previously confined lexical alias redirected before terminal verification",
        )
    fresh_paths, requirements = {}, {}
    base = Path(getattr(sys, "_base_executable", sys.executable)).resolve(strict=True)
    budget(started)

    def fresh_path(path):
        budget(started)
        lexical = str(Path(path).absolute())
        if lexical not in fresh_paths:
            value = Path(path)
            if value.is_relative_to(ROOT):
                actual = resolve(value, started, fresh=True)
            else:
                actual = value.resolve(strict=True)
                require(
                    actual == base and value.absolute() == base,
                    "Only the exact actual base interpreter may be external",
                )
            fresh_paths[lexical] = actual
        return fresh_paths[lexical]

    for key, expected in frozen.items():
        actual = fresh_path(ROOT / key)
        requirements.setdefault(actual, []).append(expected)
    for key, actual_sha in observed.items():
        actual = fresh_path(Path(key))
        requirements.setdefault(actual, []).append(actual_sha)
    for actual, expected_values in requirements.items():
        digest = sha(actual, started, fresh=True)
        require(
            all(digest == expected for expected in expected_values),
            "Fresh complete input hash differs from original premise or observed bytes",
        )
    no_numerical_or_producer_imports()
    return dict(
        freshly_hashed_frozen_or_actual_observed_paths=len(requirements),
        external_actual_base_interpreter_freshly_hashed=base in requirements,
        original_lexical_aliases_freshly_resolved=len(aliases),
    )


def seal(output, frozen, summary, started):
    summary.update(final_verify(frozen, started))
    save(output / "summary.json", summary, started)
    files = {
        relative(path, started): sha(path, started, fresh=True)
        for path in sorted(output.rglob("*"))
        if path.is_file()
    }
    verify(frozen, started)
    cpu, wall = budget(started)
    save(
        output / "manifest.json",
        dict(
            files=files,
            frozen_inputs=frozen,
            terminal_record=relative(output / "summary.json", started),
            manifest_self_hash_excluded=True,
            all_unique_inputs_fresh_resolved_and_fully_hashed_before_terminal=True,
            process_CPU_seconds_before_terminal=cpu,
            wall_seconds_before_terminal=wall,
            process_CPU_limit_seconds=CPU,
            admission_CPU_limit_seconds=ADMISSION,
            wall_limit_seconds=WALL,
            original_scientific_CPU_admission_wall_seconds=[
                SCIENTIFIC_CPU,
                SCIENTIFIC_ADMISSION,
                SCIENTIFIC_WALL,
            ],
            disclosed_total_bookkeeping_budget_expansion=True,
        ),
        started,
    )


def preserve_failure(output, frozen, exception, phase, started, scientific=None):
    if not output.exists():
        return
    try:
        budget(started)
        save(
            output / (phase + "_failure.json"),
            dict(
                type=type(exception).__name__,
                message=str(exception),
                traceback=traceback.format_exc(),
                no_retry=True,
            ),
            started,
        )
        terminal = output / (
            "completion_outcome.json" if (output / "summary.json").exists() else "summary.json"
        )
        save(
            terminal,
            dict(
                passed=False,
                budget_censored=isinstance(exception, (BudgetCensoredError, TimeoutError)),
                new_test_credit=0,
                financial_law_adopted=False,
                failed_prefix47_run001_credit=0,
                source_AST_slot_symbolic_work_started=scientific is not None,
                scientific_CPU_wall_seconds_observed=(
                    list(scientific.elapsed()) if scientific is not None else None
                ),
                total_CPU_wall_seconds_before_retention_verification=[
                    time.process_time() - started[0],
                    time.monotonic() - started[1],
                ],
                total_CPU_admission_wall_seconds=[CPU, ADMISSION, WALL],
                original_scientific_CPU_admission_wall_seconds=[
                    SCIENTIFIC_CPU,
                    SCIENTIFIC_ADMISSION,
                    SCIENTIFIC_WALL,
                ],
                disclosed_total_bookkeeping_budget_expansion=True,
                no_retry=True,
            ),
            started,
        )
        require(
            not (output / "manifest.json").exists(), "Never replace an existing or partial manifest"
        )
        verification_error = None
        try:
            final_verify(frozen, started)
        except BudgetCensoredError:
            raise
        except BaseException as changed:
            verification_error = str(changed)
        files = {
            relative(path, started): sha(path, started, fresh=True)
            for path in sorted(output.rglob("*"))
            if path.is_file()
        }
        save(
            output / "manifest.json",
            dict(
                files=files,
                frozen_inputs=frozen,
                terminal_record=relative(terminal, started),
                manifest_self_hash_excluded=True,
                failure_input_verification_error=verification_error,
                failed_fixture_credit=0,
                process_CPU_seconds_before_terminal=time.process_time() - started[0],
                wall_seconds_before_terminal=time.monotonic() - started[1],
                total_CPU_admission_wall_seconds=[CPU, ADMISSION, WALL],
                original_scientific_CPU_admission_wall_seconds=[
                    SCIENTIFIC_CPU,
                    SCIENTIFIC_ADMISSION,
                    SCIENTIFIC_WALL,
                ],
                disclosed_total_bookkeeping_budget_expansion=True,
            ),
            started,
        )
    except BaseException as retention:
        marker = output / "failed_unsealed.json"
        if not marker.exists():
            save(
                marker,
                dict(
                    passed=False,
                    new_test_credit=0,
                    receipt_unsealed=True,
                    original_error=str(exception)[:1024],
                    retention_error=str(retention)[:1024],
                    budget_censored=isinstance(exception, (BudgetCensoredError, TimeoutError))
                    or isinstance(retention, BudgetCensoredError),
                    overrides_any_intermediate_success=True,
                    no_further_hashing_verification_or_retry=True,
                    total_CPU_wall_seconds_observed=[
                        time.process_time() - started[0],
                        time.monotonic() - started[1],
                    ],
                    scientific_CPU_wall_seconds_observed=(
                        list(scientific.elapsed()) if scientific is not None else None
                    ),
                    total_CPU_admission_wall_seconds=[CPU, ADMISSION, WALL],
                    original_scientific_CPU_admission_wall_seconds=[
                        SCIENTIFIC_CPU,
                        SCIENTIFIC_ADMISSION,
                        SCIENTIFIC_WALL,
                    ],
                    disclosed_total_bookkeeping_budget_expansion=True,
                ),
            )


def original_prefix_failure(frozen, plan, started):
    require(
        not (PROGRAM / "A03_prefix47_omission_audit_run001").exists(),
        "Original intended prefix receipt is absent; no fabricated protocol or retry",
    )
    same(plan["original_author_sha256"], ORIGINAL_AUTHOR_SHA, "Executed v2 author pins unchanged")
    require(
        plan["original_admission_failure_manifest_sha256"] == PREFIX_FAILURE_SHA
        and plan["original_root_review_manifest_sha256"] == PREFIX_REVIEW_SHA,
        "Pinned complete v2 failure and review prerequisites",
    )
    for name, expected in ORIGINAL_AUTHOR_SHA.items():
        bind(frozen, RESEARCH / name, expected, started)
    diagnostic = PROGRAM / "A03_prefix47_admission_failure_run001"
    previous = owned_manifest(diagnostic, frozen, started, PREFIX_FAILURE_SHA, full_inputs=True)
    require(
        len(previous["files"]) == 5 and len(previous["frozen_inputs"]) == 5,
        "Complete failed prefix diagnostic 5 owned plus 5 frozen references",
    )
    observed = read(diagnostic / "summary.json")
    require(
        observed["passed"] is False
        and observed["actual_prepare_invoked"] is True
        and observed["actual_exit_code"] == 1
        and observed["failed_intended_receipt_absent"] is True
        and observed["failed_intended_receipt"] == "A03_prefix47_omission_audit_run001"
        and observed["source_AST_slot_symbolic_or_numerical_work_executed"] is False
        and observed["new_test_credit"] == 0
        and observed["original_author_bytes_preserved"] is True
        and observed["ideal_47_omission_claim_not_executed"] is True
        and observed["exact_final_CPU_seconds"] is None,
        "Failed preparation retained honestly at zero scientific and fixture credit",
    )
    same(
        observed["actual_fixed_CPU_admission_wall_seconds"],
        [SCIENTIFIC_CPU, SCIENTIFIC_ADMISSION, SCIENTIFIC_WALL],
        "Original overall v2 limit was 60/45/120, now explicitly expanded for bookkeeping",
    )
    review = PROGRAM / "A03_prefix47_root_review_run001"
    reviewed = owned_manifest(review, frozen, started, PREFIX_REVIEW_SHA, full_inputs=True)
    require(
        len(reviewed["files"]) == 1 and len(reviewed["frozen_inputs"]) == 3,
        "Complete original root static-review maps",
    )
    report = read(review / "summary.json")
    require(
        report["static_root_and_guard_peer_review_passed"] is True
        and report["pure_symbolic_and_archive_slot_scope"] is True
        and report["no_numeric_or_slot_execution_claim_from_review"] is True
        and report["new_pytest_credit"] == 0,
        "Original review is author-stage evidence only",
    )
    same(report["source_sha256"], ORIGINAL_AUTHOR_SHA, "Review pins exact original v2 files")
    budget(started)


def prepare(output):
    started, frozen = (time.process_time(), time.monotonic()), {}
    _PATHS.clear()
    _HASHES.clear()
    _OBSERVED.clear()
    require(sys.dont_write_bytecode is True, "Invoke interpreter with -B before -m")
    output = resolve(output, started)
    require(
        output == resolve(OUTPUT, started) and not output.exists(),
        "Fresh exact omission audit receipt",
    )
    try:
        plan = read(PREFLIGHT)
        require(
            plan["future_independent_audit"]["process_CPU_seconds"] == CPU
            and plan["future_independent_audit"]["work_admission_CPU_seconds"] == ADMISSION
            and plan["future_independent_audit"]["wall_seconds"] == WALL
            and plan["future_independent_audit"]["new_pytest_credit"] == 0,
            "Disclosed total 180/150/600 bookkeeping limit and zero credit",
        )
        same(
            plan["future_independent_audit"]["separate_scientific_CPU_admission_wall_seconds"],
            [SCIENTIFIC_CPU, SCIENTIFIC_ADMISSION, SCIENTIFIC_WALL],
            "Original scientific 60/45/120 scope is separately enforced",
        )
        require(
            plan["future_independent_audit"]["disclosed_total_bookkeeping_budget_expansion"]
            is True,
            "Bookkeeping expansion is explicit, not an unchanged overall-budget claim",
        )
        original_prefix_failure(frozen, plan, started)
        for row in plan["author_readonly_input_bindings"]:
            bind(frozen, row["path"], row["author_readonly_sha256"], started)
        require(
            len(plan["author_readonly_input_bindings"]) == 8,
            "Exactly the original8 pinned archive/provenance inputs",
        )
        old = read(OLD_PREFLIGHT)
        same(
            plan["author_readonly_input_bindings"],
            old["author_readonly_input_bindings"],
            "Original8 expected hashes unchanged",
        )
        same(
            plan["archived_readonly_inventory"],
            old["archived_readonly_inventory"],
            "Original47 candidate inventory unchanged",
        )
        failed = owned_manifest(
            PROGRAM / "WAVE10_run001", frozen, started, FAILED_MANIFEST_SHA, full_inputs=True
        )
        require(
            len(failed["files"]) == 13 and len(failed["frozen_inputs"]) == 14987,
            "Complete original failed finalizer maps preserved",
        )
        failed_summary = read(PROGRAM / "WAVE10_run001/summary.json")
        require(
            failed_summary["passed"] is False
            and failed_summary["budget_censored"] is True
            and failed_summary["new_test_credit"] == 0,
            "Original failed cumulative packet credits zero",
        )
        owned_manifest(PROGRAM / "WAVE10_run002", frozen, started)
        wave = read(PROGRAM / "WAVE10_run002/summary.json")
        require(
            wave["passed"] is True
            and wave["archived_or_current_integrity_passed"] is True
            and wave["global_live_integrity"] is False
            and wave["live_mismatch_references"] == 36
            and wave["distinct_live_mismatch_paths"] == 9
            and wave["legitimate_expected_hashes_waived"] is False
            and wave["fixed18_fixture_packet_credit"] == 252,
            "Completed W10run002/252 fixtures; original36/9 mismatch ledger retained",
        )
        same(
            read(PROGRAM / "WAVE10_run002/progress_snapshot.json")["static_author_preflights"][
                "dependency_order"
            ],
            plan["execution_release"]["fixed18_selected_labels"],
            "Immutable selected005 fixed18 snapshot",
        )
        for path in (PREFLIGHT, DOC, OLD_PREFLIGHT, OLD_DOC, Path(__file__).resolve()):
            bind(frozen, path, sha(path, started), started)
        own_cache = getattr(sys.modules[__name__], "__cached__", None)
        if own_cache and Path(own_cache).is_file():
            bind(frozen, own_cache, sha(own_cache, started), started)
        actual_interpreter = interpreter(frozen, started)
        verify(frozen, started)
        budget(started, admission=True)
        output.mkdir()
        for path in (Path(__file__).resolve(), PREFLIGHT, DOC):
            budget(started)
            copied = output / path.name
            shutil.copy2(path, copied)
            require(
                sha(copied, started) == frozen[relative(path, started)],
                "Immutable copied author/preflight bytes",
            )
            bind(frozen, copied, frozen[relative(path, started)], started)
        verify(frozen, started)
        final_verification = final_verify(frozen, started)
        budget(started, admission=True)
        save(
            output / "protocol.json",
            dict(
                schema="Gaussian47-independent-symbolic-audit-protocol-v3",
                created_utc=datetime.now(timezone.utc).isoformat(),
                local_only=True,
                frozen_inputs=frozen,
                actual_interpreter=actual_interpreter,
                frozen_before_slot_or_symbolic_work=True,
                process_CPU_seconds=CPU,
                admission_CPU_seconds=ADMISSION,
                wall_seconds=WALL,
                original_scientific_CPU_admission_wall_seconds=[
                    SCIENTIFIC_CPU,
                    SCIENTIFIC_ADMISSION,
                    SCIENTIFIC_WALL,
                ],
                disclosed_total_bookkeeping_budget_expansion=True,
                scientific_clock_starts_only_after_initial_full_verification=True,
                source_AST_slot_symbolic_work_executed=False,
                preparation_final_fresh_verification=final_verification,
                new_test_credit=0,
                failed_WAVE10_run001_credit=0,
                failed_prefix47_run001_credit=0,
                numerical_threads=1,
                JIT_disk_cache=False,
                numerical_or_producer_imports=0,
                bytecode_writes_disabled=True,
                lexical_confined_path_cache_invocation_local=True,
                SHA_cache_observed_actual_bytes_only_stat_guarded=True,
                terminal_unique_input_verification_cache_bypassing=True,
            ),
            started,
        )
    except BaseException as exception:
        preserve_failure(output, frozen, exception, "prepare", started)
        raise


def run(output):
    started = (time.process_time(), time.monotonic())
    scientific, frozen = None, {}
    _PATHS.clear()
    _HASHES.clear()
    _OBSERVED.clear()
    require(sys.dont_write_bytecode is True, "Invoke interpreter with -B before -m")
    output = resolve(output, started)
    require(output == resolve(OUTPUT, started) and output.is_dir(), "Exact prepared audit receipt")
    require(
        not any(
            (output / name).exists()
            for name in (
                "summary.json",
                "run_started.json",
                "prepare_failure.json",
                "run_failure.json",
                "manifest.json",
                "failed_unsealed.json",
            )
        ),
        "No partial or terminal retry",
    )
    try:
        protocol = read(output / "protocol.json")
        frozen = protocol["frozen_inputs"]
        verify(frozen, started)
        interpreter(frozen, started, expected=protocol["actual_interpreter"])
        require(
            protocol["frozen_before_slot_or_symbolic_work"] is True
            and protocol["new_test_credit"] == 0
            and protocol["failed_WAVE10_run001_credit"] == 0
            and protocol["failed_prefix47_run001_credit"] == 0
            and protocol["process_CPU_seconds"] == CPU
            and protocol["admission_CPU_seconds"] == ADMISSION
            and protocol["wall_seconds"] == WALL
            and protocol["disclosed_total_bookkeeping_budget_expansion"] is True
            and protocol["source_AST_slot_symbolic_work_executed"] is False,
            "Own frozen no-credit symbolic protocol",
        )
        same(
            protocol["original_scientific_CPU_admission_wall_seconds"],
            [SCIENTIFIC_CPU, SCIENTIFIC_ADMISSION, SCIENTIFIC_WALL],
            "Own original scientific budget retained separately",
        )
        save(
            output / "run_started.json",
            dict(no_retry=True, slot_and_symbolic_scope_only=True),
            started,
        )
        budget(started, admission=True)
        scientific = ScientificClock(started)
        budget(scientific, admission=True)
        source = source_conventions(frozen, scientific)
        budget(scientific, admission=True)
        operations, slots, omissions, zeros = archived_slots(
            frozen, read(bound(PREFLIGHT, frozen, scientific)), scientific
        )
        budget(scientific, admission=True)
        certificate = ideal_symbolic_certificate(omissions, source, scientific)
        save(
            output / "archived_operation_and_slot_inventory.json",
            dict(
                operation_rows=operations,
                nonroot_slot_rows=slots,
                root_RY_line=4,
                actual_operations=1998,
                actual_CX_slots=1022,
                actual_emitted_RY=976,
                potential_RY=1023,
            ),
            scientific,
        )
        save(
            output / "omission47_inventory.json",
            dict(
                rows=omissions,
                actual_absent_RY_slots=47,
                inferred_only_from_absence_before_the_following_retained_source_CX=True,
            ),
            scientific,
        )
        save(
            output / "serialized_zero740_inventory.json",
            dict(
                rows=zeros,
                actual_emitted_literalzero_rows=740,
                even_weight_mask_rows=455,
                odd_weight_mask_rows=285,
                accuracy_of_literal_or_binary64_target_certified=False,
                these_rows_are_not_the47_absences=True,
            ),
            scientific,
        )
        save(output / "ideal_omission_symbolic_certificate.json", certificate, scientific)
        remaining = read(bound(PREFLIGHT, frozen, scientific))["remaining_gaps"]
        require(
            remaining["conditional_nodes_without_angle_certificates"] == 1020
            and remaining["full_preparation_error_bound"] is None
            and remaining["financial_law_adoption"] is False,
            "Unchanged remaining angle/loader/financial gaps",
        )
        save(output / "remaining_gaps.json", remaining, scientific)
        scientific_cpu, scientific_wall = scientific.finish()
        save(
            output / "scientific_scope_clock.json",
            dict(
                actual_source_AST_slot_symbolic_work_CPU_seconds=scientific_cpu,
                actual_source_AST_slot_symbolic_work_wall_seconds=scientific_wall,
                original_CPU_admission_wall_seconds=[
                    SCIENTIFIC_CPU,
                    SCIENTIFIC_ADMISSION,
                    SCIENTIFIC_WALL,
                ],
                original_scientific_scope_limits_passed=True,
                initial_and_terminal_full_input_verification_charged_to_total_clock=True,
                symbolic_artifact_serialization_charged_to_scientific_clock=True,
            ),
            started,
        )
        interpreter(frozen, started, expected=protocol["actual_interpreter"])
        cpu, wall = budget(started)
        seal(
            output,
            frozen,
            dict(
                passed=True,
                local_only=True,
                budget_censored=False,
                independent_ideal47_omission_applicability_passed=True,
                actual_archived_operations_parsed=1998,
                actual_cyclic_Gray_CX_slots_checked=1022,
                actual_emitted_RY_rows=976,
                actual_absent_RY_slots=47,
                all47_actual_masks_nonzero_even_and_symbolically_zero_for_ideal_bins=True,
                separate_emitted_literalzero_rows=740,
                separate_literalzero_even_masks=455,
                separate_literalzero_odd_masks=285,
                numerical_or_producer_imports=0,
                CDF_conditional_angle_Walsh_table_or_statevector_evaluations=0,
                new_test_credit=0,
                old_fixture_recredit=0,
                failed_WAVE10_run001_credit=0,
                failed_prefix47_run001_credit=0,
                original_binary64_target_symmetry_certified=False,
                serialized_literalzero_accuracy_certified=False,
                remaining_conditional_nodes_without_angle_certificates=1020,
                full_loader_phase_or_accuracy_certified=False,
                financial_law_adopted=False,
                A03_remains_partial=True,
                all110_program_obligations_retained=True,
                numerical_threads=1,
                JIT_disk_cache=False,
                process_CPU_seconds_before_terminal_hashes=cpu,
                wall_seconds_before_terminal_hashes=wall,
                scientific_source_AST_slot_symbolic_CPU_seconds=scientific_cpu,
                scientific_source_AST_slot_symbolic_wall_seconds=scientific_wall,
                original_scientific_CPU_admission_wall_seconds=[
                    SCIENTIFIC_CPU,
                    SCIENTIFIC_ADMISSION,
                    SCIENTIFIC_WALL,
                ],
                total_CPU_admission_wall_seconds=[CPU, ADMISSION, WALL],
                disclosed_total_bookkeeping_budget_expansion=True,
                original_scientific_scope_limits_passed=True,
            ),
            started,
        )
    except BaseException as exception:
        preserve_failure(output, frozen, exception, "run", started, scientific)
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    (prepare if arguments.operation == "prepare" else run)(arguments.output)
