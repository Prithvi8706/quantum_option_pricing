"""Literal-gate exhaustive and boundary checks for the bounded prefix family."""
from __future__ import annotations

import copy
import random

import numpy as np
from numba import njit
import pytest

from research.controlled_source_completion.carry_lookahead import (
    VARIANTS, build_carry_lookahead, leaf_spec, prefix_pairs,
)
from research.controlled_source_completion.compiler import compile_graph
from research.controlled_source_completion.compact_parallel import (
    execute_compact_parallel, make_compact_schedule,
)
from research.controlled_source_completion.ir import Graph, evaluate
from research.controlled_source_completion.primitives import (
    array_gates, basis_run, build, resources, run_gates,
)
from research.journal_sprint.reversible_fixed_point import Program


@njit(cache=True)
def exhaustive(gates, qubits, width, subtract):
    """Every a,b,z and both forward/inverse executions, using emitted gates."""
    limit = 1 << width
    count = 0
    for a in range(limit):
        for b in range(limit):
            result = (a - b if subtract else a + b) & (limit - 1)
            for initial in range(limit):
                for inverse in (False, True):
                    state = np.zeros(qubits, np.uint8)
                    for bit in range(width):
                        state[bit] = (a >> bit) & 1
                        state[width + bit] = (b >> bit) & 1
                        state[2 * width + bit] = (initial >> bit) & 1
                    run_gates(gates, state, inverse)
                    observed = 0
                    for bit in range(width):
                        if state[bit] != (a >> bit) & 1:
                            return False, count, a, b, initial, inverse, 1
                        if state[width + bit] != (b >> bit) & 1:
                            return False, count, a, b, initial, inverse, 2
                        observed |= int(state[2 * width + bit]) << bit
                    if observed != initial ^ result:
                        return False, count, a, b, initial, inverse, 3
                    for wire in range(3 * width, qubits):
                        if state[wire]:
                            return False, count, a, b, initial, inverse, 4
                    count += 1
    return True, count, 0, 0, 0, False, 0


@pytest.mark.parametrize("variant", VARIANTS)
@pytest.mark.parametrize("op", ("add", "sub"))
def test_all_small_inputs_outputs_inverse_cleanup(op, variant):
    for width in range(1, 6):
        program, arguments, outputs = build_carry_lookahead(op, width, variant)
        report = exhaustive(array_gates(program), program.qubits, width, op == "sub")
        assert report[0], (op, variant, width, report)
        assert report[1] == 2 * (1 << (3 * width))
        output = set(outputs[0])
        inputs = set(arguments[0] + arguments[1])
        assert all(not (set(gate[:-1]) & output) for gate in program.gates)
        assert all(gate[-1] not in inputs for gate in program.gates)


def production_vectors(width):
    mask = (1 << width) - 1
    signs = (0, 1, mask, 1 << (width - 1), (1 << (width - 1)) - 1)
    values = {(a, b) for a in signs for b in signs}
    for bit in range(width):
        run = (1 << bit) - 1
        values.update(((run, 1), (run, mask), (1 << bit, 1), (0, 1 << bit),
                       (mask ^ run, run), (run, run), (1 << bit, 1 << bit)))
    rng = random.Random(20261001 + width)
    values.update((rng.getrandbits(width), rng.getrandbits(width)) for _ in range(64))
    return sorted(values)


@pytest.mark.parametrize("width", (24, 40, 72))
@pytest.mark.parametrize("variant", VARIANTS)
@pytest.mark.parametrize("op", ("add", "sub"))
def test_production_carry_signed_modular_random_reference_and_inverse(op, variant, width):
    program, arguments, outputs = build_carry_lookahead(op, width, variant)
    ripple, old_args, old_outs = build(op, width, min(40, width - 1))
    mask = (1 << width) - 1
    rng = random.Random(20261022 + width)
    for a, b in production_vectors(width):
        expected = (a + b if op == "add" else a - b) & mask
        # Independent signed reading still produces the same modular result.
        signed_a = a - (1 << width) if a >> (width - 1) else a
        signed_b = b - (1 << width) if b >> (width - 1) else b
        assert (signed_a + signed_b if op == "add" else signed_a - signed_b) & mask == expected
        for initial in (0, rng.getrandbits(width)):
            for inverse in (False, True):
                actual = basis_run(program, arguments, outputs, [a, b], [initial], inverse)[:3]
                assert actual == ([initial ^ expected], True, True)
            historical = basis_run(ripple, old_args, old_outs, [a, b], [initial])[:3]
            assert historical == ([initial ^ expected], True, True)
    assert resources(program)["qubits"] <= 4096


@pytest.mark.parametrize("variant", VARIANTS)
def test_prefix_network_truth_and_disjointness_for_every_small_bit_pattern(variant):
    # p,g have exactly three allowed states; test direct prefix composition.
    for width in range(1, 8):
        program = Program(compact=True)
        generate = program.register(width)
        propagate = program.register(width)
        start = len(program.gates)
        pairs = prefix_pairs(program, list(zip(generate, propagate)), variant)
        outputs = [program.register(2 * width)]
        end = len(program.gates)
        for i, (g, p) in enumerate(pairs):
            program.gate(g, outputs[0][2 * i])
            program.gate(p, outputs[0][2 * i + 1])
        program.undo(start, end)
        for pattern in range(3 ** width):
            states, rest, gword, pword = [], pattern, 0, 0
            for bit in range(width):
                state, rest = rest % 3, rest // 3
                g, p = ((0, 0), (0, 1), (1, 0))[state]
                states.append((g, p))
                gword |= g << bit
                pword |= p << bit
            expected, gprefix, pprefix = 0, 0, 1
            for bit, (g, p) in enumerate(states):
                gprefix = g | (p & gprefix)
                pprefix &= p
                assert not (gprefix and pprefix)
                expected |= (gprefix << (2 * bit)) | (pprefix << (2 * bit + 1))
            actual = basis_run(program, [generate, propagate], outputs, [gword, pword])[:3]
            assert actual == ([expected], True, True), (variant, width, pattern)


def test_composition_or_equals_xor_exactly_on_disjoint_domain():
    for gh in (0, 1):
        for ph in (0, 1):
            for gl in (0, 1):
                for pl in (0, 1):
                    if gh & ph or gl & pl:
                        continue
                    assert gh ^ (ph & gl) == gh | (ph & gl)
                    assert not ((gh ^ (ph & gl)) & (ph & pl))
    assert (1 ^ (1 & 1)) != (1 | (1 & 1))  # negative disjointness control


@pytest.mark.parametrize("variant", VARIANTS)
def test_dispatch_preserves_other_bytes_aliases_and_rejects_mutation(tmp_path, variant):
    from research.limitation_program_20261001.experiment_adders import PrefixIntegrationLibrary
    from research.limitation_program_20261001.experiment_constants import changed_calls

    graph = Graph(4, integer_bits=4)
    a = graph.input("a", graph.w, "provided")
    b = graph.input("b", graph.w, "provided")
    constant = graph.const_int(3)
    offset = graph.add(a, constant)
    plus = graph.add(offset, offset)
    minus = graph.sub(plus, b)
    graph.outputs = {"sum": plus, "difference": minus, "alias": minus}
    target = graph.as_dict()
    source, _ = compile_graph(target, tmp_path / "original")
    library = PrefixIntegrationLibrary(tmp_path / "new/leaves", target, source, variant)
    updated, _ = compile_graph(target, tmp_path / "new", library)
    attribution = changed_calls(source, updated)
    assert {row["op"] for row in attribution["changes"]} == {"add", "sub"}
    assert all(row["input_contract"] == {} for row in attribution["changes"])
    assert len(attribution["unchanged_leaf_keys"]) == 1
    schedule = make_compact_schedule(target, updated, updated["resources"]["logical_qubits"])
    for sample in ({"a": 0, "b": 0}, {"a": 255, "b": 127}, {"a": 128, "b": 255}):
        initial = {"sum": 0xa5, "difference": 0x3c, "alias": 0xc3}
        actual = execute_compact_parallel(target, updated, schedule, sample, initial)
        expected = {key: value ^ initial[key] for key, value in evaluate(target, sample).items()}
        assert actual["values"] == expected
        assert actual["all_input_and_workspace_bits_restored"]
    node = next(node for node in target["nodes"] if node["op"] == "add")
    library.get(node)
    assert len(library.decisions) == len(source["forward_calls"])
    mutant = copy.deepcopy(node)
    mutant["args"].reverse()
    mutant["out"][0] += 100
    with pytest.raises(ValueError, match="immutable"):
        library.get(mutant)


def test_spec_has_no_narrowing_promise_and_invalid_arguments_reject():
    for variant in VARIANTS:
        spec = leaf_spec("add", 72, 40, variant)
        assert spec["input_contract"] == {} and spec["variant"] == variant
    for args in (("mul", 72, "brent-kung"), ("add", True, "brent-kung"),
                 ("add", 0, "brent-kung"), ("add", 72, "unknown")):
        with pytest.raises(ValueError):
            build_carry_lookahead(*args)
