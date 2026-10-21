"""Full signed-domain checks for the frozen three-coefficient, six-strategy screen."""

from functools import lru_cache
import hashlib
import json
from pathlib import Path
import random

from numba import njit
import numpy as np
import pytest

from research.controlled_source_completion.compiler import resolve_library
from research.controlled_source_completion.constant_multiplier import (
    STRATEGIES as RIPPLE_STRATEGIES,
    build_constant_multiplier,
    signed_digits,
)
from research.controlled_source_completion.prefix_constant_multiplier import (
    ALGORITHM,
    LOWERING,
    STRATEGIES as PREFIX_STRATEGIES,
    VARIANT,
    build_prefix_constant_multiplier,
    leaf_spec,
    signed_constant_partial_terms,
)
from research.controlled_source_completion.primitives import (
    array_gates,
    basis_run,
    build,
    resources,
    run_gates,
)

ROOT = Path(__file__).resolve().parents[2]
BASELINE = ROOT / "results/limitation_program_20261001/A09_range_run001"
COEFFICIENTS = (1067016148260, 60222732077, 22906492245)
STRATEGIES = RIPPLE_STRATEGIES + PREFIX_STRATEGIES
SMALL_COEFFICIENTS = (-17, -7, -3, -1, 0, 1, 3, 7, 17)
NATIVE_FIXTURES = ((24, 12), (40, 23), (72, 40))


def candidate(width, fraction_bits, coefficient, strategy):
    if strategy in PREFIX_STRATEGIES:
        return build_prefix_constant_multiplier(width, fraction_bits, coefficient, strategy)
    return build_constant_multiplier(width, fraction_bits, coefficient, 0, strategy)


def independent_reference(width, fraction_bits, coefficient, raw, initial):
    """Use integer floor division with the complete native two's-complement input."""
    value = raw - (1 << width) if raw >> (width - 1) else raw
    return initial ^ ((value * coefficient // (1 << fraction_bits)) % (1 << width))


@njit(cache=True)
def exhaustive_words(gates, qubits, width, fraction_bits, coefficient):
    limit, count = 1 << width, 0
    for raw in range(limit):
        value = raw - limit if raw >> (width - 1) else raw
        expected = (value * coefficient // (1 << fraction_bits)) & (limit - 1)
        for initial_index in range(limit if width <= 3 else 3):
            initial = (
                initial_index
                if width <= 3
                else (
                    0
                    if initial_index == 0
                    else limit - 1
                    if initial_index == 1
                    else (5 * raw + coefficient) & (limit - 1)
                )
            )
            for inverse in (False, True):
                state = np.zeros(qubits, np.uint8)
                for bit in range(width):
                    state[bit] = (raw >> bit) & 1
                    state[width + bit] = (initial >> bit) & 1
                run_gates(gates, state, inverse)
                for bit in range(width):
                    if state[bit] != (raw >> bit) & 1:
                        return False, count, raw, initial, inverse, 1
                    if state[width + bit] != ((expected ^ initial) >> bit) & 1:
                        return False, count, raw, initial, inverse, 2
                for wire in range(2 * width, qubits):
                    if state[wire]:
                        return False, count, raw, initial, inverse, 3
                count += 1
    return True, count, 0, 0, False, 0


@pytest.mark.parametrize("width", range(1, 6))
@pytest.mark.parametrize("strategy", STRATEGIES)
def test_exhaustive_small_signed_inputs_all_fractions_dirty_outputs_and_inverse(width, strategy):
    for fraction_bits in range(width + 1):
        for coefficient in SMALL_COEFFICIENTS:
            program, _, _ = candidate(width, fraction_bits, coefficient, strategy)
            report = exhaustive_words(
                array_gates(program), program.qubits, width, fraction_bits, coefficient
            )
            assert report[0], (width, fraction_bits, coefficient, strategy, report)
            initial_count = (1 << width) if width <= 3 else 3
            assert report[1] == 2 * initial_count * (1 << width)


def test_independent_signed_polynomial_identity_including_coefficients_beyond_product_width():
    for width in range(1, 6):
        for fraction_bits in range(width + 1):
            mask = (1 << (width + fraction_bits)) - 1
            for coefficient in SMALL_COEFFICIENTS + (-257, 257):
                for strategy in PREFIX_STRATEGIES:
                    terms, correction = signed_constant_partial_terms(
                        width, fraction_bits, coefficient, strategy
                    )
                    for raw in range(1 << width):
                        value = raw - (1 << width) if raw >> (width - 1) else raw
                        represented = correction + sum(
                            ((1 - ((raw >> index) & 1)) if negative else ((raw >> index) & 1))
                            << column
                            for index, column, negative in terms
                        )
                        assert represented & mask == (value * coefficient) & mask


def test_negative_control_dropping_low_columns_changes_positive_floor_rounding():
    terms, correction = signed_constant_partial_terms(8, 2, 3, PREFIX_STRATEGIES[0])
    assert correction & 3 == 0
    retained = correction + sum(
        ((1 - ((3 >> index) & 1)) if negative else ((3 >> index) & 1)) << column
        for index, column, negative in terms
        if column >= 2
    )
    assert (retained & 1023) >> 2 == 1
    assert (3 * 3) // 4 == 2


def test_negative_control_short_correction_modulus_loses_signed_floor_high_ones():
    width, fraction_bits, raw = 8, 6, 255
    terms, correction = signed_constant_partial_terms(width, fraction_bits, 1, PREFIX_STRATEGIES[0])
    complemented = sum(
        ((1 - ((raw >> index) & 1)) if negative else ((raw >> index) & 1)) << column
        for index, column, negative in terms
    )
    assert correction >> width != 0
    full = (complemented + correction) & ((1 << (width + fraction_bits)) - 1)
    short = (complemented + correction) & ((1 << width) - 1)
    assert full >> fraction_bits == (-1 // 64) % 256 == 255
    assert short >> fraction_bits != 255
    assert (raw // 64) % 256 != 255  # Unsigned substitution is also incorrect.


@lru_cache(maxsize=None)
def historical_leaf(width, fraction_bits, coefficient):
    program, args, outs = build("cmul", width, fraction_bits, {"c": coefficient})
    if (width, fraction_bits) == (72, 40):
        source = json.loads((BASELINE / "B4x12/source.json").read_text(encoding="utf-8"))
        archive = resolve_library(source)
        entries = [
            json.loads((archive / (key + ".json")).read_text(encoding="utf-8"))
            for key in source["library_keys"]
        ]
        matches = [
            entry
            for entry in entries
            if entry["op"] == "cmul" and entry["params"] == {"c": coefficient}
        ]
        assert len(matches) == 1
        entry = matches[0]
        gate_file = archive / entry["gate_file"]
        assert hashlib.sha256(gate_file.read_bytes()).hexdigest() == entry["sha256"]
        assert np.array_equal(array_gates(program), np.load(gate_file, allow_pickle=False))
        assert [list(reg) for reg in args] == entry["args"]
        assert [list(reg) for reg in outs] == entry["outs"]
        assert resources(program) == entry["resources"]
    return program, args, outs


@pytest.mark.parametrize("coefficient", COEFFICIENTS)
def test_historical_full_native_cmul_matches_actual_accepted_archive(coefficient):
    old, args, outs = historical_leaf(72, 40, coefficient)
    assert old.qubits == 433
    assert args == [tuple(range(72))] and outs == [tuple(range(72, 144))]


@lru_cache(maxsize=None)
def production_vectors(width, fraction_bits):
    mask = (1 << width) - 1
    values = {0, 1, 2, 3, mask, mask - 1, mask - 2, 1 << (width - 1)}
    for power in sorted(
        {1, width // 2, fraction_bits - 1, fraction_bits, fraction_bits + 1, width - 2, width - 1}
    ):
        if 0 <= power < width:
            for difference in (-1, 0, 1):
                values.add(((1 << power) + difference) & mask)
                values.add((-(1 << power) + difference) & mask)
    values.update(
        (int("a5" * ((width + 7) // 8), 16) & mask, int("5a" * ((width + 7) // 8), 16) & mask)
    )
    rng = random.Random(20261002 + 100 * width + fraction_bits)
    words = sorted(values) + [rng.getrandbits(width) for _ in range(64)]
    return tuple((raw, rng.getrandbits(width) | (1 << (width - 1))) for raw in words)


def assert_basis(program, args, outs, width, fraction_bits, coefficient, raw, initial, inverse):
    expected = independent_reference(width, fraction_bits, coefficient, raw, initial)
    actual, clean, preserved, state = basis_run(program, args, outs, [raw], [initial], inverse)
    assert (actual, clean, preserved) == ([expected], True, True)
    assert all(state[wire] == 0 for wire in range(2 * width, program.qubits))
    assert all(int(state[wire]) == ((raw >> bit) & 1) for bit, wire in enumerate(args[0]))
    return actual, clean, preserved


@lru_cache(maxsize=None)
def historical_observation(width, fraction_bits, coefficient, raw, initial):
    program, args, outs = historical_leaf(width, fraction_bits, coefficient)
    return assert_basis(program, args, outs, width, fraction_bits, coefficient, raw, initial, False)


@pytest.mark.parametrize("width,fraction_bits", NATIVE_FIXTURES)
@pytest.mark.parametrize("coefficient", COEFFICIENTS)
@pytest.mark.parametrize("strategy", STRATEGIES)
def test_native24_40_72_extrema_tiny_negative_fraction_edges_randoms_archived_equivalence(
    width, fraction_bits, coefficient, strategy
):
    program, args, outs = candidate(width, fraction_bits, coefficient, strategy)
    vectors = production_vectors(width, fraction_bits)
    assert any(raw & ((1 << fraction_bits) - 1) for raw, _ in vectors)
    assert any(raw >> (width - 1) for raw, _ in vectors)
    for raw, dirty in vectors:
        for initial in (0, dirty):
            historical = historical_observation(width, fraction_bits, coefficient, raw, initial)
            for inverse in (False, True):
                assert (
                    assert_basis(
                        program,
                        args,
                        outs,
                        width,
                        fraction_bits,
                        coefficient,
                        raw,
                        initial,
                        inverse,
                    )
                    == historical
                )
            final = independent_reference(width, fraction_bits, coefficient, raw, initial)
            restored, clean, preserved, _ = basis_run(program, args, outs, [raw], [final])
            assert restored == [initial] and clean and preserved


@pytest.mark.parametrize("strategy", PREFIX_STRATEGIES)
@pytest.mark.parametrize(
    "width,fraction_bits,coefficient",
    (
        (1, 0, -1),
        (5, 5, -17),
        (24, 12, 1067016148260),
        (40, 23, 60222732077),
        (72, 40, 22906492245),
    ),
)
def test_full_native_interface_separate_final_rows_literal_compute_copy_inverse(
    width, fraction_bits, coefficient, strategy
):
    program, args, outs = candidate(width, fraction_bits, coefficient, strategy)
    assert args == [tuple(range(width))]
    assert outs == [tuple(range(width, 2 * width))]
    inputs, outputs = set(args[0]), set(outs[0])
    assert all(gate[-1] not in inputs for gate in program.gates)
    assert all(not set(gate[:-1]) & outputs for gate in program.gates)
    assert (len(program.gates) - width) % 2 == 0
    boundary = (len(program.gates) - width) // 2
    forward = program.gates[:boundary]
    middle = program.gates[boundary : boundary + width]
    assert program.gates[boundary + width :] == list(reversed(forward))
    assert all(not set(gate) & outputs for gate in forward)
    product_base = middle[0][0] - fraction_bits
    assert middle == [(product_base + fraction_bits + bit, width + bit) for bit in range(width)]
    n = width + fraction_bits
    left = set(range(product_base - 2 * n, product_base - n))
    right = set(range(product_base - n, product_base))
    product = set(range(product_base, product_base + n))
    assert len(left | right | product) == 3 * n
    assert not ((left | right | product) & (inputs | outputs))


@pytest.mark.parametrize("strategy", PREFIX_STRATEGIES)
def test_zero_coefficient_retains_native_registers_and_arbitrary_output_without_gates(strategy):
    program, args, outs = candidate(72, 40, 0, strategy)
    assert program.qubits == 144 and len(program.gates) == 0
    assert args == [tuple(range(72))] and outs == [tuple(range(72, 144))]
    dirty = int("a5" * 9, 16)
    for raw in (0, 1, (1 << 72) - 1, 1 << 71):
        for inverse in (False, True):
            assert basis_run(program, args, outs, [raw], [dirty], inverse)[:3] == (
                [dirty],
                True,
                True,
            )


@pytest.mark.parametrize(
    "parameters",
    (
        (0, 0, 1, PREFIX_STRATEGIES[0]),
        (-1, 0, 1, PREFIX_STRATEGIES[0]),
        (72, -1, 1, PREFIX_STRATEGIES[0]),
        (72, 73, 1, PREFIX_STRATEGIES[0]),
        (True, 0, 1, PREFIX_STRATEGIES[0]),
        (72, True, 1, PREFIX_STRATEGIES[0]),
        (72, 40, True, PREFIX_STRATEGIES[0]),
        (72.0, 40, 1, PREFIX_STRATEGIES[0]),
        (72, 40.0, 1, PREFIX_STRATEGIES[0]),
        (72, 40, 1.0, PREFIX_STRATEGIES[0]),
        (72, 40, None, PREFIX_STRATEGIES[0]),
        (72, 40, 1, "unknown"),
        (72, 40, 1, "binary-carry-save"),
        (72, 40, 1, "kogge-stone"),
        (72, 40, 1, None),
        (72, 40, 1, True),
    ),
)
def test_invalid_native_fractional_coefficient_and_strategy_parameters(parameters):
    for function in (build_prefix_constant_multiplier, leaf_spec, signed_constant_partial_terms):
        with pytest.raises(ValueError):
            function(*parameters)


def test_canonical_full_domain_spec_and_exact_coefficient_expansions():
    keys = set()
    for coefficient in COEFFICIENTS:
        for strategy in PREFIX_STRATEGIES:
            spec = leaf_spec(72, 40, coefficient, strategy)
            assert spec["lowering"] == LOWERING and spec["algorithm"] == ALGORITHM
            assert spec["variant"] == VARIANT == "brent-kung"
            assert spec["params"] == {"c": coefficient} and spec["strategy"] == strategy
            assert spec["zero_bits"] == 0 and spec["product_width"] == 112
            assert spec["input_contract"] == {"zero_low_bits": 0}
            assert not ({"active_bits", "active_operand_bits", "signed_upper_bits"} & spec.keys())
            canonical = json.dumps(spec, sort_keys=True, separators=(",", ":"))
            keys.add(hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:20])
    assert len(keys) == 6
    for coefficient in SMALL_COEFFICIENTS + COEFFICIENTS + (-257, 257):
        for form in ("binary", "signed-digit"):
            assert (
                sum(sign * (1 << position) for position, sign in signed_digits(coefficient, form))
                == coefficient
            )
