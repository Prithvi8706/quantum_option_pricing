"""Exact lookup behavior, coherent use, cache isolation and resource regression."""

import hashlib
import json

import numpy as np
import pytest

from research.controlled_source_completion.compiler import compile_graph, execute
from research.controlled_source_completion.exact_lookup import lookup_shared
from research.controlled_source_completion.ir import Graph, coefficients, evaluate
from research.controlled_source_completion.primitives import (
    Library, array_gates, basis_run, build, resources,
)
from research.journal_sprint.reversible_fixed_point import Program


@pytest.mark.parametrize("bits", [0, 1, 2, 3, 5, 6, 8])
def test_all_addresses_signed_rows_nonzero_output_and_inverse(bits):
    width = max(bits + 2, 4)
    mask = (1 << width) - 1
    table = [[i * i - 17, 13 - 7 * i] for i in range(1 << bits)]
    p, args, outs = build("lookup", width, 2, {"bits": bits}, table)
    for index in range(1 << bits):
        # High address bits are irrelevant and must be preserved.
        address = index | (3 << bits)
        initial = [mask ^ index, (index * 19 + 3) & mask]
        expected = [(value & mask) ^ old for value, old in zip(table[index], initial)]
        actual, clean, preserved, _ = basis_run(p, args, outs, [address], initial)
        assert (actual, clean, preserved) == (expected, True, True)
        restored, clean, preserved, _ = basis_run(
            p, args, outs, [address], actual, inverse=True,
        )
        assert (restored, clean, preserved) == (initial, True, True)
    output_wires = {wire for reg in outs for wire in reg}
    # Output is only XORed: all possible nonzero outputs follow by linearity.
    assert all(not (set(gate[:-1]) & output_wires) for gate in p.gates)


def test_partial_table_and_constant_table():
    for table in ([[4], [-3], [7]], [[-5]] * 8):
        p, args, outs = build("lookup", 5, 2, {"bits": 3}, table)
        for index in range(8):
            expected = ((table[index][0] if index < len(table) else 0) & 31) ^ 17
            actual, clean, preserved, _ = basis_run(p, args, outs, [index], [17])
            assert (actual, clean, preserved) == ([expected], True, True)
    assert resources(p)["ccx"] == 0


@pytest.mark.parametrize("table", [[[5, -7]], [[0, 0]]])
def test_sparse_table_with_wide_address(table):
    # The historical interface permits wide addresses with only a few rows.
    # Unlisted rows are zero; do not allocate an implicit 2**32-row table.
    p, args, outs = build("lookup", 34, 2, {"bits": 32}, table)
    mask = (1 << 34) - 1
    initial = [17, 23]
    for address in (0, 1, 2, 1 << 16, 1 << 31, (1 << 32) - 1, 3 << 32):
        row = table[0] if address & ((1 << 32) - 1) == 0 else [0, 0]
        expected = [(value & mask) ^ old for value, old in zip(row, initial)]
        actual, clean, preserved, _ = basis_run(p, args, outs, [address], initial)
        assert (actual, clean, preserved) == (expected, True, True)
        restored, clean, preserved, _ = basis_run(
            p, args, outs, [address], actual, inverse=True,
        )
        assert (restored, clean, preserved) == (initial, True, True)
    assert len(p.gates) <= 8 * 32 + 2 * 34
    assert p.qubits <= 3 * 34 + 31


def test_small_lookup_on_complex_state_with_entangled_reference():
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector

    table = [[0], [3], [-1], [2]]
    p = Program(compact=True)
    address = p.register(2)
    out = p.register(2)
    reference = p.register(1)
    lookup_shared(p, address, [out], table, 2)
    circuit = p.to_qiskit()
    rng = np.random.default_rng(20261002)
    initial = np.zeros(1 << p.qubits, complex)
    initial[:32] = rng.normal(size=32) + 1j * rng.normal(size=32)
    initial /= np.linalg.norm(initial)
    expected = np.zeros_like(initial)
    for index, amplitude in enumerate(initial):
        expected[index ^ ((table[index & 3][0] & 3) << 2)] += amplitude
    actual = Statevector(initial).evolve(circuit).data
    assert np.max(np.abs(actual - expected)) < 1e-12
    # Also lower every Toffoli to the literal phase-sensitive Clifford+T form.
    decomposed = QuantumCircuit(p.qubits)
    for gate in p.gates:
        if len(gate) < 3:
            (decomposed.x, decomposed.cx)[len(gate) - 1](*gate)
        else:
            a, b, c = gate
            decomposed.h(c)
            decomposed.cx(b, c)
            decomposed.tdg(c)
            decomposed.cx(a, c)
            decomposed.t(c)
            decomposed.cx(b, c)
            decomposed.tdg(c)
            decomposed.cx(a, c)
            decomposed.t(b)
            decomposed.t(c)
            decomposed.h(c)
            decomposed.cx(a, b)
            decomposed.t(a)
            decomposed.tdg(b)
            decomposed.cx(a, b)
    assert np.max(np.abs(Statevector(initial).evolve(decomposed).data - expected)) < 1e-12
    assert len(reference) == 1


def test_real_log_table_and_resource_improvement():
    table = coefficients("log", 32, 8, 40)
    new, args, outs = build("lookup", 72, 40, {"bits": 5}, table)
    old, _, _ = build("lookup", 72, 40, {"bits": 5, "lookup_strategy": "equality"}, table)
    mask = (1 << 72) - 1
    initial = [((i + 3) * 0xA5A5A5A5A5A5A5A5) & mask for i in range(9)]
    for index in range(32):
        wanted = [(value & mask) ^ before for value, before in zip(table[index], initial)]
        actual, clean, preserved, _ = basis_run(new, args, outs, [index], initial)
        assert (actual, clean, preserved) == (wanted, True, True)
    baseline, candidate = resources(old), resources(new)
    assert candidate["qubits"] <= baseline["qubits"]
    for metric in ("t_count", "t_depth", "clifford_t_depth"):
        assert candidate[metric] < baseline[metric]


def test_lookup_library_uses_new_lowering_key(tmp_path):
    node = {"op": "lookup", "params": {"table": "test", "bits": 2}}
    table = [[0], [1], [2], [3]]
    spec = dict(op="lookup", width=4, fraction_bits=2, params=node["params"], table=table)
    legacy_key = hashlib.sha256(
        json.dumps(spec, sort_keys=True, separators=(",", ":")).encode(),
    ).hexdigest()[:20]
    library = Library(tmp_path, 4, 2, {"test": table})
    key, entry = library.get(node)
    assert key != legacy_key
    actual_hash = hashlib.sha256((tmp_path / entry["gate_file"]).read_bytes()).hexdigest()
    assert entry["sha256"] == actual_hash
    assert np.array_equal(np.load(tmp_path / entry["gate_file"]), array_gates(
        build("lookup", 4, 2, node["params"], table)[0],
    ))


def test_lookup_in_complete_clean_graph(tmp_path):
    graph = Graph(2, 3)
    address = graph.input("address", 5)
    graph.tables["test"] = [[i * i - 9, 17 - i] for i in range(8)]
    a, b = graph.node("lookup", (address,), {"table": "test", "bits": 3}, 2)
    graph.outputs = {"sum": graph.add(a, b), "coefficient": a}
    data = graph.as_dict()
    manifest, _ = compile_graph(data, tmp_path)
    for index in range(32):
        _, values = evaluate(data, {"address": index}, trace=True)
        result = execute(manifest, {"address": index}, {"sum": 19, "coefficient": 7})
        assert result["values"] == {
            "sum": values[graph.outputs["sum"]] ^ 19, "coefficient": values[a] ^ 7,
        }
        assert result["workspace_clean"] and result["inputs_preserved"]
