"""One exact q32/native72 AS241 SSA graph; no construction occurs on import.

Both branches are eagerly evaluated with paid guards. Positive central
magnitude multiplication precedes the one shared unsigned division.
"""

from copy import deepcopy
from fractions import Fraction
import hashlib
import json
from pathlib import Path

from research.controlled_source_completion.ir import Graph


ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
S = 1 << 40
W = 72
F = 40
MASK = (1 << W) - 1
K_TAIL = 322122546
K_CENTRAL = 322122547
P_TAIL = (2 * K_TAIL + 1) << 7
P_CENTRAL = (2 * K_CENTRAL + 1) << 7
Q_CENTRAL = S // 2 - P_CENTRAL
FIXTURE_WORDS = (
    0,
    (1 << 32) - 1,
    K_TAIL,
    K_CENTRAL,
    (1 << 32) - 1 - K_TAIL,
    (1 << 32) - 1 - K_CENTRAL,
    (1 << 31) - 1,
    1 << 31,
)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def fingerprint(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def nearest_integer(value):
    value = Fraction(value)
    lower = value.numerator // value.denominator
    delta = value - lower
    return lower + int(delta > Fraction(1, 2) or (delta == Fraction(1, 2) and lower % 2))


def load_literals():
    central_path = PROGRAM / "A02_quantile_central_run002/central_certificate.json"
    tail_path = PROGRAM / "A02_quantile_tail_run001/tail_certificate.json"
    pair_path = PROGRAM / "C06_pair_run001/certificate.json"
    central, tail, pair = map(read, (central_path, tail_path, pair_path))
    if central.get("certified") is not True or tail.get("certified") is not True:
        raise ValueError("Successful frozen central and ordinary-tail certificates required")
    binding = pair["source_bindings"]
    targets = {case: read(ROOT / entry["target"]) for case, entry in binding.items()}
    if (
        targets["B4x12"]["tables"]["log"] != targets["B8x52"]["tables"]["log"]
        or any(target["width"] != W or target["fraction_bits"] != F for target in targets.values())
        or binding["B4x12"]["literal_ln2"] != binding["B8x52"]["literal_ln2"]
    ):
        raise ValueError("Original archived log source interfaces differ")
    literals = {
        "width": W,
        "fraction_bits": F,
        "uniform_bits": 32,
        "central_A_raw": central["native_arithmetic"]["native_A_raw_ascending"],
        "central_B_raw": central["native_arithmetic"]["native_B_raw_ascending"],
        "central_rconstant_raw": central["native_arithmetic"]["rconstant_raw"],
        "tail_A_raw": tail["native_interface"]["native_A_raw_ascending"],
        "tail_B_raw": tail["native_interface"]["native_B_raw_ascending"],
        "log_table": targets["B4x12"]["tables"]["log"],
        "ln2_raw": binding["B4x12"]["literal_ln2"],
        "tail_shift_raw": 1759218604442,
    }
    validate_literals(literals)
    return deepcopy(literals)


def validate_literals(literals):
    if (literals.get("width"), literals.get("fraction_bits"), literals.get("uniform_bits")) != (
        W,
        F,
        32,
    ):
        raise ValueError("Fixed native72/f40/q32 scalar interface required")
    for name in ("central_A_raw", "central_B_raw", "tail_A_raw", "tail_B_raw"):
        words = literals[name]
        if len(words) != 8 or any(
            type(word) is not int or not 0 < word < 1 << 71 for word in words
        ):
            raise ValueError("Eight positive archived raw rational coefficients required")
    table = literals["log_table"]
    if len(table) != 32 or any(
        len(row) != 9
        or any(type(word) is not int or not -(1 << 71) <= word < 1 << 71 for word in row)
        for row in table
    ):
        raise ValueError("Archived32-by9 signed log table required")
    if (
        literals["ln2_raw"] != 762123384786
        or literals["central_rconstant_raw"] != 198599287768
        or literals["tail_shift_raw"] != 1759218604442
        or literals["central_B_raw"][0] != S
        or literals["tail_B_raw"][0] != S
    ):
        raise ValueError("Exact frozen constants or denominator constant changed")


def branch_constants():
    threshold = nearest_integer(Fraction(3 * S, 40))
    if not (
        P_TAIL < Fraction(3 * S, 40) < P_CENTRAL
        and P_TAIL < threshold < P_CENTRAL
        and P_CENTRAL - P_TAIL == 256
        and P_TAIL % 256 == P_CENTRAL % 256 == 128
        and threshold % 256 != 128
        and 0 < Q_CENTRAL < Fraction(17 * S, 40)
    ):
        raise ArithmeticError("Actual q32 adjacent branch words do not separate exact3/40")
    return {"P_TAIL": P_TAIL, "P_CENTRAL": P_CENTRAL, "Q_CENTRAL": Q_CENTRAL, "P_BRANCH": threshold}


def _horner(graph, argument, coefficients):
    value = graph.const_int(coefficients[-1])
    for coefficient in reversed(coefficients[:-1]):
        value = graph.add(graph.mul(value, argument), graph.const_int(coefficient))
    return value


def _archived_log(graph, value, literals, zero):
    """Original normalization/Horner nodes, with exact archive table injection."""
    guarded = graph.maximum(value, graph.const_int(1))
    top = graph.node("msb", (guarded,))
    exponent = graph.sub(top, graph.const_int(F))
    mantissa = graph.shift(guarded, graph.sub(zero, exponent))
    clipped = graph.clip(mantissa, graph.const_int(S), graph.const_int(2 * S - 1))
    index = graph.bits(graph.sub(clipped, graph.const_int(S)), F - 5, width=5)
    center = graph.add(graph.bits(index, -(F - 5)), graph.const_int(S + (1 << (F - 6))))
    local = graph.sub(clipped, center)
    graph.tables["log"] = deepcopy(literals["log_table"])
    coefficients = graph.node("lookup", (index,), {"table": "log", "bits": 5}, nout=9)
    value = coefficients[-1]
    for coefficient in reversed(coefficients[:-1]):
        value = graph.add(graph.mul(value, local), coefficient)
    scaled_exponent = graph.bits(exponent, -F)
    exponent_product = graph.node("cmul", (scaled_exponent,), {"c": literals["ln2_raw"]})
    output = graph.add(value, exponent_product)
    return output, {
        "log_guarded_input": guarded,
        "log_exponent": exponent,
        "log_mantissa": mantissa,
        "log_clipped_mantissa": clipped,
        "log_index": index,
        "log_local": local,
        "log_output": output,
        "log_scaled_exponent": scaled_exponent,
        "log_exponent_product": exponent_product,
    }


def build_scalar_graph(literals=None):
    """Deferred graph construction; call only after the prospective freeze."""
    literals = load_literals() if literals is None else deepcopy(literals)
    validate_literals(literals)
    constants = branch_constants()
    graph = Graph(f=F, integer_bits=W - F)
    raw = graph.input("k", 32, "uniform")
    zero, scale, half = (graph.const_int(value) for value in (0, S, S // 2))
    uniform = graph.add(graph.bits(raw, -8), graph.const_int(128))
    q = graph.sub(uniform, half)
    negative = graph.lt(uniform, half)
    magnitude = graph.select(negative, graph.sub(zero, q), q)
    probability = graph.minimum(uniform, graph.sub(scale, uniform))
    tail = graph.lt(probability, graph.const_int(constants["P_BRANCH"]))
    central_q = graph.minimum(magnitude, graph.const_int(constants["Q_CENTRAL"]))
    tail_p = graph.minimum(probability, graph.const_int(constants["P_TAIL"]))
    central_r = graph.sub(
        graph.const_int(literals["central_rconstant_raw"]), graph.mul(central_q, central_q)
    )
    central_a = _horner(graph, central_r, literals["central_A_raw"])
    central_b = _horner(graph, central_r, literals["central_B_raw"])
    central_numerator = graph.mul(central_q, central_a)
    log, log_bindings = _archived_log(graph, tail_p, literals, zero)
    negative_log = graph.sub(zero, log)
    sqrt_argument = graph.pos(negative_log)
    square_root = graph.node("sqrt", (sqrt_argument,))
    tail_r = graph.sub(square_root, graph.const_int(literals["tail_shift_raw"]))
    tail_a = _horner(graph, tail_r, literals["tail_A_raw"])
    tail_b = _horner(graph, tail_r, literals["tail_B_raw"])
    numerator = graph.select(tail, tail_a, central_numerator)
    denominator = graph.select(tail, tail_b, central_b)
    divisor = graph.maximum(denominator, graph.const_int(1))
    quotient = graph.node("divide", (numerator, divisor))
    output = graph.select(negative, graph.sub(zero, quotient), quotient)
    graph.outputs = {"Z": output}
    target = graph.as_dict()
    bindings = {
        "raw_input": raw,
        "uniform": uniform,
        "q": q,
        "negative": negative,
        "qabs": magnitude,
        "probability": probability,
        "tail": tail,
        "central_qguard": central_q,
        "tail_pguard": tail_p,
        "central_r": central_r,
        "central_A": central_a,
        "central_B": central_b,
        "central_numerator": central_numerator,
        **log_bindings,
        "negative_log": negative_log,
        "sqrt_argument": sqrt_argument,
        "square_root": square_root,
        "tail_r": tail_r,
        "tail_A": tail_a,
        "tail_B": tail_b,
        "selected_numerator": numerator,
        "selected_denominator": denominator,
        "guarded_divisor": divisor,
        "quotient": quotient,
        "output": output,
    }
    return target, bindings


def validate_recipe(target, bindings, literals):
    # Reconstruct the same fixed specification for admission; this is not an
    # alternative candidate or a numerical word/range proof.
    expected, expected_bindings = build_scalar_graph(literals)
    if canonical(target) != canonical(expected) or bindings != expected_bindings:
        raise ValueError("Whole scalar graph differs from the frozen eager guarded recipe")
    return fingerprint(target)


def bind_site_proofs(target, bindings, literals, central, tail, transform):
    """Bind prior all-input arithmetic lemmas to exact new native SSA sites."""
    if any(value.get("certified") is not True for value in (central, tail, transform)) or (
        transform.get("budget_censored") is not False
        or transform.get("actual_q32_native_transform_error_included") is not True
    ):
        raise ValueError("Successful all-input scalar arithmetic proof inputs required")
    if (
        literals["central_A_raw"] != central["native_arithmetic"]["native_A_raw_ascending"]
        or literals["central_B_raw"] != central["native_arithmetic"]["native_B_raw_ascending"]
        or literals["tail_A_raw"] != tail["native_interface"]["native_A_raw_ascending"]
        or literals["tail_B_raw"] != tail["native_interface"]["native_B_raw_ascending"]
        or literals["ln2_raw"] != transform["transform"]["original_ln2_raw"]
        or literals["log_table"]
        != [
            [check["literal_raw"] for check in row["coefficient_checks"]]
            for row in transform["transform"]["log_table_cells"]
        ]
    ):
        raise ValueError("Raw source coefficients differ from successful scalar proof inputs")
    graph_hash = validate_recipe(target, bindings, literals)
    central_native, tail_native = central["native_arithmetic"], tail["native_interface"]
    central_divisor = transform["central_denominator64"]
    if any(
        proof.get(flag) is not True
        for proof, flags in (
            (
                central_native,
                (
                    "signed72_stored_values_no_overflow",
                    "signed144_full_multiply_products_no_overflow",
                    "unsigned112_division_numerator_no_truncation",
                    "native_divider_clamp_inactive",
                ),
            ),
            (
                tail_native,
                (
                    "signed72_stored_values_no_overflow",
                    "signed144_full_products_no_overflow",
                    "unsigned112_dividend_no_truncation",
                    "unsigned64_denominator_no_truncation",
                    "native_denominator_floor_at_one_guard_inactive",
                ),
            ),
            (central_divisor, ("unsigned64_denominator_no_truncation",)),
        )
        for flag in flags
    ):
        raise ValueError("Complete prior native operand width guards required")
    denominator_upper = max(
        Fraction(*central_divisor["maximum_central_denominator_raw_upper_exact"]),
        Fraction(*tail_native["maximum_denominator_raw_upper_exact"]),
    )
    numerator_upper = (
        max(
            Fraction(*central_native["maximum_shifted_division_numerator_raw_upper_exact"]),
            Fraction(*tail_native["maximum_shifted_division_numerator_raw_upper_exact"]),
        )
        / S
    )
    sqrt_upper = Fraction(*transform["transform"]["native_negative_log_upper_exact"]) * S
    if not (denominator_upper < 1 << 64 and numerator_upper < 1 << 72 and sqrt_upper < 1 << 45):
        raise ArithmeticError("Selected native division/sqrt width interface unproved")
    return {
        "target_sha256": graph_hash,
        "literal_sha256": fingerprint(literals),
        "all_q32_inputs_covered_structurally": True,
        "range_certificate_based_on_sampled_inputs": False,
        "guarded_unused_branches_have_certified_domains": True,
        "selected_branch_guard_changes_result": False,
        "central_positive_multiply_before_divide_preserved": True,
        "shared_divide_count": 1,
        "sites": {
            "divide": {
                "value": bindings["quotient"],
                "args": [bindings["selected_numerator"], bindings["guarded_divisor"]],
                "unsigned_numerator_lower": 0,
                "unsigned_numerator_upper_exact": [
                    numerator_upper.numerator,
                    numerator_upper.denominator,
                ],
                "denominator_lower": S,
                "denominator_upper_exact": [
                    denominator_upper.numerator,
                    denominator_upper.denominator,
                ],
                "input_contract": {"unsigned_denominator_bits": 64},
                "raw_one_denominator_guard_inactive": True,
            },
            "sqrt": {
                "value": bindings["square_root"],
                "args": [bindings["sqrt_argument"]],
                "unsigned_input_upper_exact": [sqrt_upper.numerator, sqrt_upper.denominator],
                "input_contract": {"unsigned_input_bits": 46},
                "positive_guard_inactive": True,
            },
        },
        "semantic_proof": (
            "The exact full-graph recipe binds actual midpoint/sign/branch producers. "
            "Paid min guards map unused branches into actual archived domain inputs; "
            "selected inputs are unchanged. Central positive floor product, both Horner "
            "branches, native archived log/sqrt and exact sign restoration equal their "
            "already proved integer functions. Selection of positive numerator/divisor "
            "inherits the union of both native operand bounds before typed reuse."
        ),
        "native_financial_path_or_Box_Muller_law_adopted": False,
    }


def validate_site_binding(target, bindings, literals, proofs, proof_inputs):
    expected = bind_site_proofs(target, bindings, literals, **proof_inputs)
    if canonical(expected) != canonical(proofs):
        raise ValueError("Typed proof differs from trusted complete arithmetic proof inputs")
    if (
        proofs.get("target_sha256") != validate_recipe(target, bindings, literals)
        or proofs.get("literal_sha256") != fingerprint(literals)
        or proofs.get("all_q32_inputs_covered_structurally") is not True
        or proofs.get("range_certificate_based_on_sampled_inputs") is not False
        or proofs.get("central_positive_multiply_before_divide_preserved") is not True
    ):
        raise ValueError("Typed native proof is not bound to this full scalar graph")
    producers = {value: node for node in target["nodes"] for value in node["out"]}
    for operation in ("divide", "sqrt"):
        site = proofs["sites"][operation]
        node = producers[site["value"]]
        if node["op"] != operation or node["args"] != site["args"]:
            raise ValueError("Typed native site arguments differ from proof producer binding")
    divisor = proofs["sites"]["divide"]
    root = proofs["sites"]["sqrt"]
    if (
        divisor["input_contract"] != {"unsigned_denominator_bits": 64}
        or divisor["denominator_lower"] != S
        or Fraction(*divisor["denominator_upper_exact"]) >= 1 << 64
        or Fraction(*divisor["unsigned_numerator_upper_exact"]) >= 1 << 72
        or root["input_contract"] != {"unsigned_input_bits": 46}
        or Fraction(*root["unsigned_input_upper_exact"]) >= 1 << 46
    ):
        raise ValueError("Native site proof operand limits do not match adopted interfaces")
    return True
