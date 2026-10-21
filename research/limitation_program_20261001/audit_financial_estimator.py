"""Independent source-compatible native-payoff estimator audit.

No financial circuit is emitted or replayed here. Actual frozen arrays are
counted in both directions; a tiny complete iterate is evaluated independently
on its whole clean-workspace subspace. Source marking records remain separate
from historical clean-XOR financial replays and from unexecuted full QPE.
"""

from __future__ import annotations

# Exact receipts retain readable prose.
# ruff: noqa: E501

import argparse
import ast
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from math import comb, factorial
from pathlib import Path
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
SCHEDULE = PROGRAM / "E07_schedule_run001"
BASELINE = PROGRAM / "A10_coefficient_run001"
COUNT_FIELDS = ("source_gates", "x", "cx", "ccx", "t_count", "clifford_cx", "clifford_h")
RESOURCE_FIELDS = COUNT_FIELDS + ("t_depth", "clifford_t_depth")


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


def pair(value):
    return [value.numerator, value.denominator]


def verify(files):
    for name, expected in files.items():
        assert sha(ROOT / name) == expected, ("frozen file changed", name)


def independent_pi_interval():
    """pi=4(atan(1/2)+atan(1/3)), independent of the producer's Machin80."""
    # Positive angles sum below pi/2 and tangent addition gives exactly one.
    assert (Fraction(1, 2) + Fraction(1, 3)) / (1 - Fraction(1, 6)) == 1
    bounds = []
    for inverse in (2, 3):
        partial, power = Fraction(0), Fraction(1, inverse)
        for k in range(240):
            partial += (-1 if k % 2 else 1) * power / (2 * k + 1)
            power /= inverse * inverse
        following = partial + power / 481  # even240 => positive next term
        bounds.append((partial, following))
    return 4 * (bounds[0][0] + bounds[1][0]), 4 * (bounds[0][1] + bounds[1][1])


def majority(repetitions, bad):
    return sum(
        (
            Fraction(comb(repetitions, k)) * bad**k * (1 - bad) ** (repetitions - k)
            for k in range(repetitions // 2 + 1, repetitions + 1)
        ),
        Fraction(0),
    )


def audit_rational_schedule(schedule, complete):
    lo, hi = independent_pi_interval()
    saved_lo, saved_hi = (Fraction(*p) for p in schedule["pi_enclosure_exact"])
    assert saved_lo <= lo <= hi <= saved_hi and hi - lo < Fraction(1, 10**140)
    assert schedule["M"] == 65536 and schedule["qpe_bits"] == 16
    assert schedule["repetitions"] == schedule["fresh_preparations"] == 15
    assert schedule["controlled_grover_calls"] == 15 * (65536 - 1) == 983025
    assert schedule["longest_single_shot_grover_chain"] == 65535
    assert schedule["normalization_span_dollars"] == 64
    error, failure = (
        Fraction(*schedule["statistical_error_dollars_exact"]),
        Fraction(*schedule["requested_failure_exact"]),
    )
    assert (error, failure) == (Fraction(9, 2000), Fraction(3, 1000))
    assert Fraction(*schedule["amplitude_tolerance_exact"]) == error / 64
    assert (
        64 * (saved_hi / 65536 + saved_hi**2 / 65536**2)
        == Fraction(*schedule["ideal_error_upper_exact"])
        <= error
    )
    assert 64 * (lo / 32768 + lo**2 / 32768**2) > error
    bad = Fraction(*schedule["elementary_failure_upper_exact"])
    assert bad >= 1 - 8 / hi**2 and bad - Fraction(1, 1 << 40) < 1 - 8 / lo**2
    assert bad < Fraction(1, 2)
    assert Fraction(*schedule["ideal_failure_upper_exact"]) == majority(15, bad) <= failure
    assert majority(13, bad) > failure
    assert schedule["output_already_discounted"] and schedule["further_discount_factor"] == [1, 1]
    assert (
        not schedule["synthesis_and_physical_failure_included"]
        and schedule["adaptive_quantum_rounds"] == 0
    )
    assert complete["output_includes_discount"] and complete["further_discount_factor_applied"] == [
        1,
        1,
    ]
    dollar = {row["name"]: row for row in complete["dollar_terms"]}
    failures = {row["name"]: row for row in complete["failure_terms"]}
    for name in (
        "finite_input_law_and_joint_Box_Muller",
        "clipped_log_tail",
        "native_arithmetic_and_polynomial",
    ):
        assert dollar[name]["bound"] is None and dollar[name]["certificate"] is None
    for name in ("QPE_rotation_synthesis", "physical_execution"):
        assert failures[name]["bound"] is None and failures[name]["certificate"] is None
    assert (
        not complete["assessment"]["complete_price_certified"]
        and not complete["assessment"]["missing_bounds_are_zero"]
    )
    return dict(
        passed=True,
        independent_pi_identity="4*(atan(1/2)+atan(1/3)),240 rational terms each",
        independent_pi_enclosure=[pair(lo), pair(hi)],
        M=65536,
        repetitions=15,
        controlled_G_calls=983025,
        ideal_error_upper=schedule["ideal_error_upper_exact"],
        ideal_failure_upper=schedule["ideal_failure_upper_exact"],
        unknown_financial_and_synthesis_bounds_preserved=True,
    )


@njit(cache=True)
def scan(gates, qubits, inverse):
    """Independent seven-T parse also accounts for actual H,CZ,Z primitives."""
    t, d, counts = np.zeros(qubits, np.int64), np.zeros(qubits, np.int64), np.zeros(6, np.int64)
    for i in range(len(gates)):
        kind, a, b, c = gates[len(gates) - 1 - i if inverse else i]
        assert 1 <= kind <= 6 and 0 <= a < qubits
        counts[kind - 1] += 1
        if kind in (1, 4, 6):
            d[a] += 1
        elif kind in (2, 5):
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


def actual_cost(file, qubits, inverse=False, extended=False):
    gates = np.load(file, mmap_mode="r")
    assert gates.dtype == np.int32 and gates.ndim == 2 and gates.shape[1] == 4
    assert extended or np.all(gates[:, 0] <= 3)
    counts, td, ctd = scan(gates, qubits, inverse)
    x, cx, ccx, h, cz, z = map(int, counts)
    result = dict(
        source_gates=len(gates),
        x=x,
        cx=cx,
        ccx=ccx,
        t_count=7 * ccx,
        clifford_cx=cx + 6 * ccx,
        clifford_h=h + 2 * ccx,
        t_depth=int(td),
        clifford_t_depth=int(ctd),
    )
    if extended:
        result.update(h=h, cz=cz, z=z, clifford_cz=cz, clifford_z=z)
    return result


def selector_pattern(value, uniform, flag, qubits):
    """Independent literal Cuccaro subtraction and clean sign-copy pattern."""
    assert (
        value == list(range(72))
        and uniform == list(range(72, 118))
        and flag == 118
        and qubits == 214
    )
    difference, extended, helper = list(range(119, 166)), list(range(166, 213)), 213
    addition = []

    def majority(x, y, z):
        addition.extend(((2, x, y, 0), (2, x, z, 0), (3, z, y, x)))

    def unmajority(x, y, z):
        addition.extend(((3, z, y, x), (2, x, z, 0), (2, z, y, 0)))

    majority(extended[0], difference[0], helper)
    for index in range(1, 47):
        majority(extended[index], difference[index], extended[index - 1])
    for index in reversed(range(1, 47)):
        unmajority(extended[index], difference[index], extended[index - 1])
    unmajority(extended[0], difference[0], helper)
    prefix = [(2, uniform[index], difference[index], 0) for index in range(46)]
    prefix += [(2, value[index], extended[index], 0) for index in range(46)]
    prefix += list(reversed(addition))
    # Both inputs are unsigned46 words: their47-bit modular difference is in
    # [-(2**46-1),2**46-1], so its sign exactly represents the strict comparison.
    return np.asarray(
        prefix + [(2, difference[-1], flag, 0)] + list(reversed(prefix)), dtype=np.int32
    )


def audit_wrapper(wrapper):
    binding = wrapper["binding"]
    case = binding["case"]
    source_directory = BASELINE / case / "min-depth"
    assert case in ("B4x12", "B8x52")
    assert wrapper["format"] == "native-positive-payoff-controlled-grover-v1"
    assert binding["word_width"] == 72 and binding["fraction_bits"] == 40
    assert binding["selector_bits"] == 46 and binding["dollar_span"] == 64
    assert (
        wrapper["probability_law"]
        == binding["probability_law"]
        == "p=E[Yraw]/2**46=E[already discounted native dollar Y]/64"
    )
    assert (
        not binding["second_discount_applied"]
        and not binding["continuous_financial_error_certified"]
    )
    for name in ("target.json", "source.json", "schedule_capped.json"):
        file = source_directory / name
        assert Path(binding["paths"][name]).resolve() == file.resolve() and binding["hashes"][
            name
        ] == sha(file)
    for name in ("certificate", "audit", "audit_manifest"):
        assert sha(binding[name + "_path"]) == binding[name + "_sha256"]
    certificate, audit = read(binding["certificate_path"]), read(binding["audit_path"])
    upper = {"B4x12": 42680645928225, "B8x52": 42680645956484}[case]
    assert (
        certificate["payoff_raw_bounds"]
        == audit["payoff_raw_bounds"]
        == binding["payoff_raw_bounds"]
        == [0, upper]
    )
    assert (
        certificate["all_original_uniform_word_patterns"]
        and not certificate["sampled_price_maximum_used"]
    )
    assert audit["passed"] and audit["all_actual_sum_max_average_subtract_discount_nodes_safe"]
    source, target, capped = (
        read(source_directory / name)
        for name in ("source.json", "target.json", "schedule_capped.json")
    )
    assert wrapper["binding_fingerprint"] == fingerprint(binding)
    assert wrapper["wrapper_fingerprint"] == fingerprint(
        {k: v for k, v in wrapper.items() if k != "wrapper_fingerprint"}
    )
    assert (
        wrapper["source_fingerprint"],
        wrapper["target_fingerprint"],
        wrapper["capped_fingerprint"],
    ) == (fingerprint(source), fingerprint(target), fingerprint(capped))
    metadata, library = entries(source), resolve_library(source)
    storage = _storage(target, source, metadata)
    assert all(capped[k] == value for k, value in storage.items())
    masks = active_bit_certificate(target)
    widths = [max(1, masks[v].bit_length()) for v in range(source["values"])]
    assert widths == storage["widths"] and storage["proof_masks"] == [
        masks[v] for v in range(source["values"])
    ]
    assert source["outputs"] == target["outputs"] == {"Y": certificate["target_output"]["Y"]}
    y = source["outputs"]["Y"]
    assert widths[y] == 72
    target_nodes = {value: node for node in target["nodes"] for value in node["out"]}
    y_node = target_nodes[y]
    assert y_node["op"] == "select"
    discounted = target_nodes[y_node["args"][1]]
    zero = target_nodes[y_node["args"][2]]
    assert (
        discounted["op"] == "cmul"
        and discounted["params"]["c"] == certificate["discount_coefficient"]
    )
    assert zero["op"] == "const" and zero["params"]["value"] == 0
    q, output_base = capped["resources"]["logical_qubits"], storage["retained_ssa_qubits"]
    private_base = output_base + 72
    assert (
        wrapper["private_base"] == private_base and wrapper["private_capacity"] == q - private_base
    )
    assert wrapper["native_named_Y_copy_omitted"] and wrapper["old_output_buffer_reused"]
    assert not wrapper["second_discount_applied"] and wrapper["G2_to_G5"] == "open"
    native = {}
    for key, entry in metadata.items():
        file = library / entry["gate_file"]
        assert sha(file) == entry["sha256"]
        native[key] = {
            direction: actual_cost(file, entry["resources"]["qubits"], direction == "inverse")
            for direction in ("forward", "inverse")
        }
        assert all(entry["resources"][f] == native[key]["forward"][f] for f in RESOURCE_FIELDS)
    assert wrapper["financial_native_costs"] == native
    seen, available, financial = (
        set(),
        {v for node in source["inputs"] for v in node["out"]},
        Counter(),
    )
    assert len(wrapper["financial_batches"]) == len(capped["groups"])
    for batch, group in zip(wrapper["financial_batches"], capped["groups"], strict=True):
        assert batch["wave"] == group["wave"] and batch["copy_rounds"] == group["copy_rounds"]
        assert [call["call_index"] for call in batch["calls"]] == group["call_indices"]
        cursor, outputs = private_base, set()
        mapped_wires = set()
        argument_wires = set()
        for record in batch["calls"]:
            index = record["call_index"]
            assert index not in seen
            seen.add(index)
            call = source["forward_calls"][index]
            entry = metadata[call["leaf"]]
            assert record["leaf"] == call["leaf"] and all(v in available for v in call["args"])
            interface = [wire for reg in entry["args"] + entry["outs"] for wire in reg]
            assert len(interface) == len(set(interface)) and all(
                0 <= wire < entry["resources"]["qubits"] for wire in interface
            )
            private_width = entry["resources"]["qubits"] - sum(widths[v] for v in call["out"])
            assert record["private_base"] == cursor and record["private_width"] == private_width
            out_wires = {
                storage["offsets"][v] + bit for v in call["out"] for bit in range(widths[v])
            }
            assert not out_wires.intersection(mapped_wires) and all(
                wire < output_base for wire in out_wires
            )
            physical = out_wires | set(range(cursor, cursor + private_width))
            assert len(physical) == entry["resources"]["qubits"] and not physical.intersection(
                mapped_wires
            )
            mapped_wires |= physical
            argument_wires.update(
                storage["offsets"][v] + bit for v in call["args"] for bit in range(widths[v])
            )
            cursor += private_width
            assert cursor <= q
            outputs.update(call["out"])
            for direction in ("forward", "inverse"):
                for field in COUNT_FIELDS:
                    financial[field] += native[call["leaf"]][direction][field]
            copies = 4 * sum(widths[v] for v in call["args"])
            for field in ("source_gates", "cx", "clifford_cx"):
                financial[field] += copies
        assert cursor - private_base == group["private_scratch_qubits"]
        assert not argument_wires.intersection(mapped_wires)
        actual_rounds = max(
            Counter(
                v for r in batch["calls"] for v in source["forward_calls"][r["call_index"]]["args"]
            ).values(),
            default=0,
        )
        assert actual_rounds == batch["copy_rounds"]
        for direction in ("forward", "inverse"):
            financial["t_depth"] += max(
                native[r["leaf"]][direction]["t_depth"] for r in batch["calls"]
            )
            financial["clifford_t_depth"] += (
                max(native[r["leaf"]][direction]["clifford_t_depth"] for r in batch["calls"])
                + 2 * actual_rounds
            )
        available.update(outputs)
    assert seen == set(range(len(source["forward_calls"]))) and wrapper[
        "financial_resources"
    ] == dict(financial)
    selector_file, reflection_file = (
        Path(wrapper["selector_file"]),
        Path(wrapper["reflection_file"]),
    )
    assert (
        sha(selector_file) == wrapper["selector_sha256"]
        and sha(reflection_file) == wrapper["reflection_sha256"]
    )
    selector_mapping = wrapper["selector_mapping"]
    selector_q = len(selector_mapping)
    assert len(set(selector_mapping)) == selector_q and all(
        0 <= wire < q for wire in selector_mapping
    )
    assert wrapper["selector_costs"] == {
        d: actual_cost(selector_file, selector_q, d == "inverse") for d in ("forward", "inverse")
    }
    value_register, uniform_register, flag = (
        wrapper["selector_native_value_register"],
        wrapper["selector_native_uniform_register"],
        wrapper["selector_native_flag_wire"],
    )
    assert np.array_equal(
        np.load(selector_file), selector_pattern(value_register, uniform_register, flag, selector_q)
    )
    assert len(value_register) == 72 and len(uniform_register) == 46
    assert len(set(value_register + uniform_register + [flag])) == 119
    assert [selector_mapping[wire] for wire in value_register] == list(
        range(storage["offsets"][y], storage["offsets"][y] + 72)
    )
    uniform = list(range(output_base, output_base + 46))
    assert (
        wrapper["selector_uniform_wires"]
        == [selector_mapping[wire] for wire in uniform_register]
        == uniform
    )
    assert wrapper["selector_flag_wire"] == selector_mapping[flag] == output_base + 46
    occupied = set(value_register + uniform_register + [flag])
    assert [selector_mapping[wire] for wire in range(selector_q) if wire not in occupied] == list(
        range(private_base, private_base + selector_q - 119)
    )
    random_wires = [
        storage["offsets"][node["out"][0]] + bit
        for node in source["inputs"]
        for bit in range(node["params"]["bits"])
    ] + uniform
    original_random = sum(node["params"]["bits"] for node in source["inputs"])
    assert (
        original_random
        == source["resources"]["random_hadamards"]
        == {"B4x12": 1920, "B8x52": 14976}[case]
    )
    assert wrapper["random_wires"] == random_wires and len(random_wires) == original_random + 46
    control = output_base + 47
    assert wrapper["control_wire"] == control and wrapper["allowed_qpe_control_wires"] == list(
        range(control, private_base)
    )
    assert len(wrapper["allowed_qpe_control_wires"]) == 25
    assert not set(wrapper["allowed_qpe_control_wires"]).intersection(
        random_wires + [output_base + 46]
    )
    reflection, spec = np.load(reflection_file), wrapper["reflection_spec"]
    nr = len(random_wires)
    assert (
        spec["qubits"] == 2 * nr
        and spec["random"] == list(range(nr))
        and spec["control"] == nr
        and spec["scratch"] == list(range(nr + 1, 2 * nr))
    )
    expected = [(4, wire, 0, 0) for wire in range(nr)] + [(1, wire, 0, 0) for wire in range(nr)]
    ladder = [(3, 0, 1, nr + 1)] + [(3, nr + j - 1, j, nr + j) for j in range(2, nr)]
    expected += ladder + [(5, 2 * nr - 1, nr, 0)] + list(reversed(ladder))
    expected += (
        [(1, wire, 0, 0) for wire in range(nr)]
        + [(4, wire, 0, 0) for wire in range(nr)]
        + [(6, nr, 0, 0)]
    )
    assert np.array_equal(reflection, np.asarray(expected, dtype=np.int32))
    assert wrapper["reflection_mapping"] == random_wires + [control] + list(
        range(private_base, private_base + nr - 1)
    )
    assert (
        len(set(wrapper["reflection_mapping"])) == 2 * nr and max(wrapper["reflection_mapping"]) < q
    )
    reflection_cost = actual_cost(reflection_file, 2 * nr, extended=True)
    assert wrapper["reflection_resources"] == reflection_cost
    total = Counter(financial)
    for cost in [*wrapper["selector_costs"].values(), reflection_cost]:
        total.update(cost)
    for field in ("source_gates", "cz", "clifford_cz", "clifford_t_depth"):
        total[field] += 1
    expected_resources = dict(
        total,
        logical_qubits=q,
        original_uniform_bits=original_random,
        selector_uniform_bits=46,
        initial_uniform_preparation_h=original_random + 46,
        additional_logical_qubits=0,
        qpe_controls_available_in_old_output_buffer=25,
    )
    assert wrapper["resources"] == expected_resources
    assert wrapper["sequence"] == [
        "original compact F forward",
        "positive selector",
        "CZ(control,flag)",
        "literal inverse selector",
        "literal inverse original F",
        "signed controlled uniform reflection (includes final Z(control))",
    ]
    return (
        dict(
            passed=True,
            case=case,
            resources=expected_resources,
            financial_resources=dict(financial),
            source_forward_calls=len(seen),
            source_literal_inverse_calls=len(seen),
            selector_bits=46,
            dollar_span=64,
            native_named_Y_copy_omitted=True,
            old_output_buffer_reused=True,
            phase_control_zero_identity=True,
            controlled_reflection_relative_sign_verified=True,
            qpe_available_nonalias_controls=25,
        ),
        source,
        target,
    )


def audit_ledger(row, wrapper, schedule):
    Q, r, bits = 983025, 15, 16
    unit = wrapper["resources"]
    assert row["binding"] == wrapper["binding"] and row["source_iterate_resources"] == unit
    assert (
        row["probability_law"] == wrapper["probability_law"]
        and row["wrapper_format"] == wrapper["format"]
    )
    assert row["case"] == wrapper["binding"]["case"] and row["normalization_span_dollars"] == 64
    assert row["price_output_already_discounted"] and not row["second_discount_applied"]
    random_bits = len(wrapper["random_wires"])
    expected = dict(
        fresh_preparations=r,
        financial_forwards=Q,
        financial_literal_inverses=Q,
        source_graph_directions=2 * Q,
        selector_forwards=Q,
        selector_literal_inverses=Q,
        controlled_predicate_CZ=Q,
        controlled_signed_reflections=Q,
        uniform_preparation_H=r * random_bits,
        qpe_preparation_H=r * bits,
        iqft_H=r * bits,
        iqft_controlled_phase_gates=r * bits * (bits - 1) // 2,
        iqft_exact_CS_gates=r * (bits - 1),
        iqft_exact_CS_T_count=3 * r * (bits - 1),
        iqft_controlled_phase_CX=2 * r * bits * (bits - 1) // 2,
        iqft_swaps_CX=3 * r * (bits // 2),
        iqft_arbitrary_Rz_rotations=3 * r * (bits * (bits - 1) // 2 - (bits - 1)),
        measured_QPE_bits=r * bits,
        source_and_selector_reset_bits=r * random_bits,
        qpe_reset_bits=r * bits,
        adaptive_quantum_rounds=0,
        serial_shots=r,
        longest_single_shot_grover_chain=65535,
        longest_single_shot_known_T_depth=65535 * unit["t_depth"] + 3 * (bits - 1),
        complete_known_T_count_excluding_arbitrary_rotation_synthesis=Q * unit["t_count"]
        + 3 * r * (bits - 1),
        serial_known_T_depth_excluding_arbitrary_rotation_synthesis=Q * unit["t_depth"]
        + 3 * r * (bits - 1),
        complete_known_clifford_CX=Q * unit["clifford_cx"]
        + 2 * r * bits * (bits - 1) // 2
        + 3 * r * (bits // 2),
        complete_known_clifford_H=Q * unit["clifford_h"] + r * random_bits + 2 * r * bits,
        complete_known_clifford_CZ=Q * unit["clifford_cz"],
        complete_known_clifford_Z=Q * unit["clifford_z"],
        complete_known_X=Q * unit["x"],
        financial_selector_reflection_T_depth=Q * unit["t_depth"],
        logical_qubits=unit["logical_qubits"],
    )
    for field, value in expected.items():
        assert row[field] == value, (field, row[field], value)
    controls = wrapper["allowed_qpe_control_wires"][:bits]
    assert row["qpe_register_wires"] == controls and len(set(controls)) == 16
    assert not set(controls).intersection(wrapper["random_wires"] + [wrapper["selector_flag_wire"]])
    assert all(wire < wrapper["private_base"] for wire in controls)
    assert Fraction(*row["required_each_rotation_operator_error"]) == Fraction(1, 1000) / (
        2 * expected["iqft_arbitrary_Rz_rotations"]
    )
    assert row["synthesis_observation_failure_allowance"] == [1, 1000]
    readout = Fraction(2, 1 << 40)
    assert row["classical_readout_error_allowance"] == pair(readout)
    error = Fraction(*schedule["ideal_error_upper_exact"]) + readout
    assert row["ideal_error_plus_readout_upper_exact"] == pair(error) and error <= Fraction(9, 2000)
    assert (
        row["statistical_error_dollars_exact"] == [9, 2000]
        and row["ideal_failure_upper_exact"] == schedule["ideal_failure_upper_exact"]
    )
    for field in (
        "synthesis_certificate",
        "full_T_count",
        "full_T_depth",
        "total_readout_or_reset_seconds",
        "full_physical_runtime_seconds",
    ):
        assert row[field] is None
    assert (
        row["ideal_digital_mean_error_confidence_certificate"]
        and not row["full_continuous_price_certificate"]
        and not row["full_physical_execution_certificate"]
    )
    assert row["G2_to_G5"] == "open"
    return dict(
        passed=True,
        exact_invocations=expected,
        all_QPE_controls_nonalias=True,
        full_synthesis_and_physical_costs_unknown=True,
        probability_law=wrapper["probability_law"],
        historical_C4_multiplier_used=False,
    )


def apply_gate_array(gates, qubits, state):
    """Independent statevector application for whole tiny-iterate verification."""
    indices = np.arange(1 << qubits, dtype=np.int64)
    for kind, a, b, c in gates:
        kind, a, b, c = map(int, (kind, a, b, c))
        if kind in (1, 2, 3):
            target = a if kind == 1 else b if kind == 2 else c
            active = np.ones(len(indices), dtype=bool)
            if kind >= 2:
                active &= ((indices >> a) & 1).astype(bool)
            if kind == 3:
                active &= ((indices >> b) & 1).astype(bool)
            permutation = indices.copy()
            permutation[active] ^= 1 << target
            state = state[permutation]
        elif kind == 4:
            zero = indices[((indices >> a) & 1) == 0]
            one = zero | (1 << a)
            old_zero, old_one = state[zero].copy(), state[one].copy()
            state[zero], state[one] = (
                (old_zero + old_one) / np.sqrt(2),
                (old_zero - old_one) / np.sqrt(2),
            )
        else:
            assert kind in (5, 6)
            active = ((indices >> a) & 1).astype(bool)
            if kind == 5:
                active &= ((indices >> b) & 1).astype(bool)
            state[active] *= -1
    return state


def audit_toy(spec, file):
    gates = np.load(file)
    assert sha(file) == spec["sha256"]
    q, random_wires, control = spec["qubits"], spec["random_wires"], spec["control_wire"]
    assert q <= 20 and control not in random_wires and len(set(random_wires)) == len(random_wires)
    work = spec["workspace_wires"]
    assert (
        set(random_wires + [control] + work) == set(range(q))
        and len(random_wires) + 1 + len(work) == q
    )
    actual_cost(file, q, extended=True)
    dimension = 1 << len(random_wires)
    markings = spec["marking_for_each_random_word"]
    assert len(markings) == dimension and all(
        type(v) in (bool, int) and v in (0, 1) for v in markings
    )
    source_bits = 2 if spec["kind"] == "positive-rare-event" else 1
    shifted = spec["kind"] == "shifted-negative-two-point"
    assert spec["shift"] == (2 if shifted else 0) and spec["selector_span"] == (4 if shifted else 2)
    expected_payoffs, expected_markings = [], []
    for word in range(dimension):
        source_word = word & ((1 << source_bits) - 1)
        uniform_word = word >> source_bits
        payoff = (
            (-1 if source_word == 0 else 1)
            if shifted
            else (int(source_word == 3) if source_bits == 2 else source_word)
        )
        expected_payoffs.append(payoff)
        expected_markings.append(int(uniform_word < payoff + spec["shift"]))
    assert spec["payoff_for_each_random_word"] == expected_payoffs and markings == expected_markings
    maximum = 0.0
    for branch in (0, 1):
        for word in range(dimension):
            physical = sum(((word >> bit) & 1) << wire for bit, wire in enumerate(random_wires)) | (
                branch << control
            )
            state = np.zeros(1 << q, dtype=np.complex128)
            state[physical] = 1
            actual = apply_gate_array(gates, q, state)
            expected = np.zeros_like(actual)
            if branch == 0:
                expected[physical] = 1
            else:
                phase = -1 if markings[word] else 1
                for other in range(dimension):
                    index = sum(
                        ((other >> bit) & 1) << wire for bit, wire in enumerate(random_wires)
                    ) | (1 << control)
                    expected[index] = phase * (2 / dimension - int(other == word))
            error = float(np.max(np.abs(actual - expected)))
            assert error < 3e-12, (spec["kind"], branch, word, error)
            maximum = max(maximum, error)
    assert Fraction(spec["probability_numerator"], spec["probability_denominator"]) == Fraction(
        sum(markings), dimension
    )
    expected_p = {
        "positive-two-point": Fraction(1, 4),
        "positive-rare-event": Fraction(1, 8),
        "shifted-negative-two-point": Fraction(1, 2),
    }[spec["kind"]]
    assert Fraction(sum(markings), dimension) == expected_p
    assert spec["source_inverse"] == spec["selector_inverse"] == "literal gate reversal"
    assert tuple(gates[-1]) == (6, control, 0, 0)
    # Removing the final control-Z must flip the active branch and fail the
    # controlled relative-sign requirement. This is an in-memory toy audit only.
    state = np.zeros(1 << q, dtype=np.complex128)
    state[1 << control] = 1
    full = apply_gate_array(gates, q, state.copy())
    missing_z = apply_gate_array(gates[:-1], q, state.copy())
    assert np.max(np.abs(missing_z + full)) < 3e-12 and np.max(np.abs(missing_z - full)) > 0.1
    return dict(
        passed=True,
        name=spec["kind"],
        complete_clean_subspace_columns=2 * dimension,
        probability_exact=pair(Fraction(sum(markings), dimension)),
        full_controlled_iterate_unitary_verified=True,
        control_zero_identity=True,
        control_one_signed_reflection_times_marker=True,
        helper_workspace_restored=True,
        maximum_matrix_column_error=maximum,
        financial_gate_replay=False,
        missing_final_control_Z_negative_control_rejected=True,
    )


def audit_readout_precision(schedule):
    """Uniform rational Horner/Taylor enclosure and midpoint-floor error bound."""
    exact_lo, exact_hi = (Fraction(*p) for p in schedule["pi_enclosure_exact"])
    scale = 1 << 160
    pi_lo = Fraction(exact_lo.numerator * scale // exact_lo.denominator, scale)
    pi_hi = Fraction(
        (exact_hi.numerator * scale + exact_hi.denominator - 1) // exact_hi.denominator, scale
    )
    assert pi_lo <= exact_lo < exact_hi <= pi_hi and pi_hi - pi_lo <= Fraction(2, scale)
    assert 3 < pi_lo < pi_hi < Fraction(22, 7)
    # 0<=x<=pi. Independent uncertain Horner factors produce at most the
    # absolute-polynomial derivative times the z interval width. Bound that
    # derivative by exp(10)<3**10, since z=x*x<10 and (2j)!>=j!.
    z_width = 8 * (pi_hi - pi_lo)
    remainder = Fraction(22, 7) ** 122 / factorial(122)
    interval_width = 32 * (z_width * 3**10 + 2 * remainder)
    assert interval_width < Fraction(1, 1 << 40)
    floor_error = Fraction(1, 1 << 40) + interval_width / 2
    assert floor_error < Fraction(2, 1 << 40)
    return dict(
        passed=True,
        all_QPE_outcomes_covered=True,
        cosine_Taylor_degree=120,
        outward_pi_dyadic_bits=160,
        actual_outward_pi_enclosure=[pair(pi_lo), pair(pi_hi)],
        independent_uniform_price_enclosure_width_upper=pair(interval_width),
        midpoint_native40_floor_error_upper=pair(floor_error),
        charged_readout_error=[2, 1 << 40],
        price_already_discounted=True,
        extra_discount_applied=False,
        quantum_price_run=False,
    )


def xml_cases(path):
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root)
    cases = [case for suite in suites for case in suite.findall("testcase")]
    unique = {(case.get("classname"), case.get("name")) for case in cases}
    assert len(unique) == len(cases) == sum(int(s.get("tests", 0)) for s in suites)
    assert all(
        int(s.get(field, 0)) == 0 for s in suites for field in ("failures", "errors", "skipped")
    )
    return unique


def receipt_files(directory):
    """Resolve both rooted receipts and the original A10 relative Windows names."""
    directory = Path(directory).resolve()
    manifest = read(directory / "manifest.json")
    result = {}
    if "files" in manifest:
        assert isinstance(manifest["files"], dict) and isinstance(manifest["frozen_inputs"], dict)
        result.update(manifest["files"])
        result.update(manifest["frozen_inputs"])
    else:
        assert manifest and all(
            isinstance(digest, str) and len(digest) == 64 for digest in manifest.values()
        )
        for name, digest in manifest.items():
            file = (directory / name.replace("\\", "/")).resolve()
            file.relative_to(directory)
            result[relative(file)] = digest
    protocol = read(directory / "protocol.json")
    result.update(protocol.get("frozen_inputs", {}))
    result.update(protocol.get("leaf_receipt_frozen_inputs", {}))
    result.update(
        {
            item["source"].replace("\\", "/"): item["sha256"]
            for item in protocol.get("executed_dependencies", [])
        }
    )
    result[relative(directory / "manifest.json")] = sha(directory / "manifest.json")
    verify(result)
    return result


def audit_marking_records(case, records, source, target, spec):
    historical = read(BASELINE / case / "comparison.json")
    sample = next(
        row for row in historical["replays"] if row["label"] == spec["original_saved_label"]
    )
    _, trace = evaluate(target, sample["inputs"], True)
    y = int(trace[target["outputs"]["Y"]])
    assert 0 < y < 1 << 46
    assert len(records) == spec["count"] == (4 if case == "B4x12" else 2)
    expected = [
        (offset, control)
        for offset in spec["selector_boundary_offsets"]
        for control in spec["controls"]
    ]
    for row, (offset, control) in zip(records, expected, strict=True):
        assert (
            row["passed"]
            and row["inputs"] == sample["inputs"]
            and row["original_label"] == sample["label"]
        )
        assert row["expected_y_raw"] == y
        actual = row["actual"]
        assert (
            actual["case"] == case
            and actual["y_raw"] == y
            and actual["selector_value"] == y + offset
        )
        assert actual["control"] == control and actual["marked"] == (offset < 0)
        assert actual["controlled_phase"] == (-1 if control and offset < 0 else 1)
        assert (
            actual["all_input_selector_control_and_workspace_restored"]
            and actual["source_inverse_is_literal_gate_reverse"]
        )
        assert not actual["full_reflection_statevector_executed"]
    assert set(sample["inputs"]) == {node["params"]["name"] for node in source["inputs"]}
    assert all(0 <= value < 1 << 32 for value in sample["inputs"].values())
    return dict(
        passed=True,
        case=case,
        recorded_source_marking_replays=len(records),
        native_y_raw=y,
        exact_selector_strict_boundary_verified=True,
        all_recorded_workspace_cleanup=True,
        whole_financial_QPE_or_reflection_executed=False,
        new_financial_gate_replays=0,
    )


def prepare(producer, output):
    producer, output = Path(producer).resolve(), Path(output).resolve()
    producer.relative_to(PROGRAM)
    output.relative_to(PROGRAM)
    assert read(producer / "summary.json")["passed"] and not output.exists()
    frozen = {}
    directories = [
        BASELINE,
        SCHEDULE,
        PROGRAM / "E03_support_run001",
        PROGRAM / "E03_support_audit_run002",
        producer,
    ]
    failed = PROGRAM / "E02_financial_run001"
    if producer != failed and (failed / "manifest.json").exists():
        directories.append(failed)
    for directory in directories:
        frozen.update(receipt_files(directory))
    own = Path(__file__).resolve()
    frozen[relative(own)] = sha(own)
    dependency = ROOT / "research/limitation_program_20261001/compact_ledger.py"
    frozen[relative(dependency)] = sha(dependency)
    verify(frozen)
    output.mkdir()
    shutil.copy2(own, output / "executed_audit_financial_estimator.py")
    save(
        output / "protocol.json",
        dict(
            local_only=True,
            created_utc=datetime.now(timezone.utc).isoformat(),
            before_independent_audit=True,
            producer=relative(producer),
            frozen_inputs=frozen,
            interpreter_sha256=sha(sys.executable),
            cases=["B4x12", "B8x52"],
            actual_source_marking_records=6,
            historical_clean_XOR_financial_replays=41,
            toy_unitary_arrays=3,
            tiny_unitary_negative_controls="Omit final controlled Z in memory and reject wrong branch relative sign",
            scope="Actual native F and literal-inverse array costs, guarded source bindings, private allocation, selector46/supportspan64, old named-Y buffer reuse,16 nonalias QPE controls, fresh-shot/QPE/IQFT/readout counts, independent rational pi and binomial bounds, complete tiny-G unitary/negative control, six recorded source marking replays, exact null synthesis/physical/continuous-price obligations",
            new_financial_candidates=0,
            new_financial_gate_replays=0,
            huge_QPE_runs=0,
            new_distinct_pytest_cases=0,
            independent_pi_identity="pi=4*(atan(1/2)+atan(1/3)),240 terms each; tangent addition exactly1",
            G2_to_G5="open",
        ),
    )
    print("Independent financial estimator audit protocol frozen", flush=True)


def run(output):
    output = Path(output).resolve()
    assert not (output / "summary.json").exists()
    protocol = read(output / "protocol.json")
    verify(protocol["frozen_inputs"])
    assert sha(sys.executable) == protocol["interpreter_sha256"]
    producer = ROOT / protocol["producer"]
    superseded_directory = PROGRAM / "E02_financial_run001"
    superseded = read(superseded_directory / "summary.json")
    assert not superseded["passed"] and superseded["static_preflight_incompatibility_confirmed"]
    assert (
        not superseded["source_binding_rejection_executed"]
        and not superseded["test_execution_completed"]
    )
    assert (
        superseded["planned_tests"] == 51 and superseded["completed_distinct_tests_credited"] == 0
    )
    assert (
        superseded["financial_wrappers_emitted"]
        == superseded["source_marking_replays"]
        == superseded["full_QPE_runs"]
        == 0
    )
    assert (
        not superseded["frozen_files_edited"] and not (superseded_directory / "tests.xml").exists()
    )
    assert (
        not (superseded_directory / "B4x12").exists()
        and not (superseded_directory / "B8x52").exists()
    )
    old_tree = ast.parse(
        (superseded_directory / "executed_code/native_payoff_estimator.py").read_text(
            encoding="utf-8"
        )
    )
    old_reader = next(
        node
        for node in old_tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "_verify_receipt"
    )
    strict_schema = [
        node
        for node in ast.walk(old_reader)
        if isinstance(node, ast.Compare)
        and len(node.ops) == 1
        and isinstance(node.ops[0], ast.NotEq)
        and isinstance(node.comparators[0], ast.Set)
    ]
    assert any(
        {item.value for item in node.comparators[0].elts} == {"files", "frozen_inputs"}
        for node in strict_schema
    )
    accepted_manifest = read(PROGRAM / "E03_support_audit_run002/manifest.json")
    assert (
        set(accepted_manifest) == {"files", "frozen_inputs", "manifest_self_hash_excluded"}
        and accepted_manifest["manifest_self_hash_excluded"] is True
    )
    save(
        output / "preserved_superseded_preflight_audit.json",
        dict(
            passed=True,
            record=superseded,
            incompatible_exact_schema_independently_confirmed=True,
            completed_test_credit=0,
            actual_rejected_binding_executions=0,
            financial_wrappers=0,
            source_marking_replays=0,
        ),
    )
    prospective, summary = read(producer / "protocol.json"), read(producer / "summary.json")
    assert summary["passed"] and prospective["cases"] == ["B4x12", "B8x52"]
    assert prospective["normalization"] == dict(
        selector_bits=46,
        dollar_span=64,
        probability="E[already discounted nativeY]/64",
        second_discount=False,
    )
    assert prospective["qpe"] == dict(M=65536, bits=16, serial_fresh_shots=15)
    assert prospective["old_full_clean_XOR_financial_replay_total_unchanged"] == 41
    assert prospective["large_QPE_statevector_or_price_runs"] == 0
    schedule, complete = (
        read(SCHEDULE / "schedule.json"),
        read(SCHEDULE / "complete_price_ledger.json"),
    )
    rational = audit_rational_schedule(schedule, complete)
    save(output / "rational_schedule_audit.json", rational)
    readout = audit_readout_precision(schedule)
    save(output / "uniform_readout_precision_audit.json", readout)
    producer_tests, schedule_tests = (
        xml_cases(producer / "tests.xml"),
        xml_cases(SCHEDULE / "tests.xml"),
    )
    assert len(schedule_tests) == 24
    classes = Counter(classname.rsplit(".", 1)[-1] for classname, name in producer_tests)
    assert (
        classes["test_native_payoff_estimator_v2"] == 44
        and classes["test_bounded_price_readout_v2"] == 7
        and classes["test_financial_estimator_ledger"] == 4
    )
    negative_names = (
        "test_reject_unproved_selector_dimensions",
        "test_incompatible_contracts_fail_before_pricing_claim",
        "test_unknown_receipt_schema_is_rejected",
        "test_final_control_z_is_required_for_correct_relative_phase",
        "test_native_binding_rejects_a_different_financial_case_before_loading",
        "test_native_binding_rejects_an_unaccepted_arithmetic_receipt_before_loading",
        "test_extended_resource_reader_rejects_gate_forgery",
    )
    assert all(
        any(name.startswith(prefix) for _, name in producer_tests) for prefix in negative_names
    )
    reports, ledger_reports, marking_reports = [], [], []
    for case in prospective["cases"]:
        directory = producer / case
        wrapper, row = read(directory / "iterate.json"), read(directory / "estimator_ledger.json")
        assert Path(wrapper["selector_file"]).resolve() == (directory / "selector.npy").resolve()
        assert (
            Path(wrapper["reflection_file"]).resolve() == (directory / "reflection.npy").resolve()
        )
        wrapper_report, source, target = audit_wrapper(wrapper)
        ledger_report = audit_ledger(row, wrapper, schedule)
        assert row["wrapper"] == relative(directory / "iterate.json") and row[
            "wrapper_sha256"
        ] == sha(directory / "iterate.json")
        marking_report = audit_marking_records(
            case,
            read(directory / "marking_replays.json"),
            source,
            target,
            prospective["actual_marking_replays"][case],
        )
        assert row["actual_marking_replays"] == marking_report["recorded_source_marking_replays"]
        expected_summary = dict(
            case=case,
            source_graph_directions=1966050,
            source_iterate_resources=wrapper["resources"],
            logical_qubits=row["logical_qubits"],
            fixed_T_count=row["complete_known_T_count_excluding_arbitrary_rotation_synthesis"],
            serial_known_T_depth=row["serial_known_T_depth_excluding_arbitrary_rotation_synthesis"],
            iqft_arbitrary_Rz_rotations=row["iqft_arbitrary_Rz_rotations"],
            marking_replays=row["actual_marking_replays"],
        )
        assert (
            next(item for item in summary["case_rows"] if item["case"] == case) == expected_summary
        )
        save(output / (case + "_wrapper_audit.json"), wrapper_report)
        save(output / (case + "_ledger_audit.json"), ledger_report)
        save(output / (case + "_marking_record_audit.json"), marking_report)
        reports.append(wrapper_report)
        ledger_reports.append(ledger_report)
        marking_reports.append(marking_report)
        print(case, "independent wrapper/ledger/recorded marking audit PASS", flush=True)
    toy_specs = read(producer / "toys/toys.json")
    assert [spec["kind"] for spec in toy_specs] == [
        "positive-two-point",
        "positive-rare-event",
        "shifted-negative-two-point",
    ]
    toys = []
    for spec in toy_specs:
        file = Path(spec["gate_file"]).resolve()
        assert file == (producer / "toys" / (spec["kind"] + ".npy")).resolve()
        toys.append(audit_toy(spec, file))
        print(spec["kind"], "independent complete controlled-unitary audit PASS", flush=True)
    save(output / "tiny_full_iterate_unitary_audit.json", toys)
    assert (
        summary["controlled_grover_calls"] == 983025
        and summary["new_source_marking_gate_replays"] == 6
    )
    assert (
        summary["new_complete_clean_XOR_financial_replays"] == 0
        and summary["historical_complete_clean_XOR_financial_replays"] == 41
    )
    assert summary["quantum_price_estimates_run"] == summary["full_QPE_statevector_runs"] == 0
    assert (
        summary["ideal_digital_mean_certificate"]
        and not summary["full_continuous_price_certificate"]
        and not summary["full_synthesis_or_physical_cost_certificate"]
    )
    assert (
        summary["no_C4_residual_counts_transferred_to_B4_B8"]
        and summary["preferred_latency_source_unchanged"]
        and summary["G2_to_G5"] == "open"
    )
    result = dict(
        passed=True,
        local_only=True,
        independent_actual_native_source_estimator_audit=True,
        cases=[dict(case=report["case"], resources=report["resources"]) for report in reports],
        M=65536,
        qpe_bits=16,
        serial_fresh_shots=15,
        controlled_G_calls=983025,
        producer_distinct_pytest_cases_reconciled=len(producer_tests),
        schedule_distinct_pytest_cases_reconciled=len(schedule_tests),
        preserved_interrupted_v1_completed_test_credit=0,
        preserved_interrupted_v1_wrappers_and_replays=0,
        new_distinct_pytest_cases=0,
        tiny_full_G_unitary_arrays_verified=len(toys),
        tiny_clean_subspace_columns_verified=sum(
            toy["complete_clean_subspace_columns"] for toy in toys
        ),
        missing_control_Z_negative_controls_rejected=3,
        recorded_financial_source_marking_replays_reconciled=6,
        historical_clean_XOR_financial_replays_unchanged=41,
        new_financial_gate_replays=0,
        new_financial_candidates=0,
        huge_QPE_executions=0,
        full_T_count=None,
        full_T_depth=None,
        synthesis_certificate=None,
        physical_runtime_seconds=None,
        readout_or_reset_seconds=None,
        full_continuous_price_certificate=False,
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
    print("Independent financial estimator audit complete", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "run"))
    parser.add_argument("--producer", type=Path, default=PROGRAM / "E02_financial_run002")
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
                    new_financial_candidates=0,
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
