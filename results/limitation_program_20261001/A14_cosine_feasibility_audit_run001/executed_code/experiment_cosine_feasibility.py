"""AUTHOR-STAGE fixed A14 cosine component and conditional resource screen.

This completed author draft awaits fixed pins, independent static review and
external ROOT release before preparation or execution. No numerical kernel,
import of a scientific package,
source walker, fit, gate, proof, fixture or preparation executed during authoring.
The only proposed rows are CORDIC48 signed72/f56 and Taylor6x64 signed72/f40.
"""

from __future__ import annotations


import argparse
import ast
import ctypes
from ctypes import wintypes
from collections import Counter
import hashlib
from importlib import metadata
from importlib.util import cache_from_source
import json
import os
from pathlib import Path
import site
import sys
import traceback

from fractions import Fraction
from math import factorial
import time


W, F, Q = 72, 40, 1 << 40
CF, CQ, ITERATIONS = 56, 1 << 56, 48
EPS, CEPS, H = Fraction(1, Q), Fraction(1, CQ), Fraction(1, 128)
CPU, ADMISSION, WALL = 300, 270, 900
ROWS = ("CORDIC_N48_W72_F56_BK72", "TAYLOR_D6_S64_W72_F40")
CASE_SITES = {"B4x12": 60, "B8x52": 468}


class BudgetCensoredError(RuntimeError):
    """Fixed process-inclusive CPU/wall boundary, never a retry request."""


class NativeRejectedError(ValueError):
    """A fixed candidate's full-word arithmetic safety was not certified."""


class ResourceRejectedError(ValueError):
    """No contract-matched measured or explicitly charged primitive was admitted."""


def require(condition, message):
    if not condition:
        raise ValueError(message)


def tick(started, admission=False):
    """Controller must supply CPU origin0 and actual process-creation wall origin."""
    require(started[0] == 0, "Charge process bootstrap CPU")
    cpu, wall = time.process_time(), time.monotonic() - started[1]
    if cpu >= (ADMISSION if admission else CPU) or wall >= WALL:
        raise BudgetCensoredError("Fixed A14 300CPU/270admission/900wall")
    return cpu, wall


def encode(value):
    value = Fraction(value)
    return [value.numerator, value.denominator]


def rational(value):
    require(
        type(value) is list
        and len(value) == 2
        and all(type(item) is int for item in value)
        and value[1] > 0,
        "Canonical rational pair",
    )
    result = Fraction(*value)
    require(encode(result) == value, "Reduced exact rational")
    return result


def interval_endpoint(value):
    sign, mantissa, exponent, bits = value
    require(
        sign in (0, 1)
        and type(mantissa) is int
        and type(exponent) is int
        and type(bits) is int
        and mantissa >= 0
        and bits >= 0,
        "Finite outward binary endpoint",
    )
    return Fraction((-1 if sign else 1) * mantissa) * Fraction(2) ** exponent


def endpoints(value):
    result = tuple(interval_endpoint(item) for item in value._mpi_)
    require(len(result) == 2 and result[0] <= result[1], "Ordered outward enclosure")
    return result


def outward(mp, value):
    value = Fraction(value)
    return mp.iv.mpf(value.numerator) / mp.iv.mpf(value.denominator)


def nearest(value):
    value = Fraction(value)
    quotient, remainder = divmod(value.numerator, value.denominator)
    return quotient + int(
        2 * remainder > value.denominator or (2 * remainder == value.denominator and quotient % 2)
    )


def signed_word(value):
    require(type(value) is int and -(1 << 71) <= value < 1 << 71, "Canonical signed72")
    return value


def native_range(value):
    require(
        type(value) is tuple
        and len(value) == 2
        and all(type(item) is int for item in value)
        and value[0] <= value[1],
        "Canonical native interval representation",
    )
    if not -(1 << 71) <= value[0] <= value[1] < 1 << 71:
        raise NativeRejectedError("Selected AND unselected signed72 operation exceeds native range")
    return value


def literal_record(true_value, fractional_bits):
    lo, hi = endpoints(true_value)
    scale = 1 << fractional_bits
    word = signed_word(nearest(scale * (lo + hi) / 2))
    error = max(abs(Fraction(word, scale) - lo), abs(Fraction(word, scale) - hi))
    return dict(
        raw=word,
        true_enclosure=[encode(lo), encode(hi)],
        exact_rounding_reference=encode((lo + hi) / 2),
        actual_abs_error_upper=encode(error),
        true_nearest_half_ULP_certified=error <= Fraction(1, 2 * scale),
    )


def make_cordic_literals(mp, started):
    """Deferred actual48 angle/gain intervals; no literal-nearest assumption."""
    tick(started, admission=True)
    rows = []
    gain_square = Fraction(1)
    for index in range(ITERATIONS):
        tick(started)
        step = Fraction(1, 1 << index)
        angle = mp.iv.atan2(outward(mp, step), outward(mp, 1)) / (2 * mp.iv.pi)
        row = literal_record(angle, CF)
        row.update(i=index, true_turns_enclosure=row.pop("true_enclosure"))
        rows.append(row)
        gain_square *= 1 + step * step
    gain = literal_record(1 / mp.iv.sqrt(outward(mp, gain_square)), CF)
    return dict(
        schema="a14-cordic-literals-v1",
        row_id=ROWS[0],
        interval_digits=90,
        fractional_bits=CF,
        iterations=ITERATIONS,
        angle_rows=rows,
        gain_reciprocal=gain,
        exact_finite_gain_square=encode(gain_square),
        exact_rounding_policy="ties-even of actual saved rational interval midpoint",
        half_ULP_premises_passed=all(row["true_nearest_half_ULP_certified"] for row in rows)
        and gain["true_nearest_half_ULP_certified"],
    )


def cordic_uniform_certificate(mp, literals, started):
    tick(started)
    require(literals["half_ULP_premises_passed"] is True, "Actual angle/gain half-ULP premises")
    same_ids = [row["i"] for row in literals["angle_rows"]]
    require(same_ids == list(range(ITERATIONS)), "Exactly48 actual angle literals")
    require(
        rational(literals["exact_finite_gain_square"]) < 4,
        "Exact finite gain square certifies K48<2",
    )
    angle_intervals = [
        tuple(rational(value) for value in row["true_turns_enclosure"])
        for row in literals["angle_rows"]
    ]
    require(all(0 < lo <= hi for lo, hi in angle_intervals), "All true angles positive")
    require(literals["angle_rows"][0]["raw"] == CQ // 8, "Exact first quarter-angle literal")
    doubling = []
    for index in range(1, ITERATIONS):
        tick(started)
        previous_upper = Fraction(1, 8) if index == 1 else angle_intervals[index - 1][1]
        require(
            previous_upper < 2 * angle_intervals[index][0],
            "Independent outward premise a_(i-1)<2*a_i",
        )
        doubling.append(
            dict(
                i=index,
                previous_upper=encode(previous_upper),
                twice_current_lower=encode(2 * angle_intervals[index][0]),
            )
        )
    pi_upper = endpoints(mp.iv.pi)[1]
    require(pi_upper < 4, "Outward pi bound used by the paper certificate")
    require(
        2 * pi_upper * angle_intervals[-1][1] < Fraction(1, 1 << 47),
        "Actual final-angle outward upper below atan power bound",
    )
    angle_bound = Fraction(1, 1 << 47) + 3 * pi_upper * ITERATIONS * CEPS
    vector_bound = (3 * ITERATIONS + 1) * CEPS
    rounding_bound = EPS / 2
    total = angle_bound + vector_bound + rounding_bound
    require(total < EPS, "Fixed48/f56 paper target at actual literal premises")
    return dict(
        schema="a14-cordic-uniform-certificate-v1",
        row_id=ROWS[0],
        interval_digits=90,
        iterations=ITERATIONS,
        actual_literal_half_ULP_premises_passed=True,
        actual_angle_doubling_premise_rows=doubling,
        exact_finite_gain_square_less_than_four=True,
        actual_final_angle_radian_upper=encode(2 * pi_upper * angle_intervals[-1][1]),
        finite_gain_less_than_two_proof="sqrt2*exp(1/6)<(3/2)*(6/5)<2",
        greedy_angle_induction="a_(i-1)<2*a_i; |z_N|<=a_47+N*e/2; true residual adds N*e/2",
        radian_residual_upper=encode(angle_bound),
        shift_floor_and_gain_vector_upper=encode(vector_bound),
        final_nearest_rounding_upper=encode(rounding_bound),
        cosine_error_upper=encode(total),
        exact_axis_and_nonexpansive_projection_recipe_required=True,
        source_and_all_native_integer_safety_required=True,
        actual_native_gate_or_full_G2_claim=False,
    )


def cordic_native_safety(literals, started):
    """Exact integer interval induction over BOTH eager branches at all48 stages."""
    tick(started, admission=True)
    gain = signed_word(literals["gain_reciprocal"]["raw"])
    x, y, z = (gain, gain), (0, 0), (-(1 << 53), 1 << 53)
    history = []
    for row in literals["angle_rows"]:
        tick(started)
        index, angle = row["i"], signed_word(row["raw"])
        sx, sy = (x[0] >> index, x[1] >> index), (y[0] >> index, y[1] >> index)
        xp, xm = (x[0] + sy[0], x[1] + sy[1]), (x[0] - sy[1], x[1] - sy[0])
        yp, ym = (y[0] + sx[0], y[1] + sx[1]), (y[0] - sx[1], y[1] - sx[0])
        zp, zm = (z[0] + angle, z[1] + angle), (z[0] - angle, z[1] - angle)
        branches = dict(x_plus=xp, x_minus=xm, y_plus=yp, y_minus=ym, z_plus=zp, z_minus=zm)
        for value in (x, y, z, sx, sy, *branches.values()):
            native_range(value)
        history.append(
            dict(
                i=index,
                old_x=list(x),
                old_y=list(y),
                old_z=list(z),
                shift_x=list(sx),
                shift_y=list(sy),
                eager_branches={key: list(value) for key, value in branches.items()},
            )
        )
        x = min(xp[0], xm[0]), max(xp[1], xm[1])
        y = min(yp[0], ym[0]), max(yp[1], ym[1])
        z = min(zp[0], zm[0]), max(zp[1], zm[1])
    for value in (x, y, (-x[1], -x[0]), (-y[1], -y[0])):
        native_range(value)
    return dict(
        schema="a14-cordic-native-safety-v1",
        row_id=ROWS[0],
        stages=history,
        selected_and_unselected_branches_checked=True,
        simultaneous_old_state_updates=True,
        retained_core_full72_words=627,
        exact_signed_rounding_rule=(
            "q=c//65536;r=c-65536*q;increment iff r>32768 or(r==32768 and q odd)"
        ),
        fold_clamp_axis_and_complete_typed_IR_guards_still_required=True,
        full_function_and_source_safety_claim=False,
    )


def make_taylor_literals(mp, started):
    tick(started, admission=True)
    rows = []
    for segment in range(64):
        center = Fraction(2 * segment + 1, 128)
        for degree in range(7):
            tick(started)
            value = (
                (2 * mp.iv.pi) ** degree
                * mp.iv.cos(2 * mp.iv.pi * outward(mp, center) + degree * mp.iv.pi / 2)
                / factorial(degree)
            )
            row = literal_record(value, F)
            row.update(
                segment=segment,
                degree=degree,
                center_raw=(2 * segment + 1) << 33,
                true_coefficient_enclosure=row.pop("true_enclosure"),
            )
            rows.append(row)
    return dict(
        schema="a14-taylor6-literals-v1",
        row_id=ROWS[1],
        interval_digits=90,
        segments=64,
        degree=6,
        coefficient_rows=rows,
        coefficient_count=448,
        center_count=64,
        total_lookup_literals=512,
        lookup_output_full72_banks=8,
        exact_rounding_policy="ties-even of saved rational90 interval midpoint",
        all_actual_coefficient_errors_paid=True,
    )


def taylor_uniform_certificate(mp, literals, started):
    tick(started)
    require(len(literals["coefficient_rows"]) == 448, "Exactly448 actual Taylor literals")
    tail = endpoints((2 * mp.iv.pi * outward(mp, H)) ** 7 / factorial(7))[1]
    floors = EPS * sum((H**power for power in range(6)), Fraction(0))
    records = []
    for segment in range(64):
        tick(started)
        rows = literals["coefficient_rows"][7 * segment : 7 * (segment + 1)]
        require(
            [row["degree"] for row in rows] == list(range(7)), "Canonical segment coefficient order"
        )
        require(all(row["segment"] == segment for row in rows), "Canonical segment identity")
        error = sum(
            (rational(row["actual_abs_error_upper"]) * H ** row["degree"] for row in rows),
            Fraction(0),
        )
        records.append(
            dict(
                segment=segment,
                literal_error_upper=encode(error),
                Taylor_tail_upper=encode(tail),
                Horner_floor_upper=encode(floors),
                cosine_error_upper=encode(error + tail + floors),
            )
        )
    return dict(
        schema="a14-taylor6-uniform-certificate-v1",
        row_id=ROWS[1],
        interval_digits=90,
        local_absolute_radius=encode(H),
        segment_rows=records,
        cosine_error_upper=encode(max(rational(row["cosine_error_upper"]) for row in records)),
        actual_errors_paid_without_assumed_half_ULP=True,
        source_and_full_native_safety_required=True,
        fitter_Bernstein_or_minimax_claim=False,
        actual_native_gate_or_full_G2_claim=False,
    )


def taylor_native_safety(literals, started):
    tick(started, admission=True)
    records = []
    h_raw = Q // 128
    for segment in range(64):
        tick(started)
        words = [
            signed_word(row["raw"])
            for row in literals["coefficient_rows"][7 * segment : 7 * (segment + 1)]
        ]
        value = words[6], words[6]
        steps = []
        for degree in range(5, -1, -1):
            products = [left * right for left in value for right in (-h_raw, h_raw)]
            product = min(products), max(products)
            require(
                -(1 << 143) <= product[0] <= product[1] < 1 << 143, "Actual full signed144 product"
            )
            floor_value = product[0] // Q, product[1] // Q
            value = native_range((floor_value[0] + words[degree], floor_value[1] + words[degree]))
            steps.append(
                dict(
                    degree=degree,
                    product144=list(product),
                    floor=list(floor_value),
                    stored72=list(value),
                )
            )
        records.append(
            dict(
                segment=segment,
                center_raw=(2 * segment + 1) << 33,
                local_raw_interval=[-h_raw, h_raw],
                Horner_steps=steps,
            )
        )
    return dict(
        schema="a14-taylor6-native-safety-v1",
        row_id=ROWS[1],
        segment_rows=records,
        endpoint_Q_selected_to_zero_before_eager_lookup=True,
        lookup_address_raw_interval=[0, 63],
        lookup_high_bits_zero_required=True,
        complete_typed_clamp_axis_lookup_IR_guards_still_required=True,
        full_function_and_source_safety_claim=False,
    )


ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
PROGRAM = ROOT / "results/limitation_program_20261001"
OUTPUT = PROGRAM / "A14_cosine_feasibility_run001"
PRODUCER = RESEARCH / "experiment_cosine_feasibility.py"
AUDITOR = RESEARCH / "audit_cosine_feasibility.py"
METHOD = RESEARCH / "a14_cosine_feasibility_preflight.json"
METHOD_DOC = RESEARCH / "A14_COSINE_FEASIBILITY_PREFLIGHT.md"
IMPLEMENTATION = RESEARCH / "a14_cosine_feasibility_implementation_preflight.json"
IMPLEMENTATION_DOC = RESEARCH / "A14_COSINE_FEASIBILITY_IMPLEMENTATION_PREFLIGHT.md"
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = 24_000, 2 * 1024**3
_PATHS, _HASHES, _OBSERVED = {}, {}, {}
_EXTERNAL_TREES, _EXTERNAL_FILES = (), ()
_EXTERNAL_ROOT = None
_EXCLUDED_RUNTIME = ()
_PROCESS_CREATION_TICKS = None


def budget(started, admission=False):
    return tick(started, admission)


def process_started():
    """Charge actual process CPU and creation-derived monotonic wall, including bootstrap."""
    global _PROCESS_CREATION_TICKS
    require(os.name == "nt" and ctypes.sizeof(ctypes.c_void_p) == 8, "Pinned Win64 runtime")
    library = ctypes.WinDLL("kernel32", use_last_error=True)
    library.GetCurrentProcess.argtypes = []
    library.GetCurrentProcess.restype = wintypes.HANDLE
    library.GetProcessTimes.argtypes = [wintypes.HANDLE, *([ctypes.POINTER(wintypes.FILETIME)] * 4)]
    library.GetProcessTimes.restype = wintypes.BOOL
    creation, exit_time, kernel, user = (wintypes.FILETIME() for _ in range(4))
    # GetCurrentProcess returns a pseudo-handle; it must not be closed as an owned handle.
    require(
        library.GetProcessTimes(
            library.GetCurrentProcess(),
            ctypes.byref(creation),
            ctypes.byref(exit_time),
            ctypes.byref(kernel),
            ctypes.byref(user),
        ),
        "Observe actual process creation time",
    )
    ticks = (creation.dwHighDateTime << 32) | creation.dwLowDateTime
    now_ns = time.time_ns()
    age_ns = now_ns - (ticks - 116444736000000000) * 100
    require(age_ns >= 0, "Observed process creation must precede current UTC")
    _PROCESS_CREATION_TICKS = ticks
    return 0.0, time.monotonic() - age_ns / 1_000_000_000


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def same(actual, expected, message):
    require(canonical(actual) == canonical(expected), message)


def read_bytes(path, started):
    """Parse only the bounded bytes whose actual SHA was observed in this invocation."""
    budget(started)
    actual = resolved(path, started)
    identity = stamp(actual)
    require(actual.is_file() and identity[2] <= 128 * 1024**2, "Bounded regular text input")
    state, chunks, total = hashlib.sha256(), [], 0
    with actual.open("rb") as stream:
        while block := stream.read(1 << 20):
            budget(started)
            total += len(block)
            require(total <= identity[2], "Text input grew beyond its observed byte bound")
            state.update(block)
            chunks.append(block)
            budget(started)
    require(stamp(actual) == identity and total == identity[2], "Text bytes changed while reading")
    value, key = state.hexdigest(), str(actual)
    require(
        key not in _OBSERVED or _OBSERVED[key] == value,
        "Parsed bytes contradict previously verified actual SHA",
    )
    _OBSERVED.setdefault(key, value)
    _HASHES[key] = (identity, value)
    data = b"".join(chunks)
    budget(started)
    return data


def read(path, started):
    data = read_bytes(path, started)
    budget(started)
    result = json.loads(data.decode("utf-8"))
    budget(started)
    return result


def save(path, value, started=None):
    if started is not None:
        budget(started)
    content = (json.dumps(value, indent=2, allow_nan=False) + "\n").encode()
    if started is not None:
        budget(started)
    with Path(path).open("xb") as stream:
        for offset in range(0, len(content), 1 << 20):
            if started is not None:
                budget(started)
            stream.write(content[offset : offset + (1 << 20)])
            if started is not None:
                budget(started)


def setup(started):
    global _EXTERNAL_TREES, _EXTERNAL_FILES, _EXTERNAL_ROOT, _EXCLUDED_RUNTIME
    _PATHS.clear()
    _HASHES.clear()
    _OBSERVED.clear()
    require(sys.dont_write_bytecode is True, "Pinned interpreter must start with -B")
    require(Path.cwd().resolve() == ROOT, "Execute module from canonical workspace ROOT")
    require(Path(__file__).resolve() == PRODUCER.resolve(), "Execute exact producer author path")
    for name in ("PYTHONPATH", "PYTHONHOME", "SAGE_ROOT", "MPMATH_SAGE", "NUMBA_CACHE_DIR"):
        require(not os.environ.get(name), "Uncaptured runtime override: " + name)
    os.environ["MPMATH_NOGMPY"] = "1"
    os.environ["MPMATH_NOSAGE"] = "1"
    base = Path(getattr(sys, "_base_executable", sys.executable)).resolve(strict=True)
    prefix = Path(sys.base_prefix).resolve(strict=True)
    excluded = (prefix / "Lib/site-packages").absolute()
    _EXCLUDED_RUNTIME = tuple(dict.fromkeys((excluded, excluded.resolve())))
    _EXTERNAL_ROOT = prefix if not prefix.is_relative_to(ROOT) else None
    require(base.parent == prefix, "Actual base interpreter adjacent to base runtime prefix")
    _EXTERNAL_TREES = tuple(
        path.resolve(strict=True)
        for path in (prefix / "Lib", prefix / "DLLs")
        if path.is_dir() and not path.resolve().is_relative_to(ROOT)
    )
    _EXTERNAL_FILES = tuple(
        path.resolve(strict=True) for path in prefix.iterdir() if path.is_file()
    )
    require(base in _EXTERNAL_FILES or base.is_relative_to(ROOT), "Exact base runtime file scope")
    budget(started)


def reject_unreachable_origin(path, started):
    """Check even vanished module/cache origins before the existence shortcut."""
    budget(started)
    value = Path(path)
    require(not value.drive or value.is_absolute(), "No ambiguous origin drive-relative path")
    for candidate in (value.absolute(), value.resolve(strict=False)):
        require(
            not any(
                candidate == scope or candidate.is_relative_to(scope) for scope in _EXCLUDED_RUNTIME
            ),
            "Unreachable base site-packages origin or alias is forbidden",
        )
    budget(started)


def allowed(path):
    if any(path == scope or path.is_relative_to(scope) for scope in _EXCLUDED_RUNTIME):
        return False
    return (
        path.is_relative_to(ROOT)
        or path == _EXTERNAL_ROOT
        or path in _EXTERNAL_FILES
        or any(path.is_relative_to(scope) for scope in _EXTERNAL_TREES)
    )


def resolved(path, started, fresh=False):
    budget(started)
    value = Path(path)
    require(not value.drive or value.is_absolute(), "No ambiguous drive-relative path")
    require(
        not any(
            value.absolute() == scope or value.absolute().is_relative_to(scope)
            for scope in _EXCLUDED_RUNTIME
        ),
        "Unreachable base site-packages is forbidden",
    )
    lexical = str(value.absolute())
    if not fresh and lexical in _PATHS:
        return _PATHS[lexical]
    actual = value.resolve(strict=True)
    require(allowed(actual), "Path outside ROOT and exact actual base-runtime scopes")
    require(
        not fresh or lexical not in _PATHS or _PATHS[lexical] == actual,
        "Previously confined lexical alias redirected",
    )
    _PATHS[lexical] = actual
    _PATHS.setdefault(str(actual), actual)
    budget(started)
    return actual


def stamp(path):
    value = path.stat()
    return (
        value.st_dev,
        value.st_ino,
        value.st_size,
        value.st_mtime_ns,
        value.st_ctime_ns,
        getattr(value, "st_file_attributes", None),
        getattr(value, "st_reparse_tag", None),
    )


def sha(path, started, fresh=False):
    actual = resolved(path, started, fresh=fresh)
    return digest(actual, started, fresh=fresh)


def digest(actual, started, fresh=False):
    budget(started)
    key, identity = str(actual), stamp(actual)
    if not fresh and key in _HASHES and _HASHES[key][0] == identity:
        budget(started)
        return _HASHES[key][1]
    result = hashlib.sha256()
    with actual.open("rb") as stream:
        while block := stream.read(1 << 20):
            budget(started)
            result.update(block)
            budget(started)
    require(stamp(actual) == identity, "Actual input changed during hashing")
    value = result.hexdigest()
    require(
        key not in _OBSERVED or _OBSERVED[key] == value, "Previously observed actual SHA changed"
    )
    _OBSERVED.setdefault(key, value)
    _HASHES[key] = (identity, value)
    budget(started)
    return value


def relative(path, started):
    return resolved(path, started).relative_to(ROOT).as_posix()


def bind(frozen, external, path, expected, started):
    budget(started)
    require(
        type(expected) is str
        and len(expected) == 64
        and all(character in "0123456789abcdef" for character in expected),
        "Canonical expected SHA256",
    )
    actual = resolved(path, started)
    if actual.is_relative_to(ROOT):
        target, key = frozen, actual.relative_to(ROOT).as_posix()
    else:
        target, key = external, str(actual)
    require(key not in target or target[key] == expected, "Conflicting canonical expected SHA")
    require(sha(actual, started) == expected, "Original expected input SHA mismatch: " + key)
    target[key] = expected
    budget(started)
    return actual


def verify(frozen, external, started):
    for mapping, prefix in ((frozen, ROOT), (external, None)):
        for key, expected in mapping.items():
            budget(started)
            path = prefix / key if prefix is not None else Path(key)
            require(sha(path, started) == expected, "Frozen input changed: " + key)


def final_verify(frozen, external, started):
    for lexical, previous in tuple(_PATHS.items()):
        budget(started)
        require(resolved(lexical, started, fresh=True) == previous, "Fresh lexical alias changed")
    expected = {}
    for mapping, prefix in ((frozen, ROOT), (external, None)):
        for key, value in mapping.items():
            actual = resolved(prefix / key if prefix is not None else key, started)
            require(actual not in expected or expected[actual] == value, "Final equal-SHA merge")
            expected[actual] = value
    observed = {Path(key): value for key, value in _OBSERVED.items()}
    for path in sorted(set(expected) | set(observed)):
        budget(started)
        actual = resolved(path, started, fresh=True)
        value = digest(actual, started, fresh=True)
        require(path not in expected or value == expected[path], "Fresh expected input SHA changed")
        require(
            path not in observed or value == observed[path], "Fresh observed actual SHA changed"
        )
    return len(set(expected) | set(observed))


def forbidden_imports():
    banned = ("numpy", "scipy", "numba", "llvmlite", "qiskit", "gmpy", "gmpy2", "sage")
    found = [
        name
        for name in sys.modules
        if any(name == prefix or name.startswith(prefix + ".") for prefix in banned)
        or (
            name.startswith("research.")
            and name
            not in (
                "research.limitation_program_20261001.experiment_cosine_feasibility",
                "research.limitation_program_20261001",
            )
        )
    ]
    require(
        not found, "No numerical builder, audited code or native backend imports: " + repr(found)
    )


def owner_rows(manifest_path, data, started):
    if "files" in data:
        require(
            type(data["files"]) is dict and type(data.get("frozen_inputs", {})) is dict,
            "Recognized original owner maps",
        )
        require(
            data.get("manifest_self_hash_excluded") is True, "Original nested manifest convention"
        )
        maps = [(field, data.get(field, {})) for field in ("files", "frozen_inputs")]
    else:
        require(
            manifest_path
            in (
                PROGRAM / "A10_coefficient_run001/manifest.json",
                PROGRAM / "A08_run001/attempt002/manifest.json",
            ),
            "Only explicitly pinned A10/A08 historical flat manifests",
        )
        require(
            all(
                type(key) is str and type(value) is str and len(value) == 64
                for key, value in data.items()
            ),
            "Exact original flat SHA map",
        )
        maps = [("flat_owned_files", data)]
    rows = []
    for field, mapping in maps:
        for original, expected in mapping.items():
            budget(started)
            normalized = original.replace("\\", "/")
            require(
                not Path(normalized).is_absolute()
                and not any(part in (".", "..") for part in normalized.split("/")),
                "Original ROOT/receipt-relative canonical member key",
            )
            candidate = (
                ROOT / normalized
                if normalized.startswith(
                    ("results/", "research/", "docs/", "manuscript/", ".context/")
                )
                else manifest_path.parent / normalized
            )
            actual = resolved(candidate, started)
            budget(started)
            require(actual.is_relative_to(ROOT), "Original owner membership ROOT confinement")
            rows.append((field, actual, original, expected))
    return rows


def runtime_candidates(root, started):
    """Prune the explicitly unreachable base site subtree before enumeration."""
    root = resolved(root, started)
    if root.is_file():
        yield root
        return
    require(root.is_dir(), "Actual runtime inventory root")
    pending, seen = [root], set()
    while pending:
        budget(started)
        current = pending.pop()
        require(current not in seen, "No aliased or recursive runtime directory")
        seen.add(current)
        for candidate in current.iterdir():
            budget(started)
            if any(candidate.absolute() == scope for scope in _EXCLUDED_RUNTIME):
                continue
            actual = resolved(candidate, started)
            require(actual.is_relative_to(root), "Runtime tree alias escaped its exact root")
            if actual.is_dir():
                pending.append(actual)
            elif actual.is_file():
                yield actual


def bootstrap_runtime_paths(site_root, started):
    """Actual startup hooks and loaded venv bytes, without admitting other packages."""
    paths = []
    for path in site_root.iterdir():
        budget(started)
        customize_name = path.name.split(".", 1)[0] in ("sitecustomize", "usercustomize")
        is_hook = path.is_file() and (
            path.suffix.lower() == ".pth"
            or customize_name
            and path.suffix.lower() in (".py", ".pyc", ".pyd")
        )
        is_package = path.is_dir() and path.name in ("sitecustomize", "usercustomize")
        if is_hook or is_package:
            actual_hook = resolved(path, started)
            require(
                actual_hook.is_relative_to(site_root),
                "Startup hook must stay in actual isolated venv",
            )
            paths.append(actual_hook)
            if path.suffix == ".py":
                cached = Path(cache_from_source(str(path)))
                if cached.is_file():
                    actual_cache = resolved(cached, started)
                    require(
                        actual_cache.is_relative_to(site_root), "Startup hook cache confinement"
                    )
                    paths.append(actual_cache)
    for name, module in tuple(sys.modules.items()):
        budget(started)
        if module is None:
            continue
        for origin in (getattr(module, "__file__", None), getattr(module, "__cached__", None)):
            if origin:
                reject_unreachable_origin(origin, started)
            if origin and Path(origin).is_file():
                actual = resolved(origin, started)
                if Path(origin).absolute().is_relative_to(site_root):
                    require(
                        actual.is_relative_to(site_root),
                        "Loaded bootstrap alias escaped actual isolated venv",
                    )
                if actual.is_relative_to(site_root) and not actual.is_relative_to(
                    site_root / "mpmath"
                ):
                    paths.append(actual)
    return sorted(set(paths))


def venv_adjacent_runtime_paths(prefix, started):
    """Record the exact admitted venv-root directory and its importable adjacent bytes."""
    paths, membership = [], []
    for candidate in prefix.iterdir():
        budget(started)
        actual = resolved(candidate, started)
        require(
            actual.parent == prefix and actual.name == candidate.name,
            "Actual venv-root member must remain directly confined without an alias",
        )
        if actual.is_file():
            membership.append([candidate.name, "file"])
            paths.append(actual)
        elif actual.is_dir():
            membership.append([candidate.name, "directory"])
            # Lib and Scripts have their separately declared complete reachable inventories.
            # A directly importable package or adjacent cache is not covered by that scope.
            if actual.name == "__pycache__" or any(
                (actual / name).is_file() for name in ("__init__.py", "__init__.pyc")
            ):
                require(actual.name not in ("Lib", "Scripts"), "No ambiguous venv package root")
                paths.append(actual)
        else:
            require(False, "Only regular file/directory venv-root members")
    return sorted(set(paths)), sorted(membership)


def inventory(paths, frozen, external, started):
    """Freeze actual directory contents, including existing caches, not RECORD alone."""
    files, total = {}, 0
    for root in paths:
        budget(started)
        root = resolved(root, started)
        candidates = runtime_candidates(root, started)
        for candidate in candidates:
            budget(started)
            if not candidate.is_file():
                continue
            path = resolved(candidate, started)
            require(path == root or path.is_relative_to(root), "Runtime directory escape")
            if path in files:
                continue
            total += path.stat().st_size
            require(len(files) < MAX_RUNTIME_FILES and total <= MAX_RUNTIME_BYTES, "Runtime cap")
            expected = sha(path, started)
            bind(frozen, external, path, expected, started)
            files[path] = expected
    return dict(
        files=len(files),
        bytes=total,
        roots=[str(path) for path in paths],
        actual_file_paths=sorted(str(path) for path in files),
    )


def runtime(frozen, external, started):
    prefix = resolved(sys.prefix, started)
    require(prefix == ROOT / ".context/frontier_t0_env", "Pinned isolated venv")
    require(resolved(sys.executable, started) == LAUNCHER, "Actual launcher provenance")
    require(site.ENABLE_USER_SITE is False, "User site disabled")
    config = prefix / "pyvenv.cfg"
    require(
        "include-system-site-packages = false" in read_bytes(config, started).decode().lower(),
        "Isolated venv",
    )
    site_root = resolved(prefix / "Lib/site-packages", started)
    distribution = metadata.distribution("mpmath")
    require(distribution.version == "1.3.0", "Fixed installed mpmath version")
    members = distribution.files
    require(members, "Nonempty mpmath installed metadata inventory")
    metadata_roots = set()
    for member in members:
        budget(started)
        path = resolved(distribution.locate_file(member), started)
        for parent in (path, *path.parents):
            if parent.name.endswith(".dist-info"):
                metadata_roots.add(parent)
                break
    require(len(metadata_roots) == 1, "Exactly one mpmath distribution metadata root")
    metadata_root = next(iter(metadata_roots))
    require(metadata_root.parent == site_root, "Confined actual distribution metadata")
    base_prefix = resolved(sys.base_prefix, started)
    roots = [
        config,
        prefix / "Scripts",
        site_root / "mpmath",
        metadata_root,
        base_prefix / "Lib",
        base_prefix / "DLLs",
        *_EXTERNAL_FILES,
    ]
    bootstrap_paths = bootstrap_runtime_paths(site_root, started)
    roots.extend(bootstrap_paths)
    adjacent_paths, adjacent_membership = venv_adjacent_runtime_paths(prefix, started)
    roots.extend(adjacent_paths)
    for source in (ROOT / "research/__init__.py", RESEARCH / "__init__.py"):
        if source.is_file():
            roots.append(source)
            cached = Path(cache_from_source(str(source)))
            if cached.is_file():
                roots.append(cached)
    # Existing producer/auditor bytecode is captured even though startup -B prevents writes.
    for source in (PRODUCER, AUDITOR):
        cached = Path(cache_from_source(str(source)))
        if cached.is_file():
            roots.append(cached)
    counts = inventory([path for path in roots if path.exists()], frozen, external, started)
    allowed_import_roots = (
        ROOT,
        prefix,
        site_root,
        base_prefix,
        base_prefix / "Lib",
        base_prefix / "DLLs",
    )
    absent = []
    for entry in sys.path:
        budget(started)
        candidate = Path(entry or ROOT)
        reject_unreachable_origin(candidate, started)
        if not candidate.exists():
            actual = candidate.resolve()
            expected_zip = base_prefix / (
                "python" + str(sys.version_info.major) + str(sys.version_info.minor) + ".zip"
            )
            require(actual == expected_zip, "Only standard absent interpreter zip path")
            absent.append(str(actual))
            continue
        path = resolved(entry or ROOT, started)
        require(
            path in _EXTERNAL_FILES or any(path == root for root in allowed_import_roots),
            "Unexpected sys.path entry: " + str(path),
        )
    return dict(
        python_version=sys.version,
        executable=str(resolved(sys.executable, started)),
        base_executable=str(resolved(sys._base_executable, started)),
        base_prefix=str(base_prefix),
        venv_prefix=str(prefix),
        mpmath_version=distribution.version,
        backend="python",
        MPMATH_NOGMPY="1",
        MPMATH_NOSAGE="1",
        startup_bytecode_disabled=True,
        user_site_disabled=True,
        runtime_inventory=counts,
        sys_path=list(sys.path),
        external_runtime_trees=[str(path) for path in _EXTERNAL_TREES],
        external_adjacent_files=[str(path) for path in _EXTERNAL_FILES],
        absent_standard_runtime_paths=absent,
        excluded_base_site_packages=str((Path(sys.base_prefix) / "Lib/site-packages").resolve()),
        excluded_base_site_packages_lexical=str(
            (Path(sys.base_prefix) / "Lib/site-packages").absolute()
        ),
        base_site_packages_import_rejected=True,
        bootstrap_hook_and_loaded_venv_paths=[str(path) for path in bootstrap_paths],
        standard_Lib_excludes_only_unreachable_base_site_packages=True,
        other_installed_venv_packages_not_blanket_admitted=True,
        exact_sys_prefix_search_path_admitted=True,
        venv_adjacent_runtime_paths=[str(path) for path in adjacent_paths],
        venv_root_directory_membership=adjacent_membership,
    )


def runtime_policy(record, started):
    budget(started)
    require(sys.version == record["python_version"], "Actual recorded interpreter version")
    require(
        str(resolved(sys.executable, started)) == record["executable"], "Actual recorded launcher"
    )
    require(
        str(resolved(sys._base_executable, started)) == record["base_executable"],
        "Actual base interpreter",
    )
    require(str(resolved(sys.base_prefix, started)) == record["base_prefix"], "Actual base prefix")
    require(
        str(resolved(sys.prefix, started)) == record["venv_prefix"], "Actual isolated venv prefix"
    )
    same(list(sys.path), record["sys_path"], "Unchanged actual interpreter search paths")
    require(
        record["excluded_base_site_packages"]
        == str((Path(sys.base_prefix) / "Lib/site-packages").resolve())
        and record["excluded_base_site_packages_lexical"]
        == str((Path(sys.base_prefix) / "Lib/site-packages").absolute())
        and record["base_site_packages_import_rejected"] is True,
        "Exact explicitly unreachable runtime scope",
    )
    require(
        record["standard_Lib_excludes_only_unreachable_base_site_packages"] is True
        and record["other_installed_venv_packages_not_blanket_admitted"] is True,
        "Explicit reachable-runtime operational policy",
    )
    site_root = resolved(Path(sys.prefix) / "Lib/site-packages", started)
    adjacent_paths, adjacent_membership = venv_adjacent_runtime_paths(
        resolved(sys.prefix, started), started
    )
    require(
        record["exact_sys_prefix_search_path_admitted"] is True,
        "Exact Windows venv-prefix search path policy",
    )
    same(
        [str(path) for path in adjacent_paths],
        record["venv_adjacent_runtime_paths"],
        "Actual adjacent venv runtime byte roots unchanged",
    )
    same(
        adjacent_membership,
        record["venv_root_directory_membership"],
        "Exact finite venv-root directory membership unchanged",
    )
    same(
        [str(path) for path in bootstrap_runtime_paths(site_root, started)],
        record["bootstrap_hook_and_loaded_venv_paths"],
        "Exact actual startup hook membership",
    )
    for entry in sys.path:
        budget(started)
        path = Path(entry or ROOT)
        reject_unreachable_origin(path, started)
        if path.exists():
            resolved(path, started)
    same(
        [str(path) for path in _EXTERNAL_TREES],
        record["external_runtime_trees"],
        "Exact external tree scope",
    )
    same(
        [str(path) for path in _EXTERNAL_FILES],
        record["external_adjacent_files"],
        "Exact adjacent runtime scope",
    )
    require(
        site.ENABLE_USER_SITE is False and sys.dont_write_bytecode is True, "Isolated startup -B"
    )
    require(
        metadata.version("mpmath") == record["mpmath_version"] == "1.3.0", "Fixed runtime metadata"
    )
    for path in record["absent_standard_runtime_paths"]:
        budget(started)
        require(not Path(path).exists(), "Previously absent interpreter zip path appeared")
    require(
        os.environ.get("MPMATH_NOGMPY") == os.environ.get("MPMATH_NOSAGE") == "1",
        "Pure Python backend policy",
    )
    actual_files = set()
    for name in record["runtime_inventory"]["roots"]:
        root = resolved(name, started)
        for candidate in runtime_candidates(root, started):
            budget(started)
            if candidate.is_file():
                actual = resolved(candidate, started)
                require(
                    actual == root or actual.is_relative_to(root), "Runtime inventory scope escape"
                )
                actual_files.add(str(actual))
    same(
        sorted(actual_files),
        record["runtime_inventory"]["actual_file_paths"],
        "Complete runtime byte inventory membership unchanged",
    )
    forbidden_imports()


def verify_loaded(frozen, external, started):
    forbidden_imports()
    observed = []
    for name, module in tuple(sys.modules.items()):
        budget(started)
        if module is None:
            continue
        origin = getattr(module, "__file__", None)
        for field, value in (("source", origin), ("cache", getattr(module, "__cached__", None))):
            if value:
                reject_unreachable_origin(value, started)
            if not value or not Path(value).is_file():
                continue
            path = resolved(value, started)
            key = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)
            mapping = frozen if path.is_relative_to(ROOT) else external
            require(key in mapping, "Loaded module byte origin not frozen: " + name + ":" + key)
            require(sha(path, started) == mapping[key], "Loaded module origin changed")
            observed.append(dict(module=name, kind=field, path=key, sha256=mapping[key]))
    return observed


def copy_exact(source, destination, frozen, external, started):
    budget(started)
    expected = sha(source, started)
    with Path(source).open("rb") as incoming, Path(destination).open("xb") as outgoing:
        while block := incoming.read(1 << 20):
            budget(started)
            outgoing.write(block)
            budget(started)
    require(sha(destination, started) == expected, "Exclusive immutable copy equality")
    bind(frozen, external, destination, expected, started)


def elapsed(started):
    return dict(
        process_CPU_seconds=time.process_time() - started[0],
        wall_seconds=time.monotonic() - started[1],
    )


def owned_files(output, started):
    files, total = {}, 0
    for path in output.rglob("*"):
        budget(started)
        if not path.is_file():
            continue
        require(path.name != "manifest.json", "No terminal/partial manifest reuse")
        require(resolved(path, started).is_relative_to(output), "Owned output confinement")
        total += path.stat().st_size
        require(len(files) < 64 and total <= 128 * 1024**2, "Finite owned artifacts cap")
        files[path.relative_to(output).as_posix()] = sha(path, started)
    return files


class ActualGraph:
    """Read-only typed actual SSA matching; never builds or evaluates a Graph."""

    def __init__(self, target, started):
        self.started, self.target, self.nodes = started, target, {}
        require(target["width"] == W and target["fraction_bits"] == 40, "Actual native W72/F40")
        arities = dict(
            input=0,
            const=0,
            bits=1,
            add=2,
            sub=2,
            mul=2,
            cmul=1,
            lt=2,
            select=3,
            msb=1,
            shift=2,
            positive=1,
            sqrt=1,
            lookup=1,
        )
        for node in target["nodes"]:
            budget(started)
            op, args, outputs, params = (node[key] for key in ("op", "args", "out", "params"))
            require(
                op in arities and type(args) is list and len(args) == arities[op], "Typed op/arity"
            )
            require(type(params) is dict and type(outputs) is list and outputs, "Typed node fields")
            require(
                all(type(value) is int and value in self.nodes for value in args),
                "Topological inputs",
            )
            require(
                all(
                    type(value) is int and value >= 0 and value not in self.nodes
                    for value in outputs
                ),
                "Unique SSA IDs",
            )
            require(len(set(outputs)) == len(outputs), "Unique multioutput SSA IDs")
            if op != "lookup":
                require(len(outputs) == 1, "Single output operation")
            if op in ("input", "bits", "lookup"):
                require(type(params.get("bits", params.get("width"))) is int, "Integer width field")
            if op == "bits":
                require(
                    type(params.get("shift")) is int and type(params.get("signed")) is bool,
                    "Typed bit shift",
                )
            if op in ("const", "cmul"):
                raw = params["value" if op == "const" else "c"]
                require(
                    set(params) == {"value" if op == "const" else "c"},
                    "Exact native literal parameter keys",
                )
                require(type(raw) is int, "Native literals are JSON ints, never flags")
                require(
                    0 <= raw < (1 << 72) if op == "const" else -(1 << 71) <= raw < (1 << 71),
                    "Const unsigned72/cmul signed72 canonical representations",
                )
                literal(raw)
            if op not in ("input", "const", "cmul", "bits", "lookup"):
                require(params == {}, "Exact arithmetic parameters")
            for value in outputs:
                self.nodes[value] = node
        require(set(self.nodes) == set(range(len(self.nodes))), "Contiguous actual SSA inventory")

    def node(self, value, op=None, params=None):
        budget(self.started)
        require(type(value) is int and value in self.nodes, "Actual SSA value identity")
        node = self.nodes[value]
        require(op is None or node["op"] == op, "Expected actual operation: " + str(value))
        if params is not None:
            same(node["params"], params, "Exact actual operation parameters")
        return node

    def const(self, value, raw=None):
        actual = literal(self.node(value, "const")["params"]["value"])
        require(raw is None or actual == raw, "Exact constant literal")
        return actual

    def clip(self, value, low=None, high=None):
        flag, middle, hi = self.node(value, "select")["args"]
        require(self.node(flag, "lt")["args"] == [middle, hi], "Upper clamp structure")
        lo_flag, lo, raw = self.node(middle, "select")["args"]
        require(self.node(lo_flag, "lt")["args"] == [raw, lo], "Lower clamp structure")
        lower, upper = self.const(lo, low), self.const(hi, high)
        require(lower < upper, "Ordered literal clamp")
        return raw

    def midpoint(self, value, input_id):
        args = self.node(value, "add")["args"]
        shifts = [arg for arg in args if self.node(arg)["op"] == "bits"]
        require(len(shifts) == 1, "Exact midpoint shift")
        shift = shifts[0]
        require(
            self.node(shift, "bits", dict(shift=-8, width=72, signed=False))["args"] == [input_id],
            "Midpoint raw input",
        )
        self.const(next(arg for arg in args if arg != shift), 128)

    def ancestors(self, value):
        found, pending = set(), [value]
        while pending:
            budget(self.started)
            current = pending.pop()
            if current not in found:
                found.add(current)
                pending.extend(self.node(current)["args"])
        return found

    def interpolation(self, value, name, argument):
        segments, degree, lo, index_bits = (32, 8, Q, 5) if name == "log" else (64, 7, 0, 6)
        candidates = {
            tuple(self.node(v)["out"])
            for v in self.ancestors(value)
            if self.node(v)["op"] == "lookup" and self.node(v)["params"]["table"] == name
        }
        require(len(candidates) == 1, "One actual interpolation lookup")
        outputs = next(iter(candidates))
        lookup = self.node(outputs[0], "lookup", dict(table=name, bits=index_bits))
        require(len(outputs) == degree + 1, "Complete actual Horner coefficient outputs")
        index = lookup["args"][0]
        address = self.node(
            index, "bits", dict(shift=40 - index_bits, width=index_bits, signed=False)
        )["args"][0]
        if lo:
            address, lower = self.node(address, "sub")["args"]
            self.const(lower, lo)
        bounded = address
        require(self.clip(bounded, lo, lo + Q - 1) == argument, "Actual interpolation domain")
        current, local = value, None
        for j in range(degree):
            args = self.node(current, "add")["args"]
            require(outputs[j] in args, "Actual Horner coefficient ordering")
            product = next(arg for arg in args if arg != outputs[j])
            factors = self.node(product, "mul")["args"]
            if local is None:
                possible = [v for v in factors if self.node(v)["op"] == "sub"]
                require(len(possible) == 1, "Unique Horner local coordinate")
                local = possible[0]
            require(local in factors, "Every actual Horner multiplication uses local")
            current = next(arg for arg in factors if arg != local)
        require(current == outputs[-1], "Actual Horner degree8/7 terminal coefficient")
        actual_x, center = self.node(local, "sub")["args"]
        require(actual_x == bounded, "Actual local-coordinate input")
        args = self.node(center, "add")["args"]
        shifts = [v for v in args if self.node(v)["op"] == "bits"]
        require(len(shifts) == 1, "Actual segment center shift")
        shift = shifts[0]
        require(
            self.node(shift, "bits", dict(shift=index_bits - 40, width=72, signed=False))["args"]
            == [index],
            "Actual center address",
        )
        self.const(next(v for v in args if v != shift), lo + Q // (2 * segments))
        return dict(
            output=value,
            input=argument,
            address=index,
            local=local,
            lookup_outputs=list(outputs),
            floors=degree,
        )

    def pair(self, roots, raw_u, raw_v, ln2):
        require(len(roots) == 2, "One original joint pair")
        factors = [self.node(value, "mul")["args"] for value in roots]
        common = set(factors[0]) & set(factors[1])
        require(len(common) == 1, "Exactly one shared actual radius")
        radius = next(iter(common))
        positive = self.node(radius, "sqrt")["args"][0]
        negative_two = self.node(positive, "positive")["args"][0]
        log_value = self.node(negative_two, "cmul", dict(c=-2 * Q))["args"][0]
        log_args = self.node(log_value, "add")["args"]
        terms = [v for v in log_args if self.node(v)["op"] == "cmul"]
        require(len(terms) == 1, "Unique exponent-ln2 product")
        term = terms[0]
        scaled = self.node(term, "cmul", dict(c=ln2))["args"][0]
        exponent = self.node(scaled, "bits", dict(shift=-40, width=72, signed=False))["args"][0]
        top, fraction = self.node(exponent, "sub")["args"]
        self.const(fraction, 40)
        safe = self.node(top, "msb")["args"][0]
        flag, tiny, mid_u = self.node(safe, "select")["args"]
        self.const(tiny, 1)
        require(self.node(flag, "lt")["args"] == [mid_u, tiny], "Actual safe positive log input")
        self.midpoint(mid_u, raw_u)
        poly = next(v for v in log_args if v != term)
        lookups = [self.node(v) for v in self.ancestors(poly) if self.node(v)["op"] == "lookup"]
        require(len({tuple(node["out"]) for node in lookups}) == 1, "Unique log lookup")
        index = lookups[0]["args"][0]
        address = self.node(index)["args"][0]
        clipped = self.node(address, "sub")["args"][0]
        mantissa = self.clip(clipped, Q, 2 * Q - 1)
        u, negated = self.node(mantissa, "shift")["args"]
        require(u == safe, "Actual mantissa normalized from safe midpoint")
        zero, actual_exponent = self.node(negated, "sub")["args"]
        self.const(zero, 0)
        require(actual_exponent == exponent, "Actual left-shift exponent")
        log_scope = self.interpolation(poly, "log", mantissa)
        cosines = [next(v for v in row if v != radius) for row in factors]
        arguments = []
        for cosine in cosines:
            lookup = [
                self.node(v) for v in self.ancestors(cosine) if self.node(v)["op"] == "lookup"
            ]
            require(len({tuple(node["out"]) for node in lookup}) == 1, "Unique cosine lookup")
            clip = self.node(lookup[0]["args"][0])["args"][0]
            arguments.append(self.clip(clip, 0, Q - 1))
        mid_v, quarter = arguments
        self.midpoint(mid_v, raw_v)
        wrapped = self.node(quarter, "bits", dict(shift=0, width=40, signed=False))["args"][0]
        args = self.node(wrapped, "add")["args"]
        require(mid_v in args, "Positive sine convention uses same midpoint")
        self.const(next(v for v in args if v != mid_v), 3 * Q // 4)
        scopes = [self.interpolation(v, "cos", a) for v, a in zip(cosines, arguments, strict=True)]
        inputs = {
            v for root in roots for v in self.ancestors(root) if self.node(v)["op"] == "input"
        }
        require(inputs == {raw_u, raw_v}, "Original pair input closure")
        return dict(
            normal_values=list(roots),
            raw_uniform_values=[raw_u, raw_v],
            radius=radius,
            log=log_scope,
            cosines=scopes,
            original_shared_pair_preserved=True,
        )

    def flatten(self, value, stops, op="add"):
        result, pending = Counter(), [value]
        while pending:
            budget(self.started)
            current = pending.pop()
            if current in stops:
                result[current] += 1
            else:
                pending.extend(self.node(current, op)["args"])
        return result

    def maxima(self, value, stops):
        result, pending = Counter(), [value]
        while pending:
            current = pending.pop()
            if current in stops:
                result[current] += 1
                continue
            flag, hi, lo = self.node(current, "select")["args"]
            require(self.node(flag, "lt")["args"] == [lo, hi], "Exact basket maximum tree")
            pending.extend((lo, hi))
        return result


class CleanRecipe:
    """Finite full72 SSA recipe; every noninput bank survives until literal inverse."""

    def __init__(self, row_id, started):
        self.row_id, self.started, self.nodes, self.constants = row_id, started, [], {}
        self.next_bank = 0
        self.input = self.emit("INPUT", fraction_bits=F)

    def emit(self, op, args=(), params=None, count=1, fraction_bits=None):
        tick(self.started)
        require(
            all(type(value) is int and 0 <= value < self.next_bank for value in args),
            "Recipe topology",
        )
        outputs = list(range(self.next_bank, self.next_bank + count))
        self.next_bank += count
        self.nodes.append(
            dict(
                op=op,
                args=list(args),
                params={} if params is None else params,
                outputs=outputs,
                fraction_bits=fraction_bits,
            )
        )
        return outputs[0] if count == 1 else outputs

    def constant(self, raw, scale):
        signed_word(raw)
        key = raw, scale
        if key not in self.constants:
            self.constants[key] = self.emit("CONST", params=dict(raw=raw), fraction_bits=scale)
        return self.constants[key]

    def bits(self, value, kind, amount=0, width=W, scale=0):
        require(kind in ("left", "signed_right", "unsigned_right", "low"), "Fixed bit-copy family")
        require(
            type(amount) is int and 0 <= amount <= 71 and 1 <= width <= W, "Finite bit-copy map"
        )
        mapping = []
        for index in range(W):
            if kind == "left":
                source = index - amount
                source = source if 0 <= source < W else None
            elif kind == "signed_right":
                source = min(index + amount, W - 1)
            elif kind == "unsigned_right":
                source = index + amount if index < width and index + amount < W else None
            else:
                source = index if index < width else None
            mapping.append(source)
        return self.emit(
            "BITS",
            [value],
            dict(kind=kind, amount=amount, width=width, output_to_input_bit=mapping),
            fraction_bits=scale,
        )

    def arithmetic(self, op, first, second, scale):
        require(op in ("ADD", "SUB", "MUL"), "Fixed unconditional arithmetic")
        return self.emit(op, [first, second], fraction_bits=scale)

    def flag(self, op, first, second):
        require(op in ("LT", "EQ", "FLAG_AND", "FLAG_OR"), "Fixed full72 flag bank")
        return self.emit(op, [first, second], fraction_bits=0)

    def select(self, flag, first, second, scale):
        return self.emit("SELECT", [flag, first, second], fraction_bits=scale)

    def clamp(self, value, low, high, scale):
        lo, hi = self.constant(low, scale), self.constant(high, scale)
        low_flag = self.flag("LT", value, lo)
        middle = self.select(low_flag, lo, value, scale)
        high_flag = self.flag("LT", hi, middle)
        return self.select(high_flag, hi, middle, scale)

    def axes(self, m, value):
        for raw, result in zip((0, Q // 4, Q // 2, 3 * Q // 4, Q), (Q, 0, -Q, 0, Q), strict=True):
            flag = self.flag("EQ", m, self.constant(raw, F))
            value = self.select(flag, self.constant(result, F), value, F)
        return value

    def finish(self, output):
        return dict(
            schema="a14-clean-cosine-typed-plan-v1",
            row_id=self.row_id,
            word_width=W,
            external_fraction_bits=F,
            input_bank=self.input,
            output_bank=output,
            allocated_full72_banks=self.next_bank,
            nodes=self.nodes,
            constant_deduplication="exact raw and fractional scale",
            all_eager_values_retained=True,
            output_XOR_bits=W,
            clean_recipe="literal F; XOR72 output; literal reversed F",
            historical_graph_or_gate_builder_used=False,
        )


def cordic_plan(literals, started):
    recipe = CleanRecipe(ROWS[0], started)
    m = recipe.clamp(recipe.input, 0, Q, F)
    doubled_twice = recipe.bits(m, "left", amount=2, scale=F)
    nearest = recipe.arithmetic("ADD", doubled_twice, recipe.constant(Q // 2, F), F)
    quarter = recipe.bits(nearest, "unsigned_right", amount=40, width=3)
    residue = recipe.arithmetic(
        "SUB",
        recipe.bits(m, "left", amount=16, scale=CF),
        recipe.bits(quarter, "left", amount=54, scale=CF),
        CF,
    )
    zero = recipe.constant(0, CF)
    x, y, z = recipe.constant(literals["gain_reciprocal"]["raw"], CF), zero, residue
    for row in literals["angle_rows"]:
        tick(started)
        i, angle = row["i"], recipe.constant(row["raw"], CF)
        sx, sy = (
            recipe.bits(x, "signed_right", amount=i, scale=CF),
            recipe.bits(y, "signed_right", amount=i, scale=CF),
        )
        negative = recipe.flag("LT", z, zero)
        xp = recipe.arithmetic("SUB", x, sy, CF)
        xm = recipe.arithmetic("ADD", x, sy, CF)
        yp = recipe.arithmetic("ADD", y, sx, CF)
        ym = recipe.arithmetic("SUB", y, sx, CF)
        zp = recipe.arithmetic("SUB", z, angle, CF)
        zm = recipe.arithmetic("ADD", z, angle, CF)
        x, y, z = (recipe.select(negative, a, b, CF) for a, b in ((xm, xp), (ym, yp), (zm, zp)))
    quadrant = recipe.bits(quarter, "low", width=2)
    minus_x, minus_y = recipe.arithmetic("SUB", zero, x, CF), recipe.arithmetic("SUB", zero, y, CF)
    chosen = y
    for raw, value in ((2, minus_x), (1, minus_y), (0, x)):
        chosen = recipe.select(
            recipe.flag("EQ", quadrant, recipe.constant(raw, 0)), value, chosen, CF
        )
    quotient = recipe.bits(chosen, "signed_right", amount=16, scale=F)
    remainder = recipe.bits(chosen, "low", width=16)
    halfway = recipe.constant(1 << 15, 0)
    above, tied = recipe.flag("LT", halfway, remainder), recipe.flag("EQ", remainder, halfway)
    odd = recipe.bits(quotient, "low", width=1)
    increment = recipe.flag("FLAG_OR", above, recipe.flag("FLAG_AND", tied, odd))
    rounded = recipe.arithmetic("ADD", quotient, increment, F)
    return recipe.finish(recipe.axes(m, recipe.clamp(rounded, -Q, Q, F)))


def taylor_plan(literals, started):
    recipe = CleanRecipe(ROWS[1], started)
    m = recipe.clamp(recipe.input, 0, Q, F)
    endpoint = recipe.flag("EQ", m, recipe.constant(Q, F))
    m0 = recipe.select(endpoint, recipe.constant(0, F), m, F)
    address = recipe.bits(m0, "unsigned_right", amount=34, width=6)
    table = [
        [(2 * index + 1) << 33]
        + [row["raw"] for row in literals["coefficient_rows"] if row["segment"] == index]
        for index in range(64)
    ]
    require(all(len(row) == 8 for row in table), "Center plus seven exact coefficient words")
    values = recipe.emit(
        "LOOKUP",
        [address],
        dict(
            bits=6,
            table=table,
            recipe="negative controls; five-chain CCX; literal CX; inverse chain; restore",
        ),
        count=8,
        fraction_bits=F,
    )
    center, *coefficients = values
    local = recipe.arithmetic("SUB", m0, center, F)
    accumulator = coefficients[-1]
    for coefficient in reversed(coefficients[:-1]):
        product = recipe.arithmetic("MUL", accumulator, local, F)
        accumulator = recipe.arithmetic("ADD", product, coefficient, F)
    return recipe.finish(recipe.axes(m, recipe.clamp(accumulator, -Q, Q, F)))


def plan_native_safety(plan, started):
    """Exact interval induction with LT branch restrictions for the public clamps."""
    bounds, defining, report = {}, {}, []
    for node in plan["nodes"]:
        tick(started)
        op, args, params = node["op"], node["args"], node["params"]
        incoming = [bounds[value] for value in args]
        product_bounds = None
        if op == "INPUT":
            outgoing = [(-(1 << 71), (1 << 71) - 1)]
        elif op == "CONST":
            outgoing = [(params["raw"], params["raw"])]
        elif op == "ADD":
            outgoing = [(incoming[0][0] + incoming[1][0], incoming[0][1] + incoming[1][1])]
        elif op == "SUB":
            outgoing = [(incoming[0][0] - incoming[1][1], incoming[0][1] - incoming[1][0])]
        elif op == "MUL":
            products = [a * b for a in incoming[0] for b in incoming[1]]
            product_bounds = min(products), max(products)
            require(
                -(1 << 143) <= product_bounds[0] <= product_bounds[1] < 1 << 143,
                "Every signed144 product",
            )
            outgoing = [(product_bounds[0] // Q, product_bounds[1] // Q)]
        elif op in ("LT", "EQ", "FLAG_AND", "FLAG_OR"):
            if op.startswith("FLAG"):
                require(all(0 <= lo <= hi <= 1 for lo, hi in incoming), "Boolean LSB flags")
            outgoing = [(0, 1)]
        elif op == "SELECT":
            require(0 <= incoming[0][0] <= incoming[0][1] <= 1, "Clean SELECT flag ABI")
            first, second = incoming[1], incoming[2]
            condition = defining[args[0]]
            if condition["op"] == "LT":
                left, right = condition["args"]
                left_bound, right_bound = bounds[left], bounds[right]
                if args[1] == left:
                    first = first[0], min(first[1], right_bound[1] - 1)
                if args[1] == right:
                    first = max(first[0], left_bound[0] + 1), first[1]
                if args[2] == left:
                    second = max(second[0], right_bound[0]), second[1]
                if args[2] == right:
                    second = second[0], min(second[1], left_bound[1])
            elif condition["op"] == "EQ":
                left, right = condition["args"]
                for value, other in ((left, right), (right, left)):
                    fixed = bounds[other]
                    if fixed[0] != fixed[1]:
                        continue
                    point = fixed[0]
                    if args[1] == value:
                        first = max(first[0], point), min(first[1], point)
                    if args[2] == value:
                        second = (
                            second[0] + int(second[0] == point),
                            second[1] - int(second[1] == point),
                        )
            choices = [pair for pair in (first, second) if pair[0] <= pair[1]]
            require(choices, "Nonempty sound SELECT branch union")
            outgoing = [(min(pair[0] for pair in choices), max(pair[1] for pair in choices))]
        elif op == "BITS":
            kind, amount, width = params["kind"], params["amount"], params["width"]
            lo, hi = incoming[0]
            if kind == "left":
                outgoing = [(lo << amount, hi << amount)]
            elif kind == "signed_right":
                outgoing = [(lo >> amount, hi >> amount)]
            elif kind == "unsigned_right":
                require(lo >= 0 and hi >> amount < 1 << width, "No dropped live high address bits")
                outgoing = [(lo >> amount, hi >> amount)]
            else:
                outgoing = [(0, (1 << width) - 1)]
        elif op == "LOOKUP":
            require(
                incoming[0][0] >= 0 and incoming[0][1] < 64, "Endpoint mapped before eager lookup"
            )
            table = params["table"]
            outgoing = [
                (min(row[index] for row in table), max(row[index] for row in table))
                for index in range(8)
            ]
        else:
            raise ValueError("Unsupported declared operation")
        for value, pair in zip(node["outputs"], outgoing, strict=True):
            bounds[value] = native_range(tuple(pair))
            defining[value] = node
        report.append(
            dict(
                outputs=node["outputs"],
                op=op,
                signed72_bounds=[list(pair) for pair in outgoing],
                signed144_product_bounds=None if product_bounds is None else list(product_bounds),
            )
        )
    final = bounds[plan["output_bank"]]
    require(-Q <= final[0] <= final[1] <= Q, "Full public output saturation")
    return dict(
        schema="a14-complete-recipe-native-safety-v1",
        row_id=plan["row_id"],
        complete_plan_checked=True,
        every_eager_selected_and_unselected_value_retained=True,
        actual_signed72_inputs_clamped_before_folding=True,
        exact_endpoint_lookup_Q_to_zero=True,
        all_signed72_outputs_and_signed144_products_safe=True,
        output_bound=list(final),
        full72_bank_count=plan["allocated_full72_banks"],
        rows=report,
        discarded_shift_inputs_preserved_by_SSA=True,
        literal_reverse_restores_every_bank=True,
        full_G2=False,
        adoption=False,
    )


RESOURCE_FIELDS = (
    "source_gates",
    "x",
    "cx",
    "ccx",
    "t_count",
    "t_depth",
    "clifford_t_depth",
    "clifford_cx",
    "clifford_h",
)
CASES = {"B4x12": (4, 12, 30), "B8x52": (8, 52, 234)}
BASELINE = {"B4x12": (520720662, 555774, 550141), "B8x52": (4267435214, 663704, 4460479)}
BRIDGE = PROGRAM / "A02_BM_native_financial_bridge_run002"
BRIDGE_AUDIT = PROGRAM / "A02_BM_native_financial_bridge_audit_run002"
PHASE_PROOF = PROGRAM / "A17_quantile_divider_run001/exact_CCX_phase_proof.json"
PHASE_SOURCE = RESEARCH / "temporary_and_fulladder.py"
EXACT_CCX_MACRO = (
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


def literal(value):
    require(type(value) is int and -(1 << 71) <= value < 1 << W, "Canonical source literal")
    return value - (1 << W) if value >= 1 << 71 else value


def policy(frozen, external, started):
    record = read(IMPLEMENTATION, started)
    require(
        record["schema"] == "a14-cosine-feasibility-implementation-preflight-v1",
        "Exact new implementation schema",
    )
    same(record["CPU_admission_wall_seconds"], [CPU, ADMISSION, WALL], "Fixed clocks")
    require(
        record["primary_digits"] == 90
        and record["independent_digits"] == 130
        and record["threads"] == 1
        and record["new_fixture_credit"] == 0
        and record["gate_emission_authorized"] is False
        and record["full_G2"] is False,
        "Fixed scope/precision/thread/no adoption",
    )
    same(record["fixed_rows"], list(ROWS), "Exactly two fixed rows")
    needed = {
        relative(PHASE_PROOF, started),
        relative(PHASE_SOURCE, started),
        "results/limitation_program_20261001/C06_pair_run001/certificate.json",
        "results/limitation_program_20261001/C06_pair_audit_run001/actual_pair_scope_audit.json",
        "results/limitation_program_20261001/A08_run001/attempt002/leaf_screen.json",
    }
    for case in CASES:
        needed.update(
            "results/limitation_program_20261001/A10_coefficient_run001/"
            + case
            + "/min-depth/"
            + name
            for name in ("target.json", "source.json", "schedule_capped.json")
        )
        for key in record["primitive_descriptor_paths"][case].values():
            needed.add(key)
    require(
        needed <= set(record["existing_source_member_SHA256"]),
        "Exact required source/phase/measured inputs pinned before any kernel",
    )
    same(
        sorted(record["author_sha256"]),
        sorted([PRODUCER.name, AUDITOR.name]),
        "Independent sources both pinned",
    )
    for name, expected in record["author_sha256"].items():
        bind(frozen, external, RESEARCH / name, expected, started)
    for name, expected in record["method_document_SHA256"].items():
        bind(frozen, external, RESEARCH / name, expected, started)
    require(
        set(record["method_document_SHA256"]) == {METHOD.name, METHOD_DOC.name},
        "Exact method documents",
    )
    bind(frozen, external, IMPLEMENTATION, sha(IMPLEMENTATION, started), started)
    bind(frozen, external, IMPLEMENTATION_DOC, sha(IMPLEMENTATION_DOC, started), started)
    method = read(METHOD, started)
    require(
        method["Taylor_comparator"]["degree"] == 6
        and method["Taylor_comparator"]["segments"] == 64
        and method["CORDIC"]["iterations"] == ITERATIONS
        and method["domain"]["new_public_endpoint_policy_differs"] is True,
        "Root-fixed Taylor simplification/total-map scope",
    )
    return record


def selected_dependencies(record, frozen, external, started):
    """Selected original membership and two complete accepted bridge packet maps."""
    owners, memberships = {}, []
    for key, expected in record["existing_owner_manifest_SHA256"].items():
        path = bind(frozen, external, ROOT / key, expected, started)
        owners[key] = owner_rows(path, read(path, started), started)
    require(owners, "Pinned real owner manifests")
    for key, expected in record["existing_source_member_SHA256"].items():
        actual = bind(frozen, external, ROOT / key, expected, started)
        found = [
            dict(
                owner_manifest=owner,
                source_map=field,
                original_key=original,
                original_expected_sha256=value,
            )
            for owner, rows in owners.items()
            for field, path, original, value in rows
            if path == actual and value == expected
        ]
        require(found, "Selected source/member lacks equal-SHA original ownership: " + key)
        memberships.append(
            dict(path=key, sha256=expected, original_memberships=found, expected_hash_waived=False)
        )
    for receipt, expected in (
        (BRIDGE, "78a8eea9dc937883b810cb6b3e2e26aec41297551b984a9c12bb15a435523162"),
        (BRIDGE_AUDIT, "62074efc3bd5a20a9cbe72b3d020fd5c6bf13e32d41b188ef57570225dade2a0"),
    ):
        mf = receipt / "manifest.json"
        require(
            record["existing_owner_manifest_SHA256"][relative(mf, started)] == expected,
            "Actual passing bridge source/audit pins",
        )
        packet = read(mf, started)
        require(
            not (receipt / "FAILED_UNSEALED.json").exists()
            and packet["completed"] is True
            and packet["passed"] is True
            and packet["budget_censored"] is False,
            "Actual accepted bridge packet",
        )
        require(packet["manifest_self_hash_excluded"] is True, "Nested manifest convention")
        owned = set()
        for field in ("files", "frozen_inputs", "external_runtime_inputs"):
            mapping = packet.get(field, {})
            require(type(mapping) is dict, "Recognized packet map")
            for key, value in mapping.items():
                tick(started)
                if field == "files":
                    path = resolved(receipt / key, started)
                    require(path.is_relative_to(receipt), "Owned packet path confinement")
                    owned.add(path)
                elif field == "external_runtime_inputs":
                    path = resolved(key, started)
                    require(not path.is_relative_to(ROOT), "External scope distinct")
                else:
                    path = resolved(ROOT / key, started)
                    require(path.is_relative_to(ROOT), "Frozen packet path confinement")
                bind(frozen, external, path, value, started)
        actual_owned = set()
        for path in receipt.rglob("*"):
            tick(started)
            if path.is_file() and path != mf:
                actual_owned.add(resolved(path, started))
        same(
            sorted(str(path) for path in owned),
            sorted(str(path) for path in actual_owned),
            "Complete original bridge owned bytes",
        )
    return memberships


def one_primitive_profile(record, case, source, frozen, external, started):
    profiles = {}
    paths = record["primitive_descriptor_paths"][case]
    require(
        paths and set(paths) <= {"ADD", "SUB", "MUL"}, "Only measured full72 arithmetic profiles"
    )
    for op, key in paths.items():
        tick(started)
        path = resolved(ROOT / key, started)
        require(relative(path, started) in frozen, "Measured profile frozen before source work")
        data = read(path, started)
        if op in ("ADD", "SUB"):
            require(type(data) is list, "A08 actual fullwidth screen")
            candidates = [
                row
                for row in data
                if row["op"] == op.lower() and row["width"] == W and row["variant"] == "brent-kung"
            ]
            require(len(candidates) == 1, "ONE fixed measured BK72 profile")
            descriptor = candidates[0]
            spec = descriptor["spec"]
            require(
                spec["lowering"] == "clean-xor-prefix-add-sub-v1"
                and spec["variant"] == "brent-kung",
                "Exact raw modular full72 adder family",
            )
            gate_path = resolved(path.parent / descriptor["gate_file"].replace("\\", "/"), started)
            builder_path = path.parent / "executed_code/carry_lookahead.py"
            require(
                relative(builder_path, started) in frozen,
                "Exact measured raw builder source frozen",
            )
            builder_module = ast.parse(read_bytes(builder_path, started).decode("utf-8"))
            builder_defs = {
                node.name: node for node in builder_module.body if isinstance(node, ast.FunctionDef)
            }
            require(
                {"build_carry_lookahead", "prefix_pairs", "_compose"} <= set(builder_defs),
                "Complete actual raw prefix builder source",
            )
            same(
                [arg.arg for arg in builder_defs["build_carry_lookahead"].args.args],
                ["op", "width", "variant"],
                "Raw builder accepts no fraction or scale input",
            )
            for name in ("build_carry_lookahead", "prefix_pairs", "_compose"):
                for item in ast.walk(builder_defs[name]):
                    tick(started)
                    require(
                        not isinstance(item, ast.Name)
                        or not any(token in item.id.lower() for token in ("fraction", "scale")),
                        "Raw bit-map construction independent of fractional label",
                    )
        else:
            descriptor = data
            spec = descriptor["spec"]
            require(
                spec["fraction_bits"] == F and spec["product_width"] == W + F,
                "Actual generic full72 f40 signed144-to112 multiplier",
            )
            gate_path = path.with_suffix(".npy")
        require(
            spec["op"] == op.lower() and spec["width"] == W and spec["params"] == {},
            "Explicit actual operation/fullwidth emptyparams",
        )
        require(
            not spec.get("input_contract")
            and not descriptor.get("input_contract")
            and not spec.get("active_operand_bits")
            and not descriptor.get("active_operand_bits"),
            "No narrow unit borrowed",
        )
        same(descriptor["args"], [list(range(W)), list(range(W, 2 * W))], "Full72 argument ABI")
        same(descriptor["outs"], [list(range(2 * W, 3 * W))], "Full72 dirty-XOR output ABI")
        gate_key = relative(gate_path, started)
        require(gate_key in frozen, "Actual measured gates originally owned and frozen")
        resources = descriptor["resources"]
        require(
            all(
                type(resources[field]) is int and resources[field] >= 0 for field in RESOURCE_FIELDS
            ),
            "Typed measured resource fields",
        )
        require(resources["t_count"] == 7 * resources["ccx"], "Actual paid exact7T profile")
        profiles[op] = dict(
            descriptor_path=relative(path, started),
            descriptor_sha256=frozen[relative(path, started)],
            gate_path=gate_key,
            gate_sha256=frozen[gate_key],
            op=op.lower(),
            spec=spec,
            args=descriptor["args"],
            outs=descriptor["outs"],
            resources=resources,
            compiled_source_format=source["format"],
            word_width=W,
            fraction_bits=F,
            raw_modular_ADD_SUB_fraction_label_reuse_only=op in ("ADD", "SUB"),
        )
        if op in ("ADD", "SUB"):
            profiles[op]["raw_bit_map_fraction_label_independence"] = dict(
                builder_path=relative(builder_path, started),
                builder_sha256=frozen[relative(builder_path, started)],
                physical_call_arguments=[op.lower(), W, "brent-kung"],
                raw_map="(a+b) mod2^72" if op == "ADD" else "(a-b) mod2^72",
                fraction_label_is_metadata_only=True,
                independent_signed_range_proofs_still_required=True,
                new_gate_or_builder_execution=False,
            )
    return profiles


def primitive_profiles(record, case, source, frozen, external, started):
    declared = record["primitive_descriptor_paths"][case]
    require(set(declared) == {"ADD", "SUB", "MUL"}, "Exact measured primitive path scope")
    result = {}
    for op, key in declared.items():
        path = resolved(ROOT / key, started)
        require(
            relative(path, started) in frozen, "Profile path must have original bound membership"
        )
        single = dict(record, primitive_descriptor_paths={case: {op: key}})
        try:
            result.update(one_primitive_profile(single, case, source, frozen, external, started))
        except (ValueError, KeyError, TypeError) as error:
            result[op] = dict(
                resource_rejected=True,
                op=op.lower(),
                descriptor_path=key,
                descriptor_sha256=frozen[relative(path, started)],
                reason=str(error),
                error_type=type(error).__name__,
                no_cost_or_contract_claim=True,
            )
    return result


def phase_premise(started):
    proof = read(PHASE_PROOF, started)
    same(
        proof,
        [
            dict(input=k, output=k ^ (((k & 1) & ((k >> 1) & 1)) << 2), exact_nonzero_phase=1)
            for k in range(8)
        ],
        "Frozen exact phase-one3wire CCX proof",
    )
    source = ast.parse(read_bytes(PHASE_SOURCE, started).decode("utf-8"))
    found = [
        node
        for node in source.body
        if isinstance(node, ast.FunctionDef) and node.name == "ccx_seven_t"
    ]
    require(len(found) == 1, "One frozen CCX source")
    returns = [node for node in found[0].body if isinstance(node, ast.Return)]
    require(
        len(returns) == 1 and isinstance(returns[0].value, ast.List), "Literal paid CCX chronology"
    )
    rows = []
    for item in returns[0].value.elts:
        require(
            isinstance(item, ast.Call)
            and isinstance(item.func, ast.Name)
            and item.func.id == "gate"
            and not item.keywords
            and isinstance(item.args[0], ast.Constant)
            and all(isinstance(arg, ast.Name) for arg in item.args[1:]),
            "Typed literal CCX row",
        )
        rows.append((item.args[0].value, *(arg.id for arg in item.args[1:])))
    same(rows, list(EXACT_CCX_MACRO), "Both control phases/literal macro chronology")
    return dict(
        exact_macro=[list(row) for row in rows],
        native_phase_one=True,
        direct_recipe_T_depth_per_CCX=7,
        direct_recipe_Clifford_T_serial_depth_per_CCX=15,
        fresh_gate_or_phase_simulation_executed=False,
    )


def removable_cosine_calls(graph, source, cosine_outputs, arguments, radius_products, started):
    stops = set().union(*(graph.ancestors(value) for value in arguments))
    candidates = set().union(*(graph.ancestors(value) for value in cosine_outputs)) - stops
    users = {value: set() for value in graph.nodes}
    for node in graph.target["nodes"]:
        tick(started)
        for value in node["args"]:
            users[value].update(node["out"])
    authorized = set(zip(cosine_outputs, radius_products, strict=True))
    proposed = set(candidates)
    changed = True
    while changed:
        changed = False
        for value in sorted(proposed):
            tick(started)
            node_outputs = set(graph.node(value)["out"])
            if any(
                user not in proposed and (output, user) not in authorized
                for output in node_outputs
                for user in users[output]
            ):
                proposed.difference_update(node_outputs)
                changed = True
                break
    require(
        set(cosine_outputs) <= proposed,
        "Every cosine endpoint replaceable only at actual radius product",
    )
    calls = [call for call in source["forward_calls"] if set(call["out"]) <= proposed]
    require(
        {value for call in calls for value in call["out"]} == proposed,
        "Complete removable node/call inventory",
    )
    return dict(
        removed_value_ids=sorted(proposed),
        removed_forward_calls=calls,
        retained_shared_or_outside_value_ids=sorted(candidates - proposed),
        authorized_cosine_output_to_radius_product_edges=[
            list(edge) for edge in sorted(authorized)
        ],
        actual_user_fixed_point=True,
        original_storage_subtracted=False,
    )


def source_binding(record, frozen, external, started):
    tick(started, admission=True)
    certificate = read(PROGRAM / "C06_pair_run001/certificate.json", started)
    archived = read(PROGRAM / "C06_pair_audit_run001/actual_pair_scope_audit.json", started)
    cases, graphs = {}, {}
    for case, (assets, dates, pairs) in CASES.items():
        tick(started)
        directory = PROGRAM / "A10_coefficient_run001" / case / "min-depth"
        target_path, source_path, schedule_path = (
            directory / name for name in ("target.json", "source.json", "schedule_capped.json")
        )
        for path in (target_path, source_path, schedule_path):
            require(relative(path, started) in frozen, "Actual source frozen before graph walk")
        target, source, schedule = (
            read(path, started) for path in (target_path, source_path, schedule_path)
        )
        graph = ActualGraph(target, started)
        graphs[case] = graph
        require(
            source["format"] == "hierarchical-clean-xor-source-v1"
            and source["word_width"] == W
            and source["fraction_bits"] == F,
            "Original full72/f40 hierarchical clean source",
        )
        inputs = [node for node in target["nodes"] if node["op"] == "input"]
        require(len(inputs) == 2 * pairs == dates * (assets + 1), "Actual pair/driver count")
        same(source["inputs"], inputs, "Full original input ABI")
        same(source["outputs"], target["outputs"], "Named dirty output ABI")
        for index, node in enumerate(inputs):
            same(
                node["params"],
                dict(name="uniform_" + str(index), bits=32, preparation="uniform"),
                "Actual joint q32 roles",
            )
        noninputs = [node for node in target["nodes"] if node["op"] != "input"]
        require(
            len(noninputs) == len(source["forward_calls"]), "Every eager original call retained"
        )
        calls = {}
        for node, call in zip(noninputs, source["forward_calls"], strict=True):
            tick(started)
            same(
                [node["args"], node["out"]], [call["args"], call["out"]], "Actual full call mapping"
            )
            require(
                call["argument_copy_cx"] == 2 * W * len(node["args"]),
                "Every full72 original argument copy paid",
            )
            for value in node["out"]:
                calls[value] = call
        original = certificate["source_bindings"][case]
        normals, ln2 = original["normal_values"], original["literal_ln2"]
        require(len(normals) == 2 * pairs, "All original normals jointly retained")
        scopes, cosines, arguments, radius_products = [], [], [], []
        for pair in range(pairs):
            tick(started)
            roots = normals[2 * pair : 2 * pair + 2]
            scope = graph.pair(
                roots, inputs[2 * pair]["out"][0], inputs[2 * pair + 1]["out"][0], ln2
            )
            scopes.append(scope)
            cosines.extend(row["output"] for row in scope["cosines"])
            arguments.extend(row["input"] for row in scope["cosines"])
            radius_products.extend(roots)
        same(
            scopes,
            archived[case]["independently_walked_pair_scopes"],
            "Exact archived independently verified pair scopes",
        )
        require(len(cosines) == CASE_SITES[case], "Both cosine/sine calls in each joint pair")
        require(
            source["resources"]["t_count"] == BASELINE[case][0],
            "Actual original whole-source T count",
        )
        require(
            schedule["resources"]["t_count"] == BASELINE[case][0]
            and schedule["resources"]["t_depth"] == BASELINE[case][1]
            and schedule["resources"]["logical_qubits"] == BASELINE[case][2],
            "Exact measured original capped schedule context/caps",
        )
        cases[case] = dict(
            assets=assets,
            dates=dates,
            joint_pairs=pairs,
            cosine_sites=len(cosines),
            target_path=relative(target_path, started),
            source_path=relative(source_path, started),
            schedule_path=relative(schedule_path, started),
            target_sha256=frozen[relative(target_path, started)],
            source_sha256=frozen[relative(source_path, started)],
            schedule_sha256=frozen[relative(schedule_path, started)],
            original_resources=source["resources"],
            original_measured_schedule=schedule,
            normal_values=normals,
            pair_scopes=scopes,
            cosine_output_values=cosines,
            cosine_argument_values=arguments,
            cosine_calls=[calls[value] for value in cosines],
            selected_primitive_profiles=primitive_profiles(
                record, case, source, frozen, external, started
            ),
            removal=removable_cosine_calls(
                graph, source, cosines, arguments, radius_products, started
            ),
            source_convention_exact=True,
            cross_date_pair_coordinates_not_divided=True,
        )
    old_path = BRIDGE / "cosine_envelope.json"
    old = read(old_path, started)
    error = rational(old["cosine_error_upper"])
    require(error >= EPS, "Freshly bound original seven propagated floors include final fullULP")
    same(
        graphs["B4x12"].target["tables"]["cos"],
        graphs["B8x52"].target["tables"]["cos"],
        "Actual source cosine tables agree",
    )
    table = graphs["B4x12"].target["tables"]["cos"]
    require(len(old["coefficient_checks"]) == 512, "All old512 coefficient checks retained")
    row_errors = [Fraction(0) for _ in range(64)]
    for index, check in enumerate(old["coefficient_checks"]):
        tick(started)
        row, degree = divmod(index, 8)
        require(
            check["row"] == row
            and check["degree"] == degree
            and check["raw"] == table[row][degree],
            "E_old exact original coefficient inventory",
        )
        lo, hi = (rational(value) for value in check["exact_coefficient_enclosure"])
        paid = rational(check["actual_literal_error_upper"])
        require(
            paid == max(abs(Fraction(check["raw"], Q) - lo), abs(Fraction(check["raw"], Q) - hi)),
            "Exact old actual-literal error arithmetic",
        )
        row_errors[row] += paid * H**degree
    floor_bound = EPS * sum((H**degree for degree in range(7)), Fraction(0))
    require(
        rational(old["literal_rounding_upper"]) == max(row_errors)
        and rational(old["Horner_floor_upper"]) == floor_bound
        and error
        == max(row_errors) + floor_bound + rational(old["Taylor_degree7_remainder_upper"]),
        "Original E_old complete source-specific formula, never a numerical guess",
    )
    radius = rational(old["pinned_native_radius_upper"])
    require(
        radius > 0 and rational(old["remaining_coordinate_error_upper"]) == radius * error + EPS,
        "Already-paid native radius and remaining cosine/product error ledger",
    )
    return dict(
        schema="a14-original-cosine-source-binding-v1",
        cases=cases,
        existing_E_old=dict(
            path=relative(old_path, started),
            sha256=frozen[relative(old_path, started)],
            cosine_error_upper=encode(error),
            pinned_native_radius_upper=encode(radius),
            remaining_coordinate_error_upper=encode(radius * error + EPS),
            all512_actual_coefficient_words_and_error_formula_bound=True,
            source_manifest_sha256=record["existing_owner_manifest_SHA256"][
                relative(BRIDGE / "manifest.json", started)
            ],
            audit_manifest_sha256=record["existing_owner_manifest_SHA256"][
                relative(BRIDGE_AUDIT / "manifest.json", started)
            ],
        ),
        phase_premise=phase_premise(started),
        arbitrary_signed_input_policy="new charged signed clamp [0,Q]",
        new_public_total_map_differs_from_original_Q_minus_one=True,
        actual_midpoint_wrap_domains_strictly_between_zero_and_Q=True,
        full_G2=False,
        cost_transfer=False,
    ), graphs


def zero_resource():
    return {field: 0 for field in RESOURCE_FIELDS}


def combine_resource(first, second, multiplier=1):
    return {field: first[field] + multiplier * second[field] for field in RESOURCE_FIELDS}


def direct_resource(x=0, cx=0, ccx=0):
    return dict(
        source_gates=x + cx + ccx,
        x=x,
        cx=cx,
        ccx=ccx,
        t_count=7 * ccx,
        t_depth=7 * ccx,
        clifford_t_depth=x + cx + 15 * ccx,
        clifford_cx=cx + 6 * ccx,
        clifford_h=2 * ccx,
    )


def node_unit(node, profiles):
    op, params = node["op"], node["params"]
    if op == "CONST":
        resource, private = direct_resource(x=(params["raw"] % (1 << W)).bit_count()), 0
    elif op in ("ADD", "SUB", "MUL"):
        profile = profiles[op]
        if profile.get("resource_rejected"):
            raise ResourceRejectedError(op + ": " + profile["reason"])
        resource = {field: profile["resources"][field] for field in RESOURCE_FIELDS}
        private = profile["resources"]["qubits"] - W
    elif op == "LT":
        resource, private = direct_resource(x=436, cx=433, ccx=286), 2 * W + 216
    elif op == "EQ":
        resource, private = direct_resource(x=144, cx=289, ccx=142), 2 * W + 143
    elif op == "SELECT":
        resource, private = direct_resource(cx=360, ccx=72), 3 * W + 72
    elif op == "BITS":
        resource, private = (
            direct_resource(cx=sum(value is not None for value in params["output_to_input_bit"])),
            W,
        )
    elif op == "FLAG_AND":
        resource, private = direct_resource(ccx=1), 2 * W
    elif op == "FLAG_OR":
        resource, private = direct_resource(cx=2, ccx=1), 2 * W
    elif op == "LOOKUP":
        table = params["table"]
        require(
            len(table) == 64 and all(len(row) == 8 for row in table), "Exact512 full72 table words"
        )
        x = sum(2 * (6 - index.bit_count()) for index in range(64))
        cx = sum((word % (1 << W)).bit_count() for row in table for word in row)
        resource, private = direct_resource(x=x, cx=cx, ccx=64 * 10), W + 5
    else:
        raise ValueError("No input/unknown primitive unit")
    require(private >= len(node["args"]) * W, "Every argument copied to its own clean bank")
    return resource, private


def resource_estimates(plans, binding, frozen, started, native_passed):
    rows = {}
    for row_id, plan in plans.items():
        tick(started)
        if not native_passed[row_id]:
            rows[row_id] = dict(
                resource_contract_passed=False,
                rejected=True,
                reason="Native arithmetic safety rejected; no resource estimate claimed",
                cases={},
                native_gates_emitted=False,
            )
            continue
        cases, units = {}, {}
        for case, original in binding["cases"].items():
            profiles = original["selected_primitive_profiles"]
            forward, events, max_private, copies, loading = zero_resource(), [], 0, 0, 0
            for node in plan["nodes"]:
                tick(started)
                if node["op"] == "INPUT":
                    continue
                try:
                    unit, private = node_unit(node, profiles)
                except ResourceRejectedError as error:
                    cases[case] = dict(
                        resource_contract_passed=False,
                        rejected=True,
                        reason=str(error),
                        no_cost_or_contract_claim=True,
                    )
                    break
                argument_copy = 2 * len(node["args"]) * W
                cost = combine_resource(unit, direct_resource(cx=argument_copy))
                forward = combine_resource(forward, cost)
                max_private = max(max_private, private)
                copies += argument_copy
                loading += unit["x"] if node["op"] == "CONST" else 0
                events.append(
                    dict(
                        outputs=node["outputs"],
                        op=node["op"],
                        primitive_resource=unit,
                        argument_copy_CX=argument_copy,
                        private_and_argument_banks=private,
                    )
                )
            if case in cases:
                continue
            clean = combine_resource(
                combine_resource(zero_resource(), forward, 2), direct_resource(cx=W)
            )
            removed = zero_resource()
            directory = PROGRAM / "A10_coefficient_run001" / case / "min-depth/leaves"
            for call in original["removal"]["removed_forward_calls"]:
                tick(started)
                path = directory / (call["leaf"] + ".json")
                require(
                    relative(path, started) in frozen,
                    "Removed actual measured leaf descriptor frozen",
                )
                descriptor = read(path, started)
                unit = {field: descriptor["resources"][field] for field in RESOURCE_FIELDS}
                removed = combine_resource(
                    removed, combine_resource(unit, direct_resource(cx=call["argument_copy_cx"]))
                )
            baseline = {field: original["original_resources"][field] for field in RESOURCE_FIELDS}
            insertion = combine_resource(clean, direct_resource(cx=2 * W))
            sites = original["cosine_sites"]
            estimated = combine_resource(
                combine_resource(baseline, removed, -2), insertion, 2 * sites
            )
            require(
                all(value >= 0 for value in estimated.values()), "No negative resource subtraction"
            )
            workspace = (plan["allocated_full72_banks"] - 1) * W + max_private
            standalone = 2 * W + workspace
            # Retain ALL original SSA storage and scratch; add one serialized clean function bank.
            whole_qubits = original["original_resources"]["logical_qubits"] + workspace + W
            within = standalone <= 131072 and whole_qubits <= BASELINE[case][2]
            improvement = (
                estimated["t_count"] < baseline["t_count"]
                and estimated["t_depth"] < baseline["t_depth"]
            )
            cases[case] = dict(
                function_forward_resource_estimate=forward,
                function_clean_resource_estimate=clean,
                inner_argument_copy_CX=copies,
                constant_loading_X=loading,
                primitive_events=events,
                full72_bank_inventory=dict(
                    allocated_recipe_banks=plan["allocated_full72_banks"],
                    retained_noninput_banks=plan["allocated_full72_banks"] - 1,
                    external_input_bank=1,
                    dirty_output_bank=1,
                    outer_argument_copy_bank=1,
                    word_qubits=plan["allocated_full72_banks"] * W,
                    maximum_reused_primitive_private_plus_arguments=max_private,
                    all_eager_and_constant_output_banks_retained=True,
                    original_storage_subtracted=False,
                ),
                outer_function_argument_copy_CX_per_clean_invocation=2 * W,
                whole_source=dict(
                    original=baseline,
                    removed_twice=combine_resource(zero_resource(), removed, 2),
                    added_twice_clean_plus_outercopies=combine_resource(
                        zero_resource(), insertion, 2 * sites
                    ),
                    estimated=estimated,
                    qubits_conservative=whole_qubits,
                    standalone_clean_workspace=standalone,
                    comparison_with_both_original_T_and_matched_serial_depth=improvement,
                    within_caps=within,
                    original_measured_T_depth_context_only=BASELINE[case][1],
                    globally_serialized_clean_workspace_reused=True,
                    workspace_reuse_proof=(
                        "Each call starts with all private/noninput banks zero. Clean "
                        "primitives preserve inputs and XOR fresh outputs. Literal "
                        "F/outputXOR/F^-1 returns every private bank zero. Sequential "
                        "calls reuse one fixed bank; all original SSA storage/scratch "
                        "remains allocated."
                    ),
                ),
                resource_contract_passed=True,
            )
            units[case] = profiles
        rows[row_id] = dict(
            plan=plan,
            plan_sha256=hashlib.sha256(canonical(plan).encode()).hexdigest(),
            primitive_units=units,
            cases=cases,
            resource_status="SYMBOLIC_ESTIMATE_ONLY",
            resource_contract_passed=all(
                case["resource_contract_passed"] for case in cases.values()
            ),
            exact7T_serial_direct_recipes=True,
            native_gates_emitted=False,
            complete_source_adoption=False,
        )
    return dict(
        schema="a14-symbolic-source-resource-estimates-v1",
        rows=rows,
        clean_function_excludes_outer_argument_copy=True,
        global_forward_and_inverse_both_invoke_complete_clean_function=True,
        full_G2=False,
        cost_transfer=False,
        adoption=False,
    )


def seal(output, frozen, external, started, outcome):
    require(
        not (output / "manifest.json").exists()
        and not (output / "FAILED_UNSEALED.json").exists()
        and not (output / "completion_outcome.json").exists(),
        "Exclusive single terminal outcome, no retry",
    )
    tick(started)
    verified = final_verify(frozen, external, started)
    outcome = dict(
        outcome,
        verification_unique_paths=verified,
        budget=elapsed(started),
        CPU_admission_wall_seconds=[CPU, ADMISSION, WALL],
        new_test_credit=0,
        full_G2=False,
        adoption=False,
        cost_transfer=False,
        gates_emitted=False,
    )
    save(output / "completion_outcome.json", outcome, started)
    files = owned_files(output, started)
    save(
        output / "manifest.json",
        dict(
            schema="a14-cosine-feasibility-terminal-manifest-v1",
            files=files,
            frozen_inputs=frozen,
            external_runtime_inputs=external,
            manifest_self_hash_excluded=True,
            completed=outcome["completed"],
            passed=outcome["passed"],
            budget_censored=outcome["budget_censored"],
            terminal_outcome_file="completion_outcome.json",
            verification_and_output_hashing_before_terminal=True,
            terminal_budget_observation=elapsed(started),
            original_expected_hashes_waived=False,
            historical_global_LIVE_integrity=dict(
                passed=False, mismatch_references=36, distinct_paths=9, expected_hashes_waived=False
            ),
            scoped_selected_receipt_validity_separate=True,
        ),
        started,
    )


def retain_failure(output, frozen, external, started, error, phase):
    if not output.exists():
        return
    try:
        require(
            not (output / "manifest.json").exists()
            and not (output / "completion_outcome.json").exists(),
            "Partial terminal records block resealing",
        )
        tick(started)
        save(
            output / "failure.json",
            dict(
                phase=phase,
                error_type=type(error).__name__,
                error=str(error),
                traceback=traceback.format_exc(),
                failed=True,
                budget=elapsed(started),
                new_test_credit=0,
            ),
            started,
        )
        seal(
            output,
            frozen,
            external,
            started,
            dict(
                completed=False,
                passed=False,
                failed=True,
                budget_censored=isinstance(error, BudgetCensoredError),
                phase=phase,
                failure_file="failure.json",
            ),
        )
    except BaseException:
        marker = output / "FAILED_UNSEALED.json"
        if not marker.exists():
            # Fixed literal emergency write: no scan, encode-heavy record or uncapped hashing.
            with marker.open("xb") as stream:
                stream.write(
                    b'{"failed":true,"completed":false,"passed":false,"budget_censored":null,"hard_budget_state_uncertified":true,"partial_success_invalid":true,"new_test_credit":0,"full_G2":false,"adoption":false,"fresh_version_required":true}\n'
                )


def prepare(output):
    started = process_started()
    frozen, external = {}, {}
    try:
        setup(started)
        require(
            resolved(output.parent, started) == PROGRAM and output.name == OUTPUT.name,
            "Exact fresh A14 output route",
        )
        require(not output.exists(), "Fresh output, no preparation retry")
        record = policy(frozen, external, started)
        memberships = selected_dependencies(record, frozen, external, started)
        interpreter = runtime(frozen, external, started)
        origins = verify_loaded(frozen, external, started)
        verify(frozen, external, started)
        final_verify(frozen, external, started)
        tick(started, admission=True)
        output.mkdir(exist_ok=False)
        (output / "executed_code").mkdir(exist_ok=False)
        for path in (PRODUCER, AUDITOR, METHOD, METHOD_DOC, IMPLEMENTATION, IMPLEMENTATION_DOC):
            copy_exact(path, output / "executed_code" / path.name, frozen, external, started)
        save(output / "selected_source_origins.json", memberships, started)
        save(output / "interpreter.json", interpreter, started)
        save(output / "loaded_origins_prepare.json", origins, started)
        final_verify(frozen, external, started)
        tick(started, admission=True)
        save(
            output / "protocol.json",
            dict(
                schema="a14-cosine-feasibility-protocol-v1",
                author_sha256=record["author_sha256"],
                method_document_SHA256=record["method_document_SHA256"],
                existing_owner_manifest_SHA256=record["existing_owner_manifest_SHA256"],
                existing_source_member_SHA256=record["existing_source_member_SHA256"],
                primitive_descriptor_paths=record["primitive_descriptor_paths"],
                CPU_admission_wall_seconds=[CPU, ADMISSION, WALL],
                primary_digits=90,
                independent_digits=130,
                threads=1,
                fixed_rows=list(ROWS),
                frozen_inputs=frozen,
                external_runtime_inputs=external,
                original_expected_hashes_waived=False,
                preparation_metadata_only=True,
                new_test_credit=0,
                full_G2=False,
                adoption=False,
                cost_transfer=False,
                prepare_budget=elapsed(started),
                complete_runtime_before_source_or_interval_work=True,
            ),
            started,
        )
    except BaseException as error:
        retain_failure(output, frozen, external, started, error, "prepare")
        raise


def protocol_guard(protocol, record):
    require(
        protocol["schema"] == "a14-cosine-feasibility-protocol-v1"
        and protocol["preparation_metadata_only"] is True,
        "Real prepared byte-only protocol",
    )
    for field in (
        "author_sha256",
        "method_document_SHA256",
        "existing_owner_manifest_SHA256",
        "existing_source_member_SHA256",
        "primitive_descriptor_paths",
    ):
        same(protocol[field], record[field], "Prepared scope/pins immutable: " + field)
    same(protocol["CPU_admission_wall_seconds"], [CPU, ADMISSION, WALL], "Prepared clocks")
    same(protocol["fixed_rows"], list(ROWS), "Prepared finite two rows")
    require(
        protocol["primary_digits"] == 90
        and protocol["independent_digits"] == 130
        and protocol["threads"] == 1
        and protocol["new_test_credit"] == 0
        and protocol["full_G2"] is False
        and protocol["adoption"] is False
        and protocol["cost_transfer"] is False
        and protocol["original_expected_hashes_waived"] is False,
        "Prepared fixed precision and no acceptance transfer",
    )


def run(output):
    started = process_started()
    frozen, external = {}, {}
    try:
        setup(started)
        require(
            resolved(output, started) == OUTPUT
            and not (output / "manifest.json").exists()
            and not (output / "FAILED_UNSEALED.json").exists(),
            "Exact prepared fresh run, no retry",
        )
        with (output / "RUN_STARTED.json").open("xb") as stream:
            stream.write(b'{"exclusive_run_started":true,"retry_forbidden":true}\n')
        protocol = read(output / "protocol.json", started)
        frozen.update(protocol["frozen_inputs"])
        external.update(protocol["external_runtime_inputs"])
        verify(frozen, external, started)
        record = policy(frozen, external, started)
        protocol_guard(protocol, record)
        memberships = selected_dependencies(record, frozen, external, started)
        same(
            memberships,
            read(output / "selected_source_origins.json", started),
            "Independent fresh selected membership",
        )
        interpreter = read(output / "interpreter.json", started)
        runtime_policy(interpreter, started)
        verify_loaded(frozen, external, started)
        final_verify(frozen, external, started)
        tick(started, admission=True)
        import mpmath as mp

        require(
            mp.__version__ == "1.3.0" and mp.libmp.BACKEND == "python",
            "Pinned pure-Python interval backend",
        )
        mp.mp.dps, mp.iv.dps = 90, 90
        save(
            output / "loaded_origins_before_kernel.json",
            verify_loaded(frozen, external, started),
            started,
        )
        binding, graphs = source_binding(record, frozen, external, started)
        save(output / "source_binding.json", binding, started)
        cordic = make_cordic_literals(mp, started)
        save(output / "cordic_literals.json", cordic, started)
        if cordic["half_ULP_premises_passed"]:
            cordic_certificate = dict(cordic_uniform_certificate(mp, cordic, started), passed=True)
        else:
            cordic_certificate = dict(
                schema="a14-cordic-uniform-certificate-v1",
                row_id=ROWS[0],
                passed=False,
                rejected=True,
                reason="Actual angle/gain half-ULP premise rejected",
            )
        save(output / "cordic_uniform_certificate.json", cordic_certificate, started)
        taylor = make_taylor_literals(mp, started)
        save(output / "taylor6_literals.json", taylor, started)
        taylor_certificate = dict(taylor_uniform_certificate(mp, taylor, started), passed=True)
        save(output / "taylor6_uniform_certificate.json", taylor_certificate, started)
        plans = {ROWS[0]: cordic_plan(cordic, started), ROWS[1]: taylor_plan(taylor, started)}
        safety_results, native_passed = {}, {}
        for row_id, literals, function in (
            (ROWS[0], cordic, cordic_native_safety),
            (ROWS[1], taylor, taylor_native_safety),
        ):
            try:
                safety = function(literals, started)
                safety["complete_recipe_certificate"] = plan_native_safety(plans[row_id], started)
                safety["passed"] = True
                native_passed[row_id] = True
            except NativeRejectedError as error:
                safety = dict(
                    row_id=row_id,
                    passed=False,
                    rejected=True,
                    reason=str(error),
                    native_arithmetic_safety_claim=False,
                    no_resource_or_adoption_claim=True,
                )
                native_passed[row_id] = False
            safety_results[row_id] = safety
        cordic_safety, taylor_safety = safety_results[ROWS[0]], safety_results[ROWS[1]]
        save(output / "cordic_native_safety.json", cordic_safety, started)
        save(output / "taylor6_native_safety.json", taylor_safety, started)
        resources = resource_estimates(plans, binding, frozen, started, native_passed)
        save(output / "resource_estimates.json", resources, started)
        old = rational(binding["existing_E_old"]["cosine_error_upper"])
        B = rational(binding["existing_E_old"]["pinned_native_radius_upper"])
        rows = []
        for row_id, certificate in ((ROWS[0], cordic_certificate), (ROWS[1], taylor_certificate)):
            tick(started)
            certified = certificate["passed"]
            error = rational(certificate["cosine_error_upper"]) if certified else None
            compare = certified and error <= old
            costs = resources["rows"][row_id]["cases"]
            resource_passed = resources["rows"][row_id]["resource_contract_passed"]
            improvement = resource_passed and all(
                row["whole_source"]["comparison_with_both_original_T_and_matched_serial_depth"]
                for row in costs.values()
            )
            within = resource_passed and all(
                row["whole_source"]["within_caps"] for row in costs.values()
            )
            eligible = compare and native_passed[row_id] and improvement and within
            status = (
                "COMPONENT_SCREEN_PASS"
                if eligible
                else "NATIVE_REJECTED"
                if not native_passed[row_id]
                else "UNIFORM_REJECTED"
                if not compare
                else "RESOURCE_REJECTED"
            )
            rows.append(
                dict(
                    row_id=row_id,
                    status=status,
                    uniform_certificate_passed=certified,
                    native_safety_passed=native_passed[row_id],
                    resource_contract_passed=resource_passed,
                    E_at_most_E_old=compare,
                    improvement_on_both_sources=improvement,
                    within_caps=within,
                    component_screen_eligible=eligible,
                    uniform_error_upper=None if error is None else encode(error),
                    conditional_remaining_coordinate_error_upper=None
                    if error is None
                    else encode(B * error + EPS),
                    whole_financial_G2_proof_still_required=True,
                    full_G2=False,
                    adoption=False,
                    cost_transfer=False,
                )
            )
        save(
            output / "fixed_frontier.json",
            dict(
                schema="a14-fixed-cosine-frontier-v1",
                rows=rows,
                financial_bridge_open=True,
                actual_root_total_map_authorization_still_required_before_production=True,
                changed_source_not_emitted=True,
                new_fixture_credit=0,
                full_G2=False,
                adoption=False,
            ),
            started,
        )
        save(
            output / "loaded_origins_after_kernel.json",
            verify_loaded(frozen, external, started),
            started,
        )
        runtime_policy(interpreter, started)
        save(
            output / "summary.json",
            dict(
                schema="a14-cosine-feasibility-summary-v1",
                passed=True,
                completed=True,
                scientific_screen_complete=True,
                budget_censored=False,
                fixed_row_ids=list(ROWS),
                component_screen_eligible_rows=[
                    row["row_id"] for row in rows if row["component_screen_eligible"]
                ],
                at_most_one_later_production_candidate_external_ROOT_release_required=True,
                interval_digits=90,
                numerical_threads=1,
                new_test_credit=0,
                full_G2=False,
                adoption=False,
                cost_transfer=False,
                gates_emitted=False,
                budget=elapsed(started),
            ),
            started,
        )
        seal(
            output,
            frozen,
            external,
            started,
            dict(
                completed=True,
                passed=True,
                failed=False,
                budget_censored=False,
                scientific_screen_complete=True,
                phase="run",
                summary_file="summary.json",
            ),
        )
    except BaseException as error:
        retain_failure(output, frozen, external, started, error, "run")
        raise


def main():
    parser = argparse.ArgumentParser(
        description="Root-released fixed A14 component/resource feasibility screen"
    )
    parser.add_argument("mode", choices=("prepare", "run"))
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    require(args.output.is_absolute(), "Explicit absolute output path")
    (prepare if args.mode == "prepare" else run)(args.output)


if __name__ == "__main__":
    main()
