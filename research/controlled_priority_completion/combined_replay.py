"""Execute composed range/wave financial, phase and selector source passes."""

import copy
from fractions import Fraction
import json
from pathlib import Path

import numpy as np

from research.controlled_priority_completion.estimator_bounded import (
    emitted_wrapper,
    shifted_selector,
)
from research.controlled_priority_completion.parallel_source import apply_half
from research.controlled_source_completion.compiler import mapped_gates
from research.controlled_source_completion.ir import evaluate
from research.controlled_source_completion.run import dump

ROOT = Path("results/controlled_priority_completion")


def put(state, offset, raw, width):
    for bit in range(width):
        state[offset + bit] = (raw >> bit) & 1


def take(state, offset, width):
    return sum(int(state[offset + bit]) << bit for bit in range(width))


def main():
    cases = json.loads(
        Path(
            "results/controlled_source_completion/validation_v2/full_source_basis.json"
        ).read_text()
    )
    phase_dir = Path("results/controlled_completion_followup/arithmetic_v1/compile_v2/phase_f64")
    phase = json.loads((phase_dir / "source.json").read_text())
    phase_target = json.loads((phase_dir / "target.json").read_text())
    phase_schedule = json.loads((ROOT / "parallel_v1/phase_f64_limit_all.json").read_text())
    selector, ins, outs = shifted_selector()
    selector_gates = np.frombuffer(selector.gates.data, dtype=np.int32).reshape(-1, 4)
    rows = []
    allocations = json.loads((ROOT / "estimator_hadamard.json").read_text())
    for name in ("C4", "H8"):
        directory = ROOT / "range_compile_v1" / (name + "_f40")
        source_path = directory / "source.json"
        source = json.loads(source_path.read_text())
        target = json.loads((directory / "target.json").read_text())
        schedule_path = ROOT / "range_parallel_v1" / (name + "_f40_limit_all.json")
        schedule = json.loads(schedule_path.read_text())
        inputs = next(c["inputs"] for c in cases if c["model"] == name and c["fraction_bits"] == 40)
        _, values = evaluate(target, inputs, True)
        y = values[target["outputs"]["Y_6"]]
        signed_y = y - (1 << 72) if y >= (1 << 71) else y
        logical_source = copy.deepcopy(source)
        logical_source["resources"] = schedule["resources"]
        wrapper = emitted_wrapper(logical_source, source_path, selector, ins, outs)
        for operation in wrapper["operations"]:
            if operation["gate"] == "call_graph_half":
                operation.update(gate="call_wave_half", wave_schedule=schedule_path.as_posix())
        dump(ROOT / ("combined_" + name + "_bounded_wrapper.json"), wrapper)
        mapping = np.array(wrapper["selector_wire_mapping"], np.int64)
        observations, cache = [], {}
        for selector_value in (signed_y + (128 << 40) - 1, signed_y + (128 << 40)):
            state = np.zeros(wrapper["qpe_register_base"], np.uint8)
            for node in source["inputs"]:
                put(state, node["out"][0] * 72, inputs[node["params"]["name"]], 72)
            for bit, wire in enumerate(ins[1]):
                state[mapping[wire]] = (selector_value >> bit) & 1
            before = state.copy()
            apply_half(source, schedule, state, cache=cache)
            mapped_gates(selector_gates, state, mapping, False)
            marked = bool(state[mapping[outs[0]]])
            assert marked == (selector_value < signed_y + (128 << 40))
            mapped_gates(selector_gates, state, mapping, True)
            apply_half(source, schedule, state, inverse=True, cache=cache)
            assert np.array_equal(state, before)
            observations.append(dict(selector_value=selector_value, marked=marked, cleanup=True))
        base = schedule["resources"]["logical_qubits"]
        state = np.zeros(base + phase_schedule["resources"]["logical_qubits"], np.uint8)
        for node in source["inputs"]:
            put(state, node["out"][0] * 72, inputs[node["params"]["name"]], 72)
        allocation = next(
            row["allocation"]
            for row in allocations
            if row["model"] == name and row["mode"] == "continuous_moment_conditional"
        )
        radius = Fraction(*allocation["initial_radius_exact"])
        contraction = Fraction(*allocation["contraction_exact"])
        phase_inputs = dict(
            Y=signed_y << 24,
            left=round(-radius * contraction * (1 << 64)),
            scale_exponent=allocation["normalizer"].bit_length() - 1,
        )
        phase_offsets = {n["params"]["name"]: base + n["out"][0] * 96 for n in phase["inputs"]}
        for key in ("left", "scale_exponent"):
            put(state, phase_offsets[key], phase_inputs[key], 96)
        before = state.copy()
        apply_half(source, schedule, state, cache=cache)
        source_offset = source["outputs"]["Y_6"] * 72
        phase_y = phase_offsets["Y"] + 24
        state[phase_y : phase_y + 72] ^= state[source_offset : source_offset + 72]
        apply_half(phase, phase_schedule, state, base=base, cache=cache)
        _, phase_values = evaluate(phase_target, phase_inputs, True)
        actual_angle = take(state, base + phase["outputs"]["angle"] * 96, 96)
        expected_angle = phase_values[phase_target["outputs"]["angle"]]
        assert actual_angle == expected_angle
        apply_half(phase, phase_schedule, state, base=base, inverse=True, cache=cache)
        state[phase_y : phase_y + 72] ^= state[source_offset : source_offset + 72]
        apply_half(source, schedule, state, inverse=True, cache=cache)
        assert np.array_equal(state, before)
        rows.append(
            dict(
                model=name,
                raw_Y=signed_y,
                selector=observations,
                phase_raw_angle=actual_angle,
                phase_inputs=phase_inputs,
                phase_cleanup=True,
                scope="Full composed emitted basis gates, not full QAE or hardware timing",
            )
        )
        dump(ROOT / "combined_replay.json", rows)
        print(json.dumps(rows[-1]), flush=True)


if __name__ == "__main__":
    main()
