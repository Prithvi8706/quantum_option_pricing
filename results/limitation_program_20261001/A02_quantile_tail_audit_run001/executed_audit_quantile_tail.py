"""Bounded independent ordinary AS241 tail audit; no producer math imports.

Reconcile every saved cell algebraically. Independently differentiate the
published rational function and enclose four fixed cells at higher precision,
using a different integrated-exp degree and interval exp density evaluation.
The supplied exact-floor transform remains conditional and unimplemented.
"""

from __future__ import annotations

# Proof and receipt explanations use ordinary prose.
# ruff: noqa: E501

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from math import comb, factorial
from pathlib import Path
import re
import shutil
import sys
import time
import traceback
import xml.etree.ElementTree as ET

import mpmath as mp

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
SOURCE = PROGRAM / "A02_quantile_tail_run001"
R_SOURCE = PROGRAM / "A02_quantile_census_run001/primary_sources/R_qnorm.c"
CELLS = 1024
RMAX = Fraction(321, 100)
SHIFT = Fraction(8, 5)
DOMAIN = Fraction(13, 2)
Q = 1 << 40
ULP = Fraction(1, Q)
TARGET = Fraction(1, 100000000)
SELECTED = (0, 1023, 511, 512)
PARTS = 8
CDF_DEGREE = 160
PI = A = B = None


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    with Path(path).open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def relative(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def bind(frozen, name, expected):
    path = Path(str(name).replace("\\", "/"))
    resolved = path.resolve() if path.is_absolute() else (ROOT / path).resolve()
    normalized = relative(resolved)
    if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
        raise ValueError("Explicit prerequisite SHA256 required")
    if normalized in frozen and frozen[normalized] != expected:
        raise ValueError("Historical prerequisite bytes conflict: " + normalized)
    frozen[normalized] = expected


def budget(started):
    if time.process_time() - started >= 180:
        raise TimeoutError("Fixed180CPU tail audit budget")


def receipt_files(output):
    return {
        relative(path): sha(path)
        for path in sorted(output.rglob("*"))
        if path.is_file() and path.name != "manifest.json"
    }


def pair(value):
    value = Fraction(value)
    return [value.numerator, value.denominator]


def exact(value):
    assert isinstance(value, list) and len(value) == 2
    assert all(type(part) is int for part in value)
    result = Fraction(*value)
    assert pair(result) == value
    return result


def verify(files):
    for name, digest in files.items():
        assert sha(ROOT / name) == digest, ("Frozen dependency changed", name)


def iv(value):
    value = Fraction(value)
    return mp.iv.mpf(value.numerator) / value.denominator


def endpoint(value):
    sign, mantissa, exponent, _ = value
    return Fraction((-1) ** sign * mantissa) * Fraction(2) ** exponent


def bounds(value):
    return tuple(endpoint(part) for part in value._mpi_)


def interval(left, right):
    assert left <= right
    return mp.iv.mpf([iv(left).a, iv(right).b])


def magnitude(value):
    return max(map(abs, bounds(value)))


def independent_pi():
    assert (Fraction(1, 2) + Fraction(1, 3)) / (1 - Fraction(1, 6)) == 1
    pieces = []
    for denominator in (2, 3):
        value = sum(
            (Fraction((-1) ** j, (2 * j + 1) * denominator ** (2 * j + 1)) for j in range(240)),
            Fraction(0),
        )
        pieces.append((value, value + Fraction(1, 481 * denominator**481)))
    return interval(4 * sum(row[0] for row in pieces), 4 * sum(row[1] for row in pieces))


def published_coefficients():
    source = R_SOURCE.read_text(encoding="utf-8")
    branch = source.split("if (r <= 5.)", 1)[1].split("else if(r <= 27)", 1)[0]
    assert "r += -1.6;" in branch
    numerator, denominator = branch.split("val =", 1)[1].split("/", 1)
    pattern = r"(?<!\w)(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?"
    coefficients = tuple(
        tuple(Fraction(token) for token in reversed(re.findall(pattern, part)))
        for part in (numerator, denominator)
    )
    assert len(coefficients[0]) == len(coefficients[1]) == 8
    assert min(coefficients[0] + coefficients[1]) > 0 and coefficients[1][0] == 1
    return coefficients


def polynomial_derivative(coefficients, degree, r):
    return sum(
        (
            iv(coefficient * (factorial(k) // factorial(k - degree))) * r ** (k - degree)
            for k, coefficient in enumerate(coefficients)
            if k >= degree
        ),
        iv(0),
    )


def rational_derivatives(r):
    numerator = [polynomial_derivative(A, degree, r) for degree in range(5)]
    denominator = [polynomial_derivative(B, degree, r) for degree in range(5)]
    assert bounds(denominator[0])[0] >= 1
    output = []
    # Differentiate N=zD explicitly, unlike producer's normalized-jet inverse.
    for degree in range(5):
        correction = sum(
            (comb(degree, j) * denominator[j] * output[degree - j] for j in range(1, degree + 1)),
            iv(0),
        )
        output.append((numerator[degree] - correction) / denominator[0])
    return output


def tighten(whole, center, radius):
    output = list(whole)
    for degree in (3, 2, 1, 0):
        delta = magnitude(output[degree + 1]) * radius
        a, b = bounds(output[degree])
        c, d = bounds(center[degree])
        output[degree] = interval(max(a, c - delta), min(b, d + delta))
    return output


def independent_cdf(z):
    assert magnitude(z) <= DOMAIN
    # Ascending recurrence prevents tiny polynomial-leading coefficient effects.
    # Exp(-s)'s degree160 derivative remainder is <=s^161/161! for s>=0;
    # integration gives the exact bound below for either sign of z.
    argument = z**2 / 2
    term = total = iv(1)
    for k in range(1, CDF_DEGREE + 1):
        term = term * argument / k
        total += (-1) ** k * term / (2 * k + 1)
    remainder = DOMAIN ** (2 * CDF_DEGREE + 3) / (
        2 ** (CDF_DEGREE + 1) * factorial(CDF_DEGREE + 1) * (2 * CDF_DEGREE + 3)
    )
    return iv(Fraction(1, 2)) + (z * total + interval(-remainder, remainder)) / mp.iv.sqrt(2 * PI)


def residual_derivatives(r, z, include_residual=True):
    z0, z1, z2, z3, z4 = z
    t = r + iv(SHIFT)
    probability = mp.iv.exp(-(t**2))
    density = mp.iv.exp(-(z0**2) / 2) / mp.iv.sqrt(2 * PI)
    return [
        independent_cdf(-z0) - probability if include_residual else None,
        -density * z1 + 2 * t * probability,
        density * (z0 * z1**2 - z2) + (2 - 4 * t**2) * probability,
        density * ((1 - z0**2) * z1**3 + 3 * z0 * z1 * z2 - z3) + (8 * t**3 - 12 * t) * probability,
        density
        * (
            (z0**3 - 3 * z0) * z1**4
            + 6 * (1 - z0**2) * z1**2 * z2
            + 3 * z0 * z2**2
            + 4 * z0 * z1 * z3
            - z4
        )
        + (-16 * t**4 + 48 * t**2 - 12) * probability,
    ]


def contained(saved, computed):
    a, b = map(exact, saved)
    c, d = bounds(computed)
    assert a <= c <= d <= b


def nearest_even(coefficient):
    value = coefficient * Q
    integer, remainder = divmod(value.numerator, value.denominator)
    return integer + int(
        2 * remainder > value.denominator or (2 * remainder == value.denominator and integer % 2)
    )


def polynomial_exact(coefficients, r):
    return sum((coefficient * r**k for k, coefficient in enumerate(coefficients)), Fraction(0))


def native_horner(coefficients, raw_r):
    value = coefficients[-1]
    for coefficient in reversed(coefficients[:-1]):
        value = (value * raw_r) // Q + coefficient
    return value


def native_error(lower, upper):
    raw_a, raw_b = tuple(map(nearest_even, A)), tuple(map(nearest_even, B))

    # Expand coefficient errors and all seven multiply-floor ULPs rather than
    # reuse the producer's recursive Horner-error implementation.
    def polynomial_error(coefficients, native):
        coefficients_error = sum(
            (
                abs(Fraction(raw, Q) - c) * upper**k
                for k, (raw, c) in enumerate(zip(native, coefficients, strict=True))
            ),
            Fraction(0),
        )
        floor_error = ULP * sum((upper**k for k in range(7)), Fraction(0))
        derivative = sum(
            (k * c * upper ** (k - 1) for k, c in enumerate(coefficients) if k), Fraction(0)
        )
        return coefficients_error + floor_error + ULP * derivative

    lower_raw = (lower.numerator * Q) // lower.denominator
    denominator = Fraction(native_horner(raw_b, lower_raw), Q)
    assert denominator >= 1
    ea, eb = polynomial_error(A, raw_a), polynomial_error(B, raw_b)
    return dict(
        hypothetical_exact_transform_floor_error_upper_exact=pair(ULP),
        native_denominator_lower_exact=pair(denominator),
        numerator_polynomial_error_upper_exact=pair(ea),
        denominator_polynomial_error_upper_exact=pair(eb),
        native_rational_arithmetic_error_upper_exact=pair((ea + DOMAIN * eb) / denominator + ULP),
    )


def audit_widths(native):
    raw_a, raw_b = tuple(map(nearest_even, A)), tuple(map(nearest_even, B))
    assert native["native_A_raw_ascending"] == list(raw_a)
    assert native["native_B_raw_ascending"] == list(raw_b)
    assert min(raw_a + raw_b) > 0 and raw_b[0] == Q

    def suffix_values(raw):
        return [
            sum((Fraction(raw[k], Q) * RMAX ** (k - start) for k in range(start, 8)), Fraction(0))
            for start in reversed(range(8))
        ]

    a_values, b_values = suffix_values(raw_a), suffix_values(raw_b)
    stored = max(*a_values, *b_values, RMAX, Fraction(1))
    product_upper = max(a_values[:-1] + b_values[:-1]) * RMAX * Q**2
    dividend_upper = a_values[-1] * Q**2
    denominator_upper = b_values[-1] * Q
    expected = dict(
        maximum_stored_fixed_point_value_upper_exact=pair(stored),
        maximum_full_product_raw_upper_exact=pair(product_upper),
        maximum_shifted_division_numerator_raw_upper_exact=pair(dividend_upper),
        maximum_denominator_raw_upper_exact=pair(denominator_upper),
    )
    assert all(native[key] == value for key, value in expected.items())
    assert stored * Q < 1 << 71 and product_upper < 1 << 143
    assert dividend_upper < 1 << 112 and denominator_upper < 1 << 64
    assert native["actual_coherent_log_sqrt_transform_error_bound"] is None
    assert native["actual_coherent_transform_leaf"] is None
    assert native["actual_quantum_gate_cost"] is None
    assert native["hypothetical_transform_implemented"] is False
    assert native["actual_reversible_divider_emitted_or_replayed"] is False
    for key in (
        "signed72_stored_values_no_overflow",
        "signed144_full_products_no_overflow",
        "unsigned112_dividend_no_truncation",
        "unsigned64_denominator_no_truncation",
        "native_denominator_floor_at_one_guard_inactive",
        "native_quotient_output72_no_truncation",
    ):
        assert native[key] is True
    # Native B>=Q: raw quotient floor((Araw*Q)/Braw)<=Araw<2^71.
    return dict(
        **expected,
        positive_denominator_at_least_one=True,
        mathematical_unsigned64_divisor_verified=True,
        signed_restored_output72_safe=True,
        actual_gate_divider_interface_or_cost_validated=False,
    )


def audit_domain(domain):
    for saved, value in (
        (domain["expanded_minimum_probability_interval_exact"], (RMAX + SHIFT) ** 2),
        (domain["expanded_maximum_probability_interval_exact"], SHIFT**2),
    ):
        contained(saved, mp.iv.exp(-iv(value)))
    contained(domain["Phi_minus_6_point_5_interval_exact"], independent_cdf(iv(-DOMAIN)))
    upper_cdf = exact(domain["Phi_minus_6_point_5_interval_exact"][1])
    assert upper_cdf < exact(domain["expanded_minimum_probability_interval_exact"][0])
    assert upper_cdf < Fraction(1, 1 << 33)
    degree4 = sum((Fraction(7, 10) ** k / factorial(k) for k in range(5)), Fraction(0))
    assert degree4 > 2 and exact(domain["positive_degree4_exp_7_over_10_lower_exact"]) == degree4
    assert Fraction(33 * 7, 10) < (RMAX + SHIFT) ** 2 < 25
    assert exact(domain["expanded_maximum_probability_interval_exact"][0]) > Fraction(3, 40)
    assert domain["q32_midpoint_minimum_tail_probability_exact"] == [1, 1 << 33]
    assert domain["ordinary_tail_probability_upper_exclusive_exact"] == [3, 40]
    assert domain["actual_q32_extreme_tail_branch_absent"] is True
    return dict(
        all_q32_ordinary_tail_inputs_covered=True,
        true_quantile_absolute_upper_exact=pair(DOMAIN),
        Chernoff_density_conversion="Gaussian mgf Markov gives Phi(-x)<=exp(-x^2/2), hence true |q|<=sqrt(2)*t; saved positive rational |z|^2<=2*t_lower^2 ensures every point between them has density>=prefactor*exp(-t_upper^2).",
        central_branch_tie_not_a_q32_midpoint=True,
        exact_transform_floor_hypothetical=True,
    )


def audit_ledger(cells, certificate, started):
    real_errors, native_errors, totals = [], [], []
    for index, cell in enumerate(cells):
        lower, upper = index * RMAX / CELLS, (index + 1) * RMAX / CELLS
        center, radius = (lower + upper) / 2, (upper - lower) / 2
        assert cell["cell_index"] == index and cell["r_domain_exact"] == [pair(lower), pair(upper)]
        assert exact(cell["center_r_exact"]) == center and exact(cell["radius_exact"]) == radius
        rational_lower, rational_upper = map(exact, cell["rational_z_range_exact"])
        center_exact = polynomial_exact(A, center) / polynomial_exact(B, center)
        assert 0 <= rational_lower <= center_exact <= rational_upper <= DOMAIN
        center_left, center_right = map(exact, cell["center_rational_z_interval_exact"])
        assert center_left <= center_exact <= center_right
        assert exact(cell["rational_z_squared_upper_exact"]) == rational_upper**2
        assert exact(cell["twice_minimum_t_squared_exact"]) == 2 * (lower + SHIFT) ** 2
        assert rational_upper**2 <= 2 * (lower + SHIFT) ** 2
        keys = (
            "center_residual_interval_exact",
            "center_first_residual_derivative_interval_exact",
            "center_second_residual_derivative_interval_exact",
            "center_third_residual_derivative_interval_exact",
        )
        center_bounds = [max(abs(exact(value)) for value in cell[key]) for key in keys]
        derivative = exact(cell["fourth_residual_derivative_absolute_upper_exact"])
        assert derivative >= 0
        residual = (
            sum((radius**k * center_bounds[k] / factorial(k) for k in range(4)), Fraction(0))
            + radius**4 * derivative / 24
        )
        assert exact(cell["CDF_residual_absolute_upper_exact"]) == residual
        density = exact(cell["inverse_density_lower_exact"])
        independently_enclosed_density = mp.iv.exp(-iv((upper + SHIFT) ** 2)) / mp.iv.sqrt(2 * PI)
        assert 0 < density <= bounds(independently_enclosed_density)[0]
        real_error = residual / density
        assert exact(cell["real_quantile_error_upper_exact"]) == real_error
        recomputed_native = native_error(lower, upper)
        assert cell["native_arithmetic"] == recomputed_native
        native = exact(recomputed_native["native_rational_arithmetic_error_upper_exact"])
        total = real_error + native
        assert exact(cell["total_conditioned_tail_quantile_error_upper_exact"]) == total
        real_errors.append(real_error)
        native_errors.append(native)
        totals.append(total)
        budget(started)
    assert len(cells) == CELLS
    assert exact(certificate["real_approximation_error_upper_exact"]) == max(real_errors)
    assert exact(certificate["native_rational_arithmetic_error_upper_exact"]) == max(native_errors)
    assert exact(certificate["total_conditioned_tail_quantile_error_upper_exact"]) == max(totals)
    assert max(totals) <= TARGET and certificate["certified"] is True
    return dict(
        ledger_rows_reconciled=CELLS,
        exact_partition_covers_expanded_domain=True,
        positive_Chernoff_density_bounds_independently_verified=CELLS,
        original_floor_conditioned_native_errors_recomputed=CELLS,
        maximum_cell_index=totals.index(max(totals)),
        maximum_real_error_exact=pair(max(real_errors)),
        maximum_native_error_exact=pair(max(native_errors)),
        maximum_conditioned_total_error_exact=pair(max(totals)),
        target_exact=pair(TARGET),
    )


def audit_selected(saved, started):
    lower, upper = map(exact, saved["r_domain_exact"])
    center, radius = (lower + upper) / 2, (upper - lower) / 2
    center_z = rational_derivatives(iv(center))
    residuals = residual_derivatives(iv(center), center_z)
    contained(saved["center_rational_z_interval_exact"], center_z[0])
    keys = (
        "center_residual_interval_exact",
        "center_first_residual_derivative_interval_exact",
        "center_second_residual_derivative_interval_exact",
        "center_third_residual_derivative_interval_exact",
    )
    for key, value in zip(keys, residuals[:4], strict=True):
        contained(saved[key], value)
    whole_derivative = Fraction(0)
    lower_z, upper_z = map(exact, saved["rational_z_range_exact"])
    parts = []
    for index in range(PARTS):
        a, b = (
            lower + index * (upper - lower) / PARTS,
            lower + (index + 1) * (upper - lower) / PARTS,
        )
        c, radius_part = (a + b) / 2, (b - a) / 2
        derivatives = tighten(
            rational_derivatives(interval(a, b)), rational_derivatives(iv(c)), radius_part
        )
        assert lower_z <= bounds(derivatives[0])[0] <= bounds(derivatives[0])[1] <= upper_z
        fourth = residual_derivatives(interval(a, b), derivatives, False)[4]
        fourth_upper = magnitude(fourth)
        whole_derivative = max(whole_derivative, fourth_upper)
        parts.append(
            dict(
                index=index,
                domain_exact=[pair(a), pair(b)],
                independent_fourth_derivative_upper_exact=pair(fourth_upper),
            )
        )
        budget(started)
    assert whole_derivative <= exact(saved["fourth_residual_derivative_absolute_upper_exact"])
    residual = (
        sum((radius**k * magnitude(residuals[k]) / factorial(k) for k in range(4)), Fraction(0))
        + radius**4 * whole_derivative / 24
    )
    assert residual <= exact(saved["CDF_residual_absolute_upper_exact"])
    return dict(
        cell_index=saved["cell_index"],
        independent_center_residual_intervals_exact=[
            [pair(a), pair(b)] for a, b in map(bounds, residuals[:4])
        ],
        independent_fourth_derivative_upper_exact=pair(whole_derivative),
        independent_CDF_residual_upper_exact=pair(residual),
        complete_cell_covered_by_fixed_independent_subintervals=parts,
        saved_native_arithmetic_reconciled_without_new_gate_or_input_execution=True,
    )


def prepare(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM)
    if output.exists():
        raise FileExistsError("Fresh immutable tail-audit receipt required")
    source_summary = read(SOURCE / "summary.json")
    if not (
        source_summary.get("passed") is True
        and source_summary.get("tail_certificate_succeeded") is True
        and source_summary.get("budget_censored") is False
    ):
        raise ValueError("Successful uncensored complete tail certificate required")
    manifest = read(SOURCE / "manifest.json")
    if (
        not {"files", "frozen_inputs"}.issubset(manifest)
        or not set(manifest).issubset({"files", "frozen_inputs", "manifest_self_hash_excluded"})
        or manifest.get("manifest_self_hash_excluded", True) is not True
    ):
        raise ValueError("Explicit prerequisite manifest schema required")
    frozen = {}
    for field in ("files", "frozen_inputs"):
        for name, expected in manifest[field].items():
            bind(frozen, name, expected)
    bind(frozen, SOURCE / "manifest.json", sha(SOURCE / "manifest.json"))
    own = Path(__file__).resolve()
    for path in [own, Path(sys.executable), R_SOURCE] + sorted(
        Path(mp.__file__).parent.rglob("*.py")
    ):
        bind(frozen, path, sha(path))
    verify(frozen)
    output.mkdir()
    try:
        prepare_receipt(output, own, frozen)
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
                "new_distinct_fixture_credit": 0,
            },
        )
        finish_manifest(output, protocol={"frozen_inputs": frozen})
        raise


def prepare_receipt(output, own, frozen):
    destination = output / "executed_audit_quantile_tail.py"
    shutil.copy2(own, destination)
    if sha(destination) != frozen[relative(own)]:
        raise ValueError("Executed tail-audit snapshot differs from frozen source bytes")
    bind(frozen, destination, frozen[relative(own)])
    save(
        output / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            local_only=True,
            before_independent_math_or_cell_recomputation=True,
            frozen_inputs=frozen,
            interpreter_sha256=sha(sys.executable),
            interpreter_and_all_mpmath_python_sources_hash_bound=True,
            source_receipt=relative(SOURCE),
            full_saved_ledger_rows=CELLS,
            selected_saved_cell_indices=list(SELECTED),
            maximum_independently_recomputed_saved_cells=8,
            actual_selected_saved_cells=4,
            fixed_subintervals_per_selected_cell=PARTS,
            independent_interval_decimal_precision=140,
            independent_pi="240-term exact alternating atan(1/2)+atan(1/3)",
            independent_CDF_integrated_exponential_degree=CDF_DEGREE,
            independent_CDF_remainder="6.5^323/(2^161*161!*323), integrated Lagrange bound, both signs",
            independent_density_and_transformed_probability="mpmath interval exp",
            independent_rational_derivatives="Differentiate published numerator and denominator polynomials directly; solve N=zD derivative recurrence through degree4",
            independent_native_error="Expanded coefficient-error powers + seven floor ULP powers; explicit derivative input-floor error and monotone integer native denominator",
            process_CPU_limit_seconds=180,
            terminal_verification_and_bulk_output_hashing_within_CPU_budget=True,
            full_1024_cell_derivative_reruns=0,
            producer_tests_reexecuted=0,
            new_financial_paths_or_native_gates=0,
            actual_log_sqrt_transform_included=False,
            accepted_Box_Muller_or_price_source_changed=False,
        ),
    )
    print("Ordinary-tail bounded independent audit prospectively frozen", flush=True)


def run(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM)
    if (output / "summary.json").exists():
        raise FileExistsError("Tail-audit receipt already terminal; no same-receipt retry")
    protocol = read(output / "protocol.json")
    try:
        run_audit(output)
    except BaseException as failure:
        if not (output / "summary.json").exists():
            save(
                output / "failure.json",
                {"failure_type": type(failure).__name__, "failure": traceback.format_exc()},
            )
            save(
                output / "summary.json",
                {
                    "passed": False,
                    "local_only": True,
                    "budget_censored": isinstance(failure, TimeoutError),
                    "failure_type": type(failure).__name__,
                    "message": str(failure),
                    "producer_fixture_reexecutions": 0,
                    "new_distinct_fixture_credit": 0,
                    "new_native_or_financial_gates": 0,
                    "accepted_finite_Box_Muller_source_changed": False,
                    "quantum_advantage_claim": False,
                },
            )
            finish_manifest(output, protocol=protocol)
        raise


def run_audit(output):
    global PI, A, B
    started = time.process_time()
    output = Path(output).resolve()
    assert not (output / "summary.json").exists()
    protocol = read(output / "protocol.json")
    verify(protocol["frozen_inputs"])
    assert sha(sys.executable) == protocol["interpreter_sha256"]
    mp.iv.dps = 140
    PI = independent_pi()
    A, B = published_coefficients()
    certificate = read(SOURCE / "tail_certificate.json")
    source_protocol = read(SOURCE / "protocol.json")
    assert source_protocol["before_tests_or_fixed_cell_tail_evaluation"] is True
    assert source_protocol["fixed_equal_r_cells"] == CELLS
    assert (
        source_protocol["Taylor_jet_degree"] == 4
        and source_protocol["dyadic_outward_precision_bits"] == 128
    )
    assert tuple(map(Fraction, certificate["source_coefficients"]["A_decimals_ascending"])) == A
    assert tuple(map(Fraction, certificate["source_coefficients"]["B_decimals_ascending"])) == B
    assert certificate["source_coefficients"]["sha256"] == sha(R_SOURCE)
    assert (
        certificate["uniform_bits"] == 32
        and certificate["fraction_bits"] == 40
        and certificate["native_word_width"] == 72
    )
    assert certificate["conditioned_on_hypothetical_exact_transform_floor"] is True
    for key in (
        "actual_coherent_log_sqrt_transform_implemented",
        "coherent_loader_implemented_or_adopted",
        "native_financial_path_arithmetic_certified",
        "accepted_Box_Muller_baseline_changed",
        "full_G2_closed",
    ):
        assert certificate[key] is False
    for key in (
        "actual_coherent_log_sqrt_input_error_certificate",
        "actual_reversible_divider_width_cleanup_validation",
        "actual_quantum_gate_cost",
    ):
        assert certificate[key] is None
    xml = ET.parse(SOURCE / "tests.xml").getroot()
    tests = list(xml.iter("testcase"))
    assert (
        len(tests) == 40
        and len({(item.attrib.get("classname"), item.attrib["name"]) for item in tests}) == 40
    )
    assert (
        not list(xml.iter("failure"))
        and not list(xml.iter("error"))
        and not list(xml.iter("skipped"))
    )
    data = read(SOURCE / "cell_bounds.json")
    assert data["fixed_cells"] == data["completed_cells"] == CELLS
    domain = audit_domain(certificate["domain_proof"])
    widths = audit_widths(certificate["native_interface"])
    ledger = audit_ledger(data["cells"], certificate, started)
    selected = [audit_selected(data["cells"][index], started) for index in SELECTED]
    save(output / "independent_selected_cells.json", selected)
    save(output / "complete_ledger_reconciliation.json", ledger)
    save(output / "domain_and_native_widths.json", dict(domain=domain, widths=widths))
    source_summary = read(SOURCE / "summary.json")
    assert source_summary["passed"] is True and source_summary["tail_certificate_succeeded"] is True
    assert source_summary["completed_cells"] == CELLS and source_summary["fixtures_passed"] == 40
    assert (
        source_summary["total_conditioned_tail_quantile_error_upper_exact"]
        == ledger["maximum_conditioned_total_error_exact"]
    )
    verify(protocol["frozen_inputs"])
    files = receipt_files(output)
    budget(started)
    save(
        output / "summary.json",
        dict(
            passed=True,
            budget_censored=False,
            local_only=True,
            producer_distinct_tests_reconciled=40,
            producer_fixture_reexecutions=0,
            new_distinct_fixture_credit=0,
            complete_saved_ledger_rows_reconciled=CELLS,
            independently_recomputed_saved_cells=len(SELECTED),
            actual_full_1024_cell_derivative_reruns=0,
            independent_cell_subintervals=PARTS * len(SELECTED),
            published_R_ordinary_C_D_coefficients_verified=True,
            negative_Phi_chain_rule_and_fourth_remainders_verified=True,
            Gaussian_domain_CDF_analytic_remainder_and_Chernoff_density_verified=True,
            native72_product144_dividend112_divisor64_mathematical_widths_verified=True,
            exact_transform_floor_condition_still_required=True,
            rational_approximation_distinct_from_exact_inverse_CDF_floor=True,
            conditioned_tail_quantile_error_upper_exact=ledger[
                "maximum_conditioned_total_error_exact"
            ],
            target_exact=pair(TARGET),
            actual_coherent_log_sqrt_error_certified=False,
            actual_transform_or_divider_gates_cost_and_cleanup_certified=False,
            prior_exact_floor_quantile_law_replaced=False,
            accepted_finite_Box_Muller_source_changed=False,
            new_native_or_financial_gates=0,
            new_financial_price_observations=0,
            continuous_path_or_full_G2_certificate=False,
            quantum_advantage_claim=False,
            elapsed_process_CPU_seconds=time.process_time() - started,
        ),
    )
    finish_manifest(output, protocol=protocol, files=files)
    print("Ordinary-tail bounded independent audit PASS", flush=True)


def finish_manifest(output, protocol=None, files=None):
    if protocol is None:
        protocol = read(output / "protocol.json")
    if files is None:
        files = receipt_files(output)
    else:
        files = dict(files)
        files[relative(output / "summary.json")] = sha(output / "summary.json")
    save(
        output / "manifest.json",
        dict(
            files=files,
            frozen_inputs=protocol["frozen_inputs"],
            manifest_self_hash_excluded=True,
        ),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, default=PROGRAM / "A02_quantile_tail_audit_run001")
    args = parser.parse_args()
    if args.phase == "prepare":
        prepare(args.output)
    else:
        run(args.output)
