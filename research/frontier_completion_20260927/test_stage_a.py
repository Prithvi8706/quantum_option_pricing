"""Protect immutable run archives; validate score semantics on a small real source."""

import json

import pytest

from research.controlled_source_completion.compiler import compile_graph, resolve_library
from research.controlled_source_completion.ir import Graph
from research.frontier_completion_20260927.stage_a import exact_dag, prepare_output


def test_refuse_existing_evidence(tmp_path):
    directory = tmp_path / "run"
    prepare_output(directory)
    artifact = directory / "evidence.json"
    artifact.write_text('{"immutable": true}')
    with pytest.raises(FileExistsError):
        prepare_output(directory)
    assert json.loads(artifact.read_text()) == {"immutable": True}


def test_dependency_accounting_uses_call_specific_costs(tmp_path):
    graph = Graph(2, 4)
    x = graph.input("x", 6)
    # Shared input; different constant-multiply leaves must be charged separately.
    a, b = graph.cmul(x, 0.5), graph.cmul(x, 0.75)
    graph.outputs = {"sum": graph.add(a, b)}
    source, _ = compile_graph(graph.as_dict(), tmp_path)
    lib = resolve_library(source)
    costs = [
        json.loads((lib / (c["leaf"] + ".json")).read_text())["resources"]
        for c in source["forward_calls"]
    ]
    assert costs[0]["t_depth"] != costs[1]["t_depth"]
    result = exact_dag(source)
    assert result["forward_dependency_t_depth"] == max(
        costs[0]["t_depth"], costs[1]["t_depth"]
    ) + costs[2]["t_depth"]
    assert result["forward_t_count"] == sum(c["t_count"] for c in costs)
