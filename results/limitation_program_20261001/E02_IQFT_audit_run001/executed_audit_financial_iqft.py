"""Independent interval-matrix and complete logical-IQFT retargeting audit.

The archived generation routine and current retargeter are never imported.
Matrices follow physical token execution; only unconditional scalar phases are
removed. Tiny Fourier checks use saved full-recipe segments, not financial or
large QPE replays.
"""

from __future__ import annotations

# Exact receipt descriptions remain readable prose.
# ruff: noqa: E501

import argparse
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import shutil
import sys
import traceback
import xml.etree.ElementTree as ET

import mpmath as mp
import numpy as np

from research.limitation_program_20261001.audit_financial_estimator import (
    independent_pi_interval,
    receipt_files,
)
from research.limitation_program_20261001.progress import ROOT

PROGRAM = ROOT / "results/limitation_program_20261001"
SOURCE = PROGRAM / "E02_financial_run002"
SOURCE_AUDIT = PROGRAM / "E02_financial_audit_run001"
ARCHIVE = ROOT / "results/controlled_completion_followup/synthesis_rotations.json"
KEYS = ["pi_1_%d" % (1 << (gap + 1)) for gap in range(2, 16)]


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def relative(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def pair(value):
    return [value.numerator, value.denominator]


def verify(files):
    for name, expected in files.items():
        assert sha(ROOT / name) == expected, ("frozen file changed", name)


def interval_upper(value):
    sign, mantissa, exponent, _ = value._mpi_[1]
    return Fraction((-1) ** sign * mantissa) * Fraction(2) ** exponent


def interval_matrix_error(string, denominator):
    """Left-apply reversed actual tokens, including W, with independent pi."""
    iv = mp.iv
    iv.dps = 150
    lo, hi = independent_pi_interval()
    lower, upper = iv.mpf(lo.numerator) / lo.denominator, iv.mpf(hi.numerator) / hi.denominator
    pi = iv.mpf([lower.a, upper.b])
    zero, one = iv.mpc(0), iv.mpc(1)
    rt = iv.sqrt(2)
    omega = iv.mpc(1 / rt, 1 / rt)
    tokens = {
        "H": ((one / rt, one / rt), (one / rt, -one / rt)),
        "X": ((zero, one), (one, zero)),
        "S": ((one, zero), (zero, iv.mpc(0, 1))),
        "T": ((one, zero), (zero, omega)),
        "W": ((omega, zero), (zero, omega)),
    }
    result = ((one, zero), (zero, one))
    for token in reversed(string):
        gate = tokens[token]
        result = tuple(
            tuple(sum(gate[row][k] * result[k][column] for k in range(2)) for column in range(2))
            for row in range(2)
        )
    half = pi / (2 * denominator)
    target = (
        (iv.mpc(iv.cos(half), -iv.sin(half)), zero),
        (zero, iv.mpc(iv.cos(half), iv.sin(half))),
    )
    squared = iv.mpf(0)
    for row in range(2):
        for column in range(2):
            delta = result[row][column] - target[row][column]
            squared += delta.real**2 + delta.imag**2
    return interval_upper(squared)


def audit_rotations(records):
    archive = read(ARCHIVE)
    epsilon = Fraction(*archive["common_operator_epsilon_exact"])
    assert epsilon == Fraction(1, 380759062412124000)
    assert set(records) == set(KEYS)
    reports = {}
    for gap, key in zip(range(2, 16), KEYS, strict=True):
        saved, original = records[key], archive["rotations"][key]
        spec = dict(kind="pi", numerator=1, denominator=1 << (gap + 1))
        assert saved["target"] == original["target"] == spec
        string = saved["matrix_product_gates"]
        assert (
            string == original["matrix_product_gates"] and string and not set(string) - set("HTSXW")
        )
        squared = interval_matrix_error(string, spec["denominator"])
        assert squared <= Fraction(*saved["frobenius_error_squared_upper_exact"]) <= epsilon**2
        assert squared <= Fraction(original["frobenius_error_squared_upper"])
        assert saved["t_count"] == original["t_count"] == string.count("T")
        assert (
            saved["clifford_count"]
            == original["clifford_count"]
            == sum(string.count(token) for token in "HSX")
        )
        assert saved["global_w_count"] == string.count("W")
        assert saved["physical_clifford_t_depth"] == len(string) - string.count("W")
        assert Fraction(*saved["operator_error_upper_exact"]) == epsilon
        assert saved["positive_execution_order"] == "reverse string, omitting scalar W"
        assert (
            saved["negative_execution_order"]
            == "forward string with daggered tokens, omitting scalar W"
        )
        reports[key] = dict(
            passed=True,
            target=spec,
            t_count=string.count("T"),
            actual_non_scalar_gate_count=len(string) - string.count("W"),
            independently_enclosed_frobenius_error_squared_upper=pair(squared),
            charged_operator_error_upper=pair(epsilon),
            interval_decimal_precision=150,
            independent_rational_pi_used=True,
            archive_generator_imported=False,
        )
        print(key, "independent interval matrix PASS", flush=True)
    return reports, epsilon


def signed_ops(wire, gap, sign, records):
    assert sign in (-1, 1)
    if gap == 1:
        return [dict(gate="t" if sign == 1 else "tdg", wires=[wire])]
    string = records["pi_1_%d" % (1 << (gap + 1))]["matrix_product_gates"]
    tokens = {
        "H": "h",
        "X": "x",
        "S": "s" if sign == 1 else "sdg",
        "T": "t" if sign == 1 else "tdg",
    }
    return [
        dict(gate=tokens[token], wires=[wire])
        for token in (reversed(string) if sign == 1 else string)
        if token != "W"
    ]


def reconstruct_recipe(controls, records):
    swaps = [
        dict(gate="swap", wires=[controls[j], controls[-1 - j]]) for j in range(len(controls) // 2)
    ]
    operations, stages = list(swaps), []
    for target_index, target in enumerate(controls):
        stage = []
        for control_index in range(target_index):
            control, gap = controls[control_index], target_index - control_index
            block = signed_ops(control, gap, -1, records) + signed_ops(target, gap, -1, records)
            block += [dict(gate="cx", wires=[control, target])]
            block += signed_ops(target, gap, 1, records) + [
                dict(gate="cx", wires=[control, target])
            ]
            stage += block
        stage.append(dict(gate="h", wires=[target]))
        stages.append(stage)
        operations += stage
    return operations, stages


def operation_matrix(operations, bits):
    """Independent dense evaluator; columns transform simultaneously."""
    dimension = 1 << bits
    matrix = np.eye(dimension, dtype=np.complex128)
    indices = np.arange(dimension, dtype=np.int64)
    phases = {"t": np.exp(1j * np.pi / 4), "tdg": np.exp(-1j * np.pi / 4), "s": 1j, "sdg": -1j}
    for operation in operations:
        gate, wires = operation["gate"], operation["wires"]
        if gate in ("cx", "swap"):
            permutation = indices.copy()
            a, b = wires
            active = (
                (((indices >> a) & 1) != 0)
                if gate == "cx"
                else (((indices >> a) ^ (indices >> b)) & 1) != 0
            )
            permutation[active] ^= (1 << b) if gate == "cx" else (1 << a) | (1 << b)
            matrix = matrix[permutation]
        elif gate in ("h", "x"):
            wire = wires[0]
            lower = indices[((indices >> wire) & 1) == 0]
            upper = lower | (1 << wire)
            original_low, original_high = matrix[lower].copy(), matrix[upper].copy()
            if gate == "x":
                matrix[lower], matrix[upper] = original_high, original_low
            else:
                matrix[lower], matrix[upper] = (
                    (original_low + original_high) / np.sqrt(2),
                    (original_low - original_high) / np.sqrt(2),
                )
        else:
            assert gate in phases
            matrix[((indices >> wires[0]) & 1) == 1] *= phases[gate]
    return matrix


def audit_signed_cp(records):
    reports = []
    for gap in range(1, 16):
        positive = operation_matrix(signed_ops(0, gap, 1, records), 1)
        negative = operation_matrix(signed_ops(0, gap, -1, records), 1)
        assert np.max(np.abs(negative @ positive - np.eye(2))) < 2e-12
        assert np.max(np.abs(negative - positive.conj().T)) < 2e-12
        ratio = positive[1, 1] / positive[0, 0]
        assert abs(ratio - np.exp(1j * np.pi / (1 << (gap + 1)))) < 2e-12
        ops = signed_ops(0, gap, -1, records) + signed_ops(1, gap, -1, records)
        ops += (
            [dict(gate="cx", wires=[0, 1])]
            + signed_ops(1, gap, 1, records)
            + [dict(gate="cx", wires=[0, 1])]
        )
        actual = operation_matrix(ops, 2)
        target = np.diag([1, 1, 1, np.exp(-1j * np.pi / (1 << gap))])
        scalar = actual[0, 0]
        maximum = float(np.max(np.abs(actual - scalar * target)))
        assert maximum < 2e-12
        assert abs(abs(scalar) - 1) < 2e-12
        # Every physical factor is unconditional. Its W contributes a scalar
        # on the whole two-qubit register, never a controlled branch sign.
        reports.append(
            dict(
                gap=gap,
                passed=True,
                half_angle_denominator=1 << (gap + 1),
                controlled_phase_denominator=1 << gap,
                signed_adjoint_verified=True,
                CP_matrix_error_up_to_scalar=maximum,
                only_unconditional_scalar_phases_omitted=True,
            )
        )
    return reports


def tiny_fourier_checks(controls, actual, stages):
    # Actual full16 operations were matched exactly before slicing. Keep each
    # complete j-stage for j<bits; reduced-width bit reversal belongs to that
    # canonical family, not a partial full16 SWAP that reaches discarded wires.
    results = []
    positions = {wire: index for index, wire in enumerate(controls)}
    for bits in (2, 3, 4):
        swaps = [dict(gate="swap", wires=[j, bits - 1 - j]) for j in range(bits // 2)]
        selected = [op for stage in stages[:bits] for op in stage]
        assert all(all(positions[wire] < bits for wire in op["wires"]) for op in selected)
        operations = swaps + [
            dict(gate=op["gate"], wires=[positions[wire] for wire in op["wires"]])
            for op in selected
        ]
        matrix = operation_matrix(operations, bits)
        dimension = 1 << bits
        row, column = np.indices((dimension, dimension))
        ideal = np.exp(-2j * np.pi * row * column / dimension) / np.sqrt(dimension)
        scalar = matrix[0, 0] / ideal[0, 0]
        error = float(np.max(np.abs(matrix - scalar * ideal)))
        unitarity = float(np.max(np.abs(matrix.conj().T @ matrix - np.eye(dimension))))
        assert error < 2e-12 and unitarity < 2e-12
        results.append(
            dict(
                bits=bits,
                passed=True,
                inverse_Fourier_error_up_to_terminal_scalar=error,
                unitarity_error=unitarity,
                actual_saved_signed_string_segments_used=True,
                reduced_width_bit_reversal_explicit=True,
                large_QPE_execution=False,
            )
        )
    return results


def audit_row(case, producer, records, epsilon):
    original_path = SOURCE / case / "estimator_ledger.json"
    original = read(original_path)
    row = read(producer / case / "synthesized_estimator_ledger.json")
    actual = read(producer / case / "iqft_operations.json")
    controls = original["qpe_register_wires"]
    assert len(controls) == len(set(controls)) == 16 and original["serial_shots"] == 15
    wrapper = read(SOURCE / case / "iterate.json")
    assert controls == wrapper["allowed_qpe_control_wires"][:16]
    assert not set(controls).intersection(wrapper["random_wires"] + [wrapper["selector_flag_wire"]])
    assert row["original_source_estimator_ledger"] == relative(original_path)
    assert row["original_source_estimator_ledger_sha256"] == sha(original_path)
    assert (
        original["full_T_count"]
        is original["full_T_depth"]
        is original["synthesis_certificate"]
        is None
    )
    changed = {"schema", "synthesis_certificate", "full_T_count", "full_T_depth"}
    assert all(row[key] == value for key, value in original.items() if key not in changed)
    expected, stages = reconstruct_recipe(controls, records)
    assert actual == expected
    saved_stages, cursor = [], len(controls) // 2
    for stage in stages:
        saved = actual[cursor : cursor + len(stage)]
        assert saved == stage
        saved_stages.append(saved)
        cursor += len(stage)
    assert cursor == len(actual)
    assert all(
        op["gate"] in ("swap", "cx", "h", "x", "s", "sdg", "t", "tdg")
        and len(op["wires"]) == (2 if op["gate"] in ("swap", "cx") else 1)
        and set(op["wires"]) <= set(controls)
        and len(set(op["wires"])) == len(op["wires"])
        for op in actual
    )
    counts = Counter(op["gate"] for op in actual)
    assert row["iqft_per_shot_physical_gate_counts"] == dict(counts)
    usage = {key: 45 * (16 - gap) for gap, key in zip(range(2, 16), KEYS, strict=True)}
    assert sum(usage.values()) == original["iqft_arbitrary_Rz_rotations"] == 4725
    assert row["synthesized_rotation_usage"] == usage
    t_count = sum(records[key]["t_count"] * uses for key, uses in usage.items())
    clifford = sum(records[key]["clifford_count"] * uses for key, uses in usage.items())
    assert (
        row["synthesized_single_qubit_T_count"] == t_count
        and row["synthesized_single_qubit_clifford_count"] == clifford
    )
    assert 15 * (counts["t"] + counts["tdg"]) == original["iqft_exact_CS_T_count"] + t_count
    assert counts["cx"] == 240 and counts["swap"] == 8
    observation = 2 * epsilon * 4725
    assert (
        Fraction(*row["synthesis_total_observation_perturbation_upper_exact"])
        == observation
        <= Fraction(1, 1000)
    )
    assert (
        epsilon
        < Fraction(*original["required_each_rotation_operator_error"])
        == Fraction(1, 9450000)
    )
    assert row["synthesis_certificate"] == relative(producer / case / "iqft_operations.json")
    unit, Q = original["source_iterate_resources"], 983025
    actual_iqft_t = 15 * (counts["t"] + counts["tdg"])
    assert (
        row["full_T_count"]
        == Q * unit["t_count"] + actual_iqft_t
        == original["complete_known_T_count_excluding_arbitrary_rotation_synthesis"] + t_count
    )
    assert (
        row["full_T_depth"]
        == Q * unit["t_depth"] + actual_iqft_t
        == original["serial_known_T_depth_excluding_arbitrary_rotation_synthesis"] + t_count
    )
    iqft_serial_ct = len(actual) + 2 * counts["swap"]
    full_ct = Q * unit["clifford_t_depth"] + 15 * (2 + iqft_serial_ct)
    assert row["full_known_clifford_t_depth_upper"] == full_ct
    full_counts = dict(
        t=row["full_T_count"],
        clifford_cx=Q * unit["clifford_cx"] + 15 * (counts["cx"] + 3 * counts["swap"]),
        clifford_h=Q * unit["clifford_h"]
        + original["uniform_preparation_H"]
        + original["qpe_preparation_H"]
        + 15 * counts["h"],
        clifford_s_or_sdg=15 * (counts["s"] + counts["sdg"]),
        x=Q * unit["x"] + 15 * counts["x"],
        clifford_cz=Q * unit["clifford_cz"],
        clifford_z=Q * unit["clifford_z"],
    )
    for field in (
        "physical_runtime_seconds",
        "full_physical_runtime_seconds",
        "total_readout_or_reset_seconds",
    ):
        assert row[field] is None
    assert row["logical_qubits"] == original["logical_qubits"]
    assert (
        row["ideal_digital_estimator_with_synthesis_certificate"]
        and not row["full_continuous_price_certificate"]
        and not row["full_physical_execution_certificate"]
    )
    assert row["G2_to_G5"] == "open"
    tiny = tiny_fourier_checks(controls, actual, saved_stages)
    return dict(
        passed=True,
        case=case,
        logical_qubits=row["logical_qubits"],
        full_T_count=row["full_T_count"],
        full_logical_serial_T_depth=row["full_T_depth"],
        full_known_clifford_t_depth_upper=full_ct,
        independently_reconstructed_complete_primitive_counts=full_counts,
        iqft_synthesis_T_count=t_count,
        iqft_per_shot_physical_gate_counts=dict(counts),
        synthesis_observation_perturbation_upper=pair(observation),
        serial_fresh_shots=15,
        source_graph_directions_unchanged=1966050,
        original_source_row_unchanged=True,
        terminal_global_phase_only=True,
        tiny_inverse_Fourier_checks=tiny,
        physical_runtime_seconds=None,
        new_financial_gate_replays=0,
    )


def xml_count(path):
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root)
    cases = [
        (case.get("classname"), case.get("name"))
        for suite in suites
        for case in suite.findall("testcase")
    ]
    assert len(cases) == len(set(cases)) == sum(int(suite.get("tests", 0)) for suite in suites)
    assert all(
        int(suite.get(field, 0)) == 0
        for suite in suites
        for field in ("failures", "errors", "skipped")
    )
    return len(cases)


def prepare(producer, output):
    producer, output = Path(producer).resolve(), Path(output).resolve()
    producer.relative_to(PROGRAM)
    output.relative_to(PROGRAM)
    assert read(producer / "summary.json")["passed"] and not output.exists()
    frozen = {}
    for directory in (SOURCE, SOURCE_AUDIT, producer):
        frozen.update(receipt_files(directory))
    own = Path(__file__).resolve()
    frozen[relative(own)] = sha(own)
    frozen[relative(ARCHIVE)] = sha(ARCHIVE)
    verify(frozen)
    output.mkdir()
    shutil.copy2(own, output / "executed_audit_financial_iqft.py")
    save(
        output / "protocol.json",
        dict(
            local_only=True,
            created_utc=datetime.now(timezone.utc).isoformat(),
            before_independent_audit=True,
            producer=relative(producer),
            frozen_inputs=frozen,
            interpreter_sha256=sha(sys.executable),
            interval_matrix_decimal_precision=150,
            interval_pi="Independent rational atan(1/2)+atan(1/3),240 terms each",
            target_keys=KEYS,
            cases=["B4x12", "B8x52"],
            rotation_applications_per_price=4725,
            scope="Independently left-applied14 archived interval matrices; signed adjoints; exact3Rz+2CX controlled-phase halves; every physical terminal IQFT operation and serial15-shot cost; tiny2/3/4 inverse-Fourier matrices using actual recipe segments; scalarW onlyuncontrolled/terminal; source55tests/sixmarkingrecords remain frozen; null physical and continuous-price obligations",
            new_rotation_generation=0,
            new_financial_candidates=0,
            new_financial_gate_replays=0,
            new_distinct_pytest_cases=0,
            huge_QPE_executions=0,
            G2_to_G5="open",
        ),
    )
    print("Independent financial IQFT audit protocol frozen", flush=True)


def run(output):
    output = Path(output).resolve()
    assert not (output / "summary.json").exists()
    protocol = read(output / "protocol.json")
    verify(protocol["frozen_inputs"])
    assert sha(sys.executable) == protocol["interpreter_sha256"]
    producer = ROOT / protocol["producer"]
    prospective, summary = read(producer / "protocol.json"), read(producer / "summary.json")
    assert (
        prospective["target_keys"] == KEYS
        and prospective["qpe_bits"] == 16
        and prospective["serial_shots"] == 15
    )
    assert prospective["usage"] == 4725 and prospective["new_financial_gate_replays"] == 0
    assert (
        prospective["physical_routing_factories_readout_durations"] is None
        and not prospective["original_source_or_estimator_rows_edited"]
    )
    assert summary["passed"] and summary["reused_distinct_rotations"] == 14
    assert (
        summary["total_arbitrary_rotation_applications_per_price"] == 4725
        and summary["complete_logical_estimator_recipe"]
    )
    assert (
        not summary["physical_runtime_certified"]
        and not summary["continuous_price_error_certified"]
    )
    assert (
        summary["new_financial_gate_replays"] == summary["huge_QPE_statevector_runs"] == 0
        and summary["G2_to_G5"] == "open"
    )
    assert xml_count(producer / "tests.xml") == 5 and xml_count(SOURCE / "tests.xml") == 55
    assert (
        read(SOURCE_AUDIT / "summary.json")["recorded_financial_source_marking_replays_reconciled"]
        == 6
    )
    records = read(producer / "rotations.json")
    rotations, epsilon = audit_rotations(records)
    save(output / "independent_rotation_interval_audit.json", rotations)
    cp = audit_signed_cp(records)
    save(output / "signed_CP_matrix_audit.json", cp)
    cases = []
    for case in ("B4x12", "B8x52"):
        report = audit_row(case, producer, records, epsilon)
        row = next(row for row in summary["cases"] if row["case"] == case)
        for key in row:
            assert row[key] == report[key], (case, key)
        save(output / (case + "_IQFT_audit.json"), report)
        cases.append(report)
        print(case, "complete physical token recipe/logical cost audit PASS", flush=True)
    result = dict(
        passed=True,
        local_only=True,
        independent_interval_matrix_and_complete_IQFT_audit=True,
        rotations_verified=14,
        signed_CP_halfangle_cases_verified=15,
        arbitrary_rotations_per_price=4725,
        complete_IQFT_bits=16,
        serial_fresh_shots=15,
        producer_distinct_pytest_cases_reconciled=5,
        frozen_source_distinct_pytest_cases_reconciled=55,
        frozen_source_marking_replays_unchanged=6,
        new_distinct_pytest_cases=0,
        new_financial_gate_replays=0,
        new_financial_candidates=0,
        new_rotation_generation=0,
        tiny_inverse_Fourier_matrix_cases=6,
        huge_QPE_executions=0,
        cases=[
            {key: value for key, value in case.items() if key != "tiny_inverse_Fourier_checks"}
            for case in cases
        ],
        synthesis_observation_perturbation_upper=pair(2 * epsilon * 4725),
        source_controlled_reflection_Z_sign_retained=True,
        only_uncontrolled_terminal_scalar_W_omitted=True,
        physical_runtime_seconds=None,
        readout_or_reset_seconds=None,
        full_continuous_price_certificate=False,
        G2_to_G5="open",
    )
    save(output / "summary.json", result)
    verify(protocol["frozen_inputs"])
    save(
        output / "manifest.json",
        dict(
            files={relative(file): sha(file) for file in output.rglob("*") if file.is_file()},
            frozen_inputs=protocol["frozen_inputs"],
            manifest_self_hash_excluded=True,
        ),
    )
    print("Independent complete financial IQFT audit PASS", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "run"))
    parser.add_argument("--producer", type=Path, default=PROGRAM / "E02_IQFT_run001")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.phase == "prepare":
        prepare(args.producer, args.output)
    else:
        try:
            run(args.output)
        except Exception as error:
            output = args.output.resolve()
            (output / "failure.txt").write_text(traceback.format_exc(), encoding="utf-8")
            save(
                output / "summary.json",
                dict(
                    passed=False,
                    local_only=True,
                    failure_type=type(error).__name__,
                    message=str(error),
                    new_financial_candidates=0,
                    new_financial_gate_replays=0,
                ),
            )
            save(
                output / "manifest.json",
                dict(
                    files={
                        relative(file): sha(file) for file in output.rglob("*") if file.is_file()
                    },
                    frozen_inputs=read(output / "protocol.json")["frozen_inputs"],
                    manifest_self_hash_excluded=True,
                ),
            )
            raise
