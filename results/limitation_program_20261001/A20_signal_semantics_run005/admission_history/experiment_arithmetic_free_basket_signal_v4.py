"""A20 restricted paid comparator-phase component; author-only until ROOT READY.

Prepare copies and verifies bytes only. Run makes one prescribed component
construction and exact finite checks. It never emits a complete price oracle.
"""

from __future__ import annotations

import argparse
from collections import Counter
import sys
import time

from research.limitation_program_20261001.a20_signal_receipt_v4 import (
    PROGRAM,
    RESEARCH,
    ROOT,
    Receipt,
    require,
)

SELECTED = {
    "research/journal_sprint/reversible_fixed_point.py": (
        "52584dee87c84541b9f9e2f070114d7276de3d49d306d33c471214795b729b8b"
    ),
    "research/controlled_source_completion/exact_lookup.py": (
        "a63e27f9995adcacad707808fd6565fe9bf62920b73203c3021dd67861822b6c"
    ),
    "results/limitation_program_20261001/E22_census_run002/B4x12_predicate_census.json": (
        "35b9cf84b23b10d871dbb64e5af1bdfe9c9ce58db811ac089f7729c6eebfabb3"
    ),
    "results/limitation_program_20261001/A17_quantile_divider_run001/exact_CCX_phase_proof.json": (
        "714698f92a1d94f61ec26f746e77f9a7aa936a41308a9b82e6e93495fa92a55c"
    ),
    "research/limitation_program_20261001/temporary_and_fulladder.py": (
        "34bb7f93d07b51de54c44d2fd8c124678d280db01066df848bb7eac43aa2dfeb"
    ),
}
TARGET = PROGRAM / "A10_coefficient_run001/B4x12/min-depth/target.json"
CENSUS = PROGRAM / "E22_census_run002/B4x12_predicate_census.json"
SUPPORT = PROGRAM / "E03_support_audit_run002/B4x12_audit.json"
PHASE = PROGRAM / "A17_quantile_divider_run001/exact_CCX_phase_proof.json"


def execute(receipt, protocol):
    receipt.verify_loaded(protocol)
    receipt.verify(True)
    receipt.check(admission=True)
    # This is the first import or invocation of the NEW scientific builder.
    from research.limitation_program_20261001 import arithmetic_free_basket_signal_v4 as builder

    receipt.verify_loaded(protocol)
    builder.CHECK = receipt.check
    builder.GATE_VISITS = 0
    proof = builder.phase_premise(
        receipt.read(PHASE), receipt.read_bytes(RESEARCH / "temporary_and_fulladder.py")
    )
    helpers = builder.native_helpers(
        receipt.read_bytes(ROOT / "research/journal_sprint/reversible_fixed_point.py"),
        receipt.read_bytes(ROOT / "research/controlled_source_completion/exact_lookup.py"),
    )
    work_cpu, work_wall = time.process_time(), time.monotonic()
    result = builder.component_experiment(
        receipt.read(TARGET), receipt.read(CENSUS), receipt.read(SUPPORT), helpers
    )
    construction_cpu = time.process_time() - work_cpu
    construction_wall = time.monotonic() - work_wall
    receipt.check(admission=True)
    require(len(result["checks"]) == 2608, "Fixed complete component check inventory")
    counts = dict(Counter(row["family"] for row in result["checks"]))
    require(
        counts
        == {
            "QROM8_word72": 32,
            "controlled_QROM8_word72": 64,
            "native_signed_LT72": 304,
            "native53_phase": 128,
            "tiny_complete_operator": 32,
            "native53_pair_phase": 2048,
        },
        "Every fixed basis/operator family completed",
    )
    receipt.write(
        "source_binding.json",
        {
            "schema": "A20-restricted-native-stock-source-binding-v2",
            "selected_expected_sha256": receipt.ready["selected_prerequisite_sha256"],
            "templates": result["templates"],
            "knots_raw": result["knots_raw"],
            "native_words": result["native_words"],
            "offline_native_scalar_evaluations": result["offline_native_scalar_evaluations"],
            "offline_truth_construction_charged": True,
            "general_q32_reachability_or_law_claim": False,
        },
    )
    receipt.write(
        "native_truth.json",
        {
            "rows": result["rows"],
            "boundary_cases": result["boundary_cases"],
            "offline_pair_truth_records": result["offline_pair_truth_records"],
            "boundary_words_are_interface_only_not_proven_reachable": True,
        },
    )
    receipt.write(
        "gate_recipes.json",
        {
            "schema": "A20-exact-paid-gate-recipes-v2",
            "recipes": result["recipes"],
            "tiny_recipe": result["tiny_recipe"],
            "one_component_construction": True,
            "original_word_width": 72,
            "original_fractional_bits": 40,
            "native_reference_bits": 53,
            "reference_upper19_zero_promised": True,
            "reference_and_selector_block_output_garbage_allowed": True,
            "stock_address_and_internal_scratch_restored": True,
            "full_pricing_source_emitted": False,
        },
    )
    receipt.write(
        "component_checks.json",
        {
            "checks": result["checks"],
            "family_counts": counts,
            "total_internal_checks": 2608,
            "new_test_credit": 0,
            "internal_checks_are_not_distinct_pytest_or_financial_fixtures": True,
            "native_pair_phase_test_view": result["native_pair_phase_test_view"],
            "exact_gate_state_visits": result["exact_gate_state_visits"],
            "native53_pair_tests_are_H_removed_reference_test_view": True,
        },
    )
    receipt.write(
        "exact_counting_proof.json",
        {
            **result["exact_counting_proof"],
            "reference_upper19_zero_promised": True,
            "strict_F_domain": [0, (1 << 53) - 1],
            "control_zero_full_identity": True,
            "threshold_transform_or_full_pricing_oracle_supplied": False,
        },
    )
    receipt.write(
        "resource_ledger.json",
        {
            "resources": result["resources"],
            "tiny_resource": builder.resource_row(result["tiny_recipe"]),
            "whole_source_comparison": result["whole_source_comparison"],
            "offline_native_evaluations": 8,
            "offline_pair_truth_records": 64,
            "constructed_recipe_count_including_tiny": 6,
            "component_work_CPU_seconds_including_emission_and_checks": construction_cpu,
            "component_work_wall_seconds_including_emission_and_checks": construction_wall,
            "native_CCX_absolute_phase_and_seven_T_paid": True,
            "QROM_address_selection_copy_cleanup_and_H_Z_CZ_paid": True,
            "depths_are_conservative_recipe_upper_bounds_not_full_source_schedules": True,
            "classical_offline_build_storage_and_load_amortization_not_assumed_free": True,
        },
    )
    receipt.write("phase_premise.json", proof)
    receipt.verify_loaded(protocol)
    receipt.verify(True)
    summary = {
        "schema": "A20-comparator-phase-component-summary-v4",
        "role": "producer",
        "completed": True,
        "passed": True,
        "budget_censored": False,
        "component_semantics_verified": True,
        "independent_audit_still_required": True,
        "internal_component_checks": 2608,
        "offline_native_scalar_evaluations": 8,
        "restricted_pair_truth_rows": 64,
        "interface_boundary_cases": 10,
        "new_test_credit": 0,
        "new_gate_replay_credit": 0,
        "new_financial_replay_credit": 0,
        "general_full72_or_q32_oracle": False,
        "threshold_QSP_transform": False,
        "complete_financial_bias_allocation": None,
        "full_G2": False,
        "adoption": False,
        "quantum_advantage": False,
        "original_scientific_precision_and_strict_ties_retained": True,
        "physical_runtime": None,
        "process_CPU_seconds_at_preseal_checkpoint": time.process_time(),
        "creation_clock_wall_seconds_at_preseal_checkpoint": time.monotonic() - receipt.started,
    }
    receipt.seal(summary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run"))
    parser.add_argument("--ready", required=True)
    parser.add_argument("--ready-sha256", required=True)
    parser.add_argument("--protocol-sha256")
    arguments = parser.parse_args()
    receipt = None
    try:
        receipt = Receipt("producer", arguments.ready, arguments.ready_sha256, arguments.mode)
        require(
            all(
                receipt.ready["selected_prerequisite_sha256"].get(key) == value
                for key, value in SELECTED.items()
            ),
            "Actual native helper, census and phase pins",
        )
        if arguments.mode == "prepare":
            require(
                arguments.protocol_sha256 is None, "No prepared-protocol pin before preparation"
            )
            print("PREPARED_PROTOCOL_SHA256=" + receipt.prepare())
        else:
            protocol = receipt.admit_run(arguments.protocol_sha256)
            execute(receipt, protocol)
            print("A20 restricted component terminal PASS; zero program fixture credit")
        return 0
    except BaseException as error:
        if receipt is not None:
            receipt.fail(error)
        print(type(error).__name__ + ": " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
