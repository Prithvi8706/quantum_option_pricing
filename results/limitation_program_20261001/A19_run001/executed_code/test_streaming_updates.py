"""Exhaustive primitive permutations and paid earlier-state snapshot cleanup."""

from itertools import product

import pytest

from research.controlled_source_completion.primitives import basis_run, build
from research.journal_sprint.reversible_fixed_point import (
    Program,
    add,
    basis,
    constant,
    copy,
    read,
    subtract,
)
from research.limitation_program_20261001.streaming_updates import (
    build_update,
    validate_counter_bound,
)


@pytest.mark.parametrize("width", [1, 2, 3, 4, 5])
def test_native_modular_add_all_inputs_and_dirty_targets(width):
    program, entry = build_update("add", width, 3)
    source, target = entry["args"][0], entry["outs"][0]
    occupied = set(source + target)
    mask = (1 << width) - 1
    for a, b in product(range(1 << width), repeat=2):
        initial = basis(source, a) | basis(target, b)
        actual = program.run(initial)
        assert read(actual, source) == a
        assert read(actual, target) == (a + b) & mask
        assert all(
            not (actual >> wire & 1) for wire in range(program.qubits) if wire not in occupied
        )
        inverse = Program()
        inverse.qubits = program.qubits
        inverse.gates = list(reversed(list(program.gates)))
        assert inverse.run(actual) == initial


@pytest.mark.parametrize("bits", [1, 2, 3, 4])
def test_controlled_counter_permutation_every_flag_and_old_count(bits):
    program, entry = build_update("controlled-increment", 4, bits)
    flag, counter = entry["args"][0], entry["outs"][0]
    occupied = set(flag + counter)
    for flag_raw, count in product(range(2), range(1 << bits)):
        initial = basis(flag, flag_raw) | basis(counter, count)
        actual = program.run(initial)
        assert read(actual, flag) == flag_raw
        assert read(actual, counter) == (count + flag_raw) % (1 << bits)
        assert all(
            not (actual >> wire & 1) for wire in range(program.qubits) if wire not in occupied
        )
        inverse = Program()
        inverse.qubits = program.qubits
        inverse.gates = list(reversed(list(program.gates)))
        assert inverse.run(actual) == initial


@pytest.mark.parametrize("bits", [1, 2, 3, 4])
def test_counter_zero_dirty_flag_and_restored_scratch(bits):
    program, entry = build_update("counter-is-zero", 4, bits)
    count, flag = entry["args"][0], entry["outs"][0]
    occupied = set(count + flag)
    for count_raw, dirty in product(range(1 << bits), range(2)):
        initial = basis(count, count_raw) | basis(flag, dirty)
        actual = program.run(initial)
        assert read(actual, count) == count_raw
        assert read(actual, flag) == dirty ^ int(count_raw == 0)
        assert all(
            not (actual >> wire & 1) for wire in range(program.qubits) if wire not in occupied
        )
        assert program.run(actual) == initial


@pytest.mark.parametrize("bits", [1, 2])
def test_monitoring_counter_rejects_information_losing_width(bits):
    with pytest.raises(ValueError, match="retain every"):
        validate_counter_bound(4, bits)


def test_four_monitoring_dates_count_fits_three_bits():
    assert validate_counter_bound(4, 3)["maximum_violations"] == 4
    program, entry = build_update("controlled-increment", 4, 3)
    flag, count = entry["args"][0], entry["outs"][0]
    for violations in product(range(2), repeat=4):
        state = 0
        for value in violations:
            state = (state & ~(1 << flag[0])) | (value << flag[0])
            state = program.run(state)
        assert read(state, count) == sum(violations)


def test_signed_strict_barrier_equality_and_both_signs():
    width = 4
    program, args, outs = build("lt", width, 0)
    for basket, threshold in product(range(16), repeat=2):
        signed_basket = basket - 16 if basket & 8 else basket
        signed_threshold = threshold - 16 if threshold & 8 else threshold
        values, clean, preserved, _ = basis_run(program, args, outs, [basket, threshold])
        violation = values[0] ^ 1
        assert violation == int(signed_basket >= signed_threshold)
        assert clean and preserved


def test_original_parallel_prefix_equals_mutable_unclipped_modular_state():
    # Values include signed wrap. Clipping the current state between dates would
    # violate this equality; temporary clipping preserves the integer target.
    for increments in product(range(4), repeat=4):
        width, mask, initial = 3, 7, 5
        old = [initial + increments[0], *increments[1:]]
        old = [value & mask for value in old]
        for distance in (1, 2):
            old = [
                old[j] if j < distance else (old[j] + old[j - distance]) & mask for j in range(4)
            ]
        current, observed = initial, []
        for increment in increments:
            current = (current + increment) & mask
            observed.append(current)
        assert observed == old
        assert width == 3


def test_two_date_snapshots_clear_only_after_paid_rewind_and_redo():
    width = 3
    program = Program()
    increments = [program.register(width), program.register(width)]
    raw, asian = program.register(width), program.register(width)
    snapshots = [program.register(width), program.register(width)]
    dirty_output, helper = program.register(width), program.register(1)[0]
    start = len(program.gates)
    constant(program, raw, 5)
    for date in range(2):
        add(program, increments[date], raw, helper)
        copy(program, raw, snapshots[date])
        add(program, snapshots[date], asian, helper)
    for date in reversed(range(2)):
        copy(program, raw, snapshots[date])
        subtract(program, increments[date], raw, helper)
    for date in range(2):
        add(program, increments[date], raw, helper)
    end = len(program.gates)
    copy(program, asian, dirty_output)
    program.undo(start, end)
    for a, b, dirty in product(range(8), repeat=3):
        initial = basis(increments[0], a) | basis(increments[1], b) | basis(dirty_output, dirty)
        actual = program.run(initial)
        assert read(actual, dirty_output) == dirty ^ ((10 + 2 * a + b) & 7)
        allowed = set(increments[0] + increments[1] + dirty_output)
        assert all(
            not (actual >> wire & 1) for wire in range(program.qubits) if wire not in allowed
        )
        assert read(actual, increments[0]) == a
        assert read(actual, increments[1]) == b


@pytest.mark.parametrize("kind", ["unknown", "mul", "alive-overwrite"])
def test_unproved_or_information_losing_update_rejected(kind):
    with pytest.raises(ValueError, match="undeclared"):
        build_update(kind, 72, 3)
