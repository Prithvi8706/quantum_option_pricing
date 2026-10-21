"""Exhaustive promised-domain tests and a local signed7 leaf experiment."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import random
import sys
import time
from functools import lru_cache
from pathlib import Path

import numpy as np
import pytest

import research.controlled_source_completion.log_constant_multiplier as implementation
from research.controlled_source_completion.constant_multiplier import (
    STRATEGIES,
    build_constant_multiplier,
)
from research.controlled_source_completion.log_constant_multiplier import (
    COEFFICIENT,
    EMBEDDINGS,
    build_log_constant_multiplier,
    contract_holds,
    input_contract,
    leaf_spec,
    site_proof,
)
from research.controlled_source_completion.primitives import (
    array_gates,
    basis_run,
    build,
    resources,
)
from research.limitation_program_20261001.prove_log_exponent import (
    EXPECTED,
    SSAContext,
    fixture,
)

ROOT = Path(__file__).resolve().parents[2]
MASK = (1 << 72) - 1


@lru_cache
def old_general():
    return build("cmul", 72, 40, {"c": COEFFICIENT})


@pytest.mark.parametrize("embedding", EMBEDDINGS)
@pytest.mark.parametrize("strategy", STRATEGIES)
def test_every_signed7_word_historical_equivalence_and_clean_inverse(strategy, embedding):
    candidate, args, outs = build_log_constant_multiplier(strategy, embedding)
    old, old_args, old_outs = old_general()
    rng = random.Random(20261012)
    for value in range(-64, 64):
        argument = (value << 40) & MASK
        assert contract_holds(argument)
        for initial in (0, rng.getrandbits(72)):
            expected = initial ^ ((value * COEFFICIENT) & MASK)
            for inverse in (False, True):
                actual, clean, preserved, _ = basis_run(
                    candidate, args, outs, [argument], [initial], inverse
                )
                assert (actual, clean, preserved) == ([expected], True, True)
            historical = basis_run(old, old_args, old_outs, [argument], [initial])[:3]
            assert historical == ([expected], True, True)
    output_wires = set(outs[0])
    ignored_input = set(args[0][:40] + args[0][47:])
    assert all(not (set(gate[:-1]) & output_wires) for gate in candidate.gates)
    assert all(not (set(gate) & ignored_input) for gate in candidate.gates)


@pytest.mark.parametrize("embedding", EMBEDDINGS)
def test_invalid_domain_is_detected_and_never_treated_as_a_general_leaf(embedding):
    candidate, args, outs = build_log_constant_multiplier(embedding=embedding)
    old, old_args, old_outs = old_general()
    invalid = [
        2,
        64 << 40,
        (-65 << 40) & MASK,
        ((-1 << 40) & MASK) ^ (1 << 71),
    ]
    for argument in invalid:
        assert not contract_holds(argument)
        actual = basis_run(candidate, args, outs, [argument], [0])[0][0]
        historical = basis_run(old, old_args, old_outs, [argument], [0])[0][0]
        assert actual != historical
    assert not contract_holds(True)
    assert not contract_holds(-1)
    assert not contract_holds(1 << 72)


def test_versioned_spec_and_full_source_site_guard():
    keys = set()
    for strategy in STRATEGIES:
        for embedding in EMBEDDINGS:
            spec = leaf_spec(strategy, embedding)
            assert spec["input_contract"] == {"zero_low_bits": 40, "signed_upper_bits": 7}
            assert spec["width"] == 72 and spec["fraction_bits"] == 40
            keys.add(hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest())
    assert len(keys) == 8 and input_contract()["signed_upper_bits"] == 7
    target = fixture()
    assert site_proof(target, 8) is not None
    coefficient_only = copy.deepcopy(target)
    coefficient_only["nodes"][8]["args"] = [0]
    assert site_proof(coefficient_only, 8) is None
    wrong_guard = copy.deepcopy(target)
    wrong_guard["nodes"][3]["args"] = [2, 0, 1]
    assert site_proof(wrong_guard, 8) is None
    for case, expected in EXPECTED.items():
        path = ROOT / "results/limitation_audit_20261001/constant_multiplier_v1"
        comparison = json.loads((path / case / "comparison.json").read_text())
        target = json.loads(
            (path / case / comparison["best"]["strategy"] / "target.json").read_text()
        )
        context = SSAContext(target)
        eligible, fallback = 0, 0
        for index, node in enumerate(context.target["nodes"]):
            if node["op"] == "cmul" and node["params"].get("c") == COEFFICIENT:
                if site_proof(context, index) is not None:
                    eligible += 1
                else:
                    fallback += 1
        assert (eligible, fallback) == (expected["log"], expected["exp"])


def test_fusion_rejects_a_noncanonical_child(monkeypatch):
    original = implementation.build_constant_multiplier

    def damaged(*args, **kwargs):
        child, arguments, outputs = original(*args, **kwargs)
        first = child.gates[0]
        child.gates[0:1] = [(outputs[0][0], first[-1])]
        return child, arguments, outputs

    monkeypatch.setattr(implementation, "build_constant_multiplier", damaged)
    with pytest.raises(ValueError, match="child"):
        build_log_constant_multiplier()


@pytest.mark.parametrize("strategy,embedding", [
    ("unknown", "fused-child-copy"),
    ("signed-digit-carry-save", "unknown"),
])
def test_invalid_strategy_or_embedding(strategy, embedding):
    with pytest.raises(ValueError):
        build_log_constant_multiplier(strategy, embedding)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def run(output):
    output = output.resolve()
    output.relative_to((ROOT / "results/limitation_program_20261001").resolve())
    output.mkdir(parents=True, exist_ok=False)
    producer = Path(__file__).resolve()
    module = ROOT / "research/controlled_source_completion/log_constant_multiplier.py"
    proof_root = ROOT / "results/limitation_program_20261001/A07_run001"
    protocol = {
        "task": "A10 exact signed7 ln2 leaf experiment",
        "family": "47-bit child with full72 output sign extension; safe twice and "
        "literal-structure-checked fused embedding",
        "input_contract": input_contract(),
        "same_graph_dispatch_proof": str(proof_root / "result.json"),
        "proof_result_sha256": digest(proof_root / "result.json"),
        "producer_sha256": digest(producer),
        "implementation_sha256": digest(module),
        "dependency_sha256": {
            str(path.relative_to(ROOT)): digest(path)
            for path in (
                ROOT / "research/controlled_source_completion/constant_multiplier.py",
                ROOT / "research/controlled_source_completion/primitives.py",
                ROOT / "research/journal_sprint/reversible_fixed_point.py",
                ROOT / "research/limitation_program_20261001/prove_log_exponent.py",
            )
        },
        "fixed_coefficient": COEFFICIENT,
        "width": 72,
        "fraction_bits": 40,
        "strategies": list(STRATEGIES),
        "embeddings": list(EMBEDDINGS),
        "acceptance": [
            "All128 signed7 inputs agree with the independent product and old72 general leaf.",
            "Arbitrary output XOR, input preservation, inverse and workspace cleanup hold.",
            "Output never controls computation; ignored sign/zero input wires are untouched.",
            "Invalid-domain negative controls differ and are not admitted by the same-SSA guard.",
            "Only log-derived calls are eligible; exponential calls retain their wider fallback.",
            "Measured complete clean-leaf resource frontier improves on current signed32 leaf.",
        ],
        "selection": "Lowest exact seven-T/all-to-all leaf T-depth, then T count and qubits",
        "stop_rule": "One child family, four arithmetic strategies, two wrappers. "
        "Reject a failed semantic/structure candidate; no full financial replay in this run.",
        "exclusions": "No library integration, financial full-source replay, changed "
        "precision/law, physical timing or advantage claim.",
    }
    save(output / "protocol.json", protocol)
    started = time.perf_counter()
    try:
        test_exit = pytest.main([str(producer), "-q"])
        if test_exit != 0:
            raise AssertionError("Leaf/domain tests failed")
        proof_result = json.loads((proof_root / "result.json").read_text())
        assert proof_result["passed"] and not proof_result["financial_function_changed"]
        baseline = {
            "old_general72": resources(old_general()[0]),
            "retained_signed32_carry_save": resources(build_constant_multiplier(
                72, 40, COEFFICIENT, 40, "signed-digit-carry-save"
            )[0]),
        }
        save(output / "baselines.json", baseline)
        candidates = []
        for strategy in STRATEGIES:
            for embedding in EMBEDDINGS:
                leaf, args, outs = build_log_constant_multiplier(strategy, embedding)
                spec = leaf_spec(strategy, embedding)
                key = hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest()[:20]
                binary = output / (key + ".npy")
                np.save(binary, array_gates(leaf))
                row = {
                    "key": key, "spec": spec, "resources": resources(leaf),
                    "args": list(map(list, args)), "outs": list(map(list, outs)),
                    "gate_file": binary.name, "sha256": digest(binary),
                    "input_contract": input_contract(),
                }
                save(output / (key + ".json"), row)
                candidates.append(row)
        best = min(candidates, key=lambda row: (
            row["resources"]["t_depth"], row["resources"]["t_count"],
            row["resources"]["qubits"],
        ))
        prior = baseline["retained_signed32_carry_save"]
        retained = all(
            best["resources"][name] < prior[name]
            for name in ("t_depth", "t_count", "qubits")
        )
        result = {
            "passed": True, "decision": "accepted leaf" if retained else "component frontier",
            "baseline": baseline, "best": best,
            "candidates": [{key: row[key] for key in ("key", "spec", "resources")}
                           for row in candidates],
            "dominates_retained_signed32_leaf": retained,
            "eligible_calls": proof_result["counts"],
            "complete_source_gain_measured": False,
            "financial_function_changed": False,
            "integrated": False,
            "seconds": time.perf_counter() - started,
        }
        save(output / "result.json", result)
        save(output / "verification.json", {
            "passed": True, "pytest_exit_code": int(test_exit), "pytest_tests": 14,
            "cases_per_candidate": 128,
            "wrappers": len(EMBEDDINGS), "strategies": len(STRATEGIES),
            "command": sys.argv, "python": sys.version, "executable": sys.executable,
            "producer_sha256": digest(producer), "implementation_sha256": digest(module),
            "protocol_saved_before_tests": True, "scope": protocol["exclusions"],
        })
        (output / "NEXT.md").write_text(
            "# Next local integration\n\n"
            "Use the measured best exact leaf only at same-SSA proven log sites. "
            "Keep exponential and unproved calls on the previous wider leaf. "
            "Version cache keys with width, fraction, coefficient, signed-upper "
            "promise, child width, wrapper, strategy and lowering. "
            "After review, compile the combined compact/capped full sources and "
            "replay them against the unchanged integer target. Do not insert this "
            "leaf-only factor into the full pricing ledger before that measurement.\n",
            encoding="utf-8",
        )
        save(output / "manifest.json", {
            "producer_sha256": digest(producer),
            "implementation_sha256": digest(module),
            "sha256": {path.name: digest(path) for path in output.iterdir()
                       if path.is_file() and path.name != "manifest.json"},
        })
        print(json.dumps({
            "decision": result["decision"], "best": best["resources"],
            "strategy": best["spec"]["strategy"], "embedding": best["spec"]["embedding"],
            "baseline": prior, "seconds": result["seconds"],
        }), flush=True)
    except Exception as error:
        save(output / "result.json", {
            "passed": False, "error_type": type(error).__name__, "error": str(error),
            "integrated": False, "financial_function_changed": False,
        })
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output)
