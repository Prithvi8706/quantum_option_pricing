"""Independent all-class native-transform audit, with zero new test credit.

Only the standard library and mpmath are imported. Producer/native proof helpers
are deliberately not imported. No audits, intervals or words run on import.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from math import isqrt
import os
from pathlib import Path
import re
import shutil
import sys
import time
import traceback
import xml.etree.ElementTree as ET

os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import mpmath as mp  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
TRANSFORM = PROGRAM / "A02_quantile_transform_run002"
CENTRAL = PROGRAM / "A02_quantile_central_run002"
TAIL = PROGRAM / "A02_quantile_tail_run001"
PAIR = PROGRAM / "C06_pair_run001"
SQRT = PROGRAM / "A10_coefficient_run001/B4x12/min-depth/leaves/160a18dba2e09b8e1ad2.json"
S = 1 << 40
ULP = Fraction(1, S)
RMAX = Fraction(321, 100)
TARGET = Fraction(1, 100000000)
DIGITS = 120
CPU_LIMIT = 180
WALL_LIMIT = 600
WORDS = (0, (1 << 32) - 1, 322122546, (1 << 32) - 1 - 322122546)
RECEIPTS = (
    "A02_quantile_transform_run002",
    "A02_quantile_central_run002",
    "A02_quantile_central_audit_run001",
    "A02_quantile_tail_run001",
    "A02_quantile_tail_audit_run001",
    "C06_pair_run001",
    "C06_pair_audit_run001",
)
CODE = ("audit_quantile_transform.py", "quantile_transform_audit_preflight.json")


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def pair(value):
    value = Fraction(value)
    return [value.numerator, value.denominator]


def exact(value):
    require(
        isinstance(value, list)
        and len(value) == 2
        and all(type(item) is int for item in value)
        and value[1] > 0,
        "Exact integer rational pair required",
    )
    return Fraction(*value)


def stored_interval(value):
    low, high = map(exact, value)
    require(low <= high, "Ordered saved interval")
    return low, high


def iv(value):
    value = Fraction(value)
    return mp.iv.mpf(value.numerator) / value.denominator


def endpoints(value):
    result = []
    for sign, mantissa, exponent, _ in value._mpi_:
        result.append(Fraction((-1) ** sign * mantissa) * Fraction(2) ** exponent)
    return tuple(result)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def relative(path):
    return Path(path).resolve().relative_to(ROOT.resolve()).as_posix()


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def bind(frozen, name, expected):
    path = Path(str(name).replace("\\", "/"))
    path = path.resolve() if path.is_absolute() else (ROOT / path).resolve()
    normalized = relative(path)
    require(
        isinstance(expected, str) and re.fullmatch(r"[0-9a-f]{64}", expected),
        "Explicit frozen SHA256 required",
    )
    require(
        normalized not in frozen or frozen[normalized] == expected,
        "Historical prerequisite bytes conflict: " + normalized,
    )
    frozen[normalized] = expected


def verify(frozen):
    for name, expected in frozen.items():
        path = (ROOT / name.replace("\\", "/")).resolve()
        path.relative_to(ROOT.resolve())
        require(digest(path) == expected, "Frozen audit input changed: " + name)


def budget(cpu, wall):
    if time.process_time() - cpu > CPU_LIMIT or time.monotonic() - wall > WALL_LIMIT:
        raise TimeoutError("Fixed independent audit180CPU/600wall budget")


def nearest_even(value):
    value = Fraction(value)
    quotient, remainder = divmod(value.numerator, value.denominator)
    twice = 2 * remainder
    return quotient + int(
        twice > value.denominator or (twice == value.denominator and quotient % 2 == 1)
    )


def integer_polynomial(coefficients, argument):
    """Exact nonnegative native floor-Horner, independent implementation."""
    accumulator = 0
    for coefficient in reversed(coefficients):
        accumulator = accumulator * argument // S + coefficient
    return accumulator


def polynomial_error(coefficients, raw, upper):
    # Expanded coefficient errors and geometric floor powers avoid using the
    # producer's recursive error propagation implementation.
    return sum(
        (
            abs(Fraction(word, S) - coefficient) * upper**degree
            for degree, (coefficient, word) in enumerate(zip(coefficients, raw, strict=True))
        ),
        Fraction(0),
    ) + ULP * sum((upper**degree for degree in range(len(raw) - 1)), Fraction(0))


def derivative_upper(coefficients, upper):
    require(all(coefficient > 0 for coefficient in coefficients), "Positive rational coefficients")
    return sum(
        (
            degree * coefficients[degree] * upper ** (degree - 1)
            for degree in range(1, len(coefficients))
        ),
        Fraction(0),
    )


def audit_source():
    bindings = read(PAIR / "certificate.json")["source_bindings"]
    tables, ln2s = [], []
    for case in ("B4x12", "B8x52"):
        binding = bindings[case]
        path = ROOT / binding["target"].replace("\\", "/")
        require(digest(path) == binding["target_sha256"], "Original target byte binding")
        target = read(path)
        require((target["width"], target["fraction_bits"]) == (72, 40), "Original native precision")
        tables.append(target["tables"]["log"])
        ln2s.append(binding["literal_ln2"])
    require(
        tables[0] == tables[1] and ln2s == [762123384786] * 2,
        "Original B4/B8 native table/ln2 equality",
    )
    require(
        len(tables[0]) == 32 and all(len(row) == 9 for row in tables[0]),
        "Original32 by9 log coefficients",
    )
    sqrt = read(SQRT)["spec"]
    require(
        (
            sqrt["op"],
            sqrt["width"],
            sqrt["fraction_bits"],
            sqrt["active_input_bits"],
            sqrt["input_contract"],
            sqrt["lowering"],
        )
        == (
            "sqrt",
            72,
            40,
            46,
            {"unsigned_input_bits": 46},
            "unsigned-nonrestoring-sqrt-signed-remainder-v1",
        ),
        "Original sqrt semantic ABI",
    )
    return tables[0], ln2s[0], bindings


def audit_log_and_normalization(saved, table, ln2, cpu, wall):
    transform = saved["transform"]
    normalization = transform["normalization"]
    require(
        normalization["all_q32_tail_words_covered"] is True
        and normalization["enumerated_q32_words_as_completeness_proof"] == 0,
        "The completeness argument is structural, not sampled",
    )
    require(
        normalization["msb_index_range"] == [7, 36]
        and normalization["log_exponent_range"] == [-33, -4]
        and normalization["mantissa_raw_bounds"] == [S, 2 * S - (1 << 11)]
        and normalization["minimum_mantissa_zero_low_bits"] == 11,
        "Normalization/congruence ranges",
    )
    for key in (
        "normalization_roundoff_exact",
        "exponent_times_ln2_floor_error_exact",
        "negative_log_negation_error_exact",
    ):
        require(exact(normalization[key]) == 0, "Exact shift/exponent/negation semantics")
    require(
        normalization["native_input_guard_raw_one_inactive"] is True
        and normalization["interpolation_clips_inactive"] is True,
        "Positive midpoint and mantissa guards must be inactive",
    )
    radius = Fraction(1, 64)
    taylor_remainder = radius**9 / 9
    floor_error = ULP * (1 - radius**8) / (1 - radius)
    saved_rows = transform["log_table_cells"]
    require(
        len(saved_rows) == 32 and [row["table_cell"] for row in saved_rows] == list(range(32)),
        "Exactly32 complete log coefficient cells",
    )
    independent_table_errors, class_rows = [], []
    max_stored, max_product = Fraction(0), Fraction(0)
    for index, (words, row) in enumerate(zip(table, saved_rows, strict=True)):
        budget(cpu, wall)
        center = Fraction(64 + 2 * index + 1, 64)
        require(
            exact(row["center_exact"]) == center and exact(row["radius_exact"]) == radius,
            "Original mantissa cell geometry",
        )
        require(len(row["coefficient_checks"]) == 9, "All nine archived coefficients")
        errors, saved_errors = [], []
        for degree, word in enumerate(words):
            require(type(word) is int, "Literal coefficient integer")
            true = (
                endpoints(mp.iv.ln(iv(center)))
                if degree == 0
                else (Fraction((-1) ** (degree - 1), degree * center**degree),) * 2
            )
            check = row["coefficient_checks"][degree]
            existing = stored_interval(check["true_coefficient_interval_exact"])
            require(
                check["degree"] == degree
                and check["literal_raw"] == word
                and existing[0] <= true[0] <= true[1] <= existing[1],
                "Independent coefficient enclosure must fit saved proof",
            )
            error = max(abs(Fraction(word, S) - endpoint) for endpoint in true)
            saved_error = exact(check["coefficient_error_upper_exact"])
            require(error <= saved_error <= ULP / 2, "Nearest native coefficient rounding")
            require(
                saved_error == max(abs(Fraction(word, S) - endpoint) for endpoint in existing),
                "Saved coefficient error reconciles with its enclosing endpoints",
            )
            errors.append(error)
            saved_errors.append(saved_error)
        independent_error = (
            taylor_remainder
            + floor_error
            + sum((error * radius**degree for degree, error in enumerate(errors)), Fraction(0))
        )
        saved_coefficient = sum(
            (error * radius**degree for degree, error in enumerate(saved_errors)), Fraction(0)
        )
        require(
            exact(row["coefficient_error_upper_exact"]) == saved_coefficient
            and exact(row["Taylor_remainder_upper_exact"]) == taylor_remainder
            and exact(row["Horner_floor_error_upper_exact"]) == floor_error
            and exact(row["table_error_upper_exact"])
            == saved_coefficient + taylor_remainder + floor_error,
            "Complete saved table error ledger",
        )
        independent_table_errors.append(independent_error)
        magnitude = abs(Fraction(words[-1], S))
        max_stored = max(max_stored, magnitude)
        for word in reversed(words[:-1]):
            max_product = max(max_product, magnitude * radius)
            product_magnitude = magnitude * radius + ULP
            magnitude = product_magnitude + abs(Fraction(word, S))
            max_stored = max(max_stored, magnitude, product_magnitude)
    ln2_iv = endpoints(mp.iv.ln(iv(2)))
    saved_ln2_iv = stored_interval(transform["ln2_interval_exact"])
    require(
        saved_ln2_iv[0] <= ln2_iv[0] <= ln2_iv[1] <= saved_ln2_iv[1], "ln2 independent enclosure"
    )
    ln2_error = max(abs(Fraction(ln2, S) - endpoint) for endpoint in ln2_iv)
    saved_ln2_error = exact(transform["ln2_literal_error_upper_exact"])
    require(
        ln2_error <= saved_ln2_error <= ULP / 2 and 33 * ln2_iv[1] < Fraction(231, 10),
        "ln2 rounding and all-q32 true log upper",
    )
    require(
        saved_ln2_error == max(abs(Fraction(ln2, S) - endpoint) for endpoint in saved_ln2_iv),
        "Saved ln2 literal error matches its outward endpoints",
    )
    combos = transform["cell_exponent_cover"]
    require(
        len(combos) == 960 and transform["exponent_classes"] == list(range(-33, -3)),
        "Complete960 conservative classes",
    )
    max_error = Fraction(0)
    tail_maximum_raw = (2 * 322122546 + 1) << 7
    require(
        Fraction(tail_maximum_raw, S) < Fraction(3, 40) < Fraction(tail_maximum_raw + 256, S),
        "Actual last tail midpoint boundary",
    )
    for ordinal, row in enumerate(combos):
        budget(cpu, wall)
        index, exponent = divmod(ordinal, 30)
        exponent -= 33
        require((row["table_cell"], row["exponent"]) == (index, exponent), "Class order/uniqueness")
        amount = independent_table_errors[index] + abs(exponent) * ln2_error
        stored_amount = (
            exact(saved_rows[index]["table_error_upper_exact"]) + abs(exponent) * saved_ln2_error
        )
        require(
            amount <= exact(row["native_log_error_upper_exact"]) == stored_amount,
            "Independent coefficient/floor/exponent error in every class",
        )
        max_error = max(max_error, amount)
        # Mantissa bin bounds are intersected with exact p=128 mod256 and
        # the exponent's leading-bit range; zero admissible words is allowed.
        factor = 1 << (-exponent)
        m_low, m_high = S + index * (1 << 35), S + (index + 1) * (1 << 35) - 1
        p_low = max(128, -(-m_low // factor), 1 << (exponent + 40))
        p_high = min(tail_maximum_raw, m_high // factor, (1 << (exponent + 41)) - 1)
        first = 128 + 256 * (-(-(p_low - 128) // 256))
        last = 128 + 256 * ((p_high - 128) // 256)
        require(7 - exponent >= 11 and factor >= 16, "At least11 exact low mantissa zeros")
        class_rows.append(
            {
                "table_cell": index,
                "exponent": exponent,
                "native_log_error_upper_exact": pair(amount),
                "probability_raw_bounds": [p_low, p_high],
                "first_admissible_q32_tail_midpoint_raw": first if first <= last else None,
                "last_admissible_q32_tail_midpoint_raw": last if first <= last else None,
                "conservative_class_may_be_unreachable": first > last,
                "normalization_floor_or_clip_error_exact": [0, 1],
            }
        )
    saved_error = exact(transform["native_log_error_upper_exact"])
    require(
        max_error
        <= saved_error
        == max(exact(row["native_log_error_upper_exact"]) for row in combos),
        "Global log envelope is the960-class maximum",
    )
    return saved_error, max_stored, max_product, class_rows


def audit_root_and_storage(saved, log_error, max_poly, max_product, ln2):
    body = saved["transform"]
    true_lower = endpoints(-mp.iv.ln(iv(Fraction(3, 40))))
    existing_lower = stored_interval(body["true_negative_log_lower_interval_exact"])
    require(
        existing_lower[0] <= true_lower[0] <= true_lower[1] <= existing_lower[1]
        and true_lower[0] > Fraction(259, 100)
        and log_error < Fraction(1, 1000),
        "Strict true/native positive radicand margin",
    )
    lower, upper = Fraction(259, 100) - log_error, Fraction(231, 10) + log_error
    require(
        exact(body["native_negative_log_lower_exact"]) == lower
        and exact(body["native_negative_log_upper_exact"]) == upper
        and lower > Fraction(1609, 1000) ** 2 > Fraction(8, 5) ** 2
        and upper < Fraction(4807, 1000) ** 2
        and upper < 24,
        "Both exact and native roots exceed1.6, with upper4.807",
    )
    shift_word = nearest_even(Fraction(8 * S, 5))
    shift_error = abs(Fraction(shift_word, S) - Fraction(8, 5))
    root_error = Fraction(5, 16) * log_error
    rho = root_error + ULP + shift_error
    require(
        body["nearest_shift_raw"] == shift_word
        and exact(body["nearest_shift_error_exact"]) == shift_error
        and exact(body["sqrt_floor_error_upper_exact"]) == ULP
        and exact(body["sqrt_sensitivity_error_upper_exact"]) == root_error
        and exact(body["native_transform_error_upper_exact"]) == rho,
        "Root Lipschitz, integer-root floor and fixed shift each charged once",
    )
    require(
        upper * S < 1 << 45 and upper * S * S < 1 << 85 and Fraction(4807, 1000) * S < 1 << 43,
        "Native45 input/85 shifted radicand/43 output",
    )
    r_low, r_high = Fraction(9, 1000) - ULP - shift_error, Fraction(3207, 1000) + shift_error
    require(
        stored_interval(body["actual_native_r_range_exact"]) == (r_low, r_high)
        and 0 < r_low <= r_high < RMAX,
        "Actual nonnegative ordinary-tail argument cap",
    )
    stored = max(
        max_poly + 33 * abs(Fraction(ln2, S)), Fraction(33), Fraction(24), Fraction(4807, 1000)
    )
    full_product = max(max_product, 33 * abs(Fraction(ln2, S))) * S * S
    require(
        exact(body["maximum_stored_value_upper_exact"]) == stored
        and stored * S < 1 << 71
        and exact(body["maximum_full_product_raw_upper_exact"]) == full_product
        and full_product < 1 << 143,
        "All logarithm/root signed storage/fullproduct bounds",
    )
    require(
        body["actual_shifted_sqrt_radicand_bits"] == 85
        and body["accepted_sqrt_semantic_radicand_bits"] == 86
        and body["sqrt_output43_bits"] is True,
        "Actual versus accepted sqrt widths",
    )
    return rho


def audit_sensitivity(saved, fresh, cpu, wall):
    tail = read(TAIL / "tail_certificate.json")
    central = read(CENTRAL / "central_certificate.json")
    cells = read(TAIL / "cell_bounds.json")["cells"]
    require(
        tail["certified"] is True
        and central["certified"] is True
        and len(cells) == fresh["fixed_rows"] == fresh["completed_rows"] == 1024,
        "Accepted complete native central/tail and refreshed rows",
    )
    rows = fresh["rows"]
    require(
        len(rows) == 1024
        and [row["cell_index"] for row in cells] == list(range(1024))
        and [row["cell_index"] for row in rows] == list(range(1024)),
        "All1024 distinct rows",
    )
    a, b = [
        tuple(map(Fraction, tail["source_coefficients"][name]))
        for name in ("A_decimals_ascending", "B_decimals_ascending")
    ]
    raw_a, raw_b = [
        tuple(nearest_even(coefficient * S) for coefficient in polynomial) for polynomial in (a, b)
    ]
    require(
        list(raw_a) == tail["native_interface"]["native_A_raw_ascending"]
        and list(raw_b) == tail["native_interface"]["native_B_raw_ascending"]
        and min(raw_a + raw_b) > 0
        and raw_b[0] == S,
        "Published decimal native rounding",
    )
    rho = exact(saved["transform"]["native_transform_error_upper_exact"])
    report, maximum = [], Fraction(0)
    for ordinal, (cell, row) in enumerate(zip(cells, rows, strict=True)):
        budget(cpu, wall)
        low, high = stored_interval(cell["r_domain_exact"])
        require(
            (low, high) == (RMAX * ordinal / 1024, RMAX * (ordinal + 1) / 1024),
            "Unchanged fixed equal tail cells",
        )
        z_low, z_high = stored_interval(cell["rational_z_range_exact"])
        require(0 <= z_low <= z_high <= Fraction(13, 2), "Audited real rational magnitude13/2")
        expanded = max(Fraction(0), low - rho), min(RMAX, high + rho)
        require(
            stored_interval(row["extended_r_domain_exact"]) == expanded
            and exact(row["argument_perturbation_upper_exact"]) == rho,
            "Fresh actual-transform argument interval replaces hypothetical1ulp",
        )
        minimum_argument_raw = expanded[0].numerator * S // expanded[0].denominator
        denominator = Fraction(integer_polynomial(raw_b, minimum_argument_raw), S)
        require(denominator >= 1, "Monotone positive native denominator")
        a_error = polynomial_error(a, raw_a, expanded[1]) + rho * derivative_upper(a, expanded[1])
        b_error = polynomial_error(b, raw_b, expanded[1]) + rho * derivative_upper(b, expanded[1])
        native_error = (a_error + Fraction(13, 2) * b_error) / denominator + ULP
        real_error = exact(cell["real_quantile_error_upper_exact"])
        total = real_error + native_error
        for key, value in {
            "native_denominator_lower_exact": denominator,
            "numerator_coefficient_Horner_and_input_error_upper_exact": a_error,
            "denominator_coefficient_Horner_and_input_error_upper_exact": b_error,
            "fresh_native_rational_error_upper_exact": native_error,
            "saved_real_approximation_error_upper_exact": real_error,
            "actual_native_tail_quantile_error_upper_exact": total,
        }.items():
            require(exact(row[key]) == value, "Independent refreshed rational ledger: " + key)
        require(
            row["previous_conditional_floor_arithmetic_error_added"] is False
            and row["actual_sqrt_floor_and_shift_error_only_in_rho"] is True,
            "No old conditional native error or root-floor double count",
        )
        maximum = max(maximum, total)
        report.append(
            {
                "cell_index": ordinal,
                "independent_native_denominator_lower_exact": pair(denominator),
                "independent_fresh_tail_total_error_upper_exact": pair(total),
                "matched_saved_ledger": True,
            }
        )
    central_error = exact(central["total_central_quantile_error_upper_exact"])
    require(
        exact(saved["actual_native_tail_quantile_error_upper_exact"]) == maximum
        and exact(saved["central_quantile_error_upper_exact"]) == central_error
        and exact(saved["combined_mathematical_native_quantile_error_upper_exact"])
        == max(maximum, central_error)
        and max(maximum, central_error) <= TARGET,
        "Combined native all-input1e-8 target",
    )
    divisor = saved["central_denominator64"]
    native = central["native_arithmetic"]
    upper_r = exact(native["r_native_upper_exact"])
    raw_central_b = native["native_B_raw_ascending"]
    upper_denominator = sum(
        (Fraction(word) * upper_r**degree for degree, word in enumerate(raw_central_b)), Fraction(0)
    )
    require(
        raw_central_b[0] == S
        and min(raw_central_b) > 0
        and upper_denominator < 1 << 64
        and exact(divisor["maximum_central_denominator_raw_upper_exact"]) == upper_denominator
        and exact(divisor["central_native_argument_upper_exact"]) == upper_r
        and divisor["unsigned64_denominator_no_truncation"] is True,
        "Independent central positive denominator64 guard",
    )
    return report, maximum, central_error


def audit_word(raw, table, ln2, rho):
    midpoint = (2 * raw + 1) * 128
    probability = min(midpoint, S - midpoint)
    require(
        128 <= probability and Fraction(probability, S) < Fraction(3, 40),
        "Declared endpoint is ordinary tail",
    )
    exponent = probability.bit_length() - 41
    mantissa = probability * (1 << -exponent)
    index = (mantissa - S) // (1 << 35)
    local = mantissa - (S + (2 * index + 1) * (1 << 34))
    accumulator = table[index][8]
    for degree in range(7, -1, -1):
        product = accumulator * local
        require(-(1 << 143) <= product < 1 << 143, "Selected word fullproduct144")
        accumulator = product // S + table[index][degree]
        require(-(1 << 71) <= accumulator < 1 << 71, "Selected word stored72")
    logarithm = accumulator + exponent * ln2
    native_negative_log = -logarithm
    require(native_negative_log > 0, "Native log exact signed negation; sqrt guard inactive")
    root = isqrt(native_negative_log * S)
    transformed = root - nearest_even(Fraction(8 * S, 5))
    ideal = endpoints(mp.iv.sqrt(-mp.iv.ln(iv(Fraction(probability, S)))) - iv(Fraction(8, 5)))
    error = max(abs(Fraction(transformed, S) - endpoint) for endpoint in ideal)
    require(
        error <= rho
        and native_negative_log.bit_length() <= 45
        and (native_negative_log * S).bit_length() <= 85
        and root.bit_length() <= 43,
        "Selected integer endpoint independently respects uniform envelope",
    )
    return {
        "q32_raw": raw,
        "tail_probability_raw": probability,
        "exponent": exponent,
        "mantissa_raw": mantissa,
        "table_index": index,
        "local_raw": local,
        "log_raw": logarithm,
        "negative_log_raw": native_negative_log,
        "sqrt_raw": root,
        "transform_r_raw": transformed,
        "independent_transform_error_upper_exact": pair(error),
        "sample_used_as_all_input_proof": False,
        "actual_gate_replay": False,
    }


def prepare(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM.resolve())
    if output.exists():
        raise FileExistsError("Fresh independent native-transform audit receipt required")
    frozen = {}
    for name in RECEIPTS:
        directory = PROGRAM / name
        summary = read(directory / "summary.json")
        require(
            summary.get("passed") is True and summary.get("budget_censored", False) is False,
            "Successful uncensored prerequisite: " + name,
        )
        if name == "A02_quantile_transform_run002":
            require(
                summary.get("native_transform_certificate_succeeded") is True,
                "Successful actual native-transform theorem required",
            )
        record = read(directory / "manifest.json")
        allowed = {"files", "frozen_inputs", "manifest_self_hash_excluded"}
        if name == "C06_pair_run001":
            allowed.add("historical_receipts_unchanged")
        require(
            {"files", "frozen_inputs"}.issubset(record)
            and set(record).issubset(allowed)
            and record.get("manifest_self_hash_excluded", True) is True
            and (
                "historical_receipts_unchanged" not in record
                or record["historical_receipts_unchanged"] is True
            )
            and all(isinstance(record[field], dict) for field in ("files", "frozen_inputs")),
            "Explicit manifest schema",
        )
        for field in ("files", "frozen_inputs"):
            for path, expected in record[field].items():
                bind(frozen, path, expected)
        bind(frozen, directory / "manifest.json", digest(directory / "manifest.json"))
    for path in [ROOT / "research/limitation_program_20261001" / name for name in CODE] + [
        SQRT,
        Path(sys.executable),
    ]:
        bind(frozen, path, digest(path))
    for path in Path(mp.__file__).parent.rglob("*.py"):
        bind(frozen, path, digest(path))
    verify(frozen)
    output.mkdir()
    try:
        prepare_receipt(output, frozen)
    except BaseException as failure:
        save(
            output / "preparation_failure.json",
            {"failure": traceback.format_exc(), "partial_files_preserved": True},
        )
        save(
            output / "summary.json",
            {
                "passed": False,
                "preparation_failed": True,
                "budget_censored": isinstance(failure, TimeoutError),
                "new_test_credit": 0,
                "new_quantum_gates_or_financial_path_evaluations": 0,
            },
        )
        finish(output, {"frozen_inputs": frozen})
        raise


def prepare_receipt(output, frozen):
    for name in CODE:
        source = ROOT / "research/limitation_program_20261001" / name
        destination = output / name
        shutil.copy2(source, destination)
        require(
            digest(destination) == frozen[relative(source)],
            "Executed audit copy equals frozen source bytes",
        )
        bind(frozen, destination, frozen[relative(source)])
    save(
        output / "protocol.json",
        {
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "local_only": True,
            "before_independent_proof_or_endpoint_word_evaluations": True,
            "requires_all_Stage_C_supervisors_and_timing_descendants_terminal": True,
            "every_frozen_insert_preserves_historical_expectations": True,
            "interpreter_mpmath_and_executed_snapshot_copy_bytes_hash_bound": True,
            "partial_prepare_failure_is_terminal_without_same_receipt_retry": True,
            "imported_producer_or_native_certificate_implementation": False,
            "fixed_interval_decimal_digits": DIGITS,
            "all_q32_normalization_table_exponent_classes": 960,
            "independently_reconciled_refreshed_tail_rows": 1024,
            "saved_real_tail_error_basis": (
                "Independently audited unchanged tail certificate; no CDF grid rerun"
            ),
            "rounding_audit_method": (
                "Exact published-decimal nearest-even, expanded geometric Horner floors, "
                "positive derivative sensitivity"
            ),
            "fixed_classical_endpoint_words": list(WORDS),
            "endpoint_words_not_all_input_proof": True,
            "new_pytest_tests_or_test_credit": 0,
            "new_quantum_gates_or_financial_path_evaluations": 0,
            "native_divider_dispatch_or_full_sampler_adoption": False,
            "actual_quantum_gate_cost": None,
            "process_CPU_limit_seconds": CPU_LIMIT,
            "elapsed_wall_limit_seconds": WALL_LIMIT,
            "bulk_output_hashing_and_frozen_verification_before_terminal_budget_check": True,
            "adaptive_precision_grid_or_retry": False,
            "preexisting_Stage_C_jobs_edited": False,
            "frozen_inputs": frozen,
            "python": sys.version,
            "executable": sys.executable,
        },
    )
    verify(frozen)
    print("Independent960+1024 native-transform audit prospectively frozen", flush=True)


def receipt_files(output):
    return {
        relative(path): digest(path)
        for path in sorted(output.rglob("*"))
        if path.is_file() and path.name != "manifest.json"
    }


def finish(output, protocol, files=None):
    if files is None:
        files = receipt_files(output)
    else:
        files = dict(files)
        files[relative(output / "summary.json")] = digest(output / "summary.json")
    save(
        output / "manifest.json",
        {
            "files": files,
            "frozen_inputs": protocol["frozen_inputs"],
            "manifest_self_hash_excluded": True,
        },
    )


def run(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM.resolve())
    if (output / "summary.json").exists():
        raise FileExistsError("Independent transform audit already terminal")
    protocol = read(output / "protocol.json")
    cpu, wall = time.process_time(), time.monotonic()
    files = None
    try:
        verify(protocol["frozen_inputs"])
        saved = read(TRANSFORM / "native_transform_certificate.json")
        require(
            saved["certified"] is True and saved["budget_censored"] is False,
            "Uncensored successful transform certificate",
        )
        require(
            saved["actual_coherent_leaf_or_quantum_gate_cost"] is None
            and saved["native_financial_path_arithmetic_certified"] is False
            and saved["coherent_loader_implemented_or_adopted"] is False
            and saved["accepted_Box_Muller_baseline_changed"] is False
            and saved["full_G2_closed"] is False,
            "Native mathematical transform is not source/path/cost adoption",
        )
        cases = list(ET.parse(TRANSFORM / "tests.xml").getroot().iter("testcase"))
        identities = {(case.attrib.get("classname", ""), case.attrib["name"]) for case in cases}
        require(
            len(cases) == len(identities) == 26
            and not any(
                case.find(tag) is not None
                for case in cases
                for tag in ("failure", "error", "skipped")
            ),
            "Reconcile prior26 unique successful cases without adding test credit",
        )
        mp.iv.dps = DIGITS
        table, ln2, bindings = audit_source()
        require(saved["source_bindings"] == bindings, "All audited original source bindings")
        log_error, max_poly, max_product, classes = audit_log_and_normalization(
            saved, table, ln2, cpu, wall
        )
        rho = audit_root_and_storage(saved, log_error, max_poly, max_product, ln2)
        refreshed, tail_error, central_error = audit_sensitivity(
            saved, read(TRANSFORM / "fresh_tail_sensitivity.json"), cpu, wall
        )
        fixtures = []
        for raw in WORDS:
            budget(cpu, wall)
            fixtures.append(audit_word(raw, table, ln2, rho))
        save(
            output / "independent_normalization_classes.json",
            {"classes": classes, "complete_classes": 960},
        )
        save(
            output / "independent_tail_sensitivity.json", {"rows": refreshed, "complete_rows": 1024}
        )
        save(
            output / "independent_endpoint_records.json",
            {"rows": fixtures, "all_input_proof_basis": False},
        )
        verify(protocol["frozen_inputs"])
        files = receipt_files(output)
        budget(cpu, wall)
        save(
            output / "summary.json",
            {
                "passed": True,
                "local_only": True,
                "budget_censored": False,
                "independent_all960_native_normalization_log_classes_verified": True,
                "independent_all1024_fresh_tail_ledgers_verified": True,
                "exact_log_negation_and_exponent_floor_cancellation_verified": True,
                "native_sqrt_input45_shifted85_output43_and_shift_rho_verified": True,
                "native_log_error_upper_exact": pair(log_error),
                "native_transform_error_upper_exact": pair(rho),
                "native_tail_quantile_error_upper_exact": pair(tail_error),
                "central_quantile_error_upper_exact": pair(central_error),
                "combined_quantile_error_upper_exact": pair(max(tail_error, central_error)),
                "central_denominator64_bound_independently_verified": True,
                "prior26_tests_reconciled_without_recredit": True,
                "new_test_credit": 0,
                "new_quantum_gates_or_financial_path_evaluations": 0,
                "classical_endpoint_diagnostics": len(fixtures),
                "samples_as_completeness_proof": False,
                "coherent_sampler_or_native_divider_adopted": False,
                "actual_quantum_gate_cost": None,
                "full_G2_or_quantum_advantage_established": False,
                "elapsed_process_CPU_seconds": time.process_time() - cpu,
                "elapsed_wall_seconds": time.monotonic() - wall,
            },
        )
    except BaseException as exc:
        save(
            output / "summary.json",
            {
                "passed": False,
                "budget_censored": isinstance(exc, TimeoutError),
                "terminal_failure": traceback.format_exc(),
                "new_test_credit": 0,
                "new_quantum_gates_or_financial_path_evaluations": 0,
            },
        )
        finish(output, protocol, files)
        raise
    finish(output, protocol, files)
    print(
        "Independent native transform audit retained; no coherent source or financial adoption",
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run"))
    parser.add_argument(
        "--output", type=Path, default=PROGRAM / "A02_quantile_transform_audit_run001"
    )
    args = parser.parse_args()
    (prepare if args.mode == "prepare" else run)(args.output)
