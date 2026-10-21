"""Independent exhaustive containment checks for conservative integer ranges."""

import copy

import pytest

from research.controlled_source_completion.ir import Graph, evaluate
from research.limitation_program_20261001.interval_bounds import bound_graph


def contain(target, samples):
    intervals, rules = bound_graph(target)
    width = target["width"]
    for sample in samples:
        _, trace = evaluate(target, sample, True)
        for value, raw in enumerate(trace):
            signed = raw - (1 << width) if raw & (1 << (width - 1)) else raw
            lo, hi = intervals[value]
            assert lo <= signed <= hi, (value, sample, signed, intervals[value], rules[value])
    return intervals, rules


@pytest.mark.parametrize("width", range(1, 6))
def test_every_small_signed_input_and_fraction(width):
    for fraction in range(width + 1):
        graph = Graph(fraction, width - fraction)
        a, b = graph.input("a", width), graph.input("b", width)
        graph.add(a, b)
        graph.sub(a, b)
        graph.mul(a, b)
        graph.node("cmul", (a,), {"c": -7})
        graph.node("cmul", (a,), {"c": 5})
        graph.maximum(a, b)
        graph.minimum(a, b)
        graph.select(a, a, b)
        graph.node("positive", (a,))
        graph.node("sqrt", (a,))
        graph.node("msb", (a,))
        graph.shift(a, b)
        graph.const_int(1 << (width + 3))
        for shift in (-width, -1, 0, 1, width):
            for bits in (max(0, width - 1), width):
                graph.bits(a, shift, bits, signed=False)
                graph.bits(a, shift, bits, signed=True)
        graph.outputs = {"a": a}
        contain(
            graph.as_dict(),
            ({"a": x, "b": y} for x in range(1 << width) for y in range(1 << width)),
        )


def normalization_graph(offset=8):
    graph = Graph(8, 4)
    raw = graph.input("x", 10)
    positive = graph.maximum(raw, graph.const_int(1))
    top = graph.node("msb", (positive,))
    exponent = graph.sub(top, graph.const_int(offset))
    normalized = graph.shift(positive, graph.neg(exponent))
    graph.outputs = {"normalized": normalized}
    return graph


def test_msb_normalization_is_proved_for_every_input():
    graph = normalization_graph()
    intervals, rules = contain(graph.as_dict(), ({"x": x} for x in range(1024)))
    value = graph.outputs["normalized"]
    assert intervals[value] == (256, 511)
    assert rules[value] == "same-SSA MSB normalization"


def test_wrong_normalization_literal_does_not_receive_special_bound():
    graph = normalization_graph(offset=7)
    _, rules = contain(graph.as_dict(), ({"x": x} for x in range(1024)))
    assert rules[graph.outputs["normalized"]] != "same-SSA MSB normalization"


def local_graph(offset=264):
    graph = Graph(8, 4)
    raw = graph.input("x", 8)
    x = graph.add(raw, graph.const_int(256))
    index = graph.bits(graph.sub(x, graph.const_int(256)), 4, 4)
    center = graph.add(graph.bits(index, -4), graph.const_int(offset))
    local = graph.sub(x, center)
    graph.outputs = {"local": local}
    return graph


def test_bin_local_residual_covers_all_values():
    graph = local_graph()
    intervals, rules = contain(graph.as_dict(), ({"x": x} for x in range(256)))
    value = graph.outputs["local"]
    assert intervals[value] == (-8, 7)
    assert rules[value] == "same-SSA bin-local residual"


def test_changed_bin_center_does_not_receive_special_bound():
    graph = local_graph(offset=263)
    _, rules = contain(graph.as_dict(), ({"x": x} for x in range(256)))
    assert rules[graph.outputs["local"]] != "same-SSA bin-local residual"


def test_bounds_snapshot_does_not_mutate_target():
    target = local_graph().as_dict()
    original = copy.deepcopy(target)
    bound_graph(target)
    assert target == original
