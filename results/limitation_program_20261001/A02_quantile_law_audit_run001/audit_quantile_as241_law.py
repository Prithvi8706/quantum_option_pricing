"""Independent exact audit of the NEW AS241 scalar-law transfer.

No producer derivations are imported. The successful independent transform
audit supplies analytic interval provenance; this audit separately recomposes
every saved log class and fresh rational-error row and proves the KS/BV step.
There are no new tests, quantum gates, prices or financial path evaluations.
"""

from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import shutil
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
RESEARCH = ROOT / "research/limitation_program_20261001"
BUILDER = ROOT / "research/advantage_frontier_20260923/barrier_oracle_depth.py"
TRANSFORM = PROGRAM / "A02_quantile_transform_run002"
TRANSFORM_AUDIT = PROGRAM / "A02_quantile_transform_audit_run001"
LAW = PROGRAM / "A02_quantile_law_run001"
GRID_AUDIT = PROGRAM / "C06_quantile_grid_audit_run001"
PAIR = PROGRAM / "C06_pair_run001"
TAIL = PROGRAM / "A02_quantile_tail_run001"
CENTRAL = PROGRAM / "A02_quantile_central_run002"
CASES = {"B4x12": (4, 12), "B8x52": (8, 52)}
S = 1 << 40
ULP = Fraction(1, S)
ERROR_TARGET = Fraction(1, 10**8)
RMAX = Fraction(321, 100)
ALLOWANCE = Fraction(1, 1000)
CPU_LIMIT = 90
ADMISSION_CPU = 75
WALL_LIMIT = 300
CODE = ("audit_quantile_as241_law.py", "quantile_as241_law_audit_preflight.json")
PARAMETERS = ("SIGMA", "CORR", "S0", "RATE", "T", "K", "H")
EXPECTED = tuple(map(Fraction, (".3", ".4", "100", ".03", "1", "100", "140")))
THEOREM = {
    "same_midpoint_coupling": (
        "At every raw word k, X=Phi_inverse((k+1/2)/2^32), |Z-X|<=E. "
        "Therefore {X<=x-E} subset {Z<=x} subset {X<=x+E}; no ordering or "
        "distinctness of the Z values is used."
    ),
    "midpoint_KS": (
        "Counting midpoints below Phi(x) differs from Phi(x) by at most1/(2N), "
        "including exact midpoint ties. Since Phi is continuous, the same bound "
        "holds for left CDF limits."
    ),
    "density": (
        "Alternating Machin sums give pi>16*(1/5-1/(3*5^3))-4/239>25/8. "
        "Thus phi(x)<=1/sqrt(2*pi)<2/5; a displacement E adds at most(2/5)E."
    ),
    "coordinate_BV": (
        "Every affected ideal GBM stock has a positive coefficient for a common "
        "or idiosyncratic increment. With other finite coordinates fixed, all "
        "affected baskets and the Asian average are nondecreasing. Strict "
        "barrier survival is a lower half-line, empty or full. On survival the "
        "Asian average<140, so the already-discounted positive payoff<40; "
        "an increase of at most40 followed by a downward knockout jump of "
        "at most40 gives total variation<=80. The strict endpoint value is zero."
    ),
    "atom_aware_integration": (
        "For the right-continuous BV coordinate payoff, integrate its signed "
        "Stieltjes measure against half-line probabilities. Closed lower "
        "half-lines use F(x), closed upper ones use1-F(x-); left CDF limits are "
        "controlled too. Thus the expectation discrepancy is at mostTV*KS, "
        "including discrete atoms at the knockout endpoint."
    ),
    "independent_product": (
        "Replace d independent scalar coordinates one at a time. The uniform "
        "BV bound holds for every mixture of discrete and continuous other "
        "coordinates. Bounded payoff permits iterated integration; triangle "
        "inequality gives80*d*(2^-33+(2/5)E). No second discount is applied."
    ),
    "scope": (
        "This is the independent NEW AS241 law versus the original continuous "
        "ideal GBM. E already includes native scalar log/root/Horner/division "
        "error once. No old hypothetical transform-floor ULP, Box-Muller joint "
        "law, native financial exp/clipping/path error, coherent compiler cost "
        "or complete original price certificate is adopted."
    ),
}


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


def q(value):
    if type(value) is int or isinstance(value, Fraction):
        return Fraction(value)
    if (
        isinstance(value, (tuple, list))
        and len(value) == 2
        and (all(type(item) is int for item in value) and value[1] > 0)
    ):
        return Fraction(*value)
    raise ValueError("Exact integer/Fraction or rational pair required")


def pair(value):
    value = q(value)
    return [value.numerator, value.denominator]


def verify(frozen):
    for name, expected in frozen.items():
        path = (ROOT / name).resolve()
        path.relative_to(ROOT)
        if sha(path) != expected:
            raise ValueError("Frozen AS241-law audit bytes differ: " + name)


def expect_pair(actual, expected, label):
    if q(actual) != expected:
        raise ValueError("Independent exact reconciliation failed: " + label)


def nearest(value):
    value = q(value)
    lower = value.numerator // value.denominator
    residual = value - lower
    return lower + int(residual > Fraction(1, 2) or (residual == Fraction(1, 2) and lower % 2))


def _interval(value):
    lo, hi = map(q, value)
    if lo > hi:
        raise ValueError("Ordered audited analytic endpoints required")
    return lo, hi


def audit_transform_classes(native, table, ln2, checkpoint):
    for flag in (
        "actual_q32_native_transform_error_included",
        "exact_transform_hypothesis_replaced_by_mathematical_native_arithmetic",
    ):
        if native.get(flag) is not True:
            raise ValueError("The actual all-input native scalar arithmetic premise is absent")
    for flag in (
        "native_financial_path_arithmetic_certified",
        "coherent_loader_implemented_or_adopted",
        "accepted_Box_Muller_baseline_changed",
        "full_G2_closed",
    ):
        if native.get(flag) is not False:
            raise ValueError(
                "An old financial-law or coherent implementation claim was transferred"
            )
    if native.get("actual_coherent_leaf_or_quantum_gate_cost") is not None:
        raise ValueError("Mathematical scalar error cannot supply coherent gate resources")
    transform = native["transform"]
    normalization = transform["normalization"]
    if (normalization["msb_index_range"], normalization["log_exponent_range"]) != (
        [7, 36],
        [-33, -4],
    ) or normalization["mantissa_raw_bounds"] != [S, 2 * S - (1 << 11)]:
        raise ValueError("Exact odd128 midpoint/left-shift normalization range differs")
    for flag in (
        "all_q32_tail_words_covered",
        "normalization_only_left_shifts",
        "native_input_guard_raw_one_inactive",
        "interpolation_clips_inactive",
    ):
        if normalization.get(flag) is not True:
            raise ValueError("Required all-input normalization guard is missing")
    for name in (
        "normalization_roundoff_exact",
        "exponent_times_ln2_floor_error_exact",
        "negative_log_negation_error_exact",
    ):
        expect_pair(normalization[name], Fraction(0), name)
    if normalization["enumerated_q32_words_as_completeness_proof"] != 0:
        raise ValueError("Samples cannot establish q32 completeness")
    if not Fraction(3, 40) * S < 1 << 37 or transform["original_ln2_raw"] != ln2:
        raise ValueError("The actual tail domain or ln2 literal differs")
    radius = Fraction(1, 64)
    remainder = radius**9 / 9
    floors = ULP * sum((radius**degree for degree in range(8)), Fraction(0))
    rows = transform["log_table_cells"]
    if len(rows) != 32 or [row["table_cell"] for row in rows] != list(range(32)):
        raise ValueError("All32 archived log cells are required")
    errors, max_value, max_product = [], Fraction(0), Fraction(0)
    for index, (raws, row) in enumerate(zip(table, rows, strict=True)):
        checkpoint()
        center = 1 + Fraction(2 * index + 1, 64)
        expect_pair(row["center_exact"], center, "table center")
        expect_pair(row["radius_exact"], radius, "table radius")
        if len(raws) != 9 or len(row["coefficient_checks"]) != 9:
            raise ValueError("All nine degree8 raw coefficients are required")
        coefficients = []
        for degree, (raw, check) in enumerate(zip(raws, row["coefficient_checks"], strict=True)):
            if type(raw) is not int or (check["degree"], check["literal_raw"]) != (degree, raw):
                raise ValueError("Audited literal coefficient identity differs")
            endpoints = _interval(check["true_coefficient_interval_exact"])
            if (
                degree
                and endpoints != (Fraction((-1) ** (degree - 1), degree) / center**degree,) * 2
            ):
                raise ValueError("Independent exact logarithm derivative coefficient differs")
            coefficient_error = max(abs(Fraction(raw, S) - endpoint) for endpoint in endpoints)
            if coefficient_error > ULP / 2:
                raise ValueError("Original nearest-f40 coefficient enclosure failed")
            expect_pair(
                check["coefficient_error_upper_exact"], coefficient_error, "coefficient error"
            )
            coefficients.append(coefficient_error)
        coefficient_sum = sum(
            (error * radius**degree for degree, error in enumerate(coefficients)), Fraction(0)
        )
        expect_pair(row["coefficient_error_upper_exact"], coefficient_sum, "weighted coefficients")
        expect_pair(row["Taylor_remainder_upper_exact"], remainder, "log Taylor remainder")
        expect_pair(row["Horner_floor_error_upper_exact"], floors, "eight signed Horner floors")
        error = coefficient_sum + remainder + floors
        expect_pair(row["table_error_upper_exact"], error, "complete log table error")
        errors.append(error)
        value = abs(Fraction(raws[-1], S))
        max_value = max(max_value, value)
        for raw in reversed(raws[:-1]):
            max_product = max(max_product, value * radius)
            after = value * radius + ULP
            value = after + abs(Fraction(raw, S))
            max_value = max(max_value, value, after)
    ln2_interval = _interval(transform["ln2_interval_exact"])
    ln2_error = max(abs(Fraction(ln2, S) - endpoint) for endpoint in ln2_interval)
    if ln2_error > ULP / 2 or not 33 * ln2_interval[1] < Fraction(231, 10):
        raise ValueError("Audited ln2 nearest-rounding/radicand margin differs")
    expect_pair(transform["ln2_literal_error_upper_exact"], ln2_error, "ln2 rounding")
    cover = transform["cell_exponent_cover"]
    expected_classes = [(cell, exponent) for cell in range(32) for exponent in range(-33, -3)]
    if [(row["table_cell"], row["exponent"]) for row in cover] != expected_classes:
        raise ValueError("All960 ordered table/exponent classes are required exactly once")
    log_errors = []
    for row in cover:
        checkpoint()
        expected = errors[row["table_cell"]] + abs(row["exponent"]) * ln2_error
        expect_pair(row["native_log_error_upper_exact"], expected, "log exponent class")
        log_errors.append(expected)
    error = max(log_errors)
    expect_pair(transform["native_log_error_upper_exact"], error, "global log error")
    shift = Fraction(8, 5)
    shift_raw = nearest(shift * S)
    shift_error = abs(Fraction(shift_raw, S) - shift)
    rho = Fraction(5, 16) * error + ULP + shift_error
    if transform["nearest_shift_raw"] != shift_raw:
        raise ValueError("Nearest-f40 eight-fifths shift differs")
    expect_pair(transform["nearest_shift_error_exact"], shift_error, "shift rounding")
    expect_pair(transform["sqrt_floor_error_upper_exact"], ULP, "one actual sqrt floor")
    expect_pair(
        transform["sqrt_sensitivity_error_upper_exact"], Fraction(5, 16) * error, "sqrt sensitivity"
    )
    expect_pair(transform["native_transform_error_upper_exact"], rho, "actual transform rho")
    lower, upper = Fraction(259, 100) - error, Fraction(231, 10) + error
    if _interval(transform["true_negative_log_lower_interval_exact"])[0] <= Fraction(259, 100):
        raise ValueError("The hash-bound analytic negative-log lower margin is absent")
    if not (
        lower > Fraction(1609, 1000) ** 2
        and lower > shift**2
        and upper < Fraction(4807, 1000) ** 2
        and upper < 24
    ):
        raise ValueError("The away-from-zero native sqrt and transform ranges are invalid")
    expect_pair(transform["native_negative_log_lower_exact"], lower, "native radicand lower")
    expect_pair(transform["native_negative_log_upper_exact"], upper, "native radicand upper")
    if transform["actual_native_r_range_exact"] != [
        pair(Fraction(9, 1000) - ULP - shift_error),
        pair(Fraction(3207, 1000) + shift_error),
    ]:
        raise ValueError("The actual native transform range differs")
    stored = max(
        max_value + 33 * abs(Fraction(ln2, S)), Fraction(33), Fraction(24), Fraction(4807, 1000)
    )
    product = max(max_product, 33 * abs(Fraction(ln2, S))) * (1 << 80)
    expect_pair(transform["maximum_stored_value_upper_exact"], stored, "stored transform bound")
    expect_pair(
        transform["maximum_full_product_raw_upper_exact"], product, "wide transform product"
    )
    if stored * S >= 1 << 71 or product >= 1 << 143:
        raise ValueError("Native signed72/signed144 overflow bound failed")
    if transform["continuous_uniform_midpoint_coupling_error_included"] is not False or (
        transform["radial_cutoff_or_bad_event_used"] is not False
    ):
        raise ValueError("Old Box-Muller midpoint/cutoff terms cannot enter this scalar E")
    return rho


def audit_fresh_rows(native, fresh, tail, cells, central, rho, checkpoint):
    a, b = (
        tuple(map(Fraction, tail["source_coefficients"][name]))
        for name in ("A_decimals_ascending", "B_decimals_ascending")
    )
    raw_a, raw_b = (tuple(nearest(value * S) for value in coefficients) for coefficients in (a, b))
    if list(raw_a) != tail["native_interface"]["native_A_raw_ascending"] or (
        list(raw_b) != tail["native_interface"]["native_B_raw_ascending"]
    ):
        raise ValueError("The original positive rational coefficient literals differ")
    if min(b) <= 0 or min(raw_b) <= 0 or raw_b[0] != S:
        raise ValueError("Positive native denominator coefficients are required")
    rows = fresh["rows"]
    if (
        fresh["fixed_rows"] != 1024
        or fresh["completed_rows"] != 1024
        or (len(rows) != 1024 or len(cells) != 1024)
    ):
        raise ValueError("All1024 original and fresh ordinary-tail cells are required")

    def horner_error(coefficients, raws, upper):
        coefficient_errors = tuple(
            abs(Fraction(raw, S) - exact) for raw, exact in zip(raws, coefficients, strict=True)
        )
        return sum(
            (value * upper**degree for degree, value in enumerate(coefficient_errors)), Fraction(0)
        ) + ULP * sum((upper**degree for degree in range(len(coefficients) - 1)), Fraction(0))

    def derivative(coefficients, upper):
        return sum(
            (
                degree * coefficient * upper ** (degree - 1)
                for degree, coefficient in enumerate(coefficients)
                if degree
            ),
            Fraction(0),
        )

    errors = []
    for index, (cell, row) in enumerate(zip(cells, rows, strict=True)):
        checkpoint()
        if cell["cell_index"] != index or row["cell_index"] != index:
            raise ValueError("Fresh tail cell ordering or membership differs")
        lower, upper = map(q, cell["r_domain_exact"])
        if (lower, upper) != (RMAX * index / 1024, RMAX * (index + 1) / 1024):
            raise ValueError("The unchanged1024-cell real-error domain partition differs")
        left, right = max(Fraction(0), lower - rho), min(RMAX, upper + rho)
        lower_raw = (left * S).numerator // (left * S).denominator
        denominator_raw = raw_b[-1]
        for coefficient in reversed(raw_b[:-1]):
            denominator_raw = (denominator_raw * lower_raw) // S + coefficient
        denominator = Fraction(denominator_raw, S)
        numerator_error = horner_error(a, raw_a, right) + rho * derivative(a, right)
        denominator_error = horner_error(b, raw_b, right) + rho * derivative(b, right)
        arithmetic = (numerator_error + Fraction(13, 2) * denominator_error) / denominator + ULP
        real = q(cell["real_quantile_error_upper_exact"])
        expected = {
            "argument_perturbation_upper_exact": rho,
            "native_denominator_lower_exact": denominator,
            "numerator_coefficient_Horner_and_input_error_upper_exact": numerator_error,
            "denominator_coefficient_Horner_and_input_error_upper_exact": denominator_error,
            "fresh_native_rational_error_upper_exact": arithmetic,
            "saved_real_approximation_error_upper_exact": real,
            "actual_native_tail_quantile_error_upper_exact": real + arithmetic,
        }
        if (
            denominator < 1
            or real < 0
            or row["extended_r_domain_exact"] != [pair(left), pair(right)]
        ):
            raise ValueError("Fresh tail denominator/domain or saved real-error proof differs")
        for name, value in expected.items():
            expect_pair(row[name], value, "fresh tail row" + str(index) + "/" + name)
        if row["previous_conditional_floor_arithmetic_error_added"] is not False or (
            row["actual_sqrt_floor_and_shift_error_only_in_rho"] is not True
        ):
            raise ValueError("The old hypothetical floor error was charged again or rho omitted")
        errors.append(real + arithmetic)
    tail_error = max(errors)
    central_error = q(central["total_central_quantile_error_upper_exact"])
    error = max(tail_error, central_error)
    expect_pair(native["actual_native_tail_quantile_error_upper_exact"], tail_error, "tail maximum")
    expect_pair(
        native["central_quantile_error_upper_exact"], central_error, "accepted central maximum"
    )
    expect_pair(
        native["combined_mathematical_native_quantile_error_upper_exact"],
        error,
        "global native maximum",
    )
    expect_pair(
        native["required_uniform_quantile_error_exact"], ERROR_TARGET, "fixed quantile target"
    )
    if central_error < 0 or error > ERROR_TARGET:
        raise ValueError("The all-input native scalar bound fails its fixed target")
    return error


def audit_original_model(case, row):
    module = ast.parse(BUILDER.read_text(encoding="utf-8"))
    economic = []
    for node in module.body:
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Tuple)
        ):
            if tuple(ast.unparse(part) for part in node.targets[0].elts) == PARAMETERS:
                economic.append(
                    tuple(Fraction(str(value)) for value in ast.literal_eval(node.value))
                )
    if economic != [EXPECTED]:
        raise ValueError("The original continuous economic constants differ")
    build = [
        node for node in module.body if isinstance(node, ast.FunctionDef) and node.name == "build"
    ]
    if len(build) != 1:
        raise ValueError("One original financial builder is required")
    expected_assignments = {
        "count": "nt * (na + 1)",
        "dt": "T / nt",
        "common": "g.cmul(zs[j * (na + 1)], SIGMA * math.sqrt(dt * CORR))",
        "idio": "g.cmul(zs[j * (na + 1) + 1 + i], SIGMA * math.sqrt(dt * (1 - CORR)))",
        "baskets": (
            "[g.cmul(tree(g, [stocks[i][j] for i in range(na)], g.add), 1 / na) for j in range(nt)]"
        ),
        "steps[0]": "g.add(steps[0], g.c(math.log(S0)))",
        "steps": "[steps[j] if j < d else g.add(steps[j], steps[j - d]) for j in range(nt)]",
        "alive": "g.lt(tree(g, baskets, g.maximum), g.c(H))",
        "average": "g.cmul(tree(g, [s for row in stocks for s in row], g.add), 1 / (na * nt))",
        "payoff": "g.cmul(g.pos(g.sub(average, g.c(K))), math.exp(-RATE * T))",
        "g.outputs": "dict(Y=g.select(alive, payoff, g.c(0)))",
    }
    nodes = list(ast.walk(build[0]))
    for target, expression in expected_assignments.items():
        expected = ast.dump(ast.parse(expression, mode="eval").body, include_attributes=False)
        count = sum(
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and (
                ast.unparse(node.targets[0]) == target
                and ast.dump(node.value, include_attributes=False) == expected
            )
            for node in nodes
        )
        if count != 1:
            raise ValueError("The original positive-coefficient/strict-knockout template differs")
    drift = ast.dump(
        ast.parse(
            "steps.append(g.add(g.add(common, idio), g.c((RATE - .5 * SIGMA ** 2) * dt)))",
            mode="eval",
        ).body,
        include_attributes=False,
    )
    if (
        sum(
            isinstance(node, ast.Call) and ast.dump(node, include_attributes=False) == drift
            for node in nodes
        )
        != 1
    ):
        raise ValueError("The original common/idiosyncratic drift increment differs")
    assets, dates = CASES[case]
    task = read(PROGRAM / "G0_run003" / (case + "_task.json"))
    names = (
        "annual_volatility_each_asset",
        "equicorrelation",
        "spot_each_asset_dollars",
        "annual_rate",
        "maturity_years",
        "strike_dollars",
        "barrier_dollars",
    )
    if (task["assets"], task["dates"]) != (assets, dates) or (
        tuple(Fraction(str(task[name])) for name in names) != EXPECTED
        or task["barrier_equality"] != "basket >= H is knocked out; alive uses strict < H"
        or len(task["observation_times"]) != dates
        or task["payoff"]
        != (
            "exp(-r*T) * max(mean over all asset/date spots - K, 0) * "
            "indicator(max over monitored dates of equal-weight spot basket < H)"
        )
        or task["continuous_sampling"]
        != (
            "Independent common/idiosyncratic standard normals give exact GBM log "
            "increments at each contractual date before numerical representation."
        )
    ):
        raise ValueError("The original task dimensions, parameters or strict endpoint differs")
    model = row["original_model_binding"]
    model_names = (
        "volatility_exact",
        "correlation_exact",
        "spot_dollars_exact",
        "rate_exact",
        "maturity_years_exact",
        "strike_dollars_exact",
        "barrier_dollars_exact",
    )
    if (model["case"], model["assets"], model["dates"], model["builder_sha256"]) != (
        case,
        assets,
        dates,
        sha(BUILDER),
    ) or tuple(q(model[name]) for name in model_names) != EXPECTED:
        raise ValueError("Saved original model/hash binding differs")
    if model["equal_asset_volatility"] is not True or (
        model["basket"] != "positive equal-weight arithmetic spot basket"
        or model["continuous_driver_law"] != "independent common and idiosyncratic Brownian drivers"
        or model["digital_paired_outputs_claimed_independent_gaussian"] is not False
    ):
        raise ValueError("The independent continuous ideal GBM assumptions differ")
    dt = EXPECTED[4] / dates
    if min(EXPECTED[0] ** 2 * dt * EXPECTED[1], EXPECTED[0] ** 2 * dt * (1 - EXPECTED[1])) <= 0:
        raise ValueError("Positive common/idiosyncratic stock coefficients are required")
    return (assets + 1) * dates


def audit_law_row(case, row, error):
    dimension = audit_original_model(case, row)
    density_pi = 16 * (Fraction(1, 5) - Fraction(1, 3 * 5**3)) - Fraction(4, 239)
    if not density_pi > Fraction(25, 8) or EXPECTED[-1] - EXPECTED[-2] != 40 or EXPECTED[3] <= 0:
        raise ValueError("The independent density/discounted payoff cap proof failed")
    midpoint, displacement = Fraction(1, 1 << 33), Fraction(2, 5) * error
    ks = midpoint + displacement
    dollars = 80 * dimension * ks
    fields = {
        "uniform_quantile_error_upper_exact": error,
        "grid_KS_error_upper_exact": midpoint,
        "quantile_displacement_KS_error_upper_exact": displacement,
        "scalar_Gaussian_KS_error_upper_exact": ks,
        "coordinate_total_variation_upper_dollars_exact": Fraction(80),
        "ideal_GBM_new_law_price_bias_upper_dollars_exact": dollars,
        "separate_exploratory_law_allowance_dollars_exact": ALLOWANCE,
    }
    for name, value in fields.items():
        expect_pair(row[name], value, case + "/" + name)
    if (
        row["case"],
        row["uniform_bits"],
        row["fraction_bits"],
        row["native_width"],
        row["normal_coordinates"],
    ) != (case, 32, 40, 72, dimension) or row[
        "new_law"
    ] != "independent q32 midpoint inputs, mathematical-native signed-restored AS241":
        raise ValueError("The NEW scalar law/word interface/dimension differs")
    for name in (
        "new_law_monotonicity_required",
        "previous_exact_floor_quantile_law_ULP_added",
        "accepted_Box_Muller_law_certified",
        "accepted_Box_Muller_baseline_changed",
        "native_financial_exp_clipping_or_path_certified",
        "coherent_divider_or_loader_adopted",
        "complete_original_price_certified",
        "full_G2_closed",
        "quantum_advantage_established",
        "second_discount_applied",
    ):
        if row[name] is not False:
            raise ValueError("A forbidden scalar-law transfer/adoption claim is present")
    for name in (
        "quantile_native_scalar_arithmetic_already_in_E",
        "independent_raw_uniform_coordinates_required",
        "original_continuous_ideal_GBM_payoff_used",
        "proof_premise_bound_to_successful_all_input_certificate",
    ):
        if row[name] is not True:
            raise ValueError("A required separate-law premise is absent")
    if (
        row["actual_quantum_gate_cost"] is not None
        or row["native_financial_price_error_bound"] is not None
    ):
        raise ValueError("Scalar-law bounds cannot fill native cost or financial bias fields")
    if row["new_law_bias_fits_separate_exploratory_allowance"] is not (dollars <= ALLOWANCE):
        raise ValueError("The separate allowance comparison differs")
    density = row["Gaussian_density_proof"]
    expect_pair(density["Machin_alternating_lower_bound_exact"], density_pi, "Machin density bound")
    expect_pair(density["pi_strict_lower_guard_exact"], Fraction(25, 8), "pi density guard")
    expect_pair(density["Gaussian_density_strict_upper_exact"], Fraction(2, 5), "density upper")
    return {
        "case": case,
        "normal_coordinates": dimension,
        "independent_scalar_KS_upper_exact": pair(ks),
        "independent_ideal_GBM_price_bias_upper_exact": pair(dollars),
        "fits_separate_exploratory_law_allowance": dollars <= ALLOWANCE,
        "native_financial_error_or_complete_price_claim_adopted": False,
    }


def prepare(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM)
    if output.exists():
        raise FileExistsError("Fresh independent AS241-law audit receipt required")
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
                    new_financial_samples_or_gate_evaluations=0,
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

    def bind(name, expected):
        path = (ROOT / str(name).replace("\\", "/")).resolve()
        path.relative_to(ROOT)
        normalized = relative(path)
        if (
            not isinstance(expected, str)
            or len(expected) != 64
            or any(char not in "0123456789abcdef" for char in expected)
        ):
            raise ValueError("Explicit canonical SHA256 dependency expected")
        if normalized in frozen and frozen[normalized] != expected:
            raise ValueError("Independent audit prerequisite hashes disagree")
        frozen[normalized] = expected

    for directory in (TRANSFORM, TRANSFORM_AUDIT, LAW, GRID_AUDIT):
        summary = read(directory / "summary.json")
        if summary.get("passed") is not True or summary.get("budget_censored", False) is not False:
            raise ValueError(
                "Successful transform, transform audit, law and model audit are required"
            )
        if directory in (TRANSFORM, LAW) and summary.get("budget_censored") is not False:
            raise ValueError("Uncensored transform and law premises are required")
        receipt = read(directory / "manifest.json")
        for field in ("files", "frozen_inputs"):
            for name, expected in receipt[field].items():
                bind(name, expected)
        bind(relative(directory / "manifest.json"), sha(directory / "manifest.json"))
    for path in (
        [RESEARCH / name for name in CODE]
        + [BUILDER]
        + [PROGRAM / "G0_run003" / (case + "_task.json") for case in CASES]
        + [Path(sys.executable)]
    ):
        bind(relative(path), sha(path))
    verify(frozen)
    output.mkdir()
    for name in CODE:
        shutil.copy2(RESEARCH / name, output / name)
        if sha(output / name) != frozen[relative(RESEARCH / name)]:
            raise ValueError("Frozen independent-law code snapshot differs: " + name)
    create(
        output / "protocol.json",
        {
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "local_only": True,
            "before_ledger_class_reconstruction_or_law_arithmetic": True,
            "requires_all_stage_c_script_supervisors_and_exclusive_descendants_terminal": True,
            "frozen_inputs": frozen,
            "executed_dependencies": [
                {
                    "original": relative(RESEARCH / name),
                    "snapshot": name,
                    "sha256": frozen[relative(RESEARCH / name)],
                }
                for name in CODE
            ],
            "independent_producer_math_imports": 0,
            "prior_transform_audit_required_for_analytic_interval_provenance": True,
            "fixed_log_cells": 32,
            "fixed_log_exponent_classes": 960,
            "fixed_fresh_tail_rows": 1024,
            "fixed_cases": list(CASES),
            "new_cutoffs_precision_candidates_samples_gates_or_financial_paths": 0,
            "new_test_credit": 0,
            "interpreter": relative(Path(sys.executable)),
            "third_party_packages_imported": 0,
            "explicit_interpreter_frozen_membership_required": True,
            "all_frozen_insertions_resolve_aliases_without_SHA_overrides": True,
            "partial_preparation_failure_is_terminal_no_retry": True,
            "previous_fixture_counts_recredited": 0,
            "source_and_old_BM_price_ledger_adoption": False,
            "process_CPU_limit_seconds": CPU_LIMIT,
            "new_work_admission_CPU_seconds": ADMISSION_CPU,
            "wall_limit_seconds": WALL_LIMIT,
            "python": sys.version,
        },
    )
    verify(frozen)
    print("Independent exact AS241-law audit prospectively frozen", flush=True)


def verify_runtime_launcher(protocol):
    name = relative(Path(sys.executable))
    if name != protocol["interpreter"] or protocol["frozen_inputs"].get(name) != sha(
        Path(sys.executable)
    ):
        raise ValueError("Actual interpreter differs from explicit frozen launcher")


def run(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM)
    if (output / "summary.json").exists():
        raise FileExistsError("Independent AS241-law audit already terminal")
    protocol = read(output / "protocol.json")
    cpu_start, wall_start = time.process_time(), time.monotonic()
    checked_files = None

    def admit():
        if (
            time.process_time() - cpu_start >= ADMISSION_CPU
            or time.monotonic() - wall_start >= WALL_LIMIT
        ):
            raise TimeoutError("The fixed independent law-audit admission budget was reached")

    try:
        verify(protocol["frozen_inputs"])
        verify_runtime_launcher(protocol)
        native = read(TRANSFORM / "native_transform_certificate.json")
        fresh = read(TRANSFORM / "fresh_tail_sensitivity.json")
        if native["certified"] is not True or native["budget_censored"] is not False:
            raise ValueError("The successful all-input native scalar certificate is missing")
        sources = read(PAIR / "certificate.json")["source_bindings"]
        if native["source_bindings"] != sources:
            raise ValueError(
                "Native transform source hash inventory differs from the audited archive"
            )
        source_rows, tables, ln2s = [], [], []
        for case in CASES:
            admit()
            path = (ROOT / sources[case]["target"].replace("\\", "/")).resolve()
            path.relative_to(ROOT)
            digest = sha(path)
            if digest != sources[case]["target_sha256"] or (
                protocol["frozen_inputs"].get(relative(path)) != digest
            ):
                raise ValueError("The actual original source bytes/hash premise differs")
            target = read(path)
            if (target["width"], target["fraction_bits"]) != (72, 40):
                raise ValueError("The actual archived logarithm interface differs")
            tables.append(target["tables"]["log"])
            ln2s.append(sources[case]["literal_ln2"])
            source_rows.append({"case": case, "target": relative(path), "sha256": digest})
        if tables[0] != tables[1] or ln2s != [762123384786, 762123384786]:
            raise ValueError("Original B4/B8 log table/ln2 literals do not coincide")
        rho = audit_transform_classes(native, tables[0], ln2s[0], admit)
        tail, central = (
            read(TAIL / "tail_certificate.json"),
            read(CENTRAL / "central_certificate.json"),
        )
        if tail["certified"] is not True or central["certified"] is not True:
            raise ValueError("Successful original real-tail/central proofs are required")
        cells = read(TAIL / "cell_bounds.json")["cells"]
        error = audit_fresh_rows(native, fresh, tail, cells, central, rho, admit)
        create(
            output / "native_error_reconciliation.json",
            {
                "passed": True,
                "source_bindings": source_rows,
                "log_cells_reconstructed": 32,
                "log_classes_reconstructed": 960,
                "fresh_tail_rows_reconstructed": 1024,
                "native_transform_rho_upper_exact": pair(rho),
                "combined_native_quantile_error_upper_exact": pair(error),
                "old_hypothetical_floor_or_joint_Box_Muller_error_added": False,
                "analytic_interval_provenance_is_the_required_independent_transform_audit": True,
            },
        )
        rows = []
        for case in CASES:
            admit()
            row = audit_law_row(case, read(LAW / (case + "_certificate.json")), error)
            create(output / (case + "_audit.json"), row)
            rows.append(row)
        verify(protocol["frozen_inputs"])
        verify_runtime_launcher(protocol)
        checked_files = {
            relative(path): sha(path) for path in sorted(output.rglob("*")) if path.is_file()
        }
        cpu, wall = time.process_time() - cpu_start, time.monotonic() - wall_start
        if cpu >= CPU_LIMIT or wall >= WALL_LIMIT:
            raise TimeoutError("The fixed independent law-audit terminal budget was exceeded")
        create(
            output / "summary.json",
            {
                "passed": True,
                "budget_censored": False,
                "local_only": True,
                "new_test_credit": 0,
                "cases": rows,
                "log_classes_checked": 960,
                "fresh_tail_rows_checked": 1024,
                "midpoint_KS_plus_native_displacement_without_monotonicity_verified": True,
                "original_ideal_GBM_BV80_and_independent60_468_conversions_verified": True,
                "old_BM_obligation_or_native_financial_cost_bias_adopted": False,
                "native_financial_price_error_or_coherent_cost": None,
                "new_financial_samples_or_gate_evaluations": 0,
                "full_G2_or_quantum_advantage_claim": False,
                "independent_theorem": THEOREM,
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
                    "local_only": True,
                    "new_test_credit": 0,
                    "failure_type": type(failure).__name__,
                    "message": str(failure),
                    "financial_price_or_source_adopted": False,
                },
            )
        raise
    finally:
        if checked_files is None or (output / "failure.json").exists():
            checked_files = {
                relative(path): sha(path) for path in sorted(output.rglob("*")) if path.is_file()
            }
        else:
            # Bulk output hashes and dependency verification precede the
            # terminal CPU check; only the new small summary remains.
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
        "Independent AS241 scalar-law audit retained; native financial obligations remain separate",
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, default=PROGRAM / "A02_quantile_law_audit_run001")
    args = parser.parse_args()
    (prepare if args.mode == "prepare" else run)(args.output)
