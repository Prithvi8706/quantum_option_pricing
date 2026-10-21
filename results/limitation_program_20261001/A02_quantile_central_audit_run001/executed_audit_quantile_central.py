"""Bounded independent audit of the two frozen central AS241 proof attempts.

No producer math is imported. Differentiate the numerator and denominator
polynomials directly, solve the quotient derivative recurrence, and use mpmath
intervals on four selected saved cells per version. Full-grid work is limited
to the saved ledger's tiling, maximum and error sums. No quantile gates or
financial paths are evaluated.
"""

from __future__ import annotations

# Receipt explanations are readable prose.
# ruff: noqa: E501

import argparse
import ast
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
VERSIONS = (("A02_quantile_central_run001", 3), ("A02_quantile_central_run002", 4))
SELECTED = (0, 2047, 1023, 1024)
PARTS = 8
QMAX = Fraction(17, 40)
RMAX = QMAX**2
NATIVE_Q = 1 << 40
TARGET = Fraction(1, 100000000)
PI = None
A = B = None


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


def pair(value):
    value = Fraction(value)
    return [value.numerator, value.denominator]


def exact(value):
    result = Fraction(*value)
    assert pair(result) == value
    return result


def verify(files):
    for name, digest in files.items():
        assert sha(ROOT / name) == digest, ("frozen dependency changed", name)


def iv(value):
    value = Fraction(value)
    return mp.iv.mpf(value.numerator) / value.denominator


def endpoint(value):
    sign, mantissa, exponent, _ = value
    return Fraction((-1) ** sign * mantissa) * Fraction(2) ** exponent


def bounds(value):
    return tuple(endpoint(part) for part in value._mpi_)


def interval(left, right):
    return mp.iv.mpf([iv(left).a, iv(right).b])


def magnitude(value):
    left, right = bounds(value)
    return max(abs(left), abs(right))


def independent_pi():
    assert (Fraction(1, 2) + Fraction(1, 3)) / (1 - Fraction(1, 6)) == 1
    values = []
    for denominator in (2, 3):
        partial = sum(
            (Fraction((-1) ** j, (2 * j + 1) * denominator ** (2 * j + 1)) for j in range(240)),
            Fraction(0),
        )
        values.append((partial, partial + Fraction(1, 481 * denominator**481)))
    left, right = (4 * sum(row[k] for row in values) for k in (0, 1))
    return interval(left, right)


def published_coefficients(path):
    text = Path(path).read_text(encoding="utf-8")
    branch = text.split("if (fabs(q) <= .425)", 1)[1].split("else {", 1)[0]
    assert "r = .180625 - q * q" in branch
    expression = branch.split("val =", 1)[1]
    decimals = re.findall(r"\d+(?:\.\d*)?(?:[eE][+-]?\d+)?", expression)
    assert len(decimals) == 16
    return tuple(map(Fraction, reversed(decimals[:8]))), tuple(
        map(Fraction, reversed(decimals[8:]))
    )


def polynomial_derivative(coefficients, degree, r):
    return sum(
        (
            iv(coefficient * (factorial(k) // factorial(k - degree))) * r ** (k - degree)
            for k, coefficient in enumerate(coefficients)
            if k >= degree
        ),
        iv(0),
    )


def compose_r_derivatives(coefficients, q):
    r, r1, r2 = iv(RMAX) - q**2, -2 * q, iv(-2)
    derivatives = [polynomial_derivative(coefficients, degree, r) for degree in range(5)]
    return [
        derivatives[0],
        derivatives[1] * r1,
        derivatives[2] * r1**2 + derivatives[1] * r2,
        derivatives[3] * r1**3 + 3 * derivatives[2] * r1 * r2,
        derivatives[4] * r1**4 + 6 * derivatives[3] * r1**2 * r2 + 3 * derivatives[2] * r2**2,
    ]


def rational_derivatives(q):
    numerator_poly, denominator = compose_r_derivatives(A, q), compose_r_derivatives(B, q)
    numerator = [
        q * numerator_poly[degree] + (degree * numerator_poly[degree - 1] if degree else 0)
        for degree in range(5)
    ]
    assert bounds(denominator[0])[0] > 0
    result = []
    for degree in range(5):
        correction = sum(
            (comb(degree, j) * denominator[j] * result[degree - j] for j in range(1, degree + 1)),
            iv(0),
        )
        result.append((numerator[degree] - correction) / denominator[0])
    return result


def tighten(whole, center, radius, order):
    result = list(whole)
    for degree in range(order - 1, -1, -1):
        excursion = magnitude(result[degree + 1]) * radius
        original_lo, original_hi = bounds(result[degree])
        center_lo, center_hi = bounds(center[degree])
        lower, upper = (
            max(original_lo, center_lo - excursion),
            min(original_hi, center_hi + excursion),
        )
        assert lower <= upper
        result[degree] = interval(lower, upper)
    return result


def gaussian_cdf(z):
    assert magnitude(z) <= Fraction(3, 2)
    # Independently integrate a 72-degree exponential Taylor polynomial;
    # Taylor's derivative bound is <=1 on the nonnegative t domain.
    integral = sum(
        (
            iv(Fraction((-1) ** j, 2**j * factorial(j) * (2 * j + 1))) * z ** (2 * j + 1)
            for j in range(73)
        ),
        iv(0),
    )
    remainder = Fraction(3, 2) ** 147 / (2**73 * factorial(73) * 147)
    return iv(Fraction(1, 2)) + (integral + interval(-remainder, remainder)) / mp.iv.sqrt(2 * PI)


def residual_derivatives(q, derivatives):
    z, z1, z2, z3, z4 = derivatives
    density = mp.iv.exp(-(z**2) / 2) / mp.iv.sqrt(2 * PI)
    return [
        gaussian_cdf(z) - q - iv(Fraction(1, 2)),
        density * z1 - 1,
        density * (z2 - z * z1**2),
        density * (z3 - 3 * z * z1 * z2 + (z**2 - 1) * z1**3),
        density
        * (
            z4
            - 4 * z * z1 * z3
            - 3 * z * z2**2
            + 6 * (z**2 - 1) * z1**2 * z2
            + (3 * z - z**3) * z1**4
        ),
    ]


def saved_interval_contains_independent(saved, computed):
    lower, upper = map(exact, saved)
    left, right = bounds(computed)
    assert lower <= left <= right <= upper


def audit_saved_cell(saved, order):
    index = saved["cell_index"]
    left, right = -QMAX + index * (2 * QMAX / 2048), -QMAX + (index + 1) * (2 * QMAX / 2048)
    center, radius = (left + right) / 2, (right - left) / 2
    assert saved["q_domain_exact"] == list(map(pair, (left, right)))
    assert exact(saved["center_q_exact"]) == center and exact(saved["radius_exact"]) == radius
    center_derivatives = rational_derivatives(iv(center))
    center_residuals = residual_derivatives(iv(center), center_derivatives)
    saved_interval_contains_independent(
        saved["center_rational_z_interval_exact"], center_derivatives[0]
    )
    keys = (
        "center_residual_interval_exact",
        "center_first_residual_derivative_interval_exact",
        "center_second_residual_derivative_interval_exact",
        "center_third_residual_derivative_interval_exact",
    )
    for derivative in range(order):
        saved_interval_contains_independent(saved[keys[derivative]], center_residuals[derivative])
    independent_whole_derivative, subdomains, zrange = Fraction(0), [], []
    for part in range(PARTS):
        subleft, subright = (
            left + part * (right - left) / PARTS,
            left + (part + 1) * (right - left) / PARTS,
        )
        subcenter, subradius = (subleft + subright) / 2, (subright - subleft) / 2
        domain = interval(subleft, subright)
        derivatives = tighten(
            rational_derivatives(domain), rational_derivatives(iv(subcenter)), subradius, order
        )
        # The CDF residual itself is unnecessary for the whole interval bound;
        # chain-rule derivative order alone controls the Taylor remainder.
        residual = residual_derivatives(domain, derivatives)[order]
        derivative_bound = magnitude(residual)
        independent_whole_derivative = max(independent_whole_derivative, derivative_bound)
        zrange.append(bounds(derivatives[0]))
        subdomains.append(
            dict(
                part=part,
                q_domain_exact=list(map(pair, (subleft, subright))),
                independent_remainder_derivative_upper_exact=pair(derivative_bound),
            )
        )
    saved_upper_key = (
        "third_residual_derivative_absolute_upper_exact"
        if order == 3
        else "fourth_residual_derivative_absolute_upper_exact"
    )
    assert independent_whole_derivative <= exact(saved[saved_upper_key]), (
        index,
        order,
        "Independent whole-cell derivative bound exceeds saved enclosure",
    )
    saved_z_lower, saved_z_upper = map(exact, saved["rational_z_range_exact"])
    assert (
        saved_z_lower
        <= min(row[0] for row in zrange)
        <= max(row[1] for row in zrange)
        <= saved_z_upper
    )
    independent_residual = sum(
        (
            radius**degree * magnitude(center_residuals[degree]) / factorial(degree)
            for degree in range(order)
        ),
        Fraction(0),
    )
    independent_residual += radius**order * independent_whole_derivative / factorial(order)
    assert 8 * independent_residual <= exact(saved["real_quantile_error_upper_exact"])
    return dict(
        passed=True,
        cell_index=index,
        derivative_order=order,
        internal_fixed_subintervals=PARTS,
        independent_real_quantile_error_upper_exact=pair(8 * independent_residual),
        saved_real_quantile_error_upper_exact=saved["real_quantile_error_upper_exact"],
        saved_center_and_whole_derivative_enclosures_independently_verified=True,
        subdomains=subdomains,
    )


def audit_native(native):
    quantum, epsilon = NATIVE_Q, Fraction(1, NATIVE_Q)
    rounded_a, rounded_b = (
        tuple(round(coefficient * quantum) for coefficient in A),
        tuple(round(coefficient * quantum) for coefficient in B),
    )
    assert (
        list(rounded_a) == native["native_A_raw_ascending"]
        and list(rounded_b) == native["native_B_raw_ascending"]
    )
    assert min(rounded_a + rounded_b) > 0 and rounded_b[0] == quantum
    rconstant = (RMAX * quantum).__ceil__()
    assert native["rconstant_raw"] == rconstant
    argument_error = Fraction(rconstant, quantum) - RMAX + epsilon
    rupper = RMAX + argument_error
    assert exact(native["r_argument_error_upper_exact"]) == argument_error
    assert (
        native["r_native_lower_exact"] == [0, 1] and exact(native["r_native_upper_exact"]) == rupper
    )

    def polynomial_error(coefficients, rounded):
        coefficient_error = sum(
            (
                abs(Fraction(raw, quantum) - coefficient) * rupper**degree
                for degree, (coefficient, raw) in enumerate(zip(coefficients, rounded, strict=True))
            ),
            Fraction(0),
        )
        floor_error = epsilon * sum((rupper**degree for degree in range(7)), Fraction(0))
        derivative_error = argument_error * sum(
            (
                degree * coefficient * rupper ** (degree - 1)
                for degree, coefficient in enumerate(coefficients)
                if degree
            ),
            Fraction(0),
        )
        return coefficient_error + floor_error + derivative_error

    a_error, b_error = polynomial_error(A, rounded_a), polynomial_error(B, rounded_b)
    assert exact(native["numerator_polynomial_error_upper_exact"]) == a_error
    assert exact(native["denominator_polynomial_error_upper_exact"]) == b_error
    total = QMAX * a_error + epsilon + Fraction(3, 2) * b_error + epsilon
    assert exact(native["native_arithmetic_error_upper_exact"]) == total
    assert native["native_denominator_lower_exact"] == [1, 1]

    def partials(rounded):
        return [
            sum(
                (Fraction(rounded[k], quantum) * rupper ** (k - i) for k in range(i, 8)),
                Fraction(0),
            )
            for i in range(8)
        ]

    pa, pb = partials(rounded_a), partials(rounded_b)
    stored = max(*pa, *pb, QMAX * pa[0], QMAX, rupper, Fraction(1))
    product = (
        max(*(value * rupper for value in pa[1:] + pb[1:]), QMAX**2, QMAX * pa[0]) * quantum**2
    )
    dividend = QMAX * pa[0] * quantum**2
    assert exact(native["maximum_stored_fixed_point_value_upper_exact"]) == stored
    assert exact(native["maximum_full_product_raw_upper_exact"]) == product
    assert exact(native["maximum_shifted_division_numerator_raw_upper_exact"]) == dividend
    assert stored * quantum < 1 << 71 and product < 1 << 143 and dividend < 1 << 112
    assert (
        native["signed72_stored_values_no_overflow"]
        and native["signed144_full_multiply_products_no_overflow"]
    )
    assert (
        native["unsigned112_division_numerator_no_truncation"]
        and native["native_divider_clamp_inactive"]
    )
    assert native["new_central_approximation_law_not_prior_exact_floor_quantile_law"]
    assert (
        not native["actual_reversible_leaf_emitted_or_replayed"]
        and not native["division_gate_cost_charged"]
    )
    assert native["quantile_quantum_cost"] is None
    return dict(
        passed=True,
        native_error_upper_exact=pair(total),
        nooverflow_stored72_product144_dividend112=True,
        positive_denominator_at_least_one=True,
        exact_q32_midpoint_q_f40=True,
        signed_magnitude_restoration_preserves_absolute_error=True,
        negative_signed_restoration_is_not_exact_floor_quantile=True,
        actual_gate_interface_or_cost_validated=False,
    )


def xml_count(path):
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root)
    names = [
        (case.get("classname"), case.get("name"))
        for suite in suites
        for case in suite.findall("testcase")
    ]
    assert len(names) == len(set(names)) == sum(int(suite.get("tests", 0)) for suite in suites)
    assert all(
        int(suite.get(field, 0)) == 0
        for suite in suites
        for field in ("failures", "errors", "skipped")
    )
    return len(names)


def audit_version(name, order, output, started):
    directory = PROGRAM / name
    protocol, summary, certificate, inventory = (
        read(directory / filename)
        for filename in (
            "protocol.json",
            "summary.json",
            "central_certificate.json",
            "cell_bounds.json",
        )
    )
    assert summary["passed"] and not summary["budget_censored"]
    tests = xml_count(directory / "tests.xml")
    assert tests == summary["fixtures_passed"]
    if order == 3:
        assert tests == 27
    assert protocol["before_tests_or_fixed_cell_certificate_evaluation"]
    assert protocol["Taylor_jet_degree"] == order and protocol["fixed_equal_q_cells"] == 2048
    assert protocol["dyadic_outward_precision_bits"] == 128
    assert (
        protocol["CDF_integrated_Taylor_degree"] == 32
        and protocol["density_exponential_Taylor_degree"] == 40
    )
    assert tuple(map(Fraction, protocol["source_coefficients"]["A_decimals_ascending"])) == A
    assert tuple(map(Fraction, protocol["source_coefficients"]["B_decimals_ascending"])) == B
    assert certificate["source_coefficients"] == protocol["source_coefficients"]
    assert (
        inventory["fixed_cells"]
        == inventory["completed_cells"]
        == certificate["completed_fixed_cells"]
        == summary["completed_cells"]
        == 2048
    )
    cells = inventory["cells"]
    assert len(cells) == 2048
    keys = (
        "center_residual_interval_exact",
        "center_first_residual_derivative_interval_exact",
        "center_second_residual_derivative_interval_exact",
        "center_third_residual_derivative_interval_exact",
    )
    high_key = (
        "third_residual_derivative_absolute_upper_exact"
        if order == 3
        else "fourth_residual_derivative_absolute_upper_exact"
    )
    # Reconcile only recorded rational sums/tiling; no independent derivative
    # evaluation is done for the other 2044 saved cells.
    maximum, worst = Fraction(0), None
    for index, cell in enumerate(cells):
        assert cell["cell_index"] == index
        left, right = -QMAX + index * (2 * QMAX / 2048), -QMAX + (index + 1) * (2 * QMAX / 2048)
        assert cell["q_domain_exact"] == list(map(pair, (left, right)))
        radius = (right - left) / 2
        saved_sum = sum(
            (
                radius**degree * max(map(abs, map(exact, cell[keys[degree]]))) / factorial(degree)
                for degree in range(order)
            ),
            Fraction(0),
        )
        saved_sum += radius**order * exact(cell[high_key]) / factorial(order)
        assert exact(cell["CDF_residual_absolute_upper_exact"]) == saved_sum
        real = exact(cell["real_quantile_error_upper_exact"])
        assert real == 8 * saved_sum
        if real > maximum:
            maximum, worst = real, index
        zlower, zupper = map(exact, cell["rational_z_range_exact"])
        assert -Fraction(3, 2) <= zlower <= zupper <= Fraction(3, 2)
    assert exact(certificate["real_approximation_error_upper_exact"]) == maximum
    native_audit = audit_native(certificate["native_arithmetic"])
    total = maximum + exact(native_audit["native_error_upper_exact"])
    assert (
        exact(certificate["total_central_quantile_error_upper_exact"])
        == exact(summary["total_central_quantile_error_upper_exact"])
        == total
    )
    assert exact(certificate["required_uniform_quantile_error_exact"]) == TARGET
    assert certificate["certified"] == summary["central_certificate_succeeded"] == (total <= TARGET)
    if order == 3:
        assert not certificate["certified"] and total > TARGET
        assert (
            certificate["reason"]
            == summary["failure_reason"]
            == "fixed_method_error_bound_exceeds_target"
        )
    reports = []
    for index in SELECTED:
        assert time.process_time() - started < 180
        reports.append(audit_saved_cell(cells[index], order))
    assert (
        not certificate["ordinary_and_extreme_tails_certified"]
        and not certificate["coherent_loader_implemented"]
    )
    assert (
        not certificate["native_financial_path_arithmetic_certified"]
        and not certificate["full_G2_closed"]
    )
    assert not certificate["accepted_Box_Muller_baseline_changed"]
    assert certificate["actual_reversible_leaf_or_division_gate_cost"] is None
    assert summary["new_original_financial_prices_or_gates"] == 0
    save(
        output / (name + "_audit.json"),
        dict(
            passed=True,
            producer_receipt=name,
            producer_tests_passed=tests,
            saved_cell_metadata_rows_reconciled=2048,
            independent_saved_cells_recomputed=len(reports),
            selected_cell_reports=reports,
            actual_independent_quantile_grid_reruns=0,
            recorded_worst_cell=worst,
            native_interface_mathematical_audit=native_audit,
            saved_real_approximation_error_upper_exact=pair(maximum),
            saved_total_central_error_upper_exact=pair(total),
            central_target_certificate_succeeded=certificate["certified"],
            failed_enclosure_is_not_error_lower_bound=True,
            new_approximation_law_not_accepted_finite_Box_Muller=True,
            tails_gate_interface_cost_and_full_price_open=True,
        ),
    )
    print(
        name,
        "bounded cell/native/ledger audit PASS; central target",
        certificate["certified"],
        flush=True,
    )
    return dict(
        name=name,
        tests=tests,
        selected_cells=len(reports),
        central_certificate_succeeded=certificate["certified"],
        total_error=pair(total),
    )


def prepare(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM)
    assert not output.exists()
    frozen = {}
    for name, _ in VERSIONS:
        directory = PROGRAM / name
        assert read(directory / "summary.json")["passed"]
        manifest = read(directory / "manifest.json")
        frozen.update(manifest["files"])
        frozen.update(manifest["frozen_inputs"])
        frozen[relative(directory / "manifest.json")] = sha(directory / "manifest.json")
    own = Path(__file__).resolve()
    frozen[relative(own)] = sha(own)
    verify(frozen)
    output.mkdir()
    shutil.copy2(own, output / "executed_audit_quantile_central.py")
    save(
        output / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            local_only=True,
            before_independent_recomputation=True,
            frozen_inputs=frozen,
            interpreter_sha256=sha(sys.executable),
            versions=[dict(name=name, derivative_order=order) for name, order in VERSIONS],
            selected_saved_cell_indices=list(SELECTED),
            maximum_selected_saved_cells_per_version=8,
            fixed_internal_subintervals_per_selected_cell=PARTS,
            independent_interval_decimal_precision=140,
            independent_pi="240-term rational alternating atan(1/2)+atan(1/3)",
            independent_CDF_expansion_degree=72,
            independent_density_method="mpmath interval exp",
            independent_rational_derivative_method="Explicit polynomial r derivatives and chain rule through order four; quotient differentiated from P=zD with binomial coefficients",
            process_CPU_limit_seconds=180,
            full_partition_derivative_recomputations=0,
            old_fixture_success_and_failed_enclosure_both_preserved=True,
            new_result_adopted_only_at_declared_central_scope=True,
            new_native_gates=0,
            new_financial_paths_or_prices=0,
            tail_or_loader_adoption=False,
        ),
    )
    print("Bounded two-version central audit frozen", flush=True)


def run(output):
    global PI, A, B
    started = time.process_time()
    output = Path(output).resolve()
    assert not (output / "summary.json").exists()
    protocol = read(output / "protocol.json")
    verify(protocol["frozen_inputs"])
    assert sha(sys.executable) == protocol["interpreter_sha256"]
    mp.iv.dps = 140
    PI = independent_pi()
    source = PROGRAM / "A02_quantile_census_run001/primary_sources/R_qnorm.c"
    A, B = published_coefficients(source)
    assert len(A) == len(B) == 8 and min(A + B) > 0 and B[0] == 1
    negative, positive = gaussian_cdf(iv(Fraction(-3, 2))), gaussian_cdf(iv(Fraction(3, 2)))
    assert bounds(negative)[1] < Fraction(3, 40) and bounds(positive)[0] > Fraction(37, 40)
    density_lower = bounds(mp.iv.exp(iv(Fraction(-9, 8))) / mp.iv.sqrt(2 * PI))[0]
    assert density_lower > Fraction(1, 8)
    versions = [audit_version(name, order, output, started) for name, order in VERSIONS]
    native_functions = (
        "nearest_integer",
        "rounded_coefficients",
        "rconstant_raw",
        "_horner_error",
        "_derivative_bound",
        "_horner_value_bounds",
        "native_rounding_certificate",
        "mathematical_native_central_word",
    )
    native_bodies = []
    for version, suffix in ((VERSIONS[0][0], ""), (VERSIONS[1][0], "_v2")):
        tree = ast.parse(
            (PROGRAM / version / ("quantile_central_certificate" + suffix + ".py")).read_text(
                encoding="utf-8"
            )
        )
        native_bodies.append(
            {
                node.name: ast.dump(node, include_attributes=False)
                for node in tree.body
                if isinstance(node, ast.FunctionDef) and node.name in native_functions
            }
        )
    assert set(native_bodies[0]) == set(native_bodies[1]) == set(native_functions)
    assert native_bodies[0] == native_bodies[1]
    assert (
        read(PROGRAM / VERSIONS[0][0] / "central_certificate.json")["native_arithmetic"]
        == read(PROGRAM / VERSIONS[1][0] / "central_certificate.json")["native_arithmetic"]
    )
    verify(protocol["frozen_inputs"])
    assert time.process_time() - started < 180
    save(
        output / "summary.json",
        dict(
            passed=True,
            local_only=True,
            versions=versions,
            independent_saved_cell_recomputations=8,
            actual_full_2048_cell_reruns=0,
            recorded_ledger_rows_reconciled=4096,
            chain_rule_g3_g4_and_centered_remainders_valid=True,
            native_law_and_published_coefficients_unchanged_across_versions=True,
            native72_f40_product144_dividend112_mathematical_bounds_verified=True,
            first_version_27_fixture_PASS_and_central_target_FAIL_preserved=True,
            enclosure_failure_is_not_approximation_impossibility=True,
            central_only_new_native_approximation_law=True,
            prior_exact_floor_quantile_law_replaced=False,
            actual_gate_interface_divider_cost_and_cleanup_certified=False,
            ordinary_or_extreme_tails_certified=False,
            accepted_Box_Muller_source_changed=False,
            new_native_gates=0,
            new_financial_paths_or_prices=0,
            tail_loader_or_full_price_adoption=False,
            elapsed_process_CPU_seconds=time.process_time() - started,
            full_G2_closed=False,
            quantum_advantage_claim=False,
        ),
    )
    finish_manifest(output)
    print("Independent bounded central certificate audit PASS", flush=True)


def finish_manifest(output):
    save(
        output / "manifest.json",
        dict(
            files={relative(path): sha(path) for path in output.rglob("*") if path.is_file()},
            frozen_inputs=read(output / "protocol.json")["frozen_inputs"],
            manifest_self_hash_excluded=True,
        ),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.phase == "prepare":
        prepare(args.output)
    else:
        try:
            run(args.output)
        except Exception as failure:
            output = args.output.resolve()
            (output / "failure.txt").write_text(traceback.format_exc(), encoding="utf-8")
            save(
                output / "summary.json",
                dict(
                    passed=False,
                    local_only=True,
                    failure_type=type(failure).__name__,
                    message=str(failure),
                    new_native_gates=0,
                    new_financial_paths_or_prices=0,
                    full_G2_closed=False,
                ),
            )
            finish_manifest(output)
            raise
