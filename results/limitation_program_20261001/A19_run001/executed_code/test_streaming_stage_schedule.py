"""Actual small-word gates, literal inverses and adversarial stage batches."""

from copy import deepcopy
import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

from research.controlled_priority_completion.parallel_source import entries
from research.controlled_source_completion.compact_parallel_v7 import _storage
from research.controlled_source_completion.compiler import compile_graph, resolve_library
from research.controlled_source_completion.ir import Graph, evaluate
from research.controlled_source_completion.primitives import basis_run, resources
from research.journal_sprint.reversible_fixed_point import Program
from research.limitation_program_20261001.streaming_stage_schedule import (
    COUNT_FIELDS,
    make_stage_schedule,
    validate_stage_schedule,
)


def fixture(tmp_path):
    graph = Graph(f=1, integer_bits=2)
    left, right = graph.input("left", 3), graph.input("right", 3)
    first, second = graph.mul(left, left), graph.mul(right, right)
    total = graph.add(first, second)
    graph.tables["pair"] = ((1, 2), (3, 0))
    coeff, _ = graph.node("lookup", (left,), dict(table="pair", bits=1), 2)
    graph.outputs = dict(Y=graph.add(total, coeff))
    target = graph.as_dict()
    source = compile_graph(target, Path(tmp_path) / "source")
    widths = _storage(target, source, entries(source))["widths"]
    return target, source, widths


def program_from_stage(source, widths, stage):
    """Independent actual-wire emission for the tiny complete XOR fixture."""
    program = Program(compact=True)
    external = {value: program.register(widths[value]) for value in stage["external_inputs"]}
    output = program.register(source["word_width"])
    active = program.register(stage["retained_qubits"])
    private = program.register(stage["peakprivate"])
    values = dict(external)
    values.update(
        {
            value: active[offset : offset + widths[value]]
            for value, offset in stage["retained_offsets"].items()
        }
    )
    metadata, library = entries(source), resolve_library(source)

    def batch_calls(batch, inverse):
        selected = list(reversed(batch["call_indices"])) if inverse else batch["call_indices"]
        native_bindings = []
        for index in selected:
            call, entry = (
                source["forward_calls"][index],
                metadata[source["forward_calls"][index]["leaf"]],
            )
            mapping = {}
            for value, register in zip(call["out"], entry["outs"], strict=True):
                for wire, physical in zip(register[: widths[value]], values[value], strict=True):
                    mapping[wire] = physical
            cursor = batch["private_offsets"][index]
            for wire in range(entry["resources"]["qubits"]):
                if wire not in mapping:
                    mapping[wire] = private[cursor]
                    cursor += 1
            for value, register in zip(call["args"], entry["args"], strict=True):
                for original, local in zip(values[value], register[: widths[value]], strict=True):
                    program.gate(original, mapping[local])
            native_bindings.append((call, entry, mapping))
        for _, entry, mapping in native_bindings:
            gates = np.load(library / entry["gate_file"])
            for row in gates[::-1] if inverse else gates:
                kind = int(row[0])
                program.gate(*(mapping[int(wire)] for wire in row[1 : kind + 1]))
        for call, entry, mapping in native_bindings:
            for value, register in zip(call["args"], entry["args"], strict=True):
                for original, local in zip(values[value], register[: widths[value]], strict=True):
                    program.gate(original, mapping[local])

    for batch in stage["groups"]:
        batch_calls(batch, False)
    for original, destination in zip(values[source["outputs"]["Y"]], output, strict=True):
        program.gate(original, destination)
    for batch in reversed(stage["groups"]):
        batch_calls(batch, True)
    return program, [external[value] for value in stage["external_inputs"]], [output]


@pytest.mark.parametrize("mode", ("parallel", "serial"))
def test_exhaustive_native_dirty_xor_full_cleanup_literal_inverse_and_costs(tmp_path, mode):
    target, source, widths = fixture(tmp_path)
    stage = make_stage_schedule(source, range(len(source["forward_calls"])), widths, mode)
    program, arguments, outputs = program_from_stage(source, widths, stage)
    measured = resources(program)
    for field in COUNT_FIELDS:
        extra_copy = 3 if field in ("source_gates", "cx", "clifford_cx") else 0
        assert measured[field] == stage["clean_resources"][field] + extra_copy
    assert measured["t_depth"] <= stage["clean_resources"]["t_depth"]
    assert measured["clifford_t_depth"] <= stage["clean_resources"]["clifford_t_depth"] + 1
    for left in range(8):
        for right in range(8):
            _, trace = evaluate(target, dict(left=left, right=right), True)
            expected = trace[target["outputs"]["Y"]]
            for dirty in range(8):
                actual, clean, preserved, _ = basis_run(
                    program, arguments, outputs, [left, right], [dirty]
                )
                assert actual == [dirty ^ expected]
                assert clean and preserved
                recovered, clean, preserved, _ = basis_run(
                    program, arguments, outputs, [left, right], actual, True
                )
                assert recovered == [dirty]
                assert clean and preserved


def test_parallel_batches_save_depth_and_charge_shared_repeated_copies(tmp_path):
    _, source, widths = fixture(tmp_path)
    indices = range(len(source["forward_calls"]))
    parallel = make_stage_schedule(source, indices, widths, "parallel")
    serial = make_stage_schedule(source, indices, widths, "serial")
    assert parallel["clean_resources"]["t_count"] == serial["clean_resources"]["t_count"]
    assert parallel["clean_resources"]["t_depth"] < serial["clean_resources"]["t_depth"]
    assert parallel["peakprivate"] > serial["peakprivate"]
    assert parallel["groups"][0]["copy_rounds"] == 3  # left twice in square + lookup
    assert set(parallel["retained_offsets"]) == {2, 3, 4, 5, 6, 7}


def test_frozen_lane_cap_and_stage_qubit_cap_pack_without_extra_candidates(tmp_path):
    _, source, widths = fixture(tmp_path)
    indices = range(len(source["forward_calls"]))
    serial = make_stage_schedule(source, indices, widths, "serial")
    parallel = make_stage_schedule(source, indices, widths, "parallel", serial["stage_qubits"], 2)
    assert parallel["stage_qubits"] <= serial["stage_qubits"]
    assert all(len(batch["call_indices"]) <= 2 for batch in parallel["groups"])
    with pytest.raises(ValueError, match="one required native leaf"):
        make_stage_schedule(source, indices, widths, "parallel", serial["stage_qubits"] - 1)


def test_external_stage_boundary_is_exact_original_values_and_json_roundtrip(tmp_path):
    _, source, widths = fixture(tmp_path)
    stage = make_stage_schedule(source, [4], widths, "parallel")
    assert stage["external_inputs"] == [4, 5]
    assert set(stage["retained_offsets"]) == {7}
    validate_stage_schedule(source, widths, json.loads(json.dumps(stage)))


@pytest.mark.parametrize(
    "damage",
    (
        "missing-call",
        "duplicate-call",
        "same-batch-predecessor",
        "private-alias",
        "missing-atomic-sibling",
        "retained-alias",
        "omitted-copy-round",
        "forged-boundary",
        "changed-width",
        "wrong-source",
        "serial-parallel-batch",
    ),
)
def test_independent_stage_validation_negative_controls(tmp_path, damage):
    _, source, widths = fixture(tmp_path)
    stage = make_stage_schedule(source, range(len(source["forward_calls"])), widths, "parallel")
    damaged = deepcopy(stage)
    if damage == "missing-call":
        damaged["groups"][-1]["call_indices"].clear()
    elif damage == "duplicate-call":
        damaged["groups"][0]["call_indices"].append(damaged["groups"][0]["call_indices"][0])
    elif damage == "same-batch-predecessor":
        damaged["groups"][0]["call_indices"].append(2)
    elif damage == "private-alias":
        index = damaged["groups"][0]["call_indices"][1]
        damaged["groups"][0]["private_offsets"][index] = 0
    elif damage == "missing-atomic-sibling":
        del damaged["retained_offsets"][6]
    elif damage == "retained-alias":
        damaged["retained_offsets"][3] = damaged["retained_offsets"][2]
    elif damage == "omitted-copy-round":
        damaged["groups"][0]["copy_rounds"] -= 1
    elif damage == "forged-boundary":
        damaged["external_inputs"].append(2)
    elif damage == "changed-width":
        damaged["widths"][2] -= 1
    elif damage == "wrong-source":
        damaged["source_fingerprint"] = "incorrect"
    elif damage == "serial-parallel-batch":
        damaged["mode"] = "serial"
    with pytest.raises(ValueError):
        validate_stage_schedule(source, widths, damaged)


@pytest.mark.parametrize(
    "damage",
    (
        "unknown-mode",
        "unsorted",
        "duplicate",
        "out-of-range",
        "missing-width",
        "negative-cap",
        "zero-lanes",
    ),
)
def test_invalid_prospective_stage_configuration(tmp_path, damage):
    _, source, widths = fixture(tmp_path)
    indices, mode, cap, lanes = list(range(len(source["forward_calls"]))), "parallel", None, None
    if damage == "unknown-mode":
        mode = "third-family"
    elif damage == "unsorted":
        indices.reverse()
    elif damage == "duplicate":
        indices.append(0)
    elif damage == "out-of-range":
        indices.append(999)
    elif damage == "missing-width":
        widths.pop()
    elif damage == "negative-cap":
        cap = -1
    elif damage == "zero-lanes":
        lanes = 0
    with pytest.raises(ValueError):
        make_stage_schedule(source, indices, widths, mode, cap, lanes)


@pytest.mark.parametrize("damage", ("hash", "metadata", "aliased-native-wire"))
def test_actual_native_arrays_and_metadata_cannot_be_forged(tmp_path, damage):
    _, source, widths = fixture(tmp_path)
    library = resolve_library(source)
    key = source["forward_calls"][0]["leaf"]
    metadata_path = library / (key + ".json")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if damage == "hash":
        metadata["sha256"] = "0" * 64
    elif damage == "metadata":
        metadata["resources"]["t_count"] += 7
    else:
        gate_file = library / metadata["gate_file"]
        gates = np.load(gate_file)
        row = int(np.flatnonzero(gates[:, 0] == 3)[0])
        gates[row, 2] = gates[row, 1]
        np.save(gate_file, gates)
        metadata["sha256"] = hashlib.sha256(gate_file.read_bytes()).hexdigest()
    metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
    with pytest.raises(ValueError):
        make_stage_schedule(source, range(len(source["forward_calls"])), widths)
