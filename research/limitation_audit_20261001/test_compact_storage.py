"""Check exact width proofs and the emitted circuit's compact binding."""

import pytest

from research.controlled_source_completion.compact_storage import (
    active_masks, compact_plan, execute_compact, narrow_comparison,
)
from research.controlled_source_completion.compiler import compile_graph
from research.controlled_source_completion.ir import Graph, evaluate
from research.controlled_source_completion.primitives import basis_run, build, resources


def test_emitted_narrow_flag():
    p, args, outs = narrow_comparison(4)
    for a in range(16):
        for b in range(16):
            expected = int((a if a < 8 else a - 16) < (b if b < 8 else b - 16))
            for initial in (0, 1):
                actual, clean, preserved, _ = basis_run(p, args, outs, [a, b], [initial])
                assert (actual, clean, preserved) == ([initial ^ expected], True, True)
    old = build("lt", 72, 40)[0]
    new = narrow_comparison(72)[0]
    assert resources(new)["qubits"] == resources(old)["qubits"] - 71
    assert resources(new)["t_count"] == resources(old)["t_count"]


def test_compact_complete_graph_all_inputs_and_nonzero_outputs(tmp_path):
    graph = Graph(0, 4)
    a, b = graph.input("a", 4), graph.input("b", 2)
    less = graph.lt(a, b)
    index = graph.bits(a, 1, 2)
    graph.tables["small"] = [[0], [3], [7], [2]]
    loaded = graph.node("lookup", (index,), {"bits": 2, "table": "small"})
    positive = graph.pos(a)
    total = graph.add(b, loaded)
    signed_bits = graph.bits(a, 7, 4, signed=True)
    graph.outputs = {"flag": less, "Y": graph.select(less, total, positive), "sign": signed_bits}
    target = graph.as_dict()
    source, _ = compile_graph(target, tmp_path)
    plan = compact_plan(target, source)
    masks, _ = active_masks(target)
    assert plan["logical_qubits"] < source["resources"]["logical_qubits"]
    assert plan["widths"][less] == 1 and plan["widths"][index] == 2
    initial = {"flag": 13, "Y": 7, "sign": 9}
    for a in range(16):
        for b in range(4):
            inputs = {"a": a, "b": b}
            _, values = evaluate(target, inputs, True)
            assert all(value & ~masks[v] == 0 for v, value in enumerate(values))
            actual = execute_compact(target, source, plan, inputs, initial)
            assert actual["inputs_and_workspace_restored"]
            assert actual["values"] == {name: values[v] ^ initial[name]
                                       for name, v in graph.outputs.items()}
    with pytest.raises(ValueError, match="promise"):
        execute_compact(target, source, plan, {"a": 0, "b": 4})
