"""AUTHOR-STAGE independent130 fixed A14 cosine screen.

This draft is not released for preparation or execution. No producer/helper
imports, numerical evaluation, source traversal, fitting, gate generation or
tests have executed during authoring. Runtime/source/lifecycle integration and
the companion executable pins remain prerequisites. The fixed candidates are
CORDIC48 signed72/f56 and Taylor6 on64 centered segments signed72/f40.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter
import ctypes
from ctypes import wintypes
from fractions import Fraction
import hashlib
from importlib import metadata
from importlib.util import cache_from_source
import json
from math import factorial
import os
from pathlib import Path
import re
import site
import sys
import time
import traceback


W, F, Q = 72, 40, 1 << 40
CORDIC_F, CORDIC_Q, ITERATIONS = 56, 1 << 56, 48
EPSILON = Fraction(1, Q)
CORDIC_EPSILON = Fraction(1, CORDIC_Q)
LOCAL_RADIUS = Fraction(1, 128)
ROW_IDS = ("CORDIC_N48_W72_F56_BK72", "TAYLOR_D6_S64_W72_F40")
ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
PROGRAM = ROOT / "results/limitation_program_20261001"
SOURCE = PROGRAM / "A14_cosine_feasibility_run001"
OUTPUT = PROGRAM / "A14_cosine_feasibility_audit_run002"
AUTHOR = RESEARCH / "audit_cosine_feasibility_v2.py"
PRODUCER_AUTHOR = RESEARCH / "experiment_cosine_feasibility.py"
METHOD = RESEARCH / "a14_cosine_feasibility_preflight.json"
METHOD_DOC = RESEARCH / "A14_COSINE_FEASIBILITY_PREFLIGHT.md"
IMPLEMENTATION = RESEARCH / "a14_cosine_feasibility_audit_implementation_preflight_v2.json"
IMPLEMENTATION_DOC = RESEARCH / "A14_COSINE_FEASIBILITY_AUDIT_IMPLEMENTATION_PREFLIGHT_V2.md"
SOURCE_SHA256 = "bdb01b0c69d8fab3ee3d61f1c48ce5764f1ae09488f564d186f658f180e4156b"
PRIOR_AUDIT = PROGRAM / "A14_cosine_feasibility_audit_run001"
PRIOR_AUDIT_SHA256 = "3b423ce15bd752745747807bf2970a2d7888a057d6c86ced1f2ed0efd98ece6e"
LITERAL_DIAGNOSTIC = PROGRAM / "A14_cosine_literal_diagnostic_run001"
LITERAL_DIAGNOSTIC_SHA256 = "c2dc33d96b0604d09666351ddefcd754d048b787f66e350174eda75c9b9fe8af"
LITERAL_DIAGNOSTIC_REVIEW = PROGRAM / "A14_cosine_literal_diagnostic_root_review_run001"
LITERAL_DIAGNOSTIC_REVIEW_SHA256 = (
    "7511709f30647a2dd6aa6b277ae38ddeddf7c81cb975c9eac2dd1d70415d3d059"
)
ORIGINAL_AUTHORS = {
    "experiment_cosine_feasibility.py": (
        "dba562b13f4d250c04376927f431e5a39ceaedfdcfc5e8ebc579bb9cdad27112"
    ),
    "audit_cosine_feasibility.py": (
        "020a9428c4a13088201f6bef5abafa6b3daee73a8ef20166efffd83147df2e35"
    ),
    "A14_COSINE_FEASIBILITY_PREFLIGHT.md": (
        "e4a66f142f2cd7458d566fbace4acd883634308534d7b5bc66cd47e4478d874b"
    ),
    "a14_cosine_feasibility_preflight.json": (
        "ae4d0d56b720a72682eeef55ad809e97d74a84631542d9de334d56af583754ad"
    ),
    "A14_COSINE_FEASIBILITY_IMPLEMENTATION_PREFLIGHT.md": (
        "1dc635235419f54f343cc9a0cf05f79ecd434ea85a7e3bf60ae248bf3f8ba8a4"
    ),
    "a14_cosine_feasibility_implementation_preflight.json": (
        "0bbf8860c0cfbe474b88e3193a35265e3b622477c42ccfbfcf3d8fcee2a467e2"
    ),
}
ORIGINAL_SOURCE_AUTHORS = {
    name: ORIGINAL_AUTHORS[name]
    for name in ("experiment_cosine_feasibility.py", "audit_cosine_feasibility.py")
}
PRIOR_REVIEWS = {
    "A14_cosine_feasibility_root_review_run001": (
        "94d7577ac27385c7d2ee2aab7e421b7b5d48a899b8c19308d4a5c6e11b5a843f",
        (1, 13, 0),
    ),
    "A14_cosine_feasibility_root_review_run002": (
        "34eb866f076cbc75226ff48b8079cb09b001fb7388f4d9944e0a3e5848652d18",
        (1, 15, 0),
    ),
}
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
CPU, ADMISSION, WALL, DIGITS = 300, 270, 900, 130
PATH_CACHE, ACTUAL_HASH_CACHE, OBSERVED_HASHES = {}, {}, {}
BASE_TREES, BASE_FILES = (), ()
BASE_PREFIX = BASE_SITE_LEXICAL = BASE_SITE = None
MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = 24000, 2 * 1024**3
SHA_PATTERN = re.compile(r"[0-9a-f]{64}\Z")
CASES = {"B4x12": (4, 12, 30), "B8x52": (8, 52, 234)}
BASELINE = {"B4x12": (520720662, 555774, 550141), "B8x52": (4267435214, 663704, 4460479)}
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
BRIDGE_PINS = {
    "results/limitation_program_20261001/A02_BM_native_financial_bridge_run002/manifest.json": (
        "78a8eea9dc937883b810cb6b3e2e26aec41297551b984a9c12bb15a435523162"
    ),
    (
        "results/limitation_program_20261001/"
        "A02_BM_native_financial_bridge_audit_run002/manifest.json"
    ): ("62074efc3bd5a20a9cbe72b3d020fd5c6bf13e32d41b188ef57570225dade2a0"),
}
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


def same(first, second, message):
    require(
        json.dumps(first, sort_keys=True, separators=(",", ":"), allow_nan=False)
        == json.dumps(second, sort_keys=True, separators=(",", ":"), allow_nan=False),
        message,
    )


def unsigned_word(value):
    require(type(value) is int and 0 <= value < 1 << W, "Canonical unsigned72 CONST")
    return value - (1 << W) if value >= 1 << 71 else value


def signed_coefficient(value):
    return native_word(value)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encode(value):
    value = Fraction(value)
    return [value.numerator, value.denominator]


def rational(value):
    require(
        type(value) is list
        and len(value) == 2
        and all(type(item) is int for item in value)
        and value[1] > 0,
        "Typed exact rational",
    )
    result = Fraction(*value)
    require(encode(result) == value, "Reduced rational encoding")
    return result


def nearest_fraction(value):
    value = Fraction(value)
    quotient, remainder = divmod(value.numerator, value.denominator)
    return quotient + int(
        2 * remainder > value.denominator or (2 * remainder == value.denominator and quotient % 2)
    )


def native_word(value):
    require(type(value) is int and -(1 << 71) <= value < 1 << 71, "Signed72 literal")
    return value


def native_range(value):
    require(
        type(value) is tuple
        and len(value) == 2
        and all(type(item) is int for item in value)
        and value[0] <= value[1],
        "Exact ordered integer interval representation",
    )
    if not (-(1 << 71) <= value[0] <= value[1] < 1 << 71):
        raise NativeRejectedError("Every selected and unselected full72 word is safe")
    return value


def interval_endpoint(value):
    sign, mantissa, exponent, bits = value
    require(type(bits) is int and bits >= 0, "Finite outward endpoint")
    return Fraction((-1 if sign else 1) * mantissa) * Fraction(2) ** exponent


def endpoints(value):
    return tuple(interval_endpoint(endpoint) for endpoint in value._mpi_)


def outward(mp, value):
    value = Fraction(value)
    return mp.iv.mpf(value.numerator) / mp.iv.mpf(value.denominator)


def actual_literal_error(raw, fractional_bits, true_value):
    native_word(raw)
    lower, upper = endpoints(true_value)
    point = Fraction(raw, 1 << fractional_bits)
    return max(abs(point - lower), abs(point - upper))


def authorize_literal(raw, fractional_bits, true_value, declared_error, declared_interval):
    lower, upper = endpoints(true_value)
    claimed = tuple(rational(value) for value in declared_interval)
    require(
        claimed[0] <= lower <= upper <= claimed[1],
        "Actual130 coefficient enclosure lies inside retained primary enclosure",
    )
    error = actual_literal_error(raw, fractional_bits, true_value)
    require(
        rational(declared_error) >= error >= 0,
        "Each actual literal error is independently authorized",
    )
    return error


def cordic_reference_literals(mp, raw_angles, raw_gain, started, *, require_half_ULP=True):
    """Fresh true angles and finite reciprocal gain; never use fitted samples."""
    require(
        len(raw_angles) == ITERATIONS and all(type(value) is int for value in raw_angles),
        "Exactly48 actual angle literals",
    )
    gain = outward(mp, 1)
    angles, records = [], []
    for index, raw in enumerate(raw_angles):
        check(started)
        native_word(raw)
        tangent = Fraction(1, 1 << index)
        angle = mp.iv.atan2(outward(mp, tangent), outward(mp, 1)) / (2 * mp.iv.pi)
        angles.append(angle)
        error = actual_literal_error(raw, CORDIC_F, angle)
        require(
            not require_half_ULP or error <= CORDIC_EPSILON / 2,
            "Actual CORDIC angle half-ULP premise, not inferred from generation",
        )
        require(raw > 0, "Positive CORDIC digital angle")
        records.append(
            dict(
                i=index,
                raw=raw,
                true_turns_enclosure=[encode(value) for value in endpoints(angle)],
                actual_abs_error_upper=encode(error),
                true_nearest_half_ULP_certified=error <= CORDIC_EPSILON / 2,
            )
        )
        gain *= mp.iv.sqrt(outward(mp, 1 + tangent * tangent))
    for index in range(1, ITERATIONS):
        check(started)
        require(
            endpoints(angles[index - 1])[1] < 2 * endpoints(angles[index])[0],
            "Strict angle relation used in the greedy induction",
        )
    gain_upper = endpoints(gain)[1]
    require(1 < gain_upper < 2, "Finite48 gain premise independently enclosed")
    reciprocal = 1 / gain
    gain_error = actual_literal_error(raw_gain, CORDIC_F, reciprocal)
    require(
        not require_half_ULP or gain_error <= CORDIC_EPSILON / 2,
        "Actual reciprocal-gain half-ULP premise independently enclosed",
    )
    require(0 < raw_gain < CORDIC_Q, "Positive subunit initial coordinate")
    return dict(
        angles=records,
        reciprocal_gain=dict(
            raw=raw_gain,
            true_reciprocal_gain_enclosure=[encode(value) for value in endpoints(reciprocal)],
            actual_abs_error_upper=encode(gain_error),
            true_nearest_half_ULP_certified=gain_error <= CORDIC_EPSILON / 2,
        ),
        finite_gain_enclosure=[encode(value) for value in endpoints(gain)],
        every_actual_half_ULP_premise_certified=gain_error <= CORDIC_EPSILON / 2
        and all(row["true_nearest_half_ULP_certified"] for row in records),
    )


def cordic_uniform_bound(mp, started):
    check(started)
    pi_upper = endpoints(mp.iv.pi)[1]
    vector = (3 * ITERATIONS + 1) * CORDIC_EPSILON
    angle = Fraction(1, 1 << (ITERATIONS - 1)) + 3 * pi_upper * ITERATIONS * CORDIC_EPSILON
    rounding = EPSILON / 2
    total = vector + angle + rounding
    require(total < EPSILON, "Fixed48/f56 paper target actually certified at130")
    return dict(
        independent_digits=130,
        vector_error_upper=encode(vector),
        radian_residual_upper=encode(angle),
        final_tie_even_f40_rounding_upper=encode(rounding),
        uniform_error_upper=encode(total),
        fixed48_strict_one_ULP_target=True,
        closed_domain_and_point_values=True,
        independent_derivation=[
            "Each selected rotation has gain sqrt(1+2^(-2i)); finite suffix gain is below2.",
            "Each two-coordinate signed-floor perturbation has Euclidean norm below sqrt2*2^-56.",
            "The propagated floor errors are below3*N*2^-56; "
            "initial reciprocal-gain error contributes below2^-56.",
            "Nearest-quarter folding gives |z0|<=1/8; a_(i-1)<2*a_i and48 "
            "actual half-ULP literal checks imply |zN|<=a47+N*2^-57.",
            "True applied angles differ from their digital literals by at most anotherN*2^-57; "
            "the chosen direction history does not alter this bound.",
            "Cosine and sine are1-Lipschitz in radians. Exact quarter reconstruction "
            "and axis values preserve this error bound.",
            "Signed ties-even f56-to-f40 adds at most2^-41; paid clipping to[-1,1] "
            "is nonexpansive relative to ideal cosine.",
        ],
    )


def pair_add(first, second):
    return native_range((first[0] + second[0], first[1] + second[1]))


def pair_subtract(first, second):
    return native_range((first[0] - second[1], first[1] - second[0]))


def pair_hull(first, second):
    return native_range((min(first[0], second[0]), max(first[1], second[1])))


def cordic_native_ranges(raw_angles, raw_gain, started):
    """Full eager branch histories, using simultaneous OLD coordinates."""
    require(len(raw_angles) == ITERATIONS, "Fixed48 native stages")
    x = native_range((native_word(raw_gain), raw_gain))
    y = native_range((0, 0))
    z = native_range((-(1 << 53), 1 << 53))
    records = []
    for index, raw in enumerate(raw_angles):
        check(started)
        angle = native_range((native_word(raw), raw))
        old_x, old_y, old_z = x, y, z
        shift_x = native_range((old_x[0] // (1 << index), old_x[1] // (1 << index)))
        shift_y = native_range((old_y[0] // (1 << index), old_y[1] // (1 << index)))
        x_plus, x_minus = pair_add(old_x, shift_y), pair_subtract(old_x, shift_y)
        y_plus, y_minus = pair_add(old_y, shift_x), pair_subtract(old_y, shift_x)
        z_plus, z_minus = pair_add(old_z, angle), pair_subtract(old_z, angle)
        x, y, z = pair_hull(x_plus, x_minus), pair_hull(y_plus, y_minus), pair_hull(z_plus, z_minus)
        records.append(
            dict(
                i=index,
                old_x_raw_bounds=list(old_x),
                old_y_raw_bounds=list(old_y),
                old_z_raw_bounds=list(old_z),
                shifted_x_raw_bounds=list(shift_x),
                shifted_y_raw_bounds=list(shift_y),
                x_plus_raw_bounds=list(x_plus),
                x_minus_raw_bounds=list(x_minus),
                y_plus_raw_bounds=list(y_plus),
                y_minus_raw_bounds=list(y_minus),
                z_plus_raw_bounds=list(z_plus),
                z_minus_raw_bounds=list(z_minus),
                selected_x_raw_bounds=list(x),
                selected_y_raw_bounds=list(y),
                selected_z_raw_bounds=list(z),
                direction_msb_full72_bank_bounds=[0, 1],
                angle_raw_bounds=list(angle),
                both_branches_and_old_state_retained=True,
            )
        )
    reconstructed = pair_hull(pair_hull(x, y), pair_hull((-x[1], -x[0]), (-y[1], -y[0])))
    quotient = native_range((reconstructed[0] // 65536, reconstructed[1] // 65536))
    incremented = pair_add(quotient, (1, 1))
    rounded = pair_hull(quotient, incremented)
    return dict(
        stages=records,
        quarter_reconstruction_raw_bounds=list(reconstructed),
        floor_quotient_raw_bounds=list(quotient),
        exact_rounding_residual_raw_bounds=[0, 65535],
        eager_incremented_quotient_raw_bounds=list(incremented),
        tie_even_rounded_raw_bounds=list(rounded),
        saturated_raw_bounds=[-Q, Q],
        exact_axis_raw_inputs=[0, Q // 4, Q // 2, 3 * Q // 4, Q],
        exact_axis_raw_outputs=[Q, 0, -Q, 0, Q],
        all_selected_and_unselected_words_safe=True,
        full72_history_words_before_fold_and_rounding=627,
        histories_not_discarded_for_cost=True,
        signed_shift_floor=True,
        full144_products_in_CORDIC_stage=0,
    )


def taylor_reference_coefficients(mp, rows, started):
    require(len(rows) == 64 * 7, "Exactly448 actual Taylor coefficients")
    records, weighted = [], []
    for segment in range(64):
        check(started)
        center_raw = (2 * segment + 1) << 33
        center = Fraction(center_raw, Q)
        error = Fraction(0)
        for degree in range(7):
            declared = rows[7 * segment + degree]
            require(
                declared["segment"] == segment
                and declared["degree"] == degree
                and declared["center_raw"] == center_raw,
                "Complete exact ordered64x7 derivative inventory",
            )
            raw = native_word(declared["raw"])
            coefficient = (
                (2 * mp.iv.pi) ** degree
                * mp.iv.cos(2 * mp.iv.pi * outward(mp, center) + degree * mp.iv.pi / 2)
                / factorial(degree)
            )
            actual_error = authorize_literal(
                raw,
                F,
                coefficient,
                declared["actual_abs_error_upper"],
                declared["true_coefficient_enclosure"],
            )
            half = actual_error <= EPSILON / 2
            if declared["true_nearest_half_ULP_certified"] is True:
                require(half, "Any claimed true-nearest Taylor premise independently checked")
            require(
                type(declared["true_nearest_half_ULP_certified"]) is bool,
                "Explicit Taylor rounding certification status",
            )
            literal_midpoint = (
                sum(rational(value) for value in declared["true_coefficient_enclosure"]) / 2
            )
            require(
                nearest_fraction(Q * literal_midpoint) == raw
                and rational(declared["exact_rounding_reference"]) == literal_midpoint
                and rational(declared["actual_abs_error_upper"])
                == max(
                    abs(Fraction(raw, Q) - rational(endpoint))
                    for endpoint in declared["true_coefficient_enclosure"]
                )
                and declared["true_nearest_half_ULP_certified"]
                is (rational(declared["actual_abs_error_upper"]) <= EPSILON / 2),
                "Single exact tie-even quantization of declared primary rational midpoint",
            )
            error += actual_error * LOCAL_RADIUS**degree
            records.append(
                dict(
                    segment=segment,
                    degree=degree,
                    center_raw=center_raw,
                    raw=raw,
                    true_coefficient_enclosure=[encode(value) for value in endpoints(coefficient)],
                    actual_abs_error_upper=encode(actual_error),
                    true_nearest_half_ULP_certified=half,
                )
            )
        weighted.append(error)
    remainder = endpoints((2 * mp.iv.pi * outward(mp, LOCAL_RADIUS)) ** 7 / factorial(7))[1]
    floor_error = EPSILON * sum((LOCAL_RADIUS**degree for degree in range(6)), Fraction(0))
    total = max(weighted) + remainder + floor_error
    return dict(
        coefficient_checks=records,
        segment_literal_error_uppers=[encode(value) for value in weighted],
        Taylor_degree6_remainder_upper=encode(remainder),
        literal_rounding_upper=encode(max(weighted)),
        Horner_floor_upper=encode(floor_error),
        uniform_error_upper=encode(total),
        actual_literal_errors_paid_without_inferred_half_ULP=True,
        no_fitting_or_minimax_optimality_claim=True,
        full_closed_local_intervals=True,
    )


def taylor_native_ranges(rows, started):
    require(len(rows) == 448, "Fixed64x7 native coefficient rows")
    local = (-Q // 128, Q // 128)
    result = []
    for segment in range(64):
        check(started)
        coefficients = [native_word(rows[7 * segment + degree]["raw"]) for degree in range(7)]
        value = (coefficients[-1], coefficients[-1])
        steps = []
        for degree in range(5, -1, -1):
            check(started)
            products = tuple(first * second for first in value for second in local)
            product = (min(products), max(products))
            if not -(1 << 143) <= product[0] <= product[1] < 1 << 143:
                raise NativeRejectedError("An actual full144 Horner product exceeds native range")
            floor = native_range((product[0] // Q, product[1] // Q))
            value = pair_add(floor, (coefficients[degree], coefficients[degree]))
            steps.append(
                dict(
                    degree=degree,
                    signed144_product_raw_bounds=list(product),
                    floored_product_raw_bounds=list(floor),
                    added_coefficient_raw=coefficients[degree],
                    output_raw_bounds=list(value),
                )
            )
        result.append(
            dict(
                segment=segment,
                center_raw=(2 * segment + 1) << 33,
                address_raw=segment,
                local_raw_bounds=list(local),
                coefficient_raw=coefficients,
                Horner_steps=steps,
                pre_saturation_raw_bounds=list(value),
                all_native72_product144_guards_passed=True,
            )
        )
    return dict(
        segments=result,
        endpoint_Q_routes_to_zero_before_any_eager_lookup=True,
        lookup_full72_address_bounds=[0, 63],
        high_address_bits_zero=True,
        table_literal_words=512,
        coefficient_literal_words=448,
        center_literal_words=64,
        full72_lookup_output_banks=8,
        exact_axis_overrides=True,
        final_saturation_raw_bounds=[-Q, Q],
    )


class BudgetCensoredError(RuntimeError):
    pass


class NativeRejectedError(ValueError):
    pass


def check(started, *, admission=False):
    cpu, wall = time.process_time(), time.monotonic() - started
    if cpu >= (ADMISSION if admission else CPU) or wall >= WALL:
        raise BudgetCensoredError("Fixed independent A14 CPU/wall censor")
    return cpu, wall


def start_clock():
    require(os.name == "nt" and ctypes.sizeof(ctypes.c_void_p) == 8, "Pinned Win64 runtime")
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.GetCurrentProcess.argtypes = []
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
    kernel.GetProcessTimes.restype = wintypes.BOOL
    fields = [wintypes.FILETIME() for _ in range(4)]
    require(
        kernel.GetProcessTimes(kernel.GetCurrentProcess(), *(ctypes.byref(v) for v in fields)),
        "Actual creation time unavailable",
    )
    ticks = (fields[0].dwHighDateTime << 32) | fields[0].dwLowDateTime
    age_ns = time.time_ns() - (ticks - 116444736000000000) * 100
    require(age_ns >= 0, "Actual creation precedes clock observation")
    return time.monotonic() - age_ns / 1000000000


class GraphAudit:
    """Own backward traversal on actual SSA; never constructs or evaluates it."""

    def __init__(self, target, started):
        self.target, self.started, self.nodes, self.ancestor_cache = target, started, {}, {}
        require((target["width"], target["fraction_bits"]) == (72, 40), "Native W72/F40")
        arities = {
            "input": 0,
            "const": 0,
            "add": 2,
            "sub": 2,
            "mul": 2,
            "cmul": 1,
            "lt": 2,
            "select": 3,
            "positive": 1,
            "msb": 1,
            "bits": 1,
            "shift": 2,
            "sqrt": 1,
            "lookup": 1,
        }
        next_value = 0
        for row in target["nodes"]:
            check(started)
            op, args, out, params = (row[k] for k in ("op", "args", "out", "params"))
            require(
                op in arities and type(args) is list and len(args) == arities[op], "Typed arity"
            )
            require(type(out) is list and type(params) is dict and out, "Typed node shape")
            require(all(type(v) is int and v in self.nodes for v in args), "Topological dependency")
            require(
                out == list(range(next_value, next_value + len(out))),
                "Exact contiguous output slots",
            )
            require(all(type(v) is int for v in out), "Typed SSA identities")
            next_value += len(out)
            require(op == "lookup" or len(out) == 1, "Single output native primitive")
            if op == "const":
                require(set(params) == {"value"}, "Exact constant fields")
                unsigned_word(params["value"])
            elif op == "cmul":
                require(set(params) == {"c"}, "Exact coefficient fields")
                signed_coefficient(params["c"])
            elif op == "bits":
                require(
                    set(params) == {"shift", "width", "signed"}
                    and type(params["shift"]) is int
                    and type(params["width"]) is int
                    and 1 <= params["width"] <= 72
                    and type(params["signed"]) is bool,
                    "Exact bit-extraction fields",
                )
            elif op == "lookup":
                require(
                    set(params) == {"table", "bits"} and type(params["bits"]) is int,
                    "Exact lookup fields",
                )
                table = target["tables"][params["table"]]
                require(
                    len(table) == 1 << params["bits"]
                    and all(len(entry) == len(out) for entry in table),
                    "Complete table shape",
                )
                for entry in table:
                    for coefficient in entry:
                        signed_coefficient(coefficient)
            elif op == "input":
                require(set(params) == {"name", "bits", "preparation"}, "Exact input fields")
            else:
                require(params == {}, "No undeclared arithmetic parameters")
            for value in out:
                self.nodes[value] = row

    def node(self, value, kind=None, params=None):
        check(self.started)
        require(type(value) is int and value in self.nodes, "Actual SSA identity")
        row = self.nodes[value]
        require(kind is None or row["op"] == kind, "Expected native operation")
        if params is not None:
            same(row["params"], params, "Exact native operation parameters")
        return row

    def constant(self, value, expected=None):
        result = unsigned_word(self.node(value, "const")["params"]["value"])
        require(expected is None or result == expected, "Actual decoded constant")
        return result

    def ancestors(self, value):
        if value not in self.ancestor_cache:
            pending, values = [value], set()
            while pending:
                check(self.started)
                current = pending.pop()
                if current not in values:
                    values.add(current)
                    pending.extend(self.node(current)["args"])
            self.ancestor_cache[value] = values
        return self.ancestor_cache[value]

    def clamp(self, value, low=None, high=None):
        topflag, middle, upper = self.node(value, "select")["args"]
        require(self.node(topflag, "lt")["args"] == [middle, upper], "Exact upper clamp")
        bottomflag, lower, original = self.node(middle, "select")["args"]
        require(self.node(bottomflag, "lt")["args"] == [original, lower], "Exact lower clamp")
        require(self.constant(lower, low) < self.constant(upper, high), "Ordered clamp literals")
        return original

    def midpoint(self, value, input_value):
        args = self.node(value, "add")["args"]
        shifted = [v for v in args if self.node(v)["op"] == "bits"]
        require(len(shifted) == 1, "One midpoint conversion")
        require(
            self.node(shifted[0], "bits", {"shift": -8, "width": 72, "signed": False})["args"]
            == [input_value],
            "Exact q32 to f40 conversion",
        )
        self.constant(next(v for v in args if v != shifted[0]), 128)

    def interpolation(self, result, table_name, input_value):
        bins, degree, lower, bits = (32, 8, Q, 5) if table_name == "log" else (64, 7, 0, 6)
        candidates = {
            tuple(self.node(v)["out"])
            for v in self.ancestors(result)
            if self.node(v)["op"] == "lookup" and self.node(v)["params"]["table"] == table_name
        }
        require(len(candidates) == 1, "One table supplies every Horner coefficient")
        coefficients = next(iter(candidates))
        require(len(coefficients) == degree + 1, "All actual polynomial coefficients")
        address = self.node(coefficients[0], "lookup", {"table": table_name, "bits": bits})["args"][
            0
        ]
        bounded = self.node(address, "bits", {"shift": 40 - bits, "width": bits, "signed": False})[
            "args"
        ][0]
        if lower:
            bounded, literal = self.node(bounded, "sub")["args"]
            self.constant(literal, lower)
        require(
            self.clamp(bounded, lower, lower + Q - 1) == input_value, "Interpolation input binding"
        )
        current, local = result, None
        for coefficient in coefficients[:-1]:
            args = self.node(current, "add")["args"]
            require(coefficient in args, "Horner coefficient order")
            factors = self.node(next(v for v in args if v != coefficient), "mul")["args"]
            if local is None:
                possible = [v for v in factors if self.node(v)["op"] == "sub"]
                require(len(possible) == 1, "One local variable in Horner")
                local = possible[0]
            require(local in factors, "Every Horner product uses same local variable")
            current = next(v for v in factors if v != local)
        require(current == coefficients[-1], "Horner terminal coefficient")
        actual, center = self.node(local, "sub")["args"]
        require(actual == bounded, "Local variable uses bounded argument")
        args = self.node(center, "add")["args"]
        shifted = [v for v in args if self.node(v)["op"] == "bits"]
        require(len(shifted) == 1, "Exact local center shift")
        require(
            self.node(shifted[0], "bits", {"shift": bits - 40, "width": 72, "signed": False})[
                "args"
            ]
            == [address],
            "Local center derives from same address",
        )
        self.constant(next(v for v in args if v != shifted[0]), lower + Q // (2 * bins))
        return dict(
            output=result,
            input=input_value,
            address=address,
            local=local,
            lookup_outputs=list(coefficients),
            floors=degree,
        )

    def joint_pair(self, first, second, input_u, input_v, ln2):
        products = [self.node(v, "mul")["args"] for v in (first, second)]
        shared = set(products[0]) & set(products[1])
        require(len(shared) == 1, "Actual pair shares one radius")
        radius = next(iter(shared))
        positive = self.node(radius, "sqrt")["args"][0]
        product = self.node(positive, "positive")["args"][0]
        logarithm = self.node(product, "cmul", {"c": -2 * Q})["args"][0]
        addends = self.node(logarithm, "add")["args"]
        exponent_terms = [v for v in addends if self.node(v)["op"] == "cmul"]
        require(len(exponent_terms) == 1, "Unique integer exponent literal product")
        term = exponent_terms[0]
        scaled = self.node(term, "cmul", {"c": ln2})["args"][0]
        exponent = self.node(scaled, "bits", {"shift": -40, "width": 72, "signed": False})["args"][
            0
        ]
        top, f = self.node(exponent, "sub")["args"]
        self.constant(f, 40)
        safe = self.node(top, "msb")["args"][0]
        flag, tiny, midpoint_u = self.node(safe, "select")["args"]
        self.constant(tiny, 1)
        require(self.node(flag, "lt")["args"] == [midpoint_u, tiny], "Actual positive-input guard")
        self.midpoint(midpoint_u, input_u)
        polynomial = next(v for v in addends if v != term)
        lookups = {
            tuple(self.node(v)["out"])
            for v in self.ancestors(polynomial)
            if self.node(v)["op"] == "lookup"
        }
        require(len(lookups) == 1, "Unique original log lookup")
        address = self.node(next(iter(lookups))[0])["args"][0]
        shifted = self.node(address)["args"][0]
        bounded = self.node(shifted, "sub")["args"][0]
        mantissa = self.clamp(bounded, Q, 2 * Q - 1)
        u, negated = self.node(mantissa, "shift")["args"]
        require(u == safe, "Same positive midpoint is normalized")
        zero, same_exponent = self.node(negated, "sub")["args"]
        self.constant(zero, 0)
        require(same_exponent == exponent, "Exact normalization exponent")
        log_scope = self.interpolation(polynomial, "log", mantissa)
        cosines = [next(v for v in args if v != radius) for args in products]
        turns = []
        for cosine in cosines:
            lookups = {
                tuple(self.node(v)["out"])
                for v in self.ancestors(cosine)
                if self.node(v)["op"] == "lookup"
            }
            require(len(lookups) == 1, "Unique original cosine lookup")
            address = self.node(next(iter(lookups))[0])["args"][0]
            bounded = self.node(address)["args"][0]
            turns.append(self.clamp(bounded, 0, Q - 1))
        midpoint_v, wrapped = turns
        self.midpoint(midpoint_v, input_v)
        total = self.node(wrapped, "bits", {"shift": 0, "width": 40, "signed": False})["args"][0]
        args = self.node(total, "add")["args"]
        require(midpoint_v in args, "Both angles derive from same midpoint")
        self.constant(next(v for v in args if v != midpoint_v), 3 * Q // 4)
        scopes = [self.interpolation(v, "cos", a) for v, a in zip(cosines, turns, strict=True)]
        dependencies = {
            v
            for root in (first, second)
            for v in self.ancestors(root)
            if self.node(v)["op"] == "input"
        }
        require(dependencies == {input_u, input_v}, "Exactly two independent pair input words")
        return dict(
            normal_values=[first, second],
            raw_uniform_values=[input_u, input_v],
            radius=radius,
            log=log_scope,
            cosines=scopes,
            original_shared_pair_preserved=True,
        )

    def sum_terms(self, value, stops):
        pending, result = [value], Counter()
        while pending:
            check(self.started)
            current = pending.pop()
            if current in stops:
                result[current] += 1
            else:
                pending.extend(self.node(current, "add")["args"])
        return result


def initialize(started):
    """Independent admission of the actual local interpreter; stdlib only."""
    global BASE_PREFIX, BASE_TREES, BASE_FILES, BASE_SITE_LEXICAL, BASE_SITE
    PATH_CACHE.clear()
    ACTUAL_HASH_CACHE.clear()
    OBSERVED_HASHES.clear()
    require(sys.dont_write_bytecode is True, "Interpreter startup -B is mandatory")
    require(
        Path.cwd().resolve() == ROOT and Path(__file__).resolve() == AUTHOR,
        "Exact auditor module and working directory",
    )
    require(Path(sys.executable).resolve() == LAUNCHER, "Pinned isolated launcher")
    require(
        Path(sys.prefix).resolve() == ROOT / ".context/frontier_t0_env",
        "Exact isolated interpreter prefix",
    )
    require(site.ENABLE_USER_SITE is False, "User site must be disabled")
    for name in ("PYTHONPATH", "PYTHONHOME", "SAGE_ROOT", "MPMATH_SAGE"):
        require(not os.environ.get(name), "Unexpected runtime override: " + name)
    os.environ["MPMATH_NOGMPY"] = os.environ["MPMATH_NOSAGE"] = "1"
    BASE_PREFIX = Path(sys.base_prefix).resolve(strict=True)
    BASE_SITE_LEXICAL = BASE_PREFIX / "Lib/site-packages"
    BASE_SITE = BASE_SITE_LEXICAL.resolve()
    base = Path(getattr(sys, "_base_executable", sys.executable)).resolve(strict=True)
    require(base.parent == BASE_PREFIX, "Actual adjacent base interpreter")
    BASE_TREES = tuple(
        (BASE_PREFIX / name).resolve(strict=True)
        for name in ("Lib", "DLLs")
        if (BASE_PREFIX / name).is_dir()
    )
    BASE_FILES = tuple(
        path.resolve(strict=True) for path in BASE_PREFIX.iterdir() if path.is_file()
    )
    require(base in BASE_FILES, "Actual base executable is captured")
    forbidden_imports()
    check(started)


def forbidden_imports():
    banned = ("numpy", "scipy", "numba", "llvmlite", "qiskit", "gmpy", "gmpy2", "sage")
    for name in sys.modules:
        require(
            not any(name == prefix or name.startswith(prefix + ".") for prefix in banned),
            "Forbidden numerical or SDK import: " + name,
        )
        if name.startswith("research."):
            require(
                name
                in (
                    "research.limitation_program_20261001",
                    "research.limitation_program_20261001.audit_cosine_feasibility_v2",
                ),
                "Auditor must not import producer or other research helpers",
            )


def permitted(path):
    if BASE_SITE is not None and path.is_relative_to(BASE_SITE):
        return False
    return (
        path.is_relative_to(ROOT)
        or path == BASE_PREFIX
        or path in BASE_FILES
        or any(path.is_relative_to(root) for root in BASE_TREES)
    )


def canonical_path(path, started, *, fresh=False):
    check(started)
    value = Path(path)
    require(not value.drive or value.is_absolute(), "Ambiguous drive-relative path forbidden")
    require(
        BASE_SITE_LEXICAL is None or not value.absolute().is_relative_to(BASE_SITE_LEXICAL),
        "Unreachable base site-packages lexical paths forbidden",
    )
    lexical = str(value.absolute())
    if not fresh and lexical in PATH_CACHE:
        check(started)
        return PATH_CACHE[lexical]
    actual = value.resolve(strict=True)
    require(permitted(actual), "Outside ROOT or exact observed base-runtime scopes")
    require(
        lexical not in PATH_CACHE or PATH_CACHE[lexical] == actual,
        "Previously confined lexical path redirected",
    )
    PATH_CACHE[lexical] = actual
    PATH_CACHE.setdefault(str(actual), actual)
    check(started)
    return actual


def fingerprint(path):
    data = path.stat()
    return (
        data.st_dev,
        data.st_ino,
        data.st_size,
        data.st_mtime_ns,
        data.st_ctime_ns,
        getattr(data, "st_file_attributes", None),
        getattr(data, "st_reparse_tag", None),
    )


def actual_digest(path, started, *, fresh=False):
    check(started)
    require(permitted(path), "Pre-read confinement of actual hash path")
    identity, key = fingerprint(path), str(path)
    require(path.is_file(), "Actual regular byte input")
    if not fresh and key in ACTUAL_HASH_CACHE and ACTUAL_HASH_CACHE[key][0] == identity:
        check(started)
        return ACTUAL_HASH_CACHE[key][1]
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            check(started)
            state.update(block)
            check(started)
    require(fingerprint(path) == identity, "Actual bytes changed during SHA observation")
    result = state.hexdigest()
    require(
        key not in OBSERVED_HASHES or OBSERVED_HASHES[key] == result,
        "First independently observed actual SHA changed",
    )
    OBSERVED_HASHES.setdefault(key, result)
    ACTUAL_HASH_CACHE[key] = (identity, result)
    check(started)
    return result


def sha(path, started, *, fresh=False):
    return actual_digest(canonical_path(path, started, fresh=fresh), started, fresh=fresh)


def root_key(path, started):
    actual = canonical_path(path, started)
    require(actual.is_relative_to(ROOT), "ROOT-relative field confinement")
    return actual.relative_to(ROOT).as_posix()


def bind(frozen, external, path, expected, started):
    check(started)
    require(type(expected) is str and SHA_PATTERN.fullmatch(expected), "Canonical SHA256")
    actual = canonical_path(path, started)
    mapping = frozen if actual.is_relative_to(ROOT) else external
    key = actual.relative_to(ROOT).as_posix() if actual.is_relative_to(ROOT) else str(actual)
    require(key not in mapping or mapping[key] == expected, "Conflicting expected SHA binding")
    require(actual_digest(actual, started) == expected, "Actual byte SHA differs: " + key)
    mapping[key] = expected
    check(started)
    return actual


def read_bytes(path, started):
    actual = canonical_path(path, started)
    identity = fingerprint(actual)
    require(
        actual.is_file() and identity[2] <= 128 * 1024**2, "Bounded regular source/artifact input"
    )
    chunks, state, total = [], hashlib.sha256(), 0
    with actual.open("rb") as stream:
        while block := stream.read(1 << 20):
            check(started)
            total += len(block)
            require(total <= identity[2], "Text input grew while reading")
            state.update(block)
            check(started)
            chunks.append(block)
    require(
        total == identity[2] and fingerprint(actual) == identity,
        "Exact text bytes stable during read",
    )
    data = b"".join(chunks)
    observed = state.hexdigest()
    check(started)
    key = str(actual)
    require(
        key not in OBSERVED_HASHES or OBSERVED_HASHES[key] == observed,
        "JSON/source read contradicts original actual SHA",
    )
    OBSERVED_HASHES.setdefault(key, observed)
    ACTUAL_HASH_CACHE[key] = (identity, observed)
    return data


def read_json(path, started):
    value = json.loads(read_bytes(path, started))
    check(started)
    return value


def write_json(path, value, started):
    check(started)
    data = (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()
    check(started)
    require(len(data) <= 128 * 1024**2, "Bounded JSON output")
    with Path(path).open("xb") as stream:
        for offset in range(0, len(data), 1 << 20):
            check(started)
            stream.write(data[offset : offset + (1 << 20)])
            check(started)


def verify_maps(frozen, external, started):
    for mapping, parent in ((frozen, ROOT), (external, None)):
        for key, expected in mapping.items():
            check(started)
            path = parent / key if parent is not None else Path(key)
            require(sha(path, started) == expected, "Immutable map byte mismatch: " + key)


def final_fresh(frozen, external, started):
    """Fresh confinement for all aliases and fresh full bytes for every actual path."""
    for lexical, expected_path in tuple(PATH_CACHE.items()):
        check(started)
        require(
            canonical_path(lexical, started, fresh=True) == expected_path,
            "Final independent lexical alias mismatch",
        )
    expected = {}
    for mapping, parent in ((frozen, ROOT), (external, None)):
        for key, value in mapping.items():
            check(started)
            actual = canonical_path(parent / key if parent is not None else key, started)
            require(actual not in expected or expected[actual] == value, "Equal-SHA final merge")
            expected[actual] = value
    observed = {Path(key): value for key, value in OBSERVED_HASHES.items()}
    union = set(expected) | set(observed)
    for path in sorted(union):
        check(started)
        actual = canonical_path(path, started, fresh=True)
        value = actual_digest(actual, started, fresh=True)
        require(path not in expected or expected[path] == value, "Final expected SHA differs")
        require(path not in observed or observed[path] == value, "Final observed SHA differs")
    return len(union)


def reject_unreachable_origin(path, started):
    """Deny excluded lexical/physical origins even when their files disappeared."""
    check(started)
    candidate = Path(path)
    require(not candidate.drive or candidate.is_absolute(), "Ambiguous runtime origin drive")
    require(
        BASE_SITE_LEXICAL is None or not candidate.absolute().is_relative_to(BASE_SITE_LEXICAL),
        "Unreachable base site-packages lexical origin forbidden",
    )
    actual = candidate.resolve(strict=False)
    require(
        BASE_SITE is None or not actual.is_relative_to(BASE_SITE),
        "Unreachable base site-packages physical origin forbidden",
    )
    check(started)


def runtime_candidates(root, started):
    """Prune the unreachable base site directory before traversing its entries."""
    root = canonical_path(root, started)
    if root.is_file():
        yield root
        return
    require(root.is_dir(), "Finite actual runtime directory")
    for current, directory_names, filenames in os.walk(root, topdown=True, followlinks=False):
        check(started)
        directory = canonical_path(current, started)
        require(
            directory == root or directory.is_relative_to(root),
            "Runtime walk directory confinement",
        )
        retained = []
        for name in directory_names:
            check(started)
            candidate = directory / name
            if candidate.absolute() == BASE_SITE_LEXICAL:
                continue
            actual = canonical_path(candidate, started)
            require(actual.is_relative_to(root), "Runtime directory alias escape")
            require(
                not candidate.is_symlink() and not candidate.is_junction(),
                "Untraversed runtime directory links forbidden",
            )
            retained.append(name)
        directory_names[:] = retained
        for name in filenames:
            check(started)
            candidate = directory / name
            if candidate.is_file():
                actual = canonical_path(candidate, started)
                require(actual.is_relative_to(root), "Runtime file alias escape")
                yield actual


def bootstrap_runtime_paths(site_root, started):
    """Exact actual hook roots and preexisting loaded venv files, without package expansion."""
    paths = set()
    for candidate in site_root.iterdir():
        check(started)
        hook_name = candidate.name.split(".", 1)[0]
        customize_names = ("sitecustomize", "usercustomize")
        hook_file = candidate.is_file() and (
            candidate.suffix.lower() == ".pth"
            or hook_name in customize_names
            and candidate.suffix.lower() in (".py", ".pyc", ".pyd")
        )
        hook_package = candidate.is_dir() and candidate.name in customize_names
        if not (hook_file or hook_package):
            continue
        reject_unreachable_origin(candidate, started)
        require(candidate.absolute().is_relative_to(site_root), "Lexical isolated startup hook")
        actual = canonical_path(candidate, started)
        require(actual.is_relative_to(site_root), "Physical isolated startup hook")
        require(actual.is_file() or actual.is_dir(), "Actual startup hook file or package")
        paths.add(actual)
        if candidate.suffix == ".py":
            cached = Path(cache_from_source(str(candidate)))
            reject_unreachable_origin(cached, started)
            if cached.is_file():
                require(
                    cached.absolute().is_relative_to(site_root), "Lexical startup cache confinement"
                )
                cache_actual = canonical_path(cached, started)
                require(
                    cache_actual.is_relative_to(site_root), "Physical startup cache confinement"
                )
                paths.add(cache_actual)
    for module in tuple(sys.modules.values()):
        check(started)
        if module is None:
            continue
        for origin in (getattr(module, "__file__", None), getattr(module, "__cached__", None)):
            if not origin:
                continue
            reject_unreachable_origin(origin, started)
            lexical = Path(origin).absolute()
            if Path(origin).is_file():
                actual = canonical_path(origin, started)
                if lexical.is_relative_to(site_root):
                    require(
                        actual.is_relative_to(site_root), "Loaded venv bootstrap alias confinement"
                    )
                if actual.is_relative_to(site_root) and not actual.is_relative_to(
                    site_root / "mpmath"
                ):
                    paths.add(actual)
    return sorted(paths)


def venv_adjacent_runtime(prefix, started):
    """Exact admitted prefix entries; capture adjacent files, caches and real packages."""
    paths, membership = set(), []
    for candidate in sorted(prefix.iterdir()):
        check(started)
        actual = canonical_path(candidate, started)
        require(
            actual == candidate.absolute() and actual.parent == prefix,
            "Adjacent actual venv entry is direct and has no redirected alias",
        )
        if candidate.is_file():
            kind = "file"
            require(actual.parent == prefix, "Actual adjacent venv regular file")
            paths.add(actual)
        else:
            require(candidate.is_dir(), "Actual adjacent venv file or directory")
            kind = "directory"
            importable_package = any(
                (candidate / name).is_file() for name in ("__init__.py", "__init__.pyc")
            )
            if candidate.name == "__pycache__" or importable_package:
                require(candidate.name not in ("Lib", "Scripts"), "No ambiguous venv package root")
                paths.add(actual)
        membership.append([candidate.name, kind])
    return sorted(paths), sorted(membership)


def runtime_inventory(frozen, external, started):
    prefix = canonical_path(sys.prefix, started)
    config = prefix / "pyvenv.cfg"
    require(
        "include-system-site-packages = false" in read_bytes(config, started).decode().lower(),
        "Isolated actual venv config",
    )
    site_root = canonical_path(prefix / "Lib/site-packages", started)
    distribution = metadata.distribution("mpmath")
    require(
        distribution.version == "1.3.0" and distribution.files,
        "Fixed installed mpmath RECORD inventory",
    )
    metadata_roots = set()
    for member in distribution.files:
        check(started)
        path = canonical_path(distribution.locate_file(member), started)
        for parent in (path, *path.parents):
            if parent.name.endswith(".dist-info"):
                metadata_roots.add(parent)
                break
    require(len(metadata_roots) == 1, "Exactly one actual mpmath metadata root")
    metadata_root = metadata_roots.pop()
    require(metadata_root.parent == site_root, "Distribution metadata confined to pinned site")
    roots = [
        config,
        prefix / "Scripts",
        site_root / "mpmath",
        metadata_root,
        *BASE_TREES,
        *BASE_FILES,
    ]
    bootstrap_paths = bootstrap_runtime_paths(site_root, started)
    roots.extend(bootstrap_paths)
    adjacent_paths, adjacent_membership = venv_adjacent_runtime(prefix, started)
    roots.extend(adjacent_paths)
    for path in (ROOT / "research/__init__.py", RESEARCH / "__init__.py"):
        if path.is_file():
            roots.append(path)
    for path in (ROOT / "research/__init__.py", RESEARCH / "__init__.py", AUTHOR, PRODUCER_AUTHOR):
        cached = Path(cache_from_source(str(path)))
        if cached.is_file():
            roots.append(cached)
    paths, total = set(), 0
    actual_roots = []
    for route in roots:
        root = canonical_path(route, started)
        actual_roots.append(str(root))
        for candidate in runtime_candidates(root, started):
            check(started)
            if not candidate.is_file():
                continue
            path = canonical_path(candidate, started)
            require(path == root or path.is_relative_to(root), "Actual runtime tree confinement")
            if path in paths:
                continue
            total += path.stat().st_size
            paths.add(path)
            require(
                len(paths) <= MAX_RUNTIME_FILES and total <= MAX_RUNTIME_BYTES,
                "Fixed entire runtime inventory cap",
            )
            bind(frozen, external, path, sha(path, started), started)
    absent = []
    allowed_roots = {ROOT, prefix, site_root, BASE_PREFIX, *BASE_TREES}
    for entry in sys.path:
        check(started)
        path = Path(entry or ROOT)
        reject_unreachable_origin(path, started)
        if path.exists():
            require(
                canonical_path(path, started) in allowed_roots
                or canonical_path(path, started) in BASE_FILES,
                "Unexpected actual module search path",
            )
        else:
            actual = path.resolve()
            require(
                actual
                == BASE_PREFIX
                / ("python" + str(sys.version_info.major) + str(sys.version_info.minor) + ".zip"),
                "Only standard absent interpreter zip",
            )
            absent.append(str(actual))
    return dict(
        python_version=sys.version,
        executable=str(canonical_path(sys.executable, started)),
        base_executable=str(canonical_path(sys._base_executable, started)),
        base_prefix=str(BASE_PREFIX),
        venv_prefix=str(prefix),
        mpmath_version="1.3.0",
        backend="python",
        MPMATH_NOGMPY="1",
        MPMATH_NOSAGE="1",
        startup_bytecode_disabled=True,
        user_site_disabled=True,
        runtime_inventory=dict(
            roots=actual_roots,
            actual_file_paths=sorted(str(p) for p in paths),
            files=len(paths),
            bytes=total,
        ),
        sys_path=list(sys.path),
        external_runtime_trees=[str(p) for p in BASE_TREES],
        external_adjacent_files=[str(p) for p in BASE_FILES],
        absent_standard_runtime_paths=absent,
        excluded_base_site_packages=str(BASE_SITE),
        excluded_base_site_packages_lexical=str(BASE_SITE_LEXICAL),
        base_site_packages_import_rejected=True,
        bootstrap_hook_and_loaded_venv_paths=[str(path) for path in bootstrap_paths],
        standard_Lib_excludes_only_unreachable_base_site_packages=True,
        other_installed_venv_packages_not_blanket_admitted=True,
        exact_sys_prefix_search_path_admitted=True,
        venv_adjacent_runtime_paths=[str(path) for path in adjacent_paths],
        venv_root_directory_membership=adjacent_membership,
    )


def verify_runtime(record, frozen, external, started):
    check(started)
    require(
        record["python_version"] == sys.version
        and record["executable"] == str(canonical_path(sys.executable, started))
        and record["base_executable"] == str(canonical_path(sys._base_executable, started))
        and record["base_prefix"] == str(BASE_PREFIX)
        and record["venv_prefix"] == str(canonical_path(sys.prefix, started))
        and record["mpmath_version"] == metadata.version("mpmath") == "1.3.0",
        "Actual interpreter and dependency version provenance",
    )
    same(record["sys_path"], list(sys.path), "Exact interpreter search path snapshot")
    same(
        record["external_runtime_trees"],
        [str(p) for p in BASE_TREES],
        "Exact observed base tree scopes",
    )
    same(
        record["external_adjacent_files"],
        [str(p) for p in BASE_FILES],
        "Exact observed adjacent runtime files",
    )
    require(
        record["backend"] == "python"
        and record["startup_bytecode_disabled"] is True
        and record["user_site_disabled"] is True
        and sys.dont_write_bytecode is True
        and site.ENABLE_USER_SITE is False
        and os.environ.get("MPMATH_NOGMPY") == os.environ.get("MPMATH_NOSAGE") == "1",
        "Exact isolated pure Python import policy",
    )
    require(
        record["excluded_base_site_packages"] == str(BASE_SITE)
        and record["excluded_base_site_packages_lexical"] == str(BASE_SITE_LEXICAL)
        and record["base_site_packages_import_rejected"] is True,
        "Exact unreachable base site-packages exclusion and import rejection",
    )
    require(
        record["standard_Lib_excludes_only_unreachable_base_site_packages"] is True
        and record["other_installed_venv_packages_not_blanket_admitted"] is True,
        "Full remaining runtime and selected venv package policy",
    )
    site_root = canonical_path(Path(sys.prefix) / "Lib/site-packages", started)
    prefix = canonical_path(sys.prefix, started)
    require(
        record["exact_sys_prefix_search_path_admitted"] is True,
        "Only exact isolated venv-prefix search root additionally admitted",
    )
    adjacent_paths, adjacent_membership = venv_adjacent_runtime(prefix, started)
    same(
        [str(path) for path in adjacent_paths],
        record["venv_adjacent_runtime_paths"],
        "Exact adjacent venv runtime roots",
    )
    same(
        adjacent_membership,
        record["venv_root_directory_membership"],
        "Exact finite venv-root directory membership",
    )
    same(
        [str(path) for path in bootstrap_runtime_paths(site_root, started)],
        record["bootstrap_hook_and_loaded_venv_paths"],
        "Actual complete startup hook membership",
    )
    allowed_sys_roots = {ROOT, prefix, site_root, BASE_PREFIX, *BASE_TREES}
    for entry in sys.path:
        check(started)
        candidate = Path(entry or ROOT)
        reject_unreachable_origin(candidate, started)
        if candidate.exists():
            actual = canonical_path(candidate, started)
            require(
                actual in allowed_sys_roots or actual in BASE_FILES,
                "Unexpected current sys.path root",
            )
    paths = set()
    for route in record["runtime_inventory"]["roots"]:
        root = canonical_path(route, started)
        for candidate in runtime_candidates(root, started):
            check(started)
            if candidate.is_file():
                path = canonical_path(candidate, started)
                require(
                    path == root or path.is_relative_to(root),
                    "Fresh runtime membership confinement",
                )
                paths.add(path)
    same(
        sorted(str(p) for p in paths),
        record["runtime_inventory"]["actual_file_paths"],
        "Complete existing source/cache/metadata/runtime file membership",
    )
    total = 0
    for path in paths:
        check(started)
        total += path.stat().st_size
        require(
            len(paths) <= MAX_RUNTIME_FILES and total <= MAX_RUNTIME_BYTES,
            "Actual complete runtime cap",
        )
        key = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)
        mapping = frozen if path.is_relative_to(ROOT) else external
        require(
            key in mapping and sha(path, started) == mapping[key],
            "Entire runtime byte origin is frozen",
        )
    require(
        record["runtime_inventory"]["files"] == len(paths)
        and record["runtime_inventory"]["bytes"] == total,
        "Exact recorded runtime count and bytes",
    )
    for path in record["absent_standard_runtime_paths"]:
        check(started)
        require(not Path(path).exists(), "Recorded absent interpreter zip appeared")
    forbidden_imports()


def loaded_origins(frozen, external, started):
    forbidden_imports()
    result = []
    for name, module in tuple(sys.modules.items()):
        check(started)
        if module is None:
            continue
        for kind, origin in (
            ("source", getattr(module, "__file__", None)),
            ("cache", getattr(module, "__cached__", None)),
        ):
            if origin:
                reject_unreachable_origin(origin, started)
            if origin and Path(origin).is_file():
                path = canonical_path(origin, started)
                key = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)
                mapping = frozen if path.is_relative_to(ROOT) else external
                require(
                    key in mapping and sha(path, started) == mapping[key],
                    "Actual loaded module source/existing cache not frozen: " + name,
                )
                result.append(dict(module=name, kind=kind, path=key, sha256=mapping[key]))
    return result


def map_inputs(record, frozen, external, started):
    for field, is_external in (("frozen_inputs", False), ("external_runtime_inputs", True)):
        mapping = record[field]
        require(type(mapping) is dict, "Complete recognized source/protocol byte map")
        for key, expected in mapping.items():
            check(started)
            require(type(key) is str, "Typed input map path")
            route = Path(key) if is_external else ROOT / key
            require(
                route.is_absolute() if is_external else not Path(key).is_absolute(),
                "Exact external-absolute / ROOT-relative map convention",
            )
            actual = bind(frozen, external, route, expected, started)
            canonical = str(actual) if is_external else actual.relative_to(ROOT).as_posix()
            require(
                canonical == key and (not is_external or not actual.is_relative_to(ROOT)),
                "Canonical source-map path; no aliases or ROOT path in external map",
            )


def elapsed(started):
    return dict(process_CPU_seconds=time.process_time(), wall_seconds=time.monotonic() - started)


def copy_exact(source, destination, frozen, external, started):
    source = canonical_path(source, started)
    expected, identity = sha(source, started), fingerprint(source)
    with source.open("rb") as incoming, Path(destination).open("xb") as outgoing:
        while block := incoming.read(1 << 20):
            check(started)
            outgoing.write(block)
            check(started)
    require(fingerprint(source) == identity, "Copy source remains immutable")
    bind(frozen, external, destination, expected, started)


def owned_artifacts(output, started):
    result, total = {}, 0
    for candidate in output.rglob("*"):
        check(started)
        if candidate.is_file():
            if candidate == output / "manifest.json":
                continue
            path = canonical_path(candidate, started)
            require(
                path.is_relative_to(output) and path.name != "manifest.json",
                "Owned output confinement and no manifest reuse",
            )
            key = path.relative_to(output).as_posix()
            require(key not in result, "No aliased owned output")
            total += path.stat().st_size
            require(len(result) < 64 and total <= 128 * 1024**2, "Finite owned artifact caps")
            result[key] = sha(path, started)
    return result


def saved_library(source, started):
    route = source["library_workspace_relative"].replace("\\", "/")
    require(".." not in route.split("/"), "No saved library traversal")
    marker = route.lower().find("/results/")
    actual = canonical_path(ROOT / (route[marker + 1 :] if marker >= 0 else route), started)
    require(actual.is_relative_to(PROGRAM), "Exact ROOT-owned saved native library")
    return actual


def descriptor_profile(entry, operation, *, brent_kung=False, source_format=None):
    """An actual owned descriptor, never a guessed narrow or controlled price."""
    require(
        entry["op"] == operation and entry.get("params", entry.get("spec", {}).get("params")) == {},
        "Exact dynamic primitive",
    )
    spec = entry.get("spec")
    if spec is None:
        require(
            operation == "lt"
            and source_format is not None
            and source_format["format"] == "hierarchical-clean-xor-source-v1"
            and source_format["word_width"] == W
            and source_format["fraction_bits"] == F,
            "Only legacy full72 LT may use the independently bound source word format",
        )
        spec = {}
    else:
        require(
            type(spec) is dict
            and spec["width"] == W
            and (operation in ("add", "sub") or spec["fraction_bits"] == F),
            "Every present actual native precision field stays exact",
        )
    same(entry["args"], [list(range(W)), list(range(W, 2 * W))], "Exact full72 input ABI")
    same(entry["outs"], [list(range(2 * W, 3 * W))], "Exact full72 dirty output ABI")
    for contract in (entry.get("input_contract"), spec.get("input_contract")):
        require(not contract, "No input-contract discount for changed operands")
    require(
        not spec.get("active_operand_bits") and not entry.get("active_operand_bits"),
        "No active-bit borrowing",
    )
    require(spec["op"] == operation and spec["params"] == {}, "Exact primitive specification")
    if brent_kung:
        require(
            operation in ("add", "sub")
            and spec["variant"] == "brent-kung"
            and spec["lowering"] == "clean-xor-prefix-add-sub-v1",
            "ONE accepted BK72 raw modular ADD/SUB family",
        )
    if operation == "mul":
        require(
            spec["fraction_bits"] == F and spec["product_width"] == W + F,
            "Explicit actual full72/f40/window112 MUL, no f56 transfer",
        )
    resources = entry["resources"]
    require(
        all(type(resources[field]) is int and resources[field] >= 0 for field in RESOURCE_FIELDS)
        and resources["t_count"] == 7 * resources["ccx"]
        and type(resources["qubits"]) is int
        and resources["qubits"] >= 3 * W,
        "Complete actual exact7T counts/private workspace",
    )
    return dict(
        resources={field: resources[field] for field in RESOURCE_FIELDS},
        private_scratch_qubits=resources["qubits"] - 3 * W,
        full72_input_arity=2,
        full72_output_words=1,
        actual_leaf_key=entry.get("key", Path(entry["gate_file"].replace("\\", "/")).stem),
        actual_gate_SHA256=entry["sha256"],
        raw_modular_word_operation=True,
        fraction_label_transfer_only_for_ADD_SUB_LT=operation in ("add", "sub", "lt"),
    )


def direct_profile(x=0, cx=0, ccx=0, *, arity, outputs=1, scratch=0, recipe):
    require(
        all(type(value) is int and value >= 0 for value in (x, cx, ccx, arity, outputs, scratch)),
        "Fixed exact symbolic recipe counts",
    )
    return dict(
        resources=dict(
            source_gates=x + cx + ccx,
            x=x,
            cx=cx,
            ccx=ccx,
            t_count=7 * ccx,
            t_depth=7 * ccx,
            clifford_t_depth=x + cx + 15 * ccx,
            clifford_cx=cx + 6 * ccx,
            clifford_h=2 * ccx,
        ),
        private_scratch_qubits=scratch,
        full72_input_arity=arity,
        full72_output_words=outputs,
        recipe=recipe,
        symbolic_recipe_not_emitted_native_descriptor=True,
        exact7T_no_relative_phase=True,
    )


def select_profile():
    return direct_profile(
        cx=5 * W,
        ccx=W,
        arity=3,
        scratch=W,
        recipe="outXORb;diffXORa,b;CCX(condLSB,diff,out)perbit;literal_inverse_diff",
    )


def equality_profile():
    return direct_profile(
        cx=4 * W + 1,
        ccx=2 * (W - 1),
        arity=2,
        scratch=2 * W - 1,
        recipe="diff72=aXORb;invert72;71AND_chain;XORflag;inverse71AND;inverse_invert_and_diff",
        x=2 * W,
    )


def signed_lt_profile():
    return direct_profile(
        x=6 * W + 4,
        cx=6 * W + 1,
        ccx=4 * W - 2,
        arity=2,
        scratch=3 * W,
        recipe="flip both input MSBs; G=(not a)andb,P=not(a XORb),C=G XOR(P*Cprevious); "
        "copy last borrow; literal inverse allGPC; restoreMSBs",
    )


def lookup_profile(table):
    require(
        len(table) == 64
        and all(len(row) == 8 for row in table)
        and all(type(value) is int for row in table for value in row),
        "Exactly64 center-plus-seven-coefficient rows",
    )
    bits = sum((native_word(value) % (1 << W)).bit_count() for row in table for value in row)
    negative_controls = sum(6 - row.bit_count() for row in range(64))
    return direct_profile(
        x=2 * negative_controls,
        cx=bits,
        ccx=2 * 5 * 64,
        arity=1,
        outputs=8,
        scratch=5,
        recipe="each6bitminterm:negative_control_X;5CCX_chain;literal_bit_CX;literal_inverse_chain_and_X",
    )


def symbolic_plan(row_id, raw_angles, raw_gain, taylor_rows, started):
    """Independently reproduce only the fixed finite, fully retained word recipe."""
    nodes, constants, next_bank = [], {}, 0

    def append(operation, arguments=(), *, parameter=None, outputs=1, scale=None):
        nonlocal next_bank
        check(started)
        require(
            all(type(value) is int and 0 <= value < next_bank for value in arguments),
            "Actual typed plan topology",
        )
        result = list(range(next_bank, next_bank + outputs))
        next_bank += outputs
        nodes.append(
            dict(
                op=operation,
                args=list(arguments),
                params={} if parameter is None else parameter,
                outputs=result,
                fraction_bits=scale,
            )
        )
        return result[0] if outputs == 1 else result

    def constant(raw, scale):
        identity = (native_word(raw), scale)
        if identity not in constants:
            constants[identity] = append("CONST", parameter={"raw": raw}, scale=scale)
        return constants[identity]

    def bits(value, kind, amount=0, width=W, scale=0):
        require(
            kind in ("left", "signed_right", "unsigned_right", "low")
            and 0 <= amount < W
            and 1 <= width <= W,
            "Fixed full72 bit map",
        )
        mapping = []
        for index in range(W):
            if kind == "left":
                source = index - amount
                source = source if source >= 0 else None
            elif kind == "signed_right":
                source = min(index + amount, W - 1)
            elif kind == "unsigned_right":
                source = index + amount if index < width and index + amount < W else None
            else:
                source = index if index < width else None
            mapping.append(source)
        return append(
            "BITS",
            [value],
            parameter=dict(kind=kind, amount=amount, width=width, output_to_input_bit=mapping),
            scale=scale,
        )

    def arithmetic(operation, first, second, scale):
        return append(operation, [first, second], scale=scale)

    def flag(operation, first, second):
        return append(operation, [first, second], scale=0)

    def select(condition, first, second, scale):
        return append("SELECT", [condition, first, second], scale=scale)

    def clamp(value, low, high, scale):
        lo, hi = constant(low, scale), constant(high, scale)
        low_flag = flag("LT", value, lo)
        middle = select(low_flag, lo, value, scale)
        high_flag = flag("LT", hi, middle)
        return select(high_flag, hi, middle, scale)

    input_value = append("INPUT", scale=F)
    bounded = clamp(input_value, 0, Q, F)
    if row_id == ROW_IDS[0]:
        require(len(raw_angles) == ITERATIONS, "Only48 fixed stages")
        shifted = bits(bounded, "left", amount=2, scale=F)
        numerator = arithmetic("ADD", shifted, constant(Q // 2, F), F)
        quarter = bits(numerator, "unsigned_right", amount=40, width=3)
        local = arithmetic(
            "SUB",
            bits(bounded, "left", amount=16, scale=CORDIC_F),
            bits(quarter, "left", amount=54, scale=CORDIC_F),
            CORDIC_F,
        )
        zero = constant(0, CORDIC_F)
        x, y, z = constant(raw_gain, CORDIC_F), zero, local
        for index, raw in enumerate(raw_angles):
            check(started)
            angle = constant(raw, CORDIC_F)
            sx, sy = (
                bits(x, "signed_right", amount=index, scale=CORDIC_F),
                bits(y, "signed_right", amount=index, scale=CORDIC_F),
            )
            negative = flag("LT", z, zero)
            xp, xm = arithmetic("SUB", x, sy, CORDIC_F), arithmetic("ADD", x, sy, CORDIC_F)
            yp, ym = arithmetic("ADD", y, sx, CORDIC_F), arithmetic("SUB", y, sx, CORDIC_F)
            zp, zm = arithmetic("SUB", z, angle, CORDIC_F), arithmetic("ADD", z, angle, CORDIC_F)
            x, y, z = (
                select(negative, xm, xp, CORDIC_F),
                select(negative, ym, yp, CORDIC_F),
                select(negative, zm, zp, CORDIC_F),
            )
        quadrant = bits(quarter, "low", width=2)
        minus_x, minus_y = (
            arithmetic("SUB", zero, x, CORDIC_F),
            arithmetic("SUB", zero, y, CORDIC_F),
        )
        reconstructed = y
        for raw, value in ((2, minus_x), (1, minus_y), (0, x)):
            reconstructed = select(
                flag("EQ", quadrant, constant(raw, 0)), value, reconstructed, CORDIC_F
            )
        quotient = bits(reconstructed, "signed_right", amount=16, scale=F)
        residual = bits(reconstructed, "low", width=16)
        half = constant(32768, 0)
        greater, tie = flag("LT", half, residual), flag("EQ", residual, half)
        parity = bits(quotient, "low", width=1)
        increment = flag("FLAG_OR", greater, flag("FLAG_AND", tie, parity))
        rounded = arithmetic("ADD", quotient, increment, F)
    else:
        require(row_id == ROW_IDS[1] and len(taylor_rows) == 448, "Only fixedTaylor6x64")
        endpoint = flag("EQ", bounded, constant(Q, F))
        safe_lookup_input = select(endpoint, constant(0, F), bounded, F)
        address = bits(safe_lookup_input, "unsigned_right", amount=34, width=6)
        table = [
            [
                (2 * segment + 1) << 33,
                *[native_word(taylor_rows[7 * segment + degree]["raw"]) for degree in range(7)],
            ]
            for segment in range(64)
        ]
        loaded = append(
            "LOOKUP",
            [address],
            parameter=dict(
                bits=6,
                table=table,
                recipe="negative controls; five-chain CCX; literal CX; inverse chain; restore",
            ),
            outputs=8,
            scale=F,
        )
        local = arithmetic("SUB", safe_lookup_input, loaded[0], F)
        rounded = loaded[7]
        for degree in range(5, -1, -1):
            check(started)
            rounded = arithmetic("ADD", arithmetic("MUL", rounded, local, F), loaded[degree + 1], F)
    output = clamp(rounded, -Q, Q, F)
    for raw, result in zip((0, Q // 4, Q // 2, 3 * Q // 4, Q), (Q, 0, -Q, 0, Q), strict=True):
        equal = flag("EQ", bounded, constant(raw, F))
        output = select(equal, constant(result, F), output, F)
    return dict(
        schema="a14-clean-cosine-typed-plan-v1",
        row_id=row_id,
        word_width=W,
        external_fraction_bits=F,
        input_bank=input_value,
        output_bank=output,
        allocated_full72_banks=next_bank,
        nodes=nodes,
        constant_deduplication="exact raw and fractional scale",
        all_eager_values_retained=True,
        output_XOR_bits=W,
        clean_recipe="literal F; XOR72 output; literal reversed F",
        historical_graph_or_gate_builder_used=False,
    )


def plan_resources(plan, profiles, started):
    """Literal direct recipes plus actual owner-matched dynamic arithmetic."""
    forward = dict.fromkeys(RESOURCE_FIELDS, 0)
    word_banks, private, copies = 0, 0, 0
    operation_counts = Counter()
    events = []
    for node in plan["nodes"]:
        check(started)
        operation = node["op"].lower()
        operation_counts[operation] += 1
        if operation == "input":
            continue
        word_banks += len(node["outputs"])
        if operation in ("add", "sub", "mul"):
            require(operation in profiles, "RESOURCE_REJECTED: missing full72 matched " + operation)
            profile = profiles[operation]
        elif operation == "lt":
            profile = signed_lt_profile()
        elif operation == "const":
            profile = direct_profile(
                x=(node["params"]["raw"] % (1 << W)).bit_count(), arity=0, recipe="literalX72"
            )
        elif operation == "select":
            profile = select_profile()
        elif operation == "eq":
            profile = equality_profile()
        elif operation == "lookup":
            profile = lookup_profile(node["params"]["table"])
        elif operation == "bits":
            mapping = node["params"]["output_to_input_bit"]
            require(
                len(mapping) == W
                and all(bit is None or type(bit) is int and 0 <= bit < W for bit in mapping),
                "Exact fixed full72 bit-copy map",
            )
            cx = sum(bit is not None for bit in mapping)
            profile = direct_profile(
                cx=cx, arity=1, recipe="fixed72bit_copy_sign_or_zero_extension"
            )
        elif operation == "flag_and":
            profile = direct_profile(ccx=1, arity=2, recipe="CCXtwoLSBtozero_outputLSB")
        elif operation == "flag_or":
            profile = direct_profile(
                cx=2, ccx=1, arity=2, recipe="XORa,XORb,CCXab_tozero_outputLSB"
            )
        else:
            raise ValueError("Unsupported fixed symbolic primitive")
        require(
            profile["full72_input_arity"] == len(node["args"])
            and profile["full72_output_words"] == len(node["outputs"]),
            "Actual full72 call ABI",
        )
        resources = profile["resources"]
        for field in RESOURCE_FIELDS:
            forward[field] += resources[field]
        copied = 2 * W * len(node["args"])
        copies += copied
        for field in ("cx", "source_gates", "clifford_cx", "clifford_t_depth"):
            forward[field] += copied
        private = max(private, profile["private_scratch_qubits"])
        events.append(
            dict(op=operation, outputs=node["outputs"], argument_copy_CX=copied, profile=profile)
        )
    clean = {field: 2 * value for field, value in forward.items()}
    for field in ("cx", "source_gates", "clifford_cx", "clifford_t_depth"):
        clean[field] += W
    history_floor = 627 if plan["row_id"] == ROW_IDS[0] else 0
    word_banks = max(word_banks, history_floor)
    qubits = W * (word_banks + 3) + private
    return dict(
        operation_counts=dict(operation_counts),
        events=events,
        function_forward_resource_estimate=forward,
        function_clean_resource_estimate=clean,
        full72_argument_copy_CX_per_forward=copies,
        dirty_output_XOR_CX=W,
        outer_function_argument_copy_CX_per_clean_invocation=2 * W,
        full72_retained_word_banks=word_banks,
        external_input_output_and_outer_copy_banks=3,
        function_private_scratch_qubits=private,
        function_logical_qubit_upper=qubits,
        standalone_cap=131072,
        standalone_cap_fit=qubits <= 131072,
        exact7T_phase_paid=True,
        relative_phase_substitution=False,
        symbolic_recipe_not_emitted_or_scheduled=True,
    )


def implementation_policy(started):
    policy = read_json(IMPLEMENTATION, started)
    require(
        policy["schema"] == "a14-cosine-feasibility-audit-only-implementation-preflight-v2",
        "Exact preregistered implementation schema",
    )
    same(
        policy["CPU_admission_wall_seconds"],
        [CPU, ADMISSION, WALL],
        "Unchanged fixed independent limits",
    )
    require(
        policy["primary_digits"] == 90
        and policy["independent_digits"] == DIGITS
        and policy["threads"] == 1,
        "Fixed precision/thread policy",
    )
    require(
        policy["runtime_backend"] == "python" and policy["mpmath_version"] == "1.3.0",
        "Exact pure interval backend",
    )
    require(
        policy["gate_emission_authorized"] is False and policy["full_G2"] is False,
        "A component screen never authorizes replacement adoption",
    )
    require(
        set(policy["author_sha256"]) == {AUTHOR.name},
        "Only the new independent audit module",
    )
    require(
        set(policy["method_document_SHA256"]) == {METHOD.name, METHOD_DOC.name},
        "Exact held method pair",
    )
    for field, parent in (("author_sha256", RESEARCH), ("method_document_SHA256", RESEARCH)):
        for name, expected in policy[field].items():
            check(started)
            require(
                type(expected) is str and SHA_PATTERN.fullmatch(expected),
                "Every release pin must be non-null before prepare",
            )
            require(sha(parent / name, started) == expected, "Actual reviewed author/method bytes")
    same(
        policy["original_author_SHA256"], ORIGINAL_AUTHORS, "All six original immutable author pins"
    )
    same(
        policy["original_source_author_SHA256"],
        ORIGINAL_SOURCE_AUTHORS,
        "Original source author pair",
    )
    require(
        policy["source_manifest_SHA256"] == SOURCE_SHA256
        and policy["prior_failed_audit_manifest_SHA256"] == PRIOR_AUDIT_SHA256
        and policy["literal_diagnostic_manifest_SHA256"] == LITERAL_DIAGNOSTIC_SHA256
        and policy["literal_diagnostic_root_review_manifest_SHA256"]
        == LITERAL_DIAGNOSTIC_REVIEW_SHA256
        and policy["operational_audit_version"] == 2
        and policy["previous_failed_audit_credit"] == 0
        and policy["source_receipt"] == SOURCE.relative_to(ROOT).as_posix()
        and policy["audit_receipt"] == OUTPUT.relative_to(ROOT).as_posix(),
        "Exact audit-only source, prior failure and fresh route",
    )
    same(
        policy["prior_root_review_manifest_SHA256"],
        {name: value[0] for name, value in PRIOR_REVIEWS.items()},
        "Both original static review manifests remain strict",
    )
    for name, expected in ORIGINAL_AUTHORS.items():
        check(started)
        require(sha(RESEARCH / name, started) == expected, "Original six bytes unchanged")
    for key, expected in BRIDGE_PINS.items():
        require(
            policy["existing_owner_manifest_SHA256"].get(key) == expected,
            "Actual original financial source and independent audit pins",
        )
    same(policy["fixed_rows"], list(ROW_IDS), "Exactly the two preregistered candidate rows")
    same(policy["owned_caps_files_bytes"], [64, 128 * 1024**2], "Fixed artifact caps")
    method = read_json(METHOD, started)
    require(
        method["finite_scope"]["CORDIC_screens"] == 1
        and method["finite_scope"]["Taylor_comparators"] == 1
        and method["finite_scope"]["minimax_comparators"] == 0,
        "No search-family substitution",
    )
    require(
        method["CORDIC"]["iterations"] == 48
        and method["CORDIC"]["fraction_bits"] == 56
        and method["Taylor_comparator"]["degree"] == 6
        and method["Taylor_comparator"]["segments"] == 64,
        "Fixed architectures",
    )
    return policy


def prior_audit_provenance(policy, frozen, external, started):
    """Bind complete original failed and release maps without result promotion."""
    same(policy["original_author_SHA256"], ORIGINAL_AUTHORS, "Pinned original author set")
    records = []
    packets = [(PRIOR_AUDIT, PRIOR_AUDIT_SHA256, (13, 697, 2842))]
    packets.extend((PROGRAM / name, pin, counts) for name, (pin, counts) in PRIOR_REVIEWS.items())
    packets.extend(
        (
            (LITERAL_DIAGNOSTIC, LITERAL_DIAGNOSTIC_SHA256, (8, 716, 2842)),
            (LITERAL_DIAGNOSTIC_REVIEW, LITERAL_DIAGNOSTIC_REVIEW_SHA256, (1, 5, 0)),
        )
    )
    for receipt, expected, counts in packets:
        check(started)
        manifest_path = bind(frozen, external, receipt / "manifest.json", expected, started)
        manifest = read_json(manifest_path, started)
        require(
            manifest.get("manifest_self_hash_excluded") is True
            and not (receipt / "FAILED_UNSEALED.json").exists(),
            "Original sealed packet has exact self-hash and no overriding marker",
        )
        fields = ("files", "frozen_inputs", "external_runtime_inputs")
        require(
            tuple(len(manifest.get(field, {})) for field in fields) == counts,
            "Complete exact original owned, frozen and external maps",
        )
        owned = set()
        records.append(
            dict(
                owner=receipt.name,
                source_map="manifest",
                original_key=root_key(manifest_path, started),
                verified_input_path=root_key(manifest_path, started),
                sha256=expected,
                expected_hash_waived=False,
            )
        )
        for field, key, path, value in owner_maps(manifest, receipt, started):
            check(started)
            actual = bind(frozen, external, path, value, started)
            if field == "external_runtime_inputs":
                require(
                    not actual.is_relative_to(ROOT) and str(actual) == key,
                    "Canonical exact original external key",
                )
                route = str(actual)
            else:
                require(
                    not Path(key).is_absolute() and "\\" not in key and ".." not in Path(key).parts,
                    "Canonical relative original key",
                )
                if field == "files":
                    require(
                        actual.is_relative_to(receipt) and actual != receipt / "manifest.json",
                        "Exact original owned receipt confinement",
                    )
                    relative = actual.relative_to(receipt).as_posix()
                    require(
                        key in (relative, actual.relative_to(ROOT).as_posix()),
                        "Owned key uses its exact ROOT or receipt spelling",
                    )
                    require(relative not in owned, "No original owned alias")
                    owned.add(relative)
                else:
                    require(
                        actual.is_relative_to(ROOT) and actual.relative_to(ROOT).as_posix() == key,
                        "Exact ROOT-relative frozen key",
                    )
                route = actual.relative_to(ROOT).as_posix()
            records.append(
                dict(
                    owner=receipt.name,
                    source_map=field,
                    original_key=key,
                    verified_input_path=route,
                    sha256=value,
                    expected_hash_waived=False,
                )
            )
        require(
            set(owned_artifacts(receipt, started)) == owned,
            "Complete actual original owned inventory",
        )
        if receipt == PRIOR_AUDIT:
            require(
                manifest["completed"] is False
                and manifest["passed"] is False
                and manifest["budget_censored"] is False,
                "Original independent failure remains uncensored and unapproved",
            )
            failure = read_json(receipt / "failure.json", started)
            outcome = read_json(receipt / "completion_outcome.json", started)
            require(
                failure["failed"] is True
                and failure["error_type"] == "ValueError"
                and failure["error"]
                == "Fresh130 true-angle inclusion and actual absolute error authorization"
                and failure["phase"] == "run"
                and failure["new_test_credit"] == 0,
                "Actual original literal authorization failure retained exactly",
            )
            require(
                outcome["completed"] is False
                and outcome["passed"] is False
                and outcome["failed"] is True
                and outcome["budget_censored"] is False
                and outcome["independent_audit_passed"] is False
                and outcome["new_test_credit"] == 0,
                "Failed original outcome cannot authorize scientific rows",
            )
            require(
                not (receipt / "summary.json").exists()
                and not (receipt / "independent_fixed_frontier.json").exists()
                and all(not (receipt / (row + ".json")).exists() for row in ROW_IDS),
                "No original independent row certificate or screen PASS",
            )
        elif receipt == LITERAL_DIAGNOSTIC:
            require(
                manifest["schema"] == "a14-literal-interval-diagnostic-manifest-v1"
                and manifest["completed"] is True
                and manifest["passed"] is True
                and manifest["budget_censored"] is False
                and manifest["diagnostic_only"] is True
                and manifest["original_expected_hashes_waived"] is False,
                "Actual bounded literal diagnostic completed with integrity only",
            )
            summary = read_json(receipt / "summary.json", started)
            outcome = read_json(receipt / "completion_outcome.json", started)
            diagnostics = read_json(receipt / "angle_gain_diagnostics.json", started)
            require(
                summary["completed"] is True
                and summary["passed"] is True
                and summary["diagnostic_complete"] is True
                and summary["budget_censored"] is False
                and summary["fixed_angle_count"] == 48
                and summary["finite_gain_count"] == 1
                and summary["actual_comparison_failing_indices"] == [0]
                and summary["first_actual_comparison_failing_index"] == 0
                and summary["gain_comparison_passes"] is True
                and summary["source_manifest_sha256"] == SOURCE_SHA256
                and summary["failed_audit_manifest_sha256"] == PRIOR_AUDIT_SHA256
                and summary["original_audit_remains_failed"] is True
                and summary["original_primary_remains_provisional"] is True,
                "Actual failing index is solely zero; this prerequisite is not row approval",
            )
            require(
                outcome["completed"] is True
                and outcome["passed"] is True
                and outcome["diagnostic_complete"] is True
                and outcome["budget_censored"] is False
                and all(
                    summary[field] is False and outcome[field] is False
                    for field in (
                        "candidate_certificate",
                        "independent_audit_passed",
                        "adoption",
                        "full_G2",
                        "cost_transfer",
                    )
                )
                and summary["new_test_credit"] == outcome["new_test_credit"] == 0,
                "Diagnostic completion supplies no candidate/audit/financial/cost credit",
            )
            rows = diagnostics["angle_rows"]
            require(
                len(rows) == 48
                and [row["i"] for row in rows] == list(range(48))
                and rows[0]["original_guard_comparison_passes"] is False
                and all(row["original_guard_comparison_passes"] is True for row in rows[1:])
                and diagnostics["reciprocal_gain"]["original_guard_comparison_passes"] is True
                and diagnostics["actual_comparison_failing_indices"] == [0],
                "All original numerical comparison diagnostics retained, no guard waiver",
            )
            exact = rows[0]["exact_analytic_a0_identity_diagnostic"]
            require(
                rational(exact["point"]) == Fraction(1, 8)
                and exact["actual_raw_equals_Q_over8"] is True
                and exact["primary_contains_exact_point"] is True
                and exact["independent130_contains_exact_point"] is True
                and rational(exact["exact_literal_error"]) == 0
                and exact["exact_literal_error_no_greater_than_saved"] is True
                and exact["numerical_interval_not_replaced"] is True
                and exact["no_original_audit_guard_waived"] is True,
                "Exact first-angle diagnostic supports the fixed analytic witness only",
            )
        elif receipt == LITERAL_DIAGNOSTIC_REVIEW:
            summary = read_json(receipt / "summary.json", started)
            require(
                summary["schema"] == "root-a14-literal-diagnostic-static-READY-v1"
                and summary["passed"] is True
                and summary["ready"] is True
                and summary["root_and_independent_TEXT_static_reviews_passed"] is True
                and summary["new_three_author_pins_frozen"] is True
                and summary["completed_diagnostic_is_not_scientific_audit"] is True
                and summary["old_audit_remains_FAILED"] is True
                and summary["new_test_credit"] == 0
                and all(
                    summary[field] is False
                    for field in ("candidate_approval", "full_G2", "adoption")
                ),
                "Literal diagnostic review is static-only and leaves old audit failed",
            )
        else:
            summary = read_json(receipt / "summary.json", started)
            require(
                summary["passed"] is True
                and summary["ready"] is True
                and summary["release_six_source_pins_frozen"] is True
                and summary["root_and_two_independent_TEXT_static_reviews"] is True
                and summary["new_fixture_credit"] == 0
                and all(
                    summary[field] is False for field in ("full_G2", "adoption", "cost_transfer")
                ),
                "Original reviews have static-only zero-credit scope",
            )
            if receipt.name.endswith("run002"):
                same(summary["fixed_rows"], list(ROW_IDS), "Corrected original display IDs")
    for name, expected in ORIGINAL_AUTHORS.items():
        check(started)
        bind(frozen, external, RESEARCH / name, expected, started)
        bind(frozen, external, SOURCE / "executed_code" / name, expected, started)
    return dict(
        schema="a14-prior-independent-audit-provenance-v2",
        records=records,
        original_failed_audit_credit=0,
        original_failed_audit_remains_failed=True,
        original_failure_did_not_record_index=True,
        actual_diagnostic_failing_indices=[0],
        actual_failing_index_from_separate_completed_diagnostic=True,
        no_expected_hash_waiver=True,
    )


def owner_maps(manifest, receipt, started):
    """Normalize metadata only; preserve every original expected-map reference."""
    if "files" not in manifest:
        require(
            all(
                type(k) is str and type(v) is str and SHA_PATTERN.fullmatch(v)
                for k, v in manifest.items()
            ),
            "Accepted legacy flat manifest",
        )
        result = []
        for key, expected in manifest.items():
            check(started)
            require(
                not Path(key).is_absolute() and ".." not in Path(key).parts, "Confined flat map"
            )
            path = (
                ROOT / key
                if key.startswith(("results/", "research/", "docs/", "manuscript/", ".context/"))
                else receipt / key
            )
            result.append(("files", key, path, expected))
        return result
    require(manifest.get("manifest_self_hash_excluded") is True, "No self-hash convention override")
    result = []
    for field in ("files", "frozen_inputs", "external_runtime_inputs"):
        mapping = manifest.get(field, {})
        require(type(mapping) is dict, "Recognized original complete byte map")
        for key, expected in mapping.items():
            check(started)
            require(
                type(key) is str and type(expected) is str and SHA_PATTERN.fullmatch(expected),
                "Exact typed original binding",
            )
            if field == "external_runtime_inputs":
                require(Path(key).is_absolute(), "Only canonical external absolute keys")
                path = Path(key)
            elif field == "files":
                path = (
                    ROOT / key
                    if key.startswith(
                        ("results/", "research/", "docs/", "manuscript/", ".context/")
                    )
                    else receipt / key
                )
            else:
                require(not Path(key).is_absolute(), "ROOT-relative frozen key")
                path = ROOT / key
            require(".." not in Path(key).parts, "No map traversal spelling")
            result.append((field, key, path, expected))
    return result


def bind_owners(policy, frozen, external, started):
    owners, memberships, all_owned, member_index = {}, [], {}, {}
    for key, expected in sorted(policy["existing_owner_manifest_SHA256"].items()):
        check(started)
        require(
            not Path(key).is_absolute() and key.endswith("/manifest.json"),
            "Exact ROOT owner-manifest route",
        )
        manifest_path = bind(frozen, external, ROOT / key, expected, started)
        require(manifest_path.relative_to(ROOT).as_posix() == key, "No owner alias")
        data = read_json(manifest_path, started)
        rows = owner_maps(data, manifest_path.parent, started)
        owners[key] = (data, rows)
        owned = {}
        for field, original, path, pin in rows:
            check(started)
            if path.is_relative_to(ROOT):
                member = path.relative_to(ROOT).as_posix()
                member_index.setdefault(member, []).append(
                    dict(
                        owner_manifest=key,
                        source_map=field if "files" in data else "flat_owned_files",
                        original_key=original,
                        original_expected_sha256=pin,
                    )
                )
            if field == "files" and key in BRIDGE_PINS:
                actual = canonical_path(path, started)
                require(
                    actual.is_relative_to(manifest_path.parent) and actual.name != "manifest.json",
                    "Original owned membership confinement",
                )
                relative = actual.relative_to(manifest_path.parent).as_posix()
                require(relative not in owned, "No original owned aliases")
                owned[relative] = pin
                all_owned[actual.relative_to(ROOT).as_posix()] = pin
            elif field == "files":
                require(
                    path.is_relative_to(ROOT),
                    "Historical owner metadata has a confined lexical ROOT route",
                )
                member = path.relative_to(ROOT).as_posix()
                require(
                    member not in all_owned or all_owned[member] == pin,
                    "No conflicting original ownership hashes",
                )
                all_owned[member] = pin
        if key in BRIDGE_PINS:
            actual_names = set()
            for path in manifest_path.parent.rglob("*"):
                check(started)
                if path.is_file() and path.name != "manifest.json":
                    resolved = canonical_path(path, started)
                    require(
                        resolved.is_relative_to(manifest_path.parent),
                        "Original owner directory confinement",
                    )
                    actual_names.add(resolved.relative_to(manifest_path.parent).as_posix())
            require(actual_names == set(owned), "Complete exact original owned inventory")
    archives = policy.get("archived_origin_routes", {})
    for owner, (data, rows) in owners.items():
        if owner not in BRIDGE_PINS:
            continue
        for field, original, path, expected in rows:
            check(started)
            actual = canonical_path(path, started)
            route_kind = "current_original"
            if sha(actual, started) != expected:
                require(field == "frozen_inputs", "Owned/external byte mismatches are never waived")
                replacement = archives.get(owner, {}).get(original)
                require(
                    type(replacement) is str
                    and replacement in all_owned
                    and all_owned[replacement] == expected,
                    "Scoped exact original-owner archival membership",
                )
                actual = canonical_path(ROOT / replacement, started)
                route_kind = "archived_exact_owned_bytes"
            bind(frozen, external, actual, expected, started)
            memberships.append(
                dict(
                    owner_manifest=owner,
                    source_map=field,
                    original_key=original,
                    verified_input_path=actual.relative_to(ROOT).as_posix()
                    if actual.is_relative_to(ROOT)
                    else str(actual),
                    sha256=expected,
                    route=route_kind,
                    expected_hash_waived=False,
                )
            )
    for key, expected in sorted(policy["existing_source_member_SHA256"].items()):
        check(started)
        require(
            any(row["original_expected_sha256"] == expected for row in member_index.get(key, [])),
            "Selected native metadata belongs to an actual original owner",
        )
        actual = bind(frozen, external, ROOT / key, expected, started)
        require(actual.relative_to(ROOT).as_posix() == key, "Selected source route has no alias")
        found = [row for row in member_index[key] if row["original_expected_sha256"] == expected]
        require(found, "Actual selected original member ownership")
        memberships.append(
            dict(path=key, sha256=expected, original_memberships=found, expected_hash_waived=False)
        )
    return memberships


def terminal_source(policy, frozen, external, started):
    bind(frozen, external, SOURCE / "manifest.json", SOURCE_SHA256, started)
    require(
        not (SOURCE / "FAILED_UNSEALED.json").exists() and not (SOURCE / "failure.json").exists(),
        "Reject failed or partial producer packet",
    )
    manifest = read_json(SOURCE / "manifest.json", started)
    require(
        manifest["schema"] == "a14-cosine-feasibility-terminal-manifest-v1"
        and manifest["manifest_self_hash_excluded"] is True
        and manifest["completed"] is True
        and manifest["passed"] is True
        and manifest["budget_censored"] is False
        and manifest["original_expected_hashes_waived"] is False,
        "Actual exclusive source terminal",
    )
    owned = {}
    for field, key, path, expected in owner_maps(manifest, SOURCE, started):
        check(started)
        actual = bind(frozen, external, path, expected, started)
        if field == "files":
            require(
                actual.is_relative_to(SOURCE) and actual.name != "manifest.json",
                "Source-owned artifact confinement",
            )
            relative = actual.relative_to(SOURCE).as_posix()
            require(relative not in owned, "No source owned aliases")
            owned[relative] = expected
    bind(
        frozen, external, SOURCE / "manifest.json", sha(SOURCE / "manifest.json", started), started
    )
    require(
        set(owned_artifacts(SOURCE, started)) == set(owned),
        "Exact complete actual producer inventory",
    )
    outcome, summary, protocol = [
        read_json(SOURCE / name, started)
        for name in ("completion_outcome.json", "summary.json", "protocol.json")
    ]
    require(
        outcome["completed"] is True
        and outcome["passed"] is True
        and outcome["budget_censored"] is False
        and outcome.get("failed", False) is False,
        "Sealed complete retained producer screen",
    )
    require(
        all(
            outcome[field] is False
            for field in ("full_G2", "adoption", "cost_transfer", "gates_emitted")
        )
        and outcome["new_test_credit"] == 0,
        "Actual source terminal has no emitted gates, adoption or fixture credit",
    )
    require(
        summary["scientific_screen_complete"] is True
        and summary["passed"] is True
        and summary["new_test_credit"] == 0,
        "Source PASS means complete two-row screen only",
    )
    require(
        all(summary[field] is False for field in ("full_G2", "adoption", "cost_transfer")),
        "No unsupported source financial/cost adoption",
    )
    same(protocol["author_sha256"], ORIGINAL_SOURCE_AUTHORS, "Exact original source author pair")
    same(
        protocol["method_document_SHA256"],
        policy["method_document_SHA256"],
        "Exact source method pair",
    )
    same(
        protocol["CPU_admission_wall_seconds"],
        [CPU, ADMISSION, WALL],
        "Matched source fixed budgets",
    )
    require(
        protocol["primary_digits"] == 90
        and protocol["independent_digits"] == DIGITS
        and protocol["threads"] == 1,
        "Exact source precision/thread scope",
    )
    require(
        protocol["schema"] == "a14-cosine-feasibility-protocol-v1"
        and protocol["preparation_metadata_only"] is True,
        "Actual byte-only source protocol",
    )
    same(protocol["fixed_rows"], list(ROW_IDS), "Exact fixed source rows")
    for name, expected in ORIGINAL_AUTHORS.items():
        path = RESEARCH / name
        require(
            sha(SOURCE / "executed_code" / name, started) == expected == sha(path, started),
            "Actual frozen executed code equals released author bytes",
        )
    require((SOURCE / "RUN_STARTED.json").is_file(), "Actual exclusive producer launch marker")
    verify_runtime(read_json(SOURCE / "interpreter.json", started), frozen, external, started)
    return dict(manifest=manifest, protocol=protocol, outcome=outcome, summary=summary)


def actual_call_catalog(graph, native, original_members, frozen, external, started):
    require(
        native["format"] == "hierarchical-clean-xor-source-v1"
        and (native["word_width"], native["fraction_bits"]) == (W, F),
        "Actual original compiled full72/f40 format",
    )
    same(
        native["inputs"],
        [node for node in graph.target["nodes"] if node["op"] == "input"],
        "Compiled actual q32 input nodes",
    )
    same(native["outputs"], graph.target["outputs"], "Compiled actual financial outputs")
    operations = [node for node in graph.target["nodes"] if node["op"] != "input"]
    require(
        len(operations) == len(native["forward_calls"]),
        "Every actual eager SSA node has one forward call",
    )
    library = saved_library(native, started)
    catalog = {}
    for operation, call in zip(operations, native["forward_calls"], strict=True):
        check(started)
        same(
            [operation["args"], operation["out"]],
            [call["args"], call["out"]],
            "Full literal actual argument/output order",
        )
        require(
            call["argument_copy_cx"] == 2 * W * len(operation["args"]),
            "Both full72 copies per caller argument",
        )
        leaf = call["leaf"]
        if leaf not in catalog:
            path = library / (leaf + ".json")
            key = path.relative_to(ROOT).as_posix()
            require(
                key in original_members,
                "Every actually used native descriptor has pinned exact A10 owner membership",
            )
            bind(frozen, external, path, original_members[key], started)
            descriptor = read_json(path, started)
            require(descriptor["key"] == leaf, "Actual source-selected descriptor key")
            gate = library / descriptor["gate_file"]
            gate_key = gate.relative_to(ROOT).as_posix()
            require(
                original_members.get(gate_key) == descriptor["sha256"],
                "Actual used gate expectedSHA agrees with original A10 member",
            )
            bind(frozen, external, gate, descriptor["sha256"], started)
            require(
                sha(gate, started) == descriptor["sha256"],
                "Actual source-owned saved native gate fingerprint; no array execution",
            )
            catalog[leaf] = descriptor
        descriptor = catalog[leaf]
        same(
            [descriptor["op"], descriptor["params"]],
            [operation["op"], operation["params"]],
            "Source call binds actual operation and parameters",
        )
        require(
            len(descriptor["args"]) == len(call["args"])
            and len(descriptor["outs"]) == len(call["out"])
            and all(len(word) == W for word in descriptor["args"] + descriptor["outs"]),
            "No argument/output high-bank elision",
        )
    return catalog


def removal_fixed_point(graph, native, scopes, started):
    candidates = set()
    boundaries = set().union(
        *(graph.ancestors(cosine["input"]) for scope in scopes for cosine in scope["cosines"])
    )
    outputs = {cosine["output"] for scope in scopes for cosine in scope["cosines"]}
    authorized = {
        (cosine["output"], normal)
        for scope in scopes
        for cosine, normal in zip(scope["cosines"], scope["normal_values"], strict=True)
    }
    pending = list(outputs)
    while pending:
        check(started)
        value = pending.pop()
        if value in boundaries or value in candidates:
            continue
        node = graph.node(value)
        require(node["op"] != "input", "Cosine closure must stop at its exact turns argument")
        candidates.update(node["out"])
        pending.extend(node["args"])
    consumers = {value: set() for value in graph.nodes}
    for node in graph.target["nodes"]:
        check(started)
        for argument in node["args"]:
            consumers[argument].update(node["out"])
    retained = set()
    for value in candidates:
        check(started)
        if (
            any(
                user not in candidates and (value, user) not in authorized
                for user in consumers[value]
            )
            or value in graph.target["outputs"]
        ):
            retained.add(value)
    pending = list(retained)
    while pending:
        check(started)
        value = pending.pop()
        node = graph.node(value)
        for dependency in [*node["out"], *node["args"]]:
            if dependency in candidates and dependency not in retained:
                retained.add(dependency)
                pending.append(dependency)
    removed = candidates - retained
    require(
        outputs <= removed,
        "Every old cosine output has only its authorized replacement product edge",
    )
    calls = []
    for index, call in enumerate(native["forward_calls"]):
        check(started)
        if set(call["out"]) & removed:
            require(
                set(call["out"]) <= removed,
                "Multioutput lookup is removed as a complete actual invocation",
            )
            calls.append(call)
    require(
        {value for call in calls for value in call["out"]} == removed,
        "Exact removed full72 value/call inventory",
    )
    return dict(
        removed_value_ids=sorted(removed),
        removed_forward_calls=calls,
        retained_shared_or_outside_value_ids=sorted(retained),
        authorized_cosine_output_to_radius_product_edges=[
            list(edge) for edge in sorted(authorized)
        ],
        actual_user_fixed_point=True,
        original_storage_subtracted=False,
    )


def independent_primitive_profiles(paths, native, frozen, external, started):
    require(set(paths) == {"ADD", "SUB", "MUL"}, "Exact three selected profile routes")
    profiles = {}
    for upper_op, key in paths.items():
        check(started)
        path = canonical_path(ROOT / key, started)
        require(path.relative_to(ROOT).as_posix() == key and key in frozen, "Frozen profile route")
        data = read_json(path, started)
        op = upper_op.lower()
        try:
            if op in ("add", "sub"):
                require(type(data) is list, "Actual A08 source-owned arithmetic screen")
                matches = [
                    row
                    for row in data
                    if row["op"] == op and row["width"] == W and row["variant"] == "brent-kung"
                ]
                require(len(matches) == 1, "ONE prescribed measured full72 BK row")
                entry = matches[0]
                gate_path = path.parent / entry["gate_file"].replace("\\", "/")
            else:
                entry, gate_path = data, path.with_suffix(".npy")
            descriptor_profile(entry, op, brent_kung=op in ("add", "sub"), source_format=native)
            profile = dict(
                descriptor_path=key,
                descriptor_sha256=frozen[key],
                gate_path=gate_path.relative_to(ROOT).as_posix(),
                gate_sha256=entry["sha256"],
                op=entry["op"],
                spec=entry["spec"],
                args=entry["args"],
                outs=entry["outs"],
                resources=entry["resources"],
                compiled_source_format=native["format"],
                word_width=W,
                fraction_bits=F,
                raw_modular_ADD_SUB_fraction_label_reuse_only=op in ("add", "sub"),
            )
            if op in ("add", "sub"):
                builder = path.parent / "executed_code/carry_lookahead.py"
                builder_key = builder.relative_to(ROOT).as_posix()
                require(builder_key in frozen, "Exact measured raw builder is frozen")
                definitions = {
                    node.name: node
                    for node in ast.parse(read_bytes(builder, started).decode("utf-8")).body
                    if isinstance(node, ast.FunctionDef)
                }
                require(
                    {"build_carry_lookahead", "prefix_pairs", "_compose"} <= definitions.keys(),
                    "Complete original raw prefix recipe definitions",
                )
                same(
                    [arg.arg for arg in definitions["build_carry_lookahead"].args.args],
                    ["op", "width", "variant"],
                    "Actual raw builder receives no fractional label",
                )
                for name in ("build_carry_lookahead", "prefix_pairs", "_compose"):
                    for node in ast.walk(definitions[name]):
                        check(started)
                        require(
                            not isinstance(node, ast.Name)
                            or not any(token in node.id.lower() for token in ("fraction", "scale")),
                            "Fraction-independent raw prefix construction",
                        )
                profile["raw_bit_map_fraction_label_independence"] = dict(
                    builder_path=builder_key,
                    builder_sha256=frozen[builder_key],
                    physical_call_arguments=[op, W, "brent-kung"],
                    raw_map="(a+b) mod2^72" if op == "add" else "(a-b) mod2^72",
                    fraction_label_is_metadata_only=True,
                    independent_signed_range_proofs_still_required=True,
                    new_gate_or_builder_execution=False,
                )
        except (ValueError, KeyError, TypeError) as error:
            profiles[upper_op] = dict(
                resource_rejected=True,
                op=op,
                descriptor_path=key,
                descriptor_sha256=frozen[key],
                reason=str(error),
                error_type=type(error).__name__,
                no_cost_or_contract_claim=True,
            )
            continue
        gate_key = profile["gate_path"]
        require(
            gate_key in frozen and frozen[gate_key] == entry["sha256"],
            "Exact original measured descriptor/gate membership agrees",
        )
        bind(frozen, external, gate_path, frozen[gate_key], started)
        profiles[upper_op] = profile
    return profiles


def diagnostic_projection(value):
    """Only free-text rejection diagnostics differ across independent validators."""
    if isinstance(value, dict):
        rejected = value.get("resource_rejected") is True or (
            value.get("resource_contract_passed") is False and value.get("rejected") is True
        )
        if rejected:
            require(
                value.get("no_cost_or_contract_claim") is True,
                "Rejected primitive/case carries no numeric cost or contract claim",
            )
            require(
                type(value.get("reason")) is str
                and value["reason"]
                and ("error_type" not in value or type(value["error_type"]) is str),
                "Retained explicit rejection diagnostics",
            )
        return {
            key: diagnostic_projection(item)
            for key, item in value.items()
            if not rejected or key not in ("reason", "error_type")
        }
    if isinstance(value, list):
        return [diagnostic_projection(item) for item in value]
    return value


def source_binding(policy, frozen, external, started):
    old = read_json(PROGRAM / "C06_pair_run001/certificate.json", started)
    envelope_path = PROGRAM / "A02_BM_native_financial_bridge_run002/cosine_envelope.json"
    envelope = read_json(envelope_path, started)
    old_error = rational(envelope["cosine_error_upper"])
    require(
        old_error >= EPSILON,
        "Actual old propagated seven-floor envelope includes its final one ULP",
    )
    archived = read_json(PROGRAM / "C06_pair_audit_run001/actual_pair_scope_audit.json", started)
    owner_path = PROGRAM / "A10_coefficient_run001/manifest.json"
    owner_key = owner_path.relative_to(ROOT).as_posix()
    bind(frozen, external, owner_path, policy["existing_owner_manifest_SHA256"][owner_key], started)
    original_members = {}
    for field, key, path, pin in owner_maps(
        read_json(owner_path, started), owner_path.parent, started
    ):
        check(started)
        if field == "files":
            require(path.is_relative_to(ROOT), "Original native member lexical ROOT confinement")
            member = path.relative_to(ROOT).as_posix()
            require(
                member not in original_members or original_members[member] == pin,
                "No conflicting original native membership",
            )
            original_members[member] = pin
    cases, catalogs = {}, {}
    for case, (assets, dates, pairs) in CASES.items():
        check(started, admission=True)
        route = PROGRAM / "A10_coefficient_run001" / case / "min-depth"
        actual_inputs = []
        for name in ("target.json", "source.json", "schedule_capped.json"):
            path = route / name
            key = path.relative_to(ROOT).as_posix()
            require(key in original_members, "Exact original target/source/schedule member")
            bind(frozen, external, path, original_members[key], started)
            actual_inputs.append(read_json(path, started))
        target, native, schedule = actual_inputs
        graph = GraphAudit(target, started)
        catalog = actual_call_catalog(graph, native, original_members, frozen, external, started)
        catalogs[case] = (graph, native, catalog)
        inputs = [node for node in target["nodes"] if node["op"] == "input"]
        require(
            len(inputs) == 2 * pairs == dates * (assets + 1), "Complete shared-pair input roles"
        )
        for index, node in enumerate(inputs):
            same(
                node["params"],
                dict(name="uniform_" + str(index), bits=32, preparation="uniform"),
                "Original q32 independent input order",
            )
        normals = old["source_bindings"][case]["normal_values"]
        require(
            len(normals) == 2 * pairs and len(set(normals)) == len(normals),
            "Every actual native normal value",
        )
        scopes = [
            graph.joint_pair(
                normals[2 * index],
                normals[2 * index + 1],
                inputs[2 * index]["out"][0],
                inputs[2 * index + 1]["out"][0],
                old["source_bindings"][case]["literal_ln2"],
            )
            for index in range(pairs)
        ]
        same(
            scopes,
            archived[case]["independently_walked_pair_scopes"],
            "Complete fresh traversal agrees with exact archived independent original pair scopes",
        )
        cosines = [cosine for scope in scopes for cosine in scope["cosines"]]
        require(len(cosines) == 2 * pairs, "Every actual cosine call scope")
        for cosine in cosines:
            require(cosine["floors"] == 7, "Actual old degree7 Horner path")
        require(
            native["resources"]["t_count"] == BASELINE[case][0],
            "Actual full financial original T baseline",
        )
        require(
            schedule["resources"]["t_count"] == BASELINE[case][0]
            and schedule["resources"]["t_depth"] == BASELINE[case][1]
            and schedule["resources"]["logical_qubits"] == BASELINE[case][2],
            "Exact measured original capped schedule/caps, separate from serial estimates",
        )
        profiles = independent_primitive_profiles(
            policy["primitive_descriptor_paths"][case], native, frozen, external, started
        )
        removal = removal_fixed_point(graph, native, scopes, started)
        calls_by_output = {tuple(call["out"]): call for call in native["forward_calls"]}
        cases[case] = dict(
            assets=assets,
            dates=dates,
            joint_pairs=pairs,
            cosine_sites=2 * pairs,
            target_path=(route / "target.json").relative_to(ROOT).as_posix(),
            source_path=(route / "source.json").relative_to(ROOT).as_posix(),
            schedule_path=(route / "schedule_capped.json").relative_to(ROOT).as_posix(),
            target_sha256=sha(route / "target.json", started),
            source_sha256=sha(route / "source.json", started),
            schedule_sha256=sha(route / "schedule_capped.json", started),
            original_resources=native["resources"],
            original_measured_schedule=schedule,
            normal_values=normals,
            pair_scopes=scopes,
            cosine_output_values=[row["output"] for row in cosines],
            cosine_argument_values=[row["input"] for row in cosines],
            cosine_calls=[calls_by_output[(row["output"],)] for row in cosines],
            selected_primitive_profiles=profiles,
            removal=removal,
            source_convention_exact=True,
            cross_date_pair_coordinates_not_divided=True,
        )
        require(type(schedule) is dict, "Actual original schedule metadata retained separately")
    original_table = catalogs["B4x12"][0].target["tables"]["cos"]
    same(
        original_table,
        catalogs["B8x52"][0].target["tables"]["cos"],
        "Same actual original cosine literal words across both targets",
    )
    require(
        len(envelope["coefficient_checks"]) == 512,
        "All accepted original derivative/literal error checks retained",
    )
    literal_errors = [Fraction(0)] * 64
    for index, entry in enumerate(envelope["coefficient_checks"]):
        check(started)
        segment, degree = divmod(index, 8)
        require(
            [entry["row"], entry["degree"], entry["raw"]]
            == [segment, degree, original_table[segment][degree]],
            "Accepted E_old binds every actual source coefficient",
        )
        lower, upper = [rational(value) for value in entry["exact_coefficient_enclosure"]]
        paid = rational(entry["actual_literal_error_upper"])
        require(
            paid
            == max(abs(Fraction(entry["raw"], Q) - lower), abs(Fraction(entry["raw"], Q) - upper)),
            "Exact preserved original literal-error arithmetic",
        )
        literal_errors[segment] += paid * LOCAL_RADIUS**degree
    floor = EPSILON * sum((LOCAL_RADIUS**degree for degree in range(7)), Fraction(0))
    require(
        rational(envelope["literal_rounding_upper"]) == max(literal_errors)
        and rational(envelope["Horner_floor_upper"]) == floor
        and old_error
        == max(literal_errors) + floor + rational(envelope["Taylor_degree7_remainder_upper"]),
        "Original fullinterval E_old formula bound, no inherited per-cos stock allowance",
    )
    radius = rational(envelope["pinned_native_radius_upper"])
    require(
        radius > 0
        and rational(envelope["remaining_coordinate_error_upper"]) == radius * old_error + EPSILON,
        "Already paid native radius and final f40 product ledger",
    )
    return (
        dict(
            schema="a14-original-cosine-source-binding-v1",
            cases=cases,
            existing_E_old=dict(
                path=envelope_path.relative_to(ROOT).as_posix(),
                sha256=sha(envelope_path, started),
                cosine_error_upper=encode(old_error),
                pinned_native_radius_upper=encode(radius),
                remaining_coordinate_error_upper=encode(radius * old_error + EPSILON),
                all512_actual_coefficient_words_and_error_formula_bound=True,
                source_manifest_sha256=list(BRIDGE_PINS.values())[0],
                audit_manifest_sha256=list(BRIDGE_PINS.values())[1],
            ),
            phase_premise=independent_phase_premise(started),
            arbitrary_signed_input_policy="new charged signed clamp [0,Q]",
            new_public_total_map_differs_from_original_Q_minus_one=True,
            actual_midpoint_wrap_domains_strictly_between_zero_and_Q=True,
            full_G2=False,
            cost_transfer=False,
        ),
        catalogs,
        envelope,
    )


def independent_phase_premise(started):
    proof = read_json(PHASE_PROOF, started)
    require(type(proof) is list and len(proof) == 8, "All three-wire exactphase premises retained")
    for state, row in enumerate(proof):
        same(
            row,
            dict(
                input=state,
                output=state ^ (4 * int((state & 1) != 0 and (state & 2) != 0)),
                exact_nonzero_phase=1,
            ),
            "Frozen applicable CCX phase-one identity on every basis input",
        )
    tree = ast.parse(read_bytes(PHASE_SOURCE, started).decode("utf-8"))
    definitions = [
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "ccx_seven_t"
    ]
    require(len(definitions) == 1, "One immutable applicable exact7T macro source")
    returns = [node for node in definitions[0].body if isinstance(node, ast.Return)]
    require(
        len(returns) == 1 and isinstance(returns[0].value, ast.List),
        "Literal exact7T chronological rows",
    )
    rows = []
    for call in returns[0].value.elts:
        check(started)
        require(
            isinstance(call, ast.Call)
            and isinstance(call.func, ast.Name)
            and call.func.id == "gate"
            and not call.keywords
            and isinstance(call.args[0], ast.Constant)
            and all(isinstance(value, ast.Name) for value in call.args[1:]),
            "Typed immutable CCX phase rows",
        )
        rows.append([call.args[0].value, *[value.id for value in call.args[1:]]])
    same(
        rows,
        [list(row) for row in EXACT_CCX_MACRO],
        "Every control/target phase and actual gate order paid",
    )
    return dict(
        exact_macro=rows,
        native_phase_one=True,
        direct_recipe_T_depth_per_CCX=7,
        direct_recipe_Clifford_T_serial_depth_per_CCX=15,
        fresh_gate_or_phase_simulation_executed=False,
    )


def complete_plan_native_ranges(plan, started):
    bounds, definitions, rows = {}, {}, []
    require(
        plan["schema"] == "a14-clean-cosine-typed-plan-v1"
        and plan["word_width"] == W
        and plan["external_fraction_bits"] == F,
        "Fixed full72 public recipe ABI",
    )
    next_value = 0
    for node in plan["nodes"]:
        check(started)
        op, args, params, outputs = node["op"], node["args"], node["params"], node["outputs"]
        require(
            outputs == list(range(next_value, next_value + len(outputs)))
            and all(value in bounds for value in args),
            "Complete typed recipe topology",
        )
        next_value += len(outputs)
        incoming = [bounds[value] for value in args]
        products = None
        if op == "INPUT":
            require(not args and outputs == [0], "One preserved public input")
            outgoing = [(-(1 << 71), (1 << 71) - 1)]
        elif op == "CONST":
            outgoing = [(native_word(params["raw"]),) * 2]
        elif op in ("ADD", "SUB"):
            outgoing = [pair_add(*incoming) if op == "ADD" else pair_subtract(*incoming)]
        elif op == "MUL":
            require(node["fraction_bits"] == F, "No unsupported f56 multiplication")
            values = [first * second for first in incoming[0] for second in incoming[1]]
            products = (min(values), max(values))
            if not -(1 << 143) <= products[0] <= products[1] < 1 << 143:
                raise NativeRejectedError("An actual eager signed144 product exceeds native range")
            outgoing = [native_range((products[0] // Q, products[1] // Q))]
        elif op in ("LT", "EQ", "FLAG_AND", "FLAG_OR"):
            if op.startswith("FLAG"):
                require(
                    all(0 <= lo <= hi <= 1 for lo, hi in incoming),
                    "Every full72 predicate is zero-extended boolean",
                )
            outgoing = [(0, 1)]
        elif op == "SELECT":
            require(
                0 <= incoming[0][0] <= incoming[0][1] <= 1, "Clean four-full72-port selector ABI"
            )
            branches = [incoming[1], incoming[2]]
            condition = definitions[args[0]]
            if condition["op"] == "LT":
                left, right = condition["args"]
                for branch in range(2):
                    value = args[branch + 1]
                    lo, hi = branches[branch]
                    if value == left:
                        if branch == 0:
                            hi = min(hi, bounds[right][1] - 1)
                        else:
                            lo = max(lo, bounds[right][0])
                    if value == right:
                        if branch == 0:
                            lo = max(lo, bounds[left][0] + 1)
                        else:
                            hi = min(hi, bounds[left][1])
                    branches[branch] = (lo, hi)
            elif condition["op"] == "EQ":
                first, second = condition["args"]
                for value, other in ((first, second), (second, first)):
                    if bounds[other][0] != bounds[other][1]:
                        continue
                    point = bounds[other][0]
                    if args[1] == value:
                        branches[0] = (max(branches[0][0], point), min(branches[0][1], point))
                    if args[2] == value:
                        lo, hi = branches[1]
                        branches[1] = (lo + int(lo == point), hi - int(hi == point))
            choices = [pair for pair in branches if pair[0] <= pair[1]]
            require(bool(choices), "Actual conditional branches cover a nonempty domain")
            outgoing = [
                native_range((min(lo for lo, hi in choices), max(hi for lo, hi in choices)))
            ]
        elif op == "BITS":
            kind, amount, width = params["kind"], params["amount"], params["width"]
            mapping = []
            for bit in range(W):
                if kind == "left":
                    source = bit - amount if bit >= amount else None
                elif kind == "signed_right":
                    source = min(bit + amount, W - 1)
                elif kind == "unsigned_right":
                    source = bit + amount if bit < width and bit + amount < W else None
                else:
                    require(kind == "low", "Fixed bit-copy semantics")
                    source = bit if bit < width else None
                mapping.append(source)
            same(params["output_to_input_bit"], mapping, "Every paid BITS CNOT/sign-extension map")
            lo, hi = incoming[0]
            if kind == "left":
                outgoing = [native_range((lo << amount, hi << amount))]
            elif kind == "signed_right":
                outgoing = [native_range((lo // (1 << amount), hi // (1 << amount)))]
            elif kind == "unsigned_right":
                require(
                    lo >= 0 and hi // (1 << amount) < 1 << width, "No omitted live high address bit"
                )
                outgoing = [(lo // (1 << amount), hi // (1 << amount))]
            else:
                outgoing = [(0, (1 << width) - 1)]
        elif op == "LOOKUP":
            require(
                params["bits"] == 6 and 0 <= incoming[0][0] <= incoming[0][1] < 64,
                "Endpoint mapped BEFORE the actual eager lookup",
            )
            table = params["table"]
            require(
                len(table) == 64 and all(len(row) == 8 for row in table),
                "All512 literal words and eight full72 output banks",
            )
            outgoing = [
                native_range((min(row[index] for row in table), max(row[index] for row in table)))
                for index in range(8)
            ]
        else:
            raise ValueError("Unsupported finite candidate node")
        for value, pair in zip(outputs, outgoing, strict=True):
            bounds[value] = native_range(tuple(pair))
            definitions[value] = node
        rows.append(
            dict(
                outputs=outputs,
                op=op,
                signed72_bounds=[list(pair) for pair in outgoing],
                signed144_product_bounds=None if products is None else list(products),
            )
        )
    require(next_value == plan["allocated_full72_banks"], "Every full72 bank accounted")
    final = bounds[plan["output_bank"]]
    require(
        -Q <= final[0] <= final[1] <= Q,
        "Actual public saturation/axes produce a bounded f40 result",
    )
    return dict(
        schema="a14-complete-recipe-native-safety-v1",
        row_id=plan["row_id"],
        complete_plan_checked=True,
        every_eager_selected_and_unselected_value_retained=True,
        actual_signed72_inputs_clamped_before_folding=True,
        exact_endpoint_lookup_Q_to_zero=True,
        all_signed72_outputs_and_signed144_products_safe=True,
        output_bound=list(final),
        full72_bank_count=next_value,
        rows=rows,
        discarded_shift_inputs_preserved_by_SSA=True,
        literal_reverse_restores_every_bank=True,
        full_G2=False,
        adoption=False,
    )


def whole_source_resources(plan, binding, catalogs, started):
    result = {}
    used = {node["op"] for node in plan["nodes"] if node["op"] in ("ADD", "SUB", "MUL")}
    for case, source_row in binding["cases"].items():
        check(started)
        graph, native, catalog = catalogs[case]
        units = {}
        rejected = [
            op
            for op in ("ADD", "SUB", "MUL")
            if op in used and source_row["selected_primitive_profiles"][op].get("resource_rejected")
        ]
        if rejected:
            first = next(node["op"] for node in plan["nodes"] if node["op"] in rejected)
            result[case] = dict(
                resource_contract_passed=False,
                rejected=True,
                reason=first + ": " + source_row["selected_primitive_profiles"][first]["reason"],
                no_cost_or_contract_claim=True,
            )
            continue
        for operation in ("add", "sub", "mul"):
            if operation.upper() not in used:
                continue
            declared = source_row["selected_primitive_profiles"].get(operation.upper())
            if declared is None:
                continue
            entry = dict(
                key=Path(declared["gate_path"]).stem,
                op=declared["op"],
                params=declared["spec"]["params"],
                spec=declared["spec"],
                args=declared["args"],
                outs=declared["outs"],
                resources=declared["resources"],
                sha256=declared["gate_sha256"],
                gate_file=Path(declared["gate_path"]).name,
            )
            units[operation] = descriptor_profile(
                entry, operation, brent_kung=operation in ("add", "sub"), source_format=native
            )
        cost = plan_resources(plan, units, started)
        clean = cost["function_clean_resource_estimate"]
        removed = dict.fromkeys(RESOURCE_FIELDS, 0)
        for call in source_row["removal"]["removed_forward_calls"]:
            check(started)
            resources = catalog[call["leaf"]]["resources"]
            for field in RESOURCE_FIELDS:
                removed[field] += 2 * resources[field]
            for field in ("cx", "source_gates", "clifford_cx", "clifford_t_depth"):
                removed[field] += 2 * call["argument_copy_cx"]
        sites = source_row["cosine_sites"]
        added = {field: 2 * sites * clean[field] for field in RESOURCE_FIELDS}
        for field in ("cx", "source_gates", "clifford_cx", "clifford_t_depth"):
            added[field] += 2 * sites * 2 * W
        original = {field: native["resources"][field] for field in RESOURCE_FIELDS}
        estimated = {
            field: original[field] - removed[field] + added[field] for field in RESOURCE_FIELDS
        }
        require(
            all(value >= 0 for value in estimated.values())
            and estimated["t_count"] == 7 * estimated["ccx"],
            "Complete nonnegative exact7T whole-source accounting",
        )
        recipe_banks = plan["allocated_full72_banks"]
        scratch = max(
            event["profile"]["private_scratch_qubits"] + event["profile"]["full72_input_arity"] * W
            for event in cost["events"]
        )
        bank_inventory = dict(
            allocated_recipe_banks=recipe_banks,
            retained_noninput_banks=recipe_banks - 1,
            external_input_bank=1,
            dirty_output_bank=1,
            outer_argument_copy_bank=1,
            word_qubits=recipe_banks * W,
            maximum_reused_primitive_private_plus_arguments=scratch,
            all_eager_and_constant_output_banks_retained=True,
            original_storage_subtracted=False,
        )
        workspace = W * (recipe_banks - 1) + scratch
        standalone = 2 * W + workspace
        whole_qubits = native["resources"]["logical_qubits"] + workspace + W
        improved = (
            estimated["t_count"] < original["t_count"]
            and estimated["t_depth"] < original["t_depth"]
        )
        caps = standalone <= 131072 and whole_qubits <= BASELINE[case][2]
        events = [
            dict(
                outputs=event["outputs"],
                op=event["op"].upper(),
                primitive_resource=event["profile"]["resources"],
                argument_copy_CX=event["argument_copy_CX"],
                private_and_argument_banks=event["profile"]["private_scratch_qubits"]
                + event["profile"]["full72_input_arity"] * W,
            )
            for event in cost["events"]
        ]
        result[case] = dict(
            function_forward_resource_estimate=cost["function_forward_resource_estimate"],
            function_clean_resource_estimate=clean,
            inner_argument_copy_CX=cost["full72_argument_copy_CX_per_forward"],
            constant_loading_X=sum(
                (node["params"]["raw"] % (1 << W)).bit_count()
                for node in plan["nodes"]
                if node["op"] == "CONST"
            ),
            primitive_events=events,
            full72_bank_inventory=bank_inventory,
            outer_function_argument_copy_CX_per_clean_invocation=2 * W,
            whole_source=dict(
                original=original,
                removed_twice=removed,
                added_twice_clean_plus_outercopies=added,
                estimated=estimated,
                qubits_conservative=whole_qubits,
                standalone_clean_workspace=standalone,
                comparison_with_both_original_T_and_matched_serial_depth=improved,
                within_caps=caps,
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
    return result


def save_literal_authorization_diagnostic(row, started):
    """Retain exact operands and decisions before a literal guard can reject."""
    path = OUTPUT / "cordic_literal_authorization_diagnostics.jsonl"
    check(started)
    first = row["literal_kind"] == "angle" and row["i"] == 0
    if first:
        require(not path.exists(), "One exclusive per-literal diagnostic stream")
    else:
        require(
            path.is_file()
            and canonical_path(path, started) == path
            and path.is_relative_to(OUTPUT),
            "Append only to the existing confined regular diagnostic stream",
        )
    data = (json.dumps(row, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()
    check(started)
    require(len(data) <= 128 * 1024, "Fixed finite individual literal diagnostic")
    with path.open("xb" if first else "ab") as stream:
        for offset in range(0, len(data), 65536):
            check(started)
            stream.write(data[offset : offset + 65536])
            check(started)


def authorize_cordic(mp, literals, certificate, started):
    require(
        literals["row_id"] == ROW_IDS[0]
        and literals["iterations"] == ITERATIONS
        and literals["fractional_bits"] == CORDIC_F,
        "Actual fixed CORDIC literal artifact",
    )
    angle_rows = literals["angle_rows"]
    require(
        [row["i"] for row in angle_rows] == list(range(ITERATIONS)),
        "Exactly ordered48 coefficient rows",
    )
    raw_angles = [native_word(row["raw"]) for row in angle_rows]
    gain_row = literals["gain_reciprocal"]
    raw_gain = native_word(gain_row["raw"])
    own = cordic_reference_literals(mp, raw_angles, raw_gain, started, require_half_ULP=False)
    gain_square = Fraction(1)
    for index in range(ITERATIONS):
        check(started)
        gain_square *= 1 + Fraction(1, 1 << (2 * index))
    require(
        rational(literals["exact_finite_gain_square"]) == gain_square < 4,
        "Exact finite gain product independently reconstructed, K48 below two",
    )
    declared_angles = []
    for actual, primary in zip(own["angles"], angle_rows, strict=True):
        check(started)
        true_interval = [rational(value) for value in actual["true_turns_enclosure"]]
        declared = [rational(value) for value in primary["true_turns_enclosure"]]
        numerical_inclusion = declared[0] <= true_interval[0] <= true_interval[1] <= declared[1]
        numerical_error = rational(primary["actual_abs_error_upper"]) >= rational(
            actual["actual_abs_error_upper"]
        )
        analytic_first_angle = actual["i"] == primary["i"] == 0
        exact_first_angle_authorized = (
            analytic_first_angle
            and primary["raw"] == CORDIC_Q // 8
            and declared[0] <= Fraction(1, 8) <= declared[1]
            and rational(primary["actual_abs_error_upper"]) >= 0
        )
        save_literal_authorization_diagnostic(
            dict(
                schema="a14-cordic-literal-authorization-diagnostic-v2",
                literal_kind="angle",
                i=primary["i"],
                primary=primary,
                independent_130=actual,
                numerical_interval_inclusion=numerical_inclusion,
                numerical_absolute_error_authorization=numerical_error,
                exact_analytic_first_angle_used=analytic_first_angle,
                exact_analytic_first_angle_authorized=exact_first_angle_authorized,
                analytic_true_turns=encode(Fraction(1, 8)) if analytic_first_angle else None,
                analytic_actual_literal_error_upper=encode(Fraction(0))
                if analytic_first_angle
                else None,
                analytic_identity="atan2(1,1)/(2*pi)=1/8" if analytic_first_angle else None,
                scientific_row_authorized=False,
                new_test_credit=0,
            ),
            started,
        )
        require(
            exact_first_angle_authorized
            if analytic_first_angle
            else numerical_inclusion and numerical_error,
            "Fresh130 true-angle inclusion and actual absolute error authorization",
        )
        midpoint = sum(declared, Fraction(0)) / 2
        require(
            nearest_fraction(midpoint * CORDIC_Q) == primary["raw"]
            and rational(primary["exact_rounding_reference"]) == midpoint
            and rational(primary["actual_abs_error_upper"])
            == max(abs(Fraction(primary["raw"], CORDIC_Q) - endpoint) for endpoint in declared)
            and primary["true_nearest_half_ULP_certified"]
            is (rational(primary["actual_abs_error_upper"]) <= CORDIC_EPSILON / 2),
            "Actual once-rounded digital angle and explicit conservative half ULP",
        )
        require(0 < declared[0] <= declared[1], "Positive saved true angle enclosure")
        declared_angles.append(tuple(declared))
    gain_interval = [rational(value) for value in gain_row["true_enclosure"]]
    true_gain = [
        rational(value) for value in own["reciprocal_gain"]["true_reciprocal_gain_enclosure"]
    ]
    save_literal_authorization_diagnostic(
        dict(
            schema="a14-cordic-literal-authorization-diagnostic-v2",
            literal_kind="gain",
            primary=gain_row,
            independent_130=own["reciprocal_gain"],
            numerical_interval_inclusion=gain_interval[0]
            <= true_gain[0]
            <= true_gain[1]
            <= gain_interval[1],
            numerical_absolute_error_authorization=rational(gain_row["actual_abs_error_upper"])
            >= rational(own["reciprocal_gain"]["actual_abs_error_upper"]),
            exact_analytic_first_angle_used=False,
            scientific_row_authorized=False,
            new_test_credit=0,
        ),
        started,
    )
    require(
        gain_interval[0] <= true_gain[0] <= true_gain[1] <= gain_interval[1]
        and rational(gain_row["actual_abs_error_upper"])
        >= rational(own["reciprocal_gain"]["actual_abs_error_upper"]),
        "Actual gain literal independently enclosed",
    )
    require(
        nearest_fraction(sum(gain_interval, Fraction(0)) * CORDIC_Q / 2) == raw_gain
        and rational(gain_row["exact_rounding_reference"]) == sum(gain_interval, Fraction(0)) / 2
        and rational(gain_row["actual_abs_error_upper"])
        == max(abs(Fraction(raw_gain, CORDIC_Q) - endpoint) for endpoint in gain_interval)
        and gain_row["true_nearest_half_ULP_certified"]
        is (rational(gain_row["actual_abs_error_upper"]) <= CORDIC_EPSILON / 2),
        "Once-rounded reciprocal gain, no generator-only premise",
    )
    passed = (
        all(row["true_nearest_half_ULP_certified"] for row in angle_rows)
        and gain_row["true_nearest_half_ULP_certified"]
    )
    require(
        literals["half_ULP_premises_passed"] is passed and certificate["passed"] is passed,
        "Conservative primary half-ULP success/rejection independently authorized",
    )
    if passed:
        require(
            own["every_actual_half_ULP_premise_certified"] is True,
            "Every claimed primary half ULP proved at130",
        )
        own_bound = cordic_uniform_bound(mp, started)
        require(raw_angles[0] == CORDIC_Q // 8, "Analytic a0 equals exact one-eighth turn")
        doubling = certificate["actual_angle_doubling_premise_rows"]
        require(len(doubling) == ITERATIONS - 1, "All47 retained greedy premises")
        for index, row in enumerate(doubling, 1):
            check(started)
            previous = Fraction(1, 8) if index == 1 else declared_angles[index - 1][1]
            twice = 2 * declared_angles[index][0]
            require(
                row["i"] == index
                and rational(row["previous_upper"]) == previous
                and rational(row["twice_current_lower"]) == twice
                and previous < twice,
                "Saved outward doubling premise refers exactly to the actual true-angle intervals",
            )
        angle_upper = rational(certificate["radian_residual_upper"])
        primary_pi_upper = (angle_upper - Fraction(1, 1 << 47)) / (3 * ITERATIONS * CORDIC_EPSILON)
        require(
            endpoints(mp.iv.pi)[1] <= primary_pi_upper < 4
            and rational(certificate["actual_final_angle_radian_upper"])
            == 2 * primary_pi_upper * declared_angles[-1][1]
            < Fraction(1, 1 << 47)
            and certificate["exact_finite_gain_square_less_than_four"] is True
            and certificate["actual_literal_half_ULP_premises_passed"] is True,
            "Independent130 pi/last-angle and gain authorize every saved fixed premise",
        )
        require(
            rational(certificate["shift_floor_and_gain_vector_upper"])
            == (3 * ITERATIONS + 1) * CORDIC_EPSILON
            and rational(certificate["final_nearest_rounding_upper"]) == EPSILON / 2
            and rational(certificate["cosine_error_upper"])
            == angle_upper + (3 * ITERATIONS + 1) * CORDIC_EPSILON + EPSILON / 2,
            "Exact complete primary CORDIC component arithmetic at authorized outward pi",
        )
        require(
            rational(certificate["cosine_error_upper"])
            >= rational(own_bound["uniform_error_upper"]),
            "Primary CORDIC full closed-interval error upper independently authorized",
        )
        require(
            certificate["actual_native_gate_or_full_G2_claim"] is False,
            "No CORDIC native gate/adoption claim",
        )
    else:
        require(
            certificate["rejected"] is True and "cosine_error_upper" not in certificate,
            "Rejected premise retains no uniform certificate or alternate method",
        )
        own_bound = dict(
            primary_uniform_certificate_authorized=False,
            rejection=True,
            primary_half_ULP_enclosure_insufficient=True,
            independent_narrower_enclosures_not_promoted=True,
        )
    own["exact_first_angle_authorization"] = dict(
        identity="atan2(1,1)/(2*pi)=1/8",
        true_turns=encode(Fraction(1, 8)),
        actual_raw=raw_angles[0],
        actual_literal_error_upper=encode(Fraction(0)),
        declared_interval_contains_exact_value=True,
        original_saved_midpoint_rounding_and_error_arithmetic_retained=True,
        other_47_angles_and_gain_numerical_authorization_unchanged=True,
        numerical_i0_enclosure_retained_as_diagnostic_only=True,
    )
    return own, own_bound, raw_angles, raw_gain


def authorize_taylor(mp, literals, certificate, started):
    require(
        literals["row_id"] == ROW_IDS[1] and literals["segments"] == 64 and literals["degree"] == 6,
        "Fixed Taylor6x64 artifact",
    )
    require(certificate["passed"] is True, "Fixed true-coefficient Taylor envelope completed")
    rows = literals["coefficient_rows"]
    require(type(rows) is list and len(rows) == 448, "All actual coefficient literals retained")
    own = taylor_reference_coefficients(mp, rows, started)
    require(len(certificate["segment_rows"]) == 64, "Every closed segment has an error envelope")
    for segment, primary in enumerate(certificate["segment_rows"]):
        check(started)
        actual = dict(
            segment=segment,
            literal_error_upper=own["segment_literal_error_uppers"][segment],
            Taylor_tail_upper=own["Taylor_degree6_remainder_upper"],
            Horner_floor_upper=own["Horner_floor_upper"],
            cosine_error_upper=encode(
                rational(own["segment_literal_error_uppers"][segment])
                + rational(own["Taylor_degree6_remainder_upper"])
                + rational(own["Horner_floor_upper"])
            ),
        )
        require(segment == primary["segment"], "Exact segment ordering")
        for field in (
            "literal_error_upper",
            "Taylor_tail_upper",
            "Horner_floor_upper",
            "cosine_error_upper",
        ):
            require(
                rational(primary[field]) >= rational(actual[field]),
                "Primary actual-word Taylor component authorized: " + field,
            )
    require(
        rational(certificate["cosine_error_upper"]) >= rational(own["uniform_error_upper"]),
        "Primary maximum segment bound independently authorized",
    )
    require(
        certificate["fitter_Bernstein_or_minimax_claim"] is False
        and certificate["actual_native_gate_or_full_G2_claim"] is False,
        "No fitting/optimality/native emission credit",
    )
    return own, rows


def audit_fixed_rows(policy, frozen, external, started):
    check(started, admission=True)
    import mpmath as mp

    mp.mp.dps = mp.iv.dps = DIGITS
    require(
        metadata.version("mpmath") == "1.3.0"
        and sys.modules["mpmath.libmp.backend"].BACKEND == "python",
        "Pure pinned130-digit interval engine",
    )
    loaded_origins(frozen, external, started)
    binding, catalogs, envelope = source_binding(policy, frozen, external, started)
    same(
        diagnostic_projection(read_json(SOURCE / "source_binding.json", started)),
        diagnostic_projection(binding),
        "Actual source/ABI/catalog/normal/pair/removal inventory independently reconstructed",
    )
    declared = read_json(SOURCE / "resource_estimates.json", started)
    frontier = read_json(SOURCE / "fixed_frontier.json", started)
    require(
        declared["schema"] == "a14-symbolic-source-resource-estimates-v1"
        and frontier["schema"] == "a14-fixed-cosine-frontier-v1",
        "Exact complete two-row artifact schemas",
    )
    require(
        set(declared["rows"]) == set(ROW_IDS)
        and [row["row_id"] for row in frontier["rows"]] == list(ROW_IDS),
        "Exactly two fixed rows, no outcome-driven substitutes",
    )
    rows, reconstructed = {}, []
    old_error = rational(binding["existing_E_old"]["cosine_error_upper"])
    radius = rational(envelope["pinned_native_radius_upper"])
    require(radius > 0, "Actual prior internal radius bound")
    for index, row_id in enumerate(ROW_IDS):
        check(started, admission=True)
        prefix = "cordic" if index == 0 else "taylor6"
        literals = read_json(SOURCE / (prefix + "_literals.json"), started)
        primary_uniform = read_json(SOURCE / (prefix + "_uniform_certificate.json"), started)
        if index == 0:
            literal_proof, uniform, angles, gain = authorize_cordic(
                mp, literals, primary_uniform, started
            )
            plan = symbolic_plan(row_id, angles, gain, [], started)
        else:
            literal_proof, taylor = authorize_taylor(mp, literals, primary_uniform, started)
            uniform = literal_proof
            plan = symbolic_plan(row_id, [], 0, taylor, started)
        record = declared["rows"][row_id]
        plan_bytes = json.dumps(
            plan, sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode()
        fingerprint = hashlib.sha256(plan_bytes).hexdigest()
        check(started)
        native_passed = True
        try:
            native_core = (
                cordic_native_ranges(angles, gain, started)
                if index == 0
                else taylor_native_ranges(taylor, started)
            )
            safety = complete_plan_native_ranges(plan, started)
        except NativeRejectedError as error:
            native_passed = False
            safety = dict(
                row_id=row_id,
                native_safety_passed=False,
                error_type=type(error).__name__,
                error=str(error),
                no_native_safety_certificate_claim=True,
            )
            native_core = safety
        primary_native = read_json(SOURCE / (prefix + "_native_safety.json"), started)
        require(
            primary_native["passed"] is native_passed,
            "Primary full public ABI safety success/rejection agrees with fresh independent ranges",
        )
        if native_passed:
            same(
                primary_native["complete_recipe_certificate"],
                safety,
                "Every selected/unselected word and full144 product bound "
                "independently reconstructed",
            )
        else:
            require(
                primary_native["rejected"] is True
                and primary_native["native_arithmetic_safety_claim"] is False,
                "Honest physical native-range rejection, no safety credit",
            )
        if native_passed:
            same(
                record["plan"],
                plan,
                "Every actual typed node/constant/shift/branch/table/output bank "
                "has the fixed independently built recipe",
            )
            require(record["plan_sha256"] == fingerprint, "Canonical exact recipe fingerprint")
            resources = whole_source_resources(plan, binding, catalogs, started)
            same(
                diagnostic_projection(record["cases"]),
                diagnostic_projection(resources),
                "Every actual selector/table/constant/copy/bank/scratch/cleanup/"
                "global-inverse resource component",
            )
            units = {
                case: binding["cases"][case]["selected_primitive_profiles"]
                for case, result in resources.items()
                if result["resource_contract_passed"]
            }
            same(
                diagnostic_projection(record["primitive_units"]),
                diagnostic_projection(units),
                "Exact independently admitted units; no unused profile rejects an unrelated row",
            )
            resource_passed = all(case["resource_contract_passed"] for case in resources.values())
            require(
                record["resource_contract_passed"] is resource_passed
                and record["resource_status"] == "SYMBOLIC_ESTIMATE_ONLY"
                and record["exact7T_serial_direct_recipes"] is True
                and record["native_gates_emitted"] is False
                and record["complete_source_adoption"] is False,
                "Exact resource success/rejection semantics without emission or adoption",
            )
        else:
            resources, resource_passed = {}, False
            require(
                set(record)
                == {
                    "resource_contract_passed",
                    "rejected",
                    "reason",
                    "cases",
                    "native_gates_emitted",
                }
                and record["resource_contract_passed"] is False
                and record["rejected"] is True
                and record["cases"] == {}
                and record["native_gates_emitted"] is False
                and type(record["reason"]) is str,
                "Native safety rejection retains no plan resource estimate or cost claim",
            )
        uniform_passed = primary_uniform["passed"]
        primary_error = rational(primary_uniform["cosine_error_upper"]) if uniform_passed else None
        uniform_fit = uniform_passed and primary_error <= old_error
        normal_upper = None
        if uniform_passed:
            product_upper = radius * (1 + primary_error) * Q * Q
            normal_upper = radius * (1 + primary_error) + EPSILON
            require(
                product_upper < 1 << 143 and normal_upper * Q < 1 << 71,
                "Remaining changed cosine-radius product and stored normal safety",
            )
        improved = resource_passed and all(
            value["whole_source"]["comparison_with_both_original_T_and_matched_serial_depth"]
            for value in resources.values()
        )
        within = resource_passed and all(
            value["whole_source"]["within_caps"] for value in resources.values()
        )
        eligible = uniform_fit and native_passed and resource_passed and improved and within
        status = (
            "NATIVE_REJECTED"
            if not native_passed
            else "UNIFORM_REJECTED"
            if not uniform_fit
            else "RESOURCE_REJECTED"
            if not resource_passed or not improved or not within
            else "COMPONENT_SCREEN_PASS"
        )
        actual = dict(
            row_id=row_id,
            status=status,
            uniform_certificate_passed=uniform_passed,
            native_safety_passed=native_passed,
            resource_contract_passed=resource_passed,
            E_at_most_E_old=uniform_fit,
            improvement_on_both_sources=improved,
            within_caps=within,
            component_screen_eligible=eligible,
            uniform_error_upper=None if primary_error is None else encode(primary_error),
            conditional_remaining_coordinate_error_upper=None
            if primary_error is None
            else encode(radius * primary_error + EPSILON),
            whole_financial_G2_proof_still_required=True,
            full_G2=False,
            adoption=False,
            cost_transfer=False,
        )
        same(
            frontier["rows"][index],
            actual,
            "Retained rejection/conditional component decision independently reconstructed",
        )
        reconstructed.append(actual)
        rows[row_id] = dict(
            actual_true130_literal_validation=literal_proof,
            independent_uniform_certificate=uniform,
            independent_core_native_safety=native_core,
            complete_plan_native_safety=safety,
            independent_resource_estimates=resources,
            conditional_financial_sensitivity=dict(
                pinned_native_radius_upper=encode(radius),
                original_cosine_error_upper=encode(old_error),
                new_cosine_error_upper=None if primary_error is None else encode(primary_error),
                remaining_coordinate_error_upper=None
                if primary_error is None
                else encode(radius * primary_error + EPSILON),
                changed_normal_absolute_upper=None
                if normal_upper is None
                else encode(normal_upper),
                E_at_most_original=uniform_fit,
                all_original_joint_pairs_retained=True,
                old_radius_log_grid_or_Holder_paid_again=False,
                changed_financial_source_or_full_G2_certified=False,
            ),
            decision=actual,
        )
    return binding, rows, reconstructed


def seal(output, frozen, external, started, outcome):
    require(
        not any(
            (output / name).exists()
            for name in ("manifest.json", "completion_outcome.json", "FAILED_UNSEALED.json")
        ),
        "One exclusive terminal, no retry/overwrite",
    )
    verified = final_fresh(frozen, external, started)
    final = dict(
        outcome,
        budget=elapsed(started),
        verification_unique_paths=verified,
        new_test_credit=0,
        all_fixture_credit=0,
        full_G2=False,
        adoption=False,
        cost_transfer=False,
        limits_CPU_admission_wall=[CPU, ADMISSION, WALL],
    )
    write_json(output / "completion_outcome.json", final, started)
    files = owned_artifacts(output, started)
    write_json(
        output / "manifest.json",
        dict(
            schema="a14-cosine-feasibility-independent-audit-manifest-v1",
            files=files,
            frozen_inputs=frozen,
            external_runtime_inputs=external,
            manifest_self_hash_excluded=True,
            terminal_outcome_file="completion_outcome.json",
            completed=final["completed"],
            passed=final["passed"],
            budget_censored=final["budget_censored"],
            terminal_budget_observation=elapsed(started),
            verification_and_output_hashing_before_terminal=True,
            original_expected_hashes_waived=False,
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
            "Existing/partial terminal blocks failed resealing",
        )
        check(started)
        write_json(
            output / "failure.json",
            dict(
                failed=True,
                completed=False,
                passed=False,
                phase=phase,
                error_type=type(error).__name__,
                error=str(error),
                traceback=traceback.format_exc(),
                budget_censored=isinstance(error, BudgetCensoredError),
                new_test_credit=0,
                independent_audit_passed=False,
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
                completed=False,
                passed=False,
                failed=True,
                rejection=False,
                independent_audit_passed=False,
                budget_censored=isinstance(error, BudgetCensoredError),
                phase=phase,
                failure_file="failure.json",
            ),
        )
    except BaseException:
        try:
            with (output / "FAILED_UNSEALED.json").open("xb") as stream:
                stream.write(
                    b'{"failed":true,"completed":false,"passed":false,"budget_censored":null,"hard_budget_state_uncertified":true,"new_test_credit":0,"independent_audit_passed":false,"partial_summary_or_manifest_is_not_terminal_success":true,"requires_fresh_version_and_receipt":true}\n'
                )
        except OSError:
            pass


def prepare(output):
    started = start_clock()
    frozen, external = {}, {}
    try:
        initialize(started)
        require(output == OUTPUT and not output.exists(), "Fresh exact independent A14 receipt")
        require(
            "mpmath" not in sys.modules, "Stdlib-only admission; no proof/source walk in prepare"
        )
        policy = implementation_policy(started)
        for path in (AUTHOR, IMPLEMENTATION, IMPLEMENTATION_DOC):
            expected = (
                policy["author_sha256"][AUTHOR.name] if path == AUTHOR else sha(path, started)
            )
            bind(frozen, external, path, expected, started)
        prior = prior_audit_provenance(policy, frozen, external, started)
        origins = bind_owners(policy, frozen, external, started)
        source = terminal_source(policy, frozen, external, started)
        runtime = runtime_inventory(frozen, external, started)
        verify_runtime(runtime, frozen, external, started)
        loaded_origins(frozen, external, started)
        final_fresh(frozen, external, started)
        check(started, admission=True)
        output.mkdir()
        (output / "executed_code").mkdir()
        for path in (AUTHOR, IMPLEMENTATION, IMPLEMENTATION_DOC):
            check(started)
            copy_exact(path, output / "executed_code" / path.name, frozen, external, started)
        write_json(output / "selected_source_origins.json", origins, started)
        write_json(output / "prior_audit_provenance.json", prior, started)
        write_json(
            output / "source_terminal_admission.json",
            dict(
                source_receipt=SOURCE.relative_to(ROOT).as_posix(),
                source_manifest_sha256=sha(SOURCE / "manifest.json", started),
                completed=True,
                scientific_screen_complete=True,
                independent_validation_not_yet_executed=True,
            ),
            started,
        )
        protocol = dict(
            schema="a14-cosine-feasibility-independent-audit-protocol-v2",
            author_sha256=policy["author_sha256"],
            original_source_author_SHA256=ORIGINAL_SOURCE_AUTHORS,
            original_author_SHA256=ORIGINAL_AUTHORS,
            operational_audit_version=2,
            prior_failed_audit_manifest_SHA256=PRIOR_AUDIT_SHA256,
            literal_diagnostic_manifest_SHA256=LITERAL_DIAGNOSTIC_SHA256,
            literal_diagnostic_root_review_manifest_SHA256=LITERAL_DIAGNOSTIC_REVIEW_SHA256,
            prior_root_review_manifest_SHA256=policy["prior_root_review_manifest_SHA256"],
            previous_failed_audit_credit=0,
            only_i0_exact_analytic_authorization=True,
            method_document_SHA256=policy["method_document_SHA256"],
            source_receipt=SOURCE.relative_to(ROOT).as_posix(),
            source_manifest_sha256=sha(SOURCE / "manifest.json", started),
            row_ids=list(ROW_IDS),
            CPU_admission_wall_seconds=[CPU, ADMISSION, WALL],
            primary_digits=90,
            independent_digits=DIGITS,
            threads=1,
            interpreter=runtime,
            frozen_inputs=frozen,
            external_runtime_inputs=external,
            no_refit_or_alternate_candidate=True,
            new_test_credit=0,
            full_G2=False,
            adoption=False,
            cost_transfer=False,
        )
        require(
            source["summary"]["scientific_screen_complete"] is True,
            "Actual source only complete two-row screen",
        )
        write_json(output / "protocol.json", protocol, started)
        write_json(
            output / "PREPARED_RECEIPT.json",
            dict(
                prepared=True,
                terminal=False,
                protocol_sha256=sha(output / "protocol.json", started),
                source_manifest_sha256=protocol["source_manifest_sha256"],
                no_scientific_import_or_source_walk_in_prepare=True,
                new_test_credit=0,
            ),
            started,
        )
        check(started)
    except BaseException as error:
        retain_failure(output, frozen, external, started, error, "prepare")
        raise


def run(output):
    started = start_clock()
    frozen, external = {}, {}
    try:
        initialize(started)
        require(
            output == OUTPUT
            and output.is_dir()
            and not any(
                (output / name).exists()
                for name in (
                    "manifest.json",
                    "completion_outcome.json",
                    "failure.json",
                    "FAILED_UNSEALED.json",
                    "RUN_STARTED.json",
                )
            ),
            "Exactly one run of the prepared fresh receipt",
        )
        write_json(output / "RUN_STARTED.json", dict(started=True, terminal=False), started)
        policy = implementation_policy(started)
        protocol = read_json(output / "protocol.json", started)
        require(
            protocol["schema"] == "a14-cosine-feasibility-independent-audit-protocol-v2",
            "Exact prepared protocol",
        )
        same(
            protocol["author_sha256"],
            policy["author_sha256"],
            "Own unchanged reviewed audit-only author",
        )
        require(
            protocol["operational_audit_version"] == 2
            and protocol["previous_failed_audit_credit"] == 0
            and protocol["only_i0_exact_analytic_authorization"] is True
            and protocol["prior_failed_audit_manifest_SHA256"] == PRIOR_AUDIT_SHA256,
            "Exact prepared audit-only version and prior failure",
        )
        require(
            protocol["literal_diagnostic_manifest_SHA256"] == LITERAL_DIAGNOSTIC_SHA256
            and protocol["literal_diagnostic_root_review_manifest_SHA256"]
            == LITERAL_DIAGNOSTIC_REVIEW_SHA256,
            "Actual completed diagnostic and its static review remain unchanged",
        )
        same(
            protocol["original_source_author_SHA256"],
            ORIGINAL_SOURCE_AUTHORS,
            "Original source pair unchanged",
        )
        same(protocol["original_author_SHA256"], ORIGINAL_AUTHORS, "All original six unchanged")
        same(
            protocol["prior_root_review_manifest_SHA256"],
            policy["prior_root_review_manifest_SHA256"],
            "Both original static releases unchanged",
        )
        same(
            protocol["method_document_SHA256"],
            policy["method_document_SHA256"],
            "Own unchanged reviewed method",
        )
        same(
            protocol["CPU_admission_wall_seconds"], [CPU, ADMISSION, WALL], "Unchanged fixed limits"
        )
        same(protocol["row_ids"], list(ROW_IDS), "Only the two original candidate rows")
        map_inputs(protocol, frozen, external, started)
        require(
            sha(SOURCE / "manifest.json", started) == protocol["source_manifest_sha256"],
            "Exact same sealed source as preparation",
        )
        prepared = read_json(output / "PREPARED_RECEIPT.json", started)
        require(
            prepared["prepared"] is True
            and prepared["terminal"] is False
            and prepared["protocol_sha256"] == sha(output / "protocol.json", started),
            "Unmodified actual independent preparation",
        )
        for path in (AUTHOR, IMPLEMENTATION, IMPLEMENTATION_DOC):
            require(
                sha(output / "executed_code" / path.name, started) == sha(path, started),
                "Own prepared immutable source copies",
            )
        prior = prior_audit_provenance(policy, frozen, external, started)
        same(
            read_json(output / "prior_audit_provenance.json", started),
            prior,
            "Every original failed/release binding freshly reconciled",
        )
        origins = bind_owners(policy, frozen, external, started)
        same(
            read_json(output / "selected_source_origins.json", started),
            origins,
            "Full original scoped byte origins freshly verified",
        )
        terminal_source(policy, frozen, external, started)
        verify_runtime(protocol["interpreter"], frozen, external, started)
        loaded_origins(frozen, external, started)
        verify_maps(frozen, external, started)
        check(started, admission=True)
        binding, proofs, frontier = audit_fixed_rows(policy, frozen, external, started)
        for row_id, evidence in proofs.items():
            write_json(output / (row_id + ".json"), evidence, started)
        write_json(output / "independent_source_binding.json", binding, started)
        write_json(
            output / "independent_fixed_frontier.json",
            dict(schema="a14-independent-fixed-cosine-frontier-v1", rows=frontier),
            started,
        )
        verify_runtime(protocol["interpreter"], frozen, external, started)
        origins_after = loaded_origins(frozen, external, started)
        write_json(output / "actual_loaded_module_origins.json", origins_after, started)
        summary = dict(
            schema="a14-cosine-feasibility-independent-audit-summary-v1",
            operational_audit_version=2,
            previous_failed_audit_credit=0,
            only_i0_exact_analytic_authorization=True,
            all_other_47_angles_and_gain_numerical_guards_retained=True,
            per_literal_diagnostics_retained_before_guards=True,
            completed=True,
            passed=True,
            independent_audit_passed=True,
            scientific_screen_complete=True,
            actual_fixed_rows=2,
            row_ids=list(ROW_IDS),
            actual_independent_digits=DIGITS,
            actual_true_CORDIC_angle_count=48,
            actual_true_Taylor_coefficient_count=448,
            actual_original_joint_pairs={case: values[2] for case, values in CASES.items()},
            actual_original_cosine_sites={case: 2 * values[2] for case, values in CASES.items()},
            all_eager_full72_and_product144_safety_independently_checked=True,
            all_fixed_rows_native_safety_passed=all(
                row["native_safety_passed"] for row in frontier
            ),
            all_fixed_rows_resource_contract_passed=all(
                row["resource_contract_passed"] for row in frontier
            ),
            rejected_rows_retained_without_safety_or_resource_credit=True,
            every_full72_copy_bank_and_literal_inverse_charged=True,
            component_eligible_rows=[
                row["row_id"] for row in frontier if row["component_screen_eligible"]
            ],
            full_native_gate_emission_or_changed_financial_source_certified=False,
            full_G2=False,
            adoption=False,
            cost_transfer=False,
            new_test_credit=0,
            all_fixture_credit=0,
            original_expected_hashes_waived=False,
            budget=elapsed(started),
        )
        write_json(output / "summary.json", summary, started)
        seal(
            output,
            frozen,
            external,
            started,
            dict(
                completed=True,
                passed=True,
                failed=False,
                rejection=False,
                independent_audit_passed=True,
                scientific_screen_complete=True,
                budget_censored=False,
                summary_file="summary.json",
            ),
        )
    except BaseException as error:
        retain_failure(output, frozen, external, started, error, "run")
        raise


def main():
    parser = argparse.ArgumentParser(
        description="Bounded independent fixed A14 cosine screen; no native gate emission"
    )
    parser.add_argument("action", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    require(
        args.output.is_absolute() and args.output.resolve() == OUTPUT,
        "Exact preregistered receipt route",
    )
    if args.action == "prepare":
        prepare(args.output.resolve())
    else:
        run(args.output.resolve())


if __name__ == "__main__":
    main()
