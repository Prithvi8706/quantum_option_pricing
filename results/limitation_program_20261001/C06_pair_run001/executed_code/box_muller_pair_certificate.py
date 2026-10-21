"""Rigorous shared-uniform coupling for the unchanged native Box-Muller pair.

Every reported enclosure is a rational endpoint of mpmath interval arithmetic
or exact integer/rational algebra. The proof covers the pair and one B4 date;
full-path clipping and the discontinuous barrier remain separate obligations.
"""

from collections import Counter
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path

import mpmath as mp

from research.limitation_program_20261001.baseline import fingerprints
from research.controlled_source_completion.finance import normals_graph
from research.controlled_source_completion.ir import Graph


UNIFORM_BITS = 32
FRACTION_BITS = 40
WIDTH = 72
CUTOFF_BITS = (20, 24)
INTERVAL_DIGITS = 90
HEADROOM = Fraction(11, 2000)
CASES = {"B4x12": (4, 12), "B8x52": (8, 52)}
BASE = "results/limitation_program_20261001"
SOURCE_BASE = f"{BASE}/A10_coefficient_run001"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def encoded(value):
    value = Fraction(value)
    return [value.numerator, value.denominator]


def decoded(value):
    return Fraction(*value)


def iv(value):
    value = Fraction(value)
    return mp.iv.mpf(value.numerator) / value.denominator


def endpoint(value):
    sign, mantissa, exponent, _ = value
    return Fraction((-1) ** sign * mantissa) * Fraction(2) ** exponent


def enclosure(value):
    return tuple(endpoint(part) for part in value._mpi_)


def lower(value):
    return enclosure(value)[0]


def upper(value):
    return enclosure(value)[1]


def sqrt_upper(value):
    require(value >= 0, "Square-root upper endpoint needs a nonnegative rational")
    return upper(mp.iv.sqrt(iv(value)))


def error_to_interval(value, interval):
    lo, hi = interval
    return max(abs(value - lo), abs(value - hi))


def signed(value, width=WIDTH):
    value %= 1 << width
    return value - (1 << width) if value & (1 << (width - 1)) else value


def midpoint(raw, q=UNIFORM_BITS):
    require(type(raw) is int and 0 <= raw < 1 << q, "Uniform integer domain")
    return Fraction(2 * raw + 1, 1 << (q + 1))


def horner_floor_bound(degree, radius, epsilon):
    require(type(degree) is int and degree > 0 and 0 <= radius < 1, "Horner error domain")
    return epsilon * sum((radius**j for j in range(degree)), Fraction(0))


def table_certificate(name, rows, fraction_bits=FRACTION_BITS):
    """Verify each saved coefficient against its true Taylor coefficient."""
    require(name in ("log", "cos"), "Only the frozen log/cos table families")
    segments, degree = (32, 8) if name == "log" else (64, 7)
    require(len(rows) == segments and all(len(row) == degree + 1 for row in rows), "Table shape")
    epsilon = Fraction(1, 1 << fraction_bits)
    radius = Fraction(1, 2 * segments)
    coefficient_errors, checks = [], []
    maximum_horner_magnitude = Fraction(0)
    for index, row in enumerate(rows):
        center = Fraction(1 if name == "log" else 0) + Fraction(2 * index + 1, 2 * segments)
        errors = []
        for degree_index, raw in enumerate(row):
            require(type(raw) is int, "Literal table coefficient must be an integer")
            if name == "log":
                coefficient = (
                    enclosure(mp.iv.log(iv(center)))
                    if degree_index == 0
                    else (
                        Fraction((-1) ** (degree_index - 1), degree_index) / center**degree_index,
                    )
                    * 2
                )
            else:
                coefficient = enclosure(
                    (2 * mp.iv.pi) ** degree_index
                    * mp.iv.cos(2 * mp.iv.pi * iv(center) + degree_index * mp.iv.pi / 2)
                    / math.factorial(degree_index)
                )
            error = error_to_interval(Fraction(raw, 1 << fraction_bits), coefficient)
            require(
                error <= epsilon / 2,
                "Saved coefficient is not enclosed by its nearest rounding allowance",
            )
            errors.append(error)
            checks.append(
                dict(
                    row=index,
                    degree=degree_index,
                    literal=raw,
                    true_coefficient_enclosure=[encoded(part) for part in coefficient],
                    rounding_error_upper_exact=encoded(error),
                )
            )
        coefficient_errors.append(
            sum((error * radius**j for j, error in enumerate(errors)), Fraction(0))
        )
        bound = abs(Fraction(row[-1], 1 << fraction_bits))
        maximum_horner_magnitude = max(maximum_horner_magnitude, bound)
        for raw in reversed(row[:-1]):
            product_bound = bound * radius + epsilon
            bound = abs(Fraction(raw, 1 << fraction_bits)) + product_bound
            maximum_horner_magnitude = max(maximum_horner_magnitude, bound, product_bound)
    require(maximum_horner_magnitude < (1 << (WIDTH - fraction_bits - 1)), "Horner signed overflow")
    remainder = (
        radius ** (degree + 1) / (degree + 1)
        if name == "log"
        else upper((2 * mp.iv.pi * iv(radius)) ** (degree + 1) / math.factorial(degree + 1))
    )
    coefficients = max(coefficient_errors)
    truncation = horner_floor_bound(degree, radius, epsilon)
    return dict(
        name=name,
        segments=segments,
        degree=degree,
        coefficient_checks=checks,
        Taylor_remainder_upper_exact=encoded(remainder),
        coefficient_rounding_upper_exact=encoded(coefficients),
        Horner_floor_upper_exact=encoded(truncation),
        total_error_upper_exact=encoded(remainder + coefficients + truncation),
        maximum_native_intermediate_magnitude_exact=encoded(maximum_horner_magnitude),
        signed_overflow_excluded=True,
    )


def radial_grid_bound(delta, h=Fraction(1, 1 << (UNIFORM_BITS + 1))):
    require(
        0 < delta < Fraction(1, 2)
        and delta * (1 << UNIFORM_BITS) == int(delta * (1 << UNIFORM_BITS)),
        "Grid-aligned radial cutoff",
    )
    radius = mp.iv.sqrt(-2 * mp.iv.log(iv(delta)))
    require(
        lower(-2 * mp.iv.log(iv(Fraction(1, 2) + h))) > 1, "Low-u radial derivative monotonicity"
    )
    low = h / (delta * lower(radius))
    high = sqrt_upper(2 * h / (Fraction(1, 2) - h))
    return dict(
        low_u_derivative_bound_exact=encoded(low),
        high_u_Holder_bound_exact=encoded(high),
        radial_grid_error_upper_exact=encoded(max(low, high)),
        radial_maximum_upper_exact=encoded(upper(radius)),
        midpoint_remains_above_cutoff=True,
        proof=(
            "For U<1/2, u*sqrt(-2log u) increases on [delta,1/2+h], giving h/(delta*r(delta)). "
            "For U>=1/2, |log U-log midpoint|<=h/(1/2-h); square-root Holder continuity gives "
            "sqrt(2h/(1/2-h)). Delta is a q32 cell boundary, so U>=delta implies midpoint>=delta+h."
        ),
    )


def pair_bound(cutoff_bits, log_table, cos_table, literal_ln2):
    require(cutoff_bits in CUTOFF_BITS, "Only two prospectively fixed cutoffs")
    delta = Fraction(1, 1 << cutoff_bits)
    epsilon = Fraction(1, 1 << FRACTION_BITS)
    h = Fraction(1, 1 << (UNIFORM_BITS + 1))
    grid = radial_grid_bound(delta, h)
    ln2_error = error_to_interval(
        Fraction(literal_ln2, 1 << FRACTION_BITS), enclosure(mp.iv.log(iv(2)))
    )
    log_error = decoded(log_table["total_error_upper_exact"]) + cutoff_bits * ln2_error
    radius_transcendental = sqrt_upper(2 * log_error)
    radius_arithmetic = radius_transcendental + epsilon
    radius_maximum = decoded(grid["radial_maximum_upper_exact"])
    cos_error = decoded(cos_table["total_error_upper_exact"])
    normal_arithmetic = (
        radius_arithmetic + (radius_maximum + radius_arithmetic) * cos_error + epsilon
    )
    angular_grid = upper(2 * mp.iv.pi * iv(h) * iv(radius_maximum))
    normal_grid = decoded(grid["radial_grid_error_upper_exact"]) + angular_grid
    coordinate = normal_arithmetic + normal_grid
    return dict(
        cutoff_bits=cutoff_bits,
        delta_exact=encoded(delta),
        good_event="Shared radial U>=delta",
        radial_grid=grid,
        angular_grid_error_upper_exact=encoded(angular_grid),
        log_normalization_shift_error_exact=[0, 1],
        log_exponent_times_ln2_floor_error_exact=[0, 1],
        negative_two_log_floor_error_exact=[0, 1],
        log_ln2_literal_error_per_exponent_exact=encoded(ln2_error),
        log_error_upper_exact=encoded(log_error),
        sqrt_argument_approximation_error_upper_exact=encoded(2 * log_error),
        radius_Holder_error_upper_exact=encoded(radius_transcendental),
        sqrt_floor_error_upper_exact=encoded(epsilon),
        final_multiply_floor_error_upper_exact=encoded(epsilon),
        normal_arithmetic_error_upper_exact=encoded(normal_arithmetic),
        normal_grid_error_upper_exact=encoded(normal_grid),
        coordinate_discrepancy_upper_exact=encoded(coordinate),
        joint_pair_Linf_discrepancy_upper_exact=encoded(coordinate),
        joint_pair_L2_discrepancy_upper_exact=encoded(sqrt_upper(2) * coordinate),
        angular_quarter_turn_and_wrap_error_exact=[0, 1],
        zero_term_proof=(
            "q32 midpoint raw=(2k+1)*128 is exact in f40. Since midpoint<1, "
            "logarithm normalization "
            "is a left shift with exponent in [-33,-1]; no mantissa bits are discarded. "
            "Integer exponent times f40 ln2, multiplication by -2, and the .75 angular turn/wrap "
            "are exact integer operations. Square-root positive clipping is 1-Lipschitz "
            "and included in the Holder bound. A native sqrt and final product floor "
            "are each charged one f40 ulp."
        ),
        independence_claim=(
            "Continuous Box-Muller outputs are independent normals; "
            "finite digital outputs remain one joint shared-input pair."
        ),
    )


def polynomial_multiply(left, right):
    result = Counter()
    for j, a in left.items():
        for k, b in right.items():
            result[j + k] += a * b
    return dict(result)


def polynomial_magnitude(poly, radius):
    return sum((abs(value) * radius**degree for degree, value in poly.items()), Fraction(0))


def polynomial_floor_certificate(target, root, variable, radius):
    """Exact formal polynomial and absolute forward floor-error recurrence."""
    producers = {value: node for node in target["nodes"] for value in node["out"]}
    epsilon = Fraction(1, 1 << target["fraction_bits"])
    cache, steps = {}, []

    def visit(value):
        if value == variable:
            return {1: Fraction(1)}, Fraction(0)
        if value in cache:
            return cache[value]
        node = producers[value]
        if node["op"] == "const":
            poly = {
                0: Fraction(
                    signed(node["params"]["value"], target["width"]), 1 << target["fraction_bits"]
                )
            }
            error = Fraction(0)
        else:
            require(
                node["op"] in ("add", "mul") and len(node["args"]) == 2,
                "Unexpected Estrin polynomial operation",
            )
            left, left_error = visit(node["args"][0])
            right, right_error = visit(node["args"][1])
            if node["op"] == "add":
                poly = dict(left)
                for degree, coefficient in right.items():
                    poly[degree] = poly.get(degree, Fraction(0)) + coefficient
                error = left_error + right_error
            else:
                poly = polynomial_multiply(left, right)
                error = (
                    polynomial_magnitude(left, radius) * right_error
                    + polynomial_magnitude(right, radius) * left_error
                    + left_error * right_error
                    + epsilon
                )
        bound = polynomial_magnitude(poly, radius) + error
        require(
            bound < 1 << (target["width"] - target["fraction_bits"] - 1),
            "Estrin native signed overflow",
        )
        cache[value] = poly, error
        steps.append(
            dict(
                value=value,
                op=node["op"],
                magnitude_upper_exact=encoded(bound),
                floor_error_upper_exact=encoded(error),
            )
        )
        return cache[value]

    polynomial, error = visit(root)
    return dict(
        coefficients={str(degree): encoded(value) for degree, value in sorted(polynomial.items())},
        evaluation_floor_error_upper_exact=encoded(error),
        steps=steps,
        signed_overflow_excluded=True,
    )


def flatten_sum(producers, root):
    node = producers[root]
    if node["op"] == "add":
        return [value for arg in node["args"] for value in flatten_sum(producers, arg)]
    return [root]


def clipped_input(producers, root):
    last = producers[root]
    require(last["op"] == "select", "Actual exp input must be clipped")
    flag, middle, high = last["args"]
    require(
        producers[flag]["op"] == "lt" and producers[flag]["args"] == [middle, high],
        "Clip high comparator",
    )
    first = producers[middle]
    require(first["op"] == "select", "Clip low selector")
    low_flag, low, raw = first["args"]
    require(
        producers[low_flag]["op"] == "lt" and producers[low_flag]["args"] == [raw, low],
        "Clip low comparator",
    )
    return (
        raw,
        signed(producers[low]["params"]["value"]),
        signed(producers[high]["params"]["value"]),
    )


def date1_bound(target, pair, normal_roots, support):
    scale = 1 << target["fraction_bits"]
    epsilon = Fraction(1, scale)
    require(
        support["assets"] == 4 and support["dates"] == 12
        and support["basket_coefficient"] == scale // 4,
        "Actual B4 first-date averaging coefficient",
    )
    producers = {value: node for node in target["nodes"] for value in node["out"]}
    stock = support["stock_ids"][0]
    shift = producers[stock]
    require(shift["op"] == "shift", "Native date1 exponential shift")
    polynomial_root, k_value = shift["args"]
    k_node = producers[k_value]
    require(
        k_node["op"] == "bits"
        and k_node["params"]["signed"]
        and k_node["params"]["shift"] == FRACTION_BITS,
        "Native exp floor exponent",
    )
    alpha_node = producers[k_node["args"][0]]
    require(alpha_node["op"] == "cmul", "Native exp inverse-ln2 multiplication")
    clipped = alpha_node["args"][0]
    require(clipped == support["clipped_log_ids"][0], "Actual first stock/log scope")
    raw_log, low_guard, high_guard = clipped_input(producers, clipped)
    leaves = flatten_sum(producers, raw_log)
    products = [producers[value] for value in leaves if producers[value]["op"] == "cmul"]
    constants = [
        signed(producers[value]["params"]["value"])
        for value in leaves
        if producers[value]["op"] == "const"
    ]
    require(
        len(leaves) == 4 and len(products) == 2 and len(constants) == 2,
        "Actual first-date GBM increment shape",
    )
    product_by_normal = {node["args"][0]: node["params"]["c"] for node in products}
    require(
        set(product_by_normal) == set(normal_roots[:2]),
        "First date uses shared first Gaussian pair",
    )
    common, idiosyncratic = (
        Fraction(product_by_normal[value], scale) for value in normal_roots[:2]
    )
    spot_literal = Fraction(max(constants), scale)
    drift_literal = Fraction(min(constants), scale)
    common_true = enclosure(mp.iv.sqrt(iv(Fraction(3, 1000))))
    idio_true = enclosure(mp.iv.sqrt(iv(Fraction(9, 2000))))
    common_error = error_to_interval(common, common_true)
    idio_error = error_to_interval(idiosyncratic, idio_true)
    drift_error = abs(drift_literal - Fraction(-1, 800))
    spot_error = error_to_interval(spot_literal, enclosure(mp.iv.log(iv(100))))
    radius = decoded(pair["radial_grid"]["radial_maximum_upper_exact"])
    beta = decoded(pair["coordinate_discrepancy_upper_exact"])
    log_error = (
        (abs(common) + abs(idiosyncratic)) * beta
        + (common_error + idio_error) * radius
        + drift_error
        + spot_error
        + 2 * epsilon
    )
    digital_normal_max = radius + decoded(pair["normal_arithmetic_error_upper_exact"])
    digital_low = (
        spot_literal
        + drift_literal
        - (abs(common) + abs(idiosyncratic)) * digital_normal_max
        - 2 * epsilon
    )
    digital_high = (
        spot_literal + drift_literal + (abs(common) + abs(idiosyncratic)) * digital_normal_max
    )
    require(
        Fraction(low_guard, scale) < digital_low < digital_high < Fraction(high_guard, scale),
        "One-date clipping exclusion failed",
    )
    alpha = Fraction(alpha_node["params"]["c"], scale)
    ln2 = Fraction(support["literal_ln2"], scale)
    k_low, k_high = math.floor(alpha * digital_low), math.floor(alpha * digital_high)
    require(0 <= k_low <= k_high <= 30, "One-date exp left-shift domain")
    remainder_radius = max(abs(Fraction(k, 1) / alpha - k * ln2) for k in range(k_low, k_high + 1))
    remainder_radius = max(
        remainder_radius,
        max(abs(Fraction(k + 1, 1) / alpha - k * ln2) for k in range(k_low, k_high + 1)),
    )
    # Actual r = clipped_log - k*literal_ln2, with integer k: the cmul is exact.
    remainder_candidates = [
        node["out"][0]
        for node in target["nodes"]
        if node["op"] == "sub"
        and node["args"][0] == clipped
        and producers[node["args"][1]]["op"] == "cmul"
        and producers[node["args"][1]]["params"]["c"] == support["literal_ln2"]
    ]
    require(len(remainder_candidates) == 1, "Native exp remainder binding")
    remainder_value = remainder_candidates[0]
    polynomial = polynomial_floor_certificate(
        target, polynomial_root, remainder_value, remainder_radius
    )
    coefficients = {
        int(degree): decoded(value) for degree, value in polynomial["coefficients"].items()
    }
    require(set(coefficients) == set(range(13)), "Actual degree-12 Estrin polynomial")
    require(
        all(
            coefficients[j] == Fraction(round(Fraction(scale, math.factorial(j))), scale)
            for j in range(13)
        ),
        "Actual nearest Taylor coefficients",
    )
    coefficient_error = sum(
        (
            abs(coefficients[j] - Fraction(1, math.factorial(j))) * remainder_radius**j
            for j in range(13)
        ),
        Fraction(0),
    )
    remainder_error = upper(
        mp.iv.exp(iv(remainder_radius)) * iv(remainder_radius) ** 13 / math.factorial(13)
    )
    evaluation_error = decoded(polynomial["evaluation_floor_error_upper_exact"])
    ln2_error = error_to_interval(ln2, enclosure(mp.iv.log(iv(2))))
    reconstruction_error = upper(
        mp.iv.exp(iv(digital_high)) * (mp.iv.exp(iv(k_high * ln2_error)) - 1)
    )
    exp_error = (1 << k_high) * (
        coefficient_error + remainder_error + evaluation_error
    ) + reconstruction_error
    continuous_high = upper(
        mp.iv.log(iv(100))
        + iv(Fraction(-1, 800))
        + (mp.iv.sqrt(iv(Fraction(3, 1000))) + mp.iv.sqrt(iv(Fraction(9, 2000)))) * iv(radius)
    )
    coupled_exp_error = upper(mp.iv.exp(iv(continuous_high)) * (mp.iv.exp(iv(log_error)) - 1))
    stock_error = coupled_exp_error + exp_error
    shifted_magnitude = (1 << k_high) * (
        sum(abs(value) * remainder_radius**degree for degree, value in coefficients.items())
        + evaluation_error
    )
    require(
        shifted_magnitude < 1 << (WIDTH - FRACTION_BITS - 1), "Native final exp left-shift overflow"
    )
    asset_scopes = []
    for asset in range(4):
        asset_stock = support["stock_ids"][12 * asset]
        asset_shift = producers[asset_stock]
        require(asset_shift["op"] == "shift", "Every first-date stock is an actual exp")
        asset_k = producers[asset_shift["args"][1]]
        require(
            asset_k["op"] == "bits" and asset_k["params"] == k_node["params"],
            "Shared exp exponent template",
        )
        asset_alpha = producers[asset_k["args"][0]]
        require(
            asset_alpha["op"] == "cmul" and asset_alpha["params"] == alpha_node["params"],
            "Shared exp literal",
        )
        asset_log = asset_alpha["args"][0]
        asset_raw, asset_lo, asset_hi = clipped_input(producers, asset_log)
        require((asset_lo, asset_hi) == (low_guard, high_guard), "Shared clipping guard")
        asset_leaves = flatten_sum(producers, asset_raw)
        asset_products = [
            producers[value] for value in asset_leaves if producers[value]["op"] == "cmul"
        ]
        asset_constants = [
            signed(producers[value]["params"]["value"])
            for value in asset_leaves
            if producers[value]["op"] == "const"
        ]
        require(
            len(asset_leaves) == 4 and sorted(asset_constants) == sorted(constants),
            "All first-date drift/logspot literals",
        )
        require(
            {node["args"][0]: node["params"]["c"] for node in asset_products}
            == {
                normal_roots[0]: product_by_normal[normal_roots[0]],
                normal_roots[asset + 1]: product_by_normal[normal_roots[1]],
            },
            "All first-date common/idiosyncratic bindings",
        )
        asset_scopes.append(
            dict(
                asset=asset,
                stock=asset_stock,
                clipped_log=asset_log,
                normal_values=[normal_roots[0], normal_roots[asset + 1]],
            )
        )
    return dict(
        date=1,
        observation_time_exact=[1, 12],
        assets=4,
        Gaussian_pairs_used=3,
        common_coefficient_literal_exact=encoded(common),
        idiosyncratic_coefficient_literal_exact=encoded(idiosyncratic),
        common_coefficient_error_upper_exact=encoded(common_error),
        idiosyncratic_coefficient_error_upper_exact=encoded(idio_error),
        drift_literal_error_upper_exact=encoded(drift_error),
        log_spot_literal_error_upper_exact=encoded(spot_error),
        two_increment_floor_error_upper_exact=encoded(2 * epsilon),
        log_discrepancy_exact=encoded(log_error),
        spot_discrepancy_dollars_exact=encoded(stock_error),
        basket_discrepancy_dollars_exact=encoded(stock_error + epsilon),
        basket_native_averaging_floor_upper_exact=encoded(epsilon),
        digital_unclipped_log_enclosure_exact=[encoded(digital_low), encoded(digital_high)],
        clipping_inactive_on_good_event=True,
        exp_range_exponents=[k_low, k_high],
        exp_remainder_magnitude_upper_exact=encoded(remainder_radius),
        exp_Taylor_remainder_upper_exact=encoded(remainder_error),
        exp_coefficient_error_upper_exact=encoded(coefficient_error),
        exp_Estrin_floor_error_upper_exact=encoded(evaluation_error),
        exp_ln2_reconstruction_error_upper_exact=encoded(reconstruction_error),
        native_exp_discrepancy_dollars_exact=encoded(exp_error),
        coupled_log_to_spot_discrepancy_dollars_exact=encoded(coupled_exp_error),
        exp_integer_k_times_ln2_floor_error_exact=[0, 1],
        exp_final_left_shift_error_exact=[0, 1],
        exp_polynomial_certificate=polynomial,
        exp_final_shift_signed_overflow_excluded=True,
        all_four_asset_date1_scopes=asset_scopes,
        unchanged_exp_templates_certified_by_independent_E03_audit=True,
        first_asset_template_bound_applies_to_all_four_assets=True,
        one_date_component_below_unallocated_headroom=stock_error <= HEADROOM,
        component_comparison_is_not_full_price_certification=True,
        barrier_boundary_mass=None,
        complete_price_bias_dollars=None,
    )


def support_binding(root, case):
    root = Path(root)
    certificate_path = root / BASE / "E03_support_run001" / f"{case}_certificate.json"
    audit_path = root / BASE / "E03_support_audit_run002" / f"{case}_audit.json"
    certificate, audit = read(certificate_path), read(audit_path)
    for directory, path in (
        ("E03_support_run001", certificate_path),
        ("E03_support_audit_run002", audit_path),
    ):
        manifest = read(root / BASE / directory / "manifest.json")
        require(
            manifest["files"][path.relative_to(root).as_posix()] == sha(path),
            "Support certificate/audit receipt binding",
        )
        target = root / SOURCE_BASE / case / "min-depth/target.json"
        bindings = {
            str(name).replace("\\", "/"): value for name, value in manifest["frozen_inputs"].items()
        }
        require(
            bindings[target.relative_to(root).as_posix()] == sha(target),
            "Support actual target binding",
        )
    require(
        audit["passed"] is True and certificate["payoff_raw_bounds"] == audit["payoff_raw_bounds"],
        "Independent support audit",
    )
    require(
        0
        == certificate["payoff_raw_bounds"][0]
        <= certificate["payoff_raw_bounds"][1]
        < 40 * (1 << FRACTION_BITS),
        "Digital dollar support below 40",
    )
    return certificate, dict(
        certificate=certificate_path.relative_to(root).as_posix(),
        certificate_sha256=sha(certificate_path),
        independent_audit=audit_path.relative_to(root).as_posix(),
        independent_audit_sha256=sha(audit_path),
        payoff_difference_on_bad_event_upper_dollars_exact=[40, 1],
    )


def normal_binding(target, count):
    inputs = [node for node in target["nodes"] if node["op"] == "input"]
    require(
        len(inputs) == count
        and all(
            node["params"]["bits"] == UNIFORM_BITS
            and node["params"].get("preparation", "uniform") == "uniform"
            for node in inputs
        ),
        "Original q32 product input law",
    )
    graph = Graph(FRACTION_BITS)
    roots = normals_graph(graph, count, UNIFORM_BITS)
    original = json.loads(json.dumps(graph.as_dict()))
    require(original["tables"] == target["tables"], "Actual normal table identity")
    original_keys, target_keys = fingerprints(original), fingerprints(target)
    reverse = {token: value for value, token in target_keys.items()}
    require(len(reverse) == len(target_keys), "Unambiguous typed SSA identities")
    result = [reverse[original_keys[value]] for value in roots]
    require(len(set(result)) == count, "Every normal output has an actual target binding")
    ln2_nodes = [
        node for node in original["nodes"] if node["op"] == "cmul" and node["params"]["c"] > 0
    ]
    require(len({node["params"]["c"] for node in ln2_nodes}) == 1, "Single original ln2 literal")
    return result, ln2_nodes[0]["params"]["c"]


def certify(root):
    root = Path(root).resolve()
    mp.iv.dps = INTERVAL_DIGITS
    targets, certificates, supports, bindings = {}, {}, {}, {}
    for case, (assets, dates) in CASES.items():
        target_path = root / SOURCE_BASE / case / "min-depth/target.json"
        target = read(target_path)
        require(
            target["width"] == WIDTH and target["fraction_bits"] == FRACTION_BITS,
            "Fixed native precision",
        )
        targets[case] = target
        certificates[case], supports[case] = support_binding(root, case)
        roots, ln2 = normal_binding(target, dates * (assets + 1))
        bindings[case] = dict(
            target=target_path.relative_to(root).as_posix(),
            target_sha256=sha(target_path),
            normal_values=roots,
            pair_count=len(roots) // 2,
            scalar_count=len(roots),
            literal_ln2=ln2,
        )
    require(
        targets["B4x12"]["tables"] == targets["B8x52"]["tables"],
        "One unchanged pair function across B4/B8",
    )
    log_table = table_certificate("log", targets["B4x12"]["tables"]["log"])
    cos_table = table_certificate("cos", targets["B4x12"]["tables"]["cos"])
    candidates, claims = [], {}
    for cutoff in CUTOFF_BITS:
        pair = pair_bound(cutoff, log_table, cos_table, bindings["B4x12"]["literal_ln2"])
        delta = decoded(pair["delta_exact"])
        pair["B4_date1"] = date1_bound(
            targets["B4x12"], pair, bindings["B4x12"]["normal_values"], certificates["B4x12"]
        )
        pair["tail_probability_union_upper_exact"] = {
            "one_pair": encoded(delta),
            "B4_date1_three_pairs": encoded(3 * delta),
            "B4_all30_pairs": encoded(30 * delta),
            "B8_all234_pairs": encoded(234 * delta),
        }
        pair["tail_payoff_difference_dollars_upper_exact"] = {
            "B4_date1_bad_pair_event_only": encoded(40 * 3 * delta),
            "B4_all30_pairs_bad_event_only": encoded(40 * 30 * delta),
            "B8_all234_pairs_bad_event_only": encoded(40 * 234 * delta),
        }
        coupling_id = f"C06_q32_f40_shared_uniform_delta2minus{cutoff}"
        pair["coupling_id"] = coupling_id
        pair["claims"] = [
            dict(
                kind="basket-absolute-error",
                upper_exact=pair["B4_date1"]["basket_discrepancy_dollars_exact"],
                scope=dict(case="B4x12", date=1),
                coupling_id=coupling_id,
                measure="continuous-underlying-uniform-coupling",
                native_exp_and_clipping_included=True,
                proved=True,
                event="First three radial uniforms are at least delta",
            ),
            dict(
                kind="bad-event-probability",
                upper_exact=encoded(3 * delta),
                scope=dict(case="B4x12", date=1),
                coupling_id=coupling_id,
                measure="continuous-underlying-uniform-coupling",
                proved=True,
            ),
        ]
        claims[f"delta2minus{cutoff}_B4_date1_basket"] = pair["claims"][0]
        claims[f"delta2minus{cutoff}_B4_date1_bad_event"] = pair["claims"][1]
        candidates.append(pair)
    epsilon = Fraction(1, 1 << FRACTION_BITS)
    global_log = decoded(log_table["maximum_native_intermediate_magnitude_exact"]) + 33 * abs(
        Fraction(bindings["B4x12"]["literal_ln2"], 1 << FRACTION_BITS)
    )
    global_radius = sqrt_upper(2 * global_log) + epsilon
    global_cos = 1 + decoded(cos_table["total_error_upper_exact"])
    require(
        global_radius * global_cos + epsilon < (1 << (WIDTH - FRACTION_BITS - 1)),
        "Native pair signed overflow",
    )
    return dict(
        format="joint-Box-Muller-midpoint-coupling-v1",
        law=(
            "Shared U,V independent continuous uniforms; digital raw words are their q32 cell "
            "indexes, followed by the original exact f40 midpoint/native graph"
        ),
        coupling_method="One shared-uniform midpoint coupling, two fixed radial cutoffs",
        uniform_bits=UNIFORM_BITS,
        fraction_bits=FRACTION_BITS,
        native_width=WIDTH,
        interval_decimal_precision=INTERVAL_DIGITS,
        outward_exact_rational_endpoints=True,
        source_bindings=bindings,
        payoff_support_bindings=supports,
        log_table_certificate=log_table,
        cos_table_certificate=cos_table,
        candidates=candidates,
        claims=claims,
        native_pair_no_overflow_certificate=dict(
            all_q32_midpoints=True,
            log_exponent_integer_bounds=[-33, -1],
            normalized_mantissa_raw_bounds=[1 << FRACTION_BITS, (2 << FRACTION_BITS) - 1],
            logarithm_magnitude_upper_exact=encoded(global_log),
            radius_magnitude_upper_exact=encoded(global_radius),
            final_normal_magnitude_upper_exact=encoded(global_radius * global_cos + epsilon),
            signed_native_real_magnitude_limit_exact=[1 << (WIDTH - FRACTION_BITS - 1), 1],
            all_Horner_intermediates_checked=True,
            native_output_overflow_excluded=True,
        ),
        unallocated_dollar_headroom_exact=encoded(HEADROOM),
        tail_dollar_proof=(
            "Both discounted payoffs are nonnegative and below40: digital support is "
            "independently audited; continuous survival requires every monitored basket<140, "
            "so the date/asset average<140 and the strike100 call is <40 before discount. "
            "Therefore absolute difference is <=40 on any event, not the sum of two bounds."
        ),
        unresolved=dict(
            full_path_clipping_dollar_bias=None,
            full_path_stock_error=None,
            barrier_boundary_probability=None,
            complete_price_bias_dollars=None,
            physical_runtime=None,
        ),
        full_G2_closed=False,
        complete_price_certified=False,
        new_financial_gate_replays=0,
        scope=(
            "Joint-pair and B4 first-date component certificate only; tail union terms are "
            "bounds for the stated bad-pair events, not the full remaining price bias."
        ),
    )
