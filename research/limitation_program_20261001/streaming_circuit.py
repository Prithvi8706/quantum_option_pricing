"""Exact date/block streaming circuits with explicit paid checkpoint cleanup.

Raw log states accumulate native modular increments. Clipping is confined to
temporary stock evaluation. The Asian statistic is a native modular stock sum;
the barrier state is a reversible violation count. All original arithmetic
arrays, tables, copied controls and literal inverses remain visible in events.
"""

from __future__ import annotations

from collections import Counter
import hashlib
from pathlib import Path

import numpy as np

from research.controlled_priority_completion.parallel_source import entries
from research.controlled_source_completion.compact_parallel_v7 import _storage
from research.controlled_source_completion.compiler import mapped_gates, resolve_library
from research.limitation_program_20261001.checkpoint_circuit import _native_cost, fingerprint
from research.limitation_program_20261001.streaming_stage_schedule import make_stage_schedule
from research.limitation_program_20261001.streaming_updates import validate_counter_bound


FORMAT = "paid-exact-monitored-streaming-circuit-v1"
PLACEMENTS = ("date-boundaries", "two-date-blocks")
COUNT_FIELDS = ("source_gates", "x", "cx", "ccx", "t_count", "clifford_cx", "clifford_h")


def _ids(descriptor, group_field="groups", index_field="call_indices"):
    if index_field in descriptor:
        return descriptor[index_field]
    return [g["call_index"] for g in descriptor[group_field]]


def _span(offset, width):
    return {"offset": int(offset), "width": int(width)}


def _wires(span):
    return np.arange(span["offset"], span["offset"] + span["width"], dtype=np.int64)


def _flip_event(event):
    flipped = dict(event)
    if event["kind"] in ("native_batch", "update"):
        flipped["inverse"] = not event["inverse"]
    return flipped


def make_streaming_schedule(target, source, scope, placement, updates, update_directory):
    """Emit one of the two frozen placements; no arithmetic/domain relaxation."""
    if placement not in PLACEMENTS:
        raise ValueError("undeclared streaming checkpoint placement")
    if target["width"] != 72 or target["fraction_bits"] != 40:
        raise ValueError("A19 freezes native72/fraction40 precision")
    metadata = entries(source)
    storage = _storage(target, source, metadata)
    widths, w = storage["widths"], source["word_width"]
    if scope["widths"] != widths:
        raise ValueError("streaming storage proof changed")
    if (scope["source_fingerprint"], scope["target_fingerprint"]) != (
        fingerprint(source),
        fingerprint(target),
    ):
        raise ValueError("streaming original financial binding changed")
    dates = scope.get("date_bindings", scope.get("dates"))
    if len(dates) != 4 or any(len(d["stock_values"]) != 2 for d in dates):
        raise ValueError("A19 freezes exactly two assets and four monitored dates")
    validate_counter_bound(len(dates), 3)
    update_directory = Path(update_directory).resolve()
    input_bindings, constants, normals, cursor = [], {}, {}, 0
    for node in source["inputs"]:
        value = node["out"][0]
        input_bindings.append(
            {
                "value": value,
                "name": node["params"]["name"],
                "bits": node["params"]["bits"],
                **_span(cursor, widths[value]),
            }
        )
        cursor += widths[value]
    original_nodes = {v: n for n in target["nodes"] for v in n["out"]}
    constant_values = sorted(v for n in target["nodes"] if n["op"] == "const" for v in n["out"])
    for value in constant_values:
        constants[value] = _span(cursor, widths[value])
        cursor += widths[value]
    normal_values = sorted({v for pair in scope["gaussian_pairs"] for v in pair["normal_values"]})
    if len(normal_values) != 12:
        raise ValueError("A19 must retain all twelve paid original Gaussian outputs")
    for value in normal_values:
        normals[value] = _span(cursor, w)
        cursor += w
    raw_logs = [_span(cursor + asset * w, w) for asset in range(2)]
    cursor += 2 * w
    asian_sum, counter, alive = _span(cursor, w), _span(cursor + w, 3), _span(cursor + w + 3, 1)
    cursor += w + 4
    named_outputs = []
    for name, value in source["outputs"].items():
        named_outputs.append({"name": name, "value": value, **_span(cursor, w)})
        cursor += w
    floor = cursor
    block_size = 1 if placement == "date-boundaries" else 2
    snapshots = (
        [[_span(floor + (date * 2 + asset) * w, w) for asset in range(2)] for date in range(2)]
        if block_size == 2
        else []
    )
    snapshot_width = 4 * w if snapshots else 0
    stage_base = floor + snapshot_width
    highwater = stage_base
    value_fixed = {n["value"]: _span(n["offset"], n["width"]) for n in input_bindings}
    value_fixed.update(constants)
    value_fixed.update(normals)
    forward, trace_checks, stage_records = [], [], []
    library, native_costs, gate_hashes = resolve_library(source), {}, {}

    def native_cost(key):
        if key not in native_costs:
            entry = metadata[key]
            file = library / entry["gate_file"]
            digest = hashlib.sha256(file.read_bytes()).hexdigest()
            if digest != entry["sha256"]:
                raise ValueError("streaming original native array hash mismatch")
            gates = np.load(file, mmap_mode="r")
            costs = {
                "forward": _native_cost(gates, entry["resources"]["qubits"], False),
                "inverse": _native_cost(gates, entry["resources"]["qubits"], True),
            }
            if any(costs["forward"][k] != entry["resources"][k] for k in costs["forward"]):
                raise ValueError("streaming actual original leaf cost changed")
            native_costs[key], gate_hashes[key] = costs, digest
        return native_costs[key]

    def append(event):
        nonlocal highwater
        for span in event.get("args", []) + event.get("outs", []):
            highwater = max(highwater, span["offset"] + span["width"])
        if "private" in event:
            highwater = max(highwater, event["private"]["offset"] + event["private"]["width"])
        if event["kind"] == "native_batch":
            for call in event["calls"]:
                for span in call["args"] + call["outs"] + [call["private"]]:
                    highwater = max(highwater, span["offset"] + span["width"])
        if event["kind"] == "cx_copy":
            for span in (event["source"], event["target"]):
                highwater = max(highwater, span["offset"] + span["width"])
        forward.append(event)

    def copy_event(source_span, target_span):
        if source_span["width"] > target_span["width"]:
            raise ValueError("streaming copy destination omits a proved active bit")
        append(
            {
                "kind": "cx_copy",
                "source": source_span,
                "target": _span(target_span["offset"], source_span["width"]),
            }
        )

    def stage(call_indices, external, label, mode="serial", max_lanes=None, flag_pad=0):
        plan = make_stage_schedule(source, call_indices, widths, mode=mode, max_lanes=max_lanes)
        retained = plan["retained_qubits"]
        binding = dict(value_fixed)
        binding.update(external)
        offsets = {int(v): off for v, off in plan["retained_offsets"].items()}
        for value, offset in offsets.items():
            binding[value] = _span(stage_base + offset, widths[value])
        batches = []
        for group in plan["groups"]:
            calls = []
            private_offsets = {int(i): off for i, off in group["private_offsets"].items()}
            for index in group["call_indices"]:
                call = source["forward_calls"][index]
                entry = metadata[call["leaf"]]
                native_cost(call["leaf"])
                private_width = entry["resources"]["qubits"] - sum(widths[v] for v in call["out"])
                try:
                    args = [binding[v] for v in call["args"]]
                except KeyError as error:
                    raise ValueError(
                        "streaming local stage lost an original predecessor"
                    ) from error
                calls.append(
                    {
                        "call_index": index,
                        "leaf": call["leaf"],
                        "arg_values": call["args"],
                        "out_values": call["out"],
                        "args": args,
                        "outs": [binding[v] for v in call["out"]],
                        "private": _span(
                            stage_base + retained + flag_pad + private_offsets[index], private_width
                        ),
                    }
                )
            batches.append(
                {"kind": "native_batch", "calls": calls, "inverse": False, "stage": label}
            )
        stage_records.append(
            {
                "label": label,
                "call_indices": call_indices,
                "mode": mode,
                "max_lanes": max_lanes,
                "flag_pad": flag_pad,
                "plan": plan,
            }
        )
        return binding, batches, stage_base + retained + flag_pad

    def apply_stage(batches, inverse=False):
        for batch in reversed(batches) if inverse else batches:
            append(_flip_event(batch) if inverse else batch)

    def update(kind, args, target, private_base, inverse=False):
        entry = updates[kind]
        q = entry["qubits"]
        private = q - sum(len(r) for r in entry["outs"])
        if [len(r) for r in entry["args"]] != [s["width"] for s in args] or (
            len(entry["outs"]) != 1 or len(entry["outs"][0]) != target["width"]
        ):
            raise ValueError("streaming update native register binding changed")
        append(
            {
                "kind": "update",
                "update": kind,
                "args": args,
                "outs": [target],
                "private": _span(private_base, private),
                "inverse": inverse,
            }
        )

    def increment_date(date, inverse=False):
        descriptor = dates[date]
        indices = descriptor.get("increment_call_indices")
        if indices is None:
            indices = [g["call_index"] for g in descriptor["increment_groups"]]
        binding, batches, private = stage(indices, {}, f"increments-date-{date}")
        apply_stage(batches)
        for asset, value in enumerate(descriptor["increment_values"]):
            update("add", [binding[value]], raw_logs[asset], private, inverse)
        apply_stage(batches, True)
        if not inverse:
            trace_checks.append(
                {
                    "after_forward_event": len(forward) - 1,
                    "values": [
                        {"value": value, **raw_logs[asset]}
                        for asset, value in enumerate(descriptor["raw_log_values"])
                    ],
                }
            )

    # All original constants are genuinely prepared and later unprepared.
    for value, span in constants.items():
        raw = int(original_nodes[value]["params"]["value"]) & ((1 << w) - 1)
        append(
            {
                "kind": "x",
                "wires": [span["offset"] + bit for bit in range(span["width"]) if raw >> bit & 1],
                "constant_value": value,
            }
        )
    for pair in scope["gaussian_pairs"]:
        binding, batches, _ = stage(
            _ids(pair), {}, f"gaussian-pair-{pair.get('pair', len(stage_records))}"
        )
        apply_stage(batches)
        for value in pair["normal_values"]:
            copy_event(binding[value], normals[value])
        apply_stage(batches, True)
    initial_log_value = scope.get(
        "initial_log_value", scope.get("semantics", {}).get("initial_log_value")
    )
    if initial_log_value is None:
        initial_log_value = scope["initial_log_constant_value"]
    for raw in raw_logs:
        copy_event(constants[initial_log_value], raw)
    barrier_value = scope.get("threshold_value", scope.get("barrier_value"))
    if barrier_value is None:
        barrier_value = scope["semantics"]["barrier_value"]
    barrier_leaf = next(
        (
            c["leaf"]
            for c in source["forward_calls"]
            if metadata[c["leaf"]]["op"] == "lt" and not metadata[c["leaf"]].get("input_contract")
        ),
        None,
    )
    if barrier_leaf is None:
        raise ValueError("generic full-native signed comparator required for monitoring")
    native_cost(barrier_leaf)
    for start in range(0, len(dates), block_size):
        chosen_dates = list(range(start, start + block_size))
        external = {}
        for local, date in enumerate(chosen_dates):
            increment_date(date)
            raw_bindings = raw_logs
            if block_size == 2:
                raw_bindings = snapshots[local]
                for asset in range(2):
                    copy_event(raw_logs[asset], raw_bindings[asset])
            external.update(zip(dates[date]["raw_log_values"], raw_bindings, strict=True))
        indices = sorted(
            {i for date in chosen_dates for i in dates[date].get("local_call_indices", [])}
        )
        if not indices:
            indices = sorted(
                {g["call_index"] for date in chosen_dates for g in dates[date]["local_groups"]}
            )
        binding, batches, private = stage(
            indices, external, f"financial-block-{start}", "parallel", 2 * block_size, block_size
        )
        apply_stage(batches)
        for local, date in enumerate(chosen_dates):
            descriptor = dates[date]
            for stock in descriptor["stock_values"]:
                update("add", [binding[stock]], asian_sum, private)
            flag = _span(private - block_size + local, 1)
            entry = metadata[barrier_leaf]
            comparator = {
                "kind": "native_batch",
                "inverse": False,
                "stage": "strict-monitoring",
                "calls": [
                    {
                        "leaf": barrier_leaf,
                        "call_index": None,
                        "arg_values": [descriptor["basket_value"], barrier_value],
                        "out_values": [None],
                        "args": [binding[descriptor["basket_value"]], constants[barrier_value]],
                        "outs": [flag],
                        "private": _span(private, entry["resources"]["qubits"] - 1),
                    }
                ],
            }
            append(comparator)
            append({"kind": "x", "wires": [flag["offset"]], "reason": "basket >= H is a violation"})
            update("controlled-increment", [flag], counter, private)
            append({"kind": "x", "wires": [flag["offset"]]})
            append(_flip_event(comparator))
        apply_stage(batches, True)
        if block_size == 2:
            # Earlier snapshot controls are cleared only while their actual
            # source raw logs are reconstructed; every rewind and redo is paid.
            for local in reversed(range(block_size)):
                date = chosen_dates[local]
                for asset in range(2):
                    copy_event(raw_logs[asset], snapshots[local][asset])
                increment_date(date, True)
            for date in chosen_dates:
                increment_date(date)
    final_sum_value = scope["final_total_stock_sum_value"]
    alive_value = scope["original_alive_value"]
    final_indices = scope.get("final_call_indices")
    if final_indices is None:
        final_indices = [g["call_index"] for g in scope.get("final_groups", scope["payoff_groups"])]
    binding, batches, private = stage(
        final_indices, {final_sum_value: asian_sum, alive_value: alive}, "final-payoff"
    )
    update("counter-is-zero", [counter], alive, private)
    trace_checks.append(
        {
            "after_forward_event": len(forward) - 1,
            "values": [{"value": final_sum_value, **asian_sum}, {"value": alive_value, **alive}],
        }
    )
    apply_stage(batches)
    events = list(forward)
    output_events = []
    for output in named_outputs:
        source_span = binding[output["value"]]
        output_events.append(
            {
                "kind": "cx_copy",
                "source": source_span,
                "target": _span(output["offset"], source_span["width"]),
                "named_output": output["name"],
            }
        )
    events.extend(output_events)
    events.extend(_flip_event(event) for event in reversed(forward))
    totals, all_copies = Counter(), 0
    for event in events:
        kind = event["kind"]
        if kind == "x":
            count = len(event["wires"])
            totals["x"] += count
            totals["source_gates"] += count
            totals["clifford_t_depth"] += int(bool(count))
        elif kind == "cx_copy":
            count = event["source"]["width"]
            for field in ("source_gates", "cx", "clifford_cx"):
                totals[field] += count
            totals["clifford_t_depth"] += 1
            all_copies += count
        else:
            calls = event["calls"] if kind == "native_batch" else [event]
            batch_td = batch_ct = 0
            controls = Counter()
            for call in calls:
                if kind == "native_batch":
                    cost = native_costs[call["leaf"]]["inverse" if event["inverse"] else "forward"]
                else:
                    cost = updates[call["update"]]["costs"][
                        "inverse" if event["inverse"] else "forward"
                    ]
                for field in COUNT_FIELDS:
                    totals[field] += cost[field]
                batch_td, batch_ct = (
                    max(batch_td, cost["t_depth"]),
                    max(batch_ct, cost["clifford_t_depth"]),
                )
                copies = 2 * sum(span["width"] for span in call["args"])
                for span in call["args"]:
                    controls.update(range(span["offset"], span["offset"] + span["width"]))
                for field in ("source_gates", "cx", "clifford_cx"):
                    totals[field] += copies
                all_copies += copies
            totals["t_depth"] += batch_td
            totals["clifford_t_depth"] += batch_ct + 2 * max(controls.values(), default=0)
    resources = dict(totals)
    resources.update(
        logical_qubits=highwater,
        fixed_floor_qubits=floor,
        checkpoint_snapshot_qubits=snapshot_width,
        transient_workspace_qubits=highwater - floor,
        random_hadamards=sum(n["bits"] for n in input_bindings),
    )
    return {
        "format": FORMAT,
        "placement": placement,
        "block_size": block_size,
        "source_fingerprint": fingerprint(source),
        "target_fingerprint": fingerprint(target),
        "scope_fingerprint": fingerprint(scope),
        "update_library": str(update_directory),
        "updates": updates,
        "native_leaf_costs": native_costs,
        "native_gate_sha256": gate_hashes,
        "inputs": input_bindings,
        "constants": constants,
        "normal_outputs": normals,
        "raw_logs": raw_logs,
        "asian_sum": asian_sum,
        "violation_counter": counter,
        "alive": alive,
        "named_outputs": named_outputs,
        "forward_event_count": len(forward),
        "output_event_count": len(output_events),
        "events": events,
        "trace_checks": trace_checks,
        "stages": stage_records,
        "resources": resources,
        "all_interface_checkpoint_output_copy_cx": all_copies,
        "monitoring": (
            "A date with signed native basket >= H contributes one violation; alive iff count==0"
        ),
        "invariant": (
            "Current raw logs equal original parallel-prefix sums modulo2**72; clipping is "
            "temporary. Running stock sum equals original balanced-tree sum modulo2**72."
        ),
        "cleanup": (
            "Literal inverse of every forward event after dirty full-native output XOR; original "
            "inputs and every constant, Gaussian, state, counter, snapshot and private wire "
            "restored"
        ),
        "depth_convention": (
            "Serial stages/events; dependency-wave disjoint native batches with fixed2/4 financial "
            "lanes; actual forward/literal-inverse seven-T leaf depths and every shared-control "
            "copy round charged"
        ),
        "G2_to_G5": "open",
    }


def replay_streaming(
    target, source, scope, schedule, inputs, initial_outputs=None, expected_trace=None
):
    """Run the hierarchical actual gates and verify all restored workspace."""
    if schedule.get("format") != FORMAT or (
        schedule["source_fingerprint"],
        schedule["target_fingerprint"],
        schedule["scope_fingerprint"],
    ) != (fingerprint(source), fingerprint(target), fingerprint(scope)):
        raise ValueError("streaming circuit original binding changed")
    metadata = entries(source)
    storage = _storage(target, source, metadata)
    if storage["widths"] != scope["widths"]:
        raise ValueError("streaming original storage proof changed")
    expected_inputs, cursor = [], 0
    for node in source["inputs"]:
        value = node["out"][0]
        expected_inputs.append(
            {
                "value": value,
                "name": node["params"]["name"],
                "bits": node["params"]["bits"],
                **_span(cursor, storage["widths"][value]),
            }
        )
        cursor += storage["widths"][value]
    if schedule["inputs"] != expected_inputs:
        raise ValueError("streaming external register law or binding changed")
    if {o["name"]: o["value"] for o in schedule["named_outputs"]} != source["outputs"] or any(
        o["width"] != source["word_width"] for o in schedule["named_outputs"]
    ):
        raise ValueError("streaming named output binding or native width changed")
    state = np.zeros(schedule["resources"]["logical_qubits"], dtype=np.uint8)
    for node in schedule["inputs"]:
        raw = int(inputs[node["name"]])
        if not 0 <= raw < 1 << node["bits"]:
            raise ValueError("streaming external input violates original word law")
        state[_wires(node)] = [(raw >> bit) & 1 for bit in range(node["width"])]
    w = source["word_width"]
    for output in schedule["named_outputs"]:
        raw = int((initial_outputs or {}).get(output["name"], 0))
        if not 0 <= raw < 1 << w:
            raise ValueError("dirty output must fit full native precision")
        state[_wires(output)] = [(raw >> bit) & 1 for bit in range(w)]
    before, library, cache = state.copy(), resolve_library(source), {}
    updates, update_directory = schedule["updates"], Path(schedule["update_library"])
    checks = {check["after_forward_event"]: check["values"] for check in schedule["trace_checks"]}
    traced = native_calls = update_calls = 0
    observed_peak = schedule["resources"]["fixed_floor_qubits"]
    maximum_violations = 0

    def load_gates(key, is_update):
        cache_key = (is_update, key)
        if cache_key not in cache:
            entry = updates[key] if is_update else metadata[key]
            file = (update_directory if is_update else library) / entry["gate_file"]
            digest = hashlib.sha256(file.read_bytes()).hexdigest()
            if digest != entry["sha256"] or (
                not is_update and digest != schedule["native_gate_sha256"][key]
            ):
                raise ValueError("streaming actual gate array hash mismatch")
            cache[cache_key] = np.load(file, mmap_mode="r")
        return cache[cache_key]

    def invoke_batch(event):
        nonlocal traced, native_calls, update_calls, observed_peak
        is_update = event["kind"] == "update"
        calls = [event] if is_update else event["calls"]
        bindings = []
        occupied = set()
        for call in calls:
            key = call["update"] if is_update else call["leaf"]
            entry = updates[key] if is_update else metadata[key]
            q = entry["qubits"] if is_update else entry["resources"]["qubits"]
            if not is_update:
                for value, span in zip(call["arg_values"], call["args"], strict=True):
                    if span["width"] != storage["widths"][value]:
                        raise ValueError("streaming argument omits an original proved active bit")
                for value, span in zip(call["out_values"], call["outs"], strict=True):
                    expected_width = 1 if value is None else storage["widths"][value]
                    if span["width"] != expected_width:
                        raise ValueError("streaming output omits an original proved active bit")
            mapping = np.full(q, -1, dtype=np.int64)
            for register, span in zip(entry["outs"], call["outs"], strict=True):
                wires = _wires(span)
                mapping[register[: len(wires)]] = wires
                if not event["inverse"] and not is_update and np.any(state[wires]):
                    raise AssertionError("streaming native compute overwrites dirty SSA")
            private = _wires(call["private"])
            remaining = np.flatnonzero(mapping < 0)
            if len(remaining) != len(private) or np.any(state[private]):
                raise AssertionError("streaming native private workspace invalid or dirty")
            mapping[remaining] = private
            physical = set(map(int, mapping))
            if len(physical) != q or physical & occupied or max(physical, default=-1) >= len(state):
                raise ValueError("streaming parallel native mappings alias or exceed workspace")
            occupied |= physical
            observed_peak = max(observed_peak, max(physical, default=-1) + 1)
            bindings.append((call, entry, mapping, private, load_gates(key, is_update)))
        controls = {int(wire) for call in calls for span in call["args"] for wire in _wires(span)}
        if (
            controls & occupied
            or min(controls, default=0) < 0
            or max(controls, default=0) >= len(state)
        ):
            raise ValueError(
                "streaming copied controls alias native destinations/private workspace"
            )
        for call, entry, mapping, _, _ in bindings:
            for register, span in zip(entry["args"], call["args"], strict=True):
                wires = _wires(span)
                state[mapping[register[: len(wires)]]] ^= state[wires]
        for _, _, mapping, _, gates in bindings:
            mapped_gates(gates, state, mapping, event["inverse"])
        for call, entry, mapping, private, _ in bindings:
            for register, span in zip(entry["args"], call["args"], strict=True):
                wires = _wires(span)
                state[mapping[register[: len(wires)]]] ^= state[wires]
            if np.any(state[private]):
                raise AssertionError("streaming native inputs/scratch/high outputs did not restore")
            if not is_update:
                for value, span in zip(call["out_values"], call["outs"], strict=True):
                    wires = _wires(span)
                    actual = sum(int(state[wire]) << bit for bit, wire in enumerate(wires))
                    if event["inverse"] and actual:
                        raise AssertionError("streaming native erase left an SSA value dirty")
                    if not event["inverse"] and expected_trace is not None and value is not None:
                        if actual != int(expected_trace[value]):
                            raise AssertionError(
                                "streaming computed native value differs from original trace"
                            )
                        traced += 1
                native_calls += 1
            else:
                update_calls += 1

    for index, event in enumerate(schedule["events"]):
        if event["kind"] == "x":
            state[event["wires"]] ^= 1
        elif event["kind"] == "cx_copy":
            state[_wires(event["target"])] ^= state[_wires(event["source"])]
            observed_peak = max(
                observed_peak,
                event["source"]["offset"] + event["source"]["width"],
                event["target"]["offset"] + event["target"]["width"],
            )
        elif event["kind"] in ("native_batch", "update"):
            invoke_batch(event)
        else:
            raise ValueError("unknown streaming circuit event")
        if event["kind"] == "update" and event["update"] == "controlled-increment":
            count = sum(
                int(state[wire]) << bit
                for bit, wire in enumerate(_wires(schedule["violation_counter"]))
            )
            maximum_violations = max(maximum_violations, count)
            if count > 4:
                raise AssertionError("actual reversible violation counter exceeded four dates")
        if expected_trace is not None and index in checks:
            for check in checks[index]:
                actual = sum(int(state[wire]) << bit for bit, wire in enumerate(_wires(check)))
                if actual != int(expected_trace[check["value"]]):
                    raise AssertionError(
                        "streaming current raw state changed original prefix semantics"
                    )
                traced += 1
    values = {
        output["name"]: sum(int(state[wire]) << bit for bit, wire in enumerate(_wires(output)))
        for output in schedule["named_outputs"]
    }
    for output in schedule["named_outputs"]:
        state[_wires(output)] = before[_wires(output)]

    def restored(spans):
        return all(np.array_equal(state[_wires(span)], before[_wires(span)]) for span in spans)

    snapshots_start = schedule["resources"]["fixed_floor_qubits"]
    snapshots_stop = snapshots_start + schedule["resources"]["checkpoint_snapshot_qubits"]
    return {
        "values": values,
        "all_input_and_workspace_bits_restored": bool(np.array_equal(state, before)),
        "full_native_output_xor_width": w,
        "observed_physical_qubits": len(state),
        "observed_peak_logical_qubits": observed_peak,
        "native_leaf_invocations": native_calls,
        "update_invocations": update_calls,
        "original_trace_values_checked": traced,
        "current_raw_log_registers_restored": restored(schedule["raw_logs"]),
        "asian_sum_restored": restored([schedule["asian_sum"]]),
        "violation_counter_restored": restored([schedule["violation_counter"]]),
        "maximum_violation_count_observed": maximum_violations,
        "gaussian_outputs_restored": restored(list(schedule["normal_outputs"].values())),
        "constants_restored": restored(list(schedule["constants"].values())),
        "snapshots_restored": bool(
            np.array_equal(
                state[snapshots_start:snapshots_stop], before[snapshots_start:snapshots_stop]
            )
        ),
        "dynamic_helpers_restored": bool(
            np.array_equal(state[snapshots_stop:], before[snapshots_stop:])
        ),
    }
