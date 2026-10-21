"""Tiny actual hierarchical replay and adversarial wire/provenance bindings."""

from copy import deepcopy

import pytest

from research.controlled_priority_completion.parallel_source import entries
from research.controlled_source_completion.compact_parallel_v7 import _storage
from research.controlled_source_completion.compiler import compile_graph
from research.controlled_source_completion.ir import Graph, evaluate
from research.limitation_program_20261001.checkpoint_circuit import fingerprint
from research.limitation_program_20261001.streaming_circuit import (
    FORMAT,
    make_streaming_schedule,
    replay_streaming,
)
from research.limitation_program_20261001.streaming_updates import emit_updates


@pytest.fixture
def tiny(tmp_path):
    # The exact source is Y=x. The hierarchy reaches Y by copying x into a
    # mutable sum with a real modular adder and then applying its literal inverse.
    graph = Graph(f=0, integer_bits=4)
    value = graph.input("x", 4)
    graph.outputs = {"Y": value}
    target = graph.as_dict()
    source, _ = compile_graph(target, tmp_path / "source")
    storage = _storage(target, source, entries(source))
    scope = {"widths": storage["widths"]}
    update_directory = tmp_path / "updates"
    updates = emit_updates(update_directory, width=4, counter_bits=3)
    update = {
        "kind": "update",
        "update": "add",
        "inverse": False,
        "args": [{"offset": 0, "width": 4}],
        "outs": [{"offset": 12, "width": 4}],
        "private": {"offset": 20, "width": 5},
    }
    reverse = dict(update, inverse=True)
    schedule = {
        "format": FORMAT,
        "source_fingerprint": fingerprint(source),
        "target_fingerprint": fingerprint(target),
        "scope_fingerprint": fingerprint(scope),
        "inputs": [{"value": value, "name": "x", "bits": 4, "offset": 0, "width": 4}],
        "named_outputs": [{"name": "Y", "value": value, "offset": 4, "width": 4}],
        "raw_logs": [{"offset": 8, "width": 4}],
        "asian_sum": {"offset": 12, "width": 4},
        "violation_counter": {"offset": 16, "width": 3},
        "alive": {"offset": 19, "width": 1},
        "constants": {},
        "normal_outputs": {},
        "native_gate_sha256": {},
        "updates": updates,
        "update_library": str(update_directory),
        "trace_checks": [
            {"after_forward_event": 0, "values": [{"value": value, "offset": 12, "width": 4}]}
        ],
        "resources": {
            "logical_qubits": 25,
            "fixed_floor_qubits": 20,
            "checkpoint_snapshot_qubits": 0,
        },
        "events": [
            update,
            {
                "kind": "cx_copy",
                "source": {"offset": 12, "width": 4},
                "target": {"offset": 4, "width": 4},
                "named_output": "Y",
            },
            reverse,
        ],
    }
    return target, source, scope, schedule


def test_actual_update_hierarchy_exhaustive_input_dirty_output_and_complete_cleanup(tiny):
    target, source, scope, schedule = tiny
    for raw in range(16):
        _, trace = evaluate(target, {"x": raw}, trace=True)
        for dirty in range(16):
            result = replay_streaming(
                target, source, scope, schedule, {"x": raw}, {"Y": dirty}, expected_trace=trace
            )
            assert result["values"] == {"Y": raw ^ dirty}
            assert result["all_input_and_workspace_bits_restored"]
            assert result["asian_sum_restored"] and result["dynamic_helpers_restored"]
            assert result["violation_counter_restored"] and result["snapshots_restored"]
            assert result["update_invocations"] == 2
            assert result["observed_peak_logical_qubits"] == 25


@pytest.mark.parametrize(
    "mutation",
    [
        "control_alias",
        "dirty_private",
        "output_width",
        "input_width_law",
        "missing_input",
        "source_binding",
        "target_binding",
        "scope_binding",
        "unknown_event",
    ],
)
def test_reader_rejects_information_or_wire_binding_corruption(tiny, mutation):
    target, source, scope, original = tiny
    schedule = deepcopy(original)
    if mutation == "control_alias":
        schedule["events"][0]["args"][0] = {"offset": 12, "width": 4}
    elif mutation == "dirty_private":
        schedule["events"].insert(0, {"kind": "x", "wires": [20]})
    elif mutation == "output_width":
        schedule["named_outputs"][0]["width"] = 3
    elif mutation == "input_width_law":
        schedule["inputs"][0]["bits"] = 5
    elif mutation == "missing_input":
        schedule["inputs"] = []
    elif mutation == "source_binding":
        schedule["source_fingerprint"] = "0" * 64
    elif mutation == "target_binding":
        schedule["target_fingerprint"] = "0" * 64
    elif mutation == "scope_binding":
        schedule["scope_fingerprint"] = "0" * 64
    else:
        schedule["events"][0]["kind"] = "dirty-overwrite"
    with pytest.raises((ValueError, AssertionError)):
        replay_streaming(target, source, scope, schedule, {"x": 3})


def test_undeclared_streaming_placement_rejected():
    with pytest.raises(ValueError, match="undeclared"):
        make_streaming_schedule({}, {}, {}, "three-date-search", {}, ".")


@pytest.mark.parametrize("precision", [(71, 40), (72, 39)])
def test_actual_harness_precision_cannot_change(precision):
    with pytest.raises(ValueError, match="freezes native"):
        make_streaming_schedule(
            {"width": precision[0], "fraction_bits": precision[1]},
            {},
            {},
            "date-boundaries",
            {},
            ".",
        )
