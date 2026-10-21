"""Memory cap, dependency preservation, copied aliases and clean inversion."""

import pytest

from research.controlled_priority_completion.parallel_source import execute
from research.controlled_source_completion.budget_schedule import make_budget_schedule
from research.controlled_source_completion.compiler import compile_graph
from research.controlled_source_completion.ir import Graph, evaluate


def test_memory_capped_schedule_with_aliases(tmp_path):
    g = Graph(2, 4)
    a, b = g.input("a", 6), g.input("b", 6)
    square, product, total = g.mul(a, a), g.mul(a, b), g.add(a, b)
    g.outputs = {"v": g.add(g.sub(square, product), total), "alias": square}
    target = g.as_dict()
    source, _ = compile_graph(target, tmp_path)
    cap = source["resources"]["logical_qubits"]
    schedule = make_budget_schedule(source, cap)
    assert schedule["resources"]["logical_qubits"] <= cap
    scheduled = [i for batch in schedule["groups"] for i in batch["call_indices"]]
    assert sorted(scheduled) == list(range(len(source["forward_calls"])))
    for a in (0, 1, 17, 31, 32, 63):
        for b in (0, 1, 17, 31, 32, 63):
            inputs = {"a": a, "b": b}
            _, values = evaluate(target, inputs, True)
            initial = {"v": 21, "alias": 37}
            actual = execute(source, schedule, inputs, initial)
            assert actual["values"] == {name: values[v] ^ initial[name]
                                         for name, v in g.outputs.items()}
            assert actual["all_input_and_workspace_bits_restored"]
    with pytest.raises(ValueError, match="cap"):
        make_budget_schedule(source, cap - source["resources"]["max_reused_scratch_qubits"])
