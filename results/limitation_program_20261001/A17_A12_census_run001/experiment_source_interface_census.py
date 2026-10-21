"""Existing fusion and actual divide-site census; no synthetic speedup."""

import argparse
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import shutil

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
from research.limitation_program_20261001.progress import ROOT


def run(output):
    output.relative_to(PROGRAM.resolve())
    assert not output.exists()
    paths = []
    for receipt_name in (
        "E02_archive_run003",
        "E02_financial_run002",
        "E02_financial_audit_run001",
    ):
        directory = PROGRAM / receipt_name
        receipt = read(directory / "manifest.json")
        assert read(directory / "summary.json")["passed"]
        paths.extend([directory / "summary.json", directory / "manifest.json"])
        for suffix in (
            ["ledger.json"]
            if receipt_name == "E02_archive_run003"
            else ["B4x12/iterate.json", "B8x52/iterate.json"]
            if receipt_name == "E02_financial_run002"
            else ["tiny_full_iterate_unitary_audit.json"]
        ):
            path = directory / suffix
            assert digest(path) == receipt["files"][relative(path)]
            paths.append(path)
    archived = read(PROGRAM / "E02_archive_run003/ledger.json")
    for row in archived["rows"]:
        path = ROOT / row["wrapper"]
        assert digest(path) == row["wrapper_sha256"]
        paths.append(path)
    paths.append(BASELINE / "manifest.json")
    legacy = {
        key.replace("\\", "/"): value for key, value in read(BASELINE / "manifest.json").items()
    }
    for case in ("B4x12", "B8x52"):
        directory = BASELINE / case / "min-depth"
        source = read(directory / "source.json")
        consumed = [directory / "source.json", directory / "target.json"]
        consumed.extend(directory / "leaves" / (key + ".json") for key in source["library_keys"])
        for path in consumed:
            assert digest(path) == legacy[path.relative_to(BASELINE).as_posix()]
        paths.extend(consumed)
    own = Path(__file__).resolve()
    paths.extend(
        ROOT / "research/limitation_program_20261001" / name
        for name in (own.name, "constant_library.py", "experiment_checkpoint.py", "progress.py")
    )
    frozen = {relative(path): digest(path) for path in paths}
    output.mkdir()
    shutil.copy2(own, output / own.name)
    protocol = dict(
        local_only=True,
        created_utc=datetime.now(timezone.utc).isoformat(),
        before_source_interface_census=True,
        frozen_inputs=frozen,
        original_financial_sources=["B4x12", "B8x52"],
        archived_estimator_rows=3,
        tiny_phase_evidence_reused_without_duplicate_credit=True,
        stop_rule="One divide-denominator inventory and fusion audit; no invented used classes",
        new_tests_gates_financial_replays_or_prices=0,
    )
    save(output / "protocol.json", protocol)
    verify(protocol)
    native_rows = []
    for case in ("B4x12", "B8x52"):
        directory = BASELINE / case / "min-depth"
        source, target = read(directory / "source.json"), read(directory / "target.json")
        metadata = {
            key: read(directory / "leaves" / (key + ".json")) for key in source["library_keys"]
        }
        counts = Counter(metadata[call["leaf"]]["op"] for call in source["forward_calls"])
        assert not any("div" in op.lower() for op in counts)
        assert not any("div" in node["op"].lower() for node in target["nodes"])
        wrapper = read(PROGRAM / "E02_financial_run002" / case / "iterate.json")
        assert wrapper["native_named_Y_copy_omitted"] and wrapper["old_output_buffer_reused"]
        assert wrapper["sequence"] == [
            "original compact F forward",
            "positive selector",
            "CZ(control,flag)",
            "literal inverse selector",
            "literal inverse original F",
            "signed controlled uniform reflection (includes final Z(control))",
        ]
        assert wrapper["resources"]["additional_logical_qubits"] == 0
        native_rows.append(
            dict(
                case=case,
                actual_forward_native_calls=sum(counts.values()),
                native_operations=dict(counts),
                actual_divide_sites=0,
                actual_denominator_classes=[],
                reciprocal_correction_prototypes_eligible_from_this_inventory=0,
                named_output_copy_boundary_already_omitted=True,
                controlled_phase_and_literal_inverse_structure_previously_audited=True,
                additional_removable_copy_boundary_proved=False,
                new_source_speedup_credited=False,
            )
        )
    archived_rows = []
    for row in archived["rows"]:
        wrapper = read(ROOT / row["wrapper"])
        if row["method"] == "hadamard":
            assert wrapper["fused_compute_phase_uncompute"] is True
        archived_rows.append(
            dict(
                model=row["model"],
                method=row["method"],
                wrapper=row["wrapper"],
                explicit_fused_phase_flag=wrapper.get("fused_compute_phase_uncompute"),
                actual_call_wave_half_operations=sum(
                    op["gate"] == "call_wave_half" for op in wrapper["operations"]
                ),
                wrapper_level_CX_operations=sum(op["gate"] == "cx" for op in wrapper["operations"]),
                null_fusion_flag_does_not_mean_unfused_source=True,
                further_copy_removal_requires_its_own_contract_proof=True,
                current_B4_B8_cost_transfer_allowed=False,
            )
        )
    tiny = read(PROGRAM / "E02_financial_audit_run001/tiny_full_iterate_unitary_audit.json")
    assert len(tiny) == 3 and sum(row["complete_clean_subspace_columns"] for row in tiny) == 40
    assert all(
        row["passed"]
        and row["control_zero_identity"]
        and row["control_one_signed_reflection_times_marker"]
        and row["missing_final_control_Z_negative_control_rejected"]
        for row in tiny
    )
    save(
        output / "certificate.json",
        dict(
            native_rows=native_rows,
            archived_rows=archived_rows,
            existing_tiny_phase_cases=3,
            existing_tiny_clean_columns=40,
            additional_tiny_phase_or_financial_replays=0,
            A12_scope=(
                "No divide classes in the accepted B4/B8 source; "
                "new quantile dividers are separate"
            ),
            A17_scope=(
                "Original source boundary already omitted; "
                "archived contracts retain separate copies"
            ),
            exact_reciprocal_for_new_quantile_or_other_family_certified=False,
            zero_additional_source_gain_credited=True,
        ),
    )
    save(
        output / "summary.json",
        dict(
            passed=True,
            local_only=True,
            actual_native_calls_inventoried=46164,
            current_financial_sources=2,
            actual_divide_sites=0,
            archived_estimator_rows_audited=3,
            existing_tiny_phase_cases_reconciled=3,
            new_tests_gates_financial_replays_or_prices=0,
            source_optimization_adopted=False,
        ),
    )
    manifest(output, protocol)
    print(
        "Fusion evidence reconciled; zero actual divide sites; no extra gain credited", flush=True
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output.resolve())
