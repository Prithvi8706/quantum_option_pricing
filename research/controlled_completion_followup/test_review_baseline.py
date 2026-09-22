"""Regression from the independent review: copies sharing controls are serial."""
import numpy as np
import pytest

from research.controlled_source_completion.compiler import compile_graph,resolve_library
from research.controlled_source_completion.ir import Graph
from research.controlled_source_completion.primitives import (
    array_gates, build, gate_resources,
)


@pytest.mark.parametrize('duplicate_output', [False, True])
def test_alias_copy_depth_bounds_flattened_emitted_schedule(tmp_path, duplicate_output):
    g = Graph(3, 5)
    a = g.input('a', 8)
    square = g.mul(a, a)
    g.outputs = {'square': square}
    if duplicate_output:
        g.outputs['same_square'] = square
    manifest, _ = compile_graph(g.as_dict(), tmp_path)

    # Independently flatten this one-leaf hierarchy, including every alias copy,
    # named output copy and inverse. Schedule the emitted primitive gates rather
    # than asserting the compiler's depth formula against a duplicate formula.
    leaf, _, _ = build('mul', 8, 3)
    gates = array_gates(leaf)
    scratch = (manifest['values'] + len(g.outputs))*8
    mapping = np.array([
        square*8 + i-16 if 16 <= i < 24 else scratch+i-(8 if i >= 24 else 0)
        for i in range(leaf.qubits)
    ])
    mapped = gates.copy()
    for gate in mapped:
        for field in range(1, int(gate[0])+1):
            gate[field] = mapping[gate[field]]
    copies = np.array([
        [2, a*8+bit, scratch+argument*8+bit, -1]
        for argument in range(2) for bit in range(8)
    ], dtype=np.int32)
    outputs = np.array([
        [2, square*8+bit, (manifest['values']+output)*8+bit, -1]
        for output in range(len(g.outputs)) for bit in range(8)
    ], dtype=np.int32)
    flattened = np.concatenate([
        copies, mapped, copies[::-1], outputs, copies, mapped[::-1], copies[::-1],
    ])
    counts, t_depth, total_depth = gate_resources(flattened, int(mapping.max())+1)
    declared = manifest['resources']
    assert int(counts.sum()) == declared['source_gates']
    assert int(counts[2])*7 == declared['t_count']
    assert int(t_depth) <= declared['t_depth']
    assert int(total_depth) <= declared['clifford_t_depth']


@pytest.mark.parametrize('manifest', [
    {'library_workspace_relative': 'results\\experiment\\leaves',
     'library': 'C:\\old\\results\\experiment\\leaves'},
    {'library_workspace_relative': 'results/experiment/leaves',
     'library': '/old/results/experiment/leaves'},
    {'library': 'C:\\Users\\previous-owner\\project\\results\\experiment\\leaves'},
    {'library': '/old/project/results/experiment/leaves'},
])
def test_library_resolution_survives_relocation_and_separators(tmp_path, monkeypatch, manifest):
    workspace = tmp_path/'relocated'
    expected = workspace/'results/experiment/leaves'
    expected.mkdir(parents=True)
    unrelated = tmp_path/'unrelated-working-directory'
    unrelated.mkdir()
    monkeypatch.chdir(unrelated)
    assert resolve_library(manifest, workspace) == expected.resolve()


@pytest.mark.parametrize('manifest', [
    {'library': 'C:\\unrelated\\gate-library'},
    {'library': '/unrelated/gate-library'},
    {'library_workspace_relative': '../outside-gate-library'},
    {'library': 'C:\\old\\results\\..\\outside-gate-library'},
])
def test_gate_library_resolution_rejects_unrelated_or_traversing_archives(tmp_path, manifest):
    with pytest.raises(ValueError):
        resolve_library(manifest, tmp_path)
