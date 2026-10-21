"""Exact scalar arithmetic and new-site guard fixtures; never run on import."""

from copy import deepcopy
from fractions import Fraction

import pytest

from research.controlled_source_completion.ir import Graph, evaluate
from research.limitation_program_20261001.quantile_central_certificate_v2 import (
    mathematical_native_central_word,
)
from research.limitation_program_20261001.quantile_tail_certificate import (
    mathematical_native_rational_word,
)
from research.limitation_program_20261001.quantile_transform_native import (
    mathematical_transform_word,
)
from research.limitation_program_20261001.scalar_quantile_ir import (
    PROGRAM,
    S,
    W,
    MASK,
    FIXTURE_WORDS,
    K_TAIL,
    K_CENTRAL,
    P_TAIL,
    P_CENTRAL,
    Q_CENTRAL,
    branch_constants,
    bind_site_proofs,
    build_scalar_graph,
    fingerprint,
    load_literals,
    read,
    validate_recipe,
    validate_site_binding,
)


@pytest.fixture(scope="module")
def scalar():
    literals = load_literals()
    target, bindings = build_scalar_graph(literals)
    inputs = {
        "central": read(PROGRAM / "A02_quantile_central_run002/central_certificate.json"),
        "tail": read(PROGRAM / "A02_quantile_tail_run001/tail_certificate.json"),
        "transform": read(
            PROGRAM / "A02_quantile_transform_run002/native_transform_certificate.json"
        ),
    }
    proofs = bind_site_proofs(target, bindings, literals, **inputs)
    return target, bindings, literals, proofs, inputs


def signed(raw):
    return raw - (1 << W) if raw >= 1 << (W - 1) else raw


def independent_integer_reference(raw, literals):
    p = min((2 * raw + 1) << 7, S - ((2 * raw + 1) << 7))
    if Fraction(p, S) >= Fraction(3, 40):
        return mathematical_native_central_word(raw)
    transformed = mathematical_transform_word(raw, literals["log_table"], literals["ln2_raw"])
    return mathematical_native_rational_word(transformed["transform_r_raw"], negative=raw < 1 << 31)


def test_integer_boundary_dispatch_and_guard_domains_exact():
    constants = branch_constants()
    assert P_TAIL < Fraction(3 * S, 40) < P_CENTRAL
    assert P_TAIL < constants["P_BRANCH"] < P_CENTRAL
    assert P_TAIL % 256 == P_CENTRAL % 256 == 128
    assert constants["P_BRANCH"] % 256 != 128
    assert Q_CENTRAL == S // 2 - P_CENTRAL
    assert Q_CENTRAL < Fraction(17 * S, 40)


@pytest.mark.parametrize("raw", FIXTURE_WORDS)
def test_fixed_scalar_ssa_equals_independent_archived_integer_function(raw, scalar):
    target, bindings, literals, _, _ = scalar
    _, trace = evaluate(target, {"k": raw}, trace=True)
    assert signed(trace[bindings["output"]]) == independent_integer_reference(raw, literals)
    p = min((2 * raw + 1) << 7, S - ((2 * raw + 1) << 7))
    assert trace[bindings["tail"]] == int(Fraction(p, S) < Fraction(3, 40))
    assert trace[bindings["negative"]] == int(raw < 1 << 31)


def test_eager_unused_branches_and_native_high_bits_are_safe_at_fixed_endpoints(scalar):
    target, bindings, _, _, _ = scalar
    for raw in FIXTURE_WORDS:
        _, trace = evaluate(target, {"k": raw}, trace=True)
        assert 0 <= trace[bindings["central_qguard"]] <= Q_CENTRAL
        assert 128 <= trace[bindings["tail_pguard"]] <= P_TAIL
        assert trace[bindings["tail_pguard"]] % 256 == 128
        assert signed(trace[bindings["central_r"]]) >= 0
        assert 0 < trace[bindings["sqrt_argument"]] < 1 << 45
        assert 0 <= signed(trace[bindings["tail_r"]]) < Fraction(321 * S, 100)
        assert S <= trace[bindings["central_B"]] < 1 << 64
        assert S <= trace[bindings["tail_B"]] < 1 << 64
        assert trace[bindings["guarded_divisor"]] == trace[bindings["selected_denominator"]]
        assert 0 <= trace[bindings["selected_numerator"]] < 1 << 72
        if trace[bindings["tail"]]:
            assert trace[bindings["tail_pguard"]] == trace[bindings["probability"]]
        else:
            assert trace[bindings["central_qguard"]] == trace[bindings["qabs"]]


@pytest.mark.parametrize("raw", [0, K_TAIL, K_CENTRAL, (1 << 31) - 1])
def test_scalar_sign_restoration_is_exact_mirror_symmetry(raw, scalar):
    target, bindings, _, _, _ = scalar
    values = []
    for word in (raw, (1 << 32) - 1 - raw):
        _, trace = evaluate(target, {"k": word}, trace=True)
        values.append(signed(trace[bindings["output"]]))
    assert values[0] == -values[1]


def test_floor_order_counterexample_and_exact_signed_restoration():
    scale, q, a, b = 16, 6, 56, 24
    accepted = (((q * a) // scale) * scale) // b
    divide_first = (q * ((a * scale) // b)) // scale
    assert accepted == 14 and divide_first == 13
    magnitude = 3
    assert (-magnitude) & MASK == (1 << W) - magnitude
    assert ((-magnitude) & MASK) >> (W - 1) == 1


def test_graph_never_uses_floating_constant_or_coefficient_regeneration(monkeypatch, scalar):
    import research.controlled_source_completion.ir as ir

    def forbidden(*args, **kwargs):
        raise AssertionError("Float convenience API or coefficient regeneration reached")

    for method in ("c", "cmul", "interpolate", "log"):
        monkeypatch.setattr(Graph, method, forbidden)
    monkeypatch.setattr(ir, "coefficients", forbidden)
    target, bindings = build_scalar_graph(scalar[2])
    assert target == scalar[0] and bindings == scalar[1]


def test_whole_graph_proof_binds_exact_new_divider_and_sqrt_arguments(scalar):
    target, bindings, literals, proofs, inputs = scalar
    assert validate_site_binding(target, bindings, literals, proofs, inputs)
    assert proofs["target_sha256"] == fingerprint(target)
    assert proofs["sites"]["divide"]["args"] == [
        bindings["selected_numerator"],
        bindings["guarded_divisor"],
    ]
    assert proofs["sites"]["sqrt"]["args"] == [bindings["sqrt_argument"]]
    assert proofs["sites"]["divide"]["input_contract"] == {"unsigned_denominator_bits": 64}


@pytest.mark.parametrize("kind", ["guard", "multiply_order", "sqrt_arg"])
def test_native_recipe_or_operand_producer_forgery_rejected(kind, scalar):
    target, bindings, literals, proofs, inputs = deepcopy(scalar)
    producers = {value: node for node in target["nodes"] for value in node["out"]}
    if kind == "guard":
        producers[bindings["tail_pguard"]]["args"][2] = bindings["probability"]
    elif kind == "multiply_order":
        producers[bindings["central_numerator"]]["args"] = [bindings["qabs"], bindings["central_A"]]
    else:
        producers[bindings["square_root"]]["args"] = [bindings["q"]]
    with pytest.raises(ValueError):
        validate_site_binding(target, bindings, literals, proofs, inputs)


@pytest.mark.parametrize("kind", ["denominator", "numerator", "sqrt"])
def test_typed_operand_limit_forgery_rejected_against_trusted_full_inputs(kind, scalar):
    target, bindings, literals, proofs, inputs = deepcopy(scalar)
    if kind == "denominator":
        proofs["sites"]["divide"]["denominator_upper_exact"] = [1 << 64, 1]
    elif kind == "numerator":
        proofs["sites"]["divide"]["unsigned_numerator_upper_exact"] = [1 << 72, 1]
    else:
        proofs["sites"]["sqrt"]["unsigned_input_upper_exact"] = [1 << 46, 1]
    with pytest.raises(ValueError):
        validate_site_binding(target, bindings, literals, proofs, inputs)


@pytest.mark.parametrize("kind", ["central", "tail", "log"])
def test_raw_literal_mutation_rejected_against_archived_proof_inputs(kind, scalar):
    target, bindings, literals, _, inputs = deepcopy(scalar)
    if kind == "central":
        literals["central_A_raw"][0] += 1
    elif kind == "tail":
        literals["tail_B_raw"][1] += 1
    else:
        literals["log_table"][0][0] += 1
    with pytest.raises(ValueError):
        bind_site_proofs(target, bindings, literals, **inputs)


def test_one_shared_division_both_guards_and_full_named_output_are_in_actual_ssa(scalar):
    target, bindings, literals, _, _ = scalar
    producers = {value: node for node in target["nodes"] for value in node["out"]}
    assert sum(node["op"] == "divide" for node in target["nodes"]) == 1
    assert sum(node["op"] == "sqrt" for node in target["nodes"]) == 1
    assert producers[bindings["selected_numerator"]]["args"] == [
        bindings["tail"],
        bindings["tail_A"],
        bindings["central_numerator"],
    ]
    assert producers[bindings["central_numerator"]]["op"] == "mul"
    assert producers[bindings["central_numerator"]]["args"] == [
        bindings["central_qguard"],
        bindings["central_A"],
    ]
    assert producers[bindings["central_qguard"]]["op"] == "select"
    assert producers[bindings["tail_pguard"]]["op"] == "select"
    assert target["outputs"] == {"Z": bindings["output"]}
    assert target["inputs"] == [bindings["raw_input"]]
    assert validate_recipe(target, bindings, literals) == fingerprint(target)
