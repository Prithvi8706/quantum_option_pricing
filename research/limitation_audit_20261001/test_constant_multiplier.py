"""Independent integer specification, signed edges, promises and cache isolation."""

import hashlib
import random

import pytest

from research.controlled_source_completion.constant_multiplier import (
    STRATEGIES, build_constant_multiplier, has_zero_low_proof, signed_digits,
)
from research.controlled_source_completion.primitives import basis_run, build
from research.controlled_source_completion.compiler import compile_graph, execute
from research.controlled_source_completion.ir import Graph, evaluate
from research.limitation_audit_20261001.experiment_constant_multiplier import ConstantLibrary


def check_case(p, args, outs, width, fraction, coefficient, value, initial, inverse=False):
    mask = (1 << width) - 1
    signed = value - (1 << width) if value & (1 << (width - 1)) else value
    expected = initial ^ ((signed * coefficient >> fraction) & mask)
    actual, clean, preserved, _ = basis_run(p, args, outs, [value], [initial], inverse)
    assert (actual, clean, preserved) == ([expected], True, True)


@pytest.mark.parametrize("strategy", STRATEGIES)
def test_exhaustive_signed_small_words(strategy):
    for width in (1, 2, 3, 4):
        for fraction in range(width + 1):
            for zero_bits in sorted({0, min(fraction, width - 1)}):
                for coefficient in (-7, -3, -1, 0, 1, 3, 7):
                    p, args, outs = build_constant_multiplier(
                        width, fraction, coefficient, zero_bits, strategy,
                    )
                    for upper in range(1 << (width - zero_bits)):
                        value = upper << zero_bits
                        check_case(p, args, outs, width, fraction, coefficient,
                                   value, upper ^ ((1 << width) - 1), bool(upper % 2))


@pytest.mark.parametrize("strategy", STRATEGIES)
def test_real_coefficient_edges_random_inverse_and_historical_leaf(strategy):
    width, fraction, coefficient = 72, 40, 762123384786
    p, args, outs = build_constant_multiplier(width, fraction, coefficient, fraction, strategy)
    old, old_args, old_outs = build("cmul", width, fraction, {"c": coefficient})
    rng = random.Random(20261005)
    uppers = [0, 1, 2**31 - 1, 2**31, 2**31 + 1, 2**32 - 2, 2**32 - 1]
    uppers += [rng.getrandbits(32) for _ in range(40)]
    for index, upper in enumerate(uppers):
        value, initial = upper << fraction, rng.getrandbits(width)
        check_case(p, args, outs, width, fraction, coefficient, value, initial, bool(index % 2))
        current = basis_run(p, args, outs, [value], [initial], bool(index % 2))[:3]
        historical = basis_run(old, old_args, old_outs, [value], [initial])[:3]
        assert current == historical
    outputs = set(outs[0])
    assert all(not (set(gate[:-1]) & outputs) for gate in p.gates)
    assert all(not (set(gate) & set(args[0][:fraction])) for gate in p.gates)


def test_signed_digit_identity_and_input_contract_negative_controls():
    for coefficient in range(-128, 129):
        for form in ("binary", "signed-digit"):
            digits = signed_digits(coefficient, form)
            assert sum(digit * (1 << position) for position, digit in digits) == coefficient
            if form == "signed-digit":
                assert all(b[0] - a[0] > 1 for a, b in zip(digits, digits[1:]))
    coefficient = 762123384786
    assert len(signed_digits(coefficient, "binary")) == 23
    assert len(signed_digits(coefficient)) == 13
    p, args, outs = build_constant_multiplier(72, 40, coefficient, 40)
    actual = basis_run(p, args, outs, [2], [0])[0][0]
    assert actual == 0 and (2 * coefficient >> 40) == 1
    # A coefficient match by itself is never a valid zero-low input proof.
    cmul = dict(op="cmul", args=[1], params={"c": coefficient})
    assert not has_zero_low_proof(cmul, {1: dict(op="input", params={})}, 40)
    assert not has_zero_low_proof(cmul, {1: dict(op="bits", params={"shift": -39})}, 40)
    assert not has_zero_low_proof(cmul, {1: dict(op="bits", params={"shift": 40})}, 40)
    assert has_zero_low_proof(cmul, {1: dict(op="bits", params={"shift": -40})}, 40)
    # Unsigned upper-word multiplication would be wrong by c*2**32 for -1.
    check_case(p, args, outs, 72, 40, coefficient, (2**32 - 1) << 40, 0)
    assert (2**32 - 1) * coefficient != -coefficient


@pytest.mark.parametrize("params", [(0, 0, 1, 0), (3, 4, 1, 0),
                                     (3, 1, 1, 2), (3, 1, 1, 3),
                                     (3, 1, 1, True)])
def test_invalid_contract_parameters_rejected(params):
    with pytest.raises(ValueError):
        build_constant_multiplier(*params)


def test_library_guard_cache_and_complete_graph(tmp_path):
    graph = Graph(2, 4)
    x = graph.input("x", graph.w)
    shifted = graph.bits(x, -graph.f, graph.w)
    raw = graph.node("cmul", (x,), {"c": 3})
    specialized = graph.node("cmul", (shifted,), {"c": 3})
    graph.outputs = {"raw": raw, "specialized": specialized}
    target = graph.as_dict()
    original, _ = compile_graph(target, tmp_path / "original")
    library = ConstantLibrary(tmp_path / "new_leaves", target, original,
                              "signed-digit-carry-save", coefficient=3)
    source, _ = compile_graph(target, tmp_path / "specialized", library)
    old_cmul = [c for c in original["forward_calls"] if c["out"] == [raw]][0]["leaf"]
    raw_cmul = [c for c in source["forward_calls"] if c["out"] == [raw]][0]["leaf"]
    new_cmul = [c for c in source["forward_calls"] if c["out"] == [specialized]][0]["leaf"]
    assert raw_cmul == old_cmul and new_cmul != raw_cmul
    assert len(library.proofs) == 1
    entry = library.entries[new_cmul]
    assert entry["input_contract"] == {"zero_low_bits": 2}
    assert entry["sha256"] == hashlib.sha256(
        (library.path / entry["gate_file"]).read_bytes(),
    ).hexdigest()
    initial = {"raw": 37, "specialized": 21}
    for value in range(1 << graph.w):
        _, values = evaluate(target, {"x": value}, True)
        actual = execute(source, {"x": value}, initial)
        assert actual["values"] == {name: values[v] ^ initial[name]
                                    for name, v in graph.outputs.items()}
        assert actual["workspace_clean"] and actual["inputs_preserved"]
    # Reload the exact cache and ensure another strategy uses a separate key.
    cached = ConstantLibrary(library.path, target, original,
                             "signed-digit-carry-save", coefficient=3)
    node = next(n for n in target["nodes"] if n["out"] == [specialized])
    assert cached.get(node)[0] == new_cmul
    other = ConstantLibrary(library.path, target, original,
                            "binary-carry-save", coefficient=3)
    assert other.get(node)[0] != new_cmul


def test_corrupted_specialized_gate_cache_rejected(tmp_path):
    graph = Graph(2, 4)
    x = graph.input("x", graph.w)
    shifted = graph.bits(x, -graph.f, graph.w)
    value = graph.node("cmul", (shifted,), {"c": 3})
    graph.outputs = {"v": value}
    target = graph.as_dict()
    original, _ = compile_graph(target, tmp_path / "original")
    library = ConstantLibrary(tmp_path / "leaves", target, original,
                              "signed-digit-carry-save", coefficient=3)
    node = next(n for n in target["nodes"] if n["out"] == [value])
    _, entry = library.get(node)
    binary = library.path / entry["gate_file"]
    binary.write_bytes(binary.read_bytes() + b"deliberate corruption")
    cached = ConstantLibrary(library.path, target, original,
                             "signed-digit-carry-save", coefficient=3)
    with pytest.raises(ValueError, match="cache"):
        cached.get(node)
