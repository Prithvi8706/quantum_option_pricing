"""Actual reversible modular updates for the monitored streaming harness.

These are permutations on the full advertised registers. The three-bit counter
does not discard an alive flag: it stores the sum of four Boolean violations,
and its complete inverse restores that information after the output XOR.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

from research.controlled_source_completion.primitives import array_gates, gate_resources, mcx
from research.journal_sprint.reversible_fixed_point import Program, add


FORMAT = "exact-in-place-streaming-update-v1"
KINDS = ("add", "controlled-increment", "counter-is-zero")


def build_update(kind, width=72, counter_bits=3):
    """Return emitted gates and explicit preserved/mutated register bindings."""
    if kind not in KINDS:
        raise ValueError("undeclared reversible streaming update")
    if type(width) is not int or width < 1:
        raise ValueError("positive native word width required")
    if type(counter_bits) is not int or counter_bits < 1:
        raise ValueError("positive counter width required")
    program = Program(compact=True)
    if kind == "add":
        source, target = program.register(width), program.register(width)
        helper = program.register(1)
        add(program, source, target, helper[0])
        arguments, outputs = [source], [target]
        semantics = "target += source modulo 2**width; source and helper restored"
    elif kind == "controlled-increment":
        flag, target = program.register(1), program.register(counter_bits)
        extension, helper = program.register(counter_bits), program.register(1)
        program.gate(flag[0], extension[0])
        add(program, extension, target, helper[0])
        program.gate(flag[0], extension[0])
        arguments, outputs = [flag], [target]
        semantics = "counter += flag modulo 2**counter_bits; flag/extension/helper restored"
    else:
        counter, target = program.register(counter_bits), program.register(1)
        scratch = program.register(max(1, counter_bits - 2))
        for wire in counter:
            program.gate(wire)
        mcx(program, counter, target[0], scratch)
        for wire in counter:
            program.gate(wire)
        arguments, outputs = [counter], [target]
        semantics = "target XOR= (counter == 0); counter and helper restored"
    return program, {
        "kind": kind,
        "args": [list(r) for r in arguments],
        "outs": [list(r) for r in outputs],
        "semantics": semantics,
        "word_width": width,
        "counter_bits": counter_bits,
        "preserved_input_registers": True,
        "target_is_mutable": kind != "counter-is-zero",
        "inverse": "literal gate-array reverse",
    }


def emit_updates(directory, width=72, counter_bits=3):
    """Emit arrays and measured forward/reverse costs after protocol freeze."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=False)
    results = {}
    for kind in KINDS:
        program, bindings = build_update(kind, width, counter_bits)
        gates = array_gates(program)
        file = directory / (kind + ".npy")
        np.save(file, gates)
        costs = {}
        for direction, array in (("forward", gates), ("inverse", gates[::-1])):
            counted, td, ctd = gate_resources(array, program.qubits)
            x, cx, ccx = map(int, counted)
            costs[direction] = {
                "source_gates": len(gates),
                "x": x,
                "cx": cx,
                "ccx": ccx,
                "t_count": 7 * ccx,
                "clifford_cx": cx + 6 * ccx,
                "clifford_h": 2 * ccx,
                "t_depth": int(td),
                "clifford_t_depth": int(ctd),
            }
        metadata = {
            "format": FORMAT,
            **bindings,
            "qubits": program.qubits,
            "gate_file": file.name,
            "sha256": hashlib.sha256(file.read_bytes()).hexdigest(),
            "costs": costs,
        }
        (directory / (kind + ".json")).write_text(
            json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
        )
        results[kind] = metadata
    return results


def validate_counter_bound(dates, counter_bits):
    if type(dates) is not int or dates < 1 or type(counter_bits) is not int:
        raise ValueError("positive finite monitoring count required")
    if counter_bits < 1 or dates >= 1 << counter_bits:
        raise ValueError("counter cannot retain every possible monitoring violation")
    return {
        "maximum_violations": dates,
        "counter_bits": counter_bits,
        "no_modular_wrap_on_forward_monitoring": True,
        "reason": "Each monitored date contributes exactly one Boolean; initial count is zero",
    }
