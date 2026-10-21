"""Verify measurement cleanup of a temporary AND, including coherent inputs.

This is an isolated, ideal-circuit experiment, not a production compiler change.
Uses only the Python standard library. Qubit order: a, b, temporary, y, reference.
"""

import argparse
import json
import math
import platform
import random
from pathlib import Path


SIZE = 32
TEMP = 2
LOGICAL_BITS = (0, 1, 3, 4)


def controlled_x(state, controls, target):
    result = [0j] * SIZE
    for index, amplitude in enumerate(state):
        destination = index
        if all((index >> bit) & 1 for bit in controls):
            destination ^= 1 << target
        result[destination] += amplitude
    return result


def hadamard(state, bit):
    result = [0j] * SIZE
    for index, amplitude in enumerate(state):
        low = index & ~(1 << bit)
        high = low | (1 << bit)
        result[low] += amplitude / math.sqrt(2)
        result[high] += (-1 if (index >> bit) & 1 else 1) * amplitude / math.sqrt(2)
    return result


def compute_and_use(state):
    return controlled_x(controlled_x(state, (0, 1), TEMP), (TEMP,), 3)


def unitary_cleanup(state):
    return controlled_x(compute_and_use(state), (0, 1), TEMP)


def measured_cleanup_branch(state, outcome, correction=True):
    state = hadamard(compute_and_use(state), TEMP)
    result = [0j] * SIZE
    for index, amplitude in enumerate(state):
        if ((index >> TEMP) & 1) != outcome:
            continue
        # CZ(a,b) conditioned CLASSICALLY on outcome, followed by resetting t.
        phase = -1 if correction and outcome and (index & 1) and (index & 2) else 1
        result[index & ~(1 << TEMP)] += phase * amplitude
    return result


def max_difference(left, right):
    return max(abs(a - b) for a, b in zip(left, right))


def norm_squared(state):
    return sum(abs(amplitude) ** 2 for amplitude in state)


def overlap(left, right):
    return sum(a.conjugate() * b for a, b in zip(left, right))


def basis_index(logical_index):
    return sum(((logical_index >> j) & 1) << bit for j, bit in enumerate(LOGICAL_BITS))


def run():
    branch_error = 0.0
    probability_error = 0.0
    reference_error = 0.0
    states = []
    # All columns of each Kraus operator on the t=0 input subspace.
    # Equality of these columns establishes coherent linear-map equality,
    # rather than merely equality of classical measurement probabilities.
    for logical_index in range(16):
        state = [0j] * SIZE
        state[basis_index(logical_index)] = 1.0 + 0j
        states.append(state)
    rng = random.Random(20261001)
    for _ in range(64):
        state = [0j] * SIZE
        for logical_index in range(16):
            state[basis_index(logical_index)] = complex(rng.gauss(0, 1), rng.gauss(0, 1))
        length = math.sqrt(norm_squared(state))
        states.append([amplitude / length for amplitude in state])

    for state in states:
        ideal = controlled_x(state, (0, 1), 3)
        reference_error = max(reference_error, max_difference(unitary_cleanup(state), ideal))
        for outcome in (0, 1):
            branch = measured_cleanup_branch(state, outcome)
            expected = [amplitude / math.sqrt(2) for amplitude in ideal]
            branch_error = max(branch_error, max_difference(branch, expected))
            probability_error = max(probability_error, abs(norm_squared(branch) - 0.5))

    # A deliberate broken variant exposes the phase damage if CZ is omitted.
    plus_inputs = [0j] * SIZE
    for index in range(4):
        plus_inputs[index] = 0.5 + 0j
    ideal = controlled_x(plus_inputs, (0, 1), 3)
    broken_fidelity = sum(
        abs(overlap(ideal, measured_cleanup_branch(plus_inputs, outcome, False))) ** 2
        for outcome in (0, 1)
    )
    passed = (
        branch_error < 1e-12
        and probability_error < 1e-12
        and reference_error < 1e-12
        and abs(broken_fidelity - 0.625) < 1e-12
    )
    result = {
        "experiment": "temporary_and_measurement_cleanup",
        "python": platform.python_version(),
        "basis_columns": 16,
        "seeded_complex_superpositions_with_reference": 64,
        "measurement_branches_per_input": 2,
        "max_kraus_column_or_state_error": branch_error,
        "max_branch_probability_error": probability_error,
        "max_unitary_reference_error": reference_error,
        "negative_control_fidelity_without_phase_correction": broken_fidelity,
        "passed": passed,
        "scope": "Ideal five-qubit channel on the temporary=0 subspace only.",
        "cleanup_resources": {
            "baseline": {"ccx": 1, "t_under_existing_exact_7t_lowering": 7},
            "replacement": {
                "h": 1,
                "measurement": 1,
                "conditional_cz_max": 1,
                "conditional_reset_x_max": 1,
                "t": 0,
            },
        },
        "not_measured": [
            "4T temporary-AND preparation circuit",
            "production compiler occurrence count and eligibility",
            "full-source T count or depth savings",
            "fault-tolerant measurement, feedback and routing latency",
            "end-to-end price or quantum advantage",
        ],
    }
    if not passed:
        raise AssertionError(result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    serialized = json.dumps(result, indent=2) + "\n"
    if args.output is not None:
        # Preserve any earlier experiment record instead of overwriting it.
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as stream:
            stream.write(serialized)
    print(serialized, end="")


if __name__ == "__main__":
    main()
