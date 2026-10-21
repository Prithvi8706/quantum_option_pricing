"""Bind AS241 financial SSA with strict signed decoding of semantic words.

These functions inspect saved SSA only. They do not build graphs, regenerate
coefficients, compile gates or transfer old Box-Muller source costs.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
import json
from math import factorial

S = 1 << 40
EPS = Fraction(1, S)
CASES = {"B4x12": (4, 12), "B8x52": (8, 52)}
LAW = "independent q32 midpoint inputs, mathematical-native signed-restored AS241"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def signed(value):
    value %= 1 << 72
    return value - (1 << 72) if value >= 1 << 71 else value


def semantic_word(value, field):
    """Decode only canonical unsigned72 JSON integer literals, never coerce."""
    require(
        type(value) is int and 0 <= value < 1 << 72,
        "Canonical modular native72 semantic word: " + field,
    )
    return value - (1 << 72) if value >= 1 << 71 else value


def signed_semantic_inventory(semantics, assets, dates):
    """Separate literal words from SSA IDs and Boolean semantic assertions."""
    result = {}
    for field in (
        "initial_log_raw",
        "lower_log_raw",
        "upper_log_raw",
        "basket_coefficient_raw",
        "average_coefficient_raw",
        "discount_coefficient_raw",
        "native_exp_inverse_ln2_raw",
        "native_exp_ln2_raw",
    ):
        result[field] = semantic_word(semantics[field], field)
    for field, count in (
        ("common_coefficients_raw_by_date", dates),
        ("native_exp_coefficients_raw", 13),
    ):
        words = semantics[field]
        require(
            type(words) is list and len(words) == count, "Complete semantic word list: " + field
        )
        result[field] = [
            semantic_word(word, field + "[" + str(index) + "]") for index, word in enumerate(words)
        ]
    for field in (
        "idiosyncratic_coefficients_raw_by_date_asset",
        "drift_literals_raw_by_date_asset",
    ):
        rows = semantics[field]
        require(
            type(rows) is list and len(rows) == dates, "Complete semantic date inventory: " + field
        )
        decoded = []
        for date, words in enumerate(rows):
            require(
                type(words) is list and len(words) == assets,
                "Complete semantic asset inventory: " + field,
            )
            decoded.append(
                [
                    semantic_word(word, field + "[" + str(date) + "][" + str(asset) + "]")
                    for asset, word in enumerate(words)
                ]
            )
        result[field] = decoded
    return result


def pair(value):
    value = Fraction(value)
    return [value.numerator, value.denominator]


def exact(value):
    require(isinstance(value, list) and len(value) == 2, "Exact rational pair required")
    require(all(type(v) is int for v in value) and value[1] > 0, "Exact integer endpoints")
    return Fraction(*value)


def canonical_hash(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def producers(target):
    require((target["width"], target["fraction_bits"]) == (72, 40), "Native72/f40 required")
    result = {}
    for node in target["nodes"]:
        for slot, output in enumerate(node["out"]):
            require(type(output) is int and output not in result, "Unique actual SSA producer")
            result[output] = (node, slot)
    return result


def normalized_closure(target, root, boundary):
    source = producers(target)
    require(len(set(boundary)) == len(boundary), "Distinct ordered normal boundaries required")
    stop = {value: index for index, value in enumerate(boundary)}
    cache = {}

    def visit(value):
        if value in stop:
            return canonical_hash(["normal", stop[value]])
        if value not in cache:
            node, slot = source[value]
            require(node["op"] != "input", "Unbound financial input below normal boundary")
            cache[value] = canonical_hash(
                [node["op"], node["params"], slot, [visit(arg) for arg in node["args"]]]
            )
        return cache[value]

    visit(root)
    tokens = {
        value: canonical_hash(["normal_boundary", index]) for index, value in enumerate(boundary)
    }
    records = []
    for item in target["nodes"]:
        if not any(value in cache for value in item["out"]):
            continue
        require(all(value in cache for value in item["out"]), "Atomic financial producer")
        record = {
            "op": item["op"],
            "params": item["params"],
            "args": [tokens[value] for value in item["args"]],
            "outputs": len(item["out"]),
        }
        if item["op"] == "lookup":
            record["table_sha256"] = canonical_hash(target["tables"][item["params"]["table"]])
        base = canonical_hash(record)
        for slot, value in enumerate(item["out"]):
            tokens[value] = canonical_hash([base, slot])
        records.append(record)
    require(target["outputs"] == {"Y": root}, "Single original named financial output")
    body = {
        "width": target["width"],
        "fraction_bits": target["fraction_bits"],
        "normal_count": len(boundary),
        "nodes": records,
        "outputs": {"Y": tokens[root]},
    }
    return canonical_hash(body), set(cache)


def validate_scalar_invocations(target, bundle, scalar):
    """Inspect every saved scalar producer, including eagerly computed branches."""
    require(bundle["target_sha256"] == canonical_hash(target), "Full new source fingerprint")
    ns = bundle["normal_source"]
    require(
        ns["law"] == LAW and ns["scalar_target_sha256"] == canonical_hash(scalar),
        "Actual signed-restored scalar law fingerprint",
    )
    require(len(scalar["inputs"]) == 1 and set(scalar["outputs"]) == {"Z"}, "Scalar Z ABI")
    old_source = producers(scalar)
    input_node, _ = old_source[scalar["inputs"][0]]
    require(
        input_node["params"] == {"name": "k", "bits": 32, "preparation": "uniform"},
        "Independent uniform q32 midpoint input",
    )
    count = sum(len(item["out"]) for item in scalar["nodes"])
    source = producers(target)
    na, nt = CASES[bundle["case"]]
    require(len(ns["invocations"]) == (na + 1) * nt, "Every original scalar role supplied")
    inputs, outputs = [], []
    for coordinate, invocation in enumerate(ns["invocations"]):
        offset = coordinate * count
        name = "as241_uniform_" + str(coordinate)
        date, role = divmod(coordinate, na + 1)
        require(
            invocation["coordinate"] == coordinate
            and invocation["value_offset"] == offset
            and invocation["date_index"] == date
            and invocation["scalar_values"] == count
            and invocation["role"] == ("common" if role == 0 else "idiosyncratic")
            and invocation["asset_index"] == (None if role == 0 else role - 1),
            "Actual date-major common/idiosyncratic roles",
        )
        for local_index, item in enumerate(scalar["nodes"]):
            params = dict(item["params"])
            if item["op"] == "input":
                params["name"] = name
            expected = dict(
                item,
                params=params,
                args=[offset + value for value in item["args"]],
                out=[offset + value for value in item["out"]],
            )
            require(
                source[expected["out"][0]][0] == expected
                and target["nodes"][coordinate * len(scalar["nodes"]) + local_index] == expected,
                "Actual scalar producer differs from accepted whole scalar recipe",
            )
            if item["op"] == "lookup":
                table = params["table"]
                require(
                    target["tables"][table] == scalar["tables"][table], "Actual scalar table bytes"
                )
        input_value = offset + scalar["inputs"][0]
        output_value = offset + scalar["outputs"]["Z"]
        require(
            invocation["input_name"] == name
            and invocation["input_value"] == input_value
            and invocation["output_value"] == output_value,
            "Scalar interface role map",
        )
        inputs.append(input_value)
        outputs.append(output_value)
    require(
        inputs == target["inputs"] and outputs == bundle["normal_values"],
        "No additional input/free normal or missing independent invocation",
    )
    require(
        ns["input_names"] == ["as241_uniform_" + str(i) for i in range(len(inputs))],
        "Every independent input name bound",
    )
    _, financial_values = normalized_closure(target, target["outputs"]["Y"], outputs)
    financial_indices = [
        i
        for i, item in enumerate(target["nodes"])
        if any(value in financial_values for value in item["out"])
    ]
    require(
        financial_indices == list(range(len(inputs) * len(scalar["nodes"]), len(target["nodes"]))),
        "Financial closure must be exactly the appended disjoint region",
    )
    require(
        len(source) == count * len(inputs) + len(financial_values),
        "No unbound additional scalar or financial producer",
    )
    return {
        "independent_scalar_invocations": len(inputs),
        "actual_scalar_source_bound": True,
        "scalar_target_sha256": canonical_hash(scalar),
    }


def validate_normalization(target, bundle, archive, original_normals):
    case = bundle["case"]
    require(case in CASES, "Original supported financial contract")
    na, nt = CASES[case]
    require((bundle["assets"], bundle["dates"]) == (na, nt), "Original dimensions")
    normals = bundle["normal_values"]
    require(len(normals) == len(original_normals) == (na + 1) * nt, "Complete ordered drivers")
    new_hash, values = normalized_closure(target, target["outputs"]["Y"], normals)
    old_hash, old_values = normalized_closure(archive, archive["outputs"]["Y"], original_normals)
    require(new_hash == old_hash, "Actual financial function changed under normal boundaries")
    record = bundle["financial_normalization"]
    require(record.get("normalized_equality") is True, "Frontend normalized equality required")
    require(record.get("normalized_closure_sha256") == new_hash, "Normalized closure binding")
    require(record.get("original_boundary_values") == original_normals, "Original driver roles")
    mapping = {int(key): value for key, value in record["original_to_new"].items()}
    require(
        all(mapping.get(value) == normals[index] for index, value in enumerate(original_normals)),
        "Actual scalar invocation to original driver role mapping",
    )
    require(all(value in mapping for value in old_values), "Complete original financial mapping")
    require({mapping[value] for value in old_values} == values, "Complete new financial mapping")
    old_source, new_source = producers(archive), producers(target)
    for value in old_values:
        old, slot = old_source[value]
        new, new_slot = new_source[mapping[value]]
        require(
            slot == new_slot
            and old["op"] == new["op"]
            and old["params"] == new["params"]
            and [mapping[arg] for arg in old["args"]] == new["args"]
            and [mapping[out] for out in old["out"]] == new["out"],
            "Verbatim original financial producer",
        )
    return {
        "normalized_closure_sha256": new_hash,
        "financial_values": sorted(values),
        "normal_values": normals,
        "new_financial_source_law": LAW,
    }


def validate_ledger(ledger, target_sha256):
    require(ledger.get("source_target_sha256") == target_sha256, "NEW source-matched ledger")
    require(ledger.get("law") == LAW, "Different AS241 scalar law must be named")
    wanted = {
        "epsilon_dollars_exact": Fraction(1, 100),
        "statistical_allowance_dollars_exact": Fraction(9, 2000),
        "residual_financial_allowance_dollars_exact": Fraction(11, 2000),
    }
    for name, value in wanted.items():
        require(exact(ledger[name]) == value, "Frozen original accuracy allocation")
    require(
        wanted["epsilon_dollars_exact"]
        == wanted["statistical_allowance_dollars_exact"]
        + wanted["residual_financial_allowance_dollars_exact"],
        "Exact budget sum",
    )
    require(
        ledger.get("accepted_joint_Box_Muller_obligation_filled") is False,
        "Do not fill the accepted joint-Box-Muller obligation",
    )
    require(
        ledger.get("old_E02_source_or_wrapper_costs_transferred") is False,
        "Old source costs do not transfer",
    )
    require(
        ledger.get("source_resources") is None and ledger.get("wrapper_resources") is None,
        "New source and wrapper quantum costs remain unknown",
    )
    return wanted


def extract_financial(target, bundle):
    case = bundle["case"]
    na, nt = CASES[case]
    source = producers(target)
    normal_values = bundle["normal_values"]
    require(len(set(normal_values)) == (na + 1) * nt, "Independent scalar invocation boundaries")
    sem = bundle["semantics"]
    words = signed_semantic_inventory(sem, na, nt)
    lower_log_raw = words["lower_log_raw"]
    upper_log_raw = words["upper_log_raw"]

    def node(value, op=None):
        actual, slot = source[value]
        require(slot == 0 and len(actual["out"]) == 1, "Single-output financial node")
        if op is not None:
            require(actual["op"] == op, "Actual financial operation changed: " + op)
        return actual

    def constant(value):
        return signed(node(value, "const")["params"]["value"])

    def sums(value):
        item = node(value)
        if item["op"] == "add":
            return [leaf for arg in item["args"] for leaf in sums(arg)]
        return [value]

    def maxima(value):
        item = node(value)
        if item["op"] != "select":
            return [value]
        flag, right, left = item["args"]
        require(node(flag, "lt")["args"] == [left, right], "Original maximum comparator")
        return maxima(left) + maxima(right)

    output = target["outputs"]["Y"]
    alive, payoff, zero = node(output, "select")["args"]
    require(constant(zero) == 0, "Original knockout output zero")
    maximum, barrier = node(alive, "lt")["args"]
    baskets = maxima(maximum)
    require(len(baskets) == nt and baskets == sem["basket_values"], "All ordered monitored baskets")
    discount_node = node(payoff, "cmul")
    positive = node(discount_node["args"][0], "positive")["args"][0]
    average, strike = node(positive, "sub")["args"]
    average_node = node(average, "cmul")
    total = average_node["args"][0]
    require(
        (output, alive, payoff, average, total)
        == (
            sem["output_value"],
            sem["alive_value"],
            sem["discounted_payoff_value"],
            sem["average_value"],
            sem["asian_stock_sum_value"],
        ),
        "Actual payoff ancestry binding",
    )
    require(constant(barrier) == 140 * S and constant(strike) == 100 * S, "Original strict H/K")
    stocks_by_date = []
    for basket in baskets:
        item = node(basket, "cmul")
        require(item["params"]["c"] * na == S, "Exact binary basket coefficient")
        stocks = sums(item["args"][0])
        require(len(stocks) == na, "Every asset in each monitored basket")
        stocks_by_date.append(stocks)
    stocks = [[stocks_by_date[j][i] for j in range(nt)] for i in range(na)]
    require(stocks == sem["stock_values"], "Ordered actual stock/date interface")
    require(
        Counter(sums(total)) == Counter(value for row in stocks for value in row),
        "Original complete Asian stock sum",
    )
    require(len(set(value for row in stocks for value in row)) == na * nt, "Distinct stock sites")
    sites = []
    common, idio, drift = [], [], []
    for asset in range(na):
        for date in range(nt):
            stock = stocks[asset][date]
            polynomial, exponent = node(stock, "shift")["args"]
            exponent_node = node(exponent, "bits")
            require(
                exponent_node["params"] == {"shift": 40, "width": 72, "signed": True},
                "Native floor exponent bits",
            )
            inverse_node = node(exponent_node["args"][0], "cmul")
            clipped = inverse_node["args"][0]
            flag, middle, high = node(clipped, "select")["args"]
            require(node(flag, "lt")["args"] == [middle, high], "Actual upper stock clamp")
            low_flag, low, raw = node(middle, "select")["args"]
            require(node(low_flag, "lt")["args"] == [raw, low], "Actual lower stock clamp")
            require(
                (raw, clipped)
                == (sem["raw_log_values"][asset][date], sem["clipped_log_values"][asset][date]),
                "Raw/stock-only clamp IDs",
            )
            require(
                (constant(low), constant(high)) == (lower_log_raw, upper_log_raw),
                "Actual clamp literals",
            )
            prefix = sums(raw)
            multipliers = [node(value) for value in prefix if node(value)["op"] == "cmul"]
            constants = [constant(value) for value in prefix if node(value)["op"] == "const"]
            require(len(prefix) == len(multipliers) + len(constants), "Only raw linear prefixes")
            expected = [normal_values[j * (na + 1)] for j in range(date + 1)] + [
                normal_values[j * (na + 1) + asset + 1] for j in range(date + 1)
            ]
            require(
                Counter(item["args"][0] for item in multipliers) == Counter(expected),
                "All original common/idiosyncratic driver roles through this date",
            )
            if asset == date == 0:
                require(len(constants) == 2, "First raw log has initial spot and drift")
                initial, mu = max(constants), min(constants)
                require(initial == words["initial_log_raw"], "Actual initial log literal")
            require(
                sum(constants) == initial + (date + 1) * mu, "Every raw drift/init contribution"
            )
            coefficients = {item["args"][0]: item["params"]["c"] for item in multipliers}
            a = coefficients[normal_values[date * (na + 1)]]
            b = coefficients[normal_values[date * (na + 1) + asset + 1]]
            require(a > 0 and b > 0, "Positive original native increment coefficients")
            if asset == 0:
                common.append(a)
                idio.append(b)
                drift.append(mu)
            require(a == common[date] and b == idio[date], "Shared equal-volatility literals")
            for j in range(date + 1):
                require(
                    coefficients[normal_values[j * (na + 1)]] == common[j]
                    and coefficients[normal_values[j * (na + 1) + asset + 1]] == idio[j],
                    "Every prefix multiplier has the proper date literal",
                )
            candidates = []
            visited = set()

            def visit(value):
                if value in visited:
                    return
                visited.add(value)
                item = node(value)
                if item["op"] == "sub" and item["args"][0] == clipped:
                    ln_node = node(item["args"][1], "cmul")
                    scale_node = node(ln_node["args"][0], "bits")
                    require(
                        scale_node["args"] == [exponent]
                        and scale_node["params"] == {"shift": -40, "width": 72, "signed": False},
                        "Exact exponent scaling",
                    )
                    candidates.append(
                        (value, ln_node["params"]["c"], ln_node["out"][0], scale_node["out"][0])
                    )
                    return
                require(item["op"] in ("const", "add", "mul"), "Actual Estrin polynomial DAG")
                for arg in item["args"]:
                    visit(arg)

            visit(polynomial)
            require(len(set(candidates)) == 1, "One actual range-reduction remainder")
            remainder, ln2, ln_value, scaled_exponent = candidates[0]
            sites.append(
                dict(
                    asset=asset,
                    date=date + 1,
                    stock=stock,
                    polynomial=polynomial,
                    remainder=remainder,
                    exponent=exponent,
                    clipped=clipped,
                    raw_log=raw,
                    clip_middle=middle,
                    inverse_value=inverse_node["out"][0],
                    scaled_exponent=scaled_exponent,
                    ln_value=ln_value,
                    inverse_ln2=inverse_node["params"]["c"],
                    ln2=ln2,
                    semantic_exp_coefficients_signed=words["native_exp_coefficients_raw"],
                )
            )
    require(
        common == words["common_coefficients_raw_by_date"]
        and [[value] * na for value in idio]
        == words["idiosyncratic_coefficients_raw_by_date_asset"]
        and [[value] * na for value in drift] == words["drift_literals_raw_by_date_asset"],
        "Complete actual native coefficient inventory",
    )
    require(
        words["basket_coefficient_raw"] == S // na
        and average_node["params"]["c"] == words["average_coefficient_raw"]
        and discount_node["params"]["c"] == words["discount_coefficient_raw"],
        "Complete actual native payoff coefficient inventory",
    )
    require(
        all(
            site["inverse_ln2"] == words["native_exp_inverse_ln2_raw"]
            and site["ln2"] == words["native_exp_ln2_raw"]
            for site in sites
        ),
        "Complete actual native range-reduction literal inventory",
    )
    return dict(
        case=case,
        assets=na,
        dates=nt,
        normal_values=normal_values,
        sites=sites,
        initial_log_raw=initial,
        lower_log_raw=lower_log_raw,
        upper_log_raw=upper_log_raw,
        common_coefficients=common,
        idiosyncratic_coefficients=idio,
        drift_literals=drift,
        basket_values=baskets,
        average_coefficient=average_node["params"]["c"],
        discount_coefficient=discount_node["params"]["c"],
        barrier_raw=140 * S,
        strike_raw=100 * S,
        output_value=output,
    )


def polynomial_model(target, site, radius, source=None):
    """Actual sparse polynomial, floor propagation and product-word checks."""
    source = producers(target) if source is None else source
    cache, steps = {}, []

    def visit(value):
        if value == site["remainder"]:
            return {1: Fraction(1)}, Fraction(0)
        if value in cache:
            return cache[value]
        item, _ = source[value]
        if item["op"] == "const":
            poly, error = {0: Fraction(signed(item["params"]["value"]), S)}, Fraction(0)
        else:
            require(item["op"] in ("add", "mul"), "Actual fixed Estrin operations")
            a, ea = visit(item["args"][0])
            b, eb = visit(item["args"][1])
            ma = sum(abs(c) * radius**k for k, c in a.items())
            mb = sum(abs(c) * radius**k for k, c in b.items())
            if item["op"] == "add":
                poly = dict(a)
                for k, c in b.items():
                    poly[k] = poly.get(k, Fraction(0)) + c
                error = ea + eb
            else:
                poly = {}
                for ka, ca in a.items():
                    for kb, cb in b.items():
                        poly[ka + kb] = poly.get(ka + kb, Fraction(0)) + ca * cb
                error = ma * eb + mb * ea + ea * eb + EPS
                require(
                    (ma + ea) * (mb + eb) * S * S < 1 << 143, "Full signed144 polynomial product"
                )
        bound = sum(abs(c) * radius**k for k, c in poly.items()) + error
        require(bound * S < 1 << 71, "Actual polynomial stored72 output")
        cache[value] = poly, error
        steps.append(
            dict(
                value=value,
                op=item["op"],
                magnitude_upper_exact=pair(bound),
                floor_error_upper_exact=pair(error),
            )
        )
        return poly, error

    coefficients, error = visit(site["polynomial"])
    require(set(coefficients) == set(range(13)), "Actual degree12 stock polynomial")
    require(all(c >= 0 for c in coefficients.values()), "Positive stock Taylor coefficients")
    require(
        [coefficients[degree] for degree in range(13)]
        == [Fraction(word, S) for word in site["semantic_exp_coefficients_signed"]],
        "Exact degree0..12 semantic coefficient inventory matches actual polynomial",
    )
    delta = sum(abs(coefficients[k] - Fraction(1, factorial(k))) * radius**k for k in range(13))
    return coefficients, error, delta, steps


def polynomial_template(target, site, source=None):
    require((target["width"], target["fraction_bits"]) == (72, 40), "Native72/f40 template")
    source = producers(target) if source is None else source
    records, cache = [], {}

    def visit(value):
        if value == site["remainder"]:
            return "remainder"
        if value not in cache:
            item, slot = source[value]
            require(
                slot == 0 and item["op"] in ("const", "add", "mul"), "Stock polynomial template"
            )
            if item["op"] == "const":
                require(
                    item["args"] == [] and set(item["params"]) == {"value"},
                    "Exact native polynomial constant parameters",
                )
                semantic_word(item["params"]["value"], "actual polynomial constant")
                children = []
            else:
                require(
                    len(item["args"]) == 2 and item["params"] == {},
                    "Exact binary native polynomial add/mul parameters",
                )
                # Integer add and signed144 floor multiplication are symmetric.
                # Canonicalize only this comparison hash, never the actual SSA.
                children = sorted(visit(arg) for arg in item["args"])
            record = [item["op"], item["params"], children]
            cache[value] = canonical_hash(record)
            records.append(value)
        return cache[value]

    return visit(site["polynomial"]), records, cache


def ceildiv(a, b):
    require(type(a) is int and type(b) is int and b > 0, "Integer positive ceiling divisor")
    return -(-a // b)


def check_word(bounds):
    require(-(1 << 71) <= bounds[0] <= bounds[1] < 1 << 71, "Signed native72 storage may overflow")
    return bounds


def multiply_bounds(left, right, square=False):
    products = [a * b for a in left for b in right]
    low, high = min(products), max(products)
    if square:
        require(left == right, "Correlated square needs identical operand")
        low = 0 if left[0] <= 0 <= left[1] else min(left[0] ** 2, left[1] ** 2)
        high = max(left[0] ** 2, left[1] ** 2)
    require(-(1 << 143) <= low <= high < 1 << 143, "Signed full144 product may overflow")
    return check_word((low // S, high // S))


def polynomial_intervals(target, site, remainder, source=None):
    source = producers(target) if source is None else source
    cache = {site["remainder"]: check_word(remainder)}
    products = []

    def visit(value):
        if value in cache:
            return cache[value]
        item, _ = source[value]
        if item["op"] == "const":
            result = (signed(item["params"]["value"]),) * 2
        else:
            require(item["op"] in ("add", "mul"), "Actual stock polynomial arithmetic")
            a, b = [visit(arg) for arg in item["args"]]
            if item["op"] == "add":
                result = (a[0] + b[0], a[1] + b[1])
            else:
                result = multiply_bounds(a, b, item["args"][0] == item["args"][1])
                products.append(
                    {"value": value, "inputs": [list(a), list(b)], "product144_safe": True}
                )
        cache[value] = check_word(result)
        return result

    return visit(site["polynomial"]), cache, products


def native_support(scope):
    na, nt = scope["assets"], scope["dates"]
    m, h, k = na * nt, scope["barrier_raw"], scope["strike_raw"]
    ca, cd = scope["average_coefficient"], scope["discount_coefficient"]
    require(0 < ca < S and 0 < cd <= S and 0 <= k < h, "Original positive discounted call")
    total = m * h - nt
    average = ca * total // S
    payoff = cd * max(average - k, 0) // S
    require(0 <= payoff < 40 * S, "Actual rounded native Asian/discount support must be below40")
    return {
        "strict_alive_stock_sum_raw_upper": total,
        "surviving_rounded_asian_average_raw_upper": average,
        "native_payoff_raw_bounds": [0, payoff],
        "native_payoff_dollars_bounds_exact": [[0, 1], pair(Fraction(payoff, S))],
        "average_coefficient_rounding_charged": True,
        "actual_strict_basket_floor_below_H": True,
        "native_support_below40": True,
    }


def financial_word_bounds(
    target, scope, financial_values, normal_bound, exp_proof, check_budget=None
):
    """All dead-path financial operations; use proved correlated stock subgraphs."""
    source = producers(target)
    require(type(normal_bound) is int and normal_bound > 0, "Outward native normal integer bound")
    overrides = {value: (-normal_bound, normal_bound) for value in scope["normal_values"]}
    ref = scope["sites"][0]
    ref_hash, _, ref_tokens = polynomial_template(target, ref, source)
    # JSON records use string IDs; normalize them without dropping any actual value.
    token_bounds = {
        ref_tokens[int(value)]: tuple(bounds)
        for value, bounds in exp_proof["polynomial_value_union_bounds"].items()
        if int(value) in ref_tokens
    }
    for site in scope["sites"]:
        template, values, tokens = polynomial_template(target, site, source)
        require(
            template == ref_hash
            and (site["inverse_ln2"], site["ln2"]) == (ref["inverse_ln2"], ref["ln2"]),
            "All actual stock exponential templates/literals",
        )
        for value in values:
            overrides[value] = token_bounds[tokens[value]]
        aliases = {
            "stock": "stock_raw_bounds",
            "remainder": "remainder_raw_bounds",
            "exponent": "exponent_bounds",
            "inverse_value": "inverse_value_raw_bounds",
            "scaled_exponent": "scaled_exponent_raw_bounds",
            "ln_value": "ln_value_raw_bounds",
        }
        for role, field in aliases.items():
            overrides[site[role]] = tuple(exp_proof[field])
        overrides[site["clipped"]] = (scope["lower_log_raw"], scope["upper_log_raw"])
    cache, rows = {}, []

    def visit(value):
        if value in cache:
            return cache[value]
        if value in overrides:
            result = overrides[value]
            kind = "proved_same_domain_stock_or_scalar_boundary"
        else:
            item, slot = source[value]
            require(slot == 0 and len(item["out"]) == 1, "Original scalar financial arithmetic")
            op = item["op"]
            args = [visit(arg) for arg in item["args"]]
            kind = op
            if op == "const":
                result = (signed(item["params"]["value"]),) * 2
            elif op == "add":
                result = (args[0][0] + args[1][0], args[0][1] + args[1][1])
            elif op == "sub":
                result = (args[0][0] - args[1][1], args[0][1] - args[1][0])
            elif op == "cmul":
                c = signed(item["params"]["c"])
                result = multiply_bounds(args[0], (c, c))
            elif op == "mul":
                result = multiply_bounds(args[0], args[1], item["args"][0] == item["args"][1])
            elif op == "lt":
                result = (0, 1)
            elif op == "select":
                result = (min(args[1][0], args[2][0]), max(args[1][1], args[2][1]))
            elif op == "positive":
                result = (max(0, args[0][0]), max(0, args[0][1]))
            else:
                raise ValueError("Uncertified financial operation or extra exponential: " + op)
        cache[value] = check_word(result)
        rows.append({"value": value, "raw_bounds": list(result), "proof": kind})
        return result

    for value in financial_values:
        if check_budget is not None:
            check_budget()
        visit(value)
    require(
        all(value in cache for value in financial_values), "Every eager financial value covered"
    )
    require(
        all(cache[site["stock"]][0] > 0 for site in scope["sites"]),
        "All stock values strictly positive",
    )
    return {
        "all_dead_path_financial_values": len(financial_values),
        "values": rows,
        "all_original_signed72_and_product144_safe": True,
        "all_stock_sites_template_bound": len(scope["sites"]),
        "source_aware_no_modular_wrap_proof": True,
    }
