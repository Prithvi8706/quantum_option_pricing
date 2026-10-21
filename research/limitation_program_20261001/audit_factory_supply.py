"""Independent finite-p supply arithmetic; no physical factory adoption."""

import argparse
from datetime import datetime, timezone
from fractions import Fraction
from math import comb
from pathlib import Path
import shutil

from research.limitation_program_20261001.constant_library import digest
from research.limitation_program_20261001.experiment_checkpoint import (
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
    directory = PROGRAM / "H05_supply_run001"
    receipt = read(directory / "manifest.json")
    assert read(directory / "summary.json")["passed"]
    paths = [directory / "manifest.json"]
    for key, expected in receipt["files"].items():
        assert digest(ROOT / key) == expected
        paths.append(ROOT / key)
    for case in ("B4x12", "B8x52"):
        paths.append(PROGRAM / "H17_demand_run002" / case / "hardware_demand.json")
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
        before_independent_supply_arithmetic=True,
        frozen_inputs=frozen,
        producer_math_imported=False,
        physical_simulation_or_adoption=False,
        new_financial_prices_gates_tests=0,
    )
    save(output / "protocol.json", protocol)
    verify(protocol)
    census = read(directory / "factory_census.json")
    assert census["H05_factory_methods"] == 2
    assert census["H06_additional_conditional_interface_categories"] == 1
    assert census["physical_architectures_admitted"] == 0
    baseline, cultivation, ccz = census["method_rows"]
    assert [row["method"] for row in census["method_rows"]] == [
        "15-to-1",
        "cultivation-with-escape",
        "CCZ-and-catalysis-interface",
    ]
    for row in census["method_rows"]:
        for key in (
            "accepted_usable_output_error_upper_bound",
            "accepted_output_rate_per_second",
            "physical_factory_qubits",
            "measurement_reaction_depth",
            "executable_latency_seconds",
            "complete_physical_failure_upper_bound",
        ):
            assert row[key] is None
    case_audits = []
    for case in ("B4x12", "B8x52"):
        recorded = census["demand_cases"][case]
        demand = read(PROGRAM / "H17_demand_run002" / case / "hardware_demand.json")
        nt = demand["consumed_T_states"]
        nc = demand["native_CCX_positions_before_exact_seven_T_expansion"]
        residual = demand["remaining_single_qubit_T_positions_in_terminal_IQFT"]
        assert nt == 7 * nc + residual
        assert Fraction(*recorded["unchanged_T_state_error_target_exact"]) == Fraction(1, 1000 * nt)
        native = recorded["native_interface"]
        assert native["arithmetic_and_selector_reflection_CCZ_states"] == nc
        assert native["remaining_terminal_IQFT_T_states"] == residual
        assert Fraction(*native["required_each_CCZ_error_upper_exact"]) == Fraction(1, 2000 * nc)
        assert Fraction(*native["required_each_residual_T_error_upper_exact"]) == Fraction(
            1, 2000 * residual
        )
        assert not native["native_CCX_replacement_compiled"]
        catalyst = recorded["optional_catalysis_interface"]
        conversions = (residual + 1) // 2
        assert catalyst["total_consumed_CCZ_states"] == nc + conversions
        assert catalyst["additional_CCZ_states_consumed_to_supply_residual_T"] == conversions
        assert catalyst["initial_T_catalyst_states"] == 1
        assert not catalyst["independent_catalyzed_T_outputs_assumed"]
        assert catalyst["complete_magic_failure_upper"] is None
        case_audits.append(dict(case=case, exact_state_inventory_and_union_targets_passed=True))
    cascade = baseline["fixed_ideal_input_Z_cascade"]
    p, raw_cost = Fraction(1, 1000), Fraction(1)
    target = Fraction(*census["demand_cases"]["B4x12"]["unchanged_T_state_error_target_exact"])
    levels = []
    for index, row in enumerate(cascade["rows"], 1):
        assert row["level"] == index
        acceptance = (1 - p) ** 15
        upper = min(Fraction(1), comb(15, 3) * p**3 / acceptance)
        scale = 1 << 192
        next_p = Fraction(-(-(upper * scale).numerator // (upper * scale).denominator), scale)
        raw_cost *= 15 / acceptance
        assert Fraction(*row["ideal_bound"]["acceptance_probability_lower_exact"]) == acceptance
        assert Fraction(*row["ideal_bound"]["conditional_bad_output_upper_exact"]) == upper
        assert Fraction(*row["upward_dyadic_output_error_upper_exact"]) == next_p
        assert Fraction(*row["expected_raw_input_consumption_upper_exact"]) == raw_cost
        assert row["conditional_target_met"] == (next_p <= target)
        assert next_p >= upper
        levels.append(next_p <= target)
        p = next_p
    assert levels == [False, False, True]
    assert cascade["first_fixed_level_meeting_target"] == 3
    assert cascade["actual_Clifford_or_storage_fault_contribution"] is None
    assert not cascade["physical_factory_or_retry_rate_adopted"]
    reported = Fraction(*baseline["published_model_row"]["reported_output_error_estimate_exact"])
    assert reported == Fraction(45, 10**21)
    assert Fraction(
        *baseline["conditional_union_charge_if_reported_error_were_valid_upper_exact"]
    ) == (census["demand_cases"]["B4x12"]["unchanged_T_state_demand"] * reported)
    assert not baseline["published_model_row"]["reported_error_is_a_proved_device_upper_bound"]
    assert all(
        Fraction(*error) > target
        for error in cultivation["escaped_published_output_error_estimates_exact"]
    )
    assert cultivation["sign_entangling_erratum_requires_corrected_circuit_verification"]
    assert not cultivation["ungrown_low_error_row_is_usable_output"]
    q = Fraction(1, 1 << 33)
    ccz_upper = comb(8, 2) * q**2 / (1 - q) ** 8
    assert (
        Fraction(*ccz["one_fixed_ideal_eight_to_CCZ_bound"]["conditional_bad_output_upper_exact"])
        == ccz_upper
    )
    assert not ccz["accepted_native_replacement_or_factory"]
    save(
        output / "summary.json",
        dict(
            passed=True,
            local_only=True,
            case_inventory_audits=case_audits,
            exact_conditional_cascade_three_levels_verified=True,
            three_levels_necessary_claim=False,
            physical_factory_or_native_CCX_mapping_adopted=False,
            reported_paper_estimates_remain_conditional=True,
            catalyst_correlation_and_extra_consumed_CCZ_preserved=True,
            new_financial_prices_gates_tests=0,
        ),
    )
    manifest(output, protocol)
    print("Independent factory arithmetic audit passed; physical mapping remains open", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output.resolve())
