"""Emit and execute a small nonlinear path with paid reversible recomputation."""

import argparse
from pathlib import Path

from research.controlled_source_completion.primitives import basis_run, build, resources
from research.journal_sprint.reversible_fixed_point import Program
from research.limitation_audit_20261001.experiment_lookup import dump


def path_circuit(width, steps, recompute):
    if steps < 2 or steps & (steps - 1):
        raise ValueError("use a power of two number of steps")
    leaf, leaf_args, leaf_outs = build("mul", width, 0)
    p = Program(compact=True)
    initial, output = p.register(width), p.register(width)
    kept = steps.bit_length() - 1 if recompute else steps - 1
    checkpoints = [p.register(width) for _ in range(kept)]
    private = p.register(leaf.qubits - width)
    calls = []

    def step(a, b):
        # Copy both operands separately so a*a never aliases two Toffoli controls.
        mapping = {}
        cursor = 0
        for wire in range(leaf.qubits):
            if wire in leaf_outs[0]:
                mapping[wire] = b[leaf_outs[0].index(wire)]
            else:
                mapping[wire] = private[cursor]
                cursor += 1
        for operand in leaf_args:
            for source, target in zip(a, operand):
                p.gate(source, mapping[target])
        for gate in leaf.gates:
            p.gate(*(mapping[wire] for wire in gate))
        for operand in leaf_args:
            for source, target in zip(a, operand):
                p.gate(source, mapping[target])
        calls.append(dict(source=list(a), target=list(b)))

    def bridge(a, b, count, pool):
        if count == 1:
            step(a, b)
        else:
            midpoint = pool[0]
            bridge(a, midpoint, count // 2, pool[1:])
            bridge(midpoint, b, count // 2, pool[1:])
            bridge(a, midpoint, count // 2, pool[1:])

    if recompute:
        bridge(initial, output, steps, checkpoints)
    else:
        chain = [initial, *checkpoints, output]
        for index in range(steps):
            step(chain[index], chain[index + 1])
        for index in reversed(range(steps - 1)):
            step(chain[index], chain[index + 1])
    return p, [initial], [output], calls


def run(output):
    output.mkdir(parents=True, exist_ok=False)
    width, steps = 5, 8
    rows = []
    for name, recompute in (("retain", False), ("recompute", True)):
        p, args, outs, calls = path_circuit(width, steps, recompute)
        for value in range(1 << width):
            expected = value
            for _ in range(steps):
                expected = expected * expected % (1 << width)
            for initial in (0, 19):
                actual, clean, preserved, _ = basis_run(p, args, outs, [value], [initial])
                assert (actual, clean, preserved) == ([initial ^ expected], True, True)
                restored, clean, preserved, _ = basis_run(p, args, outs, [value], actual, True)
                assert (restored, clean, preserved) == ([initial], True, True)
        rows.append(dict(name=name, resources=resources(p), leaf_calls=len(calls),
                         schedule=calls, every_input_and_inverse_passed=True))
        print(name, p.qubits, "qubits", len(calls), "paid leaf calls", flush=True)
    assert rows[1]["resources"]["qubits"] < rows[0]["resources"]["qubits"]
    assert rows[1]["resources"]["t_count"] > rows[0]["resources"]["t_count"]
    dump(output / "summary.json", dict(width=width, steps=steps, cases=rows, passed=True,
        transition="x_next = x*x modulo 32; deliberately isolated nonlinear path",
        disposition="Keep as a verified memory/time tradeoff. It reduces workspace "
        "and increases arithmetic. It has not yet been applied to a full financial path.",
        scope="Both variants emit exact X/CX/CCX circuits and clean all checkpoints. "
        "This tests the scheduler, not the financial suitability of the toy transition."))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output)
