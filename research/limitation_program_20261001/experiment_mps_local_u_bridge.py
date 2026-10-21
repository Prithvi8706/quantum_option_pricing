"""Freeze then execute one saved8x8 SDK U bridge, with no Gaussian adoption."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import sys
import traceback
import xml.etree.ElementTree as ET

from research.limitation_program_20261001.mps_local_u_bridge import (
    ADMISSION,
    ALLOWANCE,
    CPU,
    DPS,
    MATRIX_HASH,
    NATIVE_SLOTS,
    ROOT_BITS,
    SDK_ROWS,
    WALL,
    Budget,
    BudgetCensoredError,
    binary64_pair,
    bridge,
    certify,
    fingerprint,
    inverse,
    literal_matrix,
    pair,
    require,
)

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
PROGRAM = ROOT / "results/limitation_program_20261001"
INTERPRETER = ROOT / ".context/controlled_closeout_repro/Scripts/python.exe"
SITE = INTERPRETER.parent.parent / "Lib/site-packages"
RECEIPT = PROGRAM / "A04_mps_u_bridge_run001"
PLAN = PROGRAM / "A04_mps_run001/bond4/structure_plan.json"
PREFLIGHT = RESEARCH / "mps_local_u_bridge_preflight.json"
CODE = (
    "mps_local_u_bridge.py",
    "experiment_mps_local_u_bridge.py",
    "test_mps_local_u_bridge.py",
    "audit_mps_local_u_bridge.py",
)
DOCS = (
    "MPS_LOCAL_U_BRIDGE_PREFLIGHT.md",
    "mps_local_u_bridge_preflight.json",
    "MPS_LOCAL_U_BRIDGE_NEXT_PREFLIGHT.md",
    "mps_local_u_bridge_next_preflight.json",
)
TESTS = 6


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write("\n")


def sha(path, budget=None):
    result = hashlib.sha256()
    with Path(path).open("rb") as stream:
        while True:
            if budget is not None:
                budget.check()
            block = stream.read(1 << 20)
            if not block:
                break
            result.update(block)
            if budget is not None:
                budget.check()
    return result.hexdigest()


def relative(path):
    return Path(path).resolve().relative_to(ROOT.resolve()).as_posix()


def bind(frozen, name, expected):
    path = (ROOT / str(name).replace("\\", "/")).resolve()
    path.relative_to(ROOT.resolve())
    key = relative(path)
    require(
        type(expected) is str
        and len(expected) == 64
        and all(c in "0123456789abcdef" for c in expected),
        "Canonical expected SHA256",
    )
    require(key not in frozen or frozen[key] == expected, "No frozen expectation override: " + key)
    frozen[key] = expected


def verify(frozen, budget=None):
    for name, expected in frozen.items():
        if budget is not None:
            budget.check()
        require(sha(ROOT / name, budget) == expected, "Frozen bridge input changed: " + name)


def prior_receipt(name, frozen, expected_manifest=None, dependency_maps=True, budget=None):
    directory = PROGRAM / name
    manifest = directory / "manifest.json"
    actual = sha(manifest, budget)
    require(
        expected_manifest is None or actual == expected_manifest, "Prior manifest changed: " + name
    )
    record = read(manifest)
    require(
        type(record["files"]) is dict and type(record.get("frozen_inputs", {})) is dict,
        "Prior canonical manifest maps",
    )
    for field in ("files", "frozen_inputs") if dependency_maps else ("files",):
        for path, expected in record[field].items():
            bind(frozen, path, expected)
    bind(frozen, manifest, actual)
    return read(directory / "summary.json")


def tool_environment(frozen, budget=None):
    require(
        Path(sys.executable).resolve() == INTERPRETER.resolve(), "Pinned controlled SDK interpreter"
    )
    require(
        importlib.metadata.version("numpy") == "1.26.4"
        and importlib.metadata.version("qiskit-terra") == "0.45.3",
        "Pinned original SDK versions",
    )
    if frozen is None:
        return
    bind(frozen, INTERPRETER, sha(INTERPRETER, budget))
    for name in ("mpmath", "pytest", "_pytest"):
        directory = SITE / name
        require(directory.is_dir(), "Existing tool package required: " + name)
        for path in sorted(directory.rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
                bind(frozen, path, sha(path, budget))


def fixed_matrix():
    plan = read(PLAN)
    row = plan["transitions"][1]
    require(
        (row["site"], row["left_rank"], row["right_rank"], row["local_wires"])
        == (1, 2, 4, [10, 11, 8]),
        "Exactly saved bond4 site1 and wire order",
    )
    matrix = row["completed_local_matrix"]
    require(fingerprint(matrix) == MATRIX_HASH, "Exact saved matrix literal fingerprint")
    literal_matrix(matrix)
    return matrix


def seal(output, record, budget):
    budget.check()
    content = (json.dumps(record, indent=2, allow_nan=False) + "\n").encode()
    budget.check()
    with (output / "manifest.json").open("xb") as stream:
        for offset in range(0, len(content), 1 << 20):
            budget.check()
            stream.write(content[offset : offset + (1 << 20)])
            budget.check()


def finish(output, frozen, budget, summary):
    verify(frozen, budget)
    save(output / "summary.json", summary)
    files = {relative(p): sha(p, budget) for p in sorted(output.rglob("*")) if p.is_file()}
    verify(frozen, budget)
    cpu, wall = budget.check()
    seal(
        output,
        dict(
            files=files,
            frozen_inputs=frozen,
            manifest_self_hash_excluded=True,
            all_inputs_and_bulk_hashes_verified_before_terminal=True,
            process_CPU_seconds_before_terminal=cpu,
            wall_seconds_before_terminal=wall,
        ),
        budget,
    )


def preserve_failure(output, frozen, failure, phase, sdk_calls, budget):
    if not output.exists():
        return
    try:
        budget.check()
        retain_failure(output, frozen, failure, phase, sdk_calls, budget)
    except BaseException as sealing_failure:
        marker = output / "failed_unsealed.json"
        if not marker.exists():
            save(
                marker,
                dict(
                    passed=False,
                    local_only=True,
                    receipt_unsealed=True,
                    hard_terminal_budget_exhausted=isinstance(sealing_failure, BudgetCensoredError),
                    budget_censored=isinstance(sealing_failure, BudgetCensoredError)
                    or isinstance(failure, (BudgetCensoredError, TimeoutError)),
                    phase=phase,
                    failure_type=type(failure).__name__,
                    message=str(failure)[:1024],
                    sealing_failure_type=type(sealing_failure).__name__,
                    actual_SDK_calls_started=sdk_calls,
                    new_test_credit=0,
                    fixed_receipt_terminal_no_retry=True,
                    no_further_hashing_or_verification=True,
                ),
            )


def retain_failure(output, frozen, failure, phase, sdk_calls, budget):
    budget.check()
    save(
        output / (phase + "_failure.json"),
        dict(
            failure_type=type(failure).__name__,
            message=str(failure),
            traceback=traceback.format_exc(),
            fixed_receipt_terminal_no_retry=True,
            files_preserved=True,
        ),
    )
    terminal = output / (
        "completion_outcome.json" if (output / "summary.json").exists() else "summary.json"
    )
    save(
        terminal,
        dict(
            passed=False,
            local_only=True,
            preparation_failed=phase == "prepare",
            budget_censored=isinstance(failure, (BudgetCensoredError, TimeoutError)),
            actual_SDK_calls_started=sdk_calls,
            new_test_credit=0,
            fixed_receipt_terminal_no_retry=True,
            full_Gaussian_loader_certified=False,
            native_financial_cost=None,
            Clifford_T_cost=None,
            quantum_advantage_established=False,
        ),
    )
    if not (output / "manifest.json").exists():
        error = None
        try:
            verify(frozen, budget)
        except BudgetCensoredError:
            raise
        except BaseException as verification:
            error = str(verification)
        files = {relative(p): sha(p, budget) for p in sorted(output.rglob("*")) if p.is_file()}
        seal(
            output,
            dict(
                files=files,
                frozen_inputs=frozen,
                manifest_self_hash_excluded=True,
                terminal_record=relative(terminal),
                failure_inputs_verified=error is None,
                verification_error=error,
                failure_or_censor_preserved_without_retry=True,
            ),
            budget,
        )
    else:
        raise ValueError("Failure cannot replace an existing terminal or partial manifest")


def prepare(output):
    output = Path(output).resolve()
    require(
        output == RECEIPT.resolve() and not output.exists(), "One fresh exclusive local receipt"
    )
    frozen, budget = {}, Budget()
    try:
        preflight = read(PREFLIGHT)
        require(
            preflight["fixed_fixture_count"] == TESTS
            and preflight["maximum_SDK_calls"] == 1
            and preflight["process_CPU_seconds"] == CPU
            and preflight["admission_CPU_seconds"] == ADMISSION
            and preflight["wall_seconds"] == WALL
            and preflight["decimal_digits"] == DPS
            and preflight["outward_root_bits"] == ROOT_BITS
            and preflight["local_allowance_exact"] == pair(ALLOWANCE),
            "Fixed bridge preflight",
        )
        for name, expected in preflight["immutable_prior_manifest_sha256"].items():
            summary = prior_receipt(name, frozen, expected, budget=budget)
            require(
                summary["passed"] is True and not summary.get("budget_censored", False),
                "Completed immutable MPS prerequisite: " + name,
            )
        # WAVE10's archived/current reconciliation deliberately retains historical live mismatches.
        # Its complete owned packet is bound as the release evidence; no historical SHA is waived.
        wave = prior_receipt("WAVE10_run001", frozen, dependency_maps=False, budget=budget)
        require(
            wave["passed"] is True
            and wave["archived_or_current_integrity_passed"] is True
            and wave["global_live_integrity"] is False
            and wave["legitimate_expected_hashes_waived"] is False,
            "Completed WAVE10 reconciliation with historical mismatch evidence retained",
        )
        snapshot = read(PROGRAM / "WAVE10_run001/progress_snapshot.json")
        require(
            snapshot["static_author_preflights"]["dependency_order"]
            == preflight["fixed18_selected_labels"],
            "Exact WAVE10 fixed18 label release",
        )
        require(
            read(PROGRAM / "A03_law_screen_run001/summary.json")[
                "q10_uniform_certificate_meets_fixed_law_budget"
            ]
            is False,
            "Preserve failed q10 law",
        )
        tool_environment(frozen, budget)
        for name in CODE + DOCS:
            bind(frozen, RESEARCH / name, sha(RESEARCH / name, budget))
        matrix = fixed_matrix()
        verify(frozen, budget)
        budget.check(admission=True)
        output.mkdir()
        for name in CODE + DOCS:
            shutil.copy2(RESEARCH / name, output / name)
            require(
                sha(output / name, budget) == frozen[relative(RESEARCH / name)],
                "Copied source differs",
            )
            bind(frozen, output / name, frozen[relative(RESEARCH / name)])
        save(output / "saved_matrix.json", matrix)
        bind(frozen, output / "saved_matrix.json", sha(output / "saved_matrix.json", budget))
        verify(frozen, budget)
        budget.check()
        save(
            output / "protocol.json",
            dict(
                schema="one-saved8x8-MPS-U-bridge-protocol-v1",
                created_utc=datetime.now(timezone.utc).isoformat(),
                local_only=True,
                frozen_before_SDK_operator_tests=True,
                frozen_inputs=frozen,
                matrix_literal_sha256=MATRIX_HASH,
                matrix_source=relative(PLAN),
                matrix_transition=1,
                local_qubits=3,
                global_wires=[10, 11, 8],
                fixed_matrices=1,
                maximum_SDK_calls=1,
                SDK_basis=["u", "cx"],
                SDK_optimization_level=0,
                SDK_seed_transpiler=0,
                UnitaryGate_check_input=True,
                maximum_SDK_rows=SDK_ROWS,
                maximum_native_slots=NATIVE_SLOTS,
                phase_slots_charged=1,
                controlled_phase_cost_requires_future_ledger=True,
                decimal_digits=DPS,
                outward_root_bits=ROOT_BITS,
                local_allowance_exact=pair(ALLOWANCE),
                declared_unique_tests=TESTS,
                old_fixture_recredit=0,
                process_CPU_seconds=CPU,
                admission_CPU_seconds=ADMISSION,
                wall_seconds=WALL,
                numerical_threads=1,
                requires_root_exclusive_timing_clearance=True,
                no_precision_basis_site_or_method_retry=True,
                Gaussian_CDF_SVD_QR_synthesis_calls=0,
                full_Gaussian_loader_certified=False,
                native_financial_cost=None,
                Clifford_T_cost=None,
            ),
        )
        verify(frozen, budget)
        budget.check()
    except BaseException as failure:
        preserve_failure(output, frozen, failure, "prepare", 0, budget)
        raise


def run(output):
    output = Path(output).resolve()
    require(output == RECEIPT.resolve(), "Exact prepared one-matrix receipt")
    protocol = read(output / "protocol.json")
    require(
        not (output / "summary.json").exists() and not (output / "sdk_attempt.json").exists(),
        "Terminal or started receipt cannot retry",
    )
    frozen, budget, calls = protocol["frozen_inputs"], Budget(), 0
    try:
        for key in (
            "OPENBLAS_NUM_THREADS",
            "MKL_NUM_THREADS",
            "OMP_NUM_THREADS",
            "NUMEXPR_NUM_THREADS",
            "NUMBA_NUM_THREADS",
        ):
            os.environ[key] = "1"
        os.environ["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
        verify(frozen, budget)
        tool_environment(None, budget)
        require(
            protocol["schema"] == "one-saved8x8-MPS-U-bridge-protocol-v1"
            and protocol["maximum_SDK_calls"] == 1
            and protocol["declared_unique_tests"] == TESTS
            and protocol["decimal_digits"] == DPS
            and protocol["outward_root_bits"] == ROOT_BITS
            and protocol["process_CPU_seconds"] == CPU
            and protocol["admission_CPU_seconds"] == ADMISSION
            and protocol["wall_seconds"] == WALL
            and protocol["local_allowance_exact"] == pair(ALLOWANCE),
            "Frozen method and count",
        )
        target = read(output / "saved_matrix.json")
        require(
            fingerprint(target) == MATRIX_HASH and target == fixed_matrix(), "Prepared fixed matrix"
        )
        import numpy as np
        from qiskit import QuantumCircuit, transpile
        from qiskit.circuit.library import UnitaryGate

        budget.check(admission=True)
        array = np.array(
            [[complex(float(re), float(im)) for re, im in row] for row in literal_matrix(target)],
            dtype=np.complex128,
        )
        circuit = QuantumCircuit(3)
        circuit.append(UnitaryGate(array, check_input=True), [0, 1, 2])
        save(
            output / "sdk_attempt.json",
            dict(
                calls_started=1,
                fixed_matrix_sha256=MATRIX_HASH,
                basis=["u", "cx"],
                seed=0,
                optimization_level=0,
            ),
        )
        calls = 1
        compiled = transpile(
            circuit, basis_gates=["u", "cx"], optimization_level=0, seed_transpiler=0
        )
        budget.check()
        sdk = dict(
            schema="one-local-SDK-U-CX-v1",
            local_qubits=3,
            global_wires=[10, 11, 8],
            sdk_calls=1,
            sdk_global_phase_exact=binary64_pair(float(compiled.global_phase)),
            operations=[
                dict(
                    op=entry.operation.name,
                    wires=[compiled.find_bit(q).index for q in entry.qubits],
                    params_exact=[binary64_pair(float(p)) for p in entry.operation.params],
                )
                for entry in compiled.data
            ],
        )
        save(output / "sdk_operations.json", sdk)
        native = bridge(sdk)
        save(output / "native_operations.json", native)
        save(output / "native_inverse.json", dict(operations=inverse(native["operations"])))
        budget.check(admission=True)
        certificate = certify(sdk, native, target, budget.check)
        save(output / "operator_certificate.json", certificate)
        budget.check(admission=True)
        import pytest

        os.environ["MPS_LOCAL_U_BRIDGE_SOURCE"] = str(output)
        code = pytest.main(
            [
                str(output / "test_mps_local_u_bridge.py"),
                "-q",
                "-p",
                "no:cacheprovider",
                "--junitxml=" + str(output / "tests.xml"),
            ]
        )
        records = list(ET.parse(output / "tests.xml").getroot().iter("testcase"))
        require(
            code == 0
            and len(records)
            == len({(r.attrib.get("classname"), r.attrib["name"]) for r in records})
            == TESTS
            and not any(
                r.find(t) is not None for r in records for t in ("failure", "error", "skipped")
            ),
            "Exactly six successful unique bridge fixtures",
        )
        passed = certificate["passed"] is True
        finish(
            output,
            frozen,
            budget,
            dict(
                passed=passed,
                local_only=True,
                budget_censored=False,
                fixed_receipt_terminal_no_retry=True,
                actual_SDK_calls=calls,
                fixed_matrices=1,
                SDK_rows=len(sdk["operations"]),
                native_slots_including_paid_phase=len(native["operations"]),
                full_operator_entries=64,
                tests_completed=TESTS,
                new_unique_fixtures_passed=TESTS if passed else 0,
                new_test_credit=TESTS if passed else 0,
                old_fixture_recredit=0,
                full_phase_correct_local_operator_certified=passed,
                literal_inverse_full_operator_certified=passed,
                q10_financial_law_repaired=False,
                full_Gaussian_loader_certified=False,
                Gaussian_CDF_SVD_QR_synthesis_calls=0,
                native_financial_cost=None,
                Clifford_T_cost=None,
                controlled_phase_implementation_and_cost=None,
                quantum_advantage_established=False,
            ),
        )
    except BaseException as failure:
        preserve_failure(output, frozen, failure, "run", calls, budget)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "run"))
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    (prepare if args.phase == "prepare" else run)(args.output)


if __name__ == "__main__":
    main()
