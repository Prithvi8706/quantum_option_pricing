"""Bounded finite equivalence validation only; no candidate or fixture credit.

Extract just the independently pinned old/new selection functions by AST.
Import neither auditor module, refit no coefficient, and evaluate no financial
or interval certificate. Root must freeze this source, the V4 source and the
fixed prospective validation inputs before the single fresh invocation.
"""

from __future__ import annotations

import argparse
import ast
import ctypes
from ctypes import wintypes
from fractions import Fraction
import hashlib
from itertools import combinations
import json
from pathlib import Path
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
OUTPUT = ROOT / "results/limitation_program_20261001/A13_recovery_DP_equivalence_check_run001"
AUTHOR = RESEARCH / "verify_a13_recovery_dp_equivalence_v4.py"
OLD = RESEARCH / "audit_exp_frontier_recovery_v3.py"
NEW = RESEARCH / "audit_exp_frontier_recovery_v4.py"
OLD_SHA = "f094a5bd4738735bfae4775b6149fc354a9a15bad7e28850811aa1f0f27d7a3c"
CPU, WORK, WALL = 10, 8, 30
SHA = re.compile(r"[0-9a-f]{64}\Z")

# This fixed list is the entire validation corpus, chosen before execution.
# No source-corpus residuals or candidate outcomes enter these tiny arrays.
CASES = (
    ("all_zero", (0, 0), 1),
    ("one_nonzero_with_zeros", (0, 1, 0), 1),
    ("one_sign_infeasible", (1, 2, 3), 2),
    ("positive_first_sum_and_lex_ties", (2, -1, 2, -1, 2), 3),
    ("negative_first_sum_and_lex_ties", (-2, 1, -2, 1, -2), 3),
    ("repeated_sign_runs", (1, 3, -1, -3, 2, 4, -2, -4), 4),
    ("interleaved_zeros", (0, 2, 0, -2, 0, 2, 0, -2), 3),
    ("bottleneck_precedes_larger_sum", (10, -1, 10, -5, 5), 3),
    ("prefix_bottleneck_collapse", (10, -10, 9, -90, 8), 3),
    ("different_dyadic_scales", ((1, 2), (-3, 8), (5, 16), (-7, 32), (9, 64)), 4),
    ("negative_dyadic_first", ((-1, 1024), (3, 2), (-7, 32), (5, 16), (-9, 64)), 3),
    ("both_ending_signs_equal_sum", (1, -1, 1, -1), 3),
    ("length_exceeds_candidate_count", (1, -2, 3, -4), 6),
    ("zeros_and_two_sign_blocks", (0, 1, 2, 3, -1, -2, -3, 0), 2),
    ("many_threshold_ties", (4, -4, 4, -4, 4, -4), 4),
    (
        "large_exact_dyadic_denominators",
        ((1, 1 << 384), (-3, 1 << 385), (5, 1 << 383), (-7, 1 << 386)),
        3,
    ),
)


class ValidationBudgetError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ValueError(message)


def start_clock():
    require(sys.platform == "win32" and ctypes.sizeof(ctypes.c_void_p) == 8, "Win64 validation")
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.GetCurrentProcess.argtypes = []
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
    kernel.GetProcessTimes.restype = wintypes.BOOL
    fields = [wintypes.FILETIME() for _ in range(4)]
    require(
        kernel.GetProcessTimes(kernel.GetCurrentProcess(), *(ctypes.byref(v) for v in fields)),
        "Actual validation creation time",
    )
    ticks = (fields[0].dwHighDateTime << 32) | fields[0].dwLowDateTime
    age_ns = time.time_ns() - (ticks - 116444736000000000) * 100
    require(age_ns >= 0, "Validation creation precedes observation")
    return time.monotonic() - age_ns / 1_000_000_000


def check(started, *, admission=False):
    observed = time.process_time(), time.monotonic() - started
    if observed[0] >= (WORK if admission else CPU) or observed[1] >= WALL:
        raise ValidationBudgetError("Fixed finite validation CPU/wall bound")
    return observed


def read_and_hash(path, expected, started):
    require(type(expected) is str and SHA.fullmatch(expected), "Pinned exact source SHA")
    require(path.resolve(strict=True) == path, "Exact confined source path, no alias")
    before = path.stat()
    require(before.st_size <= 1 << 20, "Finite source byte cap")
    check(started)
    data = path.read_bytes()
    check(started)
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

    require(
        stamp(before) == stamp(after) and len(data) == after.st_size, "Stable actual source read"
    )
    require(observed == expected, "Actual source hash equals immutable expected SHA")
    return data


def selector(data, name, started):
    check(started)
    tree = ast.parse(data, filename=name)
    definitions = [
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "alternating_selection"
    ]
    require(len(definitions) == 1, "Exactly one declared selection function")
    function = definitions[0]
    require(not function.decorator_list, "No selection decorator execution")
    require(
        not any(isinstance(node, (ast.Import, ast.ImportFrom)) for node in ast.walk(function)),
        "Selection function imports no module",
    )
    isolated = ast.Module(body=[function], type_ignores=[])
    ast.fix_missing_locations(isolated)
    environment = {"Fraction": Fraction, "require": require, "check": check}
    code = compile(isolated, name, "exec")
    check(started)
    exec(code, environment)
    check(started)
    return environment["alternating_selection"]


def exhaustive_oracle(values, length, started):
    """Enumerate every subset, independent of both DP implementations."""
    best = None
    visited = 0
    for indices in combinations(range(len(values)), length):
        check(started)
        visited += 1
        selected = [values[index] for index in indices]
        if any(value == 0 for value in selected):
            continue
        if any((first > 0) == (second > 0) for first, second in zip(selected, selected[1:])):
            continue
        objective = (
            min(abs(value) for value in selected),
            sum(abs(value) for value in selected),
            indices,
        )
        if (
            best is None
            or objective[:2] > best[:2]
            or objective[:2] == best[:2]
            and objective[2] < best[2]
        ):
            best = objective
    check(started)
    return best, visited


def run_selector(function, values, length, started):
    try:
        threshold, total, indices = function(values, length, started)
    except ValueError:
        return None
    return threshold, total, tuple(indices)


def encode_result(value):
    if value is None:
        return None
    threshold, total, indices = value
    return {
        "bottleneck": [threshold.numerator, threshold.denominator],
        "absolute_height_sum": [total.numerator, total.denominator],
        "original_indices": list(indices),
    }


def write_json(path, value, started):
    check(started)
    data = (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()
    check(started)
    require(len(data) <= 1 << 20, "Finite validation record byte cap")
    with path.open("xb") as stream:
        for offset in range(0, len(data), 65536):
            check(started)
            stream.write(data[offset : offset + 65536])
            check(started)
    observed = hashlib.sha256(data).hexdigest()
    check(started)
    require(path.read_bytes() == data, "Exact retained validation JSON")
    check(started)
    return observed


def main():
    started = start_clock()
    created = False
    try:
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("--new-source-sha256", required=True)
        parser.add_argument("--validation-source-sha256", required=True)
        parser.add_argument("--output", required=True)
        arguments = parser.parse_args()
        require(sys.flags.dont_write_bytecode, "Pinned interpreter -B before -m")
        require(
            Path(sys.executable).resolve() == ROOT / ".context/frontier_t0_env/Scripts/python.exe",
            "Pinned Python",
        )
        require(Path.cwd().resolve() == ROOT, "Exact workspace cwd")
        require(
            Path(arguments.output).resolve() == OUTPUT and not OUTPUT.exists(),
            "Fresh fixed validation receipt",
        )
        data = {
            OLD: read_and_hash(OLD, OLD_SHA, started),
            NEW: read_and_hash(NEW, arguments.new_source_sha256, started),
            AUTHOR: read_and_hash(AUTHOR, arguments.validation_source_sha256, started),
        }
        old = selector(data[OLD], OLD.name, started)
        new = selector(data[NEW], NEW.name, started)
        check(started, admission=True)
        OUTPUT.mkdir()
        created = True
        records, total_subsets = [], 0
        for label, raw, length in CASES:
            check(started, admission=True)
            values = [
                Fraction(*value) if isinstance(value, tuple) else Fraction(value) for value in raw
            ]
            require(2 <= len(values) <= 8 and 1 <= length <= 6, "Preregistered tiny-array cap")
            expected, visited = exhaustive_oracle(values, length, started)
            total_subsets += visited
            require(total_subsets <= 4096, "Fixed exhaustive-subset cap")
            actual_old = run_selector(old, values, length, started)
            actual_new = run_selector(new, values, length, started)
            require(
                actual_old == expected and actual_new == expected,
                "Both exact selectors equal exhaustive oracle: " + label,
            )
            records.append(
                {
                    "case": label,
                    "length": length,
                    "candidate_locations": len(values),
                    "subsets_enumerated": visited,
                    "expected": encode_result(expected),
                    "both_selectors_equal_exhaustive_oracle": True,
                }
            )
        frozen = {}
        for path, expected in (
            (OLD, OLD_SHA),
            (NEW, arguments.new_source_sha256),
            (AUTHOR, arguments.validation_source_sha256),
        ):
            require(
                read_and_hash(path, expected, started) == data[path],
                "Fresh source bytes unchanged after finite validation",
            )
            frozen[path.relative_to(ROOT).as_posix()] = expected
        record_sha = write_json(OUTPUT / "finite_equivalence_results.json", records, started)
        cpu, wall = check(started)
        summary = {
            "schema": "a13-recovery-exact-dp-finite-equivalence-summary-v1",
            "completed": True,
            "passed": True,
            "fixed_case_count": len(CASES),
            "subsets_enumerated": total_subsets,
            "all_cases_equal_independent_exhaustive_subset_oracle": True,
            "legacy_fraction_reference_also_equal": True,
            "old_and_new_auditor_modules_imported": False,
            "source_corpus_or_fitting_replayed": False,
            "all20_scientific_screen_approved": False,
            "new_test_credit": 0,
            "new_gate_replays": 0,
            "new_price_samples": 0,
            "gate_emission_authorized": False,
            "adoption": False,
            "candidate_G2_established": False,
            "limits_CPU_work_wall_seconds": [CPU, WORK, WALL],
            "actual_process_CPU_seconds": cpu,
            "actual_creation_wall_seconds": wall,
            "scope": (
                "fixed finite selector equivalence only; "
                "no financial, approximation or resource proof"
            ),
        }
        summary_sha = write_json(OUTPUT / "summary.json", summary, started)
        write_json(
            OUTPUT / "manifest.json",
            {
                "schema": "a13-recovery-exact-dp-finite-equivalence-manifest-v1",
                "files": {
                    "finite_equivalence_results.json": record_sha,
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
        check(started)
        print(json.dumps({"passed": True, "fixed_cases": len(CASES), "new_test_credit": 0}))
    except BaseException:
        if created:
            try:
                with (OUTPUT / "FAILED_UNSEALED.json").open("xb") as stream:
                    stream.write(
                        b'{"failed":true,"passed":false,"completed":false,"new_test_credit":0,"partial_success_invalid":true}\n'
                    )
            except FileExistsError:
                pass
        raise


if __name__ == "__main__":
    main()
