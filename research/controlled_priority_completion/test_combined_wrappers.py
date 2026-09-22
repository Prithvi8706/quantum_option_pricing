"""Composition checks: changed offsets, signed angle and actual source binding."""

from collections import Counter
import copy
from fractions import Fraction
import importlib
import json
from pathlib import Path

import mpmath as mp
import pytest

from research.controlled_priority_completion.combined_wrappers import (
    audit_wrapper,
    decode_bounded,
    exact_mpf,
    sha256,
)
from research.controlled_priority_completion.estimator_hadamard import controller


ROOT = Path("results/controlled_priority_completion")


@pytest.mark.parametrize("model", ["C4", "H8"])
def test_composed_hadamard_source_offsets_and_signed_phase(model):
    wrapper = json.loads((ROOT / ("combined_" + model + "_hadamard_wrapper.json")).read_text())
    calls = [op for op in wrapper["operations"] if op["gate"] == "call_wave_half"]
    financial, phase = (json.loads(Path(op["manifest"]).read_text()) for op in calls[:2])
    financial_schedule = json.loads(Path(calls[0]["wave_schedule"]).read_text())
    base = financial_schedule["resources"]["logical_qubits"]
    assert [op["base"] for op in calls] == [0, base, base, 0]
    assert [op["inverse"] for op in calls] == [False, False, True, True]
    value_start = financial["outputs"]["Y_6"] * 72
    phase_inputs = {node["params"]["name"]: node["out"][0] * 96 for node in phase["inputs"]}
    destination = base + phase_inputs["Y"] + 24
    copies = [op for op in wrapper["operations"] if op["gate"] == "cx"]
    assert copies[:72] == [
        dict(gate="cx", wires=[value_start + j, destination + j]) for j in range(72)
    ]
    assert copies[72:] == list(reversed(copies[:72]))
    phases = [op for op in wrapper["operations"] if op["gate"] == "cp"]
    assert len(phases) == 67
    for j, op in enumerate(phases):
        exact = Fraction(-1 if j == 66 else 1) * Fraction(2) ** (j - 64)
        assert Fraction(*op["angle_radians"]) == exact
        assert op["wires"] == ["control", base + phase["outputs"]["angle"] * 96 + j]
    assert len(wrapper["random_wires"]) == financial["resources"]["random_hadamards"]
    assert audit_wrapper(wrapper)["hierarchical_calls"] == 4


def test_all_estimator_bindings_and_actual_rotation_costs():
    payload = json.loads((ROOT / "combined_estimators.json").read_text())
    assert sha256(Path(payload["cost_artifact"])) == payload["cost_artifact_sha256"]
    library_path = Path(payload["synthesis_library"])
    assert sha256(library_path) == payload["synthesis_library_sha256"]
    rotations = json.loads(library_path.read_text())["rotations"]
    costs = json.loads(Path(payload["cost_artifact"]).read_text())["rows"]
    assert len(payload["rows"]) == 6
    for row in payload["rows"]:
        assert sha256(Path(row["wrapper"])) == row["wrapper_sha256"]
        assert sha256(Path(row["allocation_source"])) == row["allocation_source_sha256"]
        matching = next(
            c
            for c in costs
            if (c["model"], c["method"], c["mode"]) == (row["model"], row["method"], row["mode"])
        )
        total = sum(
            count * rotations[key]["matrix_product_gates"].count("T")
            for key, count in row["synthesis_usage"].items()
        )
        assert matching["arithmetic_T_count"] + total == row["complete_logical_T_count"]
        assert max(row["control_wires"]) < row["allocated_logical_qubits_upper"]
        if row["method"] == "hadamard":
            reference = row["classical_controller"]["implementation"]
            module, function = reference.rsplit(".", 1)
            assert callable(getattr(importlib.import_module(module), function))
        else:
            allocation = row["allocation"]
            control = row["classical_controller"]
            assert (
                sum(p["repetitions_of_wrapper"] for p in control["powers"]) == allocation["M"] - 1
            )
            counts = Counter(op["gate"] for op in control["IQFT_operations"])
            assert counts["h"] == allocation["qpe_bits"]
            assert counts["swap"] == allocation["qpe_bits"] // 2
            assert counts["cp"] == allocation["qpe_bits"] * (allocation["qpe_bits"] - 1) // 2


def test_wrapper_audit_rejects_stale_source_hash_and_wire_alias():
    wrapper = json.loads((ROOT / "combined_C4_hadamard_wrapper.json").read_text())
    changed = copy.deepcopy(wrapper)
    next(op for op in changed["operations"] if op["gate"] == "call_wave_half")[
        "source_manifest_sha256"
    ] = "bad"
    with pytest.raises(AssertionError):
        audit_wrapper(changed)
    changed = copy.deepcopy(wrapper)
    next(op for op in changed["operations"] if op["gate"] == "cp")["wires"] = ["control", "control"]
    with pytest.raises(AssertionError):
        audit_wrapper(changed)


def test_bounded_decoder_endpoints_and_uneven_medians():
    allocation = json.loads((ROOT / "estimator_bounded.json").read_text())[0]["allocation"]
    M = allocation["M"]
    cases = ([0] * 15, [M // 2] * 15, [M - 1] * 15, [0] * 8 + [M // 2] * 7, [0] * 7 + [M // 2] * 8)
    mp.mp.dps = 120
    for values in cases:
        result = decode_bounded(values, allocation)
        reference = sorted(256 * mp.sin(mp.pi * k / M) ** 2 - 128 for k in values)[7]
        exact_reference = exact_mpf(reference._mpf_)
        lo, hi = (Fraction(*bound) for bound in result["decoded_median_interval_exact"])
        assert lo <= exact_reference <= hi
        assert abs(Fraction(result["estimate"]) - exact_reference) <= Fraction(
            result["rounding_error_bound"]
        )
        assert result["rounding_error_bound"] <= 1e-10
        assert result["ideal_plus_rounding_error_bound"] <= allocation["error"]
    with pytest.raises(ValueError):
        decode_bounded([M] * 15, allocation)
    with pytest.raises(ValueError):
        decode_bounded([0] * 14, allocation)


def test_hadamard_binary64_center_rounding_is_inside_each_saved_error():
    records = json.loads((ROOT / "estimator_hadamard.json").read_text())
    for record in records:
        allocation = record["allocation"]
        for plus in (True, False):
            result = controller(allocation, lambda stage, raw: [plus] * stage["repetitions"])
            final_left = Fraction(*result["history"][-1]["left_exact"])
            final_width = Fraction(*allocation["stages"][-1]["width_exact"]) * Fraction(
                *allocation["contraction_exact"]
            )
            center = final_left + final_width / 2
            rounding = abs(Fraction(result["estimate"]) - center)
            assert rounding <= Fraction(result["rounding_error_bound"])
            assert final_width / 2 + rounding <= Fraction(result["radius"])
            assert result["radius"] <= allocation["error"]
