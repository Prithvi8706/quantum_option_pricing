"""Freeze full B4/B8 hardware demand; no gate replay, clock or physical deployment."""

# Exact prospective protocol and provenance descriptions remain readable.
# ruff: noqa: E501

import argparse
from datetime import datetime, timezone
from pathlib import Path
import shutil
import sys
import time

import pytest

from research.controlled_priority_completion.parallel_source import entries
from research.controlled_source_completion.compact_parallel_v7 import _storage
from research.limitation_program_20261001.constant_library import digest
from research.limitation_program_20261001.experiment_checkpoint import (
    BASELINE,
    PROGRAM,
    manifest,
    read,
    relative,
    save,
    verify,
)
from research.limitation_program_20261001.hardware_demand import (
    ALLOCATIONS,
    PHYSICAL_ALLOWANCE,
    bottleneck_lower_bound,
    complete_price_demand,
    pair,
    source_batch_profile,
)
from research.limitation_program_20261001.progress import ROOT


SOURCE = PROGRAM / "E02_financial_run002"
SOURCE_AUDIT = PROGRAM / "E02_financial_audit_run001"
IQFT = PROGRAM / "E02_IQFT_run001"
IQFT_AUDIT = PROGRAM / "E02_IQFT_audit_run001"
SCHEDULE = PROGRAM / "E07_schedule_run001"
CODE = ("hardware_demand.py", "test_hardware_demand.py", "experiment_hardware_demand.py")
DOCS = (
    "docs/limitation_audit_20261001/implementation_plan/HARDWARE.md",
    "docs/limitation_audit_20261001/implementation_plan/CONTRACT.md",
    "docs/limitation_audit_20261001/HARDWARE_AND_COST_MODEL.md",
    "docs/controlled_priority_completion/CAPACITY_SCREEN.md",
    "manuscript/advantage-frontier-2026-09-23/WHY_NO_ADVANTAGE.md",
)


def prepare(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM.resolve())
    if output.exists():
        raise FileExistsError("H17 prospective receipt must be new")
    for directory in (SOURCE, SOURCE_AUDIT, IQFT, IQFT_AUDIT, SCHEDULE):
        if not read(directory / "summary.json")["passed"]:
            raise ValueError("Accepted complete logical estimator and audits required")
    if not read(SOURCE_AUDIT / "summary.json")["independent_actual_native_source_estimator_audit"]:
        raise ValueError("Actual native source/selector/reflection audit required")
    if not read(IQFT_AUDIT / "summary.json")["independent_interval_matrix_and_complete_IQFT_audit"]:
        raise ValueError("Complete IQFT synthesis and primitive-count audit required")
    allowance = next(
        term
        for term in read(SCHEDULE / "complete_price_ledger.json")["failure_terms"]
        if term["name"] == "physical_execution"
    )["allowance"]
    if allowance != pair(PHYSICAL_ALLOWANCE) or sum(ALLOCATIONS.values()) != PHYSICAL_ALLOWANCE:
        raise ValueError("Original complete physical failure allowance changed")
    frozen = {}
    for directory in (SOURCE, SOURCE_AUDIT, IQFT, IQFT_AUDIT, SCHEDULE):
        receipt = read(directory / "manifest.json")
        for field in ("files", "frozen_inputs"):
            for name, sha in receipt[field].items():
                frozen[name.replace("\\", "/")] = sha
        frozen[relative(directory / "manifest.json")] = digest(directory / "manifest.json")
    for name in DOCS:
        frozen[name] = digest(ROOT / name)
    for case in ("B4x12", "B8x52"):
        task = PROGRAM / "G0_run003" / (case + "_task.json")
        frozen[relative(task)] = digest(task)
    for name in (
        "research/limitation_program_20261001/checkpoint_circuit.py",
        "research/controlled_source_completion/compact_parallel_v7.py",
        "research/controlled_priority_completion/parallel_source.py",
    ):
        frozen[name] = digest(ROOT / name)
    output.mkdir()
    for name in CODE:
        path = ROOT / "research/limitation_program_20261001" / name
        snapshot = output / "executed_code" / name
        snapshot.parent.mkdir(exist_ok=True)
        shutil.copy2(path, snapshot)
        frozen[relative(path)] = digest(path)
    protocol = {
        "local_only": True,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "item": "H17/H18 source-compatible full-price hardware demand prerequisite",
        "before_tests_and_demand_count_evaluation": True,
        "cases": ["B4x12", "B8x52"],
        "estimator": "Same scalar already-discounted nativeY, selector46/span64, epsilon1/100, QPE16 bits/15 fresh shots/983025 controlled iterates",
        "source_count_basis": "Accepted original financial native arrays and copied controls, exact seven-T expansion, paid selector/reflection/marker, literal inverses, complete audited synthesized IQFT tokens; no flat billions-gate array",
        "fresh_H_rule": "r*(original+selector random bits + QPE bits), then the FULL terminal IQFT token recipe*r; superseded partial IQFT_H and CS fixed fields are not added again",
        "SWAP_expansion": "three logical CX gates only; physical routing cost remains unknown",
        "physical_failure_allowance_exact": pair(PHYSICAL_ALLOWANCE),
        "prospective_allocation_exact": {name: pair(value) for name, value in ALLOCATIONS.items()},
        "state_error_target": "magic_state_allocation/full_consumed_T_count",
        "data_and_control_gate_error_target": "respective allocation/full_expanded_primitive_gate_count",
        "primitive_gate_set": ["X", "CX", "H", "T_or_Tdg", "S_or_Sdg", "Z", "CZ"],
        "unknown_opportunities": [
            "idle code cycles",
            "protected reset",
            "feedback and readout",
            "routing and factory protection",
        ],
        "architecture_rows": 0,
        "maximum_architecture_rows": 3,
        "tau_grid": None,
        "physical_qubit_cap": None,
        "no_C4_H8_archived_physical_cap_clock_or_factory_fit_transferred": True,
        "acceptance": "All audited full primitive counts reconcile; every source batch, copied/repeated control, atomic native interface and high-output private slot is paid; allocations sum exactly3/1000; missing physical exposure, routing, code distances and executable latency remain null",
        "stop_rule": "One full demand ledger per accepted B4/B8 source; no new hardware model fit, physical clock grid, financial replay, classical timing or deployment",
        "full_physical_fidelity_certificate": False,
        "full_physical_latency_certificate": False,
        "process_cpu_limit_seconds": 300,
        "new_financial_gate_replays": 0,
        "new_financial_price_samples": 0,
        "preexisting_Stage_C_jobs_edited": False,
        "frozen_inputs": frozen,
        "python": sys.version,
        "executable": sys.executable,
    }
    save(output / "protocol.json", protocol)
    verify(protocol)
    print("H17/H18 full-demand prospective protocol frozen", flush=True)


def run(output):
    output = Path(output).resolve()
    if (output / "summary.json").exists():
        raise FileExistsError("H17 demand receipt already completed")
    protocol = read(output / "protocol.json")
    verify(protocol)
    started = time.process_time()
    rc = pytest.main(
        [
            str(ROOT / "research/limitation_program_20261001/test_hardware_demand.py"),
            "-q",
            "-p",
            "no:cacheprovider",
            "--junitxml=" + str(output / "tests.xml"),
        ]
    )
    if rc:
        save(output / "failed_tests.json", {"passed": False, "return_code": int(rc)})
        manifest(output, protocol)
        raise AssertionError("Frozen H17 demand fixtures failed")
    rows = []
    for case in protocol["cases"]:
        if time.process_time() - started > protocol["process_cpu_limit_seconds"]:
            save(output / "failed_limit.json", {"passed": False, "cpu_limit_seconds": 300})
            manifest(output, protocol)
            raise TimeoutError("H17 prospective CPU limit")
        wrapper = read(SOURCE / case / "iterate.json")
        row = read(IQFT / case / "synthesized_estimator_ledger.json")
        operations = read(IQFT / case / "iqft_operations.json")
        source, target, capped = (
            read(BASELINE / case / "min-depth" / name)
            for name in ("source.json", "target.json", "schedule_capped.json")
        )
        metadata = entries(source)
        storage = _storage(target, source, metadata)
        if any(capped[name] != value for name, value in storage.items()):
            raise ValueError("Original native full-target typed/storage binding changed")
        profile = source_batch_profile(wrapper, source, capped, metadata)
        demand = complete_price_demand(wrapper, row, operations, profile)
        audit = read(IQFT_AUDIT / (case + "_IQFT_audit.json"))
        mapping = {
            "t": "t",
            "clifford_cx": "cx",
            "clifford_h": "h",
            "clifford_s_or_sdg": "s",
            "x": "x",
            "clifford_cz": "cz",
            "clifford_z": "z",
        }
        expected = {
            mapping[name]: count
            for name, count in audit[
                "independently_reconstructed_complete_primitive_counts"
            ].items()
        }
        if demand["primitive_elementary_gate_counts"] != expected:
            raise ValueError(
                "Demand does not reconcile to the independent complete IQFT/source audit"
            )
        demand["provenance"] = {
            "source_iterate": relative(SOURCE / case / "iterate.json"),
            "source_iterate_sha256": digest(SOURCE / case / "iterate.json"),
            "synthesized_ledger": relative(IQFT / case / "synthesized_estimator_ledger.json"),
            "synthesized_ledger_sha256": digest(IQFT / case / "synthesized_estimator_ledger.json"),
            "independent_primitive_count_audit": relative(IQFT_AUDIT / (case + "_IQFT_audit.json")),
            "independent_primitive_count_audit_sha256": digest(
                IQFT_AUDIT / (case + "_IQFT_audit.json")
            ),
        }
        demand["parameterized_runtime_interface"] = bottleneck_lower_bound(demand)
        save(output / case / "hardware_demand.json", demand)
        save(output / case / "source_batch_profile.json", profile)
        rows.append(
            {
                "case": case,
                "logical_qubits": demand["logical_qubits"],
                "consumed_T_states": demand["consumed_T_states"],
                "primitive_elementary_gate_count": demand["primitive_elementary_gate_count"],
                "native_CCX_positions": demand[
                    "native_CCX_positions_before_exact_seven_T_expansion"
                ],
                "max_simultaneous_native_private_qubits": profile[
                    "max_simultaneous_native_private_qubits"
                ],
                "batch_maxima": profile["maxima"],
                "failure_requirements": demand["failure_requirements"],
            }
        )
        print(case, "full counts and native batch demand reconciled", flush=True)
    provenance = {
        "local_hardware_audit": DOCS[2],
        "architecture_calibrations_admitted": 0,
        "reviewed_primary_options": [
            {
                "role": "reaction dependency interface",
                "primary": "https://arxiv.org/pdf/1210.4626",
                "title": "Time-optimal quantum computation",
                "quantitative_clock_transferred": False,
            },
            {
                "role": "alternative T-state preparation",
                "primary": "https://arxiv.org/html/2409.17595v1",
                "title": "Magic-state cultivation",
                "published_reliability_transferred": False,
            },
            {
                "role": "memory, active volume and reaction interface",
                "primary": "https://arxiv.org/html/2211.15465",
                "title": "Active-volume architecture",
                "source_lowered_to_architecture": False,
            },
        ],
        "missing_matching_inputs": [
            "code distance",
            "protected data/factory/routing footprint",
            "accepted state error at current per-price target",
            "state retries and delivery",
            "reactive measurement mapping",
            "operation-specific clocks",
            "idle code-cycle exposure",
            "reset/readout/control reliability",
        ],
        "archived_C4_H8_capacity_source": "research/controlled_priority_completion/capacity_screen.py",
        "archived_source_family_cap_or_clocks_reused": False,
        "any_runtime_from_T_depth_alone": False,
    }
    save(output / "hardware_provenance.json", provenance)
    summary = {
        "passed": True,
        "local_only": True,
        "case_rows": rows,
        "full_elementary_counts_reconciled_to_independent_audit": True,
        "source_native_batch_profiles_reconciled": True,
        "physical_failure_allowance_exact": pair(PHYSICAL_ALLOWANCE),
        "prospective_allocation_exact": {name: pair(value) for name, value in ALLOCATIONS.items()},
        "physical_qubit_cap": None,
        "tau_grid": None,
        "architecture_rows": 0,
        "full_physical_fidelity_certificate": False,
        "full_physical_latency_certificate": False,
        "measurement_reaction_depth": None,
        "idle_or_code_cycle_opportunity_count": None,
        "new_financial_gate_replays": 0,
        "new_financial_price_samples": 0,
        "new_classical_price_timings": 0,
        "preexisting_Stage_C_jobs_edited": False,
        "missing_bounds_are_zero": False,
        "G5_closed": False,
        "elapsed_cpu_seconds": time.process_time() - started,
        "next": "Independently audit demands; propose a compatible finite data/factory/routing/control mapping at these exact error targets before assigning latency or admitting an architecture.",
    }
    save(output / "summary.json", summary)
    manifest(output, protocol)
    print(
        "H17/H18 complete-price demand prerequisite passed; physical implementation remains open",
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    (prepare if args.mode == "prepare" else run)(args.output)
