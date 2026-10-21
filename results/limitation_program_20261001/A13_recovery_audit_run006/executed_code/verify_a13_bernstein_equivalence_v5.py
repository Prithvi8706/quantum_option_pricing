"""Fixed exact-arithmetic Bernstein QA; no financial or candidate approval.

Extract only the pinned reference/kernel function definitions by AST. Import
neither source module. Root freezes this new validator, both method documents,
the integer kernel and the actual interpreter before the single fresh run.
"""

from __future__ import annotations

import argparse
import ast
import ctypes
from ctypes import wintypes
from fractions import Fraction
import hashlib
import json
from math import comb, lcm
from pathlib import Path
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
AUTHOR = RESEARCH / "verify_a13_bernstein_equivalence_v5.py"
OLD = RESEARCH / "audit_exp_frontier_recovery_v4.py"
KERNEL = RESEARCH / "bernstein_integer_kernel_v5.py"
METHOD_MD = RESEARCH / "A13_BERNSTEIN_EQUIVALENCE_PREFLIGHT_V5.md"
METHOD_JSON = RESEARCH / "a13_bernstein_equivalence_preflight_v5.json"
INTERPRETER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
OUTPUT = ROOT / "results/limitation_program_20261001/A13_Bernstein_equivalence_check_run001"
OLD_SHA = "61c05812abd7c7c042ab654a025e14b96afcfff00afd5398e72ea334307d07ba"
KERNEL_SHA = "695c10c095c17a0827d5e180195021828b1613e77cb22f6ead42783b7fa70048"
CPU, WORK, WALL = 180, 150, 600
MAX_SOURCE_BYTES = 1 << 20
MAX_RECORD_BYTES = 1 << 20
SHA = re.compile(r"[0-9a-f]{64}\Z")

# Entire small corpus. Each rational is a literal (numerator, denominator).
# This contains no fitted coefficient, residual, financial point or source row.
SMALL_CASES = (
    ("empty_degree0", (), (0, 1), (1, 1), 0),
    ("zero_degree0", ((0, 1),), (-1, 1), (1, 1), 0),
    ("non_dyadic_constant", ((-2, 3),), (-2, 5), (4, 7), 0),
    ("signed_dyadic_linear", ((-3, 8), (5, 16)), (-1, 2), (3, 4), 1),
    ("non_dyadic_linear_domain", ((2, 7), (-4, 9)), (-2, 3), (5, 7), 1),
    ("constant_elevated_linear", ((3, 5),), (-3, 2), (1, 2), 1),
    ("quadratic_cancellation", ((1, 1), (-2, 1), (1, 1)), (0, 1), (2, 1), 2),
    ("quadratic_zero", ((0, 1), (0, 1), (0, 1)), (-1, 3), (2, 3), 2),
    ("quadratic_degenerate", ((2, 3), (-5, 7), (11, 13)), (3, 5), (3, 5), 2),
    ("cubic_non_dyadic", ((-1, 3), (2, 5), (-3, 7), (4, 11)), (-4, 9), (5, 8), 3),
    ("cubic_missing_higher", ((-3, 4), (7, 8)), (-1, 1), (1, 1), 3),
    ("cubic_empty_degenerate", (), (7, 9), (7, 9), 3),
    ("quartic_signed_dyadic", ((1, 2), (-3, 4), (5, 8), (-7, 16), (9, 32)), (-3, 4), (1, 4), 4),
    ("quartic_constant_elevation", ((-5, 6),), (0, 1), (3, 2), 4),
    (
        "quartic_low_degree_large_dyadic384",
        ((1, 1 << 384), (-3, 1 << 385)),
        ((1 << 384) - 1, 1 << 384),
        ((1 << 384) + 1, 1 << 384),
        4,
    ),
    (
        "quintic_non_dyadic",
        ((1, 3), (-2, 5), (3, 7), (-4, 9), (5, 11), (-6, 13)),
        (-2, 7),
        (5, 9),
        5,
    ),
    (
        "quintic_cancellation",
        ((1, 1), (-5, 1), (10, 1), (-10, 1), (5, 1), (-1, 1)),
        (0, 1),
        (2, 1),
        5,
    ),
    ("quintic_sparse", ((0, 1), (0, 1), (-7, 8), (0, 1), (0, 1), (3, 16)), (-1, 2), (1, 2), 5),
    (
        "quintic_low_degree_large_dyadic544",
        ((-5, 1 << 544), (7, 1 << 543), (-11, 1 << 545)),
        (-1, 1 << 544),
        (3, 1 << 544),
        5,
    ),
    ("quintic_degenerate_signed", ((-2, 3), (4, 5), (-6, 7), (8, 9)), (-3, 7), (-3, 7), 5),
)
INVALID_CASES = (
    ("reversed_interval", ((1, 1),), (1, 1), (0, 1), 0),
    ("coefficient_count_exceeds_degree", ((1, 1), (2, 1)), (0, 1), (1, 1), 0),
    ("empty_degree_below_minus1", (), (0, 1), (1, 1), -2),
)
TAYLOR_DEGREES = (79, 111)
MAX_ORACLE_SYSTEMS = 20
MAX_ORACLE_DIMENSION = 6
MAX_ORACLE_SAMPLE_POINTS = 75
MAX_ELIMINATION_CELL_UPDATES = 4096
MAX_TOTAL_RETURNED_COORDINATES = 267


class ValidationBudgetError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ValueError(message)


def start_clock():
    require(sys.platform == "win32" and ctypes.sizeof(ctypes.c_void_p) == 8, "Win64 QA")
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.GetCurrentProcess.argtypes = []
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
    kernel.GetProcessTimes.restype = wintypes.BOOL
    fields = [wintypes.FILETIME() for _ in range(4)]
    require(
        kernel.GetProcessTimes(kernel.GetCurrentProcess(), *(ctypes.byref(v) for v in fields)),
        "Actual process creation time",
    )
    ticks = (fields[0].dwHighDateTime << 32) | fields[0].dwLowDateTime
    age_ns = time.time_ns() - (ticks - 116444736000000000) * 100
    require(age_ns >= 0, "Process creation precedes observation")
    return time.monotonic() - age_ns / 1_000_000_000


def check(started, *, admission=False):
    observed = time.process_time(), time.monotonic() - started
    if observed[0] >= (WORK if admission else CPU) or observed[1] >= WALL:
        raise ValidationBudgetError("Fixed Bernstein QA CPU/wall bound")
    return observed


def read_and_hash(path, expected, started):
    require(type(expected) is str and SHA.fullmatch(expected), "Pinned exact SHA")
    check(started)
    require(path.resolve(strict=True) == path, "Exact ROOT-confined path without alias")
    before = path.stat()
    require(path.is_file() and before.st_size <= MAX_SOURCE_BYTES, "Finite regular input")
    data = bytearray()
    with path.open("rb") as stream:
        while True:
            check(started)
            block = stream.read(65536)
            check(started)
            if not block:
                break
            data.extend(block)
            require(len(data) <= MAX_SOURCE_BYTES, "Bounded actual bytes")
    observed = hashlib.sha256(data).hexdigest()
    check(started)
    after = path.stat()

    def stamp(value):
        return (
            value.st_dev,
            value.st_ino,
            value.st_size,
            value.st_mtime_ns,
            value.st_ctime_ns,
            value.st_mode,
            getattr(value, "st_file_attributes", None),
            getattr(value, "st_reparse_tag", None),
        )

    require(stamp(before) == stamp(after) and len(data) == after.st_size, "Stable actual read")
    require(observed == expected, "Actual bytes match immutable expected SHA")
    return bytes(data)


def extract_function(data, filename, function_name, started):
    check(started)
    tree = ast.parse(data, filename=filename)
    matches = [
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == function_name
    ]
    require(len(matches) == 1, "Exactly one declared function")
    function = matches[0]
    require(
        not function.decorator_list
        and not function.args.defaults
        and not function.args.kw_defaults
        and function.returns is None
        and all(argument.annotation is None for argument in function.args.args)
        and len(function.args.args) == 5
        and function.args.vararg is None
        and function.args.kwarg is None
        and not function.args.kwonlyargs
        and not function.args.posonlyargs,
        "Five plain positional arguments; no definition-time evaluation",
    )
    require(
        not any(
            isinstance(node, (ast.Import, ast.ImportFrom, ast.ClassDef))
            for node in ast.walk(function)
        ),
        "Extracted function imports no module or class",
    )
    isolated = ast.Module(body=[function], type_ignores=[])
    ast.fix_missing_locations(isolated)
    environment = {
        "__builtins__": {
            "len": len,
            "range": range,
            "sum": sum,
            "min": min,
            "max": max,
            "tuple": tuple,
            "ValueError": ValueError,
        },
        "Fraction": Fraction,
        "comb": comb,
        "lcm": lcm,
        "require": require,
        "check": check,
    }
    code = compile(isolated, filename, "exec")
    check(started)
    exec(code, environment)
    check(started)
    return environment[function_name], hashlib.sha256(
        ast.dump(function, include_attributes=False).encode()
    ).hexdigest()


def interpolation_oracle(coefficients, left, right, degree, started, counters):
    """Evaluate p independently, then solve its Bernstein basis interpolation."""
    require(0 <= degree <= 5 and len(coefficients) <= degree + 1, "Fixed small oracle domain")
    dimension = degree + 1
    counters["systems"] += 1
    require(counters["systems"] <= MAX_ORACLE_SYSTEMS, "Finite interpolation systems")
    require(dimension <= MAX_ORACLE_DIMENSION, "Finite exact matrix dimension")
    matrix = []
    for sample in range(dimension):
        check(started)
        t = Fraction(sample, degree) if degree else Fraction(0)
        x = left + (right - left) * t
        value = Fraction(0)
        for coefficient in reversed(coefficients):
            check(started)
            value = value * x + coefficient
        row = []
        for index in range(dimension):
            check(started)
            row.append(Fraction(comb(degree, index)) * t**index * (1 - t) ** (degree - index))
        row.append(value)
        matrix.append(row)
        counters["sample_points"] += 1
        require(counters["sample_points"] <= MAX_ORACLE_SAMPLE_POINTS, "Finite oracle samples")
    for column in range(dimension):
        check(started)
        pivot = next((row for row in range(column, dimension) if matrix[row][column]), None)
        require(pivot is not None, "Nonsingular fixed Bernstein interpolation matrix")
        matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
        denominator = matrix[column][column]
        for index in range(column, dimension + 1):
            check(started)
            matrix[column][index] /= denominator
            counters["cell_updates"] += 1
            require(
                counters["cell_updates"] <= MAX_ELIMINATION_CELL_UPDATES, "Finite Gaussian updates"
            )
        for row in range(dimension):
            check(started)
            if row == column:
                continue
            multiplier = matrix[row][column]
            for index in range(column, dimension + 1):
                check(started)
                matrix[row][index] -= multiplier * matrix[column][index]
                counters["cell_updates"] += 1
                require(
                    counters["cell_updates"] <= MAX_ELIMINATION_CELL_UPDATES,
                    "Finite Gaussian updates",
                )
    return [row[-1] for row in matrix]


def vector_record(values, started):
    check(started)
    require(
        type(values) is list and all(type(value) is Fraction for value in values),
        "Exact Fraction vector ABI",
    )
    vector = [[value.numerator, value.denominator] for value in values]
    data = json.dumps(vector, separators=(",", ":")).encode()
    check(started)
    require(len(data) <= MAX_RECORD_BYTES, "Finite exact vector serialization")
    return {
        "coordinate_count": len(values),
        "exact_vector_sha256": hashlib.sha256(data).hexdigest(),
        "exact_vector": vector,
    }


def write_json(path, value, started):
    check(started)
    data = (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()
    check(started)
    require(len(data) <= MAX_RECORD_BYTES, "Finite QA record")
    with path.open("xb") as stream:
        for offset in range(0, len(data), 65536):
            check(started)
            stream.write(data[offset : offset + 65536])
            check(started)
    observed = hashlib.sha256(data).hexdigest()
    check(started)
    require(path.read_bytes() == data, "Exact retained QA bytes")
    check(started)
    return observed


def main():
    started = start_clock()
    created = False
    try:
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("--kernel-source-sha256", required=True)
        parser.add_argument("--validation-source-sha256", required=True)
        parser.add_argument("--method-md-sha256", required=True)
        parser.add_argument("--method-json-sha256", required=True)
        parser.add_argument("--interpreter-sha256", required=True)
        parser.add_argument("--output", required=True)
        arguments = parser.parse_args()
        require(arguments.kernel_source_sha256 == KERNEL_SHA, "Exact reviewed kernel pin")
        require(sys.flags.dont_write_bytecode, "Pinned Python -B before -m")
        require(Path(sys.executable).resolve() == INTERPRETER, "Pinned interpreter path")
        require(Path.cwd().resolve() == ROOT, "Exact workspace cwd")
        require(
            Path(arguments.output).resolve() == OUTPUT and not OUTPUT.exists(),
            "Fresh fixed receipt",
        )
        pins = {
            OLD: OLD_SHA,
            KERNEL: arguments.kernel_source_sha256,
            AUTHOR: arguments.validation_source_sha256,
            METHOD_MD: arguments.method_md_sha256,
            METHOD_JSON: arguments.method_json_sha256,
            INTERPRETER: arguments.interpreter_sha256,
        }
        initial = {path: read_and_hash(path, expected, started) for path, expected in pins.items()}
        policy = json.loads(initial[METHOD_JSON])
        require(
            policy["schema"] == "a13-bernstein-exact-equivalence-preflight-v5"
            and policy["old_source_sha256"] == OLD_SHA
            and policy["kernel_source_sha256"] == KERNEL_SHA
            and policy["limits_CPU_work_wall_seconds"] == [CPU, WORK, WALL]
            and policy["fixed_small_case_count"] == len(SMALL_CASES)
            and policy["fixed_Taylor_degrees"] == list(TAYLOR_DEGREES)
            and policy["fixed_small_case_names"] == [case[0] for case in SMALL_CASES]
            and policy["new_test_credit"] == 0,
            "Exact prospective QA policy",
        )
        old, old_ast_sha = extract_function(initial[OLD], OLD.name, "exact_bernstein", started)
        integer, new_ast_sha = extract_function(
            initial[KERNEL], KERNEL.name, "integer_bernstein", started
        )

        def new(coefficients, left, right, degree):
            return integer(coefficients, left, right, degree, lambda: check(started))

        check(started, admission=True)
        OUTPUT.mkdir()
        created = True
        records = []
        counters = {"systems": 0, "sample_points": 0, "cell_updates": 0}
        returned = 0
        for label, raw, left_raw, right_raw, degree in SMALL_CASES:
            check(started, admission=True)
            coefficients = [Fraction(*value) for value in raw]
            left, right = Fraction(*left_raw), Fraction(*right_raw)
            require(
                all(
                    max(abs(value.numerator).bit_length(), value.denominator.bit_length()) <= 546
                    for value in coefficients + [left, right]
                ),
                "Fixed small rational bit cap",
            )
            expected = interpolation_oracle(coefficients, left, right, degree, started, counters)
            actual_old = old(coefficients, left, right, degree, started)
            actual_new = new(coefficients, left, right, degree)
            require(
                type(actual_old) is list
                and type(actual_new) is list
                and all(type(value) is Fraction for value in actual_old + actual_new),
                "Both transforms retain the exact Fraction list ABI",
            )
            require(
                actual_old == expected and actual_new == expected,
                "Both transforms equal independent interpolation: " + label,
            )
            returned += len(expected)
            records.append(
                {
                    "case": label,
                    "degree": degree,
                    "oracle": "exact-Bernstein-basis-interpolation-Gaussian-elimination",
                    "both_equal_oracle": True,
                    **vector_record(expected, started),
                }
            )
        require(
            counters["systems"] == 20
            and counters["sample_points"] == 75
            and counters["cell_updates"] == 1395,
            "Exact fixed oracle counts",
        )
        require(
            old([], Fraction(0), Fraction(1), -1, started)
            == new([], Fraction(0), Fraction(1), -1)
            == [],
            "Empty degree minus1 compatibility",
        )
        records.append({"case": "empty_degree_minus1", "degree": -1, "both_return_empty": True})
        for label, raw, left_raw, right_raw, degree in INVALID_CASES:
            check(started, admission=True)
            coefficients = [Fraction(*value) for value in raw]
            left, right = Fraction(*left_raw), Fraction(*right_raw)
            rejected = []
            for function in (
                lambda: old(coefficients, left, right, degree, started),
                lambda: new(coefficients, left, right, degree),
            ):
                try:
                    function()
                except ValueError:
                    rejected.append(True)
                else:
                    rejected.append(False)
            require(rejected == [True, True], "Matching fixed rejected-domain behavior: " + label)
            records.append({"case": label, "both_reject_with_ValueError": True})
        for degree in TAYLOR_DEGREES:
            check(started, admission=True)
            coefficients, factorial = [], 1
            for power in range(degree + 1):
                check(started)
                if power:
                    factorial *= power
                coefficients.append(Fraction(1, factorial))
            left, right = Fraction(-1, 128), Fraction(1, 128)
            actual_old = old(coefficients, left, right, degree, started)
            actual_new = new(coefficients, left, right, degree)
            require(
                type(actual_old) is list
                and type(actual_new) is list
                and all(type(value) is Fraction for value in actual_old + actual_new),
                "Complete Taylor Fraction list ABI",
            )
            require(
                actual_old == actual_new and len(actual_new) == degree + 1,
                "Complete fixed Taylor transform equality",
            )
            returned += len(actual_new)
            require(returned <= MAX_TOTAL_RETURNED_COORDINATES, "Finite complete vector count")
            records.append(
                {
                    "case": "complete_Taylor_degree" + str(degree),
                    "degree": degree,
                    "old_new_equal": True,
                    "independent_small_oracle_applied": False,
                    "fitted_or_source_corpus": False,
                    **vector_record(actual_new, started),
                }
            )
        require(returned == 267, "Exact 75 plus 80 plus 112 returned coordinates")
        check(started, admission=True)
        result_sha = write_json(OUTPUT / "finite_equivalence_results.json", records, started)
        cpu, wall = check(started)
        summary = {
            "schema": "a13-bernstein-exact-equivalence-summary-v5",
            "completed": True,
            "passed": True,
            "budget_censored": False,
            "fixed_small_oracle_cases": 20,
            "oracle_sample_points": counters["sample_points"],
            "oracle_Gaussian_cell_updates": counters["cell_updates"],
            "empty_degree_minus1_compatibility_passed": True,
            "matching_rejected_input_cases": 3,
            "complete_Taylor_degrees": list(TAYLOR_DEGREES),
            "complete_exact_coordinates_compared": returned,
            "all_small_cases_equal_independent_interpolation_oracle": True,
            "complete_Taylor_comparisons_are_reference_equivalence_only": True,
            "old_function_AST_sha256": old_ast_sha,
            "new_function_AST_sha256": new_ast_sha,
            "auditor_and_kernel_modules_imported": False,
            "source_fitting_replayed": False,
            "interval_witness_or_financial_proof_replayed": False,
            "all20_scientific_screen_approved": False,
            "candidate_G2_established": False,
            "gate_emission_authorized": False,
            "adoption": False,
            "new_test_credit": 0,
            "new_gate_replays": 0,
            "new_price_samples": 0,
            "timing_improvement_or_future_budget_fit_claim": False,
            "limits_CPU_work_wall_seconds": [CPU, WORK, WALL],
            "actual_process_CPU_seconds": cpu,
            "actual_creation_wall_seconds": wall,
            "scope": "fixed exact arithmetic kernel QA only; no all20 or candidate approval",
        }
        summary_sha = write_json(OUTPUT / "summary.json", summary, started)
        frozen = {}
        for path, expected in pins.items():
            require(
                read_and_hash(path, expected, started) == initial[path],
                "Fresh terminal input bytes unchanged",
            )
            frozen[path.relative_to(ROOT).as_posix()] = expected
        require(
            {path.name for path in OUTPUT.iterdir()}
            == {"finite_equivalence_results.json", "summary.json"},
            "Exact fresh owned inventory before manifest",
        )
        for name, expected in (
            ("finite_equivalence_results.json", result_sha),
            ("summary.json", summary_sha),
        ):
            read_and_hash(OUTPUT / name, expected, started)
        write_json(
            OUTPUT / "manifest.json",
            {
                "schema": "a13-bernstein-exact-equivalence-manifest-v5",
                "files": {
                    "finite_equivalence_results.json": result_sha,
                    "summary.json": summary_sha,
                },
                "frozen_inputs": frozen,
                "manifest_self_hash_excluded": True,
                "completed": True,
                "passed": True,
                "new_test_credit": 0,
            },
            started,
        )
        require(
            {path.name for path in OUTPUT.iterdir()}
            == {"finite_equivalence_results.json", "summary.json", "manifest.json"},
            "Exact terminal owned inventory",
        )
        check(started)
        print(
            json.dumps(
                {
                    "passed": True,
                    "small_oracle_cases": 20,
                    "Taylor_comparisons": 2,
                    "new_test_credit": 0,
                }
            )
        )
    except BaseException:
        if created:
            try:
                with (OUTPUT / "FAILED_UNSEALED.json").open("xb") as stream:
                    stream.write(
                        b'{"failed":true,"passed":false,"completed":false,"budget_censored":null,"hard_budget_state_uncertified":true,"new_test_credit":0,"partial_success_invalid":true}\n'
                    )
            except OSError:
                pass
        raise


if __name__ == "__main__":
    main()
