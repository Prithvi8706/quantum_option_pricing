"""Independent actual-array, allocation and recorded-evidence audit for A19.

This auditor never emits a candidate or executes financial gates. It reconstructs
costs from frozen arrays, checks symbolic native-word state identities, and
reconciles recorded gate replays separately from the classical endpoint grid.
"""

from __future__ import annotations

# Receipt descriptions remain readable literal text.
# ruff: noqa: E501

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import random
import shutil
import sys
import traceback
import xml.etree.ElementTree as ET

import numpy as np
from numba import njit

from research.controlled_priority_completion.parallel_source import entries
from research.controlled_source_completion.compact_parallel_v7 import _storage
from research.controlled_source_completion.compiler import resolve_library
from research.controlled_source_completion.ir import evaluate
from research.limitation_program_20261001.compact_ledger import active_bit_certificate
from research.limitation_program_20261001.progress import ROOT

PROGRAM = ROOT / "results/limitation_program_20261001"
REFERENCE = PROGRAM / "A19_reference_run001"
FAILED = PROGRAM / "A19_run001"
COUNT_FIELDS = ("source_gates", "x", "cx", "ccx", "t_count", "clifford_cx", "clifford_h")
RESOURCE_FIELDS = COUNT_FIELDS + ("t_depth", "clifford_t_depth")
DIMENSIONS = ("logical_qubits", "t_count", "t_depth", "clifford_t_depth")
PLACEMENTS = ("date-boundaries", "two-date-blocks")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def relative(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def verify(files):
    for name, digest in files.items():
        assert sha(ROOT / name) == digest, ("frozen file changed", name)


@njit(cache=True)
def scan(gates, qubits, inverse):
    """Fresh parse and seven-T Toffoli expansion; no emitter cost helper."""
    t, d, counts = np.zeros(qubits, np.int64), np.zeros(qubits, np.int64), np.zeros(3, np.int64)
    for i in range(len(gates)):
        kind, a, b, c = gates[len(gates) - 1 - i if inverse else i]
        assert 1 <= kind <= 3 and 0 <= a < qubits
        counts[kind - 1] += 1
        if kind == 1:
            d[a] += 1
        elif kind == 2:
            assert 0 <= b < qubits and a != b
            level, depth = max(t[a], t[b]), max(d[a], d[b]) + 1
            t[a] = t[b] = level
            d[a] = d[b] = depth
        else:
            assert 0 <= b < qubits and 0 <= c < qubits and a != b and a != c and b != c
            for x, y, is_t in (
                (c, c, 0),
                (b, c, 0),
                (c, c, 1),
                (a, c, 0),
                (c, c, 1),
                (b, c, 0),
                (c, c, 1),
                (a, c, 0),
                (b, b, 1),
                (c, c, 1),
                (c, c, 0),
                (a, b, 0),
                (a, a, 1),
                (b, b, 1),
                (a, b, 0),
            ):
                level, depth = max(t[x], t[y]) + is_t, max(d[x], d[y]) + 1
                t[x] = t[y] = level
                d[x] = d[y] = depth
    return counts, t.max(), d.max()


def actual_costs(file, qubits):
    gates = np.load(file, mmap_mode="r")
    assert gates.dtype == np.int32 and gates.ndim == 2 and gates.shape[1] == 4
    result = {}
    for name, inverse in (("forward", False), ("inverse", True)):
        counts, td, ctd = scan(gates, qubits, inverse)
        x, cx, ccx = map(int, counts)
        result[name] = dict(
            source_gates=len(gates),
            x=x,
            cx=cx,
            ccx=ccx,
            t_count=7 * ccx,
            clifford_cx=cx + 6 * ccx,
            clifford_h=2 * ccx,
            t_depth=int(td),
            clifford_t_depth=int(ctd),
        )
    return result


def xml_receipt(path, expected_failures=0):
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root)
    cases = [case for suite in suites for case in suite.findall("testcase")]
    unique = {(case.get("classname"), case.get("name")) for case in cases}
    assert len(unique) == len(cases) == sum(int(s.get("tests", 0)) for s in suites)
    failed = [case for case in cases if case.find("failure") is not None]
    assert len(failed) == sum(int(s.get("failures", 0)) for s in suites) == expected_failures
    assert all(int(s.get(field, 0)) == 0 for s in suites for field in ("errors", "skipped"))
    return dict(
        distinct_cases=len(unique),
        failures=len(failed),
        passed_cases=len(unique) - len(failed),
        classes=sorted({case.get("classname") for case in cases}),
        failure_messages=[case.find("failure").get("message", "") for case in failed],
    )


def assert_native_interface(entry, qubits):
    wires = [wire for register in entry["args"] + entry["outs"] for wire in register]
    assert len(wires) == len(set(wires)) and all(type(q) is int and 0 <= q < qubits for q in wires)


def scan_libraries(source, producer):
    metadata, library = entries(source), resolve_library(source)
    native = {}
    for key, entry in metadata.items():
        file, q = library / entry["gate_file"], entry["resources"]["qubits"]
        assert sha(file) == entry["sha256"]
        assert_native_interface(entry, q)
        costs = actual_costs(file, q)
        assert all(
            entry["resources"][field] == costs["forward"][field] for field in RESOURCE_FIELDS
        )
        native[key] = dict(qubits=q, sha256=sha(file), gate_file=entry["gate_file"], **costs)
    updates, update_costs = {}, {}
    for kind in ("add", "controlled-increment", "counter-is-zero"):
        entry = read(producer / "updates" / (kind + ".json"))
        assert entry["kind"] == kind and entry["word_width"] == 72 and entry["counter_bits"] == 3
        assert (
            entry["preserved_input_registers"] and entry["inverse"] == "literal gate-array reverse"
        )
        assert entry["target_is_mutable"] == (kind != "counter-is-zero")
        expected = {
            "add": ([72], [72]),
            "controlled-increment": ([1], [3]),
            "counter-is-zero": ([3], [1]),
        }[kind]
        assert ([len(r) for r in entry["args"]], [len(r) for r in entry["outs"]]) == expected
        assert_native_interface(entry, entry["qubits"])
        file = producer / "updates" / entry["gate_file"]
        assert sha(file) == entry["sha256"]
        costs = actual_costs(file, entry["qubits"])
        assert costs == entry["costs"]
        updates[kind], update_costs[kind] = entry, costs
    return metadata, native, updates, update_costs


def graph_identities(target, source, scope):
    """Verify associative identities and the actual signed-max strict barrier DAG."""
    nodes = {v: node for node in target["nodes"] for v in node["out"]}
    assert target["width"] == source["word_width"] == 72
    assert target["fraction_bits"] == source["fraction_bits"] == 40
    assert len(source["inputs"]) == 12 and all(n["params"]["bits"] == 32 for n in source["inputs"])
    assert scope["source_fingerprint"] == fingerprint(source) and scope[
        "target_fingerprint"
    ] == fingerprint(target)
    masks = active_bit_certificate(target)
    widths = [max(1, masks[value].bit_length()) for value in range(source["values"])]
    assert (
        widths == scope["widths"]
        and [masks[v] for v in range(source["values"])] == scope["proof_masks"]
    )
    # Reuse the accepted typed guard validators, independently reconstruct widths and costs.
    checked = _storage(target, source, entries(source))
    assert checked["widths"] == widths and checked["proof_masks"] == scope["proof_masks"]
    dates = scope["date_bindings"]
    assert len(dates) == 4 and [d["date"] for d in dates] == list(range(4))
    initial = scope["semantics"]["initial_log_value"]
    assert (
        nodes[initial]["op"] == "const"
        and nodes[initial]["params"]["value"] == scope["initial_log_raw"]
    )

    def terms(value, boundaries):
        if value in boundaries:
            return Counter({value: 1})
        node = nodes[value]
        assert node["op"] == "add", ("non-additive original accumulation", value)
        return terms(node["args"][0], boundaries) + terms(node["args"][1], boundaries)

    for asset in range(2):
        increments = [date["increment_values"][asset] for date in dates]
        for date, binding in enumerate(dates):
            assert terms(binding["raw_log_values"][asset], {initial, *increments}) == Counter(
                [initial, *increments[: date + 1]]
            )
    stocks = [stock for date in dates for stock in date["stock_values"]]
    assert len(stocks) == len(set(stocks)) == 8
    assert terms(scope["final_total_stock_sum_value"], set(stocks)) == Counter(stocks)
    for binding in dates:
        basket = nodes[binding["basket_value"]]
        assert basket["op"] == "cmul" and basket["params"]["c"] == (1 << 39)
        assert terms(basket["args"][0], set(stocks)) == Counter(binding["stock_values"])
    alive = nodes[scope["original_alive_value"]]
    assert alive["op"] == "lt" and alive["args"][1] == scope["threshold_value"]
    baskets = {date["basket_value"] for date in dates}

    def max_leaves(value):
        if value in baskets:
            return [value]
        node = nodes[value]
        assert node["op"] == "select"
        comparison, yes, no = node["args"]
        compare = nodes[comparison]
        assert compare["op"] == "lt" and compare["args"] == [no, yes]
        return max_leaves(no) + max_leaves(yes)

    assert Counter(max_leaves(alive["args"][0])) == Counter(baskets)
    assert source["outputs"] == scope["original_outputs"] == target["outputs"]
    assert source["outputs"] == {"Y": scope["final_output_value"]}
    assert len(scope["gaussian_pairs"]) == 6
    assert sorted(v for pair in scope["gaussian_pairs"] for v in pair["normal_values"]) == sorted(
        scope["normal_values"]
    )
    assert len(set(scope["normal_values"])) == 12
    return widths


def batch_cost(calls, widths, native, direction, copies):
    result = {
        field: sum(native[c["leaf"]][direction][field] for c in calls) for field in COUNT_FIELDS
    }
    argument_cx = 2 * sum(widths[value] for c in calls for value in c["args"])
    for field in ("source_gates", "cx", "clifford_cx"):
        result[field] += argument_cx
    result["t_depth"] = max((native[c["leaf"]][direction]["t_depth"] for c in calls), default=0)
    result["clifford_t_depth"] = (
        max((native[c["leaf"]][direction]["clifford_t_depth"] for c in calls), default=0)
        + 2 * copies
    )
    return dict(result, argument_copy_cx=argument_cx)


def audit_stage(source, widths, stage, native):
    assert stage["source_fingerprint"] == fingerprint(source)
    indices, calls = stage["call_indices"], source["forward_calls"]
    assert indices == sorted(set(indices)) and all(0 <= i < len(calls) for i in indices)
    produced = {v for i in indices for v in calls[i]["out"]}
    external = sorted({v for i in indices for v in calls[i]["args"] if v not in produced})
    assert stage["external_inputs"] == external
    cursor, offsets = 0, {}
    for index in indices:
        for value in calls[index]["out"]:
            offsets[value], cursor = cursor, cursor + widths[value]
    assert {int(k): v for k, v in stage["retained_offsets"].items()} == offsets
    assert stage["offsets"] == stage["retained_offsets"]
    assert stage["retained_qubits"] == stage["retained_width"] == cursor
    assert {int(k): v for k, v in stage["widths"].items()} == {
        v: widths[v] for v in [*external, *offsets]
    }
    levels, waves = dict.fromkeys(external, 0), defaultdict(list)
    for index in indices:
        call = calls[index]
        level = 1 + max((levels[v] for v in call["args"]), default=0)
        levels.update(dict.fromkeys(call["out"], level))
        waves[level].append(index)
    expected, cap = [], stage["qubit_cap"]
    capacity = None if cap is None else cap - cursor
    for wave, wave_indices in sorted(waves.items()):
        packing = []
        for index in sorted(
            wave_indices, key=lambda i: (-native[calls[i]["leaf"]]["forward"]["t_depth"], i)
        ):
            call = calls[index]
            scratch = native[call["leaf"]]["qubits"] - sum(widths[v] for v in call["out"])
            assert scratch >= 0 and (capacity is None or scratch <= capacity)
            batch = next(
                (
                    b
                    for b in packing
                    if stage["mode"] == "parallel"
                    and (stage["max_lanes"] is None or len(b["call_indices"]) < stage["max_lanes"])
                    and (capacity is None or b["private_scratch_qubits"] + scratch <= capacity)
                ),
                None,
            )
            if batch is None:
                batch = dict(
                    wave=wave, call_indices=[], private_scratch_qubits=0, private_offsets={}
                )
                packing.append(batch)
            batch["private_offsets"][str(index)] = batch["private_scratch_qubits"]
            batch["private_scratch_qubits"] += scratch
            batch["call_indices"].append(index)
        for batch in packing:
            selected = [calls[i] for i in batch["call_indices"]]
            copies = max(Counter(v for c in selected for v in c["args"]).values(), default=0)
            forward, inverse = (
                batch_cost(selected, widths, native, d, copies) for d in ("forward", "inverse")
            )
            batch.update(
                copy_rounds=copies,
                forward_resources=forward,
                inverse_resources=inverse,
                t_depth=forward["t_depth"],
                clifford_t_depth=forward["clifford_t_depth"],
            )
            expected.append(batch)
    assert stage["groups"] == expected
    peak = max((b["private_scratch_qubits"] for b in expected), default=0)
    assert stage["peakprivate"] == stage["max_reused_scratch_qubits"] == peak
    assert stage["stage_qubits"] == cursor + peak
    totals = {}
    for direction in ("forward", "inverse"):
        totals[direction] = {
            f: sum(b[direction + "_resources"][f] for b in expected) for f in RESOURCE_FIELDS
        }
        assert stage[direction + "_resources"] == totals[direction]
    clean = {f: totals["forward"][f] + totals["inverse"][f] for f in RESOURCE_FIELDS}
    assert stage["clean_resources"] == clean and stage["resources"] == dict(
        clean, logical_qubits=cursor + peak
    )
    assert stage["argument_and_output_copy_cx"] == sum(
        b[d + "_resources"]["argument_copy_cx"] for b in expected for d in ("forward", "inverse")
    )
    used = {calls[i]["leaf"] for i in indices}
    assert (
        stage["native_leaf_costs"] == stage["nativecostscan"] == {key: native[key] for key in used}
    )
    assert stage["native_gate_sha256"] == {key: native[key]["sha256"] for key in used}
    return offsets


def span_key(span):
    assert type(span["offset"]) is int and type(span["width"]) is int
    assert span["offset"] >= 0 and span["width"] > 0
    return span["offset"], span["width"]


def disjoint(spans):
    ordered = sorted(
        (span["offset"], span["offset"] + span["width"]) for span in spans if span["width"]
    )
    assert all(a[1] <= b[0] for a, b in zip(ordered, ordered[1:])), ("physical alias", ordered)


def flipped(event):
    result = dict(event)
    if event["kind"] in ("native_batch", "update"):
        result["inverse"] = not event["inverse"]
    return result


def audit_circuit(target, source, scope, circuit, widths, metadata, native, updates, update_costs):
    assert circuit["format"] == "paid-exact-monitored-streaming-circuit-v1"
    assert (
        circuit["source_fingerprint"],
        circuit["target_fingerprint"],
        circuit["scope_fingerprint"],
    ) == (fingerprint(source), fingerprint(target), fingerprint(scope))
    placement, dates = circuit["placement"], scope["date_bindings"]
    block = 1 if placement == "date-boundaries" else 2
    assert placement in PLACEMENTS and circuit["block_size"] == block
    assert circuit["updates"] == updates
    cursor, expected_inputs = 0, []
    for node in source["inputs"]:
        value = node["out"][0]
        expected_inputs.append(
            dict(
                value=value,
                name=node["params"]["name"],
                bits=32,
                offset=cursor,
                width=widths[value],
            )
        )
        cursor += widths[value]
    assert circuit["inputs"] == expected_inputs
    nodes = {v: node for node in target["nodes"] for v in node["out"]}
    constants, normals = {}, {}
    for value in sorted(v for v, n in nodes.items() if n["op"] == "const"):
        constants[str(value)] = dict(offset=cursor, width=widths[value])
        cursor += widths[value]
    for value in sorted(scope["normal_values"]):
        normals[str(value)] = dict(offset=cursor, width=72)
        cursor += 72
    assert circuit["constants"] == constants and circuit["normal_outputs"] == normals
    raw = [dict(offset=cursor + 72 * a, width=72) for a in range(2)]
    cursor += 144
    asian, counter, alive = (
        dict(offset=cursor, width=72),
        dict(offset=cursor + 72, width=3),
        dict(offset=cursor + 75, width=1),
    )
    cursor += 76
    assert circuit["raw_logs"] == raw and circuit["asian_sum"] == asian
    assert circuit["violation_counter"] == counter and circuit["alive"] == alive
    outputs = []
    for name, value in source["outputs"].items():
        outputs.append(dict(name=name, value=value, offset=cursor, width=72))
        cursor += 72
    assert circuit["named_outputs"] == outputs
    floor, snapshots = cursor, 288 if block == 2 else 0
    base, highwater = floor + snapshots, floor + snapshots
    stage_map, stage_counts = {}, Counter()
    expected_stages = Counter({f"gaussian-pair-{p['pair']}": 1 for p in scope["gaussian_pairs"]})
    expected_stages.update({f"increments-date-{d}": 1 if block == 1 else 3 for d in range(4)})
    expected_stages.update({f"financial-block-{start}": 1 for start in range(0, 4, block)})
    expected_stages["final-payoff"] = 1
    for record in circuit["stages"]:
        label, plan = record["label"], record["plan"]
        financial = label.startswith("financial-block-")
        assert record["mode"] == plan["mode"] == ("parallel" if financial else "serial")
        assert record["max_lanes"] == plan["max_lanes"] == (2 * block if financial else None)
        assert record["flag_pad"] == (block if financial else 0) and plan["qubit_cap"] is None
        if financial:
            start = int(label.rsplit("-", 1)[1])
            selected = sorted(
                {i for d in range(start, start + block) for i in dates[d]["local_call_indices"]}
            )
        elif label.startswith("gaussian-pair-"):
            pair = int(label.rsplit("-", 1)[1])
            selected = scope["gaussian_pairs"][pair]["call_indices"]
        elif label.startswith("increments-date-"):
            date = int(label.rsplit("-", 1)[1])
            selected = dates[date]["increment_subroutine"]["call_indices"]
        else:
            assert label == "final-payoff"
            selected = scope["final_call_indices"]
        assert record["call_indices"] == plan["call_indices"] == selected
        audit_stage(source, widths, plan, native)
        if label in stage_map:
            assert stage_map[label] == record
        stage_map[label] = record
        stage_counts[label] += 1
    assert stage_counts == expected_stages
    events, n, o = circuit["events"], circuit["forward_event_count"], circuit["output_event_count"]
    assert o == len(outputs) and len(events) == 2 * n + o
    assert events[n + o :] == [flipped(event) for event in reversed(events[:n])]
    assert [e["named_output"] for e in events[n : n + o]] == [out["name"] for out in outputs]
    initial_value = scope["semantics"]["initial_log_value"]
    # Token ledger proves every reused boundary really is its original SSA word.
    live = {span_key(inp): ("ssa", inp["value"]) for inp in expected_inputs}
    raw_initialized, raw_terms = [False, False], [Counter(), Counter()]
    asian_terms, violations, alive_initialized = Counter(), Counter(), False
    increment_map = {
        value: (a, d)
        for d, date in enumerate(dates)
        for a, value in enumerate(date["increment_values"])
    }
    all_stocks = {stock for date in dates for stock in date["stock_values"]}
    all_baskets = {date["basket_value"] for date in dates}
    snapshots_keys = {(floor + 72 * i, 72) for i in range(4)} if snapshots else set()
    normal_keys = {span_key(span): int(value) for value, span in normals.items()}
    raw_keys = {span_key(span): a for a, span in enumerate(raw)}
    totals, all_copies, native_calls, update_calls, traced = Counter(), 0, 0, 0, 0
    used_native, event_batches, monitor_dates, output_count = set(), Counter(), Counter(), Counter()
    checks = {check["after_forward_event"]: check["values"] for check in circuit["trace_checks"]}
    assert len(checks) == len(circuit["trace_checks"])

    def raw_token(asset):
        if not raw_initialized[asset]:
            assert not +raw_terms[asset]
            return None
        assert all(c == 0 or c == 1 for c in raw_terms[asset].values())
        if not +raw_terms[asset]:
            return ("ssa", initial_value)
        for date in range(4):
            if +raw_terms[asset] == Counter(
                dates[d]["increment_values"][asset] for d in range(date + 1)
            ):
                return ("ssa", dates[date]["raw_log_values"][asset])
        raise AssertionError("raw log ceased to equal an original prefix")

    def token(span):
        key = span_key(span)
        if key in raw_keys:
            return raw_token(raw_keys[key])
        if key == span_key(asian):
            assert all(v >= 0 for v in asian_terms.values())
            return (
                ("ssa", scope["final_total_stock_sum_value"])
                if +asian_terms == Counter(all_stocks)
                else None
            )
        if key == span_key(alive):
            return ("ssa", scope["original_alive_value"]) if alive_initialized else None
        if key == span_key(counter):
            return ("counter", tuple(sorted((v, c) for v, c in violations.items() if c)))
        if key in live:
            return live[key]
        # Native normal and named-output containers reserve all72; their upper inactive bits stay zero.
        fullkey = (key[0], 72)
        if fullkey in normal_keys and fullkey in live and key[1] == widths[normal_keys[fullkey]]:
            return live[fullkey]
        return None

    def available(span, value):
        assert token(span) == ("ssa", value), (
            "incorrect original SSA boundary binding",
            span,
            value,
            token(span),
        )

    for index, event in enumerate(events):
        kind = event["kind"]
        if kind == "x":
            wires = event["wires"]
            assert len(wires) == len(set(wires)) and all(0 <= wire < highwater for wire in wires)
            if "constant_value" in event:
                value, span = event["constant_value"], constants[str(event["constant_value"])]
                literal = nodes[value]["params"]["value"] & ((1 << 72) - 1)
                assert wires == [
                    span["offset"] + b for b in range(span["width"]) if literal >> b & 1
                ]
                key = span_key(span)
                if key in live:
                    assert live.pop(key) == ("ssa", value)
                else:
                    live[key] = ("ssa", value)
            else:
                assert len(wires) == 1
                key = (wires[0], 1)
                tag, basket = live[key]
                assert tag in ("lt", "violation")
                live[key] = ("violation" if tag == "lt" else "lt", basket)
            totals["x"] += len(wires)
            totals["source_gates"] += len(wires)
            totals["clifford_t_depth"] += int(bool(wires))
        elif kind == "cx_copy":
            src, dst = event["source"], event["target"]
            assert src["width"] == dst["width"]
            disjoint([src, dst])
            highwater = max(highwater, src["offset"] + src["width"], dst["offset"] + dst["width"])
            value, key = token(src), span_key(dst)
            assert value is not None
            if "named_output" in event:
                output = next(out for out in outputs if out["name"] == event["named_output"])
                assert index in range(n, n + o) and value == ("ssa", output["value"])
                assert dst == dict(offset=output["offset"], width=widths[output["value"]])
                output_count[output["name"]] += 1
            elif key in raw_keys or (key[0], 72) in raw_keys:
                asset = raw_keys[(key[0], 72)]
                assert value == ("ssa", initial_value) and not +raw_terms[asset]
                raw_initialized[asset] = not raw_initialized[asset]
            else:
                if (key[0], 72) in normal_keys:
                    key = (key[0], 72)
                    assert value == ("ssa", normal_keys[key])
                else:
                    assert key in snapshots_keys and value[1] in {
                        v for d in dates for v in d["raw_log_values"]
                    }
                if key in live:
                    assert live.pop(key) == value, "checkpoint XOR cleanup used the wrong prefix"
                else:
                    live[key] = value
            for field in ("source_gates", "cx", "clifford_cx"):
                totals[field] += src["width"]
            totals["clifford_t_depth"] += 1
            all_copies += src["width"]
        else:
            assert kind in ("native_batch", "update")
            calls = event["calls"] if kind == "native_batch" else [event]
            occupied, controls, batch_td, batch_ct = [], Counter(), 0, 0
            for call in calls:
                is_update = kind == "update"
                key = call["update"] if is_update else call["leaf"]
                entry = updates[key] if is_update else metadata[key]
                q = entry["qubits"] if is_update else native[key]["qubits"]
                cost = (update_costs[key] if is_update else native[key])[
                    "inverse" if event["inverse"] else "forward"
                ]
                assert len(call["args"]) == len(entry["args"]) and len(call["outs"]) == len(
                    entry["outs"]
                )
                assert all(
                    span["width"] <= len(reg)
                    for span, reg in zip(
                        call["args"] + call["outs"], entry["args"] + entry["outs"], strict=True
                    )
                )
                private = call["private"]
                assert private["width"] == q - sum(s["width"] for s in call["outs"])
                assert private["offset"] >= base
                occupied.extend(call["outs"] + [private])
                disjoint(call["outs"] + [private])
                for span in call["args"]:
                    controls.update(range(span["offset"], span["offset"] + span["width"]))
                for span in call["args"] + call["outs"] + [private]:
                    highwater = max(highwater, span["offset"] + span["width"])
                if not is_update:
                    used_native.add(key)
                    assert len(call["arg_values"]) == len(call["args"]) and len(
                        call["out_values"]
                    ) == len(call["outs"])
                    for value, span in zip(call["arg_values"], call["args"], strict=True):
                        assert span["width"] == widths[value]
                        available(span, value)
                    original_index = call["call_index"]
                    if original_index is None:
                        assert event["stage"] == "strict-monitoring" and len(calls) == 1
                        assert entry["op"] == "lt" and not entry.get("input_contract")
                        assert call["arg_values"][1] == scope["threshold_value"]
                        basket = call["arg_values"][0]
                        assert basket in all_baskets and call["out_values"] == [None]
                        if index < n and not event["inverse"]:
                            monitor_dates[basket] += 1
                    else:
                        original = source["forward_calls"][original_index]
                        assert (key, call["arg_values"], call["out_values"]) == (
                            original["leaf"],
                            original["args"],
                            original["out"],
                        )
                        record = stage_map[event["stage"]]
                        batch = next(
                            b
                            for b in record["plan"]["groups"]
                            if original_index in b["call_indices"]
                        )
                        assert [c["call_index"] for c in calls] == batch["call_indices"]
                        offsets = record["plan"]["retained_offsets"]
                        assert call["outs"] == [
                            dict(offset=base + offsets[str(v)], width=widths[v])
                            for v in original["out"]
                        ]
                        assert (
                            private["offset"]
                            == base
                            + record["plan"]["retained_qubits"]
                            + record["flag_pad"]
                            + batch["private_offsets"][str(original_index)]
                        )
                    for value, span in zip(call["out_values"], call["outs"], strict=True):
                        assert span["width"] == (1 if value is None else widths[value])
                        out_token = (
                            ("lt", call["arg_values"][0]) if value is None else ("ssa", value)
                        )
                        skey = span_key(span)
                        if event["inverse"]:
                            assert live.pop(skey) == out_token
                        else:
                            assert token(span) is None and skey not in live
                            assert all(
                                skey[0] + skey[1] <= old[0] or old[0] + old[1] <= skey[0]
                                for old in live
                            ), "native output aliases another live word"
                            live[skey] = out_token
                            traced += int(value is not None)
                    native_calls += 1
                else:
                    assert [s["width"] for s in call["args"]] == [len(r) for r in entry["args"]]
                    assert [s["width"] for s in call["outs"]] == [len(r) for r in entry["outs"]]
                    target_key = span_key(call["outs"][0])
                    sign = -1 if event["inverse"] else 1
                    source_token = token(call["args"][0])
                    assert source_token is not None
                    if key == "add":
                        assert source_token[0] == "ssa"
                        value = source_token[1]
                        if target_key in raw_keys:
                            asset = raw_keys[target_key]
                            assert raw_initialized[asset] and increment_map[value][0] == asset
                            raw_terms[asset][value] += sign
                            raw_token(asset)
                        else:
                            assert target_key == span_key(asian) and value in all_stocks
                            asian_terms[value] += sign
                            assert all(c >= 0 for c in asian_terms.values())
                    elif key == "controlled-increment":
                        assert target_key == span_key(counter) and source_token[0] == "violation"
                        violations[source_token[1]] += sign
                        assert (
                            all(c in (0, 1) for c in violations.values())
                            and sum(violations.values()) <= 4
                        )
                    else:
                        assert key == "counter-is-zero" and target_key == span_key(alive)
                        assert span_key(call["args"][0]) == span_key(counter)
                        assert +violations == Counter(all_baskets)
                        alive_initialized = not alive_initialized
                    update_calls += 1
                for field in COUNT_FIELDS:
                    totals[field] += cost[field]
                batch_td, batch_ct = (
                    max(batch_td, cost["t_depth"]),
                    max(batch_ct, cost["clifford_t_depth"]),
                )
                copies = 2 * sum(s["width"] for s in call["args"])
                for field in ("source_gates", "cx", "clifford_cx"):
                    totals[field] += copies
                all_copies += copies
            disjoint(occupied)
            physical = {
                wire
                for span in occupied
                for wire in range(span["offset"], span["offset"] + span["width"])
            }
            assert not physical.intersection(controls)
            for call in calls:
                private = call["private"]
                private_wires = set(range(private["offset"], private["offset"] + private["width"]))
                assert not private_wires.intersection(
                    wire for skey in live for wire in range(skey[0], skey[0] + skey[1])
                )
            totals["t_depth"] += batch_td
            totals["clifford_t_depth"] += batch_ct + 2 * max(controls.values(), default=0)
            if kind == "native_batch" and event["stage"] != "strict-monitoring":
                event_batches[(event["stage"], tuple(c["call_index"] for c in calls))] += 1
        if index in checks:
            assert index < n
            for check in checks[index]:
                available(check, check["value"])
                traced += 1
    assert monitor_dates == Counter(all_baskets) and output_count == Counter(
        list(source["outputs"])
    )
    for label, record in stage_map.items():
        for batch in record["plan"]["groups"]:
            expected = 2 if label == "final-payoff" else 4 * stage_counts[label]
            assert event_batches[(label, tuple(batch["call_indices"]))] == expected
    assert live == {span_key(inp): ("ssa", inp["value"]) for inp in expected_inputs}
    assert not any(raw_initialized) and not any(+terms for terms in raw_terms)
    assert not +asian_terms and not +violations and not alive_initialized
    resources = dict(
        totals,
        logical_qubits=highwater,
        fixed_floor_qubits=floor,
        checkpoint_snapshot_qubits=snapshots,
        transient_workspace_qubits=highwater - floor,
        random_hadamards=384,
    )
    assert circuit["resources"] == resources
    assert circuit["all_interface_checkpoint_output_copy_cx"] == all_copies
    assert circuit["native_leaf_costs"] == {
        key: {d: native[key][d] for d in ("forward", "inverse")} for key in used_native
    }
    assert circuit["native_gate_sha256"] == {key: native[key]["sha256"] for key in used_native}
    assert circuit["G2_to_G5"] == "open"
    return dict(
        passed=True,
        placement=placement,
        resources=resources,
        events=len(events),
        stage_invocations=sum(stage_counts.values()),
        native_leaf_invocations=native_calls,
        update_invocations=update_calls,
        expected_original_trace_checks=traced,
        all_copy_cx=all_copies,
        symbolic_original_SSA_boundaries=True,
        counter_bits=3,
        maximum_forward_monitoring_violations=4,
        full_native_named_output_width=72,
        literal_global_inverse=True,
        financial_max_lanes=2 * block,
    )


def audit_control(target, source, control, widths, native):
    assert control["format"] == "compact-clean-xor-capped-wave-schedule-v7"
    assert control["source_fingerprint"] == fingerprint(source) and control[
        "target_fingerprint"
    ] == fingerprint(target)
    assert control["widths"] == widths
    masks = active_bit_certificate(target)
    assert control["proof_masks"] == [masks[v] for v in range(source["values"])]
    cursor, offsets = 0, []
    for width in widths:
        offsets.append(cursor)
        cursor += width
    assert control["offsets"] == offsets and control["retained_ssa_qubits"] == cursor
    calls, seen, live = (
        source["forward_calls"],
        set(),
        {v for n in source["inputs"] for v in n["out"]},
    )
    levels = dict.fromkeys(live, 0)
    for index, call in enumerate(calls):
        level = 1 + max((levels[v] for v in call["args"]), default=0)
        levels.update(dict.fromkeys(call["out"], level))
    peak, td, ctd = 0, 0, 0
    for group in control["groups"]:
        selected, newly_produced = [calls[i] for i in group["call_indices"]], set()
        scratch = 0
        for index, call in zip(group["call_indices"], selected, strict=True):
            assert index not in seen and all(v in live for v in call["args"])
            assert all(levels[v] == group["wave"] for v in call["out"])
            seen.add(index)
            newly_produced.update(call["out"])
            scratch += native[call["leaf"]]["qubits"] - sum(widths[v] for v in call["out"])
        copies = max(Counter(v for c in selected for v in c["args"]).values(), default=0)
        assert group["private_scratch_qubits"] == scratch and group["copy_rounds"] == copies
        native_td = max(native[c["leaf"]]["forward"]["t_depth"] for c in selected)
        native_ctd = (
            max(native[c["leaf"]]["forward"]["clifford_t_depth"] for c in selected) + 2 * copies
        )
        assert group["t_depth"] == native_td and group["clifford_t_depth"] == native_ctd
        peak, td, ctd = max(peak, scratch), td + native_td, ctd + native_ctd
        live.update(newly_produced)
    assert seen == set(range(len(calls)))
    copies = 4 * sum(widths[v] for c in calls for v in c["args"]) + sum(
        widths[v] for v in source["outputs"].values()
    )
    assert control["argument_and_output_copy_cx"] == copies
    resources = control["resources"]
    for field in COUNT_FIELDS:
        expected = 2 * sum(native[c["leaf"]]["forward"][field] for c in calls)
        if field in ("source_gates", "cx", "clifford_cx"):
            expected += copies
        assert resources[field] == expected
    assert (
        resources["logical_qubits"]
        == cursor + 72 * len(source["outputs"]) + peak
        <= control["qubit_cap"]
    )
    assert resources["max_reused_scratch_qubits"] == peak and resources["t_depth"] == 2 * td
    assert resources["clifford_t_depth"] == 2 * ctd + max(
        Counter(source["outputs"].values()).values()
    )
    assert resources["random_hadamards"] == 384
    return dict(
        passed=True,
        resources=resources,
        native_leaf_invocations=2 * len(calls),
        copy_cx=copies,
        inverse_convention="Accepted compact clean-XOR invocation; each erase repeats forward native kernel, unlike literal-inverse streaming stages",
    )


def dominated(point, choices):
    return any(
        all(other[d] <= point[d] for d in DIMENSIONS)
        and any(other[d] < point[d] for d in DIMENSIONS)
        for other in choices
    )


def audit_saved_replay(row, target, source, protocol, circuit_report=None):
    assert row["passed"]
    inputs, initial = row["inputs"], row["initial"]
    assert set(inputs) == {n["params"]["name"] for n in source["inputs"]}
    assert all(type(v) is int and 0 <= v < 1 << 32 for v in inputs.values())
    assert initial == {name: protocol["dirty_output"] for name in source["outputs"]}
    _, trace = evaluate(target, inputs, True)
    expected = {
        name: int(trace[value]) ^ initial[name] for name, value in source["outputs"].items()
    }
    actual = row["actual"]
    assert row["expected"] == actual["values"] == expected
    assert actual["all_input_and_workspace_bits_restored"]
    if circuit_report is not None:
        assert actual["full_native_output_xor_width"] == 72
        for key in (
            "current_raw_log_registers_restored",
            "asian_sum_restored",
            "violation_counter_restored",
            "gaussian_outputs_restored",
            "constants_restored",
            "snapshots_restored",
            "dynamic_helpers_restored",
        ):
            assert actual[key]
        assert actual["native_leaf_invocations"] == circuit_report["native_leaf_invocations"]
        assert actual["update_invocations"] == circuit_report["update_invocations"]
        assert (
            actual["original_trace_values_checked"]
            == circuit_report["expected_original_trace_checks"]
        )
        assert (
            actual["observed_physical_qubits"]
            == actual["observed_peak_logical_qubits"]
            == circuit_report["resources"]["logical_qubits"]
        )
        assert 0 <= actual["maximum_violation_count_observed"] <= 4
    return expected


def prepare(producer, output):
    producer, output = Path(producer).resolve(), Path(output).resolve()
    producer.relative_to(PROGRAM)
    output.relative_to(PROGRAM)
    assert read(producer / "summary.json")["passed"] and not output.exists()
    frozen = {}
    for directory in (REFERENCE, FAILED, producer):
        manifest = read(directory / "manifest.json")
        frozen.update(manifest["files"])
        frozen.update(read(directory / "protocol.json")["frozen_inputs"])
        frozen[relative(directory / "manifest.json")] = sha(directory / "manifest.json")
    own = Path(__file__).resolve()
    frozen[relative(own)] = sha(own)
    frozen[relative(ROOT / "research/limitation_program_20261001/compact_ledger.py")] = sha(
        ROOT / "research/limitation_program_20261001/compact_ledger.py"
    )
    verify(frozen)
    output.mkdir()
    shutil.copy2(own, output / "executed_reconcile_streaming.py")
    save(
        output / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            local_only=True,
            before_independent_audit=True,
            producer=relative(producer),
            reference=relative(REFERENCE),
            failed_attempt_preserved=relative(FAILED),
            frozen_inputs=frozen,
            interpreter_sha256=sha(sys.executable),
            scope="Fresh independent native/update array forward/literal-inverse scans; original-site guards and independent active widths; reconstructed stages and physical allocations; symbolic original raw-prefix, stock-sum and strict-barrier identities; complete copy charges; fullnative dirty-XOR saved replays and cleanup/trace checks; classical4096-grid recorded evidence kept separate; failed fixture receipt reconciled",
            new_candidates=0,
            new_financial_gate_replays=0,
            new_distinct_tests=0,
            classical_grid_rerun=False,
            coverage="Audit verifies recorded grid size/endpoint law and symbolic identities for all native inputs; it does not claim an independent rerun of all4096 classical comparisons or any new gate replay",
            G2_to_G5="open",
        ),
    )
    print("Independent A19 audit protocol frozen", flush=True)


def run(output):
    output = Path(output).resolve()
    assert not (output / "summary.json").exists()
    protocol = read(output / "protocol.json")
    verify(protocol["frozen_inputs"])
    assert sha(sys.executable) == protocol["interpreter_sha256"]
    producer = ROOT / protocol["producer"]
    producer_protocol, summary = read(producer / "protocol.json"), read(producer / "summary.json")
    assert summary["passed"] and producer_protocol["placements"] == list(PLACEMENTS)
    assert producer_protocol["financial_max_lanes"] == dict(zip(PLACEMENTS, (2, 4), strict=True))
    assert producer_protocol["counter_bits"] == 3 and producer_protocol["monitoring_dates"] == 4
    assert producer_protocol["dirty_output"] == int("a5" * 9, 16)
    failed = xml_receipt(FAILED / "tests.xml", 26)
    assert failed["distinct_cases"] == 61 and failed["passed_cases"] == 35
    assert all("tuple" in message for message in failed["failure_messages"])
    assert read(FAILED / "failed_tests.json") == dict(passed=False, return_code=1)
    assert not (FAILED / "summary.json").exists() and not list(FAILED.glob("*_schedule.json"))
    assert not (FAILED / "updates").exists() and not (FAILED / "tiny_grid.json").exists()
    failed.update(
        cause="compile_graph tuple not unpacked in26 stage fixtures",
        financial_candidates=0,
        financial_gate_replays=0,
    )
    save(output / "preserved_fixture_failure.json", failed)
    tests, reference_tests = (
        xml_receipt(producer / "tests.xml"),
        xml_receipt(REFERENCE / "tests.xml"),
    )
    assert tests["distinct_cases"] == 61 and reference_tests["distinct_cases"] == 12
    assert any("stage_schedule_v2" in name for name in tests["classes"])
    target, source, scope = (
        read(REFERENCE / name) for name in ("target.json", "source.json", "scope.json")
    )
    assert producer_protocol["qubit_cap"] == source["resources"]["logical_qubits"]
    widths = graph_identities(target, source, scope)
    metadata, native, updates, update_costs = scan_libraries(source, producer)
    save(output / "actual_array_costs.json", dict(native=native, updates=update_costs))
    control = read(producer / "control_schedule.json")
    control_report = audit_control(target, source, control, widths, native)
    assert control["qubit_cap"] == producer_protocol["qubit_cap"]
    assert summary["control_resources"] == control_report["resources"]
    save(output / "control_audit.json", control_report)
    reports = {}
    for placement in PLACEMENTS:
        circuit = read(producer / (placement + "_schedule.json"))
        assert Path(circuit["update_library"]).resolve() == (producer / "updates").resolve()
        report = audit_circuit(
            target, source, scope, circuit, widths, metadata, native, updates, update_costs
        )
        reports[placement] = report
        save(output / (placement + "_audit.json"), report)
        print(placement, "independent actual-array/symbolic allocation audit PASS", flush=True)
    grid = read(producer / "tiny_grid.json")
    declaration = producer_protocol["classical_tiny_draw_grid"]
    assert declaration == dict(
        each_uniform_word=[0, (1 << 32) - 1], coordinates=12, combinations=4096
    )
    assert len(declaration["each_uniform_word"]) ** declaration["coordinates"] == 4096
    assert (
        grid["passed"]
        and grid["original_integer_trace_comparisons"] == 4096
        and grid["emitted_gate_replays"] == 0
    )
    assert 0 <= grid["positive_payoff_inputs"] <= 4096 and 1 <= grid["distinct_raw_outputs"] <= 4096
    vectors = read(producer / "replay_vectors.json")
    names = [n["params"]["name"] for n in source["inputs"]]
    saved_vectors = vectors["vectors"]
    assert (
        4
        <= len(saved_vectors)
        <= producer_protocol["vectors"]["maximum_gate_replays_per_placement"]
        == 5
    )
    expected_vectors = [
        dict(label=label, inputs=dict.fromkeys(names, word))
        for label, word in (("all_zero", 0), ("all_max", (1 << 32) - 1), ("all_midpoint", 1 << 31))
    ]
    rng = random.Random(producer_protocol["vectors"]["seed"])
    expected_vectors.append(
        dict(label="seeded_random", inputs={name: rng.randrange(1 << 32) for name in names})
    )
    assert (
        saved_vectors[:4] == expected_vectors and 1 <= vectors["positive_search_evaluations"] <= 256
    )
    # Only the saved finite input rows are reevaluated classically, never financial gates.
    if len(saved_vectors) == 5:
        assert saved_vectors[-1]["label"] == "first_positive_payoff"
        _, trace = evaluate(target, saved_vectors[-1]["inputs"], True)
        assert trace[target["outputs"]["Y"]] > 0
    control_replay = read(producer / "control_replay.json")
    assert (
        control_replay["label"] == saved_vectors[-1]["label"]
        and control_replay["inputs"] == saved_vectors[-1]["inputs"]
    )
    assert control_replay["harness_only"]
    audit_saved_replay(control_replay, target, source, producer_protocol)
    attempts = summary["attempts"]
    assert [row["placement"] for row in attempts] == list(PLACEMENTS)
    choices = [control_report["resources"]] + [
        row["resources"] for row in attempts if row["fits_cap"]
    ]
    gate_replays, frontier = 1, []
    for row in attempts:
        placement, report = row["placement"], reports[row["placement"]]
        assert row["resources"] == report["resources"]
        assert row["fits_cap"] == (
            row["resources"]["logical_qubits"] <= producer_protocol["qubit_cap"]
        )
        assert row["width_saving"] == (
            row["resources"]["logical_qubits"] < control_report["resources"]["logical_qubits"]
        )
        assert row["nondominated"] == (row["fits_cap"] and not dominated(row["resources"], choices))
        selected = row["fits_cap"] and row["width_saving"] and row["nondominated"]
        assert len(row["replays"]) == (len(saved_vectors) if selected else 0)
        if selected:
            assert read(producer / (placement + "_comparison.json")) == row
            for vector, replay in zip(saved_vectors, row["replays"], strict=True):
                assert replay["label"] == vector["label"] and replay["inputs"] == vector["inputs"]
                audit_saved_replay(replay, target, source, producer_protocol, report)
            frontier.append(placement)
        gate_replays += len(row["replays"])
    assert summary["retained_harness_frontier"] == frontier
    assert (
        summary["classical_grid_comparisons"] == 4096
        and summary["new_harness_gate_replays"] == gate_replays
    )
    assert (
        summary["new_complete_B4_B8_financial_gate_replays"] == 0
        and not summary["full_B4_scaling_executed"]
    )
    assert summary["preferred_latency_source_unchanged"] and summary["G2_to_G5"] == "open"
    result = dict(
        passed=True,
        local_only=True,
        harness="B2x4",
        independent_actual_array_and_symbolic_schedule_audit=True,
        placements=[
            {key: value for key, value in report.items() if key != "resources"}
            for report in reports.values()
        ],
        control_resources=control_report["resources"],
        placement_resources={p: r["resources"] for p, r in reports.items()},
        retained_harness_frontier=frontier,
        producer_distinct_pytest_cases_reconciled=tests["distinct_cases"],
        reference_distinct_pytest_cases_reconciled=reference_tests["distinct_cases"],
        preserved_failed_fixture_cases=failed["failures"],
        new_distinct_tests=0,
        recorded_classical_endpoint_grid_comparisons=4096,
        classical_grid_independently_rerun=False,
        recorded_harness_gate_replays_reconciled=gate_replays,
        new_financial_gate_replays=0,
        new_candidates=0,
        full_B4_scaling_executed=False,
        preferred_latency_source_unchanged=True,
        G2_to_G5="open",
    )
    save(output / "summary.json", result)
    verify(protocol["frozen_inputs"])
    save(
        output / "manifest.json",
        dict(
            files={relative(file): sha(file) for file in output.rglob("*") if file.is_file()},
            frozen_inputs=protocol["frozen_inputs"],
            manifest_self_hash_excluded=True,
        ),
    )
    print("Independent A19 audit complete, recorded gate replays", gate_replays, flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "run"))
    parser.add_argument("--producer", type=Path, default=PROGRAM / "A19_run002")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.phase == "prepare":
        prepare(args.producer, args.output)
    else:
        try:
            run(args.output)
        except Exception as error:
            output = args.output.resolve()
            (output / "failure.txt").write_text(traceback.format_exc(), encoding="utf-8")
            save(
                output / "summary.json",
                dict(
                    passed=False,
                    local_only=True,
                    failure_type=type(error).__name__,
                    message=str(error),
                    new_candidates=0,
                    new_financial_gate_replays=0,
                ),
            )
            save(
                output / "manifest.json",
                dict(
                    files={
                        relative(file): sha(file) for file in output.rglob("*") if file.is_file()
                    },
                    frozen_inputs=read(output / "protocol.json")["frozen_inputs"],
                    manifest_self_hash_excluded=True,
                ),
            )
            raise
