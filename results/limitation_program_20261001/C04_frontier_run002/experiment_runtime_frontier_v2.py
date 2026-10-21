"""Exact ratio identities and conditional supply thresholds; no runtime claim."""

import argparse
from datetime import datetime, timezone
from decimal import Decimal
from fractions import Fraction
import json
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


def pair(value):
    return [value.numerator, value.denominator]


def conditional_ratios(classical_seconds, quantum_seconds):
    if classical_seconds <= 0 or quantum_seconds <= 0:
        raise ValueError("Positive compatible durations required")
    speedup = classical_seconds / quantum_seconds
    slowdown = quantum_seconds / classical_seconds
    tenfold_miss = 10 * slowdown
    assert speedup * slowdown == 1
    assert tenfold_miss == 10 / speedup
    return dict(
        speedup_exact=pair(speedup),
        slowdown_exact=pair(slowdown),
        tenfold_budget_miss_exact=pair(tenfold_miss),
        onefold_reached=quantum_seconds <= classical_seconds,
        tenfold_reached=10 * quantum_seconds <= classical_seconds,
    )


def run(output):
    output.relative_to(PROGRAM.resolve())
    assert not output.exists()
    consumed = []
    for name in ("C09_audit_run001", "H17_demand_run002", "H17_demand_audit_run001"):
        directory = PROGRAM / name
        assert read(directory / "summary.json")["passed"]
        receipt = read(directory / "manifest.json")
        paths = [directory / "summary.json", directory / "protocol.json"]
        if name == "H17_demand_run002":
            paths.extend(directory / case / "hardware_demand.json" for case in ("B4x12", "B8x52"))
        for path in paths:
            assert digest(path) == receipt["files"][relative(path)]
        consumed.extend([directory / "manifest.json", *paths])
    own = Path(__file__).resolve()
    consumed.extend(
        ROOT / "research/limitation_program_20261001" / name
        for name in (own.name, "constant_library.py", "experiment_checkpoint.py", "progress.py")
    )
    frozen = {relative(path): digest(path) for path in consumed}
    output.mkdir()
    shutil.copy2(own, output / own.name)
    protocol = dict(
        created_utc=datetime.now(timezone.utc).isoformat(),
        local_only=True,
        before_ratio_and_supply_calculations=True,
        frozen_inputs=frozen,
        cases=["B4x12", "B8x52"],
        quantum_accuracy_dollars_exact=[1, 100],
        timing_selection="All six actually measured scale=1 C09 confirmation rows",
        hypothetical_ratio_identity_pairs=[[2, 1], [2, 4], [20, 1]],
        no_physical_clock_or_capacity_assumptions=True,
        no_source_depth_to_physical_runtime_conversion=True,
        stop_rule="One exact identity check per emitted row; absent complete times stay null",
        new_financial_prices_gates_tests=0,
    )
    save(output / "protocol.json", protocol)
    verify(protocol)
    timing = json.loads(
        (PROGRAM / "C09_audit_run001/summary.json").read_text(encoding="utf-8"),
        parse_float=Decimal,
    )
    rows = []
    for candidate in timing["candidate_timing_rows"]:
        if candidate["recorded_primary_convention"] != "measured confirmation":
            continue
        assert candidate["scale"] == Decimal(1)
        case = candidate["case"]
        demand_path = PROGRAM / "H17_demand_run002" / case / "hardware_demand.json"
        demand = read(demand_path)
        assert demand["complete_executable_latency_seconds"] is None
        assert not demand["full_physical_fidelity_certificate"]
        tc = Fraction(candidate["measured_median_wall_seconds"])
        assert tc == Fraction(candidate["recorded_primary_t_c_seconds"])
        nt = demand["consumed_T_states"]
        source_t = demand["source_batch_profile"]["financial_resources_per_iterate"]["t_count"]
        identities = [
            conditional_ratios(Fraction(a), Fraction(b))
            for a, b in protocol["hypothetical_ratio_identity_pairs"]
        ]
        onefold_rate, tenfold_rate = Fraction(nt, 1) / tc, 10 * Fraction(nt, 1) / tc
        assert tenfold_rate == 10 * onefold_rate
        # Equality at these supply-only lower bounds gives ratio 1 and 10.
        assert conditional_ratios(tc, Fraction(nt, 1) / onefold_rate)["onefold_reached"]
        assert conditional_ratios(tc, Fraction(nt, 1) / tenfold_rate)["tenfold_reached"]
        epsilon = Fraction(candidate["epsilon_dollars"])
        rows.append(
            dict(
                case=case,
                classical_method=candidate["method"],
                measured_classical_wall_seconds_exact=pair(tc),
                classical_accuracy_target_dollars_exact=pair(epsilon),
                measured_classical_pooled_halfwidth_exact=pair(
                    Fraction(candidate["pooled_hw16_dollars"])
                ),
                classical_n_run_per_scramble=candidate["actual_n_run_per_scramble"],
                classical_evidence_is_measured_confirmation=True,
                classical_full_coverage_qualification=False,
                same_nominal_accuracy_target=epsilon == Fraction(1, 100),
                common_continuous_or_finite_input_law_certified=False,
                comparable_complete_runtimes_available=False,
                source_only_quantum_seconds=None,
                complete_quantum_seconds=None,
                actual_complete_speedup_ratio=None,
                actual_complete_slowdown_ratio=None,
                actual_tenfold_budget_miss_ratio=None,
                actual_onefold_reached=None,
                actual_tenfold_reached=None,
                native_financial_subroutine_T_count_per_G_iteration=source_t,
                complete_logical_T_state_demand=nt,
                logical_T_depth_is_not_physical_reaction_depth=True,
                conditional_required_accepted_T_states_per_second_onefold_exact=pair(onefold_rate),
                conditional_required_accepted_T_states_per_second_tenfold_exact=pair(tenfold_rate),
                rate_scope=(
                    "Protected usable delivered states; no free initial stock "
                    "or retry/routing credit"
                ),
                supply_threshold_is_necessary_not_sufficient=True,
                rate_is_measured_or_architecture_certified=False,
                hypothetical_identity_checks=identities,
                tenfold_target_miss_does_not_imply_quantum_slowdown=True,
            )
        )
    assert len(rows) == 6
    assert sum(row["same_nominal_accuracy_target"] for row in rows) == 4
    save(
        output / "comparison.json",
        dict(
            rows=rows,
            identity="10*T_Q/T_C = 10/(T_C/T_Q)",
            modeled_times_are_not_measured_confirmation=True,
            complete_advantage_established=False,
            source_only_advantage_established=False,
            physical_bottleneck_lower_bound_is_not_executable_latency=True,
        ),
    )
    save(
        output / "summary.json",
        dict(
            passed=True,
            local_only=True,
            measured_confirmation_rows=6,
            same_nominal_accuracy_rows=4,
            finer_classical_accuracy_rows=2,
            actual_complete_runtime_ratios_available=0,
            conditional_supply_thresholds=12,
            identity_checks_passed=True,
            full_continuous_price_or_physical_certificate=False,
            new_financial_prices_gates_tests=0,
            quantum_advantage_established=False,
        ),
    )
    manifest(output, protocol)
    print(
        "Six measured timing rows; twelve conditional supply thresholds; actual ratios null",
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output.resolve())
