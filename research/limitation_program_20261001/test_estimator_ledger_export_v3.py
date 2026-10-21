"""Independent count fixtures and exact archived-contract regressions."""

import copy
from pathlib import Path

import pytest

from research.limitation_program_20261001 import estimator_ledger_export_v3 as exporter


ROOT = Path(__file__).resolve().parents[2]


def hadamard_fixture():
    return dict(
        stages=[
            dict(stage=0, T=2, repetitions=3, controlled_U_calls=6),
            dict(stage=1, T=5, repetitions=2, controlled_U_calls=10),
        ],
        controlled_U_calls=16,
        hadamard_test_executions=5,
        longest_single_chain=5,
    )


def qpe_fixture():
    controls = [100, 101, 102]
    # Written independently: bit reversal followed by the triangular IQFT.
    operations = [
        dict(gate="swap", wires=[100, 102]),
        dict(gate="h", wires=[100]),
        dict(gate="cp", wires=[100, 101], angle_pi=[-1, 2], exact_T_count=3),
        dict(gate="h", wires=[101]),
        dict(
            gate="cp",
            wires=[100, 102],
            angle_pi=[-1, 4],
            synthesis_key="pi_1_8",
            half_angle_sign=-1,
        ),
        dict(gate="cp", wires=[101, 102], angle_pi=[-1, 2], exact_T_count=3),
        dict(gate="h", wires=[102]),
    ]
    allocation = dict(qpe_bits=3, repetitions=3, M=8, controlled_grover_calls=21)
    controller = dict(
        powers=[
            dict(control=100, repetitions_of_wrapper=1),
            dict(control=101, repetitions_of_wrapper=2),
            dict(control=102, repetitions_of_wrapper=4),
        ],
        IQFT_operations=operations,
        repetitions=3,
    )
    return allocation, controller, controls


def reflection_fixture():
    # The external-control Z is essential; an uncontrolled global sign is not.
    return [
        dict(gate="h", wires=[0]),
        dict(gate="h", wires=[1]),
        dict(gate="h", wires=[2]),
        dict(gate="x", wires=[0]),
        dict(gate="x", wires=[1]),
        dict(gate="x", wires=[2]),
        dict(gate="ccx", wires=[0, 1, 10]),
        dict(gate="ccx", wires=[10, 2, 11]),
        dict(gate="cz", wires=[11, "control"]),
        dict(gate="ccx", wires=[10, 2, 11]),
        dict(gate="ccx", wires=[0, 1, 10]),
        dict(gate="x", wires=[0]),
        dict(gate="x", wires=[1]),
        dict(gate="x", wires=[2]),
        dict(gate="h", wires=[0]),
        dict(gate="h", wires=[1]),
        dict(gate="h", wires=[2]),
        dict(gate="z", wires=["control"]),
    ]


def test_hadamard_counts_and_chain_are_distinct():
    expansion = exporter.expand_hadamard(hadamard_fixture())
    assert expansion["controlled_wrapper_calls"] == 16
    assert expansion["fresh_preparations"] == 5
    assert expansion["longest_wrapper_chain"] == 5
    assert expansion["adaptive_stages"] == 2
    assert expansion["between_stage_feedback_dependencies"] == 1
    assert expansion["qpe_executions"] == 0


@pytest.mark.parametrize(
    "field",
    ["stage_calls", "controlled_U_calls", "hadamard_test_executions", "longest_single_chain"],
)
def test_hadamard_rejects_inconsistent_saved_totals(field):
    allocation = hadamard_fixture()
    if field == "stage_calls":
        allocation["stages"][0]["controlled_U_calls"] += 1
    else:
        allocation[field] += 1
    with pytest.raises(ValueError):
        exporter.expand_hadamard(allocation)


@pytest.mark.parametrize("bad", [0, -1, True, 1.5])
def test_hadamard_rejects_nonpositive_noninteger_work(bad):
    allocation = hadamard_fixture()
    allocation["stages"][0]["T"] = bad
    with pytest.raises(ValueError):
        exporter.expand_hadamard(allocation)


def test_qpe_counts_exact_rotations_and_complete_chain():
    allocation, controller, controls = qpe_fixture()
    result = exporter.expand_qpe(allocation, controller, controls)
    assert result["controlled_wrapper_calls"] == 3 * (1 + 2 + 4)
    assert result["longest_wrapper_chain"] == 7
    assert result["largest_controlled_power"] == 4
    assert result["fresh_preparations"] == 3
    assert result["measured_bits"] == 9
    assert result["iqft_gate_counts"] == dict(swap=3, h=9, cp=9)
    assert result["iqft_synthesis_usage"] == {"pi_1_8": 9}
    assert result["iqft_exact_T_count"] == 18
    assert result["iqft_exact_T_depth_serial"] == 12
    assert result["adaptive_stages"] == 0


@pytest.mark.parametrize(
    "mutation",
    [
        "M",
        "bits",
        "even_repetition",
        "power",
        "missing_swap",
        "angle",
        "exact_charge",
        "double_charge",
    ],
)
def test_qpe_rejects_missing_or_duplicate_charges(mutation):
    allocation, controller, controls = qpe_fixture()
    if mutation == "M":
        allocation["M"] += 1
    elif mutation == "bits":
        allocation["qpe_bits"] += 1
    elif mutation == "even_repetition":
        allocation["repetitions"] = 2
    elif mutation == "power":
        controller["powers"][2]["repetitions_of_wrapper"] = 3
    elif mutation == "missing_swap":
        controller["IQFT_operations"].pop(0)
    elif mutation == "angle":
        controller["IQFT_operations"][4]["angle_pi"] = [-1, 8]
    elif mutation == "exact_charge":
        controller["IQFT_operations"][2]["exact_T_count"] = 0
    else:
        controller["IQFT_operations"][4]["exact_T_count"] = 3
    with pytest.raises(ValueError):
        exporter.expand_qpe(allocation, controller, controls)


def test_signed_reflection_counts_and_literal_inverse():
    result = exporter.audit_reflection(reflection_fixture(), [0, 1, 2])
    assert {key: result[key] for key in ("ccx", "h", "x", "cz", "control_z")} == dict(
        ccx=4, h=6, x=6, cz=1, control_z=1
    )
    assert result["T_count"] == 28
    assert result["T_depth_serial_upper"] == 24


@pytest.mark.parametrize(
    "mutation",
    [
        "missing_sign",
        "wrong_sign",
        "inverse_order",
        "duplicate_random",
        "scratch_alias",
        "missing_H",
    ],
)
def test_reflection_rejects_controlled_sign_cleanup_or_alias_errors(mutation):
    operations, random_wires = reflection_fixture(), [0, 1, 2]
    if mutation == "missing_sign":
        operations.pop()
    elif mutation == "wrong_sign":
        operations[-1]["gate"] = "x"
    elif mutation == "inverse_order":
        operations[9], operations[10] = operations[10], operations[9]
    elif mutation == "duplicate_random":
        random_wires = [0, 1, 1]
    elif mutation == "scratch_alias":
        operations[6]["wires"][2] = 2
    else:
        operations.pop(0)
    with pytest.raises(ValueError):
        exporter.audit_reflection(operations, random_wires)


@pytest.mark.parametrize("sign", [-1, 1])
def test_controlled_phase_half_angle_and_sign(sign):
    operation = dict(angle_radians=[sign, 16], synthesis_key="radian_1_32", half_angle_sign=sign)
    assert exporter.phase_synthesis_key(operation, "radians") == "radian_1_32"


@pytest.mark.parametrize("mutation", ["key", "sign"])
def test_controlled_phase_rejects_incorrect_synthesis_binding(mutation):
    operation = dict(angle_radians=[1, 16], synthesis_key="radian_1_32", half_angle_sign=1)
    operation["synthesis_key" if mutation == "key" else "half_angle_sign"] = (
        "radian_1_16" if mutation == "key" else -1
    )
    with pytest.raises(ValueError):
        exporter.phase_synthesis_key(operation, "radians")


def test_nonlocal_dependency_is_rejected():
    with pytest.raises(ValueError, match="Nonlocal"):
        exporter.local_path(ROOT, ROOT.parent / "outside.json")


def test_actual_archive_three_counts_and_t_resource_totals():
    result = exporter.export_archive(ROOT)
    expected = [
        ("C4", "hadamard", 1203320, 1301, 5762, 699762085324240),
        ("H8", "hadamard", 2967610, 918, 23663, 6238068915404940),
        ("C4", "bounded_QAE", 7864305, 15, 524287, 4473763507420080),
    ]
    actual = [
        (
            r["model"],
            r["method"],
            r["schedule_expansion"]["controlled_wrapper_calls"],
            r["schedule_expansion"]["fresh_preparations"],
            r["schedule_expansion"]["longest_wrapper_chain"],
            r["resource_reconciliation"]["complete_logical_T_count"],
        )
        for r in result["rows"]
    ]
    assert actual == expected


def test_actual_archive_preserves_unknown_costs_and_financial_boundary():
    result = exporter.export_archive(ROOT)
    assert result["financial_pair"]["status"] == "pending"
    assert result["financial_pair"]["archived_counts_times_B4_depth_allowed"] is False
    assert result["new_financial_replays"] == result["new_quantum_unitary_tests"] == 0
    for row in result["rows"]:
        assert row["source_contract"]["full_price_contract"] is False
        assert row["source_contract"]["compatible_with_current_B4_source"] is False
        assert row["unknowns"]["readout_duration_seconds"] is None
        assert row["unknowns"]["reset_duration_seconds"] is None
        assert row["unknowns"]["classical_feedback_duration_seconds"] is None
        assert (
            row["invocation_counts"]["financial_graph_forward_calls"]
            == row["invocation_counts"]["financial_graph_inverse_calls"]
        )
    bounded = result["rows"][2]
    assert bounded["invocation_counts"]["adaptive_quantum_stages"] == 0
    assert bounded["archived_sequential_adaptive_stage_label"] == 1
    assert bounded["invocation_counts"]["required_clean_reset_bits_before_preparation"] == 15 * (
        1968 + 19
    )
    assert bounded["invocation_counts"]["iqft_gate_counts"] == dict(swap=135, h=285, cp=2565)


def test_actual_archive_rejects_wrapper_hash_corruption(monkeypatch):
    original_sha = exporter.sha256

    def counterfeit(path):
        if Path(path).name == "combined_C4_hadamard_wrapper.json":
            return "0" * 64
        return original_sha(path)

    monkeypatch.setattr(exporter, "sha256", counterfeit)
    with pytest.raises(ValueError, match="wrapper binding"):
        exporter.export_archive(ROOT)


def test_selector_inverse_cannot_be_removed_from_archive_audit(monkeypatch):
    original_read = exporter.read

    def missing_inverse(path):
        value = original_read(path)
        if Path(path).name == "combined_C4_bounded_wrapper.json":
            value = copy.deepcopy(value)
            # The very first selector-inverse gate immediately follows its CZ.
            marker = next(j for j, op in enumerate(value["operations"]) if op["gate"] == "cz")
            value["operations"].pop(marker + 1)
        return value

    monkeypatch.setattr(exporter, "read", missing_inverse)
    wrapper = exporter.read(
        ROOT / "results/controlled_priority_completion/combined_C4_bounded_wrapper.json"
    )
    with pytest.raises(ValueError, match="Selector literal inverse"):
        exporter.audit_wrapper(ROOT, wrapper, "bounded_QAE")


def test_range_target_hash_uses_documented_canonical_serialization(tmp_path):
    import hashlib
    import json

    target = tmp_path / "target.json"
    value = {"z": [1, 2], "a": {"beta": 3, "alpha": 4}}
    target.write_text(json.dumps(value, separators=(",", ":")) + "\n", encoding="utf-8")
    expected = hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()
    assert exporter.canonical_json_sha256(target) == expected
    assert exporter.sha256(target) != expected
    target.write_text(json.dumps(value, indent=7) + "\n", encoding="utf-8")
    assert exporter.canonical_json_sha256(target) == expected


def test_only_uniform_inputs_receive_random_preparation():
    source = dict(
        word_width=8,
        inputs=[
            dict(out=[0], params=dict(name="uniform_default", bits=4)),
            dict(out=[1], params=dict(name="provided", bits=8, preparation="provided")),
            dict(out=[2], params=dict(name="classical", bits=8, preparation="classical")),
            dict(out=[3], params=dict(name="uniform_explicit", bits=2, preparation="uniform")),
        ],
    )
    assert exporter.random_input_wires(source) == [0, 1, 2, 3, 24, 25]
