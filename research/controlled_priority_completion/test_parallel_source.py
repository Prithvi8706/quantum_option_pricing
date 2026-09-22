"""Dependency ordering, shared-control copies and nonzero-output cleanup."""

import pytest

from research.controlled_priority_completion.parallel_source import execute, make_schedule
from research.controlled_source_completion.compiler import compile_graph
from research.controlled_source_completion.ir import Graph, evaluate


@pytest.mark.parametrize("limit", [1, 2, None])
def test_parallel_aliases_and_inverse(tmp_path, limit):
    g = Graph(2, 4)
    a, b = g.input("a", 6), g.input("b", 6)
    square, product, sum_ = g.mul(a, a), g.mul(a, b), g.add(a, b)
    value = g.sub(g.add(square, product), sum_)
    g.outputs = dict(value=value, alias=value)
    source, _ = compile_graph(g.as_dict(), tmp_path)
    schedule = make_schedule(source, limit)
    for a in (0, 1, 17, 31, 32, 63):
        for b in (0, 1, 17, 31, 32, 63):
            given = dict(a=a, b=b)
            _, values = evaluate(g.as_dict(), given, True)
            got = execute(source, schedule, given, dict(value=37, alias=42))
            assert got["values"] == dict(value=values[value] ^ 37, alias=values[value] ^ 42)
            assert got["all_input_and_workspace_bits_restored"]
    assert schedule["resources"]["t_count"] == source["resources"]["t_count"]
    if limit is None:
        # a is copied twice for its square, once for its product and once for sum.
        assert schedule["groups"][0]["copy_rounds"] == 4
        assert schedule["resources"]["t_depth"] < source["resources"]["t_depth"]


def test_reject_zero_parallelism(tmp_path):
    g = Graph(2, 4)
    a = g.input("a", 6)
    g.outputs = dict(a=g.pos(a))
    source, _ = compile_graph(g.as_dict(), tmp_path)
    with pytest.raises(ValueError):
        make_schedule(source, 0)
