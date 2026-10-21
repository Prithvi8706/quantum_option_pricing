"""Exact selector permutations and complete controlled toy Grover unitaries."""

from fractions import Fraction
import hashlib
from itertools import product
import json

import numpy as np
import pytest

from research.limitation_program_20261001 import native_payoff_estimator as estimator
from research.controlled_priority_completion.estimator_bounded import shifted_selector
from research.journal_sprint.reversible_fixed_point import Program, basis, read
from research.limitation_program_20261001.native_payoff_estimator import (
    bind_source_estimator,
    emit_toy_iterates,
    extended_resources,
    make_reflection,
    make_selector,
    make_toy_iterate,
)


def _inverse(program):
    inverse = Program(compact=True)
    inverse.qubits = program.qubits
    inverse.gates.extend(reversed(list(program.gates)))
    return inverse


def _assert_selector(program, registers, flag, value, uniform, dirty):
    initial = basis(registers[0], value) | basis(registers[1], uniform) | (dirty << flag)
    actual = program.run(initial)
    occupied = set(registers[0] + registers[1] + (flag,))
    assert read(actual, registers[0]) == value
    assert read(actual, registers[1]) == uniform
    assert not any((actual >> wire) & 1 for wire in range(program.qubits) if wire not in occupied)
    assert _inverse(program).run(actual) == initial
    return ((actual >> flag) & 1) ^ dirty


@pytest.mark.parametrize("width,bits", [(2, 1), (4, 2), (5, 3)])
def test_positive_selector_every_word_dirty_flag_and_exact_law(width, bits):
    program, registers, (flag,) = make_selector(width, bits)
    for value in range(1 << bits):
        marked = 0
        for uniform, dirty in product(range(1 << bits), range(2)):
            flag_value = _assert_selector(program, registers, flag, value, uniform, dirty)
            assert flag_value == int(uniform < value)
            if not dirty:
                marked += flag_value
        assert Fraction(marked, 1 << bits) == Fraction(value, 1 << bits)


def test_original_native72_selector_boundaries_full_word_preserved():
    program, registers, (flag,) = make_selector()
    # Both independently proved financial maxima and rare/zero selector endpoints.
    for value in (0, 1, 42680645928225, 42680645956484, (1 << 46) - 1):
        uniforms = {0, value, (1 << 46) - 1}
        if value:
            uniforms.add(value - 1)
        if value + 1 < 1 << 46:
            uniforms.add(value + 1)
        for uniform, dirty in product(sorted(uniforms), range(2)):
            assert _assert_selector(program, registers, flag, value, uniform, dirty) == int(
                uniform < value
            )


def test_shifted_negative_two_point_law_uses_offset_once():
    program, registers, (flag,) = shifted_selector(4, 0, 2)
    total = 0
    for signed_value in (-1, 1):
        marked = sum(
            _assert_selector(program, registers, flag, signed_value % 16, uniform, 0)
            for uniform in range(4)
        )
        assert Fraction(marked, 4) == Fraction(signed_value + 2, 4)
        total += marked
    assert Fraction(total, 8) == Fraction(1, 2)
    assert 4 * Fraction(total, 8) - 2 == 0


@pytest.mark.parametrize("width,bits", [(0, 1), (2, 0), (2, 3), (True, 1), (2, True), (2.0, 1)])
def test_reject_unproved_selector_dimensions(width, bits):
    with pytest.raises(ValueError, match="full native payoff word"):
        make_selector(width, bits)


def _apply(gates, vector):
    """Independent sparse statevector evaluator of each actual logical primitive."""
    vector = dict(vector)
    root_two = np.sqrt(2)
    for kind, a, b, c in gates:
        kind, a, b, c = map(int, (kind, a, b, c))
        updated = {}

        def accumulate(index, amplitude):
            updated[index] = updated.get(index, 0) + amplitude

        for index, amplitude in vector.items():
            if kind in (1, 2, 3):
                controls = () if kind == 1 else (a,) if kind == 2 else (a, b)
                target = a if kind == 1 else b if kind == 2 else c
                if all((index >> wire) & 1 for wire in controls):
                    index ^= 1 << target
                accumulate(index, amplitude)
            elif kind == 4:
                bit = (index >> a) & 1
                zero = index & ~(1 << a)
                accumulate(zero, amplitude / root_two)
                accumulate(zero | (1 << a), (-1 if bit else 1) * amplitude / root_two)
            elif kind == 5:
                accumulate(index, (-1 if (index >> a) & (index >> b) & 1 else 1) * amplitude)
            elif kind == 6:
                accumulate(index, (-1 if (index >> a) & 1 else 1) * amplitude)
            else:
                raise AssertionError("Unknown actual primitive")
        vector = {
            index: amplitude for index, amplitude in updated.items() if abs(amplitude) > 1e-13
        }
    return vector


def _embed(raw, wires):
    return sum(((raw >> bit) & 1) << wire for bit, wire in enumerate(wires))


def _active_unitary(gates, spec):
    active = spec["random_wires"] + [spec["control_wire"]]
    dimension = 1 << len(active)
    matrix = np.zeros((dimension, dimension), dtype=np.complex128)
    for raw in range(dimension):
        result = _apply(gates, {_embed(raw, active): 1})
        for index, amplitude in result.items():
            assert not any((index >> wire) & 1 for wire in spec["workspace_wires"])
            projected = sum(((index >> wire) & 1) << bit for bit, wire in enumerate(active))
            matrix[projected, raw] = amplitude
    return matrix


def _expected_unitary(spec):
    dimension = 1 << len(spec["random_wires"])
    reflection = 2 * np.ones((dimension, dimension)) / dimension - np.eye(dimension)
    marking = np.diag([(-1) ** flag for flag in spec["marking_for_each_random_word"]])
    zero = np.zeros((dimension, dimension))
    return np.block([[np.eye(dimension), zero], [zero, reflection @ marking]])


@pytest.mark.parametrize(
    "kind,probability",
    [
        ("positive-two-point", Fraction(1, 4)),
        ("positive-rare-event", Fraction(1, 8)),
        ("shifted-negative-two-point", Fraction(1, 2)),
    ],
)
def test_complete_actual_toy_iterate_controlled_unitary_and_helpers(kind, probability):
    gates, spec = make_toy_iterate(kind)
    actual = _active_unitary(gates, spec)
    expected = _expected_unitary(spec)
    assert np.allclose(actual, expected, atol=1e-12, rtol=0)
    assert np.allclose(actual.conj().T @ actual, np.eye(len(actual)), atol=1e-12, rtol=0)
    assert Fraction(spec["probability_numerator"], spec["probability_denominator"]) == probability


@pytest.mark.parametrize("kind", ["positive-two-point", "positive-rare-event"])
def test_actual_superposed_control_preserves_branch_relative_sign(kind):
    gates, spec = make_toy_iterate(kind)
    active = spec["random_wires"] + [spec["control_wire"]]
    dimension = 1 << len(spec["random_wires"])
    state = np.asarray([complex(j + 1, 2 - j) for j in range(dimension)])
    state /= np.linalg.norm(state)
    control_zero, control_one = 1 / np.sqrt(6), complex(1, 2) / np.sqrt(6)
    vector = np.concatenate((control_zero * state, control_one * state))
    embedded = {_embed(raw, active): amplitude for raw, amplitude in enumerate(vector)}
    actual = _apply(gates, embedded)
    expected = _expected_unitary(spec) @ vector
    for raw, amplitude in enumerate(expected):
        assert abs(actual.get(_embed(raw, active), 0) - amplitude) < 1e-12
    assert not any(any((index >> wire) & 1 for wire in spec["workspace_wires"]) for index in actual)


def test_final_control_z_is_required_for_correct_relative_phase():
    gates, spec = make_toy_iterate("positive-two-point")
    assert tuple(gates[-1]) == (6, spec["control_wire"], 0, 0)
    actual = _active_unitary(gates[:-1], spec)
    expected = _expected_unitary(spec)
    dimension = len(actual) // 2
    assert np.allclose(actual[:dimension, :dimension], np.eye(dimension), atol=1e-12)
    assert np.allclose(
        actual[dimension:, dimension:], -expected[dimension:, dimension:], atol=1e-12
    )
    assert not np.allclose(actual, expected, atol=1e-12)


@pytest.mark.parametrize("bits", [2, 3, 5, 9])
def test_reflection_exact_native_gate_counts_and_seven_t_cost(bits):
    gates, spec = make_reflection(bits)
    costs = extended_resources(gates, spec["qubits"])
    assert costs["x"] == costs["h"] == 2 * bits
    assert costs["ccx"] == 2 * (bits - 1)
    assert costs["cz"] == costs["z"] == 1
    assert costs["t_count"] == 14 * (bits - 1)
    assert costs["clifford_h"] == 2 * bits + 4 * (bits - 1)
    assert costs["clifford_cx"] == 12 * (bits - 1)
    assert costs["source_gates"] == len(gates)


@pytest.mark.parametrize("bits", [0, 1, True, 2.0])
def test_reflection_requires_two_actual_random_wires(bits):
    with pytest.raises(ValueError, match="two random wires"):
        make_reflection(bits)


@pytest.mark.parametrize("row", [(7, 0, 0, 0), (3, 0, 0, 1), (5, 0, 0, 0), (4, 3, 0, 0)])
def test_extended_resource_reader_rejects_gate_forgery(row):
    with pytest.raises(ValueError):
        extended_resources(np.asarray([row], dtype=np.int32), 3)


def test_toy_saved_arrays_reproduce_complete_controlled_unitaries(tmp_path):
    directory = tmp_path / "toys"
    specs = emit_toy_iterates(directory)
    assert json.loads((directory / "toys.json").read_text(encoding="utf-8")) == specs
    assert len(specs) == 3
    for spec in specs:
        gates = np.load(spec["gate_file"])
        assert np.allclose(
            _active_unitary(gates, spec), _expected_unitary(spec), atol=1e-12, rtol=0
        )


def test_native_binding_rejects_a_different_financial_case_before_loading(tmp_path):
    with pytest.raises(ValueError, match="accepted B4/B8"):
        bind_source_estimator(tmp_path / "C4" / "min-depth", tmp_path / "cert.json", tmp_path)


def test_native_binding_rejects_an_unaccepted_arithmetic_receipt_before_loading(tmp_path):
    with pytest.raises(ValueError, match="source identity"):
        bind_source_estimator(tmp_path / "B4x12" / "min-depth", tmp_path / "cert.json", tmp_path)


def test_unknown_toy_is_rejected():
    with pytest.raises(ValueError, match="Unknown frozen"):
        make_toy_iterate("new-unfrozen-candidate")


@pytest.mark.parametrize("legacy", [False, True])
def test_receipt_schemas_resolve_legacy_paths_and_protocol_inputs(tmp_path, monkeypatch, legacy):
    monkeypatch.setattr(estimator, "ROOT", tmp_path)
    receipt = tmp_path / "receipt"
    payload = receipt / "nested" / "payload.txt"
    payload.parent.mkdir(parents=True)
    payload.write_text("unchanged native source", encoding="utf-8")
    frozen = tmp_path / "input.txt"
    frozen.write_text("original proof", encoding="utf-8")

    def sha(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    inputs = {"input.txt": sha(frozen)}
    protocol = receipt / "protocol.json"
    protocol.write_text(json.dumps({"frozen_inputs": inputs}), encoding="utf-8")
    if legacy:
        manifest = {"nested\\payload.txt": sha(payload), "protocol.json": sha(protocol)}
    else:
        manifest = {
            "files": {
                "receipt/nested/payload.txt": sha(payload),
                "receipt/protocol.json": sha(protocol),
            },
            "frozen_inputs": inputs,
        }
    (receipt / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    assert estimator._verify_receipt(receipt) == manifest
    frozen.write_text("changed proof", encoding="utf-8")
    with pytest.raises(ValueError, match="receipt changed"):
        estimator._verify_receipt(receipt)


@pytest.mark.parametrize(
    "manifest",
    [
        {},
        {"files": {}},
        {"unknown": {"nested": "value"}},
        {"files": [], "frozen_inputs": {}},
        {"payload.txt": "not-a-sha256"},
    ],
)
def test_unknown_receipt_schema_is_rejected(tmp_path, manifest):
    (tmp_path / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ValueError, match="Unknown"):
        estimator._verify_receipt(tmp_path)


def test_legacy_receipt_cannot_escape_its_directory(tmp_path):
    receipt = tmp_path / "receipt"
    receipt.mkdir()
    outside = tmp_path / "outside.txt"
    outside.write_text("outside", encoding="utf-8")
    manifest = {"../outside.txt": hashlib.sha256(outside.read_bytes()).hexdigest()}
    (receipt / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ValueError, match="escapes"):
        estimator._verify_receipt(receipt)
