"""Actual native-leaf dependency batches for a validated financial stage.

Outputs keep the original compact widths and SSA IDs.  Every native argument
occurrence has its own copied register, including repeated arguments.  External
stage values are named explicitly: the caller must prove that each mutable
binding currently equals that original SSA value.  This module does not create
or weaken arithmetic input promises.
"""

from collections import Counter, defaultdict
from copy import deepcopy
from functools import lru_cache
import hashlib
import json
from pathlib import Path

import numpy as np

from research.controlled_priority_completion.parallel_source import entries
from research.controlled_source_completion.compiler import resolve_library
from research.controlled_source_completion.primitives import gate_resources


FORMAT = "paid-streaming-native-dependency-stage-v1"
COUNT_FIELDS = (
    "source_gates",
    "x",
    "cx",
    "ccx",
    "t_count",
    "clifford_cx",
    "clifford_h",
)
RESOURCE_FIELDS = COUNT_FIELDS + ("t_depth", "clifford_t_depth")


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode("utf-8")).hexdigest()


@lru_cache(maxsize=128)
def _scanned_native(path, digest, qubits):
    """The cache key includes the actual gate-file digest and native wire count."""
    gates = np.load(Path(path), mmap_mode="r")
    if gates.dtype != np.int32 or gates.ndim != 2 or gates.shape[1] != 4:
        raise ValueError("invalid emitted native gate array")
    kinds = gates[:, 0]
    if np.any((kinds < 1) | (kinds > 3)):
        raise ValueError("unsupported native gate kind")
    for column, threshold in ((1, 1), (2, 2), (3, 3)):
        active = gates[kinds >= threshold, column]
        if np.any((active < 0) | (active >= qubits)):
            raise ValueError("native gate wire outside declared register")
    cx = gates[kinds >= 2]
    ccx = gates[kinds == 3]
    if (
        np.any(cx[:, 1] == cx[:, 2])
        or np.any(ccx[:, 1] == ccx[:, 3])
        or np.any(ccx[:, 2] == ccx[:, 3])
    ):
        raise ValueError("aliased native controls or target")
    directions = {}
    for name, array in (("forward", gates), ("inverse", gates[::-1])):
        counted, td, ctd = gate_resources(array, qubits)
        x, cx_count, ccx_count = map(int, counted)
        directions[name] = dict(
            source_gates=len(gates),
            x=x,
            cx=cx_count,
            ccx=ccx_count,
            t_count=7 * ccx_count,
            clifford_cx=cx_count + 6 * ccx_count,
            clifford_h=2 * ccx_count,
            t_depth=int(td),
            clifford_t_depth=int(ctd),
        )
    return directions


def _native_costs(library, entry):
    path = library / entry["gate_file"]
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != entry["sha256"]:
        raise ValueError("native gate array differs from frozen leaf hash")
    qubits = entry["resources"]["qubits"]
    costs = deepcopy(_scanned_native(str(path.resolve()), digest, qubits))
    if any(costs["forward"][field] != entry["resources"][field] for field in RESOURCE_FIELDS):
        raise ValueError("native metadata resources disagree with actual gate array")
    return dict(qubits=qubits, sha256=digest, gate_file=entry["gate_file"], **costs)


def _batch_resources(selected, metadata, native, widths, direction, copies):
    resources = {
        field: sum(native[call["leaf"]][direction][field] for call in selected)
        for field in COUNT_FIELDS
    }
    copied_cx = 2 * sum(sum(widths[value] for value in call["args"]) for call in selected)
    for field in ("source_gates", "cx", "clifford_cx"):
        resources[field] += copied_cx
    resources["t_depth"] = max(
        (native[call["leaf"]][direction]["t_depth"] for call in selected), default=0
    )
    resources["clifford_t_depth"] = (
        max(
            (native[call["leaf"]][direction]["clifford_t_depth"] for call in selected),
            default=0,
        )
        + 2 * copies
    )
    resources["argument_copy_cx"] = copied_cx
    return resources


def make_stage_schedule(
    source, call_indices, widths, mode="parallel", qubit_cap=None, max_lanes=None
):
    """Return a stage-relative schedule; caps exclude the caller's external floor.

    A local qubit cap includes all retained stage outputs and private native
    workspace.  Without a cap or lane limit, every independent call in one DAG
    wave is charged and batched together.  Serial mode uses one call per batch.
    All policy parameters must be frozen by the financial producer before use.
    """
    if mode not in ("parallel", "serial"):
        raise ValueError("undeclared stage scheduling mode")
    if qubit_cap is not None and (type(qubit_cap) is not int or qubit_cap < 0):
        raise ValueError("stage qubit cap must be a nonnegative integer")
    if max_lanes is not None and (type(max_lanes) is not int or max_lanes < 1):
        raise ValueError("stage lane cap must be a positive integer")
    indices = list(call_indices)
    if any(type(index) is not int for index in indices) or indices != sorted(set(indices)):
        raise ValueError("stage calls must be unique original indices in ascending order")
    calls = source["forward_calls"]
    if any(not 0 <= index < len(calls) for index in indices):
        raise ValueError("stage call outside original source")
    if len(widths) != source["values"] or any(
        type(width) is not int or not 1 <= width <= source["word_width"] for width in widths
    ):
        raise ValueError("stage compact widths do not cover the original native source")
    metadata, library = entries(source), resolve_library(source)
    inputs = {value for node in source["inputs"] for value in node["out"]}
    producers = {}
    for index, call in enumerate(calls):
        for value in call["out"]:
            if value in inputs or value in producers:
                raise ValueError("original source has duplicate SSA producer")
            producers[value] = index
        if any(
            value not in inputs and producers.get(value, index) >= index for value in call["args"]
        ):
            raise ValueError("original source has missing or forward SSA input")
    selected = set(indices)
    external = sorted(
        {
            value
            for index in indices
            for value in calls[index]["args"]
            if producers.get(value) not in selected
        }
    )
    retained_offsets, retained = {}, 0
    native = {}
    for index in indices:
        call, entry = calls[index], metadata[calls[index]["leaf"]]
        if len(entry["args"]) != len(call["args"]) or len(entry["outs"]) != len(call["out"]):
            raise ValueError("native stage call register arity mismatch")
        interface = [wire for register in entry["args"] + entry["outs"] for wire in register]
        if len(interface) != len(set(interface)) or any(
            not 0 <= wire < entry["resources"]["qubits"] for wire in interface
        ):
            raise ValueError("native stage interface has aliased or invalid wires")
        for value, register in zip(
            call["args"] + call["out"], entry["args"] + entry["outs"], strict=True
        ):
            if widths[value] > len(register):
                raise ValueError("native stage register omits an active original bit")
        for value in call["out"]:
            retained_offsets[value] = retained
            retained += widths[value]
        if call["leaf"] not in native:
            native[call["leaf"]] = _native_costs(library, entry)
    capacity = None if qubit_cap is None else qubit_cap - retained
    if capacity is not None and capacity < 0:
        raise ValueError("stage cap cannot retain its atomic outputs")
    levels = {value: 0 for value in external}
    waves = defaultdict(list)
    for index in indices:
        call = calls[index]
        level = 1 + max((levels[value] for value in call["args"]), default=0)
        for value in call["out"]:
            levels[value] = level
        waves[level].append(index)
    batches = []
    for wave, wave_indices in sorted(waves.items()):
        ordered = sorted(
            wave_indices,
            key=lambda index: (-native[calls[index]["leaf"]]["forward"]["t_depth"], index),
        )
        packing = []
        for index in ordered:
            call = calls[index]
            scratch = metadata[call["leaf"]]["resources"]["qubits"] - sum(
                widths[value] for value in call["out"]
            )
            if scratch < 0 or (capacity is not None and scratch > capacity):
                raise ValueError("stage cap cannot fit one required native leaf")
            batch = None
            if mode == "parallel":
                batch = next(
                    (
                        candidate
                        for candidate in packing
                        if (max_lanes is None or len(candidate["indices"]) < max_lanes)
                        and (capacity is None or candidate["scratch"] + scratch <= capacity)
                    ),
                    None,
                )
            if batch is None:
                batch = dict(indices=[], scratch=0, private_offsets={})
                packing.append(batch)
            batch["private_offsets"][index] = batch["scratch"]
            batch["indices"].append(index)
            batch["scratch"] += scratch
        for batch in packing:
            batch_calls = [calls[index] for index in batch["indices"]]
            copies = max(
                Counter(value for call in batch_calls for value in call["args"]).values(), default=0
            )
            forward = _batch_resources(batch_calls, metadata, native, widths, "forward", copies)
            inverse = _batch_resources(batch_calls, metadata, native, widths, "inverse", copies)
            batches.append(
                dict(
                    wave=wave,
                    call_indices=batch["indices"],
                    private_scratch_qubits=batch["scratch"],
                    private_offsets=batch["private_offsets"],
                    copy_rounds=copies,
                    forward_resources=forward,
                    inverse_resources=inverse,
                    t_depth=forward["t_depth"],
                    clifford_t_depth=forward["clifford_t_depth"],
                )
            )
    forward = {
        field: sum(batch["forward_resources"][field] for batch in batches)
        for field in RESOURCE_FIELDS
    }
    inverse = {
        field: sum(batch["inverse_resources"][field] for batch in reversed(batches))
        for field in RESOURCE_FIELDS
    }
    clean = {field: forward[field] + inverse[field] for field in RESOURCE_FIELDS}
    argument_copy_cx = sum(
        batch["forward_resources"]["argument_copy_cx"]
        + batch["inverse_resources"]["argument_copy_cx"]
        for batch in batches
    )
    peak_private = max((batch["private_scratch_qubits"] for batch in batches), default=0)
    result = dict(
        format=FORMAT,
        source_fingerprint=fingerprint(source),
        mode=mode,
        call_indices=indices,
        external_inputs=external,
        widths={value: widths[value] for value in [*external, *retained_offsets]},
        retained_offsets=retained_offsets,
        offsets=retained_offsets,
        retained_qubits=retained,
        retained_width=retained,
        groups=batches,
        peakprivate=peak_private,
        max_reused_scratch_qubits=peak_private,
        stage_qubits=retained + peak_private,
        qubit_cap=qubit_cap,
        max_lanes=max_lanes,
        nativecostscan=native,
        native_leaf_costs=native,
        native_gate_sha256={key: value["sha256"] for key, value in native.items()},
        forward_resources=forward,
        inverse_resources=inverse,
        clean_resources=clean,
        resources=dict(clean, logical_qubits=retained + peak_private),
        argument_and_output_copy_cx=argument_copy_cx,
        inverse="Reverse dependency batches and literally reverse each actual native gate array",
        copies=(
            "Separate native input register per argument occurrence; "
            "shared SSA copies in disjoint rounds"
        ),
        scope=(
            "Stage costs exclude caller floor, mutable updates and output copies; "
            "those remain charged by the emitter"
        ),
    )
    validate_stage_schedule(source, widths, result)
    return result


def validate_stage_schedule(source, widths, stage):
    """Independently check dependencies, atomic outputs and private batch packing."""
    if stage["source_fingerprint"] != fingerprint(source) or stage["format"] != FORMAT:
        raise ValueError("stage provenance does not match original source")
    calls, metadata = source["forward_calls"], entries(source)
    expected = set(stage["call_indices"])
    if len(expected) != len(stage["call_indices"]):
        raise ValueError("duplicate stage call")
    produced = {value for index in expected for value in calls[index]["out"]}
    external = {
        value for index in expected for value in calls[index]["args"] if value not in produced
    }
    if set(stage["external_inputs"]) != external:
        raise ValueError("external stage inputs do not match original producer boundary")
    offsets = {int(value): offset for value, offset in stage["retained_offsets"].items()}
    if len(offsets) != len(stage["retained_offsets"]) or set(offsets) != produced:
        raise ValueError("stage atomic output registry differs from selected original calls")
    declared_widths = {int(value): width for value, width in stage["widths"].items()}
    if declared_widths != {value: widths[value] for value in external | produced}:
        raise ValueError("stage changed an original compact width")
    live, seen = external, set()
    reserved = []
    for value, offset in offsets.items():
        low, high = int(offset), int(offset) + widths[int(value)]
        if (
            low < 0
            or high > stage["retained_qubits"]
            or any(low < right and left < high for left, right in reserved)
        ):
            raise ValueError("retained stage output collision")
        reserved.append((low, high))
    if sum(high - low for low, high in reserved) != stage["retained_qubits"]:
        raise ValueError("unaccounted retained stage output storage")
    peak = 0
    for batch in stage["groups"]:
        if stage["mode"] == "serial" and len(batch["call_indices"]) != 1:
            raise ValueError("serial stage contains simultaneous leaf calls")
        private, outputs = [], set()
        for index in batch["call_indices"]:
            if index not in expected or index in seen:
                raise ValueError("missing, duplicate or undeclared stage call")
            call = calls[index]
            if any(value not in live for value in call["args"]):
                raise ValueError("batch consumes unavailable or simultaneous producer")
            if outputs.intersection(call["out"]) or any(
                value not in offsets for value in call["out"]
            ):
                raise ValueError("atomic output omitted or aliased")
            outputs.update(call["out"])
            scratch = metadata[call["leaf"]]["resources"]["qubits"] - sum(
                widths[value] for value in call["out"]
            )
            low = batch["private_offsets"].get(index, batch["private_offsets"].get(str(index)))
            high = low + scratch
            if (
                low < 0
                or high > batch["private_scratch_qubits"]
                or any(low < right and left < high for left, right in private)
            ):
                raise ValueError("native private registers collide in batch")
            private.append((low, high))
            seen.add(index)
        if sum(right - left for left, right in private) != batch["private_scratch_qubits"]:
            raise ValueError("native private scratch is not completely charged")
        if batch["copy_rounds"] != max(
            Counter(
                value for index in batch["call_indices"] for value in calls[index]["args"]
            ).values(),
            default=0,
        ):
            raise ValueError("shared/repeated argument copy round omitted")
        if stage["max_lanes"] is not None and len(batch["call_indices"]) > stage["max_lanes"]:
            raise ValueError("stage lane limit exceeded")
        live.update(outputs)
        peak = max(peak, batch["private_scratch_qubits"])
    if seen != expected or peak != stage["peakprivate"]:
        raise ValueError("stage omitted calls or private peak")
    if stage["qubit_cap"] is not None and stage["retained_qubits"] + peak > stage["qubit_cap"]:
        raise ValueError("observed stage storage exceeds declared cap")
    return dict(passed=True, atomic_calls=len(seen), peakprivate=peak)
