"""Counterexample-oriented checks of the proof-producing range interpreter."""

from itertools import product
import math
import json
from pathlib import Path

import pytest

from research.controlled_priority_completion.range_audit import (
    Audit,
    WitnessGraph,
    build,
    ranges_for_compiled,
)
from research.controlled_source_completion.ir import Graph, evaluate
from research.compound_feasibility.model import MODELS


def check_trace(data, audit, inputs):
    _, trace = evaluate(data, inputs, trace=True)
    for ident, raw in enumerate(trace):
        actual = raw - (1 << data["width"]) if raw >= 1 << (data["width"] - 1) else raw
        lo, hi = audit.bounds[ident]
        assert lo <= actual <= hi, (ident, actual, (lo, hi), audit.nodes[ident])


@pytest.mark.parametrize("op", ["add", "sub", "mul", "divide", "shift"])
def test_integer_operations_exhaustive_small_width(op):
    g = Graph(f=2, integer_bits=4)
    u, v = g.input("u", 4), g.input("v", 4)
    a, b = g.sub(u, g.const_int(8)), g.sub(v, g.const_int(8))
    g.node(op, [a, b])
    data = g.as_dict()
    audit = Audit(data).run()
    for x, y in product(range(16), repeat=2):
        check_trace(data, audit, {"u": x, "v": y})


@pytest.mark.parametrize("kind", ["log", "exp", "cdf", "cos_unit", "atan"])
def test_structural_lemmas_exhaustive_reduced_precision(kind):
    g = WitnessGraph(f=10, integer_bits=6)
    u = g.input("u", 10)
    x = u if kind in ("log", "cos_unit") else g.sub(u, g.const_int(512))
    out = getattr(g, kind)(x)
    g.outputs = {"out": out}
    data = g.as_dict()
    audit = Audit(data, g.witnesses).run()
    for value in range(1024):
        check_trace(data, audit, {"u": value})


def test_full_width_unsigned_left_shift_has_signed_modular_semantics():
    g = Graph(f=2, integer_bits=4)
    raw = g.input("u", 4)
    x = g.sub(raw, g.const_int(8))
    g.bits(x, -2)
    data = g.as_dict()
    audit = Audit(data).run()
    for value in range(16):
        check_trace(data, audit, {"u": value})


@pytest.mark.parametrize("model", [MODELS[0], MODELS[-1]], ids=["C4", "H8"])
def test_constructed_graph_unchanged_and_corner_traces_contained(model):
    from research.controlled_source_completion.finance import build_finance

    graph = build(model)
    data = graph.as_dict()
    assert data == build_finance(model, f=40, q=32).as_dict()
    audit = Audit(data, graph.witnesses).run()
    for radial, angle in product((0, (1 << 31), (1 << 32) - 1), (0, (1 << 29), (1 << 32) - 1)):
        inputs = {
            "uniform_%d" % i: radial if i % 2 == 0 else angle for i in range(len(graph.inputs))
        }
        check_trace(data, audit, inputs)
    assert not audit.unresolved
    assert audit.lemmas["moment_ratio"] == 1
    if model.name == "H8":
        assert audit.lemmas["dispersion"] == 1
    path = (
        Path("results/controlled_completion_followup/arithmetic_v1/compile_v2")
        / (model.name + "_f40")
        / "target.json"
    )
    target = json.loads(path.read_text())
    certificate = ranges_for_compiled(target, model)
    assert certificate["guaranteed"] and not certificate["signed_overflow_sites"]
    assert len(certificate["bounds"]) == sum(len(n["out"]) for n in target["nodes"])
    changed = json.loads(json.dumps(target))
    next(n for n in changed["nodes"] if n["op"] == "const")["params"]["value"] += 1
    with pytest.raises(ValueError):
        ranges_for_compiled(changed, model)


@pytest.mark.parametrize("assets", [4, 8])
def test_correlated_financial_lemmas_include_fixed_point_rounding(assets):
    q, minimum = 256, 17
    common, extra, rate = 285, 31, 264
    ratio_bound = (common + extra) * (minimum + 1) ** 2 // (minimum * minimum - q)
    dispersion_bound = math.isqrt(
        q * q * ((assets - 1) * minimum**2 + 2 * assets * minimum + assets + q) // minimum**2
    )
    for stocks in product((17, 18, 100, 1024) if assets == 4 else (17, 1024), repeat=assets):
        total = sum(stocks)
        basket = total // assets
        sqsum = sum(x * x // q for x in stocks)
        second = ((total * total // q) * common // q + sqsum * extra // q) // (assets * assets)
        ea = basket * rate // q
        ratio = second * q // (ea * ea // q)
        variance = max(0, sqsum // assets - basket * basket // q)
        dispersion = math.isqrt(variance * q) * q // basket
        assert ratio <= ratio_bound
        assert dispersion <= dispersion_bound
