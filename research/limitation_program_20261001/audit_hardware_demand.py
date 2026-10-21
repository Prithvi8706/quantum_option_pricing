"""Independently reconcile immutable logical demand and necessary fault targets."""

import argparse
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET

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


def run(output):
    output.relative_to(PROGRAM.resolve())
    assert not output.exists()
    demand_dir = PROGRAM / "H17_demand_run002"
    iqft_dir = PROGRAM / "E02_IQFT_audit_run001"
    assert read(demand_dir / "summary.json")["passed"]
    assert read(iqft_dir / "summary.json")["passed"]
    output.mkdir()
    frozen = {}
    for directory in (demand_dir, iqft_dir, PROGRAM / "H17_demand_run001"):
        receipt = read(directory / "manifest.json")
        frozen.update(receipt["files"])
        frozen.update(receipt["frozen_inputs"])
        frozen[relative(directory / "manifest.json")] = digest(directory / "manifest.json")
    code = Path(__file__).resolve()
    frozen[relative(code)] = digest(code)
    shutil.copy2(code, output / code.name)
    protocol = dict(
        created_utc=datetime.now(timezone.utc).isoformat(),
        local_only=True,
        before_independent_demand_reconciliation=True,
        cases=["B4x12", "B8x52"],
        new_financial_candidates_or_gates=0,
        new_pytest_cases=0,
        method=(
            "Independent already-audited complete primitive counts, original "
            "financial call/batch allocation and fanout reconstruction, exact "
            "marginal union requirements; no producer demand code imported"
        ),
        frozen_inputs=frozen,
    )
    save(output / "protocol.json", protocol)
    verify(protocol)
    mapping = {
        "t": "t",
        "cx": "clifford_cx",
        "h": "clifford_h",
        "s": "clifford_s_or_sdg",
        "x": "x",
        "cz": "clifford_cz",
        "z": "clifford_z",
    }
    rows = []
    for case in protocol["cases"]:
        demand = read(demand_dir / case / "hardware_demand.json")
        audit = read(iqft_dir / (case + "_IQFT_audit.json"))
        wrapper = read(PROGRAM / "E02_financial_run002" / case / "iterate.json")
        source = read(BASELINE / case / "min-depth/source.json")
        schedule = read(BASELINE / case / "min-depth/schedule_capped.json")
        assert demand["binding"] == wrapper["binding"]
        primitives = {
            k: audit["independently_reconstructed_complete_primitive_counts"][v]
            for k, v in mapping.items()
        }
        assert demand["primitive_elementary_gate_counts"] == primitives
        assert demand["primitive_elementary_gate_count"] == sum(primitives.values())
        assert demand["consumed_T_states"] == primitives["t"] == audit["full_T_count"]
        assert demand["full_logical_serial_T_depth"] == audit["full_logical_serial_T_depth"]
        assert demand["logical_qubits"] == audit["logical_qubits"]
        stages = Counter()
        for stage in demand["primitive_elementary_gate_counts_by_stage"].values():
            stages.update(stage)
        assert dict(stages) == primitives
        Q, shots = demand["controlled_G_iterations"], demand["serial_fresh_shots"]
        assert Q == 983025 and shots == 15
        assert demand["financial_graph_directions"] == 2 * Q
        assert demand["native_CCX_positions_before_exact_seven_T_expansion"] == (
            Q * wrapper["resources"]["ccx"]
        )
        profile = read(demand_dir / case / "source_batch_profile.json")
        assert profile == demand["source_batch_profile"]
        assert profile["retained_SSA_qubits"] == sum(schedule["widths"])
        assert profile["batch_count_per_financial_direction"] == len(schedule["groups"])
        assert demand["financial_batches_executed"] == 2 * Q * len(schedule["groups"])
        expected_copies = 0
        seen = set()
        for emitted, batch, group in zip(
            profile["batches"], wrapper["financial_batches"], schedule["groups"], strict=True
        ):
            assert emitted["wave"] == group["wave"] == batch["wave"]
            assert [c["call_index"] for c in emitted["calls"]] == group["call_indices"]
            fanout = Counter()
            active_arguments = 0
            private = 0
            for recorded, original in zip(emitted["calls"], batch["calls"], strict=True):
                index = original["call_index"]
                assert index not in seen
                seen.add(index)
                call = source["forward_calls"][index]
                assert recorded["leaf"] == call["leaf"] == original["leaf"]
                assert recorded["private_qubits"] == original["private_width"]
                private += original["private_width"]
                active_arguments += sum(schedule["widths"][a] for a in call["args"])
                fanout.update(call["args"])
            assert emitted["components"]["private_qubits"] == private
            assert private == group["private_scratch_qubits"]
            assert emitted["argument_copy_CX_per_direction"] == 2 * active_arguments
            assert emitted["max_shared_SSA_argument_occurrences"] == max(fanout.values())
            assert group["copy_rounds"] == max(fanout.values())
            expected_copies += 2 * active_arguments
        assert seen == set(range(len(source["forward_calls"])))
        assert demand["financial_argument_copy_CX_per_price"] == 2 * Q * expected_copies
        peak = max(b["components"]["private_qubits"] for b in profile["batches"])
        assert profile["max_simultaneous_native_private_qubits"] == peak
        assert wrapper["private_base"] + peak == demand["logical_qubits"]
        requirements = demand["failure_requirements"]
        allocations = {name: Fraction(*v) for name, v in requirements["allocation_exact"].items()}
        assert allocations == dict(
            data=Fraction(1, 1000), magic_states=Fraction(1, 1000), control=Fraction(1, 1000)
        )
        assert sum(allocations.values()) == Fraction(
            *requirements["physical_failure_allowance_exact"]
        )
        for name, field, count in (
            ("magic_states", "required_error_per_consumed_T_state_exact", primitives["t"]),
            (
                "data",
                "required_data_error_per_elementary_logical_gate_exact",
                sum(primitives.values()),
            ),
            (
                "control",
                "required_control_error_per_elementary_logical_operation_exact",
                sum(primitives.values()),
            ),
        ):
            assert Fraction(*requirements[field]) * count == allocations[name]
        for field in (
            "idle_or_code_cycle_opportunity_count",
            "code_distance",
            "physical_control_reset_feedback_opportunity_count",
            "complete_execution_failure_upper",
        ):
            assert requirements[field] is None
        assert not requirements["known_gate_union_targets_cover_idle_and_feedback"]
        assert demand["architecture_rows"] == [] and demand["physical_qubit_cap"] is None
        assert demand["complete_executable_latency_seconds"] is None
        assert not demand["full_physical_fidelity_certificate"]
        assert demand["no_archived_C4_H8_physical_cap_or_clock_transferred"]
        rows.append(
            dict(
                case=case,
                passed=True,
                full_T_count=primitives["t"],
                elementary_operations=sum(primitives.values()),
                source_calls=len(seen),
                batch_count=len(profile["batches"]),
                private_peak=peak,
                full_physical_latency_or_fidelity_certified=False,
            )
        )
    old = read(PROGRAM / "H17_demand_run001/summary.json")
    assert not old["passed"]
    suites = ET.parse(demand_dir / "tests.xml").getroot().findall("testsuite")
    assert sum(int(s.get("tests", 0)) for s in suites) == 43
    assert all(int(s.get(f, 0)) == 0 for s in suites for f in ("errors", "failures", "skipped"))
    save(
        output / "summary.json",
        dict(
            passed=True,
            local_only=True,
            cases=rows,
            independent_full_demand_and_union_requirement_audit=True,
            producer_distinct_tests_reconciled=43,
            new_pytest_cases=0,
            new_financial_candidates_or_gates=0,
            prior_schema_failure_preserved=True,
            physical_schedule_or_whole_execution_fidelity_certified=False,
            G5_closed=False,
        ),
    )
    manifest(output, protocol)
    print("Independent complete logical hardware demand audit PASS; G5 remains open", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output.resolve())
